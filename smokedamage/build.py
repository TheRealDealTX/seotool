#!/usr/bin/env python3
"""Static site generator for SmokeDamage.com.

    python3 images.py     # (only when src/img changes) builds AVIF/WebP variants
    python3 build.py      # renders ./public (site) and ./private (admin data)
    python3 validate.py   # pre-publish checks

Content collections live in content/ (see CONTENT-SPEC.md). Output:
  public/   -> uploaded to the website's public_html/
  private/  -> uploaded to sd-private/ next to public_html (never web-served)
"""

import csv
import glob
import html
import json
import math
import os
import re
import shutil
from datetime import date, datetime

from mdlite import Renderer, parse_front_matter, slugify, word_count
from siteconfig import SITE, DISCLAIMER, NAV, FOOTER_LINKS, MARKETS, TODAY

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
PRIV = os.path.join(ROOT, "private")
ORIGIN = SITE["origin"]
ASSET_V = datetime.now().strftime("%Y%m%d%H%M")

IMG_MANIFEST = {}
_m = os.path.join(ROOT, "src", "img", "manifest.json")
if os.path.exists(_m):
    IMG_MANIFEST = json.load(open(_m))
IMG_VARIANTS = {}
_v = os.path.join(ROOT, "assets", "img", "variants.json")
if os.path.exists(_v):
    IMG_VARIANTS = json.load(open(_v))


def esc(s):
    return html.escape(str(s), quote=True)


def url(path):
    return ORIGIN + path


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def fmt_date(iso):
    try:
        d = datetime.strptime(iso[:10], "%Y-%m-%d")
        return d.strftime("%B %-d, %Y")
    except Exception:
        return iso


# --------------------------------------------------------------------------
# Icons (small inline set; decorative, aria-hidden)
# --------------------------------------------------------------------------
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
    "home": '<path d="M3 10.5 12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "map": '<path d="M9 3 3 6v15l6-3 6 3 6-3V3l-6 3z"/><path d="M9 3v15M15 6v15"/>',
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.2 1.1.9 2.2 2.5 2.8z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
}


def icon(name, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>')


# --------------------------------------------------------------------------
# Images
# --------------------------------------------------------------------------

def img_alt(key):
    return IMG_MANIFEST.get(key, {}).get("alt", "")


def picture(key, sizes="100vw", cls="", eager=False, alt=None, max_w=None):
    """<picture> with AVIF + WebP srcsets from assets/img/variants.json."""
    v = IMG_VARIANTS.get(key)
    alt = img_alt(key) if alt is None else alt
    if not v:
        return f'<img class="{cls}" src="/assets/img/{key}.webp" alt="{esc(alt)}" loading="lazy" decoding="async">'
    widths = [w for w in v["widths"] if not max_w or w <= max_w] or v["widths"][:1]
    avif = ", ".join(f"/assets/img/{key}-{w}.avif {w}w" for w in widths)
    webp = ", ".join(f"/assets/img/{key}-{w}.webp {w}w" for w in widths)
    fallback_w = widths[min(1, len(widths) - 1)]
    h = round(fallback_w * v["height"] / v["width"])
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img class="{cls}" src="/assets/img/{key}-{fallback_w}.webp" width="{fallback_w}" height="{h}" '
            f'alt="{esc(alt)}" {loading} decoding="async"></picture>')


def og_image(key):
    v = IMG_VARIANTS.get(key)
    if v:
        w = max(x for x in v["widths"] if x <= 1200) if any(x <= 1200 for x in v["widths"]) else v["widths"][0]
        return url(f"/assets/img/{key}-{w}.webp")
    return url("/assets/img/og-default.webp")


# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------
PHONE_LINK = f'<a href="{SITE["phone_href"]}" data-track="phone">{SITE["phone_display"]}</a>'
EMAIL_LINK = f'<a href="mailto:{SITE["email"]}" data-track="email">{SITE["email"]}</a>'
REVIEW_LINK = f'<a href="/contact/" data-cta="inline-review">{SITE["cta_primary"]}</a>'


def cta_banner(title_html, body_html, heading_tag="p"):
    return f"""<div class="cta-banner">
<div><{heading_tag} class="cta-title">{title_html}</{heading_tag}>{body_html}</div>
<div class="btn-row"><a class="btn" href="/contact/" data-cta="banner-review">{SITE['cta_primary']}</a>
<a class="btn btn-outline" href="{SITE['phone_href']}" data-loc="banner">{icon('phone')}Call {SITE['phone_display']}</a></div>
</div>"""


def figure(key, caption):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="figure">{picture(key, "(min-width: 1060px) 760px, 100vw")}{cap}</figure>'


MD_CTX = {
    "phone_link": PHONE_LINK,
    "email_link": EMAIL_LINK,
    "review_link": REVIEW_LINK,
    "cta_banner": cta_banner,
    "figure": figure,
}


def nav_html(current):
    items = []
    for label, href, children in NAV:
        cur = ' aria-current="page"' if current == href else ""
        if children:
            sub = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in children)
            items.append(f'<li class="has-dropdown"><button type="button" aria-expanded="false" aria-haspopup="true">{esc(label)}'
                         f'<svg class="caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>'
                         f'<ul class="dropdown">{sub}</ul></li>')
        else:
            items.append(f'<li><a href="{href}"{cur}>{esc(label)}</a></li>')
    return f'<nav class="main-nav" aria-label="Main"><ul class="nav-list">{"".join(items)}</ul></nav>'


def mobile_nav_html():
    items = []
    for label, href, children in NAV:
        if children:
            sub = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in children)
            items.append(f'<li><details><summary>{esc(label)}</summary><ul>{sub}</ul></details></li>')
        else:
            items.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    return f"""<div class="mobile-nav" id="mobile-nav" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
<div class="scrim"></div>
<div class="panel">
<div class="panel-head"><a class="logo" href="/"><img src="/assets/img/logo.webp" width="600" height="121" alt="Smoke Damage Public Adjuster" style="width:170px"></a>
<button class="close" type="button" aria-label="Close menu">&times;</button></div>
<ul>{''.join(items)}</ul>
<a class="btn" href="/contact/" data-cta="mobile-nav">{SITE['cta_primary']}</a>
<a class="btn btn-outline" href="{SITE['phone_href']}" data-loc="mobile-nav">{icon('phone')}Call {SITE['phone_display']}</a>
</div></div>"""


def header_html(current):
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="container">
<div class="tb-links"><a href="{SITE['phone_href']}" data-loc="topbar">{SITE['phone_display']}</a><a class="tb-email" href="mailto:{SITE['email']}" data-loc="topbar">{SITE['email']}</a></div>
<span class="tb-note">{esc(SITE['company'])} &middot; TDI License #{SITE['license_number']} &middot; Serving all of Texas</span>
</div></div>
<header class="site-header"><div class="container header-inner">
<a class="logo" href="/" aria-label="Smoke Damage Public Adjuster home"><img src="/assets/img/logo.webp" width="600" height="121" alt="Smoke Damage Public Adjuster · Texas"></a>
{nav_html(current)}
<div class="header-actions">
<a class="header-phone" href="{SITE['phone_href']}" data-loc="header">{SITE['phone_display']}</a>
<a class="btn btn-sm header-cta" href="/contact/" data-cta="header">{SITE['cta_short']}</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span></button>
</div></div></header>
{mobile_nav_html()}"""


def footer_html():
    links = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in FOOTER_LINKS)
    addr = ""
    if SITE["licensed_address"]:
        addr = f'<li><span>{esc(SITE["licensed_address"])}</span></li>'
    year = date.today().year
    return f"""<footer class="site-footer"><div class="container">
<div class="footer-grid">
<div class="footer-brand">
<img src="/assets/img/logo-light.webp" width="600" height="121" alt="Smoke Damage Public Adjuster" loading="lazy">
<p><strong style="color:#fff">Smoke Damage Public Adjuster.</strong> {esc(SITE['tagline'])}</p>
<p>A licensed Texas Smoke Damage Public Adjuster representing policyholders, not insurance companies. We do not perform repairs, cleaning, remediation or restoration on claims we adjust.</p>
</div>
<div><p class="footer-title">Contact</p>
<ul class="footer-contact">
<li><strong>{esc(SITE['company'])}</strong><br>{esc(SITE['license_label'])}</li>
{addr}
<li><a href="{SITE['phone_href']}" data-loc="footer">{SITE['phone_display']}</a></li>
<li><a href="mailto:{SITE['email']}" data-loc="footer">{SITE['email']}</a></li>
<li>Serving Property Owners Across Texas</li>
</ul>
<a class="btn btn-sm" style="margin-top:20px" href="/contact/" data-cta="footer">{SITE['cta_primary']}</a>
</div>
<div><p class="footer-title">Explore</p><ul class="footer-links">{links}</ul></div>
</div>
<div class="footer-legal">
<p>{esc(DISCLAIMER)}</p>
<p>&copy; {year} {esc(SITE['company'])}. Smoke Damage Public Adjuster is operated by {esc(SITE['company'])}, {esc(SITE['license_label'])}. Public adjusters are not attorneys and do not provide legal advice.</p>
</div>
</div></footer>
<div class="mobile-bar no-print">
<a class="btn btn-dark" href="{SITE['phone_href']}" data-loc="mobile-bar">{icon('phone')}Call</a>
<a class="btn" href="/contact/" data-cta="mobile-bar">Free Claim Review</a>
</div>
<div class="modal" id="claim-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="modal-title">
<div class="scrim"></div>
<div class="modal-card">
<button class="modal-close" type="button" aria-label="Close">&times;</button>
<p class="eyebrow">Free Claim Review</p>
<h2 id="modal-title">Dealing With a Smoke or Fire Insurance Claim?</h2>
<p>Tell us what happened and where your claim currently stands. A licensed Texas public adjuster can review the situation with you.</p>
<a class="btn" href="/contact/?source=popup" data-cta="popup">{SITE['cta_primary']}</a>
<a class="btn btn-outline" href="{SITE['phone_href']}" data-loc="popup">{icon('phone')}Call {SITE['phone_display']}</a>
<p class="fine">{esc(SITE['company'])} &middot; TDI License #{SITE['license_number']}</p>
</div></div>"""


def analytics_head():
    out = ""
    if SITE["gsc_verification"]:
        out += f'<meta name="google-site-verification" content="{esc(SITE["gsc_verification"])}">\n'
    if SITE["bing_verification"]:
        out += f'<meta name="msvalidate.01" content="{esc(SITE["bing_verification"])}">\n'
    if SITE["ga4_id"]:
        gid = esc(SITE["ga4_id"])
        out += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>\n'
                f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
                f"gtag('js',new Date());gtag('config','{gid}',{{anonymize_ip:true}});</script>\n")
    return out


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------
ORG_ID = ORIGIN + "/#organization"
SITE_ID = ORIGIN + "/#website"
AUTHOR_ID = ORIGIN + "/about/#joseph-dittman"


def org_schema():
    org = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": SITE["brand"],
        "legalName": SITE["company"],
        "url": ORIGIN + "/",
        "logo": {"@type": "ImageObject", "url": url("/assets/img/logo.webp"), "width": 600, "height": 121},
        "image": url("/assets/img/logo.webp"),
        "telephone": SITE["phone_e164"],
        "email": SITE["email"],
        "description": SITE["tagline"],
        "areaServed": {"@type": "State", "name": "Texas", "sameAs": "https://en.wikipedia.org/wiki/Texas"},
        "knowsAbout": ["Smoke damage insurance claims", "Fire damage insurance claims", "Soot damage claims",
                       "Smoke-damaged contents", "Property insurance claim documentation"],
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                          "name": "Texas public adjuster license #" + SITE["license_number"],
                          "recognizedBy": {"@type": "GovernmentOrganization", "name": "Texas Department of Insurance",
                                           "url": "https://www.tdi.texas.gov/"}},
        "contactPoint": {"@type": "ContactPoint", "telephone": SITE["phone_e164"], "contactType": "customer service",
                         "areaServed": "US-TX", "availableLanguage": "English"},
    }
    if SITE["licensed_address"]:
        m = re.match(r"^(.*?),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5})", SITE["licensed_address"])
        org["address"] = ({"@type": "PostalAddress", "streetAddress": m.group(1), "addressLocality": m.group(2),
                           "addressRegion": m.group(3), "postalCode": m.group(4), "addressCountry": "US"}
                          if m else SITE["licensed_address"])
    if SITE["social"]:
        org["sameAs"] = list(SITE["social"].values())
    return org


def website_schema():
    return {"@type": "WebSite", "@id": SITE_ID, "url": ORIGIN + "/", "name": SITE["brand"],
            "alternateName": SITE["domain"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def person_schema():
    return {"@type": "Person", "@id": AUTHOR_ID, "name": SITE["blog_author"],
            "url": url("/about/"), "worksFor": {"@id": ORG_ID}}


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "@id": url(crumbs[-1][1]) + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": url(p)}
                                for i, (n, p) in enumerate(crumbs, 1)]}


def faq_schema(path, faqs):
    return {"@type": "FAQPage", "@id": url(path) + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a).strip()}}
        for q, a in faqs]}


def webpage_schema(page, ptype="WebPage"):
    s = {"@type": ptype, "@id": url(page["path"]) + "#webpage", "url": url(page["path"]),
         "name": page["title"], "description": page["description"], "isPartOf": {"@id": SITE_ID},
         "about": {"@id": ORG_ID}, "inLanguage": "en-US"}
    if page.get("updated"):
        s["dateModified"] = page["updated"]
    if page.get("crumbs") and len(page["crumbs"]) > 1:
        s["breadcrumb"] = {"@id": url(page["path"]) + "#breadcrumb"}
    if page.get("image"):
        s["primaryImageOfPage"] = {"@type": "ImageObject", "url": og_image(page["image"])}
    return s


def service_schema(page, area=None):
    s = {"@type": "Service", "@id": url(page["path"]) + "#service",
         "name": page.get("service_name") or page.get("h1") or page["title"],
         "serviceType": "Public adjusting — property insurance claim representation",
         "description": page["description"], "provider": {"@id": ORG_ID}, "url": url(page["path"])}
    if area:
        s["areaServed"] = area
    else:
        s["areaServed"] = {"@type": "State", "name": "Texas"}
    return s


def article_schema(page):
    s = {"@type": "BlogPosting" if page.get("kind") == "blog" else "Article",
         "@id": url(page["path"]) + "#article", "headline": page["h1"][:110],
         "description": page["description"], "mainEntityOfPage": {"@id": url(page["path"]) + "#webpage"},
         "author": {"@id": AUTHOR_ID} if page.get("kind") == "blog" else {"@id": ORG_ID},
         "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}
    if page.get("published"):
        s["datePublished"] = page["published"]
    s["dateModified"] = page.get("updated") or page.get("published") or TODAY
    if page.get("image"):
        s["image"] = og_image(page["image"])
    if page.get("words"):
        s["wordCount"] = page["words"]
    return s


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------

def render_page(page, main_html, current=None):
    canonical = url(page["path"])
    robots = page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    graph = [org_schema(), website_schema()] + page.get("schema", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    ld = ld.replace("</", "<\\/")
    og_type = "article" if page.get("kind") in ("blog", "event") else "website"
    art = ""
    if page.get("published"):
        art += f'<meta property="article:published_time" content="{page["published"]}">\n'
        art += f'<meta property="article:modified_time" content="{page.get("updated") or page["published"]}">\n'
        art += f'<meta property="article:author" content="{esc(SITE["blog_author"])}">\n'
    img = og_image(page.get("image") or "hero-fire-house")
    preload = page.get("preload", "")
    popup = "true" if SITE["popup_enabled"] and not page.get("no_popup") else "false"
    return f"""<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#FAF3E1">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE['brand'])}">
<meta property="og:title" content="{esc(page.get('og_title', page['title']))}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
{art}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(page.get('og_title', page['title']))}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{img}">
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/raleway-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{analytics_head()}<script>window.SD={{popupEnabled:{popup},popupDelay:{int(SITE['popup_delay_seconds'])}}};</script>
<script type="application/ld+json">{ld}</script>
</head>
<body class="{page.get('body_class', '')}">
{header_html(current or page['path'])}
<main id="main">
{main_html}
</main>
{footer_html()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{page.get('scripts', '')}
</body>
</html>
"""


def write(path, content):
    """Write a page for URL path `path` (a directory URL or a file name)."""
    if path.endswith("/"):
        out = os.path.join(PUB, path.strip("/"), "index.html") if path != "/" else os.path.join(PUB, "home.html")
    else:
        out = os.path.join(PUB, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)


def breadcrumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            items.append(f'<li><a href="{path}">{esc(name)}</a></li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def page_hero(page, extra_meta="", buttons=True, img=True):
    image = page.get("image") if img else None
    grid_cls = "page-hero-grid has-img" if image else "page-hero-grid"
    img_html = f'<div class="hero-img">{picture(image, "(min-width: 980px) 480px, 100vw", eager=True, max_w=1200)}</div>' if image else ""
    eyebrow = f'<p class="eyebrow">{esc(page["eyebrow"])}</p>' if page.get("eyebrow") else ""
    lead = f'<p class="lead">{page["lead_html"]}</p>' if page.get("lead_html") else ""
    btns = ""
    if buttons:
        btns = (f'<div class="btn-row"><a class="btn" href="/contact/" data-cta="hero">{SITE["cta_primary"]}</a>'
                f'<a class="btn btn-outline" href="{SITE["phone_href"]}" data-loc="hero">{icon("phone")}Call {SITE["phone_display"]}</a></div>')
    return f"""<section class="page-hero"><div class="container">
{breadcrumbs_html(page['crumbs'])}
<div class="{grid_cls}"><div>
{eyebrow}<h1>{esc(page['h1'])}</h1>
{lead}{extra_meta}{btns}
</div>{img_html}</div></div></section>"""


def sidebar_html(page, toc):
    parts = []
    if len(toc) >= 3:
        lis = "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in toc)
        parts.append(f'<nav class="side-card toc" aria-label="On this page"><h3>On this page</h3><ol>{lis}</ol></nav>')
    parts.append(f"""<div class="side-card dark">
<h3>Free Claim Review</h3>
<p>Tell us what happened and where the claim stands. A licensed Texas public adjuster will review it with you.</p>
<a class="btn" href="/contact/" data-cta="sidebar">{SITE['cta_primary']}</a>
<a class="btn btn-ghost-light" href="{SITE['phone_href']}" data-loc="sidebar">{icon('phone')}{SITE['phone_display']}</a>
<p class="small">{esc(SITE['company'])} &middot; TDI License #{SITE['license_number']}</p>
</div>""")
    rel = [p.strip() for p in page.get("related", "").split(",") if p.strip()]
    if rel:
        lis = "".join(f'<li><a href="{p}">{esc(TITLES.get(p, p))}</a></li>' for p in rel)
        parts.append(f'<div class="side-card"><h3>Related</h3><ul class="related-list">{lis}</ul></div>')
    parts.append(f"""<div class="side-card"><h3>Claim tools</h3><ul class="related-list">
<li><a href="/tools/smoke-damage-scope-calculator/">Smoke Damage Scope Calculator</a></li>
<li><a href="/tools/contents-rcv-acv-calculator/">Contents RCV / ACV Calculator</a></li></ul></div>""")
    return f'<aside class="sidebar" aria-label="Sidebar"><div class="sidebar-sticky">{"".join(parts)}</div></aside>'


# --------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------
TITLES = {}          # path -> short display title (for related links)
ALL_PAGES = []       # every indexable page (for sitemap/admin manifest)


def load_md(fp, kind):
    raw = open(fp, encoding="utf-8").read()
    meta, body = parse_front_matter(raw)
    meta["body"] = body
    meta["kind"] = kind
    meta["source"] = os.path.relpath(fp, ROOT)
    return meta


def lead_html(text):
    r = Renderer(MD_CTX)
    return r.inline(text) if text else ""


def build_crumbs(page, parent_label=None):
    crumbs = [("Home", "/")]
    parent = page.get("parent")
    if parent:
        crumbs.append((parent_label or TITLES.get(parent, parent.strip("/").title()), parent))
    crumbs.append((page.get("breadcrumb") or page["h1"], page["path"]))
    return crumbs


def render_md_page(page, extra_after="", extra_before="", schema_extra=None, hero_meta="", show_sidebar=True):
    r = Renderer(MD_CTX)
    body_html = r.render(page["body"])
    page["words"] = word_count(body_html)
    page["lead_html"] = lead_html(page.get("lead", ""))
    page.setdefault("crumbs", build_crumbs(page))
    schema = [webpage_schema(page, {"AboutPage": "AboutPage", "ContactPage": "ContactPage"}.get(page.get("schema"), "WebPage"))]
    if len(page["crumbs"]) > 1:
        schema.append(breadcrumb_schema(page["crumbs"]))
    st = page.get("schema", "WebPage")
    if st == "Service":
        schema.append(service_schema(page, page.get("area_schema")))
    if st == "Article" or page.get("kind") in ("blog", "event"):
        schema.append(article_schema(page))
    if page.get("kind") == "blog":
        schema.append(person_schema())
    if r.faqs:
        schema.append(faq_schema(page["path"], r.faqs))
    if schema_extra:
        schema += schema_extra
    page["schema"] = schema
    page["faq_count"] = len(r.faqs)
    updated = ""
    if page.get("updated") and page.get("kind") not in ("blog",):
        label = "Last reviewed" if page.get("reviewed") else "Updated"
        updated = f'<p class="page-meta"><span>{label}: <strong>{fmt_date(page.get("reviewed") or page["updated"])}</strong></span></p>'
    hero = page_hero(page, extra_meta=hero_meta or updated)
    disclaimer = f'<aside class="note" style="margin-top:40px"><p class="note-title">Educational information</p><p>{esc(DISCLAIMER)}</p></aside>'
    if page.get("no_disclaimer"):
        disclaimer = ""
    if show_sidebar:
        main = f"""{hero}
<div class="container article-layout">
<article class="prose">{extra_before}{body_html}{extra_after}{disclaimer}</article>
{sidebar_html(page, r.toc)}
</div>"""
    else:
        main = f"""{hero}<div class="container-narrow" style="padding:56px 0 72px"><article class="prose">{extra_before}{body_html}{extra_after}</article></div>"""
    return main


def final_cta(title="Need Help With a Smoke Damage Claim Anywhere in Texas?",
              text="Tell us what happened and where the claim currently stands. A licensed Texas public adjuster can review it with you. No policy or claim number is required to start."):
    return f"""<section class="section section-sand cta-final"><div class="container">
<p class="eyebrow">Free Claim Review</p>
<h2>{esc(title)}</h2>
<p>{esc(text)}</p>
<div class="btn-row"><a class="btn" href="/contact/" data-cta="final">{SITE['cta_primary']}</a>
<a class="btn btn-dark" href="{SITE['phone_href']}" data-loc="final">{icon('phone')}Call {SITE['phone_display']}</a></div>
</div></section>"""


def register(page):
    """Record an indexable page for the sitemaps and the admin manifest."""
    ALL_PAGES.append({
        "path": page["path"], "title": page["title"], "description": page["description"],
        "kind": page.get("kind", "page"), "updated": page.get("updated") or page.get("published") or TODAY,
        "h1": page.get("h1", ""), "words": page.get("words", 0), "source": page.get("source", ""),
        "noindex": "noindex" in page.get("robots", ""),
        "keyword": page.get("keyword", ""),
    })


# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------

def build_pages(pages):
    special = {"/texas/", "/contact/", "/faq/"}
    for p in pages:
        if p["path"] in special:
            continue
        main = render_md_page(p, extra_after=("" if p["path"] in LEGAL else "") )
        if p["path"] not in LEGAL:
            main += final_cta()
        write(p["path"], render_page(p, main))
        register(p)


LEGAL = {"/privacy-policy/", "/terms-of-use/", "/disclaimer/"}


def build_faq(p):
    main = render_md_page(p) + final_cta()
    write(p["path"], render_page(p, main))
    register(p)


def contact_form(source="contact"):
    statuses = ["Not Yet Filed", "Claim Filed", "Already Inspected", "Partially Paid", "Denied", "Delayed",
                "Underpaid", "Closed Claim", "Not Sure"]
    ptypes = ["Single-family home", "Condo / townhome", "Rental property", "Multifamily / apartments",
              "Office", "Retail", "Restaurant", "Warehouse / industrial", "Church / nonprofit",
              "HOA / association", "Other commercial", "Other"]
    damages = ["Smoke", "Soot", "Fire", "Odor", "Contents", "HVAC", "Water From Fire Suppression", "Commercial Loss", "Other"]
    opt = lambda xs: "".join(f'<option value="{esc(x)}">{esc(x)}</option>' for x in xs)
    chips = "".join(f'<label class="chip"><input type="checkbox" name="damage[]" value="{esc(x)}"><span>{esc(x)}</span></label>' for x in damages)
    return f"""<form class="form-card" id="claim-form" action="/api/lead.php" method="post" enctype="multipart/form-data" novalidate>
<h2 style="font-size:1.6rem">Request a Free Claim Review</h2>
<p>Fields marked <span class="req" aria-hidden="true">*</span><span class="sr-only">with an asterisk</span> are required. No policy number or claim number is needed.</p>
<div class="form-grid">
<div class="field"><label for="f-name">Full Name <span class="req" aria-hidden="true">*</span></label><input id="f-name" name="full_name" autocomplete="name" required maxlength="120"></div>
<div class="field"><label for="f-phone">Phone <span class="req" aria-hidden="true">*</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="30"></div>
<div class="field"><label for="f-email">Email <span class="req" aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
<div class="field"><label for="f-ptype">Property Type</label><select id="f-ptype" name="property_type"><option value="">Select…</option>{opt(ptypes)}</select></div>
<div class="field"><label for="f-city">Texas City <span class="req" aria-hidden="true">*</span></label><input id="f-city" name="city" autocomplete="address-level2" required maxlength="80"></div>
<div class="field"><label for="f-zip">ZIP Code</label><input id="f-zip" name="zip" autocomplete="postal-code" inputmode="numeric" maxlength="5" pattern="[0-9]{{5}}"></div>
<div class="field"><label for="f-date">Date of Loss</label><input id="f-date" name="date_of_loss" type="date" max="{TODAY}"></div>
<div class="field"><label for="f-ins">Insurance Company</label><input id="f-ins" name="insurance_company" maxlength="120"></div>
<div class="field full"><label for="f-status">Claim Status</label><select id="f-status" name="claim_status"><option value="">Select…</option>{opt(statuses)}</select></div>
<fieldset class="field full"><legend>Damage Types <span class="hint">(select any that apply)</span></legend><div class="chips">{chips}</div></fieldset>
<div class="field full"><label for="f-msg">Briefly describe what happened.</label><textarea id="f-msg" name="message" maxlength="5000"></textarea></div>
<div class="field full"><label for="f-files">Optional uploads <span class="hint">— carrier estimate, photos, denial letter or other claim documents (PDF, JPG, PNG, HEIC, DOC/DOCX; up to 8 files, 20 MB total)</span></label>
<input id="f-files" name="files[]" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.heic,.heif,.webp,.doc,.docx,.xls,.xlsx,.txt"></div>
<div class="hp-field" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="started_at" value="">
<input type="hidden" name="source" value="{esc(source)}">
<div class="full"><p class="consent">By submitting this form, you agree to be contacted by phone, text, or email regarding your request.</p>
<button class="btn" type="submit" style="margin-top:12px">Request a Free Claim Review</button>
<div class="form-status" role="status" aria-live="polite"></div></div>
</div>
</form>"""


def build_contact(p):
    r = Renderer(MD_CTX)
    body = r.render(p["body"])
    p["lead_html"] = lead_html(p.get("lead", ""))
    p["crumbs"] = build_crumbs(p)
    p["schema"] = [webpage_schema(p, "ContactPage"), breadcrumb_schema(p["crumbs"])]
    p["no_popup"] = True
    addr = f'<li><small>Licensed address</small>{esc(SITE["licensed_address"])}</li>' if SITE["licensed_address"] else ""
    main = f"""{page_hero(p, buttons=False, img=False)}
<div class="container contact-layout">
<div class="prose">{body}
<ul class="contact-points">
<li><small>Call</small><a href="{SITE['phone_href']}" data-loc="contact">{SITE['phone_display']}</a></li>
<li><small>Email</small><a href="mailto:{SITE['email']}" data-loc="contact">{SITE['email']}</a></li>
<li><small>Licensed company</small>{esc(SITE['company'])}<br>{esc(SITE['license_label'])}</li>{addr}
<li><small>Service area</small>All of Texas — residential and commercial property</li>
</ul></div>
<div>{contact_form()}</div>
</div>"""
    write(p["path"], render_page(p, main))
    register(p)
    # thank-you page (noindex)
    ty = {"path": "/contact/thank-you/", "title": "Thank You | Smoke Damage Public Adjuster",
          "description": "Your claim review request was received.", "h1": "Thank you — we received your request",
          "robots": "noindex, nofollow", "no_popup": True, "crumbs": [("Home", "/"), ("Contact", "/contact/"), ("Thank You", "/contact/thank-you/")],
          "eyebrow": "Request received",
          "lead_html": "A licensed Texas public adjuster will review what you sent and follow up using the contact details you provided. If the situation is urgent, call us now."}
    ty["schema"] = []
    main = page_hero(ty, img=False, buttons=False) + f"""<div class="container-narrow" style="padding:48px 0 80px"><div class="prose">
<p>While you wait, it can help to keep claim documents together in one place: the carrier's estimate and letters, photos and video, receipts, and a running list of affected items.</p>
<div class="btn-row"><a class="btn btn-dark" href="{SITE['phone_href']}" data-loc="thank-you">{icon('phone')}Call {SITE['phone_display']}</a>
<a class="btn btn-outline" href="/tools/contents-rcv-acv-calculator/">Start a contents inventory</a></div></div></div>"""
    write(ty["path"], render_page(ty, main))


def build_texas_hub(p, locations):
    cards = []
    for loc in sorted(locations, key=lambda x: x["city"]):
        cards.append(f'<a class="card card-link" href="{loc["path"]}"><h3>{esc(loc["city"])}</h3>'
                     f'<p>{esc(loc.get("county", ""))}{" · " + esc(loc["region"]) if loc.get("region") else ""}</p></a>')
    grid = f'<h2 id="texas-cities">Texas cities we serve</h2><p>Every page below covers local property types and claim considerations for that area. We represent policyholders anywhere in Texas — if your city is not listed, we can still help.</p><div class="card-grid">{"".join(cards)}</div>'
    mapblock = f'<div class="tx-map" style="margin:28px 0">{texas_map_svg(locations)}</div>'
    main = render_md_page(p, extra_before=mapblock, extra_after=grid) + final_cta()
    p["schema"].append({"@type": "ItemList", "@id": url(p["path"]) + "#cities", "itemListElement": [
        {"@type": "ListItem", "position": i, "url": url(l["path"]), "name": l["city"]}
        for i, l in enumerate(sorted(locations, key=lambda x: x["city"]), 1)]})
    write(p["path"], render_page(p, main))
    register(p)


def build_locations(locations):
    by_slug = {l["path"]: l for l in locations}
    for loc in locations:
        loc.setdefault("parent", "/texas/")
        loc["crumbs"] = [("Home", "/"), ("Texas Areas", "/texas/"), (loc.get("breadcrumb") or loc["city"], loc["path"])]
        loc["area_schema"] = {"@type": "City", "name": f'{loc["city"]}, Texas'}
        nearby = [n.strip() for n in loc.get("nearby", "").split(",") if n.strip()]
        near_html = ""
        if nearby:
            items = []
            for n in nearby:
                path = f"/texas/{slugify(n)}/"
                items.append(f'<li><a href="{path}">{esc(n)}</a></li>' if path in by_slug else f"<li><span>{esc(n)}</span></li>")
            near_html = f'<h2 id="nearby-communities">Nearby communities we serve</h2><ul class="city-cloud">{"".join(items)}</ul>'
        meta = f'<p class="page-meta"><span>County: <strong>{esc(loc.get("county", ""))}</strong></span><span>Region: <strong>{esc(loc.get("region", ""))}</strong></span></p>'
        main = render_md_page(loc, extra_after=near_html, hero_meta=meta)
        main += final_cta(title=f"Need Help With a Smoke Damage Claim in {loc['city']}?")
        write(loc["path"], render_page(loc, main))
        register(loc)


def post_card(p, meta_line):
    img = picture(p.get("image") or "smoke-interior", "(min-width: 1100px) 360px, (min-width: 700px) 50vw, 100vw", max_w=800)
    return (f'<a class="post-card" href="{p["path"]}"><div class="pc-img">{img}</div><div class="pc-body">'
            f'<p class="pc-meta">{meta_line}</p><h3>{esc(p["h1"])}</h3><p>{esc(p["description"])}</p></div></a>')


def build_blog(posts):
    published = sorted([p for p in posts if p.get("status", "published") == "published"],
                       key=lambda x: x.get("published", ""), reverse=True)
    for p in published:
        p["parent"] = "/blog/"
        p["crumbs"] = [("Home", "/"), ("Blog", "/blog/"), (p.get("breadcrumb") or p["h1"], p["path"])]
        p["schema_type"] = "Article"
        author = p.get("author") or SITE["blog_author"]
        initials = "".join(x[0] for x in author.split()[:2])
        meta = (f'<p class="page-meta"><span>By <strong>{esc(author)}</strong></span>'
                f'<span>Published <strong>{fmt_date(p["published"])}</strong></span>'
                + (f'<span>Updated <strong>{fmt_date(p["updated"])}</strong></span>' if p.get("updated") and p["updated"] != p["published"] else "")
                + (f'<span>{esc(p["category"])}</span>' if p.get("category") else "") + "</p>")
        author_box = (f'<div class="author-box"><div class="author-avatar" aria-hidden="true">{esc(initials)}</div><div>'
                      f'<p><strong>{esc(author)}</strong></p><p>Writes Smoke Damage Public Adjuster\'s guides for Texas property owners dealing with smoke and fire insurance claims.</p></div></div>')
        main = render_md_page(p, extra_after=author_box, hero_meta=meta) + final_cta()
        write(p["path"], render_page(p, main))
        register(p)
    # index
    idx = {"path": "/blog/", "title": "Smoke & Fire Claim Resource Center | Blog",
           "description": "Guides for Texas property owners on smoke damage, fire claims, soot, contents inventories and working through a property insurance claim.",
           "h1": "Smoke & Fire Claim Resource Center", "eyebrow": "Blog", "crumbs": [("Home", "/"), ("Blog", "/blog/")],
           "lead_html": "Plain-English guides on documenting smoke and fire damage, understanding carrier estimates, and organizing a property insurance claim in Texas.",
           "image": None}
    cards = "".join(post_card(p, f'{esc(p.get("category") or "Guide")} · {fmt_date(p["published"])}') for p in published)
    if not cards:
        cards = '<div class="empty-state"><p>New articles are published regularly. Check back soon.</p></div>'
    idx["schema"] = [webpage_schema(idx, "CollectionPage"), breadcrumb_schema(idx["crumbs"]),
                     {"@type": "ItemList", "@id": url("/blog/") + "#posts", "itemListElement": [
                         {"@type": "ListItem", "position": i, "url": url(p["path"])} for i, p in enumerate(published, 1)]}]
    main = page_hero(idx, img=False) + f'<section class="section-sm"><div class="container"><div class="post-grid">{cards}</div></div></section>' + final_cta()
    write("/blog/", render_page(idx, main))
    register(idx)
    return published


def build_events(events):
    published = sorted([e for e in events if e.get("status", "published") == "published"],
                       key=lambda x: x.get("event_date", ""), reverse=True)
    for e in published:
        e["crumbs"] = [("Home", "/"), ("Texas Fire & Smoke Events", "/texas-fire-smoke-events/"), (e.get("breadcrumb") or e["h1"], e["path"])]
        e["updated"] = e.get("last_updated") or e.get("updated") or TODAY
        e["published"] = e.get("published") or e.get("event_date")
        facts = [("Date", fmt_date(e.get("event_date", ""))), ("County", e.get("county")), ("City / area", e.get("area")),
                 ("Event type", e.get("event_type")), ("Acreage", e.get("acreage")), ("Structures affected", e.get("structures")),
                 ("Evacuations", e.get("evacuations")), ("Last updated", fmt_date(e["updated"]))]
        dl = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in facts if v)
        before = f'<dl class="event-facts">{dl}</dl>'
        note = ('<aside class="note"><p class="note-title">About this event page</p><p>This page summarizes publicly reported incident information from the sources listed below. '
                'It does not mean that any particular property was damaged or that any insurance claim is covered. Coverage depends on the individual policy and the facts of each loss.</p></aside>')
        e["schema"] = "Article"
        main = render_md_page(e, extra_before=before, extra_after=note, hero_meta="")
        main += final_cta(title="If Your Texas Property Was Affected by Smoke or Fire, Request a Free Claim Review.")
        write(e["path"], render_page(e, main))
        register(e)
    idx = {"path": "/texas-fire-smoke-events/", "title": "Texas Fire & Smoke Events | Verified Event Archive",
           "description": "A verified archive of significant Texas wildfires, commercial and industrial fires, and smoke events, with official sources.",
           "h1": "Texas Fire & Smoke Events", "eyebrow": "Event Archive", "crumbs": [("Home", "/"), ("Texas Fire & Smoke Events", "/texas-fire-smoke-events/")],
           "lead_html": "Significant Texas fire and smoke events, summarized from official and reputable sources. We review official sources weekly and add an event only when it meets our criteria — and never publish filler.",
           "image": "wildfire"}
    cards = "".join(post_card(e, f'{esc(e.get("event_type", "Event"))} · {fmt_date(e.get("event_date", ""))} · {esc(e.get("county", ""))}') for e in published)
    if not cards:
        cards = '<div class="empty-state"><p>No events are listed yet. Qualifying events are added after verification.</p></div>'
    criteria = """<div class="prose" style="margin-top:48px;max-width:860px">
<h2>How events are selected</h2>
<p>We check official sources each week — the Texas A&amp;M Forest Service, InciWeb, the Texas State Fire Marshal's Office, TCEQ, county emergency management offices, city fire departments, and the National Weather Service — with reputable local news used only for additional confirmation.</p>
<p>An event is added when it is verified by at least one authoritative source (two independent sources for material details where possible) and involves things like property damage, evacuations, multiple structures, large acreage, major commercial impact, or an official incident declaration. We do not add an event because smoke was smelled or air quality dipped, and we never estimate acreage, damage counts, causes or insurance eligibility.</p>
<h2>Property insurance considerations after a smoke or fire event</h2>
<p>Being near a fire does not by itself mean a property has a covered insurance claim. If your property was affected, the practical first steps are to follow official safety instructions, notify your insurer, and document conditions with photos, video and notes before items are discarded. Coverage depends on the individual policy and the facts of the loss. See <a href="/smoke-damage-claims/">smoke damage claims</a> and the <a href="/tools/smoke-damage-scope-calculator/">Smoke Damage Scope Calculator</a> for help organizing documentation.</p>
</div>"""
    idx["schema"] = [webpage_schema(idx, "CollectionPage"), breadcrumb_schema(idx["crumbs"])]
    main = page_hero(idx) + f'<section class="section-sm"><div class="container"><div class="post-grid">{cards}</div>{criteria}</div></section>' + final_cta(title="If Your Texas Property Was Affected by Smoke or Fire, Request a Free Claim Review.")
    write(idx["path"], render_page(idx, main))
    register(idx)
    return published


def build_history(timeline):
    idx = {"path": "/texas-fire-smoke-history/", "title": "Texas Fire & Smoke History | Major Events Timeline",
           "description": "A factual timeline of significant Texas wildfires, industrial fires and smoke events, with sources and the property-claim issues they raise.",
           "h1": "Texas Fire & Smoke History", "eyebrow": "Historical Timeline",
           "crumbs": [("Home", "/"), ("Texas Fire & Smoke History", "/texas-fire-smoke-history/")],
           "lead_html": "Significant Texas fire and smoke events, organized by year and summarized from official and reputable sources. The goal is context — not sensationalism.",
           "image": "texas-landscape", "updated": TODAY}
    years = {}
    for ev in timeline:
        years.setdefault(ev["year"], []).append(ev)
    ynav = "".join(f'<li><a href="#y{y}">{y}</a></li>' for y in sorted(years, reverse=True))
    parts = []
    for y in sorted(years, reverse=True):
        parts.append(f'<h2 class="history-year" id="y{y}">{y}</h2>')
        for ev in years[y]:
            src = " · ".join(f'<a href="{esc(s["url"])}" rel="noopener" target="_blank">{esc(s["title"])}</a>' for s in ev.get("sources", []))
            impacts = f'<p><strong>Verified property impacts:</strong> {esc(ev["impacts"])}</p>' if ev.get("impacts") else ""
            ins = f'<p><strong>Claim considerations:</strong> {esc(ev["insurance_note"])}</p>' if ev.get("insurance_note") else ""
            parts.append(f"""<article class="history-item" id="{esc(ev['id'])}"><h3>{esc(ev['name'])}</h3>
<div class="h-meta"><span class="h-type">{esc(ev['type'])}</span><span>{esc(ev['date'])}</span><span>{esc(ev['location'])}</span></div>
<p>{esc(ev['summary'])}</p>{impacts}{ins}<p class="h-src">Sources: {src}</p></article>""")
    intro = """<div class="prose" style="max-width:860px">
<p>Texas has a long record of large wildfires, refinery and chemical-plant fires, and urban fires. Looking back at them is useful for one practical reason: each kind of event tends to create a different mix of property insurance questions.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Issue</th><th scope="col">Why it comes up after major fire events</th></tr></thead><tbody>
<tr><td>Direct damage</td><td>Flame and heat damage to structures, fences, outbuildings, vehicles and equipment.</td></tr>
<tr><td>Smoke</td><td>Smoke can reach properties that never saw flame, including neighboring homes and businesses, and may require room-by-room documentation.</td></tr>
<tr><td>Soot</td><td>Residue on surfaces, contents and HVAC components can raise cleaning-versus-replacement questions.</td></tr>
<tr><td>Water from firefighting</td><td>Suppression water can damage drywall, flooring, insulation and contents in addition to the fire itself.</td></tr>
<tr><td>Contents</td><td>Personal property and business inventory often require detailed inventories and valuation.</td></tr>
<tr><td>Additional living expenses</td><td>When a home is not habitable, temporary housing and related costs may be addressed under the policy's loss-of-use provisions.</td></tr>
<tr><td>Commercial interruption</td><td>Businesses may have business income or extra expense questions, depending on the policy.</td></tr>
</tbody></table></div>
<p>Coverage for any of these depends on the specific policy and the facts of each loss. For current events, see the <a href="/texas-fire-smoke-events/">Texas Fire &amp; Smoke Events</a> archive.</p>
</div>"""
    body = f'{intro}<ul class="year-nav" aria-label="Jump to year" style="margin-top:36px">{ynav}</ul>' + "".join(parts)
    idx["schema"] = [webpage_schema(idx), breadcrumb_schema(idx["crumbs"]),
                     {"@type": "Article", "@id": url(idx["path"]) + "#article", "headline": idx["h1"], "description": idx["description"],
                      "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "dateModified": TODAY,
                      "mainEntityOfPage": {"@id": url(idx["path"]) + "#webpage"}}]
    idx["words"] = word_count(body)
    main = page_hero(idx, extra_meta=f'<p class="page-meta"><span>Updated: <strong>{fmt_date(TODAY)}</strong></span></p>') + \
        f'<section class="section-sm"><div class="container" style="max-width:980px">{body}</div></section>' + final_cta()
    write(idx["path"], render_page(idx, main))
    register(idx)


def build_case_studies(cases):
    """Case studies publish only when real, approved entries exist."""
    pub = [c for c in cases if c.get("status") == "published" and c.get("approved") == "yes"]
    if not pub:
        return []
    for c in pub:
        c["crumbs"] = [("Home", "/"), ("Case Studies", "/case-studies/"), (c["h1"], c["path"])]
        main = render_md_page(c) + final_cta()
        write(c["path"], render_page(c, main))
        register(c)
    idx = {"path": "/case-studies/", "title": "Smoke & Fire Claim Case Studies | Texas",
           "description": "Approved examples of smoke and fire property claims handled for Texas policyholders.",
           "h1": "Case Studies", "crumbs": [("Home", "/"), ("Case Studies", "/case-studies/")], "image": None,
           "lead_html": "Every claim is different. Past results do not predict or guarantee the outcome of any other claim."}
    idx["schema"] = [webpage_schema(idx, "CollectionPage"), breadcrumb_schema(idx["crumbs"])]
    cards = "".join(post_card(c, esc(c.get("loss_type", ""))) for c in pub)
    write(idx["path"], render_page(idx, page_hero(idx, img=False) + f'<section class="section-sm"><div class="container"><div class="post-grid">{cards}</div></div></section>'))
    register(idx)
    return pub


# --------------------------------------------------------------------------
# Texas map
# --------------------------------------------------------------------------
CITY_COORDS = {
    "Houston": (29.7604, -95.3698), "Dallas": (32.7767, -96.7970), "Fort Worth": (32.7555, -97.3308),
    "Austin": (30.2672, -97.7431), "San Antonio": (29.4241, -98.4936), "El Paso": (31.7619, -106.4850),
    "Corpus Christi": (27.8006, -97.3964), "Beaumont": (30.0802, -94.1266), "Port Arthur": (29.8850, -93.9399),
    "Waco": (31.5493, -97.1467), "Killeen": (31.1171, -97.7278), "Temple": (31.0982, -97.3428),
    "Lubbock": (33.5779, -101.8552), "Amarillo": (35.2220, -101.8313), "Midland": (31.9973, -102.0779),
    "Odessa": (31.8457, -102.3676), "McAllen": (26.2034, -98.2300), "Edinburg": (26.3017, -98.1633),
    "Brownsville": (25.9017, -97.4975), "Harlingen": (26.1906, -97.6961), "Laredo": (27.5306, -99.4803),
    "College Station": (30.6280, -96.3344), "Bryan": (30.6744, -96.3700), "Tyler": (32.3513, -95.3011),
    "Longview": (32.5007, -94.7405), "Galveston": (29.3013, -94.7977), "Pearland": (29.5636, -95.2860),
    "Sugar Land": (29.6197, -95.6349), "Katy": (29.7858, -95.8245), "The Woodlands": (30.1658, -95.4613),
    "Round Rock": (30.5083, -97.6789), "Georgetown": (30.6333, -97.6780), "New Braunfels": (29.7030, -98.1245),
    "San Marcos": (29.8833, -97.9414), "Arlington": (32.7357, -97.1081), "Plano": (33.0198, -96.6989),
    "Frisco": (33.1507, -96.8236), "McKinney": (33.1972, -96.6398), "Irving": (32.8140, -96.9489),
    "Garland": (32.9126, -96.6389),
}
MAJOR = {"Houston", "Dallas", "Fort Worth", "Austin", "San Antonio", "El Paso", "Corpus Christi", "Lubbock",
         "Amarillo", "Midland", "McAllen", "Laredo", "Beaumont", "Waco", "Tyler"}
LABELLED = MAJOR | {"Galveston", "Brownsville", "Odessa", "College Station"}


def texas_map_svg(locations=None, width=640):
    outline = json.load(open(os.path.join(ROOT, "src", "texas-outline.json")))
    lat0 = 31.0
    kx = math.cos(math.radians(lat0))
    minx, maxx = -106.65 * kx, -93.5 * kx
    miny, maxy = 25.84, 36.5
    scale = (width - 20) / (maxx - minx)
    height = round((maxy - miny) * scale + 20)

    def pt(lat, lng):
        return (10 + (lng * kx - minx) * scale, 10 + (maxy - lat) * scale)

    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (pt(la, lo) for lo, la in outline)) + " Z"
    have = {l["city"]: l["path"] for l in (locations or [])}
    dots = []
    for name in MARKETS:
        if name not in CITY_COORDS:
            continue
        x, y = pt(*CITY_COORDS[name])
        cls = "tx-city major" if name in MAJOR else "tx-city"
        r = 5.5 if name in MAJOR else 3.6
        label = ""
        if name in LABELLED:
            anchor = "end" if x > width * 0.72 else "start"
            dx = -8 if anchor == "end" else 8
            label = f'<text x="{x + dx:.1f}" y="{y + 4:.1f}" text-anchor="{anchor}">{esc(name)}</text>'
        circle = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"><title>{esc(name)}</title></circle>'
        if name in have:
            dots.append(f'<a class="{cls}" href="{have[name]}" aria-label="{esc(name)}">{circle}{label}</a>')
        else:
            dots.append(f'<g class="{cls}">{circle}{label}</g>')
    return (f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="txmap-t"><title id="txmap-t">Map of Texas showing major markets served statewide</title>'
            f'<path class="tx-shape" d="{d}"/>{"".join(dots)}</svg>')


# --------------------------------------------------------------------------
# Sitemaps, robots, admin manifest
# --------------------------------------------------------------------------

def build_sitemaps():
    pages = [p for p in ALL_PAGES if not p["noindex"]]
    seen = set()
    rows = []
    for p in sorted(pages, key=lambda x: (x["path"] != "/", x["path"])):
        if p["path"] in seen:
            continue
        seen.add(p["path"])
        rows.append(f"<url><loc>{url(p['path'])}</loc><lastmod>{p['updated'][:10]}</lastmod></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(PUB, "sitemap.xml"), "w") as f:
        f.write(xml)
    # keep the old Rank Math index URL alive, pointing at the new sitemap
    with open(os.path.join(PUB, "sitemap_index.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f'<sitemap><loc>{url("/sitemap.xml")}</loc><lastmod>{TODAY}</lastmod></sitemap>\n</sitemapindex>\n')
    with open(os.path.join(PUB, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /admin/\nDisallow: /api/\nDisallow: /contact/thank-you/\nDisallow: /home.html\n"
                "Disallow: /*?s=\nDisallow: /search/\n\n"
                f"Sitemap: {url('/sitemap.xml')}\n")
    # HTML sitemap
    groups = [("Main pages", lambda p: p["kind"] in ("page", "home", "tool") and not p["path"].startswith("/texas/")),
              ("Texas service areas", lambda p: p["path"].startswith("/texas/")),
              ("Articles", lambda p: p["kind"] == "blog"),
              ("Fire & smoke events", lambda p: p["kind"] == "event")]
    cols = []
    for title, fn in groups:
        items = sorted({p["path"]: p for p in pages if fn(p)}.values(), key=lambda x: x["path"])
        if not items:
            continue
        lis = "".join(f'<li><a href="{p["path"]}">{esc(p["h1"] or p["title"])}</a></li>' for p in items)
        cols.append(f"<div><h2 style='font-size:1.3rem'>{title}</h2><ul>{lis}</ul></div>")
    sm = {"path": "/sitemap/", "title": "Sitemap | Smoke Damage Public Adjuster", "description": "Every page on SmokeDamage.com, grouped by section.",
          "h1": "Sitemap", "crumbs": [("Home", "/"), ("Sitemap", "/sitemap/")], "robots": "noindex, follow", "kind": "page"}
    sm["schema"] = [webpage_schema(sm)]
    main = page_hero(sm, img=False, buttons=False) + f'<section class="section-sm"><div class="container sitemap-cols">{"".join(cols)}</div></section>'
    write("/sitemap/", render_page(sm, main))


def build_404():
    p = {"path": "/404.html", "title": "Page Not Found | Smoke Damage Public Adjuster", "description": "The page you requested could not be found.",
         "h1": "Page not found", "robots": "noindex, follow", "schema": []}
    main = f"""<section class="notfound"><div class="container-narrow">
<p class="eyebrow">404</p><h1>We couldn't find that page.</h1>
<p>The page may have moved. Try one of these instead, or call us if you need help with a smoke or fire claim.</p>
<div class="btn-row"><a class="btn" href="/">Home</a><a class="btn btn-outline" href="/smoke-damage-claims/">Smoke Damage Claims</a><a class="btn btn-outline" href="/contact/">Free Claim Review</a></div>
</div></section>"""
    html_ = render_page(p, main).replace(f'<link rel="canonical" href="{url("/404.html")}">\n', "")
    with open(os.path.join(PUB, "404.html"), "w") as f:
        f.write(html_)


def write_private(posts_all, events_all, locations):
    os.makedirs(PRIV, exist_ok=True)
    kq = []
    kq_path = os.path.join(ROOT, "content", "keyword-queue.csv")
    if os.path.exists(kq_path):
        kq = list(csv.DictReader(open(kq_path, encoding="utf-8")))
    scan = {}
    sp = os.path.join(ROOT, "content", "events", "_scan-log.json")
    if os.path.exists(sp):
        scan = json.load(open(sp))
    auto = {}
    ap = os.path.join(ROOT, "content", "automation-status.json")
    if os.path.exists(ap):
        auto = json.load(open(ap))
    manifest = {
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "pages": sorted(ALL_PAGES, key=lambda p: p["path"]),
        "blog": [{"path": p["path"], "title": p["title"], "status": p.get("status", "published"), "published": p.get("published", ""),
                  "keyword": p.get("keyword", ""), "source": p["source"], "check": p.get("check", "")} for p in posts_all],
        "events": [{"path": e["path"], "title": e["h1"], "status": e.get("status", "published"), "event_date": e.get("event_date", ""),
                    "county": e.get("county", ""), "source": e["source"]} for e in events_all],
        "locations": [{"path": l["path"], "city": l["city"], "county": l.get("county", ""), "words": l.get("words", 0)} for l in locations],
        "keyword_queue": kq,
        "event_scan": scan,
        "automation": auto,
        "site": {k: SITE[k] for k in ("brand", "company", "license_number", "licensed_address", "phone_display", "email",
                                        "lead_recipient", "popup_enabled", "popup_delay_seconds", "blog_author", "ga4_id")},
    }
    with open(os.path.join(PRIV, "site-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def copy_static():
    for d in ("assets",):
        src = os.path.join(ROOT, d)
        dst = os.path.join(PUB, d)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    for fp in glob.glob(os.path.join(ROOT, "src", "root", "*")) + glob.glob(os.path.join(ROOT, "src", "root", ".*")):
        if os.path.isfile(fp):
            shutil.copy2(fp, PUB)
    # PHP layer
    shutil.copytree(os.path.join(ROOT, "src", "php"), PUB, dirs_exist_ok=True)


def main():
    if os.path.exists(PUB):
        shutil.rmtree(PUB)
    os.makedirs(PUB)
    copy_static()

    pages = [load_md(f, "page") for f in sorted(glob.glob(os.path.join(ROOT, "content", "pages", "*.md")))]
    locations = [load_md(f, "location") for f in sorted(glob.glob(os.path.join(ROOT, "content", "locations", "*.md")))]
    posts = [load_md(f, "blog") for f in sorted(glob.glob(os.path.join(ROOT, "content", "blog", "*.md")))]
    events = [load_md(f, "event") for f in sorted(glob.glob(os.path.join(ROOT, "content", "events", "*.md")))]
    cases = [load_md(f, "case") for f in sorted(glob.glob(os.path.join(ROOT, "content", "case-studies", "*.md")))
             if not os.path.basename(f).startswith("_")]
    timeline = []
    tp = os.path.join(ROOT, "content", "history", "timeline.json")
    if os.path.exists(tp):
        timeline = json.load(open(tp))

    for p in pages + locations + posts + events:
        TITLES[p["path"]] = p.get("breadcrumb") or p.get("h1") or p["title"]
    TITLES.update({"/tools/smoke-damage-scope-calculator/": "Smoke Damage Scope Calculator",
                   "/tools/contents-rcv-acv-calculator/": "Contents RCV / ACV Calculator", "/tools/": "Claim Tools",
                   "/texas-fire-smoke-events/": "Texas Fire & Smoke Events", "/texas-fire-smoke-history/": "Texas Fire & Smoke History",
                   "/blog/": "Blog", "/contact/": "Free Claim Review", "/texas/": "Texas Service Areas"})

    by_path = {p["path"]: p for p in pages}
    build_pages(pages)
    if "/faq/" in by_path:
        build_faq(by_path["/faq/"])
    if "/contact/" in by_path:
        build_contact(by_path["/contact/"])
    build_locations(locations)
    if "/texas/" in by_path:
        build_texas_hub(by_path["/texas/"], locations)
    published_posts = build_blog(posts)
    published_events = build_events(events)
    build_history(timeline)
    build_case_studies(cases)

    import home
    import tools
    home.build(sys_mod(), locations, published_posts, published_events)
    tools.build(sys_mod())

    build_sitemaps()
    build_404()
    write_private(posts, events, locations)
    print(f"built {len(ALL_PAGES)} indexable pages -> {os.path.relpath(PUB, os.getcwd())}")


def sys_mod():
    import sys
    return sys.modules[__name__]


if __name__ == "__main__":
    import sys
    sys.modules.setdefault("build", sys.modules[__name__])
    main()
