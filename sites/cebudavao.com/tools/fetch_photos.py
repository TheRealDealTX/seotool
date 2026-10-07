#!/usr/bin/env python3
"""Fetch a licensed photo library from Wikimedia Commons.

Each entry is key -> search query. For every key the first landscape JPEG with a
free licence (CC BY / CC BY-SA / CC0 / public domain) is downloaded, resized to
1200px and 640px WebP, and recorded in data/photos.json with its credit line.
Re-running skips keys already present. Usage: python3 tools/fetch_photos.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request, io, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "photos")
DB = os.path.join(ROOT, "data", "photos.json")
UA = "CebuDavaoSiteBuilder/1.0 (https://cebudavao.com; photo credits page)"

QUERIES = {
    "cebu-skyline": "Cebu City skyline",
    "cebu-it-park": "Cebu IT Park",
    "magellans-cross": "Magellan's Cross Cebu",
    "santo-nino-basilica": "Basilica del Santo Niño Cebu",
    "fort-san-pedro": "Fort San Pedro Cebu",
    "taoist-temple-cebu": "Taoist Temple Cebu",
    "temple-of-leah": "Temple of Leah Cebu",
    "sinulog": "Sinulog festival dancers",
    "kawasan-falls": "Kawasan Falls Badian",
    "moalboal": "Moalboal Cebu",
    "oslob-whale-shark": "whale shark Oslob",
    "bantayan-island": "Bantayan Island beach",
    "malapascua": "Malapascua Island beach Bounty",
    "mactan-beach": "Mactan Island beach resort",
    "cclex-bridge": "Cebu-Cordova Link Expressway",
    "simala-shrine": "Monastery of the Holy Eucharist Simala",
    "cebu-lechon": "lechon Cebu",
    "lechon-roasting": "Lechon roasting",
    "puso-rice": "puso hanging rice",
    "siomai": "siomai",
    "cebu-guitar": "Cebu guitar Lapu-Lapu guitar making",
    "davao-city": "Davao City skyline",
    "davao-peoples-park": "People's Park Davao",
    "mount-apo": "Mount Apo",
    "philippine-eagle": "Philippine Eagle Pithecophaga jefferyi",
    "samal-beach": "Island Garden City of Samal beach",
    "pearl-farm": "Pearl Farm Beach Resort Samal",
    "talikud-island": "Talikud Island",
    "durian": "durian fruit",
    "kadayawan": "Kadayawan festival Davao",
    "eden-nature-park": "Eden Nature Park Davao",
    "davao-river": "Davao River",
    "marilog": "Marilog Davao",
    "kinilaw": "kinilaw",
    "tuna-gensan": "tuna General Santos fish port",
    "bangus": "grilled milkfish bangus",
    "adobo": "Chicken adobo",
    "sinigang": "sinigang",
    "halo-halo": "halo-halo dessert",
    "barbecue-pinoy": "Filipino pork barbecue skewers",
    "boodle-fight": "boodle fight",
    "batchoy": "batchoy",
    "pancit": "pancit",
    "dried-fish": "dried fish danggit market Philippines",
    "fish-market": "fish market Philippines",
    "basil": "basil plant",
    "chocolate-hills": "Chocolate Hills Bohol",
    "tarsier": "Philippine tarsier",
    "boracay": "White Beach Boracay",
    "siargao": "Cloud 9 Siargao",
    "el-nido": "El Nido Palawan",
    "coron": "Kayangan Lake Coron",
    "banaue": "Batad rice terraces",
    "vigan": "Calle Crisologo Vigan",
    "intramuros": "Intramuros Manila",
    "manila-skyline": "Makati skyline",
    "camiguin": "Camiguin White Island",
    "siquijor": "Siquijor beach",
    "jeepney": "jeepney Philippines",
    "ferry": "ferry Cebu port",
    "mactan-airport": "Mactan-Cebu International Airport terminal",
    "davao-airport": "Francisco Bangoy International Airport",
    "airplane-philippines": "Philippine Airlines aircraft",
    "passport": "Philippine passport",
    "basketball-court": "basketball game Philippines",
    "boxing": "boxing match ring",
    "football-philippines": "Philippines women's national football team",
    "pickleball": "pickleball",
    "surfing": "surfing Siargao",
    "running-race": "marathon runners",
    "esports": "esports tournament",
    "smartphone": "smartphone mobile phone",
    "gecko-tuko": "tokay gecko",
    "chinese-new-year": "Chinese New Year lion dance Philippines",
    "edsa": "EDSA People Power Monument",
    "rizal": "Rizal Monument Luneta",
    "concert": "concert crowd Philippines",
    "guitar-band": "band performing Manila",
    "cinema": "movie theater cinema seats",
    "books": "books library shelves",
    "typhoon-satellite": "typhoon satellite image Philippines",
    "rain-street": "rain street Philippines",
    "spratly": "Spratly Islands",
    "mall": "SM City Cebu",
    "bpo-office": "call center office",
    "condo-cebu": "condominium Cebu",
    "market-carbon": "Carbon Market Cebu",
    "coffee": "coffee cup cafe",
    "money-peso": "Philippine peso coins",
    "atm": "Automated teller machine",
    "hospital": "hospital Philippines",
    "hands-palm": "human hand palm lines",
    "face-portrait": "Denzel Washington",
    "batman": "Batman cosplay",
    "rice-field": "rice field Philippines",
    "coconut-trees": "coconut trees beach Philippines",
    "mangrove": "mangrove Philippines",
    "plantation-bay": "Plantation Bay Resort Mactan",
    "lapu-lapu-shrine": "Lapu-Lapu Shrine Mactan",
    "tops-lookout": "Tops Lookout Busay Cebu",
    "bohol-loboc": "Loboc River Bohol",
    "camotes": "Camotes Island beach",
    "iloilo": "Iloilo Esplanade",
    "bacolod-masskara": "MassKara Festival",
    "cagayan-de-oro": "Cagayan de Oro rafting",
    "baguio": "Baguio City Burnham Park",
    "sunset-beach": "sunset beach Philippines",
    "island-hopping": "bangka boat island hopping Philippines",
    "snorkel-reef": "coral reef Philippines underwater",
    "tribal-davao": "Kadayawan indigenous dance",
    "church-cebu": "Cebu Metropolitan Cathedral",
}
OK_LIC = re.compile(r"^(CC BY(-SA)?( \d\.\d)?|CC0|Public domain|PD|Attribution)", re.I)

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else json.loads(data)

def strip(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def search(q):
    p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": q + " filetype:bitmap",
         "gsrnamespace": "6", "gsrlimit": "20", "prop": "imageinfo",
         "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "960"}
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    pages = sorted(d.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 99))
    for pg in pages:
        ii = (pg.get("imageinfo") or [{}])[0]
        if ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 1000:
            continue
        if ii["width"] < ii["height"] * 1.2:
            continue
        md = ii.get("extmetadata", {})
        lic = strip(md.get("LicenseShortName", {}).get("value", ""))
        if not OK_LIC.match(lic) or "NC" in lic or "ND" in lic:
            continue
        yield pg["title"], ii, lic, strip(md.get("Artist", {}).get("value", "")) or "Unknown author"

def main():
    db = json.load(open(DB)) if os.path.exists(DB) else {}
    os.makedirs(OUT, exist_ok=True)
    only = set(sys.argv[1:])
    for key, q in QUERIES.items():
        if key in db or (only and key not in only):
            continue
        try:
            for title, ii, lic, artist in search(q):
                time.sleep(8); raw = get(ii["thumburl"], binary=True)
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                for w, suffix in ((1200, ""), (640, "-sm")):
                    c = im.copy(); c.thumbnail((w, w * 2))
                    c.save(os.path.join(OUT, f"{key}{suffix}.webp"), "WEBP", quality=78, method=6)
                db[key] = {"file": f"{key}.webp", "w": min(1200, im.width), "h": round(min(1200, im.width) * im.height / im.width),
                           "title": title[5:].rsplit(".", 1)[0], "author": artist[:120], "license": lic,
                           "source": ii["descriptionurl"], "query": q}
                print("ok ", key, "<-", title, "|", lic, "|", artist[:40])
                break
            else:
                print("MISS", key, q)
        except Exception as e:
            print("ERR ", key, e)
        json.dump(db, open(DB, "w"), indent=1, ensure_ascii=False)
        time.sleep(40)

if __name__ == "__main__":
    main()
