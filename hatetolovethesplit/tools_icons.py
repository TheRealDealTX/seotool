"""One-off asset generator: favicons + 1200x630 Open Graph JPGs (needs Pillow)."""
import glob, json, os
from PIL import Image, ImageDraw, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(ROOT, "static")


def icon(size, pad=0.0):
    k = 8  # supersample
    n = size * k
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    inset = int(n * pad)
    d.rounded_rectangle([inset, inset, n - inset - 1, n - inset - 1], radius=int((n - 2 * inset) * 0.22), fill="#211a2e")
    u = (n - 2 * inset) / 64
    o = lambda x, y: (inset + x * u, inset + y * u)
    w = int(6 * u)
    d.line([o(14, 40), o(32, 22), o(50, 40)], fill="#f3a6b5", width=w, joint="curve")
    for x, y in ((14, 40), (32, 22), (50, 40), (22, 46), (42, 46)):
        r = w / 2
        cx, cy = o(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#f3a6b5" if y != 46 else "#b8a2ea")
    d.line([o(22, 46), o(42, 46)], fill="#b8a2ea", width=w)
    return im.resize((size, size), Image.LANCZOS)


icon(48).save(os.path.join(S, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
icon(96).save(os.path.join(S, "favicon-96x96.png"))
# iOS ignores transparency: full-bleed square
bg = Image.new("RGBA", (180, 180), "#211a2e"); bg.alpha_composite(icon(180)); bg.convert("RGB").save(os.path.join(S, "apple-touch-icon.png"))
for sz in (192, 512):
    m = Image.new("RGBA", (sz, sz), "#211a2e"); m.alpha_composite(icon(sz, pad=0.1))  # maskable safe zone
    m.convert("RGB").save(os.path.join(S, f"web-app-manifest-{sz}x{sz}.png"))
json.dump({"name": "Hate to Love the Split", "short_name": "The Split", "start_url": "/", "display": "standalone",
           "background_color": "#fffaf6", "theme_color": "#211a2e",
           "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                     {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
          open(os.path.join(S, "site.webmanifest"), "w"), indent=2)

og = os.path.join(ROOT, "assets", "og"); os.makedirs(og, exist_ok=True)
for f in glob.glob(os.path.join(ROOT, "assets", "img", "*.webp")):
    im = ImageOps.fit(Image.open(f).convert("RGB"), (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
    im.save(os.path.join(og, os.path.basename(f)[:-5] + ".jpg"), quality=82, optimize=True, progressive=True)
print("ok")
