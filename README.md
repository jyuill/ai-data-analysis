# PURPOSE

Playground for experimenting with different approaches for leveraging AI to explore and analyze data, for the purposes of efficiency and streamlining the process, especially tedious elements.

## Experiment #1: Codex App / Chat for Expenses

- Started by providing prompts directly into desktop Codex app to analyze expenses.csv file provided (subset of data from my personal expense tracking).
- Updates / refinements using the chat window in VS Code.
- RESULT: expenses_analysis.ipynb

### Export

For a clean, report-style HTML export that hides code cells:

```bash
uv run jupyter nbconvert --to html --no-input expenses_analysis.ipynb
```

### Streamlit App

Streamlit app developed by Codex via chat window in VS Code.

Run the interactive explorer:

```bash
uv run streamlit run app.py
```

- smooth process that required iteration but good responses each time and saved many hrs of hand-coding.
- CRUCIALLY: Codex able to add commentary at the bottom, highlighting basic observations and simple calculations (date range, top category, median mthly) but also more complex calculations like which category had biggest range in monthly spending and even which had biggest percentage change in monthly spending. Impressive.

#### UPGRADES

- used **Claude Code** (in terminal/cli) to switch from expenses.csv to the googlesheets source, in order to keep it up to date and more data added there.
- very slick

### Overall Verdict

- worked ok.
- some operations took multiple requests and attempts.
- Streamlit development went exceptionally well.
- additional work from Claude Code was impressive, smooth experience (although, in fairness, used Codex via chat window and not terminal, so not apples-to-apples comp).
- **terminal/cli** seems to be the more efficient way to go, rather than chat window.
