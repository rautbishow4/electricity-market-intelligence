
import requests

BASE = "https://www.smard.de/app"
session = requests.Session()
session.headers.update({
    "User-Agent": "ElectricityIntelligenceProject/1.0"
})

# Price index: use DE for the documented URL pattern
index_url = f"{BASE}/chart_data/4169/DE/index_hour.json"
response = session.get(index_url, timeout=20)
response.raise_for_status()

timestamps = response.json().get("timestamps", [])
print("Price index chunks:", len(timestamps))

found = False

for timestamp in sorted(timestamps, reverse=True):
    url = (
        f"{BASE}/table_data/4169/DE/"
        f"4169_DE_hour_{timestamp}.json"
    )

    result = session.get(url, timeout=20)
    print(timestamp, result.status_code)

    if result.status_code == 404:
        continue

    result.raise_for_status()
    payload = result.json()

    print("Response keys:", list(payload.keys()))
    print("Sample response:")
    print(str(payload)[:1500])

    found = True
    break

if not found:
    print("No accessible price chunk found in the available index.")
