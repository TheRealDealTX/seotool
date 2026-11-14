#!/usr/bin/env python3
"""Photo pipeline: downloaded originals -> 1200px and 640px WebP + src/photos.json manifest.

  python3 tools/process_photos.py <dir-with-originals> <download-manifest.json>

The download manifest (written by the photo fetch step) holds, per key: Openverse id, title,
creator, license (cc0 or pdm only), provider, source URL and landing page. This script adds the
alt text and output size and writes src/photos.json. The manifest is an internal record only;
nothing from it is published as a credits page.
"""
import json
import os
import sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "assets", "img", "photos")

ALT = {
    "hero": "Downtown Boise at dusk, with light trails on Capitol Boulevard leading to the Idaho State Capitol",
    "wildfire-ridge": "Air tanker dropping red retardant on a wildfire burning above homes in the Boise foothills",
    "wildfire-smoke": "Wildfire smoke billowing over forested mountains in the Boise area",
    "farm-barn": "Red barn and farm fields under a dark, stormy sky",
    "farmland": "Historic Art Moderne creamery building in Caldwell, Idaho",
    "commercial-building": "Brick commercial building with a cast-iron front seen from street level",
    "icicles": "Long icicles hanging from a snow-covered roof edge",
    "kitchen": "Modern white kitchen with an island and pendant lights",
    "living-room": "Living room with a sofa, coffee table and ceiling fan",
    "clipboard": "Hands filling in an inspection form on a clipboard",
    "roof-shingles": "Close-up of overlapping dark roof shingles",
    "roof-inspection": "Roofer’s tool belt and hammer resting on a shingle roof",
    "house-fire": "Charred interior of a house after a fire",
    "lewiston": "Bridge in Lewiston, Idaho, with the river valley hills behind",
    "sun-valley": "Valley and mountain ranges in the Sawtooth National Forest near Sun Valley, Idaho",
    "sawtooth": "Snow-covered mountain peaks above an evergreen ridge",
    "snow-house": "Red house buried in deep winter snow",
    "snow-roof": "Wooden cabins with roofs loaded with heavy snow",
    "neighborhood": "Suburban home on a quiet residential street",
    "home-exterior": "Two-story family home with a porch and front lawn",
    "home-exterior-2": "Gabled family home with dormers and landscaped garden",
    "storm-front": "Dark storm clouds and rain over mountain peaks",
    "thunderstorm": "Thunderstorm with rain shafts glowing at sunset over open valley land",
    "snake-river": "Fall color along the Snake River canyon",
    "hail-ground": "Hailstones piled in the grass after a storm",
    "idaho-falls": "Upper Mesa Falls on the Henrys Fork in eastern Idaho",
    "pocatello": "Crew laying erosion-control matting on a burned hillside after a wildfire",
    "twin-falls": "The Snake River winding through a canyon in fall",
    "coeur-d-alene": "Lake Coeur d’Alene seen from Canfield Mountain in North Idaho",
    "calculator": "Calculator, pen and figures on a desk",
    "consult-table": "Person taking notes on a notepad at a desk",
    "meeting-room": "Small group meeting around a table in a conference room",
    "laptop-docs": "Hands using a calculator beside a laptop spreadsheet",
    "paperwork": "Notepad, calculator, glasses and pen on a white desk",
    "frozen-pipe": "Homeowner looking up at a water-stained, moldy bathroom ceiling after a leak",
}


def main(src, manifest_path):
    man = json.load(open(manifest_path, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    photos = {}
    for key, alt in ALT.items():
        fp = os.path.join(src, key + ".jpg")
        if not os.path.exists(fp) or key not in man:
            print("missing", key)
            continue
        m = man[key]
        assert m["license"] in ("cc0", "pdm"), f"{key}: license {m['license']} is not CC0/PD"
        im = ImageOps.exif_transpose(Image.open(fp)).convert("RGB")
        w = min(1200, im.width)
        big = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if im.width > w else im
        big.save(os.path.join(OUT, key + ".webp"), "WEBP", quality=80, method=6)
        sm = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        sm.save(os.path.join(OUT, key + "-640.webp"), "WEBP", quality=78, method=6)
        photos[key] = {"alt": alt, "fw": big.width, "fh": big.height, "title": m["title"], "creator": m.get("creator"),
                       "license": "CC0 1.0" if m["license"] == "cc0" else "Public domain", "provider": m.get("provider"),
                       "source": m["url"], "landing": m["landing"], "openverse_id": m["id"]}
        print("ok", key, big.width, big.height)
    json.dump(photos, open(os.path.join(ROOT, "src", "photos.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(photos), "photos")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
