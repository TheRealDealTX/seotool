#!/usr/bin/env python3
"""Static site generator for tennesseeinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.

Pages are written as dir/index.php (canonical-host guard line + static HTML); the homepage is
home.html, served for "/" by the root index.php front controller. See README for why.
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

BRAND = "Tennessee Insurance Appraiser"
HOST = "tennesseeinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261118a"
FAV = "1"

# Google Tag Manager: leave empty for none. When set (e.g. "GTM-XXXXXXX"), the head snippet and the
# <noscript> iframe after <body> are output on every page.
GTM_ID = "GTM-T6LL4KDG"
# Head snippet exactly as provided by the client. When set it is output verbatim instead of the
# standard GTM loader; the <noscript> iframe after <body> still uses GTM_ID.
GTM_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-T6LL4KDG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build:
# one line, no wrapper, no trailing newline. Never rename, wrap or delete it (Google rechecks it).
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_CONTENT = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/tn-claim-appraisals/"
LOC_BASE = "/tennessee-service-areas/"
TOOL_BASE = "/tennessee-claim-tools/"
POST_BASE = "/claim-dispute-guides/"
P_PROCESS = "/appraisal-process-tennessee/"
P_FAQ = "/tennessee-appraisal-questions/"
P_GLOSS = "/claim-terms-glossary/"
P_ABOUT = "/who-we-are/"
P_CONTACT = "/get-a-claim-review/"
P_PRIVACY = "/privacy/"
P_TERMS = "/terms/"
P_DISC = "/legal-disclaimer/"
P_MAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, TN"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {k: v.get("alt", "") for k, v in PHOTOS.items()}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consult", "home-insurance-appraisal": "house-porch",
    "commercial-hoa-appraisal": "apartments", "hail-roof-appraisal": "roof-shingles",
    "tornado-straight-line-wind-appraisal": "tornado-damage", "water-damage-appraisal": "water-ceiling",
    "fire-smoke-damage-appraisal": "house-fire", "ice-storm-freeze-appraisal": "ice-branches",
    "tree-strike-claim-appraisal": "tree-on-house", "insurance-estimate-audit": "laptop-calc",
    "neutral-umpire-services": "meeting",
}
LOC_PHOTO = {
    # Real city photos where CC0/PD ones exist; otherwise a representative housing or weather photo
    # (alt text describes the photo itself and never claims it shows that city).
    "nashville": "nashville", "memphis": "memphis", "knoxville": "hillside-house", "chattanooga": "chattanooga",
    "clarksville": "suburb-house", "murfreesboro": "two-story-house", "franklin": "colonial-house", "jackson": "lightning",
    "johnson-city": "ridge-sunset", "kingsport": "snowy-ridge", "cookeville": "storm-tree", "sevierville-gatlinburg": "log-cabin",
}
TOOL_PHOTO = {
    "claim-gap-calculator": "calculator", "rcv-acv-holdback-calculator": "paperwork",
    "roof-area-pitch-calculator": "roofer", "percentage-deductible-calculator": "storm-sky",
    "claim-deadline-calendar": "clipboard", "appraisal-readiness-check": "inspection",
    "tree-debris-allowance-calculator": "fallen-tree",
}
POST_PHOTO = {
    "reading-the-appraisal-clause-in-a-tennessee-policy": "office",
    "after-a-tennessee-tornado-first-30-days": "tornado-debris",
    "burst-pipes-after-a-hard-freeze": "icicles",
    "matching-siding-and-shingles-after-a-storm": "house-siding",
    "estimate-red-flags-tennessee-roof-claims": "roof-closeup",
    "appraisal-or-attorney-choosing-the-right-help": "consult",
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
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def _star(cx, cy, r):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return "M" + " L".join(pts) + "Z"


STARS = _star(24, 25.2, 4.6) + _star(17.6, 35.4, 4.6) + _star(30.4, 35.4, 4.6)
ROOF = "M8.5 24.5 24 11l15.5 13.5"


def mark():
    """Brand mark: navy tile, red roofline and three white stars."""
    return (f'<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="11" fill="#002D65"/>'
            f'<path d="{ROOF}" fill="none" stroke="#CC0000" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{STARS}" fill="#fff"/></svg>')


def brand_link(where):
    return f'<a class="brand" href="/" aria-label="{BRAND} home" data-brand="{where}">{mark()}<span class="brand-t"><b>Tennessee</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
LOGO_ID = DOMAIN + "/#logo"
BIZ_ID = DOMAIN + "/#business"
SITE_ID = DOMAIN + "/#website"


def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": BIZ_ID,
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": LOGO_ID, "url": DOMAIN + "/favicon-512.png", "contentUrl": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": LOGO_ID},
        "address": {"@type": "PostalAddress", "addressRegion": "TN", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-TN", "availableLanguage": "en"}],
        "areaServed": [{"@type": "State", "name": "Tennessee"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services in Tennessee", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 95 Tennessee counties.",
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Hail and roof damage", "Tornado damage", "Ice storm and freeze claims"],
        "priceRange": "$$",
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": SITE_ID, "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": BIZ_ID}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}


def item_list(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Service Areas", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Tennessee service areas", LOC_BASE)),
        ("Free Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All claim tools", TOOL_BASE)),
        ("Resources", [("Appraisal process", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Claim dispute guides", POST_BASE)], None),
    ]


def gtm_head():
    if GTM_SNIPPET:
        return "<!-- Google Tag Manager -->\n" + GTM_SNIPPET + "\n<!-- End Google Tag Manager -->\n"
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def header():
    menu = ""
    for name, links, allk in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-sub"><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="sub{wide}">{li}</ul></li>'
    menu += f'<li><a href="{P_ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="top-link" href="{P_ABOUT}">About us</a></li><li><a class="top-link" href="{P_CONTACT}">Free claim review</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="flagline" aria-hidden="true"></div>
<header class="head"><div class="shell head-in">
{brand_link("header")}
<nav class="primary" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<div class="head-cta"><a class="head-tel" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn red small" href="{P_CONTACT}">Free claim review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link("drawer")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a class="top-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><small>Mon–Fri 8am–6pm Central · All 95 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot">
<div class="foot-call"><div class="shell"><h2>Claim paid short? Let’s go through the numbers.</h2><div class="btn-row"><a class="btn red" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn outline-light" href="{P_CONTACT}">Send your estimate</a></div></div></div>
<div class="shell foot-grid">
<div class="foot-about">{brand_link("footer")}
<p>Independent appraisal, estimate review and umpire services for disputed property claims across East, Middle and West Tennessee.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Mon–Fri 8am–6pm Central</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Service areas</h3><ul class="two">{loc}</ul></div>
<div><h3>Free tools</h3><ul>{tl}</ul></div>
<div><h3>Resources</h3><ul><li><a href="{P_PROCESS}">Appraisal process</a></li><li><a href="{P_FAQ}">FAQ</a></li><li><a href="{P_GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{P_ABOUT}">About us</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="shell foot-base"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{P_PRIVACY}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Site map</a></li></ul></div>
<p class="shell foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content is general information; policy language controls. Example figures are illustrative, and results are never guaranteed.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">Free review</a></div>"""


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-home", page_type="WebPage", trail=None, main_id=None):
    canonical = DOMAIN + "/404" if path == "/404.html" else DOMAIN + path
    page_id = canonical + "#webpage"
    extra_nodes = []
    trail = trail or [("Home", "/")]
    crumb = crumbs_schema(trail)
    crumb["@id"] = canonical + "#breadcrumb"
    extra_nodes.append(crumb)
    for n in (schema or []):
        t = n.get("@type")
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": page_id}
        if t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": page_id}
                n["author"] = {"@id": BIZ_ID}
                n["publisher"] = {"@id": BIZ_ID}
                n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    pimg = PHOTOS[photo]
    if main_id is None:
        mains = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
        main_id = mains[0] if mains else BIZ_ID
    webpage = {
        "@type": page_type, "@id": page_id, "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": SITE_ID}, "about": {"@id": BIZ_ID},
        "publisher": {"@id": BIZ_ID}, "dateModified": TODAY,
        "breadcrumb": {"@id": crumb["@id"]},
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"]},
        "mainEntity": {"@id": main_id},
    }
    graph = [org_schema(), site_schema(), webpage] + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
    canon_tag = "" if robots.startswith("noindex") else f'<link rel="canonical" href="{canonical}">\n'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
{canon_tag}<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Tennessee">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Tennessee">
<meta name="geo.region" content="US-TN">
<meta name="geo.placename" content="Tennessee">
<meta name="theme-color" content="#002D65">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Arvo:wght@400;700&family=Cabin:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
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
    rel = "home.html" if path == "/" else path.strip("/") + "/index.php"
    if path.endswith(".html"):
        rel = path.strip("/")
    if "<?" in content:
        raise SystemExit(f"PHP tag in page HTML: {path}")
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
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">›</span>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn outline-light" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="page-hero"><div class="ph-media">{img(photo, "zoom", lazy=False, alt="")}</div><div class="shell ph-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><div class=\"a\"><p>{a}</p></div></details>" for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk to an appraiser</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="big-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn red" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span></a>' for k, n, p in items) + "</div>"


def cta_band(h="Is the carrier’s number too low?", p="Send us the estimate and your photos. We’ll review it and tell you what we see."):
    return f"""<section class="cta-band"><div class="shell cta-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn red" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn outline-light" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


LOSSES = ["Hail / roof", "Tornado / wind", "Ice storm / freeze", "Water / burst pipe", "Fire / smoke", "Tree strike", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=2):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Landlord", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Tennessee"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See our <a href="{P_PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn red wide" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-form" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="form-t">Get a free claim review</h2><p class="sub">Three quick fields. An appraiser calls you back, usually within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{P_PRIVACY}">privacy policy</a>.</span></label>
<button class="btn red wide" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="secure">{ic("shield")}<span>No obligation. Nothing is shared.</span></p>
</form>"""


def contact_lines():
    return f"""<ul class="contact-lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm Central</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 95 Tennessee counties</b></div></li></ul>"""


# ---------------------------------------------------------------- home
DIVISIONS = [
    ("west", "West Tennessee", "Memphis · Jackson · Dyersburg", ["Derechos", "Ice storms", "Tornadoes", "Earthquake endorsements"],
     "Flat, open land between the Mississippi River and the Tennessee River lets storm lines hold their strength. Memphis remembers the 2003 derecho and the ice storms of 2022 and 2023; Jackson has been hit by major tornadoes in 2003 and 2008. Shelby County also sits near the New Madrid Seismic Zone.",
     ["memphis", "jackson"], "memphis"),
    ("middle", "Middle Tennessee", "Nashville · Clarksville · Murfreesboro", ["Night tornadoes", "Spring hail", "Straight-line wind", "Subdivision claims"],
     "The fastest-growing part of the state is also one of its most tornado-prone. Nashville, Cookeville, Clarksville and Murfreesboro have all taken direct hits since 2009, and spring hail regularly crosses Davidson, Williamson and Rutherford counties.",
     ["nashville", "clarksville", "murfreesboro", "franklin", "cookeville"], "nashville"),
    ("east", "East Tennessee", "Knoxville · Chattanooga · Tri-Cities", ["Mountain wind", "Ice & snow", "Wildfire", "Hillside access costs"],
     "Ridges, valleys and the Smokies shape every claim. The 2011 outbreak hammered the Chattanooga area, the 2016 fires swept into Gatlinburg, and Helene’s remnants flooded the northeast in 2024. Steep lots add access and staging costs that estimates often miss.",
     ["knoxville", "chattanooga", "johnson-city", "kingsport", "sevierville-gatlinburg"], "smokies"),
]

STORMS = [
    ("1974", "April 3–4", "Super Outbreak", "One of the largest tornado outbreaks on record crossed Middle and East Tennessee."),
    ("1998", "April 16", "Downtown Nashville tornado", "A tornado tore through downtown and East Nashville in the afternoon."),
    ("2003", "July 22", "Memphis derecho", "Hurricane-force straight-line winds downed trees across Shelby County."),
    ("2008", "February 5", "Super Tuesday outbreak", "Night tornadoes struck Jackson, Union University and towns statewide."),
    ("2011", "April 27", "Southeast outbreak", "Violent tornadoes hit the Chattanooga area, including Apison."),
    ("2016", "November 28", "Sevier County fires", "Wind-driven wildfire swept into Gatlinburg and the hills around it."),
    ("2020", "March 3", "Nashville & Cookeville tornadoes", "An EF3 crossed Nashville; an EF4 devastated western Putnam County."),
    ("2023", "December 9", "Clarksville & Madison tornadoes", "Cool-season tornadoes damaged hundreds of Middle Tennessee homes."),
    ("2024", "January", "Statewide deep freeze", "Single-digit cold split pipes in homes, apartments and churches."),
    ("2024", "September", "Helene’s remnants", "Catastrophic flooding in the northeast; wind claims followed too."),
]


def home():
    K = BRAND
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 1 else "false"}" tabindex="{0 if i == 1 else -1}"><b>{e(n)}</b><small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(DIVISIONS))
    panels = ""
    for i, (k, n, _s, perils, t, cities, ph) in enumerate(DIVISIONS):
        links = "".join(f'<a href="{loc_path(LOC_BY[c])}">{e(LOC_BY[c]["city"])}</a>' for c in cities)
        panels += (f'<div class="region-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" data-initial="{1 if i == 1 else 0}"><div class="rp-media">{img(ph, sizes="(max-width:900px) 100vw, 560px", alt="")}</div>'
                   f'<div class="rp-body"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in perils)}</ul><p>{e(t)}</p><p class="rp-links">{links}</p></div></div>')

    svc_cards = "".join(
        f'<a class="svc-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="svc-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 380px", alt="")}</span>'
        f'<span class="svc-n">{i + 1:02d}</span><span class="svc-b"><h3>{e(s["name"])}</h3><span>{e(s["short"])}</span></span></a>'
        for i, s in enumerate(SERVICES))
    tool_cards = "".join(
        f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tc-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 300px", alt="")}<i>{t["icon"]}</i></span><span class="tc-b"><small>{t["kind"]}</small><h3>{e(t["name"])}</h3><span>{e(t["short"])}</span></span></a>'
        for t in TOOLS)
    city_cards = "".join(
        f'<a class="city-card rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, 280px", alt="")}<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>'
        for l in LOCATIONS)
    posts = "".join(
        f'<article class="guide-card rv"><a class="gc-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 380px", alt="")}</a><div class="gc-b"><small>{p["read"]} read</small><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS[:3])
    storms = "".join(f'<li class="rv"><span class="yr">{y}</span><small>{e(d)}</small><b>{e(n)}</b><span>{e(t)}</span></li>' for y, d, n, t in STORMS)
    steps = [
        ("Free claim review", f"Send the policy, the carrier’s estimate and your photos. A {K} reads them and tells you plainly whether appraisal fits."),
        ("Our own inspection", "We measure, photograph and scope the damage ourselves, then price it for your county."),
        ("Written demand", "Appraisal is demanded in writing and you name us as your appraiser within the policy’s window."),
        ("Panel work", "We work line by line with the carrier’s appraiser. Most disputes narrow sharply here."),
        ("Umpire and award", "Items still open go to a neutral umpire. Two of three signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="pstep"><span class="num">{i + 1}</span><div class="body rv"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))

    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent estimate, work with the carrier’s appraiser and present open items to a neutral umpire."),
        ("Is the appraisal award binding?", "Yes, on the amount of loss, once any two of the three panel members sign it. That’s why the file should be complete before anyone demands appraisal."),
        (f"When should I call a {K}?", "When coverage is accepted, you have the insurer’s itemized estimate, and the gap between it and a qualified repair estimate is meaningful — generally more than about 10% or several thousand dollars."),
        ("Is this the same as hiring a public adjuster?", "No. A public adjuster manages and negotiates the whole claim. An appraiser works inside the appraisal clause on one question: the amount of loss. We don’t give legal advice or negotiate outside appraisal."),
        ("Does Tennessee have a FAIR plan?", "No. Tennessee doesn’t operate a FAIR plan or wind pool. Owners who can’t find standard coverage often use surplus-lines insurers, whose policies may contain different appraisal terms."),
        ("What does it cost?", "You pay your own appraiser and usually half of the umpire. Our fee is set in writing before work begins, and the first conversation is free."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("storm-sky", "zoom", lazy=False, alt="")}</div>
<div class="shell hero-in">
<div class="hero-copy">
<p class="kicker light">Independent claim appraisal · All 95 counties</p>
<h1>{K} <span>for claims that came up short</span></h1>
<p class="lede">Your insurer accepted the claim, but the check won’t cover the repair. {K} builds an independent, line-by-line valuation of your loss and takes it through the appraisal process written into your policy — from Memphis to the Tri-Cities.</p>
<div class="btn-row"><a class="btn red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn outline-light" href="#how">How appraisal works</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your named appraiser</li><li>{ic("check")}County-level pricing</li><li>{ic("check")}Homes, HOAs &amp; businesses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="stats" aria-label="At a glance"><div class="shell stats-in">
<div class="stat"><b data-count="95">95</b><span>Tennessee counties served</span></div>
<div class="stat"><b data-count="3">3</b><span>Grand Divisions, one team</span></div>
<div class="stat"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="stat"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
</div></section>

<section class="sec"><div class="shell intro">
<div class="intro-media rv-l"><figure>{img("inspection", sizes="(max-width:900px) 100vw, 520px")}</figure><p class="intro-badge"><b>2 of 3</b><span>signatures make an appraisal award binding</span></p></div>
<div class="intro-copy rv-r">
<p class="kicker">The short version</p>
<h2>What a {K} does — and doesn’t do</h2>
<p>Most underpaid claims aren’t denials. They’re estimates that left things out: a roof slope, a matching floor, a code item, a crane for the oak that came through the attic. A {K} exists for the gap between “covered” and “paid in full.”</p>
<ol class="numbered">
<li><b>We value the loss from scratch.</b> Our own inspection and measurements, never a marked-up copy of the carrier’s estimate.</li>
<li><b>We price what we can defend.</b> Numbers built to hold up in front of an umpire move awards; inflated ones don’t.</li>
<li><b>We tell you when appraisal is wrong.</b> Denials, bad-faith questions and close deadlines belong with a Tennessee attorney, and we’ll say so on the first call.</li>
</ol>
<a class="btn navy" href="{P_ABOUT}">Who we are {ic("arrow")}</a>
</div>
</div></section>

<section class="sec mist" id="services"><div class="shell">
<div class="sec-head rv"><p class="kicker">Services</p><h2>Eleven ways a {K} can help</h2><p>Every service is built around one deliverable: an accurate, defensible valuation of your loss. Start with an estimate review, or bring us in after appraisal has been demanded.</p></div>
<div class="svc-grid" data-stagger>{svc_cards}</div>
<p class="center"><a class="btn navy" href="{SVC_BASE}">All appraisal services {ic("arrow")}</a></p>
</div></section>

<section class="sec navy"><div class="shell">
<div class="sec-head rv"><p class="kicker light">Three stars, three climates</p><h2>Claims look different in each Grand Division</h2><p>The three stars on the state flag stand for East, Middle and West Tennessee. A {K} has to know how each one’s weather shows up on a roof and in an estimate.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="Tennessee Grand Divisions">{tabs}</div>{panels}</div>
</div></section>

<section class="sec"><div class="shell split">
<div class="rv-l"><p class="kicker">Quick check</p><h2>Is your gap big enough for appraisal?</h2><p>Enter the two numbers you already have. If the difference is large, it’s worth a conversation with a {K}. If it’s small, a documented supplement may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}claim-gap-calculator/">claim gap &amp; fee estimator</a> subtracts appraiser and umpire fees to show a realistic net. All figures are illustrative.</p><a class="btn navy" href="{TOOL_BASE}">See all {len(TOOLS)} free tools {ic("arrow")}</a></div>
<div class="rv-r">{GAP_MINI}</div>
</div></section>

<section class="sec mist" id="how"><div class="shell split top">
<div class="rv-l sticky-col"><p class="kicker">The process</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here is how a {K} file usually moves.</p><a class="link" href="{P_PROCESS}">Read the full eight-step process guide</a></div>
<ol class="process"><span class="fill" aria-hidden="true"></span>{proc}</ol>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker">Storm memory</p><h2>Tennessee events that shaped today’s claims</h2><p>Every {K} file sits on top of this history. Outbreaks, derechos, fires and freezes taught owners, adjusters and courts how losses here are valued.</p></div>
<ol class="storm-line" tabindex="0" aria-label="Tennessee storm timeline">{storms}</ol>
</div></section>

<section class="sec mist"><div class="shell">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Claim calculators from a {K}</h2><p>Run the numbers before you pick up the phone. Every tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="tool-grid" data-stagger>{tool_cards}</div>
</div></section>

<section class="sec"><div class="shell">
<div class="sec-head rv"><p class="kicker">Service areas</p><h2>Where our {K} team works most</h2><p>We cover all 95 counties. These twelve cities and their surrounding communities are where we handle claims most often.</p></div>
<div class="city-grid" data-stagger>{city_cards}</div>
<p class="center"><a class="link" href="{LOC_BASE}">See every Tennessee service area</a></p>
</div></section>

<section class="sec mist"><div class="shell">
<div class="sec-head rv"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. A {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="who-grid" data-stagger>
<div class="who rv hl"><h3>Appraiser</h3><p class="who-q">Coverage accepted, number disputed</p><ul><li>Values the amount of loss</li><li>Works inside the appraisal clause</li><li>Ends in a binding award</li></ul></div>
<div class="who rv"><h3>Public adjuster</h3><p class="who-q">Early in a large or complex claim</p><ul><li>Manages the whole claim</li><li>Documents and negotiates</li><li>Ends in a negotiated settlement</li></ul></div>
<div class="who rv"><h3>Attorney</h3><p class="who-q">Denials, bad faith, close deadlines</p><ul><li>Handles legal disputes</li><li>Can file suit</li><li>Ends in settlement or judgment</li></ul></div>
</div>
</div></section>

<section class="sec"><div class="shell split top">
<div class="rv-l"><p class="kicker">FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn navy" href="{P_FAQ}">All FAQs {ic("arrow")}</a><a class="btn ghost" href="{P_GLOSS}">Glossary</a></div></div>
<div class="rv-r">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec mist"><div class="shell">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides on policy wording, documentation and strategy from the {K} team.</p></div>
<div class="guide-grid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{POST_BASE}">All claim dispute guides</a></p>
</div></section>

<section class="cta-photo"><div class="cp-media">{img("hero-home", alt="", extra=' data-parallax="0.16"')}</div><div class="shell cp-in rv"><p class="kicker light">Before you sign off</p><h2>Check the numbers before you accept them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn outline-light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec navy" id="contact"><div class="shell contact">
<div class="rv-l"><p class="kicker light">Start here</p><h2>Talk with a {K} about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll give you a straight answer on whether appraisal is worth pursuing. No pressure and no obligation.</p>{contact_lines()}</div>
<div class="rv-r">{lead_form(page="/", hlevel=3)}</div>
</div></section>
"""
    write("/", document("/", f"{K} | Property Claim Appraisal",
                        f"{K}: independent appraisal, estimate review and umpire services for underpaid storm, water, fire and freeze claims.",
                        body, [faq_schema(home_faqs)], photo="storm-sky", main_id=BIZ_ID), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="shell layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("All services", items, path)}{list_box("Popular service areas", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]])}</div></aside></div>
{cta_band()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": BIZ_ID}, "areaServed": {"@type": "State", "name": "Tennessee"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph, trail=trail, main_id=DOMAIN + path + "#service"), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="index-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="ic-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, 360px", alt="")}</span><span class="ic-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><span>{e(s["short"])}</span></span></a>' for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Appraisal Services Across Tennessee",
                     f"From a single estimate review to full panel representation and neutral umpire work, each {BRAND} service is built around an accurate, defensible valuation of your loss.", "roofer") + f"""
<section class="sec"><div class="shell"><div class="index-grid" data-stagger>{cards}</div></div></section>
<section class="sec mist"><div class="shell split top"><div class="rv-l"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close at that stage.</p><a class="btn navy" href="{SVC_BASE}insurance-estimate-audit/">About estimate reviews {ic("arrow")}</a></div><div class="rv-r">{faq_block([("Can I hire you for one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, condos, rentals, apartments, retail, office, industrial, churches and HOA properties."), ("Which perils do you handle?", "Hail, wind, tornado, ice, freeze, water, fire, smoke, tree strikes and other covered perils.")])}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services Across Tennessee",
                             "Insurance appraisal services across Tennessee: appraisal clause work, roof, tornado, water, fire, freeze and tree claims, reviews and umpires.",
                             body, [item_list(items)], photo="roofer", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- locations
LOC_SEO = {
    "nashville": ("Nashville Insurance Appraiser | Davidson County, TN", "Nashville insurance appraiser for Davidson County: independent valuation of tornado, hail, water and fire claims when the estimate is short."),
    "memphis": ("Memphis Insurance Appraiser | Shelby County Claims", "Memphis insurance appraiser for Shelby County homes and businesses: derecho, ice storm, tornado and burst-pipe claims valued independently."),
    "knoxville": ("Knoxville Insurance Appraiser | Knox County Claims", "Knoxville insurance appraiser serving Knox County: hail, wind, ice and water claim appraisal for Victorian, hillside and suburban homes."),
    "chattanooga": ("Chattanooga Insurance Appraiser | Hamilton County", "Chattanooga insurance appraiser for Hamilton County: tornado, hail and tree claims on mountain, lakeside and city homes valued in full."),
    "clarksville": ("Clarksville Insurance Appraiser | Montgomery Co., TN", "Clarksville insurance appraiser for Montgomery County: tornado, hail and siding-matching disputes on newer homes and rental properties."),
    "murfreesboro": ("Murfreesboro Insurance Appraiser | Rutherford County", "Murfreesboro insurance appraiser for Rutherford County: hail, wind and tornado claims on subdivision homes, HOAs and commercial buildings."),
    "franklin": ("Franklin TN Insurance Appraiser | Williamson County", "Franklin insurance appraiser for Williamson County: storm and water claims on high-value homes with slate, cedar, copper and custom finishes."),
    "jackson": ("Jackson TN Insurance Appraiser | Madison County", "Jackson insurance appraiser for Madison County: tornado, ice storm, wind and hail claims on homes, churches and commercial properties."),
    "johnson-city": ("Johnson City Insurance Appraiser | Tri-Cities TN", "Johnson City insurance appraiser for Washington County and the Tri-Cities: wind, ice, hail and tree claims, including Helene wind losses."),
    "kingsport": ("Kingsport Insurance Appraiser | Sullivan County, TN", "Kingsport insurance appraiser for Sullivan County: ice storm, hail, wind and burst-pipe claims on historic, hillside and commercial property."),
    "cookeville": ("Cookeville Insurance Appraiser | Putnam County, TN", "Cookeville insurance appraiser for Putnam County and the Upper Cumberland: tornado total losses, hail, wind and outbuilding claims valued."),
    "sevierville-gatlinburg": ("Gatlinburg & Sevierville Insurance Appraiser", "Insurance appraiser for Sevierville, Gatlinburg and Pigeon Forge: wildfire smoke, wind, ice and cabin rental claims across Sevier County."),
}


def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Service areas", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, f"{l['division']} · {l['county']}", f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Grand Division", l["division"]), ("Housing mix", l["housing"].split(",")[0])]) + f"""
<div class="shell layout"><article class="prose">
<div class="local-card"><div><b>Local claim risks</b><ul class="chips">{chips}</ul></div><div><b>Housing mix</b><p>{e(l["housing"])}.</p></div></div>
{l["body"]}
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])} and nearby communities, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}
</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("Tennessee service areas", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</div></aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        title, desc = LOC_SEO[l["slug"]]
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": BIZ_ID}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Tennessee"}}, "url": DOMAIN + path}]
        write(path, document(path, title, desc, body, schema, photo=ph, trail=trail, main_id=DOMAIN + path + "#service"), 0.8)

    trail = [("Home", "/"), ("Service areas", LOC_BASE)]
    cities = "".join(f'<a class="city-card rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:640px) 50vw, 280px", alt="")}<span><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    divs = "".join(f'<div class="index-card plain rv"><span class="ic-ph">{img(ph, sizes="(max-width:640px) 100vw, 360px", alt="")}</span><span class="ic-b"><small>{e(s)}</small><h2>{e(n)}</h2><span>{e(t)}</span></span></div>' for k, n, s, _p, t, _c, ph in DIVISIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 95 Tennessee Counties",
                     f"{BRAND} works statewide, from the Mississippi River bluffs to the Blue Ridge. These local pages cover the cities where we handle claims most often.", "nashville") + f"""
<section class="sec"><div class="shell"><div class="city-grid" data-stagger>{cities}</div></div></section>
<section class="sec mist"><div class="shell"><div class="sec-head rv"><p class="kicker">Grand Divisions</p><h2>How claims differ across the state</h2><p>The same policy language plays out very differently in a Midtown Memphis four-square, a Murfreesboro subdivision and a Smokies rental cabin.</p></div><div class="index-grid three" data-stagger>{divs}</div></div></section>
{cta_band("Don’t see your town?", "We cover every Tennessee county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Tennessee Service Areas | Appraisal by City",
                             "Insurance appraisal service areas in all 95 Tennessee counties, with local pages for Nashville, Memphis, Knoxville, Chattanooga and more.",
                             body, [item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="nashville", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tool-sec"><div class="shell"><noscript><p class="note">This calculator needs JavaScript. Everything runs in your browser and nothing is stored.</p></noscript>{t["markup"]}
<p class="hint center">For planning only. Results depend on the figures you enter and your policy’s terms; they aren’t a quote, an appraisal or legal advice. Default figures are illustrative.</p></div></section>
<div class="shell layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("All claim tools", items, path)}</div></aside></div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": BIZ_ID}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph, trail=trail, main_id=DOMAIN + path + "#webapplication"), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    cards = "".join(f'<a class="tool-card rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tc-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 300px", alt="")}<i>{t["icon"]}</i></span><span class="tc-b"><small>{t["kind"]}</small><h2>{e(t["name"])}</h2><span>{e(t["short"])}</span></span></a>' for t in TOOLS)
    T = TOOL_BASE
    body = page_hero(trail, "Free & private", "Free Tennessee Insurance Claim Tools",
                     f"{len(TOOLS)} calculators and planners built from real appraisal work. Check the carrier’s math, plan deadlines and decide next steps. No sign-up, nothing stored.", "laptop-calc", cta=False) + f"""
<section class="sec"><div class="shell"><div class="tool-grid" data-stagger>{cards}</div></div></section>
<section class="sec mist"><div class="shell split top"><div class="rv-l"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="numbered"><li>Start with the <a href="{T}claim-deadline-calendar/">deadline calendar</a> so nothing lapses.</li><li>Check roof math with the <a href="{T}roof-area-pitch-calculator/">roof area &amp; pitch calculator</a>.</li><li>See what you’ll actually receive with the <a href="{T}percentage-deductible-calculator/">deductible</a> and <a href="{T}rcv-acv-holdback-calculator/">holdback</a> calculators.</li><li>After a tree comes down, run the <a href="{T}tree-debris-allowance-calculator/">tree &amp; debris allowance calculator</a>.</li><li>Test the dispute with the <a href="{T}claim-gap-calculator/">claim gap estimator</a>, then take the <a href="{T}appraisal-readiness-check/">readiness check</a>.</li></ol></div><div class="rv-r">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Tennessee Insurance Claim Tools",
                              "Free Tennessee insurance claim tools: claim gap, RCV/ACV holdback, roof pitch, percentage deductible, deadline and tree allowance calculators.",
                              body, [item_list(items)], photo="laptop-calc", page_type="CollectionPage", trail=trail), 0.9)


# ---------------------------------------------------------------- resources
LEARN = [("Appraisal process", P_PROCESS), ("Appraisal FAQ", P_FAQ), ("Claim terms glossary", P_GLOSS), ("Claim dispute guides", POST_BASE)]


def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "The Tennessee Insurance Appraisal Process, Step by Step",
                     "Eight stages, from the first disagreement to a signed award: what happens, who does what, and where claims most often stall.", "clipboard",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="shell layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("Resources", LEARN, path)}</div></aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Tennessee", "description": "Eight steps from an amount-of-loss disagreement to a signed appraisal award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": d} for i, (n, d) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Tennessee Insurance Appraisal Process, Step by Step",
                         "The Tennessee insurance appraisal process in eight steps: written demand, choosing appraisers and an umpire, negotiation and the binding award.",
                         body, [howto], photo="clipboard", trail=trail), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    nav = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Tennessee Insurance Appraisal FAQ",
                     "Plain answers to the questions we hear most about appraisal, Tennessee rules, cost and timing, and how we work.", "kitchen") + f"""
<div class="shell layout"><article class="prose"><nav class="topic-nav" aria-label="FAQ topics">{nav}</nav>{groups}</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("Resources", LEARN, path)}</div></aside></div>{cta_band("Didn’t see your question?", "Call or email and we’ll talk it through.")}"""
    write(path, document(path, "Tennessee Insurance Appraisal FAQ | Costs & Rules",
                         "Tennessee insurance appraisal FAQ grouped by topic: how appraisal works, state rules, regulator, bad-faith law, costs, timing and our role.",
                         body, [faq_schema(allq)], photo="kitchen", trail=trail), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Claim terms glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Property Claim Terms Glossary",
                     f"{len(GLOSSARY)} terms you’ll see in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "paperwork", cta=False) + f"""
<div class="shell layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"></div><p class="az">{az}</p><dl class="glossary">{dl}</dl><p class="gloss-none" hidden>No terms match that search.</p></article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("Resources", LEARN, path)}</div></aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Property Claim Terms Glossary | 40+ Definitions",
                         "Searchable glossary of property insurance claim terms, from ACV and RCV to umpire, matching, holdback and percentage deductibles, defined.",
                         body, [dts], photo="paperwork", trail=trail), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="shell layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in others])}</article>
<aside class="aside"><div class="aside-in">{call_box()}{list_box("Resources", LEARN)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</div></aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], og_type="article", photo=ph, trail=trail), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(f'<article class="guide-card rv"><a class="gc-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 380px", alt="")}</a><div class="gc-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides", "Claim Dispute Guides for Tennessee Property Owners",
                     "Practical reading on policy wording, documentation and claim strategy, written by people who sit on appraisal panels.", "house-siding", cta=False) + f"""
<section class="sec"><div class="shell"><div class="guide-grid" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Claim Dispute Guides for Tennessee Property Owners",
                         "Claim dispute guides for Tennessee property owners: appraisal clauses, tornado and freeze claims, roof estimates, matching and choosing help.",
                         body, [item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="house-siding", page_type="CollectionPage", trail=trail), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", f"Who We Are at {BRAND}",
                     "Estimators and appraisers who believe a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "meeting") + f"""
<div class="shell layout"><article class="prose">
<figure class="lead-img">{img("consult", sizes="(max-width:1000px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Most claim professionals do a bit of everything. We chose one question — the amount of loss — and built our inspections, estimates and reporting around answering it well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible beats impressive.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand each difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys in all 95 Tennessee counties. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t promise outcomes; no honest appraiser can.</p>
<h2>One state, three Grand Divisions</h2>
<p>Ice storms in Memphis, night tornadoes in Middle Tennessee and mountain wind in the Smokies all produce different damage — and different estimating mistakes. Working statewide means we see every kind of loss Tennessee produces and price each one for the county it’s in.</p>
</article><aside class="aside"><div class="aside-in">{call_box()}{list_box("Explore", [("Appraisal services", SVC_BASE), ("Service areas", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", P_PROCESS)])}</div></aside></div>{cta_band()}"""
    write(path, document(path, f"About {BRAND} | Who We Are",
                         f"Who we are: {BRAND} is an independent appraisal practice focused on the amount of loss in property claim disputes.",
                         body, [], photo="meeting", page_type="AboutPage", trail=trail), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Free claim review", path)]
    body = page_hero(trail, "Contact", "Get a Free Claim Review",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult", cta=False) + f"""
<section class="sec navy"><div class="shell contact">
<div class="rv-l"><p class="kicker light">Direct lines</p><h2>Reach {BRAND}</h2>{contact_lines()}
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv-r">{lead_form("Tell us about your claim", page=path, hlevel=3)}</div></div></section>"""
    write(path, document(path, f"Free Claim Review | {BRAND}",
                         f"Get a free claim review from {BRAND}. Call (844) 537-1427 or send your estimate and photos through our secure form.",
                         body, [], photo="consult", page_type="ContactPage", trail=trail), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIVACY: ("Privacy Policy", f"Privacy Policy | {BRAND}", f"Privacy policy for {BRAND}: what we collect through forms and calls, how we use it, and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share, such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type and pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The figures you enter aren’t sent to us or stored.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, we’ll update this page.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To access, correct or delete information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        P_TERMS: ("Terms of Use", f"Terms of Use | {BRAND}", f"Terms of use for the {BRAND} website and free claim tools, including no legal advice and limits of liability.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Content is provided for general information about insurance appraisal and property claims in Tennessee.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when both parties sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws change. Consult a licensed Tennessee attorney about legal questions.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates from the figures you enter. Example and default figures are illustrative. None of it is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. Photographs are public-domain or CC0 images used for illustration and don’t depict our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Tennessee.</p>""", "The terms that apply when you use this website and its tools."),
        P_DISC: ("Legal Disclaimer", f"Legal Disclaimer | {BRAND}", f"Legal disclaimer for {BRAND}: general information only, no legal advice, illustrative figures, no guarantees.", f"""
<h2>General information</h2><p>Content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, don’t give legal advice, and don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Statutes and case law</h2><p>References to Tennessee statutes, including the bad-faith penalty statute, are general descriptions for context. Laws and court interpretations change. Verify current law with official sources and a Tennessee attorney.</p>
<h2>No guaranteed results</h2><p>Each claim is different. Figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is close, talk to a Tennessee attorney promptly.</p>
<h2>Weather and events</h2><p>Descriptions of storms and other events are summaries for context, based on public reporting. Verify specifics with official sources such as the National Weather Service and the Tennessee Department of Commerce and Insurance.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h1, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office", cta=False) + f'<div class="shell layout"><article class="prose narrow">{content}</article><aside class="aside"><div class="aside-in">{call_box()}</div></aside></div>'
        write(path, document(path, title, desc, body, [], photo="office", trail=trail), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("Who we are", P_ABOUT), ("Free claim review", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Service areas", [("All service areas", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", P_PRIVACY), ("Terms of use", P_TERMS), ("Legal disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="map-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "office", cta=False) + f'<section class="sec"><div class="shell"><div class="map-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | Every Page on {BRAND}",
                         f"HTML site map of {BRAND} listing every service, Tennessee service area, free claim tool, guide and legal page we publish.",
                         body, [], photo="office", trail=trail), 0.3)

    body = f"""<section class="page-hero"><div class="ph-media">{img("storm-tree", "zoom", lazy=False, alt="")}</div><div class="shell ph-in"><p class="kicker">Error 404</p><h1>That page went missing in the storm</h1><p class="lede">The page you’re looking for may have moved or never existed. These links will get you back on track.</p><div class="btn-row"><a class="btn red" href="/">Home</a><a class="btn outline-light" href="{SVC_BASE}">Services</a><a class="btn outline-light" href="{TOOL_BASE}">Free tools</a><a class="btn outline-light" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                f"This page could not be found on {BRAND}. Use these links to reach our services, free claim tools or contact page.",
                                body, robots="noindex,follow", photo="storm-tree", trail=[("Home", "/"), ("Page not found", "/404")]), sitemap=False)


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
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_CONTENT.encode("ascii"))


GUARD_PHP = r"""<?php
// Tennessee Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$tia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$tia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$tia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($tia_host === 'www.' . $tia_real || ($tia_host === $tia_real && $tia_proto === 'http')) {
    header('Location: https://' . $tia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $tia_m)) {
    $tia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $tia_m[1] . $tia_q, true, 301);
    exit;
}
// Keep the preview domain (and any other host) out of search results.
if ($tia_host !== $tia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
""".replace("__HOST__", HOST)

INDEX_PHP = r"""<?php
// Tennessee Insurance Appraiser - front controller for the static build.
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
