#!/usr/bin/env python3
"""Static site generator for oklahomainsuranceappraiser.com.

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

from services import SERVICES, SERVICE_GROUPS  # noqa: E402
from locations import LOCATIONS, REGIONS  # noqa: E402
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json"), encoding="utf-8"))
if os.environ.get("OIA_STUB_PHOTOS"):  # dev only: build before photos exist
    import collections
    PHOTOS = collections.defaultdict(lambda: {"fw": 1200, "fh": 800}, PHOTOS)

BRAND = "Oklahoma Insurance Appraiser"
HOST = "oklahomainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261113a"
FAV = "1"
# Google Tag Manager container ID (e.g. "GTM-XXXXXXX"). Empty = no GTM snippet is output.
GTM_ID = ""
# Google Search Console HTML verification file: written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/appraiser-services/"
LOC_BASE = "/cities-we-serve/"
TOOL_BASE = "/calculators-and-planners/"
POST_BASE = "/storm-claim-guides/"
PROCESS = "/the-appraisal-process/"
FAQ_P = "/appraisal-questions/"
GLOSS = "/insurance-claim-terms/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"
PRIVACY = "/privacy/"
TERMS = "/terms/"
DISCLAIM = "/disclaimer/"
SITEMAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml

SVC_BY = {s["slug"]: s for s in SERVICES}
LOC_BY = {l["slug"]: l for l in LOCATIONS}
LEARN = [("The appraisal process", PROCESS), ("Appraisal questions", FAQ_P), ("Insurance claim terms", GLOSS), ("Storm claim guides", POST_BASE)]


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


# ---------------------------------------------------------------- photos
from photo_alt import ALT  # noqa: E402  (alt text per photo key, kept next to photos.json)


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consultation", "home-insurance-appraiser": "brick-ranch-home",
    "commercial-hoa-claim-appraisal": "commercial-building", "hail-roof-damage-appraiser": "hailstones",
    "tornado-windstorm-claim-appraisal": "tornado-damage-street", "water-pipe-leak-claim-appraisal": "rain-gutter",
    "fire-smoke-loss-appraisal": "house-fire", "ice-storm-tree-damage-appraisal": "ice-storm-trees",
    "wildfire-grassfire-claim-appraisal": "grass-wildfire", "earthquake-crack-claim-appraisal": "suburban-home",
    "carrier-estimate-review": "laptop-numbers", "appraisal-umpire-services": "clipboard-inspector",
}
LOC_PHOTO = {
    "oklahoma-city": "okc-skyline", "tulsa": "tornado-funnel", "norman": "storm-wall-cloud", "broken-arrow": "suburban-home",
    "edmond": "home-dusk", "lawton": "wichita-mountains", "moore": "tornado-debris-home", "midwest-city": "brick-ranch-home",
    "enid": "grain-elevator", "stillwater": "wheat-field", "muskogee": "water-damage", "shawnee": "fallen-tree-house",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-papers", "rcv-acv-holdback-calculator": "kitchen-interior",
    "roof-pitch-squares-calculator": "roof-inspection", "percentage-deductible-calculator": "hailstones",
    "claim-timeline-planner": "consultation", "appraisal-readiness-check": "clipboard-inspector",
    "roof-payment-schedule-calculator": "roof-shingles",
}
POST_PHOTO = {
    "oklahoma-appraisal-clause-guide": "consultation", "documenting-hail-damage": "roof-torn",
    "roof-payment-schedules-and-cosmetic-exclusions": "roof-shingles", "percentage-wind-hail-deductibles": "storm-wall-cloud",
    "earthquake-endorsement-claims": "living-room", "inside-an-umpire-hearing": "laptop-numbers",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(uid="m"):
    # Brand mark: roofline over a red-clay plains horizon, on a green tile.
    return (f'<svg width="42" height="42" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#2b7a59"/><stop offset="1" stop-color="#0f3626"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="13" fill="url(#{uid})"/>'
            '<path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M16 25v8h16v-8" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round"/>'
            '<rect x="8" y="35.5" width="32" height="4" rx="2" fill="#e0764f"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "OK", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-OK", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across Oklahoma.",
        "areaServed": [{"@type": "State", "name": "Oklahoma"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Tornado damage", "Ice storm claims", "Roof payment schedules", "Xactimate estimating"],
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
    svc = [(s["name"], svc_path(s)) for s in SERVICES]
    return [
        ("Services", svc, ("All appraisal services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Oklahoma cities", LOC_BASE), True),
        ("Free Tools", [(t["name"], tool_path(t)) for t in TOOLS], ("All calculators & planners", TOOL_BASE), False),
        ("Learn", LEARN, None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all-li"><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    brand_inner = "<span><b>Oklahoma Insurance Appraiser</b><small>Independent claim appraisal</small></span>"

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="head"><div class="wrap"><div class="bar">
<a class="brand" href="/" aria-label="{BRAND} home">{mark("mh")}{brand_inner}</a>
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn clay head-cta" href="tel:{TEL}">{ic("phone")} {PHONE}</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/" aria-label="{BRAND} home">{mark("md")}{brand_inner}</a><button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ghost" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm Central · All 77 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:7])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    lr = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in LEARN)
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div class="foot-about"><a class="brand" href="/" aria-label="{BRAND} home">{mark("mf")}<span><b>Oklahoma Insurance Appraiser</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal and estimating for Oklahoma property owners whose insurance claims were accepted but underpaid — from the Panhandle to Kiamichi Country.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm Central</span></div></div>
<div><h2>Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2>Cities</h2><ul>{loc}<li><a href="{LOC_BASE}">All cities</a></li></ul></div>
<div><h2>Free tools</h2><ul>{tl}</ul></div>
<div><h2>Learn</h2><ul>{lr}<li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Site content is general and educational; policy wording controls. Every claim is different and no outcome is guaranteed.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top"><svg class="ring" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="24"/></svg>{ic("up", "up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">Free claim review</a></div>"""


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


def document(path, title, desc, body, schema=None, trail=None, og_type="website", robots="index,follow", photo="hero-supercell", page_type="WebPage", main_entity=None):
    canonical = DOMAIN + path
    trail = trail or [("Home", "/")]
    nodes = [crumbs_schema(trail)] + list(schema or [])
    for n in nodes:
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        else:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
            n["image"] = {"@id": canonical + "#primaryimage"}
    p = PHOTOS[photo]
    if main_entity is None:
        pick = [n["@id"] for n in nodes if n["@type"] in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")]
        if not pick:
            pick = [n["@id"] for n in nodes if n["@type"] == "FAQPage"]
        main_entity = pick[0] if pick else DOMAIN + "/#business"
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": canonical + "#breadcrumb"},
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"]},
        "mainEntity": {"@id": main_entity},
    }
    graph = [org_schema(), site_schema(), webpage] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Oklahoma">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Oklahoma">
<meta name="geo.region" content="US-OK">
<meta name="geo.placename" content="Oklahoma">
<meta name="theme-color" content="#1d5c42">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700&family=Libre+Franklin:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
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
    # Directory pages are served as dir/index.php: the host serves real files without running the
    # front controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
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
        parts.append(e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span aria-hidden=\"true\">›</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts rise" style="animation-delay:.3s">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row rise" style="animation-delay:.22s"><a class="btn clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return (f'<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=" data-parallax=\"0.1\"")}<div class="wrap">{crumbs(trail)}'
            f'<span class="kicker light rise">{e(tag)}</span><h1 class="rise" style="animation-delay:.06s">{e(h1)}</h1>'
            f'<p class="lede rise" style="animation-delay:.14s">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div class=\"a\"><p>{e(a)}</p></div></details>" for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal makes sense for your claim.</p><a class="big" href="tel:{TEL}">{PHONE}</a><a class="btn clay" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span aria-hidden="true">›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Claim accepted, check too small?", p="Send us both estimates. We’ll show you where the numbers part ways."):
    return f"""<section class="cta-band"><div class="wrap"><div class="in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn clay" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line" href="{CONTACT}">Email your estimate</a></div></div></div></section>"""


LOSSES = ["Hail", "Tornado / straight-line wind", "Ice storm / fallen tree", "Burst pipe / water", "Fire / smoke", "Wildfire", "Earthquake (endorsement)", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", sub="Free review, no obligation. We usually reply within one business day.", page="/"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Landlord", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Oklahoma"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I’m a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure yet</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the carrier paid or offered, and what you believe was left out."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn clay" type="submit" style="width:100%">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<div class="lead-card rise" style="animation-delay:.35s"><h2>Get a free claim review</h2><p class="sub">A few details and we’ll call you back within one business day.</p>
<form action="/api/contact.php" method="post" data-lead novalidate>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn clay" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<div class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></div>
</form></div>"""


def tcard(t, h="h3"):
    return (f'<a class="tcard rv" href="{tool_path(t)}"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:760px) 100vw, 320px", alt="")}'
            f'<span class="kind">{e(t["kind"])}</span></span><span class="tb"><{h}>{e(t["name"])}</{h}><p>{e(t["short"])}</p><span class="go">Open the {t["kind"].lower()} →</span></span></a>')


def post_card(p, h="h3"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:760px) 100vw, 380px", alt="")}</a>'
            f'<div class="pb"><span class="meta">{nice} · {p["read"]} read</span><{h}><a href="{post_path(p)}">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p><a class="link" href="{post_path(p)}">Read the guide</a></div></article>')


def city_links():
    return "".join(f'<a class="rv" href="{loc_path(l)}"><span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span>{ic("arrow")}</a>' for l in LOCATIONS)


STORMS = [
    ("May 3, 1999", "Bridge Creek–Moore tornado", "A violent tornado tore through communities southwest and south of Oklahoma City, reshaping how the state thinks about wind-resistant building and safe rooms."),
    ("December 2007", "Statewide ice storm", "Freezing rain coated trees and lines across much of central and northeastern Oklahoma, bringing a wave of fallen-limb and roof claims."),
    ("May 16, 2010", "Metro hailstorm", "Very large hail struck parts of the Oklahoma City area, damaging roofs, siding, windows and vehicles in a single afternoon."),
    ("May 20, 2013", "Moore EF5 tornado", "One of the most destructive tornadoes in state history, followed eleven days later by the El Reno tornado, the widest on record."),
    ("September 3, 2016", "Pawnee earthquake", "A magnitude 5.8 quake, the strongest recorded in Oklahoma, put earthquake endorsements and masonry cracking in the spotlight."),
    ("October 2020", "Central Oklahoma ice storm", "Ice loaded trees that still had their leaves, snapping limbs onto roofs, fences and vehicles across the metro."),
    ("February 2021", "Deep freeze", "A long stretch of sub-zero temperatures led to burst pipes and interior water losses statewide."),
    ("May 6, 2024", "Barnsdall tornado", "A violent tornado hit Barnsdall and nearby areas north of Tulsa, a reminder that Green Country sees major wind events too."),
]


# ---------------------------------------------------------------- home
def home():
    K = BRAND
    groups = ""
    for gname, slugs in SERVICE_GROUPS:
        cards = "".join(f'<a class="svc-card" href="{svc_path(SVC_BY[s])}"><span class="ph">{img(SVC_PHOTO[s], sizes="84px", alt="")}</span><span><b>{e(SVC_BY[s]["name"])}</b><small>{e(SVC_BY[s]["short"])}</small></span></a>' for s in slugs)
        groups += f'<div class="svc-group rv"><h3>{e(gname)}</h3>{cards}</div>'

    steps = [
        ("Free file review", "We read your policy, the carrier’s estimate and your photos, then tell you honestly whether appraisal fits."),
        ("Independent estimate", "Our own inspection and measurements, priced line by line for your part of Oklahoma."),
        ("Written demand", "Appraisal is requested in writing and Oklahoma Insurance Appraiser is named as your appraiser."),
        ("Appraiser-to-appraiser", "We work through the differences item by item with the carrier’s appraiser."),
        ("Signed award", "Anything left goes to a neutral umpire; two signatures set the amount of loss."),
    ]
    stepper = "".join(f'<li data-n="{i + 1}"><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    panels = "".join(
        f'<button type="button" class="panel{" on" if i == 0 else ""}" aria-expanded="{"true" if i == 0 else "false"}">{img(ph, sizes="(max-width:1100px) 100vw, 640px", alt="")}'
        f'<span class="pin"><h3>{e(n)}</h3><span class="more"><span class="chips">{"".join(f"<span>{e(x)}</span>" for x in pl)}</span><p>{e(t)}</p><small>{e(c)}</small></span></span></button>'
        for i, (k, n, s, pl, t, c, ph) in enumerate(REGIONS))
    panels = panels.replace('<span class="chips">', '<span class="chips" role="list">').replace("<span class=\"chips\" role=\"list\"><span>", "<span class=\"chips\" role=\"list\"><span role=\"listitem\">")

    tools = "".join(tcard(t) for t in TOOLS)
    storms = "".join(f'<li class="rv"><time>{e(d)}</time><b>{e(n)}</b><p>{e(t)}</p></li>' for d, n, t in STORMS)
    posts = "".join(post_card(p) for p in POSTS[:3])

    home_faqs = [
        (f"What does an {K} do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, negotiate with the carrier’s appraiser and, if needed, present the remaining items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t give legal advice or negotiate outside appraisal."),
        (f"When is it worth calling an {K}?", "When coverage is accepted, you have the carrier’s estimate, and your contractor’s number is meaningfully higher — as a rough guide, more than about 10% or several thousand dollars apart."),
        ("Does appraisal decide whether my claim is covered?", "Generally no. Appraisal sets the amount of loss. Coverage disputes and denials are a different track, often involving an Oklahoma attorney."),
        ("What does it cost?", "Each side usually pays its own appraiser and splits the umpire. We put our fee in writing before any work begins, and the first conversation is free."),
        ("Do you cover my county?", "Yes. We work in all 77 Oklahoma counties, with frequent work around Oklahoma City, Tulsa, Norman, Lawton, Enid and Stillwater."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-supercell", lazy=False, alt="")}</div>
<div class="wrap">
<div>
<span class="kicker light rise">Independent property claim appraisal · Statewide</span>
<h1 class="rise" style="animation-delay:.08s">{K} for <em>underpaid</em> storm and property claims</h1>
<p class="lede rise" style="animation-delay:.18s">Your insurer accepted the claim, but the check won’t rebuild what the storm took. {K} prepares an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row rise" style="animation-delay:.26s"><a class="btn clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="#services">See how we help {ic("arrow")}</a></div>
<ul class="hero-points rise" style="animation-delay:.34s"><li>{ic("check")}Appointed by you</li><li>{ic("check")}All 77 counties</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="strip" aria-label="Why owners choose us"><div class="wrap"><ul>
<li><span class="ic">{ic("shield")}</span><span><b>Your appraiser</b>Hired by you, not the carrier</span></li>
<li><span class="ic">{ic("ruler")}</span><span><b>Measured, not guessed</b>Our own inspection &amp; scope</span></li>
<li><span class="ic">{ic("scale")}</span><span><b>Built for the umpire</b>Numbers that hold up</span></li>
<li><span class="ic">{ic("map")}</span><span><b>Statewide</b>Panhandle to Kiamichi Country</span></li>
</ul></div></section>

<section class="sec"><div class="wrap split">
<div class="photo-stack rv-wipe">
<figure class="p1">{img("roof-torn", sizes="(max-width:1100px) 92vw, 520px")}</figure>
<figure class="p2">{img("roofer-work", sizes="(max-width:1100px) 46vw, 260px")}</figure>
<span class="tagline">Covered ≠ paid in full</span>
</div>
<div class="rv">
<span class="kicker">What we do</span>
<h2>What an {K} actually does for you</h2>
<p>Most underpaid Oklahoma claims aren’t denied. They’re short: a roof measured a few squares low, Class 4 shingles priced as builder-grade, gutters and screens left off, interior water damage that “wasn’t visible yet.” An {K} closes that gap with evidence instead of argument.</p>
<ul class="ticks">
<li>{ic("check")}<div><b>An estimate built from scratch</b><span>We inspect and measure before we read anyone else’s numbers.</span></div></li>
<li>{ic("check")}<div><b>Priced for where you live</b><span>Labor and material pricing for your area, not a generic national figure.</span></div></li>
<li>{ic("check")}<div><b>Honest about fit</b><span>If your claim needs a lawyer or a simple supplement instead, you’ll hear that on the first call.</span></div></li>
</ul>
<a class="btn" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec white" id="services"><div class="wrap">
<div class="intro rv"><span class="kicker">Services</span><h2>Twelve ways an {K} can help</h2><p>Representation when appraisal has been demanded, a second opinion before it is, and the storm and property losses Oklahoma sees most. Pick the closest match — we’ll sort out the details on the call.</p></div>
<div class="svc-groups" data-stagger>{groups}</div>
<p style="margin-top:28px"><a class="link" href="{SVC_BASE}">Compare every appraisal service</a></p>
</div></section>

<section class="numbers" data-counters aria-label="By the numbers"><div class="wrap"><ul>
<li><b data-count="77">77</b><span>Oklahoma counties covered</span></li>
<li><b data-count="12">12</b><span>Appraisal &amp; estimating services</span></li>
<li><b data-count="7">7</b><span>Free claim calculators</span></li>
<li><b>2 of 3</b><span>Signatures make an award binding</span></li>
</ul></div></section>

<section class="sec"><div class="wrap">
<div class="intro rv"><span class="kicker">The path</span><h2>From stalled claim to signed award</h2><p>The appraisal clause turns an open-ended disagreement into a defined process with a binding result. Here’s how an {K} file moves from the first call to payment.</p></div>
<ol class="stepper"><span class="fill" aria-hidden="true"></span>{stepper}</ol>
<p style="margin-top:34px"><a class="link" href="{PROCESS}">Read the full eight-step appraisal process</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="intro rv"><span class="kicker">Six claim climates</span><h2>One state, six very different kinds of weather</h2><p>Hail in the metro, ice in Green Country, grass fires on the High Plains, wind off the Wichita Mountains. An {K} has to know how each region’s weather shows up on a roof — and in an estimate.</p></div>
<div class="panels rv" data-panels>{panels}</div>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><span class="kicker">Free tools</span><h2>Run the numbers before you call an {K}</h2><p>Seven calculators and planners, free and private. Start with the two-number check on the right: if the gap is large, a conversation makes sense; if it’s small, a documented supplement may close it faster.</p><a class="btn" href="{TOOL_BASE}">Browse all seven tools {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div>
<div class="wrap" style="margin-top:46px"><div class="tool-cards" data-stagger>{tools}</div></div></section>

<section class="sec deep"><div class="wrap">
<div class="intro rv"><span class="kicker light">Storm history</span><h2>Storms that shaped Oklahoma claims</h2><p>Every big event leaves a pattern in how claims get scoped, priced and disputed. An {K} carries those lessons into every file.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec"><div class="wrap">
<div class="intro c rv"><span class="kicker">Choosing help</span><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and fees — and an {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="paths" data-stagger>
<div class="path hl rv"><span class="tag">Appraisal</span><h3>{K}</h3><dl><dt>Main job</dt><dd>Value the amount of loss</dd><dt>Best stage</dt><dd>Coverage accepted, price disputed</dd><dt>Result</dt><dd>Binding award (2 of 3 signatures)</dd></dl></div>
<div class="path rv"><span class="tag">Adjusting</span><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepare and negotiate the claim</dd><dt>Best stage</dt><dd>Early, from first notice</dd><dt>Result</dt><dd>Negotiated settlement</dd></dl></div>
<div class="path rv"><span class="tag">Legal</span><h3>Oklahoma attorney</h3><dl><dt>Main job</dt><dd>Coverage, bad faith, litigation</dd><dt>Best stage</dt><dd>Denials and deadline problems</dd><dt>Result</dt><dd>Settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec white"><div class="wrap">
<div class="intro rv"><span class="kicker">Cities</span><h2>Where {K} works most often</h2><p>We serve every county in the state. These are the communities where an {K} is called most, each with its own local page.</p></div>
<div class="city-grid" data-stagger>{city_links()}</div>
<p style="margin-top:28px"><a class="link" href="{LOC_BASE}">See all Oklahoma cities</a></p>
</div></section>

<section class="sec tint"><div class="wrap split top">
<div class="rv"><span class="kicker">FAQ</span><h2>Questions people ask an {K}</h2><p>Straight answers about what appraisal is, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:22px"><a class="btn" href="{FAQ_P}">All appraisal questions {ic("arrow")}</a><a class="btn ghost" href="{GLOSS}">Claim terms A–Z</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="intro rv"><span class="kicker">Guides</span><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on policy wording, documentation and roof-age rules.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p style="margin-top:28px"><a class="link" href="{POST_BASE}">All storm claim guides</a></p>
</div></section>

<section class="cta-photo">{img("lightning-night", "bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap rv"><span class="kicker light">Spring storm season comes every year</span><h2>Check the numbers before you sign off on them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the rebuild.</p><div class="btn-row"><a class="btn clay" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="#contact">Send your estimate</a></div></div></section>

<section class="sec deep" id="contact"><div class="wrap contact">
<div class="rv"><span class="kicker light">Start with a conversation</span><h2>Talk to an {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer about whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm Central</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Coverage</span><b>All 77 Oklahoma counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Underpaid Claim Appraisal",
                        "Oklahoma Insurance Appraiser offers independent appraisal and estimate review for underpaid hail, tornado, ice storm, water and fire claims.",
                        body, [faq_schema(home_faqs)], photo="hero-supercell", main_entity=DOMAIN + "/#business"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for s in SERVICES:
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        group = next(g for g, sl in SERVICE_GROUPS if s["slug"] in sl)
        sib = [SVC_BY[x] for g, sl in SERVICE_GROUPS if g == group for x in sl if x != s["slug"]]
        rel = (sib + [x for x in SERVICES if x is not s and x not in sib])[:3]
        related = "".join(f'<a href="{svc_path(r)}"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        ph = SVC_PHOTO[s["slug"]]
        cities = ", ".join(f'<a href="{loc_path(l)}">{e(l["city"])}</a>' for l in LOCATIONS[:8])
        body = page_hero(trail, group, s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Available across Oklahoma</h2><p>We take this work statewide, including {cities} and every county in between.</p>
<h2>Common questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Helpful tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]])}</aside></div>
{cta_band()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["keyword"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Oklahoma"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, trail, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    sections = ""
    n = 0
    for gname, slugs in SERVICE_GROUPS:
        cards = ""
        for sl in slugs:
            n += 1
            s = SVC_BY[sl]
            cards += f'<a class="icard rv" href="{svc_path(s)}"><span class="ph">{img(SVC_PHOTO[sl], sizes="(max-width:760px) 100vw, 380px", alt="")}</span><span class="ib"><span class="k">{n:02d} · {e(gname)}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
        sections += f'<h2 class="rv" style="margin-top:10px">{e(gname)}</h2><div class="idx" data-stagger style="margin-bottom:56px">{cards}</div>'
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Oklahoma",
                     "Representation once appraisal is demanded, a second opinion before it is, and focused help with the hail, wind, ice, water, fire and earthquake losses Oklahoma owners face.", "clipboard-inspector") + f"""
<section class="sec"><div class="wrap">{sections}</div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><span class="kicker">Not sure where to start?</span><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days — and plenty of disputes end there.</p><a class="btn" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and HOA claims?", "Yes — retail, office, industrial, churches, apartments and HOA communities as well as single-family homes."), ("Is it only hail?", "No. We handle tornado and straight-line wind, ice storm and tree damage, water, fire, wildfire and endorsed earthquake losses.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Oklahoma | 12 Options",
                             "Twelve insurance appraisal services for Oklahoma property owners, from appraisal representation and estimate review to umpire work.",
                             body, [item_list(items)], trail, photo="clipboard-inspector", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = "".join(f"<li>{e(h)}</li>" for h in l["neighborhoods"])
        storms = "".join(f"<li>{e(s)}</li>" for s in l["storms"])
        body = page_hero(trail, l["region"], l["h1"], e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim profile</b><ul class="chips dark">{chips}</ul></div>
{l["body"]}
<h2>{e(l["city"])} at a glance</h2>
<div class="table-wrap"><table><tbody>
<tr><th>County</th><td>{e(l["county"])}</td></tr>
<tr><th>Housing mix</th><td>{e(l["housing"])}</td></tr>
<tr><th>Neighborhoods &amp; areas</th><td><ul style="margin:0">{hoods}</ul></td></tr>
<tr><th>Storms on record</th><td><ul style="margin:0">{storms}</ul></td></tr>
</tbody></table></div>
<h2>Services for {e(l["city"])} property owners</h2>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} questions</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Oklahoma cities", items, path)}{list_box("Free claim tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, OK", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Oklahoma"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, trail, photo=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cards = "".join(f'<a class="icard rv" href="{loc_path(l)}"><span class="ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:760px) 100vw, 380px", alt="")}</span><span class="ib"><span class="k">{e(l["region"])}</span><h2>{e(l["city"])}</h2><p>{e(l["county"])} · {e(", ".join(l["perils"][:3]))}</p></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="icard rv"><span class="ph">{img(ph, sizes="(max-width:760px) 100vw, 380px", alt="")}</span><span class="ib"><span class="k">{e(", ".join(pl[:2]))}</span><h3>{e(n)}</h3><p>{e(t)}</p><p style="margin-top:10px;font-size:.88rem">{e(c)}</p></span></div>' for k, n, s, pl, t, c, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisers Serving All 77 Oklahoma Counties",
                     "From Guymon to Idabel, we inspect on site and price for local conditions. These pages cover the cities where owners call us most.", "okc-skyline") + f"""
<section class="sec"><div class="wrap"><div class="idx" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="intro rv"><span class="kicker">Regions</span><h2>How claims differ from region to region</h2><p>The same policy language plays out differently on a Panhandle farmhouse, an Edmond two-story and a Muskogee bungalow.</p></div><div class="idx" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your town?", "We cover every Oklahoma county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Oklahoma Cities We Serve | Insurance Appraisers",
                             "Insurance appraisers serving all 77 Oklahoma counties, including Oklahoma City, Tulsa, Norman, Broken Arrow, Lawton and Enid.",
                             body, [item_list([(f"{l['city']}, OK", loc_path(l)) for l in LOCATIONS])], trail, photo="okc-skyline", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for t in TOOLS:
        path = tool_path(t)
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{tool_path(o)}"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [x for x in TOOLS if x is not t][:3])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tight" style="padding-bottom:0"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms; they aren’t a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout" style="padding-top:40px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All tools", items, path)}</aside></div>
{cta_band("Want a professional to check the math?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, trail, photo=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    cards = "".join(tcard(t, "h2") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators and Planners",
                     "Seven tools built from real appraisal work: size the dispute, check the roof math, decode deductibles and roof schedules, and keep deadlines in view. No sign-up, nothing stored.", "laptop-numbers", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-cards" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><span class="kicker">Suggested order</span><h2>Using the tools together</h2><ol><li>Set your dates in the <a href="{TOOL_BASE}claim-timeline-planner/">claim timeline planner</a>.</li><li>Check measurements with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li><li>See what you’d actually receive with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a>, <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV/ACV holdback</a> and <a href="{TOOL_BASE}roof-payment-schedule-calculator/">roof payment schedule</a> calculators.</li><li>Test the dispute in the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-check/">appraisal readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Oklahoma Owners",
                              "Seven free insurance claim calculators: claim gap and fees, RCV/ACV holdback, roof squares, deductibles, roof schedules and deadlines.",
                              body, [item_list(items)], trail, photo="laptop-numbers", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("The appraisal process", path)]
    body = page_hero(trail, "Process guide", "How the Insurance Appraisal Process Works in Oklahoma",
                     "Eight steps from the first disagreement to a signed award — what happens, who does what, and where files most often go sideways.", "consultation",
                     [("Steps", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Oklahoma", "description": "Eight steps from a disputed claim to a signed appraisal award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": DOMAIN + path} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "The Insurance Appraisal Process in Oklahoma | 8 Steps",
                         "A step-by-step guide to the insurance appraisal process in Oklahoma, from the written demand and umpire selection to the signed award.",
                         body, [howto], trail, photo="consultation"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal questions", path)]
    nav = "".join(f'<a class="btn ghost small" href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions, Answered by Topic",
                     "Plain answers about how appraisal works, what it costs, how long it takes and how Oklahoma rules fit in.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><div class="btn-row" style="margin-bottom:28px">{nav}</div>{groups}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Costs, Timing & Oklahoma Rules",
                         "Insurance appraisal FAQ for Oklahoma owners, grouped by topic: the basics, costs and fees, timing and deadlines, and state rules.",
                         body, [faq_schema(allq)], trail, photo="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Insurance claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Insurance Claim Terms Glossary",
                     f"{len(GLOSSARY)} words and phrases you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "calculator-papers", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl><p class="glossary-none none" hidden>No terms match that search.</p></article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim terms glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | 40 Terms Defined",
                         "A searchable insurance claim terms glossary: 40 words from policies, estimates and appraisal awards, from ACV and holdback to umpire.",
                         body, [dts], trail, photo="calculator-papers"), 0.7)

    for p in POSTS:
        path = post_path(p)
        trail = [("Home", "/"), ("Storm claim guides", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{post_path(o)}"><small>Guide</small>{e(o["title"])}</a>' for o in [x for x in POSTS if x is not p][:3])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN)}{list_box("Free tools", [(t["name"], tool_path(t)) for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "keywords": p["keyword"], "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], trail, og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Storm claim guides", path)]
    cards = "".join(post_card(p, "h2") for p in POSTS)
    body = page_hero(trail, "Guides", "Storm Claim Guides for Oklahoma Property Owners",
                     "Practical reading on appraisal clauses, hail documentation, roof schedules, deductibles, earthquake endorsements and umpire hearings.", "storm-wall-cloud", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Storm Claim Guides for Oklahoma Property Owners",
                         "Storm claim guides for Oklahoma owners on appraisal clauses, hail evidence, roof payment schedules, deductibles and umpire hearings.",
                         body, [item_list([(p["title"], post_path(p)) for p in POSTS])], trail, photo="storm-wall-cloud", page_type="CollectionPage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", "About Oklahoma Insurance Appraiser",
                     "An independent appraisal and estimating practice built around one idea: a property claim should be paid on what the damage really costs to repair, documented clearly enough that everyone at the table can see it.", "roof-inspection") + f"""
<div class="wrap layout"><article class="prose">
<figure>{img("consultation", sizes="(max-width:1100px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>Plenty of claim professionals do a little of everything. We chose to do one thing: work out the amount of loss. That focus lets us serve as your appointed appraiser, review an estimate before a dispute hardens, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we approach every file</h2>
<ul>
<li><strong>Scope before numbers.</strong> We inspect, measure and photograph before we read the carrier’s estimate.</li>
<li><strong>Support every line.</strong> A padded estimate loses credibility with an umpire. We price what we can defend.</li>
<li><strong>Explain the differences.</strong> You’ll see, item by item, where our valuation and the carrier’s part ways and why.</li>
<li><strong>Say when it isn’t a fit.</strong> If your claim needs an attorney, a public adjuster or just a supplement, we’ll tell you.</li>
<li><strong>Fees in writing first.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who calls us</h2>
<p>Homeowners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Oklahoma. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t promise results — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Oklahoma’s weather changes from one end of the state to the other: hail and tornadoes in the central corridor, ice storms in Green Country, wildfire on the High Plains, wind and hail around the Wichita Mountains. Working all 77 counties means we see every kind of loss the state produces and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Appraisal services", SVC_BASE), ("Cities we serve", LOC_BASE), ("Free tools", TOOL_BASE), ("The appraisal process", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Oklahoma Insurance Appraiser | Our Approach",
                         "About Oklahoma Insurance Appraiser: an independent appraisal practice focused on the amount of loss for disputed property claims.",
                         body, [], trail, photo="roof-inspection", page_type="AboutPage", main_entity=DOMAIN + "/#business"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact Oklahoma Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and you’ll get an honest read on whether appraisal is likely to help.", "home-dusk", cta=False) + f"""
<section class="sec deep"><div class="wrap contact">
<div class="rv"><span class="kicker light">Direct lines</span><h2>Reach us directly</h2>
<ul class="lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm Central</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>Statewide — all 77 counties</b></div></li></ul>
<h3>Good to have handy</h3><ul><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Send your claim details", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Oklahoma Insurance Appraiser | (844) 537-1427",
                         "Contact Oklahoma Insurance Appraiser for a free review of a disputed property claim. Call (844) 537-1427 or send your claim details.",
                         body, [], trail, photo="home-dusk", page_type="ContactPage", main_entity=DOMAIN + "/#business"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | Oklahoma Insurance Appraiser",
                  "Read the Oklahoma Insurance Appraiser privacy policy to learn what we collect through our forms and tools and how that data is used.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to share — name, phone, email, property location and claim details. Our server also logs standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Calculators and planners</h2><p>Our free tools run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP at any time to opt out.</p>
<h2>Your choices</h2><p>To access, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share."),
        TERMS: ("Terms of Use", "Terms of Use | Oklahoma Insurance Appraiser",
                "These terms of use explain the rules for using the Oklahoma Insurance Appraiser website, its free claim calculators and its content.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. Its content is general information about insurance appraisal and property claims in Oklahoma.</p>
<h2>No client relationship</h2><p>Reading the site, using its tools or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. For legal questions, consult a licensed Oklahoma attorney.</p>
<h2>Tools and estimates</h2><p>Calculators give planning figures based on what you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may link to and print pages for personal use. Photographs are royalty-free public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Oklahoma.</p>""", "The rules that apply when you use this website and its tools."),
        DISCLAIM: ("Disclaimer", "Disclaimer | Oklahoma Insurance Appraiser",
                   "Important limits on the information published by Oklahoma Insurance Appraiser, including no legal advice and no guarantee of results.", f"""
<h2>General information only</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is approaching, contact an Oklahoma attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to laws, agencies and weather events are for context. Check current law and facts with official sources such as the Oklahoma Insurance Department.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h1, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "apartment-complex", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [], trail, photo="apartment-complex"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main pages", [("Home", "/"), ("About us", ABOUT), ("Contact us", CONTACT)]),
        ("Appraisal services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Cities we serve", [("All cities", LOC_BASE)] + [(f"{l['city']}, OK", loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Learn", LEARN[:3] + [("All storm claim guides", POST_BASE)] + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="icard plain rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "commercial-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="idx" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}",
                         "The Oklahoma Insurance Appraiser site map lists every page: services, city pages, free claim tools, guides and legal information.",
                         body, [item_list([x for _, links in groups for x in links])], trail, photo="commercial-building"), 0.3)

    body = f"""<section class="page-hero">{img("storm-wall-cloud", "bg", lazy=False, alt="")}<div class="wrap"><span class="kicker light">Error 404</span><h1>This page got carried off by the wind</h1><p class="lede">The page you’re after may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn clay" href="/">Home</a><a class="btn line" href="{SVC_BASE}">Services</a><a class="btn line" href="{TOOL_BASE}">Free tools</a><a class="btn line" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "Sorry, this page could not be found on Oklahoma Insurance Appraiser. Use the links below to reach our services, tools or contact page.",
                                body, robots="noindex,follow", photo="storm-wall-cloud"), sitemap=False)


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
    # Search Console verification: exact bytes, no wrapper, no trailing newline.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Oklahoma Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$oia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$oia_real  = 'oklahomainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$oia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://oklahomainsuranceappraiser.com - only on the real domain.
if ($oia_host === 'www.' . $oia_real || ($oia_host === $oia_real && $oia_proto === 'http')) {
    header('Location: https://' . $oia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $oia_m)) {
    $oia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $oia_m[1] . $oia_q, true, 301);
    exit;
}
// Keep preview/temporary hosts out of search results.
if ($oia_host !== $oia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Oklahoma Insurance Appraiser - front controller for the static build.
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
    # Guard against stray static pages the host would serve without the PHP guard.
    for dp, _, fs in os.walk(OUT):
        for f in fs:
            if f.endswith(".html") and not (dp == OUT and f in ("home.html", "404.html", GSC_FILE)):
                raise SystemExit(f"stray static page: {os.path.join(dp, f)}")
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
