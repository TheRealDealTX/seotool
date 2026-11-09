#!/usr/bin/env python3
"""Favicon + logo pipeline for Nevada Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg (flat colors, no ids, so it can be inlined
several times per page), favicon.ico (16/32/48 from a bolder variant), favicon-96x96.png,
apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a gold sun over a cream mountain ridge with a gold level line, on a deep bronze tile.
Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
TILE = (33, 26, 11)        # #211a0b deep bronze
GOLD = (226, 177, 60)      # #e2b13c
CREAM = (251, 243, 220)    # #fbf3dc

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
       '<rect width="48" height="48" rx="11" fill="#211a0b"/>'
       '<circle cx="31" cy="16.5" r="6.2" fill="#e2b13c"/>'
       '<path d="M7.5 33.5l9.5-12 6 7.5 6.5-9 11 13.5" fill="none" stroke="#fbf3dc" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M10 39.5h28" stroke="#e2b13c" stroke-width="2.6" stroke-linecap="round"/></svg>')


def draw(n, bold=False, full=False, safe=1.0):
    S = 4 * n
    im = Image.new("RGBA", (S, S), TILE + (255,))
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 11 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)
    # sun
    cx, cy = P(31, 15.5 if bold else 16.5)
    r = (7.4 if bold else 6.2) * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    # ridge
    w = round((5.2 if bold else 3.4) * k)
    pts = [P(7.5, 34), P(17, 21.5), P(23, 29), P(29.5, 20), P(40.5, 34)] if bold else [P(7.5, 33.5), P(17, 21.5), P(23, 29), P(29.5, 20), P(40.5, 33.5)]
    d.line(pts, fill=CREAM, width=w, joint="curve")
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=CREAM)
    if not bold:
        y = P(0, 39.5)[1]
        x1, x2 = P(10, 0)[0], P(38, 0)[0]
        lw = round(2.6 * k)
        d.line([(x1, y), (x2, y)], fill=GOLD, width=lw)
        for x in (x1, x2):
            d.ellipse([x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2], fill=GOLD)
    return im.resize((n, n), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    ico = [draw(s, bold=True) for s in (16, 32, 48)]
    ico[2].save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(180, full=True, safe=0.84).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, full=True, safe=0.76).convert("RGB").save(os.path.join(ST, f"favicon-{n}.png"))
    print("icons written")


if __name__ == "__main__":
    main()
