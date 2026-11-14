#!/usr/bin/env python3
"""Static site generator for idahoinsuranceappraiser.com.

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
from tools import TOOLS, GAP_MINI, TOOL_BASE  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))

BRAND = "Idaho Insurance Appraiser"
HOST = "idahoinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261114a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster
HOURS = "Mon–Fri 8am–6pm MT"

# Google Tag Manager: leave empty until a container ID is provided (e.g. "GTM-XXXXXXX").
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

# URL structure (deliberately different from the sister sites)
SVC_BASE = "/property-claim-appraisal/"
LOC_BASE = "/idaho-appraisal-areas/"
POST_BASE = "/appraisal-know-how/"
P_PROCESS = "/how-the-appraisal-clause-works/"
P_FAQ = "/idaho-appraisal-questions/"
P_GLOSS = "/claim-terms-defined/"
P_ABOUT = "/our-appraisal-approach/"
P_CONTACT = "/schedule-a-consult/"
P_PRIV = "/privacy-policy-and-data/"
P_TERMS = "/terms-of-access/"
P_DISC = "/appraisal-limits-disclaimer/"
P_SMAP = "/idaho-site-directory/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraiser/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
CITY_COUNT = len(LOCATIONS)

# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appraiser": "consult-table", "home-insurance-appraisal": "home-exterior",
    "commercial-hoa-farm-appraisal": "commercial-building", "roof-hail-damage-appraisal": "hail-ground",
    "wind-microburst-claim-appraisal": "storm-front", "water-frozen-pipe-appraisal": "frozen-pipe",
    "fire-smoke-damage-appraisal": "house-fire", "wildfire-claim-appraisal": "wildfire-ridge",
    "snow-load-ice-dam-appraisal": "snow-roof", "claim-estimate-review": "laptop-docs",
    "appraisal-umpire-services": "meeting-room",
}
LOC_PHOTO = {
    "boise": "hero", "meridian": "neighborhood", "nampa": "farm-barn", "caldwell": "farmland",
    "eagle": "home-exterior-2", "idaho-falls": "idaho-falls", "pocatello": "pocatello", "rexburg": "snow-house",
    "twin-falls": "twin-falls", "coeur-d-alene": "coeur-d-alene", "lewiston": "lewiston", "ketchum": "sun-valley",
}
TOOL_PHOTO = {
    "claim-gap-net-estimator": "calculator", "rcv-acv-holdback-calculator": "paperwork",
    "roof-pitch-squares-calculator": "roof-shingles", "percentage-deductible-calculator": "thunderstorm",
    "idaho-claim-timeline-builder": "laptop-docs", "appraisal-readiness-checkup": "clipboard",
    "roof-snow-load-estimator": "icicles",
}
POST_PHOTO = {
    "idaho-appraisal-clause-plain-english": "consult-table", "documenting-hail-and-wind-on-the-snake-river-plain": "hail-ground",
    "wildfire-smoke-claims-what-to-expect": "wildfire-smoke", "snow-load-collapse-claims-guide": "snow-roof",
    "appraiser-public-adjuster-or-attorney": "meeting-room", "reading-an-xactimate-estimate": "paperwork",
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
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "mountain": '<path d="M3 20l6.5-11 4 6 2.5-3.5L21 20z"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-clause-appraiser": "doc", "home-insurance-appraisal": "home", "commercial-hoa-farm-appraisal": "building",
    "roof-hail-damage-appraisal": "hail", "wind-microburst-claim-appraisal": "wind", "water-frozen-pipe-appraisal": "drop",
    "fire-smoke-damage-appraisal": "flame", "wildfire-claim-appraisal": "tree", "snow-load-ice-dam-appraisal": "snow",
    "claim-estimate-review": "file", "appraisal-umpire-services": "scale",
}

# Logo mark: navy tile, yellow twin-peak "roofline" (mountains + roof), white level line, small sun.
MARK_SVG = ('<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#003776"/>'
            '<circle cx="35" cy="13" r="3.2" fill="#FFE835"/>'
            '<path d="M8 33.5L18.5 18l6.5 8.5 4.8-6.2L40 33.5" fill="none" stroke="#FFE835" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M13 39.5h22" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')


def brand(extra_cls=""):
    return (f'<a class="brand{extra_cls}" href="/" aria-label="{BRAND} home">{MARK_SVG}'
            f'<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "ID", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-ID", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Idaho property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Idaho.",
        "areaServed": [{"@type": "State", "name": "Idaho"}] + [{"@type": "City", "name": l["city"].split(" &")[0]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "@id": DOMAIN + "/#catalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Wildfire claims", "Snow load damage"],
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
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}


def item_list(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
LEARN = [("How the appraisal clause works", P_PROCESS), ("Idaho appraisal FAQ", P_FAQ), ("Claim terms defined", P_GLOSS), ("Appraisal know-how guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Areas", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Idaho areas", LOC_BASE)),
        ("Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="head" id="top">
<div class="strip"><div class="wrap"><span>Statewide property claim appraisal · all 44 Idaho counties</span><span class="strip-r"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></span></div></div>
<div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-y head-cta" href="{P_CONTACT}">Free claim review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div>
</header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand(" brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>{HOURS} · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap"><p class="foot-band-t">Think your claim was underpaid? Get a second set of eyes on the numbers.</p><div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-w" href="{P_CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand(" brand-foot")}
<p>Independent appraisal and estimating support for Idaho property owners with disputed insurance claims, from the Panhandle lakes to the Upper Snake.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("clock")}{HOURS}</li></ul></div>
<div><h2 class="ft">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="ft">Areas</h2><ul>{loc}<li><a href="{LOC_BASE}">All Idaho areas</a></li></ul></div>
<div><h2 class="ft">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="ft">Resources</h2><ul><li><a href="{P_ABOUT}">About</a></li><li><a href="{P_PROCESS}">How appraisal works</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal">
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we do not give legal advice and we do not act as a public adjuster. Information on this site is general and educational; policy terms vary. Example figures are illustrative, and no outcome is guaranteed.</p>
<div class="foot-bottom"><span>© {date.today().year} {BRAND}</span><ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_SMAP}">Site directory</a></li></ul></div>
</div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],\n"
            f"j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\nheight="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero"):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    page_extra = {}
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            page_extra = {k: v for k, v in n.items() if k != "@type"}
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
        extra.append(n)
    p = PHOTOS[photo]
    img_url = f"{DOMAIN}/assets/img/photos/{photo}.webp"
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": img_url, "width": p["fw"], "height": p["fh"], "caption": p["alt"]},
    }
    webpage.update(page_extra)
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra if n.get("@type") in MAIN_TYPES]
    webpage["mainEntity"] = {"@id": main[0]} if main else {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw" fetchpriority="high">\n')
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Idaho">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Idaho">
<meta name="geo.region" content="US-ID">
<meta name="geo.placename" content="Idaho">
<meta name="theme-color" content="#003776">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Chivo:wght@600;700;800;900&display=swap">
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
    """Homepage -> home.html; every other page -> dir/index.php that starts with the canonical-host guard.

    The host serves real files directly without running the root index.php, so a plain dir/index.html
    would skip the www/http redirect. Never write a dir/index.html page.
    """
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
        depth = rel.count("/")
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-w" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.15"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through, free</h2><p>A short call tells you whether appraisal fits your claim, or whether something else would serve you better.</p><a class="big-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-y full" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Not sure the payout covers the repair?", p="Send the insurer’s estimate. We’ll read it line by line and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-w" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="aside"><div class="aside-in">{aside}</div></aside></div>'


LOSSES = ["Hail", "Wind / microburst", "Wildfire / smoke", "Snow load / ice dam", "Water / frozen pipe", "Fire", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", page="/", hl="h2", fid="f"):
    roles = ["Homeowner", "Business owner", "Property manager / HOA", "Farm or ranch owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Idaho"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hl} class="form-t">{e(heading)}</{hl}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Approx. amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-t">Get a free claim review</h2><p class="form-sub">Tell us the basics. We’ll call within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{P_PRIV}">privacy policy</a>.</span></label>
<button class="btn btn-navy full" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="form-trust">{ic("shield")}No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Treasure Valley", "Boise · Meridian · Nampa · Caldwell · Eagle", ["Hail", "Microbursts", "Foothills wildfire", "Frozen pipes"],
     "Idaho’s population center packs historic Boise homes, fast-growing subdivisions and working farms into one valley. Summer storms, foothills fire and January cold snaps drive most claims.", "boise", "hero"),
    ("North Idaho", "Coeur d’Alene · Post Falls · Sandpoint", ["Windstorms", "Falling timber", "Heavy snow", "Smoke"],
     "Forests, lakes and deeper winters. Wind-thrown trees, snow-loaded roofs and ice dams lead the list, with lake homes and vacation rentals adding coverage wrinkles.", "coeur-d-alene", "coeur-d-alene"),
    ("Lewis-Clark & Palouse", "Lewiston · Moscow · Orofino", ["Wind", "Grass fires", "Hail", "Water losses"],
     "Idaho’s lowest, warmest valley meets the rolling Palouse. Canyon winds, grass fires and summer storms shape claims on older hillside homes and university rentals.", "lewiston", "lewiston"),
    ("Wood River & Central Mountains", "Ketchum · Sun Valley · Hailey · McCall", ["Snow load", "Ice dams", "Wildfire", "Frozen pipes"],
     "Mountain construction costs, second homes left empty for weeks and some of the state’s heaviest snow loads. Wildfire season follows the melt.", "ketchum", "sun-valley"),
    ("Magic Valley", "Twin Falls · Jerome · Burley", ["High wind", "Hail", "Farm structures", "Snow load"],
     "The canyon-rim city and its agricultural hinterland: dairies, storage buildings and growing subdivisions, all exposed to wind across open ground.", "twin-falls", "twin-falls"),
    ("Eastern Idaho", "Idaho Falls · Pocatello · Rexburg", ["Hail", "Canyon wind", "Deep cold", "Snow load"],
     "Long winters on the Upper Snake plain, wind through the Portneuf Gap and summer hail. Student apartments, potato cellars and older neighborhoods all see claims.", "idaho-falls", "idaho-falls"),
]


def home():
    K = BRAND
    stats = [("44", "Idaho counties served", "44"), ("11", "Appraisal & estimating services", str(len(SERVICES))), (str(len(TOOLS)), "Free browser-based tools", str(len(TOOLS))), ("2 of 3", "Signatures that make an award", None)]
    stat_html = "".join(f'<div class="stat rv"><b{f" data-count=\"{c}\"" if c else ""}>{v}</b><span>{e(t)}</span></div>' for v, t, c in stats)

    peril_keys = ["roof-hail-damage-appraisal", "wildfire-claim-appraisal", "snow-load-ice-dam-appraisal", "wind-microburst-claim-appraisal", "water-frozen-pipe-appraisal", "fire-smoke-damage-appraisal"]
    sv = {s["slug"]: s for s in SERVICES}
    peril_cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{k}/"><span class="pcard-img">{img(SVC_PHOTO[k], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="pcard-b"><span class="pcard-ic">{ic(SVC_ICON[k])}</span><h3>{e(sv[k]["name"])}</h3><p>{e(sv[k]["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for k in peril_keys)
    other = [s for s in SERVICES if s["slug"] not in peril_keys]
    other_list = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{ic(SVC_ICON[s["slug"]])}<span><b>{e(s["name"])}</b><small>{e(s["short"])}</small></span></a></li>' for s in other)

    steps = "".join(f'<li class="tstep rv"><span class="tnum">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate([
        ("Free claim review", f"We read the policy, the insurer’s estimate and your photos, then tell you plainly whether appraisal fits."),
        ("Independent scope", "On-site inspection, measurements and a line-item estimate priced for your part of Idaho."),
        ("Written demand", f"Appraisal is invoked in writing and {K} is named as your appraiser within the policy’s deadline."),
        ("Panel work", "We work through the gap line by line with the insurer’s appraiser. Most disputes narrow here."),
        ("Signed award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]))

    regions = "".join(
        f'<article class="region rv"><div class="region-img">{img(ph, sizes="(max-width:700px) 86vw, 420px", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p><a class="more" href="{loc_path(LOC_BY[link])}">{e(LOC_BY[link]["city"])} page {ic("arrow")}</a></div></article>'
        for n, c, perils, t, link, ph in REGIONS)

    tools = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<span class="tcard-k">{e(t["kind"])}</span></span><span class="tcard-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    cities = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a></li>' for l in LOCATIONS)
    posts = "".join(f'<article class="gcard rv"><a class="gcard-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><p class="meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        (f"What does an {K} do?", f"An {K} values property damage when you and your insurer agree the loss is covered but disagree on the cost. As your named appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call an {K}?", "When coverage is accepted, you have the insurer’s estimate, and the gap between it and your contractor’s number is meaningful, often more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "Generally yes, on the amount of loss, once two of the three panel members sign it. That’s why documentation matters before you invoke appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before work starts, and the first conversation is free."),
        ("Do you cover my part of Idaho?", "Yes. We work in all 44 counties, from Coeur d’Alene and Lewiston to Boise, Twin Falls, Ketchum, Pocatello and Idaho Falls."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero", lazy=False, alt="", extra=' data-parallax="0.2"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent property claim appraisal · Statewide</p>
<h1><span class="hlt">{K}</span> for claims that came up short</h1>
<p class="lede">Your insurer accepted the claim, then sent a number that won’t cover the repair. {K} builds an independent, line-by-line valuation of the damage and takes it through the appraisal process in your policy.</p>
<div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-w" href="#services">See what we handle {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Retained by you, not the insurer</li><li>{ic("check")}Homes, HOAs, farms &amp; commercial</li><li>{ic("check")}All 44 counties</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="stats" aria-label="At a glance"><div class="wrap stats-in" data-stagger>{stat_html}</div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="intro-copy rv">
<p class="kicker dark">Why owners call us</p>
<h2>What an {K} does that an adjuster won’t</h2>
<p>Most short claims aren’t denials. They’re estimates missing a roof plane, a matching wall of siding or the code items a rebuild actually needs. {K} exists for that space between “covered” and “paid in full.”</p>
<p>The adjuster works for the insurer. When you retain {K}, we start from our own inspection and our own measurements, and we price the repair your property needs in your part of the state, whether that’s a Boise bungalow, a Rexburg apartment block or a barn outside Jerome.</p>
<ul class="ticks">
<li>{ic("check")}<span><b>A fresh valuation, not an edit.</b> Our own scope, never a marked-up copy of the insurer’s estimate.</span></li>
<li>{ic("check")}<span><b>Numbers built to hold.</b> Priced so they survive an umpire’s scrutiny.</span></li>
<li>{ic("check")}<span><b>Honest triage.</b> If you need an attorney or a simple supplement instead, we say so on the first call.</span></li>
</ul>
<a class="btn btn-navy" href="{P_ABOUT}">Our approach {ic("arrow")}</a>
</div>
<figure class="intro-fig rv">{img("roof-inspection", sizes="(max-width:900px) 100vw, 520px")}<figcaption><b>{K}</b><span>Independent of the insurer, start to finish</span></figcaption></figure>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Idaho perils</p><h2>Claims {K} handles across the state</h2><p>Six perils account for most disputed claims in Idaho. Each has its own estimating traps, and each has its own page explaining how we value it.</p></div>
<div class="pgrid" data-stagger>{peril_cards}</div>
<div class="svc-more rv"><h3>More ways {K} can help</h3><ul class="svc-list">{other_list}</ul><a class="btn btn-line" href="{SVC_BASE}">All appraisal services {ic("arrow")}</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">The process</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how {K} moves a file through it.</p></div>
<div class="tline" data-tline><div class="tline-track" aria-hidden="true"><span></span></div><ol class="tline-steps">{steps}</ol></div>
<p class="center"><a class="link" href="{P_PROCESS}">Read the full appraisal clause guide</a></p>
</div></section>

<section class="sec navy"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Six regions, six claim climates</p><h2>Local knowledge from the Panhandle to the Upper Snake</h2><p>Snow loads in Ketchum, hail in Idaho Falls, wind in Pocatello, wildfire above Boise. An {K} has to know how each region’s weather shows up on a building and in an estimate.</p></div>
<div class="carousel" data-carousel><div class="car-track" tabindex="0" aria-label="Idaho regions">{regions}</div><div class="car-nav"><button type="button" class="car-btn" data-dir="-1" aria-label="Previous region">{ic("left")}</button><button type="button" class="car-btn" data-dir="1" aria-label="Next region">{ic("right")}</button></div></div>
</div></section>

<section class="sec yel" id="gap"><div class="wrap gap-in">
<div class="gap-copy rv"><p class="kicker dark">Quick gap check</p><h2>Is your gap worth appraisal?</h2><p>Enter the two estimates you already have. A large gap is worth a conversation with an {K}. A small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}claim-gap-net-estimator/">claim gap estimator</a> adds fees and shows your net at three landing points. Figures are illustrative.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Free &amp; private</p><h2>Free claim tools from {K}</h2><p>Run the numbers before you call anyone. Every tool works in your browser, and nothing you type is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tools}</div>
<p class="center"><a class="btn btn-line" href="{TOOL_BASE}">Open the tool index {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap areas-in">
<div class="areas-fig rv">{img("snake-river", sizes="(max-width:900px) 100vw, 520px")}</div>
<div class="rv"><p class="kicker dark">Where we work</p><h2>{K} service areas</h2><p>{K} works in every Idaho county. These {CITY_COUNT} communities are where we handle claims most often, and each page covers local housing, weather history and common disputes.</p>
<ul class="city-list">{cities}</ul>
<a class="link" href="{LOC_BASE}">All Idaho service areas</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Right tool, right job</p><h2>When appraisal fits, and when it doesn’t</h2><p>{K} will point you elsewhere when appraisal isn’t the right lever. Here’s the short version.</p></div>
<div class="fit" data-stagger>
<div class="fit-card yes rv"><h3>{ic("check")}Good fit</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair-versus-replace disagreements</li><li>Matching and discontinued materials</li><li>Missing trades, code items or overhead and profit</li><li>Snow-load or hail scope disputes</li></ul></div>
<div class="fit-card no rv"><h3>{ic("x")}Poor fit</h3><ul><li>Outright coverage denials</li><li>Bad-faith or other legal claims</li><li>Gaps too small to justify fees</li><li>A suit deadline that needs an attorney now</li><li>Disputes over what the policy means</li></ul></div>
</div>
<div class="table-wrap rv"><table class="compare"><caption class="sr-only">Comparing an appraiser, a public adjuster and an attorney</caption><thead><tr><th scope="col">Question</th><th scope="col" class="hl">{K}</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Manage and negotiate the claim</td><td>Legal disputes and litigation</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Award signed by two of three</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on policy language, documentation and strategy for Idaho claims.</p></div>
<div class="ggrid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All appraisal know-how guides</a></p>
</div></section>

<section class="sec"><div class="wrap faq-in">
<div class="rv"><p class="kicker dark">FAQ</p><h2>Questions people ask an {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{P_FAQ}">All questions {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim terms defined</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec navy" id="contact"><div class="wrap contact-in">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to an {K} about your claim</h2><p>Tell us what happened and what the insurer offered. You’ll get a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="contact-lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>{HOURS}</b></span></li><li>{ic("pin")}<span><small>Coverage</small><b>All 44 Idaho counties</b></span></li></ul></div>
<div class="rv">{lead_form(page="/", hl="h3", fid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Idaho Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wildfire, snow and water claims.",
                        body, [faq_schema(home_faqs)], photo="hero"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a class="rel" href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        ph = SVC_PHOTO[s["slug"]]
        article = f"""{s["body"]}
<h2>Questions about {e(s["keyword"])}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>"""
        aside = call_box() + list_box("All services", items, path) + list_box("Where we work", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All Idaho areas", LOC_BASE)])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(article, aside) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Idaho"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">{ic(SVC_ICON[s["slug"]])}Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Idaho",
                     "From a single estimate review to full panel representation and neutral umpire work, every Idaho Insurance Appraiser service is built around one thing: an accurate, defensible valuation of the loss.", "roof-inspection") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-in"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes end there.</p><a class="btn btn-navy" href="{SVC_BASE}claim-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and ranch buildings?", "Yes. Barns, shops, storage buildings and other agricultural structures are a regular part of our work."), ("Do you only work on storm claims?", "No. We also handle fire, wildfire, water, snow-load and other covered losses.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Idaho | Claim Valuation",
                             "Insurance appraisal services across Idaho: appraisal clause work, estimate review, hail, wildfire, snow-load and water claims, and umpiring.",
                             body, schema, photo="roof-inspection"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        city = l["city"]
        kw = f"{city} Insurance Appraiser"
        trail = [("Home", "/"), ("Service areas", LOC_BASE), (city, path)]
        near = "".join(f'<a class="rel" href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        article = f"""<div class="localbox"><div><h2 class="lb-t">Local claim risks</h2><ul class="chips">{chips}</ul></div><div><h2 class="lb-t">Housing mix</h2><p>{e(l["housing"])}</p></div></div>
{l["body"]}
<h2>Services for {e(city)} property owners</h2>
<p>Every {BRAND} service is available in {e(city)} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>Questions for a {e(kw)}</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="related">{near}</div>"""
        aside = call_box() + list_box("Idaho service areas", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], kw, l["lede"], ph, [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(article, aside) + cta_strip(f"Disputed claim in {city}?", "Send the estimate and your photos. We’ll tell you honestly what we see.")
        place = city.split(" &")[0]
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {city}, Idaho", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": place, "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Idaho"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Service areas", LOC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{loc_path(l)}"><span class="icard-img">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span><span class="icard-b"><span class="icard-k">{ic("pin")}{e(l["county"])}</span><h2>{e(l["city"])}</h2><p>{e(l["lede"])}</p></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="rrow rv"><h3>{e(n)}</h3><p class="region-c">{e(c)}</p><p>{e(t)}</p></div>' for n, c, _p, t, _l, _ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 44 Idaho Counties",
                     f"Idaho Insurance Appraiser works statewide, from the Canadian border to the Bear River. These {CITY_COUNT} area pages cover the communities where we handle claims most often.", "sawtooth") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker dark">Regions</p><h2>How claims differ across Idaho</h2><p>The same policy language plays out very differently in a Ketchum chalet, a Meridian two-story and a Coeur d’Alene lake cabin.</p></div><div class="rrows" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Idaho county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Idaho Insurance Appraisal Service Areas | All 44 Counties",
                             "Insurance appraisal in all 44 Idaho counties, including Boise, Meridian, Nampa, Idaho Falls, Pocatello, Twin Falls and Coeur d’Alene.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)], photo="sawtooth"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a class="rel" href="{TOOL_BASE}{o["slug"]}/"><small>{e(o["kind"])}</small>{e(o["name"])}</a>' for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)])
        ph = TOOL_PHOTO[t["slug"]]
        article = f"""{t["explain"]}
<h2>Questions about the {e(t["keyword"])}</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div>"""
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice.</p></div></section>
{layout(article, call_box() + list_box("All free tools", items, path))}
{cta_strip("Want a professional to check the numbers?", "Send the estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    cards = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="tcard-k">{e(t["kind"])}</span></span><span class="tcard-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Idaho Owners",
                     f"{len(TOOLS)} calculators and planners drawn from real appraisal work. Use them to understand your claim, check the insurer’s math and plan next steps. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-in"><div class="rv"><p class="kicker dark">Suggested order</p><h2>Using the tools together</h2><ol class="steps-ol"><li>Start with the <a href="{TOOL_BASE}idaho-claim-timeline-builder/">claim timeline builder</a> so no deadline slips.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof squares calculator</a>, or the weight on it with the <a href="{TOOL_BASE}roof-snow-load-estimator/">snow load estimator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV vs. ACV</a> calculators.</li><li>Size the dispute with the <a href="{TOOL_BASE}claim-gap-net-estimator/">claim gap estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Idaho | 7 Tools",
                              "Free insurance claim calculators for Idaho owners: claim gap, RCV vs ACV, roof squares, deductible, snow load and deadline tools in one place.",
                              body, schema, photo="calculator"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("How the appraisal clause works", path)]
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(n)}</a></li>' for i, (n, _d) in enumerate(PROCESS_STEPS))
    article = f'<nav class="toc" aria-label="On this page"><p class="toc-t">The seven stages</p><ol>{toc}</ol></nav>{PROCESS_BODY}'
    body = page_hero(trail, "Process guide", "How the Insurance Appraisal Clause Works in Idaho",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", "clipboard",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(article, call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal clause works in Idaho", "description": "The seven stages of a property insurance appraisal, from the disagreement to the signed award.",
             "totalTime": "P90D", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How the Appraisal Clause Works in Idaho | 7-Stage Guide",
                         "How the appraisal clause works in Idaho, step by step: the written demand, choosing appraisers and an umpire, panel work and the award.",
                         body, [crumbs_schema(trail), howto], photo="clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Idaho appraisal FAQ", path)]
    jump = "".join(f'<li><a href="#faq-{i}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    article = f'<nav class="toc" aria-label="Topics"><p class="toc-t">Jump to a topic</p><ul>{jump}</ul></nav>{groups}'
    body = page_hero(trail, "Answers", "Idaho Insurance Appraisal Questions, Answered",
                     "Plain answers to the questions Idaho property owners ask most about appraisal, grouped by topic: how it works, costs and timing, Idaho specifics and working with us.", "living-room") + layout(article, call_box() + list_box("Resources", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email. We’re glad to talk it through.")
    write(path, document(path, "Idaho Insurance Appraisal FAQ | Costs, Timing & Rules",
                         "Idaho insurance appraisal FAQ grouped by topic: how appraisal works, what it costs, how long it takes and the Idaho rules worth knowing.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms defined", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gterm"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    article = f'<div class="gfilter"><label for="gloss-filter">Search {len(GLOSSARY)} terms</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="hint" data-gcount aria-live="polite"></p></div><div class="az" aria-label="Jump to letter">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Property Claim Terms Defined in Plain English",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, each explained in a sentence or two. Type in the search box to filter.", "paperwork", cta=False) + layout(article, call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Defined | Searchable Glossary",
                         "Searchable glossary of insurance claim terms: actual cash value, holdback, umpire, snow load, O&P and more, defined in plain English.",
                         body, [crumbs_schema(trail), dts], photo="paperwork"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = "".join(f'<a class="rel" href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        article = f'<p class="byline">By {BRAND} · <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div>'
        body = page_hero(trail, "Guide", p["title"], e(p["summary"]), ph, cta=False) + layout(article, call_box() + list_box("Resources", LEARN) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["keyword"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(f'<article class="gcard rv"><a class="gcard-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="gcard-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Appraisal know-how", "Insurance Appraisal Guides for Idaho Owners",
                     "Practical guides on policy language, documentation and claim strategy, written for Idaho homeowners, businesses and farm owners.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Appraisal Guides for Idaho Property Owners",
                         "Insurance appraisal guides for Idaho owners: the appraisal clause, hail documentation, wildfire smoke, snow-load claims and reading estimates.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    article = f"""
<figure class="lead-img">{img("consult-table", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a bit of everything. {BRAND} chose one job: the amount of loss. Our process, tools and documentation standards are built around answering that question well. That focus lets us serve as your named appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we study anyone else’s numbers.</li>
<li><strong>Defensible over dramatic.</strong> An inflated estimate looks good on day one and loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we tell you.</li>
<li><strong>Fees in writing.</strong> You know exactly what it costs before work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, farm and ranch owners, churches, business owners, contractors and attorneys across Idaho. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. And we don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Statewide on purpose</h2>
<p>Idaho’s weather changes dramatically between the Panhandle, the Treasure Valley, the central mountains and the Upper Snake. Working statewide means we see every kind of loss the state produces, from wind-thrown pines in Kootenai County to snow-crushed barns in Canyon County and hail across Bonneville County, and we price each one with local knowledge.</p>"""
    body = page_hero(trail, "About us", "About Idaho Insurance Appraiser",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "roof-inspection") + layout(article, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Service areas", LOC_BASE), ("Free tools", TOOL_BASE), ("How the appraisal clause works", P_PROCESS)])) + cta_strip()
    write(path, document(path, "About Idaho Insurance Appraiser | Our Appraisal Approach",
                         "About Idaho Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="roof-inspection"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Idaho Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "meeting-room", cta=False) + f"""
<section class="sec"><div class="wrap contact-in">
<div class="rv"><h2>Reach us directly</h2>
<ul class="contact-lines dark"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>{HOURS}</b></span></li><li>{ic("pin")}<span><small>Service area</small><b>Statewide, all 44 counties</b></span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks plain"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The insurer’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the insurer</span></li><li>{ic("check")}<span>Photos and any contractor estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hl="h2", fid="k")}</div></div></section>"""
    write(path, document(path, "Contact Idaho Insurance Appraiser | (844) 537-1427",
                         "Contact Idaho Insurance Appraiser for a free review of your disputed property claim. Call or text (844) 537-1427, or send the details here.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="meeting-room"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Policy", "privacy policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data, such as IP address, browser type and pages requested, for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will be updated to describe it.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                 "How we collect, use and protect what you share with us.",
                 "Privacy policy for Idaho Insurance Appraiser: what we collect through forms, calls and email, how we use it and how to request changes."),
        P_TERMS: ("Terms of Use", "terms of use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content provides general information about insurance appraisal and property claims in Idaho.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Idaho attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates based on the information you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Idaho.</p>""",
                 "The terms that apply when you use this website and its tools.",
                 "Terms of use for the Idaho Insurance Appraiser website: no legal advice, no client relationship from browsing and limits on tool results."),
        P_DISC: ("Disclaimer", "disclaimer", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Legal references</h2><p>Mentions of Idaho statutes, regulators, court decisions or bad-faith law are general descriptions for context. They may be incomplete or out of date. Verify current law with an Idaho attorney or official sources such as the Idaho Department of Insurance.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an Idaho attorney promptly.</p>
<h2>Weather and events</h2><p>References to storms, fires and other events are for context and drawn from public reporting. They aren’t statements about any specific property.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>""",
                 "Important limits on the information published on this website.",
                 "Disclaimer for Idaho Insurance Appraiser: general information only, no legal advice, illustrative figures and no guarantee of any claim result."),
    }
    for path, (title, kw, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "commercial-building", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)


def sitemap_pages():
    path = P_SMAP
    trail = [("Home", "/"), ("Site directory", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Service areas", [("All Idaho areas", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIV), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="dir-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Directory", f"Every page on {BRAND}, grouped by section.", "commercial-building", cta=False) + f'<section class="sec"><div class="wrap dir" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Directory | {BRAND}", "The Idaho Insurance Appraiser site directory: every service, Idaho service area, free claim tool, guide and legal page listed in one place.", body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-bg">{img("storm-front", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>That page isn’t here</h1><p class="lede">It may have moved, or the link may be mistyped. Try one of these instead.</p><div class="btn-row"><a class="btn btn-y" href="/">Home</a><a class="btn btn-line-w" href="{SVC_BASE}">Services</a><a class="btn btn-line-w" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line-w" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "Page not found on Idaho Insurance Appraiser. The link may be old or mistyped, so try our services, free claim tools or contact page instead.", body, robots="noindex,follow", photo="storm-front"), sitemap=False)


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w", encoding="utf-8") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, "_guard.php"), "w", encoding="utf-8") as f:
        f.write(GUARD_PHP)
    # Google Search Console verification: exact bytes, no newline, no BOM, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Idaho Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$iia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$iia_real  = 'idahoinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$iia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://idahoinsuranceappraiser.com - only on the real domain.
if ($iia_host === 'www.' . $iia_real || ($iia_host === $iia_real && $iia_proto === 'http')) {
    header('Location: https://' . $iia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$iia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($iia_uri, '?'), $iia_m)) {
    $iia_q = strpos($iia_uri, '?') !== false ? substr($iia_uri, strpos($iia_uri, '?')) : '';
    header('Location: ' . $iia_m[1] . $iia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($iia_host !== $iia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Idaho Insurance Appraiser - front controller for the static build.
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
