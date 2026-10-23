"""Release regressions. Synthetic fixtures only; no external API requests."""
from pathlib import Path
import ast
import os
import subprocess
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parents[1]))
import app


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    state = tmp_path / 'state'
    state.mkdir()
    monkeypatch.setattr(app, 'STATE', state)
    monkeypatch.setattr(app, 'ROOTS', [tmp_path.resolve()])
    app.PLANS.clear()
    root = tmp_path / 'demo'
    root.mkdir()
    original = '# Demo\n\n## Rules\n\nReview inputs.\n\n## Output\n\nBe concise.\n'
    (root / 'SKILL.md').write_text(original, encoding='utf-8')
    return TestClient(app.app), root, original


def headers():
    return {'Authorization': 'Bearer ' + app.TOKEN, 'x-skill-loom': '1'}


def operation(anchor, content):
    return {'type': 'insert', 'path': 'SKILL.md', 'anchor': anchor,
            'content': content, 'reason': 'Synthetic regression'}


def test_rejects_heading_created_by_earlier_operation(sandbox):
    _, root, original = sandbox
    plan = {'operations': [operation('## Rules', '### Newly invented heading\nNew guidance.'),
                           operation('### Newly invented heading', 'More guidance.')]}
    with pytest.raises(Exception) as error:
        app.make_plan(root, 'synthetic report', plan, {'SKILL.md': original}, [])
    assert getattr(error.value, 'status_code', None) == 400
    assert (root / 'SKILL.md').read_text(encoding='utf-8') == original
    assert app.PLANS == {}


def test_rejects_heading_inside_code_fence(sandbox):
    _, root, original = sandbox
    original += '\n```markdown\n## Code-only heading\n```\n'
    (root / 'SKILL.md').write_text(original, encoding='utf-8')
    with pytest.raises(Exception) as error:
        app.make_plan(root, 'synthetic report', {'operations': [operation('## Code-only heading', 'New guidance.')]}, {'SKILL.md': original}, [])
    assert getattr(error.value, 'status_code', None) == 400
    assert (root / 'SKILL.md').read_text(encoding='utf-8') == original


def test_repeated_inserts_under_original_heading_remain_supported(sandbox):
    _, root, original = sandbox
    plan = app.make_plan(root, 'synthetic report', {'operations': [operation('## Rules', 'First new rule.'), operation('## Rules', 'Second new rule.')]}, {'SKILL.md': original}, [])
    assert 'First new rule.' in plan['changes'][0]['after']
    assert 'Second new rule.' in plan['changes'][0]['after']
    assert (root / 'SKILL.md').read_text(encoding='utf-8') == original


@pytest.mark.parametrize('length', ['bad', '-1', '1.2', ''])
def test_invalid_content_length_returns_400(sandbox, length):
    client, root, original = sandbox
    response = client.post('/api/scan', content='{}', headers={**headers(), 'content-type': 'application/json', 'content-length': length})
    assert response.status_code == 400
    assert response.json()['detail'] == 'Invalid Content-Length header.'
    assert (root / 'SKILL.md').read_text(encoding='utf-8') == original


@pytest.mark.parametrize('length', ['1200001', '9' * 100])
def test_oversized_content_length_returns_413(sandbox, length):
    client, _, _ = sandbox
    response = client.post('/api/scan', content='{}', headers={**headers(), 'content-type': 'application/json', 'content-length': length})
    assert response.status_code == 413


def test_status_reports_release_version(sandbox):
    client, _, _ = sandbox
    response = client.get('/api/status', headers=headers())
    assert response.status_code == 200
    assert response.json()['version'] == app.APP_VERSION == '1.0.0'


def test_direct_import_default_root_is_home(tmp_path):
    env = os.environ.copy()
    env.pop('SKILL_LOOM_ROOTS', None)
    env['SKILL_LOOM_STATE'] = str(tmp_path / 'subprocess-state')
    result = subprocess.run([sys.executable, '-c', 'from pathlib import Path; import app; assert app.ROOTS == [Path.home().resolve()]'], cwd=Path(__file__).parents[1], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_launcher_default_root_is_home_without_starting_server():
    source = (Path(__file__).parents[1] / 'start.py').read_text(encoding='utf-8')
    prefix = source.split('\nimport app\n', 1)[0]
    namespace = {}
    # Executed in a subprocess so launcher argument/environment changes stay local.
    check = prefix + "\nassert os.environ['SKILL_LOOM_ROOTS'] == str(Path.home().resolve())\n"
    env = os.environ.copy()
    result = subprocess.run([sys.executable, '-c', check], env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_bundled_example_is_discoverable_and_previewable(sandbox):
    _, _, _ = sandbox
    base = Path(__file__).parents[1]
    root = base / 'examples' / 'demo-skill'
    before = (root / 'SKILL.md').read_bytes()
    report = (base / 'examples' / 'sample-report.md').read_text(encoding='utf-8')
    context, omitted = app.build_context(root, report)
    assert '## Review procedure' in context['allowed_insert_anchors']['SKILL.md']
    result = {'summary': 'Synthetic preview, not AI quality evidence.', 'operations': [operation('## Review procedure', 'Tie each proposed action to a specific observation in the supplied report.')]}
    plan = app.make_plan(root, report, result, context['editable_files'], omitted)
    assert len(plan['changes']) == 1
    assert plan['changes'][0]['before'] != plan['changes'][0]['after']
    assert (root / 'SKILL.md').read_bytes() == before


def test_model_contract_requires_semantic_delta_and_grounded_explanations():
    assert 'compare each candidate lesson against ALL existing editable_files by meaning' in app.SYSTEM
    assert 'A paraphrase of an existing instruction is still a duplicate.' in app.SYSTEM
    assert 'summary must describe only files and sections actually changed' in app.SYSTEM
    assert 'Do not invent a warning to fill the field.' in app.SYSTEM
    assert 'Never contradict the accepted lesson in the warnings.' in app.SYSTEM
