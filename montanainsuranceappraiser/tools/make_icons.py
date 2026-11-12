#!/usr/bin/env python3
"""Favicon + logo pipeline for Montana Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a white twin-peak ridgeline (an "M" for Montana) over an amber measuring rule, with an
amber sun, on a dark-blue tile. Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
NAVY_A, NAVY_B = (30, 66, 140), (10, 23, 54)   # gradient top-left -> bottom-right
AMBER, WHITE = (242, 140, 40), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1e428c"/><stop offset="1" stop-color="#0a1736"/></linearGradient></defs><rect width="48" height="48" rx="12" fill="url(#g)"/><circle cx="35" cy="12.5" r="3.4" fill="#f28c28"/><path d="M8.5 31L18 17l6.5 9 5-6.5L39.5 31" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 37.5h30" stroke="#f28c28" stroke-width="3" stroke-linecap="round"/><path d="M16 37.5v3M24 37.5v3M32 37.5v3" stroke="#f28c28" stroke-width="2" stroke-linecap="round"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(NAVY_A, NAVY_B))
    return im


def draw(n, bold=False, full=False, safe=1.0):
    """Render the mark at n px. full=True -> square full-bleed tile; safe<1 shrinks the glyph (maskable)."""
    S = 4 * n  # supersample
    im = grad(S).convert("RGBA")
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 12 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)

    def cap_line(pts, color, w):
        d.line(pts, fill=color, width=round(w), joint="curve")
        for x, y in (pts[0], pts[-1]):
            r = w / 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    sx, sy = P(35, 12.5)
    r = (4.2 if bold else 3.4) * k
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=AMBER)
    ridge = [P(8.5, 31), P(18, 17), P(24.5, 26), P(29.5, 19.5), P(39.5, 31)]
    cap_line(ridge, WHITE, (5.2 if bold else 3.6) * k)
    for x, y in ridge[1:-1]:
        rr = (5.2 if bold else 3.6) * k / 2
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=WHITE)
    cap_line([P(9, 37.5), P(39, 37.5)], AMBER, (4.4 if bold else 3) * k)
    if not bold:
        for x in (16, 24, 32):
            cap_line([P(x, 37.5), P(x, 40.5)], AMBER, 2 * k)
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
