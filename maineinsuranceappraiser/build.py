#!/usr/bin/env python3
"""Static site generator for maineinsuranceappraiser.com.

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
from learn import PROCESS_STEPS, PROCESS_INTRO, PROCESS_OUTRO, FAQ, GLOSSARY, POSTS  # noqa: E402
from tools import TOOLS, GAP_MINI  # noqa: E402

OUT = os.path.join(ROOT, "public")
STATIC = os.path.join(ROOT, "static")
PHOTOS = json.load(open(os.path.join(ROOT, "src", "photos.json")))

BRAND = "Maine Insurance Appraiser"
HOST = "maineinsuranceappraiser.com"
DOMAIN = "https://" + HOST
PHONE = "(844) 537-1427"
PHONE_INTL = "+1 (844) 537-1427"
TEL = "+18445371427"
EMAIL = "info@" + HOST
TODAY = date.today().isoformat()
VER = "20261112c"
FAV = "1"
# Google Tag Manager container ID. Empty = no tag is output.
GTM_ID = "GTM-WPRSN8X2"
# Head snippet exactly as supplied by the site owner (used instead of the standard GTM loader when set).
GTM_HEAD_SNIPPET = """<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WPRSN8X2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>"""

SVC_BASE = "/appraisal-work/"
LOC_BASE = "/towns-we-cover/"
TOOL_BASE = "/claim-math/"
POST_BASE = "/owner-guides/"
ABOUT = "/our-approach/"
CONTACT = "/reach-us/"
PROCESS = "/the-appraisal-path/"
FAQ_P = "/answers/"
GLOSS = "/plain-english-glossary/"
SITEMAP_P = "/page-directory/"

e = html.escape
pages = []  # (path, priority) for sitemap.xml


def loc_path(l):
    return f"{LOC_BASE}{l['slug']}/"


LOC_BY = {l["slug"]: l for l in LOCATIONS}
SVC_BY = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------- photos
ALT = {k: v.get("alt", "") for k, v in PHOTOS.items()}


def img(key, cls="", sizes="100vw", lazy=True, alt=None, extra=""):
    p = PHOTOS[key]
    a = e(alt if alt is not None else ALT[key])
    load = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/photos/{key}.webp" srcset="/assets/img/photos/{key}-640.webp 640w, /assets/img/photos/{key}.webp {p["fw"]}w" '
            f'sizes="{sizes}" width="{p["fw"]}" height="{p["fh"]}" alt="{a}"{load} decoding="async"{extra}>')


SVC_PHOTO = {
    "party-appraiser-representation": "consultation", "homeowner-dispute-appraisal": "snow-house",
    "commercial-condo-association-appraisal": "condo-building", "roof-hail-loss-appraisal": "shingles",
    "windstorm-microburst-appraisal": "storm-damage", "noreaster-hurricane-appraisal": "storm-surf",
    "water-damage-loss-appraisal": "ceiling-damage", "fire-smoke-puffback-appraisal": "house-fire",
    "ice-dam-snow-load-appraisal": "icicles", "fallen-tree-limb-appraisal": "tree-on-house",
    "carrier-estimate-line-review": "laptop-calc", "umpire-neutral-panel-services": "meeting",
}
LOC_PHOTO = {
    "portland-maine": "portland-harbor", "lewiston-maine": "lewiston-street", "bangor-maine": "snow-street",
    "augusta-maine": "old-house-snow", "biddeford-maine": "cape-coast", "brunswick-maine": "red-house-snow",
    "scarborough-maine": "marsh", "waterville-maine": "moose-mist", "rockland-maine": "lobster-boat",
    "bar-harbor-maine": "bar-harbor", "presque-isle-maine": "farm-field", "sanford-maine": "farmhouse",
}
TOOL_PHOTO = {
    "settlement-gap-projector": "calc-docs", "rcv-acv-holdback-calculator": "calc-desk",
    "roof-pitch-squares-converter": "roofer", "percent-deductible-checker": "storm-clouds",
    "claim-date-tracker": "clipboard", "appraisal-file-strength-test": "plans-review",
    "seasonal-camp-vacancy-check": "lake-camp",
}
POST_PHOTO = {
    "ice-dam-claims-maine-estimates": "snow-roof", "maine-appraisal-clause-plain-reading": "consultation",
    "seasonal-camp-vacancy-freeze-claims": "lake-camp", "noreaster-wind-versus-flood-maine": "storm-surf",
    "appraiser-adjuster-or-lawyer-maine": "meeting", "oil-burner-puffback-documentation": "interior",
}

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
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "left": '<path d="M15 18l-6-6 6-6"/>',
    "right": '<path d="M9 18l6-6-6-6"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
}


def ic(name, cls="ic"):
    return f'<svg class="{cls}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_I[name]}</svg>'


def mark():
    """Brand mark: navy tile, white gable roof, two coral swells."""
    return ('<svg class="mark" width="44" height="44" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
            '<rect width="64" height="64" rx="14" fill="#133458"/>'
            '<path d="M14 33 32 16l18 17" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M21 28v8h22v-8" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>'
            '<path d="M12 44c4-3 8-3 12 0s8 3 12 0 8-3 12 0 4 2 4 2" fill="none" stroke="#e2683c" stroke-width="4" stroke-linecap="round"/>'
            '<path d="M12 52c4-3 8-3 12 0s8 3 12 0 8-3 12 0 4 2 4 2" fill="none" stroke="#e2683c" stroke-width="4" stroke-linecap="round" opacity=".6"/></svg>')


def brand(cls="brand"):
    return f'<a class="{cls}" href="/" aria-label="{BRAND}, home">{mark()}<span class="brand-t"><b>{BRAND}</b><small>Independent claim appraisal</small></span></a>'


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
        "address": {"@type": "PostalAddress", "addressRegion": "ME", "addressCountry": "US"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_INTL, "email": EMAIL, "contactType": "customer service", "areaServed": "US-ME", "availableLanguage": "en"}],
        "description": "Independent insurance appraisal, estimate review and umpire services for disputed property claims across all 16 Maine counties.",
        "areaServed": [{"@type": "State", "name": "Maine"}] + [{"@type": "City", "name": l["city"]} for l in LOCATIONS],
        "knowsAbout": ["Insurance appraisal", "Appraisal clause", "Ice dam claims", "Nor’easter damage", "Property claim valuation", "Umpire services"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Insurance appraisal services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{DOMAIN}{SVC_BASE}{s['slug']}/"}} for s in SERVICES]},
    }


def site_schema():
    return {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BRAND, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(trail)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def itemlist_schema(items):
    return {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": DOMAIN + p, "name": n} for i, (n, p) in enumerate(items)]}


# ---------------------------------------------------------------- layout
def _groups():
    return [
        ("Appraisal work", [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES], ("All appraisal work", SVC_BASE)),
        ("Towns", [(l["city"], loc_path(l)) for l in LOCATIONS], ("All Maine towns", LOC_BASE)),
        ("Claim math", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS], ("All free tools", TOOL_BASE)),
        ("Learn", [("The appraisal path", PROCESS), ("Answers (FAQ)", FAQ_P), ("Plain-English glossary", GLOSS), ("Owner guides", POST_BASE)], None),
    ]


def header():
    menu = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li class="all"><a href="{allk[1]}">{e(allk[0])} →</a></li>'
        wide = " wide" if len(links) > 8 else ""
        menu += f'<li class="has-drop"><button type="button" class="drop-btn" aria-expanded="false" aria-controls="dd-{i}">{name}{ic("chev", "chev")}</button><ul class="drop{wide}" id="dd-{i}">{li}</ul></li>'
    menu += f'<li><a class="top-link" href="{ABOUT}">Our approach</a></li>'

    acc = ""
    for i, (name, links, allk) in enumerate(_groups()):
        li = "".join(f'<li><a href="{p}">{e(n)}</a></li>' for n, p in links)
        if allk:
            li += f'<li><a class="all" href="{allk[1]}">{e(allk[0])} →</a></li>'
        acc += f'<li><button type="button" class="acc-btn" aria-expanded="false" aria-controls="acc-{i}">{name}{ic("chev", "chev")}</button><ul class="acc-panel" id="acc-{i}">{li}</ul></li>'
    acc += f'<li><a class="acc-link" href="{ABOUT}">Our approach</a></li><li><a class="acc-link" href="{CONTACT}">Reach us</a></li>'

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="top"><div class="wrap hdr-in">
{brand()}
<nav class="nav" aria-label="Main"><ul class="menu">{menu}</ul></nav>
<a class="btn btn-coral hdr-cta" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a>
<a class="burger" href="#drawer" role="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false"><span></span><span></span><span></span></a>
</div></header>
<div class="scrim" data-close aria-hidden="true"></div>
<aside class="drawer" id="drawer" aria-label="Mobile menu" aria-hidden="true" inert>
<div class="drawer-top">{brand("brand brand-sm")}<a class="drawer-x" href="#top" role="button" data-close aria-label="Close menu">×</a></div>
<nav class="drawer-nav" aria-label="Mobile"><ul><li><a class="acc-link" href="/">Home</a></li>{acc}</ul></nav>
<div class="drawer-foot"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn btn-line" href="{CONTACT}">Send claim details</a><small>Mon–Fri 8am–6pm ET · All 16 counties</small></div>
</aside>"""


def footer():
    svc = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    loc = "".join(f'<li><a href="{loc_path(l)}">{e(l["city"])}</a></li>' for l in LOCATIONS[:8])
    tl = "".join(f'<li><a href="{TOOL_BASE}{t["slug"]}/">{e(t["name"])}</a></li>' for t in TOOLS)
    return f"""<footer class="ftr">
<div class="ftr-band"><div class="wrap ftr-band-in"><h2>A claim that’s accepted can still come up short.</h2><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-line light" href="{CONTACT}">Send the estimate</a></div></div></div>
<div class="wrap ftr-grid">
<div class="ftr-about">{brand("brand brand-ftr")}
<p>Independent appraisal and estimating for disputed property claims, from the Kittery bridges to the St. John Valley.</p>
<p class="ftr-contact"><a href="tel:{TEL}">{PHONE_INTL}</a><a href="mailto:{EMAIL}">{EMAIL}</a><span>Mon–Fri 8am–6pm ET</span></p></div>
<div><h3>Appraisal work</h3><ul>{svc}<li><a href="{SVC_BASE}">Everything we appraise</a></li></ul></div>
<div><h3>Towns</h3><ul>{loc}<li><a href="{LOC_BASE}">All 16 counties</a></li></ul></div>
<div><h3>Claim math</h3><ul>{tl}</ul></div>
<div><h3>Learn</h3><ul><li><a href="{PROCESS}">The appraisal path</a></li><li><a href="{FAQ_P}">Answers</a></li><li><a href="{GLOSS}">Glossary</a></li><li><a href="{POST_BASE}">Owner guides</a></li><li><a href="{ABOUT}">Our approach</a></li><li><a href="{CONTACT}">Reach us</a></li></ul></div>
</div>
<div class="wrap ftr-legal"><span>© {date.today().year} {BRAND}</span>
<ul><li><a href="/privacy-practices/">Privacy</a></li><li><a href="/site-terms/">Terms</a></li><li><a href="/fine-print/">Disclaimer</a></li><li><a href="/photo-credits/">Photo credits</a></li><li><a href="{SITEMAP_P}">Page directory</a></li></ul>
<p>{BRAND} provides insurance appraisal, estimating and umpire services. We are not a law firm, do not give legal advice and do not act as a public adjuster. Information here is general; your policy controls, and results are never guaranteed.</p></div>
</footer>
<a class="to-top" href="#top" aria-label="Back to top">{ic("up")}</a>
<div class="callbar"><a href="tel:{TEL}">{ic("phone")}<span>Call</span></a><a href="{CONTACT}">{ic("mail")}<span>Free review</span></a></div>"""


def gtm_head():
    if not GTM_ID:
        return ""
    if GTM_HEAD_SNIPPET:
        return "<!-- Google Tag Manager -->\n" + GTM_HEAD_SNIPPET + "\n<!-- End Google Tag Manager -->\n"
    return ("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\nnew Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            f"}})(window,document,'script','dataLayer','{GTM_ID}');</script>\n<!-- End Google Tag Manager -->\n")


def gtm_body():
    if not GTM_ID:
        return ""
    return (f'<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"\n'
            'height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->\n')


PAGE_TYPES = ("WebPage", "AboutPage", "ContactPage", "CollectionPage", "FAQPage")


def document(path, title, desc, body, schema=None, og_type="website", robots="index,follow", photo="hero-coast", trail=None, page_type="WebPage", body_cls=""):
    canonical = DOMAIN + path
    nodes = []
    crumb_id = None
    if trail:
        b = crumbs_schema(trail)
        b["@id"] = crumb_id = canonical + "#breadcrumb"
        nodes.append(b)
    main_id = None
    for n in (schema or []):
        t = n.get("@type")
        if t == "FAQPage":
            n["@id"] = canonical + "#faq"
        elif t in ("BlogPosting", "Service", "WebApplication", "HowTo", "DefinedTermSet", "ItemList"):
            n.setdefault("@id", canonical + "#" + t.lower())
            if t == "BlogPosting":
                n["mainEntityOfPage"] = {"@id": canonical + "#webpage"}
                n["author"] = {"@id": DOMAIN + "/#business"}
                n["publisher"] = {"@id": DOMAIN + "/#business"}
                n["inLanguage"] = "en-US"
        if main_id is None and t in ("Service", "WebApplication", "BlogPosting", "HowTo", "DefinedTermSet", "ItemList"):
            main_id = n["@id"]
        nodes.append(n)
    if main_id is None:
        faqn = [n for n in nodes if n.get("@type") == "FAQPage"]
        main_id = faqn[0]["@id"] if (faqn and page_type == "FAQPage") else DOMAIN + "/#business"
    pimg = PHOTOS[photo]
    webpage = {
        "@type": "WebPage" if page_type == "FAQPage" else page_type, "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
        "inLanguage": "en-US", "isPartOf": {"@id": DOMAIN + "/#website"}, "about": {"@id": DOMAIN + "/#business"},
        "publisher": {"@id": DOMAIN + "/#business"}, "dateModified": TODAY,
        "primaryImageOfPage": {"@type": "ImageObject", "@id": canonical + "#primaryimage", "url": f"{DOMAIN}/assets/img/photos/{photo}.webp", "width": pimg["fw"], "height": pimg["fh"]},
        "mainEntity": {"@id": main_id},
    }
    if crumb_id:
        webpage["breadcrumb"] = {"@id": crumb_id}
    graph = [org_schema(), site_schema(), webpage] + nodes
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    pre = (f'<link rel="preload" as="image" href="/assets/img/photos/{photo}.webp" imagesrcset="/assets/img/photos/{photo}-640.webp 640w, '
           f'/assets/img/photos/{photo}.webp {pimg["fw"]}w" imagesizes="100vw">\n')
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gtm_head()}<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js';</script>
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
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{BRAND}: independent property claim appraisal across Maine">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<meta name="twitter:image:alt" content="{BRAND}: independent property claim appraisal across Maine">
<meta name="geo.region" content="US-ME">
<meta name="geo.placename" content="Maine">
<meta name="theme-color" content="#133458">
<link rel="icon" href="/favicon.ico?v={FAV}" sizes="48x48">
<link rel="icon" href="/favicon.svg?v={FAV}" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png?v={FAV}" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v={FAV}" sizes="180x180">
<link rel="manifest" href="/site.webmanifest?v={FAV}">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,600;112,700;112,800&amp;family=Onest:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
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
    # The host serves real files directly without the front controller, so every directory page is a
    # dir/index.php that first requires the canonical-host guard (www/http 301, /index.php 301, off-domain noindex).
    if path == "/":
        rel = "home.html"
    elif path.endswith(".html"):
        rel = path.strip("/")
    else:
        rel = path.strip("/") + "/index.php"
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
        parts.append(f'<span aria-current="page">{e(n)}</span>' if i == len(trail) - 1 else f'<a href="{p}">{e(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def page_hero(trail, tag, h1, lede, photo, facts=None, cta=True):
    f = ""
    if facts:
        f = '<dl class="spec">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts) + "</dl>"
    c = f'<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn btn-line light" href="{CONTACT}">Free claim review</a></div>' if cta else ""
    return f"""<section class="phero"><div class="phero-media">{img(photo, lazy=False, alt="")}</div><div class="wrap phero-in">{crumbs(trail)}<p class="kicker">{e(tag)}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{c}{f}</div></section>"""


def faq_block(faqs):
    return '<div class="faq">' + "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs) + "</div>"


def call_box():
    return f"""<div class="box box-call"><h2 class="box-t">Free first conversation</h2><p>We’ll look at the carrier’s estimate and tell you plainly whether appraisal fits.</p><a class="big-tel" href="tel:{TEL}">{PHONE_INTL}</a><a class="btn btn-coral full" href="{CONTACT}">Send claim details</a></div>"""


def list_box(title, items, current=None):
    li = "".join(f'<li><a href="{p}"{" aria-current=\"page\"" if p == current else ""}>{e(n)}</a></li>' for n, p in items)
    return f'<div class="box"><h2 class="box-t">{e(title)}</h2><ul class="box-list">{li}</ul></div>'


def cta_strip(h="Have an estimate that doesn’t add up?", p="Email us the carrier’s estimate and your photos. We’ll review the lines and tell you what we see."):
    return f"""<section class="strip"><div class="wrap strip-in rv"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>{PHONE}</span></a><a class="btn btn-line light" href="{CONTACT}">Send the estimate</a></div></div></section>"""


def related(items):
    return '<div class="related">' + "".join(f'<a href="{p}"><small>{e(k)}</small><span>{e(n)}</span>{ic("arrow")}</a>' for k, n, p in items) + "</div>"


LOSSES = ["Ice dam / snow load", "Frozen or burst pipe", "Wind / nor’easter", "Fallen tree", "Roof / hail", "Water leak", "Fire / smoke / puffback", "Other"]


def _opt(xs):
    return "".join(f"<option>{e(x)}</option>" for x in xs)


def lead_form(heading="Tell us about the claim", page="/", hlevel=3):
    roles = ["Homeowner", "Camp / second-home owner", "Condo owner or HOA board", "Business owner", "Property manager", "Contractor", "Attorney", "Other"]
    towns = [l["city"] for l in LOCATIONS] + ["Elsewhere in Maine"]
    return f"""<form class="form" action="/api/contact.php" method="post" data-lead novalidate>
<h{hlevel} class="form-t">{e(heading)}</h{hlevel}><p class="form-sub">Free review, no obligation. We usually reply within one business day.</p>
<div class="fgrid">
<div><label for="f-name">Full name *</label><input id="f-name" name="name" autocomplete="name" required></div>
<div><label for="f-phone">Phone *</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="full"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
<div><label for="f-role">I am a…</label><select id="f-role" name="role">{_opt(roles)}</select></div>
<div><label for="f-loss">Type of loss</label><select id="f-loss" name="loss">{_opt(LOSSES)}</select></div>
<div><label for="f-city">Property location</label><select id="f-city" name="city">{_opt(towns)}</select></div>
<div><label for="f-amt">Rough amount in dispute</label><select id="f-amt" name="amount"><option>Not sure</option><option>Under $10,000</option><option>$10,000–$25,000</option><option>$25,000–$75,000</option><option>$75,000–$250,000</option><option>Over $250,000</option></select></div>
<div class="full"><label for="f-car">Insurance company (optional)</label><input id="f-car" name="carrier"></div>
<div class="full"><label for="f-det">What happened, and where does the claim stand?</label><textarea id="f-det" name="details" rows="4" placeholder="Date of loss, what the carrier paid or offered, and what you think was missed."></textarea></div>
<div class="full hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="{e(page)}">
<div class="full"><label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim by phone, text or email. Sending this form doesn’t create a client relationship. See the <a href="/privacy-practices/">privacy practices</a>.</span></label></div>
<div class="full"><button class="btn btn-navy full" type="submit">Send my claim details {ic("arrow")}</button></div>
</div>
<div class="form-msg" role="status"></div>
</form>"""


def hero_form():
    return f"""<form class="hform" action="/api/contact.php" method="post" data-lead novalidate>
<h2 class="hform-t">Get a free claim review</h2><p class="form-sub">Three fields. We call back within one business day.</p>
<div><label for="h-name">Name *</label><input id="h-name" name="name" autocomplete="name" required></div>
<div><label for="h-phone">Phone *</label><input id="h-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="h-loss">What happened?</label><select id="h-loss" name="loss">{_opt(LOSSES)}</select></div>
<div class="hp" aria-hidden="true"><label for="h-web">Website</label><input id="h-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="page" value="/ (hero)">
<label class="check"><input type="checkbox" name="consent" value="1" required> <span>I agree to be contacted about my claim. <a href="/privacy-practices/">Privacy</a>.</span></label>
<button class="btn btn-coral full" type="submit">Request my review {ic("arrow")}</button>
<div class="form-msg" role="status"></div>
<p class="hform-note">{ic("shield")}<span>No obligation. Your details stay private.</span></p>
</form>"""


# ---------------------------------------------------------------- home
SEASONS = [
    ("Winter", "Dec–Mar", "snow-roof", ["Ice dams behind gutters", "Snow load on flat and low roofs", "Frozen pipes at closed camps", "Chimney and wood-stove fires"],
     "Most Maine claim files open in the cold months, and many of them stay open until the snow comes off the roof."),
    ("Spring", "Apr–May", "flooded", ["Snowmelt leaks found late", "Roof damage revealed by thaw", "River ice and high water", "Basement water and sump failures"],
     "Thaw shows what winter hid. The roof that looked fine in February often shows the damage in April."),
    ("Summer", "Jun–Aug", "storm-clouds", ["Thunderstorm wind and microbursts", "Hail in the western hills", "Lightning strikes", "Trees on roofs and cars"],
     "Short, violent storms track across the interior and drop hardwoods and pines onto houses and camps."),
    ("Fall", "Sep–Nov", "storm-surf", ["Nor’easters and wind-driven rain", "Post-tropical storms", "Coastal surge and spray", "Early wet snow on leafy trees"],
     "Coastal storms and the remnants of tropical systems test siding, windows and shingles from Kittery to Eastport."),
]

REGIONS = [
    ("Southern Coast", "York County", "storm-surf", ["Coastal surge", "Nor’easters", "Older cottages"], "Kittery to Old Orchard Beach: beach cottages, brick mill conversions in Biddeford and Sanford, and condominiums in every town."),
    ("Greater Portland & Casco Bay", "Cumberland County", "portland-harbor", ["Record tides", "Triple-deckers", "Island access"], "Victorian brick, triple-deckers, waterfront commercial and island homes that need a ferry before the first shingle arrives."),
    ("Midcoast & Islands", "Sagadahoc · Lincoln · Knox · Waldo", "harbor-boats", ["Working wharves", "Wind exposure", "Sea-salt wear"], "Bath to Belfast: shipbuilding towns, harbors, capes and connected farmhouses, plus island homes off Rockland and Boothbay."),
    ("Down East & Acadia", "Hancock · Washington", "acadia-coast", ["Post-tropical wind", "Seasonal inns", "Remote pricing"], "Mount Desert Island inns and cottages, blueberry barrens and fishing towns where contractors travel long distances."),
    ("Kennebec Valley & Western Mountains", "Kennebec · Androscoggin · Franklin · Oxford · Somerset", "moose-mist", ["River flooding", "Snow load", "Ski condos"], "Augusta, Lewiston and Waterville mill cities, lake camps, and ski-area condominiums under heavy snow at Sugarloaf and Sunday River."),
    ("Penobscot Valley & The County", "Penobscot · Piscataquis · Aroostook", "farm-field", ["Deep cold", "Farm buildings", "Ice jams"], "Bangor’s Victorian neighborhoods, Moosehead camps and Aroostook farms with potato houses and metal outbuildings."),
]

STORMS = [
    ("1947", "October fires", "Wildfires burned across Mount Desert Island and southern York County, reshaping Bar Harbor."),
    ("1976", "Groundhog Day Gale", "A storm surge pushed up the Penobscot and flooded downtown Bangor."),
    ("1978", "February blizzard", "Set Portland’s tide record, 14.17 feet, which stood for 46 years."),
    ("1998", "The Ice Storm", "Ice-coated forests and power lines; parts of central and southern Maine were dark for weeks."),
    ("2017", "October windstorm", "A record number of Maine customers lost power as trees came down on roofs and wires."),
    ("2023", "December 18 storm", "Wind and heavy rain on snow sent the Kennebec and Androscoggin over their banks."),
    ("2024", "January coastal storms", "A new Portland tide record of 14.57 feet; wharves, fishing shacks and beach homes damaged."),
]


def home():
    steps = [
        ("Free estimate review", "We read your policy’s appraisal condition, the carrier’s full estimate and your photos, then tell you whether appraisal fits or another path is cheaper."),
        ("Independent scope and pricing", "On-site inspection and measurements, including the attic and the areas winter hides, and a line-item estimate priced for your part of Maine."),
        ("Written demand and appointment", "Appraisal is demanded in writing and Maine Insurance Appraiser is named as your appraiser within the time your policy allows."),
        ("Line-by-line reconciliation", "We work through each disputed line with the carrier’s appraiser. Many disagreements narrow sharply at this stage."),
        ("Umpire and signed award", "Items still in dispute go to a neutral umpire. Once two of the three sign, the amount of loss is set and payment follows under your policy."),
    ]
    stack = "".join(f'<li class="sstep" style="--i:{i}"><span class="sstep-n">{i + 1:02d}</span><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for i, (t, p) in enumerate(steps))

    seasons = "".join(
        f'<article class="season" tabindex="0">{img(ph, sizes="(max-width:900px) 100vw, 40vw", alt="")}<div class="season-in"><p class="season-when">{e(w)}</p><h3>{e(n)}</h3><p class="season-sum">{e(s)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in li)}</ul></div></article>'
        for n, w, ph, li, s in SEASONS)

    cards = "".join(
        f'<a class="scard rv" href="{SVC_BASE}{s["slug"]}/"><span class="scard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:600px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="scard-n">{i + 1:02d}</span></span><span class="scard-b"><h3>{e(s["name"])}</h3><span class="scard-p">{e(s["short"])}</span><span class="more">Read more {ic("arrow")}</span></span></a>'
        for i, s in enumerate(SERVICES))

    rail = "".join(
        f'<article class="rcard">{img(ph, sizes="(max-width:700px) 85vw, 380px", alt="")}<div class="rcard-b"><p class="kicker dark">{e(c)}</p><h3>{e(n)}</h3><ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in ch)}</ul><p>{e(t)}</p></div></article>'
        for n, c, ph, ch, t in REGIONS)

    tiles = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:600px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="tcard-k">{e(t["kind"])}</span></span><span class="tcard-b"><h3>{e(t["name"])}</h3><span>{e(t["short"])}</span></span></a>'
        for t in TOOLS)

    towns = "".join(f'<a class="town rv" href="{loc_path(l)}"><b>{e(l["city"])}</b><small>{e(l["county"])}</small>{ic("arrow")}</a>' for l in LOCATIONS)
    storms = "".join(f'<li class="rv"><span class="yr">{y}</span><div><h3>{e(n)}</h3><p>{e(t)}</p></div></li>' for y, n, t in STORMS)
    posts = "".join(post_card(p, "h3") for p in POSTS[:3])

    home_faqs = [
        ("What does a Maine Insurance Appraiser do on a claim?", "We value the damage when you and your insurer agree the loss is covered but disagree on what it costs. As your named appraiser we inspect, write an independent line-item estimate, reconcile it with the carrier’s appraiser and, if needed, present the open items to an umpire."),
        ("Is appraisal the same as hiring a public adjuster?", "No. A public adjuster handles and negotiates the whole claim. An appraiser works inside the policy’s appraisal condition on one question, the amount of loss, and doesn’t give legal advice."),
        ("When does it make sense to call a Maine Insurance Appraiser?", "When coverage is accepted, you have the carrier’s itemized estimate, and the gap between it and a contractor’s itemized number is meaningful, often more than about 10% or several thousand dollars."),
        ("Can appraisal fix a denied claim?", "Usually not. Appraisal sets the amount of a covered loss. Coverage denials and claims-handling complaints belong with a Maine attorney or the Bureau of Insurance."),
        ("How are fees handled?", "Each side pays its own appraiser and usually half the umpire. We put our fee in writing before work starts, and the first conversation is free."),
        ("Do you travel to islands and The County?", "Yes. We work in all 16 counties, including island properties reached by ferry and farms in Aroostook. Remote access is planned into the inspection, not avoided."),
    ]

    body = f"""
<section class="hero">
<div class="hero-media">{img("hero-coast", lazy=False, alt="")}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<p class="kicker">Statewide · All 16 counties · Islands included</p>
<h1><span class="h1-brand">Maine Insurance Appraiser</span><span class="h1-sub">for property claims that came up short</span></h1>
<p class="lede">Your insurer accepted the claim, but the check won’t rebuild the roof, the ceiling or the camp. Maine Insurance Appraiser prices the loss line by line and takes it through the appraisal process written into your policy.</p>
<div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn btn-line light" href="#work">See what we appraise</a></div>
</div>
{hero_form()}
</div>
</section>

<section class="ledger"><div class="wrap ledger-in">
<div class="rv"><p class="kicker dark">Why owners call</p><h2>Accepted is one word. <em>Paid in full</em> is another.</h2></div>
<div class="rv"><p>Most disputed Maine claims aren’t denials. They’re short: an attic that was never opened, a slope left off the roof report, ice-barrier membrane priced for one course when the eave needs three, clapboard that can’t be matched. A Maine Insurance Appraiser exists for the distance between the carrier’s number and the real cost to put the building back.</p>
<p>We build our own scope from the inspection, not from an edited copy of the carrier’s estimate, and we price what we can defend in front of an umpire.</p></div>
<dl class="counts">
<div><dt>Counties covered</dt><dd data-count="16">16</dd></div>
<div><dt>Kinds of appraisal work</dt><dd data-count="{len(SERVICES)}">{len(SERVICES)}</dd></div>
<div><dt>Free claim tools</dt><dd data-count="{len(TOOLS)}">{len(TOOLS)}</dd></div>
<div><dt>Signatures that bind an award</dt><dd>2 of 3</dd></div>
</dl>
</div></section>

<section class="sec" id="work"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Appraisal work</p><h2>Twelve kinds of claims a Maine Insurance Appraiser values</h2><p>Start with a review of the carrier’s estimate, or bring us in after appraisal has been demanded. Every service rests on the same thing: an independent, defensible number for your loss.</p></div>
<div class="scards" data-stagger>{cards}</div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">The Maine claim year</p><h2>What each season sends to a Maine Insurance Appraiser</h2><p>Weather here runs on a calendar. So do claims. Tap or hover a season to open it.</p></div>
<div class="seasons">{seasons}</div>
</div></section>

<section class="sec"><div class="wrap split">
<div class="split-l rv"><p class="kicker dark">How it moves</p><h2>Five stages from a short estimate to a binding number</h2><p>The appraisal condition turns an open-ended argument into a defined process with an end. Here’s how Maine Insurance Appraiser carries a file through it.</p><p><a class="link" href="{PROCESS}">Read the full appraisal path</a></p></div>
<ol class="sstack">{stack}</ol>
</div></section>

<section class="sec sec-navy"><div class="wrap split">
<div class="rv"><p class="kicker">Two numbers, one minute</p><h2>Check the size of your dispute</h2><p>Type the carrier’s estimate and your contractor’s. If the gap is wide, a call with a Maine Insurance Appraiser makes sense. If it’s narrow, a documented supplement may close it faster and for less.</p><p>The full <a href="{TOOL_BASE}settlement-gap-projector/">settlement gap projector</a> adds fees and shows the net at three possible award levels.</p></div>
<div class="rv">{GAP_MINI}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head left rv"><p class="kicker dark">Coast to County</p><h2>Six regions, six ways a Maine Insurance Appraiser prices a loss</h2><p>A Kennebunk beach cottage, a Lewiston triple-decker and a Presque Isle potato house don’t share a price list. Swipe through the regions.</p></div>
<div class="rail-wrap"><div class="rail" tabindex="0" aria-label="Maine regions">{rail}</div>
<div class="rail-nav"><button type="button" class="rail-btn" data-rail="-1" aria-label="Previous region">{ic("left")}</button><button type="button" class="rail-btn" data-rail="1" aria-label="Next region">{ic("right")}</button></div></div>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Claim math</p><h2>Free calculators from a Maine Insurance Appraiser</h2><p>Work through the numbers before you call. Every tool runs in your browser and nothing you type is stored or sent.</p></div>
<div class="tcards" data-stagger>{tiles}</div>
<p class="center mt"><a class="btn btn-navy" href="{TOOL_BASE}">Open all {len(TOOLS)} tools {ic("arrow")}</a></p>
</div></section>

<section class="sec"><div class="wrap split top">
<div class="rv"><p class="kicker dark">Storm record</p><h2>Weather years that still shape Maine claim files</h2><p>Adjusters and contractors still measure big events against these. A Maine Insurance Appraiser has to know what each one did to roofs, rivers and price lists.</p></div>
<ol class="storms" data-stagger>{storms}</ol>
</div></section>

<section class="sec sec-tint"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Where we work</p><h2>Maine Insurance Appraiser in towns across the state</h2><p>We inspect in every county. These are the places we’re called most often.</p></div>
<div class="towns" data-stagger>{towns}</div>
<p class="center mt"><a class="link" href="{LOC_BASE}">See every county we cover</a></p>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Fit check</p><h2>Good fits and poor fits for appraisal</h2><p>Maine Insurance Appraiser will tell you on the first call if your claim belongs somewhere else.</p></div>
<div class="fit">
<div class="fit-col yes rv"><h3>{ic("check")} Usually a good fit</h3><ul><li>Coverage accepted, cost disputed</li><li>Repair versus replace on a roof or floor</li><li>Matching siding, shingles or flooring that can’t be found</li><li>Missing trades, code items, ice barrier or overhead and profit</li><li>Depreciation that doesn’t match the age of the item</li></ul></div>
<div class="fit-col no rv"><h3>{ic("x")} Usually a poor fit</h3><ul><li>A full coverage denial</li><li>Claims-handling or bad-faith complaints</li><li>Gaps too small to justify the fees</li><li>Flood losses under a homeowners policy</li><li>A suit deadline that’s days away</li></ul></div>
</div>
</div></section>

<section class="sec sec-tint"><div class="wrap split top">
<div class="rv"><p class="kicker dark">Answers</p><h2>Questions owners ask a Maine Insurance Appraiser</h2><p>Short answers about the process, the cost and when appraisal is the wrong move.</p><div class="btn-row"><a class="btn btn-navy" href="{FAQ_P}">All answers {ic("arrow")}</a><a class="btn btn-line" href="{GLOSS}">Glossary</a></div></div>
<div class="rv">{faq_block(home_faqs)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head rv"><p class="kicker dark">Owner guides</p><h2>Worth reading before you demand appraisal</h2><p>Practical guides from Maine Insurance Appraiser on winter claims, policy wording and documentation.</p></div>
<div class="posts" data-stagger>{posts}</div>
<p class="center mt"><a class="link" href="{POST_BASE}">All owner guides</a></p>
</div></section>

<section class="pcta"><div class="pcta-media">{img("storm-clouds", alt="", extra=' data-parallax="0.16"')}</div><div class="wrap pcta-in rv"><p class="kicker">Before you sign the release</p><h2>A second look costs less than a settlement that won’t cover the work</h2><div class="btn-row"><a class="btn btn-coral" href="tel:{TEL}">{ic("phone")}<span>Call {PHONE}</span></a><a class="btn btn-line light" href="#contact">Send your estimate</a></div></div></section>

<section class="sec" id="contact"><div class="wrap contact">
<div class="rv"><p class="kicker dark">Start here</p><h2>Send your claim to a Maine Insurance Appraiser</h2><p>Tell us what happened and what the carrier offered. We’ll review it and give you a straight answer on whether appraisal is worth pursuing. No pressure and no obligation.</p>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Coverage</small><b>All 16 Maine counties and the islands</b></div></li></ul></div>
<div class="rv">{lead_form(page="/")}</div>
</div></section>
"""
    write("/", document("/", f"{BRAND} | Independent Claim Appraisal",
                        "Maine Insurance Appraiser: independent appraisal, estimate review and umpire work for underpaid ice dam, wind, water, tree and fire claims.",
                        body, [faq_schema(home_faqs)], photo="hero-coast", trail=[("Home", "/")], body_cls="is-home"), 1.0)


def post_card(p, h="h2"):
    nice = date.fromisoformat(p["date"]).strftime("%b %-d, %Y")
    return (f'<article class="post rv"><a class="post-ph" href="{POST_BASE}{p["slug"]}/" tabindex="-1" aria-hidden="true">{img(POST_PHOTO[p["slug"]], sizes="(max-width:700px) 100vw, 33vw", alt="")}</a>'
            f'<div class="post-b"><p class="meta">{nice} · {p["read"]} read</p><{h}><a href="{POST_BASE}{p["slug"]}/">{e(p["title"])}</a></{h}><p>{e(p["summary"])}</p></div></article>')


# ---------------------------------------------------------------- services
def service_pages():
    items = [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]
    for idx, s in enumerate(SERVICES):
        path = f'{SVC_BASE}{s["slug"]}/'
        trail = [("Home", "/"), ("Appraisal work", SVC_BASE), (s["name"], path)]
        rel = [SERVICES[(idx + k) % len(SERVICES)] for k in (1, 2, 3)]
        ph = SVC_PHOTO[s["slug"]]
        towns = [(l["city"], loc_path(l)) for l in LOCATIONS[:6]] + [("All Maine towns", LOC_BASE)]
        body = page_hero(trail, "Appraisal work", s["h1"], e(s["lede"]), ph, s["facts"]) + f"""
<div class="wrap layout"><article class="prose">{s["body"]}
<h2>Questions about {e(s["name"].lower())}</h2>{faq_block(s["faqs"])}
<h2>Related appraisal work</h2>{related([("Service", r["name"], f'{SVC_BASE}{r["slug"]}/') for r in rel])}
</article>
<aside class="aside">{call_box()}{list_box("All appraisal work", items, path)}{list_box("Towns we cover", towns)}</aside></div>
{cta_strip()}"""
        svc = {"@type": "Service", "name": s["name"], "serviceType": "Insurance appraisal", "description": s["desc"], "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "State", "name": "Maine"}, "url": DOMAIN + path, "image": f"{DOMAIN}/assets/img/photos/{ph}.webp"}
        write(path, document(path, s["title"], s["desc"], body, [svc, faq_schema(s["faqs"])], photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Appraisal work", SVC_BASE)]
    cards = "".join(
        f'<a class="icard rv" href="{SVC_BASE}{s["slug"]}/"><span class="icard-ph">{img(SVC_PHOTO[s["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><small>{i + 1:02d}</small><h2>{e(s["name"])}</h2><span>{e(s["short"])}</span></span></a>'
        for i, s in enumerate(SERVICES))
    body = page_hero(trail, "What we appraise", "Insurance Appraisal Services Across Maine",
                     "From a single estimate review to full representation on an appraisal panel and neutral umpire work, every Maine Insurance Appraiser service starts with an independent scope of the loss.", "roofer") + f"""
<section class="sec"><div class="wrap"><div class="icards" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split top"><div class="rv"><p class="kicker dark">Not sure where to start?</p><h2>Most files begin with an estimate review</h2><p>Before anyone demands appraisal, it helps to know exactly where the carrier’s estimate falls short and what that gap is worth. A review answers that in days, and some disputes close right there.</p><a class="btn btn-navy" href="{SVC_BASE}carrier-estimate-line-review/">About estimate reviews {ic("arrow")}</a></div>
<div class="rv">{faq_block([("Can I hire you for one part of the process?", "Yes. Many owners start with an estimate review and decide later whether to demand appraisal."), ("Do you handle commercial and condo claims?", "Yes. Houses, camps, condominium associations, apartment buildings, retail, offices, churches and farm buildings."), ("Do you work on claims outside southern Maine?", "Yes. We inspect in all 16 counties, including the islands and Aroostook County.")])}</div></div></section>
{cta_strip()}"""
    write(SVC_BASE, document(SVC_BASE, "Insurance Appraisal Services in Maine | 12 Types",
                             "Maine insurance appraisal services: appraisal clause representation, estimate review, ice dam, storm, water, fire and tree claims, plus umpires.",
                             body, [itemlist_schema(items)], photo="roofer", trail=trail, page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- towns
def location_pages():
    items = [(l["city"], loc_path(l)) for l in LOCATIONS]
    for l in LOCATIONS:
        path = loc_path(l)
        trail = [("Home", "/"), ("Towns we cover", LOC_BASE), (l["city"], path)]
        ph = LOC_PHOTO[l["slug"]]
        near = related([("Nearby", LOC_BY[n]["city"], loc_path(LOC_BY[n])) for n in l["near"]])
        svc_links = "".join(f'<li><a href="{SVC_BASE}{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES if s["slug"] in (
            "ice-dam-snow-load-appraisal", "noreaster-hurricane-appraisal", "water-damage-loss-appraisal", "fallen-tree-limb-appraisal", "homeowner-dispute-appraisal", "carrier-estimate-line-review"))
        snap = f"""<div class="snap"><h2>{e(l["city"])} at a glance</h2><dl>
<div><dt>County</dt><dd>{e(l["county"])}</dd></div><div><dt>Region</dt><dd>{e(l["region"])}</dd></div>
<div class="wide"><dt>Neighborhoods and villages</dt><dd><ul class="chips">{"".join(f"<li>{e(n)}</li>" for n in l["neighborhoods"])}</ul></dd></div>
<div class="wide"><dt>Housing mix</dt><dd>{e(l["housing"])}</dd></div>
<div class="wide"><dt>Common claim risks</dt><dd><ul class="chips coral">{"".join(f"<li>{e(p)}</li>" for p in l["perils"])}</ul></dd></div></dl>
<h3>Storms on record</h3><ol class="mini-storms">{"".join(f"<li><b>{e(w)}</b><span><strong>{e(n)}.</strong> {e(t)}</span></li>" for w, n, t in l["storms"])}</ol></div>"""
        body = page_hero(trail, f'{l["region"]} · {l["county"]}', f'Insurance Appraiser in {l["city"]}, Maine', e(l["lede"]), ph,
                         [("County", l["county"]), ("Region", l["region"]), ("Inspections", "On site")]) + f"""
<div class="wrap layout"><article class="prose">{snap}
{l["body"]}
<h2>Appraisal work for {e(l["city"])} properties</h2>
<p>Every {BRAND} service is available in {e(l["city"])} and the surrounding towns, including:</p>
<ul>{svc_links}</ul>
<h2>{e(l["city"])} questions</h2>{faq_block(l["faqs"])}
<h2>Nearby towns</h2>{near}
</article>
<aside class="aside">{call_box()}{list_box("Towns we cover", items, path)}{list_box("Free claim math", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>
{cta_strip(f"Disputed claim in {l['city']}?", "Send the estimate and your photos. We’ll tell you what we see, line by line.")}"""
        svc = {"@type": "Service", "name": f"Insurance appraisal in {l['city']}, Maine", "serviceType": "Insurance appraisal", "provider": {"@id": DOMAIN + "/#business"},
               "areaServed": {"@type": "City", "name": l["city"], "containedInPlace": {"@type": "AdministrativeArea", "name": l["county"] + ", Maine"}}, "url": DOMAIN + path}
        write(path, document(path, l["title"], l["desc"], body, [svc, faq_schema(l["faqs"])], photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Towns we cover", LOC_BASE)]
    cards = "".join(
        f'<a class="icard rv" href="{loc_path(l)}"><span class="icard-ph">{img(LOC_PHOTO[l["slug"]], sizes="(max-width:700px) 100vw, 260px", alt="")}</span><span class="icard-b"><small>{e(l["county"])}</small><h2>{e(l["city"])}</h2><span>{e(", ".join(l["perils"][:3]))}</span></span></a>'
        for l in LOCATIONS)
    counties = ["Androscoggin", "Aroostook", "Cumberland", "Franklin", "Hancock", "Kennebec", "Knox", "Lincoln", "Oxford", "Penobscot", "Piscataquis", "Sagadahoc", "Somerset", "Waldo", "Washington", "York"]
    reg = "".join(f'<div class="rlist-i rv"><h3>{e(n)}</h3><p class="meta">{e(c)}</p><p>{e(t)}</p></div>' for n, c, _p, _ch, t in REGIONS)
    body = page_hero(trail, "Statewide coverage", "Insurance Appraisal in All 16 Maine Counties",
                     "Maine Insurance Appraiser inspects from York County to the St. John Valley, including island homes reached by ferry. These pages cover the towns where we’re called most often.", "portland-harbor") + f"""
<section class="sec"><div class="wrap"><div class="icards" data-stagger>{cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap split top"><div class="rv"><p class="kicker dark">Counties</p><h2>Every county, not just the coast</h2><p>We cover all sixteen:</p><ul class="chips big">{"".join(f"<li>{c}</li>" for c in counties)}</ul></div>
<div class="rlist">{reg}</div></div></section>
{cta_strip("Don’t see your town?", "We cover every Maine county. Call and tell us where the property is.")}"""
    write(LOC_BASE, document(LOC_BASE, "Maine Towns We Cover | All 16 Counties",
                             "Insurance appraisal in all 16 Maine counties, including Portland, Lewiston, Bangor, Augusta, Biddeford, Rockland, Bar Harbor and Presque Isle.",
                             body, [itemlist_schema(items)], photo="portland-harbor", trail=trail, page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- tools
def tool_pages():
    items = [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]
    for i, t in enumerate(TOOLS):
        path = f'{TOOL_BASE}{t["slug"]}/'
        trail = [("Home", "/"), ("Claim math", TOOL_BASE), (t["name"], path)]
        ph = TOOL_PHOTO[t["slug"]]
        others = related([(o["kind"], o["name"], f'{TOOL_BASE}{o["slug"]}/') for o in [TOOLS[(i + k) % len(TOOLS)] for k in (1, 2, 3)]])
        body = page_hero(trail, f"Free {t['kind'].lower()} · runs in your browser", t["h1"], e(t["lede"]), ph, cta=False) + f"""
<section class="sec tool-sec"><div class="wrap">{t["markup"]}
<p class="hint fine">For planning only. Results depend on what you enter and on your policy, and aren’t a quote, an appraisal or legal advice.</p></div></section>
<div class="wrap layout"><article class="prose">{t["explain"]}
<h2>Questions about this tool</h2>{faq_block(t["faqs"])}
<h2>More claim math</h2>{others}</article>
<aside class="aside">{call_box()}{list_box("All claim math", items, path)}</aside></div>
{cta_strip("Want a professional to check the numbers?", "Send your estimate and we’ll review it line by line.")}"""
        app = {"@type": "WebApplication", "name": t["name"], "url": DOMAIN + path, "description": t["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
               "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": DOMAIN + "/#business"}}
        write(path, document(path, t["title"], t["desc"], body, [app, faq_schema(t["faqs"])], photo=ph, trail=trail), 0.8)

    trail = [("Home", "/"), ("Claim math", TOOL_BASE)]
    tiles = "".join(
        f'<a class="tcard rv" href="{TOOL_BASE}{t["slug"]}/"><span class="tcard-ph">{img(TOOL_PHOTO[t["slug"]], sizes="(max-width:600px) 100vw, (max-width:1100px) 50vw, 25vw", alt="")}<span class="tcard-k">{e(t["kind"])}</span></span><span class="tcard-b"><h2>{e(t["name"])}</h2><span>{e(t["short"])}</span></span></a>'
        for t in TOOLS)
    body = page_hero(trail, "Free and private", "Free Insurance Claim Calculators for Maine Owners",
                     "Seven calculators, planners and checks built from real appraisal work. Use them to understand your claim, test the carrier’s math and plan next steps. No sign-up, and nothing is stored.", "calc-docs", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="tcards" data-stagger>{tiles}</div></div></section>
<section class="sec sec-tint"><div class="wrap split top"><div class="rv"><p class="kicker dark">A sensible order</p><h2>Using the tools together</h2><ol class="steps-list"><li>Put your dates on a calendar with the <a href="{TOOL_BASE}claim-date-tracker/">claim date tracker</a>.</li><li>Own a camp or second home? Run the <a href="{TOOL_BASE}seasonal-camp-vacancy-check/">seasonal camp vacancy check</a>.</li><li>Check the roof quantities with the <a href="{TOOL_BASE}roof-pitch-squares-converter/">pitch and squares converter</a>.</li><li>See what you’re owed with the <a href="{TOOL_BASE}percent-deductible-checker/">deductible checker</a> and the <a href="{TOOL_BASE}rcv-acv-holdback-calculator/">holdback calculator</a>.</li><li>Size the dispute with the <a href="{TOOL_BASE}settlement-gap-projector/">settlement gap projector</a>.</li><li>Finish with the <a href="{TOOL_BASE}appraisal-file-strength-test/">file strength test</a>.</li></ol></div><div class="rv">{call_box()}</div></div></section>"""
    write(TOOL_BASE, document(TOOL_BASE, "Free Property Claim Calculators | Maine Owners",
                              "Free claim tools: settlement gap projector, RCV/ACV holdback, roof squares, percentage deductible, claim dates, file strength and camp vacancy.",
                              body, [itemlist_schema(items)], photo="calc-docs", trail=trail, page_type="CollectionPage"), 0.9)


# ---------------------------------------------------------------- learn
LEARN = [("The appraisal path", PROCESS), ("Answers (FAQ)", FAQ_P), ("Plain-English glossary", GLOSS), ("Owner guides", POST_BASE)]


def learn_pages():
    path = PROCESS
    trail = [("Home", "/"), ("The appraisal path", path)]
    steps = "".join(f'<li class="pstep" id="step-{i + 1}"><span class="pstep-n">{i + 1}</span><div><h3>{e(n)}</h3>{h}</div></li>' for i, (n, h) in enumerate(PROCESS_STEPS))
    toc = "".join(f'<li><a href="#step-{i + 1}">{e(n)}</a></li>' for i, (n, _h) in enumerate(PROCESS_STEPS))
    body = page_hero(trail, "Process guide", "How Insurance Appraisal Works in Maine, Step by Step",
                     "Seven stages from the first disagreement to a signed award: what happens, who does what, and where Maine claims most often go wrong.", "clipboard",
                     [("Stages", "7"), ("Panel", "2 appraisers + umpire"), ("Binding", "2 of 3 signatures")]) + f"""
<div class="wrap layout"><article class="prose">{PROCESS_INTRO}
<h2>The seven stages</h2><ol class="toc">{toc}</ol><ol class="psteps">{steps}</ol>
{PROCESS_OUTRO}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_strip()}"""
    howto = {"@type": "HowTo", "name": "How insurance appraisal works for a Maine property claim", "totalTime": "P120D",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "url": f"{DOMAIN}{path}#step-{i + 1}",
                       "text": _strip(h)} for i, (n, h) in enumerate(PROCESS_STEPS)]}
    write(path, document(path, "How Insurance Appraisal Works in Maine | 7 Stages",
                         "A step-by-step guide to insurance appraisal in Maine: the written demand, naming appraisers, choosing an umpire, reconciling and the award.",
                         body, [howto], photo="clipboard", trail=trail), 0.8)

    path = FAQ_P
    trail = [("Home", "/"), ("Answers", path)]
    jump = "".join(f'<a href="#faq-{i}">{e(g)}</a>' for i, (g, _q) in enumerate(FAQ))
    groups = "".join(f'<h2 id="faq-{i}">{e(g)}</h2>{faq_block(qs)}' for i, (g, qs) in enumerate(FAQ))
    allq = [qa for _, qs in FAQ for qa in qs]
    body = page_hero(trail, "Answers", "Insurance Appraisal Questions from Maine Owners",
                     f"{len(allq)} plain answers grouped by topic: the basics, cost and timing, Maine rules, winter and storm claims, and working with us.", "interior") + f"""
<div class="wrap layout"><article class="prose"><nav class="jump" aria-label="FAQ topics">{jump}</nav>{groups}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>{cta_strip("Didn’t see your question?", "Call or email. We’re glad to talk it through.")}"""
    write(path, document(path, "Insurance Appraisal FAQ | Maine Rules, Cost, Timing",
                         "Answers to common Maine insurance appraisal questions: how it works, cost and timing, Maine rules, winter claims and when the award binds.",
                         body, [faq_schema(allq)], photo="interior", trail=trail, page_type="FAQPage"), 0.8)

    path = GLOSS
    trail = [("Home", "/"), ("Glossary", path)]
    letters = sorted({t[0][0].upper() for t in GLOSSARY})
    az = "".join(f'<a href="#g-{c}">{c}</a>' for c in letters)
    dl, seen = "", set()
    for term, d in GLOSSARY:
        c = term[0].upper()
        anchor = f' id="g-{c}"' if c not in seen else ""
        seen.add(c)
        dl += f'<div class="gterm"{anchor}><dt>{e(term)}</dt><dd>{e(d)}</dd></div>'
    body = page_hero(trail, "Reference", "Plain-English Property Claim Glossary",
                     f"{len(GLOSSARY)} terms you’ll meet in policies, estimates and appraisal awards, from actual cash value to wind-driven rain, defined without jargon.", "calc-desk", cta=False) + f"""
<div class="wrap layout"><article class="prose"><div class="gfilter"><label for="gloss-q">Search the glossary</label><input id="gloss-q" type="search" placeholder="Try “ice dam” or “umpire”" autocomplete="off"><p class="hint" data-gcount>{len(GLOSSARY)} terms</p></div><nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{dl}</dl><p class="gnone" hidden>No terms match that search.</p></article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN, path)}</aside></div>"""
    dts = {"@type": "DefinedTermSet", "name": "Plain-English property claim glossary", "url": DOMAIN + path,
           "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "inDefinedTermSet": DOMAIN + path} for t, d in GLOSSARY]}
    write(path, document(path, "Property Claim Glossary | ACV, Umpire, Ice Dam",
                         "Plain-English definitions of property claim terms: actual cash value, replacement cost, depreciation, umpire, ice dam, puffback and many more.",
                         body, [dts], photo="calc-desk", trail=trail), 0.7)

    for p in POSTS:
        path = f'{POST_BASE}{p["slug"]}/'
        trail = [("Home", "/"), ("Owner guides", POST_BASE), (p["title"], path)]
        i = POSTS.index(p)
        others = related([("Guide", o["title"], f'{POST_BASE}{o["slug"]}/') for o in [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]])
        nice = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
        ph = POST_PHOTO[p["slug"]]
        body = page_hero(trail, f"Owner guide · {p['read']} read · {nice}", p["title"], e(p["summary"]), ph, cta=False) + f"""
<div class="wrap layout"><article class="prose">{p["body"]}<h2>Keep reading</h2>{others}</article>
<aside class="aside">{call_box()}{list_box("Learn", LEARN)}{list_box("Free claim math", [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS[:4]])}</aside></div>{cta_strip()}"""
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "keywords": p["keyword"],
               "image": f"{DOMAIN}/assets/img/photos/{ph}.webp", "url": DOMAIN + path}
        write(path, document(path, p["seo"], p["desc"], body, [art], og_type="article", photo=ph, trail=trail), 0.7)

    path = POST_BASE
    trail = [("Home", "/"), ("Owner guides", path)]
    body = page_hero(trail, "Owner guides", "Maine Property Claim Guides for Owners",
                     "Practical reading on ice dams, camps, coastal storms, puffback and policy wording, written from the appraisal side of the table.", "snow-roof", cta=False) + f"""
<section class="sec"><div class="wrap"><div class="posts" data-stagger>{"".join(post_card(p) for p in POSTS)}</div></div></section>{cta_strip()}"""
    write(path, document(path, "Maine Property Claim Guides | Owner Reading",
                         "Guides for Maine property owners on ice dam claims, the appraisal clause, camp freeze losses, nor’easter wind vs flood and oil burner puffback.",
                         body, [itemlist_schema([(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS])], photo="snow-roof", trail=trail, page_type="CollectionPage"), 0.7)


def _strip(h):
    import re
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


# ---------------------------------------------------------------- company & legal
def company_pages():
    path = ABOUT
    trail = [("Home", "/"), ("Our approach", path)]
    body = page_hero(trail, "Our approach", "How Maine Insurance Appraiser Works",
                     "We’re an appraisal and estimating practice built around one question on a disputed claim: what does it really cost to put this building back?", "plans-review") + f"""
<div class="wrap layout"><article class="prose">
<figure class="lead-img">{img("roofer", sizes="(max-width:1020px) 100vw, 760px")}</figure>
<h2>One question, answered well</h2>
<p>Many claim professionals do a bit of everything. Maine Insurance Appraiser chose to stay narrow. We work on the amount of loss, and we built our inspections, estimates and reports around answering that question in a way an umpire can follow. That lets us serve as your named appraiser, review an estimate before a dispute hardens, or sit as a neutral umpire on a panel where we represent neither side.</p>
<h2>What that looks like on a file</h2>
<ul>
<li><strong>Our own scope first.</strong> We inspect and measure before we study anyone else’s numbers, and we open up what winter hides: attics, soffits, wall cavities and decking.</li>
<li><strong>Defensible over dramatic.</strong> An inflated estimate looks good for a week and loses credibility with the umpire. We price what we can support with photos, measurements and local costs.</li>
<li><strong>Maine pricing realities.</strong> Island access, winter work, travel to The County, short building seasons and scarce trades after a big storm all belong in an honest number.</li>
<li><strong>Plain reporting.</strong> You’ll understand every difference between our valuation and the carrier’s.</li>
<li><strong>Fees in writing.</strong> You know what the work costs before it starts.</li>
</ul>
<h2>Who calls us</h2>
<p>Homeowners, camp and cottage owners, condominium boards, landlords, business owners, churches, farms, contractors and attorneys across Maine. On any one claim we serve in a single role, and we disclose prior relationships with the other appraiser or the umpire.</p>
<h2>What we don’t do</h2>
<p>We aren’t a law firm and don’t give legal advice. We don’t act as public adjusters or negotiate claims outside the appraisal process. We don’t decide coverage, and no honest appraiser promises a result. When a claim needs an attorney or a complaint to the Maine Bureau of Insurance, we say so on the first call.</p>
<h2>Statewide on purpose</h2>
<p>A claim in Kittery and a claim in Fort Kent share a policy form and very little else. Working all 16 counties means we see the full range of what Maine weather does to buildings, from salt-driven rain on the Midcoast to snow loads in the western mountains, and we price each with local knowledge.</p>
</article><aside class="aside">{call_box()}{list_box("Explore", [("Appraisal work", SVC_BASE), ("Towns we cover", LOC_BASE), ("Claim math", TOOL_BASE), ("The appraisal path", PROCESS)])}</aside></div>{cta_strip()}"""
    write(path, document(path, "Our Approach | Maine Insurance Appraiser",
                         "How Maine Insurance Appraiser works: independent scope, defensible pricing, plain reporting and fees in writing on disputed property claims.",
                         body, [], photo="plans-review", trail=trail, page_type="AboutPage"), 0.7)

    path = CONTACT
    trail = [("Home", "/"), ("Reach us", path)]
    body = page_hero(trail, "Reach us", "Contact Maine Insurance Appraiser",
                     "Call, text, email or send your claim details below. The first conversation is free, and we’ll tell you honestly whether appraisal is likely to help.", "meeting", cta=False) + f"""
<section class="sec"><div class="wrap contact">
<div class="rv"><p class="kicker dark">Direct lines</p><h2>Talk to us directly</h2>
<ul class="lines"><li>{ic("phone")}<div><small>Call or text</small><a href="tel:{TEL}">{PHONE_INTL}</a></div></li><li>{ic("mail")}<div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li><li>{ic("clock")}<div><small>Hours</small><b>Mon–Fri, 8am–6pm ET</b></div></li><li>{ic("pin")}<div><small>Service area</small><b>All 16 Maine counties and the islands</b></div></li></ul>
<h3>Helpful to have ready</h3><ul class="ticks"><li>Your declarations page</li><li>The carrier’s full itemized estimate (PDF)</li><li>Letters and emails from the carrier</li><li>Photos and your contractor’s estimate</li></ul></div>
<div class="rv">{lead_form("Tell us about your claim", page=path)}</div></div></section>"""
    write(path, document(path, "Contact Maine Insurance Appraiser | (844) 537-1427",
                         f"Get a free review of a disputed Maine property claim. Call or text (844) 537-1427 or email {EMAIL} to reach us.",
                         body, [], photo="meeting", trail=trail, page_type="ContactPage"), 0.8)

    credits = "".join(
        f'<tr><td>{img(k, "credit-th", sizes="120px", alt="")}</td><td>{e(v["title"])}<br><small>{e(v.get("creator") or "Unknown")}</small></td><td>{"CC0 1.0" if v["license"] == "cc0" else "Public domain"}</td><td><a href="{e(v["landing"])}" rel="nofollow noopener" target="_blank">Source</a></td></tr>'
        for k, v in PHOTOS.items())
    upd = date.today().strftime("%B %-d, %Y")
    legal = {
        "/privacy-practices/": ("Privacy Practices", "What we collect on this site, how we use it, and your choices.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>What we collect</h2><p>When you send a form, call or email, we collect what you choose to give us, such as your name, phone, email, property location and details about your claim. Our web host also records standard technical data (IP address, browser type, pages requested) for security and performance.</p>
<h2>How we use it</h2><ul><li>To respond to you and review your claim.</li><li>To provide services you ask for.</li><li>To keep the site secure and working.</li></ul>
<p>We don’t sell personal information. We share it only with people who need it to help with your claim (with your permission), with providers who host our site and email, or when the law requires it.</p>
<h2>Claim tools</h2><p>Our calculators and checks run in your browser. What you type into them isn’t sent to us or stored on our servers.</p>
<h2>Cookies and analytics</h2><p>This site doesn’t set advertising cookies. Fonts load from Google Fonts, which may log standard request data under Google’s privacy policy. If we add website analytics, it will be used in aggregate to understand which pages help visitors.</p>
<h2>Text messages</h2><p>If you agree to be contacted by text, message and data rates may apply. Reply STOP to opt out at any time.</p>
<h2>Your choices</h2><p>You can ask us to see, correct or delete the information you’ve given us by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2><p>{BRAND} · <a href="tel:{TEL}">{PHONE_INTL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>"""),
        "/site-terms/": ("Site Terms", "The terms that apply when you use this website and its free claim tools.", f"""
<p><em>Last updated: {upd}</em></p>
<h2>Using this site</h2><p>By using this website you agree to these terms. The content is general information about insurance appraisal and property claims in Maine.</p>
<h2>No client relationship</h2><p>Reading the site, using a tool or sending a form doesn’t create an appraiser–client relationship. That begins only when we both sign a written engagement.</p>
<h2>No legal advice</h2><p>{BRAND} isn’t a law firm, and nothing here is legal advice. Policies differ, and laws and court decisions change. Consult a Maine attorney about legal questions.</p>
<h2>Tools and estimates</h2><p>Calculators give planning estimates from the information you enter. They aren’t appraisals, quotes or predictions of any claim outcome.</p>
<h2>Content and photos</h2><p>Site content, design and tools belong to {BRAND}. You may share links and print pages for personal use. Photographs are used under the licenses on our <a href="/photo-credits/">photo credits</a> page.</p>
<h2>Limitation of liability</h2><p>The site is provided “as is.” To the extent the law allows, we aren’t liable for decisions made based on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Maine.</p>"""),
        "/fine-print/": ("Disclaimer", "Important limits on the general information published on this website.", f"""
<h2>General information only</h2><p>This website is educational and general. It describes how insurance appraisal commonly works, but your policy’s wording controls. Read your own policy and its endorsements.</p>
<h2>Not legal advice, not a public adjuster</h2><p>{BRAND} provides appraisal, estimating and umpire services. We are not attorneys, we don’t give legal advice, and we don’t act as public adjusters or negotiate claims outside appraisal.</p>
<h2>No guaranteed results</h2><p>Every claim is different. Example figures on this site are illustrative and are not results for any real client. No appraiser can guarantee an award.</p>
<h2>Deadlines</h2><p>Policies contain deadlines for notice, proof of loss, depreciation recovery and lawsuits. Nothing here extends or changes a deadline. If one is close, talk with a Maine attorney promptly.</p>
<h2>Statutes, agencies and storms</h2><p>References to Maine statutes, the Bureau of Insurance and past weather events are for context. Check current law and facts with official sources such as the Maine Bureau of Insurance.</p>
<h2>Photographs</h2><p>Photos are royalty-free stock and public-domain images used for illustration. They don’t show our clients’ properties.</p>"""),
        "/photo-credits/": ("Photo Credits", "Sources and licenses for every photograph used on this website.", f"""
<p>Every photograph on this site is royalty-free: either dedicated to the public domain under <strong>Creative Commons CC0 1.0</strong> or a <strong>public-domain</strong> work, such as photos by U.S. government agencies. Attribution isn’t legally required, but we credit each photographer here with thanks. Photos are illustrative and don’t show our clients’ properties.</p>
<div class="table-wrap"><table class="credits"><thead><tr><th>Photo</th><th>Title / creator</th><th>License</th><th>Link</th></tr></thead><tbody>{credits}</tbody></table></div>"""),
    }
    for path, (title, lede, content) in legal.items():
        trail = [("Home", "/"), (title, path)]
        body = page_hero(trail, "Site information", title, lede, "harbor-boats", cta=False) + f'<div class="wrap layout"><article class="prose narrow">{content}</article><aside class="aside">{call_box()}</aside></div>'
        desc = f"{title} for {BRAND} ({HOST}): {lede}"
        write(path, document(path, f"{title} | {BRAND}", desc, body, [], photo="harbor-boats", trail=trail), 0.3)


def sitemap_pages():
    path = SITEMAP_P
    trail = [("Home", "/"), ("Page directory", path)]
    groups = [
        ("Main", [("Home", "/"), ("Our approach", ABOUT), ("Reach us", CONTACT)]),
        ("Appraisal work", [("All appraisal work", SVC_BASE)] + [(s["name"], f'{SVC_BASE}{s["slug"]}/') for s in SERVICES]),
        ("Towns we cover", [("All towns", LOC_BASE)] + [(f'{l["city"]}, Maine', loc_path(l)) for l in LOCATIONS]),
        ("Claim math", [("All tools", TOOL_BASE)] + [(t["name"], f'{TOOL_BASE}{t["slug"]}/') for t in TOOLS]),
        ("Learn", LEARN + [(p["title"], f'{POST_BASE}{p["slug"]}/') for p in POSTS]),
        ("Site information", [("Privacy practices", "/privacy-practices/"), ("Site terms", "/site-terms/"), ("Disclaimer", "/fine-print/"), ("Photo credits", "/photo-credits/")]),
    ]
    cols = "".join(f'<div class="dir rv"><h2>{e(g)}</h2><ul>{"".join(f"<li><a href=\"{p}\">{e(n)}</a></li>" for n, p in links)}</ul></div>' for g, links in groups)
    body = page_hero(trail, "Navigation", "Page Directory", f"Every page on {BRAND}, grouped by section.", "harbor-boats", cta=False) + f'<section class="sec"><div class="wrap dirs" data-stagger>{cols}</div></section>'
    write(path, document(path, f"Page Directory | {BRAND}", f"A complete directory of every page on {BRAND}: appraisal work, Maine towns, free claim tools, owner guides and answers.",
                         body, [], photo="harbor-boats", trail=trail), 0.3)

    body = f"""<section class="phero err"><div class="phero-media">{img("storm-surf", lazy=False, alt="")}</div><div class="wrap phero-in"><p class="kicker">Error 404</p><h1>This page went out with the tide</h1><p class="lede">The page you were looking for has moved or never existed. Try one of these instead.</p><div class="btn-row"><a class="btn btn-coral" href="/">Home</a><a class="btn btn-line light" href="{SVC_BASE}">Appraisal work</a><a class="btn btn-line light" href="{TOOL_BASE}">Claim math</a><a class="btn btn-line light" href="{CONTACT}">Reach us</a></div></div></section>"""
    write("/404.html", document("/404.html", f"Page Not Found | {BRAND}", "The requested page could not be found.", body, robots="noindex,follow", photo="storm-surf"), sitemap=False)


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


GUARD_PHP = r"""<?php
// Maine Insurance Appraiser - canonical-host guard. Required first by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = '__HOST__';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$mia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://__HOST__ - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . $mia_uri, true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory, keeping any query string.
if (preg_match('#^(.*/)index\.php$#', (string) strtok($mia_uri, '?'), $mia_m)) {
    $mia_q = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
    header('Location: ' . $mia_m[1] . $mia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
"""

INDEX_PHP = r"""<?php
// Maine Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly (running a directory's index.php)
// and routes "/" and unknown paths here.
require_once __DIR__ . '/_guard.php';
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode((string) strtok($uri, '?'));
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
if ($path === '/' || $path === '/index.php' || $path === '') {
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.php')) {
    $q = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    header('Location: ' . $path . '/' . $q, true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.php')) {
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
