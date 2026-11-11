#!/usr/bin/env python3
"""Static site generator for massachusettsinsuranceappraiser.com.

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
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Massachusetts Insurance Appraiser"
HOST = "massachusettsinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261111a"
FAV = "1"

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = "GTM-N3W5C9HQ"
# Head snippet exactly as supplied by the owner (optional). If empty, the standard GTM loader for GTM_ID is used.
GTM_HEAD_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-N3W5C9HQ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

SVC_BASE = "/what-we-appraise/"
LOC_BASE = "/cities-and-towns/"
TOOL_BASE = "/estimators/"
POST_BASE = "/claim-library/"
ROADMAP = "/appraisal-roadmap/"
FAQ_URL = "/questions/"
GLOSS = "/insurance-terms/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"
SITEMAP_HTML = "/site-index/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, MA"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "boston-charles": "Boston skyline seen across the Charles River on a sunny day",
    "boston-rooftops": "Brick rowhouse rooftops and church spires under a dramatic sunset sky in Boston",
    "boston-harbor": "Boston waterfront towers and moored boats on the harbor under big clouds",
    "snowy-rowhouses": "Snow-covered street lined with brick rowhouses and bare trees during a snowstorm",
    "snowy-street": "Quiet residential street and parked cars buried in fresh snow",
    "snow-red-house": "Red wooden house with a steep snow-covered roof after a heavy snowfall",
    "cape-cottages": "Row of white beach cottages along the shore in Truro on Cape Cod",
    "icicles-eave": "Long icicles hanging from a roof eave in winter",
    "icicles-siding": "Sunlit icicles hanging from a snowy gutter above gray siding",
    "consultation": "Two women talking across a table during a consultation by a window",
    "advisors-laptop": "Two men reviewing figures on a laptop at a meeting table",
    "laptop-calculator": "Hands using a calculator beside a laptop showing a spreadsheet",
    "calculator-notes": "Calculator, pencil and sticky notes on a desk",
    "clapboard-porch": "Historic clapboard house with a front porch, shutters and a picket fence",
    "brick-commercial": "Ornate brick and cast-iron commercial building facade",
    "brick-mainstreet": "Brick commercial buildings along a city street corner",
    "brick-rowhouse": "Three-story brick row building with arched doorways on a city street",
    "condo-complex": "Brick condominium building with balconies beside a pond",
    "trees-down-lawn": "Large trees blown down across a lawn after a storm",
    "storm-surge-house": "Blue-green house knocked off its foundation by storm flooding",
    "wind-damaged-house": "House with a collapsed wall and roof after a windstorm",
    "tornado-street": "Street in Monson, Massachusetts, with snapped trees and leaning utility poles after the June 2011 tornado",
    "tornado-debris": "Debris and splintered trees in a Monson, Massachusetts neighborhood after the June 2011 tornado",
    "cedar-shingles": "Weathered shingle siding around a small gabled window",
    "nantucket-light": "Lighthouse beyond the dunes on Nantucket under a streaked sunset sky",
    "roof-repair-lift": "Roofer on a lift working on a damaged church roof covered with a blue tarp",
    "roofers-barn": "Crew working on the metal roof of an old red barn in winter",
    "slate-tiles": "Close-up of overlapping slate roof shingles in muted colors",
    "ceiling-collapse": "Bedroom with a collapsed ceiling exposing wood framing",
    "berkshire-hills": "Route 7 in Lanesborough winding past fall foliage in the Berkshires",
    "flooded-home": "Stop sign and brick house standing in floodwater on a residential street",
    "harbor-boats": "Boats moored in Plymouth Harbor on a calm gray day",
    "blue-hills-skyline": "Boston skyline in the distance seen over pine trees from the Blue Hills",
    "house-fire-night": "Wooden house fully engulfed in flames at night",
    "firefighter": "Firefighter in protective gear carrying a rolled fire hose",
    "hail-deck": "Wooden deck and patio furniture covered in hailstones",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    src = f"/assets/img/photos/{key}.webp"
    srcset = ""
    if p["fw"] > 640:
        srcset = f' srcset="/assets/img/photos/{key}-640.webp 640w, {src} {p["fw"]}w" sizes="{sizes}"'
    return f'<img{c} src="{src}"{srcset} width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>'


SVC_PHOTO = {
    "insurance-appraisal-representation": "consultation", "home-insurance-claim-appraisal": "clapboard-porch",
    "condo-hoa-commercial-appraisal": "condo-complex", "roof-hail-damage-appraisal": "hail-deck",
    "wind-tornado-claim-appraisal": "tornado-debris", "hurricane-noreaster-appraisal": "wind-damaged-house",
    "water-damage-claim-appraisal": "ceiling-collapse", "fire-smoke-damage-appraisal": "house-fire-night",
    "ice-dam-snow-load-appraisal": "icicles-eave", "claim-estimate-review": "laptop-calculator",
    "umpire-selection-services": "advisors-laptop",
}
# Card photos on the homepage / index can differ from the hero photo.
SVC_CARD = dict(SVC_PHOTO, **{"hurricane-noreaster-appraisal": "storm-surge-house", "fire-smoke-damage-appraisal": "firefighter",
                              "roof-hail-damage-appraisal": "roof-repair-lift"})
LOC_PHOTO = {
    "boston": "boston-harbor", "worcester": "snowy-street", "springfield": "tornado-street", "cambridge": "boston-charles",
    "lowell": "brick-mainstreet", "quincy": "blue-hills-skyline", "new-bedford": "wind-damaged-house", "brockton": "clapboard-porch",
    "plymouth": "harbor-boats", "barnstable": "cape-cottages", "pittsfield": "berkshire-hills", "salem": "snowy-rowhouses",
}
TOOL_PHOTO = {
    "appraisal-award-gap-estimator": "calculator-notes", "rcv-acv-holdback-calculator": "laptop-calculator",
    "roof-area-pitch-converter": "slate-tiles", "hurricane-deductible-calculator": "nantucket-light",
    "claim-calendar-builder": "snow-red-house", "appraisal-file-checkup": "roof-repair-lift",
    "roof-snow-load-estimator": "icicles-siding",
}
POST_PHOTO = {
    "massachusetts-reference-and-appraisal-clause": "consultation", "ice-dam-claims-what-gets-missed": "icicles-siding",
    "noreaster-wind-vs-flood-claims": "flooded-home", "condo-master-policy-vs-ho6-claims": "condo-complex",
    "triple-decker-insurance-claims": "brick-rowhouse", "choosing-an-umpire-in-massachusetts": "advisors-laptop",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
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
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3.5l3 2 3-2M9 20.5l3-2 3 2"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "wave": '<path d="M2 12c2-2 4-2 6 0s4 2 6 0 4-2 6 0M2 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0M2 6c2-2 4-2 6 0s4 2 6 0 4-2 6 0"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "insurance-appraisal-representation": "doc", "home-insurance-claim-appraisal": "home", "condo-hoa-commercial-appraisal": "building",
    "roof-hail-damage-appraisal": "hail", "wind-tornado-claim-appraisal": "wind", "hurricane-noreaster-appraisal": "storm",
    "water-damage-claim-appraisal": "drop", "fire-smoke-damage-appraisal": "flame", "ice-dam-snow-load-appraisal": "snow",
    "claim-estimate-review": "file", "umpire-selection-services": "scale",
}


def mark(uid="m"):
    return (f'<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#2e384a"/><stop offset="1" stop-color="#12161f"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="11" fill="url(#{uid})"/>'
            '<path d="M9.5 25.5L24 12l14.5 13.5" fill="none" stroke="#e07a4f" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="20.5" y="21" width="7" height="7" rx="1.2" fill="#fff"/>'
            '<path d="M8.5 35.5c3.1-2.6 6.2-2.6 9.3 0s6.2 2.6 9.3 0 6.2-2.6 9.3 0 2.6 1.1 3.1 1.1" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')


def brand_block(uid):
    return f'<a class="brand" href="/">{mark(uid)}<span class="brand-t"><b>Massachusetts</b><span>Insurance Appraiser</span></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "MA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MA", "availableLanguage": "en"}],
        "slogan": "Independent valuation for disputed property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Massachusetts.",
        "areaServed": [{"@type": "State", "name": "Massachusetts"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Massachusetts standard fire policy reference", "Ice dam claims", "Nor'easter damage", "Property claim valuation"],
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
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal roadmap", ROADMAP), ("Questions & answers", FAQ_URL), ("Insurance terms", GLOSS), ("Claim library", POST_BASE)]


def _groups():
    return [
        ("What we appraise", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE)),
        ("Cities & towns", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All cities and towns", LOC_BASE)),
        ("Estimators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free estimators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def gtm_head():
    if not GTM_ID:
        return ""
    if GTM_HEAD_SNIPPET:
        return f"<!-- Google Tag Manager -->\n{GTM_HEAD_SNIPPET}\n<!-- End Google Tag Manager -->\n"
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", "ic sm")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "ic chev")}</button><ul class="drop{wide}">{li}</ul></li>'
    menu += f'<li><a class="plain" href="{ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About us</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand_block("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-r"><a class="head-tel" href="tel:{TEL}" aria-label="Call {PHONE}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-coral head-cta" href="{CONTACT}">Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_block("md")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 14 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Not sure the settlement covers the repair?</h2><p>Send us the carrier’s estimate. We’ll tell you plainly whether appraisal is worth it.</p><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Email the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand_block("mf")}
<p>Independent appraisal, estimate review and umpire work for property owners with disputed insurance claims — from the Berkshires to Provincetown.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm ET</li></ul></div>
<div><h3>What we appraise</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Cities &amp; towns</h3><ul>{loc}<li><a href="{LOC_BASE}">Statewide coverage</a></li></ul></div>
<div><h3>Free estimators</h3><ul>{tl}</ul></div>
<div><h3>Resources</h3><ul><li><a href="{ABOUT}">About us</a></li>{"".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN)}<li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Content on this site is general and educational; policy wording controls. Outcomes are never guaranteed, and example figures are illustrative.</p>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/legal-disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="{SITEMAP_HTML}">Site index</a></li></ul></div></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("mail")} Free review</a></div>"""


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None):
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
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
            if t in ("Service", "WebApplication"):
                n["provider"] = {"@id": DOMAIN + "/#business"}
        extra.append(n)
    img_key = preload or "snowy-rowhouses"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    order = ["Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"]
    mains = sorted([n for n in extra if n.get("@type") in order], key=lambda n: order.index(n["@type"]))
    webpage["mainEntity"] = {"@id": mains[0]["@id"]} if mains else {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        p = PHOTOS[preload]
        if p["fw"] > 640:
            pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {p["fw"]}w" imagesizes="100vw">\n'
        else:
            pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<script>(function(l){{var a="{HOST}";if(l.hostname==="www."+a||(l.hostname===a&&l.protocol==="http:"))l.replace("https://"+a+l.pathname+l.search+l.hash)}})(location);document.documentElement.className="js"</script>
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Massachusetts">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Massachusetts">
<meta name="geo.region" content="US-MA">
<meta name="geo.placename" content="Massachusetts">
<meta name="theme-color" content="#202734">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
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
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    c = f'<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    f = ""
    if facts:
        f = '<div class="wrap"><dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl></div>"
    return f"""<section class="phero{' has-facts' if facts else ''}"><div class="phero-media">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.1"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}</div>{f}</section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev")}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through</h2><p>The first conversation is free. We’ll tell you honestly whether appraisal fits your claim.</p><a class="box-tel" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-coral full" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow", "ic sm")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Is the carrier’s number short?", p="Send us the estimate and a few photos. We’ll review the gap and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(cards):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow", "ic sm")}</a>' for k, n, p in cards) + "</div>"


LOSSES = ["Ice dam / snow load", "Wind / nor’easter", "Hurricane / tropical storm", "Water / burst pipe", "Fire / smoke", "Fallen tree", "Hail", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=3):
    roles = ["Homeowner", "Condo owner / trustee", "Landlord / multifamily", "Commercial owner", "Property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Massachusetts"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
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
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="/privacy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-ink full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-t">Request a free claim review</h2><p class="sub">A few details now — we call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="/privacy/">privacy policy</a>.</span></label>
<button class="btn btn-coral full" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Greater Boston", "Boston · Cambridge · Quincy", ["Nor’easters", "Ice dams", "Condo losses", "Coastal flooding"],
     "Dense triple-deckers, brownstones and condo associations mean one storm can touch dozens of owners — and a master policy, an HO-6 and a unit owner’s own claim all at once.", "boston-charles"),
    ("North Shore & Merrimack Valley", "Salem · Lowell · Gloucester", ["Wind-driven rain", "Mill-building losses", "Frozen pipes", "Tree fall"],
     "Federal-era homes in Salem, converted mill lofts in Lowell and Lawrence, and exposed coastline from Lynn to Rockport each bring their own estimating quirks.", "brick-mainstreet"),
    ("South Shore & South Coast", "Plymouth · Brockton · New Bedford", ["Storm surge", "Roof wind damage", "Flood vs. wind", "Triple-decker fires"],
     "The March 2018 nor’easters showed how fast surge and wind can hit Quincy, Scituate and Marshfield. Further south, New Bedford’s hurricane barrier protects the harbor but not every street.", "harbor-boats"),
    ("Cape Cod & the Islands", "Barnstable · Falmouth · Nantucket", ["Hurricane deductibles", "Salt-air wear", "Cedar shingles", "Seasonal-home leaks"],
     "Percentage hurricane deductibles, FAIR Plan policies and seasonal homes that sit empty for months make Cape and Islands claims a category of their own.", "cape-cottages"),
    ("Central Massachusetts", "Worcester · Fitchburg · Framingham", ["Ice storms", "Snow load", "Tornadoes", "Fallen hardwoods"],
     "Higher elevations collect heavier snow and ice. The December 2008 ice storm and the 1953 Worcester tornado are reminders that inland claims can be just as severe.", "snowy-street"),
    ("Pioneer Valley & the Berkshires", "Springfield · Northampton · Pittsfield", ["Tornadoes", "River flooding", "Hail", "Barn & outbuilding damage"],
     "The June 2011 tornado cut from Westfield through Springfield to Brimfield, and Tropical Storm Irene flooded Berkshire and Franklin County river towns the same summer.", "berkshire-hills"),
]

ALMANAC = [
    ("1938", "The Great New England Hurricane", "A fast-moving hurricane brought destructive surge to Buzzards Bay and wind damage far inland. It still shapes coastal building rules and hurricane barrier design.", "storm"),
    ("1953", "Worcester tornado", "On June 9, an F4 tornado tore through Worcester County — one of the deadliest tornadoes in U.S. history and proof that inland Massachusetts sees violent wind.", "wind"),
    ("1978", "The Blizzard of ’78", "A February nor’easter buried eastern Massachusetts and pushed record tides into coastal towns. Homes were lost along the South Shore.", "snow"),
    ("1991", "Hurricane Bob & the Halloween nor’easter", "Bob raked Cape Cod and the South Coast in August; weeks later the “Perfect Storm” battered the same shoreline with surf and surge.", "wave"),
    ("2008", "December ice storm", "Ice-laden trees and lines collapsed across Worcester County and north-central Massachusetts, leaving many homes without power for days.", "snow"),
    ("2011", "Springfield tornado & Irene", "An EF3 tornado crossed the Pioneer Valley on June 1. Tropical Storm Irene flooded western river towns that August.", "wind"),
    ("2015", "Record-setting snow", "Boston logged about 110 inches for the season. Roof collapses and ice dam leaks filled claim queues from Worcester to the Cape.", "snow"),
    ("2018", "Back-to-back March nor’easters", "Coastal flooding swamped Boston Harbor streets, Quincy, Scituate and Marshfield, followed by heavy wet snow and fallen trees.", "drop"),
]


def home():
    svc_cards = "".join(
        f'<a class="card svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-media">{img(SVC_CARD[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="num">{i + 1:02d}</span></span>'
        f'<span class="card-body"><span class="card-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><span class="card-p">{e(s["short"])}</span><span class="more">Learn more {ic("arrow", "ic sm")}</span></span></a>'
        for i, s in enumerate(SERVICES[:9]))
    almanac = "".join(f'<article class="alm-card"><span class="alm-ic">{ic(icn)}</span><span class="alm-year">{y}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for y, t, p, icn in ALMANAC)
    road = "".join(f'<li class="rstep rv"><span class="rnum">{i + 1}</span><div><h3>{e(n)}</h3><p>{e(t)}</p></div></li>' for i, (n, t) in enumerate(PROCESS_STEPS[:6]))
    regions = "".join(
        f'<article class="region rv"><div class="region-media">{img(ph, sizes="(max-width:700px) 86vw, 420px", alt="")}</div><div class="region-body"><p class="region-sub">{e(sub)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p></div></article>'
        for n, sub, perils, t, ph in REGIONS)
    tools = "".join(
        f'<a class="card tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-media">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="badge">{e(t["kind"])}</span></span><span class="card-body"><h3>{e(t["name"])}</h3><span class="card-p">{e(t["short"])}</span><span class="more">Open {ic("arrow", "ic sm")}</span></span></a>'
        for t in TOOLS[:6])
    towns = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow", "ic sm")}</a></li>' for l in LOCATIONS)
    posts = "".join(
        f'<article class="post rv"><a class="post-media" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="post-body"><p class="meta">{e(p["read"])} read · Claim library</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    home_faqs = [
        ("What does a Massachusetts Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As the appraiser you appoint, we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is appraisal the same as the “reference” in the Massachusetts standard policy?", "They are closely related. The Massachusetts standard fire policy provides for disinterested referees to decide the amount of loss, and many homeowner forms call that process appraisal. Your own policy wording controls."),
        ("When is it worth calling a Massachusetts Insurance Appraiser?", "When coverage is accepted, you have the carrier’s itemized estimate, and the gap to your contractor’s number is meaningful — often more than about 10% or several thousand dollars."),
        ("Does appraisal decide coverage or bad-faith claims?", "No. Appraisal decides the amount of loss. Coverage questions and claims under Massachusetts consumer-protection laws are matters for an attorney."),
        ("How are fees handled?", "Each side pays its own appraiser, and the umpire’s fee is usually split evenly. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you work outside Greater Boston?", "Yes. We work in all 14 counties, from Pittsfield and Springfield to Worcester, the South Coast, Cape Cod and the Islands."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("snowy-rowhouses", "bg", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · All 351 cities &amp; towns</p>
<h1>Massachusetts Insurance Appraiser for <em>disputed</em> property claims</h1>
<p class="lede">The carrier accepted your claim, but the payment won’t rebuild what the storm, the ice dam or the fire took. Massachusetts Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal process in your policy.</p>
<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#services">What we appraise {ic("arrow")}</a></div>
<ul class="hero-points"><li>{ic("check")}Appointed by you, not the carrier</li><li>{ic("check")}Homes, condos, HOAs &amp; commercial</li><li>{ic("check")}Ice dam, nor’easter, fire &amp; water losses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="figures" aria-label="At a glance"><div class="wrap figures-in">
<div class="fig rv"><b data-count="14">14</b><span>counties covered, Berkshire to Barnstable</span></div>
<div class="fig rv"><b data-count="351">351</b><span>cities and towns in our service area</span></div>
<div class="fig rv"><b data-count="11">11</b><span>appraisal and estimating services</span></div>
<div class="fig rv"><b data-count="7">7</b><span>free, private claim estimators</span></div>
</div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-media rv">
<figure class="im-a">{img("roof-repair-lift", sizes="(max-width:900px) 90vw, 440px")}</figure>
<figure class="im-b">{img("consultation", sizes="(max-width:900px) 60vw, 300px")}</figure>
</div>
<div class="intro-copy rv">
<p class="kicker">Covered isn’t the same as paid</p>
<h2>What a Massachusetts Insurance Appraiser actually does</h2>
<p>Most short claims aren’t denials. They’re estimates that skip the ice and water shield, price a 12/12 Cape roof as if it were walkable, or patch one wall of cedar shingles that will never match. A Massachusetts Insurance Appraiser closes that distance with a valuation built from our own inspection — then defends it in front of the carrier’s appraiser and, if needed, an umpire.</p>
<ul class="ticks">
<li>{ic("check")}<span><b>Independent scope.</b> We measure and photograph before we read anyone else’s numbers.</span></li>
<li>{ic("check")}<span><b>Local pricing.</b> Labor and materials priced for where the property actually is — Back Bay is not Berkshire County.</span></li>
<li>{ic("check")}<span><b>Straight answers.</b> If your file needs an attorney or a simple supplement instead, we say so on the first call.</span></li>
</ul>
<a class="btn btn-ink" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec sec-fog" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">What we appraise</p><h2>Claims a Massachusetts Insurance Appraiser can value</h2><p>From a single estimate review to full panel representation, each service is built around one deliverable: a number that holds up.</p></div>
<div class="card-grid" data-stagger>{svc_cards}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">See all 11 services {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-ink almanac" data-scroller><div class="wrap">
<div class="sec-head split-head rv"><div><p class="kicker light">Storm almanac</p><h2>Massachusetts weather that fills claim files</h2><p>Hurricanes, nor’easters, ice storms and the occasional tornado. Every storm leaves a different fingerprint on a roof — and in an estimate. A Massachusetts Insurance Appraiser has to read all of them.</p></div>
<div class="alm-nav"><button type="button" class="alm-btn" data-dir="-1" aria-label="Previous storms">{ic("left")}</button><button type="button" class="alm-btn" data-dir="1" aria-label="Next storms">{ic("arrow")}</button></div></div>
</div>
<div class="alm-track" tabindex="0" aria-label="Notable Massachusetts storms">{almanac}</div>
</section>

<section class="sec"><div class="wrap road-wrap">
<div class="road-head rv"><p class="kicker">The roadmap</p><h2>How a Massachusetts Insurance Appraiser moves a stalled claim</h2><p>Appraisal turns an open-ended argument into a defined process with a binding result. These are the six moves that matter most.</p><a class="link" href="{ROADMAP}">Read the full roadmap {ic("arrow", "ic sm")}</a></div>
<ol class="roadmap">{road}</ol>
</div></section>

<section class="sec sec-fog"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Regional know-how</p><h2>Six regions, six claim patterns</h2><p>A Massachusetts Insurance Appraiser working the Cape faces different questions than one in the Pioneer Valley. Swipe through the regions we cover.</p></div>
</div>
<div class="region-track" data-stagger>{regions}</div>
</section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free estimators from Massachusetts Insurance Appraiser</h2><p>Check the math before you pick up the phone. Every estimator runs in your browser; nothing is stored or sent.</p></div>
<div class="card-grid three" data-stagger>{tools}</div>
<p class="center mt"><a class="link" href="{TOOL_BASE}roof-snow-load-estimator/">New: roof snow load estimator for Massachusetts winters {ic("arrow", "ic sm")}</a></p>
</div></section>

<section class="sec sec-coral"><div class="wrap gapcheck">
<div class="rv"><p class="kicker">Quick gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two numbers you already have. A large gap is worth a conversation with a Massachusetts Insurance Appraiser; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}appraisal-award-gap-estimator/">award gap &amp; fee estimator</a> subtracts appraiser and umpire costs.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap towns">
<div class="towns-copy rv"><p class="kicker">Cities &amp; towns</p><h2>Where we’re called most often</h2><p>Massachusetts Insurance Appraiser covers all 351 cities and towns. These local pages cover county, neighborhoods, storm history and housing stock for the places we visit most.</p><figure class="towns-media">{img("boston-rooftops", sizes="(max-width:900px) 100vw, 420px")}</figure><a class="btn btn-line" href="{LOC_BASE}">Statewide coverage {ic("arrow")}</a></div>
<ul class="town-list" data-stagger>{towns}</ul>
</div></section>

<section class="pcta">{img("berkshire-hills", "bg", alt="", extra=' data-parallax="0.2"')}<div class="wrap pcta-in rv"><p class="kicker light">Before the next storm season</p><h2>The best time to question a settlement is before you sign it</h2><p>A short review now can keep you from accepting a payment that won’t cover the repair. Massachusetts Insurance Appraiser will look at the numbers with you.</p><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Massachusetts Insurance Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Choosing the right one first saves months and fees.</p></div>
<div class="compare" data-stagger>
<div class="cmp cmp-hl rv"><h3>Massachusetts Insurance Appraiser</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Award signed by two of three panel members</dd><dt>Decides coverage?</dt><dd>No</dd></dl></div>
<div class="cmp rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare and negotiate the whole claim</dd><dt>Best stage</dt><dd>Early, soon after the loss</dd><dt>Result</dt><dd>Negotiated settlement</dd><dt>Decides coverage?</dt><dd>No</dd></dl></div>
<div class="cmp rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Legal rights, denials and litigation</dd><dt>Best stage</dt><dd>Denials, deadlines, c. 93A / 176D questions</dd><dt>Result</dt><dd>Settlement or judgment</dd><dt>Decides coverage?</dt><dd>Argues it; a court decides</dd></dl></div>
</div>
</div></section>

<section class="sec sec-fog"><div class="wrap faq-wrap">
<div class="rv"><p class="kicker">Questions</p><h2>What people ask a Massachusetts Insurance Appraiser</h2><p>Short, plain answers. There are more on the <a href="{FAQ_URL}">questions &amp; answers</a> page and in the <a href="{GLOSS}">insurance terms</a> glossary.</p></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Claim library</p><h2>Read this before you invoke appraisal</h2><p>Guides on policy wording, documentation and strategy for Massachusetts property owners.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p class="center mt"><a class="btn btn-line" href="{POST_BASE}">Browse the claim library {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-ink" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker light">Start with a conversation</p><h2>Talk with a Massachusetts Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer about whether appraisal is worth pursuing.</p>
<ul class="contact-lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin")}<span><small>Coverage</small><b>All 14 Massachusetts counties</b></span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Appraisal",
                        "Massachusetts Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid ice dam, storm, water and fire claims.",
                        body, [faq_schema(home_faqs)], preload="snowy-rowhouses"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("What we appraise", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[idx % 6: idx % 6 + 5]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Common questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All cities and towns", LOC_BASE)])}</aside></div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s.get("kw", s["name"]), "description": s["desc"], "areaServed": {"@type": "State", "name": "Massachusetts"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("What we appraise", SVC_BASE)]
    cards = "".join(
        f'<a class="card svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-media">{img(SVC_CARD[s["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="num">{i + 1:02d}</span></span><span class="card-body"><span class="card-ic">{ic(SVC_ICON[s["slug"]])}</span><h2 class="h3">{e(s["name"])}</h2><span class="card-p">{e(s["short"])}</span><span class="more">Learn more {ic("arrow", "ic sm")}</span></span></a>'
        for i, s in enumerate(SERVICES))
    idx_faq = [("Can I hire you for just an estimate review?", "Yes. Many owners start with a review and decide afterward whether to invoke appraisal."), ("Do you handle condo associations and commercial buildings?", "Yes — single-family homes, condos and master policies, multifamily, retail, office, mixed-use, churches and other commercial property."), ("Do you only handle storm claims?", "No. We value ice dam, wind, hurricane, water, fire, tree and other covered losses.")]
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services in Massachusetts",
                     "Eleven services built around an accurate, defensible valuation of your loss — from a one-time estimate review to full appraisal panel representation and neutral umpire work.", "roof-repair-lift") + f"""
<section class="sec"><div class="wrap"><div class="card-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-fog"><div class="wrap faq-wrap"><div class="rv"><p class="kicker">Where to start</p><h2>Most files start with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn btn-ink" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block(idx_faq)}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Massachusetts",
                             "Massachusetts insurance appraisal services: panel representation, estimate review, ice dam, nor’easter, water, fire and condo claims, plus umpires.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items), faq_schema(idx_faq)], preload="roof-repair-lift"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities & towns", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                         [("County", l["county"]), ("Housing", l["housing"]), ("Storm on record", l["storm"])]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local-risks"><p class="h">Claim risks in {e(l["city"])}</p><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Services for {e(l["city"])} property owners</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding towns, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} questions</h2>{faq_block(l["faqs"])}
<h2>Nearby</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
<aside class="aside">{call_box()}{list_box("Cities & towns", items, path)}{list_box("Free estimators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Massachusetts"}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Cities & towns", LOC_BASE)]
    towns = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow", "ic sm")}</a></li>' for l in LOCATIONS)
    regions = "".join(
        f'<article class="region rv"><div class="region-media">{img(ph, sizes="(max-width:700px) 86vw, 420px", alt="")}</div><div class="region-body"><p class="region-sub">{e(sub)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p></div></article>'
        for n, sub, perils, t, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 14 Massachusetts Counties",
                     "We work in all 351 cities and towns — from the New York line to Provincetown. These pages cover the communities where we’re called most often.", "blue-hills-skyline") + f"""
<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="kicker">Local pages</p><h2>Cities and towns we visit most</h2></div><ul class="town-list wide" data-stagger>{towns}</ul></div></section>
<section class="sec sec-fog"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across the state</h2><p>The same policy language plays out very differently in a Back Bay condo, a Worcester triple-decker and a Truro cottage.</p></div></div><div class="region-track" data-stagger>{regions}</div></section>
{cta_strip("Don’t see your town?", "We cover every Massachusetts county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Massachusetts Insurance Appraiser | Cities & Towns",
                             "Insurance appraisal in all 14 Massachusetts counties, including Boston, Worcester, Springfield, Lowell, Quincy, New Bedford, Cape Cod and Pittsfield.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload="blue-hills-skyline"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Estimators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv-s">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on what you enter and your policy terms; they are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>About this {e(t["kind"].lower())}</h2>{faq_block(t["faqs"])}
<h2>More free estimators</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("All estimators", items, path)}</aside></div>
{cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Estimators", TOOL_BASE)]
    cards = "".join(
        f'<a class="card tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-media">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="badge">{e(t["kind"])}</span></span><span class="card-body"><h2 class="h3">{e(t["name"])}</h2><span class="card-p">{e(t["short"])}</span><span class="more">Open {ic("arrow", "ic sm")}</span></span></a>'
        for t in TOOLS)
    order = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(n)}</a> — {e(w)}</li>' for s, n, w in [
        ("claim-calendar-builder", "Claim calendar builder", "so no deadline slips"),
        ("roof-area-pitch-converter", "Roof area & pitch converter", "to check the carrier’s squares"),
        ("hurricane-deductible-calculator", "Hurricane deductible calculator", "if you’re near the coast"),
        ("rcv-acv-holdback-calculator", "RCV / ACV holdback calculator", "to see when the money arrives"),
        ("appraisal-award-gap-estimator", "Award gap & fee estimator", "to size the dispute"),
        ("appraisal-file-checkup", "Appraisal file checkup", "before you invoke appraisal")])
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Massachusetts",
                     "Seven estimators built from real appraisal work — including a roof snow load estimator for New England winters. No sign-up and nothing stored.", "calculator-notes", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="card-grid" data-stagger>{cards}</div></div></section>
<section class="sec sec-fog"><div class="wrap faq-wrap"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the estimators together</h2><ol class="steps-list">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Massachusetts",
                              "Seven free property claim estimators: appraisal award gap, RCV/ACV holdback, roof squares, hurricane deductible, claim calendar and snow load.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], preload="calculator-notes"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = ROADMAP
    trail = [("Home", "/"), ("Appraisal roadmap", path)]
    body = page_hero(trail, "Process guide", "Insurance Appraisal Roadmap for Massachusetts Claims",
                     "Eight steps from the first disagreement to a signed award — what happens, who does what and where files most often go wrong.", "roofers-barn",
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "Two appraisers + umpire"), ("Binding", "Two of three signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works for a Massachusetts property claim", "totalTime": "P90D",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{DOMAIN}{path}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Roadmap | Massachusetts, Step by Step",
                         "A step-by-step roadmap of insurance appraisal in Massachusetts: the written demand, appraisers, the umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], preload="roofers-barn"), 0.8)

    path = FAQ_URL
    trail = [("Home", "/"), ("Questions & answers", path)]
    toc = "".join(f'<a href="#q-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions & Answers",
                     "Plain answers about the appraisal process, costs, timing, Massachusetts rules, condos, coastal homes and winter claims.", "snow-red-house") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="Topics">{toc}</nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Massachusetts Answers",
                         "Answers to common Massachusetts insurance appraisal questions, grouped by topic: process, fees, deadlines, state rules, condos and winter claims.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="snow-red-house"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Insurance terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards — including Massachusetts-specific ones — in plain English.", "slate-tiles", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, Umpire, Ice Dam & More",
                         "Searchable glossary of property insurance claim terms: ACV, RCV, appraisal award, umpire, ice dam, master policy, FAIR Plan and many more.",
                         body, [crumbs_schema(trail), dts], preload="slate-tiles"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim library", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free estimators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "keywords": p.get("kw", ""), "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim library", path)]
    cards = "".join(
        f'<article class="post rv"><a class="post-media" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="post-body"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</p><h2 class="h3"><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS)
    body = page_hero(trail, "Claim library", "Insurance Claim Guides for Massachusetts Owners",
                     "Practical reading on policy wording, documentation and strategy — written for Massachusetts homes, condos and commercial buildings.", "cedar-shingles", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Claim Guides | Massachusetts Claim Library",
                         "Guides for Massachusetts owners on the reference clause, ice dam claims, nor’easter wind vs. flood, condo master policies and choosing an umpire.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="cedar-shingles"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About us", path)]
    body = page_hero(trail, "About us", "About Massachusetts Insurance Appraiser",
                     "An independent appraisal and estimating practice built on one idea: a covered property claim should be paid on what the damage actually costs to repair.", "boston-charles") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("advisors-laptop", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on the amount of loss</h2>
<p>Many claim professionals do a little of everything. We chose to specialize in the one question appraisal answers: how much the covered damage costs. That focus lets us serve as the appraiser you appoint, review an estimate before a dispute hardens, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect, measure and photograph before we look at anyone else’s numbers.</li>
<li><strong>Defensible over dramatic.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your file needs an attorney, a public adjuster or simply a supplement, we tell you.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners and trustees, landlords, property managers, churches, business owners, contractors, public adjusters and attorneys. On any one claim we serve in a single role, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We can’t guarantee outcomes — no honest appraiser can.</p>
<h2>Built for Massachusetts</h2>
<p>A Back Bay brownstone, a Worcester triple-decker, a Lowell mill loft and a Chatham cottage have little in common except the weather that tests them. We price each with local labor and material costs, and with an eye for what New England estimates tend to miss: ice and water shield, slate and cedar matching, steep and high-roof charges, and code items that apply when older homes are repaired.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("What we appraise", SVC_BASE), ("Cities & towns", LOC_BASE), ("Free estimators", TOOL_BASE), ("Appraisal roadmap", ROADMAP)])}</aside></div>{cta_strip()}"""
    write(path, document(path, f"About Us | {BRAND}",
                         "Massachusetts Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="boston-charles"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Massachusetts Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "advisors-laptop", cta=False) + f"""
<section class="sec sec-ink"><div class="wrap contact">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin")}<span><small>Service area</small><b>All 351 cities and towns</b></span></li></ul>
<h3>Helpful to have ready</h3><ul class="plain-list"><li>Declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters and emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND}",
                         "Get a free review of a disputed Massachusetts property claim. Call or text (844) 537-1427 or email the estimate and photos to our team.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="advisors-laptop"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"] or k)}<br><small>{e(v.get("creator") or "Unknown")} · {e(v["source"])}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        "/privacy/": ("Privacy Policy", "How we collect, use and protect the information you share with us through this website.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share — such as your name, phone number, email address, property location and claim details. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our site and email, or when the law requires it.</p>
<h2>Estimators</h2><p>Our calculators and checklists run in your browser. What you enter isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data. If we add analytics, it will be described here.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>To access, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""),
        "/terms/": ("Terms of Use", "The terms that apply when you use this website, its content and its free claim estimators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is provided for general information about insurance appraisal and property claims in Massachusetts.</p>
<h2>No client relationship</h2><p>Reading the site, using its estimators or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ and laws change. Consult a licensed Massachusetts attorney for legal questions.</p>
<h2>Estimators</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and estimators belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or estimators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the Commonwealth of Massachusetts.</p>"""),
        "/legal-disclaimer/": ("Disclaimer", "Important limits on the general information, examples and estimators published on this website.", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, don’t give legal advice, and don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes them. If a deadline is near, consult a Massachusetts attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to laws, agencies and storms are for context. Check current law and facts with official sources such as the Massachusetts Division of Insurance.</p>"""),
        "/photo-credits/": ("Photo Credits", "Sources and licenses for every photograph used on this website, with links to the originals.", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> (via StockSnap, rawpixel, Flickr and WordPress Photos) or a <strong>public-domain</strong> work such as photos by U.S. government agencies (including MassDOT, USDA and the U.S. Fish &amp; Wildlife Service). Images were found through the Openverse search engine. Attribution isn’t required, but we credit the photographers with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (title, lede, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal" if path != "/photo-credits/" else "Credits", title, lede, "brick-commercial", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", f"{title} for {BRAND} ({HOST}). {lede}"[:150].rstrip(), body, [crumbs_schema(trail)], preload="brick-commercial"), 0.3)


def sitemap_pages():
    path = SITEMAP_HTML
    trail = [("Home", "/"), ("Site index", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", ABOUT), ("Contact", CONTACT)]),
        ("What we appraise", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities & towns", [("All cities and towns", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free estimators", [("All estimators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy/"), ("Terms of use", "/terms/"), ("Disclaimer", "/legal-disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="idx-col rv"><h2 class="h3">{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on {BRAND}, grouped by section.", "brick-commercial", cta=False) + f'<section class="sec"><div class="wrap idx-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"A complete index of every page on {BRAND}: services, Massachusetts cities and towns, free estimators and claim guides.", body, [crumbs_schema(trail)], preload="brick-commercial"), 0.3)

    body = f"""<section class="phero"><div class="phero-media">{img("trees-down-lawn", "bg", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page came down in the storm</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn btn-coral" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Services</a><a class="btn btn-line light" href="{TOOL_BASE}">Free estimators</a><a class="btn btn-line light" href="{CONTACT}">Contact</a></div></div></section>"""
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
        f.write(INDEX_PHP.replace("__HOST__", HOST))


INDEX_PHP = r"""<?php
// Massachusetts Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$apex = '__HOST__';

// Canonical host and scheme - only on the real domain (TLS terminates upstream, so check X-Forwarded-Proto).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ? 'https' : 'http'));
if ($host === 'www.' . $apex || ($host === $apex && $proto === 'http')) {
    header('Location: https://' . $apex . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== $apex) {
    header('X-Robots-Tag: noindex, nofollow');
}

if (strpos($path, '..') !== false || strpos($path, '/api/_private') === 0) {
    $path = '/__invalid__';
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    $qs = $_SERVER['QUERY_STRING'] ?? '';
    header('Location: ' . $path . '/' . ($qs !== '' ? '?' . $qs : ''), true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
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
