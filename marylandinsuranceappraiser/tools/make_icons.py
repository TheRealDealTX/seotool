#!/usr/bin/env python3
"""Favicons, touch icon, maskable PWA icons and the OG image. Run from the site folder: python3 tools/make_icons.py"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
OLIVE, BRASS, PARCH, BLUE = (46, 41, 16), (217, 194, 122), (245, 242, 230), (140, 186, 214)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#2E2910"/><path d="M10.5 24.5L24 12.5l13.5 12" fill="none" stroke="#d9c27a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 23.5v8.5h16v-8.5" fill="none" stroke="#f5f2e6" stroke-width="3.2" stroke-linejoin="round"/><path d="M9.5 38.5c3.2-2.4 6-2.4 9.2 0s6 2.4 9.2 0 6-2.4 9.2 0" fill="none" stroke="#8cbad6" stroke-width="3" stroke-linecap="round"/></svg>
"""


def draw_mark(size, bold=False, full_bleed=False, pad=0.0):
    S = size * 8  # supersample
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=OLIVE)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 11 / 48), fill=OLIVE)
    inner = 1 - 2 * pad
    u = S / 48 * inner
    o = S * pad
    P = lambda x, y: (o + x * u, o + y * u)
    k = 1.45 if bold else 1.0
    roof_w, body_w, wave_w = int(4 * u * k), int(3.2 * u * k), int(3 * u * k)
    d.line([P(10.5, 24.5), P(24, 12.5), P(37.5, 24.5)], fill=BRASS, width=roof_w, joint="curve")
    for pt in (P(10.5, 24.5), P(37.5, 24.5), P(24, 12.5)):
        r = roof_w / 2
        d.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill=BRASS)
    d.line([P(16, 23.5), P(16, 32), P(32, 32), P(32, 23.5)], fill=PARCH, width=body_w, joint="curve")
    # wave
    import math
    pts = [P(9.5 + t * 27.6 / 60, 38.5 - 1.8 * math.sin(t / 60 * 3 * math.pi)) for t in range(61)]
    if bold:
        pts = [P(9.5 + t * 27.6 / 60, 38.8 - 1.6 * math.sin(t / 60 * 2 * math.pi)) for t in range(61)]
    d.line(pts, fill=BLUE, width=wave_w, joint="curve")
    for pt in (pts[0], pts[-1]):
        r = wave_w / 2
        d.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill=BLUE)
    return im.resize((size, size), Image.LANCZOS)


open(os.path.join(D, "favicon.svg"), "w").write(SVG)
os.makedirs(os.path.join(D, "assets", "img"), exist_ok=True)
open(os.path.join(D, "assets", "img", "mark.svg"), "w").write(SVG)
small = [draw_mark(s, bold=True) for s in (16, 32, 48)]
small[2].save(os.path.join(D, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=small[:2])
draw_mark(96).save(os.path.join(D, "favicon-96x96.png"))
draw_mark(180, full_bleed=True, pad=0.1).convert("RGB").save(os.path.join(D, "apple-touch-icon.png"))
draw_mark(192, full_bleed=True, pad=0.16).save(os.path.join(D, "favicon-192.png"))
draw_mark(512, full_bleed=True, pad=0.16).save(os.path.join(D, "favicon-512.png"))
open(os.path.join(D, "site.webmanifest"), "w").write(
    '{"name":"Maryland Insurance Appraiser","short_name":"MD Appraiser","start_url":"/","icons":['
    '{"src":"/favicon-192.png?v=1","sizes":"192x192","type":"image/png","purpose":"maskable"},'
    '{"src":"/favicon-512.png?v=1","sizes":"512x512","type":"image/png","purpose":"maskable"},'
    '{"src":"/favicon-96x96.png?v=1","sizes":"96x96","type":"image/png","purpose":"any"},'
    '{"src":"/favicon.svg?v=1","sizes":"any","type":"image/svg+xml","purpose":"any"}],'
    '"theme_color":"#2E2910","background_color":"#fcfbf6","display":"standalone"}\n')

# OG image 1200x630 from a site photo
src = Image.open(os.path.join(D, "assets", "img", "photos", "hero-home.webp")).convert("RGB")
w, h = src.size
scale = max(1200 / w, 630 / h)
src = src.resize((int(w * scale) + 1, int(h * scale) + 1), Image.LANCZOS)
x, y = (src.size[0] - 1200) // 2, (src.size[1] - 630) // 2
og = src.crop((x, y, x + 1200, y + 630))
shade = Image.new("RGBA", (1200, 630))
sd = ImageDraw.Draw(shade)
for i in range(1200):
    a = int(235 - 150 * i / 1200)
    sd.line([(i, 0), (i, 630)], fill=(26, 23, 8, a))
og = Image.alpha_composite(og.convert("RGBA"), shade)
og.alpha_composite(draw_mark(120), (70, 70))
dr = ImageDraw.Draw(og)
def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()
serif = font(["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", "DejaVuSerif.ttf"], 74)
sans = font(["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "DejaVuSans-Bold.ttf"], 30)
dr.text((70, 250), "Maryland", font=serif, fill=PARCH)
dr.text((70, 335), "Insurance Appraiser", font=serif, fill=PARCH)
dr.text((72, 450), "Independent appraisal for underpaid property claims", font=sans, fill=BRASS)
dr.text((72, 500), "(844) 537-1427  ·  All 23 counties & Baltimore City", font=sans, fill=(220, 230, 236))
og.convert("RGB").save(os.path.join(D, "assets", "img", "og-image.jpg"), quality=86)
print("icons + og done")
