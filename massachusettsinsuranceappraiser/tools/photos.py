#!/usr/bin/env python3
"""Photo pipeline: src/photo_sources.json -> static/assets/img/photos/<key>.webp (<=1200w) + <key>-640.webp,
and src/photos.json (metadata incl. final width/height) used by build.py and /photo-credits/.
Sources are CC0 / public-domain images found via the Openverse API (license=cc0,pdm). Requires Pillow."""
import io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "photo_sources.json")
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")
META = os.path.join(ROOT, "src", "photos.json")
os.makedirs(OUT, exist_ok=True)
src = json.load(open(SRC))
meta = json.load(open(META)) if os.path.exists(META) else {}


def run(key):
    try:
        return _run(key)
    except Exception as ex:
        return key, f"FAILED {ex}"


def _run(key):
    v = src[key]
    big = os.path.join(OUT, key + ".webp")
    if os.path.exists(big) and key in meta and "--force" not in sys.argv:
        return key, "cached"
    req = urllib.request.Request(v["url"], headers={"User-Agent": "Mozilla/5.0 (photo pipeline)"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read()))
    im = ImageOps.exif_transpose(im).convert("RGB")
    # crop very tall/wide images to 3:2 so cards and heroes behave
    w, h = im.size
    if w / h > 1.8 or w / h < 1.3:
        tw, th = (w, round(w / 1.5)) if w / h < 1.3 else (round(h * 1.5), h)
        tw, th = min(tw, w), min(th, h)
        im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))
    a = im.copy(); a.thumbnail((1200, 1200 * 2)); a.save(big, "WEBP", quality=78, method=6)
    b = im.copy(); b.thumbnail((640, 640 * 2)); b.save(os.path.join(OUT, key + "-640.webp"), "WEBP", quality=76, method=6)
    meta[key] = {**{k: v[k] for k in ("url", "title", "creator", "license", "source", "landing")}, "fw": a.size[0], "fh": a.size[1]}
    return key, a.size


with ThreadPoolExecutor(6) as ex:
    for k, r in ex.map(run, list(src)):
        print(k, r)
for k in list(meta):
    if k not in src or not os.path.exists(os.path.join(OUT, k + '.webp')):
        meta.pop(k)
json.dump({k: meta[k] for k in src if k in meta}, open(META, "w"), indent=1)
print(len(meta), "photos")
