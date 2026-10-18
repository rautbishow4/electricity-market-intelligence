import requests

BASE_URL = "https://www.smard.de/app/chart_data"

DATASETS = {
    "day_ahead_price": (4169, "DE-LU"),
    "electricity_load": (410, "DE"),
    "wind_onshore": (4067, "DE"),
    "wind_offshore": (1225, "DE"),
    "solar_generation": (4068, "DE"),
}

session = requests.Session()
session.headers.update({"User-Agent": "ElectricityIntelligenceProject/1.0"})

for name, (filter_id, region) in DATASETS.items():
    url = f"{BASE_URL}/{filter_id}/{region}/index_hour.json"

    try:
        response = session.get(url, timeout=20)
        print(f"\n{name}: HTTP {response.status_code}")
        response.raise_for_status()

        payload = response.json()
        timestamps = payload.get("timestamps", [])

        print(f"Available timestamp chunks: {len(timestamps)}")
        if timestamps:
            print(f"Latest chunk timestamp: {timestamps[-1]}")
        else:
            print("No timestamps returned.")

    except (requests.RequestException, ValueError) as error:
        print(f"Request failed: {error}")