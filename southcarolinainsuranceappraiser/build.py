#!/usr/bin/env python3
"""Static site generator for southcarolinainsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php whose first line requires the
canonical-host guard (_guard.php); the homepage is home.html served by the root index.php.
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
from learn import PROCESS_INTRO, PROCESS_STEPS, PROCESS_AFTER, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "South Carolina Insurance Appraiser"
HOST = "southcarolinainsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

SVC_BASE = "/claim-dispute-services/"
LOC_BASE = "/locations-served/"
TOOL_BASE = "/free-claim-tools/"
POST_BASE = "/appraisal-guides/"
ABOUT, CONTACT = "/about-the-firm/", "/contact-an-appraiser/"
PROCESS, FAQ_P, GLOSS = "/appraisal-process-explained/", "/insurance-appraisal-faq/", "/appraisal-glossary/"
PRIVACY, TERMS, DISC, CREDITS, SITEIDX = "/privacy/", "/terms/", "/legal-disclaimer/", "/photo-credits/", "/site-index/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consultation", "home-insurance-appraisal": "suburb-home", "commercial-hoa-appraisal": "condo-building", "roof-hail-damage-appraisal": "roof-damage", "wind-tornado-claim-appraisal": "tornado-damage", "hurricane-claim-appraisal": "hurricane-damage", "water-damage-claim-appraisal": "eave-damage", "fire-smoke-damage-appraisal": "house-fire", "tree-fall-ice-storm-appraisal": "tree-crew", "earthquake-claim-appraisal": "charleston-masonry", "claim-estimate-review": "laptop-review", "umpire-neutral-appraiser": "paperwork",
}
LOC_PHOTO = {
    "charleston": "charleston-houses", "columbia": "flood-street", "greenville": "storm-clouds", "myrtle-beach": "myrtle-beach", "spartanburg": "suburb-home", "mount-pleasant": "harbor-bridge", "summerville": "live-oak", "rock-hill": "modern-home", "hilton-head-island": "hilton-head", "florence": "river-flood", "beaufort": "beaufort", "aiken": "ice-storm",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator", "rcv-acv-holdback-calculator": "kitchen", "roof-area-pitch-estimator": "roof-aerial", "hurricane-deductible-calculator": "coastal-aerial", "claim-timeline-builder": "paperwork", "appraisal-readiness-checkup": "consultation-2", "wind-flood-damage-splitter": "flood-street",
}
POST_PHOTO = {
    "hurricane-deductibles-explained": "coastal-aerial", "when-a-tree-falls-on-your-house": "tree-crew", "wind-pool-claims-and-appraisal": "ocean-storm", "appraisal-versus-lawsuit": "consultation-2", "storm-damage-photo-checklist": "hail", "how-umpires-decide-line-items": "laptop-review",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>'


def mark(uid="m"):
    """Logo mark: a copper roofline over an equals sign — a fair valuation of the home."""
    return (f'<svg viewBox="0 0 48 48" width="42" height="42" aria-hidden="true"><defs><linearGradient id="{uid}" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#1f4f93"/><stop offset="1" stop-color="#0a1f3f"/></linearGradient></defs>'
            f'<rect width="48" height="48" rx="10" fill="url(#{uid})"/>'
            '<path d="M10 22.5L24 11l14 11.5" fill="none" stroke="#e09a5f" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M15.5 28h17M15.5 35h17" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "SC", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-SC", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 46 South Carolina counties.",
        "areaServed": [{"@type": "State", "name": "South Carolina"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hurricane claims", "Wind and flood causation", "Xactimate estimating", "Umpire services"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All claim dispute services", SVC_BASE), True),
        ("Locations", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All locations served", LOC_BASE), True),
        ("Free Tools", [(t["name"], tool_path(t)) for t in TOOLS], ("All free claim tools", TOOL_BASE), False),
        ("Resources", [("Appraisal process explained", PROCESS), ("Insurance appraisal FAQ", FAQ_P), ("Appraisal glossary", GLOSS), ("Appraisal guides", POST_BASE)], None, False),
    ]


def brand_link(uid):
    return f'<a class="brand" href="/" aria-label="{BRAND} home">{mark(uid)}<span><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="mega{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><strong>{e(allk[0])} →</strong></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="head"><div class="wrap">
{brand_link("mh")}
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn cu head-cta" href="tel:{TEL}">{ic("phone")} {PHONE}</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand_link("md")}<button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn cu" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 46 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:7])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div>{brand_link("mf")}
<p style="margin-top:18px">Independent appraisal and estimating for property owners whose insurance claims came up short — from the Blue Ridge foothills to the Sea Islands.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET</span></div></div>
<div><h2 class="foot-t">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-t">Locations</h2><ul>{loc}<li><a href="{LOC_BASE}">All locations</a></li></ul></div>
<div><h2 class="foot-t">Free tools</h2><ul>{tl}</ul></div>
<div><h2 class="foot-t">Firm</h2><ul><li><a href="{ABOUT}">About the firm</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Guides</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="foot-legal"><span>© {date.today().year} {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISC}">Disclaimer</a></li><li><a href="{CREDITS}">Photo credits</a></li><li><a href="{SITEIDX}">Site index</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general information; your policy’s wording controls and no result is guaranteed.</p>
</div></footer>
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
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-home", body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra.append(n)
    p = PHOTOS[photo]
    primary = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": p["fw"], "height": p["fh"], "caption": p["alt"]}
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY, "primaryImageOfPage": {"@id": primary["@id"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for t in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "FAQPage", "ItemList") for n in extra if n.get("@type") == t]
    webpage["mainEntity"] = {"@id": mains[0] if mains else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema()]
    if not robots.startswith("noindex"):
        graph += [webpage, primary]
    graph += extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    og_img_alt = f"{BRAND} — independent property claim appraisal across South Carolina"
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_img_alt}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{og_img_alt}">
<meta name="geo.region" content="US-SC">
<meta name="geo.placename" content="South Carolina">
<meta name="theme-color" content="#0a1f3f">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, /assets/img/photos/{photo}.webp {p["fw"]}w" imagesizes="100vw">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body{f' class="{body_cls}"' if body_cls else ""}>
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
    """Homepage -> home.html; everything else -> dir/index.php starting with the canonical-host guard."""
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
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row"><a class="btn cu" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ol" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=' data-parallax="0.1"')}<div class="wrap">{crumbs(trail)}<p class="kicker lt">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(html.unescape(q))}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box call"><h2 class="box-t">Talk it through first</h2><p>A free first conversation. We’ll tell you honestly whether appraisal fits your claim.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn cu" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span>›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_photo(h, p, photo="storm-clouds"):
    return f"""<section class="cta-photo">{img(photo, "bg", alt="", extra=' data-parallax="0.15"')}<div class="wrap rv"><p class="kicker lt" style="justify-content:center">Free first review</p><h2>{e(h)}</h2><p>{e(p)}</p><div class="btn-row"><a class="btn cu" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ol" href="{CONTACT}">Email the estimate</a></div></div></section>"""


def card(href, photo, title, text, num=None, go="Learn more", meta=None, hl="h3"):
    n = f'<span class="num">{num}</span>' if num else ""
    m = f'<span class="meta">{e(meta)}</span>' if meta else ""
    return f'<a class="card rv" href="{href}"><span class="ph">{img(photo, sizes="(max-width:640px) 100vw, (max-width:960px) 50vw, 380px", alt="")}{n}</span><span class="cb">{m}<{hl}>{e(title)}</{hl}><p>{e(text)}</p><span class="go">{e(go)}</span></span></a>'


LOSSES = ["Hurricane / tropical storm", "Wind / tornado", "Hail", "Tree fall / ice", "Water / leak", "Fire / smoke", "Earthquake (endorsed)", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send us your claim details", sub="Free review, no obligation. We usually reply within one business day.", page="/", hid="f"):
    roles = ["Homeowner", "Condo owner", "Commercial owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in South Carolina"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h3>{e(heading)}</h3><p class="sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{hid}-amt">Approx. amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">What happened, and where does the claim stand?</label><textarea id="{hid}-det" name="details" placeholder="Date of loss, what the carrier paid or offered, and what you believe was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="lead-card" action="/api/contact.php" method="post" data-lead novalidate>
<h2>Free claim review</h2><p class="sub">A few details and we’ll call you back, usually within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy policy</a>.</span></label>
<button class="btn cu" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="fine">{ic("lock")} No obligation. Your details stay private.</p>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Lowcountry", "Charleston · Beaufort · Hilton Head", ["Hurricanes", "Surge vs. wind", "Live oaks", "Historic review"],
     "Hugo, Matthew, Irma and Ian all left their mark here. Elevated homes, single houses with piazzas and wind-pool policies make for layered claims.", "charleston-houses"),
    ("Upstate", "Greenville · Spartanburg · Anderson", ["Tree fall", "Hail", "Ice storms", "Tornadoes"],
     "Helene in 2024 showed how far inland a hurricane can reach. Spring hail and winter ice keep roofers busy across the foothills.", "storm-clouds"),
    ("Midlands", "Columbia · Lexington · Aiken", ["Flooding", "Severe storms", "Ice", "Tree damage"],
     "The 2015 flood and the 2014 ice storm are still the reference points for water and tree claims around the capital and Aiken County.", "flood-street"),
    ("Grand Strand", "Myrtle Beach · Conway · Georgetown", ["Named storms", "Condo towers", "River flooding"],
     "High-rise condos, vacation rentals and Florence-era river flooding put master policies and flood coverage at the center of disputes.", "myrtle-beach"),
    ("Pee Dee", "Florence · Darlington · Dillon", ["Inland flooding", "Tornadoes", "Farm buildings"],
     "Rivers rise for days after a coastal storm. Homes, farm outbuildings and small commercial buildings often share one claim.", "river-flood"),
]

STORMS = [
    ("1954", "Hurricane Hazel", "Struck the Grand Strand in October, reshaping beachfront building along Horry County."),
    ("1989", "Hurricane Hugo", "Category 4 landfall near Charleston, with damage reaching Sumter and the Midlands."),
    ("2015", "The October flood", "Record rain overwhelmed creeks and dams around Columbia and the Midlands."),
    ("2016", "Hurricane Matthew", "Landfall near McClellanville; huge tree losses on Hilton Head and in Beaufort County."),
    ("2018", "Hurricane Florence", "Record river flooding in the Pee Dee and Horry County for weeks after landfall."),
    ("2022", "Hurricane Ian", "Landfall near Georgetown, with wind and surge along the coast."),
    ("2024", "Hurricane Helene", "Destructive wind and tree fall across the Upstate and Aiken County, far from the coast."),
]

COUNTIES = ["Abbeville", "Aiken", "Allendale", "Anderson", "Bamberg", "Barnwell", "Beaufort", "Berkeley", "Calhoun", "Charleston", "Cherokee", "Chester", "Chesterfield", "Clarendon", "Colleton", "Darlington", "Dillon", "Dorchester", "Edgefield", "Fairfield", "Florence", "Georgetown", "Greenville", "Greenwood", "Hampton", "Horry", "Jasper", "Kershaw", "Lancaster", "Laurens", "Lee", "Lexington", "McCormick", "Marion", "Marlboro", "Newberry", "Oconee", "Orangeburg", "Pickens", "Richland", "Saluda", "Spartanburg", "Sumter", "Union", "Williamsburg", "York"]
assert len(COUNTIES) == 46


def home():
    K = BRAND
    svc_cards = "".join(card(svc_path(s), SVC_PHOTO[s["slug"]], s["name"], s["short"], num=f"{i + 1:02d}") for i, s in enumerate(SERVICES[:9]))
    marquee = "".join(f"<span>{c} County</span>" for c in COUNTIES * 2)
    regions = "".join(f'<div class="region rv">{img(ph, sizes="(max-width:640px) 100vw, 50vw", alt="")}<h3>{e(n)}</h3><p>{e(t)}</p><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in tags)}</ul></div>' for n, _c, tags, t, ph in REGIONS)
    steps = [
        ("Free review", "We read the policy, the carrier’s estimate and your photos, then tell you whether appraisal fits."),
        ("Our own scope", "We inspect, measure and build a line-item estimate priced for your South Carolina ZIP code."),
        ("Written demand", "Appraisal is demanded in writing and we are named as your appraiser on time."),
        ("Appraiser talks", "We work through the differences with the carrier’s appraiser, line by line."),
        ("Umpire if needed", "Items still open go to a neutral umpire with photos and pricing support."),
        ("Signed award", "Two of three signatures set the amount of loss and payment follows the policy."),
    ]
    proc = "".join(f'<div class="step rv"><span class="n">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, (t, p) in enumerate(steps))
    trows = "".join(f'<a class="trow rv" href="{tool_path(t)}"><span class="ph">{img(TOOL_PHOTO[t["slug"]], sizes="112px", alt="")}</span><span><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p></span></a>' for t in TOOLS[1:])
    cities = "".join(card(loc_path(l), LOC_PHOTO[l["slug"]], l["city"], l["county"], go="Local claims", hl="h3") for l in LOCATIONS[:8])
    more_cities = "".join(f'<a href="{loc_path(l)}"><span>{e(l["city"])}<small>{e(l["county"])}</small></span>{ic("arrow")}</a>' for l in LOCATIONS[8:])
    storms = "".join(f'<div class="storm rv"><b>{y}</b><h3>{e(n)}</h3><p>{e(t)}</p></div>' for y, n, t in STORMS)
    posts = "".join(card(post_path(p), POST_PHOTO[p["slug"]], p["title"], p["summary"], go="Read the guide", meta=f'{p["read"]} read') for p in POSTS[:3])
    home_faqs = [
        (f"What does a {K} do?", f"A {K} values the damage when you and your insurer agree the loss is covered but disagree on what it costs. As your appointed appraiser we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, when needed, present open items to a neutral umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works within the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("Can appraisal settle a wind-versus-flood argument?", "It can value the wind damage under the wind policy, but whether an item was caused by wind or water may be treated as a coverage question. Flood policies have their own rules. Good photos and water-line evidence matter most."),
        ("Is the award binding?", "On the amount of loss, generally yes, once any two of the three panel members sign. Coverage questions and legal claims sit outside appraisal."),
        ("What does it cost?", "Each side pays its own appraiser and usually half of the umpire. We put our fee in writing before any work begins, and the first conversation is free."),
        (f"Where does a {K} work?", f"Statewide — all 46 counties, with regular work in Charleston, Columbia, Greenville, Myrtle Beach, Hilton Head Island, Beaufort, Florence, Rock Hill and Aiken."),
    ]
    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.12"')}</div>
<div class="wrap">
<div>
<p class="kicker lt">Independent claim appraisal · All 46 counties</p>
<h1>{K} for claims that came up <em>short</em></h1>
<p class="lede">When the carrier accepts your claim but the check won’t cover the repair, {K} prices the loss from scratch and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn cu" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn ol" href="#services">See our services</a></div>
<ul class="ticks"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Line-item estimates by ZIP</li><li>{ic("check")}Homes, condos, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="ledger" aria-label="At a glance"><div class="wrap">
<div><b data-count="46">46</b><span>South Carolina counties served</span></div>
<div><b data-count="12">12</b><span>Appraisal &amp; estimating services</span></div>
<div><b data-count="7">7</b><span>Free claim tools</span></div>
<div><b>2 of 3</b><span>Signatures make an award</span></div>
</div></section>

<section class="sec"><div class="wrap two">
<div class="rv">
<p class="kicker">Why owners call</p>
<h2>When the check doesn’t match the damage, call a <em>{K}</em></h2>
<p>Most underpaid claims aren’t denied — they’re simply short. A slope left off the roof diagram, flooring that can’t be matched, a code upgrade nobody priced, a tree-removal line capped too low. {K} exists for that space between “covered” and “paid in full.”</p>
<p>We don’t edit the carrier’s estimate. We inspect, measure and write our own, then compare the two line by line so you can see exactly where the money went missing.</p>
<a class="more" href="{ABOUT}">How the firm works</a>
</div>
<div class="photo-stack rv">
<figure class="p1">{img("roof-work", sizes="(max-width:960px) 92vw, 540px")}</figure>
<figure class="p2">{img("paperwork", sizes="(max-width:960px) 44vw, 260px")}</figure>
<figcaption>Every number in our estimate is measured, photographed and priced for the ZIP code.</figcaption>
</div>
</div>
<div class="wrap"><div class="fitlist rv">
<div><h3><span>✓</span>Appraisal usually fits</h3><ul><li>Coverage accepted, price disputed</li><li>Repair-or-replace and matching arguments</li><li>Missing trades, code items or overhead and profit</li><li>Roof measurements and steep or high charges</li></ul></div>
<div><h3><span>✕</span>Usually not the right tool</h3><ul><li>A full denial of coverage</li><li>Bad-faith or other legal claims</li><li>A gap too small to justify the fees</li><li>A deadline that needs an attorney first</li></ul></div>
</div></div></section>

<section class="sec tint" id="services"><div class="wrap">
<div class="sec-head"><p class="kicker">Services</p><h2>What a {K} handles</h2><p>Twelve services built around one job: a valuation of your loss that stands up to the other side. Start with an estimate review, or bring us in once appraisal has been demanded.</p></div>
<div class="cards">{svc_cards}</div>
<p style="margin-top:36px"><a class="btn line" href="{SVC_BASE}">All twelve services {ic("arrow")}</a></p>
</div></section>

<div class="marquee" aria-label="All 46 South Carolina counties"><div class="marquee-track">{marquee}</div></div>

<section class="sec"><div class="wrap">
<div class="sec-head"><p class="kicker">Five claim climates</p><h2>One state, five ways storms show up on a roof</h2><p>A {K} has to read the damage differently in a Beaufort single house, a Greenville split-level and a Myrtle Beach condo tower. Here’s what we see most in each region.</p></div>
<div class="mosaic">{regions}</div>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head c"><p class="kicker">The process</p><h2>How appraisal moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result. This is how {K} takes a file from the first call to a signed award.</p></div>
<div class="steps">{proc}</div>
<p style="text-align:center;margin-top:44px"><a class="more" href="{PROCESS}">Read the full process guide</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><p class="kicker">Free &amp; private</p><h2>Free claim tools from {K}</h2><p>Check the math before you pick up the phone. Every tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="tool-split">
<div class="rv">{GAP_MINI}<p class="disclaim">Illustrative figures. The full <a href="{tool_path(TOOLS[0])}">claim gap &amp; fee estimator</a> adds appraiser and umpire fees so you can see a net number.</p></div>
<div class="tool-list">{trows}</div>
</div>
</div></section>

<section class="sec deep"><div class="wrap">
<div class="sec-head"><p class="kicker lt">Storm history</p><h2>The storms that shaped South Carolina claims</h2><p>Every adjuster and every {K} in the state measures new losses against these events. Scroll the timeline.</p></div>
<div class="storms" tabindex="0" aria-label="Storm timeline">{storms}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><p class="kicker">Locations</p><h2>{K} locations across the state</h2><p>We travel to every county. These are the communities where {K} handles claims most often, each with its own page of local detail.</p></div>
<div class="cards four">{cities}</div>
<div class="citylist">{more_cities}</div>
<p style="margin-top:30px"><a class="more" href="{LOC_BASE}">All locations served</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head c"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. {K} will tell you when someone else is the better call.</p></div>
<div class="roles">
<div class="role us rv"><h3>{K}</h3><dl><dt>Main job</dt><dd>Values the amount of loss</dd><dt>Best moment</dt><dd>Coverage accepted, number disputed</dd><dt>Outcome</dt><dd>Award signed by two of three</dd></dl></div>
<div class="role rv"><h3>Public adjuster</h3><dl><dt>Main job</dt><dd>Prepares and negotiates the claim</dd><dt>Best moment</dt><dd>Early, soon after the loss</dd><dt>Outcome</dt><dd>Negotiated settlement</dd></dl></div>
<div class="role rv"><h3>Attorney</h3><dl><dt>Main job</dt><dd>Legal rights, coverage and bad faith</dd><dt>Best moment</dt><dd>Denials and close deadlines</dd><dt>Outcome</dt><dd>Settlement or judgment</dd></dl></div>
</div>
</div></section>

<section class="sec"><div class="wrap two top">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask a {K}</h2><p>Short, straight answers. The full FAQ covers costs, timing and South Carolina specifics.</p><div class="btn-row" style="margin-top:22px"><a class="btn" href="{FAQ_P}">All FAQs {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head"><p class="kicker">Guides</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on hurricane deductibles, tree claims, wind-pool policies and documentation.</p></div>
<div class="cards">{posts}</div>
</div></section>

{cta_photo("The best time to check the numbers is before you accept them", "A short review now can keep you from signing off on a settlement that won’t pay for the repair.", "storm-clouds")}

<section class="sec deep" id="contact"><div class="wrap contact-grid">
<div class="rv"><p class="kicker lt">Start with a conversation</p><h2>Talk to a {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal makes sense — no pressure and no obligation.</p>
<ul class="lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Coverage</span><b>All 46 South Carolina counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", hid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Claim Appraisal",
                        "South Carolina Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid hurricane, wind, hail and water claims.",
                        body, [crumbs_schema([("Home", "/")]), faq_schema(home_faqs)], photo="hero-home", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for s in SERVICES:
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [x for x in SERVICES if x is not s]
        i = SERVICES.index(s)
        rel = [rel[(i + k) % len(rel)] for k in range(3)]
        related = "".join(f'<a href="{svc_path(r)}"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        locs = [(f'{l["city"]}, SC', loc_path(l)) for l in LOCATIONS[:6]]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Claim dispute service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Where we work", locs + [("All locations served", LOC_BASE)])}</aside></div>
{cta_photo("Have a claim that doesn’t add up?", "Send the carrier’s estimate. We’ll review it and tell you plainly what we see.", ph)}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "South Carolina"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(card(svc_path(s), SVC_PHOTO[s["slug"]], s["name"], s["short"], num=f"{i + 1:02d}", hl="h2") for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we do", "Insurance Claim Dispute Services in South Carolina",
                     f"Insurance claim dispute services built on one thing: an accurate, defensible valuation of the loss. Pick a single estimate review, full appraisal representation or neutral umpire work.", "contractor") + f"""
<section class="sec"><div class="wrap"><div class="cards">{cards}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="kicker">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and some disputes close right there with a documented supplement.</p><a class="btn" href="{svc_path(SVC_BY["claim-estimate-review"])}">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one stage?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you take commercial and HOA claims?", "Yes — condo associations, apartment communities, churches, retail and office buildings, as well as single-family homes."), ("Do you only handle hurricane claims?", "No. We also value hail, tornado, tree fall, water, fire and endorsed earthquake losses.")])}</div></div></section>
{cta_photo("Have a claim that doesn’t add up?", "Send the carrier’s estimate. We’ll review it and tell you plainly what we see.")}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Claim Dispute Services in South Carolina",
                             "Insurance claim dispute services in South Carolina: appraisal demands, estimate reviews, hurricane, hail, tree, water and fire claims, plus umpires.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo="contractor"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Locations", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        storms = "".join(f"<li>{e(x)}</li>" for x in l["storms"])
        hoods = ", ".join(l["neighborhoods"])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', l["h1"], l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local">
<div><h2>Local claim risks</h2><ul class="chips">{chips}</ul></div>
<div><h2>Housing mix</h2><p>{e(l["housing"])}</p></div>
<div><h2>Storm history</h2><ul>{storms}</ul></div>
<div><h2>Neighborhoods we cover</h2><p>{e(hoods)}</p></div>
</div>
{l["body"]}
<h2>Services in {e(l["city"])}</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding area, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby areas</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Locations served", items, path)}{list_box("Free claim tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]])}</aside></div>
{cta_photo(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.", ph)}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, SC", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "South Carolina"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Locations", LOC_BASE)]
    cards = "".join(card(loc_path(l), LOC_PHOTO[l["slug"]], l["city"], f'{l["county"]} · {l["region"]}', go="Local claim detail", hl="h2") for l in LOCATIONS)
    regs = "".join(f'<div class="region rv">{img(ph, sizes="(max-width:640px) 100vw, 50vw", alt="")}<h3>{e(n)}</h3><p>{e(c)} — {e(t)}</p></div>' for n, c, _t, t, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Locations Across South Carolina",
                     "Insurance appraisal locations from the Upstate to the Sea Islands. We inspect in all 46 counties; these pages cover the cities where we work most often.", "harbor-bridge") + f"""
<section class="sec"><div class="wrap"><div class="cards four">{cards}</div></div></section>
<section class="sec sand"><div class="wrap"><div class="sec-head"><p class="kicker">Regions</p><h2>How claims differ by region</h2><p>The same policy language plays out very differently on a Mount Pleasant marsh lot, a Columbia bungalow street and a Spartanburg mill village.</p></div><div class="mosaic">{regs}</div></div></section>
{cta_photo("Don’t see your town?", "We cover every South Carolina county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraisal Locations in South Carolina",
                             "Insurance appraisal locations in all 46 South Carolina counties, including Charleston, Columbia, Greenville, Myrtle Beach, Hilton Head and Aiken.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(f"{n}, SC", p) for n, p in items])], photo="harbor-bridge"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for t in TOOLS:
        path = tool_path(t)
        trail = [("Home", "/"), ("Free tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{tool_path(o)}"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [x for x in TOOLS if x is not t][:3])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec" style="padding-bottom:0"><div class="wrap">{t["markup"]}
<p class="disclaim">For planning only. Results depend on the figures you enter and your policy’s terms, and aren’t a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout" style="padding-top:48px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All free tools", items, path)}</aside></div>
{cta_photo("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Free tools", TOOL_BASE)]
    cards = "".join(card(tool_path(t), TOOL_PHOTO[t["slug"]], t["name"], t["short"], go="Open the tool", meta=t["kind"], hl="h2") for t in TOOLS)
    T = {t["slug"]: tool_path(t) for t in TOOLS}
    body = page_hero(trail, "Free & private", "Free Insurance Claim Tools for South Carolina",
                     "Seven free insurance claim tools built from real appraisal files. Check the carrier’s math, see what you’ll actually collect and plan your next step — no sign-up, nothing stored.", "laptop-review", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards">{cards}</div></div></section>
<section class="sec tint"><div class="wrap two top"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol><li>Start with the <a href="{T["claim-timeline-builder"]}">claim timeline builder</a> so no deadline slips.</li><li>Check roof math with the <a href="{T["roof-area-pitch-estimator"]}">roof area &amp; pitch estimator</a>.</li><li>See what you’ll collect with the <a href="{T["hurricane-deductible-calculator"]}">hurricane deductible</a>, <a href="{T["rcv-acv-holdback-calculator"]}">holdback</a> and <a href="{T["wind-flood-damage-splitter"]}">wind vs. flood</a> calculators.</li><li>Size the dispute with the <a href="{T["claim-gap-fee-estimator"]}">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{T["appraisal-readiness-checkup"]}">readiness checkup</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Tools for South Carolina",
                              "Free insurance claim tools: appraisal cost, RCV vs ACV, roof squares, hurricane deductible, wind vs flood split and a claim deadline planner.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], photo="laptop-review"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("Appraisal process explained", PROCESS), ("Insurance appraisal FAQ", FAQ_P), ("Appraisal glossary", GLOSS), ("Appraisal guides", POST_BASE)]


def step_text(h):
    t = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())
    return t if len(t) <= 300 else t[:297].rsplit(" ", 1)[0] + "…"


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    steps = "".join(f'<li id="step-{i + 1}"><h2>{e(n)}</h2>{h}</li>' for i, (n, h) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in South Carolina",
                     "The insurance appraisal process in South Carolina, step by step: what happens, who does what, and where claims most often stall.", "paperwork",
                     [("Steps", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_INTRO}<ol class="steplist">{steps}</ol>{PROCESS_AFTER}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>
{cta_photo("Ready to talk about your claim?", "We’ll tell you where your file stands in the process and what comes next.")}"""
    howto = {"@type": "HowTo", "name": "The insurance appraisal process in South Carolina", "description": "How a disputed property claim moves through the appraisal clause, from the written demand to a signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}", "text": step_text(h) or n} for i, (n, h) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in South Carolina, Step by Step",
                         "The insurance appraisal process in South Carolina: written demand, appointing appraisers, choosing an umpire, negotiation and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="paperwork"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Insurance appraisal FAQ", path)]
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal FAQ for South Carolina Owners",
                     "Insurance appraisal FAQ, grouped by topic: the basics, costs, timing, South Carolina specifics and how we work.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><div class="note"><b class="h">Jump to a topic</b><ul style="margin:6px 0 0">{toc}</ul></div>{groups}</article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>
{cta_photo("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ: Costs, Timing & SC Rules",
                         "Insurance appraisal FAQ for South Carolina: how appraisal works, costs, timing, hurricane deductibles, the wind pool and when awards bind.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Appraisal glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Insurance Appraisal Glossary of Claim Terms",
                     f"An insurance appraisal glossary of {len(GLOSSARY)} terms you’ll meet in policies, estimates and awards, defined in plain English.", "calculator", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback”, “umpire” or “surge”"></div><div class="az">{az}</div><dl class="glossary">{dl}</dl></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Insurance appraisal glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary: ACV, Umpire, SCWHUA & More",
                         "Insurance appraisal glossary: plain-English definitions of ACV, replacement cost, holdback, umpire, hurricane deductible, SCWHUA and more.",
                         body, [crumbs_schema(trail), dts], photo="calculator"), 0.7)

    for p in POSTS:
        path = post_path(p)
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{post_path(o)}"><small>Guide</small>{e(o["title"])}</a>' for o in [x for x in POSTS if x is not p][:3])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Resources", LEARN)}{list_box("Free tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]])}</aside></div>
{cta_photo("Questions about your own claim?", "Send the estimate and we’ll tell you what we see.")}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(card(post_path(p), POST_PHOTO[p["slug"]], p["title"], p["summary"], go="Read the guide", meta=f'{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]}', hl="h2") for p in POSTS)
    body = page_hero(trail, "Guides", "Insurance Appraisal Guides for South Carolina",
                     "Insurance appraisal guides on hurricane deductibles, tree claims, wind-pool policies, documentation and how umpires decide — written for South Carolina owners.", "modern-home", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards">{cards}</div></div></section>
{cta_photo("Have a claim that doesn’t add up?", "Send the carrier’s estimate. We’ll review it and tell you plainly what we see.")}"""
    write(path, document(path, "Insurance Appraisal Guides for South Carolina Owners",
                         "Insurance appraisal guides for South Carolina: hurricane deductibles, tree fall claims, wind pool policies, photo checklists and umpire decisions.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(p["title"], post_path(p)) for p in POSTS])], photo="modern-home"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About the firm", "About South Carolina Insurance Appraiser",
                     "We are estimators and appraisers who think a property claim should be paid on what the damage actually costs, documented clearly enough that everyone at the table can see it.", "consultation") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("roof-work", sizes="(max-width:960px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>{BRAND} works on a single question: the amount of loss. We have built our process, our documentation standards and our free tools around answering it carefully. That focus lets us act as your appointed appraiser, review an estimate before a dispute hardens, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we read anyone else’s numbers.</li>
<li><strong>Support over volume.</strong> An inflated estimate loses credibility with an umpire. We price what we can document.</li>
<li><strong>Plain-English reports.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Straight triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so on the first call.</li>
<li><strong>Fees in writing.</strong> You know exactly what our work costs before it starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across South Carolina. On any claim we serve in one role only, and we disclose any prior relationship with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. And we don’t promise outcomes — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>South Carolina’s weather changes sharply from the Upstate to the coast. Working in all 46 counties means seeing the full range of losses the state produces — Helene’s tree fall in Greenville and Aiken, river flooding in the Pee Dee, hail in the Midlands and hurricane wind on the Sea Islands — and pricing each with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Claim dispute services", SVC_BASE), ("Locations served", LOC_BASE), ("Free claim tools", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>
{cta_photo("Want a second set of eyes on your claim?", "The first conversation is free and comes with an honest answer.")}"""
    write(path, document(path, "About South Carolina Insurance Appraiser | The Firm",
                         "About South Carolina Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss in disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="consultation"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Contact an Insurance Appraiser in South Carolina",
                     "Contact an insurance appraiser by phone, text, email or the form below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec deep"><div class="wrap contact-grid">
<div class="rv"><p class="kicker lt">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>Statewide — all 46 counties</b></div></li></ul>
<h3>Useful to have ready</h3><ul><li>Your declarations page</li><li>The carrier’s full estimate (PDF)</li><li>Letters or emails from the carrier</li><li>Photos and any contractor estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact an Insurance Appraiser in SC | (844) 537-1427",
                         "Contact an insurance appraiser for a free review of your disputed South Carolina claim. Call (844) 537-1427 or send your claim details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" style=\"width:120px;height:72px;object-fit:cover;border-radius:4px\"")}</td><td>{e(v["title"] or "Untitled")}<br><small>{e(v.get("creator") or "Unknown")} · {e(v.get("provider") or "")}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in sorted(PHOTOS.items()))
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", "Privacy Policy | South Carolina Insurance Appraiser", "How South Carolina Insurance Appraiser collects, uses and protects the information you share through this website, calls and email.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to give us — such as your name, phone number, email, property location and claim details. Our server also records standard technical data (IP address, browser, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>The calculators and checklists run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add site analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> to see, correct or delete the personal information you’ve given us.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "Terms of Use | South Carolina Insurance Appraiser", "The terms that apply when you use the South Carolina Insurance Appraiser website, its free claim tools and the information published here.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you accept these terms. The content is general information about insurance appraisal and property claims in South Carolina.</p>
<h2>No client relationship</h2><p>Reading the site, using a tool or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ and laws and court decisions change; consult a licensed South Carolina attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses listed on our <a href="{CREDITS}">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of South Carolina.</p>"""),
        DISC: ("Legal Disclaimer", "Legal Disclaimer | South Carolina Insurance Appraiser", "Important limits on the information, examples and tools published by South Carolina Insurance Appraiser, including no legal advice or guarantees.", f"""
<h2>General information only</h2><p>Content on this site is educational and general. It describes how appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies and South Carolina law set deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is approaching, consult a South Carolina attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>
<h2>Third-party references</h2><p>References to laws, agencies and storms are for context. Check current facts with official sources such as the South Carolina Department of Insurance.</p>"""),
        CREDITS: ("Photo Credits", "Photo Credits | South Carolina Insurance Appraiser", "Sources, creators and licenses for every photograph used on South Carolina Insurance Appraiser — all CC0 or public-domain images.", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong>, or a <strong>public-domain</strong> work such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each source here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (h1, title, desc, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, e(desc), "commercial-building", cta=False) + f'<div class="wrap layout"><article class="prose">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)


def sitemap_pages():
    path = SITEIDX
    trail = [("Home", "/"), ("Site index", path)]
    groups = [
        ("Main pages", [("Home", "/"), ("About the firm", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Locations", [("All locations", LOC_BASE)] + [(f'{l["city"]}, SC', loc_path(l)) for l in LOCATIONS]),
        ("Free tools", [("All tools", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Legal disclaimer", DISC), ("Photo credits", CREDITS)]),
    ]
    cols = "".join(f'<div><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Index", f"Every page on {BRAND}, grouped by section.", "commercial-building", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-cols">{cols}</div></div></section>'
    write(path, document(path, f"Site Index | {BRAND}", f"Every page on {BRAND}: services, South Carolina locations, free claim tools, guides, FAQ and legal pages.", body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)

    body = f"""<section class="page-hero">{img("storm-clouds", "bg", lazy=False, alt="")}<div class="wrap"><p class="kicker lt">Error 404</p><h1>That page washed out</h1><p class="lede">The page you were looking for has moved or never existed. One of these should get you back on track.</p><div class="btn-row"><a class="btn cu" href="/">Home</a><a class="btn ol" href="{SVC_BASE}">Services</a><a class="btn ol" href="{TOOL_BASE}">Free tools</a><a class="btn ol" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on South Carolina Insurance Appraiser.", body, robots="noindex,follow", photo="storm-clouds"), sitemap=False)


GUARD_PHP = r"""<?php
// South Carolina Insurance Appraiser - canonical host guard. Required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$scia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$scia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$scia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($scia_host === 'www.' . $scia_real || ($scia_host === $scia_real && $scia_proto === 'http')) {
    header('Location: https://' . $scia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory URL.
$scia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($scia_uri, '?'), $scia_m)) {
    $scia_q = strpos($scia_uri, '?') !== false ? substr($scia_uri, strpos($scia_uri, '?')) : '';
    header('Location: ' . $scia_m[1] . $scia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($scia_host !== $scia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
""".replace("__HOST__", HOST)

INDEX_PHP = r"""<?php
// South Carolina Insurance Appraiser - front controller for the static build.
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
if (substr($path, -1) === '/' && $path !== '/' && is_file(__DIR__ . $path . 'index.php')) {
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
        f.write(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    with open(os.path.join(OUT, "index.php"), "w") as f:
        f.write(INDEX_PHP)
    with open(os.path.join(OUT, "_guard.php"), "w") as f:
        f.write(GUARD_PHP)


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
