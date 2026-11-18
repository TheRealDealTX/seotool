#!/usr/bin/env python3
"""Static site generator for coloradoinsuranceappraiser.com.

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
from learn import PROCESS_BODY, PROCESS_STEPS, HOME_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Colorado Insurance Appraiser"
HOST = "coloradoinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261117a"
FAV = "1"
HOURS = "Mon–Fri 8am–6pm MT"

# Google Tag Manager: leave empty until a container ID is supplied (e.g. "GTM-XXXXXXX").
GTM_ID = "GTM-MLHQJXFL"

# Google Search Console HTML-file verification. Written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/colorado-claim-appraisal/"
LOC_BASE = "/colorado-service-areas/"
TOOL_BASE = "/claim-planning-tools/"
RES_BASE = "/resources/"
GUIDE_BASE = "/resources/guides/"
PROCESS = "/resources/appraisal-process/"
FAQ_PATH = "/resources/faq/"
GLOSS = "/resources/glossary/"
ABOUT = "/about-us/"
CONTACT = "/contact-us/"
PRIVACY = "/privacy/"
TERMS = "/terms/"
DISCLAIMER = "/disclaimer/"
HSM = "/html-sitemap/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{GUIDE_BASE}{p['slug']}/"


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


def photo_url(key):
    return f"{DOMAIN}/assets/img/photos/{key}.webp"


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
    "peak": '<path d="M2 20l7-12 4 6 3-4 6 10z"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "calc": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def ic(name, cls="ico"):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark():
    """Brand mark (same as favicon.svg): navy tile, aspen-gold sun, twin white peaks."""
    return ('<svg class="mark" width="44" height="44" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="12" fill="#002868"/>'
            '<circle cx="31.5" cy="16" r="6.5" fill="#F2A900"/>'
            '<path d="M5 38l12.5-19 6.5 9.5 5-6.5L43 38z" fill="#fff"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Colorado</b><small>Insurance Appraiser</small></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/icon-512.png", "contentUrl": DOMAIN + "/icon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "CO", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-CO", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for disputed Colorado property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed hail, wind, wildfire, winter and water claims across Colorado.",
        "areaServed": [{"@type": "State", "name": "Colorado"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Hail damage", "Wildfire claims", "Xactimate estimating", "Umpire services"],
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
def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All appraisal services", SVC_BASE)),
        ("Service areas", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Colorado service areas", LOC_BASE)),
        ("Tools", [(t["name"], tool_path(t)) for t in TOOLS], ("All claim planning tools", TOOL_BASE)),
        ("Resources", [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_PATH), ("Claim glossary", GLOSS), ("Guides & articles", GUIDE_BASE)], ("Resource hub", RES_BASE)),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        menu += (f'<li class="has-sub"><button type="button" class="sub-btn" aria-expanded="false" aria-controls="sub-{i}">{name}{ic("chev", "chev")}</button>'
                 f'<div class="sub" id="sub-{i}"><ul class="{"two" if len(links) > 7 else ""}">{li}</ul><a class="sub-all" href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></div></li>')
    menu += f'<li><a class="nav-a" href="{ABOUT}">About</a></li><li><a class="nav-a" href="{CONTACT}">Contact</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-head"><div class="wrap hrow">
{brand()}
<nav class="primary" aria-label="Main"><ul class="nav">{menu}</ul></nav>
<a class="call-pill" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-d")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x")}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>{HOURS} · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:7])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS[:6])
    return f"""<footer class="site-foot">
<svg class="ridge ridge-foot" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 80V52l90-24 70 30 120-46 80 38 70-20 110 34 140-58 90 40 80-18 120 36 100-30 90 22 130-40 70 26 80-14v52z"/></svg>
<div class="foot-in"><div class="wrap">
<div class="foot-cta"><div><h2>Claim paid, but not paid in full?</h2><p>Send the carrier’s estimate. We’ll tell you what we see — plainly.</p></div><div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-l" href="{CONTACT}">Email the estimate</a></div></div>
<div class="foot-grid">
<div class="foot-brand">{brand("brand brand-f")}
<p>Independent appraisal and estimating for property owners with disputed insurance claims — from the Front Range to the Western Slope.</p>
<ul class="foot-contact"><li><a href="tel:{TEL}">{PHONE_INTL}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{HOURS} · All 64 counties</li></ul></div>
<div><h3>Services</h3><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h3>Service areas</h3><ul>{loc}<li><a href="{LOC_BASE}">All service areas</a></li></ul></div>
<div><h3>Free tools</h3><ul>{tl}<li><a href="{TOOL_BASE}">All tools</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="{ABOUT}">About us</a></li><li><a href="{CONTACT}">Contact us</a></li><li><a href="{RES_BASE}">Resources</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_PATH}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li></ul></div>
</div>
<div class="foot-base"><span>© <span data-year>{date.today().year}</span> {BRAND}</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIMER}">Disclaimer</a></li><li><a href="{HSM}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Site content is general and educational; policy language controls. Outcomes depend on the facts of each claim and are never guaranteed.</p>
</div></div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call now</a><a href="{CONTACT}">{ic("doc")} Free review</a></div>"""


# Head snippet exactly as supplied by the site owner (do not reformat).
GTM_HEAD = """<!-- Google Tag Manager -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-MLHQJXFL"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>
<!-- End Google Tag Manager -->
"""


def gtm_head():
    return GTM_HEAD if GTM_ID else ""


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero", trail=None, main_ref=None):
    canonical = DOMAIN + ("/" if path == "/" else path)
    page_type, extra = "WebPage", []
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        extra.append(n)
    crumbs = crumbs_schema(trail or [("Home", "/")])
    crumbs["@id"] = canonical + "#breadcrumb"
    pimg = PHOTOS[photo]
    primary = {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": photo_url(photo), "contentUrl": photo_url(photo), "width": pimg["fw"], "height": pimg["fh"], "caption": pimg["alt"]}
    if main_ref is None:
        order = ["Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage"]
        found = sorted([n for n in extra if n.get("@type") in order], key=lambda n: order.index(n["@type"]))
        main_ref = found[0]["@id"] if found else DOMAIN + "/#business"
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "breadcrumb": {"@id": crumbs["@id"]}, "primaryImageOfPage": {"@id": primary["@id"]}, "image": {"@id": primary["@id"]},
        "mainEntity": {"@id": main_ref},
    }
    graph = [org_schema(), site_schema(), webpage, crumbs, primary] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n')
    t, d = e(title), e(desc)
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Colorado">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Colorado">
<meta name="geo.region" content="US-CO">
<meta name="geo.placename" content="Colorado">
<meta name="theme-color" content="#002868">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&amp;family=Raleway:wght@600;700;800&amp;display=swap">
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
    # Pages are served as dir/index.php: the host serves real files without running the front
    # controller, so each page starts with the canonical-host guard (www/http 301, off-domain noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
        parts.append(f'<li aria-current="page">{e(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{p}">{e(n)}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(parts) + "</ol></nav>"


RIDGE = ('<svg class="ridge" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
         '<path d="M0 90V62l110-30 60 22 130-50 90 44 60-16 120 38 150-62 80 34 90-20 130 44 110-34 70 18 140-48 100 40v48z"/></svg>')


def page_hero(trail, kicker, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-l" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return (f'<section class="phero"><div class="phero-media">{img(photo, lazy=False, alt="", extra=" data-parallax=\"0.1\"")}</div>'
            f'<div class="wrap phero-in">{crumbs(trail)}<p class="kicker kicker-l">{e(kicker)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div>{RIDGE}</section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}{ic("chev", "chev")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="rail-box rail-call"><p class="rail-k">Free first conversation</p><h2 class="rail-t">Talk through your claim</h2>'
            f'<p>We’ll tell you honestly whether appraisal fits — or whether something else would serve you better.</p>'
            f'<a class="rail-phone" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-gold btn-block" href="{CONTACT}">Send claim details</a></div>')


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("arrow")}</a></li>' for n, p in items)
    return f'<div class="rail-box"><h2 class="rail-t">{e(title)}</h2><ul class="rail-list">{li}</ul></div>'


def rail(*boxes):
    return f'<aside class="rail"><div class="rail-sticky">{"".join(boxes)}</div></aside>'


def cta_band(h="Have a Colorado claim that doesn’t add up?", p="Send us the carrier’s estimate and your photos. We’ll review them and tell you what we see.", photo="cta"):
    return (f'<section class="cta-par">{img(photo, "cta-img", alt="", extra=" data-parallax=\"0.16\"")}<div class="wrap cta-in rv"><h2>{e(h)}</h2><p>{e(p)}</p>'
            f'<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-line-l" href="{CONTACT}">Email the estimate</a></div></div></section>')


def related_cards(items):
    return '<div class="rel-grid">' + "".join(
        f'<a class="rel-card" href="{p}"><span class="rel-ph">{img(ph, sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="rel-b"><small>{e(k)}</small><b>{e(n)}</b></span></a>'
        for k, n, p, ph in items) + "</div>"


LOSSES = ["Hail", "Wind / tornado", "Wildfire", "Fire / smoke", "Snow, ice or frozen pipes", "Water / leak", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", hlevel=3, fid="f"):
    roles = ["Homeowner", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Colorado"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="lead-t">{e(heading)}</h{hlevel}><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{fid}-name">Full name *</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone *</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{fid}-email">Email *</label><input id="{fid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{fid}-city">Property location</label><select id="{fid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{fid}-amt">Amount in dispute</label><select id="{fid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{fid}-car">Insurance company (optional)</label><input id="{fid}-car" name="carrier"></div>
<div class="full"><label for="{fid}-det">What happened, and where does the claim stand?</label><textarea id="{fid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{fid}-web">Website</label><input id="{fid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="full"><button class="btn btn-navy btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="hero-card" action="/api/contact.php" method="post" data-lead novalidate>
<p class="hero-card-k">{ic("shield")} Free, no-obligation review</p>
<h2 class="hero-card-t">Is your claim underpaid?</h2>
<p class="lead-sub">Leave a name and number. We’ll call within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="{PRIVACY}">Privacy policy</a>.</span></label>
<button class="btn btn-gold btn-block" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("front", "Front Range", "Denver · Colorado Springs · Fort Collins", ["Large hail", "Downslope wind", "Wildland-urban fire", "Spring snow"],
     "Most of the state’s population lives along the I-25 corridor, and so do most of its hail claims. Storms that form over the foothills on summer afternoons drift east over Jefferson, Denver, Arapahoe, Douglas, El Paso, Larimer and Weld counties, often hitting the same neighborhoods year after year.",
     "denver"),
    ("plains", "Eastern Plains", "Greeley · Sterling · Lamar", ["Hail", "Tornadoes", "Straight-line wind", "Ag buildings"],
     "East of the urban corridor, open farm country produces the state’s tornadoes and some of its largest hailstones. Claims often blend a farmhouse, machine sheds, grain bins and fencing under one policy, with long drives between adjusters.",
     "plains"),
    ("mountains", "Mountains & resort towns", "Summit · Eagle · Pitkin · Grand", ["Snow load", "Ice dams", "Frozen pipes", "Wildfire"],
     "High-country claims follow the calendar: heavy snow on roofs in winter, burst pipes in unoccupied second homes, and wildfire threat in summer and fall. Remote sites, short building seasons and resort-area labor costs all push repair prices above metro levels.",
     "mtntown"),
    ("west", "Western Slope", "Grand Junction · Montrose · Glenwood Springs", ["Wind", "Wildfire", "Hail", "Water"],
     "Mesa, Delta, Montrose and Garfield counties see strong canyon winds, summer fire on the surrounding mesas and occasional damaging hail. Contractor availability and material delivery from the Front Range can stretch repair timelines.",
     "gj"),
    ("south", "Southern Colorado", "Pueblo · Durango · Trinidad · Alamosa", ["Hail", "Wildfire", "Wind", "Freeze"],
     "From the Pueblo area to La Plata County and the San Luis Valley, the south mixes high-desert hail and wind with forest fire risk around Durango and the Sangre de Cristo foothills.",
     "durango"),
]


def home():
    K = BRAND
    steps = HOME_STEPS
    tl = "".join(f'<li class="tl-step rv"><span class="tl-dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))

    svc_rows = "".join(
        f'<li class="rv"><a class="svc-row" href="{svc_path(s)}"><span class="svc-ph">{img(s["photo"], sizes="120px", alt="")}</span>'
        f'<span class="svc-b"><b>{e(s["name"])}</b><span>{e(s["short"])}</span></span>{ic("arrow", "ico svc-go")}</a></li>' for s in SERVICES)

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="pane-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}</button>'
        for i, (k, n, *_r) in enumerate(REGIONS))
    panes = "".join(
        f'<div class="region-pane" role="tabpanel" id="pane-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}>'
        f'<div class="region-ph">{img(ph, sizes="(max-width:900px) 100vw, 640px", alt="")}</div>'
        f'<div class="region-b"><p class="kicker">{e(sub)}</p><h3>{e(n)}</h3><p>{e(t)}</p><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in perils)}</ul></div></div>'
        for i, (k, n, sub, perils, t, ph) in enumerate(REGIONS))

    tool_cards = "".join(
        f'<a class="tcard rv" href="{tool_path(t)}"><span class="tcard-ph">{img(t["photo"], sizes="(max-width:700px) 100vw, 400px", alt="")}<i>{e(t["kind"])}</i></span>'
        f'<span class="tcard-b"><h3>{e(t["name"])}</h3><span>{e(t["short"])}</span><em>Open the tool {ic("arrow")}</em></span></a>' for t in TOOLS)

    loc_cards = "".join(
        f'<a class="lcard rv" href="{loc_path(l)}">{img(l["photo"], sizes="(max-width:700px) 50vw, 300px", alt="")}<span class="lcard-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>'
        for l in LOCATIONS)

    posts = "".join(
        f'<article class="gcard rv"><a class="gcard-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:700px) 100vw, 400px", alt="")}</a>'
        f'<div class="gcard-b"><p class="meta">{p["read"]} read</p><h3><a href="{post_path(p)}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])

    home_faqs = [
        (f"What does a {K} do?", f"A {K} values property damage when you and your insurer agree the loss is covered but disagree on what it costs. Once appraisal is invoked, we inspect, build an independent line-item estimate, work with the carrier’s appraiser and, if needed, present unresolved items to a neutral umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question — the amount of loss. We don’t negotiate outside appraisal and we don’t give legal advice."),
        ("When is the right time to call?", "Usually after the carrier has issued its estimate and you have a contractor’s number that is meaningfully higher. Call sooner if a deadline in your policy or a letter from the insurer is approaching."),
        ("Is an appraisal award binding?", "On the amount of loss, generally yes, once two of the three panel members sign. Appraisal doesn’t decide coverage questions, which is why the file should be well documented before anyone invokes it."),
        ("What does it cost?", "Each side pays its own appraiser and typically shares the umpire’s fee. We put our fee in writing before work starts, and the first conversation is free."),
        ("Do you cover my part of Colorado?", "Yes. We work in all 64 counties, from the Denver metro and Colorado Springs to Grand Junction, Durango, the mountain resort towns and the Eastern Plains."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero", lazy=False, alt="")}</div>
<div class="wrap hero-grid">
<div class="hero-copy">
<p class="kicker kicker-l">Independent property claim appraisal · Statewide</p>
<h1>{K}<span>for hail, wildfire &amp; storm claims that came up short</span></h1>
<p class="lede">When your insurer accepts the claim but the payment won’t rebuild what you lost, {K} prepares an independent, line-by-line valuation and carries it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line-l" href="#services">See how we help {ic("arrow")}</a></div>
<ul class="hero-points"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Local Colorado pricing</li><li>{ic("check")}Homes, HOAs &amp; commercial</li></ul>
</div>
{hero_form()}
</div>
{RIDGE}
</section>

<section class="alt-band" aria-label="At a glance"><div class="wrap alt-grid">
<div class="alt rv"><b data-count="64">64</b><span>Colorado counties served</span></div>
<div class="alt rv"><b data-count="{len(SERVICES)}">{len(SERVICES)}</b><span>Appraisal &amp; estimating services</span></div>
<div class="alt rv"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>Free claim planning tools</span></div>
<div class="alt rv"><b>2 of 3</b><span>Signatures set a binding award</span></div>
</div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-ph rv">{img("roofer", sizes="(max-width:900px) 100vw, 520px")}<p class="intro-tag">{ic("peak")} Retained by you — never by the carrier</p></div>
<div class="intro-b rv">
<p class="kicker">What we do</p>
<h2>What a {K} does when the numbers don’t match</h2>
<p>Most disputed claims in this state aren’t denials. They’re short payments: a roof priced as a repair when the shingles are discontinued, a hail claim that skipped the gutters and window wraps, a wildfire smoke loss that cleaned surfaces nobody tested. {K} works in that gap between “covered” and “paid in full.”</p>
<ol class="markers">
<li><b>We scope the loss ourselves.</b> Our own inspection, measurements and photos — not an edited copy of the carrier’s estimate.</li>
<li><b>We price it for where you live.</b> Labor and material costs in Breckenridge are not Pueblo’s. A {K} estimate reflects your market.</li>
<li><b>We tell you when appraisal is the wrong tool.</b> Coverage denials and legal questions belong with an attorney, and we’ll say so on the first call.</li>
</ol>
<a class="btn btn-navy" href="{ABOUT}">How we work {ic("arrow")}</a>
</div>
</div></section>

<section class="sec tint" id="services"><div class="wrap svc-split">
<div class="svc-head">
<p class="kicker">Services</p>
<h2>Claim services from {K}</h2>
<p>Eleven services built around a single job: a valuation of your loss that holds up in front of the other appraiser and, if it comes to that, an umpire.</p>
<p>Not sure where to start? Most files begin with a <a href="{svc_path(SVC_BY["carrier-estimate-review"])}">carrier estimate review</a>.</p>
<a class="btn btn-navy" href="{SVC_BASE}">Compare all services {ic("arrow")}</a>
</div>
<ul class="svc-list" data-stagger>{svc_rows}</ul>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Statewide knowledge</p><h2>Five regions, five kinds of Colorado claims</h2><p>A hailstorm in Aurora, a frozen pipe in a Vail condo and a wildfire on the Western Slope produce very different estimates. A {K} has to know how each region’s weather shows up on a building — and in the carrier’s numbers.</p></div>
<div class="regions rv" data-regions><div class="region-tabs" role="tablist" aria-label="Colorado regions">{tabs}</div>{panes}</div>
</div></section>

<section class="hail-band">{img("hail", "hail-img", alt="", extra=' data-parallax="0.14"')}<div class="wrap hail-in">
<div class="rv"><p class="kicker kicker-l">Hail Alley</p><h2>The Front Range sits in the middle of Hail Alley</h2>
<p>Forecasters use the name for the high plains where the country’s most frequent large hail falls, and metro Denver sits squarely inside it. The May 8, 2017 storm that battered the west metro is often cited as the costliest insured event in state history, and a 4.83-inch stone that fell near Bethune in 2019 set the state record.</p>
<p>For a {K}, that history matters: repeat storms create arguments about old versus new damage, discontinued shingles and whether a roof can really be repaired.</p>
<a class="btn btn-gold" href="{svc_path(SVC_BY["hail-roof-damage-appraisal"])}">Hail &amp; roof appraisal {ic("arrow")}</a></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">The process</p><h2>How {K} takes a claim from dispute to award</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result on the amount of loss. Here is the path, start to finish.</p></div>
<ol class="timeline" data-timeline><span class="tl-line" aria-hidden="true"><span class="tl-fill"></span></span>{tl}</ol>
<p class="center"><a class="link" href="{PROCESS}">Read the full appraisal process guide {ic("arrow")}</a></p>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Free &amp; private</p><h2>Free claim tools from {K}</h2><p>Check the carrier’s math before you pick up the phone. Every tool runs in your browser; nothing you type is stored or sent.</p></div>
<div class="tgrid" data-stagger>{tool_cards}</div>
<p class="center"><a class="btn btn-navy" href="{TOOL_BASE}">Browse all {len(TOOLS)} tools {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Service areas</p><h2>Where {K} works most often</h2><p>We take files in every county. These are the cities where {K} handles claims most often, each with its own storm history and housing mix.</p></div>
<div class="lgrid" data-stagger>{loc_cards}</div>
<p class="center"><a class="link" href="{LOC_BASE}">All Colorado service areas {ic("arrow")}</a></p>
</div></section>

<section class="sec navy"><div class="wrap">
<div class="sec-head rv"><p class="kicker kicker-l">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and fees, and {K} will point you elsewhere when appraisal isn’t the right fit.</p></div>
<div class="who" data-stagger>
<div class="who-card who-on rv"><h3>{K}</h3><p class="who-k">Values the amount of loss</p><ul><li>{ic("check")}Coverage accepted, number disputed</li><li>{ic("check")}Binding award on two of three signatures</li><li>{ic("x")}Doesn’t decide coverage</li></ul></div>
<div class="who-card rv"><h3>Public adjuster</h3><p class="who-k">Handles the whole claim</p><ul><li>{ic("check")}Often hired early, from first notice</li><li>{ic("check")}Negotiates a settlement</li><li>{ic("x")}Doesn’t sit on an appraisal panel as a neutral</li></ul></div>
<div class="who-card rv"><h3>Attorney</h3><p class="who-k">Handles legal disputes</p><ul><li>{ic("check")}Denials, bad faith, suit deadlines</li><li>{ic("check")}Can litigate and advise on statutes</li><li>{ic("x")}Usually not needed for a pure pricing gap</li></ul></div>
</div></div></section>

<section class="sec"><div class="wrap faq-split">
<div class="rv"><p class="kicker">FAQ</p><h2>Questions people ask a {K}</h2><p>Straight answers about how appraisal works, what it costs and when it’s the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_PATH}">All FAQs {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Claim glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker">Guides</p><h2>Read before you invoke appraisal</h2><p>Practical guides from {K} on hail documentation, wildfire claims, deductibles and reading an estimate.</p></div>
<div class="ggrid" data-stagger>{posts}</div>
<p class="center"><a class="link" href="{GUIDE_BASE}">All guides {ic("arrow")}</a></p>
</div></section>

{cta_band("Storm season is claim season — check the numbers before you sign", f"A short review by {K} now can keep you from accepting a settlement that won’t cover the repair.", "cta")}

<section class="sec" id="contact"><div class="wrap contact-split">
<div class="rv"><p class="kicker">Start with a conversation</p><h2>Talk to {K} about your claim</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing — no pressure, no obligation.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>{HOURS}</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 64 Colorado counties</b></div></li></ul></div>
<div class="rv">{lead_form(page="/", fid="c")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Hail & Wildfire Claims",
                        "Colorado Insurance Appraiser: independent appraisal, estimate review and umpire work for underpaid hail, wind, wildfire and winter claims.",
                        body, [faq_schema(home_faqs)], photo="hero", main_ref=DOMAIN + "/#business"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    for s in SERVICES:
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SVC_BY[x] for x in s["related"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], s["photo"], s["facts"]) + f"""
<div class="wrap two-col"><article class="prose">{s["body"]}
<h2>Common questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related_cards([("Service", r["name"], svc_path(r), r["photo"]) for r in rel])}
</article>
{rail(call_box(), list_box("All services", items, path), list_box("Where we work", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All service areas", LOC_BASE)]))}</div>
{cta_band()}"""
        schema = [faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                                          "areaServed": {"@type": "State", "name": "Colorado"}, "url": DOMAIN + path, "image": photo_url(s["photo"])}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=s["photo"], trail=trail), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="icard rv" href="{svc_path(s)}"><span class="icard-ph">{img(s["photo"], sizes="(max-width:700px) 100vw, 380px", alt="")}</span>'
        f'<span class="icard-b"><small>Service {i + 1:02d}</small><h2>{e(s["name"])}</h2><span>{e(s["short"])}</span></span></a>' for i, s in enumerate(SERVICES))
    idx_faq = [("Can I hire you for only part of the process?", "Yes. Many owners start with an estimate review and decide later whether to invoke appraisal. Others call us after a demand has already been made."),
               ("Do you handle commercial and HOA claims?", "Yes — single-family homes, condos and townhomes, multifamily, retail, office, industrial, churches and association-insured buildings."),
               ("Which perils do you work on?", "Hail, wind, tornado, wildfire, fire and smoke, snow load and ice dams, frozen and burst pipes, and other covered water losses.")]
    body = page_hero(trail, "What we do", "Colorado Insurance Appraisal Services",
                     f"From a one-time estimate review to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "clipboard") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Getting started</p><h2>Most files begin with an estimate review</h2><p>Before anyone invokes appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and many disputes close right there.</p><a class="btn btn-navy" href="{svc_path(SVC_BY["carrier-estimate-review"])}">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block(idx_faq)}</div></div></section>
{cta_band()}"""
    write(SVC_BASE, document(SVC_BASE, "Colorado Insurance Appraisal Services | Claim Help",
                             "Colorado insurance appraisal services: appraisal clause work, hail, wildfire, winter, water and commercial claims, estimate review and umpires.",
                             body, [{"@type": "CollectionPage"}, item_list(items), faq_schema(idx_faq)], photo="clipboard", trail=trail), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Service areas", LOC_BASE), (l["city"], path)]
        near = [LOC_BY[n] for n in l["near"]]
        svc_links = "".join(f'<li><a href="{svc_path(SVC_BY[x])}">{e(SVC_BY[x]["name"])}</a></li>' for x in l["services"])
        tags = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        body = page_hero(trail, l["region"], l["h1"], l["lede"], l["photo"],
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap two-col"><article class="prose">
<div class="callout"><p class="callout-t">Local claim risks</p><ul class="tags">{tags}</ul></div>
{l["body"]}
<h2>Services for {e(l["city"])} property owners</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding area. The ones local owners ask about most:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby service areas</h2>{related_cards([("Nearby", n["city"], loc_path(n), n["photo"]) for n in near])}
</article>
{rail(call_box(), list_box("Colorado service areas", items, path), list_box("Free claim tools", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>
{cta_band(f"Disputed claim in {l['city']}?", "Send us the estimate and your photos. We’ll tell you what we see.")}"""
        schema = [faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Colorado", "serviceType": "Insurance appraisal",
                                          "provider": {"@id": DOMAIN + "/#business"}, "url": DOMAIN + path, "image": photo_url(l["photo"]),
                                          "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Colorado"}}}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=l["photo"], trail=trail), 0.8)

    trail = [("Home", "/"), ("Service areas", LOC_BASE)]
    cards = "".join(
        f'<a class="icard rv" href="{loc_path(l)}"><span class="icard-ph">{img(l["photo"], sizes="(max-width:700px) 100vw, 380px", alt="")}</span>'
        f'<span class="icard-b"><small>{e(l["county"])}</small><h2>{e(l["city"])}</h2><span>{e(l["card"])}</span></span></a>' for l in LOCATIONS)
    reg = "".join(f'<div class="reg-row rv"><span class="reg-ph">{img(ph, sizes="(max-width:700px) 100vw, 300px", alt="")}</span><div><p class="kicker">{e(sub)}</p><h3>{e(n)}</h3><p>{e(t)}</p></div></div>' for k, n, sub, _p, t, ph in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 64 Colorado Counties",
                     f"{BRAND} works statewide, from the Eastern Plains to the Four Corners. These pages cover the cities where we handle claims most often.", "denver") + f"""
<section class="sec"><div class="wrap"><div class="igrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap"><div class="sec-head rv"><p class="kicker">Regions</p><h2>How claims differ across the state</h2><p>The same policy language plays out very differently in a Lakewood ranch house, a Breckenridge condo and a Grand Junction orchard property.</p></div><div class="reg-list">{reg}</div></div></section>
{cta_band("Don’t see your town?", "We cover every Colorado county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Colorado Service Areas | Insurance Appraisal by City",
                             "Insurance appraisal in all 64 Colorado counties, including Denver, Colorado Springs, Aurora, Fort Collins, Boulder, Pueblo and Grand Junction.",
                             body, [{"@type": "CollectionPage"}, item_list(items)], photo="denver", trail=trail), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for t in TOOLS:
        path = tool_path(t)
        trail = [("Home", "/"), ("Tools", TOOL_BASE), (t["name"], path)]
        others = [x for x in TOOLS if x is not t][:3]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], t["lede"], t["photo"], cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="fine">For planning only. Results depend on the figures you enter and your policy’s terms. They aren’t a quote, an appraisal or legal advice. Example figures are illustrative.</p></div></section>
<div class="wrap two-col"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related_cards([(o["kind"], o["name"], tool_path(o), o["photo"]) for o in others])}</article>
{rail(call_box(), list_box("All claim planning tools", items, path))}</div>
{cta_band("Want a professional to check the numbers?", "Send us your estimate and we’ll review it line by line.")}"""
        schema = [faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication",
                                          "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
                                          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=t["photo"], trail=trail), 0.8)

    trail = [("Home", "/"), ("Tools", TOOL_BASE)]
    cards = "".join(
        f'<a class="tcard rv" href="{tool_path(t)}"><span class="tcard-ph">{img(t["photo"], sizes="(max-width:700px) 100vw, 400px", alt="")}<i>{e(t["kind"])}</i></span>'
        f'<span class="tcard-b"><h2>{e(t["name"])}</h2><span>{e(t["short"])}</span><em>Open the tool {ic("arrow")}</em></span></a>' for t in TOOLS)
    order = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a> — {e(t["order"])}</li>' for t in sorted(TOOLS, key=lambda x: x["step"]))
    body = page_hero(trail, "Free & private", "Free Claim Planning Tools for Colorado Owners",
                     f"Seven calculators and planners built from real appraisal work. Check the carrier’s math, plan your deadlines and decide on next steps — no sign-up, nothing stored.", "calc", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tgrid" data-stagger>{cards}</div></div></section>
<section class="sec tint"><div class="wrap faq-split"><div class="rv"><p class="kicker">Suggested order</p><h2>Using the tools together</h2><ol class="order">{order}</ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Claim Planning Tools | Colorado Calculators",
                              "Free claim planning tools for Colorado owners: award gap, holdback, roof pitch, hail deductible and hail size calculators plus a timeline.",
                              body, [{"@type": "CollectionPage"}, item_list(items)], photo="calc", trail=trail), 0.9)


# ---------------------------------------------------------------- resources
LEARN = [("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_PATH), ("Claim glossary", GLOSS), ("Guides & articles", GUIDE_BASE)]


def learn_pages():
    # hub
    trail = [("Home", "/"), ("Resources", RES_BASE)]
    hub = [("Appraisal process guide", PROCESS, "meeting", "Seven stages from the first disagreement to a signed award."),
           ("Appraisal FAQ", FAQ_PATH, "interior", "Answers grouped by topic: process, costs, timing and Colorado specifics."),
           ("Claim glossary", GLOSS, "calc2", f"{len(GLOSSARY)} policy and estimate terms in plain English, with a search filter."),
           ("Guides & articles", GUIDE_BASE, "snowroof", f"{len(POSTS)} in-depth guides on hail, wildfire, winter claims and estimates.")]
    cards = "".join(f'<a class="icard rv" href="{p}"><span class="icard-ph">{img(ph, sizes="(max-width:700px) 100vw, 380px", alt="")}</span><span class="icard-b"><small>Resource</small><h2>{e(n)}</h2><span>{e(t)}</span></span></a>' for n, p, ph, t in hub)
    body = page_hero(trail, "Learn", "Colorado Insurance Appraisal Resources",
                     "Everything we wish every policyholder knew before a claim dispute: how appraisal works, the words in your estimate and the questions to ask first.", "meeting", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="igrid igrid-2" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(RES_BASE, document(RES_BASE, "Insurance Appraisal Resources | Colorado Owners",
                             "Free Colorado insurance appraisal resources: a step-by-step process guide, an FAQ by topic, a searchable claim glossary and in-depth guides.",
                             body, [{"@type": "CollectionPage"}, item_list([(n, p) for n, p, *_ in hub])], photo="meeting", trail=trail), 0.8)

    # process
    path = PROCESS
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Colorado",
                     "Seven stages, from the first disagreement to a signed award: what happens, who does what, and where files most often go wrong.", "meeting",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap two-col"><article class="prose">{PROCESS_BODY}</article>
{rail(call_box(), list_box("Resources", LEARN, path))}</div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Colorado", "description": "The seven stages of a property insurance appraisal, from the disagreement to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": DOMAIN + path + f"#stage-{i + 1}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Colorado | 7 Stages",
                         "A step-by-step guide to insurance appraisal in Colorado: the written demand, naming appraisers, selecting an umpire, negotiation and the award.",
                         body, [howto], photo="meeting", trail=trail), 0.8)

    # faq
    path = FAQ_PATH
    trail = [("Home", "/"), ("Resources", RES_BASE), ("FAQ", path)]
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Colorado Insurance Appraisal FAQ",
                     f"{len(allq)} plain answers to the questions we hear most, grouped by topic: the process, costs and timing, perils, and Colorado-specific rules.", "interior") + f"""
<div class="wrap two-col"><article class="prose"><nav class="toc" aria-label="FAQ topics"><p class="toc-t">Topics</p><ul>{toc}</ul></nav>{groups}</article>
{rail(call_box(), list_box("Resources", LEARN, path))}</div>{cta_band("Didn’t see your question?", "Call or email — we’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Colorado Claim Questions",
                         "Colorado insurance appraisal FAQ by topic: how the process works, costs and timing, hail and wildfire claims, and Colorado rules to know.",
                         body, [faq_schema(allq)], photo="interior", trail=trail), 0.8)

    # glossary
    path = GLOSS
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<div class=\"gl-item\"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>"
    body = page_hero(trail, "Reference", "Property Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type to filter.", "calc2", cta=False) + f"""
<div class="wrap two-col"><article class="prose"><div class="gl-filter"><label for="gl-q">Search the glossary</label><input id="gl-q" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"><p class="gl-count" data-gl-count>{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl><p class="gl-none" hidden>No terms match that search.</p></article>
{rail(call_box(), list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "url": DOMAIN + path,
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Glossary | Holdback, ACV, Umpire",
                         "Searchable glossary of property insurance claim terms: ACV, RCV, recoverable depreciation, holdback, appraisal award, umpire, O&P and more.",
                         body, [dts], photo="calc2", trail=trail), 0.7)

    # guides
    for p in POSTS:
        path = post_path(p)
        trail = [("Home", "/"), ("Resources", RES_BASE), ("Guides", GUIDE_BASE), (p["short"], path)]
        others = [x for x in POSTS if x is not p][:3]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), p["photo"], cta=False) + f"""
<div class="wrap two-col"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related_cards([("Guide", o["title"], post_path(o), o["photo"]) for o in others])}</article>
{rail(call_box(), list_box("Resources", LEARN), list_box("Free tools", [(t["name"], tool_path(t)) for t in TOOLS[:3]]))}</div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": photo_url(p["photo"]), "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], og_type="article", photo=p["photo"], trail=trail), 0.7)

    path = GUIDE_BASE
    trail = [("Home", "/"), ("Resources", RES_BASE), ("Guides", path)]
    cards = "".join(
        f'<article class="gcard rv"><a class="gcard-ph" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(p["photo"], sizes="(max-width:700px) 100vw, 400px", alt="")}</a>'
        f'<div class="gcard-b"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read</p><h2><a href="{post_path(p)}">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>' for p in POSTS)
    body = page_hero(trail, "Guides & articles", "Colorado Claim Guides & Appraisal Articles",
                     "In-depth guides on hail documentation, wildfire total losses, percentage deductibles, winter claims and reading a carrier estimate.", "snowroof", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="ggrid" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Colorado Claim Guides | Insurance Appraisal Articles",
                         "Colorado claim guides: documenting hail damage, wildfire total losses, percentage deductibles, ice dams and how to read an insurance estimate.",
                         body, [{"@type": "CollectionPage"}, item_list([(p["title"], post_path(p)) for p in POSTS])], photo="snowroof", trail=trail), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About us", path)]
    body = page_hero(trail, "About us", "About Colorado Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage actually costs — documented clearly enough that everyone at the table can see it.", "meeting2") + f"""
<div class="wrap two-col"><article class="prose">
<figure class="lead-img">{img("consult", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>Most claim professionals do a little of everything. We chose to specialize. {BRAND} focuses on one question — the amount of loss — and our process, tools and documentation standards are built around answering it well. That focus lets us serve as your appointed appraiser, review an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Independent scope first.</strong> We inspect and measure before we read anyone else’s numbers.</li>
<li><strong>Defensible over dramatic.</strong> An inflated estimate looks good on day one and loses credibility with the umpire on day forty. We price what we can support.</li>
<li><strong>Local pricing.</strong> Mountain-town labor, Front Range material costs and Western Slope travel all show up in a real estimate.</li>
<li><strong>Plain-English reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Fees in writing.</strong> You know what it costs before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo and townhome owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Colorado. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. And we don’t promise outcomes — no honest appraiser can.</p>
<h2>Why statewide</h2>
<p>Colorado’s climate changes with elevation and geography. Working in all 64 counties means seeing every kind of loss the state produces — hail in Aurora, snow load in Summit County, wind in Boulder, wildfire smoke in Larimer County — and pricing each with local knowledge.</p>
</article>{rail(call_box(), list_box("Explore", [("Our services", SVC_BASE), ("Service areas", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROCESS)]))}</div>{cta_band()}"""
    write(path, document(path, "About Us | Colorado Insurance Appraiser",
                         "About Colorado Insurance Appraiser, an independent appraisal and estimating practice focused on the amount of loss in disputed property claims.",
                         body, [{"@type": "AboutPage"}], photo="meeting2", trail=trail), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact us", path)]
    body = page_hero(trail, "Get in touch", "Contact Colorado Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consult", cta=False) + f"""
<section class="sec"><div class="wrap contact-split">
<div class="rv"><p class="kicker">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>{HOURS}</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>Statewide — all 64 counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}Your policy declarations page</li><li>{ic("check")}The carrier’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the insurer</li><li>{ic("check")}Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Send us your claim details", page=path, hlevel=2, fid="k")}</div></div></section>"""
    write(path, document(path, "Contact Us | Colorado Insurance Appraiser",
                         "Contact Colorado Insurance Appraiser for a free review of a disputed claim. Call or text (844) 537-1427, email us or send your details online.",
                         body, [{"@type": "ContactPage"}], photo="consult", trail=trail), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = [
        (PRIVACY, "Privacy Policy", "How we collect, use and protect the information you share with us.",
         "Privacy Policy | Colorado Insurance Appraiser",
         "Privacy policy for Colorado Insurance Appraiser: what we collect through forms, calls and email, how we use it, and the choices you have.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email us, we collect what you choose to share — such as your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working properly.</li></ul>
<p>We don’t sell your personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and planners run entirely in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We use Google Tag Manager and Google’s measurement tags to understand how visitors use the site, such as which pages are viewed. These tools may set cookies and collect standard device and usage data under Google’s privacy policy. Fonts load from Google Fonts, which may log standard request data. You can limit cookies through your browser settings.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete personal information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        (TERMS, "Terms of Use", "The terms that apply when you use this website and its tools.",
         "Terms of Use | Colorado Insurance Appraiser",
         "Terms of use for the Colorado Insurance Appraiser website, its free claim planning tools and the general information published on it.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Colorado.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That relationship begins only when both sides sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Colorado attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators provide planning estimates based on what you enter. They are not appraisals, quotes or predictions of any claim outcome. Example figures are illustrative.</p>
<h2>Intellectual property</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Colorado.</p>"""),
        (DISCLAIMER, "Disclaimer", "Important limits on the information published on this website.",
         "Disclaimer | Colorado Insurance Appraiser",
         "Disclaimer for Colorado Insurance Appraiser: general information only, not legal advice, illustrative figures and no guarantee of results.", f"""
<h2>General information only</h2><p>The content on this website is educational and general. It describes how insurance appraisal commonly works, but your policy’s language controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes a deadline. If one is approaching, consult a Colorado attorney promptly.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They do not show our clients’ properties.</p>
<h2>Legal and historical references</h2><p>References to statutes, programs, agencies or past storms and fires are general descriptions for context, not legal analysis. Verify current law and programs with official sources such as the Colorado Division of Insurance.</p>"""),
    ]
    for path, h1, lede, title, desc, content in legal:
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office", cta=False) + f'<div class="wrap two-col"><article class="prose narrow">{content}</article>{rail(call_box())}</div>'
        write(path, document(path, title, desc, body, [], photo="office", trail=trail), 0.3)


def sitemap_pages():
    path = HSM
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About us", ABOUT), ("Contact us", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Service areas", [("All service areas", LOC_BASE)] + [(l["city"], loc_path(l)) for l in LOCATIONS]),
        ("Claim planning tools", [("All tools", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", [("Resource hub", RES_BASE), ("Appraisal process guide", PROCESS), ("Appraisal FAQ", FAQ_PATH), ("Claim glossary", GLOSS), ("Guides & articles", GUIDE_BASE)] + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIMER)]),
    ]
    cols = "".join(f'<div class="hsm-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "office", cta=False) + f'<section class="sec"><div class="wrap"><div class="hsm" data-stagger>{cols}</div></div></section>'
    write(path, document(path, "Site Map | Colorado Insurance Appraiser",
                         "HTML site map of Colorado Insurance Appraiser: every service, Colorado service area, free claim tool, guide and legal page in one list.",
                         body, [], photo="office", trail=trail), 0.3)

    trail = [("Home", "/"), ("Page not found", "/404.html")]
    body = (f'<section class="phero phero-404"><div class="phero-media">{img("snowroof", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker kicker-l">Error 404</p>'
            f'<h1>This trail doesn’t go anywhere</h1><p class="lede">The page you’re looking for may have moved or never existed. Try one of these instead.</p>'
            f'<div class="btn-row"><a class="btn btn-gold" href="/">Home</a><a class="btn btn-line-l" href="{SVC_BASE}">Services</a><a class="btn btn-line-l" href="{TOOL_BASE}">Free tools</a><a class="btn btn-line-l" href="{CONTACT}">Contact</a></div></div>{RIDGE}</section>')
    write("/404.html", document("/404.html", "Page Not Found | Colorado Insurance Appraiser",
                                "Sorry, that page could not be found on Colorado Insurance Appraiser. Use the links to reach our services, free tools or contact page.",
                                body, [], robots="noindex,follow", photo="snowroof", trail=trail), sitemap=False)


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
        f.write(GUARD_PHP.replace("__HOST__", HOST))
    # Search Console verification: exact bytes, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Colorado Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$cia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$cia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$cia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$cia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($cia_host === 'www.' . $cia_real || ($cia_host === $cia_real && $cia_proto === 'http')) {
    header('Location: https://' . $cia_real . $cia_uri, true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', (string) strtok($cia_uri, '?'), $cia_m)) {
    $cia_q = strpos($cia_uri, '?') !== false ? substr($cia_uri, strpos($cia_uri, '?')) : '';
    header('Location: ' . $cia_m[1] . $cia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($cia_host !== $cia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Colorado Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (a directory's index.php included)
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
