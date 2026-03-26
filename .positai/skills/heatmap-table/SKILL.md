---
name: heatmap-table
description: Applies heatmap colour formatting to a data table using the gt R package, with a white-yellow-red colour scale where higher values appear red and medium values yellow. Use when the user wants a heatmap table, colour-coded table, or wants to highlight high/low values in a table.
compatibility: Requires R with the gt and tidyverse packages installed.
---

# Heatmap table formatting with `gt`

Use the `gt` package to apply a white → yellow → red heatmap colour scale to a wide-format numeric table.

## Basic pattern

```r
library(gt)

# Assume `wide_df` has a label column (e.g. "category") and numeric columns
value_cols <- names(wide_df)[-1]  # all columns except the label column

wide_df |>
  gt() |>
  fmt_currency(columns = all_of(value_cols), currency = "USD", decimals = 0) |>
  data_color(
    columns = all_of(value_cols),
    rows = everything(),
    method = "numeric",
    palette = c("white", "yellow", "red"),
    domain = c(0, max(select(wide_df, all_of(value_cols))))
  ) |>
  cols_label(category = "Category") |>
  tab_header(title = "Table title") |>
  opt_stylize(style = 1)
```

## Key options

- **`palette`**: Change colour scale as needed, e.g. `c("white", "yellow", "red")` for expenses, `c("white", "lightblue", "darkblue")` for neutral data.
- **`domain`**: Sets the min/max for colour mapping. Use `c(0, max(...))` for values starting at zero, or `c(min(...), max(...))` for data with negatives.
- **`fmt_currency()`**: Replace with `fmt_number()` for non-currency numeric data.
- **`decimals`**: Set to `2` for decimal precision, `0` for whole numbers.
- **`opt_stylize(style = 1)`**: Optional styling. Styles range from 1–6.

## Notes

- The input table must be in **wide format** (one row per category, one column per group/period).
- Use `pivot_wider()` to reshape long data before applying heatmap formatting.
- If only certain columns should be coloured (e.g. exclude a totals column), adjust `value_cols` accordingly.
- For non-currency data, replace `fmt_currency()` with `fmt_number()`.
