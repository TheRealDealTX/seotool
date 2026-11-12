#!/usr/bin/env python3
"""Photo pipeline: source JPGs -> 1200px (or native, if smaller) and 640px WebP + src/photos.json.

usage: python3 photo_pipeline.py <dir with full-size jpgs named by key> <shortlist.json from the Openverse search>
Alt text lives in ALT below; credits come from the Openverse metadata (title, creator, license, source, landing page).
"""
import html, json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")
ALT = {
    "louisville-storm-skyline": "Storm clouds over the downtown Louisville skyline and the Ohio River",
    "lexington-horse-farm": "Horse farm with a white barn on rolling bluegrass pasture near Lexington",
    "bluegrass-horse-country": "Horses grazing behind black plank fences on a Kentucky horse farm",
    "horses-graze": "White-fenced pasture and farmhouse in Kentucky horse country",
    "tobacco-barn": "Traditional black Kentucky tobacco barn behind a field of yellow wildflowers",
    "tobacco-barns-pair": "Two black tobacco barns on a grassy hillside in Kentucky",
    "frankfort-capitol": "Kentucky State Capitol building in Frankfort under a blue sky",
    "capitol-plaza": "Capitol Plaza office buildings in Frankfort, Kentucky",
    "covington-bridge": "John A. Roebling Suspension Bridge spanning the Ohio River at Covington",
    "mainstrasse": "Brick storefronts and row buildings in Covington’s MainStrasse Village",
    "paducah-downtown": "Historic brick buildings along a street in downtown Paducah",
    "ohio-river-barge": "Towboat and barges moored on the Ohio River in western Kentucky",
    "bowling-green-wku": "Cherry Hall on the Western Kentucky University campus in Bowling Green",
    "owensboro-riverfront": "Riverfront memorial plaza with flags along the Ohio River in Owensboro",
    "louisville-downtown": "Colorful historic commercial buildings on a downtown Louisville street",
    "louisville-facade": "Ornate brick facade standing in a garden in Louisville",
    "tornado-aerial": "Aerial view of a neighborhood flattened by a tornado",
    "tornado-house": "Debris from a destroyed house after an EF3 tornado",
    "tornado-heath": "Commercial building with its roof and walls torn away by a tornado",
    "ice-storm-trees": "Ice-coated tree limbs fallen across a car in front of a brick home",
    "ice-storm-branches": "Tree branches bent low under a heavy coating of ice",
    "river-flood": "Aerial view of homes surrounded by floodwater",
    "flooded-basement": "Doorway to a basement filled with muddy floodwater",
    "house-fire-2": "Charred interior framing of a building after a fire",
    "roof-shingle": "Close-up of dark roof tiles in overlapping rows",
    "roofers": "Roofers working on the gable of a house roof",
    "roofing-crew": "Roofer installing new tiles on a steep roof",
    "hailstones": "Hailstone resting in the palm of a hand",
    "calculator": "Calculator and printed charts next to a laptop keyboard",
    "desk-calculator": "Laptop, notepad and calculator on a desk",
    "consultation": "Two women talking across a small table by an office window",
    "paperwork": "Hands taking notes on paper between two laptops",
    "team-meeting": "People reviewing notes and a laptop together at a table",
    "storm-clouds": "Dark storm clouds with light breaking through",
    "storm-over-homes": "Heavy storm clouds over rooftops at dusk",
    "lightning": "Lightning bolts striking under a dark night sky",
    "winter-house": "Brick and siding home with shrubs covered in snow",
    "country-brick": "Historic brick house with a steep roof set among trees",
    "kitchen": "Modern kitchen with a tiled backsplash and built-in oven",
    "apartment-building": "Three-story brick apartment building on a street corner",
    "living-room": "Living room with a stone fireplace and white armchairs",
    "mountain-hollow": "Black-and-white view over forested ridges in the Red River Gorge",
}
SRC = {"rawpixel": "rawpixel", "stocksnap": "StockSnap", "wikimedia": "Wikimedia Commons", "wordpress": "WordPress Photo Directory", "flickr": "Flickr"}


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()
    s = re.sub(r"^File:", "", s); s = re.sub(r"\.(jpe?g|png|tiff?)$", "", s, flags=re.I)
    return re.sub(r"\s+", " ", s)[:120]


def creator(c):
    c = re.sub(r"\s*\(source\)", "", clean(c))
    return "Unknown" if not c or "Unknown" in c or "Anonymous" in c else c


def main(src_dir, shortlist):
    meta = json.load(open(shortlist))
    os.makedirs(OUT, exist_ok=True)
    photos = {}
    for key, alt in ALT.items():
        im = Image.open(os.path.join(src_dir, key + ".jpg")).convert("RGB")
        w = min(1200, im.width)
        big = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
        big.save(os.path.join(OUT, key + ".webp"), "WEBP", quality=78, method=6)
        sm = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        sm.save(os.path.join(OUT, key + "-640.webp"), "WEBP", quality=76, method=6)
        m = meta[key]
        photos[key] = {"alt": alt, "fw": big.width, "fh": big.height, "title": clean(m["title"]) or key.replace("-", " ").title(),
                       "creator": creator(m.get("creator")), "license": m["license"], "source_name": SRC.get(m["source"], m["source"]),
                       "landing": m["landing"]}
    json.dump(photos, open(os.path.join(ROOT, "src", "photos.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(photos)} photos written")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
