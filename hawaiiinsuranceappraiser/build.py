#!/usr/bin/env python3
"""Static site generator for hawaiiinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import re
import os
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from services import SERVICES, ICONS as SVC_ICON  # noqa: E402
from locations import LOCATIONS  # noqa: E402
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))

BRAND = "Hawaii Insurance Appraiser"
HOST = "hawaiiinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
HOURS = "Mon–Fri 7am–5pm HST"
TODAY = date.today().isoformat()
VER = "20261117b"
FAV = "1"
# Google Tag Manager container, e.g. "GTM-XXXXXXX". Empty = no GTM snippet is output.
GTM_ID = ""
# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraisal-specialties/"
LOC_BASE = "/island-communities/"
TOOL_BASE = "/island-claim-tools/"
POST_BASE = "/hawaii-claim-guides/"
P_PROCESS = "/appraisal-process-map/"
P_FAQ = "/appraisal-questions-by-topic/"
P_GLOSS = "/property-claim-glossary/"
P_ABOUT = "/about-hawaii-appraiser/"
P_CONTACT = "/contact-hawaii-appraiser/"
P_PRIVACY = "/privacy-and-your-data/"
P_TERMS = "/terms-of-site-use/"
P_DISC = "/appraisal-and-legal-disclaimer/"
P_MAP = "/island-site-map/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
FALLBACK = ["hero-island-homes", "oahu-suburb", "storm-surf", "wind-palms", "lanai-interior", "consultation"]


def pk(key):
    """Return `key` if that photo exists, else the first available fallback (and say so)."""
    if key in PHOTOS:
        return key
    for k in FALLBACK + list(PHOTOS):
        if k in PHOTOS:
            print(f"  note: photo '{key}' missing, using '{k}'")
            return k
    raise SystemExit("no photos in src/photos.json")


def alt_of(key):
    return PHOTOS[pk(key)].get("alt") or PHOTOS[pk(key)].get("title", "")


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    key = pk(key)
    p = PHOTOS[key]
    a = e(alt if alt is not None else alt_of(key))
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-representation": "consultation", "homeowner-claim-appraisal": "oahu-suburb",
    "condo-aoao-commercial-appraisal": "condo-towers", "roof-hail-claim-appraisal": "metal-roof",
    "kona-storm-high-wind-claims": "fallen-tree", "hurricane-claim-appraisal": "hurricane-satellite",
    "water-damage-claim-appraisal": "flood-street", "fire-smoke-claim-appraisal": "fire-damage",
    "wildfire-claim-appraisal": "wildfire", "volcanic-ashfall-lava-claims": "lava-flow",
    "carrier-estimate-review": "laptop-calculator", "umpire-services": "calculator-documents",
}
LOC_PHOTO = {
    "honolulu-oahu": "honolulu-skyline", "kailua-kaneohe-oahu": "windward-oahu", "pearl-city-aiea-oahu": "oahu-suburb",
    "kapolei-ewa-beach-oahu": "wind-palms", "mililani-wahiawa-oahu": "north-shore", "hilo-big-island": "hilo-bay",
    "kailua-kona-big-island": "kona-coast", "puna-pahoa-big-island": "lava-zone-homes", "kahului-wailuku-maui": "maui-valley",
    "kihei-wailea-maui": "kihei-coast", "lahaina-west-maui": "lahaina-harbor", "lihue-kauai": "kauai-coast",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-documents", "rcv-acv-holdback-calculator": "laptop-calculator",
    "roof-pitch-squares-estimator": "roof-damage", "hurricane-deductible-calculator": "storm-surf",
    "claim-timeline-builder": "inspection-clipboard", "appraisal-readiness-check": "consultation",
    "condo-deductible-share-calculator": "condo-towers",
}
POST_PHOTO = {
    "hurricane-deductibles-in-hawaii": "hurricane-satellite", "condo-master-policy-vs-ho6": "condo-towers",
    "documenting-wildfire-smoke-damage": "wildfire", "salt-air-corrosion-vs-storm-damage": "metal-roof",
    "general-excise-tax-and-freight-in-estimates": "roof-shingles",
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
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "fire2": '<path d="M12 2c1 3 4 4.5 4 8a4 4 0 0 1-8 0c0-1.5.6-2.6 1.4-3.6"/><path d="M3 22h18M5 22c1-3 2.5-4.5 4-5M19 22c-1-3-2.5-4.5-4-5"/>',
    "volcano": '<path d="M2 21h20L15 9H9z"/><path d="M9 9l1.5 3 1.5-2 1.5 2L15 9M10 2l1 3M14 2l-1 3M7 4l2 2.5M17 4l-2 2.5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I.get(name, _I["doc"])}</svg>'


def mark(uid="m", size=44):
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#7d4fb5"/><stop offset="1" stop-color="#2a1442"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="12" fill="url(#{uid})"/>'
            '<path d="M10.5 24.5L24 12.5l13.5 12" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M17 24v6.5M31 24v6.5" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
            '<path d="M9.5 36.5c3.2-2.8 6.3-2.8 9.5 0s6.3 2.8 9.5 0 6.3-2.8 9.5 0" fill="none" stroke="#f2b544" stroke-width="3.4" stroke-linecap="round"/></svg>')


def brand_link(uid, cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark(uid)}<span class="bt"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "HI", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-HI", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid island property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims on Oahu, Hawaii Island, Maui, Kauai, Molokai and Lanai.",
        "areaServed": [{"@type": "State", "name": "Hawaii"}] + [{"@type": "City", "name": l["schema_city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hurricane deductibles", "Condominium master policies", "Wildfire claims"],
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


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Specialties", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal specialties", SVC_BASE), True),
        ("Islands", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All island communities", LOC_BASE), True),
        ("Claim Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Resources", [("Appraisal process map", P_PROCESS), ("Questions by topic", P_FAQ), ("Claim glossary", P_GLOSS), ("Hawaii claim guides", POST_BASE)], None, False),
    ]


def header():
    menu = ""
    for i, (name, links, allk, cols) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand_link("mh")}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link("md")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{P_CONTACT}">Send claim details</a><small>{HOURS} · All islands</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>A claim that doesn’t add up deserves a second set of eyes.</h2><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line-light" href="{P_CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand_link("mf", "brand brand-foot")}
<p>Independent appraisal and estimating for property owners with disputed insurance claims — Oahu, Hawaii Island, Maui, Kauai, Molokai and Lanai.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{HOURS}</li></ul></div>
<div><h3>Specialties</h3><ul>{svc}<li><a href="{SVC_BASE}">All specialties</a></li></ul></div>
<div><h3>Islands</h3><ul>{loc}<li><a href="{LOC_BASE}">All communities</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Company</h3><ul><li><a href="{P_ABOUT}">About</a></li><li><a href="{P_PROCESS}">Process map</a></li><li><a href="{P_FAQ}">Questions</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Claim guides</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-base"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general and educational; policy terms vary, and results are never guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></div>"""


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


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, page_type="WebPage"):
    canonical = DOMAIN + path
    extra_nodes, crumb_id = [], None
    for n in (schema or []):
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": canonical + "#webpage"}
        if t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    img_key = pk(preload or "hero-island-homes")
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{img_key}.webp" imagesrcset="/assets/img/photos/{img_key}-640.webp 640w, /assets/img/photos/{img_key}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className="js"</script>
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across the islands">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across the islands">
<meta name="geo.region" content="US-HI">
<meta name="geo.placename" content="Hawaii">
<meta name="theme-color" content="#6B3FA0">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Kumbh+Sans:wght@400;500;600;700&display=swap">
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
    """/ -> home.html, /404.html -> 404.html, every other page -> dir/index.php behind the canonical-host guard.
    The host serves real files without running the root front controller, so each page must guard itself."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
        assert "<?" not in content, f"PHP tag in page HTML for {path}"
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
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.1"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn sun" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def layout(article, aside):
    return f'<div class="wrap layout"><article class="prose">{article}</article><aside class="aside">{aside}</aside></div>'


def related(cards):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in cards) + "</div>"


def cta_band(h="Not sure the settlement is right?", p="Send us the carrier’s estimate. We’ll review it and tell you what we see — no obligation."):
    return f"""<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line-light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


LOSSES = ["Hurricane / tropical storm", "Kona storm / high wind", "Roof leak / hail", "Water / plumbing", "Fire / smoke", "Wildfire", "Volcanic / ash / lava", "Condo / AOAO building loss", "Other"]
ISLANDS = ["Oahu", "Hawaii Island", "Maui", "Kauai", "Molokai", "Lanai"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hid="f"):
    roles = ["Homeowner", "Condo owner", "AOAO board / property manager", "Business owner", "Contractor", "Attorney", "Public adjuster", "Other"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Island</label><select id="{hid}-city" name="city">{_opt(ISLANDS)}</select></div>
<div><label for="{hid}-amt">Approx. amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{P_PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn wide" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Start a free claim check</h2><p class="sub">Three details and we’ll call you back, usually within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="r2"><div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="h-isl">Island</label><select id="h-isl" name="city">{_opt(ISLANDS)}</select></div></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{P_PRIVACY}">Privacy policy</a>.</span></label>
<button class="btn sun wide" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="fine">{ic("shield")}No obligation. Nothing is shared with your insurer.</p>
</form>"""


# ---------------------------------------------------------------- home
ISLAND_TABS = [
    ("oahu", "Oahu", "Honolulu County", "honolulu-skyline",
     ["Condo water losses", "Kona-storm wind", "Flash flooding", "Brush fires leeward"],
     "Most of the state’s people — and most of its high-rise condos — live on Oahu. Water losses that travel between units, roof damage from Kona-storm winds and flash flooding on the windward side make up a large share of disputed files, alongside leeward brush fires near Waianae and Makakilo.",
     "Honolulu, Kailua, Kaneohe, Pearl City, Aiea, Kapolei, Ewa Beach, Mililani, Wahiawa"),
    ("big-island", "Hawaii Island", "Hawaii County", "hilo-bay",
     ["Lava & vog", "Extreme rainfall", "Earthquake questions", "Catchment & roofs"],
     "The Big Island packs rain forest, ranchland and active volcanoes into one county. Hurricane Lane’s rainfall in 2018 hit the Hilo side hard the same year Kilauea’s eruption took homes in lower Puna, and vog keeps metal roofs and fixtures on the Kona side under constant attack.",
     "Hilo, Kailua-Kona, Pahoa, Waimea, Volcano, Honokaa, Kau"),
    ("maui", "Maui", "Maui County", "maui-valley",
     ["Wildfire", "Downslope winds", "Smoke & ash", "Rebuild costs"],
     "Since August 2023, wildfire has defined Maui claims: total losses in Lahaina, partial losses and smoke in Upcountry, and long arguments about rebuilding costs as labor and materials stretch thin. Kona storms and trade-wind gusts add roof and water claims across Central and South Maui.",
     "Kahului, Wailuku, Kihei, Wailea, Lahaina, Napili, Kula, Pukalani, Makawao"),
    ("kauai", "Kauai", "Kauai County", "kauai-coast",
     ["Hurricane history", "Record flooding", "Wind-driven rain", "Older housing"],
     "Kauai carries the memory of Iwa in 1982 and Iniki in 1992, and the 2018 north shore floods showed how fast rainfall can overwhelm roads and homes. Hurricane deductibles, wind-driven rain and the cost of shipping materials to the Garden Isle shape many disputes.",
     "Lihue, Kapaa, Wailua, Koloa, Poipu, Princeville, Hanalei, Waimea"),
    ("molokai-lanai", "Molokai & Lanai", "Maui County · Kalawao", "storm-surf",
     ["Travel logistics", "Limited contractors", "Wind & salt air", "Older homes"],
     "Small communities mean few local contractors and long lead times. Estimates for Molokai and Lanai need realistic freight, barge schedules and travel for crews — items carrier estimates sometimes price as if the home were in town on Oahu.",
     "Kaunakakai, Maunaloa, Kalaupapa, Lanai City"),
]

EVENTS = [
    ("1959", "Hurricane Dot", "A direct strike on Kauai, years before most current policy forms existed."),
    ("1982", "Hurricane Iwa", "Late-season hurricane that battered Kauai and leeward Oahu with wind and surf."),
    ("1992", "Hurricane Iniki", "The most destructive hurricane in island history; it reshaped how hurricane coverage is sold here."),
    ("2018", "Kauai & East Oahu floods", "Kauai’s north shore set a U.S. 24-hour rainfall record during the April storms."),
    ("2018", "Kilauea eruption", "Lava from the lower East Rift Zone covered neighborhoods in Puna, including Leilani Estates."),
    ("2018", "Hurricane Lane", "Extreme rainfall on the Hilo side plus wind-driven fires on Maui and Oahu."),
    ("2023", "Maui wildfires", "Fires in Lahaina and Upcountry produced total losses, smoke claims and long rebuild disputes."),
]


def home():
    steps = [
        ("Free claim check", "We read the policy, the carrier’s estimate and your photos, then say plainly whether appraisal fits."),
        ("Independent scope", "Our own inspection, measurements and line-item estimate priced for your island — freight and GET included."),
        ("Written demand", "Appraisal is invoked in writing and you name Hawaii Insurance Appraiser as your appraiser."),
        ("Panel work", "We negotiate line by line with the carrier’s appraiser; most disputes narrow here."),
        ("Signed award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="rv"><span class="n">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    def scard(i, s):
        return (f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}</span>'
                f'<span class="sc-b"><span class="num">{i + 1:02d}</span><span class="ic-c">{ic(SVC_ICON.get(s["slug"], "doc"))}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>')
    cards = "".join(scard(i, s) for i, s in enumerate(SERVICES))

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="pan-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{e(n)}</b><small>{e(sub)}</small></button>'
        for i, (k, n, sub, *_r) in enumerate(ISLAND_TABS))
    panels = "".join(
        f'<div class="isle-panel" role="tabpanel" id="pan-{k}" aria-labelledby="tab-{k}">{img(ph, sizes="(max-width:900px) 100vw, 760px", alt="")}<div class="isle-copy"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(txt)}</p><p class="cities"><b>Communities:</b> {e(cities)}</p></div></div>'
        for i, (k, n, sub, ph, perils, txt, cities) in enumerate(ISLAND_TABS))

    events = "".join(f'<li class="rv"><span class="yr">{y}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for y, n, t in EVENTS)
    tools = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}<span class="kind">{t["kind"]}</span></span><span class="tc-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open the tool {ic("arrow")}</span></span></a>' for t in TOOLS[:6])
    comms = "".join(f'<a class="ccard rv" href="{loc_path(l)}"><span class="ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, 25vw", alt="")}</span><span class="cc-b"><small>{e(l["island"])}</small><b>{e(l["city"])}</b></span></a>' for l in LOCATIONS)
    posts = "".join(f'<article class="pcard rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="pc-b"><span class="meta">{e(p["read"])} read</span><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        ("What does a Hawaii Insurance Appraiser do?", "When you and your insurer agree a loss is covered but disagree on the cost, an appraiser values the damage independently. As your appointed appraiser we inspect, build a line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("Do you work on neighbor islands?", "Yes. We take claims on Oahu, Hawaii Island, Maui, Kauai, Molokai and Lanai, and we’re upfront about any travel costs before work begins."),
        ("Can appraisal help with a condo or AOAO claim?", "Often, yes. Association master policies usually contain an appraisal clause, and the amount of a building loss affects every owner’s deductible assessment. Unit owners may also have a separate HO-6 dispute."),
        ("What if my claim was denied?", "Appraisal sets the amount of a covered loss; it doesn’t decide coverage. For a denial, talk to a Hawaii attorney first. We’ll tell you on the first call if your situation needs one."),
        ("How much does appraisal cost?", "Each side pays its own appraiser and usually half of the umpire. Our fee is put in writing before any work starts, and the first conversation is free."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-island-homes", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="tag">Independent appraisal · Oahu to Kauai</p>
<h1>Hawaii Insurance Appraiser <em>for claims that came up short</em></h1>
<p class="lede">Your insurer agreed the damage is covered, but the payment won’t rebuild it. Hawaii Insurance Appraiser prices the loss line by line — island freight, general excise tax and local labor included — and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#specialties">See our specialties {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Homes, condos &amp; commercial</li><li>{ic("check")}Every island</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="figs" aria-label="At a glance"><div class="wrap figs-in">
<div class="fig rv"><b data-count="5">5</b><span>Counties served, from Kauai to Hawaii Island</span></div>
<div class="fig rv"><b data-count="12">12</b><span>Appraisal and estimating specialties</span></div>
<div class="fig rv"><b data-count="7">7</b><span>Free claim tools that run in your browser</span></div>
<div class="fig rv"><b>2 of 3</b><span>Panel signatures that make an award binding</span></div>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<figure class="intro-ph rv">{img("consultation", sizes="(max-width:900px) 100vw, 520px")}<figcaption>Every number in our estimate is one we can explain at the table.</figcaption></figure>
<div class="rv">
<p class="kicker">The short version</p>
<h2>Covered is not the same as paid in full</h2>
<p>Most underpaid island claims aren’t denials. They’re estimates with a missing roof plane, a condo ceiling below that nobody opened, freight priced like the mainland or general excise tax left off the bottom line. A Hawaii Insurance Appraiser exists for the gap between “we’ll cover it” and a check that actually rebuilds.</p>
<p>When either side invokes the appraisal clause, you name an appraiser, the insurer names one, and the two choose an umpire. Hawaii Insurance Appraiser can be the appraiser you name — or review the numbers first so you know whether a demand is worth making.</p>
<ul class="points">
<li>{ic("check")}<div><b>We scope from scratch.</b> Our own inspection and measurements, never an edited copy of the carrier’s file.</div></li>
<li>{ic("check")}<div><b>We price for the island you’re on.</b> Barge freight, crew travel and county GET belong in a real estimate.</div></li>
<li>{ic("check")}<div><b>We say no when appraisal won’t help.</b> Denials, bad-faith questions and tight suit deadlines belong with an attorney.</div></li>
</ul>
<a class="btn" href="{P_ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec tint" id="specialties"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Specialties</p><h2>Twelve specialties, one question: what does the loss really cost?</h2><p>Hawaii Insurance Appraiser handles hurricane, Kona-storm, wildfire, volcanic and everyday water and fire claims — for single-family homes, condominium associations and commercial buildings.</p></div>
<div class="scards" data-stagger>{cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Island by island</p><h2>Each island files a different kind of claim</h2><p>A Hawaii Insurance Appraiser has to know how vog shows up on a Kona metal roof, how a stack-pipe leak travels through a Waikiki tower and what it costs to rebuild on Molokai.</p></div>
<div class="isles rv" data-tabs><div class="isle-tabs" role="tablist" aria-label="Islands">{tabs}</div><div class="isle-panels">{panels}</div></div>
</div></section>

<section class="sec deep" id="gap-check"><div class="wrap split">
<div class="rv"><p class="kicker light">Two-number gap check</p><h2>Two numbers tell you a lot</h2><p>Type in the carrier’s estimate and your contractor’s. A large gap is worth a conversation with a Hawaii Insurance Appraiser; a small one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser fees, inter-island travel and the umpire share so you can see a realistic net.</p><a class="btn sun" href="{TOOL_BASE}">Browse all seven tools {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">How it works</p><h2>From stalled claim to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. This is how Hawaii Insurance Appraiser moves a file from first call to award.</p></div>
<ol class="steps" data-stagger>{proc}</ol>
<p class="center"><a class="link" href="{P_PROCESS}">Walk through the full appraisal process map</a></p>
</div></section>

<section class="sec record"><div class="wrap">
<div class="sec-head left rv"><p class="kicker light">The record</p><h2>Storms, floods, lava and fire behind island policies</h2><p>Hurricane deductibles, lava-zone coverage and condo master-policy terms all trace back to events like these. A Hawaii Insurance Appraiser reads every estimate with this history in mind.</p></div>
<ol class="events" data-stagger>{events}</ol>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Work the numbers yourself first</h2><p>Seven calculators and planners built by Hawaii Insurance Appraiser from real appraisal work. Nothing you type is stored or sent anywhere.</p></div>
<div class="tcards" data-stagger>{tools}</div>
<p class="center"><a class="btn line" href="{TOOL_BASE}">See all claim tools, including the condo deductible calculator {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Where we work</p><h2>Communities we visit most</h2><p>Hawaii Insurance Appraiser takes claims in all five counties. These pages cover the places our files come from most often, with local housing and storm history.</p></div>
<div class="ccards" data-stagger>{comms}</div>
<p class="center"><a class="link" href="{LOC_BASE}">Explore every island community</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Honest triage</p><h2>When appraisal fits — and when to call someone else</h2><p>Appraisal is a precise tool. Hawaii Insurance Appraiser will point you elsewhere when another route serves you better.</p></div>
<div class="fit" data-stagger>
<div class="fit-yes rv"><h3>{ic("check")}Appraisal usually fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair-versus-replace arguments on roofs and finishes</li><li>Matching metal panels, tile or flooring that can’t be sourced</li><li>Freight, GET, code upgrades or overhead and profit left out</li><li>Condo building losses where the master-policy number drives assessments</li></ul></div>
<div class="fit-no rv"><h3>{ic("x")}Look elsewhere first</h3><ul><li>A full denial of coverage — talk to a Hawaii attorney</li><li>Bad-faith or claim-handling complaints — attorney or the Insurance Division</li><li>A suit-limitation date that is close</li><li>A gap too small to justify appraisal costs</li><li>Wanting someone to manage the whole claim — consider a licensed public adjuster</li></ul></div>
</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker">Questions</p><h2>Questions island owners ask first</h2><p>Straight answers from Hawaii Insurance Appraiser about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn" href="{P_FAQ}">Questions by topic {ic("arrow")}</a><a class="btn line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Island claim guides worth reading</h2><p>Practical reading on hurricane deductibles, condo master policies, wildfire smoke, salt-air corrosion and island pricing.</p></div>
<div class="pcards" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All Hawaii claim guides</a></p>
</div></section>

<section class="pcta">{img("storm-surf", "bg", alt="", extra=' data-parallax="0.2"')}<div class="wrap pcta-in rv"><p class="kicker light">Before you sign a release</p><h2>Check the math while you still can</h2><p>A short review now can keep you from accepting a settlement that won’t cover the rebuild.</p><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec deep" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker light">Start here</p><h2>Talk with a Hawaii Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>{HOURS}</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All islands · all five counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hid="hf")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Hawaii Insurance Appraiser offers independent appraisal and estimate review for underpaid hurricane, wildfire, water and condo claims.",
                        body, [faq_schema(home_faqs)], preload="hero-island-homes"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Specialties", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[::2]]
        art = s["body"] + f'<h2>Common questions</h2>{faq_block(s["faqs"])}<h2>Related specialties</h2>' + related([("Specialty", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])
        body = page_hero(trail, "Appraisal specialty", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(art, call_box() + list_box("All specialties", items, path) + list_box("Island communities", locs + [("All communities", LOC_BASE)])) + cta_band()
        svc = {"@type": "Service", "name": s["name"], "serviceType": s["keyword"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "State", "name": "Hawaii"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{pk(ph)}.webp"}
        write(path, document(path, s["title"], s["desc"], body, [crumbs_schema(trail), svc, faq_schema(s["faqs"])], preload=ph), 0.8)

    trail = [("Home", "/"), ("Specialties", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, 260px", alt="")}</span><span class="ib"><small>Specialty {i + 1:02d}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across the Islands",
                     "Every Hawaii Insurance Appraiser specialty is built around one deliverable: an accurate, defensible valuation of your loss — from a single estimate review to full panel representation or neutral umpire work.", "inspection-clipboard") + f"""
<section class="sec"><div class="wrap"><div class="ilist" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and some disputes close at that stage with a documented supplement.</p><a class="btn" href="{SVC_BASE}carrier-estimate-review/">About carrier estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle condo associations and commercial buildings?", "Yes — single-family homes, condos and AOAOs, townhouse communities, retail, office, hospitality and mixed-use buildings."), ("Which perils do you work on?", "Hurricane, Kona-storm wind, roof leaks and rare hail, water, fire and smoke, wildfire and volcanic or ash-related losses, among others.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Hawaii | 12 Specialties",
                             "Insurance appraisal services in Hawaii: appraisal clause work, estimate review, umpire services and hurricane, wildfire and condo claims.",
                             body, [crumbs_schema(trail), item_list(items)], preload="inspection-clipboard", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Island communities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        hoods = "".join(f"<li>{e(n)}</li>" for n in l["neighborhoods"])
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        art = f"""<div class="local"><div><b class="h">Local claim risks</b><ul class="chips">{chips}</ul></div><div><b class="h">Neighborhoods we cover</b><ul class="chips soft">{hoods}</ul></div><p><b>Housing:</b> {e(l["housing"])}</p><p><b>History:</b> {e(l["storms"])}</p></div>
{l["body"]}
<h2>Specialties available in {e(l["city"])}</h2><p>Every {BRAND} specialty is available to owners and associations in {e(l["city"])}, including:</p><ul class="cols2">{svc_links}</ul>
<h2>Questions from {e(l["city"])} owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2>""" + related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"] if n in LOC_BY])
        body = page_hero(trail, f'{l["island"]} · {l["region"]}', l["h1"], e(l["lede"]), ph,
                         [("County", l["county"]), ("Island", l["island"]), ("Service", "On-site inspections")]) + layout(art, call_box() + list_box("Island communities", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you honestly what we see.")
        svc = {"@type": "Service", "name": f"Insurance appraisal in {l['city']}", "serviceType": l["keyword"], "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "City", "name": l["schema_city"], "containedInPlace": {"@type": "State", "name": "Hawaii"}}, "url": DOMAIN + path}
        write(path, document(path, l["title"], l["desc"], body, [crumbs_schema(trail), svc, faq_schema(l["faqs"])], preload=ph), 0.8)

    trail = [("Home", "/"), ("Island communities", LOC_BASE)]
    comms = "".join(f'<a class="ccard rv" href="{loc_path(l)}"><span class="ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, 25vw", alt="")}</span><span class="cc-b"><small>{e(l["island"])} · {e(l["county"])}</small><b>{e(l["city"])}</b></span></a>' for l in LOCATIONS)
    isl = "".join(f'<div class="icard rv"><span class="ph">{img(ph, sizes="(max-width:640px) 100vw, 260px", alt="")}</span><span class="ib"><small>{e(sub)}</small><h2>{e(n)}</h2><p>{e(t)}</p><p class="muted">{e(c)}</p></span></div>' for k, n, sub, ph, _p, t, c in ISLAND_TABS)
    body = page_hero(trail, "All five counties", "Insurance Appraisal on Every Hawaiian Island",
                     "Hawaii Insurance Appraiser works statewide — Oahu, Hawaii Island, Maui, Kauai, Molokai and Lanai. These pages cover the communities where our claim files come from most often.", "honolulu-skyline") + f"""
<section class="sec"><div class="wrap"><div class="ccards" data-stagger>{comms}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">By island</p><h2>How claims differ from island to island</h2><p>The same policy language plays out differently in a Waikiki tower, a Puna catchment home and a Kula ranch house.</p></div><div class="ilist" data-stagger>{isl}</div></div></section>
{cta_band("Don’t see your community?", "We cover every island and all five counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraiser Locations in Hawaii | All Islands",
                             "Insurance appraiser locations across Hawaii, from Honolulu and Kailua to Hilo, Kona, Puna, Kahului, Kihei, Lahaina and Lihue.",
                             body, [crumbs_schema(trail), item_list(items)], preload="honolulu-skyline", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + f'<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>' + related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms; they are not a quote, an appraisal or legal advice. Default figures are illustrative.</p></div></section>
""" + layout(art, call_box() + list_box("All claim tools", items, path)) + cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        app = {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
               "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}
        write(path, document(path, t["title"], t["desc"], body, [crumbs_schema(trail), app, faq_schema(t["faqs"])], preload=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    cards = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}<span class="kind">{t["kind"]}</span></span><span class="tc-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open the tool {ic("arrow")}</span></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Island Owners",
                     "Seven calculators and planners from Hawaii Insurance Appraiser. Use them to understand your claim, check the carrier’s math and plan next steps — no sign-up, nothing stored.", "laptop-calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="olist"><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a> so no deadline slips.</li><li>Check roof measurements with the <a href="{TOOL_BASE}roof-pitch-squares-estimator/">roof pitch &amp; squares estimator</a>.</li><li>See what you’d actually receive with the <a href="{TOOL_BASE}hurricane-deductible-calculator/">hurricane deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV/ACV holdback</a> calculators.</li><li>Condo owner? Run the <a href="{TOOL_BASE}condo-deductible-share-calculator/">condo deductible share calculator</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-check/">appraisal readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Island Claim Tools",
                              "Free insurance claim calculators for island owners: claim gap, RCV/ACV, roof squares, hurricane and condo deductibles, plus a planner.",
                              body, [crumbs_schema(trail), item_list(items)], preload="laptop-calculator", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- resources
LEARN = [("Appraisal process map", P_PROCESS), ("Questions by topic", P_FAQ), ("Claim glossary", P_GLOSS), ("Hawaii claim guides", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Process map", path)]
    roadmap = '<ol class="roadmap">' + "".join(f'<li><a href="#step-{i + 1}"><span>{i + 1}</span><b>{e(n)}</b><small>{e(sm)}</small></a></li>' for i, (n, sm) in enumerate(PROCESS_STEPS)) + "</ol>"
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in Hawaii, Mapped",
                     f"{len(PROCESS_STEPS)} stages, from the first disagreement to a signed award — what happens, who does what and where island claims most often stall.", "inspection-clipboard",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(roadmap + re.sub(r"<h2>Step (\d+)", r'<h2 id="step-\1">Step \1', PROCESS_BODY), call_box() + list_box("Resources", LEARN, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Hawaii", "description": "The stages of a property insurance appraisal under a policy’s appraisal clause.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": sm, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, sm) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in Hawaii | Step by Step",
                         "A step-by-step map of the insurance appraisal process in Hawaii: the written demand, appraisers, umpire, negotiation and binding award.",
                         body, [crumbs_schema(trail), howto], preload="inspection-clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Questions by topic", path)]
    jump = '<nav class="jump" aria-label="FAQ topics">' + "".join(f'<a href="#t-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ)) + "</nav>"
    groups = "".join(f'<h2 id="t-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions, Grouped by Topic",
                     "Plain answers about the appraisal process, costs, deadlines and the questions that are unique to island policies.", "lanai-interior") + layout(jump + groups, call_box() + list_box("Resources", LEARN, path)) + cta_band("Didn’t see your question?", "Call or email — we’re happy to talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ by Topic | Hawaii Owners",
                         "Insurance appraisal FAQ for Hawaii owners, grouped by topic: basics, costs, deadlines, HPIA, hurricane deductibles and condo policies.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="lanai-interior"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards — including island-specific ones like AOAO, GET, HPIA and lava zone — in plain English.", "calculator-documents", cta=False) + layout(
        f'<div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “umpire”, “vog” or “depreciation”" autocomplete="off"><p class="hint" data-gcount></p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>',
        call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "url": DOMAIN + path,
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path + "#definedtermset"} for t, d in GLOSSARY]}
    write(path, document(path, "Property Claim Glossary | ACV, Umpire, GET & More",
                         "A searchable property claim glossary: actual cash value, appraisal award, umpire, hurricane deductible, AOAO, GET, HPIA and more.",
                         body, [crumbs_schema(trail), dts], preload="calculator-documents"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {e(p["read"])} read</p>' + p["body"] + (f'<h2>Quick answers</h2>{faq_block(p["faqs"])}' if p.get("faqs") else "") + "<h2>Keep reading</h2>" + related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])
        body = page_hero(trail, f"Claim guide · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", LEARN) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_band()
        bp = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{pk(ph)}.webp", "url": DOMAIN + path, "keywords": p["keyword"]}
        sch = [crumbs_schema(trail), bp] + ([faq_schema(p["faqs"])] if p.get("faqs") else [])
        write(path, document(path, p["seo"], p["desc"], body, sch, og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim guides", path)]
    cards = "".join(f'<article class="pcard rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a><div class="pc-b"><span class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</span><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Claim guides", "Hawaii Claim Guides for Property Owners",
                     "Practical guides on hurricane deductibles, condo master policies, wildfire smoke, salt-air corrosion and island pricing — written for owners heading into a claim dispute.", "lanai-interior", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pcards" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Hawaii Claim Guides | Deductibles, Condos & Smoke",
                         "Hawaii claim guides for property owners: hurricane deductibles, condo master policies, wildfire smoke, salt-air damage and estimate pricing.",
                         body, [crumbs_schema(trail), item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload="lanai-interior", page_type="CollectionPage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    art = f"""<figure class="lead-img">{img("inspection-clipboard", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most claim professionals do a little of everything. {BRAND} works on a single question — the amount of loss — and builds its inspections, estimates and tools around answering it well. That focus lets us serve as your appointed appraiser, review a carrier’s estimate before a dispute hardens, or sit as a neutral umpire where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before price.</strong> We inspect, measure and photograph before we look at anyone else’s numbers.</li>
<li><strong>Island pricing, shown openly.</strong> Freight, crew travel and general excise tax appear as their own lines, so they can be checked.</li>
<li><strong>Defensible over dramatic.</strong> An inflated number loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, AOAO boards and managing agents, landlords, churches, hotels and small businesses, contractors, public adjusters and attorneys. On any one claim we serve in a single role, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate outside the appraisal process. We don’t promise outcomes — no honest appraiser can. Questions about claim handling can also go to the Insurance Division of the Department of Commerce and Consumer Affairs.</p>
<h2>Statewide, island by island</h2>
<p>Rebuilding a plantation-style home in Hilo, a high-rise unit in Kakaako and a ranch house in Kula are three different estimates. Working on every island means we see the full range of losses Hawaii produces — and price each with local knowledge.</p>"""
    body = page_hero(trail, "About us", "About Hawaii Insurance Appraiser",
                     "We’re estimators and appraisers who believe an island property claim should be paid on what the damage actually costs to repair here — documented clearly enough that everyone at the table can see it.", "consultation") + layout(
        art, call_box() + list_box("Explore", [("Appraisal specialties", SVC_BASE), ("Island communities", LOC_BASE), ("Free claim tools", TOOL_BASE), ("Appraisal process map", P_PROCESS)])) + cta_band()
    write(path, document(path, "About Us | Independent Appraisers for Island Claims",
                         "About Hawaii Insurance Appraiser, an independent appraisal practice that values disputed property claims on every island in the state.",
                         body, [crumbs_schema(trail)], preload="consultation", page_type="AboutPage"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Hawaii Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "condo-towers", cta=False) + f"""
<section class="sec deep"><div class="wrap contact">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>{HOURS}</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>Oahu, Hawaii Island, Maui, Kauai, Molokai &amp; Lanai</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ready"><li>Your declarations page, including any hurricane deductible</li><li>The carrier’s full line-item estimate</li><li>Letters or emails from the carrier</li><li>Photos, video and your contractor’s estimate</li><li>For condos: the master policy summary and any assessment notice</li></ul></div>
<div class="rv">{lead_form("Send us your claim details", page=path, hid="cf")}</div></div></section>"""
    write(path, document(path, "Contact Us | Free Claim Review · (844) 537-1427",
                         "Contact Hawaii Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, or send your details.",
                         body, [crumbs_schema(trail)], preload="condo-towers", page_type="ContactPage"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Policy", "Privacy Policy | How We Handle Your Information",
                    "Read the Hawaii Insurance Appraiser privacy policy: what we collect through forms and calls, how we use it and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share — such as your name, phone number, email address, island and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working properly.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers that host our website and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        P_TERMS: ("Terms of Use", "Terms of Use | Rules for Using This Website",
                  "The terms of use for the Hawaii Insurance Appraiser website, its free claim tools and its educational content. Please read them first.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Hawaii.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Hawaii attorney for legal questions.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates based on what you enter. Example figures are illustrative. Neither is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs on this site are public-domain or CC0 images.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Hawaii.</p>""", "The terms that apply when you use this website and its tools."),
        P_DISC: ("Disclaimer", "Disclaimer | Appraisal, Legal and Results Limits",
                 "The Hawaii Insurance Appraiser disclaimer: general information only, no legal advice, no guaranteed results and illustrative examples.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy, endorsements and any condominium documents.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is approaching, consult a Hawaii attorney promptly.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They do not show clients’ properties.</p>
<h2>Third-party references</h2><p>References to statutes, agencies, programs and weather events are for context. Verify current law and facts with official sources such as the Insurance Division of the Hawaii Department of Commerce and Consumer Affairs.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h1, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "commercial-building", cta=False) + layout(content, call_box())
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], preload="commercial-building"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Appraisal specialties", [("All specialties", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Island communities", [("All communities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIVACY), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="smap rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, in one place.", "commercial-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="smaps" data-stagger>{cols}</div></div></section>'
    write(path, document(path, "Site Map | Every Page on Hawaii Insurance Appraiser",
                         "The complete site map for Hawaii Insurance Appraiser: appraisal specialties, island communities, free claim tools, guides and legal pages.",
                         body, [crumbs_schema(trail)], preload="commercial-building"), 0.3)

    body = f"""<section class="phero"><div class="phero-bg">{img("storm-surf", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="tag">Error 404</p><h1>This page drifted out to sea</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn sun" href="/">Home</a><a class="btn line-light" href="{SVC_BASE}">Specialties</a><a class="btn line-light" href="{TOOL_BASE}">Free tools</a><a class="btn line-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "Sorry, that page could not be found on Hawaii Insurance Appraiser. Try our specialties, free claim tools or the contact page instead.",
                                body, robots="noindex,follow"), sitemap=False)


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    files = {
        "sitemap.xml": "\n".join(xml) + "\n",
        "robots.txt": f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n",
        "index.php": INDEX_PHP,
        "_guard.php": GUARD_PHP,
    }
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(text)
    # Search Console verification: exact bytes, no newline, BOM or wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Hawaii Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$hia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$hia_real  = 'hawaiiinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$hia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://hawaiiinsuranceappraiser.com - only on the real domain.
if ($hia_host === 'www.' . $hia_real || ($hia_host === $hia_real && $hia_proto === 'http')) {
    header('Location: https://' . $hia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $hia_m)) {
    $hia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $hia_m[1] . $hia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($hia_host !== $hia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Hawaii Insurance Appraiser - front controller for the static build.
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
