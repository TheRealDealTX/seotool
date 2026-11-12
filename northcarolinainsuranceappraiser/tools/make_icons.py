#!/usr/bin/env python3
"""Favicon + logo pipeline for North Carolina Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a clay-colored roof peak that doubles as the fulcrum of a level/balance beam,
on a pine-green tile. Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
PINE_A, PINE_B = (36, 92, 60), (13, 43, 27)   # gradient top-left -> bottom-right
CLAY, CREAM = (226, 122, 79), (250, 246, 238)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#245c3c"/><stop offset="1" stop-color="#0d2b1b"/></linearGradient></defs><rect width="48" height="48" rx="11" fill="url(#g)"/><path d="M11 24.5L24 12l13 12.5" fill="none" stroke="#e27a4f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 31.5h24" stroke="#faf6ee" stroke-width="3.4" stroke-linecap="round"/><circle cx="24" cy="31.5" r="3.6" fill="#faf6ee"/><path d="M17 37h14" stroke="#faf6ee" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(PINE_A, PINE_B))
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
    w_roof = (5.6 if bold else 4) * k
    w_beam = (4.6 if bold else 3.4) * k
    d.line([P(11, 24.5), P(24, 12), P(37, 24.5)], fill=CLAY, width=round(w_roof), joint="curve")
    for x, y in (P(11, 24.5), P(37, 24.5)):
        r = w_roof / 2; d.ellipse([x - r, y - r, x + r, y + r], fill=CLAY)
    d.line([P(12, 31.5), P(36, 31.5)], fill=CREAM, width=round(w_beam))
    for x, y in (P(12, 31.5), P(36, 31.5)):
        r = w_beam / 2; d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM)
    cx, cy = P(24, 31.5); r = (4.4 if bold else 3.6) * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CREAM)
    if not bold:
        d.line([P(17, 37), P(31, 37)], fill=(170, 190, 175), width=round(2.4 * k))
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
