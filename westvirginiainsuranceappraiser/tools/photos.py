#!/usr/bin/env python3
"""Photo pipeline: src/photo_sources.json -> static/assets/img/photos/<key>.webp (<=1200w) + <key>-640.webp,
and src/photos.json (metadata incl. final width/height) used by build.py and /photo-credits/.
Sources are CC0 / public-domain images found via the Openverse API (license=cc0,pdm). Requires Pillow."""
import io, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "photo_sources.json")
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")
META = os.path.join(ROOT, "src", "photos.json")
os.makedirs(OUT, exist_ok=True)
src = json.load(open(SRC))
meta = json.load(open(META)) if os.path.exists(META) else {}


def fetch(url):
    """Download with retries. Wikimedia originals are rate-limited, so use their 1280px thumbnail."""
    urls = [url]
    if "upload.wikimedia.org" in url and "/thumb/" not in url:
        fn = url.rsplit("/", 1)[1]
        urls = [url.replace("/commons/", "/commons/thumb/") + "/1280px-" + fn, url]
    last = None
    for attempt in range(4):
        for u in urls:
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "WVIA-photo-pipeline/1.0 (static site build)"})
                return urllib.request.urlopen(req, timeout=90).read()
            except Exception as ex:
                last = ex
        time.sleep(5 * (attempt + 1))
    raise last


def run(key):
    v = src[key]
    big = os.path.join(OUT, key + ".webp")
    if os.path.exists(big) and key in meta and "--force" not in sys.argv:
        return key, "cached"
    im = Image.open(io.BytesIO(fetch(v["url"])))
    im = ImageOps.exif_transpose(im).convert("RGB")
    # crop very tall/wide images to 3:2 so cards and heroes behave
    w, h = im.size
    if w / h > 1.8 or w / h < 1.3:
        tw, th = (w, round(w / 1.5)) if w / h < 1.3 else (round(h * 1.5), h)
        tw, th = min(tw, w), min(th, h)
        im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))
    a = im.copy(); a.thumbnail((1200, 1200 * 2)); a.save(big, "WEBP", quality=78, method=6)
    b = im.copy(); b.thumbnail((640, 640 * 2)); b.save(os.path.join(OUT, key + "-640.webp"), "WEBP", quality=76, method=6)
    meta[key] = {**{k: v.get(k) for k in ("url", "title", "creator", "license", "source", "landing")}, "fw": a.size[0], "fh": a.size[1]}
    return key, a.size


def safe(k):
    try:
        return run(k)
    except Exception as ex:
        return k, f'FAILED {ex}'


with ThreadPoolExecutor(4) as ex:
    for k, r in ex.map(safe, list(src)):
        print(k, r)
for k in list(meta):
    if k not in src:
        meta.pop(k)
json.dump({k: meta[k] for k in src}, open(META, "w"), indent=1)
print(len(meta), "photos")
