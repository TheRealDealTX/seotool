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
    "hero-home": "Red brick Victorian house with gables and a tall chimney on a residential street in Norwood, Ohio",
    "house-porch": "Brick Victorian home with a turret and a wraparound front porch in Norwood, Ohio",
    "winter-house": "Red wood-sided house with an outdoor staircase surrounded by deep snow",
    "icicles-roof": "Row of icicles hanging from the edge of a snow-covered roof",
    "ice-storm": "Tree branches coated in ice with icicles hanging after an ice storm in Hocking County, Ohio",
    "storm-supercell": "Supercell thunderstorm with a lightning bolt over a barn and open farmland",
    "lightning": "Branching lightning bolts striking from a dark night sky",
    "storm-clouds": "Weathered old farmhouse in a field under dark storm clouds",
    "hailstones": "Pile of large white hailstones in the grass after a storm",
    "tornado-damage": "Debris from destroyed homes and stripped trees after an EF4 tornado",
    "tornado-aerial": "Aerial view of a neighborhood with homes destroyed and blue tarps along a tornado path",
    "wind-roof-damage": "Shingled church roof torn open by wind, exposing the wood decking beneath",
    "fallen-tree": "Large uprooted trees lying across the lawn in front of a brick ranch house",
    "flooded-basement": "Houses standing in floodwater up to the windows",
    "water-ceiling": "Collapsed bedroom ceiling with exposed wood boards above a dresser",
    "house-fire": "Wood house fully engulfed in flames at night",
    "fire-aftermath": "Fire-damaged frame house with charred, peeling siding on a city street",
    "roof-shingles": "Close-up of weathered wood shingles in overlapping rows",
    "roofer": "Roofers in safety harnesses working on the peak of a house roof",
    "slate-roof": "Close-up of overlapping natural slate roof tiles",
    "metal-roof": "Steel commercial building with a green corrugated metal roof",
    "commercial-building": "Glass and panel facade of a modern office building against a blue sky",
    "apartment-building": "Brick condominium building with white balconies beside a pond",
    "consultation": "Two women talking across a small round table by an office window",
    "paperwork": "Hand signing a document at a table with coffee and notes",
    "calculator": "Scientific calculator resting on printed papers on a wooden desk",
    "clipboard": "Inspectors in hard hats reviewing documents on a clipboard during an inspection",
    "kitchen": "Classic kitchen with cream cabinets, granite island and pendant lights",
    "living-room": "Living room with a stone fireplace, leather sectional sofa and hardwood floors",
    "columbus-skyline": "Downtown Columbus, Ohio skyline and a bridge over the Scioto River",
    "cleveland-skyline": "Cleveland, Ohio skyline lit up at night over the water",
    "cincinnati-skyline": "Downtown Cincinnati skyline at night reflected in the Ohio River",
    "toledo": "Historic Old Downtown Post Office building in Toledo, Ohio",
    "lake-erie": "Sunset over the waves of Lake Erie",
    "ohio-farm": "Amish farm with red barns and a white farmhouse beyond a harvested field in Holmes County, Ohio",
    "akron": "Downtown Akron, Ohio skyline at sunset",
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
