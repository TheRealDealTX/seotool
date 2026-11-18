#!/usr/bin/env python3
"""Static site generator for kansasinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import os
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from services import SERVICES  # noqa: E402
from locations import LOCATIONS  # noqa: E402
from learn import PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Kansas Insurance Appraiser"
HOST = "kansasinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261117a"
FAV = "1"

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = "GTM-MF386JDG"
# The head tag exactly as provided by the site owner. Leave GTM_HEAD empty to fall back to the standard GTM snippet.
GTM_HEAD = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-MF386JDG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/what-we-handle/"
LOC_BASE = "/kansas-cities-served/"
TOOL_BASE = "/claim-calculators-kansas/"
POST_BASE = "/kansas-appraisal-guides/"
PROCESS = "/kansas-appraisal-process/"
FAQ_P = "/kansas-claim-faq/"
GLOSS = "/kansas-claim-glossary/"
ABOUT = "/about-our-kansas-firm/"
CONTACT = "/request-kansas-claim-review/"
PRIVACY = "/privacy-information-ks/"
TERMS = "/website-terms-ks/"
DISCLAIM = "/appraisal-disclaimer-ks/"
SITEMAP = "/kansas-page-index/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraiser/"


def loc_label(l):
    return f"{l['city']}, KS"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {k: v["alt"] for k, v in PHOTOS.items()}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appointed-appraiser-representation": "consultation", "home-insurance-appraisal": "ranch-home",
    "commercial-hoa-appraisal": "commercial-roof", "hail-roof-appraisal": "hail-roof",
    "tornado-wind-appraisal": "tornado", "ice-storm-freeze-appraisal": "ice-storm",
    "water-damage-appraisal": "water-ceiling", "fire-smoke-appraisal": "house-fire",
    "wildfire-grass-fire-appraisal": "grass-fire", "farm-ranch-building-appraisal": "metal-barn",
    "claim-estimate-review": "estimate-review", "appraisal-umpire-services": "documents",
}
LOC_PHOTO = {
    "wichita": "wichita", "overland-park": "suburb-street", "kansas-city": "kansas-city", "olathe": "new-homes",
    "topeka": "topeka-capitol", "lawrence": "lawrence", "manhattan": "flint-hills", "salina": "grain-elevator",
    "hutchinson": "hutchinson", "dodge-city": "dodge-city", "garden-city": "garden-city", "hays": "prairie-road",
}
TOOL_PHOTO = {
    "appraisal-payoff-projector": "calculator", "holdback-recovery-calculator": "estimate-review",
    "roof-square-footage-pitch-calculator": "shingle-roof", "percentage-deductible-converter": "storm-front",
    "claim-timeline-builder": "clipboard", "appraisal-prep-scorecard": "documents",
    "roof-age-payment-schedule-calculator": "roofer",
}
POST_PHOTO = {
    "kansas-hail-claim-roof-schedules": "hail-roof", "appraisal-attorneys-and-kansas-fee-statutes": "consultation",
    "documenting-tornado-damage-kansas": "tornado-damage", "grass-fire-claims-kansas-farms": "grass-fire",
    "choosing-an-appraisal-umpire": "documents", "matching-siding-shingles-after-hail": "siding",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(cls="mark"):
    # Navy tile, gold roof chevron, three white "estimate" lines.
    return (f'<svg class="{cls}" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="10" fill="#002569"/>'
            '<path d="M9 23L24 11l15 12" fill="none" stroke="#F1AD02" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M16 28h16M16 33.5h16M16 39h10" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')


def brand(extra=""):
    return f'<a class="brand{extra}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Kansas</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "KS", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-KS", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for Kansas property claims that came up short",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed hail, wind, fire and water claims across all 105 Kansas counties.",
        "areaServed": [{"@type": "State", "name": "Kansas"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Tornado damage", "Roof payment schedules", "Property claim valuation"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ---------------------------------------------------------------- layout
LEARN = [("Kansas appraisal process", PROCESS), ("Claim FAQ", FAQ_P), ("Claim glossary", GLOSS), ("Appraisal guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Kansas cities", LOC_BASE), True),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE), False),
        ("Resources", LEARN, None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("plus", "pl")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-gold head-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<a class="nojs-menu" href="{SITEMAP}">Menu</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div><div class="progress" aria-hidden="true"></div></header>
<div class="drawer-bg" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand(" brand-dark")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm Central · All 105 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS[:5])
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Short on a hail, wind or fire claim? Get a second set of numbers.</h2><div class="btn-row"><a class="btn btn-navy" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-dark" href="{CONTACT}">Send claim details</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand(" brand-foot")}
<p>Independent appraisal and estimating for property owners with disputed insurance claims, from the Kansas City suburbs to the High Plains.</p>
<p class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm Central · Statewide</span></p></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Cities</h3><ul>{loc}<li><a href="{LOC_BASE}">All Kansas cities</a></li></ul></div>
<div><h3>Calculators</h3><ul>{tl}<li><a href="{TOOL_BASE}">All calculators</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="{ABOUT}">About</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Content on this site is general and educational; policy terms vary and results are never guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free claim review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    if GTM_HEAD:
        return "<!-- Google Tag Manager -->\n" + GTM_HEAD + "\n<!-- End Google Tag Manager -->\n"
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, page_class=""):
    canonical = DOMAIN + path
    page_type, extra_nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        if t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = preload or "hero"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
    if main:
        webpage["mainEntity"] = {"@id": main[0]}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Kansas">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Kansas">
<meta name="geo.region" content="US-KS">
<meta name="geo.placename" content="Kansas">
<meta name="theme-color" content="#002569">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Sofia+Sans+Condensed:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.remove("no-js");document.documentElement.classList.add("js");</script>
<script type="application/ld+json">{ld}</script>
</head>
<body class="{page_class}">
{gtm_body()}{header()}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/app.js?v={VER}" defer></script>
</body>
</html>
"""


def write(path, content, priority=0.6, sitemap=True):
    # Directory pages are served as dir/index.php: the host serves real files without running the
    # front controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
        depth = rel.count("/")
        content = f"<?php require_once dirname(__DIR__, {depth}) . '/_guard.php'; ?>\n" + content
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">›</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.15"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary><span>{e(q)}</span>{ic("plus", "pl")}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-t">Talk it through, free</h2><p>A short first call. We’ll tell you honestly whether appraisal is worth it.</p><a class="side-phone" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-t">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def cta_band(h="Numbers on your claim don’t add up?", p="Send the insurer’s estimate. We’ll read it line by line and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="rel-grid">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Tornado / wind", "Ice storm / freeze", "Water / leak", "Fire / smoke", "Grass fire / wildfire", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", sub="Free review, no obligation. We usually reply within one business day.", page="/", hl="h3"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Farm or ranch owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Kansas"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="form-t">{e(heading)}</{hl}><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="{PRIVACY}">privacy information</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-card" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hero-card-t">Free claim check</h2><p class="form-sub">Tell us a little. We’ll call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{PRIVACY}">privacy information</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Check my claim {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hero-card-note">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Kansas City Metro", "Overland Park · Olathe · Kansas City", "suburb-street",
     "Hail, finished-basement water losses and HOA rules about shingles and siding. Higher metro labor rates that statewide price lists miss."),
    ("Northeast & Flint Hills", "Topeka · Lawrence · Manhattan", "flint-hills",
     "Tornado history from Topeka to Manhattan, historic homes with plaster and wood siding, limestone buildings and university rentals."),
    ("South Central", "Wichita · Hutchinson · Andover", "wichita",
     "One of the busiest hail corridors in the country, plus tornado and grass fire losses. Big storms mean thousands of claims at once."),
    ("North Central & Smoky Hills", "Salina · Abilene · Concordia", "main-street",
     "Hail and straight-line wind on homes, commercial buildings along the interstates and farmsteads across rolling country."),
    ("Northwest", "Hays · Colby · Goodland", "prairie-road",
     "Limestone homes, metal farm buildings and wind-driven fires such as the December 2021 Four County Fire."),
    ("Southwest High Plains", "Dodge City · Garden City · Liberal", "wheat-storm",
     "Large hail, tornadoes, blowing dust and prairie fire, with contractor travel adding real cost to repairs."),
]


def home():
    K = BRAND
    svc_cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span><span class="pcard-b"><span class="pcard-n">{i + 1:02d}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="pcard-go">Learn more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES[:9]))
    steps = [
        ("Free claim check", "We read your policy, the insurer’s estimate and your photos, then tell you whether appraisal makes sense."),
        ("Our own valuation", "We inspect and measure the property and build a line-item estimate priced for your part of Kansas."),
        ("Written demand", "Appraisal is demanded in writing and you name a Kansas Insurance Appraiser as your appraiser on time."),
        ("Panel work", "We work through the differences with the insurer’s appraiser, line by line, with photos and measurements."),
        ("Signed award", "Open items go to a neutral umpire. Two signatures set the amount of loss and payment follows the policy."),
    ]
    track = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    regions = "".join(
        f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div></article>'
        for n, c, ph, t in REGIONS)
    tools = "".join(
        f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="trow-ph">{img(TOOL_PHOTO[t["slug"]], sizes="160px", alt="")}</span><span class="trow-b"><small>{e(t["kind"])}</small><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span>{ic("arrow", "trow-ar")}</a>'
        for t in TOOLS)
    cities = "".join(f'<a class="city rv" href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    posts = "".join(
        f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><small>{p["read"]} read · Guide</small><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree a loss is covered but disagree on the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the insurer’s estimate and the gap between it and your contractor’s number is meaningful, generally more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, yes, once any two of the three panel members sign it. That is why documentation matters before appraisal is demanded."),
        ("What will it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my part of Kansas?", "Yes. We work in all 105 Kansas counties, including Wichita, the Kansas City suburbs, Topeka, Lawrence, Manhattan, Salina, Hays, Dodge City and Garden City."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero", lazy=False, alt="", extra=' data-parallax="0.2"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-light">Independent claim appraisal · All 105 counties</p>
<h1><span>{K}</span> for hail, wind &amp; fire claims that came up short</h1>
<p class="lede">The insurer accepted your claim, but the check won’t cover the repair. A {K} builds an independent, line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="#services">See how we help {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Homes, farms, HOAs &amp; commercial</li><li>{ic("check")}Local pricing, not a template</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="sec sec-intro"><div class="wrap split">
<div class="rv">
<p class="kicker"><b>01</b> Covered, but underpaid</p>
<h2>Why Kansans call a {K}</h2>
<p>Most short claims aren’t denied. They’re just short: a few slopes approved on a roof the hail hit everywhere, siding patched where it can’t be matched, gutters and screens left off, an old roof pushed onto a payment schedule with the wrong age. A {K} exists for that gap between “covered” and “paid in full.”</p>
<ul class="ticks">
<li>{ic("ruler")}<div><b>We measure it ourselves</b><span>Our own inspection, not an edited copy of the insurer’s estimate.</span></div></li>
<li>{ic("scale")}<div><b>Defensible numbers</b><span>Estimates built to hold up in front of an umpire, not to impress on first read.</span></div></li>
<li>{ic("shield")}<div><b>Straight answers</b><span>If your claim needs an attorney or just a supplement, we’ll tell you on the first call.</span></div></li>
</ul>
<a class="btn btn-navy" href="{ABOUT}">About our approach {ic("arrow")}</a>
</div>
<figure class="intro-fig rv">{img("hail-roof", sizes="(max-width:1000px) 100vw, 520px")}<figcaption><b>Kansas is hail country.</b> Our work starts with every slope, vent, gutter and screen the storm touched.</figcaption></figure>
</div></section>

<section class="counts" aria-label="At a glance"><div class="wrap counts-in">
<div class="rv"><b data-count="105">105</b><span>Kansas counties served by a {K}</span></div>
<div class="rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal and estimating services</span></div>
<div class="rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
<div class="rv"><b>2 of 3</b><span>Signatures make an award binding</span></div>
</div></section>

<section class="sec" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker"><b>02</b> Services</p><h2>Claims a {K} values</h2><p>Twelve services, one goal: a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="pgrid" data-stagger>{svc_cards}</div>
<p class="center"><a class="btn btn-line-dark" href="{SVC_BASE}">All {len(SERVICES)} services, including farm and umpire work {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-navy"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-light"><b>03</b> The process</p><h2>How a {K} moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is the path from first call to signed award.</p></div>
<ol class="track" data-track><span class="track-line" aria-hidden="true"><span class="track-fill"></span></span>{track}</ol>
<p class="center"><a class="link-light" href="{PROCESS}">Read the full Kansas appraisal process guide</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker"><b>04</b> Statewide</p><h2>From the Kansas City suburbs to the High Plains</h2><p>Hail in Wichita, tornadoes in Topeka, ice in Lawrence, prairie fire near Hays. A {K} has to know how each region’s weather shows up on a roof, and in an estimate.</p></div>
<div class="region-grid" data-stagger>{regions}</div>
</div></section>

<section class="sec sec-sky" id="check"><div class="wrap split">
<div class="rv"><p class="kicker"><b>05</b> Quick check</p><h2>Is the gap worth an appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a {K} makes sense. If it’s small, a documented supplement may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-projector/">appraisal payoff projector</a> adds appraiser and umpire fees so you see a realistic net figure. Example numbers are illustrative.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv sticky-col"><p class="kicker"><b>06</b> Free calculators</p><h2>Free claim calculators from a {K}</h2><p>Run the numbers before you pick up the phone. Every calculator works in your browser and nothing you type is stored or sent.</p><a class="btn btn-navy" href="{TOOL_BASE}">Open all calculators {ic("arrow")}</a></div>
<div class="trows" data-stagger>{tools}</div>
</div></section>

<section class="sec sec-cities"><div class="wrap">
<div class="sec-head rv"><p class="kicker"><b>07</b> Cities</p><h2>Where a {K} works most often</h2><p>We serve every county in the state. These are the cities where our claims come from most, each with its own storms, housing and repair costs.</p></div>
<div class="city-grid" data-stagger>{cities}</div>
<p class="center"><a class="btn btn-line-dark" href="{LOC_BASE}">See all Kansas coverage {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-sky"><div class="wrap">
<div class="sec-head rv"><p class="kicker"><b>08</b> Before you demand</p><h2>Three questions to answer first</h2></div>
<div class="q3" data-stagger>
<div class="q3-card rv"><span>1</span><h3>Is coverage accepted?</h3><p>Appraisal values a covered loss. If the insurer denied the claim or cited an exclusion, talk to a Kansas attorney before anything else.</p></div>
<div class="q3-card rv"><span>2</span><h3>Is the gap big enough?</h3><p>Fees come out of the increase. A gap of a few hundred dollars rarely justifies appraisal; a missed roof replacement often does.</p></div>
<div class="q3-card rv"><span>3</span><h3>Is your file complete?</h3><p>Both line-item estimates, dated photos and your policy. The <a href="{TOOL_BASE}appraisal-prep-scorecard/">appraisal prep scorecard</a> shows what is missing.</p></div>
</div>
</div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv"><p class="kicker"><b>09</b> FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_P}">All FAQs {ic("arrow")}</a><a class="btn btn-line-dark" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sec-sky"><div class="wrap">
<div class="sec-head rv"><p class="kicker"><b>10</b> Guides</p><h2>Reading from the {K} desk</h2><p>Practical guides on hail claims, roof schedules, tornado documentation and choosing an umpire.</p></div>
<div class="ggrid" data-stagger>{posts}</div>
<p class="center"><a class="btn btn-line-dark" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-navy" id="contact"><div class="wrap split split-top">
<div class="rv"><p class="kicker kicker-light"><b>11</b> Start here</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm Central</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 105 Kansas counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Hail, Wind & Fire Claims",
                        "Kansas Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, fire and water claims.",
                        body, [faq_schema(home_faqs)], preload="hero", page_class="is-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Cities we serve", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All Kansas cities", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Kansas"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}, faq_schema(s["faqs"])]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="icard-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we handle", "Kansas Insurance Appraisal Services",
                     "From a single estimate review to full panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of your Kansas property loss.", "roofer") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec sec-sky"><div class="wrap split split-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that is worth. A review answers that in days, and many disputes close right there.</p><a class="btn btn-navy" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial claims?", "Yes: homes, condos, farms and ranches, retail, office, warehouse, churches and HOA communities."), ("Is it only hail?", "No. We handle tornado, wind, ice, water, fire and grass fire losses too.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{SVC_BASE}{s["slug"]}/', "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    write(SVC_BASE, document(SVC_BASE, "Kansas Insurance Appraisal Services | 12 Ways",
                             "Kansas insurance appraisal services: appraisal clause work, hail, tornado, ice, water, fire, grass fire, farm, estimate review and umpire.",
                             body, schema, preload="roofer"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Kansas cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks in {e(l["city"])}</b><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
<aside class="aside">{call_box()}{list_box("Kansas cities", items, path)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Kansas"}}, "url": DOMAIN + path}, faq_schema(l["faqs"])]
        title = f"{l['city']} Insurance Appraiser | {l['county']}, KS"
        if len(title) > 58:
            title = f"{l['city']}, KS Insurance Appraiser | Claim Appraisal"
        desc = f"Insurance appraiser for {l['city']} and {l['county']}: independent appraisal and estimate review for underpaid hail, wind and fire claims."
        if len(desc) > 143:
            desc = f"Insurance appraiser for {l['city']}, {l['county']}: appraisal and estimate review for underpaid hail, wind and fire claims."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Kansas cities", LOC_BASE)]
    cities = "".join(f'<a class="city rv" href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    reg = "".join(f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:700px) 100vw, 33vw", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div></article>' for n, c, ph, t in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 105 Kansas Counties",
                     "We work statewide, from Wyandotte County to the High Plains. These local pages cover the cities where our claims come from most often.", "kansas-prairie") + f"""
<section class="sec"><div class="wrap"><h2 class="sr-only">Cities</h2><div class="city-grid" data-stagger>{cities}</div></div></section>
<section class="sec sec-sky"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across Kansas</h2><p>The same policy language plays out differently on a Johnson County split-level, a Hays limestone farmhouse and a Garden City metal shop.</p></div><div class="region-grid" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your town?", "We cover every Kansas county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Kansas Cities Served | Statewide Claim Appraisal",
                             "Insurance appraisal across all 105 Kansas counties, including Wichita, Overland Park, Topeka, Lawrence, Salina, Hays and Garden City.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + loc_path(l), "name": loc_label(l)} for i, l in enumerate(LOCATIONS)]}], preload="kansas-prairie"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec sec-tool"><div class="wrap"><h2 class="sr-only">{e(t["name"])}</h2><div class="rv">{t["markup"]}</div>
<p class="hint tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("All calculators", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}, faq_schema(t["faqs"])]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    rows = "".join(f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="trow-ph">{img(TOOL_PHOTO[t["slug"]], sizes="160px", alt="")}</span><span class="trow-b"><small>{e(t["kind"])}</small><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span>{ic("arrow", "trow-ar")}</a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Claim Calculators for Kansas Property Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Check the insurer’s math, see what a roof schedule does to a hail payout and plan your next step. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="trows trows-wide" data-stagger>{rows}</div></div></section>
<section class="sec sec-sky"><div class="wrap split split-top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a> so nothing lapses.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-square-footage-pitch-calculator/">roof square footage &amp; pitch calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}percentage-deductible-converter/">deductible converter</a>, the <a href="{TOOL_BASE}roof-age-payment-schedule-calculator/">roof schedule calculator</a> and the <a href="{TOOL_BASE}holdback-recovery-calculator/">holdback calculator</a>.</li><li>Size the dispute with the <a href="{TOOL_BASE}appraisal-payoff-projector/">appraisal payoff projector</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-prep-scorecard/">prep scorecard</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{TOOL_BASE}{t["slug"]}/', "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    write(TOOL_BASE, document(TOOL_BASE, "Free Kansas Claim Calculators | 7 Tools",
                              "Free Kansas claim calculators: appraisal payoff, holdback, roof squares, percentage deductible, roof age schedule, timeline and scorecard.",
                              body, schema, preload="calculator"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "The Kansas Insurance Appraisal Process, Step by Step",
                     "Eight steps from the first disagreement to a signed award: what happens, who does what and where Kansas claims most often go wrong.", "clipboard",
                     [("Steps", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band()}"""
    names = ["Confirm the dispute is about money", "Put the gap on paper", "Send the written demand", "Each side names an appraiser", "The appraisers select an umpire", "The appraisers work the differences", "The umpire decides what remains", "The award and payment"]
    howto = {"@type": "HowTo", "name": "How the Kansas insurance appraisal process works", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": DOMAIN + path} for i, n in enumerate(names)]}
    write(path, document(path, "Kansas Insurance Appraisal Process | 8 Steps",
                         "The Kansas insurance appraisal process in eight steps: the written demand, choosing appraisers and an umpire, panel work and the award.",
                         body, [crumbs_schema(trail), howto], preload="clipboard"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Claim FAQ", path)]
    groups = "".join(f'<h2>{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    toc = "".join(f'<li>{e(g)}</li>' for g, _ in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Kansas Insurance Claim and Appraisal FAQ",
                     "Plain answers grouped by topic: appraisal basics, Kansas specifics, cost and timing, and what happens after the award.", "kitchen") + f"""
<div class="wrap layout"><article class="prose"><div class="note"><b class="h">Topics on this page</b><ul class="chips">{toc}</ul></div>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Kansas Claim & Appraisal FAQ | By Topic",
                         "Kansas claim and appraisal FAQ grouped by topic: how appraisal works, the Kansas FAIR Plan, costs, timing and binding awards.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="kitchen"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Kansas Property Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the box to filter.", "documents", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “schedule” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Kansas property claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Kansas Claim Glossary | 42 Insurance Terms",
                         "Searchable Kansas claim glossary: plain-English definitions of ACV, RCV, roof payment schedules, umpire, holdback and more.",
                         body, [crumbs_schema(trail), dts], preload="documents"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "publisher": {"@id": DOMAIN + "/#business"}, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides", "Kansas Insurance Appraisal Guides",
                     "Practical reading on hail claims, roof schedules, tornado documentation, grass fires and choosing an umpire, written by people who work appraisal panels.", "siding", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Kansas Insurance Appraisal Guides | Claim Reading",
                         "Kansas insurance appraisal guides on hail claims, roof schedules, tornado and grass fire documentation, umpires and matching siding.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{POST_BASE}{p["slug"]}/', "name": p["title"]} for i, p in enumerate(POSTS)]}], preload="siding"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", "About Kansas Insurance Appraiser",
                     "We are estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "consultation") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("estimate-review", sizes="(max-width:1000px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Many property claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built to answer it well. That lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Measure first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You will understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, farm and ranch owners, churches, business owners, contractors, public adjusters and attorneys across Kansas. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t guarantee outcomes, and no honest appraiser can. We don’t publish testimonials or client results.</p>
<h2>Statewide on purpose</h2>
<p>Kansas weather changes from the wooded northeast to the High Plains. Working statewide means we see every kind of loss the state produces, from basement water in Overland Park to hail in Wichita and grass fire near Hays, and we price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Kansas cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Kansas Insurance Appraiser | Our Approach",
                         "Kansas Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="consultation"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Request a Kansas Claim Review",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec sec-navy"><div class="wrap split split-top">
<div class="rv"><h2>Reach us directly</h2>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm Central</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>Statewide, all 105 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks-light"><li>Declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Request a Kansas Claim Review | (844) 537-1427",
                         "Request a free review of a disputed Kansas property claim. Call or text (844) 537-1427 or email us your estimate and photos.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="consultation"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Information", "Privacy Information | Kansas Insurance Appraiser",
                  "How Kansas Insurance Appraiser collects, uses and protects the information you share through our forms, calls, email and calculators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone, email, property location and claim details. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and scorecard run in your browser. The numbers you type aren’t sent to us or stored on our servers.</p>
<h2>Cookies and fonts</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics in the future, this page will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you gave us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Website Terms", "Website Terms of Use | Kansas Insurance Appraiser",
                "The website terms that apply when you use Kansas Insurance Appraiser’s pages, calculators and contact forms. Please read them first.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Kansas.</p>
<h2>No professional relationship</h2><p>Reading this site, using its calculators or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Kansas attorney for legal questions.</p>
<h2>Calculators</h2><p>Calculators give planning estimates from the figures you enter. They are not appraisals, quotes or predictions of any outcome.</p>
<h2>Content and photos</h2><p>Site text, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Kansas.</p>""", "The terms that apply when you use this website and its calculators."),
        DISCLAIM: ("Appraisal Disclaimer", "Appraisal Disclaimer | Kansas Insurance Appraiser",
                   "Important limits on the information on Kansas Insurance Appraiser’s website: general content, not legal advice, and no guaranteed results.", f"""
<h2>General information only</h2><p>Content on this website is educational. It describes how insurance appraisal commonly works, but your policy’s language controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Kansas law references</h2><p>References to Kansas statutes, such as K.S.A. 40-256 and 40-908, the Kansas Insurance Department or the Kansas FAIR Plan are general background. Laws and court decisions change; confirm current law with official sources or a Kansas attorney.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. We don’t publish testimonials, and no appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes any deadline. If one is approaching, consult a Kansas attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h1, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office-building", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], preload="office-building"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Kansas cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy information", PRIVACY), ("Website terms", TERMS), ("Appraisal disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="smap rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Kansas Insurance Appraiser Site Map", f"Every page on {BRAND}, grouped by section.", "office-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="smap-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete site map of {BRAND}: services, Kansas cities, free claim calculators, guides and legal pages.", body, [crumbs_schema(trail)], preload="office-building"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-bg">{img("kansas-prairie", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-light">Error 404</p><h1>This page blew off somewhere over the prairie</h1><p class="lede">The page you’re looking for has moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line" href="{SVC_BASE}">Services</a><a class="btn btn-line" href="{TOOL_BASE}">Calculators</a><a class="btn btn-line" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "The page you requested on Kansas Insurance Appraiser could not be found. Use the links on this page to find services or calculators.",
                                body, robots="noindex,follow"), sitemap=False)


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(xml) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, "_guard.php"), "w") as f:
        f.write(GUARD_PHP)
    # Search Console verification: exact single line, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Kansas Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$kia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$kia_real  = 'kansasinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$kia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://kansasinsuranceappraiser.com - only on the real domain.
if ($kia_host === 'www.' . $kia_real || ($kia_host === $kia_real && $kia_proto === 'http')) {
    header('Location: https://' . $kia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $kia_m)) {
    $kia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $kia_m[1] . $kia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($kia_host !== $kia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Kansas Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (a directory's index.php included)
// and routes "/" and unknown paths here.
require_once __DIR__ . '/_guard.php';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
if ($path === '/' || $path === '/index.php') {
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.php')) {
    $q = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    header('Location: ' . $path . '/' . $q, true, 301);
    exit;
}
if (substr($path, -1) === '/' && $path !== '/' && is_file(__DIR__ . $path . 'index.php')) {
    include __DIR__ . $path . 'index.php';
    exit;
}
http_response_code(404);
readfile(__DIR__ . '/404.html');
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    sitemap_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
