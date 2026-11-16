#!/usr/bin/env python3
"""Static site generator for mississippiinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Engineering (guard, front controller, deploy, form) follows the
sister-site template; content, slugs and design are specific to this site.
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
from learn import PROCESS_INTRO, PROCESS_STEPS, PROCESS_FAQS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, PAYOFF_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Mississippi Insurance Appraiser"
HOST = "mississippiinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
HOURS = "Mon–Fri 8am–6pm CT"
TODAY = date.today().isoformat()
VER = "20261116a"   # CSS/JS cache-buster
FAV = "1"           # icon cache-buster

# Google Tag Manager: leave empty until a container ID is provided (e.g. "GTM-XXXXXXX").
GTM_ID = ""

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/our-appraisal-services/"
LOC_BASE = "/counties-and-cities/"
TOOL_BASE = "/claim-calculator-suite/"
POST_BASE = "/claim-advice/"
P_PROCESS, P_FAQ, P_GLOSS = "/appraisal-roadmap/", "/questions-answered/", "/insurance-claim-terms/"
P_ABOUT, P_CONTACT = "/who-we-are/", "/talk-to-an-appraiser/"
P_PRIV, P_TERMS, P_DISC, P_MAP = "/privacy-notice/", "/website-terms/", "/legal-disclaimer/", "/page-directory/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}


# ---------------------------------------------------------------- photos
def P(*keys):
    """First photo key that exists in the manifest (lets the layout survive a missing photo)."""
    for k in keys:
        if k in PHOTOS:
            return k
    return next(iter(PHOTOS))


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p.get("alt", ""))
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


def photo_url(key):
    return f"{DOMAIN}/assets/img/photos/{key}.webp"


SVC_PHOTO = {
    "appraisal-demand-representation": P("consultation"), "home-insurance-appraisal": P("porch-home", "brick-ranch"),
    "commercial-hoa-appraisal": P("apartment-complex", "commercial-building"), "roof-hail-claim-appraisal": P("hail-damage", "roof-shingles"),
    "tornado-wind-damage-appraisal": P("tornado-damage", "tornado-roof"), "hurricane-named-storm-appraisal": P("hurricane-damage", "hurricane-debris"),
    "water-plumbing-loss-appraisal": P("water-damage"), "fire-smoke-loss-appraisal": P("house-fire"),
    "fallen-tree-claim-appraisal": P("fallen-tree"), "ice-storm-freeze-appraisal": P("ice-storm"),
    "carrier-estimate-review": P("estimate-laptop", "calculator"), "neutral-umpire-services": P("clipboard", "consultation"),
}
LOC_PHOTO = {
    "jackson-hinds-county": P("jackson-capitol"), "gulfport-harrison-county": P("gulf-coast-harbor"),
    "biloxi-harrison-county": P("gulf-pier-sunset"), "hattiesburg-forrest-county": P("pine-forest"),
    "southaven-desoto-county": P("brick-ranch"), "tupelo-lee-county": P("tupelo-elvis-birthplace"),
    "meridian-lauderdale-county": P("porch-home"), "oxford-lafayette-county": P("storm-supercell"),
    "pascagoula-jackson-county": P("coastal-home"), "vicksburg-warren-county": P("mississippi-river"),
    "columbus-lowndes-county": P("church"), "greenville-washington-county": P("delta-plowed-field"),
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": P("calculator"), "holdback-recovery-calculator": P("estimate-laptop"),
    "roof-pitch-squares-calculator": P("roof-shingles", "roof-inspector"), "named-storm-deductible-calculator": P("storm-clouds"),
    "claim-calendar-builder": P("calendar", "clipboard"), "appraisal-readiness-checkup": P("clipboard"),
    "wind-water-split-estimator": P("flood-home"),
}
POST_PHOTO = {
    "wind-vs-water-after-katrina": P("hurricane-boat"), "mississippi-appraisal-clause-guide": P("consultation"),
    "coast-hurricane-deductibles-explained": P("coastal-home"), "documenting-tornado-damage": P("tornado-roof", "tornado-damage"),
    "ice-storm-tree-claims-north-mississippi": P("ice-storm"), "line-by-line-estimate-reading": P("estimate-laptop", "calculator"),
}
HERO = P("hero-home", "porch-home")

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
    "calc": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="ico"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(size=40):
    """Brand mark: crimson tile, gold roofline over a white 'fair value' level bar."""
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="11" fill="#C21F32"/>'
            '<path d="M10 25.5L24 13l14 12.5" fill="none" stroke="#EAAB22" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15 31h18M15 37h18" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} — home">{mark()}<span class="brand-t"><b>Mississippi</b><span>Insurance Appraiser</span></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    cities = []
    for l in LOCATIONS:
        cities.append({"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Mississippi"}})
    return {
        "@type": "ProfessionalService", "@id": DOMAIN + "/#business", "name": BRAND, "url": DOMAIN + "/",
        "telephone": PHONE_INTL, "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/favicon-512.png", "contentUrl": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "MS", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MS", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, carrier estimate review and umpire services for disputed property claims across all 82 Mississippi counties.",
        "areaServed": [{"@type": "State", "name": "Mississippi"}] + cities,
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hurricane claims", "Wind vs. flood allocation", "Tornado damage", "Xactimate estimates"],
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


# ---------------------------------------------------------------- navigation
RES_LINKS = [("Appraisal roadmap", P_PROCESS), ("Questions answered", P_FAQ), ("Insurance claim terms", P_GLOSS), ("Claim advice", POST_BASE)]


def nav_groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Cities", [(f'{l["city"]}', loc_path(l)) for l in LOCATIONS], ("All counties & cities", LOC_BASE)),
        ("Calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", RES_LINKS + [(p["title"] if len(p["title"]) < 44 else p["title"].split(":")[0], f'{POST_BASE}{p["slug"]}/') for p in POSTS[:3]], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(nav_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        foot = f'<a class="panel-all" href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a>' if allk else ""
        wide = " wide" if len(links) > 8 else ""
        menu += (f'<li class="has-panel"><button type="button" class="nav-btn" aria-expanded="false" aria-controls="np-{i}">{name}{ic("chev", "ico chev")}</button>'
                 f'<div class="panel{wide}" id="np-{i}"><ul>{li}</ul>{foot}</div></li>')
    menu += f'<li><a class="nav-link" href="{P_ABOUT}">About</a></li><li><a class="nav-link" href="{P_CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(nav_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += (f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="dp-{i}">{name}{ic("chev", "ico chev")}</button>'
                f'<div class="acc-panel" id="dp-{i}" hidden><ul>{li}</ul></div></li>')
    acc += f'<li><a class="drawer-link" href="{P_ABOUT}">About</a></li><li><a class="drawer-link" href="{P_CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-head">
<div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul>{menu}</ul></nav>
<a class="btn btn-gold head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div>
</header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="drawer-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send your claim details</a><small>{HOURS} · All 82 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-foot")}
<p>Independent appraisal and estimating help for Mississippi property owners whose insurance claims came up short — from the Delta to the Gulf Coast.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>{HOURS}</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">Every service</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul>{loc}<li><a href="{LOC_BASE}">All 82 counties</a></li></ul></div>
<div><h2 class="foot-h">Calculators</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{P_ABOUT}">Who we are</a></li><li><a href="{P_PROCESS}">Appraisal roadmap</a></li><li><a href="{P_FAQ}">Questions answered</a></li><li><a href="{P_GLOSS}">Claim terms</a></li><li><a href="{POST_BASE}">Claim advice</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal">
<p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, don’t give legal advice and don’t act as a public adjuster. Site content is general and educational; your policy’s wording controls. Example figures are illustrative, and no outcome is ever guaranteed.</p>
<div class="foot-bar"><span>© <span data-year>{date.today().year}</span> {BRAND}</span><ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_MAP}">Page directory</a></li></ul></div>
</div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{P_CONTACT}">{ic("doc")} Free claim review</a></div>"""


# ---------------------------------------------------------------- document
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


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, body_cls="phero-page"):
    canonical = DOMAIN + path
    page_type, page_extra, nodes, crumb_id = "WebPage", {}, [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            page_extra = {k: v for k, v in n.items() if k != "@type"}
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
            n["isPartOf"] = {"@id": canonical + "#webpage"}
        elif t in MAIN_TYPES or t == "ItemList":
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        nodes.append(n)
    pk = photo or HERO
    pimg = PHOTOS[pk]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": photo_url(pk), "width": pimg["fw"], "height": pimg["fh"]},
    }
    webpage.update(page_extra)
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in nodes if n.get("@type") in MAIN_TYPES]
    if not main:
        main = [n["@id"] for n in nodes if n.get("@type") == "ItemList"]
    webpage["mainEntity"] = {"@id": main[0]} if main else {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = ""
    if photo:
        pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
               f'/assets/img/photos/{photo}.webp {PHOTOS[photo]["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Mississippi">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Mississippi">
<meta name="geo.region" content="US-MS">
<meta name="geo.placename" content="Mississippi">
<meta name="theme-color" content="#C21F32">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:wght@600;700;800&family=Commissioner:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
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
    """Homepage -> home.html; 404 -> 404.html; every other page -> dir/index.php behind the canonical-host guard.
    The host serves real files directly without running the root index.php, so each page enforces the guard itself."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<ul class="hero-facts">' + "".join(f"<li><small>{e(k)}</small><b>{e(v)}</b></li>" for k, v in facts) + "</ul>"
    c = f'<div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return (f'<section class="phero"><div class="phero-bg" data-parallax="0.15">{img(photo, lazy=False, alt="")}</div>'
            f'<div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faqs">' + "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="side-box side-call"><h2 class="side-h">Talk it through first</h2><p>Free first conversation. We’ll tell you plainly whether appraisal fits your claim.</p>'
            f'<a class="side-phone" href="tel:{TEL}">{ic("phone")} {PHONE_INTL}</a><a class="btn btn-gold btn-block" href="{P_CONTACT}">Send claim details</a><small>{HOURS}</small></div>')


def link_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-links">{li}</ul></div>'


def layout(article, side):
    return f'<div class="wrap cols"><article class="prose">{article}</article><aside class="side"><div class="side-in">{side}</div></aside></div>'


def related_cards(items):
    return '<div class="rel">' + "".join(f'<a class="rel-card" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


def band(h="Not sure the carrier’s number is right?", p="Send the estimate and a few photos. We’ll review it and tell you what we see — no obligation."):
    return (f'<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div>'
            f'<div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost" href="{P_CONTACT}">Email the estimate</a></div></div></section>')


LOSSES = ["Hurricane / named storm", "Tornado / straight-line wind", "Hail", "Fallen tree", "Ice storm / freeze", "Water / plumbing", "Fire / smoke", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", page="/", fid="f"):
    roles = ["Homeowner", "Business owner", "HOA / condo board", "Property manager", "Church / nonprofit", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Mississippi"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<p class="lead-h">{e(heading)}</p><p class="lead-sub">Free review · no obligation · usually a reply within one business day.</p>
<div class="lead-grid">
<div class="fld"><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div class="fld"><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="fld full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div class="fld"><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div class="fld"><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="fld"><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div class="fld"><label for="{fid}-amt">Approx. amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="fld full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="fld full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<label class="chk full"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy notice</a>.</span></label>
<button class="btn btn-red btn-block full" type="submit">Send my claim details {ic("arrow")}</button>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead lead-hero" action="/api/contact.php" method="post" data-lead novalidate>
<p class="lead-h">Get a free claim review</p><p class="lead-sub">Tell us a little. We’ll call back within one business day.</p>
<div class="fld"><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div class="fld"><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="fld"><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero form)">
<label class="chk"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{P_PRIV}">Privacy notice</a>.</span></label>
<button class="btn btn-red btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="lead-note">{ic("shield")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Gulf Coast", "Hancock · Harrison · Jackson counties", ["Named storms", "Wind vs. flood", "Wind-driven rain", "MWUA policies"],
     "Camille in 1969, Katrina in 2005, Nate and Zeta since. Coastal claims turn on named-storm deductibles, split wind and flood policies and how much of the damage each storm’s wind actually caused.",
     "Bay St. Louis · Gulfport · Biloxi · Ocean Springs · Pascagoula", P("gulf-coast-harbor")),
    ("Pine Belt", "Hattiesburg · Laurel · Columbia", ["Tornadoes", "Falling pines", "Inland hurricane wind", "Hail"],
     "Tall loblolly pines meet spring tornado tracks. The 2013 Hattiesburg tornado and the 2020 Easter outbreak showed how fast roof, tree and contents claims stack up here.",
     "Hattiesburg · Petal · Laurel · Columbia · Purvis", P("pine-forest")),
    ("Capital Region", "Hinds · Madison · Rankin counties", ["Hail", "Frozen pipes", "Water losses", "Straight-line wind"],
     "Historic Belhaven and Fondren homes, brick ranches and fast-growing suburbs. Freeze events and water-system trouble add plumbing losses to the usual hail and wind claims.",
     "Jackson · Brandon · Madison · Ridgeland · Clinton · Pearl", P("jackson-capitol")),
    ("The Delta", "Greenville · Greenwood · Clarksdale", ["Tornadoes", "Metal buildings", "Straight-line wind", "Hail"],
     "Flat, open ground lets storms build and run. Farm shops, grain bins and metal buildings sit beside older homes — the Rolling Fork tornado in 2023 hit both.",
     "Greenville · Cleveland · Greenwood · Clarksdale · Yazoo City", P("delta-farmland")),
    ("North Mississippi", "Oxford · Tupelo · Southaven · Columbus", ["Ice storms", "Tornadoes", "Hail", "Tree damage"],
     "The 1994 ice storm, the 2014 Tupelo and Louisville tornadoes and the 2019 Columbus tornado. Hill-country hardwoods and fast-growing DeSoto County subdivisions keep claims varied.",
     "Southaven · Olive Branch · Oxford · Tupelo · Starkville · Columbus", P("lightning")),
    ("Southwest & East Central", "Vicksburg · Natchez · Meridian", ["Historic homes", "Tornadoes", "Tree damage", "River flooding"],
     "Antebellum and Victorian homes along the river bluffs, plus Meridian’s older neighborhoods. Period materials and ordinance-or-law questions make these estimates harder to get right.",
     "Vicksburg · Natchez · McComb · Brookhaven · Meridian · Philadelphia", P("mississippi-swamp")),
]


def home():
    svc_cards = "".join(
        f'<a class="card rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="card-b"><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>' for s in SERVICES[:9])
    region_cards = "".join(
        f'<article class="region rv"><div class="region-img">{img(ph, sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}<span class="region-tag">{e(sub)}</span></div>'
        f'<div class="region-b"><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul><p>{e(t)}</p><p class="region-cities">{e(c)}</p></div></article>'
        for n, sub, perils, t, c, ph in REGIONS)
    tool_cards = "".join(
        f'<a class="card card-tool rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 25vw", alt="")}<span class="card-kind">{t["kind"]}</span></span>'
        f'<span class="card-b"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open the {t["kind"].lower()} {ic("arrow")}</span></span></a>' for t in TOOLS)
    city_links = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a></li>' for l in LOCATIONS)
    post_cards = "".join(
        f'<article class="card post rv"><a class="card-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a>'
        f'<div class="card-b"><small class="meta">{p["read"]} read</small><h3><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])
    steps = [
        ("Free file review", "We read the policy, the carrier’s estimate and your photos, and tell you whether appraisal fits — or whether you need someone else."),
        ("Independent scope", "On-site inspection, measurements and a line-item estimate priced for your part of Mississippi."),
        ("Written demand", "Appraisal is demanded in writing and your appraiser is named inside the policy’s window."),
        ("Appraiser to appraiser", "We work the differences line by line with the carrier’s appraiser. Many files narrow sharply here."),
        ("Umpire & award", "Anything left goes to a neutral umpire. Two signatures set the amount of loss."),
    ]
    proc = "".join(f'<li class="step"><span class="step-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(steps))
    home_faqs = [
        ("What does a Mississippi Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("Can appraisal settle a wind-versus-flood argument on the Coast?", "Appraisal can value covered wind damage. Whether damage was caused by wind or by flood is often a coverage question, and coverage disputes generally sit outside appraisal. Those may need a Mississippi attorney."),
        ("Is the appraisal award binding?", "Under a typical clause, an award signed by any two of the three panel members sets the amount of loss. That’s why the file should be complete before anyone demands appraisal."),
        ("What does it cost?", "Each side usually pays its own appraiser and splits the umpire. Our fee is agreed in writing before work starts, and the first conversation is free."),
        ("Do you cover my county?", "Yes. We work in all 82 Mississippi counties, from DeSoto County to Hancock County and from the Delta to the eastern state line."),
    ]
    K = BRAND
    body = f"""
<section class="hero">
<div class="hero-bg" data-parallax="0.25">{img(HERO, lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Independent claim appraisal · All 82 counties</p>
<h1>{K}: a fair number for your storm, water or fire claim</h1>
<p class="lede">When the carrier accepts your claim but the check won’t cover the repair, {K} builds an independent, line-by-line valuation and takes it through the appraisal process written into your policy.</p>
<div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="#services">See how we help {ic("arrow")}</a></div>
<ul class="hero-ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Wind, hail, hurricane &amp; tree claims</li><li>{ic("check")}Homes, HOAs &amp; businesses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="strip" aria-label="At a glance"><div class="wrap strip-in">
<div class="stat"><b data-count="82">82</b><span>Mississippi counties served</span></div>
<div class="stat"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="stat"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim calculators</span></div>
<div class="stat"><b>2 of 3</b><span>Signatures set a binding award</span></div>
</div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-copy rv">
<p class="kicker kicker-red">The short version</p>
<h2>Covered isn’t the same as paid in full</h2>
<p>Most underpaid Mississippi claims aren’t denied. They’re short: a roof slope left off, decking nobody priced, a floor that can’t be matched, a code upgrade the estimate skipped. {K} exists for the space between “covered” and “paid in full.”</p>
<p>We work on one question — the amount of loss. As your {K}, we inspect the property ourselves, write our own estimate and defend it in front of the carrier’s appraiser and, when needed, a neutral umpire.</p>
<ul class="ticks"><li>{ic("check")}<span><b>Our own measurements.</b> Never a marked-up copy of the carrier’s estimate.</span></li>
<li>{ic("check")}<span><b>Numbers that hold up.</b> Priced to survive an umpire’s review, not to impress on day one.</span></li>
<li>{ic("check")}<span><b>Straight answers.</b> If your claim needs an attorney or a supplement instead, we say so on the first call.</span></li></ul>
<a class="btn btn-red" href="{P_ABOUT}">How we work {ic("arrow")}</a>
</div>
<figure class="duo-img rv">{img(P("roof-inspector", "roof-shingles"), sizes="(max-width:900px) 100vw, 46vw")}<figcaption><b>Fit check</b><span>Appraisal works when coverage is accepted and the dispute is about price or scope.</span></figcaption></figure>
</div></section>

<section class="sec sec-cream" id="services"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Services</p><h2>Where {K} steps in</h2><p>Twelve services built around a single job: a valuation of your loss that holds up. Start with a review of the carrier’s estimate, or bring us in once appraisal has been demanded.</p></div>
<div class="cards cards-3" data-stagger>{svc_cards}</div>
<p class="center"><a class="btn btn-line" href="{SVC_BASE}">All twelve services {ic("arrow")}</a></p>
</div></section>

<section class="sec sec-ink"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Claim climates</p><h2>Six regions, six kinds of claims</h2><p>Surge on the Coast, falling pines in the Pine Belt, ice in the hill country, tornadoes across the Delta. A {K} has to know how each region’s weather shows up on a roof — and in an estimate.</p></div>
<div class="regions" data-stagger>{region_cards}</div>
</div></section>

<section class="sec"><div class="wrap duo duo-rev">
<div class="duo-copy rv">
<p class="kicker kicker-red">Quick check</p>
<h2>Is your gap big enough for appraisal?</h2>
<p>Type in the two numbers you already have. If the difference is large, a conversation with a {K} makes sense. If it’s small, a documented supplement request may close it faster and for less.</p>
<p>The full <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a> adds appraiser and umpire fees and shows your break-even point. Coastal owners should also try the <a href="{TOOL_BASE}wind-water-split-estimator/">wind vs. water split estimator</a>.</p>
</div>
<div class="rv">{PAYOFF_MINI}</div>
</div></section>

<section class="sec sec-cream"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Process</p><h2>From first call to signed award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. Here’s how {K} moves a file through it.</p></div>
<ol class="steps" data-steps><span class="steps-line" aria-hidden="true"><span></span></span>{proc}</ol>
<p class="center"><a class="link" href="{P_PROCESS}">Read the full appraisal roadmap</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Free &amp; private</p><h2>Claim calculators from {K}</h2><p>Run the numbers before you pick up the phone. Every calculator works in your browser — nothing is stored or sent.</p></div>
<div class="cards cards-4" data-stagger>{tool_cards}</div>
</div></section>

<section class="pcta"><div class="pcta-bg" data-parallax="0.2">{img(P("storm-clouds", "lightning"), alt="")}</div>
<div class="wrap pcta-in rv"><p class="kicker">Before you sign off</p><h2>The best time to question a settlement is before you accept it</h2><p>A short review from {K} now can keep you from closing out a claim that won’t cover the repair.</p><div class="btns"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="#contact">Send your estimate</a></div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and fees — and {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="tbl rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col" class="hl">{K}</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Handle and negotiate the claim</td><td>Legal disputes and lawsuits</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, number disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Outcome</th><td class="hl">Award signed by two of three</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Decides coverage?</th><td class="hl">No</td><td>No</td><td>Argues it in court</td></tr>
</tbody></table></div>
</div></section>

<section class="sec sec-cream"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Statewide</p><h2>{K} in your city</h2><p>We serve every county in the state. These are the places where {K} handles claims most often — each page covers local neighborhoods, storm history and housing.</p></div>
<ul class="city-list" data-stagger>{city_links}</ul>
<p class="center"><a class="link" href="{LOC_BASE}">All counties and cities</a></p>
</div></section>

<section class="sec"><div class="wrap duo duo-top">
<div class="duo-copy rv"><p class="kicker kicker-red">FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btns"><a class="btn btn-red" href="{P_FAQ}">More answers {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Claim terms</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sec-cream"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-red">Claim advice</p><h2>Read this before you demand appraisal</h2><p>Practical guides from the {K} team on Coast deductibles, tornado documentation, policy language and estimates.</p></div>
<div class="cards cards-3" data-stagger>{post_cards}</div>
<p class="center"><a class="link" href="{POST_BASE}">All claim advice</a></p>
</div></section>

<section class="sec sec-ink" id="contact"><div class="wrap duo duo-top">
<div class="duo-copy rv"><p class="kicker">Start here</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="contact-list"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>{HOURS}</b></span></li><li>{ic("pin")}<span><small>Coverage</small><b>All 82 Mississippi counties</b></span></li></ul></div>
<div class="rv">{lead_form(page="/ (contact section)", fid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Review",
                        "Mississippi Insurance Appraiser: independent appraisal for underpaid hurricane, tornado, hail, tree, water and fire claims in all 82 counties.",
                        body, [faq_schema(home_faqs)], photo=HERO, body_cls="has-hero"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        ph = SVC_PHOTO[s["slug"]]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        cities = [LOCATIONS[(idx * 5 + k) % len(LOCATIONS)] for k in range(4)]
        article = s["body"] + f"""
<h2>Available across Mississippi</h2>
<p>{e(s["name"])} is available statewide. Inspections are scheduled around your timeline in places such as {", ".join(f'<a href="{loc_path(c)}">{e(c["city"])}</a>' for c in cities)}.</p>
<h2>{e(s["name"])} questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related_cards([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}"""
        side = call_box() + link_box("All services", items, path) + link_box("Helpful calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(article, side) + band()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]),
                  {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                   "areaServed": {"@type": "State", "name": "Mississippi"}, "url": DOMAIN + path, "image": photo_url(ph)}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="card card-row rv" href="{SVC_BASE}{s["slug"]}/"><span class="card-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, 280px", alt="")}</span>'
        f'<span class="card-b"><small class="meta">{i + 1:02d}</small><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Details {ic("arrow")}</span></span></a>' for i, s in enumerate(SERVICES))
    side = call_box() + link_box("Start with a calculator", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
    intro = f"""<p>Every {BRAND} service is built around an accurate, defensible valuation of your loss. Most files start with a <a href="{SVC_BASE}carrier-estimate-review/">carrier estimate review</a>; some come to us after appraisal has already been demanded.</p>
<div class="cards cards-list" data-stagger>{cards}</div>
<h2>Which service fits your claim?</h2>
{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients begin with an estimate review and decide later whether to demand appraisal."),
            ("Do you handle commercial and HOA claims?", "Yes — retail, office, warehouses, churches, apartments, condominiums and HOA common property, as well as single-family homes."),
            ("Do you only work hurricane claims?", "No. We handle tornado, hail, straight-line wind, fallen tree, ice and freeze, water, fire and smoke claims across the state.")])}"""
    body = page_hero(trail, "What we do", "Insurance Appraisal Services for Mississippi Claims",
                     f"From a single estimate review to full panel representation and neutral umpire work — twelve ways {BRAND} helps when a covered claim comes up short.", P("roof-inspector", "contractor", "clipboard")) + layout(intro, side) + band()
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Mississippi | 12 Ways",
                             "Insurance appraisal services in Mississippi for hurricane, tornado, hail, tree, ice, water and fire claims, plus estimate review and umpires.",
                             body, schema, photo=P("roof-inspector", "contractor", "clipboard")), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(f'{l["city"]}, MS', loc_path(l)) for l in LOCATIONS]
    for idx, l in enumerate(LOCATIONS):
        path = loc_path(l)
        trail = [("Home", "/"), ("Counties & cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        storms = "".join(f"<li><b>{e(w)}</b><span>{e(t)}</span></li>" for w, t in l["storms"])
        glance = f"""<div class="glance">
<div><p class="glance-h">Neighborhoods &amp; areas</p><ul class="chips">{"".join(f"<li>{e(n)}</li>" for n in l["neighborhoods"])}</ul></div>
<div><p class="glance-h">Housing mix</p><p>{e(l["housing"])}</p></div>
<div><p class="glance-h">Storm history</p><ul class="storm-list">{storms}</ul></div>
<div><p class="glance-h">Local claim risks</p><ul class="chips chips-red">{"".join(f"<li>{e(p)}</li>" for p in l["perils"])}</ul></div>
</div>"""
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES if s["slug"] in (
            "appraisal-demand-representation", "home-insurance-appraisal", "commercial-hoa-appraisal", "roof-hail-claim-appraisal", "carrier-estimate-review",
            "hurricane-named-storm-appraisal" if l["region"] == "Gulf Coast" else "tornado-wind-damage-appraisal"))
        near = related_cards([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        article = glance + l["body"] + f"""
<h2>Appraisal services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2>{near}"""
        side = call_box() + link_box("Mississippi cities", items, path) + link_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in (TOOLS[6], TOOLS[0], TOOLS[3])])
        body = page_hero(trail, l["region"], l["h1"], e(l["lede"]), ph, [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(article, side) + \
            band(f"Disputed claim in {l['city']}?", "Send us the carrier’s estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]),
                  {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Mississippi", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"},
                   "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": f'{l["county"]}, Mississippi'}}, "url": DOMAIN + path, "image": photo_url(ph)}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Counties & cities", LOC_BASE)]
    cities = "".join(f'<li class="rv"><a href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])} · {e(l["region"])}</small>{ic("arrow")}</a></li>' for l in LOCATIONS)
    regions = "".join(
        f'<article class="region rv"><div class="region-img">{img(ph, sizes="(max-width:640px) 100vw, 360px", alt="")}<span class="region-tag">{e(sub)}</span></div>'
        f'<div class="region-b"><h2>{e(n)}</h2><p>{e(t)}</p><p class="region-cities">{e(c)}</p></div></article>' for n, sub, _p, t, c, ph in REGIONS)
    article = f"""<p>{BRAND} works in every one of Mississippi’s 82 counties. These twelve city pages cover the places we’re called most often, with local neighborhoods, storm history and housing notes.</p>
<ul class="city-list city-list-2" data-stagger>{cities}</ul>
<h2>How claims differ by region</h2>
<p>The same policy wording plays out very differently on a raised house in Pass Christian, a 1960s ranch in Pearl and a Victorian in Columbus.</p>
<div class="regions regions-2" data-stagger>{regions}</div>"""
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 82 Mississippi Counties",
                     f"From DeSoto County to Hancock County, {BRAND} inspects on site. Start with your city, or call if yours isn’t listed — we cover the whole state.", P("mississippi-river")) + \
        layout(article, call_box() + link_box("Resources", RES_LINKS)) + band("Don’t see your town?", "We cover every Mississippi county. Call and tell us where the property is.")
    write(LOC_BASE, document(LOC_BASE, "Mississippi Counties & Cities We Serve | Claim Appraisal",
                             "Insurance claim appraisal in all 82 Mississippi counties, with local pages for Jackson, Gulfport, Biloxi, Hattiesburg, Tupelo, Oxford and more.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo=P("mississippi-river")), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        ph = TOOL_PHOTO[t["slug"]]
        others = related_cards([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]])
        article = t["explain"] + f"<h2>About this {t['kind'].lower()}</h2>{faq_block(t['faqs'])}<h2>More free calculators</h2>{others}"
        body = (page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False)
                + f'<section class="tool-sec"><div class="wrap">{t["markup"]}<p class="hint tool-note">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>'
                + layout(article, call_box() + link_box("All calculators", items, path)) + band("Want a professional to check the numbers?", "Send the carrier’s estimate and we’ll review it line by line."))
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]),
                  {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
                   "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    cards = "".join(
        f'<a class="card card-tool rv" href="{TOOL_BASE}{t["slug"]}/"><span class="card-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}<span class="card-kind">{t["kind"]}</span></span>'
        f'<span class="card-b"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open {ic("arrow")}</span></span></a>' for t in TOOLS)
    order = f"""<h2>A sensible order</h2><ol>
<li>Protect your dates with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a>.</li>
<li>Check roof math with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>.</li>
<li>On the Coast, test the <a href="{TOOL_BASE}wind-water-split-estimator/">wind vs. water split</a> and your <a href="{TOOL_BASE}named-storm-deductible-calculator/">named-storm deductible</a>.</li>
<li>See how payments split with the <a href="{TOOL_BASE}holdback-recovery-calculator/">holdback recovery calculator</a>.</li>
<li>Size the dispute with the <a href="{TOOL_BASE}appraisal-payoff-estimator/">appraisal payoff estimator</a>, then finish with the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol>"""
    body = (page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Mississippi Owners",
                      "Seven calculators and planners built from real appraisal questions. Check the carrier’s math, plan your deadlines and decide your next step — no sign-up, nothing stored.", P("calculator"), cta=False)
            + f'<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>'
            + layout(order, call_box()) + band())
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators | Mississippi Owners",
                              "Free insurance claim calculators for Mississippi: appraisal payoff, holdback, roof squares, hurricane deductible, wind vs. flood and deadlines.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo=P("calculator")), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal roadmap", path)]
    steps = "".join(f'<section class="road-step"><h2><span>{i + 1}</span>{e(n)}</h2>{h}</section>' for i, (n, h) in enumerate(PROCESS_STEPS))
    article = PROCESS_INTRO + f'<div class="road">{steps}</div><h2>Roadmap questions</h2>{faq_block(PROCESS_FAQS)}'
    body = page_hero(trail, "Process guide", "The Mississippi Insurance Appraisal Roadmap",
                     f"{len(PROCESS_STEPS)} stages, from the first disagreement to payment after the award — what happens, who does what, and where files go wrong.", P("clipboard", "consultation"),
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Award", "Any 2 of 3 sign")]) + \
        layout(article, call_box() + link_box("Resources", RES_LINKS, path)) + band()
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Mississippi", "description": "The stages of a property insurance appraisal under a typical policy appraisal clause.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (n, _h) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in Mississippi | Roadmap",
                         "The insurance appraisal process in Mississippi, step by step: the written demand, appraisers, umpire, inspections, the award and payment.",
                         body.replace('<section class="road-step"><h2><span>', '<section class="road-step"><h2><span>', 1), [crumbs_schema(trail), faq_schema(PROCESS_FAQS), howto], photo=P("clipboard", "consultation")), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Questions answered", path)]
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Mississippi Insurance Appraisal Questions, Answered",
                     "Plain answers about how appraisal works, what it costs, deadlines, the Coast’s wind-and-flood questions and working with us.", P("porch-home", "consultation")) + \
        layout(f'<nav class="toc" aria-label="FAQ topics"><p class="glance-h">Jump to a topic</p><ul>{toc}</ul></nav>{groups}', call_box() + link_box("Resources", RES_LINKS, path)) + \
        band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")
    write(path, document(path, "Insurance Appraisal FAQ | Mississippi Costs & Timing",
                         "Insurance appraisal FAQ for Mississippi owners: how it works, costs, deadlines, MWUA and wind vs. flood questions, and binding awards.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo=P("porch-home", "consultation")), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Insurance claim terms", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#t-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="t-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    article = (f'<div class="gloss-tools"><label for="gloss-q">Search {len(GLOSSARY)} terms</label><input id="gloss-q" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off">'
               f'<p class="hint" data-gloss-count aria-live="polite">{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="gloss">{dl}</dl>')
    body = page_hero(trail, "Reference", "Insurance Claim Terms, Defined in Plain English",
                     f"{len(GLOSSARY)} words you’ll meet in Mississippi policies, estimates and appraisal awards — searchable, in plain English.", P("calculator", "estimate-laptop"), cta=False) + \
        layout(article, call_box() + link_box("Resources", RES_LINKS, path))
    dts = {"@type": "DefinedTermSet", "name": "Insurance claim terms", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV, Umpire & More",
                         "A searchable insurance claim terms glossary: actual cash value, holdback, named-storm deductible, MWUA, umpire and 40+ more terms.",
                         body, [crumbs_schema(trail), dts], photo=P("calculator", "estimate-laptop")), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Claim advice", POST_BASE), (p["title"], path)]
        ph = POST_PHOTO[p["slug"]]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        others = related_cards([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]])
        article = f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {p["read"]} read</p>' + p["body"] + f"<h2>Keep reading</h2>{others}"
        body = page_hero(trail, f"Claim advice · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + \
            layout(article, call_box() + link_box("Resources", RES_LINKS) + link_box("Free calculators", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])) + band()
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": photo_url(ph), "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Claim advice", path)]
    cards = "".join(
        f'<article class="card post rv"><a class="card-img" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}</a>'
        f'<div class="card-b"><small class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</small><h2><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    items = [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]
    body = page_hero(trail, "Guides", "Mississippi Insurance Claim Advice and Guides",
                     "Practical guides on Coast deductibles, wind vs. water, tornado and ice-storm documentation, policy language and reading an estimate.", P("hurricane-debris"), cta=False) + \
        f'<section class="sec"><div class="wrap"><div class="cards cards-3" data-stagger>{cards}</div></div></section>' + band()
    write(path, document(path, "Insurance Claim Advice for Mississippi Property Owners",
                         "Insurance claim advice for Mississippi owners: wind vs. water, Coast hurricane deductibles, tornado and ice-storm claims, and estimates.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo=P("hurricane-debris", "hurricane-damage")), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("Who we are", path)]
    article = f"""
<figure class="fig">{img(P("consultation"), sizes="(max-width:1020px) 100vw, 720px")}</figure>
<h2>One question, done carefully</h2>
<p>Plenty of claim professionals do a little of everything. {BRAND} chose to specialize in the amount of loss — what the covered damage actually costs to repair or replace. Our process, calculators and documentation habits are built around answering that one question well, whether we’re your appointed appraiser, reviewing an estimate before a dispute escalates, or sitting as a neutral umpire.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first, numbers second.</strong> We inspect and measure before looking at anyone else’s estimate.</li>
<li><strong>Defensible beats impressive.</strong> An inflated estimate loses credibility with the umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney, a public adjuster or simply a supplement, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who calls us</h2>
<p>Homeowners, landlords, condo owners, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Mississippi. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<div class="callout"><b class="callout-t">What we are not</b><p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. And we don’t promise outcomes — no honest appraiser can.</p></div>
<h2>Statewide on purpose</h2>
<p>Mississippi’s weather changes a lot over 340 miles. Working all 82 counties means we see every kind of loss the state produces — surge and wind on the Coast, falling pines in the Pine Belt, tornadoes across the Delta, ice in the hill country — and price each with local knowledge.</p>"""
    body = page_hero(trail, "About us", f"Who We Are at {BRAND}",
                     "Estimators and appraisers who believe a covered claim should be paid on what the damage really costs — documented clearly enough that everyone at the table can see it.", P("roof-inspector", "clipboard")) + \
        layout(article, call_box() + link_box("Explore", [("Our services", SVC_BASE), ("Counties & cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal roadmap", P_PROCESS)])) + band()
    write(path, document(path, f"About {BRAND} | Who We Are",
                         "Who we are: Mississippi Insurance Appraiser is an independent appraisal and estimating practice focused on the amount of loss in claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo=P("roof-inspector", "clipboard")), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Talk to an appraiser", path)]
    body = page_hero(trail, "Get in touch", f"Talk to {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", P("consultation"), cta=False) + f"""
<section class="sec sec-ink"><div class="wrap duo duo-top">
<div class="duo-copy rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="contact-list"><li>{ic("phone")}<span><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></span></li><li>{ic("mail")}<span><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li><li>{ic("clock")}<span><small>Hours</small><b>{HOURS}</b></span></li><li>{ic("pin")}<span><small>Service area</small><b>All 82 Mississippi counties</b></span></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks ticks-light"><li>{ic("check")}<span>Declarations page (and MWUA declarations on the Coast)</span></li><li>{ic("check")}<span>The carrier’s full estimate as a PDF</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and your contractor’s estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, fid="k")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | (844) 537-1427",
                         "Contact Mississippi Insurance Appraiser for a free review of a disputed claim. Call or text (844) 537-1427, or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo=P("consultation")), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = [
        (P_PRIV, "Privacy Notice", f"Privacy Notice | {BRAND}",
         "Our privacy notice explains what Mississippi Insurance Appraiser collects through forms, calls and email, how it’s used and your choices.",
         "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect what you choose to give us — such as your name, phone number, email address, property location and details about your claim. Our web server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our website and email, or when the law requires it.</p>
<h2>Calculators</h2><p>Our calculators and checklists run in your browser. Numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics later, this notice will be updated.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        (P_TERMS, "Website Terms", f"Website Terms of Use | {BRAND}",
         "Website terms of use for Mississippi Insurance Appraiser: no client relationship from browsing, no legal advice and limits on calculators.",
         "The terms that apply when you use this website and its calculators.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. Its content is general information about insurance appraisal and property claims in Mississippi.</p>
<h2>No client relationship</h2><p>Reading this site, using a calculator or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a Mississippi attorney about legal questions.</p>
<h2>Calculators and examples</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any claim outcome. Example figures on this site are illustrative.</p>
<h2>Content and photos</h2><p>Site text, design and calculators belong to {BRAND}. You may share links and print pages for personal use. Photographs are royalty-free public-domain or CC0 images used for illustration; they don’t show our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or calculators.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Mississippi.</p>"""),
        (P_DISC, "Legal Disclaimer", f"Legal Disclaimer | {BRAND}",
         "The legal disclaimer for Mississippi Insurance Appraiser: general information only, not legal advice, not a public adjuster, no guarantees.",
         "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy, its endorsements and — on the Coast — any separate wind or flood policy.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is approaching, consult a Mississippi attorney promptly.</p>
<h2>Weather, law and agency references</h2><p>References to storms, statutes or agencies are for context and may change. Check current rules with official sources such as the Mississippi Insurance Department.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t depict our clients’ properties.</p>"""),
    ]
    for path, h1, title, desc, lede, content in legal:
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, P("commercial-building", "calculator"), cta=False) + layout(f'<div class="narrow">{content}</div>', call_box())
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo=P("commercial-building", "calculator")), 0.3)


def directory_and_404():
    path = P_MAP
    trail = [("Home", "/"), ("Page directory", path)]
    groups = [
        ("Main", [("Home", "/"), ("Who we are", P_ABOUT), ("Talk to an appraiser", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Counties & cities", [("All counties & cities", LOC_BASE)] + [(f'{l["city"]}, MS', loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", RES_LINKS + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy notice", P_PRIV), ("Website terms", P_TERMS), ("Legal disclaimer", P_DISC)]),
    ]
    cols = "".join(f'<div class="dir-col"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Page Directory", f"Every page on {BRAND}, in one place.", P("commercial-building", "calculator"), cta=False) + \
        f'<section class="sec"><div class="wrap dir">{cols}</div></section>'
    write(path, document(path, f"Page Directory | {BRAND}",
                         "The page directory lists every Mississippi Insurance Appraiser page: services, counties and cities, free calculators, guides and legal pages.",
                         body, [crumbs_schema(trail)], photo=P("commercial-building", "calculator")), 0.3)

    body = (f'<section class="phero phero-404"><div class="phero-bg">{img(P("storm-clouds"), lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p>'
            f'<h1>That page washed out</h1><p class="lede">The page you’re looking for has moved or never existed. These will get you back on track.</p>'
            f'<div class="btns"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-ghost" href="{SVC_BASE}">Services</a><a class="btn btn-ghost" href="{TOOL_BASE}">Calculators</a><a class="btn btn-ghost" href="{P_CONTACT}">Contact</a></div></div></section>')
    write("/404.html", document("/404.html", f"Page Not Found (404) | {BRAND}",
                                "This page could not be found on Mississippi Insurance Appraiser. Use the links here to reach our services, calculators or contact page.",
                                body, robots="noindex,follow"), sitemap=False)


# ---------------------------------------------------------------- root files
GUARD_PHP = r"""<?php
// Mississippi Insurance Appraiser - canonical host guard. Required by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'mississippiinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$mia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
$mia_path  = strtok($mia_uri, '?');
$mia_qs    = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
// /dir/index.php (and /index.php) are duplicate URLs of /dir/.
$mia_clean = preg_match('#^(.*/)index\.php$#', $mia_path, $mia_m) ? $mia_m[1] : null;
// 301 www. and plain http to https://mississippiinsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . ($mia_clean ?? $mia_path) . $mia_qs, true, 301);
    exit;
}
if ($mia_clean !== null) {
    header('Location: ' . $mia_clean . $mia_qs, true, 301);
    exit;
}
// Keep preview/temporary domains out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Mississippi Insurance Appraiser - front controller for the static build.
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
        ".htaccess": "DirectoryIndex index.php\nErrorDocument 404 /404.html\nOptions -Indexes\n",
    }
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(text)
    # Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private", "*.md"))
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    directory_and_404()
    root_files()
    stray = [os.path.join(dp, f) for dp, _, fs in os.walk(OUT) for f in fs if f == "index.html"]
    assert not stray, f"dir/index.html must never be generated: {stray}"
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
