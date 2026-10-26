import os
import requests
import pandas as pd

URL = "https://api.open-meteo.com/v1/forecast"
PATH = "data/history.csv"
SITES = {
    "Nairobi": (-1.29, 36.82), "Murang'a": (-0.72, 37.15),
    "Kisumu": (-0.09, 34.77), "Mombasa": (-4.04, 39.67),
    "Eldoret": (0.51, 35.27), "Nakuru": (-0.30, 36.07),
    "Garissa": (-0.45, 39.65), "Kitale": (1.02, 35.00),
}

r = requests.get(URL, params={
    "latitude": ",".join(str(v[0]) for v in SITES.values()),
    "longitude": ",".join(str(v[1]) for v in SITES.values()),
    "current": "temperature_2m,relative_humidity_2m,precipitation",
    "timezone": "UTC",
}, timeout=30)
r.raise_for_status()

rows = []
for (name, (lat, lon)), d in zip(SITES.items(), r.json()):
    c = d["current"]
    rows.append({"time": c["time"], "site": name, "lat": lat, "lon": lon,
                 "temp_c": c["temperature_2m"], "humidity": c["relative_humidity_2m"],
                 "rain_mm": c["precipitation"]})
new = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)
if os.path.exists(PATH):
    new = pd.concat([pd.read_csv(PATH), new])
new = new.drop_duplicates(["time", "site"]).tail(8000)  # cap file size
new.to_csv(PATH, index=False)
print(f"Saved {len(new)} rows")
