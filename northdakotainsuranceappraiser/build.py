#!/usr/bin/env python3
"""Static site generator for northdakotainsuranceappraiser.com.

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
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI, TOOL_BASE  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "North Dakota Insurance Appraiser"
HOST = "northdakotainsuranceappraiser.com"
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

SVC_BASE = "/appraisal-representation/"
LOC_BASE = "/across-north-dakota/"
POST_BASE = "/claim-handbook/"
PROCESS = "/how-an-appraisal-unfolds/"
FAQ_PATH = "/policyholder-faq/"
GLOSS = "/appraisal-terms-a-z/"
ABOUT = "/firm-overview/"
CONTACT = "/request-an-appraisal/"
PRIVACY = "/your-privacy/"
TERMS = "/conditions-of-use/"
DISCLAIM = "/not-legal-advice/"
CREDITS = "/image-credits/"
HTMLMAP = "/every-page/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "barn-rural": "Red barn and silo under heavy storm clouds on the North Dakota prairie",
    "arvilla-winter": "Snow-dusted farm field and bare trees in early winter in Grand Forks County",
    "devils-lake-winter": "Flooded trees standing in the frozen shallows of Devils Lake at sunset",
    "fargo-depot": "Historic Northern Pacific railroad depot in Fargo with summer flower planters",
    "bismarck-depot": "Historic 1901 railroad depot building in downtown Bismarck",
    "minot-old-main": "Old Main administration building at Minot State University",
    "grand-forks-flood": "Aerial view of Grand Forks under floodwater during the 1997 Red River flood",
    "grand-forks-city-hall": "Historic Grand Forks city administration building",
    "valley-city-bridge": "Pedestrian suspension bridge over the Sheyenne River in Valley City",
    "valley-city-downtown": "Historic brick storefronts in downtown Valley City",
    "williston-store": "Brick department store building on Main Street in Williston",
    "badlands": "Grass-covered badlands buttes in Theodore Roosevelt National Park",
    "badlands2": "Layered badlands formations under a cloudy sky in western North Dakota",
    "farmhouse-mapleton": "Red wood-sided 1870s farmhouse in Mapleton Township near Fargo",
    "barley-silos": "Row of steel grain bins and silos at a North Dakota grain facility",
    "house-winter": "Snow-loaded cabin roof with icicles hanging from the eaves",
    "snow-house": "Small house nearly hidden by blowing snow in a whiteout",
    "frozen-pipe": "Frozen drain pipe outlet with ice beside a building foundation",
    "flooded-basement": "Open cellar doorway with mud and standing water after a flash flood",
    "water-ceiling": "Missing and water-damaged ceiling tiles with buckets catching leaks",
    "tornado-damage": "Commercial building with its roof and walls torn apart by a tornado",
    "tornado-damage2": "Debris field and stripped trees after a violent tornado",
    "supercell": "Towering supercell thunderstorm glowing at sunset over open grassland",
    "lightning": "Lightning flashing inside storm clouds over a city at night",
    "roofers": "Two roofers working on the gable of a house roof",
    "house-roof": "Steep dark-roofed modern house against a blue sky",
    "home-a": "Two-story brick home with a landscaped front yard",
    "home-c": "Shingled roof planes with skylights on a two-story house",
    "fire-a": "House fully engulfed in flames at night",
    "hail-ground": "Hailstone resting in an open palm after a hailstorm",
    "meeting": "Two people meeting at a small round table by a window",
    "handshake": "Two people shaking hands across a white table",
    "calculator": "Calculator and printed charts beside a laptop keyboard",
    "laptop-work": "Person reviewing paperwork beside a laptop",
    "kitchen": "Modern kitchen with island counter and pendant lights",
    "roof-closeup2": "Gable end of a house with lap siding, vent and trim",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appointment": "meeting", "home-condo-claim-appraisal": "home-a",
    "commercial-multifamily-hoa-appraisal": "williston-store", "hail-roof-siding-appraisal": "home-c",
    "wind-derecho-tornado-appraisal": "tornado-damage2", "water-burst-pipe-appraisal": "water-ceiling",
    "fire-smoke-grass-fire-appraisal": "fire-a", "freeze-ice-dam-snow-load-appraisal": "house-winter",
    "farm-ranch-building-appraisal": "barley-silos", "carrier-estimate-review": "laptop-work",
    "umpire-neutral-services": "handshake",
}
LOC_PHOTO = {
    "fargo": "fargo-depot", "west-fargo": "house-roof", "bismarck": "bismarck-depot", "mandan": "supercell",
    "grand-forks": "grand-forks-flood", "minot": "minot-old-main", "williston": "williston-store", "dickinson": "badlands2",
    "jamestown": "arvilla-winter", "wahpeton": "barn-rural", "devils-lake": "devils-lake-winter", "valley-city": "valley-city-bridge",
}
TOOL_PHOTO = {
    "award-break-even-calculator": "calculator", "two-check-payout-calculator": "kitchen",
    "roof-area-ice-barrier-calculator": "roof-closeup2", "hail-deductible-dollar-converter": "hail-ground",
    "policy-clock-freeze-up-planner": "meeting", "claim-file-strength-test": "handshake",
    "snow-ice-roof-weight-estimator": "snow-house",
}
POST_PHOTO = {
    "north-dakota-appraisal-clause-guide": "meeting", "hail-claim-documentation-checklist": "hail-ground",
    "winter-claims-ice-dams-frozen-pipes": "frozen-pipe", "choosing-appraiser-adjuster-or-lawyer": "handshake",
    "line-by-line-estimate-reading": "laptop-work", "matching-and-discontinued-materials": "roof-closeup2",
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
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
    "barn": '<path d="M3 21V10l9-6 9 6v11z"/><path d="M9 21v-6h6v6M9 15l6 6M15 15l-6 6M12 4v3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 4 13c0-6 7-10 16-10 0 9-4 16-10 16z"/><path d="M4 21c4-5 7-8 11-11"/>',
    "flower": '<path d="M12 22V12M12 12c-3 0-5-2-5-5 3 0 5 2 5 5zM12 12c3 0 5-2 5-5-3 0-5 2-5 5zM12 12c0-3 0-6 0-9"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-clause-appointment": "doc", "home-condo-claim-appraisal": "home", "commercial-multifamily-hoa-appraisal": "building",
    "hail-roof-siding-appraisal": "hail", "wind-derecho-tornado-appraisal": "wind", "water-burst-pipe-appraisal": "drop",
    "fire-smoke-grass-fire-appraisal": "flame", "freeze-ice-dam-snow-load-appraisal": "snow", "farm-ranch-building-appraisal": "barn",
    "carrier-estimate-review": "file", "umpire-neutral-services": "scale",
}


def mark(size=44):
    # Brand mark: navy tile, gold roof chevron over a white horizon line, gold sun dot.
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="10" fill="#002A86"/>'
            '<path d="M10 27.5L24 15l14 12.5" fill="none" stroke="#FFD12B" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M9 35h30" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
            '<circle cx="35.5" cy="12.5" r="3.2" fill="#FFD12B"/></svg>')


def brand(cls=""):
    return (f'<a class="brand{(" " + cls) if cls else ""}" href="/" aria-label="{BRAND} home">{mark()}'
            f'<span class="brand-t"><b>North Dakota</b><span>Insurance Appraiser</span></span></a>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "ND", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-ND", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across North Dakota.",
        "areaServed": [{"@type": "State", "name": "North Dakota"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Ice dams", "Snow load", "Xactimate estimating"],
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
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("Across North Dakota", LOC_BASE), True),
        ("Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Resources", [("How an appraisal unfolds", PROCESS), ("Policyholder FAQ", FAQ_PATH), ("Appraisal terms A–Z", GLOSS), ("Claim handbook", POST_BASE)], None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="solo" href="{ABOUT}">About</a></li><li><a class="solo" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="head"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-gold head-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("on-dark")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a class="solo" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · All 53 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Carrier’s number doesn’t cover the repair? Let’s compare estimates.</p><div class="btn-row"><a class="btn btn-navy" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ink-line" href="{CONTACT}">Send claim details</a></div></div></div>
<div class="wrap">
<div class="foot-grid">
<div class="foot-about">{brand("on-dark")}
<p>Independent appraisal and estimating support for property owners with disputed insurance claims — Red River Valley to the badlands.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri 8am–6pm CT</span></li></ul></div>
<div><h2 class="fh">What we appraise</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="fh">Where we work</h2><ul>{loc}<li><a href="{LOC_BASE}">All of North Dakota</a></li></ul></div>
<div><h2 class="fh">Claim calculators</h2><ul>{tl}</ul></div>
<div><h2 class="fh">The practice</h2><ul><li><a href="{ABOUT}">Firm overview</a></li><li><a href="{PROCESS}">How an appraisal unfolds</a></li><li><a href="{FAQ_PATH}">Policyholder FAQ</a></li><li><a href="{GLOSS}">Terms A–Z</a></li><li><a href="{POST_BASE}">Claim handbook</a></li><li><a href="{CONTACT}">Request an appraisal</a></li></ul></div>
</div>
<div class="foot-legal"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{CREDITS}">Image credits</a></li><li><a href="{HTMLMAP}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and are not a public adjuster. Content on this site is general and educational; policy terms vary, and results depend on the facts of each claim.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("file")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" '
            'height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="barn-rural", body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": canonical + "#webpage"}
        if t in MAIN_TYPES:
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
    main = [n["@id"] for n in extra if n.get("@type") in MAIN_TYPES]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across North Dakota">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across North Dakota">
<meta name="geo.region" content="US-ND">
<meta name="geo.placename" content="North Dakota">
<meta name="theme-color" content="#002A86">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700;800&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
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
    # Pages are served as dir/index.php: the host serves real files without running the root
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through first</h2><p>A free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="box-tel" href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a><a class="btn btn-gold" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def aside(*boxes):
    return '<aside class="side"><div class="side-in">' + "".join(boxes) + "</div></aside>"


def cta_strip(h="Have a claim that doesn’t add up?", p="Send us the carrier’s estimate. We’ll review it and tell you plainly what we see."):
    return f"""<section class="strip"><div class="wrap strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-navy" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ink-line" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Wind / tornado", "Water / frozen pipe", "Ice dam / snow load", "Fire / smoke", "Farm or ranch building", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Describe your claim", sub="Free review. No obligation. Usually a reply within one business day.", page="/"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Farm or ranch owner", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in North Dakota"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3 class="form-t">{e(heading)}</h3><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy statement</a>.</span></label></div>
<div class="full"><button class="btn btn-navy wide" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hero-form-t">Start a no-cost claim review</h2><p class="form-sub">Tell us a little. We’ll call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy statement</a>.</span></label>
<button class="btn btn-navy wide" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hero-form-note">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("redriver", "Red River Valley", "Fargo · West Fargo · Grand Forks · Wahpeton",
     ["Large hail", "Spring flooding", "Straight-line wind", "Basement water"],
     "The flattest, most populated corner of the state. Severe summer storms track straight across the valley, and snowmelt years bring sump, foundation and sewer-backup questions — many of them coverage issues, not appraisal issues.",
     "fargo-depot", ["fargo", "west-fargo", "grand-forks", "wahpeton"]),
    ("lakes", "Lakes & Drift Prairie", "Devils Lake · Jamestown · Valley City",
     ["Hail on siding", "Ice dams", "Blizzards", "Wind"],
     "Small cities, farmsteads and lake homes spread across the prairie. Claims here often mix a house, a detached garage and an outbuilding or two — and adjusters can be days away after a big storm.",
     "valley-city-bridge", ["devils-lake", "jamestown", "valley-city"]),
    ("capital", "Capital Corridor", "Bismarck · Mandan",
     ["Hail", "River ice & high water", "Snow load", "Fire"],
     "The capital region sits where the Heart River meets the Missouri River. Older homes near downtown, fast-growing subdivisions on the edges and a commercial core produce a wide mix of roof, siding and interior claims.",
     "bismarck-depot", ["bismarck", "mandan"]),
    ("northwest", "Northwest & Bakken", "Minot · Williston",
     ["Wind", "Frozen pipes", "Hail", "Flood aftermath"],
     "From the Souris River valley to the oil patch. Rapid growth added apartments, workforce housing and steel commercial buildings — construction types that each price differently in an estimate.",
     "minot-old-main", ["minot", "williston"]),
    ("badlands", "Southwest & Badlands", "Dickinson · Medora",
     ["Grass fire", "Wind", "Hail", "Extreme cold"],
     "Open rangeland, ranch buildings and oil-country towns. Dry, windy autumns raise grass-fire exposure, and long distances make careful documentation more important than ever.",
     "badlands", ["dickinson"]),
]

SEASONS = [
    ("flower", "Spring", "Mar–May", "Snowmelt, ice jams and saturated ground. Sump failures, seepage and roof leaks from late-season ice dams."),
    ("sun", "Summer", "Jun–Aug", "Peak hail and severe-storm season: shingles, siding, windows, metal buildings — plus straight-line winds and tornadoes."),
    ("leaf", "Fall", "Sep–Nov", "Dry, windy days raise grass-fire risk out west, and a race to finish repairs before freeze-up."),
    ("snow", "Winter", "Dec–Feb", "Blizzards, frozen pipes, ice dams and heavy snow load on roofs and outbuildings."),
]


def home():
    svc_cards = "".join(
        f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="card-b"><span class="card-k">{ic(SVC_ICON[s["slug"]])}{i + 1:02d}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
        for i, s in enumerate(SERVICES[:9]))

    stops = "".join(f'<li class="stop"><span class="dot">{i + 1}</span><h3>{e(n)}</h3><p>{e(d)}</p></li>' for i, (n, d) in enumerate(PROCESS_STEPS))

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}</button>'
        for i, (k, n, *_r) in enumerate(REGIONS))
    panels = ""
    for i, (k, n, cities, perils, txt, ph, slugs) in enumerate(REGIONS):
        links = " · ".join(f'<a href="{loc_path(LOC_BY[s])}">{e(LOC_BY[s]["city"])}</a>' for s in slugs)
        panels += (f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>'
                   f'<div class="region-ph">{img(ph, sizes="(max-width:900px) 100vw, 560px", alt="")}</div><div class="region-tx"><h3>{e(n)}</h3><p class="region-c">{e(cities)}</p>'
                   f'<ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(txt)}</p><p class="region-links">Local pages: {links}</p></div></div>')

    locs = "".join(
        f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 280px", alt="")}<span class="lcard-t"><h3>{e(l["city"])}</h3><small>{e(l["county"])}</small></span></a>'
        for l in LOCATIONS[:8])

    tools = "".join(
        f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="trow-ic">{e(t["icon"])}</span><span class="trow-b"><small>{e(t["kind"])}</small><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span>{ic("arrow", "ico trow-go")}</a>'
        for t in TOOLS)

    guides = "".join(
        f'<a class="card rv" href="{POST_BASE}{p["slug"]}/"><span class="card-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</span><span class="card-b"><span class="card-k">{e(p["read"])} read</span><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p></span></a>'
        for p in POSTS[:3])

    seasons = "".join(f'<div class="season rv"><span class="season-ic">{ic(icn)}</span><h3>{e(n)} <small>{e(m)}</small></h3><p>{e(t)}</p></div>' for icn, n, m, t in SEASONS)

    home_faqs = [
        ("What does a North Dakota Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is that different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When should I call a North Dakota Insurance Appraiser?", "When coverage is accepted, you have the carrier’s itemized estimate, and the gap between it and a contractor’s estimate is meaningful — generally more than about 10% or several thousand dollars."),
        ("Is the award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That’s why the file should be complete before anyone demands appraisal."),
        ("What does it cost?", "Each side usually pays its own appraiser and half of the umpire. Our fee is put in writing before work begins, and the first conversation is free."),
        ("Can winter damage wait until spring?", "Report it now and protect the property; policy clocks keep running. Snow-covered roofs can be re-inspected after thaw, and that follow-up often matters for the scope."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("barn-rural", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker"><span class="pip"></span>Independent claim appraisal · All 53 counties</p>
<h1>North Dakota Insurance Appraiser for hail, wind &amp; winter claims that came up short</h1>
<p class="lede">When the insurer accepts the claim but the check won’t cover the repair, North Dakota Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="#services">See services {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Cold-climate scope &amp; code items</li><li>{ic("check")}Homes, HOAs, farms &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="seasons-sec" aria-labelledby="seasons-h"><div class="wrap">
<div class="sec-head rv"><p class="label"><span>01</span>Claim calendar</p><h2 id="seasons-h">Four seasons, four kinds of claims</h2><p>A North Dakota Insurance Appraiser sees the year in claim types. Knowing which season produced the damage shapes what to look for — and what the carrier may have missed.</p></div>
<div class="seasons" data-stagger>{seasons}</div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-ph rv">{img("roofers", sizes="(max-width:900px) 100vw, 560px")}<div class="intro-badge">{ic("shield")}<span><b>Retained by you</b>never by the carrier</span></div></div>
<div class="intro-tx rv">
<p class="label"><span>02</span>Why owners call</p>
<h2>Why property owners bring in a North Dakota Insurance Appraiser</h2>
<p>Most underpaid claims aren’t denied. They’re short: a missed roof slope, siding that can’t be matched, an ice barrier nobody priced, a basement scoped as “clean and dry.” A North Dakota Insurance Appraiser exists for that gap between “covered” and “paid in full.”</p>
<ul class="ticks">
<li>{ic("check")}<span><b>We scope it from scratch.</b> Our own inspection and measurements — never an edited copy of the carrier’s estimate.</span></li>
<li>{ic("check")}<span><b>Defensible, not inflated.</b> Numbers built to hold up in front of an umpire, which is what moves awards.</span></li>
<li>{ic("check")}<span><b>Honest triage.</b> If your claim needs an attorney or a supplement instead, you’ll hear that on the first call.</span></li>
</ul>
<div class="counters stats">
<div><b data-count="53">53</b><span>counties served</span></div>
<div><b data-count="11">11</b><span>appraisal services</span></div>
<div><b data-count="7">7</b><span>free claim tools</span></div>
<div><b>2 of 3</b><span>signatures bind an award</span></div>
</div>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="label"><span>03</span>Services</p><h2>Claims a North Dakota Insurance Appraiser takes on</h2></div><p>Eleven services built around one job: a valuation of your loss that holds up. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="cards" data-stagger>{svc_cards}</div>
<p class="center mt"><a class="btn btn-navy" href="{SVC_BASE}">All eleven appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="label"><span>04</span>The route</p><h2>From disagreement to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here’s the route North Dakota Insurance Appraiser follows on a typical file.</p></div>
<ol class="route">{stops}<li class="route-track" aria-hidden="true"><span></span></li></ol>
<p class="center mt"><a class="tlink" href="{PROCESS}">Read the full appraisal walkthrough {ic("arrow")}</a></p>
</div></section>

<section class="sec navy" id="gap-check"><div class="wrap two">
<div class="rv"><p class="label light"><span>05</span>Quick math</p><h2>Is your gap big enough to appraise?</h2><p>Type in the two numbers you already have. A large difference is worth a conversation with a North Dakota Insurance Appraiser; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}award-break-even-calculator/">award break-even calculator</a> adds appraiser and umpire fees and shows your break-even point.</p><a class="btn btn-gold" href="{TOOL_BASE}">All seven free tools {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="label"><span>06</span>Regions</p><h2>Five claim climates in one state</h2><p>Hail in the valley, river ice in the capital, wind in the oil patch, grass fire in the badlands. A North Dakota Insurance Appraiser has to know how each region’s weather shows up on a building — and in an estimate.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="North Dakota regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="label"><span>07</span>Locations</p><h2>North Dakota Insurance Appraiser near you</h2></div><p>We work in every county. These are the communities where claims come from most often — each page covers local storms, housing and what tends to go wrong.</p></div>
<div class="lcards" data-stagger>{locs}</div>
<p class="center mt"><a class="tlink" href="{LOC_BASE}">See all twelve local pages {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap two top">
<div class="rv sticky-col"><p class="label"><span>08</span>Free tools</p><h2>Seven free calculators from a North Dakota Insurance Appraiser</h2><p>Run the numbers before you pick up the phone. Every tool works in your browser — nothing is stored or sent.</p><a class="btn btn-navy" href="{TOOL_BASE}">Open the tool library {ic("arrow")}</a></div>
<div class="trows" data-stagger>{tools}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="label"><span>09</span>Right help</p><h2>Which kind of help fits your claim?</h2><p>Each solves a different problem, and picking the right one first saves time and fees. North Dakota Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="compare" data-stagger>
<div class="cmp hl rv"><h3>Party-appointed appraiser</h3><p class="cmp-k">Values the amount of loss</p><ul><li>{ic("check")}Coverage accepted, number disputed</li><li>{ic("check")}Works inside the appraisal clause</li><li>{ic("check")}Binding award with two of three signatures</li><li>{ic("x")}Doesn’t decide coverage or bad faith</li></ul></div>
<div class="cmp rv"><h3>Licensed public adjuster</h3><p class="cmp-k">Manages and negotiates the claim</p><ul><li>{ic("check")}Most useful early, from first notice</li><li>{ic("check")}Prepares and presents the claim</li><li>{ic("check")}Negotiated settlement</li><li>{ic("x")}Isn’t a lawyer</li></ul></div>
<div class="cmp rv"><h3>Insurance coverage lawyer</h3><p class="cmp-k">Handles legal disputes</p><ul><li>{ic("check")}Denials and coverage fights</li><li>{ic("check")}Bad-faith and deadline questions</li><li>{ic("check")}Settlement or judgment</li><li>{ic("x")}Usually the costliest route</li></ul></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="label"><span>10</span>Handbook</p><h2>From the North Dakota claim handbook</h2></div><p>Practical guides on policy language, documentation and winter losses, written by North Dakota Insurance Appraiser.</p></div>
<div class="cards" data-stagger>{guides}</div>
</div></section>

<section class="sec stone"><div class="wrap two top">
<div class="rv"><p class="label"><span>11</span>Questions</p><h2>Straight answers from a North Dakota Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_PATH}">All questions {ic("arrow")}</a><a class="btn btn-ink-line" href="{GLOSS}">Terms A–Z</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec navy" id="contact"><div class="wrap two top">
<div class="rv"><p class="label light"><span>12</span>Start here</p><h2>Put your numbers in front of a North Dakota Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. You’ll get a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></span></li><li>{ic("pin")}<span><small>Coverage</small><b>All 53 North Dakota counties</b></span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    trail = [("Home", "/")]
    schema = [crumbs_schema(trail), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Hail & Winter Claims",
                        "North Dakota Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, water, fire and winter claims.",
                        body, schema, photo="barn-rural", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
{aside(call_box(), list_box("All services", items, path), list_box("Where we work", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All 53 counties", LOC_BASE)]))}</div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "North Dakota"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="card-b"><span class="card-k">{ic(SVC_ICON[s["slug"]])}{i + 1:02d}</span><h2 class="card-h">{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>'
        for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across North Dakota",
                     "From a single estimate review to full panel representation and neutral umpire work, every North Dakota Insurance Appraiser service is built around an accurate, defensible valuation of your loss.", "roofers") + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="label"><span>?</span>Where to start</p><h2>Most claims start with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and some disputes close right there.</p><a class="btn btn-navy" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle commercial and farm claims?", "Yes — houses, condos, apartments, HOAs, retail, offices, churches, shops, pole barns and other farm or ranch buildings."), ("Is it only hail?", "No. Wind, water, fire, freeze, ice-dam and snow-load losses all come through appraisal when the dispute is about cost.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in North Dakota",
                             "Appraisal clause representation, estimate review, hail, wind, water, fire, freeze and farm-building claim appraisal, plus umpire work in North Dakota.",
                             body, schema, photo="roofers"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Across North Dakota", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, North Dakota", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="localbox"><p class="localbox-t">Local claim risks</p><ul class="chips">{chips}</ul><p class="localbox-n"><b>Areas we see:</b> {e(l["neighborhoods"])}</p></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and across {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
{aside(call_box(), list_box("North Dakota locations", items, path), list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, ND", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "North Dakota"}}, "url": DOMAIN + path}]
        title = f"{l['city']}, ND Insurance Appraiser | Claim Disputes"
        if len(title) > 56:
            title = f"{l['city']}, ND Insurance Appraiser"
        desc = f"Independent insurance appraiser for {l['city']} and {l['county']}: appraisal and estimate review for underpaid hail, wind, water and winter claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {l['city']} and {l['county']}: appraisal and estimate review for underpaid hail, wind and winter claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Across North Dakota", LOC_BASE)]
    cards = "".join(
        f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 280px", alt="")}<span class="lcard-t"><h2 class="lcard-h">{e(l["city"])}</h2><small>{e(l["county"])}</small></span></a>'
        for l in LOCATIONS)
    reg = "".join(
        f'<div class="regrow rv"><div class="regrow-ph">{img(ph, sizes="(max-width:700px) 100vw, 320px", alt="")}</div><div><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in pr)}</ul></div></div>'
        for k, n, c, pr, t, ph, _s in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 53 North Dakota Counties",
                     "North Dakota Insurance Appraiser works statewide — from the Red River to the badlands and from the Canadian border to the South Dakota line. These local pages cover the cities where we handle claims most often.", "badlands") + f"""
<section class="sec"><div class="wrap"><div class="lcards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="label"><span>5</span>Regions</p><h2>How claims differ across North Dakota</h2><p>The same policy language plays out very differently on a Fargo two-story, a Minot rebuild and a ranch shop near Dickinson.</p></div><div class="regrows" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "North Dakota Insurance Appraiser Locations",
                             "Insurance appraisal in all 53 North Dakota counties, including Fargo, Bismarck, Grand Forks, Minot, Williston, Dickinson, Jamestown and Devils Lake.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f"{l['city']}, ND", loc_path(l)) for l in LOCATIONS])], photo="badlands"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms; they aren’t a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
{aside(call_box(), list_box("All claim tools", items, path))}</div>
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    tiles = "".join(
        f'<a class="card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="card-badge">{e(t["icon"])}</span></span><span class="card-b"><span class="card-k">{e(t["kind"])}</span><h2 class="card-h">{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Claim Planning Tools for North Dakota Owners",
                     "Seven calculators, planners and checklists built from appraisal work. Check the carrier’s math, plan your deadlines and decide on next steps — no sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="label"><span>→</span>Suggested order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}policy-clock-freeze-up-planner/">policy clock &amp; freeze-up planner</a> so nothing lapses.</li><li>Check roof math with the <a href="{TOOL_BASE}roof-area-ice-barrier-calculator/">roof area &amp; ice-barrier calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}hail-deductible-dollar-converter/">deductible</a> and <a href="{TOOL_BASE}two-check-payout-calculator/">payout</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}award-break-even-calculator/">break-even calculator</a>.</li><li>Finish with the <a href="{TOOL_BASE}claim-file-strength-test/">file strength test</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Tools & Calculators | ND",
                              "Free claim tools: award break-even, two-check payout, roof area and ice barrier, hail deductible, snow weight, policy clock planner and more.",
                              body, schema, photo="calculator"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("How an appraisal unfolds", PROCESS), ("Policyholder FAQ", FAQ_PATH), ("Appraisal terms A–Z", GLOSS), ("Claim handbook", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("How an appraisal unfolds", path)]
    body = page_hero(trail, "Process guide", "How an Insurance Appraisal Unfolds in North Dakota",
                     "Eight stages from the first disagreement to a signed award — what happens, who does what, and where claims most often go wrong.", "lightning",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How an insurance appraisal unfolds in North Dakota", "description": "The stages of a property insurance appraisal from disagreement to signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in ND | 8 Stages",
                         "Step-by-step guide to insurance appraisal in North Dakota: the written demand, appraisers and umpire, inspections, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="lightning"), 0.8)

    path = FAQ_PATH
    trail = [("Home", "/"), ("Policyholder FAQ", path)]
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Policyholder FAQ: Insurance Appraisal in North Dakota",
                     "Plain answers about the appraisal process, costs, timing and North Dakota specifics — grouped by topic.", "farmhouse-mapleton") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="FAQ topics"><p class="toc-t">Jump to a topic</p><ul>{toc}</ul></nav>{groups}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email — we’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Costs, Timing & ND Rules",
                         "Answers to common North Dakota insurance appraisal questions: how the process works, what it costs, how long it takes and when an award binds.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="farmhouse-mapleton"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Appraisal terms A–Z", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Searchable glossary", "Insurance Appraisal Terms A–Z",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "laptop-work", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl><p class="gloss-none" hidden>No terms match that search.</p></article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal terms A–Z", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary | ACV, Umpire & More",
                         "Plain-English definitions of property claim terms: actual cash value, replacement cost, ice dam, snow load, appraisal award, umpire, O&P and more.",
                         body, [crumbs_schema(trail), dts], photo="laptop-work"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim handbook", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Handbook · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<p class="byline">Published {nice} by {BRAND}. General information, not legal advice.</p><h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
{aside(call_box(), list_box("Resources", LEARN), list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim handbook", path)]
    cards = "".join(
        f'<a class="card rv" href="{POST_BASE}{p["slug"]}/"><span class="card-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</span><span class="card-b"><span class="card-k">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</span><h2 class="card-h">{e(p["title"])}</h2><p>{e(p["summary"])}</p></span></a>'
        for p in POSTS)
    body = page_hero(trail, "Claim handbook", "The Claim Handbook for North Dakota Property Owners",
                     "Practical guides on policy language, documentation, winter losses and choosing the right help — written by people who work appraisal panels.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Claim Handbook: Appraisal Guides for ND Owners",
                         "Guides for North Dakota property owners on appraisal clauses, hail documentation, winter claims, reading estimates and matching disputes.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Firm overview", path)]
    body = page_hero(trail, "Firm overview", "About North Dakota Insurance Appraiser",
                     "An independent appraisal and estimating practice built on one idea: a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "valley-city-downtown") + f"""
<div class="wrap layout"><article class="prose">
<figure class="figure">{img("meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. North Dakota Insurance Appraiser works on one question — the amount of loss — and builds its process, tools and documentation standards around answering it well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Cold-climate detail.</strong> Ice barrier, frost-protected foundations, heat during winter work, short building seasons — the items that often go missing from an out-of-state estimate.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, farm and ranch families, contractors, public adjusters and attorneys across North Dakota. On any one claim we serve in a single role, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate outside the appraisal process. We don’t guarantee outcomes — no honest appraiser can.</p>
<h2>Statewide on purpose</h2>
<p>Weather in the Red River Valley, the drift prairie, the capital corridor, the northwest and the badlands produces very different losses. Working in all 53 counties means seeing every kind of claim the state produces and pricing each with local knowledge.</p>
</article>{aside(call_box(), list_box("Explore", [("Appraisal services", SVC_BASE), ("Across North Dakota", LOC_BASE), ("Free tools", TOOL_BASE), ("How an appraisal unfolds", PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, "About Us | North Dakota Insurance Appraiser",
                         "North Dakota Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="valley-city-downtown"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Request an appraisal", path)]
    body = page_hero(trail, "Get in touch", "Request a Claim Review or Appraisal",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "handshake", cta=False) + f"""
<section class="sec navy"><div class="wrap two top">
<div class="rv"><p class="label light"><span>→</span>Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></span></li><li>{ic("pin")}<span><small>Service area</small><b>Statewide — all 53 counties</b></span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks light"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The carrier’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and any contractor estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Us | North Dakota Insurance Appraiser",
                         "Get a free review of your disputed property claim. Call or text (844) 537-1427 or email info@northdakotainsuranceappraiser.com.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="handshake"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td>{e(v.get("via", ""))}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Statement", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share — such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide the services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host the site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s policies. If we add analytics, this statement will be updated to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Conditions of Use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these conditions. The content is general information about insurance appraisal and property claims in North Dakota.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Talk to a licensed North Dakota attorney about legal questions.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates from the information you enter. Example figures are illustrative. Neither is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on the <a href="{CREDITS}">image credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These conditions are governed by the laws of the State of North Dakota.</p>""", "The conditions that apply when you use this website and its tools."),
        DISCLAIM: ("Disclaimer", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits, and state law can affect them. Nothing on this site extends or changes any deadline. If one is approaching, consult a North Dakota attorney promptly.</p>
<h2>Bad faith and legal claims</h2><p>North Dakota law recognizes legal claims against insurers that handle claims in bad faith, and the state’s insurance code lists unfair claim settlement practices. Whether either applies depends on facts and law that only an attorney can evaluate. Appraisal doesn’t decide those questions.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to agencies, laws or weather events are for context. Verify current rules with official sources such as the North Dakota Insurance Department.</p>""", "Important limits on the information published on this website."),
        CREDITS: ("Image Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as Carol M. Highsmith’s photographs in the Library of Congress and images by U.S. government agencies. They were found through the Openverse search engine. Attribution isn’t legally required, but we credit the creators here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Via</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site."),
    }
    for path, (title, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "arvilla-winter", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article>{aside(call_box())}</div>'
        write(path, document(path, f"{title} | {BRAND}", f"{title} for {BRAND}: {lede}", body, [crumbs_schema(trail)], photo="arvilla-winter"), 0.3)


def sitemap_pages():
    path = HTMLMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("Firm overview", ABOUT), ("Request an appraisal", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("Across North Dakota", LOC_BASE)] + [(f"{l['city']}, ND", loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy statement", PRIVACY), ("Conditions of use", TERMS), ("Disclaimer", DISCLAIM), ("Image credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "grand-forks-city-hall", cta=False) + f'<section class="sec"><div class="wrap"><div class="mapcols" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, North Dakota locations, free claim tools and guides.", body, [crumbs_schema(trail)], photo="grand-forks-city-hall"), 0.3)

    body = f"""<section class="phero"><div class="phero-bg">{img("lightning", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page didn’t ride out the storm</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line" href="{SVC_BASE}">Services</a><a class="btn btn-line" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow", photo="lightning"), sitemap=False)


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
// North Dakota Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$ndia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$ndia_real  = 'northdakotainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$ndia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://northdakotainsuranceappraiser.com - only on the real domain.
if ($ndia_host === 'www.' . $ndia_real || ($ndia_host === $ndia_real && $ndia_proto === 'http')) {
    header('Location: https://' . $ndia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $ndia_m)) {
    $ndia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $ndia_m[1] . $ndia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($ndia_host !== $ndia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// North Dakota Insurance Appraiser - front controller for the static build.
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
