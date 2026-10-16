#!/usr/bin/env python3
"""Featured-image cards for the new puregoatfarms.com posts.

The two existing posts use photo-style featured images. We cannot produce
photos here, so each new post gets a typographic card in the site's own
palette (the one its calculators use: green #202A19, rust #A34B2A, cream
#F7F4ED) at the same 1000x563 size, saved as WebP like the originals. Swap
them for photos from wp-admin whenever you like; nothing else depends on them.

Usage: python3 make_images.py payload.json out_dir
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1000, 563
GREEN, RUST, CREAM, LINE = "#202A19", "#A34B2A", "#F7F4ED", "#D8D5CC"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def wrap(draw, text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card(title, kicker, path):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    # Left rust band and thin rule, echoing the calculator styling.
    d.rectangle([0, 0, 18, H], fill=RUST)
    d.line([(70, 92), (W - 70, 92)], fill=LINE, width=2)
    label = ImageFont.truetype(SANS_BOLD, 22)
    d.text((70, 52), "PURE GOAT FARMS  ·  MILKING & DAIRY", font=label, fill=RUST)

    size = 64
    while size > 36:
        font = ImageFont.truetype(SERIF_BOLD, size)
        lines = wrap(d, title, font, W - 140)
        if len(lines) <= 3:
            break
        size -= 4
    line_h = int(size * 1.18)
    y = 150
    for ln in lines:
        d.text((70, y), ln, font=font, fill=GREEN)
        y += line_h

    kf = ImageFont.truetype(SANS, 28)
    d.text((70, y + 26), kicker, font=kf, fill=GREEN)
    d.rectangle([70, H - 70, 70 + 120, H - 62], fill=RUST)
    d.text((70, H - 50), "puregoatfarms.com", font=ImageFont.truetype(SANS, 20), fill=GREEN)
    im.save(path, "WEBP", quality=88, method=6)


def main():
    payload, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    with open(payload, encoding="utf-8") as f:
        posts = json.load(f)["posts"]
    for post in posts:
        path = os.path.join(out_dir, post["slug"] + ".webp")
        card(post["image_title"], post["image_kicker"], path)
        print(path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
