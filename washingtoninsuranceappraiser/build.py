#!/usr/bin/env python3
"""Static site generator for washingtoninsuranceappraiser.com.

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
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Washington Insurance Appraiser"
HOST = "washingtoninsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"   # cache-buster for CSS/JS
FAV = "1"           # cache-buster for icons
COUNTIES = 39

# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/insurance-appraisal-services/"
LOC_BASE = "/cities-we-serve/"
TOOL_BASE = "/free-claim-calculators/"
POST_BASE = "/claim-resources/"
P_PROCESS = "/how-insurance-appraisal-works/"
P_FAQ = "/claim-appraisal-faq/"
P_GLOSS = "/claim-appraisal-glossary/"
P_ABOUT = "/about-washington-insurance-appraiser/"
P_CONTACT = "/talk-to-an-appraiser/"
P_PRIVACY = "/your-privacy-rights/"
P_TERMS = "/terms-for-using-this-site/"
P_DISC = "/disclaimers-and-limits/"
P_MAP = "/browse-every-page/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, WA"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
def ph(key, *fallbacks):
    for k in (key,) + fallbacks:
        if k in PHOTOS:
            return k
    raise KeyError(key)


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ("" if lazy is None else ' fetchpriority="high"')
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consultation-table", "home-insurance-claim-appraisal": "home-evergreens",
    "condo-hoa-commercial-appraisal": "condo-building", "roof-hail-damage-appraisal": "roof-damage",
    "windstorm-tornado-appraisal": "storm-sky", "tree-impact-claim-appraisal": "fallen-tree-house",
    "water-rain-intrusion-appraisal": "water-damage", "house-fire-smoke-appraisal": "house-fire",
    "wildfire-ash-claim-appraisal": "wildfire-smoke", "snow-ice-freeze-appraisal": "snow-house",
    "carrier-estimate-review": "calculator-paperwork", "neutral-umpire-services": "paperwork-review",
}
LOC_PHOTO = {
    "seattle": ("seattle-skyline",), "spokane": ("snow-house",), "tacoma": ("tacoma",), "vancouver": ("columbia-river",),
    "bellevue": ("home-evergreens",), "everett": ("tree-down-street",), "olympia": ("olympia-capitol",), "bellingham": ("icicles-roof",),
    "yakima": ("wildfire-smoke",), "tri-cities": ("storm-sky",), "wenatchee": ("wenatchee",), "bremerton": ("fallen-tree-house",),
}
POST_PHOTO = {
    "washington-appraisal-clause-guide": "consultation-table", "appraisal-oic-complaint-or-ifca": "paperwork-review",
    "documenting-windstorm-tree-damage": "tree-down-street", "wildfire-total-loss-claim-checklist": "burned-home",
    "frozen-pipes-ice-dams-coverage": "icicles-roof", "reading-your-insurer-estimate": "calculator-desk",
}


def lph(l):
    return ph(*LOC_PHOTO[l["slug"]])


# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, cls="ico"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=44):
    # Brand mark: white roof chevron over a yellow "W" on an emerald tile (same art as static/favicon.svg).
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#008457"/>'
            '<path d="M12 18.5L24 9.5l12 9" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M11 23.5l5.2 14 7.8-10.5 7.8 10.5 5.2-14" fill="none" stroke="#FFD520" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Washington</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    cities = []
    for l in LOCATIONS:
        if l["slug"] == "tri-cities":
            cities += ["Kennewick", "Pasco", "Richland"]
        else:
            cities.append(l["city"])
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "WA", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-WA", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Washington property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 39 Washington counties.",
        "areaServed": [{"@type": "State", "name": "Washington"}] + [{"@type": "City", "name": c} for c in cities],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Windstorm damage", "Wildfire claims", "Xactimate estimating"],
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


# ---------------------------------------------------------------- GTM
def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            f"'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All 39 counties", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", [("How appraisal works", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Claim resources", POST_BASE)] +
         [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS[:3]], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "ico chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ico chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-head"><div class="wrap head-in">
{brand()}
<nav class="main-nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-actions"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-y head-cta" href="{P_CONTACT}">Free review</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></header>
<div class="drawer-scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}<li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></nav>
<div class="drawer-foot"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm Pacific · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap foot-band-in"><h2>Claim paid, but not paid enough?</h2><div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{P_CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-foot")}
<p>Independent appraisal, estimate review and umpire services for property owners with disputed insurance claims, from the Olympic Peninsula to the Palouse.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm Pacific</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Cities</h3><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h3>Free calculators</h3><ul>{tl}</ul></div>
<div><h3>Company</h3><ul><li><a href="{P_ABOUT}">About</a></li><li><a href="{P_CONTACT}">Contact</a></li><li><a href="{P_PROCESS}">How appraisal works</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Claim resources</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general and educational, policy terms vary, and results are never guaranteed.</p>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Site directory</a></li></ul></div></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<nav class="call-bar" aria-label="Quick contact"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">Free claim review</a></nav>"""


def document(path, title, desc, body, schema=None, trail=None, og_type="website", robots="index,follow", photo=None, home=False):
    canonical = DOMAIN + path
    trail = trail or [("Home", "/")]
    page_type, extra_nodes = "WebPage", []
    crumb = crumbs_schema(trail)
    crumb["@id"] = canonical + "#breadcrumb"
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        if t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    key = photo or ph("hero-home")
    pimg = PHOTOS[key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY, "breadcrumb": {"@id": crumb["@id"]},
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{key}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": pimg["alt"]},
    }
    order = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")
    main = sorted((n for n in extra_nodes if n.get("@type") in order), key=lambda n: order.index(n["@type"]))
    webpage["mainEntity"] = {"@id": main[0]["@id"] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage, crumb] + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pp = PHOTOS[key]
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{key}.webp" imagesrcset="/assets/img/photos/{key}-640.webp 640w, '
           f'/assets/img/photos/{key}.webp {pp["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Washington State">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Washington State">
<meta name="geo.region" content="US-WA">
<meta name="geo.placename" content="Washington">
<meta name="theme-color" content="#00432c">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gabarito:wght@500;600;700;800&family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{"is-home" if home else "is-inner"}">
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
    # Pages are written as dir/index.php: the host serves real files without running the front controller,
    # so each page starts with the canonical-host guard (www/http 301, /index.php 301, off-domain noindex).
    # Never write dir/index.html: the host would serve it directly and skip the guard.
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(parts) + "</ol></nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "ico chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box call-box"><h2 class="box-t">Talk it through, free</h2><p>Tell us what happened and what the insurer offered. We’ll tell you honestly whether appraisal fits.</p><a class="call-num" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-y full" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="box-t">{e(title)}</h2><ul class="side-links">{li}</ul></div>'


def two_col(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="side"><div class="side-in">{aside}</div></aside></div>'


def cta_strip(h="Have a claim that doesn’t add up?", p="Send us the insurer’s estimate. We’ll review it and tell you what we see."):
    return f"""<section class="cta-strip"><div class="wrap cta-strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def card(href, photo, kicker, title, text, h="h3", more="Learn more"):
    return (f'<a class="pcard rv" href="{href}"><span class="pcard-img">{img(photo, sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
            f'<span class="pcard-body"><span class="pcard-k">{e(kicker)}</span><{h} class="pcard-t">{e(title)}</{h}><span class="pcard-p">{e(text)}</span><span class="pcard-more">{more} {ic("arrow")}</span></span></a>')


LOSSES = ["Windstorm / fallen tree", "Wildfire / smoke", "Snow, ice or frozen pipe", "Water / leak", "House fire", "Hail / roof", "Earthquake", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", sub="Free review, no obligation. We usually reply within one business day.", page="/", h="h3"):
    roles = ["Homeowner", "Condo owner / HOA board", "Commercial owner", "Property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Washington"]
    return f"""<form class="lead-form" action="/api/contact.php" method="post" data-lead novalidate>
<{h} class="form-t">{e(heading)}</{h}><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="span2"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="span2"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="span2"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="span2 hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="span2"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="{P_PRIVACY}">privacy statement</a>.</span></label></div>
<div class="span2"><button class="btn btn-g full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-t">Get a free claim review</h2><p class="form-sub">Tell us a little. We’ll call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{P_PRIVACY}">privacy statement</a>.</span></label>
<button class="btn btn-y full" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="form-trust">No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Puget Sound", "King, Pierce, Snohomish, Kitsap, Thurston", "Windstorms, falling firs, water losses and the occasional arctic blast hit the most densely insured part of the state.", "seattle-skyline", ["seattle", "bellevue", "tacoma", "everett", "olympia", "bremerton"]),
    ("North Sound & San Juans", "Whatcom, Skagit, San Juan, Island", "Fraser outflow winds, hard freezes and atmospheric river rains, including the record November 2021 floods.", "icicles-roof", ["bellingham"]),
    ("Southwest Washington & Coast", "Clark, Cowlitz, Lewis, Grays Harbor, Pacific", "Columbia Gorge ice storms, coastal gales and river flooding, plus fast suburban growth around Vancouver.", "columbia-river", ["vancouver"]),
    ("Central Washington", "Chelan, Kittitas, Okanogan, Yakima", "Wildfire country on the east slope of the Cascades, with heavy snow, orchards and farm buildings.", "wildfire-hillside", ["wenatchee", "yakima"]),
    ("Columbia Basin", "Benton, Franklin, Grant, Walla Walla", "Wind, dust, hail and range fires across a hot, dry basin and the Tri-Cities.", "storm-sky", ["tri-cities"]),
    ("Inland Northwest & Palouse", "Spokane, Stevens, Whitman, Lincoln", "Hail, windstorms, snow load, ice storms and some of the state’s most destructive recent wildfires.", "snow-house", ["spokane"]),
]

PERILS = [
    ("Windstorms", "Pacific lows like the 1962 Columbus Day Storm and the 2024 bomb cyclone.", "storm-sky", "windstorm-tornado-appraisal"),
    ("Falling trees", "Douglas fir, cedar and bigleaf maple through roofs and framing.", "fallen-tree-house", "tree-impact-claim-appraisal"),
    ("Wildfire & smoke", "Total losses and ash-filled survivors, from Okanogan to Spokane County.", "wildfire-smoke", "wildfire-ash-claim-appraisal"),
    ("Snow, ice & freeze", "Ice dams, snow-load collapse and pipes that split in arctic blasts.", "snow-house", "snow-ice-freeze-appraisal"),
    ("Water & rain", "Supply-line failures and wind-driven rain during atmospheric rivers.", "water-damage", "water-rain-intrusion-appraisal"),
    ("Hail & roofs", "Summer storms east of the Cascades and roof disputes statewide.", "roof-damage", "roof-hail-damage-appraisal"),
    ("House fire", "Structure, smoke migration and contents losses room by room.", "house-fire", "house-fire-smoke-appraisal"),
]


def home():
    K = BRAND
    rail = "".join(
        f'<li class="rail-item"><a class="peril rv" href="{SVC_BASE}{slug}/">{img(ph(photo), sizes="(max-width:700px) 80vw, 320px", alt="", lazy=None)}<span class="peril-in"><span class="peril-t">{e(t)}</span><span class="peril-p">{e(p)}</span></span></a></li>'
        for t, p, photo, slug in PERILS)
    svc_cards = "".join(card(f'{SVC_BASE}{s["slug"]}/', ph(SVC_PHOTO[s["slug"]]), f"Service {i + 1:02d}", s["name"], s["short"]) for i, s in enumerate(SERVICES[:6]))
    svc_more = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])} {ic("arrow")}</a></li>' for s in SERVICES[6:])
    tool_cards = "".join(card(f'{TOOL_BASE}{t["slug"]}/', ph(t["photo"]), f"Free {t['kind'].lower()}", t["name"], t["short"], more="Open") for t in TOOLS)
    city_cards = "".join(
        f'<a class="city rv" href="{loc_path(l)}">{img(lph(l), sizes="(max-width:700px) 50vw, 280px", alt="")}<span class="city-in"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    posts = "".join(card(f'{POST_BASE}{p["slug"]}/', ph(POST_PHOTO[p["slug"]]), f'Guide · {p["read"]} read', p["title"], p["summary"], more="Read") for p in POSTS[:3])
    steps = "".join(f'<li class="step rv"><span class="step-n">{i + 1}</span><div class="step-b"><h3>{e(t)}</h3><p>{e(p.split(". ")[0])}.</p></div></li>' for i, (t, p) in enumerate(PROCESS_STEPS))

    west, east = REGIONS[0], REGIONS[5]
    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree about the cost. As your appointed appraiser we inspect, build an independent line-item estimate, work with the insurer’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster manages and negotiates the whole claim for you. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the insurer’s estimate, and the gap between it and your contractor’s number is meaningful, roughly more than 10% or several thousand dollars."),
        ("Is an appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign it. That’s why documentation matters so much before you demand appraisal."),
        ("What does appraisal cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you cover my part of Washington?", f"Yes. We work in all {COUNTIES} counties, with regular work around Seattle, Spokane, Tacoma, Vancouver, Bellevue, Everett, Olympia, Bellingham, Yakima, the Tri-Cities, Wenatchee and Bremerton."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img(ph("hero-home"), lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · All {COUNTIES} counties</p>
<h1>{K}: a second, <mark>independent</mark> number for your property claim</h1>
<p class="lede">When your insurer accepts the claim but the check won’t cover the repair, {K} builds a line-by-line valuation of the real cost and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#services">See our services {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Local pricing, county by county</li><li>{ic("check")}Homes, condos &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="numbers" aria-label="At a glance"><div class="wrap"><ul class="numbers-in">
<li><b data-count="{COUNTIES}">{COUNTIES}</b><span>Washington counties served</span></li>
<li><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; review services</span></li>
<li><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></li>
<li><b>2 of 3</b><span>Signatures make an award binding</span></li>
</ul></div></section>

<section class="sec intro"><div class="wrap intro-grid">
<div class="intro-copy rv">
<p class="kicker">What we do</p>
<h2>What a {K} does when a claim comes up short</h2>
<p>Most underpaid claims in Washington aren’t denied. They’re trimmed. A roof gets two slopes instead of four. A soaked hallway is left out of the flooring line. A Douglas fir that cracked the rafters is treated as a shingle repair. {K} exists for the gap between “covered” and “paid in full.”</p>
<p>We are appraisers, not adjusters or attorneys. Our job is one question: what does it really cost to put this property back the way it was? We answer it with our own inspection, our own measurements and pricing for your county.</p>
<ol class="principles">
<li><b>From scratch.</b> We scope the loss ourselves. We never mark up the insurer’s estimate.</li>
<li><b>Defensible.</b> Every line is something we can support in front of an umpire.</li>
<li><b>Honest triage.</b> If you need an attorney or the OIC instead, we say so on the first call.</li>
</ol>
<a class="btn btn-g" href="{P_ABOUT}">About {K} {ic("arrow")}</a>
</div>
<figure class="intro-fig rv">{img(ph("roofer-work", "clipboard-inspection"), sizes="(max-width:900px) 100vw, 520px")}<figcaption><b>Inspection first.</b> Every valuation starts on site.</figcaption></figure>
</div></section>

<section class="sec perils-sec"><div class="wrap">
<div class="sec-head row rv"><div><p class="kicker">Washington weather</p><h2>The losses a {K} values most</h2><p>Washington’s biggest claim events rarely look like the Gulf Coast’s. They come as wind, fire, ice and water.</p></div>
<div class="rail-nav"><button type="button" class="rail-btn" data-rail="-1" aria-label="Scroll perils left">{ic("left")}</button><button type="button" class="rail-btn" data-rail="1" aria-label="Scroll perils right">{ic("right")}</button></div></div>
<ul class="rail" tabindex="0" aria-label="Common Washington perils">{rail}</ul>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Appraisal services</p><h2>Twelve ways {K} can help with a disputed claim</h2><p>Start with a review of the insurer’s estimate, or bring us in once appraisal has been demanded. Every service is built around one thing: a valuation that holds up.</p></div>
<div class="cards3" data-stagger>{svc_cards}</div>
<ul class="more-links rv">{svc_more}</ul>
</div></section>

<section class="sec two-wa"><div class="wrap">
<div class="sec-head center rv"><p class="kicker">One state, two climates</p><h2>Westside and Eastside claims are not the same claim</h2><p>The Cascade crest splits Washington into two very different places to own property. A {K} has to price both.</p></div>
<div class="split-wa">
<div class="wa-side rv">{img(ph(west[3]), sizes="(max-width:900px) 100vw, 600px", alt="")}<div class="wa-in"><span class="wa-tag">West of the Cascades</span><h3>Wet, windy and wooded</h3><p>Mild, rainy winters punctuated by big Pacific windstorms. Tall evergreens come down on roofs, atmospheric rivers test every flashing detail, and rare arctic blasts freeze pipes in homes built for mild weather.</p><ul><li>Windstorms &amp; fallen trees</li><li>Rain intrusion &amp; water losses</li><li>Snow and ice events</li><li>Condo and HOA losses</li></ul></div></div>
<div class="wa-side rv">{img(ph("wildfire-hillside"), sizes="(max-width:900px) 100vw, 600px", alt="")}<div class="wa-in"><span class="wa-tag">East of the Cascades</span><h3>Dry, hot and snowy</h3><p>Hot, dry summers with thunderstorms, hail and wildfire, then cold, snowy winters. Ice storms in Spokane, heavy snow loads in Wenatchee and range fires around the Tri-Cities all show up in claims.</p><ul><li>Wildfire, smoke &amp; ash</li><li>Hail &amp; summer wind</li><li>Snow load &amp; freeze</li><li>Farm and commercial buildings</li></ul></div></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The process</p><h2>How {K} moves a stuck claim to a signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result.</p></div>
<ol class="steps" data-steps><span class="steps-line" aria-hidden="true"><span></span></span>{steps}</ol>
<p class="center rv"><a class="link" href="{P_PROCESS}">Read the full appraisal process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec deep" id="check"><div class="wrap gap-grid">
<div class="rv"><p class="kicker light">Quick gap check</p><h2>Is your gap big enough for appraisal?</h2><p>Type in the two numbers you already have. If the difference is large, a conversation with a {K} makes sense. If it’s small, a documented supplement request may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-calculator/">appraisal payoff calculator</a> adds appraiser and umpire fees so you can see a realistic net figure. Example numbers are illustrative.</p><a class="btn btn-y" href="{TOOL_BASE}">See all {len(TOOLS)} free calculators {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free claim calculators from {K}</h2><p>Run the numbers before you pick up the phone. Everything runs in your browser and nothing is stored or sent.</p></div>
<div class="cards3" data-stagger>{tool_cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head row rv"><div><p class="kicker">Statewide coverage</p><h2>Cities where {K} works most often</h2><p>We serve all {COUNTIES} counties. These local pages cover the communities where we handle claims most often.</p></div><a class="btn btn-line" href="{LOC_BASE}">All cities &amp; regions {ic("arrow")}</a></div>
<div class="cities" data-stagger>{city_cards}</div>
</div></section>

<section class="sec paths-sec"><div class="wrap">
<div class="sec-head center rv"><p class="kicker">Choosing a path</p><h2>Appraisal, an OIC complaint or an attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and money, and {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="paths" data-stagger>
<div class="path hl rv"><span class="path-tag">What we do</span><h3>Appraisal</h3><p>For when the insurer accepts coverage but you disagree on the amount. Two appraisers and an umpire set a binding number.</p><ul><li>Scope and price disputes</li><li>Binding award on value</li><li>Each side pays its appraiser</li></ul></div>
<div class="path rv"><span class="path-tag">Regulator</span><h3>OIC complaint</h3><p>For when the handling is the problem: delays, silence, unexplained decisions. The Office of the Insurance Commissioner asks the insurer to respond.</p><ul><li>Free to file</li><li>Insurer must answer the regulator</li><li>Not a lawsuit</li></ul></div>
<div class="path rv"><span class="path-tag">Legal</span><h3>Attorney &amp; IFCA</h3><p>For denials or conduct you believe was unreasonable. Washington’s Insurance Fair Conduct Act may provide remedies. Only a lawyer can advise you.</p><ul><li>Coverage denials</li><li>Bad-faith concerns</li><li>Notice rules apply</li></ul></div>
</div>
<p class="center rv"><a class="link" href="{POST_BASE}appraisal-oic-complaint-or-ifca/">Compare the three paths in detail {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap faq-grid">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-g" href="{P_FAQ}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Claim resources</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on policy language, documentation and strategy.</p></div>
<div class="cards3" data-stagger>{posts}</div>
</div></section>

<section class="cta-photo"><div class="cta-photo-bg">{img(ph("mount-rainier", "storm-sky"), alt="", extra=' data-parallax="0.15"')}</div><div class="wrap cta-photo-in rv"><p class="kicker light">Before you sign off</p><h2>The best time to check the insurer’s numbers is before you accept them</h2><p>A short review now can save you from settling for a payment that won’t cover the repair.</p><div class="btn-row"><a class="btn btn-y" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec deep" id="contact"><div class="wrap contact-grid">
<div class="rv"><p class="kicker light">Start with a conversation</p><h2>Talk to {K} about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure, no obligation.</p>
<ul class="contact-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Pacific</b></div></li><li>{ic("pin")}<div><span>Coverage</span><b>All {COUNTIES} Washington counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{K} | Independent Claim Appraisal",
                        "Washington Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid windstorm, wildfire and water claims.",
                        body, [faq_schema(home_faqs)], photo=ph("hero-home"), home=True), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        idx = SERVICES.index(s)
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(card(f'{SVC_BASE}{r["slug"]}/', ph(SVC_PHOTO[r["slug"]]), "Related service", r["name"], r["short"]) for r in rel)
        photo = ph(SVC_PHOTO[s["slug"]])
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        art = f'{s["body"]}<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}<h2>Related services</h2><div class="cards3 tight">{related}</div>'
        aside = call_box() + list_box("All services", items, path) + list_box("Where we work", locs + [("All cities", LOC_BASE)])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], photo, s["facts"]) + two_col(art, aside) + cta_strip()
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                                           "areaServed": {"@type": "State", "name": "Washington"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{photo}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, trail, photo=photo), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(card(f'{SVC_BASE}{s["slug"]}/', ph(SVC_PHOTO[s["slug"]]), f"Service {i + 1:02d}", s["name"], s["short"], h="h2") for i, s in enumerate(SERVICES))
    photo = ph("roofer-work", "clipboard-inspection")
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Washington Property Claims",
                     f"From a single estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", photo) + f"""
<section class="sec"><div class="wrap"><div class="cards3" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-grid"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most claims begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know where the insurer’s estimate falls short and what the gap is worth. A review gives you that answer in days, and many disputes close at that stage.</p><a class="btn btn-g" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle both homes and commercial buildings?", "Yes: houses, condos, multifamily, retail, office, industrial, farm buildings, churches and HOA properties."), ("Do you handle hurricane claims?", "Washington doesn’t get hurricanes. Our storm work focuses on the Pacific windstorms, wildfires, ice and water events that cause most losses here.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Washington State",
                             "Insurance appraisal services across Washington: appraisal clause work, estimate review, windstorm, wildfire, water, snow and fire claims.",
                             body, [{"@type": "CollectionPage"}, itemlist(items)], trail, photo=photo), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        near = "".join(card(loc_path(LOC_BY[n]), lph(LOC_BY[n]), "Nearby", LOC_BY[n]["city"], LOC_BY[n]["county"], more="View") for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        photo = lph(l)
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        art = f"""<div class="note local"><b class="h">Local claim risks in {e(l["city"])}</b><ul class="chips">{chips}</ul><p class="housing"><b>Housing mix:</b> {e(l["housing"])}.</p></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and across {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2><div class="cards3 tight">{near}</div>"""
        aside = call_box() + list_box("Washington cities", items, path) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], f"Insurance Appraiser for {name}", l["lede"], photo,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + two_col(art, aside) + \
            cta_strip(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        city = l["city"]
        area = ({"@type": "City", "name": city, "containedInPlace": {"@type": "State", "name": "Washington"}} if l["slug"] != "tri-cities"
                else [{"@type": "City", "name": c, "containedInPlace": {"@type": "State", "name": "Washington"}} for c in ("Kennewick", "Pasco", "Richland")])
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": area, "url": DOMAIN + path}]
        title = f"{city} Insurance Appraiser | Disputed Claims, WA"
        if len(title) > 56:
            title = f"{city} Insurance Appraiser | WA Claims"
        desc = l.get("desc") or f"Independent insurance appraiser serving {city} and {l['county']}, WA. Appraisal and estimate review for underpaid property claims."
        write(path, document(path, title, desc, body, schema, trail, photo=photo), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cities = "".join(
        f'<a class="city rv" href="{loc_path(l)}">{img(lph(l), sizes="(max-width:700px) 50vw, 280px", alt="")}<span class="city-in"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    reg = ""
    for n, counties, t, photo, cs in REGIONS:
        links = ", ".join(f'<a href="{loc_path(LOC_BY[c])}">{e(LOC_BY[c]["city"])}</a>' for c in cs)
        reg += f'<div class="region rv">{img(ph(photo, "storm-sky"), sizes="(max-width:700px) 100vw, 380px", alt="")}<div class="region-in"><h3>{e(n)}</h3><p class="region-c">{e(counties)} counties</p><p>{e(t)}</p><p class="region-l">City pages: {links}</p></div></div>'
    photo = ph("mount-rainier", "seattle-skyline")
    body = page_hero(trail, "Statewide coverage", f"Insurance Appraisal in All {COUNTIES} Washington Counties",
                     f"{BRAND} works statewide, from Cape Flattery to Clarkston. These local pages cover the cities where we handle claims most often.", photo) + f"""
<section class="sec"><div class="wrap"><div class="cities" data-stagger>{cities}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across Washington</h2><p>The same policy language plays out very differently in a Bellevue condo, a Wenatchee foothills home and a wheat farm on the Palouse.</p></div><div class="regions" data-stagger>{reg}</div></div></section>
{cta_strip("Don’t see your city?", f"We cover all {COUNTIES} Washington counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Washington Cities We Serve | Insurance Appraisal",
                             "Insurance appraisal in all 39 Washington counties, including Seattle, Spokane, Tacoma, Vancouver, Bellevue, Everett, Yakima and the Tri-Cities.",
                             body, [{"@type": "CollectionPage"}, itemlist([(loc_label(l), loc_path(l)) for l in LOCATIONS])], trail, photo=photo), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        idx = TOOLS.index(t)
        others = "".join(card(f'{TOOL_BASE}{o["slug"]}/', ph(o["photo"]), f"Free {o['kind'].lower()}", o["name"], o["short"], more="Open") for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)])
        photo = ph(t["photo"])
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], photo, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice, and nothing you enter is stored.</p></div></section>
{two_col(t["explain"] + f'<h2>Questions about this calculator</h2>{faq_block(t["faqs"])}<h2>More free calculators</h2><div class="cards3 tight">{others}</div>', call_box() + list_box("All calculators", items, path))}
{cta_strip("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
                                           "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, trail, photo=photo), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(card(f'{TOOL_BASE}{t["slug"]}/', ph(t["photo"]), f"Free {t['kind'].lower()}", t["name"], t["short"], h="h2", more="Open") for t in TOOLS)
    photo = ph("calculator-desk")
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Washington Owners",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Use them to understand your claim, check the insurer’s math and decide on next steps. No sign-up, nothing stored.", photo, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards3" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-grid"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the calculators together</h2><ol class="numbered"><li>Start with the <a href="{TOOL_BASE}claim-timeline-planner/">claim timeline planner</a> so no deadline slips.</li><li>Check the roof math with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a> and <a href="{TOOL_BASE}replacement-cost-holdback-calculator/">holdback</a> calculators.</li><li>After a wildfire, run the <a href="{TOOL_BASE}wildfire-total-loss-coverage-check/">total-loss coverage check</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-payoff-calculator/">appraisal payoff calculator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-quiz/">readiness quiz</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Claim Calculators for Washington Property Owners",
                              "Free claim calculators: appraisal payoff, RCV holdback, roof squares, earthquake deductible, deadlines, readiness and a wildfire check.",
                              body, [{"@type": "CollectionPage"}, itemlist(items)], trail, photo=photo), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("How appraisal works", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS), ("Claim resources", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("How appraisal works", path)]
    photo = ph("clipboard-inspection")
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(t)}</a></li>' for i, (t, _) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Washington, Step by Step",
                     "Seven steps from the first disagreement to a signed award: what happens, who does what, and where claims most often go wrong.", photo,
                     [("Steps", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + \
        two_col(f'<nav class="toc" aria-label="Steps"><p class="toc-t">On this page</p><ol>{toc}</ol></nav>{PROCESS_BODY}', call_box() + list_box("Resources", LEARN, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Washington", "description": "The seven steps of a property insurance appraisal, from written demand to signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Washington | 7 Steps",
                         "A step-by-step guide to insurance appraisal in Washington: the written demand, choosing appraisers and an umpire, and the binding award.",
                         body, [howto], trail, photo=photo), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    photo = ph("living-room", "kitchen")
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal FAQ for Washington Property Owners",
                     "Plain answers to the questions we hear most, grouped by topic: the process, costs and timing, Washington rules and working with us.", photo) + \
        two_col(f'<nav class="toc" aria-label="Topics"><p class="toc-t">Topics</p><ol>{toc}</ol></nav>{groups}', call_box() + list_box("Resources", LEARN, path)) + \
        cta_strip("Didn’t see your question?", "Call or email and we’ll talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ | Washington Costs, Timing & Rules",
                         "Answers to common Washington insurance appraisal questions: how it works, what it costs, timing, OIC and IFCA basics, and when awards bind.",
                         body, [faq_schema(allq)], trail, photo=photo), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    photo = ph("paperwork-review")
    gl = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in gl})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in gl:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gl-item"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim Appraisal Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the search box to filter.", photo, cta=False) + \
        two_col(f'<div class="gl-search"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”" autocomplete="off"><p class="hint" data-gl-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl>',
                call_box() + list_box("Resources", LEARN, path))
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": f"{DOMAIN}{path}#definedtermset"}} for t, d in gl]}
    write(path, document(path, "Insurance Claim Glossary | ACV, RCV, Umpire & More",
                         "A searchable glossary of 40+ property claim terms, from actual cash value and holdback to IFCA, umpire and Xactimate, in plain English.",
                         body, [dts], trail, photo=photo), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim resources", POST_BASE), (p["title"], path)]
        idx = POSTS.index(p)
        others = "".join(card(f'{POST_BASE}{o["slug"]}/', ph(POST_PHOTO[o["slug"]]), "Guide", o["title"], o["summary"], more="Read") for o in [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        photo = ph(POST_PHOTO[p["slug"]])
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), photo, cta=False) + \
            two_col(f'{p["body"]}<p class="byline">Published by {BRAND} · {nice}. General information only, not legal advice.</p><h2>Keep reading</h2><div class="cards3 tight">{others}</div>',
                    call_box() + list_box("Resources", LEARN) + list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_strip()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{photo}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], trail, og_type="article", photo=photo), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim resources", path)]
    cards = "".join(card(f'{POST_BASE}{p["slug"]}/', ph(POST_PHOTO[p["slug"]]), f'{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read', p["title"], p["summary"], h="h2", more="Read") for p in POSTS)
    photo = ph("kitchen", "living-room")
    res = "".join(card(href, ph(pk), "Reference", n, d, h="h2", more="Open") for n, href, pk, d in [
        ("How insurance appraisal works", P_PROCESS, "clipboard-inspection", "The seven steps from written demand to signed award."),
        ("Appraisal FAQ", P_FAQ, "living-room", "Answers grouped by topic, including Washington rules."),
        ("Claim glossary", P_GLOSS, "paperwork-review", f"{len(GLOSSARY)} claim terms defined in plain English.")])
    body = page_hero(trail, "Guides & reference", "Insurance Claim Resources for Washington Owners",
                     "Practical guides on policy language, documentation and claim strategy, plus our process guide, FAQ and glossary.", photo, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="kicker">Reference</p><h2 class="sr-only">Reference pages</h2></div><div class="cards3" data-stagger>{res}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Guides</p><h2 class="sr-only">Guide articles</h2></div><div class="cards3" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    allitems = [(n, h) for n, h in LEARN[:3]] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]
    write(path, document(path, "Washington Insurance Claim Resources & Guides",
                         "Guides for Washington property owners on appraisal clauses, OIC complaints, windstorm and wildfire claims, frozen pipes and reading estimates.",
                         body, [{"@type": "CollectionPage"}, itemlist(allitems)], trail, photo=photo), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    photo = ph("consultation-table")
    art = f"""
<figure class="lead-img">{img(ph("clipboard-inspection"), sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most property claim professionals do a little of everything. We chose to specialize. {BRAND} works on one question: what is the amount of loss? Our process, our calculators and our documentation standards are all built around answering it well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute grows, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible over impressive.</strong> An inflated number might look good on day one, but it loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your situation needs an attorney, a public adjuster or a complaint to the OIC, we’ll tell you.</li>
<li><strong>Fees in writing.</strong> You know what it costs before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, business owners, farms, churches, contractors, public adjusters and attorneys across Washington. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and we don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t guarantee outcomes, because no honest appraiser can.</p>
<h2>Statewide, on purpose</h2>
<p>Washington’s property risks change completely across the Cascade crest. Working statewide means we see every kind of loss the state produces: windstorm and tree damage in Puget Sound, ice storms in Vancouver and Spokane, wildfire in Okanogan and Chelan counties, and hail and wind in the Columbia Basin. We price each with local knowledge.</p>
"""
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", photo) + \
        two_col(art, call_box() + list_box("Explore", [("Our services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free calculators", TOOL_BASE), ("How appraisal works", P_PROCESS)])) + cta_strip()
    write(path, document(path, f"About {BRAND} | Our Approach",
                         "Washington Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [{"@type": "AboutPage"}], trail, photo=photo), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    photo = ph("paperwork-review")
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", photo, cta=False) + f"""
<section class="sec deep"><div class="wrap contact-grid">
<div class="rv"><p class="kicker light">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-lines"><li>{ic("phone")}<div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><span>Hours</span><b>Mon–Fri, 8am–6pm Pacific</b></div></li><li>{ic("pin")}<div><span>Service area</span><b>Statewide, all {COUNTIES} counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Get a free review of a disputed Washington property claim. Call or text (844) 537-1427, or send your claim details using our secure form.",
                         body, [{"@type": "ContactPage"}], trail, photo=photo), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Statement", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect the information you choose to give us, such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working properly.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when the law requires it.</p>
<h2>Claim calculators</h2><p>Our calculators, planners and quiz run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                    "How we collect, use and protect the information you share with us.",
                    "Privacy Statement | Washington Insurance Appraiser",
                    "How Washington Insurance Appraiser collects, uses and protects details from forms, calls and emails. Our calculators store nothing you enter."),
        P_TERMS: ("Website Use Terms", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Washington.</p>
<h2>No professional relationship</h2><p>Reading this site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Talk to a licensed Washington attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from the information you enter. They are not appraisals, quotes or predictions of any claim outcome. Example figures are illustrative.</p>
<h2>Intellectual property</h2><p>Site content, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free public-domain or CC0 images.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Washington.</p>""",
                  "The terms that apply when you use this website and its calculators.",
                  "Website Use Terms | Washington Insurance Appraiser",
                  "Terms for using the Washington Insurance Appraiser website and its free calculators: no legal advice, no client relationship, no guarantees."),
        P_DISC: ("Disclaimers and Limits", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If a deadline is close, talk to a Washington attorney promptly.</p>
<h2>Laws and regulators</h2><p>References to Washington statutes, the Insurance Fair Conduct Act, regulations, the Office of the Insurance Commissioner or weather events are general and for context. Check current law and facts with official sources such as the OIC.</p>
<h2>Photographs</h2><p>Photos on this site are royalty-free public-domain and CC0 images used for illustration. They don’t show our clients’ properties.</p>""",
                "Important limits on the information published on this website.",
                "Disclaimers & Limits | Washington Insurance Appraiser",
                "Important limits on this site: general information only, not legal advice, no guaranteed results, and illustrative example figures throughout."),
    }
    photo = ph("commercial-building")
    for path, (title, content, lede, seo, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, photo, cta=False) + two_col(content, call_box())
        write(path, document(path, seo, desc, body, None, trail, photo=photo), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site directory", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Claim resources", POST_BASE), ("How appraisal works", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim glossary", P_GLOSS)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy statement", P_PRIVACY), ("Website use terms", P_TERMS), ("Disclaimers and limits", P_DISC)]),
    ]
    cols = "".join(f'<div class="dir-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    photo = ph("commercial-building")
    body = page_hero(trail, "Navigation", "Site Directory", f"Every page on {BRAND}, grouped by section.", photo, cta=False) + f'<section class="sec"><div class="wrap"><div class="dir" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Directory | {BRAND}",
                         "A complete list of every page on Washington Insurance Appraiser: services, city pages, free claim calculators, guides and legal pages.",
                         body, None, trail, photo=photo), 0.3)

    photo = ph("storm-sky")
    body = f"""<section class="phero err"><div class="phero-bg">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page went down in the windstorm</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-y" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Services</a><a class="btn btn-line light" href="{TOOL_BASE}">Free calculators</a><a class="btn btn-line light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found (404) | {BRAND}",
                                "Sorry, this page could not be found. Try the Washington Insurance Appraiser homepage, our services, free calculators or contact page instead.",
                                body, None, [("Home", "/"), ("Page not found", "/404.html")], robots="noindex,follow", photo=photo), sitemap=False)


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
// Washington Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$wia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$wia_real  = 'washingtoninsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$wia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://washingtoninsuranceappraiser.com - only on the real domain.
if ($wia_host === 'www.' . $wia_real || ($wia_host === $wia_real && $wia_proto === 'http')) {
    header('Location: https://' . $wia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$wia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($wia_uri, '?'), $wia_m)) {
    $wia_q = strpos($wia_uri, '?') !== false ? substr($wia_uri, strpos($wia_uri, '?')) : '';
    header('Location: ' . $wia_m[1] . $wia_q, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($wia_host !== $wia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Washington Insurance Appraiser - front controller for the static build.
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
