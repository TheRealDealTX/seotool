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
            if i == tries - 1:
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
    cands.sort(key=lambda c: 0 if c["license"] in ("CC0", "Public Domain Mark") else 1)
    for c in cands[:3]:
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
        time.sleep(2.5)
    json.dump(credits, open(CRED, "w"), indent=1)
    print("products with photos:", sum(1 for p in prods if p["slug"] in credits), "/", len(prods))

if __name__ == "__main__":
    main()
