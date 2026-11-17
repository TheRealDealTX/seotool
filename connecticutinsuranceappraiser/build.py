#!/usr/bin/env python3
"""Static site generator for connecticutinsuranceappraiser.com.

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

BRAND = "Connecticut Insurance Appraiser"
HOST = "connecticutinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261117a"
FAV = "1"

# Google Tag Manager: leave empty until a container ID is supplied (e.g. "GTM-XXXXXXX").
GTM_ID = "GTM-NJGTDPZV"

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/ct-appraisal-services/"
LOC_BASE = "/ct-towns/"
TOOL_BASE = "/ct-claim-tools/"
POST_BASE = "/ct-claim-insights/"
PROCESS = "/ct-appraisal-process/"
FAQ_P = "/ct-appraisal-faq/"
GLOSS = "/ct-claim-glossary/"
ABOUT = "/about-ct-insurance-appraiser/"
CONTACT = "/contact-ct-appraiser/"
PRIVACY = "/ct-privacy-policy/"
TERMS = "/ct-terms-of-use/"
DISCLAIM = "/ct-disclaimer/"
SITEMAP = "/ct-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-saltbox": "Red saltbox colonial house with a center chimney in Connecticut",
    "hartford-river": "Hartford, Connecticut skyline across the Connecticut River",
    "new-haven-pirelli": "Modernist Pirelli building against a blue sky in New Haven, Connecticut",
    "stamford-tower": "Glass office tower with stacked floors in downtown Stamford, Connecticut",
    "candlewood-lake": "Boats and a white clubhouse on Candlewood Lake near Danbury, Connecticut",
    "new-london-harbor": "Red tugboat crossing the harbor in New London, Connecticut",
    "rowayton-marina": "Boats docked along the river in Rowayton, Norwalk, Connecticut",
    "milford-point": "Winter beach and tidal flats at Milford Point, Connecticut",
    "winter-farm": "Farmhouse in a snow-covered field below a tree line",
    "foursquare-snow": "Foursquare house with a wraparound porch after a snowfall",
    "victorian-home": "Blue Victorian house with a steep gable roof behind a hedge",
    "hartford-office-tower": "Tall concrete office tower against a deep blue sky",
    "winter-valley": "Snowy wooded hillside overlooking a Connecticut town",
    "snowy-lakehouses": "Houses on a frozen lake shore after heavy snow",
    "roof-shingles": "Close-up of overlapping dark roof shingles",
    "storm-sky": "Dark storm clouds breaking over the horizon",
    "stormy-beach": "Storm clouds and rough surf on a sandy beach",
    "lighthouse-coast": "White lighthouse with a red lantern above the sea at dusk",
    "fallen-tree": "Large fallen tree trunk on the forest floor",
    "storm-damaged-house": "Excavator clearing a storm-damaged house",
    "consultation": "Two women talking across a table by an office window",
    "team-laptops": "Three colleagues reviewing work on laptops at a table",
    "calculator-laptop": "Calculator resting on a laptop beside a printed report",
    "calculator-hands": "Hands entering figures on a calculator beside paperwork",
    "laptop-calculator": "Person using a calculator next to a laptop spreadsheet",
    "kitchen": "Bright kitchen with a white island and pendant lights",
    "living-room": "Living room with a gray sofa and large windows",
    "office-lobby": "Lit office building entrance at night",
    "rowayton-boathouse": "White shingle-style boathouse with bay windows near the water",
    "house-fire": "House engulfed in flames at night",
    "roof-torn-open": "House with its roof torn open after a storm",
    "hurricane-trees-down": "Trees snapped and blown down across a path after a hurricane",
    "tornado-home-damage": "House with heavy roof and wall damage after a tornado",
    "rain-window": "Heavy rain running down a window",
    "storm-debris": "Debris and damaged homes in a neighborhood after a severe storm",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appraiser": "consultation", "homeowners-claim-appraisal": "victorian-home",
    "commercial-condo-hoa-appraisal": "hartford-office-tower", "roof-and-hail-appraisal": "roof-shingles",
    "wind-and-tornado-appraisal": "tornado-home-damage", "hurricane-and-tropical-storm-appraisal": "stormy-beach",
    "water-damage-appraisal": "rain-window", "fire-and-smoke-appraisal": "house-fire",
    "fallen-tree-damage-appraisal": "hurricane-trees-down", "ice-dam-and-winter-storm-appraisal": "foursquare-snow",
    "insurance-estimate-review": "laptop-calculator", "umpire-services": "team-laptops",
}
LOC_PHOTO = {
    "hartford": "hartford-river", "new-haven": "new-haven-pirelli", "stamford": "stamford-tower", "bridgeport": "lighthouse-coast",
    "waterbury": "winter-valley", "norwalk": "rowayton-marina", "danbury": "candlewood-lake", "new-london": "new-london-harbor",
    "greenwich": "rowayton-boathouse", "west-hartford": "fallen-tree", "milford": "milford-point", "torrington": "winter-farm",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-hands", "rcv-acv-holdback-calculator": "calculator-laptop",
    "roof-square-pitch-converter": "roof-torn-open", "hurricane-deductible-calculator": "storm-sky",
    "claim-calendar-builder": "laptop-calculator", "appraisal-readiness-checkup": "consultation",
    "fallen-tree-claim-calculator": "fallen-tree",
}
POST_PHOTO = {
    "connecticut-hurricane-deductibles": "lighthouse-coast", "tree-fell-on-house-connecticut": "hurricane-trees-down",
    "ice-dam-claims-connecticut": "snowy-lakehouses", "appraiser-public-adjuster-or-attorney-ct": "team-laptops",
    "reading-a-carrier-estimate": "calculator-hands", "crumbling-foundations-and-appraisal": "victorian-home",
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
    "left": '<path d="M15 6l-6 6 6 6"/>',
    "right": '<path d="M9 6l6 6-6 6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=40):
    """Brand mark: a roof chevron over two estimate lines (one coral) on a blue tile."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#1F64E5"/>'
            '<path d="M10 23.5L24 12l14 11.5" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15 30h18" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>'
            '<path d="M15 37h11" stroke="#FF6B57" stroke-width="3.6" stroke-linecap="round"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Connecticut</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "CT", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-CT", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Connecticut property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 169 Connecticut towns.",
        "areaServed": [{"@type": "State", "name": "Connecticut"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Fallen tree claims", "Hurricane deductibles", "Ice dam claims"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- navigation
LEARN = [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_P), ("Claim glossary", GLOSS), ("Claim insights", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Towns", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Connecticut towns", LOC_BASE)),
        ("Free tools", [(t["name"], tool_path(t)) for t in TOOLS], ("All claim tools", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="dd-all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-dd"><button type="button" class="dd-btn" aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "ic chev")}</button><ul class="dd{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="nav-a" href="{ABOUT}">About</a></li><li><a class="nav-a" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head" id="top"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="nav-list">{menu}</ul></nav>
<div class="head-cta"><a class="head-phone" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-coral btn-sm" href="{CONTACT}">Free claim review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand drawer-brand")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-blue" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 169 towns</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot"><div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Questioning a short settlement? Start with a free look at the numbers.</p><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Email your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand foot-brand")}
<p>Independent appraisal and estimating help for Connecticut property owners whose covered claims came up short, from Greenwich to the Quiet Corner.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm ET · Statewide</li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Towns</h2><ul>{loc}<li><a href="{LOC_BASE}">All towns</a></li></ul></div>
<div><h2 class="foot-h">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{ABOUT}">About</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Claim insights</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general information; policy wording controls. Example figures are illustrative, and no outcome is guaranteed.</p>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free review</a></div>"""


# ---------------------------------------------------------------- document
# The head snippet is used exactly as supplied by the site owner.
GTM_HEAD = """<!-- Google Tag Manager -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-NJGTDPZV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>
<!-- End Google Tag Manager -->
"""


def gtm_head():
    return GTM_HEAD if GTM_ID else ""


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id, about = "WebPage", [], None, None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
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
        extra.append(n)
    img_key = preload or "hero-saltbox"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for n in extra if n.get("@type") in MAIN_TYPES]
    if path == "/":
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    elif mains:
        webpage["mainEntity"] = {"@id": mains[0]}
    elif any(n.get("@type") == "FAQPage" for n in extra):
        webpage["mainEntity"] = {"@id": canonical + "#faq"}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Connecticut">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Connecticut">
<meta name="geo.region" content="US-CT">
<meta name="geo.placename" content="Connecticut">
<meta name="theme-color" content="#1F64E5">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700;800&family=Golos+Text:wght@400;500;600;700&display=swap">
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
    # Pages are served as dir/index.php: the host serves real files without running the front
    # controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">›</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, "phero-img", lazy=False, alt="", extra=' data-parallax="0.18"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker kicker-light">{e(tag)}</p><h1>{e(h1)}</h1><p class="phero-lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-t">Talk it through first</h2><p>A free, no-pressure conversation. We’ll say plainly whether appraisal fits your claim.</p><a class="side-phone" href="tel:{TEL}">{ic("phone")} {PHONE_INTL}</a><a class="btn btn-coral btn-block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right")}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-t">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def aside(*boxes):
    return '<aside class="side"><div class="side-sticky">' + "".join(boxes) + "</div></aside>"


def cta_strip(h="Not sure the carrier’s number is right?", p="Send the estimate and a few photos. We’ll tell you what we see, free."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items, label):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(label)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for n, p in items) + "</div>"


LOSSES = ["Fallen tree", "Wind / tornado", "Hurricane / tropical storm", "Ice dam / snow load", "Hail / roof", "Water / frozen pipe", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(title="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", uid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    towns = [l["city"] for l in LOCATIONS] + ["Another Connecticut town"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<p class="lead-t">{e(title)}</p><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="span2"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property town</label><select id="{uid}-city" name="city">{_opt(towns)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="span2"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>
<div class="span2"><label for="{uid}-det">What happened, and where does the claim stand?</label><textarea id="{uid}-det" name="details" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="span2 hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="span2"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="span2"><button class="btn btn-blue btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def dock_form():
    return f"""<form class="dock" action="/api/contact.php" method="post" data-lead novalidate>
<p class="dock-t">{ic("shield")} Free claim review</p>
<div class="dock-fields">
<div><label for="d-name">Name *</label><input id="d-name" name="name" autocomplete="name" required></div>
<div><label for="d-phone">Phone *</label><input id="d-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="d-loss">Type of loss</label><select id="d-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="d-web">Website</label><input id="d-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<div class="dock-go"><button class="btn btn-coral btn-block" type="submit">Request a call {ic("arrow")}</button></div>
</div>
<label class="check dock-consent"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<div class="form-msg" role="status"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("coast", "Fairfield County & the Gold Coast", "Greenwich · Stamford · Norwalk · Bridgeport", ["Hurricane & surge", "Tree falls", "High-value homes"],
     "Waterfront homes from Byram to Black Rock face Long Island Sound, while backcountry estates sit under tall oaks. Sandy and Isaias left both kinds of damage.", "rowayton-marina"),
    ("capitol", "Greater Hartford", "Hartford · West Hartford · Manchester", ["Ice dams", "Tree falls", "Three-families"],
     "The Capitol Region’s older housing, from Asylum Hill Victorians to West Hartford colonials, makes plaster, slate and matching the usual sticking points.", "hartford-river"),
    ("shore", "New Haven & the Shoreline", "New Haven · Milford · Guilford · Old Saybrook", ["Coastal wind", "Tornado history", "Beach homes"],
     "From the 1989 Hamden tornado to Irene and Sandy on Milford’s beaches, the central shoreline sees wind from every direction.", "milford-point"),
    ("valley", "Naugatuck & Housatonic Valleys", "Waterbury · Danbury · Naugatuck · Shelton", ["Hail", "Frozen pipes", "Mill buildings"],
     "Inland valleys see more summer hail than the coast and harsher winters. Brick mills and hillside three-deckers add their own complications.", "winter-valley"),
    ("hills", "Litchfield Hills", "Torrington · Litchfield · New Milford · Winsted", ["Snow load", "Barns & outbuildings", "Second homes"],
     "Higher ground means heavier snow, longer freezes and more seasonal homes, so heat, vacancy and collapse wording all come into play.", "winter-farm"),
    ("east", "Eastern Connecticut & the Quiet Corner", "New London · Groton · Norwich · Willimantic", ["Hurricane history", "Historic buildings", "Rural property"],
     "The 1938 hurricane hit New London hardest. Today the region mixes shoreline exposure, historic downtowns and rural homes on large lots.", "new-london-harbor"),
]

ALMANAC = [
    ("1938", "The Great New England Hurricane", "Struck without warning on September 21 and reshaped the shoreline from Old Saybrook to Stonington. Still the benchmark for Connecticut wind and surge."),
    ("1955", "The August floods", "Remnants of Connie and Diane sent the Naugatuck, Farmington and Quinebaug rivers through Waterbury, Torrington, Winsted and Putnam."),
    ("1979", "Windsor Locks tornado", "An October tornado tore through Windsor and Windsor Locks, one of the strongest ever recorded in New England."),
    ("1985", "Hurricane Gloria", "Crossed the coast near Milford in September, toppling trees and knocking out power across most of the state."),
    ("1989", "Hamden tornado", "A July tornado cut through Hamden and parts of New Haven, damaging hundreds of homes."),
    ("2011", "Irene, then the October nor’easter", "Irene battered the shoreline in August. Two months later, heavy snow on leafed-out trees caused record outages and tree damage inland."),
    ("2012", "Superstorm Sandy", "Record surge flooded shoreline neighborhoods from Greenwich to East Haven and beyond."),
    ("2013", "February blizzard", "Two to three feet of snow buried much of the state; Hamden measured about 40 inches."),
    ("2018", "May 15 tornadoes", "Several tornadoes and a macroburst crossed New Haven and Fairfield counties in one afternoon."),
    ("2020", "Tropical Storm Isaias", "Gusts brought down trees and wires in nearly every town, with outages lasting a week in places."),
    ("2021", "Henri and Ida", "Henri threatened the coast in August; weeks later Ida’s remnants caused flash flooding inland."),
]


def home():
    K = BRAND
    perils_svc = SERVICES
    svc_cards = "".join(
        f'<a class="scard rv" href="{svc_path(s)}"><span class="scard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}</span><span class="scard-n">{i + 1:02d}</span><span class="scard-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">View service {ic("arrow")}</span></span></a>'
        for i, s in enumerate(perils_svc))
    alm = "".join(f'<li class="alm-card"><span class="alm-y">{y}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for y, n, t in ALMANAC)
    regions = "".join(
        f'<article class="reg{" open" if i == 0 else ""}" tabindex="0">{img(ph, "reg-img", sizes="(max-width:900px) 100vw, 40vw", alt="")}<div class="reg-in"><p class="reg-k">{e(s)}</p><h3>{e(n)}</h3><div class="reg-more"><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in pr)}</ul><p>{e(t)}</p></div></div></article>'
        for i, (k, n, s, pr, t, ph) in enumerate(REGIONS))
    steps = "".join(f'<li class="tl-step"><span class="tl-dot">{i + 1}</span><div class="tl-body rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(PROCESS_STEPS))
    tools = "".join(f'<a class="tcard rv" data-tilt href="{tool_path(t)}"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="tcard-kind">{t["kind"]}</span></span><span class="tcard-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    towns = "".join(f'<a class="town rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], "town-img", sizes="(max-width:640px) 50vw, 25vw", alt="")}<span class="town-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    posts = "".join(f'<article class="pcard rv"><a class="pcard-img" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="pcard-b"><p class="meta">{p["read"]} read</p><h3><a href="{post_path(p)}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree about the cost. As your named appraiser we inspect, write an independent line-item estimate, work with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster manages and negotiates the whole claim, usually for a percentage. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When is it worth calling a {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and a qualified contractor’s number is meaningful, often more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, yes, once two of the three panel members sign. That is why documentation should be in place before appraisal is demanded."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of any umpire fee. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you cover my town?", "Yes. We work in all 169 Connecticut towns and cities, in every one of the state’s eight counties."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero-saltbox", "hero-img", lazy=False, alt="", extra=' data-parallax="0.22"')}</div>
<div class="wrap hero-in">
<p class="kicker kicker-light">Independent property claim appraisal · Statewide</p>
<h1><span class="h1-brand">{K}</span> <span class="h1-rest">for claims that were accepted, then underpaid</span></h1>
<p class="hero-lede">Your insurer agreed the damage is covered. The check still won’t pay for the repair. {K} writes an independent, line-by-line valuation of your loss and carries it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="#services">See what we value {ic("arrow")}</a></div>
</div>
<div class="wrap dock-wrap">{dock_form()}</div>
</section>

<section class="counts" aria-label="At a glance"><div class="wrap counts-in">
<div class="count rv"><b data-count="169">169</b><span>Connecticut towns and cities served</span></div>
<div class="count rv"><b data-count="8">8</b><span>Counties, from Fairfield to Windham</span></div>
<div class="count rv"><b data-count="12">12</b><span>Appraisal and estimating services</span></div>
<div class="count rv"><b data-count="7">7</b><span>Free claim calculators</span></div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-copy rv">
<p class="kicker">Second opinion, first-hand measurements</p>
<h2>The {K} behind the second opinion</h2>
<p>Most short claims aren’t denials. They are estimates that skipped a roof plane, priced plaster as drywall, or left the crane out of a tree removal. {K} exists for the space between “covered” and “paid in full.”</p>
<p>We start from our own inspection, never from an edited copy of the carrier’s file. Then we price what we can defend, because an umpire rewards credible numbers and discounts inflated ones. When a claim needs an attorney or a public adjuster instead, a {K} conversation will tell you that on the first call.</p>
<ul class="ticks"><li>{ic("check")}<span><b>Independent scope.</b> Measured and photographed by us.</span></li><li>{ic("check")}<span><b>Connecticut pricing.</b> Line items priced for your ZIP code.</span></li><li>{ic("check")}<span><b>Plain reporting.</b> Every difference explained in writing.</span></li></ul>
<a class="btn btn-blue" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
<div class="ledger rv" aria-label="Illustrative estimate comparison">
<div class="ledger-head"><span>Where estimates thin out</span><em>Illustrative example</em></div>
<table><thead><tr><th scope="col">Line item</th><th scope="col">Carrier</th><th scope="col">Independent</th></tr></thead><tbody>
<tr><th scope="row">Roof squares (9/12 colonial)</th><td>18.0</td><td>23.4</td></tr>
<tr><th scope="row">Steep-roof labor</th><td>—</td><td>Included</td></tr>
<tr><th scope="row">Ice-and-water shield at eaves</th><td>—</td><td>Included</td></tr>
<tr><th scope="row">Plaster ceiling repair</th><td>Drywall</td><td>Plaster</td></tr>
<tr><th scope="row">Tree removal from roof (crane)</th><td>—</td><td>Included</td></tr>
<tr><th scope="row">Overhead &amp; profit</th><td>—</td><td>10% + 10%</td></tr>
</tbody><tfoot><tr><th scope="row">Replacement cost</th><td>$21,300</td><td>$38,700</td></tr></tfoot></table>
<p class="ledger-note">Figures are illustrative only, not a client result.</p>
</div>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Appraisal &amp; estimating</p><h2>Twelve kinds of loss, one valuation discipline</h2><p>Each {K} service starts the same way: an accurate scope of what was damaged and an honest price for putting it back. Begin with an estimate review, or bring us in once appraisal is demanded.</p></div>
<div class="scards" data-stagger>{svc_cards}</div>
<p class="center-row"><a class="btn btn-line" href="{SVC_BASE}">Compare every service {ic("arrow")}</a></p>
</div></section>

<section class="sec almanac"><div class="wrap">
<div class="sec-head sec-head-split rv"><div><p class="kicker kicker-light">Storm almanac</p><h2>A storm almanac for Connecticut property owners</h2><p>A {K} reads every file against the storm that caused it. These are the events that still shape how carriers, contractors and panels think about damage here.</p></div><div class="alm-nav"><button type="button" class="alm-btn" data-alm="-1" aria-label="Previous storms">{ic("left")}</button><button type="button" class="alm-btn" data-alm="1" aria-label="Next storms">{ic("right")}</button></div></div>
<ol class="alm-track" tabindex="0" aria-label="Connecticut storm timeline">{alm}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Six regions</p><h2>Six corners of the Nutmeg State, six claim patterns</h2><p>Connecticut is small, but its claims are not uniform. A {K} prices a Greenwich waterfront house, a Waterbury three-decker and a Litchfield barn very differently.</p></div>
<div class="regions" data-regions>{regions}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap tl-wrap">
<div class="tl-intro"><div class="tl-sticky rv"><p class="kicker">The process</p><h2>From demand letter to two signatures</h2><p>The appraisal clause turns an open-ended argument into eight defined steps with a binding result. This is how a {K} file moves.</p><a class="btn btn-blue" href="{PROCESS}">Read the process guide {ic("arrow")}</a></div></div>
<ol class="timeline-v" data-timeline><span class="tl-line" aria-hidden="true"><span class="tl-fill"></span></span>{steps}</ol>
</div></section>

<section class="sec sec-deep" id="gap"><div class="wrap split">
<div class="rv"><p class="kicker kicker-light">Quick check</p><h2>Run your two numbers</h2><p>Enter the carrier’s estimate and your contractor’s. If the difference is large, talking to a {K} makes sense. If it is small, a documented supplement may close it faster.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap and fee estimator</a> adds appraiser and umpire fees and shows your break-even point.</p><a class="btn btn-coral" href="{TOOL_BASE}">Open all seven tools {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Seven free calculators from a {K}</h2><p>Check the carrier’s math before you pick up the phone. Every tool runs in your browser, and nothing you enter is stored or sent.</p></div>
<div class="tcards" data-stagger>{tools}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head sec-head-split rv"><div><p class="kicker">Statewide coverage</p><h2>{K} service in twelve towns</h2><p>We inspect in every Connecticut town. These local pages cover the places our files come from most.</p></div><a class="btn btn-line" href="{LOC_BASE}">All Connecticut towns {ic("arrow")}</a></div>
<div class="towns" data-stagger>{towns}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. A {K} will point you elsewhere when appraisal is the wrong tool.</p></div>
<div class="who" data-stagger>
<div class="who-card who-us rv"><p class="who-k">{K}</p><h3>Values the amount of loss</h3><ul><li>{ic("check")}Coverage accepted, number disputed</li><li>{ic("check")}Binding award on the amount</li><li>{ic("check")}Fee agreed in writing up front</li></ul></div>
<div class="who-card rv"><p class="who-k">Public adjuster</p><h3>Manages the whole claim</h3><ul><li>{ic("check")}Best early, from first notice</li><li>{ic("check")}Negotiated settlement</li><li>{ic("check")}Usually a percentage fee</li></ul></div>
<div class="who-card rv"><p class="who-k">Attorney</p><h3>Handles legal disputes</h3><ul><li>{ic("check")}Denials and coverage fights</li><li>{ic("check")}Unfair-practice claims</li><li>{ic("check")}Suit deadlines</li></ul></div>
</div>
</div></section>

<section class="sec sec-tint"><div class="wrap split split-top">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers on how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn btn-blue" href="{FAQ_P}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head sec-head-split rv"><div><p class="kicker">Claim insights</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on deductibles, tree claims, ice dams and reading estimates.</p></div><a class="btn btn-line" href="{POST_BASE}">All guides {ic("arrow")}</a></div>
<div class="pcards" data-stagger>{posts}</div>
</div></section>

<section class="cta-par"><div class="cta-par-media">{img("stormy-beach", "cta-par-img", alt="", extra=' data-parallax="0.25"')}</div><div class="wrap cta-par-in rv"><p class="kicker kicker-light">Before you sign off</p><h2>The cheapest time to question a settlement is before you accept it</h2><p>A short review now can keep you from closing a claim that won’t cover the repair.</p><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk with a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and tell you plainly whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 169 Connecticut towns</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", uid="hf")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Appraisal",
                        "Connecticut Insurance Appraiser: independent appraisal, estimate review and umpire help for underpaid tree, storm, ice and fire claims.",
                        body, [faq_schema(faqs)], preload="hero-saltbox", body_cls="is-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([(r["name"], svc_path(r)) for r in rel], "Service")}
</article>
{aside(call_box(), list_box("All services", items, path), list_box("Towns we serve", locs + [("All Connecticut towns", LOC_BASE)]))}</div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Connecticut"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{svc_path(s)}"><span class="icard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in Connecticut",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "hartford-office-tower") + f"""
<section class="sec"><div class="wrap"><div class="icards" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close right there.</p><a class="btn btn-blue" href="{SVC_BASE}insurance-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and association claims?", "Yes: offices, retail, mills, churches, condo associations and HOAs, as well as one- to four-family homes."), ("Which Connecticut perils do you see most?", "Fallen trees, ice dams, wind and hurricane damage, frozen pipes and fire, with hail in inland areas.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Connecticut | 12 Services",
                             "Insurance appraisal services in Connecticut: appraisal clause work, estimate review, tree, ice dam, storm, water and fire claims, and umpires.",
                             body, schema, preload="hartford-office-tower"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Towns", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f'Insurance Appraiser in {l["city"]}, CT', l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local-card"><div><p class="local-k">Neighborhoods</p><p>{e(l["neighborhoods"])}</p></div><div><p class="local-k">Housing mix</p><p>{e(l["housing"])}</p></div><div><p class="local-k">Common claim drivers</p><ul class="chips">{chips}</ul></div></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to owners in {e(l["city"])} and nearby towns, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby towns</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby")}
</article>
{aside(call_box(), list_box("Connecticut towns", items, path), list_box("Free claim tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and a few photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, CT", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Connecticut"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Towns", LOC_BASE)]
    towns = "".join(f'<a class="town rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], "town-img", sizes="(max-width:640px) 50vw, 25vw", alt="")}<span class="town-b"><h2 class="town-h">{e(l["city"])}</h2><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    regs = "".join(f'<div class="icard rv"><span class="icard-img">{img(ph, sizes="(max-width:640px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">{e(s)}</span><h3>{e(n)}</h3><p>{e(t)}</p></span></div>' for k, n, s, _p, t, ph in REGIONS)
    counties = "".join(f"<li>{c}</li>" for c in ["Fairfield", "Hartford", "Litchfield", "Middlesex", "New Haven", "New London", "Tolland", "Windham"])
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 169 Connecticut Towns",
                     f"{BRAND} works in every Connecticut town and city, from Greenwich to Thompson. These local pages cover the places our files come from most often.", "hartford-river") + f"""
<section class="sec"><div class="wrap"><div class="towns" data-stagger>{towns}</div></div></section>
<section class="sec sec-tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across Connecticut</h2><p>Connecticut abolished county government in 1960, but its eight counties, Fairfield, Hartford, Litchfield, Middlesex, New Haven, New London, Tolland and Windham, are still how most people describe where they live. The same policy reads very differently on the shoreline and in the hills.</p><ul class="chips chips-center">{counties}</ul></div><div class="icards" data-stagger>{regs}</div></div></section>
{cta_strip("Don’t see your town?", "We cover all 169. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraisal in All 169 Connecticut Towns",
                             "Insurance appraisal in all 169 Connecticut towns, including Hartford, New Haven, Stamford, Bridgeport, Waterbury, Norwalk and Danbury.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(f'{l["city"]}, CT', loc_path(l)) for l in LOCATIONS])], preload="hartford-river"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = tool_path(t)
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec sec-tool"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint tool-disc">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["name"], tool_path(o)) for o in others], "Tool")}</article>
{aside(call_box(), list_box("All claim tools", items, path))}</div>
{cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    tiles = "".join(f'<a class="tcard rv" data-tilt href="{tool_path(t)}"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}<span class="tcard-kind">{t["kind"]}</span></span><span class="tcard-b"><h2 class="tcard-h">{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    T = {t["slug"]: tool_path(t) for t in TOOLS}
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Connecticut",
                     "Seven calculators and planners built from real appraisal files. Use them to understand your claim and test the carrier’s math. No sign-up, and nothing is stored.", "calculator-laptop", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards" data-stagger>{tiles}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Start with the <a href="{T['claim-calendar-builder']}">claim calendar builder</a> so no deadline slips.</li><li>Check roof math with the <a href="{T['roof-square-pitch-converter']}">roof square and pitch converter</a>.</li><li>Had a tree come down? Use the <a href="{T['fallen-tree-claim-calculator']}">fallen tree claim calculator</a>.</li><li>See what you’ll actually receive with the <a href="{T['hurricane-deductible-calculator']}">hurricane deductible</a> and <a href="{T['rcv-acv-holdback-calculator']}">holdback</a> calculators.</li><li>Test the dispute with the <a href="{T['claim-gap-fee-estimator']}">claim gap and fee estimator</a>.</li><li>Finish with the <a href="{T['appraisal-readiness-checkup']}">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Connecticut",
                              "Free insurance claim calculators for Connecticut: gap and fee, RCV vs ACV, roof squares, hurricane deductible, tree claims and deadlines.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], preload="calculator-laptop"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Connecticut",
                     "Eight stages, from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "team-laptops",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Connecticut", "description": "The eight stages of a property insurance appraisal under a Connecticut policy.", "totalTime": "P10W",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{DOMAIN}{path}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Connecticut | 8 Steps",
                         "Connecticut insurance appraisal process in eight steps: the written demand, naming appraisers, the umpire, negotiation and the signed award.",
                         body, [crumbs_schema(trail), howto], preload="team-laptops"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    toc = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Connecticut Insurance Appraisal FAQ",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, costs, timing, Connecticut specifics and working with us.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="FAQ topics">{toc}</nav>{groups}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Connecticut Insurance Appraisal FAQ | Costs & Timing",
                         "Connecticut insurance appraisal FAQ grouped by topic: how appraisal works, costs, timing, state specifics and how we work with owners.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="g-row"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary for Connecticut",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the box to filter.", "calculator-hands", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “depreciation”, “umpire” or “ice dam”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl><p class="gloss-none" hidden>No terms match that search.</p></article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Connecticut property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path + "#definedtermset"} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More",
                         "Searchable insurance claim glossary for Connecticut owners: ACV, RCV, depreciation, umpire, hurricane deductible, ice dam and more defined.",
                         body, [crumbs_schema(trail), dts], preload="calculator-hands"), 0.7)

    for idx, p in enumerate(POSTS):
        path = post_path(p)
        trail = [("Home", "/"), ("Insights", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([(o["title"], post_path(o)) for o in others], "Guide")}</article>
{aside(call_box(), list_box("Resources", LEARN), list_box("Free tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US",
               "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Insights", path)]
    cards = "".join(f'<article class="pcard rv"><a class="pcard-img" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="pcard-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2 class="pcard-h"><a href="{post_path(p)}">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Claim insights", "Connecticut Property Claim Insights and Guides",
                     "Practical guides on hurricane deductibles, tree and ice dam claims, reading estimates and choosing the right help.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pcards" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Connecticut Property Claim Insights & Guides",
                         "Connecticut property claim guides: hurricane deductibles, fallen trees, ice dams, reading estimates and appraiser vs public adjuster choices.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(p["title"], post_path(p)) for p in POSTS])], preload="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We are estimators and appraisers who believe a property claim should be paid on what the damage really costs, documented clearly enough that everyone at the table can see it.", "consultation") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("victorian-home", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Plenty of claim professionals do a little of everything. {BRAND} works on one question, the amount of loss, and builds its process, tools and reporting around answering it well. That focus lets us serve as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible, not inflated.</strong> An inflated estimate costs credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reports.</strong> You will understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, association boards, property managers, business owners, churches, contractors, public adjusters and attorneys across Connecticut. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Built around Connecticut’s claims</h2>
<p>Connecticut’s weather and housing produce a distinctive mix of losses: trees through roofs after nor’easters, ice dams on plaster-walled colonials, shoreline wind on beach houses, and hail in the inland valleys. Working statewide means we price each with local knowledge, under the oversight framework set by the Connecticut Insurance Department.</p>
</article>{aside(call_box(), list_box("Explore", [("Our services", SVC_BASE), ("Connecticut towns", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, f"About {BRAND} | Our Approach",
                         "About Connecticut Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss on disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="consultation"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "team-laptops", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 169 Connecticut towns</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The carrier’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and any contractor estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, uid="cf")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | {PHONE}",
                         "Contact Connecticut Insurance Appraiser for a free review of a disputed claim. Call or text (844) 537-1427, or send your details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="team-laptops"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | Connecticut Insurance Appraiser",
                  "Privacy policy for Connecticut Insurance Appraiser: what we collect through forms and calls, how we use it, and the choices you have.",
                  "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share, such as your name, phone, email, property town and claim details. Our server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add site analytics, this policy will be updated to describe it.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you gave us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "Terms of Use | Connecticut Insurance Appraiser",
                "Terms of use for Connecticut Insurance Appraiser’s website, calculators and content, including limits on reliance and governing law.",
                "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Connecticut.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Connecticut attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Connecticut.</p>"""),
        DISCLAIM: ("Disclaimer", "Disclaimer | Connecticut Insurance Appraiser",
                   "Disclaimer for Connecticut Insurance Appraiser: general information only, not legal advice, illustrative figures and no guaranteed results.",
                   "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>This website is educational. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes them. If a deadline is near, consult a Connecticut attorney promptly.</p>
<h2>Legal references</h2><p>References to statutes such as the standard fire policy or CUIPA are general descriptions for context, not legal analysis. Verify current law and programs with official sources such as the Connecticut Insurance Department.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office-lobby", cta=False) + f'<div class="wrap layout"><article class="prose prose-narrow">{content}</article>{aside(call_box())}</div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], preload="office-lobby"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Towns", [("All towns", LOC_BASE)] + [(f'{l["city"]}, CT', loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="smap-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "office-lobby", cta=False) + f'<section class="sec"><div class="wrap smap" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}",
                         "Site map for Connecticut Insurance Appraiser: every service, Connecticut town page, free claim tool, guide and legal page on one list.",
                         body, [crumbs_schema(trail)], preload="office-lobby"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-media">{img("storm-sky", "phero-img", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-light">Error 404</p><h1>That page went down with the last nor’easter</h1><p class="phero-lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn btn-coral" href="/">Home</a><a class="btn btn-ghost-light" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-light" href="{TOOL_BASE}">Free tools</a><a class="btn btn-ghost-light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "This Connecticut Insurance Appraiser page could not be found. Use the links to reach our services, free claim tools or contact page.",
                                body, robots="noindex,follow"), sitemap=False)


# ---------------------------------------------------------------- root files
GUARD_PHP = r"""<?php
// Connecticut Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$cia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$cia_real  = 'connecticutinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$cia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://connecticutinsuranceappraiser.com - only on the real domain.
if ($cia_host === 'www.' . $cia_real || ($cia_host === $cia_real && $cia_proto === 'http')) {
    header('Location: https://' . $cia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$cia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($cia_uri, '?'), $cia_m)) {
    $cia_q = strpos($cia_uri, '?') !== false ? substr($cia_uri, strpos($cia_uri, '?')) : '';
    header('Location: ' . $cia_m[1] . $cia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($cia_host !== $cia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Connecticut Insurance Appraiser - front controller for the static build.
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
    # Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


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
