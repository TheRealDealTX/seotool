#!/usr/bin/env python3
"""Static site generator for southdakotainsuranceappraiser.com.

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
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, PAYOFF_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "South Dakota Insurance Appraiser"
HOST = "southdakotainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster
GTM_ID = ""         # e.g. "GTM-XXXXXXX". Empty = no tag output.

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraiser-services/"
LOC_BASE = "/cities-we-serve/"
TOOL_BASE = "/policyholder-calculators/"
POST_BASE = "/storm-claim-articles/"
PROCESS = "/inside-the-appraisal-process/"
FAQ_P = "/appraisal-questions-answered/"
GLOSS = "/insurance-appraisal-glossary/"
ABOUT = "/company-profile/"
CONTACT = "/get-a-claim-review/"
PRIVACY = "/site-privacy/"
TERMS = "/site-conditions/"
DISCLAIM = "/appraiser-disclaimer/"
SITEMAP = "/page-map/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-appraiser/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {k: v["alt"] for k, v in PHOTOS.items()}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appraiser": "consult-table", "homeowners-claim-appraiser": "home-porch",
    "commercial-hoa-claim-appraiser": "apartments", "hail-roof-damage-appraiser": "hail-roof",
    "tornado-straight-line-wind-appraiser": "tornado-damage", "water-damage-claim-appraiser": "water-ceiling",
    "fire-smoke-damage-appraiser": "house-fire", "black-hills-wildfire-claim-appraiser": "wildfire",
    "blizzard-ice-snow-load-appraiser": "snow-house", "farm-ranch-outbuilding-appraiser": "farm-buildings",
    "insurance-estimate-second-opinion": "estimate-desk", "umpire-and-neutral-appraiser": "meeting",
}
LOC_PHOTO = {
    "sioux-falls": "sioux-falls", "rapid-city": "rapid-city", "aberdeen": "prairie-farm", "brookings": "lake-sunrise",
    "watertown": "lake-home", "mitchell": "grain-bins", "yankton": "river-storm", "pierre": "river-bluffs",
    "huron": "prairie-storm", "spearfish": "spearfish-canyon", "vermillion": "river-flood", "sturgis": "sturgis-main",
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": "calculator", "depreciation-recovery-calculator": "paperwork",
    "roof-slope-factor-calculator": "roofer", "hail-percentage-deductible-calculator": "hailstones",
    "appraisal-calendar-builder": "calendar-desk", "claim-file-readiness-grader": "inspector",
    "coinsurance-penalty-calculator": "metal-barn",
}
POST_PHOTO = {
    "how-the-appraisal-clause-works-in-south-dakota": "policy-review", "documenting-hail-damage-after-a-prairie-storm": "hail-roof",
    "derecho-claims-straight-line-wind-versus-tornado": "shelf-cloud", "black-hills-wildfire-smoke-claim-checklist": "wildfire",
    "who-to-call-appraiser-adjuster-or-attorney": "meeting", "coinsurance-and-farm-building-claims": "metal-barn",
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
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="i"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=40):
    """Brand mark: prairie horizon with a rising sun, in the brand blue and gold."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#0074A8"/>'
            '<path d="M13 27a11 11 0 0 1 22 0z" fill="#FFC400"/>'
            '<path d="M8 27h32" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M12 32.5h24M17 37.5h14" stroke="#9fd3ea" stroke-width="2.6" stroke-linecap="round"/></svg>')


def brand_link(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>South Dakota</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "SD", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-SD", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across South Dakota.",
        "areaServed": [{"@type": "State", "name": "South Dakota"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Derecho and wind damage", "Wildfire claims", "Coinsurance"],
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
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraiser services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All cities we serve", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", [("Inside the appraisal process", PROCESS), ("Appraisal questions answered", FAQ_P), ("Appraisal glossary", GLOSS), ("Storm claim articles", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])}</a></li>'
        wide = " wide" if len(links) > 6 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{ABOUT}">About</a></li><li><a class="top-link" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap head-in">
{brand_link()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn sun head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
<a class="nojs-menu" href="{SITEMAP}">Menu</a>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link("brand drawer-brand")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="{CONTACT}">Request a claim review</a><small>Mon–Fri, 8am–6pm Central · All 66 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Claim paid short? Put the numbers in front of an appraiser.</h2><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line-light" href="{CONTACT}">Send your estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand_link("brand foot-brand")}
<p>Independent appraisal, estimate review and umpire services for disputed property claims in every corner of South Dakota, East River and West River.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri, 8am–6pm Central</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Cities</h3><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h3>Calculators</h3><ul>{tl}</ul></div>
<div><h3>Resources</h3><ul><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">Questions answered</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Articles</a></li><li><a href="{ABOUT}">Company profile</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{SITEMAP}">Page map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, we do not give legal advice and we do not act as public adjusters. Site content is general information; your policy controls. Outcomes depend on the facts of each claim and are never guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<nav class="callbar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("doc")} Free review</a></nav>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n})(window,document,'script','dataLayer','"
            + GTM_ID + "');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-home", body_cls=""):
    canonical = DOMAIN + path if not path.endswith(".html") else DOMAIN + "/"
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
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
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
    main = [n["@id"] for n in extra if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across South Dakota">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across South Dakota">
<meta name="geo.region" content="US-SD">
<meta name="geo.placename" content="South Dakota">
<meta name="theme-color" content="#06324A">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gabarito:wght@500;600;700;800&family=Rethink+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
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


GUARD_LINE = "<?php require_once dirname(__DIR__, {n}) . '/_guard.php'; ?>\n"


def write(path, content, priority=0.6, sitemap=True):
    """'/' -> home.html; '/x.html' -> x.html; '/dir/' -> dir/index.php with the guard line on top."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
        content = GUARD_LINE.format(n=rel.count("/")) + content
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
        f = '<dl class="facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero">{img(photo, "phero-bg", lazy=False, alt="")}<div class="wrap phero-in">{crumbs(trail)}<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs, cls="faq"):
    return f'<div class="{cls}">' + "".join(f'<details><summary>{e(q)}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn ink" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Not sure the carrier’s number is right?", p="Send the estimate and your photos. We’ll review it and tell you what we see."):
    return f"""<section class="strip"><div class="wrap strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn ink" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def related(items, kind):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(kind)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for n, p in items) + "</div>"


LOSSES = ["Hail", "Wind / tornado / derecho", "Winter storm / ice", "Water / pipe / backup", "Fire / smoke", "Wildfire", "Farm or ranch building", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hlevel=3, fid="f"):
    roles = ["Homeowner", "Farm or ranch owner", "Business owner", "HOA or property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in South Dakota"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form does not create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn sun wide" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="hero-form-tab">Free claim review</p>
<h2 class="form-t">Is your claim worth a second look?</h2>
<p class="form-sub">Leave a number. A South Dakota appraiser calls back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn sun wide" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("southeast", "Sioux Empire & Southeast", "East River", ["Hail", "Derecho wind", "Tornadoes", "River flooding", "Ice storms"],
     "The most populated corner of the state, from Sioux Falls and Brookings down to Yankton and Vermillion. Hail and wind claims dominate, the 2019 Sioux Falls tornadoes and the 2022 derecho are still fresh, and the Big Sioux River and Missouri River bring flood questions to low ground.",
     ["sioux-falls", "brookings", "yankton", "vermillion"], "sioux-falls"),
    ("glacial", "Glacial Lakes & James Valley", "East River", ["Blizzards", "Hail", "Tornadoes", "Snowmelt water", "Farm buildings"],
     "Flat farmland, glacial lakes and long open stretches around Aberdeen, Watertown, Huron and Mitchell. Blizzards pack snow onto roofs, summer storms hammer steel buildings, and tornado history runs from Spencer to Delmont.",
     ["aberdeen", "watertown", "huron", "mitchell"], "prairie-farm"),
    ("river", "Missouri River Country", "The middle", ["Record hail", "Prairie wind", "River flooding", "Grass fires"],
     "Pierre, Fort Pierre and the long Missouri River reservoirs, where East River meets West River. The country’s largest recorded hailstone fell near Vivian, and the 2011 river flood reached homes in the capital.",
     ["pierre"], "river-bluffs"),
    ("hills", "Black Hills & West River", "West River", ["Wildfire & smoke", "Large hail", "Heavy snow", "Flash floods"],
     "Rapid City, Spearfish, Sturgis and the ranch country beyond. Ponderosa forests bring wildfire risk, storms off the Hills drop big hail, and early blizzards like the 2013 storm can bury roofs in feet of wet snow.",
     ["rapid-city", "spearfish", "sturgis"], "black-hills"),
]

STORMS = [
    ("1972", "Rapid City flood", "Overnight flooding on Rapid Creek reshaped the city and led to the greenway that runs through it today."),
    ("1998", "Spencer tornado", "A violent tornado destroyed much of Spencer in McCook County, one of the deadliest in state history."),
    ("2000", "Jasper Fire", "More than 80,000 acres burned in the southern Black Hills, a benchmark for wildfire risk in the region."),
    ("2010", "Vivian hailstone", "The largest hailstone recorded in the United States fell near Vivian in Lyman County."),
    ("2011", "Missouri River flood", "Record releases flooded low ground from Pierre and Fort Pierre down through southeast South Dakota."),
    ("2013", "October blizzard", "An early storm buried western South Dakota and the northern Hills in heavy, wet snow."),
    ("2019", "Sioux Falls tornadoes", "Three tornadoes touched down inside the state’s largest city in a single night."),
    ("2022", "May derecho", "Hurricane-force straight-line winds crossed eastern South Dakota, and a tornado struck Castlewood."),
    ("2024", "Southeast flooding", "Extreme June rain pushed the Big Sioux River to historic levels in the state’s southeast corner."),
]


def home():
    K = BRAND
    sv = lambda s, n: f'<a class="poster rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="poster-n">{n:02d}</span><span class="poster-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
    posters = "".join(sv(s, i + 1) for i, s in enumerate(SERVICES))

    tabs = "".join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><small>{e(side)}</small>{e(n)}</button>' for i, (k, n, side, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}">'
        f'<div class="region-ph">{img(ph, sizes="(max-width:900px) 100vw, 560px", alt="")}</div>'
        f'<div class="region-tx"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p>'
        f'<p class="region-cities">{" · ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]["city"])}</a>" for c in cities)}</p></div></div>'
        for k, n, side, perils, t, cities, ph in REGIONS)

    rail = "".join(f'<li class="rail-step"><span class="rail-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate([
        ("Free review", "We read the policy, the carrier’s estimate and your photos, then tell you honestly whether appraisal fits."),
        ("Our own valuation", "We inspect, measure and build a line-item estimate priced for your part of South Dakota."),
        ("Written demand", "Appraisal is demanded in writing and South Dakota Insurance Appraiser is named as your appraiser."),
        ("Line-by-line work", "We work through the estimate with the carrier’s appraiser. Most of the gap usually closes here."),
        ("Signed award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]))

    ledger = "".join(f'<li class="ledger-item"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for y, t, d in STORMS)
    tools = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 40vw, 220px", alt="")}<i>{e(t["icon"])}</i></span><span class="tcard-b"><small>{t["kind"]}</small><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS)

    def city_col(title, sides):
        li = "".join(f'<li><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a></li>' for l in LOCATIONS if l["side"] in sides)
        return f'<div class="city-col rv"><h3>{title}</h3><ul>{li}</ul></div>'

    posts = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{p["read"]} read</p><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser, we inspect, build our own line-item estimate, work with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster manages and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful, usually more than about 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. That is why documentation matters before you demand appraisal."),
        ("What does appraisal cost?", "Each side usually pays its own appraiser and half of the umpire. We put our fee in writing before work starts, and the first conversation is free."),
        ("Do you work in my part of South Dakota?", "Yes. We work in all 66 counties, from Sioux Falls and Aberdeen to Pierre, Rapid City and the ranches in between."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="tag">Independent claim appraisal · East River &amp; West River</p>
<h1>{K}: <span class="hl">a fair number</span> for your underpaid claim</h1>
<p class="lede">When the carrier accepts your claim but the check won’t cover the repair, {K} builds an independent, line-item valuation and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#how">See how it works</a></div>
<ul class="hero-points"><li>{ic("check")}Named as your appraiser</li><li>{ic("check")}Hail, wind, winter, fire &amp; water</li><li>{ic("check")}Homes, farms &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
<div class="hero-rail"><div class="wrap hero-rail-in">
<div class="count"><b data-count="66">66</b><span>counties served</span></div>
<div class="count"><b data-count="12">12</b><span>appraisal services</span></div>
<div class="count"><b data-count="7">7</b><span>free calculators</span></div>
<div class="count"><b>2 of 3</b><span>signatures bind the award</span></div>
</div></div>
</section>

<section class="sec qs"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Before you pick up the phone</p><h2>Three questions a {K} will ask you first</h2></div>
<ol class="qcards">
<li class="rv"><span class="qn">1</span><h3>Did the carrier accept the claim?</h3><p>Appraisal values covered losses. If the claim was denied outright, the first call is usually a South Dakota attorney, not {K}.</p></li>
<li class="rv"><span class="qn">2</span><h3>Is the gap big enough?</h3><p>Compare the carrier’s estimate with your contractor’s. A few hundred dollars can usually be closed with a supplement. Several thousand often justifies appraisal.</p></li>
<li class="rv"><span class="qn">3</span><h3>What does the clock say?</h3><p>Policies carry deadlines for proof of loss, depreciation recovery and lawsuits. Know them before anything else happens.</p></li>
</ol>
</div></section>

<section class="sec intro"><div class="wrap intro-in">
<figure class="intro-ph rv">{img("roof-inspection", sizes="(max-width:900px) 100vw, 520px")}</figure>
<div class="intro-tx rv">
<p class="kicker">Covered isn’t the same as paid</p>
<h2>Why owners bring in {K}</h2>
<p>Most short claims aren’t denials. They’re estimates with missing slopes, unmatched siding, a basement scoped as one wall, or a pole barn priced like a garden shed. {K} exists for that gap between “covered” and “paid in full.”</p>
<p>We value the loss from scratch, with our own inspection and measurements, never an edited copy of the carrier’s estimate. And we price it for where the property actually is: Sioux Falls labor, Black Hills access and a ranch two hours from the nearest supplier are not the same.</p>
<ul class="ticks">
<li>{ic("check")}<span><b>Defensible, not inflated.</b> Numbers built to hold up in front of an umpire.</span></li>
<li>{ic("check")}<span><b>Plain-English reporting.</b> You’ll understand every difference between our number and theirs.</span></li>
<li>{ic("check")}<span><b>Honest triage.</b> If your claim needs an attorney or a supplement instead, we’ll say so on the first call.</span></li>
</ul>
<a class="btn ink" href="{ABOUT}">Read our company profile {ic("arrow")}</a>
</div>
</div></section>

<section class="sec services-sec" id="services"><div class="wrap">
<div class="sec-h split-h rv"><div><p class="kicker">Twelve services</p><h2>What {K} can do for your claim</h2></div><p>From one estimate review to full panel representation, every service is built around a valuation of your loss that can stand up to scrutiny. Hurricanes don’t reach the northern plains, but derecho winds, record hail, blizzards and Black Hills wildfire do.</p></div>
<div class="posters">{posters}</div>
<p class="center"><a class="btn line" href="{SVC_BASE}">Compare all appraiser services {ic("arrow")}</a></p>
</div></section>

<section class="sec sunband" id="check"><div class="wrap split">
<div class="rv"><p class="kicker">Quick gap check</p><h2>Is the gap worth appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with {K} makes sense. If it’s small, a documented supplement may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds appraiser and umpire fees and shows your break-even point.</p></div>
<div class="rv">{PAYOFF_MINI}</div>
</div></section>

<section class="sec how" id="how"><div class="wrap">
<div class="sec-h rv"><p class="kicker">The process</p><h2>How {K} moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here’s the path from first call to signed award.</p></div>
<div class="rail" data-rail><span class="rail-track"><span class="rail-fill"></span></span><ol>{rail}</ol></div>
<p class="center"><a class="btn line" href="{PROCESS}">Read the full process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec deep"><div class="wrap">
<div class="sec-h rv"><p class="kicker light">East River · West River</p><h2>One state, four claim climates</h2><p>The Missouri River splits South Dakota in two, and the weather on each side shows up differently on a roof and in an estimate. {K} works both sides of the river.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="South Dakota regions">{tabs}</div><div class="region-panels">{panels}</div></div>
</div></section>

<section class="sec ledger-sec"><div class="wrap">
<div class="sec-h split-h rv"><div><p class="kicker">Weather on the record</p><h2>A short South Dakota storm history</h2></div><p>These events still shape how carriers and appraisers look at claims here. Each one taught {K} something about how damage shows up, and where estimates fall short.</p></div>
<ol class="ledger" tabindex="0" aria-label="Storm history timeline">{ledger}</ol>
<p class="ledger-hint">Scroll or swipe sideways for more years →</p>
</div></section>

<section class="sec tools-sec"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Free &amp; private</p><h2>Seven free calculators from {K}</h2><p>Run the numbers before you call. Every calculator works in your browser; nothing you type is stored or sent.</p></div>
<div class="tcards">{tools}</div>
<p class="center"><a class="btn line" href="{TOOL_BASE}">Open the calculator library {ic("arrow")}</a></p>
</div></section>

<section class="sec cities-sec"><div class="wrap">
<div class="city-banner rv">{img("badlands", sizes="100vw", alt="", extra=' data-parallax="0.08"')}<div class="city-banner-tx"><p class="kicker light">Statewide coverage</p><h2>Cities {K} serves</h2><p>All 66 counties, with regular work in these communities.</p></div></div>
<div class="city-cols">{city_col("East River", ("east",))}{city_col("Missouri River &amp; West River", ("river", "west"))}</div>
<p class="center"><a class="btn line" href="{LOC_BASE}">See all cities we serve {ic("arrow")}</a></p>
</div></section>

<section class="sec corner"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Choosing help</p><h2>Who should be in your corner?</h2><p>Each professional solves a different problem. {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="corner-cards">
<div class="ccard ccard-us rv"><span class="ccard-ic">{ic("scale")}</span><h3>An appraiser</h3><p class="ccard-when">Choose this when coverage is accepted and the number is the fight.</p><ul><li>Values the amount of loss</li><li>Result: binding award, 2 of 3 signatures</li><li>Doesn’t decide coverage</li></ul></div>
<div class="ccard rv"><span class="ccard-ic">{ic("users")}</span><h3>A public adjuster</h3><p class="ccard-when">Choose this when you want help managing the whole claim from the start.</p><ul><li>Prepares and negotiates the claim</li><li>Result: negotiated settlement</li><li>Licensed by the state</li></ul></div>
<div class="ccard rv"><span class="ccard-ic">{ic("doc")}</span><h3>An attorney</h3><p class="ccard-when">Choose this for denials, bad-faith concerns or a deadline that’s close.</p><ul><li>Gives legal advice, files suit</li><li>Result: settlement or judgment</li><li>Argues coverage in court</li></ul></div>
</div>
</div></section>

<section class="sec faq-sec"><div class="wrap">
<div class="sec-h rv"><p class="kicker">FAQ</p><h2>Questions people ask {K}</h2></div>
{faq_block(home_faqs, "faq faq-grid")}
<p class="center"><a class="btn line" href="{FAQ_P}">All appraisal questions {ic("arrow")}</a> <a class="btn line" href="{GLOSS}">Appraisal glossary</a></p>
</div></section>

<section class="sec posts-sec"><div class="wrap">
<div class="sec-h rv"><p class="kicker">Articles</p><h2>Read before you demand appraisal</h2><p>Practical guides from {K} on policy language, documentation and strategy.</p></div>
<div class="posts">{posts}</div>
</div></section>

<section class="parallax">{img("shelf-cloud", "parallax-bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap parallax-in rv"><p class="kicker light">Storm season is claim season</p><h2>Check the numbers before you sign off on them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec contact-sec" id="contact"><div class="wrap contact-in">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk with {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing.</p>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm Central</span></li><li>{ic("pin")}<span><small>Coverage</small>All 66 South Dakota counties</span></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Disputed Claim Appraisal",
                        "South Dakota Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hail, wind, fire and water claims.",
                        body, [faq_schema(home_faqs)], photo="hero-home", body_cls="is-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
    for i, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraiser service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([(r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel], "Service")}
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All cities", LOC_BASE)])}</aside></div>
{cta_strip()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "South Dakota"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 360px", alt="")}</span><span class="icard-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "South Dakota Insurance Appraisal Services",
                     "Twelve services, one goal: an accurate, defensible valuation of your loss. Start with an estimate review, or bring us in once appraisal has been demanded.", "estimate-desk") + f"""
<section class="sec"><div class="wrap"><div class="icards">{cards}</div></div></section>
<section class="sec tint"><div class="wrap split">
<div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. Many disputes close at that stage.</p><p>You won’t find a hurricane service here. Tropical storms don’t reach South Dakota, but derecho winds, blizzards, record hail and Black Hills wildfires do, and each has its own page.</p><a class="btn ink" href="{SVC_BASE}insurance-estimate-second-opinion/">About estimate reviews {ic("arrow")}</a></div>
<div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial claims?", "Yes: farmsteads, ranch buildings, apartments, retail, churches and HOA properties."), ("Do you only work on hail claims?", "No. We handle wind, winter, water, fire, wildfire and other covered perils.")])}</div>
</div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services | South Dakota",
                             "Insurance appraisal services in South Dakota: appraisal clause work, estimate review, hail, wind, winter, wildfire, farm and umpire services.",
                             body, schema, photo="estimate-desk"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = f'{l["city"]} Insurance Appraiser'
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', name, l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks</b><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Services for {e(l["city"])} property owners</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} owners</h2>{faq_block(l["faqs"])}
<h2>Nearby communities</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "City")}
</article>
<aside class="aside">{call_box()}{list_box("Cities we serve", items, path)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, South Dakota", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "South Dakota"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{loc_path(l)}"><span class="icard-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 360px", alt="")}</span><span class="icard-b"><small>{e(l["county"])}</small><h2>{e(l["city"])}</h2><p>{e(", ".join(l["perils"][:3]))}</p></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="region-row rv"><div class="region-row-ph">{img(ph, sizes="(max-width:700px) 100vw, 300px", alt="")}</div><div><p class="kicker">{e(side)}</p><h3>{e(n)}</h3><p>{e(t)}</p></div></div>' for k, n, side, _p, t, _c, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 66 South Dakota Counties",
                     "We work statewide, from the Sioux Empire to the edge of the Black Hills. These city pages cover the communities where we handle claims most often.", "badlands") + f"""
<section class="sec"><div class="wrap"><div class="icards">{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-h rv"><p class="kicker">Regions</p><h2>How claims differ across South Dakota</h2><p>The same policy language plays out very differently in a Sioux Falls subdivision, a James Valley farmstead and a cabin above Spearfish.</p></div>{reg}</div></section>
{cta_strip("Don’t see your town?", "We cover every South Dakota county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Cities We Serve | South Dakota Insurance Appraiser",
                             "Insurance appraisal in all 66 South Dakota counties, including Sioux Falls, Rapid City, Aberdeen, Brookings, Watertown, Pierre and Spearfish.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f'{l["city"]}, SD', loc_path(l)) for l in LOCATIONS])], photo="badlands"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · nothing stored", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2>{related([(o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others], "Calculator")}</article>
<aside class="aside">{call_box()}{list_box("All calculators", items, path)}</aside></div>
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 40vw, 220px", alt="")}<i>{e(t["icon"])}</i></span><span class="tcard-b"><small>{t["kind"]}</small><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p></span></a>' for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Policyholder Calculators for South Dakota Claims",
                     "Seven calculators and planners built from real appraisal work. Use them to understand your claim, check the carrier’s math and plan your next step. No sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards">{cards}</div></div></section>
<section class="sec tint"><div class="wrap split">
<div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="steps-list"><li>Start with the <a href="{TOOL_BASE}appraisal-calendar-builder/">appraisal calendar builder</a> so no deadline slips.</li><li>Check quantities with the <a href="{TOOL_BASE}roof-slope-factor-calculator/">roof squares and slope factor calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}hail-percentage-deductible-calculator/">hail deductible</a> and <a href="{TOOL_BASE}depreciation-recovery-calculator/">depreciation recovery</a> calculators.</li><li>Farm or commercial? Run the <a href="{TOOL_BASE}coinsurance-penalty-calculator/">coinsurance penalty calculator</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a>, then grade your file with the <a href="{TOOL_BASE}claim-file-readiness-grader/">readiness grader</a>.</li></ol></div>
<div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Policyholder Calculators | South Dakota Claims",
                              "Free policyholder calculators for appraisal payoff, depreciation, roof squares, hail deductibles, coinsurance, deadlines and claim readiness.",
                              body, schema, photo="calculator"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Inside the appraisal process", PROCESS), ("Appraisal questions answered", FAQ_P), ("Appraisal glossary", GLOSS), ("Storm claim articles", POST_BASE)]

    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "Inside the Insurance Appraisal Process, Step by Step",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what and where South Dakota claims most often go wrong.", "policy-review",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in South Dakota", "description": "The seven stages of a property insurance appraisal, from the disagreement to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in South Dakota | 7 Steps",
                         "The insurance appraisal process in South Dakota, step by step: the written demand, both appraisers, the umpire and the binding award explained.",
                         body, [crumbs_schema(trail), howto], photo="policy-review"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Questions answered", path)]
    nav = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions, Answered",
                     "Plain answers grouped by topic: how appraisal works, what it costs, how long it takes and how South Dakota rules fit in.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="FAQ topics">{nav}</nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>{cta_strip("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | South Dakota Answers",
                         "Insurance appraisal FAQ for South Dakota owners, grouped by topic: how it works, costs, timing, deadlines and the state’s regulator and rules.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gterm\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Insurance Appraisal Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "paperwork", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="gfilter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “coinsurance” or “umpire”" autocomplete="off"><p class="hint" data-gcount aria-live="polite">{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary | ACV, RCV, Umpire",
                         "Insurance appraisal glossary with 40+ plain-English terms: actual cash value, coinsurance, depreciation, umpire, derecho, O&P and more.",
                         body, [crumbs_schema(trail), dts], photo="paperwork"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Articles", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Article · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([(o["title"], f'{POST_BASE}{o["slug"]}/') for o in others], "Article")}</article>
<aside class="aside">{call_box()}{list_box("Resources", learn_items)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Articles", path)]
    cards = "".join(f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="post-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Articles", "Storm Claim Articles for South Dakota Owners",
                     "Practical guides on policy language, documentation and claim strategy, written by people who work appraisal panels.", "storm-sky", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Storm Claim Articles | South Dakota Appraisal Guides",
                         "Storm claim articles for South Dakota owners: the appraisal clause, hail documentation, derecho claims, wildfire smoke, coinsurance and more.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="storm-sky"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Company profile", path)]
    body = page_hero(trail, "Company profile", "About South Dakota Insurance Appraiser",
                     "An independent appraisal and estimating practice focused on one question: what a covered property loss actually costs, documented clearly enough that everyone at the table can see it.", "consult-table") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("roof-inspection", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} works on the amount of loss, and our process, tools and documentation standards are built around answering that question well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Inspection first.</strong> We measure and photograph before we look at anyone else’s numbers.</li>
<li><strong>Supported over impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Local pricing.</strong> Labor, material and travel costs differ between Sioux Falls, the James Valley and the Black Hills. Our estimates reflect that.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, farm and ranch families, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across South Dakota. On any claim, we serve in one role only, and we disclose any prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t guarantee outcomes. No honest appraiser can.</p>
<h2>Both sides of the river</h2>
<p>East River and West River South Dakota produce very different claims: derecho wind and hail around Sioux Falls, blizzards in the James Valley, record hail on the central plains, wildfire and heavy snow in the Black Hills. Working statewide means we see all of them and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Appraiser services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>{cta_strip()}"""
    write(path, document(path, "Company Profile | South Dakota Insurance Appraiser",
                         "About South Dakota Insurance Appraiser, an independent appraisal and estimating practice focused on the amount of loss on disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="consult-table"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Contact", "Contact South Dakota Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "meeting", cta=False) + f"""
<section class="sec contact-sec"><div class="wrap contact-in">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small>Mon–Fri, 8am–6pm Central</span></li><li>{ic("pin")}<span><small>Service area</small>Statewide, all 66 counties</span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks-plain"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hlevel=3, fid="c")}</div></div></section>"""
    write(path, document(path, "Contact Us | South Dakota Insurance Appraiser",
                         "Contact South Dakota Insurance Appraiser for a free review of a disputed claim. Call or text (844) 537-1427 or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="meeting"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | South Dakota Insurance Appraiser",
                  "The South Dakota Insurance Appraiser privacy policy: what we collect through forms, calls and email, how we use it and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and claim details. Our web host also records standard technical data, such as IP address, browser type and pages requested, for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators, planners and checklists run in your browser. Numbers and answers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, they may set cookies to measure site use.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect what you share with us."),
        TERMS: ("Terms of Use", "Terms of Use | South Dakota Insurance Appraiser",
                "Terms of use for the South Dakota Insurance Appraiser website and its free calculators, including no-advice, liability and governing-law terms.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in South Dakota.</p>
<h2>No client relationship</h2><p>Reading this site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. For legal questions, consult a licensed South Dakota attorney.</p>
<h2>Calculators and estimates</h2><p>Calculators give planning estimates based on what you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration and don’t show our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of South Dakota.</p>""", "The terms that apply when you use this website and its calculators."),
        DISCLAIM: ("Disclaimer", "Disclaimer | South Dakota Insurance Appraiser",
                   "Limits on the information South Dakota Insurance Appraiser publishes: not legal advice, illustrative figures only and no guaranteed results.", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Illustrative figures, no guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines, including for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult a South Dakota attorney promptly.</p>
<h2>Photographs</h2><p>Photos are public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to laws, agencies and weather events are for context only. Check current law and facts with official sources such as the South Dakota Division of Insurance.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h1, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office-building", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo="office-building"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Page map", path)]
    groups = [
        ("Main", [("Home", "/"), ("Company profile", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal process", PROCESS), ("Questions answered", FAQ_P), ("Glossary", GLOSS), ("Articles", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Page Map", f"Every page on {BRAND}, grouped by section.", "office-building", cta=False) + f'<section class="sec"><div class="wrap map-grid">{cols}</div></section>'
    write(path, document(path, "Page Map | South Dakota Insurance Appraiser",
                         "A complete page map of South Dakota Insurance Appraiser: every service, city page, free calculator, article and resource on the site.",
                         body, [crumbs_schema(trail)], photo="office-building"), 0.3)

    body = f"""<section class="phero phero-404">{img("storm-sky", "phero-bg", lazy=False, alt="")}<div class="wrap phero-in"><p class="tag">Error 404</p><h1>That page went with the wind</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn sun" href="/">Home</a><a class="btn line-light" href="{SVC_BASE}">Services</a><a class="btn line-light" href="{TOOL_BASE}">Calculators</a><a class="btn line-light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", "Page Not Found | South Dakota Insurance Appraiser",
                                "Sorry, this South Dakota Insurance Appraiser page could not be found. Try our services, free calculators or contact page to find your way.",
                                body, robots="noindex,follow", photo="storm-sky"), sitemap=False)


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
    # Search Console verification file: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// South Dakota Insurance Appraiser - canonical host guard.
// Required by index.php and by the first line of every dir/index.php page.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$sdia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$sdia_real  = 'southdakotainsuranceappraiser.com';
$sdia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$sdia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://southdakotainsuranceappraiser.com - only on the real domain.
if ($sdia_host === 'www.' . $sdia_real || ($sdia_host === $sdia_real && $sdia_proto === 'http')) {
    header('Location: https://' . $sdia_real . $sdia_uri, true, 301);
    exit;
}
// /dir/index.php (and /index.php) duplicate the directory URL: 301 to /dir/.
if (preg_match('#^(.*/)index\.php$#', strtok($sdia_uri, '?'), $sdia_m)) {
    $sdia_q = strpos($sdia_uri, '?') !== false ? substr($sdia_uri, strpos($sdia_uri, '?')) : '';
    header('Location: ' . $sdia_m[1] . $sdia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($sdia_host !== $sdia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// South Dakota Insurance Appraiser - front controller for the static build.
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
