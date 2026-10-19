#!/usr/bin/env python3
"""Build missouricityroofs.com (Missouri City Roofers) into dist/ and package a Hostinger upload zip.

    python3 build.py            # build dist/ + missouricityroofs-hostinger-upload.zip
    python3 check.py            # validate the build

Source layout:
    src/         static files copied verbatim (assets, PHP, icons)
    content/     page copy: blog/, services/, areas/ (JSON header + HTML body)
    build.py     layout, shared blocks, schema
    pages_home.py, pages_main.py   page templates
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import zipfile

from icons import ICONS

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CONTENT = os.path.join(ROOT, "content")
DIST = os.path.join(ROOT, "dist")
ZIP = os.path.join(ROOT, "missouricityroofs-hostinger-upload.zip")

SITE = "https://missouricityroofs.com"
DOMAIN = "missouricityroofs.com"
NAME = "Missouri City Roofers"
PHONE = "(512) 297-7580"
TEL = "+15122977580"
EMAIL = "info@missouricityroofs.com"
TODAY = dt.date(2026, 10, 19)
GEO = (29.6186, -95.5377)
ASSET_V = "1"

e = html.escape


def icon(name, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


IMG_SIZES = {}


def img(key, alt, cls="", eager=False):
    w, h = IMG_SIZES.get(key, (1600, 1067))
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


SERVICE_ORDER = ["roof-replacement-missouri-city-tx", "roof-repair-missouri-city-tx", "storm-hail-damage-missouri-city-tx",
                 "insurance-claim-help-missouri-city-tx", "metal-roofing-missouri-city-tx", "commercial-roofing-missouri-city-tx",
                 "gutters-missouri-city-tx"]
AREA_ORDER = ["roofing-sienna-tx", "roofing-sugar-land-tx", "roofing-stafford-tx", "roofing-pearland-tx",
              "roofing-fresno-tx", "roofing-richmond-tx"]

SERVICES, AREAS, POSTS = [], [], []


def cta_band(title="Free roof inspection in Missouri City",
             text="Photo report, plain-English findings and zero obligation. Most inspections are booked within a few days."):
    return (f'<aside class="cta-band" data-reveal><div class="cb-mark">{icon("clipboard")}</div><div><h3>{e(title)}</h3><p>{e(text)}</p></div>'
            f'<a class="btn" href="/free-roof-inspection/">Book it free {icon("arrow")}</a></aside>')


def prep_body(body):
    body = body.replace('<div class="cta-inline"></div>', cta_band())
    body = body.replace('<div class="callout">', '<div class="callout" data-reveal>')
    return body


def fmt_date(d):
    d = dt.date.fromisoformat(d)
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


# --------------------------------------------------------------------------- layout
NAV_TOOLS = [("/tools/roof-cost-calculator/", "Roof Cost Calculator"), ("/tools/roof-pitch-calculator/", "Roof Pitch & Area Calculator"),
             ("/tools/storm-damage-checklist/", "Storm Damage Self-Check")]

LOGO = (f'<a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark">{icon("roof")}</span>'
        f'<span class="logo-text"><b>Missouri City</b><small>Roofers</small></span></a>')


def nav_html(active):
    def a(href, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'
    svc = "".join(f"<li>{a('/services/' + s['slug'] + '/', s['name'])}</li>" for s in SERVICES)
    ars = "".join(f"<li>{a('/areas/' + s['slug'] + '/', s['name'])}</li>" for s in AREAS)
    tools = "".join(f"<li>{a(h, l)}</li>" for h, l in NAV_TOOLS)
    return f"""<nav class="nav" aria-label="Main">
<ul>
<li class="has-sub">{a('/services/', 'Services')}{icon('chevron', 'i caret')}<ul class="sub"><li>{a('/free-roof-inspection/', 'Free Roof Inspection')}</li>{svc}</ul></li>
<li class="has-sub">{a('/areas/', 'Service Areas')}{icon('chevron', 'i caret')}<ul class="sub"><li>{a('/', 'Missouri City, TX')}</li>{ars}</ul></li>
<li>{a('/weather/', 'Storm Watch')}</li>
<li class="has-sub">{a('/tools/', 'Tools')}{icon('chevron', 'i caret')}<ul class="sub">{tools}</ul></li>
<li>{a('/blog/', 'Blog')}</li>
<li>{a('/about/', 'About')}</li>
<li>{a('/contact/', 'Contact')}</li>
</ul></nav>"""


def mobile_menu_html(active):
    def a(href, label):
        cur = ' aria-current="page"' if active == href else ""
        return f'<a href="{href}"{cur}>{e(label)}</a>'

    def group(label, href, items, is_open):
        links = "".join(a(h, l) for h, l in items)
        return (f'<details class="mm-group"{" open" if is_open else ""}><summary>{e(label)}{icon("chevron")}</summary>'
                f'<div class="mm-sub">{a(href, "All " + label.lower())}{links}</div></details>')

    svc = [("/free-roof-inspection/", "Free Roof Inspection")] + [("/services/" + s["slug"] + "/", s["name"]) for s in SERVICES]
    ars = [("/", "Missouri City, TX")] + [("/areas/" + s["slug"] + "/", s["name"]) for s in AREAS]
    return f"""<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
<a class="mm-backdrop" href="#" data-menu-close tabindex="-1" aria-hidden="true"></a>
<div class="mm-panel" role="dialog" aria-modal="true" aria-label="Menu">
<div class="mm-head">{LOGO}<a class="mm-close" href="#" data-menu-close aria-label="Close menu">{icon("x")}</a></div>
<nav class="mm-body" aria-label="Mobile">
{a('/free-roof-inspection/', 'Free Roof Inspection')}
{group('Services', '/services/', svc, active.startswith('/services/'))}
{group('Service Areas', '/areas/', ars, active.startswith('/areas/'))}
{a('/weather/', 'Storm Watch: Live Weather')}
{group('Tools', '/tools/', list(NAV_TOOLS), active.startswith('/tools/'))}
{a('/blog/', 'Blog')}
{a('/about/', 'About')}
{a('/contact/', 'Contact')}
</nav>
<div class="mm-foot"><a class="btn" href="/free-roof-inspection/">Book a free inspection {icon("arrow")}</a>
<a class="btn btn-line" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div>
</div></div>"""


def footer_html():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES)
    ars = "".join(f'<li><a href="/areas/{s["slug"]}/">{e(s["name"])}</a></li>' for s in AREAS)
    return f"""<footer class="site-footer">
<div class="wrap foot-cta">
<p class="foot-big">Storm rolled through? <span>Get a straight answer about your roof.</span></p>
<div class="foot-cta-btns"><a class="btn btn-brass" href="/free-roof-inspection/">Free roof inspection {icon("arrow")}</a><a class="btn btn-line-light" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div>
</div>
<div class="wrap footer-grid">
<div class="foot-about">{LOGO}
<p>Local roofing for Missouri City, TX: free roof inspections, repairs, full replacements and storm damage documentation across Fort Bend County.</p>
<p class="foot-contact"><a href="tel:{TEL}">{icon("phone")} {PHONE}</a><a href="mailto:{EMAIL}">{icon("mail")} {EMAIL}</a></p>
</div>
<div><h4>Services</h4><ul><li><a href="/free-roof-inspection/">Free Roof Inspection</a></li>{svc}</ul></div>
<div><h4>Service Areas</h4><ul><li><a href="/">Missouri City, TX</a></li>{ars}</ul></div>
<div><h4>Resources</h4><ul>
<li><a href="/weather/">Storm Watch (Live Weather)</a></li><li><a href="/tools/">Homeowner Tools</a></li><li><a href="/blog/">Roofing Blog</a></li>
<li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact</a></li>
<li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li></ul></div>
</div>
<div class="wrap footer-bottom"><span>© <span data-year>{TODAY.year}</span> {NAME} · Missouri City, TX 77459 &amp; 77489</span>
<span>Texas law prohibits contractors from waiving or rebating insurance deductibles. We never do.</span></div>
</footer>
<div class="mobile-bar"><a href="tel:{TEL}">{icon("phone")} Call</a><a class="mb-main" href="/free-roof-inspection/">{icon("clipboard")} Free inspection</a></div>"""


def business_schema():
    return {
        "@type": "RoofingContractor",
        "@id": SITE + "/#business",
        "name": NAME,
        "url": SITE + "/",
        "telephone": "+1-512-297-7580",
        "email": EMAIL,
        "image": SITE + "/assets/img/og-image.jpg",
        "logo": SITE + "/web-app-manifest-512x512.png",
        "priceRange": "$$",
        "description": "Missouri City roofers offering free roof inspections, roof repair, roof replacement, storm and hail damage restoration and insurance claim documentation in Missouri City, TX.",
        "address": {"@type": "PostalAddress", "addressLocality": "Missouri City", "addressRegion": "TX", "postalCode": "77459", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "areaServed": [{"@type": "City", "name": n} for n in
                       ["Missouri City, TX", "Sienna, TX", "Sugar Land, TX", "Stafford, TX", "Pearland, TX", "Fresno, TX", "Richmond, TX"]],
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


# --------------------------------------------------------------------------- forms
SERVICE_OPTIONS = ["Free roof inspection", "Roof repair / leak", "Roof replacement", "Storm or hail damage", "Insurance claim help",
                   "Metal roofing", "Commercial roofing", "Gutters", "Other"]


def hidden_fields(form_name):
    return (f'<div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>'
            f'<input type="hidden" name="t" value=""><input type="hidden" name="page" value=""><input type="hidden" name="form" value="{e(form_name)}">')


def lead_form(form_id, heading="Book your free roof inspection", sub="Tell us where you are and we'll call to schedule. No cost, no pressure.",
              full=False, hlevel="h2", service=None, button="Request my free inspection"):
    opts = "".join(f'<option{" selected" if o == service else ""}>{e(o)}</option>' for o in SERVICE_OPTIONS)
    extra = ""
    if full:
        extra = f"""<div class="field"><label for="{form_id}-timing">Best timing</label><select id="{form_id}-timing" name="timing">
<option>As soon as possible</option><option>This week</option><option>Next week or later</option><option>Just researching</option></select></div>
<div class="field full"><label for="{form_id}-msg">What's going on with your roof? (optional)</label><textarea id="{form_id}-msg" name="message" placeholder="Water spot on the living room ceiling after Tuesday's storm; roof is around 15 years old..."></textarea></div>"""
    head = f'<{hlevel}>{e(heading)}</{hlevel}><p class="sub">{e(sub)}</p>' if heading else ""
    return f"""<form class="lead-form" action="/send.php" method="post" id="{form_id}">
{head}<div class="form-grid">
<div class="field"><label for="{form_id}-name">Full name *</label><input id="{form_id}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="{form_id}-phone">Phone *</label><input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="{form_id}-email">Email</label><input id="{form_id}-email" name="email" type="email" autocomplete="email"></div>
<div class="field"><label for="{form_id}-addr">Street address or ZIP</label><input id="{form_id}-addr" name="address" autocomplete="street-address"></div>
<div class="field{'' if full else ' full'}"><label for="{form_id}-svc">I need help with</label><select id="{form_id}-svc" name="service">{opts}</select></div>
{extra}
</div>
{hidden_fields(heading or form_id)}
<button class="btn btn-block" type="submit">{e(button)} {icon("arrow")}</button>
<div class="form-status" role="status" aria-live="polite"></div>
<p class="form-note">{icon("shield")} We'll only use your details to contact you about your roof. Never shared or sold.</p>
</form>"""


def quote_bar(form_id="quote-bar"):
    """Horizontal one-line lead form that sits under the homepage hero."""
    opts = "".join(f"<option>{e(o)}</option>" for o in SERVICE_OPTIONS)
    return f"""<form class="lead-form quote-bar" action="/send.php" method="post" id="{form_id}">
<div class="qb-label"><b>Free inspection</b><span>Reply within one business day</span></div>
<div class="field"><label for="{form_id}-name">Name *</label><input id="{form_id}-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="{form_id}-phone">Phone *</label><input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="field"><label for="{form_id}-addr">Address or ZIP</label><input id="{form_id}-addr" name="address" autocomplete="street-address"></div>
<div class="field"><label for="{form_id}-svc">Service</label><select id="{form_id}-svc" name="service">{opts}</select></div>
{hidden_fields("Homepage quote bar")}
<button class="btn btn-brass" type="submit">Book free {icon("arrow")}</button>
<div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def popup_html():
    return f"""<div class="popup" id="lead-popup" aria-hidden="true" hidden>
<div class="popup-backdrop" data-popup-close></div>
<div class="popup-card" role="dialog" aria-modal="true" aria-labelledby="popup-title">
<button class="popup-x" type="button" data-popup-close aria-label="Close">{icon("x")}</button>
<div class="popup-side"><span class="kicker">$0 · No obligation</span><p class="popup-title" id="popup-title">Is your roof storm-ready?</p>
<p>Get a free, photo-documented roof inspection from local Missouri City roofers.</p>
<ul class="ticks"><li>{icon("check")} Full roof &amp; attic check</li><li>{icon("check")} Photo report you keep</li><li>{icon("check")} Honest repair-or-replace advice</li></ul>
<a class="popup-phone" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div>
<div class="popup-form">{lead_form("popup-form", heading="Claim your free inspection", sub="Takes 30 seconds. We'll call to schedule.", hlevel="p", button="Get my free inspection")}</div>
</div></div>"""


# --------------------------------------------------------------------------- shared blocks
def faq_html(faqs, heading="Frequently asked questions", eyebrow="FAQ"):
    items = "".join(f'<details data-reveal><summary><span class="q-n">{i + 1:02d}</span>{e(f["q"])}{icon("chevron")}</summary><p>{e(f["a"])}</p></details>'
                    for i, f in enumerate(faqs))
    return (f'<section class="section sec-sage"><div class="wrap faq-wrap"><div class="sec-head" data-reveal><span class="kicker">{e(eyebrow)}</span>'
            f'<h2>{e(heading)}</h2><p>Still unsure? Call <a href="tel:{TEL}">{PHONE}</a> and talk it through with a roofer.</p></div><div class="faq">{items}</div></div></section>')


def final_cta(title="Get a straight answer about your roof", text=None, bg="home-dusk"):
    text = text or "Book a free roof inspection with local Missouri City roofers. You'll get photos of what we find, a plain-English explanation and an honest recommendation."
    return f"""<section class="cta-final">
<div class="wrap cta-final-grid">
<div class="cta-final-text" data-reveal><span class="kicker light">Free · No obligation</span><h2>{e(title)}</h2><p>{e(text)}</p>
<div class="actions"><a class="btn btn-brass" href="/free-roof-inspection/">Book free inspection {icon("arrow")}</a>
<a class="btn btn-line-light" href="tel:{TEL}">{icon("phone")} {PHONE}</a></div></div>
<div class="cta-final-img">{img(bg, "Missouri City home with a sound shingle roof")}</div>
</div></section>"""


def page_hero(crumbs, h1, lead, bg="storm-sky", eyebrow=None, meta=""):
    eb = f'<span class="kicker">{e(eyebrow)}</span>' if eyebrow else ""
    return f"""<section class="page-hero">
<div class="wrap ph-grid">
<div class="ph-text">{crumbs_html(crumbs)}<div data-reveal>{eb}<h1>{h1}</h1><p class="lead">{e(lead)}</p>{meta}</div></div>
<div class="ph-img">{img(bg, re.sub("<[^>]+>", "", html.unescape(h1)), eager=True)}</div>
</div></section>"""


def form_section(form_id, service=None, title="Book your free roof inspection", text=None):
    text = text or ("A Missouri City roofer walks your roof, photographs every issue and explains your options. "
                    "If there's storm damage, you'll see the evidence before you ever call your insurance company.")
    return f"""<section class="section"><div class="wrap form-split">
<div data-reveal><span class="kicker">Free roof inspections</span><h2>{e(title)}</h2><p>{e(text)}</p>
<ol class="mini-steps"><li><b>Request</b><span>Send the form or call {PHONE}.</span></li>
<li><b>Inspect</b><span>Roof surface, flashing, vents, gutters and attic.</span></li>
<li><b>Decide</b><span>Photo report and a written estimate. No pressure.</span></li></ol></div>
<div class="form-card" data-reveal>{lead_form(form_id, heading="Request your free inspection", hlevel="h3", service=service)}</div>
</div></section>"""


def aside_phone():
    return f"""<div class="box box-green"><span class="kicker light">Talk to a roofer</span><h3>Questions about a leak, a storm or a price?</h3>
<a class="big-phone" href="tel:{TEL}">{PHONE}</a><a class="btn btn-brass btn-block" href="/free-roof-inspection/">Book a free inspection</a></div>"""


# --------------------------------------------------------------------------- page shell
def page(path, title, desc, main, active=None, schema=(), og_image="og-image.jpg", og_type="website",
         scripts=(), noindex=False, extra_head="", popup=True):
    canonical = SITE + path
    graph = [business_schema(),
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
              "publisher": {"@id": SITE + "/#business"}}] + list(schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    js = "".join(f'<script src="/assets/js/{s}.js?v={ASSET_V}" defer></script>' for s in ("site",) + tuple(scripts))
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
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
<meta name="geo.placename" content="Missouri City">
<meta name="geo.position" content="{GEO[0]};{GEO[1]}">
<meta name="theme-color" content="#123d2f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="utility"><div class="wrap">
<span class="u-left">{icon("leaf")} Locally focused on Missouri City &amp; Fort Bend County<span class="u-hide"> · Free roof inspections</span></span>
<span class="u-right"><a class="u-hide" href="/weather/">{icon("cloud-rain")} Storm Watch</a><a href="tel:{TEL}">{icon("phone")} {PHONE}</a></span>
</div></div>
<header class="site-header"><div class="wrap">
{LOGO}
{nav_html(active or path)}
<a class="header-call" href="tel:{TEL}"><span class="hc-ico">{icon("phone")}</span><span><small>Call or text</small><b>{PHONE}</b></span></a>
<a class="menu-btn" href="#mobile-menu" data-menu-open role="button" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false">{icon("menu")}<span>Menu</span></a>
</div></header>
{mobile_menu_html(active or path)}
<main id="main">
{main}
</main>
{footer_html()}
{popup_html() if popup else ""}
{js}
</body>
</html>
"""


# --------------------------------------------------------------------------- output
def write(path, htmltext):
    rel = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if path.endswith(".html"):
        rel = path.strip("/")
    out = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # Relative asset paths so pages also render from an unzipped folder (404 is served at any depth, so it stays absolute).
    pre = "/" if rel == "404.html" else "../" * rel.count("/")
    htmltext = re.sub(r'(src|href)="/(assets/|favicon|apple-touch-icon|site\.webmanifest|web-app-manifest)',
                      lambda m: f'{m.group(1)}="{pre}{m.group(2)}', htmltext)
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
    imgdir = os.path.join(DIST, "assets", "img")
    for fn in os.listdir(imgdir):
        if fn.endswith(".webp"):
            out = os.popen(f'identify -format "%w %h" "{os.path.join(imgdir, fn)}"').read().split()
            if len(out) == 2:
                IMG_SIZES[fn[:-5]] = (int(out[0]), int(out[1]))

    build_home()
    build_main()

    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for p, m, pr in SITEMAP)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(DIST, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /includes/\nDisallow: /send.php\nDisallow: /thank-you/\n\nSitemap: {SITE}/sitemap.xml\n")

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(DIST):
            for fn in sorted(files):
                full = os.path.join(base, fn)
                z.write(full, os.path.relpath(full, DIST))
    n = sum(len(f) for _, _, f in os.walk(DIST))
    print(f"built {len(SITEMAP)} pages, {n} files -> {os.path.relpath(ZIP, ROOT)} ({os.path.getsize(ZIP) // 1024} KB)")


if __name__ == "__main__":
    import sys
    sys.modules["build"] = sys.modules[__name__]
    main()
