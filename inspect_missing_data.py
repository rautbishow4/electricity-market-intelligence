
from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")

DATASETS = [
    "electricity_load",
    "wind_onshore",
    "wind_offshore",
    "solar_generation",
]

series = {}

for name in DATASETS:
    path = DATA_DIR / f"{name}.csv"
    df = pd.read_csv(path)

    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"], utc=True
    )

    df = df.set_index("timestamp_utc").sort_index()
    series[name] = df["value"].rename(name)

combined = pd.concat(series.values(), axis=1)

print("=" * 70)
print("MISSING DATA INVESTIGATION")
print("=" * 70)

for name in DATASETS:
    missing = combined.index[combined[name].isna()]

    print(f"\n{name}: {len(missing)} missing values")

    if len(missing):
        print("First 10 missing timestamps:")
        print(missing[:10].to_list())

        print("\nMissing timestamp ranges:")
        groups = missing.to_series().diff().ne(
            pd.Timedelta(hours=1)
        ).cumsum()

        for _, group in missing.to_series().groupby(groups):
            start = group.iloc[0]
            end = group.iloc[-1]
            print(f"  {start} -> {end}")

print("\n" + "=" * 70)
print("MISSING VALUES BY COMBINATION")
print("=" * 70)

missing_mask = combined[DATASETS].isna()

print("\nMissing count at each timestamp:")
print(missing_mask.sum(axis=1).value_counts().sort_index())

print("\nTimestamps missing in ALL four datasets:")
all_missing = combined.index[missing_mask.all(axis=1)]
print("Count:", len(all_missing))
print(all_missing.to_list())

print("\nTimestamps missing in ANY dataset:")
any_missing = combined.index[missing_mask.any(axis=1)]
print("Count:", len(any_missing))
print(any_missing.to_list())
