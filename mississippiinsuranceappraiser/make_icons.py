#!/usr/bin/env python3
"""Generate the favicon set into ./static from the brand mark (crimson tile, gold roofline, white level bars).

python3 make_icons.py   (needs Pillow). Outputs: favicon.svg, favicon.ico (16/32/48, bold variant),
favicon-96x96.png, apple-touch-icon.png (180, full bleed), favicon-192.png / favicon-512.png (maskable),
site.webmanifest. Bump FAV in build.py after changing the icons.
"""
import json
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
RED, GOLD, WHITE = (194, 31, 50), (234, 171, 34), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#C21F32"/><path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#EAAB22" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 31h18M15 37h18" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>
"""


def line(d, pts, w, fill, s):
    pts = [(x * s, y * s) for x, y in pts]
    d.line(pts, fill=fill, width=int(w * s), joint="curve")
    r = w * s / 2
    for x, y in pts:  # round caps
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw(size, bold=False, bleed=False, safe=1.0):
    """Render at 8x and downsample. bleed: square, no rounded corners. safe: scale artwork for maskable safe zone."""
    S = 8
    big = size * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = big / 48
    if bleed:
        d.rectangle([0, 0, big, big], fill=RED)
    else:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(11 * s), fill=RED)
    off = 24 * (1 - safe)

    def T(pts):
        return [(off + x * safe, off + y * safe) for x, y in pts]
    if bold:  # fewer, heavier strokes so 16px stays legible
        line(d, T([(8, 27), (24, 12), (40, 27)]), 6.4, GOLD, s)
        line(d, T([(14, 36), (34, 36)]), 6.0, WHITE, s)
    else:
        line(d, T([(10, 25.5), (24, 13), (38, 25.5)]), 4.4, GOLD, s)
        line(d, T([(15, 31), (33, 31)]), 3.6, WHITE, s)
        line(d, T([(15, 37), (33, 37)]), 3.6, WHITE, s)
    return im.resize((size, size), Image.LANCZOS)


def main():
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write(SVG)
    ico = [draw(n, bold=True) for n in (16, 32, 48)]
    ico[2].save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(96).save(os.path.join(OUT, "favicon-96x96.png"))
    draw(180, bleed=True, safe=0.86).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, bleed=True, safe=0.72).save(os.path.join(OUT, f"favicon-{n}.png"))
    manifest = {
        "name": "Mississippi Insurance Appraiser", "short_name": "MS Appraiser", "start_url": "/", "scope": "/",
        "display": "standalone", "background_color": "#FFF9F0", "theme_color": "#C21F32",
        "icons": [{"src": f"/favicon-{n}.png?v=1", "sizes": f"{n}x{n}", "type": "image/png", "purpose": "any maskable"} for n in (192, 512)],
    }
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump(manifest, f, separators=(",", ":"))
    print("icons written")


if __name__ == "__main__":
    main()
