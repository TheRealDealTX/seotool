#!/usr/bin/env python3
"""Static site generator for michiganinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
Engineering derived from the georgiainsuranceappraiser template (guard, front controller, schema, deploy);
the layout, design, URL structure and copy are specific to this site.
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
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Michigan Insurance Appraiser"
HOST = "michiganinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261117a"
FAV = "1"
FONTS = "https://fonts.googleapis.com/css2?family=Sofia+Sans+Condensed:wght@600;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap"

# Google Tag Manager: leave empty until a container ID is supplied (e.g. "GTM-XXXXXXX").
GTM_ID = "GTM-MNMHPK67"
# If the owner supplies a full snippet, paste it here verbatim; otherwise the standard snippet is generated from GTM_ID.
GTM_HEAD_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-MNMHPK67"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

# Search Console verification file: written byte-for-byte at the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

# URL structure (unique to this site)
SVC_BASE = "/michigan-claim-appraisal/"
LOC_BASE = "/mi-cities-served/"
TOOL_BASE = "/mi-claim-calculators/"
POST_BASE = "/great-lakes-claim-guides/"
PROCESS = "/michigan-appraisal-process/"
FAQ_P = "/michigan-appraisal-questions/"
GLOSS = "/insurance-claim-terms/"
ABOUT = "/about-our-appraisers/"
CONTACT = "/request-claim-review/"
PRIVACY = "/privacy/"
TERMS = "/terms/"
DISCLAIM = "/legal-disclaimer/"
SITEMAP = "/all-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def svc_path(s):
    return f"{SVC_BASE}{s['slug']}/"


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-insurance-appraiser/"


def tool_path(t):
    return f"{TOOL_BASE}{t['slug']}/"


def post_path(p):
    return f"{POST_BASE}{p['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}
TOOL_BY = {t["slug"]: t for t in TOOLS}

# ---------------------------------------------------------------- photos
def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "meeting-table", "homeowner-claim-appraiser": "suburban-home",
    "commercial-condo-hoa-appraisal": "apartment-block", "hail-roof-damage-appraisal": "roof-shingles",
    "windstorm-tornado-appraisal": "tornado-damage", "ice-dam-frozen-pipe-appraisal": "icicles",
    "water-sewer-backup-appraisal": "flooded-basement", "fire-smoke-loss-appraisal": "house-fire",
    "fallen-tree-ice-storm-appraisal": "ice-storm-tree", "contents-personal-property-appraisal": "living-room",
    "insurance-estimate-second-opinion": "calculator-papers", "neutral-umpire-services": "handshake",
}
SVC_ICON = {
    "appraisal-demand-representation": "doc", "homeowner-claim-appraiser": "home", "commercial-condo-hoa-appraisal": "building",
    "hail-roof-damage-appraisal": "hail", "windstorm-tornado-appraisal": "wind", "ice-dam-frozen-pipe-appraisal": "snow",
    "water-sewer-backup-appraisal": "drop", "fire-smoke-loss-appraisal": "flame", "fallen-tree-ice-storm-appraisal": "tree",
    "contents-personal-property-appraisal": "box", "insurance-estimate-second-opinion": "file", "neutral-umpire-services": "scale",
}
LOC_PHOTO = {
    "detroit": "detroit-skyline", "grand-rapids": "city-grand-rapids", "ann-arbor": "city-ann-arbor", "lansing": "lansing-capitol",
    "flint": "storm-sky", "dearborn": "city-dearborn", "troy": "suburban-home", "sterling-heights": "winter-street", "kalamazoo": "tornado-damage",
    "saginaw": "flood-street", "traverse-city": "city-traverse-city", "marquette": "city-marquette",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-papers", "rcv-acv-holdback-calculator": "calculator", "roof-squares-pitch-calculator": "roofers",
    "percentage-deductible-calculator": "lightning", "claim-deadline-planner": "clipboard", "appraisal-readiness-score": "paperwork",
    "ice-dam-risk-cost-estimator": "snow-roofs",
}
POST_PHOTO = {
    "michigan-appraisal-clause-explained": "meeting-table", "appraiser-public-adjuster-or-attorney": "meeting",
    "ice-dam-claims-in-michigan": "icicles", "basement-backup-coverage-gaps": "flood-street",
    "reading-your-xactimate-estimate": "calculator", "should-you-demand-appraisal": "paperwork",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "right": '<path d="M9 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3l3 3 3-3M9 21l3-3 3 3M3 9l3 3-3 3M21 9l-3 3 3 3"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "tree": '<path d="M12 22v-5M7 17h10l-3-4h2l-4-5h1.5L12 3 8.5 8H10l-4 5h2z"/>',
    "box": '<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "calc": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/>',
}


def ic(name, cls="ic", size=20):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


MARK_SVG = ('<rect width="48" height="48" rx="12" fill="#00274C"/>'
            '<path d="M10 33V17.5l7 9.5 7-9.5 7 9.5 7-9.5V33" fill="none" stroke="#FFCB05" stroke-width="4.4" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M13 39.5h22" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>')


def mark(size=42):
    """Brand mark: twin roof peaks forming an M (maize) over an estimate line (white) on a blue tile."""
    return f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">{MARK_SVG}</svg>'


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Michigan</b><small>Insurance Appraiser</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "MI", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-MI", "availableLanguage": "en"}],
        "slogan": "Independent appraisal for underpaid Michigan property claims",
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 83 Michigan counties.",
        "areaServed": [{"@type": "State", "name": "Michigan"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": DOMAIN + svc_path(s)}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Xactimate estimating", "Ice dam claims", "Sewer backup claims", "Hail damage"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]}


def itemlist(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- navigation
LEARN = [("Appraisal process guide", PROCESS), ("Appraisal questions (FAQ)", FAQ_P), ("Claim terms glossary", GLOSS), ("Great Lakes claim guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], svc_path(s)) for s in SERVICES], ("All 12 services", SVC_BASE)),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("Statewide coverage", LOC_BASE)),
        ("Calculators", [(t["name"], tool_path(t)) for t in TOOLS], ("All free calculators", TOOL_BASE)),
        ("Resources", LEARN, None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="mm-all"><a href="{allk[1]}">{e(allk[0])} {ic("arrow")}</a></li>'
        cols = " mm-2" if len(links) > 7 else ""
        menu += (f'<li class="mm"><button type="button" class="mm-btn" aria-expanded="false" aria-controls="mm-{i}">{name}{ic("chev", "ic chev", 16)}</button>'
                 f'<div class="mm-panel" id="mm-{i}"><ul class="{cols.strip()}">{li}</ul></div></li>')
    menu += f'<li><a class="nav-a" href="{ABOUT}">About</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="acc-all" href="{allk[1]}">{e(allk[0])}</a></li>'
        acc += (f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "ic chev", 18)}</button>'
                f'<div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>')
    acc += f'<li><a class="acc-link" href="{ABOUT}">About</a></li><li><a class="acc-link" href="{CONTACT}">Contact</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="masthead" id="top"><div class="wrap mast-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="nav-list">{menu}</ul></nav>
<div class="mast-cta"><a class="mast-phone" href="tel:{TEL}">{ic("phone", "ic", 18)}<span>{PHONE}</span></a><a class="btn btn-maize btn-sm" href="{CONTACT}">Free review</a></div>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="scrim" data-close hidden></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand drawer-brand")}<button class="drawer-x" type="button" aria-label="Close menu" data-close>{ic("x", "ic", 22)}</button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-maize btn-block" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-outline btn-block" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · Both peninsulas</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:9])
    tl = "".join(f'<li><a href="{tool_path(t)}">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand foot-brand")}
<p>Independent appraisal and estimating help for Michigan property owners whose covered claims came up short, from Monroe to the Keweenaw.</p>
<ul class="foot-lines"><li>{ic("phone", "ic", 16)}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail", "ic", 16)}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock", "ic", 16)}<span>Mon–Fri 8am–6pm ET</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2 class="foot-h">Cities</h2><ul>{loc}<li><a href="{LOC_BASE}">All of Michigan</a></li></ul></div>
<div><h2 class="foot-h">Calculators</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Company</h2><ul><li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Claim guides</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. All rights reserved.</p>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCLAIM}">Disclaimer</a></li><li><a href="{SITEMAP}">Site map</a></li></ul></div>
<p class="wrap foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Content on this site is general information; your policy’s wording controls. Example figures are illustrative, and no outcome is guaranteed.</p>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone", "ic", 18)} Call now</a><a href="{CONTACT}">{ic("file", "ic", 18)} Free review</a></div>"""


# ---------------------------------------------------------------- document
def gtm_head():
    if not GTM_ID:
        return ""
    if GTM_HEAD_SNIPPET:
        return GTM_HEAD_SNIPPET.rstrip() + "\n"
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
            'style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage")
MAIN_TYPES = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")
OG_ALT = f"{BRAND}: independent property claim appraisal across both Michigan peninsulas"


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", preload=None, body_cls=""):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in PAGE_TYPES:
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        if t in MAIN_TYPES:
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
        extra.append(n)
    img_key = preload or "hero-home"
    pimg = PHOTOS[img_key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{img_key}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    mains = [n["@id"] for n in extra if n.get("@type") in MAIN_TYPES]
    if path == "/":
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    elif mains:
        webpage["mainEntity"] = {"@id": mains[0]}
    elif any(n.get("@type") == "FAQPage" for n in extra):
        webpage["mainEntity"] = {"@id": canonical + "#faq"}
    else:
        webpage["mainEntity"] = {"@id": DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = ""
    if preload:
        pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{preload}.webp" imagesrcset="/assets/img/photos/{preload}-640.webp 640w, '
               f'/assets/img/photos/{preload}.webp {PHOTOS[preload]["fw"]}w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{OG_ALT}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{OG_ALT}">
<meta name="geo.region" content="US-MI">
<meta name="geo.placename" content="Michigan">
<meta name="theme-color" content="#00274C">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
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
    # The host serves real files without running the front controller, so every page other than the
    # homepage is dir/index.php and starts with the canonical-host guard (www/http 301, off-domain noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
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
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="ph-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = (f'<div class="btn-row"><a class="btn btn-maize" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a>'
         f'<a class="btn btn-glass" href="{CONTACT}">Free claim review</a></div>') if cta else ""
    return (f'<section class="ph"><div class="ph-media">{img(photo, "ph-img", lazy=False, alt="")}</div>'
            f'<div class="wrap ph-in">{crumbs(trail)}<p class="eyebrow eyebrow-light">{e(tag)}</p><h1>{e(h1)}</h1>'
            f'<p class="ph-lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="qa">' + "".join(
        f'<details><summary><span>{e(q)}</span><i class="qa-plus" aria-hidden="true"></i></summary><div class="qa-a"><p>{a}</p></div></details>'
        for q, a in faqs) + "</div>"


def call_box():
    return (f'<div class="sbox sbox-call"><h2 class="sbox-t">Talk to an appraiser</h2><p>A free, no-pressure call. We’ll tell you plainly whether appraisal fits your claim.</p>'
            f'<a class="sbox-phone" href="tel:{TEL}">{ic("phone")} {PHONE_INTL}</a><a class="btn btn-maize btn-block" href="{CONTACT}">Send claim details</a>'
            f'<small>Mon–Fri 8am–6pm ET</small></div>')


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right", "ic", 16)}</a></li>' for n, p in items)
    return f'<div class="sbox"><h2 class="sbox-t">{e(title)}</h2><ul class="sbox-list">{li}</ul></div>'


def aside(*boxes):
    return '<aside class="side"><div class="side-in">' + "".join(boxes) + "</div></aside>"


def cta_band(h="Think the carrier’s number is too low?", p="Send the estimate and a handful of photos. We’ll tell you what we see, free."):
    return (f'<section class="band"><div class="wrap band-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div>'
            f'<div class="btn-row"><a class="btn btn-maize" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-glass" href="{CONTACT}">Email the estimate</a></div></div></section>')


def related(items, label):
    return '<div class="rel">' + "".join(f'<a href="{p}"><small>{e(label)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for n, p in items) + "</div>"


LOSSES = ["Hail / roof", "Wind / tornado", "Ice dam / frozen pipe", "Water / sewer backup", "Fallen tree / ice storm", "Fire / smoke", "Contents", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(title="Tell us about your claim", sub="Free review, no obligation. We usually reply within one business day.", page="/", uid="f", compact=False):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "Condo association / HOA", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Michigan"]
    if compact:
        mid = f"""<div class="span2"><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>"""
        tail = ""
    else:
        mid = f"""<div><label for="{uid}-role">I am a…</label><select id="{uid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{uid}-loss">Type of loss</label><select id="{uid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{uid}-city">Property location</label><select id="{uid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{uid}-amt">Amount in dispute</label><select id="{uid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="span2"><label for="{uid}-car">Insurance company (optional)</label><input id="{uid}-car" name="carrier"></div>"""
        tail = f"""<div class="span2"><label for="{uid}-det">What happened, and where does the claim stand?</label><textarea id="{uid}-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>"""
    return f"""<form class="lead{" lead-compact" if compact else ""}" action="/api/contact.php" method="post" data-lead novalidate>
<p class="lead-t">{e(title)}</p><p class="lead-sub">{e(sub)}</p>
<div class="fgrid">
<div><label for="{uid}-name">Full name *</label><input id="{uid}-name" name="name" autocomplete="name" required></div>
<div><label for="{uid}-phone">Phone *</label><input id="{uid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="span2"><label for="{uid}-email">Email *</label><input id="{uid}-email" name="email" type="email" autocomplete="email" required></div>
{mid}
{tail}
<div class="span2 hp" aria-hidden="true"><label for="{uid}-web">Website</label><input id="{uid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="span2"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Submitting this form doesn’t create a client relationship. See the <a href="{PRIVACY}">privacy policy</a>.</span></label></div>
<div class="span2"><button class="btn btn-blue btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


# ---------------------------------------------------------------- home data
REGIONS = [
    ("metro", "Metro Detroit", "Wayne · Oakland · Macomb", ["Basement flooding", "Sewer backup", "Hail", "Ice storms"],
     "Brick bungalows in Detroit and Dearborn, postwar ranches in Warren and Sterling Heights, and big colonials in Troy all share one weakness: basements. The August 2014 and June 2021 floods filled thousands of them, and the February 2023 ice storm dropped limbs across the region.",
     "detroit-skyline", ["detroit", "dearborn", "troy", "sterling-heights"]),
    ("west", "West Michigan", "Kent · Ottawa · Kalamazoo", ["Lake-effect snow", "Tornadoes", "River flooding", "Hail"],
     "From Grand Rapids to the lakeshore, snow belt winters load roofs and build ice dams, and spring storms track in off Lake Michigan. The 1956 Hudsonville–Standale tornado, the 1980 Kalamazoo tornado and the 2024 Portage tornado frame the risk.",
     "city-grand-rapids", ["grand-rapids", "kalamazoo"]),
    ("mid", "Mid-Michigan & the Bay", "Ingham · Genesee · Saginaw", ["Ice storms", "Tornado history", "Dam & river flooding", "Older housing"],
     "Lansing still remembers the December 2013 ice storm, Flint the 1953 Flint–Beecher tornado, and the Great Lakes Bay region the 2020 Edenville and Sanford dam failures. Housing ranges from early-1900s neighborhoods to newer suburbs.",
     "lansing-capitol", ["lansing", "flint", "saginaw", "ann-arbor"]),
    ("north", "Northern Michigan", "Grand Traverse · Otsego · Emmet", ["Snow load", "Seasonal homes", "Wind off the bays", "Frozen pipes"],
     "Cottages, condos and year-round homes around Traverse City and Gaylord face heavy snow and long freezes, and the May 2022 Gaylord tornado showed how quickly a summer storm can hit up north. Vacancy and heat conditions matter for seasonal homes.",
     "city-traverse-city", ["traverse-city"]),
    ("up", "Upper Peninsula", "Marquette · Houghton · Chippewa", ["Extreme snow load", "Ice dams", "Lake Superior wind", "Wood-frame homes"],
     "The U.P. measures snow in feet, not inches. Older wood-frame homes, camps and commercial buildings along Lake Superior see roof collapse risk, ice dams and gales that rival the November storms of Great Lakes history.",
     "city-marquette", ["marquette"]),
]

SEASONS = [
    ("Winter", "snow", "Ice dams, frozen and burst pipes, snow-load collapse and ice storms.", ["Late-January 2019 polar vortex", "February 2023 southeast ice storm", "December 2013 mid-Michigan ice storm"]),
    ("Spring", "hail", "Hail, tornadoes and river flooding as storms build across the Lower Peninsula.", ["April 1965 Palm Sunday outbreak", "April 2013 Grand River crest", "May 2024 Portage tornado"]),
    ("Summer", "drop", "Flash floods, sewer backups, derechos and lightning fires.", ["August 2014 metro Detroit flood", "June 2021 Detroit-area flooding", "Labor Day 1998 derecho"]),
    ("Fall", "wind", "Gales off the Great Lakes, fallen trees and heating-season fires.", ["November 1913 Great Lakes storm", "Autumn windstorms on the lakeshore", "Wood stove and furnace fires"]),
]

HOME_FAQ = [
    ("What does a Michigan insurance appraiser do?", "An insurance appraiser builds an independent valuation of a covered loss and, when either side demands appraisal under the policy, serves on the panel that sets the amount of loss. We also review estimates before a dispute escalates and serve as neutral umpires."),
    ("Is appraisal required in Michigan policies?", "Michigan’s Insurance Code requires property policies covering fire to include an appraisal provision, and most homeowners and commercial policies contain one. Read your own policy’s appraisal condition for the exact wording and deadlines."),
    ("Can appraisal decide whether my claim is covered?", "Generally no. Appraisal decides the amount of loss. If the insurer denied coverage, talk with a Michigan attorney about your options."),
    ("How much does an appraiser cost?", "Fees vary by claim size and complexity and may be flat, hourly or a percentage of the increase. Each side typically pays its own appraiser and splits the umpire. We put our fee in writing before any work starts."),
    ("Do you work in the Upper Peninsula?", "Yes. We work in all 83 counties on both peninsulas, from Detroit and Grand Rapids to Marquette, Houghton and Sault Ste. Marie."),
    ("Are you a public adjuster or a law firm?", "Neither. We provide appraisal, estimating and umpire services. If your claim needs a public adjuster or an attorney instead, we’ll tell you."),
]


def home():
    K = BRAND
    S = SERVICES
    feature = S[0]
    bento = (f'<a class="bento-card bento-feature rv" href="{svc_path(feature)}"><span class="bc-img">{img(SVC_PHOTO[feature["slug"]], sizes="(max-width:760px) 100vw, 50vw", alt="")}</span>'
             f'<span class="bc-body"><span class="bc-ic">{ic(SVC_ICON[feature["slug"]], "ic", 22)}</span><h3>{e(feature["name"])}</h3><p>{e(feature["short"])}</p><span class="more">How representation works {ic("arrow")}</span></span></a>')
    bento += "".join(
        f'<a class="bento-card rv" href="{svc_path(s)}"><span class="bc-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:560px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}</span>'
        f'<span class="bc-body"><span class="bc-ic">{ic(SVC_ICON[s["slug"]], "ic", 20)}</span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span></a>'
        for s in S[1:])
    tabs = "".join(f'<button type="button" role="tab" class="rtab" id="rt-{k}" aria-controls="rp-{k}" aria-selected="{"true" if i == 0 else "false"}">{e(n)}</button>' for i, (k, n, *_r) in enumerate(REGIONS))
    panels = "".join(
        f'<div class="rpanel" role="tabpanel" id="rp-{k}" aria-labelledby="rt-{k}">'
        f'<div class="rp-img">{img(ph, sizes="(max-width:900px) 100vw, 50vw", alt=PHOTOS[ph]["alt"])}</div>'
        f'<div class="rp-body"><p class="eyebrow">{e(sub)}</p><h3>{e(n)}</h3><p>{e(txt)}</p><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul>'
        f'<p class="rp-links">{" ".join(f"<a href=\"{loc_path(LOC_BY[c])}\">{e(LOC_BY[c]["city"])} {ic("right", "ic", 14)}</a>" for c in cities)}</p></div></div>'
        for k, n, sub, chips, txt, ph, cities in REGIONS)
    seasons = "".join(
        f'<article class="season rv"><span class="season-ic">{ic(icn, "ic", 26)}</span><h3>{e(n)}</h3><p>{e(t)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in xs)}</ul></article>'
        for n, icn, t, xs in SEASONS)
    steps = "".join(f'<li class="tl-step"><span class="tl-num">{i + 1:02d}</span><div class="tl-card"><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(PROCESS_STEPS))
    tools = "".join(
        f'<a class="tcard" href="{tool_path(t)}"><span class="tc-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 80vw, 320px", alt="")}<span class="tc-kind">{e(t["kind"])}</span></span>'
        f'<span class="tc-body"><h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><span class="more">Open {ic("arrow")}</span></span></a>' for t in TOOLS)
    cities = "".join(
        f'<a class="city rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], "city-img", sizes="(max-width:640px) 50vw, (max-width:1100px) 33vw, 25vw", alt="")}'
        f'<span class="city-b"><h3>{e(l["city"])}</h3><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    guides = "".join(
        f'<article class="gcard rv"><a class="gc-img" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:760px) 100vw, 33vw", alt="")}</a>'
        f'<div class="gc-body"><p class="meta">{e(p["read"])} read</p><h3><a href="{post_path(p)}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p></div></article>' for p in POSTS[:3])
    mini = GAP_MINI.replace("{u}", "hm")

    body = f"""<section class="hero">
<div class="hero-media">{img("hero-home", "hero-img", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow eyebrow-maize">Both peninsulas · All 83 counties</p>
<h1>{K} for claims that came up short</h1>
<p class="hero-lede">Hail on the roof, a basement full of sewer water, ice dams through the ceiling. When your carrier accepts the claim but won’t pay what the repair really costs, {K} gives you an independent number and an appraiser to stand behind it.</p>
<div class="btn-row"><a class="btn btn-maize" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-glass" href="#estimate">Run the numbers</a></div>
<ul class="hero-ticks"><li>{ic("check", "ic", 18)}Independent of carriers and contractors</li><li>{ic("check", "ic", 18)}Line-item estimates, local pricing</li><li>{ic("check", "ic", 18)}Fees in writing up front</li></ul>
</div>
<div class="hero-form">{lead_form("Free claim review", "Tell us the basics. An appraiser calls you back, usually within one business day.", "/ (hero)", "hf", compact=True)}</div>
</div></section>

<section class="ribbon" aria-label="Michigan at a glance"><div class="wrap ribbon-in">
<div class="rb rv"><b><span data-count="83">83</span></b><span>counties covered, on both peninsulas</span></div>
<div class="rb rv"><b><span data-count="20">20</span> days</b><span>to name an appraiser under the statutory form</span></div>
<div class="rb rv"><b><span data-count="2">2</span> of 3</b><span>signatures make an appraisal award</span></div>
<div class="rb rv"><b><span data-count="12">12</span></b><span>appraisal and estimating services</span></div>
</div></section>

<section class="sec"><div class="wrap duo">
<div class="duo-l rv"><p class="eyebrow">Who we are</p><h2>What a {K} actually does</h2>
<figure class="duo-img">{img("roofers", sizes="(max-width:900px) 100vw, 45vw")}</figure></div>
<div class="duo-r rv">
<p class="big">Most Michigan homeowners and business owners never think about the appraisal clause until a claim goes sideways. The carrier agrees the loss is covered, then sends an estimate that won’t rebuild the roof or dry out the basement. That gap is where {K} works.</p>
<ol class="jobs">
<li><b>Measure and price it ourselves.</b> We inspect, measure every roof plane and room, and write a line-item estimate with current local pricing, so the number on the table is grounded in your property, not a desk review.</li>
<li><b>Tell you whether appraisal fits.</b> Appraisal settles the amount of loss. If the real fight is coverage, a {K} will say so and point you toward the right help.</li>
<li><b>Serve as your appraiser.</b> When appraisal is demanded, we are the competent, independent appraiser you name, and we work the panel through to a signed award.</li>
<li><b>Act as a neutral umpire.</b> On other claims, we sit in the middle and decide the items two appraisers can’t settle.</li>
</ol>
<p>Every {K} file starts the same way: a free conversation about what happened, what the carrier paid and what you think it missed.</p>
</div></div></section>

<section class="sec sec-ice" id="services"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Services</p><h2>Twelve services from your {K}, one question: what does the damage really cost?</h2><p>From one estimate review to full panel representation, each service is built around a defensible valuation of a Michigan loss.</p></div>
<div class="bento" data-stagger>{bento}</div>
<p class="center"><a class="btn btn-blue" href="{SVC_BASE}">See all services {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">From Monroe to the Keweenaw</p><h2>Five Michigan regions, five claim patterns</h2><p>The same policy reads very differently in a Dearborn bungalow and a Marquette camp. A {K} prices each with the region in mind.</p></div>
<div class="regions rv" data-tabs><div class="rtabs" role="tablist" aria-label="Michigan regions">{tabs}</div><div class="rpanels">{panels}</div></div>
</div></section>

<section class="sec sec-blue"><div class="wrap">
<div class="sec-head sec-head-light rv"><p class="eyebrow eyebrow-maize">A year of claims</p><h2>Michigan’s claim calendar, season by season</h2><p>Every season brings its own losses. These are the patterns a {K} sees most, with storms Michigan owners still talk about.</p></div>
<div class="seasons" data-stagger>{seasons}</div>
</div></section>

<section class="sec"><div class="wrap split">
<div class="split-l rv"><p class="eyebrow">The process</p><h2>How appraisal runs, from demand letter to award</h2><p>Michigan’s Insurance Code sets the basic shape: a written demand, two independent appraisers, an umpire if needed, and an award signed by any two of the three. Here is how a {K} moves a claim through it.</p><a class="btn btn-line" href="{PROCESS}">Read the full process guide {ic("arrow")}</a></div>
<ol class="timeline" data-timeline><li class="tl-rail" aria-hidden="true"><i class="tl-fill"></i></li>{steps}</ol>
</div></section>

<section class="sec sec-maize" id="estimate"><div class="wrap split split-tool">
<div class="rv"><p class="eyebrow">Quick check</p><h2>Is your dispute big enough for appraisal?</h2><p>Enter the carrier’s estimate and your own. The figures shown are illustrative defaults; replace them with yours. For fees, umpire costs and break-even, open the <a href="{tool_path(TOOLS[0])}">full claim gap and fee estimator</a>.</p></div>
<div class="rv">{mini}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head sec-head-row rv"><div><p class="eyebrow">Free calculators</p><h2>Seven free tools from a {K}</h2></div><div class="rail-btns"><button type="button" class="rail-btn" data-rail="-1" aria-label="Scroll tools left">{ic("arrow", "ic flip")}</button><button type="button" class="rail-btn" data-rail="1" aria-label="Scroll tools right">{ic("arrow")}</button></div></div>
<p class="rail-note rv">Built from real appraisal work. Everything runs in your browser and nothing is stored.</p>
<div class="rail" data-rail-track>{tools}</div>
</div></section>

<section class="sec sec-ice"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Cities</p><h2>{K} service in twelve Michigan cities</h2><p>On-site inspections statewide. These pages cover the places our files come from most, with local storm history and housing notes.</p></div>
<div class="cities" data-stagger>{cities}</div>
<p class="center"><a class="btn btn-line" href="{LOC_BASE}">All Michigan coverage {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each plays a different role on a Michigan claim. A {K} handles valuation; the others handle the rest.</p></div>
<div class="tbl-wrap rv"><table class="compare"><thead><tr><th scope="col">Question</th><th scope="col">Insurance appraiser</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td>Values the loss; serves on the appraisal panel</td><td>Prepares and negotiates the whole claim for you</td><td>Advises on rights, coverage and litigation</td></tr>
<tr><th scope="row">Best when</th><td>Coverage is accepted; the dispute is the dollar amount</td><td>The claim is large or complex from the start</td><td>Coverage is denied or deadlines are close</td></tr>
<tr><th scope="row">Decides coverage?</th><td>No</td><td>No (negotiates it)</td><td>Can litigate it</td></tr>
<tr><th scope="row">Typical fee</th><td>Flat, hourly or percentage, agreed in writing</td><td>Usually a percentage of the claim, within state rules</td><td>Varies; often contingency or hourly</td></tr>
</tbody></table></div>
<p class="center rv"><a href="{post_path(POSTS[1])}">Read the full comparison guide {ic("arrow", "ic", 16)}</a></p>
</div></section>

<section class="sec sec-ice"><div class="wrap split split-top">
<div class="rv"><p class="eyebrow">Questions</p><h2>What owners ask a {K}</h2><p>Short answers to common questions. The <a href="{FAQ_P}">full FAQ</a> goes deeper on costs, timing and Michigan specifics.</p></div>
<div class="rv">{faq_block(HOME_FAQ)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="eyebrow">Great Lakes claim guides</p><h2>Read before you sign anything</h2></div>
<div class="gcards" data-stagger>{guides}</div>
</div></section>

<section class="pcta"><div class="pcta-media">{img("mackinac-bridge", "pcta-img", alt="", extra=' data-parallax="0.2"')}</div>
<div class="wrap pcta-in rv"><p class="eyebrow eyebrow-maize">Statewide, both peninsulas</p><h2>The cheapest time to question a settlement is before you cash it</h2><p>A {K} review costs nothing and takes one phone call. Bring the estimate; we’ll bring the questions.</p>
<div class="btn-row"><a class="btn btn-maize" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-glass" href="{CONTACT}">Send claim details</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv"><p class="eyebrow">Get in touch</p><h2>Talk with a {K} about your claim</h2>
<p>Call, text or email, or send the form. We’ll review what you have, explain where the estimates differ, and tell you honestly whether appraisal makes sense.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 83 Michigan counties</b></div></li></ul></div>
<div class="rv">{lead_form("Send your claim details", page="/ (contact)", uid="hc")}</div>
</div></section>"""
    schema = [faq_schema(HOME_FAQ)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Michigan Insurance Appraiser: independent appraisal, estimate review and umpire services for underpaid property claims in all 83 counties.",
                        body, schema, preload="hero-home", body_cls="home"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], svc_path(s)) for s in SERVICES]
    locs = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]]
    for idx, s in enumerate(SERVICES):
        path = svc_path(s)
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Frequently asked questions</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([(r["name"], svc_path(r)) for r in rel], "Service")}
</article>
{aside(call_box(), list_box("All services", items, path), list_box("Cities we serve", locs + [("All Michigan cities", LOC_BASE)]))}</div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"],
                  "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Michigan"}, "url": DOMAIN + path,
                  "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(
        f'<a class="scard rv" href="{svc_path(s)}"><span class="sc-img">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:640px) 100vw, (max-width:1100px) 50vw, 33vw", alt="")}</span>'
        f'<span class="sc-body"><span class="bc-ic">{ic(SVC_ICON[s["slug"]], "ic", 20)}</span><h2>{e(s["name"])}</h2><p>{e(s["short"])}</p><span class="more">Learn more {ic("arrow")}</span></span></a>'
        for s in SERVICES)
    est = SVC_BY["insurance-estimate-second-opinion"]
    body = page_hero(trail, "What we do", "Insurance Appraisal Services in Michigan",
                     f"From a single estimate second opinion to full panel representation and neutral umpire work, every {BRAND} service is built around an accurate, defensible valuation of your loss.", "meeting-table") + f"""
<section class="sec"><div class="wrap"><div class="scards" data-stagger>{cards}</div></div></section>
<section class="sec sec-ice"><div class="wrap split split-top"><div class="rv"><p class="eyebrow">Not sure where to start?</p><h2>Most files begin with a second opinion</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A second opinion answers that quickly, and many disputes close right there with a documented supplement.</p><a class="btn btn-blue" href="{svc_path(est)}">About estimate second opinions {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one part of the process?", "Yes. Many clients start with an estimate second opinion and decide later whether to demand appraisal."), ("Do you handle condo associations and businesses?", "Yes: offices, retail, industrial buildings, churches, apartment owners, condo associations and HOAs, as well as one- to four-family homes."), ("Which Michigan losses do you see most?", "Hail and wind on roofs, basement water and sewer backups, ice dams and frozen pipes, fallen trees after ice storms, and fire and smoke.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)]
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Michigan | 12 Services",
                             "Insurance appraisal services in Michigan: appraisal demands, estimate second opinions, hail, ice dam, sewer backup, fire claims and umpires.",
                             body, schema, preload="meeting-table"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        svc_links = "".join(f'<li><a href="{svc_path(s)}">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f'Insurance Appraiser in {l["city"]}, Michigan', e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="local"><div><p class="local-k">Neighborhoods &amp; areas</p><p>{e(l["neighborhoods"])}</p></div><div><p class="local-k">Housing mix</p><p>{e(l["housing"])}</p></div><div><p class="local-k">Common claim drivers</p><ul class="chips">{chips}</ul></div></div>
{l["body"]}
<h2>Services available in {e(l["city"])}</h2>
<p>Every {BRAND} service is available to owners in {e(l["city"])} and surrounding communities, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])} property owners</h2>{faq_block(l["faqs"])}
<h2>Nearby cities</h2>{related([(LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]], "Nearby")}
</article>
{aside(call_box(), list_box("Michigan cities", items, path), list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>
{cta_band(f"Disputed claim in {l['city']}?", "Send the estimate and a few photos. We’ll tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, MI", "serviceType": "Insurance appraisal",
                  "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Michigan"}},
                  "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, l["title"], l["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Cities", LOC_BASE)]
    cities = "".join(
        f'<a class="city rv" href="{loc_path(l)}">{img(LOC_PHOTO[l["slug"]], "city-img", sizes="(max-width:640px) 50vw, (max-width:1100px) 33vw, 25vw", alt="")}'
        f'<span class="city-b"><h2 class="city-h">{e(l["city"])}</h2><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    regs = "".join(
        f'<div class="scard rv"><span class="sc-img">{img(ph, sizes="(max-width:640px) 100vw, 33vw", alt="")}</span><span class="sc-body"><p class="eyebrow">{e(sub)}</p><h3>{e(n)}</h3><p>{e(t)}</p></span></div>'
        for k, n, sub, _c, t, ph, _x in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal Across Michigan’s 83 Counties",
                     f"{BRAND} works in every Michigan county, from Monroe and Detroit to Ironwood and Copper Harbor. These local pages cover the cities our files come from most often.", "mackinac-bridge") + f"""
<section class="sec"><div class="wrap"><div class="cities" data-stagger>{cities}</div></div></section>
<section class="sec sec-ice"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">Regions</p><h2>How claims change from region to region</h2><p>Michigan’s 83 counties span two peninsulas joined by the Mackinac Bridge. Snow belts, river valleys and dense older suburbs each shape the claims we see.</p></div><div class="scards" data-stagger>{regs}</div></div></section>
{cta_band("Don’t see your city?", "We cover all 83 counties. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Insurance Appraisal in All 83 Michigan Counties",
                             "Insurance appraisal in all 83 Michigan counties, including Detroit, Grand Rapids, Lansing, Ann Arbor, Flint, Kalamazoo and Marquette.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(f'{l["city"]}, MI', loc_path(l)) for l in LOCATIONS])], preload="mackinac-bridge"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], tool_path(t)) for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = tool_path(t)
        trail = [("Home", "/"), ("Calculators", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()}", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec sec-tool"><div class="wrap"><div class="rv">{t["markup"].replace("{u}", "t")}</div>
<p class="hint tool-disc">For planning only. Results depend on the figures you enter and your policy’s terms. They are not a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2>{related([(o["name"], tool_path(o)) for o in others], "Tool")}</article>
{aside(call_box(), list_box("All calculators", items, path))}</div>
{cta_band("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"],
                  "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
                  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, preload=ph), 0.8)

    trail = [("Home", "/"), ("Calculators", TOOL_BASE)]
    tiles = "".join(
        f'<a class="scard rv" href="{tool_path(t)}"><span class="sc-img">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:640px) 100vw, 33vw", alt="")}<span class="tc-kind">{e(t["kind"])}</span></span>'
        f'<span class="sc-body"><h2>{e(t["name"])}</h2><p>{e(t["short"])}</p><span class="more">Open the tool {ic("arrow")}</span></span></a>' for t in TOOLS)
    T = {t["slug"]: tool_path(t) for t in TOOLS}
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Michigan",
                     "Seven calculators and planners built from real appraisal work. Use them to understand your claim and test the carrier’s math. No sign-up, and nothing is stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="scards" data-stagger>{tiles}</div></div></section>
<section class="sec sec-ice"><div class="wrap split split-top"><div class="rv"><p class="eyebrow">Suggested order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Start with the <a href="{T['claim-deadline-planner']}">claim deadline planner</a> so no date slips.</li><li>Check roof math, including eave ice barrier, with the <a href="{T['roof-squares-pitch-calculator']}">roof squares and pitch calculator</a>.</li><li>Had water come through a ceiling in winter? Try the <a href="{T['ice-dam-risk-cost-estimator']}">ice dam risk and cost estimator</a>.</li><li>See what you’ll actually receive with the <a href="{T['percentage-deductible-calculator']}">percentage deductible</a> and <a href="{T['rcv-acv-holdback-calculator']}">holdback</a> calculators.</li><li>Test the dispute with the <a href="{T['claim-gap-fee-estimator']}">claim gap and fee estimator</a>.</li><li>Finish with the <a href="{T['appraisal-readiness-score']}">appraisal readiness score</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Michigan",
                              "Free insurance claim calculators for Michigan owners: claim gap and fees, RCV vs ACV, roof squares, deductibles, ice dams and deadlines.",
                              body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist(items)], preload="calculator"), 0.9)


# ---------------------------------------------------------------- resources
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Michigan",
                     "Eight stages, from the first disagreement to a signed award: what happens, who does what, and where Michigan claims most often go wrong.", "meeting",
                     [("Stages", "8"), ("Panel", "2 appraisers + umpire"), ("Award", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works in Michigan", "description": "The eight stages of a property insurance appraisal under a Michigan policy.", "totalTime": "P10W",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t, "url": f"{DOMAIN}{path}"} for i, (n, t) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Michigan | 8 Steps",
                         "How insurance appraisal works in Michigan, in eight steps: the written demand, choosing appraisers, the umpire, the award and getting paid.",
                         body, [crumbs_schema(trail), howto], preload="meeting"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Appraisal FAQ", path)]
    toc = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Michigan Insurance Appraisal FAQ",
                     "Plain answers to the questions we hear most, grouped by topic: the basics, costs, timing, Michigan specifics and working with us.", "living-room") + f"""
<div class="wrap layout"><article class="prose"><nav class="toc" aria-label="FAQ topics">{toc}</nav>{groups}</article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>{cta_band("Didn’t see your question?", "Call or email. We’re happy to talk it through.")}"""
    write(path, document(path, "Michigan Insurance Appraisal FAQ | Costs & Timing",
                         "Michigan insurance appraisal FAQ, grouped by topic: how appraisal works, what it costs, deadlines, state rules and how we work with owners.",
                         body, [crumbs_schema(trail), faq_schema(allq)], preload="living-room"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Claim glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="g-row"><dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Insurance Claim Terms Glossary for Michigan",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English. Type in the box to filter.", "paperwork", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “holdback”, “umpire” or “ice dam”" autocomplete="off"><p class="hint" data-gloss-count>{len(GLOSSARY)} terms</p></div><div class="az">{az}</div><dl class="glossary">{dl}</dl><p class="gloss-none" hidden>No terms match that search.</p></article>
{aside(call_box(), list_box("Resources", LEARN, path))}</div>"""
    dts = {"@type": "DefinedTermSet", "name": "Michigan property insurance claim glossary",
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path + "#definedtermset"} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Claim Terms Glossary | ACV, RCV & More",
                         "Searchable insurance claim terms glossary for Michigan owners: ACV, RCV, holdback, umpire, ice dam, sewer backup, DIFS and more, defined.",
                         body, [crumbs_schema(trail), dts], preload="paperwork"), 0.7)

    for idx, p in enumerate(POSTS):
        path = post_path(p)
        trail = [("Home", "/"), ("Guides", POST_BASE), (p["title"], path)]
        others = [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{related([(o["title"], post_path(o)) for o in others], "Guide")}</article>
{aside(call_box(), list_box("Resources", LEARN), list_box("Free calculators", [(t["name"], tool_path(t)) for t in TOOLS[:4]]))}</div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"],
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US",
               "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path, "keywords": p["kw"]}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", preload=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Guides", path)]
    cards = "".join(
        f'<article class="gcard rv"><a class="gc-img" href="{post_path(p)}" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:760px) 100vw, 33vw", alt="")}</a>'
        f'<div class="gc-body"><p class="meta">{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</p><h2 class="gc-h"><a href="{post_path(p)}">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p></div></article>'
        for p in POSTS)
    body = page_hero(trail, "Claim guides", "Great Lakes Claim Guides for Michigan Owners",
                     "Practical guides on Michigan’s appraisal clause, ice dams, basement backups, reading estimates and choosing the right help.", "flood-street", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="gcards" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Michigan Property Claim Guides | Great Lakes Guides",
                         "Michigan property claim guides: the appraisal clause, ice dam claims, basement backup gaps, Xactimate estimates and when to demand appraisal.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, itemlist([(p["title"], post_path(p)) for p in POSTS])], preload="flood-street"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About us", f"About {BRAND}",
                     "We are estimators and appraisers who believe a property claim should be paid on what the damage really costs, documented clearly enough that everyone at the table can see it.", "roofers") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("suburban-home", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why we focus on the amount of loss</h2>
<p>Plenty of claim professionals do a little of everything. {BRAND} works on one question, how much a covered loss costs to repair, and builds its process, tools and reporting around answering it well. That focus lets us serve as your named appraiser, give a second opinion on an estimate before a dispute escalates, or sit as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we look at anyone else’s numbers.</li>
<li><strong>Defensible, not inflated.</strong> An inflated estimate burns credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reports.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we’ll say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work begins.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, condo associations and HOAs, property managers, business owners, churches, contractors, public adjusters and attorneys across Michigan. On any claim we serve in one role only, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside appraisal. We don’t guarantee outcomes; no honest appraiser can.</p>
<h2>Built around Michigan’s claims</h2>
<p>Michigan’s weather and housing produce a distinctive mix of losses: ice dams on story-and-a-half bungalows, sewer backups in finished basements, hail on suburban roofs, snow load on Upper Peninsula camps, and trees through roofs after ice storms. Working statewide means we price each with local knowledge, within the framework overseen by the Michigan Department of Insurance and Financial Services.</p>
</article>{aside(call_box(), list_box("Explore", [("Our services", SVC_BASE), ("Michigan cities", LOC_BASE), ("Free calculators", TOOL_BASE), ("Appraisal process", PROCESS)]))}</div>{cta_band()}"""
    write(path, document(path, f"About {BRAND} | How We Work",
                         "About Michigan Insurance Appraiser: an independent appraisal and estimating practice focused on the amount of loss on disputed claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], preload="roofers"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", f"Contact {BRAND}",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "handshake", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv"><p class="eyebrow">Direct lines</p><h2>Reach us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 83 Michigan counties</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>{ic("check")}<span>Your declarations page</span></li><li>{ic("check")}<span>The carrier’s full estimate (PDF)</span></li><li>{ic("check")}<span>Letters or emails from the carrier</span></li><li>{ic("check")}<span>Photos and any contractor estimate</span></li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path, uid="cf")}</div></div></section>"""
    write(path, document(path, f"Contact {BRAND} | {PHONE}",
                         "Contact Michigan Insurance Appraiser for a free review of a disputed property claim. Call or text (844) 537-1427, or send details online.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], preload="handshake"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Policy", f"Privacy Policy | {BRAND}",
                  "Privacy policy for Michigan Insurance Appraiser: what we collect through forms and calls, how we use it, and the choices you have about it.",
                  "How we collect, use and protect the information you share with us.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share, such as your name, phone, email, property location and claim details. Our server also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and evaluate your claim.</li><li>To provide services you request.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim calculators</h2><p>Our calculators run in your browser. The numbers you enter aren’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add site analytics, this policy will be updated to describe it.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>Ask us to access, correct or delete the information you gave us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", f"Terms of Use | {BRAND}",
                "Terms of use for the Michigan Insurance Appraiser website, its free claim calculators and content, including reliance limits and governing law.",
                "The terms that apply when you use this website and its tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Use of this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Michigan.</p>
<h2>No professional relationship</h2><p>Reading this site, using its tools or submitting a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm. Nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a licensed Michigan attorney for legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the figures you enter. They aren’t appraisals, quotes or predictions of any outcome.</p>
<h2>Intellectual property</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made from its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Michigan.</p>"""),
        DISCLAIM: ("Disclaimer", f"Disclaimer | {BRAND}",
                   "Disclaimer for Michigan Insurance Appraiser: general information only, not legal advice, illustrative figures and no guaranteed results.",
                   "Important limits on the information published on this website.", f"""
<h2>General information only</h2><p>This website is educational. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>No guarantee of results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies and Michigan law contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes them. If a deadline is near, consult a Michigan attorney promptly.</p>
<h2>Legal references</h2><p>References to the Michigan Insurance Code, its appraisal and suit-limitation provisions, the Uniform Trade Practices Act or penalty interest are general descriptions for context, not legal analysis. Verify current law and programs with official sources such as the Michigan Department of Insurance and Financial Services.</p>
<h2>Photographs</h2><p>Photos are public-domain or CC0 images used for illustration. They don’t show our clients’ properties.</p>"""),
    }
    for path, (h1, title, desc, lede, content) in legal.items():
        trail = [("Home", "/"), (h1, path)]
        body = page_hero(trail, "Legal", h1, lede, "office-tower", cta=False) + f'<div class="wrap layout"><article class="prose prose-narrow">{content}</article>{aside(call_box())}</div>'
        write(path, document(path, title, desc, body, [crumbs_schema(trail)], preload="office-tower"), 0.3)


def sitemap_pages():
    path = SITEMAP
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], svc_path(s)) for s in SERVICES]),
        ("Cities", [("All cities", LOC_BASE)] + [(f'{l["city"]}, MI', loc_path(l)) for l in LOCATIONS]),
        ("Calculators", [("All calculators", TOOL_BASE)] + [(t["name"], tool_path(t)) for t in TOOLS]),
        ("Resources", LEARN + [(p["title"], post_path(p)) for p in POSTS]),
        ("Legal", [("Privacy policy", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCLAIM)]),
    ]
    cols = "".join(f'<div class="smap-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map", f"Every page on {BRAND}, grouped by section.", "office-tower", cta=False) + f'<section class="sec"><div class="wrap smap" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Map | {BRAND}",
                         "HTML site map for Michigan Insurance Appraiser: every service, city page, free claim calculator, guide and legal page in one list.",
                         body, [crumbs_schema(trail)], preload="office-tower"), 0.3)

    body = (f'<section class="ph ph-404"><div class="ph-media">{img("storm-sky", "ph-img", lazy=False, alt="")}</div><div class="wrap ph-in">'
            f'<p class="eyebrow eyebrow-light">Error 404</p><h1>That page blew away with the last lake-effect squall</h1>'
            f'<p class="ph-lede">The page you’re looking for may have moved. Try one of these instead.</p>'
            f'<div class="btn-row"><a class="btn btn-maize" href="/">Home</a><a class="btn btn-glass" href="{SVC_BASE}">Services</a><a class="btn btn-glass" href="{TOOL_BASE}">Free calculators</a><a class="btn btn-glass" href="{CONTACT}">Contact</a></div></div></section>')
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}",
                                "This Michigan Insurance Appraiser page could not be found. Use the links to reach our services, free claim calculators or contact page.",
                                body, robots="noindex,follow"), sitemap=False)


# ---------------------------------------------------------------- root files
GUARD_PHP = r"""<?php
// Michigan Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'michiganinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://michiganinsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$mia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($mia_uri, '?'), $mia_m)) {
    $mia_q = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
    header('Location: ' . $mia_m[1] . $mia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Michigan Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (a directory's index.php included)
// and routes "/" and unknown paths here.
require_once __DIR__ . '/_guard.php';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
if ($path === '/' || $path === '/index.php') {
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
    # Search Console verification: exact bytes, single line, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


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
