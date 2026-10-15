#!/usr/bin/env python3
"""Builds destinhurricane.com (Destin Hurricane) into ./public.

Every file in src/pages/ is one page. Its first line is an HTML comment that
holds a JSON object (path, title, description and optional page-head, FAQ and
schema fields, documented in README.md); the rest is the page body. build.py
wraps each body in the shared layout below, renders the page head, breadcrumb,
FAQ block and JSON-LD from the JSON header, copies src/static/ verbatim and
writes sitemap.xml and robots.txt.

    python3 build.py
"""

import hashlib
import html
import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

# Indexable. Set True only for a test domain: every page gets noindex and
# robots.txt disallows everything.
STAGING = False

SITE = {
    "name": "Destin Hurricane",
    "origin": "https://destinhurricane.com",
    "tagline": "Destin hurricane information and storm-claim help for Okaloosa and Walton counties",
    "place": "Destin, Florida",
    "lat": 30.3935,
    "lon": -86.4958,
}

# The advertising law firm. Florida Bar Rule 4-7.12 disclosures (firm name,
# office location) render in the header strip, footer, claim card and forms.
FIRM = {
    "name": "The Lawgical Firm",
    "legal_name": "The Lawgical Firm, P.A.",
    "site": "https://thelawgicalfirm.com/",
    "hurricane_url": "https://thelawgicalfirm.com/residential-property-insurance-claims/hurricane-windstorm/",
    "phone_display": "(850) 203-3385",
    "phone_href": "+18502033385",
    # Local office first; the principal office is named in the disclosure.
    "offices": [
        {"label": "Destin office", "street": "34990 Emerald Coast Pkwy, Ste 359", "city": "Destin", "region": "FL", "zip": "32541"},
        {"label": "Principal office", "street": "3191 Maguire Blvd, Ste 160", "city": "Orlando", "region": "FL", "zip": "32803"},
    ],
    "principal_city": "Orlando",
}

GA_ID = "G-26F0N02ESV"
TODAY = date.today().isoformat()
REVIEWED = "October 2026"

# Desktop navigation (the mobile panel adds the claim pages below it).
NAV = [
    ("Storm desk", "/destin-hurricane-tracker/"),
    ("Evacuation zones", "/okaloosa-walton-evacuation-zones/"),
    ("Storm surge", "/destin-storm-surge/"),
    ("Isaias claims", "/hurricane-isaias-claims-destin/"),
    ("Claim lawyer", "/destin-hurricane-claim-lawyer/"),
    ("Our firm", "/our-firm/"),
]
NAV_MORE = [
    ("Denied claim", "/denied-hurricane-claim-destin/"),
    ("Underpaid claim", "/underpaid-hurricane-claim-destin/"),
    ("Delayed claim", "/delayed-hurricane-claim-destin/"),
    ("Weather & radar", "/destin-weather/"),
    ("Shelters", "/walton-okaloosa-hurricane-shelters/"),
    ("News", "/news/"),
]


def esc(text):
    return html.escape(str(text), quote=True)


def strip_tags(text):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text))).strip()


def asset_version(rel):
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def crumbs_for(page):
    """[(name, path), ...] from Home to the current page."""
    trail = [("Home", "/")]
    for name, path in page.get("crumbs", []):
        trail.append((name, path))
    trail.append((page.get("crumb") or strip_tags(page.get("h1", page["title"].split(" | ")[0])), page["path"]))
    return trail


# ---------------------------------------------------------------- head + schema

def firm_schema():
    return {
        "@type": "LegalService",
        "@id": SITE["origin"] + "/#firm",
        "name": FIRM["legal_name"],
        "url": FIRM["site"],
        "telephone": FIRM["phone_href"],
        "image": SITE["origin"] + "/assets/img/lawgical-logo.png",
        "address": [{"@type": "PostalAddress", "streetAddress": o["street"], "addressLocality": o["city"],
                     "addressRegion": o["region"], "postalCode": o["zip"], "addressCountry": "US"} for o in FIRM["offices"]],
        "areaServed": [
            {"@type": "City", "name": "Destin, FL"},
            {"@type": "AdministrativeArea", "name": "Okaloosa County, FL"},
            {"@type": "AdministrativeArea", "name": "Walton County, FL"},
            {"@type": "State", "name": "Florida"},
        ],
        "knowsAbout": ["Hurricane insurance claims", "Windstorm claims", "Denied property insurance claims",
                       "Underpaid property insurance claims", "Roof damage claims", "Water damage claims"],
    }


def page_schema(page):
    canonical = SITE["origin"] + page["path"]
    graph = [
        {"@type": "WebSite", "@id": SITE["origin"] + "/#website", "url": SITE["origin"] + "/",
         "name": SITE["name"], "description": SITE["tagline"], "inLanguage": "en-US",
         "publisher": {"@id": SITE["origin"] + "/#firm"}},
        firm_schema(),
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
         "description": page["description"], "isPartOf": {"@id": SITE["origin"] + "/#website"},
         "inLanguage": "en-US",
         "about": {"@type": "Place", "name": page.get("place", SITE["place"]),
                   "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lon"]}},
         "dateModified": page.get("modified", TODAY)},
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE["origin"] + path}
            for i, (name, path) in enumerate(crumbs_for(page))]})
    if page.get("article"):
        graph.append({
            "@type": "Article", "@id": canonical + "#article", "headline": strip_tags(page.get("h1", page["title"]))[:110],
            "description": page["description"], "mainEntityOfPage": {"@id": canonical + "#webpage"},
            "datePublished": page.get("published", "2026-10-15"), "dateModified": page.get("modified", TODAY),
            "author": {"@id": SITE["origin"] + "/#firm"}, "publisher": {"@id": SITE["origin"] + "/#firm"},
            "image": SITE["origin"] + "/assets/og-image.png", "inLanguage": "en-US"})
    if page.get("faq"):
        graph.append({"@type": "FAQPage", "@id": canonical + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in page["faq"]]})
    graph.extend(page.get("schema", []))
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    article = ""
    if page.get("article"):
        article = (f'<meta property="article:published_time" content="{page.get("published", "2026-10-15")}">\n'
                   f'<meta property="article:modified_time" content="{page.get("modified", TODAY)}">\n')
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d6e63">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{'article' if page.get('article') else 'website'}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['origin']}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{article}<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Destin, Florida">
<meta name="geo.position" content="{SITE['lat']};{SITE['lon']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&amp;family=Figtree:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={asset_version('assets/css/site.css')}">
<script type="application/ld+json">
{page_schema(page)}
</script>
</head>
<body class="{page.get('body_class', 'pg')}">
<a class="skip" href="#content">Skip to main content</a>
"""


# ------------------------------------------------------------------ chrome

MARK_SVG = ('<svg class="mark-icon" viewBox="0 0 44 44" aria-hidden="true" focusable="false">'
            '<circle cx="22" cy="22" r="21" fill="#0d6e63"/>'
            '<path d="M22 8.5a8.5 8.5 0 0 0-8.5 8.5h17A8.5 8.5 0 0 0 22 8.5z" fill="#f4b942"/>'
            '<path d="M6 23c3 0 3-2.4 6-2.4s3 2.4 6 2.4 3-2.4 6-2.4 3 2.4 6 2.4 3-2.4 6-2.4" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M8 30c2.6 0 2.6-2 5.2-2s2.6 2 5.2 2 2.6-2 5.2-2 2.6 2 5.2 2 2.6-2 5.2-2" fill="none" stroke="#9fe0d5" stroke-width="2.4" stroke-linecap="round"/>'
            '</svg>')

PHONE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z" fill="currentColor"/></svg>')


def masthead(active):
    def link(label, href):
        cur = ' aria-current="page"' if href == active else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    main = "".join(link(l, h) for l, h in NAV)
    more = "".join(link(l, h) for l, h in NAV_MORE)
    return f"""<header class="mast" data-mast>
<div class="wrap mast-row">
<a class="mark" href="/" aria-label="Destin Hurricane, home">{MARK_SVG}<span class="mark-text"><b>Destin Hurricane</b><small>Emerald Coast storm &amp; claim desk</small></span></a>
<nav class="navpanel" id="site-nav" data-nav aria-label="Main">
<ul class="navlist">{main}</ul>
<ul class="navlist navlist--more">{more}</ul>
<div class="navpanel-cta">
<a class="btn btn--coral btn--wide" href="/free-case-review/">Free claim review</a>
<a class="btn btn--line btn--wide" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
<p class="navpanel-firm"><img src="/assets/img/lawgical-logo.png" alt="{FIRM['name']}" width="112" height="40" loading="lazy">Sponsored by {FIRM['legal_name']}</p>
</div>
</nav>
<div class="mast-actions">
<a class="mast-call" href="tel:{FIRM['phone_href']}">{PHONE_SVG}<span>{FIRM['phone_display']}</span></a>
<a class="btn btn--coral btn--sm mast-cta" href="/free-case-review/">Free claim review</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-btn><span class="burger-box" aria-hidden="true"><i></i><i></i></span><span class="burger-label">Menu</span></button>
</div>
</div>
</header>
<div class="tideline" data-alertbar role="status" aria-live="polite">
<div class="wrap tideline-row">
<span class="tideline-dot" aria-hidden="true"></span>
<span class="tideline-text" data-alertbar-text>Checking National Weather Service alerts for Destin&hellip;</span>
<a class="tideline-link" href="/destin-hurricane-tracker/">Open the storm desk</a>
</div>
</div>
<div class="scrim" data-nav-scrim hidden></div>
<main id="content">
"""


def pagehead(page):
    if not page.get("h1"):
        return ""
    trail = crumbs_for(page)
    crumbs = " ".join(
        (f'<a href="{p}">{esc(n)}</a><span aria-hidden="true">/</span>' if i < len(trail) - 1 else f'<span aria-current="page">{esc(n)}</span>')
        for i, (n, p) in enumerate(trail))
    kicker = f'<p class="kicker">{page["kicker"]}</p>' if page.get("kicker") else ""
    lede = f'<p class="lede">{page["lede"]}</p>' if page.get("lede") else ""
    meta = []
    if page.get("reviewed"):
        meta.append(f"Last reviewed: {REVIEWED}")
    if page.get("published"):
        meta.append("Published " + date.fromisoformat(page["published"]).strftime("%B %-d, %Y"))
    meta_html = f'<p class="pagehead-meta">{" &middot; ".join(meta)}</p>' if meta else ""
    actions = ""
    if page.get("head_actions", True) and page.get("head_form"):
        actions = (f'<div class="btnrow"><a class="btn btn--coral" href="tel:{FIRM["phone_href"]}">Call {FIRM["phone_display"]}</a>'
                   f'<a class="btn btn--line" href="#faq">Questions &amp; answers</a></div>')
    text = f'<nav class="trail" aria-label="Breadcrumb">{crumbs}</nav>{kicker}<h1>{page["h1"]}</h1>{lede}{meta_html}{actions}'
    if page.get("head_form"):
        form_title = page.get("form_title", "Free claim review")
        return (f'<header class="pagehead pagehead--form"><div class="wrap pagehead-grid"><div class="pagehead-text">{text}</div>'
                f'<div class="formcard"><h2 class="formcard-title">{form_title}</h2>'
                f'<p class="formcard-sub">Free, confidential, and read by the {FIRM["name"]} team.</p>{lead_form("hf", compact=True)}</div>'
                f'</div></header>\n')
    return f'<header class="pagehead"><div class="wrap">{text}</div></header>\n'


def faq_block(page):
    if not page.get("faq"):
        return ""
    items = "".join(f"<details><summary>{q}</summary><div class=\"faq-a\"><p>{a}</p></div></details>" for q, a in page["faq"])
    title = page.get("faq_title", "Questions people ask")
    return (f'<section class="band band--foam" id="faq" aria-labelledby="faq-h"><div class="wrap wrap--narrow">'
            f'<p class="kicker">FAQ</p><h2 id="faq-h">{title}</h2><div class="faq">{items}</div></div></section>\n')


def claim_card():
    return f"""<aside class="band band--tight claimband" aria-label="Free claim review">
<div class="wrap">
<div class="claimcard">
<div class="claimcard-copy">
<p class="kicker">Free claim review &middot; no upfront fees</p>
<h2>Insurer denying, delaying or shorting your storm claim?</h2>
<p>Tell the attorneys at {FIRM['legal_name']} what happened to your Destin-area home, condo or business. The review of your policy and the insurer's estimate is free, and the firm is paid only if you are.</p>
</div>
<div class="claimcard-act">
<a class="btn btn--coral" href="/free-case-review/">Start my free review</a>
<a class="btn btn--line" href="tel:{FIRM['phone_href']}">Call {FIRM['phone_display']}</a>
</div>
</div>
</div>
</aside>
"""


def footer(show_card=True):
    offices = "".join(f"<p><span>{o['label']}</span>{o['street']}<br>{o['city']}, {o['region']} {o['zip']}</p>" for o in FIRM["offices"])
    return f"""</main>
{claim_card() if show_card else ""}<footer class="foot">
<svg class="foot-wave" viewBox="0 0 1440 48" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 30c120-22 240-22 360 0s240 22 360 0 240-22 360 0 240 22 360 0v18H0z" fill="currentColor"/></svg>
<div class="foot-body">
<div class="wrap foot-grid">
<div class="foot-brand">
<a class="mark mark--foot" href="/">{MARK_SVG}<span class="mark-text"><b>Destin Hurricane</b><small>Okaloosa &amp; Walton storm desk</small></span></a>
<p>Free hurricane tracking, evacuation and recovery information for Destin, Okaloosa Island, Fort Walton Beach, Niceville, Miramar Beach and Santa Rosa Beach, with storm-claim help from {FIRM['legal_name']}.</p>
</div>
<div class="foot-col"><h2>Claim help</h2><ul>
<li><a href="/destin-hurricane-claim-lawyer/">Hurricane claim lawyer</a></li>
<li><a href="/denied-hurricane-claim-destin/">Denied claims</a></li>
<li><a href="/underpaid-hurricane-claim-destin/">Underpaid claims</a></li>
<li><a href="/delayed-hurricane-claim-destin/">Delayed claims</a></li>
<li><a href="/hurricane-isaias-claims-destin/">Hurricane Isaias claims</a></li>
<li><a href="/free-case-review/">Free case review</a></li>
</ul></div>
<div class="foot-col"><h2>Storm desk</h2><ul>
<li><a href="/destin-hurricane-tracker/">Hurricane tracker</a></li>
<li><a href="/destin-weather/">Weather &amp; radar</a></li>
<li><a href="/okaloosa-walton-evacuation-zones/">Evacuation zones</a></li>
<li><a href="/walton-okaloosa-hurricane-shelters/">Shelters &amp; outages</a></li>
<li><a href="/destin-storm-surge/">Storm surge</a></li>
<li><a href="/hurricane-preparedness/">Preparedness</a></li>
<li><a href="/hurricane-tools/">Calculators</a></li>
<li><a href="/after-the-storm/">After the storm</a></li>
</ul></div>
<div class="foot-col"><h2>Coast &amp; history</h2><ul>
<li><a href="/communities/">Community guides</a></li>
<li><a href="/destin-hurricane-history/">Destin hurricane history</a></li>
<li><a href="/news/">Hurricane news</a></li>
<li><a href="/storm-alerts/">Storm alerts</a></li>
<li><a href="/our-firm/">{FIRM['name']}</a></li>
</ul></div>
</div>
<div class="wrap foot-firm">
<img src="/assets/img/lawgical-logo-white.png" alt="{FIRM['legal_name']}" width="150" height="56" loading="lazy">
<div class="foot-offices"><p><span>{FIRM['legal_name']}</span><a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></p>{offices}</div>
</div>
<div class="wrap">
<p class="foot-legal"><strong>Attorney advertising.</strong> This website is sponsored by {FIRM['legal_name']}, which is responsible for its content. Principal office: {FIRM['principal_city']}, Florida; local office: Destin, Florida. The information here is general information only, not legal advice; reading it, using its tools or contacting us does not create an attorney-client relationship. No attorney fee unless there is a recovery; ask how case costs are handled under the written fee agreement. Past results do not guarantee a similar outcome. The hiring of a lawyer is an important decision that should not be based solely on advertisements. See the full <a href="/disclaimer/">disclaimer</a>. In an emergency call 911 and follow Okaloosa County and Walton County officials.</p>
</div>
</div>
<div class="foot-base"><div class="wrap foot-base-row">
<span>&copy; {date.today().year} Destin Hurricane &middot; {FIRM['legal_name']}</span>
<span><a href="/about/">About</a><a href="/disclaimer/">Disclaimer</a><a href="/privacy-policy/">Privacy</a><a href="/sitemap/">Sitemap</a></span>
</div></div>
</footer>
<nav class="dock" aria-label="Contact {FIRM['name']}">
<a class="dock-call" href="tel:{FIRM['phone_href']}">{PHONE_SVG}<span>Call</span></a>
<a class="dock-review" href="/free-case-review/">Free claim review</a>
</nav>
<a class="totop" href="#content" data-totop aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 6l-7 7 1.4 1.4L12 8.8l5.6 5.6L19 13z" fill="currentColor"/></svg></a>
<script src="/assets/js/site.js?v={asset_version('assets/js/site.js')}" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ lead form

ISSUES = ["Claim denied (all or part)", "Paid, but not enough", "No decision / insurer not responding",
          "Not filed yet - need guidance", "Condo or HOA claim", "Something else"]
STORMS = ["Hurricane Isaias (Oct. 2026)", "Hurricane Sally (2020)", "Another storm / not sure"]


def lead_form(n, compact=False):
    """Free case review form (posts to /api/lead.php through site.js)."""
    opts = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    extra = "" if compact else (
        f'<div class="fld fld--full"><label for="f{n}-msg">What happened? <span class="opt">optional</span></label>'
        f'<textarea id="f{n}-msg" name="message" rows="4" placeholder="Isaias tore shingles off and the ceiling leaks; the insurer\'s estimate covers a patch only..."></textarea></div>'
        f'<div class="fld"><label for="f{n}-ins">Insurance company <span class="opt">optional</span></label><input id="f{n}-ins" name="insurer" type="text" autocomplete="off"></div>')
    return f"""<form class="leadform" data-lead-form novalidate>
<div class="fgrid">
<div class="fld"><label for="f{n}-name">Full name</label><input id="f{n}-name" name="name" type="text" autocomplete="name" required></div>
<div class="fld"><label for="f{n}-phone">Phone</label><input id="f{n}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
<div class="fld"><label for="f{n}-email">Email <span class="opt">optional</span></label><input id="f{n}-email" name="email" type="email" autocomplete="email"></div>
<div class="fld"><label for="f{n}-loc">Property city or ZIP</label><input id="f{n}-loc" name="location" type="text" autocomplete="postal-code" placeholder="32541 or Miramar Beach" required></div>
<div class="fld fld--full"><label for="f{n}-issue">Where does your claim stand?</label><select id="f{n}-issue" name="issue" required>{opts(ISSUES)}</select></div>
<div class="fld{' fld--full' if compact else ''}"><label for="f{n}-storm">Which storm?</label><select id="f{n}-storm" name="storm">{opts(STORMS)}</select></div>
{extra}
<input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
<label class="tick fld--full"><input type="checkbox" name="ack" value="1" required> <span>I understand that sending this form does not make me a client of {FIRM['legal_name']} and does not create an attorney-client relationship.</span></label>
<label class="tick fld--full"><input type="checkbox" name="sms_consent" value="1"> <span>Text me about my inquiry (optional). Msg &amp; data rates may apply; reply STOP to opt out.</span></label>
</div>
<button class="btn btn--coral btn--wide" type="submit">Send my free claim review request</button>
<p class="leadform-note">Reviewed by the attorneys and staff of {FIRM['legal_name']}. Rather talk? <a href="tel:{FIRM['phone_href']}">{FIRM['phone_display']}</a></p>
<div class="leadform-out" data-lead-out role="status" aria-live="polite"></div>
</form>"""


# ------------------------------------------------------------------ pages

def expand(body, page):
    reps = {
        "{{FIRM_NAME}}": FIRM["name"], "{{FIRM_LEGAL}}": FIRM["legal_name"], "{{FIRM_SITE}}": FIRM["site"],
        "{{FIRM_URL}}": FIRM["hurricane_url"], "{{FIRM_PHONE}}": FIRM["phone_display"], "{{FIRM_TEL}}": FIRM["phone_href"],
        "{{TODAY}}": TODAY, "{{REVIEWED}}": REVIEWED, "{{FAQ}}": faq_block(page),
    }
    for k, v in reps.items():
        body = body.replace(k, v)
    n = 0
    while "{{LEAD_FORM" in body:
        n += 1
        c, f = body.find("{{LEAD_FORM_COMPACT}}"), body.find("{{LEAD_FORM}}")
        if c != -1 and (f == -1 or c < f):
            body = body.replace("{{LEAD_FORM_COMPACT}}", lead_form(n, compact=True), 1)
        else:
            body = body.replace("{{LEAD_FORM}}", lead_form(n), 1)
    return body


HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load_pages():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HEADER_RE.match(raw)
        if not m:
            raise SystemExit(f"{name}: missing JSON header comment")
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{name}: bad JSON header: {e}")
        meta["source"] = name
        meta["raw"] = raw[m.end():]
        pages.append(meta)
    return pages


def out_file(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_html(pages):
    groups = {}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups.setdefault(p.get("group", "Site"), []).append(p)
    out = ""
    for g in ["Claims", "Storm desk", "Coast", "News", "Site"]:
        if g in groups:
            items = "".join(f'<li><a href="{p["path"]}">{esc(p["title"].split(" | ")[0])}</a></li>'
                            for p in sorted(groups[g], key=lambda x: x["path"]))
            out += f'<section class="mapgroup"><h2>{g}</h2><ul>{items}</ul></section>'
    return out


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    smap = sitemap_html(pages)
    for p in pages:
        body = expand(p["raw"], p).replace("{{SITEMAP}}", smap)
        doc = head(p) + masthead(p.get("nav", p["path"])) + pagehead(p) + body + footer(show_card=p.get("cta", True))
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(doc)
    urls = "".join(f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
                   for p in pages if p.get("sitemap") is not False)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        if STAGING:
            fh.write("User-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into public/ (staging={STAGING})")


if __name__ == "__main__":
    main()
