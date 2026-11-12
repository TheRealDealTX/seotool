#!/usr/bin/env python3
"""Favicon pipeline: draws the brand mark (copper roofline over a white equals sign on a dark-blue tile)
and writes favicon.svg, favicon.ico (16/32/48, bold variant), favicon-96x96.png, apple-touch-icon.png
(full-bleed 180), maskable favicon-192/512 PNGs, assets/img/mark.svg and site.webmanifest into ../static.

python3 tools/make_icons.py   (needs Pillow)
"""
import json
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
TOP, BOT = (31, 79, 147), (10, 31, 63)
COPPER, WHITE = (224, 154, 95), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f4f93"/><stop offset="1" stop-color="#0a1f3f"/></linearGradient></defs><rect width="48" height="48" rx="10" fill="url(#g)"/><path d="M10 22.5L24 11l14 11.5" fill="none" stroke="#e09a5f" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/><path d="M15.5 28h17M15.5 35h17" stroke="#fff" stroke-width="{w}" stroke-linecap="round"/></svg>"""


def draw(size, radius=10, bold=False, full_bleed=False, safe=1.0):
    S = 1024
    k = S / 48
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    grad = Image.new("RGBA", (S, S))
    gd = ImageDraw.Draw(grad)
    for y in range(S):
        t = y / (S - 1)
        gd.line([(0, y), (S, y)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)) + (255,))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=0 if full_bleed else int(radius * k), fill=255)
    im.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(im)
    w = (5.0 if bold else 3.6) * k * safe
    c = S / 2

    def P(x, y):  # scale glyph around the centre for maskable safe zones
        return (c + (x * k - c) * safe, c + (y * k - c) * safe)

    roof = [P(10, 22.5), P(24, 11), P(38, 22.5)] if not bold else [P(9, 23), P(24, 10.5), P(39, 23)]
    d.line(roof, fill=COPPER, width=int(w), joint="curve")
    for pt in (roof[0], roof[2]):
        d.ellipse([pt[0] - w / 2, pt[1] - w / 2, pt[0] + w / 2, pt[1] + w / 2], fill=COPPER)
    for yy in ((28, 35) if not bold else (28.5, 36.5)):
        a, b = P(15.5 if not bold else 14, yy), P(32.5 if not bold else 34, yy)
        d.line([a, b], fill=WHITE, width=int(w))
        for pt in (a, b):
            d.ellipse([pt[0] - w / 2, pt[1] - w / 2, pt[0] + w / 2, pt[1] + w / 2], fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def main():
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG.format(w=3.6))
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG.format(w=3.6))
    ico = [draw(s, bold=True) for s in (16, 32, 48)]
    ico[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(32, bold=True).save(os.path.join(STATIC, "favicon-32x32.png"))
    draw(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw(180, full_bleed=True, safe=0.82).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for s in (192, 512):
        draw(s, full_bleed=True, safe=0.72).save(os.path.join(STATIC, f"favicon-{s}.png"))
    man = {"name": "South Carolina Insurance Appraiser", "short_name": "SC Appraiser", "start_url": "/", "display": "standalone",
           "background_color": "#0a1f3f", "theme_color": "#0a1f3f",
           "icons": [{"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                     {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
    json.dump(man, open(os.path.join(STATIC, "site.webmanifest"), "w"), indent=1)
    print("icons written")


if __name__ == "__main__":
    main()
