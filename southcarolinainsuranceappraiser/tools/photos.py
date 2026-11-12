#!/usr/bin/env python3
"""Photo pipeline: download selected CC0 / public-domain photos one at a time (with pauses and
backoff), save 1200px and 640px WebP into static/assets/img/photos/ and write src/photos.json
(title, creator, license, provider, landing page, alt text, output size) for img() and /photo-credits/.

python3 -I tools/photos.py <candidates.json> <selection.json>
  candidates.json: Openverse results keyed by short id (url, title, creator, license, source, landing, w, h)
  selection.json:  {"site-key": {"id": "<short id>", "alt": "Descriptive alt text", "crop": "center|top|bottom"}}
Wikimedia files are fetched at the standard 1280px thumbnail width; Flickr at the _b (1024px) size.
"""
import io
import json
import os
import sys
import time
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "static", "assets", "img", "photos")
CACHE = os.path.join(HERE, "..", ".photo-cache")  # originals; git-ignored, never deployed
UA = "StaticSitePhotoResearch/1.0 (one-at-a-time CC0/PD downloads; Python urllib)"


def get(url, tries=5):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as ex:  # noqa: BLE001
            wait = 6 * (2 ** i)
            print(f"  retry {i + 1} in {wait}s: {ex}")
            time.sleep(wait)
    return None


def src_url(c):
    u = c["url"]
    if "upload.wikimedia.org/wikipedia/commons/" in u and "/thumb/" not in u:
        a, rest = u.split("/wikipedia/commons/", 1)
        if (c.get("w") or 0) > 1280:
            return f"{a}/wikipedia/commons/thumb/{rest}/1280px-{rest.rsplit('/', 1)[1]}"
    return u


def fit(im, w, ratio=1.5, crop="center"):
    """Crop to a 3:2 frame (landscape) and resize to width w."""
    W, H = im.size
    if W / H > ratio:
        nw = int(H * ratio)
        x = (W - nw) // 2
        im = im.crop((x, 0, x + nw, H))
    elif W / H < ratio:
        nh = int(W / ratio)
        y = {"top": 0, "bottom": H - nh}.get(crop, (H - nh) // 2)
        im = im.crop((0, y, W, y + nh))
    # Sources under 1200px (Flickr _b = 1024px, StockSnap 960px) are upscaled with Lanczos to keep one size set.
    return im.resize((w, int(round(w / ratio))), Image.LANCZOS)


def main():
    cands = json.load(open(sys.argv[1]))
    sel = json.load(open(sys.argv[2]))
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    meta_path = os.path.join(HERE, "..", "src", "photos.json")
    meta = {}
    for key, s in sel.items():
        c = cands[s["id"]]
        raw = os.path.join(CACHE, f"{s['id']}.orig")
        if not os.path.exists(raw):
            print("get", key, c["source"])
            u = src_url(c)
            data = get(u, tries=2 if "/1280px-" in u else 5)
            if data is None and "/1280px-" in u:  # Wikimedia may refuse on-demand 1280px renders; 960px is pre-rendered
                time.sleep(5)
                data = get(u.replace("/1280px-", "/960px-"))
            if data is None:
                raise SystemExit(f"failed: {u}")
            Image.open(io.BytesIO(data)).verify()  # never cache an error page
            open(raw, "wb").write(data)
            time.sleep(3 if c["source"] == "wikimedia" else 1.5)
        im = Image.open(raw).convert("RGB")
        big = fit(im, 1200, crop=s.get("crop", "center"))
        big.save(os.path.join(OUT, f"{key}.webp"), "WEBP", quality=78, method=6)
        fit(im, 640, crop=s.get("crop", "center")).save(os.path.join(OUT, f"{key}-640.webp"), "WEBP", quality=74, method=6)
        meta[key] = {"title": c.get("title"), "creator": c.get("creator"), "license": c["license"], "provider": {"wikimedia": "Wikimedia Commons", "flickr": "Flickr", "rawpixel": "rawpixel", "stocksnap": "StockSnap"}.get(c["source"], c["source"]),
                     "landing": c.get("landing"), "url": c["url"], "alt": s["alt"], "fw": big.size[0], "fh": big.size[1]}
    json.dump(meta, open(meta_path, "w"), indent=1, ensure_ascii=False)
    for f in os.listdir(OUT):
        k = f.replace("-640.webp", "").replace(".webp", "")
        if f.endswith(".webp") and k not in sel:
            os.remove(os.path.join(OUT, f))
    print(f"wrote {len(meta)} photos")


if __name__ == "__main__":
    main()
