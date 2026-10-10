#!/usr/bin/env python3
"""Make labelled contact sheets of the picked images for review: contact_sheet.py OUTDIR"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
img = Path(__file__).resolve().parent / "public/assets/img"
files = sorted(f for f in img.glob("*-sm.webp"))
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
W, H, cols = 320, 200, 4
for n in range(0, len(files), 16):
    chunk = files[n:n+16]
    sheet = Image.new("RGB", (W*cols, (H+18)*((len(chunk)+cols-1)//cols)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(f).convert("RGB"); im.thumbnail((W, H))
        x, y = (i % cols)*W, (i//cols)*(H+18)
        sheet.paste(im, (x, y+18)); d.text((x+4, y+3), f.name[:-8], fill="black")
    sheet.save(out / f"sheet{n//16}.png"); print(out / f"sheet{n//16}.png")
