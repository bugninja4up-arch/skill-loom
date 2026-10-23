# Try a report-to-skill update

The included skill and report are original synthetic material licensed with this project. They contain no private data and do not require downloading someone else's skill archive.

## Run it

From the project folder, install dependencies as described in the README and start:

```sh
python start.py --root ./examples
```

Open the full session URL, scan `./examples`, and select **Demo report reviewer**. Upload `examples/sample-report.md`. Configure your own API endpoint, model, and key, then generate a preview. This sends the report and selected skill context to that provider and may incur provider charges.

## Review the proposal

A useful result would make evidence-to-action traceability and explicit uncertainty more actionable. Privacy guidance already exists in the example skill, so the model should avoid repeating it unnecessarily. These are evaluation goals, not a canned response or a promise about any model.

Check that the proposal:

- Adds concise instructions in an appropriate existing section, without rewriting the original skill.
- Ties recommended actions to specific observations and asks for missing evidence.
- Does not invent a filename, a metric, a real person, or a successful outcome.
- Preserves the original headings, YAML, language, and scope.
- Avoids duplicate or contradictory instructions.

Use **Before**, **After**, and **Diff** to inspect the full proposed file. Reject a poor proposal rather than applying it just because validation passed. An empty proposal can also be valid when no useful addition is needed.

## Apply and undo

For a proposal you accept, click **Apply changes**. Open History and choose **Restore**, then confirm. Verify the example file is back to its original content. Restore refuses to overwrite newer edits; inspect and preserve those edits first.

The app changes the example copy inside your extracted project only after Apply. Keep a separate copy if you want a disposable trial. No screenshot or fixed model output is included as a claim of model quality.
