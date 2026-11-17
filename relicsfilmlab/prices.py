"""Typical price ranges (USD) shown on product cards and pages.

These are typical *used-market* ranges for working examples (new retail for current
products like film and Instax), not live Amazon prices — every price on the site is
labelled "typical" and points shoppers to Amazon for today's price. Update freely.
"""
import re

# slug (or slug prefix ending in '*') -> (low, high)
MANUAL = {
    # point & shoot
    "olympus-trip-35": (80, 150), "olympus-stylus": (250, 400), "olympus-stylus-epic-dlx-w-panoramic": (250, 400), "olympus-stylus-35-mm-black": (80, 150),
    "olympus-stylus-infinity-mju-35mm-black-amp-silver": (80, 150), "olympus-stylus-epic-zoom-80": (90, 160), "olympus-stylus-epic-zoom-115-deluxe-1": (80, 140),
    "olympus-stylus-zoom-35-70mm": (60, 110), "olympus-stylus-120": (50, 90), "olympus-stylus-zoom-115": (50, 90), "olympus-35-rc": (100, 200),
    "olympus-xa2-2": (80, 150), "olympus-xa2-original-case-a11-electronic-flash": (100, 170), "olympus-pen-ee-1961": (70, 140), "olympus-trip-md3": (30, 60),
    "olympus-trip-af-*": (30, 60), "olympus-quick-shooter*": (25, 50), "olympus-infinity*": (30, 60), "olympus-superzoom-760": (30, 60),
    "contax-t3-like-new": (1200, 1800), "contax-t2": (700, 1100), "canon-af-35-ml": (80, 150), "canon-af-35m": (60, 120), "canon-af35m-ii": (60, 120),
    "canon-sure-shot-owl-date": (50, 100), "canon-canonet-ql-17-giii-1": (150, 280), "canon-canonet-ql-17-n": (100, 180), "canon-canonet-28": (70, 140),
    "canon-canonet-ql-25": (70, 140), "canon-a35-f-40mm-lens": (60, 120), "canon-elph-sport": (25, 50), "nikon-l35-af": (100, 180),
    "nikon-nikonos-iv-a": (150, 300), "yashica-electro-35-*": (80, 160), "yashica-35-me-1973": (50, 100), "minolta-hi-matic-*": (50, 100),
    "point-and-shoot-a-m-minolta-hi-matic-s": (50, 100), "minolta-weathermatic-dual-35": (50, 100), "nishika-n8000-3d-35mm-film-camera": (70, 140),
    "kyocera-samurai-x3-0-red-35mm-half-frame-film-camera": (100, 200), "zeiss-ikon-contessa-lk-1963": (60, 120), "agfa-silette-sl": (40, 80),
    "petri-7s": (40, 90), "minolta-minoltina-p": (50, 100),
    # SLR
    "canon-ae-1": (150, 280), "canon-ae-1-program": (180, 320), "canon-a-1-black-1": (180, 320), "canon-at-1": (80, 150), "canon-av-1": (70, 130),
    "canon-ftb": (80, 160), "canon-tx": (70, 130), "canon-tl": (60, 120), "canon-t50-with-35-70mm-zoom-lens": (50, 100), "canon-t70-1": (60, 120),
    "canon-eos-rebel-xs": (40, 90), "canon-eos-rebel": (30, 70), "minolta-x-700-mps-with-50mm-lens": (120, 220), "minolta-x-370": (60, 120),
    "minolta-xg-*": (60, 120), "minolta-xe-7-with-50mm-lens": (90, 170), "minolta-srt-*": (70, 140), "nikon-f-photomic": (200, 400), "nikon-f-with-lens": (250, 450),
    "nikon-f2-with-50mm-lens": (300, 550), "nikon-fe2": (300, 500), "nikon-fe-black": (150, 260), "nikon-fm-with-50mm-lens": (180, 320), "nikon-em": (70, 130),
    "nikon-fg-*": (70, 140), "nikon-nikomat": (80, 150), "nikon-nikkormat-black-with-24mm-wide-angle-lens": (150, 260), "pentax-k-1000-with-50mm-lens-1": (150, 280),
    "pentax-me-super-with-50mm-lens": (100, 200), "pentax-me": (80, 150), "pentax-mg-with-50mm-lens": (60, 120), "olympus-om-10*": (80, 150),
    "olympus-om-2n": (150, 280), "olympus-om-g": (70, 130), "konica-autoreflex-*": (60, 130), "fuji-fujica-st-605": (50, 100), "ricoh-kr-10m": (50, 100),
    "yashica-j-3": (50, 100), "mamiyasekor-msx-500": (50, 100), "vivitar-v3000s": (40, 80), "petri-flex-*": (40, 90),
    "zeiss-ikon-contaflex-with-original-leather-case1953": (80, 160),
    # instant
    "polaroid-one-step-land-camera": (60, 130), "polaroid-pronto-land-camera": (50, 110), "polaroid-sun-660": (60, 120), "polaroid-job-pro-2": (40, 90),
    "fujifilm-instax-wide-300-instant-film-camera-black-silver": (80, 130), "polaroid-*": (50, 110),
    # medium format
    "hasselblad-500cm": (1200, 2000), "hasselblad-503cx": (1800, 2800), "mamiya-rb67-pro-sd": (400, 700), "mamiya-c330-with-80mm-lens": (300, 500),
    "mamiya-c220-professional": (250, 400), "yashica-mat-124-g": (250, 400), "yashica-a": (120, 220), "fuji-gs645-s": (500, 800), "kiev-6c-with-65mm-lens": (150, 300),
    # movie / pocket / digital
    "canon-514xl-super-8-camera": (120, 250), "canon-310xl-super-8-camera": (100, 220), "chinon-20-p-xl-direct-sound-super-8-camera": (60, 120),
    "bolex-580-super-8-camera": (100, 200), "minolta-110-zoom-date": (80, 160), "pentax-auto-110-film-camera": (100, 200), "kodak-fisher-price": (25, 60),
    "canon-powershot-a550": (40, 80), "sony-handycam-ccd-sc5": (60, 130),
    # lenses & accessories
    "canon-lens-fd-50mm-118-chrome-nose": (40, 80), "canon": (40, 150), "28mm-lens": (40, 100), "28-85mm-lens": (40, 100),
    "35mm-film-canister-*": (8, 20), "fuji-blimp-inflated": (20, 50), "color-film": (10, 18),
}
CATEGORY = {"book": (10, 35), "print": (20, 45), "carprint": (20, 45), "tote": (15, 30), "bag": (25, 60), "strap": (12, 25), "collect": (8, 20), "lens": (40, 120)}

# film & battery shelf: typical new retail per roll / pack
FILM_PRICES = {
    "Kodak Gold 200": (10, 13), "Kodak UltraMax 400": (11, 14), "Kodak Portra 400": (16, 20), "Kodak Ektar 100": (14, 17), "CineStill 800T": (17, 22),
    "Ilford HP5 Plus 400": (9, 12), "Kodak Tri-X 400": (12, 15), "Kodak Portra 400 (120)": (14, 18), "Kodak Ektar 100 (120)": (12, 15), "Ilford HP5 Plus (120)": (8, 11),
    "Polaroid 600 Color": (18, 22), "Polaroid 600 B&W": (18, 22), "Polaroid SX-70 Color": (20, 25), "Polaroid SX-70 B&W": (20, 25),
    "Instax Wide (twin pack)": (18, 25), "Instax Wide Monochrome": (12, 16), "Kodak Vision3 50D Super 8": (40, 55), "Kodak Vision3 200T Super 8": (40, 55),
    "Kodak Vision3 500T Super 8": (40, 55), "Kodak Tri-X Super 8": (45, 55), "Lomography 110 Color": (10, 14), "Kodak FunSaver (disposable)": (16, 22),
    "Fujifilm QuickSnap (disposable)": (15, 20), "Ilford XP2 (disposable)": (14, 18),
    "LR44 / SR44": (5, 8), "CR123A": (8, 14), "CR2": (6, 10), "4LR44 / PX28 6V": (6, 10), "2CR5": (8, 12), "PX625 / MR9 adapter": (25, 35),
}

def _manual(slug):
    if slug in MANUAL:
        return MANUAL[slug]
    for k, v in MANUAL.items():
        if k.endswith("*") and slug.startswith(k[:-1]):
            return v
    return None

def price_range(p):
    """Typical (low, high) USD for a catalogue product, or None (services/workshops)."""
    r = _manual(p["slug"])
    if r:
        return r
    cat, s = p["cat"], (p["spec"] + " " + p["name"]).lower()
    if cat in CATEGORY:
        return CATEGORY[cat]
    if cat == "ps":
        if "rangefinder" in s or "half-frame" in s: return (70, 150)
        if "fixed focus" in s or "focus free" in s or "fixed-focus" in s: return (20, 45)
        if "zoom" in s: return (30, 70)
        return (35, 80)
    if cat == "slr":
        return (40, 90) if "autofocus" in s else (70, 150)
    if cat == "instant":
        return (100, 250) if "sx-70" in s else (50, 110)
    if cat == "mf": return (200, 400)
    if cat == "movie": return (80, 180)
    if cat == "pocket": return (30, 70)
    if cat == "digital": return (40, 90)
    return None

def fmt(r):
    lo, hi = r
    f = lambda v: f"${v:,}"
    return f"{f(lo)}–{f(hi)}"
