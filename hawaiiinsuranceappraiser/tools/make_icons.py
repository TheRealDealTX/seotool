#!/usr/bin/env python3
"""Generate the favicon set, apple-touch icon, maskable PWA icons, manifest and OG image into ../static.
Run after changing the mark or the hero photo:  python3 tools/make_icons.py"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "..", "static")
TOP, BOT = (125, 79, 181), (42, 20, 66)      # gradient #7d4fb5 -> #2a1442 (brand #6B3FA0 in between)
SUN, WHITE = (242, 181, 68), (255, 255, 255)
V = "1"


def gradient(big):
    g = Image.new("RGB", (big, big))
    d = ImageDraw.Draw(g)
    for i in range(big * 2):
        t = i / (big * 2 - 1)
        c = tuple(int(TOP[k] + (BOT[k] - TOP[k]) * t) for k in range(3))
        d.line([(i, 0), (0, i)], fill=c)
    return g


def poly(d, pts, w, fill):
    d.line(pts, fill=fill, width=int(w), joint="curve")
    r = w / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def draw_mark(size, bold=False, rounded=True, scale=1.0):
    """Render the 48-unit mark at `size` px. bold=True for 16-48px favicons. scale<1 shrinks the glyph inside a full-bleed tile."""
    S = 8
    big = size * S
    tile = gradient(big).convert("RGBA")
    mask = Image.new("L", (big, big), 0)
    md = ImageDraw.Draw(mask)
    if rounded:
        md.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 12 / 48), fill=255)
    else:
        md.rectangle([0, 0, big, big], fill=255)
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    im.paste(tile, (0, 0), mask)
    d = ImageDraw.Draw(im)
    u = big / 48 * scale
    off = big * (1 - scale) / 2

    def P(x, y):
        return (off + x * u, off + y * u)
    if bold:
        poly(d, [P(9, 25.5), P(24, 11.5), P(39, 25.5)], 6.2 * u, WHITE)
        wave = [P(8 + i * 0.5, 36.5 - 3.2 * math.sin(i * 0.5 / 9.5 * 2 * math.pi)) for i in range(0, 65)]
        poly(d, wave, 5.2 * u, SUN)
    else:
        poly(d, [P(10.5, 24.5), P(24, 12.5), P(37.5, 24.5)], 4 * u, WHITE)
        poly(d, [P(17, 24), P(17, 30.5)], 3.2 * u, WHITE)
        poly(d, [P(31, 24), P(31, 30.5)], 3.2 * u, WHITE)
        wave = [P(9.5 + i * 0.5, 36.5 - 2.1 * math.sin(i * 0.5 / 9.5 * 2 * math.pi)) for i in range(0, 58)]
        poly(d, wave, 3.4 * u, SUN)
    return im.resize((size, size), Image.LANCZOS)


SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
       '<stop offset="0" stop-color="#7d4fb5"/><stop offset="1" stop-color="#2a1442"/></linearGradient></defs>'
       '<rect width="48" height="48" rx="12" fill="url(#g)"/>'
       '<path d="M10.5 24.5L24 12.5l13.5 12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M17 24v6.5M31 24v6.5" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
       '<path d="M9.5 36.5c3.2-2.8 6.3-2.8 9.5 0s6.3 2.8 9.5 0 6.3-2.8 9.5 0" fill="none" stroke="#f2b544" stroke-width="3.4" stroke-linecap="round"/></svg>\n')


def main():
    open(os.path.join(STATIC, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(STATIC, "assets", "img"), exist_ok=True)
    open(os.path.join(STATIC, "assets", "img", "mark.svg"), "w").write(SVG)
    icos = [draw_mark(n, bold=True) for n in (16, 32, 48)]
    icos[2].save(os.path.join(STATIC, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=icos[:2])
    draw_mark(96).save(os.path.join(STATIC, "favicon-96x96.png"))
    draw_mark(512).save(os.path.join(STATIC, "favicon-512.png"))
    draw_mark(180, rounded=False, scale=.8).convert("RGB").save(os.path.join(STATIC, "apple-touch-icon.png"))
    for n in (192, 512):
        draw_mark(n, rounded=False, scale=.64).convert("RGB").save(os.path.join(STATIC, f"icon-maskable-{n}.png"))
        draw_mark(n).save(os.path.join(STATIC, f"icon-{n}.png"))
    open(os.path.join(STATIC, "site.webmanifest"), "w").write(
        '{"name":"Hawaii Insurance Appraiser","short_name":"HI Appraiser","start_url":"/","display":"standalone",'
        '"background_color":"#ffffff","theme_color":"#6B3FA0","icons":['
        f'{{"src":"/icon-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"any"}},'
        f'{{"src":"/icon-maskable-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/icon-maskable-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"maskable"}}]}}\n')
    # OG image 1200x630 from the homepage hero photo.
    src = Image.open(os.path.join(STATIC, "assets", "img", "photos", "hero-island-homes.webp")).convert("RGB")
    w, h = src.size
    if w / h > 1200 / 630:
        cw = int(h * 1200 / 630)
        src = src.crop(((w - cw) // 2, 0, (w - cw) // 2 + cw, h))
    else:
        ch = int(w * 630 / 1200)
        src = src.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch))
    og = src.resize((1200, 630), Image.LANCZOS).convert("RGBA")
    shade = Image.new("RGBA", (1200, 630))
    sd = ImageDraw.Draw(shade)
    for x in range(1200):
        a = int(238 - 170 * (x / 1200))
        sd.line([(x, 0), (x, 630)], fill=(26, 11, 44, max(60, a)))
    og = Image.alpha_composite(og, shade)
    d = ImageDraw.Draw(og)
    og.alpha_composite(draw_mark(108), (70, 70))
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    fr = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    d.text((70, 226), "Hawaii", font=ImageFont.truetype(fb, 84), fill=WHITE)
    d.text((70, 318), "Insurance Appraiser", font=ImageFont.truetype(fb, 84), fill=WHITE)
    d.rectangle([70, 434, 176, 440], fill=SUN)
    d.text((70, 462), "Independent appraisal for underpaid property claims", font=ImageFont.truetype(fr, 31), fill=(230, 220, 243))
    d.text((70, 510), "Oahu · Hawaii Island · Maui · Kauai  ·  (844) 537-1427", font=ImageFont.truetype(fr, 28), fill=(205, 191, 226))
    og.convert("RGB").save(os.path.join(STATIC, "assets", "img", "og-image.jpg"), quality=86)


if __name__ == "__main__":
    main()
