#!/usr/bin/env python3
"""Favicon + OG image pipeline. Writes into ../static. Run after photos exist: python3 tools/make_icons.py"""
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ST = os.path.join(ROOT, "static")
NAVY, GOLD, WHITE, INK = (0, 42, 134), (255, 209, 43), (255, 255, 255), (0, 26, 84)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#002A86"/><path d="M10 27.5L24 15l14 12.5" fill="none" stroke="#FFD12B" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 35h30" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><circle cx="35.5" cy="12.5" r="3.2" fill="#FFD12B"/></svg>
"""


def draw_mark(size, bold=False, full_bleed=False, pad=0.0):
    """Draw the mark at 4x then downsample. bold=True: thicker roof, no sun, for 16-48px."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=NAVY)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 10 / 48), fill=NAVY)
    inset = pad * S
    k = (S - 2 * inset) / 48.0

    def P(x, y):
        return (inset + x * k, inset + y * k)

    if bold:
        w = int(7.2 * k)
        pts = [P(9, 29), P(24, 14.5), P(39, 29)]
        d.line(pts, fill=GOLD, width=w, joint="curve")
        for x, y in (pts[0], pts[2]):
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=GOLD)
        hw = int(5 * k)
        d.line([P(9, 37), P(39, 37)], fill=WHITE, width=hw)
        for x, y in (P(9, 37), P(39, 37)):
            d.ellipse([x - hw / 2, y - hw / 2, x + hw / 2, y + hw / 2], fill=WHITE)
    else:
        w = int(4.4 * k)
        pts = [P(10, 27.5), P(24, 15), P(38, 27.5)]
        d.line(pts, fill=GOLD, width=w, joint="curve")
        for x, y in (pts[0], pts[2]):
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=GOLD)
        hw = int(3.2 * k)
        d.line([P(9, 35), P(39, 35)], fill=WHITE, width=hw)
        for x, y in (P(9, 35), P(39, 35)):
            d.ellipse([x - hw / 2, y - hw / 2, x + hw / 2, y + hw / 2], fill=WHITE)
        cx, cy = P(35.5, 12.5)
        r = 3.2 * k
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


def main():
    open(os.path.join(ST, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(ST, "assets/img"), exist_ok=True)
    open(os.path.join(ST, "assets/img/mark.svg"), "w").write(SVG)
    # multi-size ICO from the bold variant
    icos = [draw_mark(s, bold=True) for s in (16, 32, 48)]
    icos[2].save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
    draw_mark(32, bold=True).save(os.path.join(ST, "favicon-32x32.png"))
    draw_mark(96).save(os.path.join(ST, "favicon-96x96.png"))
    # apple-touch-icon: full bleed, no transparency
    draw_mark(180, full_bleed=True, pad=0.1).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    # maskable icons: full bleed with safe-zone padding
    for s in (192, 512):
        draw_mark(s, full_bleed=True, pad=0.16).convert("RGB").save(os.path.join(ST, f"favicon-{s}.png"))
    json.dump({
        "name": "North Dakota Insurance Appraiser", "short_name": "ND Appraiser",
        "icons": [
            {"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
            {"src": "/favicon-96x96.png?v=1", "sizes": "96x96", "type": "image/png", "purpose": "any"},
        ],
        "theme_color": "#002A86", "background_color": "#ffffff", "display": "standalone", "start_url": "/",
    }, open(os.path.join(ST, "site.webmanifest"), "w"), indent=2)

    # OG image 1200x630 from a site photo
    src = Image.open(os.path.join(ST, "assets/img/photos/barn-rural.webp")).convert("RGB")
    W, H = 1200, 630
    scale = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * scale) + 1, int(src.height * scale) + 1), Image.LANCZOS)
    left, top = (src.width - W) // 2, (src.height - H) // 2
    og = src.crop((left, top, left + W, top + H))
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for x in range(W):
        a = int(235 - 150 * (x / W))
        sd.line([(x, 0), (x, H)], fill=(0, 17, 58, max(60, a)))
    og = Image.alpha_composite(og.convert("RGBA"), shade)
    d = ImageDraw.Draw(og)
    fonts = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
    fpath = next((f for f in fonts if os.path.exists(f)), None)
    big = ImageFont.truetype(fpath, 64) if fpath else ImageFont.load_default()
    mid = ImageFont.truetype(fpath, 30) if fpath else ImageFont.load_default()
    m = draw_mark(120)
    og.alpha_composite(m, (80, 110))
    d.text((80, 270), "North Dakota", font=big, fill=WHITE)
    d.text((80, 345), "Insurance Appraiser", font=big, fill=GOLD)
    d.rectangle([80, 440, 200, 448], fill=GOLD)
    d.text((80, 470), "Independent appraisal for underpaid property claims", font=mid, fill=WHITE)
    d.text((80, 515), "(844) 537-1427  ·  All 53 counties", font=mid, fill=(220, 228, 245))
    og.convert("RGB").save(os.path.join(ST, "assets/img/og-image.jpg"), quality=86)
    print("icons + og written")


if __name__ == "__main__":
    main()
