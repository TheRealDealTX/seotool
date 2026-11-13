#!/usr/bin/env python3
"""Makes the site icons and the Open Graph image (run once; outputs are committed).

  favicon.ico                      16, 32, 48 px
  favicon-96x96.png                rounded tile
  apple-touch-icon.png             180 px, full-bleed (iOS rounds the corners)
  web-app-manifest-192x192.png     rounded tile, purpose "any"
  web-app-manifest-512x512.png     rounded tile, purpose "any"
  web-app-manifest-maskable-512x512.png   full-bleed, mark inside the safe zone
  assets/og-image.png              1200x630, rendered from tools/og.html

Needs Pillow, the Inter font (FONT below) and Playwright with Chromium.
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
NAVY = (19, 58, 107, 255)


def tile(size, radius_ratio=14 / 64, letter_ratio=0.62, scale=4):
    """The 'R' tile from favicon.svg, drawn at 4x and downsampled for clean edges."""
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(s * radius_ratio)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=NAVY) if r else d.rectangle([0, 0, s, s], fill=NAVY)
    font = ImageFont.truetype(FONT, int(s * letter_ratio))
    box = d.textbbox((0, 0), "R", font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((s - w) / 2 - box[0], (s - h) / 2 - box[1]), "R", font=font, fill="white")
    return img.resize((size, size), Image.LANCZOS)


def out(name):
    return os.path.join(ROOT, name)


def main():
    tile(96).save(out("favicon-96x96.png"))
    tile(192).save(out("web-app-manifest-192x192.png"))
    tile(512).save(out("web-app-manifest-512x512.png"))
    tile(180, radius_ratio=0, letter_ratio=0.56).convert("RGB").save(out("apple-touch-icon.png"))
    tile(512, radius_ratio=0, letter_ratio=0.44).convert("RGB").save(out("web-app-manifest-maskable-512x512.png"))
    ico = [tile(n, radius_ratio=0.18, letter_ratio=0.68) for n in (16, 32, 48)]
    ico[2].save(out("favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ico[:2])

    script = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1200, height: 630 }}, deviceScaleFactor: 1 }});
  await p.goto('file://{out("tools/og.html")}');
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({{ path: '{out("assets/og-image.png")}' }});
  await b.close();
}})();
"""
    subprocess.run(["node", "-e", script], check=True)
    for f in ["favicon.ico", "favicon-96x96.png", "apple-touch-icon.png", "web-app-manifest-192x192.png",
              "web-app-manifest-512x512.png", "web-app-manifest-maskable-512x512.png", "assets/og-image.png"]:
        print(f, os.path.getsize(out(f)), "bytes")


if __name__ == "__main__":
    main()
