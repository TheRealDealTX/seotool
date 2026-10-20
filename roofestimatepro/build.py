#!/usr/bin/env python3
"""Static site generator for roofestimatepro.com.

Renders every page from the shared layout here plus the page data under
content/, copies static/ alongside, and writes the deployable site to public/.

    python3 build.py              # production build (indexable)
    python3 build.py --staging    # temporary domain: noindex + robots Disallow
"""

import importlib
import json
import os
import pkgutil
import re
import shutil
import sys
from datetime import date

from siteconfig import BIZ, TOOLS, SERVICES, NAV, TEXAS_REGIONS, US_REGIONS, MATERIALS, WASTE, TODAY

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("REP_OUT") or os.path.join(ROOT, "public")  # REP_OUT lets parallel builds use their own dir
STAGING = "--staging" in sys.argv
ASSET_V = date.today().strftime("%Y%m%d")

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def url(path):
    return BIZ["origin"].rstrip("/") + path


def strip_tags(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


ICONS = {
    "house": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2"/><path d="m10 10 2 2"/><path d="m13 7 2 2"/>',
    "angle": '<path d="M3 20h18"/><path d="M3 20 17 6"/><path d="M9 20a6 6 0 0 0-1.8-4.2"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
    "panel": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8 4v16"/><path d="M13 4v16"/><path d="M18 4v16"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 8h1"/><path d="M14 8h1"/><path d="M9 12h1"/><path d="M14 12h1"/><path d="M10 21v-4h4v4"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "trend": '<path d="M3 6l7 7 4-4 7 7"/><path d="M21 10v6h-6"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "wind": '<path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h16a3 3 0 1 1-3 3"/><path d="M3 16h7"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8 11h.01"/><path d="M12 11h.01"/><path d="M16 11h.01"/><path d="M8 15h.01"/><path d="M12 15h.01"/><path d="M16 15v3"/>',
    "phone": '<path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "clip": '<path d="M9 4h6v3H9z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/><path d="M9 12h6"/><path d="M9 16h4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15"/><path d="M15 6v15"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "hardhat": '<path d="M3 18h18"/><path d="M5 18v-3a7 7 0 0 1 14 0v3"/><path d="M10 8V5h4v3"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    "file": '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}

# --------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------


def load_modules(pkg_name, attr):
    pkg = importlib.import_module(pkg_name)
    items = []
    for m in sorted(pkgutil.iter_modules(pkg.__path__), key=lambda m: m.name):
        mod = importlib.import_module(f"{pkg_name}.{m.name}")
        if hasattr(mod, attr):
            items.append(getattr(mod, attr))
    return items


TOOL_PAGES = {t["slug"]: t for t in load_modules("content.tools", "TOOL")}
POSTS = sorted(load_modules("content.blog", "POST"), key=lambda p: p["published"], reverse=True)

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------


def head(page):
    canonical = url(page["path"])
    og_image = url(page.get("og_image", "/assets/img/og-image.jpg"))
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    graph = [org_schema(), website_schema()] + page.get("schema", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    art = ""
    if page.get("published"):
        art = (f'<meta property="article:published_time" content="{page["published"]}">\n'
               f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    preload = page.get("preload", "")
    return f"""<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0a1211">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(page.get('og_title', page['title']))}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
{art}<link rel="preload" href="/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-800-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<script type="application/ld+json">{ld}</script>
</head>
"""


def header(active=None):
    mega = "".join(
        f'<a href="/tools/{t["slug"]}/"><span class="ico">{icon(t["icon"])}</span>'
        f'<span><strong>{esc(t["short"])}</strong><span>{esc(t["blurb"][:78].rsplit(" ", 1)[0])}…</span></span></a>'
        for t in TOOLS)
    links = []
    for label, href in NAV:
        if label == "Tools":
            cls = " is-active" if active == href else ""
            links.append(
                f'<div class="nav-drop{cls}"><button type="button" aria-expanded="false" aria-haspopup="true">'
                f'Tools {icon("chev")}</button><div class="mega">{mega}'
                f'<div class="mega-foot"><span>All 12 calculators are free, no sign-up.</span>'
                f'<a href="/tools/">Browse all tools →</a></div></div></div>')
        else:
            cur = ' aria-current="page"' if active == href else ""
            links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{BIZ['name']} home"><img src="/assets/img/logo-428.webp" width="428" height="101" alt="{BIZ['name']}"></a>
    <nav class="nav" id="site-nav" aria-label="Main">
      {''.join(links)}
      <a class="btn btn--peach nav-mobile-cta" href="/get-estimate/">Talk to an estimator</a>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{BIZ['phone_href']}">{icon('phone')}<span>{BIZ['phone_display']}</span></a>
      <a class="btn btn--peach btn--sm" href="/get-estimate/">Talk to an estimator</a>
    </div>
    <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu">{icon('menu')}</button>
  </div>
</header>
<main id="main">
"""


def footer(scripts=""):
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["short"])}</a></li>' for t in TOOLS[:8])
    services = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="/assets/img/logo-428.webp" width="428" height="101" alt="{BIZ['name']}" loading="lazy">
        <p>Free roof estimating tools and professional Xactimate estimates for contractors, adjusters and property
        owners. Based in Texas, serving every Texas county and clients across the U.S.</p>
        <div class="foot-contact">
          <a href="tel:{BIZ['phone_href']}">{icon('phone')}{BIZ['phone_display']}</a>
          <a href="mailto:{BIZ['email']}">{icon('mail')}{BIZ['email']}</a>
        </div>
      </div>
      <div><h3>Free tools</h3><ul>{tools}<li><a href="/tools/">All tools →</a></li></ul></div>
      <div><h3>Pro services</h3><ul>{services}<li><a href="/get-estimate/">Request an estimate</a></li><li><a href="/claim/">Submit a claim</a></li><li><a href="/get-a-scope/">Order a scope</a></li></ul></div>
      <div><h3>Company</h3><ul><li><a href="/about/">About</a></li><li><a href="/how-it-works/">How it works</a></li><li><a href="/areas/">Service areas</a></li><li><a href="/faqs/">FAQs</a></li><li><a href="/blog/">Blog</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
    </div>
    <div class="foot-bottom">
      <span>© <span data-year>{date.today().year}</span> {BIZ['name']}. Estimates from tools on this site are planning figures, not quotes.</span>
      <ul><li><a href="/privacy-policy/">Privacy</a></li><li><a href="/terms-of-use/">Terms</a></li></ul>
    </div>
  </div>
</footer>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{scripts}</body>
</html>
"""


def crumbs_html(trail):
    items = "".join(
        f'<li><a href="{href}">{esc(label)}</a></li>' if href else f'<li aria-current="page">{esc(label)}</li>'
        for label, href in trail)
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{items}</ol></nav>'


def hero_bg():
    return ('<div class="hero-bg" aria-hidden="true"><div class="tex"></div><div class="grid"></div>'
            '<div class="blob blob--teal"></div><div class="blob blob--peach"></div><div class="blob blob--deep"></div></div>')


def page_hero(page, trail, extra=""):
    kicker = f'<span class="kicker">{esc(page["kicker"])}</span>' if page.get("kicker") else ""
    lede = f'<p class="lede">{page["lede"]}</p>' if page.get("lede") else ""
    return f"""<section class="hero page-hero">{hero_bg()}
  <div class="wrap">
    {crumbs_html(trail)}
    {kicker}
    <h1>{page['h1']}</h1>
    {lede}
    {extra}
  </div>
</section>
"""


def cta_band(title="Need a number you can take to the bank, the bank or the carrier?",
             text="Our estimators build line-item Xactimate estimates for roofs anywhere in Texas and across the U.S. Send us what you have and we will tell you exactly what it takes."):
    return f"""<section class="section section--tight cta-section"><div class="wrap">
  <div class="cta-band" data-reveal>
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row"><a class="btn btn--peach" href="/get-estimate/">Talk to an estimator {icon('arrow')}</a>
    <a class="btn btn--ghost-light" href="tel:{BIZ['phone_href']}">{icon('phone')}{BIZ['phone_display']}</a></div>
  </div>
</div></section>
"""


def faq_html(faqs, heading="Frequently asked questions", intro=None, wrap=True):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="answer">{a}</div></details>' for q, a in faqs)
    i = f"<p>{intro}</p>" if intro else ""
    inner = f'<div class="section-head"><span class="kicker">FAQ</span><h2>{heading}</h2>{i}</div><div class="faq">{items}</div>'
    if not wrap:
        return inner
    return f'<section class="section section--paper" id="faq"><div class="wrap wrap--narrow">{inner}</div></section>'


def tool_card(t, tag=True):
    tg = f'<span class="tag">{t["group"]}</span>' if tag else ""
    return (f'<a class="tool-card" href="/tools/{t["slug"]}/" data-group="{t["group"]}" data-reveal>{tg}'
            f'<span class="ico">{icon(t["icon"])}</span><h3>{esc(t["name"])}</h3><p>{esc(t["blurb"])}</p>'
            f'<span class="go">Open calculator {icon("arrow")}</span></a>')


def post_card(p):
    return (f'<a class="post-card" href="/{p["slug"]}/" data-reveal><div class="thumb">'
            f'<img src="/assets/img/blog/{p["image"]}-640.webp" alt="{esc(p["image_alt"])}" loading="lazy" width="640" height="360"></div>'
            f'<div class="body"><span class="cat">{esc(p["category"])}</span><h3>{esc(p["h1"])}</h3>'
            f'<p>{esc(p["excerpt"])}</p><time datetime="{p["published"][:10]}">{fmt_date(p.get("modified", p["published"]))}</time></div></a>')


def fmt_date(iso):
    d = date.fromisoformat(iso[:10])
    return d.strftime("%B %-d, %Y")


def side_tools(exclude=None, n=6, title="Free estimating tools"):
    lis = "".join([f'<li><a href="/tools/{t["slug"]}/">{icon(t["icon"])}{esc(t["short"])}</a></li>'
                   for t in TOOLS if t["slug"] != exclude][:n])
    return f'<div class="side-card"><h3>{title}</h3><ul>{lis}</ul></div>'


def side_cta():
    return (f'<div class="side-card side-card--cta"><h3>Want a pro to run the numbers?</h3>'
            f'<p>Send photos, measurements or a carrier estimate. We build a line-item Xactimate estimate.</p>'
            f'<a class="btn btn--peach btn--sm" href="/get-estimate/">Request an estimate</a></div>')


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

ORG_ID = url("/#organization")


def org_schema():
    return {
        "@type": "ProfessionalService", "@id": ORG_ID, "name": BIZ["name"], "url": url("/"),
        "logo": {"@type": "ImageObject", "url": url("/assets/img/org-logo.webp"), "width": 1000, "height": 1000},
        "image": url("/assets/img/og-image.jpg"),
        "description": "Free roof estimating calculators and professional Xactimate roof estimates, claim estimate reviews and scopes of damages for Texas and the U.S.",
        "telephone": "+1-210-903-9471", "email": BIZ["email"], "priceRange": "$50–$1,000",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"],
                    "addressRegion": BIZ["state"], "postalCode": BIZ["zip"], "addressCountry": "US"},
        "areaServed": [{"@type": "State", "name": "Texas"}, {"@type": "Country", "name": "United States"}],
        "knowsAbout": ["Roof estimating", "Xactimate", "Insurance claim estimates", "Roofing takeoffs", "Scope of damages"],
    }


def website_schema():
    return {"@type": "WebSite", "@id": url("/#website"), "url": url("/"), "name": BIZ["name"],
            "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}


def webpage_schema(page, wtype="WebPage"):
    return {"@type": wtype, "@id": url(page["path"]) + "#webpage", "url": url(page["path"]), "name": page["title"],
            "description": page["description"], "isPartOf": {"@id": url("/#website")}, "inLanguage": "en-US",
            "dateModified": page.get("modified", TODAY)}


def breadcrumb_schema(trail, path):
    els = []
    for i, (label, href) in enumerate(trail, 1):
        els.append({"@type": "ListItem", "position": i, "name": label, "item": url(href or path)})
    return {"@type": "BreadcrumbList", "@id": url(path) + "#breadcrumb", "itemListElement": els}


def faq_schema(faqs, path):
    return {"@type": "FAQPage", "@id": url(path) + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]}


def tool_schema(t, page):
    return {"@type": "WebApplication", "@id": url(page["path"]) + "#app", "name": t["h1"], "url": url(page["path"]),
            "description": page["description"], "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORG_ID}}


# --------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------

WRITTEN = []  # (path, lastmod, priority) for sitemap.xml


def write(path, html, lastmod=None, priority="0.6", sitemap=True):
    if path == "/":
        fp = os.path.join(OUT, "home.html")
    elif path.endswith(".html"):
        fp = os.path.join(OUT, path.lstrip("/"))
    else:
        fp = os.path.join(OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    if sitemap:
        WRITTEN.append((path, lastmod or TODAY, priority))


def render(page, trail, main_html, active=None, scripts=""):
    schema = list(page.get("schema", []))
    if trail:
        schema.append(breadcrumb_schema(trail, page["path"]))
    page = dict(page, schema=schema)
    return head(page) + header(active) + main_html + footer(scripts)


def toc(body):
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    if len(heads) < 3:
        return ""
    lis = "".join(f'<li><a href="#{i}">{strip_tags(h)}</a></li>' for i, h in heads)
    return f'<nav class="toc" aria-label="On this page"><b>On this page</b><ol>{lis}</ol></nav>'


def ensure_h2_ids(body):
    def fix(m):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            return m.group(0)
        return f'<h2 id="{slugify(strip_tags(inner))[:60]}"{attrs}>{inner}</h2>'
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", fix, body)


# --------------------------------------------------------------------------
# Page builders
# --------------------------------------------------------------------------


def build_tool(t):
    if not isinstance(t["form"], str):
        t = dict(t, form="".join(t["form"]))
    meta = TOOL_BY_SLUG[t["slug"]]
    path = f"/tools/{t['slug']}/"
    page = {"path": path, "title": t["title"], "description": t["description"]}
    trail = [("Home", "/"), ("Tools", "/tools/"), (meta["short"], None)]
    page["schema"] = [webpage_schema(page), tool_schema(t, page), faq_schema(t["faqs"], path)]
    badges = ('<ul class="hero-badges"><li>' + icon("check") + "Free, no sign-up</li><li>" + icon("check")
              + "Texas 2026 unit prices</li><li>" + icon("check") + "Print, save or send to a pro</li></ul>")
    hero = page_hero({"h1": t["h1"], "lede": t["lede"], "kicker": meta["group"] + " tool"}, trail, badges)
    body = ensure_h2_ids(t["body"])
    related = "".join(tool_card(TOOL_BY_SLUG[s], tag=False) for s in t["related"] if s in TOOL_BY_SLUG)
    main = f"""{hero}
<section class="tool-shell"><div class="wrap">
  <div class="print-only print-head"><img src="/assets/img/logo-428.webp" alt="{BIZ['name']}" width="214" height="50"><div><b>{esc(t['h1'])}</b><br><time></time> · {BIZ['phone_display']} · roofestimatepro.com</div></div>
  <div class="tool-grid">
    <form class="panel" id="tool-form" data-tool="{t['slug']}" novalidate autocomplete="off">
      {t['form']}
    </form>
    <div class="results" id="results" aria-live="polite"><h2>Your results</h2><p>Loading calculator…</p>
      <noscript><p>This calculator needs JavaScript. You can still <a href="/get-estimate/">request an estimate</a> from our team.</p></noscript></div>
  </div>
</div></section>
<div class="mobile-total no-print" role="button" tabindex="0" aria-label="Jump to results"><div><small>Estimate</small><b>—</b></div><span class="btn btn--peach btn--sm">See results</span></div>
<section class="section tool-content"><div class="wrap">
  <div class="article-layout">
    <article class="prose">{toc(body)}{body}</article>
    <aside class="article-side">{side_cta()}{side_tools(exclude=t['slug'])}</aside>
  </div>
</div></section>
{faq_html(t['faqs'])}
<section class="section related-section"><div class="wrap">
  <div class="section-head"><span class="kicker">Keep going</span><h2>Related calculators</h2></div>
  <div class="related">{related}</div>
</div></section>
{cta_band()}"""
    scripts = (f'<script src="/assets/js/data.js?v={ASSET_V}" defer></script>\n'
               f'<script src="/assets/js/tools-core.js?v={ASSET_V}" defer></script>\n'
               f'<script src="/assets/js/tools/{t["slug"]}.js?v={ASSET_V}" defer></script>\n')
    write(path, render(page, trail, main, active="/tools/", scripts=scripts), priority="0.9")


def build_tools_hub():
    path = "/tools/"
    page = {"path": path, "title": "Free Roof Estimating Tools & Calculators | Roof Estimate Pro",
            "description": "12 free roof estimate calculators: replacement cost, squares, pitch, shingles, metal, flat roofs, insurance claims, depreciation, repairs, gutters, ventilation and bids."}
    trail = [("Home", "/"), ("Tools", None)]
    page["schema"] = [webpage_schema(page, "CollectionPage"),
                      {"@type": "ItemList", "@id": url(path) + "#tools", "itemListElement": [
                          {"@type": "ListItem", "position": i, "url": url(f"/tools/{t['slug']}/"), "name": t["name"]}
                          for i, t in enumerate(TOOLS, 1)]}]
    groups = []
    for t in TOOLS:
        if t["group"] not in groups:
            groups.append(t["group"])
    chips = ('<div class="chips" role="group" aria-label="Filter tools"><button class="chip" type="button" data-filter="all" aria-pressed="true">All tools</button>'
             + "".join(f'<button class="chip" type="button" data-filter="{g}" aria-pressed="false">{g}</button>' for g in groups) + "</div>")
    cards = "".join(tool_card(t) for t in TOOLS)
    hero = page_hero({"h1": "Free roof estimating tools", "kicker": "12 calculators",
                      "lede": "Every calculator a roof estimate needs, from measuring squares to pricing a bid and checking an insurance payout. Built by estimators, loaded with Texas 2026 pricing, and complete enough to use on their own."},
                     trail)
    main = f"""{hero}
<section class="section section--paper"><div class="wrap">
  {chips}
  <div class="grid grid--3">{cards}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="split">
    <div data-reveal>
      <span class="kicker">Built for real estimates</span>
      <h2>Not a one-number guess</h2>
      <p class="lede">Each tool shows its math, line items and assumptions, and every unit price can be edited, so a
      contractor can plug in their own costs and a homeowner can see exactly what drives the number.</p>
      <ul class="check-list">
        <li>Texas regional pricing, plus factors for other U.S. regions</li>
        <li>Itemized results you can print, save as PDF or share by link</li>
        <li>Your inputs are saved in your browser, nothing to sign up for</li>
        <li>One click to send the numbers to a professional estimator</li>
      </ul>
    </div>
    <div data-reveal style="--d:.1s">{sample_sheet()}</div>
  </div>
</div></section>
{cta_band()}"""
    write(path, render(page, trail, main, active="/tools/"), priority="0.9")


def sample_sheet():
    # Mirrors the replacement calculator's default result (2,100 sq ft footprint, 6/12, DFW).
    rows = [("Architectural shingles", "30.3 sq", "$4,238"), ("Underlayment, starter, ridge, vents", "26.6 sq", "$1,593"),
            ("Sales tax on materials", "8.25%", "$481"), ("Install labor", "26.6 sq", "$4,740"),
            ("Tear-off &amp; disposal", "1 layer", "$1,991"), ("Decking (4×8 OSB)", "5 sheets", "$425"),
            ("Overhead &amp; profit", "20%", "$2,694"), ("Permit &amp; inspection", "", "$350")]
    body = "".join(f'<div class="sheet-row"><span>{a}</span><span>{b}</span><span>{c}</span></div>' for a, b, c in rows)
    return f"""<div class="sheet" aria-hidden="true">
  <div class="sheet-head"><b>Replacement estimate</b><span>26.6 sq · 6/12 · DFW</span></div>
  {body}
  <div class="sheet-total"><span>Total</span><span>$16,512</span></div>
  <span class="sheet-stamp">ITEMIZED</span>
</div>"""


def build_post(p):
    path = f"/{p['slug']}/"
    img = f"/assets/img/blog/{p['image']}-1200.webp"
    page = {"path": path, "title": p["title"], "description": p["description"], "og_type": "article",
            "og_image": img, "published": p["published"], "modified": p.get("modified", p["published"]),
            "preload": f'<link rel="preload" as="image" href="{img}">\n'}
    trail = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], None)]
    body = ensure_h2_ids(p["body"])
    words = len(strip_tags(body).split())
    minutes = max(3, round(words / 230))
    page["schema"] = [webpage_schema(page), {
        "@type": "BlogPosting", "@id": url(path) + "#article", "headline": p["h1"], "description": p["description"],
        "image": url(img), "datePublished": p["published"], "dateModified": p.get("modified", p["published"]),
        "author": {"@type": "Organization", "name": f"{BIZ['name']} estimating team", "url": url("/about/")},
        "publisher": {"@id": ORG_ID}, "mainEntityOfPage": url(path), "wordCount": words,
        "articleSection": p["category"]}]
    if p.get("faqs"):
        page["schema"].append(faq_schema(p["faqs"], path))
    meta = (f'<div class="post-meta"><span>{esc(p["category"])}</span><span>Updated {fmt_date(page["modified"])}</span>'
            f'<span>{minutes} min read</span></div>')
    hero = page_hero({"h1": p["h1"], "lede": p.get("lede", p["excerpt"]), "kicker": p["category"]}, trail, meta)
    tools = [TOOL_BY_SLUG[s] for s in p.get("related_tools", []) if s in TOOL_BY_SLUG]
    tool_side = ""
    if tools:
        lis = "".join(f'<li><a href="/tools/{t["slug"]}/">{icon(t["icon"])}{esc(t["short"])}</a></li>' for t in tools)
        tool_side = f'<div class="side-card"><h3>Tools for this topic</h3><ul>{lis}</ul></div>'
    more = [q for q in POSTS if q["slug"] != p["slug"]][:3]
    faqs = faq_html(p["faqs"], heading="Questions we hear about this") if p.get("faqs") else ""
    author = (f'<div class="author-box"><img src="/assets/img/icon-192.webp" alt="" width="56" height="56" loading="lazy">'
              f'<div><b>{BIZ["name"]} estimating team</b><p>Written by the estimators who build roof and claim estimates for '
              f'contractors, adjusters and property owners across Texas. Questions about your own roof? '
              f'<a href="/get-estimate/">Ask an estimator</a>.</p></div></div>')
    main = f"""{hero}
<section class="section"><div class="wrap">
  <div class="article-layout">
    <article class="prose">
      <figure class="feature-img"><img src="{img}" alt="{esc(p['image_alt'])}" width="1200" height="675" fetchpriority="high"></figure>
      {toc(body)}{body}{author}
    </article>
    <aside class="article-side">{tool_side}{side_cta()}</aside>
  </div>
</div></section>
{faqs}
<section class="section"><div class="wrap">
  <div class="section-head"><span class="kicker">Keep reading</span><h2>More from the blog</h2></div>
  <div class="grid grid--3">{''.join(post_card(q) for q in more)}</div>
</div></section>
{cta_band()}"""
    write(path, render(page, trail, main, active="/blog/"), lastmod=page["modified"][:10], priority="0.7")


def build_blog_index():
    path = "/blog/"
    page = {"path": path, "title": "Roof Estimating Blog: Costs, Claims & Takeoffs | Roof Estimate Pro",
            "description": "Guides from working estimators on roof costs, measurements, insurance claims, Xactimate, commercial roofing and Texas storm season."}
    trail = [("Home", "/"), ("Blog", None)]
    page["schema"] = [webpage_schema(page, "CollectionPage"), {
        "@type": "Blog", "@id": url(path) + "#blog", "name": f"{BIZ['name']} Blog", "publisher": {"@id": ORG_ID},
        "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": url(f"/{p['slug']}/"),
                      "datePublished": p["published"]} for p in POSTS]}]
    hero = page_hero({"h1": "The roof estimating blog", "kicker": "Guides & field notes",
                      "lede": "Practical guides on pricing, measuring and documenting roofs, written by people who build estimates every day."}, trail)
    main = f"""{hero}
<section class="section section--paper"><div class="wrap">
  <div class="grid grid--3">{''.join(post_card(p) for p in POSTS)}</div>
</div></section>
{cta_band()}"""
    write(path, render(page, trail, main, active="/blog/"), priority="0.7")


def build_prose(pg):
    """Generic content page. pg keys: path, title, description, h1, lede, kicker,
    body (prose html) or html (full-width sections), faqs, side (bool), trail, schema_type, extra_schema."""
    path = pg["path"]
    trail = pg.get("trail") or [("Home", "/"), (pg.get("crumb", pg["h1"]), None)]
    page = {"path": path, "title": pg["title"], "description": pg["description"], "modified": pg.get("modified", TODAY)}
    page["schema"] = [webpage_schema(page, pg.get("schema_type", "WebPage"))] + pg.get("extra_schema", [])
    if pg.get("faqs"):
        page["schema"].append(faq_schema(pg["faqs"], path))
    hero = page_hero(pg, trail, pg.get("hero_extra", ""))
    if pg.get("html"):
        content = pg["html"]
    else:
        body = ensure_h2_ids(pg["body"])
        if pg.get("side", True):
            content = (f'<section class="section"><div class="wrap"><div class="article-layout"><article class="prose">'
                       f'{body}</article><aside class="article-side">{side_cta()}{side_tools()}</aside></div></div></section>')
        else:
            content = f'<section class="section"><div class="wrap wrap--narrow"><article class="prose">{body}</article></div></section>'
    faqs = faq_html(pg["faqs"]) if pg.get("faqs") else ""
    cta = "" if pg.get("no_cta") else cta_band()
    write(path, render(page, trail, hero + content + faqs + cta, active=pg.get("active")),
          priority=pg.get("priority", "0.6"))


# --------------------------------------------------------------------------
# Forms
# --------------------------------------------------------------------------


def f_input(name, label, type_="text", required=False, full=False, placeholder="", autocomplete=""):
    r = " required" if required else ""
    star = " *" if required else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    cls = " full" if full else ""
    return (f'<div class="f{cls}"><label for="c-{name}">{label}{star}</label>'
            f'<input id="c-{name}" name="{name}" type="{type_}"{r}{ac} placeholder="{esc(placeholder)}"></div>')


def f_select(name, label, options, required=False, full=False):
    r = " required" if required else ""
    opts = '<option value="">Select…</option>' + "".join(f"<option>{esc(o)}</option>" for o in options)
    cls = " full" if full else ""
    return f'<div class="f{cls}"><label for="c-{name}">{label}{" *" if required else ""}</label><select id="c-{name}" name="{name}"{r}>{opts}</select></div>'


def f_text(name, label, required=False, placeholder="", rows=5):
    r = " required" if required else ""
    return (f'<div class="f full"><label for="c-{name}">{label}{" *" if required else ""}</label>'
            f'<textarea id="c-{name}" name="{name}" rows="{rows}"{r} placeholder="{esc(placeholder)}"></textarea></div>')


def f_file(name, label, hint):
    return (f'<div class="f full"><label for="c-{name}">{label}</label><input id="c-{name}" name="{name}[]" type="file" multiple '
            f'accept=".jpg,.jpeg,.png,.webp,.heic,.pdf,.esx,.xlsx,.xls,.csv,.doc,.docx,.zip"><div class="hint">{hint}</div></div>')


def form_shell(form_type, fields, submit, note=""):
    return f"""<form class="form-card" data-form action="/api/contact.php" method="post" enctype="multipart/form-data">
  <input type="hidden" name="form_type" value="{form_type}"><input type="hidden" name="ts" value="">
  <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="form-grid">{fields}</div>
  <button class="btn btn--peach" type="submit" style="margin-top:20px;width:100%">{submit} {icon('arrow')}</button>
  <p class="form-note">{note or 'We reply by email or phone. Your details are used only to prepare your estimate. See our <a href="/privacy-policy/">privacy policy</a>.'}</p>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>"""


def contact_aside(title, text):
    return f"""<div>
  <span class="kicker">Talk to a real estimator</span>
  <h2>{title}</h2>
  <p class="lede">{text}</p>
  <ul class="contact-list">
    <li><span class="ico">{icon('phone')}</span><div><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a><small>Call or text</small></div></li>
    <li><span class="ico">{icon('mail')}</span><div><a href="mailto:{BIZ['email']}">{BIZ['email']}</a><small>Send files of any size</small></div></li>
    <li><span class="ico">{icon('map')}</span><div><b>All of Texas, plus other states</b><small>Remote estimates from photos, measurements and reports</small></div></li>
  </ul>
</div>"""


def build_get_estimate():
    path = "/get-estimate/"
    page = {"path": path, "title": "Request a Roof Estimate | Roof Estimate Pro",
            "description": "Request a professional Xactimate roof estimate for a replacement, repair, insurance claim or commercial roof in Texas or any U.S. state."}
    trail = [("Home", "/"), ("Get an estimate", None)]
    page["schema"] = [webpage_schema(page, "ContactPage")]
    fields = (f_input("name", "Full name", required=True, autocomplete="name")
              + f_input("company", "Company (if any)", autocomplete="organization")
              + f_input("email", "Email", "email", required=True, autocomplete="email")
              + f_input("phone", "Phone", "tel", autocomplete="tel")
              + f_select("role", "I am a…", ["Roofing contractor", "Public adjuster", "Independent / desk adjuster", "Homeowner", "Property manager / owner", "Attorney / appraiser", "Other"], required=True)
              + f_select("estimate_type", "What do you need?", ["Roof replacement estimate", "Roof repair estimate", "Insurance claim / supplement estimate", "Commercial / low-slope estimate", "Scope of damages", "Material takeoff only", "Something else"], required=True)
              + f_input("property_address", "Property address", full=True, autocomplete="street-address", placeholder="Street, city, state")
              + f_text("message", "Project details", required=True, placeholder="Roof type, size, pitch, damage, deadline, carrier… anything that helps.")
              + f_file("files", "Photos, measurement reports or carrier estimate (optional)", "JPG, PNG, PDF, ESX, XLSX or ZIP · up to 20 MB total. Larger files? Email them to " + BIZ["email"] + ".")
              + '<input type="hidden" name="source_tool" value="">')
    handoff = (f'<div class="callout" id="handoff" hidden>{icon("calc")}<p>We have attached your <b></b> results to the message below. '
               f'Add anything else you know about the roof and send it over.</p></div>')
    hero = page_hero({"h1": "Request a professional roof estimate", "kicker": "Get estimate",
                      "lede": "Tell us about the roof. We build line-item, Xactimate estimates for replacements, repairs, insurance claims and commercial roofs anywhere in Texas and across the U.S."}, trail)
    main = f"""{hero}
<section class="section"><div class="wrap"><div class="contact-split">
  {contact_aside("Prefer to talk it through?", "Call, text or email. We work with contractors, public adjusters, desk adjusters and property owners, and we can usually tell you on the first call what the estimate will need.")}
  <div>{handoff}{form_shell("estimate", fields, "Send my request")}</div>
</div></div></section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><span class="kicker">Not ready yet?</span><h2>Run the numbers yourself first</h2></div>
  <div class="grid grid--3">{''.join(tool_card(TOOL_BY_SLUG[s]) for s in ['roof-replacement-cost-calculator', 'roof-insurance-claim-calculator', 'roof-square-footage-calculator'])}</div>
</div></section>"""
    write(path, render(page, trail, main), priority="0.8")


def build_claim():
    path = "/claim/"
    price = BIZ["price_claim_review"]
    page = {"path": path, "title": f"Submit a Claim for Estimate Review (${price}) | Roof Estimate Pro",
            "description": f"Submit claim details and the carrier's estimate for a ${price} roof claim estimate review. We flag missing line items, quantities and code items."}
    trail = [("Home", "/"), ("Services", "/services/"), ("Submit a claim", None)]
    page["schema"] = [webpage_schema(page, "ContactPage")]
    fields = (f_input("name", "Your name", required=True, autocomplete="name")
              + f_input("company", "Company", autocomplete="organization")
              + f_input("email", "Email", "email", required=True, autocomplete="email")
              + f_input("phone", "Phone", "tel", autocomplete="tel")
              + f_input("insured_name", "Insured's name", required=True)
              + f_input("claim_number", "Claim number", required=True)
              + f_input("carrier", "Insurance carrier")
              + f_input("date_of_loss", "Date of loss", "date")
              + f_input("property_address", "Property address", full=True, required=True, placeholder="Street, city, state, ZIP")
              + f_input("desk_adjuster_email", "Desk adjuster's email", "email")
              + f_select("cause_of_loss", "Cause of loss", ["Hail", "Wind", "Hail and wind", "Hurricane / tropical storm", "Tree / impact", "Fire", "Other"])
              + f_text("scope_of_damages", "Scope of damages", required=True, placeholder="What was damaged and what the carrier paid or denied.")
              + f_file("files", "Carrier estimate, photos and reports", "Carrier estimate (PDF or ESX), photos, measurement or engineer reports · up to 20 MB total.")
              + f_input("discount_code", "Discount code (optional)", full=True))
    side = f"""<div>
  <span class="kicker">Claim estimate review</span>
  <h2>We check the carrier's math against the roof</h2>
  <p class="lede">Upload the carrier's estimate and your photos. An estimator compares them line by line and sends back what is missing or under-scoped.</p>
  <p><span class="price-tag"><b>${price}</b> per claim</span></p>
  <ul class="check-list">
    <li>Missing line items: drip edge, starter, ridge, steep and high charges, valley metal, flashing</li>
    <li>Quantity and waste checks against the measurements</li>
    <li>Code-upgrade items commonly left off</li>
    <li>Clear notes you can send to the desk adjuster</li>
  </ul>
  <p class="form-note">Payment is collected by secure Stripe checkout after you submit. Have a discount code? Enter it on the form.</p>
</div>"""
    hero = page_hero({"h1": "Submit your claim details", "kicker": "Fast & secure",
                      "lede": f"Send the claim, the carrier's estimate and your photos. Our ${price} review tells you exactly what the estimate is missing."}, trail)
    main = f"""{hero}
<section class="section"><div class="wrap"><div class="contact-split">
  {side}
  {form_shell("claim", fields, "Send claim for review")}
</div></div></section>
{cta_band("Want the full estimate instead?", "If the carrier's estimate is far off, we can write a complete Xactimate estimate from scratch for the claim.")}"""
    write(path, render(page, trail, main), priority="0.7")


def build_scope():
    path = "/get-a-scope/"
    price = BIZ["price_scope"]
    page = {"path": path, "title": f"Get a Scope of Damages: DIY or Order (${price}) | Roof Estimate Pro",
            "description": f"Document a property claim yourself with a DIY scope on PAscope.com, or order a professional scope of damages from Roof Estimate Pro for ${price}."}
    trail = [("Home", "/"), ("Services", "/services/"), ("Get a scope", None)]
    page["schema"] = [webpage_schema(page, "ContactPage")]
    fields = (f_input("name", "Your name", required=True, autocomplete="name")
              + f_input("email", "Email", "email", required=True, autocomplete="email")
              + f_input("phone", "Phone", "tel", autocomplete="tel")
              + f_input("company", "Company", autocomplete="organization")
              + f_input("property_address", "Property address", full=True, required=True, placeholder="Street, city, state, ZIP")
              + f_select("type_of_damage", "Type of damage", ["Roof", "Roof and exterior", "Interior water damage", "Whole property"], required=True)
              + f_select("cause_of_loss", "Cause of loss", ["Hail", "Wind", "Hail and wind", "Hurricane / tropical storm", "Water / leak", "Fire / smoke", "Other"], required=True)
              + f_text("message", "Anything we should know", placeholder="Date of loss, carrier, measurements you have, access notes…", rows=4)
              + f_file("files", "Photos and measurement reports", "Photos, drone images, EagleView/Hover reports · up to 20 MB total.")
              + f_input("discount_code", "Discount code (optional)", full=True))
    hero = page_hero({"h1": "Get a scope of damages", "kicker": "Get a scope",
                      "lede": "Two ways to document the damage: build a DIY scope yourself on PAscope.com, or order a professional scope from our estimators."}, trail)
    main = f"""{hero}
<section class="section section--paper"><div class="wrap">
  <div class="grid grid--2">
    <div class="card" data-reveal><span class="ico">{icon('clip')}</span><h3>DIY scope on PAscope.com</h3>
      <p>Prefer a hands-on approach? Document and submit the property damage yourself through PAscope.com for a fast, low-cost evaluation.</p>
      <p style="margin-top:18px"><a class="btn btn--ghost" href="https://pascope.com/" rel="noopener" target="_blank">Go to PAscope.com {icon('arrow')}</a></p></div>
    <div class="card" data-reveal style="--d:.08s"><span class="ico">{icon('hardhat')}</span><h3>Order a professional scope · ${price}</h3>
      <p>Give us the property, the type of damage and the cause of loss. We prepare a complete, carrier-ready scope of damages from your photos and measurements.</p>
      <p style="margin-top:18px"><a class="btn" href="#order">Order a scope {icon('arrow')}</a></p></div>
  </div>
</div></section>
<section class="section" id="order"><div class="wrap"><div class="contact-split">
  <div><span class="kicker">Order a scope</span><h2>What you get</h2>
    <ul class="check-list"><li>Room-by-room or slope-by-slope scope of damages</li><li>Quantities tied to measurements and photos</li><li>Cause-of-loss notes and the code items that apply</li><li>Ready to hand to the carrier, an appraiser or your estimator</li></ul>
    <p><span class="price-tag"><b>${price}</b> per property</span></p>
    <p class="form-note">Payment is collected by secure Stripe checkout after you submit.</p></div>
  {form_shell("scope", fields, "Order my scope")}
</div></div></section>"""
    write(path, render(page, trail, main), priority="0.7")


# --------------------------------------------------------------------------
# Site files
# --------------------------------------------------------------------------


def build_data_js():
    regions = [{"key": r["key"], "name": "Texas — " + r["name"], "factor": r["factor"]} for r in TEXAS_REGIONS]
    regions += [{"key": r["key"], "name": r["name"], "factor": r["factor"]} for r in US_REGIONS]
    data = {"materials": MATERIALS, "waste": WASTE, "regions": regions,
            "texasRegions": [r["key"] for r in TEXAS_REGIONS], "updated": TODAY}
    p = os.path.join(OUT, "assets", "js", "data.js")
    with open(p, "w") as f:
        f.write("/* Generated by build.py from siteconfig.py — do not edit. */\nwindow.REP_DATA = "
                + json.dumps(data, separators=(",", ":")) + ";\n")


def build_404():
    page = {"path": "/404.html", "title": "Page not found | Roof Estimate Pro",
            "description": "That page moved or no longer exists.", "robots": "noindex, follow"}
    main = f"""<section class="hero page-hero">{hero_bg()}<div class="wrap">
  <span class="kicker">404</span><h1>That page has moved</h1>
  <p class="lede">The page you were looking for isn't here anymore. Try one of our free calculators or get in touch.</p>
  <div class="btn-row"><a class="btn btn--peach" href="/tools/">Browse the tools</a><a class="btn btn--ghost-light" href="/">Go home</a></div>
</div></section>
<section class="section section--paper"><div class="wrap"><div class="grid grid--3">{''.join(tool_card(t) for t in TOOLS[:6])}</div></div></section>"""
    write("/404.html", render(page, None, main), sitemap=False)


def build_sitemap_page():
    path = "/sitemap/"
    page = {"path": path, "title": "Sitemap | Roof Estimate Pro", "description": "Every page on roofestimatepro.com: tools, services, guides and company pages."}
    trail = [("Home", "/"), ("Sitemap", None)]
    page["schema"] = [webpage_schema(page)]

    def ul(items):
        return "<ul>" + "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in items) + "</ul>"
    body = ("<h2 id='tools'>Free tools</h2>" + ul([("All tools", "/tools/")] + [(t["name"], f"/tools/{t['slug']}/") for t in TOOLS])
            + "<h2 id='services'>Services</h2>" + ul([("All services", "/services/")] + [(s["name"], f"/services/{s['slug']}/") for s in SERVICES]
                                                      + [("Request an estimate", "/get-estimate/"), ("Submit a claim for review", "/claim/"), ("Get a scope", "/get-a-scope/")])
            + "<h2 id='company'>Company</h2>" + ul([("Home", "/"), ("About", "/about/"), ("How it works", "/how-it-works/"), ("Service areas", "/areas/"), ("FAQs", "/faqs/"), ("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/")])
            + "<h2 id='blog'>Blog</h2>" + ul([("All articles", "/blog/")] + [(p["h1"], f"/{p['slug']}/") for p in POSTS]))
    build_prose({"path": path, "title": page["title"], "description": page["description"], "h1": "Sitemap",
                 "body": body, "side": False, "no_cta": True, "priority": "0.3"})


def build_sitemap_xml():
    seen, rows = set(), []
    for path, lastmod, pri in WRITTEN:
        if path in seen:
            continue
        seen.add(path)
        rows.append(f"  <url><loc>{url(path)}</loc><lastmod>{lastmod}</lastmod><priority>{pri}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(xml)


def build_robots():
    if STAGING:
        txt = "# Staging copy — not for indexing\nUser-agent: *\nDisallow: /\n"
    else:
        txt = f"User-agent: *\nDisallow: /api/\nDisallow: /home.html\n\nSitemap: {url('/sitemap.xml')}\n"
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(txt)


# Old WordPress URLs. The 288 thin city pages (/areas/<city>-roof-estimates-services/
# and one at the root) and the category archive all 301 to their replacements.
LEGACY_EXACT = {
    "/home/": "/",
    "/contact/": "/get-estimate/",
    "/contact-us/": "/get-estimate/",
    "/category/roofing/": "/blog/",
    "/feed/": "/blog/",
    "/comments/feed/": "/blog/",
    "/sitemap_index.xml": "/sitemap.xml",
    "/post-sitemap.xml": "/sitemap.xml",
    "/page-sitemap.xml": "/sitemap.xml",
    "/page-sitemap1.xml": "/sitemap.xml",
    "/page-sitemap2.xml": "/sitemap.xml",
    "/category-sitemap.xml": "/sitemap.xml",
    "/tools": "/tools/",
}


def build_index_php():
    exact = ",\n".join(f"    '{k}' => '{v}'" for k, v in LEGACY_EXACT.items())
    php = f"""<?php
// roofestimatepro.com front controller (generated by build.py).
// The host serves existing files directly and sends everything else here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$prod = 'https://roofestimatepro.com';
$base = in_array($host, ['roofestimatepro.com', 'www.roofestimatepro.com'], true) ? $prod : '';

function go($to, $code = 301) {{ header('Location: ' . $to, true, $code); exit; }}

// Canonical scheme and host on the production domain only.
if ($base !== '') {{
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host === 'www.roofestimatepro.com') go($prod . ($_SERVER['REQUEST_URI'] ?? '/'));
}}

if ($path === '/' || $path === '/index.php') {{
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}}

$exact = [
{exact}
];
if (isset($exact[$path])) go($base . $exact[$path]);

// Retired city pages -> the Texas service-area hub.
if (preg_match('#^/areas/[^/]+/?$#', $path) || preg_match('#^/[a-z0-9-]+-roof-estimates-services/?$#', $path)) go($base . '/areas/');
// Category, tag, author and date archives -> blog.
if (preg_match('#^/(category|tag|author)/#', $path) || preg_match('#^/20\\d\\d/#', $path)) go($base . '/blog/');
// Post feeds -> the post itself.
if (preg_match('#^/([a-z0-9-]+)/feed/?$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) go($base . '/' . $m[1] . '/');
// WordPress internals.
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\\.php|xmlrpc\\.php|wp-content/(plugins|themes|litespeed))(/|$)#', $path)) go($base . '/');
// Missing trailing slash on a real page.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) go($base . $path . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""
    with open(os.path.join(OUT, "index.php"), "w") as f:
        f.write(php)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    build_data_js()

    from content import home, pages, services
    home.build(globals())
    build_tools_hub()
    for slug in [t["slug"] for t in TOOLS]:
        if slug in TOOL_PAGES:
            build_tool(TOOL_PAGES[slug])
        else:
            print(f"warning: no content module for tool {slug}")
    services.build(globals())
    for pg in pages.PAGES:
        build_prose(pg)
    build_get_estimate()
    build_claim()
    build_scope()
    for p in POSTS:
        build_post(p)
    build_blog_index()
    build_sitemap_page()
    build_404()
    build_sitemap_xml()
    build_robots()
    build_index_php()
    print(f"built {len(WRITTEN)} pages into {os.path.relpath(OUT, ROOT)}/" + (" (staging)" if STAGING else ""))


if __name__ == "__main__":
    main()
