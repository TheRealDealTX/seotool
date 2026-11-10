#!/usr/bin/env python3
"""Favicon + logo pipeline for Wyoming Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a white roof gable over a dark balance beam on its fulcrum (a fair valuation under one
roof), on a burnt-orange tile. Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
EMBER_A, EMBER_B = (228, 118, 46), (150, 60, 12)   # gradient top-left -> bottom-right
DARK, WHITE = (42, 18, 6), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e4762e"/><stop offset="1" stop-color="#963c0c"/></linearGradient></defs><rect width="48" height="48" rx="11" fill="url(#g)"/><path d="M9 25.5L24 12.5l15 13" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M12.5 32h23" stroke="#2a1206" stroke-width="3.4" stroke-linecap="round"/><path d="M24 32l-4.5 6.5h9z" fill="#2a1206"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(EMBER_A, EMBER_B))
    return im


def draw(n, bold=False, full=False, safe=1.0):
    """Render the mark at n px. full=True -> square full-bleed tile; safe<1 shrinks the glyph (maskable)."""
    S = 4 * n  # supersample
    im = grad(S).convert("RGBA")
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 11 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)

    def cap_line(pts, color, w):
        d.line(pts, fill=color, width=round(w), joint="curve")
        for x, y in pts:
            r = w / 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    roof_w = (5.6 if bold else 4) * k
    cap_line([P(9, 25.5), P(24, 12.5), P(39, 25.5)], WHITE, roof_w)
    beam_w = (4.8 if bold else 3.4) * k
    cap_line([P(12.5, 32), P(35.5, 32)], DARK, beam_w)
    fw = 5.5 if bold else 4.5
    d.polygon([P(24, 32), P(24 - fw, 38.5 + (0.8 if bold else 0)), P(24 + fw, 38.5 + (0.8 if bold else 0))], fill=DARK)
    return im.resize((n, n), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    big = draw(256, bold=True)
    big.save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(180, full=True, safe=0.86).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, full=True, safe=0.78).convert("RGB").save(os.path.join(ST, f"favicon-{n}.png"))
    print("icons written")


if __name__ == "__main__":
    main()
