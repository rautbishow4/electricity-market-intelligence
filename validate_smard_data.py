
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")

DATASETS = {
    "day_ahead_price": 15,
    "electricity_load": 60,
    "wind_onshore": 60,
    "wind_offshore": 60,
    "solar_generation": 60,
}

dataframes = {}

print("=" * 65)
print("SMARD DATA QUALITY REPORT")
print("=" * 65)

for name, expected_minutes in DATASETS.items():
    path = DATA_DIR / f"{name}.csv"

    if not path.exists():
        print(f"\n{name}: FILE MISSING")
        continue

    df = pd.read_csv(path, parse_dates=["timestamp_utc"])
    df = df.sort_values("timestamp_utc")

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"], utc=True
    )

    timestamps = df["timestamp_utc"]
    intervals = timestamps.diff().dropna().dt.total_seconds() / 60

    print(f"\nDataset: {name}")
    print("-" * 40)
    print(f"Rows: {len(df)}")
    print(f"Start: {timestamps.min()}")
    print(f"End:   {timestamps.max()}")
    print(f"Duplicate timestamps: {timestamps.duplicated().sum()}")
    print(f"Missing values:\n{df[['timestamp_utc', 'value']].isna().sum()}")
    print(f"Negative values: {(df['value'] < 0).sum()}")

    if not intervals.empty:
        print(f"Most common interval (minutes): {intervals.mode().iloc[0]}")
        print(
            f"Unexpected intervals: "
            f"{(intervals != expected_minutes).sum()}"
        )

    dataframes[name] = df

print("\n" + "=" * 65)
print("TIMESTAMP COVERAGE")
print("=" * 65)

if dataframes:
    for name, df in dataframes.items():
        print(
            f"{name}: "
            f"{df['timestamp_utc'].min()} to "
            f"{df['timestamp_utc'].max()}"
        )
