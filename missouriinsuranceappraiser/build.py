#!/usr/bin/env python3
"""Static site generator for missouriinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Only the Python 3 standard library is needed. Engineering pattern from georgiainsuranceappraiser/;
copy, slugs and design are Missouri's own.
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
from learn import PROCESS_INTRO, PROCESS_STEPS, PROCESS_OUTRO, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Missouri Insurance Appraiser"
HOST = "missouriinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261109a"
FAV = "1"
# Google Tag Manager container, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""

SVC_BASE = "/appraisal-help/"
LOC_BASE = "/communities/"
TOOL_BASE = "/toolkit/"
POST_BASE = "/field-notes/"
ABOUT, CONTACT = "/our-firm/", "/get-in-touch/"
PROCESS, FAQ_P, GLOSS = "/appraisal-roadmap/", "/questions-answered/", "/appraisal-dictionary/"
PRIVACY, TERMS, DISCLAIM, CREDITS, HTMLMAP = "/privacy-notice/", "/terms-of-service/", "/site-disclaimer/", "/photo-credits/", "/site-index/"
HOURS = "Mon–Fri, 8am–6pm CT"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, MO"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hailstones-hand": "Hand holding a pile of large hailstones after a storm",
    "hail-field": "Hailstones scattered across green grass after a storm",
    "storm-before-hail": "Dark storm clouds building over open farmland before a hailstorm",
    "shingle-delivery": "Boom truck lifting bundles of roof shingles onto a house",
    "tornado-cleanup": "Excavator clearing debris from homes destroyed by a tornado",
    "tornado-funnel": "Dark tornado cloud lowering over open country",
    "tornado-mesocyclone": "Tornado funnel touching down beneath a storm cloud",
    "lightning-city": "Lightning flashing inside storm clouds above a city at dusk",
    "storm-grain-elevator": "Storm clouds rolling over flat farmland and a rural road",
    "storm-farm-field": "Rain shaft falling from storm clouds over a grassy field",
    "house-green-field": "Farmhouse under heavy storm clouds at the edge of a field",
    "storm-ominous-plains": "Storm clouds over a two-lane road and a grain elevator",
    "ice-storm-road": "Broken tree limbs coated in ice lying across a road after an ice storm",
    "ice-storm-path": "Ice-laden trees bent over a snowy lane after an ice storm",
    "iced-branches": "Long icicles hanging from a roof edge beside a window",
    "icicles-window": "Close-up of icicles formed along a frozen ledge",
    "ceiling-water-damage": "Collapsed, water-stained ceiling inside a bedroom",
    "roof-eave-damage": "Damaged roof edge with torn shingles and exposed boards",
    "two-story-house": "Two-story frame house with a front porch and green lawn",
    "storm-demolition": "Excavator demolishing a storm-damaged frame house",
    "sinkhole-yard": "Large sinkhole opened in a front yard near a house",
    "sinkhole-repair": "Road crew with a backhoe filling a sinkhole in the pavement",
    "sinkhole-lawn": "Sinkhole collapsed into a lawn in front of brick homes",
    "porch-house-blue": "Blue two-story house with a covered front porch",
    "craftsman-porch": "Brick bungalow with a deep front porch and bicycle",
    "red-brick-house": "Historic red brick house with arched windows",
    "apartments-brick": "Brick and white apartment buildings beside a pond",
    "brick-warehouse": "Five-story red brick warehouse building",
    "brick-church": "Red brick church buildings on a city street corner",
    "warehouse-stocksnap": "White commercial building with large windows",
    "work-papers": "Person reviewing printed papers at a desk",
    "meeting-a": "Notebook and papers on a meeting table",
    "meeting-c": "People talking through a document in a meeting",
    "kc-union-station": "Union Station and the Kansas City, Missouri skyline from Liberty Memorial hill",
    "kc-skyline": "Downtown Kansas City, Missouri skyline on a clear day",
    "stl-courthouse-view": "Downtown St. Louis and the Old Courthouse seen from the Gateway Arch",
    "stl-downtown": "Aerial view of downtown St. Louis, Missouri",
    "stl-river-bridges": "Bridges crossing the Mississippi River at St. Louis",
    "springfield-city-hall": "Historic stone city hall building in Springfield, Missouri",
    "springfield-route66": "Old brick and frame gas station buildings in Springfield, Missouri",
    "columbia-mizzou": "The Columns and Academic Hall at the University of Missouri in Columbia",
    "jefferson-capitol": "Missouri State Capitol in Jefferson City seen from above",
    "jefferson-flood-1993": "Missouri River floodwaters covering low ground at Jefferson City in 1993",
    "joplin-debris": "Excavator removing tornado debris in Joplin, Missouri, with a flag on the wreckage",
    "stjoe-barn": "Weathered barn and trees near St. Joseph, Missouri",
    "cape-bridge": "Bill Emerson Memorial Bridge over the Mississippi at Cape Girardeau at night",
    "ozarks-lake": "Lake and bluffs in the Missouri Ozarks",
    "independence-house": "Restored historic frame house in Independence, Missouri",
    "stl-flood-1993": "Pump truck spraying floodwater out of a flooded area",
    "calculator-paper": "Calculator resting on printed estimate pages",
    "calculator-blue": "Blue calculator, pencil and sticky notes on a desk",
    "calculator-laptop": "Calculator and laptop beside printed charts",
    "colorful-houses": "Row of colorful two-story houses",
    "snowy-brick-street": "Snow falling on a street of brick row houses",
    "firefighters-hose": "Firefighters laying hose beside a fire truck",
    "burned-apartment": "Burned-out apartment building with collapsed walls",
    "soot-wall": "Black soot stain running up a brick wall",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "meeting-c", "homeowner-claim-appraisal": "porch-house-blue",
    "commercial-hoa-appraisal": "apartments-brick", "hail-roof-damage-appraisal": "hailstones-hand",
    "tornado-straight-line-wind-appraisal": "tornado-cleanup", "burst-pipe-water-damage-appraisal": "ceiling-water-damage",
    "fire-smoke-damage-appraisal": "burned-apartment", "sinkhole-ground-collapse-appraisal": "sinkhole-yard",
    "winter-storm-ice-damage-appraisal": "ice-storm-road", "insurer-estimate-review": "calculator-paper",
    "appraisal-umpire-services": "work-papers",
}
LOC_PHOTO = {
    "kansas-city": "kc-skyline", "st-louis": "stl-courthouse-view", "springfield": "springfield-city-hall", "columbia": "columbia-mizzou",
    "independence": "independence-house", "lees-summit": "craftsman-porch", "st-charles": "red-brick-house", "st-joseph": "stjoe-barn",
    "joplin": "joplin-debris", "jefferson-city": "jefferson-capitol", "cape-girardeau": "cape-bridge", "chesterfield": "two-story-house",
}
TOOL_PHOTO = {
    "award-net-payout-estimator": "calculator-blue", "depreciation-recovery-calculator": "calculator-laptop",
    "roof-measurement-calculator": "shingle-delivery", "hail-deductible-calculator": "hail-field",
    "claim-calendar-builder": "meeting-a", "appraisal-readiness-score": "work-papers",
    "roof-repair-or-replace-splitter": "roof-eave-damage",
}
POST_PHOTO = {
    "missouri-appraisal-clause-walkthrough": "meeting-c", "hail-claims-missouri-roofs": "hailstones-hand",
    "vexatious-refusal-vs-appraisal": "calculator-paper", "tornado-rebuild-total-loss": "storm-demolition",
    "sinkholes-earth-movement-new-madrid": "sinkhole-lawn", "missouri-fair-plan-claims": "snowy-brick-street",
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
    "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


MARK_INNER = ('<rect width="48" height="48" rx="12" fill="url(#{g})"/>'
              '<path d="M12.5 38V35C12.5 20 16.5 11 24 11S35.5 20 35.5 35V38" fill="none" stroke="#f6efe5" stroke-width="3.4" stroke-linecap="round"/>'
              '<path d="M18.5 31.5L24 26l5.5 5.5" fill="none" stroke="#5fc1c4" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M8.5 38.5h31" stroke="#5fc1c4" stroke-width="3.2" stroke-linecap="round"/>')


def mark(uid="m", size=44):
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#5a3a22"/><stop offset="1" stop-color="#170d06"/></linearGradient></defs>' + MARK_INNER.format(g=uid) + '</svg>')


def brand(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span class="brand-t"><b>Missouri</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "MO", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MO", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 114 Missouri counties and the City of St. Louis.",
        "areaServed": [{"@type": "State", "name": "Missouri"}] + [{"@type": "City", "name": l["geo"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Tornado damage", "Sinkhole claims", "Ice storm damage"],
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
        ("Appraisal help", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("Every service", SVC_BASE)),
        ("Communities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All of Missouri", LOC_BASE)),
        ("Toolkit", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All seven tools", TOOL_BASE)),
        ("Learn", [("Appraisal roadmap", PROCESS), ("Questions answered", FAQ_P), ("Appraisal dictionary", GLOSS), ("Field notes", POST_BASE)], None),
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
            li += f'<li class="dd-all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        menu += f'<li class="has-dd"><button type="button" data-dd aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="dd{" dd-wide" if len(links) > 7 else ""}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="nav-a" href="{ABOUT}">Our firm</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-p" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="mast" id="top"><div class="wrap mast-in">
{brand("mh")}
<nav class="nav" aria-label="Main"><ul class="nav-l">{menu}</ul></nav>
<div class="mast-act"><a class="mast-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-teal mast-cta" href="{CONTACT}">Free claim review</a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button></div>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{ABOUT}">Our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="{CONTACT}">Send claim details</a><small>{HOURS} · all of Missouri</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="wrap foot-top">
<div class="foot-brand">{brand("mf")}
<p>Independent appraisal, estimate review and umpire work for Missouri property owners whose insurance claim is covered but underpaid.</p>
<ul class="foot-reach"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>{HOURS}</span></li></ul></div>
<div><h2 class="foot-h">Appraisal help</h2><ul>{svc}</ul></div>
<div><h2 class="foot-h">Communities</h2><ul class="foot-2">{loc}</ul><h2 class="foot-h foot-gap">Toolkit</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Firm &amp; learning</h2><ul><li><a href="{ABOUT}">Our firm</a></li><li><a href="{CONTACT}">Get in touch</a></li><li><a href="{PROCESS}">Appraisal roadmap</a></li><li><a href="{FAQ_P}">Questions answered</a></li><li><a href="{GLOSS}">Appraisal dictionary</a></li><li><a href="{POST_BASE}">Field notes</a></li></ul></div>
</div>
<div class="wrap foot-base"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we don’t give legal advice, and we don’t act as public adjusters. Content is general and educational, policy terms vary, results are never guaranteed, and example figures are illustrative.</p>
<div class="foot-row"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{HTMLMAP}">Site index</a></li></ul></div></div>
</footer>
<a class="totop" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a href="{CONTACT}">Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", noindex=False, photo="storm-before-hail"):
    canonical = DOMAIN + path
    ld = build_graph(path, title, desc, schema, photo, noindex)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {PHOTOS[photo]["fw"]}w" imagesizes="100vw" fetchpriority="high">'
    og_alt = f"{BRAND}: independent property claim appraisal across Missouri"
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
<meta name="geo.region" content="US-MO">
<meta name="geo.placename" content="Missouri">
<meta name="theme-color" content="#2A1A0E">
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
    parts = [f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + "</nav>"


def banner(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btns"><a class="btn btn-teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="banner"><div class="banner-ph">{img(photo, lazy=False, alt="")}</div><div class="wrap banner-in">{crumbs(trail)}<p class="tag tag-l">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="qa">' + "".join(f'<details><summary>{e(q)}</summary><div class="qa-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="sbox sbox-call"><h2 class="sbox-t">Talk through your claim</h2><p>No cost for the first conversation. We’ll tell you plainly whether appraisal fits.</p><a class="sbox-tel" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn btn-teal btn-block" href="{CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="sbox"><h2 class="sbox-t">{e(title)}</h2><ul class="sbox-list">{li}</ul></div>'


def finale(h="Claim covered, check too small?", p="Send the insurer’s estimate and a few photos. We’ll tell you what we see, at no cost.", photo="storm-ominous-plains"):
    return f"""<section class="finale">{img(photo, "finale-ph", alt="", extra=' data-parallax="0.16"')}<div class="wrap finale-in rv"><h2>{e(h)}</h2><p>{e(p)}</p><div class="btns"><a class="btn btn-teal" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def nextlinks(items):
    return '<div class="nextl">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Tornado / wind", "Ice storm / freeze", "Water / burst pipe", "Fire / smoke", "Sinkhole / collapse", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hl="h2"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Landlord", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Missouri"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="form-t">{e(heading)}</{hl}><p class="form-sub">No cost, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the insurer paid or offered, and what you think was missed."></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy notice</a>.</span></label></div>
<div class="full"><button class="btn btn-dark btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="ticket" action="/api/contact.php" method="post" data-lead novalidate>
<p class="ticket-t">Free claim review</p><p class="ticket-s">Three fields. A call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy notice</a>.</span></label>
<button class="btn btn-teal btn-block" type="submit">Request my review {ic("arrow")}</button>
<p class="ticket-f">{ic("lock")} Private. No obligation.</p>
<div class="form-msg" role="status"></div>
</form>"""


def svc_card(s, n, h="h3"):
    return f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/"><span class="scard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="scard-n">{n:02d}</span></span><span class="scard-b"><{h}>{e(s["name"])}</{h}><span class="scard-p">{e(s["short"])}</span><span class="more">Read more {ic("arrow")}</span></span></a>'


def svc_cta():
    return f'<a class="scard scard-cta rv" href="{CONTACT}"><span class="cta-k">Not sure which fits?</span><span class="cta-t">Send us the estimate and we’ll tell you.</span><span class="scard-p">One free conversation, an honest read on whether appraisal makes sense, and no obligation.</span><span class="more">Start a free review {ic("arrow")}</span></a>'


def tool_cta():
    return f'<a class="tcard tcard-cta rv" href="{CONTACT}"><span class="cta-k">Prefer a person?</span><span class="cta-t">Have an appraiser check the numbers</span><span class="tcard-p">Send the insurer’s estimate and we’ll review it line by line, at no cost for the first look.</span></a>'


def town_card(l, h="h3"):
    return f'<a class="town rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 300px", alt="")}<span class="town-b"><small>{e(l["county"])}</small><{h}>{e(l["city"])}</{h}></span></a>'


def tool_card(t, h="h3"):
    return f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 200px", alt="")}</span><span class="tcard-b"><span class="chip">{e(t["kind"])}</span><{h}>{e(t["name"])}</{h}><span class="tcard-p">{e(t["short"])}</span></span></a>'


def note_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return f'<article class="ncard rv"><a class="ncard-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="ncard-b"><span class="meta">{nice} · {p["read"]} read</span><{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>'


# ---------------------------------------------------------------- home
MONTHS = "JFMAMJJASOND"
SEASON = [  # peril, intensity per month 0-3, note
    ("Hail", [0, 0, 1, 3, 3, 3, 2, 1, 1, 0, 0, 0], "Peaks April to June, statewide"),
    ("Tornadoes", [0, 0, 1, 2, 3, 2, 1, 0, 0, 1, 1, 1], "Spring peak, with a second, smaller fall and early-winter season"),
    ("Derechos &amp; straight-line wind", [0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0], "Summer storm complexes, often overnight"),
    ("Ice storms &amp; freezes", [3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2], "December through February"),
    ("River &amp; flash flooding", [0, 1, 2, 3, 3, 3, 2, 1, 1, 1, 0, 0], "Spring rains; needs separate flood coverage"),
    ("Burst pipes", [3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2], "Hard freezes, vacant and seasonal homes"),
]

REGIONS = [
    ("Kansas City Metro", "Kansas City · Independence · Lee’s Summit", "Spring hail tracks across Jackson, Clay and Cass counties, landing on brick bungalows in Brookside and new HOA subdivisions alike.", "kc-union-station"),
    ("St. Louis Metro", "St. Louis · Chesterfield · St. Charles", "Old brick flats and slate roofs in the city, ranch homes in the county, and river-bottom flood history in Chesterfield Valley.", "stl-river-bridges"),
    ("Mid-Missouri", "Columbia · Jefferson City", "Tornadoes, Missouri River flooding and hail over university housing and older capital-city neighborhoods.", "jefferson-flood-1993"),
    ("Ozarks", "Springfield · Branson · Rolla", "Karst ground with thousands of mapped sinkholes, ice storms like January 2007, and wooded lots where limbs meet roofs.", "ozarks-lake"),
    ("Southwest Missouri", "Joplin · Carthage · Neosho", "Tornado Alley’s eastern edge. Rebuilding after 2011 shaped how this corner of the state thinks about code upgrades.", "tornado-funnel"),
    ("Northwest &amp; Bootheel", "St. Joseph · Cape Girardeau", "Missouri and Mississippi river towns with farm buildings, historic brick downtowns and New Madrid earthquake questions.", "stjoe-barn"),
]

STORMS = [
    ("1811–12", "New Madrid earthquakes", "A series of major quakes centered in the Bootheel; the seismic zone is why earthquake coverage comes up in southeast Missouri."),
    ("1993", "The Great Flood", "Missouri and Mississippi river flooding reached homes and businesses from St. Joseph to St. Charles County and Cape Girardeau."),
    ("2001", "I-70 hailstorm", "An April storm along the I-70 corridor in the St. Louis area became one of the costliest hail events of its time."),
    ("2006", "St. Louis derecho", "July windstorms brought down trees and lines across the St. Louis area and left many without power for days."),
    ("2007", "January ice storm", "Freezing rain coated southwest Missouri, including Springfield, snapping limbs onto roofs and cars."),
    ("2011", "Joplin tornado", "On May 22 an EF5 tornado cut across Joplin, one of the most destructive tornadoes in U.S. history."),
    ("2019", "Jefferson City tornado", "An EF3 tornado struck the capital city on May 22, eight years to the day after Joplin, as river flooding built nearby."),
    ("2021", "December tornadoes", "A rare December outbreak included a tornado in the Defiance area of St. Charles County."),
]


def home():
    K = BRAND
    steps = [
        ("Free first look", f"Send the insurer’s estimate and your photos. A {K} reviews the policy and tells you honestly whether appraisal makes sense."),
        ("Measure and price it ourselves", "We inspect, measure and write an independent line-item estimate priced for your part of Missouri, not a markup of the insurer’s."),
        ("Demand appraisal in writing", "If the gap is worth it, appraisal is invoked under your policy’s clause and we’re named as your appraiser within its time limit."),
        ("Work the differences", "We go item by item with the insurer’s appraiser. Most disagreements shrink here, once both sides see the same evidence."),
        ("Signed award", "Anything left goes to a neutral umpire. Two signatures out of three set the amount of loss, and payment follows the policy’s terms."),
    ]
    home_faqs = [
        (f"What does a {K} actually do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appraiser we inspect, write an independent line-item estimate, work with the insurer’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When does it make sense to call a {K}?", "When coverage has been accepted, you have the insurer’s itemized estimate, and the gap between it and a qualified contractor’s estimate is meaningful, often more than about 10% or several thousand dollars."),
        ("Does appraisal decide whether my claim is covered?", "Generally no. Appraisal sets the amount of loss. Coverage disputes, denials and questions under Missouri’s vexatious refusal statutes are legal matters for a Missouri attorney."),
        ("What does appraisal cost?", "Most clauses say each side pays its own appraiser and splits the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my part of Missouri?", "Yes. We work in all 114 counties and the City of St. Louis, from the Kansas City metro to the Bootheel."),
    ]

    cards = "".join(svc_card(s, i + 1) for i, s in enumerate(SERVICES)) + svc_cta()
    season_rows = "".join(
        f'<div class="srow"><span class="sname">{n}</span><span class="scells">' + "".join(f'<i class="lv{v}" title="{MONTHS[i]}"></i>' for i, v in enumerate(vals)) + f'</span><span class="snote">{t}</span></div>'
        for n, vals, t in SEASON)
    months = '<div class="srow shead" aria-hidden="true"><span class="sname"></span><span class="scells">' + "".join(f"<b>{m}</b>" for m in MONTHS) + '</span><span class="snote"></span></div>'
    stack = "".join(f'<li class="stack-c" style="--i:{i}"><span class="stack-n">Step {i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    mosaic = "".join(f'<article class="tile rv">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 400px", alt="")}<div class="tile-b"><small>{c}</small><h3>{n}</h3><p>{t}</p></div></article>' for n, c, t, ph in REGIONS)
    ledger = "".join(f'<li class="rv"><span class="yr">{e(y)}</span><div><h3>{e(n)}</h3><p>{e(t)}</p></div></li>' for y, n, t in STORMS)
    tools = "".join(tool_card(t) for t in TOOLS) + tool_cta()
    towns = "".join(town_card(l) for l in LOCATIONS)
    notes = "".join(note_card(p) for p in POSTS[:3])

    body = f"""
<section class="lead">
<div class="lead-ph">{img("storm-before-hail", lazy=False, alt="")}</div>
<div class="wrap lead-in">
<div class="lead-copy">
<p class="tag tag-l">Independent property claim appraisal · Statewide</p>
<h1>{K}: <span class="hl">a fair number</span> for your covered claim</h1>
<p class="lede">Hail, tornado, ice and sinkhole claims across the state get accepted and then underpaid. A {K} measures the damage, prices it independently and carries the dispute through the appraisal clause already written into your policy.</p>
<div class="btns"><a class="btn btn-teal" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="#help">See how we help {ic("arrow")}</a></div>
<ul class="ticks-l"><li>{ic("check")}Your appraiser, not the insurer’s</li><li>{ic("check")}Line-item estimates priced for Missouri</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="tally" aria-label="At a glance"><div class="wrap"><div class="tally-in rv">
<div><b data-count="114">114</b><span>counties plus the City of St. Louis</span></div>
<div><b data-count="11">11</b><span>appraisal and estimating services</span></div>
<div><b data-count="7">7</b><span>free tools that run in your browser</span></div>
<div><b>2 of 3</b><span>signatures make an award binding</span></div>
</div></div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-h"><p class="tag">Why owners call</p><h2>What a {K} does that the claim process doesn’t</h2><figure class="intro-ph rv">{img("shingle-delivery", sizes="(max-width:900px) 100vw, 420px")}</figure></div>
<div class="intro-b rv">
<p class="big">Most underpaid claims in Missouri aren’t denied. They’re short: a missed slope on a hail-hit roof, gutters left off, siding that can’t be matched, or a code upgrade nobody priced.</p>
<p>The insurer’s adjuster writes one estimate. When yours says something different, you need more than an argument; you need an itemized valuation that stands up when someone checks it. That is the job of a {K}. We build the number from our own inspection and measurements, then use the appraisal clause to get it in front of a panel that can settle it.</p>
<div class="two-col">
<div class="fitbox"><h3>{ic("check")} Appraisal fits when</h3><ul><li>The insurer accepts the loss but disputes the cost</li><li>Repair-versus-replace is the sticking point</li><li>Matching or discontinued materials are at issue</li><li>Trades, code items or overhead and profit were left out</li></ul></div>
<div class="fitbox fitbox-no"><h3>{ic("x")} It usually doesn’t when</h3><ul><li>The whole claim was denied</li><li>Bad faith or vexatious refusal is the real issue</li><li>The gap is too small to cover fees</li><li>A deadline needs a Missouri attorney first</li></ul></div>
</div>
<p>Not sure which side of the line you’re on? A {K} will tell you on the first call, including when the honest answer is a supplement request or a lawyer.</p>
<a class="btn btn-dark" href="{ABOUT}">How our firm works {ic("arrow")}</a>
</div>
</div></section>

<section class="sec sec-parch" id="help"><div class="wrap">
<div class="sec-h rv"><p class="tag">Appraisal help</p><h2>Eleven ways a {K} can help with your claim</h2><p>Every service comes back to one question: what does it honestly cost to put this property back? Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="sgrid">{cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h sec-h-l rv"><p class="tag">Missouri’s claim calendar</p><h2>When Missouri weather turns into claims</h2><p>Each row shows how often a peril tends to drive claims through the year. A {K} sees spring hail and tornado files first, ice and frozen-pipe files in winter, and wind from summer storm complexes in between.</p></div>
<div class="season rv" role="img" aria-label="Chart of Missouri property claim perils by month: hail peaks April to June, tornadoes in spring with a smaller fall season, straight-line wind in summer, ice storms and burst pipes December through February, flooding in spring.">{months}{season_rows}</div>
<p class="season-key" aria-hidden="true"><i class="lv1"></i>Occasional <i class="lv2"></i>Common <i class="lv3"></i>Peak</p>
</div></section>

<section class="sec sec-dark"><div class="wrap stack-wrap">
<div class="stack-h"><p class="tag tag-l">The process</p><h2>How a {K} moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here are the five steps, start to finish.</p><a class="btn btn-ghost" href="{PROCESS}">Read the full roadmap {ic("arrow")}</a></div>
<ol class="stack">{stack}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="tag">Statewide</p><h2>Six regions, six kinds of claims</h2><p>Brick flats in St. Louis, HOA roofs in Lee’s Summit, sinkholes near Springfield and river towns in the Bootheel. A {K} has to know how each region’s weather shows up in an estimate.</p></div>
<div class="mosaic">{mosaic}</div>
</div></section>

<section class="sec sec-parch"><div class="wrap ledger-wrap">
<div class="ledger-h rv"><p class="tag">Storm history</p><h2>The storms Missouri still talks about</h2><p>These events shaped how insurers, contractors and owners in Missouri handle claims today. Every {K} file is a smaller version of the same story: damage, an estimate, and a question about what it really costs.</p><figure class="ledger-ph">{img("tornado-mesocyclone", sizes="(max-width:900px) 100vw, 420px")}</figure></div>
<ol class="ledger">{ledger}</ol>
</div></section>

<section class="sec"><div class="wrap gapsplit">
<div class="rv"><p class="tag">Quick check</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two estimates you already have. If the difference is large, it’s worth a conversation with a {K}. If it’s small, a documented supplement request may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}award-net-payout-estimator/">award &amp; net payout estimator</a> also subtracts the deductible, checks already paid and appraisal fees.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec sec-parch"><div class="wrap">
<div class="sec-h rv"><p class="tag">Toolkit</p><h2>Seven free tools from a {K}</h2><p>Check the math before you pick up the phone. Every tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="tgrid">{tools}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="tag">Communities</p><h2>Where a {K} works most often</h2><p>We cover the whole state. These twelve communities each have a page on local storms, housing and neighborhoods.</p></div>
<div class="towns">{towns}</div>
<p class="center"><a class="btn btn-line" href="{LOC_BASE}">All Missouri communities {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-parch"><div class="wrap qsplit">
<div class="rv"><p class="tag">Questions</p><h2>Before you call a {K}</h2><p>Short answers to what people ask first. There are more in <a href="{FAQ_P}">questions answered</a>.</p>{call_box()}</div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="tag">Field notes</p><h2>Plain-English guides for Missouri owners</h2></div>
<div class="ngrid">{notes}</div>
<p class="center"><a class="btn btn-line" href="{POST_BASE}">All field notes {ic("arrow")}</a></p>
</div></section>
{finale(f"Talk to a {K} today", "Send the estimate and a few photos. If appraisal isn’t the right move, we’ll say so.")}"""
    write("/", document("/", f"{K} | Hail, Tornado & Storm Claims",
                        "Independent Missouri insurance appraiser for underpaid hail, tornado, ice and sinkhole claims: estimate review, appraisal and umpire work statewide.",
                        body, [faq_schema(home_faqs)], photo="storm-before-hail"), 1.0)


# ---------------------------------------------------------------- services
def body_grid(article, aside):
    return f'<div class="wrap body-grid"><article class="copy">{article}</article><aside class="side"><div class="side-in">{aside}</div></aside></div>'


def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Appraisal help", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        article = s["body"] + f'<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}<h2>Related appraisal help</h2>' + nextlinks([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = banner(trail, "Appraisal help", s["h1"], s["lede"], ph, s["facts"]) + body_grid(article, call_box() + list_box("All appraisal help", items, path) + list_box("Communities", locs + [("All of Missouri", LOC_BASE)])) + finale()
        svc = {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "State", "name": "Missouri"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, s["title"], s["desc"], body, [crumbs_schema(trail), svc, faq_schema(s["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Appraisal help", SVC_BASE)]
    cards = "".join(svc_card(s, i + 1, "h2") for i, s in enumerate(SERVICES)) + svc_cta()
    idx_faqs = [("Can I hire you for just one stage?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal."),
                ("Do you work on commercial buildings?", "Yes: houses, condos, apartment complexes, HOA communities, offices, retail, warehouses and churches."),
                ("Do you handle more than hail?", "Yes. Tornado and straight-line wind, ice and freeze, water, fire and smoke, and sinkhole or collapse claims are all part of our work.")]
    body = banner(trail, "What we do", "Insurance Appraisal Help Across Missouri",
                  "Eleven services built around one job: a defensible valuation of your loss. Start with an estimate review, or bring us in once appraisal has been demanded.", "meeting-c") + f"""
<section class="sec"><div class="wrap"><div class="sgrid">{cards}</div></div></section>
<section class="sec sec-parch"><div class="wrap qsplit"><div class="rv"><p class="tag">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the insurer’s estimate falls short and what that’s worth. A review answers that quickly, and some disputes close right there with a documented supplement.</p><a class="btn btn-dark" href="{SVC_BASE}insurer-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block(idx_faqs)}</div></div></section>
{finale()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Help in Missouri | 11 Services",
                             "Missouri insurance appraisal help: appraisal clause representation, estimate review, hail, tornado, ice, water, fire, sinkhole and umpire work.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items), faq_schema(idx_faqs)], photo="meeting-c"), 0.9)


# ---------------------------------------------------------------- communities
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Communities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = "".join(f"<li>{e(h)}</li>" for h in l["hoods"])
        storms = "".join(f'<li><span class="yr">{e(y)}</span><span><b>{e(n)}</b> {e(t)}</span></li>' for y, n, t in l["storms"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
        near = nextlinks([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        article = f"""<div class="glance"><h2 class="glance-t">{e(l["city"])} at a glance</h2><div class="glance-g"><div><h3>Common perils</h3><ul class="chips">{chips}</ul></div><div><h3>Housing mix</h3><p>{e(l["housing"])}</p></div><div class="glance-w"><h3>Neighborhoods &amp; nearby areas</h3><ul class="hoods">{hoods}</ul></div></div></div>
{l["body"]}
<h2>Storm history around {e(l["city"])}</h2><ul class="minilog">{storms}</ul>
<h2>Appraisal help available in {e(l["city"])}</h2><p>Every {BRAND} service is available to property owners in {e(l["city"])}{"" if l["county"] == "Independent city" else " and across " + e(l["county"])}:</p><ul class="cols">{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2>{near}"""
        aside = call_box() + list_box("Communities", items, path) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = banner(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {name}", e(l["lede"]), ph,
                      [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + body_grid(article, aside) + finale(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        place = {"@type": "City", "name": l["geo"]}
        place["containedInPlace"] = {"@type": "State", "name": "Missouri"} if l["county"] == "Independent city" else {"@type": "AdministrativeArea", "name": l["county"] + ", Missouri"}
        svc = {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": place, "url": DOMAIN + path}
        write(path, document(path, l["title"], l["desc"], body, [crumbs_schema(trail), svc, faq_schema(l["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Communities", LOC_BASE)]
    cards = "".join(town_card(l, "h2") for l in LOCATIONS)
    mosaic = "".join(f'<article class="tile rv">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 400px", alt="")}<div class="tile-b"><small>{c}</small><h3>{n}</h3><p>{t}</p></div></article>' for n, c, t, ph in REGIONS)
    body = banner(trail, "Statewide coverage", "Insurance Appraisal in Every Missouri County",
                  "We work in all 114 counties and the City of St. Louis. These community pages cover the places we’re called most often, with local storms, housing and neighborhoods.", "kc-union-station") + f"""
<section class="sec"><div class="wrap"><div class="towns">{cards}</div></div></section>
<section class="sec sec-parch"><div class="wrap"><div class="sec-h sec-h-l rv"><p class="tag">Regions</p><h2>How claims differ across Missouri</h2><p>The same policy language plays out differently on a St. Louis brick flat, a Joplin rebuild and an Ozarks home on karst ground.</p></div><div class="mosaic">{mosaic}</div></div></section>
{finale("Don’t see your town?", "We cover every county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Missouri Communities We Serve | Insurance Appraisal",
                             "Insurance appraisal in every Missouri county, including Kansas City, St. Louis, Springfield, Columbia, Joplin, Jefferson City and Cape Girardeau.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="kc-union-station"), 0.9)


# ---------------------------------------------------------------- toolkit
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Toolkit", TOOL_BASE), (t["name"], path)]
        ph = TOOL_PHOTO[t["slug"]]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        article = t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>' + nextlinks([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = banner(trail, f"Free {t['kind'].lower()} · nothing stored", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><h2 class="sr-only">{e(t["name"])}</h2><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and example figures are illustrative.</p>
<noscript><p class="hint center">This tool needs JavaScript to calculate. Everything else on the page works without it.</p></noscript></div></section>""" + body_grid(article, call_box() + list_box("Toolkit", items, path)) + finale("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")
        app = {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
               "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}
        write(path, document(path, t["title"], t["desc"], body, [crumbs_schema(trail), app, faq_schema(t["faqs"])], photo=ph), 0.8)

    trail = [("Home", "/"), ("Toolkit", TOOL_BASE)]
    cards = "".join(tool_card(t, "h2") for t in TOOLS) + tool_cta()
    body = banner(trail, "Free & private", "Free Claim Tools for Missouri Property Owners",
                  "Seven estimators, calculators and planners drawn from appraisal work. Use them to understand your claim, check the insurer’s math and plan your next step. No sign-up, nothing stored.", "calculator-blue", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid">{cards}</div></div></section>
<section class="sec sec-parch"><div class="wrap qsplit"><div class="rv"><p class="tag">Suggested order</p><h2>Using the tools together</h2><ol class="steps-l"><li>Start with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a> so no date slips.</li><li>Check roof figures with the <a href="{TOOL_BASE}roof-measurement-calculator/">roof measurement calculator</a> and the <a href="{TOOL_BASE}roof-repair-or-replace-splitter/">repair-or-replace splitter</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}hail-deductible-calculator/">wind &amp; hail deductible</a> and <a href="{TOOL_BASE}depreciation-recovery-calculator/">depreciation &amp; recovery</a> calculators.</li><li>Test the dispute in the <a href="{TOOL_BASE}award-net-payout-estimator/">award &amp; net payout estimator</a>, then score your file with the <a href="{TOOL_BASE}appraisal-readiness-score/">readiness score</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Tools | Missouri Toolkit",
                              "Seven free claim tools: award and net payout, depreciation recovery, roof squares, wind and hail deductible, claim calendar and repair-or-replace.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="calculator-blue"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Appraisal roadmap", PROCESS), ("Questions answered", FAQ_P), ("Appraisal dictionary", GLOSS), ("Field notes", POST_BASE)]

    path, trail = PROCESS, [("Home", "/"), ("Appraisal roadmap", PROCESS)]
    toc = "".join(f'<li><a href="#stage-{i + 1}">{e(n)}</a></li>' for i, (n, _) in enumerate(PROCESS_STEPS))
    stages = "".join(f'<section class="stage" id="stage-{i + 1}"><h2><span>Stage {i + 1}</span>{e(n)}</h2>{h}</section>' for i, (n, h) in enumerate(PROCESS_STEPS))
    article = f'{PROCESS_INTRO}<nav class="toc" aria-label="Stages"><p class="toc-t">The {len(PROCESS_STEPS)} stages</p><ol>{toc}</ol></nav>{stages}{PROCESS_OUTRO}'
    body = banner(trail, "Process guide", "The Missouri Appraisal Roadmap, Stage by Stage",
                  f"{len(PROCESS_STEPS)} stages from the first disagreement to payment: what happens, who does what, and where claims most often go wrong.", "work-papers",
                  [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "Any 2 of 3 signatures")]) + body_grid(article, call_box() + list_box("Learn", learn_items, path)) + finale()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Missouri", "description": "The stages of a property insurance appraisal from dispute to award and payment.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#stage-{i + 1}"} for i, (n, _) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Missouri Insurance Appraisal Process | 8-Stage Roadmap",
                         "How property insurance appraisal works in Missouri: the written demand, naming appraisers, choosing an umpire, the award and getting paid.",
                         body, [crumbs_schema(trail), howto], photo="work-papers"), 0.8)

    path, trail = FAQ_P, [("Home", "/"), ("Questions answered", FAQ_P)]
    jump = "".join(f'<li><a href="#topic-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="topic-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = banner(trail, "Answers by topic", "Missouri Insurance Appraisal Questions, Answered",
                  f"{len(allq)} plain answers grouped by topic: the basics, costs and timing, Missouri rules and agencies, storm claims and what happens after the award.", "meeting-a") + body_grid(
        f'<nav class="toc" aria-label="Topics"><p class="toc-t">Jump to a topic</p><ul>{jump}</ul></nav>{groups}', call_box() + list_box("Learn", learn_items, path)) + finale("Didn’t see your question?", "Call or email and we’ll talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ | Missouri Costs, Timing & Rules",
                         "Answers to Missouri insurance appraisal questions by topic: basics, costs and timing, state rules and agencies, storm claims and after the award.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="meeting-a"), 0.8)

    path, trail = GLOSS, [("Home", "/"), ("Appraisal dictionary", GLOSS)]
    gl = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in gl})
    az = "".join(f'<a href="#t-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in gl:
        c = term[0].upper()
        anchor = f' id="t-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    article = f'<div class="gsearch"><label for="gloss-q">Search {len(gl)} terms</label><input id="gloss-q" type="search" placeholder="Try “holdback”, “umpire” or “karst”" autocomplete="off"><p class="hint" data-gcount aria-live="polite"></p></div><nav class="az" aria-label="Letters">{az}</nav><dl class="gloss">{dl}</dl>'
    body = banner(trail, "Reference", "The Appraisal Dictionary: Claim Terms in Plain English",
                  f"{len(gl)} words you’ll meet in policies, estimates and appraisal awards, from actual cash value to umpire. Type in the box to filter.", "calculator-paper", cta=False) + body_grid(article, call_box() + list_box("Learn", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim and appraisal terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in gl]}
    write(path, document(path, "Insurance Claim Glossary | Appraisal Terms Defined",
                         "Searchable glossary of property insurance and appraisal terms: actual cash value, holdback, umpire, percentage deductible, karst, FAIR Plan and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-paper"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Field notes", POST_BASE), (p["title"], path)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        others = [o for o in POSTS if o is not p][:3]
        article = f'<p class="byline">By the {BRAND} team · Published {nice} · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2>' + nextlinks([("Field note", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = banner(trail, f"Field note · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + body_grid(article, call_box() + list_box("Learn", learn_items) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + finale()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path, trail = POST_BASE, [("Home", "/"), ("Field notes", POST_BASE)]
    cards = "".join(note_card(p, "h2") for p in POSTS)
    body = banner(trail, "Field notes", "Field Notes: Appraisal Guides for Missouri Owners",
                  "Practical, Missouri-specific guides on policy language, storm documentation and appraisal strategy.", "hailstones-hand", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ngrid">{cards}</div></div></section>{finale()}"""
    write(path, document(path, "Field Notes | Missouri Insurance Appraisal Guides",
                         "Guides for Missouri property owners on the appraisal clause, hail roofs, vexatious refusal, tornado rebuilds, sinkholes and FAIR Plan claims.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="hailstones-hand"), 0.7)


# ---------------------------------------------------------------- firm & legal
def company_pages():
    path, trail = ABOUT, [("Home", "/"), ("Our firm", ABOUT)]
    article = f"""<figure class="lead-img">{img("meeting-c", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, asked carefully</h2>
<p>A property claim raises plenty of questions: what happened, what the policy covers, who pays. {BRAND} works on just one of them, the amount of loss. What does it honestly cost to put this building back the way it was? Depending on the claim, we act as your appointed appraiser, review an insurer’s estimate before a dispute hardens, or serve as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Inspect first, compare later.</strong> We measure and document the damage before we read anyone else’s numbers.</li>
<li><strong>Defensible beats impressive.</strong> An inflated estimate falls apart in front of an umpire. We price what we can support line by line.</li>
<li><strong>Reports you can follow.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Straight answers on fit.</strong> If your claim needs a Missouri attorney, a public adjuster or just a supplement request, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost and how it’s calculated before work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, landlords, condo and HOA boards, property managers, churches, business owners, contractors and attorneys across Missouri. On any one claim we serve in a single role, and we disclose prior dealings with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Missouri produces nearly every kind of property loss in one state: spring hail in the Kansas City and St. Louis suburbs, tornadoes from Joplin to St. Charles County, ice storms across the Ozarks, sinkholes on karst ground, river flooding along the Missouri and Mississippi, and the background question of the New Madrid seismic zone. Working all 114 counties and the City of St. Louis keeps us current on all of them. For questions about the state’s insurance rules, the Missouri Department of Commerce and Insurance publishes consumer guidance and accepts complaints.</p>"""
    body = banner(trail, "Our firm", f"About {BRAND}",
                  "We’re estimators and appraisers who think a covered claim should be paid on what the damage really costs, documented clearly enough that everyone at the table can see it.", "meeting-c") + body_grid(
        article, call_box() + list_box("Explore", [("Appraisal help", SVC_BASE), ("Communities", LOC_BASE), ("Free toolkit", TOOL_BASE), ("Appraisal roadmap", PROCESS)])) + finale()
    write(path, document(path, f"About Our Firm | {BRAND}",
                         "Missouri Insurance Appraiser is an independent appraisal and estimating firm focused on the amount of loss in disputed Missouri property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="meeting-c"), 0.7)

    path, trail = CONTACT, [("Home", "/"), ("Get in touch", CONTACT)]
    body = banner(trail, "Get in touch", f"Contact {BRAND}",
                  "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "work-papers", cta=False) + f"""
<section class="sec sec-dark"><div class="wrap contact">
<div class="rv"><p class="tag tag-l">Direct lines</p><h2>Reach us directly</h2>
<ul class="reach"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>{HOURS}</span></li><li>{ic("pin")}<span><small>Service area</small>All 114 counties and the City of St. Louis</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks-l"><li>{ic("check")}Your declarations page</li><li>{ic("check")}The insurer’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the insurer</li><li>{ic("check")}Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact Us | {BRAND}",
                         "Get a free review of a disputed Missouri property claim. Call or text (844) 537-1427, email us, or send your claim details through the form.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="work-papers"), 0.8)

    lic = {"cc0": "CC0 1.0 (public domain dedication)", "pdm": "Public Domain Mark"}
    credits = "".join(
        f'<tr><td>{img(k, "thumb", sizes="120px", alt="")}</td><td><b>{e(v["title"] or "Untitled")}</b><br><small>{e(v.get("creator") or "Unknown creator")} · via {e(v["source"].title())}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Notice", "privacy notice", f"""<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web host records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with the providers that host our site and email, or when the law requires it.</p>
<h2>Tools</h2><p>Our calculators, planners and checklists run in your browser. The figures you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics through Google Tag Manager, this notice will be updated to say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To see, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Terms of Service", "terms of service", f"""<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. The content is general information about insurance appraisal and property claims in Missouri.</p>
<h2>No professional relationship</h2><p>Reading the site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Consult a licensed Missouri attorney about legal questions.</p>
<h2>Tools and examples</h2><p>The tools give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome, and example figures throughout the site are illustrative.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Missouri.</p>""", "The terms that apply when you use this website and its free tools."),
        DISCLAIM: ("Disclaimer", "site disclaimer", f"""<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not a law firm, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Statutes, agencies and events</h2><p>References to Missouri statutes (including the vexatious refusal provisions), the Department of Commerce and Insurance, the Missouri FAIR Plan, geology or past storms are for context only and are described in general terms. Verify current law and facts with official sources and a Missouri attorney.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, naming an appraiser, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is approaching, consult an attorney promptly.</p>
<h2>Photographs</h2><p>Photos on this site are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website."),
        CREDITS: ("Photo Credits", "photo credits", f"""<p>Every photograph on this site is either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or marked as a <strong>public-domain</strong> work, including photos by U.S. government agencies. We found them through the Openverse search engine. Attribution isn’t legally required, but we credit the creators here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for every photograph used on this site."),
    }
    for path, (title, kw, content, lede) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = banner(trail, "Site information", title, lede, "brick-warehouse", cta=False) + body_grid(content, call_box())
        desc = f"The {kw} for {BRAND} ({HOST}): {lede[0].lower() + lede[1:]}"
        if len(desc) > 150:
            desc = f"The {kw} for {BRAND}: {lede[0].lower() + lede[1:]}"
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="brick-warehouse"), 0.3)


def sitemap_pages():
    path, trail = HTMLMAP, [("Home", "/"), ("Site index", HTMLMAP)]
    groups = [
        ("Main", [("Home", "/"), ("Our firm", ABOUT), ("Get in touch", CONTACT)]),
        ("Appraisal help", [("Every service", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Communities", [("All of Missouri", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Toolkit", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", [("Appraisal roadmap", PROCESS), ("Questions answered", FAQ_P), ("Appraisal dictionary", GLOSS), ("Field notes", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy notice", PRIVACY), ("Terms of service", TERMS), ("Disclaimer", DISCLAIM), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="mapcol rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = banner(trail, "Navigation", "Site Index", f"Every page on the {BRAND} website, grouped by section.", "brick-warehouse", cta=False) + f'<section class="sec"><div class="wrap mapgrid">{cols}</div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"An HTML site index listing every page on {BRAND}: appraisal help, communities, free tools, field notes and legal pages.", body, [crumbs_schema(trail)], photo="brick-warehouse"), 0.3)

    body = f"""<section class="banner banner-404"><div class="banner-ph">{img("ice-storm-path", lazy=False, alt="")}</div><div class="wrap banner-in"><p class="tag tag-l">Error 404</p><h1>This page didn’t make it through the storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btns"><a class="btn btn-teal" href="/">Home</a><a class="btn btn-ghost" href="{SVC_BASE}">Appraisal help</a><a class="btn btn-ghost" href="{TOOL_BASE}">Toolkit</a><a class="btn btn-ghost" href="{CONTACT}">Get in touch</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, noindex=True, photo="ice-storm-path"), sitemap=False)


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
// Missouri Insurance Appraiser - front controller for the static build.
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
