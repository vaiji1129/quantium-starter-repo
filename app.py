# app.py
import pandas as pd
import glob
import os
from pandas.errors import EmptyDataError

DATA_DIR = "data"
OUTPUT_FILENAME = "formatted_sales.csv"
OUTPUT_PATH = os.path.join(DATA_DIR, OUTPUT_FILENAME)

def safe_read_csv(path):
    """Read CSV, skipping empty files or raising a controlled error."""
    # skip truly empty files
    if os.path.getsize(path) == 0:
        print(f"  - Skipping empty file: {os.path.basename(path)}")
        return None
    try:
        # engine="python" is a bit more tolerant for oddly formatted CSVs
        df = pd.read_csv(path, engine="python")
        return df
    except EmptyDataError:
        print(f"  - Skipping file with no data: {os.path.basename(path)}")
        return None
    except Exception as e:
        print(f"  - Failed to read {os.path.basename(path)}: {e}")
        return None

def normalize_columns(df):
    """Lowercase and strip column names for robust access."""
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df

def process_file(path):
    print(f"Processing: {os.path.basename(path)}")
    df = safe_read_csv(path)
    if df is None:
        return None

    df = normalize_columns(df)

    # required columns (we'll accept variants by lowercasing)
    required = {"product", "quantity", "price", "date", "region"}
    if not required.issubset(set(df.columns)):
        # If some columns are missing, show which and skip
        missing = required - set(df.columns)
        print(f"  - Missing columns {sorted(missing)} — skipping file.")
        return None

    # filter Pink Morsel (exact match). If your files use slightly different names, tweak here.
    df = df[df["product"] == "Pink Morsel"]
    if df.empty:
        print("  - No Pink Morsel rows found in this file — skipping.")
        return None

    # Convert quantity and price to numeric safely
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Drop rows where quantity or price are missing after coercion
    n_before = len(df)
    df = df.dropna(subset=["quantity", "price"])
    n_after = len(df)
    if n_after < n_before:
        print(f"  - Dropped {n_before - n_after} rows with non-numeric price/quantity.")

    # Calculate sales
    df["sales"] = df["quantity"] * df["price"]

    # Keep only the required output columns and rename to match spec (Sales, Date, Region)
    out = df[["sales", "date", "region"]].copy()
    # If you want capitalised headers in the CSV:
    out.columns = ["Sales", "Date", "Region"]

    return out

def main():
    csv_paths = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    if not csv_paths:
        print(f"No CSV files found in {DATA_DIR}/")
        return

    processed_frames = []
    for p in csv_paths:
        # Skip the output file if it already exists in data folder
        if os.path.basename(p) == OUTPUT_FILENAME:
            print(f"Skipping output file if present: {OUTPUT_FILENAME}")
            continue
        result = process_file(p)
        if result is not None and not result.empty:
            processed_frames.append(result)

    if not processed_frames:
        # still produce an empty CSV with headers to satisfy downstream checks
        empty_df = pd.DataFrame(columns=["Sales", "Date", "Region"])
        empty_df.to_csv(OUTPUT_PATH, index=False)
        print(f"No Pink Morsel data found in any files. Created empty {OUTPUT_PATH} with headers.")
        return

    combined = pd.concat(processed_frames, ignore_index=True)

    # Optional: re-order columns to exactly Sales, Date, Region (already set)
    combined = combined[["Sales", "Date", "Region"]]

    # Save
    combined.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Created {OUTPUT_PATH} with {len(combined)} rows.")

if __name__ == "__main__":
    main()
