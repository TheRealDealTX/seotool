#!/usr/bin/env python3
"""Generate the favicon set, apple-touch icon, maskable PWA icons and the OG image into ../static.
Run after changing the mark or the hero photo:  python3 tools/make_icons.py

Mark: brand-navy tile, aspen-gold sun, twin white peaks. Small sizes (16/32/48) use a bolder,
simplified glyph (bigger sun, one broad peak) so it stays legible."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
NAVY, NAVY_D, GOLD, WHITE = (0, 40, 104), (0, 15, 43), (242, 169, 0), (255, 255, 255)
V = "1"


def draw_mark(size, bold=False, rounded=True, scale=1.0):
    """Render the 48-unit mark at `size` px. scale<1 shrinks the glyph inside a full-bleed tile."""
    S = 8
    big = size * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 12 / 48), fill=NAVY)
    else:
        d.rectangle([0, 0, big, big], fill=NAVY)
    u = big / 48 * scale
    off = big * (1 - scale) / 2

    def P(pts):
        return [(off + x * u, off + y * u) for x, y in pts]

    if bold:
        cx, cy, r = 32, 15, 8.5
        d.ellipse(P([(cx - r, cy - r), (cx + r, cy + r)]), fill=GOLD)
        d.polygon(P([(3, 41), (19, 15), (29, 29), (34, 23), (45, 41)]), fill=WHITE)
    else:
        cx, cy, r = 31.5, 16, 6.5
        d.ellipse(P([(cx - r, cy - r), (cx + r, cy + r)]), fill=GOLD)
        d.polygon(P([(5, 38), (17.5, 19), (24, 28.5), (29, 22), (43, 38)]), fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#002868"/>'
       '<circle cx="31.5" cy="16" r="6.5" fill="#F2A900"/>'
       '<path d="M5 38l12.5-19 6.5 9.5 5-6.5L43 38z" fill="#fff"/></svg>\n')


def main():
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(STATIC, "assets", "img"), exist_ok=True)
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG)
    icos = [draw_mark(n, bold=True) for n in (16, 32, 48)]
    icos[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
    draw_mark(32, bold=True).save(os.path.join(STATIC, "favicon-32x32.png"))
    draw_mark(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    # Full-bleed apple touch icon (iOS applies its own rounding).
    draw_mark(180, rounded=False, scale=.8).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for n in (192, 512):
        draw_mark(n).save(os.path.join(STATIC, f"icon-{n}.png"))
        # Maskable: glyph inside the 80% safe zone on a full-bleed tile.
        draw_mark(n, rounded=False, scale=.68).convert("RGB").save(os.path.join(STATIC, f"icon-maskable-{n}.png"))
    open(os.path.join(STATIC, "site.webmanifest"), "w").write(
        '{"name":"Colorado Insurance Appraiser","short_name":"CO Appraiser","start_url":"/","display":"standalone",'
        '"background_color":"#ffffff","theme_color":"#002868","icons":['
        f'{{"src":"/icon-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-maskable-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/icon-maskable-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/favicon.svg?v={V}","sizes":"any","type":"image/svg+xml"}}]}}\n')
    # OG image 1200x630 from the hero photo.
    src = Image.open(os.path.join(STATIC, "assets", "img", "photos", "hero.webp")).convert("RGB")
    w, h = src.size
    crop_h = int(w * 630 / 1200)
    top = max(0, (h - crop_h) // 2)
    og = src.crop((0, top, w, top + crop_h)).resize((1200, 630), Image.LANCZOS).convert("RGBA")
    shade = Image.new("RGBA", (1200, 630))
    sd = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(238 - 170 * (x / 1200))
        sd.line([(x, 0), (x, 630)], fill=NAVY_D + (max(60, a),))
    og = Image.alpha_composite(og, shade)
    # ridge silhouette along the bottom
    rd = ImageDraw.Draw(og)
    pts = [(0, 630), (0, 600), (110, 576), (170, 594), (300, 554), (390, 590), (450, 577), (570, 607), (720, 558), (800, 585), (890, 569), (1020, 604), (1130, 577), (1200, 590), (1200, 630)]
    rd.polygon(pts, fill=GOLD + (255,))
    og.alpha_composite(draw_mark(112), (70, 66))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    rd.text((70, 222), "Colorado", font=ImageFont.truetype(fb, 84), fill=WHITE)
    rd.text((70, 316), "Insurance Appraiser", font=ImageFont.truetype(fb, 70), fill=WHITE)
    rd.rectangle([70, 418, 180, 424], fill=GOLD)
    rd.text((70, 446), "Independent appraisal for hail, wildfire & storm claims", font=ImageFont.truetype(fr, 30), fill=(222, 231, 247))
    rd.text((70, 494), "All 64 counties  ·  (844) 537-1427", font=ImageFont.truetype(fr, 28), fill=(255, 211, 107))
    og.convert("RGB").save(os.path.join(STATIC, "assets", "img", "og-image.jpg"), quality=86)
    print("icons + og written")


if __name__ == "__main__":
    main()
