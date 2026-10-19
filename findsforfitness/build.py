#!/usr/bin/env python3
"""Static site generator for findsforfitness.com.

python3 build.py  -> writes the whole site into ./public (standard library only).
Articles live in content/posts/*.html (JSON front matter + body, see content/POST_SPEC.md);
tool pages in content/tools.py; site constants in siteconfig.py.
"""

import html
import json
import math
import re
import shutil
from datetime import date
from pathlib import Path

from siteconfig import CATEGORIES, NAV, SITE, TODAY
from content.tools import TOOLS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
POSTS_DIR = ROOT / "content" / "posts"
IMAGES = {k: v for k, v in json.loads((ROOT / "images.json").read_text()).items()}
ORIGIN = SITE["origin"]
GA_ID = "G-3VM6161ZL8"
GTAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>"""
VERSION = TODAY.replace("-", "")
REWRITE_DATE = "2026-10-17"  # when the archived posts were rewritten for the relaunch
esc = html.escape


# ---------------------------------------------------------------- icons
ICONS = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "gauge": '<path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l4-5"/><circle cx="12" cy="16" r="1.4"/>',
    "flame": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1-3.7 2.3-5 .2 1.6.9 2.6 2 3.2C11 8.6 11 5.8 12 3z"/>',
    "egg": '<path d="M12 3c3.6 0 6.5 5.2 6.5 10a6.5 6.5 0 0 1-13 0C5.5 8.2 8.4 3 12 3z"/>',
    "drop": '<path d="M12 3s6.5 7 6.5 11.3A6.5 6.5 0 0 1 5.5 14.3C5.5 10 12 3 12 3z"/>',
    "timer": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9.5 2.5h5M19 6l1.5-1.5"/>',
    "shoe": '<path d="M3 16.5V9.5c2 0 3.5-.5 4.5-2l1 .8c1 .8 2.3.7 3.2-.1l.3-.3 4.2 4.1c1.6.4 3.3 1.3 4.3 2.6.5.7.5 1.9.5 1.9H3z"/><path d="M3 19.5h18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


LOGO = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#c6f432"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient></defs>'
        '<rect width="40" height="40" rx="12" fill="url(#lg)"/>'
        '<path d="M11 28V12h12M11 20h9M24 28l5-8-3-.5 4-7.5" fill="none" stroke="#0b1015" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------------------------------------------------------- helpers
BG_SIZES = "(max-width: 900px) 720px, 100vw"


def img_src(name, small=False):
    return f"/assets/img/{name}{'-sm' if small else ''}.webp"


def img_tag(name, alt, cls="", small=False, eager=False, sizes=None):
    w, h = (720, 480) if small else (1600, 1067)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    # both variants are 3:2, so the browser can pick the 720px file on phones
    srcset = "" if small else f' srcset="{img_src(name, True)} 720w, {img_src(name)} 1600w" sizes="{sizes or "100vw"}"'
    return f'<img{c} src="{img_src(name, small)}"{srcset} width="{w}" height="{h}" alt="{esc(alt)}" {load} decoding="async">'


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"&[a-z#0-9]+;", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60]


def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


ORG = {
    "@type": "Organization",
    "@id": f"{ORIGIN}/#org",
    "name": SITE["name"],
    "url": ORIGIN + "/",
    "email": SITE["email"],
    "logo": {"@type": "ImageObject", "url": f"{ORIGIN}/icon-512.png", "width": 512, "height": 512},
}
WEBSITE = {"@type": "WebSite", "@id": f"{ORIGIN}/#website", "name": SITE["name"], "url": ORIGIN + "/",
           "publisher": {"@id": f"{ORIGIN}/#org"}, "inLanguage": "en-US"}


def breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


# ---------------------------------------------------------------- layout
def header(current):
    links = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if current == u else ""}>{n}</a></li>' for n, u in NAV)
    mlinks = "".join(
        f'<li style="--i:{i}"><a href="{u}">{n}{icon("arrow")}</a></li>' for i, (n, u) in enumerate(NAV + [("About", "/about/"), ("Contact", "/contact/")]))
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="logo" href="/" aria-label="{SITE['name']} home">{LOGO}<span>Finds<b>For</b>Fitness</span></a>
    <nav class="main-nav" aria-label="Main"><ul>{links}</ul></nav>
    <a class="btn btn-sm header-cta" href="/tools/">Free tools</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu" data-nav-toggle>
      <span class="bar"></span><span class="bar"></span><span class="bar"></span>
    </button>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav" data-mobile-nav hidden>
  <div class="mobile-nav-in">
    <ul>{mlinks}</ul>
    <div class="mobile-nav-foot">
      <a class="btn" href="/tools/">Try the free tools</a>
      <a class="mnav-mail" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
    </div>
  </div>
</div>"""


def footer():
    cats = "".join(f'<li><a href="/category/{k}/">{v["name"]}</a></li>' for k, v in CATEGORIES.items())
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{t["name"]}</a></li>' for t in TOOLS)
    return f"""<footer class="site-footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="logo" href="/">{LOGO}<span>Finds<b>For</b>Fitness</span></a>
      <p>{SITE['tagline']}. Practical guides written for real people, real feet and real schedules.</p>
      <a class="footer-mail" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
    </div>
    <div><p class="footer-h">Topics</p><ul>{cats}</ul></div>
    <div><p class="footer-h">Free tools</p><ul>{tools}</ul></div>
    <div><p class="footer-h">Site</p><ul>
      <li><a href="/blog/">All articles</a></li><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li>
      <li><a href="/disclaimers/">Disclaimer</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li>
      <li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms-of-service/">Terms of service</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; {date.today().year} {SITE['name']}. Content is for general information and is not medical advice.</p>
    <button class="to-top" type="button" data-to-top aria-label="Back to top">{icon('up')}</button>
  </div>
</footer>"""


def page(*, path, title, description, body, current="", schema=None, og_image="runners-at-sunrise",
         og_type="website", extra_head="", scripts=("site",), body_class="", robots="index,follow", published=None, modified=None, og_alt=""):
    canonical = ORIGIN + path
    if robots.startswith("index"):
        robots += ",max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    graph = [ORG, WEBSITE] + (schema or [])
    js = "".join(f'<script src="/assets/js/{s}.js?v={VERSION}" defer></script>' for s in scripts)
    art = ""
    if published:
        art = (f'<meta property="article:published_time" content="{published}T08:00:00+00:00">'
               f'<meta property="article:modified_time" content="{modified or published}T08:00:00+00:00">')
    return f"""<!doctype html>
<html lang="en">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:image" content="{ORIGIN}{img_src(og_image)}">
<meta property="og:image:width" content="1600"><meta property="og:image:height" content="1067">
<meta property="og:image:type" content="image/webp">
<meta property="og:image:alt" content="{esc(og_alt or title)}">
{art}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{ORIGIN}{img_src(og_image)}">
<meta name="theme-color" content="#0b1015">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96.png" sizes="96x96" type="image/png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{SITE['name']}" href="{ORIGIN}/feed.xml">
<link rel="preload" href="/assets/fonts/space-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
{extra_head}
{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body class="{body_class}">
{header(current)}
<main id="main">
{body}
</main>
{footer()}
{js}
</body>
</html>
"""


# ---------------------------------------------------------------- posts
def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(.*?)-->(.*)", raw, re.S)
        if not m:
            raise SystemExit(f"{f.name}: missing front matter")
        meta = json.loads(m.group(1))
        meta["slug"] = f.stem
        meta["body_raw"] = m.group(2).strip()
        meta.setdefault("updated", meta["published"] if meta["published"] >= "2026-01-01" else REWRITE_DATE)
        if meta["image"] not in IMAGES:
            raise SystemExit(f"{f.name}: unknown image {meta['image']}")
        meta["img"] = IMAGES[meta["image"]]
        words = len(re.sub(r"<[^>]+>", " ", meta["body_raw"]).split())
        meta["words"] = words
        meta["minutes"] = max(3, math.ceil(words / 230))
        posts.append(meta)
    posts.sort(key=lambda p: p["published"], reverse=True)
    return posts


TOOL_BY_SLUG = {t["slug"]: t for t in TOOLS}
TOOLS_UPDATED = "2026-10-19"
PAGES_UPDATED = "2026-10-17"


def tool_cta(slug):
    t = TOOL_BY_SLUG[slug]
    return (f'<a class="tool-cta" href="/tools/{slug}/"><span class="tool-cta-ico">{icon(t["icon"])}</span>'
            f'<span><small>Free interactive tool</small><b>{t["name"]}</b><em>{esc(t["short"])}</em></span>'
            f'<span class="tool-cta-go">Open {icon("arrow")}</span></a>')


def render_body(p):
    body = p["body_raw"]

    def fig(m):
        uid = m.group(1)
        if uid not in IMAGES:
            raise SystemExit(f"{p['slug']}: unknown figure image {uid}")
        n = IMAGES[uid]
        return (f'src="{img_src(n)}" srcset="{img_src(n, True)} 720w, {img_src(n)} 1600w" '
                f'sizes="(max-width: 800px) 100vw, 760px" width="1600" height="1067" loading="lazy" decoding="async"')
    body = re.sub(r'src="unsplash:([0-9a-f-]+)"', fig, body)
    body = re.sub(r'<div data-tool-cta="([a-z-]+)"></div>', lambda m: tool_cta(m.group(1)), body)
    toc = []
    seen = set()

    def h2(m):
        text = m.group(1)
        sid = slugify(text)
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        toc.append((sid, re.sub(r"<[^>]+>", "", text)))
        return f'<h2 id="{sid}">{text}</h2>'
    body = re.sub(r"<h2>(.*?)</h2>", h2, body)
    body = body.replace('<table>', '<table>')
    return body, toc


def card(p, cls="card", eager=False):
    cat = CATEGORIES[p["category"]]
    return f"""<article class="{cls} reveal" data-tilt>
  <a class="card-media" href="/{p['slug']}/" tabindex="-1" aria-hidden="true">{img_tag(p['img'], p['image_alt'], small=True, eager=eager)}</a>
  <div class="card-body">
    <a class="pill pill-{cat['color']}" href="/category/{p['category']}/">{cat['name']}</a>
    <h3><a href="/{p['slug']}/">{esc(p['title'])}</a></h3>
    <p>{esc(p['excerpt'])}</p>
    <span class="card-meta">{icon('clock')}{p['minutes']} min read</span>
  </div>
</article>"""


def post_page(p, posts):
    cat = CATEGORIES[p["category"]]
    body, toc = render_body(p)
    url = f"/{p['slug']}/"
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    faq = p.get("faq") or []
    faq_html = ""
    if faq:
        items = "".join(
            f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{esc(f["q"])}<span class="faq-x" aria-hidden="true"></span></summary><div><p>{esc(f["a"])}</p></div></details>'
            for i, f in enumerate(faq))
        faq_html = f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{items}</section>'
        toc_html += '<li><a href="#faq-h">FAQ</a></li>'
    related = [q for q in posts if q["category"] == p["category"] and q["slug"] != p["slug"]][:3]
    if len(related) < 3:
        related += [q for q in posts if q["slug"] != p["slug"] and q not in related][: 3 - len(related)]
    rel_html = "".join(card(q) for q in related)
    tool_html = tool_cta(p["related_tool"]) if p.get("related_tool") else ""
    crumbs = [("Home", "/"), (cat["name"], f"/category/{p['category']}/"), (p["title"], url)]
    article_ld = {
        "@type": "BlogPosting", "@id": ORIGIN + url + "#article", "headline": p["title"][:110],
        "description": p["description"], "image": ORIGIN + img_src(p["img"]),
        "datePublished": p["published"], "dateModified": p["updated"],
        "author": {"@type": "Organization", "name": f"{SITE['name']} Editorial Team", "url": ORIGIN + "/about/"},
        "publisher": {"@id": f"{ORIGIN}/#org"}, "mainEntityOfPage": ORIGIN + url,
        "articleSection": cat["name"], "keywords": p["keyword"], "wordCount": p["words"], "inLanguage": "en-US",
    }
    schema = [article_ld, breadcrumbs(crumbs)]
    if faq:
        schema.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]})
    updated_note = ""
    if p["updated"] != p["published"]:
        updated_note = f'<span>{icon("calendar")}Updated <time datetime="{p["updated"]}">{fmt_date(p["updated"])}</time></span>'
    else:
        updated_note = f'<span>{icon("calendar")}<time datetime="{p["published"]}">{fmt_date(p["published"])}</time></span>'
    disclaimer = ("This article is for general information only and isn't a substitute for advice from your doctor, "
                  "dermatologist, podiatrist or a registered dietitian. Check with a professional before starting a new "
                  "diet, supplement, skin treatment or exercise program, especially if you have a health condition.")
    out = f"""
<article class="post">
  <header class="post-hero">
    <div class="post-hero-bg" aria-hidden="true">{img_tag(p['img'], '', eager=True, sizes=BG_SIZES)}</div>
    <div class="blobs" aria-hidden="true"><span></span><span></span></div>
    <div class="wrap post-hero-in">
      {crumbs_html(crumbs)}
      <a class="pill pill-{cat['color']}" href="/category/{p['category']}/">{cat['name']}</a>
      <h1>{esc(p['title'])}</h1>
      <p class="post-lede">{esc(p['excerpt'])}</p>
      <div class="post-meta">
        <span class="by"><span class="avatar">{LOGO}</span>{SITE['name']} Editorial Team</span>
        {updated_note}
        <span>{icon('clock')}{p['minutes']} min read</span>
      </div>
    </div>
  </header>
  <div class="wrap post-layout">
    <aside class="toc" aria-label="On this page">
      <details class="toc-box" open data-toc>
        <summary>{icon('list')}On this page</summary>
        <ol>{toc_html}</ol>
      </details>
      <div class="toc-tool">{tool_html}</div>
    </aside>
    <div class="post-main">
      <figure class="post-cover">{img_tag(p['img'], p['image_alt'], sizes='(max-width: 1080px) 100vw, 860px')}</figure>
      <div class="prose">
{body}
      </div>
      {faq_html}
      <div class="post-foot">
        <div class="author-box"><span class="avatar avatar-lg">{LOGO}</span><div><b>{SITE['name']} Editorial Team</b>
        <p>We research fitness gear, training and nutrition guidance from trusted health organizations and rewrite it into plain, practical advice. Spotted an error? <a href="/contact/">Tell us</a>.</p></div></div>
        <p class="disclaimer"><strong>Disclaimer:</strong> {disclaimer}</p>
      </div>
    </div>
  </div>
  <section class="related wrap" aria-labelledby="rel-h">
    <div class="section-head"><h2 id="rel-h">Keep reading</h2><a class="link-arrow" href="/category/{p['category']}/">More {cat['name']}{icon('arrow')}</a></div>
    <div class="grid-3">{rel_html}</div>
  </section>
</article>
{newsletter()}"""
    return page(path=url, title=p["seo_title"], description=p["description"], body=out,
                current=f"/category/{p['category']}/", schema=schema, og_image=p["img"], og_type="article",
                published=p["published"], modified=p["updated"], body_class="is-post", og_alt=p["image_alt"])


# ---------------------------------------------------------------- sections
def newsletter():
    return f"""<section class="newsletter" aria-labelledby="nl-h">
  <div class="newsletter-bg" aria-hidden="true">{img_tag('group-outdoor-workout', '', small=True)}</div>
  <div class="wrap newsletter-in reveal">
    <div>
      <span class="eyebrow">{icon('spark')}The Weekly Find</span>
      <h2 id="nl-h">One useful fitness find, every week.</h2>
      <p>A workout, a recipe or a gear tip worth your time. No spam, unsubscribe anytime.</p>
    </div>
    <form class="nl-form" action="/contact.php" method="post">
      <input type="hidden" name="type" value="newsletter">
      <label class="sr-only" for="nl-email">Email address</label>
      <input id="nl-email" type="email" name="email" placeholder="you@example.com" required autocomplete="email">
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn" type="submit">Subscribe{icon('arrow')}</button>
    </form>
  </div>
</section>"""


def tool_card(t, i=0):
    return f"""<a class="tool-card reveal" href="/tools/{t['slug']}/" style="--d:{i * 60}ms">
  <span class="tool-ico">{icon(t['icon'])}</span>
  <b>{t['name']}</b><span>{esc(t['short'])}</span><em>Open tool{icon('arrow')}</em></a>"""


def home(posts):
    by = {p["slug"]: p for p in posts}
    feat = by.get("best-tennis-shoes-for-flat-feet")
    side = [by[s] for s in ("healthy-breakfast-foods-for-weight-loss", "the-beginners-guide-to-starting-a-running-routine",
                            "daily-skincare-routine-for-glowing-skin") if s in by]
    latest = [p for p in posts if p not in side and p is not feat][:6]
    cats = "".join(f"""<a class="cat-tile cat-{v['color']} reveal" href="/category/{k}/" style="--d:{i * 70}ms">
  {img_tag(v['image'], '', small=True)}
  <span class="cat-tile-in"><b>{v['name']}</b><small>{sum(1 for p in posts if p['category'] == k)} guides</small><em>{esc(v['blurb'])}</em></span>
  <span class="cat-go">{icon('arrow')}</span></a>""" for i, (k, v) in enumerate(CATEGORIES.items()))
    ticker_words = ["Flat-feet friendly shoes", "Beginner running plans", "High-protein breakfasts", "Calisthenics",
                    "Glow-up routines", "HIIT timer", "Calorie math made simple", "Plantar fasciitis relief",
                    "Strength training 101", "Hydration"]
    ticker = "".join(f"<span>{w}</span>" for w in ticker_words) * 2
    feat_html = ""
    if feat:
        feat_html = f"""<article class="feature reveal">
  <a class="feature-media" href="/{feat['slug']}/" tabindex="-1" aria-hidden="true">{img_tag(feat['img'], feat['image_alt'])}</a>
  <div class="feature-body">
    <span class="pill pill-sky">Most-read gear guide</span>
    <h3><a href="/{feat['slug']}/">{esc(feat['title'])}</a></h3>
    <p>{esc(feat['excerpt'])}</p>
    <div class="feature-actions"><a class="btn" href="/{feat['slug']}/">See the picks{icon('arrow')}</a>
    <a class="btn btn-ghost" href="/tools/shoe-finder-quiz/">Take the shoe quiz</a></div>
  </div>
</article>"""
    side_html = "".join(f"""<a class="mini reveal" href="/{p['slug']}/" style="--d:{i * 80}ms">{img_tag(p['img'], p['image_alt'], small=True)}
<span><small>{CATEGORIES[p['category']]['name']}</small><b>{esc(p['title'])}</b></span></a>""" for i, p in enumerate(side))
    tools_html = "".join(tool_card(t, i) for i, t in enumerate(TOOLS))
    latest_html = "".join(card(p) for p in latest)
    body = f"""
<section class="hero">
  <div class="hero-bg" aria-hidden="true">{img_tag('runners-at-sunrise', '', eager=True, sizes=BG_SIZES)}</div>
  <div class="blobs" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="grain" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <span class="eyebrow hero-eyebrow">{icon('spark')}Fitness, food &amp; skin care, minus the hype</span>
    <h1 class="hero-title"><span class="line">Find what</span> <span class="line">actually <em class="grad">works</em></span> <span class="line">for your body.</span></h1>
    <p class="hero-sub">Finds For Fitness is your shortcut to better workouts, smarter weight loss and healthier skin: honest gear guides for flat feet, beginner plans, and free calculators that do the math for you.</p>
    <div class="hero-actions">
      <a class="btn btn-lg" href="/blog/">Explore the guides{icon('arrow')}</a>
      <a class="btn btn-lg btn-glass" href="/tools/">Try the free tools</a>
    </div>
    <ul class="hero-stats">
      <li><b data-count="{len(posts)}">{len(posts)}</b><span>in-depth guides</span></li>
      <li><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free fitness tools</span></li>
      <li><b data-count="5">5</b><span>topics covered</span></li>
    </ul>
  </div>
  <div class="hero-float hero-float-a" aria-hidden="true">{icon('flame')}<span><b>TDEE</b> calculated</span></div>
  <div class="hero-float hero-float-b" aria-hidden="true">{icon('shoe')}<span><b>Flat feet?</b> We've got picks</span></div>
  <a class="scroll-cue" href="#topics" aria-label="Scroll to topics"><span></span></a>
</section>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="section" id="topics" aria-labelledby="topics-h">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Browse by goal</span><h2 id="topics-h">Pick your path</h2></div>
    <p>Five focused topics, each written for beginners and busy people.</p></div>
    <div class="cat-grid">{cats}</div>
  </div>
</section>

<section class="section section-tint" aria-labelledby="feat-h">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Reader favorites</span><h2 id="feat-h">The guides people come back to</h2></div>
    <a class="link-arrow" href="/blog/">All articles{icon('arrow')}</a></div>
    <div class="feature-grid">{feat_html}<div class="mini-list">{side_html}</div></div>
  </div>
</section>

<section class="section section-dark" aria-labelledby="tools-h">
  <div class="blobs blobs-dim" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Interactive</span><h2 id="tools-h">Free tools that do the math</h2></div>
    <p>Calculators, a shoe quiz and a workout timer. Nothing to install, works great on your phone.</p></div>
    <div class="tool-grid">{tools_html}</div>
  </div>
</section>

<section class="section" aria-labelledby="latest-h">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Fresh</span><h2 id="latest-h">Latest articles</h2></div>
    <a class="link-arrow" href="/blog/">See everything{icon('arrow')}</a></div>
    <div class="grid-3">{latest_html}</div>
  </div>
</section>

<section class="section section-tint" aria-labelledby="how-h">
  <div class="wrap split">
    <div class="split-media reveal">{img_tag('push-up-coaching', 'Coach helping a man with push-up form in a gym', small=True)}
      <div class="float-card">{icon('check')}<span><b>Plain-language advice</b>No fads, no miracle claims.</span></div></div>
    <div class="split-copy reveal">
      <span class="eyebrow">How we work</span>
      <h2 id="how-h">Small, sustainable wins beat extreme plans</h2>
      <p>Finds For Fitness started as a place to share gear finds, like the tennis shoes that finally worked for flat feet. Today we cover the whole routine: how you move, what you eat and how you look after your skin.</p>
      <ul class="checklist">
        <li>Guidance grounded in recommendations from the CDC, NIH and professional associations.</li>
        <li>Beginner-first workouts with clear progressions.</li>
        <li>Gear guides that explain <em>why</em> a shoe suits your feet, not just what to buy.</li>
      </ul>
      <a class="btn" href="/about/">About Finds For Fitness{icon('arrow')}</a>
    </div>
  </div>
</section>
{newsletter()}"""
    schema = [{"@type": "CollectionPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": SITE["name"],
               "isPartOf": {"@id": f"{ORIGIN}/#website"}, "about": "Fitness, workouts, weight loss and skin care"}]
    return page(path="/", title="Finds For Fitness: Workouts, Weight Loss, Skin Care & Gear",
                description="Honest fitness gear guides, beginner workouts, weight loss nutrition and skin care tips, plus free BMI, calorie and pace calculators. Find what works for you.",
                body=body, current="/", schema=schema, body_class="is-home")


def listing(path, title, h1, lede, items, crumbs, description, image="runners-at-sunrise", current="", filters=False):
    chips = ""
    if filters:
        chips = '<div class="filter-chips" role="toolbar" aria-label="Filter articles"><button type="button" class="is-on" data-filter="all">All</button>' + "".join(
            f'<button type="button" data-filter="{k}">{v["name"]}</button>' for k, v in CATEGORIES.items()) + "</div>"
    grid = "".join(card(p).replace('<article class="card', f'<article data-cat="{p["category"]}" class="card', 1) for p in items)
    body = f"""
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true">{img_tag(image, '', eager=True, sizes=BG_SIZES)}</div>
  <div class="blobs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap page-hero-in">{crumbs_html(crumbs)}<h1>{h1}</h1><p>{lede}</p></div>
</section>
<section class="section"><div class="wrap">{chips}<div class="grid-3" data-filter-grid>{grid}</div></div></section>
{newsletter()}"""
    schema = [{"@type": "CollectionPage", "url": ORIGIN + path, "name": h1, "description": description,
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}/{p['slug']}/"} for i, p in enumerate(items)]}},
              breadcrumbs(crumbs)]
    return page(path=path, title=title, description=description, body=body, schema=schema, og_image=image, current=current)


def tools_hub():
    cards = "".join(tool_card(t, i) for i, t in enumerate(TOOLS))
    crumbs = [("Home", "/"), ("Free Tools", "/tools/")]
    body = f"""
<section class="page-hero">
  <div class="page-hero-bg" aria-hidden="true">{img_tag('battle-ropes-hiit', '', eager=True, sizes=BG_SIZES)}</div>
  <div class="blobs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap page-hero-in">{crumbs_html(crumbs)}<h1>Free fitness calculators &amp; tools</h1>
  <p>Work out your BMI, calories, protein and water needs, plan race paces, find the right shoe type for flat feet, and time your intervals.</p></div>
</section>
<section class="section section-dark"><div class="wrap"><div class="tool-grid">{cards}</div></div></section>
{newsletter()}"""
    schema = [{"@type": "CollectionPage", "url": ORIGIN + "/tools/", "name": "Free fitness tools",
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}/tools/{t['slug']}/", "name": t["name"]} for i, t in enumerate(TOOLS)]}},
              breadcrumbs(crumbs)]
    return page(path="/tools/", title="Free Fitness Calculators & Tools | Finds For Fitness",
                description="Free BMI, calorie, protein, water intake and running pace calculators, a shoe finder quiz for flat feet and a HIIT interval timer. No sign-up needed.",
                body=body, schema=schema, current="/tools/", og_image="battle-ropes-hiit")


def tool_page(t, posts):
    url = f"/tools/{t['slug']}/"
    crumbs = [("Home", "/"), ("Free Tools", "/tools/"), (t["name"], url)]
    faq = "".join(
        f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{esc(f["q"])}<span class="faq-x" aria-hidden="true"></span></summary><div><p>{esc(f["a"])}</p></div></details>'
        for i, f in enumerate(t["faq"]))
    others = "".join(tool_card(o, i) for i, o in enumerate([o for o in TOOLS if o is not t][:3]))
    body = f"""
<section class="page-hero page-hero-tool">
  <div class="page-hero-bg" aria-hidden="true">{img_tag(t['image'], '', eager=True, sizes=BG_SIZES)}</div>
  <div class="blobs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap page-hero-in">{crumbs_html(crumbs)}<span class="tool-ico tool-ico-lg">{icon(t['icon'])}</span><h1>{t['name']}</h1><p>{esc(t['description'])}</p></div>
</section>
<section class="section tool-section"><div class="wrap">
  <div class="tool-panel">{t['widget']}</div>
  <div class="tool-copy">
    <div class="prose">{t['body']}</div>
    <section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{faq}</section>
    <p class="disclaimer"><strong>Disclaimer:</strong> Results are estimates for healthy adults and are not medical advice.</p>
  </div>
</div></section>
<section class="section section-dark"><div class="wrap"><div class="section-head"><h2>More free tools</h2><a class="link-arrow" href="/tools/">All tools{icon('arrow')}</a></div>
<div class="tool-grid tool-grid-3">{others}</div></div></section>"""
    schema = [{"@type": "WebApplication", "name": t["name"], "url": ORIGIN + url, "applicationCategory": "HealthApplication",
               "operatingSystem": "Any", "description": t["description"], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
              breadcrumbs(crumbs),
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in t["faq"]]}]
    return page(path=url, title=t["seo_title"], description=t["description"], body=body, schema=schema,
                current="/tools/", scripts=("site", "tools"), og_image=t["image"], body_class="is-tool")


def simple_page(path, title, h1, lede, content, description, image="runners-at-sunrise", robots="index,follow"):
    crumbs = [("Home", "/"), (h1, path)]
    body = f"""
<section class="page-hero page-hero-sm">
  <div class="page-hero-bg" aria-hidden="true">{img_tag(image, '', eager=True, sizes=BG_SIZES)}</div>
  <div class="blobs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap page-hero-in">{crumbs_html(crumbs)}<h1>{h1}</h1><p>{lede}</p></div>
</section>
<section class="section"><div class="wrap narrow"><div class="prose">{content}</div></div></section>"""
    return page(path=path, title=title, description=description, body=body, schema=[breadcrumbs(crumbs)], og_image=image, robots=robots)


# ---------------------------------------------------------------- static pages
def legal_pages():
    e = SITE["email"]
    mail = f'<a href="mailto:{e}">{e}</a>'
    yield ("/about/", "About Finds For Fitness", "About Finds For Fitness",
           "Practical fitness, nutrition and skin care guidance for real people.",
           f"""<p>Finds For Fitness began in 2021 as a small gear blog. Our first big guide, on the <a href="/best-tennis-shoes-for-flat-feet/">best tennis shoes for flat feet</a>, came from a simple frustration: most &ldquo;best of&rdquo; lists never explained <em>why</em> a shoe would help a flat-footed player. Since then the site has grown to cover workouts, weight loss and skin care, always with the same goal: clear, practical advice you can use today.</p>
<h2>What we cover</h2>
<ul class="checklist"><li><a href="/category/workout/">Workouts</a>: running plans, calisthenics, strength training and HIIT for beginners.</li>
<li><a href="/category/weight_loss/">Weight loss</a>: calorie basics, breakfasts and habits that last.</li>
<li><a href="/category/skin_care/">Skin care</a>: simple routines and honest ingredient guides.</li>
<li><a href="/category/product-reviews/">Gear guides</a>: shoes and equipment, especially for flat feet.</li>
<li><a href="/tools/">Free tools</a>: calculators, a shoe quiz and an interval timer.</li></ul>
<h2>How we write</h2>
<p>Our editorial team researches each topic using guidance from public health bodies and professional associations such as the CDC, the National Institutes of Health, the American Academy of Dermatology and the American Heart Association, then turns it into plain-language steps. We don't sell supplements or programs, and we update articles when guidance changes.</p>
<div class="callout callout-note"><strong>Good to know:</strong> Our content is educational and not a substitute for personal medical advice. See our <a href="/disclaimers/">disclaimer</a>.</div>
<h2>Get in touch</h2><p>Questions, corrections or ideas for a guide? Email {mail} or use our <a href="/contact/">contact form</a>.</p>""",
           "Learn about Finds For Fitness: who we are, what we cover and how we research our workout, weight loss, skin care and fitness gear guides.")
    yield ("/disclaimers/", "Disclaimer | Finds For Fitness", "Disclaimer", "Please read this before acting on anything you find here.",
           f"""<p>The information on findsforfitness.com is provided for general educational purposes only. It is not medical, nutritional, dermatological or podiatric advice, and it is not a substitute for diagnosis or treatment by a qualified professional.</p>
<h2>Health and fitness</h2><p>Always consult your doctor before starting a new exercise program, changing your diet, taking a supplement or trying a skin treatment, especially if you are pregnant, nursing, have a medical condition or take medication. Stop exercising and seek medical help if you feel pain, dizziness or shortness of breath.</p>
<h2>Calculators and tools</h2><p>Our calculators use published formulas to produce estimates for healthy adults. Individual needs vary, and results should be treated as a starting point only.</p>
<h2>Product information</h2><p>Product features and availability change. Check the manufacturer's information and try products on where possible before buying.</p>
<h2>Contact</h2><p>Questions about this disclaimer: {mail}.</p>""",
           "Read the Finds For Fitness disclaimer: our fitness, nutrition, skin care and calculator content is educational and not a substitute for professional advice.")
    yield ("/affiliate-disclosure/", "Affiliate Disclosure | Finds For Fitness", "Affiliate Disclosure", "How Finds For Fitness is funded.",
           f"""<p>Finds For Fitness currently does not use affiliate links. Products are mentioned only because we think they're relevant to the reader, and no brand pays to be included in our guides.</p>
<p>If we add affiliate links in the future, for example to retailers such as Amazon, we may earn a small commission when you buy through them at no extra cost to you. Any such links will be clearly disclosed on the page, and they will never change which products we recommend.</p>
<p>Questions? Email {mail}.</p>""",
           "Finds For Fitness affiliate disclosure: how we choose the products we mention and how any future affiliate links would be disclosed.")
    yield ("/privacy-policy/", "Privacy Policy | Finds For Fitness", "Privacy Policy", f"Last updated {fmt_date(PAGES_UPDATED)}.",
           f"""<p>This policy explains what information findsforfitness.com (&ldquo;we&rdquo;) collects and how we use it.</p>
<h2>Information you give us</h2><p>If you use our contact form or newsletter sign-up, we receive your name (if given), email address and message. We use it only to reply to you or send the newsletter you asked for, and you can unsubscribe at any time.</p>
<h2>Calculators and tools</h2><p>Our tools run in your browser. The numbers you enter are not sent to us. The water tracker saves your glasses count in your browser's local storage on your device only.</p>
<h2>Cookies and analytics</h2><p>We do not use advertising cookies. Our hosting provider may keep standard server logs (IP address, browser, pages requested) for security and performance. We use Google Analytics to understand how visitors use the site; it sets cookies and collects usage data such as pages viewed, device type and approximate location. You can opt out with Google's browser add-on or by blocking cookies.</p>
<h2>Sharing</h2><p>We don't sell or rent personal information. We share it only when required by law.</p>
<h2>Your rights</h2><p>You can ask us to access, correct or delete the information we hold about you by emailing {mail}.</p>
<h2>Children</h2><p>This site is not directed to children under 13 and we don't knowingly collect their information.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p>""",
           "Read the Finds For Fitness privacy policy: what we collect through our contact form and newsletter, how our in-browser tools work, and your rights.")
    yield ("/terms-of-service/", "Terms of Service | Finds For Fitness", "Terms of Service", f"Last updated {fmt_date(PAGES_UPDATED)}.",
           f"""<p>By using findsforfitness.com you agree to these terms.</p>
<h2>Use of content</h2><p>Articles, images and tools on this site are for personal, non-commercial use. You may link to and quote short excerpts with attribution, but you may not republish whole articles without permission.</p>
<h2>No professional advice</h2><p>Content is educational and is not medical advice. See our <a href="/disclaimers/">disclaimer</a>. You use the information at your own risk.</p>
<h2>Accuracy</h2><p>We work to keep content accurate and current but make no warranties about completeness or suitability for any purpose.</p>
<h2>External links</h2><p>We link to other websites for reference. We aren't responsible for their content or practices.</p>
<h2>Limitation of liability</h2><p>To the extent permitted by law, Finds For Fitness is not liable for any loss or injury arising from use of this site.</p>
<h2>Contact</h2><p>{mail}</p>""",
           "Terms of service for findsforfitness.com covering use of our fitness articles, images and free calculators.")


def contact_page():
    e = SITE["email"]
    content = f"""
<div class="contact-grid">
  <div>
    <h2>Say hello</h2>
    <p>Have a question about a guide, a correction, or a topic you'd like us to cover? Send us a note and we'll get back to you, usually within two business days.</p>
    <a class="contact-mail" href="mailto:{e}">{icon('mail')}<span><small>Email us directly</small><b>{e}</b></span></a>
    <p class="muted">We can't give personal medical advice. For health concerns, please speak with your doctor.</p>
  </div>
  <form class="contact-form" action="/contact.php" method="post" data-contact>
    <div class="form-ok" data-form-ok hidden>{icon('check')}<span>Thanks! Your message is on its way. We'll reply to the email you gave us.</span></div>
    <input type="hidden" name="type" value="contact">
    <label class="field"><span>Your name</span><input type="text" name="name" required autocomplete="name"></label>
    <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email"></label>
    <label class="field"><span>Topic</span><select name="topic"><option>General question</option><option>Article correction</option><option>Topic suggestion</option><option>Partnership</option></select></label>
    <label class="field"><span>Message</span><textarea name="message" rows="5" required></textarea></label>
    <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    <button class="btn" type="submit">Send message{icon('arrow')}</button>
  </form>
</div>"""
    return simple_page("/contact/", "Contact Finds For Fitness", "Contact us",
                       "Questions, corrections and ideas are always welcome.", content,
                       f"Contact Finds For Fitness with questions, corrections or topic ideas. Email {e} or use our contact form.",
                       image="group-outdoor-workout")


def html_sitemap(posts):
    secs = []
    for k, v in CATEGORIES.items():
        items = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["title"])}</a></li>' for p in posts if p["category"] == k)
        secs.append(f'<h2><a href="/category/{k}/">{v["name"]}</a></h2><ul>{items}</ul>')
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{t["name"]}</a></li>' for t in TOOLS)
    content = "".join(secs) + f'<h2><a href="/tools/">Free tools</a></h2><ul>{tools}</ul>' + \
        '<h2>Site</h2><ul><li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/disclaimers/">Disclaimer</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms-of-service/">Terms of service</a></li></ul>'
    return simple_page("/sitemap/", "Sitemap | Finds For Fitness", "Sitemap", "Every page on Finds For Fitness.", content,
                       "Browse every article, category and free tool on Finds For Fitness: workouts, weight loss, skin care, gear guides and calculators.")


def not_found():
    body = f"""
<section class="page-hero nf">
  <div class="blobs" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap page-hero-in"><span class="nf-code">404</span><h1>This page skipped leg day.</h1>
  <p>We couldn't find that page. It may have moved when we rebuilt the site.</p>
  <div class="hero-actions"><a class="btn" href="/">Back home{icon('arrow')}</a><a class="btn btn-glass" href="/blog/">Browse articles</a></div></div>
</section>"""
    return page(path="/404.html", title="Page not found | Finds For Fitness", description="Page not found.", body=body, robots="noindex,follow")


# ---------------------------------------------------------------- server files
INDEX_PHP = r"""<?php
// findsforfitness.com front controller. The host routes "/" and unknown paths here
// (and ignores .htaccess), so this file serves the homepage, legacy redirects and real 404s.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://findsforfitness.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.findsforfitness.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
$redirects = [
    '#^/contact-us(-2)?/?$#'            => '/contact/',
    '#^/privacy-policy-\d+/?$#'          => '/privacy-policy/',
    '#^/disclaimer/?$#'                  => '/disclaimers/',
    '#^/terms(-of-use|-and-conditions)?/?$#' => '/terms-of-service/',
    '#^/category/health_news/?$#'        => '/blog/',
    '#^/category/uncategorized/?$#'      => '/blog/',
    '#^/(feed|comments/feed)/?$#'       => '/feed.xml',
    '#^/(page/\d+|author/[^/]+)/?$#'    => '/blog/',
    '#^/category/([a-z_-]+)/page/\d+/?$#' => '/category/$1/',
    '#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
];
foreach ($redirects as $re => $to) {
    if (preg_match($re, $path, $m)) {
        header('Location: ' . $home . preg_replace($re, $to, $path), true, 301);
        exit;
    }
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""

CONTACT_PHP = r"""<?php
// Contact + newsletter handler. Sends to the site inbox and keeps a CSV copy outside public_html.
$to = 'info@findsforfitness.com';
$back = $_SERVER['HTTP_REFERER'] ?? '/contact/';
if (parse_url($back, PHP_URL_HOST) && parse_url($back, PHP_URL_HOST) !== ($_SERVER['HTTP_HOST'] ?? '')) { $back = '/contact/'; }
$back = strtok($back, '?#');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
if (!empty($_POST['website'])) { header('Location: ' . $back . '?sent=1', true, 303); exit; }   // honeypot

$clean = fn($v, $n) => trim(substr(str_replace(["\r", "\n"], ' ', (string)($v ?? '')), 0, $n));
$type = $_POST['type'] === 'newsletter' ? 'newsletter' : 'contact';
$email = filter_var($clean($_POST['email'] ?? '', 200), FILTER_VALIDATE_EMAIL);
if (!$email) { header('Location: ' . $back . '?error=email', true, 303); exit; }
$name = $clean($_POST['name'] ?? '', 120);
$topic = $clean($_POST['topic'] ?? '', 80);
$message = trim(substr((string)($_POST['message'] ?? ''), 0, 5000));

$subject = $type === 'newsletter' ? 'New newsletter subscriber' : 'Contact form: ' . ($topic ?: 'Message') . ' from ' . ($name ?: $email);
$body = "Type: $type\nName: $name\nEmail: $email\nTopic: $topic\n\n$message\n\n--\nSent from findsforfitness.com";
$headers = "From: Finds For Fitness <$to>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8";
@mail($to, $subject, $body, $headers);

$log = dirname(__DIR__) . '/form-submissions.csv';
if ($fh = @fopen($log, 'a')) { fputcsv($fh, [date('c'), $type, $name, $email, $topic, $message]); fclose($fh); }

header('Location: ' . $back . '?sent=1' . ($type === 'newsletter' ? '#nl-h' : ''), true, 303);
"""


def rss(posts):
    items = "".join(f"""<item><title>{esc(p['title'])}</title><link>{ORIGIN}/{p['slug']}/</link><guid>{ORIGIN}/{p['slug']}/</guid>
<pubDate>{date.fromisoformat(p['published']).strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate><category>{esc(CATEGORIES[p['category']]['name'])}</category>
<description>{esc(p['excerpt'])}</description></item>
""" for p in posts[:20])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>{SITE['name']}</title><link>{ORIGIN}/</link><description>{esc(SITE['description'])}</description><language>en-us</language>
<atom:link href="{ORIGIN}/feed.xml" rel="self" type="application/rss+xml"/>
{items}</channel></rss>
"""


def favicon_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#c6f432"/><stop offset="1" stop-color="#2dd4bf"/></linearGradient></defs>'
            '<rect width="40" height="40" rx="12" fill="url(#g)"/><path d="M11 28V12h12M11 20h9M24 28l5-8-3-.5 4-7.5" fill="none" '
            'stroke="#0b1015" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


# ---------------------------------------------------------------- main
def main():
    for child in OUT.iterdir() if OUT.exists() else []:
        if child.name == "assets":
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    posts = load_posts()
    newest = max(p["updated"] for p in posts)
    urls = [("/", newest, "1.0", "runners-at-sunrise")]

    write("home.html", home(posts))
    for p in posts:
        write(f"{p['slug']}/index.html", post_page(p, posts))
        urls.append((f"/{p['slug']}/", p["updated"], "0.8", p["img"]))
    write("blog/index.html", listing("/blog/", "Fitness, Weight Loss & Skin Care Blog | Finds For Fitness",
                                     "All articles", "Workouts, weight loss, skin care, gear guides and everyday health tips.",
                                     posts, [("Home", "/"), ("Blog", "/blog/")],
                                     "Browse every Finds For Fitness article: beginner workouts, weight loss nutrition, skin care routines, flat-feet gear guides and health tips.",
                                     filters=True, current="/blog/"))
    urls.append(("/blog/", newest, "0.7", None))
    for k, v in CATEGORIES.items():
        items = [p for p in posts if p["category"] == k]
        write(f"category/{k}/index.html", listing(f"/category/{k}/", f"{v['title']} | Finds For Fitness", v["title"], v["blurb"],
                                                  items, [("Home", "/"), (v["name"], f"/category/{k}/")],
                                                  f"{v['blurb']} Browse {len(items)} {v['name'].lower()} guides from Finds For Fitness.",
                                                  image=v["image"], current=f"/category/{k}/"))
        urls.append((f"/category/{k}/", max(p["updated"] for p in items), "0.6", v["image"]))
    write("tools/index.html", tools_hub())
    urls.append(("/tools/", TOOLS_UPDATED, "0.8", "battle-ropes-hiit"))
    for t in TOOLS:
        write(f"tools/{t['slug']}/index.html", tool_page(t, posts))
        urls.append((f"/tools/{t['slug']}/", TOOLS_UPDATED, "0.8", t["image"]))
    for path, title, h1, lede, content, desc in legal_pages():
        write(f"{path.strip('/')}/index.html", simple_page(path, title, h1, lede, content, desc))
        urls.append((path, PAGES_UPDATED, "0.3", None))
    write("contact/index.html", contact_page())
    urls.append(("/contact/", PAGES_UPDATED, "0.4", None))
    write("sitemap/index.html", html_sitemap(posts))
    urls.append(("/sitemap/", newest, "0.2", None))
    write("404.html", not_found())

    sm = ""
    for u, d, pr, im in urls:
        img = f"<image:image><image:loc>{ORIGIN}{img_src(im)}</image:loc></image:image>" if im else ""
        sm += f"<url><loc>{ORIGIN}{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority>{img}</url>\n"
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          f'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{sm}</urlset>\n')
    write("feed.xml", rss(posts))
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /contact.php\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    write("index.php", INDEX_PHP)
    write("contact.php", CONTACT_PHP)
    write("favicon.svg", favicon_svg())
    write("site.webmanifest", json.dumps({
        "name": SITE["name"], "short_name": "FindsFitness", "start_url": "/", "display": "standalone",
        "background_color": "#0b1015", "theme_color": "#0b1015",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    for f in ("favicon.ico", "favicon-32.png", "favicon-48.png", "favicon-96.png", "apple-touch-icon.png",
              "icon-192.png", "icon-512.png", "googlecccfbf2f7e9e5ae4.html"):
        src = ROOT / "static" / f
        if src.exists():
            shutil.copy(src, OUT / f)
    print(f"built {len(posts)} posts, {len(TOOLS)} tools, {len(urls)} sitemap urls")


if __name__ == "__main__":
    main()
