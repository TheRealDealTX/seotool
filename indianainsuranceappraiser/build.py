#!/usr/bin/env python3
"""Static site generator for indianainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
"""
import html
import json
import os
import re
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

BRAND = "Indiana Insurance Appraiser"
HOST = "indianainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261117a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM output.
GTM_ID = "GTM-5MGHQLMK"
# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/indiana-claim-appraisal/"
LOC_BASE = "/hoosier-cities/"
TOOL_BASE = "/claim-gap-tools/"
POST_BASE = "/claim-dispute-guides/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"
PROCESS = "/appraisal-process-indiana/"
FAQ_P = "/indiana-appraisal-questions/"
GLOSS = "/insurance-appraisal-terms/"
PRIVACY = "/privacy/"
TERMS = "/terms/"
DISCL = "/legal-disclaimer/"
HTMLMAP = "/html-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraisal/"


def post_url(p):
    return f"{POST_BASE}{p['slug']}/"


def loc_label(l):
    return f"{l['city']}, IN"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
ALT = {}
try:
    from alts import ALT  # noqa: E402,F811
except ImportError:
    pass


def alt_for(key):
    return ALT.get(key) or PHOTOS[key].get("desc") or PHOTOS[key].get("title", "")


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else alt_for(key))
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    small = f'/assets/img/photos/{key}-640.webp 640w, ' if p["fw"] > 640 else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="{small}/assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-appraiser": "consultation", "home-insurance-claim-appraisal": "suburban-home",
    "commercial-hoa-claim-appraisal": "commercial-building", "hail-roof-damage-appraisal": "hail-roof",
    "tornado-wind-damage-appraisal": "tornado-damage", "water-damage-claim-appraisal": "water-ceiling",
    "fire-smoke-damage-appraisal": "fire-damage", "ice-dam-freeze-snow-load-appraisal": "icicles-house",
    "farm-outbuilding-claim-appraisal": "farm-barn", "carrier-estimate-review": "laptop-spreadsheet",
    "appraisal-umpire-services": "documents-review",
}
LOC_PHOTO = {
    "indianapolis": "indianapolis-skyline", "fort-wayne": "fort-wayne", "evansville": "evansville", "south-bend": "south-bend",
    "carmel": "carmel", "fishers": "suburban-home", "bloomington": "bloomington", "hammond": "hammond",
    "lafayette": "lafayette", "kokomo": "kokomo", "terre-haute": "terre-haute", "jeffersonville": "jeffersonville",
}
TOOL_PHOTO = {
    "claim-gap-net-recovery-estimator": "calculator", "rcv-acv-holdback-calculator": "laptop-spreadsheet",
    "roof-pitch-squares-calculator": "shingle-roof", "percentage-deductible-calculator": "hailstones",
    "claim-timeline-builder": "documents-review", "appraisal-readiness-checkup": "consultation",
    "roof-snow-load-estimator": "snow-roof",
}
POST_PHOTO = {
    "ice-dams-and-indiana-homeowners-policies": "icicles-house", "documenting-tornado-and-derecho-damage": "tornado-debris",
    "matching-discontinued-shingles-after-hail": "shingle-roof", "indiana-department-of-insurance-and-your-claim": "consultation",
    "releases-final-payments-and-holdback": "calculator", "appraisal-or-litigation-indiana": "documents-review",
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
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=44):
    # Navy tile, gold roof chevron over a white balance beam: "property + fair valuation".
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#002D62"/>'
            '<path d="M10 22.5L24 11l14 11.5" fill="none" stroke="#FDBB30" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M13 30h22M24 22v15M18 37h12" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="M13 30l-3 6h6zM35 30l-3 6h6z" fill="#BEC0C2"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "IN", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-IN", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Indiana property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 92 Indiana counties.",
        "areaServed": [{"@type": "State", "name": "Indiana"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail damage", "Tornado and wind claims", "Ice dams and snow load"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a))}} for q, a in faqs]}


def item_list(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Indiana cities", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All claim tools", TOOL_BASE)),
        ("Resources", [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_P), ("Appraisal glossary", GLOSS), ("Claim dispute guides", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="dropdown{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head" id="top"><div class="wrap head-in">
{brand()}
<nav class="primary" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-gold head-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false">{ic("menu")}</button>
</div><div class="progress" aria-hidden="true"><span></span></div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-drawer")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 92 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="checker" aria-hidden="true"></div>
<div class="wrap foot-grid">
<div class="foot-brand">{brand("brand brand-foot")}
<p>Independent appraisal and estimating for Indiana property owners whose insurance claims came up short, from Lake Michigan’s snow belt to the Ohio River towns.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{ic("phone")}{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a></li><li>{ic("clock")}Mon–Fri 8am–6pm ET</li></ul></div>
<div><p class="foot-h">Services</p><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><p class="foot-h">Indiana cities</p><ul class="two">{loc}</ul></div>
<div><p class="foot-h">Free tools</p><ul>{tl}</ul></div>
<div><p class="foot-h">Resources</p><ul><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Site content is general and educational; policy terms vary and results are never guaranteed. Example figures are illustrative.</p>
<div class="foot-bar"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCL}">Disclaimer</a></li><li><a href="{HTMLMAP}">Site map</a></li></ul></div></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("mail")} Free review</a></div>"""


# Google tag snippet exactly as supplied by the site owner (head only; no noscript part was supplied).
GTM_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-5MGHQLMK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>
"""


def gtm_head():
    if GTM_SNIPPET:
        return GTM_SNIPPET
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if GTM_SNIPPET or not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-storm-home", page_type="WebPage", main_entity=None):
    canonical = DOMAIN + (path if path != "/404.html" else "/404.html")
    extra_nodes, crumb_id = [], None
    for n in (schema or []):
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    pimg = PHOTOS[photo]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    if main_entity is None:
        pref = ["Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"]
        found = [n["@id"] for t in pref for n in extra_nodes if n.get("@type") == t]
        main_entity = found[0] if found else DOMAIN + "/#business"
    webpage["mainEntity"] = {"@id": main_entity}
    graph = [org_schema(), site_schema(), webpage] + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Indiana">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Indiana">
<meta name="geo.region" content="US-IN">
<meta name="geo.placename" content="Indiana">
<meta name="theme-color" content="#002D62">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Merriweather+Sans:ital,wght@0,400;0,600;0,700;1,400&family=Oswald:wght@500;600;700&display=swap">
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
    # Directory pages are written as dir/index.php: the host serves real files without running the
    # front controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if rel.endswith("/index.php"):
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
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box call-box"><p class="side-h">Talk it through</p><p>A free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="call-num" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><p class="side-h">{e(title)}</p><ul class="side-list">{li}</ul></div>'


def cta_band(h="Is the carrier’s number short?", p="Send us the estimate. We’ll read it line by line and tell you what we see."):
    return f"""<section class="cta-band"><div class="checker thin" aria-hidden="true"></div><div class="wrap cta-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line light" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="sidebar"><div class="sticky">{aside}</div></aside></div>'


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span></a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Tornado / wind", "Water / pipe burst", "Ice dam / snow load", "Fire / smoke", "Farm building", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hid="f"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Farm owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Indiana"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-h">{e(heading)}</p><p class="form-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{hid}-amt">Approx. amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<p class="form-h">Get a free claim review</p><p class="form-sub">Three fields. We call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What was damaged?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="form-trust">{ic("shield")}No obligation. Your details stay private.</p>
</form>"""


def svc_card(s, i, h="h3"):
    return f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="card-no">{i + 1:02d}</span></span><span class="card-b"><{h}>{e(s["name"])}</{h}><span class="card-p">{e(s["short"])}</span><span class="card-more">View service {ic("arrow")}</span></span></a>'


def tool_card(t, h="h3"):
    return f'<a class="card tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}<span class="card-tag">{e(t["kind"])}</span></span><span class="card-b"><{h}>{e(t["name"])}</{h}><span class="card-p">{e(t["short"])}</span><span class="card-more">Open tool {ic("arrow")}</span></span></a>'


def city_card(l, h="h3"):
    return f'<a class="city rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, (max-width:1100px) 50vw, 300px", alt="")}<span class="city-b"><{h}>{e(l["city"])}</{h}><small>{e(l["county"])} · {e(l["region"])}</small></span></a>'


def post_card(p, h="h3"):
    u = f'{POST_BASE}{p["slug"]}/'
    return f'<article class="post rv"><a class="post-ph" href="{u}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</a><div class="post-b"><p class="post-meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><{h}><a href="{u}">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>'


# ---------------------------------------------------------------- home
ZONES = [
    ("lake", "Lake Michigan snow belt", "Hammond · South Bend · LaPorte", ["Lake-effect snow load", "Ice dams", "Frozen pipes", "Wind off the lake"],
     "Lake County, Porter, LaPorte, St. Joseph and Elkhart counties get Indiana’s heaviest snow. Low-slope additions, porch roofs and pole barns take the load, and ice dams send meltwater into ceilings every winter.",
     ["hammond", "south-bend"], "snow-roof"),
    ("central", "Central hail corridor", "Indianapolis · Carmel · Fishers · Kokomo", ["Hail", "Straight-line wind", "Tornadoes", "Basement water"],
     "Storms crossing from the west regularly drop hail on Marion and Hamilton counties. Fast-growing suburbs share discontinued shingle and siding lines, so matching disputes follow nearly every big storm.",
     ["indianapolis", "carmel", "fishers", "kokomo"], "hail-roof"),
    ("wabash", "Wabash Valley & farm country", "Lafayette · Terre Haute · Fort Wayne", ["Tornadoes", "Derechos", "Farm buildings", "River flooding"],
     "Open farmland lets storms build fast. Pole barns, grain bins and farmhouses in Tippecanoe, Vigo, Allen and the counties between them see wind and hail losses that need structure-by-structure valuation.",
     ["lafayette", "terre-haute", "fort-wayne"], "supercell"),
    ("south", "Southern hills & Ohio River", "Evansville · Bloomington · Jeffersonville", ["Ice storms", "Tornadoes", "Tree damage", "Karst ground"],
     "Wooded hills, limestone country and river towns. Ice storms bring limbs down on roofs, tornadoes like Henryville’s in 2012 cut long paths, and historic brick and stone homes need specialized pricing.",
     ["evansville", "bloomington", "jeffersonville"], "ice-storm-trees"),
]

STORMS = [
    ("1937", "Ohio River flood", "Record flooding swamped Evansville, Jeffersonville and river towns, leading to today’s floodwalls."),
    ("1965", "Palm Sunday outbreak", "April 11 tornadoes struck northern and central Indiana, the deadliest tornado day in state history."),
    ("1974", "Super Outbreak", "On April 3, tornadoes hit communities across Indiana, including Monticello and Madison."),
    ("2005", "Evansville tornado", "A pre-dawn November 6 tornado tore through Vanderburgh and Warrick counties."),
    ("2008", "Floods and Ike’s winds", "June floods hit central and southern Indiana; in September, Ike’s remnants brought widespread wind damage."),
    ("2009", "Southern ice storm", "January freezing rain downed trees and power lines across southern Indiana."),
    ("2012", "Henryville and the derecho", "A March 2 tornado devastated Henryville; a June 29 derecho swept the state."),
    ("2023", "Sullivan tornado", "A March 31 tornado struck Sullivan in the Wabash Valley."),
]

GAP_LINES = [
    ("Roof slopes approved", 9600, 18400),
    ("Gutters, vents and soft metals", 0, 2350),
    ("Siding (matching elevations)", 2100, 6900),
    ("Interior ceiling and insulation", 1400, 3100),
    ("Overhead and profit", 0, 3080),
]


def home():
    zone_tabs = "".join(
        f'<button type="button" role="tab" id="zt-{k}" aria-controls="zp-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><b>{e(n)}</b><small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(ZONES))
    zone_panels = "".join(
        f'<div class="zone-panel" role="tabpanel" id="zp-{k}" aria-labelledby="zt-{k}"{"" if i == 0 else " hidden"}><div class="zone-ph">{img(ph, sizes="(max-width:900px) 100vw, 640px", alt="")}</div><div class="zone-b"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p><p class="zone-links">City pages: {", ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]["city"])}</a>" for c in cities)}</p></div></div>'
        for i, (k, n, _s, perils, t, cities, ph) in enumerate(ZONES))

    tot_c = sum(c for _, c, _ in GAP_LINES)
    tot_y = sum(y for _, _, y in GAP_LINES)
    mx = max(y for _, _, y in GAP_LINES)
    gap_rows = "".join(f'<li><span class="gl-n">{e(n)}</span><span class="gl-bars"><span class="gl-c" style="--w:{c / mx * 100:.1f}%"></span><span class="gl-y" style="--w:{y / mx * 100:.1f}%"></span></span><span class="gl-v">${c:,} → ${y:,}</span></li>' for n, c, y in GAP_LINES)

    steps = [
        ("Free review", "We read your policy, the carrier’s estimate and your photos and tell you plainly whether appraisal fits."),
        ("Independent scope", "Our own inspection, measurements and a line-item estimate priced for your Indiana ZIP code."),
        ("Written demand", "Appraisal is demanded in writing and Indiana Insurance Appraiser is named as your appraiser on time."),
        ("Panel negotiation", "We work line by line with the carrier’s appraiser. Most of the gap is settled here."),
        ("Signed award", "Anything left goes to a neutral umpire. Two of three signatures set the amount of loss."),
    ]
    tl = "".join(f'<li class="tl-step"><span class="tl-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    storms = "".join(f'<li class="rv"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for y, t, p in STORMS)

    home_faqs = [
        ("What does an Indiana Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your named appraiser we inspect, build an independent line-item estimate, negotiate with the carrier’s appraiser and present unresolved items to the umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside your policy’s appraisal clause on one question, the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When should I call an Indiana Insurance Appraiser?", "When coverage is accepted, you have the carrier’s estimate, and the gap to your contractor’s number is meaningful, roughly more than 10% or several thousand dollars."),
        ("Is the award binding?", "Yes, on the amount of loss, once any two of the three panel members sign it. That’s why the file should be complete before appraisal is demanded."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before any work starts, and the first conversation is free."),
        ("Do you work outside Indianapolis?", "Yes. We cover all 92 Indiana counties, from Lake County to Posey County and from Fort Wayne to Jeffersonville."),
    ]

    words = f"{BRAND} for claims that came up short"
    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-storm-home", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker gold">All 92 counties · Independent · Policyholder side</p>
<h1>{e(BRAND)} <span>for storm, water and fire claims that came up short</span></h1>
<p class="lede">Your carrier accepted the claim, but the check won’t cover the repair. {BRAND} builds an independent, line-by-line valuation of your loss and takes it through the appraisal clause already written into your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line light" href="#gap">See where claims fall short {ic("arrow")}</a></div>
<ul class="ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Indiana ZIP-code pricing</li><li>{ic("check")}Homes, HOAs, farms &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="counters" aria-label="At a glance"><div class="wrap counters-in">
<div><b data-count="92">92</b><span>Indiana counties covered</span></div>
<div><b data-count="11">11</b><span>Appraisal services</span></div>
<div><b data-count="7">7</b><span>Free claim tools</span></div>
<div><b data-count="12">12</b><span>City guides</span></div>
<div><b>2 of 3</b><span>Signatures bind the award</span></div>
</div></section>

<section class="sec" id="gap"><div class="wrap split">
<div class="rv">
<p class="kicker">Anatomy of a short claim</p>
<h2>Where an Indiana Insurance Appraiser finds the missing money</h2>
<p>Most underpaid claims aren’t denied. They’re short: two roof slopes instead of four, gutters left off, a siding elevation that can’t be matched, no overhead and profit. {BRAND} rebuilds the scope from your property, not from the carrier’s estimate, so the missing lines show up.</p>
<p>The chart is an illustrative hail claim on a central Indiana two-story. The carrier’s estimate totals ${tot_c:,}. An independent line-item scope for the same storm comes to ${tot_y:,}. That ${tot_y - tot_c:,} difference is exactly the kind of gap the appraisal clause exists to resolve.</p>
<a class="btn btn-navy" href="{SVC_BASE}carrier-estimate-review/">Start with an estimate review {ic("arrow")}</a>
</div>
<div class="gap-chart rv"><p class="gap-h">Illustrative hail claim · carrier vs. independent scope</p><ul class="gap-lines">{gap_rows}</ul><div class="gap-key"><span><i class="gl-c"></i>Carrier estimate</span><span><i class="gl-y"></i>Independent scope</span></div><p class="gap-tot"><span>Totals</span><b>${tot_c:,} → ${tot_y:,}</b></p><p class="fine">Illustrative figures only, not a client result.</p></div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Eleven services</p><h2>How Indiana Insurance Appraiser helps with your claim</h2><p>Every service is built around one job: a valuation of your loss that holds up in front of the carrier’s appraiser and an umpire. Start with a review, or bring us in once appraisal has been demanded.</p></div>
<div class="cards" data-stagger>{"".join(svc_card(s, i) for i, s in enumerate(SERVICES))}</div>
<p class="center mt"><a class="btn btn-line" href="{SVC_BASE}">Compare all appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec navy" id="process"><div class="wrap">
<div class="sec-head rv"><p class="kicker gold">Five steps</p><h2>From stuck claim to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how an Indiana Insurance Appraiser file moves from the first call to the award.</p></div>
<ol class="tl" data-tl><span class="tl-track" aria-hidden="true"><span class="tl-fill"></span></span>{tl}</ol>
<p class="center mt"><a class="link-light" href="{PROCESS}">Read the full appraisal process guide</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker">Four claim zones</p><h2>From the snow belt to the river towns: Indiana’s claim zones</h2><p>An Indiana Insurance Appraiser has to know how each part of the state’s weather shows up on a roof and in an estimate. Pick a zone to see what we see there.</p></div>
<div class="zones rv" data-tabs><div class="zone-tabs" role="tablist" aria-label="Indiana claim zones">{zone_tabs}</div>{zone_panels}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Storm almanac</p><h2>The storms that shaped Indiana claims</h2><p>Every Indiana Insurance Appraiser file sits against this history. These events changed building codes, floodwalls and how carriers look at wind, water and ice in the state.</p></div>
<ol class="almanac" data-stagger>{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free claim tools from Indiana Insurance Appraiser</h2><p>Run the numbers before you call. Every tool works in your browser, and nothing you type is stored or sent.</p></div>
<div class="cards" data-stagger>{"".join(tool_card(t) for t in TOOLS)}</div>
</div></section>

<section class="sec navy"><div class="wrap split">
<div class="rv"><p class="kicker gold">Quick check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. If the difference is large, a conversation with an Indiana Insurance Appraiser makes sense. If it’s small, a documented supplement request may close it faster and for less.</p><p>The full <a class="link-light" href="{TOOL_BASE}claim-gap-net-recovery-estimator/">claim gap and net recovery estimator</a> adds appraiser and umpire fees and compares three scenarios.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Twelve city guides</p><h2>Indiana Insurance Appraiser in your city</h2><p>We work in every county. These guides cover the cities where we handle claims most often, with local housing, storm history and the disputes we see there.</p></div>
<div class="cities" data-stagger>{"".join(city_card(l) for l in LOCATIONS)}</div>
<p class="center mt"><a class="btn btn-line" href="{LOC_BASE}">See all Indiana coverage {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Straight answers</p><h2>Is appraisal the right tool for your claim?</h2><p>An Indiana Insurance Appraiser is the right call for some problems and the wrong one for others. We’ll tell you which on the first call.</p></div>
<div class="fit" data-stagger>
<div class="fit-yes rv"><h3>{ic("check")} Appraisal usually fits</h3><ul><li>Coverage accepted, cost disputed</li><li>Partial vs. full roof or siding replacement</li><li>Matching and discontinued materials</li><li>Missing trades, code items and overhead and profit</li><li>Snow-load, ice dam and wind scope disagreements</li></ul></div>
<div class="fit-no rv"><h3>{ic("x")} Call someone else</h3><ul><li>The claim was denied outright: see an Indiana attorney</li><li>Bad-faith or conduct claims: courts decide these</li><li>A suit deadline is days away: attorney first</li><li>Gaps too small to cover appraisal fees</li><li>River flooding under a homeowners policy: usually excluded</li></ul></div>
<div class="fit-who rv"><h3>Who does what</h3><dl><dt>Appraiser</dt><dd>Values the amount of loss inside the appraisal clause.</dd><dt>Public adjuster</dt><dd>Manages and negotiates the whole claim for a fee.</dd><dt>Attorney</dt><dd>Handles denials, coverage fights, bad faith and lawsuits.</dd></dl></div>
</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions for an Indiana Insurance Appraiser</h2><p>How appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_P}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from the Indiana Insurance Appraiser team on policy language, documentation and strategy.</p></div>
<div class="posts" data-stagger>{"".join(post_card(p) for p in POSTS[:3])}</div>
<p class="center mt"><a class="btn btn-line" href="{POST_BASE}">All claim dispute guides {ic("arrow")}</a></p>
</div></section>

<section class="sec navy" id="contact"><div class="wrap split top">
<div class="rv"><p class="kicker gold">Start here</p><h2>Talk to an Indiana Insurance Appraiser today</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure, no obligation.</p>
<ul class="contact-list"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 92 Indiana counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hid="c")}</div>
</div></section>
"""
    schema = [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Indiana Insurance Appraiser: independent appraisal and estimate review for underpaid hail, wind, water, ice and fire claims statewide.",
                        body, schema, photo="hero-storm-home", main_entity=DOMAIN + "/#business"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        art = s["body"] + f"""<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}"""
        aside = call_box() + list_box("All services", items, path) + list_box("Indiana cities", locs + [("All Indiana cities", LOC_BASE)])
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + layout(art, aside) + cta_band()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Indiana"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Indiana Property Claims",
                     "From a single estimate review to full panel representation and neutral umpire work, every Indiana Insurance Appraiser service centers on an accurate, defensible valuation of your loss.", "roofer") + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{"".join(svc_card(s, i, "h2") for i, s in enumerate(SERVICES))}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn btn-navy" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle farm and commercial claims?", "Yes: farms, pole barns, retail, office, industrial, churches, apartments and HOA properties."), ("Is it only hail?", "No. We value wind, tornado, water, ice dam, snow-load, fire and other covered losses.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Indiana",
                             "Indiana insurance appraisal services: appraisal clause representation, estimate review, hail, wind, water, winter, farm and umpire work.",
                             body, [crumbs_schema(trail), item_list(items)], photo="roofer", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Indiana cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
        art = f"""<div class="local-card"><p class="local-h">Local snapshot</p><dl><div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Region</dt><dd>{e(l["region"])}</dd></div><div><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div></dl><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby city guides</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}"""
        aside = call_box() + list_box("Indiana cities", items, path) + list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On-site")]) + layout(art, aside) + cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Indiana"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {l['city']}, IN | Claim Appraisal"
        if len(title) > 58:
            title = f"Insurance Appraiser {l['city']}, IN | Claims"
        desc = l.get("desc") or f"Insurance appraiser for {l['city']} and {l['county']}: independent appraisal and estimate review for underpaid storm, water and fire claims."
        if len(desc) > 143:
            desc = f"Insurance appraiser for {l['city']}, {l['county']}: independent appraisal and estimate review for underpaid storm and water claims."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Indiana cities", LOC_BASE)]
    zones = "".join(f'<div class="zone-card rv"><div class="zone-card-ph">{img(ph, sizes="(max-width:700px) 100vw, 50vw", alt="")}</div><div class="zone-card-b"><p class="kicker">{e(s)}</p><h2>{e(n)}</h2><p>{e(t)}</p><p class="zone-links">{", ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]["city"])}</a>" for c in cs)}</p></div></div>' for k, n, s, _p, t, cs, ph in ZONES)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 92 Indiana Counties",
                     "Indiana Insurance Appraiser works statewide, from the Lake Michigan shore to the Ohio River. These city guides cover the places we handle claims most often.", "indiana-cornfield") + f"""
<section class="sec"><div class="wrap"><div class="cities" data-stagger>{"".join(city_card(l, "h2") for l in LOCATIONS)}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head left rv"><p class="kicker">Claim zones</p><h2>How claims differ across Indiana</h2><p>The same policy language plays out very differently in a South Bend bungalow under three feet of snow, a Fishers two-story after hail and an Evansville Victorian after an ice storm.</p></div><div class="zone-cards">{zones}</div></div></section>
{cta_band("Don’t see your city?", "We cover every Indiana county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Indiana Insurance Appraiser Cities | 92 Counties",
                             "Insurance appraisal in all 92 Indiana counties, with city guides for Indianapolis, Fort Wayne, Evansville, South Bend, Carmel and more.",
                             body, [crumbs_schema(trail), item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="indiana-cornfield", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + f"""<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}"""
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice.</p></div></section>""" + layout(art, call_box() + list_box("All claim tools", items, path)) + cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for Indiana Property Owners",
                     "Seven calculators and planners built from real appraisal work. Check the carrier’s math, see what you’re owed and plan next steps. No sign-up, nothing stored.", "laptop-spreadsheet", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{"".join(tool_card(t, "h2") for t in TOOLS)}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-timeline-builder/">claim timeline builder</a> so nothing lapses.</li><li>Check roof math with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’ll actually receive with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">holdback</a> calculators.</li><li>Size the dispute with the <a href="{TOOL_BASE}claim-gap-net-recovery-estimator/">claim gap estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol><p>Winter claim? The <a href="{TOOL_BASE}roof-snow-load-estimator/">roof snow load estimator</a> shows what lake-effect snow and ice weigh.</p></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Indiana",
                              "Free Indiana claim tools: gap estimator, RCV/ACV holdback, roof squares, percentage deductible, timeline builder and snow load estimator.",
                              body, [crumbs_schema(trail), item_list(items)], photo="laptop-spreadsheet", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    learn_items = [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_P), ("Appraisal glossary", GLOSS), ("Claim dispute guides", POST_BASE)]

    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Indiana",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what and where Indiana claims most often go wrong.", "documents-review",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(PROCESS_BODY, call_box() + list_box("Resources", learn_items, path)) + cta_band()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Indiana", "description": "The stages of a property insurance appraisal under a typical Indiana policy.", "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Indiana Insurance Appraisal Process | 7 Steps",
                         "The Indiana insurance appraisal process in seven steps: the written demand, appraisers and umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="documents-review"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    allq = [qa for _, qs in FAQ for qa in qs]
    jump = '<nav class="jump" aria-label="FAQ topics">' + "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ)) + "</nav>"
    groups = jump + "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    body = page_hero(trail, "Answers", "Indiana Insurance Appraisal FAQ",
                     "Plain answers to the questions we hear most about the appraisal process, costs, deadlines and how Indiana rules fit in.", "brick-home") + layout(groups, call_box() + list_box("Resources", learn_items, path)) + cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")
    write(path, document(path, "Indiana Insurance Appraisal FAQ | Costs & Timing",
                         "Indiana insurance appraisal FAQ grouped by topic: how appraisal works, what it costs, deadlines, the FAIR Plan and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="brick-home"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Appraisal glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"g-item\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    art = f'<div class="filter"><label for="gloss-filter">Search {len(GLOSSARY)} terms</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”" autocomplete="off"></div><p class="g-count" data-gcount aria-live="polite"></p><div class="az">{az}</div><dl class="glossary">{dl}</dl>'
    body = page_hero(trail, "Reference", "Insurance Appraisal Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in Indiana policies, estimates and appraisal awards, defined in plain English.", "calculator", cta=False) + layout(art, call_box() + list_box("Resources", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary | ACV, RCV, Umpire",
                         "Searchable insurance appraisal glossary: plain-English definitions of ACV, RCV, depreciation, umpire, ice dams, O&P and 30-plus more terms.",
                         body, [crumbs_schema(trail), dts], photo="calculator"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = p["body"] + f"<h2>Keep reading</h2>{related([('Guide', o['title'], post_url(o)) for o in others])}"
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", learn_items) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + cta_band()
        bp = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "publisher": {"@id": DOMAIN + "/#business"}, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), bp], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    body = page_hero(trail, "Claim dispute guides", "Claim Dispute Guides for Indiana Property Owners",
                     "Practical guides on policy language, documentation and claim strategy, written by people who work appraisal panels.", "victorian-home", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{"".join(post_card(p, "h2") for p in POSTS)}</div></div></section>{cta_band()}"""
    write(path, document(path, "Indiana Claim Dispute Guides | Appraisal Help",
                         "Indiana claim dispute guides on ice dams, wind damage, matching shingles, the Department of Insurance, releases and appraisal vs. lawsuits.",
                         body, [crumbs_schema(trail), item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="victorian-home", page_type="CollectionPage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    explore = [("Our services", SVC_BASE), ("Indiana cities", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROCESS)]
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    art = f"""<figure class="lead-img">{img("consultation", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a little of everything. {BRAND} works on one question, the amount of loss, and we built our process, documentation and tools around answering it well. That focus lets us serve as your named appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible, not inflated.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain English.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so.</li>
<li><strong>Fees in writing</strong> before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, farm families, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Indiana. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t guarantee outcomes, and no honest appraiser can.</p>
<h2>Statewide, by design</h2>
<p>Indiana’s weather changes from one end of the state to the other: lake-effect snow in South Bend, hail in Carmel, derechos across the Wabash Valley, ice storms and tornadoes along the Ohio River. Working all 92 counties means we see every kind of loss the state produces and price each one with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We’re estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "roofer") + layout(art, call_box() + list_box("Explore", explore)) + cta_band()
    write(path, document(path, f"About {BRAND} | Our Approach",
                         "About Indiana Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss in disputed claims.",
                         body, [crumbs_schema(trail)], photo="roofer", page_type="AboutPage"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "documents-review", cta=False) + f"""
<section class="sec navy"><div class="wrap split top">
<div class="rv"><p class="kicker gold">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-list"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 92 Indiana counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticklist"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, hid="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Contact Indiana Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, or send your claim details.",
                         body, [crumbs_schema(trail)], photo="documents-review", page_type="ContactPage"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | Indiana Insurance Appraiser",
                  "Indiana Insurance Appraiser privacy policy: what we collect through forms, calls and email, how we use it and the choices you have.",
                  "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to give us, such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data such as IP address, browser type and pages requested, for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. What you enter isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, this policy will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "Terms of Use | Indiana Insurance Appraiser",
                "Terms of use for the Indiana Insurance Appraiser website, its claim calculators and its general information about property claims.",
                "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Indiana.</p>
<h2>No professional relationship</h2><p>Reading the site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Indiana attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates based on what you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free public-domain or CC0 images used for illustration only.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Indiana.</p>"""),
        DISCL: ("Legal Disclaimer", "Legal Disclaimer | Indiana Insurance Appraiser",
                "Legal disclaimer for Indiana Insurance Appraiser: general information only, not legal advice, illustrative figures and no guarantee of results.",
                "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>Content on this site is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Bad faith and legal claims</h2><p>References on this site to good faith, bad faith or unfair claim practices are general descriptions only. Whether any insurer acted improperly is a legal question for an Indiana attorney.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an Indiana attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free public-domain and CC0 images used for illustration. They do not show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to statutes, agencies and weather events are for context. Verify current law and facts with official sources such as the Indiana Department of Insurance and the National Weather Service.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "commercial-building", cta=False) + layout(content, call_box())
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)


def sitemap_pages():
    path = HTMLMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main pages", [("Home", "/"), ("About us", ABOUT), ("Contact us", CONTACT)]),
        ("Appraisal services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Indiana cities", [("All Indiana cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Free claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_P), ("Appraisal glossary", GLOSS), ("Claim dispute guides", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Legal disclaimer", DISCL)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on the {BRAND} website, grouped by section.", "indiana-cornfield", cta=False) + f'<section class="sec"><div class="wrap map-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}",
                         "HTML site map for Indiana Insurance Appraiser listing every service, Indiana city guide, free claim tool, resource and legal page.",
                         body, [crumbs_schema(trail)], photo="indiana-cornfield"), 0.3)

    body = f"""<section class="phero err"><div class="phero-bg">{img("supercell", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page blew off the map</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Services</a><a class="btn btn-line light" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "Sorry, this Indiana Insurance Appraiser page could not be found. Use the links here to reach our services, free tools or contact page.",
                                body, robots="noindex,follow", photo="supercell"), sitemap=False)


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
    # Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Indiana Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$iia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$iia_real  = 'indianainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$iia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://indianainsuranceappraiser.com - only on the real domain.
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
// Keep temporary preview domains out of search results.
if ($iia_host !== $iia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Indiana Insurance Appraiser - front controller for the static build.
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
