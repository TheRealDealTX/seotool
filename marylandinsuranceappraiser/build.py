#!/usr/bin/env python3
"""Static site generator for marylandinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only.
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
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402
from media import PHOTO_ALT, SVC_PHOTO, LOC_PHOTO, TOOL_PHOTO, POST_PHOTO, PAGE_PHOTO, REGIONS  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Maryland Insurance Appraiser"
HOST = "marylandinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112a"
FAV = "1"
# Google Tag Manager container, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

SVC_BASE = "/property-claim-services/"
LOC_BASE = "/service-locations/"
TOOL_BASE = "/appraisal-calculators/"
POST_BASE = "/knowledge-base/"
P_PROCESS = "/the-appraisal-process/"
P_FAQ = "/common-questions/"
P_GLOSS = "/appraisal-glossary/"
P_ABOUT = "/about-the-firm/"
P_CONTACT = "/start-a-claim-review/"
P_PRIV = "/privacy-practices/"
P_TERMS = "/site-terms/"
P_DISC = "/important-disclaimer/"
P_CRED = "/photo-credits/"
P_MAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap


def svc_path(s):
    return f'{SVC_BASE}{s["slug"]}/'


def loc_path(l):
    return f'{LOC_BASE}{l["slug"]}/'


def tool_path(t):
    return f'{TOOL_BASE}{t["slug"]}/'


def post_path(p):
    return f'{POST_BASE}{p["slug"]}/'


LOC_BY = {l["slug"]: l for l in LOCATIONS}


# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else PHOTO_ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "gap": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "acv": '<path d="M3 3v18h18"/><path d="M7 7l5 5 3-3 5 6"/>',
    "roof": '<path d="M2 13L12 4l10 9"/><path d="M5 11v9h14v-9"/>',
    "pct": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h2M14 14h2M8 18h2"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


SVC_ICON = dict(zip([s["slug"] for s in SERVICES],
                    ["doc", "home", "building", "hail", "wind", "storm", "drop", "flame", "snow", "tree", "file", "scale"]))


def mark():
    return ('<svg class="mark" viewBox="0 0 48 48" width="44" height="44" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#2E2910"/>'
            '<path d="M10.5 24.5L24 12.5l13.5 12" fill="none" stroke="#d9c27a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M16 23.5v8.5h16v-8.5" fill="none" stroke="#f5f2e6" stroke-width="3.2" stroke-linejoin="round"/>'
            '<path d="M9.5 38.5c3.2-2.4 6-2.4 9.2 0s6 2.4 9.2 0 6-2.4 9.2 0" fill="none" stroke="#8cbad6" stroke-width="3" stroke-linecap="round"/></svg>')


def brand(where):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Maryland</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "MD", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MD", "availableLanguage": "en"}],
        "slogan": "Independent valuation for disputed property claims",
        "description": "Independent insurance appraisal, carrier estimate review and neutral umpire services for disputed property claims in every Maryland county and Baltimore City.",
        "areaServed": [{"@type": "State", "name": "Maryland"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Umpire", "Property claim valuation", "Hurricane deductibles", "Ice dam claims", "Rowhouse roofing"],
        "priceRange": "$$",
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
LEARN = [("The appraisal process", P_PROCESS), ("Common questions", P_FAQ), ("Appraisal glossary", P_GLOSS), ("Knowledge base", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All 12 services", SVC_BASE)),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Maryland locations", LOC_BASE)),
        ("Calculators", [(t["name"], tool_path(t)) for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        foot = f'<a class="dd-all" href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a>' if allk else ""
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-dd"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><div class="dd{wide}" id="dd-{i}"><ul>{li}</ul>{foot}</div></li>'
    menu += f'<li><a href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="solo" href="{P_ABOUT}">About the firm</a></li><li><a class="solo" href="{P_CONTACT}">Start a claim review</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand("h")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-r"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn sm head-cta" href="{P_CONTACT}">Free review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>
<div class="drawer-bg" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("d")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="solo" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="mailto:{EMAIL}">{ic("mail")} Email us</a><small>Mon–Fri 8am–6pm ET · all 24 Maryland jurisdictions</small></div>
</aside>"""


def footer():
    col = lambda items: "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in items)
    return f"""<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("f")}
<p>Independent appraisal and estimating for property owners whose insurance claim was accepted but underpaid — from Garrett County’s snow country to the Atlantic beaches of Worcester County.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri, 8am–6pm ET</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{col([(s["name"], svc_path(s)) for s in SERVICES[:7]])}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Locations</h2><ul>{col([(l["city"], loc_path(l)) for l in LOCATIONS[:8]])}<li><a href="{LOC_BASE}">All locations</a></li></ul></div>
<div><h2 class="foot-h">Calculators</h2><ul>{col([(t["name"], tool_path(t)) for t in TOOLS])}</ul></div>
<div><h2 class="foot-h">Firm &amp; resources</h2><ul>{col([("About the firm", P_ABOUT), ("Start a claim review", P_CONTACT)] + LEARN)}</ul></div>
</div>
<div class="wrap foot-legal">
<p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we do not give legal advice and we do not act as a public adjuster. Content on this site is general information; policy wording controls. Outcomes depend on the facts of each claim and are never guaranteed.</p>
<div class="foot-bar"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul>{col([("Privacy", P_PRIV), ("Terms", P_TERMS), ("Disclaimer", P_DISC), ("Photo credits", P_CRED), ("All pages", P_MAP)])}</ul></div>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<nav class="callbar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("doc")} Free review</a></nav>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n'


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, main_ok=True):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
        extra.append(n)
    key = photo or "hero-home"
    pimg = PHOTOS[key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for n in extra if n.get("@type") in MAIN_TYPES]
    faq = [n["@id"] for n in extra if n.get("@type") == "FAQPage"]
    if mains:
        webpage["mainEntity"] = {"@id": mains[0]}
    elif faq:
        webpage["mainEntity"] = {"@id": faq[0]}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{key}.webp" imagesrcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal in Maryland">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal in Maryland">
<meta name="geo.region" content="US-MD">
<meta name="geo.placename" content="Maryland">
<meta name="theme-color" content="#2E2910">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Young+Serif&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.className+=' js';</script>
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
    # Pages are dir/index.php: the host serves real files without running the root front controller,
    # so every page begins with the canonical-host guard. Never write dir/index.html.
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
        assert "<?" not in content, path
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
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
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(parts) + "</ol></nav>"


def page_hero(trail, kicker, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="ph-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btns"><a class="btn brass" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{P_CONTACT}">Request a free review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.18"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(kicker)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-h">Talk to an appraiser</h2><p>A free first conversation about your estimate — and a straight answer on whether appraisal fits.</p><a class="box-tel" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn brass block" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri, 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-h">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="side"><div class="side-in">{aside}</div></aside></div>'


def cta_strip(h="An estimate that doesn’t add up?", p="Send the insurer’s estimate and your photos. We’ll review it and tell you what we see — no obligation."):
    return f"""<section class="strip"><div class="wrap strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btns"><a class="btn brass" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(items, label):
    return '<div class="rel">' + "".join(f'<a href="{p}"><small>{e(label)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Wind / tornado / derecho", "Hurricane / nor’easter", "Water / pipe leak", "Snow, ice dam or freeze", "Fire / smoke", "Fallen tree", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hid="f"):
    roles = ["Homeowner", "Condo / townhome owner", "Landlord", "Business owner", "HOA / property manager", "Contractor", "Attorney or public adjuster", "Other"]
    places = [l["city"] for l in LOCATIONS] + ["Elsewhere in Maryland"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-h">{e(heading)}</h2><p class="form-sub">Free review · no obligation · usually a reply within one business day</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(places)}</select></div>
<div><label for="{hid}-amt">Rough amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure yet</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">Where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the insurer paid or offered, and what you think is missing."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about this claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy practices</a>.</span></label></div>
<div class="full"><button class="btn block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="hf-k">Free claim review</p><h2 class="hf-h">Is your settlement short?</h2>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>Contact me about this claim. <a href="{P_PRIV}">Privacy</a></span></label>
<button class="btn brass block" type="submit">Request a call back {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hf-note">{ic("shield")} No obligation. Details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
def home():
    K = BRAND
    rail = "".join(
        f'<a class="rcard" href="{svc_path(s)}"><span class="rc-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 80vw, 320px", alt="")}</span>'
        f'<span class="rc-n">{i + 1:02d}</span><span class="rc-b"><span class="rc-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
        for i, s in enumerate(SERVICES))
    regions = "".join(
        f'<li class="reg" tabindex="0">{img(ph, sizes="(max-width:900px) 100vw, 40vw", alt="")}<div class="reg-b"><p class="reg-k">{e(sub)}</p><h3>{e(name)}</h3><p class="reg-t">{e(txt)}</p><p class="reg-c">{e(cities)}</p></div></li>'
        for name, sub, txt, cities, ph in REGIONS)
    steps = [
        ("Review", "We read the policy, the insurer’s estimate and your photos, then say plainly whether appraisal fits."),
        ("Inspect", "An independent inspection and measured, line-item estimate priced for your Maryland ZIP code."),
        ("Demand", "Appraisal is invoked in writing and your appraiser is named inside the policy’s time limit."),
        ("Negotiate", "Your appraiser works item by item with the insurer’s appraiser. Most gaps narrow here."),
        ("Award", "Anything unresolved goes to a neutral umpire. Two signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="hs"><span class="hs-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    tool_rows = "".join(f'<li><a href="{tool_path(t)}"><span class="tr-ic">{ic(t["icon"] if t["icon"] in _I else "file")}</span><span><b>{e(t["name"])}</b><small>{e(t["short"])}</small></span>{ic("arrow")}</a></li>' for t in TOOLS)
    locs = "".join(f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="lc-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    posts = "".join(f'<article class="gcard rv"><a class="gc-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gc-b"><p class="gc-m">{p["read"]} read</p><h3><a href="{post_path(p)}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work through the differences with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is appraisal the same as filing a complaint with the Maryland Insurance Administration?", "No. An MIA complaint asks the regulator to look at how the insurer handled your claim. Appraisal is a process in your policy that sets the amount of loss. They are separate tracks, and an attorney can tell you how they interact in your situation."),
        (f"When should I call a {K}?", "When coverage has been accepted, you have the insurer’s estimate, and the gap between it and a qualified contractor’s estimate is meaningful — often more than 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That’s why the documentation behind your number matters so much before anyone invokes appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire’s fee. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you work outside Baltimore and the suburbs?", "Yes. We take claims in all 23 counties and Baltimore City — Western Maryland, the Capital Region, Southern Maryland and the Eastern Shore included."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.25"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent property claim appraisal · Statewide</p>
<h1>Maryland Insurance Appraiser <em>for claims that were accepted — and underpaid</em></h1>
<p class="lede">When the insurer agrees the damage is covered but the check won’t pay for the repair, Maryland Insurance Appraiser builds an independent, measured valuation and carries it through the appraisal clause in your policy.</p>
<div class="btns"><a class="btn brass" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#how">How appraisal works {ic("arrow")}</a></div>
</div>
{hero_form()}
</div>
</section>

<section class="ribbon" aria-label="At a glance"><div class="wrap ribbon-in">
<div><b data-count="24">24</b><span>Maryland jurisdictions — 23 counties &amp; Baltimore City</span></div>
<div><b data-count="12">12</b><span>Appraisal, review &amp; umpire services</span></div>
<div><b data-count="7">7</b><span>Free claim calculators</span></div>
<div><b>2 of 3</b><span>Signatures that make an award binding</span></div>
</div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-ph rv">{img("consultation", sizes="(max-width:900px) 100vw, 45vw")}<p class="intro-tag">{ic("shield")} Retained by you — never by the insurer</p></div>
<div class="rv">
<p class="kicker dark">Why owners call</p>
<h2>A Maryland Insurance Appraiser closes the gap between “covered” and “paid in full”</h2>
<p>Most short claims aren’t denials. A rowhouse roof priced as a patch, plaster walls estimated as drywall, a matching problem nobody mentioned, a code upgrade Baltimore County will require anyway. A Maryland Insurance Appraiser exists for those differences.</p>
<ol class="numlist">
<li><b>We value the loss from scratch.</b> Our own inspection and measurements — never an edited copy of the insurer’s estimate.</li>
<li><b>We price what we can defend.</b> Numbers built to persuade an umpire, because inflated numbers don’t move awards.</li>
<li><b>We tell you when appraisal is the wrong tool.</b> Denials, coverage fights and bad-faith questions belong with a Maryland attorney.</li>
</ol>
<a class="btn" href="{P_ABOUT}">About the firm {ic("arrow")}</a>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Services</p><h2>Twelve ways Maryland Insurance Appraiser works on a disputed claim</h2></div><p>Start with a review of the insurer’s estimate, bring us in after appraisal has been demanded, or appoint us as a neutral umpire. Swipe or use the arrows to browse.</p></div>
<div class="rail-wrap"><div class="rail" tabindex="0" aria-label="Services">{rail}</div>
<div class="rail-nav"><button type="button" class="rail-btn" data-rail="-1" aria-label="Previous services">{ic("left")}</button><button type="button" class="rail-btn" data-rail="1" aria-label="Next services">{ic("right")}</button><a class="link" href="{SVC_BASE}">Compare all services</a></div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Fit check</p><h2>When Maryland Insurance Appraiser is — and isn’t — the right call</h2></div><p>Appraisal answers one question: how much the covered damage costs. It is powerful for that question and useless for others.</p></div>
<div class="fit">
<div class="fit-y rv"><h3>{ic("check")} Appraisal fits</h3><ul><li>Coverage accepted, price disputed</li><li>Repair-versus-replace disagreements on roofs and floors</li><li>Matching and discontinued materials</li><li>Missing trades, code items, overhead &amp; profit</li><li>Contents or ALE totals that don’t match receipts</li></ul></div>
<div class="fit-n rv"><h3>{ic("x")} Look elsewhere</h3><ul><li>A full denial or a coverage exclusion fight</li><li>Bad-faith or unfair-practice questions (MIA or attorney)</li><li>A gap too small to justify fees</li><li>A suit deadline that is close — call an attorney first</li><li>Flood losses under a separate flood policy with its own process</li></ul></div>
</div>
</div></section>

<section class="sec olive" id="how"><div class="wrap">
<div class="sec-head light rv"><div><p class="kicker">The process</p><h2>How Maryland Insurance Appraiser moves a stuck claim</h2></div><p>The appraisal clause turns an open-ended argument into a short, defined procedure with a binding result.</p></div>
<div class="hsteps" data-steps><span class="hs-line"><span class="hs-fill"></span></span><ol>{proc}</ol></div>
<p class="center"><a class="link light" href="{P_PROCESS}">Read the full appraisal process guide</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Five claim climates</p><h2>Maryland Insurance Appraiser knows how each region’s weather shows up</h2></div><p>Lake-effect snow near Deep Creek, hail in the Frederick Valley, rowhouse fires in Baltimore, hurricane deductibles on the Bay, salt and surge in Ocean City. Hover or tap a region.</p></div>
<ul class="regions" data-stagger>{regions}</ul>
<p class="center"><a class="link" href="{LOC_BASE}">See every service location</a></p>
</div></section>

<section class="sec tint"><div class="wrap tools-split">
<div class="rv"><p class="kicker dark">Free &amp; private</p><h2>Seven calculators from Maryland Insurance Appraiser</h2><p>Check the insurer’s math before you call anyone. Every tool runs in your browser — nothing is stored or sent.</p>
<ul class="tool-rows">{tool_rows}</ul></div>
<div class="rv"><div class="blue-panel"><h3>Try the two-number gap check</h3><p>Enter the insurer’s estimate and your contractor’s. If the gap is wide, a Maryland Insurance Appraiser conversation makes sense; if it’s narrow, a documented supplement may close it faster.</p>{GAP_MINI}<p class="small">Want fees included? Open the full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</p></div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Where we work</p><h2>Maryland Insurance Appraiser service locations</h2></div><p>We take claims in every county and Baltimore City. These twelve communities have their own pages with local housing and storm history.</p></div>
<div class="lgrid" data-stagger>{locs}</div>
</div></section>

<section class="sec white"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Choosing help</p><h2>Maryland Insurance Appraiser, public adjuster or attorney?</h2></div><p>Each solves a different problem. Picking the right one first saves time and fees.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Maryland Insurance Appraiser</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Prepare &amp; negotiate the claim</td><td>Legal rights, disputes, litigation</td></tr>
<tr><th scope="row">Best moment</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Award signed by 2 of 3</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it</td></tr>
</tbody></table></div>
</div></section>

<section class="sec tint"><div class="wrap faq-split">
<div class="rv"><p class="kicker dark">Questions</p><h2>Asked of every Maryland Insurance Appraiser</h2><p>Straight answers on process, cost and when appraisal is the wrong move.</p><div class="btns"><a class="btn" href="{P_FAQ}">All common questions</a><a class="btn line" href="{P_GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="kicker dark">Knowledge base</p><h2>Read before you sign an appraisal demand</h2></div><p>Practical, Maryland-specific guides from the Maryland Insurance Appraiser knowledge base.</p></div>
<div class="ggrid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">Browse the knowledge base</a></p>
</div></section>

<section class="pcta"><div class="pcta-bg">{img("storm-clouds", alt="", extra=' data-parallax="0.3"')}</div><div class="wrap pcta-in rv"><p class="kicker">Before you sign the release</p><h2>Check the numbers while you still can change them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btns"><a class="btn brass" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#contact">Send your estimate</a></div></div></section>

<section class="sec olive-d" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start a conversation</p><h2>Talk with Maryland Insurance Appraiser about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you an honest read on whether appraisal is worth pursuing.</p>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><span>Mon–Fri, 8am–6pm ET</span></div></li><li>{ic("pin")}<div><small>Coverage</small><span>All 23 counties &amp; Baltimore City</span></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Maryland Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid storm, water, snow and fire claims.",
                        body, [faq_schema(home_faqs)], photo="hero-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(
            f"""{s["body"]}<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}<h2>Related services</h2>{related([(r["name"], svc_path(r)) for r in rel], "Service")}""",
            call_box() + list_box("All services", items, path) + list_box("Service locations", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All locations", LOC_BASE)])) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["keyword"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Maryland"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{svc_path(s)}"><span class="ic-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="ic-n">{i + 1:02d}</span></span><span class="ic-b"><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">View service {ic("arrow")}</span></span></a>' for i, s in enumerate(SERVICES))
    ph = PAGE_PHOTO["services"]
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in Maryland",
                     "Twelve services built around one job: an accurate, defensible valuation of your loss — whether we act as your appraiser, review the insurer’s estimate or sit as a neutral umpire.", ph) + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker dark">Where to start</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that difference is worth. A review answers that quickly, and many disputes are settled with a documented supplement at that stage.</p><a class="btn" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one step only?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle commercial and HOA properties?", "Yes — condominium and townhome associations, apartment buildings, retail, office, churches and light industrial properties, as well as single-family homes."), ("Do you work on flood claims?", "Flood policies, usually through the National Flood Insurance Program, have their own procedures. We focus on homeowners and commercial property policies, including wind-driven rain and storm damage that isn’t flood.")])}</div></div></section>{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Maryland | 12 Services",
                             "Maryland insurance appraisal services: appraisal demand representation, estimate review, storm, water, winter, fire and tree claims, and umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo=ph), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        storms = "".join(f"<li>{e(s)}</li>" for s in l["storms"])
        hoods = ", ".join(l["neighborhoods"])
        local = f"""<div class="localcard"><div><h2 class="lc-h">Local claim risks</h2><ul class="chips">{chips}</ul></div><div><h2 class="lc-h">Storms on record</h2><ul class="dots">{storms}</ul></div><div class="full"><h2 class="lc-h">Housing mix</h2><p>{e(l["housing"])}</p><p class="hoods"><b>Neighborhoods &amp; nearby:</b> {e(hoods)}</p></div></div>"""
        svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        article = f"""{local}{l["body"]}<h2>Services for {e(l["city"])} property owners</h2><p>Every service is available in {e(l["city"])} and the rest of {e(l["county"].split(" (")[0])}, including:</p><ul class="cols2">{svc}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}<h2>Nearby service areas</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby")}"""
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', l["h1"], l["lede"], ph,
                         [("County", l["county"].split(" (")[0]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(
            article, call_box() + list_box("Maryland locations", items, path) + list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:4]])) + cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, MD", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"},
                                                               "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"].split(" (")[0], "containedInPlace": {"@type": "State", "name": "Maryland"}}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{loc_path(l)}"><span class="ic-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="ic-n sm">{e(l["region"])}</span></span><span class="ic-b"><h2>{e(l["city"])}</h2><p>{e(l["county"])} · {e(", ".join(l["perils"][:3]))}</p><span class="more">Local page {ic("arrow")}</span></span></a>' for l in LOCATIONS)
    regs = "".join(f'<div class="regrow rv">{img(ph, sizes="(max-width:700px) 100vw, 280px", alt="")}<div><p class="kicker dark">{e(sub)}</p><h2>{e(name)}</h2><p>{e(txt)}</p><p class="small">{e(cities)}</p></div></div>' for name, sub, txt, cities, ph in REGIONS)
    ph = PAGE_PHOTO["locations"]
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 24 Maryland Jurisdictions",
                     "Maryland Insurance Appraiser works in all 23 counties and Baltimore City — from Oakland to Ocean City. These pages cover the communities where claims come from most often.", ph) + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><div><p class="kicker dark">Regions</p><h2>How claims differ across Maryland</h2></div><p>The same policy language plays out very differently in a Garrett County cabin, a Fells Point rowhouse and an Ocean City condo tower.</p></div><div class="regrows">{regs}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Maryland county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Maryland Insurance Appraiser Locations | Statewide",
                             "Insurance appraisal in all 23 Maryland counties and Baltimore City, including Annapolis, Frederick, Rockville, Hagerstown, Salisbury and Ocean City.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f"{n}, MD", p) for n, p in items])], photo=ph), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = tool_path(t)
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · nothing stored", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>""" + layout(
            f'{t["explain"]}<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free calculators</h2>{related([(o["name"], tool_path(o)) for o in others], o["kind"] if False else "Calculator")}',
            call_box() + list_box("All calculators", items, path)) + cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(f'<a class="icard rv" href="{tool_path(t)}"><span class="ic-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="ic-n sm">{e(t["kind"])}</span></span><span class="ic-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open {t["kind"].lower()} {ic("arrow")}</span></span></a>' for t in TOOLS)
    ph = PAGE_PHOTO["tools"]
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Maryland",
                     "Seven calculators and planners built from real appraisal work. Check the insurer’s math, map your deadlines and decide on next steps — no sign-up and nothing stored.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker dark">Suggested order</p><h2>Using the calculators together</h2><ol class="numlist"><li>Start with the <a href="{TOOL_BASE}claim-timeline-planner/">claim timeline planner</a> so nothing lapses.</li><li>Check roof math with the <a href="{TOOL_BASE}roof-square-pitch-calculator/">roof square &amp; pitch calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}hurricane-deductible-calculator/">hurricane deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-worksheet/">RCV / ACV</a> tools.</li><li>Size the dispute with the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-checklist/">readiness checklist</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Maryland",
                              "Seven free property claim calculators: appraisal cost, RCV vs ACV, roof squares, hurricane deductible, claim deadlines, readiness and snow load.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo=ph), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("The appraisal process", path)]
    ph = PAGE_PHOTO["process"]
    steps = "".join(f'<li><span class="vs-n">{i + 1}</span><div><h3>{e(s["name"])}</h3><p>{e(s["text"])}</p></div></li>' for i, s in enumerate(PROCESS_STEPS))
    article = f'<h2>The process at a glance</h2><ol class="vsteps">{steps}</ol>{PROCESS_BODY}'
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in Maryland, Step by Step",
                     "From the first disagreement to a signed award — what happens, who does what, and where Maryland claims most often go wrong.", ph,
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(
        article, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Maryland", "description": "The steps of a property insurance appraisal under a Maryland policy's appraisal clause.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": s["name"], "text": s["text"]} for i, s in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in Maryland: Step by Step",
                         "Step-by-step guide to the Maryland insurance appraisal process: the written demand, choosing appraisers and an umpire, negotiation and the award.",
                         body, [crumbs_schema(trail), howto], photo=ph), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Common questions", path)]
    ph = PAGE_PHOTO["faq"]
    jump = "".join(f'<a href="#t{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="t{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, f"{len(allq)} answers in {len(FAQ)} topics", "Insurance Appraisal Questions from Maryland Owners",
                     "Plain answers about the appraisal process, costs, Maryland deadlines, the MIA and storm, water and winter claims.", ph) + layout(
        f'<nav class="jump" aria-label="FAQ topics">{jump}</nav>{groups}', call_box() + list_box("Resources", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")
    write(path, document(path, "Insurance Appraisal Questions | Maryland FAQ by Topic",
                         "Answers to common Maryland insurance appraisal questions, grouped by topic: basics, fees, deadlines, the MIA and storm, water and winter claims.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo=ph), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Appraisal glossary", path)]
    ph = PAGE_PHOTO["glossary"]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Searchable reference", "Insurance Appraisal Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards — with Maryland-specific entries — defined in plain English.", ph, cta=False) + layout(
        f'<div class="gfilter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “umpire”, “MIA” or “ice dam”"><p class="hint" id="gloss-count" aria-live="polite"></p></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="glossary">{dl}</dl>',
        call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary: 40 Claim Terms Defined",
                         "Searchable glossary of insurance appraisal and claim terms: ACV, RCV, umpire, appraisal award, O&P, ice dam, MJIA, hurricane deductible and more.",
                         body, [crumbs_schema(trail), dts], photo=ph), 0.7)

    for i, p in enumerate(POSTS):
        path = post_path(p)
        trail = [("Home", "/"), ("Knowledge base", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + layout(
            f'{p["body"]}<h2>Keep reading</h2>{related([(o["title"], post_path(o)) for o in others], "Guide")}',
            call_box() + list_box("Resources", LEARN) + list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:3]])) + cta_strip()
        art = {"@type": "BlogPosting", "headline": p["title"][:110], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US", "keywords": p["keyword"], "image": {"@id": DOMAIN + path + "#primaryimage"}}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Knowledge base", path)]
    ph = PAGE_PHOTO["kb"]
    cards = "".join(f'<article class="gcard rv"><a class="gc-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gc-b"><p class="gc-m">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{post_path(p)}">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides", "Maryland Insurance Appraisal Knowledge Base",
                     "Practical guides on the appraisal clause, MIA complaints, rowhouse roofs, Bay hurricane deductibles, ice dams and choosing an appraiser.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Maryland Insurance Appraisal Guides | Knowledge Base",
                         "Guides for Maryland property owners: the appraisal clause, MIA complaints, rowhouse roof claims, Bay hurricane deductibles and ice dam claims.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], post_path(p)) for p in POSTS])], photo=ph), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About the firm", path)]
    ph = PAGE_PHOTO["about"]
    article = f"""
<figure class="fig">{img("roof-tarp", sizes="(max-width:900px) 100vw, 760px")}</figure>
<h2>An appraisal practice, not a claims mill</h2>
<p>Maryland Insurance Appraiser works on one question: the amount of loss on a property insurance claim. We act as a policyholder’s appointed appraiser, review insurer estimates before a dispute hardens, and serve as a neutral umpire when two appraisers ask us to. Keeping to that lane is deliberate — it keeps our work focused and our role clear.</p>
<h2>How we approach a file</h2>
<ul>
<li><strong>Scope before price.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Support over spin.</strong> An inflated estimate impresses no umpire. We price what we can back with photos, measurements and local costs.</li>
<li><strong>Plain-English reporting.</strong> You’ll see every difference between our valuation and the insurer’s, and why.</li>
<li><strong>Honest triage.</strong> If the dispute is about coverage or conduct, we’ll suggest an attorney or the Maryland Insurance Administration instead.</li>
<li><strong>Fees in writing.</strong> You’ll know what our work costs before it starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners and condo owners, landlords, small businesses, HOA and condominium boards, property managers, houses of worship, contractors, public adjusters and attorneys. On each claim we serve in one role only, and we disclose prior dealings with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and do not give legal advice. We are not public adjusters and do not negotiate claims outside the appraisal process. We do not promise results — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Maryland packs mountains, Piedmont, tidewater and ocean beach into one small state. A single season can bring an ice-dam leak in Garrett County, hail in Frederick, a derecho through Montgomery County and storm surge on the Lower Shore. Working all 24 jurisdictions means we price each of those losses with local knowledge.</p>"""
    body = page_hero(trail, "About", "About Maryland Insurance Appraiser",
                     "Estimators and appraisers who believe a covered claim should be paid on what the repair actually costs — documented clearly enough that everyone at the table can see it.", ph) + layout(
        article, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Locations", LOC_BASE), ("Calculators", TOOL_BASE), ("The appraisal process", P_PROCESS)])) + cta_strip()
    write(path, document(path, "About the Firm | Maryland Insurance Appraiser",
                         "Maryland Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo=ph), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Start a claim review", path)]
    ph = PAGE_PHOTO["contact"]
    body = page_hero(trail, "Contact", "Start a Free Claim Review",
                     "Call, text, email or send your claim details. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", ph, cta=False) + f"""
<section class="sec olive-d"><div class="wrap contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach Maryland Insurance Appraiser</h2>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><span>Mon–Fri, 8am–6pm ET</span></div></li><li>{ic("pin")}<div><small>Service area</small><span>All 23 counties &amp; Baltimore City</span></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters and emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about the claim", page=path, hid="c")}</div></div></section>"""
    write(path, document(path, "Start a Free Claim Review | (844) 537-1427",
                         "Get a free review of a disputed Maryland property claim. Call or text (844) 537-1427 or email info@marylandinsuranceappraiser.com.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo=ph), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · {e(v.get("source_name", ""))}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in sorted(PHOTOS.items()))
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Practices", "Privacy Practices | Maryland Insurance Appraiser", "How Maryland Insurance Appraiser collects, uses and protects the information you share through this website, by phone or by email.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Information you give us</h2><p>When you send a form, call or email, we receive what you choose to share — such as your name, phone number, email address, property location and claim details. Our server also logs standard technical data (IP address, browser, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. What you type isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used to understand overall site use.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""),
        P_TERMS: ("Site Terms", "Site Terms of Use | Maryland Insurance Appraiser", "The terms that apply when you use the Maryland Insurance Appraiser website, its free calculators and its contact forms.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is general information about insurance appraisal and property claims in Maryland.</p>
<h2>No client relationship</h2><p>Reading the site, using its tools or sending a form doesn’t create an appraiser–client relationship. That begins only with a signed written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a Maryland attorney for legal questions.</p>
<h2>Calculators</h2><p>Tools give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. Photographs are used under the licenses listed on our <a href="{P_CRED}">photo credits</a> page.</p>
<h2>Liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Maryland.</p>"""),
        P_DISC: ("Disclaimer", "Disclaimer | Maryland Insurance Appraiser", "Important limits on the information published on this site: general education only, not legal advice, illustrative examples, no guaranteed results.", f"""
<h2>General information</h2><p>This website explains how insurance appraisal commonly works. Your policy’s wording and endorsements control. Always read your own policy.</p>
<h2>Not legal advice; not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys and don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Illustrative examples only</h2><p>Dollar figures on this site are illustrative. They are not results for any client, and no appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here changes any deadline. If one is approaching, talk to a Maryland attorney promptly.</p>
<h2>Laws, agencies and storms</h2><p>References to statutes, the Maryland Insurance Administration, the Maryland Joint Insurance Association or past storms are for context. Check current law and facts with official sources.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>"""),
        P_CRED: ("Photo Credits", "Photo Credits & Licenses | Maryland Insurance Appraiser", "Sources and licenses for every photograph on this site: CC0 and public-domain images from StockSnap, rawpixel, Flickr and U.S. government agencies.", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit the photographers here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (h1, title, desc, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        ph = PAGE_PHOTO["legal"]
        body = page_hero(trail, "Site information", h1, e(desc), ph, cta=False) + layout(content, call_box())
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo=ph), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("All pages", path)]
    groups = [
        ("Main", [("Home", "/"), ("About the firm", P_ABOUT), ("Start a claim review", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(f'{l["city"]}, MD', loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], post_path(p)) for p in POSTS]),
        ("Site information", [("Privacy practices", P_PRIV), ("Site terms", P_TERMS), ("Disclaimer", P_DISC), ("Photo credits", P_CRED)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    ph = PAGE_PHOTO["legal"]
    body = page_hero(trail, "Navigation", "All Pages", f"Every page on {BRAND}, grouped by section.", ph, cta=False) + f'<section class="sec"><div class="wrap mapgrid" data-stagger>{cols}</div></section>'
    write(path, document(path, "All Pages: HTML Site Map | Maryland Insurance Appraiser", "A complete list of pages on Maryland Insurance Appraiser: services, Maryland locations, free claim calculators, guides and site information.", body, [crumbs_schema(trail), {"@type": "CollectionPage"}], photo=ph), 0.3)

    body = f"""<section class="phero nf"><div class="phero-bg">{img(PAGE_PHOTO["404"], lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>That page washed out</h1><p class="lede">The page you wanted may have moved or never existed. These will get you back on track.</p><div class="btns"><a class="btn brass" href="/">Home</a><a class="btn ghost-l" href="{SVC_BASE}">Services</a><a class="btn ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn ghost-l" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on Maryland Insurance Appraiser. Try the home page, services or free calculators.", body, robots="noindex,follow", photo=PAGE_PHOTO["404"]), sitemap=False)


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


GUARD_PHP = r"""<?php
// Maryland Insurance Appraiser - canonical-host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'marylandinsuranceappraiser.com';
$mia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://marylandinsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . $mia_uri, true, 301);
    exit;
}
// /dir/index.php and /index.php are duplicate URLs: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($mia_uri, '?'), $mia_m)) {
    $mia_q = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
    header('Location: ' . $mia_m[1] . $mia_q, true, 301);
    exit;
}
// Keep preview and other hosts out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Maryland Insurance Appraiser - front controller for the static build.
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
