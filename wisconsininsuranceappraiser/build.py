#!/usr/bin/env python3
"""Static site generator for wisconsininsuranceappraiser.com.

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
from learn import PROCESS_STEPS, PROCESS_EXTRA, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Wisconsin Insurance Appraiser"
HOST = "wisconsininsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no tag is output.
GTM_ID = ""

SVC_BASE = "/appraisal-solutions/"
LOC_BASE = "/local-appraisers/"
TOOL_BASE = "/insurance-claim-calculators/"
POST_BASE = "/learning-center/"
PROCESS = "/appraisal-process-guide/"
FAQ_URL = "/insurance-appraisal-faq/"
GLOSS = "/claims-dictionary/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"
SITEMAP_HTML = "/html-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, WI"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


def ph(*keys):
    """First photo key that exists (lets the maps fall back gracefully)."""
    for k in keys:
        if k in PHOTOS:
            return k
    raise KeyError(keys)


SVC_PHOTO = {
    "appraisal-demand-representation": ph("consultation"), "home-insurance-appraisal": ph("family-home"),
    "commercial-hoa-appraisal": ph("apartments"), "hail-roof-damage-appraisal": ph("hail-ice", "hail-shingles"),
    "tornado-straight-line-wind-appraisal": ph("tornado-damage"), "snow-load-roof-collapse-appraisal": ph("snow-roof"),
    "water-sewer-backup-appraisal": ph("ceiling-water", "flooded-basement"), "fire-smoke-damage-appraisal": ph("house-fire", "storm-trees"),
    "ice-dam-frozen-pipe-appraisal": ph("icicles"), "farm-barn-outbuilding-appraisal": ph("red-barn", "dairy-barn"),
    "carrier-estimate-review": ph("calculator"), "umpire-selection-services": ph("meeting"),
}
# City photos where a good CC0/PD image exists; otherwise a regional stand-in (lakeshore, farmland, homes).
_LOC_FALLBACK = {"kenosha": "apartments", "racine": "lake-storm", "green-bay": "storm-front", "appleton": "snow-roof", "la-crosse": "hail-sky", "oshkosh": "storm-trees",
                 "waukesha": "family-home", "eau-claire": "red-barn", "janesville": "dairy-barn"}
LOC_PHOTO = {l["slug"]: ph("city-" + l["slug"], _LOC_FALLBACK.get(l["slug"], "lake-storm"), "lake-storm") for l in LOCATIONS}
TOOL_PHOTO = {
    "settlement-gap-calculator": ph("calculator-desk"), "rcv-acv-holdback-calculator": ph("paperwork"),
    "roof-pitch-squares-calculator": ph("hail-shingles", "roof-shingles"), "percentage-deductible-calculator": ph("hail-sky", "storm-front"),
    "claim-timeline-planner": ph("clipboard", "paperwork"), "appraisal-readiness-quiz": ph("laptop-review", "consultation"),
    "roof-snow-load-calculator": ph("snow-roof"),
}
POST_PHOTO = {
    "wisconsin-appraisal-clause-guide": ph("paperwork"), "ice-dam-insurance-claims": ph("icicles"),
    "hail-claim-photo-checklist": ph("roof-tarp", "hail-shingles"), "sewer-backup-vs-flood-coverage": ph("flooded-basement", "ceiling-water"),
    "derecho-straight-line-wind-claims": ph("wind-damage", "storm-trees"), "matching-siding-and-shingles": ph("roof-shingles"),
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
    "snow": '<path d="M12 2v20M4.9 6l14.2 12M19.1 6L4.9 18M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark():
    # Navy tile, gold "W" zigzag (a valuation line) under a white roof gable.
    return ('<svg viewBox="0 0 48 48" width="46" height="46" aria-hidden="true"><rect width="48" height="48" rx="11" fill="#002986"/>'
            '<path d="M9 19l7.5 17L24 24l7.5 12L39 19" fill="none" stroke="#FFCC18" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M16.5 15.5L24 9l7.5 6.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def brand_link(sub="Independent claim appraisal"):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span><b>{BRAND}</b><small>{sub}</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "WI", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-WI", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Wisconsin property claims",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 72 Wisconsin counties.",
        "areaServed": [{"@type": "State", "name": "Wisconsin"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Ice dams", "Snow load", "Wind damage"],
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


def item_list(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_URL), ("Claims dictionary", GLOSS), ("Learning center", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Wisconsin cities", LOC_BASE), True),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE), False),
        ("Resources", LEARN, None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="full"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="head"><div class="wrap">
{brand_link()}
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone")}<span class="t">{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link()}<button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · All 72 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    res = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN) + f'<li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact us</a></li>'
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div>{brand_link()}
<p>Independent appraisal and estimating help for Wisconsin property owners whose insurance claims came up short, from the Lake Michigan shore to the North Woods.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm CT · Statewide</span></div></div>
<div><p class="foot-t">Services</p><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><p class="foot-t">Cities</p><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><p class="foot-t">Calculators</p><ul>{tl}</ul></div>
<div><p class="foot-t">Resources</p><ul>{res}</ul></div>
</div>
<div class="foot-base"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="{SITEMAP_HTML}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we don’t give legal advice and we don’t act as public adjusters. Information on this site is general and educational, and policy terms vary. Results depend on the facts of each claim and are never guaranteed.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],\n"
            f"j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None):
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
    main = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Wisconsin">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Wisconsin">
<meta name="geo.region" content="US-WI">
<meta name="geo.placename" content="Wisconsin">
<meta name="theme-color" content="#002986">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700;800&family=Mulish:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
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
        parts.append(e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>›</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts up" style="animation-delay:.3s">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row up" style="animation-delay:.22s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.12"')}<div class="wrap">{crumbs(trail)}<span class="kicker light up">{e(tag)}</span><h1 class="up" style="animation-delay:.06s">{e(h1)}</h1><p class="lede up" style="animation-delay:.14s">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div class=\"a\"><p>{e(a)}</p></div></details>" for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk it through, free</h2><p>Tell us what the insurer paid and what the repair costs. We’ll say honestly whether appraisal fits.</p><a class="call-num" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span>›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Claim paid, but not enough to fix it?", p="Send us the insurer’s estimate and your photos. We’ll tell you what we see."):
    return f"""<section class="cta-band"><div class="wrap"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line" href="{CONTACT}">Email the estimate</a></div></div></section>"""


LOSSES = ["Hail", "Wind / tornado / derecho", "Snow load or collapse", "Ice dam / frozen pipe", "Water or sewer backup", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/"):
    roles = ["Homeowner", "Business owner", "Condo association / HOA", "Farm owner", "Property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Wisconsin"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="/privacy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead-card up" style="animation-delay:.45s" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Get a free claim review</h2><p class="sub">Three quick details. We’ll call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What kind of loss?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="/privacy/">privacy policy</a>.</span></label>
<button class="btn gold" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<div class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></div>
</form>"""


# ---------------------------------------------------------------- home
SEASONS = [
    ("winter", "Winter", "Dec – Mar", "snow", "snow-roof", ["Ice dams", "Frozen & burst pipes", "Snow-load collapse", "Furnace puffbacks"],
     "Long stretches below freezing put more strain on Wisconsin homes than any single storm. Ice dams push meltwater under shingles, polar-vortex cold splits supply lines inside exterior walls, and heavy, wet snow loads test older trusses and farm buildings. These claims often surface weeks after the damage starts."),
    ("spring", "Spring", "Apr – Jun", "hail", ph("hail-sky", "storm-front"), ["Hail", "Tornadoes", "Severe thunderstorms", "Basement seepage"],
     "Severe-weather season builds through spring. Hail tracks across the southern and western counties, and tornado outbreaks such as the August 2005 storms around Stoughton show how quickly a neighborhood can change. Thawing ground and spring rain add basement water claims to the mix."),
    ("summer", "Summer", "Jul – Aug", "wind", "storm-trees", ["Derechos & straight-line wind", "Flash flooding", "Sewer backup", "Lightning & fire"],
     "Fast-moving lines of storms can flatten timber and peel roofs across several counties in an afternoon, as the July 2019 derecho did in the north. In cities, a few hours of extreme rain can overwhelm sewers: Milwaukee in 2010 and Dane County in 2018 saw widespread basement backups."),
    ("fall", "Fall", "Sep – Nov", "leaf", "family-home", ["Wind damage", "Fallen trees", "Late hail", "Pre-winter repairs"],
     "Autumn storms bring down limbs heavy with leaves, and late-season hail still happens. It’s also the deadline season for many claims: owners racing to finish roof repairs before snow, and depreciation holdback windows that close before the work can be done."),
]


def home():
    svc_cards = "".join(
        f'<a class="svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1020px) 50vw, 400px", alt="")}<span class="num">{i + 1:02d}</span></span>'
        f'<span class="bd"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="go">View service {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES[:9]))

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="si">{ic(icn)}</span>{e(n)}<small>{e(m)}</small></button>'
        for i, (k, n, m, icn, *_r) in enumerate(SEASONS))
    panels = "".join(
        f'<div class="season-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>{img(photo, sizes="(max-width:1020px) 100vw, 860px", alt="")}<div class="in"><h3>{e(n)} claims in Wisconsin</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p></div></div>'
        for i, (k, n, _m, _icn, photo, perils, t) in enumerate(SEASONS))

    steps = [
        ("Free first look", "We read the policy, the insurer’s estimate and your photos, then tell you plainly whether appraisal is the right tool for the gap you have."),
        ("Independent scope", "We inspect and measure the property ourselves and build a line-item estimate priced for your part of Wisconsin."),
        ("Written demand", "Appraisal is demanded in writing and Wisconsin Insurance Appraiser is named as your appraiser within the policy’s time limit."),
        ("Appraiser-to-appraiser work", "We go through the disagreement line by line with the insurer’s appraiser. Many disputes narrow sharply here."),
        ("Umpire and award", "Anything still unresolved goes to a neutral umpire. Signatures from two of the three set the amount of loss."),
    ]
    proc = "".join(f'<div class="tstep"><span class="dot">{i + 1}</span><div class="card rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></div>' for i, (t, p) in enumerate(steps))

    tiles = "".join(f'<a class="tool-card rv" data-tilt href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="badge"><i>{e(t["icon"])}</i>{e(t["kind"])}</span></span><span class="bd"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    locs = "".join(f'<a href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="64px", alt="")}<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    storms = [
        ("1984", "Barneveld tornado", "A violent overnight tornado in June devastated the Iowa County village west of Madison."),
        ("1996", "Oakfield tornado", "A July tornado rated F5 tore through the Fond du Lac County village of Oakfield."),
        ("2005", "August 18 outbreak", "More than two dozen tornadoes in one day, with heavy damage in and around Stoughton."),
        ("2008", "June floods", "Days of rain drained Lake Delton and flooded communities across southern Wisconsin."),
        ("2010", "Milwaukee flash flood", "A July cloudburst sent water and sewage into basements across the metro."),
        ("2018", "Dane County deluge", "Record August rainfall west of Madison flooded homes, roads and businesses."),
        ("2019", "Northern derecho", "July downbursts flattened forests and damaged roofs across the north."),
    ]
    storm_cards = "".join(f'<div class="storm rv"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for y, t, d in storms)
    guides = "".join(f'<article class="guide rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 400px", alt="")}</a><div class="bd"><span class="meta">{p["read"]} read · Guide</span><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="arrow-link" href="{POST_BASE}{p["slug"]}/">Read the guide {ic("arrow")}</a></div></article>' for p in POSTS[:3])

    home_faqs = [
        ("What does a Wisconsin Insurance Appraiser do?", "We put a dollar value on property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, when needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("When is it worth calling a Wisconsin Insurance Appraiser?", "When coverage has been accepted, you have the insurer’s estimate, and the gap between that number and a real repair price is meaningful, often more than about 10% or several thousand dollars."),
        ("Is the appraisal award final?", "On the amount of loss, an award signed by two of the three panel members is generally binding. That’s why the documentation you bring matters so much."),
        ("How are appraisal fees handled?", "Each side pays its own appraiser and usually half of the umpire. We put our fee arrangement in writing before any work starts, and the first conversation costs nothing."),
        ("Do you cover my part of Wisconsin?", "Yes. We work in all 72 counties, from Kenosha and Milwaukee to Green Bay, La Crosse, Eau Claire, Wausau and the North Woods."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero", lazy=False, alt="")}</div>
<div class="wrap">
<div>
<span class="kicker light up">Independent claim appraisal · All 72 counties</span>
<h1 class="up" style="animation-delay:.08s">Wisconsin Insurance Appraiser for claims that came up <mark>short</mark></h1>
<p class="lede up" style="animation-delay:.18s">Your insurer accepted the claim, but the check won’t cover the repair. Wisconsin Insurance Appraiser builds an independent, line-by-line valuation of the loss and takes it through the appraisal process written into your policy.</p>
<div class="btn-row up" style="animation-delay:.28s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#services">See our services {ic("arrow")}</a></div>
<ul class="hero-points up" style="animation-delay:.36s"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Homes, farms, HOAs &amp; businesses</li><li>{ic("check")}Built for Wisconsin weather</li></ul>
</div>
{hero_form()}
</div>
<div class="hero-strip"><div class="wrap"><span>{ic("snow")} Ice dams &amp; frozen pipes</span><span>{ic("hail")} Hail &amp; roof claims</span><span>{ic("wind")} Tornado &amp; derecho wind</span><span>{ic("drop")} Water &amp; sewer backup</span></div></div>
</section>

<section class="sec" id="about-appraisal"><div class="wrap">
<div class="split">
<div class="intro-photo rv-l">{img("roofer", sizes="(max-width:1020px) 100vw, 580px")}<div class="tag"><b>2 of 3</b><span>panel signatures make an appraisal award binding on the amount of loss</span></div></div>
<div class="rv-r">
<span class="kicker">Covered isn’t the same as paid</span>
<h2>Why owners bring in a Wisconsin Insurance Appraiser</h2>
<p>Most short claims aren’t denials. They’re estimates that leave things out: the second roof slope, the ice and water barrier a cold-climate roof needs, the plaster wall priced as drywall, the basement finish missing from a backup claim. A Wisconsin Insurance Appraiser is there for the space between “covered” and “paid in full.”</p>
<ul class="ticks">
<li>{ic("check")}<div><b>We start from the property, not their estimate</b><span>Our own inspection, measurements and photos, so every line can be defended.</span></div></li>
<li>{ic("check")}<div><b>Numbers built to survive an umpire</b><span>Supportable pricing moves awards. Inflated pricing loses credibility.</span></div></li>
<li>{ic("check")}<div><b>Straight answers on fit</b><span>If you need an attorney or a simple supplement instead, we say so on the first call.</span></div></li>
</ul>
<a class="btn" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div>
<div class="counters" data-counters>
<div class="counter"><b data-count="72">72</b><span>Wisconsin counties covered</span></div>
<div class="counter"><b data-count="12">12</b><span>Appraisal &amp; estimating services</span></div>
<div class="counter"><b data-count="7">7</b><span>Free claim calculators</span></div>
<div class="counter"><b data-count="4">4</b><span>Seasons of claim risk</span></div>
</div>
</div></section>

<section class="sec navy"><div class="wrap">
<div class="sec-head"><span class="kicker light">Wisconsin’s claim calendar</span><h2>Four seasons, four kinds of damage</h2><p>Every season here produces its own claims. A Wisconsin Insurance Appraiser has to know how a polar-vortex freeze, a June hailstorm and a July derecho each show up on a roof, and in an estimate.</p></div>
<div class="seasons rv" data-tabs><div class="season-tabs" role="tablist" aria-label="Seasons">{tabs}</div><div>{panels}</div></div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head c rv"><span class="kicker">Appraisal &amp; estimating</span><h2>Services from Wisconsin Insurance Appraiser</h2><p>Twelve services with one goal: a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="svc-grid" data-stagger>{svc_cards}</div>
<p class="center" style="margin-top:40px"><a class="btn line" href="{SVC_BASE}">All 12 appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head c rv"><span class="kicker">The path to an award</span><h2>How Wisconsin Insurance Appraiser moves a stalled claim</h2><p>The appraisal clause swaps an open-ended argument for a defined process with a binding result. Here’s the route from first call to signed award.</p></div>
<div class="timeline"><span class="fill"></span>{proc}</div>
<p class="center" style="margin-top:30px"><a class="arrow-link" href="{PROCESS}">Read the full appraisal process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec paper" id="calculators"><div class="wrap">
<div class="split top">
<div class="rv-l"><span class="kicker">Try it now</span><h2>Is your gap big enough to appraise?</h2><p>Enter the two numbers you already have. A large gap is worth a conversation with a Wisconsin Insurance Appraiser. A small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}settlement-gap-calculator/">settlement gap calculator</a> adds appraiser and umpire fees and shows your break-even point.</p><p class="small">The figures shown are illustrative. Replace them with your own.</p></div>
<div class="rv-r">{GAP_MINI}</div>
</div>
<div class="sec-head" style="margin:70px 0 30px"><h2>Free calculators from Wisconsin Insurance Appraiser</h2><p>Seven tools built from real appraisal work, including a roof snow-load calculator made for Wisconsin winters. Everything runs in your browser; nothing is stored or sent.</p></div>
<div class="tool-grid" data-stagger>{tiles}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Lakeshore to North Woods</span><h2>Wisconsin Insurance Appraiser in your city</h2><p>We work in every county. These are the cities where Wisconsin Insurance Appraiser handles claims most often, each with its own housing stock and storm history.</p></div>
<div class="loc-wrap">
<div class="loc-feature rv-s">{img(ph("city-milwaukee", "lake-storm"), sizes="(max-width:1020px) 100vw, 600px", alt="", extra=' data-parallax="0.08"')}<div class="in"><span class="kicker light">Statewide coverage</span><h3>On-site inspections in all 72 counties</h3><p>Milwaukee bungalows, Madison condos, Fox Valley ranches, Driftless farms and Up North cabins.</p><a class="btn gold" href="{LOC_BASE}">All Wisconsin cities {ic("arrow")}</a></div></div>
<div class="loc-list" data-stagger>{locs}</div>
</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Storm record</span><h2>Storms that shaped Wisconsin claims</h2><p>These well-known events are part of why a Wisconsin Insurance Appraiser reads every estimate with local weather in mind. Swipe for more.</p></div>
<div class="storm-rail" data-stagger>{storm_cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head c rv"><span class="kicker">Who does what</span><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Wisconsin Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="roles" data-stagger>
<div class="role us rv"><h3>Wisconsin Insurance Appraiser</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best time</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Award signed by two of three</dd></dl></div>
<div class="role rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare and negotiate the claim</dd><dt>Best time</dt><dd>Early, from first notice</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></div>
<div class="role rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Legal rights, coverage and bad-faith issues</dd><dt>Best time</dt><dd>Denials, deadlines, disputes over coverage</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec paper"><div class="wrap split top">
<div class="rv-l"><span class="kicker">FAQ</span><h2>Questions for a Wisconsin Insurance Appraiser</h2><p>Plain answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:24px"><a class="btn" href="{FAQ_URL}">All FAQs {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Claims dictionary</a></div></div>
<div class="rv-r">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Learning center</span><h2>Guides from Wisconsin Insurance Appraiser</h2><p>Practical reading on policy language, documentation and Wisconsin weather claims before you demand appraisal.</p></div>
<div class="guide-grid" data-stagger>{guides}</div>
<p style="margin-top:30px"><a class="arrow-link" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="cta-par">{img("storm-front", "bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap rv"><span class="kicker light">Before you sign off</span><h2>Check the numbers before you accept the settlement</h2><p>A short review now can keep you from accepting a payment that won’t cover the repair.</p><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#contact">Send your estimate</a></div></div></section>

<section class="sec navy" id="contact"><div class="wrap split top">
<div class="rv-l"><span class="kicker light">Start with a conversation</span><h2>Talk with Wisconsin Insurance Appraiser about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and tell you straight whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm CT</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Coverage</span><b>All 72 Wisconsin counties</b></div></li></ul></div>
<div class="rv-r">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Wisconsin Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, ice dam, water and fire claims.",
                        body, [faq_schema(home_faqs)], preload="hero"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        photo = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), photo, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Common questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Cities we serve", locs + [("All Wisconsin cities", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Wisconsin"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=photo), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="130px", alt="")}</span><span class="bd"><span class="k">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Wisconsin",
                     "From a single estimate review to full appraisal panel work and neutral umpire service, every Wisconsin Insurance Appraiser service is built around an accurate, defensible valuation of your loss.", ph("roof-tarp", "roof-shingles")) + f"""
<section class="sec"><div class="wrap"><div class="index-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv-l"><span class="kicker">Not sure where to start?</span><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review answers that in days, and some disputes end there.</p><a class="btn" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv-r">{faq_block([("Can I hire you for just one step?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial claims?", "Yes: houses, duplexes, condos, apartment buildings, retail and office space, churches, condo associations and farm buildings."), ("Is it only storm claims?", "No. We also value water, sewer backup, fire, smoke, ice dam and frozen-pipe losses.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Wisconsin | 12 Services",
                             "Wisconsin insurance appraisal services: appraisal demands, estimate review, hail, wind, snow, ice dam, water, fire and farm claims, plus umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload=ph("roof-tarp", "roof-shingles")), 0.9)


# ---------------------------------------------------------------- locations
REGION_ORDER = ["Southeast & Lakeshore", "South Central", "Fox Valley & Northeast", "Western & Driftless", "Central & North Woods"]


def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        photo = LOC_PHOTO[l["slug"]]
        storms = "".join(f"<li><b>{e(d)}</b><span>{e(t)}</span></li>" for d, t in l["storms"])
        facts_box = f"""<div class="local-facts">
<div><span class="lf-t">County</span>{e(l["county"])}</div>
<div><span class="lf-t">Region</span>{e(l["region"])}</div>
<div class="wide"><span class="lf-t">Housing mix</span>{e(l["housing"])}</div>
<div class="wide"><span class="lf-t">Local claim risks</span><ul class="chips navy" style="margin:6px 0 0">{"".join(f"<li>{e(p)}</li>" for p in l["perils"])}</ul></div>
<div class="wide"><span class="lf-t">Storm history</span><ul class="storm-list">{storms}</ul></div>
<div class="wide"><span class="lf-t">Neighborhoods &amp; nearby communities</span>{e(", ".join(l["neighborhoods"]))}</div>
</div>"""
        body = page_hero(trail, l["region"], f"{l['city']} Insurance Appraiser", e(l["lede"]), photo,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
{facts_box}
{l["body"]}
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Wisconsin cities", items, path)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Wisconsin"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, preload=photo), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    blocks = ""
    for reg in REGION_ORDER:
        ls = [l for l in LOCATIONS if l["region"] == reg]
        if not ls:
            continue
        cards = "".join(f'<a class="icard rv" href="{loc_path(l)}"><span class="ph">{img(LOC_PHOTO[l["slug"]], sizes="130px", alt="")}</span><span class="bd"><span class="k">{e(l["county"])}</span><h3>{e(l["city"])}</h3><p>{e(l["lede"][:150].rsplit(" ", 1)[0])}…</p></span></a>' for l in ls)
        blocks += f'<div class="region-block"><h2>{e(reg)}</h2><div class="index-grid" data-stagger>{cards}</div></div>'
    body = page_hero(trail, "Statewide coverage", "Local Insurance Appraisers in All 72 Wisconsin Counties",
                     "Wisconsin Insurance Appraiser works statewide, from the Illinois line to Lake Superior. These city pages cover the places we handle claims most often, grouped by region.", ph("city-madison", "lake-storm")) + f"""
<section class="sec"><div class="wrap">{blocks}</div></section>
{cta_band("Don’t see your town?", "We inspect in every Wisconsin county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Local Insurance Appraisers in Wisconsin | 12 Cities",
                             "Insurance appraisal in all 72 Wisconsin counties, with local pages for Milwaukee, Madison, Green Bay, Kenosha, Racine, Appleton, Eau Claire and more.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload=ph("city-madison", "lake-storm")), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{TOOL_BASE}{o["slug"]}/"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)])
        photo = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), photo, cta=False) + f"""
<section class="sec" style="padding-bottom:0"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and default figures are illustrative.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All calculators", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=photo), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    tiles = "".join(f'<a class="tool-card rv" data-tilt href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="badge"><i>{e(t["icon"])}</i>{e(t["kind"])}</span></span><span class="bd"><h2 style="font-size:1.12rem">{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    T = lambda s: f"{TOOL_BASE}{s}/"
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Wisconsin Owners",
                     "Seven calculators and planners built from real appraisal work, including a roof snow-load calculator for Wisconsin winters. No sign-up, and nothing you type is stored.", "calculator-desk", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-grid" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv-l"><span class="kicker">A sensible order</span><h2>Using the calculators together</h2><ol><li>Start with the <a href="{T("claim-timeline-planner")}">claim timeline planner</a> so no deadline slips.</li><li>Check the roof math with the <a href="{T("roof-pitch-squares-calculator")}">roof pitch &amp; squares calculator</a>.</li><li>See what you’ll actually receive with the <a href="{T("percentage-deductible-calculator")}">percentage deductible</a> and <a href="{T("rcv-acv-holdback-calculator")}">RCV/ACV holdback</a> calculators.</li><li>Size the dispute with the <a href="{T("settlement-gap-calculator")}">settlement gap calculator</a>.</li><li>Finish with the <a href="{T("appraisal-readiness-quiz")}">appraisal readiness quiz</a>.</li></ol></div><div class="rv-r">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Wisconsin Owners",
                              "Free claim calculators: settlement gap, RCV/ACV holdback, roof squares, percentage deductible, timeline planner, readiness quiz and roof snow load.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload="calculator-desk"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process guide", path)]
    steps_html = "".join(f'<h2>Step {i + 1}: {e(n)}</h2>{h}' for i, (n, h) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in Wisconsin, Step by Step",
                     "Eight steps from the first disagreement to a signed award: what happens, who does what, and where Wisconsin claims most often go wrong.", ph("clipboard", "paperwork"),
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{steps_html}{PROCESS_EXTRA}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band()}"""
    import re as _re
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Wisconsin", "description": "Eight steps from a disputed estimate to a signed appraisal award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", " ", h)).strip()[:300], "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, h) in enumerate(PROCESS_STEPS)]}
    body = body.replace("<h2>Step ", "<h2 id=\"step-__\">Step ")
    for i in range(len(PROCESS_STEPS)):
        body = body.replace('id="step-__"', f'id="step-{i + 1}"', 1)
    write(path, document(path, "Wisconsin Insurance Appraisal Process | 8 Steps",
                         "Step-by-step guide to the Wisconsin insurance appraisal process: the written demand, choosing appraisers and an umpire, and the binding award.",
                         body, [crumbs_schema(trail), howto], preload=ph("clipboard", "paperwork")), 0.8)

    path = FAQ_URL
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    groups = "".join(f'<h2>{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    jump = " · ".join(e(g) for g, _ in FAQ)
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for Wisconsin Property Owners",
                     f"Plain answers grouped by topic: {jump}.", "kitchen") + f"""
<div class="wrap layout"><article class="prose">{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Wisconsin Costs, Timing & Rules",
                         "Answers to common Wisconsin insurance appraisal questions: starting the process, fees, timing and deadlines, state rules and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="kitchen"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claims dictionary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Property Insurance Claims Dictionary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the search box to filter.", "paperwork", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the dictionary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “ice dam”"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claims dictionary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claims Dictionary | ACV, RCV, Umpire & More",
                         "Searchable plain-English dictionary of property insurance claim terms: actual cash value, holdback, ice dam, umpire, matching, O&P and more.",
                         body, [crumbs_schema(trail), dts], preload="paperwork"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Learning center", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        photo = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), photo, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "publisher": {"@id": DOMAIN + "/#business"}, "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=photo), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Learning center", path)]
    cards = "".join(f'<article class="guide rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 400px", alt="")}</a><div class="bd"><span class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</span><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="arrow-link" href="{POST_BASE}{p["slug"]}/">Read the guide {ic("arrow")}</a></div></article>' for p in POSTS)
    res = "".join(f'<a class="icard plain rv" href="{u}"><span class="k">Resource</span><h2>{e(n)}</h2></a>' for n, u in LEARN[:3])
    body = page_hero(trail, "Learning center", "Insurance Appraisal Guides for Wisconsin Property Owners",
                     "Practical reading on policy language, documentation and the weather claims Wisconsin produces, from ice dams to derechos.", "lake-storm", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="guide-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head"><h2>More resources</h2></div><div class="index-grid" data-stagger>{res}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Guides | Wisconsin Learning Center",
                         "Guides for Wisconsin property owners on appraisal clauses, ice dams, hail photos, sewer backup coverage, derecho wind claims and matching disputes.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="lake-storm"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About us", path)]
    body = page_hero(trail, "About us", "About Wisconsin Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "consultation") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, done well</h2>
<p>Plenty of claim professionals do a bit of everything. We chose to focus. Wisconsin Insurance Appraiser works on the amount of loss, and our inspections, estimates and calculators are built around answering that question carefully. That focus lets us act as your appointed appraiser, review an insurer’s estimate before a dispute hardens, or serve as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate might look good on day one, but it costs credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll tell you.</li>
<li><strong>Fees in writing.</strong> You know what it costs before any work starts.</li>
</ul>
<h2>Who we help</h2>
<p>Homeowners, condo owners, landlords, condo associations, farm owners, churches, business owners, contractors, public adjusters and attorneys across Wisconsin. On any claim we serve in one role only, and we disclose prior dealings with the other appraiser or the umpire.</p>
<h2>What we don’t do</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes, because no honest appraiser can.</p>
<h2>Why Wisconsin weather matters to a valuation</h2>
<p>A roof in Kenosha, a dairy barn in Marathon County and a cabin near Lake Superior fail in different ways. Ice dams, snow load, spring hail, derecho winds and summer flash floods each leave their own pattern, and each changes what a complete repair scope looks like. Working statewide means we see all of it.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Wisconsin cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process guide", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Us | Wisconsin Insurance Appraiser",
                         "Wisconsin Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="consultation"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", "Contact Wisconsin Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "laptop-review", cta=False) + f"""
<section class="sec navy"><div class="wrap split top">
<div class="rv-l"><span class="kicker light">Direct lines</span><h2>Reach us directly</h2>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm CT</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>All 72 Wisconsin counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv-r">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Wisconsin Insurance Appraiser | (844) 537-1427",
                         "Get a free review of your disputed Wisconsin property claim. Call or text (844) 537-1427, email us, or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="laptop-review"), 0.8)

    lic = {"cc0": "CC0 1.0", "pdm": "Public domain"}
    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" style=\"width:120px;height:72px;object-fit:cover;border-radius:8px\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · via {e(v["source"])}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        "/privacy/": ("Privacy Policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Information we collect</h2><p>When you send a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used to understand how the site is used, not to sell data.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us.", "Privacy policy for Wisconsin Insurance Appraiser: what we collect through forms, calls and email, how it’s used and the choices you have."),
        "/terms/": ("Terms of Use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Wisconsin.</p>
<h2>No client relationship</h2><p>Reading the site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Talk to a licensed Wisconsin attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from the information you enter. Example figures are illustrative. None of it is an appraisal, a quote or a prediction of a claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Wisconsin.</p>""", "The terms that apply when you use this website and its calculators.", "Terms of use for the Wisconsin Insurance Appraiser website: no client relationship, no legal advice, calculator limits and governing law."),
        "/disclaimer/": ("Disclaimer", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is approaching, contact a Wisconsin attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>
<h2>References</h2><p>Mentions of laws, agencies or weather events are for context only. Check current law and facts with official sources such as the Wisconsin Office of the Commissioner of Insurance.</p>""", "Important limits on the information published on this website.", "Disclaimer for Wisconsin Insurance Appraiser: general information only, no legal advice, no guaranteed results and illustrative examples."),
        "/photo-credits/": ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Photos were found through the Openverse catalog. Attribution isn’t legally required, but we credit the photographers here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site.", "Photo credits for Wisconsin Insurance Appraiser: every image is CC0 or public domain, listed with its creator, source and license."),
    }
    for path, (title, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "office-tower", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], preload="office-tower"), 0.3)


def sitemap_pages():
    path = SITEMAP_HTML
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main pages", [("Home", "/"), ("About us", ABOUT), ("Contact us", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy/"), ("Terms of use", "/terms/"), ("Disclaimer", "/disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="icard plain rv"><h2>{e(g)}</h2><ul style="padding-left:1.1em;margin:0">{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "office-tower", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: appraisal services, Wisconsin cities, free claim calculators and guides.", body, [crumbs_schema(trail)], preload="office-tower"), 0.3)

    body = f"""<section class="page-hero">{img("storm-front", "bg", lazy=False, alt="")}<div class="wrap"><span class="kicker light">Error 404</span><h1>This page is snowed under</h1><p class="lede">We couldn’t find the page you asked for. It may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn gold" href="/">Home</a><a class="btn ghost-l" href="{SVC_BASE}">Services</a><a class="btn ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn ghost-l" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow"), sitemap=False)


GUARD_PHP = r"""<?php
// Wisconsin Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$wia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$wia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$wia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($wia_host === 'www.' . $wia_real || ($wia_host === $wia_real && $wia_proto === 'http')) {
    header('Location: https://' . $wia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$wia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($wia_uri, '?'), $wia_m)) {
    $wia_q = strpos($wia_uri, '?') !== false ? substr($wia_uri, strpos($wia_uri, '?')) : '';
    header('Location: ' . $wia_m[1] . $wia_q, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($wia_host !== $wia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
""".replace("__HOST__", HOST)

INDEX_PHP = r"""<?php
// Wisconsin Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (a directory's index.php included)
// and routes "/" and unknown paths here.
require_once __DIR__ . '/_guard.php';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
if ($path === '/') {
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
