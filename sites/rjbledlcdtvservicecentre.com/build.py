#!/usr/bin/env python3
"""Static site generator for rjbledlcdtvservicecentre.com.

    python3 build.py              # production build (indexable)
    STAGING=1 python3 build.py    # temporary-domain build: noindex + robots Disallow

Writes every page into public/. Canonical URLs always point at the real domain,
so the staging copy never competes with it in search.
"""

import html
import json
import os
from datetime import date
from pathlib import Path

from content import (AREAS, BIZ, BRAND_ORDER, BRANDS, DISCLAIMER, DISTRICTS, EXTRA_LOCALITIES,
                     HOME_FAQ, MARQUEE, PROCESS, SERVICES, SYMPTOMS, TAG_REDIRECTS)

ROOT = Path(__file__).parent
OUT = ROOT / "public"
ORIGIN = "https://" + BIZ["domain"]
STAGING = os.environ.get("STAGING") == "1"
TODAY = date.today().isoformat()
VER = TODAY.replace("-", "")
SITEMAP = []

esc = html.escape

# ------------------------------------------------------------------ icons (Lucide paths)
ICONS = {
    "tv": '<rect x="2" y="7" width="20" height="15" rx="2"/><path d="m17 2-5 5-5-5"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "volume": '<path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>',
    "wifi": '<path d="M5 13a10 10 0 0 1 14 0M8.5 16.5a5 5 0 0 1 7 0M2 8.8a15 15 0 0 1 20 0"/><circle cx="12" cy="20" r="1"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "up": '<path d="m18 15-6-6-6 6"/>',
    "down": '<path d="m6 9 6 6 6-6"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
}
SERVICE_ICON = {"backlight": "sun", "power": "zap", "board": "cpu", "panel": "monitor", "sound": "volume", "smart": "wifi"}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def img(name, alt, cls="", w=1200, h=800, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{name}.webp" alt="{esc(alt)}" width="{w}" height="{h}" {load}{c}>'


def url(slug):
    return "/" if not slug else f"/{slug}/"


# ------------------------------------------------------------------ navigation
NAV = [
    ("TV Repair", "led-lcd-tv-repairing-in-kolkata"),
    ("Brands", None),
    ("Service Areas", "service-areas"),
    ("LED vs LCD", "led-vs-lcd-tv"),
    ("About", "about"),
]


def header(active):
    items = []
    for label, slug in NAV:
        if slug is None:
            sub = "".join(
                f'<li><a href="{url(BRANDS[k]["slug"])}"{cur(active, BRANDS[k]["slug"])}>{BRANDS[k]["name"]} TV Service Centre</a></li>'
                for k in BRAND_ORDER)
            items.append(
                f'<li class="has-sub"><a href="{url(BRANDS["samsung"]["slug"])}">Brands</a>'
                f'<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-brands" aria-label="Show brands">{icon("down")}</button>'
                f'<ul class="sub" id="sub-brands">{sub}</ul></li>')
        else:
            items.append(f'<li><a href="{url(slug)}"{cur(active, slug)}>{label}</a></li>')
    items.append(f'<li class="nav-cta"><a href="/contact/"{cur(active, "contact")}>Book a Repair</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="nav wrap" aria-label="Main">
    <a class="brand" href="/" aria-label="{BIZ['name']} home">
      <span class="brand-mark"><b>RJB</b></span>
      <span>RJB TV Service<small>LED · LCD · Smart TV · Kolkata</small></span>
    </a>
    <div class="nav-panel" id="nav-panel">
      <ul class="nav-links">{''.join(items)}</ul>
    </div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu"><span></span><span></span><span></span></button>
  </nav>
</header>'''


def cur(active, slug):
    return ' aria-current="page"' if active == slug else ""


def footer():
    brands = "".join(f'<li><a href="{url(BRANDS[k]["slug"])}">{BRANDS[k]["name"]} TV Service</a></li>' for k in BRAND_ORDER)
    areas = "".join(f'<li><a href="{url(a["slug"])}">{a["place"]}</a></li>' for a in AREAS[:7])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="brand" href="/"><span class="brand-mark"><b>RJB</b></span><span>RJB TV Service<small>LED · LCD · Smart TV · Kolkata</small></span></a>
        <p style="margin-top:18px">Independent LED, LCD and Smart TV repair for Kolkata, Howrah, Hooghly and the 24 Parganas. Board-level diagnosis, honest quotes.</p>
        <p><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
      </div>
      <div><h2>Repairs</h2><ul>
        <li><a href="/led-lcd-tv-repairing-in-kolkata/">LED LCD TV Repairing</a></li>{brands}
        <li><a href="/led-vs-lcd-tv/">LED vs LCD TV Guide</a></li></ul></div>
      <div><h2>Areas</h2><ul>{areas}<li><a href="/service-areas/">All service areas</a></li></ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
    </div>
    <div class="foot-bottom">
      <span>&copy; {date.today().year} {BIZ['name']}, Kolkata.</span>
      <span>LED LCD TV Service Centre Kolkata</span>
    </div>
    <p class="disclaimer">{DISCLAIMER}</p>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{icon("up")}</button>'''


# ------------------------------------------------------------------ schema
BUSINESS_ID = ORIGIN + "/#business"


def business_schema():
    return {
        "@type": "LocalBusiness", "@id": BUSINESS_ID, "name": BIZ["name"], "url": ORIGIN + "/",
        "email": BIZ["email"], "image": ORIGIN + "/assets/img/soldering-board.webp",
        "logo": ORIGIN + "/favicon.svg",
        "description": "Independent LED, LCD and Smart TV repair service in Kolkata for Samsung, Sony, LG, Videocon and other brands.",
        "address": {"@type": "PostalAddress", "addressLocality": BIZ["city"], "addressRegion": BIZ["region"], "addressCountry": BIZ["country"]},
        "areaServed": [{"@type": "City", "name": "Kolkata"}, {"@type": "City", "name": "Howrah"}]
                      + [{"@type": "Place", "name": a["place"]} for a in AREAS],
        "knowsAbout": ["LED TV repair", "LCD TV repair", "Smart TV repair", "TV backlight repair", "TV power supply repair"],
    }


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(trail)]}


def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}


def service_schema(name, desc, path, area=None):
    s = {"@type": "Service", "name": name, "description": desc, "url": ORIGIN + path,
         "provider": {"@id": BUSINESS_ID}, "serviceType": "Television repair"}
    s["areaServed"] = {"@type": "Place", "name": area or "Kolkata"}
    return s


def strip(s):
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ------------------------------------------------------------------ layout
def page(path, title, desc, body, active=None, schema=(), og_img="hero-tv-glow", priority="0.7"):
    canonical = ORIGIN + path
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": BIZ["name"], "publisher": {"@id": BUSINESS_ID}},
        business_schema(),
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc,
         "isPartOf": {"@id": ORIGIN + "/#website"}, "inLanguage": "en-IN"},
        *schema]}
    robots = '<meta name="robots" content="noindex, nofollow">' if STAGING else '<meta name="robots" content="index, follow, max-image-preview:large">'
    doc = f'''<!doctype html>
<html lang="en-IN" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_img}.webp">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#06070c">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={VER}" defer></script>
</body>
</html>
'''
    write(path, doc)
    if path != "/404.html":
        SITEMAP.append((path, priority))


def write(path, doc):
    if path == "/":
        f = OUT / "home.html"
    elif path.endswith(".html"):
        f = OUT / path.lstrip("/")
    else:
        f = OUT / path.strip("/") / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding="utf-8")


def page_hero(h1, lead, trail, image, alt, eyebrow):
    crumbs = "".join(
        f'<li><a href="{u}">{n}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (n, u) in enumerate(trail))
    return f'''<section class="page-hero scanlines">
  {img(image, alt, w=1600, h=900, eager=True)}
  <div class="wrap">
    <ol class="crumbs">{crumbs}</ol>
    <p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>{eyebrow}</p>
    <h1 class="power-on">{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-actions" style="margin:28px 0 0">
      <a class="btn btn-glow" href="/contact/">Book a repair {icon("arrow")}</a>
      <a class="btn btn-ghost" href="mailto:{BIZ['email']}">{icon("mail")} Email us</a>
    </div>
  </div>
</section>'''


def faq_block(faq, title="Frequently asked questions"):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq)
    return f'<h2>{title}</h2><div class="faq" style="margin-top:22px">{items}</div>'


def cta(title="Got a TV that won't behave?", text=None):
    text = text or ("Send us the brand, model number and what it is doing. We will tell you what is likely wrong "
                    "and what it takes to fix it, before any work starts.")
    return f'''<section class="section"><div class="wrap"><div class="cta reveal">
  <p class="eyebrow" style="justify-content:center"><span class="subpx"><i></i><i></i><i></i></span>Advice by email</p>
  <h2>{title}</h2><p>{text}</p>
  <div class="hero-actions"><a class="btn btn-glow" href="/contact/">Book a repair {icon("arrow")}</a>
  <a class="btn btn-ghost" href="mailto:{BIZ['email']}">{icon("mail")} {BIZ['email']}</a></div>
</div></div></section>'''


def sidebar(current=None):
    brands = "".join(
        f'<li><a href="{url(BRANDS[k]["slug"])}"{cur(current, BRANDS[k]["slug"])}>{BRANDS[k]["name"]} TV service <span>&rarr;</span></a></li>'
        for k in BRAND_ORDER)
    return f'''<aside class="sidebar">
  <div class="side-card side-cta">
    <h2>Book a TV repair</h2>
    <p>Tell us the brand, model and fault. We reply with likely causes and next steps.</p>
    <a class="btn btn-glow" href="/contact/">Request a repair {icon("arrow")}</a>
    <p style="margin:14px 0 0;font-size:.9rem"><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
  </div>
  <div class="side-card"><h2>Repairs by brand</h2><ul>
    <li><a href="/led-lcd-tv-repairing-in-kolkata/"{cur(current, "led-lcd-tv-repairing-in-kolkata")}>All brands: LED LCD TV repairing <span>&rarr;</span></a></li>{brands}</ul></div>
  <div class="side-card"><h2>Guides</h2><ul>
    <li><a href="/led-vs-lcd-tv/"{cur(current, "led-vs-lcd-tv")}>LED vs LCD TV: which is better? <span>&rarr;</span></a></li>
    <li><a href="/service-areas/">Service areas <span>&rarr;</span></a></li></ul></div>
</aside>'''


def services_grid(link_all=True):
    cards = []
    for i, (key, title, text) in enumerate(SERVICES):
        cards.append(f'''<a class="card card-link reveal" style="--d:{i * 0.06:.2f}s" href="/led-lcd-tv-repairing-in-kolkata/#{key}">
  <div class="icon">{icon(SERVICE_ICON[key])}</div><h3>{title}</h3><p>{text}</p>
  <span class="more">Learn more {icon("arrow")}</span></a>''')
    return f'<div class="grid g3">{"".join(cards)}</div>'


def checker():
    tabs, panels = [], []
    fx = {"nopicture": "fx-nopicture", "lines": "fx-lines", "nopower": "fx-nopower", "dim": "fx-dim",
          "flicker": "fx-flicker", "sound": "fx-sound", "smart": "fx-smart"}
    for i, (key, label, what, parts, verdict) in enumerate(SYMPTOMS):
        sel = "true" if i == 0 else "false"
        tabs.append(f'<button role="tab" id="tab-{key}" aria-selected="{sel}" aria-controls="panel-{key}" tabindex="{0 if i == 0 else -1}"><i></i>{label}</button>')
        panels.append(f'''<div class="checker-panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}"{'' if i == 0 else ' hidden'}>
  <div class="mini-tv" aria-hidden="true"><div class="fx {fx[key]}"></div></div>
  <p class="eyebrow">Symptom {i + 1} of {len(SYMPTOMS)}</p><h3>{label}</h3>
  <p>{what}</p>
  <dl><div><dt>Likely culprits</dt><dd>{parts}</dd></div><div><dt>Our verdict</dt><dd>{verdict}</dd></div></dl>
  <a class="btn btn-ghost" href="/contact/">Get this diagnosed {icon("arrow")}</a>
</div>''')
    return f'''<div class="checker reveal" data-tabs>
  <div class="checker-tabs" role="tablist" aria-label="TV symptoms" aria-orientation="vertical">{''.join(tabs)}</div>
  <div>{''.join(panels)}</div>
</div>'''


def timeline():
    steps = "".join(f'<div class="step"><div class="num">{i + 1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS))
    return f'<div class="timeline">{steps}</div>'


COMPARE = {
    "ccfl": {"title": "LCD with CCFL backlight", "label": "Fluorescent tubes",
             "text": "The original LCD TVs lit the panel with fluorescent tubes (CCFL) behind it. Thicker, warmer and more power-hungry, with a greyer black level. Still common in older Samsung, Sony, LG and Videocon sets.",
             "scores": [45, 40, 35, 70]},
    "edge": {"title": "Edge-lit LED", "label": "LEDs along the edges",
             "text": "LEDs along the edges of the panel shine into a light-guide plate. This made very thin TVs possible. Uniformity can suffer, with brighter edges or 'clouding' on dark scenes.",
             "scores": [70, 60, 80, 65]},
    "full": {"title": "Direct / full-array LED", "label": "LED grid behind panel",
             "text": "A grid of LEDs sits directly behind the panel. Most budget and mid-range TVs use this, and premium models dim zones locally for deeper blacks. It is also where most backlight repairs happen.",
             "scores": [85, 85, 70, 80]},
}


def compare():
    data = esc(json.dumps(COMPARE))
    btns = "".join(f'<button type="button" data-mode="{k}" aria-pressed="false">{v["title"].split(" with")[0] if k == "ccfl" else v["title"]}</button>' for k, v in COMPARE.items())
    meters = "".join(f'<span>{m}</span><div class="bar"><i></i></div>' for m in ["Brightness", "Contrast", "Slimness", "Power efficiency"])
    return f'''<div class="compare reveal" data-compare="{data}">
  <div class="seg" role="group" aria-label="Backlight type">{btns}</div>
  <div class="compare-body">
    <div class="panel-diagram" data-mode="ccfl" aria-hidden="true"><div class="lamps"></div><div class="lcd"></div><span class="label"></span></div>
    <div class="compare-copy" aria-live="polite"><h3 data-c="title"></h3><p data-c="text"></p><div class="meter">{meters}</div></div>
  </div>
</div>'''


def area_groups():
    groups = []
    for key, name in DISTRICTS.items():
        links = [f'<li><a href="{url(a["slug"])}">{a["place"]}</a></li>' for a in AREAS if a["district"] == key]
        extra = [f'<li><span>{p}</span></li>' for p in EXTRA_LOCALITIES.get(key, [])]
        if not links and not extra:
            continue
        groups.append(f'<div class="area-group reveal"><h3>{name}</h3><ul class="chips">{"".join(links + extra)}</ul></div>')
    return f'<div class="area-groups">{"".join(groups)}</div>'


def brand_cards():
    out = []
    for i, k in enumerate(BRAND_ORDER):
        b = BRANDS[k]
        out.append(f'''<a class="card brand-card card-link reveal" style="--d:{i * 0.08:.2f}s" href="{url(b["slug"])}">
  <div class="ph">{img(b["img"], b["img_alt"], w=1200, h=800)}<b>{b["name"]}</b></div>
  <div class="body"><p>{b["card"]}</p><span class="more">{b["name"]} TV service centre {icon("arrow")}</span></div></a>''')
    return f'<div class="grid g4">{"".join(out)}</div>'


# ------------------------------------------------------------------ pages
def build_home():
    marquee = "".join(f"<span>{m}</span>" for m in MARQUEE) * 2
    n_local = len(AREAS) + sum(len(v) for v in EXTRA_LOCALITIES.values())
    body = f'''<section class="hero scanlines">
  <div class="hero-bg">{img("tv-glow-room", "", w=1200, h=800, eager=True)}</div>
  <span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span>
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>Kolkata · Howrah · Hooghly · 24 Parganas</p>
      <h1><span class="power-on">LED LCD TV Service Centre in <span class="grad-text">Kolkata</span></span></h1>
      <p class="lead">Dark screen, lines across the picture, a TV that won't switch on? We repair Samsung, Sony, LG, Videocon and every other major brand at board level, and tell you honestly whether it's worth fixing.</p>
      <div class="hero-actions">
        <a class="btn btn-glow" href="/contact/">Book a repair {icon("arrow")}</a>
        <a class="btn btn-ghost" href="#checker">Diagnose my TV</a>
      </div>
      <ul class="hero-badges"><li>LED &amp; LCD</li><li>Smart &amp; 4K TVs</li><li>Quote before work</li></ul>
    </div>
    <div class="tv" data-channels title="Click to change channel">
      <div class="float-chip chip-b"><span class="dot">{icon("shield")}</span><span><strong>Board-level</strong>repairs, not part-swapping</span></div>
      <div class="tv-frame">
        <div class="tv-screen">
          {img("living-room-led-tv", "Flat screen LED TV in a living room", w=1200, h=800, eager=True)}
          {img("soldering-board", "Technician soldering a TV circuit board", w=1200, h=800)}
          {img("family-watching-tv", "Family watching a repaired TV at home", w=1200, h=800)}
          {img("circuit-macro", "Close-up of a TV mainboard", w=1200, h=800)}
          <canvas aria-hidden="true"></canvas>
          <div class="bars" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
          <span class="tv-osd" aria-hidden="true">CH 01</span>
        </div>
        <span class="tv-led" aria-hidden="true"></span>
      </div>
      <div class="tv-stand"></div>
      <div class="float-chip chip-a"><span class="dot">{icon("sun")}</span><span><strong>Backlight fixed</strong>our most common repair</span></div>
    </div>
  </div>
</section>
<div class="marquee" aria-label="TV brands we repair"><div class="marquee-track">{marquee}</div></div>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>What we fix</p>
      <h2>LED &amp; LCD TV repairs, done properly</h2>
      <p class="lead">Every TV comes apart on the bench, gets measured and is repaired at the component that failed. That is cheaper for you and it lasts longer.</p></div>
    {services_grid()}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div class="media-stack reveal">
      <div class="media">{img("repair-bench", "TV repair workbench with soldering station and test gear", w=1200, h=800)}<span class="media-tag">On the bench</span></div>
      <div class="media small">{img("soldering-closeup", "Close-up of soldering a component on a TV board", w=1200, h=800)}</div>
    </div>
    <div class="reveal" style="--d:.1s">
      <p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>Why RJB</p>
      <h2>Component-level repair, not guesswork</h2>
      <p class="lead">A lot of TV "repairs" are just board swaps. When the board is no longer made, or costs half a new TV, that's a dead end. We go one level deeper.</p>
      <ul class="ticks">
        <li><strong>Diagnosis first.</strong> We find the failed part before we talk about price.</li>
        <li><strong>Clear quote before work.</strong> You decide; nothing is replaced without your go-ahead.</li>
        <li><strong>Honest about panels.</strong> If a cracked screen makes repair pointless, we say so.</li>
        <li><strong>Burn-in tested.</strong> Repaired sets run for hours before they leave the bench.</li>
      </ul>
      <a class="btn btn-ghost" href="/about/">About our workshop {icon("arrow")}</a>
    </div>
  </div>
</section>

<section class="section" id="checker">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>TV symptom checker</p>
      <h2>What is your TV doing?</h2>
      <p class="lead">Pick the symptom closest to yours to see the usual causes and whether it is worth repairing.</p></div>
    {checker()}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><b class="grad-text" data-count="{len(MARQUEE)}" data-suffix="+">0</b><span>TV brands repaired</span></div>
      <div class="stat"><b class="grad-text" data-count="{n_local}" data-suffix="+">0</b><span>localities covered</span></div>
      <div class="stat"><b class="grad-text" data-count="{len(SYMPTOMS)}">0</b><span>common faults explained</span></div>
      <div class="stat"><b class="grad-text" data-count="3">0</b><span>panel types: LCD, LED, OLED</span></div>
    </div>
  </div>
</section>

<section class="section" id="brands">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>Brand specialists</p>
      <h2>Samsung, Sony, LG &amp; Videocon TV service</h2>
      <p class="lead">Each brand has its own weak spots. We know them, which means faster diagnosis and fewer surprises.</p></div>
    {brand_cards()}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center reveal"><p class="eyebrow" style="justify-content:center"><span class="subpx"><i></i><i></i><i></i></span>How it works</p>
      <h2>From blank screen to back on, in four steps</h2></div>
    {timeline()}
  </div>
</section>

<section class="band">
  {img("howrah-bridge", "Howrah Bridge over the Hooghly river at dusk, Kolkata", w=1600, h=1000)}
  <div class="wrap reveal">
    <p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>Across both banks of the Hooghly</p>
    <h2>Kolkata, Howrah, Hooghly &amp; the 24 Parganas</h2>
    <p>From Salt Lake and Santoshpur to Bally, Uttarpara, Chandannagar, Barrackpore and Budge Budge, our TV repair service covers the whole of greater Kolkata.</p>
    <a class="btn btn-glow" href="/service-areas/">See all service areas {icon("arrow")}</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>Where we work</p>
      <h2>Local TV repair, area by area</h2></div>
    {area_groups()}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>LED or LCD?</p>
      <h2>See how your TV makes light</h2>
      <p class="lead">Every LED TV is really an LCD TV. The difference is the light behind the panel, and that decides how it fails. Tap through the three types.</p></div>
    {compare()}
    <p style="margin-top:24px"><a href="/led-vs-lcd-tv/">Read the full LED vs LCD TV guide &rarr;</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">{faq_block(HOME_FAQ)}</div>
</section>
{cta()}'''
    page("/", "LED LCD TV Service Centre Kolkata | RJB TV Repair",
         "LED LCD TV service centre in Kolkata for Samsung, Sony, LG and Videocon. Board-level repair of backlight, "
         "power supply, mainboard and Smart TV faults across Kolkata, Howrah and Hooghly.",
         body, active="", schema=[faq_schema(HOME_FAQ)], priority="1.0")


def build_repairing():
    slug = "led-lcd-tv-repairing-in-kolkata"
    path = url(slug)
    sections = []
    details = {
        "backlight": ("A TV that plays sound with a black or very dim screen has almost always lost its backlight. In LED TVs the LEDs are wired in series, so when one fails the whole string goes dark. We replace the complete strip set with matched strips, check the driver circuit on the power board, and re-seat the diffuser sheets so there are no shadows or hot spots afterwards.",
                      "led tv repair"),
        "power": ("No standby light, a TV that clicks but never starts, or one that died after a power cut usually has a power supply fault. We test the board under load, find the failed capacitor, MOSFET, PWM controller or fuse, and repair it rather than selling you a new board that might not be available for your model.",
                  "tv power supply repair"),
        "board": ("The mainboard runs the software and processes the picture; the T-con board drives the panel. Boot loops, frozen menus, wrong colours, ghosting, half-screen and some line faults start here. We diagnose with the right test equipment and repair at component level, including eMMC and firmware work.",
                  "mainboard repair"),
        "panel": ("Lines, bands and half-screen faults can come from the panel itself or from the boards and cables that feed it. We test every link in that chain before we call it a panel fault. If the panel really is damaged, we tell you straight, because a replacement panel can cost close to a new TV.",
                  "lcd tv repair"),
        "sound": ("No audio, distorted speakers, HDMI ports that don't detect your set-top box, broken USB ports and ARC links that won't talk to the soundbar are all repairable on the mainboard.",
                  "tv sound repair"),
        "smart": ("Smart TVs are computers, and they fail like computers: corrupted updates, worn storage, Wi-Fi modules that drop out. We reload firmware, repair or replace eMMC storage and set up Tizen, webOS, Android TV and Google TV properly.",
                  "smart tv repair"),
    }
    for key, title, short in SERVICES:
        text, _ = details[key]
        sections.append(f'<h3 id="{key}">{title}</h3><p>{text}</p>')
    faq = [
        ("How much does LED TV repair cost in Kolkata?",
         "It depends on the fault and the model. Software and port repairs are at the low end, backlight and power supply repairs in the middle, and panel replacement at the top. We give you a clear quote after diagnosis and nothing is done without your approval."),
        ("How long does an LCD or LED TV repair take?",
         "Many repairs are completed within a few days once diagnosed. Jobs that need a specific part ordered take longer, and we tell you the timeline up front."),
        ("How do I fix an LED TV with sound but no picture myself?",
         "First check the obvious: a different input, the picture settings, and whether a torch held close to the screen shows a faint image. If it does, the backlight has failed. That repair means opening the TV and handling the panel, which is easy to crack, so it is best left to a workshop."),
        ("Do you repair older LCD TVs?",
         "Yes. Older LCD TVs use fluorescent CCFL backlights and inverter boards. We still repair them, alongside modern LED, QLED and OLED sets."),
    ]
    body = page_hero("LED LCD TV Repairing in Kolkata",
                     "Multi-brand LED and LCD TV repair with board-level diagnosis: backlight, power supply, mainboard, T-con, panel, sound and Smart TV software.",
                     [("Home", "/"), ("LED LCD TV Repairing in Kolkata", path)], "soldering-board",
                     "Technician repairing an LED TV circuit board with a soldering iron", "All brands · All faults")
    body += f'''<section class="section"><div class="wrap layout"><article class="prose">
<h2>LED TV repair and LCD TV repair under one roof</h2>
<p>Whether you have a five-year-old Full HD LED TV, a brand-new 4K Smart TV or an older LCD set that has been in the family for years, the repair process is the same: find the failed component, fix it properly, and test the TV long enough to be sure the fault is gone.</p>
<p>We repair Samsung, Sony, LG, Videocon, Panasonic, Philips, Onida, TCL, Mi, OnePlus, Haier, Vu and most other brands sold in India. If your TV is still under the manufacturer's warranty, contact the manufacturer first; once it isn't, independent repair is usually the faster and cheaper route.</p>
<figure>{img("technicians-board", "Two technicians diagnosing a TV mainboard on the workbench", w=1200, h=800)}<figcaption>Every TV is diagnosed on the bench before we quote.</figcaption></figure>
<h2>The repairs we do every day</h2>
{''.join(sections)}
<div class="callout"><p><strong>Is it worth repairing?</strong> For backlight, power, board, port and software faults, almost always. For a physically cracked panel, rarely. We tell you which before you spend anything.</p></div>
<h2>Common LED TV faults at a glance</h2>
<table><thead><tr><th>Symptom</th><th>Usual cause</th><th>Repairable?</th></tr></thead><tbody>
{''.join(f"<tr><td>{s[1]}</td><td>{s[3]}</td><td>{s[4]}</td></tr>" for s in SYMPTOMS)}
</tbody></table>
<h2>How a repair works</h2>
<ol>{''.join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in PROCESS)}</ol>
{faq_block(faq)}
</article>{sidebar(slug)}</div></section>{cta()}'''
    page(path, "LED LCD TV Repairing in Kolkata | LED & LCD TV Repair Service",
         "LED and LCD TV repairing in Kolkata: backlight, power supply, mainboard, T-con, lines on screen, sound and "
         "Smart TV faults for all brands. Board-level diagnosis and a clear quote before work.",
         body, active=slug, og_img="soldering-board",
         schema=[service_schema("LED LCD TV Repairing", "Multi-brand LED and LCD TV repair in Kolkata.", path),
                 crumbs_schema([("Home", "/"), ("LED LCD TV Repairing in Kolkata", path)]), faq_schema(faq)], priority="0.9")


def build_brand(key):
    b = BRANDS[key]
    path = url(b["slug"])
    faults = "".join(f'<div class="fault"><h3>{t}</h3><p>{d}</p></div>' for t, d in b["faults"])
    others = [BRANDS[k] for k in BRAND_ORDER if k != key]
    areas = [a for a in AREAS if a["brand"] == key]
    area_html = ""
    if areas:
        area_html = (f'<h2>{b["name"]} TV service near you</h2><p>We also have local pages for {b["name"]} TV owners in:</p>'
                     f'<ul class="chips">{"".join(f"<li><a href={chr(34)}{url(a["slug"])}{chr(34)}>{a["place"]}</a></li>" for a in areas)}</ul>')
    extra = ""
    if key == "videocon":
        extra = f'''<h2>Which is better: LED or LCD TV?</h2>
<p>It is one of the questions we are asked most, especially by Videocon owners deciding whether to repair or replace. The short answer: an LED TV <em>is</em> an LCD TV. Both use a liquid-crystal panel to make the picture. The difference is the light behind it. Older LCD TVs use fluorescent tubes (CCFL); LED TVs use light-emitting diodes.</p>
<p>LED backlighting is brighter, slimmer and uses noticeably less electricity, so an LED TV is the better choice if you are buying new. But if your LCD TV's panel is healthy, repairing its backlight or power supply is usually far cheaper than replacing the set. <a href="/led-vs-lcd-tv/">Read the full LED vs LCD comparison</a>.</p>
{compare()}'''
    body = page_hero(b["h1"], b["desc"].split(": ", 1)[-1].split(". ")[0] + ".",
                     [("Home", "/"), (f'{b["name"]} TV Service Centre', path)], b["img"], b["img_alt"],
                     f'{b["name"]} TV repair · Kolkata')
    body += f'''<section class="section"><div class="wrap layout"><article class="prose">
<h2>{b["name"]} TV repair in Kolkata</h2>
{''.join(f"<p>{p}</p>" for p in b["intro"])}
<h2>Common {b["name"]} TV faults we repair</h2>
<div class="fault-grid">{faults}</div>
<figure>{img("repair-shop" if key in ("samsung", "videocon") else "workbench-multimeter", f'{b["name"]} TV board being tested in an electronics repair workshop', w=1200, h=800)}<figcaption>Boards are tested and repaired at component level.</figcaption></figure>
<h2>{b["name"]} models we work on</h2>
<p>{b["series"]} If you're not sure what you have, the model number is on the sticker on the back of the TV. Send us that and a short description of the fault.</p>
<h2>How a {b["name"]} TV repair works</h2>
<ol>{''.join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in PROCESS)}</ol>
{extra}
{area_html}
<div class="callout"><p><strong>Independent service.</strong> We are not an authorised {b["name"]} service centre. For a TV that is still under {b["name"]}'s warranty, contact the manufacturer first. For out-of-warranty repairs, we're here.</p></div>
{faq_block(b["faq"])}
<h2>Other brands we repair</h2>
<p>{", ".join(f'<a href="{url(o["slug"])}">{o["name"]} LED LCD TV service centre</a>' for o in others)}, plus <a href="/led-lcd-tv-repairing-in-kolkata/">all other major brands</a>.</p>
</article>{sidebar(b["slug"])}</div></section>{cta(f'Is your {b["name"]} TV playing up?')}'''
    page(path, b["title"], b["desc"], body, active=b["slug"], og_img=b["img"],
         schema=[service_schema(f'{b["name"]} LED LCD TV Repair', b["desc"], path),
                 crumbs_schema([("Home", "/"), (f'{b["name"]} TV Service Centre', path)]), faq_schema(b["faq"])], priority="0.9")


DISTRICT_IMG = {"kolkata": ("victoria-memorial", "Victoria Memorial reflected in water at sunset, Kolkata"),
                "howrah": ("howrah-bridge-river", "Howrah Bridge over the Hooghly river"),
                "hooghly": ("howrah-bridge", "The Hooghly river at dusk"),
                "n24": ("kolkata-tram", "Kolkata tram depot, a familiar sight of greater Kolkata"),
                "s24": ("howrah-bridge-river", "The Hooghly river south of Kolkata"),
                "greater": ("kolkata-tram", "Kolkata tram depot")}
AREA_PHOTOS = ["living-room-wall-tv", "modern-living-tv", "living-room-led-tv", "minimal-tv-room", "tv-remote", "family-watching-tv"]


def build_area(i, a):
    path = url(a["slug"])
    b = BRANDS.get(a["brand"]) if a["brand"] else None
    brand = b["name"] if b else ""
    h1 = f'{brand + " " if brand else ""}{a["kind"]} in {a["place"]}'
    title = f'{h1} | {"Kolkata" if a["district"] in ("kolkata", "greater") else DISTRICTS[a["district"]]} TV Repair'
    if len(title) > 68:
        title = f"{h1} | RJB TV Repair"
    what = f'{brand} LED TV repair' if brand else "LCD and LED TV repair for all brands"
    desc = (f'{what} in {a["place"]}, {DISTRICTS[a["district"]]}: no picture, no power, lines on screen, backlight, '
            f'power supply and Smart TV faults. Board-level diagnosis and a clear quote.')
    if b:
        faults = b["faults"][i % 3: i % 3 + 4]
    else:
        faults = [(s[1], s[2]) for s in SYMPTOMS[i % 3: i % 3 + 4]]
    fault_html = "".join(f'<div class="fault"><h3>{t}</h3><p>{d}</p></div>' for t, d in faults)
    nearby = ""
    if a["nearby"]:
        nearby = (f'<h2>Also serving near {a["place"]}</h2><p>Our service around {a["place"]} also covers '
                  f'{", ".join(a["nearby"][:-1])} and {a["nearby"][-1]}.</p>')
    siblings = [x for x in AREAS if x["district"] == a["district"] and x is not a]
    sib_html = ""
    if siblings:
        sib_html = (f'<h2>More service areas in {DISTRICTS[a["district"]]}</h2><ul class="chips">'
                    + "".join(f'<li><a href="{url(x["slug"])}">{x["place"]}</a></li>' for x in siblings) + "</ul>")
    faq = [
        (f"Do you repair {brand + ' ' if brand else ''}TVs in {a['place']}?",
         f"Yes. {a['place']} is part of our regular service area. Email us the TV's brand, model number and fault and we will reply with the likely cause and next steps."),
        (f"What are the most common TV faults you see from {a['place']}?",
         f"Backlight failures (sound but no picture), power supply faults (TV won't turn on) and lines on the screen. All three are usually repairable."),
        ("Do you give a quote before repairing?",
         "Always. We diagnose first and quote second. Nothing is replaced without your approval."),
    ]
    photo = AREA_PHOTOS[i % len(AREA_PHOTOS)]
    dimg, dalt = DISTRICT_IMG[a["district"]]
    brand_link = (f'<p>For the full rundown on {brand} faults and models, see our <a href="{url(b["slug"])}">{brand} LED LCD TV service centre</a> page.</p>'
                  if b else '<p>See also our <a href="/led-lcd-tv-repairing-in-kolkata/">LED LCD TV repairing</a> page for every repair we offer.</p>')
    body = page_hero(h1, desc.split(": ")[0] + " for homes across " + a["place"] + " and nearby. Board-level diagnosis, honest advice and a clear quote before any work.",
                     [("Home", "/"), ("Service Areas", "/service-areas/"), (a["place"], path)], dimg, dalt,
                     f'{DISTRICTS[a["district"]]} · {"Multi-brand" if not b else brand}')
    body += f'''<section class="section"><div class="wrap layout"><article class="prose">
<h2>{what} in {a["place"]}</h2>
<p>{a["intro"]}</p>
<p>{a["local"]}</p>
<figure>{img(photo, f'{brand + " " if brand else ""}LED TV in a home in {a["place"]}', w=1200, h=800)}<figcaption>{brand + " " if brand else ""}LED &amp; LCD TV repair for homes in {a["place"]}.</figcaption></figure>
<h2>{brand + " " if brand else ""}TV problems we fix in {a["place"]}</h2>
<div class="fault-grid">{fault_html}</div>
{brand_link}
<h2>How it works</h2>
<ol>{''.join(f"<li><strong>{t}.</strong> {d}</li>" for t, d in PROCESS)}</ol>
{nearby}
{sib_html}
{faq_block(faq)}
</article>{sidebar()}</div></section>{cta(f'TV trouble in {a["place"]}?')}'''
    page(path, title, desc, body, active="service-areas", og_img=photo,
         schema=[service_schema(h1, desc, path, a["place"]),
                 crumbs_schema([("Home", "/"), ("Service Areas", "/service-areas/"), (a["place"], path)]), faq_schema(faq)])


def build_areas_hub():
    path = "/service-areas/"
    cards = "".join(
        f'''<a class="card card-link reveal" style="--d:{(i % 3) * .06:.2f}s" href="{url(a["slug"])}"><div class="icon">{icon("pin")}</div>
<h3>{a["place"]}</h3><p>{(BRANDS[a["brand"]]["name"] + " ") if a["brand"] else ""}{a["kind"]} &middot; {DISTRICTS[a["district"]]}</p>
<span class="more">View area {icon("arrow")}</span></a>''' for i, a in enumerate(AREAS))
    body = page_hero("TV Repair Service Areas in Kolkata &amp; Nearby",
                     "LED, LCD and Smart TV repair across Kolkata, Howrah, Hooghly, North 24 Parganas and South 24 Parganas.",
                     [("Home", "/"), ("Service Areas", path)], "howrah-bridge", "Howrah Bridge at dusk", "Where we work")
    body += f'''<section class="section"><div class="wrap">
<div class="section-head reveal"><h2>Areas by district</h2><p class="lead">Linked areas have their own page with local details. If your locality isn't listed, ask anyway: we cover most of greater Kolkata.</p></div>
{area_groups()}
</div></section>
<section class="section section-alt"><div class="wrap">
<div class="section-head reveal"><h2>Local TV service pages</h2></div>
<div class="grid g3">{cards}</div></div></section>{cta()}'''
    page(path, "TV Repair Service Areas | Kolkata, Howrah, Hooghly & 24 Parganas",
         "Areas covered by RJB LED LCD TV Service Centre: Kolkata, Howrah, Bally, Uttarpara, Chandannagar, Barrackpore, "
         "Naihati, Budge Budge and more. LED, LCD and Smart TV repair.",
         body, active="service-areas", og_img="howrah-bridge",
         schema=[crumbs_schema([("Home", "/"), ("Service Areas", path)]),
                 {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": ORIGIN + url(a["slug"]), "name": a["place"]} for i, a in enumerate(AREAS)]}],
         priority="0.8")


def build_led_vs_lcd():
    slug = "led-vs-lcd-tv"
    path = url(slug)
    faq = [
        ("Which is better, LED or LCD TV?",
         "For a new purchase, an LED-backlit TV is better: brighter, slimmer and more energy-efficient than an older CCFL-backlit LCD. But since every LED TV is also an LCD TV, the real comparison is between backlight types, and between edge-lit and full-array LED designs."),
        ("Is an LED TV the same as an LCD TV?",
         "Almost. Both use a liquid-crystal display panel. 'LED TV' is a marketing name for an LCD TV that uses LEDs as its backlight instead of fluorescent tubes."),
        ("Is OLED better than LED?",
         "OLED pixels make their own light, so blacks are perfectly black and contrast is excellent. LED TVs get brighter and cost less for a given size, and they have no risk of burn-in from static images."),
        ("Which lasts longer, LED or LCD?",
         "LED backlights generally outlast fluorescent CCFL tubes, but LED strips are also the most common failure in modern TVs. The good news is that both are repairable when the panel itself is undamaged."),
    ]
    body = page_hero("LED vs LCD TV: Which Is Better?",
                     "What the labels really mean, how each type makes its picture, which one to buy, and how each one fails.",
                     [("Home", "/"), ("LED vs LCD TV", path)], "tv-glow-room", "LED TV glowing in a dark room", "TV buying &amp; repair guide")
    body += f'''<section class="section"><div class="wrap layout"><article class="prose">
<h2>The short answer</h2>
<p>An LED TV <strong>is</strong> an LCD TV. Both use a liquid-crystal panel that blocks or passes light to form the picture. What differs is the light behind the panel: older LCD TVs use cold-cathode fluorescent lamps (CCFL), while "LED TVs" use light-emitting diodes. So when people ask whether LED or LCD is better, what they're really asking is which <em>backlight</em> is better, and the answer is LED.</p>
<h2>See the difference</h2>
<p>Switch between the three backlight designs below to see where the light comes from and how they compare.</p>
{compare()}
<h2>LED vs LCD: side by side</h2>
<table><thead><tr><th></th><th>LCD (CCFL backlight)</th><th>LED (edge-lit)</th><th>LED (direct / full-array)</th></tr></thead><tbody>
<tr><td>Light source</td><td>Fluorescent tubes</td><td>LEDs along the edges</td><td>LED grid behind the panel</td></tr>
<tr><td>Thickness</td><td>Thickest</td><td>Thinnest</td><td>Slim</td></tr>
<tr><td>Brightness</td><td>Moderate</td><td>Good</td><td>Very good</td></tr>
<tr><td>Black levels</td><td>Greyish</td><td>Can 'cloud' on dark scenes</td><td>Best, especially with local dimming</td></tr>
<tr><td>Power use</td><td>Highest</td><td>Low</td><td>Low to moderate</td></tr>
<tr><td>Typical failure</td><td>Lamp or inverter board</td><td>Edge LED strip</td><td>LED strips behind the panel</td></tr>
</tbody></table>
<h2>What about OLED and QLED?</h2>
<p><strong>QLED</strong> is still an LED-backlit LCD; it adds a quantum-dot layer for richer colour. <strong>OLED</strong> is different: each pixel emits its own light, so there is no backlight at all. That gives perfect blacks, but OLED panels cost more and can suffer burn-in from static logos over years of use.</p>
<figure>{img("tv-back-panel", "Back panel of a flat screen LED TV", w=1000, h=700)}<figcaption>The backlight and boards live behind this panel, and so do most faults.</figcaption></figure>
<h2>Which should you buy?</h2>
<ul>
<li><strong>Everyday TV, bright room:</strong> a direct-lit LED TV gives the best value.</li>
<li><strong>Movies in a dark room:</strong> full-array LED with local dimming, or OLED if budget allows.</li>
<li><strong>Thinnest possible on the wall:</strong> edge-lit LED or OLED.</li>
</ul>
<h2>Should you repair your old LCD TV or replace it?</h2>
<p>If your LCD or LED TV has a healthy panel, the most common faults (backlight, power supply, boards) cost far less to repair than a new TV. If the panel is cracked or has failed internally, replacement usually makes more sense. Our <a href="/led-lcd-tv-repairing-in-kolkata/">LED LCD TV repairing service</a> will tell you which applies to your set.</p>
{faq_block(faq)}
</article>{sidebar(slug)}</div></section>{cta("Not sure if your TV is worth fixing?")}'''
    page(path, "LED vs LCD TV: Which Is Better? (Explained Simply)",
         "LED vs LCD TV explained: what the difference really is, which is better to buy, how OLED and QLED compare, and "
         "whether to repair or replace an old LCD TV.", body, active=slug, og_img="tv-glow-room",
         schema=[{"@type": "Article", "headline": "LED vs LCD TV: Which Is Better?", "datePublished": "2026-10-12", "dateModified": TODAY,
                  "author": {"@type": "Organization", "name": BIZ["name"]}, "publisher": {"@id": BUSINESS_ID},
                  "image": ORIGIN + "/assets/img/tv-glow-room.webp", "mainEntityOfPage": ORIGIN + path},
                 crumbs_schema([("Home", "/"), ("LED vs LCD TV", path)]), faq_schema(faq)], priority="0.8")


def build_about():
    path = "/about/"
    body = page_hero("About RJB LED LCD TV Service Centre",
                     "A Kolkata TV repair workshop built around one idea: fix the part that failed, and be honest about the rest.",
                     [("Home", "/"), ("About", path)], "repair-shop", "Electronics repair workshop with technicians at work", "Our story")
    body += f'''<section class="section"><div class="wrap split">
<div class="reveal"><h2>Repair, not replacement</h2>
<p class="lead">RJB LED LCD TV Service Centre repairs flat-screen televisions for Kolkata households, from older LCD sets to the latest 4K Smart TVs.</p>
<p>The technology keeps changing, from CCFL-lit LCD to LED, QLED and OLED. What doesn't change is the approach: diagnose properly, repair at component level, test thoroughly and explain everything in plain language.</p>
<p>That means fewer unnecessary board swaps, lower bills, and TVs that keep working long after the manufacturer has stopped making spare parts for them.</p>
<ul class="ticks"><li><strong>Multi-brand:</strong> Samsung, Sony, LG, Videocon and every major brand sold in India.</li>
<li><strong>Every technology:</strong> LCD (CCFL), LED, QLED, Smart TV and OLED boards.</li>
<li><strong>Independent:</strong> no brand affiliation, so our advice is about your TV, not a sales target.</li></ul></div>
<div class="media-stack reveal" style="--d:.1s"><div class="media">{img("workbench-multimeter", "TV repair bench with multimeter and test boards", w=1200, h=800)}</div>
<div class="media small">{img("circuit-board", "TV circuit board close-up", w=1600, h=1000)}</div></div>
</div></section>
<section class="section section-alt"><div class="wrap"><div class="section-head center reveal"><h2>How we work</h2></div>{timeline()}</div></section>{cta()}'''
    page(path, "About Us | RJB LED LCD TV Service Centre Kolkata",
         "About RJB LED LCD TV Service Centre: independent, multi-brand LED and LCD TV repair in Kolkata with board-level diagnosis and honest advice.",
         body, active="about", og_img="repair-shop",
         schema=[crumbs_schema([("Home", "/"), ("About", path)]), {"@type": "AboutPage", "url": ORIGIN + path}], priority="0.5")


def build_contact():
    path = "/contact/"
    brand_opts = "".join(f"<option>{m}</option>" for m in MARQUEE) + "<option>Other</option>"
    fault_opts = "".join(f"<option>{s[1]}</option>" for s in SYMPTOMS) + "<option>Something else</option>"
    body = page_hero("Contact &amp; Book a TV Repair",
                     "Tell us what your TV is doing. We'll reply by email with the likely cause and the next steps.",
                     [("Home", "/"), ("Contact", path)], "tv-remote", "Hand holding a TV remote in front of a smart TV", "Get in touch")
    body += f'''<section class="section"><div class="wrap contact-grid">
<div class="reveal"><h2>Talk to a technician</h2>
<p class="lead">The fastest way to get help is to email us the brand, model number (on the sticker at the back) and a short description or photo of the fault.</p>
<ul class="info-list">
<li><span class="icon">{icon("mail")}</span><div><b>Email</b><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></div></li>
<li><span class="icon">{icon("pin")}</span><div><b>Service area</b><span>Kolkata, Howrah, Hooghly, North &amp; South 24 Parganas, West Bengal</span></div></li>
<li><span class="icon">{icon("clock")}</span><div><b>Replies</b><span>We answer every repair request by email.</span></div></li>
</ul></div>
<form class="form reveal" style="--d:.1s" action="/send.php" method="post">
<div id="form-status" role="status" hidden></div>
<div class="row"><label>Your name<input name="name" required autocomplete="name"></label>
<label>Email<input name="email" type="email" required autocomplete="email"></label></div>
<div class="row"><label>Phone (optional)<input name="phone" type="tel" autocomplete="tel"></label>
<label>Area / locality<input name="area" placeholder="e.g. Salt Lake, Bally" autocomplete="address-level2"></label></div>
<div class="row"><label>TV brand<select name="brand">{brand_opts}</select></label>
<label>Main symptom<select name="fault">{fault_opts}</select></label></div>
<label>Model number &amp; details<textarea name="message" placeholder="Model number, screen size, and what the TV is doing" required></textarea></label>
<label class="hp" aria-hidden="true">Leave blank<input name="website" tabindex="-1" autocomplete="off"></label>
<button class="btn btn-glow" type="submit">Send repair request {icon("send")}</button>
<p class="form-note">We only use your details to reply to this request. See our <a href="/privacy-policy/">privacy policy</a>.</p>
</form></div></section>'''
    page(path, "Contact RJB LED LCD TV Service Centre | Book a TV Repair in Kolkata",
         "Book an LED, LCD or Smart TV repair in Kolkata. Email info@rjbledlcdtvservicecentre.com or send the repair form with your TV's brand, model and fault.",
         body, active="contact", og_img="tv-remote",
         schema=[crumbs_schema([("Home", "/"), ("Contact", path)]), {"@type": "ContactPage", "url": ORIGIN + path}], priority="0.6")


def build_privacy():
    path = "/privacy-policy/"
    body = page_hero("Privacy Policy", "How we handle the details you send us.", [("Home", "/"), ("Privacy Policy", path)],
                     "circuit-board", "Circuit board", "Legal")
    body += f'''<section class="section"><div class="wrap"><article class="prose" style="max-width:780px">
<p>Last updated: {date.today().strftime("%d %B %Y")}</p>
<h2>What we collect</h2><p>When you email us or use the contact form, we receive the details you provide: your name, email address, optional phone number, locality, and information about your TV and its fault.</p>
<h2>How we use it</h2><p>We use these details only to reply to your enquiry and carry out any repair you ask for. We do not sell or share your information with third parties for marketing.</p>
<h2>Cookies and analytics</h2><p>This website does not set advertising cookies. Fonts are loaded from Google Fonts, which may log standard request data such as your IP address.</p>
<h2>Keeping and deleting data</h2><p>We keep enquiry emails only as long as needed to handle your repair and any follow-up. To ask us to delete your information, email <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>.</p>
<h2>Contact</h2><p>{BIZ['name']}, Kolkata, West Bengal. Email: <a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
</article></div></section>'''
    page(path, "Privacy Policy | RJB LED LCD TV Service Centre",
         "Privacy policy for RJB LED LCD TV Service Centre, Kolkata: what we collect when you contact us and how we use it.",
         body, active=None, schema=[crumbs_schema([("Home", "/"), ("Privacy Policy", path)])], priority="0.2")


def build_404():
    body = f'''<section class="nosignal"><div class="wrap">
<div class="tv-frame"><div class="tv-screen"><canvas class="static" aria-hidden="true"></canvas><span class="tv-osd">NO SIGNAL</span></div></div>
<h1>404: No signal on this channel</h1>
<p class="lead" style="margin:0 auto 28px">The page you were looking for has moved or never existed. Try one of these instead.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-glow" href="/">Home {icon("arrow")}</a>
<a class="btn btn-ghost" href="/led-lcd-tv-repairing-in-kolkata/">TV repairs</a><a class="btn btn-ghost" href="/contact/">Contact</a></div>
</div></section>'''
    page("/404.html", "Page Not Found | RJB LED LCD TV Service Centre", "This page could not be found.", body)


# ------------------------------------------------------------------ server files
def build_php():
    redirects = {f"/tag/{k}": url(v) for k, v in TAG_REDIRECTS.items()}
    redirects["/author/admin"] = "/about/"
    pairs = ",\n".join(f"    '{k}' => '{v}'" for k, v in sorted(redirects.items()))
    (OUT / "index.php").write_text(f'''<?php
// {BIZ['domain']} front controller. The host serves real files directly, ignores
// .htaccess and routes "/" plus every unknown path here. See README "Hosting".
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://{BIZ['domain']}';

// Canonical host/scheme, only once the real domain points here (the temporary
// *.hostingersite.com domain is left alone). TLS terminates upstream.
if (strpos($host, '{BIZ['domain']}') !== false) {{
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host === 'www.{BIZ['domain']}') {{
        header('Location: ' . $home . $uri, true, 301);
        exit;
    }}
}}

if ($path === '/' || $path === '/index.php') {{
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}}

// Old WordPress URLs that still carry links or rankings.
$legacy = [
{pairs}
];
$key = rtrim($path, '/');
if (isset($legacy[$key])) {{
    header('Location: ' . $legacy[$key], true, 301);
    exit;
}}
if (preg_match('#^/tag/#', $path)) {{
    header('Location: /service-areas/', true, 301);
    exit;
}}
if (preg_match('#^/(feed|comments/feed|category/[^/]+)/?$#', $path)) {{
    header('Location: /', true, 301);
    exit;
}}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\\.php|xmlrpc\\.php)(/|$)#', $path)) {{
    header('Location: /', true, 301);
    exit;
}}
// /some-page -> /some-page/ (old backlinks often omit the slash)
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {{
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}}
// /some-page/ without index.html on this host -> serve it if present
$candidate = __DIR__ . rtrim($path, '/') . '/index.html';
if (strpos($path, '..') === false && is_file($candidate)) {{
    header('Content-Type: text/html; charset=utf-8');
    readfile($candidate);
    exit;
}}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
''', encoding="utf-8")

    (OUT / "send.php").write_text(f'''<?php
// Contact form handler: emails the repair request to the business inbox.
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {{ header('Location: /contact/', true, 303); exit; }}
function field($k, $max = 2000) {{
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\\r", "\\n"], ' ', mb_substr($v, 0, $max));
    return $v;
}}
if (field('website') !== '') {{ header('Location: /contact/?sent=1', true, 303); exit; }}  // honeypot
$name = field('name', 120);
$email = filter_var(field('email', 200), FILTER_VALIDATE_EMAIL);
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 5000));
if (!$name || !$email || $message === '') {{ header('Location: /contact/?sent=0', true, 303); exit; }}
$to = '{BIZ['email']}';
$subject = 'TV repair request: ' . field('brand', 60) . ' - ' . field('fault', 80);
$body = "Name: $name\\nEmail: $email\\nPhone: " . field('phone', 40) . "\\nArea: " . field('area', 120)
      . "\\nBrand: " . field('brand', 60) . "\\nSymptom: " . field('fault', 80) . "\\n\\n" . $message . "\\n";
$headers = "From: RJB Website <{BIZ['email']}>\\r\\nReply-To: $email\\r\\nContent-Type: text/plain; charset=UTF-8";
$ok = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
header('Location: /contact/?sent=' . ($ok ? '1' : '0'), true, 303);
''', encoding="utf-8")


def build_static_files():
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" x2="1">'
        '<stop offset="0" stop-color="#ff3d6e"/><stop offset=".4" stop-color="#a855f7"/><stop offset=".7" stop-color="#3d8bff"/>'
        '<stop offset="1" stop-color="#22e6a0"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="#06070c"/>'
        '<rect x="8" y="14" width="48" height="32" rx="5" fill="none" stroke="#fff" stroke-width="4"/>'
        '<rect x="13" y="19" width="38" height="22" rx="2" fill="url(#g)"/><rect x="24" y="50" width="16" height="4" rx="2" fill="#fff"/></svg>',
        encoding="utf-8")
    if STAGING:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nDisallow: /home.html\nDisallow: /send.php\n\nSitemap: {ORIGIN}/sitemap.xml\n"
    (OUT / "robots.txt").write_text(robots, encoding="utf-8")
    urls = "".join(f"<url><loc>{ORIGIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in SITEMAP)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding="utf-8")


def main():
    build_home()
    build_repairing()
    for k in BRAND_ORDER:
        build_brand(k)
    for i, a in enumerate(AREAS):
        build_area(i, a)
    build_areas_hub()
    build_led_vs_lcd()
    build_about()
    build_contact()
    build_privacy()
    build_404()
    build_php()
    build_static_files()
    print(f"built {len(SITEMAP)} pages into {OUT} ({'STAGING' if STAGING else 'production'})")


if __name__ == "__main__":
    main()
