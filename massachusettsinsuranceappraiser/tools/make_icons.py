#!/usr/bin/env python3
"""Favicon + logo pipeline for Massachusetts Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a coral saltbox-style gable roofline with a white window over a white tide line, on a slate tile.
Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
TOP, BOT = (46, 56, 74), (18, 22, 31)          # gradient top-left -> bottom-right (#2e384a -> #12161f)
CORAL, WHITE = (224, 122, 79), (255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2e384a"/><stop offset="1" stop-color="#12161f"/></linearGradient></defs><rect width="48" height="48" rx="11" fill="url(#g)"/><path d="M9.5 25.5L24 12l14.5 13.5" fill="none" stroke="#e07a4f" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/><rect x="20.5" y="21" width="7" height="7" rx="1.2" fill="#fff"/><path d="M8.5 35.5c3.1-2.6 6.2-2.6 9.3 0s6.2 2.6 9.3 0 6.2-2.6 9.3 0 2.6 1.1 3.1 1.1" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>"""


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOT))
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
    w = (5.6 if bold else 3.8) * k
    roof = [P(9.5, 25.5), P(24, 12), P(38.5, 25.5)] if not bold else [P(8, 26), P(24, 11), P(40, 26)]
    d.line(roof, fill=CORAL, width=round(w), joint="curve")
    for x, y in (roof[0], roof[-1]):
        rr = w / 2
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=CORAL)
    win = (19.5, 20.5, 28.5, 29.5) if bold else (20.5, 21, 27.5, 28)
    d.rounded_rectangle([*P(win[0], win[1]), *P(win[2], win[3])], radius=1.2 * k, fill=WHITE)
    # tide line: sampled sine wave
    import math
    ww = (4.4 if bold else 3.0) * k
    pts = [P(8.5 + i * 0.25, (37 if bold else 36) + (-2.4 if bold else -1.3) * math.sin((i * 0.25) / (15.5 if bold else 9.3) * 2 * math.pi)) for i in range(int(31 / 0.25) + 1)]
    d.line(pts, fill=WHITE, width=round(ww), joint="curve")
    for x, y in (pts[0], pts[-1]):
        rr = ww / 2
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=WHITE)
    return im.resize((n, n), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    big = draw(256, bold=True)
    big.save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    draw(32, bold=True).save(os.path.join(ST, "favicon-32x32.png"))
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(180, full=True, safe=0.86).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, full=True, safe=0.78).convert("RGB").save(os.path.join(ST, f"favicon-{n}.png"))
    print("icons written")


if __name__ == "__main__":
    main()
