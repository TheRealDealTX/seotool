#!/usr/bin/env python3
"""Static site generator for arizonainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
Engineering derived from georgiainsuranceappraiser/; copy, slugs and design are new.
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

BRAND = "Arizona Insurance Appraiser"
HOST = "arizonainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261109a"   # bump when CSS/JS change
FAV = "1"           # bump when icons change

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""

SVC_BASE = "/appraisal/"
LOC_BASE = "/cities/"
TOOL_BASE = "/claim-calculators/"
POST_BASE = "/articles/"
PROCESS = "/appraisal-roadmap/"
FAQ_P = "/questions/"
GLOSS = "/claim-dictionary/"
ABOUT = "/our-firm/"
CONTACT = "/get-in-touch/"
SITEMAP_P = "/page-index/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, AZ"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}
TOOL_BY = {t["slug"]: t for t in TOOLS}

# ---------------------------------------------------------------- photos
ALT = {
    "haboob-phoenix": "A wall of dust from a haboob rolling toward the Phoenix skyline at dusk",
    "phoenix-aerial": "Aerial view of downtown Phoenix and the surrounding neighborhoods",
    "phoenix-skyline-palms": "Downtown Phoenix towers behind palm trees under a clear sky",
    "monsoon-thunderhead": "A towering monsoon thunderhead building over the desert",
    "rim-monsoon-storm": "Monsoon rain falling over forested canyons below the Mogollon Rim",
    "lightning-strike": "Lightning bolt striking from a dark storm over a desert ridge at night",
    "monument-valley-lightning": "Lightning striking near the sandstone buttes of Monument Valley at sunset",
    "joshua-tree-lightning": "Joshua tree silhouetted against storm clouds lit by lightning",
    "hail-street": "Hailstones covering a street and roadside after a severe storm",
    "spanish-tile-closeup": "Close-up of weathered terracotta barrel roof tiles with mortar",
    "red-tile-roof": "Red clay tile roof with a raised skylight structure",
    "tile-roof-skylight": "Rows of weathered roof tiles around a small skylight",
    "tile-roof-street": "Suburban street of stucco homes with tile roofs and palm trees",
    "wildfire-crew": "Wildland firefighter working along a line of flames in a forest",
    "pine-forest-fire": "Wildfire burning through a ponderosa pine forest",
    "contreras-fire": "Smoke and a fire whirl rising over desert grassland during the Contreras Fire",
    "horse-tank-fire-night": "Wildfire glowing behind pine trees at night beside a road",
    "burned-hillside-lodge": "Log homes standing below a hillside blackened by wildfire",
    "roof-edge-damage": "Close-up of a damaged roof edge with lifted shingles and broken fascia",
    "storm-debris-homes": "Homes and debris scattered across a neighborhood after a severe windstorm",
    "gutted-room": "Room stripped to bare walls and floor during damage repairs",
    "firefighters-doorway": "Two firefighters in turnout gear and breathing equipment at a building entrance",
    "san-francisco-peaks": "Snow-covered San Francisco Peaks above pine and aspen forest near Flagstaff",
    "inner-basin-cabin": "Log cabin in a meadow beneath the snowy San Francisco Peaks",
    "saguaro-hillside": "Saguaro cactus covering a desert hillside in southern Arizona",
    "saguaro-rock": "Saguaro cactus in the Sonoran Desert with a rocky peak behind it",
    "heat-thermometer": "Outdoor thermometer reading about 120 degrees Fahrenheit",
    "builder-site-walk": "Contractor in a hard hat walking toward a house with plans in hand",
    "consult-colleagues": "Three colleagues reviewing a laptop together at a table",
    "consult-laptop": "Two people discussing documents on a laptop",
    "calculator-notes": "Calculator, pencil and sticky notes on a desk",
    "calculator-glasses": "Calculator, pen and reading glasses on a notepad",
    "glass-office-tower": "Blue glass office tower against a clear sky",
    "conference-room": "Empty conference room with a long table and floor-to-ceiling windows",
    "covered-patio": "Covered patio living area with sofa and garden views",
    "white-kitchen": "White kitchen with cabinets and under-cabinet lighting",
    "clipboard-letter": "Signed letter on a clipboard on a wooden desk",
    "desert-highway": "Empty desert highway stretching toward distant mountains",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appointment": "clipboard-letter", "home-insurance-appraisal": "tile-roof-street",
    "commercial-and-hoa-appraisal": "glass-office-tower", "tile-roof-and-hail-claims": "spanish-tile-closeup",
    "monsoon-wind-microburst-claims": "haboob-phoenix", "water-and-slab-leak-claims": "white-kitchen",
    "fire-and-smoke-damage-appraisal": "firefighters-doorway", "wildfire-and-ash-claims": "pine-forest-fire",
    "snow-load-and-freeze-claims": "inner-basin-cabin", "claim-estimate-second-opinion": "calculator-glasses",
    "umpire-selection-and-service": "conference-room",
}
SVC_ICON = {
    "appraisal-clause-appointment": "doc", "home-insurance-appraisal": "home", "commercial-and-hoa-appraisal": "building",
    "tile-roof-and-hail-claims": "hail", "monsoon-wind-microburst-claims": "wind", "water-and-slab-leak-claims": "drop",
    "fire-and-smoke-damage-appraisal": "flame", "wildfire-and-ash-claims": "tree", "snow-load-and-freeze-claims": "snow",
    "claim-estimate-second-opinion": "file", "umpire-selection-and-service": "scale",
}
LOC_PHOTO = {
    "phoenix": "phoenix-skyline-palms", "tucson": "saguaro-hillside", "mesa": "monsoon-thunderhead", "chandler": "red-tile-roof",
    "gilbert": "covered-patio", "scottsdale": "saguaro-rock", "glendale": "phoenix-aerial", "flagstaff": "san-francisco-peaks",
    "prescott": "horse-tank-fire-night", "yuma": "heat-thermometer", "lake-havasu-city": "desert-highway", "sierra-vista": "lightning-strike",
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": "calculator-notes", "depreciation-recovery-calculator": "calculator-glasses",
    "roof-squares-by-material": "tile-roof-skylight", "percentage-deductible-calculator": "hail-street",
    "claim-deadline-calendar": "clipboard-letter", "claim-file-readiness-check": "builder-site-walk",
    "tile-roof-repair-or-replace-checker": "spanish-tile-closeup",
}
POST_PHOTO = {
    "documenting-monsoon-storm-damage": "storm-debris-homes", "tile-roof-claims-underlayment-matching": "red-tile-roof",
    "wildfire-smoke-and-ash-cleanup-claims": "burned-hillside-lodge", "water-leaks-in-seasonal-homes": "gutted-room",
    "appraisal-difi-complaint-or-attorney": "consult-laptop", "overhead-profit-and-price-lists": "roof-edge-damage",
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
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
}


def ic(name, cls="ic"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(uid="m", size=40):
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#a62020"/><stop offset="1" stop-color="#3a0909"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="11" fill="url(#{uid})"/><circle cx="24" cy="21" r="7.5" fill="#2eb8ac"/>'
            '<path d="M7.5 33.5h9l3.6-7.5h7.8l3.6 7.5h9" fill="none" stroke="#f6e2c8" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M13 39.5h22" stroke="#f6e2c8" stroke-opacity=".55" stroke-width="2.4" stroke-linecap="round"/></svg>')


def brand(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span class="brand-t"><b>Arizona</b><span>Insurance Appraiser</span></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "AZ", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-AZ", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 15 Arizona counties.",
        "areaServed": [{"@type": "State", "name": "Arizona"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Tile roof claims", "Monsoon wind damage", "Wildfire smoke damage", "Hail damage"],
        "priceRange": "$$",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "17:00"}],
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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def build_graph(path, title, desc, schema, img_key, noindex):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id = "WebPage", [], None
    for n in schema or []:
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": canonical + "#webpage"}
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        nodes.append(n)
    p = PHOTOS[img_key]
    page = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": p["fw"], "height": p["fh"]},
    }
    if crumb_id:
        page["breadcrumb"] = {"@id": crumb_id}
    order = {t: i for i, t in enumerate(MAIN_TYPES)}
    mains = sorted((n for n in nodes if n.get("@type") in order), key=lambda n: order[n["@type"]])
    page["mainEntity"] = {"@id": mains[0]["@id"] if mains else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if noindex else [page]) + nodes
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal roadmap", PROCESS), ("Questions & answers", FAQ_P), ("Claim dictionary", GLOSS), ("Articles", POST_BASE)]


def _groups():
    return [
        ("Appraisal", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("Every appraisal service", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Arizona cities", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


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


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", "ic sm")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "ic chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{ABOUT}">Our firm</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="head-in">
{brand("mh")}
<nav class="main-nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-cta"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn small" href="{CONTACT}">Free review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-veil" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{ABOUT}">Our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li></ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 7am–5pm Arizona time</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    lr = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-band-t">Short on a claim payment? Get a second set of eyes on the numbers.</p><div class="btn-row"><a class="btn teal" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-brand">{brand("mf")}
<p>Independent appraisal, estimate review and umpire work on disputed property claims, from the Colorado River to the New Mexico line.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("clock")}Mon–Fri 7am–5pm Arizona time</li><li>{ic("pin")}All 15 Arizona counties</li></ul></div>
<div><h2 class="foot-h">Appraisal</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul class="two">{loc}</ul></div>
<div><h2 class="foot-h">Free calculators</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Resources</h2><ul>{lr}<li><a href="{ABOUT}">Our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Site content is general and educational; your policy’s wording controls, and results depend on the facts of each claim.</p>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="/privacy-notice/">Privacy</a></li><li><a href="/website-terms/">Terms</a></li><li><a href="/disclosures/">Disclosures</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="{SITEMAP_P}">Page index</a></li></ul></div></div>
</footer>
<a class="to-top" href="#main" aria-label="Back to top">{ic("up")}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("mail")} Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", noindex=False, photo="haboob-phoenix"):
    canonical = DOMAIN + path
    ld = build_graph(path, title, desc, schema, photo, noindex)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    p = PHOTOS[photo]
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw" fetchpriority="high">'
    og_alt = f"{BRAND}: independent property claim appraisal across Arizona"
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
<meta property="og:image:alt" content="{og_alt}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{og_alt}">
<meta name="geo.region" content="US-AZ">
<meta name="geo.placename" content="Arizona">
<meta name="theme-color" content="#7a1414">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Figtree:wght@400;500;600;700&display=swap">
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
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg" aria-hidden="true">{img(photo, lazy=False, alt="", extra=' data-parallax="0.1"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker on-dark">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs, cls="faq"):
    return f'<div class="{cls}">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev")}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box call-box"><h2 class="side-h">Talk it through, free</h2><p>Tell us what the carrier paid and what the repair costs. We’ll give you a straight answer on whether appraisal fits.</p><a class="call-num" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn teal block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def cta_strip(h="Is the carrier’s number short?", p="Send the estimate and a few photos. We’ll tell you what we see, at no cost."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><p class="cta-strip-h">{e(h)}</p><p>{e(p)}</p></div><div class="btn-row"><a class="btn teal" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="side">{aside}</aside></div>'


LOSSES = ["Monsoon wind / microburst", "Hail", "Water / slab leak", "Fire / smoke", "Wildfire / ash", "Snow / freeze", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", page="/", hl="h3", fid="f"):
    roles = ["Homeowner", "Commercial owner", "HOA / property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Arizona"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="lead-h">{e(heading)}</{hl}><p class="lead-sub">Free, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Approx. amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="/privacy-notice/">privacy notice</a>.</span></label></div>
<div class="full"><button class="btn block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="lead hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="lead-h">Get a free claim review</h2><p class="lead-sub">Two minutes. A real person calls you back.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="h-city">Where is the property?</label><select id="h-city" name="city">{_opt([l["city"] for l in LOCATIONS] + ["Elsewhere in Arizona"])}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>Contact me about my claim. <a href="/privacy-notice/">Privacy notice</a>.</span></label>
<button class="btn block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
<p class="lead-trust">{ic("shield")}No obligation. Your details stay private.</p>
</form>"""


def svc_card(s, h="h3", big=False):
    return (f'<a class="pcard rv{" big" if big else ""}" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
            f'<span class="pcard-b"><span class="pcard-ic">{ic(SVC_ICON[s["slug"]])}</span><{h} class="pcard-t">{e(s["name"])}</{h}><span class="pcard-p">{e(s["short"])}</span><span class="pcard-go">Learn more {ic("arrow", "ic sm")}</span></span></a>')


def loc_tile(l, h="h3"):
    return (f'<a class="ctile rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}'
            f'<span class="ctile-b"><{h} class="ctile-t">{e(l["city"])}</{h}><span>{e(l["county"])}</span></span></a>')


def tool_row(t, h="h3"):
    return (f'<a class="trow rv" href="{TOOL_BASE}{t["slug"]}/"><span class="trow-ph">{img(TOOL_PHOTO[t["slug"]], sizes="120px", alt="")}</span>'
            f'<span class="trow-b"><span class="trow-k">{e(t["kind"])}</span><{h} class="trow-t">{e(t["name"])}</{h}><span class="trow-p">{e(t["short"])}</span></span>{ic("arrow", "ic trow-go")}</a>')


def post_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a>'
            f'<div class="post-b"><p class="post-m">{nice} · {p["read"]} read</p><{h} class="post-t"><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>')


# ---------------------------------------------------------------- home
REGIONS = [
    ("Valley of the Sun", "Phoenix · Mesa · Chandler · Scottsdale", "phoenix-aerial",
     "Microbursts, dust storms and hail over concrete tile, foam roofs and block walls. Slab leaks and HOA matching disputes are everyday files."),
    ("Southern Arizona", "Tucson · Sierra Vista · Green Valley", "saguaro-hillside",
     "Mountain-born monsoon storms, wash flooding, flat roofs with parapets and wildfire on the sky islands."),
    ("High Country", "Flagstaff · Prescott · Show Low · Payson", "san-francisco-peaks",
     "Wildfire and post-fire flooding, snow load, ice dams and frozen pipes in cabins and second homes."),
    ("River & Western Desert", "Yuma · Lake Havasu City · Kingman", "desert-highway",
     "Extreme heat, monsoon gusts, wash flooding and water losses in seasonal homes that sit empty all summer."),
]

CALENDAR = [
    ("Monsoon wind & microbursts", "Jun 15 – Sep 30", 6, 9, "m"),
    ("Hail", "Mostly Jul – Sep; rare autumn events", 7, 10, "h"),
    ("Wildfire", "Peaks May – early Jul", 4, 7, "f"),
    ("Extreme heat stress", "Jun – Sep", 6, 9, "t"),
    ("Tropical-remnant rain", "Sep – Oct", 9, 10, "r"),
    ("Snow load & freeze", "Nov – Mar, high country", 11, 15, "s"),
]
MONTHS = "JFMAMJJASOND"


def calendar():
    head = "".join(f"<span>{m}</span>" for m in MONTHS)
    rows = ""
    for name, when, a, b, k in CALENDAR:
        segs = []
        if b > 12:
            segs = [(a, 13), (1, b - 12 + 1)]
        else:
            segs = [(a, b + 1)]
        bars = "".join(f'<i class="cal-bar c-{k}" style="grid-column:{s}/{t}"></i>' for s, t in segs)
        rows += f'<li class="cal-row"><span class="cal-l"><b>{e(name)}</b><small>{e(when)}</small></span><span class="cal-track">{bars}</span></li>'
    return f'<div class="cal rv"><div class="cal-row cal-head" aria-hidden="true"><span class="cal-l"></span><span class="cal-track">{head}</span></div><ul class="cal-list">{rows}</ul></div>'


def home():
    feat = SVC_BY["tile-roof-and-hail-claims"]
    order = [SVC_BY[k] for k in ("appraisal-clause-appointment", "monsoon-wind-microburst-claims", "home-insurance-appraisal", "wildfire-and-ash-claims")]
    cards = svc_card(feat, big=True) + "".join(svc_card(s) for s in order)
    rest = [s for s in SERVICES if s is not feat and s not in order]
    chips = "".join(f'<a class="chip" href="{SVC_BASE}{s["slug"]}/">{ic(SVC_ICON[s["slug"]])}{e(s["name"])}</a>' for s in rest)
    regions = "".join(f'<div class="region rv">{img(ph, sizes="(max-width:700px) 100vw, 25vw", alt="")}<div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div></div>' for n, c, ph, t in REGIONS)
    tools = "".join(tool_row(t) for t in TOOLS)
    cities = "".join(loc_tile(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])
    steps = [
        ("Free review", "We read your policy, the carrier’s estimate and your photos, then tell you plainly whether appraisal is the right tool."),
        ("Independent inspection", "Measurements, tile counts, moisture readings and photographs, building our own scope from the ground up."),
        ("Line-item valuation", "An estimate priced for your Arizona ZIP code, with code items, permits and overhead and profit handled correctly."),
        ("Panel work", "The written demand goes out, appraisers are named, and we work line by line with the carrier’s appraiser."),
        ("Signed award", "Items still in dispute go to a neutral umpire. Two signatures set the amount of loss, and payment follows under the policy."),
    ]
    stack = "".join(f'<li class="scard" style="--i:{i}"><span class="scard-n">{i + 1:02d}</span><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))
    myths = [
        ("Appraisal is only for huge commercial claims.", "Most of our files are homes. If the gap is meaningful after fees, appraisal can fit a residential claim."),
        ("The appraisal panel decides whether I’m covered.", "No. Appraisal decides the amount of a covered loss. Coverage disputes belong with an attorney."),
        ("My contractor can be my appraiser.", "Policies usually require an independent appraiser. A contractor who will do the work invites a challenge."),
        ("Asking for appraisal stops every deadline.", "Not automatically. Suit limitation and other deadlines may keep running, so calendar them."),
    ]
    myth_html = "".join(f'<div class="myth rv"><p class="myth-q">{ic("x", "ic myth-x")}<span>{e(m)}</span></p><p class="myth-a">{ic("check", "ic myth-ok")}<span>{e(f)}</span></p></div>' for m, f in myths)

    home_faqs = [
        ("What does an Arizona Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. Named as your appraiser, we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster manages and negotiates your entire claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When should I call an Arizona Insurance Appraiser?", "When coverage is accepted, you have the carrier’s final estimate, and the gap between it and your contractor’s number is meaningful, usually more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That is why documentation matters before anyone invokes appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire’s fee. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you cover my part of Arizona?", "Yes. We work in all 15 counties, including metro Phoenix, Tucson, Flagstaff, Prescott, Yuma, Lake Havasu City and Sierra Vista."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg" aria-hidden="true">{img("haboob-phoenix", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker on-dark">{ic("sun", "ic sm")} Independent property claim appraisal · all 15 counties</p>
<h1>Arizona Insurance Appraiser for claims the carrier <em>underpaid</em></h1>
<p class="lede">The insurer accepted your monsoon, hail, water or fire claim, but the check won’t cover the repair. As your Arizona Insurance Appraiser, we build an independent line-item valuation and carry it through the appraisal process already written into your policy.</p>
<div class="btn-row"><a class="btn teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#services">See what we appraise</a></div>
<ul class="hero-points"><li>{ic("check")}Named as your appraiser</li><li>{ic("check")}Tile, foam &amp; shingle roofs</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="counters" aria-label="At a glance"><div class="wrap"><div class="counters-in rv">
<div class="cnt"><b data-count="15">15</b><span>Arizona counties served</span></div>
<div class="cnt"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="cnt"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
<div class="cnt"><b>2 of 3</b><span>Signatures that make an award binding</span></div>
</div></div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-copy rv">
<p class="kicker">The short-pay problem</p>
<h2>Covered is not the same as paid in full</h2>
<p>Most disputed Arizona claims are not denials. The carrier pays something, just not enough: a tile roof priced as a few spot repairs, a block wall left off a monsoon claim, a slab leak scoped as one wet room. An Arizona Insurance Appraiser works in exactly that gap between “covered” and “paid.”</p>
<p>We are independent estimators who serve as the appraiser you name under your policy. Arizona Insurance Appraiser never edits the carrier’s estimate; we measure, count and price the loss ourselves, so every line can be defended in front of an umpire.</p>
<ul class="ticks"><li>{ic("check")}<span><b>Our own scope.</b> Measured on site, never copied.</span></li><li>{ic("check")}<span><b>Defensible numbers.</b> Built to persuade an umpire, not to impress you.</span></li><li>{ic("check")}<span><b>Honest triage.</b> If you need an attorney or just a supplement, we say so.</span></li></ul>
<a class="btn line" href="{ABOUT}">How our firm works {ic("arrow")}</a>
</div>
<div class="intro-ph rv">
<figure class="ph-a">{img("tile-roof-street", sizes="(max-width:900px) 90vw, 460px")}</figure>
<figure class="ph-b">{img("roof-edge-damage", sizes="(max-width:900px) 60vw, 300px")}</figure>
<p class="ph-note">{ic("hail", "ic sm")} Typical gap: roof math, matching and missing trades</p>
</div>
</div></section>

<section class="sec sand"><div class="wrap cal-wrap">
<div class="cal-copy rv"><p class="kicker">Arizona’s claim calendar</p><h2>Every season brings a different kind of claim</h2><p>The monsoon officially runs June 15 to September 30. Wildfire season usually peaks before it, the high country freezes after it, and the heat never really leaves the low desert. An Arizona Insurance Appraiser has to know what each season does to a roof, a wall and an estimate.</p><p class="hint">Bands show typical timing. Storms do not read calendars: the October 2010 Phoenix hailstorm arrived well after the monsoon.</p></div>
{calendar()}
</div></section>

<section class="sec" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">What we appraise</p><h2>Eleven ways an Arizona Insurance Appraiser can help</h2><p>From one estimate review to full panel representation and neutral umpire work, each service is built around a single job: a valuation of your loss that holds up.</p></div>
<div class="pgrid">{cards}</div>
<div class="chips rv">{chips}</div>
<p class="center mt"><a class="btn line" href="{SVC_BASE}">Compare all appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec red" id="gap-check"><div class="wrap split">
<div class="rv"><p class="kicker on-dark">Two-number gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two figures you already have. If the difference is large, a conversation with an Arizona Insurance Appraiser makes sense. If it is small, a documented supplement request is often faster and cheaper.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds fees and shows your break-even point.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap stack-wrap">
<div class="stack-copy"><p class="kicker">From first call to signed award</p><h2>How an appraisal moves with us</h2><p>The appraisal clause turns an open-ended argument into a process with a binding result. Here is how Arizona Insurance Appraiser takes a file from first call to signed award.</p><a class="btn line" href="{PROCESS}">Read the full appraisal roadmap {ic("arrow")}</a></div>
<ol class="pstack">{stack}</ol>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="sec-head left rv"><p class="kicker on-dark">Four Arizonas</p><h2>One state, four claim climates</h2><p>Dust storms in Mesa, flash floods in Tucson washes, snow on Flagstaff roofs and 118°F afternoons in Lake Havasu City. An Arizona Insurance Appraiser has to price each one with local knowledge.</p></div>
<div class="regions">{regions}</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv sticky-copy"><p class="kicker">Free &amp; private</p><h2>Seven free calculators from an Arizona Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser; nothing is stored or sent.</p><a class="btn line" href="{TOOL_BASE}">Open the calculators {ic("arrow")}</a></div>
<div class="trows">{tools}</div>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Statewide coverage</p><h2>Where Arizona Insurance Appraiser works most often</h2><p>We serve all 15 counties, from Apache to Yuma. These are the communities where we see the most claims.</p></div>
<div class="cgrid">{cities}</div>
<p class="center mt"><a class="btn line" href="{LOC_BASE}">See every Arizona city we cover {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Clearing things up</p><h2>Four myths an Arizona Insurance Appraiser hears every week</h2></div>
<div class="myths">{myth_html}</div>
</div></section>

<section class="sec sand"><div class="wrap faq-wrap">
<div class="rv"><p class="kicker">Questions</p><h2>Ask an Arizona Insurance Appraiser</h2><p>Straight answers about how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row"><a class="btn" href="{FAQ_P}">All questions {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Claim dictionary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Articles</p><h2>Read this before you invoke appraisal</h2><p>Practical guides from the Arizona Insurance Appraiser team on documentation, roofs, wildfire and your options.</p></div>
<div class="posts">{posts}</div>
</div></section>

<section class="cta-photo"><div class="cta-photo-bg" aria-hidden="true">{img("monsoon-thunderhead", alt="", extra=' data-parallax="0.2"')}</div><div class="wrap cta-photo-in rv"><p class="kicker on-dark">Monsoon season is claim season</p><h2>Check the numbers before you sign off on them</h2><p>A short review now can keep you from accepting a payment that will not cover the repair.</p><div class="btn-row"><a class="btn teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to an Arizona Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="clines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 7am–5pm Arizona time</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All 15 Arizona counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", fid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Appraisal",
                        "Arizona Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid monsoon, hail, water and fire claims.",
                        body, [faq_schema(home_faqs)], photo="haboob-phoenix"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Appraisal", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        art = s["body"] + f"<h2>Questions about {e(s['name'].lower())}</h2>{faq_block(s['faqs'])}<h2>Related services</h2>" + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(art, call_box() + list_box("All appraisal services", items, path) + list_box("Where we work", locs + [("All Arizona cities", LOC_BASE)])) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Arizona"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Appraisal", SVC_BASE)]
    cards = "".join(svc_card(s, h="h2") for s in SERVICES)
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services for Arizona Property Claims",
                     "Every service starts with the same goal: an accurate, defensible valuation of your loss. Start with an estimate review, or bring us in once appraisal has been demanded.", "builder-site-walk") + f"""
<section class="sec"><div class="wrap"><div class="pgrid even">{cards}</div></div></section>
<section class="sec sand"><div class="wrap split top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes end there.</p><a class="btn" href="{SVC_BASE}claim-estimate-second-opinion/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, condos, manufactured homes, multifamily, retail, office, industrial, churches and HOA communities."), ("Is appraisal only for roof claims?", "No. We handle monsoon wind, hail, water, fire, wildfire, snow and freeze, and other covered perils.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Arizona | All Services",
                             "Arizona insurance appraisal services: appraisal clause representation, roof and hail, monsoon wind, water, fire, wildfire and umpire work.",
                             body, schema, photo="builder-site-walk"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        art = (f'<div class="note"><b class="h">Local claim risks</b><ul class="risk-chips">{chips}</ul></div>' + l["body"] +
               f"<h2>Appraisal services in {e(l['city'])}</h2><p>Every {BRAND} service is available to owners in {e(l['city'])} and across {e(l['county'])}, including:</p><ul>{svc}</ul>"
               f"<h2>Questions from {e(l['city'])} property owners</h2>{faq_block(l['faqs'])}<h2>Nearby cities</h2>" +
               related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]]))
        facts = [("County", l["county"]), ("Region", l["region"]), ("Housing", l["housing"].split(",")[0])]
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph, facts) + layout(art, call_box() + list_box("Arizona cities", items, path) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Arizona"}}, "url": DOMAIN + path}]
        title = f"{l['city']} Insurance Appraiser | Claim Appraisal AZ"
        if len(title) > 56:
            title = f"{l['city']} Insurance Appraiser | AZ Claims"
        desc = f"Independent insurance appraiser for {l['city']} and {l['county']}. Appraisal and estimate review for underpaid storm, water and fire claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {l['city']} and {l['county']}: appraisal and estimate review for underpaid storm, water and fire claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    tiles = "".join(loc_tile(l, h="h2") for l in LOCATIONS)
    reg = "".join(f'<div class="region rv">{img(ph, sizes="(max-width:700px) 100vw, 25vw", alt="")}<div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div></div>' for n, c, ph, t in REGIONS)
    counties = "Apache, Cochise, Coconino, Gila, Graham, Greenlee, La Paz, Maricopa, Mohave, Navajo, Pima, Pinal, Santa Cruz, Yavapai and Yuma"
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 15 Arizona Counties",
                     "From the Colorado River to the New Mexico line, we handle claims in every Arizona county. These local pages cover the cities where we work most often.", "phoenix-aerial", cta=True) + f"""
<section class="sec"><div class="wrap"><div class="cgrid">{tiles}</div></div></section>
<section class="sec dark"><div class="wrap"><div class="sec-head left rv"><p class="kicker on-dark">Regions</p><h2>How claims differ across Arizona</h2><p>The same policy language plays out very differently in a Scottsdale custom home, a Tucson adobe and a Pinetop cabin.</p></div><div class="regions">{reg}</div></div></section>
<section class="sec"><div class="wrap narrow"><h2>Every county, every claim</h2><p>We work in {counties} counties. If your property is outside the cities listed above, call and tell us where it is. Rural properties, ranches and reservation-adjacent communities are part of our regular work.</p></div></section>
{cta_strip("Don’t see your city?", "We cover all 15 Arizona counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Arizona Cities We Serve | Insurance Appraisal Statewide",
                             "Insurance appraisal in all 15 Arizona counties, including Phoenix, Tucson, Mesa, Chandler, Scottsdale, Flagstaff, Prescott and Yuma.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="phoenix-aerial"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + f"<h2>Questions about this tool</h2>{faq_block(t['faqs'])}<h2>More free calculators</h2>" + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = (page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) +
                f'<section class="sec tool-sec"><div class="wrap">{t["markup"]}<p class="hint tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>' +
                layout(art, call_box() + list_box("All calculators", items, path)) + cta_strip("Want a professional to check the numbers?", "Send the estimate and we’ll review it line by line."))
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    rows = "".join(tool_row(t, h="h2") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Arizona Owners",
                     "Seven calculators and planners built from real appraisal work. Check the carrier’s math, plan your deadlines and decide on next steps. No sign-up, nothing stored.", "calculator-notes", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="trows two">{rows}</div></div></section>
<section class="sec sand"><div class="wrap split top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}claim-deadline-calendar/">deadline calendar</a> so nothing lapses.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-squares-by-material/">roof squares calculator</a> and, for tile, the <a href="{TOOL_BASE}tile-roof-repair-or-replace-checker/">repair-or-replace checker</a>.</li><li>See what you are actually owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">deductible</a> and <a href="{TOOL_BASE}depreciation-recovery-calculator/">depreciation</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}claim-file-readiness-check/">claim file readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Arizona Owners",
                              "Free Arizona claim tools: appraisal payoff estimator, depreciation, roof squares, deductible, deadline calendar and a tile roof checker.",
                              body, schema, photo="calculator-notes"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal roadmap", path)]
    body = page_hero(trail, "Process guide", "The Arizona Insurance Appraisal Roadmap, Step by Step",
                     "Eight steps from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", "desert-highway",
                     [("Steps", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(PROCESS_BODY, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Arizona", "description": "Eight steps from the first disagreement to a signed appraisal award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(STEPS)]}
    write(path, document(path, "Arizona Insurance Appraisal Roadmap | 8 Steps",
                         "Step-by-step guide to insurance appraisal in Arizona: the written demand, choosing appraisers and an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="desert-highway"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Questions", path)]
    toc = "".join(f'<a href="#q-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = f'<nav class="toc" aria-label="Topics">{toc}</nav>' + "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions from Arizona Owners",
                     f"{len(allq)} plain answers grouped by topic: the basics, costs and timing, Arizona specifics, roofs and storms, and working with us.", "consult-colleagues") + layout(groups, call_box() + list_box("Resources", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")
    write(path, document(path, "Insurance Appraisal Questions | Arizona Costs & Rules",
                         "Answers to common Arizona insurance appraisal questions: how it works, what it costs, DIFI, FAIR plans, roofs, storms and binding awards.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="consult-colleagues"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim dictionary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    art = f'<div class="filter"><label for="gloss-filter">Search the dictionary</label><input id="gloss-filter" type="search" placeholder="Try “underlayment” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Arizona Property Claim Dictionary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards, from actual cash value to wildland-urban interface, defined in plain English.", "clipboard-letter", cta=False) + layout(art, call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Arizona property claim dictionary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Property Claim Dictionary | ACV, Umpire, Haboob & More",
                         "Plain-English definitions of Arizona property claim terms: actual cash value, underlayment, monsoon, umpire, overhead and profit and more.",
                         body, [crumbs_schema(trail), dts], photo="clipboard-letter"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Articles", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = p["body"] + "<h2>Keep reading</h2>" + related([("Article", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Article · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", LEARN) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        posting = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), posting], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Articles", path)]
    cards = "".join(post_card(p, h="h2") for p in POSTS)
    body = page_hero(trail, "Articles", "Insurance Appraisal Articles for Arizona Owners",
                     "Practical guides on documentation, tile roofs, wildfire smoke, seasonal homes and your options when a claim comes up short.", "consult-laptop", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Appraisal Articles for Arizona Owners",
                         "Guides for Arizona property owners on monsoon documentation, tile roof claims, wildfire smoke, snowbird water leaks and DIFI complaints.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="consult-laptop"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Our firm", path)]
    art = f"""
<figure class="lead-img">{img("consult-colleagues", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it accurately. That focus lets us serve as your named appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first, numbers second.</strong> We inspect and measure before we look at anyone else’s estimate.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You will understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney, a public adjuster or simply a supplement, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Built for Arizona’s claims</h2>
<p>Arizona produces losses most states never see in the same year: microbursts and haboobs in the Valley, flash floods in Tucson washes, wildfire and post-fire flooding around Flagstaff, snow load in the White Mountains and heat that ages every roof in Yuma. Concrete tile, spray foam, block walls, slab foundations and evaporative coolers each need to be priced by people who know them.</p>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across all 15 counties. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and do not give legal advice. We do not act as public adjusters or negotiate claims outside the appraisal process. We do not guarantee outcomes; no honest appraiser can. We publish no testimonials or client results on this site, and any example figures are illustrative.</p>
"""
    body = page_hero(trail, "Our firm", f"About {BRAND}",
                     "Independent estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "builder-site-walk") + layout(art, call_box() + list_box("Explore", [("Appraisal services", SVC_BASE), ("Arizona cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal roadmap", PROCESS)])) + cta_strip()
    write(path, document(path, f"About Our Firm | {BRAND}",
                         "Arizona Insurance Appraiser is an independent appraisal and estimating firm focused on the amount of loss in disputed Arizona property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="builder-site-walk"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Get in touch", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult-laptop", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="clines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 7am–5pm Arizona time</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>All 15 Arizona counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The carrier’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and your contractor’s estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hl="h2", fid="p")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         f"Get a free review of your disputed Arizona property claim. Call or text (844) 537-1427 or email {EMAIL}.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consult-laptop"), 0.8)

    lic = {"cc0": "CC0 1.0", "pdm": "Public domain"}
    credits = "".join(
        f'<tr><td>{img(k, "credit-th", sizes="120px", alt="")}</td><td>{e(v["title"] or k)}<br><small>{e(v.get("creator") or "Unknown")} · {e(v["source"])}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        "/privacy-notice/": ("Privacy Notice", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share, such as your name, phone, email, property location and claim details. Our web host records standard technical data (IP address, browser, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We do not sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. The figures you enter are not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site does not use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this notice will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you gave us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>""",
                             "How we collect, use and protect the information you share with us.", "Privacy notice for Arizona Insurance Appraiser: what we collect through forms and calls, how it is used, and how to ask us to change or delete it."),
        "/website-terms/": ("Website Terms", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is general information about insurance appraisal and property claims in Arizona.</p>
<h2>No client relationship</h2><p>Reading this site, using its calculators or submitting a form does not create an appraiser–client relationship. That begins only with a signed written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm. Nothing here is legal advice. Policies differ and laws change. Consult a licensed Arizona attorney for legal questions.</p>
<h2>Calculators</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. Photographs are used under the licenses listed on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Liability</h2><p>The site is provided “as is.” To the extent the law allows, we are not liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Arizona.</p>""",
                            "The terms that apply when you use this website and its calculators.", "Website terms for Arizona Insurance Appraiser: no client relationship or legal advice from site content, calculator limits and governing law."),
        "/disclosures/": ("Disclosures", f"""
<h2>General information only</h2><p>Content on this site is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not a law firm or public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, do not give legal advice and do not act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results, no testimonials</h2><p>Every claim is different. Example figures on this site are illustrative, not results for any client. We do not publish reviews, testimonials or client outcomes.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an Arizona attorney promptly.</p>
<h2>Legal references</h2><p>References to Arizona statutes, the Department of Insurance and Financial Institutions, court decisions or weather events are for context only and are described generally. Verify current law with official sources or an attorney.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They do not show our clients’ properties.</p>""",
                          "Important limits on the information published on this website.", "Disclosures for Arizona Insurance Appraiser: general information only, not legal advice, no guaranteed results and illustrative example figures."),
        "/photo-credits/": ("Photo Credits", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> (StockSnap, rawpixel, Flickr and WordPress Photo Directory contributors) or marked <strong>public domain</strong>, including photos by U.S. government agencies such as the U.S. Forest Service, NOAA and HUD. No attribution is legally required, but we credit each source here with thanks. Photos are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""",
                           "Sources and licenses for the photographs used on this site.", f"Photo credits for Arizona Insurance Appraiser: all {len(PHOTOS)} CC0 and public-domain photographs, with titles, creators, licenses and source links."),
    }
    for path, (title, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "glass-office-tower", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="glass-office-tower"), 0.3)


def sitemap_pages():
    path = SITEMAP_P
    trail = [("Home", "/"), ("Page index", path)]
    groups = [
        ("Main", [("Home", "/"), ("Our firm", ABOUT), ("Get in touch", CONTACT)]),
        ("Appraisal services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Arizona cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy notice", "/privacy-notice/"), ("Website terms", "/website-terms/"), ("Disclosures", "/disclosures/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="idx-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Page Index", f"Every page on {BRAND}, grouped by section.", "phoenix-skyline-palms", cta=False) + f'<section class="sec"><div class="wrap idx">{cols}</div></section>'
    write(path, document(path, f"Page Index | {BRAND}", f"A complete index of every page on {BRAND}: appraisal services, Arizona cities, free calculators, articles and legal pages.", body, [crumbs_schema(trail)], photo="phoenix-skyline-palms"), 0.3)

    body = f"""<section class="phero err"><div class="phero-bg" aria-hidden="true">{img("haboob-phoenix", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker on-dark">Error 404</p><h1>This page got lost in the dust storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn teal" href="/">Home</a><a class="btn ghost-l" href="{SVC_BASE}">Appraisal services</a><a class="btn ghost-l" href="{TOOL_BASE}">Free calculators</a><a class="btn ghost-l" href="{CONTACT}">Get in touch</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, noindex=True), sitemap=False)


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
// Arizona Insurance Appraiser - front controller for the static build.
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

if (strpos($path, '..') !== false) {
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
