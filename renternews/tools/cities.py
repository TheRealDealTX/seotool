#!/usr/bin/env python3
"""Build the offline US place lists used by the weather search and geocode.py.

    python3 tools/cities.py cities5000.zip US.zip

Inputs are GeoNames dumps (CC BY 4.0, https://www.geonames.org/):
  https://download.geonames.org/export/dump/cities5000.zip
  https://download.geonames.org/export/zip/US.zip
Writes static/assets/data/us-cities.json  [[name, state, lat, lon, population], ...]
and    static/assets/data/zips-<d>.json   [[zip, place, state, lat, lon], ...] by first digit.
"""
import json, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static/assets/data")
os.makedirs(OUT, exist_ok=True)

cities = {}
with zipfile.ZipFile(sys.argv[1]) as z:
    for line in z.open("cities5000.txt").read().decode("utf-8").splitlines():
        f = line.split("\t")
        if f[8] != "US" or f[6] != "P":
            continue
        key = (f[1], f[10])
        row = [f[1], f[10], round(float(f[4]), 4), round(float(f[5]), 4), int(f[14] or 0)]
        if key not in cities or row[4] > cities[key][4]:
            cities[key] = row
rows = sorted(cities.values(), key=lambda r: -r[4])
json.dump(rows, open(os.path.join(OUT, "us-cities.json"), "w"), separators=(",", ":"), ensure_ascii=False)

zips = {}
with zipfile.ZipFile(sys.argv[2]) as z:
    for line in z.open("US.txt").read().decode("utf-8").splitlines():
        f = line.split("\t")
        if not f[9]:
            continue
        zips.setdefault(f[1][0], []).append([f[1], f[2], f[4], round(float(f[9]), 4), round(float(f[10]), 4)])
for d, rs in zips.items():
    json.dump(sorted(rs), open(os.path.join(OUT, f"zips-{d}.json"), "w"), separators=(",", ":"), ensure_ascii=False)
print(len(rows), "cities;", sum(map(len, zips.values())), "zips")
