"""Build the favicon set from the original Better Outdoors mountain icon.
White mountains on a navy (#061E29) rounded square. Run: python3 scripts/favicons.py"""
import os, json
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = Image.open(ROOT + '/wp-content/uploads/2026/01/cropped-Better-Outdoors-Site-Icon.webp').convert('RGBA')
alpha = src.getchannel('A')
mask = alpha.crop(alpha.point(lambda a: 255 if a > 60 else 0).getbbox())
NAVY = (6, 30, 41, 255)

def icon(size, radius=0.22, scale=0.9, bleed=False):
    S = 1024
    shape = Image.new('L', (S, S), 0)
    ImageDraw.Draw(shape).rectangle([0, 0, S, S], fill=255) if bleed else ImageDraw.Draw(shape).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=255)
    m = mask.resize((int(S * scale), int(S * scale * mask.height / mask.width)), Image.LANCZOS)
    layer = Image.new('L', (S, S), 0)
    layer.paste(m, ((S - m.width) // 2, int(S * 0.53) - m.height // 2))
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    im.paste(Image.new('RGBA', (S, S), NAVY), (0, 0), shape)
    white = Image.new('RGBA', (S, S), (255, 255, 255, 255))
    from PIL import ImageChops
    im.paste(white, (0, 0), ImageChops.multiply(layer, shape))
    return im.resize((size, size), Image.LANCZOS)

out = lambda n: os.path.join(ROOT, n)
icon(48).save(out('favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
for s in (16, 32, 48, 96):
    icon(s).save(out(f'favicon-{s}x{s}.png'), optimize=True)
icon(180, bleed=True).convert('RGB').save(out('apple-touch-icon.png'), optimize=True)
icon(192).save(out('web-app-manifest-192x192.png'), optimize=True)
icon(512).save(out('web-app-manifest-512x512.png'), optimize=True)
icon(512, scale=0.68, bleed=True).save(out('web-app-manifest-maskable-512x512.png'), optimize=True)
json.dump({
    'name': 'Better Outdoors', 'short_name': 'Better Outdoors',
    'description': 'Archery guides, bow reviews and free bowhunting tools.',
    'start_url': '/', 'scope': '/', 'display': 'standalone',
    'background_color': '#ffffff', 'theme_color': '#061E29',
    'icons': [
        {'src': '/web-app-manifest-192x192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
        {'src': '/web-app-manifest-512x512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
        {'src': '/web-app-manifest-maskable-512x512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}, open(out('site.webmanifest'), 'w'), indent=2)
print('done')
