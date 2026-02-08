from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import streamlit as st


@st.cache_data
def load_data(path: str = "expenses.csv") -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Keep only months that have data through at least the 25th
    df["month"] = df["date"].dt.to_period("M")
    coverage_months = (
        df.groupby("month")["date"].max().dt.day >= 25
    ).loc[lambda s: s].index
    df = df[df["month"].isin(coverage_months)].copy()

    # Keep only expenses, filter out internal transfers/payments
    df = df[df["type"].str.upper() == "DEBIT"].copy()
    df = df[
        df["category"].astype(str).str.strip().str.lower() != "transfer/pmt"
    ].copy()

    # Spend should be positive
    df["spend"] = -df["amount"]

    # Derive month start
    df["month_start"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Normalize category
    df["category"] = df["category"].fillna("(uncategorized)").str.strip().str.lower()

    return df


def currency_axes(ax: plt.Axes, axis: str = "y") -> None:
    formatter = StrMethodFormatter("${x:,.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def main() -> None:
    st.set_page_config(page_title="Expenses Explorer", layout="wide")
    st.title("Expenses Explorer")

    df = load_data()
    if df.empty:
        st.warning("No data available after filters.")
        return

    with st.sidebar:
        st.header("Filters")
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.date_input(
            "Date range", (min_date, max_date), min_value=min_date, max_value=max_date
        )
        categories = sorted(df["category"].unique().tolist())
        selected_categories = st.multiselect(
            "Categories", categories, default=categories
        )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        mask = (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)
        df = df[mask].copy()

    if selected_categories:
        df = df[df["category"].isin(selected_categories)].copy()

    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    # Summary
    total_spend = df["spend"].sum()
    monthly_spend = df.groupby("month_start", as_index=False)["spend"].sum()
    avg_monthly_spend = monthly_spend["spend"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", f"${total_spend:,.0f}")
    col2.metric("Avg Monthly Spend", f"${avg_monthly_spend:,.0f}")
    col3.metric("Transactions", f"{len(df):,}")

    st.subheader("Monthly Spend")
    fig, ax = plt.subplots()
    ax.plot(monthly_spend["month_start"], monthly_spend["spend"], marker="o")
    ax.set_title("Monthly Spend")
    ax.tick_params(axis="x", rotation=45)
    currency_axes(ax, axis="y")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig, clear_figure=True)

    st.subheader("Top Categories")
    category_total = (
        df.groupby("category", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
    )
    fig, ax = plt.subplots()
    ax.barh(category_total.head(10)["category"], category_total.head(10)["spend"])
    ax.invert_yaxis()
    ax.set_title("Top 10 Categories by Spend")
    currency_axes(ax, axis="x")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig, clear_figure=True)

    st.subheader("Monthly Spend by Top Categories")
    category_month = (
        df.groupby(["month_start", "category"], as_index=False)["spend"].sum()
    )
    pivot = (
        category_month.pivot(index="month_start", columns="category", values="spend")
        .fillna(0)
    )
    top_cats = category_total.head(6)["category"].tolist()
    pivot_top = pivot[top_cats].copy()
    pivot_top.index = pivot_top.index.to_period("M").astype(str)

    fig, ax = plt.subplots()
    pivot_top.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Monthly Spend by Top Categories")
    ax.tick_params(axis="x", rotation=45)
    currency_axes(ax, axis="y")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig, clear_figure=True)

    st.subheader("Tables")
    st.markdown("**Summary**")
    summary = pd.DataFrame(
        {
            "total_spend": [total_spend],
            "avg_monthly_spend": [avg_monthly_spend],
            "transaction_count": [len(df)],
        }
    )
    st.dataframe(
        summary.style.format({
            "total_spend": "${:,.0f}",
            "avg_monthly_spend": "${:,.0f}",
            "transaction_count": "{:,.0f}",
        })
    )

    st.markdown("**Monthly**")
    monthly = monthly_spend.copy()
    monthly["mom_change"] = monthly["spend"].diff()
    st.dataframe(
        monthly.style.format({
            "spend": "${:,.0f}",
            "mom_change": "${:,.0f}",
        })
    )

    st.markdown("**Top Categories**")
    st.dataframe(category_total.head(10).style.format({"spend": "${:,.0f}"}))


if __name__ == "__main__":
    main()
