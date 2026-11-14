#!/usr/bin/env python3
"""Static site generator for nebraskainsuranceappraiser.com.

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

BRAND = "Nebraska Insurance Appraiser"
HOST = "nebraskainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114a"
FAV = "1"

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM output.
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraisal-services-nebraska/"
LOC_BASE = "/nebraska-cities/"
TOOL_BASE = "/claim-tools-nebraska/"
POST_BASE = "/nebraska-claim-guides/"
PROCESS = "/nebraska-appraisal-process/"
FAQ_P = "/questions-about-appraisal/"
GLOSS = "/appraisal-word-list/"
ABOUT = "/about-our-appraisers/"
CONTACT = "/free-claim-review/"
PRIVACY = "/our-privacy-policy/"
TERMS = "/website-terms-of-use/"
DISCL = "/appraisal-disclaimers/"
SITEMAP = "/site-contents/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, NE"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-supercell": "Shelf cloud of a supercell thunderstorm rolling over flat Nebraska farmland",
    "storm-anvil": "Towering thunderstorm lit pink at sunset above open grassland",
    "tornado-plains": "Tornado touching down under a dark storm over open plains",
    "omaha-skyline": "Downtown Omaha office towers and church spires under a blue sky",
    "omaha-dusk": "Omaha skyline at dusk with lit towers behind bare trees",
    "lincoln-capitol": "Nebraska State Capitol tower in Lincoln framed by trees",
    "lincoln-haymarket": "Brick warehouse buildings along a street in Lincoln’s Haymarket district",
    "scotts-bluff": "View north from Scotts Bluff National Monument over the North Platte valley",
    "chimney-rock": "Chimney Rock rising above the plains of western Nebraska",
    "grand-island": "Red brick buildings at a downtown intersection in Grand Island",
    "north-platte": "Golden Spike Tower beside the rail yard in North Platte",
    "fremont-main": "Shops along Main Street in downtown Fremont",
    "hastings-homes": "Large older homes with porches on a residential street in Hastings",
    "hastings-park": "Lagoon and lawn in Heartwell Park in Hastings",
    "norfolk-theatre": "Historic brick Grand Theatre building in downtown Norfolk",
    "columbus-hall": "City Hall building in Columbus on a sunny day",
    "bellevue-church": "White historic church with a tall steeple in Bellevue",
    "hailstones": "Hand holding several large hailstones after a storm",
    "flood-aerial": "Aerial view of river floodwater covering farmland and roads",
    "flood-road": "Floodwater covering a rural road beside power lines",
    "farm-silos": "Farmstead with concrete silos and outbuildings",
    "grain-bin-wreck": "Concrete pad and scattered steel left after a grain bin was destroyed by wind",
    "barn-storm": "Old wooden barn under gray storm clouds",
    "barn-sunset": "Weathered barn beside a bare tree at sunset",
    "grain-bins": "Two steel grain bins and farm sheds on the prairie",
    "roof-tarp": "Roofer on a lift tarping a storm-damaged roof",
    "shingles": "Close-up of overlapping dark roof shingles",
    "icicles": "Long icicles hanging from a roof edge beside a brick wall",
    "snowy-home": "Two-story home with snow-covered shrubs after a winter storm",
    "craftsman-home": "Craftsman-style home with a front porch and steps",
    "family-home": "Suburban two-story home with gables and a front lawn",
    "consultation": "Two women talking across a table in a bright office",
    "review-meeting": "Two professionals reviewing figures on a laptop together",
    "calculator-pen": "Calculator, pen and sticky note on a desk",
    "calculator-laptop": "Calculator resting on printed charts next to a laptop",
    "clipboard": "Blank clipboard on a wooden desk between two small plants",
    "condo-building": "Multi-story condominium building with balconies beside a pond",
    "glass-office": "Glass and steel atrium of a modern commercial building",
    "tornado-home": "Foundation and debris left after a tornado destroyed a home",
    "tornado-street": "Downed power poles and damaged trees on a street after a tornado",
    "ceiling-water": "Commercial interior with missing ceiling tiles and buckets catching a leak",
    "contractor-belt": "Contractor with a tool belt working on a wall",
    "platte-woods": "Trees reflected in still water along the Platte River in autumn",
    "house-fire": "House engulfed in flames at night",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy is True else (' fetchpriority="high"' if lazy is False else "")
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consultation", "homeowner-claim-appraiser": "craftsman-home",
    "commercial-hoa-claim-appraisal": "condo-building", "hail-roof-appraisal": "hailstones",
    "tornado-straight-line-wind-appraisal": "tornado-street", "farm-ranch-outbuilding-appraisal": "grain-bin-wreck",
    "water-damage-claim-appraisal": "ceiling-water", "fire-smoke-damage-appraisal": "house-fire",
    "ice-dam-frozen-pipe-appraisal": "icicles", "carrier-estimate-review": "calculator-laptop",
    "umpire-selection-services": "review-meeting",
}
TOOL_PHOTO = {
    "award-gap-fee-estimator": "calculator-pen", "acv-holdback-calculator": "calculator-laptop",
    "roof-square-pitch-converter": "shingles", "hail-deductible-calculator": "hailstones",
    "claim-calendar-builder": "clipboard", "appraisal-readiness-check": "review-meeting",
    "slope-repair-gap-calculator": "roof-tarp",
}
POST_PHOTO = {
    "nebraska-hail-claim-documentation": "roof-tarp", "percentage-deductible-explained": "calculator-pen",
    "appraiser-adjuster-or-attorney": "consultation", "farm-building-claims-after-storms": "grain-bins",
    "when-appraisal-is-the-wrong-move": "clipboard", "winter-water-damage-claims": "snowy-home",
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
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h12"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark():
    """Brand mark: a roof line over a level ledger rule, in navy, gold and silver."""
    return ('<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="9" fill="#002A86"/>'
            '<path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="10" y="30" width="28" height="5" rx="1.2" fill="#FFCC00"/>'
            '<rect x="10" y="37.5" width="17" height="3" rx="1" fill="#C8C8C8"/></svg>')


def brand(where):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "NE", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NE", "availableLanguage": "en"}],
        "slogan": "An independent number for disputed property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Nebraska.",
        "areaServed": [{"@type": "State", "name": "Nebraska"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services in Nebraska", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Wind damage", "Farm building claims", "Property claim valuation"],
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
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Nebraska cities", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All claim tools", TOOL_BASE)),
        ("Resources", [("Appraisal process guide", PROCESS), ("Questions about appraisal", FAQ_P), ("Appraisal word list", GLOSS), ("Nebraska claim guides", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        cols = " cols" if len(links) > 7 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{cols}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top" href="{ABOUT}">About</a></li><li><a class="top" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="strip"><div class="wrap"><span>Independent appraisal · All 93 Nebraska counties</span><span class="strip-r"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></span></div></div>
<div class="bar"><div class="wrap">
{brand("h")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn gold head-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div></div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("d")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn gold" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn line-light" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS[:6])
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap"><h2>Is the carrier’s number short? Get a second set of eyes on it.</h2><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn line-light" href="{CONTACT}">Send your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("f")}
<p>Independent appraisal, estimate review and umpire services for property owners with disputed claims, from the Missouri River bluffs to the Panhandle.</p>
<p class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm CT · Statewide</span></p></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Cities</h3><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}<li><a href="{TOOL_BASE}">All tools</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="{ABOUT}">About</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Word list</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><span>© {date.today().year} {BRAND}. All rights reserved.</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCL}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul>
<p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general and educational; your policy controls. Results depend on the facts of each claim and are never guaranteed.</p></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<nav class="callbar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")}<span>Call now</span></a><a href="{CONTACT}">{ic("doc")}<span>Free review</span></a></nav>"""


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


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-supercell", page_type="WebPage", trail=None):
    canonical = DOMAIN + ("/" if path == "/" else path)
    trail = trail or [("Home", "/")]
    nodes = [crumbs_schema(trail)] + list(schema or [])
    crumb_id = canonical + "#breadcrumb"
    for n in nodes:
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = crumb_id
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        if t in ("Service", "WebApplication", "HowTo", "DefinedTermSet"):
            n.setdefault("provider" if t in ("Service", "WebApplication") else "publisher", {"@id": DOMAIN + "/#business"})
    pimg = PHOTOS[photo]
    image = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "contentUrl": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": ALT[photo]}
    main_id = DOMAIN + "/#business"
    for pref in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
        hit = [n for n in nodes if n.get("@type") == pref]
        if hit:
            main_id = hit[0]["@id"]
            break
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": crumb_id}, "primaryImageOfPage": {"@id": canonical + "#primaryimage"}, "mainEntity": {"@id": main_id},
    }
    graph = [org_schema(), site_schema(), webpage, image] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Nebraska">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Nebraska">
<meta name="geo.region" content="US-NE">
<meta name="geo.placename" content="Nebraska">
<meta name="theme-color" content="#002A86">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Schibsted+Grotesk:wght@600;700;800;900&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.replace("no-js","js")</script>
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
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn line-light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero">{img(photo, "phero-img", lazy=False, alt="")}<div class="wrap">{crumbs(trail)}<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box callbox"><h2 class="box-t">Talk it through first</h2><p>A free, no-pressure conversation. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold full" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Have a claim that doesn’t add up?", p="Send the carrier’s estimate. We’ll review it and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn line-light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items, kind):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(kind)}</small><span>{e(n)}</span></a>' for n, p in items) + "</div>"


LOSSES = ["Hail", "Wind / tornado", "Water / frozen pipe", "Fire / smoke", "Farm building", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", uid="f", head_tag="h2"):
    roles = ["Homeowner", "Farm or ranch owner", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Nebraska"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{head_tag} class="form-t">{e(heading)}</{head_tag}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property location</label><select id="{uid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>
<div class="full"><label for="{uid}-det">What happened, and where does the claim stand?</label><textarea id="{uid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form does not create a client relationship. See our <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn navy full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="ticket" action="/api/contact.php" method="post" data-lead novalidate>
<p class="ticket-t">Free claim review</p><p class="sub">Two minutes. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy</a>.</span></label>
<button class="btn navy full" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
<p class="ticket-note">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("omaha", "Omaha Metro", "Omaha · Bellevue · Papillion", ["Hail", "Tornadoes", "Ice dams", "HOA losses"],
     "Douglas and Sarpy counties hold the state’s densest housing, from century-old Midtown homes to new two-story builds with steep, cut-up roofs. Hail is the headline peril, but tornadoes and winter water losses are part of the picture too.",
     "Omaha, Bellevue, Papillion, La Vista, Elkhorn, Gretna", "omaha-dusk"),
    ("lincoln", "Lincoln & the Southeast", "Lincoln · Beatrice · Nebraska City", ["Hail", "Tornadoes", "Rental claims", "Water losses"],
     "Lancaster County mixes older neighborhoods, student rentals and fast-growing subdivisions. The 2004 Hallam tornado and the 2024 storms northeast of Lincoln are reminders that wind damage is not limited to hail season.",
     "Lincoln, Waverly, Hickman, Beatrice, Nebraska City, Seward", "lincoln-haymarket"),
    ("northeast", "Northeast & Elkhorn Valley", "Norfolk · Fremont · Columbus", ["Tornadoes", "Flooding", "Farm buildings", "Snow load"],
     "Northeast Nebraska saw the 2014 Pilger tornadoes and major river flooding in 2019. Claims here often combine homes, farm buildings and questions about what water a policy covers.",
     "Norfolk, Fremont, Columbus, Wayne, South Sioux City, Schuyler", "farm-silos"),
    ("platte", "Platte Valley & Central", "Grand Island · Kearney · Hastings", ["Hail", "Straight-line wind", "Metal roofs", "Grain bins"],
     "The Platte Valley is the heart of the hail belt. Grand Island’s 1980 tornadoes are still remembered, and wide swaths of hail cross Hall, Buffalo and Adams counties most summers.",
     "Grand Island, Kearney, Hastings, York, Lexington, Holdrege", "grain-bins"),
    ("west", "Sandhills & Panhandle", "North Platte · Scottsbluff · Valentine", ["Large hail", "High wind", "Wildfire", "Blizzards"],
     "Out west, storms arrive fast off the High Plains with very large hail and strong winds. Ranch claims involve fencing, outbuildings and long distances, and dry grassland adds wildfire risk.",
     "North Platte, Scottsbluff, Gering, Ogallala, Valentine, Alliance", "chimney-rock"),
]

STORMS = [
    ("1975", "Omaha tornado", "A violent May tornado crossed the city, damaging thousands of homes and businesses."),
    ("1980", "Grand Island “Night of the Twisters”", "Several tornadoes struck Grand Island in one June night, destroying hundreds of homes."),
    ("2004", "Hallam tornado", "A wide, violent tornado devastated the village of Hallam in southern Lancaster County."),
    ("2014", "Pilger twin tornadoes", "Twin tornadoes leveled much of Pilger in northeast Nebraska in June."),
    ("2019", "March bomb cyclone floods", "Rapid snowmelt and rain flooded the Platte, Elkhorn, Loup and Missouri River basins."),
    ("2021", "December derecho", "A rare winter derecho swept the state with hurricane-force gusts."),
    ("2024", "Arbor Day tornadoes", "April tornadoes damaged homes near Elkhorn and Bennington and an industrial area northeast of Lincoln."),
]


def home():
    K = BRAND
    proc_steps = [
        ("Free claim review", "We read the policy, the carrier’s estimate and your photos, then tell you whether appraisal fits."),
        ("Independent inspection", "Our own measurements, photos and a line-item estimate priced for your part of the state."),
        ("Written demand", f"Appraisal is demanded in writing and {K} is named as your appraiser on time."),
        ("Panel work", "We go line by line with the carrier’s appraiser. Most files narrow sharply here."),
        ("Signed award", "Open items go to a neutral umpire. Two of three signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="hstep"><span class="dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(proc_steps))

    feat = SERVICES[3]
    cards = f'<a class="scard feat rv" href="{SVC_BASE}{feat["slug"]}/">{img(SVC_PHOTO[feat["slug"]], "scard-img", sizes="(max-width:760px) 100vw, 50vw", alt="")}<span class="scard-b"><span class="kicker">Most requested</span><h3>{e(feat["name"])}</h3><p>{e(feat["short"])}</p><span class="more">See how we handle hail {ic("arrow")}</span></span></a>'
    for s in [x for x in SERVICES if x is not feat][:8]:
        cards += f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], "scard-img", sizes="(max-width:760px) 100vw, 25vw", alt="")}<span class="scard-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'

    storms = "".join(f'<li class="rv"><b class="yr">{y}</b><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for y, t, d in STORMS)

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}</button>'
        for i, (k, n, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="rpanel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}>{img(ph, "rpanel-img", sizes="(max-width:900px) 100vw, 640px", alt="", lazy=None if i else True)}<div class="rpanel-b"><p class="kicker">{e(sub)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in pr)}</ul><p>{e(t)}</p><p class="small">Communities: {e(c)}</p></div></div>'
        for i, (k, n, sub, pr, t, c, ph) in enumerate(REGIONS))

    cities = "".join(f'<a class="ccard rv" href="{loc_path(l)}">{img(l["photo"], "ccard-img", sizes="(max-width:760px) 50vw, 25vw", alt="")}<span class="ccard-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    tiles = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/">{img(TOOL_PHOTO[t["slug"]], "tcard-img", sizes="(max-width:760px) 100vw, 33vw", alt="")}<span class="tcard-b"><span class="kicker">{e(t["kind"])}</span><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    posts = "".join(f'<a class="gcard rv" href="{POST_BASE}{p["slug"]}/">{img(POST_PHOTO[p["slug"]], "gcard-img", sizes="(max-width:760px) 100vw, 33vw", alt="")}<span class="gcard-b"><span class="kicker">{p["read"]} read</span><h3>{e(p["title"])}</h3><p>{e(p["summary"])}</p></span></a>' for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree on the cost. As your named appraiser we inspect, write an independent estimate, work with the carrier’s appraiser and present open items to a neutral umpire."),
        ("Is this the same as a public adjuster?", "No. A public adjuster presents and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We do not give legal advice or negotiate outside appraisal."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the carrier’s itemized estimate and the gap between it and your contractor’s number is meaningful, usually more than a few thousand dollars."),
        ("Is the award binding?", "Yes, on the amount of loss, once two of the three panel members sign. That is why documentation matters before anyone demands appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before work begins, and the first conversation is free."),
        ("Do you cover my part of the state?", "Yes. We work in all 93 counties, from Omaha and Lincoln to Grand Island, Kearney, North Platte and Scottsbluff."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero-supercell", "hero-img", lazy=False, alt="")}</div>
<div class="wrap hero-grid">
<div class="hero-copy">
<p class="tag light">Independent claim appraisal · All 93 counties</p>
<h1>{K}: an independent number for your disputed claim</h1>
<p class="lede">When the carrier accepts your hail, wind, water or fire claim but the payment won’t cover the repair, {K} builds a line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn line-light" href="#check">Check your gap {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Your named appraiser, not the carrier’s</li><li>{ic("check")}Homes, farms, HOAs &amp; commercial</li><li>{ic("check")}Fees in writing before work starts</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="tally" aria-label="At a glance"><div class="wrap tally-in">
<div><b data-count="93">93</b><span>Nebraska counties served</span></div>
<div><b data-count="11">11</b><span>Appraisal &amp; estimating services</span></div>
<div><b data-count="7">7</b><span>Free claim tools</span></div>
<div><b>2 of 3</b><span>Signatures set the award</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="tag">01 · Start here</p><h2>Three checks a {K} makes before recommending appraisal</h2><p>Appraisal is powerful, but only for the right kind of dispute. These three questions decide whether it fits your claim.</p></div>
<ol class="checks3">
<li class="rv"><span class="n">1</span><h3>Is the loss covered?</h3><p>Appraisal values covered damage. If the carrier denied the claim or applied an exclusion, that is a coverage dispute for an attorney, not a panel.</p></li>
<li class="rv"><span class="n">2</span><h3>Do you have the itemized estimate?</h3><p>The carrier’s full line-item estimate shows exactly where the disagreement lies. Without it, nobody can measure the gap.</p></li>
<li class="rv"><span class="n">3</span><h3>Is the gap worth the fees?</h3><p>A {K} costs money, and so does an umpire. On a small gap, a documented supplement may be faster and cheaper.</p></li>
</ol>
<div class="fit">
<div class="fit-yes rv"><h3>{ic("check")}Appraisal usually fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Partial roof approved after hail</li><li>Matching or discontinued materials</li><li>Missing code items, O&amp;P or outbuildings</li></ul></div>
<div class="fit-no rv"><h3>{ic("x")}Appraisal usually doesn’t</h3><ul><li>Outright denials or exclusions</li><li>Bad-faith or legal claims</li><li>Gaps too small to cover fees</li><li>Suit deadlines that are close</li></ul></div>
</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="tag">02 · The process</p><h2>How a {K} moves a stalled claim to a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process. Here is how we take a file from the first call to the award.</p></div>
<ol class="htime" data-htime><span class="htime-fill" aria-hidden="true"></span>{proc}</ol>
<p class="center"><a class="link" href="{PROCESS}">Read the full Nebraska appraisal process guide</a></p>
</div></section>

<section class="sec" id="services"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="tag">03 · Services</p><h2>What {K} does for your claim</h2></div><p>Eleven services built around one job: a valuation of your loss that holds up in front of an umpire. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="sgrid" data-stagger>{cards}</div>
<p class="center"><a class="btn line" href="{SVC_BASE}">All {len(SERVICES)} appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec silver" id="check"><div class="wrap two">
<div class="rv"><p class="tag">04 · Quick math</p><h2>Is your gap big enough for a {K}?</h2><p>Enter the two numbers you already have. If the difference is large, a conversation about appraisal makes sense. If it is small, a supplement request may close it.</p><p>The full <a href="{TOOL_BASE}award-gap-fee-estimator/">award gap and fee estimator</a> subtracts appraiser and umpire fees so you can see a realistic net.</p><a class="btn navy" href="{TOOL_BASE}">See all seven free tools {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec navy"><div class="wrap two top">
<div class="rv sticky-col"><p class="tag light">05 · The record</p><h2>Storms that shaped Nebraska property claims</h2><p>Every {K} file sits on top of this history. Repeat hail, rare winter derechos and record floods all change how carriers read a claim, and how we answer them.</p><figure class="framed">{img("tornado-home", sizes="(max-width:900px) 100vw, 520px")}</figure></div>
<ol class="record">{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="tag">06 · Statewide</p><h2>Five claim climates, one {K}</h2><p>Ice dams in Omaha, hail in Kearney, tornadoes in the northeast and wildfire in the Panhandle. Each region shows up differently on a roof, and in an estimate.</p></div>
<div class="regions rv" data-regions><div class="rtabs" role="tablist" aria-label="Nebraska regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="tag">07 · Cities</p><h2>{K} in your city</h2></div><p>We serve every county. These are the communities where {K} handles claims most often, each with local storm history and housing notes.</p></div>
<div class="cgrid" data-stagger>{cities}</div>
<p class="center"><a class="link" href="{LOC_BASE}">See every Nebraska city we serve</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="tag">08 · Free tools</p><h2>Seven free calculators from {K}</h2><p>Run the numbers before you pick up the phone. Every tool runs in your browser, and nothing you type is sent or stored.</p></div>
<div class="tgrid" data-stagger>{tiles}</div>
</div></section>

<section class="sec silver"><div class="wrap">
<div class="sec-head rv"><p class="tag">09 · Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. {K} will point you elsewhere when appraisal is not the right tool.</p></div>
<div class="who" data-stagger>
<div class="who-c hl rv"><p class="kicker">Appraiser</p><h3>Values the amount of loss</h3><p>Best once coverage is accepted and the number is disputed. Result: a binding award signed by two of three.</p></div>
<div class="who-c rv"><p class="kicker">Public adjuster</p><h3>Presents the whole claim</h3><p>Best early in a complex claim. Licensed by the state and usually paid a percentage. Result: a negotiated settlement.</p></div>
<div class="who-c rv"><p class="kicker">Attorney</p><h3>Handles legal disputes</h3><p>Best for denials, exclusions, close deadlines or bad-faith concerns. Result: a settlement or judgment.</p></div>
</div>
</div></section>

<section class="sec"><div class="wrap two top">
<div class="rv sticky-col"><p class="tag">10 · FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn navy" href="{FAQ_P}">All questions {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Word list</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head split-head rv"><div><p class="tag">11 · Guides</p><h2>Read this before you demand appraisal</h2></div><p>Practical guides from the {K} team on documentation, deductibles and strategy.</p></div>
<div class="ggrid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All Nebraska claim guides</a></p>
</div></section>

<section class="sec navy" id="contact"><div class="wrap two top">
<div class="rv"><p class="tag light">12 · Contact</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We will review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 93 Nebraska counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", uid="hc", head_tag="h3")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Nebraska Insurance Appraiser offers independent appraisal, estimate review and umpire help for underpaid hail, wind, water and fire claims.",
                        body, [faq_schema(home_faqs)], photo="hero-supercell"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [x for x in SERVICES if x is not s]
        k = SERVICES.index(s)
        rel = [rel[(k + j) % len(rel)] for j in range(3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about this service</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([(r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel], "Service")}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Cities we serve", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All Nebraska cities", LOC_BASE)])}</aside></div>
{cta_strip()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "areaServed": {"@type": "State", "name": "Nebraska"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="lcard rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], "lcard-img", sizes="(max-width:760px) 100vw, 260px", alt="")}<span class="lcard-b"><span class="kicker">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Nebraska",
                     f"From a one-time estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "contractor-belt") + f"""
<section class="sec"><div class="wrap"><div class="lgrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="tag">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn navy" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one step?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial claims?", "Yes. Homes, acreages, farms, HOAs, apartments, churches and commercial buildings."), ("Do you only work on hail?", "No. We handle wind, tornado, water, freeze, fire and other covered perils.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Nebraska",
                             "Nebraska insurance appraisal services: demand representation, estimate review, hail, wind, farm, water, freeze and fire claims plus umpires.",
                             body, [item_list(items)], photo="contractor-belt", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = l["photo"]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="localcard"><div><p class="kicker">Local claim risks</p><ul class="chips">{chips}</ul></div><dl><div><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div><div><dt>Storm history</dt><dd>{e(l["storms"])}</dd></div></dl></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby")}
</article>
<aside class="aside">{call_box()}{list_box("Nebraska cities", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Nebraska"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {l['city']}, NE | Claim Appraisal"
        if len(title) > 58:
            title = f"Insurance Appraiser in {l['city']}, NE"
        desc = l.get("desc") or f"Independent insurance appraiser in {l['city']}, {l['county']}. Appraisal and estimate review for underpaid hail, wind and water claims."
        write(path, document(path, title, desc, body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cities = "".join(f'<a class="ccard rv" href="{loc_path(l)}">{img(l["photo"], "ccard-img", sizes="(max-width:760px) 50vw, 25vw", alt="")}<span class="ccard-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="lcard plain rv">{img(ph, "lcard-img", sizes="(max-width:760px) 100vw, 260px", alt="")}<span class="lcard-b"><span class="kicker">{e(sub)}</span><h2>{e(n)}</h2><p>{e(t)}</p><p class="small">{e(c)}</p></span></div>' for k, n, sub, _p, t, c, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 93 Nebraska Counties",
                     f"{BRAND} works statewide, from the Missouri River bluffs to the Panhandle. These pages cover the cities where we handle claims most often.", "lincoln-capitol") + f"""
<section class="sec"><div class="wrap"><div class="cgrid" data-stagger>{cities}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="tag">Regions</p><h2>How claims differ across Nebraska</h2><p>The same policy language plays out differently in a Dundee foursquare, a Kearney rental and a Sandhills ranch.</p></div><div class="lgrid" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your city?", "We cover every Nebraska county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Nebraska Cities We Serve | Insurance Appraisal",
                             "Insurance appraisal in all 93 Nebraska counties, including Omaha, Lincoln, Grand Island, Kearney, Norfolk, North Platte and Scottsbluff.",
                             body, [item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="lincoln-capitol", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        k = TOOLS.index(t)
        others = [TOOLS[(k + j) % len(TOOLS)] for j in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec toolsec"><div class="wrap">{t["markup"]}
<p class="disclaim">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others], "Tool")}</article>
<aside class="aside">{call_box()}{list_box("All claim tools", items, path)}</aside></div>
{cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    tiles = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/">{img(TOOL_PHOTO[t["slug"]], "tcard-img", sizes="(max-width:760px) 100vw, 33vw", alt="")}<span class="tcard-b"><span class="kicker">{e(t["kind"])}</span><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Nebraska Owners",
                     "Seven calculators and planners built from real appraisal work. Use them to understand your claim, check the carrier’s math and plan next steps. No sign-up, nothing stored.", "calculator-pen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="tag">Suggested order</p><h2>Using the tools together</h2><ol class="plain-ol"><li>Start with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a> so no deadline slips.</li><li>Check the roof with the <a href="{TOOL_BASE}roof-square-pitch-converter/">roof square and pitch converter</a>.</li><li>If only some slopes were approved, use the <a href="{TOOL_BASE}slope-repair-gap-calculator/">slope repair gap calculator</a>.</li><li>See what you’ll actually receive with the <a href="{TOOL_BASE}hail-deductible-calculator/">hail deductible</a> and <a href="{TOOL_BASE}acv-holdback-calculator/">ACV holdback</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}award-gap-fee-estimator/">award gap and fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-check/">appraisal readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Nebraska",
                              "Free claim tools for Nebraska owners: award gap, ACV holdback, roof pitch, hail deductible, slope gap, claim calendar and a readiness check.",
                              body, [item_list(items)], photo="calculator-pen", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Appraisal process guide", PROCESS), ("Questions about appraisal", FAQ_P), ("Appraisal word list", GLOSS), ("Nebraska claim guides", POST_BASE)]

    path, trail = PROCESS, [("Home", "/"), ("Appraisal process", PROCESS)]
    body = page_hero(trail, "Process guide", "The Nebraska Insurance Appraisal Process, Step by Step",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", "clipboard",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Nebraska", "description": "The seven stages of a property insurance appraisal, from written demand to signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": DOMAIN + path + "#main"} for i, (n, t) in enumerate(STEPS)]}
    write(path, document(path, "Nebraska Insurance Appraisal Process | 7 Steps",
                         "A step-by-step guide to the Nebraska insurance appraisal process: the written demand, appraisers, umpire, negotiation and the binding award.",
                         body, [howto], photo="clipboard", trail=trail), 0.8)

    path, trail = FAQ_P, [("Home", "/"), ("Questions about appraisal", FAQ_P)]
    toc = "".join(f'<a href="#q-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Questions About Insurance Appraisal in Nebraska",
                     "Plain answers grouped by topic: the basics, costs, timing, Nebraska specifics and working with us.", "consultation") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="FAQ topics">{toc}</nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Nebraska Claim Questions",
                         "Answers to common Nebraska insurance appraisal questions, grouped by topic: basics, costs, timing, state specifics and working with us.",
                         body, [faq_schema(allq)], photo="consultation", trail=trail), 0.8)

    path, trail = GLOSS, [("Home", "/"), ("Appraisal word list", GLOSS)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gterm"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim Word List: Appraisal Terms Defined",
                     f"{len(GLOSSARY)} terms you’ll see in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "calculator-laptop", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the word list</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="small" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim and appraisal word list", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Word List | Appraisal Terms Defined",
                         "A searchable word list of insurance claim and appraisal terms, from actual cash value and holdback to umpire and wind/hail deductible.",
                         body, [dts], photo="calculator-laptop", trail=trail), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        k = POSTS.index(p)
        others = [POSTS[(k + j) % len(POSTS)] for j in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([(o["title"], f'{POST_BASE}{o["slug"]}/') for o in others], "Guide")}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], og_type="article", photo=ph, trail=trail), 0.7)

    path, trail = POST_BASE, [("Home", "/"), ("Guides", POST_BASE)]
    cards = "".join(f'<a class="gcard rv" href="{POST_BASE}{p["slug"]}/">{img(POST_PHOTO[p["slug"]], "gcard-img", sizes="(max-width:760px) 100vw, 33vw", alt="")}<span class="gcard-b"><span class="kicker">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</span><h2>{e(p["title"])}</h2><p>{e(p["summary"])}</p></span></a>' for p in POSTS)
    body = page_hero(trail, "Guides", "Nebraska Property Claim Guides",
                     "Practical guides on documentation, deductibles, farm buildings, winter losses and claim strategy, written by people who work appraisal panels.", "barn-storm", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Nebraska Property Claim Guides | Appraisal Tips",
                         "Guides for Nebraska property owners on hail documentation, percentage deductibles, farm buildings, winter water claims and appraisal strategy.",
                         body, [item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="barn-storm", page_type="CollectionPage", trail=trail), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path, trail = ABOUT, [("Home", "/"), ("About", ABOUT)]
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We are estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "review-meeting") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("roof-tarp", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Many claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You will understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, acreage owners, farmers and ranchers, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and do not give legal advice. We are not public adjusters and do not negotiate claims outside the appraisal process. We do not guarantee outcomes; no honest appraiser can.</p>
<h2>Statewide on purpose</h2>
<p>Nebraska stretches more than 400 miles from the Missouri River to the Panhandle. Working all 93 counties means we see every kind of loss the state produces, from ice dams in Omaha and hail in Kearney to tornadoes in the northeast and grass fires out west, and we price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>{cta_strip()}"""
    write(path, document(path, f"About Us | {BRAND}",
                         "Nebraska Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [], photo="review-meeting", page_type="AboutPage", trail=trail), 0.7)

    path, trail = CONTACT, [("Home", "/"), ("Free claim review", CONTACT)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND} for a Free Claim Review",
                     "Call, text, email or send your claim details below. The first conversation is free, and we will tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec navy"><div class="wrap two top">
<div class="rv"><p class="tag light">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm CT</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>Statewide, all 93 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}Declarations page</li><li>{ic("check")}The carrier’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the carrier</li><li>{ic("check")}Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, uid="c", head_tag="h2")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | Free Claim Review",
                         "Request a free review of your disputed Nebraska property claim. Call or text (844) 537-1427 or send your claim details using our form.",
                         body, [], photo="consultation", page_type="ContactPage", trail=trail), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "How we collect, use and protect the information you share with us.",
                  "Read the Nebraska Insurance Appraiser privacy policy: what we collect through forms and calls, how we use it and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web server also records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working properly.</li></ul>
<p>We do not sell your personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter are not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site does not use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the information you have given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "The terms that apply when you use this website and its tools.",
                "The terms of use for the Nebraska Insurance Appraiser website, its free claim tools and content, including limits on reliance and liability.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Nebraska.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form does not create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Nebraska attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators provide planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photographs</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free images in the public domain or dedicated to it, used for illustration only.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we are not liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Nebraska.</p>"""),
        DISCL: ("Disclaimer", "Important limits on the information published on this website.",
                "Important limits on the Nebraska Insurance Appraiser website: general information only, no legal advice and no guarantee of any claim result.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we do not give legal advice and we do not act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a Nebraska attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are royalty-free public-domain images used for illustration. They do not show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to statutes, agencies and weather events are for context only. Verify current law and facts with official sources such as the Nebraska Department of Insurance.</p>"""),
    }
    for path, (title, lede, desc, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "glass-office", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", desc, body, [], photo="glass-office", trail=trail), 0.3)


def sitemap_pages():
    path, trail = SITEMAP, [("Home", "/"), ("Site map", SITEMAP)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Free claim review", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal process guide", PROCESS), ("Questions about appraisal", FAQ_P), ("Appraisal word list", GLOSS), ("Guides", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCL)]),
    ]
    cols = "".join(f'<div class="smap rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on the {BRAND} website, grouped by section.", "glass-office", cta=False) + f'<section class="sec"><div class="wrap"><div class="smap-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", "Browse every page on Nebraska Insurance Appraiser: appraisal services, Nebraska cities, free claim tools, guides and legal pages.", body, [], photo="glass-office", trail=trail), 0.3)

    body = f"""<section class="phero err">{img("tornado-street", "phero-img", lazy=False, alt="")}<div class="wrap"><p class="tag light">Error 404</p><h1>This page didn’t make it through the storm</h1><p class="lede">The page you were looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn gold" href="/">Home</a><a class="btn line-light" href="{SVC_BASE}">Services</a><a class="btn line-light" href="{TOOL_BASE}">Free tools</a><a class="btn line-light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "That page could not be found on Nebraska Insurance Appraiser. Use the links here to reach our services, free claim tools or contact page.", body, robots="noindex,follow", photo="tornado-street", trail=[("Home", "/"), ("Page not found", "/404.html")]), sitemap=False)


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
    # Search Console verification: exact bytes, no wrapper, no trailing newline.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Nebraska Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nia_real  = 'nebraskainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://nebraskainsuranceappraiser.com - only on the real domain.
if ($nia_host === 'www.' . $nia_real || ($nia_host === $nia_real && $nia_proto === 'http')) {
    header('Location: https://' . $nia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$nia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nia_uri, '?'), $nia_m)) {
    $nia_q = strpos($nia_uri, '?') !== false ? substr($nia_uri, strpos($nia_uri, '?')) : '';
    header('Location: ' . $nia_m[1] . $nia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($nia_host !== $nia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Nebraska Insurance Appraiser - front controller for the static build.
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
