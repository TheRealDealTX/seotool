#!/usr/bin/env python3
"""Static site generator for floridainsuranceappraiser.com.

    python3 build.py      # writes the site into ./dist/
    python3 validate.py   # checks the output
"""
import json
import os
import shutil
from datetime import date

from siteconfig import BIZ, TODAY
from content.services import SERVICES
from content.locations import LOCATIONS
from content.tools import TOOLS
from content.blog import POSTS
from content.resources import ABOUT, PROCESS, FAQS, GLOSSARY, LEGAL

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
VER = "20261107"
NAME = BIZ["name"]
TEL = f'<a href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a>'
SITEMAP = []


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def url(p):
    return BIZ["origin"] + p


# ------------------------------------------------------------------ icons
_IC = {
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "hurricane": '<path d="M12 12m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0 -5 0"/><path d="M12 9.5C12 5 15 3 19 3c-2 1.5-3 3.5-3 6"/><path d="M12 14.5c0 4.5-3 6.5-7 6.5 2-1.5 3-3.5 3-6"/>',
    "roof": '<path d="M2 12l10-8 10 8"/><path d="M5 10v9h14v-9"/><path d="M9 19v-5h6v5"/><path d="M16 6V3h3v5.5"/>',
    "water": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    "sinkhole": '<path d="M3 8h18"/><path d="M6 8c1 5 3 8 6 8s5-3 6-8"/><path d="M9 20h6"/><path d="M8 4l2 2M16 4l-2 2"/>',
    "fire": '<path d="M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3.5 2-4.5 0 2 1 3 2 3 0-3 0-5 1-8.5z"/>',
    "building": '<rect x="4" y="3" width="10" height="18"/><path d="M14 9h6v12h-6"/><path d="M7 7h1M10 7h1M7 11h1M10 11h1M7 15h1M10 15h1M17 13h1M17 17h1"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    "scale": '<path d="M12 3v18M7 21h10"/><path d="M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0z"/><path d="M19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "file": '<path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 16h6"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16l4-5 3 3 5-7"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 14h2v2H8z"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12"/><path d="M4 6h.01M4 12h.01M4 18h.01"/>',
    "check": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M8 12l3 3 5-6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
    "camera": '<path d="M4 7h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
}


# ------------------------------------------------------------------ photos (Pexels license; see README credits)
PHOTO_ALT = {
    "florida-home-palm-trees": "Two-story stucco Florida home with palm trees and a covered patio",
    "hurricane-palm-trees-wind": "Palm trees bending in hurricane-force wind under a gray sky",
    "hurricane-damage-aerial": "Aerial view of homes with damaged roofs and fallen trees after a hurricane",
    "roofer-shingle-roof-repair": "Roofer working on an asphalt shingle roof",
    "water-damage-collapsed-ceiling": "Interior room with a collapsed ceiling and water-damaged debris",
    "cracked-wall-foundation": "Large cracks running through a plaster wall",
    "fire-damaged-house": "Two-story house gutted by fire with a burned-out roof",
    "florida-condo-building": "Mid-rise Florida condominium building lined with palm trees",
    "florida-commercial-property": "Commercial retail building with palm trees in Southwest Florida",
    "insurance-documents-review": "Two people reviewing a home insurance policy on a clipboard",
    "estimate-review-clipboard-laptop": "Reviewing an insurance estimate on a clipboard beside a laptop",
    "florida-coastal-homes": "White coastal homes with metal roofs and palm trees on the Florida Panhandle",
    "property-inspector-clipboard": "Property inspector in a hard hat and safety vest checking a home with a clipboard",
    "inspector-checklist": "Inspector holding a property inspection checklist on a clipboard",
    "claim-meeting-paperwork": "Property owner and professional going over claim paperwork at a table",
    "home-insurance-policy": "Home insurance policy documents and a pen on a desk",
    "post-storm-flooding-florida": "Storm debris and standing water along a palm-lined Florida waterfront",
    "flooded-house-street": "Floodwater surrounding a house after a heavy storm",
    "tile-roof-inspection": "Worker inspecting a tile roof",
    "miami-beach-skyline": "Miami Beach shoreline with high-rise condominiums at twilight",
    "tampa-skyline": "Downtown Tampa skyline across the Hillsborough River at sunset",
    "orlando-lake-eola-skyline": "Downtown Orlando skyline reflected in Lake Eola at sunrise",
    "jacksonville-skyline-bridge": "Jacksonville skyline and Main Street Bridge over the St. Johns River",
    "fort-lauderdale-beachfront": "Fort Lauderdale beachfront high-rises and boats on the inlet",
    "west-palm-beach-waterfront": "West Palm Beach waterfront and skyline under an evening sky",
    "fort-myers-neighborhood-aerial": "Aerial view of a residential neighborhood in Fort Myers",
    "naples-pier-sunset": "Naples Pier at sunset on the Gulf of Mexico",
    "sarasota-skyline": "Sarasota skyline across the bay on a clear day",
    "st-petersburg-pier": "The St. Pete Pier extending into Tampa Bay",
    "north-florida-live-oaks": "Live oaks draped in Spanish moss arching over a North Florida street",
    "pensacola-beach": "Aerial view of white sand and surf on Pensacola Beach",
}
SVC_PHOTO = {
    "homeowners-claim-appraisal": "florida-coastal-homes", "hurricane-claim-appraisal": "hurricane-damage-aerial",
    "roof-claim-appraisal": "roofer-shingle-roof-repair", "water-damage-claim-appraisal": "water-damage-collapsed-ceiling",
    "sinkhole-claim-appraisal": "cracked-wall-foundation", "fire-smoke-claim-appraisal": "fire-damaged-house",
    "condo-hoa-claim-appraisal": "florida-condo-building", "commercial-claim-appraisal": "florida-commercial-property",
    "umpire-services": "insurance-documents-review", "xactimate-estimate-review": "estimate-review-clipboard-laptop",
}
LOC_PHOTO = {
    "miami-fl": "miami-beach-skyline", "tampa-fl": "tampa-skyline", "orlando-fl": "orlando-lake-eola-skyline",
    "jacksonville-fl": "jacksonville-skyline-bridge", "fort-lauderdale-fl": "fort-lauderdale-beachfront",
    "west-palm-beach-fl": "west-palm-beach-waterfront", "fort-myers-fl": "fort-myers-neighborhood-aerial",
    "naples-fl": "naples-pier-sunset", "sarasota-fl": "sarasota-skyline", "st-petersburg-fl": "st-petersburg-pier",
    "tallahassee-fl": "north-florida-live-oaks", "pensacola-fl": "pensacola-beach",
}
POST_PHOTO = {
    "how-the-appraisal-clause-works-in-florida": "home-insurance-policy",
    "florida-hurricane-deductible-explained": "post-storm-flooding-florida",
    "appraiser-vs-public-adjuster-vs-attorney-florida": "claim-meeting-paperwork",
    "what-to-do-when-a-florida-claim-is-underpaid": "flooded-house-street",
    "florida-roof-claims-after-the-2022-reforms": "tile-roof-inspection",
}
_DIMS = {}


def _dims(name):
    if name not in _DIMS:
        from PIL import Image
        with Image.open(os.path.join(ROOT, "assets/img/photos", name + ".webp")) as im:
            _DIMS[name] = im.size
    return _DIMS[name]


def photo(name, cls="", sizes="(max-width: 760px) 100vw, 50vw", eager=False, alt=None):
    w, h = _dims(name)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="/assets/img/photos/{name}.webp" '
            f'srcset="/assets/img/photos/{name}-sm.webp 720w, /assets/img/photos/{name}.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt or PHOTO_ALT[name])}" {load} decoding="async">')


def icon(name):
    return (f'<svg viewBox="0 0 24 24" aria-hidden="true">{_IC.get(name, _IC["file"])}</svg>')


def ico(name):
    return f'<div class="ico">{icon(name)}</div>'


def _mark(tile, roof, line):
    return (f'<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="{tile}"/>'
            f'<path d="M11 21L20 13l9 8" fill="none" stroke="{roof}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M11 27.5h18" stroke="{line}" stroke-width="2.6" stroke-linecap="round"/></svg>')


LOGO = _mark("#0f4c4a", "#fff", "#c9974a")
LOGO_DARK = _mark("#fff", "#0f4c4a", "#b7832f")


def brand(dark=False):
    return (f'<a class="brand" href="/" aria-label="{NAME} home">{LOGO_DARK if dark else LOGO}'
            f'<span class="wm"><small>Florida</small><b>Insurance Appraiser</b></span></a>')


# ------------------------------------------------------------------ schema
ORG_ID = url("/#organization")


def org_schema():
    return {
        "@type": ["ProfessionalService", "LocalBusiness"], "@id": ORG_ID, "name": NAME, "url": url("/"),
        "telephone": BIZ["phone_href"], "email": BIZ["email"], "image": url("/assets/img/og-image.png"),
        "logo": url("/web-app-manifest-512x512.png"), "priceRange": "$$",
        "description": "Independent property insurance appraisal, umpire services and estimate review for homeowners, condo associations and commercial property owners across Florida.",
        "address": {"@type": "PostalAddress", "addressRegion": "FL", "addressCountry": "US"},
        "areaServed": [{"@type": "State", "name": "Florida"}] + [{"@type": "City", "name": f'{l["city"]}, FL'} for l in LOCATIONS],
        "contactPoint": {"@type": "ContactPoint", "telephone": BIZ["phone_href"], "email": BIZ["email"], "contactType": "customer service", "areaServed": "US-FL", "availableLanguage": "English"},
        "knowsAbout": ["Property insurance appraisal", "Hurricane claims", "Xactimate", "Symbility", "Umpire services", "Condominium insurance claims"],
    }


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


# ------------------------------------------------------------------ chrome
def head(p):
    canonical = url(p["path"])
    graph = [org_schema(), {"@type": "WebSite", "@id": url("/#website"), "url": url("/"), "name": NAME, "publisher": {"@id": ORG_ID}}]
    graph += p.get("schema", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    robots = p.get("robots", "index, follow, max-image-preview:large")
    og_image = url(f"/assets/img/photos/{p['photo']}.webp") if p.get("photo") else url("/assets/img/og-image.png")
    extra = ""
    if p.get("published"):
        extra = f'<meta property="article:published_time" content="{p["published"]}">\n'
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-T37B9MBK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<script>if(location.protocol==='http:'&&location.hostname==='floridainsuranceappraiser.com')location.replace('https:'+location.href.slice(5));</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p['title'])}</title>
<meta name="description" content="{esc(p['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0f4c4a">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{p.get('og_type', 'website')}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(p['title'])}">
<meta property="og:description" content="{esc(p['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
{extra}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
"""


def _drop(label, items, all_link=None, cols=False):
    lis = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in items)
    if all_link:
        lis += f'<li><a class="all" href="{all_link[1]}">{all_link[0]} →</a></li>'
    return (f'<li><button type="button" aria-expanded="false">{label}</button>'
            f'<ul class="drop{" cols" if cols else ""}">{lis}</ul></li>')


def header():
    svc = [(s["name"], f'/appraisal-services/{s["slug"]}/') for s in SERVICES]
    loc = [(f'{l["city"]}, FL', f'/florida-locations/{l["slug"]}/') for l in LOCATIONS]
    tls = [(t["name"], f'/claim-tools/{t["slug"]}/') for t in TOOLS]
    res = [("Appraisal Process", "/appraisal-process/"), ("FAQ", "/faq/"), ("Claim Glossary", "/claim-glossary/"), ("Guides & Articles", "/blog/")]
    return f"""<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-T37B9MBK" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>Independent property claim appraisal · all 67 Florida counties</span><span><span><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></span><span class="hide-m"><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></span></span></div></div>
<header class="hdr"><div class="wrap">
{brand()}
<button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span></button>
<nav class="nav" id="nav" aria-label="Main">
<ul>
{_drop('Services', svc, ('All services', '/appraisal-services/'), cols=True)}
{_drop('Locations', loc, ('All Florida locations', '/florida-locations/'), cols=True)}
{_drop('Free Tools', tls, ('All tools', '/claim-tools/'))}
{_drop('Resources', res)}
<li><a href="/about/">About</a></li>
<li><a href="/contact/">Contact</a></li>
</ul>
<a class="btn btn-primary" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
</nav>
</div></header>
"""


def footer():
    svc = "".join(f'<li><a href="/appraisal-services/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="/florida-locations/{l["slug"]}/">{l["city"]}</a></li>' for l in LOCATIONS)
    tls = "".join(f'<li><a href="/claim-tools/{t["slug"]}/">{t["name"]}</a></li>' for t in TOOLS)
    return f"""<footer class="ftr">
<div class="wrap">
<div class="ftr-grid">
<div>{brand(True)}<p>{NAME} provides independent appraisal, umpire services and line-item estimate review for Florida homeowners, condominium associations and commercial property owners in disputed insurance claims.</p>
<ul><li><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></li><li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li><li>Serving all 67 Florida counties</li></ul></div>
<div><h4>Services</h4><ul>{svc}<li><a href="/appraisal-services/">All services →</a></li></ul></div>
<div><h4>Locations</h4><ul>{loc}</ul></div>
<div><h4>Free tools</h4><ul>{tls}</ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About us</a></li><li><a href="/appraisal-process/">Appraisal process</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/claim-glossary/">Claim glossary</a></li><li><a href="/blog/">Guides</a></li><li><a href="/contact/">Contact</a></li></ul>
<h4 style="margin-top:26px">Legal</h4><ul><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms-of-use/">Terms of use</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
</div>
<div class="ftr-bottom"><p>© {date.today().year} {NAME}. General information only — not legal advice. Appraisal determines the amount of a covered loss; it does not decide coverage. We are not a law firm.</p><p><a href="/disclaimer/">Disclaimer</a></p></div>
</div></footer>
<div class="callbar"><a href="tel:{BIZ['phone_href']}">Call now</a><a href="/contact/">Free claim review</a></div>
<script src="/assets/js/site.js?v={VER}" defer></script>
"""


def page_html(p, body):
    js = f'<script src="/assets/js/tools.js?v={VER}" defer></script>\n' if p.get("tools_js") else ""
    return head(p) + header() + f'<main id="main">\n{body}\n</main>\n' + footer() + js + "</body>\n</html>\n"


def write(p, body, priority="0.7"):
    html = page_html(p, body)
    rel = p.get("file") or (p["path"].strip("/") + "/index.html")
    dest = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    if not p.get("robots", "").startswith("noindex"):
        SITEMAP.append((p["path"], p.get("modified", TODAY), priority))


# ------------------------------------------------------------------ components
def crumbs(trail):
    parts = []
    for i, (n, pth) in enumerate(trail):
        parts.append(f'<a href="{pth}">{esc(n)}</a>' if i < len(trail) - 1 else f'<span aria-current="page">{esc(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def page_hero(trail, kicker, h1, lead, extra="", img=None):
    text = f"""{crumbs(trail)}
<span class="eyebrow">{esc(kicker)}</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>{extra}"""
    if img:
        fig = photo(img, sizes="(max-width: 1000px) 100vw, 42vw", eager=True)
        return f'<section class="page-hero has-photo"><div class="wrap"><div>{text}</div><figure class="hero-photo">{fig}</figure></div></section>'
    return f'<section class="page-hero"><div class="wrap">{text}</div></section>'


def faq_block(faqs, heading="Frequently asked questions"):
    items = "".join(f'<details class="faq"><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs)
    return f'<h2>{heading}</h2>{items}'


def prose(sections):
    return "".join(f"<h2>{h}</h2>{b}" for h, b in sections)


def call_box(title="Talk to an appraiser"):
    return f"""<div class="box dark"><h3>{title}</h3><p>Send us the insurer’s estimate and your numbers. We’ll tell you plainly whether appraisal makes sense.</p>
<a class="btn btn-primary" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a>
<p style="margin:12px 0 0;font-size:.9rem"><a href="/contact/">Or send claim details online →</a></p></div>"""


def link_box(title, links):
    lis = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in links)
    return f'<div class="box"><h3>{title}</h3><ul>{lis}</ul></div>'


def cta_band(h="Disputing an insurance estimate in Florida?", sub="Get a straight answer on whether appraisal is worth it — usually within one business day."):
    return f"""<section class="cta-band"><div class="wrap"><div><h2>{h}</h2><p>{sub}</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-ink" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a><a class="btn btn-ghost" href="/contact/">Send claim details</a></div></div></section>"""


LOSS_TYPES = ["Hurricane / wind", "Roof damage", "Water / plumbing leak", "Flood-related", "Fire / smoke", "Sinkhole / ground movement", "Hail", "Mold", "Theft / vandalism", "Other"]
ROLES = ["Homeowner", "Condo / HOA board or manager", "Commercial property owner", "Contractor", "Attorney", "Public adjuster", "Other"]


def lead_form(fid="contact-form"):
    lt = "".join(f"<option>{t}</option>" for t in LOSS_TYPES)
    rl = "".join(f"<option>{t}</option>" for t in ROLES)
    return f"""<form class="lead-form" id="{fid}" action="/api/contact.php" method="post" data-lead-form data-phone="{BIZ['phone_display']}">
<h3>Send your claim details</h3>
<div class="row">
<div class="field"><label for="{fid}-name">Full name</label><input id="{fid}-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="{fid}-email">Email</label><input id="{fid}-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="{fid}-phone">Phone</label><input id="{fid}-phone" name="phone" type="tel" required autocomplete="tel"></div>
<div class="field"><label for="{fid}-city">City or county</label><input id="{fid}-city" name="location" placeholder="e.g. Cape Coral, Lee County"></div>
<div class="field"><label for="{fid}-role">I am a…</label><select id="{fid}-role" name="role">{rl}</select></div>
<div class="field"><label for="{fid}-loss">Type of loss</label><select id="{fid}-loss" name="loss_type">{lt}</select></div>
</div>
<div class="field"><label for="{fid}-msg">What happened, and where does the claim stand?</label><textarea id="{fid}-msg" name="message" rows="4" placeholder="Date of loss, insurer, amount offered vs. your estimate…"></textarea></div>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<label class="consent"><input type="checkbox" name="consent" value="yes" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form does not create an appraisal engagement.</span></label>
<button class="btn btn-primary" type="submit">Send my claim details</button>
<p class="form-msg" role="status" aria-live="polite"></p>
</form>"""


def service_card(s):
    img = photo(SVC_PHOTO[s["slug"]], sizes="(max-width: 640px) 100vw, 380px")
    return (f'<a class="card card-ph" href="/appraisal-services/{s["slug"]}/"><div class="ph">{img}</div>'
            f'<div class="cb">{ico(s["icon"])}<h3>{s["name"]}</h3><p>{esc(s["short"])}</p><span class="go">Learn more →</span></div></a>')


def tool_card(t):
    return f'<a class="card" href="/claim-tools/{t["slug"]}/">{ico(t["icon"])}<h3>{t["name"]}</h3><p>{esc(t["short"])}</p><span class="go">Open tool →</span></a>'


def post_card(p):
    img = photo(POST_PHOTO[p["slug"]], sizes="(max-width: 640px) 100vw, 380px")
    return (f'<a class="card card-ph" href="/blog/{p["slug"]}/"><div class="ph">{img}</div>'
            f'<div class="cb"><span class="num">{esc(p["kicker"])}</span><h3>{esc(p["h1"])}</h3><p>{esc(p["excerpt"])}</p><span class="go">Read · {p["read_min"]} min →</span></div></a>')


def loc_card(l):
    img = photo(LOC_PHOTO[l["slug"]], sizes="(max-width: 640px) 100vw, 290px")
    return (f'<a class="card card-ph" href="/florida-locations/{l["slug"]}/"><div class="ph">{img}</div>'
            f'<div class="cb"><h3>{l["city"]}, FL</h3><p>{esc(l["county"])} · {esc(l["region"])}</p><span class="go">View area →</span></div></a>')


# ------------------------------------------------------------------ homepage
HOME_FAQS = [
    ("What does a Florida insurance appraiser actually do?",
     "When you and your insurance company agree a loss is covered but disagree on how much it costs to repair, the appraisal provision in most Florida policies lets each side appoint an appraiser. As your Florida Insurance Appraiser, we inspect the property, build or review a line-item estimate, and negotiate the amount of loss with the insurer’s appraiser. If we can’t agree, a neutral umpire decides the disputed items."),
    ("Is appraisal binding in Florida?",
     "An appraisal award signed by any two of the three participants (the two appraisers and the umpire) generally sets the amount of loss under the policy. It does not decide coverage questions, and your policy’s exact wording controls."),
    ("How is appraisal different from hiring a public adjuster or attorney?",
     "A public adjuster manages and negotiates the whole claim, and an attorney handles legal disputes such as denials and bad-faith issues. Appraisal is narrower and usually faster: it focuses only on the dollar amount of a covered loss. See our <a href=\"/blog/appraiser-vs-public-adjuster-vs-attorney-florida/\">side-by-side comparison</a>."),
    ("Can I invoke appraisal after the insurer has already paid something?",
     "Often, yes. Many owners invoke appraisal after an initial payment that doesn’t cover the actual repair cost. The award is reduced by prior payments and your deductible. Check your policy’s timing requirements first."),
    ("Do you handle condominium and commercial claims?",
     "Yes. Florida Insurance Appraiser works with condo associations on master-policy claims and with owners of retail, office, warehouse, hospitality and multifamily properties, where scope and code-upgrade questions tend to be larger."),
    ("What does it cost to talk to you?",
     "The first conversation and a look at your insurer’s estimate cost nothing. If appraisal makes sense, we explain our fee in writing before anything is signed."),
]


def build_home():
    storms = [("1992", "Andrew rewrote South Florida’s building code"), ("2004", "Charley, Frances, Ivan & Jeanne in six weeks"),
              ("2017", "Irma hit nearly the whole peninsula"), ("2018", "Michael struck the Panhandle as a Category 5"),
              ("2022", "Ian flooded and flattened Southwest Florida"), ("2024", "Helene and Milton hit the Gulf Coast two weeks apart")]
    tl = "".join(f"<div><b>{y}</b><span>{t}</span></div>" for y, t in storms)
    svc_cards = "".join(service_card(s) for s in SERVICES[:6])
    tool_cards = "".join(tool_card(t) for t in TOOLS[:6])
    chips = "".join(f'<li><a href="/florida-locations/{l["slug"]}/">{l["city"]}</a></li>' for l in LOCATIONS)
    posts = sorted(POSTS, key=lambda p: p["published"], reverse=True)[:3]
    faq_html = "".join(f'<details class="faq"><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in HOME_FAQS)

    body = f"""
<section class="hero">
<div class="wrap">
<div>
<span class="eyebrow">Independent appraisal · all 67 counties</span>
<h1>Florida Insurance Appraiser for <em>underpaid</em> property claims</h1>
<p class="lead">Your insurer says $18,000. Your roofer says $41,000. Florida Insurance Appraiser closes that gap with measurements, photos and a line-by-line estimate the other side has to answer — for homeowners, condo associations and commercial owners from Pensacola to Key West.</p>
<div class="hero-ctas"><a class="btn btn-primary" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a><a class="btn btn-ghost" href="/contact/">Get a free claim review</a></div>
<ul class="trust"><li>Xactimate &amp; Symbility estimates</li><li>Residential &amp; commercial</li><li>Umpire services</li></ul>
</div>
<div class="hero-media">
<figure class="hero-img">{photo('florida-home-palm-trees', sizes='(max-width: 1000px) 100vw, 46vw', eager=True)}<figcaption>Stucco, tile and shingle: we price Florida homes the way they’re actually built.</figcaption></figure>
<form class="card-calc" id="quickgap" onsubmit="return false" aria-labelledby="qg-h">
<h2 id="qg-h">How big is your claim gap?</h2>
<p class="sub">A 10-second check before you call.</p>
<div class="field"><label for="qg-ins">Insurer’s estimate</label><div class="money"><input id="qg-ins" name="ins" inputmode="decimal" value="18000"></div></div>
<div class="field"><label for="qg-con">Contractor’s estimate</label><div class="money"><input id="qg-con" name="con" inputmode="decimal" value="41000"></div></div>
<div class="result"><small>Amount in dispute</small><div class="big">$23,000</div><div class="meter"><i></i></div><small class="verdict-text"></small></div>
<p style="margin:14px 0 0;font-size:.9rem"><a href="/claim-tools/appraisal-worth-it-calculator/">Run the full worth-it calculator →</a></p>
</form>
</div>
</div>
</section>

<section class="sec tight"><div class="wrap">
<div class="stats"><div><b>67</b><span>Florida counties served</span></div><div><b>{len(SERVICES)}</b><span>appraisal &amp; estimating services</span></div><div><b>{len(TOOLS)}</b><span>free claim tools</span></div><div><b>2</b><span>estimating platforms: Xactimate &amp; Symbility</span></div></div>
</div></section>

<section class="sec" id="why"><div class="wrap split">
<div>
<span class="num">The gap</span>
<h2>Why the insurer’s number and your contractor’s number never match</h2>
<p>Most underpaid Florida claims aren’t the result of one big disagreement. They’re dozens of small ones: a roof measured without its waste factor, a tile line item swapped for shingles, drywall priced for one wall instead of the whole room, matching ignored, code upgrades left off and contractor overhead and profit quietly removed.</p>
<p>A Florida Insurance Appraiser finds those differences one line at a time and puts a documented price on each of them. That is what an appraisal panel weighs — not who argues loudest, but whose estimate holds up item by item.</p>
<p><a class="btn btn-ink" href="/about/">How we work</a></p>
<figure class="inline-photo">{photo('property-inspector-clipboard', sizes='(max-width: 1000px) 100vw, 560px')}</figure>
</div>
<div class="postcard">
<h3>Illustrative example: a hip-roof hurricane claim</h3>
<div class="table-wrap"><table class="cmp"><thead><tr><th>Line item</th><th>Carrier</th><th>Re-estimate</th></tr></thead><tbody>
<tr><td>Roof area (squares)</td><td>28.0</td><td>33.6</td></tr>
<tr><td>Waste factor</td><td>0%</td><td>15%</td></tr>
<tr><td>Drip edge &amp; starter</td><td>Omitted</td><td>Included</td></tr>
<tr><td>Code-required underlayment</td><td>Omitted</td><td>Included</td></tr>
<tr><td>Interior ceiling repairs</td><td>1 room</td><td>3 rooms</td></tr>
</tbody></table></div>
<p class="note" style="margin-top:14px">Hypothetical figures to show how small line items add up. Every claim is different.</p>
</div>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head"><span class="num">Services</span><h2>What Florida Insurance Appraiser handles</h2><p>From a single water-damaged kitchen to a 200-unit condominium tower, every assignment starts the same way: an honest read of the policy, the insurer’s estimate and the gap between them.</p></div>
<div class="grid g3">{svc_cards}</div>
<p style="margin-top:28px"><a class="btn btn-ghost" href="/appraisal-services/">See all {len(SERVICES)} services</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><span class="num">The process</span><h2>How appraisal works with a Florida Insurance Appraiser in your corner</h2></div>
<ol class="steps">
<li><h3>Policy &amp; estimate review</h3><p>We read the appraisal provision, deductibles and endorsements, then compare the insurer’s estimate with yours.</p></li>
<li><h3>Written demand</h3><p>If the gap justifies it, appraisal is invoked in writing and each side names a disinterested appraiser.</p></li>
<li><h3>Inspection &amp; negotiation</h3><p>We inspect, measure and document, then work through the estimates with the insurer’s appraiser line by line.</p></li>
<li><h3>Umpire &amp; award</h3><p>Items still in dispute go to a neutral umpire. An award signed by two of the three sets the amount of loss.</p></li>
</ol>
<p style="margin-top:30px"><a href="/appraisal-process/">Read the full Florida appraisal process guide →</a></p>
</div></section>

<section class="sec ink photo-bg">{photo('hurricane-palm-trees-wind', cls='bg', sizes='100vw', alt='')}<div class="wrap">
<div class="split top">
<div><span class="num">Storm country</span>
<h2>Built for the claims Florida actually gets</h2>
<p>Hurricane season runs June 1 through November 30, but Florida losses don’t keep a calendar: summer thunderstorms, plumbing failures, kitchen fires and ground movement fill the other months. After a named storm, insurers face thousands of claims at once, and desk-adjusted estimates written from photos become the norm. That is when a Florida Insurance Appraiser earns their fee.</p>
<p>We know the difference between wind and surge, how percentage hurricane deductibles change the math, and why a 2001 tile roof in Broward is priced nothing like a 2019 shingle roof in Ocala. <a href="/appraisal-services/hurricane-claim-appraisal/">Hurricane claim appraisal →</a></p></div>
<div class="timeline">{tl}</div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head center"><span class="eyebrow">Free tools</span><h2>Free claim tools from Florida Insurance Appraiser</h2><p>Run the numbers yourself before you call anyone. No sign-up, nothing stored on our servers.</p></div>
<div class="grid g3">{tool_cards}</div>
<p style="margin-top:28px;text-align:center"><a class="btn btn-ghost" href="/claim-tools/">See all {len(TOOLS)} tools</a></p>
</div></section>

<section class="sec sand"><div class="wrap">
<div class="sec-head"><span class="num">Your options</span><h2>Appraisal vs. the other ways to resolve a Florida claim dispute</h2><p>Appraisal isn’t the right tool for every problem. Here’s how it compares, in plain terms.</p></div>
<div class="table-wrap"><table class="cmp"><thead><tr><th>Option</th><th>Best for</th><th>Decides</th><th>Typical pace</th></tr></thead><tbody>
<tr><td>Appraisal</td><td>Covered losses where the dispute is the dollar amount</td><td>Amount of loss only</td><td>Weeks to a few months</td></tr>
<tr><td>DFS mediation</td><td>Residential disputes where both sides may settle with a neutral’s help</td><td>Nothing unless both sides agree</td><td>Often a single session</td></tr>
<tr><td>Public adjuster</td><td>Owners who want the whole claim prepared and negotiated for them</td><td>Negotiated settlement</td><td>Varies with the claim</td></tr>
<tr><td>Litigation</td><td>Coverage denials, bad faith and legal questions</td><td>Coverage and damages</td><td>Often a year or more</td></tr>
</tbody></table></div>
<p class="note">General comparison, not legal advice. A Florida Insurance Appraiser decides amount-of-loss questions only; coverage questions belong with an attorney.</p>
</div></section>

<section class="sec"><div class="wrap split top">
<div><span class="num">Where we work</span>
<h2>A Florida Insurance Appraiser for every coast</h2>
<p>We work claims statewide — the high-rise condos of Miami-Dade and Broward, the older block homes of Tampa Bay, the barrier islands of Lee and Collier, the oak-canopy neighborhoods of Tallahassee and the Panhandle beaches still rebuilding from recent storms.</p>
<ul class="chips">{chips}<li><a href="/florida-locations/">All of Florida →</a></li></ul>
<div class="grid g2" style="margin-top:28px">{''.join(loc_card(l) for l in LOCATIONS if l['slug'] in ('miami-fl', 'fort-myers-fl'))}</div></div>
<div class="grid g2">
<div class="card">{ico('home')}<h3>Homeowners</h3><p>Single-family homes, townhomes and condo unit owners with HO-3, HO-6 or dwelling policies.</p></div>
<div class="card">{ico('building')}<h3>Condo associations</h3><p>Master-policy claims, shared elements and building-wide water or wind losses.</p></div>
<div class="card">{ico('briefcase')}<h3>Commercial owners</h3><p>Retail, office, warehouse, hospitality, churches and multifamily properties.</p></div>
<div class="card">{ico('users')}<h3>Contractors &amp; counsel</h3><p>Estimate support and appraisal for roofers, restoration firms and attorneys’ clients.</p></div>
</div>
</div></section>

<section class="sec sand"><div class="wrap split top">
<div><span class="num">Questions</span><h2>Questions people ask a Florida Insurance Appraiser</h2>
<p>Short answers to what we hear most. More in the <a href="/faq/">full FAQ</a> and the <a href="/claim-glossary/">claim glossary</a>.</p></div>
<div>{faq_html}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><span class="num">Guides</span><h2>Guides for Florida policyholders</h2></div>
<div class="grid g3">{''.join(post_card(p) for p in posts)}</div>
<p style="margin-top:28px"><a class="btn btn-ghost" href="/blog/">All guides</a></p>
</div></section>

<section class="sec sand" id="contact"><div class="wrap split top">
<div><span class="num">Free review</span>
<h2>Talk to a Florida Insurance Appraiser about your claim</h2>
<p>Tell us what happened and where the claim stands. We’ll look at the numbers and tell you honestly whether appraisal, a supplement, mediation or something else makes the most sense — even if the answer is that you don’t need us.</p>
<ul class="contact-list">
<li>{ico('phone')}<a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></li>
<li>{ico('mail')}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
<li>{ico('pin')}<span>Statewide — all 67 Florida counties</span></li>
</ul>
<p class="note">Florida Insurance Appraiser provides appraisal and estimating services. We are not a law firm and do not give legal advice.</p></div>
{lead_form('home-form')}
</div></section>
"""
    p = {"path": "/", "file": "home.html", "photo": "florida-home-palm-trees",
         "title": "Florida Insurance Appraiser | Property Claim Appraisal",
         "description": "Florida Insurance Appraiser resolves underpaid hurricane, roof, water and fire claims with line-item estimates, appraisal and umpire services statewide.",
         "schema": [faq_schema(HOME_FAQS)]}
    write(p, body, "1.0")


# ------------------------------------------------------------------ interior templates
def standard_page(path, trail, kicker, h1, lead, main_html, aside_html, faqs=None, schema=None, title=None, description=None, priority="0.6", extra_hero="", img=None, **kw):
    faq_html = f'<div style="margin-top:40px">{faq_block(faqs)}</div>' if faqs else ""
    body = page_hero(trail, kicker, h1, lead, extra_hero, img) + f"""
<section class="sec"><div class="wrap layout">
<article class="prose">{main_html}{faq_html}</article>
<aside class="aside">{aside_html}</aside>
</div></section>
""" + cta_band()
    sch = [crumbs_schema(trail)] + (schema or [])
    if faqs:
        sch.append(faq_schema(faqs))
    p = {"path": path, "title": title, "description": description, "schema": sch, "photo": img}
    p.update(kw)
    write(p, body, priority)


def build_services():
    trail0 = [("Home", "/"), ("Services", "/appraisal-services/")]
    cards = "".join(service_card(s) for s in SERVICES)
    body = page_hero(trail0, "Appraisal & estimating", "Property claim appraisal services across Florida",
                     f"Ten ways {NAME} helps resolve disputed claims — from a single roof to an entire condominium complex.", img="roofer-shingle-roof-repair") + f"""
<section class="sec"><div class="wrap"><div class="grid g3">{cards}</div>
<div class="postcard" style="margin-top:56px"><div class="split top"><div><h2>Not sure which service fits?</h2><p>Most clients don’t know whether they need an appraiser, an umpire or just a second set of eyes on an estimate. Call and describe the claim; we’ll point you in the right direction even if it isn’t us.</p></div>
<div><ul class="ticks"><li>Policy and estimate review before anything is signed</li><li>Clear written fee terms</li><li>Residential, condominium and commercial losses</li><li>Xactimate and Symbility line-item estimates</li></ul><a class="btn btn-primary" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_short']}</a></div></div></div>
</div></section>""" + cta_band()
    write({"path": "/appraisal-services/", "photo": "roofer-shingle-roof-repair", "title": "Insurance Appraisal Services in Florida | All Services",
           "description": "Hurricane, roof, water, sinkhole, fire, condo and commercial claim appraisal, plus umpire services and Xactimate estimate review across Florida.",
           "schema": [crumbs_schema(trail0), {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f'/appraisal-services/{s["slug"]}/'), "name": s["name"]} for i, s in enumerate(SERVICES)]}]},
          body, "0.9")
    svc_by = {s["slug"]: s for s in SERVICES}
    tool_by = {t["slug"]: t for t in TOOLS}
    for s in SERVICES:
        path = f'/appraisal-services/{s["slug"]}/'
        trail = trail0 + [(s["name"], path)]
        check = "".join(f"<li>{esc(c)}</li>" for c in s.get("checklist", []))
        main = prose(s["sections"]) + (f'<div class="postcard" style="margin-top:32px"><h3>What to gather before you call</h3><ul class="ticks">{check}</ul></div>' if check else "")
        aside = call_box() + link_box("Related services", [(svc_by[x]["name"], f"/appraisal-services/{x}/") for x in s.get("related_services", []) if x in svc_by]) \
            + link_box("Free tools", [(tool_by[x]["name"], f"/claim-tools/{x}/") for x in s.get("related_tools", []) if x in tool_by])
        schema = [{"@type": "Service", "name": s["name"], "serviceType": s["name"], "provider": {"@id": ORG_ID},
                   "areaServed": {"@type": "State", "name": "Florida"}, "url": url(path), "description": s["description"]}]
        standard_page(path, trail, s["kicker"], esc(s["h1"]), esc(s["lead"]), main, aside, s.get("faqs"), schema,
                      s["title"], s["description"], "0.8", img=SVC_PHOTO[s["slug"]])


def build_locations():
    trail0 = [("Home", "/"), ("Locations", "/florida-locations/")]
    regions = {}
    for l in LOCATIONS:
        regions.setdefault(l["region"], []).append(l)
    cards = "".join(loc_card(l) for l in LOCATIONS)
    body = page_hero(trail0, "Statewide coverage", "Insurance appraisal across Florida",
                     f"{NAME} works property claims in all 67 Florida counties. These are the markets we’re asked about most — if your city isn’t listed, we still cover it.", img="fort-myers-neighborhood-aerial") + f"""
<section class="sec"><div class="wrap"><div class="grid g4">{cards}</div>
<div class="sec-head" style="margin-top:64px"><h2>Every region has its own claim pattern</h2><p>South Florida’s high-velocity hurricane zone, Tampa Bay’s sinkhole belt, Southwest Florida’s surge-versus-wind fights and the Panhandle’s tree and wind losses each shape how estimates get written — and where they come up short. Our local pages explain what we see in each market.</p></div>
</div></section>""" + cta_band()
    write({"path": "/florida-locations/", "photo": "fort-myers-neighborhood-aerial", "title": "Florida Insurance Appraiser Locations | Statewide Service",
           "description": f"{NAME} serves all 67 Florida counties, including Miami, Tampa, Orlando, Jacksonville, Fort Myers, Naples, Sarasota and Pensacola.",
           "schema": [crumbs_schema(trail0)]}, body, "0.9")
    by = {l["slug"]: l for l in LOCATIONS}
    svc_links = [(s["name"], f'/appraisal-services/{s["slug"]}/') for s in SERVICES[:6]]
    for l in LOCATIONS:
        path = f'/florida-locations/{l["slug"]}/'
        trail = trail0 + [(f'{l["city"]}, FL', path)]
        storms = "".join(f"<li><b>{y}</b><div><strong>{esc(n)}</strong><br>{esc(t)}</div></li>" for y, n, t in l.get("storms", []))
        issues = "".join(f"<li>{esc(i)}</li>" for i in l.get("claim_issues", []))
        hoods = "".join(f"<li><span>{esc(h)}</span></li>" for h in l.get("neighborhoods", []))
        main = prose(l["sections"])
        if storms:
            main += f'<h2>Storms that shaped {esc(l["city"])} claims</h2><ul class="storm-list">{storms}</ul>'
        if issues:
            main += f'<h2>Claim issues we see in {esc(l["county"])}</h2><ul class="ticks">{issues}</ul>'
        if hoods:
            main += f'<h2>Areas we cover around {esc(l["city"])}</h2><ul class="chips">{hoods}</ul>'
        aside = call_box(f'Claim in {l["city"]}?') + link_box("Services", svc_links) + \
            link_box("Nearby areas", [(f'{by[x]["city"]}, FL', f"/florida-locations/{x}/") for x in l.get("nearby", []) if x in by])
        schema = [{"@type": "Service", "name": f'Insurance appraisal in {l["city"]}, FL', "serviceType": "Property insurance appraisal",
                   "provider": {"@id": ORG_ID}, "url": url(path),
                   "areaServed": {"@type": "City", "name": f'{l["city"]}, FL', "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"]},
                                  "geo": {"@type": "GeoCoordinates", "latitude": l["lat"], "longitude": l["lng"]}}}]
        standard_page(path, trail, l["kicker"], esc(l["h1"]), esc(l["lead"]), main, aside, l.get("faqs"), schema,
                      l["title"], l["description"], "0.8", img=LOC_PHOTO[l["slug"]])


def build_tools():
    trail0 = [("Home", "/"), ("Free Tools", "/claim-tools/")]
    body = page_hero(trail0, "Free & private", "Free Florida insurance claim tools",
                     "Calculators and checklists that help you understand your claim before you talk to anyone. Everything runs in your browser — nothing you type is sent to us.", img="estimate-review-clipboard-laptop") + f"""
<section class="sec"><div class="wrap"><div class="grid g3">{''.join(tool_card(t) for t in TOOLS)}</div>
<p class="note" style="margin-top:40px">Tools provide general estimates for planning only. They are not appraisals, legal advice or a substitute for reading your policy.</p></div></section>""" + cta_band()
    write({"path": "/claim-tools/", "photo": "estimate-review-clipboard-laptop", "title": "Free Florida Insurance Claim Calculators & Tools",
           "description": "Free Florida claim tools: appraisal worth-it, hurricane deductible, ACV depreciation, claim deadline and roof calculators, plus an inventory builder.",
           "schema": [crumbs_schema(trail0)]}, body, "0.9")
    for t in TOOLS:
        path = f'/claim-tools/{t["slug"]}/'
        trail = trail0 + [(t["name"], path)]
        others = [x for x in TOOLS if x["slug"] != t["slug"]][:3]
        body = page_hero(trail, t["kicker"], esc(t["h1"]), esc(t["lead"])) + f"""
<section class="sec"><div class="wrap">
{t['ui']}
<div class="layout"><article class="prose">{prose(t['sections'])}<div style="margin-top:40px">{faq_block(t['faqs'])}</div>
<p class="note">Estimates only, for general planning. Results depend on your policy, your property and current pricing. Not legal advice.</p></article>
<aside class="aside">{call_box('Want a second opinion?')}{link_box('More free tools', [(x['name'], f"/claim-tools/{x['slug']}/") for x in others])}</aside></div>
</div></section>""" + cta_band()
        write({"path": path, "title": t["title"], "description": t["description"], "tools_js": True,
               "schema": [crumbs_schema(trail), faq_schema(t["faqs"]),
                          {"@type": "WebApplication", "name": t["name"], "url": url(path), "applicationCategory": "FinanceApplication",
                           "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORG_ID}}]},
              body, "0.8")


def build_blog():
    trail0 = [("Home", "/"), ("Guides", "/blog/")]
    posts = sorted(POSTS, key=lambda p: p["published"], reverse=True)
    body = page_hero(trail0, "Guides & articles", "Guides for Florida property insurance claims",
                     "Plain-English explanations of appraisal, deductibles, roof claims and what to do when a settlement falls short.", img="post-storm-flooding-florida") + f"""
<section class="sec"><div class="wrap"><div class="grid g3">{''.join(post_card(p) for p in posts)}</div></div></section>""" + cta_band()
    write({"path": "/blog/", "photo": "post-storm-flooding-florida", "title": f"Florida Insurance Claim Guides | {NAME}",
           "description": "Guides from Florida Insurance Appraiser on the appraisal clause, hurricane deductibles, roof claims, underpaid settlements and choosing claim help in Florida.",
           "schema": [crumbs_schema(trail0)]}, body, "0.8")
    for p in posts:
        path = f'/blog/{p["slug"]}/'
        trail = trail0 + [(p["h1"], path)]
        pub = date.fromisoformat(p["published"]).strftime("%B %-d, %Y")
        others = [x for x in posts if x["slug"] != p["slug"]][:3]
        schema = [{"@type": "BlogPosting", "headline": p["h1"], "description": p["description"], "datePublished": p["published"],
                   "dateModified": p.get("modified", p["published"]), "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID},
                   "mainEntityOfPage": url(path), "image": url("/assets/img/og-image.png")}]
        standard_page(path, trail, p["kicker"], esc(p["h1"]), esc(p["lead"]), prose(p["sections"]) + '<p class="note">General information, not legal advice. Policies differ; read yours and consult a Florida attorney on legal questions.</p>',
                      call_box() + link_box("More guides", [(x["h1"], f"/blog/{x['slug']}/") for x in others]),
                      p.get("faqs"), schema, p["title"], p["description"], "0.7",
                      extra_hero=f'<p class="post-meta">By {NAME} · {pub} · {p["read_min"]} min read</p>', img=POST_PHOTO[p["slug"]],
                      published=p["published"], og_type="article", modified=p.get("modified", p["published"]))


def build_resources():
    # about
    vals = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in ABOUT.get("values", []))
    main = prose(ABOUT["sections"]) + (f'<h2>What we hold ourselves to</h2><div class="grid g2">{vals}</div>' if vals else "")
    standard_page("/about/", [("Home", "/"), ("About", "/about/")], ABOUT["kicker"], esc(ABOUT["h1"]), esc(ABOUT["lead"]), main,
                  call_box() + link_box("Start here", [("Appraisal process", "/appraisal-process/"), ("All services", "/appraisal-services/"), ("Free tools", "/claim-tools/"), ("FAQ", "/faq/")]),
                  None, [{"@type": "AboutPage", "url": url("/about/"), "about": {"@id": ORG_ID}}], ABOUT["title"], ABOUT["description"], "0.7", img="property-inspector-clipboard")
    # process
    steps = "".join(f'<div class="card" style="margin-bottom:16px"><span class="num">Step {i + 1:02d}</span><h3>{esc(t)}</h3>{b}</div>' for i, (t, b) in enumerate(PROCESS["steps"]))
    main = steps + prose(PROCESS.get("sections", []))
    standard_page("/appraisal-process/", [("Home", "/"), ("Appraisal Process", "/appraisal-process/")], PROCESS["kicker"], esc(PROCESS["h1"]), esc(PROCESS["lead"]), main,
                  call_box() + link_box("Helpful tools", [(t["name"], f'/claim-tools/{t["slug"]}/') for t in TOOLS[:4]]),
                  PROCESS.get("faqs"), [{"@type": "HowTo", "name": PROCESS["h1"], "step": [{"@type": "HowToStep", "position": i + 1, "name": t} for i, (t, _) in enumerate(PROCESS["steps"])]}],
                  PROCESS["title"], PROCESS["description"], "0.8", img="inspector-checklist")
    # faq
    items = "".join(f'<details class="faq"><summary>{esc(q)}</summary><div class="a">{a if a.lstrip().startswith("<") else "<p>" + a + "</p>"}</div></details>' for q, a in FAQS)
    standard_page("/faq/", [("Home", "/"), ("FAQ", "/faq/")], "Straight answers", "Florida insurance appraisal FAQ",
                  "Answers to the questions Florida property owners ask most about appraisal, cost, timing and working with us.", items,
                  call_box() + link_box("Keep reading", [("Claim glossary", "/claim-glossary/"), ("Appraisal process", "/appraisal-process/"), ("Guides", "/blog/")]),
                  None, [faq_schema(FAQS)], "Florida Insurance Appraisal FAQ | Common Questions",
                  "Answers from Florida Insurance Appraiser on how appraisal works, what it costs, how long it takes, hurricane deductibles, condo claims and more.", "0.7", img="claim-meeting-paperwork")
    # glossary
    letters, dl, seen = [], [], set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        L = term[0].upper()
        anchor = ""
        if L not in seen:
            seen.add(L)
            letters.append(L)
            anchor = f' id="letter-{L}"'
        dl.append(f"<dt{anchor}>{esc(term)}</dt><dd>{esc(d)}</dd>")
    az = "".join(f'<a href="#letter-{L}">{L}</a>' for L in letters)
    standard_page("/claim-glossary/", [("Home", "/"), ("Claim Glossary", "/claim-glossary/")], "Decode the jargon", "Florida property claim glossary",
                  f"{len(GLOSSARY)} insurance and appraisal terms you’ll see in policies, estimates and adjuster letters — explained in plain English.",
                  f'<div class="az">{az}</div><dl class="gloss">{"".join(dl)}</dl>',
                  call_box() + link_box("Related", [("FAQ", "/faq/"), ("Appraisal process", "/appraisal-process/"), ("ACV calculator", "/claim-tools/acv-depreciation-calculator/")]),
                  None, [{"@type": "DefinedTermSet", "name": "Florida property claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}],
                  "Insurance Claim Glossary: Florida Appraisal Terms",
                  "Plain-English definitions of property insurance and appraisal terms used in Florida: ACV, RCV, umpire, hurricane deductible, matching, O&P and more.", "0.6", img="home-insurance-policy")
    # legal
    for key, path, h1, title in [("privacy", "/privacy-policy/", "Privacy policy", "Privacy Policy"),
                                 ("terms", "/terms-of-use/", "Terms of use", "Terms of Use"),
                                 ("disclaimer", "/disclaimer/", "Disclaimer", "Disclaimer")]:
        standard_page(path, [("Home", "/"), (h1, path)], "Legal", h1, f"How {NAME} handles this website and the information you share with us.",
                      prose(LEGAL[key]), link_box("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/")]),
                      None, None, f"{title} | {NAME}", f"Read the {title.lower()} for the {NAME} website, covering how the site, its free tools and the information you submit are handled.", "0.3")


def build_contact():
    trail = [("Home", "/"), ("Contact", "/contact/")]
    body = page_hero(trail, "Free claim review", f"Contact {NAME}",
                     "Call, email or send your claim details. We review the insurer’s estimate and your numbers at no cost and tell you plainly what we think.", img="insurance-documents-review") + f"""
<section class="sec"><div class="wrap split top">
<div><h2>Reach us directly</h2>
<ul class="contact-list">
<li>{ico('phone')}<a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></li>
<li>{ico('mail')}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
<li>{ico('pin')}<span>Serving all 67 Florida counties</span></li>
</ul>
<h3>Helpful to have on hand</h3>
<ul class="ticks"><li>Your claim number and date of loss</li><li>The insurer’s estimate and any payment letters</li><li>Your contractor’s estimate, if you have one</li><li>Photos or video of the damage</li><li>Your policy declarations page</li></ul>
<p class="note">Sending us information does not create an appraisal engagement. We are not a law firm and do not provide legal advice.</p></div>
{lead_form()}
</div></section>"""
    write({"path": "/contact/", "photo": "insurance-documents-review", "title": f"Contact {NAME} | Free Claim Review",
           "description": f"Contact {NAME} at {BIZ['phone_display']} or online for a free review of your disputed Florida property insurance claim. Statewide service.",
           "schema": [crumbs_schema(trail), {"@type": "ContactPage", "url": url("/contact/"), "about": {"@id": ORG_ID}}]}, body, "0.8")


def build_sitemap_page():
    groups = [("Main pages", [("Home", "/"), ("About", "/about/"), ("Contact", "/contact/"), ("Appraisal process", "/appraisal-process/"), ("FAQ", "/faq/"), ("Claim glossary", "/claim-glossary/")]),
              ("Services", [("All services", "/appraisal-services/")] + [(s["name"], f'/appraisal-services/{s["slug"]}/') for s in SERVICES]),
              ("Locations", [("All locations", "/florida-locations/")] + [(f'{l["city"]}, FL', f'/florida-locations/{l["slug"]}/') for l in LOCATIONS]),
              ("Free tools", [("All tools", "/claim-tools/")] + [(t["name"], f'/claim-tools/{t["slug"]}/') for t in TOOLS]),
              ("Guides", [("All guides", "/blog/")] + [(p["h1"], f'/blog/{p["slug"]}/') for p in POSTS]),
              ("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/")])]
    html = "".join(f'<h2>{g}</h2><ul>' + "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in items) + "</ul>" for g, items in groups)
    standard_page("/sitemap/", [("Home", "/"), ("Sitemap", "/sitemap/")], "Every page", "Sitemap", f"Every page on the {NAME} website.", html,
                  call_box(), None, None, f"Sitemap | {NAME}", f"A complete list of pages on the {NAME} website: services, Florida locations, free claim tools, guides and legal pages.", "0.3")


def build_404():
    body = page_hero([("Home", "/"), ("Page not found", "/404.html")], "Error 404", "That page washed out", "The page you’re looking for doesn’t exist or has moved. Try one of these instead.") + f"""
<section class="sec"><div class="wrap"><div class="grid g3">
<a class="card" href="/appraisal-services/">{ico('scale')}<h3>Appraisal services</h3><p>What we do for Florida property owners.</p></a>
<a class="card" href="/claim-tools/">{ico('chart')}<h3>Free claim tools</h3><p>Calculators and checklists for your claim.</p></a>
<a class="card" href="/contact/">{ico('phone')}<h3>Contact us</h3><p>Call {BIZ['phone_display']}.</p></a>
</div></div></section>"""
    write({"path": "/404.html", "file": "404.html", "title": f"Page not found | {NAME}", "description": "The page you requested could not be found.", "robots": "noindex, follow"}, body)


# ------------------------------------------------------------------ root files
INDEX_PHP = r"""<?php
// Front controller: serves the homepage and returns a real 404 for unknown URLs.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = $_SERVER['HTTP_HOST'] ?? '';
$home = 'https://floridainsuranceappraiser.com';
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.floridainsuranceappraiser.com' || ($insecure && $host === 'floridainsuranceappraiser.com')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""

CONTACT_PHP = r"""<?php
// Lead form handler for floridainsuranceappraiser.com.
// Sends each submission to the mailbox over authenticated SMTP (SSL). Credentials live in
// fia-mail-config.php one level above public_html, or public_html/_config/mail.php (a PHP file with a
// direct-access guard, uploaded separately and never part of this repository or of deploy.sh):
//   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@…', 'pass' => '…'];
// Every lead is also appended to public_html/_config/leads.php (guarded against web access).
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); echo json_encode(['ok' => false, 'error' => 'Method not allowed.']); exit; }
$private = dirname(__DIR__, 2);
$to = 'info@floridainsuranceappraiser.com';
$f = function ($k, $max = 200) { return trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max)); };
if ($f('website') !== '') { echo json_encode(['ok' => true]); exit; }          // honeypot
$name = $f('name', 120); $email = $f('email', 160); $phone = $f('phone', 40);
if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen(preg_replace('/\D/', '', $phone)) < 7) {
    http_response_code(422); echo json_encode(['ok' => false, 'error' => 'Please enter your name, a valid email and phone number.']); exit;
}
if ($f('consent') !== 'yes') { http_response_code(422); echo json_encode(['ok' => false, 'error' => 'Please tick the consent box.']); exit; }
$fields = ['Name' => $name, 'Email' => $email, 'Phone' => $phone, 'Location' => $f('location'), 'Role' => $f('role'),
           'Type of loss' => $f('loss_type'), 'Message' => $f('message', 5000)];
$body = "New claim review request from floridainsuranceappraiser.com\n\n";
foreach ($fields as $k => $v) { $body .= str_pad($k . ':', 14) . ($k === 'Message' ? "\n" : '') . $v . "\n"; }
$body .= "\nPage: " . ($_SERVER['HTTP_REFERER'] ?? '') . "\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\nTime: " . gmdate('c') . "\n";
$subject = 'Claim review request: ' . $name . ($fields['Type of loss'] ? ' (' . $fields['Type of loss'] . ')' : '');

function fia_smtp(array $c, string $to, string $subject, string $body, string $replyTo, string $replyName) {
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client('ssl://' . $c['host'] . ':' . (int)$c['port'], $en, $es, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) { return 'connect failed: ' . $es; }
    stream_set_timeout($fp, 20);
    $step = function ($line, $expect, $label) use ($fp) {
        if ($line !== null) { fwrite($fp, $line . "\r\n"); }
        $resp = '';
        while (($l = fgets($fp, 1024)) !== false) { $resp .= $l; if (strlen($l) < 4 || $l[3] === ' ') { break; } }
        if ((int)substr($resp, 0, 3) !== $expect) { throw new RuntimeException($label . ': ' . trim($resp)); }
    };
    $enc = function ($s) { return '=?UTF-8?B?' . base64_encode($s) . '?='; };
    try {
        $step(null, 220, 'greeting');
        $step('EHLO floridainsuranceappraiser.com', 250, 'ehlo');
        $step('AUTH LOGIN', 334, 'auth');
        $step(base64_encode($c['user']), 334, 'auth user');
        $step(base64_encode($c['pass']), 235, 'auth pass');
        $step('MAIL FROM:<' . $c['user'] . '>', 250, 'mail from');
        $step('RCPT TO:<' . $to . '>', 250, 'rcpt to');
        $step('DATA', 354, 'data');
        $safeReply = str_replace(["\r", "\n", '<', '>'], '', $replyTo);
        $msg = 'Date: ' . date('r') . "\r\n"
             . 'From: ' . $enc('Florida Insurance Appraiser Website') . ' <' . $c['user'] . ">\r\n"
             . 'To: <' . $to . ">\r\n"
             . 'Reply-To: ' . $enc($replyName) . ' <' . $safeReply . ">\r\n"
             . 'Subject: ' . $enc($subject) . "\r\n"
             . 'Message-ID: <' . bin2hex(random_bytes(12)) . "@floridainsuranceappraiser.com>\r\n"
             . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
             . rtrim(chunk_split(base64_encode($body), 76, "\r\n")) . "\r\n.";
        $step($msg, 250, 'message');
        $step('QUIT', 221, 'quit');
    } catch (Throwable $e) { fclose($fp); return $e->getMessage(); }
    fclose($fp);
    return true;
}

$cfgFile = is_readable($private . '/fia-mail-config.php') ? $private . '/fia-mail-config.php' : dirname(__DIR__) . '/_config/mail.php';
$result = 'no mail config';
if (is_readable($cfgFile)) {
    $cfg = include $cfgFile;
    $result = fia_smtp($cfg, $to, $subject, $body, $email, $name);
}
if ($result !== true) {                                    // fall back to the local mailer
    $headers = "From: Florida Insurance Appraiser <$to>\r\nReply-To: " . str_replace(["\n", "\r"], '', $email) . "\r\nContent-Type: text/plain; charset=utf-8";
    $fallback = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $to);
    $result = ['smtp_error' => $result, 'mail_fallback' => $fallback];
}
// Backup log: a guarded .php file in public_html/_config (web requests get a 404; readable in the file manager).
$log = dirname(__DIR__) . '/_config/leads.php';
if (!is_dir(dirname($log))) { @mkdir(dirname($log), 0750, true); }
if (!file_exists($log)) { @file_put_contents($log, "<?php http_response_code(404); exit; ?>\n"); }
@file_put_contents($log, json_encode($fields + ['time' => gmdate('c'), 'delivery' => $result], JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
echo json_encode(['ok' => true]);
"""



def build_root_files():
    w = lambda rel, txt: open(os.path.join(OUT, rel), "w", encoding="utf-8").write(txt)
    w("index.php", INDEX_PHP)
    os.makedirs(os.path.join(OUT, "api"), exist_ok=True)
    w("api/contact.php", CONTACT_PHP)
    for f in ("favicon.svg", "favicon.ico", "favicon-96x96.png", "web-app-manifest-192x192.png", "web-app-manifest-512x512.png"):
        shutil.copy(os.path.join(ROOT, "assets/icons", f), os.path.join(OUT, f))
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {url('/sitemap.xml')}\n")
    w("site.webmanifest", json.dumps({"name": NAME, "short_name": "FL Appraiser", "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"}, {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}, {"src": "/favicon.svg", "type": "image/svg+xml", "sizes": "any"}], "theme_color": "#0f4c4a", "background_color": "#ffffff", "display": "standalone"}, indent=1))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, mod, pri in SITEMAP:
        xml.append(f"<url><loc>{url(path)}</loc><lastmod>{mod}</lastmod><priority>{pri}</priority></url>")
    xml.append("</urlset>")
    w("sitemap.xml", "\n".join(xml) + "\n")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    build_home()
    build_services()
    build_locations()
    build_tools()
    build_blog()
    build_resources()
    build_contact()
    build_sitemap_page()
    build_404()
    build_root_files()
    n = sum(1 for _, _, fs in os.walk(OUT) for f in fs if f.endswith(".html"))
    print(f"built {n} html files into {OUT}")


if __name__ == "__main__":
    main()
