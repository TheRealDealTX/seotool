"""Trace the site icon (a transparent PNG/WebP) into /favicon.svg.

Uses potracer, the pure-Python port of potrace:
    pip install --target /tmp/pylib potracer
    python3 _build/trace_icon.py wp-content/uploads/2025/08/Purely-Wholesome-Farm-Site-Icon.webp favicon.svg /tmp/pylib

The icon switches to sage on dark browser themes so it stays visible.
"""
import sys
sys.path.insert(0, sys.argv[3])
import numpy as np
import potrace
from PIL import Image

src = Image.open(sys.argv[1]).convert('RGBA')
bbox = src.getbbox()
im = src.crop(bbox)
# Upscale for a smoother trace, then threshold on alpha + darkness.
scale = 2
im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
a = np.array(im)
mask = (a[:, :, 3] > 128) & (a[:, :, :3].mean(axis=2) < 160)
bmp = potrace.Bitmap(~mask)
path = bmp.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)

H, W = mask.shape
side = max(W, H)
pad = side * 0.06
size = side + 2 * pad
ox, oy = pad + (side - W) / 2, pad + (side - H) / 2
f = lambda p: f"{p.x + ox:.0f} {p.y + oy:.0f}"
d = []
for curve in path:
    d.append(f"M{f(curve.start_point)}")
    for seg in curve:
        if seg.is_corner:
            d.append(f"L{f(seg.c)}L{f(seg.end_point)}")
        else:
            d.append(f"C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}")
    d.append("Z")
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size:.0f} {size:.0f}">'
       '<style>path{fill:#1C352D}@media (prefers-color-scheme:dark){path{fill:#A6B28B}}</style>'
       f'<path fill-rule="evenodd" d="{"".join(d)}"/></svg>\n')
open(sys.argv[2], 'w').write(svg)
print(len(path), 'curves', len(svg), 'bytes')
