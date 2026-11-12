#!/usr/bin/env python3
"""Generate favicon set + OG image for Arkansas Insurance Appraiser (Pillow only)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "static")
RED, DEEP, TEAL, WHITE = (143, 29, 36), (43, 7, 10), (79, 193, 185), (255, 255, 255)


def draw_mark(size, bold=False, bleed=False, safe=1.0):
    k = 8
    W = size * k
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if bleed:
        d.rectangle([0, 0, W, W], fill=RED)
    else:
        d.ellipse([0, 0, W - 1, W - 1], fill=RED)
    u = W / 48 * safe
    off = (W - 48 * u) / 2
    P = lambda x, y: (off + x * u, off + y * u)
    if not bold and not bleed:
        r = 20.5 * u
        d.ellipse([off + 24 * u - r, off + 24 * u - r, off + 24 * u + r, off + 24 * u + r], outline=(255, 255, 255, 60), width=max(1, int(1.5 * u)))
    sw = (5.2 if bold else 3.6) * u
    pts = [P(11.5, 23.5), P(24, 13), P(36.5, 23.5)] if not bold else [P(10, 24), P(24, 12), P(38, 24)]
    d.line(pts, fill=WHITE, width=int(sw), joint="curve")
    for p in (pts[0], pts[2]):
        d.ellipse([p[0] - sw / 2, p[1] - sw / 2, p[0] + sw / 2, p[1] + sw / 2], fill=WHITE)
    dia = [P(24, 22.5), P(30, 29), P(24, 36.5), P(18, 29)] if not bold else [P(24, 21.5), P(31.5, 29.5), P(24, 38), P(16.5, 29.5)]
    d.polygon(dia, fill=TEAL)
    return im.resize((size, size), Image.LANCZOS)


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="#8f1d24"/>'
       '<circle cx="24" cy="24" r="20.5" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="1.5"/>'
       '<path d="M11.5 23.5L24 13l12.5 10.5" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M24 22.5l6 6.5-6 7.5-6-7.5z" fill="#4fc1b9"/></svg>\n')

open(os.path.join(S, "favicon.svg"), "w").write(SVG)
os.makedirs(os.path.join(S, "assets/img"), exist_ok=True)
open(os.path.join(S, "assets/img/mark.svg"), "w").write(SVG)
ico = [draw_mark(n, bold=True) for n in (16, 32, 48)]
ico[2].save(os.path.join(S, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])
draw_mark(96).save(os.path.join(S, "favicon-96x96.png"))
draw_mark(180, bleed=True, safe=.78).convert("RGB").save(os.path.join(S, "apple-touch-icon.png"))
draw_mark(192, bleed=True, safe=.72).save(os.path.join(S, "favicon-192.png"))
draw_mark(512, bleed=True, safe=.72).save(os.path.join(S, "favicon-512.png"))
open(os.path.join(S, "site.webmanifest"), "w").write(
    '{"name":"Arkansas Insurance Appraiser","short_name":"AR Appraiser","start_url":"/","icons":['
    '{"src":"/favicon-192.png?v=1","sizes":"192x192","type":"image/png","purpose":"maskable"},'
    '{"src":"/favicon-512.png?v=1","sizes":"512x512","type":"image/png","purpose":"maskable"},'
    '{"src":"/favicon-96x96.png?v=1","sizes":"96x96","type":"image/png","purpose":"any"},'
    '{"src":"/favicon.svg?v=1","sizes":"any","type":"image/svg+xml","purpose":"any"}],'
    '"theme_color":"#8f1d24","background_color":"#fcfbf9","display":"standalone"}\n')

# OG image 1200x630 from a site photo
ph = Image.open(os.path.join(S, "assets/img/photos/house-dark-sky.webp")).convert("RGB")
r = max(1200 / ph.width, 630 / ph.height)
ph = ph.resize((round(ph.width * r), round(ph.height * r)), Image.LANCZOS)
x0, y0 = (ph.width - 1200) // 2, (ph.height - 630) // 2
og = ph.crop((x0, y0, x0 + 1200, y0 + 630))
ov = Image.new("RGBA", (1200, 630))
od = ImageDraw.Draw(ov)
for x in range(1200):
    a = int(235 - 175 * min(1, x / 1000))
    od.line([(x, 0), (x, 630)], fill=(43, 7, 10, a))
og = Image.alpha_composite(og.convert("RGBA"), ov)
d = ImageDraw.Draw(og)
font_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
fp = next((p for p in font_paths if os.path.exists(p)), None)
F = lambda s: ImageFont.truetype(fp, s) if fp else ImageFont.load_default()
fr = next((p for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"] if os.path.exists(p)), fp)
FR = lambda s: ImageFont.truetype(fr, s) if fr else ImageFont.load_default()
og.alpha_composite(draw_mark(112), (72, 86))
d.text((72, 236), "Arkansas", font=F(78), fill=WHITE)
d.text((72, 322), "Insurance Appraiser", font=F(66), fill=WHITE)
d.rectangle([72, 420, 150, 426], fill=TEAL)
d.text((72, 450), "Independent appraisal for underpaid property claims", font=FR(30), fill=(245, 225, 225))
d.text((72, 500), "All 75 counties  ·  +1 (844) 537-1427", font=F(30), fill=WHITE)
og.convert("RGB").save(os.path.join(S, "assets/img/og-image.jpg"), quality=86)
print("icons + og done")
