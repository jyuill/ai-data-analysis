from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_expenses(path: str | Path | None = None) -> pd.DataFrame:
    if path is None:
        path = Path(__file__).resolve().parent / "data" / "expenses.csv"
    df = pd.read_csv(path, encoding="utf-8-sig")
    category = df["category"].astype(str).str.strip().str.lower()
    df = df[category != "transfer/pmt"].reset_index(drop=True)
    return df


def main() -> None:
    df = load_expenses()
    print(f"Loaded {len(df)} rows after filtering transfer/pmt.")


if __name__ == "__main__":
    main()
