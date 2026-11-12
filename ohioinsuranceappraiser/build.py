#!/usr/bin/env python3
"""Static site generator for ohioinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
Standard library only. Pages are written as dir/index.php behind the canonical-host guard (see README).
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
from learn import PROCESS_STEPS, PROCESS_BODY, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Ohio Insurance Appraiser"
HOST = "ohioinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112b"
FAV = "1"
# Google Tag Manager container, e.g. "GTM-XXXXXXX". Empty = no tag is output.
GTM_ID = ""

SVC_BASE = "/appraisal-practice/"
LOC_BASE = "/service-cities/"
TOOL_BASE = "/appraisal-workbench/"
POST_BASE = "/appraisal-briefings/"
P_ABOUT, P_CONTACT = "/meet-the-firm/", "/contact-our-team/"
P_PROCESS, P_FAQ, P_GLOSS = "/appraisal-timeline/", "/appraisal-q-and-a/", "/appraisal-lexicon/"
P_PRIV, P_TERMS, P_DISC, P_CRED, P_MAP = "/privacy-commitment/", "/usage-terms/", "/disclaimer-notice/", "/photo-sources/", "/site-guide/"

e = html.escape
pages = []  # (path, priority) for sitemap


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}-ohio/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
# Each wanted key falls back to the next available photo, so a missing download never breaks the build.
FALLBACK = {
    "hero-home": ["house-porch", "winter-house"], "house-porch": ["hero-home"], "winter-house": ["icicles-roof", "hero-home"],
    "icicles-roof": ["winter-house", "ice-storm"], "ice-storm": ["icicles-roof", "winter-house"],
    "storm-supercell": ["storm-clouds", "lightning"], "storm-clouds": ["storm-supercell", "lightning"], "lightning": ["storm-clouds"],
    "hailstones": ["roof-shingles", "storm-clouds"], "tornado-damage": ["tornado-aerial", "wind-roof-damage"], "tornado-aerial": ["tornado-damage"],
    "wind-roof-damage": ["tornado-damage", "roof-shingles"], "fallen-tree": ["wind-roof-damage", "tornado-damage"],
    "flooded-basement": ["water-ceiling"], "water-ceiling": ["flooded-basement", "kitchen"], "house-fire": ["fire-aftermath"],
    "fire-aftermath": ["house-fire"], "roof-shingles": ["slate-roof", "roofer"], "roofer": ["roof-shingles"], "slate-roof": ["roof-shingles"],
    "metal-roof": ["commercial-building", "roof-shingles"], "commercial-building": ["apartment-building", "metal-roof"],
    "apartment-building": ["commercial-building"], "consultation": ["paperwork"], "paperwork": ["consultation", "calculator"],
    "calculator": ["paperwork"], "clipboard": ["paperwork", "roofer"], "kitchen": ["living-room"], "living-room": ["kitchen"],
    "columbus-skyline": ["storm-clouds"], "cleveland-skyline": ["lake-erie", "storm-clouds"], "cincinnati-skyline": ["storm-clouds"],
    "toledo": ["lake-erie", "ohio-farm"], "dayton": ["tornado-damage"], "lake-erie": ["cleveland-skyline"], "ohio-farm": ["storm-supercell"],
    "akron": ["house-porch"], "zanesville": ["ohio-farm"],
}


def P(key):
    seen, todo = set(), [key]
    while todo:
        k = todo.pop(0)
        if k in PHOTOS:
            return k
        if k in seen:
            continue
        seen.add(k)
        todo += FALLBACK.get(k, [])
    return next(iter(PHOTOS))


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    key = P(key)
    p = PHOTOS[key]
    a = e(alt if alt is not None else p["alt"])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-demand-representation": "consultation", "home-insurance-appraisal": "house-porch", "commercial-hoa-appraisal": "commercial-building",
    "hail-roof-appraisal": "hailstones", "tornado-windstorm-appraisal": "tornado-damage", "derecho-remnant-storm-appraisal": "fallen-tree",
    "water-damage-appraisal": "water-ceiling", "fire-smoke-appraisal": "house-fire", "ice-dam-frozen-pipe-appraisal": "icicles-roof",
    "estimate-audit": "paperwork", "neutral-umpire-services": "clipboard",
}
LOC_PHOTO = {
    "columbus": "columbus-skyline", "cleveland": "cleveland-skyline", "cincinnati": "cincinnati-skyline", "toledo": "toledo",
    "akron": "akron", "dayton": "tornado-damage", "canton": "house-porch", "youngstown": "storm-clouds", "sandusky": "lake-erie",
    "lima": "ohio-farm", "xenia": "tornado-aerial", "zanesville": "ice-storm",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator", "rcv-acv-holdback-calculator": "paperwork", "roof-area-pitch-calculator": "roofer",
    "percentage-deductible-calculator": "storm-supercell", "claim-calendar-builder": "clipboard", "appraisal-readiness-checkup": "consultation",
    "basement-backup-sublimit-calculator": "water-ceiling",
}
POST_PHOTOS = ["paperwork", "flooded-basement", "slate-roof", "icicles-roof", "calculator", "fallen-tree"]
POST_PHOTO = {p["slug"]: POST_PHOTOS[i % len(POST_PHOTOS)] for i, p in enumerate(POSTS)}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 6h2M13 6h2M9 10h2M13 10h2M9 14h2M13 14h2M10 22v-4h4v4"/>',
    "hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M8 19v1M8 14v1M16 19v1M16 14v1M12 21v1M12 16v1"/>',
    "wind": '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "storm": '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3a8 8 0 1 0-11.7 9"/><path d="M13 11l-4 6h6l-4 6"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.4.4 1.4 1.4 2.4 2.5 2.4z"/>',
    "snow": '<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1L19.1 4.9M9 3.5l3 2 3-2M9 20.5l3-2 3 2M3.5 9l2 3-2 3M20.5 9l-2 3 2 3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "doc": '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "list": '<path d="M9 6h12M9 12h12M9 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    "gauge": '<path d="M12 14l4-4"/><path d="M3.3 19a10 10 0 1 1 17.4 0"/>',
}


def ic(name, cls="ico"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I.get(name, _I["doc"])}</svg>'


TOOL_ICON = {"gap": "scale", "acv": "percent", "roof": "ruler", "pct": "percent", "cal": "calendar", "chk": "gauge", "drop": "drop"}


def mark(size=44):
    # Crimson tile, white inspection lens with a roof line inside, teal handle.
    return (f'<svg class="mark" width="{size}" height="{size}" viewBox="0 0 48 48" aria-hidden="true">'
            '<rect width="48" height="48" rx="12" fill="#C12637"/>'
            '<circle cx="21" cy="20.5" r="10.5" fill="none" stroke="#fff" stroke-width="3.6"/>'
            '<path d="M15.2 22.6l5.8-5 5.8 5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M29 28.6l8 8" stroke="#7FD8CF" stroke-width="5" stroke-linecap="round"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND} home">{mark()}<span class="brand-t"><b>Ohio Insurance</b><b class="b2">Appraiser</b></span></a>'


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "ProfessionalService",
        "@id": DOMAIN + "/#business",
        "name": BRAND,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "email": EMAIL,
        "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/favicon-512.png", "contentUrl": DOMAIN + "/favicon-512.png", "width": 512, "height": 512, "caption": BRAND},
        "image": {"@id": DOMAIN + "/#logo"},
        "address": {"@type": "PostalAddress", "addressRegion": "OH", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-OH", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate audits and umpire services for disputed property claims across Ohio’s 88 counties.",
        "areaServed": [{"@type": "State", "name": "Ohio"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Umpire", "Hail damage", "Wind and tornado damage", "Ice dams", "Sewer backup", "Xactimate estimating"],
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


def item_list(items):
    return {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Cities", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Ohio cities served", LOC_BASE), True),
        ("Workbench", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Resources", [("Appraisal timeline", P_PROCESS), ("Q&amp;A", P_FAQ), ("Appraisal lexicon", P_GLOSS), ("Briefings", POST_BASE)], None, False),
    ]


def header():
    nav = ""
    for name, links, allk, wide in _groups():
        li = "".join(f'<li><a href="{p}">{n if "&amp;" in n else e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        nav += f'<li class="has-drop"><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" wide" if wide else ""}">{li}</ul></li>'
    nav += f'<li><a class="nl" href="{P_ABOUT}">About</a></li><li><a class="nl" href="{P_CONTACT}">Contact</a></li>'
    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{n if "&amp;" in n else e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc" aria-expanded="false" aria-controls="dp-{i}">{name}{ic("chev", "chev")}</button><div class="acc-p" id="dp-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a class="dl" href="{P_ABOUT}">About the firm</a></li><li><a class="dl" href="{P_CONTACT}">Contact</a></li>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap head-in">
{brand()}
<nav class="nav" aria-label="Main"><ul>{nav}</ul></nav>
<a class="btn btn-red head-call" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-veil" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-d")}<button class="drawer-x" type="button" aria-label="Close menu" data-close><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="dl" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-line" href="{P_CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 88 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS)
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="site-foot">
<div class="foot-band"><div class="wrap foot-band-in"><p class="foot-big">Covered isn’t the same as paid. <span>Let’s check the math.</span></p><div class="btn-row"><a class="btn btn-white" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap foot-grid">
<div class="foot-about">{brand("brand brand-f")}
<p>Independent appraisal, estimate audits and umpire work for property owners whose insurance claim came in short — Lake Erie to the Ohio River.</p>
<ul class="foot-contact"><li>{ic("phone")}<a href="tel:{TEL}">{PHONE_INTL}</a></li><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("clock")}<span>Mon–Fri 8am–6pm ET</span></li></ul></div>
<div><h2 class="foot-h">Services</h2><ul>{svc}<li><a href="{SVC_BASE}">Every service →</a></li></ul></div>
<div><h2 class="foot-h">Ohio cities</h2><ul class="two">{loc}</ul></div>
<div><h2 class="foot-h">Workbench</h2><ul>{tl}</ul></div>
<div><h2 class="foot-h">Firm</h2><ul><li><a href="{P_ABOUT}">About the firm</a></li><li><a href="{P_PROCESS}">Appraisal timeline</a></li><li><a href="{P_FAQ}">Q&amp;A</a></li><li><a href="{P_GLOSS}">Lexicon</a></li><li><a href="{POST_BASE}">Briefings</a></li><li><a href="{P_CONTACT}">Contact</a></li></ul></div>
</div>
<div class="wrap foot-legal"><p>© <span data-year>{date.today().year}</span> {BRAND}. {BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, don’t give legal advice and don’t act as public adjusters. Content is general information; your policy controls. Results are never guaranteed.</p>
<ul><li><a href="{P_PRIV}">Privacy</a></li><li><a href="{P_TERMS}">Terms</a></li><li><a href="{P_DISC}">Disclaimer</a></li><li><a href="{P_CRED}">Photo sources</a></li><li><a href="{P_MAP}">Site guide</a></li></ul></div>
</footer>
<button class="top-btn" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="call-bar"><a href="tel:{TEL}">{ic("phone")} Call</a><a href="{P_CONTACT}">{ic("mail")} Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return (f"<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':\nnew Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],\n"
            f"j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\nheight="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo=None, home=False):
    canonical = DOMAIN + path
    page_type, extra, crumb_id = "WebPage", [], None
    for n in (schema or []):
        t = n.get("@type")
        if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage"):
            page_type = t
            continue
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        extra.append(n)
    key = P(photo or "hero-home")
    pimg = PHOTOS[key]
    webpage = {
        "@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{key}.webp", "width": pimg["fw"], "height": pimg["fh"], "caption": pimg["alt"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main = [n["@id"] for n in extra if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList", "FAQPage")]
    pref = [n["@id"] for n in extra if n.get("@type") in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")]
    webpage["mainEntity"] = {"@id": (pref or main or [DOMAIN + "/#business"])[0]}
    graph = [org_schema(), site_schema()] + ([] if robots.startswith("noindex") else [webpage]) + extra
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = f'<link rel="preload" as="image" href="/assets/img/photos/{key}.webp" imagesrcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {pimg["fw"]}w" imagesizes="100vw">\n'
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{BRAND} — independent property claim appraisal across Ohio">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND} — independent property claim appraisal across Ohio">
<meta name="geo.region" content="US-OH">
<meta name="geo.placename" content="Ohio">
<meta name="theme-color" content="#C12637">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Red+Hat+Display:wght@600;700;800;900&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{"is-home" if home else "is-inner"}">
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
    # The host serves real files without running the front controller, so every directory page is
    # dir/index.php starting with the canonical-host guard. Never write dir/index.html.
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
    if rel.endswith("/index.php"):
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
    parts = [(e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>') for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(f"<li>{x}</li>" for x in parts) + "</ol></nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="hero-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-bg">{img(photo, lazy=False, alt="", extra=' data-parallax="0.08"')}</div><div class="wrap phero-in">{crumbs(trail)}<p class="tag">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="faq-a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="side-box side-call"><h2 class="side-h">Talk it through first</h2><p>The first conversation is free. We’ll tell you plainly whether appraisal fits your claim.</p><a class="side-tel" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-white" href="{P_CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}{ic("right", "ar")}</a></li>' for n, p in items)
    return f'<div class="side-box"><h2 class="side-h">{e(title)}</h2><ul class="side-list">{li}</ul></div>'


def cta_strip(h="Not sure your settlement adds up?", p="Send us the insurer’s estimate. We’ll go through it and tell you what we see — no obligation."):
    return f"""<section class="cta-strip"><div class="wrap cta-in reveal"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-white" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Email the estimate</a></div></div></section>"""


def layout(article, aside):
    return f'<div class="wrap two-col"><article class="prose">{article}</article><aside class="side">{aside}</aside></div>'


def related(items):
    return '<div class="rel-grid">' + "".join(f'<a class="rel" href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow", "ar")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Hail", "Wind / tornado", "Derecho / remnant storm", "Ice dam / frozen pipe", "Water / sewer backup", "Fire / smoke", "Fallen tree", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hid="f"):
    roles = ["Homeowner", "Condo owner", "Landlord", "Business owner", "HOA / property manager", "Contractor", "Attorney", "Other"]
    cities = [l["city"] for l in LOCATIONS] + ["Elsewhere in Ohio"]
    return f"""<form class="lead" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="lead-h">{e(heading)}</h2><p class="lead-sub">Free review · no obligation · reply within one business day</p>
<div class="fgrid">
<div><label for="{hid}-name">Full name *</label><input id="{hid}-name" name="name" autocomplete="name" required></div>
<div><label for="{hid}-phone">Phone *</label><input id="{hid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="{hid}-email">Email *</label><input id="{hid}-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="{hid}-role">I am a…</label><select id="{hid}-role" name="role">{_opt(roles)}</select></div>
<div><label for="{hid}-loss">Type of loss</label><select id="{hid}-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="{hid}-city">Property location</label><select id="{hid}-city" name="city">{_opt(cities)}</select></div>
<div><label for="{hid}-amt">Rough amount in dispute</label><select id="{hid}-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="{hid}-car">Insurance company (optional)</label><input id="{hid}-car" name="carrier"></div>
<div class="full"><label for="{hid}-det">Where does the claim stand?</label><textarea id="{hid}-det" name="details" rows="4" placeholder="Date of loss, what the insurer has paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="{hid}-web">Website</label><input id="{hid}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="{P_PRIV}">privacy commitment</a>.</span></label></div>
<div class="full"><button class="btn btn-red btn-block" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


def hero_form():
    return f"""<form class="lead lead-hero" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="lead-h">Get a free claim review</h2><p class="lead-sub">Two minutes. A real person calls back.</p>
<div class="fgrid">
<div class="full"><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="full"><label for="h-email">Email</label><input id="h-email" name="email" type="email" autocomplete="email"></div>
<div class="full hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>Contact me about my claim. <a href="{P_PRIV}">Privacy</a>.</span></label></div>
<div class="full"><button class="btn btn-red btn-block" type="submit">Request my review {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status" aria-live="polite"></div>
</form>"""


# ---------------------------------------------------------------- home
REGIONS = [
    ("Northeast Ohio", "Cleveland · Akron · Canton · Youngstown", "lake-erie",
     "Lake-effect snow piles up in the snowbelt east of Cleveland, which means ice dams, snow-load damage and burst pipes in century-old homes. Spring and summer bring hail and straight-line wind across Summit, Stark and Mahoning counties.",
     ["Lake-effect snow", "Ice dams", "Hail", "Old slate roofs"]),
    ("Northwest Ohio", "Toledo · Sandusky · Lima", "ohio-farm",
     "Flat farmland gives storms a clear run. Tornadoes, derecho winds and hail cross Lucas, Wood, Erie and Allen counties, while Lake Erie adds wind-driven rain and lakeshore exposure.",
     ["Tornadoes", "Straight-line wind", "Hail", "Farm buildings"]),
    ("Central Ohio", "Columbus and suburbs", "columbus-skyline",
     "Franklin County’s fast-growing suburbs mean big subdivisions of similar homes — and big hail and wind events that hit thousands of roofs at once, as the 2012 derecho showed.",
     ["Derechos", "Hail", "Wind", "Basement water"]),
    ("Southwest Ohio", "Cincinnati · Dayton · Xenia", "cincinnati-skyline",
     "The Miami Valley sits in one of Ohio’s busiest tornado corridors, from Xenia in 1974 to the Memorial Day 2019 outbreak. Cincinnati’s hillside homes add tree, wind and water problems.",
     ["Tornadoes", "Hail", "Hillside water", "Tree damage"]),
    ("Southeast Ohio", "Zanesville · Athens · Marietta", "ice-storm",
     "Appalachian hills, river towns and older frame and brick homes. Ice storms, fallen trees and basement water are the claims that come up most along the Muskingum and the Ohio River.",
     ["Ice storms", "Fallen trees", "River-town basements", "Older homes"]),
]

STORMS = [
    ("1913", "The Great Flood", "Rivers across the state overtopped their banks in March 1913, devastating Dayton and swamping Columbus and Zanesville. Flood is still excluded from homeowners policies today."),
    ("1924", "Lorain–Sandusky tornado", "The deadliest tornado in Ohio history tore through Sandusky and Lorain on June 28, 1924."),
    ("1974", "Xenia", "An F5 tornado in the April 3, 1974 Super Outbreak cut through Xenia, one of the most destructive tornadoes the state has recorded."),
    ("1978", "The Great Blizzard", "January 1978 brought hurricane-force winds and drifting snow statewide — the benchmark for Ohio winter storms."),
    ("2008", "Ike’s remnants", "On September 14, 2008, the remains of Hurricane Ike crossed Ohio with hurricane-force gusts, leaving roughly two million customers without power and roofs damaged statewide."),
    ("2012", "The derecho", "On June 29, 2012, a derecho swept Columbus and central and southern Ohio, knocking out power to about a million customers."),
    ("2019", "Memorial Day outbreak", "Tornadoes, including an EF4, hit Trotwood, Harrison Township, Brookville and Beavercreek around Dayton."),
]


def home():
    svc_cards = "".join(
        f'<a class="card reveal" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1080px) 50vw, 380px", alt="")}<span class="card-ic">{ic(s.get("icon", "doc"))}</span></span><span class="card-b"><h3>{e(s["name"])}</h3><span class="card-p">{e(s["short"])}</span><span class="card-more">Learn more {ic("arrow", "ar")}</span></span></a>'
        for s in SERVICES[:9])
    regions = "".join(
        f'<article class="region"><div class="region-ph">{img(ph, sizes="(max-width:700px) 86vw, 420px", alt="")}</div><div class="region-b"><p class="region-k">{e(sub)}</p><h3>{e(n)}</h3><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul></div></article>'
        for n, sub, ph, t, chips in REGIONS)
    steps = [
        ("Free claim review", "We read the policy, the insurer’s estimate and your photos, then tell you whether appraisal is the right tool."),
        ("Independent scope", "Our own inspection, measurements and a line-item estimate priced for your part of Ohio."),
        ("Written demand", "Appraisal is demanded in writing and we’re named as your appraiser inside the policy’s window."),
        ("Panel work", "Line-by-line work with the insurer’s appraiser. Most of the gap usually closes here."),
        ("Signed award", "Anything left goes to the umpire. Two signatures set the amount of loss."),
    ]
    stepper = "".join(f'<li class="reveal"><span class="st-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(steps))
    tool_list = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/"><span class="tl-ph">{img(TOOL_PHOTO[t["slug"]], sizes="96px", alt="")}</span><span class="tl-b"><b>{e(t["name"])}</b><small>{e(t["short"])}</small></span>{ic("arrow", "ar")}</a></li>' for t in TOOLS)
    cities = "".join(f'<a class="city reveal" href="{loc_path(l)}">{img(LOC_PHOTO.get(l["slug"], "hero-home"), sizes="(max-width:700px) 50vw, 300px", alt="")}<span class="city-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    storms = "".join(f'<li class="reveal"><span class="yr">{y}</span><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for y, t, p in STORMS)
    posts = "".join(f'<a class="post reveal" href="{POST_BASE}{p["slug"]}/"><span class="post-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</span><span class="post-b"><small>{e(p["read"])} read</small><h3>{e(p["title"])}</h3><span class="card-p">{e(p["summary"])}</span></span></a>' for p in POSTS[:3])

    home_faqs = [
        ("What does an Ohio Insurance Appraiser do?", "We put an independent value on property damage when you and your insurer agree the loss is covered but disagree on what it costs. As your named appraiser we inspect, build a line-item estimate, work through it with the insurer’s appraiser and, if needed, present unresolved items to an umpire."),
        ("How is an appraiser different from a public adjuster?", "A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal clause on one question: the amount of loss. We don’t negotiate claims outside appraisal and we don’t give legal advice."),
        ("Is the appraisal award binding in Ohio?", "Under the standard appraisal clause, a written award signed by any two of the three panel members sets the amount of loss. It doesn’t decide coverage questions, so read your policy and get legal advice on anything beyond the dollar figure."),
        ("What does appraisal cost?", "Each side usually pays its own appraiser and half of the umpire. We give you our fee in writing before any work starts, and the first conversation is free."),
        ("How long does an Ohio appraisal take?", "Many finish within a few months of the demand, depending on how fast the panel forms, how big the loss is and whether an umpire is needed. Policy deadlines, including suit limitations, keep running, so keep an eye on the calendar."),
        ("Do you cover my county?", "Yes. We work in all 88 Ohio counties, with frequent work around Columbus, Cleveland, Cincinnati, Toledo, Akron, Dayton and the Mahoning Valley."),
    ]
    K = BRAND
    body = f"""
<section class="hero">
<div class="hero-bg">{img("hero-home", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="tag tag-light">Independent claim appraisal · All 88 counties</p>
<h1>{K}: a second, independent number for your property claim</h1>
<p class="lede">When the insurer accepts the claim but the check won’t cover the repair, {K} builds its own line-item valuation and takes it through the appraisal clause in your policy.</p>
<div class="btn-row"><a class="btn btn-red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-w" href="#services">See what we appraise {ic("arrow")}</a></div>
<ul class="hero-points"><li>{ic("check")}Your appointed appraiser</li><li>{ic("check")}Ohio pricing, ZIP by ZIP</li><li>{ic("check")}Homes, HOAs &amp; businesses</li></ul>
</div>
{hero_form()}
</div>
</section>

<section class="promise" aria-label="How we work"><div class="wrap promise-in" data-stagger>
<div class="reveal">{ic("search")}<div><b>Scope from scratch</b><span>We measure and photograph it ourselves.</span></div></div>
<div class="reveal">{ic("scale")}<div><b>Defensible numbers</b><span>Priced to hold up in front of an umpire.</span></div></div>
<div class="reveal">{ic("file")}<div><b>Fees in writing</b><span>Before any work starts.</span></div></div>
<div class="reveal">{ic("doc")}<div><b>Straight answers</b><span>If appraisal isn’t right, we say so.</span></div></div>
</div></section>

<section class="sec"><div class="wrap intro">
<div class="intro-copy reveal">
<p class="kicker">Why owners call us</p>
<h2>Covered isn’t the same as paid in full</h2>
<p>Most underpaid Ohio claims aren’t denied — they’re short. A slate roof priced as asphalt. A finished basement scoped as bare block. Ice-and-water barrier left off a snowbelt roof. {K} exists for that gap between “approved” and “enough to fix it.”</p>
<p>As an {K}, our job is narrow on purpose: work out what the loss really costs, write it up so every line can be checked, and see it through the appraisal clause if the insurer won’t move. We don’t sell roofs, we don’t take over your claim and we don’t practice law.</p>
<ul class="ticks"><li>{ic("check")}Independent inspection and measurements — never an edited copy of the insurer’s estimate.</li><li>{ic("check")}Line items priced for your part of Ohio, with code items and overhead and profit treated the way your policy reads.</li><li>{ic("check")}Honest triage: if a denial needs an attorney, you’ll hear it on the first call.</li></ul>
<a class="btn btn-dark" href="{P_ABOUT}">How the firm works {ic("arrow")}</a>
</div>
<figure class="intro-ph reveal">{img("roofer", sizes="(max-width:1080px) 100vw, 520px")}<figcaption><b>Inspected, measured, priced.</b> Every {K} estimate starts on site.</figcaption></figure>
</div></section>

<section class="sec sec-tint" id="services"><div class="wrap">
<div class="sec-head reveal"><p class="kicker">What we appraise</p><h2>Services from {K}</h2><p>Eleven services, one goal: a valuation of your loss that holds up. Start with an estimate audit or bring {K} in once appraisal has been demanded.</p></div>
<div class="cards" data-stagger>{svc_cards}</div>
<p class="center"><a class="btn btn-line" href="{SVC_BASE}">All eleven services {ic("arrow")}</a></p>
</div></section>

<section class="counters"><div class="wrap counters-in">
<div><b data-count="88">88</b><span>Ohio counties served</span></div>
<div><b data-count="5">5</b><span>Weather regions, five claim patterns</span></div>
<div><b data-count="11">11</b><span>Appraisal &amp; estimating services</span></div>
<div><b data-count="7">7</b><span>Free claim tools</span></div>
</div></section>

<section class="sec"><div class="wrap" data-carousel>
<div class="sec-head sec-head-row reveal"><div><p class="kicker">Lake Erie to the Ohio River</p><h2>Five Ohio regions, five kinds of claims</h2><p>Snowbelt ice dams in Ashtabula, hail in Franklin County, tornadoes in the Miami Valley, ice storms in the hills. An {K} has to know how each region’s weather shows up on a roof — and on an estimate.</p></div>
<div class="car-btns"><button type="button" class="car-btn" data-prev aria-label="Previous region">{ic("left")}</button><button type="button" class="car-btn" data-next aria-label="Next region">{ic("right")}</button></div></div>
<div class="car-track" tabindex="0" aria-label="Ohio regions">{regions}</div>
</div></section>

<section class="sec sec-dark"><div class="wrap">
<div class="sec-head reveal"><p class="kicker kicker-light">The process</p><h2>How {K} moves a stuck claim</h2><p>The appraisal clause turns an open-ended argument into a defined process with a binding result on the amount of loss.</p></div>
<ol class="stepper" data-stagger>{stepper}</ol>
<p class="center"><a class="btn btn-ghost-w" href="{P_PROCESS}">Read the full appraisal timeline {ic("arrow")}</a></p>
</div></section>

<section class="sec" id="workbench"><div class="wrap bench">
<div class="bench-l reveal"><p class="kicker">Free workbench</p><h2>Check your numbers with {K} tools</h2><p>Type in the two estimates you already have. A wide gap is worth a conversation with an {K}; a narrow one may close faster with a documented supplement.</p>{GAP_MINI}</div>
<div class="bench-r reveal"><h3 class="bench-h">All seven tools</h3><ul class="tool-list">{tool_list}</ul><p class="hint">Everything runs in your browser. Nothing is stored or sent.</p></div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head reveal"><p class="kicker">Statewide</p><h2>{K} service cities</h2><p>{K} works in every county. These are the places where we’re asked to look at claims most often.</p></div>
<div class="cities" data-stagger>{cities}</div>
<p class="center"><a class="btn btn-line" href="{LOC_BASE}">All Ohio service cities {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap storms-wrap">
<div class="storms-l reveal"><p class="kicker">Storm memory</p><h2>Ohio storms that shaped how claims are handled</h2><p>Ohio’s worst weather days still echo in policy language — percentage wind deductibles, flood exclusions and backup sublimits. An {K} reads every claim against that history.</p>{img("storm-supercell", "storms-ph", sizes="(max-width:1080px) 100vw, 440px")}</div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head reveal"><p class="kicker">Choosing help</p><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. {K} will point you elsewhere when appraisal isn’t the right tool.</p></div>
<div class="who" data-stagger>
<div class="who-c who-hl reveal"><h3>{K}</h3><p class="who-k">Values the amount of loss</p><ul><li>Best when coverage is accepted and the number is disputed</li><li>Result: an award signed by two of three</li><li>Doesn’t decide coverage</li></ul></div>
<div class="who-c reveal"><h3>Public adjuster</h3><p class="who-k">Handles and negotiates the claim</p><ul><li>Best early, from first notice</li><li>Result: a negotiated settlement</li><li>Licensed by the Ohio Department of Insurance</li></ul></div>
<div class="who-c reveal"><h3>Attorney</h3><p class="who-k">Legal disputes and lawsuits</p><ul><li>Best for denials, bad-faith questions and deadlines</li><li>Result: settlement or judgment</li><li>Argues coverage in court</li></ul></div>
</div></div></section>

<section class="sec"><div class="wrap faq-wrap">
<div class="faq-l reveal"><p class="kicker">Q&amp;A</p><h2>Questions people ask an {K}</h2><p>Short, straight answers about appraisal, costs and timing.</p><div class="btn-row"><a class="btn btn-dark" href="{P_FAQ}">Full Q&amp;A {ic("arrow")}</a><a class="btn btn-line" href="{P_GLOSS}">Appraisal lexicon</a></div></div>
<div class="reveal">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head reveal"><p class="kicker">Briefings</p><h2>Read this before you demand appraisal</h2><p>Practical guides from {K} on Ohio policy language, documentation and timing.</p></div>
<div class="posts" data-stagger>{posts}</div>
</div></section>

<section class="cta-photo"><div class="cta-photo-bg">{img("storm-clouds", alt="", extra=' data-parallax="0.16"')}</div><div class="wrap cta-photo-in reveal"><h2>Check the numbers before you sign off on them</h2><p>A short review now can keep you from accepting a settlement that won’t pay for the repair.</p><div class="btn-row"><a class="btn btn-red" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost-w" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact-grid">
<div class="contact-l reveal"><p class="kicker">Start with a conversation</p><h2>Talk to an {K} about your claim</h2><p>Tell us what happened and what the insurer offered. We’ll review it and tell you whether appraisal is worth pursuing — no pressure.</p>
<ul class="contact-lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 88 Ohio counties</b></div></li></ul></div>
<div class="reveal">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Ohio Insurance Appraiser: independent appraisal, estimate audits and umpire work for underpaid hail, wind, ice dam, water and fire claims in Ohio.",
                        body, [faq_schema(home_faqs)], photo="hero-home", home=True), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for i, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(i + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        art = s["body"] + f"""<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related services</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}"""
        aside = call_box() + list_box("All services", items, path) + list_box("Cities we serve", [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("Every Ohio city", LOC_BASE)])
        body = page_hero(trail, "Appraisal service", s["h1"], e(s["lede"]), ph, s["facts"]) + layout(art, aside) + cta_strip()
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["kw"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "State", "name": "Ohio"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{P(ph)}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(f'<a class="card reveal" href="{SVC_BASE}{s["slug"]}/"><span class="card-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, (max-width:1080px) 50vw, 380px", alt="")}<span class="card-ic">{ic(s.get("icon", "doc"))}</span></span><span class="card-b"><h2 class="card-h">{e(s["name"])}</h2><span class="card-p">{e(s["short"])}</span><span class="card-more">Learn more {ic("arrow", "ar")}</span></span></a>' for s in SERVICES)
    intro = faq_block([("Can I hire you for just one step?", "Yes. Plenty of owners start with an estimate audit and decide later whether to demand appraisal."),
                       ("Do you take commercial and HOA claims?", "Yes — houses, condos, rentals, multifamily, retail, office, churches and association-owned buildings."),
                       ("Do you work outside the big cities?", "Yes. We cover all 88 Ohio counties, rural townships included.")])
    body = page_hero(trail, "What we appraise", "Property Insurance Appraisal Services in Ohio",
                     "From a one-time estimate audit to full panel representation or neutral umpire work, every service is built around one thing: an accurate, defensible value for your loss.", "commercial-building") + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap faq-wrap"><div class="faq-l reveal"><p class="kicker">Where to start</p><h2>Most claims start with an estimate audit</h2><p>Before anyone demands appraisal, it helps to know exactly where the insurer’s estimate falls short and what the gap is worth. Many disputes close at that stage.</p><a class="btn btn-dark" href="{SVC_BASE}estimate-audit/">About estimate audits {ic("arrow")}</a></div><div class="reveal">{intro}</div></div></section>
{cta_strip()}"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Property Insurance Appraisal Services in Ohio",
                             "Property insurance appraisal services in Ohio: appraisal demands, estimate audits, hail, wind, ice dam, water and fire claims, plus umpire work.",
                             body, schema, photo="commercial-building"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Service cities", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO.get(l["slug"], "hero-home")
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        hoods = ", ".join(e(h) for h in l.get("hoods", []))
        snap = f"""<div class="snap"><div><small>County</small><b>{e(l["county"])}</b></div><div><small>Region</small><b>{e(l["region"])}</b></div><div class="wide"><small>Housing mix</small><span>{e(l.get("housing", ""))}</span></div><div class="wide"><small>Storm history</small><span>{e(l.get("storm", ""))}</span></div><div class="wide"><small>Local claim risks</small><ul class="chips">{chips}</ul></div></div>"""
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        art = snap + l["body"] + f"""<h2>Neighborhoods and nearby communities</h2><p>We inspect in and around {e(l["city"])}, including {hoods}, and anywhere else in {e(l["county"])} and the surrounding counties.</p>
<h2>Appraisal services in {e(l["city"])}</h2><ul class="cols2">{svc_links}</ul>
<h2>{e(l["city"])} claim questions</h2>{faq_block(l["faqs"])}
<h2>Nearby service cities</h2>{related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])}"""
        aside = call_box() + list_box("Ohio service cities", items, path) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', l["h1"], e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + layout(art, aside) + cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see.")
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Ohio", "serviceType": "Insurance appraisal", "description": l["desc"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Ohio"}}, "url": DOMAIN + path}]
        write(path, document(path, l["title"], l["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Service cities", LOC_BASE)]
    cities = "".join(f'<a class="city reveal" href="{loc_path(l)}">{img(LOC_PHOTO.get(l["slug"], "hero-home"), sizes="(max-width:700px) 50vw, 300px", alt="")}<span class="city-b"><b>{e(l["city"])}</b><small>{e(l["county"])}</small></span></a>' for l in LOCATIONS)
    regs = "".join(f'<article class="region reveal"><div class="region-ph">{img(ph, sizes="(max-width:700px) 100vw, 380px", alt="")}</div><div class="region-b"><p class="region-k">{e(sub)}</p><h2 class="card-h">{e(n)}</h2><p>{e(t)}</p><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul></div></article>' for n, sub, ph, t, chips in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisers Serving All 88 Ohio Counties",
                     "Ohio Insurance Appraiser works statewide, from the Lake Erie shore to the Ohio River. These local pages cover the cities where we handle claims most often.", "columbus-skyline") + f"""
<section class="sec"><div class="wrap"><div class="cities" data-stagger>{cities}</div></div></section>
<section class="sec sec-tint"><div class="wrap"><div class="sec-head reveal"><p class="kicker">Regions</p><h2>How claims differ across Ohio</h2><p>The same policy wording plays out very differently on a snowbelt farmhouse, a Columbus subdivision and a Cincinnati hillside home.</p></div><div class="region-grid" data-stagger>{regs}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Ohio county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Ohio Insurance Appraiser Service Cities | 88 Counties",
                             "Insurance appraisers serving all 88 Ohio counties, including Columbus, Cleveland, Cincinnati, Toledo, Akron, Dayton, Canton and Youngstown.",
                             body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(f"{l['city']}, Ohio", loc_path(l)) for l in LOCATIONS])], photo="columbus-skyline"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Workbench", TOOL_BASE), (t["name"], path)]
        others = [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]
        ph = TOOL_PHOTO[t["slug"]]
        art = t["explain"] + f"""<h2>Questions about this tool</h2>{faq_block(t["faqs"])}<h2>More free tools</h2>{related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in others])}"""
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}<noscript><p class="note-js">This calculator needs JavaScript. Turn it on, or call {PHONE} and we’ll run the numbers with you.</p></noscript>
<p class="hint">For planning only. Results depend on what you enter and on your policy, and aren’t a quote, an appraisal or legal advice.</p></div></section>""" + layout(art, call_box() + list_box("Workbench tools", items, path)) + cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll go through it line by line.")
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "description": t["desc"], "url": DOMAIN + path, "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Workbench", TOOL_BASE)]
    cards = "".join(f'<a class="card reveal" href="{TOOL_BASE}{t["slug"]}/"><span class="card-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:700px) 100vw, (max-width:1080px) 50vw, 380px", alt="")}<span class="card-ic">{ic(TOOL_ICON.get(t["icon"], "doc"))}</span><span class="card-kind">{e(t["kind"])}</span></span><span class="card-b"><h2 class="card-h">{e(t["name"])}</h2><span class="card-p">{e(t["short"])}</span><span class="card-more">Open tool {ic("arrow", "ar")}</span></span></a>' for t in TOOLS)
    order = f"""<ol class="ordered"><li>Start with the <a href="{TOOL_BASE}claim-calendar-builder/">claim calendar builder</a> so no date slips past.</li><li>Check the roof with the <a href="{TOOL_BASE}roof-area-pitch-calculator/">roof area &amp; pitch calculator</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">percentage deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">RCV/ACV holdback</a> calculators — or the <a href="{TOOL_BASE}basement-backup-sublimit-calculator/">backup sublimit calculator</a> for basement water.</li><li>Test the dispute with the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-checkup/">readiness checkup</a>.</li></ol>"""
    body = page_hero(trail, "Free & private", "Free Insurance Claim Calculators for Ohio Owners",
                     "Seven calculators and planners built from real appraisal work. Check the insurer’s math, plan your deadlines and decide on next steps — no sign-up, nothing stored.", "calculator", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap faq-wrap"><div class="faq-l reveal"><p class="kicker">Suggested order</p><h2>Using the workbench together</h2>{order}</div><div class="reveal">{call_box()}</div></div></section>"""
    schema = [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list(items)]
    write(TOOL_BASE, document(TOOL_BASE, "Free Insurance Claim Calculators for Ohio",
                              "Free insurance claim calculators for Ohio: appraisal cost, RCV vs ACV, roof squares, percentage deductible, sewer backup and deadline tools.",
                              body, schema, photo="calculator"), 0.9)


# ---------------------------------------------------------------- learn
def _stage_ids(h):
    return re.sub(r"<h2>Stage (\d+):", lambda m: f'<h2 id="stage-{m.group(1)}">Stage {m.group(1)}:', h)


def learn_pages():
    learn_items = [("Appraisal timeline", P_PROCESS), ("Appraisal Q&A", P_FAQ), ("Appraisal lexicon", P_GLOSS), ("Briefings", POST_BASE)]

    path = P_PROCESS
    trail = [("Home", "/"), ("Appraisal timeline", path)]
    body = page_hero(trail, "Process guide", "The Insurance Appraisal Process in Ohio, Stage by Stage",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what and where Ohio claims most often go wrong.", "clipboard",
                     [("Stages", str(len(PROCESS_STEPS))), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + layout(_stage_ids(PROCESS_BODY), call_box() + list_box("Resources", learn_items, path)) + cta_strip()
    howto = {"@type": "HowTo", "name": "The insurance appraisal process in Ohio", "description": "How a disputed property claim moves through the policy’s appraisal clause, from the written demand to the signed award.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#stage-{i + 1}"} for i, n in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Insurance Appraisal Process in Ohio | 7 Stages",
                         "The insurance appraisal process in Ohio step by step: the written demand, naming appraisers, seating an umpire, comparing estimates and the award.",
                         body, [crumbs_schema(trail), howto], photo="clipboard"), 0.8)

    path = P_FAQ
    trail = [("Home", "/"), ("Appraisal Q&A", path)]
    toc = "".join(f'<li><a href="#q-{i}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    groups = f'<nav class="toc" aria-label="Topics"><p class="toc-h">Jump to a topic</p><ul>{toc}</ul></nav>' + "".join(f'<h2 id="q-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Insurance Appraisal Questions and Answers for Ohio",
                     "Plain answers to the questions Ohio owners ask most — the appraisal process, costs and timing, policy rules, insurers and winter and storm claims.", "living-room") + layout(groups, call_box() + list_box("Resources", learn_items, path)) + cta_strip("Didn’t see your question?", "Call or email — we’re glad to talk it through.")
    write(path, document(path, "Insurance Appraisal Questions & Answers | Ohio",
                         "Ohio insurance appraisal questions answered by topic: how appraisal works, what it costs, how long it takes, policy rules and winter storm claims.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="living-room"), 0.8)

    path = P_GLOSS
    trail = [("Home", "/"), ("Appraisal lexicon", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#l-{c}">{c}</a>' for c in letters)
    terms, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="l-{c}"' if c not in seen else ""
        seen.add(c)
        terms += f'<div class="term"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    art = f"""<div class="lex-tools"><label for="lex-filter">Search the lexicon</label><div class="lex-in">{ic("search")}<input id="lex-filter" type="search" placeholder="Try “holdback” or “umpire”" autocomplete="off"></div><p class="hint" data-lex-count>{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Letters">{az}</nav><dl class="lexicon">{terms}</dl>"""
    body = page_hero(trail, "Reference", "Insurance Appraisal Glossary: The Ohio Claim Lexicon",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, defined in plain English and searchable.", "paperwork", cta=False) + layout(art, call_box() + list_box("Resources", learn_items, path))
    dts = {"@type": "DefinedTermSet", "name": "Ohio insurance appraisal lexicon", "url": DOMAIN + path, "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": {"@id": DOMAIN + path + "#definedtermset"}} for t, d in GLOSSARY]}
    write(path, document(path, "Insurance Appraisal Glossary | Claim Terms Defined",
                         f"Insurance appraisal glossary with {len(GLOSSARY)} searchable claim terms: ACV, RCV, holdback, umpire, award, percentage deductible, backup endorsement and more.",
                         body, [crumbs_schema(trail), dts], photo="paperwork"), 0.7)

    for i, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Briefings", POST_BASE), (p["title"], path)]
        others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        art = f'<p class="byline">By the {BRAND} team · <time datetime="{p["date"]}">{nice}</time> · {e(p["read"])} read</p>' + p["body"] + f'<h2>Keep reading</h2>{related([("Briefing", o["title"], f"{POST_BASE}{o["slug"]}/") for o in others])}'
        body = page_hero(trail, f"Briefing · {p['read']} read", p["title"], e(p["summary"]), ph, cta=False) + layout(art, call_box() + list_box("Resources", learn_items) + list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])) + cta_strip()
        art_s = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "keywords": p.get("kw", ""), "image": f"{DOMAIN}/assets/img/photos/{P(ph)}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art_s], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Briefings", path)]
    cards = "".join(f'<a class="post reveal" href="{POST_BASE}{p["slug"]}/"><span class="post-ph">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 380px", alt="")}</span><span class="post-b"><small>{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {e(p["read"])} read</small><h2 class="card-h">{e(p["title"])}</h2><span class="card-p">{e(p["summary"])}</span></span></a>' for p in POSTS)
    body = page_hero(trail, "Briefings", "Insurance Appraisal Guides for Ohio Property Owners",
                     "Practical briefings on Ohio policy language, documentation and claim timing — written by people who work appraisal panels.", "kitchen", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{cards}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Insurance Appraisal Guides for Ohio Owners",
                         "Insurance appraisal guides for Ohio owners: demand letters, basement water, slate roofs after hail, ice dams, suit deadlines and wind claims.",
                         body, [crumbs_schema(trail), {"@type": "CollectionPage"}, item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="kitchen"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = P_ABOUT
    trail = [("Home", "/"), ("About the firm", path)]
    art = f"""
<figure class="lead-img">{img("consultation", sizes="(max-width:1080px) 100vw, 760px")}</figure>
<h2>A practice built around one question</h2>
<p>Most claim professionals do a bit of everything. We chose to specialize. Ohio Insurance Appraiser works on the amount of loss — what the damage actually costs to put right — and our inspections, estimates and reports are built to answer that question clearly enough for everyone at the table to check.</p>
<p>That focus lets us serve in three roles: as the appraiser you name after appraisal is demanded, as a reviewer who audits an insurer’s estimate before a dispute hardens, or as a neutral umpire on panels where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope before numbers.</strong> We inspect and measure before we read anyone else’s estimate.</li>
<li><strong>Supportable, not inflated.</strong> An inflated number loses credibility with an umpire. We price what we can back up with photos, measurements and local costs.</li>
<li><strong>Plain-English reports.</strong> You’ll see every difference between our valuation and the insurer’s, line by line.</li>
<li><strong>Honest triage.</strong> If a claim needs an attorney or a public adjuster instead, we say so on the first call.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Who we work with</h2>
<p>Homeowners, condo owners, landlords, HOA boards, property managers, churches, business owners, contractors, public adjusters and attorneys across Ohio. On any claim we serve in one role only, and we disclose prior dealings with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters, and we don’t negotiate claims outside the appraisal process. No honest appraiser can guarantee an outcome, and we don’t.</p>
<h2>Why statewide</h2>
<p>Ohio’s weather changes a lot between the snowbelt, the northwest farm country, the Columbus suburbs, the Miami Valley and the Appalachian southeast. Working in all 88 counties means we see every kind of loss the state produces — ice dams in Geauga County, hail in Franklin County, tornadoes near Dayton, ice storms around Zanesville — and price each with local knowledge.</p>"""
    body = page_hero(trail, "About the firm", "About Ohio Insurance Appraiser",
                     "We’re estimators and appraisers who think a property claim should be paid on what the damage really costs — documented clearly enough that everyone can see it.", "clipboard") + layout(art, call_box() + list_box("Explore", [("Services", SVC_BASE), ("Service cities", LOC_BASE), ("Free workbench", TOOL_BASE), ("Appraisal timeline", P_PROCESS)])) + cta_strip()
    write(path, document(path, "About Ohio Insurance Appraiser | The Firm",
                         "About Ohio Insurance Appraiser, an independent appraisal and estimating practice focused on the amount of loss in disputed Ohio property claims.",
                         body, [crumbs_schema(trail), {"@type": "AboutPage"}], photo="clipboard"), 0.7)

    path = P_CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Contact", "Contact Ohio Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "consultation", cta=False) + f"""
<section class="sec"><div class="wrap contact-grid">
<div class="contact-l reveal"><h2>Reach us directly</h2>
<ul class="contact-lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 88 Ohio counties</b></div></li></ul>
<h3>Good to have ready</h3><ul class="ticks"><li>{ic("check")}Declarations page</li><li>{ic("check")}The insurer’s full estimate (PDF)</li><li>{ic("check")}Letters or emails from the insurer</li><li>{ic("check")}Photos and your contractor’s estimate</li></ul></div>
<div class="reveal">{lead_form("Tell us about your claim", page=path, hid="c")}</div></div></section>"""
    write(path, document(path, "Contact Ohio Insurance Appraiser | (844) 537-1427",
                         "Get a free review of a disputed Ohio property claim. Call or text (844) 537-1427 or email info@ohioinsuranceappraiser.com to reach the team.",
                         body, [crumbs_schema(trail), {"@type": "ContactPage"}], photo="consultation"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, sizes="120px", alt="", extra=" class=\"cred-img\"")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")} · {e(v.get("source_name", ""))}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        P_PRIV: ("Privacy Commitment", "privacy policy", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email us, we collect what you choose to share — your name, phone number, email address, property location and details about your claim. Our web server also keeps standard technical logs (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To answer your inquiry and evaluate your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>The calculators and checklists run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>We don’t use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used only to understand how the site is used.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>To access, correct or delete the information you’ve given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>""",
                 "How we collect, use and protect the information you share with us.",
                 "Privacy policy for Ohio Insurance Appraiser: what we collect when you contact us, how we use it, and why our claim tools never store your numbers."),
        P_TERMS: ("Terms of Use", "terms of use", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Ohio.</p>
<h2>No professional relationship</h2><p>Reading the site, using its tools or sending a form doesn’t create an appraiser–client relationship. That starts only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ and laws and court decisions change. For legal questions, consult a licensed Ohio attorney.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the information you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses on our <a href="{P_CRED}">photo sources</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made on the basis of its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Ohio.</p>""",
                  "The terms that apply when you use this website and its tools.",
                  "Terms of use for the Ohio Insurance Appraiser website: no legal advice, no client relationship until signed, and how the free claim tools may be used."),
        P_DISC: ("Disclaimer", "disclaimer", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We aren’t attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and aren’t results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits — many Ohio policies limit suits to one year. Nothing on this site extends or changes a deadline. If one is close, talk to an Ohio attorney promptly.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>
<h2>References</h2><p>References to rules, agencies and weather events are for context. Check current law and facts with official sources such as the Ohio Department of Insurance.</p>""",
                "Important limits on the information published on this website.",
                "Disclaimer for Ohio Insurance Appraiser: general information only, not legal advice, illustrative figures, no guaranteed results and policy deadlines."),
        P_CRED: ("Photo Sources", "photo credits", f"""
<p>Every photograph on this site is royalty-free: dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work such as a U.S. government photo. No attribution is legally required, but we credit the photographers and sources here with thanks. Photos are illustrative and don’t show clients’ properties.</p>
<div class="table-wrap"><table class="cred"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>""",
                "Sources and licenses for every photograph used on this site.",
                "Photo credits for Ohio Insurance Appraiser: every image is CC0 or public domain, listed here with its title, creator, license and original source."),
    }
    for path, (title, kw, content, lede, desc) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Legal", title, lede, "commercial-building", cta=False) + layout(content, call_box())
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)


def sitemap_pages():
    path = P_MAP
    trail = [("Home", "/"), ("Site guide", path)]
    groups = [
        ("Main", [("Home", "/"), ("About the firm", P_ABOUT), ("Contact", P_CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Service cities", [("All cities", LOC_BASE)] + [(f"{l['city']}, Ohio", loc_path(l)) for l in LOCATIONS]),
        ("Workbench", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Resources", [("Appraisal timeline", P_PROCESS), ("Appraisal Q&A", P_FAQ), ("Appraisal lexicon", P_GLOSS), ("Briefings", POST_BASE)] + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy commitment", P_PRIV), ("Terms of use", P_TERMS), ("Disclaimer", P_DISC), ("Photo sources", P_CRED)]),
    ]
    cols = "".join(f'<div class="map-col reveal"><h2 class="card-h">{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Guide", f"Every page on {BRAND}, in one place.", "commercial-building", cta=False) + f'<section class="sec"><div class="wrap map-grid" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Site Guide | {BRAND}", "Every page on Ohio Insurance Appraiser in one list: services, Ohio service cities, free claim tools, guides and the legal pages.",
                         body, [crumbs_schema(trail)], photo="commercial-building"), 0.3)

    body = f"""<section class="phero phero-404"><div class="phero-bg">{img("storm-clouds", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="tag">Error 404</p><h1>That page isn’t here</h1><p class="lede">It may have moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-red" href="/">Home</a><a class="btn btn-ghost-w" href="{SVC_BASE}">Services</a><a class="btn btn-ghost-w" href="{TOOL_BASE}">Free tools</a><a class="btn btn-ghost-w" href="{P_CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The page you requested could not be found on Ohio Insurance Appraiser.", body, robots="noindex,follow", photo="storm-clouds"), sitemap=False)


GUARD_PHP = r"""<?php
// Ohio Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$oia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$oia_real  = 'ohioinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$oia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://ohioinsuranceappraiser.com - only on the real domain.
if ($oia_host === 'www.' . $oia_real || ($oia_host === $oia_real && $oia_proto === 'http')) {
    header('Location: https://' . $oia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $oia_m)) {
    $oia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $oia_m[1] . $oia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($oia_host !== $oia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Ohio Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (a directory's index.php included)
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
    stray = [os.path.join(dp, f) for dp, _, fs in os.walk(OUT) for f in fs if f == "index.html"]
    assert not stray, f"dir/index.html must never be written: {stray}"
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
