#!/usr/bin/env python3
"""Static site generator for huttoroofs.com.

Renders every page from the shared layout in this file plus the page data in
content/. No WordPress, no runtime dependencies - output is plain HTML that can
be uploaded as-is.

    python3 build.py            # writes the site into ./ (repo root)
"""

import os
import re
from datetime import date

from siteconfig import BIZ, NEARBY, FOOTER_SERVING, NAV, TODAY
from content.services import SERVICES
from content.areas import AREAS
from content.blog import POSTS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT


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


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

def article_meta(page):
    """Dates for blog posts. The blog index and sitemap read these back from
    drop-in posts, so the template and the generator must agree on them."""
    if not page.get("published"):
        return ""
    mod = page.get("modified", page["published"])
    return (f'<meta property="article:published_time" content="{page["published"]}">\n'
            f'<meta property="article:modified_time" content="{mod}">\n')


def head(page):
    """<head> for one page, including its JSON-LD graph."""
    canonical = url(page["path"])
    og_image = url("/assets/img/Hutto-Roofers-Site-Icon.webp")
    schema = ",\n".join(page.get("schema", []))
    robots = page.get("robots", "index, follow, max-image-preview:large")
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{og_image}">
{article_meta(page)}<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="{BIZ['city']}, {BIZ['state_long']}">
<meta name="geo.position" content="{BIZ['latitude']};{BIZ['longitude']}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..800;1,9..40,300..700&amp;family=DM+Serif+Display:ital@0;1&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{schema}
]}}
</script>
</head>
<body>
<a class="skip-link" href="#content" style="position:absolute;left:-9999px">Skip to content</a>
"""


def header(active=None):
    links = []
    for label, href in NAV:
        current = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    links_html = "".join(links)
    return f"""<div class="site">
<div class="announcement"><div class="container">
<span>Roofing help for {BIZ['city']} homes and businesses</span>
<a href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
</div></div>
<header class="site-header"><div class="container nav-wrap">
<a class="brand" href="/">
<span class="brand-mark" aria-hidden="true">H</span>
<span class="brand-copy"><strong>{BIZ['name']}</strong><span>{BIZ['city']}, {BIZ['state']}</span></span>
</a>
<nav class="nav-links" aria-label="Primary">{links_html}
<a class="nav-cta" href="/#contact">Request an Estimate</a></nav>
<button class="menu-btn" type="button" aria-expanded="false" aria-label="Open navigation">&#9776;</button>
</div></header>
<div class="header-placeholder"></div>
<div class="header-sentinel" aria-hidden="true"></div>
<main id="content">
"""


def contact_section(heading=None, intro=None):
    heading = heading or "Tell us what is happening with your roof."
    intro = intro or (
        "Whether you are dealing with a leak, storm concern, worn shingles or an aging roof, "
        f"start the conversation here. {BIZ['name']} can help you organize the next step."
    )
    return f"""<section class="contact" id="contact"><div class="container contact-grid">
<div class="contact-copy">
<div class="eyebrow">Request an Estimate</div>
<h2>{heading}</h2>
<p>{intro}</p>
<div class="contact-meta">
<span>Call: {BIZ['phone_display']}</span>
<span>Text: {BIZ['phone_display']}</span>
<span>Email: {BIZ['email']}</span>
<span>Serving {BIZ['city']}, {BIZ['state_long']} {BIZ['zip']} and {BIZ['county']}</span>
</div>
</div>
<div class="contact-card">
<form data-estimate-form method="post" action="#">
<div class="form-grid">
<div class="field"><label for="cf-name">Name</label><input id="cf-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="cf-phone">Phone</label><input id="cf-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field full"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
<div class="field full"><label for="cf-address">Property address or {BIZ['city']} neighborhood</label><input id="cf-address" name="address" type="text" autocomplete="street-address"></div>
<div class="field full"><label for="cf-service">What do you need?</label><select id="cf-service" name="service">
<option>Roof repair</option><option>Roof leak repair</option><option>Roof replacement</option>
<option>New roof installation</option><option>Hail damage roof repair</option><option>Storm damage roof repair</option>
<option>Shingle roofing</option><option>Metal roofing</option><option>Roof inspection</option>
<option>Commercial roofing</option><option>Emergency roof repair</option><option>Something else</option>
</select></div>
<div class="field full"><label for="cf-message">Tell us about the roof</label><textarea id="cf-message" name="message" rows="4" placeholder="Leak location, storm date, roof age, anything you have noticed..."></textarea></div>
</div>
<button class="btn btn-dark submit" type="submit">Send Estimate Request &rarr;</button>
<p class="form-note">Prefer to talk it through? Call or text {BIZ['phone_display']}.</p>
</form>
</div>
</div></section>
"""


def footer():
    service_links = "".join(
        f'<a href="{s["path"]}">{s["nav_label"]}</a>' for s in SERVICES[:6]
    )
    area_links = "".join(
        f'<a href="{a["path"]}">Roofing in {a["city"]}</a>' for a in AREAS
    )
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div class="footer-about">
<a class="brand" href="/">
<span class="brand-mark" aria-hidden="true">H</span>
<span class="brand-copy"><strong>{BIZ['name']}</strong><span>{BIZ['city']}, {BIZ['state']}</span></span>
</a>
<p>{BIZ['name']} provides roofing support for homes and businesses in {BIZ['city']}, {BIZ['state']} {BIZ['zip']}
and across {BIZ['county']}. Contact us about roof repairs, replacements, inspections, storm and hail
damage, metal roofing and commercial roofing needs.</p>
<p><strong>{FOOTER_SERVING}</strong></p>
</div>
<div>
<div class="footer-title">Roofing Services</div>
<div class="footer-links">{service_links}<a href="/services/">All services</a></div>
</div>
<div>
<div class="footer-title">Service Areas</div>
<div class="footer-links">{area_links}<a href="/service-areas/">All service areas</a></div>
</div>
<div>
<div class="footer-title">Contact</div>
<div class="footer-links">
<a href="tel:{BIZ['phone_href']}">Call: {BIZ['phone_display']}</a>
<a href="sms:{BIZ['phone_href']}">Text: {BIZ['phone_display']}</a>
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
<a href="/blog/">Roofing Blog</a>
<span>{BIZ['city']}, {BIZ['state_long']} {BIZ['zip']}</span>
</div>
</div>
</div>
<div class="footer-bottom">
<span>&copy; {date.today().year} {BIZ['name']}. All Rights Reserved. {FOOTER_SERVING}.</span>
<span class="footer-links" style="display:flex;gap:18px">
<a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-use/">Terms of Use</a><a href="/sitemap/">Sitemap</a>
</span>
</div>
</div></footer>
<a class="mobile-call" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
</div>
<script src="/assets/js/site.js" defer></script>
</body>
</html>
"""


def breadcrumbs(trail):
    """trail: list of (label, href|None); last item is the current page."""
    parts = []
    for label, href in trail:
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def sub_hero(page):
    """Compact hero for interior pages."""
    img = page.get("hero_image", "/assets/img/LOCAL-HUTTO-ROOFING.webp")
    alt = page.get("hero_alt", "Residential roof in Hutto, Texas")
    actions = f"""<div class="hero-actions">
<a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']} <span>&#8599;</span></a>
<a class="btn btn-outline" href="#contact">{page.get('hero_cta', 'Request a Roof Estimate')}</a>
</div>"""
    visual = f"""<div class="hero-visual">
<div class="hero-image"><img src="{img}" alt="{esc(alt)}" width="1408" height="768" loading="eager" decoding="async"></div>
</div>"""
    return f"""<section class="hero hero-sub" aria-labelledby="page-title"><div class="container hero-grid">
<div class="hero-copy">
{breadcrumbs(page['trail'])}
<div class="eyebrow">{page['eyebrow']}</div>
<h1 id="page-title" style="color:#fff">{page['h1']}</h1>
<p>{page['hero_intro']}</p>
{actions}
</div>
{visual}
</div></section>
"""


def sidebar(page):
    """Standard interior-page sidebar: CTA card + contextual links."""
    blocks = [f"""<div class="side-card">
<h3>Talk to a {BIZ['city']} roofer</h3>
<p>Describe what you are seeing on the roof and we will help you work out the useful next step.</p>
<a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<p style="margin:14px 0 0;font-size:.82rem">Or email <a href="mailto:{BIZ['email']}" style="color:#c29a49">{BIZ['email']}</a></p>
</div>"""]
    for card in page.get("side_lists", []):
        items = "".join(f'<a href="{href}">{label}</a>' for label, href in card["items"])
        blocks.append(
            f'<div class="side-card light"><h3>{card["title"]}</h3>'
            f'<div class="side-list">{items}</div></div>'
        )
    return '<aside class="sidebar">' + "".join(blocks) + "</aside>"


def prose_page(page):
    """Full interior page: hero + prose/sidebar + optional extra sections + CTA."""
    return (
        head(page)
        + header(page.get("active"))
        + sub_hero(page)
        + '<section class="prose"><div class="container prose-grid">'
        + '<div class="prose-body">' + page["body"] + "</div>"
        + sidebar(page)
        + "</div></section>"
        + page.get("extra", "")
        + contact_section(page.get("cta_heading"), page.get("cta_intro"))
        + footer()
    )


# --------------------------------------------------------------------------
# Schema builders
# --------------------------------------------------------------------------

def org_schema():
    area = ",".join(
        '{"@type":"City","name":"%s","address":{"@type":"PostalAddress","addressRegion":"TX","addressCountry":"US"}}' % c
        for c in [BIZ["city"]] + NEARBY
    )
    return (
        '{"@type":["RoofingContractor","LocalBusiness","Organization"],'
        f'"@id":"{BIZ["origin"]}/#organization",'
        f'"name":"{BIZ["name"]}","legalName":"{BIZ["name"]}",'
        f'"url":"{BIZ["origin"]}","email":"{BIZ["email"]}","telephone":"+1-512-297-7580",'
        '"priceRange":"$$$",'
        f'"description":"{BIZ["name"]} is a roofing contractor serving {BIZ["city"]}, TX {BIZ["zip"]} and the '
        'surrounding Williamson County communities with roof repair, roof replacement, roof installation, hail and '
        'storm damage roof repair, shingle and metal roofing, roof inspections, commercial roofing and emergency '
        'roof repair.",'
        '"address":{"@type":"PostalAddress","addressLocality":"' + BIZ["city"] + '",'
        '"addressRegion":"TX","postalCode":"' + BIZ["zip"] + '","addressCountry":"US"},'
        '"geo":{"@type":"GeoCoordinates","latitude":"' + BIZ["latitude"] + '","longitude":"' + BIZ["longitude"] + '"},'
        f'"areaServed":[{area},'
        '{"@type":"AdministrativeArea","name":"Williamson County, Texas"}],'
        '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",'
        '"dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],'
        '"opens":"09:00","closes":"17:00"}],'
        f'"logo":{{"@type":"ImageObject","@id":"{BIZ["origin"]}/#logo",'
        f'"url":"{url("/assets/img/Hutto-Roofers-Site-Icon.webp")}","width":"1500","height":"1500",'
        f'"caption":"{BIZ["name"]}"}},'
        f'"image":{{"@id":"{BIZ["origin"]}/#logo"}}}}'
    )


def website_schema():
    return (
        '{"@type":"WebSite","@id":"' + BIZ["origin"] + '/#website","url":"' + BIZ["origin"] + '",'
        '"name":"' + BIZ["name"] + '","inLanguage":"en-US",'
        '"publisher":{"@id":"' + BIZ["origin"] + '/#organization"}}'
    )


def webpage_schema(page, wtype="WebPage"):
    return (
        '{"@type":"%s","@id":"%s#webpage","url":"%s","name":"%s",'
        '"description":"%s","isPartOf":{"@id":"%s/#website"},'
        '"about":{"@id":"%s/#organization"},"inLanguage":"en-US"}'
        % (
            wtype,
            url(page["path"]),
            url(page["path"]),
            esc(page["title"]),
            esc(page["description"]),
            BIZ["origin"],
            BIZ["origin"],
        )
    )


def breadcrumb_schema(trail, path):
    items = []
    for i, (label, href) in enumerate(trail, start=1):
        target = url(href) if href else url(path)
        items.append(
            '{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}' % (i, esc(label), target)
        )
    return '{"@type":"BreadcrumbList","itemListElement":[' + ",".join(items) + "]}"


def service_schema(page):
    return (
        '{"@type":"Service","@id":"%s#service","name":"%s",'
        '"serviceType":"%s","description":"%s",'
        '"provider":{"@id":"%s/#organization"},'
        '"areaServed":[%s],'
        '"availableChannel":{"@type":"ServiceChannel","servicePhone":{"@type":"ContactPoint","telephone":"+1-512-297-7580"},"serviceUrl":"%s"}}'
        % (
            url(page["path"]),
            esc(page["service_name"]),
            esc(page["service_type"]),
            esc(page["description"]),
            BIZ["origin"],
            ",".join('{"@type":"City","name":"%s"}' % c for c in [BIZ["city"]] + NEARBY),
            url(page["path"]),
        )
    )


def faq_schema(faqs):
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (esc(q), esc(re.sub(r"<[^>]+>", "", a)))
        for q, a in faqs
    )
    return '{"@type":"FAQPage","mainEntity":[' + items + "]}"


def article_schema(page):
    return (
        '{"@type":"BlogPosting","@id":"%s#article","headline":"%s","description":"%s",'
        '"datePublished":"%s","dateModified":"%s",'
        '"author":{"@id":"%s/#organization"},"publisher":{"@id":"%s/#organization"},'
        '"mainEntityOfPage":{"@id":"%s#webpage"},"inLanguage":"en-US",'
        '"image":"%s"}'
        % (
            url(page["path"]),
            esc(page["h1_plain"]),
            esc(page["description"]),
            page["published"],
            page.get("modified", page["published"]),
            BIZ["origin"],
            BIZ["origin"],
            url(page["path"]),
            url(page.get("hero_image", "/assets/img/LOCAL-HUTTO-ROOFING.webp")),
        )
    )


def faq_section(faqs, heading, intro):
    details = "".join(
        f"<details{' open' if i == 0 else ''}><summary>{q}</summary>{a}</details>"
        for i, (q, a) in enumerate(faqs)
    )
    return f"""<section class="faq"><div class="container faq-grid">
<div class="faq-intro"><div class="eyebrow">Frequently Asked Questions</div>
<h2>{heading}</h2><p>{intro}</p></div>
<div>{details}</div>
</div></section>
"""


# --------------------------------------------------------------------------
# Writer
# --------------------------------------------------------------------------

WRITTEN = []


def write(path, html):
    """path is a site path like /services/roof-repair-hutto-tx/ or /robots.txt"""
    if path.endswith("/"):
        target = os.path.join(OUT, path.strip("/"), "index.html")
    else:
        target = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(html)
    WRITTEN.append(path)




# --------------------------------------------------------------------------
# Homepage
#
# Keyword: "roofing hutto tx". The hero paragraph and the "Local Roofing
# Focus" section below are written fresh for Hutto rather than carried over
# from the sister sites, so this page is not a near-duplicate of templeroofs.
# --------------------------------------------------------------------------

def build_home():
    page = {
        "path": "/",
        "title": "Roofing Hutto TX | Hutto Roofing Company | Hutto Roofers",
        "description": (
            "Roofing in Hutto, TX. Hutto Roofers handles roof repair, replacement, hail and storm "
            "damage, inspections and metal roofing in 78634. Call (512) 297-7580."
        ),
    }
    faqs = [
        ("How do I know if my roof needs repair or replacement?",
         "It comes down to the roof's age, how widespread the problem is and the condition of the "
         "shingles around it. An isolated leak on a ten-year-old roof is a repair. Repeated leaks, "
         "widespread granule loss or shingles that crack when lifted point to replacement."),
        ("Should I have my roof inspected after hail or strong wind in Hutto?",
         "Yes, particularly since hail swaths in Central Texas are narrow &mdash; one Hutto "
         "subdivision can be hit while the next is missed entirely. Check your gutters and AC "
         "condenser for dents; if those are marked, the roof is worth looking at."),
        ("What are common signs a Hutto roof needs attention?",
         "Lifted, curled or missing shingles, ceiling stains, granules collecting where downspouts "
         "discharge, deteriorated flashing, damaged pipe boots and any sagging visible in the roof "
         "plane from across the street."),
        ("Can a roof leak be repaired without replacing the whole roof?",
         "Often, yes. If the source is localized and the surrounding shingles are still flexible "
         "and well sealed, a targeted repair is the right answer. The deciding factor is the "
         "condition of the roof around the leak."),
        ("What roofing services does Hutto Roofers offer?",
         "Roof repair, roof leak repair, roof replacement, new roof installation, hail damage "
         "repair, storm damage repair, shingle roofing, metal roofing, roof inspections, "
         "commercial roofing and emergency roof repair."),
        ("What areas do you serve besides Hutto?",
         "We work throughout Williamson County and the surrounding communities: Round Rock, "
         "Pflugerville, Taylor, Georgetown and Manor."),
        ("How do I contact Hutto Roofers?",
         "Call or text " + BIZ["phone_display"] + ", email " + BIZ["email"] + ", or use the "
         "estimate form on this page."),
    ]
    page["schema"] = [
        org_schema(),
        website_schema(),
        webpage_schema(page),
        faq_schema(faqs),
    ]

    service_cards = "".join(
        f"""<article class="service-card">
<div class="service-num">{i:02d} / {s['nav_label'].upper()}</div>
<h3>{s['nav_label']}</h3>
<p>{s['card']}</p>
<a class="service-link" href="{s['path']}">{s['card_cta']} &rarr;</a>
</article>"""
        for i, s in enumerate(HOME_SERVICE_CARDS, start=1)
    )

    area_cards = "".join(
        f"""<a class="link-card" href="{a['path']}">
<h3>Roofing in {a['city']}, TX</h3>
<p>{a['distance']} from Hutto &mdash; {a['drive']}.</p>
<span class="service-link">View {a['city']} roofing &rarr;</span>
</a>"""
        for a in AREAS
    )

    post_cards = "".join(
        f"""<a class="link-card post-card" href="{p['path']}">
<span class="post-date">{p['published']}</span>
<h3>{p['h1_plain']}</h3>
<p>{p['excerpt']}</p>
<span class="service-link">Read the guide &rarr;</span>
</a>"""
        for p in POSTS[:3]
    )

    html = head(page) + header() + f"""
<section class="hero" id="top" aria-labelledby="page-title"><div class="container hero-grid">
<div class="hero-copy">
<div class="eyebrow">Roofing Hutto TX</div>
<h1 id="page-title" style="color:#fff">Hutto roofing built for <span class="gold-text">Blackland Prairie</span> weather.</h1>
<p>Hutto roofs get no shade and no shelter. Out here on open prairie the summer sun works on the
shingles from May through September, and when a line comes through {BIZ['county']} the wind arrives
with nothing in its way. That is the roof we are used to. {BIZ['name']} is a local Hutto roofing
company handling repairs, replacements, inspections and storm damage for homes and businesses
across {BIZ['city']}, {BIZ['state']} {BIZ['zip']}.</p>
<div class="hero-actions">
<a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']} <span>&#8599;</span></a>
<a class="btn btn-outline" href="#contact">Request a Roof Estimate</a>
</div>
<div class="hero-points">
<div class="hero-point"><strong>Roof Repair</strong>Leaks, shingles &amp; flashing</div>
<div class="hero-point"><strong>Roof Replacement</strong>Aging or storm-worn roofs</div>
<div class="hero-point"><strong>Storm &amp; Hail</strong>Inspections after severe weather</div>
</div>
</div>
<div class="hero-visual" aria-label="Hutto, Texas home with a prominent roofline">
<div class="hero-image"><img src="/assets/img/LOCAL-HUTTO-ROOFING.webp" alt="Hutto, Texas home with a clean roofline" width="1408" height="768" fetchpriority="high" decoding="async"></div>
<div class="hero-card">
<span class="mini">Start with the roof condition</span>
<strong>Clear answers before bigger decisions.</strong>
<p>Talk with a {BIZ['city']} roofer about what you are seeing and the practical options for your property.</p>
</div>
</div>
</div></section>

<div class="trust-strip"><div class="container trust-grid">
<div class="trust-item trust-intro">Roofing decisions made simpler.</div>
<div class="trust-item"><span class="trust-icon">&#9670;</span><div><strong>Hutto Focus</strong><span>78634 and {BIZ['county']}</span></div></div>
<div class="trust-item"><span class="trust-icon">&#9671;</span><div><strong>Clear Options</strong><span>Repair or replace</span></div></div>
<div class="trust-item"><span class="trust-icon">&#8599;</span><div><strong>Easy Contact</strong><span>Call, text or request online</span></div></div>
</div></div>

<section class="about"><div class="container" style="padding:70px 0 0">
<div class="section-head">
<div><div class="eyebrow">Local Roofing Company</div>
<h2>A Hutto roofing contractor, not a crew passing through.</h2></div>
<p>People searching for a roofer in Hutto, TX after a storm get a lot of doors knocked on by
companies that will not be here next season. We work this town year round.</p>
</div>
<p style="max-width:760px;color:var(--muted);margin-bottom:0">Homeowners looking for roofers in
Hutto, Texas generally want three things: someone who will actually diagnose the problem, a
straight answer on repair versus replacement, and a number they can trust. That is the whole job
as we see it. Call or text <a href="tel:{BIZ['phone_href']}" style="color:var(--gold);font-weight:700">{BIZ['phone_display']}</a>
and describe what your roof is doing.</p>
</div></section>

<section class="services" id="services"><div class="container">
<div class="section-head">
<div><div class="eyebrow">Roofing Services</div>
<h2>Hutto roofing for the problems that cannot wait forever.</h2></div>
<p>Every roof problem has a different starting point. A single leak may call for targeted repair,
while aging materials or broad storm damage may need a larger plan. Our
<a href="/services/" style="color:var(--gold)">Hutto roofing services</a> are organized around what
your roof actually appears to need.</p>
</div>
<div class="service-grid">{service_cards}</div>
<p style="margin-top:28px"><a class="btn btn-dark" href="/services/">See all roofing services <span>&rarr;</span></a></p>
</div></section>

<section class="about" id="about"><div class="container split">
<div class="split-image">
<div class="image-main"><img src="/assets/img/WHY-HUTTO-ROOFERS.webp" alt="Hutto, Texas home exterior showing roof and architectural details" width="1400" height="781" loading="lazy" decoding="async"></div>
<div class="image-mini"><img src="/assets/img/A-practical-approach-to-your-roof-not-a-one-size-fits-all-answer.webp" alt="Roofing professional working on a residential roof in Hutto" width="1400" height="927" loading="lazy" decoding="async"></div>
</div>
<div class="split-copy">
<div class="eyebrow">Why {BIZ['name']}</div>
<h2>A practical approach to your roof, not a one-size-fits-all answer.</h2>
<p>A stain on the ceiling does not always tell you where a leak began. One missing shingle does not
always mean you need a new roof. Good roofing decisions start with the condition of the system, the
age of the materials and what is happening around the problem area.</p>
<p>That is the approach behind {BIZ['name']}. Whether you are dealing with a sudden issue or
planning ahead, a {BIZ['city']} roofer can help you review the situation and choose a sensible path
forward.</p>
<ul class="check-list">
<li><span class="check">&#10003;</span><span>Residential and commercial Hutto roofing support</span></li>
<li><span class="check">&#10003;</span><span>Repair and replacement options based on visible roof condition</span></li>
<li><span class="check">&#10003;</span><span>Wind, hail and storm-related roof evaluations</span></li>
<li><span class="check">&#10003;</span><span>Roof inspections for maintenance and future planning</span></li>
</ul>
<a class="btn btn-dark" href="#contact">Discuss Your Roof <span>&rarr;</span></a>
</div>
</div></section>

<section class="process" id="process"><div class="container">
<div class="section-head">
<div><div class="eyebrow">Our Process</div>
<h2 style="color:#fff">From roof concern to a clear next step.</h2></div>
<p>A roofing project feels more manageable when the path is straightforward. Here is a simple way to
begin working through your {BIZ['city']} roofing needs.</p>
</div>
<div class="process-grid">
<article class="step"><div class="step-num">01</div><h3>Tell Us What You See</h3><p>Share the property type, roof concern, leak symptoms and any recent storm information.</p></article>
<article class="step"><div class="step-num">02</div><h3>Inspect the Roof</h3><p>Review accessible roof areas, penetrations and the attic to understand the real condition.</p></article>
<article class="step"><div class="step-num">03</div><h3>Review the Options</h3><p>Discuss repair, replacement or maintenance paths based on what the roof actually needs.</p></article>
<article class="step"><div class="step-num">04</div><h3>Move Forward</h3><p>Choose a roofing scope that makes sense for the property, roof condition and project goals.</p></article>
</div>
</div></section>

<section class="materials"><div class="container">
<div class="section-head">
<div><div class="eyebrow">Roofing Options</div>
<h2>Common roof systems for Hutto properties.</h2></div>
<p>The right roof depends on the structure, slope, existing system, budget and performance
priorities. These are common starting points to discuss with a {BIZ['city']} roofer.</p>
</div>
<div class="material-grid">
<article class="material-card">
<img src="/assets/img/Asphalt-Shingle-Roofing.webp" alt="Asphalt shingle roof on a Hutto, Texas home" width="1408" height="768" loading="lazy" decoding="async">
<div class="material-content"><h3 style="color:#fff">Asphalt Shingle Roofing</h3><p>The default on most Hutto homes. Available in three-tab, architectural and Class 4 impact-resistant grades.</p></div>
</article>
<article class="material-card">
<img src="/assets/img/New-Roof-Installation.webp" alt="New roof installation on a home in Hutto, Texas" width="1408" height="768" loading="lazy" decoding="async">
<div class="material-content"><h3 style="color:#fff">New Roof Installation</h3><p>Complete roofing systems for replacement projects, additions and new construction.</p></div>
</article>
<article class="material-card">
<img src="/assets/img/Repair-Maintenance.webp" alt="Roof repair and maintenance work in Hutto, Texas" width="1408" height="768" loading="lazy" decoding="async">
<div class="material-content"><h3 style="color:#fff">Repair &amp; Maintenance</h3><p>Targeted work on specific roof concerns and the serviceable areas of an aging system.</p></div>
</article>
</div>
</div></section>

<section class="local"><div class="container local-grid">
<div class="local-copy">
<div class="eyebrow">Local Roofing Focus</div>
<h2>Why Hutto roofs wear out faster than the brochure says.</h2>
<p>Hutto sits on flat, open Blackland Prairie at the eastern edge of the Austin metro, and that
geography is hard on roofing. The subdivisions that filled in through the 2000s and 2010s &mdash;
Star Ranch, Emory Farms, Creek Bend, Cottonwood Creek, Legends of Hutto &mdash; were built on former
farmland where the landscaping is still catching up. There is almost no canopy over those roof
planes, so the shingles take direct sun from sunrise to sunset through five months of Texas summer,
then cycle 30 degrees cooler overnight. Asphalt does not enjoy that.</p>
<p>The same open ground means nothing slows the wind down. When a line moves northeast through
{BIZ['county']}, the gusts reaching the developments off FM 1660 and Chris Kelley Boulevard arrive
with the full force they carried across open field &mdash; and spring hail falls in swaths narrow
enough that one Hutto neighbourhood is hit while the next is missed entirely. Meanwhile the older
lots around Old Town Hutto and along Brushy Creek have the opposite problem: mature pecans and live
oaks that shade the roof beautifully and drop limbs on it during storms.</p>
<p>All of which is a long way of saying that a roof in 78634 needs the details right. Balanced
attic ventilation, a six-nail high-wind pattern, and honest attention after each severe season.</p>
<div class="signal-list">
<div class="signal">Missing or lifted shingles</div>
<div class="signal">Ceiling or attic stains</div>
<div class="signal">Hail impact concerns</div>
<div class="signal">Wind-related roof damage</div>
<div class="signal">Worn flashing or seals</div>
<div class="signal">Granules in the gutters</div>
</div>
</div>
<aside class="local-panel">
<small>Contact {BIZ['name']}</small>
<h3 style="color:#fff">Have a roof problem you want to talk through?</h3>
<p>Start by describing what you are seeing. We can use that conversation to help identify the most
useful next step.</p>
<a class="contact-line" href="tel:{BIZ['phone_href']}">{BIZ['phone_display']} &rarr;</a>
<a class="contact-line" href="mailto:{BIZ['email']}">{BIZ['email']} &rarr;</a>
<a class="btn btn-gold panel-cta" href="#contact">Request an Estimate</a>
</aside>
</div></section>

<section class="services"><div class="container">
<div class="section-head">
<div><div class="eyebrow">Service Areas</div>
<h2>Roofing across Hutto and the towns around it.</h2></div>
<p>{FOOTER_SERVING}. Each of those towns has its own building stock and its own storm pattern.</p>
</div>
<div class="link-grid">{area_cards}</div>
</div></section>

<section class="materials"><div class="container">
<div class="section-head">
<div><div class="eyebrow">Roofing Blog</div>
<h2>Straight answers for Central Texas homeowners.</h2></div>
<p>Costs, lifespans, storm damage and material choices &mdash; written for the roofs we actually
work on.</p>
</div>
<div class="link-grid">{post_cards}</div>
<p style="margin-top:28px"><a class="btn btn-dark" href="/blog/">Read the blog <span>&rarr;</span></a></p>
</div></section>

""" + faq_section(
        faqs,
        "Questions about Hutto roofing.",
        "Use these answers as a starting point when deciding whether it is time to contact a "
        f"{BIZ['city']} roofer about a repair, inspection or replacement.",
    ) + contact_section() + footer()

    write("/", html)


HOME_SERVICE_CARDS = []


def _home_cards():
    """Six headline services for the homepage grid."""
    copy = {
        "roof-repair-hutto-tx": (
            "Isolated leaks, damaged shingles, flashing problems and failed pipe boots &mdash; "
            "traced to the source before anything gets quoted.",
            "Ask about roof repair"),
        "roof-replacement-hutto-tx": (
            "When roof age, repeated repairs or widespread wear make a full replacement the more "
            "sensible project.",
            "Plan a replacement"),
        "hail-damage-roof-repair-hutto-tx": (
            "Hail bruises the shingle mat without leaving anything visible from the ground. We "
            "check the soft metals first, then the roof.",
            "Request a hail check"),
        "storm-damage-roof-repair-hutto-tx": (
            "Wind, wind-driven rain and debris affect different parts of a roof. Assessment covers "
            "every slope, not just the obvious one.",
            "Request an inspection"),
        "metal-roofing-hutto-tx": (
            "Standing seam and exposed-fastener panel systems for long-hold homes, shops and "
            "outbuildings around Hutto.",
            "Discuss metal roofing"),
        "commercial-roofing-hutto-tx": (
            "Low-slope and metal roofs for the US-79 corridor, the Co-Op District and Hutto's "
            "light-industrial buildings.",
            "Talk commercial roofing"),
    }
    out = []
    for slug, (card, cta) in copy.items():
        svc = next(s for s in SERVICES if s["slug"] == slug)
        out.append(dict(svc, card=card, card_cta=cta))
    return out


# --------------------------------------------------------------------------
# Service pages, service-area pages, blog posts
# --------------------------------------------------------------------------

def build_services():
    for svc in SERVICES:
        others = [s for s in SERVICES if s["slug"] != svc["slug"]]
        page = dict(svc)
        page["active"] = "/services/"
        page["hero_cta"] = "Request an Estimate"
        page["cta_heading"] = f"Ready to talk about {svc['nav_label'].lower()} in {BIZ['city']}?"
        page["cta_intro"] = (
            f"Describe what you are seeing and we will tell you what it looks like and what it "
            f"would take to put right. {BIZ['name']} covers {BIZ['city']} {BIZ['zip']} and "
            f"{BIZ['county']}."
        )
        page["side_lists"] = [
            {"title": "Other Hutto services",
             "items": [(s["nav_label"], s["path"]) for s in others]},
            {"title": "Service areas",
             "items": [(f"Roofing in {a['city']}", a["path"]) for a in AREAS]},
        ]
        page["schema"] = [
            org_schema(),
            website_schema(),
            webpage_schema(page),
            breadcrumb_schema(svc["trail"], svc["path"]),
            service_schema(svc),
            faq_schema(svc["faqs"]),
        ]
        page["extra"] = faq_section(
            svc["faqs"],
            f"{svc['nav_label']} questions from Hutto homeowners.",
            "Common questions about " + svc["keyword"] + ". If yours is not here, call or text "
            f"{BIZ['phone_display']}.",
        )
        write(svc["path"], prose_page(page))


def build_areas():
    for area in AREAS:
        others = [a for a in AREAS if a["slug"] != area["slug"]]
        page = dict(area)
        page["active"] = "/service-areas/"
        page["hero_cta"] = f"Request a {area['city']} Estimate"
        page["hero_intro"] = (
            f"{BIZ['name']} is based in {BIZ['city']} and works across {area['city']}, "
            f"{BIZ['state']} &mdash; {area['distance']} away, {area['drive']}. Same crew, same "
            f"services, and close enough that a leak call does not sit in a queue for a week."
        )
        page["body"] = f"""
<div class="fact-grid">
<div class="fact"><strong>{area['distance']}</strong><span>from our Hutto base</span></div>
<div class="fact"><strong>{area['county']}</strong><span>jurisdiction</span></div>
<div class="fact"><strong>{area['population']}</strong><span>residents</span></div>
</div>
{area['body']}
<h2>Based in Hutto, working across {area['city']}</h2>
<p>Our home market is {BIZ['city']}, {BIZ['state']} {BIZ['zip']} &mdash; see
<a href="/">Hutto Roofers</a> for the full picture of what we do and how we work. {area['city']}
is {area['distance']} from that base, {area['drive']}, which keeps response times short for
repairs, inspections and storm calls alike.</p>
<p>Call or text <a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a>, or email
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a>.</p>
"""
        page["side_lists"] = [
            {"title": "Roofing services",
             "items": [(s["nav_label"], s["path"]) for s in SERVICES]},
            {"title": "Other service areas",
             "items": [("Roofing in Hutto (main)", "/")]
                      + [(f"Roofing in {a['city']}", a["path"]) for a in others]},
        ]
        page["cta_heading"] = f"Roofing help in {area['city']}, {BIZ['state']}"
        page["cta_intro"] = (
            f"Tell us the address and what the roof is doing. We cover {area['city']} from "
            f"{BIZ['city']}, {area['distance']} away."
        )
        page["schema"] = [
            org_schema(),
            website_schema(),
            webpage_schema(page),
            breadcrumb_schema(area["trail"], area["path"]),
            service_schema(area),
        ]
        write(area["path"], prose_page(page))


def build_posts():
    for post in POSTS:
        others = [p for p in POSTS if p["slug"] != post["slug"]]
        page = dict(post)
        page["active"] = "/blog/"
        page["og_type"] = "article"
        page["hero_intro"] = post["excerpt"]
        page["hero_cta"] = "Request an Estimate"
        page["body"] = (
            f'<p class="article-meta"><span>Published {post["published"]}</span>'
            f'<span class="read-time">{post["read_time"]}</span><span>{BIZ["name"]}</span></p>'
            + post["body"]
        )
        page["side_lists"] = [
            {"title": "More from the blog",
             "items": [(p["h1_plain"], p["path"]) for p in others]},
            {"title": "Roofing services",
             "items": [(s["nav_label"], s["path"]) for s in SERVICES[:6]]},
        ]
        page["cta_heading"] = "Questions about your own roof?"
        page["cta_intro"] = (
            f"Articles describe the general case. For what is happening on your roof in "
            f"{BIZ['city']}, call or text {BIZ['phone_display']} and describe it."
        )
        page["schema"] = [
            org_schema(),
            website_schema(),
            webpage_schema(page),
            breadcrumb_schema(post["trail"], post["path"]),
            article_schema(post),
        ]
        write(post["path"], prose_page(page))


# --------------------------------------------------------------------------
# Drop-in blog posts
#
# A post can be added without touching Python: copy templates/blog-post.html
# to blog/<slug>/index.html and fill in the placeholders. build_blog_index()
# and the sitemap pick it up from its <title>, meta description, H1 and the
# article:published_time meta tag.
# --------------------------------------------------------------------------

_DROPINS = None


def discover_dropin_posts():
    global _DROPINS
    if _DROPINS is not None:
        return _DROPINS
    found = _DROPINS = []
    blog_dir = os.path.join(OUT, "blog")
    if not os.path.isdir(blog_dir):
        return found
    generated = {p["slug"] for p in POSTS}
    for slug in sorted(os.listdir(blog_dir)):
        fs = os.path.join(blog_dir, slug, "index.html")
        if slug in generated or not os.path.isfile(fs):
            continue
        html = open(fs, encoding="utf-8").read()
        # The template's instruction comment names the placeholders, so look
        # for unfilled ones only outside comments.
        if "{{" in re.sub(r"<!--.*?-->", "", html, flags=re.S):
            print(f"  ! skipping blog/{slug}/: unfilled template placeholders")
            continue

        def grab(pattern, default=""):
            m = re.search(pattern, html, re.S)
            return m.group(1).strip() if m else default

        title = grab(r"<title>(.*?)</title>")
        h1 = re.sub(r"<[^>]+>", "", grab(r"<h1[^>]*>(.*?)</h1>"))
        if not title or not h1:
            print(f"  ! skipping blog/{slug}/: no <title> or <h1>")
            continue
        found.append({
            "slug": slug,
            "path": f"/blog/{slug}/",
            "h1_plain": h1,
            "excerpt": grab(r'<meta name="description" content="(.*?)">'),
            "published": grab(r'<meta property="article:published_time" content="(.*?)">', "1970-01-01"),
            "read_time": grab(r'<span class="read-time">(.*?)</span>', ""),
            "dropin": True,
        })
        print(f"  + drop-in post: blog/{slug}/")
    return found


def all_posts():
    """Generated posts plus drop-ins, newest first."""
    return sorted(POSTS + discover_dropin_posts(), key=lambda p: p["published"], reverse=True)


# --------------------------------------------------------------------------
# Index pages
# --------------------------------------------------------------------------

def build_services_index():
    page = {
        "path": "/services/",
        "title": "Roofing Services in Hutto, TX | Hutto Roofers",
        "description": (
            "All roofing services in Hutto, TX: repair, replacement, installation, hail and storm "
            "damage, shingle, metal, inspection, commercial and emergency roofing."
        ),
        "h1": "Roofing Services in <span class=\"gold-text\">Hutto, TX</span>",
        "h1_plain": "Roofing Services in Hutto, TX",
        "eyebrow": "Hutto Roofing Services",
        "active": "/services/",
        "trail": [("Home", "/"), ("Services", None)],
        "hero_intro": (
            "Ten things we do, listed plainly. Most people arrive here knowing roughly what is "
            "wrong and wanting to know what it involves &mdash; so each page covers what the work "
            f"actually entails on a {BIZ['city']} roof, what drives the cost, and where the line "
            "between repair and replacement falls."
        ),
    }
    cards = "".join(
        f"""<a class="link-card" href="{s['path']}">
<h3>{s['nav_label']}</h3>
<p>{s['description'].split('.')[0]}.</p>
<span class="service-link">Learn more &rarr;</span>
</a>"""
        for s in SERVICES
    )
    page["body"] = f"""
<h2>Every roofing service we offer in Hutto</h2>
<p>All of these are available across {BIZ['city']}, {BIZ['state']} {BIZ['zip']} and throughout
{BIZ['county']}, plus {", ".join(NEARBY[:-1])} and {NEARBY[-1]}.</p>
<div class="link-grid">{cards}</div>

<h2>Not sure which one you need?</h2>
<p>That is normal, and it is usually the right starting point. Most people know a symptom, not a
diagnosis &mdash; a stain on the ceiling, a shingle in the yard, a neighbour getting a new roof after
the last hail storm. A <a href="/services/roof-inspection-hutto-tx/">roof inspection</a> turns the
symptom into an answer without committing you to anything.</p>
<p>If water is coming in right now, skip the rest and go to
<a href="/services/emergency-roof-repair-hutto-tx/">emergency roof repair</a> or call
<a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a>.</p>
"""
    page["side_lists"] = [
        {"title": "Service areas",
         "items": [(f"Roofing in {a['city']}", a["path"]) for a in AREAS]},
        {"title": "From the blog",
         "items": [(p["h1_plain"], p["path"]) for p in POSTS[:4]]},
    ]
    page["schema"] = [
        org_schema(), website_schema(), webpage_schema(page, "CollectionPage"),
        breadcrumb_schema(page["trail"], page["path"]),
        '{"@type":"ItemList","itemListElement":[' + ",".join(
            '{"@type":"ListItem","position":%d,"name":"%s","url":"%s"}'
            % (i, esc(s["service_name"]), url(s["path"]))
            for i, s in enumerate(SERVICES, start=1)
        ) + "]}",
    ]
    write("/services/", prose_page(page))


def build_areas_index():
    page = {
        "path": "/service-areas/",
        "title": "Roofing Service Areas | Hutto, Round Rock, Taylor | Hutto Roofers",
        "description": (
            "Hutto Roofers service areas: Hutto, Round Rock, Pflugerville, Taylor, Georgetown and "
            "Manor. Roof repair, replacement and storm damage across Central Texas."
        ),
        "h1": "Roofing <span class=\"gold-text\">Service Areas</span>",
        "h1_plain": "Roofing Service Areas",
        "eyebrow": "Where We Work",
        "active": "/service-areas/",
        "trail": [("Home", "/"), ("Service Areas", None)],
        "hero_intro": (
            f"{FOOTER_SERVING}. Hutto is our base, and everywhere else on this list is inside a "
            "twenty-five minute drive &mdash; close enough that a storm call does not sit waiting."
        ),
    }
    cards = "".join(
        f"""<a class="link-card" href="{a['path']}">
<h3>Roofing in {a['city']}, TX</h3>
<p>{a['distance']} from Hutto &mdash; {a['drive']}. {a['county']}.</p>
<span class="service-link">View {a['city']} &rarr;</span>
</a>"""
        for a in AREAS
    )
    page["body"] = f"""
<h2>Hutto, TX &mdash; our home market</h2>
<p>{BIZ['name']} is based in {BIZ['city']}, {BIZ['state']} {BIZ['zip']}, in {BIZ['county']}. The
<a href="/">Hutto roofing homepage</a> covers what we do and how Hutto's open Blackland Prairie
position affects the roofs here.</p>

<h2>Towns we also cover</h2>
<div class="link-grid">{cards}</div>

<h2>Why the area matters to the work</h2>
<p>These six towns sit within about twenty miles of each other and share a climate, but they do not
share a building stock. Taylor has a historic downtown with hundred-year-old low-slope commercial
roofs. Georgetown has Sun City's thousands of phase-built homes alongside Victorian properties near
the square. Round Rock spans four decades of construction. Hutto and Manor are near-twins &mdash;
fast-growing prairie towns where whole subdivisions reach replacement age together.</p>
<p>Those differences change what a roofing visit involves, which is why each town has its own page
rather than a name swapped into the same text.</p>
"""
    page["side_lists"] = [
        {"title": "Roofing services",
         "items": [(s["nav_label"], s["path"]) for s in SERVICES]},
    ]
    page["schema"] = [
        org_schema(), website_schema(), webpage_schema(page, "CollectionPage"),
        breadcrumb_schema(page["trail"], page["path"]),
    ]
    write("/service-areas/", prose_page(page))


def build_blog_index():
    page = {
        "path": "/blog/",
        "title": "Roofing Blog | Central Texas Roof Advice | Hutto Roofers",
        "description": (
            "Roofing advice for Central Texas homeowners: new roof costs in Hutto, roof lifespans, "
            "hail damage inspection, metal vs shingle and storm season prep."
        ),
        "h1": "The <span class=\"gold-text\">Hutto Roofers</span> Blog",
        "h1_plain": "The Hutto Roofers Blog",
        "eyebrow": "Roofing Blog",
        "active": "/blog/",
        "trail": [("Home", "/"), ("Blog", None)],
        "hero_intro": (
            "Practical answers for Central Texas homeowners &mdash; what roofs cost here, how long "
            "they actually last, and what to do after the hail comes through. Written about the "
            "roofs we work on, not roofs in general."
        ),
    }
    cards = "".join(
        f"""<a class="link-card post-card" href="{p['path']}">
<span class="post-date">{p['published']}{' &middot; ' + p['read_time'] if p.get('read_time') else ''}</span>
<h3>{p['h1_plain']}</h3>
<p>{p['excerpt']}</p>
<span class="service-link">Read the guide &rarr;</span>
</a>"""
        for p in all_posts()
    )
    page["body"] = f"""
<h2>Latest guides</h2>
<div class="link-grid">{cards}</div>

<h2>Have a question we have not covered?</h2>
<p>Call or text <a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a>, or email
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a>. If it comes up often enough it will end up
here.</p>
"""
    page["side_lists"] = [
        {"title": "Roofing services",
         "items": [(s["nav_label"], s["path"]) for s in SERVICES]},
        {"title": "Service areas",
         "items": [(f"Roofing in {a['city']}", a["path"]) for a in AREAS]},
    ]
    page["schema"] = [
        org_schema(), website_schema(), webpage_schema(page, "Blog"),
        breadcrumb_schema(page["trail"], page["path"]),
        '{"@type":"ItemList","itemListElement":[' + ",".join(
            '{"@type":"ListItem","position":%d,"name":"%s","url":"%s"}'
            % (i, esc(p["h1_plain"]), url(p["path"]))
            for i, p in enumerate(all_posts(), start=1)
        ) + "]}",
    ]
    write("/blog/", prose_page(page))


# --------------------------------------------------------------------------
# Legal, HTML sitemap, 404
# --------------------------------------------------------------------------

def build_legal():
    from content.legal import PRIVACY_BODY, TERMS_BODY

    for path, title, h1, desc, body in [
        ("/privacy-policy/", f"Privacy Policy | {BIZ['name']}", "Privacy Policy",
         f"Privacy Policy for {BIZ['name']}, covering what information the huttoroofs.com "
         "website collects, how it is used and the choices you have.", PRIVACY_BODY),
        ("/terms-of-use/", f"Terms of Use | {BIZ['name']}", "Terms of Use",
         f"Terms of Use governing access to and use of the {BIZ['name']} website at "
         "huttoroofs.com.", TERMS_BODY),
    ]:
        page = {
            "path": path, "title": title, "description": desc,
            "trail": [("Home", "/"), (h1, None)],
        }
        page["schema"] = [
            org_schema(), website_schema(), webpage_schema(page),
            breadcrumb_schema(page["trail"], path),
        ]
        html = (
            head(page) + header()
            + f"""<section class="hero hero-sub"><div class="container" style="padding:56px 0 50px">
{breadcrumbs(page['trail'])}
<div class="eyebrow">Legal</div>
<h1 id="page-title" style="color:#fff;font-size:clamp(2.4rem,4vw,3.6rem)">{h1}</h1>
</div></section>
<section class="legal prose"><div class="container"><div class="prose-body">{body}</div></div></section>
"""
            + footer()
        )
        write(path, html)


def build_sitemap_page():
    page = {
        "path": "/sitemap/",
        "title": f"Sitemap | {BIZ['name']}",
        "description": (
            f"Every page on huttoroofs.com: roofing services in {BIZ['city']}, TX, service areas "
            "across Williamson County and the roofing blog."
        ),
        "trail": [("Home", "/"), ("Sitemap", None)],
    }
    page["schema"] = [
        org_schema(), website_schema(), webpage_schema(page),
        breadcrumb_schema(page["trail"], "/sitemap/"),
    ]

    def links(items):
        return '<div class="side-list">' + "".join(
            f'<a href="{href}">{label}</a>' for label, href in items
        ) + "</div>"

    body = f"""
<h2>Main pages</h2>
{links([("Roofing Hutto TX (Home)", "/"), ("Roofing Services", "/services/"),
        ("Service Areas", "/service-areas/"), ("Roofing Blog", "/blog/")])}
<h2>Roofing services in {BIZ['city']}, {BIZ['state']}</h2>
{links([(s["service_name"], s["path"]) for s in SERVICES])}
<h2>Service areas</h2>
{links([(a["service_name"], a["path"]) for a in AREAS])}
<h2>Blog posts</h2>
{links([(p["h1_plain"], p["path"]) for p in POSTS])}
<h2>Legal</h2>
{links([("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/"),
        ("XML Sitemap", "/sitemap.xml")])}
"""
    html = (
        head(page) + header()
        + f"""<section class="hero hero-sub"><div class="container" style="padding:56px 0 50px">
{breadcrumbs(page['trail'])}
<div class="eyebrow">Sitemap</div>
<h1 id="page-title" style="color:#fff;font-size:clamp(2.4rem,4vw,3.6rem)">Sitemap</h1>
</div></section>
<section class="legal prose"><div class="container"><div class="prose-body">{body}</div></div></section>
"""
        + contact_section() + footer()
    )
    write("/sitemap/", html)


def build_404():
    page = {
        "path": "/404.html",
        "title": f"Page Not Found | {BIZ['name']}",
        "description": "That page could not be found. Browse Hutto roofing services or call "
                       f"{BIZ['phone_display']}.",
        "robots": "noindex, follow",
        "trail": [("Home", "/"), ("Not Found", None)],
    }
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page)]
    body = f"""
<p>The page you were looking for is not here. It may have moved, or the link may be out of date.</p>
<h2>Roofing services</h2>
<div class="side-list">{"".join(f'<a href="{s["path"]}">{s["service_name"]}</a>' for s in SERVICES)}</div>
<h2>Service areas</h2>
<div class="side-list">{"".join(f'<a href="{a["path"]}">{a["service_name"]}</a>' for a in AREAS)}</div>
<p style="margin-top:24px"><a class="btn btn-dark" href="/">Back to the Hutto Roofers homepage <span>&rarr;</span></a></p>
"""
    html = (
        head(page) + header()
        + f"""<section class="hero hero-sub"><div class="container" style="padding:56px 0 50px">
<div class="eyebrow">404</div>
<h1 id="page-title" style="color:#fff;font-size:clamp(2.4rem,4vw,3.6rem)">Page not found</h1>
<p style="color:#c6c2b9">Try one of the pages below, or call
<a href="tel:{BIZ['phone_href']}" style="color:#c29a49">{BIZ['phone_display']}</a>.</p>
</div></section>
<section class="legal prose"><div class="container"><div class="prose-body">{body}</div></div></section>
"""
        + footer()
    )
    write("/404.html", html)


# --------------------------------------------------------------------------
# Blog post template (templates/blog-post.html)
#
# Rendered through the same prose_page() as every generated post, so it can
# never drift from the live design. Placeholders are {{UPPER_CASE}} tokens.
# templates/ is excluded from the sitemap, validation and the deploy archive.
# --------------------------------------------------------------------------

def build_blog_template():
    page = {
        "path": "/blog/{{SLUG}}/",
        "title": "{{TITLE}} | " + BIZ["name"],
        "description": "{{META_DESCRIPTION}}",
        "h1": "{{H1}}",
        "h1_plain": "{{H1}}",
        "eyebrow": "{{EYEBROW}}",
        "published": "{{YYYY-MM-DD}}",
        "read_time": "{{N}} min read",
        "excerpt": "{{META_DESCRIPTION}}",
        "hero_image": "/assets/img/LOCAL-HUTTO-ROOFING.webp",
        "hero_alt": "{{HERO_IMAGE_ALT}}",
        "active": "/blog/",
        "og_type": "article",
        "hero_intro": "{{META_DESCRIPTION}}",
        "hero_cta": "Request an Estimate",
        "trail": [("Home", "/"), ("Blog", "/blog/"), ("{{H1}}", None)],
        "body": (
            '<p class="article-meta"><span>Published {{YYYY-MM-DD}}</span>'
            '<span class="read-time">{{N}} min read</span><span>' + BIZ["name"] + "</span></p>\n"
            "<!-- ARTICLE BODY: replace everything between these markers. Use <h2> for sections,\n"
            "     <h3> for sub-sections, <p>, <ul>/<ol>, and <div class=\"callout\"> for asides.\n"
            "     Link to services with /services/<slug>/ and other posts with /blog/<slug>/. -->\n"
            "{{BODY_HTML}}\n"
            "<!-- END ARTICLE BODY -->"
        ),
        "side_lists": [
            {"title": "More from the blog",
             "items": [(p["h1_plain"], p["path"]) for p in POSTS]},
            {"title": "Roofing services",
             "items": [(s["nav_label"], s["path"]) for s in SERVICES[:6]]},
        ],
        "cta_heading": "Questions about your own roof?",
        "cta_intro": (
            f"Articles describe the general case. For what is happening on your roof in "
            f"{BIZ['city']}, call or text {BIZ['phone_display']} and describe it."
        ),
    }
    page["schema"] = [
        org_schema(), website_schema(), webpage_schema(page),
        breadcrumb_schema(page["trail"], page["path"]), article_schema(page),
    ]
    html = prose_page(page)
    instructions = """<!--
  HUTTO ROOFERS BLOG POST TEMPLATE
  ================================
  1. Copy this file to  blog/<slug>/index.html   (slug: lowercase-with-hyphens)
  2. Replace every {{PLACEHOLDER}}:
       {{SLUG}}              the folder name, e.g. roof-ventilation-basics
       {{TITLE}}             page title, under 50 chars (" | Hutto Roofers" is appended)
       {{META_DESCRIPTION}}  140-160 chars, includes the post's main keyword
       {{H1}}                the headline; may differ from TITLE
       {{EYEBROW}}           short category label, e.g. Roofing Costs
       {{YYYY-MM-DD}}        publish date (appears twice)
       {{N}}                 reading time in minutes (appears twice)
       {{HERO_IMAGE_ALT}}    alt text for the hero image; change the src if you add an image
       {{BODY_HTML}}         the article, as HTML
  3. Run  python3 build.py  - the post is picked up automatically and added to
     /blog/ and sitemap.xml. Then  python3 validate.py.
  Leave everything else alone; header, footer, sidebar and schema come from the live design.
-->
"""
    html = html.replace("<!DOCTYPE html>\n", "<!DOCTYPE html>\n" + instructions, 1)
    target = os.path.join(OUT, "templates", "blog-post.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(html)
    WRITTEN.append("/templates/blog-post.html")


# --------------------------------------------------------------------------
# robots.txt + sitemap.xml
# --------------------------------------------------------------------------

def build_sitemap_xml():
    entries = [("/", "1.0", "weekly"), ("/services/", "0.9", "monthly"),
               ("/service-areas/", "0.8", "monthly"), ("/blog/", "0.7", "weekly")]
    entries += [(s["path"], "0.9", "monthly") for s in SERVICES]
    entries += [(a["path"], "0.7", "monthly") for a in AREAS]
    entries += [(p["path"], "0.6", "monthly") for p in all_posts()]
    entries += [("/sitemap/", "0.3", "yearly"), ("/privacy-policy/", "0.2", "yearly"),
                ("/terms-of-use/", "0.2", "yearly")]
    urls = "\n".join(
        f"  <url>\n    <loc>{url(p)}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        for p, pri, freq in entries
    )
    write("/sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + urls + "\n</urlset>\n")


def build_legacy_sitemaps():
    """The WordPress site published sitemap_index.xml and page-sitemap.xml
    (Rank Math). Keep both URLs alive so nothing indexed returns a 404."""
    write("/sitemap_index.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"  <sitemap>\n    <loc>{url('/sitemap.xml')}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </sitemap>\n"
          "</sitemapindex>\n")
    write("/page-sitemap.xml", open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read())


def build_htaccess():
    """Apache/LiteSpeed config for the static site: index.html first (the
    WordPress install preferred index.php), a real 404 page, and 301s for
    the WordPress URL patterns that no longer exist."""
    write("/.htaccess", """# huttoroofs.com - static site
DirectoryIndex index.html index.htm
ErrorDocument 404 /404.html
Options -Indexes

<IfModule mod_rewrite.c>
RewriteEngine On
# Old WordPress-only paths -> nearest static equivalent
RewriteRule ^feed/?$ /blog/ [R=301,L]
RewriteRule ^(wp-admin|wp-login\\.php|xmlrpc\\.php|wp-json)(/.*)?$ / [R=301,L]
RewriteRule ^wp-content/uploads/2026/09/(.+)$ /assets/img/$1 [R=301,L]
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 1 year"
ExpiresByType text/css "access plus 1 month"
ExpiresByType application/javascript "access plus 1 month"
</IfModule>
""")


def build_robots():
    write("/robots.txt",
          "User-agent: *\n"
          "Allow: /\n"
          "Disallow: /templates/\n\n"
          f"Sitemap: {url('/sitemap.xml')}\n")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    global HOME_SERVICE_CARDS
    HOME_SERVICE_CARDS = _home_cards()

    build_home()
    build_services_index()
    build_services()
    build_areas_index()
    build_areas()
    build_posts()
    build_blog_index()
    build_blog_template()
    build_legal()
    build_sitemap_page()
    build_404()
    build_sitemap_xml()
    build_legacy_sitemaps()
    build_htaccess()
    build_robots()

    print(f"Built {len(WRITTEN)} files:")
    for p in WRITTEN:
        print("  " + p)


if __name__ == "__main__":
    main()
