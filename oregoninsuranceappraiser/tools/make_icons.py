#!/usr/bin/env python3
"""Favicon pipeline: writes favicon.svg, multi-size favicon.ico (bold variant at 16/32/48), favicon-96x96.png,
a full-bleed 180px apple-touch-icon, maskable 192/512 PNGs and site.webmanifest into ../static.
Run once after changing the mark: python3 tools/make_icons.py   (needs Pillow)."""
import json
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "static")
NAVY, SUN, WHITE = (0, 42, 134), (255, 234, 15), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#002a86"/><path d="M7 33.5L18.5 15l6 9.2 4.2-5.7L41 33.5z" fill="#ffea0f"/><path d="M18.5 15l-3.4 5.5 2.3-.9 1.3 1.7 1.4-1.6 2 .9z" fill="#fff"/><rect x="7" y="36.5" width="34" height="3.2" rx="1.6" fill="#fff"/></svg>
"""


def draw(size, bold=False, full_bleed=False, safe=1.0):
    """Render the mark on a 48-unit grid. bold: chunkier peaks/line for tiny sizes. safe: shrink art for maskable."""
    S = 1024
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = S / 48
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=NAVY)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(11 * k), fill=NAVY)
    c = 24
    t = lambda x, y: ((c + (x - c) * safe) * k, (c + (y - c) * safe) * k)
    if bold:
        peaks = [(5, 35), (18, 12), (25, 23), (30, 16.5), (43, 35)]
        line = (5, 38, 43, 43)
    else:
        peaks = [(7, 33.5), (18.5, 15), (24.5, 24.2), (28.7, 18.5), (41, 33.5)]
        line = (7, 36.5, 41, 39.7)
    d.polygon([t(*p) for p in peaks], fill=SUN)
    if not bold:
        cap = [(18.5, 15), (15.1, 20.5), (17.4, 19.6), (18.7, 21.3), (20.1, 19.7), (22.1, 20.6)]
        d.polygon([t(*p) for p in cap], fill=WHITE)
    x0, y0 = t(line[0], line[1]); x1, y1 = t(line[2], line[3])
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def main():
    open(os.path.join(OUT, "favicon.svg"), "w").write(SVG)
    ico = [draw(s, bold=True) for s in (16, 32, 48)]
    ico[2].save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(96).save(os.path.join(OUT, "favicon-96x96.png"))
    draw(180, full_bleed=True, safe=0.86).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
    for s in (192, 512):
        draw(s, full_bleed=True, safe=0.72).save(os.path.join(OUT, f"favicon-{s}.png"))
    man = {"name": "Oregon Insurance Appraiser", "short_name": "OR Appraiser", "start_url": "/", "display": "standalone",
           "background_color": "#f7f6f1", "theme_color": "#002a86",
           "icons": [{"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "maskable any"},
                     {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "maskable any"}]}
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps(man, indent=2) + "\n")
    print("icons written")


if __name__ == "__main__":
    main()
