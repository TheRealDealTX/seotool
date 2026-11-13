#!/usr/bin/env python3
"""Static site generator for alaskainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php behind the canonical-host guard.
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

BRAND = "Alaska Insurance Appraiser"
HOST = "alaskainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is printed.
GTM_ID = "GTM-W3M89TSN"
HOURS = "Mon–Fri 8am–6pm Alaska Time"

SVC_BASE = "/appraisal-practice/"
LOC_BASE = "/communities-served/"
TOOL_BASE = "/appraisal-tools/"
POST_BASE = "/alaska-claim-guides/"
P_PROCESS = "/appraisal-clause-process/"
P_FAQ = "/alaska-appraisal-faq/"
P_GLOSS = "/insurance-claim-glossary/"
P_ABOUT = "/about-the-practice/"
P_CONTACT = "/contact-an-appraiser/"
P_PRIV = "/privacy-and-data/"
P_TERMS = "/website-use-terms/"
P_DISC = "/appraisal-disclaimer/"
P_CREDITS = "/photo-credits/"
P_MAP = "/full-site-map/"

e = html.escape
pages = []  # (path, priority)


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraiser/"


def loc_city(l):
    return l["city"]


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {k: v.get("alt", "") for k, v in PHOTOS.items()}

SVC_PHOTO = {
    "appraisal-panel-representation": "consultation", "home-insurance-claim-appraisal": "house-winter",
    "commercial-hoa-condo-appraisal": "condo-building", "roof-damage-claim-appraisal": "metal-roof",
    "windstorm-claim-appraisal": "wind-tree", "snow-load-ice-dam-claims": "snow-collapse",
    "frozen-pipe-water-damage-appraisal": "water-ceiling", "fire-smoke-ash-claim-appraisal": "house-fire",
    "earthquake-endorsement-claims": "quake-damage", "remote-property-claim-appraisal": "remote-cabin",
    "carrier-estimate-review": "laptop-calculator", "neutral-umpire-services": "consultation-laptop",
}
POST_PHOTO = {p["slug"]: p["photo"] for p in POSTS}
TOOL_PHOTO = {t["slug"]: t["photo"] for t in TOOLS}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 2 3-2M9 21l3-2 3 2M3 9l2 3-2 3M21 9l-2 3 2 3"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "quake": '<path d="M2 12h4l2-6 3 12 3-9 2 3h6"/>',
    "plane": '<path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "roof": '<path d="M2 12L12 4l10 8M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-panel-representation": "scale", "home-insurance-claim-appraisal": "home", "commercial-hoa-condo-appraisal": "building",
    "roof-damage-claim-appraisal": "roof", "windstorm-claim-appraisal": "wind", "snow-load-ice-dam-claims": "snow",
    "frozen-pipe-water-damage-appraisal": "drop", "fire-smoke-ash-claim-appraisal": "flame", "earthquake-endorsement-claims": "quake",
    "remote-property-claim-appraisal": "plane", "carrier-estimate-review": "file", "neutral-umpire-services": "shield",
}


def mark(cls="mark"):
    """Brand mark: a gold peak with a snow cap over a ledger line, on a midnight tile."""
    return (f'<svg class="{cls}" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#0E1621"/>'
            '<path d="M7 35 19.5 14l6.2 10.3 3.6-5.6L41 35z" fill="#FFB612"/>'
            '<path d="M19.5 14l4.1 6.8-2.3-1.6-1.8 2.4-1.9-2.2-2.3 1.4z" fill="#fff"/>'
            '<rect x="7" y="38.5" width="34" height="3" rx="1.5" fill="#7CC4F2"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "AK", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-AK", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for disputed Alaska property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims throughout Alaska.",
        "areaServed": [{"@type": "State", "name": "Alaska"}] + [{"@type": "City", "name": c} for l in LOCATIONS for c in l["city"].split(" & ")],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Snow load damage", "Earthquake claims", "Remote construction costs"],
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
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All 12 services", SVC_BASE)),
        ("Communities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All communities", LOC_BASE)),
        ("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All tools", TOOL_BASE)),
        ("Learn", [("Appraisal process", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Claim guides", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        cols = " two" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "ic chev")}</button><ul class="sub{cols}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a class="top" href="{P_ABOUT}">About</a></li><li><a class="top" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc" aria-expanded="false" aria-controls="dr-{i}">{name}{ic("chev", "ic chev")}</button><ul class="acc-panel" id="dr-{i}">{li}</ul></li>'
    acc += f'<li><a class="solo" href="{P_ABOUT}">About</a></li><li><a class="solo" href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head" id="top"><div class="wrap head-in">
<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Alaska</b><span>Insurance Appraiser</span></span></a>
<nav class="nav" aria-label="Main"><ul class="nav-list">{menu}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark()}<span class="brand-t"><b>Alaska</b><span>Insurance Appraiser</span></span></a><button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav aria-label="Mobile"><ul class="drawer-list"><li><a class="solo" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap band-in"><p class="band-t">Disputed claim? Send the estimate and we’ll tell you what we see.</p><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Free claim review</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about"><a class="brand" href="/">{mark()}<span class="brand-t"><b>Alaska</b><span>Insurance Appraiser</span></span></a>
<p>Independent appraisal and estimating for property owners with disputed insurance claims, from Ketchikan to Utqiagvik.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")} {PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")} {EMAIL}</a></li><li>{ic("clock")} {HOURS}</li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Communities</h2><ul class="cols2">{loc}</ul></div>
<div><h2 class="foot-h">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{P_ABOUT}">About the practice</a></li><li><a href="{P_PROCESS}">Appraisal process</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Claim guides</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. {BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Information on this site is general; policy terms vary and results are never guaranteed.</p>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_CREDITS}">Photo credits</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call</a><a href="{P_CONTACT}">{ic("file")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    # The client's tag, used exactly as provided.
    return (f'<!-- Google Tag Manager -->\n<script async src="https://www.googletagmanager.com/gtm.js?id={GTM_ID}"></script>\n'
            "<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n</script>\n"
            "<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "FAQPage", "ItemList")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero", main_ref=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, nodes, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
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
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        if t in ("Service", "WebApplication"):
            n["provider"] = {"@id": DOMAIN + "/#business"}
        nodes.append(n)
    pimg = PHOTOS[photo]
    primary = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "contentUrl": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": ALT[photo]}
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY, "primaryImageOfPage": {"@id": canonical + "#primaryimage"},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    if main_ref:
        webpage["mainEntity"] = {"@id": main_ref}
    else:
        mains = [n["@id"] for t0 in MAIN_TYPES for n in nodes if n.get("@type") == t0]
        webpage["mainEntity"] = {"@id": mains[0] if mains else DOMAIN + "/#business"}
    noindex = robots.startswith("noindex")
    graph = [org_schema(), site_schema()] + ([] if noindex else [webpage, primary]) + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Alaska">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Alaska">
<meta name="geo.region" content="US-AK">
<meta name="geo.placename" content="Alaska">
<meta name="theme-color" content="#0E1621">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Space+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.className+=' js';</script>
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
    # Pages are dir/index.php: the host serves real files without running the root front controller,
    # so each page starts with the canonical-host guard (www/http 301, /index.php 301, off-domain noindex).
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
        assert "<?" not in content, path
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
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="ihero"><div class="ihero-text"><div class="ihero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></div><figure class="ihero-photo">{img(photo, lazy=False, sizes="(max-width:900px) 100vw, 55vw", alt="")}</figure></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box call"><h2 class="side-h">Talk it through</h2><p>Free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="side-phone" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold block" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="side"><div class="side-stick">{aside}</div></aside></div>'


def cta_strip(h="Not sure the number is right?", p="Send us the carrier’s estimate and your photos. We’ll review them and give you a straight answer."):
    return f"""<section class="cta-strip"><div class="wrap cta-in rv"><div><p class="cta-h">{e(h)}</p><p>{e(p)}</p></div><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def related(cards):
    return '<div class="rel-grid">' + "".join(f'<a class="rel" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in cards) + "</div>"


LOSSES = ["Wind", "Snow load / ice dam", "Frozen pipe / water", "Fire / smoke / wildfire", "Earthquake (with coverage)", "Roof damage", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", page="/", fid="f"):
    roles = ["Homeowner", "Condo owner", "Commercial owner", "Property manager / HOA", "Contractor", "Attorney", "Public adjuster", "Other"]
    places = [l["city"] for l in LOCATIONS] + ["Elsewhere in Alaska", "Off the road system"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<p class="lead-h">{e(heading)}</p><p class="lead-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="lead-grid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(places)}</select></div>
<div><label for="{fid}-amt">Approx. amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy page</a>.</span></label></div>
<div class="full"><button class="btn gold block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="quick" action="/api/contact.php" method="post" data-lead novalidate>
<p class="quick-h">{ic("file")} Free claim review</p>
<div class="quick-grid">
<div><label for="q-name">Name *</label><input id="q-name" name="name" autocomplete="name" required></div>
<div><label for="q-phone">Phone *</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="q-loss">Type of loss</label><select id="q-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="q-web">Website</label><input id="q-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<div class="quick-go"><button class="btn gold block" type="submit">Request review {ic("arrow")}</button></div>
</div>
<label class="check small"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{P_PRIV}">Privacy</a>.</span></label>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Southcentral & Mat-Su", "Anchorage · Eagle River · Wasilla · Palmer", ["Earthquake (with coverage)", "Downslope & Matanuska winds", "Snow load", "Wildfire"], "anchorage",
     "Most of the state’s population and most of its claims. The 2018 earthquake, Hillside and Matanuska windstorms and heavy-snow winters all show up here."),
    ("Interior", "Fairbanks · North Pole · Delta Junction", ["Forty-below freeze-ups", "Rain on snow", "Wildfire smoke", "Chimney fires"], "wildfire",
     "Extreme cold turns a heating failure into a whole-house water loss. Summers bring wildfire smoke across the Tanana Valley."),
    ("Southeast", "Juneau · Ketchikan · Sitka", ["Heavy rain", "Taku & Gulf winds", "Glacial outburst floods", "Landslides"], "juneau",
     "Steep, wet and barge-supplied. Water intrusion, wind and difficult access drive the cost of nearly every repair."),
    ("Kenai Peninsula & Kodiak", "Kenai · Soldotna · Homer · Kodiak", ["Wildfire", "Coastal wind", "Volcanic ash", "Earthquake (with coverage)"], "homer",
     "Beetle-killed spruce, coastal storms and Cook Inlet volcanoes. Island and end-of-road locations raise repair costs."),
    ("Western & Arctic", "Bethel · Nome · Utqiagvik · villages", ["Ex-typhoon storms", "Extreme cold", "Fire", "Remote logistics"], "storm-response",
     "Off the road system, freight and travel can rival the repair itself. Flood and erosion are usually excluded; wind, fire and interior water are not."),
]


def home():
    svc_cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="pcard-b"><span class="pcard-ic">{ic(SVC_ICON[s["slug"]])}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for s in SERVICES)
    regions = "".join(
        f'<article class="region rv"><div class="region-img">{img(ph, sizes="(max-width:800px) 100vw, 40vw", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-sub">{e(sub)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p></div></article>'
        for n, sub, perils, ph, t in REGIONS)
    tool_cards = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(t["photo"], sizes="(max-width:640px) 100vw, 300px", alt="")}<span class="tag">{e(t["kind"])}</span></span><span class="tcard-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>'
        for t in TOOLS)
    towns = "".join(
        f'<a class="town" href="{loc_path(l)}">{img(l["slug"], sizes="280px", alt="")}<span class="town-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>'
        for l in LOCATIONS)
    posts = "".join(
        f'<article class="post rv"><a class="post-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    steps = "".join(f'<li class="trail-step"><span class="dot">{i + 1}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(PROCESS_STEPS[2:7]))

    home_faqs = [
        ("What does an Alaska Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once any two of the three panel members sign. That is why the documentation going in matters so much."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster presents and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("Do you work outside Anchorage?", "Yes. We work statewide, including the Mat-Su, the Interior, Southeast, the Kenai Peninsula, Kodiak and communities off the road system. Remote inspections are planned around weather and access."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. Our fee is agreed in writing before work starts, and the first conversation is free."),
        ("Does Alaska have a FAIR plan?", "No. Alaska doesn’t operate a FAIR plan or a wind pool. Owners who can’t find standard coverage often use the surplus lines market. Appraisal clauses appear in most standard and surplus lines property forms."),
    ]

    body = f"""
<section class="hero">
<div class="hero-photo">{img("hero", lazy=False, alt="", extra=' data-parallax="0.25"')}</div>
<div class="wrap hero-in">
<p class="kicker">Independent claim appraisal · Statewide</p>
<h1>Alaska Insurance Appraiser for disputed and <em>underpaid</em> property claims</h1>
<p class="lede">When the insurer accepts your claim but the estimate won’t cover the repair, Alaska Insurance Appraiser builds an independent, line-by-line valuation and takes it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line light" href="#services">See services {ic("arrow")}</a></div>
</div>
<div class="wrap hero-form">{hero_form()}</div>
</section>

<section class="counts" aria-label="At a glance"><div class="wrap counts-in">
<div class="count"><b data-count="30">30</b><span>borough &amp; census-area equivalents covered</span></div>
<div class="count"><b data-count="12">12</b><span>appraisal &amp; estimating services</span></div>
<div class="count"><b data-count="7">7</b><span>free in-browser claim tools</span></div>
<div class="count"><b>2 of 3</b><span>signatures make an award binding</span></div>
</div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-copy rv">
<p class="kicker dark">Why owners call</p>
<h2>The gap between “covered” and “paid in full”</h2>
<p>Most disputed claims in Alaska aren’t denials. They’re estimates that leave things out: the insulation behind the wet drywall, the steep charge on a snow-country roof, the barge freight to Kodiak, the second course of ice and water shield. Alaska Insurance Appraiser exists for that gap.</p>
<p>As an Alaska Insurance Appraiser, we start from our own inspection and measurements, never from an edited copy of the carrier’s numbers. The goal is a valuation that holds up in front of an umpire, because that is what actually moves an award.</p>
<ul class="ticks"><li>{ic("check")}<span><b>Retained by you.</b> An Alaska Insurance Appraiser you appoint, independent of the carrier.</span></li><li>{ic("check")}<span><b>Priced for the place.</b> Freight, travel and seasonal access included where they apply.</span></li><li>{ic("check")}<span><b>Honest triage.</b> If you need an attorney or a supplement instead, we’ll say so.</span></li></ul>
</div>
<figure class="intro-photo rv">{img("roofer", sizes="(max-width:900px) 100vw, 46vw")}<figcaption>Every estimate starts with our own measurements.</figcaption></figure>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Services</p><h2>Twelve ways Alaska Insurance Appraiser works on a claim</h2><p>From a quick estimate review to full appraisal panel work and neutral umpire appointments, each service is built around one job: an accurate, defensible number for your loss.</p></div>
<div class="pgrid" data-stagger>{svc_cards}</div>
</div></section>

<section class="sec"><div class="wrap fit">
<div class="fit-col yes rv"><h2>When an Alaska Insurance Appraiser is the right call</h2><ul><li>{ic("check")}Coverage accepted, cost disputed</li><li>{ic("check")}Repair-versus-replace arguments</li><li>{ic("check")}Discontinued siding, metal panels or flooring</li><li>{ic("check")}Missing code items, steep charges or overhead and profit</li><li>{ic("check")}Freight and travel left out for remote properties</li></ul></div>
<div class="fit-col no rv"><h2>When you probably need someone else</h2><ul><li>{ic("x")}Outright denials based on an exclusion</li><li>{ic("x")}Claims-handling or bad-faith concerns</li><li>{ic("x")}Flood, surge or erosion with no flood policy</li><li>{ic("x")}A gap too small to justify fees</li><li>{ic("x")}A suit deadline that is close</li></ul></div>
</div></section>

<section class="sec night"><div class="wrap">
<div class="sec-head rv"><p class="kicker">How it works</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended disagreement into a defined process. Here is the path Alaska Insurance Appraiser follows once a demand is made.</p></div>
<ol class="trail" data-trail><span class="trail-line" aria-hidden="true"><i></i></span>{steps}</ol>
<p class="center"><a class="btn line light" href="{P_PROCESS}">Read the full eight-step guide {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker dark">One state, five claim climates</p><h2>How Alaska weather shows up in an estimate</h2><p>Forty-below freeze-ups in Fairbanks, Taku winds in Juneau, wildfire smoke in the Mat-Su and earthquakes under Anchorage. An Alaska Insurance Appraiser has to price each one differently.</p></div>
<div class="regions">{regions}</div>
</div></section>

<section class="sec tint"><div class="wrap gapsec">
<div class="rv"><p class="kicker dark">Quick gap check</p><h2>Is your gap worth an appraisal?</h2><p>Enter the two numbers you already have. If the difference is large, a conversation with an Alaska Insurance Appraiser makes sense. If it is small, a documented supplement request may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}appraisal-gap-fee-estimator/">gap and fee estimator</a> adds appraiser, umpire and travel costs for a realistic net figure.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Free &amp; private</p><h2>Seven free claim tools from Alaska Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser and nothing you type is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tool_cards}</div>
<p class="center"><a class="btn line" href="{TOOL_BASE}">Open the tools page {ic("arrow")}</a></p>
</div></section>

<section class="sec night"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Communities served</p><h2>Alaska Insurance Appraiser, from Ketchikan to Fairbanks</h2><p>We work in all 19 organized boroughs and across the Unorganized Borough. These are the communities where Alaska Insurance Appraiser handles claims most often.</p></div>
</div>
<div class="towns-scroll" tabindex="0" aria-label="Communities, scroll sideways"><div class="towns">{towns}</div></div>
<div class="wrap"><p class="center"><a class="btn line light" href="{LOC_BASE}">All communities {ic("arrow")}</a></p></div>
</section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Alaska Insurance Appraiser will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="who" data-stagger>
<div class="who-card hl rv"><p class="who-k">Alaska Insurance Appraiser</p><h3>Values the amount of loss</h3><ul><li><b>Best when:</b> coverage accepted, number disputed</li><li><b>Result:</b> binding award on the amount</li><li><b>Decides coverage:</b> no</li></ul></div>
<div class="who-card rv"><p class="who-k">Public adjuster</p><h3>Presents and negotiates the claim</h3><ul><li><b>Best when:</b> early, from first notice</li><li><b>Result:</b> negotiated settlement</li><li><b>Licensed by:</b> Alaska Division of Insurance</li></ul></div>
<div class="who-card rv"><p class="who-k">Attorney</p><h3>Handles legal disputes</h3><ul><li><b>Best when:</b> denials, bad faith, deadlines</li><li><b>Result:</b> settlement or judgment</li><li><b>Decides coverage:</b> argues it in court</li></ul></div>
</div>
</div></section>

<section class="sec tint"><div class="wrap faqsec">
<div class="rv"><p class="kicker dark">FAQ</p><h2>Questions people ask an Alaska Insurance Appraiser</h2><p>Straight answers about the process, the cost and when appraisal is the wrong move.</p><div class="btn-row"><a class="btn dark" href="{P_FAQ}">All FAQs {ic("arrow")}</a><a class="btn line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Claim guides</p><h2>Read before you invoke appraisal</h2><p>Practical guides from Alaska Insurance Appraiser on policy language, documentation and Alaska-specific costs.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p class="center"><a class="btn line" href="{POST_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

<section class="sec night" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to an Alaska Insurance Appraiser about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>{HOURS}</span></li><li>{ic("pin")}<span><small>Coverage</small>Statewide, including off the road system</span></li></ul></div>
<div class="rv">{lead_form(page="/", fid="c")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Alaska Insurance Appraiser: independent appraisal, estimate review and umpire services for disputed wind, snow, water, fire and quake claims.",
                        body, schema, photo="hero", main_ref=DOMAIN + "/#business", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [x for x in SERVICES if x is not s]
        i = SERVICES.index(s)
        rel = (rel[i:] + rel[:i])[:3]
        ph = SVC_PHOTO[s["slug"]]
        art = s["body"] + f'<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}<h2>Related services</h2>' + related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        aside = call_box() + list_box("All services", items, path) + list_box("Communities", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All communities", LOC_BASE)])
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(art, aside) + cta_strip()
        schema = [crumbs_schema(trail), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "areaServed": {"@type": "State", "name": "Alaska"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}, faq_schema(s["faqs"])]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span><span class="pcard-b"><span class="pcard-ic">{ic(SVC_ICON[s["slug"]])}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for s in SERVICES)
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Alaska Property Claims",
                     "Twelve services, one goal: a valuation of your loss that holds up. Start with an estimate review, bring us in after appraisal is demanded, or appoint us as a neutral umpire.", "roof-repair") + f"""
<section class="sec"><div class="wrap"><div class="pgrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faqsec"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know where the carrier’s estimate falls short and what that gap is worth. Many disputes close at that stage.</p><a class="btn dark" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle both residential and commercial claims?", "Yes: houses, condos, multifamily, retail, office, lodges, hangars and association properties."), ("Do you only handle storm claims?", "No. We work on wind, snow load, water, fire, earthquake (where covered) and other perils.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Alaska | 12 Services",
                             "Alaska insurance appraisal services: appraisal clause representation, estimate review, wind, snow load, water, fire, quake and umpire work.",
                             body, schema, photo="roof-repair"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Communities", LOC_BASE), (l["city"], path)]
        city = l["city"]
        ph = l["slug"]
        snap = f"""<div class="snap"><div><p class="snap-k">Borough</p><p>{e(l["county"])}</p></div><div><p class="snap-k">Region</p><p>{e(l["region"])}</p></div><div class="w"><p class="snap-k">Neighborhoods &amp; areas</p><p>{e(", ".join(l["hoods"]))}</p></div><div class="w"><p class="snap-k">Housing mix</p><p>{e(l["housing"][0].upper() + l["housing"][1:])}</p></div><div class="w"><p class="snap-k">Notable events</p><ul>{"".join(f"<li>{e(x)}</li>" for x in l["events"])}</ul></div><div class="w"><p class="snap-k">Local claim risks</p><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in l["perils"])}</ul></div></div>"""
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        art = snap + l["body"] + f"""<h2>Services available in {e(city)}</h2><p>Every {BRAND} service is available to property owners in {e(city)} and nearby, including:</p><ul>{svc_links}</ul>
<h2>Questions from {e(city)} property owners</h2>{faq_block(l["faqs"])}<h2>Nearby communities</h2>""" + related([("Community", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        aside = call_box() + list_box("Communities", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {city}, Alaska", e(l["lede"]), ph,
                         [("Borough", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, aside) + cta_strip(f"Disputed claim in {city}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        names = city.split(" & ")
        area = [{"@type": "City", "name": n, "containedInPlace": {"@type": "State", "name": "Alaska"}} for n in names]
        schema = [crumbs_schema(trail), {"@type": "Service", "name": f"Insurance appraisal in {city}, Alaska", "serviceType": "Insurance appraisal", "areaServed": area if len(area) > 1 else area[0], "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}, faq_schema(l["faqs"])]
        short = names[0] if len(city) > 16 else city
        title = f"Insurance Appraiser {short}, AK | Claim Appraisal"
        if len(title) > 56:
            title = f"Insurance Appraiser {short}, AK | Appraisal"
        desc = f"Insurance appraiser for {city}, {l['county']}: independent appraisal and estimate review for disputed wind, snow, water and fire claims."
        if len(desc) > 150:
            desc = f"Insurance appraiser for {city}: independent appraisal and estimate review for disputed wind, snow, water and fire claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Communities", LOC_BASE)]
    towns = "".join(f'<a class="lcard rv" href="{loc_path(l)}"><span class="lcard-img">{img(l["slug"], sizes="(max-width:640px) 100vw, 300px", alt="")}</span><span class="lcard-b"><h2>{e(l["city"])}</h2><p>{e(l["county"])} · {e(l["region"])}</p></span></a>' for l in LOCATIONS)
    regions = "".join(f'<article class="region rv"><div class="region-img">{img(ph, sizes="(max-width:800px) 100vw, 40vw", alt="")}</div><div class="region-b"><h3>{e(n)}</h3><p class="region-sub">{e(sub)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p></div></article>' for n, sub, perils, ph, t in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in Every Alaska Borough and Census Area",
                     "Alaska has no counties. It has 19 organized boroughs and a vast Unorganized Borough split into 11 census areas, 30 county-equivalents in all. We work in every one of them, including communities off the road system.", "anchorage") + f"""
<section class="sec"><div class="wrap"><div class="lgrid" data-stagger>{towns}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker dark">Regions</p><h2>How claims differ across Alaska</h2><p>The same policy language plays out very differently in a Fairbanks log home, a Juneau hillside house and a Mat-Su shop.</p></div><div class="regions">{regions}</div></div></section>
{cta_strip("Don’t see your community?", "We work statewide. Call and tell us where the property is, including fly-in and barge-served locations.")}"""
    write(LOC_BASE, document(LOC_BASE, "Alaska Communities We Serve | Insurance Appraisal",
                             "Insurance appraisal in all 30 Alaska borough and census-area equivalents, including Anchorage, Fairbanks, Juneau, the Mat-Su and Kodiak.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo="anchorage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Tools", TOOL_BASE), (t["name"], path)]
        others = [o for o in TOOLS if o is not t][:3]
        ph = t["photo"]
        art = t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>' + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap"><div class="rv-off">{t["markup"]}</div><p class="hint center">For planning only. Results depend on what you enter and on your policy, and are not a quote, an appraisal or legal advice.</p><noscript><p class="note">This calculator needs JavaScript. You can still call us at {PHONE} and we’ll run the numbers with you.</p></noscript></div></section>
""" + layout(art, call_box() + list_box("All claim tools", items, path)) + cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}, faq_schema(t["faqs"])]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Tools", TOOL_BASE)]
    cards = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(t["photo"], sizes="(max-width:640px) 100vw, 300px", alt="")}<span class="tag">{e(t["kind"])}</span></span><span class="tcard-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Alaska Property Owners",
                     "Seven calculators, planners and checklists built from appraisal work, including a roof snow load calculator. No sign-up, and nothing you enter is stored.", "laptop-calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faqsec"><div class="rv"><p class="kicker dark">Suggested order</p><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-timeline-planner/">timeline planner</a> so nothing lapses.</li><li>If snow was involved, record the load with the <a href="{TOOL_BASE}roof-snow-load-calculator/">snow load calculator</a>.</li><li>Check roof quantities with the <a href="{TOOL_BASE}roof-area-pitch-calculator/">roof area and pitch calculator</a>.</li><li>See what you are owed with the <a href="{TOOL_BASE}deductible-impact-calculator/">deductible</a> and <a href="{TOOL_BASE}depreciation-holdback-worksheet/">depreciation</a> tools.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-gap-fee-estimator/">gap and fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-file-checkup/">file checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Alaska",
                              "Free Alaska claim tools: appraisal cost, depreciation, roof square, snow load and percentage deductible calculators, plus a deadline planner.",
                              body, schema, photo="laptop-calculator"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("Appraisal process", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Claim guides", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    steps = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in PROCESS_STEPS)
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in Alaska, Step by Step",
                     "Eight stages from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", "clipboard-notes",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(PROCESS_BODY.replace("{steps}", steps), call_box() + list_box("Learn", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Alaska", "description": "The eight stages of a property insurance appraisal, from the disagreement to the signed award.", "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in Alaska | 8 Steps",
                         "The insurance appraisal process in Alaska step by step: the written demand, naming appraisers and an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="clipboard-notes"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    toc = '<nav class="toc" aria-label="FAQ topics"><p class="toc-h">Topics</p><ul>' + "".join(f'<li><a href="#t{i}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ)) + "</ul></nav>"
    groups = toc + "".join(f'<h2 id="t{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Alaska Insurance Appraisal FAQ, Grouped by Topic",
                     "Plain answers to the questions we hear most: the basics, costs and timing, Alaska-specific rules and how we work.", "consultation-laptop") + layout(groups, call_box() + list_box("Learn", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email and we’ll talk it through.")
    write(path, document(path, "Alaska Insurance Appraisal FAQ | Costs, Timing, Rules",
                         "Answers to common Alaska insurance appraisal questions: how it works, what it costs, how long it takes, earthquake and flood coverage and more.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="consultation-laptop"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    art = f'<div class="gfilter"><label for="gq">Search {len(GLOSSARY)} terms</label><input id="gq" type="search" placeholder="Try “holdback” or “snow load”" autocomplete="off"><p class="hint" data-gcount></p></div><div class="az">{az}</div><dl class="gloss">{dl}</dl><p class="hint" data-gnone hidden>No terms match that search.</p>'
    body = page_hero(trail, "Reference", "Insurance Claim Glossary: Alaska Edition",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, plus a few that are unique to Alaska, defined in plain English.", "calculator-documents", cta=False) + layout(art, call_box() + list_box("Learn", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More",
                         "Plain-English definitions of insurance claim terms: actual cash value, holdback, appraisal award, umpire, snow load, borough and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator-documents"), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim guides", POST_BASE), (p["title"], path)]
        others = [o for o in POSTS if o is not p][:3]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        art = f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>' + p["body"] + "<h2>Keep reading</h2>" + related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Guide · {p['read']} read", p["title"], e(p["summary"]), p["photo"], cta=False) + layout(art, call_box() + list_box("Learn", LEARN) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        artn = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{p['photo']}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), artn], og_type="article", photo=p["photo"]), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim guides", path)]
    cards = "".join(f'<article class="post rv"><a class="post-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides", "Alaska Property Claim Guides",
                     "Practical guides on policy language, earthquake and snow claims, remote repair costs and choosing the right help.", "house-winter", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Alaska Property Claim Guides | Appraisal Tips",
                         "Guides for Alaska property owners on appraisal clauses, earthquake and snow load claims, remote repair costs and who to call for help.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="house-winter"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    art = f"""
<figure class="lead-img">{img("consultation", sizes="(max-width:900px) 100vw, 720px")}<figcaption>Plain-English reporting: you should understand every line we price.</figcaption></figure>
<h2>Why we focus only on appraisal</h2>
<p>{BRAND} works on one question: the amount of loss. We built our process, our tools and our documentation standards around answering it well. That focus lets us act as your appointed appraiser, review an estimate before a dispute escalates, or serve as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Priced for the place.</strong> Freight, travel, seasonal access and winter conditions are real costs in Alaska, and we show them separately.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll tell you.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, lodge owners, churches, businesses, contractors, public adjusters and attorneys across Alaska. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes, and no honest appraiser can. We don’t publish testimonials or client results.</p>
<h2>Statewide, on purpose</h2>
<p>Alaska’s claims change with the landscape: forty-below freeze-ups in Fairbanks, Taku winds in Juneau, wildfire smoke in the Mat-Su, quake cracks in Anchorage and snow loads in Valdez. Working statewide means we price each one with that context in mind.</p>"""
    body = page_hero(trail, "About us", "About Alaska Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs to repair, wherever in Alaska the property happens to be.", "house-winter") + layout(art, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Communities", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", P_PROCESS)])) + cta_strip()
    write(path, document(path, "About Alaska Insurance Appraiser | Our Approach",
                         "Alaska Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="house-winter", main_ref=DOMAIN + "/#business"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact an Alaska Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation-laptop", cta=False) + f"""
<section class="sec night"><div class="wrap contact">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>{HOURS}</span></li><li>{ic("pin")}<span><small>Service area</small>All of Alaska, including off the road system</span></li></ul>
<h3>Helpful to have ready</h3><ul class="plain-list"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimates</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, fid="f")}</div></div></section>"""
    write(path, document(path, "Contact an Alaska Insurance Appraiser | (844) 537-1427",
                         "Get a free review of a disputed Alaska property claim. Call or text (844) 537-1427 or email info@alaskainsuranceappraiser.com.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation-laptop", main_ref=DOMAIN + "/#business"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · {e(v.get("source_name", ""))}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in sorted(PHOTOS.items()))
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy and Data", "Privacy Policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect the information you choose to share, such as your name, phone number, email address, property location and claim details. Our web host records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim</li><li>To provide services you ask for</li><li>To keep the site secure and working</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators, planners and checklists run in your browser. What you enter is not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data. If we add analytics, it will be described here.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you’ve shared by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us.",
                 "Privacy policy for Alaska Insurance Appraiser: what we collect through forms, calls and email, how we use it, and the choices you have."),
        P_TERMS: ("Website Use Terms", "Terms of Use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is general information about insurance appraisal and property claims in Alaska.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That starts only with a signed written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ and laws change. Consult a licensed Alaska attorney for legal questions.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates from the figures you enter. Example figures on this site are illustrative. None of it is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses on our <a href="{P_CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Alaska.</p>""", "The terms that apply when you use this website and its tools.",
                 "Terms of use for the Alaska Insurance Appraiser website and its free claim tools, including limits on advice and liability."),
        P_DISC: ("Appraisal Disclaimer", "Disclaimer", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, don’t give legal advice and don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures are illustrative and are not results for any client. We don’t publish testimonials or claim outcomes. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is close, consult an Alaska attorney promptly.</p>
<h2>Legal references</h2><p>References to the Alaska insurance code, unfair claim settlement practices or bad-faith claims are general descriptions, not legal analysis. Verify current law with an attorney and with the Alaska Division of Insurance.</p>
<h2>Weather and events</h2><p>References to earthquakes, storms, fires and floods are for context and drawn from public sources. Details may be simplified.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website.",
                 "Disclaimer for Alaska Insurance Appraiser: general information only, not legal advice, no guaranteed results and illustrative example figures."),
        P_CREDITS: ("Photo Credits", "Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit sources here with thanks. Photos are illustrative and don’t show our clients’ properties. All were found through the Openverse search API.</p>
<div class="tbl"><table><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""", "Sources and licenses for the photographs used on this site.",
                 "Photo credits for Alaska Insurance Appraiser: every image is CC0 or public domain, listed with its title, creator, license and source link."),
    }
    for path, (h1, crumb, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (crumb, path)]
        body = page_hero(trail, "Site information", h1, lede, "office-building", cta=False) + layout(content, call_box())
        write(path, document(path, f"{h1} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="office-building"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Communities", [("All communities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy", P_PRIV), ("Terms", P_TERMS), ("Disclaimer", P_DISC), ("Photo credits", P_CREDITS)]),
    ]
    cols = "".join(f'<div class="map-col"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "office-building", cta=False) + f'<section class="sec"><div class="wrap map-grid">{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of every page on {BRAND}: services, Alaska communities, free claim tools, guides and site information.", body, [crumbs_schema(trail)], photo="office-building"), 0.3)

    body = f"""<section class="ihero err"><div class="ihero-text"><div class="ihero-in"><p class="kicker">Error 404</p><h1>This page is snowed in</h1><p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn gold" href="/">Home</a><a class="btn line light" href="{SVC_BASE}">Services</a><a class="btn line light" href="{TOOL_BASE}">Free tools</a><a class="btn line light" href="{P_CONTACT}">Contact</a></div></div></div><figure class="ihero-photo">{img("snowy-roof", lazy=False, alt="")}</figure></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on Alaska Insurance Appraiser. Try the home page, services, free tools or contact page.", body, robots="noindex,follow", photo="snowy-roof"), sitemap=False)


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(xml) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT, "index.php"), "w").write(INDEX_PHP)
    open(os.path.join(OUT, "_guard.php"), "w").write(GUARD_PHP)


GUARD_PHP = r"""<?php
// Alaska Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$aia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$aia_real  = 'alaskainsuranceappraiser.com';
$aia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$aia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://alaskainsuranceappraiser.com - only on the real domain.
if ($aia_host === 'www.' . $aia_real || ($aia_host === $aia_real && $aia_proto === 'http')) {
    header('Location: https://' . $aia_real . $aia_uri, true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($aia_uri, '?'), $aia_m)) {
    $aia_q = strpos($aia_uri, '?') !== false ? substr($aia_uri, strpos($aia_uri, '?')) : '';
    header('Location: ' . $aia_m[1] . $aia_q, true, 301);
    exit;
}
// Keep preview and other hosts out of search results.
if ($aia_host !== $aia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Alaska Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (running a directory's index.php)
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
