#!/usr/bin/env python3
"""Build the Relics Film Lab static site into ./public.

    python3 build.py && python3 validate.py

Every page is written to public/_p/<url-path>.html and served by public/index.php
at its exact old Shopify URL (no trailing slash). See README.md.
"""
import hashlib, html, json, os, re, shutil, urllib.parse
from datetime import date
import sys
import catalog, content as C, pages as PG, guides as GD, tools as TL, prices as PR

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
PDIR = os.path.join(PUB, "_p")
SITE = "https://relicsfilmlab.com"
TODAY = date.today().isoformat()
KW = json.load(open(os.path.join(ROOT, "data", "keywords.json")))
CRED = {}
for _f in ("image_credits_b.json", "image_credits.json", "image_credits_extra.json", "image_credits_site.json"):
    _p = os.path.join(ROOT, "data", _f)
    if os.path.exists(_p):
        CRED.update({k: v for k, v in json.load(open(_p)).items() if not k.startswith("_")})
CRED = {k: v for k, v in CRED.items() if os.path.exists(os.path.join(ROOT, "public", "assets", "img", "site" if k.startswith("site:") else "products", (k[5:] if k.startswith("site:") else k) + ".webp"))}
PRODUCTS = catalog.products()
BY_SLUG = {p["slug"]: p for p in PRODUCTS}
WRITTEN = {}   # url path -> title (for sitemap / validation)
esc = lambda s: html.escape(str(s), quote=True)

# ---------------------------------------------------------------- helpers
# Verified Amazon product matches (query -> ASIN), built from data/amazon_asins.json.
# Anything without a verified match falls back to a tagged Amazon search.
_ASIN_FILE = os.path.join(ROOT, "data", "amazon_asins.json")
ASINS = json.load(open(_ASIN_FILE)) if os.path.exists(_ASIN_FILE) else {}
SLUG_ASIN = {v["for"]: v for v in ASINS.values() if v.get("for")}
# Closest similar model for products whose exact model isn't on Amazon: slug -> {asin, title, note, level}
_SIM_FILE = os.path.join(ROOT, "data", "amazon_similar.json")
SIMILAR = json.load(open(_SIM_FILE)) if os.path.exists(_SIM_FILE) else {}

def amz(q):
    a = ASINS.get(q)
    if a:
        return f"https://www.amazon.com/dp/{a['asin']}?tag={C.AMZ_TAG}"
    return "https://www.amazon.com/s?" + urllib.parse.urlencode({"k": q, "tag": C.AMZ_TAG})

def amz_link(label, q, cls="btn", extra=""):
    return (f'<a class="{cls}" href="{esc(amz(q))}" target="_blank" rel="sponsored nofollow noopener" data-amz="{esc(q)}"{extra}>{label}</a>')

ICON = {
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.3 3 4.5 6.7 4.5c2.1 0 3.6 1.1 5.3 3 1.7-1.9 3.2-3 5.3-3 3.7 0 5.8 3.8 4.3 7.3C19.5 16.4 12 21 12 21z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>',
}

def img_path(key):
    """URL of a local image (product slug or 'site:name'), or None."""
    if key in CRED:
        if key.startswith("site:"):
            return f"/assets/img/site/{key[5:]}.webp"
        return f"/assets/img/products/{key}.webp"
    return None

def site_img(name, fallback="hero"):
    return img_path("site:" + name) or img_path("site:" + fallback) or ""

def credit_html(key):
    c = CRED.get(key)
    if not c:
        return ""
    kind = c.get("kind")
    pre = (f'Representative photo of the {esc(c.get("family", "same"))} line — condition and exact model vary by listing. ' if kind == "representative"
           else "Illustrative photo. " if kind == "illustrative" else "")
    return (pre + f'Photo: <a href="{esc(c["page"])}" target="_blank" rel="noopener nofollow">{esc(c["artist"])}</a>, '
            f'{esc(c["license"])}, via {esc(c["source"])}')

def kws(path, n=8):
    return KW.get(path, {}).get("kws", [])[:n]

def brand_of(p):
    first = p["slug"].split("-")[0]
    if first == "point":
        first = "minolta"
    if first in ("canonn",):
        first = "canon"
    if first == "mamiyasekor":
        first = "mamiya"
    if first.isdigit() or p["cat"] in ("book", "print", "carprint", "tote", "service", "workshop", "film"):
        return None
    return C.BRANDS.get(first, (first.title(), ""))

def film_kind(p):
    s = (p["spec"] + " " + p["name"]).lower()
    if "sx-70" in s: return "sx70"
    if "instax" in s: return "instax"
    if "aps" in s.split() or "(aps)" in s: return "aps"
    if p["cat"] == "instant": return "600"
    if p["cat"] == "mf": return "120"
    if p["cat"] == "movie": return "super8"
    if p["cat"] == "pocket": return "110"
    if p["cat"] == "digital": return "digital"
    if p["cat"] in ("ps", "slr"): return "35mm"
    return None

FORMAT_KEY = {"sx70": "instant", "600": "instant", "instax": "instant", "120": "120", "super8": "super8", "110": "110", "digital": "digital", "35mm": "35mm", "aps": "aps"}

def amz_query(p):
    n = re.sub(r"\(.*?\)", "", p["name"]).strip()
    n = re.sub(r"\s+with\s+.*$", "", n, flags=re.I).strip()
    cat = p["cat"]
    if cat in ("ps", "slr", "mf", "pocket"):
        return n + " film camera"
    if cat == "instant":
        return n if "camera" in n.lower() else n + " camera"
    if cat == "movie":
        return n
    if cat == "book":
        return n + " book"
    if cat in ("print", "carprint"):
        return re.sub(r"\s*Print$", "", n) + " poster"
    if cat == "lens" and p["slug"] == "canon":
        return "Canon FD lens"
    return n

def rank_of(p):
    return -KW.get("/products/" + p["slug"], {}).get("traffic", 0)

# ---------------------------------------------------------------- layout
# Top-level shop navigation (shopping first; film-lab/repair/guide pages live in the footer)
NAV_MAIN = [("/collections/point-shoot-cameras", "Point &amp; Shoot", "ps"), ("/collections/slr-cameras", "SLR", "slr"),
            ("/collections/polaroid-cameras", "Instant", "instant"), ("/collections/medium-format-cameras", "Medium Format", "mf"),
            ("/collections/super-8-collections", "Super 8", "super8"), ("/collections/film", "Film", "film"),
            ("/collections/accessories", "Accessories", "acc"), ("/collections/gift-guide", "Gifts", "gifts"), ("/tools", "Tools", "tools")]
NAV_MEGA = [
    ("Cameras", [("/collections/all-film-cameras", "All Film Cameras", "Every camera we cover", False),
                 ("/collections/point-shoot-cameras", "Point &amp; Shoot", "Pocket 35mm compacts", True),
                 ("/collections/slr-cameras", "SLR Cameras", "35mm, manual &amp; auto", True),
                 ("/collections/polaroid-cameras", "Polaroid &amp; Instant", "Land, 600 &amp; Instax", True),
                 ("/collections/medium-format-cameras", "Medium Format", "120 film TLRs &amp; SLRs", True),
                 ("/collections/super-8-collections", "Super 8 Cameras", "Home-movie magic", True)]),
    ("Film &amp; Gear", [("/collections/film", "Film &amp; Batteries", "35mm, 120, instant, Super 8", True),
                         ("/collections/accessories", "Lenses &amp; Accessories", "Bags, straps, glass", True),
                         ("/collections/film-lab", "Developing &amp; Scanning", "Home lab kits &amp; scanners", False),
                         ("/tools", "Film Tools", "Calculators &amp; camera finder", True)]),
    ("Gifts &amp; Wall Art", [("/collections/gift-guide", "Gift Guide", "For the film-obsessed", True),
                              ("/collections/prints", "Ready-to-Hang Prints", "Wall art &amp; totes", False),
                              ("/collections/car-collection", "Car Prints", "Porsche, rally &amp; more", False),
                              ("/collections/books", "Photo Books", "Technique &amp; monographs", False),
                              ("/collections/all", "Shop Everything", "The full catalogue", False)]),
]

def header(active=""):
    mega = "".join(f'<div class="mega__col"><div class="mega__h">{h}</div>' + "".join(
        f'<a href="{u}"{" class=dup" if dup else ""}>{t}<small>{d}</small></a>' for u, t, d, dup in links) + "</div>" for h, links in NAV_MEGA)
    items = "".join(f'<li><a href="{u}"{" class=is-active" if active == k else ""}>{t}</a></li>' for u, t, k in NAV_MAIN)
    return f"""<div class="ticker" aria-hidden="true"><div class="ticker__track">{"".join(f"<span>{t}</span>" for t in ["Curated film cameras", "Real buying advice", "Secure checkout", "Free film tools", "Long Beach born", "New picks every month"] * 4)}</div></div>
<header class="hdr"><div class="wrap hdr__in">
<a class="logo" href="/" aria-label="Relics Film Lab home"><span class="logo__mark" aria-hidden="true"></span>Relics<small>FILM LAB</small></a>
<ul class="nav" id="nav">
<li class="nav__mega"><button aria-haspopup="true">Shop all ▾</button><div class="nav__drop mega">{mega}</div></li>
{items}
<li class="nav__m nav__m--all"><a href="/collections/all">Shop all →</a></li>
<li class="nav__more"><a href="/collections/all-film-cameras">All cameras</a><a href="/collections/prints">Prints</a><a href="/collections/books">Books</a><a href="/blogs/guides">Guides</a></li>
</ul>
<div class="hdr__tools">
<button class="icon-btn js-search" aria-label="Search the shop">{ICON["search"]}</button>
<a class="icon-btn" href="/pages/wishlist" aria-label="Wishlist">{ICON["heart"]}<span class="badge js-wl-count"></span></a>
<button class="icon-btn burger" aria-label="Menu" aria-controls="nav" aria-expanded="false">{ICON["menu"]}</button>
</div></div></header>"""

def footer():
    cols = [("Shop", [("/collections/point-shoot-cameras", "Point &amp; Shoots"), ("/collections/slr-cameras", "SLR Cameras"), ("/collections/polaroid-cameras", "Polaroid &amp; Instant"),
                       ("/collections/medium-format-cameras", "Medium Format"), ("/collections/super-8-collections", "Super 8 Cameras"), ("/collections/film", "Film &amp; Batteries"),
                       ("/collections/accessories", "Accessories"), ("/collections/prints", "Prints"), ("/collections/books", "Photo Books"), ("/collections/gift-guide", "Gift Guide"), ("/collections/all", "Shop All")]),
            ("Tools", [("/tools/camera-finder", "Camera Finder"), ("/tools/exposure-calculator", "Exposure Calculator"), ("/tools/film-stock-finder", "Film Stock Finder"),
                       ("/tools/battery-finder", "Battery Finder"), ("/tools/cost-per-shot-calculator", "Cost per Shot"), ("/tools/depth-of-field-calculator", "Depth of Field"),
                       ("/tools/super-8-calculator", "Super 8 Calculator")]),
            ("Film Lab", [("/collections/film-lab", "The Film Lab"), ("/film-services", "Film Services"), ("/order-now", "Where to Develop Film"), ("/products/develop-only", "Develop Only"),
                          ("/products/scan-only", "Scan Only"), ("/camera-repairs", "Camera Repairs"), ("/pages/basic-camera-cleaning", "Camera Cleaning"), ("/blogs/guides", "Guides")]),
            ("Relics", [("/pages/the-relics-standard", "Why Relics?"), ("/pages/about-us", "About Us"), ("/pages/faqs", "FAQs"),
                        ("/pages/contact", "Contact"), ("/pages/store-help", "Store Help")])]
    cols_html = "".join(f'<div><h4>{h}</h4><ul>{"".join(f"<li><a href={u!r}>{t}</a></li>" for u, t in links)}</ul></div>' for h, links in cols)
    return f"""<footer class="ftr"><div class="wrap">
<div class="ftr__big" aria-hidden="true">Relics Film Lab</div>
<div class="ftr__grid">
<div><a class="logo" href="/"><span class="logo__mark" aria-hidden="true"></span>Relics<small>FILM LAB</small></a>
<p class="muted" style="margin-top:16px;max-width:36ch">Film cameras, film and lab gear — curated by people who have loaded, shot, developed and repaired thousands of them.</p>
<p><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
<p class="disclosure">As an Amazon Associate, Relics Film Lab earns from qualifying purchases. Orders are placed and fulfilled on Amazon; prices and availability are set there.</p></div>
{cols_html}</div>
<div class="ftr__legal"><span>© {date.today().year} Relics Film Lab</span>
<span><a href="/pages/affiliate-disclosure">Affiliate Disclosure</a> · <a href="/pages/returns-exchanges">Returns</a> · <a href="/pages/privacy-policy">Privacy</a> · <a href="/pages/terms-of-service">Terms</a> · <a href="/pages/photo-credits">Photo Credits</a> · <a href="/sitemap">Sitemap</a></span></div>
</div></footer>
<div class="search" role="dialog" aria-label="Search"><div class="search__box"><input type="search" placeholder="Search cameras, film, books…" aria-label="Search"><div class="search__res"></div><p class="muted mono" style="margin-top:18px">Esc to close · / to open</p></div></div>
<div class="grain" aria-hidden="true"></div>"""

CSS_V = JS_V = "1"

def layout(path, title, desc, body, schema=None, active="", preload=None, ogimg=None, robots="index,follow", scripts=None):
    canonical = SITE + (path if path != "/" else "/")
    full_title = title if "Relics" in title else f"{title} | Relics Film Lab"
    og = SITE + (ogimg or site_img("hero"))
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Relics Film Lab">
<meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d0c0b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
{pre}
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
{ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/site.js?v={JS_V}" defer></script>{"".join(f'<script src="{u}?v={JS_V}" defer></script>' for u in (scripts or []))}
</body></html>
"""

def write(path, title, desc, body, **kw):
    f = "home" if path == "/" else path.lstrip("/")
    out = os.path.join(PDIR, f + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        fh.write(layout(path, title, desc, body, **kw))
    WRITTEN[path] = title

def crumbs(items):
    """items: list of (url, label); last is current page."""
    h = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a>'
    for u, l in items:
        h += f'<span>/</span>' + (f'<a href="{u}">{l}</a>' if u else f'<span aria-current="page">{l}</span>')
    h += "</nav>"
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement":
          [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}] +
          [{"@type": "ListItem", "position": i + 2, "name": re.sub("<.*?>", "", html.unescape(l)), **({"item": SITE + u} if u else {})} for i, (u, l) in enumerate(items)]}
    return h, ld

def faq_html(items):
    h = '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in items) + "</div>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<.*?>", "", a)}} for q, a in items]}
    return h, ld

def phero(title_html, lead, crumbs_html, img=None):
    im = f'<div class="phero__img"><img src="{img}" alt="" fetchpriority="high"></div>' if img else ""
    return f'<section class="phero">{im}<div class="wrap">{crumbs_html}<h1>{title_html}</h1>{f"<p class=lead>{lead}</p>" if lead else ""}</div></section>'

def product_card(p, i=0):
    im = img_path(p["slug"])
    b = brand_of(p)
    label = catalog.CATEGORIES[p["cat"]][0]
    kind = CRED.get(p["slug"], {}).get("kind")
    alt = p["name"] + (" — representative photo" if kind == "representative" else "") if kind != "illustrative" else ""
    media = (f'<img src="{im}" alt="{esc(alt)}" loading="lazy" width="500" height="500">' if im
             else f'<div class="ph">{esc(p["name"])}</div>')
    pr = PR.price_range(p)
    price_html = f'<span class="card__price">{PR.fmt(pr)}<small>typical price</small></span>' if pr else '<span class="card__price card__price--na">See guide</span>'
    return f"""<article class="card reveal" data-brand="{esc(b[0] if b else 'Other')}" data-name="{esc(p['name'])}" data-year="{esc(re.sub(r'[^0-9]', '', p['year'])[:4])}" data-rank="{i}" data-price="{pr[0] if pr else 99999}">
<div class="card__img">{media}<span class="card__tag">{label}</span></div>
<div class="card__body"><h3 class="card__title"><a href="/products/{p['slug']}">{esc(p['name'])}</a></h3>
<div class="card__spec">{esc(p['spec'])}</div>
<div class="card__foot">{price_html}<button class="heart" data-slug="{p['slug']}" aria-label="Save {esc(p['name'])} to wishlist" aria-pressed="false">{ICON['heart']}</button></div></div></article>"""

def grid(items, filters=True):
    items = sorted(items, key=rank_of)
    tb = ""
    if filters and len(items) > 6:
        brands = sorted({(brand_of(p) or ("Other",))[0] for p in items})
        counts = {}
        for p in items:
            k = (brand_of(p) or ("Other",))[0]; counts[k] = counts.get(k, 0) + 1
        chips = ""
        brand_sel = ""
        if len(brands) > 1:
            chips = '<div class="chips"><button class="chip is-on" data-brand="all">All</button>' + "".join(f'<button class="chip" data-brand="{esc(b)}">{esc(b)}</button>' for b in brands) + "</div>"
            brand_sel = (f'<label class="fsel"><span>Brand</span><select id="brand" aria-label="Filter by brand"><option value="all">All brands ({len(items)})</option>'
                         + "".join(f'<option value="{esc(b)}">{esc(b)} ({counts[b]})</option>' for b in brands) + "</select></label>")
        tb = f"""<div class="toolbar">{chips}{brand_sel}<label class="fsel fsel--sort"><span>Sort</span><select id="sort" aria-label="Sort"><option value="pop">Most popular</option><option value="az">A–Z</option><option value="za">Z–A</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option><option value="old">Oldest first</option><option value="new">Newest first</option></select></label><span class="count"></span></div>"""
    return tb + '<div class="grid" id="pgrid">' + "".join(product_card(p, i) for i, p in enumerate(items)) + "</div>"

# ---------------------------------------------------------------- product pages
def why_points(p):
    s = p["spec"].lower(); n = p["name"]; pts = []
    if "autofocus" in s: pts.append("Autofocus and automatic exposure — you frame, it does the rest, so it is easy to hand to friends at a party.")
    if "zoom" in s and p["cat"] == "ps": pts.append("A zoom lens covers wide group shots and tighter portraits without changing position.")
    if re.search(r"f/1\.[0-9]", s): pts.append("A genuinely fast lens for its class, which means cleaner low-light shots and softer backgrounds.")
    if "weatherproof" in s or "waterproof" in s or "underwater" in s: pts.append("Sealed against splashes and weather, so it can go to the beach, the pool party or the hike.")
    if "mechanical" in s: pts.append("Mechanical controls teach you exposure properly — aperture, shutter speed and focus are all yours.")
    elif "manual" in s: pts.append("Full manual control is there whenever you want to take over from the automation.")
    if "program" in s: pts.append("A Program mode for quick shooting, with manual control available whenever you want it.")
    if "aperture-priority" in s: pts.append("Aperture-priority auto exposure: choose your depth of field and the camera picks the shutter speed.")
    if "shutter-priority" in s: pts.append("Shutter-priority auto exposure keeps motion sharp while the camera handles the aperture.")
    if "selenium" in s or "no batteries" in s: pts.append("A selenium light meter that needs no battery at all — it will keep working decades from now.")
    if "half-frame" in s: pts.append("Half-frame format doubles the shots per roll — 72 photos on a 36-exposure roll — and invites diptychs.")
    if "rangefinder" in s: pts.append("Rangefinder focusing is quick and precise, and the quiet leaf shutter is great for street photography.")
    if "tlr" in s: pts.append("Waist-level viewing on a big, bright ground glass slows you down in the best way.")
    if "titanium" in s or "zeiss" in s: pts.append("Carl Zeiss optics and premium build that still compare favourably with modern cameras.")
    if "mount" in s and p["cat"] == "slr": pts.append(f"An interchangeable-lens system with plenty of affordable used lenses to grow into.")
    if "panorama" in s: pts.append("A built-in panorama mode for wide, cinematic frames.")
    if p["cat"] == "instant": pts.append("One-of-a-kind prints in your hand within minutes — nothing beats it at parties and weddings.")
    if p["cat"] == "movie": pts.append("Real film motion with the grain, colour and flicker that digital filters only imitate.")
    if p["cat"] == "mf": pts.append("A big 120 negative delivers smooth tones and detail no 35mm camera can match.")
    if p["cat"] == "pocket": pts.append("Tiny, light and fun — 110 cameras are the original pocket cameras.")
    if not pts or len(pts) < 3:
        pts += ["Simple controls — there is very little to go wrong and very little to learn.",
                "Affordable enough that you can take it anywhere without worrying.",
                "The slightly imperfect, nostalgic look that people search for on film."][: 3 - len(pts)]
    return pts[:5]

def who_for(p):
    return {
        "ps": "first-time film shooters, travellers and anyone who wants a camera that lives in a jacket pocket",
        "slr": "anyone learning photography properly, students and shooters who want full manual control and interchangeable lenses",
        "instant": "parties, weddings, guest books and anyone who loves holding a photo seconds after taking it",
        "mf": "portrait, landscape and fine-art photographers who want the most out of every frame",
        "movie": "filmmakers, music-video directors and couples who want their wedding on real film",
        "pocket": "collectors and anyone after a lo-fi, retro look",
        "digital": "anyone chasing the early-2000s digicam and camcorder look",
    }.get(p["cat"], "film photographers")

def product_page(p):
    slug, name, cat = p["slug"], p["name"], p["cat"]
    path = "/products/" + slug
    catlabel, colslug = catalog.CATEGORIES[cat][0], catalog.CATEGORIES[cat][1]
    col = C.COLLECTIONS.get(colslug, {})
    b = brand_of(p)
    brand = b[0] if b else ""
    special = PG.SPECIAL_PRODUCTS.get(slug)
    q = amz_query(p)
    kwlist = [k for k, v, pos in kws(path, 10)]
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    GENERIC = {"camera", "cameras", "film", "35mm", "35", "mm", "vintage", "price", "prices", "for", "sale", "review", "slr", "point", "and", "shoot",
               "instant", "lens", "movie", "super", "8", "the", "a", "used", "buy", "old", "zoom", "date", "black", "silver"}
    nn = norm(name)
    aliases = []
    for k in kwlist:
        toks = [norm(t) for t in re.split(r"[\s/]+", k) if norm(t) and t.lower() not in GENERIC]
        if not toks or not all(t in nn for t in toks):
            continue
        if norm(k) not in nn and all(norm(k) != norm(a) for a in aliases) and len(aliases) < 4:
            aliases.append(k)
    fk = film_kind(p)
    fmt_label = {"35mm": "35mm film", "120": "120 medium format film", "600": "Polaroid 600 film", "sx70": "Polaroid SX-70 film", "instax": "Instax Wide film",
                 "super8": "Super 8 cartridges", "110": "110 film", "digital": "digital", "aps": "APS film"}.get(fk, "")
    im = img_path(slug)
    if not im:
        im_fallback = {"book": "books", "print": "prints", "tote": "prints", "carprint": "cars", "bag": "accessories", "strap": "accessories", "collect": "film-rolls",
                       "service": "negatives", "workshop": "workshop", "film": "film-rolls", "lens": "lens", "digital": "point-shoot", "ps": "point-shoot", "slr": "slr",
                       "instant": "polaroids", "mf": "medium-format", "movie": "super8", "pocket": "point-shoot"}.get(cat, "hero")
        im_site = site_img(im_fallback)
    _k = CRED.get(slug, {}).get("kind")
    _alt = "" if _k == "illustrative" else name + (" — representative photo" if _k == "representative" else "")
    media = (f'<img src="{im}" alt="{esc(_alt)}" width="1000" height="1000" fetchpriority="high">' if im
             else (f'<img src="{im_site}" alt="" style="opacity:.35" fetchpriority="high"><div class="ph">{esc(name)}</div>' if im_site else f'<div class="ph">{esc(name)}</div>'))
    credit = credit_html(slug) if im else ("Illustrative photo. " + credit_html("site:" + im_fallback) if im_site else "")
    chips = "".join(f"<span>{esc(x.strip())}</span>" for x in p["spec"].split("·") if x.strip())
    if p["year"]:
        chips = f"<span>{esc(p['year'])}</span>" + chips

    # intro
    if special:
        intro = special["intro"]
    elif p["blurb"]:
        intro = esc(p["blurb"])
    else:
        y = p["year"]
        era = (f" from the {y}" if y.endswith("s") else f" from {y}") if y and y[0].isdigit() else ""
        closers = ["It is exactly the kind of honest, well-made film camera we love to recommend.",
                   "Cameras like this are why so many people fall for film — simple, capable and full of character.",
                   "It's an easy, affordable way into film photography that still makes lovely pictures.",
                   "Find a clean copy and it will happily shoot roll after roll.",
                   "It remains a smart buy for anyone who wants real film results without fuss."]
        closer = closers[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(closers)]
        if cat in ("ps", "slr", "mf", "movie", "pocket", "instant", "digital"):
            intro = (f"The {esc(name)} is a {esc(catlabel.lower())}{esc(era)}"
                     + (f" by {esc(brand)}" if brand and not name.lower().startswith(brand.lower()) else "")
                     + f" — {esc(p['spec'].replace(' · ', ', '))}. {closer}")
        elif cat == "book":
            intro = f"<em>{esc(name)}</em> is one of the photography books we kept on the shelf at Relics — the kind you return to for ideas, technique and inspiration."
        elif cat in ("print", "carprint"):
            intro = f"The {esc(name)} brings a classic photograph to your wall. Choose a poster or framed print in the size that suits your space."
        elif cat == "tote":
            intro = f"The {esc(name)} is a sturdy canvas tote printed with a classic photograph — big enough for a camera, a few rolls of film and a book."
        else:
            intro = f"The {esc(name)} — {esc(p['spec'])}. A small upgrade that makes shooting film more enjoyable."

    is_cam = cat in ("ps", "slr", "instant", "mf", "movie", "pocket", "digital")
    # buybox
    _bq = special['q'] if special else q
    if slug in SLUG_ASIN:            # matched by product, independent of the query wording
        ASINS[_bq] = SLUG_ASIN[slug]
    btn_label = ("Buy on Amazon" if _bq in ASINS else "See all listings on Amazon") if not special else (
        "Buy on Amazon" if _bq in ASINS else special.get("btn", "Shop on Amazon"))
    sim = SIMILAR.get(slug) if slug not in SLUG_ASIN else None
    if sim:
        sim_url = f"https://www.amazon.com/dp/{sim['asin']}?tag={C.AMZ_TAG}"
        rel_txt = {"series": "from the same series", "brand": f"from {esc(brand) or 'the same maker'}", "comparable": "a comparable model"}.get(sim.get("level"), "a similar model")
        if sim.get("level") == "film":
            sim_msg = (f'<b>No Super 8 cameras are listed on Amazon right now.</b> Already have a camera, or found one elsewhere? '
                       f'This links to the film it shoots: {esc(sim["note"])}.')
            sim_btn = "Shop Super 8 film on Amazon"
        else:
            sim_msg = f'<b>This exact model isn\'t on Amazon right now.</b> Closest match ({rel_txt}): {esc(sim["note"])}.'
            sim_btn = "Shop the closest match on Amazon"
        buy_row = (f'<div class="buybox__sim">{sim_msg}</div>'
                   f'<div class="buybox__row"><a class="btn btn--block" href="{esc(sim_url)}" target="_blank" rel="sponsored nofollow noopener" data-amz="{esc(sim["asin"])}">{ICON["cart"]} {sim_btn}</a></div>'
                   f'<p class="buybox__alt">Prefer the exact model? {amz_link("Search Amazon for the " + esc(name) + " →", _bq, "")}</p>')
    else:
        buy_row = f'<div class="buybox__row">{amz_link(ICON["cart"] + " " + btn_label, _bq, "btn btn--block")}</div>'
    _pr = PR.price_range(p)
    price_box = (f'<div class="buybox__price"><span>Typical price</span><b>{PR.fmt(_pr)}</b>'
                 f'<small>{"Typical new price" if slug.startswith("fujifilm-instax") or cat in ("book", "print", "carprint", "tote", "bag", "strap", "collect", "film") else "Typical used price for a working example"} — prices change, so check Amazon for today\'s price.</small></div>') if _pr else ""
    buy = f"""<div class="buybox">
{price_box}<div class="mono muted">Available from independent sellers on Amazon</div>
{buy_row}
<div class="buybox__row"><button class="heart" data-slug="{slug}" aria-pressed="false">{ICON['heart']} Save to wishlist</button></div>
<p class="buybox__note">We link to live Amazon listings so you always see current prices, condition and seller ratings. Relics earns a small commission at no extra cost to you.</p>
<div class="trust"><div><b>Checkout</b>Secure on Amazon</div><div><b>Returns</b>Amazon return policy</div><div><b>Advice</b>Written by film shooters</div></div>
</div>"""
    alias_html = f'<p class="aliases">Also searched as: {", ".join(esc(a) for a in aliases)}</p>' if aliases and is_cam else ""

    # body sections
    sec = []
    if special:
        sec.append(special["body"])
    elif is_cam:
        sec.append(f"<h2>Why we rate the {esc(name)}</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in why_points(p)) + "</ul>")
        sec.append(f"<p>It is a great fit for {who_for(p)}.</p>")
        if b and b[1]:
            sec.append(f"<h3>About {esc(brand)}</h3><p>{esc(b[1])}</p>")
        ck = C.CHECKS.get(cat if cat in C.CHECKS else "ps")
        sec.append(f"<h2>Buying a used {esc(name)}: what to check</h2><p>Most listings on Amazon come from independent sellers, and condition varies. Read the description and seller rating, and when it arrives:</p><ol>"
                   + "".join(f"<li>{esc(x)}</li>" for x in ck) + "</ol>"
                   + "<p>Buying through Amazon means you are covered by its A-to-z Guarantee if a camera doesn't arrive as described.</p>")
        ff = C.FAQ_FORMAT.get(FORMAT_KEY.get(fk, "35mm"), "")
        bat = C.BATTERIES.get(slug)
        bat_txt = ("It needs no battery for its exposure system." if bat == "none" else
                   f"It uses {C.BATTERY_PHRASE[bat]}." if bat else "Check the battery compartment before buying — most cameras of this type use a common lithium, alkaline or silver-oxide cell that is easy to find.")
        if fk in ("600",):
            bat_txt = "No separate battery is needed: Polaroid 600 film packs contain the battery that powers the camera."
        sec.append(f"<h2>Film &amp; batteries</h2><p>{ff} {bat_txt}</p>")
        rows = [("Brand", brand or "—"), ("Model", name), ("Type", catlabel), ("Format", fmt_label or "—"), ("Introduced", p["year"] or "—"),
                ("Key features", p["spec"].replace(" · ", ", ")), ("Batteries", (C.BATTERY_KIT[bat][0] if bat and bat != "none" else "None needed" if bat == "none" else "See battery door"))]
        sec.append('<h2>Specifications</h2><table class="spec-table">' + "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in rows) + "</table>")
    elif cat == "book":
        sec.append(f"<h2>Why it belongs on your shelf</h2><p>Photography books teach in a way videos can't: you can sit with a picture, study the light and come back to it next year with fresh eyes. We recommend <em>{esc(name)}</em> to anyone who wants to look harder and shoot better.</p>"
                   "<h3>Buying used photo books</h3><ul><li>Check the edition and whether it is hardcover or paperback.</li><li>Ask the seller about dust jackets, writing and water damage.</li><li>Out-of-print titles are often far cheaper used than new — compare a few listings.</li></ul>")
    elif cat in ("print", "carprint", "tote"):
        sec.append("<h2>Choosing a print</h2><ul><li>Measure your wall first — prints look best when they fill around two-thirds of the space above furniture.</li>"
                   "<li>A matte paper reduces glare; a gloss paper makes colours pop.</li><li>A simple black or natural-wood frame suits almost every photograph.</li></ul>"
                   "<p>Browse current posters, canvases and framed versions on Amazon — sizes and finishes vary by seller.</p>")
    else:
        sec.append(f"<h2>What to look for</h2><ul><li>Check compatibility with your camera body, mount or bag size.</li><li>Read recent reviews for build quality.</li><li>Vintage items vary in condition — look closely at photos and seller ratings.</li></ul>")

    # FAQ
    faqs = []
    if special and special.get("faq"):
        faqs = special["faq"]
    elif is_cam:
        faqs.append((f"What film does the {name} take?", C.FAQ_FORMAT.get(FORMAT_KEY.get(fk, "35mm"), "")))
        bat = C.BATTERIES.get(slug)
        if bat or fk == "600":
            faqs.append((f"Does the {name} need batteries?", "No — Polaroid 600 film packs contain their own battery." if fk == "600" else
                         ("No. Its exposure system needs no battery." if bat == "none" else f"Yes, it uses {C.BATTERY_PHRASE[bat]}.")))
        faqs.append((f"Is the {name} good for beginners?",
                     {"slr": "Yes. A manual-focus SLR is the classic way to learn exposure, and this one is simple to operate. Start with a 400-speed film for flexibility.",
                      "ps": "Very. Compacts like this handle focus and exposure for you — just load the film and shoot.",
                      "instant": "Yes — instant cameras are about as simple as photography gets. Keep fresh film out of the heat and shield prints from light as they develop.",
                      "mf": "It's a rewarding step up once you understand exposure. Medium format slows you down and rewards careful composition.",
                      "movie": "Yes, if you can use a camcorder you can shoot Super 8. Use the built-in meter and keep shots short — a 50ft cartridge lasts about 3 minutes at 18fps.",
                      }.get(cat, "Yes — it is straightforward to use.")))
        faqs.append(("Where can I get my film developed?", 'Any lab that processes the format will do — see our guide to <a href="/order-now">where to develop film</a>, or learn to <a href="/blogs/guides/how-to-develop-film-at-home">develop film at home</a>.'))
        _sim = SIMILAR.get(slug) if slug not in SLUG_ASIN else None
        faqs.append((f"Where can I buy a {name}?",
                     (f'Super 8 cameras aren\'t listed on Amazon right now, so our button links to the film it shoots ({esc(_sim["note"])}). The link under it searches Amazon for the {esc(name)} itself — sellers list vintage Super 8 cameras from time to time — and specialist used-camera shops and auction sites usually have copies.') if _sim and _sim.get("level") == "film" else
                     (f'The {esc(name)} isn\'t listed on Amazon right now, so our button links to the closest match we found — {esc(_sim["note"])} — and the link under it searches Amazon for the {esc(name)} itself, as independent sellers list copies from time to time.') if _sim else
                     f'Vintage cameras are sold by independent sellers on Amazon. Use the “Buy on Amazon” button above to see the current listing, price and condition for the {esc(name)}.'))
    faq_h, faq_ld = faq_html(faqs) if faqs else ("", None)

    # kit (aside)
    kit = []
    if fk and fk in C.FILM_KITS:
        kit += C.FILM_KITS[fk]
    bat = C.BATTERIES.get(slug)
    if bat and bat != "none" and C.BATTERY_KIT.get(bat):
        kit.append(C.BATTERY_KIT[bat])
    if special and special.get("kit"):
        kit = special["kit"]
    if is_cam:
        kit += C.CARE_KIT[:2]
    aside = ""
    if kit:
        aside = ('<aside><div class="aside-card"><div class="eyebrow">Shoot it with</div><h3>The kit we\'d add</h3><div class="kit">'
                 + "".join(amz_link(f"{esc(l)} <span>Amazon →</span>", qq, "") for l, qq in kit[:7]) + "</div>"
                 + '<p class="buybox__note">Affiliate links — we earn from qualifying purchases.</p></div></aside>')

    # related
    rel = [x for x in PRODUCTS if x["cat"] == cat and x["slug"] != slug]
    if b:
        rel.sort(key=lambda x: (0 if brand_of(x) and brand_of(x)[0] == brand else 1, rank_of(x)))
    else:
        rel.sort(key=rank_of)
    rel = rel[:4]

    cr_h, cr_ld = crumbs([(f"/collections/{colslug}", col.get("h1", catlabel).replace("<em>", "").replace("</em>", "")), (None, esc(name))])
    title_core = name
    top = kwlist[0] if kwlist else ""
    meta_title = f"{name} — {catlabel}" if len(name) < 40 else name
    desc = (f"{re.sub('<.*?>', '', html.unescape(intro))[:120].rstrip()}… Specs, film, buying checklist and current deals on Amazon.")
    if top and norm(top) not in norm(desc):
        desc = f"{name}: {re.sub('<.*?>', '', html.unescape(intro))[:100].rstrip()}… Specs, film & where to buy ({top})."
    body = f"""<div class="wrap">{cr_h}
<section class="pdp">
<div class="pdp__media reveal"><div class="pdp__frame">{media}</div><p class="pdp__credit">{credit}</p></div>
<div class="pdp__info">
<div class="eyebrow">{esc(catlabel)}{(" · " + esc(brand)) if brand else ""}</div>
<h1>{esc(title_core)}</h1>
{f'<div class="pdp__mprice"><b>{PR.fmt(_pr)}</b><span>typical price</span></div>' if _pr else ""}
<div class="specline">{chips}</div>
<p class="lede">{intro}</p>
{alias_html}
{buy}
</div></section>
<section class="pdp-body"><div class="prose">{''.join(sec)}<h2>FAQ</h2>{faq_h}</div>{aside}</section>
{f'<section class="section" style="padding-top:20px"><div class="head-row"><h2>You might also like</h2><a class="btn btn--ghost btn--sm" href="/collections/{colslug}">See all {re.sub("<.*?>", "", col.get("h1", catlabel + "s")).replace("&amp;", "&")}</a></div><div class="grid">' + "".join(product_card(x, i) for i, x in enumerate(rel)) + "</div></section>" if rel else ""}
</div>"""
    schema = [cr_ld] + ([faq_ld] if faq_ld else [])
    write(path, meta_title, desc, body, schema=schema, preload=im, ogimg=im)

# ---------------------------------------------------------------- collections
def collection_page(slug, c):
    path = "/collections/" + slug
    if c.get("gift"):
        picks = [BY_SLUG[s] for s in PG.GIFT_PICKS if s in BY_SLUG]
        items_html = grid(picks, filters=False)
    else:
        items = [p for p in PRODUCTS if (c["cats"] is None or p["cat"] in c["cats"])]
        if c.get("filt"):
            items = [p for p in items if c["filt"] in p["slug"] or c["filt"] in p["name"].lower()]
        items_html = grid(items)
    plain = re.sub("<.*?>", "", html.unescape(c["h1"]))
    cr_h, cr_ld = crumbs([("/collections/all", "Shop"), (None, esc(plain))]) if slug != "all" else crumbs([(None, "Shop")])
    extra = PG.COLLECTION_EXTRA.get(slug, {})
    faq_h, faq_ld = faq_html(extra["faq"]) if extra.get("faq") else ("", None)
    body = (phero(c["h1"], c["intro"], cr_h, site_img(c["img"]))
            + f'<section class="section" style="padding-top:48px"><div class="wrap">{extra.get("top", "")}{items_html}</div></section>'
            + (f'<section class="section" style="padding-top:0"><div class="wrap prose">{extra.get("body", "")}{("<h2>FAQ</h2>" + faq_h) if faq_h else ""}</div></section>' if extra else ""))
    schema = [cr_ld] + ([faq_ld] if faq_ld else [])
    write(path, c["title"], c["desc"], body, schema=schema, preload=site_img(c["img"]), ogimg=site_img(c["img"]))

# ---------------------------------------------------------------- run
def main():
    global CSS_V, JS_V
    if os.path.exists(PDIR):
        shutil.rmtree(PDIR)
    os.makedirs(os.path.join(PUB, "assets"), exist_ok=True)
    for f in ("site.css", "site.js", "tools.js"):
        src = open(os.path.join(ROOT, "src", f)).read()
        open(os.path.join(PUB, "assets", f), "w").write(src)
    CSS_V = hashlib.md5(open(os.path.join(PUB, "assets", "site.css"), "rb").read()).hexdigest()[:8]
    JS_V = hashlib.md5(open(os.path.join(PUB, "assets", "site.js"), "rb").read()).hexdigest()[:8]

    ctx = dict(PRODUCTS=PRODUCTS, BY_SLUG=BY_SLUG, write=write, crumbs=crumbs, faq_html=faq_html, phero=phero, grid=grid, product_card=product_card,
               site_img=site_img, img_path=img_path, amz_link=amz_link, amz=amz, ICON=ICON, esc=esc, KW=KW, CRED=CRED, rank_of=rank_of, SITE=SITE, TODAY=TODAY, credit_html=credit_html)
    for p in PRODUCTS:
        product_page(p)
    for slug, c in C.COLLECTIONS.items():
        collection_page(slug, c)
    PG.build_pages(ctx)
    GD.build_guides(ctx)
    ctx["build"] = sys.modules[__name__]
    TL.build_film_page(ctx)
    TL.build_tools(ctx)
    PG.build_home(ctx)
    PG.build_sitemap_page(ctx, WRITTEN)

    # search index
    idx = [dict(s=p["slug"], n=p["name"], c=catalog.CATEGORIES[p["cat"]][0], u="/products/" + p["slug"], i=img_path(p["slug"]) or "",
                k=" ".join(k for k, v, pos in kws("/products/" + p["slug"], 4))) for p in sorted(PRODUCTS, key=rank_of)]
    idx += [dict(s="", n=re.sub("<.*?>", "", html.unescape(c["h1"])), c="Collection", u="/collections/" + s, i="") for s, c in C.COLLECTIONS.items()]
    idx += [dict(s="", n="Film & Batteries", c="Collection", u="/collections/film", i="", k="35mm 120 polaroid instax super 8 film battery")]
    idx += [dict(s="", n=t, c="Tool", u="/tools/" + s, i="", k=sh) for s, t, d, sh in TL.TOOLS]
    json.dump(idx, open(os.path.join(PUB, "assets", "search.json"), "w"), separators=(",", ":"))

    # redirects + router
    redirects = dict(PG.STATIC_REDIRECTS)
    for old, new in catalog.PRODUCT_REDIRECTS.items():
        redirects["/products/" + old] = new if new.startswith("/") else "/products/" + new
    for k, v in list(redirects.items()):   # resolve chains
        seen = 0
        while v in redirects and seen < 5:
            v = redirects[v]; seen += 1
        redirects[k] = v
    for k, v in redirects.items():
        assert v in WRITTEN, f"redirect target missing: {k} -> {v}"
        assert k not in WRITTEN, f"redirect source is also a page: {k}"
    php = "<?php\n// generated by build.py — old URL => new URL (301)\nreturn " + "[\n" + "".join(f"  {json.dumps(k)} => {json.dumps(v)},\n" for k, v in sorted(redirects.items())) + "];\n"
    open(os.path.join(PUB, "_redirects.php"), "w").write(php)
    shutil.copy(os.path.join(ROOT, "src", "index.php"), os.path.join(PUB, "index.php"))

    # 404
    body404 = f"""<section class="hero" style="min-height:70vh"><div class="hero__bg"><img src="{site_img('negatives')}" alt=""></div><div class="wrap hero__in">
<div class="eyebrow"><span class="rec">Error 404</span></div><h1><span class="line"><span>This frame</span></span><span class="line"><span>didn't <em>develop</em>.</span></span></h1>
<p class="hero__lead">The page you were looking for has moved or never existed. Try the search, or start from one of these.</p>
<div class="hero__cta"><a class="btn" href="/collections/all-film-cameras">Shop film cameras {ICON['arrow']}</a><a class="btn btn--ghost" href="/blogs/guides">Read the guides</a><button class="btn btn--ghost js-search">Search</button></div></div></section>"""
    with open(os.path.join(PUB, "404.html"), "w") as fh:
        fh.write(layout("/404", "Page not found", "This page could not be found.", body404, robots="noindex,follow"))

    # sitemap.xml + robots
    urls = sorted(WRITTEN)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE}{u if u != '/' else '/'}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(PUB, "sitemap.xml"), "w").write(sm)
    open(os.path.join(PUB, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /_p/\nDisallow: /pages/wishlist\nDisallow: /search\n\nSitemap: {SITE}/sitemap.xml\n")
    for f in os.listdir(os.path.join(ROOT, "src", "static")):
        s = os.path.join(ROOT, "src", "static", f)
        if os.path.isfile(s):
            shutil.copy(s, os.path.join(PUB, f))
    # old Shopify CDN image URLs with backlinks -> keep them resolving with a real photo
    for name in ("IMG_0006_35628deb-ec83-4753-8c69-cb583d1021cc.jpg", "IMG_0171_2a58889d-a2ae-4930-b59d-dcfcf93a7f07.jpg"):
        src_key = "olympus-trip-af-60" if "0006" in name else "olympus-trip-35"
        src = os.path.join(PUB, "assets", "img", "products", src_key + ".webp")
        if not os.path.exists(src):
            src = os.path.join(PUB, "assets", "img", "site", "hero.webp")
        if os.path.exists(src):
            from PIL import Image
            os.makedirs(os.path.join(PUB, "cdn", "shop", "files"), exist_ok=True)
            Image.open(src).convert("RGB").save(os.path.join(PUB, "cdn", "shop", "files", name), "JPEG", quality=85)
    print(f"built {len(WRITTEN)} pages, {len(redirects)} redirects")

if __name__ == "__main__":
    main()
