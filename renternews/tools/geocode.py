#!/usr/bin/env python3
"""Fill content/geo.json with coordinates for every article's "city" field
("City, ST"), using the offline GeoNames list built by tools/cities.py.
Unknown cities are printed so you can add them to content/geo.json by hand.

    python3 tools/geocode.py
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from build import load_articles  # noqa: E402

cities = json.load(open(os.path.join(ROOT, "static/assets/data/us-cities.json")))
index = {}
for name, st, lat, lon, _pop in cities:          # list is sorted by population: first wins
    index.setdefault((name.lower(), st), [lat, lon])

path = os.path.join(ROOT, "content/geo.json")
geo = json.load(open(path)) if os.path.exists(path) else {}
for a in load_articles():
    city = a.get("city")
    if not city or city in geo:
        continue
    name, _, st = city.rpartition(", ")
    hit = index.get((name.lower(), st))
    if hit:
        geo[city] = hit
        print("ok  ", city, hit)
    else:
        print("MISS", city, "- add [lat, lon] to content/geo.json by hand")
json.dump(dict(sorted(geo.items())), open(path, "w"), indent=1)
