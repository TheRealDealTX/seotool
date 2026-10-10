#!/usr/bin/env python3
"""Download the chosen royalty-free photos and write optimized WebP crops.

    python3 fetch_photos.py            # only missing files
    python3 fetch_photos.py --force    # re-download everything

Reads photos.json (key -> source photo + alt text), writes
assets/photos/<key>-800.webp and -1600.webp (16:10 crops). Needs ImageMagick.
Every photo is royalty-free: the Pexels License, CC0 or public domain (the
latter found through Openverse). None requires attribution; photos.json keeps
each photo's source page and license on record.
"""

import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "photos"


def main():
    force = "--force" in sys.argv
    photos = json.loads((ROOT / "photos.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    for key, ph in photos.items():
        targets = [OUT / f"{key}-{w}.webp" for w in (800, 1600)]
        if not force and all(t.exists() for t in targets):
            continue
        if ph["license"] not in ("pexels", "cc0", "pdm"):
            raise SystemExit(f"{key}: license {ph['license']} is not a royalty-free license")
        req = urllib.request.Request(ph["url"], headers={"User-Agent": "hotsbuzz-rebuild/1.0"})
        with tempfile.NamedTemporaryFile(suffix=".img") as tmp:
            for attempt in range(4):
                try:
                    tmp.write(urllib.request.urlopen(req, timeout=120).read())
                    break
                except Exception as e:  # Wikimedia/Flickr throttle bursts with 429s
                    if attempt == 3:
                        raise
                    print("retry", key, e)
                    time.sleep(10 * (attempt + 1))
            tmp.flush()
            for w, t in zip((800, 1600), targets):
                h = w * 10 // 16
                subprocess.run(["convert", tmp.name + "[0]", "-auto-orient", "-colorspace", "sRGB",
                                "-resize", f"{w}x{h}^", "-gravity", ph.get("gravity", "center"),
                                "-extent", f"{w}x{h}", "-strip", "-quality", "80", str(t)], check=True)
        print("ok", key)


if __name__ == "__main__":
    main()
