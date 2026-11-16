#!/usr/bin/env python3
"""Generate the favicon set, maskable PWA icons and the 1200x630 OG image into ../static.

python3 tools/make_icons.py   (needs Pillow; run from anywhere)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
GREEN, DEEP, GOLD, WHITE = (21, 71, 52), (11, 42, 31), (255, 204, 51), (255, 255, 255)
SS = 8  # supersampling

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#154734"/><rect x="3.5" y="3.5" width="41" height="41" rx="7.5" fill="none" stroke="#ffcc33" stroke-width="2"/><path d="M9 33l9.5-14 5 7 4-5.5L39 33z" fill="#ffcc33"/><path d="M18.5 19l2.6 3.8 2.4-1.6 1.4 2" fill="none" stroke="#154734" stroke-width="1.8" stroke-linejoin="round"/><path d="M10 38h28" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>
"""


def draw_mark(size, bold=False, bleed=False, content=1.0):
    """Draw the mark on a size x size canvas. bleed=True fills the square; content scales the artwork."""
    S = size * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = S / 48.0
    if bleed:
        d.rectangle([0, 0, S, S], fill=GREEN)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=10 * u, fill=GREEN)
    off = (1 - content) * 24

    def P(x, y):
        return (off * u + x * u * content, off * u + y * u * content)

    if bold:
        d.polygon([P(5, 35), P(17.5, 14), P(24, 24), P(29.5, 16.5), P(43, 35)], fill=GOLD)
        d.line([P(7, 41), P(41, 41)], fill=WHITE, width=int(4.4 * u * content))
    else:
        if not bleed:
            d.rounded_rectangle([3.5 * u, 3.5 * u, 44.5 * u, 44.5 * u], radius=7.5 * u, outline=GOLD, width=int(2 * u))
        d.polygon([P(9, 33), P(18.5, 19), P(23.5, 26), P(27.5, 20.5), P(39, 33)], fill=GOLD)
        d.line([P(18.5, 19), P(21.1, 22.8), P(23.5, 21.2), P(24.9, 23.2)], fill=GREEN, width=int(1.8 * u * content), joint="curve")
        lw = 2.6 * u * content
        d.line([P(10, 38), P(38, 38)], fill=WHITE, width=int(lw))
        for x in (10, 38):
            cx, cy = P(x, 38)
            d.ellipse([cx - lw / 2, cy - lw / 2, cx + lw / 2, cy + lw / 2], fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def main():
    with open(os.path.join(STATIC, "favicon.svg"), "w") as f:
        f.write(SVG)
    small = [draw_mark(s, bold=True) for s in (16, 32, 48)]
    small[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=small[:2])
    draw_mark(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw_mark(180, bleed=True, content=0.86).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for s in (192, 512):
        draw_mark(s, bleed=True, content=0.66).save(os.path.join(STATIC, f"favicon-{s}.png"))
    with open(os.path.join(STATIC, "site.webmanifest"), "w") as f:
        f.write('{\n  "name": "Vermont Insurance Appraiser",\n  "short_name": "VT Appraiser",\n  "start_url": "/",\n  "display": "standalone",\n'
                '  "background_color": "#fbfaf5",\n  "theme_color": "#154734",\n  "icons": [\n'
                '    {"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},\n'
                '    {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}\n  ]\n}\n')

    # OG image from a site photo
    photo = Image.open(os.path.join(STATIC, "assets", "img", "photos", "farmhouse-snow.webp")).convert("RGB")
    w, h = photo.size
    top = max(0, (h - 630) // 2)
    og = photo.crop((0, top, 1200, top + 630)).copy()
    shade = Image.new("RGBA", (1200, 630))
    sd = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(235 * max(0.0, 1 - x / 900)) if x < 900 else 0
        sd.line([(x, 0), (x, 630)], fill=(7, 28, 20, a))
    og = Image.alpha_composite(og.convert("RGBA"), shade)
    d = ImageDraw.Draw(og)
    d.rectangle([0, 0, 1200, 10], fill=GOLD)
    og.alpha_composite(draw_mark(120), (72, 120))
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.text((72, 280), "Vermont Insurance", font=ImageFont.truetype(serif, 66), fill=WHITE)
    d.text((72, 356), "Appraiser", font=ImageFont.truetype(serif, 66), fill=GOLD)
    d.text((72, 460), "Independent appraisal for disputed property claims", font=ImageFont.truetype(sans, 30), fill=(225, 237, 230))
    d.text((72, 506), "All 14 Vermont counties  ·  (844) 537-1427", font=ImageFont.truetype(sans, 28), fill=(225, 237, 230))
    og.convert("RGB").save(os.path.join(STATIC, "assets", "img", "og-image.jpg"), quality=86)
    print("icons and OG image written")


if __name__ == "__main__":
    main()
