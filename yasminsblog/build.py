#!/usr/bin/env python3
"""Build the yasminsblog.com static site into ./public.

    python3 build.py && python3 validate.py

Standard library only, plus Pillow (optional) for the Open Graph PNGs.
"""
import html
import json
import os
import random
import shutil
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone

from content import SITE, CATEGORIES, TAGS, POSTS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
HOST = SITE["host"]
UPDATED = SITE["updated"]
VERSION = UPDATED.replace("-", "")

esc = html.escape

PALETTES = [
    ("#f6efe4", "#e8553a", "#1f3a5f", "#f2b134", "#14110f"),   # pastrami & mustard
    ("#efe7ff", "#6b3b5b", "#ff7a59", "#2b2d42", "#ffd166"),   # neon dusk
    ("#e9f3ef", "#1f6f6a", "#f2b134", "#e8553a", "#14110f"),   # subway tile
    ("#fff1e6", "#d62246", "#4b88a2", "#f4b942", "#1b1b1e"),   # candy store
    ("#f3f0e8", "#2d6a4f", "#e76f51", "#264653", "#e9c46a"),   # lemon grove
    ("#fdf0d5", "#c1121f", "#003049", "#669bbc", "#780000"),   # diner
]

NAV = [("Home", "/"), ("Journal", "/mamablog"), ("Food", "/mamablog/category/Food"),
       ("Culture", "/mamablog/category/Culture"), ("Photography", "/mamablog/category/Photography"),
       ("About", "/about")]


def slug_of(p):
    return p["path"].rsplit("/", 1)[-1]


def pal_for(key):
    return PALETTES[sum(map(ord, key)) % len(PALETTES)]


# --------------------------------------------------------------- cover art
def cover_svg(key, title="", variant=0, cls="cover"):
    """Seeded Bauhaus-style composition: unique per post, no stock photos."""
    rnd = random.Random(f"{key}:{variant}")
    bg, a, b, c, ink = pal_for(key + str(variant))
    W, H = 1200, 800
    s = [f'<svg class="{cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">',
         f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    # big disc
    cx, cy, r = rnd.randint(250, 950), rnd.randint(200, 600), rnd.randint(220, 360)
    s.append(f'<circle class="sh s1" cx="{cx}" cy="{cy}" r="{r}" fill="{a}"/>')
    # half disc
    hx, hy, hr = rnd.randint(100, 1100), rnd.choice([0, H]), rnd.randint(160, 300)
    sweep = 1 if hy == H else 0
    s.append(f'<path class="sh s2" d="M{hx-hr} {hy} A{hr} {hr} 0 0 {sweep} {hx+hr} {hy} Z" fill="{b}"/>')
    # stripes
    sx, sy = rnd.randint(0, 900), rnd.randint(0, 600)
    for i in range(rnd.randint(4, 7)):
        s.append(f'<rect class="sh s3" x="{sx}" y="{sy + i*26}" width="{rnd.randint(180, 320)}" height="11" rx="5" fill="{ink}"/>')
    # dot grid
    gx, gy = rnd.randint(40, 1000), rnd.randint(40, 640)
    dots = "".join(f'<circle cx="{gx + i*28}" cy="{gy + j*28}" r="5"/>' for i in range(6) for j in range(4))
    s.append(f'<g class="sh s4" fill="{c}">{dots}</g>')
    # quarter arc ring
    ax, ay, ar = rnd.randint(200, 1000), rnd.randint(150, 650), rnd.randint(90, 170)
    s.append(f'<circle class="sh s5" cx="{ax}" cy="{ay}" r="{ar}" fill="none" stroke="{c}" stroke-width="34" stroke-dasharray="{int(ar*1.6)} {int(ar*5)}"/>')
    # squiggle
    px, py = rnd.randint(80, 700), rnd.randint(120, 700)
    d = f"M{px} {py} " + " ".join(f"q 40 {(-1)**k * 60} 80 0" for k in range(rnd.randint(4, 6)))
    s.append(f'<path class="sh s6" d="{d}" fill="none" stroke="{ink}" stroke-width="14" stroke-linecap="round"/>')
    s.append("</svg>")
    return "".join(s)


def og_png(key, title, dest):
    """1200x630 share image: same palette and shapes, plus the title."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    rnd = random.Random(f"{key}:0")
    bg, a, b, c, ink = pal_for(key + "0")
    im = Image.new("RGB", (1200, 630), bg)
    d = ImageDraw.Draw(im)
    cx, cy, r = rnd.randint(700, 1050), rnd.randint(150, 480), rnd.randint(200, 300)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    hr = rnd.randint(140, 220)
    d.pieslice([900 - hr, 630 - hr, 900 + hr, 630 + hr], 180, 360, fill=b)
    for i in range(6):
        d.rounded_rectangle([60, 470 + i * 22, 300, 479 + i * 22], 4, fill=ink)
    for i in range(6):
        for j in range(3):
            d.ellipse([820 + i * 26, 60 + j * 26, 830 + i * 26, 70 + j * 26], fill=c)

    def font(size, bold=True):
        for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                  "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"):
            if os.path.exists(f):
                return ImageFont.truetype(f, size)
        return ImageFont.load_default()

    words, lines, cur, ft = title.split(), [], "", font(58)
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=ft) > 700 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    lines = lines[:4]
    pad = 18
    y = 70
    d.text((60, 40 - 10), "YASMIN'S BLOG", font=font(26, False), fill=ink)
    for ln in lines:
        w = d.textlength(ln, font=ft)
        d.rectangle([60 - 8, y + 20, 60 + w + 8, y + 76 + 8], fill=bg)
        d.text((60, y + 18), ln, font=ft, fill=ink)
        y += 76 + pad
    im.save(dest, "PNG", optimize=True)
    return True


# --------------------------------------------------------------- layout
def jsonld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs)


ORG = {"@type": "Organization", "@id": HOST + "/#org", "name": SITE["name"], "url": HOST + "/",
       "logo": {"@type": "ImageObject", "url": HOST + "/assets/img/logo-512.png"}}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "@id": HOST + "/#website", "url": HOST + "/",
           "name": SITE["name"], "description": SITE["description"], "publisher": {"@id": HOST + "/#org"},
           "inLanguage": "en-US"}


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": HOST + u} for i, (n, u) in enumerate(items)]}


def page(*, path, title, description, body, schema=(), og_image="/assets/img/og-default.png",
         og_type="website", body_class="", extra_head=""):
    canonical = HOST + (path if path != "/" else "/")
    nav = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if (u == path or (u != "/" and path.startswith(u + "/"))) else ""}>{n}</a></li>'
        for n, u in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{HOST}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14110f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/logo-180.png">
<link rel="alternate" type="application/rss+xml" title="{SITE['name']}" href="/mamablog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..900,0..100;1,9..144,300..900,0..100&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
<script>try{{var t=localStorage.getItem('yb-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{extra_head}{jsonld(*schema)}
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/" aria-label="{SITE['name']} home"><span class="brand-mark" aria-hidden="true"></span><span>Yasmin's<em>Blog</em></span></a>
    <nav class="nav" aria-label="Main"><ul>{nav}</ul></nav>
    <div class="header-tools">
      <button class="theme-toggle" type="button" aria-label="Toggle dark mode"><span aria-hidden="true"></span></button>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-big" aria-hidden="true">Yasmin's Blog</div>
    <div class="footer-grid">
      <div><p class="footer-lede">{esc(SITE['description'])}</p></div>
      <div><h2>Read</h2><ul>{''.join(f'<li><a href="/mamablog/category/{k}">{k}</a></li>' for k in CATEGORIES)}<li><a href="/mamablog">All posts</a></li></ul></div>
      <div><h2>Site</h2><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy-policy">Privacy</a></li><li><a href="/mamablog/feed.xml">RSS</a></li></ul></div>
    </div>
    <p class="fine">&copy; {date.today().year} {SITE['name']}. Independent and reader-supported.</p>
  </div>
</footer>
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------- components
def fmt_cats(p):
    return f'<a class="chip" href="/mamablog/category/{p["category"]}">{p["category"]}</a>'


def card(p, big=False, i=0):
    return f"""<article class="card reveal{' card-big' if big else ''}" data-cat="{p['category']}" style="--d:{(i % 3) * 80}ms" data-search="{esc((p['title'] + ' ' + p['description']).lower())}">
  <a class="card-link" href="{p['path']}" aria-label="{esc(p['title'])}"></a>
  <div class="card-art tilt">{cover_svg(slug_of(p), p['title'])}</div>
  <div class="card-body">
    <div class="meta">{fmt_cats(p)}<span>{p['read']} min read</span></div>
    <h3>{esc(p['h1'])}</h3>
    <p>{esc(p['dek'])}</p>
  </div>
</article>"""


def grid(posts, cls=""):
    return f'<div class="grid {cls}">' + "".join(card(p, i=i) for i, p in enumerate(posts)) + "</div>"


def marquee(items):
    row = "".join(f"<span>{esc(x)}</span><i aria-hidden='true'>✦</i>" for x in items)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{row}{row}</div></div>'


def hero_small(kicker, h1, lede, key):
    return f"""<section class="hero-small">
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="wrap">
    <p class="kicker reveal">{kicker}</p>
    <h1 class="reveal display">{h1}</h1>
    <p class="lede reveal">{lede}</p>
  </div>
</section>"""


# --------------------------------------------------------------- pages
def write(path, content):
    if path == "/":
        dest = os.path.join(OUT, "home.html")
    elif path == "/mamablog/feed.xml":
        dest = os.path.join(OUT, "_pages", "mamablog", "feed.xml")
    elif path.endswith(".html") or path.endswith(".xml") or path.endswith(".txt"):
        dest = os.path.join(OUT, path.lstrip("/"))
    else:
        # Pages live in _pages/<path>.html, NOT <path>/index.html: the host's web
        # server 301s any URL matching a real directory to a trailing-slash form
        # before PHP runs, which would break the slash-less legacy URLs.
        dest = os.path.join(OUT, "_pages", path.lstrip("/") + ".html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)


def build_home():
    feat = POSTS[0]
    rest = [p for p in POSTS if p is not feat]
    photo_posts = [p for p in POSTS if p.get("photos")]
    cats = "".join(f"""<a class="cat-tile reveal" href="/mamablog/category/{k}" style="--d:{i*90}ms">
      <span class="cat-num">0{i+1}</span><span class="cat-name">{k}</span><span class="cat-desc">{esc(v)}</span>
      <span class="cat-count">{sum(1 for p in POSTS if p['category']==k)} stories →</span></a>""" for i, (k, v) in enumerate(CATEGORIES.items()))
    strip = "".join(f'<figure class="strip-item reveal" style="--d:{i*70}ms">{cover_svg(slug_of(p), cap, variant=i+1)}<figcaption>{esc(cap)}</figcaption></figure>'
                    for p in photo_posts for i, (cap, _) in enumerate(p["photos"]))
    body = f"""
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="grain"></div></div>
  <div class="wrap hero-grid">
    <div>
      <p class="kicker reveal">Est. on the Lower East Side · Food · Culture · Photos</p>
      <h1 class="display hero-title reveal">New York, <span class="ital">one</span> plate, one story, <span class="hl">one frame</span> at a time.</h1>
      <p class="lede reveal">{esc(SITE['description'])} Pastrami and pole dancing, century-old coffee merchants and the dollar slice at 2&nbsp;a.m.</p>
      <div class="cta-row reveal"><a class="btn" href="/mamablog">Read the journal</a><a class="btn ghost" href="{feat['path']}">Featured story →</a></div>
    </div>
    <div class="hero-art reveal" aria-hidden="true">
      <div class="hero-stack">
        {''.join(f'<div class="stack-card sc{i}">{cover_svg(slug_of(p), p["title"])}<span>{esc(p["category"])}</span></div>' for i, p in enumerate(POSTS[1:4]))}
      </div>
      <div class="badge"><svg viewBox="0 0 200 200"><defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text><textPath href="#circ">NEW YORK · FOOD · CULTURE · PHOTOGRAPHY · </textPath></text></svg><span>✦</span></div>
    </div>
  </div>
</section>
{marquee(['Katz’s pastrami', 'Bleecker Street beans', 'Yunnan mixian', 'The dollar slice', 'Economy Candy', 'Subway portraits', 'Hand-poke tattoos', 'Catland', 'Photoville', 'Green Lanes', 'Frenchmen Street', 'Salerno'])}
<section class="section">
  <div class="wrap">
    <div class="feature reveal">
      <a class="card-link" href="{feat['path']}" aria-label="{esc(feat['title'])}"></a>
      <div class="feature-art tilt">{cover_svg(slug_of(feat), feat['title'])}</div>
      <div class="feature-body">
        <p class="kicker">Featured · {feat['category']}</p>
        <h2 class="display">{esc(feat['h1'])}</h2>
        <p>{esc(feat['dek'])}</p>
        <span class="read-more">Read the story <b>→</b></span>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display">Latest from the journal</h2><a href="/mamablog">All {len(POSTS)} posts →</a></div>
    {grid(rest[:6])}
  </div>
</section>
<section class="section dark">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display">Four sections, one city</h2></div>
    <div class="cat-grid">{cats}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display">The “4 Photos” series</h2><a href="/mamablog/category/Photography">Photography →</a></div>
  </div>
  <div class="strip">{strip}</div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display">From the archive</h2></div>
    {grid(rest[6:12])}
  </div>
</section>
<section class="section cta-band">
  <div class="wrap reveal">
    <h2 class="display">Got a tip on a great New York spot?</h2>
    <p>Old-school deli, new noodle counter or a shop that's been there since your grandparents' time: tell us about it.</p>
    <a class="btn" href="/contact">Send a tip</a>
  </div>
</section>"""
    write("/", page(path="/", title=f"{SITE['name']} | {SITE['tagline']}",
                    description="Yasmin's Blog: an independent New York journal on food institutions, neighborhood shops, culture and street photography, from Katz's pastrami to the dollar slice.",
                    body=body, body_class="home",
                    schema=[WEBSITE, {"@context": "https://schema.org", **ORG},
                            {"@context": "https://schema.org", "@type": "Blog", "@id": HOST + "/mamablog#blog", "name": SITE["name"], "url": HOST + "/mamablog",
                             "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": HOST + p["path"]} for p in POSTS]}]))


def build_index():
    chips = '<button class="filter on" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{k}">{k}</button>' for k in CATEGORIES)
    body = hero_small("The journal", "All stories", "Every post on Yasmin's Blog: food, culture, photography and travel. Filter by section or search.", "journal") + f"""
<section class="section tight">
  <div class="wrap">
    <div class="toolbar reveal"><div class="filters" role="group" aria-label="Filter by section">{chips}</div>
    <label class="search"><span class="sr">Search posts</span><input type="search" placeholder="Search pastrami, ramen, tattoos…" data-search-input></label></div>
    {grid(POSTS, 'filterable')}
    <p class="empty" hidden>No posts match that search.</p>
  </div>
</section>"""
    write("/mamablog", page(path="/mamablog", title=f"The Journal: All Posts | {SITE['name']}",
                            description="Browse every Yasmin's Blog post: New York food institutions, culture features, photo essays and short travel guides.",
                            body=body,
                            schema=[crumbs([("Home", "/"), ("Journal", "/mamablog")]),
                                    {"@context": "https://schema.org", "@type": "CollectionPage", "name": "The Journal", "url": HOST + "/mamablog",
                                     "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": HOST + p["path"]} for i, p in enumerate(POSTS)]}}]))


def build_collection(path, kicker, h1, lede, posts, title, desc, crumb):
    body = hero_small(kicker, esc(h1), esc(lede), path) + f"""
<section class="section tight"><div class="wrap">{grid(posts)}
<p class="back reveal"><a href="/mamablog">← Back to all posts</a></p></div></section>"""
    write(path, page(path=path, title=title, description=desc, body=body,
                     schema=[crumbs(crumb), {"@context": "https://schema.org", "@type": "CollectionPage", "name": h1, "url": HOST + path,
                                             "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": HOST + p["path"]} for i, p in enumerate(posts)]}}]))


def build_post(p, idx):
    slug = slug_of(p)
    og = f"/assets/img/og/{slug}.png"
    have_og = og_png(slug, p["title"], os.path.join(OUT, og.lstrip("/")))
    photos = ""
    if p.get("photos"):
        photos = '<div class="plates">' + "".join(
            f'<figure class="plate reveal" style="--d:{i*80}ms"><div class="plate-art tilt">{cover_svg(slug, cap, variant=i+1)}<span class="plate-no">{i+1}/4</span></div><figcaption><strong>{esc(cap)}</strong> {esc(txt)}</figcaption></figure>'
            for i, (cap, txt) in enumerate(p["photos"])) + "</div>"
    faq_html, faq_schema = "", []
    if p.get("faq"):
        faq_html = '<section class="faq"><h2>FAQ</h2>' + "".join(
            f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in p["faq"]) + "</section>"
        faq_schema = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]
    tags = "".join(f'<a class="chip" href="/mamablog/tag/{t}">#{esc(TAGS[t]["label"])}</a>' for t in p["tags"])
    related = [q for q in POSTS if q is not p and q["category"] == p["category"]][:3]
    if len(related) < 3:
        related += [q for q in POSTS if q is not p and q not in related][:3 - len(related)]
    prev_p, next_p = POSTS[(idx + 1) % len(POSTS)], POSTS[idx - 1]
    body = f"""
<article class="post">
  <header class="post-hero">
    <div class="post-hero-art" aria-hidden="true">{cover_svg(slug, p['title'], cls='cover parallax')}</div>
    <div class="wrap narrow post-hero-text">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/mamablog">Journal</a> / <a href="/mamablog/category/{p['category']}">{p['category']}</a></nav>
      <h1 class="display reveal">{esc(p['h1'])}</h1>
      <p class="dek reveal">{esc(p['dek'])}</p>
      <div class="meta reveal">{fmt_cats(p)}<span>{p['read']} min read</span><span>Updated <time datetime="{UPDATED}">{datetime.strptime(UPDATED, '%Y-%m-%d').strftime('%B %-d, %Y')}</time></span></div>
    </div>
  </header>
  <div class="wrap narrow prose">
    {p['body']}
    {photos}
    {p.get('after', '')}
    {faq_html}
    <div class="post-tags">{tags}</div>
    <nav class="pager" aria-label="More posts">
      <a href="{prev_p['path']}"><span>Previous</span>{esc(prev_p['h1'])}</a>
      <a href="{next_p['path']}"><span>Next</span>{esc(next_p['h1'])}</a>
    </nav>
  </div>
</article>
<section class="section"><div class="wrap"><div class="section-head reveal"><h2 class="display">Keep reading</h2></div>{grid(related)}</div></section>"""
    schema = [crumbs([("Home", "/"), ("Journal", "/mamablog"), (p["category"], f"/mamablog/category/{p['category']}"), (p["h1"], p["path"])]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"][:110], "description": p["description"],
               "mainEntityOfPage": HOST + p["path"], "url": HOST + p["path"], "datePublished": UPDATED, "dateModified": UPDATED,
               "image": HOST + (og if have_og else "/assets/img/og-default.png"), "articleSection": p["category"],
               "keywords": p["keyword"], "author": {"@id": HOST + "/#org"}, "publisher": ORG, "inLanguage": "en-US"},
              *faq_schema]
    write(p["path"], page(path=p["path"], title=f"{p['title']} | {SITE['name']}" if len(p["title"]) < 52 else p["title"],
                          description=p["description"], body=body, schema=schema, og_type="article",
                          og_image=og if have_og else "/assets/img/og-default.png", body_class="post-page",
                          extra_head=f'<meta property="article:modified_time" content="{UPDATED}">\n'))


def build_static_pages():
    about = hero_small("About", "About Yasmin's Blog", "An independent journal about the places, people and plates that make New York feel like home.", "about") + f"""
<section class="section tight"><div class="wrap narrow prose reveal">
<p><strong>Yasmin's Blog</strong> covers New York City through its food institutions, neighborhood shops, culture and street photography. We write about the places that have outlasted every trend, like a deli carving pastrami since 1888 or a coffee merchant on Bleecker Street since 1907. We also write about the communities and scenes that keep reinventing the city.</p>
<h2>What we cover</h2>
<ul>{''.join(f'<li><strong><a href="/mamablog/category/{k}">{k}</a>:</strong> {esc(v)}</li>' for k, v in CATEGORIES.items())}</ul>
<h2>How we work</h2>
<p>Our guides are written and fact-checked by the Yasmin's Blog editorial team. We do not accept payment for coverage. Restaurants and shops change hours, prices and even locations, so we note when a place has closed and recommend checking current details before you visit. Spotted something out of date? <a href="/contact">Tell us</a>.</p>
<h2>A note on this site</h2>
<p>Yasmin's Blog relaunched in 2026 as an independently operated publication. Older URLs from the site's archive have been kept and given new, updated articles on the same subjects. The current site is not affiliated with, and does not speak for, any previous owner or contributor of the domain.</p>
</div></section>"""
    write("/about", page(path="/about", title=f"About | {SITE['name']}", description="About Yasmin's Blog, an independent New York journal on food institutions, neighborhood culture and street photography.",
                         body=about, schema=[crumbs([("Home", "/"), ("About", "/about")]), {"@context": "https://schema.org", "@type": "AboutPage", "url": HOST + "/about", "publisher": ORG}]))

    contact = hero_small("Contact", "Say hello", "Tips, corrections and story ideas are always welcome.", "contact") + f"""
<section class="section tight"><div class="wrap narrow prose reveal">
<div class="contact-card">
<p>The best way to reach the editors is by email:</p>
<p class="big-link"><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
<p>Tell us about a New York spot worth covering, a place that has closed or changed, or anything we got wrong. We read everything, but we can't reply to every message.</p>
</div>
<h2>Corrections</h2>
<p>If a post contains a factual error, email us with the URL and the correction, and we'll update the article.</p>
</div></section>"""
    write("/contact", page(path="/contact", title=f"Contact | {SITE['name']}", description="Contact Yasmin's Blog with New York food and culture tips, corrections and story ideas.",
                           body=contact, schema=[crumbs([("Home", "/"), ("Contact", "/contact")]), {"@context": "https://schema.org", "@type": "ContactPage", "url": HOST + "/contact"}]))

    privacy = hero_small("Legal", "Privacy policy", f"Last updated {datetime.strptime(UPDATED, '%Y-%m-%d').strftime('%B %-d, %Y')}.", "privacy") + """
<section class="section tight"><div class="wrap narrow prose">
<p>Yasmin's Blog is a static website. We do not run user accounts, comments or advertising trackers, and we do not sell personal information.</p>
<h2>What is collected</h2>
<p>Our web host keeps standard server logs (IP address, browser type, pages requested and timestamps) for security and performance. Fonts are loaded from Google Fonts, which receives your IP address when serving them. Your light/dark theme preference is stored only in your own browser.</p>
<h2>Email</h2>
<p>If you email us, we use your address only to read and respond to your message.</p>
<h2>Links</h2>
<p>Posts link to other websites. Their privacy practices are their own.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:hello@yasminsblog.com">hello@yasminsblog.com</a>.</p>
</div></section>"""
    write("/privacy-policy", page(path="/privacy-policy", title=f"Privacy Policy | {SITE['name']}", description="The Yasmin's Blog privacy policy: what our static site collects and how it is used.",
                                  body=privacy, schema=[crumbs([("Home", "/"), ("Privacy policy", "/privacy-policy")])]))

    nf = f"""<section class="hero-small notfound"><div class="blob b1"></div><div class="blob b2"></div><div class="wrap">
<p class="kicker">Error 404</p><h1 class="display">This page took the wrong train.</h1>
<p class="lede">The page you're after isn't here. It may have moved when the site was rebuilt.</p>
<div class="cta-row"><a class="btn" href="/">Go home</a><a class="btn ghost" href="/mamablog">Browse all posts</a></div></div></section>
<section class="section tight"><div class="wrap"><div class="section-head"><h2 class="display">Popular stories</h2></div>{grid(POSTS[:3])}</div></section>"""
    html_404 = page(path="/404", title=f"Page not found | {SITE['name']}", description="This page could not be found on Yasmin's Blog. Browse the journal or head back to the homepage.", body=nf)
    write("/404.html", html_404.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"'))


def build_feeds():
    urls = ["/", "/mamablog", "/about", "/contact", "/privacy-policy"] + [p["path"] for p in POSTS] + \
           [f"/mamablog/category/{k}" for k in CATEGORIES] + [f"/mamablog/tag/{t}" for t in TAGS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{esc(HOST + u)}</loc><lastmod>{UPDATED}</lastmod></url>" for u in urls]
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /_pages/\n\nSitemap: {HOST}/sitemap.xml\n")
    pub = format_datetime(datetime.strptime(UPDATED, "%Y-%m-%d").replace(tzinfo=timezone.utc))
    items = "".join(f"""<item><title>{esc(p['title'])}</title><link>{HOST}{p['path']}</link><guid>{HOST}{p['path']}</guid><pubDate>{pub}</pubDate><category>{p['category']}</category><description>{esc(p['description'])}</description></item>""" for p in POSTS)
    write("/mamablog/feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>{SITE['name']}</title><link>{HOST}/mamablog</link><description>{esc(SITE['description'])}</description><language>en-us</language><lastBuildDate>{pub}</lastBuildDate>{items}</channel></rss>
""")


def build_assets():
    shutil.copytree(os.path.join(ROOT, "static"), OUT, dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/img/og"), exist_ok=True)
    og_png("yasmins-blog-home", "New York food, culture & photography", os.path.join(OUT, "assets/img/og-default.png"))
    try:
        from PIL import Image, ImageDraw
        for size in (180, 512):
            im = Image.new("RGB", (size, size), "#14110f")
            d = ImageDraw.Draw(im)
            r = size * 0.32
            d.ellipse([size * .5 - r - size * .08, size * .5 - r, size * .5 + r - size * .08, size * .5 + r], fill="#e8553a")
            d.rectangle([size * .56, size * .26, size * .72, size * .74], fill="#f2b134")
            im.save(os.path.join(OUT, f"assets/img/logo-{size}.png"), "PNG", optimize=True)
    except ImportError:
        pass


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_assets()
    build_home()
    build_index()
    for i, p in enumerate(POSTS):
        build_post(p, i)
    for k, v in CATEGORIES.items():
        posts = [p for p in POSTS if p["category"] == k]
        build_collection(f"/mamablog/category/{k}", "Section", k, v, posts,
                         f"{k} | {SITE['name']}", f"{k} stories from Yasmin's Blog. {v}"[:158],
                         [("Home", "/"), ("Journal", "/mamablog"), (k, f"/mamablog/category/{k}")])
    for t, meta in TAGS.items():
        posts = [p for p in POSTS if t in p["tags"]]
        build_collection(f"/mamablog/tag/{t}", "Tag", meta["label"], meta["intro"], posts,
                         f"{meta['label']}: Posts Tagged | {SITE['name']}", meta["intro"][:158],
                         [("Home", "/"), ("Journal", "/mamablog"), (meta["label"], f"/mamablog/tag/{t}")])
    build_static_pages()
    build_feeds()
    n = sum(len(f) for _, _, f in os.walk(OUT))
    print(f"built {len(POSTS)} posts, {len(CATEGORIES)} categories, {len(TAGS)} tags -> {OUT} ({n} files)")


if __name__ == "__main__":
    main()
