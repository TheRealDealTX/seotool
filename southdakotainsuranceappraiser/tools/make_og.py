#!/usr/bin/env python3
"""1200x630 Open Graph image from the hero photo, with the brand mark and name."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "tools", ".cache", "hero-home.orig")
im = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert("RGB"), (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
ov = Image.new("RGBA", (1200, 630))
d = ImageDraw.Draw(ov)
for x in range(1200):
    a = int(235 * max(0, 1 - x / 900))
    d.line([(x, 0), (x, 630)], fill=(3, 32, 47, a))
im = Image.alpha_composite(im.convert("RGBA"), ov)
d = ImageDraw.Draw(im)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# mark
d.rounded_rectangle([70, 70, 166, 166], radius=22, fill=(0, 116, 168))
d.pieslice([96, 102, 140, 146], 180, 360, fill=(255, 196, 0))
d.rounded_rectangle([83, 121, 153, 127], radius=3, fill="white")
d.rounded_rectangle([91, 132, 145, 137], radius=3, fill=(159, 211, 234))
d.rounded_rectangle([101, 142, 135, 147], radius=3, fill=(159, 211, 234))
d.text((70, 215), "South Dakota", font=ImageFont.truetype(B, 74), fill="white")
d.text((70, 300), "Insurance Appraiser", font=ImageFont.truetype(B, 74), fill=(255, 196, 0))
d.text((72, 410), "Independent appraisal for underpaid", font=ImageFont.truetype(R, 34), fill=(220, 237, 245))
d.text((72, 454), "hail, wind, winter, fire and water claims", font=ImageFont.truetype(R, 34), fill=(220, 237, 245))
d.rectangle([0, 618, 1200, 630], fill=(255, 196, 0))
im.convert("RGB").save(os.path.join(ROOT, "static", "assets", "img", "og-image.jpg"), quality=86, optimize=True)
print("og-image written")
