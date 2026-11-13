#!/usr/bin/env python3
"""Static site generator for newjerseyinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Only the Python 3 standard library is needed.
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

BRAND = "New Jersey Insurance Appraiser"
HOST = "newjerseyinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = "GTM-WFQ9FC4S"
# Head snippet exactly as supplied by the site owner (output only when GTM_ID is set).
GTM_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WFQ9FC4S"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

SVC_BASE = "/appraisal-practice/"
LOC_BASE = "/garden-state-coverage/"
TOOL_BASE = "/claim-toolbox/"
RES_BASE = "/resource-center/"
ART_BASE = RES_BASE + "articles/"
PROC_PATH = RES_BASE + "appraisal-process/"
FAQ_PATH = RES_BASE + "faq/"
GLOSS_PATH = RES_BASE + "glossary/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-nj/"


def loc_label(l):
    return f"{l['city']}, NJ"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

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
    "appraisal-demand-representation": "consultation", "homeowners-insurance-appraisal": "hero-home",
    "condo-hoa-commercial-appraisal": "condo-building", "roof-and-hail-damage": "hailstones",
    "wind-tornado-claims": "tornado-house", "hurricane-noreaster-claims": "casino-pier",
    "water-ice-dam-pipe-claims": "icicles", "fire-smoke-loss-appraisal": "burned-house",
    "pinelands-wildfire-claims": "pine-barrens", "tree-fall-ice-storm-claims": "fallen-trees",
    "carrier-estimate-review": "calculator", "neutral-umpire-services": "meeting",
}
LOC_PHOTO = {
    "newark": "city-rowhouses", "jersey-city": "condo-building", "paterson": "brick-homes", "hackensack": "suburb-street",
    "edison": "hero-home", "morristown": "snow-house", "trenton": "porch-rowhouses", "toms-river": "sandy-aftermath",
    "long-branch": "long-branch", "cherry-hill": "tornado-street", "atlantic-city": "atlantic-city", "ocean-city": "cape-may-shore",
}
TOOL_PHOTO = {
    "claim-gap-net-recovery-estimator": "calculator", "acv-holdback-calculator": "paperwork",
    "roof-pitch-squares-calculator": "roof-edge", "hurricane-deductible-calculator": "coast-breach",
    "claim-calendar-builder": "calendar-clipboard", "appraisal-readiness-checkup": "meeting",
    "fallen-tree-coverage-calculator": "fallen-trees",
}
POST_PHOTO = {
    "new-jersey-appraisal-clause-explained": "consultation", "wind-versus-flood-lessons-from-sandy": "marina-storm",
    "hurricane-deductibles-in-new-jersey": "storm-field", "documenting-ice-dam-and-frozen-pipe-claims": "water-damage",
    "reading-a-carrier-estimate-line-by-line": "paperwork", "appraiser-public-adjuster-or-attorney-in-nj": "meeting",
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
    "roof": '<path d="M2 13L12 4l10 9"/><path d="M5 11v9h14v-9"/><path d="M15 4h3v4"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "pine": '<path d="M12 2l-5 7h3l-4 6h4l-3 5h10l-3-5h4l-4-6h3z"/><path d="M12 20v2"/>',
    "tree": '<path d="M12 22v-6"/><circle cx="12" cy="9" r="6"/><path d="M9 16l3-3 3 3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h8"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "gauge": '<path d="M12 14l4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-demand-representation": "doc", "homeowners-insurance-appraisal": "home", "condo-hoa-commercial-appraisal": "building",
    "roof-and-hail-damage": "roof", "wind-tornado-claims": "wind", "hurricane-noreaster-claims": "storm",
    "water-ice-dam-pipe-claims": "drop", "fire-smoke-loss-appraisal": "flame", "pinelands-wildfire-claims": "pine",
    "tree-fall-ice-storm-claims": "tree", "carrier-estimate-review": "file", "neutral-umpire-services": "scale",
}
TOOL_ICON = {
    "claim-gap-net-recovery-estimator": "calc", "acv-holdback-calculator": "percent", "roof-pitch-squares-calculator": "roof",
    "hurricane-deductible-calculator": "storm", "claim-calendar-builder": "cal", "appraisal-readiness-checkup": "gauge",
    "fallen-tree-coverage-calculator": "tree",
}


def mark():
    """Brand mark: an appraisal dial (arc + needle) in amber on deep ink."""
    return ('<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="13" fill="#2a1e08"/>'
            '<path d="M10.5 31a13.5 13.5 0 0 1 27 0" fill="none" stroke="#FFCA66" stroke-width="4.2" stroke-linecap="round"/>'
            '<path d="M24 31l7.2-9" stroke="#fff6e3" stroke-width="3.6" stroke-linecap="round"/>'
            '<circle cx="24" cy="31" r="3.4" fill="#FFCA66"/><path d="M14 37.5h20" stroke="#FFCA66" stroke-width="2.6" stroke-linecap="round" opacity=".55"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "NJ", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NJ", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for New Jersey property claims that came up short",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 21 New Jersey counties.",
        "areaServed": [{"@type": "State", "name": "New Jersey"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hurricane deductibles", "Wind and flood claims", "Nor’easter damage"],
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
    return {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All 12 services", SVC_BASE)),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All 21 counties", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("Open the toolbox", TOOL_BASE)),
        ("Resources", [("Appraisal process", PROC_PATH), ("FAQ", FAQ_PATH), ("Glossary", GLOSS_PATH), ("Articles", ART_BASE)], ("Resource center", RES_BASE)),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 6 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += '<li><a class="top-link" href="/about-us/">About</a></li><li><a class="top-link" href="/contact-us/">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += '<li><a class="acc-link" href="/about-us/">About</a></li><li><a class="acc-link" href="/contact-us/">Contact</a></li>'

    brand = f'{mark()}<span class="brand-t"><b>New Jersey</b><span>Insurance Appraiser</span></span>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="head" id="top"><div class="wrap head-in">
<a class="brand" href="/" aria-label="{BRAND} home">{brand}</a>
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn amber head-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/" aria-label="{BRAND} home">{brand}</a><button class="drawer-x" type="button" aria-label="Close menu" data-close>{_x()}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="/contact-us/">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 21 counties</small></div>
</aside>"""


def _x():
    return '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18"/></svg>'


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Carrier’s number won’t cover the repair? Let’s compare estimates.</h2><div class="btn-row"><a class="btn ink" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ink-line" href="/contact-us/">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about"><a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>New Jersey</b><span>Insurance Appraiser</span></span></a>
<p>Independent appraisal and estimating for property owners with disputed insurance claims, from High Point to Cape May Point.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm ET</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Locations</h3><ul>{loc}<li><a href="{LOC_BASE}">All New Jersey</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Company</h3><ul><li><a href="/about-us/">About us</a></li><li><a href="{RES_BASE}">Resource center</a></li><li><a href="{PROC_PATH}">Appraisal process</a></li><li><a href="{FAQ_PATH}">FAQ</a></li><li><a href="{GLOSS_PATH}">Glossary</a></li><li><a href="/contact-us/">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="/site-index/">Site index</a></li></ul>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general; policy terms vary, and results depend on the facts of each claim.</p></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="/contact-us/">{ic("mail")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return "<!-- Google Tag Manager -->\n" + GTM_SNIPPET + "\n<!-- End Google Tag Manager -->\n"


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, trail=None):
    canonical = DOMAIN + path
    page_type, extra = "WebPage", []
    trail = trail or ([("Home", "/")] if path == "/" else None)
    nodes = list(schema or [])
    if trail and not any(n.get("@type") == "BreadcrumbList" for n in nodes):
        nodes.insert(0, crumbs_schema(trail))
    for n in nodes:
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
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
        extra.append(n)
    img_key = preload or "hero-home"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if any(n.get("@type") == "BreadcrumbList" for n in extra):
        webpage["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    main = None
    for pref in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
        main = next((n["@id"] for n in extra if n.get("@type") == pref), None)
        if main:
            break
    webpage["mainEntity"] = {"@id": main or DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<script>document.documentElement.className="js"</script>
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across New Jersey">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across New Jersey">
<meta name="geo.region" content="US-NJ">
<meta name="geo.placename" content="New Jersey">
<meta name="theme-color" content="#2a1e08">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=Space+Grotesk:wght@500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
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
    # Directory pages are written as dir/index.php: the host serves real files without running the root
    # front controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if "<?" in content:
        raise SystemExit(f"PHP open tag in page HTML: {path}")
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
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="/contact-us/">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.12"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box callbox"><h2 class="box-t">Talk through your claim</h2><p>The first conversation is free. We’ll tell you honestly whether appraisal fits.</p><a class="callbox-num" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ink" href="/contact-us/">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_band(h="Have a claim that doesn’t add up?", p="Send us the carrier’s estimate. We’ll read it and tell you what we see."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn ink" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ink-line" href="/contact-us/">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


LOSSES = ["Roof / hail", "Wind / tornado", "Hurricane / nor’easter", "Water / ice dam / pipe", "Fire / smoke", "Wildfire / smoke", "Fallen tree", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=2):
    roles = ["Homeowner", "Condo / HOA board", "Commercial owner", "Property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in New Jersey"]
    return f"""<form class="form card" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="/privacy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn amber wide" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="hform card" action="/api/contact.php" method="post" data-lead novalidate>
<div class="hform-top"><span class="hform-k">Free claim review</span><h2 class="hform-t">Is your settlement short?</h2><p class="sub">Two minutes. We call back within one business day.</p></div>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div class="row2"><div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="/privacy/">privacy policy</a>.</span></label>
<button class="btn amber wide" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
<p class="hform-note">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("gateway", "Gateway North Jersey", "Bergen · Essex · Hudson · Passaic · Union", ["River & flash flooding", "Multi-family water losses", "Flat roofs", "Condo towers"],
     "The most densely built part of the state, from Hudson River condo towers to Paterson’s multi-family blocks. Claims here often involve several units, shared roofs and water that moves between floors.",
     "Newark, Jersey City, Paterson, Hackensack, Elizabeth, Hoboken", "city-rowhouses"),
    ("skylands", "Skylands & Highlands", "Morris · Sussex · Warren · Hunterdon", ["Ice dams", "Heavy snow", "Tree fall", "Frozen pipes"],
     "Higher ground and colder winters. Heavy wet snow, ice storms and big hardwoods make tree and winter water losses the main event, as the Halloween nor’easter of 2011 showed.",
     "Morristown, Parsippany, Newton, Flemington, Phillipsburg", "snow-house"),
    ("central", "Central Jersey", "Middlesex · Somerset · Mercer", ["Inland flooding", "Wind & hail", "Commercial roofs", "Rowhouse fires"],
     "The Raritan basin floods in big tropical rains, from Floyd in 1999 to Ida in 2021. Postwar suburbs, Route 1 commerce and Trenton’s rowhouses fill the claim files.",
     "Edison, New Brunswick, Trenton, Princeton, Somerville, Bound Brook", "suburb-street"),
    ("shore", "The Jersey Shore", "Monmouth · Ocean · Atlantic · Cape May", ["Nor’easters", "Wind vs. flood", "Hurricane deductibles", "Seasonal-home freezes"],
     "Barrier islands, bay towns and elevated rebuilds. Every major storm raises the same questions: which damage was wind, which was water, and which deductible applies.",
     "Long Branch, Toms River, Atlantic City, Ocean City, Cape May", "sandy-aftermath"),
    ("south", "South Jersey & the Pinelands", "Camden · Burlington · Gloucester · Salem · Cumberland", ["Derecho winds", "Tornadoes", "Wildfire smoke", "Farm buildings"],
     "Philadelphia suburbs give way to farms and the Pine Barrens. Derechos, the 2021 Mullica Hill tornado and Pinelands wildfires all shape claims here.",
     "Cherry Hill, Mount Laurel, Mullica Hill, Vineland, Hammonton", "pine-barrens"),
]

STORMS = [
    ("1962", "Ash Wednesday Storm", "A three-day nor’easter reshaped the shore. Lesson: nor’easters can do hurricane-scale damage without a hurricane deductible."),
    ("1999", "Tropical Storm Floyd", "Record flooding along the Raritan basin. Lesson: inland homes need flood coverage too."),
    ("Aug 2011", "Hurricane Irene", "Came ashore near Little Egg Inlet and flooded river towns. Lesson: wind and water claims arrive together."),
    ("Oct 2011", "Halloween nor’easter", "Heavy snow on leafy trees across North Jersey. Lesson: debris limits rarely cover big trees."),
    ("Jun 2012", "South Jersey derecho", "Straight-line winds toppled trees and roofs in minutes. Lesson: document wind damage before cleanup."),
    ("Oct 2012", "Superstorm Sandy", "Landfall near Brigantine and record surge. Lesson: hurricane deductibles depend on exact trigger wording."),
    ("Sep 2021", "Ida’s remnants", "Flash floods and the Mullica Hill tornado. Lesson: basement water is often a flood or endorsement question."),
    ("Apr 2025", "Jones Road Wildfire", "About 15,000 acres burned in Ocean County. Lesson: smoke damage reaches homes the fire never touched."),
]


def home():
    K = BRAND
    perils = [("Roofs & hail", "roof"), ("Nor’easters", "storm"), ("Ice dams", "drop"), ("Fallen trees", "tree"), ("Fire & smoke", "flame"), ("Condo & HOA", "building")]
    chips = "".join(f"<li>{ic(i)}{e(p)}</li>" for p, i in perils)

    feat = SERVICES[:2]
    rest = SERVICES[2:]
    svc_cards = "".join(
        f'<a class="scard{" feat" if s in feat else ""} rv" href="{SVC_BASE}{s["slug"]}/"><span class="scard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="scard-n">{i + 1:02d}</span><span class="scard-b"><span class="scard-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(feat + rest))

    storms = "".join(f'<li class="storm rv"><span class="storm-y">{e(y)}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for y, n, t in STORMS)

    proc = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><div class="step-b rv"><h3>{e(t)}</h3><p>{e(p.split(". ")[0])}.</p></div></li>' for i, (t, p) in enumerate(PROCESS_STEPS))

    regions = "".join(
        f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:800px) 100vw, 40vw", alt="")}</div><div class="region-b"><p class="region-c">{e(s)}</p><h3>{e(n)}</h3><p>{e(t)}</p><ul class="pchips">{"".join(f"<li>{e(x)}</li>" for x in pl)}</ul><p class="region-t"><b>Towns:</b> {e(c)}</p></div></article>'
        for k, n, s, pl, t, c, ph in REGIONS)

    tools = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tcard-ic">{ic(TOOL_ICON[t["slug"]])}</span></span><span class="tcard-b"><span class="kind">{e(t["kind"])}</span><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)

    cities = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><span>{e(l["county"])}</span>{ic("arrow")}</a></li>' for l in LOCATIONS)
    posts = "".join(f'<article class="pcard rv"><a class="pcard-ph" href="{ART_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pcard-b"><p class="meta">{p["read"]} read</p><h3><a href="{ART_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your named appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster is licensed by the state to manage and negotiate the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal, and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful, usually more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, yes, once any two of the three panel members sign. That’s why the file should be complete before anyone demands appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee terms in writing before any work starts, and the first conversation is free."),
        (f"Does a {K} cover the whole state?", "Yes. We work in all 21 counties, from Sussex and Bergen to Cumberland and Cape May."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="pill"><i></i>Independent appraisal · All 21 counties</p>
<h1>{K}: a second, independent number for claims that came up short</h1>
<p class="lede">When your insurer accepts the claim but the check won’t cover the repair, {K} builds a line-by-line valuation of the damage and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="#services">See our services {ic("arrow")}</a></div>
<ul class="hero-chips">{chips}</ul>
</div>
{hero_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap ledger-in">
<div class="lg"><b data-count="21">21</b><span>New Jersey counties served</span></div>
<div class="lg"><b data-count="564">564</b><span>municipalities, one standard of work</span></div>
<div class="lg"><b data-count="12">12</b><span>appraisal &amp; estimating services</span></div>
<div class="lg"><b data-count="7">7</b><span>free claim tools, nothing stored</span></div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-ph rv-l"><figure class="ip1">{img("roofers-lift", sizes="(max-width:900px) 90vw, 460px")}</figure><figure class="ip2">{img("water-damage", sizes="(max-width:900px) 60vw, 300px")}</figure><p class="ip-note"><b>Covered ≠ paid in full.</b> Most short claims aren’t denied. They’re just missing pieces.</p></div>
<div class="rv-r">
<p class="kicker">Why owners call</p>
<h2>Why owners call a {K} instead of arguing by phone</h2>
<p>A missing roof slope. Plaster priced as drywall. A two-family house valued as one unit. Code items nobody counted. A {K} exists for that space between “your claim is covered” and “your repair is paid for.”</p>
<ul class="ticks">
<li>{ic("check")}<div><b>We start from the property, not their estimate.</b> Our own inspection, measurements and photos.</div></li>
<li>{ic("check")}<div><b>Numbers built to survive an umpire.</b> Supportable beats inflated every time.</div></li>
<li>{ic("check")}<div><b>Straight answers on the first call.</b> If you need an attorney or a simple supplement instead, we’ll say so.</div></li>
</ul>
<a class="btn ink" href="/about-us/">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Twelve services</p><h2>What a {K} can take off your plate</h2><p>Every service is built around one job: an accurate valuation of your loss that holds up when the other side checks it. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="sgrid" data-stagger>{svc_cards}</div>
</div></section>

<section class="sec storms-sec"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker">Storm record</p><h2>Eight storms that taught a {K} what to look for</h2></div><p>New Jersey’s big losses rarely fit the textbook. Each of these events changed how claims are scoped, split between policies or argued.</p></div>
</div>
<ol class="storm-track" data-stagger>{storms}</ol>
</section>

<section class="sec ink-sec"><div class="wrap proc-wrap">
<div class="proc-intro rv-l"><p class="kicker light">The process</p><h2>Seven steps from a short estimate to a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. This is how a {K} moves a file from first call to award.</p><a class="btn amber" href="{PROC_PATH}">Read the full process guide {ic("arrow")}</a></div>
<ol class="steps"><span class="steps-fill" aria-hidden="true"></span>{proc}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Five regions</p><h2>From the Skylands to Cape May, a {K} prices local damage</h2><p>The same policy language plays out differently in a Paterson two-family, a Morristown Victorian and an Ocean City duplex. A {K} has to know how each region’s weather shows up on a roof and in an estimate.</p></div>
<div class="regions" data-stagger>{regions}</div>
</div></section>

<section class="sec amber-sec" id="gap-check"><div class="wrap split">
<div class="rv-l"><p class="kicker">Quick check</p><h2>Is the gap big enough to appraise?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a {K} makes sense. If it’s small, a documented supplement request may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}claim-gap-net-recovery-estimator/">claim gap &amp; net recovery estimator</a> adds appraiser and umpire fees and shows three outcomes.</p></div>
<div class="rv-r">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Seven free tools from a {K}</h2><p>Run the numbers before you pick up the phone. Every tool works in your browser, and nothing you type is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tools}</div>
<p class="center"><a class="btn line-dark" href="{TOOL_BASE}">Open the claim toolbox {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="loc-hero rv">{img("atlantic-city", sizes="100vw", alt="", extra=' data-parallax="0.1"')}<div class="loc-hero-b"><p class="kicker light">Statewide</p><h2>Where a {K} inspects most often</h2><p>We cover every county. These are the communities where {K} handles claims most often.</p></div></div>
<ul class="cities" data-stagger>{cities}</ul>
<p class="center"><a class="link" href="{LOC_BASE}">See all 21 counties {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and fees, and a {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">{K}</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Prepare &amp; negotiate the claim</td><td>Legal disputes &amp; lawsuits</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Binding award (2 of 3 signatures)</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Works for</th><td class="hl">The side that names them, or neither side as umpire</td><td>The policyholder, under a state license</td><td>The client</td></tr>
</tbody></table></div>
</div></section>

<section class="sec tint"><div class="wrap split top">
<div class="rv-l"><p class="kicker">Questions</p><h2>What people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn ink" href="{FAQ_PATH}">All FAQs {ic("arrow")}</a><a class="btn line-dark" href="{GLOSS_PATH}">Glossary</a></div></div>
<div class="rv-r">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Articles</p><h2>Read this before you demand appraisal</h2><p>Practical guides from the {K} team on policy language, documentation and strategy.</p></div>
<div class="pgrid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{ART_BASE}">All articles {ic("arrow")}</a></p>
</div></section>

<section class="pcta">{img("storm-field", "pcta-bg", alt="", extra=' data-parallax="0.2"')}<div class="wrap pcta-in rv"><p class="kicker light">Before you sign a release</p><h2>Check the numbers while you still can</h2><p>A short review now can keep you from accepting a settlement that won’t cover the work.</p><div class="btn-row"><a class="btn amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn glass" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv-l"><p class="kicker">Start here</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth it. No pressure, no obligation.</p>
<ul class="clines"><li><span class="clines-ic">{ic("phone")}</span><div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="clines-ic">{ic("mail")}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="clines-ic">{ic("clock")}</span><div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="clines-ic">{ic("pin")}</span><div><small>Coverage</small><b>All 21 New Jersey counties</b></div></li></ul></div>
<div class="rv-r">{lead_form(page="/", hlevel=3)}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "New Jersey Insurance Appraiser: independent appraisal, estimate review and umpire services for short roof, storm, water and fire claims.",
                        body, schema, preload="hero-home", trail=[("Home", "/")]), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a class="rel" href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}{ic("arrow")}</a>' for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[idx % 3::3][:5]]
        ph = SVC_PHOTO[s["slug"]]
        article = s["body"] + f'<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}<h2>Related services</h2><div class="related">{related}</div>'
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(article, call_box() + list_box("All services", items, path) + list_box("Where we work", locs + [("All New Jersey locations", LOC_BASE)])) + cta_band()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "New Jersey"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><span class="k">{ic(SVC_ICON[s["slug"]])} Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in New Jersey",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "roof-edge") + f"""
<section class="sec"><div class="wrap"><div class="ilist" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv-l"><p class="kicker">Not sure where to start?</p><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what each gap is worth. A review answers that in days, and many disputes end there.</p><a class="btn ink" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv-r">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle both homes and commercial buildings?", "Yes: houses, two-families, condos, associations, retail, office, warehouses and houses of worship."), ("Do you work on flood claims?", "We focus on the homeowners or commercial side. Where wind and flood overlap, we help keep the two claims separate.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in New Jersey | 12 Services",
                             "Twelve New Jersey insurance appraisal services: appraisal demands, roof, storm, water, fire, wildfire and tree claims, estimate review and umpires.",
                             body, schema, preload="roof-edge"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a class="rel" href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}{ic("arrow")}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        article = f"""<div class="note"><b class="h">Local claim risks</b><ul class="pchips">{chips}</ul></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="related">{near}</div>"""
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"])]) + layout(article, call_box() + list_box("New Jersey locations", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", New Jersey"}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        title = f"Insurance Appraiser in {l['city']}, NJ | Claim Disputes"
        if len(title) > 58:
            title = f"Insurance Appraiser in {l['city']}, NJ"
        desc = f"Independent insurance appraiser serving {l['city']} and {l['county']}: appraisal and estimate review for short storm, water and fire claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {l['city']} and {l['county']}: appraisal and estimate review for short storm, water and fire claims."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cities = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><span>{e(l["county"])}</span>{ic("arrow")}</a></li>' for l in LOCATIONS)
    reg = "".join(f'<article class="region rv"><div class="region-ph">{img(ph, sizes="(max-width:800px) 100vw, 40vw", alt="")}</div><div class="region-b"><p class="region-c">{e(s)}</p><h3>{e(n)}</h3><p>{e(t)}</p><ul class="pchips">{"".join(f"<li>{e(x)}</li>" for x in pl)}</ul><p class="region-t"><b>Towns:</b> {e(c)}</p></div></article>' for k, n, s, pl, t, c, ph in REGIONS)
    counties = ["Atlantic", "Bergen", "Burlington", "Camden", "Cape May", "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon", "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"]
    clist = "".join(f"<li>{c}</li>" for c in counties)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 21 New Jersey Counties",
                     f"{BRAND} works statewide, from the Kittatinny Ridge to Cape May Point. These local pages cover the communities where we handle claims most often.", "atlantic-city") + f"""
<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="kicker">Featured communities</p><h2>Twelve New Jersey cities and towns</h2></div><ul class="cities" data-stagger>{cities}</ul></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across New Jersey</h2><p>The same policy language plays out very differently in a Jersey City condo, a Morristown Victorian and an Ocean City duplex.</p></div><div class="regions" data-stagger>{reg}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="kicker">Every county</p><h2>All 21 counties we serve</h2></div><ul class="county-list rv">{clist}</ul></div></section>
{cta_band("Don’t see your town?", "We cover all 21 counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "New Jersey Insurance Appraiser Locations | 21 Counties",
                             "Insurance appraisal in all 21 New Jersey counties, including Newark, Jersey City, Paterson, Edison, Trenton, Toms River and Atlantic City.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload="atlantic-city"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim toolbox", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a class="rel" href="{TOOL_BASE}{o["slug"]}/"><small>{e(o["kind"])}</small>{e(o["name"])}{ic("arrow")}</a>' for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint tool-hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and nothing you type is stored.</p></div></section>""" + layout(t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2><div class="related">{others}</div>', call_box() + list_box("All claim tools", items, path)) + cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Claim toolbox", TOOL_BASE)]
    tiles = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tcard-ic">{ic(TOOL_ICON[t["slug"]])}</span></span><span class="tcard-b"><span class="kind">{e(t["kind"])}</span><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    T = TOOL_BASE
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for New Jersey Owners",
                     "Seven calculators and planners built from real appraisal work. Check the carrier’s math, see your deductible in dollars and plan your deadlines. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv-l"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="olist"><li>Start with the <a href="{T}claim-calendar-builder/">claim calendar builder</a> so no deadline slips.</li><li>Check roof math with the <a href="{T}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’re owed with the <a href="{T}hurricane-deductible-calculator/">hurricane deductible</a>, <a href="{T}acv-holdback-calculator/">ACV &amp; holdback</a> and <a href="{T}fallen-tree-coverage-calculator/">fallen tree</a> calculators.</li><li>Test the dispute with the <a href="{T}claim-gap-net-recovery-estimator/">claim gap estimator</a>.</li><li>Finish with the <a href="{T}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol></div><div class="rv-r">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for NJ Owners",
                              "Seven free claim tools: gap and fee estimator, ACV holdback, roof squares, hurricane deductible, fallen tree, deadline calendar and readiness.",
                              body, schema, preload="calculator"), 0.9)


# ---------------------------------------------------------------- resources
def resource_pages():
    res_items = [("Appraisal process guide", PROC_PATH), ("Appraisal FAQ", FAQ_PATH), ("Claim glossary", GLOSS_PATH), ("Articles", ART_BASE)]

    path = PROC_PATH
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Appraisal process", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _p) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in New Jersey",
                     "Seven steps from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", "clipboard",
                     [("Steps", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(f'<nav class="toc" aria-label="Steps"><p class="toc-t">On this page</p><ol>{toc}</ol></nav>' + PROCESS_BODY, call_box() + list_box("Resource center", res_items, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in New Jersey", "description": "The seven steps of a property insurance appraisal, from the written demand to the signed award.", "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in New Jersey | 7 Steps",
                         "Step-by-step guide to New Jersey insurance appraisal: the written demand, naming appraisers, choosing an umpire, negotiation and the award.",
                         body, [crumbs_schema(trail), howto], preload="clipboard"), 0.8)

    path = FAQ_PATH
    trail = [("Home", "/"), ("Resources", RES_BASE), ("FAQ", path)]
    jump = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for New Jersey Owners",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, deadlines, costs, New Jersey specifics and working with us.", "kitchen") + layout(f'<div class="jump">{jump}</div>' + groups, call_box() + list_box("Resource center", res_items, path)) + cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ | New Jersey Costs & Deadlines",
                         "Answers to common New Jersey insurance appraisal questions: how it works, deadlines, costs, hurricane deductibles and the state FAIR Plan.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="kitchen"), 0.8)

    path = GLOSS_PATH
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll see in New Jersey policies, estimates and appraisal awards, defined in plain English. Type to filter.", "paperwork", cta=False) + layout(f'<div class="gfilter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="hint" data-gcount></p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl><p class="gnone" hidden>No terms match that search.</p>', call_box() + list_box("Resource center", res_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More",
                         "Plain-English definitions of 40 property insurance claim terms: ACV, replacement cost, holdback, hurricane deductible, umpire, O&P and more.",
                         body, [crumbs_schema(trail), dts], preload="paperwork"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{ART_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Resources", RES_BASE), ("Articles", ART_BASE), (p["title"], path)]
        others = "".join(f'<a class="rel" href="{ART_BASE}{o["slug"]}/"><small>Article</small>{e(o["title"])}{ic("arrow")}</a>' for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Article · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + layout(p["body"] + f'<p class="byline">Written by the {BRAND} team. General information, not legal advice.</p><h2>Keep reading</h2><div class="related">{others}</div>', call_box() + list_box("Resource center", res_items) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_band()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = ART_BASE
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Articles", path)]
    cards = "".join(f'<article class="pcard rv"><a class="pcard-ph" href="{ART_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pcard-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{ART_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Articles", "Insurance Appraisal Articles for New Jersey Owners",
                     "Practical guides on policy language, documentation and claim strategy, written for New Jersey property owners.", "marina-storm", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pgrid" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Articles for New Jersey Owners",
                         "Articles for New Jersey property owners on the appraisal clause, wind versus flood, hurricane deductibles, water claims and reading estimates.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{ART_BASE}{p["slug"]}/') for p in POSTS])], preload="marina-storm"), 0.7)

    path = RES_BASE
    trail = [("Home", "/"), ("Resources", path)]
    hub = [
        ("Appraisal process guide", PROC_PATH, "Seven steps from the written demand to a signed award.", "clipboard", "doc"),
        ("Appraisal FAQ", FAQ_PATH, f"{len(allq)} answers grouped by topic, including New Jersey specifics.", "kitchen", "file"),
        ("Claim glossary", GLOSS_PATH, f"{len(GLOSSARY)} searchable terms, from ACV to Xactimate.", "paperwork", "calc"),
        ("Articles", ART_BASE, f"{len(POSTS)} practical guides on policies, storms and estimates.", "marina-storm", "home"),
    ]
    cards = "".join(f'<a class="icard rv" href="{p}"><span class="icard-ph">{img(ph, sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><span class="k">{ic(icn)} Resource</span><h2>{e(n)}</h2><p>{e(t)}</p></span></a>' for n, p, t, ph, icn in hub)
    body = page_hero(trail, "Resource center", "Insurance Appraisal Resource Center",
                     "Guides, answers and definitions for New Jersey property owners working through a disputed claim.", "clipboard", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ilist" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Insurance Appraisal Resource Center | New Jersey",
                         "Free resources for New Jersey property owners: an appraisal process guide, a grouped FAQ, a searchable glossary and practical claim articles.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(n, p) for n, p, *_r in hub])], preload="clipboard"), 0.8)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = "/about-us/"
    trail = [("Home", "/"), ("About", path)]
    article = f"""<figure class="lead-img">{img("consultation", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll tell you.</li>
<li><strong>Fees in writing.</strong> You’ll know what it costs before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, association boards, property managers, houses of worship, business owners, contractors and attorneys across New Jersey. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t guarantee outcomes, because no honest appraiser can.</p>
<h2>Statewide on purpose</h2>
<p>New Jersey packs a lot of different risk into a small state: ice and big trees in the Skylands, dense multi-family housing in the Gateway cities, inland flooding in the Raritan basin, coastal storms at the shore and wildfire in the Pinelands. Working in all 21 counties means we see every kind of loss the state produces and price each one with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "meeting") + layout(article, call_box() + list_box("Explore", [("Our services", SVC_BASE), ("Locations", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROC_PATH)])) + cta_band()
    write(path, document(path, f"About Us | {BRAND}",
                         "New Jersey Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="meeting"), 0.7)

    path = "/contact-us/"
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv-l"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="clines"><li><span class="clines-ic">{ic("phone")}</span><div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="clines-ic">{ic("mail")}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="clines-ic">{ic("clock")}</span><div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="clines-ic">{ic("pin")}</span><div><small>Service area</small><b>All 21 New Jersey counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="plain-list"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv-r">{lead_form(page=path, hlevel=3)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Get a free review of your disputed New Jersey property claim. Call or text (844) 537-1427, email us, or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · via {e(v["via"])}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in sorted(PHOTOS.items()))
    legal = {
        "/privacy/": ("Privacy Policy", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web server also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you type aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used to understand site traffic in aggregate.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share."),
        "/terms/": ("Terms of Use", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in New Jersey.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing on this site is legal advice. Policies differ, and laws and court decisions change. Ask a licensed New Jersey attorney about legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photos are used under the licenses listed on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of New Jersey.</p>""", "The terms that apply when you use this website and its tools."),
        "/disclaimer/": ("Disclaimer", f"""
<h2>General information only</h2><p>The content on this site is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site, including the default values in our tools, are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, replacement cost recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is close, talk to a New Jersey attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to laws, agencies and weather events are for context. Check current law and facts with official sources such as the New Jersey Department of Banking and Insurance.</p>""", "Important limits on the information published on this website."),
        "/photo-credits/": ("Photo Credits", f"""
<p>Every photograph on this site is either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or is a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and don’t show our clients’ properties. Titles are shown as published by the source, lightly shortened.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site."),
    }
    for path, (title, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "office-building", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", f"{title} for {BRAND} (newjerseyinsuranceappraiser.com): {lede}", body, [crumbs_schema(trail)], preload="office-building"), 0.3)


def sitemap_pages():
    path = "/site-index/"
    trail = [("Home", "/"), ("Site index", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", "/about-us/"), ("Contact us", "/contact-us/")]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim toolbox", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Resource center", RES_BASE), ("Appraisal process", PROC_PATH), ("FAQ", FAQ_PATH), ("Glossary", GLOSS_PATH), ("Articles", ART_BASE)] + [(p["title"], f'{ART_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy/"), ("Terms of use", "/terms/"), ("Disclaimer", "/disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="sm-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on {BRAND}, in one place.", "office-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="sm-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"A complete list of every page on {BRAND}: services, New Jersey locations, free claim tools, resources and legal pages.", body, [crumbs_schema(trail)], preload="office-building"), 0.3)

    body = f"""<section class="phero err"><div class="phero-bg">{img("storm-field", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="tag">Error 404</p><h1>That page isn’t here</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn amber" href="/">Home</a><a class="btn glass" href="{SVC_BASE}">Services</a><a class="btn glass" href="{TOOL_BASE}">Free tools</a><a class="btn glass" href="/contact-us/">Contact</a></div></div></section>"""
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
        f.write(GUARD_PHP.replace("__HOST__", HOST))


GUARD_PHP = r"""<?php
// New Jersey Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nja_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nja_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nja_proto = strtolower(trim(explode(',', $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'))[0]));
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($nja_host === 'www.' . $nja_real || ($nja_host === $nja_real && $nja_proto === 'http')) {
    header('Location: https://' . $nja_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$nja_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nja_uri, '?'), $nja_m)) {
    $nja_q = strpos($nja_uri, '?') !== false ? substr($nja_uri, strpos($nja_uri, '?')) : '';
    header('Location: ' . $nja_m[1] . $nja_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($nja_host !== $nja_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// New Jersey Insurance Appraiser - front controller for the static build.
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
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.php')) {
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
    resource_pages()
    company_pages()
    sitemap_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
