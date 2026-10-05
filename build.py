#!/usr/bin/env python3
"""Static site generator for beltonbanners.com (Christina Dittman Creations).

Renders every page from the shared layout in this file plus the page data in
content/. Output is plain HTML (served by index.php on the host) plus the two
hand-written PHP files that live alongside it (index.php, contact.php).

    python3 build.py            # writes the site into ./ (repo root)
    python3 validate.py         # then check it
"""

import json
import os
import re
from datetime import date

from siteconfig import BIZ, NEARBY, FOOTER_SERVING, NAV, SIZES, TODAY
from content.creations import CREATIONS, CATEGORIES, CATEGORY_LABEL, BY_SLUG as CREATION
from content.occasions import OCCASIONS
from content.blog import POSTS
from content.legal import PRIVACY, TERMS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT
KW = "Belton Banners"
P = BIZ["phone_display"]
TEL = BIZ["phone_href"]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def url(path):
    return BIZ["origin"].rstrip("/") + path


def jsonld(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def img(slug, alt, cls="", sizes="(max-width: 700px) 100vw, 50vw", loading="lazy", width=None, height=None):
    """Responsive <img> for a gallery image rendered by build-assets."""
    base = f"/assets/img/gallery/{slug}"
    srcset = f"{base}-400.webp 400w, {base}-800.webp 800w, {base}.webp 1600w"
    if not os.path.exists(os.path.join(ROOT, "assets/img/gallery", f"{slug}-800.webp")):
        srcset = f"{base}.webp 1600w"
    dims = f' width="{width}" height="{height}"' if width and height else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{base}-800.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" '
            f'loading="{loading}" decoding="async"{dims}>')


def trim(text, n):
    """Cut a string at a word boundary so it fits in n characters."""
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0].rstrip(",;:") + "."


def pretty_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return date(y, m, d).strftime("%B %-d, %Y")


# --------------------------------------------------------------------------
# Shared chrome
# --------------------------------------------------------------------------

def head(page):
    canonical = url(page["path"])
    og_image = url(page.get("og_image", BIZ["og_image"]))
    schema = ",\n".join(page.get("schema", []))
    robots = page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    article = ""
    if page.get("published"):
        article = (f'<meta property="article:published_time" content="{page["published"]}">\n'
                   f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#2F1F10">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{BIZ['name']} | {KW}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page['title'])}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{og_image}">
{article}<meta name="geo.region" content="US-TX">
<meta name="geo.placename" content="{BIZ['city']}, {BIZ['state_long']}">
<meta name="geo.position" content="{BIZ['latitude']};{BIZ['longitude']}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&amp;family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,600&amp;family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=1">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{schema}
]}}
</script>
</head>
<body class="{page.get('body_class', '')}">
<a class="skip-link" href="#content">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
"""


def header(active=None, light=False):
    links = []
    for label, href in NAV:
        current = ' aria-current="page"' if href == active else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    links_html = "".join(links)
    return f"""<div class="site{' site--light' if light else ''}">
<div class="announcement"><div class="container">
<span class="announcement-copy"><span class="dot" aria-hidden="true"></span>{KW} &middot; hand-painted in {BIZ['city']}, {BIZ['state']} &middot; made to order</span>
<span class="announcement-links"><a href="tel:{TEL}">Call {P}</a><a href="sms:{TEL}">Text us</a></span>
</div></div>
<header class="site-header" id="top"><div class="container nav-wrap">
<a class="brand" href="/" aria-label="{BIZ['name']} home">
<img class="brand-logo" src="{BIZ['logo']}" alt="{BIZ['name']} logo" width="56" height="56">
<span class="brand-copy"><strong>{BIZ['name']}</strong><span>{KW} &middot; {BIZ['city']}, {BIZ['state']}</span></span>
</a>
<nav class="nav-links" id="primary-nav" aria-label="Primary">{links_html}
<a class="nav-cta" href="/contact-us/">Get a Quote</a></nav>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open navigation"><span></span><span></span><span></span></button>
</div></header>
<main id="content">
"""


def footer():
    occ_links = "".join(f'<a href="/custom-banners/{o["slug"]}/">{o["label"]}</a>' for o in OCCASIONS)
    return f"""</main>
<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div class="footer-about">
<a class="brand" href="/">
<img class="brand-logo" src="{BIZ['logo']}" alt="{BIZ['name']} logo" width="64" height="64" loading="lazy">
<span class="brand-copy"><strong>{BIZ['name']}</strong><span>{KW}</span></span>
</a>
<p>{BIZ['name']} specializes in custom hand-painted banners designed to make life’s most meaningful moments even more memorable. From weddings and birthdays to baby showers, engagements, graduations, church services and seasonal celebrations, each piece is thoughtfully crafted with care, creativity and attention to detail. Every banner is made to order in {BIZ['city']}, {BIZ['state_long']}.</p>
<p><strong>{FOOTER_SERVING}</strong></p>
</div>
<div>
<div class="footer-title">Custom Banners</div>
<div class="footer-links">{occ_links}<a href="/custom-banners/">All banner types</a></div>
</div>
<div>
<div class="footer-title">Quick Links</div>
<div class="footer-links">
<a href="/">Home</a>
<a href="/about-christina-dittman-creations/">About {BIZ['name']}</a>
<a href="/gallery/">Gallery</a>
<a href="/how-it-works/">How It Works</a>
<a href="/pricing-and-sizes/">Pricing &amp; Sizes</a>
<a href="/design-your-banner/">Design Your Banner</a>
<a href="/belton-banners/">{KW} in {BIZ['city']}, {BIZ['state']}</a>
<a href="/faq/">FAQ</a>
<a href="/blog/">Blog</a>
<a href="/contact-us/">Contact Us</a>
</div>
</div>
<div>
<div class="footer-title">Contact</div>
<div class="footer-links">
<a href="tel:{TEL}">Call: {P}</a>
<a href="sms:{TEL}">Text: {P}</a>
<a href="mailto:{BIZ['email']}">{BIZ['email']}</a>
<span>{BIZ['city']}, {BIZ['state_long']} &middot; {BIZ['county']}</span>
<span>Made to order &middot; local pickup and delivery by arrangement</span>
</div>
</div>
</div>
<div class="footer-bottom">
<span>&copy; Copyright {date.today().year} {BIZ['name']}. All Rights Reserved. {KW} &middot; {BIZ['city']}, {BIZ['state']}.</span>
<span class="footer-legal"><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-of-use/">Terms of Use</a><a href="/sitemap/">Sitemap</a></span>
</div>
</div></footer>
<a class="mobile-call" href="tel:{TEL}">Get a Banner Quote: {P}</a>
<div class="lightbox" id="lightbox" hidden aria-hidden="true" role="dialog" aria-label="Image viewer">
<button class="lb-close" type="button" aria-label="Close">&times;</button>
<button class="lb-prev" type="button" aria-label="Previous image">&#8249;</button>
<figure><img alt=""><figcaption></figcaption></figure>
<button class="lb-next" type="button" aria-label="Next image">&#8250;</button>
</div>
</div>
<script src="/assets/js/site.js?v=1" defer></script>
</body>
</html>
"""


def breadcrumbs(trail):
    parts = []
    for label, href in trail:
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb">{"<span class=sep>/</span>".join(parts)}</nav>'


def sub_hero(page, trail, eyebrow=None, lead=None, extra=""):
    return f"""<section class="sub-hero"><div class="container">
{breadcrumbs(trail)}
{f'<div class="eyebrow" data-reveal>{eyebrow}</div>' if eyebrow else ''}
<h1 class="display" data-reveal data-split>{page['h1']}</h1>
{f'<p class="lead" data-reveal>{lead}</p>' if lead else ''}
{extra}
</div><div class="sub-hero-art" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div></section>
"""


def section_head(eyebrow, heading, lead=None, center=True):
    return (f'<div class="section-head{" center" if center else ""}">'
            f'<div class="eyebrow" data-reveal>{eyebrow}</div>'
            f'<h2 data-reveal data-split>{heading}</h2>'
            f'{f"<p class=lead data-reveal>{lead}</p>" if lead else ""}</div>')


def faq_section(faqs, heading="Questions, answered", intro=None, eyebrow="FAQ"):
    items = "".join(
        f'<details class="faq-item" data-reveal style="--i:{i}"><summary><span>{q}</span><span class="faq-icon" aria-hidden="true"></span></summary><div class="faq-body"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs)
    )
    return f"""<section class="faq"><div class="container narrow">
{section_head(eyebrow, heading, intro)}
<div class="faq-list">{items}</div>
</div></section>
"""


def cta_band(heading=None, text=None):
    heading = heading or "Ready to create something beautiful?"
    text = text or f"Let’s turn your idea into a hand-painted banner you’ll love - and keep. {KW} are made to order by {BIZ['name']}."
    return f"""<section class="cta-band"><div class="container cta-inner">
<div data-reveal>
<h2 class="display">{heading}</h2>
<p>{text}</p>
</div>
<div class="cta-actions" data-reveal>
<a class="btn btn-light" href="/contact-us/">Order Your Custom Banner</a>
<a class="btn btn-ghost-light" href="tel:{TEL}">Get a Quote: {P}</a>
</div>
<div class="cta-art" aria-hidden="true"><span></span><span></span><span></span></div>
</section>
"""


def occasion_options(selected=None):
    opts = ['<option value="">Choose an occasion</option>']
    for o in OCCASIONS:
        s = " selected" if o["slug"] == selected else ""
        opts.append(f'<option{s}>{o["label"].replace(" Banners", "").replace(" & Scripture", "")}</option>')
    opts.append("<option>Engagement / Anniversary</option><option>Something else</option>")
    return "".join(opts)


def size_options(selected=None):
    return '<option value="">Not sure yet</option>' + "".join(
        f'<option{" selected" if s == selected else ""}>{esc(s)}</option>' for s in SIZES)


def contact_form(source, heading=None, intro=None, compact=False, occasion=None, product=None):
    heading = heading or "Tell us about your moment"
    intro = intro or ("Share the occasion, the date, the wording and any inspiration you have. "
                      f"You’ll hear back with a sketch direction and a quote.")
    product_field = (f'<input type="hidden" name="product" value="{esc(product)}">' if product else "")
    return f"""<section class="contact" id="contact"><div class="container contact-grid">
<div class="contact-copy" data-reveal>
<div class="eyebrow">Get a Banner Quote</div>
<h2 class="display">{heading}</h2>
<p>{intro}</p>
<div class="contact-meta">
<a href="tel:{TEL}"><span class="ico" aria-hidden="true">☎</span> Call: {P}</a>
<a href="sms:{TEL}"><span class="ico" aria-hidden="true">✉</span> Text: {P}</a>
<a href="mailto:{BIZ['email']}"><span class="ico" aria-hidden="true">@</span> {BIZ['email']}</a>
<span><span class="ico" aria-hidden="true">⌂</span> {BIZ['city']}, {BIZ['state_long']} &middot; serving {', '.join(NEARBY[:4])} and {BIZ['region']}</span>
</div>
<ul class="trust-list">
<li>Every banner sketched for approval before painting</li>
<li>Starting at $90-$100, quote confirmed up front</li>
<li>Local pickup or delivery around Belton by arrangement</li>
</ul>
</div>
<div class="contact-card" data-reveal>
<form class="quote-form" method="post" action="/contact.php" novalidate>
<input type="hidden" name="source" value="{esc(source)}">
{product_field}
<div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-grid">
<div class="field"><label for="{source}-name">Name</label><input id="{source}-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="{source}-phone">Phone Number</label><input id="{source}-phone" name="phone" type="tel" autocomplete="tel"></div>
<div class="field full"><label for="{source}-email">Email</label><input id="{source}-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="{source}-occasion">Occasion</label><select id="{source}-occasion" name="occasion">{occasion_options(occasion)}</select></div>
<div class="field"><label for="{source}-size">Size</label><select id="{source}-size" name="size">{size_options()}</select></div>
<div class="field"><label for="{source}-date">Event Date</label><input id="{source}-date" name="event_date" type="date"></div>
<div class="field"><label for="{source}-wording">Wording / Name on the banner</label><input id="{source}-wording" name="wording" type="text" placeholder="Happy Birthday Everly"></div>
<div class="field full"><label for="{source}-message">Message / Personalization Details</label><textarea id="{source}-message" name="message" rows="{3 if compact else 5}" placeholder="Colors, theme, hobbies, a verse, where it will hang, anything that helps..."></textarea></div>
</div>
<button class="btn btn-primary submit" type="submit"><span>Send My Request</span><span class="btn-arrow" aria-hidden="true">→</span></button>
<p class="form-status" role="status" aria-live="polite"></p>
<p class="form-note">By sending this form you agree to our <a href="/privacy-policy/">privacy policy</a>. Prefer to talk? Call or text {P}.</p>
</form>
</div>
</div></section>
"""


def creation_card(c, i=0, link=True, show_price=True):
    price = f'<span class="card-price">Starts at ${c["price"]}.00</span>' if show_price else ""
    inner = f"""<div class="card-media">{img(c['image'], c['alt'], sizes="(max-width: 700px) 100vw, 33vw")}<span class="card-tag">{CATEGORY_LABEL[c['category']]}</span></div>
<div class="card-body"><h3>{c['title']}</h3>{price}<span class="card-link">View banner →</span></div>"""
    if link:
        return f'<a class="creation-card" href="/creation/{c["slug"]}/" data-reveal data-tilt style="--i:{i % 6}" data-cat="{c["category"]}">{inner}</a>'
    return f'<div class="creation-card" data-reveal style="--i:{i % 6}" data-cat="{c["category"]}">{inner}</div>'


def post_card(p, i=0):
    return f"""<a class="post-card" href="/{p['slug']}/" data-reveal style="--i:{i}">
<div class="post-media">{img(p['image'], p['image_alt'], sizes="(max-width: 700px) 100vw, 33vw")}</div>
<div class="post-body">
<span class="post-meta">{pretty_date(p['published'])} &middot; {p['read_time']}</span>
<h3>{p['title']}</h3>
<p>{p['excerpt'][:160].rsplit(' ', 1)[0]}…</p>
<span class="card-link">Read more →</span>
</div></a>"""


# --------------------------------------------------------------------------
# Schema builders
# --------------------------------------------------------------------------

def org_schema():
    return jsonld({
        "@type": ["LocalBusiness", "Store"],
        "@id": url("/#business"),
        "name": BIZ["name"],
        "alternateName": [KW, "CDC Belton Banners"],
        "description": "Custom hand-painted banners for birthdays, weddings, baby showers, church services, graduations and seasonal celebrations, painted to order in Belton, Texas.",
        "url": url("/"),
        "telephone": P,
        "email": BIZ["email"],
        "logo": url(BIZ["logo"]),
        "image": url(BIZ["og_image"]),
        "priceRange": "$90 - $300",
        "founder": {"@type": "Person", "name": BIZ["founder"]},
        "address": {"@type": "PostalAddress", "addressLocality": BIZ["city"], "addressRegion": BIZ["state"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["latitude"], "longitude": BIZ["longitude"]},
        "areaServed": [{"@type": "City", "name": c} for c in [BIZ["city"]] + NEARBY],
        "knowsAbout": ["hand painted banners", "custom birthday banners", "wedding banners", "church banners", "scripture banners", "baby shower banners"],
        "sameAs": [],
    })


def website_schema():
    return jsonld({
        "@type": "WebSite", "@id": url("/#website"), "url": url("/"),
        "name": f"{BIZ['name']} | {KW}", "alternateName": KW,
        "publisher": {"@id": url("/#business")}, "inLanguage": "en-US",
    })


def webpage_schema(page, wtype="WebPage"):
    d = {"@type": wtype, "@id": url(page["path"]) + "#webpage", "url": url(page["path"]),
         "name": page["title"], "description": page["description"],
         "isPartOf": {"@id": url("/#website")}, "about": {"@id": url("/#business")},
         "inLanguage": "en-US", "dateModified": TODAY}
    if page.get("published"):
        d["datePublished"] = page["published"]
    return jsonld(d)


def breadcrumb_schema(trail):
    return jsonld({"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": re.sub("<[^>]+>", "", label),
         **({"item": url(href)} if href else {})}
        for i, (label, href) in enumerate(trail)]})


def faq_schema(faqs):
    return jsonld({"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub("<[^>]+>", "", q),
         "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]})


def service_schema(o):
    return jsonld({
        "@type": "Service", "@id": url(f"/custom-banners/{o['slug']}/") + "#service",
        "name": f"Hand-painted {o['label'].lower()}", "serviceType": o["label"],
        "provider": {"@id": url("/#business")},
        "areaServed": [{"@type": "City", "name": c} for c in [BIZ["city"]] + NEARBY],
        "url": url(f"/custom-banners/{o['slug']}/"),
        "offers": {"@type": "Offer", "priceCurrency": "USD", "price": "90", "priceSpecification": {"@type": "PriceSpecification", "minPrice": "90", "priceCurrency": "USD"}},
    })


def product_schema(c):
    return jsonld({
        "@type": "Product", "@id": url(f"/creation/{c['slug']}/") + "#product",
        "name": c["title"], "description": c["blurb"],
        "image": url(f"/assets/img/gallery/{c['image']}.webp"),
        "brand": {"@type": "Brand", "name": BIZ["name"]},
        "category": CATEGORY_LABEL[c["category"]] + " banners",
        "material": "Acrylic paint on kraft paper",
        "offers": {"@type": "Offer", "url": url(f"/creation/{c['slug']}/"), "priceCurrency": "USD",
                   "price": str(c["price"]), "availability": "https://schema.org/InStock",
                   "itemCondition": "https://schema.org/NewCondition",
                   "seller": {"@id": url("/#business")}},
    })


def article_schema(p):
    return jsonld({
        "@type": "BlogPosting", "@id": url(f"/{p['slug']}/") + "#article",
        "headline": p["title"], "description": p["description"],
        "image": url(f"/assets/img/gallery/{p['image']}.webp"),
        "datePublished": p["published"], "dateModified": p["modified"],
        "author": {"@type": "Person", "name": BIZ["founder"], "url": url("/about-christina-dittman-creations/")},
        "publisher": {"@id": url("/#business")},
        "mainEntityOfPage": url(f"/{p['slug']}/"),
        "keywords": p["keyword"], "inLanguage": "en-US",
    })


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

WRITTEN = []


def write(path, html):
    if path.endswith("/"):
        path = path + "index.html"
    full = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    WRITTEN.append(path)


PAGES = []  # (path, lastmod, priority) for sitemap.xml


def register(path, lastmod=None, priority="0.7"):
    PAGES.append((path, lastmod or TODAY, priority))


# --------------------------------------------------------------------------
# Interactive banner designer (used on the homepage and /design-your-banner/)
# --------------------------------------------------------------------------

def designer(full=False):
    presets = [
        ("birthday", "🎂 Birthday", "Happy Birthday", "Gabbie", "script", "kraft", "#F5F0E6", "sunflower", '48" x 30"'),
        ("wedding", "💍 Wedding", "Welcome to our", "Wedding", "serif", "cream", "#6B4A2B", "leaf", '60" x 30"'),
        ("baby", "🌙 Baby", "Over the moon for", "Baby Boy Orion", "script", "kraft", "#2E5AAC", "star", '48" x 30"'),
        ("scripture", "✝️ Scripture", "Love the Lord your God", "Mark 12:30", "script", "kraft", "#B4232C", "heart", '36" x 30"'),
        ("graduation", "🎓 Graduation", "Congrats Grad", "Class of 2026", "bold", "kraft", "#1A8084", "star", '48" x 30"'),
        ("fall", "🍂 Fall", "Happy Fall", "Y’all!", "script", "grey", "#A9C7E8", "pumpkin", '36" x 30"'),
    ]
    preset_btns = "".join(
        f'<button type="button" class="chip" data-preset data-p-line1="{esc(l1)}" data-p-line2="{esc(l2)}" data-p-style="{st}" data-p-paper="{pa}" data-p-ink="{ink}" data-p-motif="{mo}" data-p-size="{esc(sz)}">{label}</button>'
        for key, label, l1, l2, st, pa, ink, mo, sz in presets)
    inks = ["#F5F0E6", "#2F2F2F", "#B4232C", "#C0552B", "#F2C94C", "#5F8F3E", "#1A8084", "#2E5AAC", "#8A64A7", "#F4B6C2"]
    ink_btns = "".join(f'<button type="button" class="swatch" data-ink="{c}" style="--c:{c}" aria-label="Ink {c}"></button>' for c in inks)
    motifs = [("none", "None"), ("star", "Stars"), ("heart", "Hearts"), ("flower", "Flowers"), ("sunflower", "Sunflowers"),
              ("balloon", "Balloons"), ("pumpkin", "Pumpkins"), ("leaf", "Greenery"), ("cross", "Cross"), ("truck", "Trucks")]
    motif_btns = "".join(f'<button type="button" class="chip" data-motif="{k}">{v}</button>' for k, v in motifs)
    sizes = "".join(f'<option{" selected" if s == SIZES[2] else ""}>{esc(s)}</option>' for s in SIZES)
    return f"""<section class="designer" id="design"><div class="container">
{section_head("Interactive", "Design your banner, live", f"Pick an occasion, type the wording, choose paper, lettering and a motif. The preview updates as you go - then send it straight to {BIZ['founder']} as a quote request.")}
<div class="designer-grid" data-designer>
<div class="designer-controls" data-reveal>
<div class="ctl"><span class="ctl-label">Start from an occasion</span><div class="chips">{preset_btns}</div></div>
<div class="ctl two">
<label>Line one<input type="text" data-in-line1 maxlength="32" value="Happy Birthday"></label>
<label>Line two (name)<input type="text" data-in-line2 maxlength="24" value="Gabbie"></label>
</div>
<div class="ctl"><span class="ctl-label">Lettering</span><div class="chips" data-styles>
<button type="button" class="chip is-active" data-style="script">Script</button>
<button type="button" class="chip" data-style="bold">Bold block</button>
<button type="button" class="chip" data-style="serif">Elegant serif</button>
</div></div>
<div class="ctl"><span class="ctl-label">Paper</span><div class="chips" data-papers>
<button type="button" class="chip is-active" data-paper="kraft">Kraft</button>
<button type="button" class="chip" data-paper="cream">Cream</button>
<button type="button" class="chip" data-paper="grey">Grey</button>
<button type="button" class="chip" data-paper="black">Black</button>
</div></div>
<div class="ctl"><span class="ctl-label">Ink color</span><div class="swatches" data-inks>{ink_btns}</div></div>
<div class="ctl"><span class="ctl-label">Motif</span><div class="chips" data-motifs>{motif_btns}</div></div>
<div class="ctl two">
<label>Size<select data-in-size>{sizes}</select></label>
<label class="ctl-inline"><span>Wobble</span><input type="range" data-in-wobble min="0" max="10" value="4" aria-label="Hand-painted wobble"></label>
</div>
<div class="designer-actions">
<a class="btn btn-primary" href="{'#contact' if not full else '/contact-us/'}" data-send-design><span>Send this design for a quote</span><span class="btn-arrow" aria-hidden="true">→</span></a>
<button type="button" class="btn btn-ghost" data-shuffle>Surprise me</button>
</div>
</div>
<div class="designer-stage" data-reveal>
<div class="banner-preview" data-preview data-paper="kraft" data-style="script" data-motif="sunflower" style="--ink:#F5F0E6;--ratio:48/30;--wobble:4">
<span class="tape t1" aria-hidden="true"></span><span class="tape t2" aria-hidden="true"></span>
<span class="motif m1" aria-hidden="true"></span><span class="motif m2" aria-hidden="true"></span><span class="motif m3" aria-hidden="true"></span><span class="motif m4" aria-hidden="true"></span>
<div class="bp-text"><span class="bp-line1">Happy Birthday</span><span class="bp-line2">Gabbie</span></div>
</div>
<p class="designer-summary" data-summary>48" x 30" &middot; kraft paper &middot; script lettering &middot; sunflowers</p>
<p class="designer-note">This is a rough mock-up to get the conversation started. The real banner is sketched by hand and approved by you before painting.</p>
</div>
</div>
</div></section>
"""


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def build_home():
    page = {
        "path": "/",
        "title": f"{KW} | {BIZ['name']} | Hand-Painted in Belton, TX",
        "description": (f"{KW} by {BIZ['name']}: custom hand-painted banners for birthdays, weddings, baby showers, "
                        f"church and graduations, made to order in Belton, TX. From $90."),
        "body_class": "home",
    }
    faqs = [
        (f"What are {KW}?", f"{KW} is the name people use for the custom hand-painted banners made by {BIZ['name']} in Belton, Texas. Every banner is lettered and illustrated by hand on kraft paper - no printing, no templates."),
        ("How much does a custom hand-painted banner cost?", "Banners start at $90 to $100 depending on size and detail. You get a confirmed quote before any painting starts. See the pricing and sizes page for what affects the price."),
        ("How long does a banner take?", "Most banners take a few days to a couple of weeks, depending on size, complexity and the current queue. Two to three weeks ahead is a comfortable lead time; rush requests are often possible."),
        ("What sizes are available?", 'Standard sizes are 30" x 30", 36" x 30", 48" x 30", 60" x 30" and 36" x 60". Larger stage banners are possible on request.'),
        (f"Do you deliver {KW.lower()} outside Belton?", f"Yes. {BIZ['name']} serves Belton, Temple, Killeen, Harker Heights, Salado and the rest of Bell County, with pickup or delivery arranged when the banner is ready."),
        ("Can I keep the banner after the event?", "That is the whole point. Roll it (never fold it), store it dry, or frame it as wall art."),
        (f"How do I order {KW.lower()}?", f"Use the contact form, call or text {P}, or email {BIZ['email']} with the occasion, the date, the wording and the size you have in mind."),
    ]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), faq_schema(faqs)]

    why = [
        ("Truly custom designs", "Every banner is created from scratch based on your vision - never reused or templated.", "✎"),
        ("Hand-painted quality", "Each piece is painted by hand, giving it a unique, high-end feel you can’t replicate digitally.", "🖌"),
        ("Made with care", "Your event matters. Every detail is handled with precision, patience and intention.", "♥"),
        ("Designed to impress", "From photos to first impressions, your banner will stand out and elevate the whole event.", "✦"),
        ("Simple, stress-free process", "Share your idea, approve your design, and we take care of the rest.", "✓"),
        ("Local to Belton, TX", f"{KW} are painted right here in Bell County, with pickup or delivery around Belton, Temple and Killeen.", "⌂"),
    ]
    why_html = "".join(
        f'<article class="why-card" data-reveal data-tilt style="--i:{i}"><span class="why-icon" aria-hidden="true">{ic}</span><h3>{h}</h3><p>{t}</p></article>'
        for i, (h, t, ic) in enumerate(why))

    occ_html = "".join(
        f'<a class="occ-card" href="/custom-banners/{o["slug"]}/" data-reveal data-tilt style="--i:{i}"><span class="occ-icon" aria-hidden="true">{o["icon"]}</span><h3>{o["label"]}</h3><p>{o["intro"][:110].rsplit(" ", 1)[0]}…</p><span class="card-link">Explore →</span></a>'
        for i, o in enumerate(OCCASIONS))

    strip = "".join(
        f'<a class="strip-item" href="/creation/{c["slug"]}/" data-reveal style="--i:{i % 6}">{img(c["image"], c["alt"], sizes="(max-width: 700px) 80vw, 420px")}<span class="strip-caption"><strong>{c["title"]}</strong><span>Starts at ${c["price"]}.00</span></span></a>'
        for i, c in enumerate(CREATIONS[:12]))

    steps = [
        ("Share your idea", "Tell us the occasion, the date, the wording and anything you love. A vague idea is enough."),
        ("Sketch & approve", "Colors, lettering and layout take shape in a sketch you approve before any paint goes down."),
        ("Painted by hand", "Every letter and illustration is painted by hand on kraft paper in the Belton studio."),
        ("Pickup or delivery", "Your banner is finished, checked and ready for the party - rolled, never folded."),
    ]
    steps_html = "".join(
        f'<li class="step" data-reveal style="--i:{i}"><span class="step-num">{i + 1:02d}</span><h3>{h}</h3><p>{t}</p></li>'
        for i, (h, t) in enumerate(steps))

    posts_html = "".join(post_card(p, i) for i, p in enumerate(sorted(POSTS, key=lambda p: p["published"], reverse=True)[:3]))

    body = f"""
<section class="hero">
<div class="hero-bg" data-parallax="0.35" aria-hidden="true">{img('hero-bg', '', cls='hero-img', sizes='100vw', loading='eager')}</div>
<div class="hero-veil" aria-hidden="true"></div>
<canvas class="paint-canvas" aria-hidden="true"></canvas>
<div class="container hero-inner">
<div class="eyebrow light" data-reveal><img src="{BIZ['logo']}" alt="" width="28" height="28" aria-hidden="true"> {BIZ['name']} &middot; {KW}</div>
<h1 class="display hero-title" data-reveal data-split>Custom Hand-Painted <em class="stroke">{KW}</em> for Life’s Most Meaningful Moments</h1>
<p class="lead light" data-reveal>Weddings, birthdays, baby showers, church services, graduations and everything in between - lettered and illustrated by hand in Belton, Texas, made with care and designed just for you.</p>
<div class="hero-actions" data-reveal>
<a class="btn btn-primary btn-lg" href="/contact-us/"><span>Order Your Custom Banner</span><span class="btn-arrow" aria-hidden="true">→</span></a>
<a class="btn btn-ghost-light btn-lg" href="tel:{TEL}">Get a Quote: {P}</a>
</div>
<ul class="hero-stats" data-reveal>
<li><strong data-count="100" data-suffix="%">100%</strong><span>hand-painted</span></li>
<li><strong data-count="90" data-prefix="$">$90</strong><span>starting price</span></li>
<li><strong data-count="5">5</strong><span>standard sizes</span></li>
<li><strong>1</strong><span>artist, start to finish</span></li>
</ul>
</div>
<a class="scroll-cue" href="#intro" aria-label="Scroll down"><span></span></a>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
{"".join(f'<span>{w}</span><i>✦</i>' for w in ["Birthday banners", KW, "Wedding welcome signs", "Baby shower banners", "Children’s church banners", "Scripture verse banners", "Graduation banners", "Seasonal banners", KW, "Hand-lettered in Belton, TX"] * 2)}
</div></div>

<section class="intro" id="intro"><div class="container split">
<div class="split-media" data-reveal>
<div class="brush-frame" data-brush>{img('custom-hand-painted-birthday-banner-2', CREATION['custom-hand-painted-birthday-banner-2']['alt'], sizes='(max-width: 900px) 100vw, 50vw')}</div>
<div class="floating-card" data-parallax="-0.08"><img src="{BIZ['logo']}" alt="" width="72" height="72" aria-hidden="true"><div><strong>{BIZ['name']}</strong><span>{KW} &middot; est. in Belton, TX</span></div></div>
</div>
<div class="split-copy">
<div class="eyebrow" data-reveal>Made with heart, designed for your moment</div>
<h2 data-reveal data-split>Meet the artist behind {KW}</h2>
<p data-reveal>{BIZ['name']} was built on a love for art, celebration and meaningful details. Every one of our {KW.lower()} is carefully hand-painted to reflect your unique story - no templates, no shortcuts. Just thoughtful craftsmanship and designs made to stand out at the party and on the wall afterward.</p>
<p data-reveal>Based in Belton, Texas, {BIZ['founder']} paints birthday banners, wedding welcome signs, baby shower backdrops, children’s church and scripture banners, graduation banners and seasonal pieces for families, churches and businesses across Bell County.</p>
<div class="btn-row" data-reveal><a class="btn btn-dark" href="/about-christina-dittman-creations/">Learn more about us</a><a class="btn btn-ghost" href="/gallery/">See the gallery</a></div>
</div>
</div></section>

<section class="why"><div class="container">
{section_head("Why choose " + BIZ['name'] + "?", f"Why Belton chooses {KW}", "Printed banners are easy, fast and forgettable. A hand-painted banner is the piece people photograph, talk about and keep.")}
<div class="why-grid">{why_html}</div>
</div></section>

<section class="occasions"><div class="container">
{section_head("Custom banners for every occasion", f"{KW} for every celebration", "Six kinds of banners we paint most often. Don’t see yours? Every banner is custom - just ask.")}
<div class="occ-grid">{occ_html}</div>
</div></section>

<section class="gallery-strip"><div class="container">
{section_head("Gallery", f"{BIZ['name']} - {KW} gallery", "A few of the banners painted in the studio. Scroll sideways, tap to open.", center=False)}
<div class="strip-wrap"><div class="strip" data-strip>{strip}</div>
<div class="strip-nav"><button type="button" class="strip-btn" data-strip-prev aria-label="Scroll gallery left">‹</button><button type="button" class="strip-btn" data-strip-next aria-label="Scroll gallery right">›</button></div></div>
<p class="center" data-reveal><a class="btn btn-dark" href="/gallery/">See more creations</a></p>
</div></section>

{designer()}

<section class="process"><div class="container">
{section_head("How it works", "From idea to finished banner in four steps", f"Ordering {KW.lower()} is simple: you bring the moment, we bring the brushes.")}
<ol class="steps">{steps_html}</ol>
<p class="center" data-reveal><a class="btn btn-ghost" href="/how-it-works/">Read the full process</a></p>
</div></section>

<section class="local"><div class="container split reverse">
<div class="split-copy">
<div class="eyebrow" data-reveal>Belton, Texas</div>
<h2 data-reveal data-split>Hand-painted banners from Belton, for Central Texas</h2>
<p data-reveal>{KW} start in a home studio in Belton and end up at birthday parties in Temple, church classrooms in Killeen, wedding receptions in Salado and porches across Bell County. If you are within a short drive of Belton, pickup or delivery can be arranged when the banner is ready; if you are further away, ask - most things are possible.</p>
<ul class="check-list" data-reveal>
<li>Belton, Temple, Killeen, Harker Heights, Salado, Nolanville and Troy</li>
<li>Churches, schools, families and small businesses</li>
<li>Made to order - every quote confirmed before painting</li>
</ul>
<div class="btn-row" data-reveal><a class="btn btn-dark" href="/belton-banners/">{KW} in Belton, TX</a></div>
</div>
<div class="split-media" data-reveal>
<div class="brush-frame" data-brush>{img('custom-painted-verse-banner-5', CREATION['custom-painted-verse-banner-5']['alt'], sizes='(max-width: 900px) 100vw, 50vw')}</div>
</div>
</div></section>

{faq_section(faqs, f"{KW} - questions, answered", f"The questions we hear most about ordering custom hand-painted banners from {BIZ['name']}.")}

<section class="posts"><div class="container">
{section_head("Latest articles", "From the studio blog", "Ideas, wording tips and behind-the-scenes notes on hand-painted banners.")}
<div class="post-grid">{posts_html}</div>
<p class="center" data-reveal><a class="btn btn-ghost" href="/blog/">More articles</a></p>
</div></section>

{cta_band()}
{contact_form("home", heading="Ready for your own " + KW.lower() + "?", intro=f"Share the occasion, the date and the wording. {BIZ['founder']} will reply with a sketch direction and a quote - usually within a day.")}
"""
    write("/home.html", head(page) + header("/") + body + footer())
    register("/", priority="1.0")


def build_occasions_index():
    page = {
        "path": "/custom-banners/",
        "title": f"Custom Hand-Painted Banners for Every Occasion | {KW}",
        "description": f"Birthday, wedding, baby shower, church, graduation and seasonal banners, each painted by hand to order in Belton, TX by {BIZ['name']}. From $90.",
        "h1": "Custom banners for every occasion",
    }
    trail = [("Home", "/"), ("Custom Banners", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema(trail),
                      jsonld({"@type": "ItemList", "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "name": o["label"], "url": url(f"/custom-banners/{o['slug']}/")}
                          for i, o in enumerate(OCCASIONS)]})]
    cards = "".join(
        f"""<a class="occ-feature" href="/custom-banners/{o['slug']}/" data-reveal style="--i:{i % 3}">
<div class="occ-feature-media">{img(CREATION[o['gallery'][0]]['image'], CREATION[o['gallery'][0]]['alt'], sizes='(max-width: 700px) 100vw, 33vw')}</div>
<div class="occ-feature-body"><span class="occ-icon" aria-hidden="true">{o['icon']}</span><h2>{o['label']}</h2><p>{o['intro'][:150].rsplit(' ', 1)[0]}…</p><span class="card-link">See {o['nav_label'].lower()} banners →</span></div></a>"""
        for i, o in enumerate(OCCASIONS))
    body = sub_hero(page, trail, "Custom Banners", f"Every banner {BIZ['name']} paints is made to order, but most fall into one of six families. Pick yours to see examples, wording ideas and answers to common questions.") + f"""
<section class="section"><div class="container"><div class="occ-feature-grid">{cards}</div></div></section>
{designer(full=False)}
{cta_band("Have something else in mind?", "Anniversaries, retirements, business openings, school events - if it deserves a banner, it can be painted.")}
{contact_form("custom-banners")}
"""
    write(page["path"], head(page) + header("/custom-banners/") + body + footer())
    register(page["path"], priority="0.9")


def build_occasions():
    for o in OCCASIONS:
        path = f"/custom-banners/{o['slug']}/"
        page = {"path": path, "title": o["title"], "description": o["description"], "h1": o["h1"]}
        trail = [("Home", "/"), ("Custom Banners", "/custom-banners/"), (o["label"], None)]
        page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), service_schema(o), faq_schema(o["faqs"])]
        page["og_image"] = f"/assets/img/gallery/{CREATION[o['gallery'][0]]['image']}.webp"
        sections = "".join(
            f'<div class="prose-block" data-reveal><h2>{h}</h2>{"".join(f"<p>{p}</p>" for p in ps)}</div>' for h, ps in o["sections"])
        ideas = "".join(f'<li data-reveal style="--i:{i}"><span class="idea-mark" aria-hidden="true">✎</span>{esc(t)}</li>' for i, t in enumerate(o["ideas"]))
        gallery = "".join(creation_card(CREATION[s], i) for i, s in enumerate(o["gallery"]))
        others = "".join(f'<a class="pill" href="/custom-banners/{x["slug"]}/">{x["icon"]} {x["label"]}</a>' for x in OCCASIONS if x is not o)
        body = sub_hero(page, trail, o["label"], o["intro"]) + f"""
<section class="section"><div class="container prose-grid">
<div class="prose">{sections}
<div class="prose-block" data-reveal><h2>Wording ideas for {o['label'].lower()}</h2><ul class="idea-list">{ideas}</ul></div>
</div>
<aside class="sidebar">
<div class="side-card" data-reveal>
<h3>Order a {o['nav_label'].lower()} banner</h3>
<p>Starts at $90-$100. Sketch approved before painting. Pickup or delivery around Belton.</p>
<a class="btn btn-primary" href="#contact">Request a quote</a>
<a class="btn btn-ghost" href="tel:{TEL}">Call {P}</a>
</div>
<div class="side-card" data-reveal>
<h3>Standard sizes</h3>
<ul class="size-list">{"".join(f"<li>{esc(s)}</li>" for s in SIZES)}</ul>
<a class="text-link" href="/pricing-and-sizes/">Pricing &amp; sizes →</a>
</div>
<div class="side-card" data-reveal>
<h3>Other banner types</h3>
<div class="pills">{others}</div>
</div>
</aside>
</div></section>
<section class="section alt"><div class="container">
{section_head("From the gallery", f"{o['label']} we’ve painted", None, center=False)}
<div class="creation-grid">{gallery}</div>
<p class="center" data-reveal><a class="btn btn-dark" href="/gallery/">See the full gallery</a></p>
</div></section>
{faq_section(o['faqs'], f"{o['label']}: common questions")}
{contact_form(o['slug'], heading=f"Order your {o['nav_label'].lower()} banner", occasion=o['slug'])}
"""
        write(path, head(page) + header("/custom-banners/") + body + footer())
        register(path, priority="0.8")


def build_gallery():
    page = {
        "path": "/gallery/",
        "title": f"Gallery | Hand-Painted Banners | {KW}",
        "description": f"Browse hand-painted birthday, baby shower, church, scripture and seasonal banners by {BIZ['name']} in Belton, TX. Made to order from $90.",
        "h1": "Gallery of hand-painted banners",
    }
    trail = [("Home", "/"), ("Gallery", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema(trail),
                      jsonld({"@type": "ItemList", "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "name": c["title"], "url": url(f"/creation/{c['slug']}/")}
                          for i, c in enumerate(CREATIONS)]})]
    filters = '<button type="button" class="chip is-active" data-filter="all">All</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{k}">{v}</button>' for k, v in CATEGORIES)
    cards = "".join(creation_card(c, i) for i, c in enumerate(CREATIONS))
    body = sub_hero(page, trail, "Hand Painted Banners", f"Every banner here was painted by hand in Belton, Texas. Filter by occasion, tap a banner to see it closer, and use any of them as a starting point for your own.",
                    extra=f'<div class="filters" data-filters role="group" aria-label="Filter gallery">{filters}</div>') + f"""
<section class="section"><div class="container">
<div class="creation-grid" data-gallery>{cards}</div>
<p class="empty-note" data-empty hidden>No banners in this category yet - ask about one!</p>
</div></section>
{cta_band("Like what you see?", "Every banner in this gallery started as a quick message. Send yours and get a sketch direction and quote.")}
{contact_form("gallery")}
"""
    write(page["path"], head(page) + header("/gallery/") + body + footer())
    register(page["path"], priority="0.9")


def build_creations():
    n = len(CREATIONS)
    for i, c in enumerate(CREATIONS):
        path = f"/creation/{c['slug']}/"
        page = {
            "path": path,
            "title": f"{c['title']} | {BIZ['name']}",
            "description": trim(f"{c['blurb'].split('. ')[0].rstrip('.')}. Hand-painted to order in Belton, TX by {BIZ['name']}. Starts at ${c['price']}.", 160),
            "h1": c["title"],
            "og_image": f"/assets/img/gallery/{c['image']}.webp",
            "og_type": "product",
        }
        trail = [("Home", "/"), ("Hand Painted Banners", "/gallery/"), (c["title"], None)]
        page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "ItemPage"), breadcrumb_schema(trail), product_schema(c)]
        prev_c, next_c = CREATIONS[(i - 1) % n], CREATIONS[(i + 1) % n]
        related = [x for x in CREATIONS if x["category"] == c["category"] and x is not c][:3]
        if len(related) < 3:
            related += [x for x in CREATIONS if x not in related and x is not c][:3 - len(related)]
        related_html = "".join(creation_card(x, j) for j, x in enumerate(related))
        details = "".join(f"<li>{d}</li>" for d in c["details"])
        palette = "".join(f'<span class="swatch static" style="--c:{p}" title="{p}"></span>' for p in c["palette"])
        occ = next((o for o in OCCASIONS if c["slug"] in o["gallery"]), None)
        occ_link = f'<a class="pill" href="/custom-banners/{occ["slug"]}/">{occ["icon"]} More {occ["label"].lower()}</a>' if occ else ""
        body = f"""
<section class="product"><div class="container">
{breadcrumbs(trail)}
<div class="product-grid">
<div class="product-media" data-reveal>
<a class="zoomable" href="/assets/img/gallery/{c['image']}.webp" data-lightbox="creation" data-caption="{esc(c['title'])}">
{img(c['image'], c['alt'], cls='product-img ' + c['orientation'], sizes='(max-width: 900px) 100vw, 60vw', loading='eager')}
<span class="zoom-hint" aria-hidden="true">Tap to zoom</span></a>
<div class="product-nav"><a href="/creation/{prev_c['slug']}/" rel="prev">‹ {prev_c['title']}</a><a href="/creation/{next_c['slug']}/" rel="next">{next_c['title']} ›</a></div>
</div>
<div class="product-copy">
<div class="eyebrow" data-reveal>{CATEGORY_LABEL[c['category']]} &middot; {KW}</div>
<h1 class="display" data-reveal data-split>{c['title']}</h1>
<p class="price" data-reveal>Starts at ${c['price']}.00</p>
<p class="lead" data-reveal>{c['blurb']}</p>
<dl class="spec" data-reveal>
<div><dt>Painted wording</dt><dd>{esc(c['wording'])}</dd></div>
<div><dt>Palette</dt><dd class="palette">{palette}</dd></div>
<div><dt>Sizes</dt><dd>{", ".join(esc(s) for s in SIZES)}</dd></div>
<div><dt>Made in</dt><dd>Belton, Texas &middot; hand-painted to order</dd></div>
</dl>
<ul class="check-list" data-reveal>{details}</ul>
<div class="share" data-reveal><span>Share:</span>
<a href="https://www.facebook.com/sharer/sharer.php?u={url(path)}" target="_blank" rel="noopener">Facebook</a>
<a href="https://pinterest.com/pin/create/button/?url={url(path)}&amp;media={url('/assets/img/gallery/' + c['image'] + '.webp')}&amp;description={esc(c['title'])}" target="_blank" rel="noopener">Pinterest</a>
<a href="mailto:?subject={esc(c['title'])}&amp;body={url(path)}">Email</a>
<button type="button" class="text-btn" data-copy="{url(path)}">Copy link</button>
</div>
<div class="pills" data-reveal>{occ_link}<a class="pill" href="/gallery/">All hand painted banners</a></div>
</div>
</div>
</div></section>
<section class="order" id="order"><div class="container order-grid">
<div class="order-copy" data-reveal>
<div class="eyebrow">Order this design</div>
<h2 class="display">Make it yours</h2>
<p>Choose a size, tell us the name, date and any personalization, and a version of this banner will be sketched for your event. Starting at ${c['price']}.00; the final quote depends on size and detail and is confirmed before painting.</p>
<ul class="trust-list"><li>Sketch approved by you before painting</li><li>Any wording, colors and motifs can change</li><li>Pickup or delivery around Belton, TX</li></ul>
</div>
<div class="contact-card" data-reveal>
<form class="quote-form" method="post" action="/contact.php" novalidate>
<input type="hidden" name="source" value="creation">
<input type="hidden" name="product" value="{esc(c['title'])} (/creation/{c['slug']}/)">
<div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="form-grid">
<div class="field full"><label for="o-size">Size</label><select id="o-size" name="size" required><option value="">------</option>{"".join(f"<option>{esc(s)}</option>" for s in SIZES)}</select></div>
<div class="field full"><label for="o-details">Personalization Details</label><textarea id="o-details" name="message" rows="4" placeholder="Name, wording, colors, theme, where it will hang..." required></textarea></div>
<div class="field"><label for="o-date">Event Date</label><input id="o-date" name="event_date" type="date"></div>
<div class="field"><label for="o-name">Name</label><input id="o-name" name="name" type="text" autocomplete="name" required></div>
<div class="field"><label for="o-email">Email</label><input id="o-email" name="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="o-phone">Phone Number</label><input id="o-phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
<button class="btn btn-primary submit" type="submit"><span>Send</span><span class="btn-arrow" aria-hidden="true">→</span></button>
<p class="form-status" role="status" aria-live="polite"></p>
<p class="form-note">Or call / text {P}.</p>
</form>
</div>
</div></section>
<section class="section alt"><div class="container">
{section_head("You may also like", "More hand-painted banners", None, center=False)}
<div class="creation-grid">{related_html}</div>
<p class="center" data-reveal><a class="btn btn-dark" href="/gallery/">Load more</a></p>
</div></section>
"""
        write(path, head(page) + header("/gallery/") + body + footer())
        register(path, c["published"], "0.7")


def build_about():
    page = {
        "path": "/about-christina-dittman-creations/",
        "title": f"About {BIZ['name']} | The Artist Behind {KW}",
        "description": "Every celebration deserves something personal. Something that feels like it was made just for that moment. That’s exactly where Christina Dittman Creations began.",
        "h1": f"About {BIZ['name']}",
    }
    trail = [("Home", "/"), (f"About {BIZ['name']}", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "AboutPage"), breadcrumb_schema(trail),
                      jsonld({"@type": "Person", "@id": url("/about-christina-dittman-creations/#person"), "name": BIZ["founder"],
                              "jobTitle": "Artist and owner", "worksFor": {"@id": url("/#business")}, "url": url("/about-christina-dittman-creations/")})]
    values = [
        ("Hand-painted with care", "Every letter and illustration is painted by hand. Visible brushwork is part of the charm."),
        ("Designed for your occasion", "No templates. The banner is drawn around your story, your colors and your theme."),
        ("Attention to color, style and theme", "Palettes are matched to invitations, decorations or the room where the banner will hang."),
        ("Personal, not mass-produced", "Each order is treated like it’s for a close friend or family member - because that level of care shows."),
    ]
    values_html = "".join(f'<article class="why-card" data-reveal data-tilt style="--i:{i}"><span class="why-icon" aria-hidden="true">✦</span><h3>{h}</h3><p>{t}</p></article>' for i, (h, t) in enumerate(values))
    body = sub_hero(page, trail, "Our story", "Every celebration deserves something personal. Something that feels like it was made just for that moment. That’s exactly where Christina Dittman Creations began.") + f"""
<section class="section"><div class="container split">
<div class="split-media" data-reveal><div class="brush-frame" data-brush>{img('custom-hand-painted-birthday-banner-3', CREATION['custom-hand-painted-birthday-banner-3']['alt'], sizes='(max-width: 900px) 100vw, 50vw')}</div>
<div class="floating-card" data-parallax="-0.08"><img src="{BIZ['logo']}" alt="" width="72" height="72" aria-hidden="true"><div><strong>{BIZ['founder']}</strong><span>Artist &middot; Belton, Texas</span></div></div></div>
<div class="split-copy prose">
<h2 data-reveal>How it started</h2>
<p data-reveal>What started as a love for art, lettering and meaningful details grew into a passion for creating custom hand-painted banners that turn ordinary events into unforgettable experiences. Whether it’s a wedding, birthday, baby shower, engagement, graduation, church service or a once-in-a-lifetime celebration, each banner is designed to reflect your story.</p>
<p data-reveal><strong>No templates. No shortcuts. Just thoughtful, handcrafted work.</strong></p>
<p data-reveal>Today the studio is better known around Bell County simply as <a href="/belton-banners/">{KW}</a> - the place in Belton, Texas where a birthday banner, a church verse or a wedding welcome sign gets painted by hand.</p>
</div>
</div></section>
<section class="section alt"><div class="container">
{section_head("The heart behind the craft", "The small details matter", "A banner isn’t just decoration. It’s the backdrop to your photos. The focal point of your event. The piece people remember long after the celebration ends. That’s why every banner is:")}
<div class="why-grid four">{values_html}</div>
</div></section>
<section class="section"><div class="container prose narrow">
<h2 data-reveal>Custom made, start to finish</h2>
<p data-reveal>Every banner begins with your vision. From the wording and colors to the overall style, each detail is carefully planned and brought to life by hand. Whether you want something elegant and minimal or bold and eye-catching, the goal is always the same: to create a piece that feels uniquely yours.</p>
<p data-reveal>You’re not just ordering a banner - you’re collaborating on something meaningful.</p>
<h2 data-reveal>Designed for life’s biggest moments</h2>
<p data-reveal>{BIZ['name']} proudly creates banners for:</p>
<ul class="check-list cols" data-reveal>
<li><a href="/custom-banners/wedding-banners/">Weddings</a></li><li><a href="/custom-banners/birthday-banners/">Birthdays</a></li><li><a href="/custom-banners/baby-shower-banners/">Baby showers</a></li>
<li>Engagement celebrations</li><li><a href="/custom-banners/graduation-banners/">Graduations</a></li><li><a href="/custom-banners/church-banners/">Church services and children’s church</a></li>
<li><a href="/custom-banners/holiday-seasonal-banners/">Holidays and seasons</a></li><li>And all of life’s special occasions</li>
</ul>
<p data-reveal>If it matters to you, it matters here.</p>
<h2 data-reveal>Made with care, meant to last</h2>
<p data-reveal>There’s something special about handmade work. You can see it. You can feel it. Every brushstroke, every letter, every detail is created with intention. The result is more than just décor - it’s a keepsake you’ll want to hold onto long after the event is over.</p>
</div></section>
{cta_band("Let’s make something for your moment", f"Call or text {P}, or send a few details and {BIZ['founder']} will be in touch.")}
{contact_form("about")}
"""
    write(page["path"], head(page) + header("/about-christina-dittman-creations/") + body + footer())
    register(page["path"], priority="0.8")


def build_contact():
    page = {
        "path": "/contact-us/",
        "title": f"Contact Us | Get a Custom Banner Quote | {KW}",
        "description": f"Have an idea in mind? Contact {BIZ['name']} in Belton, TX for a custom hand-painted banner quote. Call or text {P}.",
        "h1": "Contact Us",
    }
    trail = [("Home", "/"), ("Contact Us", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "ContactPage"), breadcrumb_schema(trail)]
    body = sub_hero(page, trail, "Let’s bring it to life", "Have an idea in mind? Whether you’re planning a wedding, celebrating a milestone, or creating something truly one-of-a-kind, I’d love to hear from you. Share your vision, event details and any inspiration you have, and we’ll start designing a custom hand-painted banner that fits your moment perfectly.") + f"""
<section class="section contact-ways"><div class="container three">
<a class="way" href="tel:{TEL}" data-reveal data-tilt style="--i:0"><span class="way-icon" aria-hidden="true">☎</span><strong>Call</strong><span>{P}</span></a>
<a class="way" href="sms:{TEL}" data-reveal data-tilt style="--i:1"><span class="way-icon" aria-hidden="true">✉</span><strong>Text</strong><span>{P}</span></a>
<a class="way" href="mailto:{BIZ['email']}" data-reveal data-tilt style="--i:2"><span class="way-icon" aria-hidden="true">@</span><strong>Email</strong><span>{BIZ['email']}</span></a>
</div></section>
{contact_form("contact", heading="Every order is personal, and it all starts right here", intro="Fill out the form below and I’ll be in touch soon - usually within a day. The more you share (date, size, wording, colors, inspiration photos later by text or email), the faster the sketch comes together.")}
<section class="section alt"><div class="container narrow prose">
<h2 data-reveal>What happens next</h2>
<ol class="steps compact">
<li class="step" data-reveal style="--i:0"><span class="step-num">01</span><h3>You send the details</h3><p>Occasion, date, size, wording and anything you love.</p></li>
<li class="step" data-reveal style="--i:1"><span class="step-num">02</span><h3>Sketch and quote</h3><p>A design direction and a confirmed price come back to you.</p></li>
<li class="step" data-reveal style="--i:2"><span class="step-num">03</span><h3>Painting</h3><p>Once approved, the banner is painted by hand in Belton.</p></li>
<li class="step" data-reveal style="--i:3"><span class="step-num">04</span><h3>Pickup or delivery</h3><p>Rolled and ready for your event.</p></li>
</ol>
<p data-reveal>Serving Belton, Temple, Killeen, Harker Heights, Salado and the rest of Central Texas. <a href="/faq/">Read the FAQ</a> for sizes, timing and care.</p>
</div></section>
"""
    write(page["path"], head(page) + header("/contact-us/") + body + footer())
    register(page["path"], priority="0.9")


def build_how_it_works():
    page = {
        "path": "/how-it-works/",
        "title": f"How It Works | Ordering a Hand-Painted Banner | {KW}",
        "description": f"How to order a custom hand-painted banner from {BIZ['name']} in Belton, TX: share your idea, approve a sketch, painting by hand, then pickup or delivery.",
        "h1": "How ordering a hand-painted banner works",
    }
    trail = [("Home", "/"), ("How It Works", None)]
    steps = [
        ("Inspiration & idea", "You bring your vision - or even just a vague idea. The occasion, the date, where the banner will hang, a name, a verse, a theme. Photos of the invitation or the room help with colors.", "A message, a call or a text is enough to start."),
        ("Concept development", "Colors, lettering style and layout start taking shape. Script or block? Kraft paper or cream? One big illustration or a border of small ones? This is where the banner becomes yours.", "You’ll get a quote at this stage, before anything is painted."),
        ("Sketch & approval", "A draft is created so you can see the direction before painting begins. Change the wording, swap a motif, tweak a color - approval is the point of no surprises.", "Most sketches are approved in one or two rounds."),
        ("Painting process", "This is where the magic happens. Each letter and illustration is painted by hand on kraft paper in the Belton studio, layer by layer, with visible brushwork that no printer can fake.", "A few days to a couple of weeks depending on detail."),
        ("Final touches & delivery", "Details are refined, the banner is checked, rolled (never folded) and prepared for your event. Pickup in Belton or delivery nearby is arranged with you.", "Hang it with painter’s tape, clips or clothespins."),
    ]
    steps_html = "".join(
        f'<li class="timeline-item" data-reveal style="--i:{i}"><div class="timeline-marker"><span>{i + 1:02d}</span></div><div class="timeline-body"><h2>{h}</h2><p>{t}</p><p class="note">{n}</p></div></li>'
        for i, (h, t, n) in enumerate(steps))
    faqs = [
        ("How far in advance should I order?", "Two to three weeks ahead is comfortable for most banners. Easter, Christmas and May graduation season fill up earlier. Rush requests are often possible - ask."),
        ("What do you need from me to start?", "The occasion, the event date, the wording (names, ages, a verse), the size you have in mind and anything that shows your style: invitation, colors, a photo of the room."),
        ("Can I change the design after the sketch?", "Yes - that is what the sketch is for. Changes after painting has started may affect the price or timing."),
        ("How do I hang the banner?", "Painter’s tape or removable mounting strips on the back corners, clips on a line, or clothespins on a string. Avoid regular tape on painted areas."),
    ]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), faq_schema(faqs),
                      jsonld({"@type": "HowTo", "name": "How to order a custom hand-painted banner", "step": [
                          {"@type": "HowToStep", "position": i + 1, "name": h, "text": re.sub("<[^>]+>", "", t)} for i, (h, t, n) in enumerate(steps)]})]
    body = sub_hero(page, trail, "The process", "Creating a hand-painted banner is not a quick click-and-order process. It’s collaborative, intentional and personal. Here’s how it typically works.") + f"""
<section class="section"><div class="container narrow"><ol class="timeline">{steps_html}</ol></div></section>
{designer()}
{faq_section(faqs, "Before you order")}
{cta_band("Ready to start step one?", f"Send the details or call {P}.")}
{contact_form("how-it-works")}
"""
    write(page["path"], head(page) + header("/how-it-works/") + body + footer())
    register(page["path"], priority="0.8")


def build_pricing():
    page = {
        "path": "/pricing-and-sizes/",
        "title": f"Pricing & Sizes | Hand-Painted Banners from $90 | {KW}",
        "description": f"Hand-painted banner pricing from {BIZ['name']} in Belton, TX: banners start at $90-$100 in five standard sizes. What affects the price and how quotes work.",
        "h1": "Pricing and sizes",
    }
    trail = [("Home", "/"), ("Pricing & Sizes", None)]
    faqs = [
        ("Why don’t you list a fixed price per size?", "Because two banners of the same size can take very different amounts of work. A name in script with two small motifs is quicker than a full nativity scene with a verse. The quote reflects the actual design, and it is confirmed before painting."),
        ("What is included in the starting price?", "Design consultation, a sketch for approval, the paint and paper, and the finished banner ready to hang. Delivery around Belton is arranged separately."),
        ("Do you offer discounts for churches or multiple banners?", "Group and repeat orders are welcome - ask when you request the quote."),
        ("How do I pay?", "Payment details are confirmed with your quote. Custom work that has started is not refundable."),
    ]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), faq_schema(faqs)]
    size_cards = ""
    size_use = {
        '30" x 30"': ("Square accent", "A door, a highchair backdrop, a small wall or a sign for a table."),
        '36" x 30"': ("Classic", "Behind a cake table, a classroom wall or a mantel."),
        '48" x 30"': ("Most popular", "A dining-room wall or the backdrop for a gift table."),
        '60" x 30"': ("Wide backdrop", "A photo backdrop, a stage or a fellowship hall."),
        '36" x 60"': ("Tall", "A classroom door, a stage side panel or a tall entryway wall."),
    }
    for i, s in enumerate(SIZES):
        w, h = [int(x) for x in re.findall(r"(\d+)", s)]
        label, use = size_use[s]
        size_cards += f'<li class="size-card" data-reveal data-tilt style="--i:{i}"><div class="size-box" style="--w:{w};--h:{h}"><span>{esc(s)}</span></div><h3>{label}</h3><p>{use}</p></li>'
    factors = [
        ("Size", "Bigger paper, more paint, more time. The five standard sizes are listed below; larger banners are possible."),
        ("Amount of lettering", "A name and a greeting is quick. A full verse with a reference takes longer and needs careful spacing."),
        ("Illustrations", "Each painted motif - a tractor, a cowgirl portrait, a nativity scene - adds time. Three to six small motifs is typical."),
        ("Detail and layering", "Camo borders, gingham, rope frames, shading and gradients are layered by hand."),
        ("Timing", "Rush requests may add to the price when the schedule allows them at all."),
    ]
    factors_html = "".join(f'<article class="why-card" data-reveal style="--i:{i}"><span class="why-icon" aria-hidden="true">{i + 1}</span><h3>{h}</h3><p>{t}</p></article>' for i, (h, t) in enumerate(factors))
    body = sub_hero(page, trail, "Honest pricing", f"Hand-painted banners from {BIZ['name']} start at $90 to $100. Most of the banners in the gallery are listed at “starts at $100”. The final price depends on size and detail, and it is confirmed with you before any painting begins.") + f"""
<section class="section"><div class="container">
<div class="price-hero" data-reveal>
<div class="price-big"><span class="eyebrow">Banners start at</span><strong>$90<span>–</span>$100</strong><span class="eyebrow">quote confirmed before painting</span></div>
<ul class="check-list"><li>Design consultation and sketch included</li><li>Painted by hand on kraft (or cream, grey, white) paper</li><li>Rolled and ready to hang</li><li>Pickup in Belton or delivery nearby by arrangement</li></ul>
</div>
{section_head("Five standard sizes", "Pick the size for the space", "All sizes are in inches, width by height. Not sure? Tell us where the banner will hang and we’ll suggest one.")}
<ul class="size-grid">{size_cards}</ul>
</div></section>
<section class="section alt"><div class="container">
{section_head("What affects the price", "Five things that move a quote up or down")}
<div class="why-grid">{factors_html}</div>
</div></section>
{designer()}
{faq_section(faqs, "Pricing questions")}
{cta_band("Want a number for your banner?", "Send the size, the wording and the occasion and you’ll have a quote - no obligation.")}
{contact_form("pricing")}
"""
    write(page["path"], head(page) + header("/pricing-and-sizes/") + body + footer())
    register(page["path"], priority="0.8")


FAQ_GROUPS = [
    ("Ordering", [
        ("How do I order a custom banner?", f"Use the contact form on any page, call or text {P}, or email {BIZ['email']}. Share the occasion, the date, the wording and the size, and you’ll get a sketch direction and a quote."),
        ("How far ahead should I order?", "Two to three weeks is comfortable. Easter, Christmas and graduation season book earlier. Rush requests are often possible depending on the queue."),
        ("Do I approve the design before it is painted?", "Yes. A sketch or detailed description is shared for approval first. Painting starts only after you say go."),
        ("Can you work from a photo or a Pinterest idea?", "Absolutely. Inspiration photos are the fastest way to get the style right. The banner will be an original painting in that spirit, not a copy."),
    ]),
    ("Pricing", [
        ("How much does a hand-painted banner cost?", "Banners start at $90 to $100. Size, the amount of lettering and the number of illustrations set the final quote, which is confirmed before painting."),
        ("Is there a deposit?", "Payment terms are confirmed with your quote."),
        ("Do you do group or church orders?", "Yes. Multiple banners in one style for a church season, a school or a group of families are welcome."),
    ]),
    ("Sizes & materials", [
        ("What sizes do you offer?", 'Five standard sizes: 30" x 30", 36" x 30", 48" x 30", 60" x 30" and 36" x 60". Larger banners for stages are possible on request.'),
        ("What are banners painted on?", "Kraft paper is the signature look. Cream, white and grey paper are available, and canvas can be arranged for banners that will be hung outdoors more often."),
        ("What kind of paint is used?", "Acrylic paint, applied by hand with brushes. It dries matte and durable."),
    ]),
    ("Hanging & care", [
        ("How do I hang my banner?", "Painter’s tape or removable mounting strips on the back corners, clips on a line, or clothespins. Avoid regular tape on painted areas."),
        ("Can I use it outside?", "On a covered porch or under a tent, yes. Bring it in for rain and heavy wind."),
        ("How do I store it?", "Roll it around a cardboard tube with the painted side out, wrap it loosely and keep it dry. Never fold it."),
        ("Can I frame it?", "Yes - many banners end up framed as wall art. A poster frame or a custom frame with a mat both work."),
    ]),
    ("Local", [
        (f"Where are {KW} made?", f"In {BIZ['founder']}’s studio in Belton, Texas, in Bell County."),
        ("Do you deliver?", "Pickup in Belton and delivery to nearby towns - Temple, Killeen, Harker Heights, Salado, Nolanville, Troy - are arranged when the banner is ready."),
        ("Do you ship?", "Shipping rolled banners further afield can be arranged on request; ask when you order."),
    ]),
]


def build_faq():
    page = {
        "path": "/faq/",
        "title": f"FAQ | Hand-Painted Banner Questions | {KW}",
        "description": f"Answers about ordering hand-painted banners from {BIZ['name']} in Belton, TX: pricing, sizes, timing, materials, hanging, storage, delivery and more.",
        "h1": "Frequently asked questions",
    }
    trail = [("Home", "/"), ("FAQ", None)]
    allq = [q for _, qs in FAQ_GROUPS for q in qs]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "FAQPage"), breadcrumb_schema(trail), faq_schema(allq)]
    groups = ""
    for g, qs in FAQ_GROUPS:
        items = "".join(f'<details class="faq-item" data-reveal style="--i:{i}"><summary><span>{q}</span><span class="faq-icon" aria-hidden="true"></span></summary><div class="faq-body"><p>{a}</p></div></details>' for i, (q, a) in enumerate(qs))
        groups += f'<div class="faq-group" id="{g.lower().split()[0]}"><h2 data-reveal>{g}</h2><div class="faq-list">{items}</div></div>'
    jump = "".join(f'<a class="pill" href="#{g.lower().split()[0]}">{g}</a>' for g, _ in FAQ_GROUPS)
    body = sub_hero(page, trail, "Help", "Everything people ask before ordering a hand-painted banner. Not answered here? Call or text " + P + ".", extra=f'<div class="pills" data-reveal>{jump}</div>') + f"""
<section class="section"><div class="container narrow">{groups}</div></section>
{cta_band("Still have a question?", "Ask it in the form and you’ll hear back quickly.")}
{contact_form("faq")}
"""
    write(page["path"], head(page) + header("/faq/") + body + footer())
    register(page["path"], priority="0.7")


def build_belton():
    page = {
        "path": "/belton-banners/",
        "title": f"{KW} | Hand-Painted Banners in Belton, TX",
        "description": f"{KW}: custom hand-painted birthday, wedding, church and seasonal banners made in Belton, Texas by {BIZ['name']}. Serving Temple, Killeen and Salado.",
        "h1": f"{KW}: hand-painted in Belton, Texas",
    }
    trail = [("Home", "/"), (f"{KW} in Belton, TX", None)]
    faqs = [
        (f"Is {KW} the same as {BIZ['name']}?", f"Yes. {BIZ['name']} is the studio; {KW} is what people around Bell County call the banners it paints, and this site lives at beltonbanners.com."),
        ("Where do you deliver around Belton?", "Pickup in Belton, and delivery to Temple, Killeen, Harker Heights, Salado, Nolanville, Troy and nearby towns when the banner is ready."),
        ("Do you paint banners for Belton schools and churches?", "Yes - children’s church banners, VBS banners, senior-night and graduation banners, and classroom verse banners are regular orders."),
        ("Can I see examples?", "The gallery shows banners painted in the studio, from first birthdays to Christmas services."),
    ]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), faq_schema(faqs)]
    towns = "".join(f'<li data-reveal style="--i:{i}"><span class="pin" aria-hidden="true">⌖</span>{t}</li>' for i, t in enumerate([BIZ["city"]] + NEARBY))
    gallery = "".join(creation_card(c, i) for i, c in enumerate(CREATIONS[:6]))
    body = sub_hero(page, trail, "Belton, Texas", f"{KW} is the local name for the custom hand-painted banners made by {BIZ['name']}. Every one is lettered and illustrated by hand in a Belton studio and carried to parties, churches, schools and porches across Bell County and Central Texas.") + f"""
<section class="section"><div class="container split">
<div class="split-copy prose">
<h2 data-reveal>Why Belton families choose hand-painted</h2>
<p data-reveal>A printed banner from a big-box store is identical to a thousand others. {KW} are painted one at a time - the name in script, the age painted like a road for a construction party, the family dog in the corner, a verse for Sunday school. They photograph like art because they are art, and they come home after the event instead of going in the trash.</p>
<p data-reveal>Because the studio is local, the process is personal: a quick text to talk through the idea, a sketch to approve, pickup in Belton or delivery to Temple, Killeen, Harker Heights or Salado when the banner is ready.</p>
<h2 data-reveal>What we paint for Belton</h2>
<ul class="check-list" data-reveal>
<li><a href="/custom-banners/birthday-banners/">Birthday banners</a> for kids, milestones and 21sts</li>
<li><a href="/custom-banners/wedding-banners/">Wedding welcome signs</a> and sweetheart-table banners</li>
<li><a href="/custom-banners/baby-shower-banners/">Baby shower and gender reveal</a> banners</li>
<li><a href="/custom-banners/church-banners/">Children’s church and scripture</a> banners</li>
<li><a href="/custom-banners/graduation-banners/">Graduation and senior-night</a> banners in school colors</li>
<li><a href="/custom-banners/holiday-seasonal-banners/">Fall, Christmas and Easter</a> banners</li>
</ul>
</div>
<div class="split-media" data-reveal>
<div class="brush-frame" data-brush>{img('custom-hand-painted-birthday-banner-5', CREATION['custom-hand-painted-birthday-banner-5']['alt'], sizes='(max-width: 900px) 100vw, 50vw')}</div>
</div>
</div></section>
<section class="section alt"><div class="container">
{section_head("Service area", "Serving Belton and Central Texas", "Pickup in Belton; delivery arranged for the towns below and beyond.")}
<ul class="town-list">{towns}</ul>
</div></section>
<section class="section"><div class="container">
{section_head("Recent work", f"{KW} from the gallery", None, center=False)}
<div class="creation-grid">{gallery}</div>
<p class="center" data-reveal><a class="btn btn-dark" href="/gallery/">See the full gallery</a></p>
</div></section>
{faq_section(faqs, f"{KW} questions")}
{cta_band(f"Order {KW.lower()} for your next event", f"Call or text {P}, or send the details below.")}
{contact_form("belton")}
"""
    write(page["path"], head(page) + header(None) + body + footer())
    register(page["path"], priority="0.8")


def build_design_page():
    page = {
        "path": "/design-your-banner/",
        "title": f"Design Your Banner Online | Live Preview | {KW}",
        "description": f"Mock up your hand-painted banner: choose the occasion, wording, paper, lettering, ink color, motif and size, then send it to {BIZ['name']} as a quote request.",
        "h1": "Design your banner",
    }
    trail = [("Home", "/"), ("Design Your Banner", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail)]
    body = sub_hero(page, trail, "Interactive", "Play with the wording, paper, lettering and motifs until the mock-up feels right, then send it as a quote request. It lands in the form below with everything filled in.") + f"""
{designer(full=False)}
<section class="section alt"><div class="container narrow prose">
<h2 data-reveal>A mock-up, not the finished art</h2>
<p data-reveal>The designer is a quick way to describe what you want. The real banner is sketched by hand, with lettering and illustrations drawn for your words and your space, and you approve that sketch before painting. Think of this page as the start of the conversation.</p>
<p data-reveal>Want to see what hand-painted lettering and motifs look like for real? Browse the <a href="/gallery/">gallery</a>, or read about the <a href="/how-it-works/">process</a>.</p>
</div></section>
{contact_form("design", heading="Send your design", intro="Your mock-up details are filled in below. Add the date, your contact details and anything else, and send.")}
"""
    write(page["path"], head(page) + header(None) + body + footer())
    register(page["path"], priority="0.7")


def build_blog_index():
    posts = sorted(POSTS, key=lambda p: p["published"], reverse=True)
    page = {
        "path": "/blog/",
        "title": f"Blog | Hand-Painted Banner Ideas & Tips | {KW}",
        "description": f"Articles from the {KW} studio: banner ideas for birthdays, weddings, church and seasons, wording tips, sizes and how to care for a hand-painted banner.",
        "h1": "Latest articles",
    }
    trail = [("Home", "/"), ("Blog", None)]
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page, "CollectionPage"), breadcrumb_schema(trail),
                      jsonld({"@type": "Blog", "@id": url("/blog/#blog"), "name": f"{BIZ['name']} blog", "blogPost": [{"@id": url(f"/{p['slug']}/") + "#article"} for p in posts]})]
    cards = "".join(post_card(p, i) for i, p in enumerate(posts))
    body = sub_hero(page, trail, "Blog", "Ideas, wording tips and notes from the studio on hand-painted banners.") + f"""
<section class="section"><div class="container"><div class="post-grid">{cards}</div></div></section>
{cta_band()}
"""
    write(page["path"], head(page) + header("/blog/") + body + footer())
    register(page["path"], posts[0]["modified"], "0.7")

    # /category/general/ - the only WordPress category archive, kept as a listing
    cat = {
        "path": "/category/general/",
        "title": f"General | Blog Category | {BIZ['name']}",
        "description": f"All articles in the General category of the {BIZ['name']} blog.",
        "h1": "General",
        "robots": "noindex, follow",
    }
    cat["schema"] = [org_schema(), website_schema(), webpage_schema(cat, "CollectionPage"), breadcrumb_schema([("Home", "/"), ("Blog", "/blog/"), ("General", None)])]
    body = sub_hero(cat, [("Home", "/"), ("Blog", "/blog/"), ("General", None)], "Category") + f"""
<section class="section"><div class="container"><div class="post-grid">{cards}</div></div></section>
"""
    write(cat["path"], head(cat) + header("/blog/") + body + footer())


def build_posts():
    posts = sorted(POSTS, key=lambda p: p["published"], reverse=True)
    for p in POSTS:
        path = f"/{p['slug']}/"
        page = {
            "path": path, "title": p["seo_title"], "description": p["description"], "h1": p["title"],
            "published": p["published"], "modified": p["modified"], "og_type": "article",
            "og_image": f"/assets/img/gallery/{p['image']}.webp",
        }
        trail = [("Home", "/"), ("Blog", "/blog/"), (p["title"], None)]
        page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail), article_schema(p), faq_schema(p["faqs"])]
        related = [x for x in posts if x is not p][:2]
        related_html = "".join(post_card(x, i) for i, x in enumerate(related))
        faq_html = "".join(f'<details class="faq-item" data-reveal style="--i:{i}"><summary><span>{i + 1}. {q}</span><span class="faq-icon" aria-hidden="true"></span></summary><div class="faq-body"><p>{a}</p></div></details>' for i, (q, a) in enumerate(p["faqs"]))
        body = f"""
<article class="post">
<header class="post-hero"><div class="container narrow">
{breadcrumbs([("Home", "/"), ("Blog", "/blog/"), ("Article", None)])}
<div class="eyebrow" data-reveal><a href="/category/general/">General</a> &middot; {pretty_date(p['published'])} &middot; {p['read_time']}</div>
<h1 class="display" data-reveal data-split>{p['title']}</h1>
<p class="byline" data-reveal>By <a href="/about-christina-dittman-creations/">{BIZ['founder']}</a>, {BIZ['name']} &middot; Belton, TX</p>
</div>
<div class="container post-cover" data-reveal><div class="brush-frame" data-brush>{img(p['image'], p['image_alt'], sizes='(max-width: 1100px) 100vw, 1000px', loading='eager')}</div></div>
</header>
<div class="container narrow prose post-body" data-reveal>
{p['body']}
<h2>FAQs</h2>
<div class="faq-list">{faq_html}</div>
<div class="post-share"><span>Share:</span>
<a href="https://www.facebook.com/sharer/sharer.php?u={url(path)}" target="_blank" rel="noopener">Facebook</a>
<a href="https://pinterest.com/pin/create/button/?url={url(path)}&amp;media={url('/assets/img/gallery/' + p['image'] + '.webp')}&amp;description={esc(p['title'])}" target="_blank" rel="noopener">Pinterest</a>
<a href="mailto:?subject={esc(p['title'])}&amp;body={url(path)}">Email</a>
<button type="button" class="text-btn" data-copy="{url(path)}">Copy link</button></div>
<div class="author-box"><img src="{BIZ['logo']}" alt="" width="72" height="72" aria-hidden="true"><div><strong>{BIZ['founder']}</strong><p>Artist and owner of {BIZ['name']} - {KW} - painting custom banners by hand in Belton, Texas. <a href="/about-christina-dittman-creations/">About the studio →</a></p></div></div>
</div>
</article>
<section class="section alt"><div class="container">
{section_head("Related articles", "Keep reading", None, center=False)}
<div class="post-grid two">{related_html}</div>
</div></section>
{cta_band()}
{contact_form(p['slug'])}
"""
        write(path, head(page) + header("/blog/") + body + footer())
        register(path, p["modified"], "0.6")


def build_legal():
    for item in (PRIVACY, TERMS):
        page = {"path": item["path"], "title": item["title"], "description": item["description"], "h1": item["h1"]}
        trail = [("Home", "/"), (item["h1"], None)]
        page["schema"] = [org_schema(), website_schema(), webpage_schema(page), breadcrumb_schema(trail)]
        body = sub_hero(page, trail, item["effective"]) + f"""
<section class="section"><div class="container narrow prose legal" data-reveal>{item['body']}</div></section>
"""
        write(item["path"], head(page) + header(None) + body + footer())
        register(item["path"], priority="0.3")


def build_thank_you():
    page = {
        "path": "/thank-you/",
        "title": f"Thank You | {BIZ['name']}",
        "description": "Your banner request has been sent. Christina will be in touch soon.",
        "h1": "Thank you - your request is on its way",
        "robots": "noindex, nofollow",
    }
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page)]
    body = sub_hero(page, [("Home", "/"), ("Thank you", None)], "Sent", f"Thanks for reaching out to {BIZ['name']}. You’ll hear back soon, usually within a day. If it’s urgent, call or text {P}.") + f"""
<section class="section"><div class="container narrow center">
<div class="btn-row center" data-reveal><a class="btn btn-dark" href="/gallery/">Browse the gallery</a><a class="btn btn-ghost" href="/blog/">Read the blog</a></div>
</div></section>
"""
    write(page["path"], head(page) + header(None) + body + footer())


def build_sitemap_page():
    page = {
        "path": "/sitemap/",
        "title": f"Sitemap | {BIZ['name']}",
        "description": f"Every page on beltonbanners.com - {KW} by {BIZ['name']}.",
        "h1": "Sitemap",
    }
    page["schema"] = [org_schema(), website_schema(), webpage_schema(page)]
    groups = [
        ("Main pages", [("Home", "/"), (f"About {BIZ['name']}", "/about-christina-dittman-creations/"), ("Gallery", "/gallery/"), ("How It Works", "/how-it-works/"), ("Pricing & Sizes", "/pricing-and-sizes/"), ("Design Your Banner", "/design-your-banner/"), (f"{KW} in Belton, TX", "/belton-banners/"), ("FAQ", "/faq/"), ("Contact Us", "/contact-us/"), ("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/")]),
        ("Custom banners", [("All custom banners", "/custom-banners/")] + [(o["label"], f"/custom-banners/{o['slug']}/") for o in OCCASIONS]),
        ("Hand painted banners (gallery)", [(c["title"], f"/creation/{c['slug']}/") for c in CREATIONS]),
        ("Blog", [("All articles", "/blog/"), ("Category: General", "/category/general/")] + [(p["title"], f"/{p['slug']}/") for p in POSTS]),
    ]
    def li(items):
        return "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in items)
    html = "".join(f'<div class="sitemap-group" data-reveal><h2>{g}</h2><ul>{li(items)}</ul></div>' for g, items in groups)
    body = sub_hero(page, [("Home", "/"), ("Sitemap", None)]) + f'<section class="section"><div class="container sitemap-grid">{html}</div></section>'
    write(page["path"], head(page) + header(None) + body + footer())
    register(page["path"], priority="0.3")


def build_404():
    page = {
        "path": "/404.html",
        "title": f"Page Not Found | {BIZ['name']}",
        "description": "That page isn’t here. Browse the gallery, custom banner types or contact us.",
        "h1": "That page got painted over",
        "robots": "noindex, nofollow",
    }
    page["schema"] = [org_schema(), website_schema()]
    body = sub_hero(page, [("Home", "/"), ("404", None)], "404", "The page you’re looking for isn’t here. Try one of these instead.") + f"""
<section class="section"><div class="container narrow center">
<div class="btn-row center" data-reveal><a class="btn btn-dark" href="/">Home</a><a class="btn btn-ghost" href="/gallery/">Gallery</a><a class="btn btn-ghost" href="/custom-banners/">Custom banners</a><a class="btn btn-ghost" href="/contact-us/">Contact</a></div>
</div></section>
"""
    write("/404.html", head(page) + header(None) + body + footer())


def build_sitemap_xml():
    items = "".join(
        f"<url><loc>{url(p)}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>\n"
        for p, lm, pr in PAGES)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + items + "</urlset>\n")
    write("/sitemap.xml", xml)
    # Yoast's sitemap index URL is in Search Console and robots history; keep it valid.
    write("/sitemap_index.xml", ('<?xml version="1.0" encoding="UTF-8"?>\n'
                                 '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 f"<sitemap><loc>{url('/sitemap.xml')}</loc><lastmod>{TODAY}</lastmod></sitemap>\n"
                                 "</sitemapindex>\n"))


def build_robots():
    write("/robots.txt",
          "User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /contact.php\nDisallow: /thank-you/\n\n"
          f"Sitemap: {url('/sitemap.xml')}\n")


def build_manifest():
    write("/site.webmanifest", json.dumps({
        "name": f"{BIZ['name']} | {KW}", "short_name": KW,
        "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                  {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": "#2F1F10", "background_color": "#FEF9ED", "display": "standalone"}, indent=2))


def main():
    build_home()
    build_occasions_index()
    build_occasions()
    build_gallery()
    build_creations()
    build_about()
    build_contact()
    build_how_it_works()
    build_pricing()
    build_faq()
    build_belton()
    build_design_page()
    build_blog_index()
    build_posts()
    build_legal()
    build_thank_you()
    build_sitemap_page()
    build_404()
    build_sitemap_xml()
    build_robots()
    build_manifest()
    print(f"wrote {len(WRITTEN)} files, {len(PAGES)} sitemap URLs")


if __name__ == "__main__":
    main()
