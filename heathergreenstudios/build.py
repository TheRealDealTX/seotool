#!/usr/bin/env python3
"""Static generator for heathergreenstudios.com.

    python3 build.py      # writes the deployable site into ./public

Standard library only. Source: src/ (CSS, JS, PHP), content/posts.py (journal).
"""
import html
import json
import math
import random
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from content.posts import POSTS  # noqa: E402

OUT = ROOT / "public"
ORIGIN = "https://heathergreenstudios.com"
SITE = "HGS Studio Journal"
EMAIL = "info@heathergreenstudios.com"
TODAY = "2026-10-10"
ASSET_V = "2"

NAV = [
    ("Printmaking", "/printmaking/"),
    ("Bisbee Art Guide", "/bisbee-art-guide/"),
    ("Journal", "/journal/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]

PALETTE = ["#b8602c", "#1f8a83", "#d98a4e", "#46b8ac", "#e6c99a", "#16130f", "#7a3b1c"]
CATS = ["Printmaking", "Collecting", "Mixed Media", "Studio Life", "Bisbee"]


def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(d)}, {y}"


# ---------------------------------------------------------------- generative art
def art_svg(seed, w=800, h=500, label=""):
    """A deterministic abstract 'print': Mule Mountain ridges, a sun disc,
    halftone dots and carved hatching in copper / turquoise / ink."""
    r = random.Random(seed)
    pal = PALETTE[:]
    r.shuffle(pal)
    bg = r.choice(["#f6f0e4", "#efe5d2", "#fffaf0"])
    uid = f"a{seed}"
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{esc(label or "Abstract print artwork")}">']
    parts.append(f'<defs><pattern id="{uid}d" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="2.4" fill="{pal[5] if pal[5] != bg else "#16130f"}" opacity=".35"/></pattern>'
                 f'<pattern id="{uid}h" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate({r.choice([30, 45, 60, -30])})"><line x1="0" y1="0" x2="0" y2="10" stroke="#16130f" stroke-width="2" opacity=".5"/></pattern>'
                 f'<filter id="{uid}r"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{seed}"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.1"/><feComposite in="SourceGraphic" operator="in"/></filter></defs>')
    parts.append(f'<rect width="{w}" height="{h}" fill="{bg}"/>')
    # sun / moon disc
    cx, cy, cr = r.uniform(.2, .8) * w, r.uniform(.15, .45) * h, r.uniform(.12, .22) * h * 1.6
    parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{cr:.0f}" fill="{pal[0]}" filter="url(#{uid}r)"/>')
    if r.random() < .6:
        parts.append(f'<circle cx="{cx + cr * .35:.0f}" cy="{cy - cr * .2:.0f}" r="{cr * .75:.0f}" fill="url(#{uid}d)"/>')
    # ridges
    layers = r.randint(3, 4)
    for i in range(layers):
        base = h * (0.48 + i * 0.14)
        amp = h * r.uniform(.06, .16)
        pts = []
        steps = 9
        for k in range(steps + 1):
            x = w * k / steps
            y = base - amp * (0.5 + 0.5 * math.sin(k * r.uniform(.6, 1.4) + r.uniform(0, 6))) - r.uniform(0, amp * .4)
            pts.append((x, y))
        d = f"M0 {h} L" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + f" L{w} {h} Z"
        col = pal[(i + 1) % len(pal)]
        if col == bg:
            col = "#16130f"
        parts.append(f'<path d="{d}" fill="{col}" filter="url(#{uid}r)" opacity="{0.92 - i * 0.04:.2f}"/>')
        if r.random() < .45:
            parts.append(f'<path d="{d}" fill="url(#{uid}h)" opacity=".5"/>')
    # carved marks
    for _ in range(r.randint(4, 9)):
        x, y = r.uniform(0, w), r.uniform(.05, .4) * h
        L = r.uniform(30, 120)
        parts.append(f'<path d="M{x:.0f} {y:.0f} q{L / 2:.0f} {-r.uniform(5, 25):.0f} {L:.0f} 0" stroke="#16130f" stroke-width="{r.uniform(1.5, 4):.1f}" fill="none" stroke-linecap="round" opacity=".55"/>')
    # stitched line
    if r.random() < .5:
        y = r.uniform(.6, .9) * h
        parts.append(f'<line x1="20" y1="{y:.0f}" x2="{w - 20}" y2="{y:.0f}" stroke="{bg}" stroke-width="3" stroke-dasharray="12 9" opacity=".9"/>')
    parts.append("</svg>")
    return "".join(parts)


PHOTO_DIR = ROOT / "src" / "assets" / "img" / "photos"

POST_PHOTOS = {
    "/2011/07/how-to-print-linoleum-block.html": ("printing-blocks-relief-carved", "Carved relief printing blocks arranged in a wooden frame"),
    "/2009/03/dos-and-donts-of-collecting-artists.html": ("art-gallery-framed-paintings", "Framed artworks lining the walls of a gallery corridor"),
    "/2009/02/original-art-for-little-scratch.html": ("hand-painting-with-fine-brush", "An artist's hand painting with a fine brush on white paper"),
    "/2011/04/paper-quilts.html": ("colored-paper-sheets", "Stacked sheets of colored paper"),
    "/2012/02/stitches-and-folds.html": ("antique-sewing-machine", "An antique sewing machine"),
    "/2009/06/great-reference-for-artists-books.html": ("handmade-books", "Handmade books with decorated covers"),
    "/2012/03/wall-musings.html": ("graphite-drawing-pencils", "Graphite drawing pencils from hard to soft"),
    "/2015/01/call-to-artists-mail-art-exchange.html": ("envelopes-mail-art", "Blank envelopes on a wooden table, ready for mail art"),
    "/2009/03/date-night-bisbee-after-5.html": ("bisbee-main-street-1940", "Main Street in Bisbee, Arizona, in 1940"),
    "/2011/11/my-paper-anniversary.html": ("book-pages-paper", "The fanned-out paper pages of an open book"),
    "/2015/04/life-is-process-as-is-art.html": ("watercolor-palette-studio", "A watercolor palette and brush on a studio table"),
    "/journal/how-to-hang-art/": ("framed-print-on-wall", "A framed print hanging on a dark wall above a plant"),
}


def photo(name, alt, cls="", eager=False, sizes="(max-width: 860px) 100vw, 60vw"):
    """<img> for a file in assets/img/photos, with real dimensions."""
    from PIL import Image  # optional dependency only needed for dimensions
    with Image.open(PHOTO_DIR / f"{name}.webp") as im:
        w, h = im.size
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="/assets/img/photos/{name}.webp" alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async" sizes="{sizes}">'


def mark_svg():
    return ('<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#16130f"/>'
            '<circle cx="31" cy="17" r="7" fill="#b8602c"/><path d="M4 33 L14 22 L21 28 L30 18 L44 31 A23 23 0 0 1 4 33Z" fill="#1f8a83"/>'
            '<path d="M8 38 L18 30 L26 35 L36 28 L42 34" stroke="#f6f0e4" stroke-width="1.6" fill="none" stroke-dasharray="3 2.5"/></svg>')


RIDGE = ('<svg class="ridge" viewBox="0 0 1440 180" preserveAspectRatio="none" aria-hidden="true">'
         '<path d="M0 120 L120 80 L230 110 L360 40 L470 95 L600 60 L720 105 L860 30 L980 90 L1110 55 L1240 100 L1340 70 L1440 95 L1440 180 L0 180Z" fill="#1f8a83" opacity=".9"/>'
         '<path d="M0 150 L160 110 L300 140 L420 100 L560 135 L700 95 L850 140 L1000 105 L1150 145 L1290 115 L1440 140 L1440 180 L0 180Z" fill="#16130f"/></svg>')


# ---------------------------------------------------------------- schema
def org_schema():
    return {
        "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE,
        "alternateName": "Heather Green Studios Journal",
        "url": ORIGIN + "/", "email": EMAIL,
        "logo": ORIGIN + "/assets/img/logo.svg",
        "areaServed": "Bisbee, Arizona",
    }


def site_schema():
    return {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": SITE,
            "publisher": {"@id": ORIGIN + "/#org"}, "inLanguage": "en-US"}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(items)]}


def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


# ---------------------------------------------------------------- layout
def layout(*, path, title, desc, body, schema=None, og_type="website", extra_head="", robots="index,follow"):
    url = ORIGIN + path
    graph = [org_schema(), site_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    nav = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{n}</a></li>' for n, u in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ORIGIN}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16130f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="/">{mark_svg()}<span class="brand-name">HGS Studio Journal<small>Bisbee · Print · Paper</small></span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span><span></span><span></span></button>
    <ul class="menu" id="menu">{nav}</ul>
  </nav>
</header>
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def footer():
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)[:4]
    recent = "".join(f'<li><a href="{p["path"]}">{esc(p["h1"])}</a></li>' for p in posts)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/" style="color:#f6f0e4">{mark_svg()}<span class="brand-name">HGS Studio Journal</span></a>
        <p style="margin-top:18px;max-width:34ch">An independent journal of printmaking, works on paper and the art scene of Bisbee, Arizona.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Explore</h4><ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)}</ul></div>
      <div><h4>Guides</h4><ul>
        <li><a href="/2011/07/how-to-print-linoleum-block.html">Print a linoleum block</a></li>
        <li><a href="/2009/03/dos-and-donts-of-collecting-artists.html">Collecting prints</a></li>
        <li><a href="/journal/how-to-hang-art/">How to hang art</a></li>
        <li><a href="/2015/01/call-to-artists-mail-art-exchange.html">Mail art exchanges</a></li>
      </ul></div>
      <div><h4>Recent</h4><ul>{recent}</ul></div>
    </div>
    <div class="foot-big" aria-hidden="true">Print · Paper · Bisbee</div>
    <div class="foot-bottom"><span>© <span data-year>2026</span> HGS Studio Journal · heathergreenstudios.com</span><span><a href="/privacy-policy/">Privacy</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
  </div>
</footer>"""


def cta():
    return f"""<section class="section-tight"><div class="wrap">
  <div class="cta reveal">
    <svg class="cta-art" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="cp" d="M100 100 m-80 0 a80 80 0 1 1 160 0 a80 80 0 1 1 -160 0"/></defs>
    <text style="font:600 13px sans-serif;letter-spacing:6px;fill:#fff"><textPath href="#cp">MAKE · PRINT · SEND · SHARE · MAKE · PRINT · SEND · SHARE ·</textPath></text></svg>
    <span class="eyebrow" style="color:#bff0ea">Get in touch</span>
    <h2>Have a story, a show or a print to share?</h2>
    <p>We feature printmakers, book artists and Bisbee happenings, and we run occasional mail-art exchanges. Drop us a line.</p>
    <a class="btn" href="/contact/">Contact the journal <span class="arr">→</span></a>
  </div>
</div></section>"""


def post_card(p, idx=0):
    d = f" reveal-d{idx % 3 + 1}" if idx else ""
    return f"""<a class="post-card reveal{d}" href="{p['path']}" data-cat="{slugify(p['cat'])}">
  <div class="art">{photo(*POST_PHOTOS[p['path']], sizes="(max-width: 700px) 100vw, 33vw") if p['path'] in POST_PHOTOS else art_svg(p['seed'], label=p['h1'])}</div>
  <div class="body"><span class="meta">{p['cat']} · {p['read']} min read</span><h3>{esc(p['h1'])}</h3><p>{esc(p['desc'])}</p></div>
</a>"""


# ---------------------------------------------------------------- pages
def page_home():
    featured = [p for p in POSTS if p["path"] in (
        "/2011/07/how-to-print-linoleum-block.html",
        "/2009/03/dos-and-donts-of-collecting-artists.html",
        "/journal/how-to-hang-art/")]
    techniques = [
        ("01", "Relief", "Linocut and woodcut: carve away what you don't want to print.", "/2011/07/how-to-print-linoleum-block.html", "#b8602c", ("printing-blocks-relief-carved", "Carved relief printing blocks")),
        ("02", "Collagraph", "Build a plate from texture, then print it like an etching.", "/2011/04/paper-quilts.html", "#1f8a83", ("colored-paper-sheets", "Sheets of colored paper")),
        ("03", "Monotype", "Paint on a plate, pull one unique print, then a ghost.", "/printmaking/#monotype", "#d98a4e", ("watercolor-palette-studio", "A paint palette and brush on a studio table")),
        ("04", "Book arts", "Fold, stitch and bind prints into objects you can hold.", "/2009/06/great-reference-for-artists-books.html", "#46b8ac", ("handmade-books", "Handmade books with decorated covers")),
    ]
    tech = "".join(f"""<a class="card card-photo reveal reveal-d{i % 3 + 1}" href="{u}" style="--accent:{c}"><span class="card-img">{photo(*img, sizes="(max-width: 700px) 100vw, 25vw")}</span><span class="blob" style="background:{c}"></span><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></a>"""
                   for i, (n, t, d, u, c, img) in enumerate(techniques))
    latest = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    words = ["Linocut", "Collagraph", "Monotype", "Artists' books", "Mail art", "Bisbee art walk", "Works on paper", "Ghost prints"]
    marquee = "".join(f"<span>{w}</span>" for w in words * 2)
    body = f"""
<section class="hero">
  <canvas id="ink" aria-hidden="true"></canvas>
  <svg class="hero-badge" viewBox="0 0 200 200" aria-hidden="true"><defs><path id="hb" d="M100 100 m-74 0 a74 74 0 1 1 148 0 a74 74 0 1 1 -148 0"/></defs>
    <text><textPath href="#hb">Bisbee, Arizona · Since 2009 · Print &amp; Paper ·</textPath></text>
    <circle cx="100" cy="100" r="30" fill="#b8602c"/><path d="M76 112 L90 96 L100 104 L112 90 L126 108" stroke="#f6f0e4" stroke-width="3" fill="none"/></svg>
  <div class="wrap">
    <span class="eyebrow">Studio journal · Bisbee, AZ</span>
    <h1 class="split">Ink, paper &amp; the <em>art&nbsp;of</em> Bisbee</h1>
    <p class="lede reveal reveal-d2">Hands-on guides to printmaking and book arts, honest advice on collecting original prints, and notes from the galleries and studios of Arizona's copper-mining town turned art town.</p>
    <div class="hero-actions reveal reveal-d3">
      <a class="btn btn-dark" href="/printmaking/">Explore printmaking <span class="arr">→</span></a>
      <a class="btn btn-ghost" href="/bisbee-art-guide/">Bisbee art guide</a>
    </div>
  </div>
  {RIDGE}
</section>
<div class="marquee-wrap" aria-hidden="true"><div class="marquee"><div class="marquee-track">{marquee}</div></div></div>

<section class="section">
  <div class="wrap intro">
    <div>
      <span class="eyebrow reveal">The journal</span>
      <p class="big reveal">Since 2009 this address has belonged to the <strong>print studio</strong>, the <strong>paper dress</strong>, the <strong>open call</strong> and the second-Saturday <strong>art walk</strong>. The journal keeps those threads going.</p>
      <p class="reveal">We write about how prints are made, how to tell an original from a reproduction, how to hang what you buy and where to see art in Bisbee. Everything here is written for working artists and curious collectors alike.</p>
      <a class="btn btn-ghost reveal" href="/about/">About the journal <span class="arr">→</span></a>
    </div>
    <div class="plate plate-photo reveal reveal-d2">{photo("printing-blocks-relief-carved", "Carved relief printing blocks in a wooden frame", sizes="(max-width: 860px) 100vw, 45vw")}<span class="tag">Relief blocks</span></div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">Techniques</span><h2 class="split">Four ways to make a mark</h2></div>
      <p class="reveal">Start with the technique that suits your space and tools. Each guide covers materials, process and troubleshooting.</p>
    </div>
    <div class="cards">{tech}</div>
    <div class="stats">
      <div class="stat reveal"><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>in-depth guides and essays</span></div>
      <div class="stat reveal reveal-d1"><b data-count="57">57</b><span>inches: gallery hanging height</span></div>
      <div class="stat reveal reveal-d2"><b data-count="5300">5300</b><span>feet: Bisbee's elevation</span></div>
      <div class="stat reveal reveal-d3"><b data-count="2009">2009</b><span>the year this studio blog began</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">Start here</span><h2 class="split">Most-read guides</h2></div>
      <p class="reveal">Our most-read guides on printing, collecting and displaying work on paper.</p>
    </div>
    <div class="posts">{"".join(post_card(p, i) for i, p in enumerate(featured))}</div>
  </div>
</section>

<section class="photo-band" aria-label="Main Street, Bisbee, 1940">
  <div class="photo-band-img" data-parallax>{photo("bisbee-main-street-mule-mountains-1940", "Main Street in Bisbee, Arizona, in 1940, with the Mule Mountains behind", cls="duotone", sizes="100vw")}</div>
  <div class="wrap photo-band-text"><p class="split">Copper built the town. Artists kept it alive.</p><span class="cap">Main Street, Bisbee · 1940</span></div>
</section>

<section class="section" style="background:var(--paper-2)">
  <div class="wrap intro">
    <div class="plate plate-photo reveal">{photo("bisbee-arizona-hillside-town", "Old Bisbee's brick buildings and hillside houses below the Mule Mountains", sizes="(max-width: 860px) 100vw, 45vw")}<span class="tag">Old Bisbee</span></div>
    <div>
      <span class="eyebrow reveal">Bisbee, Arizona</span>
      <h2 class="split">A mining camp that became an art town</h2>
      <p class="reveal">Tucked into the Mule Mountains near the Mexican border, Bisbee grew rich on copper and turquoise, then reinvented itself as a haven for artists after the mines closed. Today its steep streets are lined with galleries, studios and a monthly evening art walk.</p>
      <p class="reveal">Our guide covers the neighborhoods, the art walk, community art spaces and how to plan a visit.</p>
      <a class="btn btn-dark reveal" href="/bisbee-art-guide/">Read the Bisbee art guide <span class="arr">→</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow">From the journal</span><h2 class="split">Latest writing</h2></div>
      <a class="btn btn-ghost reveal" href="/journal/">All journal posts <span class="arr">→</span></a>
    </div>
    <div class="posts">{"".join(post_card(p, i) for i, p in enumerate(latest[:6]))}</div>
  </div>
</section>
{cta()}
"""
    return layout(path="/", title="HGS Studio Journal | Printmaking, Works on Paper & Bisbee Art",
                  desc="An independent journal of printmaking, book arts and collecting original prints, with guides to the galleries and art walk of Bisbee, Arizona.",
                  body=body)


def page_hero(crumbs, eyebrow, h1, lede, meta=""):
    cr = " / ".join(f'<a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]) + f" / <span>{esc(crumbs[-1][0])}</span>"
    return f"""<section class="page-hero"><span class="orb a"></span><span class="orb b"></span>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1 class="split">{h1}</h1>
    <p class="lede reveal reveal-d2">{lede}</p>{meta}
  </div>
</section>"""


def add_ids(body):
    toc = []

    def rep(m):
        attrs, text = m.group(1), m.group(2)
        if "id=" in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
            toc.append((hid, re.sub("<[^>]+>", "", text)))
            return m.group(0)
        hid = slugify(re.sub("<[^>]+>", "", text))
        toc.append((hid, re.sub("<[^>]+>", "", text)))
        return f'<h2 id="{hid}"{attrs}>{text}</h2>'
    return re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body), toc


def faq_html(faq):
    if not faq:
        return ""
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    return f'<h2 id="faq">Questions</h2><div class="faq">{items}</div>'


def page_post(p):
    body, toc = add_ids(p["body"])
    if p["faq"]:
        toc.append(("faq", "Questions"))
    related = [x for x in POSTS if x["cat"] == p["cat"] and x is not p][:3]
    if len(related) < 3:
        related += [x for x in POSTS if x is not p and x not in related][:3 - len(related)]
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    rel_html = "".join(f'<li><a href="{x["path"]}">{esc(x["h1"])}</a></li>' for x in related)
    meta = (f'<div class="post-meta reveal reveal-d3"><span>{p["cat"]}</span><span>First published {fmt_date(p["date"])}</span>'
            f'<span>Updated {fmt_date(p["updated"])}</span><span>{p["read"]} min read</span></div>')
    crumbs = [("Home", "/"), ("Journal", "/journal/"), (p["h1"], p["path"])]
    html_body = page_hero(crumbs, p["cat"], esc(p["h1"]), esc(p["desc"]), meta) + f"""
<section class="section-tight" style="padding-top:20px"><div class="wrap article-layout">
  <article class="prose">
    <figure class="photo-fig">{photo(*POST_PHOTOS[p['path']], eager=True, sizes="(max-width: 960px) 100vw, 780px") if p['path'] in POST_PHOTOS else art_svg(p['seed'], 1200, 600, p['h1'])}</figure>
    {body}
    {faq_html(p['faq'])}
  </article>
  <aside class="aside">
    <div class="aside-box toc"><h4>On this page</h4><ul>{toc_html}</ul></div>
    <div class="aside-box"><h4>Keep reading</h4><ul>{rel_html}</ul></div>
  </aside>
</div></section>
{cta()}"""
    schema = [
        {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
         "datePublished": p["date"], "dateModified": p["updated"],
         "mainEntityOfPage": ORIGIN + p["path"], "author": {"@id": ORIGIN + "/#org"},
         "publisher": {"@id": ORIGIN + "/#org"}, "articleSection": p["cat"],
         "image": ORIGIN + (f"/assets/img/photos/{POST_PHOTOS[p['path']][0]}.webp" if p['path'] in POST_PHOTOS else "/assets/img/og.png")},
        crumbs_schema(crumbs)]
    if p["faq"]:
        schema.append(faq_schema(p["faq"]))
    return layout(path=p["path"], title=f'{p["title"]} | {SITE}', desc=p["desc"], body=html_body,
                  schema=schema, og_type="article",
                  extra_head=f'<meta property="article:published_time" content="{p["date"]}">\n')


def page_journal():
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    btns = '<button aria-pressed="true" data-filter="all">All</button>' + "".join(
        f'<button aria-pressed="false" data-filter="{slugify(c)}">{c}</button>' for c in CATS)
    crumbs = [("Home", "/"), ("Journal", "/journal/")]
    body = page_hero(crumbs, "The journal", "Notes from the press bed",
                     "Guides, essays and Bisbee dispatches, from the studio blog's first posts in 2009 to today.") + f"""
<section class="section-tight" style="padding-top:10px"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter by topic">{btns}</div>
  <div class="posts">{"".join(post_card(p, i) for i, p in enumerate(posts))}</div>
</div></section>{cta()}"""
    schema = [crumbs_schema(crumbs), {"@type": "Blog", "name": SITE + " Journal", "url": ORIGIN + "/journal/",
              "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": ORIGIN + p["path"], "datePublished": p["date"]} for p in posts]}]
    return layout(path="/journal/", title=f"Journal: Printmaking, Collecting & Bisbee Art | {SITE}",
                  desc="All journal posts: printmaking how-tos, advice on collecting and hanging original prints, book arts, mail art and Bisbee art walk notes.",
                  body=body, schema=schema)


def page_printmaking():
    crumbs = [("Home", "/"), ("Printmaking", "/printmaking/")]
    faq = [
        ("What is the easiest printmaking technique for beginners?", "Monotype and linocut. Monotype needs only a smooth plate, ink and paper; linocut needs a block, a few gouges and a brayer, and both can be printed by hand."),
        ("Do I need a printing press?", "Not to start. Relief prints and monotypes can be burnished by hand with a baren or wooden spoon. Etchings, collagraphs inked intaglio and drypoints need an etching press."),
        ("What's the difference between relief and intaglio?", "In relief printing the raised surface takes the ink; in intaglio the ink sits in grooves and recesses below the surface and is pressed out onto damp paper."),
    ]
    rows = [
        ("Linocut / woodcut", "Relief", "Carving tools, brayer, baren", "No", "Bold shapes, graphic line"),
        ("Collagraph", "Intaglio or relief", "Board, glue, textures, press", "Usually", "Rich texture, painterly tone"),
        ("Monotype", "Planographic", "Plexi plate, ink, brushes", "No", "One-of-a-kind, painterly"),
        ("Drypoint", "Intaglio", "Scribe, plexi or copper, press", "Yes", "Velvety burred line"),
        ("Etching", "Intaglio", "Metal plate, ground, mordant, press", "Yes", "Fine line, tone with aquatint"),
        ("Screenprint", "Stencil", "Screen, squeegee, stencil", "No", "Flat, vivid color"),
    ]
    table = "".join(f"<tr>{''.join(f'<td>{c}</td>' for c in r)}</tr>" for r in rows)
    body = page_hero(crumbs, "Guide", "Printmaking, from first proof to finished edition",
                     "A field guide to the main printmaking techniques: how each works, what you need and where to start. Short versions here, with full how-tos in the journal.") + f"""
<section class="section-tight" style="padding-top:20px"><div class="wrap article-layout">
  <article class="prose">
    <figure class="photo-fig">{photo("printmakers-workshop-engraving", "An 18th-century engraving of a printmaker's workshop with a rolling press", eager=True, sizes="(max-width: 960px) 100vw, 780px")}<figcaption>A printmaker's workshop, from an 18th-century engraving. The rolling press has barely changed since.</figcaption></figure>
    <h2 id="what-makes-a-print">What makes a print a print?</h2>
    <p>Printmaking transfers an image from a prepared surface, called the matrix, onto paper. The matrix might be a block of linoleum, a copper plate, a sheet of plexiglass or a collaged board. Because the matrix can be inked again, one image can exist as several original impressions. That's what makes original prints the most affordable way to own a real artist's work, as explained in our <a href="/2009/03/dos-and-donts-of-collecting-artists.html">collecting guide</a>.</p>

    <h2 id="compare">Techniques at a glance</h2>
    <div class="table-wrap"><table><tr><th>Technique</th><th>Family</th><th>Key tools</th><th>Press needed?</th><th>Look</th></tr>{table}</table></div>

    <h2 id="relief">Relief: linocut and woodcut</h2>
    <p>Carve away everything you don't want to print, roll ink across the surface and press paper onto it. Linoleum is soft and even, wood has grain that can become part of the image. Read the full guide: <a href="/2011/07/how-to-print-linoleum-block.html">How to Print a Linoleum Block</a>.</p>
    <figure class="photo-fig">{photo("printing-blocks-relief-carved", "Carved relief printing blocks arranged in a frame", sizes="(max-width: 960px) 100vw, 780px")}</figure>
    <h3>Reduction prints</h3>
    <p>A multi-color print from a single block: print the lightest color across the whole edition, carve away what should stay that color, print the next color and repeat. The block is destroyed as you go, so the edition size is fixed from the start.</p>

    <h2 id="collagraph">Collagraph</h2>
    <p>A plate collaged from textured materials (lace, card, grit, gel medium), sealed and inked like an etching or a relief block. It is a wonderfully forgiving, tactile technique. See <a href="/2011/04/paper-quilts.html">Paper Quilts</a>.</p>

    <h2 id="monotype">Monotype and ghost prints</h2>
    <p>Paint or roll ink onto a smooth plate, wipe and draw into it, then print. Only one strong impression comes off, which makes every monotype unique. Run the plate through a second time and you get a <em>ghost</em>, a softer echo of the first. Tiny monotypes, just an inch or two across, make intimate jewel-like pieces.</p>

    <h2 id="intaglio">Intaglio: etching and drypoint</h2>
    <p>Lines are cut or bitten into a plate. Ink is pushed into them, the surface is wiped clean and damp paper is forced into the lines under heavy press pressure. Drypoint scratches directly into the plate, raising a burr that prints a soft, velvety line. Etching uses acid (or safer modern mordants) to bite lines drawn through a protective ground. Bisbee's copper heritage makes copper-plate etching a fitting local technique.</p>

    <h2 id="paper">Choosing paper</h2>
    <ul>
      <li><strong>Japanese papers</strong> (hosho, kitakata, mulberry): thin, strong, ideal for hand-burnished relief prints.</li>
      <li><strong>Western printmaking papers</strong> (cotton rag, mould-made): heavier sheets for press work and intaglio, usually dampened first.</li>
      <li><strong>Newsprint</strong> for proofs, always.</li>
    </ul>

    <h2 id="beyond-the-print">Beyond the single print</h2>
    <p>Prints are building blocks. Bind them into <a href="/2009/06/great-reference-for-artists-books.html">artists' books</a>, stitch them into <a href="/2012/02/stitches-and-folds.html">paper garments</a>, mail them in an <a href="/2015/01/call-to-artists-mail-art-exchange.html">exchange</a>, or frame them and <a href="/journal/how-to-hang-art/">hang them well</a>.</p>
    {faq_html(faq)}
  </article>
  <aside class="aside">
    <div class="aside-box toc"><h4>On this page</h4><ul>
      <li><a href="#compare">At a glance</a></li><li><a href="#relief">Relief</a></li><li><a href="#collagraph">Collagraph</a></li>
      <li><a href="#monotype">Monotype</a></li><li><a href="#intaglio">Intaglio</a></li><li><a href="#paper">Paper</a></li><li><a href="#faq">Questions</a></li></ul></div>
    <div class="plate plate-photo" style="aspect-ratio:3/4">{photo("drawing-pencils-art-supplies", "Drawing pencils and art supplies laid out on a table", sizes="300px")}<span class="tag">Studio tools</span></div>
  </aside>
</div></section>{cta()}"""
    schema = [crumbs_schema(crumbs), faq_schema(faq),
              {"@type": "Article", "headline": "Printmaking Techniques: A Field Guide", "dateModified": TODAY,
               "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"}, "mainEntityOfPage": ORIGIN + "/printmaking/"}]
    return layout(path="/printmaking/", title=f"Printmaking Techniques Guide: Linocut, Collagraph, Monotype & Etching | {SITE}",
                  desc="A field guide to printmaking techniques: linocut, woodcut, collagraph, monotype, drypoint and etching, with the tools each needs and how to choose paper.",
                  body=body, schema=schema)


def page_bisbee():
    crumbs = [("Home", "/"), ("Bisbee Art Guide", "/bisbee-art-guide/")]
    faq = [
        ("Where is Bisbee, Arizona?", "In Cochise County in southeastern Arizona, in the Mule Mountains about 90 miles southeast of Tucson and a few miles north of the Mexican border."),
        ("Why is Bisbee known as an art town?", "After large-scale copper mining wound down in the 1970s, low rents and dramatic scenery drew artists, writers and musicians, who filled the historic downtown with studios and galleries."),
        ("When is the best time to visit Bisbee for art?", "Spring and fall are mild. Plan around the monthly evening art walk, and check local calendars for festivals and open-studio events."),
    ]
    body = page_hero(crumbs, "Local guide", "The Bisbee art guide",
                     "How a copper-mining camp in the Mule Mountains became one of Arizona's most creative small towns, and how to explore its galleries, studios and art walk.") + f"""
<section class="section-tight" style="padding-top:20px"><div class="wrap article-layout">
  <article class="prose">
    <figure class="photo-fig">{photo("bisbee-arizona-hillside-town", "Old Bisbee's brick commercial buildings with houses climbing the hills behind", eager=True, sizes="(max-width: 960px) 100vw, 780px")}<figcaption>Old Bisbee climbs the canyon walls of Tombstone Canyon and Brewery Gulch.</figcaption></figure>
    <h2 id="from-copper-to-canvas">From copper to canvas</h2>
    <p>Bisbee was founded in 1880 on one of the richest copper deposits in the world. The Copper Queen and its neighbors produced copper, gold, silver and a vivid, much-prized turquoise known as <em>Bisbee Blue</em>. When large-scale mining ended in the mid-1970s, the town emptied out, and artists moved in. Victorian houses were cheap, the light was extraordinary and the canyon streets felt like nowhere else in America.</p>
    <p>Half a century later, Old Bisbee's brick storefronts hold galleries, working studios, bookshops and cafes, and the town's arts calendar is busier than many cities'.</p>

    <h2 id="timeline">A short timeline</h2>
    <div class="timeline">
      <div class="t"><b>1880</b>Mining claims staked in the Mule Mountains; the town of Bisbee follows.</div>
      <div class="t"><b>Early 1900s</b>Boom years. Bisbee becomes one of the largest towns in the Southwest.</div>
      <div class="t"><b>1975</b>Phelps Dodge ends large-scale mining operations in Bisbee.</div>
      <div class="t"><b>1970s–80s</b>Artists and craftspeople settle in Old Bisbee's empty storefronts and houses.</div>
      <div class="t"><b>Today</b>Galleries, studios, festivals and a monthly evening art walk define the town.</div>
    </div>

    <div class="photo-grid">
      <figure>{photo("bisbee-arizona-canyon-1940", "Bisbee seen from above in 1940, filling the canyon below bare hills", cls="duotone", sizes="(max-width: 700px) 100vw, 260px")}<figcaption>The town in its canyon, 1940</figcaption></figure>
      <figure>{photo("bisbee-main-street-1940", "Cars parked along Main Street in Bisbee in 1940", cls="duotone", sizes="(max-width: 700px) 100vw, 260px")}<figcaption>Main Street, 1940</figcaption></figure>
      <figure>{photo("bisbee-housetops-1940", "Rooftops of hillside houses in Bisbee in 1940", cls="duotone", sizes="(max-width: 700px) 100vw, 260px")}<figcaption>Hillside housetops, 1940</figcaption></figure>
    </div>
    <h2 id="where-to-look">Where to look</h2>
    <h3>Main Street</h3>
    <p>The heart of Old Bisbee: a winding street of galleries, studios and shops in turn-of-the-century buildings, climbing gently uphill from the Copper Queen Plaza.</p>
    <h3>Subway Street</h3>
    <p>Just above Main, a quieter lane of small galleries and studios, and the former home of this studio's storefront gallery.</p>
    <h3>Brewery Gulch</h3>
    <p>Once one of the rowdiest streets in the West, now a mix of bars, restaurants and creative spaces running up a side canyon.</p>
    <h3>Community art spaces</h3>
    <p>Bisbee's former school and civic buildings have been turned into studios, exhibition spaces and youth arts programs. Look for open studios and exhibitions in the historic Central School building above Main Street.</p>

    <h2 id="art-walk">The art walk</h2>
    <p>Bisbee has long held a monthly evening gallery walk on the second Saturday, when galleries stay open late, artists are on hand and the streets fill with music. Participating venues and hours change, so check current local listings. For tips on pacing the evening, read <a href="/2009/03/date-night-bisbee-after-5.html">Date Night in Bisbee</a>.</p>

    <figure class="photo-fig">{photo("arizona-desert-mountains", "Sunlit desert mountains rising above scrubland in southern Arizona", sizes="(max-width: 960px) 100vw, 780px")}<figcaption>The high desert of southern Arizona on the road to Bisbee.</figcaption></figure>
    <h2 id="plan-your-visit">Plan your visit</h2>
    <ul>
      <li><strong>Altitude:</strong> about 5,300 feet. Evenings are cool and the stairs are steep. Bring water and good shoes.</li>
      <li><strong>Getting there:</strong> roughly a 1.5-hour drive from Tucson via I-10 and AZ-80.</li>
      <li><strong>Beyond the galleries:</strong> the mining and historical museum, the underground mine tour and the Lavender Pit overlook tell the copper story.</li>
      <li><strong>Collect thoughtfully:</strong> read up on <a href="/2009/03/dos-and-donts-of-collecting-artists.html">buying original prints</a> before you go.</li>
    </ul>
    {faq_html(faq)}
  </article>
  <aside class="aside">
    <div class="aside-box toc"><h4>On this page</h4><ul>
      <li><a href="#from-copper-to-canvas">Copper to canvas</a></li><li><a href="#timeline">Timeline</a></li><li><a href="#where-to-look">Where to look</a></li>
      <li><a href="#art-walk">The art walk</a></li><li><a href="#plan-your-visit">Plan your visit</a></li><li><a href="#faq">Questions</a></li></ul></div>
    <div class="aside-box"><h4>Bisbee reading</h4><ul>
      <li><a href="/2009/03/date-night-bisbee-after-5.html">Date night on the art walk</a></li>
      <li><a href="/2015/04/life-is-process-as-is-art.html">Life is a process, as is art</a></li>
      <li><a href="/2015/01/call-to-artists-mail-art-exchange.html">Mail art exchanges</a></li></ul></div>
  </aside>
</div></section>{cta()}"""
    schema = [crumbs_schema(crumbs), faq_schema(faq),
              {"@type": "Article", "headline": "The Bisbee Art Guide", "dateModified": TODAY,
               "about": {"@type": "City", "name": "Bisbee", "containedInPlace": {"@type": "State", "name": "Arizona"}},
               "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"}, "mainEntityOfPage": ORIGIN + "/bisbee-art-guide/"}]
    return layout(path="/bisbee-art-guide/", title=f"Bisbee, Arizona Art Guide: Galleries, Studios & Art Walk | {SITE}",
                  desc="A guide to the art scene of Bisbee, Arizona: its copper-mining history, galleries on Main Street, Subway Street and Brewery Gulch, the art walk and visiting tips.",
                  body=body, schema=schema)


def page_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    body = page_hero(crumbs, "About", "A journal about print, paper and place",
                     "Who we are, what we write about and the history of this address.") + f"""
<section class="section-tight" style="padding-top:20px"><div class="wrap article-layout">
  <article class="prose">
    <h2 id="what-we-do">What we do</h2>
    <p>HGS Studio Journal publishes practical, carefully researched writing on printmaking, book arts and works on paper, plus guides for people who want to collect and live with original art. We also cover the arts community of Bisbee, Arizona, the small mountain town where this site's story began.</p>
    <ul>
      <li><strong>How-to guides</strong> for printmakers and paper artists at every level</li>
      <li><strong>Collector guides</strong> on editions, reproductions, framing and hanging</li>
      <li><strong>Local coverage</strong> of Bisbee's galleries, art walk and community art spaces</li>
      <li><strong>Exchanges and open calls</strong>, including occasional mail-art projects</li>
    </ul>

    <h2 id="history">The history of this address</h2>
    <p>From 2009 to 2015, heathergreenstudios.com was home to an artist's studio blog and storefront gallery on Subway Street in Old Bisbee. It covered printmaking and paper dresses, anniversary open calls, the second-Saturday art walk and youth art festivals. In 2015 the gallery closed and the blog went quiet.</p>
    <p>When the domain later became available, we rebuilt it as an independent journal on the same subjects, so the people and pages that once linked here still find something useful. The articles at the blog's original addresses have been newly written; the archive's subjects and spirit carry on.</p>
    <div class="callout"><strong>Please note</strong>HGS Studio Journal is an independent publication. It is not operated by, affiliated with or endorsed by the artist who originally ran this website, and it does not sell or represent her artwork.</div>

    <h2 id="contact">Get in touch</h2>
    <p>Story ideas, corrections, exhibition news and mail-art inquiries are always welcome: <a href="mailto:{EMAIL}">{EMAIL}</a>, or use the <a href="/contact/">contact form</a>.</p>
  </article>
  <aside class="aside">
    <div class="plate plate-photo" style="aspect-ratio:3/4">{photo("bisbee-arizona-canyon-1940", "Bisbee, Arizona, seen from above in 1940", cls="duotone", sizes="300px")}<span class="tag">Bisbee · 1940</span></div>
  </aside>
</div></section>{cta()}"""
    schema = [crumbs_schema(crumbs), {"@type": "AboutPage", "url": ORIGIN + "/about/", "about": {"@id": ORIGIN + "/#org"}}]
    return layout(path="/about/", title=f"About the Journal | {SITE}",
                  desc="About HGS Studio Journal, an independent publication on printmaking, works on paper and the Bisbee, Arizona art scene, and the history of heathergreenstudios.com.",
                  body=body, schema=schema)


def page_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    body = page_hero(crumbs, "Contact", "Say hello",
                     "Story pitches, exhibition news, mail-art inquiries or just a question about a print. We read everything.") + f"""
<section class="section-tight" style="padding-top:10px"><div class="wrap contact-grid">
  <div class="reveal">
    <h2 style="font-size:1.8rem">Email us directly</h2>
    <p><a href="mailto:{EMAIL}" style="font:600 1.3rem var(--serif)">{EMAIL}</a></p>
    <p>We usually reply within a few days.</p>
    <div class="plate plate-photo" style="aspect-ratio:4/3;margin-top:30px">{photo("vintage-postcards", "Boxes of vintage postcards for sale", sizes="(max-width: 860px) 100vw, 40vw")}<span class="tag">Mail art welcome</span></div>
  </div>
  <div class="reveal reveal-d1">
    <div id="form-note" hidden></div>
    <form class="form" method="post" action="/contact.php">
      <div class="row">
        <div><label for="f-name">Name</label><input id="f-name" name="name" required maxlength="120" autocomplete="name"></div>
        <div><label for="f-email">Email</label><input id="f-email" name="email" type="email" required maxlength="200" autocomplete="email"></div>
      </div>
      <div><label for="f-topic">Topic</label>
        <select id="f-topic" name="topic"><option>General question</option><option>Story or exhibition news</option><option>Mail art exchange</option><option>Correction</option><option>Other</option></select></div>
      <div><label for="f-msg">Message</label><textarea id="f-msg" name="message" required maxlength="5000"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
      <div><button class="btn btn-dark" type="submit">Send message <span class="arr">→</span></button></div>
    </form>
  </div>
</div></section>"""
    schema = [crumbs_schema(crumbs), {"@type": "ContactPage", "url": ORIGIN + "/contact/"}]
    return layout(path="/contact/", title=f"Contact | {SITE}",
                  desc="Contact HGS Studio Journal at info@heathergreenstudios.com with story ideas, exhibition news, mail-art inquiries or questions about prints.",
                  body=body, schema=schema)


def page_privacy():
    crumbs = [("Home", "/"), ("Privacy Policy", "/privacy-policy/")]
    body = page_hero(crumbs, "Legal", "Privacy policy", f"Last updated {fmt_date(TODAY)}.") + f"""
<section class="section-tight" style="padding-top:10px"><div class="wrap"><div class="prose">
<h2>What we collect</h2>
<p>This site doesn't use advertising trackers or set its own cookies. When you send a message through the contact form, we receive your name, email address and message so we can reply. Our web host keeps standard server logs (IP address, browser, pages requested) for security and maintenance.</p>
<h2>Fonts</h2>
<p>Pages load typefaces from Google Fonts, which receives your IP address when the fonts are requested.</p>
<h2>How we use it</h2>
<p>Messages are used only to respond to you. We don't sell or share personal information.</p>
<h2>Your choices</h2>
<p>To ask about or delete any message you've sent us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></div></section>"""
    return layout(path="/privacy-policy/", title=f"Privacy Policy | {SITE}",
                  desc="Privacy policy for heathergreenstudios.com: what the contact form collects, server logs, fonts and how to reach us.",
                  body=body, schema=[crumbs_schema(crumbs)])


def page_404():
    body = f"""<section class="nf"><div>
  <b>404</b>
  <h1 style="font-size:2.2rem">This page got lost in the press</h1>
  <p>The page you were looking for doesn't exist, or it moved when the site was rebuilt.</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn btn-dark" href="/">Home <span class="arr">→</span></a><a class="btn btn-ghost" href="/journal/">Browse the journal</a></div>
</div></section>"""
    return layout(path="/404.html", title=f"Page not found | {SITE}", desc="Page not found.", body=body, robots="noindex,follow")


# ---------------------------------------------------------------- write
def write(rel, text):
    f = OUT / rel.lstrip("/")
    if rel.endswith("/"):
        f = f / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "src", OUT)
    # Homepage is served by index.php (see README): no root index.html.
    write("/home.html", page_home())
    pages = ["/", "/printmaking/", "/bisbee-art-guide/", "/journal/", "/about/", "/contact/", "/privacy-policy/"]
    write("/printmaking/", page_printmaking())
    write("/bisbee-art-guide/", page_bisbee())
    write("/journal/", page_journal())
    write("/about/", page_about())
    write("/contact/", page_contact())
    write("/privacy-policy/", page_privacy())
    write("/404.html", page_404())
    for p in POSTS:
        write(p["path"], page_post(p))
    # logo + favicon
    logo = mark_svg().replace(' class="brand-mark"', ' xmlns="http://www.w3.org/2000/svg"')
    write("/favicon.svg", logo)
    write("/assets/img/logo.svg", logo)
    # sitemap
    urls = [(u, TODAY) for u in pages] + [(p["path"], p["updated"]) for p in POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls]
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", f"User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    print(f"built {len(pages) + len(POSTS) + 1} pages into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
