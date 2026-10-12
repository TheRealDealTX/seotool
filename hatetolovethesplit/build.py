#!/usr/bin/env python3
"""Static site generator for hatetolovethesplit.com.

python3 build.py   -> writes the site into ./public/
Only the Python standard library is used.
"""
import html
import json
import math
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from content.posts import POSTS  # noqa: E402

OUT = os.path.join(ROOT, "public")
SITE = {
    "name": "Hate to Love the Split",
    "short": "hate to love the split",
    "tagline": "A Minneapolis split-level, one stubborn project at a time.",
    "origin": "https://hatetolovethesplit.com",
    "email": "info@hatetolovethesplit.com",
    "author": "Emelia",
    "locale": "Minneapolis, Minnesota",
}
PER_PAGE = 6
NAV = [("Home", "/"), ("Projects", "/projects/"), ("Random Thoughts", "/category/random-thoughts/"),
       ("Archive", "/archives/"), ("About", "/about/"), ("Contact", "/contact/")]

CATEGORIES = {
    "kitchen": ("Kitchen", "white-kitchen", "IKEA Akurum cabinets, plumbing surprises and the long road from avocado green to bright and white."),
    "main-bathroom": ("Main Bathroom", "bathroom-sink", "Wallpaper removal, faux wood tiles, mocha grout and a Delta faucet: our main bathroom renovation from demo to reveal."),
    "hallway": ("Hallway", "bright-hallway", "New doors, a Ryobi hinge template and DIY board and batten walls for a split-level hallway."),
    "living-room": ("Living Room", "living-room", "Ceilings on the brain, tongue and groove plans and a secondhand Churchill chair."),
    "basement": ("Basement", "bar-counter", "The lower level: carpet, countertops and a built-in kegerator bar."),
    "bedroom": ("Bedroom", "split-stairs", "Closets, IKEA Pax and making a small split-level bedroom work harder."),
    "outsideyarddeck": ("Outside / Yard / Deck", "patio", "Cement pavers, lilac trimming, front stoop curb appeal and everything outdoors at the split."),
    "crafty": ("Crafty", "frames-brick", "Framing great grandma's recipe, gallery wall shelves with Ribba frames and other weekend crafts."),
    "random-thoughts": ("Random Thoughts", "couple-walk", "Life outside the renovation: Minneapolis eats, the NE bar scene, bike rides, books and travel."),
}
CATEGORY_ORDER = ["kitchen", "main-bathroom", "hallway", "living-room", "basement", "bedroom", "outsideyarddeck", "crafty", "random-thoughts"]

TAG_NAMES = {
    "ikea-akurum": "IKEA Akurum", "ikea-cabinets": "IKEA Cabinets", "ikea-pax": "IKEA Pax", "ikea-hektar": "IKEA Hektar",
    "ribba-frames": "Ribba Frames", "behr-dolphin-fin": "Behr Dolphin Fin", "delta-faucet": "Delta Faucet",
    "taylormade-golf-experience": "TaylorMade Golf Experience", "ne-minneapolis-bar-scene": "NE Minneapolis Bar Scene",
    "restoration-hardware-churchill": "Restoration Hardware Churchill", "the-fran-lebowitz-reader": "The Fran Lebowitz Reader",
    "el-jefe-guapo": "El Jefe Guapo", "bistro-le-roux": "Bistro Le Roux", "zinsser-gardz": "Zinsser Gardz",
    "ryobi-door-hinge-template": "Ryobi Door Hinge Template", "fig-and-olive": "Fig & Olive", "diy": "DIY",
    "minnesota-ironman-bike-ride": "Minnesota Ironman Bike Ride", "lifetime-fitness": "Lifetime Fitness",
    "hola-arepa": "Hola Arepa", "hammerheart-brewery": "Hammerheart Brewery", "las-vegas": "Las Vegas",
    "diy-fails": "DIY Fails", "diy-landscaping": "DIY Landscaping", "molly-shannon": "Molly Shannon",
}
TAG_INTRO = {
    "ribba-frames": "Everything we've done with IKEA Ribba frames, including step-by-step Ribba frame instructions for swapping mats and photos and styling them on gallery wall shelves.",
    "kegerator": "Our kegerator posts: comparing Summit, Marvel and Beverage Factory units, built-in vs. freestanding, and running a countertop beer tap.",
    "built-in-kegerator": "How to choose and install a built-in kegerator under a counter, including why front ventilation matters.",
    "beverage-factory": "Notes on Beverage Factory kegerators and draft parts from our basement bar build.",
    "cement-pavers": "How we installed cement pavers for a DIY patio, from excavation and gravel base to polymeric sand.",
    "ikea-cabinets": "IKEA cabinets throughout the split: Akurum kitchen cabinets, a wine fridge bay, fridge drawers and an under-cabinet kegerator.",
    "el-jefe-guapo": "El Jefe Guapo (pronounced el HEH-feh GWAH-po, \"the handsome boss\") is the neighborhood cat who supervises our projects.",
    "stinger-energy-gel": "Fueling long rides with Honey Stinger energy gel while training for the Minnesota Ironman bike ride.",
    "hiawatha-bike-trail": "Training rides on the Hiawatha bike trail in Minneapolis (and notes on the Route of the Hiawatha out west).",
    "minnesota-ironman-bike-ride": "Getting ready for the Minnesota Ironman bike ride, one of the state's classic spring rides.",
    "delta-faucet": "Our Delta faucet picks, including the oil rubbed bronze bathroom faucet from the main bathroom reveal.",
    "mocha-grout": "Why we used mocha grout with faux wood tile, and how to seal it.",
    "faux-wood-tiles": "Faux wood tiles in our main bathroom: layout offsets, grout joints and grout color.",
    "door-hardware": "Door hardware swaps around the split, including how to remove a Weslock door knob.",
    "behr-dolphin-fin": "Behr Dolphin Fin vs. Behr Ceiling White for walls and a white tongue and groove ceiling.",
    "restoration-hardware-churchill": "Our secondhand Restoration Hardware Churchill leather library chair.",
    "taylormade-golf-experience": "A morning at the TaylorMade Golf Experience in Las Vegas.",
    "lifetime-fitness": "Spin class at Lakeville Lifetime Fitness while training for long bike rides.",
    "stephanie-plum-series": "Reading the Stephanie Plum series by Janet Evanovich, in order.",
    "the-fran-lebowitz-reader": "Why The Fran Lebowitz Reader is the perfect between-coats-of-paint book.",
    "ne-minneapolis-bar-scene": "Celebrating finished projects in the NE Minneapolis bar scene.",
    "hammerheart-brewery": "A day trip to Hammerheart Brewery in Lino Lakes.",
    "jimmy-rig": "Our jimmy rig fixes, including a wobbly Churchill chair leg.",
    "ikea-hektar": "The IKEA Hektar lamp that made our closet corner feel like a boutique hotel.",
    "ikea-pax": "Designing a closet with the IKEA Pax planner.",
    "zara": "Shopping Zara in Las Vegas.",
    "bistro-le-roux": "A celebration dinner at Bistro Le Roux.",
    "mung-bean-griddle-cake": "Korean mung bean griddle cakes (bindaetteok) in NYC, and how to make them at home.",
    "ikea-akurum": "Installing IKEA Akurum base and wall cabinets on the suspension rail.",
}

IMG_SIZES = {}


def esc(s):
    return html.escape(s, quote=True)


def tag_name(slug):
    return TAG_NAMES.get(slug) or slug.replace("-", " ").title()


def img_size(name):
    if name not in IMG_SIZES:
        path = os.path.join(ROOT, "assets", "img", name + ".webp")
        with open(path, "rb") as f:
            data = f.read(64)
        # VP8 / VP8L / VP8X headers
        fmt = data[12:16]
        if fmt == b"VP8X":
            w = 1 + int.from_bytes(data[24:27], "little")
            h = 1 + int.from_bytes(data[27:30], "little")
        elif fmt == b"VP8L":
            b = int.from_bytes(data[21:25], "little")
            w, h = (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        else:
            w = int.from_bytes(data[26:28], "little") & 0x3FFF
            h = int.from_bytes(data[28:30], "little") & 0x3FFF
        IMG_SIZES[name] = (w, h)
    return IMG_SIZES[name]


def img(name, alt, cls="", eager=False, sizes=None):
    w, h = img_size(name)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/assets/img/{name}.webp" alt="{esc(alt)}" width="{w}" height="{h}" {load}{c}>'


# ------------------------------------------------------------------ posts
for p in POSTS:
    y, m, d = p["date"].split("-")
    p["url"] = f"/{y}/{m}/{d}/{p['slug']}/"
    p["dt"] = datetime.strptime(p["date"], "%Y-%m-%d").date()
    p["display_date"] = p["dt"].strftime("%B %-d, %Y")
    text = re.sub(r"<[^>]+>|\[\[.*?\]\]", " ", p["body"])
    p["words"] = len(text.split())
    p["read"] = max(2, math.ceil(p["words"] / 220))
POSTS.sort(key=lambda p: p["dt"], reverse=True)
for i, p in enumerate(POSTS):
    p["newer"] = POSTS[i - 1] if i > 0 else None
    p["older"] = POSTS[i + 1] if i + 1 < len(POSTS) else None

BY_CAT = defaultdict(list)
BY_TAG = defaultdict(list)
BY_MONTH = defaultdict(list)
BY_YEAR = defaultdict(list)
for p in POSTS:
    BY_CAT[p["category"]].append(p)
    for t in p["tags"]:
        BY_TAG[t].append(p)
    BY_MONTH[p["date"][:7]].append(p)
    BY_YEAR[p["date"][:4]].append(p)


def render_body(body):
    def fig(m):
        name, alt, cap = [x.strip() for x in m.group(1).split("|")]
        return (f'<figure class="post-fig reveal">{img(name, alt)}'
                f'<figcaption>{esc(cap)}</figcaption></figure>')

    def tip(m):
        title, text = [x.strip() for x in m.group(1).split("|", 1)]
        return (f'<aside class="tip reveal"><span class="tip-ico" aria-hidden="true">✦</span>'
                f'<div><strong>{esc(title)}</strong><p>{esc(text)}</p></div></aside>')

    body = re.sub(r"\[\[fig (.*?)\]\]", fig, body)
    body = re.sub(r"\[\[tip (.*?)\]\]", tip, body)
    body = body.replace("info@hatetolovethesplit.com",
                        f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>')
    return body.strip()


# ------------------------------------------------------------------ layout
LOGO = ('<a class="brand" href="/" aria-label="Hate to Love the Split, home">'
        '<span class="brand-mark" aria-hidden="true"><span></span><span></span></span>'
        '<span class="brand-text"><s>hate</s> to <em>love</em> the split</span></a>')


def header(current):
    links = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if u == current else ""}>{n}</a></li>' for n, u in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" data-header>
  <div class="wrap header-in">
    {LOGO}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu" data-nav-toggle>
      <span class="bars" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main" data-nav>
      <ul>{links}</ul>
      <a class="nav-cta" href="mailto:{SITE['email']}">Say hello</a>
    </nav>
  </div>
</header>
<div class="nav-scrim" data-nav-scrim hidden></div>"""


def footer():
    cats = "".join(f'<li><a href="/category/{c}/">{CATEGORIES[c][0]}</a></li>' for c in CATEGORY_ORDER)
    recent = "".join(f'<li><a href="{p["url"]}">{esc(p["title"])}</a></li>' for p in POSTS[:5])
    return f"""<footer class="site-footer">
  <div class="footer-wave" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-about">
      {LOGO}
      <p>{esc(SITE['tagline'])} Renovation stories, DIY how-tos and the occasional detour for tacos, from a 1970s split-level in the Twin Cities.</p>
      <a class="btn btn-light" href="mailto:{SITE['email']}">{SITE['email']}</a>
    </div>
    <div><h2 class="footer-h">Rooms</h2><ul>{cats}</ul></div>
    <div><h2 class="footer-h">Recent stories</h2><ul>{recent}</ul></div>
    <div><h2 class="footer-h">Around here</h2><ul>
      <li><a href="/projects/">All projects</a></li><li><a href="/archives/">Archive</a></li>
      <li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy policy</a></li></ul></div>
  </div>
  <div class="wrap footer-base"><p>© <span data-year>{date.today().year}</span> Hate to Love the Split. Made with paint-covered hands in Minnesota.</p>
  <a href="#main" class="to-top" aria-label="Back to top">↑</a></div>
</footer>"""


def page(path, title, description, body, current="", og_image="split-stairs", schema=None,
         og_type="website", body_class="", noindex=False):
    canonical = SITE["origin"] + path
    w, h = img_size(og_image)
    ld = [{
        "@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
        "url": SITE["origin"] + "/", "description": SITE["tagline"],
        "publisher": {"@type": "Organization", "name": SITE["name"], "email": SITE["email"]},
    }]
    if schema:
        ld.extend(schema if isinstance(schema, list) else [schema])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#211a2e">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['origin']}/assets/img/{og_image}.webp">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..700&family=Inter:wght@400;500;600;700&family=Caveat:wght@600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
{ld_html}
</head>
<body class="{body_class}">
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def write(path, content):
    if path == "/":
        dest = os.path.join(OUT, "home.html")
    elif path.endswith(".xml") or path.endswith(".txt") or path.endswith(".html"):
        dest = os.path.join(OUT, path.lstrip("/"))
    else:
        dest = os.path.join(OUT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(content)
    if path.endswith("/"):
        PAGES.append(path)


PAGES = []


def crumbs(items):
    lis = []
    for i, (name, url) in enumerate(items):
        if url and i < len(items) - 1:
            lis.append(f'<li><a href="{url}">{esc(name)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{esc(name)}</li>')
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["origin"] + (u or "")}
        for i, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>', schema


def card(p, big=False, eager=False):
    cat = CATEGORIES[p["category"]][0]
    cls = "card card-big" if big else "card"
    return f"""<article class="{cls} reveal" data-tilt>
  <a class="card-media" href="{p['url']}" tabindex="-1" aria-hidden="true">{img(p['image'], p['image_alt'], eager=eager)}</a>
  <div class="card-body">
    <a class="chip" href="/category/{p['category']}/">{cat}</a>
    <h3 class="card-title"><a href="{p['url']}">{esc(p['title'])}</a></h3>
    {'<p class="card-ex">' + esc(p['description']) + '</p>' if big else ''}
    <p class="meta"><time datetime="{p['date']}">{p['display_date']}</time> · {p['read']} min read</p>
  </div>
</article>"""


def hero_band(kicker, title, intro, image, alt):
    return f"""<section class="band">
  <div class="band-bg">{img(image, alt, eager=True)}</div>
  <div class="wrap band-in">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    {f'<p class="band-intro">{intro}</p>' if intro else ''}
  </div>
</section>"""


def pager(base, n, total):
    if total <= 1:
        return ""
    out = []
    for i in range(1, total + 1):
        url = base if i == 1 else f"{base}page/{i}/"
        cur = ' aria-current="page"' if i == n else ""
        out.append(f'<a href="{url}"{cur}>{i}</a>')
    prev = f'<a class="pg-step" href="{base if n == 2 else f"{base}page/{n-1}/"}">← Newer</a>' if n > 1 else ""
    nxt = f'<a class="pg-step" href="{base}page/{n+1}/">Older →</a>' if n < total else ""
    return f'<nav class="pager" aria-label="Pagination">{prev}{"".join(out)}{nxt}</nav>'


def listing(path, kicker, h1, intro, posts, image, alt, title, description, trail, paginate=True):
    pages = math.ceil(len(posts) / PER_PAGE) if paginate else 1
    for n in range(1, pages + 1):
        chunk = posts[(n - 1) * PER_PAGE: n * PER_PAGE] if paginate else posts
        url = path if n == 1 else f"{path}page/{n}/"
        bc, bc_schema = crumbs(trail + ([(f"Page {n}", url)] if n > 1 else []))
        t = title if n == 1 else f"{title} – Page {n}"
        body = hero_band(kicker, h1 + (f" <small>· page {n}</small>" if n > 1 else ""), intro, image, alt)
        body += f'<section class="wrap section">{bc}<div class="grid">{"".join(card(p) for p in chunk)}</div>{pager(path, n, pages)}</section>'
        schema = [bc_schema, {"@context": "https://schema.org", "@type": "CollectionPage", "name": h1,
                              "url": SITE["origin"] + url, "description": description}]
        write(url, page(url, t, description, body, current=path, og_image=image, schema=schema))


# ------------------------------------------------------------------ builders
def build_post(p):
    cat_name = CATEGORIES[p["category"]][0]
    bc, bc_schema = crumbs([("Home", "/"), (cat_name, f"/category/{p['category']}/"), (p["title"], p["url"])])
    tags = "".join(f'<a class="tag" href="/tag/{t}/">#{esc(tag_name(t))}</a>' for t in p["tags"])
    related = [q for q in POSTS if q is not p and (q["category"] == p["category"] or set(q["tags"]) & set(p["tags"]))]
    related += [q for q in POSTS if q is not p and q not in related]
    nav_links = ""
    if p["older"]:
        nav_links += f'<a class="pn pn-prev" href="{p["older"]["url"]}"><span>← Previous</span><strong>{esc(p["older"]["title"])}</strong></a>'
    if p["newer"]:
        nav_links += f'<a class="pn pn-next" href="{p["newer"]["url"]}"><span>Next →</span><strong>{esc(p["newer"]["title"])}</strong></a>'
    w, h = img_size(p["image"])
    body = f"""<article class="post">
  <header class="post-hero">
    <div class="post-hero-bg">{img(p['image'], p['image_alt'], eager=True)}</div>
    <div class="wrap post-hero-in">
      <a class="chip chip-light" href="/category/{p['category']}/">{cat_name}</a>
      <h1>{esc(p['title'])}</h1>
      <p class="meta">By {SITE['author']} · <time datetime="{p['date']}">{p['display_date']}</time> · {p['read']} min read</p>
    </div>
  </header>
  <div class="wrap post-wrap">
    {bc}
    <div class="prose">{render_body(p['body'])}</div>
    <div class="post-tags"><span>Tagged</span>{tags}</div>
    <aside class="author-box reveal">
      {img('couple-walk', 'Two people walking hand in hand down a sidewalk', cls='author-img')}
      <div><strong>Written by {SITE['author']}</strong><p>Half of the team slowly falling in love with a 1970s split-level in the Twin Cities. Questions about this project? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p></div>
    </aside>
    <nav class="post-nav" aria-label="More posts">{nav_links}</nav>
  </div>
</article>
<section class="section section-tint"><div class="wrap">
  <div class="section-head"><p class="kicker">Keep reading</p><h2>More from the split</h2></div>
  <div class="grid">{"".join(card(q) for q in related[:3])}</div>
</div></section>"""
    schema = [bc_schema, {
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
        "description": p["description"], "datePublished": p["date"], "dateModified": p["date"],
        "mainEntityOfPage": SITE["origin"] + p["url"],
        "image": {"@type": "ImageObject", "url": f"{SITE['origin']}/assets/img/{p['image']}.webp", "width": w, "height": h},
        "author": {"@type": "Person", "name": SITE["author"]},
        "publisher": {"@type": "Organization", "name": SITE["name"]},
        "articleSection": cat_name, "keywords": ", ".join(tag_name(t) for t in p["tags"]), "wordCount": p["words"],
    }]
    write(p["url"], page(p["url"], f"{p['seo_title']} | Hate to Love the Split", p["description"], body,
                         og_image=p["image"], schema=schema, og_type="article", body_class="is-post"))


def build_home():
    latest = POSTS[:7]
    popular_slugs = ["akurum-cabinets", "lilac-trimming", "carpet-countertop-beer", "installing-cement-pavers",
                     "diy-gallery-wall-shelves-pt-2", "ceilings-on-the-brain"]
    popular = [next(p for p in POSTS if p["slug"] == s) for s in popular_slugs]
    rooms = "".join(f"""<a class="room reveal" href="/category/{c}/" data-tilt>
  {img(CATEGORIES[c][1], CATEGORIES[c][0] + ' projects')}
  <span class="room-label"><strong>{CATEGORIES[c][0]}</strong><small>{len(BY_CAT[c])} {'story' if len(BY_CAT[c]) == 1 else 'stories'}</small></span>
</a>""" for c in CATEGORY_ORDER)
    marquee_tags = sorted(BY_TAG, key=lambda t: -len(BY_TAG[t]))[:18]
    marquee = "".join(f'<a href="/tag/{t}/">{esc(tag_name(t))}</a><span aria-hidden="true">✦</span>' for t in marquee_tags)
    body = f"""<section class="hero">
  <div class="hero-bg" data-parallax>{img('split-stairs', 'A bright split-level living room with a floating staircase', eager=True)}</div>
  <div class="hero-blobs" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap hero-in">
    <p class="kicker kicker-light">A split-level renovation blog · Minneapolis</p>
    <h1 class="hero-title">From <span class="strike">hate</span> to <span class="love">love</span>,<br>one split-level at a time.</h1>
    <p class="hero-sub">We bought a 1970s split-level we didn't love. These are the projects, the mistakes and the small wins that are slowly changing our minds, plus the occasional detour for arepas.</p>
    <div class="hero-cta"><a class="btn" href="#latest">Read the latest</a><a class="btn btn-ghost" href="/projects/">Tour the rooms</a></div>
  </div>
  <a class="scroll-cue" href="#intro" aria-label="Scroll to content"><span></span></a>
</section>

<div class="marquee" aria-label="Popular topics"><div class="marquee-track">{marquee}{marquee}</div></div>

<section class="section" id="intro"><div class="wrap split">
  <div class="split-media reveal">
    {img('house', 'A two-story suburban house at dusk with a lit front porch')}
    <span class="sticker" aria-hidden="true">est. 2014</span>
  </div>
  <div class="split-copy reveal">
    <p class="kicker">So, what's a split?</p>
    <h2>Half a flight up, half a flight down, and completely ours.</h2>
    <p>A split-level is that very 1970s house where you walk in the front door and immediately have to choose: up to the kitchen and bedrooms, or down to the family room. Ours came with popcorn ceilings, three layers of bathroom wallpaper and a mouse problem. We hated it a little.</p>
    <p>So we started fixing it, one room at a time, and writing it all down. Honest how-tos, real costs and the things we'd do differently.</p>
    <dl class="stats">
      <div><dt>Stories</dt><dd data-count="{len(POSTS)}">{len(POSTS)}</dd></div>
      <div><dt>Rooms tackled</dt><dd data-count="{len(CATEGORY_ORDER) - 1}">{len(CATEGORY_ORDER) - 1}</dd></div>
      <div><dt>Trips to IKEA</dt><dd data-count="214" data-suffix="+">214+</dd></div>
    </dl>
  </div>
</div></section>

<section class="section section-dark"><div class="wrap ba-wrap">
  <div class="section-head reveal"><p class="kicker kicker-light">Drag the handle</p><h2>The whole idea, in one slider</h2>
  <p>Every room starts on the left. The goal is always the right.</p></div>
  <div class="ba reveal" data-ba style="--pos:50%">
    <div class="ba-img ba-after">{img('living-room', 'A bright, finished living room with a sectional and wood floors')}</div>
    <div class="ba-img ba-before" aria-hidden="true">{img('living-room', '')}</div>
    <span class="ba-tag ba-tag-l">hate</span><span class="ba-tag ba-tag-r">love</span>
    <div class="ba-handle" aria-hidden="true"><span>⇆</span></div>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after">
  </div>
</div></section>

<section class="section" id="rooms"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Tour the split</p><h2>Pick a room, any room</h2></div>
  <div class="rooms">{rooms}</div>
</div></section>

<section class="section section-tint" id="latest"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Fresh off the drop cloth</p><h2>Latest stories</h2></div>
  <div class="feature">{card(latest[0], big=True)}</div>
  <div class="grid">{"".join(card(p) for p in latest[1:7])}</div>
  <p class="center"><a class="btn btn-outline" href="/archives/">See every story</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Reader favorites</p><h2>The projects everyone asks about</h2></div>
  <ol class="popular">{"".join(f'<li class="reveal"><a href="{p["url"]}"><span class="pop-n">{i+1:02d}</span><span class="pop-t">{esc(p["title"])}</span><span class="pop-c">{CATEGORIES[p["category"]][0]}</span></a></li>' for i, p in enumerate(popular))}</ol>
</div></section>

<section class="section cta-band"><div class="wrap split split-rev">
  <div class="split-media reveal">{img('couple-walk', 'Two people walking hand in hand down a tree-lined sidewalk')}</div>
  <div class="split-copy reveal">
    <p class="kicker">Hi, we're the split</p>
    <h2>Two people, one house, too many paint samples.</h2>
    <p>{SITE['author']} writes most of the posts. The Mister handles the power tools and the kegerator. Together we're turning a house we didn't love into one we can't imagine leaving.</p>
    <p>Have a question about a project, or a split-level of your own? We'd love to hear from you.</p>
    <div class="hero-cta"><a class="btn" href="mailto:{SITE['email']}">{SITE['email']}</a><a class="btn btn-outline" href="/about/">Our story</a></div>
  </div>
</div></section>"""
    schema = {"@context": "https://schema.org", "@type": "Blog", "name": SITE["name"], "url": SITE["origin"] + "/",
              "description": SITE["tagline"], "author": {"@type": "Person", "name": SITE["author"]},
              "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE["origin"] + p["url"],
                            "datePublished": p["date"]} for p in POSTS[:10]]}
    write("/", page("/", "Hate to Love the Split | A Minneapolis Split-Level Renovation Blog",
                    "Hate to Love the Split is a home renovation and DIY blog about falling in love with a 1970s Minneapolis split-level: kitchen, bathroom, hallway and yard projects, plus Twin Cities eats.",
                    body, current="/", schema=schema, body_class="is-home"))


def build_categories():
    for c in CATEGORY_ORDER:
        name, image, intro = CATEGORIES[c]
        listing(f"/category/{c}/", "Category", name, esc(intro), BY_CAT[c], image, name,
                f"{name} Projects | Hate to Love the Split", intro,
                [("Home", "/"), ("Projects", "/projects/"), (name, f"/category/{c}/")])


def build_tags():
    for t, posts in BY_TAG.items():
        name = tag_name(t)
        intro = TAG_INTRO.get(t, f"Every post on Hate to Love the Split tagged {name}.")
        listing(f"/tag/{t}/", "Tag", name, esc(intro), posts, posts[0]["image"], posts[0]["image_alt"],
                f"{name} | Hate to Love the Split", intro, [("Home", "/"), (f"Tag: {name}", f"/tag/{t}/")],
                paginate=False)


def build_archives():
    for ym, posts in BY_MONTH.items():
        y, m = ym.split("-")
        label = datetime(int(y), int(m), 1).strftime("%B %Y")
        url = f"/{y}/{m}/"
        listing(url, "Archive", label, f"Everything we posted in {label}.", posts, posts[0]["image"], posts[0]["image_alt"],
                f"{label} Archive | Hate to Love the Split",
                f"Posts from {label} on Hate to Love the Split: " + "; ".join(p["title"] for p in posts)[:140] + ".",
                [("Home", "/"), ("Archive", "/archives/"), (label, url)], paginate=False)
    for y, posts in BY_YEAR.items():
        listing(f"/{y}/", "Archive", y, f"Every story from {y}.", posts, posts[-1]["image"], posts[-1]["image_alt"],
                f"{y} Archive | Hate to Love the Split", f"All {len(posts)} posts from {y} on Hate to Love the Split.",
                [("Home", "/"), ("Archive", "/archives/"), (y, f"/{y}/")])
    # full archive
    blocks = []
    for y in sorted(BY_YEAR, reverse=True):
        items = "".join(f'<li class="reveal"><time datetime="{p["date"]}">{p["dt"].strftime("%b %-d")}</time>'
                        f'<a href="{p["url"]}">{esc(p["title"])}</a><span class="chip">{CATEGORIES[p["category"]][0]}</span></li>'
                        for p in BY_YEAR[y])
        blocks.append(f'<div class="arch-year"><h2><a href="/{y}/">{y}</a></h2><ul class="arch-list">{items}</ul></div>')
    months = "".join(f'<a class="tag" href="/{ym[:4]}/{ym[5:]}/">{datetime(int(ym[:4]), int(ym[5:]), 1).strftime("%b %Y")}</a>'
                     for ym in sorted(BY_MONTH, reverse=True))
    tags = "".join(f'<a class="tag" href="/tag/{t}/">#{esc(tag_name(t))} <small>{len(BY_TAG[t])}</small></a>' for t in sorted(BY_TAG))
    bc, bc_schema = crumbs([("Home", "/"), ("Archive", "/archives/")])
    body = hero_band("The whole story", "Archive", f"All {len(POSTS)} posts, newest first.", "bookshelf", "Bookshelf full of books")
    body += f'<section class="wrap section">{bc}{"".join(blocks)}<h2 class="sub-h">By month</h2><div class="tag-cloud">{months}</div><h2 class="sub-h">By tag</h2><div class="tag-cloud">{tags}</div></section>'
    write("/archives/", page("/archives/", "Archive: Every Post | Hate to Love the Split",
                             "Browse every post on Hate to Love the Split by year, month and tag, from IKEA Akurum cabinets to board and batten.",
                             body, current="/archives/", og_image="bookshelf", schema=bc_schema))


def build_projects():
    bc, bc_schema = crumbs([("Home", "/"), ("Projects", "/projects/")])
    blocks = []
    for c in CATEGORY_ORDER:
        name, image, intro = CATEGORIES[c]
        items = "".join(f'<li><a href="{p["url"]}">{esc(p["title"])}</a></li>' for p in BY_CAT[c])
        blocks.append(f"""<section class="proj reveal">
  <a class="proj-media" href="/category/{c}/" tabindex="-1" aria-hidden="true">{img(image, name)}</a>
  <div class="proj-body"><h2><a href="/category/{c}/">{name}</a></h2><p>{esc(intro)}</p><ul>{items}</ul></div>
</section>""")
    body = hero_band("Room by room", "Projects", "Every space in the split, and what we've done to it so far.", "brick-kitchen", "A white brick kitchen with open shelves")
    body += f'<div class="wrap section">{bc}<div class="projs">{"".join(blocks)}</div></div>'
    write("/projects/", page("/projects/", "Split-Level Renovation Projects, Room by Room | Hate to Love the Split",
                             "Our split-level renovation projects room by room: kitchen, main bathroom, hallway, living room, basement bar, bedroom closet, yard and crafts.",
                             body, current="/projects/", og_image="brick-kitchen", schema=bc_schema))


def simple_page(path, kicker, h1, image, alt, title, description, inner, current=""):
    bc, bc_schema = crumbs([("Home", "/"), (h1, path)])
    body = hero_band(kicker, h1, "", image, alt)
    body += f'<div class="wrap section narrow">{bc}<div class="prose">{inner}</div></div>'
    write(path, page(path, title, description, body, current=current or path, og_image=image, schema=bc_schema))


def build_pages():
    simple_page("/about/", "Our story", "About the Split", "couple-walk", "Two people walking hand in hand",
                "About Us | Hate to Love the Split",
                "Meet the people behind Hate to Love the Split, a DIY renovation blog about a 1970s split-level house in Minneapolis.",
                f"""<p class="lead">In late 2013 we bought a split-level in the Twin Cities. It had good bones, a great yard and absolutely everything else wrong with it.</p>
<p>The kitchen was avocado green. The bathroom had three layers of wallpaper (the bottom one was gold foil). The hallway doors were hollow, the ceilings were popcorn and there was, briefly, a family of mice living under the sink. We did not love it. Honestly? We kind of hated it.</p>
[[fig split-stairs | A bright living room with a floating staircase | The dream version of a split-level. We're getting there.]]
<h2>Why "Hate to Love the Split"?</h2>
<p>Because that's the plan: take a house we didn't love and fix it, one room at a time, until we can't imagine living anywhere else. This blog is the record of that: what we tried, what it cost, what worked and what we'd never do again (looking at you, indoor spray paint).</p>
<h2>What you'll find here</h2>
<ul>
<li><strong>Room-by-room renovation stories</strong> with honest how-tos, from <a href="/2014/02/07/akurum-cabinets/">IKEA Akurum cabinets</a> to <a href="/2016/01/03/hallway-part-2-board-and-batten/">board and batten</a>.</li>
<li><strong>Yard and garden projects</strong> like <a href="/2014/06/22/installing-cement-pavers/">installing cement pavers</a> and <a href="/2014/07/07/lilac-trimming/">trimming lilacs</a>.</li>
<li><strong>Crafts</strong> like <a href="/2014/01/19/crafty-great-grandmas-recipe/">framing great grandma's recipe</a>.</li>
<li><strong>Random thoughts</strong>: Minneapolis restaurants, bike rides, books and travel.</li>
</ul>
<h2>Say hello</h2>
<p>We read every email. Reach us at <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>""".replace("[[fig split-stairs | A bright living room with a floating staircase | The dream version of a split-level. We're getting there.]]",
                                                                                                     render_body("[[fig split-stairs | A bright living room with a floating staircase | The dream version of a split-level. We're getting there.]]")))

    simple_page("/contact/", "Get in touch", "Contact", "coffee", "A latte on a wooden table",
                "Contact Us | Hate to Love the Split",
                "Contact Hate to Love the Split: questions about a project, collaborations or split-level stories. Email info@hatetolovethesplit.com.",
                f"""<p class="lead">Questions about a project? Have a split-level of your own? Want to tell us we're holding the drill wrong? We'd love to hear from you.</p>
<div class="contact-card">
  <span class="contact-ico" aria-hidden="true">✉</span>
  <div><strong>Email us</strong><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p><small>We usually reply within a few days (longer if we're mid-demo).</small></div>
</div>
<form class="contact-form" action="/contact.php" method="post">
  <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" autocomplete="name" required></div>
  <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" rows="6" required></textarea></div>
  <div class="hp" aria-hidden="true"><label for="cf-web">Website</label><input id="cf-web" name="website" tabindex="-1" autocomplete="off"></div>
  <button class="btn" type="submit">Send message</button>
  <p class="form-note" data-form-note role="status"></p>
</form>""")

    simple_page("/privacy-policy/", "The fine print", "Privacy Policy", "reading", "A person reading a book",
                "Privacy Policy | Hate to Love the Split", "The privacy policy for hatetolovethesplit.com.",
                f"""<p>Last updated {date.today().strftime('%B %-d, %Y')}.</p>
<p>Hate to Love the Split ("we") runs hatetolovethesplit.com. This page explains what information we collect and how we use it.</p>
<h2>Information you send us</h2>
<p>If you email us or use the contact form, we receive your name, email address and message. We use it only to reply to you and never sell or share it.</p>
<h2>Server logs and cookies</h2>
<p>Our web host keeps standard server logs (IP address, browser, pages requested) for security and performance. The site itself does not set advertising or tracking cookies. Fonts are loaded from Google Fonts, which may log your IP address.</p>
<h2>Links</h2>
<p>Posts may link to other websites. We are not responsible for their content or privacy practices.</p>
<h2>Contact</h2>
<p>Questions about this policy? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>""", current="")

    body = hero_band("404", "This room isn't finished yet", "The page you're looking for has moved or never existed. Try one of these instead.", "gutted-room", "A room mid-demolition")
    body += f'<section class="wrap section"><div class="grid">{"".join(card(p) for p in POSTS[:6])}</div><p class="center"><a class="btn" href="/">Back home</a></p></section>'
    html_404 = page("/404/", "Page Not Found | Hate to Love the Split", "Page not found.", body, og_image="gutted-room", noindex=True)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html_404)


def build_meta():
    today = date.today().isoformat()
    urls = []
    for path in sorted(set(PAGES)):
        if path == "/404/":
            continue
        lastmod = next((p["date"] for p in POSTS if p["url"] == path), today)
        urls.append(f"<url><loc>{SITE['origin']}{path}</loc><lastmod>{lastmod}</lastmod></url>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    # RSS feed (served at /feed/ by index.php)
    items = "".join(f"""<item><title>{esc(p['title'])}</title><link>{SITE['origin']}{p['url']}</link><guid>{SITE['origin']}{p['url']}</guid><pubDate>{p['dt'].strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate><description>{esc(p['description'])}</description></item>""" for p in POSTS[:15])
    with open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{SITE["name"]}</title><link>{SITE["origin"]}/</link><description>{esc(SITE["tagline"])}</description>{items}</channel></rss>\n')


def copy_static():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for f in ("index.php", "contact.php", "favicon.svg", ".htaccess"):
        shutil.copy(os.path.join(ROOT, "static", f), os.path.join(OUT, f))


VERSION = date.today().strftime("%Y%m%d")

if __name__ == "__main__":
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_static()
    build_home()
    for p in POSTS:
        build_post(p)
    build_categories()
    build_tags()
    build_archives()
    build_projects()
    build_pages()
    build_meta()
    print(f"built {len(set(PAGES))} pages into {OUT}")
