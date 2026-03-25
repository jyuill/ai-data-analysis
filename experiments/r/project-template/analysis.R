# Main script for this experiment
# Keep setup explicit so each project is reproducible.

options(stringsAsFactors = FALSE)

message("Starting analysis...")

# Example: load a CSV if present
raw_csv <- "data/raw/input.csv"
if (file.exists(raw_csv)) {
  df <- read.csv(raw_csv)
  message(sprintf("Loaded %d rows from %s", nrow(df), raw_csv))

  # Minimal processing placeholder
  out_csv <- "data/processed/preview.csv"
  dir.create(dirname(out_csv), recursive = TRUE, showWarnings = FALSE)
  write.csv(utils::head(df, 100), out_csv, row.names = FALSE)
  message(sprintf("Wrote preview to %s", out_csv))
} else {
  message("No data/raw/input.csv found. Add source data and rerun.")
}

message("Done.")
