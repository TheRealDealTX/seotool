#!/usr/bin/env python3
"""Static site generator for vermontinsuranceappraiser.com.

python3 build.py   -> writes the complete site into ./public
No dependencies beyond the Python 3 standard library.
Engineering adapted from the Georgia template (guard, front controller, contact handler, tools);
content, URL structure and design are specific to this site.
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
from learn import PROCESS_BODY, PROCESS_STEPS, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Vermont Insurance Appraiser"
HOST = "vermontinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261116a"
FAV = "1"
# Google Tag Manager container ID, e.g. "GTM-XXXXXXX". Empty = no GTM output.
GTM_ID = ""
# Google Search Console HTML-file verification. Written byte-for-byte to the site root on every build.
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = "google-site-verification: googlecccfbf2f7e9e5ae4.html"

SVC_BASE = "/vt-claim-appraisal/"
LOC_BASE = "/vermont-towns/"
TOOL_BASE = "/vermont-claim-tools/"
POST_BASE = "/appraisal-field-guides/"
PROCESS = "/vermont-appraisal-process/"
FAQ_P = "/vermont-claim-questions/"
GLOSS = "/searchable-claim-glossary/"
ABOUT = "/our-vermont-practice/"
CONTACT = "/claim-review-request/"
PRIVACY = "/how-we-use-information/"
TERMS = "/site-use-terms/"
DISCL = "/scope-disclaimer/"
SITEMAP_P = "/all-vermont-pages/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


def loc_label(l):
    return f"{l['city']}, VT"


LOC_BY = {l["slug"]: l for l in LOCATIONS}

# ---------------------------------------------------------------- photos
ALT = {
    "farmhouse-snow": "White clapboard farmhouse with a red brick chimney in late-winter snow",
    "foliage-ridge": "Autumn foliage across forested Green Mountain ridges under a blue sky",
    "foliage-valley": "View over a valley of orange and red autumn forest from a rocky summit",
    "icicles-gutter": "Long icicles hanging from a roof gutter in bright winter sun",
    "snow-roof-eaves": "Thick snow overhanging a roof edge with icicles along the gutter",
    "snowy-street": "Residential street with snow-covered roofs and plowed snowbanks",
    "victorian-snow": "Red Victorian house with a long porch and gingerbread trim in winter",
    "red-barn-snow": "Weathered red barn with a new metal roof standing in snow",
    "white-barn-snow": "Old white barn in a snowy valley below snow-dusted hills",
    "barn-roof-crew": "Roofing crew and a telehandler installing a metal roof on a red barn",
    "roof-aerial": "Aerial view of a newly roofed wooden building in a forest clearing",
    "roof-damage": "Commercial building with roof covering torn away",
    "roofer-ladder": "Roofer climbing a ladder to the flat roof of a commercial building",
    "shingles": "Close-up of overlapping dark roof shingles",
    "river-flood": "Floodwater covering roads and fields beside a swollen river",
    "winter-river": "River running between snow and ice-covered banks in winter",
    "timber-frame": "New timber framing and decking inside a building under repair",
    "framing-pipes": "Open wall framing with copper water pipes against a stone foundation",
    "bennington-aerial": "Aerial view of Bennington, Vermont, with brick buildings among trees",
    "north-bennington-house": "Weathered red wood-frame house with climbing vines in North Bennington",
    "fairbanks-museum": "Red sandstone Fairbanks Museum building in St. Johnsbury, Vermont",
    "covered-bridge": "Weathered wooden covered bridge over a pond surrounded by autumn trees",
    "windstorm-trees": "Large trees blown over against a yellow clapboard building after a windstorm",
    "fallen-trees-building": "Uprooted trees lying across a lawn in front of a two-story building after a storm",
    "fire-ladder": "Fire crew using an aerial ladder at a brick house fire",
    "burned-house": "Aerial view of a house badly damaged by fire",
    "calculator-pencil": "Calculator, pencil and sticky notes on a table",
    "calculator-hands": "Person working figures on a calculator beside open paperwork",
    "calculator-notebook": "Hand using a calculator beside a notebook and laptop",
    "team-meeting": "People meeting around a table with laptops and notes",
    "writing-papers": "Hands writing notes on paper beside a laptop",
    "business-document": "Pen resting on a printed document on a desk",
    "condo-building": "Brick condominium building with balconies among trees",
    "office-night": "Glass-fronted office building lit at dusk",
    "thunderstorm": "Dark storm clouds gathering over a treeline",
    "lightning-houses": "Lightning lighting up the night sky above house rooftops",
    "treasury-house": "Large stone house with white columns and a front portico",
}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp 1200w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "appraisal-clause-representation": "business-document", "homeowner-claim-appraisal": "victorian-snow",
    "commercial-hoa-claim-appraisal": "condo-building", "roof-and-hail-damage-appraisal": "roof-aerial",
    "wind-and-microburst-damage-appraisal": "windstorm-trees", "tropical-storm-claim-appraisal": "river-flood",
    "water-damage-claim-appraisal": "framing-pipes", "fire-and-smoke-claim-appraisal": "fire-ladder",
    "ice-dam-and-frozen-pipe-appraisal": "icicles-gutter", "snow-load-collapse-appraisal": "white-barn-snow",
    "insurance-estimate-review": "calculator-notebook", "umpire-services": "team-meeting",
}
LOC_PHOTO = {
    "burlington": "snowy-street", "south-burlington": "condo-building", "rutland": "foliage-valley",
    "montpelier": "river-flood", "barre": "winter-river", "st-albans": "red-barn-snow",
    "brattleboro": "fallen-trees-building", "bennington": "bennington-aerial", "middlebury": "barn-roof-crew",
    "st-johnsbury": "fairbanks-museum", "stowe": "snow-roof-eaves", "hartford": "covered-bridge",
}
TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator-pencil", "rcv-acv-holdback-calculator": "calculator-hands",
    "roof-pitch-squares-calculator": "shingles", "percentage-deductible-calculator": "thunderstorm",
    "claim-deadline-calendar": "business-document", "appraisal-readiness-check": "writing-papers",
    "roof-snow-load-estimator": "red-barn-snow",
}
POST_PHOTO = {
    "ice-dam-claims-in-vermont": "snow-roof-eaves", "flood-or-water-damage-after-a-vermont-storm": "river-flood",
    "documenting-a-winter-claim": "victorian-snow", "reading-a-carrier-estimate": "calculator-notebook",
    "lessons-from-irene-and-the-july-floods": "covered-bridge", "choosing-an-appraiser-and-umpire": "team-meeting",
}

# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M22 6l-10 7L2 6"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark():
    """Brand mark: a gold-ringed green seal with a mountain ridge and a level line (valuation)."""
    return ('<svg viewBox="0 0 48 48" width="42" height="42" aria-hidden="true" focusable="false">'
            '<rect width="48" height="48" rx="10" fill="#154734"/>'
            '<rect x="3.5" y="3.5" width="41" height="41" rx="7.5" fill="none" stroke="#ffcc33" stroke-width="2"/>'
            '<path d="M9 33l9.5-14 5 7 4-5.5L39 33z" fill="#ffcc33"/>'
            '<path d="M18.5 19l2.6 3.8 2.4-1.6 1.4 2" fill="none" stroke="#154734" stroke-width="1.8" stroke-linejoin="round"/>'
            '<path d="M10 38h28" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>')


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
        "address": {"@type": "PostalAddress", "addressRegion": "VT", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-VT", "availableLanguage": "en"}],
        "slogan": "Independent valuation for disputed property claims",
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims in all 14 Vermont counties.",
        "areaServed": [{"@type": "State", "name": "Vermont"}] + [{"@type": "City", "name": l["city"], "containedInPlace": {"@type": "State", "name": "Vermont"}} for l in LOCATIONS],
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Property claim valuation", "Ice dam claims", "Snow load collapse", "Flood and water damage claims"],
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
LEARN = [("How appraisal works", PROCESS), ("Claim questions (FAQ)", FAQ_P), ("Searchable glossary", GLOSS), ("Field guides", POST_BASE)]


def _groups():
    return [
        ("Services", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal services", SVC_BASE), True),
        ("Towns", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Vermont towns", LOC_BASE), True),
        ("Tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE), False),
        ("Learn", LEARN, None, False),
    ]


def header():
    menu = ""
    for name, links, allk, cols in _groups():
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        menu += f'<li><button type="button" data-drop aria-expanded="false">{name}{ic("chev", "chev")}</button><ul class="drop{" cols" if cols else ""}">{li}</ul></li>'
    menu += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    acc = ""
    for i, (name, links, allk, _) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a href="{allk[1]}"><b>{e(allk[0])} →</b></a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><div class="acc-panel" id="acc-{i}"><ul>{li}</ul></div></li>'
    acc += f'<li><a href="{ABOUT}">About</a></li><li><a href="{CONTACT}">Contact</a></li>'
    brand = f'<a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span><b>{BRAND}</b><small>Independent claim valuation</small></span></a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="util"><div class="wrap"><span>Appraisal &amp; umpire services · All 14 Vermont counties</span>
<div class="util-r"><a class="hide-s" href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{TEL}">{PHONE_INTL}</a></div></div></div>
<header class="head"><div class="wrap">
{brand}
<nav aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn gold small head-cta" href="tel:{TEL}">{ic("phone")} {PHONE}</a>
<button class="burger" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></button>
</div></header>
<div class="drawer-bg" data-close></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand}<button class="drawer-close" type="button" aria-label="Close menu" data-close>×</button></div>
<nav class="drawer-body" aria-label="Mobile"><ul><li><a href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · Statewide</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:6])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:7])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS[:6])
    return f"""<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/" aria-label="{BRAND} home">{mark()}<span><b>{BRAND}</b><small>Independent claim valuation</small></span></a>
<p>Independent appraisal, estimate review and umpire work for Vermont property owners whose covered claims were paid short, from the Champlain Valley to the Northeast Kingdom.</p>
<div class="foot-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET</span></div></div>
<div><h2>Services</h2><ul>{svc}<li><a href="{SVC_BASE}">All services</a></li></ul></div>
<div><h2>Towns</h2><ul>{loc}<li><a href="{LOC_BASE}">All towns</a></li></ul></div>
<div><h2>Free tools</h2><ul>{tl}<li><a href="{TOOL_BASE}">All tools</a></li></ul></div>
<div><h2>Practice</h2><ul><li><a href="{ABOUT}">About</a></li><li><a href="{PROCESS}">Appraisal process</a></li><li><a href="{FAQ_P}">FAQ</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Field guides</a></li><li><a href="{CONTACT}">Contact</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© {date.today().year} {BRAND}. All rights reserved.</span>
<ul><li><a href="{PRIVACY}">Privacy</a></li><li><a href="{TERMS}">Terms</a></li><li><a href="{DISCL}">Disclaimer</a></li><li><a href="{SITEMAP_P}">Site map</a></li></ul></div>
<p class="foot-disc">{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as public adjusters. Information on this site is general and educational, policies differ, and results depend on the facts of each claim. Example figures are illustrative.</p>
</div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ic("up")}</button>
<div class="mobile-call"><a href="tel:{TEL}">Call now</a><a href="{CONTACT}">Free review</a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});"
            "var f=d.getElementsByTagName(s)[0],\nj=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;"
            f"f.parentNode.insertBefore(j,f);\n}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="farmhouse-snow", page_type=None):
    canonical = DOMAIN + ("/" if path == "/" else path)
    extra_nodes, crumb_id = [], None
    for n in (schema or []):
        t = n.get("@type")
        if t == "BreadcrumbList":
            n["@id"] = crumb_id = canonical + "#breadcrumb"
        elif t == "FAQPage":
            n["@id"] = canonical + "#faq"
        else:
            n.setdefault("@id", canonical + "#" + t.lower())
        if t == "BlogPosting":
            n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
            n["author"] = {"@id": DOMAIN + "/#business"}
            n["publisher"] = {"@id": DOMAIN + "/#business"}
            n["inLanguage"] = "en-US"
        extra_nodes.append(n)
    pimg = PHOTOS[photo]
    webpage = {
        "@type": page_type or "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"]},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    main_types = ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList")
    main = [n["@id"] for n in extra_nodes if n.get("@type") in main_types]
    webpage["mainEntity"] = {"@id": main[0] if main else DOMAIN + "/#business"}
    graph = [org_schema(), site_schema(), webpage] + extra_nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp 1200w" imagesizes="100vw">\n')
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
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal in Vermont">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal in Vermont">
<meta name="geo.region" content="US-VT">
<meta name="geo.placename" content="Vermont">
<meta name="theme-color" content="#154734">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="16x16 32x32 48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;0,900;1,400&family=Spectral:ital,wght@0,600;0,700;1,600&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="has-hero">
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
    """Pages are dir/index.php: the host serves real files directly, so each page starts with the guard."""
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
        assert "<?" not in content, path
        content = f"<?php require_once dirname(__DIR__, {rel.count('/')}) . '/_guard.php'; ?>\n" + content
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    if sitemap:
        pages.append((path, priority))


# ---------------------------------------------------------------- shared blocks
def crumbs(trail):
    parts = [e(n) if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>' for i, (n, p) in enumerate(trail)]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span aria-hidden=\"true\">›</span>".join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<div class="facts">' + "".join(f"<div><small>{e(k)}</small><b>{e(v)}</b></div>" for k, v in facts) + "</div>"
    c = f'<div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return (f'<section class="page-hero">{img(photo, "bg", lazy=False, alt="", extra=" data-parallax=\"0.1\"")}<div class="wrap">{crumbs(trail)}'
            f'<span class="kicker on-dark">{e(tag)}</span><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>')


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs) + "</div>"


def call_box():
    return f'<div class="box call"><h2 class="box-t">Talk it through first</h2><p>The first conversation is free. We will tell you plainly whether appraisal fits your claim.</p><a class="big" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn gold" href="{CONTACT}">Send claim details</a></div>'


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}<span aria-hidden="true">›</span></a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul>{li}</ul></div>'


def cta_band(h="Is the carrier’s number short of the repair?", p="Send us the estimate. We will read it line by line and tell you what we see."):
    return f'<section class="cta-band"><div class="wrap"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn light" href="{CONTACT}">Email the estimate</a></div></div></section>'


LOSSES = ["Ice dam / frozen pipe", "Water / leak", "Wind / microburst", "Hail / roof", "Snow load / collapse", "Fire / smoke", "Tropical storm", "Fallen tree", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Send your claim details", page="/", hlevel="h3"):
    roles = ["Homeowner", "Second-home owner", "Business owner", "Condo or HOA board", "Property manager", "Contractor", "Attorney", "Public adjuster", "Other"]
    towns = [l["city"] for l in LOCATIONS] + ["Elsewhere in Vermont"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<{hlevel}>{e(heading)}</{hlevel}><p class="sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(towns)}</select></div>
<div><label for="f-amt">Approx. amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form does not create a client relationship. See the <a href="{PRIVACY}">privacy notice</a>.</span></label></div>
<div class="full"><button class="btn" type="submit" style="width:100%">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<div class="lead-card enter" style="animation-delay:.35s"><form action="/api/contact.php" method="post" data-lead novalidate>
<h2>Free claim review</h2><p class="sub">A few details and we will call you back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">Type of loss</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<div><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. See the <a href="{PRIVACY}">privacy notice</a>.</span></label></div>
<button class="btn gold" type="submit">Request my free review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<div class="trust">{ic("shield")}<span>No obligation. Your details stay private.</span></div>
</form></div>"""


def contact_lines():
    return f"""<ul class="contact-lines"><li><span class="ic">{ic("phone")}</span><div><span>Call or text</span><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li><span class="ic">{ic("mail")}</span><div><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li><span class="ic">{ic("clock")}</span><div><span>Hours</span><b>Mon–Fri, 8am–6pm ET</b></div></li><li><span class="ic">{ic("pin")}</span><div><span>Service area</span><b>All 14 Vermont counties</b></div></li></ul>"""


def card(href, photo, title, text, hl="h3", badge="", glyph="", more="Read more", meta="", cls=""):
    b = f'<span class="badge">{e(badge)}</span>' if badge else ""
    g = f'<span class="glyph" aria-hidden="true">{glyph}</span>' if glyph else ""
    m = f'<span class="meta">{e(meta)}</span>' if meta else ""
    return (f'<article class="card rv {cls}"><a class="ph" href="{href}" tabindex="-1" aria-hidden="true">{img(photo, sizes="(max-width:700px) 100vw, (max-width:1020px) 50vw, 33vw", alt="")}{b}{g}</a>'
            f'<div class="in">{m}<{hl}><a href="{href}">{e(title)}</a></{hl}><p>{e(text)}</p><a class="more" href="{href}" tabindex="-1" aria-hidden="true">{e(more)} →</a></div></article>')


# ---------------------------------------------------------------- home
SEASONS = [
    ("winter", "Winter", "Ice dams, frozen pipes, snow load", "icicles-gutter",
     ["Ice dams", "Burst pipes", "Roof collapse", "Chimney fires"],
     "December through March brings the claims Vermont is known for. Meltwater backs up behind ice at the eaves and into ceilings, pipes split during cold snaps, heavy wet snow loads barn and porch roofs, and wood stoves work overtime. A Vermont Insurance Appraiser spends much of the winter following water through walls and checking whether heat conditions in the policy were met."),
    ("spring", "Mud season", "Thaw, ice jams, high water", "river-flood",
     ["Ice-jam flooding", "Sump failures", "Roof leaks", "Basement water"],
     "When the snowpack melts, rivers rise and ice jams can push water into low-lying neighborhoods, as Montpelier saw in 1992. Basements take on water, sump pumps fail and old roofs that held all winter start to leak. Sorting covered water from excluded flood matters most in this season."),
    ("summer", "Summer", "Thunderstorms, hail, flash floods", "lightning-houses",
     ["Flash flooding", "Hail", "Microbursts", "Lightning"],
     "Warm-season storms bring hail and damaging straight-line winds, and some summers bring far worse. The July 2023 floods and the remnants of Beryl in July 2024 caused flash flooding across central Vermont and the Northeast Kingdom. Wind and tree damage often arrive alongside the water."),
    ("fall", "Fall", "Gales, falling trees, tropical remnants", "windstorm-trees",
     ["Tree impact", "Wind damage", "Tropical remnants", "Power-loss freeze-ups"],
     "Autumn gales and the occasional tropical remnant, like Irene in late August 2011, bring trees down onto roofs while the leaves are still on. The Halloween storm of 2019 knocked out power across the state. A fall loss can turn into a winter loss if repairs stall before the first hard freeze."),
]

REGIONS = [
    ("Champlain Valley & the northwest", "red-barn-snow", "Burlington, South Burlington, St. Albans, Middlebury",
     "Vermont’s most populated region mixes dense older neighborhoods, condos, lake camps and dairy farms. Wind off the lake, ice storms and summer hail are the main weather risks."),
    ("Central Vermont & the Green Mountains", "foliage-ridge", "Montpelier, Barre, Stowe, Waterbury",
     "River towns that flooded in 2023 and 2024, plus ski-country homes and condos carrying some of the heaviest snow loads in the state."),
    ("The Northeast Kingdom", "fairbanks-museum", "St. Johnsbury, Lyndon, Newport, Island Pond",
     "Long cold winters, remote properties and wood heat. Freeze-ups, snow load and chimney fires lead the claim list, and repair costs reflect the distance."),
    ("Southern Vermont & the eastern river valleys", "bennington-aerial", "Brattleboro, Bennington, Rutland, Hartford",
     "Irene hit this region hardest in 2011. Historic village homes, hillside lots and river valleys shape both the losses and the repair costs."),
]


def home():
    marquee_items = ["Ice dam claims", "Frozen pipe bursts", "Snow load collapse", "Flash flood wind damage", "Microburst roofs", "Chimney fires", "Condo association losses", "Farm and barn claims", "Estimate reviews", "Neutral umpire work"]
    marquee = "".join(f"<span>{e(x)}</span>" for x in marquee_items) + "".join(f'<span aria-hidden="true">{e(x)}</span>' for x in marquee_items)

    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(n)}<small>{e(s)}</small></button>'
        for i, (k, n, s, *_r) in enumerate(SEASONS))
    panels = "".join(
        f'<div class="season-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{"" if i == 0 else " hidden"}><div class="ph">{img(ph, sizes="(max-width:1020px) 100vw, 470px", alt="")}</div>'
        f'<div class="in"><h3>{e(n)} claims in Vermont</h3><ul class="chips">{"".join(f"<li>{e(c)}</li>" for c in chips)}</ul><p>{e(t)}</p></div></div>'
        for i, (k, n, _s, ph, chips, t) in enumerate(SEASONS))

    rows = "".join(
        f'<a class="svc-row rv" href="{SVC_BASE}{s["slug"]}/"><span class="n">{i + 1:02d}</span><span class="ph">{img(SVC_PHOTO[s["slug"]], sizes="112px", alt="")}</span>'
        f'<span><h3>{e(s["name"])}</h3><p>{e(s["short"])}</p></span>{ic("arrow")}</a>' for i, s in enumerate(SERVICES))

    steps = "".join(f'<li><span class="dot">{i + 1}</span><h3>{e(t)}</h3><p>{e(p.split(". ")[0])}.</p></li>' for i, (t, p) in enumerate(PROCESS_STEPS[:6]))

    regions = "".join(f'<article class="region rv"><div class="ph">{img(ph, sizes="(max-width:700px) 100vw, (max-width:1140px) 50vw, 25vw", alt="")}</div><div class="in"><h3>{e(n)}</h3><p>{e(t)}</p><p class="towns">{e(towns)}</p></div></article>' for n, ph, towns, t in REGIONS)

    tool_cards = "".join(card(f'{TOOL_BASE}{t["slug"]}/', TOOL_PHOTO[t["slug"]], t["name"], t["short"], badge=t["kind"], glyph=t["icon"], more="Open tool") for t in TOOLS[:6])
    town_cards = "".join(card(loc_path(l), LOC_PHOTO[l["slug"]], l["city"], l["lede"][:96].rsplit(" ", 1)[0] + "…", meta=l["county"], more="Local page", cls="town-card") for l in LOCATIONS[:8])
    post_cards = "".join(card(f'{POST_BASE}{p["slug"]}/', POST_PHOTO[p["slug"]], p["title"], p["summary"], meta=f'{p["read"]} read · Field guide', more="Read the guide") for p in POSTS[:3])

    home_faqs = [
        ("What does a Vermont Insurance Appraiser do?", "We value property damage when you and your insurer agree the loss is covered but disagree on the cost. As the appraiser you name, we inspect, write an independent line-item estimate, work the differences with the carrier’s appraiser and, if needed, present open items to a neutral umpire."),
        ("Is an appraiser the same as a public adjuster?", "No. A public adjuster handles the whole claim for you. An appraiser works inside the policy’s appraisal clause on one question, the amount of loss. We do not give legal advice."),
        ("When does it make sense to call?", "When coverage has been accepted, you have the carrier’s estimate, and the gap between it and your contractor’s number is meaningful, often more than about 10% or several thousand dollars."),
        ("Can appraisal help with a flood claim?", "Flood from rising water is usually excluded from homeowners policies. If you also have a flood policy, it has its own appraisal provision and strict deadlines. Covered wind, tree or plumbing damage from the same storm can be appraised under the property policy."),
        ("What does it cost?", "Each side pays its own appraiser and usually half the umpire. We quote our fee in writing before any work starts, and the first conversation is free."),
        ("Do you work in my part of Vermont?", "Yes. We work in all 14 counties, from Grand Isle to Windham and from Bennington to Essex."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("farmhouse-snow", lazy=False, alt="", extra=' data-parallax="0.18"')}</div>
<div class="wrap">
<div>
<span class="kicker on-dark enter">Independent claim appraisal · Statewide</span>
<h1 class="enter" style="animation-delay:.1s">Vermont Insurance Appraiser for claims that came up <em>short</em></h1>
<p class="lede enter" style="animation-delay:.2s">When the carrier agrees the damage is covered but its check will not pay for the repair, Vermont Insurance Appraiser builds an independent, line-by-line valuation and carries it through the appraisal clause in your policy.</p>
<div class="btn-row enter" style="animation-delay:.28s"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn light" href="#services">See what we handle {ic("arrow")}</a></div>
<ul class="hero-points enter" style="animation-delay:.36s"><li>{ic("check")}Your named appraiser</li><li>{ic("check")}Homes, camps, farms &amp; condos</li><li>{ic("check")}All 14 counties</li></ul>
</div>
{hero_form()}
</div>
</section>

<div class="marquee" aria-label="Claim types we value"><div class="marquee-track">{marquee}</div></div>

<section class="sec white"><div class="wrap split">
<div class="rv">
<span class="kicker">Where the money goes missing</span>
<h2>Most short claims are not denied. They are just missing lines.</h2>
<p>A slope left off the roof diagram. Plaster priced as drywall. Ice-and-water barrier nobody included. Each gap looks small on its own, but together they decide whether the check covers the repair. Vermont Insurance Appraiser starts from the building, not from the carrier’s estimate, and prices what is actually there.</p>
<ul class="ticks">
<li>{ic("check")}<div><b>Our own measurements</b>Every slope, room and wall measured on site rather than borrowed from the carrier’s sketch.</div></li>
<li>{ic("check")}<div><b>Built for an umpire</b>Numbers supported by photos and pricing, because that is what moves an award.</div></li>
<li>{ic("check")}<div><b>Straight answers</b>If your claim needs a lawyer or just a supplement request, we say so on the first call.</div></li>
</ul>
<a class="btn line" href="{ABOUT}">How Vermont Insurance Appraiser works {ic("arrow")}</a>
</div>
<div class="rv">
<div class="ledger" role="table" aria-label="Illustrative example of an ice dam estimate comparison">
<div class="ledger-head" role="row"><span role="columnheader">Line item</span><span role="columnheader">Carrier</span><span role="columnheader">Independent</span></div>
<div class="ledger-row" role="row"><span role="cell">Ceiling repair, two rooms</span><span role="cell">$1,840</span><span role="cell">$4,960</span></div>
<div class="ledger-row" role="row"><span role="cell">Wet insulation removal</span><span role="cell" class="miss">missing</span><span role="cell">$1,380</span></div>
<div class="ledger-row" role="row"><span role="cell">Wall cavity drying &amp; repair</span><span role="cell" class="miss">missing</span><span role="cell">$2,150</span></div>
<div class="ledger-row" role="row"><span role="cell">Ice &amp; water barrier at eaves</span><span role="cell" class="miss">missing</span><span role="cell">$1,720</span></div>
<div class="ledger-row" role="row"><span role="cell">Paint, matching adjoining walls</span><span role="cell">$610</span><span role="cell">$1,290</span></div>
<div class="ledger-row total" role="row"><span role="cell">Total</span><span role="cell">$2,450</span><span role="cell">$11,500</span></div>
<p class="ledger-note">Illustrative figures only, not a real client file. Policy terms decide which items are owed.</p>
</div>
</div>
</div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Four seasons of claims</span><h2>Every Vermont season leaves its own kind of damage</h2><p>The appraisal clause works the same in January and July, but the losses do not. Pick a season to see what a Vermont Insurance Appraiser is usually called about.</p></div>
<div class="seasons rv" data-tabs><div class="season-tabs" role="tablist" aria-label="Seasons">{tabs}</div>{panels}</div>
</div></section>

<section class="sec white" id="services"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Appraisal &amp; estimating</span><h2>Twelve services from Vermont Insurance Appraiser</h2><p>From a single estimate review to full panel representation or neutral umpire work. Each one is built around a valuation that holds up when someone checks it.</p></div>
<div class="svc-list" data-stagger>{rows}</div>
<p class="center" style="margin-top:36px"><a class="btn line" href="{SVC_BASE}">Compare all services {ic("arrow")}</a></p>
</div></section>

<section class="sec forest"><div class="wrap process-wrap">
<div class="sticky rv"><span class="kicker on-dark">The appraisal clause</span><h2>From disagreement to signed award</h2><p>The appraisal paragraph in your policy turns an open-ended argument into a defined process with a binding result on the amount of loss. Here is how Vermont Insurance Appraiser moves a file through it.</p><a class="btn gold" href="{PROCESS}">Read the full process guide {ic("arrow")}</a></div>
<ol class="steps"><span class="fill" aria-hidden="true"></span>{steps}</ol>
</div></section>

<section class="sec gold"><div class="wrap split">
<div class="rv"><span class="kicker">Two-number gap check</span><h2>Is the gap big enough for appraisal?</h2><p>Type in the two numbers you already have. A large gap is worth a conversation with a Vermont Insurance Appraiser. A small one may close faster with a documented supplement request.</p><p>The full <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a> adds appraiser and umpire fees and shows three possible outcomes side by side.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec white"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Statewide</span><h2>One small state, four very different claim regions</h2><p>Lake wind in the northwest, river floods in the center, deep cold in the Kingdom and Irene’s scars in the south. A Vermont Insurance Appraiser has to price each one with local knowledge.</p></div>
<div class="regions" data-stagger>{regions}</div>
</div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head c rv"><span class="kicker">Free &amp; private</span><h2>Claim tools from Vermont Insurance Appraiser</h2><p>Check the math before you pick up the phone. Every tool runs in your browser, and nothing you type is stored or sent.</p></div>
<div class="cards" data-stagger>{tool_cards}</div>
<p class="center" style="margin-top:36px"><a class="link" href="{TOOL_BASE}">All seven tools, including the roof snow load estimator</a></p>
</div></section>

<section class="sec white"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Local pages</span><h2>Towns where Vermont Insurance Appraiser works most</h2><p>We take claims in every county. These pages cover the towns we hear from most, with their housing, storm history and local claim patterns.</p></div>
<div class="cards four" data-stagger>{town_cards}</div>
<p class="center" style="margin-top:36px"><a class="link" href="{LOC_BASE}">See all twelve town pages</a></p>
</div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head c rv"><span class="kicker">Choosing help</span><h2>Appraiser, public adjuster or attorney?</h2><p>Each solves a different problem. Picking the right one first saves time and fees, and Vermont Insurance Appraiser will point you elsewhere when appraisal is not the right tool.</p></div>
<div class="table-wrap rv"><table><thead><tr><th scope="col">Question</th><th scope="col" class="hl">Appraiser</th><th scope="col">Public adjuster</th><th scope="col">Attorney</th></tr></thead><tbody>
<tr><th scope="row">Main job</th><td class="hl">Value the amount of loss</td><td>Prepare and negotiate the whole claim</td><td>Legal disputes and lawsuits</td></tr>
<tr><th scope="row">Best stage</th><td class="hl">Coverage accepted, amount disputed</td><td>Early, from first notice</td><td>Denials, bad faith, deadlines</td></tr>
<tr><th scope="row">Result</th><td class="hl">Award signed by two of three</td><td>Negotiated settlement</td><td>Settlement or judgment</td></tr>
<tr><th scope="row">Licensed by Vermont DFR?</th><td class="hl">No separate license</td><td>Yes</td><td>Licensed by the Vermont bar</td></tr>
</tbody></table></div>
</div></section>

<section class="sec white"><div class="wrap split top">
<div class="rv"><span class="kicker">Questions</span><h2>What people ask a Vermont Insurance Appraiser</h2><p>Straight answers on how appraisal works, what it costs and when it is the wrong move.</p><div class="btn-row" style="margin-top:22px"><a class="btn" href="{FAQ_P}">All claim questions {ic("arrow")}</a><a class="btn line" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec mist"><div class="wrap">
<div class="sec-head rv"><span class="kicker">Field guides</span><h2>Read before you demand appraisal</h2><p>Practical guides on ice dams, floods, winter documentation and reading an estimate, written for Vermont owners.</p></div>
<div class="cards" data-stagger>{post_cards}</div>
</div></section>

<section class="cta-photo">{img("foliage-valley", "bg", alt="", extra=' data-parallax="0.16"')}<div class="wrap rv"><span class="kicker on-dark">Before you sign off</span><h2>The best time to check the numbers is before you accept them</h2><p>A short review now can keep you from settling for a payment that will not cover the work.</p><div class="btn-row"><a class="btn gold" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec forest" id="contact"><div class="wrap split top">
<div class="rv"><span class="kicker on-dark">Start with a conversation</span><h2>Talk to Vermont Insurance Appraiser about your claim</h2><p>Tell us what happened and what the carrier offered. We will review it and give you a straight answer on whether appraisal is worth pursuing, with no pressure and no obligation.</p>{contact_lines()}</div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    schema = [faq_schema(home_faqs)]
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Vermont Insurance Appraiser offers independent appraisal, estimate review and umpire work for short ice dam, wind, water and fire claims.",
                        body, schema, photo="farmhouse-snow"), 1.0)


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Services", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        related = "".join(f'<a href="{SVC_BASE}{r["slug"]}/"><small>Service</small>{e(r["name"])}</a>' for r in rel)
        ph = SVC_PHOTO[s["slug"]]
        body = page_hero(trail, "Appraisal service", s["h1"], s["lede"], ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about this service</h2>{faq_block(s["faqs"])}
<h2>Related services</h2><div class="related">{related}</div>
</article>
<aside class="aside">{call_box()}{list_box("All services", items, path)}{list_box("Vermont towns", [(loc_label(l), loc_path(l)) for l in LOCATIONS[:5]] + [("All twelve towns", LOC_BASE)])}</aside></div>
{cta_band()}"""
        schema = [crumbs_schema(trail), faq_schema(s["faqs"]), {"@type": "Service", "name": s["name"], "serviceType": s["name"], "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
                                                                 "areaServed": {"@type": "State", "name": "Vermont"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}]
        write(path, document(path, s["title"], s["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Services", SVC_BASE)]
    cards = "".join(card(f'{SVC_BASE}{s["slug"]}/', SVC_PHOTO[s["slug"]], s["name"], s["short"], hl="h2", badge=f"Service {i + 1:02d}", more="View service") for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we handle", "Insurance Appraisal Services Across Vermont",
                     "Twelve services, one job: an accurate, defensible value for your loss. Start with an estimate review, bring us in once appraisal is demanded, or ask us to serve as a neutral umpire.", "roofer-ladder") + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec mist"><div class="wrap split top"><div class="rv"><span class="kicker">Not sure where to start?</span><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what the gap is worth. A review answers that in days, and many disputes close right there.</p><a class="btn" href="{SVC_BASE}insurance-estimate-review/">About estimate reviews {ic("arrow")}</a></div><div class="rv">{faq_block([("Can I hire you for just one step?", "Yes. Many clients start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and farm claims?", "Yes: inns, shops, multifamily buildings, condo associations, churches, barns and other farm structures."), ("Do you handle flood claims?", "We value covered damage. Flood from rising water is usually a separate policy with its own rules; we will explain how that affects your claim.")])}</div></div></section>
{cta_band()}"""
    schema = [crumbs_schema(trail), item_list(items)]
    write(SVC_BASE, document(SVC_BASE, "Vermont Insurance Appraisal Services | 12 Ways to Help",
                             "Vermont insurance appraisal services: appraisal clause work, estimate review, ice dam, snow load, wind, water and fire claims, and umpires.",
                             body, schema, photo="roofer-ladder", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- locations
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        name = loc_label(l)
        trail = [("Home", "/"), ("Towns", LOC_BASE), (l["city"], path)]
        near = "".join(f'<a href="{loc_path(LOC_BY[n])}"><small>Nearby</small>{e(LOC_BY[n]["city"])}</a>' for n in l["near"])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:8])
        ph = LOC_PHOTO[l["slug"]]
        chips = "".join(f"<li>{e(p)}</li>" for p in l["perils"])
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f"Insurance Appraiser in {name}", l["lede"], ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">
<div class="risk"><span class="h">Common claims in {e(l["city"])}</span><ul class="chips">{chips}</ul></div>
{l["body"]}
<h2>Services for {e(l["city"])} property owners</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the rest of {e(l["county"])}, including:</p>
<ul>{svc_links}</ul>
<h2>Questions from {e(l["city"])}</h2>{faq_block(l["faqs"])}
<h2>Nearby town pages</h2><div class="related">{near}</div>
</article>
<aside class="aside">{call_box()}{list_box("Vermont towns", items, path)}{list_box("Free claim tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_band(f"A disputed claim in {l['city']}?", "Send the estimate and your photos. We will tell you what we see.")}"""
        schema = [crumbs_schema(trail), faq_schema(l["faqs"]), {"@type": "Service", "name": f"Insurance appraisal in {name}", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"},
                                                                 "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Vermont"}}, "url": DOMAIN + path}]
        title = f"Insurance Appraiser in {l['city']}, VT | Claim Disputes"
        if len(title) > 58:
            title = f"Insurance Appraiser in {l['city']}, VT"
        desc = l.get("desc") or f"Insurance appraiser in {l['city']}, VT and {l['county']}: independent appraisal and estimate review for short storm, water and fire claims."
        if len(desc) > 143:
            desc = f"Insurance appraiser in {l['city']}, VT: independent appraisal and estimate review for short storm, water and fire claims in {l['county']}."
        write(path, document(path, title, desc, body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Towns", LOC_BASE)]
    cards = "".join(card(loc_path(l), LOC_PHOTO[l["slug"]], l["city"], l["lede"][:110].rsplit(" ", 1)[0] + "…", hl="h2", meta=l["county"], more="Local page", cls="town-card") for l in LOCATIONS)
    regions = "".join(f'<article class="region rv"><div class="ph">{img(ph, sizes="(max-width:700px) 100vw, 25vw", alt="")}</div><div class="in"><h3>{e(n)}</h3><p>{e(t)}</p><p class="towns">{e(towns)}</p></div></article>' for n, ph, towns, t in REGIONS)
    counties = "Addison, Bennington, Caledonia, Chittenden, Essex, Franklin, Grand Isle, Lamoille, Orange, Orleans, Rutland, Washington, Windham and Windsor"
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 14 Vermont Counties",
                     f"We take claims everywhere from Alburgh to Vernon. These town pages cover the places we hear from most, but we work in all fourteen counties: {counties}.", "foliage-ridge") + f"""
<section class="sec"><div class="wrap"><div class="cards four" data-stagger>{cards}</div></div></section>
<section class="sec mist"><div class="wrap"><div class="sec-head rv"><span class="kicker">Regions</span><h2>How claims differ around Vermont</h2><p>The same policy language plays out differently in a Burlington triplex, a Stowe ski condo and a Northeast Kingdom farmhouse.</p></div><div class="regions" data-stagger>{regions}</div></div></section>
{cta_band("Don’t see your town?", "We cover every Vermont county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Vermont Towns We Serve | Insurance Appraisal Statewide",
                             "Insurance appraisal in all 14 Vermont counties, with local pages for Burlington, Rutland, Montpelier, Barre, Brattleboro, Stowe and more.",
                             body, [crumbs_schema(trail), item_list([(loc_label(l), loc_path(l)) for l in LOCATIONS])], photo="foliage-ridge", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for idx, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim tools", TOOL_BASE), (t["name"], path)]
        others = "".join(f'<a href="{TOOL_BASE}{o["slug"]}/"><small>{o["kind"]}</small>{e(o["name"])}</a>' for o in [TOOLS[(idx + k) % len(TOOLS)] for k in (1, 2, 3)])
        ph = TOOL_PHOTO[t["slug"]]
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], t["lede"], ph, cta=False) + f"""
<section class="sec tight" style="padding-bottom:0"><div class="wrap">{t["markup"]}
<p class="hint">For planning only. Results depend on what you enter and on your policy, and are not a quote, an appraisal or legal advice. Nothing you type is stored or sent.</p></div></section>
<div class="wrap layout" style="padding-top:40px"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More free tools</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("All claim tools", items, path)}</aside></div>
{cta_band("Want a professional to check the numbers?", "Send the estimate and we will review it line by line.")}"""
        schema = [crumbs_schema(trail), faq_schema(t["faqs"]), {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication",
                                                                 "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
                                                                 "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}]
        write(path, document(path, t["title"], t["desc"], body, schema, photo=ph), 0.8)

    trail = [("Home", "/"), ("Claim tools", TOOL_BASE)]
    cards = "".join(card(f'{TOOL_BASE}{t["slug"]}/', TOOL_PHOTO[t["slug"]], t["name"], t["short"], hl="h2", badge=t["kind"], glyph=t["icon"], more="Open tool") for t in TOOLS)
    body = page_hero(trail, "Free & private", "Free Claim Tools for Vermont Property Owners",
                     "Seven calculators, planners and checklists built from appraisal work, including a roof snow load estimator for Vermont winters. No sign-up, and nothing you type leaves your browser.", "calculator-pencil", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>
<section class="sec mist"><div class="wrap split top"><div class="rv"><span class="kicker">A sensible order</span><h2>Using the tools together</h2><ol><li>Start with the <a href="{TOOL_BASE}claim-deadline-calendar/">claim deadline calendar</a> so nothing lapses.</li><li>Check the roof with the <a href="{TOOL_BASE}roof-pitch-squares-calculator/">roof pitch &amp; squares calculator</a>, and the <a href="{TOOL_BASE}roof-snow-load-estimator/">snow load estimator</a> for collapse claims.</li><li>See what you are owed with the <a href="{TOOL_BASE}percentage-deductible-calculator/">deductible</a> and <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">holdback</a> calculators.</li><li>Test the dispute in the <a href="{TOOL_BASE}claim-gap-fee-estimator/">claim gap &amp; fee estimator</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-readiness-check/">appraisal readiness check</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Vermont Claim Tools | Calculators and Planners",
                              "Free Vermont claim tools: claim gap and fee estimator, holdback, roof squares, deductible, deadline calendar, readiness and snow load math.",
                              body, [crumbs_schema(trail), item_list(items)], photo="calculator-pencil", page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- learn
def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("Appraisal process", path)]
    body = page_hero(trail, "Process guide", "The Vermont Insurance Appraisal Process, Step by Step",
                     "Eight stages from the first disagreement to a signed award: what happens, who does what and where files most often go wrong.", "timber-frame",
                     [("Stages", "8"), ("Panel", "Two appraisers + umpire"), ("Binding", "Two of three signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_BODY}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_band()}"""
    howto = {"@type": "HowTo", "name": "How the insurance appraisal process works in Vermont", "description": "The steps of a property insurance appraisal under a typical appraisal clause.",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": p, "url": f"{DOMAIN}{path}#step-{i + 1}"} for i, (t, p) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "Vermont Insurance Appraisal Process | 8 Clear Steps",
                         "The Vermont insurance appraisal process in eight steps: the written demand, naming appraisers, choosing an umpire and the binding award.",
                         body, [crumbs_schema(trail), howto], photo="timber-frame"), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Claim questions", path)]
    groups = "".join(f'<h2 id="faq-{i + 1}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    toc = "".join(f'<li><a href="#faq-{i + 1}">{e(g)}</a></li>' for i, (g, _) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers by topic", "Vermont Insurance Claim Questions, Answered",
                     "Plain answers grouped by topic: the basics, costs and timing, Vermont specifics, and working with us.", "north-bennington-house") + f"""
<div class="wrap layout"><article class="prose"><div class="callout"><b>Jump to a topic:</b><ul>{toc}</ul></div>{groups}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_band("Didn’t see your question?", "Call or email. We are happy to talk it through.")}"""
    write(path, document(path, "Vermont Insurance Claim Questions | Appraisal FAQ",
                         "Vermont insurance claim questions answered by topic: how appraisal works, costs, timing, flood, ice dams and how Vermont rules fit in.",
                         body, [crumbs_schema(trail), faq_schema(allq)], photo="north-bennington-house"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY, key=lambda x: x[0].lower()):
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f"<dt{anchor}>{e(term)}</dt><dd>{e(d)}</dd>"
    body = page_hero(trail, "Reference", "Searchable Insurance Claim Glossary",
                     f"{len(GLOSSARY)} terms from policies, estimates and appraisal awards, defined in plain English. Type in the box to filter.", "business-document", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="filter"><label for="gloss-filter">Search the glossary</label><input id="gloss-filter" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"></div><nav class="az" aria-label="Glossary letters">{az}</nav><dl class="glossary">{dl}</dl><p class="gloss-none" hidden>No terms match that search.</p></article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Property insurance claim glossary", "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    write(path, document(path, "Searchable Insurance Claim Glossary | 40 Terms",
                         "A searchable insurance claim glossary: ACV, RCV, holdback, ice dam, snow load, umpire, O&P and more, each defined in plain English.",
                         body, [crumbs_schema(trail), dts], photo="business-document"), 0.7)

    for idx, p in enumerate(POSTS):
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Field guides", POST_BASE), (p["title"], path)]
        others = "".join(f'<a href="{POST_BASE}{o["slug"]}/"><small>Field guide</small>{e(o["title"])}</a>' for o in [POSTS[(idx + k) % len(POSTS)] for k in (1, 2, 3)])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Field guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<p><em>This guide is general information, not legal advice. Your policy’s wording controls.</em></p><h2>Keep reading</h2><div class="related">{others}</div></article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN)}{list_box("Free tools", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:3]])}</aside></div>{cta_band()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [crumbs_schema(trail), art], og_type="article", photo=ph), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Field guides", path)]
    cards = "".join(card(f'{POST_BASE}{p["slug"]}/', POST_PHOTO[p["slug"]], p["title"], p["summary"], hl="h2", meta=f'{date.fromisoformat(p["date"]).strftime("%b %-d, %Y")} · {p["read"]} read', more="Read the guide") for p in POSTS)
    body = page_hero(trail, "Field guides", "Appraisal Field Guides for Vermont Property Owners",
                     "Practical reading on ice dams, floods, winter documentation, estimates and choosing an appraiser, written for Vermont owners.", "foliage-valley", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="cards" data-stagger>{cards}</div></div></section>{cta_band()}"""
    write(path, document(path, "Appraisal Field Guides | Vermont Claim Reading",
                         "Appraisal field guides for Vermont owners: ice dam claims, flood versus water damage, winter documentation and reading a carrier estimate.",
                         body, [crumbs_schema(trail), item_list([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="foliage-valley", page_type="CollectionPage"), 0.7)


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("About", path)]
    body = page_hero(trail, "About the practice", "About Vermont Insurance Appraiser",
                     "An independent appraisal and estimating practice for one question: what a covered property loss actually costs to repair in Vermont.", "treasury-house") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("timber-frame", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>Why a practice focused on appraisal</h2>
<p>Most claim professionals do a little of everything. {BRAND} works on the amount of loss: the measured, priced cost to put a building back the way it was. That focus lets us serve as the appraiser you name under your policy, review an estimate before a dispute grows, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>How we work</h2>
<ul>
<li><strong>Scope first.</strong> We inspect and measure before we read anyone else’s numbers.</li>
<li><strong>Defensible, not inflated.</strong> An inflated estimate loses credibility with an umpire. We price what we can support.</li>
<li><strong>Plain-English reporting.</strong> You will understand every difference between our valuation and the carrier’s.</li>
<li><strong>Honest triage.</strong> If your claim needs an attorney or a public adjuster instead, we say so.</li>
<li><strong>Fees in writing.</strong> You know the cost before any work starts.</li>
</ul>
<h2>Built for Vermont buildings</h2>
<p>Vermont’s housing is old and varied: timber-frame farmhouses with ells and attached barns, Victorian homes in the river towns, ski-country condos, lake camps and nineteenth-century downtown blocks. Repairs often involve plaster, slate, wide-plank floors and steep roofs, and remote sites add travel and short building seasons. We price those realities rather than software defaults.</p>
<h2>Who we work with</h2>
<p>Homeowners, second-home owners, landlords, condo and HOA boards, farm owners, churches, businesses, contractors, public adjusters and attorneys. On any one claim we serve in only one role, and we disclose prior dealings with the other appraiser or the umpire.</p>
<h2>What we are not</h2>
<p>We are not a law firm and do not give legal advice. We are not public adjusters and do not negotiate claims outside the appraisal process. We do not publish testimonials or promise results, because no honest appraiser can guarantee an award.</p>
<h2>Regulators and resources</h2>
<p>Insurance in Vermont is regulated by the Vermont Department of Financial Regulation, which licenses insurers, agents and public adjusters and accepts consumer complaints. If your dispute is about coverage, delay or claim handling, the Department or a Vermont attorney is often the right first call.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Our services", SVC_BASE), ("Vermont towns", LOC_BASE), ("Free tools", TOOL_BASE), ("Appraisal process", PROCESS)])}</aside></div>{cta_band()}"""
    write(path, document(path, "About Vermont Insurance Appraiser | Our Practice",
                         "About Vermont Insurance Appraiser, an independent practice that values disputed property losses for owners, boards and businesses statewide.",
                         body, [crumbs_schema(trail)], photo="treasury-house", page_type="AboutPage"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Contact", path)]
    body = page_hero(trail, "Get in touch", "Request a Free Vermont Claim Review",
                     "Call, text, email or send your claim details below. The first conversation is free, and we will tell you honestly whether appraisal is likely to help.", "team-meeting", cta=False) + f"""
<section class="sec forest"><div class="wrap split top">
<div class="rv"><span class="kicker on-dark">Direct lines</span><h2>Reach us directly</h2>{contact_lines()}
<h3>Helpful to have ready</h3><ul><li>Your declarations page</li><li>The carrier’s full, itemized estimate</li><li>Letters or emails from the carrier</li><li>Photos and your contractor’s estimate</li><li>For freeze losses, heat and fuel records</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Vermont Insurance Appraiser | (844) 537-1427",
                         "Request a free claim review from Vermont Insurance Appraiser. Call or text (844) 537-1427, email us, or send your claim details online.",
                         body, [crumbs_schema(trail)], photo="team-meeting", page_type="ContactPage"), 0.8)

    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        PRIVACY: ("Privacy Notice", "How we use information", "How we use information you share with Vermont Insurance Appraiser: form details, calls, tool privacy and your choices about your data.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you submit a form, call or email, we collect what you choose to share: your name, phone number, email address, property location and details about your claim. Our web host also records standard technical data, such as IP address, browser type and pages requested, for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to your inquiry and review your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We do not sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers that host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checklists run in your browser. The numbers you enter are not sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site does not use advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add analytics through Google Tag Manager, it will be used to understand how pages are used, not to sell data.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP at any time to opt out.</p>
<h2>Your choices</h2><p>To see, correct or delete information you have given us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        TERMS: ("Terms of Use", "Site use terms", "The terms that apply when you use the Vermont Insurance Appraiser website, its free claim tools and its published guides.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Vermont.</p>
<h2>No client relationship</h2><p>Reading this site, using its tools or sending a form does not create an appraiser–client relationship. That begins only when we both sign a written engagement agreement.</p>
<h2>No legal advice</h2><p>{BRAND} is not a law firm, and nothing here is legal advice. Policies differ and laws change. Consult a Vermont attorney for legal questions.</p>
<h2>Tools and examples</h2><p>Calculators give planning estimates from the figures you enter. Example figures on the site are illustrative. None of it is an appraisal, a quote or a prediction of any claim result.</p>
<h2>Content and photos</h2><p>Site text, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are public-domain or CC0 images used for illustration; they do not show our clients’ properties.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we are not liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Vermont.</p>"""),
        DISCL: ("Disclaimer", "Scope and limits", "Important limits on the information published by Vermont Insurance Appraiser: general content only, no legal advice and no promised results.", f"""
<h2>General information only</h2><p>Content on this site explains how insurance appraisal commonly works. Your policy’s wording controls. Always read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we do not give legal advice, and we do not act as public adjusters or negotiate claims outside the appraisal process.</p>
<h2>Legal topics</h2><p>References to Vermont law, including the state’s insurance trade practices provisions and court decisions on bad faith, are general descriptions only. They may be incomplete or out of date. Speak with a Vermont attorney about your situation.</p>
<h2>No promised results</h2><p>Every claim is different. Example figures are illustrative and are not results for any client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing on this site extends or changes any deadline. If one is near, consult a Vermont attorney promptly.</p>
<h2>Weather and history</h2><p>References to storms, floods and agencies give context. Verify current facts with official sources such as the Vermont Department of Financial Regulation, FEMA and the National Weather Service.</p>"""),
    }
    for path, (title, crumb, desc, content) in legal.items():
        trail = [("Home", "/"), (crumb, path)]
        body = page_hero(trail, "Legal", title, e(desc.split(": ")[-1] if ": " in desc else desc), "office-night", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        write(path, document(path, f"{title} | {BRAND}", desc, body, [crumbs_schema(trail)], photo="office-night"), 0.3)


def sitemap_pages():
    path = SITEMAP_P
    trail = [("Home", "/"), ("Site map", path)]
    groups = [
        ("Main", [("Home", "/"), ("About", ABOUT), ("Contact", CONTACT)]),
        ("Services", [("All services", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Vermont towns", [("All towns", LOC_BASE)] + [(loc_label(l), loc_path(l)) for l in LOCATIONS]),
        ("Claim tools", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Legal", [("Privacy notice", PRIVACY), ("Terms of use", TERMS), ("Disclaimer", DISCL)]),
    ]
    cols = "".join(f'<div class="plain-col rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Site Map: Every Vermont Insurance Appraiser Page", f"Every page on {BRAND}, grouped by section.", "winter-river", cta=False) + f'<section class="sec"><div class="wrap"><div class="index-grid" data-stagger>{cols}</div></div></section>'
    write(path, document(path, f"Site Map | {BRAND}", "The Vermont Insurance Appraiser site map lists every page: services, Vermont towns, free claim tools, field guides and legal pages.",
                         body, [crumbs_schema(trail)], photo="winter-river"), 0.3)

    body = f"""<section class="page-hero">{img("lightning-houses", "bg", lazy=False, alt="")}<div class="wrap"><span class="kicker on-dark">Error 404</span><h1>That page isn’t here</h1><p class="lede">It may have moved, or the address may have a typo. These links will get you back on track.</p><div class="btn-row"><a class="btn gold" href="/">Home</a><a class="btn light" href="{SVC_BASE}">Services</a><a class="btn light" href="{TOOL_BASE}">Free tools</a><a class="btn light" href="{CONTACT}">Contact</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "This Vermont Insurance Appraiser page could not be found. Use the links on this page to reach our services, tools or contact page.",
                                body, robots="noindex,follow", photo="lightning-houses"), sitemap=False)


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
    # Search Console verification file: exact single line, no newline, no wrapper.
    with open(os.path.join(OUT, GSC_FILE), "wb") as f:
        f.write(GSC_BODY.encode("ascii"))


GUARD_PHP = r"""<?php
// Vermont Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$via_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$via_real  = 'vermontinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$via_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://vermontinsuranceappraiser.com - only on the real domain.
if ($via_host === 'www.' . $via_real || ($via_host === $via_real && $via_proto === 'http')) {
    header('Location: https://' . $via_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$via_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($via_uri, '?'), $via_m)) {
    $via_q = strpos($via_uri, '?') !== false ? substr($via_uri, strpos($via_uri, '?')) : '';
    header('Location: ' . $via_m[1] . $via_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($via_host !== $via_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Vermont Insurance Appraiser - front controller for the static build.
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


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT, ignore=shutil.ignore_patterns("_private", "*.md"))
    home()
    service_pages()
    location_pages()
    tool_pages()
    learn_pages()
    company_pages()
    sitemap_pages()
    root_files()
    for dp, _, fs in os.walk(OUT):
        for f in fs:
            assert not (f == "index.html"), os.path.join(dp, f)
    print(f"built {len(pages)} sitemap pages into {OUT}")


if __name__ == "__main__":
    main()
