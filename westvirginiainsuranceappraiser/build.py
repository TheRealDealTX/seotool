#!/usr/bin/env python3
"""Static site generator for westvirginiainsuranceappraiser.com.

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
from locations import LOCATIONS, REGIONS as REGION_COPY  # noqa: E402
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "West Virginia Insurance Appraiser"
HOST = "westvirginiainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261111a"
FAV = "1"
OG_ALT = "West Virginia Insurance Appraiser — independent property claim appraisal across all 55 counties"

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = "GTM-TFJFX2FN"
# Head snippet exactly as supplied by the owner (optional). If empty, the standard GTM loader for GTM_ID is used.
GTM_HEAD_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-TFJFX2FN"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

SVC_BASE = "/wv-appraisal-services/"
LOC_BASE = "/west-virginia-service-areas/"
TOOL_BASE = "/free-appraisal-tools/"
POST_BASE = "/claim-library/"
P_PROCESS = "/appraisal-step-by-step/"
P_FAQ = "/faq-by-topic/"
P_GLOSS = "/appraisal-glossary/"
P_ABOUT = "/about-the-firm/"
P_CONTACT = "/request-a-review/"
P_PRIV = "/privacy-statement/"
P_TERMS = "/terms-and-conditions/"
P_DISC = "/legal-notice/"
P_CREDITS = "/photo-credits/"
P_MAP = "/html-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-wv/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "hero-gorge-bridge": "New River Gorge Bridge spanning a forested gorge in West Virginia",
    "gorge-overlook": "The New River winding through a deep green gorge seen from an overlook",
    "blue-ridges": "Layers of blue Appalachian ridges above a green valley",
    "capitol-charleston": "West Virginia State Capitol dome and fountain in Charleston",
    "parkersburg-view": "Downtown Parkersburg and the Ohio River at sunset from Quincy Hill",
    "wheeling-theatre": "Ornate white facade of the Capitol Theatre in downtown Wheeling",
    "lewisburg-hall": "Carnegie Hall, a red-brick building with white columns in Lewisburg",
    "morgantown-hillside": "Historic photo of wood-frame houses on a Morgantown hillside",
    "gorge-bridge-green": "Steel arch of the New River Gorge Bridge over a forested canyon",
    "tree-on-house": "Brick house with a garage after storm damage, branches in the yard",
    "storm-flood-house": "Two-story house knocked off its foundation after floodwater and storm damage",
    "roof-peeled": "Metal roof peeled back and draped over the side of a brick building after high winds",
    "tornado-street": "Damaged homes and debris across a neighborhood after a tornado",
    "fallen-trees-yard": "Large trees blown down around a one-story house after a windstorm",
    "ice-storm-road": "Ice-coated branches fallen across a road in a freezing fog",
    "snow-cabin": "Wood-sided mountain house buried in heavy snow",
    "burned-building": "Charred interior of a building after a fire, with a fire hose in front",
    "roof-eave-damage": "Close-up of damaged asphalt shingles curling at a roof eave",
    "metal-roof-barn": "Red barn with a new standing-seam metal roof",
    "metal-roof-panels": "Corrugated metal roof panels with a snow guard",
    "roof-repair-brick": "Historic red-brick building with roof repairs in progress",
    "brick-apartments": "Four-story brick apartment building on a street corner in winter",
    "stone-office": "Stone federal office building at a downtown intersection",
    "flooded-yard": "Floodwater covering a residential street up to a stop sign",
    "wall-crack": "Long crack running across a concrete basement wall",
    "landslide-slope": "Aerial view of a hillside landslide scar through a forest",
    "consult-window": "Two women talking through documents at a table by a window",
    "meeting-laptop": "Three people discussing a project around a laptop",
    "handshake": "Two people shaking hands across a table after a meeting",
    "calculator-paper": "Scientific calculator resting on printed estimate pages",
    "calculator-notes": "Calculator, pencil and sticky note on a desk",
    "paperwork": "Hands holding a pen over paperwork on a desk",
    "classic-kitchen": "Cream-colored kitchen with an island, granite counters and pendant lights",
    "tool-belt": "Contractor wearing a tool belt beside new siding",
    "older-home": "Two-story wood-frame house with a front porch and dormer",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "invoking-appraisal-representation": "consult-window", "homeowners-claim-appraiser": "older-home",
    "commercial-hoa-claim-appraiser": "brick-apartments", "roof-hail-claim-appraiser": "roof-eave-damage",
    "derecho-wind-tornado-appraiser": "fallen-trees-yard", "tropical-remnant-storm-appraiser": "storm-flood-house",
    "water-damage-claim-appraiser": "classic-kitchen", "fire-smoke-claim-appraiser": "burned-building",
    "mine-subsidence-claim-appraiser": "wall-crack", "ice-snow-freeze-claim-appraiser": "ice-storm-road",
    "claim-estimate-review": "calculator-paper", "appraisal-umpire-services": "handshake",
}
LOC_PHOTO = {
    "charleston": "capitol-charleston", "huntington": "ice-storm-road", "morgantown": "morgantown-hillside",
    "parkersburg": "parkersburg-view", "wheeling": "wheeling-theatre", "martinsburg": "fallen-trees-yard",
    "fairmont": "stone-office", "beckley": "gorge-bridge-green", "clarksburg": "tornado-street",
    "lewisburg": "lewisburg-hall", "bluefield": "blue-ridges", "elkins": "snow-cabin",
}
REGION_PHOTO = {
    "northern-panhandle": "wheeling-theatre", "eastern-panhandle": "tree-on-house", "north-central": "morgantown-hillside",
    "mid-ohio-valley": "parkersburg-view", "metro-valley": "capitol-charleston", "southern-coalfields": "gorge-overlook",
    "highlands": "blue-ridges",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-notes", "rcv-acv-holdback-calculator": "paperwork",
    "roof-square-pitch-estimator": "metal-roof-panels", "percentage-deductible-checker": "roof-peeled",
    "claim-timeline-ics-planner": "meeting-laptop", "appraisal-readiness-scorecard": "roof-repair-brick",
    "mine-subsidence-limit-calculator": "wall-crack",
}
POST_PHOTO = {
    "wv-appraisal-clause-guide": "paperwork", "landslide-vs-mine-subsidence-claims": "landslide-slope",
    "documenting-storm-damage-wv": "tree-on-house", "appraisal-or-attorney-wv": "meeting-laptop",
    "depreciation-holdback-wv": "calculator-paper", "overhead-profit-and-pricing-wv": "tool-belt",
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
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
}


def ic(name, cls="", size=20):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


def mark(uid="m", size=44):
    """Brand mark: a ridgeline over a level line (the 'measured' line of an appraisal) on a forest-green tile."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#235c16"/><stop offset="1" stop-color="#0b1f07"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="10" fill="url(#{uid})"/>'
            '<path d="M7 31l9.5-11 6 6.5L29 17l12 14" fill="none" stroke="#f4f1e8" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M11 37.5h26" stroke="#e0679a" stroke-width="3.4" stroke-linecap="round"/><circle cx="35.5" cy="12.5" r="3.2" fill="#e0679a"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "WV", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-WV", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 55 West Virginia counties.",
        "areaServed": [{"@type": "State", "name": "West Virginia"}] + [{"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "West Virginia"}} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Mine subsidence claims", "Wind and derecho damage"],
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


# ---------------------------------------------------------------- GTM
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


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal step by step", P_PROCESS), ("FAQ by topic", P_FAQ), ("Appraisal glossary", P_GLOSS), ("Claim library", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All 12 services", SVC_BASE), "cols"),
        ("Service areas", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All 55 counties", LOC_BASE), "cols"),
        ("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), ""),
        ("Resources", LEARN, None, ""),
    ]


def header():
    menu = ""
    for i, (name, links, allk, cols) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", size=16)}</a></li>'
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev", 16)}</button><ul class="drop {cols}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top" href="{P_ABOUT}">About</a></li><li><a class="top" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="b" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev", 18)}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="lnk" href="{P_ABOUT}">About the firm</a></li><li><a class="lnk" href="{P_CONTACT}">Request a review</a></li>'

    brand = lambda uid: f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span class="bt"><b>West Virginia</b><small>Insurance Appraiser</small></span></a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone", size=18)}<span><small>Free file review</small>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu", size=24)}</button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("md")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x", size=22)}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="lnk" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · all 55 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}, WV</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="ridge" aria-hidden="true"><svg viewBox="0 0 1440 90" preserveAspectRatio="none" width="1440" height="90"><path d="M0 90V58l120-30 110 26 140-44 120 38 100-22 150 40 130-52 120 30 140-20 110 34 100-24 100 22v34z" fill="currentColor"/></svg></div>
<div class="foot-body"><div class="wrap">
<div class="foot-cta"><div><h2>Before you accept the final number, compare the line items.</h2><p>Send the carrier’s estimate. We’ll tell you plainly whether appraisal is worth it.</p></div><div class="btn-row"><a class="btn pink" href="tel:{TEL}">{ic("phone", size=18)} {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Request a review</a></div></div>
<div class="foot-grid">
<div class="foot-brand"><a class="brand" href="/" aria-label="{BRAND} home">{mark("mf")}<span class="bt"><b>West Virginia</b><small>Insurance Appraiser</small></span></a>
<p>Independent appraisal, estimate review and umpire work for disputed property claims — Northern Panhandle to the coalfields.</p>
<p class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET</span></p></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Service areas</h3><ul class="two">{loc}</ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Firm &amp; resources</h3><ul><li><a href="{P_ABOUT}">About the firm</a></li><li><a href="{P_PROCESS}">Appraisal step by step</a></li><li><a href="{P_FAQ}">FAQ by topic</a></li><li><a href="{P_GLOSS}">Appraisal glossary</a></li><li><a href="{POST_BASE}">Claim library</a></li><li><a href="{P_CONTACT}">Request a review</a></li></ul></div>
</div>
<div class="foot-legal"><span>© {date.today().year} {BRAND}</span>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Legal notice</a></li><li><a href="{P_CREDITS}">Photo credits</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we do not give legal advice, and we do not act as a public adjuster. Content on this site is general information; your policy controls. Example figures are illustrative, and no outcome is guaranteed.</p>
</div></div></footer>
<a class="to-top" href="#main" aria-label="Back to top">{ic("up", size=20)}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone", size=18)} Call</a><a href="{P_CONTACT}">Free review</a></div>"""


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, page_type="WebPage", main_business=False):
    canonical = DOMAIN + path
    extra_nodes, crumb_id = [], None
    for n in (schema or []):
        t = n.get("@type")
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
        extra_nodes.append(n)
    img_key = preload or "hero-gorge-bridge"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = sorted([n for n in extra_nodes if n.get("@type") in MAIN_TYPES], key=lambda n: MAIN_TYPES.index(n["@type"]))
    webpage["mainEntity"] = {"@id": DOMAIN + "/#business"} if (main_business or not mains) else {"@id": mains[0]["@id"]}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<script>(function(l,h){{if((l.hostname==="www."+h)||(l.hostname===h&&l.protocol==="http:")){{l.replace("https://"+h+l.pathname+l.search+l.hash);}}}})(location,"{HOST}");</script>
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className="js";</script>
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
<meta property="og:image:alt" content="{e(OG_ALT)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{e(OG_ALT)}">
<meta name="geo.region" content="US-WV">
<meta name="geo.placename" content="West Virginia">
<meta name="theme-color" content="#15370d">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@500;600;700&amp;family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;display=swap">
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">›</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn pink" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Free file review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev", 18)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box callbox"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We’ll say so if appraisal isn’t the right tool.</p><a class="big" href="tel:{TEL}">{PHONE}</a><a class="btn pink full" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right", size=16)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def band(h="Not sure the carrier’s number is right?", p="Email the estimate and a few photos. We’ll review them and tell you what we see."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn pink" href="tel:{TEL}">{ic("phone", size=18)} {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Send the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small>{e(n)}{ic("arrow", size=18)}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Wind / derecho / tornado", "Hail / roof", "Water / burst pipe", "Ice / snow load", "Fire / smoke", "Fallen tree", "Mine subsidence", "Remnant tropical storm", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=3):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Landlord", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in West Virginia"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Nearest city</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the insurer paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy statement</a>.</span></label></div>
<div class="full"><button class="btn full" type="submit">Send claim details {ic("arrow", size=18)}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hform" action="/api/contact.php" method="post" data-lead novalidate>
<div class="hform-top"><h2>Free file review</h2><p>Two minutes. A call back within one business day.</p></div>
<div class="hform-body">
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What kind of loss?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>Yes, contact me about my claim. <a href="{P_PRIV}">Privacy</a></span></label>
<button class="btn pink full" type="submit">Request my review {ic("arrow", size=18)}</button>
<div class="form-msg" role="status"></div>
</div></form>"""


def svc_card(s, hl=3, big=False):
    return (f'<a class="card rv{" big" if big else ""}" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
            f'<span class="card-b"><h{hl}>{e(s["name"])}</h{hl}><span class="card-p">{e(s["short"])}</span><span class="more">View service {ic("arrow", size=16)}</span></span></a>')


def tool_card(t, hl=3):
    return (f'<a class="card tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="badge">{e(t["kind"])}</span></span>'
            f'<span class="card-b"><h{hl}>{e(t["name"])}</h{hl}><span class="card-p">{e(t["short"])}</span><span class="more">Open the tool {ic("arrow", size=16)}</span></span></a>')


def loc_card(l, hl=3):
    return (f'<a class="card loc-card rv" href="{loc_path(l)}"><span class="card-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}</span>'
            f'<span class="card-b"><h{hl}>{e(l["city"])}</h{hl}><span class="card-p">{e(l["county"])} · {e(l["region"])}</span></span></a>')


def post_card(p, hl=3):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<a class="card post-card rv" href="{POST_BASE}{p["slug"]}/"><span class="card-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span>'
            f'<span class="card-b"><span class="meta">{nice} · {e(p["read"])} read</span><h{hl}>{e(p["title"])}</h{hl}><span class="card-p">{e(p["summary"])}</span><span class="more">Read the guide {ic("arrow", size=16)}</span></span></a>')


# ---------------------------------------------------------------- home
STORMS = [
    ("1937", "Ohio River flood", "Record January crests swamped river towns from Wheeling to Huntington and led to the floodwalls many cities still rely on.", "flooded-yard"),
    ("1944", "Shinnston tornado", "On June 23 a tornado tore through Shinnston in Harrison County — still the deadliest tornado in state history.", "tornado-street"),
    ("1985", "Election Day flood", "Early November rains sent the Cheat and South Branch rivers through Parsons, Rowlesburg and the Potomac Highlands.", "storm-flood-house"),
    ("2004", "Ivan’s remnants", "In September the leftovers of Hurricane Ivan pushed the Ohio River into Wheeling and other Northern Panhandle towns.", "gorge-overlook"),
    ("2012", "The June derecho", "A fast line of storms crossed the state on June 29, toppling trees and leaving much of West Virginia without power for days.", "fallen-trees-yard"),
    ("2012", "Sandy’s mountain snow", "In late October Superstorm Sandy buried Tucker, Randolph and nearby counties in heavy wet snow; roofs and porches gave way.", "snow-cabin"),
    ("2016", "The June 23 flood", "Torrential rain struck Greenbrier, Kanawha and Nicholas counties, devastating White Sulphur Springs, Rainelle, Richwood and Clendenin.", "tree-on-house"),
    ("2021", "Huntington-area ice storm", "In February a thick glaze brought down trees and lines across Cabell, Wayne, Lincoln and Putnam counties.", "ice-storm-road"),
]


def home():
    K = BRAND
    checkpoints = [
        ("File review", f"We read the policy, both estimates and your photos and tell you whether a {K} can move the number."),
        ("Independent scope", "Our own inspection, measurements and a line-item estimate priced for your part of the state."),
        ("Written demand", "Appraisal is invoked in writing and your appraiser is named inside the policy’s window."),
        ("Panel work", "Line-by-line negotiation with the insurer’s appraiser narrows the disagreement."),
        ("Signed award", "Anything still open goes to a neutral umpire; two signatures set the amount of loss."),
    ]
    tl = "".join(f'<li class="tl-step"><span class="tl-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(checkpoints))

    storms = "".join(f'<li class="storm">{img(ph, sizes="320px", alt="")}<div><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for y, t, d, ph in STORMS)
    regions = "".join(
        f'<article class="region rv"><div class="region-ph">{img(REGION_PHOTO[k], sizes="(max-width:700px) 100vw, 33vw", alt="")}</div><div class="region-b"><p class="towns">{e(towns)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(txt)}</p></div></article>'
        for k, n, towns, perils, txt, _c in REGION_COPY)

    svc = "".join(svc_card(s, big=(i == 0)) for i, s in enumerate(SERVICES))
    tools = "".join(tool_card(t) for t in TOOLS)
    cities = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><span>{e(l["county"])}</span>{ic("arrow", size=16)}</a></li>' for l in LOCATIONS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do that my adjuster doesn’t?", f"Your adjuster works for the insurer and writes the company’s estimate. A {K} is appointed by you under the policy’s appraisal clause to build an independent valuation, work through the differences with the insurer’s appraiser and, if needed, present the open items to an umpire."),
        ("Is appraisal the same as suing the insurance company?", "No. Appraisal is a process written into most property policies to settle disagreements over the amount of loss. It does not decide coverage or bad-faith questions, which are matters for a West Virginia attorney."),
        (f"When is it worth calling a {K}?", "When the insurer has accepted coverage, you have its itemized estimate, and the difference from your contractor’s estimate is meaningful — often more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That is why the scope should be complete before appraisal is demanded."),
        ("How are appraisal fees handled?", "Each side usually pays its own appraiser and half of the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Can appraisal help with mine subsidence or landslide damage?", "If the insurer agrees a subsidence loss is covered but disputes the cost, appraisal can value it within the endorsement’s limit. If the dispute is whether the ground movement is covered at all, that is a coverage question rather than an appraisal question."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-gorge-bridge", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · 55 counties</p>
<h1>{K}</h1>
<p class="lede">Covered, inspected, and still underpaid? As your {K}, we build an independent, line-by-line valuation of the damage and take it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn pink" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn line light" href="#services">See what we handle</a></div>
<ul class="hero-points"><li>{ic("check", size=18)}Appointed by you, not the carrier</li><li>{ic("check", size=18)}Homes, rentals, HOAs &amp; businesses</li><li>{ic("check", size=18)}Statewide on-site inspections</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="numbers" aria-label="At a glance"><div class="wrap numbers-in">
<div class="num rv"><b data-count="55">55</b><span>counties served, statewide</span></div>
<div class="num rv"><b data-count="12">12</b><span>appraisal &amp; estimating services</span></div>
<div class="num rv"><b data-count="7">7</b><span>free in-browser claim tools</span></div>
<div class="num rv"><b>2&nbsp;of&nbsp;3</b><span>signatures make an award binding</span></div>
</div></section>

<section class="sec intro"><div class="wrap split">
<div class="photo-pair rv">
<figure class="pp1">{img("older-home", sizes="(max-width:900px) 80vw, 420px")}</figure>
<figure class="pp2">{img("roof-eave-damage", sizes="(max-width:900px) 60vw, 300px")}</figure>
</div>
<div class="rv">
<p class="kicker">Covered is not the same as paid</p>
<h2>When a covered claim still comes up short</h2>
<p>Most disputed claims in this state aren’t denials. The adjuster agrees the storm, the frozen pipe or the fire happened — then writes an estimate that leaves out a slope of the roof, prices slate as asphalt, skips the second-story labor or forgets the code upgrade. A {K} works in that gap between “covered” and “fully paid.”</p>
<p>We don’t edit the carrier’s estimate. A {K} starts over: our own inspection, our own measurements and pricing for your county, so every number we put in front of a panel can be defended.</p>
<a class="btn" href="{P_ABOUT}">How the firm works {ic("arrow", size=18)}</a>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Twelve services</p><h2>Where a {K} steps in</h2><p>From a single estimate review to full panel representation and neutral umpire work. Each service has its own page with the West Virginia details that matter.</p></div>
<div class="grid svc-grid" data-stagger>{svc}</div>
</div></section>

<section class="sec storms-sec"><div class="wrap">
<div class="sec-head row rv"><div><p class="kicker light">Storm history</p><h2>Floods, derechos and ice: the claims this state remembers</h2><p>Every big event changes how the next claim is written. A {K} prices damage knowing what the last storm did to the same roofs, hollows and river towns.</p></div>
<div class="car-btns"><button type="button" class="car-btn" data-car="-1" aria-label="Previous storm">{ic("left", size=20)}</button><button type="button" class="car-btn" data-car="1" aria-label="Next storm">{ic("right", size=20)}</button></div></div>
<ol class="storms" data-carousel tabindex="0" aria-label="West Virginia storm timeline">{storms}</ol>
<p class="fine">Photos are illustrative and do not show the events described.</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">How it moves</p><h2>Five checkpoints between a low estimate and a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process. Here is how a {K} carries a file from the first call to the award.</p></div>
<ol class="timeline-h" data-timeline><span class="tl-fill" aria-hidden="true"></span>{tl}</ol>
<p class="center"><a class="link" href="{P_PROCESS}">Read the full seven-stage guide {ic("arrow", size=16)}</a></p>
</div></section>

<section class="sec moss"><div class="wrap split">
<div class="rv"><p class="kicker light">Try it now</p><h2>Put your two estimates side by side</h2><p>Type in the insurer’s total and your contractor’s total. A large gap is worth a conversation with a {K}; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees and shows cautious, likely and strong outcomes.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Calculators a {K} uses every week</h2><p>Seven tools that run entirely in your browser. Nothing you type is stored or sent anywhere.</p></div>
<div class="grid tool-grid" data-stagger>{tools}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Seven regions</p><h2>From the Northern Panhandle to the coalfields</h2><p>The same policy reads differently on a Wheeling rowhouse, a Martinsburg subdivision and a cabin above Canaan Valley. A {K} has to know how each region’s weather and housing show up in an estimate.</p></div>
<div class="grid region-grid" data-stagger>{regions}</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker">Cities we visit most</p><h2>On-site in all 55 counties</h2><p>We inspect in person statewide. These twelve local pages cover the places a {K} is called most often, with neighborhoods, housing and storm history for each.</p><a class="btn ghost" href="{LOC_BASE}">See every service area {ic("arrow", size=18)}</a></div>
<ul class="city-list rv" data-stagger>{cities}</ul>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Know the limits</p><h2>What appraisal can and can’t decide</h2><p>A good {K} tells you early when a different kind of help fits better.</p></div>
<div class="decide">
<div class="dc yes rv"><h3>{ic("check", size=20)} Appraisal can settle</h3><ul><li>How much a covered loss costs to repair</li><li>Repair-versus-replace and matching disputes</li><li>Missing trades, steep and high charges, code items</li><li>Overhead and profit when the policy allows it</li><li>Replacement cost and actual cash value figures</li></ul></div>
<div class="dc no rv"><h3>{ic("x", size=20)} Appraisal can’t settle</h3><ul><li>Whether a loss is covered or excluded (flood, landslide)</li><li>Bad-faith or unfair-practice claims</li><li>Late-notice or misrepresentation defenses</li><li>Deadlines that already need an attorney</li><li>Disputes too small to justify fees</li></ul></div>
</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker">Questions</p><h2>Straight answers before you sign anything</h2><p>Common questions property owners ask a {K} about cost, timing and when appraisal is the wrong move.</p><div class="btn-row"><a class="btn" href="{P_FAQ}">FAQ by topic {ic("arrow", size=18)}</a><a class="btn ghost" href="{P_GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Claim library</p><h2>Guides worth reading before a demand</h2><p>Practical reading from a {K} on policy language, documentation and pricing in rural West Virginia.</p></div>
<div class="grid post-grid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">Browse all six guides {ic("arrow", size=16)}</a></p>
</div></section>

<section class="pcta"><div class="pcta-bg" data-parallax="0.15">{img("gorge-overlook", alt="")}</div><div class="wrap pcta-in rv"><p class="kicker light">Before you cash the last check</p><h2>Ask a {K} to compare the line items first</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn pink" href="tel:{TEL}">{ic("phone", size=18)} Call {PHONE}</a><a class="btn line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start here</p><h2>Start with a free file review</h2><p>Tell us what happened and what the insurer offered. We’ll look it over and give you a straight answer about whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 55 West Virginia counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Appraisal",
                        "West Virginia Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid wind, water, ice and fire claims.",
                        body, [faq_schema(home_faqs)], preload="hero-gorge-bridge", main_business=True), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about this service</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Service areas", [(l["city"] + ", WV", loc_path(l)) for l in LOCATIONS[:6]] + [("All 55 counties", LOC_BASE)])}</aside></div>
{band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "West Virginia"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(svc_card(s, hl=2) for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across West Virginia",
                     f"Twelve ways a {BRAND} can help — from a single estimate review to full representation under the appraisal clause and neutral umpire work.", "roof-repair-brick") + f"""
<section class="sec"><div class="wrap"><div class="grid svc-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what the difference is worth. A review answers that in days, and plenty of disputes close at that point.</p><a class="btn" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow", size=18)}</a></div><div class="rv">{faq_block([("Can I hire you for only one step?", "Yes. Many owners begin with an estimate review and decide later whether to invoke appraisal."), ("Do you handle commercial and HOA claims?", "Yes — apartment buildings, retail, offices, churches, farms and association properties, as well as single-family homes."), ("Do you work outside the twelve cities listed?", "Yes. We inspect in all 55 counties, including rural areas a long way from the interstate.")])}</div></div></section>
{band()}"""
    write(SVC_BASE, document(SVC_BASE, "WV Insurance Appraisal Services | 12 Claim Types",
                             "Insurance appraisal services in West Virginia: appraisal clause help, estimate review, wind, water, ice, fire and mine subsidence claims.",
                             body, [crumbs_schema(trail), item_list(items)], preload="roof-repair-brick", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"] + ", WV", loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        city = l["city"]
        trail = [("Home", "/"), ("Service areas", LOC_BASE), (city, path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(e(n) for n in l["neighborhoods"])
        snap = f"""<div class="snapshot"><h2>{e(city)} at a glance</h2><dl>
<div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Region</dt><dd>{e(l["region"])}</dd></div>
<div class="w"><dt>Neighborhoods &amp; nearby</dt><dd>{hoods}</dd></div>
<div class="w"><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div>
<div class="w"><dt>Storm history</dt><dd>{e(l["storm"])}</dd></div>
<div class="w"><dt>Typical claim risks</dt><dd><ul class="chips">{chips}</ul></dd></div></dl></div>"""
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, f'{l["county"]} · {l["region"]}', f"Insurance Appraiser in {city}, WV", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On-site")]) + f"""
<div class="wrap layout"><article class="prose">{snap}
{l["body"]}
<h2>Services for {e(city)} property owners</h2>
<p>Every {BRAND} service is available in {e(city)} and the surrounding area, including:</p>
<ul class="cols2">{svc_links}</ul>
<h2>{e(city)} questions</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2>{related([("Nearby", LOC_BY[n]["city"] + ", WV", loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
<aside class="aside">{call_box()}{list_box("Service areas", items, path)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{band(f"Disputed claim in {city}?", "Send the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {city}, WV", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", West Virginia"}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        title = f"Insurance Appraiser {city}, WV | Claim Disputes"
        desc = f"Independent insurance appraiser for {city} and {l['county']}: appraisal and estimate review for underpaid storm, water, ice and fire claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {city} and {l['county']}: appraisal and estimate review for underpaid storm, water, ice and fire claims."
        write(path, document(path, title, desc, body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Service areas", LOC_BASE)]
    cards = "".join(loc_card(l, hl=2) for l in LOCATIONS)
    reg = "".join(
        f'<article class="region rv"><div class="region-ph">{img(REGION_PHOTO[k], sizes="(max-width:700px) 100vw, 33vw", alt="")}</div><div class="region-b"><p class="towns">{e(towns)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(txt)}</p><p class="small">Also: {e(c)}</p></div></article>'
        for k, n, towns, perils, txt, c in REGION_COPY)
    body = page_hero(trail, "Statewide", "Insurance Appraisal in All 55 West Virginia Counties",
                     f"{BRAND} inspects in person from Chester to Bluefield and Harpers Ferry to Kenova. These pages cover the cities where we are called most often.", "capitol-charleston") + f"""
<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="kicker">Twelve cities</p><h2>Local pages</h2></div><div class="grid loc-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ around the state</h2><p>River towns, mountain counties and fast-growing suburbs each produce their own kind of dispute.</p></div><div class="grid region-grid" data-stagger>{reg}</div></div></section>
{band("Don’t see your town?", "We cover every county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "West Virginia Service Areas | 55 Counties",
                             "Insurance appraisal in all 55 West Virginia counties, including Charleston, Huntington, Morgantown, Parkersburg, Wheeling and Martinsburg.",
                             body, [crumbs_schema(trail), item_list(items)], preload="capitol-charleston", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on what you enter and on your policy, and are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("All free tools", items, path)}</aside></div>
{band("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    cards = "".join(tool_card(t, hl=2) for t in TOOLS)
    order = [("claim-timeline-ics-planner", "Put every deadline on a calendar first."), ("roof-square-pitch-estimator", "Check the roof count against the carrier’s."),
             ("percentage-deductible-checker", "Know what the deductible takes off the top."), ("rcv-acv-holdback-calculator", "Split the claim into first check and holdback."),
             ("mine-subsidence-limit-calculator", "If the ground moved, compare repair cost with the endorsement cap."), ("claim-gap-fee-estimator", "Test whether appraisal pays after fees."),
             ("appraisal-readiness-scorecard", "Score the file before anyone signs a demand.")]
    by = {t["slug"]: t for t in TOOLS}
    steps = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(by[s]["name"])}</a> — {e(d)}</li>' for s, d in order)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for West Virginia Owners",
                     "Seven calculators and planners built from real appraisal work. No sign-up, and nothing you type leaves your browser.", "calculator-notes", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="grid tool-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">A suggested order</p><h2>Using the tools together</h2><ol class="steps">{steps}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Property Claim Calculators | WV Owners",
                              "Free claim tools for West Virginia owners: gap and fee estimator, ACV holdback, roof squares, deductibles, deadlines and mine subsidence.",
                              body, [crumbs_schema(trail), item_list(items)], preload="calculator-notes", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal step by step", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(n)}</a></li>' for i, (n, _t) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in West Virginia",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what and where files most often go wrong.", "paperwork",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="On this page"><p class="toc-t">The seven stages</p><ol>{toc}</ol></nav>{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in West Virginia", "description": "The stages of a property insurance appraisal, from the disagreement to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in WV | 7 Stages",
                         "A step-by-step guide to the insurance appraisal process in West Virginia: the demand, choosing appraisers and an umpire, and the award.",
                         body, [crumbs_schema(trail), howto], preload="paperwork"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("FAQ by topic", path)]
    jump = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ, Grouped by Topic",
                     f"{len(allq)} plain answers about appraisal costs, timing, West Virginia specifics and what happens after the award.", "consult-window") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="Topics"><p class="toc-t">Topics</p><ol>{jump}</ol></nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ by Topic | WV Claims",
                         "Answers to insurance appraisal questions in West Virginia, grouped by topic: costs, timing, deadlines, state specifics and the award.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="consult-window"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Appraisal glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Appraisal Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards, defined in plain English. Type to filter.", "calculator-paper", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="hint" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary | 40+ Claim Terms",
                         "Searchable glossary of insurance appraisal and claim terms: ACV, RCV, holdback, umpire, mine subsidence, matching, O&P and many more.",
                         body, [crumbs_schema(trail), dts], preload="calculator-paper"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim library", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim library", path)]
    cards = "".join(post_card(p, hl=2) for p in POSTS)
    body = page_hero(trail, "Claim library", "Insurance Claim Guides for West Virginia Owners",
                     "Practical guides on appraisal clauses, documentation, depreciation, pricing and the difference between landslide and mine subsidence claims.", "classic-kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="grid post-grid" data-stagger>{cards}</div></div></section>{band()}"""
    write(path, document(path, "Claim Library | Appraisal Guides for WV Owners",
                         "Guides for West Virginia property owners on appraisal clauses, storm documentation, depreciation, overhead and profit, and subsidence.",
                         body, [crumbs_schema(trail), item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="classic-kitchen", page_type="CollectionPage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About the firm", path)]
    body = page_hero(trail, "About the firm", "About West Virginia Insurance Appraiser",
                     "An appraisal and estimating practice built around one question on a disputed claim: what does the damage actually cost to repair?", "consult-window") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("meeting-laptop", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One job, done carefully</h2>
<p>Plenty of claim professionals try to do everything. We chose to concentrate on the amount of loss. {BRAND} serves as the appraiser you appoint under your policy, reviews estimates before a disagreement hardens, and sits as a neutral umpire on panels where we represent neither side. Our process, tools and documentation standards are all built around that single task.</p>
<h2>How a file is handled</h2>
<ul>
<li><strong>Scope before price.</strong> We inspect and measure before we look closely at anyone else’s numbers.</li>
<li><strong>Supportable over impressive.</strong> An inflated estimate loses the umpire’s trust. We price what we can back up with photos, measurements and local costs.</li>
<li><strong>Written in plain English.</strong> You will understand each difference between our valuation and the insurer’s.</li>
<li><strong>Straight triage.</strong> If the claim needs an attorney, a public adjuster or a simple supplement instead, we say so on the first call.</li>
<li><strong>Fees in writing</strong> before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, landlords, HOA boards, churches, farms, business owners, contractors, public adjusters and attorneys across West Virginia. On any claim we serve in one role only, and we disclose prior working relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and do not give legal advice. We do not act as a public adjuster or negotiate claims outside the appraisal process. And we do not promise outcomes — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>West Virginia’s terrain makes its claims unusually varied: river flooding in the Ohio Valley, derecho wind in the Eastern Panhandle, heavy snow in the Potomac Highlands, subsidence over old mine workings in the coalfields. Working in every county means we see — and price — all of it.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Service areas", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal step by step", P_PROCESS)])}</aside></div>{band()}"""
    write(path, document(path, "About the Firm | West Virginia Insurance Appraiser",
                         "Who we are: an independent West Virginia appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail)], preload="consult-window", page_type="AboutPage"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Request a review", path)]
    body = page_hero(trail, "Get in touch", "Request a Free Claim File Review",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "handshake", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv"><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 55 West Virginia counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Send your claim details", page=path)}</div></div></section>"""
    write(path, document(path, "Request a Claim Review | WV Insurance Appraiser",
                         "Request a free review of a disputed West Virginia property claim. Call or text (844) 537-1427, email us, or send claim details online.",
                         body, [crumbs_schema(trail)], preload="handshake", page_type="ContactPage"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown creator")} · {e((v.get("source") or "").title())}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Statement", "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Information you give us</h2><p>When you fill in a form, call or email, we receive what you choose to share: usually your name, phone number, email address, property location and details about your claim. Our host also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and review your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We do not sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our website and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>The calculators and planners run in your browser. What you type is not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We do not use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s own policy. If we add analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP at any time to opt out.</p>
<h2>Your choices</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> to ask us to access, correct or delete the information you have given us.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        P_TERMS: ("Terms and Conditions", "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. The content is general information about insurance appraisal and property claims in West Virginia.</p>
<h2>No client relationship</h2><p>Reading the site, using its tools or sending a form does not make you our client. That relationship starts only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. For legal questions, consult a licensed West Virginia attorney.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any outcome. Example figures are illustrative.</p>
<h2>Content ownership</h2><p>Site text, design and tools belong to {BRAND}. You may link to pages and print them for personal use. Photographs are used under the licenses listed on the <a href="{P_CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we are not liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of West Virginia.</p>"""),
        P_DISC: ("Legal Notice", "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>This website explains how insurance appraisal commonly works. Your own policy language controls. Always read your policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we do not give legal advice, and we do not act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site changes or extends any deadline. If one is approaching, consult a West Virginia attorney promptly.</p>
<h2>Statutes and agencies</h2><p>References to West Virginia law, the Offices of the Insurance Commissioner, the Essential Property Insurance Association or the mine subsidence program are general context. Confirm current rules with official sources.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They do not show our clients’ properties or the specific events described.</p>"""),
        P_CREDITS: ("Photo Credits", "Sources and licenses for every photograph used on this site.", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> (mostly via rawpixel, StockSnap, Flickr and Wikimedia Commons) or marked <strong>public domain</strong>, such as photos by U.S. government agencies. Attribution is not legally required, but we credit each source here with thanks. All photos were found through the Openverse search engine. They are illustrative and do not show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    titles = {P_PRIV: "Privacy Statement | WV Insurance Appraiser", P_TERMS: "Terms and Conditions | WV Insurance Appraiser",
              P_DISC: "Legal Notice | WV Insurance Appraiser", P_CREDITS: "Photo Credits | WV Insurance Appraiser"}
    descs = {P_PRIV: "Privacy statement for westvirginiainsuranceappraiser.com: what we collect through forms and calls, how we use it, and the choices you have.",
             P_TERMS: "Terms and conditions for using westvirginiainsuranceappraiser.com and its free claim tools, including limits on advice and liability.",
             P_DISC: "Legal notice: this site offers general information on insurance appraisal in West Virginia, not legal advice, and no outcome is guaranteed.",
             P_CREDITS: "Photo credits for westvirginiainsuranceappraiser.com: the CC0 and public-domain sources and licenses for every photograph on the site."}
    for path, (title, lede, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "stone-office", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, titles[path], descs[path], body, [crumbs_schema(trail)], preload="stone-office"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About the firm", P_ABOUT), ("Request a review", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Service areas", [("All service areas", LOC_BASE)] + [(l["city"] + ", WV", loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy statement", P_PRIV), ("Terms and conditions", P_TERMS), ("Legal notice", P_DISC), ("Photo credits", P_CREDITS)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on the {BRAND} website.", "blue-ridges", cta=False) + f'<section class="sec"><div class="wrap"><div class="map-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, "Site Map | West Virginia Insurance Appraiser", "Every page on West Virginia Insurance Appraiser in one list: services, service areas, free claim tools, guides and site information.", body, [crumbs_schema(trail)], preload="blue-ridges"), 0.3)

    body = f"""<section class="phero nf"><div class="phero-bg">{img("ice-storm-road", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker light">Error 404</p><h1>This road is closed</h1><p class="lede">The page you were looking for has moved or never existed. One of these should get you back on track.</p><div class="btn-row"><a class="btn pink" href="/">Home</a><a class="btn line light" href="{SVC_BASE}">Services</a><a class="btn line light" href="{TOOL_BASE}">Free tools</a><a class="btn line light" href="{P_CONTACT}">Contact</a></div></div></section>"""
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
// West Virginia Insurance Appraiser - front controller for the static build.
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
