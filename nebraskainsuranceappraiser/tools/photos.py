#!/usr/bin/env python3
"""Photo pipeline: originals (CC0 / public domain only) -> 1200px + 640px WebP, and src/photos.json.

python3 tools/photos.py <originals-dir> <openverse-metadata.json>

The metadata file maps each photo key to its Openverse record (title, creator, license,
source, url, foreign_landing_url). Only `cc0` and `pdm` licenses are accepted. The record is
kept in src/photos.json for our own files; it is never published as a credits page.
"""
import json, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(ROOT, "static", "assets", "img", "photos")
MAN = os.path.join(ROOT, "src", "photos.json")


def main(src_dir, meta_file):
    meta = json.load(open(meta_file))
    man = json.load(open(MAN)) if os.path.exists(MAN) else {}
    os.makedirs(DEST, exist_ok=True)
    for key, r in meta.items():
        if r.get("license") not in ("cc0", "pdm"):
            sys.exit(f"{key}: license {r.get('license')} is not CC0/PD")
        fn = os.path.join(src_dir, key + ".jpg")
        if not os.path.exists(fn):
            print("missing", key); continue
        im = Image.open(fn).convert("RGB")
        sizes = {}
        for w, suffix in ((1200, ""), (640, "-640")):
            x = im.copy()
            if x.width > w:
                x = x.resize((w, round(x.height * w / x.width)), Image.LANCZOS)
            x.save(os.path.join(DEST, f"{key}{suffix}.webp"), "WEBP", quality=80, method=6)
            sizes[suffix or "full"] = x.size
        man[key] = {
            "title": r.get("title"), "creator": r.get("creator"), "license": r["license"],
            "source": r.get("source"), "url": r.get("url"), "landing": r.get("foreign_landing_url") or r.get("landing"),
            "fw": sizes["full"][0], "fh": sizes["full"][1],
        }
        print(key, sizes)
    json.dump(dict(sorted(man.items())), open(MAN, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
