## Expenses Experimentation

(notes also available in Obsidian Vault > 10-Projects-details > AI for Analysis)

Working with expense data generated via R in expenses repo.
Streamlit app available at subdomain: https://expenses.johnyuill.com/ 

## AI Tools

- started with OpenAI Codex desktop app
- follow-up with Claude Code

## Data Source

- orig: [Expenses google sheet](https://docs.google.com/spreadsheets/d/1dZhNtCPDG2tAzMkd5FpVh1GqtDXeJFEHhVYd2wY12n0/edit?usp=sharing)
    - csv stored in `expenses/data/expenses.csv` -> just for experimental purposes 
- CONNECT/IMPORT: 

## Run The Streamlit App

```bash
uv run streamlit run experiments/expenses/streamlit/app.py
```

Or BETTER run the local helper script:

```bash
./experiments/expenses/streamlit/run_local.sh
```

## Work With The Notebook

Open:

- `experiments/expenses/notebooks/expenses_analysis.ipynb`

Export to HTML (hide code cells):

```bash
uv run jupyter nbconvert --to html --no-input \
  experiments/expenses/notebooks/expenses_analysis.ipynb
```

## Railway Deployment

Entrypoint is configured in:

- `Procfile`
- `nixpacks.toml`

Both now run:

- `experiments/expenses/streamlit/app.py`

Settings:
- repo: jyuill/ai-data-analysis
- root directory: / (need top level for Profile, pyproject.toml, etc)
- Deploy section:
    - custom start command: uv run streamlit run experiments/expenses/streamlit/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

Set these Railway variables:

- `AUTH_USERNAME`
- `AUTH_NAME`
- `AUTH_PASSWORD_HASH`
- `GOOGLE_CREDENTIALS_JSON`
