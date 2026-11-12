#!/usr/bin/env python3
"""Builds static/assets/img/og-image.jpg (1200x630) from the hero photo with a dark-blue overlay,
the brand mark and the site name. python3 tools/make_og.py (needs Pillow; run after tools/photos.py)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(HERE, "..", "static")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

im = Image.open(os.path.join(ST, "assets/img/photos/hero-home.webp")).convert("RGB")
W, H = 1200, 630
r = max(W / im.width, H / im.height)
im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
ov = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(ov)
for x in range(W):  # left-to-right navy fade
    a = int(235 - 150 * (x / W))
    d.line([(x, 0), (x, H)], fill=(8, 24, 50, max(70, a)))
im = Image.alpha_composite(im.convert("RGBA"), ov)
mark = Image.open(os.path.join(ST, "favicon-512.png")).convert("RGBA").resize((120, 120), Image.LANCZOS)
im.alpha_composite(mark, (70, 120))
d = ImageDraw.Draw(im)
d.line([(70, 286), (124, 286)], fill=(224, 154, 95), width=4)
d.text((140, 272), "INDEPENDENT CLAIM APPRAISAL · ALL 46 COUNTIES", font=ImageFont.truetype(SANS, 22), fill=(240, 201, 166))
f = ImageFont.truetype(SERIF, 66)
d.text((70, 320), "South Carolina", font=f, fill="white")
d.text((70, 398), "Insurance Appraiser", font=f, fill="white")
d.text((70, 500), "Appraisal · Estimate review · Umpire services   (844) 537-1427", font=ImageFont.truetype(SANS, 26), fill=(211, 222, 236))
im.convert("RGB").save(os.path.join(ST, "assets/img/og-image.jpg"), quality=86, optimize=True)
print("og-image.jpg written")
