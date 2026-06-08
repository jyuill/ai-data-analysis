# AI Data Analysis Playground

Repo for experimenting with AI-assisted data analysis workflows in both Python and R.

## Repository Structure

- `experiments` folder for different experimental projects
- expenses app was first one, has dedicated folder.
- subsequent experiments/apps will be under `python` or `R` as applicable

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
- `experiments/R/`: reserved for new R experiments - includes template

## Experiment: Expenses

Builds on work done in R repo 'expenses' to collect and categorize monthly personal expenses.
- streamlit app for visual analysis + AI-generated observations

See `experiments/expenses/README.md` for more info.
Or Obsidian Vault > 10-Projects-details > AI for Data Analysis

