#!/usr/bin/env python3
"""Static site generator for the live-style.co.uk rebuild.

Reads article modules from content/posts_*.py (each defines POSTS; posts_d.py
also defines TAG_INTROS and CATEGORY_INTROS) and writes the whole site into
public/, which is what gets deployed. Standard library only.

    python3 build.py && python3 validate.py
"""

import glob
import html
import importlib.util
import json
import os
import re
import shutil
from datetime import date

from siteconfig import CATEGORIES, CATEGORY_BY_NAME, CATEGORY_IMAGES, NAV, SITE, TODAY

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = SITE["origin"]
NAME = SITE["name"]
ASSET_V = TODAY.replace("-", "")
esc = html.escape


# --------------------------------------------------------------------------- content

def load_content():
    posts, tag_intros, cat_intros = [], {}, {}
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "posts_*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        posts.extend(mod.POSTS)
        tag_intros.update(getattr(mod, "TAG_INTROS", {}))
        cat_intros.update(getattr(mod, "CATEGORY_INTROS", {}))
    for p in posts:
        p["cat_slug"] = CATEGORY_BY_NAME[p["category"]]
        p["tag_slugs"] = [(slugify(t), t) for t in p["tags"]]
        p["words"] = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
        p["read"] = max(2, round(p["words"] / 220))
    posts.sort(key=lambda p: (p["date"], p["path"]), reverse=True)
    return posts, tag_intros, cat_intros


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("&", "")).strip("-")


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def img(name, alt, cls="", sizes="100vw", eager=False, thumb_only=False):
    """<img> with a 720px thumb and the 1600px original as srcset candidates."""
    full, thumb = f"/assets/img/{name}", f"/assets/img/thumbs/{name}"
    src = thumb if thumb_only else full
    srcset = f'{thumb} 720w, {full} 1600w'
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{src}" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" {loading}>'


# --------------------------------------------------------------------------- layout

def head(title, description, path, og_image="hero-living-room.jpg", og_type="website", extra="", schema=None, noindex=False):
    canonical = ORIGIN + path
    ld = ""
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="{SITE['locale']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
{extra}<meta name="theme-color" content="#f5efe6">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{ld}
</head>
"""


def header(path):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if path.startswith(href) else ""
        links.append(f'<li><a href="{href}"{cur}>{esc(label)}</a></li>')
    links = "\n".join(links)
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" data-header>
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark">L</span><span class="logo-word">Live<em>-</em>Style</span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
{links}
      </ul>
      <a class="nav-cta" href="/contact/">Get in touch</a>
    </nav>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu" data-nav-toggle>
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<main id="main">
"""


def footer():
    cats = "".join(f'<li><a href="/category/{s}/">{esc(n)}</a></li>' for s, n in CATEGORIES)
    year = TODAY[:4]
    return f"""</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="logo logo-light" href="/"><span class="logo-mark">L</span><span class="logo-word">Live<em>-</em>Style</span></a>
      <p>{esc(SITE['tagline'])}. A London-born journal of homes, makers, art and the small pleasures that make a place feel like yours.</p>
      <p><a class="footer-mail" href="mailto:{SITE['email']}">{SITE['email']}</a></p>
    </div>
    <div>
      <h2 class="footer-h">Sections</h2>
      <ul class="footer-list">{cats}</ul>
    </div>
    <div>
      <h2 class="footer-h">The site</h2>
      <ul class="footer-list">
        <li><a href="/journal/">All stories</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>&copy; {SITE['founded']}&ndash;{year} {NAME}. All rights reserved.</p>
    <a class="to-top" href="#main">Back to top &uarr;</a>
  </div>
</footer>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
"""


def page(path, title, description, body, **kw):
    return head(title, description, path, **kw) + header(path) + body + footer()


def write(path, content):
    """path is the URL path; '/' becomes home.html (served by index.php)."""
    if path == "/":
        dest = os.path.join(OUT, "home.html")
    elif path.endswith("/"):
        dest = os.path.join(OUT, path.strip("/"), "index.html")
    else:
        dest = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------- schema

PUBLISHER = {
    "@type": "Organization",
    "@id": ORIGIN + "/#org",
    "name": NAME,
    "url": ORIGIN + "/",
    "email": SITE["email"],
    "logo": {"@type": "ImageObject", "url": ORIGIN + "/favicon.svg"},
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": NAME, "url": ORIGIN + "/",
           "description": SITE["tagline"], "inLanguage": "en-GB", "publisher": {"@id": ORIGIN + "/#org"}}


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(items)]}


def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": [PUBLISHER, WEBSITE, *nodes]}


def breadcrumb_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


# --------------------------------------------------------------------------- components

def card(p, size="", eager=False):
    cat = dict(CATEGORIES)[p["cat_slug"]]
    cls = f"card {size}".strip()
    return f"""<article class="{cls} reveal">
  <a class="card-media" href="{p['path']}" tabindex="-1" aria-hidden="true">{img(p['image'], p['image_alt'], sizes='(max-width: 700px) 100vw, 33vw', eager=eager)}</a>
  <div class="card-body">
    <p class="kicker"><a href="/category/{p['cat_slug']}/">{esc(cat)}</a><span>&middot;</span><time datetime="{p['date']}">{nice_date(p['date'])}</time></p>
    <h3 class="card-title"><a href="{p['path']}">{esc(p['title'])}</a></h3>
    <p class="card-excerpt">{esc(p['excerpt'])}</p>
  </div>
</article>"""


def grid(posts, cls="grid"):
    return f'<div class="{cls}">' + "\n".join(card(p) for p in posts) + "</div>"


def cta_band():
    return f"""<section class="cta-band reveal">
  <div class="wrap cta-inner">
    <div>
      <p class="eyebrow">Say hello</p>
      <h2>Got a home, a maker or a find we should see?</h2>
      <p>We love hearing about independent designers, clever renovations and London spots worth the journey.</p>
    </div>
    <a class="btn btn-light magnetic" href="mailto:{SITE['email']}">{SITE['email']}</a>
  </div>
</section>"""


# --------------------------------------------------------------------------- pages

def build_home(posts):
    by_path = {p["path"]: p for p in posts}
    featured_paths = [
        "/2013/06/30/open-shelving-in-kitchens/",
        "/2014/03/28/comic-art-ltd-by-john-patrick-reynolds/",
        "/2015/07/16/final-paint-selections/",
    ]
    feat = [by_path[x] for x in featured_paths if x in by_path]
    lead, side = feat[0], feat[1:]
    latest = [p for p in posts if p["path"] not in featured_paths][:6]

    ticker_items = "".join(f'<a href="/category/{s}/">{esc(n)}</a><span aria-hidden="true">&#10022;</span>' for s, n in CATEGORIES)

    tiles = []
    for s, n in CATEGORIES[:6]:
        count = sum(1 for p in posts if p["cat_slug"] == s)
        tiles.append(f"""<a class="tile reveal" href="/category/{s}/">
  {img(CATEGORY_IMAGES[s], n + ' stories on Live-Style', sizes='(max-width: 700px) 50vw, 33vw', thumb_only=True)}
  <span class="tile-label"><span class="tile-name">{esc(n)}</span><span class="tile-count">{count} stories</span></span>
</a>""")

    reno = [p for p in posts if p["cat_slug"] == "renovation-diary"][:3]
    reno_list = "".join(f'<li><a href="{p["path"]}"><span class="num">0{i+1}</span>{esc(p["title"])}</a></li>' for i, p in enumerate(reno))
    cure = [p for p in posts if p["cat_slug"] == "january-cure"]
    cure_links = "".join(f'<li><a href="{p["path"]}">{esc(p["title"])} &rarr;</a></li>' for p in cure)

    side_html = "\n".join(card(p, "card-row") for p in side)
    body = f"""
<section class="hero" data-hero>
  <div class="hero-media" data-parallax>
    {img('hero-living-room.jpg', 'Sunlit modern living room with a low sofa, terracotta stools and tall plants', eager=True)}
  </div>
  <div class="hero-shade"></div>
  <div class="blob blob-a" aria-hidden="true"></div><div class="blob blob-b" aria-hidden="true"></div>
  <div class="wrap hero-content">
    <p class="eyebrow hero-in" style="--d:0">Est. {SITE['founded']} &middot; London</p>
    <h1 class="hero-title"><span class="line hero-in" style="--d:1">Homes, makers</span> <span class="line hero-in" style="--d:2">&amp; <em>the art of</em></span> <span class="line hero-in" style="--d:3">living well.</span></h1>
    <p class="hero-sub hero-in" style="--d:4">Live-Style is an interiors and lifestyle journal: real renovations, independent designers, prints worth framing and the London places we keep going back to.</p>
    <div class="hero-actions hero-in" style="--d:5">
      <a class="btn magnetic" href="/journal/">Read the journal</a>
      <a class="btn btn-ghost" href="/category/renovation-diary/">The renovation diary</a>
    </div>
  </div>
  <a class="scroll-cue" href="#featured" aria-label="Scroll to featured stories"><span></span></a>
</section>

<div class="ticker" aria-label="Sections">
  <div class="ticker-track">{ticker_items}{ticker_items}</div>
</div>

<section class="section" id="featured">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Most read</p>
      <h2>Stories readers keep coming back to</h2>
    </div>
    <div class="featured">
      <article class="feature-lead reveal">
        <a class="feature-media tilt" href="{lead['path']}" tabindex="-1" aria-hidden="true">{img(lead['image'], lead['image_alt'], sizes='(max-width: 900px) 100vw, 60vw')}</a>
        <div class="feature-body">
          <p class="kicker"><a href="/category/{lead['cat_slug']}/">{esc(lead['category'])}</a><span>&middot;</span>{lead['read']} min read</p>
          <h3 class="feature-title"><a href="{lead['path']}">{esc(lead['title'])}</a></h3>
          <p>{esc(lead['excerpt'])}</p>
          <a class="link-arrow" href="{lead['path']}">Read the story</a>
        </div>
      </article>
      <div class="feature-side">
{side_html}
      </div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Explore</p>
      <h2>Find your corner of Live-Style</h2>
    </div>
    <div class="tiles">
{''.join(tiles)}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split-media reveal">
      <div class="stack">
        {img('little-greene-paint.jpg', 'Well-used paintbrushes with layers of colourful dried paint', cls='stack-a', sizes='(max-width: 900px) 80vw, 40vw')}
        {img('roger-oates-runner.jpg', 'Sunny hallway with herringbone floor, armchair and sideboard', cls='stack-b', sizes='(max-width: 900px) 60vw, 25vw')}
      </div>
    </div>
    <div class="split-copy reveal">
      <p class="eyebrow">Renovation diary</p>
      <h2>Paint charts, stair runners and the DIY that didn&rsquo;t quite work</h2>
      <p>Our own house project, told honestly: the colours we agonised over, the trades we trusted, and the jobs we&rsquo;d do differently next time.</p>
      <ol class="num-list">{reno_list}</ol>
      <a class="link-arrow" href="/category/renovation-diary/">All renovation stories</a>
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow">Fresh from the journal</p>
      <h2>Latest stories</h2>
    </div>
    {grid(latest)}
    <p class="center reveal"><a class="btn btn-light" href="/journal/">See every story</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap cure">
    <div class="cure-copy reveal">
      <p class="eyebrow">A new-year ritual</p>
      <h2>The January Cure, our way</h2>
      <p>Every January we sign up for Apartment Therapy&rsquo;s month-long home reset: one small job a day, a cleared-out cupboard at a time. Here&rsquo;s how we got on.</p>
      <ul class="plain-links">{cure_links}</ul>
    </div>
    <div class="cure-media reveal">
      {img('january-cure.jpg', 'Calm, decluttered white room with a black sofa, chest of drawers and floor lamp', sizes='(max-width: 900px) 100vw, 45vw')}
      <div class="badge-spin" aria-hidden="true"><svg viewBox="0 0 100 100"><defs><path id="c" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0"/></defs><text><textPath href="#c">declutter &middot; refresh &middot; repeat &middot; </textPath></text></svg></div>
    </div>
  </div>
</section>
{cta_band()}
"""
    schema = graph({"@type": "CollectionPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/",
                    "name": f"{NAME} | {SITE['tagline']}", "isPartOf": {"@id": ORIGIN + "/#website"},
                    "about": "Interiors, design, art and lifestyle"})
    write("/", page("/", f"{NAME} | Interiors, Design & Lifestyle Journal",
                    "Live-Style is a London interiors and lifestyle journal: renovation diaries, independent makers, art prints, design shopping and favourite places.",
                    body, schema=schema))


def related_for(p, posts, n=3):
    same = [q for q in posts if q is not p and q["cat_slug"] == p["cat_slug"]]
    tags = {t for t, _ in p["tag_slugs"]}
    shared = [q for q in posts if q is not p and q not in same and tags & {t for t, _ in q["tag_slugs"]}]
    rest = [q for q in posts if q is not p and q not in same and q not in shared]
    return (same + shared + rest)[:n]


def build_post(p, posts, idx):
    cat_name = dict(CATEGORIES)[p["cat_slug"]]
    items = [("Home", "/"), (cat_name, f"/category/{p['cat_slug']}/"), (p["title"], p["path"])]
    tags = "".join(f'<a href="/tag/{s}/">{esc(n)}</a>' for s, n in p["tag_slugs"])
    faq_html, faq_schema = "", None
    if p.get("faq"):
        qs = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p["faq"])
        faq_html = f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Questions readers ask</h2>{qs}</section>'
        faq_schema = {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    newer = posts[idx - 1] if idx > 0 else None
    older = posts[idx + 1] if idx + 1 < len(posts) else None
    pn = '<nav class="post-nav" aria-label="More stories">'
    pn += f'<a class="pn-prev" href="{older["path"]}"><span>Previous story</span>{esc(older["title"])}</a>' if older else "<span></span>"
    pn += f'<a class="pn-next" href="{newer["path"]}"><span>Next story</span>{esc(newer["title"])}</a>' if newer else "<span></span>"
    pn += "</nav>"
    related = related_for(p, posts)

    body = f"""
<article class="post">
  <header class="post-hero">
    <div class="post-hero-media" data-parallax>{img(p['image'], p['image_alt'], eager=True)}</div>
    <div class="post-hero-shade"></div>
    <div class="wrap post-hero-inner">
      {breadcrumb_html(items)}
      <p class="kicker light hero-in" style="--d:0"><a href="/category/{p['cat_slug']}/">{esc(cat_name)}</a><span>&middot;</span><time datetime="{p['date']}">{nice_date(p['date'])}</time><span>&middot;</span>{p['read']} min read</p>
      <h1 class="post-title hero-in" style="--d:1">{esc(p['title'])}</h1>
      <p class="post-standfirst hero-in" style="--d:2">{esc(p['excerpt'])}</p>
    </div>
  </header>
  <div class="wrap post-layout">
    <div class="prose">
{p['body']}
      {faq_html}
      <div class="post-tags">{tags}</div>
      <div class="share">
        <span>Share</span>
        <button type="button" class="chip" data-copy>Copy link</button>
        <a class="chip" href="mailto:?subject={esc(p['title'])}&amp;body={ORIGIN}{p['path']}">Email</a>
      </div>
    </div>
    <aside class="post-aside">
      <div class="aside-card">
        <p class="eyebrow">In this section</p>
        <ul>{''.join(f'<li><a href="{q["path"]}">{esc(q["title"])}</a></li>' for q in [x for x in posts if x["cat_slug"] == p["cat_slug"] and x is not p][:5]) or '<li><a href="/journal/">All stories</a></li>'}</ul>
      </div>
      <div class="aside-card aside-accent">
        <p class="eyebrow">Write to us</p>
        <p>Tips, makers, homes to feature: we read everything.</p>
        <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      </div>
    </aside>
  </div>
  <div class="wrap">{pn}</div>
</article>
<section class="section section-tint">
  <div class="wrap">
    <div class="section-head reveal"><p class="eyebrow">Keep reading</p><h2>You might also like</h2></div>
    {grid(related)}
  </div>
</section>
"""
    article = {
        "@type": "BlogPosting", "@id": ORIGIN + p["path"] + "#article", "headline": p["title"],
        "description": p["description"], "datePublished": p["date"], "dateModified": p.get("modified", TODAY),
        "image": ORIGIN + "/assets/img/" + p["image"], "mainEntityOfPage": ORIGIN + p["path"],
        "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"},
        "articleSection": cat_name, "keywords": ", ".join(p["tags"]), "wordCount": p["words"], "inLanguage": "en-GB",
    }
    nodes = [article, crumbs(items)] + ([faq_schema] if faq_schema else [])
    extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
             f'<meta property="article:section" content="{esc(cat_name)}">\n')
    write(p["path"], page(p["path"], f"{p['seo_title']} | {NAME}", p["description"], body,
                          og_image=p["image"], og_type="article", extra=extra, schema=graph(*nodes)))


def listing(path, title, h1, eyebrow, intro, items, posts, image, meta_desc, noindex=False):
    body = f"""
<header class="list-hero">
  <div class="list-hero-media" data-parallax>{img(image, h1, eager=True)}</div>
  <div class="post-hero-shade"></div>
  <div class="wrap list-hero-inner">
    {breadcrumb_html(items)}
    <p class="eyebrow light hero-in" style="--d:0">{esc(eyebrow)}</p>
    <h1 class="hero-in" style="--d:1">{esc(h1)}</h1>
    <p class="list-intro hero-in" style="--d:2">{esc(intro)}</p>
  </div>
</header>
<section class="section">
  <div class="wrap">
    <p class="count reveal">{len(posts)} {'story' if len(posts) == 1 else 'stories'}</p>
    {grid(posts)}
  </div>
</section>
{cta_band()}
"""
    schema = graph({"@type": "CollectionPage", "url": ORIGIN + path, "name": h1, "description": meta_desc,
                    "isPartOf": {"@id": ORIGIN + "/#website"},
                    "mainEntity": {"@type": "ItemList", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["path"]} for i, p in enumerate(posts)]}},
                   crumbs(items))
    write(path, page(path, title, meta_desc, body, og_image=image, schema=schema, noindex=noindex))


def indexable_tag(slug, posts, tag_intros):
    """Single-post tag pages are thin, so only the ones with an intro or 2+ posts are indexed."""
    return slug in tag_intros or len(posts) > 1


def build_listings(posts, tag_intros, cat_intros):
    listing("/journal/", f"The Journal: Every Story | {NAME}", "The journal", "Every story",
            "Everything we have published, newest first: interiors, makers, art, renovation notes, food and places.",
            [("Home", "/"), ("Journal", "/journal/")], posts, "home-green-study.jpg",
            "Browse every Live-Style story: interiors ideas, independent makers, art prints, our renovation diary, shopping edits and favourite places.")
    for slug, name in CATEGORIES:
        ps = [p for p in posts if p["cat_slug"] == slug]
        intro = cat_intros.get(slug, f"Stories filed under {name}.")
        listing(f"/category/{slug}/", f"{name} | {NAME}", name, "Section", intro,
                [("Home", "/"), (name, f"/category/{slug}/")], ps, CATEGORY_IMAGES[slug],
                trim(f"{name} on Live-Style: {intro}", 158))
    tags = {}
    for p in posts:
        for s, n in p["tag_slugs"]:
            tags.setdefault(s, [n, []])[1].append(p)
    for s, (n, ps) in sorted(tags.items()):
        intro = tag_intros.get(s, f"Every Live-Style story tagged {n}.")
        listing(f"/tag/{s}/", f"{n}: Tagged Stories | {NAME}", n, "Tag", intro,
                [("Home", "/"), ("Journal", "/journal/"), (n, f"/tag/{s}/")], ps, ps[0]["image"],
                trim(f"{n}: {intro}", 158), noindex=not indexable_tag(s, ps, tag_intros))
    return tags, tag_intros


def trim(text, n):
    if len(text) <= n:
        return text
    cut = text[: n - 1].rsplit(" ", 1)[0].rstrip(",.;:")
    return cut + "…"


def simple_page(path, title, h1, eyebrow, desc, inner, image, schema_type="WebPage"):
    items = [("Home", "/"), (h1, path)]
    body = f"""
<header class="list-hero list-hero-short">
  <div class="list-hero-media" data-parallax>{img(image, h1, eager=True)}</div>
  <div class="post-hero-shade"></div>
  <div class="wrap list-hero-inner">
    {breadcrumb_html(items)}
    <p class="eyebrow light hero-in" style="--d:0">{esc(eyebrow)}</p>
    <h1 class="hero-in" style="--d:1">{esc(h1)}</h1>
  </div>
</header>
<section class="section">
  <div class="wrap narrow prose">
{inner}
  </div>
</section>
"""
    schema = graph({"@type": schema_type, "url": ORIGIN + path, "name": h1, "description": desc,
                    "isPartOf": {"@id": ORIGIN + "/#website"}}, crumbs(items))
    write(path, page(path, title, desc, body, og_image=image, schema=schema))


def build_static_pages(posts):
    n = len(posts)
    about = f"""
<p class="lede">Live-Style began in {SITE['founded']} as a London notebook about making a home: the pieces we saved for, the makers we met at fairs and open studios, the paint colours we argued over and the restaurants we walked to on a Friday night.</p>
<p>This is the new home of that journal. We have rebuilt the stories readers still look for, from <a href="/2013/06/30/open-shelving-in-kitchens/">open shelving in kitchens</a> to <a href="/2015/07/16/final-paint-selections/">our final Little Greene paint selections</a>, and we&rsquo;re adding to them.</p>
<h2>What we write about</h2>
<ul>
  <li><strong>Interiors</strong>: practical ideas for real rooms, not just photo shoots.</li>
  <li><strong>Design &amp; makers</strong>: independent designers, lighting, textiles and furniture with a story.</li>
  <li><strong>Art &amp; prints</strong>: affordable art, illustrators and the festivals worth a ticket.</li>
  <li><strong>Renovation diary</strong>: our own house project, mistakes included.</li>
  <li><strong>Food &amp; places</strong>: cafés, restaurants and shops, mostly in London.</li>
</ul>
<h2>How we choose what to feature</h2>
<p>We write about things we have seen, used or genuinely want. We don&rsquo;t accept payment for coverage, and if that ever changes we&rsquo;ll say so clearly on the page.</p>
<blockquote>A home doesn&rsquo;t need to be finished to be lovely. It just needs to feel like the people who live there.</blockquote>
<h2>Say hello</h2>
<p>Ideas, corrections, makers we should know about: email <a href="mailto:{SITE['email']}">{SITE['email']}</a> or use the <a href="/contact/">contact page</a>. There are {n} stories in the <a href="/journal/">journal</a> so far.</p>
"""
    simple_page("/about/", f"About Live-Style | Interiors & Lifestyle Journal", "About Live-Style", "Our story",
                "About Live-Style, a London interiors, design and lifestyle journal founded in 2013: what we cover, how we choose what to feature, and how to reach us.",
                about, "home-green-study.jpg", "AboutPage")

    contact = f"""
<p class="lede">We&rsquo;d love to hear from you, whether it&rsquo;s a maker we should meet, a home worth featuring, a correction or a collaboration idea.</p>
<div class="contact-grid">
  <div class="contact-card">
    <p class="eyebrow">Email</p>
    <p><a class="big-link" href="mailto:{SITE['email']}">{SITE['email']}</a></p>
    <p>We read every message and aim to reply within a few working days.</p>
  </div>
  <form class="contact-form" action="/contact.php" method="post" data-contact>
    <div class="field"><label for="cf-name">Name</label><input id="cf-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" rows="6" required></textarea></div>
    <div class="hp" aria-hidden="true"><label for="cf-web">Website</label><input id="cf-web" name="website" tabindex="-1" autocomplete="off"></div>
    <button class="btn magnetic" type="submit">Send message</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</div>
"""
    simple_page("/contact/", f"Contact | {NAME}", "Contact us", "Get in touch",
                f"Contact Live-Style: email {SITE['email']} with story ideas, makers to feature, corrections or collaboration enquiries.",
                contact, "about-desk.jpg", "ContactPage")

    privacy = f"""
<p class="lede">This policy explains what information {NAME} collects when you visit live-style.co.uk and how it is used.</p>
<h2>Information you give us</h2>
<p>If you email us or use the contact form, we receive your name, email address and message. We use them only to reply to you and we do not sell or share them. Messages are deleted when they are no longer needed.</p>
<h2>Information collected automatically</h2>
<p>Like most websites, our host keeps standard server logs (IP address, browser type, pages requested and the time of the request) for security and to keep the site running. We do not use advertising trackers.</p>
<h2>Cookies</h2>
<p>The site itself does not set cookies. Fonts are loaded from Google Fonts, which may receive your IP address as part of delivering them.</p>
<h2>Your rights</h2>
<p>Under UK data protection law you can ask to see, correct or delete personal information we hold about you. Email <a href="mailto:{SITE['email']}">{SITE['email']}</a> and we&rsquo;ll respond within one month.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. This version was last updated on {nice_date(TODAY)}.</p>
"""
    simple_page("/privacy-policy/", f"Privacy Policy | {NAME}", "Privacy policy", "The small print",
                "How Live-Style handles your information: contact form messages, server logs, cookies and your rights under UK data protection law.",
                privacy, "home-bedroom.jpg")


def build_404(posts):
    body = f"""
<section class="notfound">
  <div class="wrap narrow center">
    <p class="eyebrow">Error 404</p>
    <h1>This room is empty</h1>
    <p>The page you were looking for has moved or no longer exists. Try one of these instead.</p>
    <p class="hero-actions center"><a class="btn" href="/">Home</a> <a class="btn btn-ghost-dark" href="/journal/">All stories</a></p>
  </div>
</section>
<section class="section section-tint"><div class="wrap">{grid(posts[:3])}</div></section>
"""
    html_ = page("/404.html", f"Page not found | {NAME}", "This page could not be found.", body, noindex=True)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html_)


def build_sitemap(posts, tags):
    urls = [("/", TODAY, "1.0"), ("/journal/", TODAY, "0.8"), ("/about/", TODAY, "0.5"),
            ("/contact/", TODAY, "0.4"), ("/privacy-policy/", TODAY, "0.2")]
    urls += [(f"/category/{s}/", TODAY, "0.6") for s, _ in CATEGORIES]
    urls += [(f"/tag/{s}/", TODAY, "0.4") for s in sorted(tags)]
    urls += [(p["path"], p.get("modified", TODAY), "0.7") for p in posts]
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pr in urls:
        out.append(f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
    out.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(out) + "\n")


def copy_static():
    for d in ("assets",):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), os.path.join(OUT, f))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    posts, tag_intros, cat_intros = load_content()
    copy_static()
    build_home(posts)
    for i, p in enumerate(posts):
        build_post(p, posts, i)
    tags, tag_intros = build_listings(posts, tag_intros, cat_intros)
    build_static_pages(posts)
    build_404(posts)
    build_sitemap(posts, {s: v for s, v in tags.items() if indexable_tag(s, v[1], tag_intros)})
    print(f"built {len(posts)} posts, {len(CATEGORIES)} categories, {len(tags)} tags -> public/")


if __name__ == "__main__":
    main()
