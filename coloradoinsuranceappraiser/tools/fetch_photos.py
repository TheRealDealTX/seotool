#!/usr/bin/env python3
"""Download the photos listed in src/photos.json and write 1200px + 640px WebP files to static/assets/img/photos.

Every entry must be CC0 or public domain (license "cc0" or "pdm"). The manifest keeps the source URL, landing
page, creator and license for our own records; none of it is published on the site.

    python3 tools/fetch_photos.py            # fetch missing files only
    python3 tools/fetch_photos.py --force    # re-fetch everything

Downloads run one at a time with pauses and backoff (Openverse, Flickr and Wikimedia rate-limit hard).
Wikimedia originals are requested through the standard 1280px thumbnail width.
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(ROOT, "src", "photos.json")
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")
UA = {"User-Agent": "site-photo-pipeline/1.0 (static site build)"}


def wm_thumb(url, width=1280):
    """https://upload.wikimedia.org/wikipedia/commons/a/ab/File.jpg -> .../thumb/a/ab/File.jpg/1280px-File.jpg"""
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/([0-9a-f])/([0-9a-f]{2})/([^/]+)$", url)
    if not m:
        return url
    base, a, ab, name = m.groups()
    return f"{base}/thumb/{a}/{ab}/{name}/{width}px-{name}"


def fetch(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as ex:  # noqa: BLE001
            wait = 8 * (attempt + 1)
            print(f"  retry in {wait}s: {ex}", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"could not download {url}")


def main(force=False):
    photos = json.load(open(MANIFEST))
    os.makedirs(OUT, exist_ok=True)
    for key, p in photos.items():
        assert p["license"] in ("cc0", "pdm"), f"{key}: license must be CC0 or public domain"
        big, small = os.path.join(OUT, f"{key}.webp"), os.path.join(OUT, f"{key}-640.webp")
        if not force and os.path.exists(big) and os.path.exists(small) and p.get("fw"):
            continue
        url = wm_thumb(p["url"]) if "upload.wikimedia.org" in p["url"] else p["url"]
        print(f"{key}: {url}", flush=True)
        im = Image.open(io.BytesIO(fetch(url)))
        im = ImageOps.exif_transpose(im).convert("RGB")
        crop = p.get("crop")  # optional [left, top, right, bottom] as fractions
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        w, h = im.size
        fw = 1200
        fh = round(h * fw / w)
        im.resize((fw, fh), Image.LANCZOS).save(big, "WEBP", quality=80, method=6)
        im.resize((640, round(h * 640 / w)), Image.LANCZOS).save(small, "WEBP", quality=78, method=6)
        p.update({"fw": fw, "fh": fh, "srcw": w, "srch": h})
        json.dump(photos, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
        time.sleep(2.5)
    json.dump(photos, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
    print("done", len(photos), "photos")


if __name__ == "__main__":
    main("--force" in sys.argv)
