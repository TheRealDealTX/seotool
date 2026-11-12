#!/usr/bin/env python3
"""Static site generator for nevadainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Engineering pattern carried over from the sister-site template;
copy, slugs, layout and design are specific to this site.
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

BRAND = "Nevada Insurance Appraiser"
HOST = "nevadainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261109a"   # bump when CSS/JS change
FAV = "1"           # bump when icons change
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM output.
GTM_ID = "GTM-PDTLXWJ8"
# Head snippet exactly as supplied by the site owner (do not reformat).
GTM_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-PDTLXWJ8"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

SVC_BASE = "/appraisal/"
LOC_BASE = "/cities/"
TOOL_BASE = "/toolkit/"
POST_BASE = "/field-notes/"
P_PROCESS = "/appraisal-roadmap/"
P_FAQ = "/questions/"
P_GLOSS = "/claim-dictionary/"
P_ABOUT = "/our-story/"
P_CONTACT = "/get-in-touch/"
P_PRIVACY = "/privacy-notice/"
P_TERMS = "/website-terms/"
P_DISC = "/disclaimers/"
P_CREDITS = "/photo-credits/"
P_MAP = "/site-index/"
HOURS = "Mon–Fri 8am–6pm PT"
COUNTY_LINE = "16 counties + Carson City"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, NV"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "desert-storm-basin": "Storm clouds and a rain shaft over a wide sagebrush basin",
    "red-rock-escarpment": "Red Rock escarpment rising above desert scrub west of Las Vegas",
    "valley-of-fire-road": "Road winding through red sandstone in Valley of Fire State Park, Nevada",
    "vegas-valley-night": "Las Vegas Valley lights stretching to the mountains at dusk",
    "vegas-dusk-tower": "Las Vegas at dusk with the Strat tower and city lights",
    "vegas-valley-sunset": "Las Vegas Valley skyline under an orange sunset with mountains behind",
    "vegas-suburb-aerial": "Aerial view of curving subdivision streets in the Las Vegas Valley",
    "henderson-neighborhood": "Stucco homes with tile roofs along a street in Henderson, Nevada",
    "reno-arch": "The lit Reno arch sign over Virginia Street at night",
    "north-reno-hills": "Sagebrush hills and homes in north Reno, Nevada",
    "sparks-historic-house": "Historic white two-story Robison house in Sparks, Nevada",
    "tahoe-rocky-shore": "Clear water and granite boulders on Lake Tahoe’s shore with snowy peaks",
    "hoover-dam-aerial": "Aerial view of Hoover Dam and Lake Mead near Boulder City, Nevada",
    "mesquite-desert": "Desert scrub and mountains near Mesquite, Nevada",
    "aspen-creek": "Golden aspens along a rocky creek in the Ruby Mountains",
    "wild-horses": "Wild horses grazing on a sagebrush plain in Nevada",
    "desert-highway-mountains": "Desert highway curving toward red rock mountains in Southern Nevada",
    "desert-lightning": "Lightning striking desert mountains under a purple storm sky",
    "joshua-tree-storm": "Joshua tree silhouetted under a lightning-lit storm",
    "monsoon-rain-shaft": "Monsoon thunderstorm dropping a rain shaft over flat desert",
    "wildfire-night-ridge": "Wildfire glowing on a mountain ridge at night under heavy smoke",
    "burned-sagebrush": "Smoldering, burned sagebrush after a rangeland fire",
    "wildland-firefighter": "Wildland firefighter working beside tall flames",
    "snow-cabin": "Red mountain home with a heavy snow load on the roof",
    "icicles": "Icicles hanging from a frozen roof edge",
    "burned-building": "Fire-gutted building interior after a structure fire",
    "hailstones": "Large hailstones collected after a storm",
    "tile-roof-sky": "Clay S-tile roof against a deep blue sky",
    "clay-tile-rows": "Rows of terracotta roof tiles on a sloped roof",
    "roof-torn-wind": "Building with its roof torn open by high winds",
    "fallen-tree": "Large tree blown down across a driveway",
    "pipe-leak": "Water spraying from a leaking hose fitting",
    "flood-pump": "Crew pumping water out of a flooded residential street",
    "handshake-table": "Two people shaking hands across a meeting table",
    "meeting-laptop-notes": "Two people reviewing notes beside a laptop",
    "signing-papers": "Person reading and signing paperwork at a desk",
    "stressed-laptop": "Frustrated man with his head in his hands at a laptop",
    "calculator-pencil": "Calculator, pencil and sticky notes on a desk",
    "calculator-closeup": "Close-up of a calculator keypad",
    "drafting-plans": "Drafting tools on building plans",
    "office-towers": "Modern glass office towers against a blue sky",
    "condo-building": "Modern multi-story condominium building",
    "living-room": "Living room with a fireplace, sofas and a rug",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-help": "meeting-laptop-notes", "homeowner-claims": "henderson-neighborhood",
    "commercial-hoa-claims": "condo-building", "roof-hail-claims": "hailstones", "high-wind-claims": "roof-torn-wind",
    "monsoon-storm-claims": "monsoon-rain-shaft", "water-leak-claims": "pipe-leak", "fire-smoke-claims": "burned-building",
    "wildfire-claims": "wildfire-night-ridge", "snow-load-freeze-claims": "snow-cabin", "estimate-review": "calculator-pencil",
    "umpire-services": "handshake-table",
}
SVC_ICON = {
    "appraisal-clause-help": "doc", "homeowner-claims": "home", "commercial-hoa-claims": "building", "roof-hail-claims": "hail",
    "high-wind-claims": "wind", "monsoon-storm-claims": "storm", "water-leak-claims": "drop", "fire-smoke-claims": "flame",
    "wildfire-claims": "tree", "snow-load-freeze-claims": "snow", "estimate-review": "file", "umpire-services": "scale",
}
LOC_PHOTO = {
    "las-vegas": "vegas-dusk-tower", "henderson": "henderson-neighborhood", "north-las-vegas": "vegas-suburb-aerial",
    "boulder-city": "hoover-dam-aerial", "mesquite": "mesquite-desert", "pahrump": "wild-horses", "reno": "reno-arch",
    "sparks": "sparks-historic-house", "carson-city": "burned-sagebrush", "minden-gardnerville": "desert-highway-mountains",
    "incline-village": "tahoe-rocky-shore", "elko": "aspen-creek",
}
LOC_ALT = {  # page-specific alt text where a photo is generic rather than of the city itself
    "carson-city": "Burned sagebrush after a rangeland fire, the kind of wildland edge found above Carson City",
    "minden-gardnerville": "Desert highway curving toward the mountains, typical of Nevada valley country",
    "elko": "Golden aspens along a creek in the Ruby Mountains southeast of Elko",
    "pahrump": "Wild horses on a sagebrush plain, typical of the open valleys around Pahrump",
}
POST_PHOTO = {p["slug"]: p["photo"] for p in POSTS}
TOOL_PHOTO = {t["slug"]: t["photo"] for t in TOOLS}

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
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 4l3 3 3-3M9 20l3-3 3 3M4 9l3 3-3 3M20 9l-3 3 3 3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 19h.01M12 19h4"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


MARK_SVG = open(os.path.join(STATIC, "assets", "img", "mark.svg")).read() if os.path.exists(os.path.join(STATIC, "assets", "img", "mark.svg")) else ""


def mark():
    return '<span class="mark" aria-hidden="true">' + MARK_SVG.replace("<svg ", '<svg width="44" height="44" ', 1) + "</span>"


def brand(small="Independent claim appraisal"):
    return f'<a class="brand" href="/">{mark()}<span class="brand-t"><b>{BRAND}</b><small>{small}</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "NV", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-NV", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims throughout Nevada.",
        "areaServed": [{"@type": "State", "name": "Nevada"}] + [{"@type": "City", "name": c} for l in LOCATIONS for c in l["city"].split(" & ")],
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Tile roof claims", "Wildfire smoke damage", "Water and slab leak claims", "Snow load damage"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
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
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(_strip(a))}} for q, a in faqs]}


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


def _strip(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Nevada cities", LOC_BASE)),
        ("Toolkit", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE)),
        ("Resources", [("Appraisal roadmap", P_PROCESS), ("Questions & answers", P_FAQ), ("Claim dictionary", P_GLOSS), ("Field notes", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "ic chev")}</button><ul class="sub{wide}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">Our story</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{P_ABOUT}">Our story</a></li><li><a class="acc-link" href="{P_CONTACT}">Get in touch</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head" id="top"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-act"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-gold btn-sm" href="{P_CONTACT}">Free review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand()}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>{HOURS} · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Claim paid short? <span>Let’s check the numbers.</span></p><div class="btn-row"><a class="btn btn-ink" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ink-line" href="{P_CONTACT}">Send your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-brand">{brand()}
<p>Independent appraisal and estimating for Nevada property owners with disputed insurance claims, from the Las Vegas Valley to Lake Tahoe and Elko.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>{HOURS}</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul class="two">{loc}</ul></div>
<div><h2 class="foot-h">Toolkit</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{P_ABOUT}">Our story</a></li><li><a href="{P_CONTACT}">Get in touch</a></li><li><a href="{P_PROCESS}">Appraisal roadmap</a></li><li><a href="{P_FAQ}">Questions</a></li><li><a href="{P_GLOSS}">Claim dictionary</a></li><li><a href="{POST_BASE}">Field notes</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Site content is general information; your policy controls. Results depend on each claim’s facts and are never guaranteed. Photos are illustrative stock images.</p>
<div class="foot-bottom"><span>© {date.today().year} {BRAND}</span><ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimers</a></li><li><a href="{P_CREDITS}">Photo credits</a></li><li><a href="{P_MAP}">Site index</a></li></ul></div></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">Free claim review</a></div>"""


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
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "FAQPage", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="desert-storm-basin", main_entity=None):
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
    if main_entity:
        webpage["mainEntity"] = {"@id": main_entity}
    else:
        order = ["Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"]
        cands = sorted([n for n in extra if n.get("@type") in order], key=lambda n: order.index(n["@type"]))
        webpage["mainEntity"] = {"@id": cands[0]["@id"] if cands else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    p = PHOTOS[photo]
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className="js";(function(l){{if(l.hostname==="www.{HOST}"||(l.hostname==="{HOST}"&&l.protocol==="http:"))l.replace("https://{HOST}"+l.pathname+l.search+l.hash)}})(location);</script>
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Nevada">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Nevada">
<meta name="geo.region" content="US-NV">
<meta name="geo.placename" content="Nevada">
<meta name="theme-color" content="#211a0b">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,650;12..96,750&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True, alt=""):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-glass" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, "phero-img", lazy=False, alt=alt)}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary><span>{e(q)}</span>{ic("chev", "ic chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-h">Talk it through</h2><p>A free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="side-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def cta_strip(h="Insurer’s number doesn’t cover the repair?", p="Send us the estimate. We’ll read it line by line and tell you what we find."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-glass" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(items, label):
    return '<div class="related">' + "".join(f'<a class="rel" href="{p}"><small>{e(label)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for n, p in items) + "</div>"


LOSSES = ["Roof / hail", "Wind / microburst", "Monsoon / rain", "Water / slab leak", "Fire / smoke", "Wildfire / ash", "Snow / freeze", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=2, uid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "HOA board / manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Nevada"]
    h = f"h{hlevel}"
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{h} class="form-h">{e(heading)}</{h}><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property location</label><select id="{uid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>
<div class="full"><label for="{uid}-det">What happened, and where does the claim stand?</label><textarea id="{uid}-det" name="details" rows="4" placeholder="Date of loss, what the insurer paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See our <a href="{P_PRIVACY}">privacy notice</a>.</span></label></div>
<div class="full"><button class="btn btn-gold btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-h">Get a free claim review</h2><p class="form-sub">Three fields. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{P_PRIVACY}">Privacy notice</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
<p class="form-trust">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("south", "Las Vegas Valley", "Clark County", ["Monsoon storms", "Microbursts", "Tile roofs", "Slab leaks"],
     "About three of every four Nevadans live in Clark County, most of them in stucco homes with concrete tile roofs built since the 1980s. Extreme heat ages roofing fast, very hard water corrodes plumbing, and summer monsoon storms bring sudden wind, hail and flooding.",
     [("Las Vegas", "las-vegas"), ("Henderson", "henderson"), ("North Las Vegas", "north-las-vegas"), ("Boulder City", "boulder-city"), ("Mesquite", "mesquite")], "vegas-valley-sunset"),
    ("reno", "Reno–Sparks", "Washoe County", ["Wildfire & smoke", "Zephyr winds", "River floods", "Freeze"],
     "The Truckee Meadows sit where the Sierra meets the Great Basin. Foothill neighborhoods face wildfire, the Washoe Zephyr tests roofs every summer afternoon, and the Truckee River has flooded downtown Reno and Sparks more than once.",
     [("Reno", "reno"), ("Sparks", "sparks")], "north-reno-hills"),
    ("sierra", "Carson Valley & Lake Tahoe", "Carson City, Douglas & Washoe", ["Snow load", "Ice dams", "Wildfire", "Downslope wind"],
     "Nevada’s capital and the Carson Valley sit at the foot of the Carson Range; Lake Tahoe’s Nevada shore sits above them in heavy-snow country. Claims here involve fire at the wildland edge, winter snow loads and high-value mountain construction.",
     [("Carson City", "carson-city"), ("Minden & Gardnerville", "minden-gardnerville"), ("Incline Village", "incline-village")], "tahoe-rocky-shore"),
    ("rural", "Rural & Great Basin Nevada", "Nye, Elko & beyond", ["Extreme cold", "Rangeland fire", "Wind", "Earthquake"],
     "Most of Nevada’s land is open basin and range. In Pahrump, Elko and the towns between, homes sit on large lots with outbuildings and wells, winters can be brutal, and the 2008 Wells earthquake showed that the Great Basin can shake.",
     [("Pahrump", "pahrump"), ("Elko", "elko")], "wild-horses"),
]

EVENTS = [
    ("Jan 1997", "New Year’s flood", "The Truckee River floods downtown Reno and much of Sparks; the Carson River floods the Carson Valley."),
    ("Jul 1999", "Las Vegas Valley flash flood", "A severe monsoon storm floods neighborhoods across the valley."),
    ("Jul 2004", "Waterfall Fire", "Homes burn on Carson City’s west side."),
    ("Feb 2008", "Wells earthquake", "A magnitude 6.0 quake damages older masonry buildings in Elko County."),
    ("Nov 2011", "Caughlin Fire", "Wind-driven fire burns homes in southwest Reno, followed in January 2012 by the Washoe Drive Fire."),
    ("May 2020", "Monte Cristo Range earthquake", "Nevada’s largest earthquake in decades, magnitude 6.5, in west-central Nevada."),
    ("Jul 2022", "Monsoon flooding", "Intense storms send water through Las Vegas streets and buildings."),
    ("2022–23", "Heavy Sierra snow", "Deep snow loads damage roofs and decks around Lake Tahoe."),
    ("Aug 2023", "Tropical Storm Hilary", "Remnants bring heavy rain and wind across Southern Nevada."),
    ("Sep 2024", "Davis Fire", "Fire burns homes in Washoe Valley between Reno and Carson City."),
]


def home():
    K = BRAND
    perils = [("hail", "Tile & shingle roofs"), ("wind", "Wind & microbursts"), ("storm", "Monsoon storms"), ("tree", "Wildfire smoke"),
              ("drop", "Slab & pipe leaks"), ("snow", "Snow load & freeze"), ("flame", "Fire damage"), ("building", "Commercial & HOA")]
    ribbon = "".join(f'<li>{ic(i)}<span>{e(t)}</span></li>' for i, t in perils)
    scards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-media">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="pcard-body"><span class="pcard-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for s in SERVICES)
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{e(n)}</b><small>{e(sub)}</small></button>'
        for i, (k, n, sub, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<div class="region-media">{img(ph, sizes="(max-width:900px) 100vw, 55vw", alt="")}</div>'
        f'<div class="region-body"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in ps)}</ul><p>{e(t)}</p>'
        f'<p class="region-links">{" · ".join(f"<a href=\"{LOC_BASE}{s}/\">{e(c)}</a>" for c, s in cs)}</p></div></div>'
        for i, (k, n, _sub, ps, t, cs, ph) in enumerate(REGIONS))
    steps = [
        ("Free review", "We read your policy, the insurer’s estimate and your photos, then tell you plainly whether appraisal fits."),
        ("Independent scope", "We inspect, measure and build a line-item estimate priced for your part of Nevada."),
        ("Written demand", "Appraisal is demanded in writing and we are named as your appraiser within the policy’s time frame."),
        ("Panel work", "We work line by line with the insurer’s appraiser. Most disputes narrow sharply here."),
        ("Signed award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="step rv"><span class="step-n">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    events = "".join(f'<li class="rv"><time>{e(d)}</time><div><b>{e(t)}</b><span>{e(x)}</span></div></li>' for d, t, x in EVENTS)
    tcards = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-media">{img(t["photo"], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="tag">{e(t["kind"])}</span></span>'
        f'<span class="tcard-body"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    ctiles = "".join(
        f'<a class="ctile rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, (max-width:1100px) 33vw, 25vw", alt="")}<span class="ctile-t"><b>{e(l["city"])}</b><small>{e(l["county"].split(" (")[0])}</small></span></a>'
        for l in LOCATIONS)
    posts = "".join(post_card(p, "h3") for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree a loss is covered but disagree on what it costs. As your appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is that different from a public adjuster?", "A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the insurer’s estimate and the gap between it and your contractor’s number is meaningful, generally more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign. That is why documentation matters so much before appraisal is demanded."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you work outside Las Vegas and Reno?", f"Yes. We work in all {COUNTY_LINE}, including Carson City, the Carson Valley, Lake Tahoe, Pahrump, Mesquite and Elko."),
    ]
    h1w = f'{K} <span class="h1-sub">for claims that came up short</span>'
    body = f"""
<section class="hero">
<div class="hero-media">{img("desert-storm-basin", "hero-img", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent claim appraisal · Statewide</p>
<h1>{h1w}</h1>
<p class="lede">Your insurer accepted the claim, but the check won’t cover the repair. {K} builds an independent, line-by-line valuation of the damage and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-glass" href="#services">See our services {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Your named appraiser</li><li>{ic("check")}Tile, smoke &amp; snow-load expertise</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ribbon" aria-label="Claims we value"><div class="wrap"><ul class="ribbon-list">{ribbon}</ul></div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-text rv">
<p class="kicker dark">The short version</p>
<h2>What a {K} actually does</h2>
<p>Most underpaid claims are not denials. They are short: a tile roof priced as a patch, a smoke claim reduced to a wipe-down, a slab leak with no allowance for the floor. {K} exists for the gap between “covered” and “paid in full.”</p>
<p>When the appraisal clause is invoked, each side names an appraiser. As your {K}, we inspect the property ourselves, price every line for your area and defend that number in front of the insurer’s appraiser and, if needed, a neutral umpire.</p>
<ul class="ticklist"><li>{ic("check")}<span><b>We start from scratch.</b> Our own measurements, not an edited copy of the insurer’s estimate.</span></li><li>{ic("check")}<span><b>Defensible, not inflated.</b> Numbers built to survive an umpire’s review.</span></li><li>{ic("check")}<span><b>Straight answers.</b> If your claim needs an attorney or a supplement instead, we say so on the first call.</span></li></ul>
<a class="btn btn-ink" href="{P_ABOUT}">Read our story {ic("arrow")}</a>
</div>
<div class="duo-media rv">{img("meeting-laptop-notes", "duo-a", sizes="(max-width:900px) 90vw, 440px")}{img("tile-roof-sky", "duo-b", sizes="(max-width:900px) 60vw, 300px")}</div>
</div></section>

<section class="counters" aria-label="By the numbers"><div class="wrap counters-in">
<div><b data-count="17">17</b><span>County-level jurisdictions served: 16 counties plus Carson City</span></div>
<div><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal and estimating services</span></div>
<div><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim tools that run in your browser</span></div>
<div><b>2 of 3</b><span>Panel signatures that make an award binding</span></div>
</div></section>

<section class="sec sand" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Services</p><h2>How {K} helps with your claim</h2><p>Twelve services built around one job: a valuation of your loss that holds up. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="pcards" data-stagger>{scards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Four claim climates</p><h2>One state, very different losses</h2><p>A {K} has to know how a monsoon microburst in Henderson differs from a snow load in Incline Village or a smoke claim in southwest Reno, and how each one shows up in an estimate.</p></div>
<div class="regions" data-tabs><div class="region-tabs" role="tablist" aria-label="Nevada regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec gold-tint" id="gap"><div class="wrap duo">
<div class="duo-text rv"><p class="kicker dark">Quick check</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a call with a {K} makes sense. If it is small, a documented supplement request may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}claim-gap-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees and shows your break-even point.</p><a class="btn btn-ink" href="{TOOL_BASE}">Open the toolkit {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">The process</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how {K} moves a file through it.</p></div>
<ol class="steps" data-stagger>{proc}</ol>
<p class="center"><a class="link" href="{P_PROCESS}">Read the full appraisal roadmap {ic("arrow")}</a></p>
</div></section>

<section class="sec indigo"><div class="wrap duo top">
<div class="duo-text rv"><p class="kicker">Nevada’s loss record</p><h2>The events behind Nevada claims</h2><p>Floods on the Truckee, monsoon storms in the Las Vegas Valley, fires along the Sierra front and earthquakes in the Great Basin. Every {K} file is shaped by this history, because insurers ask about prior damage and appraisers have to separate old from new.</p><p class="small">Dates and descriptions are summarized from public records for context.</p></div>
<ol class="events" data-stagger>{events}</ol>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Free &amp; private</p><h2>Claim tools from a {K}</h2><p>Run the numbers before you pick up the phone. Every tool works in your browser; nothing is stored or sent.</p></div>
<div class="tcards" data-stagger>{tcards}</div>
<p class="center"><a class="btn btn-ink" href="{TOOL_BASE}">See all seven tools {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Statewide</p><h2>{K} in your city</h2><p>We work in every Nevada county. These are the communities where {K} handles claims most often.</p></div>
<div class="ctiles" data-stagger>{ctiles}</div>
<p class="center"><a class="link" href="{LOC_BASE}">All Nevada cities {ic("arrow")}</a></p>
</div></section>

<section class="sec sand"><div class="wrap fit">
<div class="fit-card yes rv"><h2>{ic("check")} When appraisal fits</h2><ul><li>Coverage accepted, cost disputed</li><li>Repair-or-replace arguments on tile, stucco or flooring</li><li>Smoke cleaning scope too thin</li><li>Missing trades, code items or overhead and profit</li></ul></div>
<div class="fit-card no rv"><h2>{ic("x")} When it doesn’t</h2><ul><li>Outright coverage denials</li><li>Bad-faith or other legal claims</li><li>Gaps too small to justify fees</li><li>Lawsuit deadlines that need an attorney now</li></ul></div>
</div></section>

<section class="sec"><div class="wrap duo top">
<div class="duo-text rv"><p class="kicker dark">Questions</p><h2>What people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn btn-ink" href="{P_FAQ}">All questions {ic("arrow")}</a><a class="btn btn-line-dark" href="{P_GLOSS}">Claim dictionary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Field notes</p><h2>Read before you demand appraisal</h2><p>Practical guides from {K} on policy wording, documentation and Nevada-specific claims.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="pcta"><div class="pcta-media" data-parallax>{img("vegas-valley-night", "pcta-img", alt="")}</div><div class="wrap pcta-in rv"><p class="kicker">Before you sign off</p><h2>The best time to check the numbers is before you accept them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-glass" href="#contact">Send your estimate</a></div></div></section>

<section class="sec dark" id="contact"><div class="wrap duo top">
<div class="duo-text rv"><p class="kicker">Start a conversation</p><h2>Talk with a {K}</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure, no obligation.</p>
{contact_lines()}</div>
<div class="rv">{lead_form(page="/", hlevel=3, uid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Appraisal",
                        "Nevada Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid roof, wind, water, smoke and fire claims.",
                        body, [faq_schema(home_faqs)], photo="desert-storm-basin", main_entity=DOMAIN + "/#business"), 1.0)


def contact_lines():
    return f"""<ul class="clines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>{HOURS}</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All of Nevada: {COUNTY_LINE}</b></div></li></ul>"""


def post_card(p, h="h2"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="post-media" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a>'
            f'<div class="post-body"><p class="meta">{nice} · {p["read"]} read</p><{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>')


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about this service</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([(r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel], "Service")}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Nevada cities", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]] + [("All cities", LOC_BASE)])}</aside></div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Nevada"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-media">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="pcard-body"><span class="pcard-ic">{ic(SVC_ICON[s["slug"]])}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Nevada",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "drafting-plans") + f"""
<section class="sec"><div class="wrap"><div class="pcards" data-stagger>{cards}</div></div></section>
<section class="sec sand"><div class="wrap duo top"><div class="duo-text rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review gives you that answer in days, and many disputes end there.</p><a class="btn btn-ink" href="{SVC_BASE}estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one step?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, condos, rentals, HOAs, retail, office, industrial and multifamily properties."), ("Which perils do you handle?", "Wind, hail, monsoon rain, water, fire, wildfire smoke, snow load, freeze and other covered perils.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Nevada | 12 Services",
                             "Nevada insurance appraisal services: appraisal clause representation, estimate review, tile roof, wind, water, smoke, snow load and umpire work.",
                             body, schema, photo="drafting-plans"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"].split(",")[0])], alt=LOC_ALT.get(l["slug"], "")) + f"""
<div class="wrap layout"><article class="prose">
<div class="local-box"><h2 class="local-h">Local claim risks in {e(l["city"])}</h2><ul class="chips">{chips}</ul><p><b>Housing mix:</b> {e(l["housing"])}.</p></div>
{l["body"]}
<h2>Services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the surrounding area, including:</p>
<ul class="cols">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby areas</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby")}
</article>
<aside class="aside">{call_box()}{list_box("Nevada cities", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        cities = [c for c in l["city"].split(" & ")]
        area = [{"@type": "City", "name": c, "containedInPlace": {"@type": "State", "name": "Nevada"}} for c in cities]
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": area if len(area) > 1 else area[0], "url": DOMAIN + path}]
        title = f"{l['city']} Insurance Appraiser | Claim Appraisal NV"
        if len(title) > 58:
            title = f"{l['city']}, NV Insurance Appraiser"
        desc = f"Independent insurance appraiser for {l['city']} and {l['county'].split(' (')[0]}: appraisal and estimate review for underpaid storm, water, fire and smoke claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {l['city']}, Nevada: appraisal and estimate review for underpaid storm, water, fire and smoke claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    tiles = "".join(
        f'<a class="ctile rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, (max-width:1100px) 33vw, 25vw", alt="")}<span class="ctile-t"><b>{e(l["city"])}</b><small>{e(l["county"].split(" (")[0])}</small></span></a>'
        for l in LOCATIONS)
    reg = "".join(f'<div class="rcard rv">{img(ph, sizes="(max-width:640px) 100vw, 50vw", alt="")}<div class="rcard-b"><h2>{e(n)}</h2><p class="meta">{e(sub)}</p><p>{e(t)}</p><p class="region-links">{" · ".join(f"<a href=\"{LOC_BASE}{s}/\">{e(c)}</a>" for c, s in cs)}</p></div></div>' for k, n, sub, _p, t, cs, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in Every Nevada County",
                     f"{BRAND} works statewide, in all {COUNTY_LINE}. These pages cover the communities where we handle claims most often, with local risks, neighborhoods and housing.", "valley-of-fire-road") + f"""
<section class="sec"><div class="wrap"><div class="ctiles" data-stagger>{tiles}</div></div></section>
<section class="sec sand"><div class="wrap"><div class="sec-head rv"><p class="kicker dark">Regions</p><h2>How claims differ across Nevada</h2><p>The same policy wording plays out very differently in a Summerlin tract home, a Washoe Valley ranch house and an Incline Village chalet.</p></div><div class="rcards" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover all of Nevada. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Nevada Cities We Serve | Statewide Claim Appraisal",
                             "Insurance appraisal in all 16 Nevada counties and Carson City, including Las Vegas, Henderson, Reno, Sparks, Carson City, Lake Tahoe and Elko.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="valley-of-fire-road"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Toolkit", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = t["photo"]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint tool-note">For planning only. Results depend on what you enter and your policy’s terms. They are not a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others], "Tool")}</article>
<aside class="aside">{call_box()}{list_box("The toolkit", items, path)}</aside></div>
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Toolkit", TOOL_BASE)]
    cards = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-media">{img(t["photo"], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="tag">{e(t["kind"])}</span></span>'
        f'<span class="tcard-body"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Nevada Property Owners",
                     "Seven calculators, planners and checklists built from real appraisal work. Use them to understand your claim, check the insurer’s math and decide on next steps. No sign-up, nothing stored.", "calculator-closeup", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards" data-stagger>{cards}</div></div></section>
<section class="sec sand"><div class="wrap duo top"><div class="duo-text rv"><p class="kicker dark">Suggested order</p><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a> so nothing lapses.</li><li>Check roof measurements with the <a href="{TOOL_BASE}roof-squares-tile-calculator/">roof squares &amp; tile calculator</a>.</li><li>See what you are actually owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a> and <a href="{TOOL_BASE}depreciation-recovery-calculator/">depreciation recovery</a> calculators.</li><li>For wildfire or house-fire smoke, build a scope with the <a href="{TOOL_BASE}smoke-ash-cleaning-estimator/">smoke &amp; ash cleaning estimator</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}claim-gap-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-file-scorecard/">appraisal file scorecard</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Tools for Nevada | Toolkit",
                              "Seven free claim tools: gap and fee estimator, depreciation, roof squares and tile, deductibles, a deadline calendar, a scorecard and a smoke scope.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo="calculator-closeup"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("Appraisal roadmap", P_PROCESS), ("Questions & answers", P_FAQ), ("Claim dictionary", P_GLOSS), ("Field notes", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal roadmap", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _p) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "The Nevada Insurance Appraisal Roadmap, Step by Step",
                     "Seven steps from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", "signing-papers",
                     [("Steps", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="Steps"><p class="toc-h">On this page</p><ol>{toc}</ol></nav>{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Nevada", "description": "Seven steps from the first disagreement to a signed appraisal award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Nevada Insurance Appraisal Roadmap | 7 Steps",
                         "Step-by-step guide to insurance appraisal in Nevada: the written demand, naming appraisers, umpire selection, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="signing-papers"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Questions", path)]
    jump = "".join(f'<li><a href="#faq-{i}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions from Nevada Property Owners",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, costs, timing, Nevada specifics and working with us.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="Topics"><p class="toc-h">Topics</p><ol>{jump}</ol></nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal Questions & Answers | Nevada",
                         "Answers to common Nevada insurance appraisal questions, grouped by topic: how it works, costs, timing, earthquake and FAIR plan questions, and more.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim dictionary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Property Insurance Claim Dictionary",
                     f"{len(GLOSSARY)} terms you will see in policies, estimates and appraisal awards, defined in plain English, with a few that are specific to Nevada.", "calculator-pencil", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the dictionary</label><input id="gloss-filter" type="search" placeholder="Try “underlayment” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim dictionary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Claim Dictionary | ACV, RCV, Umpire & Nevada Terms",
                         "Plain-English definitions of property claim terms: actual cash value, replacement cost, depreciation, appraisal award, umpire, underlayment and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-pencil"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Field notes", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = p["photo"]
        body = page_hero(trail, f"Field note · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<p class="byline">Written by the {BRAND} team · Updated {nice}</p><h2>Keep reading</h2>{related([(o["title"], f'{POST_BASE}{o["slug"]}/') for o in others], "Field note")}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "inLanguage": "en-US"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Field notes", path)]
    cards = "".join(post_card(p) for p in POSTS)
    body = page_hero(trail, "Guides", "Field Notes: Insurance Appraisal Guides for Nevada",
                     "Practical guides on policy wording, documentation and Nevada claims: tile roofs, wildfire smoke, monsoon water, earthquakes and choosing the right help.", "stressed-laptop", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Field Notes | Nevada Insurance Appraisal Guides",
                         "Guides for Nevada property owners on appraisal clauses, tile roof claims, wildfire smoke, monsoon water damage, earthquakes and choosing help.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="stressed-laptop"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("Our story", path)]
    body = page_hero(trail, "Our story", "About Nevada Insurance Appraiser",
                     "We are estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "handshake-table") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("drafting-plans", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we only do appraisal</h2>
<p>Most claim professionals do a bit of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your named appraiser, review estimates before a dispute escalates or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate looks good on day one and loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You will understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so.</li>
<li><strong>Fees in writing.</strong> You know what it costs before work starts.</li>
</ul>
<h2>Built for Nevada’s claims</h2>
<p>Nevada packs very different climates into one state. Concrete tile and stucco dominate the Las Vegas Valley, where heat and hard water drive roof and plumbing claims. Reno, Carson City and the Carson Valley sit at the wildland edge. Lake Tahoe’s Nevada shore is heavy-snow country, and rural towns like Pahrump and Elko have their own construction and coverage quirks. Working statewide means we see all of it and price each loss with local knowledge.</p>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, business owners, contractors, public adjusters and attorneys across Nevada. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t guarantee outcomes, and no honest appraiser can. We don’t publish testimonials or claim results; every claim is different.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Nevada cities", LOC_BASE), ("Free toolkit", TOOL_BASE), ("Appraisal roadmap", P_PROCESS)])}</aside></div>{cta_strip()}"""
    write(path, document(path, "Our Story | Nevada Insurance Appraiser",
                         "Nevada Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed Nevada property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="handshake-table", main_entity=DOMAIN + "/#business"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Get in touch", path)]
    body = page_hero(trail, "Get in touch", "Contact Nevada Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we will tell you honestly whether appraisal is likely to help.", "meeting-laptop-notes", cta=False) + f"""
<section class="sec dark"><div class="wrap duo top">
<div class="duo-text rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>{contact_lines()}
<h3>Helpful to have ready</h3><ul class="plain"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form(page=path, uid="k")}</div></div></section>"""
    write(path, document(path, "Contact Us | Nevada Insurance Appraiser (844) 537-1427",
                         "Get a free review of your disputed Nevada property claim. Call or text (844) 537-1427 or email info@nevadainsuranceappraiser.com.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="meeting-laptop-notes", main_entity=DOMAIN + "/#business"), 0.8)

    lic = {"cc0": "CC0 1.0", "pdm": "Public domain"}
    credits = "".join(
        f'<tr><td>{img(k, "thumb", sizes="120px", alt="")}</td><td>{e(v["title"] or k)}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{lic.get(v["license"], v["license"])}</td><td>{e(v["source"].capitalize())}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Notice", "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to give us, such as your name, phone number, email, property location and claim details. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators, planners and checklists run in your browser. What you type isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, we will update this notice.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the information you have given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        P_TERMS: ("Website Terms", "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Nevada.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ and laws change. Consult a licensed Nevada attorney about legal questions.</p>
<h2>Tools and figures</h2><p>Calculators give planning estimates based on what you enter. Example figures are illustrative. Nothing here is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photos are used under the licenses listed on our <a href="{P_CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Nevada.</p>"""),
        P_DISC: ("Disclaimers", "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>This site describes how insurance appraisal commonly works. Your policy’s wording controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>Legal references</h2><p>Mentions of Nevada’s unfair claims practices rules, bad-faith law or other legal topics are general descriptions, not statements of how the law applies to your situation. Verify current law with a Nevada attorney or the Nevada Division of Insurance.</p>
<h2>No guarantees, no testimonials</h2><p>Every claim is different. Example figures on this site are illustrative, not results for any client. We don’t publish reviews or claim outcomes, and no appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a Nevada attorney promptly.</p>
<h2>Weather and event history</h2><p>References to storms, fires, floods and earthquakes summarize public information for context. Details may be simplified.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties, and a photo on a city page may show a nearby or similar landscape rather than that exact city.</p>"""),
        P_CREDITS: ("Photo Credits", "Sources and licenses for every photograph used on this site.", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work. We found them through the Openverse search engine; most come from rawpixel, StockSnap and Wikimedia Commons. Attribution isn’t legally required, but we credit sources here. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Via</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    photo_for = {P_PRIVACY: "office-towers", P_TERMS: "office-towers", P_DISC: "office-towers", P_CREDITS: "red-rock-escarpment"}
    descs = {
        P_PRIVACY: "Privacy notice for Nevada Insurance Appraiser: what we collect through forms, calls and email, how we use it, and the choices you have.",
        P_TERMS: "Website terms for Nevada Insurance Appraiser: no client relationship or legal advice from site use, illustrative tool figures and Nevada law.",
        P_DISC: "Disclaimers for Nevada Insurance Appraiser: general information only, no legal advice, no guarantees or testimonials, and deadline cautions.",
        P_CREDITS: "Photo credits for Nevada Insurance Appraiser: every photo used on the site with its CC0 or public-domain license, creator and original source.",
    }
    for path, (title, lede, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, photo_for[path], cta=False) + f'<div class="wrap layout"><article class="prose{" wide" if path == P_CREDITS else ""}">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", descs[path], body, [crumbs_schema(trail)], photo=photo_for[path], main_entity=DOMAIN + "/#business"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site index", path)]
    groups = [
        ("Main", [("Home", "/"), ("Our story", P_ABOUT), ("Get in touch", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Toolkit", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy notice", P_PRIVACY), ("Website terms", P_TERMS), ("Disclaimers", P_DISC), ("Photo credits", P_CREDITS)]),
    ]
    cols = "".join(f'<div class="index-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    allp = [x for _, links in groups for x in links]
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on {BRAND}, grouped by section.", "red-rock-escarpment", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-cols" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"A complete index of every page on {BRAND}: appraisal services, Nevada cities, free claim tools, resources and site information.", body, [crumbs_schema(trail), itemlist(allp)], photo="red-rock-escarpment"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-media">{img("joshua-tree-storm", "phero-img", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page is lost somewhere in the basin</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-glass" href="{SVC_BASE}">Services</a><a class="btn btn-glass" href="{TOOL_BASE}">Free tools</a><a class="btn btn-glass" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on Nevada Insurance Appraiser. Try the home page, services, free tools or contact page.", body, robots="noindex,follow", photo="joshua-tree-storm"), sitemap=False)


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
// Nevada Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$real = '__HOST__';

// Canonical host and scheme: only on the real domain (TLS terminates upstream, so trust X-Forwarded-Proto).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ? 'https' : 'http'));
if ($host === 'www.' . $real || ($host === $real && $proto === 'http')) {
    header('Location: https://' . $real . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== $real) {
    header('X-Robots-Tag: noindex, nofollow');
}
if (strpos($path, '..') !== false) { $path = '/'; }

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    $q = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    header('Location: ' . $path . '/' . $q, true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex');
readfile(__DIR__ . '/404.html');
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private"))
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
