#!/usr/bin/env python3
"""Builds the 1200x630 Open Graph image from a site photo: python3 tools/make_og.py (needs Pillow + DejaVu fonts)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "static", "assets", "img", "photos", "hero-home.webp")
OUT = os.path.join(HERE, "..", "static", "assets", "img", "og-image.jpg")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

im = Image.open(SRC).convert("RGB")
W, H = 1200, 630
s = max(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
ov = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(ov)
for x in range(W):  # navy gradient, strongest on the left
    a = int(240 - 150 * x / W)
    d.line([(x, 0), (x, H)], fill=(0, 15, 56, a))
im = Image.alpha_composite(im.convert("RGBA"), ov)
d = ImageDraw.Draw(im)
d.rectangle([0, H - 18, W, H], fill=(255, 234, 15))
# mark
d.rounded_rectangle([70, 80, 166, 176], radius=22, fill=(0, 42, 134))
k = 96 / 48
P = lambda pts: [(70 + x * k, 80 + y * k) for x, y in pts]
d.polygon(P([(7, 33.5), (18.5, 15), (24.5, 24.2), (28.7, 18.5), (41, 33.5)]), fill=(255, 234, 15))
d.rounded_rectangle([70 + 7 * k, 80 + 36.5 * k, 70 + 41 * k, 80 + 39.7 * k], radius=3, fill="white")
d.text((70, 220), "Oregon Insurance", font=ImageFont.truetype(SERIF, 74), fill="white")
d.text((70, 305), "Appraiser", font=ImageFont.truetype(SERIF, 74), fill=(255, 234, 15))
d.text((72, 420), "Independent appraisal for underpaid property claims", font=ImageFont.truetype(SANS, 32), fill=(225, 232, 250))
d.text((72, 470), "All 36 Oregon counties  ·  (844) 537-1427", font=ImageFont.truetype(SANS, 30), fill=(255, 234, 15))
im.convert("RGB").save(OUT, "JPEG", quality=85, optimize=True)
print("wrote", OUT)
