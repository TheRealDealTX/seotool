#!/usr/bin/env python3
"""Static site generator for thecolonypublicadjuster.com.

    python3 build.py      -> writes the full site into ./dist and ./thecolonypublicadjuster-site.zip

Standard library only (Pillow optional, used to read image sizes and make the OG image).
"""
import html
import json
import os
import re
import shutil
import zipfile
from datetime import date

from content.services import SERVICES, SERVICE_BY_SLUG
from content.blog import POSTS, POST_BY_SLUG
from content import pages as P

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, "static")
DIST = os.path.join(ROOT, "dist")
ZIP = os.path.join(ROOT, "thecolonypublicadjuster-site.zip")

SITE = {
    "name": "The Colony Public Adjuster",
    "origin": "https://thecolonypublicadjuster.com",
    "phone": "(832) 503-5866",
    "phone_href": "+18325035866",
    "phone_schema": "+1-832-503-5866",
    "email": "info@thecolonypublicadjuster.com",
    "company": "Rise Public Adjusting LLC",
    "license": "3356839",
    "city": "The Colony",
    "county": "Denton County",
    "zip": "75056",
    "lat": "33.0890",
    "lng": "-96.8864",
    "parent_site": "https://txpublicadjusting.com/",
}
TODAY = date.today().isoformat()
ASSET_VER = TODAY.replace("-", "")

# --------------------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "home": '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "hail": '<path d="M16 13V9a4 4 0 1 0-8 0 4 4 0 0 0-4 4h0a3 3 0 0 0 3 3h10a3 3 0 0 0 0-6"/><path d="M8 19v.01M12 21v.01M16 19v.01"/>',
    "droplet": '<path d="M12 2.7s7 7.3 7 12.3a7 7 0 0 1-14 0c0-5 7-12.3 7-12.3z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.3 1.6 1.3 2.8 2.5 2.8z"/>',
    "filex": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9.5 12.5l5 5M14.5 12.5l-5 5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2M9 13l2 2 4-4"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v3M8 18h4"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3 6 1 1 2-2M3 12l1 1 2-2M3 18l1 1 2-2"/>',
    "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "scale": '<path d="M12 3v18M5 21h14M3 7h18M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


ARROW = icon("arrow")

# --------------------------------------------------------------------------- images
_SIZES = {}


def _size(name):
    if name in _SIZES:
        return _SIZES[name]
    path = os.path.join(STATIC, "assets", "img", name + ".webp")
    w, h = 1600, 1000
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        pass
    _SIZES[name] = (w, h)
    return w, h


def img(name, alt, cls="", lazy=True, parallax=None, priority=False):
    w, h = _size(name)
    attrs = [f'src="/assets/img/{name}.webp"', f'alt="{html.escape(alt)}"', f'width="{w}"', f'height="{h}"']
    if cls:
        attrs.append(f'class="{cls}"')
    if priority:
        attrs.append('fetchpriority="high"')
    elif lazy:
        attrs.append('loading="lazy" decoding="async"')
    if parallax:
        attrs.append(f'data-parallax="{parallax}"')
    return "<img " + " ".join(attrs) + ">"


# --------------------------------------------------------------------------- navigation
NAV = [("Home", "/"), ("About", "/about/"), ("Services", "/services/"), ("Process", "/our-process/"),
       ("Tools", "/tools/"), ("Blog", "/blog/"), ("FAQs", "/faqs/"), ("Contact", "/contact/")]


def header(current):
    drop = "".join(
        f'<a href="/services/{s["slug"]}/"><span class="drop-ico">{icon(s["icon"])}</span>'
        f'<span><strong>{s["name"]}</strong><span>{s["card"]}</span></span></a>' for s in SERVICES)
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if current == href else ""
        if label == "Services":
            links.append(
                f'<div class="nav-drop"><button type="button" aria-expanded="false" aria-haspopup="true">Services</button>'
                f'<div class="drop-panel">{drop}<a href="/services/"><span class="drop-ico">{icon("list")}</span>'
                f'<span><strong>All claim services</strong><span>Compare every service we offer</span></span></a></div></div>')
        else:
            links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f'''<div class="scroll-progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span class="tagline"><span class="dot"></span>Licensed Texas public adjusters &middot; Serving The Colony &amp; Denton County</span><a href="tel:{SITE["phone_href"]}">Free claim review: {SITE["phone"]}</a></div></div>
<header class="site-header"><div class="wrap header-row">
<a class="brand" href="/" aria-label="{SITE["name"]} home"><span class="brand-mark">TC</span><span class="brand-text">The Colony<small>PUBLIC ADJUSTER</small></span></a>
<nav class="main-nav" id="main-nav" aria-label="Main">{"".join(links)}</nav>
<div class="header-cta"><a class="button small" href="/contact/">Free claim review</a>
<button class="menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button></div>
</div></header><div class="nav-backdrop"></div>'''


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["short"]}</a></li>' for s in SERVICES)
    return f'''<footer class="site-footer"><div class="wrap footer-grid">
<div><a class="brand" href="/"><span class="brand-mark">TC</span><span class="brand-text">The Colony<small>PUBLIC ADJUSTER</small></span></a>
<p style="margin-top:20px">{SITE["name"]} represents homeowners and businesses in The Colony, Texas with residential and commercial property insurance claims.</p>
<span class="license">{icon("shield")} {SITE["company"]} &middot; Texas License #{SITE["license"]}</span></div>
<div><h3>Explore</h3><ul><li><a href="/about/">About us</a></li><li><a href="/our-process/">Our process</a></li><li><a href="/tools/">Free claim tools</a></li><li><a href="/blog/">Claim guides</a></li><li><a href="/faqs/">FAQs</a></li><li><a href="/contact/">Contact</a></li></ul></div>
<div><h3>Claims we handle</h3><ul>{svc}</ul></div>
<div><h3>Start a conversation</h3><ul><li><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a></li><li><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li><li>The Colony, TX {SITE["zip"]} &middot; {SITE["county"]}</li></ul>
<p style="margin-top:18px">Also serving Frisco, Little Elm, Lewisville, Plano, Carrollton and Hebron.</p>
<a class="button small light" href="/contact/">Request your free review</a></div>
</div>
<div class="wrap footer-bottom"><span>&copy; <span data-year>{date.today().year}</span> {SITE["name"]}. A service of {SITE["company"]}.</span><nav aria-label="Legal"><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-use/">Terms of Use</a><a href="/sitemap/">Sitemap</a></nav></div>
<p class="wrap disclaimer">General educational information only. Coverage and claim outcomes depend on your policy and the facts of the loss, and no outcome is guaranteed. {SITE["name"]} is not a law firm and does not provide legal advice.</p>
</footer>
<div class="mobile-cta"><a class="button ghost" href="tel:{SITE["phone_href"]}">{icon("phone")} Call</a><a class="button" href="/contact/">Free review</a></div>
<button class="back-top" type="button" aria-label="Back to top"><svg class="ring-svg" viewBox="0 0 54 54" aria-hidden="true"><circle cx="27" cy="27" r="24" stroke="#f0e2e6"/><circle class="fg" cx="27" cy="27" r="24" stroke="#6f1731" stroke-dasharray="151" stroke-dashoffset="151"/></svg>{icon("up", "arrow")}</button>'''


# --------------------------------------------------------------------------- schema
ORG_ID = SITE["origin"] + "/#organization"


def base_schema():
    return [
        {
            "@type": ["ProfessionalService", "LocalBusiness"],
            "@id": ORG_ID,
            "name": SITE["name"],
            "url": SITE["origin"] + "/",
            "logo": SITE["origin"] + "/assets/img/icon-512.png",
            "image": SITE["origin"] + "/assets/img/og-image.jpg",
            "telephone": SITE["phone_schema"],
            "email": SITE["email"],
            "priceRange": "Free initial claim review",
            "description": "Public adjuster serving The Colony, Texas. Residential and commercial property insurance claim representation for wind, hail, water, fire and denied or underpaid claims.",
            "address": {"@type": "PostalAddress", "addressLocality": "The Colony", "addressRegion": "TX",
                        "postalCode": SITE["zip"], "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]},
            "areaServed": [{"@type": "City", "name": c + ", TX"} for c in
                           ["The Colony", "Frisco", "Little Elm", "Lewisville", "Plano", "Carrollton"]],
            "parentOrganization": {"@type": "Organization", "name": SITE["company"], "url": SITE["parent_site"]},
            "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                              "name": "Texas Public Adjuster License #" + SITE["license"],
                              "recognizedBy": {"@type": "GovernmentOrganization", "name": "Texas Department of Insurance"}},
            "knowsAbout": ["Public adjusting", "Hail damage claims", "Wind damage claims", "Water damage claims",
                           "Fire damage claims", "Commercial property claims", "Denied insurance claims"],
            "sameAs": [SITE["parent_site"]],
        },
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "name": SITE["name"], "url": SITE["origin"] + "/",
         "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"},
    ]


def breadcrumb_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE["origin"] + url}
        for i, (name, url) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
        for q, a in faqs]}


# --------------------------------------------------------------------------- page shell
def render(path, title, desc, body, current=None, schema=None, og_image="og-image.jpg", og_type="website",
           scripts=(), head_extra="", noindex=False):
    url = SITE["origin"] + path
    graph = base_schema() + [{"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title,
                              "description": desc, "isPartOf": {"@id": SITE["origin"] + "/#website"},
                              "about": {"@id": ORG_ID}, "inLanguage": "en-US"}] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    script_tags = "".join(f'<script src="/assets/js/{s}?v={ASSET_VER}" defer></script>' for s in ("site.js",) + tuple(scripts))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    t = html.escape(title)
    d = html.escape(desc)
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EVQS4TKQT9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-EVQS4TKQT9');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#6f1731">
<meta name="geo.region" content="US-TX"><meta name="geo.placename" content="The Colony">
<meta property="og:site_name" content="{SITE["name"]}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE["origin"]}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE["origin"]}/assets/img/{og_image}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&amp;family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&amp;display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_VER}">
{head_extra}<script type="application/ld+json">{ld}</script>
{script_tags}
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''


def page_hero(title_html, lead, image, alt, crumbs, actions=True, extra=""):
    trail = "".join(
        f'<li><a href="{u}">{html.escape(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{html.escape(n)}</li>'
        for i, (n, u) in enumerate(crumbs))
    act = (f'<div class="hero-actions"><a class="button light" href="/contact/">Get a free claim review {ARROW}</a>'
           f'<a class="button outline-light" href="tel:{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a></div>') if actions else ""
    return f'''<section class="page-hero"><div class="bg">{img(image, alt, lazy=False, priority=True, parallax=".12")}</div>
<div class="wrap"><nav aria-label="Breadcrumb"><ol class="crumbs">{trail}</ol></nav>
<h1 data-reveal>{title_html}</h1><p class="lead" data-reveal style="--d:120">{lead}</p>{extra}{act}</div></section>'''


def cta_band(title="Your claim deserves a closer look.", text=None):
    text = text or f"Talk with {SITE['name']} about the damage, the paperwork and your next step. The first review is free and there is no obligation."
    return f'''<section class="section tight"><div class="wrap"><div class="cta-band" data-reveal="zoom"><span class="blob a"></span><span class="blob b"></span>
<div><span class="eyebrow on-dark" style="color:var(--gold-2)">A clearer path forward</span><h2>{title}</h2><p>{text}</p></div>
<div class="actions"><a class="button light" href="/contact/">Request a free claim review {ARROW}</a><a class="button outline-light" href="tel:{SITE["phone_href"]}">{icon("phone")} Call {SITE["phone"]}</a></div>
</div></div></section>'''


def faq_block(faqs, open_first=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        o = " open" if (i == 0 and open_first) else ""
        out.append(f'<details{o}><summary>{html.escape(q)}</summary><div class="answer"><p>{a}</p></div></details>')
    return '<div class="faq" data-stagger>' + "".join(out) + "</div>"


def service_cards(items=SERVICES):
    out = []
    for i, s in enumerate(items, 1):
        out.append(f'''<a class="service-card" href="/services/{s["slug"]}/">{img(s["img"], s["img_alt"])}<span class="num">{i:02d}</span>
<span class="body"><h3>{s["name"]}</h3><p>{s["card"]}</p><span class="go">Explore this service {ARROW}</span></span></a>''')
    return '<div class="service-grid" data-stagger>' + "".join(out) + "</div>"


def fmt_date(iso):
    y, m, d = map(int, iso.split("-"))
    return date(y, m, d).strftime("%B %-d, %Y")


def blog_cards(posts):
    out = []
    for p in posts:
        out.append(f'''<article class="blog-card" data-category="{p["category"]}"><a class="thumb" href="/blog/{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(p["img"], p["img_alt"])}</a>
<div class="body"><div class="meta"><span class="cat">{p["category"]}</span><time datetime="{p["date"]}">{fmt_date(p["date"])}</time></div>
<h3><a href="/blog/{p["slug"]}/">{p["h1"][0].upper() + p["h1"][1:]}</a></h3><p>{p["excerpt"]}</p>
<a class="text-link" href="/blog/{p["slug"]}/">Read the guide {ARROW}</a></div></article>''')
    return "".join(out)


TOOLS = [
    {"slug": "deductible-calculator", "name": "Deductible calculator", "kicker": "Calculator", "icon": "percent",
     "short": "Turn a percentage deductible into dollars and compare it with a repair estimate."},
    {"slug": "claim-payment-calculator", "name": "Claim payment calculator", "kicker": "Calculator", "icon": "calculator",
     "short": "See how RCV, depreciation, your deductible and prior payments shape a claim payment."},
    {"slug": "depreciation-calculator", "name": "Depreciation calculator", "kicker": "Worksheet", "icon": "trend",
     "short": "Estimate actual cash value for roofs, flooring, appliances and more, item by item."},
    {"slug": "texas-claim-deadlines", "name": "Texas claim deadline calculator", "kicker": "Timeline", "icon": "calendar",
     "short": "Map the insurer response dates set by the Texas Prompt Payment of Claims Act."},
    {"slug": "claim-checklist", "name": "Claim preparation checklist", "kicker": "Checklist", "icon": "list",
     "short": "A 24-step, five-stage checklist that saves your progress and prints cleanly."},
    {"slug": "home-inventory", "name": "Home inventory builder", "kicker": "Organizer", "icon": "box",
     "short": "Build a room-by-room contents list with values, then export it to CSV."},
    {"slug": "claim-diary", "name": "Claim communication diary", "kicker": "Organizer", "icon": "message",
     "short": "Log every call, email and inspection with follow-up reminders."},
]
TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}


def tool_cards(items=TOOLS):
    return '<div class="tool-cards" data-stagger>' + "".join(
        f'<a class="tool-card" href="/tools/{t["slug"]}/"><span class="ico">{icon(t["icon"])}</span><span class="kicker">{t["kicker"]}</span>'
        f'<h3>{t["name"]}</h3><p>{t["short"]}</p><span class="text-link">Open the tool {ARROW}</span></a>' for t in items) + "</div>"


# --------------------------------------------------------------------------- writing
PAGES = []  # (path, html)


def write(path, content):
    PAGES.append(path)
    out = os.path.join(DIST, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(DIST, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)
    make_og_image()
    ctx = dict(SITE=SITE, SERVICES=SERVICES, SERVICE_BY_SLUG=SERVICE_BY_SLUG, POSTS=POSTS, POST_BY_SLUG=POST_BY_SLUG,
               TOOLS=TOOLS, TOOL_BY_SLUG=TOOL_BY_SLUG, render=render, page_hero=page_hero, cta_band=cta_band,
               faq_block=faq_block, service_cards=service_cards, blog_cards=blog_cards, tool_cards=tool_cards,
               icon=icon, img=img, ARROW=ARROW, breadcrumb_schema=breadcrumb_schema, faq_schema=faq_schema,
               fmt_date=fmt_date, TODAY=TODAY, write=write)
    P.build_all(ctx)
    write_sitemaps()
    make_zip()
    print(f"Built {len(PAGES)} pages into {DIST}")
    print(f"Zip: {ZIP} ({os.path.getsize(ZIP) // 1024} KB)")


def write_sitemaps():
    urls = [p for p in PAGES if p.endswith("/")]
    prio = lambda u: "1.0" if u == "/" else ("0.9" if u.count("/") == 3 and u.startswith("/services/") else "0.8" if u in ("/services/", "/contact/", "/tools/") else "0.7")
    items = "".join(f"<url><loc>{SITE['origin']}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio(u)}</priority></url>"
                    for u in urls if u not in ("/sitemap/",))
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + items + "</urlset>\n")


def make_og_image():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    src = os.path.join(STATIC, "assets", "img", "hero.webp")
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        tw, th = 1200, 630
        scale = max(tw / w, th / h)
        im = im.resize((int(w * scale) + 1, int(h * scale) + 1))
        left = (im.width - tw) // 2
        top = (im.height - th) // 2
        im = im.crop((left, top, left + tw, top + th))
        overlay = Image.new("RGBA", (tw, th))
        d = ImageDraw.Draw(overlay)
        for x in range(tw):
            a = int(235 * max(0.0, 1 - x / (tw * 0.85)))
            d.line([(x, 0), (x, th)], fill=(42, 11, 23, a))
        im = Image.alpha_composite(im.convert("RGBA"), overlay)
        d = ImageDraw.Draw(im)
        serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
        sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        try:
            f1 = ImageFont.truetype(serif, 64)
            f2 = ImageFont.truetype(sans, 28)
        except Exception:
            f1 = f2 = ImageFont.load_default()
        d.text((70, 190), "The Colony", font=f1, fill="white")
        d.text((70, 270), "Public Adjuster", font=f1, fill="white")
        d.rectangle([70, 370, 170, 376], fill=(226, 196, 143))
        d.text((70, 400), "Property claim help for homeowners", font=f2, fill=(241, 223, 229))
        d.text((70, 440), "and businesses  ·  (832) 503-5866", font=f2, fill=(241, 223, 229))
        im.convert("RGB").save(os.path.join(DIST, "assets", "img", "og-image.jpg"), quality=84)


def make_zip():
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _dirs, files in os.walk(DIST):
            for fn in sorted(files):
                full = os.path.join(base, fn)
                z.write(full, os.path.relpath(full, DIST))


if __name__ == "__main__":
    build()
