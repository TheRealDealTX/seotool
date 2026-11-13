#!/usr/bin/env python3
"""Static site generator for utahinsuranceappraiser.com.

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
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Utah Insurance Appraiser"
HOST = "utahinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""

SVC_BASE = "/utah-appraisal-services/"
LOC_BASE = "/utah-communities/"
TOOL_BASE = "/utah-claim-calculators/"
POST_BASE = "/utah-claim-articles/"
ABOUT = "/our-company/"
CONTACT = "/contact-utah-appraiser/"
PROCESS = "/how-utah-appraisal-works/"
FAQ_P = "/utah-appraisal-faq/"
GLOSS = "/claim-terms-glossary/"
PRIVACY = "/your-privacy/"
TERMS = "/use-terms/"
DISC = "/legal-disclaimers/"
CREDITS = "/photo-credits/"
SITEMAP = "/utah-site-map/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
CITIES_SCHEMA = [l["city"] for l in LOCATIONS]

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
    "policy-appraisal-representation": "meeting-table", "home-insurance-appraisal": "home-exterior",
    "commercial-hoa-appraisal": "office-tower", "hail-roof-damage-appraisal": "roof-shingles",
    "canyon-wind-damage-appraisal": "wind-damage", "snow-ice-freeze-appraisal": "icicles",
    "water-pipe-leak-appraisal": "damaged-interior", "fire-smoke-damage-appraisal": "house-fire",
    "wildfire-claim-appraisal": "wildfire", "earthquake-claim-appraisal": "brick-house",
    "insurance-estimate-audit": "laptop-numbers", "appraisal-umpire-services": "panel-meeting",
}
LOC_PHOTO = {
    "salt-lake-city": "slc-skyline", "west-valley-city": "suburb-street", "sandy": "sandy",
    "provo": "provo", "orem": "orem", "lehi": "lehi", "ogden": "ogden",
    "layton": "layton", "st-george": "st-george", "logan": "logan", "park-city": "park-city",
    "cedar-city": "lightning",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator", "rcv-acv-holdback-calculator": "documents",
    "roof-pitch-squares-estimator": "roof-shingles", "percentage-deductible-calculator": "brick-house",
    "claim-timeline-planner": "laptop-numbers", "appraisal-readiness-checkup": "contractor",
    "roof-snow-load-estimator": "roof-snow",
}
POST_PHOTO = {
    "utah-appraisal-clause-guide": "meeting-table", "snow-load-ice-dam-claims": "roof-snow",
    "canyon-windstorm-claim-checklist": "wind-damage", "earthquake-coverage-deductibles": "brick-house",
    "wildfire-smoke-documentation": "wildfire-smoke", "choosing-claim-help": "panel-meeting",
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
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(uid="m"):
    return (f'<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#123574"/><stop offset="1" stop-color="#071d49"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="11" fill="url(#{uid})"/>'
            '<circle cx="33" cy="15" r="5" fill="#e0703a"/>'
            '<path d="M6 37l11-15 6 8 5-6 14 13z" fill="#ffffff"/>'
            '<path d="M17 22l3.2 4.4-2.4-1.2-2.5 2.2z" fill="#c9d3e6"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "UT", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-UT", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Utah property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 29 Utah counties.",
        "areaServed": [{"@type": "State", "name": "Utah"}] + [{"@type": "City", "name": c} for c in CITIES_SCHEMA],
        "hasOfferCatalog": {"@type": "OfferCatalog", "@id": DOMAIN + "/#services", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Snow load", "Wildfire claims", "Earthquake endorsements"],
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
LEARN = [("How appraisal works", PROCESS), ("Appraisal FAQ", FAQ_P), ("Claim terms glossary", GLOSS), ("Claim articles", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE)),
        ("Communities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Utah communities", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for name, links, allk in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", "ico sm")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false">{name}{ic("chev", "ico chev")}</button><ul class="sub{wide}">{li}</ul></li>'
    menu += f'<li><a class="top-a" href="{ABOUT}">Company</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ico chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">Company</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head" id="top"><div class="shell">
<a class="brand" href="/" aria-label="{BRAND} home">{mark("mh")}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<nav class="nav" aria-label="Main"><ul class="nav-list">{menu}</ul></nav>
<div class="head-act"><a class="phone-pill" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-accent head-cta" href="{CONTACT}">Free claim review</a></div>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark("md")}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a><button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm MT · All 29 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="shell"><h2>Questions about a Utah claim? Start with a free review.</h2><div class="row-btns"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-l" href="{CONTACT}">Email the estimate</a></div></div></div>
<div class="shell foot-grid">
<div class="foot-about"><a class="brand" href="/">{mark("mf")}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal and estimating help for property owners with disputed insurance claims, from Cache Valley to Washington County.</p>
<p class="foot-lines"><a href="tel:{TEL}">{PHONE_INTL}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><span>Mon–Fri 8am–6pm MT</span></p></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Communities</h3><ul class="two">{loc}</ul></div>
<div><h3>Calculators</h3><ul>{tl}</ul></div>
<div><h3>Company</h3><ul><li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact</a></li><li><a href="{PROCESS}">How appraisal works</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Articles</a></li></ul></div>
</div>
<div class="shell foot-base"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISC}">Disclaimers</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="shell foot-legal">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Content on this site is general and educational, policy wording varies, and example figures are illustrative. No outcome is guaranteed.</p>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, body_cls="page"):
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
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = preload or "hero-home"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main_types = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")
    main = [n["@id"] for t in main_types for n in extra_nodes if n.get("@type") == t]
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Utah">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Utah">
<meta name="geo.region" content="US-UT">
<meta name="geo.placename" content="Utah">
<meta name="theme-color" content="#071d49">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Urbanist:wght@600;700;800&family=Work+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.replace("no-js","js")</script>
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
    # Pages are served as dir/index.php: the host serves real files without running the front
    # controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="row-btns"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="sub-hero"><div class="sub-hero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.1"')}</div><div class="shell sub-hero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}<span class="plus" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-t">Talk it through, free</h2><p>Send the carrier’s estimate or call. We’ll tell you plainly whether appraisal is worth it.</p><a class="side-phone" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-accent btn-block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow", "ico sm")}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-t">{e(title)}</h2><ul class="side-links">{li}</ul></div>'


def layout(article, aside):
    return f'<div class="shell two-col"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


def cta_strip(h="Does the carrier’s number feel low?", p="Send the estimate and a few photos. We’ll review it and tell you what we see, at no cost."):
    return f"""<section class="cta-strip"><div class="shell cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="row-btns"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-l" href="{CONTACT}">Send claim details</a></div></div></section>"""


def related(items):
    return '<div class="rel-grid">' + "".join(f'<a class="rel" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow", "ico sm")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Wind", "Snow load / ice dam", "Frozen or burst pipe", "Water leak", "Fire / smoke", "Wildfire", "Earthquake", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", uid="f"):
    roles = ["Homeowner", "Commercial owner", "HOA board / manager", "Landlord", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Utah"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="lead-sub">{e(sub)}</p>
<div class="fields">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property location</label><select id="{uid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>
<div class="full"><label for="{uid}-det">What happened and where does the claim stand?</label><textarea id="{uid}-det" name="details" rows="4" placeholder="Date of loss, what the insurer paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-card" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Get a free claim review</h2><p class="lead-sub">A few details and we’ll call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What was damaged by?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy policy</a>.</span></label>
<button class="btn btn-accent btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="card-note">{ic("shield")}<span>No obligation. Nothing is shared without your permission.</span></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Wasatch Front", "Salt Lake, Davis & Weber counties", "slc-skyline",
     "Canyon windstorms, summer hail, ice dams and the occasional tornado, layered over century-old brick homes, mid-century ranches and high-rise condos.",
     ["Canyon wind", "Hail", "Ice dams", "Earthquake"]),
    ("Utah Valley", "Provo, Orem, Lehi & south county", "provo",
     "Fast-growing subdivisions, student rentals and foothill homes exposed to hail, wildfire smoke and winter water losses.",
     ["Hail", "Wildfire smoke", "Rental water losses"]),
    ("Mountain resorts", "Park City, Heber & Ogden Valley", "park-city",
     "The heaviest snow loads in the state, frozen pipes in empty second homes and high-end finishes that valley pricing misses.",
     ["Snow load", "Frozen pipes", "High-value finishes"]),
    ("Northern valleys", "Logan & Cache Valley", "logan",
     "Long, cold winters and agricultural outbuildings make frozen pipes, snow-load collapses and barn claims a regular pattern.",
     ["Extreme cold", "Snow load", "Outbuildings"]),
    ("Southern Utah", "St. George, Cedar City & Iron County", "st-george",
     "Monsoon wind, flash floods, stucco and tile roofs, plus wildfire country around Brian Head and Cedar Mountain.",
     ["Monsoon wind", "Tile roofs", "Wildfire"]),
]

HISTORY = [
    ("1983", "Spring snowmelt floods", "A record snowpack melted fast, turning State Street in Salt Lake City into a sandbagged channel and flooding communities statewide."),
    ("1999", "Salt Lake City tornado", "On August 11, a tornado crossed downtown, the Avenues and Capitol Hill, damaging hundreds of buildings."),
    ("2005", "Santa Clara River flood", "In January, flooding on the Santa Clara and Virgin rivers destroyed and damaged homes in Washington County."),
    ("2011", "Davis County windstorm", "On December 1, downslope gusts over 100 mph tore through Centerville, Farmington and neighboring towns."),
    ("2017", "Brian Head Fire", "A summer wildfire in Iron and Garfield counties burned for weeks and destroyed homes and cabins."),
    ("2020", "Magna earthquake & windstorm", "A magnitude 5.7 quake in March, then a September downslope windstorm that toppled thousands of trees."),
    ("2023", "Record snowpack winter", "Months of heavy snow led to roof and carport failures, ice dams and spring flood worries across northern Utah."),
]


def home():
    svc_cards = "".join(
        f'<a class="svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="svc-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="svc-n">{i + 1:02d}</span><span class="svc-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow", "ico sm")}</span></span></a>'
        for i, s in enumerate(SERVICES))
    bands = "".join(
        f'<li class="band{" on" if i == 0 else ""}" tabindex="0">{img(ph, sizes="(max-width:900px) 100vw, 50vw", alt="")}<div class="band-in"><span class="band-k">{e(sub)}</span><h3>{e(n)}</h3><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul></div></li>'
        for i, (n, sub, ph, t, chips) in enumerate(REGIONS))
    rail = "".join(f'<li class="rv"><span class="dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS_STEPS[1:7]))
    hist = "".join(f'<li class="rv"><span class="yr">{y}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for y, t, d in HISTORY)
    tool_cards = "".join(
        f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tool-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tool-ic">{t["icon"]}</span></span><span class="tool-b"><small>{e(t["kind"])}</small><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    comm = "".join(f'<li class="rv"><a href="{loc_path(l)}"><span class="c-name">{e(l["city"])}</span><span class="c-county">{e(l["county"])}</span>{ic("arrow", "ico sm")}</a></li>' for l in LOCATIONS)
    posts = "".join(
        f'<article class="post-card rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><small>{p["read"]} read</small><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])

    home_faqs = [
        ("What does a Utah Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your selected appraiser, we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster presents and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When does it make sense to call a Utah Insurance Appraiser?", "When coverage has been accepted, you have the insurer’s estimate, and the gap between it and a contractor’s number is meaningful. As a rough guide, more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once any two of the three panel members sign. It doesn’t decide coverage."),
        ("What does appraisal cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work starts. The first conversation is free."),
        ("Do you work outside the Wasatch Front?", "Yes. We cover all 29 Utah counties, including Cache Valley, the mountain resort areas and southern Utah."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="shell hero-in">
<div class="hero-copy">
<p class="kicker">Independent claim appraisal · All 29 Utah counties</p>
<h1>Utah Insurance Appraiser for claims that came up short</h1>
<p class="lede">Your insurer agreed the damage is covered, then sent a number that won’t rebuild it. Utah Insurance Appraiser prepares an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="row-btns"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="#services">See what we value</a></div>
<ul class="hero-ticks"><li>{ic("check")}Retained by you, never the carrier</li><li>{ic("check")}Homes, HOAs and commercial</li><li>{ic("check")}Free first review</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="proof" aria-label="At a glance"><div class="shell"><ul class="proof-in">
<li><b data-count="29">29</b><span>Utah counties covered</span></li>
<li><b data-count="12">12</b><span>Appraisal &amp; estimating services</span></li>
<li><b data-count="7">7</b><span>Free claim calculators</span></li>
<li><b>2 of 3</b><span>Signatures make an award binding</span></li>
</ul></div></section>

<section class="sec"><div class="shell intro">
<div class="intro-media rv">
<figure class="im-a">{img("contractor", sizes="(max-width:900px) 90vw, 460px")}</figure>
<figure class="im-b">{img("roof-shingles", sizes="(max-width:900px) 60vw, 300px")}</figure>
<p class="im-tag">{ic("ruler")}<span>We measure first, then price</span></p>
</div>
<div class="intro-copy rv">
<p class="kicker dark">Why owners call</p>
<h2>What a Utah Insurance Appraiser actually fixes</h2>
<p>Most underpaid claims aren’t denials. They’re estimates that stop short: two roof slopes instead of four, a basement floor patched when the planks are discontinued, drywall replaced with no allowance for the knockdown texture. Utah Insurance Appraiser exists for the space between “covered” and “paid in full.”</p>
<ul class="ticks">
<li>{ic("check")}<div><b>Our own scope, from the building up</b><span>We inspect and measure before we look at anyone else’s numbers.</span></div></li>
<li>{ic("check")}<div><b>Numbers that hold up</b><span>Valuations built to survive an umpire’s questions, not just to look big.</span></div></li>
<li>{ic("check")}<div><b>Straight answers</b><span>If your claim needs an attorney or a supplement instead, you’ll hear it on the first call.</span></div></li>
</ul>
<a class="btn btn-navy" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec sec-tint" id="services"><div class="shell">
<div class="sec-head rv"><p class="kicker dark">Services</p><h2>Utah Insurance Appraiser services for every kind of loss</h2><p>Twelve services, one goal: a valuation of your loss that stands up. Bring Utah Insurance Appraiser in for a quick estimate review or once appraisal has been demanded.</p></div>
<div class="svc-grid" data-stagger>{svc_cards}</div>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head left rv"><p class="kicker dark">Five claim climates</p><h2>Same policy, very different Utah losses</h2><p>Hail in Orem, canyon wind in Layton, roof-crushing snow in Park City, sub-zero cold in Logan and monsoon storms in St. George. A Utah Insurance Appraiser has to know how each region’s weather shows up in a building and in an estimate.</p></div>
<ul class="bands rv" data-bands>{bands}</ul>
</div></section>

<section class="sec sec-navy" id="gap-check"><div class="shell split">
<div class="rv"><p class="kicker">Quick gap check</p><h2>Is the gap big enough for appraisal?</h2><p>Enter the two numbers you already have. A large difference is worth a conversation with a Utah Insurance Appraiser. A small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap and fee estimator</a> subtracts appraiser and umpire fees so you see a realistic net.</p><a class="btn btn-accent" href="{TOOL_BASE}">All seven calculators {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker dark">The process</p><h2>From written demand to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process. Here is the route Utah Insurance Appraiser takes once an amount dispute is confirmed.</p></div>
<ol class="rail" data-rail>{rail}</ol>
<p class="center"><a class="link" href="{PROCESS}">Read the full step-by-step guide</a></p>
</div></section>

<section class="sec sec-sand"><div class="shell split top">
<div class="rv sticky-col"><p class="kicker dark">Utah storm record</p><h2>Events that shaped Utah claims</h2><p>Utah’s biggest property losses rarely come from one kind of storm. Floods, tornadoes, windstorms, wildfire, earthquakes and record snow have all tested local policies. Utah Insurance Appraiser keeps that history in mind when reading damage and policy language.</p>{img("storm-sky", "hist-img", sizes="(max-width:900px) 100vw, 480px")}</div>
<ol class="history">{hist}</ol>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker dark">Free and private</p><h2>Claim calculators from a Utah Insurance Appraiser</h2><p>Check the numbers before you call anyone. Each calculator runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="tool-grid" data-stagger>{tool_cards}</div>
</div></section>

<section class="sec sec-tint"><div class="shell comm">
<div class="comm-banner rv">{img("slc-skyline", sizes="(max-width:900px) 100vw, 520px", alt="")}<div class="comm-banner-in"><p class="kicker">Statewide</p><h3>Utah Insurance Appraiser communities</h3><p>We travel to every county. These are the cities where Utah Insurance Appraiser handles claims most often.</p><a class="btn btn-accent" href="{LOC_BASE}">All Utah communities</a></div></div>
<ul class="comm-list" data-stagger>{comm}</ul>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker dark">Right tool, right time</p><h2>Is appraisal the right move for your claim?</h2><p>Appraisal solves one problem well. A good Utah Insurance Appraiser will tell you when your claim needs something else.</p></div>
<div class="fit">
<div class="fit-card yes rv"><h3>{ic("check")}Appraisal usually fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair versus replace disagreements</li><li>Matching and discontinued materials</li><li>Missing trades, code items or overhead and profit</li></ul></div>
<div class="fit-card no rv"><h3>{ic("x")}Look elsewhere first</h3><ul><li>Outright denials and coverage disputes</li><li>Claims-handling or bad-faith concerns</li><li>Gaps too small to justify fees</li><li>A suit deadline that’s close</li></ul></div>
</div>
</div></section>

<section class="sec sec-sand"><div class="shell split top">
<div class="rv"><p class="kicker dark">FAQ</p><h2>Questions people ask a Utah Insurance Appraiser</h2><p>Plain answers about the process, the cost and when appraisal is the wrong move.</p><div class="row-btns"><a class="btn btn-navy" href="{FAQ_P}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker dark">Articles</p><h2>Reading before you demand appraisal</h2><p>Practical articles from Utah Insurance Appraiser on policy wording, winter claims and documentation.</p></div>
<div class="post-grid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All claim articles</a></p>
</div></section>

<section class="photo-cta"><div class="photo-cta-bg">{img("wasatch-snow", alt="", extra=' data-parallax="0.12"')}</div><div class="shell rv"><p class="kicker">Before you sign off</p><h2>Check the numbers before you accept the check</h2><p>A short, free review can keep you from accepting a settlement that won’t cover the repair.</p><div class="row-btns"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="#contact">Send your estimate</a></div></div></section>

<section class="sec sec-navy" id="contact"><div class="shell split contact">
<div class="rv"><p class="kicker">Start here</p><h2>Talk with a Utah Insurance Appraiser</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="c-lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm MT</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 29 Utah counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", uid="hf")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Utah Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, snow, water, fire and wildfire claims.",
                        body, [faq_schema(home_faqs)], preload="hero-home", body_cls="page home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        art = s["body"] + f'<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}<h2>Related services</h2>' + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(art, call_box() + list_box("All services", items, path) + list_box("Communities", locs + [("All Utah communities", LOC_BASE)])) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Utah"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="svc-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span><span class="svc-n">{i + 1:02d}</span><span class="svc-b"><h2 class="h3">{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow", "ico sm")}</span></span></a>'
        for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Utah",
                     "From a single estimate review to full panel representation and neutral umpire work, every service is built around one thing: an accurate, defensible valuation of your loss.", "contractor") + f"""
<section class="sec"><div class="shell"><div class="svc-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-sand"><div class="shell split top"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review gives you that answer quickly, and many disputes close at that stage.</p><a class="btn btn-navy" href="{SVC_BASE}insurance-estimate-audit/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, cabins, condos, multifamily, retail, office, industrial, churches and HOA communities."), ("Is earthquake damage something you appraise?", "Yes, when the property carries earthquake coverage and the insurer disputes the amount.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Utah | Claim Valuation",
                             "Utah insurance appraisal services: appraisal clause representation, estimate review, hail, wind, snow, water, fire, wildfire and umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload="contractor"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        city = l["city"]
        trail = [("Home", "/"), ("Communities", LOC_BASE), (city, path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        art = f'<div class="callout"><b>Local claim risks</b><ul class="chips">{chips}</ul></div>' + l["body"] + \
            f'<h2>Services for {e(city)} property owners</h2><p>Every {BRAND} service is available in {e(city)} and across {e(l["county"])}, including:</p><ul class="cols2">{svc_links}</ul>' + \
            f'<h2>Questions from {e(city)} owners</h2>{faq_block(l["faqs"])}<h2>Nearby communities</h2>' + related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {city}, Utah", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + \
            layout(art, call_box() + list_box("Utah communities", items, path) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + \
            cta_strip(f"Disputed claim in {city}?", "Send the estimate and your photos. We’ll tell you what we see, at no cost.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {city}, Utah", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Utah"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {city}, UT | Claim Appraisal"
        if len(title) > 58:
            title = f"Insurance Appraiser {city}, UT | Claims"
        desc = f"Independent insurance appraiser serving {city} and {l['county']}, Utah: appraisal and estimate review for underpaid storm, water and fire claims."
        if len(desc) > 150:
            desc = f"Independent insurance appraiser for {city} and {l['county']}, Utah: appraisal and estimate review for underpaid property claims."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Communities", LOC_BASE)]
    comm = "".join(f'<li class="rv"><a href="{loc_path(l)}"><span class="c-name">{e(l["city"])}</span><span class="c-county">{e(l["county"])}</span>{ic("arrow", "ico sm")}</a></li>' for l in LOCATIONS)
    reg = "".join(f'<div class="reg-card rv">{img(ph, sizes="(max-width:700px) 100vw, 33vw", alt="")}<div><small>{e(sub)}</small><h2 class="h3">{e(n)}</h2><p>{e(t)}</p></div></div>' for n, sub, ph, t, _c in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 29 Utah Counties",
                     "We work statewide, from Cache Valley to the red rock of Washington County. These pages cover the communities where we handle claims most often.", "slc-skyline") + f"""
<section class="sec"><div class="shell"><ul class="comm-list wide" data-stagger>{comm}</ul></div></section>
<section class="sec sec-sand"><div class="shell"><div class="sec-head left rv"><p class="kicker dark">Regions</p><h2>How claims differ across Utah</h2><p>The same policy language plays out very differently in an Avenues bungalow, a Park City condo and a St. George stucco home.</p></div><div class="reg-grid" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your city?", "We cover every Utah county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Utah Insurance Appraiser Communities | All 29 Counties",
                             "Insurance appraisal across all 29 Utah counties, including Salt Lake City, Provo, Ogden, Layton, St. George, Logan, Park City and Cedar City.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload="slc-skyline"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + f'<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}<h2>More free calculators</h2>' + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], t["lede"], ph, cta=False) + \
            f'<section class="sec tool-sec"><div class="shell"><div class="rv">{t["markup"]}</div><p class="tool-note">For planning only. Results depend on what you enter and on your policy, and aren’t a quote, an appraisal or legal advice. Nothing you enter is stored.</p></div></section>' + \
            layout(art, call_box() + list_box("All calculators", items, path)) + cta_strip("Want a professional to check the math?", "Send your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(
        f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tool-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tool-ic">{t["icon"]}</span></span><span class="tool-b"><small>{e(t["kind"])}</small><h2 class="h3">{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    order = "".join(f'<li><a href="{TOOL_BASE}{s}/">{n}</a>: {d}</li>' for s, n, d in [
        ("claim-timeline-planner", "Timeline planner", "map the deadlines first so nothing lapses."),
        ("roof-pitch-squares-estimator", "Roof pitch & squares", "check the roof measurements."),
        ("roof-snow-load-estimator", "Snow load estimator", "for winter roof and carport claims."),
        ("percentage-deductible-calculator", "Percentage deductible", "and "), ])
    order = order.replace("and </li>", f'see what you’d actually receive, alongside the <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">holdback calculator</a>.</li>')
    order += f'<li><a href="{TOOL_BASE}claim-gap-fee-estimator/">Gap &amp; fee estimator</a>: test whether appraisal pays after fees.</li><li><a href="{TOOL_BASE}appraisal-readiness-checkup/">Readiness checkup</a>: finish with a file check.</li>'
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Utah Owners",
                     "Seven calculators and planners built around real appraisal questions. Check the insurer’s math and plan next steps. No sign-up, and nothing is stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="shell"><div class="tool-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-sand"><div class="shell split top"><div class="rv"><p class="kicker dark">Suggested order</p><h2>Using the calculators together</h2><ol class="steps-list">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Utah Property Owners",
                              "Free claim calculators: gap and fee estimator, RCV to ACV holdback, roof squares, percentage deductible, snow load, timeline planner and more.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload="calculator"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("How appraisal works", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _d) in enumerate(PROCESS_STEPS))
    art = f'<nav class="toc" aria-label="Steps"><b>On this page</b><ol>{toc}</ol></nav>' + PROCESS_BODY
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Utah, Step by Step",
                     "Eight steps from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "documents",
                     [("Steps", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(art, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Utah", "description": "The steps of the appraisal process in a Utah property insurance policy.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Utah | 8 Steps",
                         "A step-by-step guide to insurance appraisal in Utah: the written demand, choosing appraisers and an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], preload="documents"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    jump = "".join(f'<a href="#t-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = f'<div class="jump">{jump}</div>' + "".join(f'<h2 id="t-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Utah Insurance Appraisal FAQ",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, costs and timing, Utah-specific rules and working with us.", "living-room") + layout(groups, call_box() + list_box("Resources", LEARN, path)) + \
        cta_strip("Didn’t see your question?", "Call or email. We’re glad to talk it through.")
    write(path, document(path, "Utah Insurance Appraisal FAQ | Costs, Timing & Rules",
                         "Answers to common Utah insurance appraisal questions, grouped by topic: how it works, costs, timing, Utah rules and when the award is binding.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="g-item"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    art = f'<div class="g-search"><label for="gloss-q">Search {len(GLOSSARY)} terms</label><input id="gloss-q" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="g-count" aria-live="polite"></p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards, defined in plain English and searchable.", "documents", cta=False) + layout(art, call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim terms glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "Searchable plain-English glossary of property insurance claim terms: ACV, RCV, holdback, appraisal award, umpire, snow load, O&P and more.",
                         body, [crumbs_schema(trail), dts], preload="documents"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Articles", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = f'<p class="byline">By the {BRAND} team · Published <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>' + p["body"] + "<h2>Keep reading</h2>" + related([("Article", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Article · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", LEARN) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        post = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), post], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Articles", path)]
    cards = "".join(
        f'<article class="post-card rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2 class="h3"><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS)
    body = page_hero(trail, "Articles", "Utah Insurance Claim Articles and Guides",
                     "Practical reading on policy wording, winter and wildfire claims, earthquake coverage and choosing the right help.", "kitchen", cta=False) + \
        f'<section class="sec"><div class="shell"><div class="post-grid" data-stagger>{cards}</div></div></section>' + cta_strip()
    write(path, document(path, "Utah Insurance Claim Articles & Appraisal Guides",
                         "Articles for Utah property owners on the appraisal clause, snow-load and ice-dam claims, windstorms, earthquake coverage and wildfire smoke.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Company", path)]
    art = f"""
<figure class="lead-fig">{img("meeting-table", sizes="(max-width:1000px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most claim professionals do a little of everything. We chose to focus. {BRAND} works on the amount of loss, the one question an appraisal panel decides, and our inspection routine, estimating standards and calculators are all built around answering it well. That focus lets us serve as your appraiser, review an estimate before a dispute grows, or sit as a neutral umpire for panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before numbers.</strong> We inspect and measure before we read anyone else’s estimate.</li>
<li><strong>Support over size.</strong> An inflated estimate loses an umpire’s trust. We price what we can document.</li>
<li><strong>Plain reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You’ll know the cost before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, cabin owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Utah. On each claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. And we don’t promise outcomes; no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Utah packs a lot of weather into one state: canyon wind on the Wasatch Front, record snow in the mountains, sub-zero cold in Cache Valley, monsoon storms and wildfire in the south, and an active fault under the most populated corridor. Working statewide means we see every kind of loss Utah produces and price each one with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"About {BRAND}", "Estimating and appraisal for Utah property owners who believe a claim should be paid on what the damage actually costs.", "contractor") + \
        layout(art, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Communities", LOC_BASE), ("Calculators", TOOL_BASE), ("How appraisal works", PROCESS)])) + cta_strip()
    write(path, document(path, f"About Us | {BRAND}",
                         "Utah Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed Utah property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="contractor"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "meeting-table", cta=False) + f"""
<section class="sec sec-navy"><div class="shell split contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="c-lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm MT</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>Statewide, all 29 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks-plain"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Send your claim details", page=path, uid="cf")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         f"Request a free review of your disputed Utah property claim. Call or text (844) 537-1427 or email {EMAIL}.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="meeting-table"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, "thumb", sizes="120px", alt="")}</td><td><b>{e(v["title"])}</b><br><small>{e(v.get("creator") or "Unknown")} · {e(v["source_name"])}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    ld = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", f"""
<p><em>Last updated: {ld}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share: your name, phone, email, property location and claim details. Our web host also records standard technical data such as IP address, browser type and pages requested, for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and review your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. What you type isn’t sent to us or stored.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data. If we add analytics through Google Tag Manager, it will be used to understand site traffic in aggregate.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP at any time to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve shared by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us.", "Privacy Policy | Utah Insurance Appraiser"),
        TERMS: ("Terms of Use", f"""
<p><em>Last updated: {ld}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. Its content is general information about insurance appraisal and property claims in Utah.</p>
<h2>No client relationship</h2><p>Reading the site, using a calculator or sending a form doesn’t create an appraiser–client relationship. That begins only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Utah attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from what you enter. Example figures are illustrative. Neither is an appraisal, a quote or a prediction of any claim’s outcome.</p>
<h2>Content and photos</h2><p>Site text, design and calculators belong to {BRAND}. You may link to and print pages for personal use. Photos are used under the licenses listed on the <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Utah.</p>""", "The terms that apply when you use this website and its calculators.", "Terms of Use | Utah Insurance Appraiser"),
        DISC: ("Disclaimers", f"""
<h2>General information</h2><p>This website is educational. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, don’t give legal advice and don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>No reviews, no results claims</h2><p>We don’t publish testimonials or client results. Example figures on this site are illustrative and don’t describe any real claim. No appraiser can guarantee an award.</p>
<h2>Laws and deadlines</h2><p>References to Utah statutes, the Utah Insurance Department and court doctrines are general summaries for context, not legal conclusions. Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits; nothing here extends or changes them. If a deadline is near, contact a Utah attorney promptly.</p>
<h2>Weather and history</h2><p>Descriptions of storms, fires, floods and earthquakes draw on public reports and are included for context.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website.", "Disclaimers | Utah Insurance Appraiser"),
        CREDITS: ("Photo Credits", f"""
<p>Every photo on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site.", "Photo Credits | Utah Insurance Appraiser"),
    }
    for path, (title, content, lede, seo) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "office-tower", cta=False) + layout(content, call_box())
        write(path, document(path, seo, f"{title} for {BRAND} ({HOST}): {lede}"[:150].rstrip(), body, [crumbs_schema(trail)], preload="office-tower"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Communities", [("All communities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimers", DISC), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2 class="h3">{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "office-tower", cta=False) + f'<section class="sec"><div class="shell map-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Utah communities, free claim calculators, articles and legal pages.", body, [crumbs_schema(trail)], preload="office-tower"), 0.3)

    body = f"""<section class="sub-hero nf"><div class="sub-hero-bg">{img("storm-sky", lazy=False, alt="")}</div><div class="shell sub-hero-in"><p class="kicker">Error 404</p><h1>This page isn’t on the map</h1><p class="lede">It may have moved or never existed. Try one of these instead.</p><div class="row-btns"><a class="btn btn-accent" href="/">Home</a><a class="btn btn-ghost-l" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn btn-ghost-l" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow"), sitemap=False)


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
// Utah Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$uia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$uia_real  = 'utahinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$uia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://utahinsuranceappraiser.com - only on the real domain.
if ($uia_host === 'www.' . $uia_real || ($uia_host === $uia_real && $uia_proto === 'http')) {
    header('Location: https://' . $uia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$uia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($uia_uri, '?'), $uia_m)) {
    $uia_q = strpos($uia_uri, '?') !== false ? substr($uia_uri, strpos($uia_uri, '?')) : '';
    header('Location: ' . $uia_m[1] . $uia_q, true, 301);
    exit;
}
// Keep the temporary preview domain (and any other host) out of search results.
if ($uia_host !== $uia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Utah Insurance Appraiser - front controller for the static build.
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
