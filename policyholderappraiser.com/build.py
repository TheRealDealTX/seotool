#!/usr/bin/env python3
"""Static site generator for policyholderappraiser.com.

    python3 build.py        # writes the whole site into ./public/

Shared chrome lives here; page copy lives in content/. Output is plain HTML
plus the files in src/ (CSS, JS, images, contact.php, .htaccess) copied over.
"""

import json
import os
import shutil

from siteconfig import BIZ, MARKETS, NAV, TODAY
from content.services import SERVICES
from content.guides import GUIDES, BY_SLUG as GUIDE
from content.faq import FAQ
from content.legal import PRIVACY_BODY, TERMS_BODY
from content.cities import CITIES
from content.bio import BIO
from content.cities_extra import EXTRA
from content.storms import STORMS, PUBLISHED as STORMS_PUBLISHED
from content.teasers import BLOG_TEASERS, HOME_SERVICE, HOME_GUIDE

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
PHONE = BIZ["phone_display"]
TEL = BIZ["phone_href"]


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def url(path):
    return BIZ["origin"].rstrip("/") + path


def jd(obj):
    """Compact JSON-LD."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# --------------------------------------------------------------------------
# Icons (inline SVG, stroke-based, 24px)
# --------------------------------------------------------------------------
ICONS = {
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
    "hail": '<path d="M7 15a4 4 0 0 1-.5-8 6 6 0 0 1 11.6 1.4A3.5 3.5 0 0 1 17.5 15H7z"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="20" r="1"/><circle cx="16" cy="19" r="1"/>',
    "wind": '<path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h15a3 3 0 1 1-3 3"/><path d="M3 16h8"/>',
    "water": '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/><path d="M9 14a3 3 0 0 0 3 3"/>',
    "fire": '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 1-3s0 3 2 3c1-3-1-6 2-10z"/>',
    "scale": '<path d="M12 4v16M7 20h10M4 8h16"/><path d="M4 8l-3 6h6zM20 8l-3 6h6z"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


LOGO = ('<svg class="logo-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#0f1c2b"/>'
        '<g fill="none" stroke="#d9a93f" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M32 14v34"/><path d="M24 48h16"/><path d="M14 22h36"/><path d="M14 22l-7 14h14z"/><path d="M50 22l-7 14h14z"/></g>'
        '<circle cx="32" cy="14" r="3.2" fill="#d9a93f"/></svg>')


# --------------------------------------------------------------------------
# Schema builders
# --------------------------------------------------------------------------
ORG_ID = url("/#organization")
SITE_ID = url("/#website")
PERSON_ID = url("/joseph-dittman/#person")


def org_schema():
    return {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": ORG_ID,
        "name": BIZ["name"],
        "legalName": BIZ["legal_name"],
        "alternateName": "Policyholder Appraiser by Rise Public Adjusting",
        "url": url("/"),
        "logo": url("/web-app-manifest-512x512.png"),
        "image": url("/img/og-image.png"),
        "telephone": "+1-832-503-5866",
        "email": BIZ["email"],
        "description": "Independent insurance appraisers and umpires for disputed residential and commercial property claims in Texas.",
        "areaServed": [{"@type": "State", "name": "Texas"}] + [{"@type": "City", "name": c["name"] + ", TX", "url": url(c["path"])} for c in CITIES],
        "address": {"@type": "PostalAddress", "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"},
        "priceRange": "$$",
        "openingHours": "Mo-Sa 08:00-19:00",
        "founder": {"@id": PERSON_ID},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Texas Insurance Code Chapter 1813", "Property insurance claims"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Appraisal services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["service_type"], "url": url(s["path"])}}
                for s in SERVICES
            ],
        },
    }


def person_schema():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": BIZ["principal"],
        "jobTitle": BIZ["principal_title"],
        "worksFor": {"@id": ORG_ID},
        "image": url("/img/joseph-dittman-appraiser.webp"),
        "url": url("/joseph-dittman/"),
        "sameAs": BIO["sameas"],
        "knowsAbout": ["Insurance appraisal", "Appraisal umpire", "Xactimate estimating", "Property insurance claims", "Texas Insurance Code Chapter 1813"],
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Texas public adjuster license",
             "identifier": BIZ["license_number"], "recognizedBy": {"@type": "GovernmentOrganization", "name": "Texas Department of Insurance"}},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Texas independent adjuster license",
             "identifier": BIZ["ia_license_number"], "recognizedBy": {"@type": "GovernmentOrganization", "name": "Texas Department of Insurance"}},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "P.L.A.N. Umpire / Appraiser Certification"},
        ],
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE_ID, "url": url("/"), "name": BIZ["name"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def webpage_schema(page, extra_type=None):
    t = ["WebPage"] + ([extra_type] if extra_type else [])
    d = {"@type": t if extra_type else "WebPage", "@id": url(page["path"]) + "#webpage", "url": url(page["path"]),
         "name": page["title"], "description": page["description"], "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID},
         "inLanguage": "en-US", "dateModified": TODAY}
    if page.get("published"):
        d["datePublished"] = page["published"]
    return d


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url(path)} for i, (name, path) in enumerate(crumbs)]}


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def service_schema(s):
    return {"@type": "Service", "@id": url(s["path"]) + "#service", "name": s["service_type"], "serviceType": s["service_type"],
            "provider": {"@id": ORG_ID}, "areaServed": {"@type": "State", "name": "Texas"}, "url": url(s["path"]),
            "description": s["description"]}


def article_schema(g):
    return {"@type": "Article", "@id": url(g["path"]) + "#article", "headline": g["h1_plain"], "description": g["description"],
            "author": {"@id": PERSON_ID}, "publisher": {"@id": ORG_ID}, "datePublished": g["published"], "dateModified": TODAY,
            "mainEntityOfPage": url(g["path"]), "image": url("/img/og-image.png")}


# --------------------------------------------------------------------------
# Chrome
# --------------------------------------------------------------------------
def head(page, graph):
    canonical = url(page["path"])
    robots = page.get("robots", "index, follow, max-image-preview:large")
    og_type = "article" if page.get("published") else "website"
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0f1c2b">
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-W4HZ6QQF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url('/img/og-image.png')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{url('/img/og-image.png')}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Texas">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&amp;family=Inter:wght@400;600;700&amp;display=swap">
<link rel="stylesheet" href="/css/site.css">
<script type="application/ld+json">{jd({"@context": "https://schema.org", "@graph": graph})}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(active=None):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<div class="topbar"><div class="wrap topbar-in">
<span><strong>Independent appraisers for Texas policyholders</strong> &middot; Certified appraiser &amp; umpire &middot; Statewide Texas</span>
<span class="topbar-links"><a href="tel:{TEL}">Call {PHONE}</a><a href="sms:{TEL}">Text {PHONE}</a></span>
</div></div>
<header class="site-header"><div class="wrap header-in">
<a class="logo" href="/" aria-label="{BIZ['name']} home">{LOGO}<span class="logo-text"><strong>Policyholder Appraiser</strong><em>Texas</em></span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="nav-label">Menu</span></button>
<nav class="site-nav" id="site-nav" aria-label="Primary"><ul><li class="areas-item"><a class="areas-link" href="/service-areas/"{' aria-current="page"' if active == "/service-areas/" else ''}><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>Insurance Appraiser Service Areas</a></li>{''.join(items)}</ul><a class="btn btn-brass nav-cta" href="/contact/">Free Review</a></nav>
</div></header>
<main id="main">
"""


def footer():
    services = "".join(f'<a href="{s["path"]}">{s["nav_label"]}</a>' for s in SERVICES)
    guides = "".join(f'<a href="{g["path"]}">{g["nav_label"]}</a>' for g in GUIDES)
    city_links = " &middot; ".join(f'<a href="{c["path"]}">{kw_title(c)}</a>' for c in CITIES)
    return f"""</main>
<section class="cta-band" aria-label="Call to action"><div class="wrap cta-band-in">
<div><h2>Disagree with the carrier's number?</h2><p>Send us the estimate. We will tell you within one business day whether appraisal fits and what it would cost.</p></div>
<div class="hero-actions" style="margin:0"><a class="btn btn-dark" href="/contact/">Request a Free Review</a><a class="btn btn-outline" href="tel:{TEL}">Call {PHONE}</a></div>
</div></section>
<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div class="footer-about">
<a class="logo logo-light" href="/">{LOGO}<span class="logo-text"><strong>Policyholder Appraiser</strong><em>Texas</em></span></a>
<p>{BIZ['name']} provides independent insurance appraisal and umpire services for disputed residential and commercial property claims throughout Texas. A service of {BIZ['legal_name']}, {BIZ['license_label']}.</p>
<p><a href="tel:{TEL}">{PHONE}</a> &middot; <a href="mailto:{BIZ['email']}">{BIZ['email']}</a><br>{BIZ['hours']}</p>
</div>
<div><div class="footer-title">Appraisal Services</div><div class="footer-links">{services}<a href="/services/">All services</a></div></div>
<div><div class="footer-title">Guides</div><div class="footer-links"><a href="/appraisal-process/">How appraisal works</a>{guides}<a href="/faq/">FAQ</a><a href="/blog/">Storm history blog</a></div></div>
<div><div class="footer-title">Company</div><div class="footer-links"><a href="/about/">About</a><a href="/joseph-dittman/">Joseph Dittman, appraiser</a><a href="/service-areas/">Service areas</a><a href="/contact/">Contact</a><a href="/privacy-policy/">Privacy policy</a><a href="/terms-of-use/">Terms of use</a></div></div>
</div>
<div class="footer-title" style="margin-top:8px">Insurance appraiser by city</div>
<p class="footer-cities">{city_links}</p>
<p class="disclaimer">Appraisal determines the amount of loss, not coverage. Nothing on this site is legal advice; consult a Texas attorney about your claim. Appraisal and umpire services are provided only under a signed engagement letter. We do not serve as appraiser on claims where Rise Public Adjusting acted as public adjuster.</p>
<div class="footer-bottom"><span>&copy; {TODAY[:4]} {BIZ['legal_name']}. All rights reserved.</span><span><a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>
<a class="mobile-call" href="tel:{TEL}">Call {PHONE}</a>
<script src="/js/site.js" defer></script>
</body>
</html>
"""


def kw(c):
    return f"{c['name']} insurance appraiser"


def kw_title(c):
    return f"{c['name']} Insurance Appraiser"


def post_path(c):
    return f"/blog/{c['slug']}-storm-history/"


def crumbs(items):
    lis = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{name}</span></li>')
        else:
            lis.append(f'<li><a href="{path}">{name}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def page_hero(page, breadcrumbs, actions=True):
    act = (f'<div class="hero-actions"><a class="btn btn-brass" href="/contact/">Request a Free Review</a>'
           f'<a class="btn btn-ghost-light" href="tel:{TEL}">Call {PHONE}</a></div>') if actions else ""
    return f"""<section class="page-hero"><div class="wrap">
{crumbs(breadcrumbs)}
<p class="eyebrow">{page['eyebrow']}</p>
<h1>{page['h1']}</h1>
<p class="lede">{page['intro']}</p>
{act}
</div></section>
"""


def contact_form(compact=False):
    opts = "".join(f"<option>{o}</option>" for o in [
        "Hail or roof", "Hurricane or wind", "Water or plumbing", "Fire or smoke", "Freeze", "Commercial property", "Other"])
    stage = "".join(f"<option>{o}</option>" for o in [
        "Carrier paid, but too little", "Carrier estimate received, no payment yet", "Appraisal already demanded",
        "Need an umpire", "Claim denied", "Not sure"])
    return f"""<form class="form-card" data-contact data-label="Send My Estimate for Review" method="post" action="/contact.php">
<h2 style="font-size:1.35rem">Free appraisal review</h2>
<p class="small" style="color:var(--muted);margin-bottom:18px">Tell us where the claim stands. We reply within one business day with a straight answer on whether appraisal fits.</p>
<div class="form-grid">
<div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="f-zip">Property ZIP</label><input id="f-zip" name="zip" type="text" inputmode="numeric" autocomplete="postal-code"></div>
<div class="field"><label for="f-type">Type of loss</label><select id="f-type" name="type">{opts}</select></div>
<div class="field"><label for="f-stage">Where the claim stands</label><select id="f-stage" name="stage">{stage}</select></div>
<div class="field full"><label for="f-carrier">Insurance carrier (optional)</label><input id="f-carrier" name="carrier" type="text"></div>
<div class="field full"><label for="f-message">What is in dispute?</label><textarea id="f-message" name="message" rows="4" placeholder="Carrier's estimate amount, your contractor's estimate, date of loss, anything else"></textarea></div>
<div class="field full"><label class="consent"><input type="checkbox" name="consent" value="yes" required><span>I agree to be contacted by call, text or email about my inquiry. Message and data rates may apply. Reply STOP to opt out. Consent is not a condition of service.</span></label></div>
<div class="hp" aria-hidden="true"><label for="f-website">Leave blank</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
</div>
<p style="margin-top:16px;margin-bottom:0"><button class="btn btn-brass btn-block" type="submit">Send My Estimate for Review</button></p>
<p class="form-status" role="status"></p>
<p class="form-note">No upfront fee for the review. If we take the engagement, the fee is quoted in writing first. Prefer to talk? Call or text {PHONE}.</p>
</form>"""


def contact_section(heading=None, intro=None, compact=False):
    """Contact block. The homepage and contact page carry the full intro; every
    other page passes its own heading and uses the compact variant so the
    block does not repeat a paragraph across the site."""
    heading = heading or "Send us the carrier's estimate."
    if compact:
        copy = f"""<p class="eyebrow">Get started</p>
<h2>{heading}</h2>
<div class="contact-meta">
<a href="tel:{TEL}">Call {PHONE}</a>
<a href="sms:{TEL}">Text {PHONE}</a>
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
</div>"""
    else:
        intro = intro or ("We read the appraisal clause, compare the carrier's scope with the damage you describe, and tell you plainly whether appraisal is the right move. If it is, you get a flat fee in writing before you appoint us.")
        copy = f"""<p class="eyebrow">Get started</p>
<h2>{heading}</h2>
<p class="lede">{intro}</p>
<div class="contact-meta">
<a href="tel:{TEL}">Call {PHONE}<span>{BIZ['hours']}</span></a>
<a href="sms:{TEL}">Text {PHONE}<span>Photos of the estimate are welcome</span></a>
<a href="mailto:{BIZ['email']}">{BIZ['email']}<span>Attach the carrier's estimate and your policy</span></a>
</div>"""
    return f"""<section class="contact" id="contact"><div class="wrap split">
<div>
{copy}
</div>
{contact_form()}
</div></section>
"""


def faq_block(items, heading="Common questions about appraisal", intro=None, link=True, answers=True):
    """Full Q&A on /faq/ only. Everywhere else `answers=False` renders the
    questions as links into /faq/, so answer text is not duplicated."""
    if answers:
        details = "".join(f'<details id="q-{FAQ.index((q, a)) + 1}"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    else:
        details = '<ul class="faq-links">' + "".join(f'<li><a href="/faq/#q-{FAQ.index((q, a)) + 1}">{q}</a></li>' for q, a in items) + "</ul>"
    more = '<p style="margin-top:18px"><a class="btn btn-outline" href="/faq/">All questions, answered</a></p>' if link else ""
    intro_html = f"<p>{intro}</p>" if intro else ""
    return f"""<section class="sand"><div class="wrap">
<div class="section-head"><p class="eyebrow">FAQ</p><h2>{heading}</h2>{intro_html}</div>
<div style="max-width:860px">{details}{more}</div>
</div></section>
"""


def sidebar(current=None):
    links = "".join(
        f'<a href="{s["path"]}"{" aria-current=\"page\"" if s["path"] == current else ""}>{s["nav_label"]}</a>' for s in SERVICES)
    glinks = "".join(
        f'<a href="{g["path"]}"{" aria-current=\"page\"" if g["path"] == current else ""}>{g["nav_label"]}</a>' for g in GUIDES)
    return f"""<aside class="sidebar">
<div class="side-card"><h3>Talk to an appraiser</h3><p>Free review of the carrier's estimate. Flat fee quoted in writing before you appoint us.</p><a class="btn btn-brass" href="/contact/">Request a Free Review</a><p style="margin:12px 0 0;text-align:center"><a href="tel:{TEL}" style="color:#fff;text-decoration:none;font-weight:700">Call {PHONE}</a></p></div>
<div class="side-card light"><h3>Appraisal services</h3><div class="side-list">{links}</div></div>
<div class="side-card light"><h3>Guides</h3><div class="side-list"><a href="/appraisal-process/">How appraisal works</a>{glinks}</div></div>
</aside>"""


def author_box():
    return f"""<div class="author-box">
<img src="/img/joseph-dittman-appraiser.webp" alt="{BIZ['principal']}, appraiser and licensed Texas public adjuster" width="72" height="72" loading="lazy">
<p><strong>{BIZ['principal']}</strong>Certified insurance appraiser and umpire, licensed Texas adjuster. <a href="/joseph-dittman/">Full bio</a></p>
</div>"""


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def write(path, html):
    fs = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        fs = os.path.join(fs, "index.html")
    os.makedirs(os.path.dirname(fs), exist_ok=True)
    with open(fs, "w", encoding="utf-8") as f:
        f.write(html)


def service_cards(items, cls="grid grid-3", blurbs=None):
    cards = []
    for s in items:
        blurb = blurbs[s["slug"]] if blurbs else s["card"]
        cards.append(f'<a class="card" href="{s["path"]}"><div class="card-icon">{icon(s["icon"])}</div>'
                     f'<h3>{s["nav_label"]}</h3><p>{blurb}</p><span class="more">Learn more &rarr;</span></a>')
    return f'<div class="{cls}">{"".join(cards)}</div>'


def city_cards(items=None, compact=False):
    items = items or CITIES
    if compact:
        return '<ul class="pill-row city-pills">' + "".join(f'<li><a href="{c["path"]}">{kw_title(c)}</a></li>' for c in items) + "</ul>"
    cards = "".join(f'<a class="card city-card" href="{c["path"]}"><h3>{c["name"]}</h3><p>{c["county"]} &middot; {c["region"]}</p><span class="more">{kw_title(c)} &rarr;</span></a>' for c in items)
    return f'<div class="grid grid-4">{cards}</div>'


def guide_cards(items, blurbs=None):
    cards = []
    for g in items:
        blurb = blurbs[g["slug"]] if blurbs else g["card"]
        cards.append(f'<a class="card" href="{g["path"]}"><div class="card-icon">{icon("doc")}</div>'
                     f'<h3>{g["nav_label"]}</h3><p>{blurb}</p><span class="more">Read the guide &rarr;</span></a>')
    return f'<div class="grid grid-2">{"".join(cards)}</div>'


def steps_block(dark=True, variant="process"):
    if variant == "home":
        steps = [
            ("Day 0", "Invoke the clause", "One signed letter to the carrier starts the process and names your appraiser."),
            ("Within 20 days", "Two appraisers", "The carrier names its own. Both must be competent, independent and disinterested."),
            ("Within 120 days", "Inspect, estimate, compare", "Line by line, in the same software, until only the real disputes are left."),
            ("By day 240", "Binding award", "An umpire decides what remains. Two of three signatures and the number is final."),
        ]
        html = "".join(f'<div class="step"><div class="step-num">0{i + 1}</div><span class="when">{w}</span><h3">{t}</h3><p>{d}</p></div>'.replace('<h3">', '<h3>')
                       for i, (w, t, d) in enumerate(steps))
        return f'<div class="steps">{html}</div>'
    steps = [
        ("Day 0", "You demand appraisal", "A written demand to the carrier invokes the policy's appraisal clause and names your appraiser."),
        ("Within 20 days", "Appraisers are named", "Each side appoints a competent, independent, disinterested appraiser and shares contact details."),
        ("Within 120 days", "Appraisers inspect and compare", "Both appraisers document the loss, exchange estimates and agree on everything they can."),
        ("By day 240", "Umpire resolves the rest", "Remaining items go to a jointly chosen umpire. Two signatures make the award binding."),
    ]
    html = "".join(f'<div class="step"><div class="step-num">0{i + 1}</div><span class="when">{w}</span><h3>{t}</h3><p>{d}</p></div>'
                   for i, (w, t, d) in enumerate(steps))
    return f'<div class="steps">{html}</div>'


def build_home():
    page = {
        "path": "/",
        "title": "Texas Insurance Appraiser & Umpire | Policyholder Appraiser",
        "description": ("Certified insurance appraiser and umpire for Texas policyholders. Invoke your appraisal clause and "
                        "appoint an independent appraiser."),
    }
    graph = [org_schema(), person_schema(), website_schema(), webpage_schema(page)]
    body = f"""<section class="hero"><div class="wrap hero-in">
<div>
<p class="eyebrow">Certified insurance appraiser &amp; umpire &middot; Texas</p>
<h1>Texas insurance appraiser <span>for policyholders.</span></h1>
<p class="lede">When the carrier will not agree on what your loss costs, or says the damage is wear instead of the storm, your policy lets you invoke appraisal. You appoint an appraiser. We are the appraiser Texas policyholders appoint: competent, independent, and disinterested in the outcome, which is exactly what makes our number hold up.</p>
<div class="hero-actions"><a class="btn btn-brass" href="/contact/">Request a Free Review</a><a class="btn btn-ghost-light" href="/appraisal-process/">How appraisal works</a></div>
<ul class="trust-row"><li>Flat fee, quoted in writing</li><li>{BIZ['license_label']}</li><li>Residential &amp; commercial</li><li>Statewide Texas</li></ul>
</div>
<div class="hero-card">
<p class="eyebrow" style="color:var(--brass-ink)">Is appraisal right for your claim?</p>
<h2>Three quick questions</h2>
<ul class="check-list">
<li>The carrier paid less than repairs cost, or blamed the damage on wear instead of the storm</li>
<li>You have a contractor's estimate, photos or a report that says otherwise</li>
<li>Your policy has an appraisal clause (every Texas home policy will from March 2027)</li>
</ul>
<p class="small">Three yeses and appraisal is probably the fastest, cheapest way to a binding number. In Texas the panel can decide causation too, so a "wear and tear" letter is not the end. Send us the estimate and we will confirm.</p>
<a class="btn btn-dark btn-block" href="/contact/">Send the Carrier's Estimate</a>
</div>
</div></section>

<div class="stats"><div class="wrap stats-in">
<div class="stat"><strong>Amount of loss</strong><span>What appraisal decides. Binding on both sides.</span></div>
<div class="stat"><strong>20 / 120 / 240 days</strong><span>2027 Texas deadlines to name appraisers, agree, and award</span></div>
<div class="stat"><strong>Flat fee</strong><span>Quoted in writing before you appoint us</span></div>
<div class="stat"><strong>No lawsuit required</strong><span>Appraisal is a contractual process, not litigation</span></div>
</div></div>

<section><div class="wrap">
<div class="section-head"><p class="eyebrow">What we do</p><h2>Appraisal and umpire services for disputed property claims</h2><p>One job, done carefully: determine the amount of loss and defend it at the appraiser conference and before the umpire.</p></div>
{service_cards(SERVICES[:6], blurbs=HOME_SERVICE)}
<p style="margin-top:22px"><a class="btn btn-outline" href="/services/">All services, including umpire appointments</a></p>
</div></section>

<section class="dark"><div class="wrap">
<div class="section-head"><p class="eyebrow">How it works</p><h2>Appraisal in four steps</h2><p>Deadlines shown are the Texas residential rules for policies issued or renewed on or after March 1, 2027. Older policies follow the clause as printed.</p></div>
{steps_block(variant="home")}
<p style="margin-top:26px"><a class="btn btn-brass" href="/appraisal-process/">The full process, explained</a> <a class="btn btn-ghost-light" href="/texas-appraisal-rules/">The 2027 Texas rules</a></p>
</div></section>

<section><div class="wrap split">
<div>
<p class="eyebrow">Why independence matters</p>
<h2>An appraiser with a stake in the award is an appraiser the umpire discounts.</h2>
<p>Texas now requires appraisers to be competent, independent of the parties and disinterested in the outcome. We built the practice around that standard before it was a rule:</p>
<ul class="check-list">
<li>Fees are flat or hourly and quoted in writing before you appoint us</li>
<li>We decline appointments on any claim where Rise Public Adjusting acted as public adjuster</li>
<li>Our estimates are written in industry-standard software, line by line, so they can be compared and defended</li>
<li>We tell you when appraisal is the wrong tool, including when the real dispute is coverage</li>
</ul>
<a class="btn btn-dark" href="/about/">About the appraiser</a>
</div>
<div class="panel">
<p class="eyebrow">Credentials</p>
<h3>{BIZ['principal']}</h3>
<p class="small">Certified insurance appraiser and umpire. Texas public adjuster license #{BIZ['license_number']} and independent adjuster license #{BIZ['ia_license_number']}, both verifiable on the TDI license lookup. 463 appraisals closed and settled in 2025. Eight years of carrier-side adjusting and six years of hands-on construction behind every estimate. <a href="/joseph-dittman/" style="color:#fff;font-weight:700">Full bio &rarr;</a></p>
<img src="/img/joseph-dittman-appraiser.webp" alt="{BIZ['principal']}, appraiser and licensed Texas public adjuster" class="portrait" width="320" height="320" loading="lazy" style="margin-top:16px">
</div>
</div></section>

<section class="sand"><div class="wrap">
<div class="section-head"><p class="eyebrow">Guides</p><h2>Understand the process before you start it</h2></div>
{guide_cards(GUIDES, blurbs=HOME_GUIDE)}
</div></section>

<section><div class="wrap">
<div class="section-head"><p class="eyebrow">Statewide</p><h2>Insurance appraiser in every major Texas city</h2><p>Based in Houston, working everywhere in Texas. Each city page covers the storms, housing stock and county courts that shape appraisals there.</p></div>
{city_cards(compact=True)}
</div></section>

{faq_block(FAQ[:8], answers=False)}
{contact_section()}
"""
    write("/", head(page, graph) + header("/") + body + footer())


def build_services_index():
    page = {"path": "/services/", "title": "Insurance Appraisal Services in Texas | Appraiser & Umpire",
            "description": "Policyholder-appointed appraiser and neutral umpire for residential and commercial property claims in Texas: roof, hail, hurricane, water, fire.",
            "eyebrow": "Services", "h1": "Appraisal &amp; Umpire <span>Services</span>",
            "intro": "We serve in two roles only: the appraiser a policyholder appoints under the appraisal clause, and the neutral umpire both appraisers select. Pick the loss type below."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema([("Home", "/"), ("Services", "/services/")])]
    body = page_hero(page, [("Home", "/"), ("Services", "/services/")]) + f"""
<section><div class="wrap">{service_cards(SERVICES)}</div></section>
<section class="sand"><div class="wrap split">
<div><p class="eyebrow">What we do not do</p><h2>Appraisal has limits. We respect them.</h2>
<p>Appraisal decides the amount of loss, which in Texas includes causation: a panel can decide how much damage the storm caused versus wear or a prior event (State Farm Lloyds v. Johnson, Tex. 2009). It does not decide pure policy-interpretation questions or the carrier's conduct. When a dispute is really about policy wording, we will say so and point you to the right resource rather than take an engagement that cannot help you.</p>
<p>We also do not serve as appraiser on any claim where Rise Public Adjusting acted as public adjuster. Independence is not a marketing line; it is the qualification.</p></div>
<div class="panel panel-light"><h3>Not sure which applies?</h3><p>Send the carrier's estimate and letters. We will reply within one business day with a plain answer: appraisal, public adjuster, attorney, or wait.</p><a class="btn btn-dark" href="/contact/">Request a Free Review</a></div>
</div></section>
""" + faq_block(FAQ[:6], answers=False) + contact_section("Not sure which service fits? Send the estimate.", compact=True)
    write(page["path"], head(page, graph) + header("/services/") + body + footer())


def build_service(s):
    page = dict(s)
    graph = [org_schema(), website_schema(), webpage_schema(page), service_schema(s),
             breadcrumb_schema([("Home", "/"), ("Services", "/services/"), (s["h1_plain"], s["path"])])]
    body = page_hero(page, [("Home", "/"), ("Services", "/services/"), (s["nav_label"], s["path"])]) + f"""
<section><div class="wrap prose-grid">
<article class="prose">{s['body']}{author_box()}</article>
{sidebar(s['path'])}
</div></section>
""" + faq_block(FAQ[:5], heading=f"Questions about {s['nav_label'].lower()}", answers=False) + contact_section(f"Start a {s['nav_label'].lower()} review.", compact=True)
    write(s["path"], head(page, graph) + header("/services/") + body + footer())


def build_process():
    page = {"path": "/appraisal-process/", "title": "Insurance Appraisal Process Explained, Step by Step | Texas",
            "description": "The insurance appraisal process step by step: the demand, appointing appraisers, the inspection, the umpire and the award, with Texas deadlines.",
            "eyebrow": "The process", "h1": "The Insurance Appraisal Process, <span>Step by Step</span>",
            "intro": "Appraisal is the dispute-resolution process written into most property policies for one question: how much is the loss? Here is each step, who does what, and the deadlines that now apply in Texas."}
    graph = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema([("Home", "/"), ("How Appraisal Works", page["path"])]),
             {"@type": "HowTo", "name": "How to resolve a disputed Texas property claim through appraisal",
              "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate([
                  ("Confirm appraisal fits", "The dispute is about the amount of loss: scope, price, or what the covered event caused. In Texas, causation is appraisable."),
                  ("Demand appraisal in writing", "Deliver a written demand to the carrier that invokes the policy's appraisal clause and names your appraiser."),
                  ("Appraisers are appointed", "Each party names a competent, independent, disinterested appraiser within 20 days under the 2027 Texas rules."),
                  ("Inspection and estimates", "Both appraisers inspect, document and price the loss, then compare estimates line by line and agree where they can."),
                  ("Umpire selection", "If items remain in dispute, the appraisers jointly choose an umpire within 15 days; a court can appoint one if they cannot agree."),
                  ("Award", "The umpire decides the disputed items. An award signed by two of the three is binding as to the amount of loss."),
              ])]}]
    body = page_hero(page, [("Home", "/"), ("How Appraisal Works", page["path"])]) + f"""
<section class="dark" style="padding-top:48px"><div class="wrap">{steps_block()}</div></section>
<section><div class="wrap prose-grid">
<article class="prose">
<h2>Step 1: Confirm that appraisal fits the dispute</h2>
<p>Appraisal exists to answer one question: the <strong>amount of loss</strong>. In Texas that question includes causation. Since State Farm Lloyds v. Johnson (Tex. 2009), an appraisal panel may decide how much of the damage the covered event caused and how much is wear, deterioration or a prior loss, and award the covered portion. So "we have paid the reasonable cost of repair" is an appraisable dispute, and "the damage is the result of wear and tear" is one too. What a panel may not decide is a pure policy question: whether the policy's wording excludes a category of loss, or whether a condition of coverage was satisfied. Read the carrier's letter with that line in mind, and send it to us if you are unsure which side it falls on.</p>

<h2>Step 2: Read the appraisal clause</h2>
<p>Find the Conditions section of the full policy. The appraisal clause will tell you who may demand appraisal, any time limit, how an umpire is chosen if the appraisers cannot agree, and how costs are split. For residential and personal auto policies issued or renewed on or after March 1, 2027, Texas requires the clause to give both sides a unilateral right to demand appraisal, with no impasse requirement, and to state the deadlines summarized on this page. Commercial and TWIA policies keep their own clauses.</p>

<h2>Step 3: Demand appraisal in writing</h2>
<p>Send a short letter to the carrier's claims department identifying the claim, invoking the appraisal provision and naming your appraiser. Deliver it in a way you can prove, such as certified mail plus email, and keep a copy. Our <a href="/guides/invoke-appraisal-clause/">guide to invoking the appraisal clause</a> includes a sample letter. Under the 2027 rules the demand generally must be made before the policy's limitations period for filing suit runs, and special timing applies once a lawsuit is filed.</p>

<h2>Step 4: Both sides appoint appraisers</h2>
<p>Each party hires its own appraiser and gives the other side the appraiser's name and contact information. The 2027 Texas rules allow 20 days. Appraisers must be competent for the type of loss, independent of the parties and disinterested in the outcome; on residential dwelling losses they must also be a licensed adjuster or public adjuster with estimating experience, an engineer or architect, or a qualified tradesperson. Ask any appraiser how they are paid and whether they had any prior role in your claim.</p>

<h2>Step 5: Inspection and the appraiser conference</h2>
<p>The appraisers inspect the property, jointly or separately, and each prepares an itemized estimate. They then compare estimates line by line, agree on what they can and list what remains in dispute. A large share of most gaps closes at this stage. Under the 2027 rules the appraisers have 120 days from the demand to attempt agreement.</p>

<h2>Step 6: Umpire selection</h2>
<p>If items remain in dispute, the appraisers jointly choose an umpire, within 15 days under the 2027 rules. The umpire must meet the same qualification and independence standards. If the appraisers cannot agree on a person, either party may ask a county or district court where the property is located to appoint an umpire, after 10 days' written notice to the other side. A policy may also allow the policyholder to use an independent umpire-selection vendor, or the parties may agree in writing on another method.</p>

<h2>Step 7: The award</h2>
<p>Each appraiser submits its position on the disputed items to the umpire, who may inspect and then decides. An award signed by both appraisers, or by one appraiser and the umpire, sets the amount of loss and binds both parties. Under the 2027 rules an umpire award must issue within 240 days of the demand; if it does not, the umpire's engagement ends and a new umpire must be chosen within 15 days. The carrier then pays the award, less the deductible, prior payments and any depreciation the policy allows it to hold until repairs are complete.</p>

<h2>What appraisal costs</h2>
<p>Each party pays its own appraiser. The umpire's fee is typically split equally. We quote a flat or hourly fee in writing before you appoint us, based on the size and complexity of the loss. For most roof and water disputes the fee is small relative to the gap between the carrier's estimate and the real cost of repair.</p>

<div class="callout"><span class="label">Ready to start?</span><p>Send us the carrier's estimate and your policy. We will confirm whether appraisal fits, quote the fee, and prepare the demand for your signature.</p><p><a class="btn btn-brass" href="/contact/">Request a Free Review</a></p></div>
{author_box()}
</article>
{sidebar()}
</div></section>
""" + faq_block(FAQ[:8], answers=False) + contact_section("Ready for step one? Send the carrier's letter.", compact=True)
    write(page["path"], head(page, graph) + header("/appraisal-process/") + body + footer())


def build_guides_index():
    page = {"path": "/guides/", "title": "Insurance Appraisal Guides for Texas Policyholders",
            "description": "Plain-language guides to insurance appraisal in Texas: the 2027 rules, invoking the clause, appraisal vs. public adjuster vs. lawsuit.",
            "eyebrow": "Guides", "h1": "Appraisal Guides for <span>Texas Policyholders</span>",
            "intro": "Everything we wish homeowners knew before they called: how the clause works, what the new Texas rules require, and how to choose between appraisal, a public adjuster and a lawsuit."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema([("Home", "/"), ("Guides", "/guides/")])]
    body = page_hero(page, [("Home", "/"), ("Guides", "/guides/")], actions=False) + f"""
<section><div class="wrap">{guide_cards(GUIDES)}
<div class="grid grid-2" style="margin-top:18px"><a class="card" href="/appraisal-process/"><div class="card-icon">{icon('clock')}</div><h3>How the appraisal process works</h3><p>Seven steps from demand to award, with the Texas deadlines.</p><span class="more">Read &rarr;</span></a>
<a class="card" href="/faq/"><div class="card-icon">{icon('shield')}</div><h3>Frequently asked questions</h3><p>Cost, timing, binding effect, qualifications and more.</p><span class="more">Read &rarr;</span></a></div>
</div></section>
""" + contact_section("Questions about your own claim?", compact=True)
    write(page["path"], head(page, graph) + header("/guides/") + body + footer())


def build_guide(g):
    page = dict(g)
    parent = ("2027 Texas Rules", "/texas-appraisal-rules/") if g["slug"] == "texas-appraisal-rules" else ("Guides", "/guides/")
    active = "/texas-appraisal-rules/" if g["slug"] == "texas-appraisal-rules" else "/guides/"
    trail = [("Home", "/")] + ([parent] if parent[1] != g["path"] else []) + [(g["nav_label"], g["path"])]
    graph = [org_schema(), person_schema(), website_schema(), webpage_schema(page), article_schema(g), breadcrumb_schema(trail)]
    body = page_hero(page, trail, actions=False) + f"""
<section><div class="wrap prose-grid">
<article class="prose">{g['body']}{author_box()}</article>
{sidebar(g['path'])}
</div></section>
""" + contact_section(f"Apply this to your claim.", compact=True)
    write(g["path"], head(page, graph) + header(active) + body + footer())


def build_faq():
    page = {"path": "/faq/", "title": "Insurance Appraisal FAQ for Texas Policyholders",
            "description": "Common questions about insurance appraisal in Texas: what appraisers do, cost, how long it takes, whether the award is binding and who may serve.",
            "eyebrow": "FAQ", "h1": "Insurance Appraisal <span>Questions &amp; Answers</span>",
            "intro": "Straight answers about the appraisal clause, appraiser qualifications, cost, timing and the 2027 Texas rules."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "FAQPage"), faq_schema(FAQ), breadcrumb_schema([("Home", "/"), ("FAQ", "/faq/")])]
    body = page_hero(page, [("Home", "/"), ("FAQ", "/faq/")], actions=False) + faq_block(FAQ, heading="Everything policyholders ask us", link=False) + contact_section("Still have a question? Ask it here.", compact=True)
    write(page["path"], head(page, graph) + header("/faq/") + body + footer())


def build_about():
    city_list = ", ".join(f'<a href="{c["path"]}">{c["name"]}</a>' for c in CITIES[:-1]) + f' and <a href="{CITIES[-1]["path"]}">{CITIES[-1]["name"]}</a>'
    page = {"path": "/about/", "title": "About Policyholder Appraiser | Texas Appraisal Practice",
            "description": "The statewide appraisal and umpire practice of Joseph Dittman, a certified insurance appraiser and licensed Texas adjuster.",
            "eyebrow": "About", "h1": "An appraisal practice built on <span>independence</span>",
            "intro": "Policyholder Appraiser is the appraisal and umpire practice of Joseph Dittman and Rise Public Adjusting LLC. It exists because Texas policyholders deserve an appraiser who is as prepared as the carrier's, as impartial as the rule requires, and available in every corner of the state."}
    graph = [org_schema(), person_schema(), website_schema(), webpage_schema(page, "AboutPage"), breadcrumb_schema([("Home", "/"), ("About", "/about/")])]
    body = page_hero(page, [("Home", "/"), ("About", "/about/")]) + f"""
<section><div class="wrap split">
<div><img src="/img/joseph-dittman-appraiser.webp" alt="{BIZ['principal']}, certified insurance appraiser and umpire" class="portrait" width="320" height="320"><p class="center" style="margin-top:18px"><a class="btn btn-dark" href="/joseph-dittman/">Read Joseph's full bio</a></p></div>
<div class="prose">
<h2>{BIZ['principal']}</h2>
<p><strong>{BIZ['principal_title']}</strong></p>
<p>Joseph Dittman is a certified insurance appraiser and umpire who has worked property claims from every side of the table: eight years as an independent adjuster for carriers, hands-on years as a construction foreman, and public adjusting on the policyholder side with Rise Public Adjusting LLC. He holds Texas public adjuster license #{BIZ['license_number']} and independent adjuster license #{BIZ['ia_license_number']}, both verifiable on the TDI license lookup, and closed 463 appraisals in 2025 alone.</p>
<p>He works all over Texas, not just Houston. Appraisal and umpire engagements run statewide, including {city_list}, with the same flat, written fee wherever the property sits.</p>
<p>Policyholder Appraiser is the part of that practice devoted to the appraisal clause. In the appraiser's chair Joseph's job changes: no longer an advocate negotiating a settlement, but an independent professional determining the amount of loss and defending that determination to the carrier's appraiser and, where needed, to an umpire.</p>
<h3>How we keep the roles separate</h3>
<ul>
<li>We do not serve as appraiser on any claim in which Rise Public Adjusting acted as the public adjuster.</li>
<li>Appraisal and umpire fees are flat or hourly and quoted in writing before you appoint us.</li>
<li>Before accepting an umpire appointment we disclose any prior dealings with either party, either appraiser or counsel.</li>
<li>We decline engagements where appraisal cannot help, such as disputes that turn purely on policy wording.</li>
</ul>
<h3>Qualified under the 2027 Texas rules</h3>
<p>28 TAC §5.9804 requires appraisers and umpires on residential dwelling losses to be competent by training or experience, independent of the parties, disinterested in the outcome, and either a licensed adjuster or public adjuster with residential estimating experience, an engineer or architect, or a qualified tradesperson. Joseph meets the adjuster standard twice over, with daily residential and commercial estimating experience and a construction background behind it.</p>
</div>
</div></section>
<section class="sand"><div class="wrap">
<div class="section-head"><p class="eyebrow">Where we work</p><h2>Statewide Texas, city by city</h2><p>Rise Public Adjusting LLC also operates public adjusting practices in Texas. Those practices represent policyholders in presenting and negotiating claims; Policyholder Appraiser is kept separate so that appraisal work remains independent. Appraisal and umpire engagements are accepted anywhere in the state.</p></div>
{city_cards(compact=True)}
</div></section>
""" + contact_section("Work with an independent appraiser.", compact=True)
    write(page["path"], head(page, graph) + header("/about/") + body + footer())

def build_areas():
    page = {"path": "/service-areas/", "title": "Insurance Appraiser Service Areas | Every Major Texas City",
            "description": "Independent insurance appraiser and umpire serving every major Texas city: Houston, San Antonio, Dallas, Fort Worth, Austin, El Paso and more.",
            "eyebrow": "Service areas", "h1": "Insurance appraiser <span>across Texas</span>",
            "intro": "The appraisal clause works the same way in every Texas county, but the storms, the housing and the courts that appoint umpires do not. Each city below has its own page covering what drives appraisals there. Based in Houston; travel statewide is included in the quoted fee."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema([("Home", "/"), ("Service Areas", "/service-areas/")]),
             {"@type": "ItemList", "name": "Texas cities served", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": f"Insurance appraiser in {c['name']}, TX", "url": url(c["path"])} for i, c in enumerate(CITIES)]}]
    body = page_hero(page, [("Home", "/"), ("Service Areas", "/service-areas/")]) + f"""
<section><div class="wrap">{city_cards()}
<p style="margin-top:22px;color:var(--slate)">Not listed? If the property is in Texas, call. Remote document review and video walk-throughs cover the early steps for distant properties before an in-person inspection.</p></div></section>
""" + contact_section("Tell us where the property is.", compact=True)
    write(page["path"], head(page, graph) + header("/service-areas/") + body + footer())


def build_city(c):
    K, KT, post = kw(c), kw_title(c), post_path(c)
    title = f"{KT} | Policyholder Appraiser"
    desc = c["description"]
    for cut in (" Call (832) 503-5866.", " (832) 503-5866.", " Flat fee, binding award.", " Binding award, flat fee.", " Flat fee quoted in writing.", " Flat fee.", " Binding award without a lawsuit.", " Flat fee, binding award, no lawsuit."):
        if len(desc) > 145:
            desc = desc.replace(cut, "")
    page = {"path": c["path"], "title": title, "description": desc, "eyebrow": f"{K} &middot; serving {c['county']}",
            "h1": f"{KT} <span>for Policyholders</span>", "intro": c["intro"]}
    trail = [("Home", "/"), ("Areas Served", "/service-areas/"), (KT, c["path"])]
    graph = [org_schema(), person_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), faq_schema(c["faq"]),
             {"@type": "Service", "@id": url(c["path"]) + "#service", "name": f"{KT} services",
              "serviceType": "Insurance claim appraisal and umpire services", "provider": {"@id": ORG_ID},
              "areaServed": [{"@type": "City", "name": c["name"], "containedInPlace": {"@type": "State", "name": "Texas"}}] + [{"@type": "City", "name": n} for n in c["nearby"]],
              "url": url(c["path"]), "description": c["description"]}]
    others = [o for o in CITIES if o["slug"] != c["slug"]]
    other_links = " &middot; ".join(f'<a href="{o["path"]}">{kw_title(o)}</a>' for o in others)
    nearby = "".join(f"<li>{n}</li>" for n in c["nearby"])
    faqs = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in c["faq"])
    extra = EXTRA[c["slug"]].format(kw=K, city=c["name"], post=post)
    storm = STORMS[c["slug"]]
    body = page_hero(page, trail) + f"""
<section><div class="wrap prose-grid">
<article class="prose">{c['body']}
{extra}
<h2>Questions for a {K}</h2>
{faqs}
<p class="callout"><span class="label">Appoint a {K}</span>We cover {c['county']} and the properties around {c['nearby'][0]}, {c['nearby'][1]} and {c['nearby'][2]}. Send the carrier's estimate for a {c['name']} claim and the fee comes back in writing.</p>
{author_box()}
</article>
<aside class="sidebar">
<div class="side-card"><h3>Your {K}</h3><p>Property in {c['county']}? Send the carrier's estimate and we reply the next business day.</p><a class="btn btn-brass" href="/contact/">Request a Free Review</a><p style="margin:12px 0 0;text-align:center"><a href="tel:{TEL}" style="color:#fff;text-decoration:none;font-weight:700">Call {PHONE}</a></p></div>
<div class="side-card light"><h3>{c['name']} storm history</h3><p>{storm['description']}</p><div class="side-list"><a href="{post}">Read the {c['name']} storm timeline</a></div></div>
<div class="side-card light"><h3>Also serving near {c['name']}</h3><ul class="pill-row" style="margin-top:4px">{nearby}</ul></div>
<div class="side-card light"><h3>Appraisal services</h3><div class="side-list">{''.join(f'<a href="{s["path"]}">{s["nav_label"]}</a>' for s in SERVICES)}</div></div>
<div class="side-card light"><h3>Guides</h3><div class="side-list"><a href="/appraisal-process/">How appraisal works</a><a href="/texas-appraisal-rules/">2027 Texas appraisal rules</a><a href="/guides/invoke-appraisal-clause/">How to invoke the appraisal clause</a></div></div>
</aside>
</div></section>
<section class="sand"><div class="wrap"><p class="eyebrow">Insurance appraiser in other Texas cities</p><p class="footer-cities" style="color:var(--slate)">{other_links}</p></div></section>
""" + contact_section(f"Start your {c['name']} appraisal review.", compact=True)
    write(c["path"], head(page, graph) + header("/service-areas/") + body + footer())


def build_blog_index():
    page = {"path": "/blog/", "title": "Texas Storm History Blog | Policyholder Appraiser",
            "description": "City-by-city storm histories for Texas: the hurricanes, hail, tornadoes, floods and freezes behind property insurance claims, and what each means for appraisal.",
            "eyebrow": "Blog", "h1": "Texas Storm History, <span>City by City</span>",
            "intro": "Every underpaid claim starts with a storm. These posts lay out the major weather events in each Texas city we serve, what carriers did with the claims that followed, and how appraisal resolves the disputes that remain."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema([("Home", "/"), ("Blog", "/blog/")]),
             {"@type": "Blog", "@id": url("/blog/#blog"), "name": "Policyholder Appraiser storm history blog", "publisher": {"@id": ORG_ID},
              "blogPost": [{"@type": "BlogPosting", "headline": STORMS[c["slug"]]["title"], "url": url(post_path(c)), "datePublished": STORMS_PUBLISHED} for c in CITIES]}]
    cards = "".join(f'<a class="card" href="{post_path(c)}"><div class="card-icon">{icon("wind")}</div><h3>{STORMS[c["slug"]]["title"].split(":")[0]}</h3><p>{BLOG_TEASERS[c["slug"]]}</p><span class="more">Read the {c["name"]} timeline &rarr;</span></a>' for c in CITIES)
    body = page_hero(page, [("Home", "/"), ("Blog", "/blog/")], actions=False) + f"""
<section><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>
""" + contact_section("Your storm is probably on this list.", compact=True)
    write(page["path"], head(page, graph) + header("/blog/") + body + footer())


def build_post(c):
    s = STORMS[c["slug"]]
    path = post_path(c)
    page = {"path": path, "title": s["title"], "description": s["description"], "eyebrow": f"Storm history &middot; {c['name']}, Texas",
            "h1": s["h1"], "intro": s["intro"], "published": STORMS_PUBLISHED}
    trail = [("Home", "/"), ("Blog", "/blog/"), (f"{c['name']} storm history", path)]
    graph = [org_schema(), person_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail),
             {"@type": "BlogPosting", "@id": url(path) + "#post", "headline": s["title"], "description": s["description"],
              "author": {"@id": PERSON_ID}, "publisher": {"@id": ORG_ID}, "datePublished": STORMS_PUBLISHED, "dateModified": TODAY,
              "mainEntityOfPage": url(path), "image": url("/img/og-image.png"), "about": {"@type": "City", "name": c["name"] + ", TX"}}]
    svc = {s_["slug"]: s_["path"] for s_ in SERVICES}
    body_html = s["body"].replace("<h2>What this history means for your claim</h2>", f"<h2>What this means for a {c['name']} claim today</h2>").format(city_url=c["path"], kw=kw(c), hail=svc["hail-and-roof-claim-appraisal"], wind=svc["hurricane-and-wind-claim-appraisal"],
                                 water=svc["water-damage-claim-appraisal"], fire=svc["fire-and-smoke-claim-appraisal"], home=svc["residential-property-appraisal"])
    others = [o for o in CITIES if o["slug"] != c["slug"]]
    other_posts = " &middot; ".join(f'<a href="{post_path(o)}">{o["name"]}</a>' for o in others)
    body = page_hero(page, trail, actions=False) + f"""
<section><div class="wrap prose-grid">
<article class="prose">{body_html}{author_box()}</article>
<aside class="sidebar">
<div class="side-card"><h3>{kw_title(c)}</h3><p>{c['county']} claims from any storm on this page.</p><a class="btn btn-brass" href="{c['path']}">{kw_title(c)} services</a><p style="margin:12px 0 0;text-align:center"><a href="tel:{TEL}" style="color:#fff;text-decoration:none;font-weight:700">Call {PHONE}</a></p></div>
<div class="side-card light"><h3>Appraisal services</h3><div class="side-list">{''.join(f'<a href="{s_["path"]}">{s_["nav_label"]}</a>' for s_ in SERVICES)}</div></div>
<div class="side-card light"><h3>Guides</h3><div class="side-list"><a href="/appraisal-process/">How appraisal works</a><a href="/texas-appraisal-rules/">2027 Texas appraisal rules</a><a href="/guides/invoke-appraisal-clause/">How to invoke the appraisal clause</a></div></div>
</aside>
</div></section>
<section class="sand"><div class="wrap"><p class="eyebrow">Storm history in other Texas cities</p><p class="footer-cities" style="color:var(--slate)">{other_posts}</p></div></section>
""" + contact_section(f"Underpaid after one of these {c['name']} storms?", compact=True)
    write(path, head(page, graph) + header("/blog/") + body + footer())


def build_bio():
    b = BIO
    page = {"path": b["path"], "title": b["title"], "description": b["description"], "eyebrow": b["eyebrow"], "h1": b["h1"], "intro": b["intro"]}
    trail = [("Home", "/"), ("About", "/about/"), ("Joseph Dittman", b["path"])]
    person = person_schema(); person["description"] = b["description"]
    graph = [org_schema(), person, website_schema(), webpage_schema(page, "ProfilePage"), breadcrumb_schema(trail)]
    stats = "".join(f'<div class="stat"><strong>{n}</strong><span>{d}</span></div>' for n, d in b["stats"])
    lic = "".join(f"<li>{x}</li>" for x in b["licenses"])
    skills = "".join(f"<li>{x}</li>" for x in b["skills"])
    testimony = "".join(f"<li>{x}</li>" for x in b["testimony"])
    city_list = ", ".join(f'<a href="{c["path"]}">{c["name"]}</a>' for c in CITIES)
    writing = "".join(f'<li><a href="{u}" rel="noopener">{t_}</a></li>' for t_, u in b["writing"])
    body = page_hero(page, trail) + f"""
<div class="stats"><div class="wrap stats-in">{stats}</div></div>
<section><div class="wrap prose-grid">
<article class="prose" id="person">
<h2>Appraisal and umpire experience (2022 to present)</h2>
<p>463 appraisals closed and settled in 2025. Loss types handled: {b['loss_types']}. Engagements have been balanced between policyholder-appointed and carrier-appointed appraiser roles, which supports impartial umpire selection and award drafting that both sides can accept.</p>
<p>Issues regularly evaluated: {b['issues']}.</p>
<p>Carriers appraised for or against include {b['appraisal_carriers']}.</p>

<h2>Sworn testimony</h2>
<ul>{testimony}</ul>

<h2>Carrier-side independent adjusting (2018 to 2025)</h2>
<p><strong>Commercial:</strong> {b['ia_commercial']}.</p>
<p><strong>E&amp;O and liability:</strong> {b['ia_liability']}.</p>
<p><strong>Residential:</strong> {b['ia_residential']}.</p>
<p>Loss types: wind, hail, sewage backups, pipe bursts, fire, tornado, hurricane, explosions, mitigation and complex multi-trade losses. Eight years of writing carrier estimates is why the carrier's appraiser cannot surprise us with a line item.</p>

<h2>Policyholder-side public adjusting</h2>
<p>{b['pa']} Policyholder Appraiser is kept separate from that work: we do not serve as appraiser on any claim where Rise Public Adjusting acted as public adjuster.</p>

<h2>Construction and trades background</h2>
<p>{b['construction']}</p>

<h2>Licenses and certifications</h2>
<ul>{lic}</ul>

<h2>Umpire-relevant skills</h2>
<ul>{skills}</ul>

<h2>Writing</h2>
<ul>{writing}<li>Author and publisher at <a href="https://txinsuranceappraiser.com" rel="noopener">txinsuranceappraiser.com</a></li></ul>

<h2>Where Joseph works</h2>
<p>Statewide Texas, including {city_list}, and the surrounding counties of each. Travel is included in the quoted fee.</p>
</article>
<aside class="sidebar">
<div class="side-card"><img src="/img/joseph-dittman-appraiser.webp" alt="{BIZ['principal']}, certified insurance appraiser and umpire" class="portrait" width="220" height="220" style="width:160px;margin-bottom:14px"><h3>Appoint Joseph as your appraiser</h3><p>Or request him as umpire. Written fee before any engagement.</p><a class="btn btn-brass" href="/contact/">Contact</a><p style="margin:12px 0 0;text-align:center"><a href="tel:{TEL}" style="color:#fff;text-decoration:none;font-weight:700">Call {PHONE}</a></p></div>
<div class="side-card light"><h3>Services</h3><div class="side-list">{''.join(f'<a href="{s["path"]}">{s["nav_label"]}</a>' for s in SERVICES)}</div></div>
</aside>
</div></section>
""" + contact_section("Appoint Joseph as your appraiser or umpire.", compact=True)
    write(page["path"], head(page, graph) + header("/about/") + body + footer())

def build_contact():
    page = {"path": "/contact/", "title": "Contact Policyholder Appraiser | Free Claim Review",
            "description": "Send us the carrier's estimate for a free appraisal review, or call or text (832) 503-5866. Independent insurance appraiser serving all of Texas.",
            "eyebrow": "Contact", "h1": "Request a <span>free appraisal review</span>",
            "intro": "Send the carrier's estimate and letters. Within one business day we will tell you whether appraisal fits your dispute and, if it does, quote a flat fee in writing."}
    graph = [org_schema(), website_schema(), webpage_schema(page, "ContactPage"), breadcrumb_schema([("Home", "/"), ("Contact", "/contact/")])]
    body = page_hero(page, [("Home", "/"), ("Contact", "/contact/")], actions=False) + f"""
<section class="contact" style="padding-top:48px"><div class="wrap split">
<div>
<h2>Three ways to reach us</h2>
<div class="contact-meta">
<a href="tel:{TEL}">Call {PHONE}<span>{BIZ['hours']}</span></a>
<a href="sms:{TEL}">Text {PHONE}<span>Photos of the estimate and the damage are welcome</span></a>
<a href="mailto:{BIZ['email']}">{BIZ['email']}<span>Attach the carrier's estimate, its letters and your policy</span></a>
</div>
<h3 style="margin-top:32px;color:#fff">What to have ready</h3>
<ul class="check-list">
<li>The carrier's estimate and acceptance or payment letter</li>
<li>Your contractor's or public adjuster's estimate, if any</li>
<li>Your policy, including the appraisal clause</li>
<li>Date of loss and date the claim was filed</li>
</ul>
<p class="small" style="color:#a9b6c4">Appraisers and attorneys seeking an umpire: include the claim number, both appraisers' names and the policy's appraisal clause.</p>
</div>
{contact_form()}
</div></section>
""" + faq_block(FAQ[:6], heading="Before you call, the questions we hear most", answers=False, link=True)
    write(page["path"], head(page, graph) + header("/contact/") + body + footer())


def build_thanks():
    page = {"path": "/thank-you/", "title": "Thanks | Policyholder Appraiser", "description": "We received your message and will reply within one business day.",
            "robots": "noindex, nofollow"}
    graph = [org_schema(), website_schema(), webpage_schema(page)]
    body = f"""<section class="notfound"><div class="wrap">
<p class="eyebrow">Message received</p>
<h1 style="font-size:clamp(2rem,5vw,3.2rem)">Thank you.</h1>
<p class="lede" style="margin-inline:auto">We will review what you sent and reply within one business day. If the matter is time-sensitive, call or text {PHONE}.</p>
<p style="margin-top:24px"><a class="btn btn-dark" href="/">Back to the homepage</a> <a class="btn btn-outline" href="/appraisal-process/">Read how appraisal works</a></p>
</div></section>"""
    write(page["path"], head(page, graph) + header() + body + footer())


def build_legal(path, title, h1, body_html):
    page = {"path": path, "title": f"{title} | Policyholder Appraiser", "description": f"{title} for policyholderappraiser.com.",
            "eyebrow": "Legal", "h1": h1, "intro": ""}
    graph = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema([("Home", "/"), (title, path)])]
    hero = f"""<section class="page-hero"><div class="wrap">{crumbs([("Home", "/"), (title, path)])}<p class="eyebrow">Legal</p><h1>{h1}</h1></div></section>"""
    body = hero + f'<section class="legal"><div class="wrap"><article class="prose">{body_html}</article></div></section>'
    write(path, head(page, graph) + header() + body + footer())


def build_404():
    page = {"path": "/404.html", "title": "Page Not Found | Policyholder Appraiser", "description": "That page does not exist.", "robots": "noindex, nofollow"}
    graph = [org_schema(), website_schema()]
    body = f"""<section class="notfound"><div class="wrap">
<p class="eyebrow">Error 404</p><h1>Page not found</h1>
<p class="lede" style="margin-inline:auto">The page you were looking for has moved or never existed. Try one of these instead.</p>
<p style="margin-top:24px"><a class="btn btn-dark" href="/">Homepage</a> <a class="btn btn-outline" href="/services/">Services</a> <a class="btn btn-outline" href="/appraisal-process/">How appraisal works</a> <a class="btn btn-outline" href="/contact/">Contact</a></p>
</div></section>"""
    html = head(page, graph).replace('<link rel="canonical" href="https://policyholderappraiser.com/404.html">\n', "") + header() + body + footer()
    write("/404.html", html)


def build_sitemap(paths):
    items = "".join(f"<url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod></url>" for p in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def copy_static():
    for name in os.listdir(SRC):
        src = os.path.join(SRC, name)
        dst = os.path.join(OUT, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_static()
    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_process()
    build_guides_index()
    for g in GUIDES:
        build_guide(g)
    build_faq()
    build_about()
    build_areas()
    for c in CITIES:
        build_city(c)
        build_post(c)
    build_blog_index()
    build_bio()
    build_contact()
    build_thanks()
    build_legal("/privacy-policy/", "Privacy Policy", "Privacy Policy", PRIVACY_BODY)
    build_legal("/terms-of-use/", "Terms of Use", "Terms of Use", TERMS_BODY)
    build_404()
    indexable = ["/", "/services/"] + [s["path"] for s in SERVICES] + ["/appraisal-process/", "/guides/"] + \
                [g["path"] for g in GUIDES] + ["/faq/", "/about/", BIO["path"], "/service-areas/"] + [c["path"] for c in CITIES] + ["/blog/"] + [post_path(c) for c in CITIES] + ["/contact/", "/privacy-policy/", "/terms-of-use/"]
    build_sitemap(indexable)
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"built {len(indexable)} pages, {n} files -> {OUT}")


if __name__ == "__main__":
    main()
