#!/usr/bin/env python3
"""Static generator for agadecor.com.

Writes every page to public/pages/*.html and a route table to public/routes.php.
public/index.php serves them (see README, "Hosting"). Standard library only.

    python3 build.py && python3 validate.py
"""

import html
import json
import os
import re
from datetime import date

from siteconfig import SITE, NAV
import blog

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
PAGES_DIR = os.path.join(PUB, "pages")
TODAY = date.today().isoformat()
ORIGIN = SITE["origin"]

IMG = {c["file"][:-5]: c for c in json.load(open(os.path.join(HERE, "image-credits.json")))}


def esc(s):
    return html.escape(s, quote=True)


def img(name, alt, cls="", eager=False, sizes="(max-width: 900px) 100vw, 50vw", attrs=""):
    c = IMG[name]
    w, h = c["w"], c["h"]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<img src="/assets/img/{name}.webp" srcset="/assets/img/{name}-sm.webp 640w, /assets/img/{name}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}"{cls_attr} {loading}{attrs}>')


# --------------------------------------------------------------------------- layout

def nav_html(current):
    items = []
    for label, href, subs in NAV:
        cur = ' aria-current="page"' if href == current or any(s[1] == current for s in subs) else ""
        sub = ""
        if subs:
            sub = '<ul class="sub">' + "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in subs) + "</ul>"
        items.append(f'<li><a href="{href}"{cur}>{esc(label)}</a>{sub}</li>')
    items.append('<li class="cta"><a href="/contact-us">Start Planning</a></li>')
    return "".join(items)


BRAND = '<span class="brand-mark">AGA <span>Décor</span></span>'


def footer_html():
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a class="brand" href="/">{BRAND}</a>
        <p>Wedding and event décor for {esc(SITE['region'])} — planning, design, florals and rentals, styled from the first sketch to the last candle.</p>
        <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="/services">Plan · Design · Décor</a></li>
          <li><a href="/wedding-planing">Planning &amp; Packages</a></li>
          <li><a href="/destination-weddings">Destination Weddings</a></li>
          <li><a href="/gallery">Inspiration Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4>Rentals</h4>
        <ul>
          <li><a href="/decor-rental">Décor Rental</a></li>
          <li><a href="/decor-rental#backdrops">Flower Walls &amp; Backdrops</a></li>
          <li><a href="/linens">Linens</a></li>
          <li><a href="/furniture">Furniture</a></li>
          <li><a href="/vases">Vases &amp; Glass</a></li>
          <li><a href="/extras">Extras &amp; Lighting</a></li>
        </ul>
      </div>
      <div>
        <h4>Studio</h4>
        <ul>
          <li><a href="/about-us">About</a></li>
          <li><a href="/vendors">Chicago Venue Guide</a></li>
          <li><a href="/blog">Journal</a></li>
          <li><a href="/contact-us">Contact</a></li>
          <li><a href="/privacy-policy">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-big" aria-hidden="true">Art · Glamour · Ambiance</div>
    <div class="footer-bottom">
      <span>© <span data-year>{date.today().year}</span> AGA Décor · Serving {esc(SITE['region'])} and destination celebrations</span>
      <span><a href="/sitemap.xml">Sitemap</a> · <a href="/privacy-policy">Privacy</a></span>
    </div>
    <p class="disclaimer">agadecor.com is independently owned and operated. It is not affiliated with any business that previously used this domain. Photography on this site is licensed stock inspiration imagery (CC0), not portfolio work — see <a href="/privacy-policy#credits">image credits</a>.</p>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><svg viewBox="0 0 54 54" aria-hidden="true"><circle cx="27" cy="27" r="24"/></svg>↑</button>"""


def org_schema():
    return {
        "@type": "Organization",
        "@id": ORIGIN + "/#org",
        "name": SITE["name_plain"],
        "alternateName": SITE["name"],
        "url": ORIGIN + "/",
        "email": SITE["email"],
        "slogan": SITE["tagline"],
        "description": "Wedding and event décor studio serving Chicago and the North Shore: planning, design, custom florals and décor rentals.",
        "areaServed": [{"@type": "City", "name": c} for c in SITE["area_served"]],
        "knowsAbout": ["Wedding decor", "Event decor", "Wedding flowers", "Flower wall rental", "Wedding planning", "Décor rental"],
    }


def breadcrumb(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + (u if u != "/" else "/")}
            for i, (n, u) in enumerate(trail)
        ],
    }


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }


def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{esc(q)}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faqs
    ) + "</div>"


def layout(path, title, desc, body, schema=None, og_image="hero-aisle", header_class="", og_type="website", extra_head=""):
    canonical = ORIGIN + (path if path != "/" else "/")
    graph = [org_schema(), {
        "@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
        "description": desc, "isPartOf": {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": SITE["name_plain"]},
        "primaryImageOfPage": ORIGIN + f"/assets/img/{og_image}.webp", "inLanguage": "en-US",
    }] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#120e0c">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_image}.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header {header_class}">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="AGA Décor home">{BRAND}<span class="brand-tag">Chicago</span></a>
    <nav aria-label="Primary"><ul class="menu" id="menu">{nav_html(path)}</ul></nav>
    <button class="burger" type="button" aria-label="Menu" aria-controls="menu" aria-expanded="false"><span></span></button>
  </div>
</header>
<main id="main">
{body}
</main>
{footer_html()}
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def page_hero(eyebrow, h1, lede, image, crumbs):
    cr = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{esc(n)}</li>'
                 for i, (n, u) in enumerate(crumbs))
    return f"""
<section class="page-hero">
  <div class="bg" data-parallax="10">{img(image, "", eager=True, sizes="100vw")}</div>
  <div class="wrap">
    <ol class="crumbs fade-up">{cr}</ol>
    <p class="eyebrow fade-up" style="animation-delay:.1s">{eyebrow}</p>
    <h1 class="fade-up" style="animation-delay:.2s">{h1}</h1>
    <p class="lede fade-up" style="animation-delay:.35s">{lede}</p>
  </div>
</section>"""


def cta_block(h2="Let’s design the day you keep picturing.", lede="Tell us the date, the venue and the feeling you want guests to walk into. We’ll come back with a décor plan, a mood board and a clear quote.", service=""):
    q = f"?service={service}" if service else ""
    return f"""
<section class="section tight">
  <div class="wrap">
    <div class="cta-block reveal">
      <p class="eyebrow">Now booking weddings &amp; events</p>
      <h2>{h2}</h2>
      <p class="lede">{lede}</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-gold" href="/contact-us{q}">Start your inquiry <span class="arrow">→</span></a>
        <a class="btn btn-ghost" href="/gallery">Browse inspiration</a>
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------- pages

PAGES = {}   # path -> html
META = {}    # path -> dict(title, desc, lastmod, priority)


def add(path, title, desc, body, priority="0.7", **kw):
    assert path not in PAGES, path
    PAGES[path] = layout(path, title, desc, body, **kw)
    META[path] = {"title": title, "desc": desc, "lastmod": TODAY, "priority": priority}


THEMES = [
    # name, palette, swatch names, note
    ("Romantic Blush", dict(bg="#3a2a27", drape="#f3dcd5", linen="#fbf3ef", runner="#d9a8a0", flower="#efc3bb", accent="#f6e1c8", leaf="#9fae95"),
     "Blush rose|Dusty mauve|Ivory linen|Candle glow|Sheer drape", "Soft blush florals, ivory linen and a forest of candlelight — timeless, airy, endlessly photogenic."),
    ("Black, White & Gold", dict(bg="#0e0c0b", drape="#2b2724", linen="#f7f4ee", runner="#1a1716", flower="#fbfaf6", accent="#d6b06a", leaf="#6f7a68"),
     "White bloom|Black runner|Crisp white|Gilded gold|Noir drape", "Black-tie drama: white blooms against noir, gold chargers and crystal catching the light."),
    ("Garden Coral", dict(bg="#2f3328", drape="#e8efe0", linen="#fdfaf4", runner="#a9b79c", flower="#f29a7e", accent="#ffd9a8", leaf="#7e9a6c"),
     "Coral peony|Sage runner|Garden linen|Peach glow|Fern drape", "Coral peonies, trailing greenery and garden-party ease — made for summer terraces."),
    ("Vintage Champagne", dict(bg="#30281f", drape="#efe2cc", linen="#f8f0e2", runner="#c9a873", flower="#f3e6cf", accent="#f7d9a0", leaf="#a3a184"),
     "Champagne rose|Antique gold|Parchment|Warm glow|Lace drape", "Champagne roses, antique gold and lace — a 1920s toast with modern restraint."),
    ("Dusty Rose", dict(bg="#3b2b30", drape="#e9cfd3", linen="#f7eef0", runner="#a9727c", flower="#cf98a1", accent="#f1d1c4", leaf="#8d9a8a"),
     "Dusty rose|Mauve velvet|Rose linen|Blush glow|Petal drape", "Muted rose, mauve velvet and eucalyptus: romantic, a little moody, very now."),
    ("Rose Gold Lustre", dict(bg="#2c2122", drape="#f2d7cc", linen="#fff7f2", runner="#c48f7a", flower="#f5d0c4", accent="#ffd1b0", leaf="#a8b19c"),
     "Rose quartz|Rose gold|Pearl linen|Sequin glow|Satin drape", "Rose-gold sequins, pearl linens and blush blooms — the ‘everything that sparkles’ edit."),
]


def studio_html():
    btns = []
    for name, pal, names, note in THEMES:
        dots = "".join(f'<i style="background:{pal[k]}"></i>' for k in ("flower", "runner", "accent"))
        btns.append(f'<button class="theme-btn" type="button" aria-pressed="false" data-palette=\'{json.dumps(pal)}\' '
                    f'data-names="{esc(names)}" data-note="{esc(note)}">{esc(name)}<span class="dots">{dots}</span></button>')
    sw = "".join('<div class="swatch"><i></i><span></span></div>' for _ in range(5))
    return f"""
<div class="studio">
  <div class="themes" role="group" aria-label="Choose a décor theme">{''.join(btns)}</div>
  <div>
    <div class="scene" role="img" aria-label="Illustrated reception table that changes colour with the selected theme">
      <div class="backdrop"></div><div class="lights"></div>
      <div class="table"></div><div class="runner"></div>
      <div class="leaf l1"></div><div class="leaf l2"></div>
      <div class="bloom b4"></div><div class="bloom b5"></div>
      <div class="bloom b1"></div><div class="bloom b2"></div><div class="bloom b3"></div>
      <div class="candle c1"></div><div class="candle c2"></div><div class="candle c3"></div><div class="candle c4"></div>
    </div>
    <div class="swatches">{sw}</div>
    <p class="theme-note" aria-live="polite"></p>
  </div>
</div>"""


HOME_FAQ = [
    ("What areas do you serve?",
     "We design weddings and events across Chicago, Park Ridge and the North Shore — Evanston, Wilmette, Winnetka, Glenview, Highland Park and Lake Forest — plus the western and northwest suburbs. Destination weddings are planned case by case."),
    ("Do you only do weddings?",
     "Weddings are the heart of what we do, but the same plan · design · décor process works for engagement parties, showers, milestone birthdays, galas and brand events. If it has guests and a mood, we can style it."),
    ("Can I rent décor without full-service design?",
     "Yes. Flower walls, backdrops, linens, furniture, vases and lighting can be booked on their own. Delivery, set-up and tear-down are quoted with every rental so you are not hauling anything on the day."),
    ("How far ahead should we book?",
     "For Saturday weddings in May through October, six to twelve months ahead is comfortable. Smaller events and rental-only orders can often be turned around in a few weeks — ask, and we will check the calendar."),
    ("How do you price wedding décor?",
     "Every quote is built from your guest count, venue, floral choices and rentals, so we don’t publish one-size prices. After a consultation you receive an itemised proposal you can adjust line by line."),
]


def build_home():
    services = [
        ("services", "reception-blush", "01", "Plan · Design · Décor", "Our signature three-step process: a blueprint, a theme and colour story, then a full install on the day."),
        ("decor-rental", "tablescape-gold", "02", "Décor Rental", "Flower walls, sequin backdrops, gold stands, crystal candle holders, linens and lounge furniture."),
        ("wedding-planing", "bouquet-bride", "03", "Planning & Florals", "Full planning, month-of coordination and custom floral collections from bouquet to centrepiece."),
    ]
    cards = "".join(f"""
      <a class="card reveal" style="--d:{i * .12}s" href="/{slug}">
        {img(im, "")}
        <span class="shine"></span>
        <div class="card-body"><span class="num">{n}</span><h3>{t}</h3><p>{p}</p><span class="more">Explore →</span></div>
      </a>""" for i, (slug, im, n, t, p) in enumerate(services))

    gallery_preview = "".join(f"""
      <figure class="tile reveal" style="--d:{i * .08}s" data-cat="x">{img(n, a, sizes="(max-width: 700px) 100vw, 33vw")}<figcaption>{esc(c)}<small>{esc(s)}</small></figcaption></figure>"""
        for i, (n, a, c, s) in enumerate([
            ("hero-aisle", "Ceremony aisle lined with white and blush flower arrangements on gold stands", "Garden of Roses", "Ceremony"),
            ("tablescape-gold", "Long table with gold candlesticks, greenery runner and white china", "Vintage Champagne", "Reception"),
            ("bridal-bouquets", "Bride holding a loose white and peach garden bouquet", "Blush Garden", "Florals"),
            ("crystal-chandelier", "Crystal drum chandelier glowing over a reception", "Black, White & Gold", "Lighting"),
            ("beach-arch", "Beach wedding arch with white drapes and pink aisle chairs", "Destination", "Ceremony"),
            ("roses-moody", "Peach roses and white blooms in a moody arrangement", "Dusty Rose", "Florals"),
        ]))

    body = f"""
<section class="hero">
  <div class="hero-media">{img("hero-aisle", "Wedding ceremony aisle lined with white and blush floral arrangements", eager=True, sizes="100vw")}</div>
  <canvas id="petals" aria-hidden="true"></canvas>
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <p class="eyebrow fade-up">Wedding &amp; Event Décor · Chicago</p>
    <h1 data-split>Wedding and event décor, <em class="shimmer">styled to stay with you.</em></h1>
    <p class="lede fade-up" style="animation-delay:.9s">AGA Décor plans, designs and installs wedding and event décor across Chicago and the North Shore — custom florals, flower walls, backdrops, linens and lighting, brought together into one unforgettable room.</p>
    <div class="hero-actions fade-up" style="animation-delay:1.1s">
      <a class="btn btn-gold" href="/contact-us">Plan your event <span class="arrow">→</span></a>
      <a class="btn btn-ghost" href="/decor-rental">Explore rentals</a>
    </div>
    <div class="hero-meta fade-up" style="animation-delay:1.3s"><span>Plan</span><span>Design</span><span>Décor</span><span>Delivery, set-up &amp; tear-down included</span></div>
  </div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{''.join(f'<span>{t}</span>' for t in ['Romantic Blush','Black, White &amp; Gold','Garden Coral','Vintage Champagne','Dusty Rose','Rose Gold','Classic &amp; Vintage','Blush Garden','Peach Accents','Asian Weddings']*2)}</div></div>

<section class="section">
  <div class="wrap split">
    <div class="stack">
      <figure class="a reveal-img">{img("reception-blush", "Reception tables dressed in white with blush and fuchsia centrepieces")}</figure>
      <figure class="b reveal-img">{img("bouquet-roses", "Lavender rose bridal bouquet", sizes="(max-width: 900px) 60vw, 25vw")}</figure>
      <div class="badge" aria-hidden="true">
        <svg viewBox="0 0 120 120"><defs><path id="circ" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><text font-size="10.5" letter-spacing="3.2" fill="currentColor" font-family="Manrope, sans-serif" font-weight="600"><textPath href="#circ">PLAN · DESIGN · DÉCOR · CHICAGO · </textPath></text></svg>
        <b>A</b>
      </div>
    </div>
    <div>
      <p class="eyebrow reveal">Event décor, start to finish</p>
      <h2 class="reveal">Your vision, <em>staged</em> like a set.</h2>
      <p class="lede reveal">Great event décor is architecture with flowers. We start with your venue’s bones — ceilings, sightlines, light — and build a room around the story you want to tell.</p>
      <p class="reveal">Whether it’s a ballroom wedding in Rosemont, a loft reception in the West Loop or a garden party on the North Shore, we bring every element under one plan: the colour scheme, the backdrop, the centrepieces, the linens, the glow. One team designs it, delivers it, sets it up and takes it home again.</p>
      <ul class="checks reveal">
        <li>Wedding coordination</li><li>Custom floral design</li><li>Ceremony décor</li><li>Reception décor</li>
        <li>Flower walls &amp; backdrops</li><li>Charger plates &amp; linens</li><li>Up-lighting</li><li>Rentals with set-up</li>
      </ul>
      <a class="btn reveal" href="/about-us">Meet the studio <span class="arrow">→</span></a>
    </div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">What we do</p><h2 class="reveal">Wedding and event décor services</h2></div>
      <p class="lede reveal">Book the full design experience, a single flower wall, or anything in between. Every service includes delivery, installation and tear-down.</p>
    </div>
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap process">
    <div class="process-visual">
      {img("wedding-menu", "Wedding menu card on a white place setting")}
      {img("tablescape-gold", "Styled reception table with gold candlesticks")}
      {img("reception-hall-lights", "Reception hall with long tables under strings of lights")}
      <span class="label">Plan</span>
    </div>
    <div>
      <p class="eyebrow">How it works</p>
      <h2>Plan. Design. Décor.</h2>
      <p class="lede">A simple three-tier structure that turns a Pinterest board into a room you can walk into.</p>
      <div class="steps"><span class="bar"></span>
        <div class="step" data-label="Plan"><span class="k">i.</span><h3>Plan — the blueprint</h3><p>A one-on-one consultation to learn about you, the venue and the feeling you’re after. We map the floor plan, guest count and every décor element into a detailed, itemised plan — and often surface ideas you didn’t know you wanted.</p></div>
        <div class="step" data-label="Design"><span class="k">ii.</span><h3>Design — theme &amp; colour</h3><p>Every event has a story and a vibrancy to flaunt. Burnt orange for an autumn affair, the shimmer of crystal for a red-carpet night, blush and gold for something timeless. You’ll see a mood board, sample palettes and mock-ups before anything is ordered.</p></div>
        <div class="step" data-label="Décor"><span class="k">iii.</span><h3>Décor — the day itself</h3><p>Months of planning come together in a few hours of install. We decorate from the floor up — linens, furniture, florals, candles, lighting — then step back so your grand entrance lands exactly as imagined. Tear-down is on us.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section bg-noir">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Palette studio</p><h2>Try a colour story on for size.</h2></div>
      <p class="lede">Tap a theme to restyle the table. Every palette here is one we can build in real flowers, linens and light — mix, match, or bring your own.</p>
    </div>
    {studio_html()}
  </div>
</section>

<section class="band">
  {img("ballroom", "", sizes="100vw", attrs=' data-parallax="14"')}
  <div class="wrap reveal">
    <blockquote>“A wedding should be like a fingerprint — unique to its owners, and impossible to replicate.”</blockquote>
    <cite>The AGA Décor philosophy</cite>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">Inspiration</p><h2 class="reveal">Looks we love to build</h2></div>
      <p class="lede reveal">Romantic blush, black-tie gold, coral gardens, champagne vintage. Browse the full <a class="link-arrow" href="/gallery">inspiration gallery</a>.</p>
    </div>
    <div class="masonry">{gallery_preview}</div>
  </div>
</section>

<section class="section bg-cream">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">Why AGA Décor</p><h2 class="reveal">Stress-free décor, start to finish</h2></div>
      <p class="lede reveal">No pressure sales and no surprise fees — just a clear plan and a team that shows up with everything.</p>
    </div>
    <div class="features">
      <div class="feature reveal"><div class="ico">✦</div><h3>Always on-trend</h3><p>We track each season’s colours and textures so your design feels current — and still timeless in photos.</p></div>
      <div class="feature reveal" style="--d:.1s"><div class="ico">❀</div><h3>Custom florals</h3><p>Bouquets, centrepieces and large installs designed around your palette, not a catalogue.</p></div>
      <div class="feature reveal" style="--d:.2s"><div class="ico">⌂</div><h3>Delivery included</h3><p>Every booking includes delivery, set-up and tear-down at your venue.</p></div>
      <div class="feature reveal" style="--d:.3s"><div class="ico">♡</div><h3>No-pressure planning</h3><p>Itemised proposals you can adjust line by line, with honest advice on where to spend.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow reveal">Wedding décor Chicago</p>
      <h2 class="reveal">Chicago weddings, from ballroom to beach house</h2>
      <p class="reveal">Chicago gives you every kind of room: gilded ballrooms near O’Hare, raw-brick lofts in the West Loop, country clubs along the North Shore, conservatories and lakefront terraces. Each one asks for something different — a ballroom needs scale and up-lighting, a loft wants warmth and texture, a garden needs florals that survive July.</p>
      <p class="reveal">We’ve put together a <a href="/vendors">Chicago-area venue guide</a> with the banquet halls, hotels and country clubs couples ask us about most, plus notes on what décor tends to work in each type of space.</p>
      <ul class="pill-list reveal">{''.join(f'<li>{c}</li>' for c in SITE['area_served'][:10])}</ul>
    </div>
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img("garden-reception", "Outdoor reception under trees strung with lights and bunting")}</div>
  </div>
</section>

<section class="section bg-cream">
  <div class="narrow">
    <p class="eyebrow reveal">Questions</p>
    <h2 class="reveal">Event décor FAQs</h2>
    {faq_html(HOME_FAQ)}
  </div>
</section>
{cta_block()}
"""
    add("/", "Wedding & Event Decor Chicago | Flowers, Rentals & Design — AGA Décor",
        "Wedding and event decor in Chicago and the North Shore: custom wedding flowers, flower wall rental, backdrops, linens and full plan-design-décor service.",
        body, priority="1.0", schema=[faq_schema(HOME_FAQ)], header_class="")


def build_services():
    faqs = [
        ("What happens at the first consultation?", "We talk through your date, venue, guest count, budget and the look you love. Bring screenshots, swatches, even a fabric scrap. From there we sketch the floor plan and list every décor element in a draft proposal."),
        ("Can you work with my venue’s rules?", "Yes. Many Chicago venues restrict open flame, ceiling rigging or install windows. We confirm the rules with the venue coordinator up front and design around them — LED candles, freestanding backdrops, faster load-in."),
        ("Do you coordinate with my florist or planner?", "Happily. If you already have a florist or planner, we can supply only the décor, rentals and installation and take direction from their timeline."),
    ]
    blocks = [
        ("plan", "Plan", "Wedding décor blueprint", "wedding-menu",
         "We believe it’s essential to create an organised blueprint that captures exactly what you’re looking for. It starts with a one-on-one consultation — a chance to get to know you, the event and the theme you want surrounding you on the big day.",
         ["Venue walk-through and floor plan", "Guest count, table shapes and layout", "Itemised décor list with options", "Budget guidance and priorities", "Timeline for orders, samples and install"]),
        ("design", "Design", "Theme and colour scheme", "tablescape-gold",
         "Every event has a story to tell and a vibrancy to flaunt. Coordinating your colour scheme with your theme is where we shine — whether it’s a burnt orange autumn affair or the glitz of red-carpet Hollywood.",
         ["Mood board and colour story", "Floral recipe for bouquets and centrepieces", "Linen, charger and glassware pairing", "Backdrop and focal-point concepts", "Lighting plan: up-lighting, candles, pin-spots"]),
        ("decor", "Décor", "The wedding day", "reception-hall-lights",
         "The decorations have been hand-picked, the layout sketched, and all that’s left is decorating from the bottom up at the venue. When you make your grand entrance, we want you looking in every direction, smiling cheek to cheek.",
         ["Delivery to the venue", "Full ceremony and reception install", "Florals placed fresh on the day", "Final walk-through with the venue", "Tear-down and pick-up after the event"]),
    ]
    rows = "".join(f"""
<section class="section{' bg-cream' if i % 2 else ''}" id="{k}">
  <div class="wrap split{' rev' if i % 2 else ''}">
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img(im, f'{label} stage: {h}')}</div>
    <div>
      <p class="eyebrow reveal">Step {i + 1} · {label}</p>
      <h2 class="reveal">{label}: <em>{h.lower()}</em></h2>
      <p class="lede reveal">{p}</p>
      <ul class="checks reveal">{''.join(f'<li>{x}</li>' for x in li)}</ul>
    </div>
  </div>
</section>""" for i, (k, label, h, im, p, li) in enumerate(blocks))
    body = page_hero("Services", "Plan · Design · Décor: wedding &amp; event decoration",
                     "Our goal is to take different decorative elements and bring them together into exactly what you imagined — and display it even better than you expected.",
                     "reception-blush", [("Home", "/"), ("Services", "/services")]) + f"""
<section class="section tight">
  <div class="wrap">
    <div class="features">
      <div class="feature reveal"><div class="ico">✦</div><h3>Wedding coordination</h3><p>From full planning to month-of — see <a href="/wedding-planing">packages</a>.</p></div>
      <div class="feature reveal" style="--d:.1s"><div class="ico">❀</div><h3>Custom florals</h3><p>Bouquets, boutonnières, centrepieces and statement floral installs.</p></div>
      <div class="feature reveal" style="--d:.2s"><div class="ico">◇</div><h3>Ceremony &amp; reception</h3><p>Arches, aisles, head tables, sweetheart tables, lounges and entrances.</p></div>
      <div class="feature reveal" style="--d:.3s"><div class="ico">☼</div><h3>Backdrops &amp; lighting</h3><p>Flower walls, sequin backdrops, draping, up-lighting and candlelight.</p></div>
    </div>
  </div>
</section>
{rows}
<section class="section">
  <div class="narrow">
    <p class="eyebrow reveal">Good to know</p>
    <h2 class="reveal">Wedding décor questions</h2>
    {faq_html(faqs)}
  </div>
</section>
<section class="section tight bg-blush">
  <div class="wrap split">
    <div><p class="eyebrow reveal">Referrals</p><h2 class="reveal">We love referrals</h2></div>
    <p class="lede reveal">Planning something for a friend? Introduce them to us — when they book, we’ll send a thank-you gift your way.</p>
  </div>
</section>
{cta_block(service="design")}
"""
    add("/services", "Wedding Event Decoration Services | Plan · Design · Décor — AGA Décor",
        "Full-service wedding and event decoration in Chicago: consultation and floor plan, theme and colour design, then complete ceremony and reception décor install.",
        body, priority="0.9", og_image="reception-blush",
        schema=[breadcrumb([("Home", "/"), ("Services", "/services")]), faq_schema(faqs),
                {"@type": "Service", "name": "Wedding and event decoration", "serviceType": "Event decor",
                 "provider": {"@id": ORIGIN + "/#org"}, "areaServed": SITE["area_served"]}])


RENTAL_CATS = [
    ("backdrops", "Backdrops & flower walls", "pink-hydrangea", "/decor-rental",
     "The single most photographed spot at any wedding. Our flower walls and backdrops frame the sweetheart table, the ceremony or the photo corner — and arrive fully assembled.",
     [("Ivory flower wall", "Full rose & hydrangea panels"), ("Blush flower wall", "Soft pink mix"), ("Champagne sequin backdrop", "Shimmer wall"), ("Greenery wall", "Boxwood & ivy"),
      ("Draped ceremony arch", "Chiffon or tulle"), ("Neon sign add-on", "Names or a phrase")]),
    ("glass", "Glass & vases", "compote-arrangement", "/vases",
     "Clear and gilded vessels for every centrepiece height — the backbone of a cohesive tablescape.",
     [("Small & large cylinders", "Floating candles or florals"), ("Ceramic gold mini hexagon", "Low bud arrangements"), ("Trumpet vases", "Tall statement pieces"),
      ("Bud vase clusters", "Scattered runners"), ("Mercury glass votives", "Warm candle glow"), ("Hurricane globes", "Pillar candles")]),
    ("metal", "Metal stands & candelabra", "tablescape-gold", "/extras",
     "Height changes everything. Gold and silver stands lift florals above eye level so guests can still talk across the table.",
     [("Paris stands", "Silver & gold"), ("Geometric candle holders", "Modern gold"), ("Gold floor urns", "Ceremony & entrance"), ("Five-arm candelabra", "Classic gold"),
      ("Floral hoops", "Hanging or standing"), ("Gold charger plates", "Beaded or rimmed")]),
    ("crystal", "Crystal", "crystal-chandelier", "/extras",
     "For the glitz-and-glam crowd: crystal candle holders and trees that throw light across the whole room.",
     [("Gold crystal tall holders", "Tall centrepieces"), ("Manzanita crystal trees", "Silver branches"), ("Beaded crystal votives", "Round"), ("Crystal garland", "Draped strands"),
      ("Crystal cake stand", "Tiered"), ("Chandelier pin-spots", "Ceiling sparkle")]),
    ("furniture", "Furniture", "head-table", "/furniture",
     "Sweetheart tables, lounge vignettes and statement pieces that turn a ballroom into a series of moments.",
     [("48\" acrylic table", "Clear, modern"), ("60\" half-round table", "Head-table ends"), ("Velvet loveseat", "Sweetheart lounge"), ("Chiavari chairs", "Gold, silver, clear"),
      ("Lounge sets", "Sofa, chairs & rug"), ("Cake & dessert tables", "With skirts")]),
    ("linens", "Linens", "linen-texture", "/linens",
     "Linens set the tone before a single flower lands. Choose from satin, sequin, velvet and overlays in dozens of shades.",
     [("Silver sequin", "Head-table drama"), ("Champagne overlays", "Over ivory"), ("Blush satin", "Soft sheen"), ("Black & ivory", "Classic"),
      ("Chair covers & sashes", "Spandex or satin"), ("Napkins & runners", "Every colour")]),
]


def build_rental():
    nav = "".join(f'<li><a href="#{k}">{esc(t.split(" &")[0])}</a></li>' for k, t, *_ in RENTAL_CATS)
    cats = "".join(f"""
    <section class="cat" id="{k}">
      <figure class="reveal-img">{img(im, t + ' rental')}</figure>
      <div>
        <p class="eyebrow reveal">{'0' + str(i + 1)} · Rentals</p>
        <h2 class="reveal">{esc(t)}</h2>
        <p class="reveal">{p}</p>
        <ul class="items reveal">{''.join(f'<li>{esc(a)}<small>{esc(b)}</small></li>' for a, b in items)}</ul>
        <a class="link-arrow reveal" href="{link if link != '/decor-rental' else '/contact-us?service=rental'}">{'Check availability' if link == '/decor-rental' else 'See ' + esc(t.lower())} →</a>
      </div>
    </section>""" for i, (k, t, im, link, p, items) in enumerate(RENTAL_CATS))
    faqs = [
        ("How much does a flower wall rental in Chicago cost?", "It depends on size, flower density and whether you add signage or lighting, so we quote each one — delivery, assembly and pick-up are always included in the number you see. Ask for a quote with your date and venue and we’ll reply with options."),
        ("Do rentals include delivery and set-up?", "Yes. Every rental order includes delivery, set-up and tear-down within the Chicago area. Destination and long-distance orders are quoted separately."),
        ("Can I see items before booking?", "Yes — schedule a showroom-style appointment and we’ll pull the pieces you’re considering, including linen swatches and candle holders, so you can build a sample table."),
        ("What if something is damaged?", "Normal wear is on us. Breakage or loss beyond normal use is billed at replacement cost; we’ll walk you through it in writing before you book."),
    ]
    body = page_hero("Décor rental · Chicago", "Décor &amp; flower wall rental in Chicago",
                     "Quality, unique rental pieces for weddings and events — flower walls, backdrops, linens, furniture, glass, metal and crystal — with delivery, set-up and tear-down included.",
                     "tablescape-gold", [("Home", "/"), ("Décor Rental", "/decor-rental")]) + f"""
<nav class="cat-nav" aria-label="Rental categories"><div class="wrap"><ul>{nav}</ul></div></nav>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">Full-service rentals</p><h2 class="reveal">Everything you need, nothing to haul.</h2></div>
      <p class="lede reveal">Rent a single statement flower wall or outfit an entire ballroom. We deliver, install, and come back for it all after the last dance — so the only thing you take home is the bouquet.</p>
    </div>
    <div class="catalog">{cats}</div>
  </div>
</section>
<section class="band">
  {img("pink-hydrangea", "", sizes="100vw", attrs=' data-parallax="14"')}
  <div class="wrap reveal"><blockquote>Flower wall rental, Chicago-style: delivered, built and photographed-ready.</blockquote><cite>Backdrops · Arches · Photo corners</cite></div>
</section>
<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow reveal">Flower wall rental Chicago</p>
      <h2 class="reveal">Choosing the right flower wall</h2>
      <p class="reveal">An eight-by-eight wall frames a sweetheart table; a wider wall works behind a ceremony or as a photo-booth backdrop. Ivory and blush suit almost any palette, while a greenery wall reads modern and pairs beautifully with neon script. Ballrooms with high ceilings can take a taller build or a hanging installation above it.</p>
      <p class="reveal">Read our <a href="/blog/flower-wall-rental-guide">flower wall rental guide</a> for sizes, placement tips and the questions to ask any rental company, or just send us your venue and date.</p>
      <a class="btn reveal" href="/contact-us?service=rental">Request a flower wall quote <span class="arrow">→</span></a>
    </div>
    <div class="narrow" style="width:100%">{faq_html(faqs)}</div>
  </div>
</section>
{cta_block("Build your rental list.", "Tell us the venue and guest count and we’ll suggest quantities, pair linens with centrepieces and send a single quote with delivery included.", "rental")}
"""
    add("/decor-rental", "Flower Wall & Décor Rental Chicago | Backdrops, Linens, Furniture — AGA Décor",
        "Flower wall rental in Chicago plus backdrops, linens, furniture, vases, gold stands and crystal décor. Delivery, set-up and tear-down included with every rental.",
        body, priority="0.9", og_image="pink-hydrangea",
        schema=[breadcrumb([("Home", "/"), ("Décor Rental", "/decor-rental")]), faq_schema(faqs),
                {"@type": "Service", "name": "Flower wall and décor rental", "serviceType": "Event decor rental",
                 "provider": {"@id": ORIGIN + "/#org"}, "areaServed": SITE["area_served"]}])


SUBRENTALS = {
    "/linens": ("Linens", "Wedding linen rental: tablecloths, overlays &amp; chair covers", "linen-texture", "Linen Rental Chicago | Tablecloths, Overlays & Chair Covers — AGA Décor",
                "Wedding and event linen rental in Chicago: sequin and satin tablecloths, champagne overlays, chair covers, sashes, runners and napkins with delivery and set-up.",
                "linens",
                "Linens are the largest surface in the room, so they set the mood before the first flower is placed. We stock satin, sequin, velvet and textured overlays in neutrals and seasonal colours, sized for rounds, banquets, cocktail tables and sweetheart tables.",
                [("Colour first", "Pick linens after your florals so the petals pop rather than disappear — blush on ivory, burgundy on champagne, white on black."),
                 ("Mix textures", "A sequin head table with satin guest tables, or velvet runners over linen, adds depth without adding colour."),
                 ("Floor-length", "Floor-length cloths hide table legs and storage and photograph far better than lap-length."),
                 ("Chairs count too", "Chair covers and sashes are optional with Chiavari chairs, but they transform a banquet-hall chair.")]),
    "/furniture": ("Furniture", "Event furniture rental: lounges, sweetheart &amp; acrylic tables", "head-table", "Event Furniture Rental Chicago | Lounge, Acrylic & Sweetheart Tables — AGA Décor",
                   "Wedding furniture rental in Chicago: velvet loveseats, lounge vignettes, acrylic and half-round tables, Chiavari chairs and dessert tables, delivered and set up.",
                   "furniture",
                   "Furniture turns a big room into a series of places: a lounge where grandparents can sit, a sweetheart table that feels like a stage, a dessert table that becomes a destination. Everything is delivered, placed to the floor plan and collected after.",
                   [("Sweetheart tables", "Acrylic, mirrored or skirted — sized for two with room for florals."),
                    ("Lounge vignettes", "Velvet loveseats, accent chairs, rugs and side tables for cocktail hour."),
                    ("Head tables", "60\" half-rounds and banquets to build long or curved head tables."),
                    ("Chairs", "Chiavari chairs in gold, silver and clear, with cushions to match your palette.")]),
    "/vases": ("Vases & Glass", "Vase &amp; glassware rental for wedding centrepieces", "compote-arrangement", "Vase Rental for Wedding Centerpieces Chicago — AGA Décor",
               "Rent wedding centerpiece vases in Chicago: glass cylinders, gold hexagon vessels, trumpet vases, bud vases, mercury votives and hurricanes for every table.",
               "glass",
               "The vessel decides the silhouette of every centrepiece. Mix heights — a tall trumpet vase on every other table and low clusters between — and the room feels designed rather than repeated.",
               [("Cylinders", "Small to large, for floating candles, submerged blooms or tall branches."),
                ("Gold & ceramic", "Mini hexagons and compotes for low, lush garden arrangements."),
                ("Bud clusters", "Five to nine bud vases down a banquet table read like a runner."),
                ("Candle glass", "Mercury votives and hurricanes bring the warm glow photographers love.")]),
    "/extras": ("Extras & Lighting", "Lighting, stands, crystal &amp; finishing touches", "candles", "Wedding Decor Extras Chicago | Up-Lighting, Crystal & Gold Stands — AGA Décor",
                "Finishing touches for Chicago weddings and events: up-lighting, candelabra, gold floor urns, Paris stands, crystal holders, charger plates and signage.",
                "metal",
                "The extras are what guests remember without knowing why: a wash of up-lighting on bare walls, a gold urn at the entrance, a crystal tree catching candlelight. They’re easy to add to any rental or design package.",
                [("Up-lighting", "Wireless LED fixtures that wash walls in your palette — the fastest way to transform a ballroom."),
                 ("Stands & urns", "Paris stands, floral hoops and gold floor urns for aisles and entrances."),
                 ("Crystal", "Tall gold crystal holders and manzanita crystal trees for glamour."),
                 ("Chargers & signage", "Beaded and gold-rim charger plates, welcome signs and table numbers.")]),
}


def build_subrentals():
    for path, (name, h1, im, title, desc, anchor, intro, tips) in SUBRENTALS.items():
        cat = next(c for c in RENTAL_CATS if c[0] == anchor)
        items = "".join(f'<li>{esc(a)}<small>{esc(b)}</small></li>' for a, b in cat[5])
        tips_html = "".join(f'<div class="feature reveal" style="--d:{i * .1}s"><div class="ico">✦</div><h3>{esc(t)}</h3><p>{esc(p)}</p></div>' for i, (t, p) in enumerate(tips))
        body = page_hero("Décor rental", h1, intro, im, [("Home", "/"), ("Décor Rental", "/decor-rental"), (name, path)]) + f"""
<section class="section">
  <div class="wrap split">
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img(im, name + ' for weddings and events')}</div>
    <div>
      <p class="eyebrow reveal">In the collection</p>
      <h2 class="reveal">{esc(name)} we rent</h2>
      <ul class="items reveal">{items}</ul>
      <p class="reveal">Inventory changes with the seasons — tell us your palette and we’ll send photos of what’s available for your date.</p>
      <a class="btn reveal" href="/contact-us?service=rental">Check availability <span class="arrow">→</span></a>
    </div>
  </div>
</section>
<section class="section bg-cream">
  <div class="wrap">
    <p class="eyebrow reveal">Styling notes</p>
    <h2 class="reveal">How to style {esc(name.lower())}</h2>
    <div class="features">{tips_html}</div>
    <p class="reveal" style="margin-top:2rem">Browse the rest of our <a href="/decor-rental">décor rental collection</a> — flower walls, backdrops, crystal and more.</p>
  </div>
</section>
{cta_block(service="rental")}
"""
        add(path, title, desc, body, priority="0.6", og_image=im,
            schema=[breadcrumb([("Home", "/"), ("Décor Rental", "/decor-rental"), (name, path)])])


def build_packages():
    faqs = [
        ("What’s the difference between full planning and month-of coordination?", "Full planning starts right after the engagement: we help you choose the venue and every vendor, build the budget and run the timeline. Month-of coordination is for couples who’ve booked everything already and want a pro to confirm vendors, finalise the timeline and run the day."),
        ("Can I add florals to a coordination package?", "Yes — most couples combine coordination with a floral collection and a few rentals. Everything appears on one proposal."),
        ("Do you publish package prices?", "Floral costs swing with the season, flower varieties and guest count, so we quote each wedding individually. You’ll get an itemised proposal within a few days of your consultation."),
    ]
    pk = [
        ("Full planning", "Wedding Planning Elite", False,
         "Perfect for couples who just got engaged and have chosen a date. We help you find every vendor — venue, ceremony location, photo and video, music, hair and makeup, favours — and design a flawless, magical day.",
         ["Venue search and vendor shortlists", "Budget planning and tracking", "Design concept and décor plan", "Vendor contracts review and scheduling", "Rehearsal and full wedding-day management"]),
        ("Most requested", "Month-of Coordination", True,
         "For couples who have booked every vendor but want the big day organised by someone else. The footwork starts one month out: vendor confirmations two weeks before, timelines sent one week before.",
         ["Kick-off meeting four to six weeks out", "Vendor confirmations and final details", "Minute-by-minute timeline", "Rehearsal direction", "On-site coordination on the day"]),
        ("Florals", "‘Fresh From the Garden’ Collection", False,
         "A complete floral collection in premium blooms — jumbo hydrangeas, garden roses and greenery in white or ivory with an accent colour of your choice.",
         ["Hand-tied bridal bouquet", "Bridesmaid bouquets and boutonnières", "Corsages for family", "Tall and low centrepieces", "Head-table florals with candles", "Delivery, set-up and tear-down"]),
        ("À la carte", "Create Your Own", False,
         "Build a package from scratch. Send us your inspiration photos and a rough list and we’ll come back with a tailored quote — florals, rentals, design, coordination, in any combination.",
         ["Mix florals, rentals and design", "Pick only what you need", "Itemised, adjustable quote", "Perfect for intimate weddings and showers"]),
    ]
    cards = "".join(f"""
      <article class="pkg reveal{' featured' if feat else ''}" style="--d:{i * .1}s">
        <span class="tag">{esc(tag)}</span>
        <h3>{esc(name)}</h3>
        <p>{esc(p)}</p>
        <ul>{''.join(f'<li>{esc(x)}</li>' for x in li)}</ul>
        <a class="btn {'btn-gold' if feat else ''}" href="/contact-us?service=planning">Ask about this package <span class="arrow">→</span></a>
      </article>""" for i, (tag, name, feat, p, li) in enumerate(pk))
    body = page_hero("Planning &amp; packages", "Wedding planning, coordination &amp; floral packages",
                     "From the day you say yes to the last dance: full wedding planning, month-of coordination and floral collections you can tailor to your celebration.",
                     "bouquet-bride", [("Home", "/"), ("Services", "/services"), ("Planning & Packages", "/wedding-planing")]) + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">Packages</p><h2 class="reveal">Choose your level of support</h2></div>
      <p class="lede reveal">Every package can be combined with <a href="/services">décor design</a> and <a href="/decor-rental">rentals</a>. Not sure what you need? Start with a free consultation.</p>
    </div>
    <div class="packages">{cards}</div>
  </div>
</section>
<section class="section bg-cream">
  <div class="wrap split">
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img("bouquet-pastel", "Pastel bridal bouquet of roses, hydrangea and greenery")}</div>
    <div>
      <p class="eyebrow reveal">Good to know</p>
      <h2 class="reveal">Planning FAQs</h2>
      {faq_html(faqs)}
    </div>
  </div>
</section>
{cta_block(service="planning")}
"""
    add("/wedding-planing", "Wedding Planning & Coordination Packages Chicago — AGA Décor",
        "Wedding planning and month-of coordination in Chicago, plus floral packages and à la carte décor. Tailored proposals with delivery, set-up and tear-down.",
        body, priority="0.8", og_image="bouquet-bride",
        schema=[breadcrumb([("Home", "/"), ("Services", "/services"), ("Planning & Packages", "/wedding-planing")]), faq_schema(faqs)])


def build_destination():
    body = page_hero("Destination weddings", "Destination wedding décor &amp; honeymoon planning",
                     "Saying “I do” somewhere with a view? We design destination ceremonies and receptions — and can take the honeymoon planning off your plate, too.",
                     "beach-arch", [("Home", "/"), ("Services", "/services"), ("Destination Weddings", "/destination-weddings")]) + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow reveal">Beach, vineyard, villa</p>
      <h2 class="reveal">Destination décor that travels well</h2>
      <p class="reveal">Destination weddings bring their own rules: humidity that wilts the wrong flowers, wind that topples tall centrepieces, resort vendors you’ve never met. We design with the location in mind — sturdy arches anchored for the breeze, tropical-hardy blooms, lanterns instead of open candles — and coordinate directly with your resort or local florist.</p>
      <p class="reveal">You get the same plan · design · décor process as a Chicago wedding, delivered remotely: video consultations, a shared mood board, sample palettes shipped to your door, and a clear brief for the on-site team.</p>
      <ul class="checks reveal"><li>Ceremony arches &amp; aisles</li><li>Tropical-hardy florals</li><li>Lanterns &amp; wind-safe lighting</li><li>Resort vendor coordination</li></ul>
    </div>
    <div class="stack">
      <figure class="a reveal-img">{img("beach-gazebo", "Beach wedding gazebo with white drapes and pink chairs")}</figure>
      <figure class="b reveal-img">{img("beach-tables", "Beach reception table with colourful florals under a flower canopy", sizes="(max-width: 900px) 60vw, 25vw")}</figure>
    </div>
  </div>
</section>
<section class="band">
  {img("beach-arch", "", sizes="100vw", attrs=' data-parallax="14"')}
  <div class="wrap reveal"><blockquote>Wherever you’re going, the honeymoon shouldn’t be the last thing you plan.</blockquote><cite>Honeymoon planning</cite></div>
</section>
<section class="section bg-cream">
  <div class="wrap split rev">
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img("garden-bouquet", "Bright garden bouquet of roses and ranunculus on a wooden table")}</div>
    <div>
      <p class="eyebrow reveal">Honeymoon planning</p>
      <h2 class="reveal">Let us plan the honeymoon, too</h2>
      <p class="reveal">Wedding planning takes the better part of a year, and one of the things couples tell us most is, “We haven’t even started on the honeymoon.” It can feel daunting so close to the date — so let us take it off your shoulders.</p>
      <p class="reveal">The process is simple: tell us what you’d like the trip to feel like — all-inclusive beach, adventure, city-hopping, quiet villa — and we’ll come back with personalised options. All you have to do is choose.</p>
      <a class="btn reveal" href="/contact-us?service=destination">Plan a destination wedding <span class="arrow">→</span></a>
    </div>
  </div>
</section>
{cta_block(service="destination")}
"""
    add("/destination-weddings", "Destination Wedding Décor & Honeymoon Planning — AGA Décor",
        "Destination wedding decor designed for the location — beach, vineyard or villa — plus honeymoon planning so you can arrive relaxed. Based in Chicago.",
        body, priority="0.7", og_image="beach-arch",
        schema=[breadcrumb([("Home", "/"), ("Services", "/services"), ("Destination Weddings", "/destination-weddings")])])


GALLERY = [
    ("hero-aisle", "Garden of Roses", "ceremony florals", "Ceremony aisle of white and blush roses on gold stands"),
    ("reception-blush", "Romantic Blush", "reception florals", "Reception tables with blush and fuchsia centrepieces"),
    ("tablescape-gold", "Vintage Champagne", "reception", "Long table with gold candlesticks and a greenery runner"),
    ("crystal-chandelier", "Black, White & Gold", "reception lighting", "Crystal drum chandelier"),
    ("bridal-bouquets", "Blush Garden", "florals", "Loose white and peach bridal bouquet"),
    ("beach-arch", "Destination Breeze", "ceremony destination", "Beach ceremony arch with white drapes"),
    ("roses-moody", "Dusty Rose", "florals", "Peach roses and white blooms in a vase"),
    ("reception-hall-lights", "Rustic Glow", "reception lighting", "Long tables under strings of warm lights"),
    ("pink-hydrangea", "Pink Beauty", "florals backdrops", "Close-up of pink hydrangea blooms"),
    ("orange-table", "Autumn Harvest", "reception florals", "Long table with orange napkins and wildflower centrepieces"),
    ("aisle-moss", "Garden Ceremony", "ceremony", "White ceremony chairs with moss balls and petals"),
    ("bouquet-roses", "Lavender Romance", "florals", "Lavender rose bouquet"),
    ("tent-reception", "Tented Elegance", "reception", "Wedding reception under a white tent"),
    ("beach-gazebo", "Barefoot Chic", "destination ceremony", "Beach gazebo with pink chairs"),
    ("compote-arrangement", "Peach Accents", "florals", "Garden arrangement in a footed compote"),
    ("garden-reception", "Garden Coral", "reception lighting", "Outdoor reception under trees with lights"),
    ("ballroom", "Ballroom Classic", "reception", "Elegant ballroom with chandeliers"),
    ("bouquet-pastel", "Pastel Garden", "florals", "Pastel bridal bouquet"),
    ("table-setting-round", "Champagne Toast", "reception", "Round table setting with glassware and florals"),
    ("candles", "Candlelit", "lighting", "Row of pillar candles"),
    ("beach-tables", "Tropical Bloom", "destination reception", "Beach reception under a floral canopy"),
    ("head-table", "Head Table", "reception", "Wedding head table with white linens"),
    ("bouquet-chair", "Wildflower", "florals", "White garden bouquet resting on a chair"),
    ("long-table", "Loft Long Table", "reception", "Long white tables in a loft"),
]


def build_gallery():
    tiles = "".join(f"""
      <figure class="tile reveal" data-cat="{cat}">{img(n, alt, sizes="(max-width: 700px) 100vw, 33vw", attrs=f' data-full="/assets/img/{n}.webp"')}<figcaption>{esc(cap)}<small>{esc(cat.split()[0])}</small></figcaption></figure>"""
                    for n, cap, cat, alt in GALLERY)
    filters = "".join(f'<button type="button" data-filter="{f}" aria-pressed="{"true" if f == "all" else "false"}">{l}</button>'
                      for f, l in [("all", "All"), ("ceremony", "Ceremony"), ("reception", "Reception"), ("florals", "Florals"),
                                   ("lighting", "Lighting"), ("backdrops", "Backdrops"), ("destination", "Destination")])
    body = page_hero("Gallery", "Wedding décor inspiration gallery",
                     "Romantic blush, black and gold, coral gardens, champagne vintage — a mood board of looks we love to build. Tap any image to view it full-screen.",
                     "reception-toast", [("Home", "/"), ("Gallery", "/gallery")]) + f"""
<section class="section">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter gallery">{filters}</div>
    <div class="masonry">{tiles}</div>
    <p class="center" style="margin-top:2rem;color:var(--muted);font-size:.9rem">Inspiration imagery is licensed CC0 stock photography, used to illustrate styles and palettes.</p>
  </div>
</section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer">
  <button class="lb-close" type="button" aria-label="Close">✕</button>
  <button class="lb-prev" type="button" aria-label="Previous">←</button>
  <button class="lb-next" type="button" aria-label="Next">→</button>
  <div><img src="data:," alt=""><p></p></div>
</div>
{cta_block("Seen a look you love?", "Send us the theme name or a screenshot and we’ll show you how it could work at your venue, with your colours.")}
"""
    add("/gallery", "Wedding Decor Inspiration Gallery | Themes & Palettes — AGA Décor",
        "Browse wedding decor inspiration by theme: romantic blush, black white and gold, garden coral, dusty rose, vintage champagne, ceremony arches and flower walls.",
        body, priority="0.7", og_image="reception-toast",
        schema=[breadcrumb([("Home", "/"), ("Gallery", "/gallery")])])


VENUES = {
    "Banquet halls": ["Allegra", "Chateau Ritz", "Seville", "Venuti’s", "Café La Cave", "La Mirage", "Stonegate", "Camelot", "Crystal Grand", "Belvedere Chateau",
                      "European Crystal", "Victoria", "Florian", "Lido", "Gala", "Janosik", "Paradise", "Royalty West", "Mayfield", "DiNolfo’s", "Crystal Palace", "Salvatore’s", "Sabre Room", "Manzo’s"],
    "Hotels": ["Sheraton Grand Rosemont", "Chicago Marriott O’Hare", "Marriott Hoffman Estates", "Holiday Inn Skokie", "W Chicago", "Geneva Grand Resort"],
    "Country clubs & gardens": ["Chevy Chase Country Club", "Mission Hills Country Club", "White Pines Golf Club", "Chicago Botanic Garden", "Crystal Pavilion Evanston", "Redfield Estate", "Greenhouse Loft"],
}


def build_vendors():
    groups = "".join(f"""
      <div class="reveal" style="--d:{i * .1}s"><h3>{esc(g)}</h3><ul class="venues" style="columns:1">{''.join(f'<li>{esc(v)}</li>' for v in vs)}</ul></div>"""
                     for i, (g, vs) in enumerate(VENUES.items()))
    tips = [
        ("Ballrooms & banquet halls", "Scale is everything. Tall centrepieces on gold stands, up-lighting on the walls and a statement head table stop a big room from feeling empty."),
        ("Hotels", "Check install windows — hotel ballrooms often turn over fast. Freestanding backdrops and pre-built centrepieces keep load-in short."),
        ("Country clubs", "Lean into the view. Low, lush centrepieces keep sightlines to the windows and greens; save height for the ceremony."),
        ("Gardens & conservatories", "Let the setting lead. Choose heat-hardy blooms, add lanterns for evening, and plan a rain-ready second layout."),
        ("Lofts", "Exposed brick and beams love candlelight, greenery and long banquet tables. Draping can soften a ceiling."),
        ("Restaurants", "Work with the existing décor: bud vases, votives and a single focal arrangement rather than a full room overhaul."),
    ]
    tip_html = "".join(f'<div class="feature reveal" style="--d:{i % 4 * .08}s"><div class="ico">✦</div><h3>{esc(t)}</h3><p>{esc(p)}</p></div>' for i, (t, p) in enumerate(tips))
    body = page_hero("Chicago venue guide", "Chicago wedding venues &amp; vendor guide",
                     "The banquet halls, hotels, country clubs and gardens Chicago couples ask us about most — and how to decorate each kind of room.",
                     "ballroom", [("Home", "/"), ("About", "/about-us"), ("Venue Guide", "/vendors")]) + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow reveal">Venues we love to decorate</p><h2 class="reveal">Popular Chicago-area venues</h2></div>
      <p class="lede reveal">A starting list for your venue search across the city, the northwest suburbs and the North Shore. Always confirm availability, capacity and décor rules with the venue directly.</p>
    </div>
    <div class="venue-groups">{groups}</div>
  </div>
</section>
<section class="section bg-cream">
  <div class="wrap">
    <p class="eyebrow reveal">Décor by venue type</p>
    <h2 class="reveal">How to decorate every kind of room</h2>
    <div class="features">{tip_html}</div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow reveal">Building your team</p>
      <h2 class="reveal">The rest of your vendor list</h2>
      <p class="reveal">Beyond the venue, most Chicago weddings come together with the same core team: <strong>beauty</strong> (hair and makeup), a <strong>DJ or band</strong>, <strong>catering and sweets</strong>, <strong>photo and video</strong>, and — if you want help pulling it all together — a <a href="/wedding-planing">planner or month-of coordinator</a>.</p>
      <p class="reveal">Book the venue and photographer first; they set the date and fill fastest. Décor and florals usually follow once you know the room and the season.</p>
      <a class="btn reveal" href="/contact-us">Ask us for recommendations <span class="arrow">→</span></a>
    </div>
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img("events-venue", "Event venue set for a reception with long tables")}</div>
  </div>
</section>
{cta_block()}
"""
    add("/vendors", "Chicago Wedding Venues & Vendor Guide — AGA Décor",
        "A guide to popular Chicago wedding venues — banquet halls, hotels, country clubs and gardens — with decor tips for each type of room and the vendors to book.",
        body, priority="0.6", og_image="ballroom",
        schema=[breadcrumb([("Home", "/"), ("About", "/about-us"), ("Venue Guide", "/vendors")])])


def build_about():
    body = page_hero("About the studio", "A wedding &amp; event décor studio for Chicago",
                     "AGA Décor — Art, Glamour, Ambiance — is a wedding and event decorating studio serving Chicago, Park Ridge, the North Shore and destination celebrations.",
                     "bouquet-roses", [("Home", "/"), ("About", "/about-us")]) + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow reveal">Our philosophy</p>
      <h2 class="reveal">Plan, design, décor — <em>and listen first.</em></h2>
      <p class="lede reveal dropcap">Your wedding is the one day that leaves an imprint on your memory forever. Our concept is simple: plan, design, décor.</p>
      <p class="reveal">Each design is different because it starts with your concept, not ours. By following the three-tier structure we deliver something specific to each event — beauty, elegance and the flutter of butterflies as you walk in.</p>
      <p class="reveal">Our job is to take different decorative elements — flowers, fabric, light, furniture — and bring them together to create exactly what you want, displayed even better than you expected. We bring every element you need, from the colour scheme to the backdrop, across a wide range of themes, cultures and venue types.</p>
    </div>
    <div class="stack">
      <figure class="a reveal-img">{img("table-decoration", "Elegant wedding table with candelabra and white florals")}</figure>
      <figure class="b reveal-img">{img("flower-pink", "Pink roses and garden flowers", sizes="(max-width: 900px) 60vw, 25vw")}</figure>
    </div>
  </div>
</section>
<section class="section bg-noir">
  <div class="wrap">
    <p class="eyebrow">What it takes</p>
    <h2>Four things every event decorator needs</h2>
    <div class="cards four">
      {''.join(f'<div class="feature reveal" style="--d:{i * .1}s;background:transparent;border:1px solid rgba(245,237,230,.14);border-radius:var(--radius)"><div class="ico">{ic}</div><h3>{t}</h3><p style="color:rgba(245,237,230,.7)">{p}</p></div>' for i, (ic, t, p) in enumerate([
        ("❦", "Patience", "Every decision shapes the outcome. We’re not here to rush the process — we’re here to perfect the design you’ve envisioned."),
        ("✦", "Enthusiasm", "This is such a happy time. Being part of a union, a birth or any celebration is a privilege, and it shows in the details."),
        ("❀", "Creativity", "We treat each room as an empty canvas waiting for colourful cloth, blooming flowers and a glow that widens the senses."),
        ("♡", "Listening", "Our task isn’t to invent your idea but to inherit it and bring it to life — on your budget, in your style."),
      ]))}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split rev">
    <div class="img-round reveal-img" style="aspect-ratio:4/5">{img("place-card", "Place card tied to a pinecone on a white place setting")}</div>
    <div>
      <p class="eyebrow reveal">Our services include</p>
      <h2 class="reveal">Everything under one roof</h2>
      <ul class="checks reveal">
        <li>Custom centrepieces</li><li>Rental décor</li><li>Ceremony set-up</li><li>Ceremony furniture</li><li>Church decorations</li><li>Reception decorations</li>
        <li>Tablecloths &amp; linens</li><li>Chiavari chair rental</li><li>Chair covers</li><li>Backdrops</li><li>Charger plates</li><li>Up-lighting</li>
      </ul>
      <p class="reveal">…and much, much more. See <a href="/services">how we work</a> or explore the <a href="/decor-rental">rental collection</a>.</p>
    </div>
  </div>
</section>
{cta_block()}
"""
    add("/about-us", "About AGA Décor | Chicago Wedding & Event Decorators",
        "AGA Décor is a Chicago wedding and event decorating studio: plan, design, décor. Custom florals, rentals and full installs across Chicago and the North Shore.",
        body, priority="0.7", og_image="bouquet-roses",
        schema=[breadcrumb([("Home", "/"), ("About", "/about-us")])])


def build_contact():
    services = [("design", "Full décor design"), ("florals", "Wedding flowers"), ("rental", "Rentals only"), ("planning", "Wedding planning"),
                ("coordination", "Month-of coordination"), ("destination", "Destination wedding"), ("other", "Something else")]
    chips = "".join(f'<label><input type="checkbox" name="services[]" value="{v}"><span>{esc(l)}</span></label>' for v, l in services)
    hear = "".join(f"<option>{esc(o)}</option>" for o in ["Google search", "Instagram", "Facebook", "Friend referral", "Vendor referral", "Other"])
    body = page_hero("Contact", "Start planning your wedding décor",
                     "Share a few details and we’ll reply with availability, ideas and next steps — usually within one business day.",
                     "bouquet-chair", [("Home", "/"), ("Contact", "/contact-us")]) + f"""
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <p class="eyebrow reveal">Inquiries</p>
      <h2 class="reveal">Tell us about your day</h2>
      <p class="reveal">The more we know, the better our first ideas: the venue, the guest count, a few photos you love, and any colours you’re already set on. If you’re building a custom package, add your wish list in the message and we’ll return an itemised proposal.</p>
      <ul class="contact-list reveal">
        <li><div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
        <li><div><b>Serving</b>Chicago, Park Ridge, the North Shore, the suburbs &amp; destinations</div></li>
        <li><div><b>Consultations</b>In person or by video, by appointment</div></li>
      </ul>
    </div>
    <form class="form reveal" id="form" method="post" action="/contact-us">
      <p class="notice" role="status">Thank you — your details were sent. We’ll be in touch shortly.</p>
      <p class="notice err" role="alert">Sorry, something went wrong. Please check the required fields or email us directly.</p>
      <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="f-date">Event date</label><input id="f-date" name="date" type="date"></div>
      <div class="field"><label for="f-venue">Ceremony &amp; reception location</label><input id="f-venue" name="venue"></div>
      <div class="field"><label for="f-guests">Guest count</label><input id="f-guests" name="guests" inputmode="numeric"></div>
      <div class="field full"><label>Services you’re interested in</label><div class="chips">{chips}</div></div>
      <div class="field full"><label for="f-hear">How did you hear about us?</label><select id="f-hear" name="heard"><option value="">Choose one</option>{hear}</select></div>
      <div class="field full"><label for="f-msg">Tell us about your vision</label><textarea id="f-msg" name="message" placeholder="Colours, themes, must-haves, links to inspiration…"></textarea></div>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="ts" value="">
      <div class="full"><button class="btn btn-gold" type="submit">Send inquiry <span class="arrow">→</span></button></div>
      <p class="form-note full">We only use your details to reply to your inquiry. See our <a href="/privacy-policy">privacy policy</a>.</p>
    </form>
  </div>
</section>
"""
    add("/contact-us", "Contact AGA Décor | Wedding Decor Inquiry Chicago",
        "Inquire about wedding and event decor, flower wall rental, wedding flowers or planning in Chicago. Send your date and venue for availability and ideas.",
        body, priority="0.8", og_image="bouquet-chair",
        schema=[breadcrumb([("Home", "/"), ("Contact", "/contact-us")]), {"@type": "ContactPage", "url": ORIGIN + "/contact-us"}])


def build_privacy():
    credits = json.load(open(os.path.join(HERE, "image-credits.json")))
    rows = "".join(f'<li>{esc(c["file"])} — “{esc(c["title"] or "Untitled")}”{(" by " + esc(c["creator"])) if c.get("creator") else ""}, '
                   f'{esc(c["license"].upper())} via {esc(c["source"])} (<a href="{esc(c["landing"])}" rel="nofollow noopener">source</a>)</li>'
                   for c in credits)
    body = page_hero("Legal", "Privacy policy", "How agadecor.com handles the information you share with us.",
                     "linen-texture", [("Home", "/"), ("Privacy", "/privacy-policy")]) + f"""
<section class="section">
  <div class="narrow prose">
    <p>Last updated {date.today().strftime('%B %Y')}.</p>
    <h2>What we collect</h2>
    <p>When you send an inquiry we receive the details you type into the form — name, email, phone, event date, venue, guest count, services and message. We use them only to respond to your inquiry and to prepare a proposal.</p>
    <h2>What we don’t do</h2>
    <p>We don’t sell your information, and we don’t add you to marketing lists without asking. This site does not use advertising trackers.</p>
    <h2>Retention</h2>
    <p>Inquiry details are kept for as long as needed to plan your event and meet record-keeping obligations, then deleted. Email <a href="mailto:{SITE['email']}">{SITE['email']}</a> to request access to, or deletion of, your data.</p>
    <h2>Ownership</h2>
    <p>agadecor.com is independently owned and operated. It is not affiliated with any business or individual that previously used this domain name.</p>
    <h2 id="credits">Image credits</h2>
    <p>All photographs on this site are public-domain (CC0) stock images used as styling inspiration. They do not depict events produced by AGA Décor.</p>
    <ul style="font-size:.85rem">{rows}</ul>
  </div>
</section>
"""
    add("/privacy-policy", "Privacy Policy — AGA Décor", "Privacy policy and image credits for agadecor.com.", body, priority="0.2", og_image="linen-texture")


def build_blog():
    for p in blog.POSTS:
        trail = [("Home", "/"), ("Journal", "/blog"), (p["short"], p["path"])]
        toc = ""
        heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])
        if len(heads) >= 3:
            toc = '<nav class="toc"><strong>In this article</strong><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + "</ol></nav>"
        related = [q for q in blog.POSTS if q["path"] != p["path"]][:3]
        rel = "".join(post_card(q) for q in related)
        body = f"""
<section class="page-hero">
  <div class="bg" data-parallax="10">{img(p['image'], '', eager=True, sizes='100vw')}</div>
  <div class="wrap">
    <ol class="crumbs fade-up">{''.join(f'<li><a href="{u}">{esc(n)}</a></li>' if i < 2 else f'<li aria-current="page">{esc(n)}</li>' for i, (n, u) in enumerate(trail))}</ol>
    <p class="eyebrow fade-up" style="animation-delay:.1s">{esc(p['category'])}</p>
    <h1 class="fade-up" style="animation-delay:.2s">{esc(p['h1'])}</h1>
    <p class="post-meta fade-up" style="animation-delay:.35s"><span>AGA Décor Journal</span><span>Updated {date.fromisoformat(p['modified']).strftime('%B %Y')}</span><span>{p['minutes']} min read</span></p>
  </div>
</section>
<article class="section">
  <div class="narrow prose">
    {toc}
    {p['body']}
    <div class="callout reveal"><h3>Planning something?</h3><p>{p.get('cta', 'Tell us your date and venue and we’ll put together a décor plan and quote.')}</p><a class="btn" href="/contact-us">Start your inquiry <span class="arrow">→</span></a></div>
  </div>
</article>
<section class="section bg-cream">
  <div class="wrap"><p class="eyebrow reveal">Keep reading</p><h2 class="reveal">More from the journal</h2><div class="posts">{rel}</div></div>
</section>"""
        schema = [breadcrumb(trail), {
            "@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "image": ORIGIN + f"/assets/img/{p['image']}.webp",
            "datePublished": p["published"], "dateModified": p["modified"], "mainEntityOfPage": ORIGIN + p["path"],
            "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"}}]
        add(p["path"], p["title"], p["desc"], body, priority="0.6", og_image=p["image"], og_type="article", schema=schema)
        META[p["path"]]["lastmod"] = p["modified"]

    cards = "".join(post_card(p) for p in blog.POSTS)
    body = page_hero("Journal", "Wedding décor ideas, trends &amp; guides",
                     "Colour trends, flower ideas, rental guides and real-world advice for decorating weddings and events in Chicago and beyond.",
                     "wedding-flowers", [("Home", "/"), ("Journal", "/blog")]) + f"""
<section class="section"><div class="wrap"><div class="posts">{cards}</div></div></section>
{cta_block()}"""
    add("/blog", "Wedding Decor Ideas & Trends Journal — AGA Décor",
        "Wedding decor ideas, colour trends, wedding flower decoration tips and flower wall rental guides from AGA Décor, a Chicago wedding and event decor studio.",
        body, priority="0.7", og_image="wedding-flowers",
        schema=[breadcrumb([("Home", "/"), ("Journal", "/blog")]),
                {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["path"]} for i, p in enumerate(blog.POSTS)]}])


def post_card(p):
    return f"""
      <a class="post-card reveal" href="{p['path']}">
        <div class="ph">{img(p['image'], p['h1'], sizes="(max-width: 600px) 100vw, 33vw")}</div>
        <span class="meta">{esc(p['category'])} · {p['minutes']} min</span>
        <h3>{esc(p['short'])}</h3>
        <p>{esc(p['desc'])}</p>
      </a>"""


def build_404():
    body = f"""
<section class="hero err-hero">
  <div class="hero-media">{img("candles", "", eager=True, sizes="100vw")}</div>
  <canvas id="petals" aria-hidden="true"></canvas>
  <div class="wrap">
    <p class="big shimmer">404</p>
    <h1 style="font-size:clamp(2rem,4vw,3rem);max-width:none">This page has floated away.</h1>
    <p class="lede" style="margin-inline:auto">The link may be old or mistyped. Try one of these instead:</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-gold" href="/">Home</a><a class="btn btn-ghost" href="/decor-rental">Décor rental</a><a class="btn btn-ghost" href="/gallery">Gallery</a><a class="btn btn-ghost" href="/contact-us">Contact</a>
    </div>
  </div>
</section>"""
    return layout("/404", "Page not found — AGA Décor", "The page you were looking for could not be found.", body)


def build_410():
    body = """
<section class="section" style="padding-top:200px">
  <div class="narrow center">
    <p class="eyebrow">410 · Gone</p>
    <h1 style="font-size:clamp(2rem,4vw,3rem)">This page no longer exists.</h1>
    <p class="lede">Member profile pages from this domain’s previous website have been permanently removed.</p>
    <a class="btn btn-gold" href="/">Visit AGA Décor</a>
  </div>
</section>"""
    return layout("/410", "Page removed — AGA Décor", "This page has been permanently removed.", body, header_class="light")


# --------------------------------------------------------------------------- write

VERSION = "1"


def main():
    global VERSION
    css = open(os.path.join(PUB, "assets/css/site.css"), "rb").read()
    js = open(os.path.join(PUB, "assets/js/site.js"), "rb").read()
    import hashlib
    VERSION = hashlib.md5(css + js).hexdigest()[:8]

    for f in (build_home, build_services, build_rental, build_subrentals, build_packages, build_destination,
              build_gallery, build_vendors, build_about, build_contact, build_blog, build_privacy):
        f()

    os.makedirs(PAGES_DIR, exist_ok=True)
    for f in os.listdir(PAGES_DIR):
        os.remove(os.path.join(PAGES_DIR, f))
    routes = {}
    for path, doc in PAGES.items():
        fname = "home.html" if path == "/" else re.sub(r"[^A-Za-z0-9]+", "-", path.strip("/")).strip("-").lower() + ".html"
        assert fname not in routes.values(), fname
        open(os.path.join(PAGES_DIR, fname), "w").write(doc)
        routes[path] = {"file": fname, **META[path]}
    open(os.path.join(PAGES_DIR, "_404.html"), "w").write(build_404())
    open(os.path.join(PAGES_DIR, "_410.html"), "w").write(build_410())

    def php(v):
        return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"
    lines = ["<?php", "// Generated by build.py — do not edit. path => [file, lastmod, priority]", "return ["]
    for path, r in routes.items():
        lines.append(f"  {php(path)} => [{php(r['file'])}, {php(r['lastmod'])}, {php(r['priority'])}],")
    lines.append("];\n")
    open(os.path.join(PUB, "routes.php"), "w").write("\n".join(lines))
    print(f"built {len(routes)} pages + 404/410, css/js v{VERSION}")


if __name__ == "__main__":
    main()
