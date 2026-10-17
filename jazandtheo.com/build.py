#!/usr/bin/env python3
"""Static site generator for jazandtheo.com.

Reads post fragments from content/posts/, page copy from content/pages.py and
tool copy from content/tools.py, and writes every HTML page, sitemap.xml and
robots.txt into this directory. Python 3 standard library only.
"""

import html
import json
import os
import re
import shutil
from datetime import date, datetime

from content.pages import ABOUT, PRIVACY, HUB_COPY
from content.tools import TOOLS

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN = "https://jazandtheo.com"
SITE = "Jaz & Theo"
EMAIL = "info@jazandtheo.com"
TODAY = date.today().isoformat()
MODIFIED = "2026-10-17"
PER_PAGE = 12

CATS = {
    "wedding": ("Weddings", "Venue guides, planning help and photography advice for weddings across Texas and Arizona."),
    "portraits": ("Portraits", "Engagement, senior and anniversary sessions — locations, outfits and how to feel at ease on camera."),
    "home": ("Home", "Small, thoughtful home projects: peg rails, shiplap, lighting, windows and a calmer kitchen."),
    "travel": ("Travel", "Road trips and destination ideas from the desert Southwest to the Badlands and Yellowstone."),
    "photography": ("Photography", "For photographers and the curious: learning the craft, gear, light and the business side."),
}
TAG_NAMES = {
    "jaz-and-theo-weekly-adventures": "Jaz & Theo Weekly Adventures",
    "amy-and-jordan-business-course": "Amy and Jordan Business Course",
}

NAV = [
    ("Weddings", "/weddings/"),
    ("Portraits", "/portraits/"),
    ("Lifestyle", "/lifestyle/"),
    ("Journal", "/blog/"),
    ("Tools", "/tools/"),
    ("Shop", "/shop/"),
    ("About", "/about/"),
]

e = lambda s: html.escape(str(s), quote=True)

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "coins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.7-2.7-3-6-3"/></svg>',
    "lamp": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 2v5M5 15a7 7 0 0 1 14 0z"/><path d="M10 18a2 2 0 0 0 4 0"/></svg>',
    "ruler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2" y="8" width="20" height="8" rx="1.5"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l8-8"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/></svg>',
    "palette": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18c1.2 0 2-.8 2-1.8 0-1.3-1.2-1.7-1.2-3 0-1 .8-1.7 1.8-1.7H17a4 4 0 0 0 4-4C21 6.4 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/></svg>',
}
SHARE_ICONS = {
    "pin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.7 2-2.7.9 0 1.4.7 1.4 1.6 0 1-.6 2.4-.9 3.7-.3 1.1.6 2 1.7 2 2 0 3.5-2.1 3.5-5.2 0-2.7-2-4.6-4.8-4.6-3.3 0-5.2 2.5-5.2 5 0 1 .4 2.1.9 2.7l.1.4-.3 1.4c0 .2-.2.3-.4.2-1.5-.7-2.4-2.8-2.4-4.6 0-3.7 2.7-7.2 7.8-7.2 4.1 0 7.3 2.9 7.3 6.9 0 4.1-2.6 7.4-6.2 7.4-1.2 0-2.4-.6-2.7-1.4l-.8 2.8c-.3 1-1 2.3-1.5 3.1A10 10 0 1 0 12 2z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9h3V5h-3c-2.8 0-4 1.7-4 4.3V11H7v4h3v7h4v-7h3l1-4h-4V9.6c0-.4.3-.6.6-.6z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "link": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
}

# Alt text comes from the image manifest so it always describes the actual photo.
def _load_alts():
    try:
        m = json.load(open(os.path.join(ROOT, "assets", "img", "manifest.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: re.sub(r"\s*\([^)]*\)", "", v.get("description", "")).strip().rstrip(".") for k, v in m.items()}


ALT = _load_alts()


# Image slots: 1600/800 webp (3:2); *-hero slots also have 2400 (16:9).
def img_src(slot, w=1600):
    return f"/assets/img/{slot}-{w}.webp"


def img(slot, alt, cls="", eager=False, sizes="(max-width: 700px) 100vw, 50vw", hero=False):
    if hero and slot.endswith("-hero"):
        srcset = f"{img_src(slot, 800)} 800w, {img_src(slot, 1600)} 1600w, {img_src(slot, 2400)} 2400w"
        w, h, src = 2400, 1350, img_src(slot, 1600)
    else:
        srcset = f"{img_src(slot, 800)} 800w, {img_src(slot, 1600)} 1600w"
        w, h, src = 1600, 1067, img_src(slot, 1600 if hero else 800)
    alt = ALT.get(slot) or alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}"{c} {load}>'


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s).lower().replace("&amp;", "and").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def fmt_date(iso, short=False):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return d.strftime("%b %Y" if short else "%B %-d, %Y")


def read_minutes(text):
    words = len(re.sub(r"<[^>]+>", " ", text).split())
    return max(3, round(words / 230))


# ---------------------------------------------------------------- posts
def load_posts():
    posts = []
    d = os.path.join(ROOT, "content", "posts")
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"):
            continue
        raw = open(os.path.join(d, fn), encoding="utf-8").read()
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*(.*)", raw, re.S)
        if not m:
            raise SystemExit(f"bad header in {fn}")
        meta = json.loads(m.group(1))
        meta["body_src"] = m.group(2).strip()
        meta["file"] = fn
        meta["minutes"] = read_minutes(meta["body_src"])
        meta["is_new"] = meta["date"] >= "2026-01-01"
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


POSTS = load_posts()
BY_URL = {p["url"]: p for p in POSTS}
TOOL_BY_KEY = {t["key"]: t for t in TOOLS}
_TAG_COUNTS = {}
for _p in POSTS:
    for _t in _p.get("tags", []):
        _TAG_COUNTS[_t] = _TAG_COUNTS.get(_t, 0) + 1
# Tag archives only where they collect enough stories, plus the two legacy tags that ranked.
TAG_PAGES = {t for t, n in _TAG_COUNTS.items() if n >= 3} | set(TAG_NAMES)


def tool_block(key, heading_level=3):
    t = TOOL_BY_KEY[key]
    return (f'<div class="tool" data-tool="{key}" id="tool-{key}"><div class="tool-head"><div class="ic">{ICONS[t["icon"]]}</div>'
            f'<div><h{heading_level}>{e(t["name"])}</h{heading_level}><p>{e(t["tagline"])}</p></div></div>'
            f'<noscript><p>This interactive tool needs JavaScript turned on.</p></noscript></div>')


def expand_body(src):
    def fig(m):
        slot, alt, cap = m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()
        cap_html = f"<figcaption>{e(cap)}</figcaption>" if cap else ""
        return f'<figure class="reveal">{img(slot, alt, sizes="(max-width: 900px) 100vw, 840px")}{cap_html}</figure>'
    out = re.sub(r"<!--img:([^|>]+)\|([^|>]*)(?:\|([^>]*?))?-->", fig, src)
    out = re.sub(r"<!--tool:([a-z-]+)-->", lambda m: tool_block(m.group(1)), out)
    toc = []
    used = set()

    def h2(m):
        attrs, inner = m.group(1), m.group(2)
        hid = slugify(inner) or "section"
        while hid in used:
            hid += "-2"
        used.add(hid)
        toc.append((hid, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{hid}"{attrs}>{inner}</h2>'
    out = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, out, flags=re.S)
    return out, toc


# ---------------------------------------------------------------- layout
def org_schema():
    return {
        "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE, "url": ORIGIN + "/",
        "email": EMAIL, "logo": {"@type": "ImageObject", "url": ORIGIN + "/apple-touch-icon.png"},
        "description": "An independent journal about weddings, portraits, the desert Southwest and making a home.",
    }


def website_schema():
    return {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE, "publisher": {"@id": ORIGIN + "/#org"}, "inLanguage": "en-US"}


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{e(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{e(n)}</a><span aria-hidden="true">/</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def header(path, solid):
    items = []
    for name, url in NAV:
        cur = ' aria-current="page"' if (path == url or (url != "/" and path.startswith(url))) else ""
        items.append(f'<li><a href="{url}"{cur}>{name}</a></li>')
    items.append('<li class="nav-cta"><a href="/contact/">Say hello</a></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header{' always-solid' if solid else ''}">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Jaz &amp; Theo home">Jaz<span class="amp">&amp;</span>Theo</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{"".join(items)}</ul>
      <div class="nav-extra"><p>Weddings, portraits, desert light and a home made by hand.</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    </nav>
  </div>
</header>'''


def footer():
    cats = "".join(f'<li><a href="/category/{k}/">{v[0]}</a></li>' for k, v in CATS.items())
    tools = "".join(f'<li><a href="{t["url"]}">{e(t["short"])}</a></li>' for t in TOOLS[:6])
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-big" aria-hidden="true">Jaz<span class="amp">&amp;</span>Theo</div>
    <div class="footer-grid">
      <div>
        <h4>The journal</h4>
        <p>An independent journal about weddings, portraits, the desert Southwest and the small projects that make a house feel like home.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Explore</h4><ul><li><a href="/weddings/">Weddings</a></li><li><a href="/portraits/">Portraits</a></li><li><a href="/lifestyle/">Lifestyle</a></li><li><a href="/shop/">Shop &amp; printables</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h4>Journal</h4><ul>{cats}<li><a href="/blog/">All stories</a></li></ul></div>
      <div><h4>Free tools</h4><ul>{tools}<li><a href="/tools/">All tools</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>{date.today().year}</span> Jaz &amp; Theo. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></span>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button>'''


def layout(path, title, desc, body, schema=None, og=None, solid=False, og_type="website", extra_head="", robots=None):
    graph = [org_schema(), website_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    canon = ORIGIN + path
    og_img = ORIGIN + (og or "/assets/img/og-default.jpg")
    tools_js = '\n<script src="/assets/js/tools.js" defer></script>' if 'data-tool="' in body else ""
    progress = '<div class="progress" aria-hidden="true"></div>' if og_type == "article" else ""
    robots_tag = f'\n<meta name="robots" content="{robots}">' if robots else '\n<meta name="robots" content="index, follow, max-image-preview:large">'
    return f'''<!DOCTYPE html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{robots_tag}
<meta property="og:site_name" content="{SITE}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">{extra_head}
<meta name="theme-color" content="#231d2b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Jaz &amp; Theo" href="/rss.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{progress}{header(path, solid)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>{tools_js.replace(".js", ".js?v=" + ASSET_V)}
</body>
</html>
'''


ASSET_V = datetime.now().strftime("%Y%m%d%H%M")


def write(path, content):
    rel = path.lstrip("/")
    if rel.endswith("/") or rel == "":
        rel = rel + "index.html"
    full = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    GENERATED.append(rel)


GENERATED = []
SITEMAP = []  # (path, lastmod, priority)


# ---------------------------------------------------------------- components
def card(p, feature=False, eager=False):
    cat = CATS[p["category"]][0]
    cls = "card card-feature" if feature else "card"
    sizes = "(max-width: 960px) 100vw, 60vw" if feature else "(max-width: 640px) 100vw, (max-width: 960px) 50vw, 33vw"
    return (f'<a class="{cls}" href="{p["url"]}" data-cat="{p["category"]}"><div class="media">{img(p["image"], p["image_alt"], sizes=sizes, eager=eager)}'
            f'<span class="chip">{cat}</span></div><div class="body"><h3>{e(p["title"])}</h3><p>{e(p["excerpt"])}</p>'
            f'<div class="meta"><span>{fmt_date(p["date"], short=True)}</span><span>{p["minutes"]} min read</span></div></div></a>')


def cards_grid(posts, feature_first=False):
    out = []
    for i, p in enumerate(posts):
        out.append(card(p, feature=feature_first and i == 0))
    return f'<div class="cards reveal-stagger">{"".join(out)}</div>'


def page_hero(title, sub, slot=None, alt="", crumbs=None, eyebrow=None):
    media = f'<div class="hero-media">{img(slot, alt, eager=True, sizes="100vw", hero=True)}</div>' if slot else '<div class="sun" aria-hidden="true"></div>'
    cls = "page-hero grain" + ("" if slot else " compact")
    eb = f'<div class="eyebrow" style="color:var(--gold)">{e(eyebrow)}</div>' if eyebrow else ""
    return (f'<section class="{cls}">{media}<div class="wrap">{crumbs_html(crumbs) if crumbs else ""}{eb}'
            f'<h1 class="fade-up">{title}</h1><p class="fade-up" style="animation-delay:.2s">{sub}</p></div></section>')


def faq_html(faqs, heading="Questions, answered"):
    if not faqs:
        return ""
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    return f'<section class="faq"><h2 id="faq">{heading}</h2>{items}</section>'


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def tool_cards(tools, cls="tool-cards reveal-stagger"):
    return f'<div class="{cls}">' + "".join(
        f'<a class="tool-card" href="{t["url"]}"><div class="ic">{ICONS[t["icon"]]}</div><h3>{e(t["name"])}</h3><p>{e(t["tagline"])}</p></a>'
        for t in tools) + "</div>"


def cta_band(title="Have a question, a story idea or a correction?", text="We read every note. Tell us about a venue we should cover, a project you want to see, or something we got wrong."):
    return (f'<section class="section"><div class="wrap"><div class="cta-band reveal">{img("couple-walk", "A couple walking hand in hand at golden hour", sizes="100vw")}'
            f'<h2>{title}</h2><p>{text}</p><div class="hero-actions"><a class="btn btn-light" href="/contact/">Write to us {ARROW}</a>'
            f'<a class="btn btn-outline-light" href="/tools/">Try the free tools</a></div></div></div></section>')


# ---------------------------------------------------------------- post pages
def build_post(p, idx):
    body, toc = expand_body(p["body_src"])
    cat_name = CATS[p["category"]][0]
    url = ORIGIN + p["url"]
    crumbs = [("Home", "/"), ("Journal", "/blog/"), (cat_name, f'/category/{p["category"]}/'), (p["title"], p["url"])]
    toc_html = "".join(f'<li><a href="#{h}">{e(t)}</a></li>' for h, t in toc)
    if p.get("faq"):
        toc_html += '<li><a href="#faq">Questions</a></li>'
    share_t = e(p["title"])
    share = (f'<div class="share"><a href="https://www.pinterest.com/pin/create/button/?url={e(url)}&amp;media={e(ORIGIN + img_src(p["image"]))}&amp;description={share_t}" target="_blank" rel="noopener" aria-label="Save to Pinterest">{SHARE_ICONS["pin"]}</a>'
             f'<a href="https://www.facebook.com/sharer/sharer.php?u={e(url)}" target="_blank" rel="noopener" aria-label="Share on Facebook">{SHARE_ICONS["fb"]}</a>'
             f'<a href="mailto:?subject={share_t}&amp;body={e(url)}" aria-label="Share by email">{SHARE_ICONS["mail"]}</a>'
             f'<button type="button" data-copy="{e(url)}" aria-label="Copy link">{SHARE_ICONS["link"]}</button></div>')
    tags = "".join(f'<a class="chip" style="background:var(--sand)" href="/tag/{t}/">{e(tag_name(t))}</a> ' for t in p.get("tags", []) if t in TAG_PAGES)
    related = [q for q in POSTS if q["category"] == p["category"] and q is not p][:3]
    if len(related) < 3:
        related += [q for q in POSTS if q is not p and q not in related][: 3 - len(related)]
    prev_p = POSTS[idx + 1] if idx + 1 < len(POSTS) else None
    next_p = POSTS[idx - 1] if idx > 0 else None
    nav = '<nav class="post-nav" aria-label="More stories">'
    nav += f'<a href="{prev_p["url"]}"><small>Previous</small>{e(prev_p["title"])}</a>' if prev_p else "<span></span>"
    nav += f'<a class="next" href="{next_p["url"]}"><small>Next</small>{e(next_p["title"])}</a>' if next_p else "<span></span>"
    nav += "</nav>"
    if p["is_new"]:
        dated = f'<time datetime="{p["date"]}">{fmt_date(p["date"])}</time>'
        note = ""
    else:
        dated = f'<span>Updated <time datetime="{MODIFIED}">{fmt_date(MODIFIED)}</time></span>'
        note = f'<p class="updated-note">First published in {fmt_date(p["date"], short=True)} and fully rewritten and updated for {MODIFIED[:4]}. Details like permits, fees and hours change — confirm them with the venue or land manager before you go.</p>'
    hero = (f'<section class="post-hero grain"><div class="hero-media">{img(p["image"], p["image_alt"], eager=True, sizes="100vw", hero=True)}</div>'
            f'<div class="wrap hero-inner">{crumbs_html(crumbs)}<a class="chip chip-clay" href="/category/{p["category"]}/">{cat_name}</a>'
            f'<h1 class="fade-up" style="margin-top:18px">{e(p["title"])}</h1><div class="post-meta fade-up" style="animation-delay:.2s">'
            f'<span>By the Jaz &amp; Theo editors</span><i class="dot"></i>{dated}<i class="dot"></i><span>{p["minutes"]} min read</span></div></div></section>')
    article = (f'<div class="wrap"><div class="article-layout"><aside class="toc" aria-label="In this story"><strong>In this story</strong><ol>{toc_html}</ol>{share}</aside>'
               f'<article class="prose">{body}{faq_html(p.get("faq"))}'
               f'<p style="margin-top:36px">{tags}</p>'
               f'<div class="author-box"><div class="mono" aria-hidden="true">J&amp;T</div><p><b>The Jaz &amp; Theo editors</b> write about weddings, portraits, the desert Southwest and home projects. Spotted something out of date? <a href="/contact/">Tell us</a>.</p></div>'
               f'{note}{nav}</article><div class="article-aside-right"></div></div></div>')
    rel_html = (f'<section class="section section-sand"><div class="wrap"><div class="section-head"><div class="eyebrow">Keep reading</div><h2>More {cat_name.lower()} stories</h2></div>'
                f'{cards_grid(related)}</div></section>')
    schema = [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": p["title"], "description": p["description"],
         "image": [ORIGIN + img_src(p["image"])], "datePublished": p["date"], "dateModified": MODIFIED if not p["is_new"] else p["date"],
         "author": {"@type": "Organization", "name": "Jaz & Theo editors", "url": ORIGIN + "/about/"},
         "publisher": {"@id": ORIGIN + "/#org"}, "mainEntityOfPage": url, "articleSection": cat_name,
         "keywords": ", ".join([p.get("keyword", "")] + p.get("tags", [])), "inLanguage": "en-US",
         "wordCount": len(re.sub(r"<[^>]+>", " ", p["body_src"]).split())},
        crumbs_schema(crumbs),
    ]
    if p.get("faq"):
        schema.append(faq_schema(p["faq"]))
    extra = (f'\n<meta property="article:published_time" content="{p["date"]}T09:00:00-06:00">'
             f'\n<meta property="article:modified_time" content="{(MODIFIED if not p["is_new"] else p["date"])}T09:00:00-06:00">'
             f'\n<meta property="article:section" content="{cat_name}">')
    write(p["url"], layout(p["url"], p["seo_title"], p["description"], hero + article + rel_html, schema,
                           og=img_src(p["image"]), og_type="article", extra_head=extra))
    SITEMAP.append((p["url"], MODIFIED if not p["is_new"] else p["date"], "0.7"))


def in_cat(p, k):
    if k == "travel":
        return p["category"] == "travel" or "jaz-and-theo-weekly-adventures" in p.get("tags", []) or "lake-powell" in p["url"]
    return p["category"] == k


def tag_name(t):
    return TAG_NAMES.get(t, t.replace("-", " ").title())


# ---------------------------------------------------------------- listings
def listing(path, h1, sub, posts, crumbs, title, desc, page=1, pages=1, base=None, intro_html="", eyebrow="The journal", filters=True):
    bar = ""
    if filters:
        links = [f'<a href="/blog/"{" aria-current=\"page\"" if path.startswith("/blog/") else ""}>All</a>']
        for k, (n, _) in CATS.items():
            cur = ' aria-current="page"' if path == f"/category/{k}/" else ""
            links.append(f'<a href="/category/{k}/"{cur}>{n}</a>')
        bar = f'<nav class="filter-bar" aria-label="Categories">{"".join(links)}</nav>'
    pager = ""
    if pages > 1:
        bits = []
        for n in range(1, pages + 1):
            href = base if n == 1 else f"{base}page/{n}/"
            bits.append(f'<span class="current" aria-current="page">{n}</span>' if n == page else f'<a href="{href}">{n}</a>')
        if page < pages:
            bits.append(f'<a href="{base}page/{page + 1}/" aria-label="Next page">&rarr;</a>')
        pager = f'<nav class="pager" aria-label="Pagination">{"".join(bits)}</nav>'
    body = (page_hero(h1, sub, crumbs=crumbs, eyebrow=eyebrow) +
            f'<section class="section"><div class="wrap">{intro_html}{bar}{cards_grid(posts, feature_first=(page == 1 and len(posts) > 4))}{pager}</div></section>' + cta_band())
    schema = [crumbs_schema(crumbs), {"@type": "CollectionPage", "name": title, "url": ORIGIN + path, "description": desc,
              "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["url"]} for i, p in enumerate(posts)]}}]
    extra = ""
    if pages > 1:
        if page > 1:
            extra += f'\n<link rel="prev" href="{ORIGIN}{base if page == 2 else f"{base}page/{page - 1}/"}">'
        if page < pages:
            extra += f'\n<link rel="next" href="{ORIGIN}{base}page/{page + 1}/">'
    write(path, layout(path, title, desc, body, schema, solid=False, extra_head=extra))
    SITEMAP.append((path, MODIFIED, "0.6" if page == 1 else "0.4"))


def build_blog():
    pages = (len(POSTS) + PER_PAGE - 1) // PER_PAGE
    for n in range(1, pages + 1):
        chunk = POSTS[(n - 1) * PER_PAGE: n * PER_PAGE]
        path = "/blog/" if n == 1 else f"/blog/page/{n}/"
        suffix = "" if n == 1 else f" — Page {n}"
        crumbs = [("Home", "/"), ("Journal", "/blog/")] + ([(f"Page {n}", path)] if n > 1 else [])
        listing(path, "The <em class=\"accent\">journal</em>" + (f" · page {n}" if n > 1 else ""),
                "Wedding venue guides, portrait locations, Southwest road trips and home projects — written to be useful.",
                chunk, crumbs, f"The Jaz & Theo Journal{suffix}: Weddings, Portraits & Home",
                f"Every Jaz & Theo story{suffix.lower()}: wedding venue guides, engagement and senior photo spots across El Paso, Arizona and Austin, plus DIY home projects.",
                page=n, pages=pages, base="/blog/")


def build_categories():
    for k, (name, blurb) in CATS.items():
        ps = [p for p in POSTS if in_cat(p, k)]
        path = f"/category/{k}/"
        titles = {
            "wedding": ("Wedding Guides: Venues, Timelines & Photo Tips", "Wedding venue guides for El Paso, Tucson, Phoenix, the Gila Valley and Lake Powell, plus timelines, exits and how to choose a wedding photographer."),
            "portraits": ("Portrait Session Guides: Engagements & Seniors", "Engagement, senior and anniversary photo guides: the best locations in El Paso, Tucson, Phoenix, Los Angeles and Austin, plus outfit help."),
            "home": ("Home Projects: Peg Rails, Lighting & Shiplap", "DIY home projects and ideas: peg rail shelves, shiplap, hanging light fixtures, wall displays, windows, labels and cloth napkins."),
            "travel": ("Travel: Southwest Road Trips & Adventures", "Road-trip guides and travel notes from the Southwest to South Dakota and Yellowstone, with photo tips for every stop."),
            "photography": ("Photography: Learning, Gear & Light", "Photography guides for beginners and working photographers: courses, golden hour, gear gift ideas and the business side."),
        }[k]
        listing(path, e(name), e(blurb), ps, [("Home", "/"), ("Journal", "/blog/"), (name, path)], titles[0], titles[1], eyebrow="Category")


def build_tags():
    tags = {}
    for p in POSTS:
        for t in p.get("tags", []):
            tags.setdefault(t, []).append(p)
    tags = {t: ps for t, ps in tags.items() if t in TAG_PAGES}
    for t, ps in sorted(tags.items()):
        name = tag_name(t)
        path = f"/tag/{t}/"
        n = len(ps)
        desc = f"{n} Jaz & Theo {'story' if n == 1 else 'stories'} tagged {name}: guides on weddings, portraits, travel and home projects across Texas and Arizona."
        listing(path, e(name), f"{n} {'story' if n == 1 else 'stories'} tagged &ldquo;{e(name)}&rdquo;.", ps,
                [("Home", "/"), ("Journal", "/blog/"), (name, path)], f"{name} — Jaz & Theo Journal"[:70], desc, eyebrow="Tag", filters=False)
    return tags


# ---------------------------------------------------------------- tools
def build_tools():
    path = "/tools/"
    body = (page_hero('Free tools for <em class="accent">planning</em> and making', "Calculators and planners we wish we had: golden hour times, wedding-day timelines, photography budgets and a few for the house.",
                      slot="tools-hero", alt="Camera, notebook and planning tools on a table", crumbs=[("Home", "/"), ("Tools", path)], eyebrow="Interactive")
            + f'<section class="section"><div class="wrap"><div class="section-head"><div class="eyebrow">Eight tools, all free</div><h2>Pick a tool</h2><p>No sign-up, nothing saved on our side. Everything runs right in your browser.</p></div>{tool_cards(TOOLS)}</div></section>'
            + f'<section class="section section-sand"><div class="wrap wrap-narrow">{tool_block("golden-hour", 2)}</div></section>' + cta_band())
    schema = [crumbs_schema([("Home", "/"), ("Tools", path)]), {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": ORIGIN + t["url"], "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    write(path, layout(path, "Free Wedding, Photo & Home Calculators | Jaz & Theo", "Free interactive tools: golden hour calculator, wedding day timeline builder, photography cost estimator, chandelier size and peg rail calculators.", body, schema))
    SITEMAP.append((path, MODIFIED, "0.8"))
    for t in TOOLS:
        crumbs = [("Home", "/"), ("Tools", "/tools/"), (t["short"], t["url"])]
        rel = [BY_URL[u] for u in t["related"] if u in BY_URL]
        intro = "".join(f"<p>{x}</p>" for x in t["intro"])
        how = "".join(f"<li>{x}</li>" for x in t["how"])
        others = [o for o in TOOLS if o is not t][:4]
        body = (page_hero(e(t["h1"]), e(t["tagline"]), crumbs=crumbs, eyebrow="Free tool")
                + f'<section class="section" style="padding-top:56px"><div class="wrap wrap-narrow"><div class="prose"><p class="lead">{t["lead"]}</p></div>{tool_block(t["key"], 2)}'
                + f'<div class="prose">{intro}<h2 id="how-it-works">How it works</h2><ul>{how}</ul>{faq_html(t["faq"])}</div></div></section>'
                + (f'<section class="section section-sand"><div class="wrap"><div class="section-head"><div class="eyebrow">Read next</div><h2>Guides that use this tool</h2></div>{cards_grid(rel[:3])}</div></section>' if rel else "")
                + f'<section class="section"><div class="wrap"><div class="section-head"><div class="eyebrow">More free tools</div><h2>Keep planning</h2></div>{tool_cards(others)}</div></section>')
        schema = [crumbs_schema(crumbs), faq_schema(t["faq"]),
                  {"@type": "WebApplication", "name": t["name"], "url": ORIGIN + t["url"], "applicationCategory": "UtilitiesApplication",
                   "operatingSystem": "Any", "browserRequirements": "Requires JavaScript", "description": t["desc"],
                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORIGIN + "/#org"}}]
        write(t["url"], layout(t["url"], t["title"], t["desc"], body, schema))
        SITEMAP.append((t["url"], MODIFIED, "0.7"))


# ---------------------------------------------------------------- hubs
def hub(path, key):
    c = HUB_COPY[key]
    cats = c["cats"]
    ps = [p for p in POSTS if p["category"] in cats]
    crumbs = [("Home", "/"), (c["crumb"], path)]
    sections = ""
    for block in c["blocks"]:
        sections += (f'<section class="section{" section-sand" if block.get("sand") else ""}"><div class="wrap"><div class="split{" reverse" if block.get("reverse") else ""}">'
                     f'<div class="reveal"><div class="eyebrow">{e(block["eyebrow"])}</div><h2>{block["h2"]}</h2>{block["html"]}</div>'
                     f'<div class="stack-img reveal"><div class="main img-reveal">{img(block["img"], block["alt"], sizes="(max-width: 960px) 100vw, 45vw")}</div>'
                     f'<div class="accent-img">{img(block["img2"], block["alt2"], sizes="240px")}</div></div></div></div></section>')
    tools = [TOOL_BY_KEY[k] for k in c["tools"]]
    start = "".join(f'<li><a href="{u}">{e(BY_URL[u]["title"])}</a></li>' for u in c["start"] if u in BY_URL)
    body = (page_hero(c["h1"], c["sub"], slot=c["hero"], alt=c["hero_alt"], crumbs=crumbs, eyebrow=c["eyebrow"])
            + f'<section class="section"><div class="wrap"><div class="split"><div class="reveal"><div class="eyebrow">Start here</div><h2>{c["intro_h2"]}</h2>{c["intro"]}</div>'
            + f'<div class="reveal"><div class="checklist" style="margin:0"><ul>{"".join("<li>" + x + "</li>" for x in c["checklist"])}</ul></div>'
            + f'<p class="tool-note">Tick these off as you go — your progress stays in this browser.</p><h3 style="margin-top:28px">Most-read guides</h3><ul class="plain-links">{start}</ul></div></div></div></section>'
            + sections
            + f'<section class="section section-dusk grain"><div class="wrap"><div class="section-head"><div class="eyebrow">Free tools</div><h2>{c["tools_h2"]}</h2></div>{tool_cards(tools)}</div></section>'
            + f'<section class="section"><div class="wrap"><div class="section-head"><div class="eyebrow">From the journal</div><h2>{c["list_h2"]}</h2></div>{cards_grid(ps, feature_first=True)}</div></section>'
            + f'<section class="section section-sand"><div class="wrap wrap-narrow">{faq_html(c["faq"])}</div></section>' + cta_band())
    schema = [crumbs_schema(crumbs), faq_schema(c["faq"]), {"@type": "CollectionPage", "name": c["title"], "url": ORIGIN + path, "description": c["desc"]}]
    write(path, layout(path, c["title"], c["desc"], body, schema, og=img_src(c["hero"])))
    SITEMAP.append((path, MODIFIED, "0.9"))


# ---------------------------------------------------------------- home
GALLERY = [
    ("gather-estate", "Wedding reception under string lights", "tall"),
    ("sonoran-cactus", "Saguaro cactus against a desert sky", "wide"),
    ("red-sands", "Wind-carved dunes at golden hour", "square"),
    ("lake-powell", "Red rock and blue water at Lake Powell", "wide"),
    ("el-paso-winter", "City lights on a winter evening", "tall"),
    ("peg-rail", "A simple entry with a peg rail shelf", "square"),
    ("bouquet", "A loose garden bouquet", "tall"),
    ("south-dakota", "Layered badlands at dusk", "wide"),
    ("tucson-senior", "A portrait in the Sonoran desert", "tall"),
]


def build_home():
    latest = POSTS[:5]
    popular_urls = ["/2018/03/gather-estate-wedding-arizona-mikayla-shung/", "/2018/11/red-sands-el-paso-tx-yasmin-jared/",
                    "/2019/12/our-entry-peg-rail-shelf-and-shiplap-for-christmas/", "/2019/01/downtown-el-paso-winter-engagement-jordanne-aidan/",
                    "/2018/04/arizona-sonoran-desert-museum-cactus-wedding-erin-ricky/", "/2020/08/lake-powell-desitination-wedding-mikay-ryker/"]
    popular = [BY_URL[u] for u in popular_urls if u in BY_URL]
    tiles = [
        ("01", "Weddings", "/weddings/", "weddings-hero", "Bride and groom embracing outdoors", "Venue guides, timelines, budgets and the photos that matter most."),
        ("02", "Portraits", "/portraits/", "portraits-hero", "A couple laughing during a portrait session", "Engagement, senior and anniversary sessions — where to go and what to wear."),
        ("03", "Home", "/lifestyle/", "kitchen", "A bright, simply styled living space", "Peg rails, shiplap, lighting and small changes with a big payoff."),
        ("04", "Travel", "/category/travel/", "south-dakota-2", "Steam rising from a hot spring in Yellowstone", "Road trips across the Southwest and beyond, with a camera in hand."),
    ]
    tiles_html = "".join(
        f'<a class="tile" href="{u}">{img(s, a, sizes="(max-width: 640px) 50vw, 25vw")}<span class="arrow">{ARROW}</span><div class="num">{n}</div><h3>{t}</h3><p>{d}</p></a>'
        for n, t, u, s, a, d in tiles)
    gal = "".join(
        f'<button type="button" class="{shape}" data-full="{img_src(s)}" data-caption="{e(ALT.get(s, cap))}">{img(s, cap, sizes="(max-width: 640px) 100vw, 33vw")}</button>'
        for s, cap, shape in GALLERY)
    places = [("El Paso", "/2026/09/el-paso-engagement-photo-locations/"), ("Red Sands", "/2018/11/red-sands-el-paso-tx-yasmin-jared/"),
              ("Tucson", "/2019/05/tucson-downtown-and-desert-senior-session/"), ("Sabino Canyon", "/2017/06/hannah-caleb-sabino-canyon-anniversary-session/"),
              ("Phoenix &amp; Papago", "/2018/03/phoenix-papago-desert-engagement-mikayla-shung/"), ("Mesa", "/2018/03/gather-estate-wedding-arizona-mikayla-shung/"),
              ("Gila Valley", "/2018/05/lush-gila-valley-temple-wedding-tia-marco/"), ("Lake Powell", "/2020/08/lake-powell-desitination-wedding-mikay-ryker/"),
              ("Austin", "/2026/08/austin-wedding-photo-locations/"), ("Los Angeles", "/2019/01/downtown-los-angeles-senior-session/"),
              ("Badlands &amp; Yellowstone", "/2018/05/south-dakota-yellowstone-trip/")]
    places_html = "".join(f'<a href="{u}">{n}</a>' for n, u in places)
    badge = ('<div class="badge" aria-hidden="true"><svg viewBox="0 0 100 100"><defs><path id="circ" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0"/></defs>'
             '<text font-size="8.2" letter-spacing="1.9" fill="#1f1b18" font-family="Manrope, sans-serif" font-weight="700"><textPath href="#circ">WEDDINGS · PORTRAITS · HOME · </textPath></text></svg><b>&amp;</b></div>')
    words = ["Weddings", "Engagements", "Desert light", "Senior portraits", "Peg rails &amp; shiplap", "Road trips", "Golden hour", "Home projects"]
    marquee = "".join(f"<span>{w}</span>" for w in words) * 2
    body = f'''
<section class="hero grain">
  <div class="hero-media">{img("home-hero", "A couple embracing in the desert at sunset", eager=True, sizes="100vw", hero=True)}</div>
  <div class="sun" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="eyebrow fade-up" style="color:var(--gold)">Weddings · Portraits · Home · Travel</div>
    <h1 data-split>Love stories, <em class="accent">desert light</em> &amp; a home made by hand</h1>
    <p class="lede fade-up" style="animation-delay:.9s">Jaz &amp; Theo is a journal for couples and makers — wedding venue guides from El Paso to Lake Powell, portrait locations, planning tools, and home projects you can finish in a weekend.</p>
    <div class="hero-actions fade-up" style="animation-delay:1.1s"><a class="btn" href="/blog/">Read the journal {ARROW}</a><a class="btn btn-outline-light" href="/tools/golden-hour-calculator/">Find tonight&rsquo;s golden hour</a></div>
  </div>
  <div class="scroll-cue" aria-hidden="true">Scroll</div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section">
  <div class="wrap split">
    <div class="stack-img reveal">
      <div class="main img-reveal">{img("weddings-hero", "Bride and groom embracing outdoors", sizes="(max-width: 960px) 100vw, 45vw")}</div>
      <div class="accent-img">{img("rings", "Wedding rings resting on a linen napkin", sizes="240px")}</div>
      {badge}
    </div>
    <div class="reveal">
      <div class="eyebrow">Welcome</div>
      <h2>Real places, honest advice, and the <em class="accent">light</em> that makes it all glow</h2>
      <p class="lead-xl">Jaz &amp; Theo started as a photographers&rsquo; blog about weddings in the desert Southwest and the house projects in between. The journal carries that on.</p>
      <p>You&rsquo;ll find guides to venues and photo locations across West Texas, Arizona and Austin, plain-spoken planning help — what photography really costs, how to build a wedding-day timeline, when golden hour starts — and home projects like the peg rail shelf readers still ask us about.</p>
      <div class="stats">
        <div class="stat"><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>in-depth guides</span></div>
        <div class="stat"><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free tools</span></div>
        <div class="stat"><b data-count="11">11</b><span>places covered</span></div>
      </div>
      <p class="signature">— Jaz &amp; Theo</p>
    </div>
  </div>
</section>

<section class="section section-sand" style="padding-top:80px">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">Explore</div><h2>Where would you like to start?</h2></div>
    <div class="tiles reveal-stagger">{tiles_html}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">Fresh in the journal</div><h2>New this season</h2><p>Planning guides written for 2026 couples, with calculators built right in.</p></div>
    {cards_grid(latest, feature_first=True)}
  </div>
</section>

<section class="section section-dusk gh-band grain">
  <div class="sky" aria-hidden="true"></div>
  <div class="wrap gh-live">
    <div class="reveal">
      <div class="eyebrow">Live · El Paso</div>
      <h2>Tonight&rsquo;s golden hour</h2>
      <p style="color:#f3e2d4">The warm, low light photographers chase every evening — calculated from the sun&rsquo;s position for today. Planning a session in Tucson, Austin or Lake Powell? The full calculator covers a dozen places, or uses your location.</p>
      <a class="btn btn-light" href="/tools/golden-hour-calculator/">Open the calculator {ARROW}</a>
    </div>
    <div class="reveal"><div class="tool" data-tool="golden-hour" data-compact data-city="0" style="background:none;border:0;box-shadow:none;padding:0;margin:0"><noscript><p>Turn on JavaScript to see today&rsquo;s times.</p></noscript></div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center"><div class="eyebrow">Reader favorites</div><h2>The stories people keep coming back to</h2></div>
    {cards_grid(popular)}
    <p style="text-align:center;margin-top:44px"><a class="btn btn-ghost" href="/blog/">Browse all {len(POSTS)} stories {ARROW}</a></p>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">The places</div><h2>From the Franklin Mountains to the Badlands</h2><p>Tap a place to read the guide.</p></div>
    <nav class="filter-bar reveal" aria-label="Places">{places_html}</nav>
    <div class="gallery reveal">{gal}</div>
  </div>
</section>

<section class="section section-dusk grain">
  <div class="wrap">
    <div class="section-head"><div class="eyebrow">Free tools</div><h2>Plan it, size it, time it</h2><p>Calculators for the wedding day and for the house — no sign-up, nothing to download.</p></div>
    {tool_cards(TOOLS)}
  </div>
</section>
{cta_band("Planning something? Let&rsquo;s talk.", "Questions about a venue, a home project or a guide? Send a note to " + EMAIL + " or use the contact form — we read everything.")}
'''
    title = "Jaz & Theo — Wedding, Portrait & Home Journal"
    desc = "Wedding venue guides, engagement and senior photo spots from El Paso to Arizona and Austin, golden hour and timeline tools, and DIY home projects."
    write("/home.html", layout("/", title, desc, body, [{"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": title, "isPartOf": {"@id": ORIGIN + "/#website"}}],
                                og="/assets/img/og-default.jpg"))
    SITEMAP.insert(0, ("/", MODIFIED, "1.0"))


# ---------------------------------------------------------------- shop
def build_shop():
    path = "/shop/"
    crumbs = [("Home", "/"), ("Shop", path)]
    items = [
        ("Family formals shot list", "timeline", "A printable, tickable list of the family photo groupings most couples want — hand it to the friend who'll call names.", "/shop/#shot-list", "Use it below"),
        ("Wedding day timeline builder", "reception", "Enter your ceremony time and get a printable, photographer-friendly schedule with golden-hour portraits slotted in.", "/tools/wedding-timeline-builder/", "Build your timeline"),
        ("Photography budget planner", "photo-cost", "See typical price ranges for your region and coverage, then set a realistic budget line.", "/tools/wedding-photography-cost-calculator/", "Estimate costs"),
        ("Peg rail cut & drill plan", "peg-rail-2", "Peg count, exact center marks and rail height for your wall — print it and take it to the garage.", "/tools/peg-rail-spacing-calculator/", "Plan your rail"),
        ("Engagement outfit palettes", "engagement-outfits", "Six color palettes matched to desert, city, mountain, lake, winter-lights and garden settings.", "/tools/engagement-outfit-color-palettes/", "Pick a palette"),
        ("Senior session checklist", "senior-checklist", "Everything to pack, plan and practice before senior pictures, in one printable list.", "/2026/08/senior-portrait-session-checklist/", "Open the checklist"),
    ]
    res = "".join(
        f'<div class="resource reveal"><div class="media">{img(s, n, sizes="(max-width: 960px) 100vw, 40vw")}</div><div class="body"><span class="price-free">FREE</span>'
        f'<h2 style="font-size:1.7rem">{e(n)}</h2><p>{e(d)}</p><a class="btn btn-sm" href="{u}">{e(cta)} {ARROW}</a></div></div>'
        for n, s, d, u, cta in items)
    groups = ["Couple with both sets of parents", "Couple with Partner 1's parents", "Couple with Partner 1's parents and siblings", "Couple with Partner 1's grandparents",
              "Couple with Partner 1's full immediate family", "Couple with Partner 2's parents", "Couple with Partner 2's parents and siblings", "Couple with Partner 2's grandparents",
              "Couple with Partner 2's full immediate family", "Couple with all grandparents", "Couple with both immediate families together", "Extended family (aunts, uncles, cousins) — one big group each side",
              "Couple with godparents or special mentors", "Couple with the officiant", "Couple with any children in the family"]
    shot = "".join(f"<li>{e(g)}</li>" for g in groups)
    body = (page_hero('The <em class="accent">shop</em>: free printables &amp; planners', "Everything here is free — checklists, planners and calculators to print, tick off and share with your people.",
                      slot="shop-hero", alt="Wedding stationery and planning notes laid out on a table", crumbs=crumbs, eyebrow="Free resources")
            + f'<section class="section"><div class="wrap">{res}</div></section>'
            + f'<section class="section section-sand" id="shot-list"><div class="wrap wrap-narrow"><div class="eyebrow">Printable</div><h2>Family formals shot list</h2>'
            + '<p>Family photos go fastest with a written list and one helper who knows everyone. Tick the groups you want (your choices stay in this browser), delete the rest, then print it or screenshot it for your photographer. Plan roughly three minutes per group.</p>'
            + f'<div class="checklist"><ul>{shot}</ul></div><button type="button" class="btn btn-sm no-print" onclick="window.print()">Print this list</button></div></section>'
            + cta_band("Want a printable we haven&rsquo;t made yet?", "Tell us what would help you plan — a shot list, a packing list, a project plan — and we&rsquo;ll consider it for the shop."))
    write(path, layout(path, "Free Wedding Printables & Planners | Jaz & Theo Shop", "Free wedding and home printables: family photo shot list, wedding timeline builder, photography budget planner, peg rail plan and outfit palettes.",
                       body, [crumbs_schema(crumbs)], og=img_src("shop-hero")))
    SITEMAP.append((path, MODIFIED, "0.7"))


# ---------------------------------------------------------------- simple pages
def build_about():
    path = "/about/"
    crumbs = [("Home", "/"), ("About", path)]
    body = (page_hero(ABOUT["h1"], ABOUT["sub"], slot="about-hero", alt="Open road through the desert at sunset", crumbs=crumbs, eyebrow="About")
            + f'<section class="section"><div class="wrap split"><div class="reveal prose">{ABOUT["html"]}</div>'
            + f'<div class="stack-img reveal"><div class="main img-reveal">{img("camera-gear", "A film camera and lenses on a wooden table", sizes="(max-width: 960px) 100vw, 45vw")}</div><div class="accent-img">{img("kitchen", "A warm, simple kitchen corner", sizes="240px")}</div></div></div></section>'
            + cta_band())
    write(path, layout(path, "About Jaz & Theo — A Wedding, Portrait & Home Journal", "About Jaz & Theo: an independent journal about weddings, portraits, the desert Southwest and making a home, with free planning tools.", body,
                       [crumbs_schema(crumbs), {"@type": "AboutPage", "url": ORIGIN + path, "name": "About Jaz & Theo"}]))
    SITEMAP.append((path, MODIFIED, "0.5"))


def build_contact():
    path = "/contact/"
    crumbs = [("Home", "/"), ("Contact", path)]
    topics = ["A question about a guide", "Suggest a venue or location", "Correction or update", "Home project question", "Partnership or press", "Something else"]
    opts = "".join(f"<option>{t}</option>" for t in topics)
    form = f'''<form class="form-card" action="/contact.php" method="post" data-ajax>
  <div class="form-grid">
    <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" autocomplete="name" required minlength="2"></div>
    <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field full"><label for="c-topic">What&rsquo;s it about?</label><select id="c-topic" name="topic">{opts}</select></div>
    <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required minlength="10"></textarea></div>
    <div class="hp" aria-hidden="true"><label for="c-web">Website</label><input id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
  </div>
  <p style="margin-top:20px"><button class="btn" type="submit">Send message {ARROW}</button></p>
  <div class="form-status" role="status" aria-live="polite"></div>
</form>'''
    aside = f'''<div class="contact-aside">
  <div class="box"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p class="tool-note">We aim to reply within two business days.</p></div>
  <div class="box"><h3>Corrections</h3><p>Venues change hands, parks change their permit rules. If a guide is out of date, tell us and we&rsquo;ll update it.</p></div>
  <div class="box"><h3>Please note</h3><p>Jaz &amp; Theo is a journal, not a photography studio — we don&rsquo;t take bookings. We&rsquo;re happy to point you to guides that help you find the right photographer.</p><p><a href="/2018/06/how-to-find-your-wedding-photographer/">How to find your wedding photographer &rarr;</a></p></div>
</div>'''
    body = (page_hero("Say <em class=\"accent\">hello</em>", "Questions, story ideas, corrections or a project you want us to tackle — we read every note.", crumbs=crumbs, eyebrow="Contact")
            + f'<section class="section"><div class="wrap split" style="align-items:start">{form}{aside}</div></section>')
    write(path, layout(path, "Contact Jaz & Theo", "Contact the Jaz & Theo journal at info@jazandtheo.com with questions about a guide, venue suggestions, corrections or home project questions.", body,
                       [crumbs_schema(crumbs), {"@type": "ContactPage", "url": ORIGIN + path, "name": "Contact Jaz & Theo"}]))
    SITEMAP.append((path, MODIFIED, "0.5"))
    t = "/contact/thanks/"
    body = page_hero("Thank <em class=\"accent\">you</em>", "Your note is on its way. We usually reply within two business days.", eyebrow="Message sent") + \
        f'<section class="section"><div class="wrap" style="text-align:center"><a class="btn" href="/blog/">Back to the journal {ARROW}</a></div></section>'
    write(t, layout(t, "Thank You — Jaz & Theo", "Thanks for writing to Jaz & Theo.", body, robots="noindex, follow"))


def build_privacy():
    path = "/privacy-policy/"
    crumbs = [("Home", "/"), ("Privacy policy", path)]
    body = page_hero("Privacy policy", f"Last updated {fmt_date(MODIFIED)}.", crumbs=crumbs) + f'<section class="prose-page"><div class="wrap"><div class="prose">{PRIVACY}</div></div></section>'
    write(path, layout(path, "Privacy Policy | Jaz & Theo", "How the Jaz & Theo website handles contact form messages, browser storage for checklists and tools, and third-party services.", body, [crumbs_schema(crumbs)]))
    SITEMAP.append((path, MODIFIED, "0.2"))


def build_sitemap_page(tags):
    path = "/sitemap/"
    crumbs = [("Home", "/"), ("Sitemap", path)]
    sec = lambda h, links: f"<h2>{h}</h2><ul>" + "".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in links) + "</ul>"
    pages = [("Home", "/"), ("Weddings", "/weddings/"), ("Portraits", "/portraits/"), ("Lifestyle", "/lifestyle/"), ("Journal", "/blog/"), ("Tools", "/tools/"), ("Shop", "/shop/"), ("About", "/about/"), ("Contact", "/contact/"), ("Privacy policy", "/privacy-policy/")]
    html_ = (sec("Pages", pages) + sec("Free tools", [(t["name"], t["url"]) for t in TOOLS])
             + sec("Categories", [(v[0], f"/category/{k}/") for k, v in CATS.items()])
             + "".join(sec(CATS[k][0] + " stories", [(p["title"], p["url"]) for p in POSTS if p["category"] == k]) for k in CATS)
             + sec("Tags", [(tag_name(t), f"/tag/{t}/") for t in sorted(tags)]))
    body = page_hero("Sitemap", "Every page on Jaz &amp; Theo in one place.", crumbs=crumbs) + f'<section class="prose-page"><div class="wrap"><div class="prose html-sitemap">{html_}</div></div></section>'
    write(path, layout(path, "Sitemap | Jaz & Theo", "A complete list of Jaz & Theo pages: wedding, portrait, home and travel guides, free tools and categories.", body, [crumbs_schema(crumbs)]))
    SITEMAP.append((path, MODIFIED, "0.2"))


def build_404():
    body = (f'<section class="notfound"><div class="wrap"><div class="big">404</div><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">This trail fades out in the sand</h1>'
            f'<p>The page you&rsquo;re after has moved or never existed. Try the journal, or one of these favorites.</p>'
            f'<p class="hero-actions" style="justify-content:center;margin-top:24px"><a class="btn" href="/">Go home {ARROW}</a><a class="btn btn-ghost" href="/blog/">Browse the journal</a></p></div></section>'
            f'<section class="section section-sand"><div class="wrap">{cards_grid(POSTS[:3])}</div></section>')
    content = layout("/404.html", "Page not found | Jaz & Theo", "That page could not be found.", body, solid=True, robots="noindex, follow")
    write("/404.html", content)
    GENERATED.pop()


# ---------------------------------------------------------------- feeds
def build_xml():
    urls = "".join(f"<url><loc>{ORIGIN}{p}</loc><lastmod>{m}</lastmod><priority>{pr}</priority></url>\n" for p, m, pr in SITEMAP)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /contact.php\nDisallow: /contact/thanks/\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    items = ""
    for p in POSTS[:20]:
        d = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 09:00:00 -0600")
        items += f"<item><title>{e(p['title'])}</title><link>{ORIGIN}{p['url']}</link><guid>{ORIGIN}{p['url']}</guid><pubDate>{d}</pubDate><description>{e(p['excerpt'])}</description></item>\n"
    open(os.path.join(ROOT, "rss.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Jaz &amp; Theo</title><link>{ORIGIN}/</link><description>Weddings, portraits, the desert Southwest and making a home.</description><language>en-us</language>\n{items}</channel></rss>\n')
    manifest = {"name": "Jaz & Theo", "short_name": "Jaz & Theo", "start_url": "/", "display": "standalone", "background_color": "#fbf7f1", "theme_color": "#231d2b",
                "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png"}]}
    open(os.path.join(ROOT, "site.webmanifest"), "w").write(json.dumps(manifest, indent=2) + "\n")


def clean_previous():
    mf = os.path.join(ROOT, ".generated")
    if os.path.exists(mf):
        for rel in open(mf).read().split():
            f = os.path.join(ROOT, rel)
            if os.path.isfile(f):
                os.remove(f)
        for top in ["2017", "2018", "2019", "2020", "2026", "blog", "category", "tag", "tools", "weddings", "portraits", "lifestyle", "shop", "about", "contact", "privacy-policy", "sitemap"]:
            d = os.path.join(ROOT, top)
            for dirpath, dirs, files in sorted(os.walk(d, topdown=False)):
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)


def main():
    clean_previous()
    for i, p in enumerate(POSTS):
        build_post(p, i)
    build_home()
    hub("/weddings/", "weddings")
    hub("/portraits/", "portraits")
    hub("/lifestyle/", "lifestyle")
    build_blog()
    build_categories()
    tags = build_tags()
    build_tools()
    build_shop()
    build_about()
    build_contact()
    build_privacy()
    build_sitemap_page(tags)
    build_404()
    build_xml()
    open(os.path.join(ROOT, ".generated"), "w").write("\n".join(sorted(GENERATED)) + "\n")
    print(f"built {len(GENERATED)} pages ({len(POSTS)} posts, {len(tags)} tags, {len(TOOLS)} tools)")


if __name__ == "__main__":
    main()
