#!/usr/bin/env python3
"""Static site generator for northcarolinainsuranceappraiser.com.

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
from learn import PROCESS_STEPS, PROCESS_INTRO, PROCESS_OUTRO, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "North Carolina Insurance Appraiser"
HOST = "northcarolinainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261109b"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""

SVC_BASE = "/claim-appraisal/"
LOC_BASE = "/areas-we-serve/"
TOOL_BASE = "/calculators/"
POST_BASE = "/guides/"
ABOUT, CONTACT = "/who-we-are/", "/contact-us/"
PROCESS, FAQ_P, GLOSS = "/appraisal-process-guide/", "/common-questions/", "/insurance-terms/"
PRIVACY, TERMS, DISCLAIM, CREDITS, HTMLMAP = "/privacy/", "/terms/", "/legal-disclaimer/", "/photo-credits/", "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return l["city"] if l["slug"] == "outer-banks" else f"{l['city']}, NC"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "charlotte-skyline": "Uptown Charlotte skyline above trees and a highway overpass",
    "durham-downtown": "Aerial view of downtown Durham and its ballpark",
    "winston-salem-skyline": "Downtown Winston-Salem skyline with brick smokestacks and office towers",
    "old-salem-house": "Brick 18th-century house on Main Street in Old Salem, Winston-Salem",
    "biltmore-asheville": "Biltmore Estate and gardens with the Blue Ridge behind, Asheville",
    "blue-ridge-valley": "Blue Ridge Mountains above a wooded valley near Sylva in western North Carolina",
    "cape-hatteras-lighthouse": "Black-and-white spiral Cape Hatteras Lighthouse under a blue sky",
    "outer-banks-sunrise": "Sunrise over the Atlantic surf on the Outer Banks",
    "florence-satellite": "Satellite image of Hurricane Florence approaching the East Coast in 2018",
    "florence-flooded-street": "Residential street under floodwater after Hurricane Florence",
    "flooded-neighborhood-aerial": "Aerial view of a flooded coastal neighborhood after a hurricane",
    "fallen-trees-house": "Large fallen trees on a lawn in front of a single-story house",
    "snapped-tree-campus": "Snapped tree trunk beside a brick building after Hurricane Matthew",
    "hail-street": "Hailstones covering a road and parking lot during a severe storm",
    "burned-house-aerial": "Aerial view of a house gutted by fire, with the roof burned away",
    "ice-storm-car": "Ice-coated tree limbs collapsed onto a car in front of a house",
    "snow-covered-house": "Two-story house with shrubs buried in snow after a winter storm",
    "flooded-houses": "Floodwater surrounding the porches of a row of houses",
    "water-damaged-ceiling": "Homeowner pointing to a water-stained, collapsing ceiling",
    "calculator-pencil": "Calculator, pencil and sticky note on a desk",
    "craftsman-bungalow": "Craftsman-style bungalow with a front porch and stone steps",
    "suburban-homes": "Row of suburban homes with gabled roofs and white trim",
    "brick-commercial-building": "Historic four-story brick commercial building",
    "apartment-community": "Three-story apartment community with a covered entry and parking",
    "storm-over-ridges": "Dark storm clouds and rain over a mountain ridge at sunset",
    "barn-storm-clouds": "Weathered barn under heavy storm clouds",
    "ice-storm-limb": "Ice-coated tree with a split, broken limb after an ice storm",
    "raleigh-skyline": "Downtown Raleigh skyline beyond railroad tracks",
    "cary-downtown-park": "Families on the lawn at Downtown Cary Park",
    "brick-home": "Two-story brick home with a landscaped front yard",
    "handshake-table": "Two people shaking hands across a white table",
    "meeting-laptop": "Two professionals reviewing figures on a laptop",
    "roof-shingle-tools": "Roofing nail gun and tool belt on an asphalt shingle roof",
    "roofer-at-work": "Roofer in a hard hat and safety harness hammering on a roof deck",
    "damaged-roof-tiles": "Roof with tiles torn away exposing the underlayment",
    "team-consultation": "Professional explaining figures to two colleagues at a table",
    "notes-review": "People taking notes at a wooden table during a review meeting",
    "storm-damaged-homes": "Homes and a car surrounded by debris after a severe storm",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-panel-representation": "team-consultation", "residential-claim-disputes": "craftsman-bungalow",
    "commercial-hoa-condo-claims": "apartment-community", "roof-hail-loss-appraisal": "roof-shingle-tools",
    "wind-tornado-loss-appraisal": "storm-damaged-homes", "hurricane-tropical-storm-claims": "florence-satellite",
    "water-plumbing-loss-appraisal": "water-damaged-ceiling", "fire-smoke-loss-appraisal": "burned-house-aerial",
    "ice-storm-freeze-damage": "ice-storm-car", "carrier-estimate-audit": "notes-review",
    "neutral-umpire-services": "meeting-laptop",
}
LOC_PHOTO = {
    "raleigh": "raleigh-skyline", "charlotte": "charlotte-skyline", "greensboro": "suburban-homes", "durham": "durham-downtown",
    "winston-salem": "winston-salem-skyline", "fayetteville": "snapped-tree-campus", "cary": "cary-downtown-park",
    "wilmington": "florence-flooded-street", "asheville": "biltmore-asheville", "greenville": "flooded-houses",
    "new-bern": "flooded-neighborhood-aerial", "outer-banks": "cape-hatteras-lighthouse",
}
TOOL_PHOTO = {
    "settlement-gap-estimator": "calculator-pencil", "rcv-acv-holdback-calculator": "brick-home",
    "roof-area-pitch-estimator": "roofer-at-work", "named-storm-deductible-calculator": "outer-banks-sunrise",
    "claim-timeline-planner": "notes-review", "appraisal-preparedness-checkup": "handshake-table",
    "wind-flood-damage-splitter": "florence-flooded-street",
}
POST_PHOTO = {
    "invoking-appraisal-north-carolina-policy": "handshake-table", "wind-vs-flood-hurricane-claims-nc": "flooded-houses",
    "ice-storm-claims-north-carolina": "ice-storm-limb", "coastal-pool-fair-plan-claims": "outer-banks-sunrise",
    "matching-disputes-roof-siding": "damaged-roof-tiles", "choosing-an-independent-appraiser": "meeting-laptop",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(uid="m", size=42):
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#245c3c"/><stop offset="1" stop-color="#0d2b1b"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="11" fill="url(#{uid})"/>'
            '<path d="M11 24.5L24 12l13 12.5" fill="none" stroke="#e27a4f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M12 31.5h24" stroke="#faf6ee" stroke-width="3.4" stroke-linecap="round"/><circle cx="24" cy="31.5" r="3.6" fill="#faf6ee"/>'
            '<path d="M17 37h14" stroke="#faf6ee" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/></svg>')


def brand(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span><b>North Carolina</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "NC", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NC", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across North Carolina’s 100 counties.",
        "areaServed": [{"@type": "State", "name": "North Carolina"}] + [{"@type": "City", "name": l["geo"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hurricane claims", "Ice storm damage", "Hail damage"],
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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def build_graph(path, title, desc, schema, img_key, noindex):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id, main_hint = "WebPage", [], None, None
    for n in schema or []:
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            main_hint = n.get("mainEntity")
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": canonical + "#webpage"}
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        nodes.append(n)
    p = PHOTOS[img_key]
    page = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": p["fw"], "height": p["fh"]},
    }
    if crumb_id:
        page["breadcrumb"] = {"@id": crumb_id}
    order = {t: i for i, t in enumerate(MAIN_TYPES)}
    mains = sorted((n for n in nodes if n.get("@type") in order), key=lambda n: order[n["@type"]])
    page["mainEntity"] = {"@id": main_hint or (mains[0]["@id"] if mains else DOMAIN + "/#business")}
    graph = [org_schema(), site_schema()] + ([] if noindex else [page]) + nodes
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Areas", [(l["city"], loc_path(l)) for l in LOCATIONS], ("Statewide coverage", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", [("Appraisal process guide", PROCESS), ("Common questions", FAQ_P), ("Insurance terms glossary", GLOSS), ("Guides", POST_BASE)], None),
    ]


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


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li class="has-sub"><button type="button" data-drop aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "chev")}</button><ul class="sub{" two" if len(links) > 7 else ""}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">Who we are</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="strong" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head" id="top"><div class="wrap head-in">
{brand("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-act"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-clay head-cta" href="{CONTACT}">Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button></div>
</div></header>
<div class="drawer-bg" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{ABOUT}">Who we are</a></li><li><a href="{CONTACT}">Contact us</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · all 100 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("mf")}
<p>Independent appraisal, estimate audits and umpire work for property owners with disputed insurance claims across North Carolina.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri, 8am–6pm ET</span></li></ul></div>
<div><h2 class="ft">Services</h2><ul>{svc}</ul></div>
<div><h2 class="ft">Areas we serve</h2><ul class="cols2">{loc}</ul><h2 class="ft ft-gap">Calculators</h2><ul>{tl}</ul></div>
<div><h2 class="ft">Company</h2><ul><li><a href="{ABOUT}">Who we are</a></li><li><a href="{CONTACT}">Contact us</a></li><li><a href="{PROCESS}">Appraisal process guide</a></li><li><a href="{FAQ_P}">Common questions</a></li><li><a href="{GLOSS}">Insurance terms</a></li><li><a href="{POST_BASE}">Guides</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we don’t give legal advice, and we don’t act as public adjusters. Content is general and educational, policy terms vary, and results are never guaranteed. Example figures are illustrative.</p>
<div class="foot-row"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{HTMLMAP}">All pages</a></li></ul></div></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top"><svg class="ring" width="52" height="52" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle cx="26" cy="26" r="23"/><circle class="ring-fill" cx="26" cy="26" r="23"/></svg>{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", noindex=False, photo="storm-over-ridges", hero_dark=True):
    canonical = DOMAIN + path
    ld = build_graph(path, title, desc, schema, photo, noindex)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {PHOTOS[photo]["fw"]}w" imagesizes="100vw" fetchpriority="high">'
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across North Carolina">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across North Carolina">
<meta name="geo.region" content="US-NC">
<meta name="geo.placename" content="North Carolina">
<meta name="theme-color" content="#14361f">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script type="application/ld+json">{ld}</script>
</head>
<body{' class="hero-dark"' if hero_dark else ""}>
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
    rel = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if path.endswith(".html"):
        rel = path.strip("/")
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.18"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker kicker-l">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through, free</h2><p>Tell us what the carrier offered. We’ll say honestly whether appraisal makes sense.</p><a class="box-tel" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-clay btn-block" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_band(h="Is the carrier’s number short?", p="Send the estimate and a few photos. We’ll tell you what we see, at no cost."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-clay" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-l" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hurricane / tropical storm", "Wind / tornado", "Hail / roof", "Ice storm / freeze", "Water / plumbing", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", page="/", hl="h3"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in North Carolina"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="form-t">{e(heading)}</{hl}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-pine btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def strip_form():
    return f"""<form class="strip" action="/api/contact.php" method="post" data-lead novalidate aria-label="Request a free claim review">
<p class="strip-t">Free claim review <span>We call back within one business day</span></p>
<div class="strip-f">
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<button class="btn btn-clay" type="submit">Request review {ic("arrow")}</button>
</div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy policy</a>.</span></label>
<div class="form-msg" role="status"></div>
</form>"""


def svc_card(s, h="h3"):
    return f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span><span class="pcard-b"><{h}>{e(s["name"])}</{h}><span class="pcard-p">{e(s["short"])}</span><span class="more">View service {ic("arrow")}</span></span></a>'


def loc_card(l, h="h3"):
    return f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 300px", alt="")}<span class="lcard-b"><small>{e(l["county"])}</small><{h}>{e(l["city"])}</{h}></span></a>'


def tool_row(t, h="h3"):
    return f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="trow-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 220px", alt="")}</span><span class="trow-b"><span class="tag">{e(t["kind"])}</span><{h}>{e(t["name"])}</{h}><span class="trow-p">{e(t["short"])}</span></span><span class="trow-go">{ic("arrow")}</span></a>'


def post_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="gcard-b"><span class="meta">{nice} · {p["read"]} read</span><{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>'


# ---------------------------------------------------------------- home
STORMS = [
    ("1954", "Hurricane Hazel", "Came ashore near the state line as a major hurricane; its surge flattened much of the southern Brunswick County beachfront."),
    ("1989", "Hurricane Hugo", "Stayed strong far inland and brought down trees across Charlotte and the western Piedmont."),
    ("1996", "Hurricane Fran", "Landed near Cape Fear and carried damaging wind and falling trees deep into the Triangle."),
    ("1999", "Hurricane Floyd", "Produced record river flooding across eastern North Carolina, including the Tar and Neuse basins."),
    ("2002", "December ice storm", "Freezing rain coated the Piedmont from Charlotte to Raleigh and left well over a million customers in the dark."),
    ("2011", "April 16 tornadoes", "An outbreak of tornadoes crossed central and eastern counties, striking Sanford and parts of Raleigh."),
    ("2016", "Hurricane Matthew", "Drove severe river flooding along the Lumber, Neuse and Cape Fear basins."),
    ("2018", "Hurricane Florence", "Made landfall near Wrightsville Beach, stalled, and pushed surge up the Neuse into New Bern."),
    ("2024", "Hurricane Helene", "Caused catastrophic flooding, landslides and wind damage across the western mountains."),
]

REGIONS = [
    ("Mountains", "Asheville · Boone · Sylva", "Ice dams, heavy snow loads, falling hardwoods and, after Helene, wind-versus-flood questions on mountain homes and cabins.", "blue-ridge-valley"),
    ("Foothills", "Hickory · Morganton · Lenoir", "Strong thunderstorms, hail and ice storms where the Piedmont meets the Blue Ridge escarpment.", "storm-over-ridges"),
    ("Piedmont", "Charlotte · Triad · Triangle", "The state’s hail and ice-storm belt, with dense tree canopy over older neighborhoods and fast-growing HOA suburbs.", "charlotte-skyline"),
    ("Sandhills", "Fayetteville · Southern Pines", "Tornadoes, tropical remnants and long-leaf pines that snap in high wind, plus large rental and military housing stocks.", "snapped-tree-campus"),
    ("Coastal Plain", "Greenville · Kinston · Lumberton", "River flooding from slow hurricanes, farm structures and older homes on crawlspaces.", "barn-storm-clouds"),
    ("Coast & Outer Banks", "Wilmington · New Bern · Nags Head", "Named-storm deductibles, coastal pool policies, wind-driven rain and homes on pilings.", "cape-hatteras-lighthouse"),
]


def home():
    K = BRAND
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, write an independent line-item estimate, work with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When is it worth calling a {K}?", "When coverage has been accepted, you have the carrier’s estimate, and the gap between it and a qualified contractor’s estimate is meaningful, often more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. Coverage questions are not decided by the award."),
        ("How are appraisal fees handled?", "Each side pays its own appraiser and usually half of the umpire. We put our fee terms in writing before any work begins, and the first conversation is free."),
        ("Do you cover my county?", "Yes. We work in all 100 North Carolina counties, from the mountains to the Outer Banks, with frequent work around Charlotte, the Triad, the Triangle, Fayetteville, Wilmington and the coast."),
    ]
    pillars = [("scale", "Appointed by you", "Never by the carrier"), ("ruler", "Measured, not guessed", "Our own inspection and scope"), ("file", "Line-item estimates", "Priced for your NC market"), ("shield", "Plain, honest triage", "We’ll say when appraisal won’t help")]
    pill = "".join(f'<li>{ic(i)}<span><b>{e(a)}</b>{e(b)}</span></li>' for i, a, b in pillars)
    svc = "".join(svc_card(s) for s in SERVICES)
    storms = "".join(f'<li class="storm rv"><span class="yr">{y}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for y, n, t in STORMS)
    regions = "".join(f'<article class="rcard rv">{img(ph, sizes="(max-width:700px) 85vw, 340px", alt="")}<div class="rcard-b"><small>{e(c)}</small><h3>{e(n)}</h3><p>{e(t)}</p></div></article>' for n, c, t, ph in REGIONS)
    steps = [
        ("Free review", f"Send the policy, the carrier’s estimate and your photos. A {K} reads them and tells you plainly whether appraisal fits."),
        ("Independent scope", "We inspect, measure and photograph the property, then build a line-item estimate priced for your area."),
        ("Written demand", "Appraisal is demanded in writing and we’re named as your appraiser within the policy’s deadline."),
        ("Panel work", "We work line by line with the carrier’s appraiser. Most disputes narrow sharply here."),
        ("Signed award", "Open items go to a neutral umpire; two signatures set the amount of loss and payment follows."),
    ]
    proc = "".join(f'<li class="step rv"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    tools = "".join(tool_row(t) for t in TOOLS)
    locs = "".join(loc_card(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    body = f"""
<section class="hero">
<div class="hero-bg">{img("storm-over-ridges", lazy=False, alt="", extra=' data-parallax="0.22"')}</div>
<div class="wrap hero-in">
<p class="kicker kicker-l">Independent property claim appraisal · all 100 counties</p>
<h1>{K} for <em>disputed</em> property claims</h1>
<p class="lede">When your insurer accepts the claim but the payment won’t rebuild what you lost, {K} prepares an independent, line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="#services">See our services</a></div>
{strip_form()}
</div>
</section>

<section class="pillars" aria-label="How we work"><div class="wrap"><ul class="pill-list">{pill}</ul></div></section>

<section class="sec"><div class="wrap intro">
<figure class="intro-ph rv">{img("roofer-at-work", sizes="(max-width:900px) 100vw, 520px")}<figcaption>Every valuation starts on the roof, in the attic and in the crawlspace, not in the carrier’s file.</figcaption></figure>
<div class="intro-tx rv">
<p class="kicker">What we do</p>
<h2>What a {K} actually does for you</h2>
<p>Most underpaid claims in this state aren’t denied. They’re short: a slope left off the roof, a hardwood floor that stops at the doorway, an ice-storm limb strike priced as a patch, code work nobody included. {K} exists for the gap between “covered” and “paid in full.”</p>
<p>When either side invokes the appraisal clause, you name an appraiser, the carrier names one, and the two of them (with an umpire if needed) set the amount of loss. As your {K}, we build the number you take to that table and we defend it item by item.</p>
<ul class="ticks"><li>{ic("check")}Independent inspection and measurements</li><li>{ic("check")}Line-item estimates priced for your area</li><li>{ic("check")}Panel negotiation and umpire presentation</li><li>{ic("check")}Written fee terms before work begins</li></ul>
<a class="btn btn-pine" href="{ABOUT}">How we work {ic("arrow")}</a>
</div></div></section>

<section class="sec sec-sage" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Services</p><h2>Eleven ways a {K} can help</h2><p>From a quick estimate audit to full appraisal panel representation and neutral umpire work, each service is built around a valuation that holds up.</p></div>
<div class="pgrid">{svc}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">Compare every service {ic("arrow")}</a></p>
</div></section>

<section class="ribbon" aria-label="At a glance"><div class="wrap ribbon-in">
<div><b data-count="100">100</b><span>North Carolina counties served</span></div>
<div><b data-count="11">11</b><span>Appraisal and estimating services</span></div>
<div><b data-count="7">7</b><span>Free claim calculators</span></div>
<div><b>2 of 3</b><span>Signatures make an award binding</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Storm record</p><h2>The storms that shaped how North Carolina claims are valued</h2><p>A {K} has to understand what each kind of event does to a building. These are the storms property owners here still measure against.</p></div>
<ol class="storm-rail" tabindex="0" aria-label="Notable North Carolina storms">{storms}</ol>
<p class="hint">Swipe or scroll sideways to see the full timeline.</p>
</div></section>

<section class="sec sec-pine"><div class="wrap">
<div class="sec-head left rv"><p class="kicker kicker-l">Six claim climates</p><h2>From the Blue Ridge to the barrier islands</h2><p>Our state stretches more than 500 miles. A {K} working in Boone faces different losses than one working in Nags Head, and the estimate has to reflect that.</p></div>
<div class="region-rail">{regions}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The process</p><h2>From first call to a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding answer on the amount of loss.</p></div>
<ol class="steps">{proc}</ol>
<p class="center mt"><a class="link" href="{PROCESS}">Read the full appraisal process guide</a></p>
</div></section>

<section class="sec sec-cream" id="gap-check"><div class="wrap split">
<div class="rv"><p class="kicker">Quick check</p><h2>Is the gap big enough for appraisal?</h2><p>Type in the two numbers you already have. A large gap is worth a conversation with a {K}; a small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}settlement-gap-estimator/">settlement gap estimator</a> adds appraiser and umpire fees and shows your net at three outcomes. All figures are illustrative.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv sticky-col"><p class="kicker">Free calculators</p><h2>Seven free tools from a {K}</h2><p>Check the carrier’s math before you pick up the phone. Every calculator runs in your browser; nothing is stored or sent.</p><a class="btn btn-line" href="{TOOL_BASE}">All calculators {ic("arrow")}</a></div>
<div class="tlist">{tools}</div>
</div></section>

<section class="sec sec-sage"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Areas we serve</p><h2>Where our {K} team works most often</h2><p>We take claims in every county. These twelve local pages cover the places we’re called to most.</p></div>
<div class="lgrid">{locs}</div>
<p class="center mt"><a class="link" href="{LOC_BASE}">See statewide coverage</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. A {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="who">
<div class="who-c who-hl rv"><h3>{K}</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Binding award on the amount</dd></dl></div>
<div class="who-c rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Manage and negotiate the claim</dd><dt>Best stage</dt><dd>Early, from first notice</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></div>
<div class="who-c rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Legal disputes and litigation</dd><dt>Best stage</dt><dd>Denials, bad faith, deadlines</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></div>
</div></div></section>

<section class="sec sec-cream"><div class="wrap split split-top">
<div class="rv"><p class="kicker">Questions</p><h2>Questions people ask a {K}</h2><p>Straight answers on how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-pine" href="{FAQ_P}">All questions {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Insurance terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read this before you invoke appraisal</h2><p>Practical guides from {K} on policy language, documentation and strategy.</p></div>
<div class="ggrid">{posts}</div>
<p class="center mt"><a class="link" href="{POST_BASE}">All guides</a></p>
</div></section>

<section class="pcta"><div class="pcta-bg">{img("ice-storm-limb", alt="", extra=' data-parallax="0.25"')}</div><div class="wrap pcta-in rv"><p class="kicker kicker-l">Before you sign the release</p><h2>Check the numbers while you still can</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn btn-clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-l" href="#contact">Send your estimate</a></div></div></section>

<section class="sec sec-pine" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker kicker-l">Start here</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. You’ll get a straight answer on whether appraisal is worth pursuing, with no pressure.</p>
<ul class="clines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Coverage</small>All 100 North Carolina counties</span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Disputed Claims",
                        "North Carolina Insurance Appraiser: independent appraisal, estimate audits and umpire services for underpaid storm, ice, water and fire claims.",
                        body, schema, photo="storm-over-ridges"), 1.0)


# ---------------------------------------------------------------- services
def layout(article, aside):
    return f'<div class="wrap layout"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Claim appraisal", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        article = s["body"] + f'<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}<h2>Related services</h2>' + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Claim appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(article, call_box() + list_box("All services", items, path) + list_box("Areas we serve", locs + [("Statewide coverage", LOC_BASE)])) + cta_band()
        svc = {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "State", "name": "North Carolina"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, s["title"], s["desc"], body, [crumbs_schema(trail), svc, faq_schema(s["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim appraisal", SVC_BASE)]
    cards = "".join(svc_card(s, "h2") for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across North Carolina",
                     "Eleven services built around one job: an accurate, defensible valuation of your loss. Start with an estimate audit, or bring us in once appraisal has been demanded.", "team-consultation") + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
<section class="sec sec-cream"><div class="wrap split split-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate audit</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. An audit answers that in days, and some disputes close right there with a documented supplement.</p><a class="btn btn-pine" href="{SVC_BASE}carrier-estimate-audit/">About estimate audits {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one stage?", "Yes. Many clients start with an audit and decide later whether to invoke appraisal."), ("Do you handle both homes and commercial buildings?", "Yes: houses, condos, townhome communities, apartments, offices, retail, churches and industrial buildings."), ("Do you only handle hurricane claims?", "No. Hail, wind, tornado, ice storm, water, fire and other covered perils are all part of our work.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in NC | 11 Claim Services",
                             "Insurance appraisal services across North Carolina: panel representation, estimate audits, hurricane, hail, ice storm, water, fire and umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="team-consultation"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Areas we serve", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(l["hoods"])
        storms = "".join(f'<li><span class="yr">{e(y)}</span><span><b>{e(n)}</b>{e(t)}</span></li>' for y, n, t in l["storms"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
        near = related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        article = f"""<div class="localbox"><div><h2 class="lb-t">{e(l["city"])} at a glance</h2><ul class="chips">{chips}</ul><p><b>Housing:</b> {e(l["housing"])}</p><p><b>Where we work:</b> {e(hoods)}</p></div></div>
{l["body"]}
<h2>Storm history around {e(l["city"])}</h2><ul class="mini-storms">{storms}</ul>
<h2>Services available in {e(l["city"])}</h2><p>Every {BRAND} service is available to property owners in {e(l["city"])} and across {e(l["county"])}:</p><ul class="cols">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby areas</h2>{near}"""
        aside = call_box() + list_box("Areas we serve", items, path) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(article, aside) + cta_band(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        svc = {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "City", "name": l["geo"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", North Carolina"}}, "url": DOMAIN + path}
        write(path, document(path, l["title"], l["desc"], body, [crumbs_schema(trail), svc, faq_schema(l["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Areas we serve", LOC_BASE)]
    cards = "".join(loc_card(l, "h2") for l in LOCATIONS)
    regions = "".join(f'<article class="rcard rv">{img(ph, sizes="(max-width:700px) 85vw, 340px", alt="")}<div class="rcard-b"><small>{e(c)}</small><h3>{e(n)}</h3><p>{e(t)}</p></div></article>' for n, c, t, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 100 North Carolina Counties",
                     "We work statewide, from Murphy to Manteo. These local pages cover the cities and coastal communities where we’re called most often.", "raleigh-skyline") + f"""
<section class="sec"><div class="wrap"><div class="lgrid">{cards}</div></div></section>
<section class="sec sec-pine"><div class="wrap"><div class="sec-head left rv"><p class="kicker kicker-l">Regions</p><h2>How claims differ across the state</h2><p>The same policy language plays out very differently in a mountain cabin, a Charlotte high-rise and a Nags Head cottage on pilings.</p></div><div class="region-rail">{regions}</div></div></section>
{cta_band("Don’t see your town?", "We cover every county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Areas We Serve | NC Insurance Appraisal, 100 Counties",
                             "Insurance appraisal in all 100 North Carolina counties, including Raleigh, Charlotte, Greensboro, Durham, Wilmington, Asheville and the Outer Banks.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="raleigh-skyline"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        ph = TOOL_PHOTO[t["slug"]]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        article = t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free calculators</h2>' + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Free {t['kind'].lower()} · nothing stored", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and all example figures are illustrative.</p></div></section>""" + layout(article, call_box() + list_box("All calculators", items, path)) + cta_band("Want a professional to check the numbers?", "Send your estimate and we’ll audit it line by line.")
        app = {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
               "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}
        write(path, document(path, t["title"], t["desc"], body, [crumbs_schema(trail), app, faq_schema(t["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    rows = "".join(tool_row(t, "h2") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for North Carolina",
                     "Seven calculators, planners and worksheets drawn from real appraisal work. Use them to understand your claim, check the carrier’s math and plan next steps. No sign-up, nothing stored.", "calculator-pencil", cta=False) + f"""
<section class="sec"><div class="wrap narrow-w"><div class="tlist">{rows}</div></div></section>
<section class="sec sec-cream"><div class="wrap split split-top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="olist"><li>Start with the <a href="{TOOL_BASE}claim-timeline-planner/">claim timeline planner</a> so no deadline slips.</li><li>Check the roof math in the <a href="{TOOL_BASE}roof-area-pitch-estimator/">roof area &amp; pitch estimator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}named-storm-deductible-calculator/">named-storm deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV/ACV holdback</a> calculators.</li><li>After a hurricane, sort damage in the <a href="{TOOL_BASE}wind-flood-damage-splitter/">wind vs. flood splitter</a>.</li><li>Test the dispute in the <a href="{TOOL_BASE}settlement-gap-estimator/">settlement gap estimator</a>, then score your file with the <a href="{TOOL_BASE}appraisal-preparedness-checkup/">preparedness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | NC Property Owners",
                              "Free claim calculators: settlement gap, RCV/ACV holdback, roof area, named-storm deductible, deadline planner, wind vs. flood splitter and more.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="calculator-pencil"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    learn_items = [("Appraisal process guide", PROCESS), ("Common questions", FAQ_P), ("Insurance terms glossary", GLOSS), ("Guides", POST_BASE)]

    path, trail = PROCESS, [("Home", "/"), ("Appraisal process guide", PROCESS)]
    toc = "".join(f'<li><a href="#stage-{i + 1}">{e(n)}</a></li>' for i, (n, _) in enumerate(PROCESS_STEPS))
    stages = "".join(f'<section class="stage" id="stage-{i + 1}"><h2><span>Stage {i + 1}</span>{e(n)}</h2>{h}</section>' for i, (n, h) in enumerate(PROCESS_STEPS))
    article = f'{PROCESS_INTRO}<nav class="toc" aria-label="Stages"><p class="toc-t">The {len(PROCESS_STEPS)} stages</p><ol>{toc}</ol></nav>{stages}{PROCESS_OUTRO}'
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in North Carolina, Stage by Stage",
                     f"{len(PROCESS_STEPS)} stages, from the first disagreement to payment: what happens, who does what, and where claims most often go wrong.", "notes-review",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "Any 2 of 3 signatures")]) + layout(article, call_box() + list_box("Resources", learn_items, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in North Carolina", "description": "The stages of a property insurance appraisal from dispute to award and payment.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#stage-{i + 1}"} for i, (n, _) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process Guide | NC, Stage by Stage",
                         "How property insurance appraisal works in North Carolina: the written demand, naming appraisers, the umpire, negotiation, the award and payment.",
                         body, [crumbs_schema(trail), howto], photo="notes-review"), 0.8)

    path, trail = FAQ_P, [("Home", "/"), ("Common questions", FAQ_P)]
    jump = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Common Questions About Insurance Appraisal in North Carolina",
                     f"{len(allq)} plain answers grouped by topic: the basics, costs and timing, state specifics, storm claims and what happens after the award.", "handshake-table") + layout(
        f'<nav class="toc" aria-label="Topics"><p class="toc-t">Jump to a topic</p><ul>{jump}</ul></nav>{groups}', call_box() + list_box("Resources", learn_items, path)) + cta_band("Didn’t see your question?", "Call or email and we’ll talk it through.")
    write(path, document(path, "Insurance Appraisal Questions | Costs, Timing & NC Rules",
                         "Answers to common North Carolina insurance appraisal questions, grouped by topic: basics, costs, timing, storm claims and what follows the award.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="handshake-table"), 0.8)

    path, trail = GLOSS, [("Home", "/"), ("Insurance terms", GLOSS)]
    gl = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in gl})
    az = "".join(f'<a href="#t-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in gl:
        c = term[0].upper()
        anchor = f' id="t-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    article = f'<div class="gfilter"><label for="gloss-filter">Search {len(gl)} terms</label><input id="gloss-filter" type="search" placeholder="Try “holdback”, “umpire” or “NCIUA”" autocomplete="off"><p class="hint" data-gcount aria-live="polite"></p></div><nav class="az" aria-label="Letters">{az}</nav><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms, Defined in Plain English",
                     f"{len(gl)} words you’ll meet in policies, estimates and appraisal awards, from actual cash value to umpire. Type in the box to filter.", "calculator-pencil", cta=False) + layout(article, call_box() + list_box("Resources", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in gl]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "Searchable glossary of property insurance claim terms: actual cash value, replacement cost, holdback, umpire, named-storm deductible, NCIUA and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-pencil"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        others = [o for o in POSTS if o is not p][:3]
        article = f'<p class="byline">By the {BRAND} team · Published {nice} · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2>' + related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Guide · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(article, call_box() + list_box("Resources", learn_items) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_band()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path, trail = POST_BASE, [("Home", "/"), ("Guides", POST_BASE)]
    cards = "".join(post_card(p, "h2") for p in POSTS)
    body = page_hero(trail, "Guides", "Insurance Appraisal Guides for North Carolina Owners",
                     "Practical, state-specific guides on policy language, storm documentation and appraisal strategy.", "damaged-roof-tiles", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid">{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Guides | North Carolina Claims",
                         "Guides for North Carolina property owners on invoking appraisal, wind vs. flood, ice storms, coastal pool claims, matching and choosing an appraiser.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="damaged-roof-tiles"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path, trail = ABOUT, [("Home", "/"), ("Who we are", ABOUT)]
    article = f"""<figure class="lead-img">{img("team-consultation", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most property claim professionals do a little of everything. {BRAND} chose to specialize in the amount of loss: what it genuinely costs to put a damaged property back the way it was. Our process, documentation standards and free calculators all serve that question. Depending on the claim, we act as your appointed appraiser, audit an estimate before a dispute hardens, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before price.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate looks good on day one and loses credibility with the umpire. We price what we can defend.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney, a public adjuster or simply a supplement, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost and how we’re paid before work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo and townhome owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across North Carolina. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>North Carolina produces almost every kind of property loss: ice storms in the Piedmont, hail in the foothills, tornadoes in the Sandhills, river flooding on the Coastal Plain, hurricanes on the coast and, after Helene, mountain flood and wind damage on a scale few expected. Working all 100 counties keeps us current on every one of them. If you have questions about the state’s insurance rules, the North Carolina Department of Insurance publishes consumer guidance and accepts complaints.</p>"""
    body = page_hero(trail, "Who we are", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "meeting-laptop") + layout(
        article, call_box() + list_box("Explore", [("Claim appraisal services", SVC_BASE), ("Areas we serve", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process guide", PROCESS)])) + cta_band()
    write(path, document(path, f"About Us | {BRAND}",
                         "North Carolina Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="meeting-laptop"), 0.7)

    path, trail = CONTACT, [("Home", "/"), ("Contact us", CONTACT)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "handshake-table", cta=False) + f"""
<section class="sec sec-pine"><div class="wrap contact">
<div class="rv"><p class="kicker kicker-l">Direct lines</p><h2>Reach us directly</h2>
<ul class="clines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Service area</small>Statewide, all 100 counties</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks ticks-l"><li>{ic("check")}Your declarations page</li><li>{ic("check")}The carrier’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the carrier</li><li>{ic("check")}Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact Us | {BRAND}",
                         "Get a free review of a disputed North Carolina property claim. Call or text (844) 537-1427, email us, or send your claim details through the form.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="handshake-table"), 0.8)

    lic = {"cc0": "CC0 1.0 (public domain dedication)", "pdm": "Public Domain Mark"}
    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td><b>{e(v["title"])}</b><br><small>{e(v.get("creator") or "Unknown creator")} · via {e(v["source"].title())}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "privacy policy", f"""<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web host records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. The figures you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics through Google Tag Manager, this policy will be updated to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To see, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Terms of Use", "terms of use", f"""<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. The content is general information about insurance appraisal and property claims in North Carolina.</p>
<h2>No professional relationship</h2><p>Reading the site, using its calculators or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Consult a licensed North Carolina attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome, and example figures throughout the site are illustrative.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of North Carolina.</p>""", "The terms that apply when you use this website and its calculators."),
        DISCLAIM: ("Disclaimer", "legal disclaimer", f"""<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Statutes and agencies</h2><p>References to North Carolina statutes, the Department of Insurance, the coastal and FAIR plan associations or past storms are for context only and described in general terms. Verify current law and facts with official sources and a North Carolina attorney.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is approaching, consult an attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website."),
        CREDITS: ("Photo Credits", "photo credits", f"""<p>Every photograph on this site is either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or marked as a <strong>public-domain</strong> work (including photos by U.S. government agencies such as NOAA, USGS, USDA, HUD, the National Park Service and the National Guard). We found them through the Openverse search engine. Attribution isn’t legally required, but we credit the creators here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for every photograph used on this site."),
    }
    for path, (title, kw, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "brick-commercial-building", cta=False) + layout(content, call_box())
        desc = f"The {kw} for {BRAND} ({HOST}): {lede[0].lower() + lede[1:]}"
        if len(desc) > 150:
            desc = f"The {kw} for {BRAND}: {lede[0].lower() + lede[1:]}"
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="brick-commercial-building"), 0.3)


def sitemap_pages():
    path, trail = HTMLMAP, [("Home", "/"), ("All pages", HTMLMAP)]
    groups = [
        ("Main", [("Home", "/"), ("Who we are", ABOUT), ("Contact us", CONTACT)]),
        ("Claim appraisal", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Areas we serve", [("Statewide coverage", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal process guide", PROCESS), ("Common questions", FAQ_P), ("Insurance terms", GLOSS), ("Guides", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIM), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "All Pages", f"Every page on the {BRAND} website, grouped by section.", "brick-commercial-building", cta=False) + f'<section class="sec"><div class="wrap mapgrid">{cols}</div></section>'
    write(path, document(path, f"HTML Site Map | {BRAND}", f"An HTML site map listing every page on {BRAND}: services, local areas, free calculators, guides and legal pages.", body, [crumbs_schema(trail)], photo="brick-commercial-building"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-bg">{img("fallen-trees-house", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-l">Error 404</p><h1>This page came down in the storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-clay" href="/">Home</a><a class="btn btn-ghost-l" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn btn-ghost-l" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, noindex=True, photo="fallen-trees-house"), sitemap=False)


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
        f.write(INDEX_PHP.replace("__HOST__", HOST))


INDEX_PHP = r"""<?php
// North Carolina Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$home = 'https://__HOST__';

// Canonical host and scheme, only on the real domain (TLS terminates upstream).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off' ? 'http' : 'https'));
if ($host === 'www.__HOST__' || ($host === '__HOST__' && $proto === 'http')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== '__HOST__') {
    header('X-Robots-Tag: noindex, nofollow');
}
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
$serve = function (string $file, int $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile($file);
    exit;
};
if ($path === '/' || $path === '/index.php') {
    $serve(__DIR__ . '/home.html');
}
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    $serve(__DIR__ . $path . 'index.html');
}
$serve(__DIR__ . '/404.html', 404);
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
