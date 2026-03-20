# AI Data Analysis Playground

Repo for experimenting with AI-assisted data analysis workflows in both Python and R.

## Repository Structure

- `experiments/expenses/`
  - `data/expenses.csv`: local fallback expense data
  - `notebooks/expenses_analysis.ipynb`: notebook analysis
  - `notebooks/expenses_analysis.html`: exported notebook report
  - `streamlit/app.py`: Streamlit explorer app
  - `streamlit/run_local.sh`: local run script with test auth env vars
  - `streamlit/generate_password.py` and `streamlit/hash_password.py`: auth helpers
  - `streamlit/test_sheets_connection.py`: Google Sheets connectivity check
  - `docs/AUTH_SETUP.md`: authentication/deployment notes
- `experiments/python/`: reserved for new Python experiments

## Run The Streamlit App

```bash
uv run streamlit run experiments/expenses/streamlit/app.py
```

Or run the local helper script:

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

Set these Railway variables:

- `AUTH_USERNAME`
- `AUTH_NAME`
- `AUTH_PASSWORD_HASH`
- `GOOGLE_CREDENTIALS_JSON`
