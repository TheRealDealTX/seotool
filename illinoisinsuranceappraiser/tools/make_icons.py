#!/usr/bin/env python3
"""Generate favicon/app icons and the OG image into static/. Run: python3 tools/make_icons.py"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, "static")
ORANGE, DEEP, WHITE = (255, 95, 15), (43, 17, 5), (255, 255, 255)

def draw_mark(size, bold=False, full_bleed=False, content=1.0):
    k = 8  # supersample
    W = size * k
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, W, W], fill=ORANGE)
    else:
        d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 11 / 48), fill=ORANGE)
    u = W / 48 * content
    off = (W - 48 * u) / 2
    P = lambda x, y: (off + x * u, off + y * u)
    rw, bw = (6.6, 6.0) if bold else (4.4, 4.0)
    roof = [P(9.5, 24.5), P(24, 12), P(38.5, 24.5)] if not bold else [P(8, 25), P(24, 11), P(40, 25)]
    def line(pts, w, col):
        w = int(w * u)
        d.line(pts, fill=col, width=w, joint="curve")
        for p in (pts[0], pts[-1]):
            d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)
    line(roof, rw, WHITE)
    if bold:
        line([P(14.5, 33), P(33.5, 33)], bw, DEEP)
        line([P(14.5, 40.5), P(26, 40.5)], bw, DEEP)
    else:
        line([P(15.5, 31), P(32.5, 31)], bw, DEEP)
        line([P(15.5, 37.5), P(25.5, 37.5)], bw, DEEP)
    return im.resize((size, size), Image.LANCZOS)

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#ff5f0f"/>'
       '<path d="M9.5 24.5L24 12l14.5 12.5" fill="none" stroke="#fff" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M15.5 31h17M15.5 37.5h10" fill="none" stroke="#2b1105" stroke-width="4" stroke-linecap="round"/></svg>\n')
open(os.path.join(S, "favicon.svg"), "w").write(svg)
os.makedirs(os.path.join(S, "assets/img"), exist_ok=True)
open(os.path.join(S, "assets/img/mark.svg"), "w").write(svg)
icos = [draw_mark(n, bold=True) for n in (16, 32, 48)]
icos[2].save(os.path.join(S, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
draw_mark(96, bold=True).save(os.path.join(S, "favicon-96x96.png"))
draw_mark(180, full_bleed=True, content=.82).convert("RGB").save(os.path.join(S, "apple-touch-icon.png"))
draw_mark(192, full_bleed=True, content=.64).save(os.path.join(S, "favicon-192.png"))
draw_mark(512, full_bleed=True, content=.64).save(os.path.join(S, "favicon-512.png"))
open(os.path.join(S, "site.webmanifest"), "w").write("""{
  "name": "Illinois Insurance Appraiser",
  "short_name": "IL Appraiser",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#ff5f0f",
  "icons": [
    {"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
    {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
""")

# OG image: site photo + brand overlay
ph = Image.open(os.path.join(S, "assets/img/photos/chicago-lakefront-aerial.webp")).convert("RGB")
w, h = ph.size
tw, th = 1200, 630
scale = max(tw / w, th / h)
ph = ph.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
x, y = (ph.width - tw) // 2, (ph.height - th) // 2
og = ph.crop((x, y, x + tw, y + th))
ov = Image.new("RGBA", (tw, th))
od = ImageDraw.Draw(ov)
for i in range(tw):
    a = int(235 - 150 * i / tw)
    od.line([(i, 0), (i, th)], fill=(27, 10, 3, a))
og = Image.alpha_composite(og.convert("RGBA"), ov)
d = ImageDraw.Draw(og)
def font(names, size):
    for n in names:
        try: return ImageFont.truetype(n, size)
        except OSError: pass
    return ImageFont.load_default()
bold = [os.path.join(ROOT, "tools/fonts/BigShouldersDisplay-Black.ttf"), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
reg = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
m = draw_mark(120)
og.alpha_composite(m, (80, 110))
d.text((80, 250), "ILLINOIS", font=font(bold, 132), fill=WHITE)
d.text((80, 385), "INSURANCE APPRAISER", font=font(bold, 78), fill=ORANGE)
d.text((80, 470), "Independent appraisal for underpaid property claims", font=font(reg, 30), fill=(255, 235, 222))
d.text((80, 520), "(844) 537-1427  ·  All 102 Illinois counties", font=font(reg, 28), fill=(255, 235, 222))
d.rectangle([0, th - 12, tw, th], fill=ORANGE)
og.convert("RGB").save(os.path.join(S, "assets/img/og-image.jpg"), quality=86, optimize=True)
print("icons + og image written")
