# Contributing

Thanks for helping make report-to-skill updates more useful and reviewable.

Before opening a change, install `requirements-dev.txt` in a virtual environment and run `python -m pytest -q`. Use synthetic fixtures; do not add customer reports, copied skill archives, API keys, session links, backup records, or raw provider logs.

For a bug report, include the app version, Python version, operating system, minimal reproduction steps, expected behavior, actual behavior, and a sanitized error message. Make clear whether the provider was real or mocked. Never claim semantic accuracy from mock tests.

Prefer small changes with focused tests. Maintain additive-only edits, explicit user review before writes, path restrictions, stale-file protection, and reversible backups. If a change affects data sent to providers or local retention, update the README.

Submit only material you have the right to contribute under the project's MIT License; third-party dependencies keep their own licenses. Do not add promotional spam, purchased engagement, or fabricated results.

Use repository issues for ordinary bugs once the repository is published. See SECURITY.md for sensitive vulnerability reports.
