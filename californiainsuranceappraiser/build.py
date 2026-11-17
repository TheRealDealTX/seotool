#!/usr/bin/env python3
"""Static site generator for californiainsuranceappraiser.com.

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
from locations import LOCATIONS, LOC_DESC  # noqa: E402
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402
from photos import PHOTOS, ALT, SVC_PHOTO, LOC_PHOTO, TOOL_PHOTO, POST_PHOTO  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")

BRAND = "California Insurance Appraiser"
HOST = "californiainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261116a"
FAV = "1"
# Google Tag Manager: container ID, and the head snippet exactly as provided by the site owner.
GTM_ID = "GTM-KRLKWZKJ"
GTM_HEAD = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-KRLKWZKJ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""
# Google Search Console verification file: written verbatim at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/disputed-claim-services/"
LOC_BASE = "/city-coverage/"
TOOL_BASE = "/claim-check-tools/"
POST_BASE = "/appraisal-playbook/"
PROCESS = "/the-appraisal-process/"
FAQ_P = "/appraisal-questions/"
GLOSS = "/claim-terms-defined/"
ABOUT = "/about-the-firm/"
CONTACT = "/get-in-touch/"
PRIVACY = "/privacy/"
TERMS = "/terms/"
DISCLAIMER = "/legal-disclaimer/"
SITEMAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraiser/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}


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
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "box": '<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "roof": '<path d="M2 12l10-8 10 8"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "policyholder-appraiser-representation": "scale", "home-claim-appraisal": "home", "commercial-hoa-claim-appraisal": "building",
    "roof-damage-appraisal": "roof", "santa-ana-wind-damage-appraisal": "wind", "atmospheric-river-storm-claim-appraisal": "storm",
    "water-leak-claim-appraisal": "drop", "smoke-ash-fire-claim-appraisal": "flame", "wildfire-total-loss-appraisal": "flame",
    "contents-inventory-appraisal": "box", "carrier-estimate-review": "file", "umpire-appointment-services": "doc",
}


def mark(cls="mark"):
    # Brand mark: crimson tile, copper roofline over a white "equals" bar pair (a fair valuation).
    return (f'<svg class="{cls}" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#ba0c2f"/>'
            '<path d="M10 23.5L24 12l14 11.5" fill="none" stroke="#e2b07e" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="15" y="27" width="18" height="3.6" rx="1.8" fill="#fff"/><rect x="15" y="33.6" width="18" height="3.6" rx="1.8" fill="#fff"/></svg>')


def brand_link(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>California</b><span>Insurance Appraiser</span></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "CA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-CA", "availableLanguage": "en"}],
        "slogan": "An independent number for disputed property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims throughout California.",
        "areaServed": [{"@type": "State", "name": "California"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "California Insurance Code §2071", "Wildfire claims", "Smoke damage", "Xactimate estimating", "Umpire services"],
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


def itemlist(items):
    return {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def nav_groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All California cities", LOC_BASE)),
        ("Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE)),
        ("Learn", [("The appraisal process", PROCESS), ("Appraisal questions", FAQ_P), ("Claim terms defined", GLOSS), ("Appraisal playbook", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(nav_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "ic chev")}</button><ul class="sub{wide}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{ABOUT}">About</a></li><li><a class="top-link" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(nav_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-panel" id="acc-{i}" hidden><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About the firm</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="util"><div class="wrap"><span>Independent claim appraisal in all 58 California counties</span><span class="util-r"><a href="mailto:{EMAIL}" class="hide-s">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></span></div></div>
<header class="site-head" id="top"><div class="wrap head-in">
{brand_link()}
<nav class="main-nav" aria-label="Main"><ul class="nav-list">{menu}</ul></nav>
<a class="btn btn-sm btn-copper head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link()}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri, 8am–6pm Pacific</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot"><div class="wrap">
<div class="foot-band"><p class="foot-big">Covered isn’t the same as paid in full.</p><div class="btn-row"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Send claim details</a></div></div>
<div class="foot-grid">
<div class="foot-about">{brand_link("brand brand-foot")}
<p>Independent appraisal, estimate review and umpire services for property owners with disputed insurance claims, from the Redwood Coast to the Imperial Valley.</p>
<p class="foot-lines"><a href="tel:{TEL}">{PHONE_INTL}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><span>Mon–Fri, 8am–6pm Pacific · Statewide</span></p></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h2 class="foot-h">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Firm</h2><ul><li><a href="{ABOUT}">About the firm</a></li><li><a href="{PROCESS}">The appraisal process</a></li><li><a href="{FAQ_P}">Appraisal questions</a></li><li><a href="{GLOSS}">Claim terms defined</a></li><li><a href="{POST_BASE}">Appraisal playbook</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="foot-legal"><span>© {date.today().year} {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIMER}">Disclaimer</a></li><li><a href="{SITEMAP}">All pages</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general; your policy controls. Results depend on the facts of each claim and are never guaranteed.</p>
</div></footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<nav class="call-bar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")} Call</a><a href="{CONTACT}">{ic("mail")} Free review</a></nav>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return "<!-- Google Tag Manager -->\n" + GTM_HEAD + "\n<!-- End Google Tag Manager -->\n"


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-home", page_type="WebPage", trail=None, body_cls=""):
    canonical = DOMAIN + path
    trail = trail or [("Home", "/")]
    nodes = [crumbs_schema(trail)] + list(schema or [])
    for n in nodes:
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
    p = PHOTOS[photo]
    pimg = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "contentUrl": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"], "caption": ALT[photo]}
    main = next((n["@id"] for t in MAIN_TYPES for n in nodes if n.get("@type") == t), DOMAIN + "/#business")
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": canonical + "#breadcrumb"}, "primaryImageOfPage": {"@id": canonical + "#primaryimage"},
        "image": {"@id": canonical + "#primaryimage"}, "mainEntity": {"@id": main},
    }
    graph = [org_schema(), site_schema(), webpage, pimg] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=" js";</script>
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across California">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across California">
<meta name="geo.region" content="US-CA">
<meta name="geo.placename" content="California">
<meta name="theme-color" content="#7d0820">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,500;6..96,600;6..96,700&family=Jost:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
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
        assert "<?" not in content, path
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
    c = f'<div class="btn-row"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="p-hero"><div class="p-hero-img">{img(photo, lazy=False, alt="")}</div><div class="wrap p-hero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="qa">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev")}</summary><div class="qa-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-card side-call"><p class="side-h">Talk it through</p><p>A free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="side-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-copper btn-block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-card"><p class="side-h">{e(title)}</p><ul class="side-list">{li}</ul></div>'


def aside(*boxes):
    return '<aside class="side"><div class="side-sticky">' + "".join(boxes) + "</div></aside>"


def cta_strip(h="Is the carrier’s number short?", p="Send the estimate and your photos. We’ll review them and tell you plainly what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="rel-grid">' + "".join(f'<a class="rel" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


def photo_card(href, photo, kicker, title, text, h="h3", sizes="(max-width:720px) 100vw, 33vw"):
    return f'<a class="pcard rv" href="{href}"><span class="pcard-img">{img(photo, sizes=sizes, alt="")}</span><span class="pcard-body"><span class="pcard-k">{e(kicker)}</span><{h} class="pcard-t">{e(title)}</{h}><span class="pcard-p">{e(text)}</span><span class="pcard-go">Read more {ic("arrow")}</span></span></a>'


LOSSES = ["Wildfire / total loss", "Smoke & ash", "Wind", "Storm / roof leak", "Water / plumbing", "Fire (partial)", "Contents", "Earthquake / fire following", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel="h2", fid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Commercial owner", "HOA board / manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in California"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<{hlevel} class="lead-h">{e(heading)}</{hlevel}><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Approx. amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$50,000</option><option>$50,000–$150,000</option><option>$150,000–$500,000</option><option>Over $500,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-crimson btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hero-form-h">Get a free claim review</h2><p class="lead-sub">Three fields. We’ll call within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn btn-crimson btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("North Coast & Redwood Empire", "Santa Rosa · Eureka · Ukiah", "Wildfire, river flooding, falling redwoods and firs, and FAIR Plan policies on rural homes.", "santa-rosa"),
    ("Bay Area", "San Francisco · Oakland · San Jose", "Shared walls, water between units, hillside fire risk and some of the highest repair costs in the country.", "san-francisco"),
    ("Sacramento Valley & Foothills", "Sacramento · Chico · Redding", "Tree impacts in winter storms, atmospheric-river leaks and Camp Fire–scale wildfire exposure in the foothills.", "sacramento"),
    ("Central Valley & Sierra", "Fresno · Bakersfield · Modesto", "Heat-aged roofs, farm buildings, smoke from Sierra fires and snow load at elevation.", "fresno"),
    ("Central Coast", "Ventura · Santa Barbara · San Luis Obispo", "Canyon wildfires, post-fire debris flows and coastal storms on older homes.", "ventura"),
    ("Southern California", "Los Angeles · Orange County · Inland Empire · San Diego", "Santa Ana winds, tile roofs, HOA master-policy gaps and the largest wildfire rebuilds in state history.", "los-angeles"),
]


def home():
    svc_feature = SERVICES[8], SERVICES[0]  # wildfire total loss, representation
    svc_cards = "".join(photo_card(f'{SVC_BASE}{s["slug"]}/', SVC_PHOTO[s["slug"]], f"Service {i + 1:02d}", s["name"], s["short"]) for i, s in enumerate(SERVICES[:6]))
    svc_more = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{ic(SVC_ICON[s["slug"]])}<span>{e(s["name"])}</span></a></li>' for s in SERVICES[6:])

    steps = [
        ("Free file review", "We read the policy, the carrier’s estimate and your photos, and tell you whether appraisal makes sense."),
        ("Independent estimate", "We inspect, measure and build our own line-item valuation, priced for your part of California."),
        ("Written demand", "Appraisal is demanded in writing and California Insurance Appraiser is named as your appraiser within 20 days."),
        ("Appraiser-to-appraiser", "We work through every disputed item with the carrier’s appraiser. Most gaps narrow here."),
        ("Signed award", "Remaining items go to the umpire. Any two signatures on an itemized award set the amount."),
    ]
    tl = "".join(f'<li class="tl-step rv"><span class="tl-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    rail = "".join(f'<article class="reg-card"><div class="reg-img">{img(LOC_PHOTO[ph], sizes="(max-width:720px) 85vw, 380px", alt="")}</div><div class="reg-body"><h3>{e(n)}</h3><p class="reg-c">{e(c)}</p><p>{e(t)}</p></div></article>' for n, c, t, ph in REGIONS)

    tools = "".join(photo_card(f'{TOOL_BASE}{t["slug"]}/', TOOL_PHOTO[t["slug"]], t["kind"], t["name"], t["short"]) for t in TOOLS[:6])
    cities = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></a></li>' for l in LOCATIONS)
    posts = "".join(photo_card(f'{POST_BASE}{p["slug"]}/', POST_PHOTO[p["slug"]], f'Guide · {p["read"]}', p["title"], p["summary"]) for p in POSTS[:3])

    home_faqs = [
        ("What does a California Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and don’t give legal advice."),
        ("When should I call a California Insurance Appraiser?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful, generally more than about 10% or several thousand dollars."),
        ("Can appraisal help after a wildfire?", "Yes, when the carrier accepts the loss but its rebuild, smoke or contents figure is too low. Appraisal cannot raise policy limits, but it can establish the full cost of the loss."),
        ("What does it cost?", "Each side pays its own appraiser and shares the umpire’s fee. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my county?", "Yes. California Insurance Appraiser works in all 58 counties, from Del Norte to Imperial."),
    ]

    body = f"""
<section class="hero">
<div class="hero-img">{img("hero-home", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent appraisal · All 58 counties</p>
<h1>California Insurance Appraiser for claims that came in short</h1>
<p class="lede">Your carrier accepted the claim. The check still won’t rebuild the house, clean out the smoke or replace what you lost. California Insurance Appraiser prices the loss independently and takes it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#services">See what we value</a></div>
<ul class="hero-ticks"><li>{ic("check")}Named as your appraiser</li><li>{ic("check")}Itemized, ZIP-level pricing</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap ledger-in">
<div class="led rv"><b data-count="58">58</b><span>California counties served</span></div>
<div class="led rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="led rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim tools</span></div>
<div class="led rv"><b data-count="20">20</b><span>Days to name appraisers after a demand</span></div>
</div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-img rv">{img("consult", sizes="(max-width:960px) 100vw, 540px")}<figure class="duo-quote"><blockquote>“Appraisal decides one thing: what the covered loss costs. That’s the only thing we do.”</blockquote></figure></div>
<div class="duo-copy rv">
<p class="kicker">The short version</p>
<h2>What a California Insurance Appraiser is hired to do</h2>
<p>Most short claims in California aren’t denied. They’re scoped narrowly. A tile roof priced as a spot repair, a smoke-filled house priced as a wipe-down, a hillside rebuild priced like a flat lot. California Insurance Appraiser exists for the space between “covered” and “paid in full.”</p>
<p>When you hire us, we become your appraiser under the policy’s appraisal clause, the process set out in the standard fire policy in Insurance Code §2071. We build the number from our own inspection, defend it line by line with the carrier’s appraiser, and present what remains to a neutral umpire.</p>
<div class="fit-pair">
<div class="fit yes"><h3>{ic("check")}Good fit</h3><ul><li>Coverage accepted, amount disputed</li><li>Repair-versus-replace disagreements</li><li>Rebuild cost below your real cost</li><li>Smoke scopes that stop at cleaning</li></ul></div>
<div class="fit no"><h3>{ic("x")}Not a fit</h3><ul><li>Full coverage denials</li><li>Bad-faith or legal claims</li><li>Small gaps that fees would erase</li><li>Deadlines that need a lawyer first</li></ul></div>
</div>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Losses we value</p><h2>California Insurance Appraiser services, from smoke to rebuild</h2><p>{len(SERVICES)} services built around one job: a valuation of your loss that holds up in front of an umpire.</p></div>
<div class="pgrid">{svc_cards}</div>
<ul class="svc-more rv">{svc_more}</ul>
<p class="center"><a class="btn btn-line" href="{SVC_BASE}">Compare every service {ic("arrow")}</a></p>
</div></section>

<section class="fire-band"><div class="fire-img">{img("wildfire-ruins", sizes="(max-width:960px) 100vw, 50vw", alt="")}</div><div class="wrap fire-in"><div class="fire-copy rv">
<p class="kicker light">The California peril</p>
<h2>After a wildfire, the rebuild estimate is the claim</h2>
<p>Tubbs, Camp, Woolsey, Palisades, Eaton. Each left thousands of families comparing a carrier’s rebuild figure with what local builders were actually charging. A California Insurance Appraiser can establish the full cost of a comparable rebuild under current code, which decides whether you reach extended replacement cost and code upgrade coverage.</p>
<ul class="ticks light"><li>{ic("check")}Dwelling, other structures and debris removal</li><li>{ic("check")}Contents inventories and depreciation</li><li>{ic("check")}Smoke and ash in homes that survived</li></ul>
<div class="btn-row"><a class="btn btn-copper" href="{SVC_BASE}{svc_feature[0]["slug"]}/">Wildfire total loss appraisal</a><a class="btn btn-line light" href="{TOOL_BASE}rebuild-cost-underinsurance-check/">Check your rebuild gap</a></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The path</p><h2>Five stages from disputed estimate to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process. Here is how California Insurance Appraiser runs a file.</p></div>
<ol class="tl" data-tl><span class="tl-line" aria-hidden="true"><span class="tl-fill"></span></span>{tl}</ol>
<p class="center"><a class="link" href="{PROCESS}">Read the full appraisal process {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap duo duo-tool">
<div class="rv"><p class="kicker">Two numbers</p><h2>Run the gap before you run the clause</h2><p>Enter the carrier’s estimate and your contractor’s. A large gap means a conversation with a California Insurance Appraiser is worth having; a small one usually closes faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds appraiser and umpire fees so you can see a realistic net figure.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="sec-head left rv"><p class="kicker light">Six regions</p><h2>From the Redwood Coast to the Imperial Valley</h2><p>California Insurance Appraiser works statewide because the claims change every few hundred miles. Scroll the regions.</p></div>
</div><div class="rail" tabindex="0" aria-label="California regions">{rail}</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free and private</p><h2>Free tools from a California Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser, and nothing you type is stored or sent.</p></div>
<div class="pgrid">{tools}</div>
<p class="center"><a class="btn btn-line" href="{TOOL_BASE}">All {len(TOOLS)} free tools {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraisal, a CDI complaint, mediation or a lawyer?</h2><p>Each solves a different problem. California Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Appraisal</th><th scope="col">CDI complaint</th><th scope="col">Mediation</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Best for</th><td class="hl">Disputed amount of a covered loss</td><td>Claim-handling problems and delays</td><td>Negotiated settlement with a neutral</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Itemized award, two of three signatures</td><td>Department review of the insurer’s handling</td><td>Voluntary agreement, if reached</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Only by agreement</td><td>Argues it in court</td></tr>
<tr><th scope="row">Typical cost</th><td class="hl">Own appraiser plus half the umpire</td><td>Free to file</td><td>Varies; sometimes offered after disasters</td><td>Varies by fee agreement</td></tr>
</tbody></table></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="duo duo-top">
<div class="rv"><p class="kicker">Where we work most</p><h2>California Insurance Appraiser city coverage</h2><p>California Insurance Appraiser works in all 58 counties. These twelve cities have their own pages with local claim history, neighborhoods and housing notes.</p><a class="btn btn-line" href="{LOC_BASE}">All city coverage {ic("arrow")}</a></div>
<ul class="city-list rv">{cities}</ul>
</div>
</div></section>

<section class="sec tint"><div class="wrap duo duo-top">
<div class="rv"><p class="kicker">Questions</p><h2>What owners ask a California Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-line" href="{FAQ_P}">Every question {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Claim terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The playbook</p><h2>Read this before you demand appraisal</h2><p>Practical guides from California Insurance Appraiser on policy language, documentation and strategy.</p></div>
<div class="pgrid">{posts}</div>
</div></section>

<section class="para-cta"><div class="para-img" data-parallax>{img("storm-clouds", sizes="100vw", alt="")}</div><div class="wrap para-in rv"><p class="kicker light">Before you sign a release</p><h2>Check the numbers before you accept them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the work.</p><div class="btn-row"><a class="btn btn-copper" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec dark" id="contact"><div class="wrap duo duo-top">
<div class="rv"><p class="kicker light">Start with a conversation</p><h2>Talk to a California Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. California Insurance Appraiser will review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="c-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Pacific</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 58 California counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hlevel="h3")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Property Claims",
                        "California Insurance Appraiser: independent appraisal, estimate review and umpire help for underpaid wildfire, smoke, wind and water claims.",
                        body, [faq_schema(home_faqs)], photo="hero-home", body_cls="has-hero"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(f'{l["city"]}', loc_path(l)) for l in LOCATIONS[:6]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap two-col"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
{aside(call_box(), list_box("All services", items, path), list_box("City coverage", locs + [("All cities", LOC_BASE)]))}</div>
{cta_strip()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "California"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(photo_card(f'{SVC_BASE}{s["slug"]}/', SVC_PHOTO[s["slug"]], f"Service {i + 1:02d}", s["name"], s["short"], h="h2") for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we value", "Insurance Appraisal Services for California Property Claims",
                     "From a single estimate review to full panel representation and neutral umpire work, every California Insurance Appraiser service is built around a defensible valuation of your loss.", "roof-crew") + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
<section class="sec tint"><div class="wrap duo duo-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn btn-line" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and HOA claims?", "Yes: retail, office, industrial, multifamily, churches and homeowner associations."), ("Do you only handle wildfire claims?", "No. We handle wind, storm, water, fire, smoke, contents and other covered losses statewide.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in California | All 12",
                             "Insurance appraisal services across California: appraisal clause representation, wildfire, smoke, wind, water and roof claims, and umpires.",
                             body, [itemlist(items)], photo="roof-crew", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        city = l["city"]
        trail = [("Home", "/"), ("City coverage", LOC_BASE), (city, path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {city}, California", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap two-col"><article class="prose">
<div class="note"><b class="h">Local claim risks in {e(city)}</b><ul class="chips">{chips}</ul><p class="hoods"><b>Neighborhoods we often work in:</b> {e(l["hoods"])}</p></div>
{l["body"]}
<h2>Services available in {e(city)}</h2>
<p>Every {BRAND} service is available to property owners in {e(city)} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(city)} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby city coverage</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
{aside(call_box(), list_box("California cities", items, path), list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {city}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraiser in {city}, California", "serviceType": "Insurance appraisal", "description": LOC_DESC[l["slug"]], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"]}}, "url": DOMAIN + path}]
        title = None
        for t in (f"Insurance Appraiser {city}, CA | Disputed Claims", f"Insurance Appraiser {city}, CA | Claim Appraisal", f"Insurance Appraiser {city}, CA"):
            if len(t) <= 56:
                title = t
                break
        write(path, document(path, title, LOC_DESC[l["slug"]], body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("City coverage", LOC_BASE)]
    cards = "".join(photo_card(loc_path(l), LOC_PHOTO[l["slug"]], l["county"], f'{l["city"]} insurance appraiser', l["lede"], h="h2") for l in LOCATIONS)
    reg = "".join(f'<li><h3>{e(n)}</h3><p class="reg-c">{e(c)}</p><p>{e(t)}</p></li>' for n, c, t, _ in REGIONS)
    body = page_hero(trail, "Statewide", "Insurance Appraisal in All 58 California Counties",
                     "California Insurance Appraiser works statewide, from Crescent City to Calexico. These pages cover the cities where we handle claims most often.", "la-skyline") + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">Regions</p><h2>How claims differ across California</h2><p>The same policy language plays out differently in a Sierra cabin, a San Francisco flat and an Inland Empire tract home.</p></div><ul class="reg-list rv">{reg}</ul></div></section>
{cta_strip("Don’t see your city?", "We work in every California county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "California Insurance Appraiser City Coverage",
                             "Insurance appraisal city coverage in all 58 California counties, including Los Angeles, San Diego, San Jose, Sacramento, Fresno and Chico.",
                             body, [itemlist(items)], photo="la-skyline", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint tool-note">For planning only. Results depend on what you enter and on your policy, and aren’t a quote, an appraisal or legal advice. Nothing you type leaves your browser.</p></div></section>
<div class="wrap two-col"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
{aside(call_box(), list_box("All claim tools", items, path))}</div>
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    cards = "".join(photo_card(f'{TOOL_BASE}{t["slug"]}/', TOOL_PHOTO[t["slug"]], t["kind"], t["name"], t["short"], h="h2") for t in TOOLS)
    body = page_hero(trail, "Free and private", "Free Claim Calculators for California Property Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Check the carrier’s math and plan your next step. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
<section class="sec tint"><div class="wrap duo duo-top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">timeline builder</a> so no deadline slips.</li><li>Check the roof with the <a href="{TOOL_BASE}roof-area-pitch-calculator/">roof area calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}acv-holdback-calculator/">ACV and holdback calculator</a>.</li><li>For a total loss, run the <a href="{TOOL_BASE}rebuild-cost-underinsurance-check/">rebuild cost check</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-payoff-estimator/">payoff estimator</a>, then the <a href="{TOOL_BASE}appraisal-readiness-check/">readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | California Tools",
                              "Free insurance claim calculators for California: appraisal payoff, ACV holdback, roof area, earthquake deductible and rebuild cost checks.",
                              body, [itemlist(items)], photo="calculator", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("The appraisal process", PROCESS), ("Appraisal questions", FAQ_P), ("Claim terms defined", GLOSS), ("Appraisal playbook", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("The appraisal process", path)]
    steps = "".join(f'<li><b>{e(n)}</b><span>{e(d)}</span></li>' for n, d in PROCESS_STEPS)
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in California, Step by Step",
                     "Eight stages, from the first disagreement to a filed award: what happens, who does what, and where files most often go wrong.", "clipboard",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Award", "Any 2 of 3")]) + f"""
<div class="wrap two-col"><article class="prose"><ol class="step-summary">{steps}</ol>{PROCESS_BODY}</article>
{aside(call_box(), list_box("Learn", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in California", "description": "The eight stages of a California property insurance appraisal under the standard appraisal clause.", "totalTime": "P90D",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d, "url": f"{DOMAIN}{path}#main"} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in California | 8 Steps",
                         "The insurance appraisal process in California step by step: the written demand, 20-day appraiser window, umpire selection and the award.",
                         body, [howto], photo="clipboard", trail=trail), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal questions", path)]
    nav = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions from California Owners",
                     "Plain answers grouped by topic: appraisal basics, costs, deadlines, California rules and working with us.", "living-room") + f"""
<div class="wrap two-col"><article class="prose"><nav class="toc" aria-label="FAQ topics">{nav}</nav>{groups}</article>
{aside(call_box(), list_box("Learn", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email and we’ll talk it through.")}"""
    write(path, document(path, "Insurance Appraisal Questions | California FAQ",
                         "Insurance appraisal questions answered for California owners: basics, fees, the 20-day and 15-day windows, FAIR Plan and earthquake rules.",
                         body, [faq_schema(allq)], photo="living-room", trail=trail), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim terms defined", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms Defined in Plain English",
                     f"{len(GLOSSARY)} terms you’ll meet in California policies, estimates and appraisal awards. Type to filter.", "paper-writing", cta=False) + f"""
<div class="wrap two-col"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “FAIR Plan”" autocomplete="off"><p class="hint" data-gloss-count></p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
{aside(call_box(), list_box("Learn", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim terms defined", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Defined | Glossary of 40+ Terms",
                         "Insurance claim terms defined in plain English: ACV, holdback, FAIR Plan, DIC, extended replacement cost, umpire and more, searchable.",
                         body, [dts], photo="paper-writing", trail=trail), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Appraisal playbook", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap two-col"><article class="prose">{p["body"]}<p class="byline">Written by the {BRAND} team. General information, not legal advice.</p><h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
{aside(call_box(), list_box("Learn", LEARN), list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], og_type="article", photo=ph, trail=trail), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Appraisal playbook", path)]
    cards = "".join(photo_card(f'{POST_BASE}{p["slug"]}/', POST_PHOTO[p["slug"]], f'{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]}', p["title"], p["summary"], h="h2") for p in POSTS)
    body = page_hero(trail, "Guides", "The Appraisal Playbook for California Policyholders",
                     "Practical guides on policy language, wildfire claims, smoke, FAIR Plan policies and reading estimates.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Appraisal Playbook | California Claim Guides",
                         "The appraisal playbook: California claim guides on the §2071 appraisal clause, wildfire total losses, smoke, FAIR Plan and estimates.",
                         body, [itemlist([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="kitchen", page_type="CollectionPage", trail=trail), 0.7)


# ---------------------------------------------------------------- firm & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About the firm", path)]
    body = page_hero(trail, "About the firm", "About California Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "clipboard-site") + f"""
<div class="wrap two-col"><article class="prose">
<figure class="lead-img">{img("consult", sizes="(max-width:960px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. We specialize. California Insurance Appraiser works on one question, the amount of loss, and we’ve built our process, tools and documentation standards around answering it well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll tell you.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know what it costs.</li>
</ul>
<h2>Independence</h2>
<p>California’s standard appraisal clause requires each appraiser to be competent and disinterested. We disclose prior relationships with the carrier, the other appraiser and the umpire, and we decline files where we have a conflict.</p>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, business owners, churches, contractors, public adjusters and attorneys throughout California. On any one claim we serve in one role only.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t guarantee outcomes, and no honest appraiser can.</p>
<h2>Statewide, on purpose</h2>
<p>California’s claims change with the landscape: wildfire in the foothills and canyons, atmospheric-river leaks in the valleys, Santa Ana winds in the south, shared-wall water losses in the cities. Working in all 58 counties means we see every kind of loss the state produces and price each one with local knowledge.</p>
</article>{aside(call_box(), list_box("Explore", [("Our services", SVC_BASE), ("City coverage", LOC_BASE), ("Free tools", TOOL_BASE), ("The appraisal process", PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, "About the Firm | California Insurance Appraiser",
                         "About California Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss on disputed claims.",
                         body, [], photo="clipboard-site", page_type="AboutPage", trail=trail), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Contact", "Contact California Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult", cta=False) + f"""
<section class="sec dark"><div class="wrap duo duo-top">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="c-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Pacific</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>All 58 California counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks light"><li>{ic("check")}Declarations page</li><li>{ic("check")}The carrier’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the carrier</li><li>{ic("check")}Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Us | California Insurance Appraiser",
                         "Contact California Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427 or send your details.",
                         body, [], photo="consult", page_type="ContactPage", trail=trail), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | California Insurance Appraiser",
                  "Privacy policy for California Insurance Appraiser: what we collect through forms, calls and email, how we use it and your California rights.",
                  "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect the information you choose to provide, such as your name, phone number, email address, property location and details about your claim. Our web host records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell or share your personal information for cross-context behavioral advertising. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when required by law.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data. If we add analytics, this policy will be updated to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your California privacy rights</h2><p>Depending on how the law applies to us, California residents may have rights to know, delete and correct personal information and to opt out of its sale or sharing. To make a request, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We won’t discriminate against you for exercising these rights.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "Terms of Use | California Insurance Appraiser",
                "Terms of use for the California Insurance Appraiser website and its free claim tools, including limits on reliance and no legal advice.",
                "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in California.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a California attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any outcome.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of California.</p>"""),
        DISCLAIMER: ("Disclaimer", "Legal Disclaimer | California Insurance Appraiser",
                     "Legal disclaimer for California Insurance Appraiser: general information only, no legal advice, no guaranteed results and illustrative figures.",
                     "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>Statutes and regulations</h2><p>References to the California Insurance Code, the Fair Claims Settlement Practices Regulations and other rules are general summaries for context. Laws change, and their application depends on facts. Check current law with official sources such as the California Department of Insurance, or ask an attorney.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies and statutes contain deadlines for notice, proof of loss, replacement cost recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a California attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office", cta=False) + f'<div class="wrap two-col"><article class="prose">{content}</article>{aside(call_box())}</div>'
        write(path, document(path, title, desc, body, [], photo="office", trail=trail), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("All pages", path)]
    groups = [
        ("Main", [("Home", "/"), ("About the firm", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("City coverage", [("All cities", LOC_BASE)] + [(f'{l["city"]}, CA', loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIMER)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    allp = [x for _, links in groups for x in links]
    body = page_hero(trail, "Navigation", "All Pages on California Insurance Appraiser", "Every page on the site, grouped by section.", "office", cta=False) + f'<section class="sec"><div class="wrap map-grid">{cols}</div></section>'
    write(path, document(path, "All Pages | California Insurance Appraiser Site Map",
                         "Site map listing every page on California Insurance Appraiser: services, California city coverage, free claim tools, guides and legal pages.",
                         body, [itemlist(allp)], photo="office", page_type="CollectionPage", trail=trail), 0.3)

    body = f"""<section class="p-hero p-404"><div class="p-hero-img">{img("storm-clouds", lazy=False, alt="")}</div><div class="wrap p-hero-in"><p class="kicker light">Error 404</p><h1>That page isn’t here</h1><p class="lede">It may have moved, or the link may be mistyped. These are good places to start.</p><div class="btn-row"><a class="btn btn-copper" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Services</a><a class="btn btn-line light" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "Page not found on California Insurance Appraiser. The link may be old or mistyped; try our services, free claim tools or contact page.",
                                body, robots="noindex,follow", photo="storm-clouds", trail=[("Home", "/"), ("Page not found", "/404.html")]), sitemap=False)


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
    # Google Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "w", encoding="utf-8", newline="") as f:
        f.write(GSC_BODY)


GUARD_PHP = r"""<?php
// California Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$cia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$cia_real  = 'californiainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$cia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://californiainsuranceappraiser.com - only on the real domain.
if ($cia_host === 'www.' . $cia_real || ($cia_host === $cia_real && $cia_proto === 'http')) {
    header('Location: https://' . $cia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $cia_m)) {
    $cia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $cia_m[1] . $cia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($cia_host !== $cia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// California Insurance Appraiser - front controller for the static build.
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
