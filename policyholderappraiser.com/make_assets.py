#!/usr/bin/env python3
"""Generate the logo, favicons and Open Graph image into src/.

Run once (or whenever the mark changes); build.py copies src/ into public/.
Requires Pillow and ImageMagick's `convert` (for the .ico only).
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
IMG = os.path.join(SRC, "img")
os.makedirs(IMG, exist_ok=True)

NAVY = (15, 28, 43)
BRASS = (217, 169, 63)

# Balance-scale mark, drawn as paths so the same SVG works at 16px and in the header.
LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Policyholder Appraiser">
<rect width="64" height="64" rx="14" fill="#0f1c2b"/>
<g fill="none" stroke="#d9a93f" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
<path d="M32 14v34"/><path d="M24 48h16"/><path d="M14 22h36"/>
<path d="M14 22l-7 14h14z"/><path d="M50 22l-7 14h14z"/>
</g>
<circle cx="32" cy="14" r="3.2" fill="#d9a93f"/>
</svg>
"""

def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

write(os.path.join(SRC, "favicon.svg"), LOGO_SVG)
write(os.path.join(IMG, "logo-mark.svg"), LOGO_SVG)


def draw_mark(size, radius_ratio=14 / 64):
    """Rasterize the same mark with Pillow (no SVG rasterizer needed)."""
    s = size
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * radius_ratio), fill=NAVY)
    u = s / 64.0
    w = max(2, int(3.2 * u))
    def P(x, y):
        return (x * u, y * u)
    d.line([P(32, 14), P(32, 48)], fill=BRASS, width=w)
    d.line([P(24, 48), P(40, 48)], fill=BRASS, width=w)
    d.line([P(14, 22), P(50, 22)], fill=BRASS, width=w)
    for cx in (14, 50):
        d.line([P(cx, 22), P(cx - 7, 36), P(cx + 7, 36), P(cx, 22)], fill=BRASS, width=w, joint="curve")
    r = 3.2 * u
    d.ellipse([32 * u - r, 14 * u - r, 32 * u + r, 14 * u + r], fill=BRASS)
    return im

for size, name in [(96, "favicon-96x96.png"), (180, "apple-touch-icon.png"),
                   (192, "web-app-manifest-192x192.png"), (512, "web-app-manifest-512x512.png")]:
    draw_mark(size).save(os.path.join(SRC, name), optimize=True)

tmp = []
for s in (16, 32, 48):
    p = os.path.join(IMG, f"_fav{s}.png")
    draw_mark(s).save(p)
    tmp.append(p)
subprocess.run(["convert", *tmp, os.path.join(SRC, "favicon.ico")], check=True)
for p in tmp:
    os.remove(p)

# Open Graph image 1200x630
def font(size, bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

og = Image.new("RGBA", (1200, 630), NAVY + (255,))
glow = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(18, 0, -1):
    a = int(10 * (18 - i) / 18) + 2
    gd.ellipse([1200 - 60 - i * 28, -220 - i * 20, 1200 + 260 + i * 10, 300 + i * 12], fill=(217, 169, 63, a))
og = Image.alpha_composite(og, glow).convert("RGB")
d = ImageDraw.Draw(og)
mark = draw_mark(120)
og.paste(mark, (80, 80), mark)
d.text((220, 92), "POLICYHOLDER APPRAISER", font=font(34), fill=(255, 255, 255))
d.text((220, 140), "INDEPENDENT INSURANCE APPRAISERS  -  TEXAS", font=font(20, False), fill=BRASS)
d.text((80, 270), "Your appraiser in the", font=font(64), fill=(255, 255, 255))
d.text((80, 350), "insurance appraisal process.", font=font(64), fill=BRASS)
d.text((80, 470), "Competent. Independent. Disinterested in the outcome.", font=font(28, False), fill=(197, 208, 220))
d.text((80, 540), "policyholderappraiser.com   |   (832) 503-5866", font=font(26, False), fill=(197, 208, 220))
og.save(os.path.join(IMG, "og-image.png"), optimize=True)
print("assets written to", SRC)
