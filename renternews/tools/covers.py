#!/usr/bin/env python3
"""Draw original cover art for new articles (and the default share image).

Each cover is a 1200x675 WebP: a category-colored gradient sky over an
apartment skyline with lit windows, plus a category accent (flames, a rising
chart line, a shield...). Deterministic per slug, no text baked in, so no
photo licensing is involved.

    python3 tools/covers.py          # only draws missing covers
    python3 tools/covers.py --force  # redraws all
"""
import hashlib
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
W, H = 1200, 675

PALETTES = {
    "fire":           ((40, 12, 30), (190, 60, 30), (255, 170, 60)),
    "safety":         ((30, 22, 50), (200, 110, 20), (255, 200, 90)),
    "rent-prices":    ((6, 40, 52), (15, 140, 125), (150, 240, 210)),
    "housing-policy": ((24, 22, 70), (91, 95, 199), (190, 190, 255)),
    "tenant-rights":  ((10, 30, 66), (31, 111, 178), (150, 210, 255)),
    "guides":         ((44, 32, 8), (184, 134, 11), (255, 220, 120)),
    "default":        ((11, 37, 69), (31, 92, 153), (184, 150, 11)),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_cover(path, category, seed, w=W, h=H):
    rnd = random.Random(seed)
    dark, mid, light = PALETTES.get(category, PALETTES["default"])
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=lerp(dark, mid, min(1, t * 1.25)))

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    cx, cy = rnd.randint(int(w * .25), int(w * .75)), int(h * rnd.uniform(.40, .55))
    for r in range(420, 0, -12):
        a = int(70 * (1 - r / 420) ** 1.6)
        g.ellipse([cx - r * 1.4, cy - r, cx + r * 1.4, cy + r], fill=light + (a,))
    img.paste(glow, (0, 0), glow)

    # Category accent behind the skyline
    acc = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    a_ = ImageDraw.Draw(acc)
    if category in ("fire",):
        for _ in range(26):
            x = rnd.randint(int(w * .15), int(w * .85))
            hh = rnd.randint(140, 330)
            ww = rnd.randint(40, 110)
            base = h * .72
            col = rnd.choice([(255, 120, 40), (255, 170, 60), (255, 210, 110)])
            a_.polygon([(x - ww, base), (x + rnd.randint(-30, 30), base - hh), (x + ww, base)], fill=col + (rnd.randint(70, 140),))
        acc = acc.filter(ImageFilter.GaussianBlur(16))
    elif category in ("rent-prices",):
        pts, y = [], h * .58
        for i in range(13):
            y -= rnd.uniform(-8, 26)
            pts.append((i * w / 12, y))
        a_.line(pts, fill=light + (220,), width=9, joint="curve")
        for p in pts[::2]:
            a_.ellipse([p[0] - 11, p[1] - 11, p[0] + 11, p[1] + 11], fill=light + (240,))
        acc = acc.filter(ImageFilter.GaussianBlur(1.2))
    elif category in ("safety", "tenant-rights", "housing-policy", "guides"):
        for i in range(7):
            r = 90 + i * 70
            a_.ellipse([cx - r, cy - r - 80, cx + r, cy + r - 80], outline=light + (60 - i * 7,), width=3)
    img.paste(acc, (0, 0), acc)

    # Skyline (two layers)
    for layer, (shade, top_lo, top_hi, lit) in enumerate([(0.55, .50, .66, .18), (0.25, .64, .80, .35)]):
        col = lerp(dark, (0, 0, 0), shade)
        x = -rnd.randint(0, 60)
        while x < w:
            bw = rnd.randint(70, 170)
            top = int(h * rnd.uniform(top_lo, top_hi))
            d.rectangle([x, top, x + bw, h], fill=col)
            if rnd.random() < .35:
                d.rectangle([x + bw * .3, top - rnd.randint(14, 40), x + bw * .7, top], fill=col)
            for wy in range(top + 18, h - 10, 26):
                for wx in range(x + 12, x + bw - 16, 22):
                    if rnd.random() < lit:
                        wc = lerp(light, (255, 245, 210), rnd.random() * .6)
                        d.rectangle([wx, wy, wx + 10, wy + 14], fill=wc)
            x += bw + rnd.randint(-4, 14)

    # Vignette + film grain for depth
    vig = Image.new("L", (w, h), 0)
    v = ImageDraw.Draw(vig)
    for i in range(60):
        v.rectangle([i * 6, i * 4, w - i * 6, h - i * 4], outline=int(150 * (1 - i / 60) ** 2))
    vig = vig.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), img, vig)
    noise = Image.effect_noise((w, h), 18).convert("RGB")
    img = Image.blend(img, noise, 0.04)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "WEBP", quality=82, method=6)


def main():
    from build import load_articles
    force = "--force" in sys.argv
    n = 0
    for a in load_articles():
        if a.get("legacy"):
            continue
        out = os.path.join(ROOT, "static", a["image"].lstrip("/"))
        if force or not os.path.exists(out):
            draw_cover(out, a["category"], int(hashlib.md5(a["slug"].encode()).hexdigest()[:8], 16))
            n += 1
    og = os.path.join(ROOT, "static/assets/img/og-default.webp")
    if force or not os.path.exists(og):
        draw_cover(og, "default", 7, 1200, 630)
        from PIL import Image as I
        im = I.open(og).convert("RGBA")
        logo = I.open(os.path.join(ROOT, "static/wp-content/uploads/2025/08/Renter-News-Logo.webp")).convert("RGBA")
        logo = logo.resize((560, int(560 * logo.height / logo.width)))
        im.paste(logo, ((1200 - logo.width) // 2, (630 - logo.height) // 2 - 40), logo)
        im.convert("RGB").save(og, "WEBP", quality=85)
    print(f"drew {n} covers")


if __name__ == "__main__":
    main()
