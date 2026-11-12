#!/usr/bin/env python3
"""Static site generator for kentuckyinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php (guard line + static HTML);
the homepage is home.html, served by the index.php front controller.
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
from tools import TOOLS, PAYOFF_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Kentucky Insurance Appraiser"
HOST = "kentuckyinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
GTM_ID = ""  # e.g. "GTM-XXXXXXX". Empty = no tag manager output.
TODAY = date.today().isoformat()
VER = "20261112a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster

SVC_BASE = "/insurance-appraisal/"
LOC_BASE = "/regions-served/"
TOOL_BASE = "/appraisal-calculators/"
POST_BASE = "/appraisal-articles/"
PROCESS = "/kentucky-appraisal-process/"
FAQ_P = "/insurance-appraisal-questions/"
GLOSS = "/appraisal-terms/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml

LOC_BY = {l["slug"]: l for l in LOCATIONS}


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "party-appraiser-representation": "consultation", "home-insurance-appraisal": "winter-house",
    "commercial-hoa-appraisal": "apartment-building", "roof-hail-appraisal": "hailstones",
    "tornado-wind-appraisal": "tornado-house", "water-damage-appraisal": "flooded-basement",
    "fire-smoke-appraisal": "house-fire-2", "ice-storm-freeze-appraisal": "ice-storm-trees",
    "farm-equine-property-appraisal": "tobacco-barn", "second-look-estimate-review": "desk-calculator",
    "neutral-umpire-services": "paperwork",
}
LOC_PHOTO = {
    "louisville": "louisville-downtown", "lexington": "lexington-horse-farm", "bowling-green": "bowling-green-wku",
    "owensboro": "owensboro-riverfront", "covington": "covington-bridge", "richmond": "horses-graze",
    "elizabethtown": "country-brick", "paducah": "paducah-downtown", "frankfort": "frankfort-capitol",
    "hopkinsville": "tobacco-barns-pair", "pikeville": "mountain-hollow", "ashland": "ohio-river-barge",
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": "calculator", "rcv-acv-holdback-calculator": "team-meeting",
    "roof-measurement-calculator": "roofers", "percentage-deductible-calculator": "storm-over-homes",
    "claim-timeline-builder": "paperwork", "appraisal-readiness-checkup": "consultation",
    "tree-removal-coverage-calculator": "ice-storm-trees",
}
POST_PHOTO = {
    "kentucky-appraisal-clause-basics": "frankfort-capitol", "ice-storm-frozen-pipe-claims": "ice-storm-branches",
    "tornado-claim-first-30-days": "tornado-aerial", "matching-discontinued-materials": "roof-shingle",
    "flood-vs-water-damage-kentucky": "river-flood", "choosing-appraiser-and-umpire": "team-meeting",
    "sinkholes-mine-subsidence-coverage": "mountain-hollow",
}

# ---------------------------------------------------------------- icons (24px line icons, explicit size via CSS)
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "map": '<path d="M1 6v16l7-4 8 4 7-4V2l-7 4-8-4z"/><path d="M8 2v16M16 6v16"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h12"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark(size=40):
    """Brand mark: an estimate's line items sheltered under a roofline, coral 'settled' dot."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="11" fill="#0033A0"/>'
            '<path d="M9.5 24.5L24 11.5l14.5 13" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15.5 30.5h17M15.5 37h9.5" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>'
            '<circle cx="32.5" cy="37" r="3.3" fill="#FF6B4A"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "KY", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-KY", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 120 Kentucky counties.",
        "areaServed": [{"@type": "State", "name": "Kentucky"}] + [{"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Kentucky"}} for l in LOCATIONS],
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Amount of loss", "Property claim estimating", "Hail and wind damage", "Ice storm damage"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
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


# ---------------------------------------------------------------- layout
LEARN = [("Appraisal process guide", PROCESS), ("Appraisal questions", FAQ_P), ("Appraisal terms", GLOSS), ("Guide articles", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All services", SVC_BASE), "two"),
        ("Regions", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All regions served", LOC_BASE), "two"),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE), ""),
        ("Resources", LEARN, None, ""),
    ]


def header():
    nav = ""
    for i, (name, links, allk, cls) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        nav += f'<li class="nav-item"><button type="button" aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "ic chev")}</button><div class="dd {cls}" id="dd-{i}"><ul>{li}</ul></div></li>'
    nav += f'<li><a class="nav-link" href="{ABOUT}">About</a></li><li><a class="nav-link" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc" aria-expanded="false" aria-controls="dp-{i}">{name}{ic("chev", "ic chev")}</button><div class="acc-p" id="dp-{i}" hidden><ul>{li}</ul></div></li>'
    acc += f'<li><a class="top" href="{ABOUT}">About</a></li><li><a class="top" href="{CONTACT}">Contact</a></li>'

    brand = f'<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap head-in">
<a class="brand" href="/" aria-label="{BRAND} — home">{mark()}{brand}</a>
<nav class="nav" aria-label="Main"><ul>{nav}</ul></nav>
<a class="head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div></header>
<div class="scrim" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{mark(36)}{brand}</a><button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="top" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · all 120 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    res = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN) + f'<li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact</a></li>'
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap"><div><h2>Not sure the carrier’s number is right?</h2><p>Send the estimate. We’ll read it line by line and tell you honestly whether appraisal is worth it.</p></div><div class="btns"><a class="btn coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Email the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about"><a class="brand" href="/">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal, estimate review and umpire work for disputed property claims — from the Jackson Purchase to the Big Sandy.</p>
<p class="foot-contact"><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a><span>{ic("clock")}Mon–Fri 8am–6pm ET</span></p></div>
<div><h2 class="fh">Services</h2><ul class="foot-links">{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="fh">Regions</h2><ul class="foot-links">{loc}<li><a href="{LOC_BASE}">All regions</a></li></ul></div>
<div><h2 class="fh">Calculators</h2><ul class="foot-links">{tl}</ul></div>
<div><h2 class="fh">Resources</h2><ul class="foot-links">{res}</ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. {BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Information on this site is general; your policy controls. Outcomes are never guaranteed.</p>
<ul class="foot-links row"><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li><li><a href="/legal-disclaimer/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="/site-index/">Site index</a></li></ul></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("doc")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\nheight="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            "<!-- End Google Tag Manager (noscript) -->\n")


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, trail, schema=None, og_type="website", robots="index,follow", photo="louisville-storm-skyline", main_ref=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, nodes = "WebPage", []
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        nodes.append(n)
    crumbs = crumbs_schema(trail)
    crumbs["@id"] = canonical + "#breadcrumb"
    p = PHOTOS[photo]
    mains = [n["@id"] for n in nodes if n.get("@type") in MAIN_TYPES]
    main = main_ref or (mains[0] if mains else DOMAIN + "/#business")
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": crumbs["@id"]},
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"], "caption": p["alt"]},
        "mainEntity": {"@id": main},
    }
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage, crumbs]) + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw" fetchpriority="high">\n')
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Kentucky">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Kentucky">
<meta name="geo.region" content="US-KY">
<meta name="geo.placename" content="Kentucky">
<meta name="theme-color" content="#0033A0">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400&amp;family=Sora:wght@500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script>document.documentElement.classList.add("js")</script>
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
    """Homepage -> home.html; every other page -> dir/index.php starting with the canonical-host guard."""
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
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(parts) + "</ol></nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<ul class="chips">' + "".join(f"<li><small>{e(k)}</small>{e(v)}</li>" for k, v in facts) + "</ul>"
    c = f'<p class="btns"><a class="btn coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Free claim review</a></p>' if cta else ""
    return (f'<section class="phero"><div class="phero-img">{img(photo, lazy=False, alt="", extra=" data-parallax=\"0.08\"")}</div>'
            f'<div class="wrap phero-in">{crumbs(trail)}<p class="eyebrow on-dark">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ic chev")}</summary><p>{e(a)}</p></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="box box-call"><h2 class="box-t">Free claim conversation</h2><p>Tell us what the carrier offered. We’ll say plainly whether appraisal fits.</p>'
            f'<a class="box-phone" href="tel:{TEL}">{ic("phone")}{PHONE}</a><a class="btn coral full" href="{CONTACT}">Send claim details</a>'
            f'<small>{ic("clock")} Mon–Fri 8am–6pm ET</small></div>')


def link_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow")}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-links">{li}</ul></div>'


def side(*boxes):
    return '<aside class="side"><div class="side-in">' + "".join(boxes) + "</div></aside>"


def cta_strip(h="Carrier’s estimate doesn’t add up?", p="Send it over with your photos. We’ll review it and tell you what we see — no obligation."):
    return (f'<section class="strip"><div class="wrap strip-in reveal"><div><h2>{e(h)}</h2><p>{e(p)}</p></div>'
            f'<p class="btns"><a class="btn coral" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Send the estimate</a></p></div></section>')


def related(items):
    return '<div class="rel">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Tornado / straight-line wind", "Ice storm / freeze", "Burst pipe / water", "Fire / smoke / lightning", "Fallen tree", "Farm / barn", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(fid, heading, sub, page, compact=False, htag="h2"):
    roles = ["Homeowner", "Business owner", "Property manager / HOA", "Farm owner", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Kentucky"]
    rows = f"""<div><label for="{fid}-name">Full name <span aria-hidden="true">*</span></label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone <span aria-hidden="true">*</span></label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="span"><label for="{fid}-email">Email <span aria-hidden="true">*</span></label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div class="span"><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>"""
    if not compact:
        rows += f"""<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div><label for="{fid}-car">Insurance company</label><input id="{fid}-car" name="carrier"></div>
<div class="span"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>"""
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<{htag} class="lead-t">{e(heading)}</{htag}><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">{rows}
<div class="span hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="span"><label class="tick"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="/privacy/">privacy policy</a>.</span></label></div>
<div class="span"><button class="btn coral full" type="submit">Request my free review {ic("arrow")}</button></div>
</div>
<p class="form-msg" role="status"></p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Louisville Metro", "Jefferson, Oldham, Bullitt & Hardin", "louisville-facade", "Spring hail, Ohio Valley windstorms and older brick housing stock. The 2008 Ike windstorm showed how far inland a tropical remnant can reach.", ["louisville", "elizabethtown"]),
    ("The Bluegrass", "Fayette, Scott, Madison & Franklin", "bluegrass-horse-country", "Horse farms, historic downtowns and fast-growing subdivisions. Ice storms and hail lead the claim list, with barns and fencing in the mix.", ["lexington", "richmond", "frankfort"]),
    ("Northern Kentucky", "Kenton, Boone & Campbell", "mainstrasse", "Nineteenth-century row houses, river-town flooding risk and hillsides prone to slippage — plus the same hail tracks that cross the Cincinnati metro.", ["covington"]),
    ("Eastern Kentucky", "Pike, Boyd, Perry & Letcher", "mountain-hollow", "Steep hollows funnel flash floods, as July 2022 showed. Hillside homes, manufactured housing and mine-subsidence questions shape claims here.", ["pikeville", "ashland"]),
    ("Western Kentucky", "McCracken, Daviess, Christian & Graves", "ohio-river-barge", "Tornado country. The December 2021 outbreak and the 2009 ice storm both left their deepest marks west of I-65.", ["paducah", "owensboro", "hopkinsville"]),
    ("South Central", "Warren, Barren & Pulaski", "bowling-green-wku", "Karst ground, sinkholes and fast growth around Bowling Green, which took an overnight tornado hit in December 2021.", ["bowling-green"]),
]

STORMS = [
    ("1937", "Ohio River flood", "Record river levels flooded Louisville, Paducah and much of the Ohio Valley, and changed how river towns built.", "river-flood"),
    ("1974", "April 3 Super Outbreak", "A wave of tornadoes crossed the state, including the Brandenburg and Louisville tornadoes.", "lightning"),
    ("2008", "Ike windstorm", "Hurricane Ike’s remnants brought hurricane-force gusts to the Louisville area and a long statewide cleanup.", "storm-over-homes"),
    ("2009", "January ice storm", "Heavy ice brought down trees and power lines across western Kentucky, Paducah included.", "ice-storm-branches"),
    ("2021", "December tornadoes", "Overnight tornadoes struck Mayfield, Dawson Springs and Bowling Green in one of the state’s worst disasters.", "tornado-aerial"),
    ("2022", "Eastern Kentucky floods", "Flash flooding in late July swept through hollows in Perry, Knott, Breathitt and Letcher counties.", "river-flood"),
]


def home():
    services_rows = "".join(
        f'<a class="srow" href="{SVC_BASE}{s["slug"]}/"><span class="srow-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 96px, 120px", alt="")}</span>'
        f'<span class="srow-b"><small>{i + 1:02d}</small><strong>{e(s["name"])}</strong><span>{e(s["short"])}</span></span>{ic("arrow")}</a>'
        for i, s in enumerate(SERVICES))
    steps = "".join(f'<li class="step"><span class="dot">{i + 1}</span><h3>{e(n)}</h3><p>{e(t)}</p></li>' for i, (n, t) in enumerate(PROCESS_STEPS))
    regions = "".join(
        f'<article class="rcard"><div class="rcard-img">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</div><div class="rcard-b">'
        f'<small>{e(counties)}</small><h3>{e(n)}</h3><p>{e(t)}</p><p class="rcard-l">' + " ".join(f'<a href="{loc_path(LOC_BY[c])}">{e(LOC_BY[c]["city"])}</a>' for c in cs) + '</p></div></article>'
        for n, counties, ph, t, cs in REGIONS)
    storms = "".join(
        f'<li class="storm">{img(ph, sizes="(max-width:700px) 80vw, 320px", alt="")}<div><b>{y}</b><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for y, t, d, ph in STORMS)
    tools = "".join(
        f'<a class="tcard" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 25vw", alt="")}<i>{e(t["kind"])}</i></span>'
        f'<span class="tcard-b"><strong>{e(t["name"])}</strong><span>{e(t["short"])}</span></span></a>' for t in TOOLS)
    posts = "".join(
        f'<article class="gcard"><a class="gcard-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a>'
        f'<div class="gcard-b"><small>{p["read"]} read</small><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])
    cities = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}<small>{e(l["county"])}</small></a></li>' for l in LOCATIONS)

    home_faqs = [
        ("What does a Kentucky Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, take unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles the whole claim for a fee. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate the rest of the claim and we don’t give legal advice."),
        ("When is it worth calling a Kentucky Insurance Appraiser?", "When coverage has been accepted, you have the carrier’s itemized estimate, and the gap to your contractor’s number is meaningful — often more than about 10 percent or several thousand dollars."),
        ("Does appraisal decide whether my claim is covered?", "No. Appraisal sets the amount of loss. Coverage disputes, denials and bad-faith questions belong with a Kentucky attorney, and the Kentucky Department of Insurance takes consumer complaints."),
        ("What does it cost?", "Each side usually pays its own appraiser and splits the umpire. Our fee is put in writing before work starts, and the first conversation is free."),
        ("Do you cover my county?", "Yes. We take appraisal and review work in all 120 Kentucky counties, from Paducah and Hopkinsville to Lexington, Covington, Pikeville and Ashland."),
    ]

    body = f"""
<section class="hero">
<div class="hero-img">{img("louisville-storm-skyline", lazy=False, alt="", extra=' data-parallax="0.1"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow on-dark">Statewide · all 120 counties</p>
<h1>Kentucky Insurance Appraiser for claims that came up <em>short</em></h1>
<p class="lede">Your insurer agreed the damage is covered — then sent a number that won’t pay for the repair. Kentucky Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal clause in your policy.</p>
<p class="btns"><a class="btn coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="#services">See our services {ic("arrow")}</a></p>
<ul class="hero-ticks"><li>{ic("check")}Your named party appraiser</li><li>{ic("check")}Line-item estimates priced locally</li><li>{ic("check")}Homes, farms, HOAs &amp; commercial</li></ul>
</div>
<div class="hero-form">{lead_form("h", "Get a free claim review", "A few details and we’ll call you back, usually within one business day.", "/ (hero)", compact=True)}</div>
</div>
</section>

<section class="triage"><div class="wrap"><ol class="triage-in" data-stagger>
<li><span>1</span><div><h2>Is coverage accepted?</h2><p>Appraisal settles <em>how much</em>, not <em>whether</em>. If the claim was denied, start with a Kentucky attorney.</p></div></li>
<li><span>2</span><div><h2>Is the gap real?</h2><p>Compare both estimates in the <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> — fees included.</p></div></li>
<li><span>3</span><div><h2>Is a deadline close?</h2><p>Map proof-of-loss, holdback and suit dates with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a>.</p></div></li>
</ol></div></section>

<section class="sec intro"><div class="wrap intro-in">
<div class="reveal">
<p class="eyebrow">Why owners call us</p>
<h2>A Kentucky Insurance Appraiser works on one question: the amount of loss</h2>
<p>Most underpaid Kentucky claims aren’t denied. They’re just short — a roof slope left off, a steep charge missing, siding that can’t be matched, a code item nobody priced. Kentucky Insurance Appraiser exists for the space between “covered” and “paid in full.”</p>
<p>We inspect and measure the property ourselves, price the repair for the county it sits in, and put every difference with the carrier’s estimate in plain English. When appraisal isn’t the right tool, we say so on the first call.</p>
<ul class="ticks"><li>{ic("check")}<span><b>Independent scope.</b> Built from our own inspection, never an edited copy of the carrier’s estimate.</span></li>
<li>{ic("check")}<span><b>Defensible numbers.</b> Priced to hold up in front of an umpire, which is what actually moves an award.</span></li>
<li>{ic("check")}<span><b>Honest triage.</b> If you need an attorney or a simple supplement instead, you’ll hear it from us.</span></li></ul>
<p class="btns"><a class="btn blue" href="{ABOUT}">How we work {ic("arrow")}</a></p>
</div>
<div class="glance counters reveal">
<p class="glance-t">Kentucky Insurance Appraiser at a glance</p>
<dl>
<div><dt><b data-count="120">120</b></dt><dd>Kentucky counties served</dd></div>
<div><dt><b data-count="{len(SERVICES)}">{len(SERVICES)}</b></dt><dd>Appraisal &amp; estimating services</dd></div>
<div><dt><b data-count="{len(TOOLS)}">{len(TOOLS)}</b></dt><dd>Free calculators, nothing stored</dd></div>
<div><dt><b>2 of 3</b></dt><dd>Signatures that make an award binding</dd></div>
</dl>
<figure>{img("lexington-horse-farm", sizes="(max-width:900px) 100vw, 440px")}</figure>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head reveal"><p class="eyebrow">Services</p><h2>What Kentucky Insurance Appraiser handles</h2><p>Eleven services built around one job: a valuation of your loss that holds up. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="srows" data-stagger>{services_rows}</div>
<p class="center"><a class="btn line" href="{SVC_BASE}">Compare all services {ic("arrow")}</a></p>
</div></section>

<section class="sec deep"><div class="wrap gapsec">
<div class="reveal"><p class="eyebrow on-dark">Quick check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. A wide gap is worth a conversation with a Kentucky Insurance Appraiser. A narrow one may close faster with a documented supplement.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds appraiser and umpire fees and shows the break-even point.</p></div>
<div class="reveal">{PAYOFF_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head reveal"><p class="eyebrow">The process</p><h2>Seven steps from stuck claim to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how Kentucky Insurance Appraiser moves a file from first call to award.</p></div>
<ol class="steps">{steps}</ol>
<p class="center"><a class="link" href="{PROCESS}">Read the full Kentucky appraisal process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head left reveal"><p class="eyebrow">Six claim climates</p><h2>Kentucky Insurance Appraiser coverage, region by region</h2><p>Tornado alley in the west, karst in the south, ice in the Bluegrass, flash floods in the mountains. Each region writes a different kind of estimate.</p></div>
<div class="rcards" data-stagger>{regions}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left reveal"><p class="eyebrow">Storm memory</p><h2>The storms that shaped Kentucky claims</h2><p>Every Kentucky Insurance Appraiser file is read against this history: what failed, what got missed, and what estimates tend to leave out after a big event.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head reveal"><p class="eyebrow">Free &amp; private</p><h2>Free calculators from a Kentucky Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser — nothing you type is sent or stored.</p></div>
<div class="tcards" data-stagger>{tools}</div>
</div></section>

<section class="sec"><div class="wrap myth">
<div class="reveal"><p class="eyebrow">Straight talk</p><h2>Myths a Kentucky Insurance Appraiser hears every week</h2><p>A few common beliefs that cost owners money — and what is usually true instead. Your policy language always controls.</p></div>
<dl class="myths" data-stagger>
<div><dt>{ic("x")}“Appraisal means suing my insurer.”</dt><dd>{ic("check")}It’s a contract process inside your policy, not a lawsuit. It decides the amount of loss only.</dd></div>
<div><dt>{ic("x")}“The adjuster’s estimate is final.”</dt><dd>{ic("check")}It’s the carrier’s opening valuation. Supplements and, when needed, appraisal exist because estimates miss things.</dd></div>
<div><dt>{ic("x")}“My contractor can be my appraiser.”</dt><dd>{ic("check")}Most policies require an impartial or independent appraiser. A contractor with a stake in the repair can put the award at risk.</dd></div>
<div><dt>{ic("x")}“Appraisal always pays off.”</dt><dd>{ic("check")}Not when the gap is small. Fees can eat a narrow difference — run the payoff estimator first.</dd></div>
</dl>
</div></section>

<section class="sec tint"><div class="wrap faqsec">
<div class="reveal"><p class="eyebrow">Questions</p><h2>Asked of every Kentucky Insurance Appraiser</h2><p>Short answers about how appraisal works, what it costs and when it’s the wrong move.</p><p class="btns"><a class="btn blue" href="{FAQ_P}">All appraisal questions {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Appraisal terms</a></p></div>
<div class="reveal">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head reveal"><p class="eyebrow">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical articles from Kentucky Insurance Appraiser on policy wording, documentation and claim strategy.</p></div>
<div class="gcards" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All guide articles {ic("arrow")}</a></p>
</div></section>

<section class="pcta"><div class="pcta-img">{img("storm-clouds", alt="", extra=' data-parallax="0.16"')}</div><div class="wrap pcta-in reveal">
<p class="eyebrow on-dark">Before you sign off</p><h2>The best time to check a settlement is before you accept it</h2>
<p>A short review by a Kentucky Insurance Appraiser can keep you from closing a claim that won’t cover the repair.</p>
<p class="btns"><a class="btn coral" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost-l" href="{CONTACT}">Send your estimate</a></p></div></section>

<section class="sec"><div class="wrap where">
<div class="reveal"><p class="eyebrow">Where we work</p><h2>Kentucky Insurance Appraiser service areas</h2><p>Kentucky Insurance Appraiser takes work in every county. These are the communities where our files come from most often. Don’t see yours? <a href="{CONTACT}">Ask us</a> — the answer is almost certainly yes.</p>
<ul class="contact-lines"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri, 8am–6pm ET</span></li><li>{ic("map")}<span>All 120 Kentucky counties</span></li></ul></div>
<ul class="city-list" data-stagger>{cities}</ul>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Kentucky Insurance Appraiser: independent appraisal, estimate review and umpire work for underpaid hail, tornado, ice storm, water and fire claims.",
                        body, [("Home", "/")], [faq_schema(home_faqs)], photo="louisville-storm-skyline", main_ref=DOMAIN + "/#business", body_cls="has-hero"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap cols"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
{side(call_box(), link_box("All services", items, path), link_box("Regions we serve", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All regions", LOC_BASE)]))}</div>
{cta_strip()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                                          "areaServed": {"@type": "State", "name": "Kentucky"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, trail, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="icard" href="{SVC_BASE}{s["slug"]}/"><span class="icard-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span>'
        f'<span class="icard-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><span>{e(s["short"])}</span></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Kentucky Property Owners",
                     "From a single estimate review to full party-appraiser representation and neutral umpire work, every service is built around an accurate, defensible valuation of the loss.", "roofing-crew") + f"""
<section class="sec"><div class="wrap"><div class="icards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faqsec"><div class="reveal"><p class="eyebrow">Where to start</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days — and plenty of disputes close right there.</p><p class="btns"><a class="btn blue" href="{SVC_BASE}second-look-estimate-review/">About estimate reviews {ic("arrow")}</a></p></div>
<div class="reveal">{faq_block([("Can I hire you for just one step?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial property?", "Yes — barns, equine facilities, retail, office, warehouses, churches, apartments and condominium associations, as well as houses."), ("Is appraisal only for hail claims?", "No. It applies to any covered loss where the amount is disputed: wind, ice, water, fire, fallen trees and more.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Kentucky | All Services",
                             "Kentucky insurance appraisal services: party-appraiser representation, estimate review, roof, tornado, ice storm, water, fire, farm and umpire work.",
                             body, trail, [{"@type": "CollectionPage"}, item_list(items)], photo="roofing-crew"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Regions served", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        hoods = "".join(f"<li>{e(n)}</li>" for n in l["neighborhoods"])
        perils = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        storms = "".join(f'<li><b>{e(y)}</b><span>{e(t)}</span></li>' for y, t in l["storms"])
        snap = f"""<section class="snap"><h2>{e(l["city"])} at a glance</h2>
<dl class="snap-facts"><div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Region</dt><dd>{e(l["region"])}</dd></div><div><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div></dl>
<h3>Local claim risks</h3><ul class="tags">{perils}</ul>
<h3>Neighborhoods and nearby communities</h3><ul class="tags light">{hoods}</ul>
<h3>Weather history</h3><ol class="mini-tl">{storms}</ol></section>"""
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        near = related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', l["h1"], e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap cols"><article class="prose">{snap}
{l["body"]}
<h2>Appraisal services available in {e(l["city"])}</h2><p>Every {BRAND} service is available to owners in {e(l["city"])} and across {e(l["county"])}, including:</p><ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby regions</h2>{near}
</article>
{side(call_box(), link_box("Regions served", items, path), link_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]]))}</div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see — and whether appraisal makes sense.")}"""
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Kentucky", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"},
                                          "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Kentucky"}}, "url": DOMAIN + path,
                                          "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, trail, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Regions served", LOC_BASE)]
    cards = "".join(
        f'<a class="icard" href="{loc_path(l)}"><span class="icard-img">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</span>'
        f'<span class="icard-b"><small>{e(l["region"])} · {e(l["county"])}</small><h2>{e(l["city"])}</h2><span>{e(l["lede"])}</span></span></a>' for l in LOCATIONS)
    regions = "".join(f'<div class="rmini"><h3>{e(n)}</h3><p class="small">{e(c)}</p><p>{e(t)}</p></div>' for n, c, _ph, t, _cs in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 120 Kentucky Counties",
                     f"{BRAND} takes work statewide — from the Mississippi River bluffs to the Big Sandy. These pages cover the cities where our files come from most often.", "bluegrass-horse-country") + f"""
<section class="sec"><div class="wrap"><div class="icards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left reveal"><p class="eyebrow">Regions</p><h2>How claims differ across Kentucky</h2><p>The same policy wording plays out differently in a Paducah ranch, a Covington row house and a Pike County hillside home.</p></div><div class="rminis" data-stagger>{regions}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Kentucky county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Kentucky Regions We Serve | Statewide Claim Appraisal",
                             "Insurance appraisal in all 120 Kentucky counties, including Louisville, Lexington, Bowling Green, Owensboro, Covington, Paducah and Pikeville.",
                             body, trail, [{"@type": "CollectionPage"}, item_list(items)], photo="bluegrass-horse-country"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec toolsec"><div class="wrap">{t["markup"]}
<p class="fine">For planning only. Results depend on what you enter and on your policy’s terms. They are not a quote, an appraisal or legal advice. Nothing you type leaves your browser.</p></div></section>
<div class="wrap cols"><article class="prose">{t["explain"]}
<h2>Questions about the {e(t["name"].lower())}</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
{side(call_box(), link_box("All calculators", items, path))}</div>
{cta_strip("Want a professional to check the math?", "Send the carrier’s estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication",
                                          "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
                                          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, trail, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(
        f'<a class="tcard" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<i>{e(t["kind"])}</i></span>'
        f'<span class="tcard-b"><h2>{e(t["name"])}</h2><span>{e(t["short"])}</span></span></a>' for t in TOOLS)
    order = "".join(f'<li><a href="{TOOL_BASE}{s}/">{e(n)}</a> — {e(w)}</li>' for s, n, w in [
        ("claim-timeline-builder", "Claim timeline builder", "so no deadline slips"),
        ("roof-measurement-calculator", "Roof measurement calculator", "to check squares and pitch"),
        ("percentage-deductible-calculator", "Percentage deductible calculator", "to see what the deductible takes"),
        ("rcv-acv-holdback-calculator", "RCV & ACV holdback calculator", "to understand the first check"),
        ("tree-removal-coverage-calculator", "Tree removal coverage calculator", "after an ice storm or windstorm"),
        ("appraisal-payoff-estimator", "Appraisal payoff estimator", "to test the dispute with fees"),
        ("appraisal-readiness-checkup", "Appraisal readiness checkup", "before you demand appraisal")])
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Kentucky Owners",
                     "Seven calculators and planners drawn from real appraisal work. Check the carrier’s math, see what you’re owed and decide on next steps — no sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards three" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faqsec"><div class="reveal"><p class="eyebrow">A sensible order</p><h2>Using the calculators together</h2><ol class="order">{order}</ol></div><div class="reveal">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Kentucky Owners",
                              "Seven free claim calculators: appraisal payoff, RCV/ACV holdback, roof measurement, percentage deductible, tree removal, timelines and readiness.",
                              body, trail, [{"@type": "CollectionPage"}, item_list(items)], photo="calculator"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    stepper = "".join(f'<li><span>{i + 1}</span><b>{e(n)}</b></li>' for i, (n, _t) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "The Kentucky Insurance Appraisal Process, Step by Step",
                     "Seven stages from the first disagreement to a signed award — what happens, who does what and where claims most often go wrong.", "paperwork",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "Any 2 of 3 sign")]) + f"""
<div class="wrap cols"><article class="prose"><ol class="stepper">{stepper}</ol>{PROCESS_BODY}</article>
{side(call_box(), link_box("Resources", LEARN, path))}</div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Kentucky", "description": "The seven stages of a property insurance appraisal under a typical policy appraisal clause.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": DOMAIN + path} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Kentucky Insurance Appraisal Process | 7 Steps",
                         "Step-by-step guide to the Kentucky insurance appraisal process: written demand, party appraisers, umpire selection, negotiation and the binding award.",
                         body, trail, [howto], photo="paperwork"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal questions", path)]
    jump = "".join(f'<li><a href="#q-{i}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, f"{len(allq)} answers", "Insurance Appraisal Questions From Kentucky Owners",
                     "Plain answers about the appraisal process, costs, timing and how Kentucky rules fit in — grouped by topic.", "living-room") + f"""
<div class="wrap cols"><article class="prose"><ul class="jump">{jump}</ul>{groups}</article>
{side(call_box(), link_box("Resources", LEARN, path))}</div>{cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Kentucky Owners’ Questions",
                         "Answers to common Kentucky insurance appraisal questions: how it works, costs and fees, timing and deadlines, state specifics and working with us.",
                         body, trail, [faq_schema(allq)], photo="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Appraisal terms", path)]
    terms = "".join(f'<div><dt id="t-{i}">{e(t)}</dt><dd>{e(d)}</dd></div>' for i, (t, d) in enumerate(GLOSSARY))
    body = page_hero(trail, "Reference", "Insurance Appraisal Terms, Defined in Plain English",
                     f"{len(GLOSSARY)} words you’ll meet in policies, estimates and appraisal awards. Type in the box to filter.", "desk-calculator", cta=False) + f"""
<div class="wrap cols"><article class="prose"><div class="search"><label for="term-search">Search the terms</label><input id="term-search" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><output id="term-count" for="term-search">{len(GLOSSARY)} terms</output></div><dl class="terms">{terms}</dl></article>
{side(call_box(), link_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "url": f"{DOMAIN}{path}#t-{i}"} for i, (t, d) in enumerate(GLOSSARY)]}
    write(path, document(path, "Insurance Appraisal Terms | Claim Glossary A–Z",
                         "Plain-English glossary of insurance appraisal terms: actual cash value, holdback, umpire, overhead and profit, matching, mine subsidence and more.",
                         body, trail, [dts], photo="desk-calculator"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guide articles", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap cols"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
{side(call_box(), link_box("Resources", LEARN), link_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]]))}</div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
               "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["keyword"]}
        write(path, document(path, p["seo"], p["desc"], body, trail, [art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guide articles", path)]
    cards = "".join(
        f'<article class="gcard"><a class="gcard-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a>'
        f'<div class="gcard-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guide articles", "Insurance Appraisal Guides for Kentucky Property Owners",
                     "Practical articles on policy wording, documentation and claim strategy — ice storms, tornadoes, matching, flood and ground movement.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="gcards" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Appraisal Guides | Kentucky Claim Articles",
                         "Guides for Kentucky property owners on the appraisal clause, ice storm and tornado claims, matching, flood vs. water damage and choosing an umpire.",
                         body, trail, [{"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About us", path)]
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "Estimators and appraisers who think a property claim should be paid on what the damage actually costs — documented so clearly that everyone at the table can see it.", "team-meeting") + f"""
<div class="wrap cols"><article class="prose">
<figure class="wide-img">{img("consultation", sizes="(max-width:1080px) 100vw, 760px")}<figcaption>A claim review starts with the policy, the carrier’s estimate and your photos.</figcaption></figure>
<h2>Why we only do appraisal work</h2>
<p>Many claim professionals do a little of everything. We chose one lane. {BRAND} works on the amount of loss — as your party appraiser, as a reviewer before a dispute escalates, or as a neutral umpire on panels where we represent neither side. Our process, tools and documentation standards are built around answering that one question well.</p>
<h2>How a file moves through our hands</h2>
<ol><li><strong>Read first.</strong> Policy, declarations page, the carrier’s estimate and correspondence — before we form any opinion.</li>
<li><strong>Inspect and measure.</strong> Our own scope, photographed and measured, never a markup of someone else’s estimate.</li>
<li><strong>Price locally.</strong> Line items priced for the Kentucky market the property sits in.</li>
<li><strong>Explain the gap.</strong> A plain-English comparison of every difference with the carrier’s number.</li>
<li><strong>Carry it through.</strong> Work with the other appraiser and, if needed, present to the umpire.</li></ol>
<h2>Who calls us</h2>
<p>Homeowners and condo owners, landlords, HOA boards, property managers, churches, business owners, farm and equine operations, contractors, public adjusters and attorneys across Kentucky. On any one claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t promise results — no honest appraiser can. Coverage disputes and bad-faith questions go to a Kentucky attorney; consumer complaints about an insurer go to the Kentucky Department of Insurance.</p>
<h2>Statewide on purpose</h2>
<p>Kentucky’s weather changes fast across 400 miles: tornadoes in the Purchase, karst sinkholes around Bowling Green, ice storms in the Bluegrass, flash floods in the eastern hollows. Working statewide means we see every kind of loss the state produces and price each one with local knowledge.</p>
</article>{side(call_box(), link_box("Explore", [("Our services", SVC_BASE), ("Regions served", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process", PROCESS)]))}</div>{cta_strip()}"""
    write(path, document(path, f"About {BRAND} | How We Work",
                         f"{BRAND} is an independent appraisal and estimating practice focused on the amount of loss in disputed Kentucky property claims.",
                         body, trail, [{"@type": "AboutPage"}], photo="team-meeting"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="reveal"><h2>Reach us directly</h2>
<ul class="contact-cards"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("map")}<div><small>Service area</small><b>All 120 Kentucky counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The carrier’s full, itemized estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and your contractor’s estimate</span></li></ul></div>
<div class="reveal">{lead_form("c", "Tell us about your claim", "Free review. No obligation. Usually a reply within one business day.", path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Get a free review of a disputed Kentucky property claim. Call or text (844) 537-1427 or email info@kentuckyinsuranceappraiser.com.",
                         body, trail, [{"@type": "ContactPage"}], photo="consultation"), 0.8)

    lic = {"cc0": "CC0 1.0 (public domain dedication)", "pdm": "Public Domain Mark"}
    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"thumb\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · {e(v["source_name"])}</small></td><td>{lic.get(v["license"], v["license"])}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in sorted(PHOTOS.items()))
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        "/privacy/": ("Privacy Policy", "Privacy Policy | Kentucky Insurance Appraiser", "How Kentucky Insurance Appraiser collects, uses and protects information you share through this website, forms, calls and email.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share — such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run entirely in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add an analytics tag, it will be used to understand site traffic in aggregate.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete what you’ve shared by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        "/terms/": ("Terms of Use", "Terms of Use | Kentucky Insurance Appraiser", "The terms that apply when you use the Kentucky Insurance Appraiser website, its free calculators and its contact forms.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Kentucky.</p>
<h2>No client relationship</h2><p>Reading the site, using a calculator or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Talk to a licensed Kentucky attorney about legal questions.</p>
<h2>Calculators</h2><p>Calculators give planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on the <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the Commonwealth of Kentucky.</p>"""),
        "/legal-disclaimer/": ("Disclaimer", "Legal Disclaimer | Kentucky Insurance Appraiser", "Important limits on the information published on this site: general education only, no legal advice, no public adjusting and no guaranteed results.", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and its endorsements.</p>
<h2>Not legal advice, not public adjusting</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, replacement-cost recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is close, talk to a Kentucky attorney promptly.</p>
<h2>Statutes and agencies</h2><p>References to Kentucky law, the Kentucky Department of Insurance, the Kentucky FAIR Plan or past storms are for context only. Check current law and facts with official sources.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>"""),
        "/photo-credits/": ("Photo Credits", "Photo Credits & Licenses | Kentucky Insurance Appraiser", "Sources and licenses for every photograph on Kentucky Insurance Appraiser: CC0 and public-domain images from rawpixel, StockSnap and more.", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or marked as a <strong>public-domain</strong> work (including photos from U.S. government sources and the Library of Congress collection). Attribution isn’t legally required, but we credit each creator here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="scroll-x"><table class="credits"><thead><tr><th scope="col">Photo</th><th scope="col">Title / creator / source</th><th scope="col">License</th><th scope="col">Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (h1, title, desc, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, e(desc), "capitol-plaza", cta=False) + f'<div class="wrap cols"><article class="prose narrow">{content}</article>{side(call_box())}</div>'
        write(path, document(path, title, desc, body, trail, photo="capitol-plaza"), 0.3)


def index_pages():
    path = "/site-index/"
    trail = [("Home", "/"), ("Site index", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", ABOUT), ("Contact us", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Regions served", [("All regions", LOC_BASE)] + [(f'{l["city"]}, KY', loc_path(l)) for l in LOCATIONS]),
        ("Free calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", "/privacy/"), ("Terms of use", "/terms/"), ("Disclaimer", "/legal-disclaimer/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="ixcol"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on {BRAND}, in one place.", "capitol-plaza", cta=False) + f'<section class="sec"><div class="wrap ix" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"A complete list of pages on {BRAND}: services, Kentucky regions, free claim calculators, guides and legal pages.", body, trail, photo="capitol-plaza"), 0.3)

    body = (f'<section class="phero nf"><div class="phero-img">{img("tornado-heath", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="eyebrow on-dark">Error 404</p>'
            f'<h1>That page went down with the last storm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p>'
            f'<p class="btns"><a class="btn coral" href="/">Home</a><a class="btn ghost-l" href="{SVC_BASE}">Services</a><a class="btn ghost-l" href="{TOOL_BASE}">Calculators</a><a class="btn ghost-l" href="{CONTACT}">Contact</a></p></div></section>')
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on Kentucky Insurance Appraiser. Try the homepage, services or free calculators.", body, [("Home", "/")], robots="noindex,follow", photo="tornado-heath"), sitemap=False)


# ---------------------------------------------------------------- root files
GUARD_PHP = r"""<?php
// Kentucky Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$kia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$kia_real  = 'kentuckyinsuranceappraiser.com';
$kia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$kia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// /dir/index.php (or /index.php) duplicates /dir/: drop the file name, keeping any query string.
$kia_path  = (string) strtok($kia_uri, '?');
$kia_query = strpos($kia_uri, '?') !== false ? substr($kia_uri, strpos($kia_uri, '?')) : '';
$kia_clean = preg_replace('#(^|/)index\.php$#', '$1', $kia_path);
$kia_wrong = ($kia_host === 'www.' . $kia_real || ($kia_host === $kia_real && $kia_proto === 'http'));
// One 301 to https://kentuckyinsuranceappraiser.com for www. / plain http (real domain only) and for index.php URLs.
if ($kia_wrong) {
    header('Location: https://' . $kia_real . $kia_clean . $kia_query, true, 301);
    exit;
}
if ($kia_clean !== $kia_path) {
    header('Location: ' . $kia_clean . $kia_query, true, 301);
    exit;
}
// Keep preview/temporary hosts out of search results.
if ($kia_host !== $kia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Kentucky Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (running a directory's index.php)
// and routes "/" and unknown paths here.
require_once __DIR__ . '/_guard.php';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode((string) strtok($uri, '?'));
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
if ($path === '/') {
    readfile(__DIR__ . '/home.html');
    exit;
}
// Directory without trailing slash: 301 to add it.
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.php')) {
    $q = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    header('Location: ' . $path . '/' . $q, true, 301);
    exit;
}
// Directory URL that reached the front controller: run that page.
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.php')) {
    include __DIR__ . $path . 'index.php';
    exit;
}
http_response_code(404);
readfile(__DIR__ . '/404.html');
"""


def root_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        xml.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>")
    xml.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(xml) + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\nDisallow: /404.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, "_guard.php"), "w") as f:
        f.write(GUARD_PHP)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private", ".DS_Store"))
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    index_pages()
    root_files()
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
