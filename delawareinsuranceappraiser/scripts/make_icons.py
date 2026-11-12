#!/usr/bin/env python3
"""Generate favicon.svg, favicon.ico (16/32/48, bold variant), PNG icons, apple-touch-icon and the
manifest from the brand mark. Run: python3 scripts/make_icons.py  (writes into static/)."""
import json
import os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
SLATE, CORAL, WHITE = (35, 61, 77), (240, 121, 91), (255, 255, 255)

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#233D4D"/>'
       '<path d="M11 25.5L24 13.5l13 12" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M16.5 23.5V34h15V23.5" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
       '<path d="M12 38.5h24" stroke="#F0795B" stroke-width="3.6" stroke-linecap="round"/>'
       '<circle cx="24" cy="28" r="2.6" fill="#F0795B"/></svg>')


def line(d, pts, w, fill, s):
    pts = [(x * s, y * s) for x, y in pts]
    d.line(pts, fill=fill, width=int(w * s), joint="curve")
    r = w * s / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw(px, bold=False, radius=True, pad=0.0):
    """Render the mark at px (supersampled 8x). bold = thicker, simpler strokes for 16-48px.
    pad = inner padding fraction (maskable icons keep the art inside the safe zone)."""
    S = 8
    big = px * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if radius:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 11 / 48), fill=SLATE)
    else:
        d.rectangle([0, 0, big, big], fill=SLATE)
    inner = big * (1 - 2 * pad)
    s = inner / 48
    off = big * pad
    def L(pts, w, c):
        line(d, [(x + off / s, y + off / s) for x, y in pts], w, c, s)
    if bold:
        L([(9, 26), (24, 12), (39, 26)], 6.4, WHITE)
        L([(15.5, 23.5), (15.5, 33.5), (32.5, 33.5), (32.5, 23.5)], 5.2, WHITE)
        L([(11, 40.5), (37, 40.5)], 5.6, CORAL)
    else:
        L([(11, 25.5), (24, 13.5), (37, 25.5)], 3.6, WHITE)
        L([(16.5, 23.5), (16.5, 34), (31.5, 34), (31.5, 23.5)], 3.0, WHITE)
        L([(12, 38.5), (36, 38.5)], 3.6, CORAL)
        cx, cy, r = (24 + off / s) * s, (28 + off / s) * s, 2.6 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CORAL)
    return im.resize((px, px), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(SVG)
    ico = [draw(n, bold=True) for n in (16, 32, 48)]
    ico[2].save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw(180, radius=False, pad=0.08).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    for n in (192, 512):
        draw(n, radius=False, pad=0.12).save(os.path.join(ST, f"favicon-{n}.png"))
    man = {"name": "Delaware Insurance Appraiser", "short_name": "DE Appraiser", "start_url": "/", "display": "standalone",
           "theme_color": "#233D4D", "background_color": "#ffffff",
           "icons": [{"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                     {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
                     {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                     {"src": "/favicon.svg?v=1", "sizes": "any", "type": "image/svg+xml"}]}
    open(os.path.join(ST, "site.webmanifest"), "w").write(json.dumps(man, separators=(",", ":")))
    print("icons written")


if __name__ == "__main__":
    main()
