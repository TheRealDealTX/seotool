#!/usr/bin/env python3
"""Static site generator for shopvipgifts.com.

Writes everything into ./public. Run:  python3 build.py && python3 validate.py
Standard library only.
"""

import html
import json
import os
import re
import shutil

from content.site import SITE, NAV, FOOTER_COLS, TODAY
from content.guides import GUIDES
from content.blog import POSTS
from content import pages as P

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = SITE["origin"]
FONTS = ("https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800"
         "&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap")

GA_ID = "G-PTQD14707B"
GTAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>"""

ICONS = {
    "chev": '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7M7.5 8a2.5 2.5 0 0 1 0-5C10 3 12 8 12 8s2-5 4.5-5a2.5 2.5 0 0 1 0 5"/></g></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 22l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
    "pen": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "box": '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/></g></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></g></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
}

LOGO_SVG = ('<svg viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#f3dca6"/><stop offset=".55" stop-color="#d6b16a"/><stop offset="1" stop-color="#a8833f"/></linearGradient></defs>'
            '<rect x="6" y="15" width="28" height="20" rx="3" fill="none" stroke="url(#lg)" stroke-width="2"/>'
            '<rect x="4" y="11" width="32" height="6" rx="2" fill="url(#lg)"/>'
            '<path d="M20 11v24" stroke="#0e0b16" stroke-width="2.4"/><path d="M20 11v24" stroke="url(#lg)" stroke-width="1.2"/>'
            '<path d="M20 11c-3-6-10-6-9-2 .6 2.4 6 2 9 2zM20 11c3-6 10-6 9-2-.6 2.4-6 2-9 2z" fill="none" stroke="url(#lg)" stroke-width="1.8"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


_DIMS = {}


def dims(name):
    """Real pixel size of /assets/img/<name>.webp (read from the WebP header)."""
    if name not in _DIMS:
        with open(os.path.join(OUT, "assets", "img", name + ".webp"), "rb") as f:
            head = f.read(30)
        if head[12:16] == b"VP8 ":
            w = int.from_bytes(head[26:28], "little") & 0x3FFF
            h = int.from_bytes(head[28:30], "little") & 0x3FFF
        elif head[12:16] == b"VP8L":
            b = int.from_bytes(head[21:25], "little")
            w, h = (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        else:  # VP8X
            w = int.from_bytes(head[24:27], "little") + 1
            h = int.from_bytes(head[27:30], "little") + 1
        _DIMS[name] = (w, h)
    return _DIMS[name]


def img(name, alt, w=None, h=None, cls="", lazy=True, extra=""):
    w, h = dims(name)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="/assets/img/{name}.webp" alt="{esc(alt)}" width="{w}" height="{h}"{c}{l}{extra}>'


# ---------------------------------------------------------------- layout

def nav_html(current):
    items = []
    for label, href, children in NAV:
        if children:
            cur_attr = ' aria-current="page"'
            sub = "".join(
                f'<li><a href="{h}"{cur_attr if h == current else ""}>{esc(l)}</a></li>' for l, h in children)
            items.append(
                f'<li class="has-sub"><button type="button" class="sub-toggle" aria-expanded="false">{esc(label)} {ICONS["chev"]}</button>'
                f'<ul class="sub">{sub}</ul></li>')
        else:
            cur = ' aria-current="page"' if href == current else ""
            items.append(f'<li><a href="{href}"{cur}>{esc(label)}</a></li>')
    items.append('<li class="nav-cta"><a class="btn" href="/gift-finder/">Find a gift ✦</a></li>')
    return "".join(items)


def header(current):
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="/" aria-label="{esc(SITE["name"])} home">{LOGO_SVG}<span class="logo-text">Shop <em>VIP</em> Gifts<small>Curated luxury gifting</small></span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main"><ul>{nav_html(current)}</ul></nav>
    <button class="burger" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer():
    cols = ""
    for title, links in FOOTER_COLS:
        lis = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in links)
        cols += f'<div><h4>{esc(title)}</h4><ul>{lis}</ul></div>'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-about">
        <a class="logo" href="/">{LOGO_SVG}<span class="logo-text">Shop <em>VIP</em> Gifts</span></a>
        <p>Curated VIP gift ideas, luxury gift guides and free planning tools for the people who matter most — partners, parents, clients and the friend who has everything.</p>
        <p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
      </div>
      {cols}
    </div>
    <div class="foot-bottom">
      <span>© <span data-year>2026</span> {esc(SITE["name"])}. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/sitemap/">Sitemap</a></span>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">↑</button>'''


def org_schema():
    return {
        "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE["name"], "url": ORIGIN + "/",
        "email": SITE["email"],
        "logo": {"@type": "ImageObject", "url": ORIGIN + "/web-app-manifest-512x512.png", "width": 512, "height": 512},
        "contactPoint": {"@type": "ContactPoint", "email": SITE["email"], "contactType": "customer support"},
    }


def website_schema():
    return {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": SITE["name"], "url": ORIGIN + "/",
            "publisher": {"@id": ORIGIN + "/#org"}}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(trail)]}


def crumbs_html(trail):
    parts = []
    for i, (n, u) in enumerate(trail):
        parts.append(esc(n) if i == len(trail) - 1 else f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def layout(path, title, desc, body, schema=None, scripts=(), og_image="hero", og_type="website",
           extra_head="", body_class="", robots="index,follow", canonical=None, hero_img=None):
    url = ORIGIN + (canonical or path)
    ogw, ogh = dims(og_image)
    hero_img = hero_img or og_image
    graph = [org_schema(), website_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    ld = ld.replace("</", "<\\/")
    js = "".join(f'<script src="/assets/js/{s}.js?v={SITE["ver"]}" defer></script>' for s in ("site",) + tuple(scripts))
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GTAG}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(SITE["name"])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta property="og:image:width" content="{ogw}">
<meta property="og:image:height" content="{ogh}">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta name="theme-color" content="#0e0b16">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="VIP Gifts">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Shop VIP Gifts Journal" href="{ORIGIN}/blog/feed.xml">
<link rel="preload" as="image" href="/assets/img/{hero_img}.webp" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css?v={SITE["ver"]}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body{f' class="{body_class}"' if body_class else ""}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{js}
</body>
</html>
'''


def page_hero(trail, eyebrow, h1, lead, image, meta=""):
    return f'''<section class="page-hero">
  <div class="hero-bg">{img(image, "", lazy=False)}</div>
  <div class="wrap">
    {crumbs_html(trail)}
    <span class="eyebrow">{esc(eyebrow)}</span>
    <h1>{h1}</h1>
    {f'<p class="lead">{lead}</p>' if lead else ""}
    {meta}
  </div>
</section>'''


def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in faqs) + "</div>"


def faq_schema(faqs):
    import re
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in faqs]}


def post_card(p):
    return f'''<a class="post-card reveal" href="/blog/{p["slug"]}/">
  <div class="pc-img">{img(p["img"], p["img_alt"], 800, 500)}</div>
  <div class="pc-body"><span class="tag">{esc(p["cat"])}</span><h3>{esc(p["h1"])}</h3><p>{esc(p["excerpt"])}</p><span class="more">Read the guide →</span></div>
</a>'''


def guide_card(g, wide=False):
    return f'''<a class="cat-card reveal{' wide' if wide else ''}" href="/{g["slug"]}/" data-tilt>
  {img(g["card_img"], g["card_alt"], 800, 600)}
  <span class="arrow">{ICONS["arrow"]}</span>
  <div class="cc-body"><span class="tag">{esc(g["tagline"])}</span><h3>{esc(g["menu"])}</h3><p>{esc(g["card_text"])}</p></div>
</a>'''


TOOLS = [
    ("/gift-finder/", "Gift Finder Quiz", "Answer four quick questions and get six matched VIP gift ideas.", "gift-ribbon"),
    ("/gift-budget-planner/", "Gift Budget Planner", "Plan your whole list, auto-split a budget and see exactly where it goes.", "gifts-stack"),
    ("/gift-message-generator/", "Gift Message Generator", "Never stare at a blank card again — heartfelt, witty or formal in one tap.", "note-pen"),
    ("/anniversary-gifts-by-year/", "Anniversary Gifts by Year", "Traditional, modern, gemstone and flower for every milestone year.", "anniversary"),
]


def tool_cards(exclude=None):
    out = ""
    for href, name, text, im in TOOLS:
        if href == exclude:
            continue
        out += f'''<a class="tool-card reveal" href="{href}">{img(im, name, 400, 400)}<div><h3>{esc(name)}</h3><p>{esc(text)}</p><span class="go">Open the tool →</span></div></a>'''
    return out


# ---------------------------------------------------------------- pages

def build_home():
    guides = GUIDES
    latest = POSTS[:3]
    marquee_items = ["Birthdays", "Anniversaries", "Client appreciation", "Weddings", "Holidays", "Promotions",
                     "Retirement", "Mother's Day", "Father's Day", "Thank-yous", "Housewarmings", "Just because"]
    mq = "".join(f"<span>{m}</span>" for m in marquee_items) * 2
    body = f'''<section class="hero">
  <div class="hero-bg">{img("hero", "Luxury wrapped gifts with ribbon and dried flowers", 1200, 800, lazy=False)}</div>
  <canvas id="sparkles" aria-hidden="true"></canvas>
  <div class="orb orb-1"></div><div class="orb orb-2"></div>
  <div class="wrap hero-grid">
    <div class="reveal in">
      <span class="eyebrow">The art of VIP gifting</span>
      <h1>VIP gifts for the people who <span class="shimmer">matter most</span></h1>
      <p class="hero-lead">Shop VIP Gifts is your concierge for unforgettable presents — curated luxury gift guides, VIP gift ideas for every budget and free tools that take the guesswork out of giving.</p>
      <div class="hero-actions">
        <a class="btn btn-gold" href="/gift-finder/">Take the Gift Finder quiz</a>
        <a class="btn btn-ghost" href="/gift-guides/">Browse gift guides</a>
      </div>
      <div class="hero-trust">
        <div><strong data-count="{len(guides)}">{len(guides)}</strong>curated gift guides</div>
        <div><strong data-count="150" data-suffix="+">150+</strong>VIP gift ideas</div>
        <div><strong data-count="4">4</strong>free gifting tools</div>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="hv-card hv-1">{img("gift-pink", "", 800, 550)}</div>
      <div class="hv-card hv-2">{img("pearls", "", 600, 400)}</div>
      <div class="hv-card hv-3">{img("wine-toast", "", 500, 330)}</div>
      <div class="hv-badge"><span class="dot">✦</span><span><b>Gift matched</b>98% perfect for Mom</span></div>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Gift guides</span>
      <h2>Curated collections for every kind of VIP</h2>
      <p>Each guide is hand-built around one person or occasion, with ideas from thoughtful-under-$50 to once-in-a-lifetime splurges.</p>
    </div>
    <div class="cat-grid">
      {guide_card(guides[0], wide=True)}
      {guide_card(guides[1])}
      {"".join(guide_card(g) for g in guides[2:])}
      <a class="cat-card reveal wide" href="/gift-finder/" data-tilt>
        {img("gift-pattern", "Black gift boxes tied with gold ribbon", 800, 600)}
        <span class="arrow">{ICONS["arrow"]}</span>
        <div class="cc-body"><span class="tag">Not sure yet?</span><h3>Take the 60-second Gift Finder</h3><p>Answer four questions and get six VIP gift ideas ranked for your person, occasion and budget.</p></div>
      </a>
    </div>
  </div>
</section>

<section class="section cream">
  <div class="wrap split">
    <div class="split-media reveal">
      {img("gift-hands", "Person holding a gift wrapped in kraft paper and twine", 1200, 800)}
      {img("gift-ribbon", "Kraft paper gift tied with a pink satin ribbon", 600, 600, cls="float-img")}
    </div>
    <div class="reveal d1">
      <span class="eyebrow">What makes a VIP gift?</span>
      <h2>It isn't the price tag. It's the feeling of being <em>seen</em>.</h2>
      <p>A VIP gift tells someone you paid attention — to the coffee they order, the trip they keep mentioning, the watch they'd never buy for themselves. We call it the VIP formula: <strong>personal, premium, presented beautifully</strong>.</p>
      <ul class="ticks">
        <li><strong>Personal</strong> — chosen for one person, not for "someone like them."</li>
        <li><strong>Premium</strong> — the best version of a thing, even when the thing is small.</li>
        <li><strong>Presented</strong> — wrapping, timing and a handwritten note do half the work.</li>
      </ul>
      <a class="btn btn-dark" href="/blog/vip-gift-ideas-what-makes-a-gift-feel-vip/">Read the VIP gifting guide</a>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">How we curate</span>
      <h2>Gifting, done like a concierge would</h2>
    </div>
    <div class="tiles">
      <div class="tile reveal"><div class="ico">{ICONS["heart"]}</div><h3>Person first</h3><p>We start with who they are — interests, routines, style — and only then look at products.</p></div>
      <div class="tile reveal d1"><div class="ico">{ICONS["star"]}</div><h3>Quality filter</h3><p>Materials, craftsmanship and longevity matter more to us than logos and hype.</p></div>
      <div class="tile reveal d2"><div class="ico">{ICONS["box"]}</div><h3>Presentation</h3><p>Every guide includes wrapping, delivery and note-writing tips so it lands like a VIP moment.</p></div>
      <div class="tile reveal d3"><div class="ico">{ICONS["clock"]}</div><h3>Perfect timing</h3><p>Countdowns, timelines and reminders so you're never stuck with a last-minute gift card.</p></div>
    </div>
  </div>
</section>

<section class="section white">
  <div class="wrap">
    <div class="countdown reveal" data-countdown>
      <div>
        <span class="eyebrow">Gift-giving countdown</span>
        <h2><span data-cd-name>Christmas</span> is coming</h2>
        <p data-cd-date></p>
        <div class="cd-tabs" role="group" aria-label="Choose an occasion"></div>
      </div>
      <div class="cd-units" aria-live="off">
        <div class="cd-unit"><b data-d>0</b><small>Days</small></div>
        <div class="cd-unit"><b data-h>00</b><small>Hours</small></div>
        <div class="cd-unit"><b data-m>00</b><small>Mins</small></div>
        <div class="cd-unit"><b data-s>00</b><small>Secs</small></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Free gifting tools</span>
      <h2>Interactive tools that make giving effortless</h2>
      <p>Find the right present, plan your list, write the card and decode anniversary traditions — all free, no sign-up.</p>
    </div>
    <div class="tool-grid">{tool_cards()}</div>
  </div>
</section>

<section class="section cream">
  <div class="wrap split rev">
    <div class="split-media reveal">
      {img("handshake", "Two professionals shaking hands across a desk", 1200, 800)}
      {img("wine-toast", "Friends raising glasses of red wine in a toast", 600, 600, cls="float-img")}
    </div>
    <div class="reveal d1">
      <span class="eyebrow">For business</span>
      <h2>Corporate & client VIP gifts that strengthen relationships</h2>
      <p>The right client gift is remembered long after the invoice is paid. Our corporate gifting guide covers budgets per tier, etiquette and compliance limits, branding that doesn't feel like marketing, and timing that stands out from the December pile.</p>
      <ul class="ticks">
        <li>Tiered budgets for top clients, partners and teams</li>
        <li>Gift-policy friendly ideas under common $25–$100 limits</li>
        <li>Holiday, thank-you and milestone gifting calendars</li>
      </ul>
      <a class="btn btn-dark" href="/corporate-gifts/">Explore corporate gifts</a>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><b data-count="{len(GUIDES)}">{len(GUIDES)}</b><span>Hand-built gift guides</span></div>
      <div class="stat reveal d1"><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>In-depth gifting articles</span></div>
      <div class="stat reveal d2"><b data-count="24">24</b><span>Anniversary years decoded</span></div>
      <div class="stat reveal d3"><b data-count="63">63</b><span>Ready-to-use card messages</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="eyebrow">Gifting journal</span>
      <h2>Ideas, etiquette & inspiration</h2>
    </div>
    <div class="post-grid">{"".join(post_card(p) for p in latest)}</div>
    <p style="text-align:center;margin-top:44px"><a class="btn btn-line" href="/blog/">See all articles</a></p>
  </div>
</section>

<section class="section white">
  <div class="wrap">
    <div class="sec-head center reveal"><span class="eyebrow">House rules</span><h2>Three VIP gifting rules we live by</h2></div>
    <div class="quote-grid">
      <div class="quote reveal"><p>Upgrade something they use every day. A beautiful version of an ordinary object gets noticed every single morning.</p><cite>— Rule 1: Daily luxury</cite></div>
      <div class="quote reveal d1"><p>Spend a third of your effort on presentation. Wrapping, timing and a handwritten note do half the emotional work.</p><cite>— Rule 2: The reveal matters</cite></div>
      <div class="quote reveal d2"><p>Listen for "someday". "I'd love to try that someday" is the best gift brief you'll ever get.</p><cite>— Rule 3: Pay attention</cite></div>
    </div>
  </div>
</section>

<section class="section-sm">
  <div class="wrap">
    <div class="cta-band reveal">
      {img("gift-pattern", "", 1200, 1200)}
      <span class="eyebrow">The VIP list</span>
      <h2>Get our best gift ideas before every big occasion</h2>
      <p>One thoughtful email ahead of each major gifting date — curated picks, deadlines and wrapping tips. No spam, ever.</p>
      <form class="inline-form" action="/contact.php" method="post" data-ajax data-success="You're on the VIP list — welcome!">
        <input type="hidden" name="form" value="newsletter">
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <label class="sr-only" for="nl-email">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="Your email address" required>
        <button class="btn btn-gold" type="submit">Join the list</button>
      </form>
      <p class="form-note" aria-live="polite"></p>
    </div>
  </div>
</section>'''
    faqs = P.HOME_FAQS
    body += f'''
<section class="section">
  <div class="narrow">
    <div class="sec-head center reveal"><span class="eyebrow">FAQ</span><h2>VIP gift questions, answered</h2></div>
    {faq_html(faqs)}
  </div>
</section>'''
    schema = [faq_schema(faqs), {"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/",
                                  "name": P.HOME_TITLE, "isPartOf": {"@id": ORIGIN + "/#website"}}]
    return layout("/", P.HOME_TITLE, P.HOME_DESC, body, schema=schema, canonical="/", og_image="hero")


def build_guides_index():
    trail = [("Home", "/"), ("Gift Guides", "/gift-guides/")]
    cards = "".join(guide_card(g) for g in GUIDES)
    body = page_hero(trail, "Gift guides", "Luxury gift guides for every VIP in your life",
                     "Browse our curated collections by person and occasion. Every guide includes price ranges, why each idea feels special, and how to present it.",
                     "gifts-stack")
    body += f'''<section class="section"><div class="wrap"><div class="cat-grid">{cards}</div></div></section>
<section class="section cream"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Not sure where to start?</span><h2>Let the tools do the thinking</h2></div><div class="tool-grid">{tool_cards()}</div></div></section>'''
    schema = [crumbs_schema(trail), {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": f'{ORIGIN}/{g["slug"]}/', "name": g["menu"]} for i, g in enumerate(GUIDES)]}]
    return layout("/gift-guides/", "Luxury Gift Guides by Person & Occasion",
                  "Curated luxury gift guides for him, her, clients, couples and more. VIP gift ideas with price ranges, presentation tips and expert advice.",
                  body, schema=schema, og_image="gifts-stack")


def build_guide(g):
    trail = [("Home", "/"), ("Gift Guides", "/gift-guides/"), (g["menu"], f'/{g["slug"]}/')]
    path = f'/{g["slug"]}/'
    ideas = ""
    for i, it in enumerate(g["ideas"]):
        name, im, price, text, vip = it
        ideas += f'''<article class="idea reveal{' d1' if i % 3 == 1 else ' d2' if i % 3 == 2 else ''}">
  <div class="i-img">{img(im, name, 600, 450)}<span class="price">{esc(price)}</span></div>
  <div class="i-body"><h3>{esc(name)}</h3><p>{text}</p><p class="vip"><b>VIP touch:</b> {vip}</p></div>
</article>'''
    more = ""
    if g.get("more"):
        rows = "".join(f'<div class="idea-row reveal"><div><h3>{esc(n)}</h3><p>{t}</p></div><span class="pr">{esc(p)}</span></div>' for n, p, t in g["more"])
        more = f'''<section class="section cream"><div class="narrow"><div class="sec-head reveal"><span class="eyebrow">More ideas</span><h2>{esc(g["more_title"])}</h2></div><div class="ideas-text">{rows}</div></div></section>'''
    others = [x for x in GUIDES if x["slug"] != g["slug"]][:3]
    related_posts = [p for p in POSTS if p["slug"] in g.get("posts", [])][:3] or POSTS[:3]
    body = page_hero(trail, g["eyebrow"], g["h1"], g["lead"], g["hero_img"])
    body += f'''<section class="section-sm"><div class="narrow prose reveal">{g["intro"]}</div></section>
<section class="section-sm" style="padding-top:0"><div class="wrap"><div class="idea-grid">{ideas}</div></div></section>
{more}
<section class="section"><div class="narrow prose reveal">{g["body"]}</div></section>
<section class="section-sm cream"><div class="wrap"><div class="split">
  <div class="reveal"><span class="eyebrow">Still deciding?</span><h2>Get six matched ideas in under a minute</h2><p>Tell our Gift Finder who it's for, the occasion, your budget and their personality — it ranks ideas from our guides for you.</p><a class="btn btn-dark" href="/gift-finder/">Try the Gift Finder</a></div>
  <div class="reveal d1" style="text-align:center"><div class="giftbox" role="img" aria-label="Animated gift box"><div class="burst"></div><div class="lid"><div class="bow"></div></div><div class="box"></div></div><p style="color:var(--muted);font-size:.9rem">Tap the box ✦</p></div>
</div></div></section>
<section class="section"><div class="narrow"><div class="sec-head center reveal"><span class="eyebrow">FAQ</span><h2>{esc(g["menu"])}: common questions</h2></div>{faq_html(g["faqs"])}</div></section>
<section class="section white"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Keep reading</span><h2>Related articles</h2></div><div class="post-grid">{"".join(post_card(p) for p in related_posts)}</div></div></section>
<section class="section"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">More guides</span><h2>Other VIPs on your list</h2></div><div class="cat-grid">{"".join(guide_card(x) for x in others)}</div></div></section>'''
    schema = [crumbs_schema(trail), faq_schema(g["faqs"]),
              {"@type": "ItemList", "name": g["h1_plain"], "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "name": it[0]} for i, it in enumerate(g["ideas"])]}]
    return layout(path, g["title"], g["desc"], body, schema=schema, og_image=g["hero_img"])


def build_blog_index():
    trail = [("Home", "/"), ("Blog", "/blog/")]
    body = page_hero(trail, "The gifting journal", "VIP gifting blog: ideas, etiquette & inspiration",
                     "Practical, in-depth guides to choosing, presenting and timing gifts that feel truly special.", "gift-pink")
    body += f'''<section class="section"><div class="wrap"><div class="post-grid">{"".join(post_card(p) for p in POSTS)}</div></div></section>'''
    schema = [crumbs_schema(trail), {"@type": "Blog", "name": "Shop VIP Gifts Journal", "url": ORIGIN + "/blog/",
                                     "blogPost": [{"@type": "BlogPosting", "headline": p["h1"], "url": f'{ORIGIN}/blog/{p["slug"]}/'} for p in POSTS]}]
    return layout("/blog/", "Gifting Blog: VIP Gift Ideas & Etiquette",
                  "Expert articles on VIP gift ideas, corporate gift etiquette, luxury wrapping, gift baskets, card messages and holiday gift planning.",
                  body, schema=schema, og_image="gift-pink")


def build_post(p):
    path = f'/blog/{p["slug"]}/'
    trail = [("Home", "/"), ("Blog", "/blog/"), (p["h1"], path)]
    words = len(p["body"].split())
    mins = max(3, round(words / 230))
    meta = f'<div class="post-meta"><span>{esc(p["cat"])}</span><span>{mins} min read</span><span>Updated {p["date"]}</span></div>'
    toc = ""
    import re
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])
    if len(heads) >= 3:
        toc = '<div class="toc"><b>In this guide</b><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + "</ol></div>"
    related = [x for x in POSTS if x["slug"] != p["slug"]][:3]
    side_links = "".join(f'<li><a href="/{g["slug"]}/">{esc(g["menu"])}</a></li>' for g in GUIDES)
    tool = next((t for t in TOOLS if t[0] == p.get("tool")), TOOLS[0])
    body = page_hero(trail, p["cat"], esc(p["h1"]), esc(p["excerpt"]), p["img"], meta)
    body += f'''<div class="read-progress" aria-hidden="true"></div>
<section class="section-sm"><div class="wrap article-layout">
  <article class="prose">{toc}{p["body"]}
    {('<h2 id="faq">Frequently asked questions</h2>' + faq_html(p["faqs"])) if p.get("faqs") else ""}
  </article>
  <aside class="sidebar">
    <div class="side-promo"><span class="eyebrow">Free tool</span><h3>{esc(tool[1])}</h3><p>{esc(tool[2])}</p><a class="btn btn-gold btn-sm" href="{tool[0]}">Open it</a></div>
    <div class="side-box"><h3>Gift guides</h3><ul>{side_links}</ul></div>
  </aside>
</div></section>
<section class="section white"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">Keep reading</span><h2>More from the journal</h2></div><div class="post-grid">{"".join(post_card(x) for x in related)}</div></div></section>'''
    schema = [crumbs_schema(trail), {
        "@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "image": f'{ORIGIN}/assets/img/{p["img"]}.webp',
        "datePublished": p["date"], "dateModified": p["date"], "mainEntityOfPage": ORIGIN + path,
        "author": {"@type": "Organization", "name": SITE["name"], "url": ORIGIN + "/"}, "publisher": {"@id": ORIGIN + "/#org"}}]
    if p.get("faqs"):
        schema.append(faq_schema(p["faqs"]))
    head = (f'<meta property="article:published_time" content="{p["date"]}">\n'
            f'<meta property="article:modified_time" content="{p["date"]}">\n'
            f'<meta property="article:section" content="{esc(p["cat"])}">\n')
    return layout(path, p["title"], p["desc"], body, schema=schema, og_image=p["img"], og_type="article", extra_head=head)


def tool_page(path, name, title, desc, eyebrow, h1, lead, image, tool_html, content_html, faqs):
    trail = [("Home", "/"), ("Tools", "/tools/"), (name, path)]
    body = page_hero(trail, eyebrow, h1, lead, image)
    body += f'''<section class="section-sm" style="padding-top:0"><div class="wrap">{tool_html}</div></section>
<section class="section"><div class="narrow prose reveal">{content_html}</div></section>
<section class="section-sm cream"><div class="narrow"><div class="sec-head center reveal"><span class="eyebrow">FAQ</span><h2>Questions about the {esc(name.lower())}</h2></div>{faq_html(faqs)}</div></section>
<section class="section"><div class="wrap"><div class="sec-head reveal"><span class="eyebrow">More free tools</span><h2>Keep planning</h2></div><div class="tool-grid">{tool_cards(exclude=path)}</div></div></section>'''
    schema = [crumbs_schema(trail), faq_schema(faqs), {
        "@type": "WebApplication", "name": name, "url": ORIGIN + path, "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    return layout(path, title, desc, body, schema=schema, scripts=("tools",), og_image=image)


def build_tools_index():
    trail = [("Home", "/"), ("Tools", "/tools/")]
    body = page_hero(trail, "Free gifting tools", "Free interactive gift tools",
                     "Quizzes, planners and generators that make choosing, budgeting and writing for gifts quick and enjoyable.", "gifts-stack")
    body += f'<section class="section"><div class="wrap"><div class="tool-grid">{tool_cards()}</div></div></section>'
    return layout("/tools/", "Free Gift Tools: Finder, Planner & More | Shop VIP Gifts",
                  "Free interactive gifting tools: a gift finder quiz, holiday gift budget planner, gift message generator and anniversary gifts by year lookup.",
                  body, schema=[crumbs_schema(trail)], og_image="gifts-stack")


def simple_page(path, crumb, title, desc, eyebrow, h1, lead, image, inner, schema_extra=None, robots="index,follow"):
    trail = [("Home", "/"), (crumb, path)]
    body = page_hero(trail, eyebrow, h1, lead, image) + inner
    return layout(path, title, desc, body, schema=[crumbs_schema(trail)] + (schema_extra or []), og_image=image, robots=robots)


def build_sitemap_page(urls):
    groups = [("Main", [("Home", "/"), ("Gift Guides", "/gift-guides/"), ("Tools", "/tools/"), ("Blog", "/blog/"),
                        ("About", "/about/"), ("Contact", "/contact/")]),
              ("Gift guides", [(g["menu"], f'/{g["slug"]}/') for g in GUIDES]),
              ("Tools", [(t[1], t[0]) for t in TOOLS]),
              ("Blog", [(p["h1"], f'/blog/{p["slug"]}/') for p in POSTS]),
              ("Legal", [("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms/")])]
    inner = '<section class="section"><div class="narrow prose">' + "".join(
        f'<h2>{t}</h2><ul>' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in links) + "</ul>" for t, links in groups) + "</div></section>"
    return simple_page("/sitemap/", "Sitemap", "Sitemap | Shop VIP Gifts", "Browse every page on Shop VIP Gifts: luxury gift guides, free interactive gifting tools, blog articles on gift ideas and etiquette, and site information.",
                       "Sitemap", "Sitemap", "", "gift-pattern", inner)


def build_404():
    body = f'''<section class="nf"><div><span class="eyebrow">Page not found</span><h1 class="shimmer">404</h1>
<p style="color:rgba(255,255,255,.75);max-width:520px;margin:0 auto 30px">This gift seems to have been unwrapped already. Let's find you something even better.</p>
<div class="hero-actions" style="justify-content:center"><a class="btn btn-gold" href="/">Back to home</a><a class="btn btn-ghost" href="/gift-guides/">Browse gift guides</a></div></div></section>'''
    return layout("/404.html", "Page Not Found | Shop VIP Gifts", "The page you were looking for could not be found.", body, robots="noindex,follow")


def build_feed():
    from email.utils import format_datetime
    from datetime import datetime, timezone
    items = ""
    for p in POSTS:
        d = format_datetime(datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc))
        url = f'{ORIGIN}/blog/{p["slug"]}/'
        items += (f"<item><title>{esc(p['h1'])}</title><link>{url}</link><guid>{url}</guid>"
                  f"<pubDate>{d}</pubDate><description>{esc(p['excerpt'])}</description></item>\n")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>\n'
            f'<title>Shop VIP Gifts Journal</title><link>{ORIGIN}/blog/</link>'
            f'<atom:link href="{ORIGIN}/blog/feed.xml" rel="self" type="application/rss+xml"/>'
            f'<description>VIP gift ideas, gifting etiquette and inspiration.</description><language>en-us</language>\n{items}</channel></rss>\n')


# ---------------------------------------------------------------- write

def write(rel, content):
    full = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    # clean generated html (keep assets)
    for name in os.listdir(OUT):
        if name == "assets":
            continue
        p = os.path.join(OUT, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    pages = {}
    pages["/"] = build_home()
    pages["/gift-guides/"] = build_guides_index()
    for g in GUIDES:
        pages[f'/{g["slug"]}/'] = build_guide(g)
    pages["/blog/"] = build_blog_index()
    for p in POSTS:
        pages[f'/blog/{p["slug"]}/'] = build_post(p)
    pages["/tools/"] = build_tools_index()
    for t in P.TOOL_PAGES:
        pages[t["path"]] = tool_page(**t)
    for sp in P.SIMPLE_PAGES:
        pages[sp["path"]] = simple_page(**sp)
    pages["/sitemap/"] = build_sitemap_page(pages)

    for path, content in pages.items():
        write("home.html" if path == "/" else path.strip("/") + "/index.html", content)
    write("404.html", build_404())

    # sitemap.xml (lastmod: post date for posts, build date otherwise; image entries for each page's hero)
    post_dates = {f'/blog/{p["slug"]}/': p["date"] for p in POSTS}
    prio = lambda u: "1.0" if u == "/" else "0.9" if u.count("/") == 2 and not u.startswith("/blog/") else "0.7"
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for path, content in pages.items():
        images = []
        for src in re.findall(r'<img src="(/assets/img/[\w-]+\.webp)"', content):
            if src not in images:
                images.append(src)
        imgs = "".join(f"<image:image><image:loc>{ORIGIN}{i}</image:loc></image:image>" for i in images[:10])
        sm.append(f"  <url><loc>{ORIGIN}{path}</loc><lastmod>{post_dates.get(path, TODAY)}</lastmod>"
                  f"<priority>{prio(path)}</priority>{imgs}</url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    write("site.webmanifest", json.dumps({
        "name": SITE["name"], "short_name": "VIP Gifts", "description": P.HOME_DESC,
        "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                  {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": "#0e0b16", "background_color": "#0e0b16", "display": "standalone", "start_url": "/"}, indent=2))
    write("blog/feed.xml", build_feed())
    # PHP, favicons and the Search Console verification file
    for f in os.listdir(os.path.join(ROOT, "server")):
        shutil.copy(os.path.join(ROOT, "server", f), os.path.join(OUT, f))
    print(f"built {len(pages)} pages + 404 into {OUT}")


if __name__ == "__main__":
    main()
