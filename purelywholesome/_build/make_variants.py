"""Recreate WordPress resized image variants (foo-300x200.webp) from the originals.

The host answers missing image paths with its own 404 before PHP runs, so the
variant URLs the old site exposed in srcsets (and Google Images may have indexed)
must exist as real files.

    python3 _build/make_variants.py variant-urls.txt
"""
import os
import re
import sys

from PIL import Image, ImageOps

ROOT = os.path.join(os.path.dirname(__file__), "..")
made = skipped = 0
for line in open(sys.argv[1]):
    m = re.search(r"/(wp-content/uploads/.+)-(\d+)x(\d+)(\.\w+)$", line.strip())
    if not m:
        continue
    base, w, h, ext = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    out = os.path.join(ROOT, f"{base}-{w}x{h}{ext}")
    src = os.path.join(ROOT, base + ext)
    if os.path.exists(out) or not os.path.exists(src):
        skipped += 1
        continue
    with Image.open(src) as im:
        im = ImageOps.fit(im.convert("RGB"), (w, h), Image.LANCZOS) if (w / h) != (im.width / im.height) else im.convert("RGB").resize((w, h), Image.LANCZOS)
        fmt = {".webp": "WEBP", ".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}[ext.lower()]
        im.save(out, fmt, **({"quality": 78} if fmt != "PNG" else {"optimize": True}))
    made += 1
print(f"made={made} skipped={skipped}")
