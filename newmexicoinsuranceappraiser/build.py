#!/usr/bin/env python3
"""Static site generator for newmexicoinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Homepage -> home.html, every other page -> dir/index.php
(first line requires _guard.php, rest is static HTML).
"""
import html
import json
import re
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

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))

BRAND = "New Mexico Insurance Appraiser"
HOST = "newmexicoinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
HOURS = "Mon–Fri, 8am–6pm MT"
TODAY = date.today().isoformat()
VER = "20261114a"
FAV = "1"

# Google Tag Manager: leave empty for none. When set (e.g. "GTM-XXXXXXX"), the head snippet and
# the <noscript> iframe after <body> are emitted on every page.
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraiser-services/"
LOC_BASE = "/cities-we-serve/"
TOOL_BASE = "/claim-estimators/"
POST_BASE = "/reading-room/"
PROCESS = "/inside-the-appraisal-process/"
FAQ_P = "/frequently-asked/"
GLOSS = "/claim-terms-a-to-z/"
ABOUT = "/about-the-company/"
CONTACT = "/contact-new-mexico-appraiser/"
PRIVACY = "/privacy-and-cookies/"
TERMS = "/terms-of-website-use/"
DISCLAIM = "/important-notices/"
HTMLMAP = "/all-site-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, '
            f'/assets/img/photos/{key}.webp {p["fw"]}w" sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" '
            f'alt="{a}"{load} decoding="async"{extra}>')


def ph(*keys):
    """First key that exists in the photo manifest (lets the build survive a missing download)."""
    for k in keys:
        if k in PHOTOS:
            return k
    return next(iter(PHOTOS))


HERO = ph("hero-adobe-home")
SVC_PHOTO = {
    "appraisal-demand-representation": ph("consultation"), "home-insurance-appraisal": ph("stucco-home"),
    "commercial-hoa-appraisal": ph("commercial-center"), "hail-roof-appraisal": ph("hail-stones"),
    "high-wind-damage-appraisal": ph("dust-storm"), "water-damage-appraisal": ph("water-ceiling"),
    "fire-smoke-damage-appraisal": ph("house-fire"), "wildfire-loss-appraisal": ph("wildfire-smoke"),
    "flat-roof-stucco-appraisal": ph("flat-roof"), "winter-freeze-damage-appraisal": ph("metal-roof"),
    "claim-estimate-review": ph("calculator"), "umpire-services": ph("clipboard"),
}
LOC_PHOTO = {
    "albuquerque": ph("abq-skyline"), "las-cruces": ph("organ-mountains"), "rio-rancho": ph("rio-grande"),
    "santa-fe": ph("santa-fe-adobe"), "roswell": ph("storm-plains"), "farmington": ph("farmington"),
    "hobbs": ph("oilfield"), "clovis": ph("plains-farm"), "carlsbad": ph("carlsbad-caverns"),
    "alamogordo": ph("dust-storm"), "los-alamos": ph("los-alamos"), "ruidoso": ph("ruidoso-pines"),
}
TOOL_PHOTO = {
    "claim-gap-net-recovery-estimator": ph("calculator"), "depreciation-holdback-splitter": ph("paperwork"),
    "roof-area-pitch-converter": ph("roof-shingles"), "percentage-deductible-converter": ph("hail-hand"),
    "claim-calendar-builder": ph("clipboard"), "appraisal-file-checkup": ph("roofer"),
    "wildfire-contents-inventory-estimator": ph("wildfire-night"),
}
POST_PHOTO = {
    "wildfire-claim-after-total-loss": ph("wildfire-burned"), "hail-damage-on-flat-and-stucco-roofs": ph("stucco-wall"),
    "invoke-appraisal-new-mexico-policy": ph("paperwork"), "appraisal-or-public-adjuster-or-lawyer": ph("consultation"),
    "monsoon-water-damage-claims": ph("lightning"), "depreciation-and-holdback-explained": ph("calculator"),
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
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


def mark(uid="m"):
    """Brand mark: red tile, gold stepped (terraced) roofline and a sun disc. Same art as favicon.svg."""
    return (f'<svg viewBox="0 0 48 48" width="46" height="46" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#d0123b"/><stop offset="1" stop-color="#8f0723"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="9" fill="url(#{uid})"/>'
            '<circle cx="33" cy="15" r="5.5" fill="#ffd700"/>'
            '<path d="M7 38V29h6v-5h7v-7h8v7h7v5h6v9z" fill="#ffd700"/>'
            '<path d="M21 38v-6h6v6z" fill="#8f0723"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "NM", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NM", "availableLanguage": ["en"]}],
        "slogan": "Independent appraisal for disputed property claims across New Mexico",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 33 New Mexico counties.",
        "areaServed": [{"@type": "State", "name": "New Mexico"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Amount of loss", "Wildfire claims", "Hail damage", "Flat roofs", "Xactimate estimating"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
        "priceRange": "$$",
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
def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All cities we serve", LOC_BASE), True),
        ("Estimators", [(t["name"], tool_path(t)) for t in TOOLS], ("All free estimators", TOOL_BASE), False),
        ("Resources", [("Inside the appraisal process", PROCESS), ("Frequently asked questions", FAQ_P), ("Claim terms A to Z", GLOSS), ("Reading room", POST_BASE)], None, False),
    ]


def brand_link(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


def header():
    menu, acc = "", ""
    for i, (name, links, allk, cols) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="full"><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="mega{" cols" if cols else ""}">{li}</ul></li>'
        acc += (f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button>'
                f'<div class="acc-panel" id="acc-{i}"><ul>{li.replace(" class=\"full\"", "").replace(" class=\"all\"", "")}</ul></div></li>')
    tail = f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topline"><div class="wrap"><span>Independent appraisal for disputed property claims · All 33 New Mexico counties</span>
<div class="topline-r"><a class="hide-s" href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></div></div></div>
<header class="head"><div class="wrap">
{brand_link("mh")}
<nav aria-label="Main"><ul class="menu">{menu}{tail}</ul></nav>
<a class="btn small head-cta" href="tel:{TEL}">{ic("phone")} {PHONE}</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link("md")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}{tail}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>{HOURS} · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-cta"><div class="wrap"><h2>Covered claim, short check? Send us both estimates.</h2><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn light" href="{CONTACT}">Request a review</a></div></div></div>
<div class="wrap">
<div class="foot-cols">
<div>{brand_link("mf")}
<p style="margin-top:16px">Independent appraisal and estimating for property owners whose insurance claims don’t add up — from Farmington to Las Cruces and Hobbs to Gallup.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>{HOURS}</span></div></div>
<div><h2 class="fh">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="fh">Cities</h2><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h2 class="fh">Free estimators</h2><ul>{tl}</ul></div>
<div><h2 class="fh">Company</h2><ul><li><a href="{ABOUT}">About</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Claim terms</a></li><li><a href="{POST_BASE}">Reading room</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Notices &amp; disclaimer</a></li><li><a href="{HTMLMAP}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm and do not give legal advice, and we do not act as public adjusters. Content on this site is general information; policy language controls, and results are never guaranteed.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">Call now</a><a href="{CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, on_hero=True):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id, main_override = "WebPage", [], None, None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            main_override = n.get("mainEntity")
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
        nodes.append(n)
    photo = photo or HERO
    pimg = PHOTOS[photo]
    img_node = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": pimg["alt"]}
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY, "primaryImageOfPage": {"@id": img_node["@id"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for n in nodes if n.get("@type") in MAIN_TYPES]
    if main_override:
        webpage["mainEntity"] = main_override
    elif mains:
        webpage["mainEntity"] = {"@id": mains[0]}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage, img_node] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across New Mexico">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across New Mexico">
<meta name="geo.region" content="US-NM">
<meta name="geo.placename" content="New Mexico">
<meta name="theme-color" content="#bf0a30">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&family=Unbounded:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body{' class="on-hero"' if on_hero else ""}>
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
    # The host serves real files without running the front controller, so every directory page is
    # dir/index.php whose first line requires the canonical-host guard (www/http 301, preview noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts fade-up" style="animation-delay:.3s">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = (f'<div class="btn-row fade-up" style="animation-delay:.22s;margin-top:26px"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a>'
         f'<a class="btn light" href="{CONTACT}">Free claim review</a></div>') if cta else ""
    return (f'<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=" data-parallax=\"0.12\"")}<div class="wrap">{crumbs(trail)}'
            f'<span class="kicker light fade-up">{e(tag)}</span><h1 class="fade-up" style="animation-delay:.06s">{e(h1)}</h1>'
            f'<p class="lede fade-up" style="animation-delay:.14s">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="box call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. If appraisal isn’t the right tool, we’ll say so.</p>'
            f'<a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold" href="{CONTACT}">Send claim details</a></div>')


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span aria-hidden="true">›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Is the carrier’s number short?", p="Send the estimate and your photos. We’ll tell you plainly what we see."):
    return (f'<section class="cta-band"><div class="wrap"><div class="in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div>'
            f'<div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line" href="{CONTACT}">Email the estimate</a></div></div></div></section>')


LOSSES = ["Hail", "Wind / microburst", "Wildfire", "Fire / smoke", "Water / plumbing", "Monsoon roof leak", "Freeze / burst pipe", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", sub="Free review, no obligation. We usually reply within one business day.", page="/"):
    roles = ["Homeowner", "Business owner", "Property manager / HOA", "Landlord", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in New Mexico"]
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
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer paid or offered, and what you think is missing."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow", "ar")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead-card fade-up" style="animation-delay:.4s" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Get a free claim review</h2><p class="sub">A few details and we’ll call you back, usually within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn" type="submit">Request my review {ic("arrow", "ar")}</button>
<div class="form-msg" role="status"></div>
<div class="trust">{ic("shield")}<span>No obligation. Nothing is shared with your insurer.</span></div>
</form>"""


def contact_lines():
    return (f'<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li>'
            f'<li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>'
            f'<li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>{HOURS}</b></div></li>'
            f'<li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>Statewide · all 33 counties</b></div></li></ul>')


def pcard(href, photo, h, p, tag=None, hl="h3", more="Learn more"):
    t = f'<span class="num">{e(tag)}</span>' if tag else ""
    return (f'<a class="pcard rv" href="{href}"><span class="ph">{img(photo, sizes="(max-width:760px) 100vw, (max-width:1060px) 50vw, 400px", alt="")}{t}</span>'
            f'<span class="pb"><{hl}>{e(h)}</{hl}><p>{e(p)}</p><span class="more">{more}</span></span></a>')


def trow(t, hl="h3"):
    return (f'<a class="trow rv" href="{tool_path(t)}"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="150px", alt="")}<span>{e(t["icon"])}</span></span>'
            f'<span class="tb"><span class="kind">{e(t["kind"])}</span><{hl}>{e(t["name"])}</{hl}><p>{e(t["short"])}</p><span class="more">Open</span></span></a>')


def ccard(l):
    return (f'<a class="ccard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:760px) 50vw, 300px", alt="")}'
            f'<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>')


def post_card(p, hl="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:760px) 100vw, 400px", alt="")}</a>'
            f'<div class="pb"><span class="meta">{nice} · {e(p["read"])} read</span><{hl}><a href="{post_path(p)}">{e(p["title"])}</a></{hl}><p>{e(p["summary"])}</p>'
            f'<a class="more" href="{post_path(p)}">Read the guide</a></div></article>')


# ---------------------------------------------------------------- home
REGIONS = [
    ("Middle Rio Grande", "Albuquerque · Rio Rancho · Los Lunas", ["Hail", "Spring wind", "Monsoon leaks"],
     "The state’s largest housing market. Stucco ranch homes in the Northeast Heights, flat-roofed Pueblo Revival houses near the river and pitched-roof subdivisions on the West Mesa all take hail differently.", "abq-skyline"),
    ("Northern Mountains & Four Corners", "Santa Fe · Los Alamos · Farmington · Taos", ["Wildfire", "Freeze", "Snow load"],
     "Elevation changes everything: adobe and historic-district rules in Santa Fe, wildfire exposure in the Jemez and Sangre de Cristo foothills, and hard freezes that split pipes.", "santa-fe-adobe"),
    ("Eastern Plains & Pecos Valley", "Clovis · Roswell · Hobbs · Carlsbad", ["Large hail", "Tornadoes", "Straight-line wind"],
     "Open country where spring and summer storms can drop very large hail and spin up tornadoes. Oilfield growth adds commercial yards, apartments and new subdivisions to the claim mix.", "plains-farm"),
    ("Southern Desert & Sacramento Mountains", "Las Cruces · Alamogordo · Ruidoso", ["Microbursts", "Dust storms", "Wildfire & flash floods"],
     "Desert wind and monsoon downbursts around Las Cruces and the Tularosa Basin, and fire-then-flood risk in the forested mountains above Ruidoso.", "ruidoso-pines"),
]


def home():
    K = BRAND
    perils = [("hail", "Hail", "Roofs, coolers, stucco"), ("wind", "High wind", "Spring gusts & microbursts"), ("flame", "Wildfire", "Total & partial losses"),
              ("drop", "Water", "Plumbing & monsoon leaks"), ("snow", "Freeze", "Burst pipes & ice")]
    band = "".join(f'<li><span>{ic(i)}</span><div>{e(n)}<small>{e(s)}</small></div></li>' for i, n, s in perils)
    svc_cards = "".join(pcard(svc_path(s), SVC_PHOTO[s["slug"]], s["name"], s["short"], f"{i + 1:02d}") for i, s in enumerate(SERVICES[:9]))
    regions = "".join(
        f'<div class="rcard rv">{img(ph(p), sizes="(max-width:760px) 85vw, 320px", alt="")}<div class="in"><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>'
        f'<h3>{e(n)}</h3><p>{e(t)}</p><small>{e(cities)}</small></div></div>' for n, cities, chips, t, p in REGIONS)
    steps = [
        ("Free review", "We read the policy, the insurer’s estimate and your photos, then tell you honestly whether appraisal fits."),
        ("Inspect & measure", "Our own site visit, measurements and photos — never an edited copy of the carrier’s scope."),
        ("Price it locally", "A line-item estimate priced for your part of New Mexico, with code items and overhead handled the way your policy reads."),
        ("Work the panel", "We sit down with the insurer’s appraiser line by line. Many differences close at this stage."),
        ("Award", "Anything left goes to the umpire. Two signatures set the amount of loss."),
    ]
    stepper = "".join(f'<li class="step"><span class="dot">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    tools = "".join(trow(t) for t in TOOLS)
    cities = "".join(ccard(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree about the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to an umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster handles the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When does it make sense to call?", "When coverage has been accepted, you have the insurer’s itemized estimate, and the gap to a contractor’s number is meaningful — often more than about ten percent or several thousand dollars."),
        ("Is the award binding?", "On the amount of loss, generally yes once two of the three panel members sign. Coverage questions are separate and may need a New Mexico attorney."),
        ("What does appraisal cost?", "Each side usually pays its own appraiser and splits the umpire. Our fee is put in writing before any work starts, and the first conversation is free."),
        ("Do you work outside Albuquerque?", "Yes. We work statewide in all 33 counties, including Las Cruces, Santa Fe, the eastern plains, the Four Corners and the mountain communities."),
    ]
    body = f"""
<section class="hero">
<div class="hero-media">{img(HERO, lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-grid">
<div>
<span class="kicker light fade-up">Statewide · independent · policyholder-side</span>
<h1 class="fade-up" style="animation-delay:.08s"><span class="hl">{K}</span> for underpaid property claims</h1>
<p class="lede fade-up" style="animation-delay:.18s">When the insurer accepts the claim but the payment won’t rebuild the roof, the stucco or the house, {K} builds an independent, line-by-line valuation and takes it through the appraisal clause in your policy.</p>
<div class="btn-row fade-up" style="animation-delay:.28s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn light" href="#services">See our services {ic("arrow", "ar")}</a></div>
<ul class="hero-points fade-up" style="animation-delay:.38s"><li>{ic("check")}Your named appraiser</li><li>{ic("check")}Priced for New Mexico</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="peril-band" aria-label="Perils we appraise"><div class="wrap"><ul>{band}</ul></div></section>

<section class="sec"><div class="wrap split">
<div class="rv-l">
<span class="kicker">Why owners call us</span>
<h2>Covered isn’t the same as paid in full</h2>
<p>Most short claims aren’t denials. They’re missing parapet flashing, a stucco wall priced as a patch, a roof measured two squares small or a cooler nobody looked at. {K} exists for the gap between what the insurer agreed to cover and what the repair actually costs.</p>
<p>As a {K}, we work for the policyholder inside the appraisal process. We don’t argue coverage and we don’t inflate numbers — we document the loss well enough that the panel can see it.</p>
<ul class="ticks">
<li><span>{ic("check")}</span><div><b>An independent scope</b>Our own inspection and measurements before we read anyone else’s estimate.</div></li>
<li><span>{ic("check")}</span><div><b>Built for the umpire</b>Pricing and photos that hold up when a neutral reviews them, not just on day one.</div></li>
<li><span>{ic("check")}</span><div><b>Straight triage</b>If the claim needs an attorney or a supplement instead of appraisal, you’ll hear it on the first call.</div></li>
</ul>
<a class="btn line" href="{ABOUT}">How we work {ic("arrow", "ar")}</a>
</div>
<div class="photo-stack rv-r"><figure>{img(ph("roofer"), sizes="(max-width:1060px) 100vw, 560px")}</figure>
<div class="counters" aria-label="At a glance"><div class="counter"><b data-count="33">33</b><span>counties served</span></div><div class="counter"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>appraisal services</span></div><div class="counter"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free estimators</span></div></div>
</div>
</div></section>

<section class="sec sec-white terrace-top" id="services"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Appraisal &amp; estimating</span><h2>What {K} does for your claim</h2><p>Twelve services, one goal: a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="card-grid" data-stagger>{svc_cards}</div>
<div class="btn-row" style="justify-content:center;margin-top:40px"><a class="btn line" href="{SVC_BASE}">All twelve services {ic("arrow", "ar")}</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Four claim climates</span><h2>One state, very different losses</h2><p>Hail on the Llano Estacado, wildfire in the Sacramento Mountains, freezes in Los Alamos and monsoon microbursts in Las Cruces. A {K} has to know how each region’s weather shows up on a building — and in an estimate.</p></div>
<div class="region-row" data-stagger>{regions}</div>
</div></section>

<section class="sec sec-red"><div class="wrap">
<div class="sec-head rv"><span class="kicker light">How it works</span><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process. Here is how {K} moves a file through it.</p></div>
<ol class="stepper">{stepper}</ol>
<p style="margin-top:40px"><a href="{PROCESS}">Read the full appraisal process guide →</a></p>
</div></section>

<section class="sec sec-teal"><div class="wrap split">
<div class="rv-l"><span class="kicker light">Quick check</span><h2>Is the gap worth appraisal?</h2><p>Put in the two numbers you already have. A large difference is worth a conversation with a {K}; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}claim-gap-net-recovery-estimator/">claim gap net-recovery estimator</a> adds appraiser and umpire fees so you see a realistic net figure. Example numbers are illustrative.</p></div>
<div class="rv-r">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Free &amp; private</span><h2>Free estimators from {K}</h2><p>Check the insurer’s math before you call anyone. Every tool runs in your browser; nothing is stored or sent.</p></div>
<div class="tool-list" data-stagger>{tools}</div>
</div></section>

<section class="sec sec-cream"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Statewide</span><h2>Cities {K} serves most often</h2><p>We work in every New Mexico county. These local pages cover the places our claims come from most.</p></div>
<div class="city-grid" data-stagger>{cities}</div>
<div class="btn-row" style="justify-content:center;margin-top:36px"><a class="btn line" href="{LOC_BASE}">All cities we serve {ic("arrow", "ar")}</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head center rv"><span class="kicker">Choosing help</span><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="compare" data-stagger>
<div class="cmp us rv"><h3>{K}</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, number disputed</dd><dt>Outcome</dt><dd>Award signed by two of three panel members</dd></dl></div>
<div class="cmp rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare and negotiate the whole claim</dd><dt>Best stage</dt><dd>Early, from first notice</dd><dt>Outcome</dt><dd>Negotiated settlement</dd></dl></div>
<div class="cmp rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Coverage disputes, bad faith, litigation</dd><dt>Best stage</dt><dd>Denials and approaching deadlines</dd><dt>Outcome</dt><dd>Settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec sec-white"><div class="wrap split top">
<div class="rv-l"><span class="kicker">FAQ</span><h2>Questions for a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:22px"><a class="btn" href="{FAQ_P}">All questions {ic("arrow", "ar")}</a><a class="btn line" href="{GLOSS}">Claim terms A–Z</a></div></div>
<div class="rv-r">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Reading room</span><h2>Guides from {K}</h2><p>Practical reading on wildfire claims, hail on flat roofs, monsoon leaks and how to invoke appraisal.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="sec sec-ink" id="contact"><div class="wrap contact">
<div class="rv-l"><span class="kicker light">Start with a conversation</span><h2>Talk to {K}</h2><p>Tell us what happened and what the insurer offered. We’ll review it and tell you whether appraisal is worth pursuing — no pressure and no obligation.</p>{contact_lines()}</div>
<div class="rv-r">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Property Claim Appraisal",
                        "New Mexico Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wildfire and water claims.",
                        body, schema + [{"@type": "WebPage", "mainEntity": {"@id": DOMAIN + "/#business"}}], photo=HERO), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a href="{svc_path(r)}"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        photo = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), photo, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Cities we serve", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All cities", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["keyword"], "description": s["desc"],
                  "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "New Mexico"}, "url": DOMAIN + path,
                  "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=photo), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(pcard(svc_path(s), SVC_PHOTO[s["slug"]], s["name"], s["short"], f"{i + 1:02d}", hl="h2") for i, s in enumerate(SERVICES))
    photo = ph("roofer")
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across New Mexico",
                     "From a one-time estimate review to full appraisal-panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of the loss.", photo) + f"""
<section class="sec"><div class="wrap"><div class="card-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-white"><div class="wrap split top"><div class="rv-l"><span class="kicker">Not sure where to start?</span><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review answers that, and some disputes close right there.</p><a class="btn" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow", "ar")}</a></div>
<div class="rv-r">{faq_block([("Can I hire you for one step only?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and HOA claims?", "Yes: retail, office, warehouse, multifamily, churches, schools and HOA master policies."), ("Is every peril covered by appraisal?", "Appraisal can value any covered loss when the only disagreement is the amount. Whether something is covered is a separate question.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in New Mexico | 12 Types",
                             "Insurance appraisal services in New Mexico: appraisal clause representation, estimate review, hail, wildfire, water and freeze claims, umpires.",
                             body, schema, photo=photo), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Cities we serve", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        photo = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, New Mexico", e(l["lede"]), photo,
                         [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Claim risks around {e(l["city"])}</b><ul class="chips-row">{chips}</ul></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Cities we serve", items, path)}{list_box("Free estimators", [(t["name"], tool_path(t)) for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send the insurer’s estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, NM", "serviceType": "Insurance appraisal",
                  "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "New Mexico"}},
                  "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=photo), 0.8)

    trail = [("Home", "/"), ("Cities we serve", LOC_BASE)]
    cards = "".join(ccard(l) for l in LOCATIONS)
    reg = "".join(f'<div class="plain-card rv"><h2>{e(n)}</h2><p>{e(t)}</p><p style="font-size:.9rem;color:var(--muted);margin:0">{e(c)}</p></div>' for n, c, _x, t, _p in REGIONS)
    photo = ph("sandia-mountains", "abq-skyline")
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 33 New Mexico Counties",
                     f"{BRAND} works statewide, from the Four Corners to the Bootheel. These pages cover the cities where our claims come from most often.", photo) + f"""
<section class="sec"><div class="wrap"><div class="city-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-white"><div class="wrap"><div class="sec-head rv"><span class="kicker">Regions</span><h2>How claims change across New Mexico</h2><p>The same policy language plays out very differently in a Santa Fe adobe, a Rio Rancho tract home and a Ruidoso cabin.</p></div><div class="index-list" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your town?", "We cover every New Mexico county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "New Mexico Insurance Appraiser Cities | Statewide",
                             "Cities we serve as a New Mexico insurance appraiser: Albuquerque, Las Cruces, Santa Fe, Rio Rancho, Roswell, Ruidoso and every other county.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f"{n}, NM", p) for n, p in items])], photo=photo), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = tool_path(t)
        trail = [("Home", "/"), ("Estimators", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{tool_path(o)}"><small>{e(o["kind"])}</small>{e(o["name"])}</a>' for o in [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)])
        photo = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), photo, cta=False) + f"""
<section class="sec tight" style="padding-bottom:0"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint disclaim">For planning only. Results depend on what you enter and on your policy, and they aren’t a quote, an appraisal or legal advice. Default figures are illustrative.</p></div></section>
<div class="wrap layout" style="padding-top:44px"><article class="prose">{t["explain"]}
<h2>Questions about this estimator</h2>{faq_block(t["faqs"])}
<h2>More free estimators</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All estimators", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send the estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"],
                  "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                  "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=photo), 0.8)

    trail = [("Home", "/"), ("Estimators", TOOL_BASE)]
    rows = "".join(trow(t, hl="h2") for t in TOOLS)
    photo = ph("calculator")
    body = page_hero(trail, "Free & private", "Free Claim Estimators for New Mexico Property Owners",
                     "Seven calculators, planners and checklists built from real appraisal work. No sign-up and nothing stored — everything runs in your browser.", photo, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-list" data-stagger>{rows}</div></div></section>
<section class="sec sec-white"><div class="wrap split top"><div class="rv-l"><span class="kicker">Suggested order</span><h2>Using the estimators together</h2><ol>
<li>Map your dates first with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a>.</li>
<li>Check roof measurements with the <a href="{TOOL_BASE}roof-area-pitch-converter/">roof area &amp; pitch converter</a>.</li>
<li>See what you’re owed with the <a href="{TOOL_BASE}percentage-deductible-converter/">deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-splitter/">depreciation</a> tools.</li>
<li>After a wildfire, start the <a href="{TOOL_BASE}wildfire-contents-inventory-estimator/">contents inventory estimator</a>.</li>
<li>Test the dispute in the <a href="{TOOL_BASE}claim-gap-net-recovery-estimator/">net-recovery estimator</a>, then run the <a href="{TOOL_BASE}appraisal-file-checkup/">file checkup</a>.</li></ol></div><div class="rv-r">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | New Mexico",
                              "Free insurance claim calculators for New Mexico owners: appraisal cost, depreciation, roof squares, deductibles, deadlines and contents.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo=photo), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("Inside the appraisal process", PROCESS), ("Frequently asked questions", FAQ_P), ("Claim terms A to Z", GLOSS), ("Reading room", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    photo = ph("paperwork")
    body = page_hero(trail, "Process guide", "Inside the Insurance Appraisal Process, Step by Step",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what and where New Mexico claims most often stall.", photo,
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Decides", "Amount of loss")]) + f"""
<div class="wrap layout"><article class="prose">{re.sub(r"<h2>Step (\d+):", r'<h2 id="step-\1">Step \1:', PROCESS_BODY)}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in New Mexico", "description": "The seven stages of a property insurance appraisal, from disagreement to award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, n in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process Guide | 7 Steps in New Mexico",
                         "An insurance appraisal process guide for New Mexico claims: the written demand, naming appraisers, the umpire, pricing and the final award.",
                         body, [crumbs_schema(trail), howto], photo=photo), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("FAQ", path)]
    groups = "".join(f"<h2>{e(g)}</h2>{faq_block(qs)}" for g, qs in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    photo = ph("living-room", "consultation")
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions, Grouped by Topic",
                     "Plain answers about how appraisal works, what it costs, how long it takes and how it fits New Mexico claims.", photo) + f"""
<div class="wrap layout"><article class="prose">{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Costs, Timing & NM Rules",
                         "Insurance appraisal FAQ grouped by topic: how appraisal works, costs and fees, timing, New Mexico specifics and what to expect from us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo=photo), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    photo = ph("clipboard")
    body = page_hero(trail, "Reference", "Insurance Claim Terms from A to Z",
                     f"{len(GLOSSARY)} words you’ll meet in policies, estimates and appraisal awards — including the flat-roof and adobe vocabulary specific to New Mexico.", photo, cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “canale” or “umpire”"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim terms A to Z", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | Searchable A to Z Terms",
                         "A searchable insurance claim glossary: ACV, RCV, umpire, appraisal award, canales, parapets, percentage deductibles and dozens more terms.",
                         body, [crumbs_schema(trail), dts], photo=photo), 0.7)

    for i, p in enumerate(POSTS):
        path = post_path(p)
        trail = [("Home", "/"), ("Reading room", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{post_path(o)}"><small>Guide</small>{e(o["title"])}</a>' for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        photo = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), photo, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free estimators", [(t["name"], tool_path(t)) for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "keywords": p["keyword"], "datePublished": p["date"], "dateModified": p["date"],
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US",
               "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=photo), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Reading room", path)]
    cards = "".join(post_card(p, hl="h2") for p in POSTS)
    photo = ph("storm-desert")
    body = page_hero(trail, "Reading room", "Insurance Claim Guides for New Mexico Owners",
                     "Practical reading on wildfire losses, hail on flat roofs, monsoon leaks, depreciation and when to invoke appraisal.", photo, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Claim Guides | New Mexico Reading Room",
                         "Insurance claim guides for New Mexico property owners: wildfire total losses, hail on flat roofs, monsoon leaks, depreciation and appraisal.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], post_path(p)) for p in POSTS])], photo=photo), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    photo = ph("consultation")
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "An independent appraisal and estimating practice for New Mexico property owners whose claims are covered but underpaid.", photo) + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img(ph("stucco-home"), sizes="(max-width:1060px) 100vw, 780px")}</figure>
<h2>One question, answered carefully</h2>
<p>{BRAND} focuses on the amount of loss. We don’t sell roofs, we don’t argue coverage and we don’t run lawsuits. We measure, document and price damage so that the people deciding a claim — the insurer’s appraiser, an umpire, or the adjuster before it ever gets that far — can see what the repair really costs.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before numbers.</strong> We inspect and measure before reading anyone else’s estimate.</li>
<li><strong>Local pricing.</strong> Material and labor costs in Farmington, Hobbs and Santa Fe aren’t the same; estimates should reflect where the property is.</li>
<li><strong>Defensible, not inflated.</strong> An estimate that can’t survive an umpire doesn’t help you. We price what we can support.</li>
<li><strong>Plain English.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, landlords, HOA boards, property managers, churches and business owners across New Mexico, as well as the contractors and attorneys who represent them. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We aren’t public adjusters. We don’t guarantee results — no honest appraiser can. If your claim has been denied or a deadline is close, we’ll suggest talking to a New Mexico attorney first.</p>
<h2>Built for New Mexico buildings</h2>
<p>Parapet walls and canales, three-coat stucco, viga ceilings, evaporative coolers, metal mountain roofs and manufactured homes all show up in New Mexico claims, and generic estimates often price them poorly. Knowing how they’re built — and repaired — is most of the job.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free estimators", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, f"About {BRAND} | Our Approach",
                         "About New Mexico Insurance Appraiser: an independent practice focused on the amount of loss for covered but underpaid property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage", "mainEntity": {"@id": DOMAIN + "/#business"}}], photo=photo), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    photo = ph("paperwork", "consultation")
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send the form. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", photo, cta=False) + f"""
<section class="sec sec-ink"><div class="wrap contact">
<div class="rv-l"><span class="kicker light">Direct lines</span><h2>Reach us directly</h2>{contact_lines()}
<h3>Helpful to have ready</h3><ul><li>Your declarations page</li><li>The insurer’s full itemized estimate</li><li>Letters or emails from the insurer</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv-r">{lead_form("Send your claim details", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Contact New Mexico Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, or send details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage", "mainEntity": {"@id": DOMAIN + "/#business"}}], photo=photo, on_hero=True), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy & Cookies", "Privacy Policy & Cookies | New Mexico Insurance Appraiser",
                  "Privacy policy for New Mexico Insurance Appraiser: what we collect through forms and calls, how we use it, cookies and how to reach us.",
                  "How we collect, use and protect what you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to give us — your name, phone, email, property location and claim details. Our web host also records standard technical data (IP address, browser, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To reply to you and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our website and email, or when the law requires it.</p>
<h2>Estimators and calculators</h2><p>Our claim estimators run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics later, this page will say so.</p>
<h2>Text messages</h2><p>If you agree to texts, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve shared by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Website Use", "Terms of Website Use | New Mexico Insurance Appraiser",
                "Terms of website use for New Mexico Insurance Appraiser: no client relationship from browsing, no legal advice, estimator limits and liability.",
                "The terms that apply when you use this website and its estimators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in New Mexico.</p>
<h2>No client relationship</h2><p>Reading the site, using an estimator or sending a form doesn’t create an appraiser–client relationship. That starts only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. For legal questions, consult a licensed New Mexico attorney.</p>
<h2>Estimators</h2><p>Calculators give planning figures based on what you enter. They aren’t appraisals, quotes or predictions of a claim outcome.</p>
<h2>Content and images</h2><p>Site text, design and tools belong to {BRAND}. You may link to pages and print them for personal use. Photographs are public-domain or CC0 images used for illustration and don’t show client properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of New Mexico.</p>"""),
        DISCLAIM: ("Notices & Disclaimer", "Disclaimer & Important Notices | NM Insurance Appraiser",
                   "Disclaimer and notices from New Mexico Insurance Appraiser: general information only, no legal advice, illustrative figures and deadlines.",
                   "Important limits on the information published here.", f"""
<h2>General information only</h2><p>This website explains how insurance appraisal commonly works. Your own policy and its endorsements control. Read them carefully.</p>
<h2>Not legal advice; not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Illustrative figures</h2><p>Any dollar amounts on this site are illustrative examples. They aren’t results for any client, and no appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies set deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here changes any deadline. If one is approaching, contact a New Mexico attorney promptly.</p>
<h2>Bad faith and legal claims</h2><p>New Mexico’s Insurance Code lists unfair claims practices, and New Mexico courts recognize bad-faith claims. Whether either applies to a claim is a legal question for an attorney, not something we evaluate.</p>
<h2>References and photos</h2><p>Mentions of agencies, programs and weather events are for context; verify current facts with official sources such as the New Mexico Office of Superintendent of Insurance. Photos are illustrative public-domain or CC0 images and don’t depict client properties.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        photo = ph("office-building", "commercial-center")
        body = page_hero(trail, "Legal", h1, lede, photo, cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo=photo), 0.3)


def sitemap_pages():
    path = HTMLMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Cities we serve", [("All cities", LOC_BASE)] + [(f'{l["city"]}, NM', loc_path(l)) for l in LOCATIONS]),
        ("Free estimators", [("All estimators", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy & cookies", PRIVACY), ("Terms of website use", TERMS), ("Notices & disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="plain-card rv"><h2>{e(g)}</h2><ul style="padding-left:1.1em;margin:0">{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    photo = ph("rio-grande", "abq-skyline")
    body = page_hero(trail, "Navigation", "Site Map: Every Page in One Place", f"All {len(pages) + 1} pages on {BRAND}, grouped by section.", photo, cta=False) + \
        f'<section class="sec"><div class="wrap"><div class="index-list" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"HTML Site Map | {BRAND}",
                         "HTML site map for New Mexico Insurance Appraiser: every service, city page, free estimator, guide and legal page linked from one place.",
                         body, [crumbs_schema(trail)], photo=photo), 0.3)

    photo = ph("dust-storm", "storm-desert")
    body = (f'<section class="page-hero">{img(photo, "bg", lazy=False, alt="")}<div class="wrap"><span class="kicker light">Error 404</span><h1>This page blew off in the spring wind</h1>'
            f'<p class="lede">The page you wanted isn’t here. It may have moved, or the link may be mistyped. Try one of these instead.</p>'
            f'<div class="btn-row" style="margin-top:24px"><a class="btn gold" href="/">Home</a><a class="btn light" href="{SVC_BASE}">Services</a><a class="btn light" href="{TOOL_BASE}">Free estimators</a><a class="btn light" href="{CONTACT}">Contact</a></div></div></section>')
    write("/404.html", document("/404.html", f"Page Not Found (404) | {BRAND}",
                                "Page not found on New Mexico Insurance Appraiser. The link may be old or mistyped; use these links to reach services, estimators or contact.",
                                body, robots="noindex,follow", photo=photo), sitemap=False)


GUARD_PHP = r"""<?php
// New Mexico Insurance Appraiser - canonical host guard. Required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nmia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nmia_real  = 'newmexicoinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nmia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://newmexicoinsuranceappraiser.com - only on the real domain.
if ($nmia_host === 'www.' . $nmia_real || ($nmia_host === $nmia_real && $nmia_proto === 'http')) {
    header('Location: https://' . $nmia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// /dir/index.php (and /index.php) are duplicate URLs: 301 to the directory.
$nmia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nmia_uri, '?'), $nmia_m)) {
    $nmia_q = strpos($nmia_uri, '?') !== false ? substr($nmia_uri, strpos($nmia_uri, '?')) : '';
    header('Location: ' . $nmia_m[1] . $nmia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($nmia_host !== $nmia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// New Mexico Insurance Appraiser - front controller for the static build.
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
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w", encoding="utf-8") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, "_guard.php"), "w", encoding="utf-8") as f:
        f.write(GUARD_PHP)
    # Search Console verification: exact single line, no newline, no BOM, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private", "*.log*"))
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    sitemap_pages()
    root_files()
    for dp, _, fs in os.walk(OUT):
        assert "index.html" not in fs, f"stray index.html in {dp}"
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
