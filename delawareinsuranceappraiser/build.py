#!/usr/bin/env python3
"""Static site generator for delawareinsuranceappraiser.com.

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
from learn import PROCESS_BODY, STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Delaware Insurance Appraiser"
HOST = "delawareinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112b"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no GTM output.
GTM_ID = "GTM-THRM2QP8"

SVC_BASE = "/appraisal-expertise/"
LOC_BASE = "/serving-delaware/"
TOOL_BASE = "/claim-worksheets/"
POST_BASE = "/appraisal-journal/"
P_ROAD = "/how-the-appraisal-panel-works/"
P_FAQ = "/delaware-appraisal-faq/"
P_GLOSS = "/claim-terms-explained/"
P_ABOUT = "/our-practice/"
P_CONTACT = "/start-your-review/"
P_PRIV = "/privacy-practices/"
P_TERMS = "/terms-of-service-de/"
P_DISC = "/important-disclaimer/"
P_CRED = "/photo-credits/"
P_MAP = "/browse-all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, DE"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# Approximate Arial widths (per 1000 em), same table as validate.py, to keep titles under ~580px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


def title_ok(t):
    return len(t) <= 60 and sum(_W.get(c, 556) for c in t) * 20 / 1000 <= 580


def pick_title(*cands):
    for c in cands:
        if title_ok(c):
            return c
    raise SystemExit(f"no title fits: {cands}")


def pick_desc(*cands):
    for c in cands:
        if 110 <= len(c) <= 150:
            return c
    raise SystemExit(f"no description fits: {[(len(c), c) for c in cands]}")


# ---------------------------------------------------------------- photos
ALT = {
    "hero-coastal-home": "Two-story house with lit windows at dusk",
    "home-front-porch": "Two-story suburban home with a covered front porch",
    "townhomes": "Row of townhomes on a residential street",
    "condo-building": "Mid-rise condominium building with balconies",
    "office-building": "Glass office tower against a blue sky",
    "warehouse-roof": "Aerial view of a flat-roofed warehouse at dusk",
    "farm-barn": "Red barn on flat farmland under storm clouds",
    "roof-shingles": "Aerial view of a house with an asphalt shingle roof",
    "roofer-at-work": "Roofer working on a shingle roof",
    "hail-stones": "Hailstones collected after a storm",
    "roof-storm-damage": "Roof with a section of shingles and decking torn open",
    "tornado-damage": "House with its roof and walls torn apart by a tornado",
    "fallen-tree-house": "Uprooted tree beside a house wrecked by a tornado",
    "flood-street": "Floodwater covering a residential street and front yards",
    "coastal-storm-damage": "Sand-covered coastal homes after Hurricane Sandy",
    "water-ceiling": "Water stains spreading across a ceiling",
    "fire-damage": "House damaged by fire with charred siding and roof",
    "smoke-interior": "Charred interior wreckage after a fire",
    "storm-clouds-shore": "Dark storm clouds over the ocean and beach",
    "rough-surf": "Storm surf crashing under a pier",
    "snow-house": "House and yard covered in heavy snow",
    "icicles-roof": "Icicles hanging from the edge of a roof",
    "lightning": "Lightning below a storm cloud at night",
    "consultation": "Two people reviewing documents together at a table",
    "inspector-clipboard": "Hands writing notes on a clipboard",
    "calculator-paperwork": "Calculator and paperwork on a desk",
    "laptop-spreadsheet": "Laptop showing a spreadsheet with hands on the keyboard",
    "wilmington-skyline": "Wilmington, Delaware skyline above the Brandywine",
    "dover-legislative-hall": "Legislative Hall, the Delaware State Capitol in Dover",
    "rehoboth-boardwalk": "Boardwalk at Rehoboth Avenue in Rehoboth Beach, Delaware",
    "lewes-cape-henlopen": "Cape May–Lewes Ferry terminal in Lewes, Delaware",
    "brandywine-creek": "Brandywine Creek near Hagley in northern Delaware",
    "delaware-beach-dunes": "Beach umbrellas and dune grass at Rehoboth Beach, Delaware",
    "delaware-farmland": "Storm clouds over open farm fields",
}
FALLBACK = {}  # filled in main(): missing photo key -> available substitute


def ph(key):
    return key if key in PHOTOS else FALLBACK.get(key, next(iter(PHOTOS)))


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    key = ph(key)
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT.get(key, p.get("title", "")))
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
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 2 3-2M9 21l3-2 3 2M3 9l2 3-2 3M21 9l-2 3 2 3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls="ico"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(size=40):
    """Brand mark: slate tile, white roofline over a coral 'balance' bar."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#233D4D"/>'
            '<path d="M11 25.5L24 13.5l13 12" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M16.5 23.5V34h15V23.5" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M12 38.5h24" stroke="#F0795B" stroke-width="3.6" stroke-linecap="round"/>'
            '<circle cx="24" cy="28" r="2.6" fill="#F0795B"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal · First State</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "DE", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-DE", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid property claims in the First State",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in New Castle, Kent and Sussex counties, Delaware.",
        "areaServed": [{"@type": "State", "name": "Delaware"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Nor'easter damage", "Hurricane deductibles", "Wind vs. flood allocation"],
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


def itemlist_schema(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Delaware", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Delaware communities", LOC_BASE)),
        ("Worksheets", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free worksheets", TOOL_BASE)),
        ("Resources", [("Appraisal roadmap", P_ROAD), ("Questions answered", P_FAQ), ("Claim terms", P_GLOSS), ("Appraisal journal", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        cls = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{cls}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head" id="top"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-act"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-coral head-cta" href="{P_CONTACT}">Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>
<div class="drawer-veil" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{P_ABOUT}">About us</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · New Castle, Kent &amp; Sussex</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:9])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-foot")}
<p>Independent appraisal and estimating for property owners with disputed insurance claims, from Claymont and Hockessin to Fenwick Island and Delmar.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("clock")}Mon–Fri 8am–6pm ET</li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Communities</h2><ul>{loc}<li><a href="{LOC_BASE}">All of Delaware</a></li></ul></div>
<div><h2 class="foot-h">Worksheets</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{P_ABOUT}">Who we are</a></li><li><a href="{P_CONTACT}">Contact us</a></li><li><a href="{P_ROAD}">Appraisal roadmap</a></li><li><a href="{P_FAQ}">Questions answered</a></li><li><a href="{P_GLOSS}">Claim terms</a></li><li><a href="{POST_BASE}">Appraisal journal</a></li></ul></div>
</div>
<div class="wrap foot-base"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_CRED}">Photo credits</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Information on this site is general and educational; policy wording controls. Example figures are illustrative, and results depend on the facts of each claim.</p>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></div>"""


def gtm_head():
    # Head snippet exactly as provided by the site owner.
    if not GTM_ID:
        return ""
    return (f'<script async src="https://www.googletagmanager.com/gtm.js?id={GTM_ID}"></script>\n'
            "<script>\n"
            "  window.dataLayer = window.dataLayer || [];\n"
            "  function gtag(){dataLayer.push(arguments);}\n"
            "  gtag('js', new Date());\n"
            "</script>\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\nheight="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-coastal-home", page_type="WebPage", main_entity=None):
    canonical = DOMAIN + ("/" if path == "/" else path)
    photo = ph(photo)
    extra, crumb_id = [], None
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
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        extra.append(n)
    pimg = PHOTOS[photo]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    if main_entity:
        webpage["mainEntity"] = {"@id": main_entity}
    else:
        for want in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
            hit = [n["@id"] for n in extra if n.get("@type") == want]
            if hit:
                webpage["mainEntity"] = {"@id": hit[0]}
                break
        else:
            webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw" fetchpriority="high">\n')
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Delaware">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Delaware">
<meta name="geo.region" content="US-DE">
<meta name="geo.placename" content="Delaware">
<meta name="theme-color" content="#233D4D">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Nunito+Sans:ital,opsz,wght@0,6..12,400;0,6..12,600;0,6..12,700;1,6..12,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{gtm_body()}<div class="progress" aria-hidden="true"><span></span></div>
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
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
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
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(parts) + "</ol></nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-h">Talk it through, free</h2><p>A short call tells you whether appraisal fits your claim — and if it doesn’t, what will.</p><a class="side-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-coral" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow")}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def cta_band(h="Have a claim that doesn’t add up?", p="Send us the carrier’s estimate and your photos. We’ll tell you plainly what we see."):
    return f"""<section class="cta-band"><div class="wrap cta-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="sidebar"><div class="sticky">{aside}</div></aside></div>'


LOSSES = ["Wind / tornado", "Hurricane / coastal storm", "Nor’easter / winter storm", "Hail / roof", "Water / pipe leak", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", page="/", hlevel=3, fid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord / investor", "Commercial owner", "HOA board / manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in New Castle County", "Elsewhere in Kent County", "Elsewhere in Sussex County"]
    h = f"h{hlevel}"
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<{h} class="lead-h">{e(heading)}</{h}><p class="lead-sub">Free review · No obligation · Usually a reply within one business day.</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="{P_PRIV}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-coral btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def quick_form():
    return f"""<form class="lead quick" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="lead-h">Get a free claim review</h2><p class="lead-sub">Two minutes. We call back within one business day.</p>
<div><label for="q-name">Name *</label><input id="q-name" name="name" autocomplete="name" required></div>
<div><label for="q-phone">Phone *</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="q-loss">Type of loss</label><select id="q-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="q-county">County</label><select id="q-county" name="city"><option>New Castle County</option><option>Kent County</option><option>Sussex County</option></select></div>
<div class="hp" aria-hidden="true"><label for="q-web">Website</label><input id="q-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{P_PRIV}">privacy policy</a>.</span></label>
<button class="btn btn-coral btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="lead-note">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
COUNTIES = [
    ("newcastle", "New Castle County", "Wilmington · Newark · Middletown · Bear",
     "Delaware’s most populous county runs from the Pennsylvania line and the Brandywine Valley down past the Chesapeake & Delaware Canal. Rowhomes, stone houses and Riverfront condos in the north give way to fast-growing subdivisions in Middletown and Townsend.",
     ["Creek & river flooding", "Frozen pipes", "Tree damage", "HOA matching"], "wilmington-skyline"),
    ("kent", "Kent County", "Dover · Smyrna · Milford · Camden",
     "The middle county centers on Dover, the state capital, with farmland and Delaware Bay marshes on its eastern edge. Open country lets summer squall lines and tropical remnants build, and Dover Air Force Base means many military households.",
     ["Squall lines", "Tornadoes", "Hail", "Farm buildings"], "dover-legislative-hall"),
    ("sussex", "Sussex County", "Lewes · Rehoboth · Bethany · Georgetown · Seaford",
     "The largest county by area holds Delaware’s Atlantic beaches, the inland bays and a deep agricultural interior. Coastal Sussex faces nor’easters, named storms and wind-versus-flood questions; western Sussex sees poultry houses, farms and river towns.",
     ["Nor’easters", "Hurricanes", "Wind vs. flood", "Poultry houses"], "rehoboth-boardwalk"),
]

STORMS = [
    ("1962", "Ash Wednesday Storm", "A slow nor’easter lingered for several tide cycles in March, battering Rehoboth, Bethany and Fenwick and reshaping the coastline."),
    ("1985", "Hurricane Gloria", "Gloria raced up the coast in September, bringing wind damage and power outages across the state."),
    ("2003", "Hurricane Isabel", "Isabel’s surge and wind affected the Delaware Bay shore and coastal communities in September."),
    ("2010", "Back-to-back snowstorms", "February storms brought record seasonal snow to northern Delaware, with roof and ice-dam claims."),
    ("2012", "Superstorm Sandy", "Sandy flooded bayfront and inland-bay communities and damaged dunes, roads and beachfront property."),
    ("2020", "Tropical Storm Isaias", "Isaias produced tornadoes in Delaware in August, including a long-track twister through Kent and New Castle counties."),
    ("2021", "Remnants of Ida", "Ida’s rain pushed the Brandywine to record levels in Wilmington in September, flooding homes and businesses."),
]


def svc_card(s, h="h3"):
    return (f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-media">{img(s["photo"], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="card-ico">{ic(s["icon"])}</span></span>'
            f'<span class="card-body"><{h} class="card-t">{e(s["name"])}</{h}><span class="card-p">{e(s["short"])}</span><span class="card-more">Learn more {ic("arrow")}</span></span></a>')


def tool_card(t, h="h3"):
    return (f'<a class="card card-tool rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-media">{img(t["photo"], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="card-tag">{e(t["kind"])}</span></span>'
            f'<span class="card-body"><{h} class="card-t">{e(t["name"])}</{h}><span class="card-p">{e(t["short"])}</span><span class="card-more">Open worksheet {ic("arrow")}</span></span></a>')


def loc_card(l, h="h3"):
    return (f'<a class="place rv" href="{loc_path(l)}">{img(l["photo"], sizes="(max-width:700px) 50vw, 300px", alt="")}<span class="place-in"><{h} class="place-t">{e(l["city"])}</{h}><span>{e(l["county"])}</span></span></a>')


def post_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="post-media" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:700px) 100vw, 380px", alt="")}</a>'
            f'<div class="post-body"><p class="post-meta">{nice} · {p["read"]} read</p><{h} class="post-t"><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>')


def county_tabs(hl="h3"):
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}<small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(COUNTIES))
    panels = "".join(
        f'<div class="county-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" data-panel>{img(p, sizes="(max-width:900px) 100vw, 560px", alt="")}<div class="county-txt"><{hl}>{e(n)}</{hl}><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p class="county-towns">{e(s)}</p></div></div>'
        for i, (k, n, s, t, perils, p) in enumerate(COUNTIES))
    return f'<div class="counties" data-tabs><div class="county-tabs" role="tablist" aria-label="Delaware counties">{tabs}</div>{panels}</div>'


def home():
    home_faqs = [
        ("What does a Delaware Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When is it worth calling a Delaware Insurance Appraiser?", "When coverage is accepted, you have the insurer’s estimate, and the gap between it and your contractor’s number is meaningful — generally more than several thousand dollars or about 10%."),
        ("Is the appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign. That’s why your documentation should be solid before appraisal is invoked."),
        ("What does appraisal cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you cover my part of Delaware?", "Yes — all three counties. We regularly work in Wilmington, Newark, Bear, Middletown, Dover, Smyrna, Milford, Georgetown, Seaford, Lewes, Rehoboth Beach and Bethany Beach."),
    ]
    roads = "".join(f'<li class="road-step"><span class="road-n">{i + 1}</span><div class="road-c rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(STEPS[:6]))
    storms = "".join(f'<li class="storm rv"><span class="storm-y">{y}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for y, n, t in STORMS)
    svc = "".join(svc_card(s) for s in SERVICES[:9])
    tools = "".join(tool_card(t) for t in TOOLS[:6])
    places = "".join(loc_card(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero-coastal-home", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent claim appraisal · New Castle · Kent · Sussex</p>
<h1>Delaware Insurance Appraiser for claims that came up short</h1>
<p class="lede">Your insurer agreed the damage is covered, then sent a number that won’t pay for the repair. Delaware Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#services">See our services {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Local repair pricing</li><li>{ic("check")}Homes, condos &amp; commercial</li></ul>
</div>
<div class="hero-form">{quick_form()}</div>
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap"><ul class="ledger-in">
<li><b data-count="3">3</b><span>Counties served, every town</span></li>
<li><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></li>
<li><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim worksheets</span></li>
<li><b>2 of 3</b><span>Signatures make an award binding</span></li>
</ul></div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-txt rv">
<p class="kicker dark">Covered isn’t the same as paid</p>
<h2>What a Delaware Insurance Appraiser actually does</h2>
<p>Most disputed claims in the First State aren’t denials. They’re short: a roof approved for repair when the shingles can’t be matched, a water loss scoped for one room when the floor runs through three, a coastal home where wind damage was written off as flood. A Delaware Insurance Appraiser exists for the gap between “covered” and “paid in full.”</p>
<p>When either side invokes the appraisal clause, Delaware Insurance Appraiser can be the appraiser you name. We inspect the property ourselves, price the repair for your town — Wilmington labor isn’t Seaford labor — and work line by line with the insurer’s appraiser until the numbers meet or an umpire decides.</p>
<ul class="ticks">
<li>{ic("check")}<span><b>A fresh scope, not an edited one.</b> Our own measurements and photos come first.</span></li>
<li>{ic("check")}<span><b>Numbers built to hold up.</b> An inflated estimate loses the umpire; a supported one moves the award.</span></li>
<li>{ic("check")}<span><b>Straight answers.</b> If your claim needs an attorney or a supplement instead, you’ll hear it on the first call.</span></li>
</ul>
<a class="btn btn-slate" href="{P_ABOUT}">Who we are {ic("arrow")}</a>
</div>
<div class="intro-media rv">
<figure class="fig-a">{img("inspector-clipboard", sizes="(max-width:900px) 90vw, 460px")}</figure>
<figure class="fig-b">{img("roof-shingles", sizes="(max-width:900px) 60vw, 300px")}</figure>
<p class="intro-badge">{ic("shield")}<span><b>Hired by you</b>Never by the insurer on your claim</span></p>
</div>
</div></section>

<section class="sec sec-mist"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Three counties, three claim climates</p><h2>How a Delaware Insurance Appraiser reads each county</h2><p>Delaware is small — just three counties — but a rowhome fire in Wilmington, a hail-damaged roof in Dover and a wind-versus-flood fight in Bethany Beach are different claims. Pick a county to see what we look for there.</p></div>
{county_tabs()}
</div></section>

<section class="sec" id="services"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker dark">Appraisal &amp; estimating</p><h2>Services from Delaware Insurance Appraiser</h2></div><p>Eleven services built around one job: a valuation of your loss that stands up in front of an appraisal panel. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="cards" data-stagger>{svc}</div>
<p class="center-cta"><a class="btn btn-slate" href="{SVC_BASE}">All {len(SERVICES)} appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-deep" id="gap-check"><div class="wrap gap-wrap">
<div class="gap-copy rv"><p class="kicker">Quick check</p><h2>Is the gap big enough to appraise?</h2><p>Enter the two numbers you already have. A large gap is worth a conversation with a Delaware Insurance Appraiser; a small one is often closed faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}claim-gap-and-fee-estimator/">claim gap and fee estimator</a> subtracts appraiser and umpire fees so you can see a realistic net figure. All figures are illustrative.</p><a class="btn btn-coral" href="{TOOL_BASE}">All {len(TOOLS)} free worksheets {ic("arrow")}</a></div>
<div class="gap-tool rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap roadmap-wrap">
<div class="roadmap-head"><div class="sticky rv"><p class="kicker dark">The appraisal roadmap</p><h2>From short check to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here’s how Delaware Insurance Appraiser moves a file from the first call to the award.</p><a class="btn btn-slate" href="{P_ROAD}">Read the full roadmap {ic("arrow")}</a></div></div>
<ol class="road" data-road><span class="road-fill" aria-hidden="true"></span>{roads}</ol>
</div></section>

<section class="sec sec-sand"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Storm record</p><h2>The storms behind Delaware property claims</h2><p>Direct hurricane landfalls are rare here. Nor’easters, tropical remnants and summer storms are not. A Delaware Insurance Appraiser has to know how each one shows up on a roof, a wall and an estimate.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker dark">Free &amp; private</p><h2>Claim worksheets from a Delaware Insurance Appraiser</h2></div><p>Run the numbers before you call anyone. Every worksheet runs in your browser — nothing you type is stored or sent.</p></div>
<div class="cards" data-stagger>{tools}</div>
<p class="center-cta"><a class="link" href="{TOOL_BASE}wind-vs-flood-split-estimator/">New: the wind vs. flood split estimator for coastal homes {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-mist"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker dark">Statewide, on site</p><h2>Delaware Insurance Appraiser in your community</h2></div><p>We inspect in person in every town in all three counties. These are the communities where Delaware Insurance Appraiser handles claims most often.</p></div>
<div class="places" data-stagger>{places}</div>
<p class="center-cta"><a class="btn btn-slate" href="{LOC_BASE}">All Delaware communities {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right help first saves time and fees — and a Delaware Insurance Appraiser should tell you when appraisal is the wrong tool.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Appraiser (us)</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Prepare &amp; negotiate the claim</td><td>Legal disputes &amp; lawsuits</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, amount disputed</td><td>Early, from first notice</td><td>Denials, deadlines, conduct issues</td></tr>
<tr><th scope="row">Result</th><td class="hl">Binding award (2 of 3 signatures)</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec sec-mist"><div class="wrap faq-wrap">
<div class="rv"><p class="kicker dark">FAQ</p><h2>Questions people ask a Delaware Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-slate" href="{P_FAQ}">All questions {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker dark">Appraisal journal</p><h2>Read before you invoke appraisal</h2></div><p>Practical guides on policy language, coastal storms and documentation, written for Delaware property owners.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="sec sec-deep" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to a Delaware Insurance Appraiser about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="contact-lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Coverage</small>New Castle, Kent &amp; Sussex counties</span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", pick_title(f"{BRAND} | Claim Appraisal & Umpire", f"{BRAND} | Claim Appraisal"),
                        pick_desc(f"{BRAND}: independent appraisal, estimate review and umpire services for underpaid wind, hurricane, nor’easter and water claims."),
                        body, schema, photo="hero-coastal-home", main_entity=DOMAIN + "/#business"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(svc_card(r) for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        art = f"""{s["body"]}<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}<h2>Related services</h2><div class="cards cards-3">{related}</div>"""
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], s["photo"], s["facts"]) + layout(art, call_box() + list_box("All services", items, path) + list_box("Where we work", locs + [("All Delaware communities", LOC_BASE)])) + cta_band()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Delaware"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph(s['photo'])}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=s["photo"]), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(svc_card(s, "h2") for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in Delaware",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "roofer-at-work") + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec sec-mist"><div class="wrap faq-wrap"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review gives you that answer within days, and many disputes end there.</p><a class="btn btn-slate" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle residential and commercial claims?", "Yes — houses, rowhomes, condos, multifamily, retail, office, warehouses, farms, churches and HOA properties."), ("Which perils do you handle?", "Wind, tornado, hurricane, nor’easter, hail, water, fire and smoke, plus other covered perils.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist_schema(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Delaware | All 11",
                             "Delaware insurance appraisal services: appraisal clause representation, estimate review, storm, water, fire and winter claims, plus umpire work.",
                             body, schema, photo="roofer-at-work"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Serving Delaware", LOC_BASE), (l["city"], path)]
        near = "".join(loc_card(LOC_BY[n]) for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        art = f"""<div class="local-card"><div><h2 class="local-h">{e(l["city"])} at a glance</h2><dl class="local-dl"><div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Neighborhoods</dt><dd>{e(l["hoods"])}</dd></div><div><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div></dl></div><div><p class="local-k">Local claim risks</p><ul class="chips">{chips}</ul></div></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area:</p>
<ul class="cols-2">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2><div class="places places-3">{near}</div>"""
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], l["photo"],
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, call_box() + list_box("Delaware communities", items, path) + list_box("Free worksheets", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Delaware"}}, "url": DOMAIN + path}]
        c = l["city"]
        title = pick_title(f"Insurance Appraiser in {c}, DE | Claim Disputes", f"Insurance Appraiser in {c}, DE | Appraisal", f"{c}, DE Insurance Appraiser", f"{c} DE Insurance Appraiser")
        county = l["county"].replace(" counties", "").replace(" County", "")
        desc = pick_desc(f"Insurance appraiser for {c}, DE ({county} County area): independent appraisal and estimate review for underpaid storm, water and fire claims.",
                         f"Insurance appraiser for {c}, Delaware: independent appraisal and estimate review for underpaid storm, water and fire claims.",
                         f"Insurance appraiser for {c}, DE: appraisal and estimate review for underpaid storm, water and fire claims.")
        write(path, document(path, title, desc, body, schema, photo=l["photo"]), 0.8)

    trail = [("Home", "/"), ("Serving Delaware", LOC_BASE)]
    places = "".join(loc_card(l, "h2") for l in LOCATIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All Three Delaware Counties",
                     f"{BRAND} works in every community in New Castle, Kent and Sussex counties — from the Pennsylvania line to the Maryland border at Delmar and Fenwick Island.", "delaware-beach-dunes") + f"""
<section class="sec"><div class="wrap"><div class="places" data-stagger>{places}</div></div></section>
<section class="sec sec-mist"><div class="wrap"><div class="sec-head rv"><p class="kicker dark">By county</p><h2>How claims differ across Delaware</h2><p>The same policy language plays out very differently in a Wilmington rowhome, a Kent County farmhouse and a Bethany Beach cottage on pilings.</p></div>{county_tabs()}</div></section>
{cta_band("Don’t see your town?", "We cover every community in all three counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraisers Serving All of Delaware",
                             "Insurance appraisal in New Castle, Kent and Sussex counties: Wilmington, Newark, Dover, Milford, Georgetown, Lewes, Rehoboth and Bethany Beach.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist_schema([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="delaware-beach-dunes"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Worksheets", TOOL_BASE), (t["name"], path)]
        others = "".join(tool_card(TOOLS[(idx + k) % len(TOOLS)]) for k in (1, 2, 3))
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], t["photo"], cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and nothing you enter is stored.</p></div></section>""" + layout(
            f'{t["explain"]}<h2>Questions about this worksheet</h2>{faq_block(t["faqs"])}<h2>More free worksheets</h2><div class="cards cards-3">{others}</div>',
            call_box() + list_box("All worksheets", items, path)) + cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=t["photo"]), 0.8)

    trail = [("Home", "/"), ("Worksheets", TOOL_BASE)]
    cards = "".join(tool_card(t, "h2") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Worksheets for Delaware",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Use them to understand your claim, check the insurer’s math and plan your next step — no sign-up, nothing stored.", "calculator-paperwork", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec sec-mist"><div class="wrap faq-wrap"><div class="rv"><p class="kicker dark">A sensible order</p><h2>Using the worksheets together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}policy-deadline-calendar/">claim deadline calendar</a> so nothing lapses.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-pitch-and-squares-calculator/">roof pitch and squares calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}named-storm-deductible-worksheet/">hurricane deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-worksheet/">RCV/ACV holdback</a> calculators.</li><li>Coastal home? Try the <a href="{TOOL_BASE}wind-vs-flood-split-estimator/">wind vs. flood split estimator</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}claim-gap-and-fee-estimator/">claim gap and fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-check/">appraisal readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist_schema(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Worksheets & Calculators",
                              "Free claim worksheets: gap and fee estimator, RCV/ACV holdback, roof squares, hurricane deductible, deadline calendar and wind vs. flood split.",
                              body, schema, photo="calculator-paperwork"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Appraisal roadmap", P_ROAD), ("Questions answered", P_FAQ), ("Claim terms", P_GLOSS), ("Appraisal journal", POST_BASE)]

    path = P_ROAD
    trail = [("Home", "/"), ("Appraisal roadmap", path)]
    body = page_hero(trail, "Process guide", "The Delaware Insurance Appraisal Roadmap, Step by Step",
                     "Eight stages from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "inspector-clipboard",
                     [("Stages", str(len(STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(PROCESS_BODY, call_box() + list_box("Resources", learn_items, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Delaware", "description": "The stages of a property insurance appraisal, from the written demand to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(STEPS)]}
    write(path, document(path, "Delaware Insurance Appraisal Roadmap | 8 Steps",
                         "Step-by-step roadmap of insurance appraisal in Delaware: the written demand, choosing appraisers and an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="inspector-clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Questions answered", path)]
    toc = "".join(f'<li><a href="#faq-{i}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = f'<nav class="toc" aria-label="FAQ topics"><p class="local-k">Jump to a topic</p><ul>{toc}</ul></nav>' + "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions, Answered for Delaware",
                     "Plain answers to the questions we hear most, grouped by topic: the process, Delaware specifics, costs, timing and working with us.", "consultation") + layout(groups, call_box() + list_box("Resources", learn_items, path)) + cta_band("Didn’t see your question?", "Call or email — we’re happy to talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ for Delaware Property Owners",
                         "Answers to common insurance appraisal questions in Delaware: how it works, costs, timing, the FAIR plan, flood and when the award is binding.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="consultation"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#t-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="t-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>'
    art = f'<div class="filter"><label for="term-filter">Search {len(GLOSSARY)} terms</label><input id="term-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="filter-none" hidden>No terms match that search.</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Property Insurance Claim Terms, Defined",
                     f"{len(GLOSSARY)} words you’ll meet in policies, estimates and appraisal awards, explained in plain English.", "calculator-paperwork", cta=False) + layout(art, call_box() + list_box("Resources", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms | ACV, RCV, Umpire & More",
                         "A searchable glossary of property insurance claim terms: actual cash value, replacement cost, holdback, appraisal award, umpire, O&P and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-paperwork"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Journal", POST_BASE), (p["title"], path)]
        others = "".join(post_card(POSTS[(idx + k) % len(POSTS)]) for k in (1, 2, 3))
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        body = page_hero(trail, f"Journal · {p['read']} read · {nice}", p["title"], e(p["summary"]), p["photo"], cta=False) + layout(
            f'{p["body"]}<h2>Keep reading</h2><div class="posts posts-3">{others}</div>',
            call_box() + list_box("Resources", learn_items) + list_box("Free worksheets", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_band()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph(p['photo'])}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=p["photo"]), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Journal", path)]
    cards = "".join(post_card(p, "h2") for p in POSTS)
    body = page_hero(trail, "Appraisal journal", "The Delaware Appraisal Journal",
                     "Practical guides on policy language, coastal storms, documentation and claim strategy for Delaware property owners.", "laptop-spreadsheet", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Appraisal Journal | Guides for Delaware Owners",
                         "Guides for Delaware property owners on the appraisal clause, wind vs. flood, nor’easter damage, reading estimates and choosing the right help.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist_schema([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="laptop-spreadsheet"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("Who we are", path)]
    art = f"""<figure class="lead-img">{img("consultation", sizes="(max-width:1000px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on the amount of loss — what the covered damage actually costs to repair — and we’ve built our process, worksheets and documentation standards around answering that question well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate might look good on day one, but it costs credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, farms, business owners, contractors, public adjusters and attorneys across Delaware. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes — no honest appraiser can — and we don’t publish testimonials or “results” that could set false expectations.</p>
<h2>Why Delaware</h2>
<p>A state with three counties still holds a wide range of claims: rowhomes and Riverfront condos in Wilmington, subdivisions in Middletown and Bear, farms and poultry houses around Georgetown, and elevated beach homes from Lewes to Fenwick Island. Working the whole state means we see every kind of loss it produces and price each one with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"Who We Are at {BRAND}",
                     "Estimators and appraisers who believe a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.", "inspector-clipboard") + layout(art, call_box() + list_box("Explore", [("Our services", SVC_BASE), ("Communities", LOC_BASE), ("Free worksheets", TOOL_BASE), ("Appraisal roadmap", P_ROAD)])) + cta_band()
    write(path, document(path, f"Who We Are | {BRAND}",
                         f"{BRAND} is an independent appraisal and estimating practice focused on the amount of loss on disputed Delaware property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="inspector-clipboard"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec sec-deep"><div class="wrap contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm ET</span></li><li>{ic("pin")}<span><small>Service area</small>All of Delaware — New Castle, Kent &amp; Sussex</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks plain"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The insurer’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the insurer</span></li><li>{ic("check")}<span>Photos and any contractor estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | {PHONE}",
                         f"Get a free review of your disputed Delaware property claim. Call or text {PHONE} or email {EMAIL} to reach us.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect the information you choose to give — such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when required by law.</p>
<h2>Claim worksheets</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. We may use a tag manager and analytics to understand how visitors use the site. Fonts are loaded from Google Fonts, which may log standard request data under Google’s privacy policy.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        P_TERMS: ("Terms of Use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Delaware.</p>
<h2>No professional relationship</h2><p>Reading this site, using its worksheets or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a Delaware attorney for legal questions.</p>
<h2>Worksheets and estimates</h2><p>Calculators give planning estimates based on what you enter. They aren’t appraisals, quotes or predictions of any claim outcome. Example figures are illustrative.</p>
<h2>Intellectual property</h2><p>Site content, design and worksheets belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{P_CRED}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent permitted by law, we aren’t liable for decisions made based on its content or worksheets.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Delaware.</p>""", "The terms that apply when you use this website and its worksheets."),
        P_DISC: ("Disclaimer", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award. We do not publish testimonials or client results.</p>
<h2>Deadlines</h2><p>Policies contain deadlines, including for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If a deadline is approaching, talk to a Delaware attorney promptly.</p>
<h2>Statutes, agencies and storms</h2><p>References to Delaware law, the Delaware Department of Insurance, the state’s FAIR plan, the NFIP or past storms are general context. Verify current law and facts with official sources such as the Delaware Department of Insurance.</p>
<h2>Photographs</h2><p>Photos on this site are royalty-free CC0 and public-domain images used for illustration. They do not show our clients’ properties.</p>""", "Important limits on the information published on this website."),
        P_CRED: ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. No attribution is legally required, but we credit the sources here with thanks. Photos are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site."),
    }
    titles = {P_PRIV: "Privacy Policy", P_TERMS: "Terms of Use", P_DISC: "Disclaimer", P_CRED: "Photo Credits"}
    for path, (title, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal" if path != P_CRED else "Credits", title, lede, "office-building", cta=False) + layout(content, call_box())
        desc = pick_desc(f"{titles[path]} for {BRAND} ({HOST}): {lede}", f"{titles[path]} for {BRAND}: {lede}")
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="office-building"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("Who we are", P_ABOUT), ("Contact us", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Delaware communities", [("All communities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim worksheets", [("All worksheets", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal roadmap", P_ROAD), ("Questions answered", P_FAQ), ("Claim terms", P_GLOSS), ("Appraisal journal", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIV), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC), ("Photo credits", P_CRED)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "office-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="map-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Delaware communities, free claim worksheets, guides and legal pages.", body, [crumbs_schema(trail)], photo="office-building"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-media">{img("rough-surf", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page washed out with the tide</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn btn-coral" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Services</a><a class="btn btn-line light" href="{TOOL_BASE}">Free worksheets</a><a class="btn btn-line light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow", photo="rough-surf"), sitemap=False)


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
// Delaware Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$dia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$dia_real  = 'delawareinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$dia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://delawareinsuranceappraiser.com - only on the real domain.
if ($dia_host === 'www.' . $dia_real || ($dia_host === $dia_real && $dia_proto === 'http')) {
    header('Location: https://' . $dia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $dia_m)) {
    $dia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $dia_m[1] . $dia_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($dia_host !== $dia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Delaware Insurance Appraiser - front controller for the static build.
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
    used = {"hero-coastal-home", "office-building", "rough-surf", "inspector-clipboard", "roof-shingles", "consultation", "calculator-paperwork", "laptop-spreadsheet", "roofer-at-work", "delaware-beach-dunes"}
    used |= {s["photo"] for s in SERVICES} | {l["photo"] for l in LOCATIONS} | {t["photo"] for t in TOOLS} | {p["photo"] for p in POSTS} | {c[-1] for c in COUNTIES}
    missing = sorted(k for k in used if k not in PHOTOS)
    if missing:
        print("WARN missing photos (substituted):", missing)
        subs = {"delaware": "hero-coastal-home"}
        for k in missing:
            FALLBACK[k] = next((v for p, v in subs.items() if k.startswith(p) and v in PHOTOS), next(iter(PHOTOS)))
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
