"""Build data/climate.json: monthly climate normals for every destination.

Source: Open-Meteo historical weather API (ERA5 / ERA5-Land reanalysis), daily
values for 2015-2024 at each destination's visitor hub, corrected to the hub's
elevation. Run it again whenever DESTINATIONS changes:

    python3 scripts/fetch_climate.py
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from siteconfig import DESTINATIONS  # noqa: E402

START, END = "2015-01-01", "2024-12-31"
YEARS = 10
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "climate.json")
DAILY = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum",
         "snowfall_sum", "sunshine_duration", "wind_speed_10m_max"]


def fetch(lat, lon, elev):
    q = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon, "elevation": elev,
        "start_date": START, "end_date": END, "daily": ",".join(DAILY),
        "temperature_unit": "fahrenheit", "precipitation_unit": "inch",
        "wind_speed_unit": "mph", "timezone": "auto",
    })
    url = "https://archive-api.open-meteo.com/v1/archive?" + q
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # rate limit or transient error
            print("  retry", attempt + 1, e)
            time.sleep(10 * (attempt + 1))
    raise SystemExit("failed: " + url)


def summarize(d):
    days = d["daily"]
    acc = defaultdict(lambda: defaultdict(list))
    for i, t in enumerate(days["time"]):
        m = int(t[5:7]) - 1
        for k in DAILY:
            v = days[k][i]
            if v is not None:
                acc[m][k].append(v)
    months = []
    for m in range(12):
        a = acc[m]
        hi, lo = a["temperature_2m_max"], a["temperature_2m_min"]
        pr, sn = a["precipitation_sum"], a["snowfall_sum"]
        sun, wind = a["sunshine_duration"], a["wind_speed_10m_max"]
        months.append({
            "high": round(sum(hi) / len(hi), 1),
            "low": round(sum(lo) / len(lo), 1),
            "precip_in": round(sum(pr) / YEARS, 2),            # monthly total
            "wet_days": round(sum(1 for v in pr if v >= 0.04) / YEARS, 1),
            "snow_in": round(sum(sn) / YEARS, 1),
            "snow_days": round(sum(1 for v in sn if v >= 0.4) / YEARS, 1),
            "hot_days": round(sum(1 for v in hi if v >= 90) / YEARS, 1),
            "freeze_nights": round(sum(1 for v in lo if v <= 32) / YEARS, 1),
            "sun_hours": round(sum(sun) / len(sun) / 3600, 1),  # per day
            "wind_mph": round(sum(wind) / len(wind), 1),         # mean daily max
        })
    return months


def main():
    out = {"source": "Open-Meteo historical weather API (ERA5 reanalysis), daily data "
                     f"{START[:4]}–{END[:4]}, adjusted to each hub's elevation",
           "places": {}}
    if os.path.exists(OUT):
        out["places"] = json.load(open(OUT)).get("places", {})
    for slug, name, _state, lat, lon, elev, hub in DESTINATIONS:
        if slug in out["places"]:
            continue
        print(slug)
        out["places"][slug] = {"hub": hub, "lat": lat, "lon": lon, "elevation_m": elev,
                               "months": summarize(fetch(lat, lon, elev))}
        json.dump(out, open(OUT, "w"), indent=1)
        time.sleep(3)
    json.dump(out, open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
