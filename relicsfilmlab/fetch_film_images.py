"""Candidate photos for the Film & Batteries shelf (openly licensed, via Openverse).

  python3 fetch_film_images.py candidates   # writes contact sheets to a scratch dir for review
  python3 fetch_film_images.py pick key=idx ...   # saves chosen candidates + credits
Chosen images: public/assets/img/film/<key>.webp, credits: data/image_credits_film.json
"""
import json, os, re, sys, io, time
from PIL import Image, ImageDraw
import fetch_images as F

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public", "assets", "img", "film")
CRED = os.path.join(ROOT, "data", "image_credits_film.json")
SCRATCH = os.environ.get("SCRATCH", "/tmp")

def key(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

# shelf item name -> (queries, title tokens that must appear (any group satisfied), )
ITEMS = {
    "Kodak Gold 200": (["Kodak Gold 200 film", "Kodak Gold 200"], ["gold"]),
    "Kodak UltraMax 400": (["Kodak Ultramax 400", "Kodak Ultramax film"], ["ultramax", "ultra max"]),
    "Kodak Portra 400": (["Kodak Portra 400 box", "Kodak Portra 400 film roll"], ["portra"]),
    "Kodak Ektar 100": (["Kodak Ektar 100 film", "Kodak Ektar"], ["ektar"]),
    "CineStill 800T": (["CineStill 800T film", "Cinestill 800"], ["cinestill"]),
    "Ilford HP5 Plus 400": (["Ilford HP5 Plus film", "Ilford HP5"], ["hp5", "hp 5"]),
    "Kodak Tri-X 400": (["Kodak Tri-X 400 film", "Kodak Tri-X"], ["tri-x", "trix", "tri x"]),
    "Kodak Portra 400 (120)": (["Portra 120 film", "Kodak Portra 120"], ["portra"]),
    "Kodak Ektar 100 (120)": (["Ektar 120 film", "Kodak Ektar 120"], ["ektar"]),
    "Ilford HP5 Plus (120)": (["Ilford HP5 120", "Ilford 120 film"], ["ilford", "hp5"]),
    "Polaroid 600 Color": (["Polaroid 600 film pack", "Polaroid 600 film"], ["600"]),
    "Polaroid 600 B&W": (["Polaroid black and white 600 film", "Impossible project black white film"], ["polaroid", "impossible"]),
    "Polaroid SX-70 Color": (["Polaroid SX-70 film", "SX-70 film pack"], ["sx-70", "sx70", "sx 70"]),
    "Polaroid SX-70 B&W": (["SX-70 black and white film", "Polaroid SX-70 film"], ["sx-70", "sx70", "sx 70"]),
    "Instax Wide (twin pack)": (["Instax Wide film", "Fujifilm Instax film"], ["instax"]),
    "Instax Wide Monochrome": (["Instax monochrome film", "Instax Wide film"], ["instax"]),
    "Kodak Vision3 50D Super 8": (["Kodak Super 8 film cartridge", "Super 8 cartridge"], ["super 8", "super8", "super-8"]),
    "Kodak Vision3 200T Super 8": (["Kodak Vision3 Super 8", "Super 8 film cartridge"], ["super 8", "super8", "super-8", "vision"]),
    "Kodak Vision3 500T Super 8": (["Kodak Vision3 500T", "Super 8 film"], ["super 8", "super8", "vision", "500t"]),
    "Kodak Tri-X Super 8": (["Tri-X Super 8", "Kodak Super 8 film"], ["super 8", "super8", "tri-x"]),
    "Lomography 110 Color": (["Lomography 110 film", "110 film cartridge"], ["110"]),
    "Kodak FunSaver (disposable)": (["Kodak FunSaver", "Kodak disposable camera"], ["kodak", "funsaver", "fun saver"]),
    "Fujifilm QuickSnap (disposable)": (["Fujifilm QuickSnap", "Fuji Quicksnap"], ["quicksnap", "quick snap"]),
    "Ilford XP2 (disposable)": (["Ilford XP2", "Ilford single use camera"], ["xp2", "ilford"]),
    "LR44 / SR44": (["LR44 battery", "LR44 button cell"], ["lr44", "ag13", "button"]),
    "CR123A": (["CR123A battery", "CR123 battery"], ["cr123", "123"]),
    "CR2": (["CR2 battery", "CR2 lithium"], ["cr2"]),
    "4LR44 / PX28 6V": (["4LR44 battery", "PX28 battery", "6V battery"], ["4lr44", "px28", "6v"]),
    "2CR5": (["2CR5 battery", "2CR5"], ["2cr5"]),
    "PX625 / MR9 adapter": (["PX625 battery", "mercury battery camera"], ["625", "mercury"]),
}
BAD = ("shot on", "shot with", "taken with", "portrait", "street", "landscape", "beach", "sunset", "#", "selfie", "wedding", "flower")

def candidates():
    allc = {}
    for name, (qs, toks) in ITEMS.items():
        c = []
        for q in qs:
            try:
                c += F.openverse(q, "cc0,pdm,by,by-sa", 20, min_w=400)
            except Exception as e:
                print("search fail", q, e); time.sleep(20)
            time.sleep(3.5)
        seen, out = set(), []
        for x in c:
            t = x["title"].lower()
            if x["url"] in seen or "wikimedia" in x["url"] or any(b in t for b in BAD) or not any(k in t for k in toks):
                continue
            seen.add(x["url"]); out.append(x)
        allc[key(name)] = out[:10]
        W, H, cols = 220, 160, 10
        sheet = Image.new("RGB", (W * cols, H + 16), "white"); d = ImageDraw.Draw(sheet)
        for i, x in enumerate(out[:10]):
            try:
                u = x["url"]
                if "upload.wikimedia.org" in u and "/thumb/" not in u:
                    u = F.thumb(u).replace("1280px", "330px")
                im = Image.open(io.BytesIO(F.get(u))).convert("RGB"); im.thumbnail((W, H))
                sheet.paste(im, (i * W, 0)); d.text((i * W + 2, H + 2), f"{i} {x['title'][:30]}", fill="black")
            except Exception as e:
                print("thumb fail", name, i, e)
        sheet.save(os.path.join(SCRATCH, f"film-{key(name)}.png"))
        json.dump(allc, open(os.path.join(SCRATCH, "film-cands.json"), "w"))
        print(name, len(out), flush=True)

def pick(args):
    allc = json.load(open(os.path.join(SCRATCH, "film-cands.json")))
    cred = json.load(open(CRED)) if os.path.exists(CRED) else {}
    os.makedirs(OUT, exist_ok=True)
    for a in args:
        k, i = a.split("=")
        x = allc[k][int(i)]
        cred[k] = F.save(x, os.path.join(OUT, k + ".webp"), 800, 1.0)
        print("saved", k, x["title"][:60])
    json.dump(cred, open(CRED, "w"), indent=1)

if __name__ == "__main__":
    if sys.argv[1] == "candidates":
        candidates()
    else:
        pick(sys.argv[2:])
