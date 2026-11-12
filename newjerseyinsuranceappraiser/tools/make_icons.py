#!/usr/bin/env python3
"""Favicons, touch icon, maskable PWA icons, manifest and the 1200x630 OG image.
Run from the site folder after the photos exist:  python3 tools/make_icons.py [og-photo-key]
Needs Pillow."""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
INK, AMBER, CREAM = (42, 30, 8), (255, 202, 102), (255, 246, 227)
V = "1"

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="13" fill="#2a1e08"/><path d="M10.5 31a13.5 13.5 0 0 1 27 0" fill="none" stroke="#FFCA66" stroke-width="4.2" stroke-linecap="round"/><path d="M24 31l7.2-9" stroke="#fff6e3" stroke-width="3.6" stroke-linecap="round"/><circle cx="24" cy="31" r="3.4" fill="#FFCA66"/><path d="M14 37.5h20" stroke="#FFCA66" stroke-width="2.6" stroke-linecap="round" opacity=".55"/></svg>
"""


def draw_mark(size, bold=False, full_bleed=False, pad=0.0):
    """Appraisal dial: amber arc, cream needle, amber hub. `bold` thickens strokes for 16-48px."""
    S = size * 8
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, S, S], fill=INK)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 13 / 48), fill=INK)
    u = S / 48 * (1 - 2 * pad)
    o = S * pad
    P = lambda x, y: (o + x * u, o + y * u)
    k = 1.55 if bold else 1.0
    cx, cy, rad = 24, 31 if not bold else 30, 13.5 if not bold else 13
    arc_w = int(4.2 * u * k)
    pts = [P(cx - rad * math.cos(math.radians(a)), cy - rad * math.sin(math.radians(a))) for a in range(0, 181, 3)]
    d.line(pts, fill=AMBER, width=arc_w, joint="curve")
    for pt in (pts[0], pts[-1]):
        r = arc_w / 2
        d.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r], fill=AMBER)
    nw = int(3.6 * u * k)
    a, b = P(cx, cy), P(cx + 7.2, cy - 9)
    d.line([a, b], fill=CREAM, width=nw)
    r = nw / 2
    d.ellipse([b[0] - r, b[1] - r, b[0] + r, b[1] + r], fill=CREAM)
    hub = 3.4 * u * (1.25 if bold else 1)
    d.ellipse([a[0] - hub, a[1] - hub, a[0] + hub, a[1] + hub], fill=AMBER)
    if not bold:
        y = 37.5
        d.line([P(14, y), P(34, y)], fill=(170, 135, 70), width=int(2.6 * u))
    return im.resize((size, size), Image.LANCZOS)


def main():
    open(os.path.join(D, "favicon.svg"), "w").write(SVG)
    os.makedirs(os.path.join(D, "assets", "img"), exist_ok=True)
    open(os.path.join(D, "assets", "img", "mark.svg"), "w").write(SVG)
    small = [draw_mark(s, bold=True) for s in (16, 32, 48)]
    small[2].save(os.path.join(D, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=small[:2])
    draw_mark(96).save(os.path.join(D, "favicon-96x96.png"))
    draw_mark(180, full_bleed=True, pad=0.1).convert("RGB").save(os.path.join(D, "apple-touch-icon.png"))
    draw_mark(192, full_bleed=True, pad=0.16).save(os.path.join(D, "favicon-192.png"))
    draw_mark(512, full_bleed=True, pad=0.16).save(os.path.join(D, "favicon-512.png"))
    open(os.path.join(D, "site.webmanifest"), "w").write(
        '{"name":"New Jersey Insurance Appraiser","short_name":"NJ Appraiser","start_url":"/","icons":['
        f'{{"src":"/favicon-192.png?v={V}","sizes":"192x192","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/favicon-512.png?v={V}","sizes":"512x512","type":"image/png","purpose":"maskable"}},'
        f'{{"src":"/favicon-96x96.png?v={V}","sizes":"96x96","type":"image/png","purpose":"any"}},'
        f'{{"src":"/favicon.svg?v={V}","sizes":"any","type":"image/svg+xml","purpose":"any"}}],'
        '"theme_color":"#2a1e08","background_color":"#fbf9f4","display":"standalone"}\n')

    key = sys.argv[1] if len(sys.argv) > 1 else "hero-home"
    src = Image.open(os.path.join(D, "assets", "img", "photos", key + ".webp")).convert("RGB")
    W, H = 1200, 630
    s = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    x, y = (src.width - W) // 2, (src.height - H) // 2
    og = src.crop((x, y, x + W, y + H)).convert("RGBA")
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for i in range(W):
        sd.line([(i, 0), (i, H)], fill=(24, 17, 4, int(240 - 140 * i / W)))
    og = Image.alpha_composite(og, shade)
    og.alpha_composite(draw_mark(112), (72, 72))
    dr = ImageDraw.Draw(og)

    def font(names, size):
        for n in names:
            for base in ("/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/", "/usr/share/fonts/truetype/"):
                p = os.path.join(base, n)
                if os.path.exists(p):
                    return ImageFont.truetype(p, size)
        return ImageFont.load_default()
    bold = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
    reg = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    dr.text((72, 232), "New Jersey", font=font(bold, 70), fill=AMBER)
    dr.text((72, 312), "Insurance Appraiser", font=font(bold, 70), fill=(255, 255, 255))
    dr.rectangle([72, 414, 150, 420], fill=AMBER)
    dr.text((72, 446), "Independent appraisal for property claims that came up short", font=font(reg, 28), fill=(240, 232, 214))
    dr.text((72, 492), "All 21 counties  ·  (844) 537-1427", font=font(bold, 28), fill=AMBER)
    og.convert("RGB").save(os.path.join(D, "assets", "img", "og-image.jpg"), quality=86, optimize=True)
    print("icons, manifest and og-image.jpg written (OG photo:", key + ")")


if __name__ == "__main__":
    main()
