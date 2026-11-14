#!/usr/bin/env python3
"""Static site generator for newhampshireinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php (canonical-host guard + static HTML);
the homepage is home.html, served by the root index.php front controller.
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
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "New Hampshire Insurance Appraiser"
HOST = "newhampshireinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114b"
FAV = "1"
STATE = "New Hampshire"

# Google Tag Manager: leave empty until a container ID (GTM-XXXXXXX) is provided.
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/nh-appraisal-services/"
LOC_BASE = "/new-hampshire-cities/"
TOOL_BASE = "/nh-claim-calculators/"
POST_BASE = "/nh-appraisal-guides/"
P_PROCESS = "/how-nh-appraisal-works/"
P_FAQ = "/nh-appraisal-faq/"
P_GLOSS = "/nh-claim-glossary/"
P_ABOUT = "/about-our-appraisers/"
P_CONTACT = "/contact-nh-appraiser/"
P_PRIV = "/website-privacy/"
P_TERMS = "/nh-site-terms/"
P_DISC = "/nh-appraiser-disclaimer/"
P_MAP = "/nh-site-map/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
ALT = {
    "storm-sky-homes": "Dark storm clouds rolling over a row of suburban houses",
    "icicles-eaves": "Long icicles hanging from the eaves of a building",
    "icicles-brick": "Snow overhang and icicles along a roof edge above a brick wall",
    "snow-roof-chimney": "Deep snow covering a roof around a chimney under a blue sky",
    "ice-storm-limb": "Tree limbs split and coated in ice after an ice storm",
    "ice-storm-car": "Ice-coated tree limbs broken down onto a parked car beside a house",
    "fallen-trees-yard": "Large trees uprooted across a lawn near a single-story house",
    "fallen-trees-snow-road": "Cut sections of fallen trees pushed aside on a snowy roadside",
    "storm-collapsed-house": "Wood-frame house partly collapsed after a severe storm",
    "flood-damaged-homes": "Homes and a washed-out yard after tropical storm flooding",
    "roof-shingles-close": "Close-up of asphalt shingles on a sloped roof",
    "roof-edge-damage": "Damaged shingles curling at the edge of a roof",
    "roof-aerial-damage": "Aerial view of a shingle roof with missing and damaged patches",
    "roof-crew": "Roofers stripping and repairing the roof of a wooden building",
    "hailstorm": "Hailstones covering a street and roadside during a hailstorm",
    "lightning-night": "Multiple lightning bolts striking during a night thunderstorm",
    "gust-clouds": "Turbulent storm clouds churning in a dark sky",
    "noreaster-satellite": "Satellite view of a large nor’easter spinning off the East Coast",
    "snow-shoveling": "Person shoveling a path through deep snow after a snowstorm",
    "fire-damaged-house": "House with a burned-out roof after a fire",
    "woodstove-cabin": "Cabin interior with a wood stove, firewood and wooden walls",
    "inspection-visit": "Inspector with a tablet talking with a homeowner inside a damaged home",
    "consult-table": "Two women talking across a round table by a window",
    "consult-laptop": "Professionals reviewing figures on a laptop in a meeting",
    "calculator-notes": "Calculator, pencil and sticky note on a desk",
    "calculator-papers": "Scientific calculator resting on printed papers",
    "condo-building": "Four-story brick condominium building on a city street",
    "brick-mill": "Brick mill building with arched windows against a blue sky",
    "victorian-home": "Victorian house with a brick turret and a white picket fence",
    "colonial-home": "White colonial-style house with black shutters and a brick side",
    "porch-home": "Two-story family home with a covered front porch",
    "snow-day-house": "Snow-covered trees and a house on a snow day",
    "kitchen-interior": "Modern kitchen with white cabinets and an island",
    "concord-state-house": "The New Hampshire State House in Concord under a blue sky",
    "manchester-mills": "Brick Amoskeag mill buildings and clock tower in Manchester",
    "nashua-city-hall": "Nashua City Hall, a brick civic building in downtown Nashua",
    "portsmouth-aerial": "Aerial view of downtown Portsmouth and the Piscataqua River",
    "hampton-dunes": "Dunes and beach grass under storm clouds at Hampton Beach",
    "lebanon-library": "The classical-style Lebanon Public Library in Lebanon",
    "hanover-webster-hall": "Columned brick Webster Hall at Dartmouth College in Hanover",
    "laconia-mills": "Brick mill building beside the Winnipesaukee River",
    "wolfeboro-street": "Main Street in Wolfeboro with shops and a brick clock tower",
    "conway-covered-bridge": "The Saco River covered bridge in Conway",
    "lonesome-lake": "Lonesome Lake reflecting White Mountain peaks under a blue sky",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-representation-nh": "consult-table", "homeowners-claim-appraisal-nh": "colonial-home",
    "nh-commercial-hoa-appraisal": "condo-building", "roof-and-hail-appraisal": "roof-aerial-damage",
    "wind-microburst-tornado-appraisal": "storm-collapsed-house", "tropical-storm-hurricane-appraisal-nh": "flood-damaged-homes",
    "pipe-burst-water-appraisal": "kitchen-interior", "fire-smoke-soot-appraisal": "fire-damaged-house",
    "ice-dam-roof-snow-appraisal": "icicles-eaves", "falling-tree-claim-appraisal": "ice-storm-car",
    "insurer-estimate-audit": "calculator-papers", "appraisal-umpire-nh": "consult-laptop",
}
LOC_PHOTO = {
    "manchester-nh": "manchester-mills", "nashua-nh": "nashua-city-hall", "concord-nh": "concord-state-house",
    "portsmouth-nh": "portsmouth-aerial", "dover-nh": "brick-mill", "rochester-nh": "porch-home",
    "derry-nh": "colonial-home", "salem-nh": "victorian-home", "keene-nh": "fallen-trees-snow-road",
    "laconia-nh": "laconia-mills", "lebanon-hanover-nh": "hanover-webster-hall", "north-conway-nh": "conway-covered-bridge",
}
TOOL_PHOTO = {
    "gap-and-fee-estimator": "calculator-notes", "depreciation-holdback-planner": "calculator-papers",
    "roof-squares-pitch-tool": "roof-shingles-close", "percent-deductible-converter": "gust-clouds",
    "nh-claim-deadline-calendar": "snow-shoveling", "nh-appraisal-readiness-score": "inspection-visit",
    "snow-weight-roof-calculator": "snow-roof-chimney",
}
POST_PHOTO = dict(zip([p["slug"] for p in POSTS], ["icicles-brick", "fallen-trees-yard", "consult-table", "calculator-notes", "woodstove-cabin", "roof-edge-damage"]))

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
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(size=44):
    """Brand mark: navy tile, granite peaks, gold ridge line and sun."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#002A86"/>'
            '<circle cx="34" cy="14" r="4.5" fill="#EFAE0E"/>'
            '<path d="M6 37l11-16 6 8 5-6 14 14z" fill="#ffffff"/>'
            '<path d="M6 37l11-16 6 8 5-6 14 14" fill="none" stroke="#EFAE0E" stroke-width="2.6" stroke-linejoin="round"/>'
            '<path d="M17 21l3.2 4.6-3.2-1.6-3 2.2z" fill="#c9d6f2"/></svg>')


def brand(cls="brand", tag="Independent claim appraisal"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>{tag}</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "NH", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NH", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for property claims that came up short",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across New Hampshire.",
        "areaServed": [{"@type": "State", "name": STATE}] + [{"@type": "City", "name": n} for l in LOCATIONS for n in l["city"].split(" & ")],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Ice dam claims", "Roof snow load", "Umpire services"],
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
LEARN = [("How NH appraisal works", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All New Hampshire cities", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Learn", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" class="drop-btn" aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">About</a></li><li><a class="top-link" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="hdr-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-gold hdr-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 10 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="ftr">
<div class="ftr-cta"><div class="wrap"><h2>Covered on paper, short at the bank? Let’s line up the numbers.</h2><div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Send claim details</a></div></div></div>
<div class="wrap ftr-grid">
<div class="ftr-about">{brand("brand brand-light")}
<p>Independent appraisal and estimate review for New Hampshire property owners with disputed insurance claims — from the Seacoast to the Great North Woods.</p>
<ul class="ftr-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm ET</li></ul></div>
<div><h3>Appraisal work</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Communities</h3><ul class="cols2">{loc}</ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>The firm</h3><ul><li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li><li><a href="{P_PROCESS}">How appraisal works</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li></ul></div>
</div>
<div class="wrap ftr-base"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="wrap ftr-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Content on this site is general information; policy language controls and outcomes are never guaranteed.</p>
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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="storm-sky-homes", body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra.append(n)
    p = PHOTOS[photo]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    preload = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n'
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal">
<meta name="geo.region" content="US-NH">
<meta name="geo.placename" content="{STATE}">
<meta name="theme-color" content="#002A86">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{preload}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap">
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
    # Pages are dir/index.php: the host serves real files without running the front controller, so each page
    # starts with the canonical-host guard (www/http 301, /index.php 301, off-domain noindex).
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
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">›</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, chips=None, cta=True):
    ch = ""
    if chips:
        ch = '<ul class="phero-chips">' + "".join(f"<li><small>{e(k)}</small><b>{e(v)}</b></li>" for k, v in chips) + "</ul>"
    c = f'<div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{ch}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">A free first look</h2><p>A free first conversation. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow", "ico-sm")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def band(h="Does the insurer’s number actually cover the work?", p="Send us the insurer’s estimate. We’ll read it line by line and tell you what we see."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow", "ico-sm")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Ice dam / snow load", "Wind / microburst", "Hail", "Tree fall", "Frozen or burst pipe", "Fire / smoke", "Tropical storm / nor’easter", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Describe the loss", page="/", hlevel=3):
    roles = ["Homeowner", "Condo owner", "Landlord", "Commercial owner", "HOA / property manager", "Contractor", "Attorney or public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in New Hampshire"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead-card" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="lead-t">Get a call back</h2><p class="form-sub">Leave a number. We’ll call within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{P_PRIV}">privacy policy</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="lead-note">{ic("shield", "ico-sm")} No obligation. Nothing is shared.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("seacoast", "Seacoast", "Portsmouth · Dover · Hampton", "hampton-dunes", ["Nor’easter wind", "Wind-driven rain", "Salt-air wear disputes", "Historic homes"],
     "Eighteen miles of coastline, the Piscataqua River and Great Bay. Older homes in Portsmouth’s South End and Exeter meet newer subdivisions inland, and nor’easters test both."),
    ("valley", "Merrimack Valley", "Manchester · Nashua · Concord", "manchester-mills", ["Microbursts &amp; hail", "Burst pipes in multifamily", "Tree fall", "Mill-condo losses"],
     "The state’s population center. Summer storms track across Hillsborough and Merrimack counties, and multi-unit buildings turn one frozen pipe into several claims."),
    ("lakes", "Lakes Region", "Laconia · Wolfeboro · Meredith", "wolfeboro-street", ["Vacant-camp freeze-ups", "Ice dams", "Docks &amp; boathouses", "Ice storms"],
     "Lake Winnipesaukee’s shoreline is lined with seasonal camps that sit empty for months. Freeze-ups found in spring and ice damage to waterfront structures lead the claim list."),
    ("west", "Monadnock &amp; Upper Valley", "Keene · Lebanon · Hanover", "lebanon-library", ["River flooding", "Snow load", "Rental &amp; campus housing", "Downed hardwoods"],
     "Brick downtowns, river valleys and college-town rentals. Heavy wet snow and river flooding have both left their mark on Cheshire and Grafton counties."),
    ("north", "White Mountains &amp; North Country", "North Conway · Lincoln · Berlin", "lonesome-lake", ["Roof snow load", "Ski-condo HOA claims", "Ice storms", "Flash flooding"],
     "Elevation, deep snowpack and steep valleys. Carroll and Coös county claims often involve condominium associations, snow-load framing damage and storm runoff."),
]

MONTHS = [
    ("Jan", ["Ice dams", "Frozen pipes"], 3), ("Feb", ["Roof snow load", "Ice dams"], 3), ("Mar", ["Nor’easters", "Snowmelt leaks"], 2),
    ("Apr", ["Spring floods", "Thaw leaks"], 1), ("May", ["Wind", "Hail"], 1), ("Jun", ["Hail", "Lightning"], 2),
    ("Jul", ["Microbursts", "Hail"], 2), ("Aug", ["Tropical remnants", "Flash floods"], 2), ("Sep", ["Tropical storms", "Wind"], 1),
    ("Oct", ["Early snow", "Windstorms"], 2), ("Nov", ["Chimney fires", "Wind"], 1), ("Dec", ["Ice storms", "Wind &amp; rain"], 3),
]

STORMS = [
    ("1938", "The Great Hurricane of ’38", "Still the benchmark for wind damage in the state — a reminder that inland New Hampshire can see hurricane-force gusts."),
    ("1998", "North Country ice storm", "Ice-loaded limbs across the North Country and Lakes Region. Tree-fall and roof-impact claims dominated."),
    ("2006", "Mother’s Day floods", "Days of rain swelled rivers in the Lakes Region and Seacoast, separating flood-policy losses from homeowners claims."),
    ("2008", "Deerfield tornado &amp; December ice storm", "A rare EF2 tornado in July, then an ice storm that left hundreds of thousands without power in December."),
    ("2011", "Tropical Storm Irene &amp; “Snowtober”", "Irene’s flooding tore through White Mountain valleys; an October snowstorm then dropped heavy snow on trees still in leaf."),
    ("2015", "Record late-winter snowpack", "Weeks of accumulated snow led to ice dams, interior leaks and roof-load damage across southern New Hampshire."),
    ("2017", "Halloween-eve windstorm", "One of the largest power outages in state history and a wave of tree-on-house claims."),
    ("2023", "December 18 wind and rain", "Damaging gusts, heavy rain on frozen ground and river flooding, just before the holidays."),
]


def home():
    marquee_items = [l["city"] for l in LOCATIONS] + ["Exeter", "Hampton", "Bedford", "Londonderry", "Hudson", "Wolfeboro", "Littleton", "Berlin", "Claremont", "Peterborough"]
    marquee = "".join(f"<span>{e(t)}</span>" for t in marquee_items * 2)

    feat = SERVICES[8], SERVICES[0]
    rest = [s for s in SERVICES if s not in feat]
    svc_cards = "".join(
        f'<a class="pc{" pc-feat" if s in feat else ""} rv" href="{SVC_BASE}{s["slug"]}/"><span class="pc-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="pc-b"><span class="pc-k">{ic(s["icon"], "ico-sm")} {("Most asked about" if s is feat[0] else "Core service") if s in feat else "Service"}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="pc-go">Learn more {ic("arrow", "ico-sm")}</span></span></a>'
        for s in list(feat) + rest)

    months = "".join(f'<li class="mo lvl{lv} rv"><b>{m}</b>{"".join(f"<span>{p}</span>" for p in ps)}</li>' for m, ps, lv in MONTHS)

    steps = [
        ("Read the file", "Policy, declarations, the insurer’s estimate and your photos — then a plain answer on whether appraisal fits."),
        ("Re-scope the loss", "Our own inspection and measurements, priced line by line for your part of New Hampshire."),
        ("Invoke the clause in writing", "Appraisal is invoked under your policy, and your appraiser is named within its time limits."),
        ("Reconcile line by line", "Line-by-line work with the insurer’s appraiser. Most of the gap is usually settled here."),
        ("Two signatures, one award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]
    steps_html = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    tabs = "".join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{n}</b><small>{s}</small></button>' for i, (k, n, s, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="reg-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>{img(ph, sizes="(max-width:900px) 100vw, 760px", alt="")}<div class="reg-copy"><h3>{n}</h3><p>{t}</p><ul class="chips">{"".join(f"<li>{x}</li>" for x in pl)}</ul></div></div>'
        for i, (k, n, s, ph, pl, t) in enumerate(REGIONS))

    tool_cards = "".join(f'<a class="tc rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tc-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<i>{t["icon"]}</i></span><span class="tc-b"><small>{t["kind"]}</small><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    storms = "".join(f'<li class="rec rv"><span class="rec-y">{y}</span><div><h3>{n}</h3><p>{p}</p></div></li>' for y, n, p in STORMS)
    cities = "".join(f'<a class="cc rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="cc-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    guides = "".join(f'<a class="gc rv" href="{POST_BASE}{p["slug"]}/"><span class="gc-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="gc-b"><small>{p["read"]} read</small><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p></span></a>' for p in POSTS[:3])

    home_faqs = [
        ("What does a New Hampshire Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work through the differences with the insurer’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When does it make sense to call?", "When coverage has been accepted, you have the insurer’s itemized estimate, and the gap to your contractor’s number is meaningful — often more than about 10% or several thousand dollars."),
        ("Is the award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That’s why the file should be complete before appraisal is demanded."),
        ("What does it cost?", "Each side usually pays its own appraiser and half of the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my town?", "Yes. We work in all 10 New Hampshire counties, from Seabrook to Pittsburg."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("storm-sky-homes", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-light">Independent appraisal · All 10 counties</p>
<h1><span>New Hampshire Insurance Appraiser</span> for claims the insurer underpaid</h1>
<p class="lede">Your insurer accepted the claim, but the check won’t cover the work. New Hampshire Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal clause in your policy.</p>
<div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="#ledger">See how gaps happen {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")} Your appointed appraiser</li><li>{ic("check")} Homes, condos &amp; commercial</li><li>{ic("check")} Fee in writing up front</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ribbon" aria-label="At a glance"><div class="wrap ribbon-in">
<div><b data-count="10">10</b><span>counties covered</span></div>
<div><b data-count="234">234</b><span>cities &amp; towns</span></div>
<div><b data-count="12">12</b><span>appraisal services</span></div>
<div><b data-count="7">7</b><span>free calculators</span></div>
</div></section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="sec" id="ledger"><div class="wrap split">
<div class="rv">
<p class="kicker">Where the money goes missing</p>
<h2>The gap is usually in the line items, not the headline</h2>
<p>Most short claims aren’t denials. They’re estimates with a slope left off, ice &amp; water shield priced at the eaves only, a ceiling painted but not the room, or overhead and profit left out. A New Hampshire Insurance Appraiser finds those lines, measures them and prices them so they hold up in front of an umpire.</p>
<p>The ledger shows the kind of differences we look for. It’s an illustrative example, not a client file.</p>
<a class="btn btn-navy" href="{SVC_BASE}insurer-estimate-audit/">About estimate audits {ic("arrow")}</a>
</div>
<div class="ledger rv" role="group" aria-label="Illustrative estimate comparison">
<div class="ledger-h"><span>Line item</span><span>Insurer</span><span>Re-scoped</span></div>
<div class="ledger-r"><span>Roof squares (9/12 cape, both slopes)</span><span>14.0</span><span>21.6</span></div>
<div class="ledger-r"><span>Ice &amp; water shield</span><span>Eaves only</span><span>Eaves + valleys</span></div>
<div class="ledger-r"><span>Steep-roof labor charge</span><span>—</span><span>Included</span></div>
<div class="ledger-r"><span>Kitchen ceiling &amp; walls repaint</span><span>Ceiling</span><span>Whole room</span></div>
<div class="ledger-r"><span>Overhead &amp; profit (3+ trades)</span><span>—</span><span>Included</span></div>
<div class="ledger-t"><span>Replacement cost total</span><span>$17,940</span><span>$29,310</span></div>
<p class="ledger-note">Illustrative figures only. Every claim depends on its own policy, damage and pricing.</p>
</div>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">What we appraise</p><h2>A dozen claim types, one independent New Hampshire Insurance Appraiser</h2><p>Bring us in for a single estimate audit, as your appointed appraiser once appraisal is demanded, or as a neutral umpire.</p></div>
<div class="svc-grid" data-stagger>{svc_cards}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">Compare every service {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">A year of claims</p><h2>Twelve months of New Hampshire weather, twelve kinds of file</h2><p>Winter writes the most files, but every month brings something. Darker months are when a New Hampshire Insurance Appraiser hears from the most owners.</p></div>
<ol class="months" data-stagger>{months}</ol>
</div></section>

<section class="sec sec-navy"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-light">How it works</p><h2>The appraisal clause, one step at a time</h2><p>The appraisal clause swaps an open-ended argument for a defined process. Here’s how New Hampshire Insurance Appraiser moves a file through it.</p></div>
<div class="steps"><div class="steps-line" aria-hidden="true"><i></i></div><ol class="steps-list">{steps_html}</ol></div>
<p class="center mt"><a class="link-light" href="{P_PROCESS}">Read the full step-by-step guide {ic("arrow", "ico-sm")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Regional knowledge</p><h2>From the Seacoast to the North Country</h2><p>Salt wind on the Seacoast, frozen camps on Winnipesaukee, snow-loaded condos below Mount Washington. A New Hampshire Insurance Appraiser has to know how each one shows up in an estimate.</p></div>
<div class="regions rv" data-regions><div class="reg-tabs" role="tablist" aria-label="New Hampshire regions">{tabs}</div><div class="reg-panels">{panels}</div></div>
</div></section>

<section class="sec sec-gold"><div class="wrap split">
<div class="rv"><p class="kicker">Quick check</p><h2>Run your two numbers before you call</h2><p>Type in the two numbers you already have. If the difference is large, talking with a New Hampshire Insurance Appraiser makes sense. If it’s small, a documented supplement request may close it faster.</p><p>The full <a href="{TOOL_BASE}gap-and-fee-estimator/">dispute size &amp; net recovery estimator</a> adds appraiser and umpire fees.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free and private</p><h2>Seven calculators, built from appraisal files</h2><p>Run the numbers before you call anyone. Each tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="tool-grid" data-stagger>{tool_cards}</div>
</div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv sticky-col"><p class="kicker">On the record</p><h2>The storms behind today’s claim arguments</h2><p>Older storms set the patterns adjusters and appraisers still argue about: what counts as wind versus flood, how ice damage is scoped, when a tree-on-roof claim includes the tree. A New Hampshire Insurance Appraiser reads every file with that history in mind.</p>{img("noreaster-satellite", "round", sizes="(max-width:900px) 100vw, 460px")}</div>
<ol class="record">{storms}</ol>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Statewide</p><h2>Local pages for twelve New Hampshire communities</h2><p>We work in every county. These are the communities where owners call us most often.</p></div>
<div class="city-grid" data-stagger>{cities}</div>
<p class="center mt"><a class="btn btn-line" href="{LOC_BASE}">All New Hampshire cities {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Right help, first time</p><h2>Who should you call about a short claim?</h2><p>Each professional solves a different problem. New Hampshire Insurance Appraiser will tell you when appraisal isn’t the right tool.</p></div>
<div class="who" data-stagger>
<div class="who-c who-hl rv"><h3>Hire an appraiser when…</h3><p class="who-when">Coverage accepted, amount disputed.</p><ul><li>Values the amount of loss</li><li>Works inside the appraisal clause</li><li>Result: an award signed by two of three</li></ul></div>
<div class="who-c rv"><h3>Hire a public adjuster when…</h3><p class="who-when">You want the whole claim handled.</p><ul><li>Prepares and negotiates the claim</li><li>Usually best early on</li><li>Result: a negotiated settlement</li></ul></div>
<div class="who-c rv"><h3>Call an attorney when…</h3><p class="who-when">Denials, coverage fights, deadlines.</p><ul><li>Advises on legal rights</li><li>Handles litigation</li><li>Result: settlement or judgment</li></ul></div>
</div>
</div></section>

<section class="sec sec-tint"><div class="wrap split split-top">
<div class="rv"><p class="kicker">FAQ</p><h2>Plain answers from a New Hampshire Insurance Appraiser</h2><p>Short answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btns"><a class="btn btn-navy" href="{P_FAQ}">All questions {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Short reads for owners holding a short check</h2><p>Practical guides from New Hampshire Insurance Appraiser on policy language, documentation and timing.</p></div>
<div class="guide-grid" data-stagger>{guides}</div>
<p class="center mt"><a class="btn btn-line" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-navy" id="contact"><div class="wrap split">
<div class="rv"><p class="kicker kicker-light">Start here</p><h2>Bring your claim file to a New Hampshire Insurance Appraiser</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin")}<span><small>Coverage</small><b>All 10 counties, 234 cities and towns</b></span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Claim Disputes", "New Hampshire Insurance Appraiser: independent appraisal and estimate review for underpaid ice dam, wind, hail, tree, water and fire claims.", body, schema, photo="storm-sky-homes", body_cls="is-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All NH cities", LOC_BASE)]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [("Service", SVC_BY[r]["name"], f'{SVC_BASE}{r}/') for r in s["related"]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>What owners ask about this</h2>{faq_block(s["faqs"])}
<h2>Services that often overlap</h2>{related(rel)}
</article>
<aside class="side">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs)}</aside></div>
{band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": STATE}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="row-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="row-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="row-b"><small>{i + 1:02d} · {ic(s["icon"], "ico-sm")}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span>{ic("arrow", "row-go")}</a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services in New Hampshire",
                     "Twelve services, one goal: an accurate, defensible valuation of your loss. Start with an estimate audit, bring us in as your appointed appraiser, or ask us to serve as umpire.", "roof-crew") + f"""
<section class="sec"><div class="wrap"><div class="row-list" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate audit</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that difference is worth. An audit answers that quickly, and plenty of disputes close at that stage with a documented supplement.</p><a class="btn btn-navy" href="{SVC_BASE}insurer-estimate-audit/">About estimate audits {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many owners start with an estimate audit and decide later whether to demand appraisal."), ("Do you handle commercial and association claims?", "Yes — condominium associations, multifamily buildings, mill conversions, retail, offices and churches, as well as single-family homes."), ("Is it only winter claims?", "No. We also work on wind, hail, tree, water, fire and tropical-storm losses.")])}</div></div></section>
{band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in New Hampshire", "Insurance appraisal services in New Hampshire: appraisal clause help, estimate audits, winter, storm, water and fire claims, and umpire work.", body, schema, photo="roof-crew"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        near = [("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(l["neighborhoods"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', l["h1"], e(l["lede"]), ph, [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local-card"><div><h2 class="local-t">At a glance</h2><p><b>Areas we cover:</b> {e(hoods)}.</p><p><b>Storm history:</b> {e(l["storm_note"])}</p></div><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Appraisal help available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding towns, including:</p>
<ul>{svc_links}</ul>
<h2>Asked by {e(l["city"])} owners</h2>{faq_block(l["faqs"])}
<h2>Neighboring communities</h2>{related(near)}
</article>
<aside class="side">{call_box()}{list_box("New Hampshire cities", items, path)}{list_box("Calculators for your claim", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{band(f"Short-paid claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        names = l["city"].split(" & ")
        area = [{"@type": "City", "name": n, "containedInPlace": {"@type": "State", "name": STATE}} for n in names]
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, NH", "serviceType": l["kw"], "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": area if len(area) > 1 else area[0], "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cities = "".join(f'<a class="cc rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="cc-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="row-card static rv"><span class="row-ph">{img(ph, sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="row-b"><small>{s}</small><h3>{n}</h3><p>{t}</p></span></div>' for k, n, s, ph, pl, t in REGIONS)
    counties = "".join(f"<li>{c}</li>" for c in ["Belknap", "Carroll", "Cheshire", "Coös", "Grafton", "Hillsborough", "Merrimack", "Rockingham", "Strafford", "Sullivan"])
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisers Across New Hampshire",
                     "New Hampshire Insurance Appraiser works in all 10 counties and 234 cities and towns. These pages cover the communities where owners call us most.", "lonesome-lake") + f"""
<section class="sec"><div class="wrap"><div class="city-grid" data-stagger>{cities}</div></div></section>
<section class="sec sec-tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims change from region to region</h2><p>The same policy wording plays out differently in a Portsmouth colonial, a Laconia camp and a North Conway ski condo.</p></div><div class="row-list" data-stagger>{reg}</div>
<div class="county-box rv"><h2>All 10 counties</h2><ul class="chips">{counties}</ul></div></div></section>
{band("Your town isn’t listed?", "We cover the whole state. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "NH Insurance Appraisers by City | All 10 Counties", "Insurance appraisers serving all 10 New Hampshire counties, including Manchester, Nashua, Concord, Portsmouth, Keene, Laconia and North Conway.", body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="lonesome-lake"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in [x for x in TOOLS if x is not t][:3]]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec sec-tool"><div class="wrap"><h2 class="sr-only">{e(t["name"])}</h2><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on what you enter and your policy terms, and aren’t a quote, appraisal or legal advice. Nothing is stored.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>About this tool</h2>{faq_block(t["faqs"])}
<h2>Try another calculator</h2>{related(others)}</article>
<aside class="side">{call_box()}{list_box("Every calculator", items, path)}</aside></div>
{band("Rather have someone check the math?", "Send us your estimate and we’ll go through it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(f'<a class="tc rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tc-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<i>{t["icon"]}</i></span><span class="tc-b"><small>{t["kind"]}</small><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for NH Owners",
                     "Seven calculators and planners built from appraisal work. Check the insurer’s math, size your dispute and plan your deadlines — no sign-up, nothing stored.", "calculator-notes", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Suggested order</p><h2>A sensible order for the calculators</h2><ol class="steps-plain"><li>Start with the <a href="{TOOL_BASE}nh-claim-deadline-calendar/">deadline calendar</a> so nothing lapses.</li><li>Check the roof with the <a href="{TOOL_BASE}roof-squares-pitch-tool/">roof squares &amp; pitch tool</a> — and, after a big winter, the <a href="{TOOL_BASE}snow-weight-roof-calculator/">snow weight calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}percent-deductible-converter/">deductible converter</a> and <a href="{TOOL_BASE}depreciation-holdback-planner/">holdback planner</a>.</li><li>Size the dispute with the <a href="{TOOL_BASE}gap-and-fee-estimator/">gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}nh-appraisal-readiness-score/">readiness score</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | NH Owners", "Free insurance claim calculators for NH owners: appraisal gap and fees, depreciation, roof squares, deductibles, deadlines and roof snow load.", body, schema, photo="calculator-notes"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("How appraisal works", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in New Hampshire",
                     f"{len(PROCESS_STEPS)} steps from the first disagreement to a signed award — what happens, who does what, and where files most often go wrong.", "inspection-visit",
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="side">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in New Hampshire", "description": "The steps of a property insurance appraisal, from a written demand to a signed award.", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, n in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in New Hampshire", "How insurance appraisal works in New Hampshire, step by step: the written demand, appraisers, the umpire, line-by-line review and the award.", body, [crumbs_schema(trail), howto], photo="inspection-visit"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    jump = "".join(f'<a href="#faq-{i + 1}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for New Hampshire",
                     f"{len(allq)} plain answers, grouped by topic — the process, money, timing, working with us and New Hampshire specifics.", "consult-laptop") + f"""
<div class="wrap layout"><article class="prose"><nav class="jump" aria-label="FAQ topics">{jump}</nav>{groups}</article>
<aside class="side">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{band("Still wondering about something?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | New Hampshire Owners", "Insurance appraisal FAQ for New Hampshire owners: how the process works, what it costs, timing, deadlines and when an award is binding.", body, [crumbs_schema(trail), faq_schema(allq)], photo="consult-laptop"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"g-item\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Insurance Claim Glossary for New Hampshire",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards, in plain English. Type to filter.", "calculator-papers", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="glossary">{dl}</dl></article>
<aside class="side">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "New Hampshire property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | NH Appraisal Terms", "Insurance claim glossary for NH owners: plain-English definitions of ACV, RCV, umpire, ice dam, proof of loss, O&P and dozens more terms.", body, [crumbs_schema(trail), dts], photo="calculator-papers"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in [x for x in POSTS if x is not p][:3]]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related(others)}</article>
<aside class="side">{call_box()}{list_box("Learn", LEARN)}{list_box("Calculators for your claim", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(f'<a class="gc rv" href="{POST_BASE}{p["slug"]}/"><span class="gc-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="gc-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2>{e(p["title"])}</h2><p>{e(p["summary"])}</p></span></a>' for p in POSTS)
    body = page_hero(trail, "Guides", "Insurance Appraisal Guides for NH Owners",
                     "Practical reading on winter claims, estimates, depreciation and when appraisal is — and isn’t — the right move.", "snow-day-house", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="guide-grid" data-stagger>{cards}</div></div></section>{band()}"""
    write(path, document(path, "Insurance Appraisal Guides for NH Owners", "Insurance appraisal guides for NH owners on ice dams, storm documentation, estimates, burst pipes, roof depreciation and the appraisal clause.", body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="snow-day-house"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", "About New Hampshire Insurance Appraiser",
                     "We work on one question — what the damage actually costs — and document the answer clearly enough that everyone at the table can follow it.", "roof-crew") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("inspection-visit", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we only do appraisal work</h2>
<p>Plenty of claim professionals do a little of everything. We chose a narrower job. New Hampshire Insurance Appraiser focuses on the amount of loss, and our process, calculators and documentation standards are built around answering that one question well. That focus lets us serve as your appointed appraiser, audit an estimate before a dispute hardens, or sit as a neutral umpire for neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate looks good for a day and then loses the umpire’s trust. We price what we can back up.</li>
<li><strong>Plain reporting.</strong> You’ll understand each difference between our valuation and the insurer’s.</li>
<li><strong>Straight triage.</strong> If an attorney or a public adjuster fits your situation better, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You’ll know the cost before any work starts.</li>
</ul>
<h2>Who calls us</h2>
<p>Homeowners, condo owners, landlords, associations, property managers, churches, business owners, contractors, public adjusters and attorneys across New Hampshire. On any one claim we serve in a single role, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>Lines we don’t cross</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t promise outcomes — no honest appraiser can.</p>
<h2>Why statewide matters</h2>
<p>A roof in Coös County and a roof in Rockingham County live different lives. Working across all 10 counties means we see what each region produces — snow-loaded framing in the White Mountains, frozen camps on the lakes, wind on the Seacoast, hail in the Merrimack Valley — and price each loss with that context.</p>
</article><aside class="side">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free calculators", TOOL_BASE), ("How appraisal works", P_PROCESS)])}</aside></div>{band()}"""
    write(path, document(path, "About New Hampshire Insurance Appraiser", "About New Hampshire Insurance Appraiser: an independent practice focused on the amount of loss in disputed property insurance claims.", body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="roof-crew"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact New Hampshire Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult-table", cta=False) + f"""
<section class="sec"><div class="wrap split split-top">
<div class="rv"><h2>Direct lines</h2>
<ul class="lines lines-dark"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin")}<span><small>Service area</small><b>All 10 New Hampshire counties</b></span></li></ul>
<h3>Gather these before you call</h3><ul class="ticks"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Walk us through the claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact NH Insurance Appraiser | (844) 537-1427", "Contact our NH insurance appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, or send your details online.", body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consult-table"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Policy", "Website privacy policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Information you give us</h2><p>When you send a form, call or email, we collect what you choose to give us — such as your name, phone, email, property location and claim details. Our server also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and review your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. What you type into them isn’t sent to us or stored.</p>
<h2>Cookies, fonts and analytics</h2><p>The site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics later, this policy will say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                 "How we collect, use and protect what you share with us.",
                 "Website privacy policy for New Hampshire Insurance Appraiser: what we collect through forms and calls, how we use it, and your choices."),
        P_TERMS: ("Terms of Use", "Website terms of use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Agreeing to these terms</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in New Hampshire.</p>
<h2>When an engagement begins</h2><p>Reading the site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>Legal questions</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Ask a New Hampshire attorney about legal questions.</p>
<h2>Calculators</h2><p>Calculators give planning estimates from what you enter. They aren’t appraisals, quotes or predictions of any outcome.</p>
<h2>Ownership and images</h2><p>Site text, design and tools belong to {BRAND}. Photos are royalty-free public-domain or CC0 images used for illustration; they don’t show clients’ properties. You may link to pages and print them for personal use.</p>
<h2>Liability limits</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of New Hampshire.</p>""",
                 "The terms that apply when you use this website and its calculators.",
                 "Terms of use for the New Hampshire Insurance Appraiser website: no client relationship, no legal advice, calculator limits and governing law."),
        P_DISC: ("Disclaimer", "Important limits", f"""
<h2>Education, not advice</h2><p>This website is educational. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>What our role does not include</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>Outcomes vary</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes them. If a deadline is near, contact a New Hampshire attorney promptly.</p>
<h2>Photos</h2><p>Photos are royalty-free public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>
<h2>Outside references</h2><p>Mentions of statutes, agencies or storms are for context only. Check current law and facts with official sources such as the New Hampshire Insurance Department.</p>""",
                 "What the information on this website can and can’t do for you.",
                 "Disclaimer for New Hampshire Insurance Appraiser: general information only, no legal advice, illustrative figures and no guaranteed results."),
    }
    for path, (title, tag, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, tag, title, lede, "concord-state-house", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="side">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="concord-state-house"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIV), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "lonesome-lake", cta=False) + f'<section class="sec"><div class="wrap map-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}", "Site map for New Hampshire Insurance Appraiser: every service, city page, free calculator, guide and legal page on the website.", body, [crumbs_schema(trail)], photo="lonesome-lake"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-media">{img("snow-roof-chimney", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page is buried under the snow</h1><p class="lede">The page you wanted may have moved or never existed. Try one of these instead.</p><div class="btns"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line-light" href="{SVC_BASE}">Services</a><a class="btn btn-line-light" href="{TOOL_BASE}">Calculators</a><a class="btn btn-line-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "Page not found on New Hampshire Insurance Appraiser. The page may have moved; use the links to find services, calculators or contact.", body, [crumbs_schema([("Home", "/"), ("Page not found", "/404.html")])], robots="noindex,follow", photo="snow-roof-chimney"), sitemap=False)


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
    # Search Console verification: exact single line, no newline, no wrapper. Never rename or remove.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// New Hampshire Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nhia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nhia_real  = 'newhampshireinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nhia_proto = strtolower(trim(explode(',', $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'))[0]));
$nhia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
$nhia_path  = strtok($nhia_uri, '?');
$nhia_q     = strpos($nhia_uri, '?') !== false ? substr($nhia_uri, strpos($nhia_uri, '?')) : '';
// /dir/index.php and /index.php are duplicate URLs of /dir/ and /.
if (preg_match('#^(.*/)index\.php$#', $nhia_path, $nhia_m)) {
    $nhia_path = $nhia_m[1];
    $nhia_idx = true;
}
// 301 www. and plain http to https://newhampshireinsuranceappraiser.com - only on the real domain.
if ($nhia_host === 'www.' . $nhia_real || ($nhia_host === $nhia_real && $nhia_proto === 'http')) {
    header('Location: https://' . $nhia_real . $nhia_path . $nhia_q, true, 301);
    exit;
}
if (!empty($nhia_idx)) {
    header('Location: ' . $nhia_path . $nhia_q, true, 301);
    exit;
}
// Keep preview / temporary domains out of search results.
if ($nhia_host !== $nhia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// New Hampshire Insurance Appraiser - front controller for the static build.
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
    learn_pages()
    company_pages()
    sitemap_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
