# Project Memory

## Data Files

- **`experiments/expenses/data/expenses.csv`** — Personal expense tracker data

## Schema

| Column | Description |
|---|---|
| `date` | Transaction date |
| `amount` | Transaction amount (negative = expense) |
| `name` | Merchant/payee name |
| `memo` | Additional notes |
| `source` | Account source (e.g. `cap_one_visa`, `td_visa`, `beem_ch`) |
| `category` | Expense category |
| `month` | Month (format: `MM-YYYY`) |
| `year` | Year |
| `amount_inv` | Amount as formatted string (positive values) |

## Loading Instructions

When loading `expenses.csv`:

1. Drop these columns: `type`, `id`, `spend_type`, `vendor`
2. Filter out these categories: `income`, `rental inc`, `transfer/pmt`, `investment`

```r
expenses <- read.csv("experiments/expenses/data/expenses.csv")
expenses <- expenses[, !names(expenses) %in% c("type", "id", "spend_type", "vendor")]
expenses <- expenses |> dplyr::filter(!category %in% c("income", "rental inc", "transfer/pmt", "investment"))
```

## Notes

- `amount` is negative for expenses; multiply by -1 for display purposes
- `01-2026` data appears to be a partial month
- There is a large `int/bank chg/tax` spike in `05-2025` (~$6,577) that may warrant investigation
