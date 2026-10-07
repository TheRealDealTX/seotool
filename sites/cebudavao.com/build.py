#!/usr/bin/env python3
"""Static generator for cebudavao.com.

Reads content/posts/*.md (new + recreated legacy posts), the WordPress REST
export of the 51 posts kept from the 2023-2025 site, data/*.py and
data/photos.json, and writes the whole site into public/ (deployed as-is to
the Hostinger PHP website). Standard library only. See README.md.
"""
import glob
import html
import json
import math
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "data"))

import md  # noqa: E402
import pages as static_pages  # noqa: E402
import plan  # noqa: E402
import redirects  # noqa: E402
from config import CATEGORIES, NAV, PLACES, SITE, TODAY, WEATHER_CITIES  # noqa: E402

OUT = os.path.join(ROOT, "public")
ORIGIN = SITE["origin"]
WP = os.path.join(ROOT, "backup", "wordpress-2026-10-07", "api")
PER_PAGE = 24
PHOTOS = json.load(open(os.path.join(ROOT, "data", "photos.json"), encoding="utf-8"))
ASSET_V = datetime.now().strftime("%Y%m%d%H%M")

CATEGORY_FALLBACK_IMG = {
    "news": "cebu-skyline", "travel": "island-hopping", "food": "market-carbon", "culture": "santo-nino-basilica",
    "lifestyle": "coffee", "entertainment": "guitar-band", "sports": "basketball-court", "money": "money-peso",
    "tech": "smartphone", "expat-living": "manila-skyline",
}

esc = html.escape


# --------------------------------------------------------------------------- helpers

def write(rel, content):
    path = os.path.join(OUT, rel.lstrip("/"))
    if rel.endswith("/"):
        path = os.path.join(path, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def fmt_date(iso):
    d = datetime.fromisoformat(iso[:10])
    return d.strftime("%B %-d, %Y")


def strip_tags(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or ""))).strip()


def clip(s, n):
    s = strip_tags(s)
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def photo(key):
    return PHOTOS.get(key)


def image_for(post):
    """Return dict(src, src_sm, w, h, credit_html) for a post's lead image."""
    if post.get("wp_image"):
        return post["wp_image"]
    for key in (post.get("image"), CATEGORY_FALLBACK_IMG.get(post["category"]), "cebu-skyline"):
        p = photo(key) if key else None
        if p:
            return {
                "src": f"/assets/img/photos/{key}.webp", "src_sm": f"/assets/img/photos/{key}-sm.webp",
                "w": p["w"], "h": p["h"], "key": key,
                "credit": f'Photo: {esc(p["author"])} / <a href="{esc(p["source"])}" rel="noopener" target="_blank">{esc(p["license"])}</a>, via Wikimedia Commons',
            }
    return None


def img_tag(im, alt, cls="", eager=False, sizes="(max-width: 700px) 100vw, 700px"):
    if not im:
        return f'<div class="img-ph {cls}" aria-hidden="true"></div>'
    srcset = f'{im["src_sm"]} 640w, {im["src"]} {min(im["w"], 1200)}w' if im.get("src_sm") else ""
    h = round(im["h"] * 1200 / im["w"]) if im["w"] > 1200 else im["h"]
    w = min(im["w"], 1200)
    attrs = f'src="{im["src"]}" width="{w}" height="{h}" alt="{esc(alt)}"'
    if srcset:
        attrs += f' srcset="{srcset}" sizes="{sizes}"'
    attrs += ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"'
    return f'<img class="{cls}" {attrs}>'


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def cat_name(slug):
    return CATEGORIES[slug][0]


def cat_url(slug):
    return f"/category/{slug}/"


ORG = {
    "@type": "NewsMediaOrganization", "@id": ORIGIN + "/#org", "name": SITE["name"], "url": ORIGIN + "/",
    "logo": {"@type": "ImageObject", "url": ORIGIN + "/assets/img/logo-512.png", "width": 512, "height": 512},
    "foundingDate": SITE["founded"], "email": SITE["email"],
    "publishingPrinciples": ORIGIN + "/editorial-policy/", "areaServed": ["Cebu", "Davao", "Philippines"],
}
WEBSITE = {
    "@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE["name"],
    "description": SITE["tagline"], "publisher": {"@id": ORIGIN + "/#org"}, "inLanguage": "en-PH",
    "potentialAction": {"@type": "SearchAction", "target": ORIGIN + "/search/?q={search_term_string}",
                        "query-input": "required name=search_term_string"},
}


def breadcrumb_ld(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u} for i, (n, u) in enumerate(trail)]}


def breadcrumbs_html(trail):
    parts = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span class="sep">/</span> '.join(parts) + "</nav>"


# --------------------------------------------------------------------------- layout

ICONS = {
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "close": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v6h4v-6h3l1-4h-4V8a0 0 0 0 1 0 0z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4l16 16M20 4 4 20"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9c0 3 3 6 6 6l1-1.5-2-1-1 1c-1-.5-2-1.5-2.5-2.5l1-1-1-2z"/></svg>',
    "link": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
}

LOGO = ('<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="var(--sea)"/>'
        '<circle cx="31" cy="17" r="7" fill="var(--sun)"/><path d="M3 30c5-4 9-4 14 0s9 4 14 0 9-4 14 0v6a23 23 0 0 1-42 0z" fill="#fff" opacity=".92"/>'
        '<path d="M3 36c5-4 9-4 14 0s9 4 14 0 9-4 14 0" stroke="var(--sea-d)" stroke-width="2.4" fill="none"/></svg>')


def header_html(active=""):
    nav = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if active == u else ""}>{esc(n)}</a></li>' for n, u in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap topbar-in">
  <span class="tb-date" data-phdate>Philippines</span>
  <a class="tb-wx" href="/weather/" data-wxmini aria-label="Weather in Cebu and Davao">Cebu <b>--°</b> · Davao <b>--°</b></a>
  <span class="tb-links"><a href="/tools/currency-converter/" data-fxmini>₱ rates</a><a href="/news/">Live news</a><a href="/about/">About</a></span>
</div></div>
<header class="site-header"><div class="wrap hdr-in">
  <button class="icon-btn nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">{ICONS["menu"]}</button>
  <a class="brand" href="/" aria-label="{SITE["name"]} home">{LOGO}<span class="brand-txt"><span class="bn">Cebu<i>·</i>Davao</span><small>News · Travel · Life</small></span></a>
  <div class="hdr-actions">
    <a class="icon-btn" href="/search/" aria-label="Search" data-search-open>{ICONS["search"]}</a>
    <button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">{ICONS["moon"]}</button>
  </div>
</div>
<nav id="primary-nav" class="primary-nav" aria-label="Primary"><div class="wrap"><ul>{nav}</ul></div></nav>
</header>'''


def footer_html():
    cats = "".join(f'<li><a href="{cat_url(s)}">{esc(v[0])}</a></li>' for s, v in CATEGORIES.items())
    return f'''<footer class="site-footer">
<div class="wrap foot-grid">
  <div class="foot-brand">
    <a class="brand brand-foot" href="/">{LOGO}<span class="brand-txt"><span class="bn">Cebu<i>·</i>Davao</span><small>News · Travel · Life</small></span></a>
    <p>{esc(SITE["tagline"])}. Independent, local and proudly Bisaya.</p>
    <form class="newsletter" action="/api/subscribe.php" method="post" data-ajax-form>
      <label for="nl-email">Get the weekly Cebu-Davao letter</label>
      <div class="nl-row"><input id="nl-email" type="email" name="email" placeholder="you@example.com" required autocomplete="email">
      <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button type="submit">Subscribe</button></div>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
  <div><h2>Sections</h2><ul>{cats}</ul></div>
  <div><h2>Places & tools</h2><ul>
    <li><a href="/cebu/">Cebu guide</a></li><li><a href="/davao/">Davao guide</a></li><li><a href="/philippines/">Around the Philippines</a></li>
    <li><a href="/weather/">Weather forecast</a></li><li><a href="/tools/">Reader tools</a></li><li><a href="/news/">Live news wire</a></li>
    <li><a href="/tools/festival-calendar/">Festival calendar</a></li><li><a href="/tools/bisaya-dictionary/">Bisaya dictionary</a></li></ul></div>
  <div><h2>Cebu-Davao</h2><ul>
    <li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/editorial-policy/">Editorial policy</a></li>
    <li><a href="/faqs/">FAQs</a></li><li><a href="/blog/">All stories</a></li><li><a href="/photo-credits/">Photo credits</a></li>
    <li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
</div>
<div class="wrap foot-base"><p>© {TODAY[:4]} {SITE["name"]} · cebudavao.com · Weather data by <a href="https://open-meteo.com/" rel="noopener" target="_blank">Open-Meteo</a> · Rates by <a href="https://www.exchangerate-api.com" rel="noopener" target="_blank">ExchangeRate-API</a></p>
<p><a href="#top" class="to-top">Back to top ↑</a></p></div>
</footer>
<div class="search-overlay" data-search-overlay hidden><div class="search-box" role="dialog" aria-modal="true" aria-label="Search">
<form action="/search/" role="search"><label class="sr" for="ovq">Search Cebu-Davao</label><input id="ovq" name="q" type="search" placeholder="Search lechon, Samal, typhoon signal…" autocomplete="off" data-search-input>
<button type="button" class="icon-btn" data-search-close aria-label="Close search">{ICONS["close"]}</button></form>
<ul class="search-results" data-search-results></ul></div></div>'''


def page(path, title, description, body, *, ld=None, og_type="website", image=None, active="", robots=None,
         extra_head="", full_title=False, body_class=""):
    canonical = ORIGIN + path
    t = title if full_title or len(title) > 52 else f"{title} | {SITE['name']}"
    og_img = ORIGIN + (image["src"] if image else "/assets/img/og-default.jpg")
    graph = [ORG, WEBSITE] + (ld or [])
    head_ld = jsonld({"@context": "https://schema.org", "@graph": graph})
    return f'''<!doctype html>
<html lang="en-PH" id="top">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
{f'<meta name="robots" content="{robots}">' if robots else '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">'}
<meta property="og:site_name" content="{SITE["name"]}">
<meta property="og:locale" content="{SITE["locale"]}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b2a3f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{SITE["name"]} RSS" href="{ORIGIN}/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script>try{{var t=localStorage.getItem("cd-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{extra_head}{head_ld}
</head>
<body class="{body_class}">
{header_html(active)}
<main id="main">
{body}
</main>
{footer_html()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


# --------------------------------------------------------------------------- widgets

def widget(name):
    if name in ("weather-cebu", "weather-davao"):
        city = "cebu-city" if name.endswith("cebu") else "davao-city"
        return (f'<div class="widget wx-widget" data-wx-card="{city}"><p class="wx-loading">Loading live weather for '
                f'{WEATHER_CITIES[city][0]}…</p><p class="widget-foot"><a href="/weather/{city}/">Full {WEATHER_CITIES[city][0]} forecast →</a></p></div>')
    if name.startswith("news-wire-"):
        topic = name.split("-")[-1]
        return (f'<div class="widget news-wire" data-news="{topic}"><h3 class="widget-title">Latest {topic.title()} headlines</h3>'
                f'<ul class="wire-list"><li class="muted">Loading headlines…</li></ul><p class="widget-foot">Headlines link to the original publishers. '
                f'<a href="/news/">More live news →</a></p></div>')
    tool = {
        "fish-translator": ("fish", "Fish name translator", "/tools/fish-names/"),
        "bisaya-dictionary": ("bisaya", "Bisaya–Tagalog–English dictionary", "/tools/bisaya-dictionary/"),
        "distance": ("distance", "Distance between Philippine cities", "/travel/mileage-from-to-distance-between-cities/"),
        "currency": ("currency", "Peso currency converter", "/tools/currency-converter/"),
        "budget": ("budget", "Trip budget calculator", "/tools/trip-budget-calculator/"),
        "quiz-destinations": ("quiz", "Name these Philippine destinations", "/fun-quizzes/name-these-philippine-travel-destinations/"),
        "festival-countdown": ("festivals", "Festival countdown", "/tools/festival-calendar/"),
    }.get(name)
    if not tool:
        return ""
    t, label, url = tool
    return (f'<div class="widget tool-embed" data-tool="{t}" data-compact="1"><h3 class="widget-title">{label}</h3>'
            f'<noscript><p>This interactive tool needs JavaScript.</p></noscript>'
            f'<p class="widget-foot"><a href="{url}">Open the full tool →</a></p></div>')


# --------------------------------------------------------------------------- content loading

def load_md_posts():
    posts = []
    legacy_paths = {p for p, *_ in plan.LEGACY}
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "posts", "*.md"))):
        meta, body = md.parse_front(open(f, encoding="utf-8").read())
        path = meta["path"]
        if not path.endswith("/"):
            path += "/"
        cat = meta.get("category", "news")
        if cat not in CATEGORIES:
            raise SystemExit(f"{f}: unknown category {cat}")
        html_body, headings, faqs = md.render(body, widget)
        words = len(strip_tags(html_body).split())
        post = {
            "file": os.path.relpath(f, ROOT), "path": path, "title": meta["title"], "h1": meta.get("h1", meta["title"]),
            "description": meta.get("description", ""), "excerpt": meta.get("excerpt") or clip(html_body, 180),
            "category": cat, "places": [p.strip() for p in meta.get("places", "other").split(",") if p.strip() in PLACES] or ["other"],
            "keyword": meta.get("keyword", ""), "image": meta.get("image", ""), "image_alt": meta.get("image_alt") or meta["title"],
            "type": meta.get("type", "article"), "date": meta.get("date", TODAY), "updated": meta.get("updated", TODAY),
            "html": html_body, "headings": [h for h in headings if not h[0].startswith("frequently")], "faqs": faqs,
            "words": words, "author": SITE["editorial"], "author_url": "/about/", "legacy": path in legacy_paths,
            "recipe": None, "source": "md",
        }
        if post["type"] == "recipe":
            post["recipe"] = {
                "yield": meta.get("recipe_yield", ""), "prep": meta.get("recipe_prep", ""), "cook": meta.get("recipe_cook", ""),
                "ingredients": md.section_items(body, "Ingredients"), "steps": md.section_items(body, "Instructions"),
            }
        posts.append(post)
    return posts


def clean_wp_html(c):
    c = re.sub(r'\s(data-start|data-end|data-is-last-node|data-is-only-node|data-col-size)="[^"]*"', "", c)
    c = re.sub(r"<style.*?</style>", "", c, flags=re.S)
    c = c.replace("https://cebudavao.com/wp-content/", "/wp-content/")
    c = re.sub(r'<img ', '<img loading="lazy" decoding="async" ', c)
    # make heading ids for TOC
    def hid(m):
        text = strip_tags(m.group(2))
        return f'<h{m.group(1)} id="{md.slugify(text)}">{m.group(2)}</h{m.group(1)}>'
    c = re.sub(r"<h([23])[^>]*>(.*?)</h\1>", hid, c, flags=re.S)
    return c


def wp_featured(media_by_id, mid):
    m = media_by_id.get(mid)
    if not m:
        return None
    rel = re.sub(r"^https?://cebudavao\.com", "", m["source_url"])
    local = os.path.join(ROOT, rel.lstrip("/"))
    if not os.path.exists(local):
        return None
    # derived WebP copies in assets/img/wp/
    out_big = os.path.join(ROOT, "assets", "img", "wp", f"{mid}.webp")
    out_sm = os.path.join(ROOT, "assets", "img", "wp", f"{mid}-sm.webp")
    if not os.path.exists(out_big):
        from PIL import Image
        os.makedirs(os.path.dirname(out_big), exist_ok=True)
        im = Image.open(local).convert("RGB")
        for w, p in ((1200, out_big), (640, out_sm)):
            c = im.copy(); c.thumbnail((w, w * 2)); c.save(p, "WEBP", quality=78, method=6)
    from PIL import Image
    w, h = Image.open(out_big).size
    return {"src": f"/assets/img/wp/{mid}.webp", "src_sm": f"/assets/img/wp/{mid}-sm.webp", "w": w, "h": h,
            "credit": "", "alt": strip_tags(m.get("alt_text") or m["title"]["rendered"])}


def load_wp_posts():
    posts = []
    media_by_id = {m["id"]: m for m in json.load(open(os.path.join(WP, "media.json"), encoding="utf-8"))}
    for p in json.load(open(os.path.join(WP, "posts.json"), encoding="utf-8")):
        path = "/" + p["slug"] + "/"
        body = clean_wp_html(p["content"]["rendered"])
        title = strip_tags(p["title"]["rendered"]) or "Living abroad notes"
        excerpt = clip(p["excerpt"]["rendered"], 180)
        fi = wp_featured(media_by_id, p["featured_media"])
        heads = [(i, strip_tags(t)) for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S)]
        posts.append({
            "file": None, "path": path, "title": title, "h1": title,
            "description": clip(p["excerpt"]["rendered"], 155), "excerpt": excerpt, "category": "expat-living",
            "places": ["other"], "keyword": "", "image": "", "wp_image": fi, "image_alt": (fi or {}).get("alt") or title,
            "type": "article", "date": p["date"][:10], "updated": p["modified"][:10], "html": body,
            "headings": heads, "faqs": [], "words": len(strip_tags(body).split()), "author": "Brandy",
            "author_url": "/category/expat-living/", "legacy": True, "recipe": None, "source": "wp",
        })
    return posts


# --------------------------------------------------------------------------- cards & lists

def card(p, size="md", show_cat=True):
    im = image_for(p)
    cat = p["category"]
    color = CATEGORIES[cat][2]
    badge = f'<a class="badge" style="--c:{color}" href="{cat_url(cat)}">{esc(cat_name(cat))}</a>' if show_cat else ""
    ex = f'<p class="card-ex">{esc(p["excerpt"])}</p>' if size in ("lg", "md") else ""
    sizes = "(max-width: 700px) 100vw, 640px" if size == "lg" else "(max-width: 700px) 50vw, 360px"
    return f'''<article class="card card-{size}">
  <a class="card-img" href="{p["path"]}" tabindex="-1" aria-hidden="true">{img_tag(im, p["image_alt"], sizes=sizes)}</a>
  <div class="card-body">{badge}
    <h3 class="card-title"><a href="{p["path"]}">{esc(p["title"])}</a></h3>{ex}
    <p class="card-meta"><time datetime="{p["updated"]}">{fmt_date(p["updated"])}</time> · {max(1, round(p["words"] / 220))} min read</p>
  </div>
</article>'''


def mini(p):
    return f'<li><a href="{p["path"]}">{esc(p["title"])}</a><span class="muted"> · {esc(cat_name(p["category"]))}</span></li>'


def pager(base, page_no, pages):
    if pages <= 1:
        return ""
    links = []
    for n in range(1, pages + 1):
        url = base if n == 1 else f"{base}page/{n}/"
        cur = ' aria-current="page"' if n == page_no else ""
        links.append(f'<a href="{url}"{cur}>{n}</a>')
    prev = f'<a rel="prev" href="{base if page_no == 2 else f"{base}page/{page_no - 1}/"}">← Newer</a>' if page_no > 1 else ""
    nxt = f'<a rel="next" href="{base}page/{page_no + 1}/">Older →</a>' if page_no < pages else ""
    return f'<nav class="pager" aria-label="Pagination">{prev}{"".join(links)}{nxt}</nav>'


def listing_pages(base, title, intro, items, trail, desc, *, hero_extra="", active="", aside="", seo_title=None):
    pages_n = max(1, math.ceil(len(items) / PER_PAGE))
    for n in range(1, pages_n + 1):
        chunk = items[(n - 1) * PER_PAGE: n * PER_PAGE]
        url = base if n == 1 else f"{base}page/{n}/"
        t = title if n == 1 else f"{title} – Page {n}"
        st = (seo_title or title) if n == 1 else f"{seo_title or title} – Page {n}"
        body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html(trail)}
<h1>{esc(t)}</h1><p class="lede">{intro}</p>{hero_extra if n == 1 else ""}</div></section>
<div class="wrap layout"><div class="main-col"><div class="grid grid-3">{"".join(card(p) for p in chunk)}</div>
{pager(base, n, pages_n)}</div>{aside}</div>'''
        ld = [breadcrumb_ld(trail), {"@type": "CollectionPage", "name": t, "url": ORIGIN + url, "description": desc,
              "isPartOf": {"@id": ORIGIN + "/#website"},
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["path"]} for i, p in enumerate(chunk)]}}]
        write(url, page(url, st, desc if n == 1 else f"{desc} Page {n}.", body, ld=ld, active=active,
                        robots="noindex, follow" if n > 1 else None))


def sidebar(posts, place=None, exclude=None):
    pop = [p for p in POPULAR if p["path"] != exclude][:6]
    wx = "davao-city" if place == "davao" else "cebu-city"
    return f'''<aside class="side-col">
<div class="widget wx-widget" data-wx-card="{wx}"><p class="wx-loading">Loading live weather…</p><p class="widget-foot"><a href="/weather/">All forecasts →</a></p></div>
<div class="widget"><h3 class="widget-title">Most read</h3><ol class="pop-list">{"".join(f'<li><a href="{p["path"]}">{esc(p["title"])}</a></li>' for p in pop)}</ol></div>
<div class="widget tools-mini"><h3 class="widget-title">Reader tools</h3><ul>
<li><a href="/tools/currency-converter/">₱ Currency converter</a></li><li><a href="/tools/trip-budget-calculator/">Trip budget calculator</a></li>
<li><a href="/tools/bisaya-dictionary/">Bisaya dictionary</a></li><li><a href="/tools/festival-calendar/">Festival countdown</a></li>
<li><a href="/tools/fish-names/">Fish name translator</a></li><li><a href="/travel/mileage-from-to-distance-between-cities/">City distance calculator</a></li>
<li><a href="/tools/packing-checklist/">Packing checklist</a></li></ul></div>
</aside>'''


# --------------------------------------------------------------------------- post page

def related(p, posts, n=4):
    def score(q):
        s = 0
        if q["category"] == p["category"]:
            s += 3
        s += 2 * len(set(q["places"]) & set(p["places"]) - {"other"})
        return s
    cands = [q for q in posts if q["path"] != p["path"] and (q["category"] != "expat-living" or p["category"] == "expat-living")]
    cands.sort(key=lambda q: (-score(q), q["title"]))
    return cands[:n]


def post_page(p, posts):
    im = image_for(p)
    cat = p["category"]
    trail = [("Home", "/"), (cat_name(cat), cat_url(cat)), (p["title"], p["path"])]
    read = max(1, round(p["words"] / 220))
    toc = ""
    if len(p["headings"]) >= 4:
        toc = '<details class="toc" open><summary>In this article</summary><ol>' + "".join(
            f'<li><a href="#{i}">{esc(strip_tags(t))}</a></li>' for i, t in p["headings"]) + "</ol></details>"
    places = "".join(f'<a class="chip" href="{PLACES[x][1]}">{PLACES[x][0]}</a>' for x in p["places"])
    figure = ""
    if im:
        cap = f'<figcaption>{im["credit"]}</figcaption>' if im.get("credit") else ""
        figure = f'<figure class="lead-img">{img_tag(im, p["image_alt"], eager=True, sizes="(max-width: 1100px) 100vw, 760px")}{cap}</figure>'
    share_url = esc(ORIGIN + p["path"])
    share_t = esc(p["title"])
    share = f'''<div class="share" aria-label="Share this article"><span>Share</span>
<a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener" aria-label="Share on Facebook">{ICONS["fb"]}</a>
<a href="https://twitter.com/intent/tweet?url={share_url}&amp;text={share_t}" target="_blank" rel="noopener" aria-label="Share on X">{ICONS["x"]}</a>
<a href="https://wa.me/?text={share_t}%20{share_url}" target="_blank" rel="noopener" aria-label="Share on WhatsApp">{ICONS["wa"]}</a>
<button type="button" data-copy="{share_url}" aria-label="Copy link">{ICONS["link"]}</button></div>'''
    updated_note = ""
    if p["updated"] != p["date"]:
        updated_note = f' · Updated <time datetime="{p["updated"]}">{fmt_date(p["updated"])}</time>'
    rel = related(p, posts)
    rel_html = f'<section class="related"><h2>Keep reading</h2><div class="grid grid-2">{"".join(card(q, "sm") for q in rel)}</div></section>' if rel else ""
    recipe_box = ""
    if p["recipe"]:
        r = p["recipe"]
        def dur(s):
            m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", s or "")
            if not m or not any(m.groups()):
                return "—"
            return " ".join(x for x in [f"{m.group(1)} hr" if m.group(1) else "", f"{m.group(2)} min" if m.group(2) else ""] if x)
        recipe_box = (f'<div class="recipe-box"><div><span>Prep</span><b>{dur(r["prep"])}</b></div><div><span>Cook</span><b>{dur(r["cook"])}</b></div>'
                      f'<div><span>Serves</span><b>{esc(r["yield"] or "—")}</b></div><div><a class="btn btn-sm" href="#ingredients">Jump to recipe</a> '
                      f'<button class="btn btn-sm btn-ghost" type="button" data-print>Print</button></div></div>')
    author_box = (f'<div class="author-box"><div class="avatar" aria-hidden="true">{esc(p["author"][:1])}</div><div><p><b>{esc(p["author"])}</b></p>'
                  + ('<p>Local writers and editors covering Cebu, Davao and the wider Philippines. We fact-check against official sources and update guides when things change. '
                     '<a href="/editorial-policy/">How we work</a> · <a href="/contact/">Suggest a correction</a></p>' if p["source"] == "md" else
                     '<p>Part of our Living Abroad archive — notes on moving, renting and travelling from our Texan wanderlust years.</p>')
                  + "</div></div>")
    disclaimer = ""
    if p["category"] == "lifestyle" and any(k in p["path"] for k in ("health", "simian", "cancer")):
        disclaimer = '<aside class="callout callout-warn"><p>This article is for general information and is not medical advice. Please consult a doctor about your own health.</p></aside>'
    body = f'''<div class="progress" aria-hidden="true"><span data-progress></span></div>
<article class="post" data-post>
<header class="post-head wrap-narrow">{breadcrumbs_html(trail)}
<a class="badge" style="--c:{CATEGORIES[cat][2]}" href="{cat_url(cat)}">{esc(cat_name(cat))}</a>
<h1>{esc(p["h1"])}</h1>
<p class="dek">{esc(p["excerpt"])}</p>
<p class="byline">By <a href="{p["author_url"]}">{esc(p["author"])}</a> · <time datetime="{p["date"]}">{fmt_date(p["date"])}</time>{updated_note} · {read} min read</p>
<div class="post-tools">{places}{share}</div>
</header>
<div class="wrap-wide">{figure}</div>
<div class="wrap layout post-layout"><div class="main-col prose">
{recipe_box}{toc}{disclaimer}
{p["html"]}
{share}
{author_box}
{rel_html}
</div>{sidebar(posts, p["places"][0], p["path"])}</div>
</article>'''
    img_url = ORIGIN + im["src"] if im else ORIGIN + "/assets/img/og-default.jpg"
    art_type = "NewsArticle" if cat == "news" else "BlogPosting"
    author = ({"@type": "Organization", "name": p["author"], "url": ORIGIN + "/about/"} if p["source"] == "md"
              else {"@type": "Person", "name": p["author"]})
    art = {"@type": art_type, "@id": ORIGIN + p["path"] + "#article", "headline": p["title"][:110],
           "description": p["description"], "image": [img_url], "datePublished": p["date"] + "T08:00:00+08:00",
           "dateModified": p["updated"] + "T08:00:00+08:00", "author": author, "publisher": {"@id": ORIGIN + "/#org"},
           "mainEntityOfPage": ORIGIN + p["path"], "articleSection": cat_name(cat), "inLanguage": "en-PH",
           "wordCount": p["words"]}
    if p["keyword"]:
        art["keywords"] = p["keyword"]
    if any(x in p["places"] for x in ("cebu", "davao")):
        art["contentLocation"] = [{"@type": "Place", "name": PLACES[x][0] + ", Philippines"} for x in p["places"] if x != "other"]
    ld = [art, breadcrumb_ld(trail)]
    if p["faqs"]:
        ld.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(md.inline(a))}} for q, a in p["faqs"]]})
    if p["recipe"] and p["recipe"]["ingredients"]:
        r = p["recipe"]
        rec = {"@type": "Recipe", "name": p["title"], "image": [img_url], "description": p["description"],
               "author": author, "datePublished": p["date"], "recipeCuisine": "Filipino", "recipeCategory": "Main course",
               "keywords": p["keyword"], "recipeIngredient": r["ingredients"],
               "recipeInstructions": [{"@type": "HowToStep", "text": s} for s in r["steps"]]}
        if r["yield"]:
            rec["recipeYield"] = r["yield"]
        if r["prep"]:
            rec["prepTime"] = r["prep"]
        if r["cook"]:
            rec["cookTime"] = r["cook"]
        ld.append(rec)
    write(p["path"], page(p["path"], p["title"], p["description"], body, ld=ld, og_type="article", image=im,
                          extra_head=f'<meta property="article:published_time" content="{p["date"]}T08:00:00+08:00">'
                                     f'<meta property="article:modified_time" content="{p["updated"]}T08:00:00+08:00">'
                                     f'<meta property="article:section" content="{esc(cat_name(cat))}">'))


# --------------------------------------------------------------------------- homepage, hubs

def home(posts):
    main = [p for p in posts if p["category"] != "expat-living"]
    feat = sorted(main, key=lambda p: -SCORE.get(p["path"], 0))
    lead, side = feat[0], feat[1:5]
    used = {p["path"] for p in [lead] + side}

    def section(title, url, items, n=4, cls="grid-4"):
        items = [p for p in items if p["path"] not in used][:n]
        used.update(p["path"] for p in items)
        if not items:
            return ""
        return f'<section class="home-sec"><div class="sec-head"><h2><a href="{url}">{title}</a></h2><a class="more" href="{url}">See all →</a></div><div class="grid {cls}">{"".join(card(p, "sm") for p in items)}</div></section>'

    by_place = lambda pl: [p for p in feat if pl in p["places"]]
    by_cat = lambda c: [p for p in feat if p["category"] == c]
    tools = "".join(f'<a class="tool-tile" href="{u}"><span class="tt-ico" aria-hidden="true">{i}</span><b>{n}</b><span>{d}</span></a>' for i, n, d, u in TOOLS)
    body = f'''<section class="home-hero"><div class="wrap">
<h1 class="home-h1">Cebu &amp; Davao news, travel, food and life</h1>
<div class="hero-grid">
  <div class="hero-lead">{card(lead, "lg")}</div>
  <div class="hero-side">{"".join(card(p, "row") for p in side)}</div>
</div></div></section>

<section class="wx-strip"><div class="wrap">
  <div class="wx-strip-head"><h2>Weather now</h2><a href="/weather/">7-day forecasts →</a></div>
  <div class="wx-strip-grid" data-wx-strip="cebu-city,davao-city,lapu-lapu-city,manila,boracay,siargao"></div>
</div></section>

<div class="wrap layout home-layout"><div class="main-col">
{section("Cebu", "/cebu/", by_place("cebu"))}
{section("Davao", "/davao/", by_place("davao"))}
<section class="home-sec news-sec"><div class="sec-head"><h2><a href="/news/">Live news wire</a></h2><a class="more" href="/news/">More →</a></div>
<div class="tabs" data-tabs><div class="tab-btns" role="tablist">
<button role="tab" aria-selected="true" data-tab="cebu">Cebu</button><button role="tab" aria-selected="false" data-tab="davao">Davao</button>
<button role="tab" aria-selected="false" data-tab="ph">Philippines</button><button role="tab" aria-selected="false" data-tab="sports">Sports</button></div>
<div class="news-wire" data-news="cebu" data-news-tabs><ul class="wire-list"><li class="muted">Loading headlines…</li></ul></div></div>
<p class="muted small">Headlines are pulled automatically and link to the original publishers.</p></section>
{section("Travel", cat_url("travel"), by_cat("travel"), 6, "grid-3")}
{section("Food & recipes", cat_url("food"), by_cat("food"), 4)}
<section class="home-sec"><div class="sec-head"><h2><a href="/tools/">Reader tools</a></h2><a class="more" href="/tools/">All tools →</a></div><div class="tool-grid">{tools}</div></section>
{section("Culture & language", cat_url("culture"), by_cat("culture"), 4)}
{section("Sports", cat_url("sports"), by_cat("sports"), 4)}
{section("Entertainment", cat_url("entertainment"), by_cat("entertainment"), 4)}
{section("Money & work", cat_url("money"), by_cat("money"), 4)}
{section("Tech & esports", cat_url("tech"), by_cat("tech"), 4)}
{section("Lifestyle", cat_url("lifestyle"), by_cat("lifestyle"), 4)}
{section("News & explainers", "/news/", by_cat("news"), 4)}
</div>{sidebar(posts)}</div>'''
    desc = "Cebu and Davao news, travel guides, food and recipes, culture, sports and entertainment — plus live weather, a peso converter and a Bisaya dictionary."
    html_ = page("/", "Cebu-Davao: Cebu & Davao News, Travel, Food & Lifestyle", desc, body, full_title=True,
                 ld=[{"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": "Cebu-Davao", "isPartOf": {"@id": ORIGIN + "/#website"},
                      "about": [{"@type": "Place", "name": "Cebu"}, {"@type": "Place", "name": "Davao City"}]}],
                 body_class="is-home")
    write("/home.html", html_)


def place_hubs(posts):
    info = {
        "cebu": ("Cebu Guide: News, Travel, Food & Life in the Queen City of the South",
                 "Cebu Guide: Travel, Food, Culture & News",
                 "Everything Cebu: from Magellan's Cross and Sinulog to lechon, Moalboal's sardine run and the CCLEX bridge — plus live Cebu weather and news.",
                 "cebu-city", "cebu-skyline",
                 [("Province", "Cebu (Central Visayas, Region VII)"), ("Main cities", "Cebu City, Mandaue, Lapu-Lapu"), ("Language", "Cebuano (Bisaya), English, Filipino"),
                  ("Airport", "Mactan-Cebu International (CEB)"), ("Big festival", "Sinulog — third Sunday of January"), ("Famous for", "Lechon, dried mangoes, guitars, diving")]),
        "davao": ("Davao Guide: News, Travel, Food & Life in Davao City",
                  "Davao Guide: Travel, Food, Culture & News",
                  "Everything Davao: Samal Island beaches, Mount Apo, the Philippine eagle, durian and Kadayawan — plus live Davao weather and news.",
                  "davao-city", "davao-city",
                  [("Region", "Davao Region (Region XI), Mindanao"), ("City size", "One of the largest cities by land area in the Philippines"), ("Language", "Cebuano/Davaoeño, Filipino, English"),
                   ("Airport", "Francisco Bangoy International (DVO)"), ("Big festival", "Kadayawan — August"), ("Famous for", "Durian, Mount Apo, Samal, tuna")]),
        "other": ("Around the Philippines: Travel, Food & Culture Beyond Cebu and Davao",
                  "Around the Philippines: Travel, Food & Culture",
                  "Boracay, Siargao, Palawan, Bohol, Camiguin and more — guides, explainers and culture from all over the Philippines.",
                  "manila", "island-hopping", []),
    }
    for key, (h1, title, intro, wx, img) in ((k, v[:5]) for k, v in info.items()):
        url = PLACES[key][1]
        items = [p for p in FEATURED_ORDER if key in p["places"] and p["category"] != "expat-living"]
        facts = info[key][5]
        facts_html = ""
        if facts:
            facts_html = '<dl class="facts">' + "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in facts) + "</dl>"
        extra = f'''<div class="hub-extra">{facts_html}<div class="widget wx-widget" data-wx-card="{wx}"><p class="wx-loading">Loading live weather…</p></div>
{f'<div class="widget news-wire" data-news="{key}"><h3 class="widget-title">Latest {PLACES[key][0]} headlines</h3><ul class="wire-list"><li class="muted">Loading…</li></ul></div>' if key != "other" else ""}</div>'''
        listing_pages(url, h1, esc(intro), items, [("Home", "/"), (PLACES[key][0], url)], intro, hero_extra=extra, active=url, seo_title=title)


def category_pages(posts):
    for slug, (name, desc, color) in CATEGORIES.items():
        items = [p for p in (FEATURED_ORDER if slug != "expat-living" else sorted(posts, key=lambda p: p["date"], reverse=True)) if p["category"] == slug]
        url = cat_url(slug)
        title = f"{name}: Cebu, Davao & Philippines" if slug not in ("expat-living",) else "Living Abroad: Moving, Renting & Travel Guides"
        seo_desc = desc if len(desc) >= 90 else f"{desc} Guides, explainers and the latest stories from Cebu, Davao and across the Philippines."
        listing_pages(url, title, esc(desc), items, [("Home", "/"), (name, url)], seo_desc, active=url)


def blog_index(posts):
    items = sorted(posts, key=lambda p: (p["updated"], SCORE.get(p["path"], 0)), reverse=True)
    listing_pages("/blog/", "All Stories", "Every article on Cebu-Davao, newest first — news explainers, travel guides, recipes, culture and more.",
                  items, [("Home", "/"), ("All stories", "/blog/")], "Every Cebu-Davao article, newest first: news explainers, travel guides, Filipino recipes, culture, sports, money and tech stories.")


def news_hub(posts):
    items = [p for p in FEATURED_ORDER if p["category"] == "news"]
    wires = "".join(f'<section class="wire-col"><h2>{t}</h2><div class="news-wire" data-news="{k}"><ul class="wire-list"><li class="muted">Loading…</li></ul></div></section>'
                    for k, t in (("cebu", "Cebu"), ("davao", "Davao"), ("ph", "Philippines"), ("sports", "Sports")))
    body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html([("Home", "/"), ("News", "/news/")])}
<h1>Cebu &amp; Davao News Today</h1><p class="lede">Live headlines from Cebu, Davao and the rest of the Philippines, refreshed through the day, plus our own explainers and public-service guides.</p></div></section>
<div class="wrap"><div class="wire-grid">{wires}</div>
<p class="muted small">Live headlines are gathered automatically from news publishers through Google News and link to the original stories. Cebu-Davao does not edit them.</p>
<section class="home-sec"><div class="sec-head"><h2>Our explainers &amp; guides</h2></div><div class="grid grid-3">{"".join(card(p) for p in items)}</div></section></div>'''
    ld = [breadcrumb_ld([("Home", "/"), ("News", "/news/")]), {"@type": "CollectionPage", "name": "Cebu & Davao News Today", "url": ORIGIN + "/news/"}]
    write("/news/", page("/news/", "Cebu & Davao News Today: Live Headlines & Explainers",
                         "Cebu news and Davao news today: live headlines from local and national publishers plus Cebu-Davao explainers on typhoons, bridges, IDs and travel rules.",
                         body, ld=ld, active="/news/"))


# --------------------------------------------------------------------------- weather & tools

def weather_pages():
    opts = "".join(f'<option value="{k}">{esc(v[0])}</option>' for k, v in WEATHER_CITIES.items())
    city_links = "".join(f'<li><a href="/weather/{k}/">{esc(v[0])}</a></li>' for k, v in WEATHER_CITIES.items())
    signals = '''<section class="signals"><h2>PAGASA tropical cyclone wind signals at a glance</h2><div class="table-wrap"><table>
<thead><tr><th>Signal</th><th>Winds expected</th><th>What it means for you</th></tr></thead><tbody>
<tr><td><span class="sig s1">1</span></td><td>Strong winds (about 39–61 km/h)</td><td>Minimal to minor threat. Secure loose items; follow class and sea-travel advisories.</td></tr>
<tr><td><span class="sig s2">2</span></td><td>Gale-force winds (about 62–88 km/h)</td><td>Minor to moderate threat. Sea trips usually suspended; prepare go-bags.</td></tr>
<tr><td><span class="sig s3">3</span></td><td>Storm-force winds (about 89–117 km/h)</td><td>Moderate to significant threat. Stay indoors; heed evacuation orders.</td></tr>
<tr><td><span class="sig s4">4</span></td><td>Typhoon-force winds (about 118–184 km/h)</td><td>Significant to severe threat to life and property.</td></tr>
<tr><td><span class="sig s5">5</span></td><td>Typhoon-force winds (185 km/h or higher)</td><td>Extreme threat. Follow local government instructions immediately.</td></tr>
</tbody></table></div><p class="muted small">Summary of PAGASA's wind-signal system. Always follow official bulletins from <a href="https://www.pagasa.dost.gov.ph/" target="_blank" rel="noopener">PAGASA</a> and your LGU. Read our <a href="/news/pagasa-typhoon-signals-explained/">full typhoon signals guide</a>.</p></section>'''
    body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html([("Home", "/"), ("Weather", "/weather/")])}
<h1>Cebu &amp; Davao Weather Forecast</h1><p class="lede">Live conditions, hourly rain chances and 7-day forecasts for Cebu, Davao and popular Philippine destinations. Updated continuously from weather models.</p></div></section>
<div class="wrap"><div class="wx-app" data-wx-app>
<div class="wx-controls"><label for="wx-city">City</label><select id="wx-city" data-wx-select>{opts}</select>
<button class="btn btn-sm btn-ghost" type="button" data-wx-locate>Use my location</button>
<div class="seg" role="group" aria-label="Units"><button type="button" aria-pressed="true" data-unit="c">°C</button><button type="button" aria-pressed="false" data-unit="f">°F</button></div></div>
<div class="wx-full" data-wx-full="cebu-city"><p class="wx-loading">Loading forecast…</p></div>
</div>
<section class="home-sec"><h2>Right now across the Philippines</h2><div class="wx-strip-grid" data-wx-strip="{",".join(WEATHER_CITIES)}"></div></section>
{signals}
<section><h2>Forecasts by city</h2><ul class="link-cols">{city_links}</ul></section>
<p class="muted small">Forecast data: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (CC BY 4.0). For warnings and official forecasts, rely on <a href="https://www.pagasa.dost.gov.ph/" target="_blank" rel="noopener">PAGASA</a>.</p></div>'''
    ld = [breadcrumb_ld([("Home", "/"), ("Weather", "/weather/")]), {"@type": "WebApplication", "name": "Cebu-Davao Weather", "applicationCategory": "WeatherApplication",
          "operatingSystem": "Any", "url": ORIGIN + "/weather/", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PHP"}}]
    write("/weather/", page("/weather/", "Cebu & Davao Weather Forecast: Live, Hourly & 7-Day",
                            "Cebu weather and Davao weather today: live temperature, hourly rain chance and 7-day forecasts for Cebu, Davao, Manila, Boracay, Siargao and more.",
                            body, ld=ld, active="/weather/"))
    for k, (name, lat, lon, region, blurb) in WEATHER_CITIES.items():
        url = f"/weather/{k}/"
        trail = [("Home", "/"), ("Weather", "/weather/"), (name, url)]
        others = "".join(f'<li><a href="/weather/{o}/">{esc(v[0])}</a></li>' for o, v in WEATHER_CITIES.items() if o != k)
        body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html(trail)}
<h1>{esc(name)} Weather Forecast</h1><p class="lede">Live weather in {esc(name)} ({esc(region)}): current temperature, feels-like, humidity, wind, hourly rain chances and the 7-day outlook.</p></div></section>
<div class="wrap"><div class="wx-app" data-wx-app><div class="wx-controls"><div class="seg" role="group" aria-label="Units"><button type="button" aria-pressed="true" data-unit="c">°C</button><button type="button" aria-pressed="false" data-unit="f">°F</button></div></div>
<div class="wx-full" data-wx-full="{k}"><p class="wx-loading">Loading {esc(name)} forecast…</p></div></div>
<section class="prose"><h2>{esc(name)} climate in brief</h2><p>{esc(blurb)}</p>
<p>Planning a trip? See our <a href="/travel/best-time-to-visit-cebu-and-davao/">best time to visit guide</a>, the <a href="/news/pagasa-typhoon-signals-explained/">typhoon signals explainer</a> and the <a href="/tools/packing-checklist/">packing checklist</a>.</p></section>
{signals}
<section><h2>Other forecasts</h2><ul class="link-cols">{others}</ul></section>
<p class="muted small">Forecast data: <a href="https://open-meteo.com/" target="_blank" rel="noopener">Open-Meteo</a> (CC BY 4.0). Official warnings: <a href="https://www.pagasa.dost.gov.ph/" target="_blank" rel="noopener">PAGASA</a>.</p></div>'''
        ld = [breadcrumb_ld(trail), {"@type": "WebPage", "name": f"{name} Weather Forecast", "url": ORIGIN + url,
              "about": {"@type": "Place", "name": name, "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}}}]
        write(url, page(url, f"{name} Weather Forecast: Today, Hourly & 7-Day",
                        f"{name} weather today: live temperature, rain chance by the hour and a 7-day forecast for {name}, {region}, Philippines.",
                        body, ld=ld, active="/weather/"))


TOOLS = [
    ("🌦️", "Weather forecast", "Live, hourly and 7-day for 12 cities", "/weather/"),
    ("₱", "Currency converter", "Peso vs USD, EUR, JPY, KRW, AED…", "/tools/currency-converter/"),
    ("🧮", "Trip budget calculator", "Estimate a Cebu, Davao or island trip", "/tools/trip-budget-calculator/"),
    ("🗣️", "Bisaya dictionary", "Bisaya–Tagalog–English + flashcards", "/tools/bisaya-dictionary/"),
    ("🐟", "Fish name translator", "Lapu-lapu, bangus, malasugi in English", "/tools/fish-names/"),
    ("🎉", "Festival calendar", "Countdowns to Sinulog, Kadayawan & more", "/tools/festival-calendar/"),
    ("📏", "City distance calculator", "Kilometres and travel time between cities", "/travel/mileage-from-to-distance-between-cities/"),
    ("🧳", "Packing checklist", "Tick-off list for beach, city or typhoon season", "/tools/packing-checklist/"),
    ("❓", "Destination quiz", "How well do you know the Philippines?", "/fun-quizzes/name-these-philippine-travel-destinations/"),
    ("📰", "Live news wire", "Cebu, Davao, national and sports headlines", "/news/"),
]


def tool_pages():
    fish = json.load(open(os.path.join(ROOT, "assets", "data", "fish.json"), encoding="utf-8"))
    bis = json.load(open(os.path.join(ROOT, "assets", "data", "bisaya.json"), encoding="utf-8"))
    defs = {
        "currency-converter": ("Peso Currency Converter: PHP to USD, EUR, JPY & More",
            "Convert Philippine pesos to US dollars, euros, yen, won, dirhams and more with live daily rates — handy for OFW remittances, travel and shopping.",
            "Peso Currency Converter", "Live daily exchange rates between the Philippine peso and 15 major currencies — useful for remittances, travel budgets and online shopping.",
            '<div class="tool" data-tool="currency"></div>',
            "<h2>How to use the converter</h2><p>Type an amount, choose the two currencies and the result updates instantly. Use the swap button to flip directions. Rates are mid-market reference rates refreshed daily; banks, remittance centres and card networks add their own spread or fees, so the amount you actually receive will usually be a little lower.</p><h2>Tips for better peso rates</h2><ul><li>Compare the total cost (fee + rate) of remittance apps, banks and money changers.</li><li>Money changers in malls often beat airport counters.</li><li>Pay in pesos when a card terminal offers to charge you in your home currency (dynamic currency conversion is usually more expensive).</li></ul>"),
        "trip-budget-calculator": ("Philippines Trip Budget Calculator: Cebu, Davao & Islands",
            "Estimate the cost of a trip to Cebu, Davao, Boracay, Siargao, Bohol or El Nido by days, travellers and travel style — in pesos and your currency.",
            "Trip Budget Calculator", "Plan your Cebu, Davao or island-hopping budget in seconds. Adjust days, group size, travel style and activities.",
            '<div class="tool" data-tool="budget"></div>',
            "<h2>How the estimate works</h2><p>The calculator multiplies typical daily costs for accommodation, food and local transport by the number of days and travellers, adjusts for the destination, then adds the activities you tick. Figures are rough 2026 planning ranges gathered from typical published rates — not quotes — and do not include international or domestic flights. Peak seasons (Christmas, Holy Week, Sinulog, summer) can push room rates much higher.</p>"),
        "bisaya-dictionary": ("Bisaya Dictionary: Cebuano to Tagalog & English Phrases",
            "Searchable Bisaya (Cebuano) to Tagalog and English dictionary with 150+ everyday words and phrases, false friends and a flashcard trainer.",
            "Bisaya–Tagalog–English Dictionary", "Search everyday Cebuano (Bisaya) words and phrases with their Tagalog and English meanings, then test yourself with flashcards.",
            '<div class="tool" data-tool="bisaya"></div>',
            "<h2>Why Bisaya and Tagalog trip people up</h2><p>Cebuano and Tagalog share many words, but some look identical and mean different things. <em>Libog</em> means confused in Cebuano but lust in Tagalog; <em>bukid</em> is a mountain in Cebuano but a farm in Tagalog. When in doubt, ask — Cebuanos and Davaoeños are usually delighted when visitors try.</p><p>Learn more in our <a href=\"/culture/learn-bisaya-50-phrases/\">50 essential Bisaya phrases</a> guide and <a href=\"/culture/the-trouble-with-filipino-tongues/\">languages of Cebu and Davao</a>.</p>"),
        "fish-names": ("Fish Names in Bisaya, Tagalog & English: Translator",
            "What is lapu-lapu, bangus or malasugi in English? Search 40 Philippine fish and seafood names in Bisaya, Tagalog and English.",
            "Fish Name Translator", "Find the English name of Philippine fish and seafood — and the Bisaya or Tagalog name of the fish you know.",
            '<div class="tool" data-tool="fish"></div>',
            "<h2>Why the same fish has many names</h2><p>Fish names change from island to island — even between towns. Market vendors in Cebu, Davao and Manila may use different words for the same catch, and the same word can mean different fish elsewhere. Use the table as a starting point and ask the vendor. Read more in <a href=\"/culture/cebus-and-davaos-different-fish/\">Cebu's and Davao's different fish</a>.</p>"),
        "festival-calendar": ("Philippine Festival Calendar 2026–2027 with Countdowns",
            "Countdown to Sinulog, Dinagyang, Ati-Atihan, Kadayawan, MassKara, Chinese New Year and other Philippine festivals, with dates and add-to-calendar.",
            "Philippine Festival Calendar", "Live countdowns to the biggest fiestas and holidays in Cebu, Davao and the Philippines. Add any event to your calendar.",
            '<div class="tool" data-tool="festivals"></div>',
            "<h2>About the dates</h2><p>Many Philippine festivals follow a rule (for example, Sinulog on the third Sunday of January) rather than a fixed date, and organisers sometimes shift events. Dates marked “approx.” are estimates — confirm with the organisers or local tourism office before booking.</p><p>Read our guides to <a href=\"/festivals/what-makes-the-sinulog-2012-festival-the-number-one-festival-in-the-philippines/\">Sinulog</a>, <a href=\"/festivals/whats-so-interesting-about-the-kadayawan-festival/\">Kadayawan</a> and <a href=\"/events/kung-hei-fat-choy/\">Chinese New Year</a>.</p>"),
        "packing-checklist": ("Philippines Packing Checklist: Beach, City & Typhoon Season",
            "Interactive packing checklist for a Philippines trip — beach, city, mountain and rainy-season essentials. Ticks are saved on your device; print it.",
            "Philippines Packing Checklist", "Tick off what you've packed for Cebu, Davao or the islands. Your ticks are saved in this browser.",
            '<div class="tool" data-tool="packing"></div>',
            "<h2>Packing tips for the tropics</h2><ul><li>Light, quick-dry clothes beat cotton in the humidity.</li><li>Churches and shrines such as Simala expect covered shoulders and knees.</li><li>Keep a power bank under the airline limit in your hand-carry, not checked bags.</li><li>During typhoon season keep a waterproof pouch for your phone and documents.</li></ul>"),
    }
    for slug, (title, desc, h1, lede, tool, after) in defs.items():
        url = f"/tools/{slug}/"
        trail = [("Home", "/"), ("Tools", "/tools/"), (h1, url)]
        static = ""
        if slug == "fish-names":
            static = '<div class="table-wrap static-table" data-static-for="fish"><table><thead><tr><th>Bisaya / Cebuano</th><th>Tagalog</th><th>English</th><th>Notes</th></tr></thead><tbody>' + "".join(
                f"<tr><td>{esc(f['b'])}</td><td>{esc(f['t'])}</td><td>{esc(f['e'])}</td><td>{esc(f['n'])}</td></tr>" for f in fish) + "</tbody></table></div>"
        if slug == "bisaya-dictionary":
            static = '<div class="table-wrap static-table" data-static-for="bisaya"><table><thead><tr><th>Bisaya</th><th>Tagalog</th><th>English</th></tr></thead><tbody>' + "".join(
                f"<tr><td>{esc(b['b'])}</td><td>{esc(b['t'])}</td><td>{esc(b['e'])}</td></tr>" for b in bis) + "</tbody></table></div>"
        body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html(trail)}<h1>{esc(h1)}</h1><p class="lede">{esc(lede)}</p></div></section>
<div class="wrap layout"><div class="main-col">{tool}{static}<div class="prose">{after}</div></div>{sidebar([], None)}</div>'''
        ld = [breadcrumb_ld(trail), {"@type": "WebApplication", "name": h1, "url": ORIGIN + url, "applicationCategory": "UtilitiesApplication",
              "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PHP"}, "description": desc}]
        write(url, page(url, title, desc, body, ld=ld, active="/tools/"))
    tiles = "".join(f'<a class="tool-tile" href="{u}"><span class="tt-ico" aria-hidden="true">{i}</span><b>{n}</b><span>{d}</span></a>' for i, n, d, u in TOOLS)
    body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html([("Home", "/"), ("Tools", "/tools/")])}<h1>Free Tools for Cebu, Davao &amp; Philippines Travel</h1>
<p class="lede">Weather, money, language and planning tools built for readers in Cebu, Davao and everywhere in between. Free, no sign-up.</p></div></section>
<div class="wrap"><div class="tool-grid tool-grid-lg">{tiles}</div></div>'''
    write("/tools/", page("/tools/", "Free Philippines Travel Tools: Weather, Peso, Bisaya & More",
                          "Free reader tools: live weather, peso converter, trip budget calculator, Bisaya dictionary, fish names, festival countdowns and a packing checklist.",
                          body, ld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/")])], active="/tools/"))


def search_page(posts):
    body = f'''<section class="page-hero"><div class="wrap">{breadcrumbs_html([("Home", "/"), ("Search", "/search/")])}<h1>Search Cebu-Davao</h1>
<form class="search-page-form" action="/search/" role="search"><label class="sr" for="sq">Search</label><input id="sq" type="search" name="q" placeholder="Try: lechon, Samal ferry, typhoon signal" data-search-page></form></div></section>
<div class="wrap"><ul class="search-results search-results-page" data-search-results-page></ul></div>'''
    write("/search/", page("/search/", "Search", "Search every Cebu-Davao article, travel guide, Filipino recipe, explainer and reader tool by keyword.", body, robots="noindex, follow"))
    idx = [{"t": p["title"], "u": p["path"], "c": cat_name(p["category"]), "e": p["excerpt"][:140], "k": p["keyword"]} for p in posts]
    idx += [{"t": n, "u": u, "c": "Tool", "e": d, "k": ""} for _i, n, d, u in TOOLS]
    idx += [{"t": f"{v[0]} weather forecast", "u": f"/weather/{k}/", "c": "Weather", "e": f"Live and 7-day forecast for {v[0]}", "k": "weather"} for k, v in WEATHER_CITIES.items()]
    os.makedirs(os.path.join(OUT, "assets", "data"), exist_ok=True)
    json.dump(idx, open(os.path.join(OUT, "assets", "data", "search.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))


# --------------------------------------------------------------------------- feeds, sitemaps, redirects

def rfc822(iso):
    return format_datetime(datetime.fromisoformat(iso[:10]).replace(hour=8, tzinfo=timezone.utc))


def feeds(posts):
    items = sorted([p for p in posts if p["category"] != "expat-living"], key=lambda p: (p["updated"], SCORE.get(p["path"], 0)), reverse=True)[:40]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', "<channel>",
           f"<title>{SITE['name']}</title>", f"<link>{ORIGIN}/</link>", f"<description>{esc(SITE['tagline'])}</description>",
           "<language>en-ph</language>", f'<atom:link href="{ORIGIN}/feed/" rel="self" type="application/rss+xml"/>']
    for p in items:
        xml.append(f"<item><title>{esc(p['title'])}</title><link>{ORIGIN}{p['path']}</link><guid>{ORIGIN}{p['path']}</guid>"
                   f"<pubDate>{rfc822(p['updated'])}</pubDate><category>{esc(cat_name(p['category']))}</category><description>{esc(p['excerpt'])}</description></item>")
    xml += ["</channel>", "</rss>"]
    write("/feed.xml", "\n".join(xml))


def sitemaps(posts, extra_pages):
    def urlset(entries, images=False):
        ns = ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"' if images else ""
        out = ['<?xml version="1.0" encoding="UTF-8"?>', f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"{ns}>']
        for loc, lastmod, img in entries:
            im = f"<image:image><image:loc>{ORIGIN}{img}</image:loc></image:image>" if img else ""
            out.append(f"<url><loc>{ORIGIN}{loc}</loc><lastmod>{lastmod}</lastmod>{im}</url>")
        out.append("</urlset>")
        return "\n".join(out)
    post_entries = [(p["path"], p["updated"], (image_for(p) or {}).get("src")) for p in posts]
    write("/sitemap-posts.xml", urlset(post_entries, images=True))
    write("/sitemap-pages.xml", urlset([(u, TODAY, None) for u in extra_pages]))
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<sitemap><loc>{ORIGIN}/{s}</loc><lastmod>{TODAY}</lastmod></sitemap>\n" for s in ("sitemap-posts.xml", "sitemap-pages.xml"))
          + "</sitemapindex>")
    write("/robots.txt", f"User-agent: *\nDisallow: /api/\nDisallow: /search/\nDisallow: /home.html\n\nSitemap: {ORIGIN}/sitemap.xml\n")


def legacy_urls():
    import csv
    src = os.path.join(ROOT, "data", "legacy-urls.txt")
    return [l.strip() for l in open(src, encoding="utf-8") if l.strip()]


def redirect_map(live_paths):
    live = set(live_paths)
    rmap = {}
    for path in legacy_urls():
        if path in live or path == "/":
            continue
        target = redirects.SPECIFIC.get(path, "/")
        seg = path.strip("/").split("/")
        if path not in redirects.SPECIFIC and seg and seg[0] == "category" and len(seg) >= 2:
            target = redirects.CATEGORY.get(seg[1], "/") or "/"
        if target is None:
            continue
        rmap[path] = target
    for k, v in redirects.SPECIFIC.items():
        if v and k not in live:
            rmap.setdefault(k, v)
    # resolve chains and verify targets exist
    for k, v in list(rmap.items()):
        seen = 0
        while v in rmap and seen < 5:
            v = rmap[v]; seen += 1
        if v != "/" and v not in live:
            raise SystemExit(f"redirect target missing: {k} -> {v}")
        rmap[k] = v
    return rmap


def write_php(rmap, live_paths):
    lines = ["<?php", "// Generated by build.py — legacy URL 301 map (old path => new path).", "return ["]
    for k in sorted(rmap):
        lines.append(f"  {json.dumps(k)} => {json.dumps(rmap[k])},")
    lines.append("];")
    write("/redirects.php", "\n".join(lines) + "\n")
    hubs = {k: v for k, v in redirects.SECTION_HUB.items()}
    write("/sections.php", "<?php\n// Generated: bare legacy section paths => hub.\nreturn " + "[" + ",".join(f"{json.dumps(k)}=>{json.dumps(v)}" for k, v in hubs.items()) + "];\n")
    for name in ("index.php", "api/news.php", "api/contact.php", "api/subscribe.php", "api/lib.php"):
        src = os.path.join(ROOT, "php", name)
        dst = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
    # intermediate directories of post paths that have no page of their own -> PHP 301 to the hub
    dirs = set()
    for pth in live_paths:
        parts = pth.strip("/").split("/")
        for i in range(1, len(parts)):
            dirs.add("/" + "/".join(parts[:i]) + "/")
    for d in sorted(dirs):
        if d in live_paths:
            continue
        seg = d.strip("/").split("/")[0]
        target = redirects.SECTION_HUB.get(seg, "/")
        if d.count("/") > 2:
            target = redirects.SECTION_HUB.get(seg, "/")
        write(d + "index.php", f"<?php\nheader('Location: {ORIGIN}{target}', true, 301);\nexit;\n")


# --------------------------------------------------------------------------- main

SCORE, POPULAR, FEATURED_ORDER = {}, [], []


def compute_scores(posts):
    """Rank posts for the homepage: legacy search demand first, then new trending posts."""
    vol = {}
    src = os.path.join(ROOT, "data", "legacy-volume.json")
    if os.path.exists(src):
        vol = json.load(open(src))
    new_paths = [p for p, *_ in plan.NEW]
    for p in posts:
        s = vol.get(p["path"], 0)
        if p["path"] in new_paths:
            s += 3000 - new_paths.index(p["path"]) * 40
        if p["category"] == "expat-living":
            s = -1
        SCORE[p["path"]] = s
    ranked = sorted(posts, key=lambda p: -SCORE[p["path"]])
    POPULAR[:] = [p for p in sorted(posts, key=lambda p: -vol.get(p["path"], 0)) if p["category"] != "expat-living"][:8]
    FEATURED_ORDER[:] = ranked


def copy_static():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    shutil.copytree(os.path.join(ROOT, "wp-content"), os.path.join(OUT, "wp-content"))
    for f in os.listdir(os.path.join(ROOT, "static")):
        s = os.path.join(ROOT, "static", f)
        (shutil.copytree if os.path.isdir(s) else shutil.copy)(s, os.path.join(OUT, f))


def main():
    md_posts = load_md_posts()
    wp_posts = load_wp_posts()
    posts = md_posts + wp_posts
    paths = [p["path"] for p in posts]
    dup = {x for x in paths if paths.count(x) > 1}
    if dup:
        raise SystemExit(f"duplicate paths: {dup}")
    missing = [p for p, *_ in plan.LEGACY + [(n[0],) for n in plan.NEW] if p not in paths]
    if missing:
        print(f"WARNING: {len(missing)} planned posts not written yet:", *missing[:10], sep="\n  ")
    compute_scores(posts)
    copy_static()
    for p in posts:
        post_page(p, posts)
    home(posts)
    category_pages(posts)
    place_hubs(posts)
    blog_index(posts)
    news_hub(posts)
    weather_pages()
    tool_pages()
    search_page(posts)
    extra = static_pages.build(page, write, breadcrumbs_html, breadcrumb_ld, posts, PHOTOS, CATEGORIES, cat_url, esc)
    hub_pages = (["/news/", "/weather/", "/tools/", "/blog/", "/cebu/", "/davao/", "/philippines/"]
                 + [cat_url(c) for c in CATEGORIES] + [f"/weather/{k}/" for k in WEATHER_CITIES]
                 + [f"/tools/{t}/" for t in ("currency-converter", "trip-budget-calculator", "bisaya-dictionary", "fish-names", "festival-calendar", "packing-checklist")]
                 + extra)
    feeds(posts)
    sitemaps(posts, ["/"] + hub_pages)
    live = set(paths) | set(hub_pages) | {"/", "/search/", "/feed/"}
    rmap = redirect_map(live)
    write_php(rmap, live)
    print(f"built {len(posts)} posts ({len(md_posts)} new/recreated, {len(wp_posts)} kept from WordPress), "
          f"{len(hub_pages)} hub/static pages, {len(rmap)} redirects -> {os.path.relpath(OUT, ROOT)}/")


if __name__ == "__main__":
    main()
