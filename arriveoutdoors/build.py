#!/usr/bin/env python3
"""Generate the Arrive Outdoors static site into public/.

    python3 build.py && python3 validate.py

Standard library only. Content lives in content/, settings and the URL
inventory in siteconfig.py, climate normals in data/climate.json.
"""
import datetime
import glob
import hashlib
import html
import json
import os
import re
import shutil
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from siteconfig import (SITE, AUTHOR, NAV, CATEGORIES, TOOLS as TOOL_LIST, DESTINATIONS,  # noqa: E402
                        MONTHS, ARTICLES, REDIRECTS, GONE)
from content.tools import TOOLS as TOOL_COPY  # noqa: E402
from content.gear import GEAR  # noqa: E402

OUT = os.path.join(ROOT, "public")
TODAY = "2026-10-31"
BUILD_DATE = os.environ.get("BUILD_DATE") or datetime.date.today().isoformat()
UNPUBLISHED_RX = None
E = html.escape
URL = SITE["url"]
MONTH_NAMES = [m.capitalize() for m in MONTHS]
MON3 = [m[:3].capitalize() for m in MONTHS]
SITEMAP = []  # (path, lastmod)


# --------------------------------------------------------------------------- helpers
def write(path, text):
    """path is a URL path like /tools/ or a file like /robots.txt"""
    if UNPUBLISHED_RX is not None:
        text = UNPUBLISHED_RX.sub(r"\1", text)
    fp = OUT + (path + "index.html" if path.endswith("/") else path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(text)


def asset_v(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def amazon_search(q):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(q)}&tag={SITE['amazon_tag']}"


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def breadcrumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + p} for i, (n, p) in enumerate(items)]}


def crumbs_html(items):
    parts = [f'<a href="{p}">{E(n)}</a>' for n, p in items[:-1]] + [E(items[-1][0])]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(parts) + "</nav>"


def faq_block(faq, heading="Frequently asked questions"):
    if not faq:
        return "", None
    items = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faq)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return f'<section class="faq"><h2 id="faq">{E(heading)}</h2>{items}</section>', schema


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


# --------------------------------------------------------------------------- icons
ICONS = {
    "backpack": '<path d="M4 10a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/><path d="M8 21v-5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v5"/><path d="M8 10h8"/>',
    "cloud-sun": '<path d="M12 2v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="M20 12h2"/><path d="m19.07 4.93-1.41 1.41"/><path d="M15.95 12.65a4 4 0 0 0-5.93-4.32"/><path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z"/>',
    "timer": '<path d="M10 2h4"/><path d="M12 14l3-3"/><circle cx="12" cy="14" r="8"/>',
    "droplet": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
    "sunrise": '<path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m8 6 4-4 4 4"/><path d="M16 18a4 4 0 0 0-8 0"/>',
    "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "thermometer": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "mountain": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>',
    "map": '<path d="M14.1 6.3 9.9 3.6a2 2 0 0 0-1.8 0L3.6 6A1 1 0 0 0 3 7v12.4a1 1 0 0 0 1.4.9l3.7-2.1a2 2 0 0 1 1.8 0l4.2 2.7a2 2 0 0 0 1.8 0l4.5-2.4a1 1 0 0 0 .6-.9V5.2a1 1 0 0 0-1.4-.9l-3.7 2.1a2 2 0 0 1-1.8 0z"/><path d="M15 5.8v15"/><path d="M9 3.2v15"/>',
    "tent": '<path d="M3.5 21 14 3"/><path d="M20.5 21 10 3"/><path d="M15.5 21 12 15l-3.5 6"/><path d="M2 21h20"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "menu": '<line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
}


def icon(name, size=22):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


LOGO = ('<svg width="40" height="32" viewBox="0 0 38 30" aria-hidden="true"><path d="M2 28 14 6l6 10 4-6 12 18z" fill="#86a86b"/>'
        '<path d="M14 6l3.4 6.2-2.2-1.4-2.4 2.6-1.6-1.6z M24 10l2.6 3.9-1.6-.8-1.6 1.6-1.2-1.2z" fill="#fff"/>'
        '<path d="M10 28l8-9 5 5 4-3 9 7z" fill="#ff6a2b"/></svg>')

# Layered mountain silhouettes at the bottom of every hero (parallax at different speeds)
RIDGE_BACK = ('<svg class="r1" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true"><path d="M0 220V120l70-36 60 22 90-70 80 54 60-30 110 66 70-44 90 26 70-52 60 30 80-60 110 80 70-30 90 40 80-56 100 66 70-22 60 18 70-30v168z"/></svg>')
RIDGE_MID = ('<svg class="r2" viewBox="0 0 1440 180" preserveAspectRatio="none" aria-hidden="true"><path d="M0 180V110l110-40 70 30 120-62 100 58 80-24 130 50 100-46 90 30 120-58 90 42 110-30 100 36 120-44 100 40v118z"/>'
             '<g><path d="M218 112l10-28 10 28z"/><path d="M232 112l8-22 8 22z"/><path d="M1010 104l11-30 11 30z"/><path d="M1026 104l8-22 8 22z"/><path d="M640 120l9-24 9 24z"/></g></svg>')


def ridges(fill):
    return (f'<div class="ridges" aria-hidden="true"><div data-parallax="-0.06">{RIDGE_BACK}</div><div data-parallax="-0.02">{RIDGE_MID}</div>'
            f'<svg viewBox="0 0 1440 70" preserveAspectRatio="none"><path fill="{fill}" d="M0 70V40c120-20 240 18 380 4s250-36 400-10 260 24 380 6 200-20 280-8v38z"/></svg></div>')


FOOT_RIDGE = ('<div class="ridge-top" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none">'
              '<path fill="#0d1f19" d="M0 120V70l90-30 80 24 120-52 90 40 70-22 130 50 90-32 100 26 90-44 120 56 90-28 110 32 100-48 120 44 70-18v82z"/>'
              '<path fill="#07130f" d="M0 120V96l130-30 90 26 140-42 110 44 100-22 150 34 120-30 110 22 140-36 110 30 120-18 120 26v20z"/></svg></div>')

CSS_V = asset_v("assets/css/site.css")
JS_V = asset_v("assets/js/site.js")
FX_V = asset_v("assets/js/fx.js")

# --------------------------------------------------------------------------- photos
_pj = os.path.join(ROOT, "data", "photos.json")
PHOTOS = json.load(open(_pj)) if os.path.exists(_pj) else {}


def photo_src(key, w=1280):
    p = PHOTOS.get(key)
    if not p:
        return None
    best = min(p["widths"], key=lambda x: abs(x - w))
    return f"/assets/img/photos/{key}-{best}.webp"


def picture(key, sizes="100vw", cls="", eager=False, alt=None):
    p = PHOTOS.get(key)
    if not p:
        return f'<div class="ph {cls}">{icon("mountain", 44)}</div>'
    srcset = ", ".join(f"/assets/img/photos/{key}-{w}.webp {w}w" for w in p["widths"])
    w0 = p["widths"][min(1, len(p["widths"]) - 1)]
    h0 = round(w0 / p["ratio"])
    a = p.get("alt", "") if alt is None else alt
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/img/photos/{key}-{w0}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w0}" height="{h0}" alt="{E(a)}" {load}>')


# --------------------------------------------------------------------------- layout
def layout(*, path, title, description, body, schema=(), og_image=None, og_type="website",
           scripts=(), noindex=False, sitemap=True, lastmod=TODAY, active=None, progress=False):
    full_title = title if (SITE["name"] in title or len(title) + len(SITE["name"]) + 3 > 65) else f"{title} | {SITE['name']}"
    canonical = URL + path
    og_img = URL + (og_image or photo_src("hero-night", 1280) or "/assets/img/icon-192.webp")
    gtag = ""
    if SITE.get("gtag"):
        ids = SITE["gtag"] if isinstance(SITE["gtag"], list) else [SITE["gtag"]]
        gtag = (f'<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id={ids[0]}"></script>'
                "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());"
                + "".join(f"gtag('config','{i}');" for i in ids) + "</script>")
    ads = ""
    if SITE.get("adsense_on"):
        ads = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={SITE["adsense_client"]}" crossorigin="anonymous"></script>'
    nav = "".join(f'<a href="{h}"{" aria-current=page" if active == h else ""}>{E(n)}</a>' for n, h in NAV)
    js = (f'<script src="/assets/js/site.js?v={JS_V}" defer></script><script src="/assets/js/fx.js?v={FX_V}" defer></script>' +
          "".join(f'<script src="{s}?v={asset_v(s.lstrip("/"))}" defer></script>' for s in scripts))
    schema_html = "".join(ld(s) for s in schema if s)
    if sitemap and not noindex:
        SITEMAP.append((path, lastmod))
    foot_tools = "".join(f'<li><a href="/tools/{s}/">{E(n.split(" (")[0].replace(" Calculator", "").replace(" Generator", ""))}</a></li>' for s, n, *_ in TOOL_LIST[:6])
    foot_dest = "".join(f'<li><a href="/destinations/{d[0]}/">{E(d[1].replace(" National Park", ""))}</a></li>' for d in DESTINATIONS[:6])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full_title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{canonical}">
{'<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/icons/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#07130f">
<link rel="preload" href="/assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://api.open-meteo.com" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
{gtag}{ads}{schema_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{'<div class="progress-trail" aria-hidden="true"></div>' if progress else ''}
<div class="grain" aria-hidden="true"></div>
<header class="site-header"><div class="wrap">
<a class="brand" href="/">{LOGO}<span>Arrive<small>Outdoors</small></span></a>
<button class="menu-btn" aria-controls="nav" aria-expanded="false" aria-label="Menu">{icon("menu")}</button>
<nav class="nav" id="nav">{nav}<a class="cta" href="/tools/trail-weather/">Trail forecast</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-footer">{FOOT_RIDGE}<canvas data-fx="stars" data-star-top="1" aria-hidden="true"></canvas><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/">{LOGO}<span>Arrive<small>Outdoors</small></span></a>
<p style="margin-top:14px">{E(SITE['description'])}</p>
<p class="small">Some links are affiliate links: if you buy through them we may earn a commission, at no cost to you. <a href="/affiliate-disclosure/">How that works</a>.</p></div>
<div><h4>Tools</h4><ul>{foot_tools}<li><a href="/tools/">All tools</a></li></ul></div>
<div><h4>Destinations</h4><ul>{foot_dest}<li><a href="/destinations/">All destinations</a></li></ul></div>
<div><h4>Plan</h4><ul><li><a href="/weather/">Where to go by month</a></li><li><a href="/guides/">Guides</a></li><li><a href="/gear/">Gear picks</a></li><li><a href="/rent-camping-gear/">Rent camping gear</a></li><li><a href="/tools/packing-list/">Packing list</a></li></ul></div>
<div><h4>Arrive Outdoors</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms-of-use/">Terms of use</a></li><li><a href="/photo-credits/">Photo credits</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© 2026 Arrive Outdoors. Weather data: Open-Meteo (CC BY 4.0). Photos: Pexels. Conditions change — always check official park and weather sources.</span><span>As an Amazon Associate, Arrive Outdoors earns from qualifying purchases.</span></div>
</div></footer>
{js}
</body>
</html>
"""


def hero(title, lead, eyebrow=None, small=True, extra="", photo=None, fx_modes=None, full=False, split=False, below="var(--bg)", crumbs=None):
    has = photo and photo in PHOTOS
    if not has and not fx_modes:
        fx_modes = "stars"
    bg = f'<div class="bg" data-parallax="0.3">{picture(photo, eager=True, alt="")}</div>' if has else '<div class="bg"></div>'
    canvas = f'<canvas class="fx" data-fx="{fx_modes}" aria-hidden="true"></canvas>' if fx_modes else ""
    cls = "hero" + (" full" if full else " small" if small else "") + ("" if has else " no-photo")
    credit = ""
    if has and PHOTOS[photo].get("page"):
        who = PHOTOS[photo].get("photographer") or "Pexels"
        credit = f'<span class="hero-photo-credit">Photo: <a href="{E(PHOTOS[photo]["page"])}" rel="nofollow noopener">{E(who)}</a></span>'
    return (f'<section class="{cls}">{bg}{canvas}<div class="wrap">'
            + (crumbs_html(crumbs) if crumbs else "")
            + (f'<span class="eyebrow">{E(eyebrow)}</span>' if eyebrow else "")
            + f'<h1{" data-split" if split else ""}>{title}</h1>' + (f'<p class="lead">{lead}</p>' if lead else "") + extra
            + f"</div>{ridges(below)}{credit}</section>")


# --------------------------------------------------------------------------- climate
CLIMATE = json.load(open(os.path.join(ROOT, "data", "climate.json")))["places"]


def month_score(m):
    """0-100 comfort score for hiking & tent camping in an average month."""
    s = 100.0
    hi, lo = m["high"], m["low"]
    if hi < 62:
        s -= (62 - hi) * 2.0
    if hi > 80:
        s -= (hi - 80) * 2.8
    if lo < 35:
        s -= (35 - lo) * 0.9
    s -= m["wet_days"] * 1.6
    s -= m["snow_days"] * 2.5
    s -= m["hot_days"] * 0.5
    return max(0, min(100, round(s)))


def score_class(s):
    return "good" if s >= 75 else "ok" if s >= 60 else "fair" if s >= 45 else "poor"


def score_word(s):
    return {"good": "Excellent", "ok": "Good", "fair": "Fair", "poor": "Poor"}[score_class(s)]


SCORE_COLORS = {"good": "#23784a", "ok": "#677516", "fair": "#a3640b", "poor": "#b8412a"}


def place_scores(slug):
    return [month_score(m) for m in CLIMATE[slug]["months"]]


def best_months(slug, n=3):
    sc = place_scores(slug)
    order = sorted(range(12), key=lambda i: -sc[i])
    return sorted(order[:n])


def month_reason(m):
    bits = [f"highs near {round(m['high'])}°F, lows {round(m['low'])}°F"]
    if m["wet_days"] >= 8:
        bits.append(f"{round(m['wet_days'])} wet days")
    elif m["wet_days"] <= 3:
        bits.append("mostly dry")
    if m["snow_days"] >= 2:
        bits.append(f"snow on ~{round(m['snow_days'])} days")
    if m["hot_days"] >= 5:
        bits.append(f"{round(m['hot_days'])} days over 90°F")
    if m["freeze_nights"] >= 10:
        bits.append("frequent freezing nights")
    return ", ".join(bits)


def load_dest_copy(slug):
    fp = os.path.join(ROOT, "content", "destinations", slug + ".json")
    if os.path.exists(fp):
        return json.load(open(fp, encoding="utf-8"))
    return {}


DEST = {d[0]: dict(zip(("slug", "name", "state", "lat", "lon", "elev", "hub"), d)) for d in DESTINATIONS}
for _s in DEST:
    DEST[_s]["copy"] = load_dest_copy(_s)


def short_name(slug):
    return DEST[slug]["name"].replace(" National Park", "")


# --------------------------------------------------------------------------- articles
def load_articles():
    arts = {}
    for slug in ARTICLES:
        fp = os.path.join(ROOT, "content", "articles", slug.replace("/", "__") + ".html")
        if not os.path.exists(fp):
            print("  missing article:", slug)
            continue
        raw = open(fp, encoding="utf-8").read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*(.*)", raw, re.S)
        if not m:
            raise SystemExit("bad meta block: " + fp)
        meta = json.loads(m.group(1))
        body = m.group(2).strip()
        # Amazon links: always sponsored/nofollow and new tab-safe
        def fix_amz(mm):
            tag = mm.group(0)
            tag = re.sub(r'\srel="[^"]*"', "", tag)
            return tag[:-1] + ' rel="sponsored nofollow noopener" target="_blank">'
        body = re.sub(r'<a [^>]*href="https://(?:www\.)?amazon\.com[^"]*"[^>]*>', fix_amz, body)
        # external non-amazon links open normally but get noopener
        meta["slug"] = slug
        meta["path"] = "/" + slug + "/"
        meta["body"] = body
        meta["words"] = len(re.sub(r"<[^>]+>", " ", body).split())
        meta["toc"] = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', body, re.S)
        meta["has_amazon"] = "amazon.com" in body
        img = slug.split("/")[-1]
        meta["image"] = f"/assets/img/posts/{img}.webp" if os.path.exists(os.path.join(ROOT, "assets", "img", "posts", img + ".webp")) else None
        arts[slug] = meta
    return arts


ARTS_ALL = load_articles()
ARTS = {}


def art_photo(a):
    k = "art-" + a["slug"].split("/")[-1]
    if k == "art-camping-101-a-guide-for-the-first-time-camper":
        k = "art-camping-101"
    return k if k in PHOTOS else None


def article_card(a):
    k = art_photo(a)
    if k:
        media = picture(k, sizes="(max-width:700px) 100vw, 400px")
    elif a.get("image"):
        media = f'<img src="{a["image"]}" alt="" loading="lazy" width="900" height="600">'
    else:
        media = f'<div class="ph">{icon("mountain", 44)}</div>'
    return (f'<a class="card" href="{a["path"]}"><div class="media">{media}</div><div class="body"><span class="meta">{E(CATEGORIES.get(a["category"], ""))}</span>'
            f'<h3>{E(a["h1"])}</h3><p>{E(a.get("summary", ""))}</p><span class="more">Read the guide</span></div></a>')


def tool_card(slug, light=False):
    t = next(x for x in TOOL_LIST if x[0] == slug)
    return (f'<a class="card tool-card{" light" if light else ""}" href="/tools/{slug}/"><div class="body"><div class="icon-badge">{icon(t[3], 24)}</div>'
            f'<h3>{E(t[1])}</h3><p>{E(t[2])}</p><span class="more">Open tool</span></div></a>')


def dest_card(slug, month=None):
    d = DEST[slug]
    sc = place_scores(slug)
    band = "".join(f'<i style="background:{SCORE_COLORS[score_class(s)]}" title="{MON3[i]}: {score_word(s)}"></i>' for i, s in enumerate(sc))
    bm = best_months(slug)
    extra = f'<span class="chip {score_class(sc[month])}">{MONTH_NAMES[month]}: {score_word(sc[month])}</span>' if month is not None else ""
    return (f'<a class="card dest-card" href="/destinations/{slug}/"><div class="media">{picture("dest-" + slug, sizes="(max-width:700px) 100vw, 320px")}</div>'
            f'<div class="body"><span class="meta">{E(d["state"])}</span><h3>{E(short_name(slug))}</h3>'
            f'<p>Best weather: <strong>{" · ".join(MON3[i] for i in bm)}</strong></p>{extra}'
            f'<div class="band" aria-label="Weather score by month">{band}</div><div class="band-labels"><span>Jan</span><span>Jun</span><span>Dec</span></div></div></a>')


def rank_item(sc, s, m, thumb=True):
    t = picture("dest-" + s, sizes="64px", cls="thumb", alt="") if thumb and ("dest-" + s) in PHOTOS else ""
    return (f'<li class="{"" if t else "nothumb"}">{t}<div><a href="/destinations/{s}/">{E(DEST[s]["name"])}</a><div class="why">{E(month_reason(m))}</div></div>'
            f'<span class="score-pill" style="background:{SCORE_COLORS[score_class(sc)]}">{sc} · {score_word(sc)}</span></li>')


def render_article(a):
    path = a["path"]
    cat = a["category"]
    crumbs = [("Home", "/"), ("Guides", "/guides/"), (CATEGORIES.get(cat, "Guides"), f"/guides/#{cat}"), (a["h1"], path)]
    toc = ""
    if len(a["toc"]) >= 3:
        toc = '<nav class="toc" aria-label="Contents"><h2>In this guide</h2><ol>' + "".join(
            f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in a["toc"]) + (
            '<li><a href="#faq">FAQ</a></li>' if a.get("faq") else "") + "</ol></nav>"
    tools_side = "".join(f'<li><a href="/tools/{t}/">{E(next(x[1] for x in TOOL_LIST if x[0] == t))}</a></li>'
                         for t in a.get("tools", []) if any(x[0] == t for x in TOOL_LIST))
    dest_side = "".join(f'<li><a href="/destinations/{d}/">{E(DEST[d]["name"])}</a></li>' for d in a.get("destinations", []) if d in DEST)
    aside = toc
    if tools_side:
        aside += f'<div class="side-card"><h3>Free tools for this</h3><ul>{tools_side}</ul></div>'
    if dest_side:
        aside += f'<div class="side-card"><h3>Weather & timing guides</h3><ul>{dest_side}</ul></div>'
    disclosure = ('<p class="disclosure">This guide contains affiliate links. If you buy through them, Arrive Outdoors may earn a '
                  'commission at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>') if a["has_amazon"] else ""
    faq_html, faq_schema = faq_block([(f["q"], f["a"]) for f in a.get("faq", [])])
    related = [ARTS[s] for s in a.get("related", []) if s in ARTS][:3]
    rel_html = ('<section class="block topo"><div class="wrap"><div class="section-head"><div><span class="kicker">Keep exploring</span><h2>Read next</h2></div></div><div class="grid g3 reveal-stagger">' +
                "".join(article_card(r) for r in related) + "</div></div></section>") if related else ""
    minutes = max(3, round(a["words"] / 230))
    updated = a.get("updated", TODAY)
    k = art_photo(a)
    byline = (f'<p class="lead">{E(a.get("summary", ""))}</p><div class="byline"><span>By <a href="{AUTHOR["url"]}"><strong>{E(AUTHOR["name"])}</strong></a></span><i class="dot"></i>'
              f'<span>{"Published" if updated == a["published"] else "Updated"} <time datetime="{updated}">{fmt_date(updated)}</time></span><i class="dot"></i><span>{minutes} min read</span></div>')
    body = (hero(E(a["h1"]), "", eyebrow=CATEGORIES.get(cat, ""), photo=k, extra=byline, crumbs=crumbs,
                 fx_modes="embers" if "fire" in a["slug"] else ("snow" if "cold" in a["slug"] else ("stars" if not k else None))) +
            f"""<div class="wrap">
<div class="layout">
<article class="prose">
{disclosure}
{a["body"]}
{faq_html}
<div class="author-box"><div class="avatar">{icon("mountain", 26)}</div><div><strong>{E(AUTHOR['name'])}</strong><p>{E(AUTHOR['bio'])}</p>
<p class="small muted">{"First published " + fmt_date(a["published"]) + "." if updated != a["published"] else ""} Spot something out of date? <a href="/contact/">Tell us</a>.</p></div></div>
</article>
<aside class="no-print">{aside}</aside>
</div></div>
{rel_html}""")
    img = photo_src(k, 1280) if k else a.get("image")
    schema = [{
        "@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["description"],
        "datePublished": a["published"], "dateModified": updated, "mainEntityOfPage": URL + path,
        "author": {"@type": "Organization", "name": AUTHOR["name"], "url": URL + AUTHOR["url"]},
        "publisher": {"@type": "Organization", "name": SITE["name"], "logo": {"@type": "ImageObject", "url": URL + "/assets/icons/icon-512.png"}},
        **({"image": URL + img} if img else {}),
    }, breadcrumbs_ld(crumbs), faq_schema]
    write(path, layout(path=path, title=a["title"], description=a["description"], body=body, schema=schema,
                       og_image=img, og_type="article", lastmod=updated, active="/guides/", progress=True))


# --------------------------------------------------------------------------- tools
TOOL_PHOTOS = {"trip-finder": "art-car-camping-essentials", "packing-list": "hero-day", "trail-weather": "summit", "hiking-time-calculator": "trail", "water-calculator": "desert-camp",
               "sleeping-bag-temperature": "snow-camp", "backpack-size": "art-how-to-measure-torso-length-for-backpack",
               "sunrise-sunset": "summit", "camp-meal-planner": "campfire", "rent-vs-buy": "art-rent-camping-gear", "feels-like": "desert-camp"}
TOOL_FX = {"sleeping-bag-temperature": "snow", "camp-meal-planner": "embers", "sunrise-sunset": "stars"}


def render_tool(slug, name, desc, ic):
    c = TOOL_COPY[slug]
    path = f"/tools/{slug}/"
    form = c["form"]
    if "{QUICK_PLACES}" in form:
        quick = "".join(f'<button type="button" class="chip" style="cursor:pointer" data-name="{E(d["hub"] + ", " + short_name(s))}" '
                        f'data-lat="{d["lat"]}" data-lon="{d["lon"]}" data-elev="{d["elev"]}">{E(short_name(s))}</button>'
                        for s, d in list(DEST.items())[:12])
        form = form.replace("{QUICK_PLACES}", quick)
    result_title = c.get("result_title", "")
    faq_html, faq_schema = faq_block(c["faq"])
    others = [t[0] for t in TOOL_LIST if t[0] != slug][:3]
    crumbs = [("Home", "/"), ("Tools", "/tools/"), (c["h1"], path)]
    res_cls = ' class="forecast"' if slug == "trail-weather" else ""
    data_js = ""
    if "PLACE_FIELD" in c.get("form_marker", "") or 'id="place"' in form:
        places = [{"n": d["name"], "h": d["hub"], "lat": d["lat"], "lon": d["lon"], "e": d["elev"]} for d in DEST.values()]
        data_js += "<script>window.AO_PLACES=" + json.dumps(places, separators=(",", ":")) + ";</script>"
    if slug == "trip-finder":
        trips = [{"slug": k, "name": d["name"], "short": short_name(k), "lat": d["lat"], "lon": d["lon"], "sc": place_scores(k),
                  "hi": [round(m["high"]) for m in CLIMATE[k]["months"]], "lo": [round(m["low"]) for m in CLIMATE[k]["months"]],
                  "wet": [round(m["wet_days"]) for m in CLIMATE[k]["months"]], "p": photo_src("dest-" + k, 640) or ""}
                 for k, d in DEST.items() if k in CLIMATE]
        data_js += "<script>window.AO_TRIPS=" + json.dumps(trips, separators=(",", ":")) + ";</script>"
    body = (hero(E(c["h1"]), E(c["intro"]), eyebrow="Free tool", photo=TOOL_PHOTOS.get(slug), fx_modes=TOOL_FX.get(slug), crumbs=crumbs) +
            f'<div class="wrap"><div class="tool-shell">{form}<div class="panel" aria-live="polite">{result_title}<div id="result"{res_cls}></div></div></div>{data_js}'
            f'<div class="read prose reveal">{c["explain"]}{faq_html}</div></div>'
            f'<section class="block dark no-print"><div class="wrap"><div class="section-head"><div><span class="kicker">Keep planning</span><h2>More free tools</h2></div><a class="link" style="color:var(--amber)" href="/tools/">All tools →</a></div><div class="grid g3 reveal-stagger">{"".join(tool_card(o) for o in others)}</div></div></section>')
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": c["h1"], "url": URL + path,
               "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "description": c["description"],
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}, breadcrumbs_ld(crumbs), faq_schema]
    write(path, layout(path=path, title=c["title"], description=c["description"], body=body, schema=schema,
                       scripts=[f"/assets/js/tools/{slug}.js"], active="/tools/"))


def render_tools_hub():
    body = (hero("Free camping & hiking tools", "Planning calculators that answer the questions every trip starts with: what to pack, how long it'll take, how much water, how warm a bag, and what the weather will do.",
                 eyebrow="Tools", photo="map", below="var(--night)") +
            f'<section class="block dark" style="padding-top:40px"><div class="wrap"><div class="grid g3 reveal-stagger">{"".join(tool_card(t[0]) for t in TOOL_LIST)}</div>'
            '<p class="small" style="margin-top:28px;color:rgba(255,255,255,.6)">Every tool runs in your browser and is free to use. Forecasts come from Open-Meteo; formulas are explained on each page.</p></div></section>')
    write("/tools/", layout(path="/tools/", title="Free Camping & Hiking Tools and Calculators",
                            description="Free camping and hiking tools: packing list generator, trail forecast with hike score, hiking time, water, sleeping bag, backpack size and more.",
                            body=body, active="/tools/"))


# --------------------------------------------------------------------------- destinations
def climate_section(slug):
    c = CLIMATE[slug]
    ms = c["months"]
    sc = place_scores(slug)
    tmin = min(m["low"] for m in ms) - 5
    tmax = max(m["high"] for m in ms) + 8
    span = tmax - tmin
    cols = ""
    for m in ms:
        bottom = (m["low"] - tmin) / span * 100
        height = (m["high"] - m["low"]) / span * 100
        cols += (f'<div class="col"><div class="bar" style="bottom:{bottom:.1f}%;height:{height:.1f}%">'
                 f'<b>{round(m["high"])}°</b><i>{round(m["low"])}°</i></div></div>')
    pmax = max(m["precip_in"] for m in ms) or 1
    precip = "".join(f'<div style="height:{max(3, m["precip_in"] / pmax * 100):.0f}%"><span>{m["precip_in"]:.1f}"</span></div>' for m in ms)
    strip = "".join(f'<div class="m {score_class(s)}">{MON3[i]}<small>{s}</small></div>' for i, s in enumerate(sc))
    rows = "".join(
        f'<tr><td><a href="/weather/{MONTHS[i]}/">{MONTH_NAMES[i]}</a></td><td>{round(m["high"])}°F</td><td>{round(m["low"])}°F</td>'
        f'<td>{m["precip_in"]:.1f} in</td><td>{m["wet_days"]:.0f}</td><td>{m["snow_in"]:.0f} in</td><td>{m["freeze_nights"]:.0f}</td>'
        f'<td>{m["sun_hours"]:.0f} h</td><td><span class="chip {score_class(sc[i])}">{score_word(sc[i])}</span></td></tr>'
        for i, m in enumerate(ms))
    elev_ft = round(c["elevation_m"] * 3.281)
    return f"""<h2 id="weather">Month-by-month weather at {E(c["hub"])}</h2>
<p>Ten-year averages (2015–2024) at {E(c["hub"])}, about {elev_ft:,} ft. Higher trails are colder, windier and snowier — temperatures typically drop 3–5°F for every 1,000 ft you climb.</p>
<h3>Hiking & camping weather score by month</h3>
<div class="months" role="img" aria-label="Monthly weather score">{strip}</div>
<div class="legend"><span><i style="background:var(--good)"></i>Excellent 75+</span><span><i style="background:var(--ok)"></i>Good 60–74</span><span><i style="background:var(--fair)"></i>Fair 45–59</span><span><i style="background:var(--poor)"></i>Poor &lt;45</span></div>
<h3>Average high and low temperature (°F)</h3>
<div class="chart pre" role="img" aria-label="Average monthly high and low temperatures">{cols}</div>
<div class="chart-labels">{"".join(f"<span>{m}</span>" for m in MON3)}</div>
<h3>Average precipitation (inches per month)</h3>
<div class="precip" role="img" aria-label="Average monthly precipitation">{precip}</div>
<div class="chart-labels" style="margin-top:6px">{"".join(f"<span>{m}</span>" for m in MON3)}</div>
<div class="table-wrap"><table><thead><tr><th>Month</th><th>Avg high</th><th>Avg low</th><th>Precip</th><th>Wet days</th><th>Snow</th><th>Freezing nights</th><th>Sun/day</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small muted">Score rates hiking and tent-camping weather only (temperature, rain, snow and heat) — it doesn't account for crowds, road closures or permits, which are covered in the seasonal notes. Data: Open-Meteo historical weather API (ERA5 reanalysis), adjusted to the hub elevation.</p>"""


def render_destination(slug):
    d = DEST[slug]
    cp = d["copy"]
    path = f"/destinations/{slug}/"
    ms = CLIMATE[slug]["months"]
    sc = place_scores(slug)
    bm = best_months(slug)
    name = d["name"]
    sname = short_name(slug)
    title = cp.get("title") or f"Best Time to Visit {sname}: Month-by-Month Weather"
    desc = cp.get("description") or f"When to visit {name}: 10-year monthly weather averages, the best months for hiking and camping, seasonal tips and a live 7-day forecast."
    hottest = max(range(12), key=lambda i: ms[i]["high"])
    coldest = min(range(12), key=lambda i: ms[i]["low"])
    wettest = max(range(12), key=lambda i: ms[i]["precip_in"])
    stats = (f'<div class="stats"><div class="stat"><span>Best weather</span><b>{", ".join(MON3[i] for i in bm)}</b></div>'
             f'<div class="stat"><span>Warmest</span><b>{MON3[hottest]} · {round(ms[hottest]["high"])}°F</b></div>'
             f'<div class="stat"><span>Coldest nights</span><b>{MON3[coldest]} · {round(ms[coldest]["low"])}°F</b></div>'
             f'<div class="stat"><span>Wettest</span><b>{MON3[wettest]} · {ms[wettest]["precip_in"]:.1f} in</b></div>'
             f'<div class="stat"><span>Hub elevation</span><b>{round(d["elev"] * 3.281):,} ft</b></div></div>')
    best_for = ""
    if cp.get("best_for"):
        best_for = '<div class="table-wrap"><table><tbody>' + "".join(
            f"<tr><th>Best for {E(k)}</th><td>{E(v)}</td></tr>" for k, v in cp["best_for"].items()) + "</tbody></table></div>"
    seasons = ""
    if cp.get("seasons"):
        seasons = '<h2 id="seasons">Season by season</h2><div class="season-grid">' + "".join(
            f'<div class="season reveal" data-icon="{ {"spring": "🌱", "summer": "☀️", "fall": "🍂", "winter": "❄️"}.get(k, "")}"><h3>{k.capitalize()}</h3>{v}</div>' for k, v in cp["seasons"].items()) + "</div>"
    hikes = ""
    if cp.get("hikes"):
        hikes = ('<h2 id="hikes">Hikes worth timing right</h2><div class="table-wrap"><table><thead><tr><th>Hike</th><th>Level</th><th>Notes</th></tr></thead><tbody>' +
                 "".join(f'<tr><td><strong>{E(h["name"])}</strong></td><td>{E(h.get("level", ""))}</td><td>{E(h.get("note", ""))}</td></tr>' for h in cp["hikes"]) +
                 "</tbody></table></div>")
    camping = f'<h2 id="camping">Camping at {E(sname)}</h2>{cp["camping"]}' if cp.get("camping") else ""
    know = ""
    if cp.get("know_before"):
        know = '<h2 id="know-before">Know before you go</h2><ul>' + "".join(f"<li>{E(k)}</li>" for k in cp["know_before"]) + "</ul>"
    if cp.get("official_url"):
        know += f'<p>Official information, alerts and current conditions: <a href="{E(cp["official_url"])}" rel="noopener">{E(cp["official_url"].replace("https://", "").rstrip("/"))}</a>.</p>'
    season_key = {0: "cold", 1: "cold", 2: "shoulder", 3: "shoulder", 4: "shoulder", 5: "warm", 6: "warm", 7: "warm", 8: "warm", 9: "shoulder", 10: "shoulder", 11: "cold"}
    pack_links = " · ".join(
        f'<a href="/tools/packing-list/?trip=car&season={s}&nights=2&people=2&extras={"bear" if slug in ("yellowstone", "glacier", "grand-teton", "yosemite", "sequoia", "great-smoky-mountains", "rocky-mountain", "olympic", "mount-rainier", "shenandoah", "acadia", "cloud-peak-wilderness", "grand-mesa") else ""}">{lab}</a>'
        for s, lab in (("warm", "summer list"), ("shoulder", "spring/fall list"), ("cold", "winter list")))
    faq = [(f["q"], f["a"]) for f in cp.get("faq", [])]
    if not faq:
        faq = [(f"What is the best month to visit {sname}?", f"For hiking and camping weather, {', '.join(MONTH_NAMES[i] for i in bm)} score best at {d['hub']}, based on 10 years of weather data.")]
    faq_html, faq_schema = faq_block(faq)
    nearby = [n for n in cp.get("nearby", []) if n in DEST and n != slug][:3]
    if not nearby:
        nearby = [s for s in DEST if s != slug and DEST[s]["state"] == d["state"]][:3]
    rel_arts = [ARTS[a] for a in cp.get("related_articles", []) if a in ARTS]
    rel_arts += [a for a in ARTS.values() if slug in a.get("destinations", []) and a not in rel_arts]
    crumbs = [("Home", "/"), ("Destinations", "/destinations/"), (sname, path)]
    intro = cp.get("intro") or f"<p>{E(name)} in {E(d['state'])}. Here's when the weather is best for hiking and camping, month by month.</p>"
    best_time = cp.get("best_time") or f"Based on 10 years of weather data, {', '.join(MONTH_NAMES[i] for i in bm)} offer the most comfortable hiking and camping weather at {d['hub']}."
    toc_items = [("best-time", "Best time to visit"), ("weather", "Monthly weather"), ("forecast", "7-day forecast")]
    if seasons:
        toc_items.append(("seasons", "Season by season"))
    if hikes:
        toc_items.append(("hikes", "Hikes"))
    if camping:
        toc_items.append(("camping", "Camping"))
    if know:
        toc_items.append(("know-before", "Know before you go"))
    toc = '<nav class="toc"><h2>On this page</h2><ol>' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc_items) + '<li><a href="#faq">FAQ</a></li></ol></nav>'
    side_near = "".join(f'<li><a href="/destinations/{n}/">{E(DEST[n]["name"])}</a></li>' for n in nearby)
    side_arts = "".join(f'<li><a href="{a["path"]}">{E(a["h1"])}</a></li>' for a in rel_arts[:4])
    chips = "".join(f'<span class="glass-chip">{E(h)}</span>' for h in cp.get("highlights", [])[:5])
    hero_extra = f'<div class="hero-meta"><span class="glass-chip">☀️ Best: {" · ".join(MON3[i] for i in bm)}</span><span class="glass-chip">⛰️ {round(d["elev"] * 3.281):,} ft</span>{chips}</div>'
    body = (hero(E(f"Best time to visit {sname}"), E(f"{d['state']} · month-by-month weather, seasons, camping and a live forecast"), eyebrow="Destination guide",
                 photo="dest-" + slug, extra=hero_extra, crumbs=crumbs) +
            f"""<div class="wrap">
<div class="layout"><article class="prose">
<h2 id="best-time">Best time to visit</h2>
<p class="lead"><strong>{E(best_time)}</strong></p>
{stats}
{best_for}
{intro}
{climate_section(slug)}
<h2 id="forecast">7-day forecast and hike score</h2>
<div class="forecast" id="fc" data-name="{E(d['hub'] + ', ' + sname)}" data-lat="{d['lat']}" data-lon="{d['lon']}" data-elev="{d['elev']}"><p class="status">Loading forecast…</p></div>
<p class="small"><a href="/tools/trail-weather/?lat={d['lat']}&amp;lon={d['lon']}&amp;name={urllib.parse.quote(d['hub'])}">Open in the trail forecast tool</a> to check other trailheads.</p>
{seasons}
{hikes}
{camping}
{know}
<div class="callout tool">Packing for {E(sname)}? Start from a ready-made checklist: {pack_links}. Size your sleep system with the <a href="/tools/sleeping-bag-temperature/">sleeping bag guide</a>.</div>
{faq_html}
</article>
<aside class="no-print">{toc}
<div class="side-card"><h3>Nearby destinations</h3><ul>{side_near}</ul></div>
{f'<div class="side-card"><h3>Related guides</h3><ul>{side_arts}</ul></div>' if side_arts else ''}
<div class="side-card"><h3>Plan by month</h3><div class="chips">{"".join(f'<a class="chip {score_class(sc[i])}" href="/weather/{MONTHS[i]}/">{MON3[i]}</a>' for i in range(12))}</div></div>
</aside></div></div>
<script>document.addEventListener("DOMContentLoaded",function(){{var f=document.getElementById("fc");AO.renderForecast(f,{{name:f.dataset.name,lat:+f.dataset.lat,lon:+f.dataset.lon,elevation:+f.dataset.elev}});}});</script>""")
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
               "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": URL + path,
               "author": {"@type": "Organization", "name": AUTHOR["name"]},
               "publisher": {"@type": "Organization", "name": SITE["name"]},
               "about": {"@type": "TouristDestination", "name": name,
                         "geo": {"@type": "GeoCoordinates", "latitude": d["lat"], "longitude": d["lon"]}}},
              breadcrumbs_ld(crumbs), faq_schema]
    write(path, layout(path=path, title=title, description=desc, body=body, schema=schema, active="/destinations/", og_image=photo_src("dest-" + slug, 1280)))


def render_destinations_hub():
    by_state = sorted(DEST)
    cards = "".join(dest_card(s) for s in by_state)
    now = 10  # November is the next month when this launches; the JS picker defaults to the visitor's month
    body = (hero("When to go: national park weather guides",
                 "Month-by-month weather from 10 years of data, the best time to visit for hiking and camping, seasonal notes and a live forecast for each park.",
                 eyebrow="Destinations", photo="summit") +
            f"""<section class="block topo"><div class="wrap">
<div class="section-head"><div><span class="kicker">{len(DEST)} parks & wild places</span><h2>Pick your next trip</h2><p>The colored strip on each card runs January → December: <span class="chip good">Excellent</span> <span class="chip ok">Good</span> <span class="chip fair">Fair</span> <span class="chip poor">Poor</span> hiking weather.</p></div><a class="btn outline sm" href="/weather/">Where to go this month →</a></div>
<div class="grid g4 reveal-stagger">{cards}</div></div></section>""")
    write("/destinations/", layout(path="/destinations/", title="National Park Weather Guides: Best Time to Visit",
                                   description=f"When to visit {len(DEST)} popular national parks and wild places: monthly weather from 10 years of data, best months for hiking and camping, and live forecasts.",
                                   body=body, active="/destinations/"))


# --------------------------------------------------------------------------- weather (by month)
def month_ranking(mi):
    rows = []
    for s in DEST:
        m = CLIMATE[s]["months"][mi]
        rows.append((month_score(m), s, m))
    rows.sort(key=lambda r: -r[0])
    return rows


def render_weather_month(mi):
    mname = MONTH_NAMES[mi]
    path = f"/weather/{MONTHS[mi]}/"
    rows = month_ranking(mi)
    good = [r for r in rows if r[0] >= 60]
    li = "".join(rank_item(sc, s, m) for sc, s, m in rows)
    top3 = ", ".join(short_name(s) for _, s, _ in rows[:3])
    avoid = [short_name(s) for sc, s, _ in rows[-3:]]
    tabs = "".join(f'<a href="/weather/{MONTHS[i]}/"{" aria-current=page" if i == mi else ""}>{MON3[i]}</a>' for i in range(12))
    season = "cold" if mi in (11, 0, 1) else "warm" if mi in (5, 6, 7, 8) else "shoulder"
    intro = (f"Based on 10 years of weather data, the national parks with the best hiking and camping weather in {mname} are "
             f"<strong>{E(top3)}</strong>. {len(good)} of the {len(rows)} destinations we track score good or better this month; "
             f"{E(', '.join(avoid))} are the toughest bets on weather alone.")
    faq = [(f"What national park is best to visit in {mname}?",
            f"On weather alone, {short_name(rows[0][1])} scores highest in {mname} ({month_reason(rows[0][2])}). Check each park's guide for road closures, crowds and permits."),
           (f"Where is it warm in {mname}?",
            "Warmest highs this month: " + ", ".join(f"{short_name(s)} (~{round(m['high'])}°F)" for _, s, m in sorted(rows, key=lambda r: -r[2]['high'])[:3]) + "."),
           (f"Is {mname} a good time to go camping?",
            f"Depends where. {len(good)} of {len(rows)} parks we track have good or excellent camping weather in {mname}. Watch overnight lows: " +
            ", ".join(f"{short_name(s)} averages {round(m['low'])}°F" for _, s, m in sorted(rows, key=lambda r: r[2]['low'])[:2]) + " at night.")]
    faq_html, faq_schema = faq_block(faq)
    crumbs = [("Home", "/"), ("Weather", "/weather/"), (mname, path)]
    mphoto = {"cold": "snow-camp", "warm": "hero-day", "shoulder": "forest" if mi in (2, 3, 4) else "summit"}[season]
    body = (hero(E(f"Best national parks to visit in {mname}"), f"Ranked by hiking and camping weather from 10 years of data. Top pick: <strong>{E(short_name(rows[0][1]))}</strong>.",
                 eyebrow="Where to go by month", photo=mphoto, fx_modes="snow" if season == "cold" else None, crumbs=crumbs) +
            f"""<div class="wrap" style="margin-top:30px">
<div class="month-tabs">{tabs}</div>
<div class="read prose"><p class="lead">{intro}</p></div>
<ol class="rank reveal-stagger">{li}</ol>
<div class="read prose">
<p class="small muted">Scores rate average weather only — temperature, rain, snow and heat at each park's main visitor area. Seasonal roads, crowds and reservations matter too; each destination guide covers them.</p>
<div class="callout tool">Going in {mname}? Build a <a href="/tools/packing-list/?season={season}">{season.replace("shoulder", "spring/fall").replace("warm", "summer").replace("cold", "winter")} packing list</a>, and check the <a href="/tools/trail-weather/">7-day trail forecast</a> before you leave.</div>
{faq_html}</div></div>""")
    write(path, layout(path=path, title=f"Best National Parks to Visit in {mname} (Weather-Ranked)",
                       description=f"The best national parks to visit in {mname} for hiking and camping, ranked by 10 years of weather data: temperatures, rain, snow and heat.",
                       body=body, schema=[breadcrumbs_ld(crumbs), faq_schema], active="/weather/"))


def render_weather_hub():
    data = {s: {"n": DEST[s]["name"], "sc": place_scores(s), "p": photo_src("dest-" + s, 640) or "",
                "hi": [round(m["high"]) for m in CLIMATE[s]["months"]],
                "lo": [round(m["low"]) for m in CLIMATE[s]["months"]]} for s in DEST}
    tabs = "".join(f'<button type="button" data-m="{i}">{MON3[i]}</button>' for i in range(12))
    month_links = "".join(f'<a class="chip" href="/weather/{MONTHS[i]}/">Best parks in {MONTH_NAMES[i]}</a>' for i in range(12))
    body = (hero("Where to go hiking this month", f"Pick a month to rank {len(DEST)} national parks and wild places by hiking and camping weather — or check a live forecast for any trailhead.", eyebrow="Weather",
                 photo="stars", fx_modes="stars") +
            f"""<section class="block"><div class="wrap">
<div class="grid g2" style="align-items:start">
<div class="panel"><h2>Rank parks by month</h2><div class="month-tabs" id="mtabs">{tabs}</div>
<div class="seg" style="margin-bottom:12px"><label><input type="radio" name="pref" value="all" checked> Any weather</label><label><input type="radio" name="pref" value="warm"> I want warm</label><label><input type="radio" name="pref" value="cool"> Escape the heat</label></div>
<ol class="rank" id="mrank"></ol></div>
<div><div class="panel" style="background:var(--night);color:#e7efe9;border-color:transparent"><h2 style="color:#fff">📍 Parks near you</h2><p>Trip Finder uses your location (or any address) to rank parks by drive time and this month's weather.</p><a class="btn primary" href="/tools/trip-finder/">Open Trip Finder</a></div>
<div class="panel" style="margin-top:20px"><h2>Live forecast for any trailhead</h2><p>Get a 7-day forecast with a daily hike score and warnings for storms, heat, wind and freezing nights.</p><a class="btn primary" href="/tools/trail-weather/">Open the trail forecast</a></div>
<div class="panel" style="margin-top:20px"><h2>Monthly guides</h2><div class="chips">{month_links}</div></div>
<div class="panel" style="margin-top:20px"><h2>Weather tools</h2><ul><li><a href="/tools/sunrise-sunset/">Sunrise, sunset & golden hour</a></li><li><a href="/tools/feels-like/">Wind chill & heat index</a></li><li><a href="/tools/water-calculator/">Hiking water calculator</a></li><li><a href="/tools/sleeping-bag-temperature/">Sleeping bag temperature guide</a></li></ul></div></div>
</div></div></section>
<script>
(function(){{var D={json.dumps(data, separators=(",", ":"))};
var M={json.dumps(MON3)},F={json.dumps(MONTHS)},cur=new Date().getMonth();
function col(s){{return s>=75?"#23784a":s>=60?"#677516":s>=45?"#a3640b":"#b8412a"}}
function word(s){{return s>=75?"Excellent":s>=60?"Good":s>=45?"Fair":"Poor"}}
function draw(){{var pref=document.querySelector("input[name=pref]:checked").value;
var rows=Object.keys(D).map(function(k){{var d=D[k],s=d.sc[cur];if(pref==="warm")s+= (d.hi[cur]-70)*0.8;if(pref==="cool")s-=Math.max(0,d.hi[cur]-75)*1.5;return [Math.round(Math.max(0,Math.min(100,s))),k,d];}});
rows.sort(function(a,b){{return b[0]-a[0]}});
document.getElementById("mrank").innerHTML=rows.slice(0,10).map(function(r){{return "<li>"+(r[2].p?"<img class='thumb' src='"+r[2].p+"' alt='' loading='lazy'>":"")+"<div><a href='/destinations/"+r[1]+"/'>"+r[2].n+"</a><div class='why'>Avg high "+r[2].hi[cur]+"°F · low "+r[2].lo[cur]+"°F</div></div><span class='score-pill' style='background:"+col(r[0])+"'>"+r[0]+" · "+word(r[0])+"</span></li>"}}).join("")+"<li class='nothumb' style='grid-template-columns:1fr'><a href='/weather/"+F[cur]+"/'>See all {len(DEST)} for "+M[cur]+" →</a></li>";
Array.prototype.forEach.call(document.querySelectorAll("#mtabs button"),function(b){{b.classList.toggle("on",+b.dataset.m===cur)}});}}
document.getElementById("mtabs").addEventListener("click",function(e){{var b=e.target.closest("button");if(b){{cur=+b.dataset.m;draw();}}}});
Array.prototype.forEach.call(document.querySelectorAll("input[name=pref]"),function(r){{r.addEventListener("change",draw)}});
draw();}})();
</script>""")
    write("/weather/", layout(path="/weather/", title="Where to Go Hiking This Month: Park Weather by Month",
                              description="Find the best national parks to visit any month, ranked by 10 years of hiking and camping weather data, plus live trail forecasts with a hike score.",
                              body=body, active="/weather/"))


# --------------------------------------------------------------------------- guides hub
def render_guides():
    sections = ""
    for key, label in CATEGORIES.items():
        items = [a for a in ARTS.values() if a["category"] == key]
        if not items:
            continue
        sections += f'<h2 id="{key}" class="reveal">{E(label)}</h2><div class="grid g3 reveal-stagger">{"".join(article_card(a) for a in items)}</div>'
    chips = "".join(f'<a class="chip" href="#{k}">{E(v)}</a>' for k, v in CATEGORIES.items() if any(a["category"] == k for a in ARTS.values()))
    body = (hero("Camping & hiking guides", "Practical, specific how-tos for planning, packing and staying safe outside.", eyebrow="Guides", photo="forest") +
            f'<section class="block topo" style="padding-top:50px"><div class="wrap"><div class="chips" style="margin-bottom:10px">{chips}</div>{sections}</div></section>')
    write("/guides/", layout(path="/guides/", title="Camping & Hiking Guides",
                             description="Practical camping and hiking guides: beginner camping, campfire safety, scrambling, backpacking hygiene, car camping, gear and renting gear.",
                             body=body, active="/guides/"))


# --------------------------------------------------------------------------- gear
def render_gear():
    sections, nav = "", ""
    for anchor, label, note, guide, items in GEAR:
        nav += f'<a class="chip" href="#{anchor}">{E(label)}</a>'
        cards = "".join(
            f'<div class="gear-item"><h3>{E(n)}</h3><p>{E(t)}</p><a class="btn outline sm" href="{('https://www.amazon.com/dp/' + asin + '/?tag=' + SITE['amazon_tag']) if asin else amazon_search(n)}" rel="sponsored nofollow noopener" target="_blank">Check price on Amazon</a></div>'
            for n, asin, t in items)
        guide_link = f' <a href="{guide}">Read the guide →</a>' if guide else ""
        sections += f'<h2 id="{anchor}" class="reveal">{E(label)}</h2><p class="muted">{E(note)}{guide_link}</p><div class="gear-list reveal-stagger">{cards}</div>'
    body = (hero("Gear picks", "The gear our guides point to, grouped by what it's for — plus the tools to size it right.", eyebrow="Gear", photo="art-best-hiking-black-friday-deals") +
            f"""<section class="block"><div class="wrap">
<p class="disclosure">Links on this page are Amazon affiliate links: if you buy through them, Arrive Outdoors may earn a commission at no extra cost to you. We don't accept payment for placement. <a href="/affiliate-disclosure/">Details</a>.</p>
<div class="chips" style="margin:10px 0 6px">{nav}</div>
{sections}
<div class="callout tool" style="margin-top:32px">Not sure you'll use it enough to buy? Run the numbers with the <a href="/tools/rent-vs-buy/">rent vs buy calculator</a>, or see <a href="/rent-camping-gear/">where to rent camping gear</a>.</div>
</div></section>""")
    write("/gear/", layout(path="/gear/", title="Camping & Hiking Gear Picks",
                           description="Camping and hiking gear our guides recommend — packs, sleep systems, water filters, footwear, safety and camera gear — with tools to size it right.",
                           body=body, active="/gear/"))


# --------------------------------------------------------------------------- home
def render_home():
    feat_tools = ["trip-finder", "packing-list", "trail-weather", "hiking-time-calculator", "water-calculator", "sleeping-bag-temperature"]
    month = 10  # November
    rank = month_ranking(month)[:5]
    feat_dest = ["yosemite", "zion", "grand-teton", "glacier", "great-smoky-mountains", "arches", "acadia", "joshua-tree"]
    feat_arts = [ARTS[s] for s in ["honda-crv-camper", "blogs/the-outdoor-traveler/camping-101-a-guide-for-the-first-time-camper",
                                    "class-3-scramble", "cold-weather-camping", "how-to-put-out-a-fire", "rent-camping-gear"] if s in ARTS]
    hero_extra = ('<div class="btns"><a class="btn primary" href="/tools/packing-list/">Build your packing list</a>'
                  '<a class="btn ghost" href="/tools/trip-finder/">📍 Find parks near me</a></div>'
                  f'<div class="hero-meta"><a class="glass-chip" href="/tools/">🧭 {len(TOOL_LIST)} free tools</a><a class="glass-chip" href="/destinations/">⛰️ {len(DEST)} park weather guides</a>'
                  '<a class="glass-chip" href="/tools/trail-weather/">🌤️ Live trail forecasts</a></div>')
    body = (hero("Plan it right. Pack it light. Arrive ready.",
                 "Free trip-planning tools, month-by-month weather for national parks, and camping advice that actually helps — everything you need before you hit the trail.",
                 eyebrow="Camping & hiking, planned properly", full=True, split=True, photo="hero-night", fx_modes="stars fireflies",
                 extra=hero_extra, below="var(--night)").replace("</div><div class=\"ridges\"", '</div><a class="scroll-cue" href="#start"><i></i>Explore</a><div class="ridges"', 1) +
            f"""<section class="block dark" id="start" style="padding-top:40px">
<div class="wrap">
<div class="stats-strip reveal" style="margin-bottom:80px">
<div><b data-count="{len(TOOL_LIST)}">{len(TOOL_LIST)}</b><span>free planning tools</span></div>
<div><b data-count="{len(DEST)}">{len(DEST)}</b><span>park weather guides</span></div>
<div><b data-count="10">10</b><span>years of daily weather data</span></div>
<div><b data-count="{len(ARTS)}">{len(ARTS)}</b><span>practical guides</span></div>
</div>
<div class="section-head"><div><span class="kicker">Free tools</span><h2>Answers before you leave the driveway</h2><p style="color:rgba(255,255,255,.65)">What to pack, how long it'll take, how much water, how warm a bag — and whether the weather will cooperate.</p></div><a class="link" style="color:var(--amber)" href="/tools/">All {len(TOOL_LIST)} tools →</a></div>
<div class="grid g3 reveal-stagger">{"".join(tool_card(t) for t in feat_tools)}</div>
</div></section>
<section class="block topo"><div class="wrap">
<div class="feature">
<div class="photo reveal">{picture("summit", sizes="(max-width:900px) 100vw, 600px")}<div class="float"><span class="glass-chip">📅 Updated for November</span></div></div>
<div class="reveal">
<span class="kicker">Where to go this month</span>
<h2 style="margin-top:0">Best parks for hiking weather in November</h2>
<p class="muted">Ranked from 10 years of daily weather at each park's main visitor area.</p>
<ol class="rank">{"".join(rank_item(sc, s, m) for sc, s, m in rank)}</ol>
<div class="btns"><a class="btn primary" href="/weather/november/">See all {len(DEST)} for November</a><a class="btn outline" href="/weather/">Pick another month</a></div>
</div></div></div></section>
<section class="block alt"><div class="wrap">
<div class="section-head"><div><span class="kicker">Destination guides</span><h2>Know exactly when to go</h2><p>Month-by-month weather, seasonal road openings, camping and a live forecast for each park.</p></div><a class="link" href="/destinations/">All {len(DEST)} destinations →</a></div>
<div class="grid g4 reveal-stagger">{"".join(dest_card(s) for s in feat_dest)}</div>
</div></section>
<section class="block"><div class="wrap">
<div class="feature" style="grid-template-columns:1fr 1.1fr">
<div class="reveal">
<span class="kicker">Live trail forecast</span>
<h2 style="margin-top:0">Is tomorrow a good day to hike?</h2>
<p>Search any trailhead for a 7-day forecast scored for hiking — with the warnings that matter on the trail.</p>
<ul class="check-list"><li>Daily 0–100 hike score you can compare at a glance</li><li>Thunderstorm, heat, wind and snow warnings</li><li>Freezing level for high-country routes</li><li>Sunrise and sunset so you can plan your turnaround</li></ul>
<div class="btns"><a class="btn primary" href="/tools/trail-weather/">Check a trailhead</a></div>
</div>
<div class="photo reveal">{picture("trail", sizes="(max-width:900px) 100vw, 640px")}<div class="float"><span class="glass-chip">⛅ Hike score: 86 · Great</span></div></div>
</div></div></section>
<section class="block topo"><div class="wrap">
<div class="section-head"><div><span class="kicker">Guides</span><h2>Popular guides</h2></div><a class="link" href="/guides/">All guides →</a></div>
<div class="grid g3 reveal-stagger">{"".join(article_card(a) for a in feat_arts)}</div></div></section>
<section class="block tight"><div class="wrap"><div class="band-cta reveal">
<canvas data-fx="embers" aria-hidden="true"></canvas><div class="glow"></div>
<div><span class="kicker" style="color:var(--amber)">Since 2019</span><h2>Renting gear for a park trip?</h2><p>Arrive Outdoors started in 2019 as a camping gear rental service for national and state park trips. The rental service has ended, but our guide covers where to rent today, what to check, and when buying makes more sense.</p></div>
<div class="btns" style="justify-content:flex-end"><a class="btn primary" href="/rent-camping-gear/">Where to rent camping gear</a><a class="btn ghost" href="/tools/rent-vs-buy/">Rent vs buy calculator</a></div>
</div></div></section>""")
    schema = [{"@context": "https://schema.org", "@type": "Organization", "name": SITE["name"], "url": URL,
               "logo": URL + "/assets/icons/icon-512.png", "email": SITE["email"]},
              {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": URL}]
    write("/", layout(path="/", title="Arrive Outdoors — Camping & Hiking Tools, Park Weather Guides",
                      description=SITE["description"], body=body, schema=schema))


def render_credits():
    rows = ""
    for k, p in sorted(PHOTOS.items()):
        who = p.get("photographer") or "Pexels contributor"
        rows += (f'<tr><td>{E(p.get("alt", k))}</td><td>{E(who)}</td>'
                 f'<td>{f"""<a href="{E(p["page"])}" rel="nofollow noopener">Pexels</a>""" if p.get("page") else "Pexels"}</td></tr>')
    simple_page("/photo-credits/", "Photo Credits", "Credits for the photographs used on Arrive Outdoors, sourced from Pexels under the Pexels license.",
                "Photo credits", photo="stars", content=f"""
<p class="lead">The photographs on this site come from <a href="https://www.pexels.com/">Pexels</a> and are used under the <a href="https://www.pexels.com/license/">Pexels license</a>. Thank you to the photographers who share their work.</p>
<div class="table-wrap"><table><thead><tr><th>Photo</th><th>Photographer</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>""")


# --------------------------------------------------------------------------- static pages
def simple_page(path, title, description, h1, content, lead="", noindex=False, active=None, photo="forest", fx_modes=None):
    crumbs = [("Home", "/"), (h1, path)]
    body = hero(E(h1), lead, small=True, photo=photo, fx_modes=fx_modes, crumbs=crumbs) + f'<div class="wrap" style="margin-top:40px"><div class="read prose">{content}</div></div>'
    write(path, layout(path=path, title=title, description=description, body=body, noindex=noindex,
                       schema=[breadcrumbs_ld(crumbs)], active=active))


def render_static():
    simple_page("/about/", "About Arrive Outdoors", "Arrive Outdoors is an independent camping and hiking resource with free trip-planning tools and park weather guides. Here's our story and how we work.",
                "About Arrive Outdoors", photo="campfire", fx_modes="embers", content=f"""
<p class="lead">Arrive Outdoors helps you plan camping and hiking trips: when to go, what to pack, and how to stay comfortable and safe once you're out there.</p>
<h2 id="story">Our story</h2>
<p>Arrive Outdoors launched in 2019 as a camping gear rental service. The idea was simple — rent quality tents, sleeping bags and packs for a national or state park trip instead of buying gear you'd use once a year — and it worked with park partners along the way.</p>
<p><strong>That rental service has ended, and Arrive Outdoors no longer rents gear.</strong> If you're looking to rent, our guide to <a href="/rent-camping-gear/">where to rent camping gear</a> covers the options available today, and the <a href="/tools/rent-vs-buy/">rent vs buy calculator</a> helps you decide.</p>
<p>Today arriveoutdoors.com is an independent planning resource built around three things:</p>
<ul><li><strong><a href="/tools/">Free tools</a></strong> — packing lists, trail forecasts with a hike score, hiking time, water, sleeping bag and backpack calculators.</li>
<li><strong><a href="/destinations/">Destination weather guides</a></strong> — month-by-month conditions for popular parks built from 10 years of weather data, and a <a href="/weather/">where-to-go-by-month</a> ranking.</li>
<li><strong><a href="/guides/">Practical guides</a></strong> — specific, checkable advice on camping, hiking, backpacking and safety.</li></ul>
<h2 id="standards">How we work</h2>
<ul><li>Safety guidance follows the land agencies and health authorities (National Park Service, U.S. Forest Service, CDC, Leave No Trace). When conditions or rules change often — fees, permits, fire restrictions — we point you to the official source instead of quoting numbers that go stale.</li>
<li>Weather data comes from Open-Meteo's historical and forecast APIs. Each tool page explains its formula.</li>
<li>We review guides each season and note the last update on every page. If something's wrong or out of date, <a href="/contact/">tell us</a> and we'll fix it.</li></ul>
<h2 id="money">How we make money</h2>
<p>Some guides link to products on Amazon and other retailers. If you buy through those links, we may earn a commission at no extra cost to you. Nobody pays to be included, and our tools are free. <a href="/affiliate-disclosure/">Read the full disclosure</a>.</p>
<h2 id="contact">Get in touch</h2>
<p>Questions, corrections or partnership inquiries: <a href="/contact/">contact us</a> or email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>""")

    simple_page("/affiliate-disclosure/", "Affiliate Disclosure", "How Arrive Outdoors uses affiliate links, including the Amazon Associates program.",
                "Affiliate disclosure", """
<p>Arrive Outdoors is reader-supported. Some links on this site are affiliate links, which means that if you click one and make a purchase, we may earn a commission. It costs you nothing extra.</p>
<p><strong>Arrive Outdoors is a participant in the Amazon Services LLC Associates Program</strong>, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate, we earn from qualifying purchases.</p>
<h2 id="independence">Our independence</h2>
<ul><li>Products are included because they fit what the guide is about — never because a brand paid for placement.</li>
<li>We don't publish sponsored posts or sell links.</li>
<li>Affiliate links are marked as sponsored and every page that contains them says so near the top.</li>
<li>Our tools are free and don't require you to buy anything.</li></ul>
<p>Questions? <a href="/contact/">Contact us</a>.</p>""")

    simple_page("/privacy-policy/", "Privacy Policy", "Privacy policy for arriveoutdoors.com: what data we collect, cookies, analytics, affiliate links and your choices.",
                "Privacy policy", f"""
<p><em>Last updated: {fmt_date(TODAY)}</em></p>
<h2 id="collect">What we collect</h2>
<ul><li><strong>Analytics:</strong> we use Google Analytics (Google tag) to understand how visitors use the site — pages viewed, approximate location, device and browser. Google may set cookies to do this. See <a href="https://policies.google.com/technologies/partner-sites">how Google uses data from sites that use its services</a>.</li>
<li><strong>Contact form:</strong> if you message us, we receive your name, email and message, and use them only to reply.</li>
<li><strong>Tools:</strong> our tools run in your browser. Packing-list ticks and your last searched place are stored in your browser's local storage on your device, not on our servers. If you use "Use my location", your coordinates are used in your browser to request a forecast from Open-Meteo and are not stored by us.</li></ul>
<h2 id="third-parties">Third parties</h2>
<p>Weather searches send the place name or coordinates to <a href="https://open-meteo.com/">Open-Meteo</a> to return results. Addresses typed into Trip Finder are sent to <a href="https://osmfoundation.org/wiki/Privacy_Policy">OpenStreetMap's Nominatim geocoder</a> to find their coordinates; "Use my location" coordinates stay in your browser (saved in local storage so the tool remembers your starting point). Affiliate links (for example to Amazon) may set cookies on the retailer's site to attribute purchases.</p>
<h2 id="choices">Your choices</h2>
<p>You can block or delete cookies in your browser settings, use the <a href="https://tools.google.com/dlpage/gaoptout">Google Analytics opt-out add-on</a>, and clear local storage to remove saved tool data. To ask about or delete data you've sent us, email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
<h2 id="changes">Changes</h2><p>We'll update this page if our practices change.</p>""")

    simple_page("/terms-of-use/", "Terms of Use", "Terms of use for arriveoutdoors.com, including the outdoor safety disclaimer for our guides and tools.",
                "Terms of use", f"""
<p><em>Last updated: {fmt_date(TODAY)}</em></p>
<h2 id="safety">Outdoor safety disclaimer</h2>
<p>Hiking, camping, scrambling and other outdoor activities carry real risk of injury or death. Our guides, weather data, scores and calculators are general information to help you plan — they are estimates, not guarantees, and they don't replace your own judgment, training, current official forecasts, park alerts or professional instruction. Conditions change quickly. You are responsible for your own safety and decisions.</p>
<h2 id="accuracy">Accuracy</h2>
<p>We work to keep information accurate and current, but rules, fees, closures and conditions change. Always confirm with the managing agency (for example the National Park Service or U.S. Forest Service) before you go.</p>
<h2 id="use">Using this site</h2>
<p>You may use the site and tools for personal, non-commercial trip planning. Don't copy or republish our content without permission. Links to other sites are provided for convenience; we're not responsible for their content.</p>
<h2 id="contact">Contact</h2><p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>""")

    # 404
    page404 = layout(path="/404.html", title="Page not found", description="This page doesn't exist. Find camping tools, park weather guides and hiking guides on Arrive Outdoors.", noindex=True, sitemap=False,
                     body=hero("Off trail", "That page doesn't exist — it may have moved when we rebuilt the site.", small=True, photo="stars", fx_modes="stars fireflies") +
                     '<div class="wrap"><div class="read prose" style="padding:30px 0"><p>Try one of these:</p><ul>'
                     '<li><a href="/">Home</a></li><li><a href="/tools/">Free camping & hiking tools</a></li><li><a href="/destinations/">Park weather guides</a></li>'
                     '<li><a href="/guides/">All guides</a></li><li><a href="/tools/trail-weather/">Trail forecast</a></li></ul></div></div>')
    write("/404.html", page404.replace('<link rel="canonical" href="https://arriveoutdoors.com/404.html">', ""))


def render_contact():
    path = "/contact/"
    crumbs = [("Home", "/"), ("Contact", path)]
    form = f"""<?php
$sent = false; $error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {{
    $name = trim(str_replace(["\\r", "\\n"], ' ', $_POST['name'] ?? ''));
    $email = trim($_POST['email'] ?? '');
    $msg = trim($_POST['message'] ?? '');
    $trap = $_POST['website'] ?? '';
    if ($trap !== '') {{ $sent = true; }}
    elseif ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($msg) < 10) {{ $error = 'Please add your name, a valid email and a message.'; }}
    elseif (strlen($msg) > 5000) {{ $error = 'Please keep your message under 5,000 characters.'; }}
    else {{
        $body = "Name: $name\\nEmail: $email\\n\\n$msg\\n";
        $headers = "From: Arrive Outdoors <{SITE['email']}>\\r\\nReply-To: $email\\r\\nContent-Type: text/plain; charset=UTF-8";
        $sent = @mail('{SITE['email']}', 'Contact form: ' . mb_substr($name, 0, 60), $body, $headers);
        if (!$sent) {{ $error = 'Sorry, the message could not be sent. Please email us directly.'; }}
    }}
}}
?>"""
    content = f"""<p class="lead">Questions about a guide, a correction, or a partnership idea? We read everything.</p>
<?php if ($sent): ?><div class="callout tip"><strong>Thanks!</strong> Your message is on its way. We usually reply within a few days.</div>
<?php else: ?>
<?php if ($error): ?><div class="callout warn"><?php echo htmlspecialchars($error); ?></div><?php endif; ?>
<form method="post" class="panel" action="/contact/">
<div class="field"><label for="name">Name</label><input type="text" id="name" name="name" required maxlength="100" value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>"></div>
<div class="field"><label for="email">Email</label><input type="text" id="email" name="email" required maxlength="200" inputmode="email" value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>"></div>
<div class="field" style="position:absolute;left:-9999px" aria-hidden="true"><label for="website">Website</label><input type="text" id="website" name="website" tabindex="-1" autocomplete="off"></div>
<div class="field"><label for="message">Message</label><textarea id="message" name="message" rows="7" required maxlength="5000"><?php echo htmlspecialchars($_POST['message'] ?? ''); ?></textarea></div>
<button class="btn primary" type="submit">Send message</button>
</form>
<?php endif; ?>
<p>Or email <a href="mailto:{SITE['email']}">{SITE['email']}</a>. Note: Arrive Outdoors no longer rents gear — see <a href="/rent-camping-gear/">where to rent camping gear</a>.</p>"""
    body = hero("Contact us", "", small=True, photo="trail", crumbs=crumbs) + f'<div class="wrap" style="margin-top:40px"><div class="read prose">{content}</div></div>'
    page = layout(path=path, title="Contact Arrive Outdoors", description="Contact Arrive Outdoors with questions, corrections or partnership inquiries.",
                  body=body, schema=[breadcrumbs_ld(crumbs)])
    fp = OUT + "/contact/index.php"
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(form + "\n" + page)


# --------------------------------------------------------------------------- server files
def rx(path):
    p = path.strip("/")
    return "^" + re.escape(p).replace("\\-", "-").replace("\\/", "/") + "/?$"


def render_server_files():
    lines = ["# Arrive Outdoors static site (generated by build.py — edit siteconfig.py, not this file)",
             "DirectoryIndex index.html index.php",
             "Options -Indexes",
             "ErrorDocument 404 /404.html",
             "ErrorDocument 410 /404.html",
             "AddType image/x-icon .ico",
             "AddType application/manifest+json .webmanifest",
             "",
             "<IfModule mod_headers.c>",
             '  Header always set X-Content-Type-Options "nosniff"',
             '  Header always set Referrer-Policy "strict-origin-when-cross-origin"',
             '  Header always set X-Frame-Options "SAMEORIGIN"',
             "</IfModule>",
             "<IfModule mod_expires.c>",
             "  ExpiresActive on",
             "  ExpiresByType text/css A31536000",
             "  ExpiresByType application/javascript A31536000",
             "  ExpiresByType text/javascript A31536000",
             "  ExpiresByType image/webp A31536000",
             "  ExpiresByType image/png A31536000",
             "  ExpiresByType image/svg+xml A31536000",
             "  ExpiresByType image/x-icon A2592000",
             "  ExpiresByType text/html A600",
             "</IfModule>",
             "",
             "RewriteEngine On",
             "RewriteBase /",
             "# Canonical host: https://arriveoutdoors.com",
             "RewriteCond %{HTTP_HOST} ^www\\.arriveoutdoors\\.com$ [NC]",
             "RewriteRule ^(.*)$ https://arriveoutdoors.com/$1 [R=301,L]",
             "RewriteCond %{HTTPS} !=on",
             "RewriteCond %{HTTP:X-Forwarded-Proto} !=https",
             "RewriteRule ^(.*)$ https://arriveoutdoors.com/$1 [R=301,L]",
             "",
             "# Scheduled-release packs are applied by cron, never served directly",
             "RewriteRule ^_releases(/|$) - [F,L]",
             "",
             "# Scheduled articles not yet published (removed from this list on their release date)"] + [
             f"RewriteRule ^{k}(/.*)?$ - [R=404,L]" for k in sorted(ARTS_ALL) if k not in ARTS] + [
             "",
             "# Removed content (410 Gone)"]
    for p in GONE:
        lines.append(f"RewriteRule {rx(p)} - [G,L]")
    lines += ["", "# Legacy URLs → new pages (301)"]
    for old, (new, _why) in REDIRECTS.items():
        lines.append(f"RewriteRule {rx(old)} {new} [R=301,L,NE,QSD]")
    lines += ["", "# Catch-alls for old WordPress / Shopify URL patterns",
              "RewriteRule ^products/.+$ /gear/ [R=301,L,QSD]",
              "RewriteRule ^group/.+$ /gear/ [R=301,L,QSD]",
              "RewriteRule ^collections(/.*)?$ /gear/ [R=301,L,QSD]",
              "RewriteRule ^pages/.+$ /destinations/ [R=301,L,QSD]",
              "RewriteRule ^blogs/(?!the-outdoor-traveler/camping-101-a-guide-for-the-first-time-camper).+$ /guides/ [R=301,L,QSD]",
              "RewriteRule ^(category|tag)/.+$ /guides/ [R=301,L,QSD]",
              "RewriteRule ^author/.+$ /about/ [R=301,L,QSD]",
              "RewriteRule ^20[0-9]{2}/.*$ /guides/ [R=301,L,QSD]",
              "RewriteRule ^(comments/)?feed/?$ /guides/ [R=301,L,QSD]",
              "RewriteRule ^(.+)/feed/?$ /$1/ [R=301,L,QSD]",
              "RewriteRule ^(.+)/amp/?$ /$1/ [R=301,L,QSD]",
              "",
              "# Anything else that isn't a real file or folder gets the 404 page",
              "RewriteCond %{REQUEST_FILENAME} !-f",
              "RewriteCond %{REQUEST_FILENAME} !-d",
              "RewriteRule . - [R=404,L]",
              ""]
    write("/.htaccess", "\n".join(lines))
    write("/index.php", "<?php\n// Static site: serve the homepage; anything else routed here is a 404.\n"
                        "$p = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');\n"
                        "if ($p === '/' || $p === '/index.php') { header('Content-Type: text/html; charset=utf-8'); readfile(__DIR__ . '/index.html'); exit; }\n"
                        "http_response_code(404); header('Content-Type: text/html; charset=utf-8'); readfile(__DIR__ . '/404.html');\n")
    write("/robots.txt", f"User-agent: *\nDisallow: /wp-admin/\nAllow: /wp-admin/admin-ajax.php\n\nSitemap: {URL}/sitemap.xml\n")
    write("/ads.txt", "google.com, pub-3886800648957674, DIRECT, f08c47fec0942fa0\n")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, lm in sorted(set(SITEMAP), key=lambda x: (x[0] != "/", x[0])):
        sm.append(f"<url><loc>{URL}{p}</loc><lastmod>{lm}</lastmod></url>")
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    # Old Yoast sitemap URLs point to the new one
    for old in ("/sitemap_index.xml", "/post-sitemap.xml", "/page-sitemap.xml", "/products-sitemap.xml", "/category-sitemap.xml", "/group-sitemap.xml"):
        write(old, open(OUT + "/sitemap.xml").read())
    llms = [f"# {SITE['name']}", "", f"> {SITE['description']}", "", "## Tools"]
    llms += [f"- [{n}]({URL}/tools/{s}/): {d}" for s, n, d, _ in TOOL_LIST]
    llms += ["", "## Destination weather guides"] + [f"- [{d['name']}]({URL}/destinations/{s}/)" for s, d in DEST.items()]
    llms += ["", "## Guides"] + [f"- [{a['h1']}]({URL}{a['path']}): {a.get('summary', '')}" for a in ARTS.values()]
    write("/llms.txt", "\n".join(llms) + "\n")
    write("/site.webmanifest", json.dumps({"name": SITE["name"], "short_name": "Arrive", "start_url": "/", "display": "standalone",
                                           "background_color": "#fbfaf6", "theme_color": "#07130f",
                                           "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                                                     {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                                                     {"src": "/assets/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}))
    write("/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -8 46 46"><rect x="-4" y="-8" width="46" height="46" rx="9" fill="#07130f"/>'
                          '<path d="M2 28 14 6l6 10 4-6 12 18z" fill="#86a86b"/><path d="M14 6l3.4 6.2-2.2-1.4-2.4 2.6-1.6-1.6zM24 10l2.6 3.9-1.6-.8-1.6 1.6-1.2-1.2z" fill="#fff"/>'
                          '<path d="M10 28l8-9 5 5 4-3 9 7z" fill="#ff6a2b"/></svg>')
    for f in ("favicon.ico", "apple-touch-icon.png"):
        shutil.copy(os.path.join(ROOT, "assets", "icons", f), os.path.join(OUT, f))


def copy_assets():
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("logo-old.webp", "photos-src"))
    src_icon = os.path.join(ROOT, "assets", "img", "icon-old.webp")
    shutil.copy(src_icon, os.path.join(OUT, "assets", "img", "icon-192.webp"))


# --------------------------------------------------------------------------- main
def set_build_date(d):
    """Make only articles published on or before d live; strip links to the rest."""
    global ARTS, UNPUBLISHED_RX, BUILD_DATE
    BUILD_DATE = d
    ARTS = {k: v for k, v in ARTS_ALL.items() if v["published"] <= d}
    hidden = [k for k in ARTS_ALL if k not in ARTS]
    UNPUBLISHED_RX = (re.compile(r'<a [^>]*href="/(?:' + "|".join(re.escape(h) for h in hidden) + r')/(?:#[^"]*)?"[^>]*>(.*?)</a>', re.S)
                      if hidden else None)


def build_site(out, d, assets=True):
    global OUT, SITEMAP
    OUT = out
    SITEMAP = []
    set_build_date(d)
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    if assets:
        copy_assets()
    render_home()
    for a in ARTS.values():
        render_article(a)
    render_guides()
    render_tools_hub()
    for t in TOOL_LIST:
        render_tool(*t)
    render_destinations_hub()
    for s in DEST:
        render_destination(s)
    render_weather_hub()
    for i in range(12):
        render_weather_month(i)
    render_gear()
    render_static()
    render_credits()
    render_contact()
    SITEMAP.append(("/contact/", TODAY))
    render_server_files()


PUBLISH_PHP = """<?php
// Scheduled publishing for the static site. Run daily by a Hostinger cron job:
//   php /home/u401386392/domains/arriveoutdoors.com/public_html/_releases/publish.php
// Each _releases/YYYY-MM-DD/ folder holds only the files that change on that date
// (the new article page plus the hub pages, sitemap and related links that list it).
// Folders whose date has arrived are copied into the site root once, in date order.
$rel = __DIR__; $root = dirname($rel); $log = $rel . '/applied.txt';
$applied = file_exists($log) ? file($log, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) : [];
$today = (new DateTime('now', new DateTimeZone('America/Los_Angeles')))->format('Y-m-d');
foreach (glob($rel . '/20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]', GLOB_ONLYDIR) as $dir) {
    $d = basename($dir);
    if ($d > $today || in_array($d, $applied, true)) continue;
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS));
    $n = 0;
    foreach ($it as $f) {
        if ($f->getFilename() === '.htaccess') continue;               // pack-folder guard file, not content
        $rel_path = substr($f->getPathname(), strlen($dir));
        if ($f->getFilename() === '_htaccess') $rel_path = substr($rel_path, 0, -9) . '.htaccess';
        $target = $root . $rel_path;
        if (!is_dir(dirname($target))) mkdir(dirname($target), 0755, true);
        if (copy($f->getPathname(), $target)) $n++;
    }
    file_put_contents($log, $d . PHP_EOL, FILE_APPEND);
    echo "applied $d ($n files)\n";
}
"""


def snapshot(out):
    files = {}
    for dp, _, fs in os.walk(out):
        if os.sep + "assets" in dp or os.sep + "_releases" in dp:
            continue
        for f in fs:
            fp = os.path.join(dp, f)
            files[fp[len(out):]] = open(fp, "rb").read()
    return files


def main():
    main_out = os.path.join(ROOT, "public")
    build_site(main_out, BUILD_DATE)
    live = len(ARTS)
    pages = len(set(SITEMAP))
    # Release packs for scheduled articles: only files that differ from the previous state
    future = sorted({a["published"] for a in ARTS_ALL.values() if a["published"] > BUILD_DATE})
    prev = snapshot(main_out)
    rel_root = os.path.join(main_out, "_releases")
    tmp = os.path.join(ROOT, ".release-tmp")
    for d in future:
        build_site(tmp, d, assets=False)
        cur = snapshot(tmp)
        changed = {k: v for k, v in cur.items() if prev.get(k) != v}
        for k, v in changed.items():
            # never place a live .htaccess inside a pack (the server would apply it to the pack folder)
            fp = os.path.join(rel_root, d) + (k[:-len(".htaccess")] + "_htaccess" if k.endswith("/.htaccess") else k)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "wb").write(v)
        prev.update(cur)
        print(f"  release {d}: {len(changed)} files")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    if future:
        open(os.path.join(rel_root, "publish.php"), "w").write(PUBLISH_PHP)
        deny = "Require all denied\n"
        open(os.path.join(rel_root, ".htaccess"), "w").write(deny)
        for d in future:  # guard each pack folder too
            open(os.path.join(rel_root, d, ".htaccess"), "w").write(deny)
    n = sum(len(f) for _, _, f in os.walk(main_out))
    print(f"built {pages} indexable pages, {live} live articles ({len(ARTS_ALL) - live} scheduled), {n} files → public/")


if __name__ == "__main__":
    main()
