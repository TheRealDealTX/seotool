"""Static site generator for stonecoatedroofs.com.

Reads content/wp.json (the WordPress export, see extract.py) and content/new/*.html
(pages added in the rebuild), and writes the finished site into public/.
Standard library only:  python3 build.py && python3 validate.py
"""

import html
import json
import math
import re
import shutil
from pathlib import Path

from siteconfig import AREA_KEYWORDS, BIZ, BRANDS, FEATURED_CITIES, NAV, REGIONS, SEO, TODAY
import homepage
import tools

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
WP = json.loads((ROOT / "content" / "wp.json").read_text())
ORIGIN = BIZ["origin"]
BRAND = BIZ["name"]
PER_PAGE = 36
SITE_IMG = "/wp-content/uploads/2026/05/Stone-Coated-Roofs-Site-Image.webp"
CSS_V = JS_V = TODAY.replace("-", "")

E = lambda s: html.escape(str(s), quote=True)  # noqa: E731
PAGES = {}  # path -> dict(html=, sitemap=, lastmod=, group=)


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def words(s):
    return len(strip_tags(s).split())


def full_title(t):
    t = html.unescape(t)
    return t if BRAND in t or len(t) + len(BRAND) + 3 > 66 else f"{t} | {BRAND}"


def trim(s, n):
    s = strip_tags(s)
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


# ------------------------------------------------------------------ content model
CATS = {c["id"]: c for c in WP["categories"]}
CAT_BY_SLUG = {c["slug"]: c for c in WP["categories"]}
CAT_BLURB = {
    "compare": "Head-to-head comparisons of stone coated steel against asphalt, tile, slate, cedar, standing seam and more — lifespan, hail, weight, cost and insurance.",
    "general": "Guides to stone coated steel roofing in Texas: cost, lifespan, problems, hail and hurricane performance, insurance discounts and commercial roofing.",
    "roof-brands": "Reviews of the leading stone coated steel brands we install — Decra, Tilcor, TEK, Roser and more — with profiles, ratings and warranties.",
    "roof-styles": "Stone coated steel can look like slate, cedar shake, clay tile or dimensional shingles. Explore each roof style and how it performs in Texas.",
}
CAT_TITLE = {"compare": "Stone Coated Steel vs Other Roofing: Comparisons",
             "general": "Stone Coated Roofing Guides for Texas Owners",
             "roof-brands": "Stone Coated Steel Roofing Brands",
             "roof-styles": "Stone Coated Roof Styles: Slate, Shake, Tile, Shingle"}


def parse_new(path):
    raw = path.read_text()
    m = re.match(r"\s*<!--META (.*?) -->\s*", raw, flags=re.S)
    meta = json.loads(m.group(1))
    meta["body"] = raw[m.end():].strip()
    return meta


NEW = [parse_new(p) for p in sorted((ROOT / "content" / "new").glob("*.html"))]

GUIDE_IMG = {
    "storm-damage-roof-replacement": "/wp-content/uploads/2026/06/hail-resistant-roofing-texas-1.webp",
    "roof-types-for-insurance": "/wp-content/uploads/2026/07/insurance-approved-roofing-systems-1.webp",
    "stone-coated-steel-roofing-market": "/wp-content/uploads/2026/06/Why-Stone-Coated-Roofing-Is-Growing-in-Texas-1.webp",
}

POSTS = []
for p in WP["posts"]:
    o = SEO.get(p["path"], {})
    POSTS.append(dict(p, h1=o.get("h1", p["title"]), seo_title=o.get("title", p["seo_title"]),
                      description=o.get("description") or p["description"] or trim(p["excerpt"], 155),
                      modified=TODAY if o else p["modified"], faq=[], cat_slugs=[CATS[c]["slug"] for c in p["categories"]]))
for n in NEW:
    if n["kind"] != "guide":
        continue
    POSTS.append(dict(id=n["slug"], kind="post", slug=n["slug"], path=f"/{n['slug']}/", title=n["h1"], h1=n["h1"],
                      seo_title=n["title"], description=n["description"], date=TODAY, modified=TODAY,
                      categories=[1], cat_slugs=["general"], image={"src": GUIDE_IMG[n["slug"]], "width": 900, "height": 600},
                      excerpt=n["lede"], body=n["body"], faq=n.get("faq", []), lede=n["lede"]))
POSTS.sort(key=lambda p: (p["date"], str(p["id"])), reverse=True)


def short_title(t):
    """Long WordPress headlines -> the part before the colon (keeps the keyword, fits the SERP)."""
    t = html.unescape(t)
    if len(t) > 60 and ":" in t:
        t = t.split(":")[0].strip()
    return t


for p in POSTS:
    p["seo_title"] = short_title(p["seo_title"])

CITY_NAMES = {}
AREAS = []
for p in WP["pages"]:
    if p["kind"] != "area":
        continue
    key = p["slug"].replace("-stone-coated-roofs", "")
    city = p["title"]
    kw = AREA_KEYWORDS.get(key)
    AREAS.append(dict(key=key, city=city, path=p["path"], h1=f"Stone Coated Steel Roofing in {city}, TX",
                      seo_title=kw[0] if kw else f"{city} Stone Coated Steel Roofing",
                      description=kw[1] if kw else p["description"], body=p["body"], faq=[], date=p["date"],
                      modified=TODAY, lede=None, image=None))
for n in NEW:
    if n["kind"] != "area":
        continue
    key = n["slug"].replace("-stone-coated-roofs", "")
    city = " ".join(w.capitalize() for w in key.split("-")).replace("Mckinney", "McKinney")
    AREAS.append(dict(key=key, city=city, path=f"/service-area/{n['slug']}/", h1=n["h1"], seo_title=n["title"],
                      description=n["description"], body=n["body"], faq=n.get("faq", []), date=TODAY,
                      modified=TODAY, lede=n.get("lede"), image=None, eyebrow=n.get("eyebrow")))
AREAS.sort(key=lambda a: a["city"])
AREA = {a["key"]: a for a in AREAS}
AREA_IMGS = ["/wp-content/uploads/2026/05/What-Is-Stone-Coated-Steel-Roofing.webp", "/wp-content/uploads/2026/05/Tile-Roofs.webp",
             "/wp-content/uploads/2026/05/Slate-Roof.webp", "/wp-content/uploads/2026/05/Wood-Shake-Roof.webp",
             "/wp-content/uploads/2026/05/Shingle-Roofs.webp", "/wp-content/uploads/2026/05/Are-Stone-Coated-Roofs-Worth-It.webp"]
for i, a in enumerate(AREAS):
    a["image"] = {"src": AREA_IMGS[i % len(AREA_IMGS)], "width": 900, "height": 600}
missing = [k for r in REGIONS.values() for k in r if k not in AREA]
assert not missing, f"REGIONS lists cities with no page: {missing}"

WPP = {p["slug"]: p for p in WP["pages"]}

# ------------------------------------------------------------------ shared chrome
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

BUSINESS = {
    "@type": ["RoofingContractor", "LocalBusiness"], "@id": f"{ORIGIN}/#business", "name": BRAND,
    "url": f"{ORIGIN}/", "telephone": BIZ["phone_href"], "description": f"{BIZ['tagline']}. Residential and commercial, every leading brand, statewide service.",
    "logo": f"{ORIGIN}/wp-content/uploads/2026/05/Stone-Coated-Roofs-Logo.webp", "image": f"{ORIGIN}{SITE_IMG}",
    "priceRange": "$$$", "areaServed": {"@type": "State", "name": "Texas"},
    "address": {"@type": "PostalAddress", "addressRegion": "TX", "addressCountry": "US"},
    "knowsAbout": ["Stone coated steel roofing", "Class 4 impact resistant roofing", "Hail damage roof replacement",
                   "Hurricane resistant roofing", "Commercial mansard roofing"],
    "brand": [{"@type": "Brand", "name": b[0]} for b in BRANDS],
}
WEBSITE = {"@type": "WebSite", "@id": f"{ORIGIN}/#website", "url": f"{ORIGIN}/", "name": BRAND, "publisher": {"@id": f"{ORIGIN}/#business"}}


def crumbs_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": html.unescape(n), "item": f"{ORIGIN}{u}"} for i, (n, u) in enumerate(trail)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"],
            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(q["a"])}} for q in faq]}


def crumbs_html(trail):
    parts = [f'<a href="{u}">{E(html.unescape(n))}</a>' for n, u in trail[:-1]]
    parts.append(f'<span aria-current="page">{E(html.unescape(trail[-1][0]))}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def header(path):
    links = "".join(f'<a href="{u}"{" aria-current=page" if path.startswith(u) else ""}>{n}</a>' for n, u, _ in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="topbar"><div class="wrap"><span><i class="pulse"></i>Free inspections statewide · <span class="hide-s">Residential &amp; commercial · Every leading brand</span></span><a href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a></div></div>
<header class="site-header"><div class="wrap">
<a class="logo" href="/" aria-label="{BRAND} home"><span class="mark" aria-hidden="true"></span><span>Stone Coated <i>Roofs</i></span></a>
<button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-sm mag" href="/free-quote/">Free Quote <span class="arr">→</span></a></nav>
</div></header>"""


def footer():
    cities = "".join(f'<li><a href="{AREA[k]["path"]}">{AREA[k]["city"]}</a></li>' for k in FEATURED_CITIES[:6])
    brands = "".join(f'<li><a href="{b[4]}">{b[0]}</a></li>' for b in BRANDS if b[4])
    learn = [("Stone coated roofing cost", "/stone-coated-roofing-cost-texas/"), ("Lifespan", "/stone-coated-steel-roof-lifespan/"),
             ("Problems &amp; fixes", "/stone-coated-steel-roof-problems/"), ("Hail performance", "/best-roofing-material-for-hailstorms-in-texas/"),
             ("Insurance discounts", "/insurance-discounts-for-class-4-roofing/"), ("Storm damage", "/storm-damage-roof-replacement/")]
    tl = [(t["short"], t["path"]) for t in tools.TOOLS]
    lis = lambda xs: "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in xs)  # noqa: E731
    return f"""<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><a class="logo" href="/"><span class="mark" aria-hidden="true"></span><span>Stone Coated <i>Roofs</i></span></a>
<p style="margin-top:18px;max-width:340px">{BIZ['tagline']}. Residential and commercial, every leading brand, statewide service.</p>
<a class="foot-tel" href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></div>
<div><h4>Service Area</h4><ul>{cities}<li><a href="/service-area/">All Texas cities</a></li></ul></div>
<div><h4>Brands &amp; Styles</h4><ul>{brands}<li><a href="/topic/roof-styles/">Roof styles</a></li><li><a href="/commercial/">Commercial</a></li></ul></div>
<div><h4>Learn</h4><ul>{lis(learn)}</ul></div>
<div><h4>Tools</h4><ul>{lis(tl)}</ul></div>
</div>
<div class="foot-bottom"><span>© {TODAY[:4]} STONECOATEDROOFS.COM · TEXAS-BASED · STATEWIDE SERVICE</span><span><a href="/privacy-policy/">Privacy</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>"""


PROPERTY_TYPES = ["Single-family home", "Apartments / Multifamily", "Commercial / Retail", "Hospitality", "Church / Religious", "HOA / Community", "Other"]
REASONS = ["Hail Damage", "Wind Damage", "Hurricane Damage", "Tornado Damage", "End of Lifespan", "Insurance Non-Renewal", "Upgrade / New Build", "Other"]


def lead_form(fid, title=None, button="Request My Free Estimate"):
    opts = lambda xs: "".join(f"<option>{E(x)}</option>" for x in xs)  # noqa: E731
    head = f"<h3>{title}</h3>" if title else ""
    return f"""<form class="lead" action="/quote.php" method="post" data-form="{fid}" data-phone="{BIZ['phone_display']}">{head}
<div class="fields">
<div class="field"><label for="{fid}-name">Your name</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="{fid}-phone">Phone (10-digit)</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="field"><label for="{fid}-email">Email</label><input id="{fid}-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="{fid}-city">City</label><input id="{fid}-city" name="city" autocomplete="address-level2" required></div>
<div class="field"><label for="{fid}-type">Property type</label><select id="{fid}-type" name="type">{opts(PROPERTY_TYPES)}</select></div>
<div class="field"><label for="{fid}-reason">Reason to replace</label><select id="{fid}-reason" name="reason">{opts(REASONS)}</select></div>
</div>
<div class="hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<button class="btn btn-block" type="submit">{button} <span class="arr">→</span></button>
<p class="form-note">Free, no-pressure estimate. We'll call to schedule — or reach us now at <a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a>.</p>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def popup():
    return f"""<div class="popup" id="quote-popup" role="dialog" aria-modal="true" aria-labelledby="pop-title" aria-hidden="true">
<div class="box">
<button class="x" type="button" data-close aria-label="Close">×</button>
<div class="side"><span class="eyebrow">Free estimate</span><h3>A roof you install once.</h3>
<ul><li>Class 4 hail &amp; 120+ mph wind rated</li><li>Every leading brand — Decra, Tilcor, TEK, Roser</li><li>Insurance documentation support</li><li>Statewide crews, residential &amp; commercial</li></ul></div>
{lead_form("pop", title='<span id="pop-title">Get your free stone coated roof estimate</span>', button="Get My Free Estimate")}
</div></div>
<div class="sticky-call"><a class="btn btn-sm" href="tel:{BIZ['phone_href']}">Call now</a><a class="btn btn-sm btn-ghost" style="background:#fff" href="/free-quote/" data-open-quote>Free quote</a></div>"""


def page(path, title, description, body, graph=(), image=SITE_IMG, og_type="website", robots="index,follow,max-image-preview:large",
         extra_head="", scripts=("site",), no_popup=False, sitemap=True, lastmod=TODAY, group="page"):
    canonical = f"{ORIGIN}{path}"
    ld = json.dumps({"@context": "https://schema.org", "@graph": [BUSINESS, WEBSITE, *graph]}, ensure_ascii=False, separators=(",", ":"))
    js = "".join(f'<script src="/assets/js/{s}.js?v={JS_V}" defer></script>' for s in scripts)
    img = f"{ORIGIN}{image}" if image.startswith("/") else image
    doc = f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=" js"</script>
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#12100e">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="msapplication-TileImage" content="/web-app-manifest-192x192.png">
{FONTS}
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body{' data-no-popup' if no_popup else ''}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{popup()}
{js}
</body>
</html>
"""
    PAGES[path] = dict(html=doc, sitemap=sitemap, lastmod=lastmod, group=group)


def cta_band(h="Ready for the last roof you'll ever buy?", p=None):
    p = p or f"Book a free inspection with {BRAND}. We document storm damage, walk you through every brand and profile, and give you a clear written estimate."
    return f"""<section class="section tight"><div class="wrap"><div class="cta-band rv">
<div><span class="eyebrow" style="color:#fbe6d9">Free estimate</span><h2>{h}</h2><p>{p}</p></div>
<div class="actions"><a class="btn mag" href="/free-quote/">Get a free estimate <span class="arr">→</span></a><a class="btn btn-ghost" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a></div>
</div></div></section>"""


def phero(trail, h1, lede=None, eyebrow=None, img=None, meta=None):
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    ld = f'<p class="lede">{lede}</p>' if lede else ""
    mt = f'<div class="meta-row">{meta}</div>' if meta else ""
    ph = (f'<div class="ph rv rv-s"><img src="{img["src"]}" width="{img.get("width") or 900}" height="{img.get("height") or 600}" alt="{E(strip_tags(h1))}" fetchpriority="high"></div>'
          if img else "")
    return f"""<section class="phero{'' if img else ' noimg'}"><div class="wrap"><div>{crumbs_html(trail)}{eb}<h1 class="split-words">{h1}</h1>{ld}{mt}</div>{ph}</div></section>"""


def faq_html(faq, title="Frequently asked questions"):
    if not faq:
        return ""
    items = "".join(f'<details{" open" if i == 0 else ""}><summary>{E(q["q"])}</summary><div class="a"><p>{q["a"]}</p></div></details>' for i, q in enumerate(faq))
    return f'<section class="section tight" id="faq"><div class="wrap"><div class="sec-head center"><span class="eyebrow">FAQ</span><h2>{title}</h2></div><div class="faq rv">{items}</div></div></section>'


def post_card(p, lazy=True):
    img = p.get("image") or {"src": SITE_IMG}
    src = re.sub(r"\.webp$", "-768x512.webp", img["src"]) if (OUT / img["src"].lstrip("/").replace(".webp", "-768x512.webp")).exists() else img["src"]
    cat = CATS[p["categories"][0]]["name"] if p.get("categories") else "Guide"
    return f"""<a class="post-card rv" href="{p['path']}"><div class="ph"><img src="{src}" alt="{E(strip_tags(p['title']))}" width="768" height="512"{' loading="lazy"' if lazy else ''} decoding="async"></div>
<div class="bd"><div class="meta">{E(cat)} · {read_min(p['body'])} min read</div><h3>{E(html.unescape(p['title']))}</h3><p>{E(trim(p['excerpt'], 140))}</p></div></a>"""


def read_min(body):
    return max(2, math.ceil(words(body) / 230))


def fmt_date(iso):
    y, m, d = iso.split("-")
    return f"{['January','February','March','April','May','June','July','August','September','October','November','December'][int(m)-1]} {int(d)}, {y}"


TOOL_HINTS = [  # (regex on slug/title, tool path)
    (r"maint|checklist", "/tools/roof-maintenance-checklist-log/"),
    (r"insurance|premium|class-4|discount", "/tools/insurance-discount-estimator/"),
    (r"hail|storm", "/tools/hail-damage-roof-checklist/"),
    (r"cost|price|worth|regret|cheap", "/tools/stone-coated-roof-cost-calculator/"),
    (r"tile|slate|weight|concrete|clay", "/tools/roof-weight-calculator/"),
    (r"lifespan|last|vs|compare|asphalt|shingle", "/tools/lifetime-roof-cost-calculator/"),
]


def tool_for(slug):
    for rx, u in TOOL_HINTS:
        if re.search(rx, slug):
            return tools.BY_PATH[u]
    return tools.BY_PATH["/tools/stone-coated-roof-cost-calculator/"]


def tool_side(t):
    return f'<a class="card lift" href="{t["path"]}" style="padding:24px"><span class="tag">Free tool</span><h3 style="font-size:1.2rem">{t["name"]}</h3><p style="font-size:.92rem">{t["teaser"]}</p><span class="more">Open the tool</span></a>'


def inject_cta(body, t):
    """Drop a mid-article CTA before the h2 nearest the 45% mark."""
    hs = [m.start() for m in re.finditer(r"<h2>", body)]
    if len(hs) < 3:
        return body
    i = hs[max(1, int(len(hs) * 0.45))]
    box = (f'<div class="inline-cta"><div><strong>Try the {t["name"].lower()}</strong><span>{t["teaser"]}</span></div>'
           f'<a class="btn btn-sm" href="{t["path"]}">Open tool <span class="arr">→</span></a></div>')
    return body[:i] + box + body[i:]


def article(trail, h1, lede, eyebrow, img, body, meta, side_extra, faq, graph, path, title, description, related, og_type="article", lastmod=TODAY, group="post"):
    t = tool_for(path)
    side = f"""<aside class="aside no-print"><nav class="toc" aria-label="On this page"><h4>On this page</h4><ol></ol></nav>
<div class="side-cta"><h4>Free stone coated roof estimate</h4><p>Inspection, storm documentation and a written quote from {BRAND}.</p><a class="btn" href="/free-quote/" data-open-quote>Get my estimate <span class="arr">→</span></a><a class="tel" href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></div>
{tool_side(t)}{side_extra}</aside>"""
    rel = ""
    if related:
        rel = f'<section class="section tight sand"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Keep reading</span><h2>Related <span class="it">guides</span></h2></div><p><a href="/blog/">All stone coated roofing guides →</a></p></div><div class="grid g3">{"".join(post_card(r) for r in related)}</div></div></section>'
    share = (f'<div class="share no-print"><button type="button" data-copy>Copy link</button>'
             f'<a href="https://www.facebook.com/sharer/sharer.php?u={ORIGIN}{path}" rel="noopener" target="_blank">Share on Facebook</a>'
             f'<a href="mailto:?subject={E(strip_tags(h1))}&amp;body={ORIGIN}{path}">Email</a></div>')
    author = (f'<div class="author"><span class="mark" aria-hidden="true"></span><div><strong>{BRAND}</strong>'
              f'<small>{BIZ["tagline"]}. Reviewed for Texas building conditions.</small></div></div>')
    body = inject_cta(body, t)
    html_body = (phero(trail, h1, lede, eyebrow, img, meta)
                 + f'<div class="wrap article-wrap"><article class="prose">{body}{author}{share}</article>{side}</div>'
                 + faq_html(faq) + rel + cta_band())
    page(path, full_title(title), description, html_body, graph=graph, image=(img or {}).get("src", SITE_IMG), og_type=og_type, lastmod=lastmod, group=group)


# ------------------------------------------------------------------ page builders
def build_posts():
    for p in POSTS:
        cat = CATS[p["categories"][0]]
        trail = [("Home", "/"), ("Blog", "/blog/"), (cat["name"], cat["path"]), (p["h1"], p["path"])]
        related = [r for r in POSTS if r is not p and set(r["categories"]) & set(p["categories"])]
        # stable but varied: neighbours by date
        idx = POSTS.index(p)
        related = sorted(related, key=lambda r: abs(POSTS.index(r) - idx))[:3]
        lede = p.get("lede") or trim(p["excerpt"], 210)
        meta = f'<span>Updated <b>{fmt_date(p["modified"])}</b></span><span><b>{read_min(p["body"])}</b> min read</span><span>By <b>{BRAND}</b></span>'
        graph = [crumbs_ld(trail), {
            "@type": "BlogPosting", "headline": strip_tags(p["h1"])[:110], "description": p["description"],
            "datePublished": p["date"], "dateModified": p["modified"], "mainEntityOfPage": f"{ORIGIN}{p['path']}",
            "image": f"{ORIGIN}{(p.get('image') or {}).get('src', SITE_IMG)}", "wordCount": words(p["body"]),
            "author": {"@id": f"{ORIGIN}/#business"}, "publisher": {"@id": f"{ORIGIN}/#business"},
            "articleSection": cat["name"]}]
        if p["faq"]:
            graph.append(faq_ld(p["faq"]))
        article(trail, E(html.unescape(p["h1"])), E(lede), E(cat["name"]), p.get("image"), p["body"], meta, "", p["faq"],
                graph, p["path"], p["seo_title"], p["description"], related, lastmod=p["modified"])


def region_of(key):
    for r, ks in REGIONS.items():
        if key in ks:
            return r
    return "Texas"


REGION_PHRASE = {"Dallas–Fort Worth": "the rest of Dallas–Fort Worth", "Houston & Gulf Coast": "the Gulf Coast",
                 "Central Texas": "Central Texas", "West Texas & Panhandle": "West Texas", "East Texas": "East Texas"}


def build_areas():
    for a in AREAS:
        trail = [("Home", "/"), ("Service Area", "/service-area/"), (a["city"], a["path"])]
        region = region_of(a["key"])
        near = [AREA[k] for k in REGIONS.get(region, []) if k != a["key"]][:10] or [AREA[k] for k in FEATURED_CITIES if k != a["key"]][:8]
        side = '<div class="side-list"><h4>Nearby service areas</h4>' + "".join(f'<a href="{n["path"]}">{n["city"]} stone coated roofs</a>' for n in near) + '<a href="/service-area/">All Texas cities →</a></div>'
        around = REGION_PHRASE.get(region, "the surrounding area")
        lede = a["lede"] or f"{BRAND} installs Class 4 stone coated steel roofing across {a['city']} and {around} — every leading brand, residential and commercial, with free inspections and insurance documentation."
        meta = f'<span>Serving <b>{a["city"]}</b> &amp; {E(around)}</span><span>Free inspections</span><span><a href="tel:{BIZ["phone_href"]}" style="color:#fff">{BIZ["phone_display"]}</a></span>'
        graph = [crumbs_ld(trail), {
            "@type": "Service", "name": f"Stone coated steel roofing in {a['city']}, TX", "serviceType": "Stone coated steel roof installation and replacement",
            "provider": {"@id": f"{ORIGIN}/#business"}, "areaServed": {"@type": "City", "name": f"{a['city']}, TX"}, "url": f"{ORIGIN}{a['path']}"}]
        if a["faq"]:
            graph.append(faq_ld(a["faq"]))
        article(trail, E(a["h1"]), E(lede), E(a.get("eyebrow") or f"{region} · Service area"), a["image"], a["body"], meta, side, a["faq"],
                graph, a["path"], a["seo_title"], a["description"], [], og_type="website", group="page")


# Texas outline (lon, lat) and city coordinates for the service-area map
TX = [(-103.04, 36.5), (-100.0, 36.5), (-100.0, 34.56), (-99.2, 34.4), (-98.1, 34.1), (-97.0, 33.8), (-96.0, 33.9), (-95.2, 33.9),
      (-94.48, 33.64), (-94.04, 33.55), (-94.04, 33.0), (-94.04, 31.99), (-93.6, 31.2), (-93.5, 30.4), (-93.84, 29.7), (-94.7, 29.35),
      (-95.1, 29.1), (-96.0, 28.6), (-96.8, 28.2), (-97.2, 27.7), (-97.4, 27.2), (-97.4, 26.5), (-97.15, 25.95), (-97.7, 26.05),
      (-98.5, 26.3), (-99.1, 26.6), (-99.5, 27.5), (-100.3, 28.3), (-100.7, 29.1), (-101.4, 29.77), (-102.4, 29.8), (-102.9, 29.2),
      (-103.3, 29.0), (-104.0, 29.4), (-104.7, 30.0), (-105.0, 30.7), (-106.0, 31.4), (-106.5, 31.78), (-106.6, 32.0), (-103.06, 32.0)]
COORDS = {"houston": (29.76, -95.37), "dallas": (32.78, -96.80), "austin": (30.27, -97.74), "san-antonio": (29.42, -98.49),
          "fort-worth": (32.75, -97.33), "el-paso": (31.76, -106.49), "arlington": (32.74, -97.11), "corpus-christi": (27.80, -97.40),
          "plano": (33.02, -96.70), "lubbock": (33.58, -101.86), "belton": (31.06, -97.46), "lufkin": (31.34, -94.73),
          "frisco": (33.15, -96.82), "coppell": (32.95, -96.99), "colleyville": (32.88, -97.15), "denton": (33.21, -97.13),
          "prosper": (33.24, -96.80), "mckinney": (33.20, -96.64), "westlake": (32.99, -97.20), "keller": (32.93, -97.23),
          "southlake": (32.94, -97.13), "grapevine": (32.93, -97.08), "grand-prairie": (32.75, -97.00), "mesquite": (32.77, -96.60),
          "irving": (32.81, -96.95), "lewisville": (33.05, -96.99)}


def tx_map():
    k = 52
    px = lambda lon, lat: ((lon + 106.8) * k * 0.86, (36.7 - lat) * k)  # noqa: E731
    pts = " ".join("%.1f,%.1f" % px(lo, la) for lo, la in TX)
    dots = []
    for key, (la, lo) in COORDS.items():
        if key not in AREA:
            continue
        x, y = px(lo, la)
        label = f'<text x="{x + 8:.1f}" y="{y + 4:.1f}">{AREA[key]["city"]}</text>' if key in ("houston", "dallas", "austin", "san-antonio", "el-paso", "lubbock", "corpus-christi", "lufkin", "belton") else ""
        dots.append(f'<a href="{AREA[key]["path"]}" aria-label="{AREA[key]["city"]}"><circle class="dot-ring" cx="{x:.1f}" cy="{y:.1f}" r="5" style="animation-delay:{(len(dots) % 7) * .37:.2f}s"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="4"/>{label}</a>')
    return f'<div class="tx-map rv rv-s"><svg viewBox="0 0 {k * 0.86 * 13.4:.0f} {k * 11:.0f}" role="img" aria-label="Map of Texas cities served by {BRAND}"><polygon class="state" points="{pts}"/>{"".join(dots)}</svg></div>'


def city_grid(keys=None, fid="cities"):
    keys = keys or [a["key"] for a in AREAS]
    return (f'<div class="city-search"><label class="sr" for="{fid}-q">Find your city</label><input id="{fid}-q" placeholder="Find your city…" data-city-filter="#{fid}"></div>'
            f'<div class="cities" id="{fid}">' + "".join(f'<a href="{AREA[k]["path"]}">{AREA[k]["city"]}</a>' for k in keys) + "</div>")


def build_service_area():
    p = WPP["service-area"]
    body = re.sub(r"<h2>Areas We Serve</h2>.*?</ul>", "", p["body"], flags=re.S)
    trail = [("Home", "/"), ("Service Area", "/service-area/")]
    regions = "".join(
        f'<div class="card rv" style="--d:{i * .06:.2f}s"><span class="tag">{len(ks)} {"city" if len(ks) == 1 else "cities"}</span><h3>{E(r)}</h3><ul class="pill-list">'
        + "".join(f'<li><a href="{AREA[k]["path"]}">{AREA[k]["city"]}</a></li>' for k in ks) + "</ul></div>"
        for i, (r, ks) in enumerate(REGIONS.items()))
    html_body = (phero(trail, "Stone Coated Steel Roofing <span class='it'>Across Texas</span>",
                       f"{BRAND} installs stone coated steel roofing statewide — from the Panhandle to the Gulf Coast. Pick your city for local storm, code and HOA detail.",
                       "Service area")
                 + f'<section class="section dark"><div class="wrap two"><div><span class="eyebrow">Find your city</span><h2>Crews dispatched <span class="it">statewide.</span></h2><p class="muted" style="color:#b8ada1">{len(AREAS)} city guides and counting. Don\'t see yours? We still serve it — <a href="/free-quote/">request an estimate</a>.</p>{city_grid(fid="hub")}</div>{tx_map()}</div></section>'
                 + f'<section class="section"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">By region</span><h2>Where we <span class="it">work.</span></h2></div><p>Each region brings different roof stresses — DFW hail, Gulf hurricanes, West Texas wind and UV.</p></div><div class="grid g3">{regions}</div></div></section>'
                 + f'<div class="wrap article-wrap" style="padding-top:0"><article class="prose">{body}</article><aside class="aside"><div class="side-cta"><h4>Free estimate, anywhere in Texas</h4><p>Tell us your city and we\'ll route the closest crew.</p><a class="btn" href="/free-quote/" data-open-quote>Get my estimate <span class="arr">→</span></a><a class="tel" href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a></div></aside></div>'
                 + cta_band())
    graph = [crumbs_ld(trail), {"@type": "ItemList", "name": "Texas service areas", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}{a['path']}", "name": a["city"]} for i, a in enumerate(AREAS)]}]
    page("/service-area/", "Stone Coated Steel Roofing Service Area: All of Texas",
         f"{BRAND} serves all of Texas — Houston, Dallas–Fort Worth, Austin, San Antonio, Corpus Christi, El Paso and more. Find your local stone coated roofing page.",
         html_body, graph=graph)


def build_why_replace():
    p = WPP["why-replace"]
    trail = [("Home", "/"), ("Why Replace", "/why-replace/")]
    reasons = homepage.reasons_cards()
    html_body = (phero(trail, "Why Replace Your Roof <span class='it'>Before It Fails</span>",
                       "Hail bruising, wind-lifted tabs, an aging asphalt roof or a non-renewal letter — here are the signs it's time, and why stone coated steel is the replacement Texas owners stop worrying about.",
                       "Why replace", {"src": "/wp-content/uploads/2026/06/What-Homeowners-Regret-About-Cheap-Roofing-Systems-1.webp", "width": 900, "height": 600})
                 + f'<section class="section tight sand"><div class="wrap"><div class="grid g3">{reasons}</div></div></section>'
                 + f'<div class="wrap article-wrap"><article class="prose">{p["body"]}</article><aside class="aside no-print"><nav class="toc"><h4>On this page</h4><ol></ol></nav>{tool_side(tools.BY_PATH["/tools/hail-damage-roof-checklist/"])}<div class="side-cta"><h4>Free roof inspection</h4><p>We document everything for your carrier.</p><a class="btn" href="/free-quote/" data-open-quote>Book inspection <span class="arr">→</span></a></div></aside></div>'
                 + cta_band())
    page("/why-replace/", "Why Replace Your Roof? Signs & Reasons | Stone Coated Roofs",
         "Why replace your roof: hail and wind damage, end of lifespan, insurance non-renewal and hidden leaks — and why stone coated steel lasts in Texas.",
         html_body, graph=[crumbs_ld(trail)], image="/wp-content/uploads/2026/06/What-Homeowners-Regret-About-Cheap-Roofing-Systems-1.webp")


COMMERCIAL = [
    ("Apartments", "Multifamily roofs that don't need replacement every claim cycle.", "Multifamily", "/apartment-roofing-systems-texas/", "M8 50V18L32 6l24 12v32zM16 24h6M28 24h6M40 24h6M16 32h6M28 32h6M40 32h6M28 50v-6h8v6"),
    ("Hotels & Motels", "Mansard roofs across mid-tier and boutique hospitality properties.", "Hospitality", "/hotel-roofing-replacement/", "M6 50V22L32 8l26 14v28zM14 50V30h36v20M20 36h6M38 36h6M30 50v-8h4v8"),
    ("Pharmacies", "CVS, Walgreens, and independents — branded mansard profiles.", "Retail healthcare", "/retail-center-roofing-replacement/", "M6 50V22h52v28zM6 22l12-12h28l12 12M28 26h8v-8h-8zM30 22h4M32 20v4"),
    ("Strip Retail", "Multi-tenant shopping centers with prominent mansard fronts.", "Retail", "/retail-center-roofing-replacement/", "M4 50V24h56v26zM4 24l8-10h40l8 10M16 50V32h8v18M40 50V32h8v18M28 38h8M28 44h8"),
    ("Restaurants", "Quick-service, mid-scale, and franchise locations with sloped roofs.", "Food service", "/commercial-stone-coated-roofing/", "M8 50V26h48v24zM8 26l8-12h32l8 12M24 32h16v18H24zM32 14V8M28 8h8"),
    ("Senior Living", "Assisted living, memory care, and independent living communities.", "Healthcare", "/assisted-living-roofing-systems/", "M6 50V28l26-16 26 16v22zM14 50V34h12v16M36 50V34h14v16M32 20v8M30 24h4"),
    ("Churches", "Sanctuaries and fellowship halls with steep, visible roof lines.", "Religious", "/church-metal-roofing-systems/", "M10 50V30l22-16 22 16v20zM28 50V40h8v10M32 14V4M28 8h8"),
    ("HOAs & Communities", "Community-wide reroofs planned around reserves and board approvals.", "Associations", "/hoa-roofing-replacement/", "M4 50V30l12-10 12 10v20zM36 50V30l12-10 12 10v20zM12 50v-8h8v8M44 50v-8h8v8"),
]


def svg_icon(d, vb="0 0 64 56"):
    return f'<svg viewBox="{vb}" aria-hidden="true"><path d="{d}"/></svg>'


def commercial_cards():
    return "".join(
        f'<a class="card tilt rv" style="--d:{i * .05:.2f}s" href="{u}"><span class="ico">{svg_icon(dd)}</span><span class="tag">{t}</span><h3>{E(n)}</h3><p>{E(desc)}</p><span class="more">Read the guide</span></a>'
        for i, (n, desc, t, u, dd) in enumerate(COMMERCIAL))


def build_commercial():
    trail = [("Home", "/"), ("Commercial", "/commercial/")]
    posts = [p for p in POSTS if p["slug"] in ("commercial-stone-coated-roofing", "long-lifespan-commercial-roofing", "multifamily-roofing-contractor-texas",
                                               "apartment-roofing-systems-texas", "hotel-roofing-replacement", "church-metal-roofing-systems",
                                               "retail-center-roofing-replacement", "assisted-living-roofing-systems", "hoa-roofing-replacement")]
    faq = [
        {"q": "Can stone coated steel go on a commercial building?", "a": "Yes — on any sloped or mansard roof section. It is the go-to upgrade for apartment complexes, hotels, pharmacies, strip retail, restaurants, churches and senior living. Low-slope field areas stay on a membrane system; we detail the transition."},
        {"q": "How do you keep a property open during a reroof?", "a": "Commercial work is phased building-by-building or elevation-by-elevation, with daily dry-in, protected entrances, scheduled noisy work and a single point of contact for property management."},
        {"q": "Does a commercial stone coated roof lower insurance costs?", "a": "Class 4 impact and Class A fire ratings strengthen the underwriting file and can reduce premiums or wind/hail deductibles, depending on the carrier. We supply the product documentation your broker needs."},
        {"q": "What warranties are available on commercial projects?", "a": "Manufacturer warranties on stone coated steel typically run 50 years to lifetime on the material, plus our workmanship warranty. Hospitality and multifamily owners should confirm transferability and wind ratings in writing — we walk through each brand's terms."},
    ]
    html_body = (phero(trail, "Commercial Stone Coated <span class='it'>Steel Roofing</span>",
                       f"If your building has a sloped or mansard roof, stone coated steel makes it permanent. {BRAND} handles apartments, hotels, retail, churches, senior living and HOAs across Texas — lower lifetime cost, lower insurance, lower maintenance.",
                       "Multi-unit &amp; business", {"src": "/wp-content/uploads/2026/07/commercial-stone-coated-roofing-1.webp", "width": 900, "height": 600})
                 + f'<section class="section"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Property types</span><h2>Built for commercial <span class="it">properties, too.</span></h2></div><p>One roof for the life of the building — fewer claims, fewer tenant disruptions, fewer capital surprises.</p></div><div class="grid g4">{commercial_cards()}</div></div></section>'
                 + f'<section class="section dark"><div class="wrap two"><div><span class="eyebrow">Why owners switch</span><h2>Lifecycle math that <span class="it">works.</span></h2><p style="color:#d6ccbf">An asphalt mansard on a Texas property may need replacing two or three times in the span one stone coated steel system lasts. Every replacement means scaffolding, tenant notices, dumpsters and a fresh insurance claim.</p><ul class="layer-list" style="color:#e9e2d8"><li><b style="color:#fff">40–70 year service life</b><span style="color:#b8ada1">versus 12–18 years for asphalt in Texas heat.</span></li><li><b style="color:#fff">Class 4 hail &amp; Class A fire</b><span style="color:#b8ada1">the ratings underwriters look for.</span></li><li><b style="color:#fff">~2.4 lb per sq ft</b><span style="color:#b8ada1">a fraction of concrete tile — no structural upgrade on most mansards.</span></li></ul><p class="mt"><a class="btn" href="/tools/lifetime-roof-cost-calculator/">Run the lifetime cost calculator <span class="arr">→</span></a></p></div><div class="quote-box">{lead_form("com", "Request a commercial bid")}</div></div></section>'
                 + f'<section class="section sand"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Commercial guides</span><h2>Plan your <span class="it">project.</span></h2></div><p>Practical guides for owners, asset managers and boards.</p></div><div class="grid g3">{"".join(post_card(p) for p in posts)}</div></div></section>'
                 + faq_html(faq, "Commercial roofing questions") + cta_band("Get a commercial stone coated roofing bid"))
    page("/commercial/", "Commercial Stone Coated Steel Roofing in Texas | Stone Coated Roofs",
         "Commercial stone coated steel roofing for apartments, hotels, retail, churches, senior living and HOAs across Texas — durable, insurable, long-life roofs.",
         html_body, graph=[crumbs_ld(trail), faq_ld(faq), {"@type": "Service", "name": "Commercial stone coated steel roofing", "provider": {"@id": f"{ORIGIN}/#business"}, "areaServed": {"@type": "State", "name": "Texas"}}],
         image="/wp-content/uploads/2026/07/commercial-stone-coated-roofing-1.webp")


def build_quote():
    p = WPP["free-quote"]
    trail = [("Home", "/"), ("Free Quote", "/free-quote/")]
    intro = re.sub(r"<(h2|form)[\s\S]*", "", p["body"])
    steps = [("Tell us about the roof", "Two minutes on the form or a call. We ask about the property, the damage and your timeline."),
             ("Free inspection", "A specialist walks the roof, photographs damage and measures every plane."),
             ("Options &amp; written estimate", "Brands, profiles and install methods side by side — with honest pricing."),
             ("Insurance support", "If storm damage is involved, we document it for your carrier and review the scope."),
             ("Installation", "Scheduled, protected and cleaned up daily — then registered for the manufacturer warranty.")]
    st = "".join(f'<div class="step rv" style="--d:{i * .08:.2f}s"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(steps))
    html_body = (phero(trail, "Get a Free Stone Coated <span class='it'>Roof Estimate</span>",
                       "Planning a roof replacement? Dealing with hail or storm damage? Free, no-pressure estimates for stone coated steel roofing anywhere in Texas.", "Free quote")
                 + f'<section class="section"><div class="wrap two" style="align-items:start"><div class="prose">{intro}<ul><li>Residential, commercial, multifamily and HOA</li><li>Decra, Tilcor, TEK, Roser, Westlake Royal, Gerard and more</li><li>Hail, wind and hurricane damage documentation</li></ul><p>Prefer to talk? Call <a href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a>.</p></div><div class="quote-box rv">{lead_form("fq", "Request my free estimate")}</div></div></section>'
                 + f'<section class="section sand"><div class="wrap"><div class="sec-head center"><span class="eyebrow">What happens next</span><h2>From call to <span class="it">finished roof.</span></h2></div><div class="steps">{st}</div></div></section>')
    page("/free-quote/", "Free Quote: Stone Coated Steel Roofing Estimate | Stone Coated Roofs",
         "Request a free, no-pressure stone coated steel roofing estimate anywhere in Texas — residential or commercial, storm damage or planned replacement.",
         html_body, graph=[crumbs_ld(trail)], no_popup=True)


def listing(path, trail, h1, lede, eyebrow, posts, title, description, chips_active, page_no=1, pages=1, base=None):
    chips = '<nav class="filters" aria-label="Topics">' + f'<a href="/blog/"{" aria-current=page" if chips_active == "all" else ""}>All guides</a>' + "".join(
        f'<a href="{c["path"]}"{" aria-current=page" if chips_active == c["slug"] else ""}>{E(c["name"])}</a>' for c in WP["categories"]) + '<a href="/tools/">Tools</a></nav>'
    pager = ""
    if pages > 1:
        base = base or path
        links = [f"<span>{i}</span>" if i == page_no else f'<a href="{base if i == 1 else f"{base}page/{i}/"}">{i}</a>' for i in range(1, pages + 1)]
        pager = '<nav class="pager" aria-label="Pages">' + "".join(links) + "</nav>"
    cards = "".join(post_card(p, lazy=i > 2) for i, p in enumerate(posts))
    body = phero(trail, h1, lede, eyebrow) + f'<section class="section"><div class="wrap">{chips}<div class="grid g3">{cards}</div>{pager}</div></section>' + cta_band()
    graph = [crumbs_ld(trail), {"@type": "CollectionPage", "name": strip_tags(h1), "url": f"{ORIGIN}{path}",
                                "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}{p['path']}"} for i, p in enumerate(posts)]}}]
    prevnext = ""
    if pages > 1:
        b = base or path
        if page_no > 1:
            prevnext += f'<link rel="prev" href="{ORIGIN}{b if page_no == 2 else f"{b}page/{page_no - 1}/"}">'
        if page_no < pages:
            prevnext += f'<link rel="next" href="{ORIGIN}{b}page/{page_no + 1}/">'
    page(path, title, description, body, graph=graph, extra_head=prevnext, group="category" if chips_active not in ("all",) else "page")


def build_blog():
    pages = math.ceil(len(POSTS) / PER_PAGE)
    for n in range(1, pages + 1):
        chunk = POSTS[(n - 1) * PER_PAGE:n * PER_PAGE]
        path = "/blog/" if n == 1 else f"/blog/page/{n}/"
        trail = [("Home", "/"), ("Blog", "/blog/")] + ([(f"Page {n}", path)] if n > 1 else [])
        listing(path, trail, "Stone Coated Roofing <span class='it'>Guides</span>" + (f" — Page {n}" if n > 1 else ""),
                f"{len(POSTS)} plain-English guides from {BRAND}: cost, lifespan, problems, hail and hurricane performance, insurance and commercial roofing in Texas.",
                "Blog", chunk, f"Stone Coated Roofing Blog{f' — Page {n}' if n > 1 else ''} | {BRAND}",
                "Stone coated steel roofing guides for Texas: costs, pros and cons, problems, hail and hurricane performance, insurance discounts and brand reviews." + (f" Page {n}." if n > 1 else ""),
                "all", n, pages, "/blog/")
    for c in WP["categories"]:
        posts = [p for p in POSTS if c["id"] in p["categories"]]
        trail = [("Home", "/"), ("Blog", "/blog/"), (c["name"], c["path"])]
        listing(c["path"], trail, E(CAT_TITLE[c["slug"]]), CAT_BLURB[c["slug"]], f"Topic · {len(posts)} guides", posts,
                f"{CAT_TITLE[c['slug']]} | {BRAND}" if len(CAT_TITLE[c['slug']]) < 44 else CAT_TITLE[c["slug"]],
                CAT_BLURB[c["slug"]][:158], c["slug"])


def build_privacy():
    trail = [("Home", "/"), ("Privacy Policy", "/privacy-policy/")]
    body = f"""<p>This policy explains what information {BRAND} (stonecoatedroofs.com) collects and how it is used.</p>
<h2>Information you give us</h2><p>When you request an estimate we collect the details you enter — name, phone number, email, city, property type and the reason for your request — and the page you sent it from. We use them only to contact you about your roofing project and to prepare an estimate.</p>
<h2>Information collected automatically</h2><p>Like most websites, our host records standard server logs (IP address, browser type, pages requested). The interactive tools on this site store your inputs and checklist progress in your own browser's local storage; that information never leaves your device unless you submit a form.</p>
<h2>Sharing</h2><p>We do not sell your information. We may share project details with a roofing manufacturer for warranty registration or with your insurance carrier at your request.</p>
<h2>Retention and your choices</h2><p>We keep estimate requests for as long as needed to serve you and meet record-keeping obligations. To review or delete your information, call {BIZ['phone_display']}.</p>
<h2>Changes</h2><p>We may update this policy; the date below shows the latest revision.</p><p><em>Last updated {fmt_date(TODAY)}.</em></p>"""
    html_body = phero(trail, "Privacy Policy") + f'<div class="wrap" style="padding:64px var(--gut)"><article class="prose">{body}</article></div>'
    page("/privacy-policy/", f"Privacy Policy | {BRAND}", f"How {BRAND} collects and uses the information you share when requesting a stone coated roofing estimate.", html_body, graph=[crumbs_ld(trail)])


def build_404():
    body = (f'<section class="phero noimg not-found"><div class="wrap"><div><span class="eyebrow">404</span><h1>That page blew <span class="it">off the roof.</span></h1>'
            f'<p class="lede">The page you were looking for has moved or no longer exists.</p><p style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn" href="/">Back to home</a><a class="btn btn-ghost" style="color:#fff" href="/blog/">Browse guides</a><a class="btn btn-ghost" style="color:#fff" href="/service-area/">Find your city</a></p></div></div></section>')
    page("/404.html", f"Page not found | {BRAND}", "This page could not be found.", body, robots="noindex,follow", sitemap=False)


# ------------------------------------------------------------------ output
def out_file(path):
    if path == "/":
        return OUT / "home.html"
    if path.endswith(".html"):
        return OUT / path.lstrip("/")
    return OUT / path.strip("/") / "index.html"


def write_sitemaps():
    groups = {"page": [], "post": [], "category": []}
    for path, p in sorted(PAGES.items()):
        if p["sitemap"]:
            groups[p["group"]].append((path, p["lastmod"]))
    def urlset(rows):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "".join(f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{m}</lastmod></url>\n" for u, m in rows) + "</urlset>\n")
    for g, fname in (("page", "page-sitemap.xml"), ("post", "post-sitemap.xml"), ("category", "category-sitemap.xml")):
        (OUT / fname).write_text(urlset(groups[g]))
    (OUT / "sitemap_index.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                          + "".join(f"  <sitemap><loc>{ORIGIN}/{f}</loc><lastmod>{TODAY}</lastmod></sitemap>\n" for f in ("page-sitemap.xml", "post-sitemap.xml", "category-sitemap.xml"))
                                          + "</sitemapindex>\n")
    (OUT / "sitemap.xml").write_text(urlset(groups["page"] + groups["post"] + groups["category"]))
    (OUT / "robots.txt").write_text(f"User-agent: *\nDisallow: /home.html\nDisallow: /quote.php\n\nSitemap: {ORIGIN}/sitemap_index.xml\nSitemap: {ORIGIN}/sitemap.xml\n")


def clean_output():
    """Remove previously generated pages (everything but assets, uploads and hand-written files)."""
    keep = {"assets", "wp-content", "index.php", "quote.php", ".user.ini", "scr-leads", "scr-config.php",
            "favicon.ico", "favicon.svg", "favicon-48x48.png", "favicon-96x96.png", "apple-touch-icon.png",
            "web-app-manifest-192x192.png", "web-app-manifest-512x512.png", "site.webmanifest"}
    for child in OUT.iterdir():
        if child.name in keep:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


TOOL_CARDS_SMALL = "".join(
    f'<a class="card lift" href="{t["path"]}" style="padding:22px"><span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{t["icon"]}"/></svg></span><h3 style="font-size:1.15rem">{t["name"]}</h3><span class="more">Open</span></a>'
    for t in tools.TOOLS[1:4])


LINK_FIXES = {  # hand-checked where the closest-name match would be wrong
    "/blog/benefits-of-class-4-roofing-in-texas/": "/class-4-stone-coated-roofing/",
    "/blog/benefits-of-stone-coated-steel-roofs/": "/pros-and-cons-of-stone-coated-steel-roofing/",
    "/blog/class-4-impact-resistant-roofing/": "/class-4-stone-coated-roofing/",
    "/blog/stone-coated-metal-roofing/": "/what-is-stone-coated-steel-roofing/",
    "/blog/stone-coated-slate-alternatives/": "/stone-coated-vs-synthetic-slate/",
    "/blog/stone-coated-steel-roof-cost/": "/stone-coated-roofing-cost-texas/",
    "/blog/how-long-do-stone-coated-steel-roof-warranties-last/": "/stone-coated-steel-roof-warranty/",
    "/class-4-roofing-insurance-discounts/": "/insurance-discounts-for-class-4-roofing/",
}


def fix_links(doc):
    """Old posts link to /blog/<slug>/ URLs that never existed; point each at the closest real page."""
    import difflib
    real = [u for u in PAGES if u.endswith("/")]
    def sub(m):
        h = m.group(1)
        if h in PAGES or not h.startswith("/") or h.startswith("/wp-content/") or "." in h.rsplit("/", 1)[-1] or h.startswith("/assets/"):
            return m.group(0)
        if h not in LINK_FIXES:
            slug = h.rstrip("/").rsplit("/", 1)[-1]
            cand = f"/{slug}/"
            if cand not in PAGES:
                best = difflib.get_close_matches(cand, real, n=1, cutoff=0.5)
                cand = best[0] if best else "/blog/"
            LINK_FIXES[h] = cand
        return f'href="{LINK_FIXES[h]}"'
    return re.sub(r'href="(/[^"#?]*)"', sub, doc)


def main():
    clean_output()
    homepage.build(globals())
    build_posts()
    build_areas()
    build_service_area()
    build_why_replace()
    build_commercial()
    build_quote()
    build_blog()
    tools.build(globals())
    build_privacy()
    build_404()
    for p in PAGES.values():
        p["html"] = fix_links(p["html"])
    used = {k: v for k, v in sorted(LINK_FIXES.items())}
    (ROOT / "content" / "link-fixes.json").write_text(json.dumps(used, indent=1))
    # the same map, as 301s for anyone who follows the old links from elsewhere
    (OUT / "redirects.php").write_text("<?php\n// Generated by build.py: dead WordPress-era links -> live pages (served as 301s by index.php).\nreturn "
                                       + "[\n" + "".join(f"    {json.dumps(k)} => {json.dumps(v)},\n" for k, v in used.items()) + "];\n")
    for path, p in PAGES.items():
        f = out_file(path)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(p["html"])
    write_sitemaps()
    print(f"built {len(PAGES)} pages -> {OUT}")


if __name__ == "__main__":
    main()
