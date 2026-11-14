#!/usr/bin/env python3
"""Logo, favicon and OG image pipeline.

python3 tools/icons.py [path/to/display-font] [path/to/body-font]
Writes favicon.svg, favicon.ico (16/32/48, bold variant), favicon-96x96.png, apple-touch-icon.png (180, full bleed),
favicon-192.png / favicon-512.png (maskable), site.webmanifest, assets/img/mark.svg and assets/img/og-image.jpg into static/.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "static")
NAVY, GOLD, SILVER, WHITE = (0, 42, 134), (255, 204, 0), (200, 200, 200), (255, 255, 255)
FAV = "1"

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="9" fill="#002A86"/><path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/><rect x="10" y="30" width="28" height="5" rx="1.2" fill="#FFCC00"/><rect x="10" y="37.5" width="17" height="3" rx="1" fill="#C8C8C8"/></svg>"""


def draw_mark(size, bold=False, bleed=False, safe=1.0):
    """Render the mark at size px. bold: thicker roof + one wide bar (legible at 16px). bleed: square, no rounded corners.
    safe: scale the glyph into the centre (maskable icons keep content inside the 80% safe zone)."""
    k = 8
    W = size * k
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bleed:
        d.rectangle([0, 0, W, W], fill=NAVY)
    else:
        d.rounded_rectangle([0, 0, W - 1, W - 1], radius=W * 9 / 48, fill=NAVY)
    u = W / 48 * safe
    o = (W - 48 * u) / 2
    P = lambda x, y: (o + x * u, o + y * u)
    sw = (6.2 if bold else 4.2) * u
    pts = [P(9 if bold else 10, 26 if bold else 25.5), P(24, 12 if bold else 13), P(39 if bold else 38, 26 if bold else 25.5)]
    d.line(pts, fill=WHITE, width=round(sw), joint="curve")
    for p in (pts[0], pts[2]):
        d.ellipse([p[0] - sw / 2, p[1] - sw / 2, p[0] + sw / 2, p[1] + sw / 2], fill=WHITE)
    if bold:
        d.rounded_rectangle([*P(9, 31), *P(39, 39)], radius=1.5 * u, fill=GOLD)
    else:
        d.rounded_rectangle([*P(10, 30), *P(38, 35)], radius=1.2 * u, fill=GOLD)
        d.rounded_rectangle([*P(10, 37.5), *P(27, 40.5)], radius=1 * u, fill=SILVER)
    return im.resize((size, size), Image.LANCZOS)


def main(fd=None, fb=None):
    open(os.path.join(S, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(S, "assets", "img"), exist_ok=True)
    open(os.path.join(S, "assets", "img", "mark.svg"), "w").write(SVG)
    ico = [draw_mark(n, bold=True) for n in (16, 32, 48)]
    ico[2].save(os.path.join(S, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
    draw_mark(96).save(os.path.join(S, "favicon-96x96.png"))
    draw_mark(180, bleed=True, safe=0.86).convert("RGB").save(os.path.join(S, "apple-touch-icon.png"))
    for n in (192, 512):
        draw_mark(n, bleed=True, safe=0.72).save(os.path.join(S, f"favicon-{n}.png"))
    json.dump({"name": "Nebraska Insurance Appraiser", "short_name": "NE Appraiser", "start_url": "/", "scope": "/",
               "icons": [{"src": f"/favicon-192.png?v={FAV}", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                         {"src": f"/favicon-512.png?v={FAV}", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
                         {"src": f"/favicon.svg?v={FAV}", "sizes": "any", "type": "image/svg+xml"}],
               "theme_color": "#002A86", "background_color": "#ffffff", "display": "standalone"},
              open(os.path.join(S, "site.webmanifest"), "w"))
    # OG image 1200x630 from a site photo
    ph = Image.open(os.path.join(S, "assets", "img", "photos", "hero-supercell.webp")).convert("RGB")
    r = max(1200 / ph.width, 630 / ph.height)
    ph = ph.resize((round(ph.width * r), round(ph.height * r)), Image.LANCZOS)
    x, y = (ph.width - 1200) // 2, (ph.height - 630) // 2
    og = ph.crop((x, y, x + 1200, y + 630))
    ov = Image.new("RGBA", (1200, 630))
    od = ImageDraw.Draw(ov)
    for i in range(1200):
        a = int(240 - 150 * (i / 1200))
        od.line([(i, 0), (i, 630)], fill=(0, 14, 48, a))
    og = Image.alpha_composite(og.convert("RGBA"), ov)
    d = ImageDraw.Draw(og)
    d.rectangle([0, 0, 1200, 12], fill=GOLD)
    og.alpha_composite(draw_mark(120), (72, 92))
    big = ImageFont.truetype(fd, 76) if fd else ImageFont.load_default()
    small = ImageFont.truetype(fb, 34) if fb else ImageFont.load_default()
    d.text((72, 250), "Nebraska Insurance", font=big, fill=WHITE)
    d.text((72, 336), "Appraiser", font=big, fill=WHITE)
    d.rectangle([72, 440, 172, 448], fill=GOLD)
    d.text((72, 470), "Independent appraisal for disputed property claims", font=small, fill=(227, 233, 247))
    d.text((72, 520), "All 93 counties  ·  (844) 537-1427", font=small, fill=GOLD)
    og.convert("RGB").save(os.path.join(S, "assets", "img", "og-image.jpg"), quality=86, optimize=True, progressive=True)
    print("icons + og written")


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
