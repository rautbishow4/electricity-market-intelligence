
from pathlib import Path

import pandas as pd
import requests

BASE = "https://www.smard.de/app/chart_data"
DATA_DIR = Path("data/raw")

DATASETS = {
    "electricity_load": 410,
    "wind_onshore": 4067,
    "wind_offshore": 1225,
    "solar_generation": 4068,
}

session = requests.Session()
session.headers.update({
    "User-Agent": "ElectricityIntelligenceProject/1.0"
})

for name, filter_id in DATASETS.items():
    print(f"\n{'=' * 60}\n{name}")

    csv_path = DATA_DIR / f"{name}.csv"
    df = pd.read_csv(csv_path)
    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_utc"], utc=True
    )

    missing = df[df["value"].isna()]

    print("Missing in CSV:", len(missing))

    index_url = f"{BASE}/{filter_id}/DE/index_hour.json"
    index_response = session.get(index_url, timeout=30)
    index_response.raise_for_status()

    latest_timestamp = max(
        index_response.json()["timestamps"]
    )

    data_url = (
        f"{BASE}/{filter_id}/DE/"
        f"{filter_id}_DE_hour_{latest_timestamp}.json"
    )
    response = session.get(data_url, timeout=30)
    response.raise_for_status()

    api_series = response.json().get("series", [])
    api_values = {
        int(timestamp): value
        for timestamp, value in api_series
    }

    if missing.empty:
        print("No missing CSV values to compare.")
        continue

    for _, row in missing.iterrows():
        timestamp_ms = int(row["timestamp_utc"].timestamp() * 1000)
        api_value = api_values.get(timestamp_ms, "TIMESTAMP NOT IN LATEST CHUNK")
        print(f"{row['timestamp_utc']} | API value: {api_value}")
