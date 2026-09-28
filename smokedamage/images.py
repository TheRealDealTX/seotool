#!/usr/bin/env python3
"""Build responsive AVIF + WebP variants from src/img/*.jpg (needs Pillow).

    python3 images.py

Writes assets/img/<key>-<width>.{avif,webp} and assets/img/variants.json,
which build.py uses for <picture> srcsets. Run only when src/img changes.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "img")
OUT = os.path.join(ROOT, "assets", "img")
WIDTHS = [480, 800, 1200, 1600]


def main():
    manifest = json.load(open(os.path.join(SRC, "manifest.json")))
    variants = {}
    for key in sorted(manifest):
        src = next((os.path.join(SRC, key + ext) for ext in (".jpg", ".jpeg", ".png", ".webp")
                    if os.path.exists(os.path.join(SRC, key + ext))), None)
        if not src:
            print("missing source for", key)
            continue
        im = Image.open(src).convert("RGB")
        widths = [w for w in WIDTHS if w <= im.width] or [im.width]
        for w in widths:
            h = round(im.height * w / im.width)
            r = im.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(OUT, f"{key}-{w}.webp"), "WEBP", quality=78, method=6)
            r.save(os.path.join(OUT, f"{key}-{w}.avif"), "AVIF", quality=55, speed=6)
        variants[key] = {"widths": widths, "width": im.width, "height": im.height}
        print(key, widths)
    # Open Graph default (1200x630 crop of the hero)
    if "hero-fire-house" in variants:
        src = os.path.join(SRC, "hero-fire-house.jpg")
        im = Image.open(src).convert("RGB")
        ratio = 1200 / 630
        w, h = im.size
        if w / h > ratio:
            nw = int(h * ratio); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / ratio); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, "og-default.webp"), "WEBP", quality=80)
    json.dump(variants, open(os.path.join(OUT, "variants.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
