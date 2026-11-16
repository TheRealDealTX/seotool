#!/usr/bin/env python3
"""Favicon, app-icon and OG-image pipeline for californiainsuranceappraiser.com.

python3 make_icons.py [path/to/display-font.ttf] [path/to/text-font.ttf]
Writes into ./static: favicon.svg, favicon.ico (16/32/48, bold mark), favicon-96x96.png,
apple-touch-icon.png (180, full-bleed), favicon-192.png / favicon-512.png (maskable),
site.webmanifest and assets/img/og-image.jpg (1200x630, built from a site photo).
Requires Pillow. Fonts are optional (falls back to DejaVu).
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(ROOT, "static")
CRIMSON, CRIMSON_DARK, COPPER_LIGHT, WHITE = (186, 12, 47), (74, 6, 19), (226, 176, 126), (255, 255, 255)
FAV = "1"

# Same geometry as build.py's mark() on a 48-unit grid.
SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#ba0c2f"/>'
       '<path d="M10 23.5L24 12l14 11.5" fill="none" stroke="#e2b07e" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
       '<rect x="15" y="27" width="18" height="3.6" rx="1.8" fill="#fff"/><rect x="15" y="33.6" width="18" height="3.6" rx="1.8" fill="#fff"/></svg>')


def draw_mark(size, bold=False, full_bleed=False, safe=1.0):
    """Render the mark at `size` px. bold = thicker, simplified strokes for 16-48px.
    full_bleed = square background (apple-touch / maskable); safe scales the glyph into the safe zone."""
    S = 1024
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = S / 48
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=CRIMSON)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=(13 if bold else 11) * u, fill=CRIMSON)
    k = safe
    c = S / 2

    def P(x, y):  # scale around the centre for the safe zone
        return (c + (x * u - c) * k, c + (y * u - c) * k)

    roof_w = (6.2 if bold else 3.6) * u * k
    bar_h = (5.2 if bold else 3.6) * u * k
    if bold:
        pts = [P(8, 24.5), P(24, 11), P(40, 24.5)]
        bars = [(13, 27.5), (13, 35.2)]
        bw = 22
    else:
        pts = [P(10, 23.5), P(24, 12), P(38, 23.5)]
        bars = [(15, 27), (15, 33.6)]
        bw = 18
    d.line(pts, fill=COPPER_LIGHT, width=int(roof_w), joint="curve")
    for p in (pts[0], pts[-1]):
        r = roof_w / 2
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=COPPER_LIGHT)
    for x, y in bars:
        a, b = P(x, y), P(x + bw, y)
        d.rounded_rectangle([a[0], a[1], b[0], a[1] + bar_h], radius=bar_h / 2, fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def font(path, size, fallback="DejaVuSerif-Bold.ttf"):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{fallback}", size)


def og_image(display, text):
    W, H = 1200, 630
    src = Image.open(os.path.join(ST, "assets/img/photos/hero-home.webp")).convert("RGB")
    sw, sh = src.size
    scale = max(W / sw, H / sh)
    src = src.resize((int(sw * scale) + 1, int(sh * scale) + 1), Image.LANCZOS)
    x = (src.width - W) // 2
    y = (src.height - H) // 2
    im = src.crop((x, y, x + W, y + H))
    # warm crimson-to-espresso overlay, heavier on the left for text
    ov = Image.new("RGBA", (W, H))
    od = ImageDraw.Draw(ov)
    for i in range(W):
        t = i / W
        a = int(235 - 150 * t)
        col = tuple(int(CRIMSON_DARK[j] * (1 - t) + 29 * t) for j in range(3))
        od.line([(i, 0), (i, H)], fill=col + (a,))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    d = ImageDraw.Draw(im)
    m = draw_mark(112)
    im.alpha_composite(m, (72, 72))
    d.text((72, 228), "California", font=font(display, 92), fill=WHITE)
    d.text((72, 330), "Insurance Appraiser", font=font(display, 92), fill=WHITE)
    d.rectangle([72, 452, 152, 456], fill=COPPER_LIGHT)
    d.text((72, 478), "Independent appraisal for disputed property claims", font=font(text, 34, "DejaVuSans-Bold.ttf"), fill=(244, 232, 222))
    d.text((72, 528), "All 58 counties  ·  +1 (844) 537-1427", font=font(text, 30, "DejaVuSans-Bold.ttf"), fill=COPPER_LIGHT)
    im.convert("RGB").save(os.path.join(ST, "assets/img/og-image.jpg"), "JPEG", quality=86, optimize=True, progressive=True)


def main():
    display = sys.argv[1] if len(sys.argv) > 1 else ""
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    os.makedirs(os.path.join(ST, "assets/img"), exist_ok=True)
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    open(os.path.join(ST, "assets/img/mark.svg"), "w").write(SVG)
    bold = draw_mark(256, bold=True)
    bold.save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    draw_mark(96).save(os.path.join(ST, "favicon-96x96.png"))
    draw_mark(180, full_bleed=True, safe=0.86).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    draw_mark(192, full_bleed=True, safe=0.72).save(os.path.join(ST, "favicon-192.png"))
    draw_mark(512, full_bleed=True, safe=0.72).save(os.path.join(ST, "favicon-512.png"))
    manifest = {
        "name": "California Insurance Appraiser", "short_name": "CA Appraiser", "start_url": "/", "display": "standalone",
        "theme_color": "#7d0820", "background_color": "#fbf7f2",
        "icons": [
            {"src": f"/favicon-192.png?v={FAV}", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": f"/favicon-512.png?v={FAV}", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
            {"src": f"/favicon-96x96.png?v={FAV}", "sizes": "96x96", "type": "image/png", "purpose": "any"},
            {"src": f"/favicon.svg?v={FAV}", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
        ],
    }
    json.dump(manifest, open(os.path.join(ST, "site.webmanifest"), "w"), indent=1)
    og_image(display, text)
    print("icons + og image written")


if __name__ == "__main__":
    main()
