#!/usr/bin/env python3
"""Static site generator for rhodeislandinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php (guarded) and home.html; see README.
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
from locations import LOCATIONS, REGIONS  # noqa: E402
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))
ALT = json.load(open(os.path.join(ROOT, "src", "photo_alt.json"), encoding="utf-8"))

BRAND = "Rhode Island Insurance Appraiser"
HOST = "rhodeislandinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

SVC_BASE = "/claim-valuation-services/"
LOC_BASE = "/rhode-island-communities/"
TOOL_BASE = "/policyholder-tools/"
POST_BASE = "/claim-notebook/"
PROCESS = "/the-appraisal-sequence/"
FAQ_P = "/policyholder-questions/"
GLOSS = "/claim-wordbook/"
ABOUT = "/firm-profile/"
CONTACT = "/request-a-claim-review/"
MAP = "/browse-the-site/"
PRIVACY, TERMS, DISCL, CREDITS = "/data-privacy/", "/use-terms/", "/claim-disclaimer/", "/photo-credits/"

e = html.escape
pages = []  # (path, priority) for sitemap


def P(*keys):
    """First available photo key (lets the shot list substitute gracefully)."""
    for k in keys:
        if k in PHOTOS:
            return k
    raise KeyError(f"none of {keys} in photos.json")


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    """lazy=True: loading=lazy; lazy=False: high-priority hero image; lazy=None: eager, normal priority (horizontal rails)."""
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT.get(key, p.get("title", "")))
    load = ' loading="lazy"' if lazy else ("" if lazy is None else ' fetchpriority="high"')
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-advocacy": P("consultation-table"), "homeowner-claim-valuation": P("hero-coastal-house", "triple-decker"),
    "commercial-condo-hoa-claims": P("commercial-storefront", "condo-building"), "roof-hail-claim-valuation": P("roof-shingles-damaged", "roofer-at-work"),
    "wind-microburst-tornado-claims": P("tree-on-house", "storm-surf"), "hurricane-tropical-storm-claims": P("hurricane-flood-street", "storm-surf"),
    "water-leak-sewer-backup-claims": P("water-ceiling", "flood-cleanup"), "ice-dam-freeze-claims": P("frozen-icicles", "snow-roof"),
    "fire-smoke-claim-valuation": P("burned-house"), "claim-estimate-audit": P("estimate-calculator"),
    "neutral-umpire-services": P("insurance-paperwork", "consultation-table"),
}
TOOL_PHOTO = {
    "settlement-gap-estimator": P("estimate-calculator"), "rcv-acv-holdback-calculator": P("insurance-paperwork", "estimate-calculator"),
    "roof-area-pitch-converter": P("roofer-at-work", "roof-shingles-damaged"), "hurricane-deductible-calculator": P("storm-surf", "lightning-sky"),
    "claim-timeline-builder": P("inspector-clipboard", "insurance-paperwork"), "appraisal-readiness-checkup": P("consultation-table"),
    "wind-flood-damage-splitter": P("flood-cleanup", "hurricane-flood-street"),
}
POST_PHOTO = {
    "rhode-island-appraisal-provision-explained": P("ri-state-house", "providence-skyline"),
    "hurricane-deductibles-in-rhode-island": P("lightning-sky", "storm-surf"),
    "documenting-ice-dam-and-nor-easter-damage": P("snow-roof", "frozen-icicles"),
    "wind-versus-flood-after-a-coastal-storm": P("flood-cleanup", "hurricane-flood-street"),
    "matching-materials-on-older-rhode-island-homes": P("providence-college-hill", "colonial-house"),
    "choosing-claim-help-in-rhode-island": P("consultation-table"),
}
HERO = P("colonial-house")

# ---------------------------------------------------------------- icons (all SVGs carry explicit width/height)
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "snow": '<path d="M12 2v20M4.9 6.5l14.2 11M19.1 6.5L4.9 17.5M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
}


def ic(name, cls="ic", size=20):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>')


def mark(size=40):
    """Brand mark: sun-yellow tile, a roof line and an Ocean State wave."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#FEC500"/>'
            '<path d="M10.5 25.5L24 13l13.5 12.5" fill="none" stroke="#16171B" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M9 35.5c3.75-4.2 7.5-4.2 11.25 0s7.5 4.2 11.25 0 5.6-4.2 8.5-1.6" fill="none" stroke="#23317A" stroke-width="3.6" stroke-linecap="round"/></svg>')


def brand(cls=""):
    return (f'<a class="brand{(" " + cls) if cls else ""}" href="/" aria-label="{BRAND}, home">{mark()}'
            f'<span class="brand-t"><b>Rhode Island</b><span>Insurance Appraiser</span></span></a>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "RI", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-RI", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Rhode Island.",
        "areaServed": [{"@type": "State", "name": "Rhode Island"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal provision", "Hurricane deductibles", "Wind and flood damage", "Ice dam claims", "Property claim estimating"],
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


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE)),
        ("Communities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Rhode Island", LOC_BASE)),
        ("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All tools", TOOL_BASE)),
        ("Learn", [("The appraisal sequence", PROCESS), ("Policyholder questions", FAQ_P), ("Claim wordbook", GLOSS), ("Claim notebook (guides)", POST_BASE)], None),
    ]


def header(hero):
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow", "ic", 16)}</a></li>'
        cols = " cols" if len(links) > 7 else ""
        menu += f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "ic chev", 16)}</button><ul class="sub{cols}" id="sub-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{ABOUT}">About</a></li><li><a class="top-link" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += (f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev", 18)}</button>'
                f'<div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>')
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="hdr{" over-hero" if hero else ""}"><div class="wrap hdr-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="hdr-call" href="tel:{TEL}">{ic("phone", "ic", 18)}<span>{PHONE}</span></a>
<a class="nojs-menu" href="{MAP}">Menu</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close aria-hidden="true"></div>
<nav class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x", "ic", 22)}</button></div>
<ul class="drawer-list"><li><a class="acc-link" href="/">Home</a></li>{acc}</ul>
<div class="drawer-foot"><a class="btn sun" href="tel:{TEL}">{ic("phone", "ic", 18)} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri, 8am–6pm ET · Statewide</small></div>
</nav>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="ftr">
<div class="ftr-band"><div class="wrap ftr-band-in"><h2>Short check? Let’s see what was missed.</h2><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone", "ic", 18)} {PHONE}</a><a class="btn glass" href="{CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap ftr-grid">
<div class="ftr-about">{brand("brand-ftr")}
<p>Independent appraisal and estimating for property owners with disputed insurance claims, from Woonsocket to Westerly and out to Block Island.</p>
<ul class="ftr-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri, 8am–6pm ET</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Communities</h3><ul>{loc}<li><a href="{LOC_BASE}">All Rhode Island</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Learn</h3><ul><li><a href="{PROCESS}">The appraisal sequence</a></li><li><a href="{FAQ_P}">Policyholder questions</a></li><li><a href="{GLOSS}">Claim wordbook</a></li><li><a href="{POST_BASE}">Claim notebook</a></li><li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap ftr-legal"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCL}">Disclaimer</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{MAP}">Site map</a></li></ul></div>
<p class="wrap ftr-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general; policy wording controls. Example figures are illustrative, and no result is guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up", "ic", 20)}</button>
<div class="callbar"><a href="tel:{TEL}">{ic("phone", "ic", 18)} Call now</a><a href="{CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, hero=True):
    canonical = DOMAIN + path
    page_type, extra, crumb_id, main_pref = "WebPage", [], None, None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            main_pref = n.get("_main")
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        if t in ("Service", "WebApplication"):
            n["provider"] = {"@id": DOMAIN + "/#business"}
        extra.append(n)
    img_key = photo or HERO
    pimg = PHOTOS[img_key]
    img_url = f"{DOMAIN}/assets/img/photos/{img_key}.webp"
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": img_url, "contentUrl": img_url, "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    ids = {n["@type"]: n["@id"] for n in extra if "@id" in n}
    order = [main_pref] if main_pref else []
    order += ["Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"]
    main_id = next((ids[t] for t in order if t in ids), DOMAIN + "/#business")
    webpage["mainEntity"] = {"@id": main_id}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{img_key}.webp" imagesrcset="/assets/img/photos/{img_key}-640.webp 640w, '
           f'/assets/img/photos/{img_key}.webp {pimg["fw"]}w" imagesizes="100vw">\n') if hero else ""
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Rhode Island">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Rhode Island">
<meta name="geo.region" content="US-RI">
<meta name="geo.placename" content="Rhode Island">
<meta name="theme-color" content="#16171B">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Epilogue:wght@600;700;800&family=Instrument+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{gtm_body()}{header(hero)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/app.js?v={VER}" defer></script>
</body>
</html>
"""


def write(path, content, priority=0.6, sitemap=True):
    # The host serves real files without running the front controller, so every directory page is
    # dir/index.php whose first line requires the canonical-host guard. Never write dir/index.html.
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = (f'<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone", "ic", 18)} Call {PHONE}</a>'
         f'<a class="btn glass" href="{CONTACT}">Free claim review</a></div>') if cta else ""
    return (f'<section class="phero">{img(photo, "phero-bg", lazy=False, alt="")}<div class="wrap phero-in">{crumbs(trail)}'
            f'<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev", 18)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="box box-call"><h2 class="box-t">Talk it through</h2><p>A free first conversation. We’ll tell you plainly whether appraisal fits your claim.</p>'
            f'<a class="box-phone" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn ink" href="{CONTACT}">Send claim details</a></div>')


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right", "ic", 14)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Carrier’s number doesn’t cover the repair?", p="Send us the estimate and your photos. We’ll review them and tell you what we see."):
    return (f'<section class="strip"><div class="wrap strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row">'
            f'<a class="btn ink" href="tel:{TEL}">{ic("phone", "ic", 18)} {PHONE}</a><a class="btn ink-line" href="{CONTACT}">Email the estimate</a></div></div></section>')


def related(items, label):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(label)}</small><span>{e(n)}</span>{ic("arrow", "ic", 18)}</a>' for n, p in items) + "</div>"


LOSSES = ["Wind / nor’easter", "Hurricane / tropical storm", "Ice dam / frozen pipe", "Water leak", "Fire / smoke", "Roof / hail", "Tree on structure", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Commercial owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Rhode Island"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-t">{e(heading)}</p><p class="form-sub">Free review · no obligation · a reply within one business day, usually sooner.</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{hid}-amt">Approximate amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. This doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn ink wide" type="submit">Send my claim details {ic("arrow", "ic", 18)}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="ticket" action="/api/contact.php" method="post" data-lead novalidate>
<p class="ticket-t">Free claim review</p><p class="form-sub">Three fields. A real person calls you back, usually the same business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy</a>.</span></label>
<button class="btn ink wide" type="submit">Request my review {ic("arrow", "ic", 18)}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


# ---------------------------------------------------------------- home
SEASONS = [
    ("Jan–Mar", "Blizzards & ice dams", "Heavy snow, roof loads and meltwater backing up under shingles.", "snow"),
    ("Mar–May", "Spring rain & nor’easters", "Saturated ground, river flooding and late-season coastal storms.", "drop"),
    ("Jun–Aug", "Thunderstorms & hail", "Downbursts, lightning and occasional hail crossing from the west.", "hail"),
    ("Aug–Oct", "Hurricane season peak", "Tropical systems funneling wind and surge up Narragansett Bay.", "storm"),
    ("Oct–Dec", "Fall nor’easters", "Long-duration wind, falling trees and wind-driven rain.", "wind"),
]

STORMS = [
    ("1938", "New England Hurricane", "Storm surge flooded downtown Providence and swept away homes along the South County beaches."),
    ("1954", "Hurricane Carol", "Flooded Providence again and led to the Fox Point Hurricane Barrier."),
    ("1978", "The Blizzard of ’78", "Still the benchmark for snowfall and roof loads across the state."),
    ("1991", "Hurricane Bob", "Battered the coast from Westerly to Little Compton."),
    ("2010", "March floods", "The Pawtuxet River reached record levels in Cranston and Warwick."),
    ("2012", "Superstorm Sandy", "Damaged dunes, seawalls and homes in Misquamicut and Narragansett."),
    ("2021", "Henri", "Made landfall near Westerly, bringing wind and downed trees inland."),
]


def home():
    K = BRAND
    rail = "".join(
        f'<a class="rail-card rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 80vw, 340px", lazy=None, alt="")}'
        f'<span class="rail-n">{i + 1:02d}</span><span class="rail-b"><span class="rail-ic">{ic(s["icon"], "ic", 22)}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
        for i, s in enumerate(SERVICES))
    seasons = "".join(f'<li class="rv"><span class="s-ic">{ic(icn, "ic", 22)}</span><b>{e(m)}</b><h3>{e(t)}</h3><p>{e(d)}</p></li>' for m, t, d, icn in SEASONS)
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}</button>'
        for i, (k, n, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0">'
        f'<div class="region-ph">{img(P(ph), sizes="(max-width:900px) 100vw, 560px", alt="")}</div>'
        f'<div class="region-tx"><p class="tag dark">{e(sub)}</p><h3>{e(n)}</h3><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p class="small">Towns: {e(towns)}</p></div></div>'
        for i, (k, n, sub, perils, t, towns, ph) in enumerate(REGIONS))
    steps = "".join(f'<li class="rv"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PROCESS_STEPS[1:6]))
    storms = "".join(f'<li class="rv"><b>{y}</b><h3>{e(n)}</h3><p>{e(d)}</p></li>' for y, n, d in STORMS)
    tools = "".join(
        f'<a class="pcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="pcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="pcard-k">{e(t["kind"])}</span></span>'
        f'<span class="pcard-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open the tool {ic("arrow", "ic", 16)}</span></span></a>' for t in TOOLS)
    towns = "".join(
        f'<a class="town rv" href="{loc_path(l)}">{img(P(l["photo"]), sizes="(max-width:700px) 50vw, 280px", alt="")}<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    posts = "".join(
        f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a>'
        f'<div class="post-b"><p class="meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree a loss is covered but disagree on the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work through it with the carrier’s appraiser and, if needed, present unresolved items to the umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster represents you in preparing and negotiating the whole claim. An appraiser works inside the policy’s appraisal process on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When does appraisal make sense?", "When coverage is accepted, you have the carrier’s itemized estimate and a credible estimate of your own, and the difference is meaningful: generally more than about 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, generally yes, once any two of the three panel members sign. That’s why the file should be well documented before appraisal starts."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you cover Block Island and the rest of the state?", "Yes. We work in all 39 cities and towns across Rhode Island’s five counties, and on Block Island by arrangement."),
    ]
    body = f"""
<section class="hero">
<div class="hero-bg">{img(HERO, lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="tag">Independent property claim appraisal · Statewide</p>
<h1><span class="hl">{K}</span> for claims that came up short</h1>
<p class="lede">The carrier accepted your claim, but the check won’t pay for the repair. A {K} builds an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone", "ic", 18)} Call {PHONE}</a><a class="btn glass" href="#services">See what we value {ic("arrow", "ic", 18)}</a></div>
</div>
{hero_form()}
</div>
</section>

<section class="facts-band" aria-label="At a glance"><div class="wrap facts-band-in">
<div class="fb"><b data-count="39">39</b><span>Cities and towns covered</span></div>
<div class="fb"><b data-count="5">5</b><span>Counties, one appraiser</span></div>
<div class="fb"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="fb"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim tools</span></div>
</div></section>

<section class="sec"><div class="wrap ledger-wrap">
<div class="rv">
<p class="tag dark">The short version</p>
<h2>Covered isn’t the same as paid</h2>
<p>Most underpaid claims in Rhode Island aren’t denied. They’re short: a slope left off the roof, plaster priced as drywall, a hurricane deductible applied to an incomplete scope. A {K} works in the space between the carrier’s number and the real cost of the repair.</p>
<p>We inspect, measure and price the loss from scratch, then put that valuation in front of the carrier’s appraiser line by line. When we can’t agree, a neutral umpire decides the difference.</p>
<a class="btn ink" href="{ABOUT}">How we work {ic("arrow", "ic", 18)}</a>
</div>
<div class="ledger rv" aria-label="Illustrative example of an underpaid claim">
<p class="ledger-h">Illustrative example · not a client result</p>
<div class="ledger-row"><span>Carrier’s estimate (RCV)</span><b>$18,450</b></div>
<div class="ledger-row"><span>Missed: rear slope, 7 squares</span><b>+$4,980</b></div>
<div class="ledger-row"><span>Missed: steep charge, 10/12 pitch</span><b>+$1,320</b></div>
<div class="ledger-row"><span>Plaster ceiling priced as drywall</span><b>+$2,140</b></div>
<div class="ledger-row"><span>General contractor O&amp;P</span><b>+$2,890</b></div>
<div class="ledger-row total"><span>Independent valuation</span><b>$29,780</b></div>
</div>
</div></section>

<section class="sec sun-wash" id="services"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">What we value</p><h2>{len(SERVICES)} ways a {K} works on your claim</h2></div><p>Start with an estimate review, or bring us in after appraisal has been demanded. Every service is about one thing: a valuation of your loss that holds up.</p></div>
<div class="rail-wrap"><div class="rail" data-rail tabindex="0" aria-label="Services">{rail}</div>
<div class="rail-ctl"><button type="button" class="rail-btn" data-rail-prev aria-label="Previous services">{ic("left", "ic", 20)}</button><button type="button" class="rail-btn" data-rail-next aria-label="Next services">{ic("right", "ic", 20)}</button><a class="link" href="{SVC_BASE}">All services {ic("arrow", "ic", 16)}</a></div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Ocean State claim calendar</p><h2>What each season sends a {K}</h2></div><p>Rhode Island’s weather runs on a calendar. Knowing when and how damage happens helps us scope it, and helps you document it.</p></div>
<ol class="seasons">{seasons}</ol>
</div></section>

<section class="sec ink-sec"><div class="wrap">
<div class="sec-head rv"><div><p class="tag">Six regions, one small state</p><h2>Where a {K} sees claims</h2></div><p>A Westerly beach house, a Pawtucket three-decker and a Glocester farmhouse can all be damaged by the same storm in very different ways.</p></div>
<div class="regions rv" data-tabs><div class="region-tabs" role="tablist" aria-label="Rhode Island regions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec"><div class="wrap split">
<div class="rv"><p class="tag dark">How it works</p><h2>From written demand to signed award</h2><p>The appraisal provision turns an open-ended argument into a defined process with a binding result on the amount of loss. Here is how a {K} takes a file through it.</p><a class="link" href="{PROCESS}">Read the full appraisal sequence {ic("arrow", "ic", 16)}</a></div>
<ol class="steps">{steps}</ol>
</div></section>

<section class="sec harbor" id="check"><div class="wrap split">
<div class="rv"><p class="tag">Quick gap check</p><h2>Is the difference worth an appraisal?</h2><p>Enter the two numbers you already have. If the gap is large, it’s worth a call with a {K}. If it’s small, a documented supplement request may close it faster.</p><p>The full <a href="{TOOL_BASE}settlement-gap-estimator/">settlement gap estimator</a> subtracts appraiser and umpire fees so you can see a realistic net.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Storm record</p><h2>Storms a {K} still hears about</h2></div><p>Adjusters, contractors and homeowners here still measure claims against these events.</p></div>
<ol class="storms" data-rail tabindex="0" aria-label="Rhode Island storm history">{storms}</ol>
</div></section>

<section class="sec sun-wash"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Free &amp; private</p><h2>Claim tools from a {K}</h2></div><p>Check the carrier’s math before you pick up the phone. Every tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="pgrid seven">{tools}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Communities</p><h2>{K} services in your city or town</h2></div><p>We inspect in every Rhode Island community. These pages cover the places we’re called most often.</p></div>
<div class="towns">{towns}</div>
<p class="center"><a class="link" href="{LOC_BASE}">See every region {ic("arrow", "ic", 16)}</a></p>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Three-question test</p><h2>Should you call a {K}?</h2></div><p>Answer these honestly. If all three are “yes,” appraisal is worth a conversation. If not, we’ll point you to the right kind of help.</p></div>
<div class="test">
<div class="test-q rv"><span>1</span><h3>Has the insurer accepted coverage?</h3><p>Appraisal values a covered loss. If the claim was denied outright, a Rhode Island attorney is usually the first call.</p></div>
<div class="test-q rv"><span>2</span><h3>Do you have two itemized estimates?</h3><p>The carrier’s full line-item estimate and a credible one of your own. A one-line bid isn’t enough for a panel.</p></div>
<div class="test-q rv"><span>3</span><h3>Is the gap worth the cost?</h3><p>Generally more than about 10% of the carrier’s estimate or several thousand dollars. Smaller gaps often close with a supplement.</p></div>
</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="tag dark">Questions</p><h2>What people ask a {K}</h2><p>Short, plain answers about the process, costs and when appraisal is the wrong move.</p><div class="btn-row"><a class="btn ink" href="{FAQ_P}">All questions {ic("arrow", "ic", 18)}</a><a class="btn line" href="{GLOSS}">Claim wordbook</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec stone"><div class="wrap">
<div class="sec-head rv"><div><p class="tag dark">Claim notebook</p><h2>Read this before you invoke appraisal</h2></div><p>Guides on Rhode Island policy wording, hurricane deductibles and documentation from the {K} team.</p></div>
<div class="posts">{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All guides {ic("arrow", "ic", 16)}</a></p>
</div></section>

<section class="sec ink-sec" id="contact"><div class="wrap split top">
<div class="rv"><p class="tag">Start with a conversation</p><h2>Talk with a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="lines"><li>{ic("phone", "ic", 20)}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail", "ic", 20)}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock", "ic", 20)}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin", "ic", 20)}<span><small>Coverage</small><b>All 39 Rhode Island cities and towns</b></span></li></ul></div>
<div class="rv">{lead_form(page="/", hid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Help",
                        f"{BRAND}: independent appraisal, estimate review and umpire services for underpaid wind, hurricane, ice dam and fire claims.",
                        body, [faq_schema(home_faqs)], photo=HERO), 1.0)


# ---------------------------------------------------------------- services
def layout(article, aside):
    return f'<div class="wrap layout"><article class="prose">{article}</article><aside class="side">{aside}</aside></div>'


def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
        art = (s["body"] + f'<h2>Questions about {e(s["name"].lower())}</h2>' + faq_block(s["faqs"]) +
               '<h2>Related services</h2>' + related([(r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel], "Service"))
        body = page_hero(trail, "Service", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(
            art, call_box() + list_box("All services", items, path) + list_box("Where we work", locs + [("All Rhode Island", LOC_BASE)])) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "areaServed": {"@type": "State", "name": "Rhode Island"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    ph = P("roofer-at-work")
    cards = "".join(
        f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/"><span class="pcard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="pcard-k">{i + 1:02d}</span></span>'
        f'<span class="pcard-b"><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Read more {ic("arrow", "ic", 16)}</span></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we value", "Insurance Appraisal Services Across Rhode Island",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of the loss.", ph) + f"""
<section class="sec"><div class="wrap"><div class="pgrid">{cards}</div></div></section>
<section class="sec stone"><div class="wrap split top"><div class="rv"><p class="tag dark">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review gives you the answer in days, and many disputes close at that stage.</p><a class="btn ink" href="{SVC_BASE}claim-estimate-audit/">About estimate reviews {ic("arrow", "ic", 18)}</a></div>
<div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to invoke appraisal."), ("Do you handle commercial and association claims?", "Yes: mixed-use buildings, mills, retail, offices and condominium associations."), ("Do you handle flood claims?", "Our appraisal work is under property policies that cover the loss. Flood policies have their own procedures; we can help organize a mixed wind and flood loss.")])}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage", "_main": "ItemList"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services | Rhode Island",
                             "Rhode Island insurance appraisal services: appraisal clause representation, estimate review, wind, hurricane, ice dam, water and fire claims.",
                             body, schema, photo=ph), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        city = l["city"]
        trail = [("Home", "/"), ("Communities", LOC_BASE), (city, path)]
        ph = P(l["photo"])
        chips = "".join(f"<li>{e(x)}</li>" for x in l["perils"])
        hoods = "".join(f"<li>{e(x)}</li>" for x in l["neighborhoods"])
        storms = "".join(f'<li><b>{e(y)}</b><span>{e(t)}</span></li>' for y, t in l["storms"])
        svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        art = (f'<div class="note"><p class="note-t">Local claim risks</p><ul class="chips">{chips}</ul></div>' + l["body"] +
               f'<h2>Neighborhoods and villages we cover in {e(city)}</h2><ul class="chips plain">{hoods}</ul>'
               f'<h2>Housing in {e(city)}</h2><p>{e(l["housing"])}</p>'
               f'<h2>{e(city)} storm history</h2><ul class="mini-timeline">{storms}</ul>'
               f'<h2>Services available in {e(city)}</h2><p>Every {BRAND} service is available to owners in {e(city)} and nearby towns, including:</p><ul>{svc}</ul>'
               f'<h2>Questions from {e(city)} owners</h2>{faq_block(l["faqs"])}'
               f'<h2>Nearby communities</h2>' + related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby"))
        aside = call_box() + list_box("Rhode Island communities", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {city}, Rhode Island", e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, aside) + cta_strip(
            f"Disputed claim in {city}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]),
                  {"@type": "Service", "name": f"Insurance appraisal in {city}, RI", "serviceType": "Insurance appraisal",
                   "areaServed": {"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "Rhode Island"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {city}, RI | Claim Disputes"
        if len(title) > 56:
            title = f"Insurance Appraiser in {city}, RI"
        desc = f"Independent insurance appraiser in {city}, {l['county']}. Appraisal and estimate review for underpaid storm, water, ice dam and fire claims."
        if len(desc) > 150:
            desc = f"Independent insurance appraiser in {city}, RI: appraisal and estimate review for underpaid storm, water, ice dam and fire claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Communities", LOC_BASE)]
    ph = P("providence-skyline")
    towns = "".join(f'<a class="town rv" href="{loc_path(l)}">{img(P(l["photo"]), sizes="(max-width:700px) 50vw, 280px", alt="")}<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="pcard static rv"><span class="pcard-ph">{img(P(rph), sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="pcard-k">{e(sub)}</span></span>'
                  f'<span class="pcard-b"><h2>{e(n)}</h2><p>{e(t)}</p><p class="small">{e(tw)}</p></span></div>' for k, n, sub, _p, t, tw, rph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in Every Rhode Island Community",
                     f"Rhode Island has 39 cities and towns in five counties, with no county government, so every claim is local. {BRAND} inspects statewide; these pages cover the communities we visit most.", ph) + f"""
<section class="sec"><div class="wrap"><div class="towns">{towns}</div></div></section>
<section class="sec stone"><div class="wrap"><div class="sec-head rv"><div><p class="tag dark">Regions</p><h2>How claims differ across Rhode Island</h2></div><p>The same policy language plays out very differently on a barrier beach, in a mill city and in the northwest hills.</p></div><div class="pgrid">{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We work in all 39 cities and towns. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Rhode Island Insurance Appraiser Communities",
                             "Insurance appraisal in all 39 Rhode Island cities and towns, including Providence, Warwick, Cranston, Pawtucket, Newport and Westerly.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage", "_main": "ItemList"}, itemlist(items)], photo=ph), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + '<h2>Questions about this tool</h2>' + faq_block(t["faqs"]) + '<h2>More free tools</h2>' + related([(o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others], "Tool")
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice.</p></div></section>
""" + layout(art, call_box() + list_box("All claim tools", items, path)) + cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]),
                  {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
                   "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    ph = P("estimate-calculator")
    cards = "".join(
        f'<a class="pcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="pcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}<span class="pcard-k">{e(t["kind"])}</span></span>'
        f'<span class="pcard-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open the tool {ic("arrow", "ic", 16)}</span></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Property Claim Tools for Rhode Island Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Check the carrier’s math, plan your deadlines and sort out a coastal loss, with no sign-up and nothing stored.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="pgrid seven">{cards}</div></div></section>
<section class="sec stone"><div class="wrap split top"><div class="rv"><p class="tag dark">Suggested order</p><h2>Using the tools together</h2><ol class="order"><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a> so nothing lapses.</li><li>After a coastal storm, sort the loss with the <a href="{TOOL_BASE}wind-flood-damage-splitter/">wind vs. flood splitter</a>.</li><li>Check roof quantities with the <a href="{TOOL_BASE}roof-area-pitch-converter/">roof area &amp; pitch converter</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}hurricane-deductible-calculator/">hurricane deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV / ACV</a> calculators.</li><li>Test the dispute with the <a href="{TOOL_BASE}settlement-gap-estimator/">settlement gap estimator</a>, then take the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Property Claim Tools | Rhode Island",
                              "Free property claim tools: settlement gap, RCV/ACV holdback, roof pitch and hurricane deductible calculators, a timeline builder and more.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage", "_main": "ItemList"}, itemlist(items)], photo=ph), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("The appraisal sequence", PROCESS), ("Policyholder questions", FAQ_P), ("Claim wordbook", GLOSS), ("Claim notebook", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("The appraisal sequence", path)]
    ph = P("inspector-clipboard")
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Rhode Island",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what and where claims most often go wrong.", ph,
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(PROCESS_BODY, call_box() + list_box("Learn", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Rhode Island", "description": "The seven stages of a property insurance appraisal, from the written demand to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Rhode Island",
                         "Step-by-step guide to insurance appraisal in Rhode Island: the written demand, naming appraisers, choosing an umpire and the binding award.",
                         body, [crumbs_schema(trail), howto], photo=ph), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Policyholder questions", path)]
    ph = P("consultation-table")
    toc = "".join(f'<li><a href="#q-{i}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = f'<nav class="toc" aria-label="Topics"><p class="note-t">Jump to a topic</p><ul>{toc}</ul></nav>' + "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions from Rhode Island Owners",
                     "Plain answers about the appraisal process, costs, timing and how Rhode Island rules fit in, grouped by topic.", ph) + layout(
        groups, call_box() + list_box("Learn", LEARN, path)) + cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")
    write(path, document(path, "Insurance Appraisal Questions | Rhode Island FAQ",
                         "Answers to Rhode Island insurance appraisal questions by topic: the basics, when it fits, costs and timing, and state-specific rules.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo=ph), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim wordbook", path)]
    ph = P("insurance-paperwork", "estimate-calculator")
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="g-item"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>'
    art = (f'<div class="filter"><label for="gloss-filter">Search the wordbook</label><input id="gloss-filter" type="search" placeholder="Try “deductible” or “umpire”" autocomplete="off">'
           f'<p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>')
    body = page_hero(trail, "Reference", "Property Claim Wordbook: Terms Defined",
                     f"{len(GLOSSARY)} terms you’ll see in Rhode Island policies, estimates and appraisal awards, defined in plain English.", ph, cta=False) + layout(art, call_box() + list_box("Learn", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property claim wordbook", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Claim Wordbook | ACV, RCV, Umpire & More Defined",
                         "A searchable wordbook of property claim terms: actual cash value, hurricane deductible, ice dam, umpire, storm surge, O&P and more, in plain English.",
                         body, [crumbs_schema(trail), dts], photo=ph), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim notebook", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = (f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>' + p["body"] +
               '<h2>Keep reading</h2>' + related([(o["title"], f'{POST_BASE}{o["slug"]}/') for o in others], "Guide"))
        body = page_hero(trail, "Claim notebook", p["title"], e(p["summary"]), ph, cta=False) + layout(
            art, call_box() + list_box("Learn", LEARN) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_strip()
        art_s = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art_s], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim notebook", path)]
    ph = P("newport-cliff-walk", "newport-mansion", "newport-harbor")
    cards = "".join(
        f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a>'
        f'<div class="post-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides", "The Claim Notebook: Guides for Rhode Island Owners",
                     "Practical guides on policy wording, hurricane deductibles, winter damage and documentation, written from appraisal work.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Claim Notebook | Rhode Island Appraisal Guides",
                         "Guides for Rhode Island property owners on the appraisal provision, hurricane deductibles, ice dams, wind vs. flood and matching materials.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage", "_main": "ItemList"}, itemlist([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo=ph), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    ph = P("ri-state-house", "providence-skyline")
    art = f"""
<figure class="lead-img">{img(P("inspector-clipboard"), sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Older buildings, priced honestly.</strong> Plaster, slate, cedar and period trim cost what they cost.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, condominium associations, property managers, churches, business owners, contractors, public adjusters and attorneys across Rhode Island. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Small state, wide range of claims</h2>
<p>Rhode Island fits a remarkable range of claims into a small area: hurricane and nor’easter damage on the coast, ice dams and snow loads inland, river flooding in the valleys and some of the oldest housing stock in the country. Working statewide means we see every kind of loss the state produces.</p>"""
    body = page_hero(trail, "About", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", ph) + layout(
        art, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Communities", LOC_BASE), ("Free tools", TOOL_BASE), ("The appraisal sequence", PROCESS)])) + cta_strip()
    write(path, document(path, f"About {BRAND}",
                         f"{BRAND} is an independent appraisal and estimating practice focused on the amount of loss on disputed property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo=ph), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    ph = P("consultation-table")
    body = page_hero(trail, "Contact", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", ph, cta=False) + f"""
<section class="sec ink-sec"><div class="wrap split top">
<div class="rv"><p class="tag">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone", "ic", 20)}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail", "ic", 20)}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock", "ic", 20)}<span><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></span></li><li>{ic("pin", "ic", 20)}<span><small>Service area</small><b>All of Rhode Island</b></span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hid="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         f"Request a free review of a disputed property claim. Call or text (844) 537-1427 or email {EMAIL}.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo=ph), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, "thumb", sizes="120px", alt="")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td>'
        f'<td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td>{e(v.get("source", ""))}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web host records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim</li><li>To provide services you ask for</li><li>To keep the site secure and working</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. What you enter isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will say so.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out.</p>
<h2>Your choices</h2><p>To see, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                  "How we collect, use and protect the information you share with us.", "Privacy Policy | Rhode Island Insurance Appraiser",
                  "Privacy policy for Rhode Island Insurance Appraiser: what we collect through forms and calls, how we use it, and the choices you have."),
        TERMS: ("Terms of Use", "Terms of Use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in Rhode Island.</p>
<h2>No professional relationship</h2><p>Reading the site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a Rhode Island attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Rhode Island.</p>""",
                "The terms that apply when you use this website and its tools.", "Terms of Use | Rhode Island Insurance Appraiser",
                "Terms of use for the Rhode Island Insurance Appraiser website: no legal advice, no client relationship from browsing, and limits on tool results."),
        DISCL: ("Disclaimer", "Disclaimer", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Statutes and agencies</h2><p>References to Rhode Island law, the Department of Business Regulation, the FAIR Plan or the bad-faith statute are general descriptions for context, not legal analysis. Verify current law with official sources and a Rhode Island attorney.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a Rhode Island attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>""",
                "Important limits on the information published on this website.", "Disclaimer | Rhode Island Insurance Appraiser",
                "Disclaimer for Rhode Island Insurance Appraiser: general information only, not legal advice, illustrative figures and no guarantee of results."),
        CREDITS: ("Photo Credits", "Photo Credits", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator</th><th scope="col">License</th><th scope="col">Via</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>""",
                    "Sources and licenses for the photographs used on this site.", "Photo Credits | Rhode Island Insurance Appraiser",
                    "Photo credits for Rhode Island Insurance Appraiser: every image is CC0 or public domain, listed here with its creator, license and source."),
    }
    ph = P("ri-farm-field", "colonial-house")
    for path, (crumb, h1, content, lede, title, desc) in legal.items():
        trail = [("Home", "/"), (crumb, path)]
        body = page_hero(trail, "Legal", h1, lede, ph, cta=False) + layout(content, call_box())
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo=ph), 0.3)


def sitemap_pages():
    path = MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Communities", [("All communities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCL), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div class="map-col"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    ph = P("ri-farm-field", "colonial-house")
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", ph, cta=False) + f'<section class="sec"><div class="wrap map-grid">{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}", f"A complete list of pages on {BRAND}: services, Rhode Island communities, free claim tools, guides and legal pages.",
                         body, [crumbs_schema(trail)], photo=ph), 0.3)

    ph = P("storm-surf", "lightning-sky")
    body = (f'<section class="phero tall">{img(ph, "phero-bg", lazy=False, alt="")}<div class="wrap phero-in"><p class="tag">Error 404</p><h1>That page washed out</h1>'
            f'<p class="lede">The page you’re looking for may have moved. Try one of these instead.</p><div class="btn-row"><a class="btn sun" href="/">Home</a>'
            f'<a class="btn glass" href="{SVC_BASE}">Services</a><a class="btn glass" href="{TOOL_BASE}">Free tools</a><a class="btn glass" href="{CONTACT}">Contact</a></div></div></section>')
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on this site.", body, robots="noindex,follow", photo=ph), sitemap=False)


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
// Rhode Island Insurance Appraiser - canonical host guard. Required by index.php and by the first line of every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$ria_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$ria_real  = 'rhodeislandinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$ria_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$ria_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://rhodeislandinsuranceappraiser.com - only on the real domain.
if ($ria_host === 'www.' . $ria_real || ($ria_host === $ria_real && $ria_proto === 'http')) {
    header('Location: https://' . $ria_real . preg_replace('#^(.*/)index\.php(\?|$)#', '$1$2', $ria_uri), true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory URL.
if (preg_match('#^(.*/)index\.php$#', strtok($ria_uri, '?'), $ria_m)) {
    $ria_q = strpos($ria_uri, '?') !== false ? substr($ria_uri, strpos($ria_uri, '?')) : '';
    header('Location: ' . $ria_m[1] . $ria_q, true, 301);
    exit;
}
// Keep the temporary preview domain (and any other host) out of search results.
if ($ria_host !== $ria_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Rhode Island Insurance Appraiser - front controller for the static build.
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
