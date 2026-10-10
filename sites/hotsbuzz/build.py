#!/usr/bin/env python3
"""Static site generator for the hotsbuzz.com rebuild.

    python3 build.py && python3 validate.py

Writes the deployable site into ./public (committed). Standard library only.
"""

import hashlib
import html
import importlib
import json
import pkgutil
import random
import re
import shutil
from pathlib import Path

import content
from motifs import motif
from siteconfig import CAT, CATEGORIES, HOLIDAYS, SITE, STAGING, TODAY

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
ORIGIN = SITE["origin"]
ASSET_V = ""  # filled in main() with a content hash for cache busting


# ---------------------------------------------------------------- content ---

def load_posts():
    posts = []
    for mod in sorted(m.name for m in pkgutil.iter_modules(content.__path__)):
        if mod.startswith("posts_"):
            posts += importlib.import_module(f"content.{mod}").POSTS
    slugs = [p["slug"] for p in posts]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        raise SystemExit(f"duplicate slugs: {dupes}")
    for p in posts:
        if p["category"] not in CAT:
            raise SystemExit(f"{p['slug']}: unknown category {p['category']}")
        p["url"] = f"/{p['slug']}/"
        p["minutes"] = parse_minutes(p["time"])
        p["words"] = len(re.sub(r"<[^>]+>", " ", json.dumps(
            [p["intro"], p["steps"], p["tips"], p["variations"], p["faq"]])).split())
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def parse_minutes(text):
    """Hands-on minutes from a free-text time ("1.5-2 hours plus drying" -> 120)."""
    active = re.split(r"\bplus\b|,|\bthen\b", text.lower())[0]
    if "half a day" in active:
        return 240
    pairs = re.findall(r"(\d+(?:\.\d+)?)\s*(hours?|hrs?|minutes?|mins?|days?)?", active)
    pairs = [(float(n), u) for n, u in pairs]
    if not pairs:
        return 60
    n, unit = next((x for x in reversed(pairs) if x[1]), pairs[-1])
    unit = unit or "min"
    return int(n * (60 if unit.startswith("h") else 1440 if unit.startswith("d") else 1))


def time_bucket(mins):
    return "quick" if mins <= 60 else "afternoon" if mins <= 180 else "weekend"


# ------------------------------------------------------------------ helpers ---

def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def asset(path):
    return f"{path}?v={ASSET_V}"


PHOTOS = json.loads((ROOT / "photos.json").read_text(encoding="utf-8")) if (ROOT / "photos.json").exists() else {}


def has_photo(key):
    return key in PHOTOS and (ROOT / "assets" / "photos" / f"{key}-1600.webp").exists()


def img(key, alt, sizes="(max-width: 760px) 100vw, 33vw", loading="lazy", priority=False, cls=""):
    """Responsive photo for `key` (post slug, cat-<slug> or home); falls back to the SVG cover."""
    c = f' class="{cls}"' if cls else ""
    load = ' fetchpriority="high"' if priority else f' loading="{loading}"'
    if has_photo(key):
        return (f'<img{c} src="/assets/photos/{key}-1600.webp" srcset="/assets/photos/{key}-800.webp 800w, '
                f'/assets/photos/{key}-1600.webp 1600w" sizes="{sizes}" alt="{esc(alt)}" width="1600" height="1000"{load} decoding="async">')
    return f'<img{c} src="/assets/covers/{key}.svg" alt="{esc(alt)}" width="1200" height="750"{load} decoding="async">'


def photo_alt(key, fallback):
    return PHOTOS.get(key, {}).get("alt") or fallback


# --------------------------------------------------------------- cover art ---

def cover_svg(seed, cat, motif_name, w=1200, h=750, big=True):
    """Deterministic cut-paper cover: gradient, confetti, dotted grid, motif."""
    rnd = random.Random(hashlib.md5(seed.encode()).hexdigest())
    c1, c2, acc = cat["c1"], cat["c2"], cat["accent"]
    uid = re.sub(r"[^a-z0-9]", "", seed.lower())[:12] or "c"
    shapes = []
    for _ in range(26):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(6, 22)
        rot = rnd.uniform(0, 360)
        col = rnd.choice([acc, "#ffffff", acc, "#ffffff", c1])
        op = rnd.uniform(.25, .7)
        kind = rnd.random()
        if kind < .35:
            shapes.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * .6:.1f}" fill="{col}" opacity="{op:.2f}"/>')
        elif kind < .7:
            shapes.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r * 1.8:.0f}" height="{r * .7:.0f}" rx="3" fill="{col}" opacity="{op:.2f}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>')
        else:
            shapes.append(f'<path d="M{x:.0f} {y:.0f}l{r:.0f} {r * 1.7:.0f}h-{r * 2:.0f}z" fill="{col}" opacity="{op:.2f}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>')
    blob_r = h * .46
    cx, cy = (w * .62, h * .52) if big else (w * .5, h * .5)
    scale = (h * .62) / 100
    tilt = rnd.uniform(-12, 12)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<pattern id="d{uid}" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#fff" opacity=".18"/></pattern>
<filter id="s{uid}" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".28"/></filter></defs>
<rect width="{w}" height="{h}" fill="url(#g{uid})"/><rect width="{w}" height="{h}" fill="url(#d{uid})"/>
<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{blob_r:.0f}" fill="#fff" opacity=".12"/><circle cx="{cx - blob_r * .9:.0f}" cy="{cy + blob_r * .7:.0f}" r="{blob_r * .5:.0f}" fill="{acc}" opacity=".22"/>
{"".join(shapes)}
<g filter="url(#s{uid})" transform="translate({cx - 50 * scale:.0f} {cy - 50 * scale:.0f}) rotate({tilt:.1f} {50 * scale:.0f} {50 * scale:.0f}) scale({scale:.3f})" color="#fff" fill="#fff">{motif(motif_name, acc)}</g>
</svg>'''


# ------------------------------------------------------------------ layout ---

NAV = [(c["short"], f"/category/{c['slug']}/") for c in CATEGORIES if c["slug"] not in HOLIDAYS]


def head(title, desc, path, og_type="website", image=None, jsonld=None, extra=""):
    url = ORIGIN + path
    og_img = ORIGIN + (image or "/assets/og/home.jpg")
    robots = "noindex, nofollow" if STAGING else "index, follow, max-image-preview:large"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fff8ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16121f" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{SITE['name']}" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,500..900,100&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Caveat:wght@600;700&display=swap">
<link rel="stylesheet" href="{asset('/assets/css/site.css')}">
<script>try{{var t=localStorage.getItem('hb-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{extra}{ld}
</head>
'''


LOGO = '''<a class="logo" href="/" aria-label="HotsBuzz home"><span class="logo__mark" aria-hidden="true"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="var(--coral)"/><path d="M21 7l-9 15h7l-2 11 10-16h-7z" fill="#fff"/></svg></span><span class="logo__word">Hots<b>Buzz</b></span></a>'''


def header(active=""):
    links = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a></li>'
        for label, href in NAV)
    hol = "".join(
        f'<li><a href="/category/{s}/"><span class="dot" style="--c:{CAT[s]["c1"]}"></span>{CAT[s]["short"]}</a></li>'
        for s in HOLIDAYS)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header">
  <div class="wrap site-header__in">
    {LOGO}
    <nav class="nav" aria-label="Main">
      <ul class="nav__list">
        {links}
        <li class="nav__drop"><button class="nav__dropbtn" aria-expanded="false" aria-controls="holidays">Holidays <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></button>
          <ul class="nav__menu" id="holidays">{hol}</ul></li>
        <li><a href="/projects/"{' aria-current="page"' if active == '/projects/' else ''}>All Projects</a></li>
        <li><a href="/about/"{' aria-current="page"' if active == '/about/' else ''}>About</a></li>
      </ul>
    </nav>
    <div class="site-header__tools">
      <a class="icon-btn" href="/projects/#search" aria-label="Search projects"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></a>
      <button class="icon-btn theme-toggle" aria-label="Toggle dark mode"><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></g></svg><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 019.5 4a8.5 8.5 0 1010.5 10.5z" fill="currentColor"/></svg></button>
      <button class="icon-btn nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
'''


def footer():
    cats = "".join(f'<li><a href="/category/{c["slug"]}/">{c["name"]}</a></li>' for c in CATEGORIES)
    return f'''</main>
<footer class="site-footer">
  <div class="site-footer__wave" aria-hidden="true"><svg viewBox="0 0 1440 80" preserveAspectRatio="none"><path d="M0 40c120-30 240-30 360 0s240 30 360 0 240-30 360 0 240 30 360 0v40H0z" fill="currentColor"/></svg></div>
  <div class="wrap site-footer__grid">
    <div class="site-footer__brand">
      {LOGO}
      <p>{SITE['about']}</p>
    </div>
    <div><h2 class="site-footer__h">Categories</h2><ul>{cats}</ul></div>
    <div><h2 class="site-footer__h">HotsBuzz</h2><ul>
      <li><a href="/projects/">All projects</a></li>
      <li><a href="/about/">About us</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a href="/privacy-policy/">Privacy policy</a></li>
      <li><a href="/image-credits/">Image credits</a></li>
      <li><a href="/feed.xml">RSS feed</a></li>
    </ul></div>
  </div>
  <div class="wrap site-footer__base"><p>© {TODAY[:4]} {SITE['name']} · Make it. Gift it. Love it.</p><a class="to-top" href="#main">Back to top ↑</a></div>
</footer>
<script src="{asset('/assets/js/site.js')}" defer></script>
</body>
</html>
'''


def breadcrumbs(items):
    """items: [(name, path)], last one is the current page."""
    li = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            li.append(f'<li aria-current="page">{name}</li>')
        else:
            li.append(f'<li><a href="{path}">{name}</a></li>')
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": strip_tags(n), "item": ORIGIN + p}
        for i, (n, p) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(li)}</ol></nav>', ld


ORG = {
    "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE["name"], "url": ORIGIN + "/",
    "logo": {"@type": "ImageObject", "url": ORIGIN + "/web-app-manifest-512x512.png"},
    "email": SITE["email"],
}


# ------------------------------------------------------------------- cards ---

def chip_level(level):
    dots = {"Easy": 1, "Moderate": 2, "Advanced": 3}.get(level, 1)
    return f'<span class="lvl lvl--{dots}" title="{level}"><i></i><i></i><i></i>{level}</span>'


def card(p, eager=False, size=""):
    c = CAT[p["category"]]
    loading = "eager" if eager else "lazy"
    return f'''<article class="card {size} reveal" data-tilt style="--c1:{c['c1']};--c2:{c['c2']};--acc:{c['accent']}"
  data-cat="{p['category']}" data-level="{p['difficulty'].lower()}" data-time="{time_bucket(p['minutes'])}" data-search="{esc((p['title'] + ' ' + p['keyword'] + ' ' + p['excerpt'] + ' ' + c['name']).lower())}">
  <a class="card__link" href="{p['url']}">
    <div class="card__media"><span class="tape" aria-hidden="true"></span>{img(p['slug'], photo_alt(p['slug'], strip_tags(p['title'])), loading=loading)}</div>
    <div class="card__body">
      <span class="pill" style="--pc:{c['c1']}">{c['short']}</span>
      <h3 class="card__title">{p['title']}</h3>
      <p class="card__ex">{p['excerpt']}</p>
      <div class="card__meta">{chip_level(p['difficulty'])}<span class="meta-time">⏱ {p['time']}</span></div>
    </div>
  </a>
</article>'''


# ------------------------------------------------------------------- pages ---

def page_home(posts):
    feat = posts[0]
    fc = CAT[feat["category"]]
    counts = {c["slug"]: sum(1 for p in posts if p["category"] == c["slug"]) for c in CATEGORIES}
    tiles = "".join(f'''<a class="tile reveal" href="/category/{c['slug']}/" style="--c1:{c['c1']};--c2:{c['c2']};--acc:{c['accent']};--d:{i * 60}ms" data-tilt>
  {img("cat-" + c["slug"], "", sizes="(max-width: 600px) 100vw, 25vw", cls="tile__photo") if has_photo("cat-" + c["slug"]) else ""}
  <span class="tile__art" aria-hidden="true"><svg viewBox="0 0 100 100" color="#fff" fill="#fff">{motif(c['motif'], c['accent'])}</svg></span>
  <span class="tile__name">{c['name']}</span><span class="tile__count">{counts[c['slug']]} projects</span>
</a>''' for i, c in enumerate(CATEGORIES))
    latest = "".join(card(p, eager=i < 3) for i, p in enumerate(posts[1:7]))
    marquee_items = "".join(f'<span><svg viewBox="0 0 100 100" color="currentColor" fill="currentColor" aria-hidden="true">{motif(c["motif"], "var(--paper)")}</svg>{c["name"]}</span>' for c in CATEGORIES)
    floaters = []
    rnd = random.Random(7)
    spots = [(6, 18), (88, 12), (78, 70), (14, 74), (50, 6), (94, 44), (34, 88), (64, 92)]
    names = ["heart", "star", "leaf", "flower", "pumpkin", "snowflake", "shamrock", "yarn"]
    cols = ["var(--coral)", "var(--sun)", "var(--teal)", "var(--plum)", "var(--coral)", "var(--teal)", "var(--leaf)", "var(--plum)"]
    for (x, y), n, col in zip(spots, names, cols):
        floaters.append(f'<span class="floater" style="left:{x}%;top:{y}%;--r:{rnd.randint(-25, 25)}deg;--s:{rnd.uniform(.7, 1.15):.2f};--dur:{rnd.uniform(7, 12):.1f}s;color:{col}" data-depth="{rnd.uniform(.4, 1.6):.2f}"><svg viewBox="0 0 100 100" fill="currentColor" color="currentColor">{motif(n, "var(--paper)")}</svg></span>')
    holiday_season = [
        ("Jan–Feb", "valentines-crafts"), ("March", "st-patricks-day-crafts"),
        ("Sept–Oct", "halloween-crafts"), ("November", "thanksgiving-crafts"), ("December", "christmas-crafts"),
    ]
    season_btns = "".join(f'<button class="season__btn" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-season="{s}" style="--c1:{CAT[s]["c1"]}">{m}</button>' for i, (m, s) in enumerate(holiday_season))
    season_panels = ""
    for i, (m, s) in enumerate(holiday_season):
        c = CAT[s]
        items = [p for p in posts if p["category"] == s][:3]
        lis = "".join(f'<li><a href="{p["url"]}">{img(p["slug"], "", sizes="(max-width: 860px) 120px, 22vw")}<span>{p["title"]}</span></a></li>' for p in items)
        season_panels += f'''<div class="season__panel" role="tabpanel" data-panel="{s}"{"" if i == 0 else " hidden"} style="--c1:{c['c1']};--c2:{c['c2']};--acc:{c['accent']}">
  <div class="season__intro"><h3>{c['name']}</h3><p>{c['blurb']}</p><a class="btn btn--light" href="/category/{s}/">See all {c['short']} crafts</a></div>
  <ul class="season__list">{lis}</ul></div>'''
    desc = ("HotsBuzz is your home for DIY projects, DIY ideas and crafts: step-by-step home decor makeovers, "
            "handmade gifts and holiday crafts for every season.")
    title = "HotsBuzz | DIY Projects, DIY Ideas, Crafts & More"
    ld = [{"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": ORIGIN + "/#site", "name": SITE["name"], "url": ORIGIN + "/",
         "description": desc, "publisher": {"@id": ORIGIN + "/#org"},
         "potentialAction": {"@type": "SearchAction", "target": ORIGIN + "/projects/?q={search_term_string}",
                             "query-input": "required name=search_term_string"}},
        ORG,
        {"@type": "ItemList", "name": "Latest DIY projects", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["url"], "name": strip_tags(p["title"])}
            for i, p in enumerate(posts[:7])]},
    ]}]
    out = head(title, desc, "/", jsonld=ld) + header("/") + f'''
<section class="hero">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="blob blob--3"></span></div>
  <div class="hero__floaters" aria-hidden="true">{"".join(floaters)}</div>
  <div class="wrap hero__in">
    <p class="kicker reveal">DIY projects · DIY ideas · crafts &amp; more</p>
    <h1 class="hero__title reveal">DIY projects &amp; crafts to <span class="rotator" data-words="make|gift|love|share"><span class="rotator__word">make</span></span> <span class="hl">with your own two hands.</span></h1>
    <p class="hero__lede reveal">HotsBuzz gathers easy DIY ideas, home decor makeovers and holiday crafts with clear materials lists, honest timing and step-by-step instructions, so every project turns out like a little masterpiece.</p>
    <div class="hero__cta reveal">
      <a class="btn btn--primary" href="/projects/" data-confetti>Browse {len(posts)} projects</a>
      <a class="btn btn--ghost" href="#picker">Help me pick a craft</a>
    </div>
    <ul class="hero__stats reveal" aria-label="At a glance">
      <li><b data-count="{len(posts)}">{len(posts)}</b><span>step-by-step projects</span></li>
      <li><b data-count="{len(CATEGORIES)}">{len(CATEGORIES)}</b><span>craft categories</span></li>
      <li><b data-count="{sum(1 for p in posts if p['difficulty'] == 'Easy')}">{sum(1 for p in posts if p['difficulty'] == 'Easy')}</b><span>beginner-friendly</span></li>
    </ul>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee_items}{marquee_items}</div></div>

<section class="section wrap">
  <a class="feature reveal" href="{feat['url']}" style="--c1:{fc['c1']};--c2:{fc['c2']};--acc:{fc['accent']}" data-tilt>
    <div class="feature__media">{img(feat['slug'], photo_alt(feat['slug'], strip_tags(feat['title'])), sizes="(max-width: 860px) 100vw, 55vw")}</div>
    <div class="feature__body">
      <span class="feature__flag">Fresh on HotsBuzz</span>
      <h2>{feat['title']}</h2>
      <p>{feat['excerpt']}</p>
      <div class="card__meta">{chip_level(feat['difficulty'])}<span class="meta-time">⏱ {feat['time']}</span><span class="meta-time">💸 {feat['cost']}</span></div>
      <span class="btn btn--light">Start this project →</span>
    </div>
  </a>
</section>

<section class="section wrap" aria-labelledby="cats-h">
  <div class="section__head"><h2 id="cats-h" class="h-script-under">Pick your craft corner</h2><p>Seven categories, from everyday home decor to every holiday on the calendar.</p></div>
  <div class="tiles">{tiles}</div>
</section>

<section class="section wrap" aria-labelledby="latest-h">
  <div class="section__head"><h2 id="latest-h" class="h-script-under">Latest DIY ideas</h2><a class="link-arrow" href="/projects/">See every project →</a></div>
  <div class="grid">{latest}</div>
</section>

<section class="section picker-wrap" id="picker" aria-labelledby="picker-h">
  <div class="wrap picker reveal">
    <div class="picker__copy">
      <span class="script">craft matchmaker</span>
      <h2 id="picker-h">What should I make today?</h2>
      <p>Tell us how much time you have and how adventurous you feel. We’ll line up projects that fit.</p>
    </div>
    <form class="picker__form" action="/projects/" method="get">
      <fieldset><legend>I have…</legend>
        <label><input type="radio" name="time" value="quick" checked><span>⏱ An hour or less</span></label>
        <label><input type="radio" name="time" value="afternoon"><span>☕ An afternoon</span></label>
        <label><input type="radio" name="time" value="weekend"><span>🗓 A whole weekend</span></label>
      </fieldset>
      <fieldset><legend>My skill level…</legend>
        <label><input type="radio" name="level" value="easy" checked><span>🌱 Total beginner</span></label>
        <label><input type="radio" name="level" value="moderate"><span>✂️ Comfortable</span></label>
        <label><input type="radio" name="level" value="" ><span>🔥 Surprise me</span></label>
      </fieldset>
      <button class="btn btn--primary" type="submit" data-confetti>Show my matches <span class="picker__n" aria-live="polite"></span></button>
    </form>
  </div>
</section>

<section class="section wrap season" aria-labelledby="season-h">
  <div class="section__head"><h2 id="season-h" class="h-script-under">Crafts for every season</h2><p>Plan ahead: pick a month and get a head start on the holiday.</p></div>
  <div class="season__tabs" role="tablist" aria-label="Holiday seasons">{season_btns}</div>
  {season_panels}
</section>

<section class="section wrap about-strip reveal">
  <div class="about-strip__art" aria-hidden="true"><svg viewBox="0 0 100 100" color="var(--coral)" fill="var(--coral)">{motif('scissors', 'var(--sun)')}</svg></div>
  <div><h2>Handmade beats store-bought</h2><p>{SITE['about']} Every tutorial lists the materials, tools, time and rough cost up front, so you know what you are getting into before the glue gun heats up.</p><a class="link-arrow" href="/about/">More about HotsBuzz →</a></div>
</section>
<script>window.HB_INDEX={json.dumps([{"t": time_bucket(p["minutes"]), "l": p["difficulty"].lower()} for p in posts], separators=(",", ":"))};</script>
''' + footer()
    write("home.html", out)


def page_category(c, posts):
    items = [p for p in posts if p["category"] == c["slug"]]
    path = f"/category/{c['slug']}/"
    crumbs, crumbs_ld = breadcrumbs([("Home", "/"), (c["name"], path)])
    others = "".join(f'<a class="pill pill--lg" style="--pc:{o["c1"]}" href="/category/{o["slug"]}/">{o["short"]}</a>' for o in CATEGORIES if o is not c)
    title = f"{strip_tags(c['name'])} Ideas & Tutorials | HotsBuzz"
    desc = f"{strip_tags(c['blurb'])} {len(items)} step-by-step {strip_tags(c['short'])} projects with materials, time and cost."
    ld = [crumbs_ld, {"@context": "https://schema.org", "@type": "CollectionPage", "name": strip_tags(c["name"]),
                      "url": ORIGIN + path, "description": desc, "isPartOf": {"@id": ORIGIN + "/#site"},
                      "mainEntity": {"@type": "ItemList", "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "url": ORIGIN + p["url"]} for i, p in enumerate(items)]}}]
    write(f"category/{c['slug']}/index.html", head(title, desc, path, image=f"/assets/og/cat-{c['slug']}.jpg", jsonld=ld) + header(path) + f'''
<section class="phero{' phero--photo' if has_photo('cat-' + c['slug']) else ''}" style="--c1:{c['c1']};--c2:{c['c2']};--acc:{c['accent']}">
  {img('cat-' + c['slug'], '', sizes='100vw', priority=True, cls='phero__photo') if has_photo('cat-' + c['slug']) else ''}
  <div class="phero__art" aria-hidden="true"><svg viewBox="0 0 100 100" color="#fff" fill="#fff">{motif(c['motif'], c['accent'])}</svg></div>
  <div class="wrap">
    {crumbs}
    <h1>{c['name']}</h1>
    <p class="phero__lede">{c['blurb']}</p>
    <p class="phero__count"><b>{len(items)}</b> projects in this category</p>
  </div>
</section>
<section class="section wrap">
  <div class="grid">{"".join(card(p, eager=i < 3) for i, p in enumerate(items))}</div>
</section>
<section class="section wrap more-cats"><h2 class="h-script-under">Explore more crafts</h2><div class="pills">{others}</div></section>
''' + footer())


def page_projects(posts):
    path = "/projects/"
    crumbs, crumbs_ld = breadcrumbs([("Home", "/"), ("All Projects", path)])
    chips = '<button class="chip" aria-pressed="true" data-cat="">All</button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-cat="{c["slug"]}" style="--pc:{c["c1"]}">{c["short"]}</button>' for c in CATEGORIES)
    title = "All DIY Projects & Craft Ideas | HotsBuzz"
    desc = f"Browse all {len(posts)} HotsBuzz DIY projects and craft ideas. Filter by category, time and skill level to find the perfect thing to make today."
    write("projects/index.html", head(title, desc, path, jsonld=[crumbs_ld]) + header(path) + f'''
<section class="phero phero--plain">
  <div class="wrap">{crumbs}<h1>All DIY projects</h1><p class="phero__lede">Every tutorial on HotsBuzz in one place. Search, filter and find your next make.</p></div>
</section>
<section class="section wrap">
  <div class="filters" id="search">
    <label class="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 20l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><span class="sr">Search projects</span><input type="search" name="q" placeholder="Search: wreath, mason jar, kids…" autocomplete="off"></label>
    <div class="chips" role="group" aria-label="Category">{chips}</div>
    <div class="selects">
      <label>Time <select name="time"><option value="">Any</option><option value="quick">An hour or less</option><option value="afternoon">An afternoon</option><option value="weekend">A weekend</option></select></label>
      <label>Skill <select name="level"><option value="">Any</option><option value="easy">Easy</option><option value="moderate">Moderate</option><option value="advanced">Advanced</option></select></label>
    </div>
    <p class="filters__count" aria-live="polite"><b>{len(posts)}</b> projects</p>
  </div>
  <div class="grid grid--filter">{"".join(card(p, eager=i < 3) for i, p in enumerate(posts))}</div>
  <div class="empty" hidden><p>No projects match those filters yet.</p><button class="btn btn--ghost" data-reset>Clear filters</button></div>
</section>
''' + footer())


def page_post(p, posts):
    c = CAT[p["category"]]
    path = p["url"]
    crumbs, crumbs_ld = breadcrumbs([("Home", "/"), (c["name"], f"/category/{c['slug']}/"), (p["title"], path)])
    intro = "".join(f"<p>{x}</p>" for x in p["intro"])
    mats = "".join(f'<li><label><input type="checkbox"><span>{m}</span></label></li>' for m in p["materials"])
    tools = "".join(f'<li><label><input type="checkbox"><span>{t}</span></label></li>' for t in p["tools"])
    steps = "".join(f'''<li class="step reveal" id="step-{i + 1}"><span class="step__n" aria-hidden="true">{i + 1}</span><div><h3>{s['title']}</h3><p>{s['body']}</p></div></li>''' for i, s in enumerate(p["steps"]))
    tips = "".join(f"<li>{t}</li>" for t in p["tips"])
    vars_ = "".join(f'<div class="var reveal" data-tilt><h3>{v["title"]}</h3><p>{v["body"]}</p></div>' for v in p["variations"])
    faq = "".join(f'<details class="faq__item"><summary>{f["q"]}</summary><div><p>{f["a"]}</p></div></details>' for f in p["faq"])
    related = [x for x in posts if x["category"] == p["category"] and x is not p]
    related += [x for x in posts if x["category"] != p["category"]][: max(0, 3 - len(related))]
    rel = "".join(card(x) for x in related[:3])
    toc = [("materials", "Materials &amp; tools"), ("steps", "Step-by-step"), ("tips", "Tips for success"),
           ("variations", "Make it your own"), ("faq", "FAQ")]
    toc_html = "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in toc)
    plain_title = strip_tags(p["title"])
    title = plain_title if len(plain_title) > 48 else f"{plain_title} | HotsBuzz"
    og_img = f"/assets/og/{p['slug']}.jpg"
    ld = [crumbs_ld, {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": ORIGIN + path + "#article", "headline": plain_title,
         "description": strip_tags(p["description"]), "datePublished": p["date"], "dateModified": p["date"],
         "mainEntityOfPage": ORIGIN + path, "image": ORIGIN + og_img, "articleSection": strip_tags(c["name"]),
         "keywords": p["keyword"], "wordCount": p["words"],
         "author": {"@type": "Organization", "name": SITE["name"] + " Team", "url": ORIGIN + "/about/"},
         "publisher": {"@id": ORIGIN + "/#org"}},
        {"@type": "HowTo", "name": plain_title, "description": strip_tags(p["excerpt"]), "image": ORIGIN + og_img,
         "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": strip_tags(p["cost"]).replace("$", "")},
         "supply": [{"@type": "HowToSupply", "name": strip_tags(m)} for m in p["materials"]],
         "tool": [{"@type": "HowToTool", "name": strip_tags(t)} for t in p["tools"]],
         "step": [{"@type": "HowToStep", "position": i + 1, "name": strip_tags(s["title"]), "text": strip_tags(s["body"]),
                   "url": ORIGIN + path + f"#step-{i + 1}"} for i, s in enumerate(p["steps"])]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip_tags(f["q"]),
                                             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(f["a"])}} for f in p["faq"]]},
        ORG,
    ]}]
    extra = f'<meta property="article:published_time" content="{p["date"]}">\n<meta property="article:section" content="{esc(strip_tags(c["name"]))}">\n'
    write(f"{p['slug']}/index.html", head(title, strip_tags(p["description"]), path, og_type="article", image=og_img, jsonld=ld, extra=extra) + header() + f'''
<article class="post" style="--c1:{c['c1']};--c2:{c['c2']};--acc:{c['accent']}" data-slug="{p['slug']}">
  <header class="post__hero">
    <div class="wrap post__hero-in">
      <div class="post__head">
        {crumbs}
        <a class="pill" style="--pc:{c['c1']}" href="/category/{c['slug']}/">{c['name']}</a>
        <h1>{p['title']}</h1>
        <p class="post__ex">{p['excerpt']}</p>
        <p class="post__by">By the {SITE['name']} team · <time datetime="{p['date']}">{fmt_date(p['date'])}</time></p>
      </div>
      <figure class="post__cover" data-tilt><span class="tape" aria-hidden="true"></span>{img(p['slug'], photo_alt(p['slug'], plain_title), sizes="(max-width: 860px) 100vw, 50vw", priority=True)}</figure>
    </div>
    <ul class="wrap facts">
      <li><span>Skill level</span>{chip_level(p['difficulty'])}</li>
      <li><span>Time</span><b>{p['time']}</b></li>
      <li><span>Budget</span><b>{p['cost']}</b></li>
      <li><span>Steps</span><b>{len(p['steps'])}</b></li>
    </ul>
  </header>
  <div class="wrap post__layout">
    <aside class="post__toc" aria-label="On this page"><div class="toc"><p class="toc__h">On this page</p><ol>{toc_html}</ol>
      <div class="toc__progress"><span class="toc__bar"></span><span class="toc__label">0% read</span></div></div></aside>
    <div class="prose">
      {intro}
      <section id="materials" class="box box--materials reveal">
        <div class="box__head"><h2>Materials &amp; tools</h2><span class="box__done" aria-live="polite"></span></div>
        <p class="box__note">Tick things off as you gather them. We’ll remember your list on this device.</p>
        <div class="box__cols"><div><h3>You’ll need</h3><ul class="check">{mats}</ul></div><div><h3>Tools</h3><ul class="check">{tools}</ul></div></div>
      </section>
      <section id="steps"><h2>Step-by-step instructions</h2><ol class="steps">{steps}</ol></section>
      <section id="tips" class="box box--tips reveal"><h2>Tips for success</h2><ul class="tips">{tips}</ul></section>
      <section id="variations"><h2>Make it your own</h2><div class="vars">{vars_}</div></section>
      <section id="faq" class="faq"><h2>Frequently asked questions</h2>{faq}</section>
      <div class="share reveal"><p>Made one? Share the idea with a crafty friend.</p>
        <div class="share__btns"><a class="btn btn--ghost" target="_blank" rel="noopener" href="https://www.pinterest.com/pin/create/button/?url={esc(ORIGIN + path)}&amp;description={esc(plain_title)}">Save to Pinterest</a><button class="btn btn--ghost" data-copy="{ORIGIN + path}">Copy link</button></div></div>
    </div>
  </div>
</article>
<section class="section wrap related"><div class="section__head"><h2 class="h-script-under">You might also like</h2><a class="link-arrow" href="/category/{c['slug']}/">More {c['short']} →</a></div><div class="grid">{rel}</div></section>
''' + footer())


def simple_page(path, title, desc, h1, body, lede=""):
    crumbs, crumbs_ld = breadcrumbs([("Home", "/"), (h1, path)])
    write(path.strip("/") + "/index.html", head(title, desc, path, jsonld=[crumbs_ld]) + header(path) + f'''
<section class="phero phero--plain"><div class="wrap">{crumbs}<h1>{h1}</h1>{f'<p class="phero__lede">{lede}</p>' if lede else ''}</div></section>
<section class="section wrap"><div class="prose prose--page">{body}</div></section>
''' + footer())


def page_static(posts):
    cats = "".join(f'<li><a href="/category/{c["slug"]}/">{c["name"]}</a>: {c["blurb"]}</li>' for c in CATEGORIES)
    simple_page("/about/", "About HotsBuzz | DIY Projects, Ideas & Crafts",
                "HotsBuzz is a DIY projects and crafts site: home decor makeovers, handmade gifts and holiday crafts with clear, honest, step-by-step instructions.",
                "About HotsBuzz", f'''
<p>{SITE['about']}</p>
<p>HotsBuzz started as a place to collect the DIY ideas and crafts we loved, and it is back with a fresh look and freshly written, step-by-step tutorials. Every project is planned so that a beginner with a free afternoon can finish it and be proud to give it away or hang it on the wall.</p>
<h2>How we write our tutorials</h2>
<ul>
<li><strong>Everything up front.</strong> Each project lists materials, tools, skill level, time and a realistic budget before you start.</li>
<li><strong>Real steps, not fluff.</strong> Instructions are short, numbered and specific, with the measurements you actually need.</li>
<li><strong>Safety included.</strong> Hot glue, candles, spray paint and craft knives come with plain-English safety notes, especially when kids are helping.</li>
<li><strong>Room to riff.</strong> Every tutorial ends with variations, so your version can look nothing like ours.</li>
</ul>
<h2>What you’ll find here</h2>
<ul>{cats}</ul>
<p>Have an idea you want to see, or a question about a project? <a href="/contact/">Get in touch</a>.</p>''',
                lede="Make it. Gift it. Love it. Handmade projects for real homes and real budgets.")
    simple_page("/contact/", "Contact HotsBuzz", "Get in touch with the HotsBuzz team with project questions, craft ideas or collaboration requests.",
                "Contact us", f'''
<p>We love hearing from fellow makers. Questions about a tutorial, a project you want us to try, or a photo of your finished make: send it over.</p>
<p class="contact-card"><span class="script">drop us a line</span><a class="btn btn--primary" href="mailto:{SITE['email']}" data-confetti>{SITE['email']}</a></p>
<p>We read every message and reply as quickly as we can, usually within a few days.</p>''',
                lede="Questions, ideas or show-and-tell. Our inbox is open.")
    simple_page("/privacy-policy/", "Privacy Policy | HotsBuzz", "How HotsBuzz handles information when you visit hotsbuzz.com, including cookies, local storage and email correspondence.",
                "Privacy policy", f'''
<p><em>Last updated {fmt_date(TODAY)}.</em></p>
<p>This policy explains what information {SITE['name']} ({SITE['domain']}) handles when you visit the site.</p>
<h2>Information we collect</h2>
<p>We do not ask you to create an account and we do not run sign-up forms. If you email us, we receive your email address and whatever you include in your message, and we use it only to reply.</p>
<h2>Local storage</h2>
<p>The site stores two small preferences in your browser’s local storage: your light or dark theme choice, and which materials you have ticked on a project checklist. They never leave your device and you can clear them at any time in your browser settings.</p>
<h2>Fonts and server logs</h2>
<p>Fonts are served by Google Fonts, which receives your IP address when your browser requests them. Our host keeps standard server logs (IP address, browser, pages requested) for security and troubleshooting.</p>
<h2>Third-party links</h2>
<p>When you use the “Save to Pinterest” button you are taken to Pinterest, whose own privacy policy applies.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>''')


def page_credits(posts):
    names = {p["slug"]: strip_tags(p["title"]) for p in posts}
    names.update({"cat-" + c["slug"]: strip_tags(c["name"]) + " (category)" for c in CATEGORIES})
    names["home"] = "Homepage"
    lic = {"pexels": ("Pexels License (free to use)", "https://www.pexels.com/license/"),
           "cc0": ("CC0 1.0 (public domain dedication)", "https://creativecommons.org/publicdomain/zero/1.0/"),
           "pdm": ("Public Domain Mark 1.0", "https://creativecommons.org/publicdomain/mark/1.0/")}
    items = []
    for key, ph in PHOTOS.items():
        if not has_photo(key):
            continue
        ln, lu = lic[ph["license"]]
        by = f" by {esc(ph['creator'])}" if ph.get("creator") else ""
        items.append(f'''<li><img src="/assets/photos/{key}-800.webp" alt="" width="800" height="500" loading="lazy"><div><b>{names.get(key, key)}</b>
Photo{by} via <a href="{esc(ph['landing'])}" rel="nofollow noopener" target="_blank">{esc(ph['source'].title())}</a> · <a href="{lu}" rel="nofollow noopener" target="_blank">{ln}</a></div></li>''')
    simple_page("/image-credits/", "Image Credits | HotsBuzz",
                "Sources and licenses for the photos used on HotsBuzz. Every photo is a royalty-free stock image under the Pexels License, CC0 or public domain.",
                "Image credits", f'''
<p>The photos on HotsBuzz are royalty-free stock images: free to use under the <strong>Pexels License</strong>, released under <strong>CC0</strong>, or marked as <strong>public domain</strong>. None of them requires payment or attribution. We credit the photographers here anyway, with thanks.</p>
<ul class="credits">{"".join(items)}</ul>''')


def page_404():
    write("404.html", head("Page not found | HotsBuzz", "Sorry, this page could not be found. Browse every HotsBuzz DIY project and craft idea instead.", "/404.html").replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + header() + f'''
<section class="phero phero--plain nf"><div class="wrap">
  <div class="nf__art" aria-hidden="true"><svg viewBox="0 0 100 100" color="var(--coral)" fill="var(--coral)">{motif('yarn', 'var(--sun)')}</svg></div>
  <h1>Oops, this project came unraveled.</h1>
  <p class="phero__lede">The page you’re looking for isn’t here. It may have moved when we rebuilt the site.</p>
  <p><a class="btn btn--primary" href="/">Back to the homepage</a> <a class="btn btn--ghost" href="/projects/">Browse all projects</a></p>
</div></section>
''' + footer())


def page_feeds(posts):
    urls = [("/", TODAY, "1.0"), ("/projects/", TODAY, "0.8"), ("/about/", TODAY, "0.4"),
            ("/contact/", TODAY, "0.3"), ("/privacy-policy/", TODAY, "0.2"), ("/image-credits/", TODAY, "0.1")]
    urls += [(f"/category/{c['slug']}/", TODAY, "0.7") for c in CATEGORIES]
    urls += [(p["url"], p["date"], "0.6") for p in posts]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls) + "</urlset>\n")
    if STAGING:
        write("robots.txt", "# Temporary hosting domain: keep it out of search until hotsbuzz.com is live.\nUser-agent: *\nDisallow: /\n")
    else:
        write("robots.txt", f"User-agent: *\nDisallow: /home.html\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    items = "".join(f'''<item><title>{esc(strip_tags(p["title"]))}</title><link>{ORIGIN}{p["url"]}</link><guid>{ORIGIN}{p["url"]}</guid><pubDate>{p["date"]}</pubDate><description>{esc(strip_tags(p["excerpt"]))}</description></item>''' for p in posts[:20])
    write("feed.xml", f'''<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{SITE['name']}</title><link>{ORIGIN}/</link><description>{SITE['tagline']}</description>{items}</channel></rss>\n''')


# -------------------------------------------------------------------- main ---

def main():
    global ASSET_V
    posts = load_posts()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    h = hashlib.md5()
    for f in sorted((ROOT / "assets").rglob("*")):
        if f.is_file():
            h.update(f.read_bytes())
    ASSET_V = h.hexdigest()[:8]
    for f in (ROOT / "static").iterdir():
        shutil.copy2(f, OUT / f.name)
    # cover art
    covers = OUT / "assets" / "covers"
    covers.mkdir(parents=True, exist_ok=True)
    for p in posts:
        (covers / f"{p['slug']}.svg").write_text(cover_svg(p["slug"], CAT[p["category"]], p["motif"]), encoding="utf-8")
    for c in CATEGORIES:
        (covers / f"cat-{c['slug']}.svg").write_text(cover_svg("cat" + c["slug"], c, c["motif"]), encoding="utf-8")

    page_home(posts)
    for c in CATEGORIES:
        page_category(c, posts)
    page_projects(posts)
    for p in posts:
        page_post(p, posts)
    page_static(posts)
    page_credits(posts)
    page_404()
    page_feeds(posts)
    # Card data for render_og.mjs (social images); not deployed.
    (ROOT / ".og.json").write_text(json.dumps(
        [{"file": "home", "title": "DIY projects, DIY ideas, crafts &amp; more", "label": SITE["domain"], "cover": "home"}]
        + [{"file": f"cat-{c['slug']}", "title": c["name"], "label": "Category", "cover": f"cat-{c['slug']}"} for c in CATEGORIES]
        + [{"file": p["slug"], "title": p["title"], "label": CAT[p["category"]]["short"], "cover": p["slug"]} for p in posts],
        ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"built {len(posts)} posts, {len(CATEGORIES)} categories -> {OUT.relative_to(ROOT.parent.parent)}")


if __name__ == "__main__":
    main()
