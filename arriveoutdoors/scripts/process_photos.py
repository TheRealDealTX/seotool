"""Turn assets/photos-src/*.jpg (Pexels downloads + manifests) into responsive WebP files
in assets/img/photos/ and write data/photos.json (alt text, credit, available widths).

    python3 scripts/process_photos.py
"""
import glob
import json
import os

from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "assets", "photos-src")
DST = os.path.join(ROOT, "assets", "img", "photos")
WIDTHS = (640, 1280, 1920)

os.makedirs(DST, exist_ok=True)
manifest = {}
for mf in sorted(glob.glob(os.path.join(SRC, "manifest-*.json"))):
    manifest.update(json.load(open(mf, encoding="utf-8")))

out = {}
for key, meta in sorted(manifest.items()):
    fp = os.path.join(SRC, meta.get("file") or key + ".jpg")
    if not os.path.exists(fp):
        print("missing", key)
        continue
    im = ImageOps.exif_transpose(Image.open(fp)).convert("RGB")
    w, h = im.size
    widths = []
    for tw in WIDTHS:
        if tw > w and widths:
            continue
        tw = min(tw, w)
        th = round(h * tw / w)
        im.resize((tw, th), Image.LANCZOS).save(os.path.join(DST, f"{key}-{tw}.webp"), "WEBP", quality=74, method=6)
        widths.append(tw)
    out[key] = {"widths": widths, "ratio": round(w / h, 3), "alt": meta.get("alt", ""),
                "photographer": meta.get("photographer"), "page": meta.get("page"), "source": meta.get("source", "Pexels")}
json.dump(out, open(os.path.join(ROOT, "data", "photos.json"), "w"), indent=1)
print(f"processed {len(out)} photos")
