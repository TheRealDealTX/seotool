#!/usr/bin/env python3
"""Static site generator for virginiainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.

Hosting model (Hostinger Agency, php-fpm): the host serves real files directly, so every page except
the homepage is written as dir/index.php whose first line requires _guard.php (canonical host, noindex
off-domain). The homepage is home.html, served by the root index.php front controller.
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
from learn import PROCESS_BODY, STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))

BRAND = "Virginia Insurance Appraiser"
HOST = "virginiainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster

# Google Tag Manager: leave empty until a container ID is provided (e.g. "GTM-XXXXXXX").
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraisal-and-umpire-services/"
LOC_BASE = "/virginia-localities/"
TOOL_BASE = "/calculators-for-policyholders/"
POST_BASE = "/policy-and-claim-guides/"
PROCESS = "/virginia-appraisal-steps/"
FAQ_P = "/virginia-appraisal-questions/"
GLOSS = "/claim-and-policy-terms/"
ABOUT = "/about-our-appraisers/"
CONTACT = "/schedule-a-claim-review/"
PRIVACY = "/how-we-handle-data/"
TERMS = "/website-terms-of-use/"
DISC = "/disclaimer-and-notices/"
SMAP = "/site-contents/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}insurance-appraiser-{l['slug']}-va/"


def loc_label(l):
    return l["city"] if l["kind"] == "County" else f"{l['city']}, VA"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
SVC_PHOTO = {
    "appraisal-demand-representation": "consult-table", "homeowners-insurance-appraisal": "fairfax-suburb",
    "commercial-and-hoa-claim-appraisal": "condo-building", "hail-and-roof-damage-appraisal": "hail-shingles",
    "windstorm-and-tornado-appraisal": "storm-roof-damage", "hurricane-and-noreaster-appraisal": "hurricane-flooding",
    "water-damage-claim-appraisal": "water-ceiling", "fire-and-smoke-damage-appraisal": "fire-damage",
    "tree-fall-and-ice-storm-appraisal": "tree-on-house", "historic-home-claim-appraisal": "historic-interior",
    "carrier-estimate-review": "laptop-estimate", "umpire-selection-and-services": "calculator-papers",
}


def alt_of(key):
    return PHOTOS[key].get("desc") or PHOTOS[key].get("title", "")


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else alt_of(key))
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
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "landmark": '<path d="M3 21h18M5 21V10M9.5 21V10M14.5 21V10M19 21V10M2 10l10-6 10 6z"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
}


def ic(name, cls="i"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=44):
    """Brand mark: navy tile, white roof line over a brick-orange 'ledger' bar."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#00297B"/>'
            '<path d="M10.5 24.5 24 12.5l13.5 12" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15.5 21.5V35h17V21.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>'
            '<rect x="12" y="37" width="24" height="3.6" rx="1.8" fill="#F08A4B"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="bt"><b>{BRAND}</b><small>Independent claim appraisal · VA</small></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    areas = [{"@type": "State", "name": "Virginia"}]
    for l in LOCATIONS:
        areas.append({"@type": "AdministrativeArea" if l["kind"] == "County" else "City", "name": l["city"] + (", Virginia")})
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/web-app-manifest-512x512.png", "contentUrl": DOMAIN + "/web-app-manifest-512x512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "VA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-VA", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across the Commonwealth of Virginia.",
        "areaServed": areas,
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hurricane claims", "Hail damage", "Fallen tree claims"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services in Virginia", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
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


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
RES_LINKS = [("How appraisal works", PROCESS), ("Appraisal FAQ", FAQ_P), ("Claim & policy terms", GLOSS), ("Claim guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE), "cols"),
        ("Localities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Virginia localities", LOC_BASE), "cols"),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All calculators", TOOL_BASE), ""),
        ("Resources", RES_LINKS + [("About us", ABOUT)], None, ""),
    ]


def header():
    menu = ""
    for i, (name, links, allk, cols) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li class="has-drop"><button type="button" class="drop-btn" aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop {cols}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="nav-link" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="strong" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}" hidden><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="head" id="top"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-accent head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-shade" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{CONTACT}">Contact</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    res = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in RES_LINKS + [("About us", ABOUT), ("Contact", CONTACT)])
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Short check, long repair? Let’s compare the numbers.</h2><div class="btn-row"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Send claim details</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-foot")}
<p>Independent appraisal, estimate review and umpire services for disputed property claims, from the Eastern Shore to the Cumberland Gap.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("clock")}Mon–Fri 8am–6pm ET</li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All 12 services</a></li></ul></div>
<div class="foot-locs"><h2 class="foot-h">Localities</h2><ul class="two">{loc}</ul><p class="foot-more"><a href="{LOC_BASE}">All Virginia localities</a></p></div>
<div><h2 class="foot-h">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Resources</h2><ul>{res}</ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms of use</a></li><li><a href="{DISC}">Disclaimer</a></li><li><a href="{SMAP}">Site contents</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and are not public adjusters. Information on this site is general and educational; policy terms vary. Example figures are illustrative, and no result is guaranteed.</p>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("doc")} Free review</a></div>"""


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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema, trail, photo, og_type="website", robots="index,follow"):
    canonical = DOMAIN + path
    page_type, nodes = "WebPage", []
    main_pref = None
    for n in schema:
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        nodes.append(n)
    crumbs = crumbs_schema(trail)
    crumbs["@id"] = canonical + "#breadcrumb"
    nodes.append(crumbs)
    pimg = PHOTOS[photo]
    img_node = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": alt_of(photo)}
    for t in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
        hit = [n for n in nodes if n.get("@type") == t]
        if hit:
            main_pref = hit[0]["@id"]
            break
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": crumbs["@id"]}, "primaryImageOfPage": {"@id": img_node["@id"]},
        "mainEntity": {"@id": main_pref or DOMAIN + "/#business"},
    }
    graph = [org_schema(), site_schema(), webpage, img_node] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    canon = "" if robots.startswith("noindex") else f'<link rel="canonical" href="{canonical}">\n'
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
{canon}<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Virginia">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Virginia">
<meta name="geo.region" content="US-VA">
<meta name="geo.placename" content="Virginia">
<meta name="theme-color" content="#00297B">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&amp;family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
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
    """'/' -> home.html; '/404.html' -> 404.html; '/x/y/' -> x/y/index.php with the guard as line 1."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, lazy=False, alt="", extra=' data-parallax="0.18"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-h">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="box-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-accent btn-block" href="{CONTACT}">Send claim details</a><p class="box-small">Mon–Fri 8am–6pm ET · All of Virginia</p></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-h">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Carrier’s number and the repair bill don’t match?", p="Send us the estimate. We’ll review it and tell you what we see, at no cost for the first look."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span></a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Wind / derecho / tornado", "Hurricane / nor’easter", "Water / burst pipe", "Fire / smoke / lightning", "Fallen tree / ice", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", idp="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    places = [loc_label(l) for l in LOCATIONS] + ["Elsewhere in Virginia"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-h">{e(heading)}</p><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{idp}-name">Full name *</label><input id="{idp}-name" name="name" autocomplete="name" required></div>
<div><label for="{idp}-phone">Phone *</label><input id="{idp}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{idp}-email">Email *</label><input id="{idp}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{idp}-role">I am a…</label><select id="{idp}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{idp}-loss">Type of loss</label><select id="{idp}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{idp}-city">Property location</label><select id="{idp}-city" name="city">{_opt(places)}</select></div>
<div><label for="{idp}-amt">Amount in dispute (approx.)</label><select id="{idp}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{idp}-car">Insurance company (optional)</label><input id="{idp}-car" name="carrier"></div>
<div class="full"><label for="{idp}-det">What happened, and where does the claim stand?</label><textarea id="{idp}-det" name="details" rows="4" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{idp}-web">Website</label><input id="{idp}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-primary btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-h">Free claim review</p><p class="form-sub">Three fields. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy policy</a>.</span></label>
<button class="btn btn-accent btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="form-trust">{ic("shield")}No obligation. Your details stay private.</p>
</form>"""


def photo_card(href, photo, kicker, title, text, h="h3"):
    return f'<a class="pcard rv" href="{href}"><span class="pcard-media">{img(photo, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span><span class="pcard-body"><span class="pcard-k">{e(kicker)}</span><{h}>{e(title)}</{h}><span class="pcard-t">{e(text)}</span><span class="pcard-go">Read more {ic("arrow")}</span></span></a>'


# ---------------------------------------------------------------- home
REGIONS = [
    ("tidewater", "Hampton Roads & Eastern Shore", "norfolk-waterfront", ["Hurricanes", "Nor’easters", "Wind-driven rain", "Condo losses"],
     "Named-storm deductibles, wind-versus-flood questions and crawlspace homes define claims from Virginia Beach and Norfolk to Hampton, Suffolk and the Eastern Shore."),
    ("nova", "Northern Virginia", "arlington-rosslyn", ["Flash flooding", "Derechos", "Fallen trees", "High-rise water losses"],
     "Arlington, Alexandria, Fairfax, Loudoun and Prince William bring high-dollar finishes, finished basements, condo towers and the state’s highest construction prices."),
    ("central", "Richmond & Central Virginia", "richmond-skyline", ["Tree strikes", "Hail", "Ice", "Historic rowhouses"],
     "Richmond’s rowhouses, Fredericksburg’s historic downtown and fast-growing suburbs in Henrico, Chesterfield and Stafford see thunderstorms, hail and ice under a heavy tree canopy."),
    ("valley", "Shenandoah Valley & Blue Ridge", "blue-ridge-mountains", ["Hail", "Ice storms", "Frozen pipes", "Steep roofs"],
     "Charlottesville, Harrisonburg, Staunton and Winchester sit in hail country, with winter ice, slate roofs on older homes and steep lots that raise labor costs."),
    ("southwest", "Roanoke, Southside & Southwest", "roanoke-valley", ["Flash flooding", "Tornadoes", "Hail", "Ice"],
     "From Roanoke and Lynchburg to Danville and the coalfields, claims follow mountain flash floods, spring tornadoes and the kind of hail that strips old roofs."),
]


def home():
    svc_cards = "".join(photo_card(f'{SVC_BASE}{s["slug"]}/', SVC_PHOTO[s["slug"]], f"Service {i + 1:02d}", s["name"], s["short"]) for i, s in enumerate(SERVICES))
    loc_cards = "".join(
        f'<a class="lcard rv" href="{loc_path(l)}"><span class="lcard-media">{img(l["photo"], sizes="(max-width:700px) 50vw, 25vw", alt="")}</span><span class="lcard-body"><b>{e(l["city"])}</b><small>{e(l["region"])}</small></span></a>'
        for l in LOCATIONS)
    tool_cards = "".join(photo_card(f'{TOOL_BASE}{t["slug"]}/', t["photo"], t["kind"], t["name"], t["short"]) for t in TOOLS)
    posts = "".join(photo_card(f'{POST_BASE}{p["slug"]}/', p["photo"], f'Guide · {p["read"]} read', p["title"], p["summary"]) for p in POSTS[:3])
    steps = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(STEPS))
    regions = "".join(
        f'<li class="region" tabindex="0">{img(ph, sizes="(max-width:900px) 100vw, 40vw", alt="")}<div class="region-in"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p></div></li>'
        for k, n, ph, perils, t in REGIONS)

    home_faqs = [
        ("What does a Virginia Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree about what it costs. As your named appraiser, we inspect, build an independent line-item estimate, work with the insurer’s appraiser and present open items to a neutral umpire if needed."),
        ("How is that different from a public adjuster?", "Public adjusters are licensed by the Virginia Bureau of Insurance to handle and negotiate whole claims. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When is it worth calling a Virginia Insurance Appraiser?", "When coverage has been accepted, you have the insurer’s estimate, and the gap between it and a qualified contractor’s number is meaningful, often more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, yes, once two of the three panel members sign. That’s why we build the file carefully before anyone demands appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire’s fee. We put our fee in writing before any work begins, and the first review is free."),
        ("Which parts of Virginia do you serve?", "All of it: 95 counties and 38 independent cities, with regular work in Hampton Roads, Northern Virginia, Richmond, Charlottesville, Roanoke and Lynchburg."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero-brick-colonial", lazy=False, alt="", extra=' data-parallax="0.22"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-light">Independent property claim appraisal · Commonwealth-wide</p>
<h1>Virginia Insurance Appraiser for claims that came up <em>short</em></h1>
<p class="lede">When your insurer accepts the claim but the payment won’t cover the repair, Virginia Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="#services">See our services {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Named appraiser or neutral umpire</li><li>{ic("check")}Pricing for your Virginia ZIP code</li><li>{ic("check")}Homes, condos, HOAs and businesses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap"><ul class="ledger-in">
<li><b data-count="133">133</b><span>Virginia localities served</span></li>
<li><b data-count="95">95</b><span>counties, plus 38 independent cities</span></li>
<li><b data-count="12">12</b><span>appraisal &amp; estimating services</span></li>
<li><b>2 of 3</b><span>signatures make an award binding</span></li>
</ul></div></section>

<section class="sec"><div class="wrap split">
<div class="rv">
<p class="kicker">The short version</p>
<h2>What a Virginia Insurance Appraiser does, and doesn’t do</h2>
<p>Most short claims aren’t denials. They’re estimates that missed something: two slopes instead of five, plaster priced as drywall, a floor that can’t be matched, a crane left off a tree job. Virginia Insurance Appraiser works on that gap between “covered” and “paid in full.”</p>
<ol class="numbered">
<li><b>We value the loss from scratch.</b> Our own inspection and measurements, never an edited copy of the insurer’s estimate.</li>
<li><b>We build numbers that survive scrutiny.</b> An inflated estimate loses credibility with an umpire. A documented one moves the award.</li>
<li><b>We tell you when appraisal is the wrong tool.</b> Denials, coverage fights and looming suit deadlines belong with a Virginia attorney.</li>
</ol>
<a class="btn btn-primary" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
<figure class="framed rv">{img("roofer-shingles", sizes="(max-width:900px) 100vw, 46vw")}<figcaption><b>Measured, not guessed.</b> Every Virginia Insurance Appraiser estimate starts with our own field inspection.</figcaption></figure>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Appraisal &amp; estimating</p><h2>Services from Virginia Insurance Appraiser</h2><p>Twelve services, one goal: a valuation of your loss that holds up. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="cards cards-3" data-stagger>{svc_cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Honest triage</p><h2>When to call a Virginia Insurance Appraiser, and when not to</h2></div>
<div class="fit" data-stagger>
<div class="fit-col fit-yes rv"><h3>{ic("check")}Appraisal usually fits</h3><ul><li>Coverage is accepted, but the amount is disputed</li><li>Repair-versus-replace disagreements on roofs and siding</li><li>Matching problems with discontinued materials</li><li>Missing trades, code items, crane work or overhead and profit</li></ul></div>
<div class="fit-col fit-no rv"><h3>{ic("x")}Appraisal usually doesn’t</h3><ul><li>The claim was denied outright</li><li>The dispute is about what the policy covers</li><li>A suit deadline is close and needs an attorney</li><li>The gap is too small to justify the fees</li></ul></div>
</div>
</div></section>

<section class="sec sec-navy"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-light">The process</p><h2>Seven steps from short check to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined procedure. Here is how Virginia Insurance Appraiser moves a file from the first call to a binding number.</p></div>
<div class="track" data-track><div class="track-bar" aria-hidden="true"><span></span></div><ol class="steps">{steps}</ol></div>
<p class="center"><a class="btn btn-ghost-light" href="{PROCESS}">Read the full process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-tint" id="gap"><div class="wrap split">
<div class="rv"><p class="kicker">Quick check</p><h2>Is the gap big enough for appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a Virginia Insurance Appraiser makes sense. If it’s small, a documented supplement may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}claim-gap-and-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees so you can see a realistic net figure. Example figures are illustrative.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Five claim climates</p><h2>Virginia’s regions don’t file the same claims</h2><p>Hurricanes in Norfolk, flash floods in Arlington, ice in Charlottesville, hail in Roanoke. A Virginia Insurance Appraiser has to know how each region’s weather shows up on a roof and in an estimate.</p></div>
<ul class="regions rv">{regions}</ul>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Local knowledge</p><h2>Where Virginia Insurance Appraiser works most</h2><p>We take files in every county and independent city. These twelve localities each have their own page with local storm history and housing notes.</p></div>
<div class="lcards" data-stagger>{loc_cards}</div>
<p class="center"><a class="btn btn-primary" href="{LOC_BASE}">All Virginia localities {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Virginia ground rules</p><h2>Four facts every Virginia policyholder should know</h2><p>A Virginia Insurance Appraiser isn’t a lawyer, but these basics shape every claim we see. They’re general information, not legal advice.</p></div>
<div class="facts-grid" data-stagger>
<div class="fact rv"><span class="fact-k">Regulator</span><h3>Bureau of Insurance</h3><p>Part of the State Corporation Commission. It licenses insurers, agents and public adjusters and takes consumer complaints.</p></div>
<div class="fact rv"><span class="fact-k">Market of last resort</span><h3>VPIA, the FAIR Plan</h3><p>The Virginia Property Insurance Association offers basic property coverage to owners who can’t find it in the regular market.</p></div>
<div class="fact rv"><span class="fact-k">Bad-faith remedy</span><h3>Va. Code § 38.2-209</h3><p>Lets a court award costs and attorney’s fees in certain cases where an insurer refused to pay in bad faith. That’s a legal question, outside appraisal.</p></div>
<div class="fact rv"><span class="fact-k">Deadline</span><h3>Commonly two years</h3><p>Virginia’s standard fire policy provisions commonly allow two years from the loss to file suit. Your policy controls, and appraisal may not pause it.</p></div>
</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Seven free tools from Virginia Insurance Appraiser</h2><p>Run the numbers before you pick up the phone. Every calculator runs in your browser, and nothing you enter is stored or sent.</p></div>
<div class="cards cards-4" data-stagger>{tool_cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Virginia Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Virginia Insurance Appraiser</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Handle and negotiate the claim</td><td>Legal disputes and lawsuits</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, amount disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Binding award (2 of 3 signatures)</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec sec-tint"><div class="wrap split split-top">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask a Virginia Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-primary" href="{FAQ_P}">All appraisal questions {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Claim &amp; policy terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from Virginia Insurance Appraiser on policy language, documentation and the rules that apply in Virginia.</p></div>
<div class="cards cards-3" data-stagger>{posts}</div>
<p class="center"><a class="btn btn-line" href="{POST_BASE}">All claim guides {ic("arrow")}</a></p>
</div></section>

<section class="cta-photo"><div class="cta-photo-media">{img("storm-sky", alt="", extra=' data-parallax="0.25"')}</div><div class="wrap cta-photo-in rv"><p class="kicker kicker-light">Before you sign off</p><h2>The best time to check the numbers is before you accept them</h2><p>A short review now can keep you from settling for a payment that won’t cover the repair.</p><div class="btn-row"><a class="btn btn-accent" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec sec-navy" id="contact"><div class="wrap split split-top">
<div class="rv"><p class="kicker kicker-light">Start with a conversation</p><h2>Talk to a Virginia Insurance Appraiser about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure, no obligation.</p>
<ul class="contact-list"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Coverage</small>All 133 Virginia localities</span></li></ul></div>
<div class="rv">{lead_form(page="/", idp="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Virginia Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid storm, tree, water and fire claims.",
                        body, [faq_schema(home_faqs)], [("Home", "/")], "hero-brick-colonial"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        art = s["body"] + f'<h2>Questions about {e(s["name"].lower())}</h2>' + faq_block(s["faqs"]) + "<h2>Related services</h2>" + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(art, call_box() + list_box("All services", items, path) + list_box("Where we work", locs + [("All localities", LOC_BASE)])) + cta_strip()
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Virginia"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, trail, ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(photo_card(f'{SVC_BASE}{s["slug"]}/', SVC_PHOTO[s["slug"]], f"Service {i + 1:02d}", s["name"], s["short"], h="h2") for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in Virginia",
                     "Panel representation, estimate reviews, umpire work and peril-specific valuations. Every service is built around one thing: an accurate, defensible number for your loss.", "roofer-shingles") + f"""
<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn btn-primary" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and HOA claims?", "Yes: offices, retail, churches, apartments, warehouses and condo or townhome associations."), ("Do you only work storm claims?", "No. We also value water, fire, smoke, lightning and tree claims, plus historic-home losses.")])}</div></div></section>
{cta_strip()}"""
    schema = [{"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Virginia | 12 Options",
                             "Insurance appraisal services in Virginia: appraisal clause work, estimate reviews, umpire services and storm, water, fire and tree claims.",
                             body, schema, trail, "roofer-shingles"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(loc_label(l), loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Localities", LOC_BASE), (l["city"], path)]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        near = related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        art = (f'<div class="note"><b class="h">Local claim risks</b><ul class="chips chips-dark">{chips}</ul><p class="note-small"><b>Housing mix:</b> {e(l["housing"])}.</p></div>'
               + l["body"]
               + f'<h2>Services available in {e(l["city"])}</h2><p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area, including:</p><ul class="cols2">{svc_links}</ul>'
               + f'<h2>Questions from {e(l["city"])} property owners</h2>' + faq_block(l["faqs"])
               + "<h2>Nearby localities</h2>" + near)
        aside = call_box() + list_box("Virginia localities", items, path) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {loc_label(l)}", l["lede"], l["photo"],
                         [("Locality", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, aside) + cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        area = {"@type": "AdministrativeArea" if l["kind"] == "County" else "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Virginia"}}
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {loc_label(l)}", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": area, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, trail, l["photo"]), 0.8)

    trail = [("Home", "/"), ("Localities", LOC_BASE)]
    cards = "".join(photo_card(loc_path(l), l["photo"], l["region"], loc_label(l), l["county"], h="h2") for l in LOCATIONS)
    regions = "".join(f'<div class="region-row rv"><span class="region-row-media">{img(ph, sizes="(max-width:700px) 100vw, 280px", alt="")}</span><div><h3>{e(n)}</h3><p>{e(t)}</p></div></div>' for k, n, ph, _p, t in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisers Serving All of Virginia",
                     "Virginia is divided into 95 counties and 38 independent cities, 133 localities in all, and we take files in every one. These local pages cover the places where we work most often.", "blue-ridge-mountains") + f"""
<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims change across the Commonwealth</h2><p>The same policy language plays out differently in a Sandbridge rental, an Arlington condo and a Roanoke foursquare.</p></div><div class="region-rows">{regions}</div></div></section>
{cta_strip("Don’t see your city or county?", "We work in all 133 Virginia localities. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraisers Serving All Virginia Localities",
                             "Insurance appraisers serving all 133 Virginia localities, including Virginia Beach, Norfolk, Richmond, Arlington, Fairfax and Roanoke.",
                             body, [{"@type": "CollectionPage"}, itemlist(items)], trail, "blue-ridge-mountains"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        art = t["explain"] + "<h2>Questions about this tool</h2>" + faq_block(t["faqs"]) + "<h2>More free tools</h2>" + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = (page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], t["photo"], cta=False)
                + f'<section class="sec sec-tool"><div class="wrap"><div class="rv">{t["markup"]}</div><p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice. Default figures are illustrative.</p><noscript><p class="tool-note">This calculator needs JavaScript. Everything runs in your browser and nothing is sent anywhere.</p></noscript></div></section>'
                + layout(art, call_box() + list_box("All free tools", items, path)) + cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line."))
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, trail, t["photo"]), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    cards = "".join(photo_card(f'{TOOL_BASE}{t["slug"]}/', t["photo"], t["kind"], t["name"], t["short"], h="h2") for t in TOOLS)
    order = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(n)}</a>: {e(w)}</li>' for s, n, w in [
        ("claim-clock-calendar-builder", "Claim clock & calendar builder", "put every policy deadline on your calendar first."),
        ("roof-pitch-and-squares-checker", "Roof pitch & squares checker", "check the roof measurements in the estimate."),
        ("fallen-tree-claim-splitter", "Fallen tree claim splitter", "see how tree limits change the payment."),
        ("hurricane-wind-deductible-converter", "Deductible converter", "see what a percentage deductible costs you."),
        ("holdback-recovery-calculator", "Holdback recovery calculator", "split the payment into ACV and holdback."),
        ("claim-gap-and-fee-estimator", "Claim gap & fee estimator", "test whether the dispute justifies appraisal."),
        ("appraisal-readiness-scorecard", "Readiness scorecard", "find the gaps in your file before you demand.")])
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Virginia Owners",
                     "Seven calculators and planners built from real appraisal work. Check the insurer’s math, plan your deadlines and decide on next steps. No sign-up, and nothing is stored.", "calculator-papers", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="order">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Virginia",
                              "Free insurance claim calculators for Virginia: claim gap and fees, RCV vs ACV holdback, roof squares, deductibles, deadlines and trees.",
                              body, [{"@type": "CollectionPage"}, itemlist(items)], trail, "calculator-papers"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("How appraisal works", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _d) in enumerate(STEPS))
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Virginia",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what, and where Virginia files most often go wrong.", "tape-measure",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(
        f'<nav class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>{toc}</ol></nav>' + PROCESS_BODY,
        call_box() + list_box("Resources", RES_LINKS, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Virginia", "description": "The seven stages of a property insurance appraisal under a typical Virginia policy.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, d) in enumerate(STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Virginia | 7 Steps",
                         "How insurance appraisal works in Virginia: the written demand, naming appraisers, choosing an umpire and the binding award, step by step.",
                         body, [howto], trail, "tape-measure"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    jump = "".join(f'<li><a href="#faq-{i}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Virginia Insurance Appraisal Questions, Answered",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, costs, timing, Virginia rules and working with us.", "consult-table") + layout(
        f'<nav class="toc" aria-label="Topics"><p class="toc-h">Topics</p><ol>{jump}</ol></nav>' + groups,
        call_box() + list_box("Resources", RES_LINKS, path)) + cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")
    write(path, document(path, "Virginia Insurance Appraisal FAQ | Grouped by Topic",
                         "Virginia insurance appraisal FAQ grouped by topic: how appraisal works, costs, deadlines, the Bureau of Insurance and working with us.",
                         body, [faq_schema(allq)], trail, "consult-table"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim & policy terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gterm"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim & Policy Terms Glossary",
                     f"{len(GLOSSARY)} terms you’ll see in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "laptop-estimate", cta=False) + layout(
        f'<div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”" autocomplete="off"><p class="filter-count" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>',
        call_box() + list_box("Resources", RES_LINKS, path))
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim and policy terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": f"{DOMAIN}{path}#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | 40+ Policy Terms Defined",
                         "Insurance claim glossary of 40+ policy and appraisal terms in plain English: ACV, RCV, umpire, VPIA, hurricane deductible and more.",
                         body, [dts], trail, "laptop-estimate"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        art = f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>' + p["body"] + "<h2>Keep reading</h2>" + related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Guide · {p['read']} read", p["title"], e(p["summary"]), p["photo"], cta=False) + layout(art, call_box() + list_box("Resources", RES_LINKS) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        art_s = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f'{DOMAIN}/assets/img/photos/{p["photo"]}.webp', "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [art_s], trail, p["photo"], og_type="article"), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim guides", path)]
    cards = "".join(photo_card(f'{POST_BASE}{p["slug"]}/', p["photo"], date.fromisoformat(p["date"]).strftime("%b %-d, %Y") + f' · {p["read"]} read', p["title"], p["summary"], h="h2") for p in POSTS)
    body = page_hero(trail, "Claim guides", "Virginia Property Claim Guides",
                     "Practical guides on policy language, documentation, deductibles and the rules that apply to Virginia property claims.", "storm-sky", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Virginia Property Claim Guides | Appraisal & Policy Tips",
                         "Virginia property claim guides on appraisal clauses, bad-faith rules, hurricane deductibles, the FAIR Plan and storm damage documentation.",
                         body, [{"@type": "CollectionPage"}, itemlist([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], trail, "storm-sky"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    art = f"""
<figure class="framed">{img("consult-table", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we only do appraisal</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your named appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> A padded estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know exactly what our work costs before it starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, association boards, property managers, churches, business owners, contractors and attorneys across Virginia. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser, the umpire or the insurer.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t guarantee outcomes, because no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Virginia stretches from Atlantic beaches to Appalachian coalfields. Working across all 133 localities means we see every kind of loss the Commonwealth produces, from hurricane wind in Hampton Roads and flash floods in Arlington to ice in Charlottesville and hail in Roanoke, and price each with local knowledge.</p>
"""
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "roofer-shingles") + layout(
        art, call_box() + list_box("Explore", [("Our services", SVC_BASE), ("Localities", LOC_BASE), ("Free tools", TOOL_BASE), ("How appraisal works", PROCESS)])) + cta_strip()
    write(path, document(path, f"About {BRAND} | How We Work",
                         "About Virginia Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss in property claims.",
                         body, [{"@type": "AboutPage"}], trail, "roofer-shingles"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "hero-brick-colonial", cta=False) + f"""
<section class="sec sec-navy"><div class="wrap split split-top">
<div class="rv"><h2>Reach us directly</h2>
<ul class="contact-list"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Service area</small>Statewide: all 133 localities</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks ticks-light"><li>{ic("check")}Your declarations page</li><li>{ic("check")}The insurer’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the insurer</li><li>{ic("check")}Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, idp="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Contact Virginia Insurance Appraiser for a free review of a disputed property claim. Call (844) 537-1427 or send your claim details online.",
                         body, [{"@type": "ContactPage"}], trail, "hero-brick-colonial"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "How we collect, use and protect the information you share with us.",
                  f"Privacy Policy | {BRAND}",
                  "Privacy policy for Virginia Insurance Appraiser: what we collect through our forms, how we use it, and the choices you have about your data.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and the readiness scorecard run in your browser. The figures you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, we’ll update this policy to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "The terms that apply when you use this website and its tools.",
                f"Terms of Use | {BRAND}",
                "Terms of use for the Virginia Insurance Appraiser website, its calculators and its content, including limits on liability and governing law.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Virginia.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship starts only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. For legal questions, consult a Virginia attorney.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates based on what you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free public-domain or CC0 images used for illustration and don’t show our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the Commonwealth of Virginia.</p>"""),
        DISC: ("Disclaimer", "Important limits on the information published on this website.",
               f"Disclaimer & Notices | {BRAND}",
               "Disclaimer for Virginia Insurance Appraiser: general information only, not legal advice, not a public adjuster and no guarantee of results.", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process.</p>
<h2>Statutes and agencies</h2><p>References to Virginia statutes, the Bureau of Insurance, the VPIA or past storms are general descriptions for context. They may be summarized, may change, and shouldn’t be relied on without checking official sources or speaking with a Virginia attorney.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site, including calculator defaults, are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a Virginia attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free public-domain or CC0 images used for illustration. They don’t depict our clients’ properties or results.</p>"""),
    }
    for path, (h1, lede, title, desc, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "alexandria-old-town", cta=False) + layout(content, call_box())
        write(path, document(path, title, desc, body, [], trail, "alexandria-old-town"), 0.3)


def sitemap_pages():
    path = SMAP
    trail = [("Home", "/"), ("Site contents", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Localities", [("All localities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", RES_LINKS + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISC)]),
    ]
    cols = "".join(f'<div class="smap-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Contents", f"Every page on {BRAND}, grouped by section.", "blue-ridge-mountains", cta=False) + f'<section class="sec"><div class="wrap smap" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Contents | {BRAND}",
                         "Site contents for Virginia Insurance Appraiser: every service, Virginia locality, free claim calculator, guide and legal page in one list.",
                         body, [], trail, "blue-ridge-mountains"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-media">{img("ice-storm", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-light">Error 404</p><h1>That page came down in the storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-accent" href="/">Home</a><a class="btn btn-ghost-light" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-light" href="{TOOL_BASE}">Free tools</a><a class="btn btn-ghost-light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "This page could not be found on Virginia Insurance Appraiser. Use the links here to reach our services, free tools or contact page.",
                                body, [], [("Home", "/"), ("Page not found", "/404.html")], "ice-storm", robots="noindex,follow"), sitemap=False)


GUARD_PHP = r"""<?php
// Virginia Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$via_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$via_real  = 'virginiainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$via_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://virginiainsuranceappraiser.com - only on the real domain.
if ($via_host === 'www.' . $via_real || ($via_host === $via_real && $via_proto === 'http')) {
    header('Location: https://' . $via_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $via_m)) {
    $via_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $via_m[1] . $via_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($via_host !== $via_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Virginia Insurance Appraiser - front controller for the static build.
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
    # Search Console verification: exact bytes, no newline, no BOM, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


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
