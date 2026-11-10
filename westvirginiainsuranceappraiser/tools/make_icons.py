#!/usr/bin/env python3
"""Favicon + logo pipeline for West Virginia Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a cream ridgeline over a rhododendron-pink level line, with a pink sun, on a forest-green tile.
Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
TOP, BOT = (35, 92, 22), (11, 31, 7)
CREAM, PINK = (244, 241, 232), (224, 103, 154)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#235c16"/><stop offset="1" stop-color="#0b1f07"/></linearGradient></defs><rect width="48" height="48" rx="10" fill="url(#g)"/><path d="M7 31l9.5-11 6 6.5L29 17l12 14" fill="none" stroke="#f4f1e8" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 37.5h26" stroke="#e0679a" stroke-width="3.4" stroke-linecap="round"/><circle cx="35.5" cy="12.5" r="3.2" fill="#e0679a"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        t = y / (n - 1)
        c = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOT))
        for x in range(n):
            px[x, y] = c
    return im


def draw(n, bold=False, full=False, safe=1.0):
    """Render the mark at n px. full=True -> square full-bleed tile; safe<1 shrinks the glyph (maskable)."""
    S = 4 * n
    im = grad(S).convert("RGBA")
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 10 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)
    w = (5.2 if bold else 3.4) * k
    pts = [P(7, 31), P(16.5, 20), P(22.5, 26.5), P(29, 17), P(41, 31)] if not bold else [P(6, 31), P(17, 18), P(31, 31), P(42, 31)]
    if bold:
        pts = [P(6, 32), P(17, 17), P(24, 25), P(30, 18), P(42, 32)]
    d.line(pts, fill=CREAM, width=round(w), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = w / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM)
    lw = (5 if bold else 3.4) * k
    a, b = P(10 if bold else 11, 38.5 if bold else 37.5), P(38 if bold else 37, 38.5 if bold else 37.5)
    d.line([a, b], fill=PINK, width=round(lw))
    for x, y in (a, b):
        r = lw / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=PINK)
    cx, cy = P(35.5, 12.5) if not bold else P(37, 10.5)
    r = (4.4 if bold else 3.2) * k
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PINK)
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
    p32 = os.path.join(ST, "favicon-32x32.png")
    if os.path.exists(p32):
        os.remove(p32)
    print("icons written")


if __name__ == "__main__":
    main()
