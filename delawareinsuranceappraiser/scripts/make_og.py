#!/usr/bin/env python3
"""Build the 1200x630 Open Graph JPG from a site photo: python3 scripts/make_og.py [photo-key]"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key = sys.argv[1] if len(sys.argv) > 1 else "hero-coastal-home"
src = Image.open(os.path.join(ROOT, "static/assets/img/photos", key + ".webp")).convert("RGB")
W, H = 1200, 630
s = max(W / src.width, H / src.height)
src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
x, y = (src.width - W) // 2, (src.height - H) // 2
im = src.crop((x, y, x + W, y + H))
# slate gradient overlay, strongest on the left
ov = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(ov)
for i in range(W):
    a = int(235 - 150 * (i / W))
    d.line([(i, 0), (i, H)], fill=(20, 37, 48, a))
im = Image.alpha_composite(im.convert("RGBA"), ov)
d = ImageDraw.Draw(im)


def font(names, size):
    for n in names:
        for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/", "/usr/share/fonts/truetype/"):
            p = os.path.join(base, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


bold = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
reg = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
# mark
m = 96
d.rounded_rectangle([72, 120, 72 + m, 120 + m], radius=22, fill=(35, 61, 77), outline=(255, 255, 255, 90), width=2)
k = m / 48
L = lambda pts, w, c: d.line([(72 + a * k, 120 + b * k) for a, b in pts], fill=c, width=int(w * k), joint="curve")
L([(11, 25.5), (24, 13.5), (37, 25.5)], 3.6, (255, 255, 255))
L([(16.5, 23.5), (16.5, 34), (31.5, 34), (31.5, 23.5)], 3.0, (255, 255, 255))
L([(12, 38.5), (36, 38.5)], 3.6, (240, 121, 91))
d.text((72, 255), "Delaware Insurance", font=font(bold, 66), fill=(255, 255, 255))
d.text((72, 330), "Appraiser", font=font(bold, 66), fill=(255, 255, 255))
d.rectangle([72, 425, 132, 430], fill=(240, 121, 91))
d.text((72, 450), "Independent appraisal for underpaid property claims", font=font(reg, 30), fill=(230, 238, 242))
d.text((72, 495), "New Castle · Kent · Sussex   |   (844) 537-1427", font=font(reg, 26), fill=(249, 184, 166))
im.convert("RGB").save(os.path.join(ROOT, "static/assets/img/og-image.jpg"), quality=86, optimize=True)
print("og-image.jpg written from", key)
