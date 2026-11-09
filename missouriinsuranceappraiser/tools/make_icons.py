#!/usr/bin/env python3
"""Favicon + logo pipeline for Missouri Insurance Appraiser.

Writes static/favicon.svg, static/assets/img/mark.svg, favicon.ico (16/32/48, bolder strokes),
favicon-96x96.png, apple-touch-icon.png (180, full-bleed) and maskable favicon-192/512.png.
The mark: a cream catenary arch over a teal roof line and ground line, on an espresso tile. Requires Pillow.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
TOP, BOT = (90, 58, 34), (23, 13, 6)          # gradient top-left -> bottom-right
CREAM, TEAL = (246, 239, 229), (95, 193, 196)

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
       '<stop offset="0" stop-color="#5a3a22"/><stop offset="1" stop-color="#170d06"/></linearGradient></defs>'
       '<rect width="48" height="48" rx="12" fill="url(#g)"/>'
       '<path d="M12.5 38V35C12.5 20 16.5 11 24 11S35.5 20 35.5 35V38" fill="none" stroke="#f6efe5" stroke-width="3.4" stroke-linecap="round"/>'
       '<path d="M18.5 31.5L24 26l5.5 5.5" fill="none" stroke="#5fc1c4" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M8.5 38.5h31" stroke="#5fc1c4" stroke-width="3.2" stroke-linecap="round"/></svg>')


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


ARCH = [(12.5, 38)] + bez((12.5, 35), (12.5, 20), (16.5, 11), (24, 11)) + bez((24, 11), (31.5, 11), (35.5, 20), (35.5, 35))[1:] + [(35.5, 38)]


def grad(n):
    im = Image.new("RGB", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            t = (x + y) / (2 * (n - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOT))
    return im


def poly(d, pts, color, w):
    d.line(pts, fill=color, width=round(w), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = w / 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def draw(n, bold=False, full=False, safe=1.0):
    S = 4 * n
    im = grad(S).convert("RGBA")
    if not full:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 12 / 48, fill=255)
        im.putalpha(mask)
    d = ImageDraw.Draw(im)
    k = S / 48 * safe
    off = S / 2 - 24 * k
    P = lambda x, y: (off + x * k, off + y * k)
    poly(d, [P(*p) for p in ARCH], CREAM, (5.2 if bold else 3.4) * k)
    if not bold:
        poly(d, [P(18.5, 31.5), P(24, 26), P(29.5, 31.5)], TEAL, 3.2 * k)
    poly(d, [P(8.5, 38.5), P(39.5, 38.5)], TEAL, (4.8 if bold else 3.2) * k)
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
