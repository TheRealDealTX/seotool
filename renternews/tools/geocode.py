#!/usr/bin/env python3
"""Fill content/geo.json with coordinates for every article's "city" field.

Uses the Open-Meteo geocoding API (no key). Results are cached in
content/geo.json and committed, so build.py never needs the network.
    python3 tools/geocode.py
"""
import json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from build import load_articles  # noqa: E402

STATES = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District of Columbia","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming","PR":"Puerto Rico"}

path = os.path.join(ROOT, "content/geo.json")
geo = json.load(open(path)) if os.path.exists(path) else {}
for a in load_articles():
    city = a.get("city")
    if not city or city in geo:
        continue
    name, _, st = city.rpartition(", ")
    q = urllib.parse.urlencode({"name": name, "count": 10, "country": "US", "format": "json"})
    res = json.load(urllib.request.urlopen("https://geocoding-api.open-meteo.com/v1/search?" + q)).get("results", [])
    hit = next((r for r in res if r.get("admin1") == STATES.get(st)), None)
    if hit:
        geo[city] = [round(hit["latitude"], 4), round(hit["longitude"], 4)]
        print("ok  ", city, geo[city])
    else:
        print("MISS", city)
json.dump(dict(sorted(geo.items())), open(path, "w"), indent=1)
