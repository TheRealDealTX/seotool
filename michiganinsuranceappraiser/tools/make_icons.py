#!/usr/bin/env python3
"""Generate the favicon set, apple-touch icon, maskable PWA icons and the OG image into ../static.
Run after changing the mark or the hero photo:  python3 tools/make_icons.py
The mark: twin roof peaks forming an "M" (maize) over an estimate line (white) on a Michigan-blue tile."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
BLUE, MAIZE, WHITE = (0, 39, 76), (255, 203, 5), (255, 255, 255)
V = "1"


def poly(d, pts, w, fill):
    d.line(pts, fill=fill, width=int(w), joint="curve")
    r = w / 2
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw_mark(size, bold=False, rounded=True, scale=1.0):
    """Render the 48-unit mark at `size` px. bold=True thickens strokes for 16-48px; scale<1 insets it in a full-bleed tile."""
    S = 8
    big = size * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 12 / 48), fill=BLUE)
    else:
        d.rectangle([0, 0, big, big], fill=BLUE)
    u = big / 48 * scale
    off = big * (1 - scale) / 2

    def P(pts):
        return [(off + x * u, off + y * u) for x, y in pts]
    if bold:
        poly(d, P([(9, 34), (9, 16), (16.5, 26.5), (24, 16), (31.5, 26.5), (39, 16), (39, 34)]), 6.4 * u, MAIZE)
        poly(d, P([(12, 40.5), (36, 40.5)]), 4.6 * u, WHITE)
    else:
        poly(d, P([(10, 33), (10, 17.5), (17, 27), (24, 17.5), (31, 27), (38, 17.5), (38, 33)]), 4.4 * u, MAIZE)
        poly(d, P([(13, 39.5), (35, 39.5)]), 3.2 * u, WHITE)
    return im.resize((size, size), Image.LANCZOS)


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#00274C"/>'
       '<path d="M10 33V17.5l7 9.5 7-9.5 7 9.5 7-9.5V33" fill="none" stroke="#FFCB05" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M13 39.5h22" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/></svg>\n')


def main():
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(STATIC, "assets", "img"), exist_ok=True)
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG)
    icos = [draw_mark(n, bold=True) for n in (16, 32, 48)]
    icos[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
    draw_mark(32, bold=True).save(os.path.join(STATIC, "favicon-32x32.png"))
    draw_mark(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw_mark(512).save(os.path.join(STATIC, "favicon-512.png"))
    draw_mark(180, rounded=False, scale=.8).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for n in (192, 512):
        draw_mark(n, rounded=False, scale=.66).convert("RGB").save(os.path.join(STATIC, f"icon-maskable-{n}.png"))
        draw_mark(n).save(os.path.join(STATIC, f"icon-{n}.png"))
    open(os.path.join(STATIC, "site.webmanifest"), "w").write(
        '{"name":"Michigan Insurance Appraiser","short_name":"MI Appraiser","start_url":"/","display":"standalone",'
        '"background_color":"#ffffff","theme_color":"#00274C","icons":['
        f'{{"src":"/icon-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-maskable-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/icon-maskable-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"maskable"}}]}}\n')
    # OG image 1200x630 from a site photo.
    src = Image.open(os.path.join(STATIC, "assets", "img", "photos", "mackinac-bridge.webp")).convert("RGB")
    w, h = src.size
    crop_h = int(w * 630 / 1200)
    top = max(0, (h - crop_h) // 2)
    og = src.crop((0, top, w, top + crop_h)).resize((1200, 630), Image.LANCZOS)
    shade = Image.new("RGBA", (1200, 630))
    sd = ImageDraw.Draw(shade)
    for x in range(1200):
        sd.line([(x, 0), (x, 630)], fill=(0, 24, 47, max(70, int(240 - 170 * (x / 1200)))))
    og = Image.alpha_composite(og.convert("RGBA"), shade)
    d = ImageDraw.Draw(og)
    og.alpha_composite(draw_mark(112), (70, 68))
    fb = os.path.join(HERE, "fonts", "SofiaSansCondensed-ExtraBold.ttf")
    fr = os.path.join(HERE, "fonts", "AtkinsonHyperlegible-Regular.ttf")
    d.text((70, 196), "MICHIGAN", font=ImageFont.truetype(fb, 120), fill=MAIZE)
    d.text((70, 318), "Insurance Appraiser", font=ImageFont.truetype(fb, 84), fill=WHITE)
    d.rectangle([70, 420, 190, 427], fill=MAIZE)
    d.text((70, 452), "Independent appraisal for underpaid property claims", font=ImageFont.truetype(fr, 31), fill=(220, 232, 244))
    d.text((70, 500), "Both peninsulas  ·  All 83 counties  ·  (844) 537-1427", font=ImageFont.truetype(fr, 28), fill=(185, 205, 228))
    og.convert("RGB").save(os.path.join(STATIC, "assets", "img", "og-image.jpg"), quality=86)


if __name__ == "__main__":
    main()
