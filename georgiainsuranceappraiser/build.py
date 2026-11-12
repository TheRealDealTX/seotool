#!/usr/bin/env python3
"""Static site generator for georgiainsuranceappraiser.com.

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

BRAND = "Georgia Insurance Appraiser"
DOMAIN = "https://georgiainsuranceappraiser.com"
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@georgiainsuranceappraiser.com"
TODAY = date.today().isoformat()
VER = "20261107b"
FAV = "3"

SVC_BASE = "/appraisal-services/"
LOC_BASE = "/locations/"
TOOL_BASE = "/claim-tools/"
POST_BASE = "/insights/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-ga/"


def loc_label(l):
    return f"{l['city']}, GA"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-home-after-rain": "Two-story Georgia-style home with a wet driveway after a storm",
    "house-dusk": "Suburban family home lit up at dusk",
    "storm-clouds": "Dark storm clouds building over open country",
    "lightning-storm": "Lightning strikes during a severe thunderstorm at night",
    "coastal-storm": "Storm clouds rolling in over a beach and surf",
    "storm-horizon": "Storm front over farm fields at sunset",
    "roof-gable": "Dark shingle roof gable against the sky",
    "metal-roof": "Corrugated metal roof on a commercial building",
    "roof-tiles": "Close-up of roof shingles in rows",
    "plans-review": "Two contractors in safety vests reviewing construction plans",
    "clipboard-notes": "Contractor writing notes on a clipboard at a job site",
    "contractor": "Construction worker in a hard hat and safety vest on site",
    "consultation": "Two professionals in a consultation at a table by the window",
    "consultation-laptop": "Two women reviewing documents on a laptop",
    "laptop-calculator": "Hands using a calculator next to a laptop spreadsheet",
    "calculator-documents": "Person calculating figures with a calculator and paperwork",
    "calculator-desk": "Calculator, glasses and pen on a white desk",
    "glass-building": "Modern glass office building against a blue sky",
    "commercial-lobby": "Commercial office building lobby lit at night",
    "atlanta-skyline": "Aerial view of the Atlanta, Georgia skyline",
    "savannah-bridge": "Sunset over the Savannah River and Talmadge Bridge in Savannah, Georgia",
    "roof-torn-off": "House with its roof torn open after a severe storm",
    "storm-debris-home": "Home surrounded by downed trees and debris after a tornado",
    "tornado-debris": "Homes and debris scattered across a neighborhood after a tornado",
    "trees-down": "Trees blown down across a path after a hurricane",
    "house-fire": "House engulfed in flames at night",
    "rain-window": "Heavy rain running down a window pane",
    "kitchen": "Bright kitchen with sink and counters",
    "living-room": "Living room with sofa and cushions in a family home",
    "modern-kitchen": "Modern kitchen with island and pendant lights",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-representation": "consultation", "homeowner-claim-appraisal": "house-dusk",
    "commercial-claim-appraisal": "commercial-lobby", "hail-roof-claim-appraisal": "roof-gable",
    "wind-tornado-damage-appraisal": "roof-torn-off", "hurricane-tropical-storm-appraisal": "coastal-storm",
    "water-leak-damage-appraisal": "rain-window", "fire-smoke-claim-appraisal": "house-fire",
    "fallen-tree-damage-appraisal": "trees-down", "insurance-estimate-review": "laptop-calculator",
    "umpire-and-neutral-services": "consultation-laptop",
}
LOC_PHOTO = {
    "atlanta": "atlanta-skyline", "savannah": "savannah-bridge", "augusta": "storm-horizon", "columbus": "lightning-storm",
    "macon": "storm-debris-home", "athens": "house-dusk", "marietta": "roof-tiles", "alpharetta": "hero-home-after-rain",
    "albany": "tornado-debris", "valdosta": "storm-clouds", "warner-robins": "metal-roof", "brunswick": "coastal-storm",
}
TOOL_PHOTO = {
    "appraisal-value-estimator": "calculator-documents", "depreciation-holdback-calculator": "calculator-desk",
    "roof-squares-pitch-calculator": "roof-tiles", "wind-hail-deductible-calculator": "storm-clouds",
    "claim-deadline-planner": "clipboard-notes", "appraisal-readiness-score": "plans-review",
}
POST_PHOTO = {
    "georgia-appraisal-clause-explained": "consultation", "appraiser-vs-public-adjuster-vs-attorney": "consultation-laptop",
    "documenting-hail-damage-in-georgia": "roof-gable", "when-not-to-invoke-appraisal": "calculator-desk",
    "reading-your-insurance-estimate": "laptop-calculator",
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
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-clause-representation": "doc", "homeowner-claim-appraisal": "home", "commercial-claim-appraisal": "building",
    "hail-roof-claim-appraisal": "hail", "wind-tornado-damage-appraisal": "wind", "hurricane-tropical-storm-appraisal": "storm",
    "water-leak-damage-appraisal": "drop", "fire-smoke-claim-appraisal": "flame", "fallen-tree-damage-appraisal": "tree",
    "insurance-estimate-review": "file", "umpire-and-neutral-services": "scale",
}


def mark(uid="m"):
    return (f'<svg viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#a62d4a"/><stop offset="1" stop-color="#43111f"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="12" fill="url(#{uid})"/>'
            '<path d="M24 8.5l13 4.8v9.6c0 8-5.4 14-13 17.3-7.6-3.3-13-9.3-13-17.3v-9.6z" fill="none" stroke="#f3cf8e" stroke-width="3.2" stroke-linejoin="round"/>'
            '<path d="M18 24.6l4.4 4.4 8-9" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "GA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-GA", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid property claims",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims throughout Georgia.",
        "areaServed": [{"@type": "State", "name": "Georgia"}] + [{"@type": "City", "name": l["city"].split(" &")[0]} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Hail damage", "Hurricane claims"],
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
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("Statewide coverage", LOC_BASE), True),
        ("Claim Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Learn", [("How appraisal works", "/how-appraisal-works/"), ("Appraisal FAQ", "/appraisal-faq/"), ("Claim glossary", "/claim-glossary/"), ("Insights & guides", POST_BASE)], None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="full"><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="mega{" cols" if cols else ""}">{li}</ul></li>'
    menu += '<li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += '<li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="topbar"><div class="wrap"><span><i class="pulse"></i>Independent property claim appraisal · All 159 Georgia counties</span>
<div class="topbar-r"><a class="hide-s" href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></div></div></div>
<header class="head"><div class="wrap">
<a class="brand" href="/" aria-label="{BRAND} home">{mark("mh")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn head-cta" href="tel:{TEL}">{ic("phone")} Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark("md")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a><button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost" href="/contact/">Send claim details</a><small>Mon–Fri 8am–6pm ET · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-cta"><h2>Underpaid claim? Let’s look at the numbers together.</h2><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn glass" href="/contact/">Send claim details</a></div></div>
<div class="foot-top">
<div><a class="brand" href="/">{mark("mf")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal and estimating support for property owners with disputed insurance claims, from the North Georgia mountains to the Golden Isles.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET · Statewide</span></div></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Locations</h3><ul>{loc}<li><a href="{LOC_BASE}">All Georgia</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Company</h3><ul><li><a href="/about/">About</a></li><li><a href="/how-appraisal-works/">How appraisal works</a></li><li><a href="/appraisal-faq/">FAQ</a></li><li><a href="/claim-glossary/">Glossary</a></li><li><a href="{POST_BASE}">Insights</a></li><li><a href="/contact/">Contact</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="/privacy-policy/">Privacy</a></li><li><a href="/terms-of-use/">Terms</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="/site-map/">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not provide legal advice and are not acting as a public adjuster. Information on this site is general and educational; policy terms vary. Results depend on the facts of each claim and are never guaranteed.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">Call now</a><a href="/contact/">Free review</a></div>"""


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
        if t in ("FAQPage",):
            n["@id"] = canonical + "#faq"
        if t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = preload or "hero-home-after-rain"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet")]
    if main:
        webpage["mainEntity"] = {"@id": main[0]}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<!-- Google Tag Manager -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-K6P2TP3Z"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<!-- End Google Tag Manager -->
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal in Georgia">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="geo.region" content="US-GA">
<meta name="theme-color" content="#5c1628">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="on-hero">
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K6P2TP3Z" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
{header()}
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts fade-up" style="animation-delay:.35s">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row fade-up" style="animation-delay:.25s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="/contact/">Free claim review</a></div>' if cta else ""
    return f"""<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.12"')}<div class="orb o1"></div><div class="grain"></div><div class="wrap">{crumbs(trail)}<span class="eyebrow light fade-up">{e(tag)}</span><h1 class="fade-up" style="animation-delay:.08s">{e(h1)}</h1><p class="lede fade-up" style="animation-delay:.16s">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div class=\"a\"><p>{a}</p></div></details>" for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk through your claim</h2><p>Free initial conversation. We’ll tell you honestly whether appraisal fits.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold" href="/contact/">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span>›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Have a claim that doesn’t add up?", p="Send us the carrier’s estimate. We’ll review it and tell you what we see."):
    return f"""<section class="cta-band"><div class="wrap"><div class="in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn glass" href="/contact/">Email the estimate</a></div></div></div></section>"""


LOSSES = ["Hail", "Wind / tornado", "Hurricane / tropical storm", "Water / leak", "Fire / smoke", "Fallen tree", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", sub="Free review. No obligation. Usually a reply within one business day.", page="/"):
    roles = ["Homeowner", "Commercial owner", "Property manager / HOA", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Georgia"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="/privacy-policy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow", "ar")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def mini_form():
    return f"""<form class="glass-card mini-form fade-up" style="animation-delay:.5s" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Free claim review</h2><p class="sub">Tell us a little. We’ll call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="/privacy-policy/">privacy policy</a>.</span></label>
<button class="btn gold" type="submit">Request my free review {ic("arrow", "ar")}</button>
<div class="form-msg" role="status"></div>
<div class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("north", "North Georgia Mountains", "Dalton · Blue Ridge · Dahlonega", ["Ice & snow load", "Frozen pipes", "Ridgeline wind", "Falling hardwoods"],
     "Elevation brings winter weather the rest of the state rarely sees. Ice-laden limbs, collapsed gutters and burst pipes in seasonal cabins are the claims we see most in Rabun, Union, Fannin, Gilmer and Whitfield counties.",
     "Rome, Dalton, Calhoun, Blue Ridge, Ellijay, Dahlonega", "storm-clouds"),
    ("metro", "Metro Atlanta", "Atlanta · Marietta · Alpharetta", ["Hail", "Severe storms", "Tornadoes", "Water losses"],
     "The busiest claim market in the Southeast. Spring hail tracks through Cobb, Cherokee, Gwinnett and North Fulton, while in-town neighborhoods add historic homes and high-rise condos to the mix.",
     "Atlanta, Marietta, Alpharetta, Sandy Springs, Roswell, Lawrenceville, Decatur", "atlanta-skyline"),
    ("piedmont", "Piedmont & Middle Georgia", "Athens · Macon · Columbus", ["Tornadoes", "Straight-line winds", "Tree damage", "Fire"],
     "Spring squall lines strengthen across the Piedmont. Mature oaks over historic homes in Macon and Athens mean tree impacts are as common as roof damage.",
     "Athens, Macon, Columbus, Warner Robins, Milledgeville, LaGrange", "lightning-storm"),
    ("south", "South & Southwest Georgia", "Albany · Valdosta · Tifton", ["Hurricanes", "Fallen pines", "Farm structures", "Tornadoes"],
     "Gulf hurricanes cross this region with surprising strength. Pine forests, pecan orchards and farm outbuildings create claims that blend residential, agricultural and commercial coverage.",
     "Albany, Valdosta, Tifton, Thomasville, Moultrie, Americus", "trees-down"),
    ("coast", "Coastal Georgia", "Savannah · Brunswick · St. Marys", ["Named storms", "Wind-driven rain", "Mold", "Condo losses"],
     "Named-storm deductibles, wind-versus-flood questions and historic buildings define coastal claims from Chatham County to Camden County.",
     "Savannah, Brunswick, St. Simons Island, Richmond Hill, Kingsland, St. Marys", "savannah-bridge"),
]


def home():
    words = "Georgia Insurance Appraiser for <span class=\"grad-text\">underpaid</span> property claims".split(" ")
    h1, d, i = [], 0.15, 0
    while i < len(words):
        w = words[i]
        if w.startswith("<span"):
            w = w + " " + words[i + 1]
            i += 1
        h1.append(f'<span class="w" style="animation-delay:{d:.2f}s">{w}</span>')
        d += 0.07
        i += 1
    h1 = " ".join(h1)

    perils = ["Hail damage", "Tornado losses", "Hurricane claims", "Fallen trees", "Burst pipes", "Fire & smoke", "Commercial roofs", "Condo & HOA", "Wind-driven rain", "Estimate reviews"]
    marquee = "".join(f"<span><i></i>{p}</span>" for p in perils * 2)

    big = SERVICES[0], SERVICES[3]
    wide = SERVICES[5], SERVICES[4]
    pc = lambda s, cls, tag: f'<a class="pcard {cls} rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 50vw", alt="")}<span class="tagp">{tag}</span><span class="go">{ic("arrow")}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></a>'
    sc = lambda s: f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/"><span class="ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></a>'
    rest = [s for s in SERVICES if s not in big + wide]
    bento = pc(big[0], "big", "Core service") + pc(big[1], "", "Most requested") + pc(wide[1], "", "Storm") + pc(wide[0], "wide", "Coastal & inland") + "".join(sc(s) for s in rest)

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 1 else "false"}" tabindex="{0 if i == 1 else -1}">{e(n)}<small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 1 else " hidden"}>{img(ph, sizes="(max-width:1020px) 100vw, 800px", alt="")}<div class="in"><h3>{e(n)}</h3><ul class="peril-chips">{"".join(f"<li>{e(p)}</li>" for p in perils_)}</ul><p>{e(t)}</p><p class="cities">Communities: {e(c)}</p></div></div>'
        for i, (k, n, _s, perils_, t, c, ph) in enumerate(REGIONS))

    tiles = "".join(f'<a class="tile rv" data-tilt href="{TOOL_BASE}{t["slug"]}/"><div class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="kind">{t["kind"]}</span><span class="ico">{t["icon"]}</span></div><div class="tb"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open tool</span></div></a>' for t in TOOLS)
    cities = "".join(f'<a class="rv" href="{loc_path(l)}"><span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span>{ic("arrow")}</a>' for l in LOCATIONS)
    posts = "".join(f'<article class="post rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pb"><span class="meta">{p["read"]} read · Guide</span><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="link" href="{POST_BASE}{p["slug"]}/">Read guide</a></div></article>' for p in POSTS[:3])

    steps = [
        ("Free claim review", "We read your policy, the carrier’s estimate and your photos, then tell you plainly whether appraisal fits your situation."),
        ("Independent valuation", "On-site inspection, measurements and a line-item Xactimate estimate priced for your Georgia ZIP code."),
        ("Written demand", "Appraisal is invoked in writing and Georgia Insurance Appraiser is named as your appraiser within the policy deadline."),
        ("Panel negotiation", "We work line by line with the carrier’s appraiser. Most disputes narrow sharply at this stage."),
        ("Binding award", "Unresolved items go to a neutral umpire. Two signatures set the amount of loss and payment follows."),
    ]
    proc = "".join(f'<div class="pstep"><span class="num">{i + 1:02d}</span><div class="body rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></div>' for i, (t, p) in enumerate(steps))

    home_faqs = [
        ("What does a Georgia Insurance Appraiser actually do?", "We value property damage when you and your insurer agree a loss is covered but disagree on the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is this different from a public adjuster?", "A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("When should I call a Georgia Insurance Appraiser?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful — generally more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign. That’s why documentation matters so much before you invoke appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work starts, and our first conversation is free."),
        ("Do you serve my part of Georgia?", "Yes. We work statewide across all 159 counties, with regular work in metro Atlanta, Savannah, Augusta, Columbus, Macon, Athens and South Georgia."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home-after-rain", lazy=False, alt="")}</div><div class="orb o1"></div><div class="orb o2"></div><div class="grain"></div>
<div class="wrap">
<div>
<span class="eyebrow light fade-up">Independent claim appraisal · Statewide</span>
<h1>{h1}</h1>
<p class="lede fade-up" style="animation-delay:.6s">When your carrier accepts the claim but the check won’t cover the repair, Georgia Insurance Appraiser builds an independent, line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<div class="btn-row fade-up" style="animation-delay:.75s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="#services">Explore services {ic("arrow", "ar")}</a></div>
<ul class="chips fade-up" style="animation-delay:.9s"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Xactimate pricing by ZIP</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{mini_form()}
</div>
<span class="scroll-cue" aria-hidden="true"></span>
</section>

<section class="stats" aria-label="At a glance"><div class="wrap"><div class="stats-in">
<div class="stat"><b class="grad-text-m" data-count="159">159</b><span>Georgia counties served</span></div>
<div class="stat"><b class="grad-text-m" data-count="11">11</b><span>Appraisal &amp; estimating services</span></div>
<div class="stat"><b class="grad-text-m" data-count="6">6</b><span>Free claim tools</span></div>
<div class="stat"><b class="grad-text-m">2 of 3</b><span>Signatures make the award binding</span></div>
</div></div></section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="sec" style="padding-top:60px"><div class="wrap split">
<div class="collage rv-l">
<figure class="c1">{img("plans-review", sizes="(max-width:1020px) 90vw, 480px")}</figure>
<figure class="c2">{img("roof-gable", sizes="(max-width:1020px) 60vw, 360px")}</figure>
<div class="badge-float"><span class="ic">{ic("shield")}</span><div><b>Independent &amp; statewide</b><span>Retained by you, not the carrier</span></div></div>
</div>
<div class="rv-r">
<span class="eyebrow">Why owners call us</span>
<h2>Why property owners call a <span class="grad-text-m">Georgia Insurance Appraiser</span></h2>
<p>Most underpaid claims aren’t denied — they’re just short. A missing roof slope, a mismatched floor, a code item nobody priced. Georgia Insurance Appraiser exists for that gap between “covered” and “paid in full.”</p>
<ul class="checks">
<li>{ic("check")}<div><b>We value the loss from scratch</b><span>Our own inspection and measurements — never an edited copy of the carrier’s estimate.</span></div></li>
<li>{ic("check")}<div><b>Defensible, not inflated</b><span>Numbers built to hold up in front of an umpire, so they actually move the award.</span></div></li>
<li>{ic("check")}<div><b>Honest triage</b><span>If your claim needs an attorney or a supplement instead, we’ll tell you on the first call.</span></div></li>
</ul>
<a class="btn" href="/about/">About our approach {ic("arrow", "ar")}</a>
</div>
</div>
<div class="wrap fit" data-stagger>
<div class="rv"><h3><i>✓</i>When appraisal fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair vs. replace disagreements</li><li>Matching and discontinued materials</li><li>Missing trades, code items and O&amp;P</li></ul></div>
<div class="rv no"><h3><i>✕</i>When it doesn’t</h3><ul><li>Outright coverage denials</li><li>Bad-faith or legal claims</li><li>Gaps too small to justify fees</li><li>Deadlines that need an attorney first</li></ul></div>
</div></section>

<section class="sec blush" id="services"><div class="wrap">
<div class="head-c rv"><span class="eyebrow">Appraisal &amp; estimating</span><h2>What Georgia Insurance Appraiser does for your claim</h2><p>Eleven services built around one job: producing a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="bento" data-stagger>{bento}</div>
<p style="text-align:center;margin-top:40px"><a class="btn ghost" href="{SVC_BASE}">Compare all appraisal services {ic("arrow", "ar")}</a></p>
</div></section>

<section class="sec maroon" id="check"><div class="wrap split">
<div class="rv-l"><span class="eyebrow light">Quick gap check</span><h2>Is your gap worth an appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a Georgia Insurance Appraiser makes sense. If it’s small, a documented supplement request may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}appraisal-value-estimator/">appraisal value estimator</a> adds appraiser and umpire fees so you can see a realistic net figure.</p><a class="btn gold" href="{TOOL_BASE}">See all six free tools {ic("arrow", "ar")}</a></div>
<div class="rv-r">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="head-c rv"><span class="eyebrow">The process</span><h2>How appraisal moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how Georgia Insurance Appraiser takes a file from first call to signed award.</p></div>
<div class="process"><span class="fill"></span>{proc}</div>
<p style="text-align:center;margin-top:40px"><a class="link" href="/how-appraisal-works/">Read the full appraisal process guide</a></p>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="head-l rv"><span class="eyebrow light">Statewide knowledge</span><h2>One state, five very different claim climates</h2><p>Ice in Blue Ridge, hail in Marietta, tornadoes in Macon, hurricanes in Valdosta and Brunswick. A Georgia Insurance Appraiser has to know how each region’s weather shows up on a roof — and in an estimate.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="Georgia regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec blush"><div class="wrap">
<div class="head-c rv"><span class="eyebrow">Free &amp; private</span><h2>Free claim tools built by a Georgia Insurance Appraiser</h2><p>Run the numbers before you pick up the phone. Every tool works in your browser — nothing is stored or sent.</p></div>
<div class="tiles" data-stagger>{tiles}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="loc-banner rv-s">{img("atlanta-skyline", sizes="100vw", alt="", extra=' data-parallax="0.1"')}<div class="in"><span class="eyebrow light">Statewide coverage</span><h3>Georgia Insurance Appraiser locations</h3><p>We serve every county in the state. These are the communities where Georgia Insurance Appraiser handles claims most often.</p></div></div>
<div class="cities-grid" data-stagger>{cities}</div>
<p style="text-align:center;margin-top:36px"><a class="link" href="{LOC_BASE}">See statewide coverage</a></p>
</div></section>

<section class="sec white"><div class="wrap">
<div class="head-c rv"><span class="eyebrow">Choosing help</span><h2>Appraiser, public adjuster or attorney?</h2><p>Each one solves a different problem. Picking the right help first saves time and fees — and Georgia Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="table-wrap rv"><table><thead><tr><th>Question</th><th class="hl">Georgia Insurance Appraiser</th><th>Public adjuster</th><th>Attorney</th></tr></thead><tbody>
<tr><th>Main job</th><td class="hl">Value the amount of loss</td><td>Manage &amp; negotiate the claim</td><td>Legal disputes &amp; litigation</td></tr>
<tr><th>Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th>Result</th><td class="hl">Binding award (2 of 3 signatures)</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th>Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec blush"><div class="wrap split top">
<div class="rv-l"><span class="eyebrow">FAQ</span><h2>Questions people ask a Georgia Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:24px"><a class="btn" href="/appraisal-faq/">All FAQs {ic("arrow", "ar")}</a><a class="btn ghost" href="/claim-glossary/">Claim glossary</a></div></div>
<div class="rv-r">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="head-c rv"><span class="eyebrow">Guides</span><h2>Read before you invoke appraisal</h2><p>Practical guides from the Georgia Insurance Appraiser team on policy language, documentation and strategy.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="cta-photo">{img("storm-clouds", "bg", alt="", extra=' data-parallax="0.18"')}<div class="wrap rv"><span class="eyebrow light">Storm season is claim season</span><h2>The best time to check your numbers is before you sign off on them</h2><p>A short review now can save you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="#contact">Send your estimate</a></div></div></section>

<section class="sec dark" id="contact"><div class="wrap contact">
<div class="rv-l"><span class="eyebrow light">Start with a conversation</span><h2>Talk to a Georgia Insurance Appraiser about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call / text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Coverage</span><b>All 159 Georgia counties</b></div></li></ul></div>
<div class="rv-r">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Georgia Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, hurricane, water and fire claims.",
                        body, schema, preload="hero-home-after-rain"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [x for x in SERVICES if x is not s][:3]
        related = "".join(f'<a href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All Georgia locations", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Georgia"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="index-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 240px", alt="")}</span><span class="ib"><span class="k">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Georgia Property Claims",
                     "From a single estimate review to full panel representation and neutral umpire work, every Georgia Insurance Appraiser service is built around an accurate, defensible valuation of your loss.", "contractor") + f"""
<section class="sec"><div class="wrap"><div class="index-list" data-stagger>{cards}</div></div></section>
<section class="sec blush"><div class="wrap split top"><div class="rv-l"><span class="eyebrow">Not sure where to start?</span><h2>Most claims begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review gives you that answer in days, and many disputes close at that stage.</p><a class="btn" href="{SVC_BASE}insurance-estimate-review/">About estimate reviews {ic("arrow", "ar")}</a></div><div class="rv-r">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you work on both residential and commercial claims?", "Yes — houses, condos, multifamily, retail, office, industrial, churches and HOA properties."), ("Do you only work on hail claims?", "No. We handle wind, hurricane, water, fire, tree and other covered perils.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{SVC_BASE}{s["slug"]}/', "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Georgia | Claim Valuation",
                             "Georgia insurance appraisal services: appraisal clause representation, estimate review, storm, water, fire and tree claims, plus umpire work.",
                             body, schema, preload="contractor"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f'<li style="background:var(--maroon)">{e(p)}</li>' for p in l["perils"])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Coverage", "On-site inspections")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks</b><ul class="peril-chips" style="margin:10px 0 0">{chips}</ul></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Georgia locations", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        city = l["city"].split(" &")[0]
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "Georgia"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser {city}, GA | Disputed Claim Appraisal"
        if len(title) > 56:
            title = f"Insurance Appraiser {city}, GA | Claim Appraisal"
        desc = f"Independent insurance appraiser for {city} and {l['county']}. Appraisal and estimate review for underpaid storm, water and fire claims."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cities = "".join(f'<a class="rv" href="{loc_path(l)}"><span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span>{ic("arrow")}</a>' for l in LOCATIONS)
    reg = "".join(f'<div class="index-card rv"><span class="ph">{img(ph, sizes="(max-width:700px) 100vw, 240px", alt="")}</span><span class="ib"><span class="k">{e(s)}</span><h2>{e(n)}</h2><p>{e(t)}</p><p style="margin-top:10px;font-size:.88rem;color:var(--muted)">{e(c)}</p></span></div>' for k, n, s, _p, t, c, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 159 Georgia Counties",
                     "Georgia Insurance Appraiser works statewide — from the Tennessee line to the St. Marys River. These local pages cover the cities where we handle claims most often.", "atlanta-skyline") + f"""
<section class="sec"><div class="wrap"><div class="cities-grid" data-stagger>{cities}</div></div></section>
<section class="sec blush"><div class="wrap"><div class="head-l rv"><span class="eyebrow">Regions</span><h2>How claims differ across Georgia</h2><p>The same policy language plays out very differently in a mountain cabin, a Buckhead condo and a Golden Isles beach house.</p></div><div class="index-list" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your city?", "We cover every Georgia county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Georgia Insurance Appraiser Locations | Statewide",
                             "Insurance appraisal in all 159 Georgia counties, including Atlanta, Savannah, Augusta, Columbus, Macon, Athens, Albany, Valdosta and Brunswick.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + loc_path(l), "name": loc_label(l)} for i, l in enumerate(LOCATIONS)]}], preload="atlanta-skyline"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{TOOL_BASE}{o["slug"]}/"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [x for x in TOOLS if x is not t][:3])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tight" style="padding-bottom:0"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms, and aren’t a quote, appraisal or legal advice.</p></div></section>
<div class="wrap layout" style="padding-top:40px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All claim tools", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    tiles = "".join(f'<a class="tile rv" data-tilt href="{TOOL_BASE}{t["slug"]}/"><div class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="kind">{t["kind"]}</span><span class="ico">{t["icon"]}</span></div><div class="tb"><h2 style="font-size:1.18rem">{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open tool</span></div></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Georgia Property Owners",
                     "Six calculators and planners built from real appraisal work. Use them to understand your claim, check the carrier’s math and decide on next steps — no sign-up, nothing stored.", "laptop-calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tiles" data-stagger>{tiles}</div></div></section>
<section class="sec blush"><div class="wrap split top"><div class="rv-l"><span class="eyebrow">Suggested order</span><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-deadline-planner/">deadline planner</a> so nothing lapses.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-squares-pitch-calculator/">squares &amp; pitch calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}wind-hail-deductible-calculator/">deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-calculator/">depreciation</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-value-estimator/">appraisal value estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-score/">readiness score</a>.</li></ol></div><div class="rv-r">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{TOOL_BASE}{t["slug"]}/', "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators & Tools for Georgia",
                              "Free property claim tools: appraisal value estimator, depreciation, roof squares and wind/hail deductible calculators, deadline planner and more.",
                              body, schema, preload="laptop-calculator"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("How appraisal works", "/how-appraisal-works/"), ("Appraisal FAQ", "/appraisal-faq/"), ("Claim glossary", "/claim-glossary/"), ("Insights & guides", POST_BASE)]

    path = "/how-appraisal-works/"
    trail = [("Home", "/"), ("How appraisal works", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Georgia, Step by Step",
                     "Seven stages, from the first disagreement to a signed award — what happens, who does what, and where claims most often go wrong.", "clipboard-notes",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Georgia", "step": [{"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(["The disagreement", "The written demand", "Both sides name appraisers", "Choosing an umpire", "Negotiation between appraisers", "Umpire review", "The award"])]}
    write(path, document(path, "How Insurance Appraisal Works in Georgia | 7 Steps",
                         "Step-by-step guide to Georgia insurance appraisal: the written demand, choosing appraisers and an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], preload="clipboard-notes"), 0.8)

    path = "/appraisal-faq/"
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    groups = "".join(f'<h2>{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for Georgia Property Owners",
                     "Plain answers to the questions we hear most — about the appraisal process, costs, timing and how Georgia rules fit in.", "living-room") + f"""
<div class="wrap layout"><article class="prose">{groups}</article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email — we’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Costs, Timing & Georgia Rules",
                         "Answers to common Georgia insurance appraisal questions: how it works, what it costs, how long it takes and when the award is binding.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="living-room"), 0.8)

    path = "/claim-glossary/"
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll see in policies, estimates and appraisal awards, defined in plain English.", "calculator-documents", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Filter terms</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More Defined",
                         "Plain-English definitions of property insurance claim terms: actual cash value, replacement cost, depreciation, appraisal award, umpire, O&P and more.",
                         body, [crumbs_schema(trail), dts], preload="calculator-documents"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Insights", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [x for x in POSTS if x is not p][:3])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Learn", learn_items)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Insights", path)]
    cards = "".join(f'<article class="post rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pb"><span class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</span><h2 style="font-size:1.25rem;margin:8px 0 10px"><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="link" href="{POST_BASE}{p["slug"]}/">Read guide</a></div></article>' for p in POSTS)
    body = page_hero(trail, "Insights & guides", "Insurance Appraisal Insights for Georgia Property Owners",
                     "Practical guides on policy language, documentation and claim strategy, written by people who work appraisal panels.", "modern-kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Insights & Guides for Georgia",
                         "Guides for Georgia property owners on appraisal clauses, hail documentation, reading estimates and choosing an appraiser, adjuster or attorney.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + f'{POST_BASE}{p["slug"]}/', "name": p["title"]} for i, p in enumerate(POSTS)]}], preload="modern-kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = "/about/"
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", "About Georgia Insurance Appraiser",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.", "plans-review") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("consultation", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus only on appraisal</h2>
<p>Most property claim professionals do a little of everything. We chose to specialize. Georgia Insurance Appraiser works on one question — the amount of loss — and we’ve built our process, tools and documentation standards around answering it well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate might look good on day one, but it loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know exactly what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Georgia. On any given claim, we serve in one role only, and we disclose any prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes — no honest appraiser can.</p>
<h2>Statewide, on purpose</h2>
<p>Georgia’s weather varies dramatically between the mountains, the Piedmont, the Coastal Plain and the coast. Working statewide means we see every kind of loss the state produces — ice in Blue Ridge, hail in Marietta, tornadoes in Macon, hurricanes in Brunswick — and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Locations", LOC_BASE), ("Free tools", TOOL_BASE), ("How appraisal works", "/how-appraisal-works/")])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Us | Georgia Insurance Appraiser",
                         "Georgia Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage", "url": DOMAIN + path, "about": {"@id": DOMAIN + "/#business"}}], preload="plans-review"), 0.7)

    path = "/contact/"
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Georgia Insurance Appraiser",
                     "Call, text, email or send your claim details below. Our first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec dark"><div class="wrap contact">
<div class="rv-l"><span class="eyebrow light">Direct lines</span><h2>Reach us directly</h2>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call / text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>Statewide — all 159 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul><li>Declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv-r">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Georgia Insurance Appraiser | (844) 537-1427",
                         "Get a free review of your disputed property claim. Call or text (844) 537-1427 or email info@georgiainsuranceappraiser.com to reach us.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage", "url": DOMAIN + path}], preload="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" style=\"width:120px;height:72px;object-fit:cover;border-radius:8px\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    legal = {
        "/privacy-policy/": ("Privacy Policy", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect the information you choose to provide — such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working properly.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when required by law.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies</h2><p>This site doesn’t use advertising cookies. Fonts are loaded from Google Fonts, which may log standard request data under Google’s privacy policy.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        "/terms-of-use/": ("Terms of Use", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is provided for general information about insurance appraisal and property claims in Georgia.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Insurance policies differ, and laws and court decisions change. Consult a licensed Georgia attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators provide planning estimates based on the information you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent permitted by law, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Georgia.</p>""", "The terms that apply when you use this website and its tools."),
        "/disclaimer/": ("Disclaimer", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t provide legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any specific client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Insurance policies contain deadlines, including for notice, proof of loss, depreciation recovery and lawsuits. Information on this site doesn’t extend or alter any deadline. If a deadline is approaching, consult a Georgia attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are royalty-free stock and public-domain images used for illustration. They do not depict our clients’ properties.</p>
<h2>Third-party references</h2><p>References to statutes, agencies or weather events are for context. Verify current law and facts with official sources such as the Georgia Office of Commissioner of Insurance and Safety Fire.</p>""", "Important limits on the information published on this website."),
        "/photo-credits/": ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> (mostly via StockSnap and rawpixel) or a <strong>public-domain</strong> work such as photos by U.S. government agencies. No attribution is legally required, but we credit the photographers here with thanks. Photos are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site."),
    }
    for path, (title, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "glass-building", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", f"{title} for {BRAND} (georgiainsuranceappraiser.com): {lede}", body, [crumbs_schema(trail)], preload="glass-building"), 0.3)


def sitemap_pages():
    path = "/site-map/"
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", "/about/"), ("Contact", "/contact/")]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", [("How appraisal works", "/how-appraisal-works/"), ("Appraisal FAQ", "/appraisal-faq/"), ("Claim glossary", "/claim-glossary/"), ("Insights", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="index-card plain rv"><h2>{e(g)}</h2><ul style="padding-left:1.1em;margin:0">{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}.", "glass-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-list" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Georgia locations, free claim tools and guides.", body, [crumbs_schema(trail)]), 0.3)

    body = f"""<section class="page-hero">{img("storm-clouds", "bg", lazy=False, alt="")}<div class="grain"></div><div class="wrap"><span class="eyebrow light">Error 404</span><h1>This page blew away in the storm</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn gold" href="/">Home</a><a class="btn glass" href="{SVC_BASE}">Services</a><a class="btn glass" href="{TOOL_BASE}">Free tools</a><a class="btn glass" href="/contact/">Contact</a></div></div></section>"""
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
    with open(os.path.join(OUT, ".htaccess"), "w") as f:
        f.write("DirectoryIndex index.php\nErrorDocument 404 /404.html\nOptions -Indexes\n")


GUARD_PHP = r"""<?php
// Georgia Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$gia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$gia_real  = 'georgiainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$gia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://georgiainsuranceappraiser.com - only on the real domain.
if ($gia_host === 'www.' . $gia_real || ($gia_host === $gia_real && $gia_proto === 'http')) {
    header('Location: https://' . $gia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($gia_host !== $gia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Georgia Insurance Appraiser - front controller for the static build.
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
