#!/usr/bin/env python3
"""Static site generator for rooftarp.com.

Renders every page from the shared layout in this file plus the page data in
content/. No WordPress, no runtime dependencies -- output is plain HTML.

    python3 build.py            # writes the site into ./ (rooftarp/)
    python3 validate.py         # verify the output

Why this rebuild exists
-----------------------
The WordPress site had 158 /service-areas/roof-tarp-<city>/ pages that were
96-98% identical to one another. Google's August 2026 spam update -- which
targeted scaled content abuse and doorway pages, and which explicitly called
out location pages that only change the city name -- completed its rollout on
21 August 2026. rooftarp.com lost roughly 80% of its impressions that day and
average position went from ~50 to ~85.

This build keeps the 17 metros that actually earned traffic, gives each one
genuinely distinct content, adds the service pages the old site never had, and
returns 410 for the 141 removed city URLs. validate.py fails the build if any
two pages drift back toward being near-duplicates.
"""

import os
import re
from datetime import date

from siteconfig import BIZ, NAV, FOOTER_SERVING, RESPONSE_WINDOW, TODAY
from content.services import SERVICES
from content.areas import AREAS
from content.blog import POSTS
from content.pages import ABOUT, FAQS_PAGE, CONTACT
from content.legal import LEGAL

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT

WRITTEN = []


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def esc(text):
    """Escape a string for use inside an HTML attribute."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def url(path):
    return BIZ["origin"].rstrip("/") + path


def json_str(s):
    """Escape a Python string for embedding in JSON-LD."""
    return (
        str(s)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("&mdash;", "—")
        .replace("&ndash;", "–")
        .replace("&amp;", "&")
        .replace("&hellip;", "…")
    )


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

def org_schema():
    areas = ", ".join(f'{{"@type":"City","name":"{a["city"]}, TX"}}' for a in AREAS)
    return f"""{{
"@type":"RoofingContractor",
"@id":"{url('/#business')}",
"name":"{BIZ['name']}",
"url":"{BIZ['origin']}/",
"telephone":"{BIZ['phone_display']}",
"email":"{BIZ['email']}",
"description":"24/7 emergency roof tarping across Texas. Storm, hail and tree damage covered fast to stop water entering while permanent repairs are arranged.",
"address":{{"@type":"PostalAddress","addressLocality":"{BIZ['city']}","addressRegion":"{BIZ['state']}","postalCode":"{BIZ['zip']}","addressCountry":"US"}},
"geo":{{"@type":"GeoCoordinates","latitude":"{BIZ['latitude']}","longitude":"{BIZ['longitude']}"}},
"areaServed":[{areas}],
"openingHoursSpecification":{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}},
"priceRange":"$$"
}}"""


def website_schema():
    return f"""{{
"@type":"WebSite",
"@id":"{url('/#website')}",
"url":"{BIZ['origin']}/",
"name":"{BIZ['name']}",
"publisher":{{"@id":"{url('/#business')}"}}
}}"""


def webpage_schema(page, wtype="WebPage"):
    return f"""{{
"@type":"{wtype}",
"@id":"{url(page['path'])}#webpage",
"url":"{url(page['path'])}",
"name":"{json_str(page['title'])}",
"description":"{json_str(page['description'])}",
"isPartOf":{{"@id":"{url('/#website')}"}},
"about":{{"@id":"{url('/#business')}"}}
}}"""


def crumb_schema(trail):
    items = [
        f'{{"@type":"ListItem","position":{i},"name":"{json_str(label)}","item":"{url(href)}"}}'
        for i, (label, href) in enumerate(trail, start=1)
    ]
    return '{"@type":"BreadcrumbList","itemListElement":[' + ",".join(items) + "]}"


def service_schema(page, area_name=None):
    served = area_name or f"{BIZ['state_long']}"
    return f"""{{
"@type":"Service",
"name":"{json_str(page.get('service_name', page['h1_plain']))}",
"serviceType":"{json_str(page.get('service_type', 'Roof Tarping'))}",
"provider":{{"@id":"{url('/#business')}"}},
"areaServed":{{"@type":"State","name":"{json_str(served)}"}},
"url":"{url(page['path'])}",
"description":"{json_str(page['description'])}"
}}"""


def faq_schema(faqs):
    items = [
        f'{{"@type":"Question","name":"{json_str(q)}","acceptedAnswer":{{"@type":"Answer","text":"{json_str(a)}"}}}}'
        for q, a in faqs
    ]
    return '{"@type":"FAQPage","mainEntity":[' + ",".join(items) + "]}"


def article_schema(page):
    return f"""{{
"@type":"BlogPosting",
"headline":"{json_str(page['h1_plain'])}",
"description":"{json_str(page['description'])}",
"datePublished":"{page['published']}",
"dateModified":"{page.get('modified', page['published'])}",
"author":{{"@id":"{url('/#business')}"}},
"publisher":{{"@id":"{url('/#business')}"}},
"mainEntityOfPage":{{"@id":"{url(page['path'])}#webpage"}}
}}"""


def itemlist_schema(name, items):
    els = [
        f'{{"@type":"ListItem","position":{i},"name":"{json_str(n)}","url":"{url(h)}"}}'
        for i, (n, h) in enumerate(items, start=1)
    ]
    return (
        f'{{"@type":"ItemList","name":"{json_str(name)}","itemListElement":['
        + ",".join(els)
        + "]}"
    )


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

def head(page):
    canonical = url(page["path"])
    og_image = url("/assets/img/site-icon-192x192.png")
    robots = page.get("robots", "index, follow")
    graph = ",\n".join(page.get("schema", []))
    article = ""
    if page.get("published"):
        mod = page.get("modified", page["published"])
        article = (
            f'<meta property="article:published_time" content="{page["published"]}">\n'
            f'<meta property="article:modified_time" content="{mod}">\n'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'article' if page.get('published') else 'website'}">
<meta property="og:site_name" content="{esc(BIZ['name'])}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
{article}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/assets/img/site-icon-32x32.png" sizes="32x32">
<link rel="icon" href="/assets/img/site-icon-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/site-icon-180x180.png">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{graph}
]}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active=None):
    def nav_link(label, href):
        cls = ' class="is-active"' if active == href else ""
        return f'<li><a href="{href}"{cls}>{label}</a></li>'

    links = "".join(nav_link(label, href) for label, href in NAV)
    return f"""<div class="announcement"><div class="container">
<span>24/7 emergency roof tarping across Texas</span>
<a class="announce-cta" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</div></div>
<header class="site-header"><div class="container header-inner">
<a class="brand" href="/"><span class="brand-mark">Roof</span>Tarp</a>
<button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle menu">
<span></span><span></span><span></span>
</button>
<nav class="site-nav" id="site-nav" aria-label="Main"><ul>{links}</ul></nav>
<a class="btn btn-emergency header-cta" href="tel:{BIZ['phone_href']}">Emergency Tarping</a>
</div></header>
<main id="main">
"""


def footer():
    service_links = "".join(
        f'<li><a href="/services/{s["slug"]}/">{s["nav_label"]}</a></li>' for s in SERVICES
    )
    area_links = "".join(
        f'<li><a href="/service-areas/{a["slug"]}/">{a["city"]}, TX</a></li>' for a in AREAS[:10]
    )
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div class="footer-col footer-brand">
<a class="brand" href="/"><span class="brand-mark">Roof</span>Tarp</a>
<p>Emergency roof tarping across Texas. We cover storm, hail and tree damage fast, so water stops
getting in while you arrange a permanent repair.</p>
<p class="footer-phone"><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></p>
<p><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
</div>
<div class="footer-col"><h3>Services</h3><ul>{service_links}</ul></div>
<div class="footer-col"><h3>Service Areas</h3><ul>{area_links}
<li><a href="/service-areas/">All service areas &rarr;</a></li></ul></div>
<div class="footer-col"><h3>Company</h3><ul>
<li><a href="/about/">About Us</a></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/faqs/">FAQs</a></li>
<li><a href="/contact/">Contact</a></li>
<li><a href="/sitemap/">Sitemap</a></li>
</ul></div>
</div>
<div class="footer-bottom">
<p>{FOOTER_SERVING}</p>
<p>&copy; {date.today().year} {BIZ['name']}. All rights reserved.
<a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms-of-use/">Terms of Use</a></p>
</div>
</div></footer>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def breadcrumbs(trail, current):
    links = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in trail)
    return (
        f'<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="container"><ol>'
        f'{links}<li aria-current="page">{current}</li></ol></div></nav>'
    )


def sub_hero(page):
    return f"""<section class="sub-hero"><div class="container">
<p class="eyebrow">{page.get('eyebrow', '')}</p>
<h1 id="page-title">{page['h1']}</h1>
<div class="sub-hero-intro">{page.get('hero_intro', page.get('intro', ''))}</div>
<div class="hero-actions">
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<a class="btn btn-ghost" href="/contact/">Request a callback</a>
</div>
</div></section>"""


def cta_band(heading, text):
    return f"""<section class="cta-band"><div class="container">
<h2>{heading}</h2>
<p>{text}</p>
<div class="hero-actions">
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<a class="btn btn-ghost" href="/contact/">Request a callback</a>
</div>
</div></section>"""


def faq_section(faqs, heading="Frequently asked questions"):
    items = "".join(
        f"""<details class="faq-item"><summary><h3>{q}</h3></summary><div class="faq-answer"><p>{a}</p></div></details>"""
        for q, a in faqs
    )
    return f"""<section class="faq-section"><div class="container">
<h2>{heading}</h2>
<div class="faq-list">{items}</div>
</div></section>"""


def write(path, html):
    """Write one file, creating directories as needed."""
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(html)
    WRITTEN.append(path)


def page_path(path):
    """URL path -> file path.

    The homepage is written as home.html, not index.html. The Hostinger H5G
    platform this deploys to ignores .htaccess and, when an index.html exists,
    answers every unknown path with it as a 200 -- which would turn the 141
    removed city URLs into soft-404s serving the homepage. index.php (see
    build_index_php) serves home.html for "/" and real 404/410s otherwise.
    """
    if path == "/":
        return "home.html"
    return path.strip("/") + "/index.html"


# --------------------------------------------------------------------------
# Home
# --------------------------------------------------------------------------

def build_home():
    page = {
        "path": "/",
        "title": "Roof Tarp | 24/7 Emergency Roof Tarping Services in Texas",
        "description": (
            "Emergency roof tarping across Texas, 24/7. Storm, hail and tree damage covered fast to "
            "stop water getting in. Call (512) 297-7580."
        ),
    }
    faqs = [
        ("How fast can you get a roof tarp installed?",
         "We dispatch 24 hours a day and aim to be on site " + RESPONSE_WINDOW + ". Timing depends on "
         "distance, how many calls a storm has generated in that metro, and whether conditions are safe "
         "to work in."),
        ("Do you work at night and on weekends?",
         "Yes. Dispatch runs around the clock including holidays. Most roofs fail outside business "
         "hours, which is exactly when it matters most."),
        ("Does insurance cover emergency roof tarping?",
         "Usually. Most homeowner policies also require you to take reasonable steps to prevent further "
         "damage after a covered loss, which is what tarping does. Keep the invoice and the photographs."),
        ("How long will a roof tarp last?",
         "A standard tarp properly anchored lasts days to a few weeks. Heavy-duty UV-stabilised "
         "material installed for the long term runs several months to around a year in Texas sun."),
        ("Do you have to put holes in my roof?",
         "Not always. On tile, slate and metal we use ballasted, no-penetration anchoring as standard. "
         "On asphalt shingle, board-wrapped fastening is usually most secure, and the holes are dealt "
         "with at repair."),
        ("What areas of Texas do you cover?",
         "We work statewide, with detailed coverage across Houston, Dallas, Fort Worth, Austin, San "
         "Antonio, El Paso, Lubbock, Corpus Christi and a dozen more metros. If your town is not "
         "listed, call anyway."),
    ]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), faq_schema(faqs)]

    service_cards = "".join(
        f"""<article class="service-card">
<div class="service-num">{i:02d}</div>
<h3><a href="/services/{s['slug']}/">{s['nav_label']}</a></h3>
<p>{s['card']}</p>
<a class="service-link" href="/services/{s['slug']}/">{s['card_cta']} &rarr;</a>
</article>"""
        for i, s in enumerate(SERVICES, start=1)
    )

    area_cards = "".join(
        f"""<a class="link-card" href="/service-areas/{a['slug']}/">
<h3>{a['city']}, TX</h3>
<p>{a['blurb']}</p>
<span class="service-link">{a['city']} tarping &rarr;</span>
</a>"""
        for a in AREAS
    )

    post_cards = "".join(
        f"""<a class="link-card post-card" href="/blog/{p['slug']}/">
<span class="post-date">{p['published']}</span>
<h3>{p['h1_plain']}</h3>
<p>{p['excerpt']}</p>
<span class="service-link">Read the guide &rarr;</span>
</a>"""
        for p in POSTS[:3]
    )

    html = head(page) + header("/") + f"""
<section class="hero" id="top" aria-labelledby="page-title"><div class="container">
<div class="hero-copy">
<p class="eyebrow">24/7 Emergency Response &mdash; Texas</p>
<h1 id="page-title">Roof Tarping Services &mdash; <span class="accent-text">24/7 Emergency Service</span></h1>
<p class="hero-lead">When a storm opens up your roof, the damage stops growing the moment the water
stops getting in. We install secured emergency tarps across Texas, day or night, so a bad night does
not turn into a rebuild.</p>
<div class="hero-actions">
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<a class="btn btn-ghost" href="/contact/">Request a callback</a>
</div>
<ul class="hero-points">
<li>Dispatch answered 24/7, including holidays</li>
<li>On site {RESPONSE_WINDOW}</li>
<li>Photographed and documented for your claim</li>
<li>Price agreed before work starts</li>
</ul>
</div>
</div></section>

<section class="section" id="process"><div class="container">
<p class="eyebrow">Our Simple Process</p>
<h2>What happens when you call</h2>
<div class="process-grid">
<div class="process-step"><span class="step-num">Step 1</span><h3>Call us anytime</h3>
<p>Tell us what happened, roughly how big the damage is, whether anything is still on the roof, and
whether water is coming into living space right now. That decides what we bring and how fast we move.</p></div>
<div class="process-step"><span class="step-num">Step 2</span><h3>We assess the damage</h3>
<p>On arrival we check the structure is safe to work on, find the full extent of the breach &mdash;
usually larger than the visible hole &mdash; and photograph everything before anything is covered.</p></div>
<div class="process-step"><span class="step-num">Step 3</span><h3>We install the tarp</h3>
<p>Sized well past the damage, anchored by the method your roof covering needs, every edge sealed or
weighted. Nothing left flapping, because that is how covers fail.</p></div>
<div class="process-step"><span class="step-num">Step 4</span><h3>You get the documentation</h3>
<p>Dated photographs before, during and after, plus an itemised invoice. That is what your insurer
needs to see as evidence of both the damage and the mitigation.</p></div>
</div>
</div></section>

<section class="section section-alt" id="services"><div class="container">
<p class="eyebrow">Our Roof Tarping Services</p>
<h2>Tarping, specified for the situation</h2>
<p class="section-intro">An overnight emergency cover and a tarp that has to survive a four-month
insurance process are different jobs. We will tell you which one you need.</p>
<div class="service-grid">{service_cards}</div>
</div></section>

<section class="section" id="why"><div class="container">
<p class="eyebrow">Why Roof Tarp</p>
<h2>We do one thing, and we do it around the clock</h2>
<div class="feature-grid">
<div class="feature"><h3>24/7 availability</h3><p>Roofs fail at night and at weekends. Dispatch is
staffed 24 hours, including holidays, because waiting until Monday is how a contained loss spreads.</p></div>
<div class="feature"><h3>Tarping specialists</h3><p>For a general roofer a tarp is an unbilled
inconvenience. For us it is the job &mdash; right material, right sizes, right anchoring for your roof
covering.</p></div>
<div class="feature"><h3>Statewide capacity</h3><p>Texas storm seasons are staggered, so crews move
toward whichever metro was actually hit &mdash; which matters when every local roofer is booked out.</p></div>
<div class="feature"><h3>Transparent pricing</h3><p>You get a figure before work starts, not an
invoice afterwards.</p></div>
<div class="feature"><h3>Claim-ready documentation</h3><p>Photographs before, during and after, plus
an itemised invoice. Adjusters move fastest on files with clear dated evidence.</p></div>
<div class="feature"><h3>Straight answers</h3><p>If what you are describing does not need a tarp
tonight, we will say so rather than dispatch a crew you do not need.</p></div>
</div>
</div></section>

<section class="section section-alt" id="areas"><div class="container">
<p class="eyebrow">Service Areas</p>
<h2>Where we work across Texas</h2>
<p class="section-intro">Each metro has its own storm profile &mdash; Gulf tropical systems on the
coast, hail alley through DFW and I-35, High Plains wind in Lubbock, pine fall in the Piney Woods.
The method changes accordingly.</p>
<div class="link-grid">{area_cards}</div>
</div></section>

<section class="section" id="blog"><div class="container">
<p class="eyebrow">Latest Articles</p>
<h2>Guides to roof tarping</h2>
<div class="link-grid">{post_cards}</div>
<p class="section-more"><a class="service-link" href="/blog/">Read the blog &rarr;</a></p>
</div></section>

""" + faq_section(faqs) + cta_band(
        "Roof open? Call now.",
        "Dispatch is answered 24 hours a day, seven days a week, across Texas.",
    ) + footer()
    write(page_path("/"), html)


# --------------------------------------------------------------------------
# Services
# --------------------------------------------------------------------------

def build_services_index():
    page = {
        "path": "/services/",
        "title": "Roof Tarping Services | Emergency & Long-Term | Roof Tarp",
        "description": (
            "Roof tarping services across Texas: emergency, long-term, residential, commercial, storm "
            "and hail damage tarping. Call (512) 297-7580."
        ),
        "h1": 'Roof Tarping <span class="accent-text">Services</span>',
        "h1_plain": "Roof Tarping Services",
        "eyebrow": "What We Do",
        "hero_intro": (
            "Every tarping job is specified by two things: what the roof is covered with, and how long "
            "the cover has to last. Those two answers decide the material and the anchoring method."
        ),
    }
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page, "CollectionPage"),
        crumb_schema(trail + [("Services", "/services/")]),
        itemlist_schema(
            "Roof Tarping Services",
            [(s["h1_plain"], f"/services/{s['slug']}/") for s in SERVICES],
        ),
    ]
    cards = "".join(
        f"""<article class="service-card">
<div class="service-num">{i:02d}</div>
<h3><a href="/services/{s['slug']}/">{s['nav_label']}</a></h3>
<p>{s['card']}</p>
<a class="service-link" href="/services/{s['slug']}/">{s['card_cta']} &rarr;</a>
</article>"""
        for i, s in enumerate(SERVICES, start=1)
    )
    html = (
        head(page)
        + header("/services/")
        + breadcrumbs(trail, "Services")
        + sub_hero(page)
        + f"""<section class="section"><div class="container">
<div class="service-grid">{cards}</div>
</div></section>
<section class="section section-alt"><div class="container prose">
<h2>Emergency or long-term?</h2>
<p>It comes down to the realistic gap between now and the permanent repair.</p>
<p>Under about two weeks &mdash; a contractor is booked, materials are in stock, nothing is waiting on
an adjuster &mdash; a standard tarp correctly anchored is the right answer and the cost-effective one.</p>
<p>Beyond a month &mdash; an insurance process, a material lead time, a post-storm backlog, a permit
&mdash; UV degradation and repeated wind loading become the limiting factor. Installing a lightweight
cover in that situation means paying for the job twice, and usually discovering the failure during the
storm you needed it for.</p>
<p>We will tell you which situation you are in. If you are not sure, describe the timeline on the phone
and we will give you a straight answer.</p>
</div></section>"""
        + cta_band(
            "Not sure what you need?",
            "Call and describe the damage. If it does not need a tarp tonight, we will tell you.",
        )
        + footer()
    )
    write(page_path("/services/"), html)


def build_services():
    for s in SERVICES:
        path = f"/services/{s['slug']}/"
        page = dict(s)
        page["path"] = path
        trail = [("Home", "/"), ("Services", "/services/")]
        page["schema"] = [
            org_schema(),
            webpage_schema(page),
            crumb_schema(trail + [(s["h1_plain"], path)]),
            service_schema(page),
            faq_schema(s["faqs"]),
        ]
        related = "".join(
            f'<li><a href="/services/{o["slug"]}/">{o["nav_label"]}</a></li>'
            for o in SERVICES
            if o["slug"] != s["slug"]
        )
        html = (
            head(page)
            + header("/services/")
            + breadcrumbs(trail, s["h1_plain"])
            + sub_hero(page)
            + f"""<section class="section"><div class="container content-layout">
<article class="prose">{s['body']}</article>
<aside class="sidebar">
<div class="sidebar-card sidebar-cta">
<h3>Need this now?</h3>
<p>Dispatch is answered 24 hours a day across Texas.</p>
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</div>
<div class="sidebar-card">
<h3>Other services</h3>
<ul class="sidebar-list">{related}</ul>
</div>
<div class="sidebar-card">
<h3>Where we work</h3>
<p>Emergency tarping across Texas, from the Gulf coast to the High Plains.</p>
<a class="service-link" href="/service-areas/">See service areas &rarr;</a>
</div>
</aside>
</div></section>"""
            + faq_section(s["faqs"])
            + cta_band(
                "Get it covered before the next front.",
                "Call " + BIZ["phone_short"] + " &mdash; 24 hours a day, seven days a week.",
            )
            + footer()
        )
        write(page_path(path), html)


# --------------------------------------------------------------------------
# Service areas
# --------------------------------------------------------------------------

def build_areas_index():
    page = {
        "path": "/service-areas/",
        "title": "Service Areas | Texas Roof Tarping Coverage | Roof Tarp",
        "description": (
            "Emergency roof tarping across Texas: Houston, Dallas, Fort Worth, Austin, San Antonio, "
            "El Paso, Lubbock, Corpus Christi and more. Call (512) 297-7580."
        ),
        "h1": 'Texas <span class="accent-text">Service Areas</span>',
        "h1_plain": "Texas Service Areas",
        "eyebrow": "Where We Work",
        "hero_intro": (
            "Texas is not one roofing climate, it is several. What damages a roof in Corpus Christi is "
            "not what damages one in Lubbock, and the tarping method changes with it."
        ),
    }
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page, "CollectionPage"),
        crumb_schema(trail + [("Service Areas", "/service-areas/")]),
        itemlist_schema(
            "Texas Service Areas",
            [(f"{a['city']}, TX", f"/service-areas/{a['slug']}/") for a in AREAS],
        ),
    ]
    cards = "".join(
        f"""<a class="link-card" href="/service-areas/{a['slug']}/">
<h3>{a['city']}, TX</h3>
<p class="card-county">{a['county']}</p>
<p>{a['blurb']}</p>
<span class="service-link">{a['city']} tarping &rarr;</span>
</a>"""
        for a in AREAS
    )
    html = (
        head(page)
        + header("/service-areas/")
        + breadcrumbs(trail, "Service Areas")
        + sub_hero(page)
        + f"""<section class="section"><div class="container">
<div class="link-grid">{cards}</div>
</div></section>
<section class="section section-alt"><div class="container prose">
<h2>Why the metro matters</h2>
<p>A roof tarp is specified for the weather it has to survive, and Texas weather is regional to an
unusual degree.</p>
<ul>
<li><strong>The Gulf coast</strong> &mdash; Houston, Corpus Christi, Beaumont &mdash; takes tropical
systems that load a roof for hours with the wind direction reversing as the centre passes. Anchoring
has to hold from every direction, and coastal salt corrodes ordinary fastenings.</li>
<li><strong>Hail alley</strong> &mdash; DFW, the I-35 corridor, Waco &mdash; sees narrow, intense hail
swaths. Damage is often invisible from the ground and concentrated on a street or two.</li>
<li><strong>The High Plains and Permian Basin</strong> &mdash; Lubbock, Midland &mdash; is flat and
open, so wind arrives unobstructed. Standard anchor spacing that works elsewhere does not hold here.</li>
<li><strong>The desert</strong> &mdash; El Paso &mdash; has flat roofs, violent monsoon bursts and the
harshest UV in the state, which shortens tarp life dramatically.</li>
<li><strong>The Piney Woods</strong> &mdash; The Woodlands, Huntsville &mdash; is tree-fall country.
Damage is concentrated point impact, often with the tree still in place.</li>
</ul>
<p>If your town is not listed, call anyway. These are the metros we are asked for most often, not the
limit of where we work.</p>
</div></section>"""
        + cta_band(
            "Wherever you are in Texas.",
            "Call " + BIZ["phone_short"] + " and we will tell you honestly how fast we can reach you.",
        )
        + footer()
    )
    write(page_path("/service-areas/"), html)


def build_areas():
    for a in AREAS:
        path = f"/service-areas/{a['slug']}/"
        page = dict(a)
        page["path"] = path
        page["h1"] = f'Roof Tarp <span class="accent-text">{a["city"]}, TX</span>'
        page["h1_plain"] = f"Roof Tarp {a['city']}, TX"
        page["eyebrow"] = f"{a['county']}"
        trail = [("Home", "/"), ("Service Areas", "/service-areas/")]
        page["schema"] = [
            org_schema(),
            webpage_schema(page),
            crumb_schema(trail + [(page["h1_plain"], path)]),
            service_schema(
                {
                    "path": path,
                    "description": a["description"],
                    "h1_plain": page["h1_plain"],
                    "service_name": f"Emergency Roof Tarping in {a['city']}, TX",
                    "service_type": "Emergency Roof Tarping",
                },
                area_name=f"{a['city']}, Texas",
            ),
            faq_schema(a["faqs"]),
        ]
        others = "".join(
            f'<li><a href="/service-areas/{o["slug"]}/">{o["city"]}, TX</a></li>'
            for o in AREAS
            if o["slug"] != a["slug"]
        )
        services = "".join(
            f'<li><a href="/services/{s["slug"]}/">{s["nav_label"]}</a></li>' for s in SERVICES[:5]
        )
        html = (
            head(page)
            + header("/service-areas/")
            + breadcrumbs(trail, page["h1_plain"])
            + sub_hero(page)
            + f"""<section class="section"><div class="container content-layout">
<article class="prose">
{a['storm_profile']}
{a['local_detail']}
<h2>What we cover in {a['city']}</h2>
<p>The full range of tarping work, specified for {a['county']} conditions:
<a href="/services/emergency-roof-tarping/">emergency tarping</a> when the roof is open and rain is
coming, <a href="/services/long-term-roof-tarping/">long-term tarping</a> when the repair is months
away, and <a href="/services/commercial-roof-tarping/">commercial tarping</a> for flat and low-slope
buildings. Dispatch is answered 24 hours a day.</p>
</article>
<aside class="sidebar">
<div class="sidebar-card sidebar-cta">
<h3>{a['city']} emergency line</h3>
<p>Answered 24 hours a day, seven days a week.</p>
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</div>
<div class="sidebar-card">
<h3>Services</h3>
<ul class="sidebar-list">{services}
<li><a href="/services/">All services &rarr;</a></li></ul>
</div>
<div class="sidebar-card">
<h3>Other Texas areas</h3>
<ul class="sidebar-list">{others}</ul>
</div>
</aside>
</div></section>"""
            + faq_section(a["faqs"], f"{a['city']} roof tarping questions")
            + cta_band(
                f"Roof damage in {a['city']}?",
                "Call " + BIZ["phone_short"] + " &mdash; dispatch is staffed around the clock.",
            )
            + footer()
        )
        write(page_path(path), html)


# --------------------------------------------------------------------------
# Blog
# --------------------------------------------------------------------------

def build_blog_index():
    page = {
        "path": "/blog/",
        "title": "Roof Tarping Guides & Advice | Roof Tarp Blog",
        "description": (
            "Practical guides to roof tarping: materials, installation without nails, how long tarps "
            "last, and protecting your home after roof failure."
        ),
        "h1": 'Roof Tarping <span class="accent-text">Guides</span>',
        "h1_plain": "Roof Tarping Guides",
        "eyebrow": "Blog",
        "hero_intro": (
            "Practical, specific guidance on tarping a roof and keeping water out while you wait for a "
            "permanent repair."
        ),
    }
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page, "CollectionPage"),
        crumb_schema(trail + [("Blog", "/blog/")]),
        itemlist_schema("Roof Tarping Guides", [(p["h1_plain"], f"/blog/{p['slug']}/") for p in POSTS]),
    ]
    cards = "".join(
        f"""<a class="link-card post-card" href="/blog/{p['slug']}/">
<span class="post-date">{p['published']}</span>
<h3>{p['h1_plain']}</h3>
<p>{p['excerpt']}</p>
<span class="service-link">Read the guide &rarr;</span>
</a>"""
        for p in POSTS
    )
    html = (
        head(page)
        + header("/blog/")
        + breadcrumbs(trail, "Blog")
        + sub_hero(page)
        + f"""<section class="section"><div class="container">
<div class="link-grid">{cards}</div>
</div></section>"""
        + cta_band(
            "Rather have someone else do it?",
            "Call " + BIZ["phone_short"] + " for emergency tarping anywhere in Texas.",
        )
        + footer()
    )
    write(page_path("/blog/"), html)


def build_posts():
    for i, p in enumerate(POSTS):
        path = f"/blog/{p['slug']}/"
        page = dict(p)
        page["path"] = path
        page["h1"] = p["h1_plain"]
        page["eyebrow"] = "Guide"
        trail = [("Home", "/"), ("Blog", "/blog/")]
        page["schema"] = [
            org_schema(),
            webpage_schema(page, "WebPage"),
            crumb_schema(trail + [(p["h1_plain"], path)]),
            article_schema(page),
            faq_schema(p["faqs"]),
        ]
        others = "".join(
            f'<li><a href="/blog/{o["slug"]}/">{o["h1_plain"]}</a></li>'
            for o in POSTS
            if o["slug"] != p["slug"]
        )[:2000]
        html = (
            head(page)
            + header("/blog/")
            + breadcrumbs(trail, p["h1_plain"])
            + f"""<section class="sub-hero post-hero"><div class="container">
<p class="eyebrow">Guide &middot; {p['published']}</p>
<h1 id="page-title">{p['h1_plain']}</h1>
<p class="sub-hero-intro">{p['description']}</p>
</div></section>
<section class="section"><div class="container content-layout">
<article class="prose">
{p['body']}
</article>
<aside class="sidebar">
<div class="sidebar-card sidebar-cta">
<h3>Need a tarp installed?</h3>
<p>Emergency tarping across Texas, 24 hours a day.</p>
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</div>
<div class="sidebar-card">
<h3>More guides</h3>
<ul class="sidebar-list">{others}</ul>
</div>
</aside>
</div></section>"""
            + faq_section(p["faqs"])
            + cta_band(
                "Want it done properly?",
                "Call " + BIZ["phone_short"] + " &mdash; we tarp roofs across Texas, day or night.",
            )
            + footer()
        )
        write(page_path(path), html)


# --------------------------------------------------------------------------
# About / FAQs / Contact
# --------------------------------------------------------------------------

def build_about():
    page = dict(ABOUT)
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page, "AboutPage"),
        crumb_schema(trail + [("About", "/about/")]),
    ]
    html = (
        head(page)
        + header("/about/")
        + breadcrumbs(trail, "About")
        + sub_hero(page)
        + f"""<section class="section"><div class="container prose">{ABOUT['body']}</div></section>"""
        + cta_band("Talk to us.", "Call " + BIZ["phone_short"] + " any time, day or night.")
        + footer()
    )
    write(page_path("/about/"), html)


def build_faqs():
    page = dict(FAQS_PAGE)
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page),
        crumb_schema(trail + [("FAQs", "/faqs/")]),
        faq_schema(FAQS_PAGE["faqs"]),
    ]
    html = (
        head(page)
        + header("/faqs/")
        + breadcrumbs(trail, "FAQs")
        + sub_hero(page)
        + faq_section(FAQS_PAGE["faqs"], "Roof tarping questions")
        + cta_band(
            "Question not answered?",
            "Call " + BIZ["phone_short"] + " and ask. We will give you a straight answer.",
        )
        + footer()
    )
    write(page_path("/faqs/"), html)


def build_contact():
    page = dict(CONTACT)
    trail = [("Home", "/")]
    page["schema"] = [
        org_schema(),
        webpage_schema(page, "ContactPage"),
        crumb_schema(trail + [("Contact", "/contact/")]),
    ]
    html = (
        head(page)
        + header("/contact/")
        + breadcrumbs(trail, "Contact")
        + sub_hero(page)
        + f"""<section class="section"><div class="container content-layout">
<article class="prose">{CONTACT['body']}</article>
<aside class="sidebar">
<div class="sidebar-card sidebar-cta">
<h3>Emergency line</h3>
<p>24 hours a day, seven days a week, including holidays.</p>
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</div>
<div class="sidebar-card">
<h3>Request a callback</h3>
<form class="callback-form" method="post" action="#" data-unwired="true">
<label for="cb-name">Name</label>
<input id="cb-name" name="name" type="text" autocomplete="name" required>
<label for="cb-phone">Phone</label>
<input id="cb-phone" name="phone" type="tel" autocomplete="tel" required>
<label for="cb-email">Email</label>
<input id="cb-email" name="email" type="email" autocomplete="email">
<label for="cb-zip">ZIP code</label>
<input id="cb-zip" name="zip" type="text" inputmode="numeric" autocomplete="postal-code">
<label for="cb-msg">What happened?</label>
<textarea id="cb-msg" name="message" rows="4"></textarea>
<button class="btn btn-emergency" type="submit">Send request</button>
<p class="form-note">For an active leak, please call instead &mdash; it is faster.</p>
</form>
</div>
</aside>
</div></section>"""
        + footer()
    )
    write(page_path("/contact/"), html)


# --------------------------------------------------------------------------
# Legal, sitemap page, 404
# --------------------------------------------------------------------------

def build_legal():
    for item in LEGAL:
        page = dict(item)
        page["robots"] = "noindex, follow"
        page["eyebrow"] = "Legal"
        trail = [("Home", "/")]
        page["schema"] = [org_schema(), webpage_schema(page)]
        html = (
            head(page)
            + header()
            + breadcrumbs(trail, item["h1_plain"])
            + f"""<section class="sub-hero"><div class="container">
<p class="eyebrow">Legal</p><h1 id="page-title">{item['h1']}</h1>
</div></section>
<section class="section"><div class="container prose">{item['body']}</div></section>"""
            + footer()
        )
        write(page_path(item["path"]), html)


def build_sitemap_page():
    page = {
        "path": "/sitemap/",
        "title": "Sitemap | Roof Tarp",
        "description": (
            "Every page on rooftarp.com in one place: tarping services, Texas service areas, "
            "guides and company information."
        ),
        "h1": "Sitemap",
        "h1_plain": "Sitemap",
        "eyebrow": "All Pages",
    }
    page["schema"] = [org_schema(), webpage_schema(page)]
    services = "".join(
        f'<li><a href="/services/{s["slug"]}/">{s["h1_plain"]}</a></li>' for s in SERVICES
    )
    areas = "".join(
        f'<li><a href="/service-areas/{a["slug"]}/">Roof Tarp {a["city"]}, TX</a></li>' for a in AREAS
    )
    posts = "".join(f'<li><a href="/blog/{p["slug"]}/">{p["h1_plain"]}</a></li>' for p in POSTS)
    html = (
        head(page)
        + header()
        + breadcrumbs([("Home", "/")], "Sitemap")
        + f"""<section class="sub-hero"><div class="container">
<p class="eyebrow">All Pages</p><h1 id="page-title">Sitemap</h1>
</div></section>
<section class="section"><div class="container prose">
<h2>Main pages</h2>
<ul>
<li><a href="/">Home</a></li>
<li><a href="/services/">Services</a></li>
<li><a href="/service-areas/">Service Areas</a></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/about/">About</a></li>
<li><a href="/faqs/">FAQs</a></li>
<li><a href="/contact/">Contact</a></li>
</ul>
<h2>Services</h2><ul>{services}</ul>
<h2>Service areas</h2><ul>{areas}</ul>
<h2>Guides</h2><ul>{posts}</ul>
<h2>Legal</h2>
<ul><li><a href="/privacy-policy/">Privacy Policy</a></li>
<li><a href="/terms-of-use/">Terms of Use</a></li></ul>
</div></section>"""
        + footer()
    )
    write(page_path("/sitemap/"), html)


def build_404():
    page = {
        "path": "/404.html",
        "title": "Page Not Found | Roof Tarp",
        "description": "That page does not exist. Find roof tarping services and service areas here.",
        "h1": "Page not found",
        "h1_plain": "Page not found",
        "robots": "noindex, follow",
    }
    page["schema"] = [org_schema(), webpage_schema(page)]
    html = (
        head(page)
        + header()
        + f"""<section class="sub-hero"><div class="container">
<p class="eyebrow">404</p>
<h1 id="page-title">Page not found</h1>
<p class="sub-hero-intro">That page does not exist. If you were looking for a city page, we have
consolidated our service areas &mdash; the metros we cover are listed below.</p>
<div class="hero-actions">
<a class="btn btn-emergency" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<a class="btn btn-ghost" href="/service-areas/">Service areas</a>
</div>
</div></section>
<section class="section"><div class="container prose">
<h2>Try one of these</h2>
<ul>
<li><a href="/services/emergency-roof-tarping/">Emergency roof tarping</a></li>
<li><a href="/services/">All tarping services</a></li>
<li><a href="/service-areas/">Texas service areas</a></li>
<li><a href="/blog/">Roof tarping guides</a></li>
<li><a href="/contact/">Contact us</a></li>
</ul>
</div></section>"""
        + footer()
    )
    write("404.html", html)


# --------------------------------------------------------------------------
# sitemap.xml, robots.txt, .htaccess
# --------------------------------------------------------------------------

def all_urls():
    """(path, lastmod) for every indexable page, in sitemap order."""
    urls = [("/", TODAY), ("/services/", TODAY)]
    urls += [(f"/services/{s['slug']}/", TODAY) for s in SERVICES]
    urls += [("/service-areas/", TODAY)]
    urls += [(f"/service-areas/{a['slug']}/", TODAY) for a in AREAS]
    urls += [("/blog/", TODAY)]
    urls += [(f"/blog/{p['slug']}/", p.get("modified", p["published"])) for p in POSTS]
    urls += [("/about/", TODAY), ("/faqs/", TODAY), ("/contact/", TODAY), ("/sitemap/", TODAY)]
    return urls


def build_sitemap_xml():
    entries = "".join(
        f"<url><loc>{url(p)}</loc><lastmod>{m}</lastmod></url>\n" for p, m in all_urls()
    )
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n",
    )


def build_robots():
    write(
        "robots.txt",
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /templates/\n"
        "Disallow: /home.html\n"
        "\n"
        f"Sitemap: {url('/sitemap.xml')}\n",
    )


def pruned_slugs():
    """City slugs on the old WordPress site that are not rebuilt here.

    Read from prune-list.txt, which is generated from the Search Console export:
    every /service-areas/roof-tarp-<city>/ page that earned zero clicks in the
    16 months to 2026-09-19. These return 410 Gone so Google drops them rather
    than treating them as a soft 404 or, worse, keeping them in the index as
    part of the doorway pattern that caused the demotion.
    """
    fp = os.path.join(ROOT, "prune-list.txt")
    if not os.path.exists(fp):
        return []
    keep = {a["slug"] for a in AREAS}
    out = []
    with open(fp, encoding="utf-8") as fh:
        for line in fh:
            slug = line.strip()
            if slug and not slug.startswith("#") and slug not in keep:
                out.append(slug)
    return out


def build_htaccess():
    slugs = pruned_slugs()
    lines = [
        "# Generated by build.py - do not edit by hand.",
        "",
        "Options -Indexes",
        "DirectoryIndex index.html",
        "",
        "<IfModule mod_rewrite.c>",
        "RewriteEngine On",
        "",
        "# Canonical host and scheme",
        "RewriteCond %{HTTPS} off [OR]",
        "RewriteCond %{HTTP_HOST} ^www\\. [NC]",
        "RewriteRule ^(.*)$ https://rooftarp.com/$1 [R=301,L]",
        "",
    ]
    if slugs:
        lines += [
            f"# {len(slugs)} removed near-duplicate city pages -> 410 Gone.",
            "# These earned zero clicks in the 16 months to 2026-09-19 and were",
            "# 96-98% identical to one another. 410 tells Google they are",
            "# intentionally gone, which de-indexes them faster than a 404.",
        ]
        for i in range(0, len(slugs), 20):
            chunk = "|".join(slugs[i : i + 20])
            lines.append(f"RewriteRule ^service-areas/({chunk})/?$ - [G,L]")
        lines += [""]
    lines += [
        "# Legacy WordPress paths",
        "RewriteRule ^(wp-admin|wp-includes|wp-login\\.php|xmlrpc\\.php) - [G,L]",
        "RewriteRule ^(sitemap_index|page-sitemap|post-sitemap|category-sitemap)\\.xml$ /sitemap.xml [R=301,L]",
        "</IfModule>",
        "",
        "ErrorDocument 404 /404.html",
        "",
        "<IfModule mod_expires.c>",
        "ExpiresActive On",
        "ExpiresByType text/css A31557600",
        "ExpiresByType application/javascript A31557600",
        "ExpiresByType image/webp A31557600",
        "ExpiresByType image/png A31557600",
        "ExpiresByType image/svg+xml A31557600",
        "</IfModule>",
        "",
    ]
    write(".htaccess", "\n".join(lines))


# --------------------------------------------------------------------------

def build_index_php():
    """Front controller for the Hostinger H5G platform.

    The platform serves existing files directly, ignores .htaccess, and routes
    "/" and every unknown path here (provided no index.html exists). This is
    therefore the only place that can enforce the canonical host, return 410
    for the removed city pages, and give a real 404 for everything else.
    .htaccess is still generated for portability to Apache hosts.
    """
    slugs = pruned_slugs()
    php_slugs = ",\n".join(f"    '{s}'" for s in slugs)
    write("/index.php", f"""<?php
// rooftarp.com - static site front controller. See README, "Hosting note".
// Generated by build.py - do not edit by hand.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://rooftarp.com';

// Canonical host and scheme. TLS terminates upstream, so REQUEST_SCHEME is
// always http here; X-Forwarded-Proto carries the real scheme.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.rooftarp.com') {{
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}}

if ($path === '/' || $path === '/index.php') {{
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}}

// {len(slugs)} removed near-duplicate city pages -> 410 Gone. These earned zero
// clicks in 16 months and were 96-98% identical to one another; 410 tells
// Google they are intentionally gone. Kept city pages exist as real files
// and never reach this controller.
$gone = [
{php_slugs}
];
if (preg_match('#^/service-areas/([a-z0-9-]+)/?$#', $path, $m) && in_array($m[1], $gone, true)) {{
    http_response_code(410);
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/404.html');
    exit;
}}

// Legacy WordPress paths.
if (preg_match('#^/(wp-admin|wp-includes|wp-login\\.php|xmlrpc\\.php|wp-json)(/|$)#', $path)) {{
    http_response_code(410);
    exit;
}}
if (preg_match('#^/(sitemap_index|page-sitemap|post-sitemap|category-sitemap)\\.xml$#', $path)) {{
    header('Location: ' . $home . '/sitemap.xml', true, 301);
    exit;
}}
if (preg_match('#^/(feed|comments/feed|category/blog)/?$#', $path)) {{
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}}

// Directory requested without its trailing slash.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {{
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
""")


#: Directories whose contents build.py owns completely. Anything under these
#: that the current build did not write is stale and gets removed.
GENERATED_TREES = ["services", "service-areas", "blog"]


def prune_stale():
    """Delete generated pages that are no longer part of the build.

    Without this, removing a city from content/areas.py leaves its directory
    on disk, it gets deployed again, and it stays indexed -- which on this site
    is the precise failure we are trying to undo. Returns the removed paths.
    """
    written = {os.path.normpath(os.path.join(OUT, p.lstrip("/"))) for p in WRITTEN}
    removed = []
    for tree in GENERATED_TREES:
        base = os.path.join(OUT, tree)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            d = os.path.join(base, entry)
            if not os.path.isdir(d):
                continue
            index = os.path.normpath(os.path.join(d, "index.html"))
            if index not in written:
                for root, dirs, files in os.walk(d, topdown=False):
                    for f in files:
                        os.remove(os.path.join(root, f))
                    for sub in dirs:
                        os.rmdir(os.path.join(root, sub))
                os.rmdir(d)
                removed.append(f"/{tree}/{entry}/")
    return removed


def main():
    build_home()
    build_services_index()
    build_services()
    build_areas_index()
    build_areas()
    build_blog_index()
    build_posts()
    build_about()
    build_faqs()
    build_contact()
    build_legal()
    build_sitemap_page()
    build_404()
    build_sitemap_xml()
    build_robots()
    build_htaccess()
    build_index_php()

    removed = prune_stale()

    print(f"Built {len(WRITTEN)} files:")
    for p in WRITTEN:
        print("  " + p)
    if removed:
        print(f"\nRemoved {len(removed)} stale page(s):")
        for p in removed:
            print("  " + p)


if __name__ == "__main__":
    main()
