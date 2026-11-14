#!/usr/bin/env python3
"""Static site generator for pennsylvaniainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.

Pages are written as dir/index.php (first line: the canonical-host guard, then static HTML).
The homepage is home.html, served by the root index.php front controller.
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
from learn import PROCESS_STEPS, PROCESS_INTRO, PROCESS_OUTRO, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Pennsylvania Insurance Appraiser"
HOST = "pennsylvaniainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/property-appraisal-services/"
LOC_BASE = "/where-we-work/"
TOOL_BASE = "/claim-calculators/"
POST_BASE = "/policy-and-claim-guides/"
P_PROCESS = "/appraisal-process-explained/"
P_FAQ = "/insurance-appraisal-faq/"
P_GLOSS = "/claim-terms-glossary/"
P_ABOUT = "/about-us/"
P_CONTACT = "/contact-us/"
P_PRIVACY = "/privacy/"
P_TERMS = "/terms/"
P_DISC = "/legal-disclaimer/"
P_MAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, PA"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
# Every photo is CC0 or public domain (source + license recorded in src/photos.json; not published on the site).


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consult-table", "home-insurance-claim-appraisal": "house-porch",
    "commercial-hoa-claim-appraisal": "apartments", "roof-hail-damage-appraisal": "roof-shingles",
    "windstorm-tornado-appraisal": "tornado-damage", "tropical-storm-remnant-appraisal": "flood-street",
    "water-damage-claim-appraisal": "water-ceiling", "fire-smoke-damage-appraisal": "house-fire",
    "ice-dam-frozen-pipe-appraisal": "icicles", "insurance-estimate-audit": "calc-papers",
    "umpire-neutral-services": "meeting",
}
LOC_PHOTO = {
    "philadelphia": "philadelphia", "pittsburgh": "pittsburgh", "allentown": "brick-rowhomes", "erie": "snow-street",
    "reading": "rowhouse-street", "scranton": "victorian-house", "lancaster": "farm-barn", "harrisburg": "harrisburg",
    "state-college": "college-town", "wilkes-barre": "river-town", "york": "brick-rowhomes-2", "johnstown": "hill-town",
}
TOOL_PHOTO = {
    "claim-gap-fee-projector": "calc-papers", "rcv-acv-holdback-calculator": "interior",
    "roof-pitch-squares-estimator": "roof-slate", "deductible-impact-calculator": "storm-sky",
    "claim-deadline-calendar": "clipboard", "appraisal-readiness-checkup": "inspector",
    "roof-snow-load-estimator": "snow-roofs",
}
POST_PHOTO = {
    "pennsylvania-appraisal-clause-guide": "consult-table", "one-year-suit-limitation-and-appraisal": "clipboard",
    "flood-or-water-damage-after-tropical-remnants": "flood-street", "ice-dam-and-frozen-pipe-claims": "icicles",
    "rowhome-flat-roof-claims": "rowhouse-street", "mine-subsidence-sinkholes-and-your-policy": "river-town",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 4 13c0-6 6-10 16-10 0 10-4 16-10 16"/><path d="M4 21c4-6 8-9 12-11"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ' class="i"'
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark():
    """Keystone mark: navy keystone, gold rim, white roof chevron."""
    return ('<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true">'
            '<path d="M6 5h36l-6 38H12z" fill="#002A86"/>'
            '<path d="M10.2 9h27.6l-4.9 30H15.1z" fill="none" stroke="#FFCE00" stroke-width="2.6" stroke-linejoin="round"/>'
            '<path d="M16 27.5l8-7.5 8 7.5" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M19.5 26v6.5h9V26" fill="none" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Pennsylvania</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/favicon-512.png", "contentUrl": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "PA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-PA", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Pennsylvania property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 67 Pennsylvania counties.",
        "areaServed": [{"@type": "State", "name": "Pennsylvania"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Ice dam claims", "Hail and wind damage", "Water damage claims"],
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


# ---------------------------------------------------------------- GTM
def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],\n"
            f"j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\nheight="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal process explained", P_PROCESS), ("Insurance appraisal FAQ", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Policy & claim guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Where we work", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Pennsylvania areas", LOC_BASE)),
        ("Calculators", [(t["name"], tool_path(t)) for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "chev")}</button><ul class="sub{wide}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">About</a></li><li><a class="top-link" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-veil" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-d")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 67 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    res = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN + [("About us", P_ABOUT), ("Contact us", P_CONTACT)])
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Carrier’s number doesn’t cover the repair? Let’s look at it together.</p><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Send your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-f")}
<p>Independent appraisal and estimating help for Pennsylvania property owners whose insurance claims came in short — from Lake Erie to the Schuylkill.</p>
<p class="foot-lines"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET</span></p></div>
<div class="foot-col"><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div class="foot-col"><h2 class="foot-h">Where we work</h2><ul class="two">{loc}</ul></div>
<div class="foot-col"><h2 class="foot-h">Free calculators</h2><ul>{tl}</ul></div>
<div class="foot-col"><h2 class="foot-h">Resources</h2><ul>{res}</ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we don’t give legal advice, and we are not public adjusters. Information on this site is general and educational; policy language controls and results are never guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    page_extra = {}
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            page_extra = {k: v for k, v in n.items() if k != "@type"}
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
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra.append(n)
    img_key = photo or "hero"
    pimg = PHOTOS[img_key]
    img_url = f"{DOMAIN}/assets/img/photos/{img_key}.webp"
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": img_url, "contentUrl": img_url, "width": pimg["fw"], "height": pimg["fh"]},
    }
    webpage.update(page_extra)
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    order = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")
    mains = sorted([n for n in extra if n.get("@type") in order], key=lambda n: order.index(n["@type"]))
    webpage["mainEntity"] = {"@id": mains[0]["@id"]} if mains else {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = ""
    if photo:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {PHOTOS[photo]["fw"]}w" imagesizes="100vw" fetchpriority="high">\n'
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Pennsylvania">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Pennsylvania">
<meta name="geo.region" content="US-PA">
<meta name="geo.placename" content="Pennsylvania">
<meta name="theme-color" content="#002A86">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Schibsted+Grotesk:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{body_cls}">
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
    """/ -> home.html; /x.html -> x.html at the root; /dir/ -> dir/index.php with the guard line first."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
        depth = rel.count("/")
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
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
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="p-hero"><div class="p-hero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.15"')}</div><div class="wrap p-hero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-h">Talk it through, free</h2><p>Tell us what the carrier offered. We’ll say honestly whether appraisal makes sense.</p><a class="side-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def aside(*boxes):
    return f'<aside class="side"><div class="side-sticky">{"".join(boxes)}</div></aside>'


def cta_strip(h="Carrier’s estimate missing things?", p="Send it to us. We’ll review it line by line and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-navy" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Wind / hail", "Ice dam / frozen pipe", "Snow load", "Water / leak", "Fire / smoke", "Tree impact", "Tropical storm remnants", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", uid="f"):
    roles = ["Homeowner", "Landlord / rental owner", "Commercial owner", "HOA / condo board", "Property manager", "Contractor", "Attorney or public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Pennsylvania"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-h">{e(heading)}</h2><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property location</label><select id="{uid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>
<div class="full"><label for="{uid}-det">What happened, and where does the claim stand?</label><textarea id="{uid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="{P_PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="hero-form-tag">Free claim review</p>
<h2 class="hero-form-h">Is your settlement short?</h2><p class="form-sub">Leave a number. We’ll call within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{P_PRIVACY}">privacy policy</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hero-form-note">{ic("shield")} No obligation. Nothing is shared.</p>
</form>"""


def contact_lines():
    return f"""<ul class="c-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 67 Pennsylvania counties</b></div></li></ul>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Southeastern PA", "philadelphia", "Philadelphia and the collar counties: rowhome flat roofs, party walls, burst pipes in old housing and the Ida-era split between flood and covered water.", ["philadelphia"]),
    ("Lehigh Valley & Berks", "brick-rowhomes", "Allentown and Reading: brick rows, twins, warehouses and the limestone sinkhole question that sits under parts of the valley.", ["allentown", "reading"]),
    ("Northeastern PA", "victorian-house", "Scranton, Wilkes-Barre and the Poconos: heavy snow, river flooding history and the coal-region mine subsidence issue.", ["scranton", "wilkes-barre"]),
    ("South Central PA", "farm-barn", "Harrisburg, Lancaster and York: Susquehanna flooding history, stone farmhouses, bank barns and spring hail.", ["harrisburg", "lancaster", "york"]),
    ("Central PA", "college-town", "State College and the ridge-and-valley country: student rentals, ice storms and wind funnelled along the ridges.", ["state-college"]),
    ("Western PA", "pittsburgh", "Pittsburgh, Johnstown and Erie: hillside homes, flash floods in the hollows and lake-effect snow loads.", ["pittsburgh", "johnstown", "erie"]),
]

SEASONS = [
    ("snow", "Winter", "Dec – Mar", ["Burst and frozen pipes", "Ice dams and attic leaks", "Snow-load collapse", "Ice storms and fallen limbs"],
     "The Blizzard of 1993, the January 1996 blizzard, the February 2010 storms and Erie’s Christmas 2017 lake-effect snow all left roof and water claims behind."),
    ("bolt", "Spring", "Apr – Jun", ["Hail and severe storms", "Tornadoes", "Flash flooding", "Roof wind damage"],
     "Western Pennsylvania’s May 31, 1985 tornado outbreak and Agnes in June 1972 are the reminders every adjuster in the state knows."),
    ("sun", "Summer", "Jul – Sep", ["Tropical storm remnants", "Lightning fires", "Downbursts and trees", "Water through roofs"],
     "Remnants of Ivan (2004), Lee (2011), Ida (2021) and Debby (2024) showed how much rain a fading tropical system can drop inland."),
    ("leaf", "Fall", "Oct – Nov", ["Nor’easters and wind", "Clogged gutters and leaks", "Early freezes", "Power-outage losses"],
     "Superstorm Sandy in October 2012 brought hours of wind, fallen trees and long outages across the eastern half of the state."),
]


def home():
    K = BRAND
    svc_cards = "".join(
        f'<a class="s-card rv" href="{svc_path(s)}"><span class="s-card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="s-card-b"><span class="s-num">{i + 1:02d}</span><h3>{e(s["name"])}</h3><span class="s-txt">{e(s["short"])}</span><span class="s-more">Learn more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES))
    seasons = "".join(
        f'<article class="season rv"><header><span class="season-ic">{ic(icn)}</span><h3>{n}</h3><span class="season-m">{m}</span></header><ul>{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(note)}</p></article>'
        for icn, n, m, perils, note in SEASONS)
    steps = [
        ("Free review", "We read the policy, the carrier’s estimate and your photos, then tell you plainly whether appraisal fits."),
        ("Our own scope", "A Pennsylvania Insurance Appraiser inspects, measures and writes a line-item estimate priced for your area."),
        ("Written demand", "Appraisal is demanded in writing and your appraiser is named, with the suit-limitation date in view."),
        ("Panel work", "Both appraisers compare scope and pricing line by line. Most of the gap is settled here."),
        ("Signed award", "An umpire decides anything left. Two of three signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="tl-step"><span class="tl-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    regions = "".join(
        f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p>{e(t)}</p><p class="region-links">{" · ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]["city"])}</a>" for c in cs)}</p></div></article>'
        for n, ph, t, cs in REGIONS)
    city_chips = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a></li>' for l in LOCATIONS)
    tools = "".join(
        f'<a class="t-card rv" href="{tool_path(t)}"><span class="t-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="t-ic" aria-hidden="true">{t["icon"]}</span></span><span class="t-b"><span class="t-kind">{t["kind"]}</span><h3>{e(t["name"])}</h3><span class="t-txt">{e(t["short"])}</span></span></a>'
        for t in TOOLS)
    posts = "".join(
        f'<article class="g-card rv"><a class="g-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="g-b"><p class="g-meta">{e(p["read"])} read · Guide</p><h3><a href="{post_path(p)}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, write an independent line-item estimate, work with the carrier’s appraiser and, if needed, take unresolved items to a neutral umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster, licensed by the Pennsylvania Insurance Department, handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and a contractor’s line-item estimate is meaningful — often more than about 10% or several thousand dollars."),
        ("Does appraisal stop my one-year suit deadline?", "Not automatically. Many Pennsylvania policies limit lawsuits to one year from the date of loss, and appraisal may not pause that clock unless the policy or a written agreement says so. If the date is close, talk to a Pennsylvania attorney."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my county?", "Yes. We work in all 67 Pennsylvania counties, with frequent work around Philadelphia, Pittsburgh, the Lehigh Valley, Harrisburg, Lancaster, Scranton and Erie."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero", lazy=False, alt="", extra=' data-parallax="0.25"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-gold">Independent appraisal · All 67 counties</p>
<h1>{K}: a second, independent number for your property claim</h1>
<p class="lede">When the insurer accepts the claim but the check won’t cover the repair, {K} writes its own line-by-line valuation and carries it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="#services">See our services {ic("arrow")}</a></div>
<ul class="hero-points"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Homes, rentals, HOAs &amp; commercial</li><li>{ic("check")}Fee in writing up front</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap ledger-in">
<div class="ledger-i rv"><b data-count="67">67</b><span>Pennsylvania counties served</span></div>
<div class="ledger-i rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="ledger-i rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
<div class="ledger-i rv"><b>2 of 3</b><span>Signatures make an award binding</span></div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-copy rv">
<p class="kicker">What we do</p>
<h2>What a {K} does — and doesn’t</h2>
<p class="drop">Most underpaid claims in Pennsylvania aren’t denied. They’re short. A slate roof priced as asphalt, a rowhome flat roof patched on paper when it needs replacing, plaster walls written up as drywall, a frozen-pipe loss with half the tear-out missing. {K} exists for the gap between “covered” and “paid in full.”</p>
<p>We value the loss from scratch — our own inspection, measurements and pricing — and we build numbers that hold up in front of an umpire. If your problem is really a coverage denial, a bad-faith question or a looming deadline, we’ll tell you on the first call that you need a Pennsylvania attorney instead.</p>
<div class="fit">
<div class="fit-yes"><h3>{ic("check")} Appraisal usually fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair vs. replace arguments</li><li>Matching, slate and specialty materials</li><li>Missing trades, code items and O&amp;P</li></ul></div>
<div class="fit-no"><h3>{ic("x")} It usually doesn’t</h3><ul><li>Outright coverage denials</li><li>Bad-faith or legal claims</li><li>Flood losses under a homeowner policy</li><li>Gaps too small to justify fees</li></ul></div>
</div>
<a class="btn btn-navy" href="{P_ABOUT}">About {K} {ic("arrow")}</a>
</div>
<figure class="intro-fig rv">{img("inspector", sizes="(max-width:900px) 100vw, 520px")}<figcaption>Every valuation starts with our own inspection, not an edited copy of the carrier’s estimate.</figcaption></figure>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Services</p><h2>Appraisal services from {K}</h2><p>{len(SERVICES)} services built around one job: a valuation of your loss that holds up. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="s-grid" data-stagger>{svc_cards}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">Compare all services {ic("arrow")}</a></p>
</div></section>

<section class="sec seasons-sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Pennsylvania’s claim year</p><h2>The four seasons a {K} plans around</h2><p>Pennsylvania weather sends a different kind of claim every quarter. Knowing what each season does to a roof, a pipe or a basement is half of writing an accurate estimate.</p></div>
<div class="seasons" data-stagger>{seasons}</div>
</div></section>

<section class="sec sec-navy"><div class="wrap">
<div class="sec-head light rv"><p class="kicker kicker-gold">How it works</p><h2>From first call to signed award with {K}</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how a file moves.</p></div>
<ol class="timeline-h" data-timeline><span class="tl-track" aria-hidden="true"><span class="tl-fill"></span></span>{proc}</ol>
<p class="center mt"><a class="link-light" href="{P_PROCESS}">Read the full appraisal process, step by step</a></p>
</div></section>

<section class="sec gap-sec"><div class="wrap gap-in">
<div class="rv"><p class="kicker">Quick gap check</p><h2>Is your gap big enough for a {K}?</h2><p>Type in the two numbers you already have. A large difference is worth a conversation; a small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-projector/">claim gap &amp; fee projector</a> adds appraiser and umpire fees so you see a realistic net.</p><a class="btn btn-navy" href="{TOOL_BASE}">All {len(TOOLS)} free calculators {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec sec-paper"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Statewide</p><h2>Six regions, one {K}</h2><p>A flat roof in South Philly, a slate roof in Scranton’s Hill Section and a bank barn outside Lancaster fail in different ways. Here is how claims differ across the state.</p></div>
<div class="regions" data-stagger>{regions}</div>
<h3 class="cities-h rv">Cities we visit most</h3>
<ul class="city-chips" data-stagger>{city_chips}</ul>
<p class="center mt"><a class="btn btn-line" href="{LOC_BASE}">See every area we serve {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free calculators from {K}</h2><p>Run the numbers before you pick up the phone. Every calculator works in your browser; nothing is stored or sent.</p></div>
<div class="t-grid" data-stagger>{tools}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each one solves a different problem. Picking the right one first saves time and fees, and {K} will point you elsewhere when appraisal isn’t the tool.</p></div>
<div class="who" data-stagger>
<article class="who-c who-us rv"><p class="who-tag">You are here</p><h3>{K}</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Award signed by two of three</dd></dl></article>
<article class="who-c rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare and negotiate the whole claim</dd><dt>Best stage</dt><dd>Early, soon after the loss</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></article>
<article class="who-c rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Coverage, bad faith, litigation</dd><dt>Best stage</dt><dd>Denials and close deadlines</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></article>
</div>
</div></section>

<section class="cta-photo">{img("storm-sky", "cta-photo-bg", alt="", extra=' data-parallax="0.2"')}<div class="wrap cta-photo-in rv"><p class="kicker kicker-gold">Before you sign the release</p><h2>Check the numbers with a {K} first</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair — and from missing a one-year suit date while you argue about it.</p><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec"><div class="wrap faq-split">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers on how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{P_FAQ}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sec-paper"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on Pennsylvania policy language, documentation and timing.</p></div>
<div class="g-grid" data-stagger>{posts}</div>
<p class="center mt"><a class="btn btn-line" href="{POST_BASE}">All policy &amp; claim guides {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-navy" id="contact"><div class="wrap contact-in">
<div class="rv"><p class="kicker kicker-gold">Start with a conversation</p><h2>Talk to {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>{contact_lines()}</div>
<div class="rv">{lead_form(page="/", uid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Claim Appraisal & Review",
                        f"{BRAND}: independent appraisal, estimate review and umpire help for underpaid storm, ice, water and fire claims.",
                        body, [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)], photo="hero", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All Pennsylvania areas", LOC_BASE)]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], svc_path(r)) for r in rel])}
</article>
{aside(call_box(), list_box("All services", items, path), list_box("Where we work", locs))}</div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["name"], "serviceType": s["keyword"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                   "areaServed": {"@type": "State", "name": "Pennsylvania"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="s-card rv" href="{svc_path(s)}"><span class="s-card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="s-card-b"><span class="s-num">{i + 1:02d}</span><h2 class="h3">{e(s["name"])}</h2><span class="s-txt">{e(s["short"])}</span><span class="s-more">Learn more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Pennsylvania",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "contractor") + f"""
<section class="sec"><div class="wrap"><div class="s-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and plenty of disputes close at that stage with a documented supplement.</p><a class="btn btn-navy" href="{SVC_BASE}insurance-estimate-audit/">About estimate reviews {ic("arrow")}</a></div>
<div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and HOA claims?", "Yes: apartment buildings, condo associations, retail, office, industrial, churches and mixed-use properties."), ("Do you handle flood claims?", "Not under a homeowner policy’s appraisal clause. Flood is excluded from standard homeowner policies and NFIP claims have their own process, but we can value the covered wind and water damage from the same storm.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Pennsylvania",
                             "Pennsylvania insurance appraisal services: appraisal clause work, estimate review, storm, ice dam, water and fire claims, plus umpire help.",
                             body, schema, photo="contractor"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Where we work", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                         [("County", l["county"]), ("Housing", l["housing"]), ("Storm on record", l["storm"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="peril-box"><p class="peril-h">Common local claim risks</p><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul class="cols2">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby areas</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
{aside(call_box(), list_box("Pennsylvania areas", items, path), list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]),
                  {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"},
                   "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Pennsylvania"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Where we work", LOC_BASE)]
    cards = "".join(
        f'<a class="l-card rv" href="{loc_path(l)}"><span class="l-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}</span><span class="l-b"><span class="t-kind">{e(l["region"])}</span><h2 class="h3">{e(l["city"])}</h2><span class="l-c">{e(l["county"])} · {e(l["housing"])}</span></span></a>'
        for l in LOCATIONS)
    regions = "".join(f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:700px) 100vw, 380px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p>{e(t)}</p></div></article>' for n, ph, t, _c in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 67 Pennsylvania Counties",
                     f"{BRAND} works statewide, from the Lake Erie shore to the Schuylkill and the Susquehanna. These pages cover the cities where we handle claims most often.", "philadelphia") + f"""
<section class="sec"><div class="wrap"><div class="l-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-paper"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across Pennsylvania</h2><p>The same policy wording plays out very differently on a rowhome flat roof, a hillside brick house and a stone farmhouse.</p></div><div class="regions" data-stagger>{regions}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Pennsylvania county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Pennsylvania Insurance Appraiser Service Areas",
                             "Insurance appraisal in all 67 Pennsylvania counties, including Philadelphia, Pittsburgh, Allentown, Erie, Harrisburg, Lancaster and Scranton.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="philadelphia"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = tool_path(t)
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms; they aren’t a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2>{related([(o["kind"], o["name"], tool_path(o)) for o in others])}</article>
{aside(call_box(), list_box("All calculators", items, path))}</div>
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]),
                  {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
                   "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(
        f'<a class="t-card rv" href="{tool_path(t)}"><span class="t-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="t-ic" aria-hidden="true">{t["icon"]}</span></span><span class="t-b"><span class="t-kind">{t["kind"]}</span><h2 class="h3">{e(t["name"])}</h2><span class="t-txt">{e(t["short"])}</span></span></a>'
        for t in TOOLS)
    order = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a> — {e(w)}</li>' for t, w in zip(
        [TOOLS[4], TOOLS[2], TOOLS[6], TOOLS[3], TOOLS[1], TOOLS[0], TOOLS[5]],
        ["calendar the suit and holdback dates first", "check the roof measurements", "if winter weight played a part", "see what the deductible takes", "split RCV, ACV and holdback", "test whether the dispute is worth fees", "finish with a file checkup"]))
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Pennsylvania",
                     f"{len(TOOLS)} calculators and planners shaped by real appraisal work. Use them to understand your claim, check the carrier’s math and plan the next step — no sign-up, nothing stored.", "calc-desk", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="t-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="steps-list">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Pennsylvania",
                              "Free insurance claim calculators: claim gap, RCV vs ACV, roof squares, deductible, snow load, deadline calendar and an appraisal checkup.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="calc-desk"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal process explained", path)]
    steps = "".join(f'<li class="v-step" id="step-{i + 1}"><span class="v-num">{i + 1}</span><div><h2>{e(n)}</h2>{h}</div></li>' for i, (n, h) in enumerate(PROCESS_STEPS))
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(n)}</a></li>' for i, (n, _h) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Pennsylvania",
                     f"{len(PROCESS_STEPS)} stages, from the first disagreement to payment: what happens, who does what and where Pennsylvania claims most often stall.", "clipboard",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_INTRO}<ol class="v-steps" data-vline>{steps}</ol>{PROCESS_OUTRO}</article>
{aside(call_box(), f'<div class="side-box"><h2 class="side-h">On this page</h2><ol class="side-list toc">{toc}</ol></div>', list_box("Resources", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Pennsylvania", "description": "The stages of a Pennsylvania property insurance appraisal, from the disagreement to the signed award and payment.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, _h) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Pennsylvania",
                         "Step-by-step guide to insurance appraisal in Pennsylvania: the written demand, appraisers, the umpire, the award and the one-year suit clause.",
                         body, [crumbs_schema(trail), howto], photo="clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Insurance appraisal FAQ", path)]
    slug = lambda g: "faq-" + "".join(c if c.isalnum() else "-" for c in g.lower()).strip("-")
    groups = "".join(f'<h2 id="{slug(g)}">{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    jump = "".join(f'<li><a href="#{slug(g)}">{e(g)}</a></li>' for g, _ in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for Pennsylvania Owners",
                     "Plain answers to the questions we hear most, grouped by topic: getting started, fees, deadlines, Pennsylvania rules and working with your insurer.", "interior") + f"""
<div class="wrap layout"><article class="prose"><ul class="jump">{jump}</ul>{groups}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Pennsylvania Claims",
                         "Insurance appraisal FAQ for Pennsylvania: how it works, fees, the one-year suit clause, the Insurance Department, FAIR Plan and flood.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="interior"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="g-item"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Property Insurance Claim Terms Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in Pennsylvania policies, estimates and appraisal awards, defined in plain English. Type to filter.", "calc-papers", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="glossary">{dl}</dl><p class="gloss-empty" hidden>No terms match that search.</p></article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "Searchable claim terms glossary: plain-English definitions of ACV, RCV, holdback, appraisal award, umpire, mine subsidence and more.",
                         body, [crumbs_schema(trail), dts], photo="calc-papers"), 0.7)

    for idx, p in enumerate(POSTS):
        path = post_path(p)
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], post_path(o)) for o in others])}</article>
{aside(call_box(), list_box("Resources", LEARN), list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
               "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["keyword"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(
        f'<article class="g-card rv"><a class="g-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="g-b"><p class="g-meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</p><h2 class="h3"><a href="{post_path(p)}">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS)
    body = page_hero(trail, "Policy & claim guides", "Pennsylvania Policy and Claim Guides",
                     "Practical guides on Pennsylvania policy language, documentation and timing, written from the appraisal side of the table.", "snow-roofs", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="g-grid" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Policy & Claim Guides for Pennsylvania Owners",
                         "Pennsylvania policy and claim guides: the appraisal clause, one-year suit clause, flood vs water, ice dams, rowhome roofs and subsidence.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], post_path(p)) for p in POSTS])], photo="snow-roofs"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About us", path)]
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.", "consult-table") + f"""
<div class="wrap layout"><article class="prose">
<figure class="wide-fig">{img("meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Plenty of claim professionals do a little of everything. We chose one question — the amount of loss — and built our process, calculators and documentation standards around answering it well. That focus lets {BRAND} serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we study anyone else’s numbers.</li>
<li><strong>Defensible over dramatic.</strong> An inflated estimate looks good on day one and loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs a Pennsylvania attorney or a licensed public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, rowhome and condo owners, landlords, HOA and condo boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Pennsylvania. On any one claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t guarantee outcomes — no honest appraiser can — and we don’t publish testimonials or case results.</p>
<h2>Statewide, on purpose</h2>
<p>Pennsylvania packs lake-effect snow belts, ridge-and-valley wind, river towns with long flood histories and dense rowhome cities into one state. Working all 67 counties means we see every kind of loss it produces and price each with local knowledge.</p>
</article>{aside(call_box(), list_box("Explore", [("Our services", SVC_BASE), ("Where we work", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process explained", P_PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, f"About Us | {BRAND}",
                         f"About {BRAND}: an independent appraisal and estimating practice focused on the amount of loss in disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="consult-table"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "meeting", cta=False) + f"""
<section class="sec sec-navy"><div class="wrap contact-in">
<div class="rv"><p class="kicker kicker-gold">Direct lines</p><h2>Reach us directly</h2>{contact_lines()}
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s full line-item estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li><li>Your policy’s suit-limitation date, if you know it</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, uid="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         f"Contact {BRAND} for a free review of a disputed claim. Call or text (844) 537-1427, or email us your estimate.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="meeting"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Policy", "Privacy Policy | Pennsylvania Insurance Appraiser",
                    "Privacy policy for Pennsylvania Insurance Appraiser: what we collect through forms, calls and email, how we use it and the choices you have.",
                    "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to give us — such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. The numbers you type aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will be updated to describe it.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        P_TERMS: ("Terms of Use", "Terms of Use | Pennsylvania Insurance Appraiser",
                  "Terms of use for the Pennsylvania Insurance Appraiser website and its free claim calculators, including limits on reliance and liability.",
                  "The terms that apply when you use this website and its calculators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Pennsylvania.</p>
<h2>No professional relationship</h2><p>Reading this site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a Pennsylvania attorney for legal questions.</p>
<h2>Calculators and estimates</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photographs</h2><p>Site text, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the Commonwealth of Pennsylvania.</p>"""),
        P_DISC: ("Disclaimer", "Legal Disclaimer | Pennsylvania Insurance Appraiser",
                 "Legal disclaimer for Pennsylvania Insurance Appraiser: general information only, not legal advice, no guaranteed results.",
                 "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Dollar figures on this site are illustrative examples, not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits — in many Pennsylvania policies, one year from the date of loss. Nothing on this site extends or changes any deadline. If one is approaching, consult a Pennsylvania attorney promptly.</p>
<h2>Statutes, agencies and storms</h2><p>References to statutes, the Pennsylvania Insurance Department, the FAIR Plan, the Mine Subsidence Insurance program or past weather events are for context. Verify current law and facts with official sources.</p>
<h2>Photographs</h2><p>Photos are royalty-free public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article>{aside(call_box())}</div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo="office"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", P_ABOUT), ("Contact us", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Where we work", [("All areas", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free calculators", [("All calculators", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN[:3] + [("All guides", POST_BASE)] + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIVACY), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2 class="h3">{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on the {BRAND} website, grouped by section.", "office", cta=False) + f'<section class="sec"><div class="wrap map-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}",
                         f"HTML site map for {BRAND}: every service, Pennsylvania city page, free calculator, guide and policy page in one list.",
                         body, [crumbs_schema(trail), item_list([(n, p) for _, links in groups for n, p in links])], photo="office"), 0.3)

    body = f"""<section class="p-hero p-hero-404"><div class="p-hero-bg">{img("storm-sky", lazy=False, alt="")}</div><div class="wrap p-hero-in"><p class="kicker kicker-gold">Error 404</p><h1>That page isn’t here</h1><p class="lede">It may have moved, or the link may be mistyped. Try one of these instead.</p><div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line-light" href="{SVC_BASE}">Services</a><a class="btn btn-line-light" href="{TOOL_BASE}">Calculators</a><a class="btn btn-line-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                f"Sorry, this page could not be found on {BRAND}. Use the links here to reach our services, calculators or contact page.",
                                body, [crumbs_schema([("Home", "/"), ("Page not found", "/404.html")])], robots="noindex,follow", photo="storm-sky"), sitemap=False)


GUARD_PHP = r"""<?php
// Pennsylvania Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$pia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$pia_real  = 'pennsylvaniainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$pia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://pennsylvaniainsuranceappraiser.com - only on the real domain.
if ($pia_host === 'www.' . $pia_real || ($pia_host === $pia_real && $pia_proto === 'http')) {
    header('Location: https://' . $pia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$pia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($pia_uri, '?'), $pia_m)) {
    $pia_q = strpos($pia_uri, '?') !== false ? substr($pia_uri, strpos($pia_uri, '?')) : '';
    header('Location: ' . $pia_m[1] . $pia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($pia_host !== $pia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Pennsylvania Insurance Appraiser - front controller for the static build.
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
    # Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private", "*.log"))
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
