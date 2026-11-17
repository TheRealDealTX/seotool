#!/usr/bin/env python3
"""Favicon, logo and OG-image pipeline. Writes into static/.

    python3 assets.py

Mark: navy (#002D65) rounded tile, red (#CC0000) roofline, three white stars (a nod to the three
Grand Divisions on the state flag). Small sizes (16/32/48 .ico) use a bolder variant: thicker roof,
bigger stars. Outputs favicon.svg, favicon.ico (16/32/48), favicon-96x96.png, apple-touch-icon.png
(180, full-bleed), favicon-192.png / favicon-512.png (maskable, listed in site.webmanifest),
assets/img/mark.svg and assets/img/og-image.jpg (1200x630, built from a site photo).
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(ROOT, "static")
NAVY, RED, WHITE = (0, 45, 101), (204, 0, 0), (255, 255, 255)
FAV = "1"


def star_pts(cx, cy, r, k=0.45):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * k
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def svg(bold=False, full=False):
    rx = 0 if full else 11
    sw = 6 if bold else 4.6
    sr = 6.2 if bold else 4.6
    stars = [(24, 26 if bold else 25.2), (16.6 if bold else 17.6, 37 if bold else 35.4), (31.4 if bold else 30.4, 37 if bold else 35.4)]
    paths = "".join("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in star_pts(cx, cy, sr)) + "Z" for cx, cy in stars)
    roof = "M8 24.5 24 10.5l16 14" if bold else "M8.5 24.5 24 11l15.5 13.5"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="{rx}" fill="#002D65"/>'
            f'<path d="{roof}" fill="none" stroke="#CC0000" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{paths}" fill="#fff"/></svg>')


def raster(size, bold=False, full=False, pad=0.0):
    """Draw the mark at 4x then downsample. pad = fraction of inset for maskable safe zone."""
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full or pad:
        d.rectangle([0, 0, S, S], fill=NAVY)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 11 / 48, fill=NAVY)
    inner = S * (1 - 2 * pad)
    off = S * pad
    u = inner / 48
    P = lambda x, y: (off + x * u, off + y * u)
    sw = (6 if bold else 4.6) * u
    roof = [P(8, 24.5), P(24, 10.5), P(40, 24.5)] if bold else [P(8.5, 24.5), P(24, 11), P(39.5, 24.5)]
    d.line(roof, fill=RED, width=round(sw), joint="curve")
    for x, y in (roof[0], roof[2]):
        d.ellipse([x - sw / 2, y - sw / 2, x + sw / 2, y + sw / 2], fill=RED)
    sr = 6.2 if bold else 4.6
    stars = [(24, 26 if bold else 25.2), (16.6 if bold else 17.6, 37 if bold else 35.4), (31.4 if bold else 30.4, 37 if bold else 35.4)]
    for cx, cy in stars:
        d.polygon([P(x, y) for x, y in star_pts(cx, cy, sr)], fill=WHITE)
    return im.resize((size, size), Image.LANCZOS)


def og():
    photos = json.load(open(os.path.join(ROOT, "src", "photos.json")))
    key = "storm-sky"
    src = Image.open(os.path.join(ST, "assets", "img", "photos", f"{key}.webp")).convert("RGB")
    W, H = 1200, 630
    s = max(W / src.width, H / src.height)
    src = src.resize((math.ceil(src.width * s), math.ceil(src.height * s)), Image.LANCZOS)
    x, y = (src.width - W) // 2, (src.height - H) // 2
    im = src.crop((x, y, x + W, y + H))
    shade = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shade)
    for i in range(W):
        a = int(235 - 120 * (i / W))
        sd.line([(i, 0), (i, H)], fill=(0, 22, 52, a))
    im = Image.alpha_composite(im.convert("RGBA"), shade)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    mark = raster(132)
    im.alpha_composite(mark, (72, 96))

    def font(names, size):
        for n in names:
            for base in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype"):
                p = os.path.join(base, n)
                if os.path.exists(p):
                    return ImageFont.truetype(p, size)
        return ImageFont.load_default()
    serif_b = font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"], 74)
    sans = font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf"], 34)
    sans_b = font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"], 30)
    d.text((72, 270), "Tennessee", font=serif_b, fill=WHITE)
    d.text((72, 352), "Insurance Appraiser", font=serif_b, fill=WHITE)
    d.rectangle([72, 456, 168, 462], fill=RED)
    d.text((72, 484), "Independent appraisal for underpaid property claims", font=sans, fill=(220, 232, 247))
    d.text((72, 540), "All 95 counties  ·  (844) 537-1427", font=sans_b, fill=WHITE)
    im.convert("RGB").save(os.path.join(ST, "assets", "img", "og-image.jpg"), quality=86, optimize=True, progressive=True)
    return photos[key]


def main():
    os.makedirs(os.path.join(ST, "assets", "img"), exist_ok=True)
    open(os.path.join(ST, "favicon.svg"), "w").write(svg())
    open(os.path.join(ST, "assets", "img", "mark.svg"), "w").write(svg())
    bold = [raster(s, bold=True) for s in (16, 32, 48)]
    bold[2].save(os.path.join(ST, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=bold[:2])
    raster(96).save(os.path.join(ST, "favicon-96x96.png"))
    raster(180, full=True).convert("RGB").save(os.path.join(ST, "apple-touch-icon.png"))
    raster(192, pad=0.12).save(os.path.join(ST, "favicon-192.png"))
    raster(512, pad=0.12).save(os.path.join(ST, "favicon-512.png"))
    for old in ("favicon-32x32.png",):
        p = os.path.join(ST, old)
        if os.path.exists(p):
            os.remove(p)
    manifest = {"name": "Tennessee Insurance Appraiser", "short_name": "TN Appraiser", "start_url": "/", "display": "standalone",
                "theme_color": "#002D65", "background_color": "#FBFAF8",
                "icons": [{"src": f"/favicon-192.png?v={FAV}", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                          {"src": f"/favicon-512.png?v={FAV}", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
                          {"src": f"/favicon-96x96.png?v={FAV}", "sizes": "96x96", "type": "image/png", "purpose": "any"},
                          {"src": f"/favicon.svg?v={FAV}", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]}
    json.dump(manifest, open(os.path.join(ST, "site.webmanifest"), "w"), separators=(",", ":"))
    og()
    print("assets written")


if __name__ == "__main__":
    main()
