
from pathlib import Path
import sys

import pandas as pd


DATA_DIRS = {
    "raw": Path("data/raw"),
    "staging": Path("data/staging"),
}


def validate_dataset(file_path):
    df = pd.read_csv(file_path)

    print("\n" + "=" * 65)
    print(f"Dataset: {file_path.stem}")
    print("=" * 65)

    rows = len(df)
    missing_values = int(df["value"].isna().sum())
    duplicate_timestamps = int(df["timestamp_ms"].duplicated().sum())

    timestamps = pd.to_datetime(
        df["timestamp_utc"], utc=True, errors="coerce"
    )

    invalid_timestamps = int(timestamps.isna().sum())
    valid_timestamps = timestamps.dropna().sort_values()
    intervals = valid_timestamps.diff().dropna().dt.total_seconds() / 60

    print(f"Rows: {rows}")
    print(f"Missing values: {missing_values}")
    print(f"Duplicate timestamps: {duplicate_timestamps}")
    print(f"Invalid timestamps: {invalid_timestamps}")

    if not df.empty and not valid_timestamps.empty:
        print(f"Start: {valid_timestamps.min()}")
        print(f"End:   {valid_timestamps.max()}")

    numeric_values = pd.to_numeric(df["value"], errors="coerce")
    print(f"Negative values: {(numeric_values < 0).sum()}")

    if not intervals.empty:
        print(f"Most common interval (minutes): {intervals.mode().iloc[0]}")
        print(f"Unexpected intervals: {(intervals != intervals.mode().iloc[0]).sum()}")

    passed = (
        rows > 0
        and missing_values == 0
        and duplicate_timestamps == 0
        and invalid_timestamps == 0
    )
    print(f"Basic validation: {'PASS' if passed else 'CHECK'}")


def main():
    layer = sys.argv[1].lower() if len(sys.argv) > 1 else "staging"

    if layer not in DATA_DIRS:
        raise SystemExit("Usage: python validate_smard_data.py [raw|staging]")

    data_dir = DATA_DIRS[layer]

    if not data_dir.exists():
        raise SystemExit(f"Data directory not found: {data_dir}")

    files = sorted(data_dir.glob("*.csv"))
    if not files:
        raise SystemExit(f"No CSV files found in {data_dir}")

    print(f"SMARD DATA QUALITY REPORT — {layer.upper()}")

    for file_path in files:
        validate_dataset(file_path)


if __name__ == "__main__":
    main()
