#!/usr/bin/env python3
"""Static site generator for minnesotainsuranceappraiser.com.

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

BRAND = "Minnesota Insurance Appraiser"
HOST = "minnesotainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster
# Google Tag Manager container, e.g. "GTM-XXXXXXX". Empty = no tag is printed.
GTM_ID = ""

SVC_BASE = "/appraisal-solutions/"
LOC_BASE = "/service-area/"
TOOL_BASE = "/free-tools/"
POST_BASE = "/learning-center/"
PROCESS = "/appraisal-process-guide/"
FAQ_P = "/common-questions/"
GLOSS = "/insurance-terms/"
ABOUT = "/who-we-are/"
CONTACT = "/contact-us/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, MN"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
ALT = {
    "mpls-stone-arch": "Downtown Minneapolis skyline seen from the Stone Arch Bridge over the Mississippi River",
    "mpls-skyline": "Aerial view of the downtown Minneapolis skyline above the Loring Park neighborhood",
    "stpaul-river": "St. Paul skyline lit at dusk above the Mississippi River",
    "stpaul-capitol": "Minnesota State Capitol building in St. Paul with autumn trees",
    "duluth-street": "Collapsed street pavement in Duluth, Minnesota, with a car caught in the washout",
    "duluth-harbor": "Duluth harbor and hillside neighborhoods along icy Lake Superior",
    "lake-superior-shore": "Rocky Lake Superior shoreline with pines along the water",
    "rochester-aerial": "Aerial view of downtown Rochester, Minnesota, along the Zumbro River",
    "north-mankato": "Aerial view of Mankato and North Mankato along the Minnesota River",
    "icicles-roof": "Close-up of long icicles hanging from a snow-covered roof edge",
    "winter-house-icicles": "Red wood house with heavy snow on the roof and icicles along the eaves",
    "snowy-rooftops": "Snow-covered roofs of a cluster of houses in winter",
    "cabin-snow": "Wood cabin in the woods with snow on the roof and smoke from the chimney",
    "winter-suburban": "Suburban two-story home and shrubs covered in fresh snow",
    "bungalow": "Craftsman-style bungalow with a front porch and tall trees",
    "townhomes": "Row of three-story brick townhomes with steep gables",
    "prairie-storm": "Dark storm clouds building over open farmland before a hailstorm",
    "barn-storm": "Old wooden barn under heavy storm clouds",
    "lightning-town": "Lightning bolts over a town during a night thunderstorm",
    "tornado-damage": "House crushed and stripped of siding after a tornado",
    "tornado-debris": "Neighborhood littered with debris and broken trees after a tornado",
    "flood-damaged-home": "Two-story house undermined by floodwater with its foundation exposed",
    "flooded-basement": "Mud-covered basement doorway after a flash flood",
    "rotted-eave": "Close-up of a damaged roof edge with deteriorated shingles and fascia",
    "roof-aerial": "Aerial view of a single-story home with a new shingle roof",
    "roofer": "Roofer’s hammer and tool belt resting on asphalt shingles",
    "fire-damaged-roof": "House with a burned-through tile roof after a fire",
    "firefighter-smoke": "Firefighter in breathing gear moving through thick smoke",
    "wildfire-smoke-lodge": "Wooded lodge and cabins under wildfire smoke near a forested hillside",
    "consultation": "Two people reviewing paperwork together at a wooden table",
    "consultation-laptop": "Two people reviewing documents and a laptop at a meeting table",
    "calculator-chart": "Calculator, printed charts and a laptop on a desk",
    "office-corner": "Corner of a modern glass office building against the sky",
    "living-room": "Bright living room with a sofa, coffee table and wood floors",
    "hail-damage-motel": "Commercial motel building and parking lot after a hailstorm",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-help": "consultation", "home-insurance-appraisal": "bungalow",
    "commercial-hoa-appraisal": "townhomes", "hail-roof-appraisal": "roof-aerial",
    "tornado-derecho-wind-appraisal": "tornado-damage", "water-damage-appraisal": "flooded-basement",
    "fire-smoke-appraisal": "fire-damaged-roof", "ice-dam-winter-damage-appraisal": "icicles-roof",
    "claim-estimate-review": "calculator-chart", "appraisal-umpire": "consultation-laptop",
    "contents-personal-property-appraisal": "living-room",
}
LOC_PHOTO = {
    "minneapolis": "mpls-stone-arch", "saint-paul": "stpaul-river", "rochester": "rochester-aerial", "duluth": "duluth-harbor",
    "bloomington": "winter-suburban", "plymouth": "roof-aerial", "woodbury": "townhomes", "eagan": "bungalow",
    "blaine": "tornado-debris", "st-cloud": "snowy-rooftops", "mankato": "north-mankato", "moorhead": "flood-damaged-home",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-chart", "rcv-acv-holdback-calculator": "rotted-eave",
    "roof-area-pitch-calculator": "roofer", "percentage-deductible-calculator": "prairie-storm",
    "claim-timeline-planner": "consultation", "appraisal-readiness-checkup": "consultation-laptop",
    "roof-snow-load-calculator": "winter-house-icicles",
}
POST_PHOTO = {
    "ice-dams-and-your-insurance-claim": "icicles-roof", "minnesota-appraisal-clause-and-causation": "stpaul-capitol",
    "hail-claim-checklist-for-minnesota-homes": "hail-damage-motel", "derecho-vs-tornado-wind-claims": "barn-storm",
    "choosing-appraiser-public-adjuster-or-attorney": "consultation-laptop", "when-appraisal-is-the-wrong-tool": "calculator-chart",
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
    "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "box": '<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ' class="i"'
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-clause-help": "doc", "home-insurance-appraisal": "home", "commercial-hoa-appraisal": "building",
    "hail-roof-appraisal": "hail", "tornado-derecho-wind-appraisal": "wind", "water-damage-appraisal": "drop",
    "fire-smoke-appraisal": "flame", "ice-dam-winter-damage-appraisal": "snow", "claim-estimate-review": "file",
    "appraisal-umpire": "scale", "contents-personal-property-appraisal": "box",
}


def mark(uid="m"):
    """Brand mark: navy tile, sky-blue roof line over a level bar (the 'measured' roof)."""
    return (f'<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#0b4a8f"/><stop offset="1" stop-color="#002d5d"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="11" fill="url(#{uid})"/>'
            '<path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#52c9e8" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15.5 33.5h17" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/>'
            '<circle cx="24" cy="33.5" r="3.6" fill="#f4a93b"/></svg>')


def brand(uid, cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark(uid)}<span class="brand-t"><b>Minnesota</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/web-app-manifest-512x512.png", "contentUrl": DOMAIN + "/web-app-manifest-512x512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "MN", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MN", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Minnesota’s 87 counties.",
        "areaServed": [{"@type": "State", "name": "Minnesota"}] + [{"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Minnesota"}} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Ice dams", "Derecho and tornado wind damage", "Xactimate estimating"],
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
    return {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Solutions", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal solutions", SVC_BASE), True),
        ("Service Area", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All of Minnesota", LOC_BASE), True),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Resources", [("Appraisal process guide", PROCESS), ("Common questions", FAQ_P), ("Insurance terms", GLOSS), ("Learning center", POST_BASE)], None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" two" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a class="top" href="{ABOUT}">About</a></li><li><a class="top" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap head-in">
{brand("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-act"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-sky btn-sm" href="{CONTACT}">Free claim review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm CT · All 87 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="wrap foot-band"><div><h2>Disputed claim? Get a straight read on the numbers.</h2><p>Free first conversation. We’ll tell you whether appraisal fits — or what does.</p></div><div class="btn-row"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Email your estimate</a></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("mf", "brand foot-brand")}
<p>Independent appraisal, estimate review and umpire services for Minnesota property owners — from the Red River Valley to the North Shore.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri, 8am–6pm Central</span></li></ul></div>
<div><h3>Solutions</h3><ul>{svc}<li><a href="{SVC_BASE}">All solutions</a></li></ul></div>
<div><h3>Service area</h3><ul class="two-col">{loc}</ul><p class="foot-more"><a href="{LOC_BASE}">All 87 counties</a></p></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Resources</h3><ul><li><a href="{PROCESS}">Appraisal process guide</a></li><li><a href="{FAQ_P}">Common questions</a></li><li><a href="{GLOSS}">Insurance terms</a></li><li><a href="{POST_BASE}">Learning center</a></li><li><a href="{ABOUT}">Who we are</a></li><li><a href="{CONTACT}">Contact us</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general information; policy language controls. Outcomes depend on the facts of each claim and are never guaranteed.</p>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/legal-disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="/html-sitemap/">Site map</a></li></ul></div></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free review</a></div>"""


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


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="mpls-skyline", main=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        if t in ("Service",):
            n["provider"] = {"@id": DOMAIN + "/#business"}
        nodes.append(n)
    p = PHOTOS[photo]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    ids = {n.get("@type"): n["@id"] for n in nodes if "@id" in n}
    target = None
    for t in (main or ()) or ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"):
        if t in ids:
            target = ids[t]
            break
    webpage["mainEntity"] = {"@id": target or DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Minnesota">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Minnesota">
<meta name="geo.region" content="US-MN">
<meta name="geo.placename" content="Minnesota">
<meta name="theme-color" content="#002d5d">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=Schibsted+Grotesk:wght@600;700;800&amp;display=swap">
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
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
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
    c = f'<div class="btn-row"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="sub-hero"><div class="sub-hero-ph" aria-hidden="true">{img(photo, lazy=False, alt="", extra=' data-parallax="0.18"')}</div><div class="wrap sub-hero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-t">Talk it through</h2><p>A free first conversation about your claim. No pressure, no obligation.</p><a class="side-tel" href="tel:{TEL}">{ic("phone")} {PHONE_INTL}</a><a class="btn btn-sky btn-block" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm Central</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-t">{e(title)}</h2><ul class="side-links">{li}</ul></div>'


def cta_strip(h="Not sure the settlement adds up?", p="Send us the insurer’s estimate and your photos. We’ll tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap"><div class="cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Send the estimate</a></div></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="sidebar"><div class="sticky">{aside}</div></aside></div>'


def related(cards):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in cards) + "</div>"


LOSSES = ["Hail", "Wind / tornado / derecho", "Ice dam / snow load", "Water / frozen pipe", "Fire / smoke", "Contents", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=3):
    roles = ["Homeowner", "Condo / townhome owner", "HOA / property manager", "Business owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Minnesota"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="lead-t">{e(heading)}</h{hlevel}><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer has paid or offered, and what you think is missing."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="/privacy/">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hero-form-t">Free claim review</h2><p class="lead-sub">Three details and we’ll call you back, usually within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="/privacy/">Privacy policy</a>.</span></label>
<button class="btn btn-navy btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hero-form-note">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("metro", "Twin Cities Metro", "Minneapolis · St. Paul · suburbs", ["Hail", "Ice dams", "Straight-line wind", "Condo & HOA losses"],
     "Seven counties, three generations of housing. Plaster-walled bungalows in Minneapolis and St. Paul, 1960s ramblers in the first-ring suburbs and townhome associations at the edges — often hit by the same spring hail line.",
     "Minneapolis, St. Paul, Bloomington, Plymouth, Woodbury, Eagan, Blaine", "mpls-skyline"),
    ("south", "Southern Minnesota", "Rochester · Mankato · Albert Lea", ["Tornadoes", "Derecho winds", "Hail", "Farm buildings"],
     "Open country lets severe storms organize. The March 1998 St. Peter and Comfrey tornadoes and the May 2022 derecho both tracked through this region, where claims mix homes, machine sheds and small-town commercial buildings.",
     "Rochester, Mankato, North Mankato, Owatonna, Faribault, Winona", "prairie-storm"),
    ("northeast", "Northeast & Arrowhead", "Duluth · North Shore · Iron Range", ["Heavy snow", "Frozen pipes", "Wildfire smoke", "Flash floods"],
     "Lake-effect snow, steep hillside lots and seasonal cabins define claims here. The June 2012 Duluth flood showed how quickly water can overwhelm older storm systems.",
     "Duluth, Hermantown, Two Harbors, Cloquet, Hibbing, Grand Marais", "duluth-harbor"),
    ("central", "Central Minnesota & Lakes", "St. Cloud · Brainerd lakes", ["Snow load", "Ice dams", "Fallen trees", "Cabin losses"],
     "Lake country means seasonal properties that sit empty for months — the classic setup for an undiscovered frozen pipe or a snow-loaded porch roof.",
     "St. Cloud, Sartell, Brainerd, Baxter, Little Falls, Alexandria", "cabin-snow"),
    ("west", "Red River Valley", "Moorhead · Fergus Falls", ["Spring flooding", "Blizzards", "Wind", "Hail"],
     "Flat terrain and a north-flowing river create a flood season unlike anywhere else in the state. Flood itself usually needs separate coverage, which makes sorting wind, water and flood damage a big part of claims here.",
     "Moorhead, Dilworth, Fergus Falls, Detroit Lakes, Crookston", "flood-damaged-home"),
]

SEASONS = [
    ("Winter", "Ice dams & snow load", "Meltwater backs up under shingles, pipes freeze in cabins and heavy snow tests older roofs.", "icicles-roof"),
    ("Spring", "Thaw & first hail", "Snowmelt finds every weak spot, and the first hail lines of the season roll through the metro and south.", "prairie-storm"),
    ("Summer", "Derechos & tornadoes", "Severe-weather season peaks: straight-line wind, tornadoes, hail and lightning fires.", "lightning-town"),
    ("Fall", "Wind & hidden damage", "Autumn storms and the last chance to find and document summer damage before snow covers the roof.", "barn-storm"),
]


def home():
    svc_cards = "".join(
        f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><div class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="card-num">{i + 1:02d}</span></div>'
        f'<div class="card-b"><span class="card-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></div></a>'
        for i, s in enumerate(SERVICES[:6]))
    svc_more = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{ic(SVC_ICON[s["slug"]])}<span>{e(s["name"])}</span></a></li>' for s in SERVICES[6:])

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{e(n)}</b><small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}><div class="region-ph">{img(ph, sizes="(max-width:900px) 100vw, 640px", alt="")}</div>'
        f'<div class="region-b"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in pr)}</ul><p>{e(t)}</p><p class="region-cities"><b>Communities:</b> {e(c)}</p></div></div>'
        for i, (k, n, _s, pr, t, c, ph) in enumerate(REGIONS))

    seasons = "".join(f'<div class="season rv"><div class="season-ph">{img(ph, sizes="(max-width:700px) 100vw, 300px", alt="")}</div><div class="season-b"><span class="season-k">{k}</span><h3>{e(t)}</h3><p>{e(d)}</p></div></div>' for k, t, d, ph in SEASONS)

    tools = "".join(f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><div class="tool-card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="tool-badge">{e(t["kind"])}</span></div><div class="tool-card-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></div></a>' for t in TOOLS)

    feat = LOCATIONS[:4]
    loc_feat = "".join(f'<a class="city rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 280px", alt="")}<span class="city-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in feat)
    loc_rest = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a></li>' for l in LOCATIONS[4:])

    posts = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="post-b"><p class="post-meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    steps = [
        ("Call & claim review", "We read the policy, the insurer’s estimate and your photos, then tell you plainly whether appraisal fits."),
        ("Independent inspection", "Our own measurements and photos, then a line-item estimate priced for your Minnesota ZIP code."),
        ("Written demand", "Appraisal is demanded in writing, and Minnesota Insurance Appraiser is named as your appraiser."),
        ("Appraiser-to-appraiser review", "We go line by line with the insurer’s appraiser. Many differences close at this stage."),
        ("Umpire & award", "Anything left goes to a neutral umpire. Signatures from two of the three set the amount of loss."),
    ]
    proc = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><div class="step-b rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))

    home_faqs = [
        ("What does a Minnesota Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent estimate, work with the insurer’s appraiser and, if needed, present the remaining items to an umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim and is licensed by the Minnesota Department of Commerce. An appraiser works within the policy’s appraisal clause on one question: the amount of loss."),
        ("When is it worth calling?", "When coverage is accepted, you have the insurer’s itemized estimate, and the gap to your contractor’s number is meaningful — often more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "An award signed by any two of the three panel members generally sets the amount of loss. It doesn’t decide coverage, which is why the file should be complete before appraisal starts."),
        ("Can appraisers decide what caused the damage?", "In Minnesota, the state Supreme Court’s 2012 Quade v. Secura decision held that appraisers may decide causation as part of the amount of loss, while coverage questions stay with the courts. How that applies depends on your policy and facts."),
        ("Do you work outside the Twin Cities?", "Yes. We work statewide in all 87 counties, including Rochester, Duluth, St. Cloud, Mankato and Moorhead."),
    ]

    body = f"""
<section class="hero">
<div class="hero-ph" aria-hidden="true">{img("mpls-skyline", lazy=False, alt="", extra=' data-parallax="0.25"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · All 87 counties</p>
<h1><span class="h1-main">Minnesota Insurance Appraiser</span><span class="h1-sub">for property claims that came up short</span></h1>
<p class="lede">Your insurer accepted the claim, but the payment won’t cover the repair. Minnesota Insurance Appraiser builds an independent, line-by-line valuation of the loss and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#solutions">See our solutions {ic("arrow")}</a></div>
<ul class="hero-points"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Hail, wind, ice dam, water &amp; fire</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="numbers" aria-label="At a glance"><div class="wrap"><div class="numbers-in">
<div class="num rv"><b data-count="87">87</b><span>Minnesota counties served</span></div>
<div class="num rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating solutions</span></div>
<div class="num rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim tools</span></div>
<div class="num rv"><b>2 of 3</b><span>Signatures that set the award</span></div>
</div></div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-ph rv">
<figure class="ph-a">{img("winter-house-icicles", sizes="(max-width:900px) 90vw, 460px")}</figure>
<figure class="ph-b">{img("roofer", sizes="(max-width:900px) 60vw, 300px")}</figure>
</div>
<div class="duo-b rv">
<p class="kicker">Covered isn’t the same as paid</p>
<h2>Why owners bring in a Minnesota Insurance Appraiser</h2>
<p>Most short claims aren’t denied — they’re underscoped. A missed roof slope, steel siding that can’t be matched, ice and water shield left off the eaves, an interior ceiling written as “paint only.” A Minnesota Insurance Appraiser exists for that gap between an accepted claim and a repair that’s actually funded.</p>
<ul class="ticks">
<li>{ic("check")}<div><b>Scope from scratch</b><span>We inspect and measure ourselves rather than editing the insurer’s estimate.</span></div></li>
<li>{ic("check")}<div><b>Numbers built to hold up</b><span>Every line is supported, so it carries weight with the other appraiser and the umpire.</span></div></li>
<li>{ic("check")}<div><b>Honest triage</b><span>If your claim needs an attorney, a supplement or nothing at all, we say so on the first call.</span></div></li>
</ul>
<a class="btn btn-navy" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div>
<div class="wrap fit">
<div class="fit-col yes rv"><h3>{ic("check")}Appraisal tends to fit</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair-versus-replace disagreements</li><li>Matching siding, shingles or flooring</li><li>Missing trades, code items, overhead &amp; profit</li></ul></div>
<div class="fit-col no rv"><h3>{ic("x")}It usually doesn’t</h3><ul><li>Full coverage denials</li><li>Bad-faith or other legal claims</li><li>Gaps too small to cover fees</li><li>Deadlines that need an attorney first</li></ul></div>
</div></section>

<section class="sec tint" id="solutions"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Appraisal solutions</p><h2>What Minnesota Insurance Appraiser handles</h2><p>{len(SERVICES)} services, one goal: a valuation of your loss that stands up. Start with an estimate review or bring us in once appraisal is demanded.</p></div>
<div class="cards" data-stagger>{svc_cards}</div>
<ul class="svc-more rv">{svc_more}</ul>
<p class="center"><a class="btn btn-line" href="{SVC_BASE}">Compare all solutions {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap process-wrap">
<div class="process-intro rv"><p class="kicker">The process</p><h2>From first call to a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result on the amount. Here is how Minnesota Insurance Appraiser moves a file through it.</p><a class="link" href="{PROCESS}">Read the full process guide {ic("arrow")}</a></div>
<ol class="steps" data-fill><span class="steps-line" aria-hidden="true"><span></span></span>{proc}</ol>
</div></section>

<section class="sec navy"><div class="wrap gap-split">
<div class="rv"><p class="kicker light">60-second gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. A large difference is worth a call to a Minnesota Insurance Appraiser; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees and shows your break-even point.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Five claim regions</p><h2>One state, very different claims</h2><p>Hail in Plymouth, derechos near Mankato, lake-effect snow in Duluth, floods along the Red River. A Minnesota Insurance Appraiser has to know how each region’s weather shows up on a building — and in an estimate.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="Minnesota regions">{tabs}</div><div class="region-panels">{panels}</div></div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">A year of claims</p><h2>Every Minnesota season brings its own losses</h2><p>We see the same patterns every year. Knowing which season your damage came from helps date it, scope it and defend it.</p></div>
<div class="seasons" data-stagger>{seasons}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free claim tools from a Minnesota Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser, and nothing you type is stored or sent.</p></div>
<div class="tool-cards" data-stagger>{tools}</div>
<p class="center"><a class="btn btn-line" href="{TOOL_BASE}">Open the tool library {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Service area</p><h2>Minnesota Insurance Appraiser service area</h2><p>We inspect in person across the state. These are the communities where we handle claims most often.</p></div>
<div class="city-row" data-stagger>{loc_feat}</div>
<ul class="city-list rv">{loc_rest}</ul>
<p class="center"><a class="link" href="{LOC_BASE}">See statewide coverage {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. The right one first saves time and fees — and Minnesota Insurance Appraiser will point you elsewhere when appraisal isn’t the tool.</p></div>
<div class="table-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Minnesota Insurance Appraiser</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Handle &amp; negotiate the claim</td><td>Legal disputes &amp; litigation</td></tr>
<tr><th scope="row">Best moment</th><td class="hl">Coverage accepted, amount disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Award signed by 2 of 3</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec tint"><div class="wrap faq-split">
<div class="rv"><p class="kicker">Questions</p><h2>Asked often of a Minnesota Insurance Appraiser</h2><p>Straight answers on how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_P}">All common questions {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Insurance terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Learning center</p><h2>Read this before you invoke appraisal</h2><p>Guides from the Minnesota Insurance Appraiser team on policy language, documentation and strategy.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="cta-photo"><div class="cta-photo-ph" aria-hidden="true">{img("lightning-town", alt="", extra=' data-parallax="0.2"')}</div><div class="wrap cta-photo-in rv"><p class="kicker light">Before you sign off</p><h2>Check the numbers before you accept them</h2><p>A short review now can keep you from settling for less than the repair costs.</p><div class="btn-row"><a class="btn btn-sky" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec navy" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker light">Start with a conversation</p><h2>Talk with a Minnesota Insurance Appraiser</h2><p>Tell us what happened and what the insurer offered. We’ll review it and tell you plainly whether appraisal is worth pursuing.</p>
<ul class="contact-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Central</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 87 Minnesota counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Minnesota Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, ice dam, water and fire claims.",
                        body, schema, photo="mpls-skyline", main=("__none__",), body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Solutions", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        art = f"""{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related solutions</h2>{related([("Solution", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}"""
        aside = call_box() + list_box("All solutions", items, path) + list_box("Service area", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All of Minnesota", LOC_BASE)])
        body = page_hero(trail, "Appraisal solution", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(art, aside) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "areaServed": {"@type": "State", "name": "Minnesota"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Solutions", SVC_BASE)]
    cards = "".join(f'<a class="row-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="row-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="row-b"><span class="row-k">{ic(SVC_ICON[s["slug"]])} Solution {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Solutions for Minnesota Property Claims",
                     "From a one-time estimate review to full appraisal panel representation and neutral umpire work, every Minnesota Insurance Appraiser solution centers on an accurate, defensible valuation of your loss.", "consultation") + f"""
<section class="sec"><div class="wrap"><div class="row-cards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Where to start</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review gives you that in days, and some disputes close right there.</p><a class="btn btn-navy" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and association claims?", "Yes — houses, cabins, condos and townhomes, apartment buildings, retail, office, churches and HOA properties."), ("Is hail the only peril you work on?", "No. We also handle wind, tornado and derecho, ice dam and snow load, water, fire and smoke, and contents claims.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Solutions in Minnesota | 11 Services",
                             "Minnesota insurance appraisal solutions: appraisal clause help, estimate review, hail, wind, ice dam, water, fire, contents and umpire services.",
                             body, schema, photo="consultation"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Service area", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = "".join(f"<li>{e(n)}</li>" for n in l["neighborhoods"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
        art = f"""<div class="local-card"><div><h2 class="local-t">Local claim snapshot</h2><dl class="local-dl"><div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Region</dt><dd>{e(l["region"])}</dd></div><div><dt>Housing</dt><dd>{e(l["housing"])}</dd></div><div><dt>Storm history</dt><dd>{e(l["storm"])}</dd></div></dl></div>
<div><p class="local-k">Common perils</p><ul class="chips">{chips}</ul><p class="local-k">Neighborhoods we inspect</p><ul class="chips soft">{hoods}</ul></div></div>
{l["body"]}
<h2>Appraisal solutions available in {e(l["city"])}</h2>
<p>Every {BRAND} solution is available to property owners in {e(l["city"])} and the surrounding communities, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}"""
        aside = call_box() + list_box("Service area", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                         [("County", l["county"]), ("Housing", l["housing"]), ("Notable storm", l["storm"])]) + layout(art, aside) + cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Minnesota"}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Service area", LOC_BASE)]
    cities = "".join(f'<a class="city rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 280px", alt="")}<span class="city-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="row-card static rv"><span class="row-ph">{img(ph, sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="row-b"><span class="row-k">{e(s)}</span><h2>{e(n)}</h2><p>{e(t)}</p><p class="row-meta">{e(c)}</p></span></div>' for k, n, s, _p, t, c, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 87 Minnesota Counties",
                     "Minnesota Insurance Appraiser works statewide, from the Iowa line to the Canadian border. These local pages cover the cities where we handle claims most often.", "stpaul-capitol") + f"""
<section class="sec"><div class="wrap"><div class="city-row all" data-stagger>{cities}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">Regions</p><h2>How claims differ across Minnesota</h2><p>The same policy language plays out very differently on a Duluth hillside, a Woodbury townhome and a Moorhead rambler.</p></div><div class="row-cards" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Minnesota county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Minnesota Insurance Appraiser Service Area | 87 Counties",
                             "Insurance appraisal in all 87 Minnesota counties, including Minneapolis, St. Paul, Rochester, Duluth, St. Cloud, Mankato and Moorhead.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="stpaul-capitol"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>""" + layout(
            f'{t["explain"]}<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>{related([(o["kind"], o["name"], f"{TOOL_BASE}{o["slug"]}/") for o in others])}',
            call_box() + list_box("All free tools", items, path)) + cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    tiles = "".join(f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><div class="tool-card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 300px", alt="")}<span class="tool-badge">{e(t["kind"])}</span></div><div class="tool-card-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></div></a>' for t in TOOLS)
    tl = lambda s, n: f'<a href="{TOOL_BASE}{s}/">{n}</a>'
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Minnesota Property Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work — including a roof snow load calculator for Minnesota winters. No sign-up, and nothing you enter is stored.", "calculator-chart", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-cards" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="order"><li>Start with the {tl("claim-timeline-planner", "claim timeline planner")} so no deadline slips.</li><li>Check roof measurements with the {tl("roof-area-pitch-calculator", "roof area &amp; pitch calculator")}.</li><li>See what you’re really owed with the {tl("percentage-deductible-calculator", "percentage deductible")} and {tl("rcv-acv-holdback-calculator", "RCV / ACV")} calculators.</li><li>Test the dispute with the {tl("claim-gap-fee-estimator", "claim gap &amp; fee estimator")}.</li><li>Finish with the {tl("appraisal-readiness-checkup", "appraisal readiness checkup")}.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Minnesota Owners",
                              "Free claim tools: appraisal cost, RCV/ACV, roof squares, percentage deductible and roof snow load calculators, a deadline planner and more.",
                              body, schema, photo="calculator-chart"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("Appraisal process guide", PROCESS), ("Common questions", FAQ_P), ("Insurance terms", GLOSS), ("Learning center", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process guide", path)]
    tl = "".join(f'<li><span>{i + 1}</span><div><b>{e(n)}</b><p>{e(d)}</p></div></li>' for i, (n, d) in enumerate(PROCESS_STEPS))
    art = f'<div class="mini-steps"><h2 class="local-t">The eight steps at a glance</h2><ol>{tl}</ol></div>{PROCESS_BODY}'
    body = page_hero(trail, "Process guide", "The Minnesota Insurance Appraisal Process, Step by Step",
                     f"{len(PROCESS_STEPS)} stages from the first disagreement to a signed award and payment — what happens, who does what, and where files most often stall.", "consultation-laptop",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Award", "Any 2 of 3 signatures")]) + layout(art, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Minnesota", "description": "The steps of a property insurance appraisal from first disagreement to signed award.", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Minnesota Insurance Appraisal Process | 8-Step Guide",
                         "Step-by-step guide to the Minnesota insurance appraisal process: the written demand, choosing appraisers and an umpire, and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="consultation-laptop"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Common questions", path)]
    jump = "".join(f'<a href="#q-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Common Questions About Insurance Appraisal in Minnesota",
                     "Plain answers grouped by topic — the basics, costs, timing, Minnesota rules and working with us.", "living-room") + layout(f'<nav class="jump" aria-label="Question topics">{jump}</nav>{groups}', call_box() + list_box("Resources", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")
    write(path, document(path, "Insurance Appraisal Questions | Minnesota Owners’ FAQ",
                         "Answers to common Minnesota insurance appraisal questions, grouped by topic: basics, costs and fees, timing, state rules and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Insurance terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms, Defined in Plain English",
                     f"A searchable glossary of {len(GLOSSARY)} words you’ll meet in Minnesota policies, estimates and appraisal awards.", "calculator-chart", cta=False) + layout(
        f'<div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"><p class="hint" id="gloss-count" aria-live="polite">{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="glossary">{dl}</dl>',
        call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Minnesota property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path + "#definedtermset"} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | Appraisal & Policy Terms",
                         f"Searchable glossary of {len(GLOSSARY)} property insurance terms: actual cash value, appraisal award, ice dam, matching, O&P, umpire and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-chart"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Learning center", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = f'<p class="byline">By the {BRAND} team · Published <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f"{POST_BASE}{o["slug"]}/") for o in others])}'
        body = page_hero(trail, f"Guide · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", LEARN) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        post = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "keywords": p.get("keyword", "")}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), post], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Learning center", path)]
    cards = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="post-b"><p class="post-meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    res = "".join(f'<a class="res-card rv" href="{u}"><b>{e(n)}</b><span>{d}</span>{ic("arrow")}</a>' for n, u, d in [("Appraisal process guide", PROCESS, "Eight steps from disagreement to award"), ("Common questions", FAQ_P, f"{sum(len(q) for _, q in FAQ)} answers in {len(FAQ)} topics"), ("Insurance terms", GLOSS, f"{len(GLOSSARY)} searchable definitions")])
    body = page_hero(trail, "Learning center", "Minnesota Insurance Appraisal Guides & Resources",
                     "Practical guides on policy language, documentation and claim strategy for Minnesota property owners, plus our process guide, FAQ and glossary.", "icicles-roof", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="res-row" data-stagger>{res}</div><div class="posts" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Appraisal Guides & Resources for Minnesota",
                         "Guides for Minnesota property owners on ice dam claims, hail documentation, derecho damage, causation in appraisal and choosing the right help.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="icicles-roof"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Who we are", path)]
    art = f"""<figure class="wide-ph">{img("consultation", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most claim professionals do a little of everything. {BRAND} chose to focus on the amount of loss — what it actually costs to put a damaged Minnesota property back the way it was. Our process, tools and documentation standards are built to answer that well, whether we serve as your appointed appraiser, review an estimate before a dispute grows, or sit as a neutral umpire.</p>
<h2>Principles we work by</h2>
<ul>
<li><strong>Inspect before we compare.</strong> We measure and photograph first, then look at the insurer’s numbers.</li>
<li><strong>Supportable beats impressive.</strong> An inflated estimate looks good for a day and loses credibility with the umpire. We price what we can defend.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Straight triage.</strong> If an attorney, a public adjuster or a simple supplement would serve you better, we’ll say so.</li>
<li><strong>Fees in writing first.</strong> You’ll know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, cabin owners, condo and townhome owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys. On any given claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t promise outcomes — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Minnesota’s claims change with the landscape: ice dams on St. Paul Victorians, hail on Plymouth two-stories, derecho damage near Mankato, frozen pipes in lake cabins, floods along the Red River. Working across all 87 counties means we see each of those losses often and price them with local knowledge.</p>"""
    body = page_hero(trail, "Who we are", f"About {BRAND}",
                     "Estimators and appraisers who believe a property claim should be paid on what the damage really costs — documented clearly enough that everyone at the table can see it.", "office-corner") + layout(art, call_box() + list_box("Explore", [("Appraisal solutions", SVC_BASE), ("Service area", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process guide", PROCESS)])) + cta_strip()
    write(path, document(path, f"About Us | {BRAND}",
                         "Minnesota Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="office-corner"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation-laptop", cta=False) + f"""
<section class="sec navy"><div class="wrap contact">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Central</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>Statewide — all 87 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ready-list"><li>Your declarations page</li><li>The insurer’s full, itemized estimate</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Get a free review of your disputed Minnesota property claim. Call or text (844) 537-1427, email us, or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation-laptop"), 0.8)

    lic = {"cc0": "CC0 1.0", "pdm": "Public domain"}
    credits = "".join(
        f'<tr><td>{img(k, "credit-th", sizes="120px", alt="")}</td><td>{e(v.get("title") or k.replace("-", " ").title())}<br><small>{e(v.get("creator") or "Unknown")} · {e(v["source"].title())}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    legal = {
        "/privacy/": ("Privacy Policy", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share — such as your name, phone, email, property location and claim details. Our server also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run entirely in your browser. What you enter isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP at any time to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        "/terms/": ("Terms of Use", f"""
<p><em>Last updated: {date.today().strftime("%B %-d, %Y")}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is provided for general information about insurance appraisal and property claims in Minnesota.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Minnesota attorney about legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Minnesota.</p>""", "The terms that apply when you use this website and its tools."),
        "/legal-disclaimer/": ("Disclaimer", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, don’t give legal advice, and don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, replacement-cost recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a Minnesota attorney promptly.</p>
<h2>Legal references</h2><p>Mentions of statutes, court decisions, agencies or storms are for context and are described in general terms. Verify current law with official sources such as the Minnesota Department of Commerce and the Minnesota Revisor of Statutes, and with an attorney.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. Not all were taken in Minnesota, and none show our clients’ properties.</p>""", "Important limits on the information published on this website."),
        "/photo-credits/": ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> (via StockSnap, rawpixel, Flickr and Wikimedia Commons) or a <strong>public-domain</strong> work such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative, not all were taken in Minnesota, and none show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", f"Sources and licenses for all {len(PHOTOS)} photographs used on this site."),
    }
    descs = {
        "/privacy/": "Privacy policy for Minnesota Insurance Appraiser: what we collect through forms and calls, how we use it, and how our claim tools keep data private.",
        "/terms/": "Terms of use for the Minnesota Insurance Appraiser website, its free claim tools and content, including the no-legal-advice and liability terms.",
        "/legal-disclaimer/": "Disclaimer for Minnesota Insurance Appraiser: general information only, no legal advice, illustrative figures, deadlines and photo notes.",
        "/photo-credits/": "Photo credits for Minnesota Insurance Appraiser: the source, creator and CC0 or public-domain license of every photograph on this website.",
    }
    for path, (title, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, e(lede), "office-corner", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", descs[path], body, [crumbs_schema(trail)], photo="office-corner"), 0.3)


def sitemap_pages():
    path = "/html-sitemap/"
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("Who we are", ABOUT), ("Contact us", CONTACT)]),
        ("Appraisal solutions", [("All solutions", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Service area", [("All of Minnesota", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy/"), ("Terms of use", "/terms/"), ("Disclaimer", "/legal-disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "mpls-stone-arch", cta=False) + f'<section class="sec"><div class="wrap"><div class="map-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", "A complete list of pages on Minnesota Insurance Appraiser: appraisal solutions, Minnesota service areas, free claim tools and guides.", body, [crumbs_schema(trail)], photo="mpls-stone-arch"), 0.3)

    body = f"""<section class="sub-hero"><div class="sub-hero-ph" aria-hidden="true">{img("snowy-rooftops", lazy=False, alt="")}</div><div class="wrap sub-hero-in"><p class="kicker">Error 404</p><h1>This page is buried under the snow</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-sky" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Solutions</a><a class="btn btn-line light" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found on Minnesota Insurance Appraiser.", body, robots="noindex,follow", photo="snowy-rooftops"), sitemap=False)


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
// Minnesota Insurance Appraiser - canonical host guard, required by index.php and every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'minnesotainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://minnesotainsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $mia_m)) {
    $mia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $mia_m[1] . $mia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Minnesota Insurance Appraiser - front controller for the static build.
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
