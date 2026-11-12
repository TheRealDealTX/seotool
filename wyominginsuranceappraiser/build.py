#!/usr/bin/env python3
"""Static site generator for wyominginsuranceappraiser.com.

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
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Wyoming Insurance Appraiser"
HOST = "wyominginsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261111b"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = "GTM-WF9LR26Z"

SVC_BASE = "/what-we-appraise/"
LOC_BASE = "/where-we-work/"
TOOL_BASE = "/free-calculators/"
POST_BASE = "/claim-guides/"
P_ABOUT, P_CONTACT = "/about-us/", "/talk-to-us/"
P_PROCESS, P_FAQ, P_GLOSS = "/appraisal-step-by-step/", "/appraisal-answers/", "/claim-terms/"
P_PRIV, P_TERMS, P_DISC, P_CRED, P_MAP = "/privacy-statement/", "/terms-and-conditions/", "/legal-notice/", "/photo-credits/", "/html-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, WY"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-supercell": "Supercell thunderstorm glowing at sunset over open prairie grassland",
    "storm-chase": "Storm researchers watching a dark shelf cloud roll over flat farmland",
    "hail-ground": "Ground covered with large hailstones after a severe hailstorm",
    "tree-snapped": "Large evergreen tree snapped at the trunk and lying across a lawn after a windstorm",
    "cheyenne-depot": "Historic sandstone Union Pacific depot and clock tower in downtown Cheyenne, Wyoming",
    "state-capitol": "Wyoming State Capitol with its gold dome in Cheyenne, framed by trees",
    "casper-downtown": "Downtown Casper, Wyoming street with a classic car and the America Theatre sign",
    "laramie-railyard": "Union Pacific rail yard and footbridge in Laramie, Wyoming under a cloudy sky",
    "jackson-downtown": "Boardwalk and western storefronts in downtown Jackson, Wyoming with mountains behind",
    "cody-downtown": "Main street storefronts in downtown Cody, Wyoming under dramatic clouds",
    "cody-sheridan-ave": "Brick storefronts along Sheridan Avenue in Cody, Wyoming",
    "gillette-avenue": "South Gillette Avenue in Gillette, Wyoming with parked trucks and a bank tower",
    "riverton-theater": "Historic brick Acme Theater building on a main street in Riverton, Wyoming",
    "green-river-island": "Green River flowing past Expedition Island with a sandstone butte in Green River, Wyoming",
    "uinta-wind-turbines": "Wind turbines on a ridge above rangeland in Uinta County, Wyoming",
    "cabin-snow": "Weathered wooden cabin with snow on its roof in a winter forest",
    "porch-collapse": "Porch roof collapsed under heavy snow against a timber building",
    "barns-snow": "Two red barns surrounded by deep snow on a hillside",
    "log-home-snow": "Two-story log home with a snow-covered green metal roof among pines",
    "blizzard-lake": "Blowing snow obscuring a frozen lake and pine trees during a blizzard",
    "metal-roof-shop": "Metal-roofed shop building seen from above beside a row of trees",
    "roofers-gable": "Two roofers working on the peak of a gable roof against a blue sky",
    "roof-tarp-lift": "Workers on a lift repairing a storm-damaged brick gable covered with a blue tarp",
    "shingle-texture": "Close-up of weathered roof shingles in overlapping rows",
    "tornado-plains": "Splintered lumber and debris scattered across a plains farmyard after a tornado",
    "commercial-wind": "Commercial metal building torn apart by violent wind with debris in the lot",
    "fire-damaged-house": "Two-story house with its roof burned through after a fire",
    "wildfire-rawlins": "Large wildfire smoke plume rising over sagebrush hills south of Rawlins, Wyoming",
    "log-home-smoke": "Log home under a hazy smoke-filled sky near a forested mountainside",
    "frozen-pipe": "Downspout frozen solid with ice spilling onto rocks below",
    "mall-water": "Commercial interior with ceiling tiles removed and buckets catching a water leak",
    "team-meeting": "People reviewing paperwork and laptops together around a wooden table",
    "calculator-laptop": "Calculator and printed figures beside an open laptop keyboard",
    "laptop-review": "Professional reviewing documents on a laptop at a desk",
    "financial-calculator": "Close-up of a financial calculator keypad",
    "aframe-house": "A-frame house with a steep roof and landscaped yard in Gillette, Wyoming",
    "inspector-clipboard": "Inspector with a clipboard documenting damage inside a home",
    "rawlins-ferris": "Victorian Ferris Mansion with turret and porch in Rawlins, Wyoming",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "name-your-appraiser": "team-meeting", "home-insurance-dispute": "aframe-house", "commercial-hoa-property-claims": "metal-roof-shop",
    "hail-roof-claim-disputes": "hail-ground", "high-wind-tornado-claims": "tornado-plains", "burst-pipe-water-claims": "frozen-pipe",
    "house-fire-smoke-claims": "fire-damaged-house", "wildfire-ember-claims": "log-home-smoke", "snow-load-ice-dam-claims": "porch-collapse",
    "carrier-estimate-second-look": "inspector-clipboard", "neutral-umpire": "laptop-review",
}
SVC_FIG = {  # second, in-article photo per service
    "commercial-hoa-property-claims": "commercial-wind", "burst-pipe-water-claims": "mall-water", "high-wind-tornado-claims": "tree-snapped",
    "snow-load-ice-dam-claims": "log-home-snow", "wildfire-ember-claims": "wildfire-rawlins", "hail-roof-claim-disputes": "roof-tarp-lift",
    "home-insurance-dispute": "cabin-snow",
}
LOC_PHOTO = {
    "cheyenne": "cheyenne-depot", "casper": "casper-downtown", "laramie": "laramie-railyard", "gillette": "gillette-avenue",
    "rock-springs": "storm-chase", "sheridan": "barns-snow", "green-river": "green-river-island", "evanston": "uinta-wind-turbines",
    "riverton": "riverton-theater", "jackson": "jackson-downtown", "cody": "cody-downtown", "rawlins": "rawlins-ferris",
}
TOOL_PHOTO = {
    "award-net-gain-projector": "calculator-laptop", "acv-holdback-worksheet": "financial-calculator", "roof-area-pitch-waste": "roofers-gable",
    "deductible-comparison": "storm-chase", "claim-timeline-builder": "laptop-review", "appraisal-ready-meter": "team-meeting",
    "hail-test-square-scorer": "roof-tarp-lift",
}
POST_PHOTO = {
    "wyoming-appraisal-clause-plain-english": "team-meeting", "wind-driven-hail-siding-claims": "shingle-texture",
    "roof-collapse-from-snow-what-to-document": "cabin-snow", "choosing-appraiser-adjuster-or-attorney": "inspector-clipboard",
    "matching-and-discontinued-materials": "roofers-gable",
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
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


MARK_SVG = open(os.path.join(STATIC, "assets", "img", "mark.svg")).read() if os.path.exists(os.path.join(STATIC, "assets", "img", "mark.svg")) else ""


def mark(uid="m"):
    # inline brand mark (same geometry as favicon.svg); unique gradient id per instance
    return MARK_SVG.replace('id="g"', f'id="{uid}"').replace("url(#g)", f"url(#{uid})").replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


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
        "address": {"@type": "PostalAddress", "addressRegion": "WY", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-WY", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Wyoming property claims",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed hail, wind, snow, water and fire claims in all 23 Wyoming counties.",
        "areaServed": [{"@type": "State", "name": "Wyoming"}] + [{"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Wyoming"}} for l in LOCATIONS],
        "priceRange": "$$",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Wind damage", "Snow load", "Xactimate estimating", "Umpire services"],
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
LEARN = [("Appraisal step by step", P_PROCESS), ("Appraisal answers (FAQ)", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Claim guides", POST_BASE)]


def _groups():
    return [
        ("What we appraise", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("Every service", SVC_BASE), True),
        ("Where we work", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All 23 counties", LOC_BASE), True),
        ("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All calculators", TOOL_BASE), False),
        ("Resources", LEARN, None, False),
    ]


def header():
    menu = ""
    short = {"What we appraise": "Services", "Where we work": "Towns", "Free calculators": "Calculators", "Resources": "Resources"}
    for name, links, allk, cols in _groups():
        name = short[name]
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{e(name)}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{e(name)}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="solo" href="{P_ABOUT}">About us</a></li><li><a class="solo" href="{P_CONTACT}">Talk to us</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="head"><div class="wrap">
<a class="brand" href="/" aria-label="{BRAND} home">{mark("mh")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-r"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-sm head-cta" href="{P_CONTACT}">Free review</a>
<a class="nojs-menu" href="{P_MAP}">Menu</a><button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark("md")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a><button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a class="solo" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><small>Mon–Fri 8am–6pm Mountain · All 23 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap"><p class="foot-band-t">A claim that came up short deserves a second set of numbers.</p><div class="btn-row"><a class="btn btn-dark" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Send your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about"><a class="brand" href="/">{mark("mf")}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal, estimate review and umpire services for property owners with disputed insurance claims, from the Black Hills foothills to the Tetons.</p>
<p class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm Mountain</span></p></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Wyoming towns</h2><ul class="two">{loc}</ul></div>
<div><h2 class="foot-h">Calculators</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{P_ABOUT}">About us</a></li><li><a href="{P_CONTACT}">Talk to us</a></li><li><a href="{P_PROCESS}">Step by step</a></li><li><a href="{P_FAQ}">Answers</a></li><li><a href="{P_GLOSS}">Claim terms</a></li><li><a href="{POST_BASE}">Guides</a></li></ul></div>
</div>
<div class="wrap foot-base"><span>© {date.today().year} {BRAND}</span>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Legal notice</a></li><li><a href="{P_CRED}">Photo credits</a></li><li><a href="{P_MAP}">Site map</a></li></ul>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general and educational, policy terms vary, and no result is guaranteed.</p></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">Free review</a></div>"""


def gtm_head():
    # Snippet exactly as supplied by the site owner.
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
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n')


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, main=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, extra_nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        if t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = preload or "hero-supercell"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for t in MAIN_TYPES for n in extra_nodes if n.get("@type") == t]
    webpage["mainEntity"] = {"@id": main or (mains[0] if mains else DOMAIN + "/#business")}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Wyoming">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Wyoming">
<meta name="geo.region" content="US-WY">
<meta name="geo.placename" content="Wyoming">
<meta name="theme-color" content="#2a1206">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
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
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero">{img(photo, "phero-bg", lazy=False, alt="", extra=' data-zoom')}<div class="wrap">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><p class="side-t">Talk it through</p><p>The first conversation is free. We’ll tell you honestly whether appraisal fits your claim.</p><a class="side-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-block" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><p class="side-t">{e(title)}</p><ul class="side-list">{li}</ul></div>'


def cta_strip(h="Covered, but not paid in full?", p="Send us the carrier’s estimate. We’ll read it line by line and tell you what we see."):
    return f"""<section class="strip"><div class="wrap strip-in rv"><div><p class="strip-t">{e(h)}</p><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-dark" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap twocol"><article class="prose">{article}</article><aside class="side">{aside}</aside></div>'


LOSSES = ["Hail", "Wind / tornado", "Snow load / ice dam", "Frozen pipe / water", "Fire / smoke", "Wildfire", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hid="f"):
    roles = ["Homeowner", "Business owner", "Property manager / HOA", "Rancher / farm owner", "Contractor", "Attorney", "Public adjuster", "Other"]
    towns = [l["city"] for l in LOCATIONS] + ["Elsewhere in Wyoming"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-t">{e(heading)}</p><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(towns)}</select></div>
<div><label for="{hid}-amt">Amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy statement</a>.</span></label></div>
<div class="full"><button class="btn btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-t">Get a free claim review</p><p class="form-sub">Three fields. We’ll call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{P_PRIV}">privacy statement</a>.</span></label>
<button class="btn btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hero-form-note">{ic("shield")} No obligation. Nothing is shared.</p>
</form>"""


# ---------------------------------------------------------------- home
STORMS = [
    ("1949", "The Blizzard of ’49", "A January blizzard buried southeast Wyoming and the plains for weeks, stranding ranches and trains and killing livestock across the region."),
    ("1979", "Cheyenne tornado", "On July 16 a tornado crossed north Cheyenne near the airport, damaging hundreds of homes and businesses."),
    ("1985", "Cheyenne flash flood & hail", "On August 1 a stalled storm dropped heavy rain and hail on the city; the flood that followed killed twelve people."),
    ("1987", "Teton–Yellowstone tornado", "A violent tornado crossed the Teton Wilderness above 10,000 feet, flattening forest over miles of high terrain."),
    ("2005", "Wright tornado", "An August tornado struck the town of Wright in Campbell County, killing two people and destroying homes."),
    ("2020", "Mullen Fire", "The Mullen Fire burned more than 150,000 acres in the Medicine Bow National Forest and destroyed dozens of cabins and structures."),
]

PERILS = [
    ("hail-ground", "Hail", "Laramie County sits at the north end of one of the most active hail corridors in the country, and the hail usually rides a west wind.", f"{SVC_BASE}hail-roof-claim-disputes/"),
    ("tornado-plains", "Wind", "Downslope gusts along I-80 and I-25 strip shingles, siding and shop doors in every season — not only summer.", f"{SVC_BASE}high-wind-tornado-claims/"),
    ("porch-collapse", "Snow load", "Mountain towns carry some of the heaviest design snow loads in the lower 48. Framing fails before shingles do.", f"{SVC_BASE}snow-load-ice-dam-claims/"),
    ("frozen-pipe", "Freeze", "Twenty-below nights find every exterior-wall pipe and unheated crawlspace in the state.", f"{SVC_BASE}burst-pipe-water-claims/"),
    ("wildfire-rawlins", "Wildfire", "Beetle-killed timber and fast grass fires put cabins, ranches and outbuildings at risk from June to October.", f"{SVC_BASE}wildfire-ember-claims/"),
]


def home():
    K = BRAND
    perils = "".join(
        f'<a class="peril rv" href="{u}">{img(ph, sizes="(max-width:700px) 80vw, 300px", alt="")}<span class="peril-in"><span class="peril-k">{e(n)}</span><span class="peril-p">{e(t)}</span><span class="peril-go">{ic("arrow")}</span></span></a>'
        for ph, n, t, u in PERILS)
    svc_rows = "".join(
        f'<li class="rv"><a href="{SVC_BASE}{s["slug"]}/"><span class="svc-n">{i + 1:02d}</span><span class="svc-ph">{img(SVC_PHOTO[s["slug"]], sizes="96px", alt="")}</span><span class="svc-b"><span class="svc-t">{e(s["name"])}</span><span class="svc-s">{e(s["short"])}</span></span>{ic("arrow", "svc-a")}</a></li>'
        for i, s in enumerate(SERVICES))
    steps = [
        ("Free first look", f"We read your policy, the carrier’s estimate and your photos, then tell you whether a {K} can actually help — or whether you need someone else."),
        ("Our own scope", "We measure and photograph the property ourselves: every roof facet, every elevation, every room. No edited copies of the carrier’s numbers."),
        ("Written demand", f"Appraisal is demanded in writing and {K} is named as your appraiser inside the policy’s window."),
        ("Panel work", "We meet the carrier’s appraiser, ideally on site, and settle every line item the evidence supports."),
        ("Signed award", "Anything left goes to a neutral umpire. Two of three signatures set the amount of loss, and payment follows."),
    ]
    proc = "".join(f'<li class="tl-step"><span class="tl-dot">{i + 1}</span><div class="tl-body rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))
    storms = "".join(f'<li class="rv"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for y, t, p in STORMS)
    tools = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tcard-ico" aria-hidden="true">{e(t["icon"])}</span></span><span class="tcard-b"><span class="tcard-k">{e(t["kind"])}</span><span class="tcard-t">{e(t["name"])}</span><span class="tcard-s">{e(t["short"])}</span></span></a>'
        for t in TOOLS)
    towns = "".join(
        f'<a class="town rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="town-in"><span class="town-t">{e(l["city"])}</span><span class="town-c">{e(l["county"])}</span></span></a>'
        for l in LOCATIONS)
    guides = "".join(
        f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><p class="gcard-m">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree on what it costs. As the appraiser you name, we inspect, write an independent line-item estimate, work with the carrier’s appraiser and, if needed, present the leftover items to a neutral umpire."),
        (f"When is it worth calling a {K}?", "When coverage has been accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful — as a rough guide, more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, yes, once any two of the three panel members sign. It does not decide coverage, interest or bad-faith questions."),
        ("How is appraisal different from hiring a public adjuster?", "A public adjuster negotiates the whole claim, usually for a share of the recovery. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before work starts, and the first conversation is free."),
        (f"Does {K} cover my town?", "Yes. We work in all 23 Wyoming counties, with frequent claims in Cheyenne, Casper, Laramie, Gillette, Rock Springs, Sheridan and Jackson."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-supercell", lazy=False, alt="", extra=' data-zoom')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent claim appraisal · All 23 counties</p>
<h1>{K} <span>for claims that came up short</span></h1>
<p class="lede">Your carrier accepted the claim, but the check won’t rebuild the roof. {K} writes an independent, line-by-line valuation of the damage and carries it through the appraisal process already written into your policy.</p>
<div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="#services">See what we appraise</a></div>
</div>
{hero_form()}
</div>
<div class="wrap"><ul class="hero-ribbon"><li><b>Your appraiser</b><span>Retained by you, never the carrier</span></li><li><b>Priced locally</b><span>Cheyenne is not Jackson</span></li><li><b>Plain answers</b><span>Including “appraisal won’t help”</span></li></ul></div>
</section>

<section class="sec" id="fit"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Start here</p><h2>Do you need a {K}, or someone else?</h2><p>Three common situations, three different first calls. Picking the right one saves time and fees.</p></div>
<div class="fork" data-stagger>
<div class="fork-card yes rv"><span class="fork-n">A</span><h3>Covered, but paid short</h3><p>The carrier agrees the damage is covered. The argument is about slopes, siding, matching, prices or what’s missing.</p><p class="fork-go">Call a {K} — this is exactly what appraisal decides.</p></div>
<div class="fork-card rv"><span class="fork-n">B</span><h3>Not sure what’s missing</h3><p>You have the carrier’s estimate and a contractor’s bid, but you can’t tell where they differ or by how much.</p><p class="fork-go">Start with an <a href="{SVC_BASE}carrier-estimate-second-look/">estimate review</a>.</p></div>
<div class="fork-card no rv"><span class="fork-n">C</span><h3>Denied outright</h3><p>The carrier says the loss isn’t covered, raised late notice, or a deadline to sue is close.</p><p class="fork-go">Talk to a Wyoming-licensed attorney first. Appraisal doesn’t decide coverage.</p></div>
</div></div></section>

<section class="sec sec-stone"><div class="wrap">
<div class="sec-head left rv"><p class="kicker dark">Wyoming perils</p><h2>What Wyoming does to a building</h2><p>Every {K} file starts with the weather that caused it. These five perils account for nearly every disputed claim we see.</p></div>
<div class="perils" data-stagger>{perils}</div>
</div></section>

<section class="sec" id="services"><div class="wrap svc-split">
<div class="svc-intro rv"><p class="kicker dark">What we appraise</p><h2>Eleven ways a {K} works your claim</h2><p>Every service comes back to one job: a valuation of your loss that holds up in front of an umpire. Bring us in for a single estimate review, or name us as your appraiser once a demand is made.</p>
<figure class="svc-fig">{img("roofers-gable", sizes="(max-width:1020px) 100vw, 420px")}</figure>
<a class="btn" href="{SVC_BASE}">Compare every service {ic("arrow")}</a></div>
<ol class="svc-list">{svc_rows}</ol>
</div></section>

<section class="count-band" aria-label="At a glance"><div class="wrap counts">
<div class="count rv"><b data-count="23">23</b><span>Wyoming counties covered</span></div>
<div class="count rv"><b data-count="11">11</b><span>Appraisal &amp; estimating services</span></div>
<div class="count rv"><b data-count="7">7</b><span>Free claim calculators</span></div>
<div class="count rv"><b>2 of 3</b><span>Signatures make an award binding</span></div>
</div></section>

<section class="sec"><div class="wrap tl-split">
<div class="tl-photo rv">{img("inspector-clipboard", sizes="(max-width:1020px) 100vw, 460px")}<p class="tl-cap">An appraisal is won with measurements and photos, not adjectives.</p></div>
<div><div class="sec-head left rv"><p class="kicker dark">How it works</p><h2>From first call to a signed award</h2><p>The appraisal clause turns an open-ended argument into five defined steps. Here is how a {K} moves a file through them.</p></div>
<ol class="tl" data-fill><span class="tl-line" aria-hidden="true"><span class="tl-fill"></span></span>{proc}</ol>
<p><a class="more" href="{P_PROCESS}">Read the full eight-step guide {ic("arrow")}</a></p></div>
</div></section>

<section class="sec sec-ember" id="gap"><div class="wrap gap-split">
<div class="rv"><p class="kicker">Quick gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. If the difference is large, it is worth a conversation with a {K}. If it’s small, a documented supplement request may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}award-net-gain-projector/">award net-gain projector</a> subtracts appraiser and umpire fees so you can see a realistic net.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec sec-basalt"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Storm history</p><h2>The Wyoming storms that still shape claims</h2><p>Long memories matter in claims work. Carriers price risk on this history, and a {K} has to understand how each kind of event shows up in a building.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Free &amp; private</p><h2>Seven free calculators from a {K}</h2><p>Check the carrier’s math before you pick up the phone. Everything runs in your browser; nothing is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tools}</div>
<p class="center"><a class="btn btn-line" href="{TOOL_BASE}">Open the calculator library {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-stone"><div class="wrap">
<div class="sec-head left rv"><p class="kicker dark">Where we work</p><h2>{K} service across all 23 counties</h2><p>From Cheyenne to Jackson, every town has its own mix of weather and housing. These are the communities where {K} handles claims most often.</p></div>
<div class="towns" data-stagger>{towns}</div>
<p class="center"><a class="more" href="{LOC_BASE}">See statewide coverage {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Picking the right help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. A {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="who" data-stagger>
<div class="who-card hl rv"><h3>{K}</h3><dl><dt>Main job</dt><dd>Value the amount of a covered loss</dd><dt>Best time</dt><dd>Coverage accepted, number disputed</dd><dt>Result</dt><dd>Binding award on the amount</dd></dl></div>
<div class="who-card rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Present and negotiate the whole claim</dd><dt>Best time</dt><dd>Early, soon after the loss</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></div>
<div class="who-card rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Coverage, deadlines and bad faith</dd><dt>Best time</dt><dd>Denials or legal disputes</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></div>
</div></div></section>

<section class="sec sec-stone"><div class="wrap faq-split">
<div class="rv"><p class="kicker dark">Answers</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn" href="{P_FAQ}">All answers {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Claim guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from the {K} team on policy language, evidence and strategy.</p></div>
<div class="ggrid" data-stagger>{guides}</div>
</div></section>

<section class="pcta">{img("blizzard-lake", "pcta-bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap rv"><p class="kicker">Before you sign off</p><h2>The best time to check the numbers is before you accept them</h2><p>A short review now can keep you from settling for less than the repair costs.</p><div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec sec-basalt" id="contact"><div class="wrap contact-split">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Mountain</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 23 Wyoming counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hid="c")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Wyoming Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, snow, freeze and fire claims.",
                        body, schema, preload="hero-supercell", main=DOMAIN + "/#business", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("What we appraise", SVC_BASE), (s["name"], path)]
        idx = SERVICES.index(s)
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a class="rel" href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        towns = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All Wyoming towns", LOC_BASE)]
        ph = SVC_PHOTO[s["slug"]]
        fig = f'<figure class="fig">{img(SVC_FIG[s["slug"]], sizes="(max-width:1020px) 100vw, 720px")}</figure>' if s["slug"] in SVC_FIG else ""
        body_html = s["body"]
        if fig:
            parts = body_html.split("<h2>", 3)
            body_html = "<h2>".join(parts[:3]) + fig + "<h2>" + parts[3] if len(parts) > 3 else body_html + fig
        art = f"""{body_html}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="rels">{related}</div>"""
        body = page_hero(trail, "What we appraise", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(art, call_box() + list_box("All services", items, path) + list_box("Where we work", towns)) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Wyoming"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("What we appraise", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services in Wyoming",
                     "From a single estimate review to full panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of your loss.", "roofers-gable") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec sec-stone"><div class="wrap faq-split"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and plenty of disputes close right there.</p><a class="btn" href="{SVC_BASE}carrier-estimate-second-look/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you work on homes and commercial buildings?", "Yes — houses, cabins, manufactured homes, apartments, HOAs, shops, warehouses, churches and ranch buildings."), ("Is it only hail?", "No. We handle wind, snow load, freeze, water, fire, wildfire and other covered perils.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Wyoming | 11 Services",
                             "Insurance appraisal services in Wyoming: clause representation, hail, wind, snow load, freeze, fire and wildfire claims, estimate review and umpires.",
                             body, schema, preload="roofers-gable"), 0.9)


# ---------------------------------------------------------------- locations
REGIONS = [
    ("Southeast plains", "Cheyenne · Laramie · Wheatland · Torrington", "Hail, downslope wind and flash flooding along the Front Range and the North Platte valley.", "cheyenne-depot"),
    ("Central basins", "Casper · Riverton · Lander · Douglas", "Winter windstorms, cold inversions and summer hail in the North Platte and Wind River basins.", "casper-downtown"),
    ("Powder River & Bighorns", "Gillette · Sheridan · Buffalo · Newcastle", "Severe summer thunderstorms, large hail and occasional tornadoes on the northeast plains.", "gillette-avenue"),
    ("Southwest & I-80", "Rock Springs · Green River · Evanston · Rawlins", "Relentless wind, ground blizzards and frozen pipes along the I-80 corridor.", "green-river-island"),
    ("Northwest mountains", "Jackson · Cody · Pinedale · Afton", "Heavy snow loads, ice dams, wildfire and high-value custom homes.", "jackson-downtown"),
]


def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Where we work", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a class="rel" href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        art = f"""<div class="note"><b class="h">Local claim risks</b><ul class="chips">{chips}</ul><p class="small">Housing mix: {e(l["housing"])}.</p></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}:</p>
<ul class="cols2">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby towns</h2><div class="rels">{near}</div>"""
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, call_box() + list_box("Wyoming towns", items, path) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Wyoming"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {l['city']}, WY | Claim Disputes"
        if len(title) > 58:
            title = f"Insurance Appraiser in {l['city']}, WY"
        desc = f"Independent insurance appraiser in {l['city']}, {l['county']}. Appraisal and estimate review for underpaid hail, wind, snow and water claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser in {l['city']}, {l['county']}: appraisal and estimate review for underpaid hail, wind, snow and water claims."
        if len(desc) < 110:
            desc = desc[:-1] + ", with on-site inspections."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Where we work", LOC_BASE)]
    towns = "".join(f'<a class="town rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="town-in"><span class="town-t">{e(l["city"])}</span><span class="town-c">{e(l["county"])}</span></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="icard rv"><span class="icard-ph">{img(ph, sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">{e(t)}</span><h3>{e(n)}</h3><p>{e(d)}</p></span></div>' for n, t, d, ph in REGIONS)
    body = page_hero(trail, "Where we work", "Insurance Appraisal Across All 23 Wyoming Counties",
                     "We work statewide, from the Nebraska line to Yellowstone. These local pages cover the towns where we handle claims most often; we travel to every county.", "state-capitol") + f"""
<section class="sec"><div class="wrap"><div class="towns" data-stagger>{towns}</div></div></section>
<section class="sec sec-stone"><div class="wrap"><div class="sec-head left rv"><p class="kicker dark">Regions</p><h2>How claims differ across Wyoming</h2><p>The same policy wording plays out very differently on a Cheyenne ranch house, a Gillette metal shop and a Teton County timber home.</p></div><div class="igrid" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Wyoming county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Wyoming Insurance Appraiser Locations | 23 Counties",
                             "Insurance appraisal in all 23 Wyoming counties, including Cheyenne, Casper, Laramie, Gillette, Rock Springs, Sheridan, Jackson and Cody.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload="state-capitol"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free calculators", TOOL_BASE), (t["name"], path)]
        i = TOOLS.index(t)
        others = "".join(f'<a class="rel" href="{TOOL_BASE}{o["slug"]}/"><small>{e(o["kind"])}</small>{e(o["name"])}</a>' for o in [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>
""" + layout(f'{t["explain"]}<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}<h2>More free calculators</h2><div class="rels">{others}</div>', call_box() + list_box("All calculators", items, path)) + cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Free calculators", TOOL_BASE)]
    tiles = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tcard-ico" aria-hidden="true">{e(t["icon"])}</span></span><span class="tcard-b"><span class="tcard-k">{e(t["kind"])}</span><h2 class="tcard-t">{e(t["name"])}</h2><span class="tcard-s">{e(t["short"])}</span></span></a>' for t in TOOLS)
    order = [("claim-timeline-builder", "Protect your deadlines first"), ("hail-test-square-scorer", "Score each roof slope after a hailstorm"), ("roof-area-pitch-waste", "Check the roof measurements"), ("deductible-comparison", "See what the deductible takes"), ("acv-holdback-worksheet", "Split the payment into ACV and holdback"), ("award-net-gain-projector", "Test whether appraisal pays off"), ("appraisal-ready-meter", "Score your file before a demand")]
    ol = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(next(t["name"] for t in TOOLS if t["slug"] == s))}</a> — {e(d)}</li>' for s, d in order)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Wyoming",
                     "Seven calculators and planners built from real appraisal work. Check the carrier’s math and decide your next step — no sign-up, and nothing you enter leaves your browser.", "calculator-laptop", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{tiles}</div></div></section>
<section class="sec sec-stone"><div class="wrap faq-split"><div class="rv"><p class="kicker dark">Suggested order</p><h2>Using the calculators together</h2><ol>{ol}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Wyoming Tools",
                              "Seven free property claim calculators: appraisal net gain, RCV vs ACV, roof squares, deductibles, claim deadlines, readiness and hail test squares.",
                              body, schema, preload="calculator-laptop"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal step by step", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _) in enumerate(PROCESS_STEPS))
    art = f'<nav class="toc" aria-label="Steps"><p class="toc-t">The eight steps</p><ol>{toc}</ol></nav>{PROCESS_BODY}'
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Wyoming, Step by Step",
                     "Eight steps from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "inspector-clipboard",
                     [("Steps", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "Any 2 of 3 sign")]) + layout(art, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Wyoming", "description": "The steps of a property insurance appraisal from the first disagreement to a signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Wyoming | 8 Steps",
                         "A step-by-step guide to insurance appraisal in Wyoming: the written demand, naming appraisers, choosing an umpire, panel work and the award.",
                         body, [crumbs_schema(trail), howto], preload="inspector-clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal answers", path)]
    jump = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = f'<div class="jump">{jump}</div>' + "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions, Answered for Wyoming",
                     "Plain answers grouped by topic: appraisal basics, cost and timing, Wyoming specifics and working with us.", "team-meeting") + layout(groups, call_box() + list_box("Resources", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ for Wyoming | Answers by Topic",
                         "Answers to common Wyoming insurance appraisal questions, grouped by topic: how it works, cost and timing, state rules and working with an appraiser.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="team-meeting"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>"
    art = f'<div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "financial-calculator", cta=False) + layout(art, call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "A searchable glossary of property insurance claim terms: actual cash value, holdback, test squares, umpires, matching, O&P and more, in plain English.",
                         body, [crumbs_schema(trail), dts], preload="financial-calculator"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim guides", POST_BASE), (p["title"], path)]
        i = POSTS.index(p)
        others = "".join(f'<a class="rel" href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = f'<p class="byline">By the {BRAND} team · Published {nice} · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2><div class="rels">{others}</div>'
        body = page_hero(trail, f"Claim guide · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", LEARN) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        artn = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "keywords": p["kw"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), artn], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim guides", path)]
    cards = "".join(f'<article class="gcard rv"><a class="gcard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><p class="gcard-m">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Claim guides", "Claim Guides for Wyoming Property Owners",
                     "Practical guides on policy language, evidence and claim strategy, written by people who work appraisal panels.", "shingle-texture", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Claim Guides for Wyoming Property Owners",
                         "Guides for Wyoming property owners on the appraisal clause, wind-driven hail, snow load claims, matching and choosing an appraiser or attorney.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="shingle-texture"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About us", path)]
    art = f"""<figure class="fig">{img("team-meeting", sizes="(max-width:1020px) 100vw, 720px")}</figure>
<h2>One question, done well</h2>
<p>Most claim professionals do a little of everything. {BRAND} works on one question — the amount of a covered loss — and our process, calculators and documentation standards are built around answering it well. That focus lets us serve as the appraiser you name, review an estimate before a dispute escalates, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>We scope it ourselves.</strong> We measure and photograph before we look at anyone else’s numbers.</li>
<li><strong>Defensible beats impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Local pricing.</strong> Labor and materials in Teton County are not priced like Laramie County, and remote jobs carry travel and mobilization. Our numbers reflect where the property is.</li>
<li><strong>Plain-English reports.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If you need an attorney or a public adjuster instead, we say so on the first call.</li>
<li><strong>Fees in writing</strong> before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, cabin owners, ranchers, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Wyoming. On any one claim we serve in a single role, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t publish testimonials or promise outcomes; every claim turns on its own facts.</p>
<h2>Statewide on purpose</h2>
<p>Wyoming has about 590,000 people spread across nearly 98,000 square miles. Working statewide means we see every kind of loss the state produces — hail in Cheyenne, wind in Rawlins, snow load in Jackson, freeze in Laramie, wildfire in the Medicine Bow — and we price each with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a covered claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "roof-tarp-lift") + layout(art, call_box() + list_box("Explore", [("What we appraise", SVC_BASE), ("Where we work", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal step by step", P_PROCESS)])) + cta_strip()
    write(path, document(path, f"About Us | {BRAND}",
                         "Wyoming Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property insurance claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="roof-tarp-lift"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Talk to us", path)]
    body = page_hero(trail, "Talk to us", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "laptop-review", cta=False) + f"""
<section class="sec sec-basalt"><div class="wrap contact-split">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Mountain</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>Statewide — all 23 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s complete estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hid="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Get a free review of a disputed Wyoming property claim. Call or text (844) 537-1427, email us, or send your claim details through the form.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="laptop-review"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · {e(v["source"].title())}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    legal = {
        P_PRIV: ("Privacy Statement", "Privacy statement", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share — such as your name, phone number, email address, property location and claim details. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. The figures you enter are not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics through Google Tag Manager, it will be described here.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us.",
                 "Privacy statement for Wyoming Insurance Appraiser: what we collect through forms, calls and email, how we use it, and the choices you have."),
        P_TERMS: ("Terms and Conditions", "Terms", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in Wyoming.</p>
<h2>No professional relationship</h2><p>Reading the site, using a calculator or submitting a form doesn’t create an appraiser–client relationship. That begins only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a Wyoming-licensed attorney for legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from the figures you enter. Example figures are illustrative. None of it is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{P_CRED}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Wyoming.</p>""", "The terms that apply when you use this website and its calculators.",
                 "Terms and conditions for using the Wyoming Insurance Appraiser website, its free claim calculators, guides and contact forms."),
        P_DISC: ("Legal Notice", "Legal notice", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results, no testimonials</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. We don’t publish reviews or testimonials, and no appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, contact a Wyoming-licensed attorney promptly.</p>
<h2>Legal references</h2><p>References to statutes, court decisions, the Wyoming Department of Insurance or historical weather events are general context, not legal analysis. Verify current law with official sources.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. Some show Wyoming towns; others show weather or damage elsewhere. None show our clients’ properties.</p>""", "Important limits on the information published on this website.",
                 "Legal notice for Wyoming Insurance Appraiser: general information only, no legal advice, no guaranteed results, and how to treat policy deadlines."),
        P_CRED: ("Photo Credits", "Photo credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. We found them through the Openverse catalog; sources include Wikimedia Commons, Flickr, rawpixel and StockSnap. Attribution isn’t legally required, but we credit the photographers here with thanks. Photos are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for every photograph used on this site.",
                 "Photo credits for Wyoming Insurance Appraiser: sources, creators and CC0 or public-domain licenses for every photograph used on the site."),
    }
    for path, (title, crumb, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (crumb, path)]
        body = page_hero(trail, "Legal", title, lede, "state-capitol", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], preload="state-capitol"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", P_ABOUT), ("Talk to us", P_CONTACT)]),
        ("What we appraise", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Where we work", [("All Wyoming towns", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy statement", P_PRIV), ("Terms and conditions", P_TERMS), ("Legal notice", P_DISC), ("Photo credits", P_CRED)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "state-capitol", cta=False) + f'<section class="sec"><div class="wrap"><div class="mapgrid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Wyoming towns, free claim calculators, guides and legal pages.", body, [crumbs_schema(trail)], preload="state-capitol"), 0.3)

    body = f"""<section class="phero phero-404">{img("blizzard-lake", "phero-bg", lazy=False, alt="")}<div class="wrap"><p class="kicker">Error 404</p><h1>Lost in a ground blizzard</h1><p class="lede">The page you’re looking for has moved or never existed. One of these should get you back on the road.</p><div class="btn-row"><a class="btn" href="/">Home</a><a class="btn btn-line-light" href="{SVC_BASE}">Services</a><a class="btn btn-line-light" href="{TOOL_BASE}">Calculators</a><a class="btn btn-line-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
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
// Wyoming Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$wyia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$wyia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$wyia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($wyia_host === 'www.' . $wyia_real || ($wyia_host === $wyia_real && $wyia_proto === 'http')) {
    header('Location: https://' . $wyia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $idx_m)) {
    $idx_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $idx_m[1] . $idx_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($wyia_host !== $wyia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Wyoming Insurance Appraiser - front controller for the static build.
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
