#!/usr/bin/env python3
"""Favicon pipeline: draws the brand mark (prairie horizon + rising sun) and writes every icon into static/.
python3 tools/make_icons.py   (needs Pillow)"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
BLUE, SUN, WHITE, PALE, DEEP = (0, 116, 168), (255, 196, 0), (255, 255, 255), (159, 211, 234), (6, 50, 74)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#0074A8"/><path d="M13 27a11 11 0 0 1 22 0z" fill="#FFC400"/><path d="M8 27h32" stroke="#fff" stroke-width="3" stroke-linecap="round"/><path d="M12 32.5h24M17 37.5h14" stroke="#9fd3ea" stroke-width="2.6" stroke-linecap="round"/></svg>"""


def draw(size, bold=False, bleed=False, safe=1.0):
    """Render at 8x and downsample. bold = simplified mark for 16-48px. bleed = square full-bleed background.
    safe = scale of the artwork inside the canvas (maskable icons keep the art in the central safe zone)."""
    S = size * 8
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bleed:
        d.rectangle([0, 0, S, S], fill=BLUE)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 11 / 48), fill=BLUE)
    u = S / 48 * safe
    o = (S - 48 * u) / 2
    X = lambda v: o + v * u
    if bold:
        # bigger sun, one thick horizon, one thick underline
        d.pieslice([X(9), X(13), X(39), X(43)], 180, 360, fill=SUN)
        d.rounded_rectangle([X(5), X(26.5), X(43), X(32)], radius=int(2.7 * u), fill=WHITE)
        d.rounded_rectangle([X(12), X(36), X(36), X(41)], radius=int(2.5 * u), fill=PALE)
    else:
        d.pieslice([X(13), X(16), X(35), X(38)], 180, 360, fill=SUN)
        d.rounded_rectangle([X(6.5), X(25.5), X(41.5), X(28.5)], radius=int(1.5 * u), fill=WHITE)
        d.rounded_rectangle([X(10.7), X(31.2), X(37.3), X(33.8)], radius=int(1.3 * u), fill=PALE)
        d.rounded_rectangle([X(15.7), X(36.2), X(32.3), X(38.8)], radius=int(1.3 * u), fill=PALE)
    return im.resize((size, size), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    small = [draw(s, bold=True) for s in (16, 32, 48)]
    small[2].save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=small[:2])
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(32, bold=True).save(os.path.join(ST, "favicon-32x32.png"))
    draw(180, bleed=True, safe=0.86).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for s in (192, 512):
        draw(s, bleed=True, safe=0.74).save(os.path.join(ST, f"favicon-{s}.png"))
    print("icons written")


if __name__ == "__main__":
    main()
