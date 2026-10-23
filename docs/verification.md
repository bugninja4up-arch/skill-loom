# Testing and compatibility

## Run the tests

From an activated project virtual environment:

```sh
python -m pip install -r requirements-dev.txt
python -m pip check
python -m pytest -q
```

The default suite uses synthetic fixtures and simulated provider responses. It requires no API key and makes no paid model requests. It covers authentication, request validation, JSON parsing and error handling, additive previews, apply/restore, byte-exact restoration, stale edits, duplicate reports, path traversal, symbolic-link targets, nested skills, and insertion-heading restrictions.

An optional archive discovery test is skipped unless `SKILL_LOOM_TEST_ARCHIVE` points to a directory containing a `pentest` skill. You do not need an external archive to run the normal suite. Never upload private skills or archives as test fixtures.

## Dependency versions

`constraints-tested.txt` records the dependency versions used with Python 3.12 on Linux. To use those versions in a compatible environment:

```sh
python -m pip install -r requirements-dev.txt -c constraints-tested.txt
```

These constraints are not a hash-locked dependency supply-chain guarantee. Recheck compatibility and third-party licenses when versions change. The tested HTTPX-backed TestClient emits a Starlette deprecation warning; it does not fail the current suite and may require maintenance as dependencies evolve.

## Compatibility

The source targets Python 3.10+. The exercised configuration is Linux with Python 3.12. Windows, macOS, and other Python versions have not been exercised to the same extent; the installation commands for those systems follow standard Python virtual-environment conventions. A GitHub Actions matrix is provided, but a workflow file alone is not evidence of a successful hosted run.

The app expects an OpenAI-compatible Chat Completions response containing one valid JSON update plan. Provider compatibility, availability, cost, and output quality can change. Saving API settings confirms neither connectivity nor key validity; generate a preview to check your configuration.

## Review a real provider response

Use a disposable copy of the [bundled example](example-walkthrough.md) and your own provider key. A real request sends the report and selected Markdown context to that provider and may incur charges.

Check that the preview is useful, grounded in the report, non-duplicative, and in the skill's language. Apply only a proposal you accept, then restore it and compare the file bytes with your saved baseline. A successful example does not establish correctness for unrelated reports or future model responses.

## Safety boundaries

Keep the app on localhost, use one process, and select a narrow allowed folder. Do not expose it to untrusted users or use directories writable by an attacker. Path and stale-edit checks are not a filesystem sandbox against a competing local process, and the declared Content-Length check is not a general streaming denial-of-service defense.

Mechanical validation cannot rule out hallucinations, semantic duplicates, contradictions, prompt injection, or unsafe advice. Review every proposed change, and keep independent backups or version control for important skills.
