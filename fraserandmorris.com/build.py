#!/usr/bin/env python3
"""Static site generator for fraserandmorris.com.

Writes every page into this directory. Run `python3 build.py`, then
`python3 validate.py`. No dependencies beyond the standard library.
"""

import html
import json
import os
from datetime import date

from content import GARDENS, HOME_FAQ

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN = "https://fraserandmorris.com"
NAME = "Fraser & Morris"
EMAIL = "info@fraserandmorris.com"
TODAY = date.today().isoformat()
GARDEN_BY_SLUG = {g["slug"]: g for g in GARDENS}

ICON = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "caret": '<svg class="caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
    "leaf": '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M6 26C6 13 14 5 27 5c0 13-8 21-21 21z" fill="currentColor" opacity=".18"/><path d="M6 26C6 13 14 5 27 5c0 13-8 21-21 21zM6 26L19 13" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
    "pencil": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21l3.5-1 12-12-2.5-2.5-12 12L3 21zM14.5 6l2.5 2.5"/><path d="M3 10V3h7M14 21h7v-7"/></svg>',
    "sprout": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21v-9"/><path d="M12 12C12 7 9 4 4 4c0 5 3 8 8 8zM12 14c0-4 3-7 8-7 0 4-3 7-8 7z"/><path d="M7 21h10"/></svg>',
    "spade": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v9M9 2h6"/><path d="M7 11h10v4a5 5 0 0 1-10 0v-4z"/><path d="M12 20v2"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M9 15l2 2 4-4"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
}

NAV = [
    ("Home", "/"),
    ("Gardens", "/gardens.html"),
    ("Services", "/services.html"),
    ("About", "/about.html"),
    ("Contact", "/contact.html"),
]

AREAS = [
    ("North London", "Highgate, Hampstead, Belsize Park, Islington, Primrose Hill and Muswell Hill."),
    ("South London", "Camberwell, Dulwich, Peckham, Brixton, Clapham, Kennington and Greenwich."),
    ("Oxfordshire &amp; Cotswolds", "Country gardens across Oxfordshire, the Cotswolds, Berkshire and Buckinghamshire."),
    ("Suffolk &amp; Sussex", "Coastal and country gardens in Suffolk, East and West Sussex and Kent."),
]


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    out, skip = [], False
    for ch in s:
        if ch == "<":
            skip = True
        elif ch == ">":
            skip = False
        elif not skip:
            out.append(ch)
    return "".join(out)


def img(name, alt, w, h, cls="", lazy=True, extra=""):
    attrs = f' class="{cls}"' if cls else ""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="/assets/img/{name}.webp" alt="{esc(alt)}" width="{w}" height="{h}"{attrs}{load}{extra}>'


IMG_SIZE = {}


def load_sizes():
    import struct
    d = os.path.join(ROOT, "assets", "img")
    for f in os.listdir(d):
        if not f.endswith(".webp"):
            continue
        with open(os.path.join(d, f), "rb") as fh:
            data = fh.read(40)
        chunk = data[12:16]
        if chunk == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            IMG_SIZE[f[:-5]] = (w & 0x3FFF, h & 0x3FFF)
        elif chunk == b"VP8L":
            b = data[21:25]
            bits = int.from_bytes(b, "little")
            IMG_SIZE[f[:-5]] = ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        elif chunk == b"VP8X":
            w = int.from_bytes(data[24:27], "little") + 1
            h = int.from_bytes(data[27:30], "little") + 1
            IMG_SIZE[f[:-5]] = (w, h)


def pic(name, alt, cls="", lazy=True, extra=""):
    w, h = IMG_SIZE[name]
    return img(name, alt, w, h, cls, lazy, extra)


ALT = {
    "hero-garden-path": "Curving garden path through lush borders of white roses and clipped shrubs towards a large house",
    "courtyard-fountain": "Enclosed courtyard garden with a stone fountain, palms and lush green planting",
    "courtyard-pots": "Sunny paved courtyard with potted trees and flowering shrubs",
    "courtyard-patio": "Town house garden with climbing plants and pots of flowers on the terrace",
    "town-house-door": "Period town house entrance flanked by clipped topiary in terracotta pots",
    "family-lawn": "Long family lawn with a stone path, weeping willow and mature trees",
    "family-house-garden": "Family house with a formal garden of rounded shrubs, white roses and a stone birdbath",
    "country-house-garden": "Country house with a manicured lawn and colourful flower beds",
    "country-topiary": "Clipped yew topiary on a broad lawn in an English country garden",
    "lush-glasshouse": "Lush ferns and tropical foliage under a Victorian glasshouse roof",
    "fern-detail": "Dense green fern fronds in shade",
    "fern-dark": "Fern fronds against a dark woodland floor",
    "woodland-fern": "Fern growing in the dim light of a dense woodland",
    "artist-studio": "Small pink garden studio among climbing roses and lawn",
    "study-window": "Window of a study looking out onto a green garden with hanging plants",
    "modern-patio": "Modern garden room with large windows, chairs and planting",
    "terracotta-pot": "Terracotta pot with a climbing plant against a white wall",
    "hands-planting": "Gardener in gloves planting seedlings into prepared soil",
    "hands-seedling": "Hands holding a young seedling in garden soil",
    "hands-trowel": "Gloved hands planting a young plant with a trowel",
    "dahlias": "Coral, peach and cream dahlias in full bloom",
    "dahlia-pink": "Pink pompon dahlia in soft focus",
    "allium": "Purple allium flower heads in a green garden",
    "allium-field": "Purple alliums standing above green foliage",
    "salvia": "Purple salvia flowers in a summer border",
    "meadow-path": "Mown path running through long meadow grasses",
}


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


ORG = {
    "@type": ["ProfessionalService", "LocalBusiness"],
    "@id": ORIGIN + "/#business",
    "name": NAME,
    "alternateName": "Fraser and Morris",
    "description": "Plant-led garden design and planting studio based in London, designing town, courtyard, family and country gardens.",
    "url": ORIGIN + "/",
    "email": EMAIL,
    "image": ORIGIN + "/assets/img/hero-garden-path.webp",
    "logo": ORIGIN + "/assets/img/logo.svg",
    "priceRange": "££",
    "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
    "areaServed": ["London", "North London", "South London", "Oxfordshire", "Cotswolds", "Suffolk", "Sussex"],
    "knowsAbout": ["Garden design", "Planting design", "Courtyard garden design", "Town garden design", "Family garden design", "Architectural planting"],
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": NAME, "publisher": {"@id": ORIGIN + "/#business"}}


def breadcrumbs(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(items)
        ],
    }


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs
        ],
    }


def header(current, light=False):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        if label == "Gardens":
            sub = "".join(
                f'<li><a href="/gardens/{g["slug"]}.html">{esc(g["nav"])}<small>{esc(g["tag"])}</small></a></li>'
                for g in GARDENS
            )
            sub = f'<li><a href="/gardens.html">All gardens<small>Overview of our work</small></a></li>' + sub
            items.append(
                f'<li class="has-sub"><button type="button" class="nav-link" aria-expanded="false" aria-controls="sub-gardens">Gardens {ICON["caret"]}</button>'
                f'<ul class="sub" id="sub-gardens">{sub}</ul></li>'
            )
        else:
            items.append(f'<li><a class="nav-link" href="{href}"{cur}>{label}</a></li>')
    cls = "site-header is-light" if light else "site-header"
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="{cls}">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{NAME} home">{ICON["leaf"]}<span>Fraser<span class="amp">&amp;</span>Morris</span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{"".join(items)}</ul>
      <a class="btn" href="/contact.html">Start your garden {ICON["arrow"]}</a>
      <p class="nav-contact">Garden design &amp; planting, London<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </nav>
  </div>
</header>"""


def footer():
    gardens = "".join(f'<li><a href="/gardens/{g["slug"]}.html">{esc(g["nav"])}</a></li>' for g in GARDENS[:6])
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/">{ICON["leaf"]}<span>Fraser<span class="amp">&amp;</span>Morris</span></a>
        <p>A plant-led garden design studio creating town, courtyard, family and country gardens across London, Oxfordshire, Suffolk and Sussex.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Gardens</h4><ul>{gardens}<li><a href="/gardens.html">All gardens</a></li></ul></div>
      <div><h4>Studio</h4><ul><li><a href="/about.html">About</a></li><li><a href="/services.html">Services</a></li><li><a href="/contact.html">Contact</a></li><li><a href="/privacy.html">Privacy</a></li></ul></div>
      <div><h4>Areas</h4><ul><li>North London</li><li>South London</li><li>Oxfordshire</li><li>Suffolk &amp; Sussex</li></ul></div>
    </div>
    <div class="footer-bottom"><span>&copy; <span id="year">{date.today().year}</span> {NAME}. Garden design &amp; planting.</span><span>London &middot; Oxfordshire &middot; Suffolk &middot; Sussex</span></div>
  </div>
  <div class="footer-big" aria-hidden="true">Fraser&amp;Morris</div>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><svg class="ring" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="24"/></svg>{ICON["up"]}</button>
<script src="/assets/js/site.js" defer></script>"""


def page(path, title, description, body, current, schema=None, og_image="hero-garden-path", light=False, robots="index,follow"):
    canonical = ORIGIN + ("/" if path == "/" else path)
    graph = [ORG, WEBSITE] + (schema or [])
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta name="theme-color" content="#1c2b22">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..500;1,9..144,300..500&amp;family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
{header(current, light)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


def photo_hero(image, eyebrow, h1, lead, crumbs=None, actions="", cls="hero page-hero", petals=False):
    crumb_html = ""
    if crumbs:
        parts = [f'<a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]] + [f"<span aria-current=\"page\">{esc(crumbs[-1][0])}</span>"]
        crumb_html = '<nav class="crumbs fade-up" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"
    canvas = '<canvas aria-hidden="true"></canvas>' if petals else ""
    return f"""<section class="{cls}">
  <div class="hero__media" data-parallax="0.25">{pic(image, ALT[image], lazy=False)}</div>
  {canvas}
  <div class="hero__content"><div class="wrap">
    {crumb_html}
    <p class="eyebrow fade-up">{eyebrow}</p>
    <h1 class="fade-up">{h1}</h1>
    <p class="lead fade-up d2">{lead}</p>
    {actions}
  </div></div>
</section>"""


def split_h1(text):
    """Wrap each line (split on |) in animated spans."""
    return "".join(f'<span class="split-line"><span>{line}</span></span>' for line in text.split("|"))


def garden_cards(slugs, related=False):
    cards = []
    for i, s in enumerate(slugs):
        g = GARDEN_BY_SLUG[s]
        cards.append(
            f'<a class="card reveal" data-delay="{i % 3}" href="/gardens/{s}.html">{pic(g["hero"], ALT[g["hero"]])}'
            f'<span class="arrow">{ICON["arrow"]}</span>'
            f'<span class="card__body"><span class="card__tag">{esc(g["tag"])}</span><h3>{esc(g["nav"])}</h3><p>{esc(g["card"])}</p></span></a>'
        )
    return f'<div class="cards{" cards--related" if related else ""}">' + "".join(cards) + "</div>"


def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{esc(q)}</summary><div class="answer"><p>{esc(a)}</p></div></details>' for q, a in faqs
    ) + "</div>"


def cta(title="Let's talk about <em>your garden</em>", text="Tell us a little about your garden and what you would like from it. We will arrange a visit to see the space, talk through ideas and explain how we can help.", image="fern-dark"):
    return f"""<section class="section"><div class="wrap">
  <div class="cta reveal">{pic(image, "")}
    <p class="eyebrow">Start a conversation</p>
    <h2>{title}</h2>
    <p>{text}</p>
    <a class="btn" href="/contact.html">Book a consultation {ICON["arrow"]}</a>
  </div>
</div></section>"""


SERVICES = [
    ("pencil", "Garden design", "A complete design: measured survey, concept, detailed layout, construction drawings and a planting plan, ready to build."),
    ("sprout", "Planting design", "Planting plans for new borders or a whole garden, with plants sourced, set out and placed by us on the day."),
    ("spade", "Build management", "We tender the work to trusted landscapers, oversee the build and make sure the details are right."),
    ("calendar", "Aftercare", "Seasonal visits in the first years to edit, replant and guide the garden as it matures."),
]

PROCESS = [
    ("Consultation", "We visit, walk the garden with you and talk about how you want to use it."),
    ("Survey", "A measured survey records levels, boundaries, trees, soil and aspect."),
    ("Concept", "Sketch layouts and mood images explore ideas before anything is fixed."),
    ("Design", "A detailed plan, drawings and planting plan, costed and ready to build."),
    ("Build &amp; plant", "We oversee the landscapers and set out every plant ourselves."),
]

SEASONS = [
    ("Spring", "allium", "Bulbs push through, blossom opens and fresh foliage unfurls. We plan for a long spring: snowdrops and hellebores, then tulips, alliums, blossom and the first perennials.",
     ["Tulips", "Alliums", "Crab apple blossom", "Hellebores", "Epimedium", "Camassia"]),
    ("Summer", "dahlias", "Borders reach their height. Roses, salvias, geraniums and grasses carry the garden from June into a late summer flush of dahlias and asters.",
     ["Roses", "Salvias", "Dahlias", "Geranium 'Rozanne'", "Verbena bonariensis", "Agapanthus"]),
    ("Autumn", "meadow-path", "Grasses turn to straw and copper, seedheads form and leaves colour. Autumn planting is often the most atmospheric of the year.",
     ["Miscanthus", "Sanguisorba", "Asters", "Japanese maple", "Persicaria", "Malus fruit"]),
    ("Winter", "country-topiary", "Structure takes over. Clipped evergreens, bark, seedheads and winter-flowering shrubs keep a well-designed garden alive in the coldest months.",
     ["Yew &amp; clipped shapes", "Betula bark", "Sarcococca", "Hellebores", "Grasses", "Snowdrops"]),
]


def build_home():
    services = "".join(
        f'<div class="service reveal" data-delay="{i}"><span class="num">0{i + 1}</span><div class="icon">{ICON[ic]}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, (ic, t, d) in enumerate(SERVICES)
    )
    process = '<div class="process"><span class="line"></span>' + "".join(
        f'<div class="step reveal" data-delay="{min(i, 3)}"><div class="dot">{i + 1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS)
    ) + "</div>"
    tabs = "".join(
        f'<button class="tab" type="button" role="tab" id="tab-{s.lower()}" aria-controls="panel-{s.lower()}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{s}</button>'
        for i, (s, *_r) in enumerate(SEASONS)
    )
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="panel-{s.lower()}" aria-labelledby="tab-{s.lower()}"{"" if i == 0 else " hidden"}><p>{t}</p><ul>{"".join(f"<li>{p}</li>" for p in plants)}</ul></div>'
        for i, (s, _im, t, plants) in enumerate(SEASONS)
    )
    season_imgs = "".join(
        pic(im, f"{s} planting: {ALT[im]}", "on" if i == 0 else "") for i, (s, im, *_r) in enumerate(SEASONS)
    )
    areas = "".join(
        f'<div class="area reveal" data-delay="{i}">{ICON["pin"]}<h3>{n}</h3><p>{d}</p></div>' for i, (n, d) in enumerate(AREAS)
    )
    plants = ["Dahlias", "Crab apples", "Alliums", "Ornamental grasses", "Ferns", "Old roses", "Salvias", "Clipped yew", "Hellebores", "Meadow", "Tulips", "Sanguisorba"]
    marquee = "".join(f"<span>{p}</span>" for p in plants * 2)

    body = f"""
<section class="hero">
  <div class="hero__media" data-parallax="0.3">{pic("hero-garden-path", ALT["hero-garden-path"], lazy=False)}</div>
  <canvas aria-hidden="true"></canvas>
  <div class="hero__content"><div class="wrap">
    <p class="eyebrow fade-up">Garden design &amp; planting &middot; London</p>
    <h1>{split_h1("Gardens designed|from the <em>plants</em> up")}</h1>
    <p class="lead fade-up d2">Fraser &amp; Morris is a plant-led garden design studio. We create town, courtyard, family and country gardens across London, Oxfordshire, Suffolk and Sussex, with planting that looks good in every season.</p>
    <div class="hero__actions fade-up d3"><a class="btn" href="/contact.html">Book a consultation {ICON["arrow"]}</a><a class="btn btn--ghost" href="/gardens.html">Explore our gardens</a></div>
  </div></div>
  <a class="hero__scroll" href="#intro">Scroll</a>
</section>

<section class="section" id="intro"><div class="wrap split">
  <div class="stack reveal">
    <div class="main reveal-img">{pic("hands-planting", ALT["hands-planting"])}</div>
    <div class="inset">{pic("dahlia-pink", ALT["dahlia-pink"])}</div>
    <div class="badge" aria-hidden="true"><svg viewBox="0 0 130 130"><defs><path id="circ" d="M65,65 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs><text font-size="11" letter-spacing="3" fill="#fff" font-family="Manrope, sans-serif" font-weight="700"><textPath href="#circ">PLANT-LED &#8226; GARDEN DESIGN &#8226; LONDON &#8226;</textPath></text></svg><b>&#10049;</b></div>
  </div>
  <div class="reveal" data-delay="1">
    <p class="eyebrow">The studio</p>
    <h2>A garden designer who starts with <em>the planting</em></h2>
    <p>Fraser &amp; Morris designs gardens around plants. Layout, paving and structure matter, and we draw them carefully, but what makes a garden memorable is how it is planted: the layering, the colour, the way it changes through the year.</p>
    <p>Whether it is a shaded courtyard in south London, a family garden in Highgate or a country garden in Oxfordshire, we design for the site, the soil and the people who will use it.</p>
    <ul class="checks"><li>Planting plans drawn and set out by the designer</li><li>Gardens that look good in winter as well as June</li><li>Practical layouts for families, entertaining and working from home</li></ul>
    <a class="btn btn--dark" href="/about.html">About our approach {ICON["arrow"]}</a>
  </div>
</div></section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee}</div></div>

<section class="section section--cream"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">Gardens</p><h2>Every garden starts with <em>its setting</em></h2></div><p>From enclosed courtyards to country gardens that open onto fields, these are the kinds of gardens we design most often, and how we approach each one.</p></div>
  {garden_cards([g["slug"] for g in GARDENS[:6]])}
  <p style="text-align:center;margin:90px 0 0"><a class="btn btn--dark" href="/gardens.html">See all garden types {ICON["arrow"]}</a></p>
</div></section>

<section class="section section--dark"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">Services</p><h2>From first sketch to <em>first flowering</em></h2></div><p>We can take a garden from survey to planting, or help with one part of it. Every project starts with a conversation in the garden.</p></div>
  <div class="services">{services}</div>
  <p style="margin:40px 0 0"><a class="btn" href="/services.html">Our services in detail {ICON["arrow"]}</a></p>
</div></section>

<section class="band">
  <div class="band__media" data-parallax="0.18">{pic("lush-glasshouse", ALT["lush-glasshouse"])}</div>
  <div class="wrap reveal"><blockquote>&ldquo;A garden is never finished. We design the first chapter, and <em>the plants</em> write the rest.&rdquo;</blockquote><cite>The Fraser &amp; Morris approach</cite></div>
</section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">How it works</p><h2>A clear process, <em>start to finish</em></h2></div><p>Designing a garden is a collaboration. Here is what happens between the first visit and the first summer.</p></div>
  {process}
</div></section>

<section class="section section--cream"><div class="wrap seasons" data-tabs>
  <div class="reveal">
    <p class="eyebrow">Planting through the year</p>
    <h2>Gardens designed for <em>all four seasons</em></h2>
    <p>Choose a season to see how a Fraser &amp; Morris planting plan keeps the garden interesting all year round.</p>
    <div class="tabs" role="tablist" aria-label="Seasons">{tabs}</div>
    {panels}
  </div>
  <div class="season-media reveal" data-delay="1">{season_imgs}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">Where we work</p><h2>London gardens, and <em>beyond</em></h2></div><p>Based in London, we design gardens across the capital and in the countryside of Oxfordshire, Suffolk and Sussex.</p></div>
  <div class="areas">{areas}</div>
</div></section>

<section class="section section--cream"><div class="wrap">
  <div class="section-head reveal" style="justify-content:center;text-align:center"><div><p class="eyebrow">Questions</p><h2>Frequently asked</h2></div></div>
  {faq_html(HOME_FAQ)}
</div></section>
{cta()}
"""
    title = "Fraser & Morris | Garden Design London | Plant-Led Garden Designers"
    desc = "Fraser & Morris is a plant-led garden design studio in London creating courtyard, town, family and country gardens across London, Oxfordshire, Suffolk and Sussex."
    return page("/", title, desc, body, "/", [faq_schema(HOME_FAQ)])


def build_garden(g):
    path = f"/gardens/{g['slug']}.html"
    crumbs = [("Home", "/"), ("Gardens", "/gardens.html"), (g["nav"], path)]
    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in g["facts"])
    palette = "".join(f"<span>{esc(p)}</span>" for p in g["palette"])
    duo = '<div class="duo">' + "".join(f'<div class="reveal-img">{pic(n, ALT[n])}</div>' for n in g["duo"]) + "</div>"
    body_html = g["body"].strip()
    # place the image pair before the final h2 section
    idx = body_html.rfind("<h2>")
    body_html = body_html[:idx] + duo + body_html[idx:]
    lead = esc(g["description"])
    body = f"""
{photo_hero(g["hero"], esc(g["kicker"]), g["h1"], lead, crumbs, f'<div class="hero__actions fade-up d3"><a class="btn" href="/contact.html">Discuss your garden {ICON["arrow"]}</a></div>')}
<section class="section"><div class="wrap prose-grid">
  <article class="prose reveal">{body_html}</article>
  <aside class="aside">
    <div class="aside-card reveal"><h3>At a glance</h3><dl>{facts}<div><dt>Signature plants</dt><dd><div class="palette">{palette}</div></dd></div></dl></div>
    <div class="aside-card aside-card--dark reveal"><h3>Planning a {esc(g["tag"].lower())}?</h3><p>Tell us about your space and we will arrange a consultation visit.</p><a class="btn" href="/contact.html">Get in touch {ICON["arrow"]}</a><p style="margin:16px 0 0;font-size:.9rem">Or email <a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a></p></div>
  </aside>
</div></section>
<section class="section section--cream"><div class="wrap">
  <div class="section-head reveal" style="justify-content:center;text-align:center"><div><p class="eyebrow">Questions</p><h2>{esc(g["tag"])} FAQs</h2></div></div>
  {faq_html(g["faq"])}
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">Explore</p><h2>Related <em>gardens</em></h2></div><a class="btn btn--dark" href="/gardens.html">All gardens {ICON["arrow"]}</a></div>
  {garden_cards(g["related"], related=True)}
</div></section>
{cta()}
"""
    schema = [
        breadcrumbs(crumbs),
        {"@type": "Service", "name": strip_tags(g["h1"]), "serviceType": g["kicker"], "provider": {"@id": ORIGIN + "/#business"},
         "areaServed": ORG["areaServed"], "description": g["description"], "url": ORIGIN + path},
        faq_schema(g["faq"]),
    ]
    return path, page(path, g["title"], g["description"], body, "/gardens.html", schema, og_image=g["hero"])


def build_gardens_index():
    rows = []
    for i, g in enumerate(GARDENS):
        rev = " split--rev" if i % 2 else ""
        rows.append(f"""<div class="split{rev}" style="margin-bottom:clamp(70px,10vw,130px)">
  <a class="reveal-img" href="/gardens/{g['slug']}.html" style="display:block;aspect-ratio:5/4;overflow:hidden">{pic(g["hero"], ALT[g["hero"]], extra=' style="width:100%;height:100%;object-fit:cover"')}</a>
  <div class="reveal" data-delay="1"><p class="eyebrow">0{i + 1} &middot; {esc(g["tag"])}</p><h2>{esc(g["nav"])}</h2><p class="lead">{esc(g["card"])}</p><p>{esc(g["description"])}</p>
  <div class="palette" style="margin:20px 0 30px">{"".join(f'<span style="background:var(--cream)">{esc(p)}</span>' for p in g["palette"][:4])}</div>
  <a class="btn btn--dark" href="/gardens/{g['slug']}.html">Read more {ICON["arrow"]}</a></div>
</div>""")
    crumbs = [("Home", "/"), ("Gardens", "/gardens.html")]
    body = f"""
{photo_hero("lush-glasshouse", "Gardens", "Gardens for every <em>kind of space</em>", "Courtyards, town gardens, family gardens and country gardens. Explore the garden types we design and how we approach each one.", crumbs)}
<section class="section"><div class="wrap">{"".join(rows)}</div></section>
{cta()}
"""
    schema = [breadcrumbs(crumbs), {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}/gardens/{g['slug']}.html", "name": g["nav"]} for i, g in enumerate(GARDENS)]}]
    return page("/gardens.html", "Our Gardens: Courtyard, Town, Family & Country | Fraser & Morris",
                "Explore the gardens Fraser & Morris designs: courtyard and town gardens in London, family gardens, lush shade gardens and country gardens in Oxfordshire.",
                body, "/gardens.html", schema, og_image="lush-glasshouse")


def build_about():
    crumbs = [("Home", "/"), ("About", "/about.html")]
    values = [
        ("Plants first", "We are planting designers at heart. Every layout is drawn to give the plants the best possible conditions, and every plant is chosen for its place."),
        ("Right plant, right place", "We design for your soil, aspect and microclimate, so the garden thrives without constant intervention."),
        ("Year-round interest", "A garden should earn its keep in February as well as June. Structure, bark, seedheads and evergreens carry it through winter."),
        ("Gardens for living", "Beautiful, but practical: somewhere to eat, play, work and sit quietly, designed around the way you live."),
    ]
    vals = "".join(f'<div class="area reveal" data-delay="{i}">{ICON["leaf"]}<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(values))
    body = f"""
{photo_hero("meadow-path", "About", "A plant-led <em>garden design</em> studio", "Fraser &amp; Morris designs gardens in which planting comes first: layered, seasonal and right for the place.", crumbs)}
<section class="section"><div class="wrap split">
  <div class="reveal">
    <p class="eyebrow">Our approach</p>
    <h2>Gardens that feel <em>as if they belong</em></h2>
    <p>Fraser &amp; Morris is a garden design and planting studio based in London. We design gardens of every size, from basement courtyards and narrow town gardens to family gardens and country gardens in Oxfordshire, Suffolk and Sussex.</p>
    <p>Our work begins and ends with plants. We spend time understanding a site (its soil, light, wind and views) and the people who will use it, then design a garden that suits both. Layout and materials are there to support the planting, not the other way round.</p>
    <p>We are as happy working on a single border as on a whole garden, and we work alongside architects, builders and landscape contractors to make sure the finished garden is exactly as it was drawn.</p>
    <a class="btn btn--dark" href="/services.html">How we work {ICON["arrow"]}</a>
  </div>
  <div class="stack reveal" data-delay="1">
    <div class="main reveal-img">{pic("hands-trowel", ALT["hands-trowel"])}</div>
    <div class="inset">{pic("allium", ALT["allium"])}</div>
  </div>
</div></section>
<section class="section section--cream"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">What we believe</p><h2>Four principles behind <em>every garden</em></h2></div></div>
  <div class="areas">{vals}</div>
</div></section>
<section class="band">
  <div class="band__media" data-parallax="0.18">{pic("country-topiary", ALT["country-topiary"])}</div>
  <div class="wrap reveal"><blockquote>&ldquo;Plant for February first. If the garden looks good then, it will look <em>wonderful</em> in June.&rdquo;</blockquote><cite>A Fraser &amp; Morris rule of thumb</cite></div>
</section>
<section class="section"><div class="wrap split split--rev">
  <div class="reveal">
    <p class="eyebrow">Writing &amp; plants</p>
    <h2>Curious about <em>plants</em></h2>
    <p>Good planting design comes from looking: at gardens, at wild plant communities, at nurseries and at the way plants behave in different soils and seasons. We visit gardens and nurseries throughout the year and bring what we learn back into our planting plans.</p>
    <p>Dahlias, crab apples, alliums, grasses and woodland plants appear again and again in our work, because they are generous, long-lasting and beautiful as they fade.</p>
  </div>
  <div class="reveal-img" style="aspect-ratio:4/3;overflow:hidden">{pic("dahlias", ALT["dahlias"], extra=' style="width:100%;height:100%;object-fit:cover"')}</div>
</div></section>
{cta()}
"""
    return page("/about.html", "About Fraser & Morris | Plant-Led Garden Designers in London",
                "About Fraser & Morris, a London garden design and planting studio creating plant-led town, courtyard, family and country gardens.",
                body, "/about.html", [breadcrumbs(crumbs)], og_image="meadow-path")


def build_services():
    crumbs = [("Home", "/"), ("Services", "/services.html")]
    detail = [
        ("pencil", "Full garden design", "hero-garden-path",
         "Our complete design service takes a garden from first visit to finished planting plan.",
         ["Consultation visit and design brief", "Measured topographical survey", "Concept layouts and mood boards", "Final scaled masterplan", "Construction and setting-out drawings", "Detailed planting plan and plant schedule"]),
        ("sprout", "Planting design", "dahlias",
         "For new borders, a tired garden or a layout built by someone else. Planting is our speciality.",
         ["Planting plans for borders or whole gardens", "Seasonal and year-round schemes", "Plants sourced from specialist nurseries", "Plants set out and placed by us on planting day", "Bulb and meadow planting", "Container and roof-terrace planting"]),
        ("spade", "Build management", "hands-planting",
         "We work with a small group of trusted landscape contractors and oversee the build.",
         ["Tender documents and contractor selection", "Regular site visits during construction", "Coordination with architects and builders", "Quality checks on materials and finishes", "Lighting and irrigation coordination", "Final snagging"]),
        ("calendar", "Aftercare &amp; consultancy", "fern-detail",
         "Gardens change. We help them settle in and keep evolving.",
         ["Seasonal aftercare visits", "Editing and replanting borders", "Garden consultations and advice visits", "Maintenance schedules for gardeners", "Planting for events and seasons", "Advice on existing trees and plants"]),
    ]
    blocks = []
    for i, (ic, t, im, intro, items) in enumerate(detail):
        rev = " split--rev" if i % 2 else ""
        lis = "".join(f"<li>{x}</li>" for x in items)
        blocks.append(f"""<div class="split{rev}" style="margin-bottom:clamp(70px,10vw,120px)">
  <div class="reveal-img" style="aspect-ratio:5/4;overflow:hidden">{pic(im, ALT[im], extra=' style="width:100%;height:100%;object-fit:cover"')}</div>
  <div class="reveal" data-delay="1"><p class="eyebrow">Service 0{i + 1}</p><h2>{t}</h2><p class="lead">{intro}</p><ul class="checks">{lis}</ul></div>
</div>""")
    process = '<div class="process"><span class="line"></span>' + "".join(
        f'<div class="step reveal" data-delay="{min(i, 3)}"><div class="dot">{i + 1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS)
    ) + "</div>"
    faqs = HOME_FAQ[1:]
    body = f"""
{photo_hero("hands-planting", "Services", "Garden design services, <em>survey to planting</em>", "Full garden design, planting plans, build management and aftercare for gardens in London and the countryside.", crumbs)}
<section class="section"><div class="wrap">{"".join(blocks)}</div></section>
<section class="section section--cream"><div class="wrap">
  <div class="section-head reveal"><div><p class="eyebrow">The process</p><h2>Five steps to <em>a new garden</em></h2></div><p>Every project is different, but most follow this path from first conversation to planting day.</p></div>
  {process}
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head reveal" style="justify-content:center;text-align:center"><div><p class="eyebrow">Questions</p><h2>About our services</h2></div></div>
  {faq_html(faqs)}
</div></section>
{cta()}
"""
    schema = [breadcrumbs(crumbs), faq_schema(faqs)] + [
        {"@type": "Service", "name": strip_tags(t).replace("&amp;", "&"), "provider": {"@id": ORIGIN + "/#business"}, "areaServed": ORG["areaServed"], "description": intro}
        for _ic, t, _im, intro, _it in detail
    ]
    return page("/services.html", "Garden Design Services London | Planting Plans | Fraser & Morris",
                "Garden design services from Fraser & Morris: full garden design, planting plans, build management and aftercare across London, Oxfordshire, Suffolk and Sussex.",
                body, "/services.html", schema, og_image="hands-planting")


def build_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact.html")]
    options = "".join(f"<option>{esc(g['nav'])}</option>" for g in GARDENS)
    body = f"""
<section class="plain-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Contact</span></nav>
  <p class="eyebrow">Contact</p>
  <h1>Let's talk about <em>your garden</em></h1>
  <p class="lead">Whether it is a small courtyard or a country garden, the first step is a conversation. Send us a few details and we will be in touch to arrange a visit.</p>
</div></section>
<section class="section" style="padding-top:70px"><div class="wrap contact-grid">
  <div class="reveal">
    <h2>Get in touch</h2>
    <p>We design gardens across London and in Oxfordshire, the Cotswolds, Suffolk and Sussex. Tell us where your garden is, roughly how big it is, and what you would like to change.</p>
    <div class="contact-info">
      <div>{ICON["mail"]}<p><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div>{ICON["pin"]}<p><strong>Studio</strong>London. Visits by appointment across London and the Home Counties.</p></div>
      <div>{ICON["clock"]}<p><strong>Response</strong>We reply to every enquiry, usually within two working days.</p></div>
    </div>
    <div class="reveal-img" style="margin-top:40px;aspect-ratio:16/10;overflow:hidden">{pic("courtyard-pots", ALT["courtyard-pots"], extra=' style="width:100%;height:100%;object-fit:cover"')}</div>
  </div>
  <form class="form reveal" data-delay="1" id="form" action="/contact.php" method="post">
    <div class="form-status" role="status" aria-live="polite"></div>
    <div class="row">
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required maxlength="120"></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
    </div>
    <div class="row">
      <div class="field"><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40"></div>
      <div class="field"><label for="f-loc">Garden location</label><input id="f-loc" name="location" placeholder="e.g. Camberwell, London" maxlength="120"></div>
    </div>
    <div class="field"><label for="f-type">Type of garden</label><select id="f-type" name="type"><option value="">Choose one</option>{options}<option>Something else</option></select></div>
    <div class="field"><label for="f-msg">Tell us about your garden</label><textarea id="f-msg" name="message" required maxlength="5000" placeholder="Size, aspect, what you love and what you would like to change..."></textarea></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
    <button class="btn" type="submit">Send message {ICON["arrow"]}</button>
    <p style="font-size:.85rem;color:var(--muted);margin:18px 0 0">We only use your details to reply to your enquiry. See our <a href="/privacy.html">privacy notice</a>.</p>
  </form>
</div></section>
"""
    schema = [breadcrumbs(crumbs), {"@type": "ContactPage", "url": ORIGIN + "/contact.html", "about": {"@id": ORIGIN + "/#business"}}]
    return page("/contact.html", "Contact Fraser & Morris | Garden Designers in London",
                "Contact Fraser & Morris to discuss garden design in London, Oxfordshire, Suffolk or Sussex. Email info@fraserandmorris.com or send us a message.",
                body, "/contact.html", schema, light=True, og_image="courtyard-pots")


def build_privacy():
    body = f"""
<section class="plain-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span aria-current="page">Privacy</span></nav>
  <h1>Privacy notice</h1>
</div></section>
<section class="section" style="padding-top:60px"><div class="wrap prose" style="max-width:780px">
<p>This notice explains how {NAME} uses personal information collected through this website.</p>
<h2>What we collect</h2>
<p>When you send an enquiry we receive the details you enter in the form: your name, email address, phone number if given, the location of your garden and your message. We do not use advertising or tracking cookies.</p>
<h2>How we use it</h2>
<p>We use these details only to reply to your enquiry and, if you go ahead, to manage your project. We do not sell or share your information with third parties for marketing.</p>
<h2>How long we keep it</h2>
<p>Enquiries that do not lead to a project are deleted within twelve months. Project records are kept for as long as needed for our legal and accounting obligations.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete the personal information we hold about you by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p><small>Last updated {TODAY}.</small></p>
</div></section>
"""
    return page("/privacy.html", "Privacy Notice | Fraser & Morris", "How Fraser & Morris uses the personal information you send through this website.",
                body, "", [breadcrumbs([("Home", "/"), ("Privacy", "/privacy.html")])], light=True)


def build_404():
    body = f"""
<section class="plain-hero" style="min-height:70vh"><div class="wrap">
  <p class="eyebrow">Page not found</p>
  <h1>This path is <em>overgrown</em></h1>
  <p class="lead">The page you were looking for has moved or no longer exists. Try one of these instead.</p>
  <div class="hero__actions"><a class="btn" href="/">Back to home {ICON["arrow"]}</a><a class="btn btn--dark" href="/gardens.html">Explore our gardens</a></div>
</div></section>
"""
    return page("/404.html", "Page Not Found | Fraser & Morris", "The page you were looking for could not be found.", body, "", light=True, robots="noindex,follow")


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(content)


def main():
    load_sizes()
    pages = {"home.html": build_home(), "about.html": build_about(), "services.html": build_services(),
             "contact.html": build_contact(), "gardens.html": build_gardens_index(), "privacy.html": build_privacy(), "404.html": build_404()}
    for g in GARDENS:
        path, content = build_garden(g)
        pages[path.lstrip("/")] = content
    for rel, content in pages.items():
        write(rel, content)

    urls = ["/", "/about.html", "/services.html", "/gardens.html"] + [f"/gardens/{g['slug']}.html" for g in GARDENS] + ["/contact.html", "/privacy.html"]
    prio = {"/": "1.0", "/gardens.html": "0.9", "/services.html": "0.9"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, '0.7')}</priority></url>")
    sm.append("</urlset>\n")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    print(f"built {len(pages)} pages")


if __name__ == "__main__":
    main()
