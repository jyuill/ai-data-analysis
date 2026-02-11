from __future__ import annotations

import json
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SPREADSHEET_ID = "1dZhNtCPDG2tAzMkd5FpVh1GqtDXeJFEHhVYd2wY12n0"
SHEET_NAME = "spending-r"
SHEET_RANGE = "A10:O"  # Open-ended range to accommodate growing data
CREDENTIALS_FILE = "credentials/original-return-107905-3b03bf4c17bf.json"


@st.cache_data
def load_data(use_google_sheets: bool = True) -> pd.DataFrame:
    if use_google_sheets:
        # Authenticate with Google Sheets
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
        ]

        # Check for credentials in environment variable (for Railway/cloud deployment)
        credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if credentials_json:
            # Parse JSON from environment variable
            credentials_info = json.loads(credentials_json)
            creds = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        else:
            # Fall back to file-based credentials (for local development)
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)

        client = gspread.authorize(creds)

        # Open the spreadsheet and get the data
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
        data = sheet.get(SHEET_RANGE)

        # Convert to DataFrame (first row is headers)
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        # Fallback to CSV
        df = pd.read_csv("expenses.csv", encoding="utf-8-sig")

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
    excluded_categories = {"transfer/pmt", "investment", "rental inc"}
    df = df[
        ~df["category"].astype(str).str.strip().str.lower().isin(excluded_categories)
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
    st.markdown(
        """
        <style>
        div[data-testid="stDataFrame"] table {
            font-size: 1.25rem;
        }
        div[data-testid="stDataFrame"] {
            font-size: 1.25rem;
        }
        /* Make multiselect dropdown taller */
        div[data-baseweb="select"] > div {
            max-height: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Monthly Spend")
        fig, ax = plt.subplots(figsize=(5.5, 3))
        ax.plot(monthly_spend["month_start"], monthly_spend["spend"], marker="o")
        ax.set_title("Monthly Spend")
        ax.tick_params(axis="x", rotation=45)
        currency_axes(ax, axis="y")
        ax.set_xlabel("")
        ax.set_ylabel("")
        st.pyplot(fig, clear_figure=True, use_container_width=True)

    with col_right:
        st.subheader("Top Categories")
        category_total = (
            df.groupby("category", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
        )
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        ax.barh(category_total.head(12)["category"], category_total.head(12)["spend"])
        ax.invert_yaxis()
        ax.set_title("Top 12 Categories by Spend")
        currency_axes(ax, axis="x")
        ax.set_xlabel("")
        ax.set_ylabel("")
        st.pyplot(fig, clear_figure=True, use_container_width=True)

    st.subheader("Monthly Spend by Top Categories")
    category_total = (
        df.groupby("category", as_index=False)["spend"].sum().sort_values("spend", ascending=False)
    )
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

    fig, ax = plt.subplots(figsize=(10, 3.6))
    pivot_top.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Monthly Spend by Top Categories")
    ax.tick_params(axis="x", rotation=45)
    currency_axes(ax, axis="y")
    ax.set_xlabel("")
    ax.set_ylabel("")
    legend = ax.get_legend()
    if legend:
        legend.set_title("")
        legend.set_bbox_to_anchor((0, 1))
        legend._loc = 2
        for text in legend.get_texts():
            text.set_fontsize(7)
    st.pyplot(fig, clear_figure=True, use_container_width=True)

    # Additional charts
    dist_col, range_col = st.columns(2)

    with dist_col:
        st.subheader("Monthly Spend Distribution")
        spend_vals = monthly_spend["spend"].dropna()
        if not spend_vals.empty:
            bin_size = 2000
            min_val = (spend_vals.min() // bin_size) * bin_size
            max_val = ((spend_vals.max() // bin_size) + 1) * bin_size
            bins = np.arange(min_val, max_val + bin_size, bin_size)
        else:
            bins = 12
        fig, ax = plt.subplots(figsize=(5.5, 3))
        ax.hist(spend_vals, bins=bins, color="#4C78A8", edgecolor="white")
        ax.set_title("Distribution of Monthly Spend")
        if isinstance(bins, np.ndarray) and bins.size > 1:
            ax.set_xticks(np.arange(bins[0], bins[-1] + 1, 4000))
        currency_axes(ax, axis="x")
        ax.set_xlabel("Monthly Spend")
        ax.set_ylabel("Months")
        st.pyplot(fig, clear_figure=True, use_container_width=True)

    with range_col:
        st.subheader("Monthly Spend Range by Category")
        top_cats_box = category_total.head(10)["category"].tolist()
        box_data = [
            pivot.get(cat).dropna().values if cat in pivot.columns else []
            for cat in top_cats_box
        ]
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        ax.boxplot(box_data, labels=top_cats_box, vert=False, patch_artist=True)
        ax.set_title("Monthly Spend Range by Top Categories")
        currency_axes(ax, axis="x")
        ax.set_xlabel("")
        ax.set_ylabel("")
        st.pyplot(fig, clear_figure=True, use_container_width=True)

    st.subheader("Tables")
    monthly = monthly_spend.copy()
    monthly["month_start"] = monthly["month_start"].dt.date
    monthly["mom_change"] = monthly["spend"].diff()
    monthly["mom_change_pct"] = monthly["spend"].pct_change() * 100

    tbl_left, tbl_right = st.columns(2)
    with tbl_left:
        st.markdown("**Monthly**")
        st.dataframe(
            monthly.style.format({
                "spend": "${:,.0f}",
                "mom_change": "${:,.0f}",
                "mom_change_pct": "{:,.0f}%",
            })
        )

    with tbl_right:
        st.markdown("**Top Categories**")
        st.dataframe(category_total.head(10).style.format({"spend": "${:,.0f}"}))

    # Correlation heatmap
    st.subheader("Category Correlations")
    heat_left, heat_mid, heat_right = st.columns([1, 2, 1])
    monthly_cat_corr = (
        df.groupby(["month_start", "category"], as_index=False)["spend"].sum()
    )
    pivot_corr = (
        monthly_cat_corr.pivot(index="month_start", columns="category", values="spend")
        .sort_index()
    )
    min_months = 4
    eligible = pivot_corr.count() >= min_months
    corr_data = pivot_corr.loc[:, eligible]
    corr_summary: list[str] = []
    if corr_data.shape[1] >= 2:
        corr = corr_data.corr()
        corr_plot = corr.fillna(0).copy()
        diag_mask = np.eye(corr_plot.shape[0], dtype=bool)
        corr_plot.values[diag_mask] = np.nan
        cmap = sns.color_palette("vlag", as_cmap=True)
        cmap.set_bad("black")
        fig, ax = plt.subplots(figsize=(6.2, 3.6))
        sns.heatmap(
            corr_plot,
            ax=ax,
            cmap=cmap,
            vmin=-1,
            vmax=1,
            center=0,
            square=True,
            linewidths=0.5,
            linecolor="#f0f0f0",
            mask=diag_mask,
            cbar_kws={"label": "Correlation", "shrink": 0.75},
        )
        ax.set_title("Monthly Spend Correlation by Category")
        ax.tick_params(axis="x", labelrotation=45, labelsize=7)
        ax.set_xticklabels(ax.get_xticklabels(), ha="right", rotation_mode="anchor")
        ax.tick_params(axis="y", labelsize=7)
        ax.set_xlabel("Category", fontsize=8)
        ax.set_ylabel("Category", fontsize=8)
        fig.tight_layout()
        st.caption(
            f"Based on {corr_data.shape[0]} months. "
            f"Showing categories with at least {min_months} months of data."
        )
        with heat_mid:
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(labelsize=7)
            cbar.set_label("Correlation", fontsize=8)
            st.pyplot(fig, clear_figure=True, use_container_width=False)

        corr_pairs = corr.where(~np.eye(corr.shape[0], dtype=bool))
        corr_stack = corr_pairs.stack().sort_values()
        if not corr_stack.empty:
            strongest_neg = corr_stack.iloc[0]
            strongest_pos = corr_stack.iloc[-1]
            neg_pair = corr_stack.index[0]
            pos_pair = corr_stack.index[-1]
            corr_summary.append(
                f"Strongest negative correlation: "
                f"{neg_pair[0]} vs {neg_pair[1]} "
                f"({strongest_neg:,.2f})."
            )
            corr_summary.append(
                f"Strongest positive correlation: "
                f"{pos_pair[0]} vs {pos_pair[1]} "
                f"({strongest_pos:,.2f})."
            )
    else:
        st.info(
            "Not enough category history to compute correlations. "
            "Try a wider date range or more categories."
        )

    # Insights
    insights: list[str] = []
    date_label = f"{start_date} to {end_date}"
    insights.append(f"Date range: {date_label} across {len(monthly_spend)} months.")

    if not monthly_spend.empty:
        median_monthly = monthly_spend["spend"].median()
        insights.append(f"Median monthly spend: ${median_monthly:,.0f}.")

    if not category_total.empty and total_spend > 0:
        top_cat = category_total.iloc[0]
        top_share = (top_cat["spend"] / total_spend) * 100
        insights.append(
            f"Top category is '{top_cat['category']}' at ${top_cat['spend']:,.0f} "
            f"({top_share:,.0f}% of spend)."
        )

    monthly_cat = (
        df.groupby(["month_start", "category"], as_index=False)["spend"].sum()
    )
    pivot_cat = (
        monthly_cat.pivot(index="month_start", columns="category", values="spend")
        .sort_index()
    )
    valid_cats = pivot_cat.count() >= 2
    if valid_cats.any():
        range_by_cat = (pivot_cat.max() - pivot_cat.min()).loc[valid_cats]
        stable_cat = range_by_cat.idxmin()
        stable_range = range_by_cat.min()
        insights.append(
            f"Most stable category: '{stable_cat}' with a ${stable_range:,.0f} "
            "monthly range."
        )

        var_cat_range = range_by_cat.idxmax()
        var_range = range_by_cat.max()
        pct_change = (
            pivot_cat.pct_change()
            .replace([np.inf, -np.inf], np.nan)
            .abs()
        )
        max_pct_by_cat = pct_change.max().loc[valid_cats]
        var_cat_pct = max_pct_by_cat.idxmax()
        var_pct = max_pct_by_cat.max() * 100
        insights.append(
            f"Most variable category: '{var_cat_range}' with a ${var_range:,.0f} range; "
            f"largest MoM % change in '{var_cat_pct}' at {var_pct:,.0f}%."
        )

    # Keep 3-5 succinct bullets
    if corr_summary:
        corr_summary = corr_summary[:2]
        remaining = max(0, 7 - len(corr_summary))
        insights = insights[:remaining] + corr_summary
    else:
        insights = insights[:7]
    st.subheader("Insights")
    st.markdown("\n".join([f"- {point}" for point in insights]))


if __name__ == "__main__":
    main()
