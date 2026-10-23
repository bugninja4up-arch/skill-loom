# Skill Loom v1.0.0

First public release of Skill Loom, a local report-to-skill editor for Markdown agent skills.

## What's included

- English web interface for selecting a local skill and adding a Markdown or plain-text report.
- OpenAI-compatible AI API integration using your own endpoint, model, and key.
- Reviewable, additive-only Markdown changes with summary, warnings, and Diff / Before / After views.
- Local backups, stale-edit checks, and rollback that refuses to overwrite newer edits.
- Original example skill and report, installation instructions, contribution guidance, and tests.
- MIT project license and third-party dependency notices.

## Get started

Clone the `skill-loom` repository or download the source ZIP, create a Python virtual environment, install `requirements.txt`, and run `python start.py --root ./examples`. Full commands are in the [README](README.md).

## Requirements and limits

Python 3.10+ and an OpenAI-compatible Chat Completions provider are required; Linux with Python 3.12 is the tested configuration. Bring your own API key. Requests send report and skill context to that provider and may incur charges.

Use the app locally as a single user. Do not expose it directly to the internet. Markdown skills and text reports are supported; there is no bundled model, PDF/Word import, or automatic registry sync.

Review every proposal. Models can repeat instructions, invent details, or miss context. Keep an independent backup for important skills. This release does not promise model accuracy, public-hosting suitability, security certification, stars, or downloads.
