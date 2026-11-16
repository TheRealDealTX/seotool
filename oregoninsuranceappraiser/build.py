#!/usr/bin/env python3
"""Static site generator for oregoninsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
Pages are written as dir/index.php (canonical-host guard + static HTML); the homepage is home.html.
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

BRAND = "Oregon Insurance Appraiser"
HOST = "oregoninsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261116a"
FAV = "1"
HOURS = "Mon–Fri 8am–6pm PT"

# Google Tag Manager: leave empty until a container ID is provided (e.g. "GTM-XXXXXXX").
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/property-appraisals/"
LOC_BASE = "/appraisal-near-you/"
TOOL_BASE = "/oregon-claim-calculators/"
POST_BASE = "/policy-pointers/"
PROCESS = "/oregon-appraisal-roadmap/"
FAQ_P = "/claim-questions-oregon/"
GLOSS = "/insurance-claim-dictionary/"
ABOUT = "/about-our-oregon-team/"
CONTACT = "/reach-an-appraiser/"
PRIVACY = "/oregon-privacy-policy/"
TERMS = "/website-terms-oregon/"
DISCLAIMER = "/appraisal-disclaimer-oregon/"
SITEMAP = "/oregon-site-map/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, OR"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
ALT = {k: v.get("alt", "") for k, v in PHOTOS.items()}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


from photomap import SVC_PHOTO, LOC_PHOTO, TOOL_PHOTO, POST_PHOTO, PAGE_PHOTO, REGION_PHOTO  # noqa: E402

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9"/><path d="M9 4l3 2 3-2M9 20l3-2 3 2M4 9l2 3-2 3M20 9l-2 3 2 3"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "forest": '<path d="M8 3l-5 8h3l-3 5h10l-3-5h3zM8 16v5M17 7l-3 5h2l-2 4h6l-2-4h2zM17 16v5"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


SVC_ICON = {
    "appraisal-clause-help": "doc", "home-insurance-appraisal": "home", "commercial-hoa-appraisal": "building",
    "roof-hail-appraisal": "hail", "windstorm-tornado-appraisal": "wind", "ice-storm-snow-appraisal": "snow",
    "water-damage-appraisal": "drop", "house-fire-smoke-appraisal": "flame", "wildfire-loss-appraisal": "forest",
    "fallen-tree-appraisal": "tree", "carrier-estimate-review": "file", "neutral-umpire-services": "scale",
}


def mark():
    """Brand mark: navy tile, yellow Cascade peaks, white level line (an appraiser's even measure)."""
    return ('<svg viewBox="0 0 48 48" width="46" height="46" aria-hidden="true"><rect width="48" height="48" rx="11" fill="#002a86"/>'
            '<path d="M7 33.5L18.5 15l6 9.2 4.2-5.7L41 33.5z" fill="#ffea0f"/>'
            '<path d="M18.5 15l-3.4 5.5 2.3-.9 1.3 1.7 1.4-1.6 2 .9z" fill="#fff"/>'
            '<rect x="7" y="36.5" width="34" height="3.2" rx="1.6" fill="#fff"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "OR", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-OR", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Oregon property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 36 Oregon counties.",
        "areaServed": [{"@type": "State", "name": "Oregon"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Wildfire claims", "Ice storm damage", "Windstorm damage"],
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
LEARN = [("The appraisal path", PROCESS), ("Questions answered", FAQ_P), ("Claim dictionary", GLOSS), ("Policy pointers", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Oregon cities", LOC_BASE), True),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE), False),
        ("Resources", LEARN, None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="full"><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="mega{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    brand = f'{mark()}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="utility"><div class="wrap"><span class="u-l">Appraisal for disputed property claims · <b>All 36 Oregon counties</b></span>
<span class="u-r"><a class="hide-s" href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></span></div></div>
<header class="head"><div class="wrap"><div class="bar">
<a class="brand" href="/" aria-label="{BRAND} home">{brand}</a>
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn sun head-cta" href="tel:{TEL}">{ic("phone")} {PHONE}</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top"><a class="brand" href="/">{brand}</a><button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>{HOURS} · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-top">
<div><a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>
<p>Independent appraisal and estimating for Oregon property owners whose insurance claims came up short, from Astoria to Ontario and Portland to Brookings.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>{HOURS}</span></div></div>
<div><h2 class="ft">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="ft">Cities</h2><ul>{loc}</ul></div>
<div><h2 class="ft">Calculators</h2><ul>{tl}</ul></div>
<div><h2 class="ft">Company</h2><ul><li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact</a></li><li><a href="{PROCESS}">The appraisal path</a></li><li><a href="{FAQ_P}">Questions answered</a></li><li><a href="{GLOSS}">Claim dictionary</a></li><li><a href="{POST_BASE}">Policy pointers</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIMER}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and are not a public adjuster. Information on this site is general and educational; policy terms vary. Example figures are illustrative. Results depend on the facts of each claim and are never guaranteed.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">Call now</a><a href="{CONTACT}">Free review</a></div>"""


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


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None):
    canonical = DOMAIN + path
    page_type, extra_nodes, crumb_id = "WebPage", [], None
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
        extra_nodes.append(n)
    img_key = preload or "hero-home"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra_nodes if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")]
    if main:
        webpage["mainEntity"] = {"@id": main[0]}
    elif any(n.get("@type") == "FAQPage" for n in extra_nodes):
        webpage["mainEntity"] = {"@id": canonical + "#faq"}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = ""
    if preload:
        pre = f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, /assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n'
    on_hero = ' class="on-hero"'
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Oregon">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Oregon">
<meta name="geo.region" content="US-OR">
<meta name="geo.placename" content="Oregon">
<meta name="theme-color" content="#002a86">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:wght@600;700;800&family=Rubik:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body{on_hero}>
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
    # The host serves real files without running the front controller, so every directory page is
    # dir/index.php and starts with the canonical-host guard. The homepage is home.html (served by index.php).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
        assert "<?" not in content, f"PHP tag in page HTML: {path}"
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
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts fade-up" style="animation-delay:.3s">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row fade-up" style="animation-delay:.22s"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-w" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.12"')}<div class="wrap">{crumbs(trail)}<span class="kicker fade-up">{e(tag)}</span><h1 class="fade-up" style="animation-delay:.08s">{e(h1)}</h1><p class="lede fade-up" style="animation-delay:.15s">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk through your claim</h2><p>The first conversation is free. We’ll tell you straight whether appraisal fits.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn sun" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span aria-hidden="true">›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Settlement short of the repair bill?", p="Send us the insurer’s estimate and your photos. We’ll tell you what we see."):
    return f"""<section class="cta-band"><div class="wrap"><div class="in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn line" href="{CONTACT}">Email the estimate</a></div></div></div></section>"""


LOSSES = ["Wind / windstorm", "Ice storm / snow", "Fallen tree", "Wildfire", "Fire / smoke", "Water / leak", "Hail", "Earthquake", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel="h2"):
    roles = ["Homeowner", "Condo / HOA board", "Landlord / property manager", "Business owner", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Oregon"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hlevel}>{e(heading)}</{hlevel}><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(cities)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See our <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow", "ar")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def ticket_form():
    return f"""<div class="ticket fade-up" style="animation-delay:.45s"><div class="ticket-top"><span>Free claim review</span><span>{PHONE}</span></div>
<form action="/api/contact.php" method="post" data-lead novalidate>
<h2>Is your settlement short?</h2><p class="sub">Leave a few details. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See our <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn" type="submit">Request my free review {ic("arrow", "ar")}</button>
<div class="form-msg" role="status"></div>
<p class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form></div>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Portland Metro", ["Ice storms", "Falling firs", "Gorge east winds", "Condo water losses"],
     "Oregon’s busiest claim market. Ice storms in 2021 and 2024 brought down trees across Multnomah County, Washington County and Clackamas County, and older housing makes every repair more expensive.",
     "Portland, Beaverton, Hillsboro, Lake Oswego, Gresham"),
    ("Willamette Valley", ["Windstorms", "Snow & ice", "Santiam Canyon fires", "Tornado (rare)"],
     "From Salem to Eugene, big-leaf maples and Douglas firs meet winter storms. The 2019 snowstorm and the 2020 Labor Day fires both left deep marks.",
     "Salem, Eugene, Corvallis, Albany, Springfield"),
    ("Oregon Coast", ["Coastal gales", "Wind-driven rain", "Salt-air wear", "Vacation rentals"],
     "The 2007 Great Coastal Gale set the benchmark. Wind-driven rain and salt air shape every roof and siding argument from Astoria to Brookings.",
     "Newport, Lincoln City, Seaside, Coos Bay, Astoria"),
    ("Southern Oregon", ["Wildfire", "Smoke infiltration", "Extreme heat", "Manufactured homes"],
     "The Almeda Fire swept from Ashland toward Medford in 2020. Wildfire, smoke and heat now drive many Rogue Valley claims.",
     "Medford, Grants Pass, Ashland, Roseburg, Klamath Falls"),
    ("Central Oregon", ["Snow load", "Hail", "Frozen pipes", "Wildfire risk"],
     "High-desert winters and summer thunderstorms. Many second homes sit empty for weeks, which changes how frozen-pipe claims play out.",
     "Bend, Redmond, Sisters, Sunriver, Prineville"),
    ("Eastern Oregon", ["Hail", "Thunderstorm wind", "Hard freezes", "Farm buildings"],
     "Wheat country and ranch land, where hail and downbursts damage roofs, siding and outbuildings.",
     "Pendleton, Hermiston, La Grande, Baker City, Ontario"),
]

RECORD = [
    ("1962", "Columbus Day Storm", "A remnant typhoon brought extreme winds to western Oregon, toppling trees and damaging buildings across the Willamette Valley. It remains the benchmark Pacific Northwest windstorm."),
    ("2007", "Great Coastal Gale", "In early December, hurricane-force gusts hit the Oregon coast, knocking out power for days and damaging roofs, siding and trees from Astoria south."),
    ("2010", "Aumsville tornado", "An EF2 tornado struck the small Marion County town of Aumsville in December, a reminder that Oregon tornadoes are rare but real."),
    ("2019", "Willamette Valley snowstorm", "Heavy, wet February snow brought down thousands of trees and limbs on homes in Eugene, Springfield and the southern valley."),
    ("2020", "Labor Day fires", "Wind-driven wildfires, including Almeda, Beachie Creek, Lionshead, Holiday Farm and Archie Creek, destroyed thousands of Oregon homes in a few days."),
    ("2021", "February ice storm", "Freezing rain coated the Portland and Salem areas, bringing down trees and power lines and leaving many homes without power for days."),
]

LEAKS = [
    ("Matching left out", "One slope of roof or one wall of siding approved, when the rest can’t be matched.", "Illustrative gap: $6,000–$15,000"),
    ("Old-house finishes priced as new", "Plaster walls, old-growth fir trim and original hardwood priced as builder-grade drywall and laminate.", "Illustrative gap: $4,000–$12,000"),
    ("Tree impact priced as a patch", "A fallen fir scoped as a roof repair with no framing, decking or interior damage.", "Illustrative gap: $8,000–$30,000"),
    ("Drying stopped too early", "Water losses closed out before crawlspaces, insulation and subfloor were dry.", "Illustrative gap: $3,000–$10,000"),
    ("Code items missing", "Underlayment, flashing and other work a building department can require during repairs.", "Illustrative gap: $2,000–$8,000"),
    ("Post-disaster pricing ignored", "Rebuild costs estimated at normal prices after a regional wildfire or ice storm.", "Illustrative gap: varies widely"),
]


def home():
    feat = [SVC_BY["wildfire-loss-appraisal"], SVC_BY["ice-storm-snow-appraisal"], SVC_BY["appraisal-clause-help"]]
    tags = ["Oregon’s biggest losses", "Winter storms", "Core service"]
    fcards = "".join(f'<a class="pcard rv" href="{SVC_BASE}{s["slug"]}/">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}<span class="tag">{t}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></a>' for s, t in zip(feat, tags))
    rows = "".join(f'<a href="{SVC_BASE}{s["slug"]}/"><span class="i">{ic(SVC_ICON[s["slug"]])}</span><span><b>{e(s["name"])}</b><small>{e(s["short"][:72].rsplit(" ", 1)[0])}…</small></span>{ic("arrow", "go")}</a>' for s in SERVICES if s not in feat)

    regions = "".join(f'<article class="region">{img(REGION_PHOTO[i], sizes="(max-width:700px) 84vw, 360px", alt="")}<div class="in"><span class="idx">{i + 1:02d} / {len(REGIONS):02d}</span><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(p)}</li>" for p in ps)}</ul><p>{e(t)}</p><p class="cities">{e(c)}</p></div></article>' for i, (n, ps, t, c) in enumerate(REGIONS))

    trail = "".join(f'<div class="tstep rv"><span class="dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, (t, p) in enumerate(PROCESS_STEPS))

    tcards = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="kind">{t["kind"]}</span></span><span class="tb"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open</span></span></a>' for t in TOOLS)
    tcards += f'<a class="tcard all rv" href="{TOOL_BASE}"><h3>All seven calculators</h3><p>Free, private and built from real appraisal files.</p><span class="more">See them all</span></a>'

    record = "".join(f'<article class="rv"><span class="yr">{y}</span><h3>{e(t)}</h3><p>{e(p)}</p></article>' for y, t, p in RECORD)
    lcards = "".join(f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    posts = "".join(f'<article class="post rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pb"><span class="meta">{p["read"]} read</span><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="link" href="{POST_BASE}{p["slug"]}/">Read the guide</a></div></article>' for p in POSTS[:3])
    leaks = "".join(f'<div class="leak rv"><span class="n">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p><span class="eg">{e(g)}</span></div>' for i, (t, p, g) in enumerate(LEAKS))

    home_faqs = [
        ("What does an Oregon Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As the appraiser you appoint, we inspect, write an independent line-item estimate, work with the insurer’s appraiser and, if needed, present open items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When is it worth calling an Oregon Insurance Appraiser?", "When coverage is accepted, you have the insurer’s estimate, and the gap to your contractor’s number is meaningful, roughly more than 10% or several thousand dollars."),
        ("Is the appraisal award binding?", "On the amount of loss, yes, once two of the three panel members sign. That is why the file you bring matters."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We quote our fee in writing before work begins, and the first conversation is free."),
        ("Do you cover my part of Oregon?", "Yes. We work in all 36 counties, from the Portland metro and Willamette Valley to the coast, Southern, Central and Eastern Oregon."),
    ]

    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.18"')}</div><span class="hero-stripe" aria-hidden="true"></span>
<div class="wrap">
<div>
<span class="kicker light fade-up">Statewide · Independent · Policyholder side</span>
<h1 class="fade-up" style="animation-delay:.1s">Oregon Insurance Appraiser for claims that were <span class="hl-sun">paid short</span></h1>
<p class="lede fade-up" style="animation-delay:.2s">When your insurer accepts the claim but the check won’t rebuild what the storm, the ice or the fire took, Oregon Insurance Appraiser builds an independent, line-by-line valuation and takes it through the appraisal clause in your policy.</p>
<div class="btn-row fade-up" style="animation-delay:.3s"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-w" href="#services">See what we appraise {ic("arrow", "ar")}</a></div>
<ul class="hero-points fade-up" style="animation-delay:.4s"><li><b>You appoint us</b>Your appraiser, not the insurer’s</li><li><b>Line by line</b>Priced for your part of Oregon</li><li><b>Homes to HOAs</b>Residential and commercial</li></ul>
</div>
{ticket_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap"><div class="ledger-in rv">
<div class="cell"><b data-count="36">36</b><span>Oregon counties covered</span></div>
<div class="cell"><b data-count="12">12</b><span>Appraisal &amp; estimating services</span></div>
<div class="cell"><b data-count="7">7</b><span>Free claim calculators</span></div>
<div class="cell"><b>2 of 3</b><span>Signatures make an award</span></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">Where the money goes missing</span><h2>Six places an Oregon claim usually comes up short</h2></div><p>Most underpaid claims aren’t denied. They’re just incomplete. These are the gaps an Oregon Insurance Appraiser finds again and again in estimates written after Oregon storms and fires. The dollar ranges are illustrative only, not results from any client.</p></div>
<div class="leaks" data-stagger>{leaks}</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">What we appraise</span><h2>Twelve services from Oregon Insurance Appraiser</h2></div><p>Every service answers one question: what does this loss really cost to put right? Start with an estimate review, or bring Oregon Insurance Appraiser in once appraisal has been demanded.</p></div>
<div class="svc-feature" data-stagger>{fcards}</div>
<div class="svc-rows rv">{rows}</div>
<p style="margin-top:34px"><a class="btn line" href="{SVC_BASE}">Compare all appraisal services {ic("arrow", "ar")}</a></p>
</div></section>

<section class="sec navy on-dark"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker light">Six claim climates</span><h2>Oregon’s weather, read the way an estimate should read it</h2></div><div><p>Ice in Portland, wind on the coast, wildfire in the Rogue Valley, hail near Pendleton. Oregon Insurance Appraiser prices each region’s damage on its own terms.</p><div class="strip-nav" style="margin-top:18px"><button type="button" data-strip="-1" aria-label="Scroll regions back">{ic("left")}</button><button type="button" data-strip="1" aria-label="Scroll regions forward">{ic("arrow")}</button></div></div></div>
<div class="strip-wrap"><div class="strip" data-strip-track tabindex="0" aria-label="Oregon regions">{regions}</div></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">The appraisal trail</span><h2>From a short check to a signed award</h2></div><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. This is the trail an Oregon Insurance Appraiser walks with you.</p></div>
<div class="trail" data-trail>{trail}</div>
<p style="margin-top:40px"><a class="link" href="{PROCESS}">Read the full appraisal path, stage by stage</a></p>
</div></section>

<section class="sec white"><div class="wrap gap-split">
<div class="rv"><span class="kicker">Two-number check</span><h2>Run the gap before you pick up the phone</h2><p>Type in the insurer’s estimate and your contractor’s. If the difference is large, a call with an Oregon Insurance Appraiser makes sense. If it’s small, a documented supplement may close it faster and cheaper.</p><p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds fees and three award scenarios.</p></div>
<div class="rv">{PAYOFF_MINI}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">Free &amp; private</span><h2>Claim calculators from Oregon Insurance Appraiser</h2></div><p>Seven tools built from appraisal work, including a wildfire contents estimator made for Oregon’s total-loss claims. They run in your browser and nothing is stored or sent.</p></div>
<div class="tool-grid" data-stagger>{tcards}</div>
</div></section>

<section class="sec navy on-dark"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker light">The storm record</span><h2>Events that still shape Oregon claim files</h2></div><p>Every Oregon Insurance Appraiser estimate is written with this history in mind: what each kind of event does to a building, and what adjusters tend to miss afterwards.</p></div>
<div class="record" data-stagger>{record}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">Local pages</span><h2>Oregon Insurance Appraiser in your city</h2></div><p>We serve every county in the state. These twelve pages cover the places where Oregon Insurance Appraiser handles claims most often, with local storm history and housing notes. <a href="{LOC_BASE}">See statewide coverage</a>.</p></div>
<div class="loc-grid" data-stagger>{lcards}</div>
</div></section>

<section class="sec white"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">Three roles, one claim</span><h2>Where an appraiser fits next to adjusters and lawyers</h2></div><p>Choosing the right help first saves time and fees. Oregon Insurance Appraiser will tell you when your claim needs someone else.</p></div>
<div class="roles" data-stagger>
<div class="role me rv"><span class="who">Oregon Insurance Appraiser</span><h3>Values the loss</h3><dl><dt>Best when</dt><dd>Coverage is accepted and the number is disputed</dd><dt>Ends with</dt><dd>A binding award on the amount of loss</dd></dl></div>
<div class="role rv"><span class="who">Public adjuster</span><h3>Handles the claim</h3><dl><dt>Best when</dt><dd>You want someone to manage the claim from the start</dd><dt>Ends with</dt><dd>A negotiated settlement</dd></dl></div>
<div class="role rv"><span class="who">Oregon attorney</span><h3>Handles legal disputes</h3><dl><dt>Best when</dt><dd>The claim is denied, a deadline is near, or conduct is the issue</dd><dt>Ends with</dt><dd>A settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec tint"><div class="wrap split top">
<div class="rv"><span class="kicker">Questions</span><h2>Asked often of an Oregon Insurance Appraiser</h2><p>Plain answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row" style="margin-top:22px"><a class="btn" href="{FAQ_P}">All questions {ic("arrow", "ar")}</a><a class="btn line" href="{GLOSS}">Claim dictionary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><div><span class="kicker">Policy pointers</span><h2>Short guides worth reading first</h2></div><p>Practical reading from the Oregon Insurance Appraiser team on policy wording, documentation and choosing the right path. <a href="{POST_BASE}">All guides</a>.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="cta-par">{img("coast-waves", "bg", alt="", extra=' data-parallax="0.18"')}<div class="wrap rv"><span class="kicker light">Before you sign off</span><h2>Check the numbers before you accept them</h2><p>A short review now can keep you from accepting a settlement that won’t cover the repair.</p><div class="btn-row"><a class="btn sun" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line-w" href="#contact">Send your estimate</a></div></div></section>

<section class="sec navy on-dark" id="contact"><div class="wrap contact">
<div class="rv"><span class="kicker light">Start with a conversation</span><h2>Talk with an Oregon Insurance Appraiser about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>{HOURS}</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Coverage</span><b>All 36 Oregon counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hlevel="h3")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Oregon Insurance Appraiser: independent appraisal and estimate review for underpaid wildfire, ice storm, wind, water and fire claims statewide.",
                        body, schema, preload="hero-home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for s in SERVICES:
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        i = SERVICES.index(s)
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        locs = [(loc_label(l), loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Oregon cities", locs + [("All Oregon cities", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Oregon"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="index-card rv" href="{SVC_BASE}{s["slug"]}/"><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 240px", alt="")}</span><span class="ib"><span class="k">Service {i + 1:02d}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p></span></a>' for i, s in enumerate(SERVICES))
    ph = PAGE_PHOTO["services"]
    body = page_hero(trail, "What we do", "Oregon Insurance Appraisal Services",
                     "From a single estimate review to full appraisal panel representation and neutral umpire work, every service is built around an accurate, defensible valuation of your Oregon property loss.", ph) + f"""
<section class="sec"><div class="wrap"><div class="index-list" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><span class="kicker">Not sure where to start?</span><h2>Most claims start with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what the gap is worth. A review answers that, and many disputes end there.</p><a class="btn" href="{SVC_BASE}carrier-estimate-review/">About estimate reviews {ic("arrow", "ar")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle residential and commercial claims?", "Yes: houses, condos, rentals, apartments, retail, office, industrial, churches and associations."), ("Do you only handle wildfire claims?", "No. We handle wind, ice, snow, water, fire, tree, hail and other covered perils across Oregon.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Oregon Insurance Appraisal Services | 12 Ways We Help",
                             "Oregon insurance appraisal services: appraisal clause representation, wildfire, ice, wind, water and fire claims, estimate review and umpires.",
                             body, schema, preload=ph), 0.9)


LOC_DESC = {
    "portland": "Insurance appraiser in Portland, Oregon for underpaid ice storm, fallen fir, water and condo claims in older homes and towers across the city.",
    "beaverton": "Insurance appraiser in Beaverton, Oregon for underpaid wind, ice and water claims on ranch homes and HOA townhomes in Washington County.",
    "hillsboro": "Insurance appraiser in Hillsboro, Oregon for disputed home, apartment and commercial roof claims after windstorms and ice in Washington County.",
    "lake-oswego": "Insurance appraiser in Lake Oswego, Oregon for underpaid fallen tree, ice storm and high-value interior claims in Clackamas County homes.",
    "salem": "Insurance appraiser in Salem, Oregon for underpaid ice storm, fallen tree, smoke and wind claims in the capital and the nearby Santiam Canyon.",
    "eugene": "Insurance appraiser in Eugene, Oregon for disputed snow, fallen tree, wildfire and smoke claims across Lane County and the McKenzie corridor.",
    "corvallis": "Insurance appraiser in Corvallis, Oregon for underpaid wind, tree, ice and water claims on homes and rentals in Benton County near OSU.",
    "bend": "Insurance appraiser in Bend, Oregon for disputed snow load, hail, frozen pipe and smoke claims on Central Oregon homes and second homes.",
    "medford": "Insurance appraiser in Medford, Oregon for underpaid wildfire, smoke and storm claims across the Rogue Valley, including Almeda Fire losses.",
    "grants-pass": "Insurance appraiser in Grants Pass, Oregon for disputed wildfire, smoke and storm claims on homes, acreage and barns in Josephine County.",
    "newport": "Insurance appraiser in Newport, Oregon for underpaid coastal gale and wind-driven rain claims on Lincoln County homes and vacation rentals.",
    "pendleton": "Insurance appraiser in Pendleton, Oregon for disputed hail, thunderstorm wind and winter claims on homes and farm buildings in Umatilla County.",
}


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        body = page_hero(trail, l["region"], f"Insurance Appraiser in {l['city']}, Oregon", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="note"><b class="h">Local claim risks</b><ul class="chips" style="margin:10px 0 0">{chips}</ul></div>
{l["body"]}
<h2>Neighborhoods we cover</h2>
<p>We inspect homes and buildings throughout {e(l["city"])}, including {e(l["hoods"])}, and the surrounding parts of {e(l["county"])}.</p>
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to property owners in {e(l["city"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Oregon cities", items, path)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Oregon"}}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        title = f"Insurance Appraiser in {l['city']}, OR | Claim Appraisal"
        if len(title) > 58:
            title = f"Insurance Appraiser in {l['city']}, Oregon"
        write(path, document(path, title, LOC_DESC[l["slug"]], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cards = "".join(f'<a class="lcard rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<b>{e(l["city"])}</b><small>{e(l["county"])}</small></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="index-card rv"><span class="ph">{img(REGION_PHOTO[i], sizes="(max-width:700px) 100vw, 240px", alt="")}</span><span class="ib"><span class="k">Region {i + 1:02d}</span><h2>{e(n)}</h2><p>{e(t)}</p><p style="margin-top:10px;font-size:.88rem;color:var(--muted)">{e(c)}</p></span></div>' for i, (n, _p, t, c) in enumerate(REGIONS))
    ph = PAGE_PHOTO["locations"]
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across All 36 Oregon Counties",
                     "Oregon Insurance Appraiser works statewide, from the Columbia River to the Siskiyous and from the coast to the Snake River. These local pages cover the cities where we handle claims most often.", ph) + f"""
<section class="sec"><div class="wrap"><div class="loc-grid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head solo rv"><div><span class="kicker">Regions</span><h2>How claims differ across Oregon</h2><p>The same policy wording plays out very differently in a Portland bungalow, a Bend vacation home and a Newport beach cottage.</p></div></div><div class="index-list" data-stagger>{reg}</div></div></section>
{cta_band("Don’t see your city?", "We cover every Oregon county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Oregon Insurance Appraiser Cities | Statewide Coverage",
                             "Oregon insurance appraiser coverage in all 36 counties, with local pages for Portland, Salem, Eugene, Bend, Medford, Newport and more.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], preload=ph), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for t in TOOLS:
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        i = TOOLS.index(t)
        others = "".join(f'<a href="{TOOL_BASE}{o["slug"]}/"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tight" style="padding-bottom:0"><div class="wrap"><div class="rv">{t["markup"]}</div>
<p class="hint">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout" style="padding-top:40px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free calculators</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All calculators", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    tiles = "".join(f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 50vw, 25vw", alt="")}<span class="kind">{t["kind"]}</span></span><span class="tb"><h2 style="font-size:1.08rem">{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open</span></span></a>' for t in TOOLS)
    ph = PAGE_PHOTO["tools"]
    body = page_hero(trail, "Free & private", "Free Oregon Insurance Claim Calculators",
                     "Seven calculators and planners built from appraisal work. Check the insurer’s math, size up a wildfire contents claim and plan your deadlines. No sign-up, nothing stored.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tool-grid" data-stagger>{tiles}</div></div></section>
<section class="sec tint"><div class="wrap split top"><div class="rv"><span class="kicker">Suggested order</span><h2>Using the calculators together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a> so nothing lapses.</li><li>Check roof measurements with the <a href="{TOOL_BASE}roof-pitch-squares-converter/">roof pitch and squares converter</a>.</li><li>See what you’re actually owed with the <a href="{TOOL_BASE}percentage-deductible-checker/">deductible checker</a> and the <a href="{TOOL_BASE}depreciation-holdback-tracker/">holdback tracker</a>.</li><li>Size up contents after a total loss with the <a href="{TOOL_BASE}wildfire-contents-estimator/">wildfire contents estimator</a>.</li><li>Test the dispute with the <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a>, then take the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Oregon Insurance Claim Calculators | 7 Tools",
                              "Free Oregon insurance claim calculators: appraisal payoff, depreciation, roof squares, percentage deductible, deadlines and wildfire contents.",
                              body, schema, preload=ph), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("The appraisal path", path)]
    ph = PAGE_PHOTO["process"]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Oregon",
                     "Eight stages from the first disagreement to a signed award: what happens, who does what, and where Oregon claims most often go wrong.", ph,
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="trail-rail" data-rail aria-hidden="true"><i></i></div>
{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Oregon", "description": "The eight stages of a property insurance appraisal, from disagreement to signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{DOMAIN}{path}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Oregon | 8 Stages",
                         "How insurance appraisal works in Oregon, in eight stages: the written demand, naming appraisers, the umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], preload=ph), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Questions answered", path)]
    groups = "".join(f'<h2>{e(g)}</h2>{faq_block(qs)}' for g, qs in FAQ)
    allq = [qa for _, qs in FAQ for qa in qs]
    ph = PAGE_PHOTO["faq"]
    body = page_hero(trail, "Answers", "Oregon Insurance Appraisal Questions, Answered",
                     "Plain answers to the questions we hear most about the appraisal process, costs, timing and Oregon’s rules and resources.", ph) + f"""
<div class="wrap layout"><article class="prose">{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Oregon Insurance Appraisal FAQ | Costs, Timing & Rules",
                         "Oregon insurance appraisal FAQ, grouped by topic: how appraisal works, what it costs, deadlines, Oregon rules and working with us.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload=ph), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim dictionary", path)]
    gl = sorted(GLOSSARY, key=lambda t: t[0].lower())
    letters = sorted({t[0][0].upper() for t in gl})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in gl:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{term}</dt><dd>{e(d)}</dd>"
    ph = PAGE_PHOTO["glossary"]
    body = page_hero(trail, "Reference", "Insurance Claim Dictionary for Oregon Property Owners",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English, with Oregon-specific entries.", ph, cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the dictionary</label><input id="gloss-filter" type="search" placeholder="Try “depreciation” or “umpire”"></div><p class="gloss-count" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Oregon property insurance claim dictionary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": html.unescape(t), "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in gl]}
    write(path, document(path, "Insurance Claim Dictionary | ACV, RCV, Umpire & More",
                         "Searchable insurance claim dictionary: actual cash value, replacement cost, depreciation, appraisal award, umpire, FAIR Plan, DFR and more.",
                         body, [crumbs_schema(trail), dts], preload=ph), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Policy pointers", POST_BASE), (p["title"], path)]
        i = POSTS.index(p)
        others = "".join(f'<a href="{POST_BASE}{o["slug"]}/"><small>Guide</small>{e(o["title"])}</a>' for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Policy pointers", path)]
    cards = "".join(f'<article class="post rv"><a class="ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a><div class="pb"><span class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</span><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="link" href="{POST_BASE}{p["slug"]}/">Read the guide</a></div></article>' for p in POSTS)
    ph = PAGE_PHOTO["posts"]
    body = page_hero(trail, "Policy pointers", "Guides for Oregon Property Owners With Disputed Claims",
                     "Short, practical guides on policy wording, documentation and choosing the right path, written by people who work appraisal panels.", ph, cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Oregon Insurance Claim Guides | Policy Pointers",
                         "Oregon insurance claim guides on appraisal clauses, wildfire total losses, ice storms, earthquake coverage and reading the insurer’s estimate.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], preload=ph), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    ph = PAGE_PHOTO["about"]
    body = page_hero(trail, "About us", "About Oregon Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can follow it.", ph) + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img(PAGE_PHOTO["about-inline"], sizes="(max-width:1040px) 100vw, 760px")}</figure>
<h2>Why we focus on appraisal</h2>
<p>Many claim professionals do a bit of everything. We chose to specialize. Oregon Insurance Appraiser works on one question, the amount of loss, and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your appointed appraiser, review estimates before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look closely at anyone else’s numbers.</li>
<li><strong>Defensible over dramatic.</strong> A padded estimate may look good on day one, but it loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the insurer’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> Before any work starts, you know what it costs.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Oregon. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We aren’t public adjusters and don’t negotiate claims outside the appraisal process. We don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Statewide, on purpose</h2>
<p>Oregon’s weather and hazards change sharply from the coast to the Willamette Valley, the Cascades and the high desert. Working statewide means we see every kind of loss Oregon produces, from Portland ice storms and coastal gales to Rogue Valley wildfires and Pendleton hail, and price each one with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Oregon cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("The appraisal path", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Oregon Insurance Appraiser | Our Approach",
                         "About Oregon Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss in disputed Oregon claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload=ph), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    ph = PAGE_PHOTO["contact"]
    body = page_hero(trail, "Get in touch", "Contact Oregon Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", ph, cta=False) + f"""
<section class="sec navy on-dark"><div class="wrap contact">
<div class="rv"><span class="kicker light">Direct lines</span><h2>Reach us directly</h2>
<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>{HOURS}</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>Statewide, all 36 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul><li>Your declarations page</li><li>The insurer’s full estimate (PDF)</li><li>Letters or emails from the insurer</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Oregon Insurance Appraiser | (844) 537-1427",
                         "Contact Oregon Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, email us, or send the form.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload=ph), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | Oregon Insurance Appraiser",
                  "Privacy policy for Oregon Insurance Appraiser: what we collect through forms, calls and email, how we use it and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect what you choose to give us, such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with service providers who host our site and email, or when the law requires it.</p>
<h2>Claim calculators</h2><p>Our calculators and checklists run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics, we will update this page.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""", "How we collect, use and protect the information you share with us."),
        TERMS: ("Terms of Use", "Terms of Use | Oregon Insurance Appraiser",
                "Terms of use for the Oregon Insurance Appraiser website and its free claim calculators, including limits on reliance and client status.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Oregon.</p>
<h2>No client relationship</h2><p>Reading this site, using its calculators or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing on this site is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Oregon attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates based on what you enter. Example figures are illustrative. None of it is an appraisal, a quote or a prediction of any claim outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Oregon.</p>""", "The terms that apply when you use this website and its tools."),
        DISCLAIMER: ("Disclaimer", "Legal Disclaimer | Oregon Insurance Appraiser",
                     "Oregon Insurance Appraiser disclaimer: general information only, not legal advice, illustrative examples and no guaranteed claim results.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures and dollar ranges on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is approaching, consult an Oregon attorney promptly.</p>
<h2>Statutes and agencies</h2><p>References to Oregon statutes, the Division of Financial Regulation, the Oregon FAIR Plan or weather events are for general context and are described only in general terms. Check current law and facts with official sources.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>""", "Important limits on the information published on this website."),
    }
    for path, (h, title, desc, content, lede) in legal.items():
        trail = [("Home", "/"), (h, path)]
        ph = PAGE_PHOTO["legal"]
        body = page_hero(trail, "Legal", h, lede, ph, cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], preload=ph), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIMER)]),
    ]
    cols = "".join(f'<div class="index-card plain rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    ph = PAGE_PHOTO["legal"]
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", ph, cta=False) + f'<section class="sec"><div class="wrap"><div class="index-list" data-stagger>{cols}</div></div></section>'
    write(path, document(path, "Site Map | Oregon Insurance Appraiser",
                         "Site map for Oregon Insurance Appraiser: every service, Oregon city page, free claim calculator, guide and legal page, grouped by section.",
                         body, [crumbs_schema(trail)], preload=ph), 0.3)

    ph = PAGE_PHOTO["404"]
    body = f"""<section class="page-hero">{img(ph, "bg", lazy=False, alt="")}<div class="wrap"><span class="kicker">Error 404</span><h1>That page washed out</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn sun" href="/">Home</a><a class="btn line-w" href="{SVC_BASE}">Services</a><a class="btn line-w" href="{TOOL_BASE}">Calculators</a><a class="btn line-w" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", "Page Not Found | Oregon Insurance Appraiser",
                                "Page not found on Oregon Insurance Appraiser. The address may have changed; use the links to reach services, calculators or contact.",
                                body, robots="noindex,follow", preload=ph), sitemap=False)


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
    # Search Console verification file: exact bytes, no newline, wrapper or BOM.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Oregon Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$oia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$oia_real  = 'oregoninsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$oia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://oregoninsuranceappraiser.com - only on the real domain.
if ($oia_host === 'www.' . $oia_real || ($oia_host === $oia_real && $oia_proto === 'http')) {
    header('Location: https://' . $oia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$oia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($oia_uri, '?'), $oia_m)) {
    $oia_q = strpos($oia_uri, '?') !== false ? substr($oia_uri, strpos($oia_uri, '?')) : '';
    header('Location: ' . $oia_m[1] . $oia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($oia_host !== $oia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Oregon Insurance Appraiser - front controller for the static build.
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
    bad = [os.path.join(dp, f) for dp, _, fs in os.walk(OUT) for f in fs if f == "index.html"]
    assert not bad, f"index.html must never be written: {bad}"
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
