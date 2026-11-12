#!/usr/bin/env python3
"""Static site generator for arkansasinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only.
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

BRAND = "Arkansas Insurance Appraiser"
HOST = "arkansasinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112b"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no GTM output.
GTM_ID = ""

SVC_BASE = "/claim-appraisal-services/"
LOC_BASE = "/arkansas-locations/"
TOOL_BASE = "/property-claim-tools/"
POST_BASE = "/appraisal-guides/"
P_PROCESS = "/appraisal-process-explained/"
P_FAQ = "/faq/"
P_GLOSS = "/insurance-claim-glossary/"
P_ABOUT = "/company/"
P_CONTACT = "/contact-an-appraiser/"
P_PRIVACY = "/privacy-information/"
P_TERMS = "/website-use-terms/"
P_DISC = "/appraisal-disclaimer/"
P_CREDITS = "/photo-credits/"
P_MAP = "/site-navigation/"

e = html.escape
pages = []  # (path, priority)


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-appraiser/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "house-dark-sky": "Farmhouse standing in an open green field under dark storm clouds",
    "hero-roofline": "Aerial view of a gray shingle roof on a single-story home",
    "roof-missing": "Aerial view of a shingle roof with storm-torn shingles missing near the ridge",
    "roof-aerial-hip": "Aerial view of a hip roof with dark architectural shingles",
    "roofer-tarp": "Roofer on a lift beside a brick gable covered with a blue tarp",
    "roof-crew": "Roofing crew stripping an old barn roof from a lift",
    "roof-edge-damage": "Close-up of a damaged roof edge with exposed decking and fascia",
    "tornado-field": "Debris and splintered trees across a field after the February 2008 tornado near Atkins, Arkansas",
    "debris-inspector": "FEMA inspector walking through tornado debris near Atkins, Arkansas",
    "fallen-oaks": "Large fallen oak trees around a brick ranch house after a windstorm",
    "snapped-tree": "Tall tree snapped at the trunk and lying across a lawn after a storm",
    "ice-tree-car": "Ice-coated tree limbs collapsed over a parked car and apartment building",
    "ice-limb": "Heavy limb split from an ice-covered tree during an ice storm",
    "icicles-gutter": "Long icicles hanging from a gutter along a building",
    "storm-sky": "Dark storm clouds and rain shafts over open green fields",
    "storm-rain": "Rain curtain falling from a storm cloud over a small town",
    "bungalow": "Craftsman bungalow with a front porch and stone steps",
    "snow-house": "Two-story home with shrubs bent under heavy snow",
    "church": "White frame church with a tall steeple",
    "little-rock-skyline": "Little Rock skyline at dusk seen across the Arkansas River",
    "ozark-overlook": "Autumn forest across the rolling hills of the Ozarks",
    "arkansas-river-valley": "River winding through a wooded valley seen from a mountain overlook",
    "fort-smith": "Historic red brick building on the grounds of the Fort Smith National Historic Site",
    "pine-bluff": "Jefferson County Courthouse with its clock tower in Pine Bluff",
    "springdale-creek": "Spring Creek and a greenway bridge in Springdale",
    "bentonville": "Glass museum building reflected in a pond in Bentonville",
    "consultation": "Two people shaking hands across a table after a consultation",
    "meeting": "Hands resting on a desk beside open notebooks during a meeting",
    "planner": "Notebook, coffee cup and phone on a table during a planning session",
    "kitchen": "Kitchen and living area with wood cabinets and plank flooring",
    "house-fire": "Farmhouse burning behind a wooden fence",
    "calculator": "Calculator, pencil and sticky notes on a desk",
    "paperwork": "Calculator on printed charts beside a laptop",
    "commercial": "Aerial view of a strip shopping center and parking lot",
    "checklist": "Hands filling out a paper form with a pencil",
    "hot-springs": "Row of historic stucco cottages with tile roofs at a motel in Hot Springs",
    "ozark-cabin": "Weathered wooden house under oak trees in the Ozark hills",
    "fayetteville": "Historic brick commercial building on a corner in Fayetteville",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT.get(key, p["title"]))
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appointed-appraiser-representation": "consultation", "home-insurance-claim-appraiser": "bungalow",
    "commercial-hoa-property-appraisal": "commercial", "roof-hail-damage-appraisal": "roof-missing",
    "tornado-wind-damage-appraisal": "tornado-field", "hurricane-remnant-wind-appraisal": "snapped-tree",
    "water-damage-claim-appraiser": "kitchen", "fire-smoke-loss-appraisal": "house-fire",
    "ice-storm-freeze-damage-appraisal": "ice-tree-car", "carrier-estimate-review": "calculator",
    "appraisal-umpire-services": "meeting",
}
LOC_PHOTO = {
    "little-rock": "little-rock-skyline", "north-little-rock": "arkansas-river-valley", "fort-smith": "fort-smith",
    "fayetteville": "fayetteville", "springdale": "springdale-creek", "rogers": "roof-aerial-hip",
    "bentonville": "bentonville", "jonesboro": "storm-rain", "conway": "debris-inspector",
    "pine-bluff": "pine-bluff", "hot-springs": "hot-springs", "texarkana": "fallen-oaks",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator", "rcv-acv-holdback-calculator": "paperwork",
    "roof-pitch-squares-calculator": "hero-roofline", "wind-hail-percentage-deductible": "storm-sky",
    "claim-timeline-builder": "planner", "appraisal-readiness-checkup": "checklist", "ice-load-limb-calculator": "ice-limb",
}
POST_PHOTO = {
    "arkansas-appraisal-clause-basics": "meeting", "labor-depreciation-arkansas-acv": "paperwork",
    "ice-storm-claims-trees-gutters-roofs": "icicles-gutter", "tornado-claim-first-30-days": "debris-inspector",
    "hail-documentation-northwest-arkansas": "roof-missing", "river-flood-vs-wind-coverage": "arkansas-river-valley",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M4 12h15M13 5l7 7-7 7"/>',
    "check": '<path d="M4.5 12.5l5 5L19.5 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "gem": '<path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M12 21L8 9l4-6 4 6z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "gap": '<path d="M3 20h18M6 16V9M12 16V5M18 16v-4"/>',
    "dep": '<path d="M3 3v18h18"/><path d="M7 7l4 5 3-2 5 7"/>',
    "roof": '<path d="M2 13L12 4l10 9"/><path d="M5 11v9h14v-9"/>',
    "pct": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "cal": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "ice": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
}


def ic(name, cls="", size=20):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


def mark(size=44):
    """Brand mark: dark red badge, white roofline, teal diamond (value) beneath it."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<circle cx="24" cy="24" r="24" fill="#8f1d24"/><circle cx="24" cy="24" r="20.5" fill="none" stroke="#ffffff" stroke-opacity=".22" stroke-width="1.5"/>'
            '<path d="M11.5 23.5L24 13l12.5 10.5" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M24 22.5l6 6.5-6 7.5-6-7.5z" fill="#4fc1b9"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "AR", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-AR", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 75 Arkansas counties.",
        "areaServed": [{"@type": "State", "name": "Arkansas"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Tornado damage", "Ice storm damage"],
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


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Arkansas locations", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All claim tools", TOOL_BASE)),
        ("Resources", [("Appraisal process", P_PROCESS), ("FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Appraisal guides", POST_BASE)] +
         [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS[:3]], None),
    ]


def header():
    menu = ""
    for name, links, allk in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", size=14)}</a></li>'
        wide = " wide" if len(links) > 7 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false">{name}{ic("chev", "chev", 14)}</button><ul class="sub{wide}">{li}</ul></li>'
    menu += f'<li><a href="{P_ABOUT}">Company</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="strong" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += (f'<li><button type="button" class="acc" aria-expanded="false" aria-controls="dz-{i}">{name}{ic("chev", "chev", 18)}</button>'
                f'<div class="acc-p" id="dz-{i}"><ul>{li}</ul></div></li>')
    acc += f'<li><a href="{P_ABOUT}">Company</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="top"><div class="wrap hdr-in">
<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent property claim appraisal</small></span></a>
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="hdr-call" href="tel:{TEL}">{ic("phone", size=18)}<span><small>Free claim review</small>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark(38)}<span class="brand-t"><b>{BRAND}</b><small>Independent property claim appraisal</small></span></a><button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x", size=22)}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-red" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · All 75 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="ft">
<div class="ft-cta"><div class="wrap"><h2>Covered, but not paid in full? Let’s compare the numbers.</h2><div class="row"><a class="btn btn-white" href="tel:{TEL}">{ic("phone", size=18)} {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Email the estimate</a></div></div></div>
<div class="wrap ft-grid">
<div class="ft-about"><a class="brand" href="/">{mark(40)}<span class="brand-t"><b>{BRAND}</b><small>Independent property claim appraisal</small></span></a>
<p>Independent appraisal, estimate review and umpire services for Arkansas property owners, from the Ozark Plateau to the Delta and the pine country of the Gulf Coastal Plain.</p>
<p class="ft-lines"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm CT</span></p></div>
<div><h2>Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2>Locations</h2><ul>{loc}<li><a href="{LOC_BASE}">All locations</a></li></ul></div>
<div><h2>Free tools</h2><ul>{tl}</ul></div>
<div><h2>Company</h2><ul><li><a href="{P_ABOUT}">About the company</a></li><li><a href="{P_PROCESS}">Appraisal process</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap ft-base"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_CREDITS}">Photo credits</a></li><li><a href="{P_MAP}">Site navigation</a></li></ul></div>
<p class="wrap ft-legal">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general and educational; your policy’s terms control. Example figures are illustrative, and no result is guaranteed.</p>
</footer>
<a class="totop" href="#top" aria-label="Back to top"><svg class="totop-ring" width="52" height="52" viewBox="0 0 52 52" aria-hidden="true" focusable="false"><circle cx="26" cy="26" r="23" fill="none" stroke-width="3"/></svg>{ic("up", size=18)}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone", size=18)} Call now</a><a href="{P_CONTACT}">Free claim review</a></div>"""


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


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="house-dark-sky", home=False):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
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
                n["image"] = {"@id": canonical + "#primaryimage"}
                n["inLanguage"] = "en-US"
        nodes.append(n)
    p = PHOTOS[photo]
    pimg = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "contentUrl": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"], "caption": ALT.get(photo, p["title"])}
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY, "primaryImageOfPage": {"@id": canonical + "#primaryimage"},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = None
    for pref in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
        main = next((n["@id"] for n in nodes if n.get("@type") == pref), None)
        if main:
            break
    webpage["mainEntity"] = {"@id": main or DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()]
    if not robots.startswith("noindex"):
        graph += [webpage, pimg]
    graph += nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n'
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Arkansas">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Arkansas">
<meta name="geo.region" content="US-AR">
<meta name="geo.placename" content="Arkansas">
<meta name="theme-color" content="#8f1d24">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@600;700;800;900&family=Red+Hat+Text:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{"home" if home else "inner"}">
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
    # The host serves real files without running the root front controller, so every page is
    # dir/index.php starting with the canonical-host guard (www/http 301, /index.php 301, off-domain noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(f"<li>{x}</li>" for x in parts) + "</ol></nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<ul class="facts">' + "".join(f"<li><small>{e(k)}</small><b>{e(v)}</b></li>" for k, v in facts) + "</ul>"
    c = f'<div class="row"><a class="btn btn-red" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return (f'<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=" data-parallax=\"0.18\"")}</div>'
            f'<div class="wrap phero-in">{crumbs(trail)}<p class="kicker kicker-l">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev", 18)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="sbox sbox-call"><h2 class="sbox-t">Talk it through, free</h2><p>A short call tells you whether appraisal fits your claim, or whether something else would serve you better.</p>'
            f'<a class="sbox-tel" href="tel:{TEL}">{ic("phone", size=18)} {PHONE_INTL}</a><a class="btn btn-white btn-block" href="{P_CONTACT}">Send claim details</a></div>')


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right", size=14)}</a></li>' for n, p in items)
    return f'<div class="sbox"><h2 class="sbox-t">{e(title)}</h2><ul class="sbox-list">{li}</ul></div>'


def band(h="Does the carrier’s number fall short?", p="Send the estimate and your photos. We’ll review it and tell you plainly what we see."):
    return (f'<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div>'
            f'<div class="row"><a class="btn btn-white" href="tel:{TEL}">{ic("phone", size=18)} {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Send the estimate</a></div></div></section>')


LOSSES = ["Hail / roof", "Tornado / wind", "Ice storm / freeze", "Water / burst pipe", "Fire / smoke", "Tree fall", "Hurricane remnant", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", page="/", hlevel=2):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Landlord", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Arkansas"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="lead-t">{e(heading)}</h{hlevel}><p class="lead-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fields">
<div><label for="l-name">Full name *</label><input id="l-name" name="name" autocomplete="name" required></div>
<div><label for="l-phone">Phone *</label><input id="l-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="l-email">Email *</label><input id="l-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="l-role">I am a…</label><select id="l-role" name="role">{_opt(roles)}</select></div>
<div><label for="l-loss">Type of loss</label><select id="l-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="l-city">Property location</label><select id="l-city" name="city">{_opt(cities)}</select></div>
<div><label for="l-amt">Rough amount in dispute</label><select id="l-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="l-car">Insurance company (optional)</label><input id="l-car" name="carrier"></div>
<div class="full"><label for="l-det">What happened, and where does the claim stand?</label><textarea id="l-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="l-web">Website</label><input id="l-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIVACY}">privacy information</a>.</span></label></div>
<div class="full"><button class="btn btn-red btn-block" type="submit">Send my claim details {ic("arrow", size=18)}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hf-t">Get a free claim review</h2><p class="hf-sub">Two minutes. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What kind of damage?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero form)">
<label class="tick"><input type="checkbox" name="consent" value="1" required> <span>Contact me about my claim. <a href="{P_PRIVACY}">Privacy</a></span></label>
<button class="btn btn-red btn-block" type="submit">Request my free review {ic("arrow", size=18)}</button>
<div class="form-msg" role="status"></div>
<p class="hf-note">{ic("shield", size=16)} No obligation · details kept private</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Ozark Plateau & Northwest Arkansas", "Fayetteville · Springdale · Rogers · Bentonville", "ozark-overlook",
     "The state’s busiest hail corridor and the core of the January 2009 ice storm. Fast growth means many young roofs, complex rooflines and discontinued products.",
     ["Large hail", "Ice storms", "Tornadoes"]),
    ("Arkansas River Valley", "Fort Smith · Van Buren · Russellville · Conway", "arkansas-river-valley",
     "A natural storm track between the Ozarks and the Ouachitas. Tornadoes, straight-line winds and the 2019 river flood all left their mark here.",
     ["Tornadoes", "Wind", "River flooding"]),
    ("Central Arkansas", "Little Rock · North Little Rock · Benton · Cabot", "little-rock-skyline",
     "The metro area hit by the March 31, 2023 tornadoes, with historic homes, mid-century ranches and large commercial buildings side by side.",
     ["Tornadoes", "Hail", "Burst pipes"]),
    ("Ouachita Mountains", "Hot Springs · Hot Springs Village · Mena", "hot-springs",
     "Wooded slopes, lakes and steep lots. Tree impacts, flash flooding and access costs shape claims in Garland, Montgomery and Polk counties.",
     ["Tree fall", "Flash flooding", "Ice"]),
    ("The Delta & Crowley’s Ridge", "Jonesboro · Pine Bluff · West Memphis · Helena", "storm-rain",
     "Flat, open farmland where storm systems intensify. Tornadoes and long-track straight-line winds hit homes, churches, shops and grain facilities.",
     ["Tornadoes", "Straight-line wind", "Farm buildings"]),
    ("South Arkansas Timberlands", "Texarkana · El Dorado · Camden · Magnolia", "fallen-oaks",
     "Pine forest country where the December 2000 ice storm and Gulf hurricane remnants brought down thousands of trees onto roofs.",
     ["Ice storms", "Tropical remnants", "Fallen pines"]),
]

SEASONS = [
    ("Winter", "Dec–Feb", "ice", ["Freezing rain & glaze ice", "Burst pipes in hard freezes", "Ice dams on low-slope roofs"], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
    ("Spring", "Mar–May", "storm", ["Tornado outbreaks", "Large hail, especially in the northwest", "Flash flooding"], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
    ("Summer", "Jun–Aug", "sun", ["Straight-line winds & derechos", "Lightning and fire", "Hail in early summer"], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]),
    ("Fall", "Sep–Nov", "wind", ["Gulf hurricane remnants", "A second tornado season", "Dry-season woodland fires"], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]),
]


def service_card(s, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", h=3):
    return (f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-ph">{img(SVC_PHOTO[s["slug"]], sizes=sizes, alt="")}</span>'
            f'<span class="pcard-b"><h{h}>{e(s["name"])}</h{h}><span class="pcard-p">{e(s["short"])}</span><span class="more">Learn more {ic("arrow", size=16)}</span></span></a>')


def tool_card(t, h=3):
    return (f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 360px", alt="")}<span class="tcard-ic">{ic(t["icon"], size=22)}</span></span>'
            f'<span class="tcard-b"><span class="tag">{e(t["kind"])}</span><h{h}>{e(t["name"])}</h{h}><span class="pcard-p">{e(t["short"])}</span></span></a>')


def tool_cta(title, text, href, label, h=3):
    return (f'<a class="tcard tcard-cta rv" href="{href}"><span class="tcard-ic">{ic("arrow", size=22)}</span><h{h}>{e(title)}</h{h}>'
            f'<span class="pcard-p">{e(text)}</span><span class="more">{e(label)} {ic("arrow", size=16)}</span></a>')


def city_card(l, h=3):
    return (f'<a class="ccard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}'
            f'<span class="ccard-b"><h{h}>{e(l["city"])}</h{h}><small>{e(l["county"])} · {e(l["region"])}</small></span></a>')


def post_card(p, h=3):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a>'
            f'<div class="gcard-b"><p class="meta">{nice} · {p["read"]} read</p><h{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h{h}><p>{e(p["summary"])}</p></div></article>')


def home():
    K = BRAND
    services = "".join(service_card(s) for s in SERVICES[:9])
    months = "JFMAMJJASOND"
    seasons = ""
    for name, rng, icon, items, bars in SEASONS:
        strip = "".join(f'<i class="{"on" if b else ""}">{months[i]}</i>' for i, b in enumerate(bars))
        seasons += (f'<div class="season rv"><div class="season-h"><span class="season-ic">{ic(icon, size=22)}</span><div><h3>{name}</h3><small>{rng}</small></div></div>'
                    f'<div class="months" aria-hidden="true">{strip}</div><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>')
    steps = "".join(f'<li class="stack-card" style="--i:{i}"><span class="stack-n">{i + 1:02d}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(PROCESS_STEPS[:6]))
    regions = "".join(
        f'<li class="region"><div class="region-ph">{img(ph, sizes="(max-width:700px) 85vw, 420px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in pr)}</ul></div></li>'
        for n, c, ph, t, pr in REGIONS)
    tools = "".join(tool_card(t) for t in TOOLS) + tool_cta("Prefer a professional check?", "Send the carrier’s estimate and we’ll review it line by line, free.", "#contact", "Send your estimate")
    cities = "".join(city_card(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    home_faqs = [
        (f"What does an {K} do?", f"An {K} values property damage when you and your insurer agree the loss is covered but disagree on the cost. As your named appraiser we inspect, build an independent line-item estimate, work through the differences with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When does it make sense to call an {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and a qualified contractor’s estimate is meaningful, often more than about 10% or a few thousand dollars."),
        ("Is the appraisal award binding?", "Generally yes, on the amount of loss for the items submitted, once two of the three panel members sign. That is why documentation matters before appraisal is demanded."),
        ("What does appraisal cost?", "Each side usually pays its own appraiser and half of the umpire. Fees are agreed in writing before work starts, and the first conversation is free."),
        ("Do you cover my part of the state?", "Yes. We work in all 75 Arkansas counties, with frequent work in Northwest Arkansas, the River Valley, central Arkansas, the Delta and south Arkansas."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("house-dark-sky", lazy=False, alt="", extra=' data-parallax="0.22"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker kicker-l">Independent appraisal · All 75 counties</p>
<h1><span class="h1-a">{K}</span> <span class="h1-b">for covered claims that came up short</span></h1>
<p class="lede">Your insurer agreed the damage is covered, but the check won’t pay for the repair. {K} builds an independent, line-by-line valuation of the loss and takes it through the appraisal process written into your policy.</p>
<div class="row"><a class="btn btn-red" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn btn-ghost-w" href="#services">See our services</a></div>
<ul class="hero-ticks"><li>{ic("check", size=18)}Your named appraiser</li><li>{ic("check", size=18)}Line-item local pricing</li><li>{ic("check", size=18)}Homes, HOAs &amp; businesses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="counts" aria-label="At a glance"><div class="wrap"><ul class="counts-in">
<li><b data-count="75">75</b><span>Arkansas counties served</span></li>
<li><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></li>
<li><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free in-browser claim tools</span></li>
<li><b>2 of 3</b><span>Signatures set a binding award</span></li>
</ul></div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-media rv">
<figure class="fig-a">{img("roofer-tarp", sizes="(max-width:900px) 92vw, 520px")}</figure>
<figure class="fig-b">{img("roof-edge-damage", sizes="(max-width:900px) 50vw, 260px")}</figure>
</div>
<div class="duo-copy rv">
<p class="kicker">Covered is not the same as paid</p>
<h2>Why owners bring in an {K}</h2>
<p>Most underpaid claims in Arkansas aren’t denied. They’re short: a roof slope priced as a repair, a hallway of flooring left out, drip edge and ridge vent missing, depreciation taken on items that shouldn’t lose that much value. An {K} is there to close the gap between what the carrier approved and what the repair really costs.</p>
<ul class="ticks">
<li>{ic("check", size=20)}<div><b>An independent scope</b><span>We measure and document the damage ourselves before looking at anyone else’s estimate.</span></div></li>
<li>{ic("check", size=20)}<div><b>Numbers built to hold up</b><span>Each line is supported by photos, measurements and current local pricing an umpire can follow.</span></div></li>
<li>{ic("check", size=20)}<div><b>Straight answers</b><span>If your dispute is really about coverage, or the gap is too small, we tell you on the first call.</span></div></li>
</ul>
<p><a class="link" href="{P_ABOUT}">How the company works {ic("arrow", size=16)}</a></p>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Appraisal &amp; estimating services</p><h2>What an {K} handles</h2><p>From one disputed roof to a multi-building HOA claim, every service is aimed at a valuation of your loss that stands up on its own.</p></div>
<div class="grid3" data-stagger>{services}</div>
<p class="center"><a class="btn btn-line" href="{SVC_BASE}">All {len(SERVICES)} appraisal services {ic("arrow", size=18)}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Arkansas claim calendar</p><h2>Four seasons of property damage</h2><p>Arkansas doesn’t have one storm season. It has four, and each leaves a different kind of claim behind. An {K} prices each one with that history in mind.</p></div>
<div class="seasons" data-stagger>{seasons}</div>
</div></section>

<section class="sec ink" id="process"><div class="wrap stack-wrap">
<div class="stack-intro rv"><p class="kicker kicker-l">How appraisal works</p><h2>From stuck claim to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how {K} takes a file from the first call to the award.</p><p><a class="btn btn-white" href="{P_PROCESS}">Read the full process guide {ic("arrow", size=18)}</a></p></div>
<ol class="stack">{steps}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h split-h rv"><div><p class="kicker">Regional knowledge</p><h2>Six regions, six kinds of claims</h2><p>Hail in Bentonville is not ice in Texarkana. An {K} has to know how each part of the state’s weather shows up on a roof, and in an estimate.</p></div>
<div class="rail-nav"><button type="button" class="rail-btn" data-rail="-1" aria-label="Previous region">{ic("left", size=20)}</button><button type="button" class="rail-btn" data-rail="1" aria-label="Next region">{ic("right", size=20)}</button></div></div>
<ul class="rail" tabindex="0" aria-label="Arkansas regions">{regions}</ul>
</div></section>

<section class="sec red" id="gap-check"><div class="wrap duo">
<div class="duo-copy rv"><p class="kicker kicker-l">Quick gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. If the difference is large, a conversation with an {K} makes sense. If it’s small, a documented supplement request is often faster and cheaper.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees and shows a break-even point.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Free &amp; private</p><h2>Free claim tools from an {K}</h2><p>Seven calculators and planners that run entirely in your browser. Nothing you type is stored or sent.</p></div>
<div class="grid4" data-stagger>{tools}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Statewide service</p><h2>{K} locations</h2><p>We cover every county. These twelve communities are where {K} works on claims most often.</p></div>
<div class="cgrid" data-stagger>{cities}</div>
<p class="center"><a class="link" href="{LOC_BASE}">All Arkansas locations {ic("arrow", size=16)}</a></p>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Right tool for the job</p><h2>Appraisal fits some disputes, not all</h2><p>Picking the right help first saves time and fees. {K} will point you elsewhere when appraisal isn’t the answer.</p></div>
<div class="fit" data-stagger>
<div class="fit-col yes rv"><h3>{ic("check", size=22)} Good fit for appraisal</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair vs. replace on roofs or floors</li><li>Matching and discontinued materials</li><li>Missing trades, code items or overhead and profit</li><li>Depreciation that looks too heavy</li></ul></div>
<div class="fit-col no rv"><h3>{ic("x", size=22)} Usually not a fit</h3><ul><li>The claim was denied outright</li><li>The question is whether a cause is covered</li><li>Bad-faith or statutory penalty claims</li><li>Gaps too small to justify fees</li><li>Deadlines that need an attorney now</li></ul></div>
</div>
<div class="table-wrap rv"><table class="compare"><caption class="sr-only">Comparing an appraiser, a public adjuster and an attorney</caption><thead><tr><th scope="col">Question</th><th scope="col" class="hl">{K}</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Handle and negotiate the claim</td><td>Legal disputes and litigation</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>From first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Typical result</th><td class="hl">Two-signature award</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
</tbody></table></div>
</div></section>

<section class="sec"><div class="wrap duo top">
<div class="duo-copy rv"><p class="kicker">Questions</p><h2>Questions people ask an {K}</h2><p>Plain answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="row"><a class="btn btn-red" href="{P_FAQ}">All FAQs {ic("arrow", size=18)}</a><a class="btn btn-line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Guides</p><h2>Read before you demand appraisal</h2><p>Practical guides from {K} on Arkansas policy language, documentation and claim strategy.</p></div>
<div class="grid3" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All appraisal guides {ic("arrow", size=16)}</a></p>
</div></section>

<section class="pcta">{img("storm-sky", "pcta-bg", alt="", extra=' data-parallax="0.25"')}<div class="wrap pcta-in rv"><p class="kicker kicker-l">Before you sign off</p><h2>Check the numbers before you accept them</h2><p>A short review now can keep you from settling for less than the repair costs.</p><div class="row"><a class="btn btn-white" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn btn-ghost-w" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="contact-copy rv"><p class="kicker">Start with a conversation</p><h2>Talk with an {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure and no obligation.</p>
<ul class="lines"><li>{ic("phone", size=20)}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail", size=20)}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock", size=20)}<div><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin", size=20)}<div><small>Service area</small><b>All 75 Arkansas counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Arkansas Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, tornado, ice, water and fire claims.",
                        body, schema, photo="house-dark-sky", home=True), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        idx = SERVICES.index(s)
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(service_card(r, sizes="(max-width:700px) 100vw, 260px") for r in rel)
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap two"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="rel3">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All Arkansas locations", LOC_BASE)])}</aside></div>
{band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Arkansas"}, "url": DOMAIN + path}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(service_card(s, h=2) for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Arkansas Property Claims",
                     f"Eleven services built around one job: an accurate, defensible valuation of your loss. Start with an estimate review, or bring {BRAND} in once appraisal has been demanded.", "roofer-tarp") + f"""
<section class="sec"><div class="wrap"><div class="grid3" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap duo top"><div class="duo-copy rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that difference is worth. Many disputes close at that stage.</p><p><a class="btn btn-red" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow", size=18)}</a></p></div>
<div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, condos, rentals, apartments, retail, offices, warehouses, churches and HOA communities."), ("Is hail all you do?", "No. We handle tornado and wind, ice storm and freeze, water, fire, tree fall and hurricane-remnant claims as well.")])}</div></div></section>
{band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services | Arkansas Claims",
                             "Insurance appraisal services across Arkansas: appraisal clause representation, estimate review, hail, tornado, ice, water, fire and umpire work.",
                             body, schema, photo="roofer-tarp"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = "".join(city_card(LOC_BY[n]) for n in l["near"][:3])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, Arkansas", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap two"><article class="prose">
<div class="callout"><p class="callout-t">Common claim risks in {e(l["city"])}</p><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="rel3">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Arkansas locations", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{band(f"Disputed claim in {l['city']}?", "Send the estimate and photos. We’ll tell you what we see and whether appraisal fits.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Arkansas", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Arkansas"}}, "url": DOMAIN + path}]
        title = f"{l['city']} Insurance Appraiser | Claim Disputes, AR"
        if len(title) > 58:
            title = f"{l['city']} Insurance Appraiser | Arkansas"
        desc = f"Insurance appraiser for {l['city']} and {l['county']}: independent appraisal and estimate review for underpaid storm, water and fire claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {l['city']}, Arkansas: independent appraisal and estimate review for underpaid storm and fire claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cities = "".join(city_card(l, h=2) for l in LOCATIONS)
    reg = "".join(f'<div class="regcard rv"><div class="regcard-ph">{img(ph, sizes="(max-width:700px) 100vw, 380px", alt="")}</div><div class="regcard-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div></div>' for n, c, ph, t, _p in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 75 Arkansas Counties",
                     f"{BRAND} works statewide, from Benton County in the northwest to Chicot County in the southeast. These local pages cover the communities where we handle claims most often.", "ozark-overlook") + f"""
<section class="sec"><div class="wrap"><div class="cgrid" data-stagger>{cities}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-h rv"><p class="kicker">Regions</p><h2>How claims differ across Arkansas</h2><p>The same policy language plays out differently on a Bentonville rooftop, a Delta church and a Hot Springs lake house.</p></div><div class="grid3" data-stagger>{reg}</div></div></section>
{band("Don’t see your town?", "We cover every Arkansas county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Arkansas Insurance Appraiser Locations | 75 Counties",
                             "Insurance appraisal in all 75 Arkansas counties, including Little Rock, Fort Smith, Fayetteville, Bentonville, Jonesboro, Conway and Texarkana.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="ozark-overlook"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        idx = TOOLS.index(t)
        others = "".join(tool_card(TOOLS[(idx + k) % len(TOOLS)]) for k in (1, 2, 3))
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="fineprint">For planning only. Results depend on the figures you enter and your policy’s terms. They are illustrative, not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap two"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="rel3">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All claim tools", items, path)}</aside></div>
{band("Want a professional to check the math?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    cards = "".join(tool_card(t, h=2) for t in TOOLS) + tool_cta("Want a second set of eyes?", "Our appraisers can check the carrier’s math for you. The first conversation is free.", P_CONTACT, "Contact an appraiser", h=2)
    body = page_hero(trail, "Free & private", "Free Property Claim Tools for Arkansas Owners",
                     "Seven calculators and planners drawn from real appraisal work. Check the carrier’s math, plan your deadlines and decide on next steps. No sign-up, and nothing you type is stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="grid4" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap duo top"><div class="duo-copy rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="steps-ol"><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a> so no deadline slips.</li><li>Check roof quantities with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}wind-hail-percentage-deductible/">percentage deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV vs. ACV</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Property Claim Tools & Calculators | Arkansas",
                              "Free property claim tools: claim gap and fee estimator, RCV vs. ACV, roof squares, percentage deductible, deadline calendar and ice load calculator.",
                              body, schema, photo="calculator"), 0.9)


# ---------------------------------------------------------------- resources
LEARN = [("Appraisal process", P_PROCESS), ("FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Appraisal guides", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process, Explained Step by Step",
                     "Eight stages from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "planner",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap two"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Arkansas", "description": "The stages of a property insurance appraisal, from the disagreement to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process Explained | 8 Steps",
                         "The insurance appraisal process explained for Arkansas policyholders: the written demand, naming appraisers, the umpire and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="planner"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("FAQ", path)]
    jump = "".join(f'<a href="#t-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="t-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal FAQ for Arkansas Property Owners",
                     "Straight answers to the questions we hear most, grouped by topic: the basics, costs, deadlines, Arkansas specifics and working with us.", "consultation") + f"""
<div class="wrap two"><article class="prose"><nav class="jump" aria-label="FAQ topics">{jump}</nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{band("Didn’t see your question?", "Call or email and we’ll talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Arkansas Policyholders",
                         "Insurance appraisal FAQ for Arkansas: how appraisal works, what it costs, deadlines, ARRUA, the Insurance Department and when appraisal doesn’t fit.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="consultation"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"term\"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Insurance Claim Glossary: Plain-English Terms",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined simply. Type to filter.", "paperwork", cta=False) + f"""
<div class="wrap two"><article class="prose"><div class="gfilter"><label for="gloss-q">Search the glossary</label><input id="gloss-q" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="note" data-gcount>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More",
                         "Insurance claim glossary in plain English: actual cash value, replacement cost, holdback, appraisal award, umpire, ARRUA, ice dams and 40+ more terms.",
                         body, [crumbs_schema(trail), dts], photo="paperwork"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        idx = POSTS.index(p)
        others = "".join(post_card(POSTS[(idx + k) % len(POSTS)]) for k in (1, 2, 3))
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap two"><article class="prose">{p["body"]}<p class="fineprint">General information, not legal advice. Policy wording and Arkansas law control.</p><h2>Keep reading</h2><div class="rel3">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(post_card(p, h=2) for p in POSTS)
    body = page_hero(trail, "Guides", "Insurance Appraisal Guides for Arkansas Owners",
                     "Practical reading on Arkansas policy language, documentation and claim strategy, from the appraisal clause to ice storms and river floods.", "debris-inspector", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="grid3" data-stagger>{cards}</div></div></section>{band()}"""
    write(path, document(path, "Insurance Appraisal Guides | Arkansas Claims",
                         "Insurance appraisal guides for Arkansas owners: the appraisal clause, labor depreciation, ice storms, tornado claims, hail photos and flood vs. wind.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="debris-inspector"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("Company", path)]
    body = page_hero(trail, "The company", f"About {BRAND}",
                     "An appraisal and estimating practice built on one idea: a covered property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "roof-crew") + f"""
<div class="wrap two"><article class="prose">
<figure class="wide-fig">{img("meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Many claim professionals do a little of everything. {BRAND} works on one question, the amount of loss, and builds its process, tools and documentation standards around answering it well. That focus lets us serve as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable, not inflated.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a different approach, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA and POA boards, property managers, churches, business owners, contractors and attorneys across Arkansas. On any claim we serve in one role only, and we disclose prior working relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes, because no honest appraiser can.</p>
<h2>Statewide by design</h2>
<p>Arkansas weather changes a lot from the Ozark Plateau to the Delta to the timberlands of the south. Working in all 75 counties means we see the full range of losses the state produces, from hail in Benton County to ice in Miller County to tornadoes across the Arkansas River Valley, and we price each with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Locations", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", P_PROCESS)])}</aside></div>{band()}"""
    write(path, document(path, f"About the Company | {BRAND}",
                         f"{BRAND} is an independent appraisal and estimating practice focused on the amount of loss on disputed Arkansas property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="roof-crew"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact an Arkansas Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="contact-copy rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone", size=20)}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail", size=20)}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock", size=20)}<div><small>Hours</small><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin", size=20)}<div><small>Service area</small><b>Statewide, all 75 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks-s"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact an Arkansas Insurance Appraiser | Free Review",
                         "Contact an Arkansas insurance appraiser for a free review of a disputed property claim. Call or text (844) 537-1427 or send claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td>'
        f'<td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td>{e(v["source"].title())}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">View source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Information", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to share, such as your name, phone, email, property location and claim details. Our server also records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To reply to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this page will say so.</p>
<h2>Text messages</h2><p>If you agree to texts, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To access, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                    "How we collect, use and protect the information you share with us.", "Privacy Information | " + BRAND,
                    f"Privacy information for {BRAND}: what we collect when you contact us, how we use it and how our claim tools keep data private."),
        P_TERMS: ("Website Use Terms", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in Arkansas.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or sending a form doesn’t create an appraiser–client relationship. That begins only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Arkansas attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give illustrative planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photos are used under the licenses listed on our <a href="{P_CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Arkansas.</p>""",
                  "The terms that apply when you use this website and its tools.", "Website Use Terms | " + BRAND,
                  f"Website use terms for {BRAND}: no client relationship or legal advice from site content, how the tools work and governing law."),
        P_DISC: ("Appraisal Disclaimer", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t provide legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative, not results for any client. No appraiser can guarantee an award.</p>
<h2>Legal references</h2><p>References to Arkansas statutes, court decisions, the Arkansas Insurance Department or the Arkansas Rural Risk Underwriting Association are general and may be out of date. Verify current law with official sources and a licensed Arkansas attorney.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, replacement-cost recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an attorney promptly.</p>
<h2>Weather events</h2><p>Storm references are drawn from widely reported public information and are included for context only.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They do not show our clients’ properties.</p>""",
                 "Important limits on the information published on this website.", "Appraisal Disclaimer | " + BRAND,
                 f"Disclaimer for {BRAND}: general information only, not legal advice, no guaranteed results and limits on legal citations."),
        P_CREDITS: ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work such as photos by U.S. government agencies. Photos were found through the Openverse search engine. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Source</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""",
                     "Sources and licenses for every photograph used on this site.", "Photo Credits & Licenses | " + BRAND,
                     f"Photo credits for {BRAND}: every image used on the site with its CC0 or public-domain license, creator and original source link."),
    }
    for path, (title, content, lede, seo, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "snow-house" if path == P_CREDITS else "church", cta=False) + f'<div class="wrap two"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, seo, desc, body, [crumbs_schema(trail)], photo="church"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site navigation", path)]
    groups = [
        ("Main pages", [("Home", "/"), ("Company", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(f"{l['city']}, AR", loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy information", P_PRIVACY), ("Website use terms", P_TERMS), ("Appraisal disclaimer", P_DISC), ("Photo credits", P_CREDITS)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Navigation", f"Every page on {BRAND}, in one place.", "ozark-cabin", cta=False) + f'<section class="sec"><div class="wrap"><div class="grid3" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Navigation | {BRAND}", f"Every page on {BRAND} in one list: appraisal services, Arkansas locations, free claim tools, guides and site information.", body, [crumbs_schema(trail)], photo="ozark-cabin"), 0.3)

    body = f"""<section class="phero nf"><div class="phero-bg">{img("snapped-tree", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-l">Error 404</p><h1>This page came down in the storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="row"><a class="btn btn-white" href="/">Home</a><a class="btn btn-ghost-w" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-w" href="{TOOL_BASE}">Free tools</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found.", body, robots="noindex,follow", photo="snapped-tree"), sitemap=False)


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
// Arkansas Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$aia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$aia_real  = 'arkansasinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$aia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$aia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://arkansasinsuranceappraiser.com - only on the real domain.
if ($aia_host === 'www.' . $aia_real || ($aia_host === $aia_real && $aia_proto === 'http')) {
    $aia_uri = preg_replace('#^((?:[^?]*/)?)index\.php(?=$|\?)#', '$1', $aia_uri);
    header('Location: https://' . $aia_real . $aia_uri, true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($aia_uri, '?'), $aia_m)) {
    $aia_q = strpos($aia_uri, '?') !== false ? substr($aia_uri, strpos($aia_uri, '?')) : '';
    header('Location: ' . $aia_m[1] . $aia_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($aia_host !== $aia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Arkansas Insurance Appraiser - front controller for the static build.
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
