"""Download royalty-free / openly licensed photos for the catalog.

Sources: Wikimedia Commons (product photos of the exact camera model) and
Openverse (CC0 / public-domain lifestyle photography). Only licences that allow
commercial reuse are accepted (CC0, PD, CC BY, CC BY-SA). Credits are written
to data/image_credits.json and rendered on each product page and on
/pages/photo-credits.

    python3 fetch_images.py            # fetch anything missing
"""
import json, os, re, sys, time, html, io, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import catalog

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public", "assets", "img")
CRED = os.environ.get("CRED_FILE") or os.path.join(ROOT, "data", "image_credits.json")
UA = "RelicsFilmLabSiteBuilder/1.0 (static site build; contact info@relicsfilmlab.com)"
OK_LIC = re.compile(r"^(cc0|cc-?zero|public domain|pd|pdm|cc by(-sa)?( \d\.\d)?|cc-by(-sa)?-\d\.\d|by|by-sa)", re.I)

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1 or ("wikimedia.org" in url and "429" in str(e)):
                raise
            time.sleep((15 if "429" in str(e) else 2) * (i + 1))

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def commons(query, limit=12):
    q = urllib.parse.urlencode(dict(action="query", format="json", generator="search", gsrsearch=query + " filetype:bitmap",
                                    gsrnamespace=6, gsrlimit=limit, prop="imageinfo", iiprop="url|extmetadata|size",
                                    iiurlwidth=960, iiextmetadatafilter="LicenseShortName|Artist|LicenseUrl"))
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
    res = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip(md.get("LicenseShortName", {}).get("value"))
        if not OK_LIC.match(lic) or "nc" in lic.lower() or "nd" in lic.lower().split():
            continue
        if ii.get("width", 0) < 500:
            continue
        res.append(dict(title=p["title"].replace("File:", ""), url=ii.get("thumburl") or ii.get("url"),
                        page=ii.get("descriptionurl", "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p["title"])),
                        artist=strip(md.get("Artist", {}).get("value"))[:80] or "Unknown", license=lic, source="Wikimedia Commons"))
    return res

def openverse(query, licenses="cc0,pdm", n=20, wide=False, min_w=900):
    q = dict(q=query, license=licenses, page_size=n)
    if wide:
        q["aspect_ratio"] = "wide"
        q["size"] = "large"
    d = json.loads(get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(q)))
    res = []
    for r in d.get("results", []):
        if (r.get("width") or 0) < min_w:
            continue
        lic = ("CC0" if r["license"] == "cc0" else "Public Domain Mark" if r["license"] == "pdm"
               else f"CC {r['license'].upper()} {r.get('license_version') or ''}".strip())
        res.append(dict(title=r.get("title") or query, url=r["url"], page=r.get("foreign_landing_url") or r["url"],
                        artist=(r.get("creator") or "Unknown")[:80], license=lic, source=r.get("source", "Openverse").title()))
    return res

def thumb(url):
    m = re.match(r"https://upload\.wikimedia\.org/wikipedia/commons/(\w/\w\w)/([^/?]+)$", url)
    if m:
        return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{m.group(1)}/{m.group(2)}/1280px-{m.group(2)}"
    return url

def save(item, path, maxw=1200, ratio=None):
    raw = get(thumb(item["url"]))
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGB")
    if ratio:  # centre crop to w/h ratio
        w, h = im.size
        if w / h > ratio:
            nw = int(h * ratio); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(w / ratio); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=78, method=5)
    return dict(item, w=im.width, h=im.height)

# ---- product query building -------------------------------------------------
STOP = {"with", "lens", "the", "and", "black", "silver", "red", "date", "new", "like", "new", "instant", "camera", "film",
        "35mm", "(black)", "&", "–", "-", "original", "case", "quartz", "kit", "professional"}

def model_tokens(name):
    n = re.sub(r"\(.*?\)", "", name)
    n = re.sub(r"\bwith\b.*$", "", n, flags=re.I)
    n = re.sub(r"\b(19\d\d)\b", "", n)
    toks = [t for t in re.split(r"[\s/]+", n) if t and t.lower() not in STOP]
    return toks

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def matches(title, toks):
    t = norm(title)
    must = [norm(x) for x in toks if norm(x)]
    # brand + every model token must appear (allowing "AE-1" == "AE1")
    return all(m in t for m in must)

CAR_Q = {
    "2002-porsche-911-turbo": "Porsche 996 Turbo", "1997-911-carrera-cabriolet": "Porsche 993 Carrera Cabriolet",
    "1997-911-carrera-targa": "Porsche 993 Targa", "porsche-carerra": "Porsche 911 Carrera classic",
    "porsche-progression": "Porsche 911 generations", "lancia-delta": "Lancia Delta Integrale",
    "mercedes-500sl": "Mercedes-Benz R129 500 SL", "paris-dakar-rally": "Dakar Rally car",
}
CAT_STOCK = {  # openverse lifestyle queries for non-camera items
    "book": "photography books", "print": "basketball hoop vintage", "tote": "canvas tote bag",
    "bag": "leather camera bag", "strap": "vintage camera strap", "collect": "35mm film canister",
    "service": "film negatives", "workshop": "darkroom photography", "film": "35mm film roll",
    "lens": "camera lens", "digital": "camcorder",
}

LIFESTYLE = {  # site imagery: name -> (query, licences, ratio)
    "hero": ("vintage film camera", "cc0,pdm", 16 / 9),
    "hero2": ("35mm film camera photographer", "cc0,pdm", 16 / 9),
    "film-rolls": ("35mm film roll", "cc0,pdm", 4 / 3),
    "darkroom": ("darkroom photography", "cc0,pdm,by,by-sa", 4 / 3),
    "negatives": ("film negatives", "cc0,pdm,by,by-sa", 4 / 3),
    "polaroids": ("polaroid photos", "cc0,pdm,by,by-sa", 4 / 3),
    "slr": ("SLR film camera", "cc0,pdm", 4 / 3),
    "point-shoot": ("compact film camera", "cc0,pdm,by,by-sa", 4 / 3),
    "medium-format": ("Hasselblad camera", "cc0,pdm,by,by-sa", 4 / 3),
    "super8": ("super 8 camera", "cc0,pdm,by,by-sa", 4 / 3),
    "workshop": ("photography class", "cc0,pdm,by,by-sa", 4 / 3),
    "books": ("photography books", "cc0,pdm,by,by-sa", 4 / 3),
    "prints": ("framed photographs wall", "cc0,pdm,by,by-sa", 4 / 3),
    "cars": ("Porsche 911 classic", "cc0,pdm,by,by-sa", 4 / 3),
    "accessories": ("camera bag", "cc0,pdm,by,by-sa", 4 / 3),
    "long-beach": ("Long Beach California", "cc0,pdm,by,by-sa", 16 / 9),
    "repair": ("camera repair", "cc0,pdm,by,by-sa", 4 / 3),
    "scanner": ("film scanner", "cc0,pdm,by,by-sa", 4 / 3),
    "gift": ("vintage camera gift", "cc0,pdm,by,by-sa", 4 / 3),
    "disposable": ("disposable camera", "cc0,pdm,by,by-sa", 4 / 3),
    "lens": ("camera lens", "cc0,pdm", 4 / 3),
    "photographer": ("photographer film camera street", "cc0,pdm", 4 / 5),
}

def fetch_product(p, credits):
    slug = p["slug"]
    path = os.path.join(OUT, "products", slug + ".webp")
    if os.path.exists(path) and slug in credits:
        return slug, credits[slug]
    cands = []
    try:
        if p["cat"] == "carprint":
            cands = openverse(CAR_Q.get(slug, p["name"]), "cc0,pdm,by,by-sa", 10)
        elif p["cat"] in ("ps", "slr", "instant", "mf", "movie", "pocket", "digital", "lens") and slug not in ("canon", "28mm-lens", "28-85mm-lens", "ds-max-hc-2000", "kinon-5050"):
            toks = model_tokens(p["name"])
            q = " ".join(toks)
            cands = [c for c in openverse(q, "cc0,pdm,by,by-sa", 20, min_w=500) if matches(c["title"], toks)]
    except Exception as e:
        print("search fail", slug, e, file=sys.stderr)
        return slug, "retry"
    cands.sort(key=lambda c: (1 if "wikimedia" in c["url"] else 0, 0 if c["license"] in ("CC0", "Public Domain Mark") else 1))
    for c in cands[:4]:
        try:
            return slug, save(c, path, 1000)
        except Exception as e:
            print("dl fail", slug, e, file=sys.stderr)
    return slug, None

def main():
    credits = json.load(open(CRED)) if os.path.exists(CRED) else {}
    # lifestyle imagery
    for name in ([] if os.environ.get("REVERSE") else LIFESTYLE):
        pass
    for name, (q, lic, ratio) in ({} if os.environ.get("REVERSE") else LIFESTYLE).items():
        key = "site:" + name
        path = os.path.join(OUT, "site", name + ".webp")
        if os.path.exists(path) and key in credits:
            continue
        try:
            for c in openverse(q, lic, 20, wide=ratio > 1.2)[:4]:
                try:
                    credits[key] = save(c, path, 1800 if ratio > 1.2 else 1200, ratio)
                    print("site", name, c["title"][:60])
                    break
                except Exception as e:
                    print("dl fail", name, e, file=sys.stderr)
        except Exception as e:
            print("search fail", name, e, file=sys.stderr)
        time.sleep(0.5)
    json.dump(credits, open(CRED, "w"), indent=1)
    prods = catalog.products()
    only = set(sys.argv[1:])
    if os.environ.get("REVERSE"):
        prods = prods[::-1]
    for p in prods:
        if os.environ.get("REVERSE") and os.path.exists(os.path.join(OUT, "products", p["slug"] + ".webp")):
            continue
        if only and p["slug"] not in only:
            continue
        if p["slug"] in credits or p["slug"] in credits.get("_miss", []):
            continue
        slug, cred = fetch_product(p, credits)
        if cred == "retry":
            time.sleep(30)
            continue
        if cred:
            credits[slug] = cred
            print("ok", slug, flush=True)
        else:
            credits.setdefault("_miss", []).append(slug)
            print("--", slug, flush=True)
        json.dump(credits, open(CRED, "w"), indent=1)
        time.sleep(1.5)
    json.dump(credits, open(CRED, "w"), indent=1)
    print("products with photos:", sum(1 for p in prods if p["slug"] in credits), "/", len(prods))

if __name__ == "__main__":
    main()

# ---- second pass: alternate names / relaxed matching for misses ----------------
ALT = {
    "mamiya-7-with-80mm-lens": ["Mamiya 7"], "pentax-km-35mm-film-camera-with-50mm-lens": ["Pentax KM"], "nikon-f-black-35mm-film-camera-with-35-70mm-lens": ["Nikon F black", "Nikon F"],
    "werra": ["Werra camera", "Zeiss Werra"], "polaroid-pz2001": ["Polaroid PZ2001", "Polaroid PZ"], "olympus-infinity-zoom-2000": ["Olympus Infinity Zoom"],
    "olympus-stylus-epic-zoom-170": ["Olympus mju zoom 170", "Olympus Stylus Epic Zoom"], "sony-cyber-shot-dsc-wx350-white": ["Sony WX350", "Sony Cyber-shot WX"],
    "bell-amp-howell-bf-705-big-finder-motor": ["Bell Howell camera"], "premier-pc-80-with-50mm-lens": ["Premier PC-80"],
    "minolta-x-700-mps-with-50mm-lens": ["Minolta X-700"], "canon-eos-rebel-xs": ["Canon EOS 500"], "canon-sure-shot-z-115": ["Canon Prima Super 115", "Canon Sure Shot Z115"],
    "olympus-quick-shooter": ["Olympus Quick Shooter"], "pentax-iqzoom-160": ["Pentax Espio 160", "Pentax IQZoom 160"], "olympus-superzoom-760": ["Olympus Superzoom"],
    "canon-514xl-super-8-camera": ["Canon 514XL", "Canon 514"], "olympus-stylus-zoom-35-70mm": ["Olympus mju zoom", "Olympus Stylus Zoom"],
    "olympus-infinity-zoom-200": ["Olympus Infinity Zoom"], "polaroid-one-step-land-camera": ["Polaroid OneStep", "Polaroid One Step"],
    "olympus-stylus": ["Olympus mju II", "Olympus Stylus Epic"], "olympus-stylus-epic-dlx-w-panoramic": ["Olympus mju II", "Olympus Stylus Epic"],
    "kodak-cameo-motor-ex": ["Kodak Cameo"], "kodak-cameo-focus-free": ["Kodak Cameo"], "kodak-cameo-zoom-plus": ["Kodak Cameo"],
    "fuji-discovery-1000-zoom": ["Fuji Discovery"], "fuji-discovery": ["Fuji Discovery"], "nikon-tele-touch": ["Nikon Tele Touch", "Nikon TW2"],
    "canon-sure-shot-owl-date": ["Canon Sure Shot Owl", "Canon Autoboy 3"], "minolta-xg-1": ["Minolta XG-1", "Minolta XG1"], "nikon-f-photomic": ["Nikon F Photomic"],
    "polaroid-600-one-step-spirit-instant-camera": ["Polaroid Spirit 600"], "polaroid-600-onestep-close-up-instant-camera": ["Polaroid OneStep Close Up", "Polaroid 600"],
    "nikon-one-touch": ["Nikon One Touch", "Nikon L35AF3"], "nikon-one-touch-zoom-90s": ["Nikon One Touch Zoom"], "kiev-6c-with-65mm-lens": ["Kiev 6C", "Kiev 60"],
    "olympus-stylus-120": ["Olympus mju zoom 120", "Olympus Stylus"], "olympus-stylus-infinity-mju-35mm-black-amp-silver": ["Olympus mju"],
    "olympus-stylus-35-mm-black": ["Olympus mju"], "chinon-20-p-xl-direct-sound-super-8-camera": ["Chinon Super 8"], "minolta-srt-101-with-50mm-lens-1966": ["Minolta SRT 101", "Minolta SR-T 101"],
    "contax-t3-like-new": ["Contax T3"], "olympus-om-2n": ["Olympus OM-2"], "canon-af-35-ml": ["Canon AF35ML"], "konica-autoreflex-t3": ["Konica Autoreflex T3", "Konica T3"],
    "polaroid-sun-660": ["Polaroid Sun 660"], "olympus-om-g": ["Olympus OM-G", "Olympus OM-20"], "polaroid-600-cool-cam-instant-camera": ["Polaroid Cool Cam"],
    "fujifilm-instax-wide-300-instant-film-camera-black-silver": ["Instax Wide 300"], "minolta-af-tel": ["Minolta AF-Tele"], "polaroid-pronto-land-camera": ["Polaroid Pronto"],
    "minolta-110-zoom-date": ["Minolta 110 Zoom"], "polaroid-600-sun-lms-instant-camera": ["Polaroid Sun 600"], "pentax-auto-110-film-camera": ["Pentax Auto 110"],
    "minolta-xe-7-with-50mm-lens": ["Minolta XE-7", "Minolta XE"], "nikon-nikonos-iv-a": ["Nikonos IV"], "fuji-fujica-st-605": ["Fujica ST605", "Fujica ST 605"],
    "canon-310xl-super-8-camera": ["Canon 310XL", "Canon 310 XL"], "nikon-l35-af": ["Nikon L35AF", "Nikon L35 AF"], "minolta-srt-200": ["Minolta SRT", "Minolta SR-T"],
    "canon-t70-1": ["Canon T70"], "fuji-gs645-s": ["Fuji GS645"], "minolta-hi-matic-af-2": ["Minolta Hi-Matic AF2"], "minolta-hi-matic-af2-md": ["Minolta Hi-Matic AF2"],
    "minolta-hi-matic-af2-m": ["Minolta Hi-Matic AF2"], "yashica-35-me-1973": ["Yashica 35-ME", "Yashica 35 ME"], "mamiya-c330-with-80mm-lens": ["Mamiya C330"],
    "olympus-pen-ee-1961": ["Olympus Pen EE"], "zeiss-ikon-contaflex-with-original-leather-case1953": ["Zeiss Ikon Contaflex"], "olympus-xa2-2": ["Olympus XA2"],
    "olympus-xa2-original-case-a11-electronic-flash": ["Olympus XA2"], "canon-tl": ["Canon TL"], "canon-ftb": ["Canon FTb"], "zeiss-ikon-contessa-lk-1963": ["Zeiss Ikon Contessa"],
    "nishika-n8000-3d-35mm-film-camera": ["Nishika N8000"], "pentax-mg-with-50mm-lens": ["Pentax MG"], "canon-a-1-black-1": ["Canon A-1"], "pentax-k-1000-with-50mm-lens-1": ["Pentax K1000"],
    "nikon-fe2": ["Nikon FE2"], "canon-canonet-ql-17-giii-1": ["Canonet QL17", "Canonet G-III"], "canon-canonet-ql-17-n": ["Canonet QL17"], "hasselblad-503cx": ["Hasselblad 503CX", "Hasselblad 503"],
    "hasselblad-500cm": ["Hasselblad 500C/M", "Hasselblad 500CM"], "nikon-em": ["Nikon EM"], "nikon-fg-1982": ["Nikon FG"], "nikon-fg-black-with-50mm-lens": ["Nikon FG"],
    "mamiya-rb67-pro-sd": ["Mamiya RB67"], "contax-t2": ["Contax T2"], "nikon-f2-with-50mm-lens": ["Nikon F2"], "nikon-fe-black": ["Nikon FE"], "nikon-fm-with-50mm-lens": ["Nikon FM"],
    "pentax-me-super-with-50mm-lens": ["Pentax ME Super"], "pentax-me": ["Pentax ME"], "olympus-om-10-with-50mm-lens-black": ["Olympus OM-10"], "olympus-om-10": ["Olympus OM-10", "Olympus OM10"],
    "yashica-mat-124-g": ["Yashica Mat 124", "Yashica-Mat"], "yashica-electro-35-gsn": ["Yashica Electro 35"], "yashica-electro-35-gt": ["Yashica Electro 35"], "yashica-a": ["Yashica-A", "Yashica TLR"],
    "mamiya-c220-professional": ["Mamiya C220"], "canon-ae-1-program": ["Canon AE-1 Program"], "canon-at-1": ["Canon AT-1"], "canon-av-1": ["Canon AV-1"], "canon-tx": ["Canon TX"],
    "canon-t50-with-35-70mm-zoom-lens": ["Canon T50"], "minolta-x-370": ["Minolta X-370", "Minolta X-300"], "minolta-xg-m": ["Minolta XG-M"], "minolta-xg-9": ["Minolta XG-9", "Minolta XG9"],
    "olympus-35-rc": ["Olympus 35 RC"], "canon-af-35m": ["Canon AF35M"], "canon-af35m-ii": ["Canon AF35M"], "olympus-trip-af-50": ["Olympus Trip AF"], "olympus-trip-af-60": ["Olympus Trip AF"],
    "olympus-trip-md3": ["Olympus Trip MD"], "petri-7s": ["Petri 7s", "Petri 7"], "petri-flex-7": ["Petriflex 7", "Petri Flex"], "petri-flex-v": ["Petriflex V", "Petri Flex"],
    "agfa-silette-sl": ["Agfa Silette"], "agfa-optima-500": ["Agfa Optima"], "konica-autoreflex-tc": ["Konica Autoreflex TC"], "ricoh-kr-10m": ["Ricoh KR-10"],
    "kyocera-samurai-x3-0-red-35mm-half-frame-film-camera": ["Kyocera Samurai", "Yashica Samurai"], "canon-elph-sport": ["Canon Elph"], "minolta-weathermatic-dual-35": ["Minolta Weathermatic"],
    "canon-canonet-28": ["Canonet 28"], "canon-canonet-ql-25": ["Canonet QL25", "Canonet"], "canon-a35-f-40mm-lens": ["Canon A35F", "Canon A35"], "sony-handycam-ccd-sc5": ["Sony CCD-SC5", "Sony Handycam"],
    "canon-powershot-a550": ["Canon PowerShot A550"], "bolex-580-super-8-camera": ["Bolex Super 8", "Bolex 580"], "minolta-minoltina-p": ["Minoltina"], "yashica-j-3": ["Yashica J-3"],
    "mamiyasekor-msx-500": ["Mamiya Sekor 500", "Mamiya MSX"], "vivitar-v3000s": ["Vivitar V3000"], "pentax-espio-738": ["Pentax Espio"], "pentax-pc-35-afm": ["Pentax PC35AF"],
    "polaroid-impulse-se": ["Polaroid Impulse"], "polaroid-600-impulse-instant-camera": ["Polaroid Impulse"], "polaroid-600-silver-express-instant-camera": ["Polaroid 600 Express", "Polaroid OneStep 600"],
    "polaroid-600-one-step-rainbow-instant-camera": ["Polaroid OneStep 600", "Polaroid 600"], "polaroid-job-pro-2": ["Polaroid Job Pro"], "polaroid-photo-magic-system": ["Polaroid 600"],
    "polaroid-252-bv": ["Polaroid camera"], "minolta-freedom-dual": ["Minolta Freedom"], "minolta-freedom-zoom-90": ["Minolta Freedom Zoom"], "nikon-zoom-touch-400": ["Nikon Zoom Touch"],
    "nikon-lite-touch-zoom-110": ["Nikon Lite Touch"], "canon-sureshot-telemax": ["Canon Sure Shot Tele"], "canon-sure-shot-telemax-date": ["Canon Sure Shot Tele"],
    "pentax-iqzoom-900": ["Pentax IQZoom"], "minolta-freedom-zoom-supreme-ex": ["Minolta Freedom Zoom"], "samsung-maxima-zoom-70-xl": ["Samsung Maxima"],
    "point-and-shoot-a-m-minolta-hi-matic-s": ["Minolta Hi-Matic"], "minolta-hi-matic-s2": ["Minolta Hi-Matic"],
}

def second_pass():
    credits = json.load(open(CRED))
    miss = [s for s in credits.get("_miss", []) if s in ALT]
    prods = {p["slug"]: p for p in catalog.products()}
    for slug in miss:
        p = prods[slug]
        got = None
        for q in ALT[slug]:
            toks = [t for t in re.split(r"\s+", q)]
            try:
                cands = [c for c in openverse(q, "cc0,pdm,by,by-sa", 20, min_w=500) if matches(c["title"], toks)]
            except Exception as e:
                print("search fail", slug, e, file=sys.stderr); time.sleep(30); continue
            cands.sort(key=lambda c: (1 if "wikimedia" in c["url"] else 0, 0 if c["license"] in ("CC0", "Public Domain Mark") else 1))
            for c in cands[:4]:
                try:
                    got = save(c, os.path.join(OUT, "products", slug + ".webp"), 1000); break
                except Exception as e:
                    print("dl fail", slug, e, file=sys.stderr)
            time.sleep(3)
            if got:
                break
        if got:
            credits[slug] = got; credits["_miss"].remove(slug); print("ok2", slug, flush=True)
        else:
            print("--2", slug, flush=True)
        json.dump(credits, open(CRED, "w"), indent=1)
