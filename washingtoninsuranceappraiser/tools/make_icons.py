#!/usr/bin/env python3
"""Favicon pipeline. Draws the brand mark (white roof chevron over a yellow "W" on an emerald tile) and writes
favicon.svg, favicon.ico (16/32/48, bolder strokes), favicon-96x96.png, apple-touch-icon.png (full-bleed 180),
maskable favicon-192/512 PNGs, assets/img/mark.svg and site.webmanifest into ../static.

python3 tools/make_icons.py   (needs Pillow)
"""
import json
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
GREEN, YELLOW, WHITE = (0, 132, 87), (255, 213, 32), (255, 255, 255)
FAV = "1"

ROOF = [(12, 18.5), (24, 9.5), (36, 18.5)]
W = [(11, 23.5), (16.2, 37.5), (24, 27), (31.8, 37.5), (37, 23.5)]
ROOF_B = [(10.5, 19.5), (24, 8.5), (37.5, 19.5)]
W_B = [(9.5, 25), (15.5, 39.5), (24, 28.5), (32.5, 39.5), (38.5, 25)]

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#008457"/>'
       '<path d="M12 18.5L24 9.5l12 9" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M11 23.5l5.2 14 7.8-10.5 7.8 10.5 5.2-14" fill="none" stroke="#FFD520" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def draw(size, radius=12, bold=False, full_bleed=False, safe=1.0):
    S = 1024
    k = S / 48
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=0 if full_bleed else int(radius * k), fill=GREEN + (255,))
    c = S / 2

    def P(x, y):
        return (c + (x * k - c) * safe, c + (y * k - c) * safe)

    def line(pts, color, w):
        pts = [P(*p) for p in pts]
        d.line(pts, fill=color, width=int(w), joint="curve")
        for pt in pts:  # round caps and joins
            d.ellipse([pt[0] - w / 2, pt[1] - w / 2, pt[0] + w / 2, pt[1] + w / 2], fill=color)

    line(ROOF_B if bold else ROOF, WHITE, (5.2 if bold else 3.4) * k * safe)
    line(W_B if bold else W, YELLOW, (5.6 if bold else 3.8) * k * safe)
    return im.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(STATIC, "assets", "img"), exist_ok=True)
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG)
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG)
    ico = [draw(s, radius=9 if s > 16 else 6, bold=True) for s in (16, 32, 48)]
    ico[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw(180, full_bleed=True, safe=0.84).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for s in (192, 512):
        draw(s, full_bleed=True, safe=0.7).save(os.path.join(STATIC, f"favicon-{s}.png"))
    man = {"name": "Washington Insurance Appraiser", "short_name": "WA Appraiser", "start_url": "/", "display": "standalone",
           "theme_color": "#00432c", "background_color": "#fbfcfa",
           "icons": [{"src": f"/favicon-192.png?v={FAV}", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                     {"src": f"/favicon-512.png?v={FAV}", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
                     {"src": f"/favicon-96x96.png?v={FAV}", "sizes": "96x96", "type": "image/png", "purpose": "any"},
                     {"src": f"/favicon.svg?v={FAV}", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]}
    json.dump(man, open(os.path.join(STATIC, "site.webmanifest"), "w"), separators=(",", ":"))
    print("icons written")


if __name__ == "__main__":
    main()
