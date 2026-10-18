
import requests
from datetime import datetime, timezone

BASE = "https://www.smard.de/app"
FILTER = 4169
REGION = "DE"

session = requests.Session()
session.headers.update({
    "User-Agent": "ElectricityIntelligenceProject/1.0"
})

index_url = (
    f"{BASE}/chart_data/{FILTER}/{REGION}/"
    "index_quarterhour.json"
)

response = session.get(index_url, timeout=20)
print("Index HTTP status:", response.status_code)
response.raise_for_status()

timestamps = sorted(
    response.json().get("timestamps", []),
    reverse=True
)

print("Available chunks:", len(timestamps))

for timestamp in timestamps[:3]:
    readable = datetime.fromtimestamp(
        timestamp / 1000,
        tz=timezone.utc
    ).isoformat()

    data_url = (
        f"{BASE}/chart_data/{FILTER}/{REGION}/"
        f"{FILTER}_{REGION}_quarterhour_{timestamp}.json"
    )

    result = session.get(data_url, timeout=20)

    print(f"\nChunk: {readable}")
    print("HTTP status:", result.status_code)

    if result.status_code == 200:
        payload = result.json()
        series = payload.get("series", [])

        print("Observations:", len(series))
        print("Sample:", series[:5])
    else:
        print(result.text[:200])
