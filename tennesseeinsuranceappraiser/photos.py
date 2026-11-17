#!/usr/bin/env python3
"""Photo pipeline: download each pick in src/photo_sources.json and write WebP files.

    python3 photos.py            # fetch missing photos only
    python3 photos.py --force    # re-fetch everything

Every source is CC0 or public domain (Openverse license=cc0,pdm) — no attribution required, so the
site has no credits page. Sources and licenses are recorded in src/photo_sources.json and README
for our own records. Output: static/assets/img/photos/<key>.webp (max 1200px wide) and <key>-640.webp,
plus src/photos.json (manifest with final widths/heights used by build.py).

Downloads run one at a time with pauses and exponential backoff (Openverse, Flickr and Wikimedia
rate-limit hard). Wikimedia files use the standard 1280px thumbnail width.
Requires Pillow with WebP support.
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "photo_sources.json")
OUTDIR = os.path.join(ROOT, "static", "assets", "img", "photos")
MANIFEST = os.path.join(ROOT, "src", "photos.json")
UA = {"User-Agent": "site-photo-pipeline/1.0"}


def best_url(p):
    u = p["url"]
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w)/(\w\w)/(.+)$", u)
    if m and (p.get("w") or 0) > 1280:
        n = m.group(3)
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/{n}/1280px-{n}"
    if "stocksnap.io" in u:
        return u  # CDN serves 960w; still fine behind overlays
    return u


def fetch(url):
    for attempt in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception as ex:
            wait = 8 * 2 ** attempt
            print(f"  retry in {wait}s: {ex}", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")


def main():
    force = "--force" in sys.argv
    picks = json.load(open(SRC))
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) and not force else {}
    for key, p in picks.items():
        big = os.path.join(OUTDIR, f"{key}.webp")
        if not force and key in manifest and os.path.exists(big):
            continue
        print("fetch", key)
        try:
            im = Image.open(io.BytesIO(fetch(best_url(p)))).convert("RGB")
        except RuntimeError as ex:
            print("  SKIPPED", key, ex, file=sys.stderr)
            continue
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(big, "WEBP", quality=80, method=6)
        sm = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS) if im.width > 640 else im
        sm.save(os.path.join(OUTDIR, f"{key}-640.webp"), "WEBP", quality=78, method=6)
        manifest[key] = {**{k: p[k] for k in ("title", "creator", "license", "source", "landing", "url", "alt")}, "fw": im.width, "fh": im.height}
        json.dump(manifest, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
        time.sleep(2.5)
    # keep manifest order/alt in sync with picks
    manifest = {k: {**manifest[k], "alt": picks[k]["alt"]} for k in picks if k in manifest}
    json.dump(manifest, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
    print(f"{len(manifest)} photos ready")


if __name__ == "__main__":
    main()
