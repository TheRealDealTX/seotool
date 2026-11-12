#!/usr/bin/env python3
"""Favicon + logo pipeline for Arizona Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a turquoise sun rising behind a sandstone mesa line on a dark-red tile. Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
RED_A, RED_B = (166, 32, 32), (58, 9, 9)       # gradient top-left -> bottom-right
SUN, SAND = (46, 184, 172), (246, 226, 200)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a62020"/><stop offset="1" stop-color="#3a0909"/></linearGradient></defs><rect width="48" height="48" rx="11" fill="url(#g)"/><circle cx="24" cy="21" r="7.5" fill="#2eb8ac"/><path d="M7.5 33.5h9l3.6-7.5h7.8l3.6 7.5h9" fill="none" stroke="#f6e2c8" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 39.5h22" stroke="#f6e2c8" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(RED_A, RED_B))
    return im


def draw(n, bold=False, full=False, safe=1.0):
    """Render the mark at n px. full=True -> square full-bleed tile; safe<1 shrinks the glyph (maskable)."""
    S = 4 * n
    im = grad(S).convert("RGBA")
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 11 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)
    cx, cy = P(24, 21); r = (8.5 if bold else 7.5) * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN)
    w = (5.2 if bold else 3.6) * k
    pts = [P(7.5, 33.5), P(16.5, 33.5), P(20.1, 26), P(27.9, 26), P(31.5, 33.5), P(40.5, 33.5)]
    d.line(pts, fill=SAND, width=round(w), joint="curve")
    for x, y in (pts[0], pts[-1]):
        rr = w / 2; d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=SAND)
    if not bold:
        d.line([P(13, 39.5), P(35, 39.5)], fill=(214, 160, 150), width=round(2.4 * k))
    return im.resize((n, n), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    draw(256, bold=True).save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(180, full=True, safe=0.86).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, full=True, safe=0.78).convert("RGB").save(os.path.join(ST, f"favicon-{n}.png"))
    print("icons written")


if __name__ == "__main__":
    main()
