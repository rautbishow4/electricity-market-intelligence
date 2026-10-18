
from pathlib import Path

import pandas as pd
import requests


BASE_URL = "https://www.smard.de/app/chart_data"
OUTPUT_DIR = Path("data/raw")
CHUNKS_TO_FETCH = 4

DATASETS = {
    "day_ahead_price": {
        "filter_id": 4169,
        "region": "DE",
        "resolution": "quarterhour",
    },
    "electricity_load": {
        "filter_id": 410,
        "region": "DE",
        "resolution": "hour",
    },
    "wind_onshore": {
        "filter_id": 4067,
        "region": "DE",
        "resolution": "hour",
    },
    "wind_offshore": {
        "filter_id": 1225,
        "region": "DE",
        "resolution": "hour",
    },
    "solar_generation": {
        "filter_id": 4068,
        "region": "DE",
        "resolution": "hour",
    },
}


def fetch_dataset(name, config, session):
    filter_id = config["filter_id"]
    region = config["region"]
    resolution = config["resolution"]

    index_url = (
        f"{BASE_URL}/{filter_id}/{region}/"
        f"index_{resolution}.json"
    )

    response = session.get(index_url, timeout=30)
    response.raise_for_status()

    timestamps = sorted(
        response.json().get("timestamps", []),
        reverse=True,
    )[:CHUNKS_TO_FETCH]

    if not timestamps:
        raise ValueError(f"No timestamps found for {name}")

    records = []

    for chunk_timestamp in timestamps:
        data_url = (
            f"{BASE_URL}/{filter_id}/{region}/"
            f"{filter_id}_{region}_{resolution}_"
            f"{chunk_timestamp}.json"
        )

        result = session.get(data_url, timeout=30)

        if result.status_code != 200:
            print(
                f"WARNING: {name} chunk "
                f"{chunk_timestamp} returned HTTP "
                f"{result.status_code}"
            )
            continue

        payload = result.json()

        # chart_data stores observations as [timestamp, value].
        for observation in payload.get("series", []):
            if (
                isinstance(observation, list)
                and len(observation) == 2
            ):
                timestamp, value = observation
                records.append({
                    "timestamp_ms": timestamp,
                    "value": value,
                })

    if not records:
        raise ValueError(f"No observations retrieved for {name}")

    df = pd.DataFrame(records)

    df = df.drop_duplicates(subset="timestamp_ms")
    df["timestamp_utc"] = pd.to_datetime(
        df["timestamp_ms"],
        unit="ms",
        utc=True,
    )
    df["timestamp_berlin"] = (
        df["timestamp_utc"].dt.tz_convert("Europe/Berlin")
    )

    df = df.sort_values("timestamp_utc").reset_index(drop=True)

    return df


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "ElectricityIntelligenceProject/1.0"
    })

    for name, config in DATASETS.items():
        print(f"\nDownloading: {name}")

        try:
            df = fetch_dataset(name, config, session)

            output_file = OUTPUT_DIR / f"{name}.csv"
            df.to_csv(output_file, index=False)

            print(f"Rows downloaded: {len(df)}")
            print(f"Saved to: {output_file}")
            print(df.head(3).to_string(index=False))

        except (requests.RequestException, ValueError, KeyError) as error:
            print(f"FAILED: {name}: {error}")


if __name__ == "__main__":
    main()
