#!/usr/bin/env python3
"""Static site generator for illinoisinsuranceappraiser.com.

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

BRAND = "Illinois Insurance Appraiser"
HOST = "illinoisinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114a"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no GTM snippet is output.
GTM_ID = ""
# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraiser-services/"
LOC_BASE = "/cities-we-serve/"
TOOL_BASE = "/calculators-and-planners/"
POST_BASE = "/policyholder-articles/"
P_ABOUT = "/about-the-firm/"
P_CONTACT = "/contact-an-appraiser/"
P_PROCESS = "/illinois-appraisal-process/"
P_FAQ = "/appraisal-questions/"
P_GLOSS = "/insurance-claim-terms/"
P_PRIV = "/privacy-statement/"
P_TERMS = "/terms-and-conditions/"
P_DISC = "/important-disclaimer/"
P_MAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-il/"


def loc_short(l):
    return l["city"].split("–")[0]


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "chicago-lakefront-aerial": "Aerial view of downtown Chicago high-rises along the Lake Michigan shoreline",
    "chicago-skyline-night": "Chicago skyline lit up at night across the lake",
    "chicago-towers-park": "Chicago residential towers rising behind a green park",
    "chicago-night-aerial": "Chicago’s downtown towers and street grid glowing at night",
    "chicago-loop-street": "Street lined with tall buildings in downtown Chicago",
    "springfield-capitol": "Illinois State Capitol dome in Springfield under a blue sky",
    "peoria-brick-building": "Historic brick commercial building on a Peoria street corner",
    "illinois-cornfield": "Young corn growing under a bright summer sky",
    "fire-gutted-house": "House interior burned out to the framing after a fire",
    "shingle-rows": "Close-up of overlapping dark roof shingles",
    "storm-cloud-mono": "Towering storm cloud building in a dark sky",
    "snowy-suburban-home": "Suburban home with shrubs buried in fresh snow",
    "craftsman-bungalow": "Craftsman bungalow with a front porch and stone steps",
    "brick-two-story": "Brick-front two-story suburban home with a green lawn",
    "suburban-street": "Large suburban homes along a curving residential street",
    "team-meeting": "Several people working through documents together at a table",
    "signing-paperwork": "Person holding a pen over paperwork at a desk",
    "calculator-charts": "Calculator beside printed charts and a laptop keyboard",
    "calculator-sticky-note": "Calculator, pencil and sticky note on a desk",
    "contractors-plans": "Two contractors in safety vests reviewing construction plans",
    "conference-room": "Empty conference room with a long table and chairs",
    "tornado-debris-field": "Neighborhood reduced to debris and stripped trees after a violent tornado",
    "flooded-basement": "Basement stairwell flooded with muddy water after a storm",
    "joliet-victorian": "Restored Victorian home with a wraparound porch in Joliet’s Upper Bluff",
    "belleville-depot": "Historic brick railroad depot with a steep roof",
    "frozen-pipes": "Pipes encased in thick ice after a hard freeze",
    "prairie-supercell": "Supercell thunderstorm glowing over open grassland at sunset",
    "roofers-at-work": "Roofers working on the peak of a house roof",
    "illinois-river-bridge": "Stone arch bridge over a slow, wide river",
    "wind-torn-house": "House with its roof torn apart by tornado winds",
    "brick-apartments": "Three-story brick apartment building",
    "campus-brick-hall": "Brick campus building at the University of Illinois",
    "chicago-river-west": "Chicago’s River West neighborhood and skyline at night",
    "storm-wreckage": "Splintered lumber and debris scattered across a field after a tornado",
    "snow-cabin": "Wood cabin with a snow-covered roof in winter woods",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "named-appraiser-representation": "signing-paperwork", "illinois-homeowner-claim-appraisal": "craftsman-bungalow",
    "association-commercial-claim-appraisal": "brick-apartments", "hailstorm-roof-claim-appraisal": "roofers-at-work",
    "tornado-derecho-claim-appraisal": "wind-torn-house", "basement-backup-water-claim-appraisal": "flooded-basement",
    "fire-soot-smoke-claim-appraisal": "fire-gutted-house", "polar-vortex-freeze-claim-appraisal": "frozen-pipes",
    "household-contents-claim-appraisal": "team-meeting", "adjuster-estimate-audit": "calculator-charts",
    "impartial-umpire-appointments": "conference-room",
}
LOC_PHOTO = {
    "chicago": "chicago-lakefront-aerial", "aurora": "suburban-street", "naperville": "brick-two-story", "joliet": "joliet-victorian",
    "rockford": "snowy-suburban-home", "springfield": "springfield-capitol", "peoria": "peoria-brick-building", "champaign": "campus-brick-hall",
    "bloomington": "illinois-cornfield", "elgin": "craftsman-bungalow", "belleville": "belleville-depot", "carbondale": "storm-cloud-mono",
}
TOOL_PHOTO = {
    "disputed-amount-net-estimator": "calculator-sticky-note", "recoverable-depreciation-planner": "calculator-charts",
    "pitch-adjusted-roof-squares": "shingle-rows", "deductible-dollars-converter": "prairie-supercell",
    "illinois-claim-deadline-calendar": "signing-paperwork", "appraisal-file-strength-score": "contractors-plans",
    "sewer-backup-endorsement-gap": "flooded-basement",
}
POST_PHOTO = {
    "appraisal-clause-in-illinois-policies": "signing-paperwork", "section-155-and-appraisal-basics": "conference-room",
    "prairie-hail-roof-documentation": "roofers-at-work", "first-30-days-after-tornado-or-derecho": "storm-wreckage",
    "basement-backup-vs-flood-in-illinois": "flooded-basement", "siding-matching-disputes-illinois": "suburban-street",
}

# Hand-written meta descriptions for location pages (110–143 characters each).
LOC_DESC = {
    "chicago": "Chicago insurance appraiser for bungalows, two-flats and condos: appraisal and estimate review for underpaid basement, hail and fire claims.",
    "aurora": "Aurora, IL insurance appraiser for Fox Valley homes and HOAs: independent appraisal for underpaid hail, wind and basement water claims.",
    "naperville": "Naperville insurance appraiser for DuPage and Will County homes: appraisal for underpaid tornado, hail and finished-basement claims.",
    "joliet": "Joliet insurance appraiser serving Will County: independent appraisal and estimate review for disputed hail, wind and river-area claims.",
    "rockford": "Rockford insurance appraiser for Winnebago County: appraisal for underpaid ice dam, hail, tornado and frozen-pipe property claims.",
    "springfield": "Springfield, IL insurance appraiser for Sangamon County homes: appraisal for underpaid tornado, hail, tree and ice storm claims.",
    "peoria": "Peoria insurance appraiser for bluff homes and river businesses: appraisal for underpaid tornado, hail and slate roof claims.",
    "champaign": "Champaign–Urbana insurance appraiser for owners and landlords: independent appraisal for underpaid hail, wind and rental claims.",
    "bloomington": "Bloomington–Normal insurance appraiser for McLean County: appraisal and estimate review for underpaid hail, wind and ice claims.",
    "elgin": "Elgin insurance appraiser for Victorian and newer homes: independent appraisal for underpaid hail, ice dam and Fox River claims.",
    "belleville": "Belleville and Metro East insurance appraiser: independent appraisal for underpaid tornado, hail, brick masonry and water claims.",
    "carbondale": "Carbondale insurance appraiser for Southern Illinois: appraisal for underpaid derecho, tornado, ice storm and tree damage claims.",
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
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, cls="ico"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


MARK_PATHS = ('<rect width="48" height="48" rx="11" fill="#ff5f0f"/>'
              '<path d="M9.5 24.5L24 12l14.5 12.5" fill="none" stroke="#fff" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M15.5 31h17M15.5 37.5h10" fill="none" stroke="#2b1105" stroke-width="4" stroke-linecap="round"/>')


def mark():
    return f'<svg class="mark" width="42" height="42" viewBox="0 0 48 48" aria-hidden="true" focusable="false">{MARK_PATHS}</svg>'


def brand_link(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Illinois</b><span>Insurance Appraiser</span></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "IL", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-IL", "availableLanguage": "en"}],
        "slogan": "Covered isn’t the same as paid in full",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 102 Illinois counties.",
        "areaServed": [{"@type": "State", "name": "Illinois"}] + [{"@type": "City", "name": loc_short(l)} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Tornado and derecho damage", "Sewer backup claims"],
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
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("Every appraisal service", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Illinois cities", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All calculators & planners", TOOL_BASE)),
        ("Resources", [("Illinois appraisal process", P_PROCESS), ("Appraisal questions", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Policyholder articles", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 7 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "ico chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">About</a></li><li><a class="top-link" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ico chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{P_ABOUT}">About the firm</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head" id="top"><div class="wrap head-in">
{brand_link()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="call-pill" href="tel:{TEL}">{ic("phone")}<span><small>Free claim review</small>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link()}<button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · All 102 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Carrier’s number doesn’t cover the repair? <span>Let’s look at it line by line.</span></p><div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line-light" href="{P_CONTACT}">Email the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand_link("brand brand-foot")}
<p>Independent appraisal, estimate review and umpire services for property owners with disputed insurance claims — from Lake County to the Shawnee Hills.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri 8am–6pm CT</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul class="two">{loc}</ul></div>
<div><h2 class="foot-h">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Firm</h2><ul><li><a href="{P_ABOUT}">About the firm</a></li><li><a href="{P_PROCESS}">Appraisal process</a></li><li><a href="{P_FAQ}">Questions</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Articles</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Site content is general and educational; policy terms vary, and outcomes depend on the facts of each claim and are never guaranteed.</p>
<div class="foot-bottom"><span>© {date.today().year} {BRAND}</span><ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">All pages</a></li></ul></div></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top"><svg class="ring" width="52" height="52" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle cx="26" cy="26" r="23" fill="none" stroke="currentColor" stroke-opacity=".18" stroke-width="3"/><circle class="ring-p" cx="26" cy="26" r="23" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="144.5" stroke-dashoffset="144.5" transform="rotate(-90 26 26)"/></svg>{ic("up")}</a>
<div class="mobile-call"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
"""


def gtm_body():
    if not GTM_ID:
        return ""
    return f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, main_entity=None):
    canonical = DOMAIN + path
    page_type, extra_nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
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
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = preload or "chicago-lakefront-aerial"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    if main_entity is None:
        order = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")
        cands = sorted([n for n in extra_nodes if n.get("@type") in order], key=lambda n: order.index(n["@type"]))
        main_entity = cands[0]["@id"] if cands else DOMAIN + "/#business"
    webpage["mainEntity"] = {"@id": main_entity}
    graph = [org_schema(), site_schema(), webpage] + extra_nodes
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Illinois">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Illinois">
<meta name="geo.region" content="US-IL">
<meta name="geo.placename" content="Illinois">
<meta name="theme-color" content="#ff5f0f">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800;900&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,700;1,9..40,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>
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
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.1"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}<span class="pm" aria-hidden="true"></span></summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn full" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_band(h="Not sure the carrier’s estimate is right?", p="Send it over. We’ll review it and tell you what we see — free and without obligation."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn dark" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line-dark" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Tornado / derecho / wind", "Basement backup / water", "Frozen pipe / ice dam", "Fire / smoke", "Contents", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", sub="Free review, no obligation. Most replies within one business day.", page="/", level="h3"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Illinois"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{level} class="form-h">{e(heading)}</{level}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the carrier has paid or offered, and what you think is missing."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy statement</a>.</span></label></div>
<div class="full"><button class="btn full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-card" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hero-card-h">Get a free claim review</h2><p class="sub">Tell us the basics. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{P_PRIV}">privacy statement</a>.</span></label>
<button class="btn full" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Chicago & Cook County", "Bungalows, two-flats, towers", ["Basement backup", "Hail", "Freeze"],
     "Combined sewers, brick bungalows and lakefront condos. Basement backups after summer cloudbursts and pipes split by polar-vortex cold are as common here as storm damage.", "chicago-night-aerial", "chicago"),
    ("Collar counties", "DuPage · Kane · Lake · McHenry · Will", ["Tornadoes", "Hail", "HOA roofs"],
     "Subdivisions and townhome associations from Naperville to Waukegan. One hail swath can touch dozens of buildings under a single master policy.", "suburban-street", "naperville"),
    ("Northern Illinois", "Rockford · Elgin · Rock River Valley", ["Ice dams", "Heavy snow", "Wind"],
     "Long winters bring ice dams and snow load; spring brings tornadoes like the 2023 Belvidere storm. Older housing stock adds plaster and wood-siding matching questions.", "snowy-suburban-home", "rockford"),
    ("Central Illinois", "Peoria · Springfield · Bloomington · Champaign", ["Tornadoes", "Hail", "Ice storms"],
     "Open prairie lets storms arrive at full strength. Washington in 2013 and Springfield in 2006 show how severe central Illinois tornadoes can be.", "prairie-supercell", "peoria"),
    ("Metro East & Southern Illinois", "Belleville · Edwardsville · Carbondale", ["Derechos", "Tornadoes", "Earthquake endorsements"],
     "From the 1925 Tri-State Tornado to the 2009 derecho, southern Illinois has a long wind history — and sits near the New Madrid seismic zone.", "tornado-debris-field", "carbondale"),
]

STORMS = [
    ("1925", "Tri-State Tornado", "Crossed southern Illinois, including Murphysboro; still the deadliest tornado in U.S. history."),
    ("1990", "Plainfield tornado", "An F5 tornado struck Plainfield, Crest Hill and Joliet on August 28."),
    ("2011", "Groundhog Day Blizzard", "More than 20 inches of snow in Chicago, stranding drivers on Lake Shore Drive."),
    ("2013", "April floods & Washington tornado", "Basements flooded across Cook and DuPage in April; an EF-4 hit Washington in November."),
    ("2019", "Polar vortex", "Chicago fell below −20°F in January, splitting pipes in homes that had never frozen."),
    ("2020", "August derecho", "Hurricane-force gusts crossed northern Illinois, flattening crops, trees and roofs."),
    ("2021", "Naperville–Woodridge tornado", "An EF-3 tore through neighborhoods on the night of June 20."),
    ("2023", "Belvidere storms", "A March tornado collapsed part of a theater roof during a concert."),
]


def home():
    svc_cards = "".join(
        f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}<span class="num">{i + 1:02d}</span></span><span class="card-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES))

    steps = [
        ("Free review", "We read the policy, the carrier’s estimate and your photos, then tell you plainly whether appraisal fits."),
        ("Our own valuation", "We inspect, measure and build an independent line-item estimate priced for your Illinois ZIP code."),
        ("Written demand", "Appraisal is demanded in writing and we’re named as your appraiser within the policy’s window."),
        ("Panel work", "We work line by line with the carrier’s appraiser. Most disputes narrow sharply here."),
        ("Signed award", "Items still open go to a neutral umpire. Two of three signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="pstep"><span class="dot" aria-hidden="true">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    regions = "".join(
        f'<article class="region"><div class="region-ph">{img(ph, sizes="(max-width:700px) 85vw, 420px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-sub">{e(sub)}</p><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul><p>{e(t)}</p><a class="more" href="{loc_path(LOC_BY[link])}">{e(LOC_BY[link]["city"])} page {ic("arrow")}</a></div></article>'
        for n, sub, chips, t, ph, link in REGIONS)

    storms = "".join(f'<li class="storm rv"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for y, t, d in STORMS)

    tools = "".join(f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tico" aria-hidden="true">{t["icon"]}</span><span class="tb"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span>{ic("arrow")}</a>' for t in TOOLS)
    cities = "".join(f'<a class="city rv" href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a>' for l in LOCATIONS)
    posts = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        ("What does an Illinois Insurance Appraiser do?", "We value property damage when you and your insurer agree a loss is covered but disagree on what it costs. As your named appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When should I call an Illinois Insurance Appraiser?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful — usually more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, yes, once any two of the three panel members sign it. That’s why the file should be complete before appraisal is demanded."),
        ("Can appraisal get me Section 155 penalties?", "No. Section 155 of the Illinois Insurance Code is a remedy a court may consider in a lawsuit. Appraisal only sets the amount of loss. Talk to an Illinois attorney about legal remedies."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("chicago-lakefront-aerial", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · All 102 counties</p>
<h1>Illinois Insurance Appraiser <span>for claims that came up short</span></h1>
<p class="lede">Your carrier accepted the claim, but the check won’t rebuild the roof, the basement or the kitchen. As an Illinois Insurance Appraiser, we build an independent, line-by-line valuation and carry it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#services">See what we handle {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Named appraiser, not the carrier’s</li><li>{ic("check")}Pricing for your ZIP code</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="stats" aria-label="At a glance"><div class="wrap stats-in">
<div class="stat"><b data-count="102">102</b><span>Illinois counties served</span></div>
<div class="stat"><b data-count="11">11</b><span>Appraisal &amp; estimating services</span></div>
<div class="stat"><b data-count="7">7</b><span>Free claim calculators</span></div>
<div class="stat"><b>2 of 3</b><span>Signatures make an award binding</span></div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-ph rv">{img("roofers-at-work", sizes="(max-width:900px) 100vw, 46vw")}<p class="intro-tag"><b>Covered ≠ paid in full</b><span>Most disputed claims aren’t denied. They’re short.</span></p></div>
<div class="intro-b rv">
<p class="kicker">Why owners call</p>
<h2>What an Illinois Insurance Appraiser brings to a stuck claim</h2>
<p>A missed roof slope, siding that can’t be matched, a finished basement priced as bare concrete, code items nobody listed. An Illinois Insurance Appraiser exists for the gap between “we accept coverage” and a payment that actually covers the repair.</p>
<ol class="reasons">
<li><b>We start from zero.</b> Our own inspection and measurements, never an edited copy of the adjuster’s estimate.</li>
<li><b>We price what we can prove.</b> Numbers built to hold up in front of an umpire, which is what moves awards.</li>
<li><b>We triage honestly.</b> If your claim needs an attorney or a simple supplement instead, you’ll hear that on the first call.</li>
</ol>
<a class="btn dark" href="{P_ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Eleven services</p><h2>Claims an Illinois Insurance Appraiser can take on</h2><p>From a single estimate review to full panel representation and neutral umpire work. Every service is built around one goal: a valuation of your loss that holds up.</p></div>
<div class="cards" data-stagger>{svc_cards}</div>
<p class="center"><a class="btn line-dark" href="{SVC_BASE}">Compare all services {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Five steps</p><h2>How the appraisal clause moves a claim</h2><p>Appraisal turns an open-ended argument into a defined process with a binding result. Here is how an Illinois Insurance Appraiser takes a file from first call to signed award.</p></div>
<div class="process" data-process><span class="track" aria-hidden="true"><span class="fill"></span></span><ol class="psteps">{proc}</ol></div>
<p class="center"><a class="link" href="{P_PROCESS}">Read the full seven-stage Illinois appraisal process</a></p>
</div></section>

<section class="sec dark regions-sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker light">Five claim climates</p><h2>One state, five very different kinds of loss</h2><p>Basement backups in Chicago, HOA hail claims in DuPage, ice dams in Rockford, tornadoes on the central prairie, derechos in Little Egypt. An Illinois Insurance Appraiser has to read each region’s weather on a roof and in an estimate.</p>
<div class="scroller-nav"><button type="button" class="sbtn" data-scroll="-1" aria-label="Previous region">{ic("left")}</button><button type="button" class="sbtn" data-scroll="1" aria-label="Next region">{ic("right")}</button></div></div>
<div class="scroller" data-scroller tabindex="0" aria-label="Illinois regions">{regions}</div>
</div></section>

<section class="sec"><div class="wrap split">
<div class="rv"><p class="kicker">Check your numbers</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two figures you already have. A large gap is worth a conversation with an Illinois Insurance Appraiser; a small one may close faster with a documented supplement. The examples are illustrative.</p>
<p>Seven free tools, all running in your browser with nothing stored:</p>
<div class="trows">{tools}</div></div>
<div class="rv sticky-col">{GAP_MINI}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Illinois storm record</p><h2>Storms that shaped Illinois claims</h2><p>Every Illinois Insurance Appraiser file sits on top of this history: tornadoes, derechos, blizzards, floods and deep freezes that keep testing how policies are read.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="city-banner rv">{img("chicago-skyline-night", sizes="100vw", alt="", extra=' data-parallax="0.08"')}<div class="city-banner-b"><p class="kicker light">Statewide</p><h2>Illinois Insurance Appraiser service areas</h2><p>We work in every county. These are the cities where an Illinois Insurance Appraiser from our team handles claims most often.</p></div></div>
<div class="cities" data-stagger>{cities}</div>
<p class="center"><a class="link" href="{LOC_BASE}">See statewide coverage</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Picking the right help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Choosing first saves time and fees, and an Illinois Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="roles" data-stagger>
<div class="role hl rv"><h3>Illinois Insurance Appraiser</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Binding award on value</dd></dl></div>
<div class="role rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare &amp; negotiate the claim</dd><dt>Best stage</dt><dd>Early, from first notice</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></div>
<div class="role rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Coverage &amp; legal disputes</dd><dt>Best stage</dt><dd>Denials, deadlines, delay</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker">Questions</p><h2>Questions people ask an Illinois Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn dark" href="{P_FAQ}">All questions {ic("arrow")}</a><a class="btn line-dark" href="{P_GLOSS}">Claim terms glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Articles</p><h2>Read before you demand appraisal</h2><p>Practical articles from the Illinois Insurance Appraiser team on policy wording, documentation and timing.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All policyholder articles</a></p>
</div></section>

<section class="pcta">{img("prairie-supercell", "bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap pcta-in rv"><p class="kicker light">Storm season is claim season</p><h2>Check the numbers before you sign off on them</h2><p>A short review now can keep you from accepting a payment that won’t cover the repair.</p><div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec dark" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker light">Start with a conversation</p><h2>Talk to an Illinois Insurance Appraiser about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth it — no pressure and no obligation.</p>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 102 Illinois counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Illinois Insurance Appraiser: independent appraisal, estimate review and umpire help for underpaid hail, wind, water, freeze and fire claims.",
                        body, schema, preload="chicago-lakefront-aerial", main_entity=DOMAIN + "/#business"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All Illinois cities", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Illinois"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Illinois Claims",
                     "From one estimate review to full panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of your loss.", "contractors-plans") + f"""
<section class="sec"><div class="wrap"><div class="ilist" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Where to begin</p><h2>Most files start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that shortfall is worth. A review answers that in days, and plenty of disputes close right there.</p><a class="btn dark" href="{SVC_BASE}adjuster-estimate-audit/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one step?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and association claims?", "Yes — houses, condos, apartment buildings, retail, office, industrial, churches and townhome associations."), ("Is it only hail?", "No. We handle wind, tornado, derecho, water, freeze, fire, contents and other covered losses.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Illinois | 11 Services",
                             "Illinois insurance appraisal services: appraisal clause representation, estimate review, hail, tornado, water, freeze and fire claims.",
                             body, schema, preload="contractors-plans"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, Illinois", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks</b><ul class="chips">{chips}</ul><p class="housing"><b>Housing mix:</b> {e(l["housing"])}.</p></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and nearby communities, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} owners</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
<aside class="aside">{call_box()}{list_box("Illinois cities", items, path)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you honestly what we see.")}"""
        city = loc_short(l)
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Illinois", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "Illinois"}}, "url": DOMAIN + path}]
        title = f"{l['city']}, IL Insurance Appraiser | Claim Appraisal"
        if len(title) > 58:
            title = f"{l['city']}, IL Insurance Appraiser"
        write(path, document(path, title, LOC_DESC[l["slug"]], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cities = "".join(f'<a class="city rv" href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a>' for l in LOCATIONS)
    reg = "".join(f'<div class="icard rv"><span class="icard-ph">{img(ph, sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><small>{e(sub)}</small><h2>{e(n)}</h2><p>{e(t)}</p></span></div>' for n, sub, _c, t, ph, _l in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 102 Illinois Counties",
                     "We work statewide, from Lake County to Alexander County. These pages cover the cities where we handle claims most often, with local storm history and housing detail.", "chicago-river-west") + f"""
<section class="sec"><div class="wrap"><div class="cities" data-stagger>{cities}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">Regions</p><h2>How claims differ across Illinois</h2><p>The same policy wording plays out very differently in a Chicago two-flat, a Naperville cul-de-sac and a farmhouse outside Carbondale.</p></div><div class="ilist" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your city?", "We cover every Illinois county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Illinois Cities We Serve | Insurance Appraisal Statewide",
                             "Insurance appraisal in all 102 Illinois counties, including Chicago, Aurora, Naperville, Joliet, Rockford, Springfield, Peoria and Champaign.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f"{l['city']}, Illinois", loc_path(l)) for l in LOCATIONS])], preload="chicago-river-west"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and nothing you type is stored.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("All tools", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send us the estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Tools", TOOL_BASE)]
    rows = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="tico" aria-hidden="true">{t["icon"]}</span></span><span class="tcard-b"><small>{t["kind"]}</small><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open tool {ic("arrow")}</span></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Claim Calculators and Planners for Illinois",
                     "Seven tools built from real appraisal work. Use them to understand your claim, check the carrier’s math and decide what to do next — no sign-up, nothing stored.", "calculator-charts", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards" data-stagger>{rows}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}illinois-claim-deadline-calendar/">deadline calendar</a> so nothing lapses.</li><li>Check roof math with the <a href="{TOOL_BASE}pitch-adjusted-roof-squares/">pitch-adjusted squares calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}deductible-dollars-converter/">deductible converter</a>, the <a href="{TOOL_BASE}recoverable-depreciation-planner/">depreciation planner</a> and, for basements, the <a href="{TOOL_BASE}sewer-backup-endorsement-gap/">backup endorsement checker</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}disputed-amount-net-estimator/">disputed amount estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-file-strength-score/">file strength score</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators & Planners | Illinois",
                              "Seven free claim tools for Illinois owners: disputed amount, depreciation, roof squares, deductibles, deadlines and sewer backup limits.",
                              body, schema, preload="calculator-charts"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Illinois appraisal process", P_PROCESS), ("Appraisal questions", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Policyholder articles", POST_BASE)]

    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "The Illinois Insurance Appraisal Process, Step by Step",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "team-meeting",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_band()}"""
    step_names = ["Pin down the disagreement", "Make the written demand", "Each side names an appraiser", "Select an umpire", "Appraisers work the differences", "The umpire decides what’s left", "The award and payment"]
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Illinois", "description": "The seven stages of a typical Illinois property insurance appraisal.", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}"} for i, n in enumerate(step_names)]}
    write(path, document(path, "Illinois Insurance Appraisal Process | 7 Stages",
                         "The Illinois insurance appraisal process in seven stages: the written demand, naming appraisers, choosing an umpire and the binding award.",
                         body, [crumbs_schema(trail), howto], preload="team-meeting"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal questions", path)]
    jump = "".join(f'<li><a href="#faq-{i}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions from Illinois Owners",
                     "Plain answers to the questions we hear most — about the process, costs, timing and the Illinois rules around it.", "conference-room") + f"""
<div class="wrap layout"><article class="prose"><nav class="jump" aria-label="FAQ topics"><ul>{jump}</ul></nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Illinois Costs, Timing & Rules",
                         "Answers to common Illinois insurance appraisal questions, grouped by topic: basics, fees, deadlines, Illinois rules and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="conference-room"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Insurance Claim Terms Glossary",
                     f"{len(GLOSSARY)} words you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the box to filter.", "calculator-sticky-note", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count></p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "A searchable glossary of property insurance claim terms: actual cash value, replacement cost, appraisal award, umpire, Section 155 and more.",
                         body, [crumbs_schema(trail), dts], preload="calculator-sticky-note"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Articles", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Article · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Article", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "publisher": {"@id": DOMAIN + "/#business"}, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Articles", path)]
    cards = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Articles", "Policyholder Articles for Illinois Property Owners",
                     "Practical guides on policy wording, documentation and claim timing, written by people who work appraisal panels.", "brick-two-story", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Policyholder Articles | Illinois Insurance Appraisal Guides",
                         "Articles for Illinois property owners on appraisal clauses, Section 155, hail documentation, basement backup coverage and siding matching.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="brick-two-story"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About the firm", "About Illinois Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.", "contractors-plans") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("team-meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we only do appraisal</h2>
<p>Many claim professionals do a bit of everything. We chose to specialize. Illinois Insurance Appraiser works on one question — the amount of loss — and our process, tools and documentation standards are built around answering it well. That focus lets us act as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Support over spin.</strong> An inflated estimate may look good on day one, but it loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, association boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Illinois. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside appraisal. We don’t promise outcomes — no honest appraiser can. You won’t find testimonials or win-rate claims on this site, because every claim is different.</p>
<h2>Statewide on purpose</h2>
<p>Illinois weather changes a lot over 400 miles. Working statewide means we see every kind of loss the state produces — backups in Chicago, hail in DuPage, ice dams in Rockford, tornadoes around Peoria and derechos near Carbondale — and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", P_PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About the Firm | Illinois Insurance Appraiser",
                         "About Illinois Insurance Appraiser, an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="contractors-plans"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact an Illinois Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "signing-paperwork", cta=False) + f"""
<section class="sec dark"><div class="wrap contact">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>Statewide — all 102 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ready"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact an Illinois Insurance Appraiser | (844) 537-1427",
                         "Contact Illinois Insurance Appraiser for a free review of a disputed claim. Call or text (844) 537-1427, email us or send your claim details.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="signing-paperwork"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Statement", "How we collect, use and protect the information you share with us.",
                 "Our privacy statement explains what Illinois Insurance Appraiser collects through forms, calls and email, how it is used and your choices.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to share — such as your name, phone number, email address, property location and claim details. Our web server also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this statement will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To access, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        P_TERMS: ("Terms and Conditions", "The terms that apply when you use this website and its tools.",
                  "The terms and conditions for using the Illinois Insurance Appraiser website, its free claim tools and its contact forms. Please read them.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in Illinois.</p>
<h2>No client relationship</h2><p>Reading the site, using its tools or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. For legal questions, consult a licensed Illinois attorney.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates from the figures you enter. Example figures on the site are illustrative. None of it is an appraisal, a quote or a prediction of any outcome.</p>
<h2>Content ownership</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free images used for illustration and don’t show our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Illinois.</p>"""),
        P_DISC: ("Important Disclaimer", "Important limits on the information published on this website.",
                 "Important disclaimer for the Illinois Insurance Appraiser site: general information only, no legal advice and no guaranteed claim results.", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, don’t give legal advice and don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>Legal topics</h2><p>References to Illinois law, including Section 155 of the Illinois Insurance Code and limitation periods, are simplified general descriptions. They may not reflect recent changes or how a court would apply them to your facts.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an Illinois attorney promptly.</p>
<h2>Weather and history</h2><p>References to storms and events give context. Verify facts with official sources such as the National Weather Service and the Illinois Department of Insurance.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>"""),
    }
    for path, (title, lede, desc, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "chicago-loop-street", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], preload="chicago-loop-street"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("All pages", path)]
    groups = [
        ("Main", [("Home", "/"), ("About the firm", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(f"{l['city']}, IL", loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Illinois appraisal process", P_PROCESS), ("Appraisal questions", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Policyholder articles", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy statement", P_PRIV), ("Terms and conditions", P_TERMS), ("Important disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "All Pages", f"Every page on {BRAND}, grouped by section.", "chicago-towers-park", cta=False) + f'<section class="sec"><div class="wrap"><div class="mapgrid" data-stagger>{cols}</div></div></section>'
    flat = [(n, p) for _, links in groups for n, p in links]
    write(path, document(path, f"All Pages | {BRAND}", "Every page on the Illinois Insurance Appraiser site in one list: services, Illinois cities, free claim tools, articles and legal pages.",
                         body, [crumbs_schema(trail), item_list(flat)], preload="chicago-towers-park"), 0.3)

    body = f"""<section class="phero err"><div class="phero-media">{img("storm-cloud-mono", "bg", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker light">Error 404</p><h1>This page got blown off the map</h1><p class="lede">The page you wanted may have moved or never existed. These are good places to pick up again.</p><div class="btn-row"><a class="btn" href="/">Home</a><a class="btn line-light" href="{SVC_BASE}">Services</a><a class="btn line-light" href="{TOOL_BASE}">Free tools</a><a class="btn line-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "Sorry, that page isn’t on the Illinois Insurance Appraiser site. Use the links on this page to find services, tools or contact details.", body, robots="noindex,follow", preload="storm-cloud-mono"), sitemap=False)


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
    # Search Console verification file: exact bytes, no newline, wrapper, guard or BOM.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Illinois Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$iia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$iia_real  = 'illinoisinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$iia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://illinoisinsuranceappraiser.com - only on the real domain.
if ($iia_host === 'www.' . $iia_real || ($iia_host === $iia_real && $iia_proto === 'http')) {
    header('Location: https://' . $iia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $iia_m)) {
    $iia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $iia_m[1] . $iia_q, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($iia_host !== $iia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Illinois Insurance Appraiser - front controller for the static build.
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
