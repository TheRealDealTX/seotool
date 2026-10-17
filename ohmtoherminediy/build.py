#!/usr/bin/env python3
"""Static site generator for ohmtoherminediy.com (Oh, Mother Mine DIY).

python3 build.py  ->  writes the whole site into ./public
"""
import html
import json
import os
import re
import shutil
from datetime import date

from content.posts_a import POSTS as POSTS_A
from content.posts_b import POSTS as POSTS_B
from content.pages import CATEGORIES, TOOLS, HOME_FAQ, PILLAR

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
SRC = os.path.join(ROOT, "src")
SITE = "https://ohmtoherminediy.com"
NAME = "Oh, Mother Mine DIY"
EMAIL = "info@ohmtoherminediy.com"
TODAY = date(2026, 10, 17).isoformat()
ASSET_V = "4"

POSTS = sorted(POSTS_A + POSTS_B, key=lambda p: p["date"], reverse=True)
BY_SLUG = {p["slug"]: p for p in POSTS}
CAT = {c["slug"]: c for c in CATEGORIES}

esc = lambda s: html.escape(str(s), quote=True)

# ---------------------------------------------------------------- icons
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "tag": '<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "wallet": '<rect x="3" y="6" width="18" height="13" rx="3"/><path d="M16 12h2M3 9h18"/>',
    "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 10h18"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "brush": '<path d="M14 4l6 6-8 8H6v-6z"/><path d="M4 20c1-2 2-3 4-3"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1 0 1.5-.8 1.5-1.6 0-1.2-1-1.6-1-2.6 0-1 .8-1.8 1.8-1.8H17a4 4 0 0 0 4-4C21 6.5 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    "quiz": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .9-1 1.7M12 17h.01"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="3"/><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>',
    "beaker": '<path d="M9 3h6M10 3v6L5 19a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2l-5-10V3"/><path d="M7.5 15h9"/>',
    "piggy": '<path d="M5 11a6 5 0 0 1 11-3h2l1 3h1v4h-2l-1 3h-3v-2h-4v2H7l-1-3a5 5 0 0 1-1-4z"/><path d="M14 10h.01"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "fb": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v6h4v-6h3l1-4h-4V8z"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
    "swap": '<path d="M8 7l-4 5 4 5M16 7l4 5-4 5"/>',
    "leaf": '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/>',
    "home": '<path d="M4 11l8-7 8 7v9H4z"/><path d="M10 20v-5h4v5"/>',
}


def icon(name, cls=""):
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (' class="%s"' % cls if cls else "", ICONS[name]))


LOGO_MARK = ('<span class="logo-mark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>'
             '<path d="M9.5 11.5l2 2 3.5-4"/></svg></span>')


def img(key, alt, size="", cls="", lazy=True, w=None, h=None, sizes=None):
    """<img> for an image key. size '' = 1600w file, 'sm' = 720w file."""
    src = "/assets/img/%s%s.webp" % (key, "-sm" if size == "sm" else "")
    attrs = ['src="%s"' % src, 'alt="%s"' % esc(alt)]
    if size != "sm":
        attrs.append('srcset="/assets/img/%s-sm.webp 720w, /assets/img/%s.webp 1024w"' % (key, key))
        attrs.append('sizes="%s"' % (sizes or "100vw"))
    if w:
        attrs.append('width="%d" height="%d"' % (w, h))
    attrs.append('loading="lazy" decoding="async"' if lazy else 'fetchpriority="high"')
    if cls:
        attrs.append('class="%s"' % cls)
    return "<img %s>" % " ".join(attrs)


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = "January February March April May June July August September October November December".split()
    return "%s %d, %s" % (months[int(m) - 1], int(d), y)


def url_of(p):
    return "/blog/%s/" % p["slug"]


# ---------------------------------------------------------------- layout
NAV = [("/", "Home"), ("/blog/", "DIY Projects"), ("/diys-for-moms/", "DIYs for Moms"),
       ("/diy-tools/", "DIY Tools"), ("/about/", "About")]

ORG = {
    "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
    "email": EMAIL, "logo": {"@type": "ImageObject", "url": SITE + "/apple-touch-icon.png", "width": 180, "height": 180},
    "sameAs": ["https://www.pinterest.com/ohmothermine/"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
           "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(items)]}


def crumbs_html(items):
    lis = []
    for i, (u, n) in enumerate(items):
        if i == len(items) - 1:
            lis.append('<li aria-current="page">%s</li>' % esc(n))
        else:
            lis.append('<li><a href="%s">%s</a></li>' % (u, esc(n)))
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">%s</ol></nav>' % "".join(lis)


def page(path, title, desc, body, schema=(), og_image="og-default.jpg", og_type="website",
         extra_head="", scripts=(), active=None, footer_alt=False, robots="index, follow", full_title=None):
    canonical = SITE + path
    t = full_title or ("%s | %s" % (title, NAME))
    graph = {"@context": "https://schema.org", "@graph": [ORG, WEBSITE] + list(schema)}
    nav = []
    for u, n in NAV:
        cur = ' aria-current="page"' if u == (active or path) else ""
        nav.append('<a href="%s"%s>%s</a>' % (u, cur, n))
    cta_cur = ' aria-current="page"' if path == "/contact/" else ""
    js = "".join('<script src="/assets/js/%s?v=%s" defer></script>' % (s, ASSET_V) for s in ("site.js",) + tuple(scripts))
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/{og_image}">
<meta name="theme-color" content="#c8553d">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Fraunces:ital,opsz,wght,SOFT@0,9..144,500..700,100;1,9..144,500..700,100&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{extra_head}<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">New: try our free <a href="/diy-tools/project-finder/">DIY Project Finder</a> and get a project matched to your time &amp; budget ✨</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="{esc(NAME)} home">{LOGO_MARK}<span class="logo-text">Oh, Mother Mine<small>DIY</small></span></a>
    <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {"".join(nav)}
      <a class="nav-cta" href="/contact/"{cta_cur}>Say hello</a>
      <div class="nav-extra"><span class="hand">Make something lovely today</span><a href="mailto:{EMAIL}" style="font-size:1rem;border:0;font-family:inherit;padding:0;opacity:1;transform:none">{EMAIL}</a></div>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
{footer(footer_alt)}
<button class="to-top" type="button" aria-label="Back to top">{icon("up")}</button>
{js}
</body>
</html>
"""


def footer(alt=False):
    cats = "".join('<li><a href="/category/%s/">%s</a></li>' % (c["slug"], esc(c["name"])) for c in CATEGORIES)
    tools = "".join('<li><a href="%s">%s</a></li>' % (t["url"], esc(t["short"])) for t in TOOLS)
    return f"""<footer class="site-footer{' on-alt' if alt else ''}">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/">{LOGO_MARK}<span class="logo-text">Oh, Mother Mine<small>DIY</small></span></a>
        <p>Budget-friendly DIY projects, furniture makeovers, kids' crafts and handmade gifts for busy moms who love a pretty, doable project.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="https://www.pinterest.com/ohmothermine/" rel="noopener" target="_blank">Find us on Pinterest →</a></p>
      </div>
      <div><h4>Projects</h4><ul>{cats}</ul></div>
      <div><h4>Free DIY tools</h4><ul>{tools}</ul></div>
      <div><h4>The site</h4><ul>
        <li><a href="/blog/">All DIY projects</a></li><li><a href="/diys-for-moms/">DIYs for moms</a></li>
        <li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li>
        <li><a href="/disclosure/">Disclosure</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© <span data-year>2026</span> {esc(NAME)}. Made with glue sticks &amp; love.</span><span>Projects are for inspiration — always follow product safety labels.</span></div>
  </div>
</footer>"""


def page_hero(crumbs, eyebrow, h1, lead, extra=""):
    return f"""<section class="page-hero">
  <div class="blob blob-1" aria-hidden="true"></div><div class="blob blob-2" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(crumbs)}
    <span class="eyebrow reveal">{esc(eyebrow)}</span>
    <h1 class="reveal" style="--d:.08s">{h1}</h1>
    <p class="lead reveal" style="--d:.16s">{lead}</p>{extra}
  </div>
</section>"""


def diff_badge(d):
    return '<span class="diff %s">%s</span>' % (d.lower(), esc(d))


def card(p, i=0, featured=False):
    c = CAT[p["category"]]
    size = "" if featured else "sm"
    return f"""<article class="card{' featured' if featured else ''} reveal" style="--d:{(i % 3) * 0.1:.1f}s" data-cat="{p['category']}" data-tilt>
  <a class="card-media" href="{url_of(p)}" tabindex="-1">{img(p['image'], p['image_alt'], size, w=720, h=480, sizes='(max-width:620px) 100vw, 60vw')}<span class="card-tag">{esc(c['name'])}</span></a>
  <div class="card-body">
    <div class="card-meta">{diff_badge(p['difficulty'])}<span>{icon('clock')}{esc(p['time'])}</span><span>{icon('wallet')}{esc(p['cost'])}</span></div>
    <h3><a href="{url_of(p)}">{esc(p['h1'])}</a></h3>
    <p>{esc(p['excerpt'])}</p>
    <a class="more" href="{url_of(p)}" aria-label="Read: {esc(p['h1'])}">Read the tutorial {icon('arrow')}</a>
  </div>
</article>"""


def newsletter():
    return f"""<section class="section"><div class="wrap">
  <div class="newsletter reveal reveal-zoom">
    <span class="hand" style="color:#ffe1d3">Psst… want the good stuff?</span>
    <h2>Get one easy project in your inbox every week</h2>
    <p>Seasonal ideas, thrift-flip inspiration and printable supply lists — no spam, unsubscribe anytime.</p>
    <form class="nl-form" action="/send.php" method="post" data-ajax>
      <input type="hidden" name="type" value="newsletter">
      <label class="hp">Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label>
      <input type="email" name="email" required placeholder="you@email.com" aria-label="Email address">
      <button class="btn" type="submit">Count me in {icon('arrow')}</button>
    </form>
    <p class="form-note" aria-live="polite"></p>
  </div>
</div></section>"""


def faq_html(items):
    return '<div class="faq">%s</div>' % "".join(
        '<details class="reveal"><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in items)


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def tool_cards(exclude=None):
    out = []
    for i, t in enumerate(TOOLS):
        if t["url"] == exclude:
            continue
        out.append(f'<a class="tool-card reveal" style="--d:{i * 0.08:.2f}s;--tc:{t["color"]}" href="{t["url"]}"><span class="ic">{icon(t["icon"])}</span><h3>{esc(t["name"])}</h3><p>{esc(t["blurb"])}</p></a>')
    return '<div class="tool-grid">%s</div>' % "".join(out)


# ---------------------------------------------------------------- pages
def build_home():
    feat, rest = POSTS[0], POSTS[1:5]
    tiles = []
    for i, c in enumerate(CATEGORIES):
        n = sum(1 for p in POSTS if p["category"] == c["slug"])
        tiles.append(f"""<a class="cat-tile reveal" style="--d:{(i % 3) * .08:.2f}s" href="/category/{c['slug']}/">{img(c['image'], c['alt'], 'sm' if i > 1 else '', w=720, h=480, sizes='(max-width:860px) 100vw, 50vw')}
  <span class="count">{n} project{"s" if n != 1 else ""}</span><span class="arrow">{icon('arrow')}</span>
  <span class="cat-body"><h3>{esc(c['name'])}</h3><p>{esc(c['tagline'])}</p></span></a>""")
    marquee_items = ["Furniture flips", "Chalk paint", "Kids' crafts", "Handmade gifts", "Cozy fall porches", "Christmas DIY", "Dollar store hacks", "Soy candles", "Mason jars", "Organizing"]
    mq = "".join("<span>%s</span>" % m for m in marquee_items) * 2
    schema = [faq_schema(HOME_FAQ), {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + url_of(p), "name": p["h1"]} for i, p in enumerate(POSTS[:6])]}]
    body = f"""<section class="hero">
  <div class="hero-media">{img('hero-living', 'Bright, cozy living room decorated with handmade pillows and thrifted furniture', lazy=False, w=1600, h=1064)}</div>
  <div class="blob blob-1" aria-hidden="true"></div><div class="blob blob-2" aria-hidden="true"></div>
  <div class="wrap">
    <div class="hero-content">
      <span class="eyebrow reveal">DIY home decor · crafts · makeovers</span>
      <h1 class="reveal" style="--d:.08s">Pretty, doable DIY for <em>busy moms<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M4 14 C 70 4, 150 4, 296 12" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></svg></em></h1>
      <p class="lead reveal" style="--d:.16s">Welcome to Oh, Mother Mine DIY — step-by-step furniture makeovers, budget home decor, kids' crafts and handmade gifts you can actually finish between school pickup and dinner.</p>
      <div class="hero-actions reveal" style="--d:.24s">
        <a class="btn" href="/blog/">Browse DIY projects {icon('arrow')}</a>
        <a class="btn btn-ghost" href="/diy-tools/project-finder/">Find my next project</a>
      </div>
      <div class="hero-badges reveal" style="--d:.32s"><span class="badge"><i></i>Budget-friendly</span><span class="badge"><i style="background:var(--mustard)"></i>Kid-approved</span><span class="badge"><i style="background:var(--clay)"></i>Step-by-step</span></div>
    </div>
  </div>
  <div class="float-card" aria-hidden="true"><span class="ic">{icon('brush')}</span><div><strong>Thrift → treasure</strong><span>Chalk paint dresser in a weekend</span></div></div>
  <div class="float-card two" aria-hidden="true"><span class="ic">{icon('heart')}</span><div><strong>Made with love</strong><span>Gifts the grandparents will keep</span></div></div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow reveal">Pick your project</span><h2 class="reveal">What are we making today?</h2></div>
  <a class="btn btn-ghost reveal" href="/blog/">See every project</a></div>
  <div class="cat-grid">{"".join(tiles)}</div>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow reveal">Fresh from the craft table</span><h2 class="reveal">Latest DIY tutorials</h2></div>
  <p class="lead reveal" style="max-width:42ch;margin:0">Every tutorial lists the time, cost and difficulty up front — so you know before you start.</p></div>
  <div class="card-grid">{card(feat, 0, True)}{"".join(card(p, i + 1) for i, p in enumerate(rest))}</div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="split-media reveal reveal-zoom">
    <div class="ba" aria-label="Before and after slider: thrifted dining set makeover">
      {img('dining-farmhouse', 'Dining room after a farmhouse makeover with painted chairs and greenery', w=1600, h=1064, sizes='(max-width:860px) 100vw, 50vw')}
      <img class="ba-before" src="/assets/img/dining-farmhouse.webp" alt="" aria-hidden="true" loading="lazy">
      <span class="ba-label l">Before</span><span class="ba-label r">After</span>
      <span class="ba-line"></span><span class="ba-handle">{icon('swap')}</span>
      <input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
    </div>
  </div>
  <div>
    <span class="eyebrow reveal">Drag the slider</span>
    <h2 class="reveal">From tired &amp; thrifted to <span class="hand">totally treasured</span></h2>
    <p class="lead reveal">Most of our favorite pieces started as curbside finds and $10 thrift-store rescues. A little sanding, the right paint and a free afternoon make all the difference.</p>
    <ul class="check-list reveal">
      <li>Beginner-proof furniture painting — no sanding marathons</li>
      <li>Our homemade chalk paint recipe costs a fraction of the store version</li>
      <li>Distressing, waxing and sealing explained in plain English</li>
    </ul>
    <a class="btn reveal" href="/category/furniture-makeovers/">Start a furniture makeover {icon('arrow')}</a>
  </div>
</div></section>

<section class="section section-sand"><div class="wrap">
  <div class="center" style="margin-bottom:44px"><span class="eyebrow reveal">Free &amp; interactive</span><h2 class="reveal">DIY tools that do the math for you</h2>
  <p class="lead reveal">Stop guessing how much paint to buy or what your makeover will really cost.</p></div>
  {tool_cards()}
</div></section>

<section class="section section-ink"><div class="wrap split rev">
  <div class="split-media reveal"><div class="photo-stack">{img('cozy-corner', 'Cozy reading corner with a teal chair and a crocheted blanket', 'sm', w=720, h=480)}{img('kid-easel', 'Child painting at an easel', 'sm', w=720, h=480)}<div class="sticker"><span>made<br>by moms</span></div></div></div>
  <div>
    <span class="eyebrow reveal" style="color:var(--blush)">Our story</span>
    <h2 class="reveal">Real-life DIY, made by moms for moms</h2>
    <p class="lead reveal">Oh, Mother Mine DIY started with a paint-splattered kitchen table, a stack of thrift-store finds and kids who wanted to "help." We share the projects that actually work in a busy family home — tested, budget-checked and explained step by step.</p>
    <a class="btn btn-light reveal" href="/about/">Read our story {icon('arrow')}</a>
    <div class="stats">
      <div class="stat reveal"><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>step-by-step tutorials</span></div>
      <div class="stat reveal" style="--d:.1s"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free DIY tools</span></div>
      <div class="stat reveal" style="--d:.2s"><b data-count="{len(CATEGORIES)}">{len(CATEGORIES)}</b><span>project categories</span></div>
      <div class="stat reveal" style="--d:.3s"><b data-count="100" data-suffix="%">100%</b><span>kitchen-table tested</span></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="split-media reveal"><div class="photo-stack">{img('craft-tin', 'Tin box filled with ribbons, twine and craft supplies', 'sm', w=720, h=480)}{img('candle-jar', 'Handmade candle in a glass jar on a stack of books', 'sm', w=720, h=480)}</div></div>
  <div>
    <span class="eyebrow reveal">Start here</span>
    <h2 class="reveal">DIYs for moms: the beginner's guide</h2>
    <p class="lead reveal">New to DIY, short on time, or crafting with little ones underfoot? Our DIYs for moms guide walks you through the starter toolkit, quick wins and the projects worth your naptime.</p>
    <a class="btn reveal" href="/diys-for-moms/">Read the guide {icon('arrow')}</a>
  </div>
</div></section>

<section class="section section-alt"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><span class="eyebrow reveal">Good questions</span><h2 class="reveal">DIY questions moms ask us most</h2></div>
  <div style="display:flex;justify-content:center">{faq_html(HOME_FAQ)}</div>
</div></section>
{newsletter()}"""
    return page("/", "DIY Home Decor, Crafts & Furniture Makeovers for Moms",
                "Oh, Mother Mine DIY shares easy DIY home decor, chalk paint furniture makeovers, kids' crafts and handmade gifts for busy moms — plus free DIY calculators.",
                body, schema, og_image="og-default.jpg",
                full_title="Oh, Mother Mine DIY — Easy DIY Home Decor & Crafts for Moms")


def render_body(p):
    def fig(m):
        parts = [x.strip() for x in m.group(1).split("|")]
        key, alt = parts[0], parts[1] if len(parts) > 1 else ""
        cap = parts[2] if len(parts) > 2 and parts[2] else ""
        return '<figure class="reveal">%s%s</figure>' % (
            img(key, alt, "sm", w=720, h=480), "<figcaption>%s</figcaption>" % esc(cap) if cap else "")
    b = re.sub(r"\{\{img:([^}]+)\}\}", fig, p["body"])
    return b


def toc_of(body):
    return re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)


def related(p, n=3):
    same = [x for x in POSTS if x["category"] == p["category"] and x["slug"] != p["slug"]]
    other = [x for x in POSTS if x["category"] != p["category"]]
    return (same + other)[:n]


def build_post(p):
    c = CAT[p["category"]]
    body = render_body(p)
    toc = toc_of(body)
    crumbs = [("/", "Home"), ("/blog/", "DIY Projects"), ("/category/%s/" % c["slug"], c["name"]), (url_of(p), p["h1"])]
    supplies = ""
    if p["supplies"]:
        supplies = ('<div class="supplies" data-key="%s"><h2 id="supplies">What you\'ll need</h2><ul>%s</ul><p class="hint">Tap items to check them off — we\'ll remember your list on this device.</p></div>'
                    % (p["slug"], "".join("<li>%s</li>" % esc(s) for s in p["supplies"])))
    toc_html = "".join('<li><a href="#%s">%s</a></li>' % (i, re.sub("<[^>]+>", "", t)) for i, t in toc)
    words = len(re.sub("<[^>]+>", " ", p["body"]).split())
    rel_tool = next((t for t in TOOLS if t["url"] in p["body"]), TOOLS[2])
    share_url = SITE + url_of(p)
    pin = "https://www.pinterest.com/pin/create/button/?url=%s&media=%s&description=%s" % (
        share_url, SITE + "/assets/img/%s.webp" % p["image"], html.escape(p["h1"]).replace(" ", "%20"))
    fb = "https://www.facebook.com/sharer/sharer.php?u=" + share_url
    schema = [
        {"@type": "BlogPosting", "@id": share_url + "#article", "headline": p["h1"], "description": p["description"],
         "image": SITE + "/assets/img/%s.webp" % p["image"], "datePublished": p["date"], "dateModified": p["date"],
         "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": share_url,
         "articleSection": c["name"], "keywords": p["keyword"], "wordCount": words, "inLanguage": "en-US"},
        crumbs_schema(crumbs), faq_schema(p["faq"]),
    ]
    page_body = f"""<div class="reading-progress" aria-hidden="true"></div>
<article>
<header class="post-hero">
  <div class="blob blob-1" aria-hidden="true" style="left:auto;right:-160px;top:-160px"></div>
  <div class="wrap">
    {crumbs_html(crumbs)}
    <a class="eyebrow reveal" href="/category/{c['slug']}/" style="text-decoration:none">{esc(c['name'])}</a>
    <h1 class="reveal" style="--d:.08s">{esc(p['h1'])}</h1>
    <div class="post-meta reveal" style="--d:.16s"><span>{icon('cal')}<time datetime="{p['date']}">{fmt_date(p['date'])}</time></span><span>{icon('clock')}{max(3, round(words / 230))} min read</span><span>{icon('heart')}By the {esc(NAME)} team</span></div>
    <div class="post-cover reveal reveal-zoom">{img(p['image'], p['image_alt'], lazy=False, w=1600, h=1064)}</div>
    <div class="project-facts reveal"><div><small>Difficulty</small><b>{esc(p['difficulty'])}</b></div><div><small>Time</small><b>{esc(p['time'])}</b></div><div><small>Cost</small><b>{esc(p['cost'])}</b></div></div>
  </div>
</header>
<div class="wrap post-layout">
  <div class="prose">
    {supplies}
    {body}
    <h2 id="faq">Frequently asked questions</h2>
    {faq_html(p['faq'])}
    <div class="share"><b>Share this project:</b>
      <a href="{esc(pin)}" target="_blank" rel="noopener" aria-label="Save to Pinterest">{icon('pin')}</a>
      <a href="{esc(fb)}" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon('fb')}</a>
      <a href="mailto:?subject={esc(p['h1'])}&amp;body={share_url}" aria-label="Share by email">{icon('mail')}</a>
      <button type="button" data-copy-link aria-label="Copy link">{icon('link')}</button>
    </div>
    <div class="author-box">{LOGO_MARK}<div><b>Written by the {esc(NAME)} team</b><p>We're moms who test every project at our own kitchen tables before it goes on the blog. Questions? <a href="/contact/">Drop us a line</a>.</p></div></div>
  </div>
  <aside class="sidebar"><div class="sidebar-inner">
    <nav class="side-box toc" aria-label="On this page"><h3>On this page</h3><ol>{('<li><a href="#supplies">What you&#x27;ll need</a></li>' if supplies else '') + toc_html}<li><a href="#faq">FAQ</a></li></ol></nav>
    <div class="side-box side-cta"><h3>{esc(rel_tool['name'])}</h3><p>{esc(rel_tool['blurb'])}</p><a class="btn" href="{rel_tool['url']}">Try it free {icon('arrow')}</a></div>
  </div></aside>
</div>
</article>
<section class="section section-alt" style="padding-top:70px"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">Keep crafting</span><h2>You might also love</h2></div><a class="btn btn-ghost" href="/category/{c['slug']}/">More {esc(c['name'].lower())}</a></div>
  <div class="card-grid">{"".join(card(r, i) for i, r in enumerate(related(p)))}</div>
</div></section>"""
    return page(url_of(p), p["title"], p["description"], page_body, schema,
                og_image="%s.webp" % p["image"], og_type="article", active="/blog/", footer_alt=True,
                extra_head='<meta property="article:published_time" content="%sT08:00:00-05:00">\n<meta property="article:section" content="%s">\n' % (p["date"], esc(c["name"])))


def build_blog_index():
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All projects</button>' + "".join(
        '<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s</button>' % (c["slug"], esc(c["name"])) for c in CATEGORIES)
    crumbs = [("/", "Home"), ("/blog/", "DIY Projects")]
    body = page_hero(crumbs, "The DIY project library", "All DIY projects &amp; tutorials",
                     "Furniture makeovers, budget home decor, holiday DIY, kids' crafts and handmade gifts — filter by category or search for exactly what you want to make.")
    body += f"""<section class="section" style="padding-top:20px"><div class="wrap">
  <div class="search-box">{icon('search')}<input type="search" placeholder="Search projects (try “candle” or “wreath”)" aria-label="Search projects" data-search></div>
  <div class="chips" role="group" aria-label="Filter by category">{chips}</div>
  <div class="card-grid" data-filter-grid>{"".join(card(p, i) for i, p in enumerate(POSTS))}</div>
  <p class="empty-msg">No projects match that search yet — try another word, or <a href="/contact/">suggest a project</a>!</p>
</div></section>{newsletter()}"""
    schema = [crumbs_schema(crumbs), {"@type": "CollectionPage", "name": "DIY Projects", "url": SITE + "/blog/",
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": SITE + url_of(p)} for i, p in enumerate(POSTS)]}}]
    return page("/blog/", "DIY Projects & Tutorials for Home, Kids and Gifts",
                "Browse every Oh, Mother Mine DIY tutorial: chalk paint furniture makeovers, budget home decor, holiday DIY, kids' crafts, handmade gifts and organizing ideas.",
                body, schema)


def build_category(c):
    posts = [p for p in POSTS if p["category"] == c["slug"]]
    crumbs = [("/", "Home"), ("/blog/", "DIY Projects"), ("/category/%s/" % c["slug"], c["name"])]
    body = page_hero(crumbs, "Category", esc(c["h1"]), esc(c["intro"]))
    body += f"""<section class="section" style="padding-top:20px"><div class="wrap">
  <div class="card-grid">{"".join(card(p, i) for i, p in enumerate(posts))}</div>
</div></section>
<section class="section section-alt"><div class="wrap split">
  <div class="split-media reveal">{img(c['image'], c['alt'], 'sm', cls='', w=720, h=480).replace('<img ', '<img style="border-radius:22px;box-shadow:var(--shadow)" ')}</div>
  <div class="prose reveal">{c['body']}</div>
</div></section>
<section class="section section-sand"><div class="wrap"><div class="center" style="margin-bottom:36px"><h2>Helpful free tools</h2></div>{tool_cards()}</div></section>"""
    schema = [crumbs_schema(crumbs), {"@type": "CollectionPage", "name": c["h1"], "url": SITE + "/category/%s/" % c["slug"],
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": SITE + url_of(p)} for i, p in enumerate(posts)]}}]
    return page("/category/%s/" % c["slug"], c["title"], c["description"], body, schema,
                og_image="%s.webp" % c["image"], active="/blog/")


def build_pillar():
    crumbs = [("/", "Home"), ("/diys-for-moms/", "DIYs for Moms")]
    picks = [BY_SLUG[s] for s in PILLAR["picks"]]
    body = page_hero(crumbs, "The beginner's guide", esc(PILLAR["h1"]), esc(PILLAR["lead"]),
                     '<div class="hero-actions reveal" style="--d:.24s"><a class="btn" href="#quick-wins">Jump to quick wins %s</a><a class="btn btn-ghost" href="/diy-tools/project-finder/">Take the project quiz</a></div>' % icon("arrow"))
    body += f"""<section class="section" style="padding-top:10px"><div class="wrap split">
  <div class="split-media reveal"><div class="photo-stack">{img('art-studio', 'Craft table full of paint jars and brushes', 'sm', w=720, h=480)}{img('brush-cup', 'Cup of paintbrushes on a bright table', 'sm', w=720, h=480)}<div class="sticker"><span>start<br>here!</span></div></div></div>
  <div class="prose reveal">{PILLAR['intro']}</div>
</div></section>
<section class="section section-sand"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><span class="eyebrow">The mom-proof method</span><h2>How to actually finish a DIY project</h2></div>
  <div class="pillar-steps">{"".join('<div class="pillar-step reveal" style="--d:%.2fs"><h3>%s</h3><p>%s</p></div>' % (i * .08, esc(t), esc(d)) for i, (t, d) in enumerate(PILLAR['steps']))}</div>
</div></section>
<section class="section" id="quick-wins"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">Quick wins</span><h2>Our favorite DIYs for moms</h2></div></div>
  <div class="card-grid">{"".join(card(p, i) for i, p in enumerate(picks))}</div>
</div></section>
<section class="section section-alt"><div class="wrap split rev">
  <div class="split-media reveal">{img('screws-organizer', 'Organized compartment box of screws and hardware', 'sm', w=720, h=480).replace('<img ', '<img style="border-radius:22px;box-shadow:var(--shadow)" ')}</div>
  <div class="prose reveal">{PILLAR['toolkit']}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><h2>DIYs for moms: FAQ</h2></div>
  <div style="display:flex;justify-content:center">{faq_html(PILLAR['faq'])}</div>
</div></section>
<section class="section section-sand"><div class="wrap"><div class="center" style="margin-bottom:36px"><h2>Free tools to plan your next project</h2></div>{tool_cards()}</div></section>
{newsletter()}"""
    schema = [crumbs_schema(crumbs), faq_schema(PILLAR["faq"]),
              {"@type": "Article", "headline": PILLAR["h1"], "description": PILLAR["description"], "author": {"@id": SITE + "/#org"},
               "publisher": {"@id": SITE + "/#org"}, "datePublished": "2026-06-01", "dateModified": TODAY,
               "image": SITE + "/assets/img/art-studio.webp", "mainEntityOfPage": SITE + "/diys-for-moms/"}]
    return page("/diys-for-moms/", PILLAR["title"], PILLAR["description"], body, schema, og_image="art-studio.webp")


def build_tools_hub():
    crumbs = [("/", "Home"), ("/diy-tools/", "DIY Tools")]
    body = page_hero(crumbs, "Free & interactive", "Free DIY tools &amp; calculators",
                     "Plan smarter before you pick up a brush. Calculate paint, mix homemade chalk paint, budget a room makeover, build a color palette or let our quiz pick your next project.")
    body += f'<section class="section" style="padding-top:20px"><div class="wrap">{tool_cards()}</div></section>{newsletter()}'
    schema = [crumbs_schema(crumbs), {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + t["url"], "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    return page("/diy-tools/", "Free DIY Tools: Paint Calculator, Chalk Paint Mixer & More",
                "Free DIY tools from Oh, Mother Mine DIY: a paint calculator, homemade chalk paint mixer, project quiz, budget planner and palette generator.",
                body, schema, og_image="paint-cans.webp")


SWATCHES = ["#c8553d", "#7f9c86", "#e5a442", "#6b4a63", "#3d5a80", "#f3e8da", "#2a1f1a"]


def swatch_row(name="swatch"):
    return '<div class="swatch-row" role="radiogroup" aria-label="Preview color">%s</div>' % "".join(
        '<label><input type="radio" name="%s" value="%s"%s aria-label="%s"><span style="--c:%s"></span></label>'
        % (name, c, " checked" if i == 1 else "", c, c) for i, c in enumerate(SWATCHES))


def tool_page(t, widget, extra_html="", schema_extra=()):
    crumbs = [("/", "Home"), ("/diy-tools/", "DIY Tools"), (t["url"], t["name"])]
    body = page_hero(crumbs, "Free DIY tool", esc(t["h1"]), esc(t["lead"]))
    body += f"""<section class="section" style="padding-top:10px"><div class="wrap">{widget}</div></section>
<section class="section section-alt"><div class="wrap"><div class="prose" style="margin:0 auto">{t['guide']}<h2 id="faq">FAQ</h2>{faq_html(t['faq'])}</div></div></section>
{extra_html}
<section class="section"><div class="wrap"><div class="center" style="margin-bottom:36px"><h2>More free DIY tools</h2></div>{tool_cards(exclude=t['url'])}</div></section>"""
    schema = [crumbs_schema(crumbs), faq_schema(t["faq"]),
              {"@type": "WebApplication", "name": t["name"], "url": SITE + t["url"], "applicationCategory": "UtilitiesApplication",
               "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": t["description"]}] + list(schema_extra)
    return page(t["url"], t["title"], t["description"], body, schema, scripts=("tools.js",), active="/diy-tools/",
                og_image="%s.webp" % t["image"], footer_alt=False)


def W_paint():
    return f"""<div class="tool-shell" data-tool="paint">
  <div class="panel">
    <div class="seg" data-seg="mode" role="group" aria-label="What are you painting?"><button type="button" data-val="walls" aria-pressed="true">Walls &amp; rooms</button><button type="button" data-val="furniture" aria-pressed="false">Furniture</button></div>
    <div data-mode-panel="walls">
      <div class="field-row">
        <div class="field"><label for="pc-len">Room length <output id="o-len"></output></label><input id="pc-len" type="range" min="4" max="40" value="14" data-out="o-len" data-unit=" ft"></div>
        <div class="field"><label for="pc-wid">Room width <output id="o-wid"></output></label><input id="pc-wid" type="range" min="4" max="40" value="12" data-out="o-wid" data-unit=" ft"></div>
      </div>
      <div class="field"><label for="pc-ht">Wall height <output id="o-ht"></output></label><input id="pc-ht" type="range" min="7" max="16" value="8" data-out="o-ht" data-unit=" ft"></div>
      <div class="field-row">
        <div class="field"><label for="pc-doors">Doors</label><input id="pc-doors" type="number" min="0" max="10" value="1"></div>
        <div class="field"><label for="pc-wins">Windows</label><input id="pc-wins" type="number" min="0" max="20" value="2"></div>
      </div>
      <div class="field"><label for="pc-surface">Wall surface</label><select id="pc-surface"><option value="400">Smooth, previously painted</option><option value="350" selected>Average / light texture</option><option value="275">Heavy texture or new drywall</option></select></div>
      <div class="field"><label><span><input id="pc-ceiling" type="checkbox"> Include the ceiling</span></label><label><span><input id="pc-primer" type="checkbox"> I need primer (big color change or bare drywall)</span></label></div>
    </div>
    <div data-mode-panel="furniture" hidden>
      <div class="field"><label for="pc-piece">Piece of furniture</label><select id="pc-piece"><option value="side-table">Side / end table</option><option value="nightstand">Nightstand</option><option value="chair">Dining chair</option><option value="coffee-table">Coffee table</option><option value="dining-table">Dining table</option><option value="bookshelf">Bookshelf</option><option value="dresser" selected>Dresser (6 drawers)</option><option value="buffet">Buffet / sideboard</option><option value="kitchen-island">Kitchen island</option></select></div>
      <div class="field"><label for="pc-qty">How many? <output id="o-qty"></output></label><input id="pc-qty" type="range" min="1" max="8" value="1" data-out="o-qty"></div>
      <div class="field"><label><span><input id="pc-inside" type="checkbox"> Paint the insides / drawer boxes too</span></label></div>
    </div>
    <div class="field"><label for="pc-coats">Coats <output id="o-coats"></output></label><input id="pc-coats" type="range" min="1" max="3" value="2" data-out="o-coats"></div>
    <div class="field"><label for="pc-price">Price per gallon ($)</label><input id="pc-price" type="number" min="5" max="150" value="40"></div>
    <div class="field"><span class="lbl">Preview color</span>{swatch_row()}</div>
  </div>
  <div class="result" aria-live="polite">
    <h2>You'll need about</h2>
    <div><span class="big-num" id="pc-big">0</span> <span class="unit" id="pc-unit">gallons</span></div>
    <div class="cans" id="pc-cans" aria-hidden="true"></div>
    <ul class="result-list" id="pc-list"></ul>
    <p class="note">Estimates assume standard doors (20 sq ft) and windows (15 sq ft). Always check the coverage on your paint can — and buy from one batch so the color matches.</p>
  </div>
</div>"""


def W_chalk():
    return f"""<div class="tool-shell" data-tool="chalk">
  <div class="panel">
    <span class="lbl" style="font-weight:700;display:block;margin-bottom:8px">Choose your recipe</span>
    <div class="seg" data-seg="recipe" role="group" aria-label="Recipe"><button type="button" data-val="plaster" aria-pressed="true">Plaster of Paris</button><button type="button" data-val="calcium" aria-pressed="false">Calcium carbonate</button><button type="button" data-val="soda" aria-pressed="false">Baking soda</button></div>
    <div class="field"><label for="cm-cups">Latex paint <output id="o-cups"></output></label><input id="cm-cups" type="range" min="0.5" max="8" step="0.5" value="2" data-out="o-cups" data-unit=" cups"></div>
    <div class="field"><span class="lbl">Paint color</span>{swatch_row()}</div>
    <svg viewBox="0 0 200 210" width="180" style="display:block;margin:10px auto 0" aria-hidden="true">
      <defs><clipPath id="jarclip"><rect x="40" y="40" width="120" height="150" rx="18"/></clipPath></defs>
      <rect x="55" y="18" width="90" height="24" rx="6" fill="#d5c7ba"/>
      <g clip-path="url(#jarclip)"><rect id="cm-jar-fill" x="40" y="140" width="120" height="50" fill="#7f9c86" style="transition:all .5s"/></g>
      <rect x="40" y="40" width="120" height="150" rx="18" fill="none" stroke="#2a1f1a" stroke-width="4"/>
      <path d="M60 60v100" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".5"/>
    </svg>
  </div>
  <div class="result" aria-live="polite">
    <h2>Your chalk paint recipe</h2>
    <ul class="result-list" id="cm-list"></ul>
    <p style="margin:22px 0 0">Covers roughly</p>
    <div><span class="big-num" id="cm-big">0</span> <span class="unit">sq ft per coat</span></div>
    <p>That's enough for <b id="cm-fits" style="color:#fff"></b>.</p>
    <p class="note" id="cm-note"></p>
  </div>
</div>"""


def W_quiz():
    data = [{"slug": p["slug"], "title": p["h1"], "url": url_of(p), "img": "/assets/img/%s-sm.webp" % p["image"], "alt": p["image_alt"],
             "cat": p["category"], "diff": p["difficulty"], "time": p["time"], "cost": p["cost"], "excerpt": p["excerpt"]} for p in POSTS]
    qs = [
        ("who", "Who are you making it with — or for?", [("🏡", "My home", "Decor & makeovers", "home"), ("🧒", "With the kids", "Mess-friendly fun", "kids"), ("🎁", "As a gift", "Handmade & heartfelt", "gift")]),
        ("time", "How much time do you have?", [("⚡", "Under an hour", "Naptime-sized", "quick"), ("☕", "An afternoon", "2–4 hours", "afternoon"), ("🗓️", "A whole weekend", "Let's go big", "weekend")]),
        ("budget", "What's your budget?", [("🪙", "Under $15", "Use what I have", "low"), ("💵", "$15–$50", "A small splurge", "mid"), ("💳", "$50+", "Worth it", "high")]),
        ("vibe", "Pick a vibe", [("🪵", "Cozy farmhouse", "Wood, wreaths, chalk paint", "farmhouse"), ("🌿", "Fresh & bright", "Plants, color, light", "fresh"), ("🎃", "Seasonal", "Holiday & porch decor", "seasonal"), ("🧺", "Organized", "Calm, clutter-free", "organized")]),
    ]
    steps = []
    for i, (k, q, opts) in enumerate(qs):
        o = "".join('<button type="button" class="q-opt" data-val="%s"><span class="emo" aria-hidden="true">%s</span><b>%s</b><span>%s</span></button>' % (v, e, esc(t), esc(s)) for e, t, s, v in opts)
        back = '<button type="button" class="q-back">← Back</button>' if i else ""
        steps.append('<div class="q-step" data-q="%s"><span class="eyebrow">Question %d of %d</span><h2>%s</h2><div class="q-opts">%s</div>%s</div>' % (k, i + 1, len(qs), esc(q), o, back))
    steps.append('<div class="q-step q-results"><span class="eyebrow">Your matches</span><h2>Here\'s what we\'d make next 🎉</h2><div class="card-grid" id="quiz-results"></div><button type="button" class="btn btn-ghost q-restart" style="margin-top:30px">Take the quiz again</button></div>')
    return '<div class="quiz panel" data-tool="quiz"><div class="quiz-progress" aria-hidden="true"><i></i></div>%s<script type="application/json" id="quiz-data">%s</script></div>' % (
        "".join(steps), json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))


def W_budget():
    return f"""<div class="tool-shell" data-tool="budget">
  <div class="panel">
    <div class="field"><label for="bp-room">Room preset</label><select id="bp-room"><option value="living">Living room refresh</option><option value="bedroom">Bedroom makeover</option><option value="kitchen">Kitchen update</option><option value="kids">Kids' room</option><option value="porch">Front porch</option></select></div>
    <div class="field"><label for="bp-budget">Your total budget <output id="o-budget"></output></label><input id="bp-budget" type="range" min="50" max="2000" step="25" value="400" data-out="o-budget" data-prefix="$"></div>
    <div class="budget-row budget-head" aria-hidden="true"><span>Item</span><span>DIY $</span><span>Store $</span><span></span></div>
    <div id="bp-rows"></div>
    <button type="button" class="btn btn-ghost" id="bp-add" style="margin-top:8px;padding:10px 20px">+ Add item</button>
    <div class="field" style="margin-top:20px"><label><span><input id="bp-buffer" type="checkbox" checked> Add a 10% "oops" buffer (trust us)</span></label></div>
  </div>
  <div class="result" aria-live="polite">
    <h2>Your DIY makeover total</h2>
    <span class="big-num" id="bp-big">$0</span>
    <div class="meter"><i id="bp-meter"></i></div>
    <p id="bp-status" style="margin:0;color:#fff;font-weight:700"></p>
    <svg class="donut" viewBox="0 0 160 160" aria-hidden="true"><circle cx="80" cy="80" r="60" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="20"/><circle id="bp-donut-diy" cx="80" cy="80" r="60" fill="none" stroke="#e5a442" stroke-width="20" stroke-dasharray="0 400" transform="rotate(-90 80 80)" style="transition:stroke-dasharray .6s"/><text x="80" y="78" text-anchor="middle" fill="#fff" font-family="Fraunces, serif" font-size="30" id="bp-donut-label">0%</text><text x="80" y="100" text-anchor="middle" fill="#d9c9bb" font-size="12">saved</text></svg>
    <ul class="result-list" id="bp-list"></ul>
    <p class="note">Store-bought prices are typical planning numbers for new items — edit any row to match your own quotes.</p>
  </div>
</div>"""


def W_palette():
    presets = [("#c8553d", "Terracotta"), ("#7f9c86", "Sage"), ("#3d5a80", "Denim"), ("#e5a442", "Honey"), ("#6b4a63", "Plum"), ("#b7a48f", "Greige")]
    pb = "".join('<button type="button" class="chip" data-preset="%s"><span style="display:inline-block;width:12px;height:12px;border-radius:50%%;background:%s;margin-right:6px;vertical-align:-1px"></span>%s</button>' % (h, h, n) for h, n in presets)
    return f"""<div data-tool="palette">
  <div class="tool-shell">
    <div class="panel">
      <div class="color-pick" style="margin-bottom:20px"><input type="color" id="cp-base" value="#7f9c86" aria-label="Base color"><div><b>Your base color</b><br><span id="cp-hex" style="font-family:var(--ff-display);font-size:1.4rem"></span></div>
      <button type="button" class="btn" id="cp-random" style="margin-left:auto">{icon('sparkle')} Surprise me</button></div>
      <div class="chips" style="margin-bottom:18px">{pb}</div>
      <span class="lbl" style="font-weight:700;display:block;margin-bottom:8px">Color harmony</span>
      <div class="seg" data-seg="harmony" role="group" aria-label="Color harmony"><button type="button" data-val="analogous" aria-pressed="true">Analogous</button><button type="button" data-val="complementary" aria-pressed="false">Complementary</button><button type="button" data-val="triadic" aria-pressed="false">Triadic</button><button type="button" data-val="split" aria-pressed="false">Split</button><button type="button" data-val="mono" aria-pressed="false">Monochrome</button></div>
      <div class="palette" id="cp-palette" aria-live="polite"></div>
      <p style="font-size:.88rem;color:var(--muted);margin-top:10px">Tap a color to copy its hex code.</p>
    </div>
    <div class="result">
      <h2>See it in a room</h2>
      <div class="room-preview"><svg viewBox="0 0 640 360" role="img" aria-label="Living room preview using your palette">
        <rect id="rp-wall" width="640" height="270" fill="#eee"/>
        <rect id="rp-floor" y="270" width="640" height="90" fill="#6b5a4c"/>
        <rect id="rp-art" x="250" y="50" width="140" height="95" rx="6" fill="#ccc" stroke="#fff" stroke-width="8"/>
        <ellipse id="rp-rug" cx="320" cy="318" rx="250" ry="30" fill="#ddd"/>
        <rect id="rp-sofa" x="150" y="190" width="340" height="90" rx="26" fill="#999"/>
        <rect x="130" y="210" width="50" height="80" rx="18" fill="#000" opacity=".12"/><rect x="460" y="210" width="50" height="80" rx="18" fill="#000" opacity=".12"/>
        <rect id="rp-pillow" x="190" y="170" width="70" height="55" rx="14" fill="#c8553d"/>
        <rect x="380" y="172" width="70" height="52" rx="14" fill="#fff" opacity=".7"/>
        <rect x="540" y="200" width="16" height="80" fill="#2a1f1a" opacity=".6"/><path id="rp-vase" d="M530 200 q18 -60 36 0 z" fill="#555"/>
        <circle cx="548" cy="120" r="34" fill="#7f9c86" opacity=".8"/><rect x="545" y="140" width="6" height="60" fill="#2a1f1a" opacity=".5"/>
      </svg></div>
      <ul class="result-list" id="cp-tips"></ul>
      <p class="note">Designers' 60-30-10 rule: 60% main color on walls, 30% on large pieces, 10% accent in pillows, art and accessories.</p>
    </div>
  </div>
</div>"""


WIDGETS = {"paint-calculator": W_paint, "chalk-paint-mixer": W_chalk, "project-finder": W_quiz,
           "makeover-budget-planner": W_budget, "color-palette-generator": W_palette}


def build_about():
    crumbs = [("/", "Home"), ("/about/", "About")]
    from content.pages import ABOUT
    body = page_hero(crumbs, "Hello, friend", "About Oh, Mother Mine DIY", esc(ABOUT["lead"]))
    body += f"""<section class="section" style="padding-top:10px"><div class="wrap split">
  <div class="split-media reveal"><div class="photo-stack">{img('sewing-kit', 'Colorful thread spools, scissors and pins from a sewing kit', 'sm', w=720, h=480)}{img('kids-clay', 'Kids shaping clay at a craft table', 'sm', w=720, h=480)}<div class="sticker"><span>since<br>day one</span></div></div></div>
  <div class="prose reveal">{ABOUT['story']}</div>
</div></section>
<section class="section section-sand"><div class="wrap">
  <div class="center" style="margin-bottom:40px"><span class="eyebrow">What we believe</span><h2>Our DIY promises</h2></div>
  <div class="pillar-steps">{"".join('<div class="pillar-step reveal" style="--d:%.2fs"><h3>%s</h3><p>%s</p></div>' % (i * .08, esc(t), esc(d)) for i, (t, d) in enumerate(ABOUT['values']))}</div>
</div></section>
<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Start here</span><h2>Reader favorites</h2></div></div>
<div class="card-grid">{"".join(card(BY_SLUG[s], i) for i, s in enumerate(ABOUT['favorites']))}</div></div></section>
{newsletter()}"""
    return page("/about/", "About Us — DIY Made by Moms, for Moms",
                "Meet Oh, Mother Mine DIY: a home decor and crafts blog sharing budget-friendly, kitchen-table-tested DIY projects, furniture makeovers and kids' crafts.",
                body, [crumbs_schema(crumbs), {"@type": "AboutPage", "url": SITE + "/about/", "name": "About Oh, Mother Mine DIY"}])


def build_contact():
    crumbs = [("/", "Home"), ("/contact/", "Contact")]
    body = page_hero(crumbs, "Say hello", "Contact Oh, Mother Mine DIY",
                     "Questions about a project, a tutorial request, or a collaboration idea? We read every message and usually reply within two business days.")
    body += f"""<section class="section" style="padding-top:10px"><div class="wrap tool-shell">
  <form class="panel" action="/send.php" method="post" data-ajax>
    <input type="hidden" name="type" value="contact">
    <label class="hp">Leave this empty <input name="website" tabindex="-1" autocomplete="off"></label>
    <div class="field-row"><div class="field"><label for="c-name">Your name</label><input id="c-name" type="text" name="name" required autocomplete="name"></div>
    <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div></div>
    <div class="field"><label for="c-topic">What's it about?</label><select id="c-topic" name="topic"><option>A question about a project</option><option>Tutorial request</option><option>Collaboration / brand partnership</option><option>Something else</option></select></div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>
    <button class="btn" type="submit">Send message {icon('arrow')}</button>
    <p class="form-note" aria-live="polite"></p>
  </form>
  <div class="contact-cards">
    <div class="contact-card reveal"><span class="ic">{icon('mail')}</span><div><b>Email us</b><br><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
    <div class="contact-card reveal" style="--d:.08s"><span class="ic">{icon('pin')}</span><div><b>Pin with us</b><br><a href="https://www.pinterest.com/ohmothermine/" target="_blank" rel="noopener">pinterest.com/ohmothermine</a></div></div>
    <div class="contact-card reveal" style="--d:.16s"><span class="ic">{icon('sparkle')}</span><div><b>Request a tutorial</b><br>Tell us what you'd love to make — reader ideas shape our project list.</div></div>
    {img('flowers-table', 'Fresh white flowers in an enamel pitcher on a wooden table', 'sm', w=720, h=480).replace('<img ', '<img style="border-radius:22px;box-shadow:var(--shadow-sm);aspect-ratio:16/10;object-fit:cover" ')}
  </div>
</div></section>"""
    return page("/contact/", "Contact Us",
                "Contact Oh, Mother Mine DIY with project questions, tutorial requests or collaboration ideas. Email info@ohmtoherminediy.com or use our contact form.",
                body, [crumbs_schema(crumbs), {"@type": "ContactPage", "url": SITE + "/contact/", "name": "Contact Oh, Mother Mine DIY"}])


def build_legal(slug, title, desc, content):
    crumbs = [("/", "Home"), ("/%s/" % slug, title)]
    body = page_hero(crumbs, "The fine print", esc(title), "Last updated %s." % fmt_date(TODAY))
    body += '<section class="section" style="padding-top:10px"><div class="wrap"><div class="prose legal">%s</div></div></section>' % content
    return page("/%s/" % slug, title, desc, body, [crumbs_schema(crumbs)])


def build_sitemap_page():
    crumbs = [("/", "Home"), ("/sitemap/", "Sitemap")]
    body = page_hero(crumbs, "Find your way", "Sitemap", "Every page on Oh, Mother Mine DIY in one place.")
    sec = []
    sec.append("<h2>Main pages</h2><ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (u, n) for u, n in NAV + [("/contact/", "Contact")]))
    for c in CATEGORIES:
        items = "".join('<li><a href="%s">%s</a></li>' % (url_of(p), esc(p["h1"])) for p in POSTS if p["category"] == c["slug"])
        sec.append('<h2><a href="/category/%s/">%s</a></h2><ul>%s</ul>' % (c["slug"], esc(c["name"]), items))
    sec.append("<h2>DIY tools</h2><ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (t["url"], esc(t["name"])) for t in TOOLS))
    sec.append('<h2>Legal</h2><ul><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li><li><a href="/disclosure/">Disclosure</a></li></ul>')
    body += '<section class="section" style="padding-top:10px"><div class="wrap prose" style="max-width:none">%s</div></section>' % "".join(sec)
    return page("/sitemap/", "Sitemap", "Browse every page on Oh, Mother Mine DIY: DIY project tutorials by category, free DIY tools, and site information pages.", body, [crumbs_schema(crumbs)])


def build_404():
    body = f"""<section class="notfound"><div class="wrap">
  <div class="big">4<span class="hand" style="font-size:1em">0</span>4</div>
  <h1>Oops — this page got glued to the craft table</h1>
  <p class="lead" style="margin:0 auto 30px">The page you're looking for has moved or never existed. Try one of these instead:</p>
  <div class="hero-actions" style="justify-content:center"><a class="btn" href="/blog/">Browse DIY projects {icon('arrow')}</a><a class="btn btn-ghost" href="/">Go home</a></div>
</div></section>
<section class="section section-alt"><div class="wrap"><h2 class="center">Popular projects</h2><div class="card-grid">{"".join(card(p, i) for i, p in enumerate(POSTS[:3]))}</div></div></section>"""
    return page("/404.html", "Page Not Found", "This page could not be found. Browse DIY projects and free tools from Oh, Mother Mine DIY.", body, robots="noindex, follow")


# ---------------------------------------------------------------- output
def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for fn in os.listdir(os.path.join(SRC, "root")):
        shutil.copy(os.path.join(SRC, "root", fn), os.path.join(OUT, fn))

    from content.pages import PRIVACY, TERMS, DISCLOSURE
    urls = []  # (path, lastmod, priority)
    write("/home.html", build_home()); urls.append(("/", TODAY, "1.0"))
    write("/blog/", build_blog_index()); urls.append(("/blog/", TODAY, "0.9"))
    write("/diys-for-moms/", build_pillar()); urls.append(("/diys-for-moms/", TODAY, "0.9"))
    for c in CATEGORIES:
        write("/category/%s/" % c["slug"], build_category(c)); urls.append(("/category/%s/" % c["slug"], TODAY, "0.8"))
    for p in POSTS:
        write(url_of(p), build_post(p)); urls.append((url_of(p), p["date"], "0.8"))
    write("/diy-tools/", build_tools_hub()); urls.append(("/diy-tools/", TODAY, "0.8"))
    for t in TOOLS:
        write(t["url"], tool_page(t, WIDGETS[t["url"].strip("/").split("/")[-1]]())); urls.append((t["url"], TODAY, "0.8"))
    write("/about/", build_about()); urls.append(("/about/", TODAY, "0.6"))
    write("/contact/", build_contact()); urls.append(("/contact/", TODAY, "0.5"))
    write("/privacy-policy/", build_legal("privacy-policy", "Privacy Policy", "How Oh, Mother Mine DIY collects, uses and protects information from visitors, newsletter subscribers and people who contact us.", PRIVACY)); urls.append(("/privacy-policy/", TODAY, "0.2"))
    write("/terms/", build_legal("terms", "Terms of Use", "The terms that apply when you use Oh, Mother Mine DIY, including project safety, content use and our free interactive DIY tools.", TERMS)); urls.append(("/terms/", TODAY, "0.2"))
    write("/disclosure/", build_legal("disclosure", "Disclosure", "How Oh, Mother Mine DIY handles affiliate links, sponsored content and product mentions in our DIY tutorials and guides.", DISCLOSURE)); urls.append(("/disclosure/", TODAY, "0.2"))
    write("/sitemap/", build_sitemap_page()); urls.append(("/sitemap/", TODAY, "0.3"))
    write("/404.html", build_404())

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pr in urls:
        sm.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (SITE, u, lm, pr))
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", "User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /send.php\n\nSitemap: %s/sitemap.xml\n" % SITE)
    # slugs the front controller can redirect old flat/dated WordPress permalinks to
    write("/routes.json", json.dumps({"posts": [p["slug"] for p in POSTS], "categories": [c["slug"] for c in CATEGORIES]}))
    print("built %d pages into %s" % (len(urls) + 1, OUT))


if __name__ == "__main__":
    main()
