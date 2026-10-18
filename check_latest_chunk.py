
import requests
from datetime import datetime, timezone

BASE = "https://www.smard.de/app/chart_data"

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
    print(f"\n{'=' * 55}")
    print(name)

    index_url = f"{BASE}/{filter_id}/DE/index_hour.json"
    response = session.get(index_url, timeout=30)
    response.raise_for_status()

    timestamps = sorted(
        response.json().get("timestamps", []),
        reverse=True
    )

    for chunk_timestamp in timestamps[:2]:
        chunk_date = datetime.fromtimestamp(
            chunk_timestamp / 1000,
            tz=timezone.utc,
        )

        data_url = (
            f"{BASE}/{filter_id}/DE/"
            f"{filter_id}_DE_hour_{chunk_timestamp}.json"
        )

        result = session.get(data_url, timeout=30)
        print(f"\nChunk start: {chunk_date.isoformat()}")
        print("HTTP status:", result.status_code)

        if result.status_code != 200:
            print(result.text[:200])
            continue

        series = result.json().get("series", [])
        null_count = sum(
            value is None for _, value in series
        )

        valid_count = sum(
            value is not None for _, value in series
        )

        print("Observations:", len(series))
        print("Valid values:", valid_count)
        print("Null values:", null_count)
        print("Last 25 observations:")
        print(series[-25:])
