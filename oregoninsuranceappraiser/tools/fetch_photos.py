#!/usr/bin/env python3
"""Photo pipeline: download picked CC0 / public-domain originals (found via the Openverse API) one at a time,
then write 1200px and 640px WebP into static/assets/img/photos and the manifest src/photos.json
(source URL, license, creator, size, alt text). Internal record only; nothing here is published as credits.

usage: python3 tools/fetch_photos.py <openverse-candidates.json>   (needs Pillow)"""
import io
import json
import os
import sys
import time
import urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, "..", "static", "assets", "img", "photos")
MANIFEST = os.path.join(HERE, "..", "src", "photos.json")
UA = {"User-Agent": "site-photo-pipeline/1.0"}

# key: (openverse id prefix, alt text)
PICKS = {
    "hero-home": ("05b7ff", "Portland, Oregon spread below forested hills with Mount Hood on the horizon"),
    "portland-downtown": ("36e9f7", "Downtown Portland office towers rising above green trees"),
    "salem-capitol": ("3434c9", "Oregon State Capitol in Salem behind cherry blossoms and daffodils"),
    "bend-drake-park": ("6013ec", "Mirror Pond at Drake Park in Bend, Oregon, framed by pines and autumn trees"),
    "calapooia-winter": ("79bd9d", "Snow-covered evergreens along the Calapooia River in winter"),
    "siuslaw-winter": ("db1e7f", "Frosted firs and mist along the Siuslaw River in winter"),
    "coast-waves": ("7b4a89", "Winter storm waves breaking over rocks on the Oregon coast"),
    "cannon-beach": ("db87a4", "Rocky Oregon coastline with sea stacks and a low fog bank"),
    "hood-lake": ("5fe8a4", "Snow-capped Mount Hood reflected in a still forest lake"),
    "crooked-river": ("f01ec0", "High-desert canyon of the Crooked River in Central Oregon"),
    "storm-hills": ("a047be", "Dark storm clouds over open grassy hills"),
    "barn-valley": ("82b30c", "Red barn reflected in a farm pond in western Oregon"),
    "ice-storm": ("f23ec4", "Ice-coated tree limbs collapsed over a parked car and house after an ice storm"),
    "ice-limbs": ("2ee803", "Ice storm damage with a large limb split from a tree"),
    "snow-cabin": ("6e1eb4", "Wood cabin under heavy snow among snow-laden trees"),
    "tree-roof": ("ef55cf", "Fallen tree trunk crushing the roof and wall of a building"),
    "roof-damage": ("624fd9", "Damaged, sagging roof edge and shingles on an older house"),
    "roof-shingles": ("0b83e8", "Close view of rows of dark roof shingles"),
    "rain-window": ("05dfeb", "Heavy rain drops on a window with blurred lights behind"),
    "house-fire": ("223493", "House engulfed in flames at night"),
    "wildfire-aftermath": ("6f0175", "Neighborhood lot reduced to ash and debris after a wildfire"),
    "wildfire-street": ("2f536a", "Smoke-filled sky over a residential street during a wildfire"),
    "wildfire-forest": ("2dbff9", "Sunlight streaming through wildfire smoke in a conifer forest"),
    "wildfire-crew": ("b0b4e1", "Wildland firefighters working a fire line on a smoky hillside"),
    "smoke-landscape": ("a4ca4c", "Trees and dry grass under a hazy, smoke-filled sky"),
    "storm-clouds": ("c42632", "Dramatic dark storm clouds with light breaking through"),
    "lightning": ("d9650c", "Lightning bolt striking during a night thunderstorm"),
    "commercial-glass": ("97f7b6", "Modern glass office building against a blue sky"),
    "apartments": ("8d0a4b", "Apartment building exterior with rows of windows"),
    "meeting": ("99aae2", "People reviewing papers and a laptop at a meeting table"),
    "plans-clipboard": ("14cac5", "Contractor in a safety vest writing on a clipboard over plans"),
    "builder-house": ("50b6db", "Builder in a hard hat walking toward a house under construction"),
    "calculator": ("1a11f4", "Calculator beside printed charts and a laptop"),
    "kitchen": ("f9f515", "Kitchen with wood cabinets, stone counters and a range"),
    "living-room": ("ab2997", "Bright living room with sofa, armchair and coffee table"),
    "house-dusk": ("2b7392", "Two-story family home with lights on at dusk"),
}


def fetch(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as ex:
            print("  retry", i + 1, ex, flush=True)
            time.sleep(6 * (i + 1))
    raise RuntimeError("download failed: " + url)


def main(cands):
    allc = json.load(open(cands))
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    os.makedirs(DST, exist_ok=True)
    for key, (pref, alt) in PICKS.items():
        hits = [r for i, r in allc.items() if i.startswith(pref)]
        if len(hits) != 1:
            print("!! ambiguous/missing", key, pref, len(hits)); continue
        r = hits[0]
        assert r["license"] in ("cc0", "pdm"), (key, r["license"])
        out = os.path.join(DST, key + ".webp")
        if key in man and os.path.exists(out):
            man[key]["alt"] = alt
            continue
        print("get", key, r["url"], flush=True)
        im = Image.open(io.BytesIO(fetch(r["url"]))).convert("RGB")
        fw = min(1200, im.width)
        big = im.resize((fw, round(im.height * fw / im.width)), Image.LANCZOS)
        big.save(out, "WEBP", quality=78, method=6)
        sm = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        sm.save(os.path.join(DST, key + "-640.webp"), "WEBP", quality=74, method=6)
        man[key] = {"title": r["title"], "creator": r["creator"], "license": r["license"], "provider": r["provider"],
                    "source": r["source"], "landing": r["foreign_landing_url"], "file": r["url"], "openverse_id": r["id"],
                    "fw": big.width, "fh": big.height, "alt": alt}
        json.dump(man, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
        time.sleep(2.5)
    json.dump(man, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
    print("done", len(man))


if __name__ == "__main__":
    main(sys.argv[1])
