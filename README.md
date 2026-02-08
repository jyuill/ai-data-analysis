# PURPOSE

Playground for experimenting with different approaches for leveraging AI to explore and analyze data, for the purposes of efficiency and streamlining the process, especially tedious elements.

## Experiment #1: Codex App / Chat

- Started by providing prompts directly into desktop Codex app to analyze expenses.csv (subset of data from my personal expense tracking).
- Updates / refinements using the chat window in VS Code.
- RESULT: expenses_analysis.ipynb

### Export

For a clean, report-style HTML export that hides code cells:

```bash
uv run jupyter nbconvert --to html --no-input expenses_analysis.ipynb
```

### Verdict

- worked ok
- some operations took multiple requests and attempts
