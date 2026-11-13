#!/usr/bin/env python3
"""Favicon, logo and OG-image pipeline. Writes into ./static (then build.py copies it to ./public).

python3 make_assets.py
Needs Pillow and Node + Playwright (preinstalled Chromium) to rasterize the SVG mark.
"""
import json
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(ROOT, "static")
SUN, INK, HARBOR = "#FEC500", "#16171B", "#23317A"

ROOF = f'<path d="M10.5 25.5L24 13l13.5 12.5" fill="none" stroke="{INK}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
WAVE = f'<path d="M9 35.5c3.75-4.2 7.5-4.2 11.25 0s7.5 4.2 11.25 0 5.6-4.2 8.5-1.6" fill="none" stroke="{HARBOR}" stroke-width="3.6" stroke-linecap="round"/>'
# Bolder, simpler version for 16-48px: thicker strokes and a single wave crest.
ROOF_B = f'<path d="M9 26L24 12l15 14" fill="none" stroke="{INK}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>'
WAVE_B = f'<path d="M8.5 37c5-6 10.5-6 15.5 0s10.5 6 15.5 0" fill="none" stroke="{HARBOR}" stroke-width="5.6" stroke-linecap="round"/>'


def svg(inner, rx=11, scale=1.0, size=48):
    off = (48 - 48 * scale) / 2
    g = f'<g transform="translate({off:.2f} {off:.2f}) scale({scale})">{inner}</g>' if scale != 1 else inner
    rect = f'<rect width="48" height="48" rx="{rx}" fill="{SUN}"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 48 48">{rect}{g}</svg>'


MARK = svg(ROOF + WAVE)
BOLD = svg(ROOF_B + WAVE_B, rx=9)
TOUCH = svg(ROOF + WAVE, rx=0, scale=0.78)       # full-bleed for iOS (it rounds corners itself)
MASK = svg(ROOF + WAVE, rx=0, scale=0.62)        # content inside the maskable 80% safe zone

JS = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const j of jobs) {
    await p.setViewportSize({ width: j.size, height: j.size });
    const html = '<html><body style="margin:0;background:transparent">' + j.svg.replace(/width="\d+" height="\d+"/, `width="${j.size}" height="${j.size}"`) + '</body></html>';
    await p.setContent(html);
    await p.screenshot({ path: j.out, omitBackground: true, clip: { x: 0, y: 0, width: j.size, height: j.size } });
  }
  await b.close();
})();
"""


def raster(jobs):
    with tempfile.TemporaryDirectory() as td:
        jf, sf = os.path.join(td, "jobs.json"), os.path.join(td, "r.js")
        json.dump(jobs, open(jf, "w"))
        open(sf, "w").write(JS)
        subprocess.run(["node", sf, jf], check=True, cwd=td)


def og_image():
    photos = json.load(open(os.path.join(ROOT, "src", "photos.json")))
    key = next(k for k in ("hero-coastal-house", "newport-harbor", "westerly-beach") if k in photos)
    im = Image.open(os.path.join(S, "assets", "img", "photos", f"{key}.webp")).convert("RGB")
    w, h = 1200, 630
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    shade = Image.new("L", (w, h))
    d = ImageDraw.Draw(shade)
    for x in range(w):
        d.line([(x, 0), (x, h)], fill=int(225 - 150 * x / w))
    dark = Image.new("RGB", (w, h), (16, 17, 21))
    im = Image.composite(dark, im, shade)
    d = ImageDraw.Draw(im)
    d.rectangle([0, h - 16, w, h], fill=SUN)
    mark = Image.open(os.path.join(S, "favicon-512.png")).convert("RGBA").resize((112, 112), Image.LANCZOS)
    im.paste(mark, (70, 120), mark)

    def font(size, bold=True):
        for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
            if os.path.exists(f):
                return ImageFont.truetype(f, size)
        return ImageFont.load_default()
    d.text((70, 270), "Rhode Island", font=font(74), fill="white")
    d.text((70, 355), "Insurance Appraiser", font=font(74), fill=SUN)
    d.text((72, 462), "Independent appraisal for underpaid property claims", font=font(30, False), fill=(235, 235, 235))
    d.text((72, 510), "rhodeislandinsuranceappraiser.com  ·  (844) 537-1427", font=font(26, False), fill=(200, 200, 200))
    im.save(os.path.join(S, "assets", "img", "og-image.jpg"), quality=86, optimize=True, progressive=True)


def main():
    os.makedirs(os.path.join(S, "assets", "img"), exist_ok=True)
    open(os.path.join(S, "favicon.svg"), "w").write(MARK)
    open(os.path.join(S, "assets", "img", "mark.svg"), "w").write(MARK)
    tmp = tempfile.mkdtemp()
    jobs = [{"svg": BOLD, "size": s, "out": os.path.join(tmp, f"b{s}.png")} for s in (16, 32, 48)]
    jobs += [{"svg": MARK, "size": 96, "out": os.path.join(S, "favicon-96x96.png")},
             {"svg": BOLD, "size": 32, "out": os.path.join(S, "favicon-32x32.png")},
             {"svg": TOUCH, "size": 180, "out": os.path.join(S, "apple-touch-icon.png")},
             {"svg": MASK, "size": 192, "out": os.path.join(S, "favicon-192.png")},
             {"svg": MASK, "size": 512, "out": os.path.join(S, "favicon-512.png")}]
    raster(jobs)
    ims = [Image.open(os.path.join(tmp, f"b{s}.png")).convert("RGBA") for s in (16, 32, 48)]
    ims[2].save(os.path.join(S, "favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=ims[:2])
    # apple-touch-icon must be opaque (full bleed)
    t = Image.open(os.path.join(S, "apple-touch-icon.png")).convert("RGB")
    t.save(os.path.join(S, "apple-touch-icon.png"))
    json.dump({
        "name": "Rhode Island Insurance Appraiser", "short_name": "RI Appraiser",
        "description": "Independent insurance appraisal for disputed property claims across Rhode Island.",
        "start_url": "/", "scope": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#16171B",
        "icons": [{"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                  {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
                  {"src": "/favicon-192.png?v=1", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                  {"src": "/favicon-512.png?v=1", "sizes": "512x512", "type": "image/png", "purpose": "any"}],
    }, open(os.path.join(S, "site.webmanifest"), "w"), indent=2)
    if os.path.exists(os.path.join(ROOT, "src", "photos.json")):
        og_image()
    print("assets written")


if __name__ == "__main__":
    main()
