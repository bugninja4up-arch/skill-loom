# Skill Loom

Turn reports into reviewable additions to agent skills — with diffs, local backups, and rollback.

Skill Loom is a local web app for improving Markdown agent skills from reports. Select a skill, paste or upload a report, and use your AI API to propose reusable guidance. Review the diff before applying changes, and restore a backup when needed.

## Install and run

You need **Git, Python 3.10+**, and an API provider supporting OpenAI-compatible Chat Completions. Python 3.12 on Linux is the tested configuration. AI requests require your own key and may incur provider charges.

### macOS / Linux

```sh
git clone "https://github.com/bugninja4up-arch/skill-loom.git"
cd skill-loom
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python start.py --root ./examples
```

### Windows PowerShell

```powershell
git clone "https://github.com/bugninja4up-arch/skill-loom.git"
cd skill-loom
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python start.py --root ./examples
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of `python` for the install and launch commands; activation is not required. If you prefer a ZIP, extract the source download, open its `skill-loom` folder, and start at the virtual-environment step.

Open the full session URL printed in the terminal, including `#token=...`. Keep it private: it grants access to the allowed folders. There is no bundled AI model and no account registration in the app.

## Use it in five steps

1. In **Folder path**, enter `./examples`, click **Scan folder**, and select **Demo report reviewer**. Paths refer to the computer running the server; a direct `SKILL.md` path is also accepted.
2. Paste or upload `examples/sample-report.md`.
3. Open **API settings** and enter your provider's base URL, model ID, and API key. Use a base URL such as `https://api.openai.com/v1`, without `/chat/completions`. Saving settings does not verify the connection.
4. Click **Generate preview**. Review the summary, warnings, and **Diff / Before / After** views. Generating a preview does not change the skill.
5. Choose **Apply changes** only if the additions are useful and correct. Use **History → Restore** to undo them; restore refuses to overwrite newer edits.

The bundled example is original synthetic material. See [the example walkthrough](docs/example-walkthrough.md) for what to check in the proposal.

For your own skills, restart with a narrow allowed directory:

```sh
python start.py --root "/path/to/your/skills"
```

Repeat `--root` to allow multiple directories. Without it, the default is your home directory; choosing a smaller folder is recommended. Keep the default localhost binding and use one server process, not multiple workers. This is a local, single-user tool, not a public hosting service.

## Configure an AI provider

Use a provider implementing the required Chat Completions JSON response format. Compatibility and model quality vary. Endpoint and model can also be set at launch:

```sh
python start.py --root ./examples --endpoint https://vyceai.com/v1 --model deepseek-v4-flash
```

Supply your own key in **API settings**, or set `OPENAI_API_KEY` in the server process environment. Keys entered in the interface stay in page memory and are cleared on reload. If you change providers, supply the new provider's key; the server does not forward its default key to a different endpoint.

| Environment variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Default provider key |
| `OPENAI_API_BASE` | Provider base URL; `OPENAI_BASE_URL` is a fallback alias |
| `SKILL_LOOM_MODEL` | Model ID; default `gpt-4.1-mini` |
| `SKILL_LOOM_STATE` | Backup directory; default local `.state/` |
| `SKILL_LOOM_JSON_MODE` | JSON output mode is on by default; set to `0` only if your provider requires it |

Requests are not automatically retried. If authentication fails, the provider times out, or its plan is invalid, inspect the displayed error and provider settings before trying again. The app never executes provider text or commands from reports.

## Supported input and limits

- UTF-8 Markdown skills with a `SKILL.md` file.
- Reports pasted as text or uploaded as `.md` / `.txt`; no PDF, Word, image, or ZIP import.
- Additions only: insert under an existing Markdown section or create a new Markdown reference. There is no intentional deletion or replacement, YAML editing, command execution, or remote registry sync.
- Reports: 20–160,000 characters; uploads: 160,000 bytes; skill files: up to 180,000 bytes each.
- Context: up to 20 complete files within 210,000 characters. The preview identifies included files and warns about omitted files; omitted existing files cannot be edited.
- Plans: up to 12 operations and 30,000 added characters. They expire after one hour and are lost on restart; saved backups remain.

## Privacy and safe use

**AI is not offline.** The report, a file/heading index, and selected full Markdown files are sent to your chosen provider. That provider's retention and training policies apply. Remove secrets and personal information before generating a preview.

API keys pass through the local server to the selected provider. They are not intentionally written to project files or browser `localStorage`. The session token uses `sessionStorage`; do not share the session URL.

Local `.state/` backups contain skill content and paths. Treat them as sensitive, and do not commit backups, credentials, private reports, or skill copies. Keep an independent backup or use version control for important skills.

Apply checks for edits since preview, and restore checks for newer edits. Path checks restrict writes to the selected skill and reject unsafe targets, including symbolic links and nested skills unless selected directly. These checks are not a security audit or a defense against hostile local processes. Do not use attacker-writable directories or expose the app directly to the internet.

**Human review is required.** Models can repeat existing rules, invent details, or propose contradictory guidance. Check meaning, evidence, language, scope, and navigation links before applying. A valid plan is not proof of a good instruction.

## Development and support

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The default tests use synthetic fixtures and simulated provider responses; they make no paid AI requests. See [testing and compatibility](docs/verification.md) for coverage and reproducible dependency versions.

For contributions and useful bug reports, see [CONTRIBUTING.md](CONTRIBUTING.md). For vulnerability reporting guidance, see [SECURITY.md](SECURITY.md). Include sanitized reproduction steps, not API keys or private skill content.

## License

Project source and original examples are under the [MIT License](LICENSE). Dependencies retain their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Model accuracy, security outcomes, stars, downloads, and adoption are not guaranteed.
