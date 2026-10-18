
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
STAGING_DIR = Path("data/staging")


def prepare_dataset(name):
    source_file = RAW_DIR / f"{name}.csv"
    output_file = STAGING_DIR / f"{name}.csv"

    df = pd.read_csv(source_file)

    rows_before = len(df)
    missing_before = int(df["value"].isna().sum())

    # Keep valid observations; do not replace missing values with zero.
    df = df.dropna(subset=["value"]).copy()

    # Parse timestamps and maintain chronological order.
    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"],
        utc=True,
    )

    df = (
        df.sort_values("timestamp_utc")
        .drop_duplicates(subset="timestamp_ms")
        .reset_index(drop=True)
    )

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\nDataset: {name}")
    print(f"Rows in raw data: {rows_before}")
    print(f"Missing values removed: {missing_before}")
    print(f"Rows in staging: {len(df)}")
    print(f"Saved to: {output_file}")


def main():
    for source_file in sorted(RAW_DIR.glob("*.csv")):
        prepare_dataset(source_file.stem)


if __name__ == "__main__":
    main()
