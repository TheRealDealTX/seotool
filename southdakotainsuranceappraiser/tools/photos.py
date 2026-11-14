#!/usr/bin/env python3
"""Photo pipeline. Reads src/photo_sources.json (key -> source record), downloads each original once
(one file at a time, with pauses and backoff), and writes static/assets/img/photos/<key>.webp (1200px)
and <key>-640.webp, then src/photos.json (source record + rendered width/height) for build.py.
Only CC0 / public-domain images belong in the manifest. Needs Pillow."""
import json, os, re, sys, time, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "photo_sources.json")
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")
CACHE = os.path.join(ROOT, "tools", ".cache")
UA = {"User-Agent": "CC0PhotoPipeline/1.0 (one-off site build; Python-urllib)"}


def get(url, tries=5):
    for a in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as ex:
            wait = 10 * (a + 1) * (3 if "429" in str(ex) else 1)
            print(f"  retry in {wait}s: {ex}", flush=True)
            time.sleep(wait)
    raise RuntimeError("download failed: " + url)


def best_url(rec):
    """Flickr: the photo page lists larger sizes than the 1024px URL Openverse indexes."""
    if rec["source"] == "flickr" and rec.get("landing"):
        page = get(rec["landing"]).decode("utf-8", "ignore")
        time.sleep(4)
        for k in ("h", "k", "c", "l"):
            m = re.search(r'"%s":\{"displayUrl":"([^"]+)","width":(\d+)' % k, page)
            if m and int(m.group(2)) >= 1200 or (m and k in ("c", "l")):
                return "https:" + m.group(1).replace("\\/", "/")
    # rawpixel: keep the clean editor_1024 file; its larger public renditions are watermarked.
    return rec["url"]


def main():
    srcs = json.load(open(SRC))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    meta = {}
    for key, rec in srcs.items():
        cached = os.path.join(CACHE, key + ".orig")
        if not os.path.exists(cached):
            print("fetch", key, flush=True)
            url = best_url(rec)
            open(cached, "wb").write(get(url))
            rec["fetched"] = url
            time.sleep(3)
        im = ImageOps.exif_transpose(Image.open(cached)).convert("RGB")
        crop = rec.get("crop")  # optional [left, top, right, bottom] as fractions
        if crop:
            w, h = im.size
            im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        w, h = im.size
        if w / h > 2.2:  # keep panoramas usable as card images
            nw = int(h * 2.0); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h)); w = nw
        big = im if w <= 1200 else im.resize((1200, round(h * 1200 / w)), Image.LANCZOS)
        big.save(os.path.join(OUT, key + ".webp"), "WEBP", quality=78, method=6)
        sm = im.resize((640, round(h * 640 / w)), Image.LANCZOS)
        sm.save(os.path.join(OUT, key + "-640.webp"), "WEBP", quality=76, method=6)
        meta[key] = dict(rec, fw=big.size[0], fh=big.size[1], orig_w=w, orig_h=h)
        if w < 1200:
            print(f"  note: {key} source is only {w}px wide", flush=True)
    json.dump(srcs, open(SRC, "w"), indent=1, ensure_ascii=False)
    json.dump(meta, open(os.path.join(ROOT, "src", "photos.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(meta)} photos processed")


if __name__ == "__main__":
    sys.exit(main())
