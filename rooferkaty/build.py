#!/usr/bin/env python3
"""Build rooferkaty.com (Katy Roofer) into dist/ and package a Hostinger upload zip.

    python3 build.py            # build dist/ + rooferkaty-hostinger-upload.zip
    python3 check.py            # validate the build

Source layout:
    src/         static files copied verbatim (assets, PHP, icons)
    content/     page copy: blog/, services/, areas/ (JSON header + HTML body)
    build.py     layout, page templates, homepage/tools/weather copy, schema
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "dist")
ZIP = os.path.join(ROOT, "rooferkaty-hostinger-upload.zip")

SITE = "https://rooferkaty.com"
NAME = "Katy Roofer"
PHONE = "(512) 297-7580"
TEL = "+15122977580"
TODAY = dt.date(2026, 10, 3)
GEO = (29.7858, -95.8245)
GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7JWYNK4EPC"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-7JWYNK4EPC');
</script>
"""

e = html.escape


# --------------------------------------------------------------------------- icons
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "hammer": '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6"/><path d="m20.9 11.7-1.3-1.3a2 2 0 0 1-.6-1.4V7.9l-2.3-2.3a5.5 5.5 0 0 0-3.9-1.6H9l.9.8a5.4 5.4 0 0 1 1.9 4.1v1.6l2 2h2.2c.5 0 1 .2 1.4.6l1.3 1.3"/>',
    "cloud-hail": '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="M16 14v2M8 14v2M16 20h.01M8 20h.01M12 16v2M12 22h.01"/>',
    "file-check": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>',
    "layers": '<path d="m12.8 2.2a2 2 0 0 0-1.6 0L2.6 6.1a1 1 0 0 0 0 1.8l8.6 3.9a2 2 0 0 0 1.6 0l8.6-3.9a1 1 0 0 0 0-1.8z"/><path d="m22 17.6-9.2 4.2a2 2 0 0 1-1.6 0L2 17.6"/><path d="m22 12.6-9.2 4.2a2 2 0 0 1-1.6 0L2 12.6"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.8 4-4 0-1.2-.6-2.3-1.8-3.3S7.1 6.6 7 5.3c-.1 1.3-1 2.6-2.2 3.6S3 11.1 3 12.3c0 2.2 1.8 4 4 4z"/><path d="M12.6 6.6A11 11 0 0 0 14 3c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.9 5"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "wind": '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2"/>',
    "cloud-rain": '<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2"/><path d="M16 14v6M8 14v6M12 16v6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "thermo": '<path d="M14 4v10.5a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "roof": '<path d="M2 13 12 4l10 9"/><path d="M5 11v9h14v-9"/><path d="M9 20v-5h6v5"/><path d="M16 6V3h3v6"/>',
    "alert": '<path d="m21.7 18-8-14a2 2 0 0 0-3.5 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3z"/><path d="M12 9v4M12 17h.01"/>',
}


def icon(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


IMG_SIZES = {}


def img(key, alt, cls="", eager=False, sizes="(max-width: 760px) 100vw, 50vw"):
    w, h = IMG_SIZES.get(key, (1200, 800))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{key}.webp" alt="{e(alt)}" width="{w}" height="{h}" {load}{c}>'


# --------------------------------------------------------------------------- content
def load_dir(kind):
    items = []
    folder = os.path.join(CONTENT, kind)
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(folder, fn), encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*(.*)$", raw, re.S)
        if not m:
            raise SystemExit(f"bad content header: {kind}/{fn}")
        meta = json.loads(m.group(1))
        meta["body"] = m.group(2).strip()
        meta.setdefault("slug", fn[:-5])
        items.append(meta)
    return items


SERVICE_ORDER = ["roof-replacement-katy-tx", "roof-repair-katy-tx", "storm-hail-damage-katy-tx", "insurance-claim-help-katy-tx",
                 "metal-roofing-katy-tx", "commercial-roofing-katy-tx", "gutters-katy-tx"]
AREA_ORDER = ["roofing-cinco-ranch-tx", "roofing-fulshear-tx", "roofing-brookshire-tx", "roofing-cypress-tx",
              "roofing-richmond-tx", "roofing-west-houston-tx"]

SERVICES, AREAS, POSTS = [], [], []


def cta_band(title="Free roof inspection in Katy", text="Photo-documented, honest advice, zero obligation. Most inspections are booked within a few days."):
    return (f'<div class="cta-band" data-reveal><div><h3>{e(title)}</h3><p>{e(text)}</p></div>'
            f'<a class="btn" href="/free-roof-inspection/">Book my free inspection {icon("arrow")}</a></div>')


def prep_body(body):
    body = body.replace('<div class="cta-inline"></div>', cta_band())
    body = re.sub(r'<div class="callout">', '<div class="callout" data-reveal>', body)
    return body


def fmt_date(d):
    d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


# --------------------------------------------------------------------------- layout
NAV_TOOLS = [("/tools/roof-cost-calculator/", "Roof Cost Calculator"), ("/tools/roof-pitch-calculator/", "Roof Pitch & Area Calculator"),
             ("/tools/storm-damage-checklist/", "Storm Damage Self-Check")]


def nav_html(active):
    def a(href, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'
    svc = "".join(f"<li>{a('/services/' + s['slug'] + '/', s['name'])}</li>" for s in SERVICES)
    ars = "".join(f"<li>{a('/areas/' + s['slug'] + '/', s['name'])}</li>" for s in AREAS)
    tools = "".join(f"<li>{a(h, l)}</li>" for h, l in NAV_TOOLS)
    return f"""<nav class="nav" id="nav" aria-label="Main">
<ul>
<li class="has-sub">{a('/services/', 'Services')}<ul class="sub">{svc}</ul></li>
<li>{a('/free-roof-inspection/', 'Free Inspection')}</li>
<li class="has-sub">{a('/areas/', 'Areas')}<ul class="sub"><li>{a('/', 'Katy, TX')}</li>{ars}</ul></li>
<li>{a('/weather/', 'Weather')}</li>
<li class="has-sub">{a('/tools/', 'Tools')}<ul class="sub">{tools}</ul></li>
<li>{a('/blog/', 'Blog')}</li>
<li>{a('/about/', 'About')}</li>
<li>{a('/contact/', 'Contact')}</li>
</ul></nav>"""


def mobile_menu_html(active):
    """Phone/tablet menu. Lives outside <header>: the header's backdrop-filter would trap a fixed panel inside it."""
    def a(href, label, sub=False):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'

    def group(label, href, items, is_open):
        links = "".join(a(h, l) for h, l in items)
        return (f'<details class="mm-group"{" open" if is_open else ""}><summary>{e(label)}{icon("chevron")}</summary>'
                f'<div class="mm-sub">{a(href, "All " + label.lower())}{links}</div></details>')

    svc = [("/free-roof-inspection/", "Free Roof Inspection")] + [("/services/" + s["slug"] + "/", s["name"]) for s in SERVICES]
    ars = [("/", "Katy, TX")] + [("/areas/" + s["slug"] + "/", s["name"]) for s in AREAS]
    tools = list(NAV_TOOLS)
    return f"""<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
<a class="mm-backdrop" href="#" data-menu-close tabindex="-1" aria-hidden="true"></a>
<div class="mm-panel" role="dialog" aria-modal="true" aria-label="Menu">
<div class="mm-head">{LOGO}<a class="mm-close" href="#" data-menu-close aria-label="Close menu">{icon("x")}</a></div>
<nav class="mm-body" aria-label="Mobile">
{a('/free-roof-inspection/', 'Free Roof Inspection')}
{group('Services', '/services/', svc, active.startswith('/services/'))}
{group('Service Areas', '/areas/', ars, active.startswith('/areas/'))}
{a('/weather/', 'Katy Weather')}
{group('Tools', '/tools/', tools, active.startswith('/tools/'))}
{a('/blog/', 'Blog')}
{a('/about/', 'About')}
{a('/contact/', 'Contact')}
</nav>
<div class="mm-foot"><a class="btn" href="/free-roof-inspection/">Book a free inspection {icon("arrow")}</a>
<a class="btn btn-ghost" href="tel:{TEL}">{icon("phone")} Call {PHONE}</a></div>
</div></div>"""


LOGO = (f'<a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark">{icon("roof")}</span>'
        f'<span>Katy <em>Roofer</em></span></a>')


def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    ars = "".join(f'<li><a href="/areas/{s["slug"]}/">{e(s["name"])}</a></li>' for s in AREAS)
    return f"""<footer class="site-footer">
<div class="wrap footer-grid">
<div>{LOGO}
<p>Local roofing for Katy, TX homeowners and businesses: free roof inspections, repairs, replacements and storm damage help across Harris, Fort Bend and Waller counties.</p>
<a class="footer-phone" href="tel:{TEL}">{icon("phone")} {PHONE}</a>
<p><a class="btn btn-sm" href="/free-roof-inspection/">Free Roof Inspection</a></p>
</div>
<div><h4>Services</h4><ul><li><a href="/free-roof-inspection/">Free Roof Inspection</a></li>{svc}</ul></div>
<div><h4>Service Areas</h4><ul><li><a href="/">Katy, TX</a></li>{ars}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="/about/">About Us</a></li><li><a href="/blog/">Roofing Blog</a></li><li><a href="/weather/">Katy Weather</a></li>
<li><a href="/tools/">Homeowner Tools</a></li><li><a href="/contact/">Contact</a></li>
<li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li></ul></div>
</div>
<div class="wrap footer-bottom"><span>© <span data-year>{TODAY.year}</span> {NAME}. Serving Katy, TX 77449 · 77450 · 77493 · 77494.</span>
<span>Texas law prohibits contractors from waiving or rebating insurance deductibles. We never do.</span></div>
</footer>
<div class="mobile-bar"><a class="btn btn-ghost" href="tel:{TEL}">{icon("phone")} Call now</a><a class="btn" href="/free-roof-inspection/">Free inspection</a></div>"""


def business_schema():
    return {
        "@type": "RoofingContractor",
        "@id": SITE + "/#business",
        "name": NAME,
        "url": SITE + "/",
        "telephone": "+1-512-297-7580",
        "image": SITE + "/assets/img/og-image.jpg",
        "logo": SITE + "/web-app-manifest-512x512.png",
        "priceRange": "$$",
        "description": "Katy roofer offering free roof inspections, roof repair, roof replacement, storm and hail damage restoration and insurance claim help in Katy, TX.",
        "address": {"@type": "PostalAddress", "addressLocality": "Katy", "addressRegion": "TX", "postalCode": "77494", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "areaServed": [{"@type": "City", "name": n} for n in
                       ["Katy, TX", "Cinco Ranch, TX", "Fulshear, TX", "Brookshire, TX", "Cypress, TX", "Richmond, TX", "Houston, TX"]],
        "makesOffer": {"@type": "Offer", "name": "Free Roof Inspection", "price": "0", "priceCurrency": "USD",
                       "url": SITE + "/free-roof-inspection/"},
    }


def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def crumbs_html(crumbs):
    items = "".join(
        f'<li><a href="{u}">{e(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{e(n)}</li>'
        for i, (n, u) in enumerate(crumbs))
    return f'<ol class="crumbs">{items}</ol>'


def page(path, title, desc, main, active=None, schema=(), og_image="og-image.jpg", og_type="website",
         scripts=(), noindex=False, preload=None, extra_head=""):
    canonical = SITE + path
    graph = [business_schema(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
              "publisher": {"@id": SITE + "/#business"}}] + list(schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    pre = f'<link rel="preload" as="image" href="/assets/img/{preload}.webp" fetchpriority="high">\n' if preload else ""
    js = "".join(f'<script src="/assets/js/{s}.js?v=7" defer></script>' for s in ("site",) + tuple(scripts))
    return f"""<!doctype html>
<html lang="en-US">
<head>
{GTAG}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/{og_image}">
<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="Katy">
<meta name="theme-color" content="#0b1626">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap">
{pre}<link rel="stylesheet" href="/assets/css/site.css?v=7">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<div class="topbar"><div class="wrap">
<div class="tb-left"><span class="pill">FREE</span><span>Free roof inspections for Katy homeowners · <span class="tb-hide">no cost, no obligation</span></span></div>
<div><span class="tb-hide">Call or text: </span><a href="tel:{TEL}">{PHONE}</a></div>
</div></div>
<header class="site-header"><div class="wrap">
{LOGO}
{nav_html(active or path)}
<div class="header-cta"><a class="btn btn-ghost btn-sm" href="tel:{TEL}">{icon("phone")} {PHONE}</a><a class="btn btn-sm" href="/free-roof-inspection/">Free Inspection</a></div>
<a class="menu-btn" href="#mobile-menu" data-menu-open role="button" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false">{icon("menu")}</a>
</div></header>
{mobile_menu_html(active or path)}
<main id="main">
{main}
</main>
{footer_html()}
{js}
</body>
</html>
"""


# --------------------------------------------------------------------------- shared blocks
SERVICE_OPTIONS = ["Free roof inspection", "Roof repair / leak", "Roof replacement", "Storm or hail damage", "Insurance claim help",
                   "Metal roofing", "Commercial roofing", "Gutters", "Other"]


def lead_form(form_id, heading="Book your free roof inspection", sub="Tell us where you are and we'll call to schedule. No cost, no pressure.",
              full=False, hlevel="h2", service=None):
    opts = "".join(f'<option{" selected" if o == service else ""}>{e(o)}</option>' for o in SERVICE_OPTIONS)
    extra = ""
    if full:
        extra = """<div class="field"><label for="{0}-timing">When is best?</label><select id="{0}-timing" name="timing">
<option>As soon as possible</option><option>This week</option><option>Next week or later</option><option>Just researching</option></select></div>
<div class="field full"><label for="{0}-msg">What's going on with your roof? (optional)</label><textarea id="{0}-msg" name="message" placeholder="Leak in the upstairs bedroom after the last storm, roof is about 14 years old..."></textarea></div>""".format(form_id)
    return f"""<form class="lead-form" action="/send.php" method="post" id="{form_id}">
<{hlevel}>{e(heading)}</{hlevel}>
<p class="sub">{e(sub)}</p>
<div class="form-grid">
<div class="field"><label for="{form_id}-name">Full name *</label><input id="{form_id}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="{form_id}-phone">Phone *</label><input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="{form_id}-email">Email</label><input id="{form_id}-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="{form_id}-addr">Street address or ZIP</label><input id="{form_id}-addr" name="address" autocomplete="street-address"></div>
<div class="field{'' if full else ' full'}"><label for="{form_id}-svc">I need help with</label><select id="{form_id}-svc" name="service">{opts}</select></div>
{extra}
</div>
<div class="hp" aria-hidden="true"><label for="{form_id}-web">Leave this empty</label><input id="{form_id}-web" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="t" value=""><input type="hidden" name="page" value=""><input type="hidden" name="form" value="{e(heading)}">
<button class="btn" type="submit">Get my free inspection {icon("arrow")}</button>
<div class="form-status" role="status" aria-live="polite"></div>
<p class="form-note">By submitting, you agree we may call or text you about your request. We never share your information.</p>
</form>"""


def faq_html(faqs, heading="Frequently asked questions"):
    items = "".join(f'<details data-reveal style="--d:{i*0.05:.2f}s"><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>'
                    for i, f in enumerate(faqs))
    return f'<section class="section section-soft"><div class="wrap"><div class="section-head"><span class="eyebrow">FAQ</span><h2>{e(heading)}</h2></div><div class="faq">{items}</div></div></section>'


def final_cta(title="Get a straight answer about your roof", text=None, bg="home-sunset"):
    text = text or "Book a free roof inspection with a local Katy roofer. You'll get photos of what we find, a plain-English explanation and an honest recommendation."
    return f"""<section class="section cta-final">
<div class="hero-bg" style="background-image:url(/assets/img/{bg}.webp)"></div>
<div class="wrap" data-reveal><span class="eyebrow">Free · No obligation</span><h2>{e(title)}</h2><p>{e(text)}</p>
<div class="hero-actions"><a class="btn" href="/free-roof-inspection/">Book free inspection {icon("arrow")}</a>
<a class="btn btn-outline-light" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div></div></section>"""


def page_hero(crumbs, h1, lead, bg="storm-clouds", eyebrow=None, meta=""):
    eb = f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else ""
    return f"""<section class="hero hero-page">
<div class="hero-bg" style="background-image:url(/assets/img/{bg}.webp)"></div>
<div class="wrap">{crumbs_html(crumbs)}<div data-reveal>{eb}<h1>{h1}</h1><p class="lead">{e(lead)}</p>{meta}</div></div></section>"""


def form_section(form_id, service=None, title="Book your free roof inspection", text=None):
    text = text or ("A Katy roofer will walk your roof, photograph every issue and explain your options. "
                    "If there's storm damage, we'll show you the evidence before you ever call your insurance company.")
    return f"""<section class="section"><div class="wrap split">
<div data-reveal="left"><span class="eyebrow">Free roof inspections</span><h2>{e(title)}</h2><p>{e(text)}</p>
<ul class="checks"><li>{icon("check-circle")}<span>Full roof, attic-side and gutter check</span></li>
<li>{icon("check-circle")}<span>Photo report you keep, whether you hire us or not</span></li>
<li>{icon("check-circle")}<span>Written estimate with itemized scope</span></li>
<li>{icon("check-circle")}<span>No pressure, no deductible games, no obligation</span></li></ul>
<a class="btn btn-ghost" href="tel:{TEL}">{icon("phone")} Prefer to talk? {PHONE}</a></div>
<div class="form-card" data-reveal="right">{lead_form(form_id, heading="Request your free inspection", hlevel="h3", service=service)}</div>
</div></section>"""


def aside_phone():
    return f"""<div class="box phone-box"><h3>Talk to a Katy roofer</h3><p style="margin:0">Questions about a leak, a storm or an estimate?</p>
<a class="big" href="tel:{TEL}">{PHONE}</a><a class="btn btn-light btn-sm" style="width:100%" href="/free-roof-inspection/">Book a free inspection</a></div>"""


# --------------------------------------------------------------------------- pages
def write(path, htmltext):
    rel = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if path.endswith(".html"):
        rel = path.strip("/")
    out = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Relative asset paths: images/CSS/JS load even from a local preview or a subfolder install.
    pre = "/" if rel == "404.html" else "../" * rel.count("/")  # 404 is served at any depth
    htmltext = re.sub(r'(src|href)="/(assets/|favicon|apple-touch-icon|site\.webmanifest|web-app-manifest)', lambda m: f'{m.group(1)}="{pre}{m.group(2)}', htmltext)
    htmltext = htmltext.replace("url(/assets/", f"url({pre}assets/")
    with open(out, "w", encoding="utf-8") as f:
        f.write(htmltext)


SITEMAP = []


def add(path, htmltext, lastmod=None, priority="0.7", sitemap=True):
    write(path, htmltext)
    if sitemap:
        SITEMAP.append((path, lastmod or TODAY.isoformat(), priority))


def main():
    from pages_home import build_home
    from pages_main import build_main
    svc = {s["slug"]: s for s in load_dir("services")}
    ars = {s["slug"]: s for s in load_dir("areas")}
    SERVICES[:] = [svc[s] for s in SERVICE_ORDER if s in svc]
    AREAS[:] = [ars[s] for s in AREA_ORDER if s in ars]
    POSTS[:] = sorted(load_dir("blog"), key=lambda p: p["date"], reverse=True)

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)
    for fn in os.listdir(os.path.join(DIST, "assets", "img")):
        if fn.endswith(".webp"):
            out = os.popen(f'identify -format "%w %h" "{os.path.join(DIST, "assets", "img", fn)}"').read().split()
            if len(out) == 2:
                IMG_SIZES[fn[:-5]] = (int(out[0]), int(out[1]))

    build_home()
    build_main()

    # sitemap + robots
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for p, m, pr in SITEMAP)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(DIST, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /includes/\nDisallow: /send.php\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")

    # zip for Hostinger (files at the zip root -> extract straight into public_html)
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(DIST):
            for fn in sorted(files):
                full = os.path.join(base, fn)
                z.write(full, os.path.relpath(full, DIST))
    n = sum(len(f) for _, _, f in os.walk(DIST))
    print(f"built {len(SITEMAP)} pages, {n} files -> {os.path.relpath(ZIP, ROOT)} ({os.path.getsize(ZIP)//1024} KB)")


if __name__ == "__main__":
    import sys
    sys.modules["build"] = sys.modules[__name__]
    main()
