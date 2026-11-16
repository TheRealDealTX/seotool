"""Fill in photos for products that fetch_images.py couldn't match exactly.

Tier 1  exact model photo                      -> kind "exact"
Tier 2  same product family / series           -> kind "representative" (labelled on the page)
Tier 3  topic photo for non-camera items       -> kind "illustrative"  (labelled on the page)

Only openly licensed photos (CC0 / PD / CC BY / CC BY-SA) via Openverse. Titles that look
like sample photos *taken with* a camera are rejected. Writes data/image_credits_extra.json.

    python3 fetch_missing.py
"""
import json, os, re, sys, time, hashlib
import catalog, fetch_images as F

ROOT = os.path.dirname(os.path.abspath(__file__))
EXTRA = os.path.join(ROOT, "data", "image_credits_extra.json")
OUT = os.path.join(ROOT, "public", "assets", "img", "products")
LIC = "cc0,pdm,by,by-sa"
BAD_WORDS = ("shot with", "shot on", "taken with", "photo taken", "test roll", "scan", "portrait", "street", "digital", "dslr", "mirrorless",
             "selfie", "sears", "advert", " ad ", "catalog", "1958", "lot of", "collection", "sunset", "landscape", "beach", "wedding", "flower", "tree", "sample", "expired", "roll ", "frame ", "#")

FAMILY = [  # (slug prefix, family queries, family label)
    ("minolta-freedom", ["Minolta Freedom camera", "Minolta Riva", "Minolta compact camera"], "Minolta Freedom"),
    ("minolta-hi-matic", ["Minolta Hi-Matic AF2", "Minolta Hi-Matic"], "Minolta Hi-Matic"),
    ("minolta-af101r", ["Minolta compact camera"], "Minolta compact"), ("minolta-af-tel", ["Minolta AF-Tele", "Minolta compact camera"], "Minolta AF compact"),
    ("minolta-silver-streak", ["Minolta compact camera"], "Minolta compact"),
    ("canon-sure-shot", ["Canon Sure Shot", "Canon Sureshot", "Canon Prima", "Canon Autoboy"], "Canon Sure Shot"),
    ("canon-sureshot", ["Canon Sure Shot", "Canon Sureshot", "Canon Prima", "Canon Autoboy"], "Canon Sure Shot"),
    ("canon-z-135", ["Canon Sure Shot", "Canon Prima"], "Canon Sure Shot"), ("canon-a1-sureshot", ["Canon Sure Shot A1", "Canon Sure Shot"], "Canon Sure Shot"),
    ("canon-snappy", ["Canon Snappy", "Canon compact camera"], "Canon Snappy"), ("canon-af-10", ["Canon compact camera", "Canon Snappy"], "Canon compact"),
    ("canon-a35", ["Canon A35", "Canonet"], "Canon rangefinder"), ("canon-at-1", ["Canon AT-1", "Canon AE-1"], "Canon A-series"),
    ("canon-eos-rebel-xs", ["Canon EOS 500 film", "Canon EOS film camera", "Canon EOS Rebel film"], "Canon EOS film SLR"),
    ("pentax-iq", ["Pentax IQZoom", "Pentax Espio", "Pentax compact camera"], "Pentax IQZoom"), ("pentax-espio", ["Pentax Espio", "Pentax IQZoom"], "Pentax Espio"),
    ("pentax-zoom-70", ["Pentax Zoom 70", "Pentax compact camera"], "Pentax Zoom"),
    ("olympus-infinity", ["Olympus Infinity", "Olympus Superzoom", "Olympus AF camera"], "Olympus Infinity"),
    ("olympus-superzoom", ["Olympus Superzoom", "Olympus Infinity"], "Olympus Superzoom"),
    ("olympus-stylus", ["Olympus mju", "Olympus Stylus film", "Olympus mju-II"], "Olympus Stylus / mju"),
    ("olympus-quick-shooter", ["Olympus Quick Shooter", "Olympus compact camera"], "Olympus compact"),
    ("olympus-xa2", ["Olympus XA2", "Olympus XA"], "Olympus XA"),
    ("samsung", ["Samsung Maxima", "Samsung Evoca", "Samsung compact camera"], "Samsung Maxima"),
    ("vivitar", ["Vivitar camera", "Vivitar 35mm"], "Vivitar 35mm"), ("quantaray", ["Quantaray camera", "compact 35mm camera"], "35mm compact"),
    ("nikon-one-touch", ["Nikon One Touch", "Nikon L35AF", "Nikon compact camera"], "Nikon One Touch"),
    ("nikon-tele-touch", ["Nikon Tele Touch", "Nikon TW", "Nikon compact camera"], "Nikon Touch"),
    ("nikon-lite-touch", ["Nikon Lite Touch", "Nikon compact camera"], "Nikon Lite Touch"), ("nikon-zoom-touch", ["Nikon Zoom Touch", "Nikon compact camera"], "Nikon Zoom Touch"),
    ("nikon-fun-touch", ["Nikon Fun Touch", "Nikon compact camera"], "Nikon compact"), ("nikon-fe2", ["Nikon FE2", "Nikon FE", "Nikon FM2"], "Nikon FE"),
    ("kodak-cameo", ["Kodak Cameo", "Kodak 35mm camera"], "Kodak Cameo"), ("kodak-kb", ["Kodak KB", "Kodak 35mm camera"], "Kodak 35mm"),
    ("kodak-s300", ["Kodak 35mm camera"], "Kodak 35mm"), ("kodak-fisher", ["Fisher-Price camera", "Kodak 110 camera"], "110 camera"),
    ("fuji-discovery", ["Fuji Discovery", "Fujifilm compact camera"], "Fuji Discovery"), ("fujica-dl", ["Fujica DL", "Fujica compact"], "Fujica DL"),
    ("konica", ["Konica compact camera", "Konica Big Mini", "Konica camera"], "Konica compact"),
    ("ricoh", ["Ricoh compact camera", "Ricoh FF", "Ricoh camera"], "Ricoh compact"),
    ("keystone", ["Keystone camera"], "Keystone"), ("kinon", ["compact 35mm camera"], "35mm compact"), ("ds-max", ["compact 35mm camera"], "35mm compact"),
    ("yashica-zoom", ["Yashica Microtec", "Yashica compact camera"], "Yashica compact"), ("yashica-j-3", ["Yashica J-3", "Yashica Penta J", "Yashica SLR"], "Yashica SLR"),
    ("yashica-a", ["Yashica-A", "Yashica 44", "Yashica TLR", "Yashica Mat"], "Yashica TLR"),
    ("agfa-optima", ["Agfa Optima", "Agfa camera"], "Agfa Optima"), ("agfa-silette", ["Agfa Silette", "Agfa camera"], "Agfa Silette"),
    ("zeiss-ikon-contessa", ["Zeiss Ikon Contessa", "Zeiss Ikon camera"], "Zeiss Ikon"),
    ("kyocera-samurai", ["Yashica Samurai", "Kyocera Samurai", "half frame camera"], "Samurai half-frame"),
    ("petri", ["Petri camera", "Petriflex"], "Petri"), ("chinon", ["Chinon super 8", "Chinon camera", "super 8 camera"], "Chinon Super 8"),
    ("polaroid-pronto", ["Polaroid Pronto", "Polaroid SX-70 camera"], "Polaroid SX-70"), ("polaroid-job-pro", ["Polaroid 600 camera", "Polaroid camera"], "Polaroid 600"),
    ("polaroid", ["Polaroid 600 camera", "Polaroid One Step", "Polaroid camera"], "Polaroid 600"),
    ("hasselblad", ["Hasselblad camera", "Hasselblad 500", "Hasselblad"], "Hasselblad V-system"),
    ("mamiya-rb67", ["Mamiya RB67", "Mamiya RZ67", "Mamiya camera"], "Mamiya RB67"), ("mamiya-c220", ["Mamiya C220", "Mamiya C330", "Mamiya TLR"], "Mamiya C-series TLR"),
    ("kiev", ["Kiev 60", "Kiev 88", "Kiev camera", "Pentacon Six"], "Kiev medium format"),
    ("canon-powershot", ["Canon PowerShot", "Canon digital compact"], "Canon PowerShot"),
]

TOPICS = {  # category -> queries for illustrative photos
    "book": ["photography book", "photo book", "camera books", "vintage photography book"],
    "print": ["basketball", "basketball hoop", "basketball court", "basketball game"],
    "tote": ["canvas tote bag", "tote bag"],
    "bag": ["leather camera bag", "camera bag", "vintage camera case"],
    "strap": ["camera strap", "vintage camera strap"],
    "collect": ["35mm film canister", "film canister", "film cartridge"],
    "lens": ["camera lens", "28mm lens", "zoom lens"],
    "service": ["film developing", "film negatives", "film scanner", "darkroom", "photo prints"],
    "workshop": ["darkroom", "film camera class", "developing tank", "photography lesson"],
    "film": ["35mm film roll", "Kodak film", "film rolls"],
    "carprint": ["Porsche 911"],
}
SPECIFIC = {  # slug -> topic query override
    "fuji-blimp-inflated": ["Fuji blimp", "Fujifilm blimp", "blimp"], "scan-only": ["film scanner", "negative scanner"],
    "develop-only": ["developing tank", "film developing"], "black-white-film-processing": ["black and white film developing", "darkroom"],
    "develop-scan-ecn-2-motion-picture-film": ["motion picture film", "35mm cinema film"], "4x6-prints-individual": ["photo prints", "photographs prints"],
    "camera-repair-diagnostic": ["camera repair", "disassembled camera"], "color-film": ["Kodak Portra", "35mm color film", "Kodak Gold"],
    "black-and-white-film-developing-workshop": ["darkroom", "developing film"], "camera-basics-workshop": ["film camera", "learning photography"],
    "private-film-photography-group-workshop-with-drake-founder-of-relics": ["photography walk", "film photographers"],
    "porsche-progression": ["Porsche 911 classic", "Porsche 964", "Porsche 993"], "the-darkroom-book": ["darkroom"], "the-morgan-amp-morgan-darkroom-book": ["darkroom enlarger"],
    "the-practical-zone-system": ["light meter", "black and white landscape print"], "28mm-lens": ["28mm lens", "wide angle lens"], "28-85mm-lens": ["zoom lens", "camera lens"],
    "canon": ["Canon FD lens", "Canon lens"], "autumn-vintage-strap": ["camera strap"], "mike-tyson-bobby-brown-tote-bag": ["tote bag"],
}

def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

def clean_title(c):
    t = c["title"].lower()
    return not any(w in t for w in BAD_WORDS)

USED = set()

def search(q, n=20):
    for i in range(3):
        try:
            return F.openverse(q, LIC, n, min_w=500)
        except Exception as e:
            print("search fail", q, e, file=sys.stderr)
            time.sleep(20 * (i + 1))
    return []

def try_save(cands, slug, used_ok=False):
    cands = [c for c in cands if used_ok or c["url"] not in USED]
    cands.sort(key=lambda c: (1 if "wikimedia" in c["url"] else 0, 0 if c["license"] in ("CC0", "Public Domain Mark") else 1))
    for c in cands[:4]:
        try:
            r = F.save(c, os.path.join(OUT, slug + ".webp"), 1000)
            USED.add(c["url"])
            return r
        except Exception as e:
            print("dl fail", slug, e, file=sys.stderr)
    return None

def brand_tok(slug):
    b = slug.split("-")[0]
    return {"fujica": "fuji", "fujifilm": "fuji", "mamiyasekor": "mamiya", "ds": "", "kinon": "", "quantaray": ""}.get(b, b)

def fetch(p):
    slug, cat = p["slug"], p["cat"]
    is_cam = cat in ("ps", "slr", "instant", "mf", "movie", "pocket", "digital")
    if is_cam:
        # tier 1: exact
        qs = F.ALT.get(slug, []) + [" ".join(F.model_tokens(p["name"]))]
        for q in qs:
            toks = q.split()
            c = [x for x in search(q) if F.matches(x["title"], toks) and clean_title(x)]
            r = try_save(c, slug)
            time.sleep(1.5)
            if r:
                if F.matches(r["title"], F.model_tokens(p["name"])):
                    return dict(r, kind="exact")
                fam = next((lab for pre, qq, lab in FAMILY if slug.startswith(pre)), q)
                return dict(r, kind="representative", family=fam)
        # tier 2: family
        fam = next(((qq, lab) for pre, qq, lab in FAMILY if slug.startswith(pre)), None)
        if fam:
            b = norm(brand_tok(slug))
            for q in fam[0]:
                c = [x for x in search(q) if clean_title(x) and (not b or b in norm(x["title"])) and ("camera" in x["title"].lower() or norm(q.split()[-1]) in norm(x["title"]))]
                r = try_save(c, slug)
                time.sleep(1.5)
                if r:
                    return dict(r, kind="representative", family=fam[1])
        return None
    # tier 3: topic
    for q in SPECIFIC.get(slug, TOPICS.get(cat, [])):
        c = [x for x in search(q, 20)]
        r = try_save(c, slug)
        time.sleep(1.5)
        if r:
            return dict(r, kind="illustrative")
    return None

def main():
    extra = json.load(open(EXTRA)) if os.path.exists(EXTRA) else {}
    for v in extra.values():
        USED.add(v["url"])
    only = set(sys.argv[1:])
    todo = [p for p in catalog.products() if not os.path.exists(os.path.join(OUT, p["slug"] + ".webp")) and (not only or p["slug"] in only)]
    print("missing:", len(todo), flush=True)
    for p in todo:
        r = fetch(p)
        if r:
            extra[p["slug"]] = r
            print("ok", r["kind"], p["slug"], "|", r["title"][:60], flush=True)
        else:
            print("--", p["slug"], flush=True)
        json.dump(extra, open(EXTRA, "w"), indent=1)

if __name__ == "__main__":
    main()


def reuse_siblings():
    """For products still without a photo, reuse an approved photo of the same series (cameras)
    or the same category (books, prints, bags...), labelled representative / illustrative."""
    import shutil
    extra = json.load(open(EXTRA)) if os.path.exists(EXTRA) else {}
    allc = {}
    for f in ("image_credits.json", "image_credits_extra.json"):
        allc.update({k: v for k, v in json.load(open(os.path.join(ROOT, "data", f))).items() if not k.startswith("_") and not k.startswith("site:")})
    allc = {k: v for k, v in allc.items() if os.path.exists(os.path.join(OUT, k + ".webp"))}
    prods = catalog.products()
    bycat = {}
    for p in prods:
        bycat.setdefault(p["cat"], []).append(p["slug"])
    def fam_of(slug):
        return next(((pre, lab) for pre, qq, lab in FAMILY if slug.startswith(pre)), None)
    n = 0
    for i, p in enumerate(prods):
        slug, cat = p["slug"], p["cat"]
        if os.path.exists(os.path.join(OUT, slug + ".webp")):
            continue
        src, kind, label = None, None, None
        fam = fam_of(slug)
        if fam:
            sib = [k for k in allc if k != slug and k.startswith(fam[0]) and allc[k].get("kind") in (None, "exact", "representative")]
            if not sib and "-" in fam[0]:   # widen to brand + type, e.g. any Minolta compact
                b = slug.split("-")[0]
                sib = [k for k in allc if k.startswith(b + "-") and next((q["cat"] for q in prods if q["slug"] == k), "") == cat and allc[k].get("kind") in (None, "exact", "representative")]
                label = f"{b.title()} {catalog.CATEGORIES[cat][0].lower()}" if sib else None
            if sib:
                src, kind, label = sib[i % len(sib)], "representative", label or fam[1]
        if not src:
            sib = [k for k in allc if k in bycat.get(cat, []) and k != slug]
            if sib:
                src = sib[i % len(sib)]
                kind = "illustrative"   # different model/brand: never claim it represents this product
                label = None
        if src:
            shutil.copy(os.path.join(OUT, src + ".webp"), os.path.join(OUT, slug + ".webp"))
            c = {k: v for k, v in allc[src].items() if k not in ("kind", "family")}
            extra[slug] = dict(c, kind=kind, **({"family": label} if kind == "representative" else {}))
            n += 1
            print("reuse", kind, slug, "<-", src)
        else:
            print("still missing", slug)
    json.dump(extra, open(EXTRA, "w"), indent=1)
    print("reused", n)
