#!/usr/bin/env python3
"""Static site generator for newyorkinsuranceappraiser.com.

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

BRAND = "New York Insurance Appraiser"
HOST = "newyorkinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112a"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no tag output.
GTM_ID = ""

SVC_BASE = "/claim-appraisals/"
LOC_BASE = "/where-we-appraise/"
TOOL_BASE = "/appraisal-calculators/"
POST_BASE = "/policyholder-guides/"
P_PROCESS = "/appraisal-walkthrough/"
P_FAQ = "/ask-an-appraiser/"
P_GLOSS = "/claim-vocabulary/"
P_ABOUT = "/our-practice/"
P_CONTACT = "/reach-us/"
P_PRIV, P_TERMS, P_DISC, P_CRED, P_MAP = "/privacy-practices/", "/site-terms/", "/professional-disclaimer/", "/photo-credits/", "/site-directory/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, NY"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
from photomap import ALT, SVC_PHOTO, LOC_PHOTO, TOOL_PHOTO, POST_PHOTO  # noqa: E402


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
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
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=40):
    # Brand mark: blue tile, white roofline over an orange "fair value" bar.
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="9" fill="#1550a8"/>'
            '<path d="M10 25 24 12l14 13" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="14" y="29" width="20" height="4.6" rx="2.3" fill="#f26a1b"/>'
            '<rect x="14" y="36" width="20" height="4.6" rx="2.3" fill="#fff"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>New York</b><span>Insurance Appraiser</span></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "NY", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NY", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for disputed New York property claims",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across New York State.",
        "areaServed": [{"@type": "State", "name": "New York"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Ice dam claims", "Hurricane deductibles", "Co-op and condo claims"],
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
LEARN = [("Appraisal walkthrough", P_PROCESS), ("Ask an appraiser (FAQ)", P_FAQ), ("Claim vocabulary", P_GLOSS), ("Policyholder guides", POST_BASE)]


def _groups():
    return [
        ("Appraisals", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("Every appraisal service", SVC_BASE)),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All of New York State", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="dropdown{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">Our practice</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-head">
<div class="util"><div class="wrap"><span class="util-l">Independent property claim appraisal · all 62 New York counties</span><span class="util-r"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{ic("phone")}{PHONE}</a></span></div></div>
<div class="bar"><div class="wrap">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-orange head-cta" href="{P_CONTACT}">Free claim review</a>
<a class="nojs-menu" href="{P_MAP}">Menu</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div></div>
</header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-drawer")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{P_ABOUT}">Our practice</a></li><li><a href="{P_CONTACT}">Reach us</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-orange" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap"><h2>Carrier’s number doesn’t cover the repair?</h2><div class="btn-row"><a class="btn btn-orange" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-l" href="{P_CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-foot")}
<p>Independent appraisal and estimating for owners of disputed property claims, from Montauk to Niagara Falls.</p>
<p class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>Mon–Fri 8am–6pm ET</p></div>
<div><h3>Appraisals</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Locations</h3><ul class="two">{loc}</ul></div>
<div><h3>Calculators</h3><ul>{tl}</ul></div>
<div><h3>Practice</h3><ul><li><a href="{P_ABOUT}">Our practice</a></li><li><a href="{P_CONTACT}">Reach us</a></li><li><a href="{P_PROCESS}">Appraisal walkthrough</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Claim vocabulary</a></li><li><a href="{POST_BASE}">Guides</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. {BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content is general information; your policy controls. Outcomes are never guaranteed.</p>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_CRED}">Photo credits</a></li><li><a href="{P_MAP}">Site directory</a></li></ul></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<nav class="callbar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")} Call</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></nav>"""


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


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, body_cls=""):
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across New York State">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across New York State">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="New York">
<meta name="theme-color" content="#0a1a3a">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
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
    c = f'<div class="btn-row"><a class="btn btn-orange" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero">{img(photo, "phero-bg", lazy=False, alt="")}<div class="phero-shade"></div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><p class="side-t">Talk it through</p><p>A first conversation is free. We’ll tell you honestly whether appraisal fits your claim.</p><a class="side-tel" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-orange btn-block" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<nav class="side-box side-links" aria-label="{e(title)}"><p class="side-t">{e(title)}</p><ul>{li}</ul></nav>'


def aside(*boxes):
    return f'<aside class="side"><div class="side-sticky">{call_box()}{"".join(boxes)}</div></aside>'


def related_cards(items):
    return '<div class="rel-grid">' + "".join(f'<a class="rel" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


def cta_strip(h="Covered, but not paid in full?", p="Send us the carrier’s estimate and your photos. We’ll read it line by line and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-orange" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-l" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


LOSSES = ["Snow / ice dam", "Water / burst pipe", "Wind / tree", "Hurricane / nor’easter", "Hail / roof", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hid="f"):
    roles = ["Homeowner", "Co-op / condo owner", "Board or managing agent", "Commercial owner", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in New York"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h3 class="lead-t">{e(heading)}</h3><p class="lead-sub">Free review, no obligation. Most replies within one business day.</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{hid}-amt">Amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think is missing."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy practices</a>.</span></label></div>
<div class="full"><button class="btn btn-blue btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="hf-t">Free claim review</p><p class="lead-sub">Three fields. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{P_PRIV}">Privacy</a>.</span></label>
<button class="btn btn-orange btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hf-trust">{ic("lock")} Private. No obligation. No spam.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("nyc", "New York City", "Five boroughs", "manhattan", ["Unit-to-unit water", "Fire & smoke migration", "Flash flooding", "Wind-driven rain"],
     "Co-ops, condos, brownstones and attached brick homes put two or three policies on every loss. A burst riser in a pre-war co-op or a fire next door in a Brooklyn row means sorting the board’s master policy from your own before anyone can price the damage.",
     ["manhattan", "brooklyn", "queens", "staten-island"]),
    ("li", "Long Island", "Nassau & Suffolk", "long-island", ["Hurricane deductibles", "Nor’easters", "Tree fall", "Wind vs. surge"],
     "South Shore communities still measure storms against Sandy. Percentage hurricane deductibles, wind-versus-flood questions and big oaks over capes and high-ranches drive most of the disputes we see east of the city line.",
     ["hempstead", "islip"]),
    ("hudson", "Hudson Valley & Westchester", "From Yonkers to Kingston", "westchester", ["Severe thunderstorms", "Falling trees", "Hail", "Basement water"],
     "Leafy suburbs mean limbs on roofs. Summer squall lines, the occasional tornado and cloudburst flooding like the remnants of Ida leave older colonials and Tudors with layered roofs, finished basements and complicated scopes.",
     ["white-plains"]),
    ("capital", "Capital Region & North Country", "Albany to the St. Lawrence", "albany", ["Ice dams", "Ice storms", "Frozen pipes", "Hail"],
     "Freeze–thaw cycles do quiet, expensive damage to Albany brick rowhouses and Adirondack camps alike. Ice dams, burst pipes in vacant seasonal homes and ice-loaded trees are the claims winter leaves behind.",
     ["albany"]),
    ("central", "Central NY & Finger Lakes", "Syracuse · Rochester", "syracuse", ["Lake-effect snow load", "Derecho winds", "Ice dams", "Hail"],
     "Some of the snowiest large cities in the country sit along the Thruway. Heavy, wet lake-effect loads stress older wood-frame roofs, and summer derechos like the 1998 Labor Day storm show how fast wind claims pile up.",
     ["syracuse", "rochester"]),
    ("west", "Western NY & Southern Tier", "Buffalo · Binghamton", "buffalo", ["Blizzards", "Roof collapse", "River-valley water", "Wind"],
     "Buffalo doubles under multi-foot lake-effect snow and Southern Tier homes along the Susquehanna share one thing: losses where cause matters. Separating covered snow, ice and wind damage from excluded flooding is often the whole dispute.",
     ["buffalo", "binghamton"]),
]

STORMS = [
    ("1938", "Long Island Express", "Long Island", "The hurricane that reshaped the South Shore and still anchors how coastal wind risk is priced."),
    ("1998", "Labor Day derecho", "Central NY", "Straight-line winds across Syracuse showed that inland wind claims can rival a coastal storm."),
    ("2011", "Irene & Lee", "Catskills · Southern Tier", "Back-to-back storms flooded the Schoharie Valley and Binghamton, and tested the line between flood and covered water."),
    ("2012", "Superstorm Sandy", "NYC · Long Island", "Surge, wind and the Breezy Point fire in one event made cause-of-loss the central claim question."),
    ("2014", "“Snowvember”", "Buffalo area", "Several feet of lake-effect snow in days brought roof collapses, ice dams and interior water claims."),
    ("2021", "Remnants of Ida", "Queens · Westchester", "Record cloudburst rainfall flooded basements, raising sewer-backup and surface-water coverage questions."),
    ("2022", "Buffalo blizzard", "Western NY", "Hurricane-force gusts and whiteout snow left frozen pipes, wind damage and long-delayed inspections."),
]


def home():
    K = BRAND
    marq = ["Manhattan", "Brooklyn", "Queens", "Staten Island", "The Bronx", "Long Island", "Westchester", "Hudson Valley", "Albany", "Syracuse", "Rochester", "Buffalo", "Binghamton", "North Country", "Finger Lakes"]
    marquee = "".join(f"<span>{p}</span>" for p in marq * 2)

    who = [
        ("Homeowners", "Houses, two-families and attached homes with a short or stalled claim.", "homeowners-insurance-appraisal", "who-home"),
        ("Co-op & condo boards", "Master-policy losses, unit-to-unit leaks and board-managed buildings.", "co-op-condo-commercial-appraisal", "apartment"),
        ("Business owners", "Storefronts, offices, mixed-use and multifamily property claims.", "co-op-condo-commercial-appraisal", "commercial"),
        ("Attorneys & adjusters", "Independent valuation, estimate review and umpire appointments.", "appraisal-umpire-services", "consult"),
    ]
    who_html = "".join(f'<a class="who rv" href="{SVC_BASE}{s}/"><span class="who-ph">{img(ph, sizes="(max-width:700px) 100vw, 25vw", alt="")}</span><span class="who-b"><b>{e(t)}</b><span>{e(d)}</span><em>See how we help {ic("arrow")}</em></span></a>' for t, d, s, ph in who)

    stations = "".join(f'<li class="rv"><a href="{SVC_BASE}{s["slug"]}/"><span class="dot">{i + 1}</span><span class="st-b"><b>{e(s["name"])}</b><span>{e(s["short"])}</span></span>{ic("arrow")}</a></li>' for i, s in enumerate(SERVICES))

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{e(n)}</b><small>{e(sub)}</small></button>'
        for i, (k, n, sub, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="rpanel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}><div class="rpanel-ph">{img(ph, sizes="(max-width:900px) 100vw, 560px", alt="")}</div><div class="rpanel-b"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p><p class="rp-links">{" ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]['city'])}</a>" for c in cities)}</p></div></div>'
        for i, (k, n, sub, ph, perils, t, cities) in enumerate(REGIONS))

    storms = "".join(f'<li class="storm rv"><span class="yr">{y}</span><b>{e(n)}</b><small>{e(r)}</small><p>{e(t)}</p></li>' for y, n, r, t in STORMS)

    line = [("Call", "Free first conversation about the policy, the estimate and the gap."), ("Re-scope", "Our own inspection, measurements and photos of the loss."),
            ("Value", "Line-item estimate priced for your New York ZIP code."), ("Demand", "Appraisal invoked in writing; we’re named as your appraiser."),
            ("Panel", "Line-by-line work with the carrier’s appraiser."), ("Award", "Two of three signatures set the amount of loss.")]
    line_html = "".join(f'<li class="rv"><span class="stop"></span><b>{e(t)}</b><span>{e(d)}</span></li>' for t, d in line)

    tools = "".join(f'<a class="card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="badge">{e(t["kind"])}</span></span><span class="card-b"><b>{e(t["name"])}</b><span>{e(t["short"])}</span></span></a>' for t in TOOLS)
    locs = "".join(f'<a class="loc rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="loc-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    posts = "".join(f'<a class="card post rv" href="{POST_BASE}{p["slug"]}/"><span class="card-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="card-b"><small>{p["read"]} read</small><b>{e(p["title"])}</b><span>{e(p["summary"])}</span></span></a>' for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do?", f"A {K} values a property loss when you and your insurer agree the damage is covered but disagree on what it costs. Once appraisal is invoked we act as your appointed appraiser: inspect, build an independent estimate, work with the carrier’s appraiser and, if needed, present open items to the umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster, licensed by the Department of Financial Services, manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t handle coverage disputes or give legal advice."),
        (f"When is it worth calling a {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap to a credible repair estimate is meaningful. Small gaps are often closed faster with a documented supplement request."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That’s why documentation matters before you invoke appraisal."),
        ("What does appraisal cost?", "Each side usually pays its own appraiser and splits the umpire. Our fee is agreed in writing before any work starts, and the first conversation is free."),
        (f"Does {K} cover upstate as well as the city?", "Yes. We work across all 62 counties, from the five boroughs and Long Island to the Capital Region, Central New York, the Finger Lakes, Western New York and the Southern Tier."),
    ]

    body = f"""
<section class="hero">
<div class="hero-ph">{img("hero", lazy=False, alt="")}</div><div class="hero-shade"></div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-l">Independent appraisal · Statewide</p>
<h1>{K}: <span>a second, independent number</span> for your property claim</h1>
<p class="lede">When the carrier accepts your claim but its estimate won’t pay for the repair, {K} re-scopes the loss from the ground up and takes the difference through the appraisal clause in your policy.</p>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Homes, co-ops, condos &amp; commercial</li><li>{ic("check")}All 62 counties</li></ul>
<div class="btn-row"><a class="btn btn-orange" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="#line">How it works</a></div>
</div>
{hero_form()}
</div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{marquee}</div></div>

<section class="sec intro"><div class="wrap intro-grid">
<div class="rv">
<p class="kicker">Covered isn’t the same as paid</p>
<h2>Why owners call a {K} instead of arguing alone</h2>
<p>Most short claims aren’t denials. They’re estimates with a slope missing, a ceiling priced as patch-and-paint, a co-op wall assigned to the wrong policy, or an ice-dam leak written up as “maintenance.” {K} works the space between “we’ll cover it” and a check that actually rebuilds.</p>
<p>We start from our own inspection, never an edited copy of the carrier’s file, and we price what we can defend in front of an umpire. If your problem is a denial or a deadline, we’ll say so on the first call and point you to the right professional.</p>
<a class="btn btn-blue" href="{P_ABOUT}">How our practice works {ic("arrow")}</a>
</div>
<div class="tally" aria-label="At a glance">
<div class="rv"><b data-count="62">62</b><span>New York counties covered</span></div>
<div class="rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
<div class="rv"><b>2<small>of</small>3</b><span>Signatures that make an award binding</span></div>
</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Start with your situation</p><h2>Who {K} works for</h2><p>The appraisal clause reads the same for everyone, but a Park Slope brownstone, a Midtown co-op and a Rochester strip mall raise very different questions.</p></div>
<div class="who-grid">{who_html}</div>
</div></section>

<section class="sec" id="services"><div class="wrap line-split">
<div class="line-intro rv">
<p class="kicker">Appraisal &amp; estimating</p>
<h2>Eleven services from one {K}</h2>
<p>Every stop on this line leads to the same destination: a valuation of your loss that holds up. Some clients need the whole route; many only need an estimate review.</p>
<figure>{img("roofer", sizes="(max-width:900px) 100vw, 420px")}</figure>
<a class="btn btn-blue" href="{SVC_BASE}">Compare all services {ic("arrow")}</a>
</div>
<ol class="stations">{stations}</ol>
</div></section>

<section class="sec navy"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-l">Regional knowledge</p><h2>From the boroughs to the Great Lakes: six claim climates</h2><p>A {K} has to know how a Sandy-era South Shore roof, a Syracuse snow load and a Bronx riser leak each show up in an estimate.</p></div>
<div class="regions rv" data-regions><div class="rtabs" role="tablist" aria-label="New York regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec storms-sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Storm record</p><h2>Storms that still shape New York claims</h2><p>Each of these events left a lesson about how damage gets scoped, priced and argued. A {K} reads every new claim with them in mind.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec tint" id="check"><div class="wrap check-grid">
<div class="rv">
<p class="kicker">Before you demand appraisal</p>
<h2>Three questions a {K} asks first</h2>
<ol class="path">
<li><b>Has the carrier accepted coverage?</b><span>Appraisal values a covered loss. A denial is a coverage fight, and that usually means a New York attorney.</span></li>
<li><b>Is the gap worth the cost?</b><span>Each side pays its own appraiser and shares the umpire. Run the numbers in the box.</span></li>
<li><b>Can you document it?</b><span>Photos, measurements and a credible line-item estimate move awards. Opinions don’t.</span></li>
</ol>
<p>Want fees included? Try the <a href="{TOOL_BASE}settlement-gap-fee-estimator/">settlement gap &amp; fee estimator</a>.</p>
</div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec" id="line"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The route</p><h2>How {K} moves a stalled claim</h2><p>Six stops from the first call to a signed award. Most panels resolve the bulk of the dispute between stops four and five.</p></div>
<ol class="route" data-stagger>{line_html}</ol>
<p class="center"><a class="more" href="{P_PROCESS}">Read the full appraisal walkthrough {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Claim calculators from a {K}</h2><p>Check the carrier’s math before you pick up the phone. Each calculator runs in your browser and nothing you type is stored or sent.</p></div>
<div class="card-grid four" data-stagger>{tools}</div>
<p class="center"><a class="more" href="{TOOL_BASE}">See all {len(TOOLS)} calculators {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">On-site statewide</p><h2>Where {K} inspects most often</h2><p>We cover every county. These are the communities that call us most, each with its own housing stock and storm history.</p></div>
<div class="loc-grid" data-stagger>{locs}</div>
<p class="center"><a class="more" href="{LOC_BASE}">All New York locations {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap faq-split">
<div class="rv"><p class="kicker">Questions</p><h2>Ask a {K}</h2><p>Plain answers about the process, the cost and when appraisal is the wrong move.</p><figure class="faq-ph">{img("consult2", sizes="(max-width:900px) 100vw, 420px")}</figure><div class="btn-row"><a class="btn btn-blue" href="{P_FAQ}">Every FAQ {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim vocabulary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Policyholder guides</p><h2>Read this before you sign a proof of loss</h2><p>Guides from {K} on New York policy language, documentation and claim strategy.</p></div>
<div class="card-grid three" data-stagger>{posts}</div>
<p class="center"><a class="more" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="sec navy" id="contact"><div class="wrap contact-grid">
<div class="rv">
<p class="kicker kicker-l">Start with a conversation</p>
<h2>Talk to a {K} about your claim</h2>
<p>Tell us what happened and what the carrier offered. You’ll get a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Coverage</small>All 62 New York counties</span></li></ul>
</div>
<div class="rv">{lead_form(page="/", hid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "New York Insurance Appraiser: independent appraisal, estimate review and umpire services for disputed snow, water, wind, hurricane and fire claims.",
                        body, [faq_schema(home_faqs)], preload="hero", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Appraisals", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = related_cards([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[idx % 6: idx % 6 + 6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related}
</article>
{aside(list_box("Appraisal services", items, path), list_box("Where we inspect", locs + [("All New York locations", LOC_BASE)]))}</div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "New York"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Appraisals", SVC_BASE)]
    cards = "".join(f'<a class="card wide-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="badge">{i + 1:02d}</span></span><span class="card-b"><b>{e(s["name"])}</b><span>{e(s["short"])}</span><em>Details {ic("arrow")}</em></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services Across New York",
                     "From a one-time estimate review to full panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of the loss.", "roofer") + f"""
<section class="sec"><div class="wrap"><div class="card-grid three" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that difference is worth. A review answers that in days, and many disputes close at that stage with a documented supplement.</p><a class="btn btn-blue" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal."), ("Do you work on co-op and condo buildings?", "Yes. We work for unit owners and for boards and managing agents, and we sort out which policy responds to which part of the loss."), ("Do you handle flood claims?", "Flood is excluded from standard homeowners policies. We can review flood estimates, but appraisal under a flood policy follows that policy’s own, narrower rules.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in New York | 11 Services",
                             "Insurance appraisal services across New York: appraisal clause representation, estimate review, snow, water, wind, fire and co-op claims, and umpires.",
                             body, schema, preload="roofer"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = related_cards([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(l["neighborhoods"])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, New York", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local-card"><div><p class="lc-t">Local claim risks</p><ul class="chips">{chips}</ul></div><div><p class="lc-t">Housing mix</p><p>{e(l["housing"])}</p></div><div><p class="lc-t">Areas we visit</p><p>{e(hoods)}</p></div></div>
{l["body"]}
<h2>Appraisal services for {e(l["city"])} properties</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and across {e(l["county"])}, including:</p>
<ul class="cols">{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby locations</h2>{near}
</article>
{aside(list_box("New York locations", items, path), list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see and whether appraisal makes sense.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, NY", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"], "containedInPlace": {"@type": "State", "name": "New York"}}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    locs = "".join(f'<a class="loc rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="loc-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="reg-row rv"><span class="reg-ph">{img(ph, sizes="(max-width:700px) 100vw, 280px", alt="")}</span><div><h3>{e(n)}</h3><p class="muted">{e(sub)}</p><p>{e(t)}</p><p class="rp-links">{" ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]['city'])}</a>" for c in cities)}</p></div></div>' for k, n, sub, ph, _p, t, cities in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 62 New York Counties",
                     "From the five boroughs to Chautauqua County, we inspect on site. These pages cover the communities where we’re called most often.", "manhattan") + f"""
<section class="sec"><div class="wrap"><div class="loc-grid" data-stagger>{locs}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">Regions</p><h2>How claims change across the state</h2><p>The same policy language plays out very differently in a Tribeca loft, a Levittown cape and a Buffalo double.</p></div><div class="reg-list">{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every county in New York. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "New York Insurance Appraisal Locations | All 62 Counties",
                             "Insurance appraisal across New York: Manhattan, Brooklyn, Queens, Staten Island, Long Island, Westchester, Albany, Syracuse, Rochester and Buffalo.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload="manhattan"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = related_cards([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and nothing you enter leaves your browser.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2>{others}</article>
{aside(list_box("All calculators", items, path))}</div>
{cta_strip("Want a professional to check the numbers?", "Send us the carrier’s estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(f'<a class="card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="badge">{e(t["kind"])}</span></span><span class="card-b"><b>{e(t["name"])}</b><span>{e(t["short"])}</span><em>Open {ic("arrow")}</em></span></a>' for t in TOOLS)
    order = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(n)}</a>: {e(w)}</li>' for s, n, w in [
        ("claim-calendar-builder", "Claim calendar builder", "put every policy deadline on your calendar first."),
        ("roof-area-pitch-estimator", "Roof area & pitch estimator", "check the squares and steep charges on the roof line."),
        ("acv-rcv-holdback-calculator", "ACV/RCV holdback calculator", "see what the first check should be and what’s held back."),
        ("hurricane-deductible-calculator", "Hurricane deductible calculator", "learn what a percentage deductible really costs."),
        ("co-op-condo-claim-splitter", "Co-op & condo claim splitter", "split a unit loss between the building and your HO-6."),
        ("settlement-gap-fee-estimator", "Settlement gap & fee estimator", "test whether appraisal pays after fees."),
        ("appraisal-readiness-checkup", "Appraisal readiness checkup", "make sure your file is ready before you demand appraisal.")])
    body = page_hero(trail, "Free & private", "Free Property Claim Calculators for New York Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Use them to check the carrier’s math and plan next steps. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="card-grid three" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="steps-list">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for New York Owners",
                              "Free claim calculators: settlement gap and fees, ACV/RCV holdback, roof pitch, hurricane deductibles, a claim calendar and a co-op/condo splitter.",
                              body, schema, preload="calculator"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal walkthrough", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in New York, Step by Step",
                     f"{len(PROCESS_STEPS)} steps from the first disagreement to a signed award: what happens, who does what, and where files most often go wrong.", "clipboard",
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
{aside(list_box("Resources", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in New York", "description": "The steps of a property insurance appraisal under a New York policy, from the written demand to the binding award.", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, n in enumerate(PROCESS_STEPS)]}
    pb = PROCESS_BODY
    for i, n in enumerate(PROCESS_STEPS):
        pb = pb.replace(f"<h2>Step {i + 1}: ", f'<h2 id="step-{i + 1}">Step {i + 1}: ', 1)
    body = body.replace(PROCESS_BODY, pb)
    write(path, document(path, "How Insurance Appraisal Works in New York | Walkthrough",
                         "A step-by-step walkthrough of New York insurance appraisal: the written demand, appraisers, the umpire, line-by-line negotiation and the award.",
                         body, [crumbs_schema(trail), howto], preload="clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Ask an appraiser", path)]
    jump = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions from New York Owners",
                     "Plain answers to what we hear most about the appraisal process, costs, deadlines and New York’s rules.", "livingroom") + f"""
<div class="wrap layout"><article class="prose"><nav class="jump" aria-label="FAQ topics">{jump}</nav>{groups}</article>
{aside(list_box("Resources", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ for New York | Costs & Rules",
                         "Answers to common New York insurance appraisal questions, grouped by topic: basics, costs, deadlines, state rules and agencies, and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="livingroom"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim vocabulary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gterm"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Property Claim Vocabulary: Terms Defined",
                     f"{len(GLOSSARY)} terms you’ll meet in New York policies, estimates and appraisal awards, defined in plain English.", "laptop", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="gfilter"><label for="gloss-filter">Search the vocabulary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"><p class="gcount" aria-live="polite"><span data-gcount>{len(GLOSSARY)}</span> terms shown</p></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl></article>
{aside(list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim vocabulary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path + "#definedtermset"} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Vocabulary | ACV, Umpire, Ice Dam & More",
                         "Searchable plain-English definitions of property claim terms: actual cash value, appraisal award, hurricane deductible, ice dam, umpire and more.",
                         body, [crumbs_schema(trail), dts], preload="laptop"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = related_cards([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{others}</article>
{aside(list_box("Resources", LEARN), list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"][:110], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p.get("kw", "")}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(f'<a class="card post rv" href="{POST_BASE}{p["slug"]}/"><span class="card-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="card-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><b>{e(p["title"])}</b><span>{e(p["summary"])}</span><em>Read the guide {ic("arrow")}</em></span></a>' for p in POSTS)
    body = page_hero(trail, "Policyholder guides", "Guides for New York Policyholders With a Disputed Claim",
                     "Practical reading on policy language, documentation and claim strategy, written from the appraisal side of the table.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="card-grid three" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Claim Guides for New York Policyholders",
                         "Guides for New York owners: the standard fire policy appraisal clause, hurricane deductibles, ice dams, co-op claims, basement water and who to hire.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("Our practice", path)]
    body = page_hero(trail, "Our practice", "About Our New York Appraisal Practice",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "consult") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("office", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>Most claim professionals do a little of everything. {BRAND} works on one question, the amount of loss, and builds every process, calculator and report around answering it well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>Principles we work by</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we read anyone else’s numbers.</li>
<li><strong>Defensible beats dramatic.</strong> An inflated estimate looks good on day one and loses credibility with the umpire on day thirty. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If the claim needs a New York attorney or a licensed public adjuster instead, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who calls us</h2>
<p>Homeowners and two-family owners, co-op shareholders and condo unit owners, boards and managing agents, landlords, business owners, houses of worship, contractors, public adjusters and attorneys. On any one claim we serve in a single role, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t decide coverage, and we don’t guarantee results. No honest appraiser can.</p>
<h2>Why statewide</h2>
<p>New York’s claim climates range from Atlantic surge on the South Shore to lake-effect snow loads in Oswego County. Working across all 62 counties means we see every kind of loss the state produces and price each one with local knowledge of materials, labor and building codes.</p>
</article>{aside(list_box("Explore", [("Appraisal services", SVC_BASE), ("Locations", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal walkthrough", P_PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, f"Our Practice | {BRAND}",
                         "New York Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="consult"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Reach us", path)]
    body = page_hero(trail, "Reach us", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult2", cta=False) + f"""
<section class="sec"><div class="wrap contact-grid light">
<div class="rv"><h2>Direct lines</h2>
<ul class="lines dark-t"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Service area</small>All 62 New York counties</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimate</li><li>For co-ops and condos: the proprietary lease or bylaws section on repairs</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         f"Get a free review of a disputed New York property claim. Call or text (844) 537-1427 or email {EMAIL}.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="consult2"), 0.8)

    def lic(v):
        return "CC0 1.0" if v["license"] == "cc0" else "Public domain"
    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{lic(v)}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Practices", "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Information you give us</h2><p>When you submit a form, call or email, we collect what you choose to share, such as your name, phone number, email address, property location and details about your claim. Our host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, it will be described here.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        P_TERMS: ("Site Terms", "The terms that apply when you use this website and its calculators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in New York.</p>
<h2>No client relationship</h2><p>Reading this site, using its calculators or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a New York attorney with legal questions.</p>
<h2>Calculators</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on the <a href="{P_CRED}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of New York.</p>"""),
        P_DISC: ("Professional Disclaimer", "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys and don’t give legal advice. We don’t act as public adjusters, who are licensed separately by the New York State Department of Financial Services, and we don’t negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is approaching, consult a New York attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to statutes, regulations, agencies and storms are for context. Verify current law and facts with official sources such as the New York State Department of Financial Services.</p>"""),
        P_CRED: ("Photo Credits", "Sources and licenses for every photograph used on this site.", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos made by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (title, lede, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "office", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article>{aside()}</div>'
        desc = f"{title} for {BRAND} ({HOST}). {lede}"
        if len(desc) < 110:
            desc = f"{title} for the {BRAND} website at {HOST}. {lede}"
        write(path, document(path, f"{title} | {BRAND}", desc[:150], body, [crumbs_schema(trail)], preload="office"), 0.3)


def directory_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site directory", path)]
    groups = [
        ("Main", [("Home", "/"), ("Our practice", P_ABOUT), ("Reach us", P_CONTACT)]),
        ("Appraisal services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy practices", P_PRIV), ("Site terms", P_TERMS), ("Professional disclaimer", P_DISC), ("Photo credits", P_CRED)]),
    ]
    cols = "".join(f'<div class="dir-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Directory", f"Every page on the {BRAND} website, in one place.", "office", cta=False) + f'<section class="sec"><div class="wrap dir-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Directory | {BRAND}", f"A complete directory of every page on {BRAND}: appraisal services, New York locations, free calculators and guides.", body, [crumbs_schema(trail)], preload="office"), 0.3)

    body = f"""<section class="phero err">{img("storm", "phero-bg", lazy=False, alt="")}<div class="phero-shade"></div><div class="wrap phero-in"><p class="kicker kicker-l">Error 404</p><h1>That page isn’t on this line</h1><p class="lede">The page may have moved or never existed. Try one of these stops instead.</p><div class="btn-row"><a class="btn btn-orange" href="/">Home</a><a class="btn btn-ghost-l" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn btn-ghost-l" href="{P_MAP}">Site directory</a></div></div></section>"""
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
// New York Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nyia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nyia_real  = 'newyorkinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nyia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://newyorkinsuranceappraiser.com - only on the real domain.
if ($nyia_host === 'www.' . $nyia_real || ($nyia_host === $nyia_real && $nyia_proto === 'http')) {
    header('Location: https://' . $nyia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $nyia_m)) {
    $nyia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $nyia_m[1] . $nyia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($nyia_host !== $nyia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// New York Insurance Appraiser - front controller for the static build.
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
    directory_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
