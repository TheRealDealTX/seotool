#!/usr/bin/env python3
"""Static site generator for montanainsuranceappraiser.com.

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
from learn import PROCESS_STEPS, PROCESS_INTRO, PROCESS_OUTRO, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, SNOW_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Montana Insurance Appraiser"
HOST = "montanainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261109a"   # bump when CSS/JS change
FAV = "1"           # bump when icons change
HOURS = "Mon–Fri, 8am–6pm MT"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""

SVC_BASE = "/claim-services/"
LOC_BASE = "/montana-cities/"
TOOL_BASE = "/claim-toolkit/"
POST_BASE = "/field-notes/"
ABOUT, CONTACT = "/about-our-firm/", "/get-in-touch/"
PROCESS, FAQ_P, GLOSS = "/appraisal-roadmap/", "/appraisal-questions/", "/claim-dictionary/"
PRIVACY, TERMS, DISCLAIM, CREDITS, HTMLMAP = "/privacy-notice/", "/terms-of-service/", "/site-disclaimer/", "/photo-credits/", "/site-index/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, MT"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
TOOL_BY = {t["slug"]: t for t in TOOLS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-supercell": "Supercell thunderstorm towering over flat farmland",
    "storm-sunset": "Layered supercell thunderstorm glowing at sunset over the plains",
    "tornado-funnel": "Tornado funnel beneath a dark storm over open country",
    "supercell-barn": "Rotating storm cloud with lightning above a farm and barn",
    "hail-sky": "Dark hailstorm clouds rolling over a green field",
    "hail-ground": "Hailstones piled on the ground between rocks after a storm",
    "roof-toolbelt": "Roofer’s tool belt and hammer resting on an asphalt shingle roof",
    "roof-eave-damage": "Close view of a damaged roof edge with broken shingles and fascia",
    "ceiling-collapse": "Bedroom with a collapsed, water-damaged ceiling",
    "house-demolition": "Excavator tearing down a damaged two-story house",
    "storm-debris": "Homes surrounded by debris and broken trees after a severe storm",
    "log-home-burn-scar": "Log home and fenced meadow below a hillside burned by wildfire",
    "forest-fire-night": "Wildfire glowing orange behind a stand of conifers at night",
    "smoke-plume": "Large wildfire smoke plume rising above a forested ridge",
    "burned-prairie": "Blackened grassland and lingering smoke after a grass fire",
    "icicles-eave": "Icicles hanging from a snow-covered roof eave",
    "snow-roof-icicles": "Thick snow load overhanging a roof edge with long icicles",
    "snow-broken-trees": "Trees bent and snapped under heavy snow in a mountain forest",
    "flood-house": "House collapsing into the flooded Yellowstone River in June 2022",
    "flood-washout": "Riverbank and road washed out by the June 2022 Yellowstone flood",
    "red-barn-snow": "Red barn in a snowy pasture below mountains",
    "ranch-cattle": "Black calf in a ranch pasture with snowcapped mountains behind",
    "condo-building": "Multi-story brick condominium building on a city street",
    "commercial-building": "Low commercial building and parking lot at dusk",
    "calculator": "Blue calculator, pencil and sticky notes on a desk",
    "notebook": "Hands writing in a notebook beside a laptop and phone",
    "desk-meeting": "Two people reviewing documents across a wooden table",
    "signing": "Two people going over paperwork at a white desk with a laptop",
    "field-datasheet": "Hand filling in a printed inspection data sheet on a clipboard",
    "house-in-pines": "Two-story wood-sided house among tall pines",
    "great-falls": "Black Eagle Dam and falls on the Missouri River at Great Falls",
    "helena-capitol": "Montana State Capitol and its copper dome in Helena",
    "kalispell-valley": "Flathead Valley around Kalispell with snowy peaks beyond",
    "butte-panorama": "Panoramic view over Butte toward the surrounding mountains",
    "whitefish-mountain": "Snow-encrusted trees on Big Mountain above Whitefish",
    "livingston-cattle": "Cattle grazing in a valley pasture beneath snow-capped peaks",
    "hiline-hay": "Hay bales on the Hi-Line with the Sweet Grass Hills on the horizon",
    "polson-flathead": "Flathead Lake in autumn with farmland and a home on the shore",
    "bozeman-ridge": "Rugged mountain ridge above a forested valley",
    "missoula-clark-fork": "Clark Fork River flowing between wooded mountains in western Montana",
    "billings-pompeys": "Pompeys Pillar sandstone butte above prairie east of Billings",
    "miles-city-prairie": "Fence line across open eastern Montana prairie under a wide sky",
    "yellowstone-river": "Yellowstone River below sandstone bluffs near Pompeys Pillar",
    "whitefish-lake": "Sun setting over a mountain lake",
    "firefighter-smoke": "Firefighter in protective gear moving through thick smoke",
    "home-burned-hillside": "Ranch-style home in a valley below a hillside scorched by wildfire",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-representation": "desk-meeting", "homeowner-claim-appraisal": "house-in-pines",
    "commercial-hoa-claim-appraisal": "condo-building", "hail-roof-damage-appraisal": "hail-ground",
    "wind-tornado-damage-appraisal": "tornado-funnel", "water-damage-claim-appraisal": "ceiling-collapse",
    "fire-smoke-claim-appraisal": "firefighter-smoke", "wildfire-claim-appraisal": "log-home-burn-scar",
    "snow-load-ice-dam-freeze-claims": "icicles-eave", "ranch-farm-outbuilding-claims": "red-barn-snow",
    "insurance-estimate-review": "field-datasheet", "umpire-services": "signing",
}
LOC_PHOTO = {
    "billings": "billings-pompeys", "missoula": "missoula-clark-fork", "great-falls": "great-falls", "bozeman": "bozeman-ridge",
    "butte": "butte-panorama", "helena": "helena-capitol", "kalispell": "kalispell-valley", "whitefish": "whitefish-mountain",
    "livingston": "livingston-cattle", "havre": "hiline-hay", "polson": "polson-flathead", "miles-city": "miles-city-prairie",
}
POST_PHOTO = {
    "montana-appraisal-clause-explained": "desk-meeting", "hail-claims-on-montana-roofs": "roof-eave-damage",
    "wildfire-and-smoke-claims-montana": "smoke-plume", "snow-load-and-ice-dam-claims": "snow-broken-trees",
    "montana-unfair-claim-practices-overview": "helena-capitol", "building-a-claim-file-before-appraisal": "notebook",
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
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "hail": '<path d="M7 15a4 4 0 0 1 .5-8A5.5 5.5 0 0 1 18 8.5a3.5 3.5 0 0 1-1 6.5"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="21" r="1"/><circle cx="16" cy="19" r="1"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(uid="m", size=44):
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#1e428c"/><stop offset="1" stop-color="#0a1736"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="12" fill="url(#{uid})"/><circle cx="35" cy="12.5" r="3.4" fill="#f28c28"/>'
            '<path d="M8.5 31L18 17l6.5 9 5-6.5L39.5 31" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M9 37.5h30" stroke="#f28c28" stroke-width="3" stroke-linecap="round"/><path d="M16 37.5v3M24 37.5v3M32 37.5v3" stroke="#f28c28" stroke-width="2" stroke-linecap="round"/></svg>')


def brand(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span><b>Montana</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "MT", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MT", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 56 Montana counties.",
        "areaServed": [{"@type": "State", "name": "Montana"}] + [{"@type": "City", "name": l["geo"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services in Montana", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Wildfire claims", "Snow load and ice dam claims", "Property claim valuation"],
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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def build_graph(path, title, desc, schema, img_key, noindex):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id, main_hint = "WebPage", [], None, None
    for n in schema or []:
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            main_hint = n.get("mainEntity")
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
    page["mainEntity"] = {"@id": main_hint or (mains[0]["@id"] if mains else DOMAIN + "/#business")}
    graph = [org_schema(), site_schema()] + ([] if noindex else [page]) + nodes
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All claim services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Montana cities", LOC_BASE)),
        ("Toolkit", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("The full claim toolkit", TOOL_BASE)),
        ("Learn", [("Appraisal roadmap", PROCESS), ("Appraisal questions", FAQ_P), ("Claim dictionary", GLOSS), ("Field notes", POST_BASE)], None),
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
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li class="has-sub"><button type="button" data-drop aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "chev")}</button><ul class="sub{" two" if len(links) > 7 else ""}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="strong" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head" id="top"><div class="progress" aria-hidden="true"><span></span></div><div class="wrap head-in">
{brand("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-act"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-amber head-cta" href="{CONTACT}">Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button></div>
</div></header>
<div class="shade" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{ABOUT}">About our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-outline-l" href="{CONTACT}">Send claim details</a><small>{HOURS} · all 56 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("mf")}
<p>Independent appraisal, estimate review and umpire services for property owners with disputed insurance claims, from the Bitterroot to the Badlands.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>{HOURS}</span></li><li>{ic("pin")}<span>All 56 Montana counties</span></li></ul></div>
<div><h2 class="ft">Claim services</h2><ul>{svc}</ul></div>
<div><h2 class="ft">Montana cities</h2><ul class="cols2">{loc}</ul><h2 class="ft ft-gap">Claim toolkit</h2><ul>{tl}</ul></div>
<div><h2 class="ft">Learn</h2><ul><li><a href="{PROCESS}">Appraisal roadmap</a></li><li><a href="{FAQ_P}">Appraisal questions</a></li><li><a href="{GLOSS}">Claim dictionary</a></li><li><a href="{POST_BASE}">Field notes</a></li><li><a href="{ABOUT}">About our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we don’t give legal advice, and we don’t act as public adjusters. Content is general and educational, policy terms vary, and no result is guaranteed. Example figures are illustrative.</p>
<div class="foot-row"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{PRIVACY}">Privacy notice</a></li><li><a href="{TERMS}">Terms of service</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{HTMLMAP}">Site index</a></li></ul></div></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("file")} Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", noindex=False, photo="hero-supercell", body_cls=""):
    canonical = DOMAIN + path
    ld = build_graph(path, title, desc, schema, photo, noindex)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {PHOTOS[photo]["fw"]}w" imagesizes="(max-width:900px) 100vw, 50vw" fetchpriority="high">'
    og_alt = f"{BRAND}: independent property claim appraisal across Montana"
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
<meta name="geo.region" content="US-MT">
<meta name="geo.placename" content="Montana">
<meta name="theme-color" content="#13306b">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Figtree:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script type="application/ld+json">{ld}</script>
</head>
<body{f' class="{body_cls}"' if body_cls else ""}>
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
    parts = [f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    """Interior hero: dark-blue text panel on the left, full-height photo on the right."""
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-outline-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="ihero"><div class="ihero-ph">{img(photo, lazy=False, alt="", sizes="(max-width:900px) 100vw, 50vw")}</div>
<div class="wrap ihero-in"><div class="ihero-tx">{crumbs(trail)}<p class="eyebrow eyebrow-l">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><p class="box-k">Free first look</p><h2 class="box-t">Talk to an appraiser</h2><p>Tell us what the carrier paid and what you think it missed. We’ll say plainly whether appraisal makes sense.</p><a class="box-tel" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-amber btn-block" href="{CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_band(h="Think the carrier’s number is short?", p="Send the estimate and a few photos. We’ll tell you what we see, free."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-amber" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-outline-l" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Wind / tornado", "Wildfire / smoke", "Snow load / ice dam", "Frozen or burst pipe", "Water leak", "Fire", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", page="/", hl="h3", fid="f"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Farm or ranch owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Montana"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="form-t">{e(heading)}</{hl}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Rough amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy notice</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="ticket" action="/api/contact.php" method="post" data-lead novalidate aria-label="Request a free claim review">
<p class="ticket-t">Free claim review</p><p class="ticket-s">A real person calls back, usually within one business day.</p>
<div class="ticket-f">
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-city">Where is the property?</label><select id="h-city" name="city">{_opt([l["city"] for l in LOCATIONS] + ["Elsewhere in Montana"])}</select></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
</div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy notice</a>.</span></label>
<button class="btn btn-amber btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
</form>"""


def svc_card(s, h="h3"):
    return f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 300px", alt="")}<span class="scard-b"><{h}>{e(s["name"])}</{h}><span class="scard-p">{e(s["short"])}</span><span class="more">Explore {ic("arrow")}</span></span></a>'


def loc_card(l, h="h3"):
    return f'<a class="ccard rv" href="{loc_path(l)}"><span class="ccard-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 33vw, 290px", alt="")}</span><span class="ccard-b"><{h}>{e(l["city"])}</{h}><small>{e(l["county"])} · {e(l["region"])}</small></span></a>'


def tool_card(t, h="h3"):
    return f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(t["photo"], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 360px", alt="")}<span class="tag">{e(t["kind"])}</span></span><span class="tcard-b"><{h}>{e(t["name"])}</{h}><span class="tcard-p">{e(t["short"])}</span><span class="more">Open the tool {ic("arrow")}</span></span></a>'


def post_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return f'<article class="ncard rv"><a class="ncard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 380px", alt="")}</a><div class="ncard-b"><span class="meta">{nice} · {p["read"]} read</span><{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>'


# ---------------------------------------------------------------- home
SEASONS = [
    ("leaf", "Spring", "April–June", ["Heavy, wet spring snow on roofs", "Snowmelt and rain-on-snow flooding", "Hail season opens east of the Divide"]),
    ("sun", "Summer", "June–August", ["Peak hail on the plains and Hi-Line", "Thunderstorm winds and the odd tornado", "Wildfire season builds by late July"]),
    ("hail", "Fall", "September–November", ["Wildfire smoke and ash claims", "Early snow on unfinished repairs", "Chinook wind events return"]),
    ("snow", "Winter", "December–March", ["Snow load and ice dams", "Frozen pipes in cabins and vacant homes", "Downslope windstorms along the Front"]),
]

REGIONS = [
    ("Western Mountains & Flathead", "Missoula · Kalispell · Whitefish · Polson", "Wildfire and smoke, heavy mountain snow, falling timber and lake cabins with seasonal occupancy.", "kalispell-valley"),
    ("Southwest & Gallatin", "Bozeman · Butte · Helena · Livingston", "High building costs, snow load, fierce valley winds and older brick and frame homes.", "bozeman-ridge"),
    ("Rocky Mountain Front & Hi-Line", "Great Falls · Havre · Shelby · Cut Bank", "Chinook winds, hard hail, sudden temperature swings and long distances for contractors.", "hiline-hay"),
    ("Yellowstone Valley & Eastern Plains", "Billings · Miles City · Glendive · Sidney", "Montana’s busiest hail corridor, thunderstorm winds, river flooding and grass fires.", "billings-pompeys"),
]


def home():
    K = BRAND
    home_faqs = [
        (f"What does a {K} actually do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, write an independent line-item estimate, work with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        (f"Is a {K} the same as a public adjuster?", "No. A public adjuster manages and negotiates a whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When is appraisal worth it?", "Usually when coverage has been accepted, you have the carrier’s full estimate, and the gap between it and a qualified contractor’s estimate is meaningful, often more than about 10% or several thousand dollars. Our claim gap calculator helps you test that."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. The award doesn’t decide coverage questions, and your policy wording controls."),
        ("How are fees handled?", "Each side pays its own appraiser and usually half of any umpire. We put fee terms in writing before work begins, and the first conversation costs nothing."),
        ("Do you work outside the big cities?", "Yes. We take claims in all 56 Montana counties, from mountain towns and lake cabins to ranches on the eastern plains."),
    ]
    marquee_items = ["Hail", "Chinook wind", "Wildfire smoke", "Snow load", "Ice dams", "Frozen pipes", "Tornado", "Fire", "Billings", "Missoula", "Great Falls", "Bozeman", "Butte", "Helena", "Kalispell", "Havre", "Miles City"]
    mq = "".join(f"<li>{e(x)}</li>" for x in marquee_items)
    pledges = [
        ("scale", "Your appraiser, not theirs", "We’re appointed by you and owe the carrier nothing but a fair, supportable number."),
        ("ruler", "Measured on site", "Every valuation starts with our own inspection, photos and measurements."),
        ("file", "Line by line", "A full estimate priced for your part of Montana, not a percentage guess."),
    ]
    pl = "".join(f'<li class="rv">{ic(i)}<div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, t, p in pledges)
    svc = "".join(svc_card(s) for s in SERVICES)
    seasons = "".join(f'<li class="season rv">{ic(i)}<h3>{e(n)}</h3><small>{e(m)}</small><ul>{"".join(f"<li>{e(x)}</li>" for x in xs)}</ul></li>' for i, n, m, xs in SEASONS)
    regions = "".join(f'<article class="region rv">{img(ph, sizes="(max-width:700px) 100vw, 50vw", alt="")}<div class="region-b"><h3>{e(n)}</h3><small>{e(c)}</small><p>{e(t)}</p></div></article>' for n, c, t, ph in REGIONS)
    steps = [
        ("Free first look", f"Send the policy, the carrier’s estimate and your photos. A {K} reads them and tells you plainly whether appraisal fits."),
        ("Our own scope", "We inspect, measure and photograph, then build a line-item estimate priced for your area and season."),
        ("Written demand", "Appraisal is demanded in writing and we’re named as your appraiser within the policy’s timeline."),
        ("Panel work", "We go line by line with the carrier’s appraiser. Most differences narrow sharply here."),
        ("Signed award", "Anything still open goes to a neutral umpire. Two signatures set the amount of loss, and payment follows."),
    ]
    proc = "".join(f'<li class="rv"><span class="n">{i + 1:02d}</span><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))
    tools = "".join(tool_card(t) for t in TOOLS)
    locs = "".join(loc_card(l) for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    body = f"""
<section class="hero">
<div class="hero-ph">{img("hero-supercell", lazy=False, alt="", sizes="100vw")}</div>
<div class="wrap hero-in">
<div class="hero-tx">
<p class="eyebrow eyebrow-l">Independent property claim appraisal · all 56 counties</p>
<h1>{K}</h1>
<p class="hero-sub">For hail, wind, wildfire and winter claims that came back short.</p>
<p class="lede">When your insurer accepts the claim but the payment won’t put the roof, the walls or the barn back, {K} builds an independent, line-by-line valuation and takes it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn btn-amber" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-outline-l" href="#services">See what we handle</a></div>
</div>
{hero_form()}
</div>
</section>

<div class="marquee" aria-label="Claims and places we work"><ul>{mq}</ul><ul aria-hidden="true">{mq}</ul></div>

<section class="sec"><div class="wrap intro">
<div class="intro-tx rv">
<p class="eyebrow">Why people call us</p>
<h2>What a {K} does when a claim comes up short</h2>
<p class="big">Most underpaid Montana claims aren’t denied. They’re short: a roof slope missing from the estimate, steel siding priced as a patch, a pole barn left off, ice-and-water membrane nobody counted.</p>
<p>{K} works in the space between “covered” and “paid in full.” When either side invokes the appraisal clause, each names an appraiser, and the two of them, with an umpire if needed, set the amount of loss. As your {K}, we build the number you take to that table and defend it item by item.</p>
<a class="link" href="{ABOUT}">How our firm works</a>
</div>
<div class="intro-side">
<figure class="intro-ph rv">{img("roof-toolbelt", sizes="(max-width:900px) 100vw, 480px")}</figure>
<ol class="pledges" data-stagger>{pl}</ol>
</div>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Claim services</p><h2>Twelve ways a {K} can help</h2><p>From a quick estimate review to full appraisal clause representation and neutral umpire work, built around the losses Montana actually gets.</p></div>
<div class="sgrid" data-stagger>{svc}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">Compare all claim services {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Claim seasons</p><h2>Montana’s weather writes the claim calendar</h2><p>A {K} has to know what each season does to a building. Here’s when the calls come in.</p></div>
<ol class="seasons" data-stagger>{seasons}</ol>
</div></section>

<section class="sec sec-navy"><div class="wrap">
<div class="sec-head left rv"><p class="eyebrow eyebrow-l">Four Montanas</p><h2>One state, four very different claim climates</h2><p>Montana is the fourth-largest state, with 56 counties and terrain from glaciated peaks to badlands. A {K} working in Whitefish faces different losses than one working in Miles City, and the estimate has to show it.</p></div>
<div class="regions" data-stagger>{regions}</div>
</div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv sticky-col"><p class="eyebrow">The process</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding answer on the amount of loss.</p><a class="btn btn-line" href="{PROCESS}">Read the full appraisal roadmap {ic("arrow")}</a></div>
<ol class="trail" data-stagger>{proc}</ol>
</div></section>

<section class="sec sec-tint" id="snow-check"><div class="wrap split">
<div class="rv"><p class="eyebrow">Try it now</p><h2>How heavy is the snow on your roof?</h2><p>Depth alone doesn’t tell you much. Twenty inches of wind-packed snow weighs far more than twenty inches of fresh powder. Enter what’s up there for a quick, illustrative estimate.</p><p>The full <a href="{TOOL_BASE}roof-snow-load-estimator/">roof snow load estimator</a> handles multiple layers, roof area and total weight. It’s one of seven free tools from {K}.</p></div>
<div class="rv">{SNOW_MINI}</div>
</div></section>

<section class="sec sec-deep"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow eyebrow-l">Free claim toolkit</p><h2>Seven free tools built by a {K}</h2><p>Check the carrier’s math before you pick up the phone. Everything runs in your browser; nothing is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tools}</div>
<p class="center mt"><a class="btn btn-outline-l" href="{TOOL_BASE}">Open the claim toolkit {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Montana cities</p><h2>Where a {K} is called most often</h2><p>We take claims statewide. These twelve local pages cover the communities we hear from most.</p></div>
<div class="cgrid" data-stagger>{locs}</div>
<p class="center mt"><a class="link" href="{LOC_BASE}">All Montana cities and counties</a></p>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Straight talk</p><h2>When appraisal is the right tool, and when it isn’t</h2><p>A good {K} will tell you when to look elsewhere. Here’s the short version.</p></div>
<div class="fit">
<div class="fit-c fit-yes rv"><h3>{ic("check")}Appraisal tends to fit</h3><ul><li>The carrier accepted the claim but the estimate is short</li><li>The dispute is about price, quantity or repair method</li><li>You have the carrier’s line-item estimate and your own</li><li>The gap is large enough to justify the cost</li></ul></div>
<div class="fit-c fit-no rv"><h3>{ic("x")}Look elsewhere first</h3><ul><li>The whole claim was denied for coverage reasons</li><li>A deadline is days away (call a Montana attorney)</li><li>The gap is small and a supplement could close it</li><li>You suspect bad faith or unfair claim handling</li></ul></div>
</div></div></section>

<section class="sec"><div class="wrap split split-top">
<div class="rv"><p class="eyebrow">Questions</p><h2>Questions people ask a {K}</h2><p>Plain answers on how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_P}">All appraisal questions {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Claim dictionary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Field notes</p><h2>Read this before you demand appraisal</h2><p>Practical, Montana-specific guides on policy language, documentation and timing.</p></div>
<div class="ngrid" data-stagger>{posts}</div>
<p class="center mt"><a class="link" href="{POST_BASE}">All field notes</a></p>
</div></section>

<section class="sec sec-contact" id="contact"><div class="contact-ph">{img("red-barn-snow", alt="", sizes="100vw")}</div><div class="wrap contact">
<div class="contact-tx rv"><p class="eyebrow eyebrow-l">Start here</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. You’ll get a straight answer on whether appraisal is worth pursuing, with no pressure.</p>
<ul class="clines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>{HOURS}</span></li><li>{ic("pin")}<span><small>Coverage</small>All 56 Montana counties</span></li></ul></div>
<div class="rv">{lead_form(page="/", fid="c")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Hail, Wildfire & Snow Claims",
                        "Montana Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, wildfire and winter claims.",
                        body, schema, photo="hero-supercell", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def layout(article, aside):
    return f'<div class="wrap layout"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Claim services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[idx % 6: idx % 6 + 6]]
        ph = SVC_PHOTO[s["slug"]]
        article = s["body"] + f'<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}<h2>Related claim services</h2>' + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Claim service", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(article, call_box() + list_box("All claim services", items, path) + list_box("Montana cities", locs + [("All cities", LOC_BASE)])) + cta_band()
        svc = {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "State", "name": "Montana"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, s["title"], s["desc"], body, [crumbs_schema(trail), svc, faq_schema(s["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim services", SVC_BASE)]
    cards = "".join(svc_card(s, "h2") for s in SERVICES)
    body = page_hero(trail, "What we handle", "Insurance Appraisal Services in Montana",
                     "Twelve services built around one job: an accurate, defensible valuation of your loss. Start with an estimate review, or bring us in once appraisal has been demanded.", "desk-meeting") + f"""
<section class="sec"><div class="wrap"><div class="sgrid" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="eyebrow">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that difference is worth. A review answers that quickly, and some disputes close right there with a documented supplement.</p><a class="btn btn-navy" href="{SVC_BASE}insurance-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one stage?", "Yes. Many clients start with a review and decide later whether to demand appraisal."), ("Do you handle homes, ranches and commercial buildings?", "Yes: houses, cabins, condos, HOA communities, apartments, shops, churches, farm and ranch outbuildings and commercial buildings."), ("Do you handle hurricane claims?", "Montana doesn’t get hurricanes. Our work centers on hail, wind, wildfire, winter, water and fire losses.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Montana | 12 Services",
                             "Insurance appraisal services across Montana: appraisal clause representation, estimate review, hail, wind, wildfire, snow load and umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="desk-meeting"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Montana cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(l["hoods"])
        storms = "".join(f'<li><span class="yr">{e(str(y))}</span><span><b>{e(n)}</b> {e(t)}</span></li>' for y, n, t in l["storms"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
        near = related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        article = f"""<div class="localbox"><h2 class="lb-t">{e(l["city"])} at a glance</h2><ul class="chips">{chips}</ul><p><b>Housing:</b> {e(l["housing"])}</p><p><b>Neighborhoods and nearby areas:</b> {e(hoods)}</p></div>
{l["body"]}
<h2>Weather history around {e(l["city"])}</h2><ul class="mini-storms">{storms}</ul>
<h2>Claim services in {e(l["city"])}</h2><p>Every {BRAND} service is available to property owners in {e(l["city"])} and across {e(l["county"])}:</p><ul class="cols">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2>{near}"""
        aside = call_box() + list_box("Montana cities", items, path) + list_box("Claim toolkit", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(article, aside) + cta_band(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        svc = {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "City", "name": l["geo"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Montana"}}, "url": DOMAIN + path}
        write(path, document(path, l["title"], l["desc"], body, [crumbs_schema(trail), svc, faq_schema(l["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Montana cities", LOC_BASE)]
    cards = "".join(loc_card(l, "h2") for l in LOCATIONS)
    regions = "".join(f'<article class="region rv">{img(ph, sizes="(max-width:700px) 100vw, 50vw", alt="")}<div class="region-b"><h3>{e(n)}</h3><small>{e(c)}</small><p>{e(t)}</p></div></article>' for n, c, t, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 56 Montana Counties",
                     "We work statewide, from Libby to Ekalaka. These local pages cover the cities and towns where we’re called most often.", "great-falls") + f"""
<section class="sec"><div class="wrap"><div class="cgrid" data-stagger>{cards}</div></div></section>
<section class="sec sec-navy"><div class="wrap"><div class="sec-head left rv"><p class="eyebrow eyebrow-l">Regions</p><h2>How claims differ across Montana</h2><p>The same policy language plays out very differently on a Whitefish ski cabin, a Billings ranch house and a Havre machine shed.</p></div><div class="regions" data-stagger>{regions}</div></div></section>
{cta_band("Don’t see your town?", "We cover every county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Montana Cities We Serve | Appraisal in 56 Counties",
                             "Insurance appraisal in all 56 Montana counties, including Billings, Missoula, Great Falls, Bozeman, Butte, Helena, Kalispell and Havre.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="great-falls"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim toolkit", TOOL_BASE), (t["name"], path)]
        ph = t["photo"]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        article = t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>' + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Free {t['kind'].lower()} · nothing stored", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and all example figures are illustrative.</p></div></section>""" + layout(article, call_box() + list_box("Claim toolkit", items, path)) + cta_band("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")
        app = {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
               "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}
        write(path, document(path, t["title"], t["desc"], body, [crumbs_schema(trail), app, faq_schema(t["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim toolkit", TOOL_BASE)]
    cards = "".join(tool_card(t, "h2") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Montana Property Owners",
                     "Seven calculators, planners and checklists drawn from appraisal work. Use them to understand your claim, check the carrier’s math and plan next steps. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split split-top"><div class="rv"><p class="eyebrow">Suggested order</p><h2>Using the tools together</h2><ol class="olist"><li>Start with the <a href="{TOOL_BASE}claim-deadline-calendar/">claim deadline calendar</a> so no date slips, especially before winter.</li><li>Check roof quantities in the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’re really owed with the <a href="{TOOL_BASE}wind-hail-deductible-calculator/">wind/hail deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-calculator/">depreciation &amp; holdback</a> calculators.</li><li>In winter, estimate weight with the <a href="{TOOL_BASE}roof-snow-load-estimator/">roof snow load estimator</a>.</li><li>Test the dispute in the <a href="{TOOL_BASE}claim-gap-calculator/">claim gap calculator</a>, then score your file with the <a href="{TOOL_BASE}appraisal-readiness-quiz/">readiness quiz</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Claim Toolkit | 7 Calculators for Montana Claims",
                              "Free insurance claim tools: claim gap, depreciation holdback, roof squares, wind/hail deductible, deadline calendar, readiness quiz and snow load.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="calculator"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    learn_items = [("Appraisal roadmap", PROCESS), ("Appraisal questions", FAQ_P), ("Claim dictionary", GLOSS), ("Field notes", POST_BASE)]

    path, trail = PROCESS, [("Home", "/"), ("Appraisal roadmap", PROCESS)]
    toc = "".join(f'<li><a href="#stage-{i + 1}">{e(n)}</a></li>' for i, (n, _) in enumerate(PROCESS_STEPS))
    stages = "".join(f'<section class="stage" id="stage-{i + 1}"><h2><span>Stage {i + 1}</span>{e(n)}</h2>{h}</section>' for i, (n, h) in enumerate(PROCESS_STEPS))
    article = f'{PROCESS_INTRO}<nav class="toc" aria-label="Stages"><p class="toc-t">The {len(PROCESS_STEPS)} stages</p><ol>{toc}</ol></nav><div class="stages">{stages}</div>{PROCESS_OUTRO}'
    body = page_hero(trail, "Appraisal roadmap", "The Montana Insurance Appraisal Process, Step by Step",
                     f"{len(PROCESS_STEPS)} stages from the first disagreement to payment: what happens, who does what, and where claims most often stall.", "field-datasheet",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "Any 2 of 3 signatures")]) + layout(article, call_box() + list_box("Learn", learn_items, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Montana", "description": "The stages of a property insurance appraisal from dispute to award and payment.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#stage-{i + 1}"} for i, (n, _) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Montana Insurance Appraisal Process | 8-Stage Roadmap",
                         "How property insurance appraisal works in Montana: the written demand, choosing appraisers, the umpire, inspection, negotiation, award and payment.",
                         body, [crumbs_schema(trail), howto], photo="field-datasheet"), 0.8)

    path, trail = FAQ_P, [("Home", "/"), ("Appraisal questions", FAQ_P)]
    jump = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions, Answered for Montana",
                     f"{len(allq)} plain answers grouped by topic: the basics, costs and timing, Montana specifics, hail, wind, wildfire and winter, and what happens after the award.", "signing") + layout(
        f'<nav class="toc" aria-label="Topics"><p class="toc-t">Jump to a topic</p><ul>{jump}</ul></nav>{groups}', call_box() + list_box("Learn", learn_items, path)) + cta_band("Didn’t see your question?", "Call or email and we’ll talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ | Montana Costs, Timing & Rules",
                         "Answers to common Montana insurance appraisal questions, grouped by topic: basics, costs, timing, state specifics, storm claims and the award.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="signing"), 0.8)

    path, trail = GLOSS, [("Home", "/"), ("Claim dictionary", GLOSS)]
    gl = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in gl})
    az = "".join(f'<a href="#t-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in gl:
        c = term[0].upper()
        anchor = f' id="t-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    article = f'<div class="gfilter"><label for="gloss-filter">Search {len(gl)} terms</label><input id="gloss-filter" type="search" placeholder="Try “holdback”, “umpire” or “snow load”" autocomplete="off"><p class="hint" data-gcount aria-live="polite"></p></div><nav class="az" aria-label="Letters">{az}</nav><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Montana Claim Dictionary: Insurance Terms in Plain English",
                     f"{len(gl)} words you’ll meet in policies, estimates and appraisal awards, from actual cash value to wildland-urban interface. Type in the box to filter.", "notebook", cta=False) + layout(article, call_box() + list_box("Learn", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Montana property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in gl]}
    write(path, document(path, "Insurance Claim Dictionary | ACV, Umpire, Snow Load & More",
                         "A searchable dictionary of property insurance claim terms: actual cash value, holdback, umpire, wind/hail deductible, snow load, CSI and more.",
                         body, [crumbs_schema(trail), dts], photo="notebook"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Field notes", POST_BASE), (p["title"], path)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        others = [o for o in POSTS if o is not p][:3]
        article = f'<p class="byline">By the {BRAND} team · Published {nice} · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2>' + related([("Field note", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Field note · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(article, call_box() + list_box("Learn", learn_items) + list_box("Claim toolkit", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_band()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path, trail = POST_BASE, [("Home", "/"), ("Field notes", POST_BASE)]
    cards = "".join(post_card(p, "h2") for p in POSTS)
    body = page_hero(trail, "Field notes", "Field Notes: Montana Insurance Appraisal Guides",
                     "Practical, Montana-specific guides on policy language, hail, wildfire, winter losses and building a claim file that holds up.", "roof-eave-damage", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ngrid" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Field Notes | Montana Insurance Appraisal Guides",
                         "Guides for Montana property owners on the appraisal clause, hail roofs, wildfire smoke, snow load, unfair claim practices and claim files.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="roof-eave-damage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path, trail = ABOUT, [("Home", "/"), ("About our firm", ABOUT)]
    article = f"""<figure class="lead-img">{img("desk-meeting", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Plenty of claim professionals do a little of everything. {BRAND} focuses on the amount of loss: what it genuinely costs to put a damaged Montana property back the way it was. Our process, documentation and free tools all serve that question. Depending on the claim, we act as your appointed appraiser, review an estimate before a dispute hardens, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before price.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate looks good on day one and loses credibility with an umpire. We price what we can defend.</li>
<li><strong>Montana pricing.</strong> Labor, materials and travel cost differently in Big Sky than in Glendive. Estimates should reflect where the property actually is.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or simply a supplement, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost and how we’re paid before work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, cabin owners, landlords, HOA boards, property managers, churches, business owners, farm and ranch families, contractors and attorneys across Montana. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Montana produces a wide spread of property losses: hail on the plains and the Hi-Line, downslope windstorms along the Rocky Mountain Front, wildfire and smoke in the western valleys, heavy snow and ice dams in the mountains, and frozen pipes everywhere. Working all 56 counties keeps us current on every one of them. For questions about the state’s insurance rules, the Office of the Montana Commissioner of Securities and Insurance publishes consumer guidance and accepts complaints.</p>"""
    body = page_hero(trail, "About our firm", f"About {BRAND}",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "house-in-pines") + layout(
        article, call_box() + list_box("Explore", [("Claim services", SVC_BASE), ("Montana cities", LOC_BASE), ("Claim toolkit", TOOL_BASE), ("Appraisal roadmap", PROCESS)])) + cta_band()
    write(path, document(path, f"About Our Firm | {BRAND}",
                         "Montana Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="house-in-pines"), 0.7)

    path, trail = CONTACT, [("Home", "/"), ("Get in touch", CONTACT)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "signing", cta=False) + f"""
<section class="sec"><div class="wrap contact contact-page">
<div class="rv"><p class="eyebrow">Direct lines</p><h2>Reach us directly</h2>
<ul class="clines clines-d"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>{HOURS}</span></li><li>{ic("pin")}<span><small>Service area</small>Statewide, all 56 counties</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}Your declarations page</li><li>{ic("check")}The carrier’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the carrier</li><li>{ic("check")}Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hl="h2")}</div></div></section>"""
    write(path, document(path, f"Contact Us | {BRAND}",
                         "Get a free review of a disputed Montana property claim. Call or text (844) 537-1427, email us, or send your claim details through the form.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="signing"), 0.8)

    lic = {"cc0": "CC0 1.0 (public domain dedication)", "pdm": "Public Domain Mark"}
    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td><b>{e(v["title"])}</b><br><small>{e(v.get("creator") or "Unknown creator")} · via {e(v["source"].title())}</small><br><small class="muted">Used on this site as: {e(ALT[k])}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Notice", "privacy notice", f"""<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web host records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The figures you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics through Google Tag Manager, this notice will be updated to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To see, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Terms of Service", "terms of service", f"""<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. The content is general information about insurance appraisal and property claims in Montana.</p>
<h2>No professional relationship</h2><p>Reading the site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Consult a licensed Montana attorney about legal questions.</p>
<h2>Tools and examples</h2><p>Our tools give planning estimates from the figures you enter. They aren’t appraisals, quotes, engineering assessments or predictions of any outcome, and example figures throughout the site are illustrative.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Montana.</p>""", "The terms that apply when you use this website and its claim tools."),
        DISCLAIM: ("Site Disclaimer", "site disclaimer", f"""<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Statutes, agencies and storms</h2><p>References to Montana statutes, the Commissioner of Securities and Insurance, the surplus-lines market or past storms and fires are for context only and described in general terms. Verify current law and facts with official sources and a licensed Montana attorney.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is approaching, consult an attorney promptly.</p>
<h2>Snow load and safety</h2><p>The roof snow load estimator uses typical snow densities and is not an engineering assessment. If a roof shows signs of distress, leave the building and contact a qualified professional.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website."),
        CREDITS: ("Photo Credits", "photo credits", f"""<p>Every photograph on this site is either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or marked as a <strong>public-domain</strong> work, including photos by U.S. government agencies such as NOAA, the USDA and Forest Service, the National Park Service, the Bureau of Land Management, the NRCS and the U.S. Fish and Wildlife Service. We found them through the Openverse search engine. Attribution isn’t legally required, but we credit the creators here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for every photograph used on this site."),
    }
    for path, (title, kw, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "helena-capitol", cta=False) + layout(content, call_box())
        desc = f"The {kw} for {BRAND} ({HOST}): {lede[0].lower() + lede[1:]}"
        if len(desc) > 150:
            desc = f"The {kw} for {BRAND}: {lede[0].lower() + lede[1:]}"
        if len(desc) < 110:
            desc = desc[:-1] + ", for property owners across Montana."
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="helena-capitol"), 0.3)


def sitemap_pages():
    path, trail = HTMLMAP, [("Home", "/"), ("Site index", HTMLMAP)]
    groups = [
        ("Main", [("Home", "/"), ("About our firm", ABOUT), ("Get in touch", CONTACT)]),
        ("Claim services", [("All claim services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Montana cities", [("All Montana cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim toolkit", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", [("Appraisal roadmap", PROCESS), ("Appraisal questions", FAQ_P), ("Claim dictionary", GLOSS), ("Field notes", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy notice", PRIVACY), ("Terms of service", TERMS), ("Site disclaimer", DISCLAIM), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on the {BRAND} website, grouped by section.", "helena-capitol", cta=False) + f'<section class="sec"><div class="wrap mapgrid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"An HTML site index listing every page on {BRAND}: claim services, Montana cities, free tools, field notes and legal pages.", body, [crumbs_schema(trail)], photo="helena-capitol"), 0.3)

    body = f"""<section class="ihero ihero-404"><div class="ihero-ph">{img("snow-broken-trees", lazy=False, alt="")}</div><div class="wrap ihero-in"><div class="ihero-tx"><p class="eyebrow eyebrow-l">Error 404</p><h1>This page didn’t make it through the winter</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-amber" href="/">Home</a><a class="btn btn-outline-l" href="{SVC_BASE}">Services</a><a class="btn btn-outline-l" href="{TOOL_BASE}">Toolkit</a><a class="btn btn-outline-l" href="{CONTACT}">Contact</a></div></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, noindex=True, photo="snow-broken-trees"), sitemap=False)


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
// Montana Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$home = 'https://__HOST__';

// Canonical host and scheme, only on the real domain (TLS terminates upstream).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off' ? 'http' : 'https'));
if ($host === 'www.__HOST__' || ($host === '__HOST__' && $proto === 'http')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== '__HOST__') {
    header('X-Robots-Tag: noindex, nofollow');
}
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
$serve = function (string $file, int $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile($file);
    exit;
};
if ($path === '/' || $path === '/index.php') {
    $serve(__DIR__ . '/home.html');
}
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    $serve(__DIR__ . $path . 'index.html');
}
$serve(__DIR__ . '/404.html', 404);
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
