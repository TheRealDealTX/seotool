#!/usr/bin/env python3
"""Generate favicon set, apple-touch icon, maskable PWA icons and the OG image into ../static.
Run once after changing the mark:  python3 tools/make_icons.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
BLUE, CORAL, WHITE = (31, 100, 229), (255, 107, 87), (255, 255, 255)


def stroke(d, pts, w, fill, s):
    pts = [(x * s, y * s) for x, y in pts]
    d.line(pts, fill=fill, width=int(w * s), joint="curve")
    r = w * s / 2
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw_mark(size, bold=False, rounded=True, scale=1.0):
    """Render the 48-unit mark at `size` px. scale<1 shrinks the glyph inside a full-bleed tile."""
    S = 8
    big = size * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 11 / 48), fill=BLUE)
    else:
        d.rectangle([0, 0, big, big], fill=BLUE)
    u = big / 48 * scale
    off = big * (1 - scale) / 2
    s = 1
    def P(pts):
        return [(off + x * u, off + y * u) for x, y in pts]
    if bold:
        stroke(d, P([(9, 25), (24, 11.5), (39, 25)]), 6.4 * u, WHITE, s)
        stroke(d, P([(14, 32.5), (34, 32.5)]), 5.6 * u, WHITE, s)
        stroke(d, P([(14, 40), (26, 40)]), 5.6 * u, CORAL, s)
    else:
        stroke(d, P([(10, 23.5), (24, 12), (38, 23.5)]), 4 * u, WHITE, s)
        stroke(d, P([(15, 30), (33, 30)]), 3.6 * u, WHITE, s)
        stroke(d, P([(15, 37), (26, 37)]), 3.6 * u, CORAL, s)
    return im.resize((size, size), Image.LANCZOS)


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="#1F64E5"/>'
       '<path d="M10 23.5L24 12l14 11.5" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M15 30h18" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>'
       '<path d="M15 37h11" stroke="#FF6B57" stroke-width="3.6" stroke-linecap="round"/></svg>\n')


def main():
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(STATIC, "assets", "img"), exist_ok=True)
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG)
    # Multi-size ICO with the bolder glyph for 16/32/48.
    icos = [draw_mark(n, bold=True) for n in (16, 32, 48)]
    icos[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
    draw_mark(32, bold=True).save(os.path.join(STATIC, "favicon-32x32.png"))
    draw_mark(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw_mark(512).save(os.path.join(STATIC, "favicon-512.png"))
    # Full-bleed apple touch icon (iOS applies its own rounding).
    draw_mark(180, rounded=False, scale=.78).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    # Maskable icons: glyph inside the 80% safe zone.
    for n in (192, 512):
        draw_mark(n, rounded=False, scale=.66).convert("RGB").save(os.path.join(STATIC, f"icon-maskable-{n}.png"))
        draw_mark(n).save(os.path.join(STATIC, f"icon-{n}.png"))
    open(os.path.join(STATIC, "site.webmanifest"), "w").write(
        '{"name":"Connecticut Insurance Appraiser","short_name":"CT Appraiser","start_url":"/","display":"standalone",'
        '"background_color":"#ffffff","theme_color":"#1F64E5","icons":['
        '{"src":"/icon-192.png?v=1","sizes":"192x192","type":"image/png","purpose":"any"},'
        '{"src":"/icon-512.png?v=1","sizes":"512x512","type":"image/png","purpose":"any"},'
        '{"src":"/icon-maskable-192.png?v=1","sizes":"192x192","type":"image/png","purpose":"maskable"},'
        '{"src":"/icon-maskable-512.png?v=1","sizes":"512x512","type":"image/png","purpose":"maskable"}]}\n')
    # OG image 1200x630 from the hero photo.
    src = Image.open(os.path.join(STATIC, "assets", "img", "photos", "hero-saltbox.webp")).convert("RGB")
    w, h = src.size
    crop_h = int(w * 630 / 1200)
    top = max(0, (h - crop_h) // 2 - 40)
    og = src.crop((0, top, w, top + crop_h)).resize((1200, 630), Image.LANCZOS)
    shade = Image.new("RGBA", (1200, 630))
    sd = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(235 - 175 * (x / 1200))
        sd.line([(x, 0), (x, 630)], fill=(8, 24, 61, max(40, a)))
    og = Image.alpha_composite(og.convert("RGBA"), shade)
    d = ImageDraw.Draw(og)
    og.alpha_composite(draw_mark(110), (70, 70))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.text((70, 230), "Connecticut", font=ImageFont.truetype(fb, 78), fill=WHITE)
    d.text((70, 318), "Insurance Appraiser", font=ImageFont.truetype(fb, 78), fill=WHITE)
    d.rectangle([70, 428, 170, 434], fill=CORAL)
    d.text((70, 456), "Independent appraisal for underpaid property claims", font=ImageFont.truetype(fr, 32), fill=(219, 230, 252))
    d.text((70, 506), "All 169 towns  ·  (844) 537-1427", font=ImageFont.truetype(fr, 30), fill=(185, 205, 247))
    og.convert("RGB").save(os.path.join(STATIC, "assets", "img", "og-image.jpg"), quality=86)


if __name__ == "__main__":
    main()
