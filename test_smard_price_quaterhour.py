
import requests
from datetime import datetime, timezone

BASE = "https://www.smard.de/app"
session = requests.Session()
session.headers.update({
    "User-Agent": "ElectricityIntelligenceProject/1.0"
})

# Retrieve the quarter-hour timestamp index
index_url = f"{BASE}/chart_data/4169/DE/index_quarterhour.json"
response = session.get(index_url, timeout=20)
response.raise_for_status()

timestamps = sorted(
    response.json().get("timestamps", []),
    reverse=True
)

print("Available quarter-hour chunks:", len(timestamps))

# Test only the 5 newest chunks first
for timestamp in timestamps[:5]:
    readable = datetime.fromtimestamp(
        timestamp / 1000, tz=timezone.utc
    ).isoformat()

    url = (
        f"{BASE}/table_data/4169/DE/"
        f"4169_DE_quarterhour_{timestamp}.json"
    )

    try:
        result = session.get(url, timeout=20)
        print(f"\nChunk: {readable} | HTTP {result.status_code}")

        if result.status_code != 200:
            continue

        payload = result.json()
        series = payload.get("series", [])

        observations = []
        for item in series:
            # Table responses may wrap observations in "values"
            observations.extend(item.get("values", []))

        print("Observations:", len(observations))
        print("Sample:", observations[:3])

    except (requests.RequestException, ValueError) as error:
        print("Request error:", error)
