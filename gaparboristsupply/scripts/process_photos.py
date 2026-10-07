"""Turns the hand-picked candidates in work/photos/picks.json into web images and
the credits file the site reads.

picks.json: {"<kind>": [["<source kind>", <candidate n>, <focus y 0-1, optional>], ...], ...}
A kind may borrow a candidate from another kind's folder (e.g. "hero" from "chainsaw").

Writes site/assets/photos/<kind>-<i>.webp (1200x900) and -sm.webp (600x450),
and site/data/images.json: {"<kind>": [{"src", "sm", "title", "creator", ...}]}.
    python3 scripts/process_photos.py
"""
import json
import os

from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'work', 'photos')
OUT = os.path.join(ROOT, 'site', 'assets', 'photos')
os.makedirs(OUT, exist_ok=True)
picks = json.load(open(os.path.join(SRC, 'picks.json')))
meta = {}
images = {}
for kind, items in picks.items():
    images[kind] = []
    for i, item in enumerate(items):
        src_kind, n = item[0], item[1]
        focus = item[2] if len(item) > 2 else 0.45
        if src_kind not in meta:
            meta[src_kind] = {m['n']: m for m in json.load(open(os.path.join(SRC, src_kind, 'meta.json')))}
        m = meta[src_kind][n]
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src_kind, f'{n:02d}.jpg'))).convert('RGB')
        big = ImageOps.fit(im, (1200, 900), Image.LANCZOS, centering=(0.5, focus))
        name = f'{kind}-{i}'
        big.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=78, method=6)
        big.resize((600, 450), Image.LANCZOS).save(os.path.join(OUT, name + '-sm.webp'), 'WEBP', quality=76, method=6)
        lic = (m['license'] or '').upper()
        lic = 'Public domain' if lic == 'PDM' else ('CC0' if lic == 'CC0' else f"CC {lic} {m.get('license_version') or ''}".strip())
        images[kind].append({
            'src': f'/assets/photos/{name}.webp', 'sm': f'/assets/photos/{name}-sm.webp',
            'title': (m.get('title') or 'Untitled').strip(), 'creator': (m.get('creator') or 'Unknown').strip(),
            'creator_url': m.get('creator_url') or '', 'license': lic, 'license_url': m.get('license_url') or '',
            'source_url': m.get('foreign_landing_url') or '',
        })
json.dump(images, open(os.path.join(ROOT, 'site', 'data', 'images.json'), 'w'), indent=1, ensure_ascii=False)
print({k: len(v) for k, v in images.items()})
