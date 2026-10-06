#!/usr/bin/env python3
"""Static site generator for renternews.net.

Renders the whole news site into ./public from:
  content/legacy_posts.json   the 28 original WordPress articles (URLs kept 1:1)
  content/legacy_pages.json   the original WordPress pages (about, FAQ, legal...)
  content/articles/*.json     newer articles (drop a JSON file in, rebuild)
  content/geo.json            city -> [lat, lon] cache for the incident map
  static/                     copied verbatim (old /wp-content/uploads, assets)

    python3 build.py && python3 validate.py

Standard library only, except tools/covers.py (Pillow), which build.py calls to
draw a cover image for any new article that does not have one yet.
"""

import glob
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://renternews.net"
SITE = "Renter News"
TAGLINE = "Apartment & Renter News"
EMAIL = "info@renternews.net"
LOGO = "/wp-content/uploads/2025/08/Renter-News-Logo.webp"
ICON = "/wp-content/uploads/2025/08/cropped-Renter-News-Site-Icon"
DEFAULT_OG = "/assets/img/og-default.webp"
AUTHOR = {"name": "Renter News Staff", "path": "/news/author/renter-news-staff/"}
PER_PAGE = 24
NOW = datetime.now(timezone.utc)

# Partner offers carried over from the WordPress sidebar.
OFFERS = {
    "insurance": "https://e.customeriomail.com/e/c/eyJlbWFpbF9pZCI6ImRnVGlxd29BQUtNMW9qVUJsSW93aWM5TTZxZHZRSUhnMUU1ciIsImhyZWYiOiJodHRwczovL2dvLmxlbW9uYWRlLmNvbS92aXNpdC8_YnRhPTM1NDUyXHUwMDI2YnJhbmQ9cmVudCIsImludGVybmFsIjoiZTJhYjBhMDBhMjM1YTMzNSIsImxpbmtfaWQiOjEwfQ/66d296e7a577c0de131fa8ddd4fa136354829e88c72535c36475cfdfd7c4d65e",
    "credit": "https://www.pav04trk.com/CBS8TP/K9TM4Q/?source_id=tx_rising",
}

CATS = {
    "fire":           {"name": "Fire",           "color": "#e4572e", "icon": "flame",
                       "blurb": "Apartment and multifamily fires across the US: what happened, who was displaced, and what renters can learn from it."},
    "safety":         {"name": "Safety",         "color": "#f08c00", "icon": "shield",
                       "blurb": "Building emergencies, hazards and the safety habits that protect renters and their neighbors."},
    "rent-prices":    {"name": "Rent & Market",  "color": "#0f9d8a", "icon": "chart",
                       "blurb": "Rent prices, vacancy, new supply and the market data that shapes what you pay."},
    "housing-policy": {"name": "Housing Policy", "color": "#5b5fc7", "icon": "landmark",
                       "blurb": "Rent caps, eviction rules, vouchers and the laws and programs that affect renters."},
    "tenant-rights":  {"name": "Tenant Rights",  "color": "#1f6fb2", "icon": "scale",
                       "blurb": "Court rulings, enforcement actions and explainers on what tenants are entitled to."},
    "guides":         {"name": "Renter Guides",  "color": "#b8860b", "icon": "book",
                       "blurb": "Practical, sourced how-tos for renters: insurance, deposits, repairs, scams and more."},
}

NAV = [
    ("News", "/news/"),
    ("Fire", "/news/category/fire/"),
    ("Rent & Market", "/news/category/rent-prices/"),
    ("Tenant Rights", "/news/category/tenant-rights/"),
    ("Guides", "/news/category/guides/"),
    ("Tools", "/tools/"),
    ("Fire Map", "/fire-map/"),
    ("Weather", "/weather/"),
]

TOOLS = [
    {"slug": "rent-affordability-calculator", "name": "Rent Affordability Calculator", "icon": "wallet",
     "short": "How much rent can you afford?",
     "desc": "Find a comfortable rent from your income and debts using the 30% rule, the 50/30/20 budget and the 40x landlord income test."},
    {"slug": "rent-split-calculator", "name": "Roommate Rent Split Calculator", "icon": "users",
     "short": "Split rent fairly with roommates",
     "desc": "Split rent and utilities evenly, by room size or by income, for up to six roommates, and share the result."},
    {"slug": "rent-increase-calculator", "name": "Rent Increase Calculator", "icon": "trend",
     "short": "What does your increase really cost?",
     "desc": "Turn a renewal offer into a percentage, a monthly and a yearly cost, and compare it with a cap you enter."},
    {"slug": "moving-cost-calculator", "name": "Move-In Cost Calculator", "icon": "truck",
     "short": "Total cash needed to move",
     "desc": "Add up deposit, first and last month, fees, movers and utility setup to see the cash you need on move-in day."},
    {"slug": "rent-vs-buy-calculator", "name": "Rent vs. Buy Calculator", "icon": "home",
     "short": "Compare renting and buying",
     "desc": "Compare the long-run cost of renting and investing the difference against buying with a mortgage, year by year."},
    {"slug": "renters-insurance-calculator", "name": "Renters Insurance Coverage Calculator", "icon": "umbrella",
     "short": "How much coverage do you need?",
     "desc": "Inventory your belongings room by room to estimate the personal-property coverage and liability limit to ask for."},
    {"slug": "lease-notice-calculator", "name": "Lease Notice Date Calculator", "icon": "calendar",
     "short": "When must you give notice?",
     "desc": "Work out the last day to give move-out notice for your lease and add a reminder to your calendar."},
    {"slug": "fire-safety-checklist", "name": "Apartment Fire Safety Checklist", "icon": "flame",
     "short": "Score your home's fire readiness",
     "desc": "An interactive checklist that scores your apartment's fire readiness and tells you what to fix first."},
]

# Inline SVG icons (Lucide-style strokes). Kept tiny and reused everywhere.
ICONS = {
    "flame": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.07-2.14-.22-4.05 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.15.43-2.29 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "chart": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "landmark": '<path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 2l8 5H4z"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1zM2 16l3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1zM7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V2H6.5A2.5 2.5 0 0 0 4 4.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/>',
    "wallet": '<path d="M20 12V8H6a2 2 0 0 1 0-4h12v4"/><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "truck": '<path d="M10 17h4V5H2v12h3M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h1"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "umbrella": '<path d="M22 12a10.06 10.06 1 0 0-20 0z"/><path d="M12 12v8a2 2 0 0 0 4 0M12 2v1"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "close": '<path d="M18 6 6 18M6 6l12 12"/>',
    "map": '<path d="M14.1 6 9.9 4 3 7v13l6.9-3 4.2 2 6.9-3V3z"/><path d="M9.9 4v13M14.1 6v13"/>',
    "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98M15.41 6.51l-6.82 3.98"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "rss": '<path d="M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "print": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "x": '<path d="M4 4l16 16M20 4 4 20"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=True)


def url(path):
    return ORIGIN + path


def parse_dt(s):
    if len(s) == 10:
        s += "T13:00:00+00:00"
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def nice_date(dt):
    return dt.strftime("%B %-d, %Y")


def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", " ", h))


def words(h):
    return len(plain(h).split())


def read_time(h):
    return max(1, math.ceil(words(h) / 225))


def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if full.endswith("/"):
        full += "index.html"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def jsonld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


# --------------------------------------------------------------------------
# Content loading
# --------------------------------------------------------------------------

def load_articles():
    cities = json.load(open(os.path.join(ROOT, "content/legacy_cities.json")))
    arts = []
    for p in json.load(open(os.path.join(ROOT, "content/legacy_posts.json"))):
        p = dict(p)
        p["city"] = cities.get(p["slug"])
        p.setdefault("tags", [])
        arts.append(p)
    seen = {a["slug"] for a in arts}
    for f in sorted(glob.glob(os.path.join(ROOT, "content/articles/*.json"))):
        data = json.load(open(f, encoding="utf-8"))
        for a in (data if isinstance(data, list) else [data]):
            if a["slug"] in seen:
                raise SystemExit(f"duplicate slug {a['slug']} in {f}")
            if a["category"] not in CATS:
                raise SystemExit(f"unknown category {a['category']} in {f}")
            seen.add(a["slug"])
            a = dict(a)
            a["path"] = f"/news/{a['slug']}/"
            a.setdefault("modified", a["date"])
            a.setdefault("image", f"/assets/img/covers/{a['slug']}.webp")
            a.setdefault("image_alt", a["title"])
            a.setdefault("image_w", 1200)
            a.setdefault("image_h", 675)
            a.setdefault("tags", [])
            arts.append(a)
    for a in arts:
        a["dt"] = parse_dt(a["date"])
        a["mdt"] = max(parse_dt(a["modified"]), a["dt"])
        a["cat"] = CATS[a["category"]]
        a["minutes"] = read_time(a["body_html"])
    arts.sort(key=lambda a: a["dt"], reverse=True)
    return arts


def ensure_covers(arts):
    missing = [a for a in arts if not a.get("legacy")
               and not os.path.exists(os.path.join(ROOT, "static", a["image"].lstrip("/")))]
    if missing:
        subprocess.run([sys.executable, os.path.join(ROOT, "tools/covers.py")], check=True)


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def head(page):
    canonical = url(page["path"])
    img = page.get("image") or DEFAULT_OG
    title = page["title"]
    full_title = title if title.endswith(SITE) else f"{title} | {SITE}"
    robots = page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1")
    extra = page.get("head_extra", "")
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0b2545" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#1f5c99" media="(prefers-color-scheme: light)">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url(img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(page['description'])}">
<meta name="twitter:image" content="{url(img)}">
{extra}<link rel="icon" href="{ICON}-32x32.webp" sizes="32x32">
<link rel="icon" href="{ICON}-192x192.webp" sizes="192x192">
<link rel="apple-touch-icon" href="{ICON}-180x180.webp">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="{SITE} &raquo; Feed" href="{ORIGIN}/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script>try{{var t=localStorage.getItem('rn-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
{jsonld({"@context": "https://schema.org", "@graph": page.get("schema", [])})}
</head>
"""


def header(active=""):
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if active == href else ""}>{name}</a></li>'
        for name, href in NAV)
    ticker = "".join(
        f'<a href="{a["path"]}"><span class="dot" style="--c:{a["cat"]["color"]}"></span>{esc(a["title"])}</a>'
        for a in ARTICLES[:10])
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="topbar">
  <div class="wrap topbar-in">
    <span class="today" data-today>{nice_date(NOW)}</span>
    <a class="wx-mini" href="/weather/" data-wx-mini aria-label="Local weather">{icon("cloud")}<span>Weather</span></a>
    <nav class="topbar-links" aria-label="Utility"><a href="/tools/">Renter Tools</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="{SITE} home"><img src="{LOGO}" alt="{SITE}" width="128" height="57"></a>
    <nav class="main-nav" id="main-nav" aria-label="Main"><ul>{nav}</ul></nav>
    <div class="header-actions">
      <form class="search-pop" action="/search/" role="search"><label class="sr" for="hq">Search</label><input id="hq" name="q" type="search" placeholder="Search news, cities, tools…" autocomplete="off"></form>
      <button class="icon-btn" data-search-toggle aria-label="Search">{icon("search")}</button>
      <button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode">{icon("moon", "ico i-moon")}{icon("sun", "ico i-sun")}</button>
      <button class="icon-btn menu-btn" data-menu aria-controls="main-nav" aria-expanded="false" aria-label="Menu">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="ticker" aria-label="Latest headlines">
  <div class="wrap ticker-in"><span class="ticker-label"><span class="live"></span>Latest</span>
    <div class="ticker-track"><div class="ticker-move">{ticker}{ticker.replace('<a ', '<a tabindex="-1" aria-hidden="true" ')}</div></div>
  </div>
</div>
<main id="main">
"""


def footer(scripts=""):
    cats = "".join(f'<li><a href="/news/category/{k}/">{v["name"]}</a></li>' for k, v in CATS.items())
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{t["name"].replace(" Calculator", "")}</a></li>' for t in TOOLS[:6])
    return f"""</main>
<footer class="site-footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="{LOGO}" alt="{SITE}" width="150" height="67" loading="lazy">
      <p>Independent news for America's renters: apartment fires and safety, rent prices, tenant rights and housing policy, with free tools and live weather.</p>
      <div class="footer-social"><a href="/feed/" aria-label="RSS feed">{icon("rss")}</a><a href="mailto:{EMAIL}" aria-label="Email">{icon("mail")}</a><a href="/weather/" aria-label="Weather">{icon("cloud")}</a></div>
    </div>
    <div><h3>Sections</h3><ul>{cats}</ul></div>
    <div><h3>Renter Tools</h3><ul>{tools}<li><a href="/tools/">All tools →</a></li></ul></div>
    <div><h3>Renter News</h3><ul>
      <li><a href="/about/">About Us</a></li><li><a href="/editorial-policy/">Editorial Policy</a></li>
      <li><a href="/corrections-policy/">Corrections</a></li><li><a href="/frequently-asked-questions/">FAQs</a></li>
      <li><a href="/contact/">Contact Us</a></li><li><a href="/fire-map/">Fire Map</a></li><li><a href="/weather/">Live Weather</a></li></ul></div>
  </div>
  <div class="wrap footer-bottom">
    <span>© {NOW.year} {SITE}. All rights reserved.</span>
    <span><a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-service/">Terms of Service</a> · <a href="/sitemap_index.xml">Sitemap</a></span>
  </div>
</footer>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{scripts}</body>
</html>
"""


def page_html(page, body, active="", scripts=""):
    return head(page) + header(active) + body + footer(scripts)


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

def org_schema():
    return {
        "@type": ["Organization", "NewsMediaOrganization"],
        "@id": ORIGIN + "/#organization",
        "name": SITE,
        "url": ORIGIN + "/",
        "logo": {"@type": "ImageObject", "url": url(LOGO), "width": 512, "height": 227},
        "email": EMAIL,
        "description": "Independent US news site covering apartment fires, renter safety, rent prices, tenant rights and housing policy.",
        "publishingPrinciples": url("/editorial-policy/"),
        "correctionsPolicy": url("/corrections-policy/"),
        "contactPoint": {"@type": "ContactPoint", "contactType": "newsroom", "email": EMAIL, "url": url("/contact/")},
    }


def website_schema():
    return {
        "@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE,
        "description": TAGLINE, "publisher": {"@id": ORIGIN + "/#organization"}, "inLanguage": "en-US",
        "potentialAction": {"@type": "SearchAction",
                            "target": {"@type": "EntryPoint", "urlTemplate": ORIGIN + "/search/?q={search_term_string}"},
                            "query-input": "required name=search_term_string"},
    }


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}


def crumb_html(items):
    parts = [f'<a href="{p}">{esc(n)}</a>' for n, p in items[:-1]] + [f'<span aria-current="page">{esc(items[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------

def chip(a, link=True):
    c = a["cat"]
    inner = f'{icon(c["icon"], "ico ico-sm")}{c["name"]}'
    if link:
        return f'<a class="chip" style="--c:{c["color"]}" href="/news/category/{a["category"]}/">{inner}</a>'
    return f'<span class="chip" style="--c:{c["color"]}">{inner}</span>'


def img_tag(a, cls="", sizes="(max-width: 700px) 100vw, 33vw", eager=False):
    w, h = a.get("image_w") or 1200, a.get("image_h") or 675
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img class="{cls}" src="{a["image"]}" alt="{esc(a["image_alt"])}" width="{w}" height="{h}" sizes="{sizes}" {load}>'


def meta_line(a):
    city = f'<span>{icon("pin", "ico ico-sm")}{esc(a["city"])}</span>' if a.get("city") else ""
    return (f'<div class="meta"><time datetime="{a["dt"].isoformat()}">{nice_date(a["dt"])}</time>'
            f'<span>{icon("clock", "ico ico-sm")}{a["minutes"]} min read</span>{city}</div>')


def card(a, variant="", eager=False):
    return f"""<article class="card {variant} reveal" data-cat="{a['category']}">
  <a class="card-media" href="{a['path']}" tabindex="-1" aria-hidden="true">{img_tag(a, eager=eager)}</a>
  <div class="card-body">{chip(a)}
    <h3 class="card-title"><a href="{a['path']}">{esc(a['title'])}</a></h3>
    <p class="card-dek">{esc(a['description'])}</p>
    {meta_line(a)}
  </div>
</article>"""


def mini(a, n=None):
    num = f'<span class="rank">{n:02d}</span>' if n else ""
    return f"""<li class="mini">{num}<div><a href="{a['path']}">{esc(a['title'])}</a>
<span class="mini-meta" style="--c:{a['cat']['color']}">{a['cat']['name']} · <time datetime="{a['dt'].date()}">{a['dt'].strftime('%b %-d, %Y')}</time></span></div></li>"""


def offers_box():
    return f"""<div class="offer-stack">
  <a class="offer offer-ins" href="{OFFERS['insurance']}" target="_blank" rel="sponsored noopener">
    {icon("umbrella")}<span><strong>Get Renters Coverage Now</strong><small>Starting from $5/mo.</small></span><em>Sponsored</em></a>
  <a class="offer offer-img" href="{OFFERS['credit']}" target="_blank" rel="sponsored noopener">
    <img src="/wp-content/uploads/2025/08/Boost-Your-Credit-Score-BY-82-points.webp" alt="Boost your credit score by 82 points - join for free" width="500" height="192" loading="lazy"><em>Sponsored</em></a>
</div>"""


def wx_card():
    return """<section class="wx-card" data-wx-card aria-label="Local weather">
  <div class="wx-card-head"><span>Weather</span><a href="/weather/">Full forecast →</a></div>
  <div class="wx-card-body"><div class="skeleton" style="height:84px"></div></div>
</section>"""


def tools_band():
    items = "".join(
        f'<a class="tool-tile reveal" href="/tools/{t["slug"]}/"><span class="tool-ico">{icon(t["icon"])}</span>'
        f'<strong>{t["name"]}</strong><small>{t["short"]}</small></a>' for t in TOOLS)
    return f"""<section class="band band-tools">
  <div class="wrap">
    <div class="section-head"><h2>Renter Tools</h2><a href="/tools/">All tools {icon("arrow", "ico ico-sm")}</a></div>
    <div class="tool-grid">{items}</div>
  </div>
</section>"""


def sidebar(exclude=None):
    latest = [a for a in ARTICLES if a is not exclude][:6]
    guides = [a for a in ARTICLES if a["category"] == "guides" and a is not exclude][:4]
    g = ""
    if guides:
        g = f'<section class="side-box"><h2 class="side-title">Renter Guides</h2><ul class="mini-list">{"".join(mini(a) for a in guides)}</ul></section>'
    return f"""<aside class="sidebar">
  {wx_card()}
  <section class="side-box"><h2 class="side-title">Latest News</h2><ol class="mini-list ranked">{"".join(mini(a, i + 1) for i, a in enumerate(latest))}</ol></section>
  {offers_box()}
  {g}
  <section class="side-box side-tools"><h2 class="side-title">Quick Tools</h2>
    {"".join(f'<a href="/tools/{t["slug"]}/">{icon(t["icon"], "ico ico-sm")}{t["name"]}</a>' for t in TOOLS[:5])}
  </section>
</aside>"""


def pager(base, page, pages):
    if pages <= 1:
        return ""
    def href(n):
        return base if n == 1 else f"{base}page/{n}/"
    links = []
    if page > 1:
        links.append(f'<a rel="prev" href="{href(page - 1)}">← Newer</a>')
    for n in range(1, pages + 1):
        links.append(f'<span aria-current="page">{n}</span>' if n == page else f'<a href="{href(n)}">{n}</a>')
    if page < pages:
        links.append(f'<a rel="next" href="{href(page + 1)}">Older →</a>')
    return '<nav class="pager" aria-label="Pagination">' + "".join(links) + "</nav>"


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def build_home():
    lead, side = ARTICLES[0], ARTICLES[1:5]
    rest = ARTICLES[5:17]
    stats_cities = len({a["city"] for a in ARTICLES if a.get("city")})
    fires = sum(1 for a in ARTICLES if a["category"] == "fire")
    filters = '<button class="filter is-on" data-filter="all">All</button>' + "".join(
        f'<button class="filter" data-filter="{k}" style="--c:{v["color"]}">{v["name"]}</button>'
        for k, v in CATS.items() if any(a["category"] == k for a in ARTICLES))
    sections = ""
    for key in ["fire", "rent-prices", "tenant-rights", "guides"]:
        items = [a for a in ARTICLES if a["category"] == key][:3]
        if len(items) < 2:
            continue
        c = CATS[key]
        sections += f"""<section class="cat-block" style="--c:{c['color']}">
  <div class="section-head"><h2><span class="bar"></span>{c['name']}</h2><a href="/news/category/{key}/">More {c['name']} {icon("arrow", "ico ico-sm")}</a></div>
  <div class="grid-3">{"".join(card(a, "card-compact") for a in items)}</div>
</section>"""
    side_html = "".join(f"""<article class="stack-item reveal">
  <a class="stack-media" href="{a['path']}" tabindex="-1" aria-hidden="true">{img_tag(a, sizes="160px")}</a>
  <div>{chip(a)}<h3><a href="{a['path']}">{esc(a['title'])}</a></h3>{meta_line(a)}</div>
</article>""" for a in side)
    body = f"""
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap hero-grid">
    <article class="lead reveal">
      <a href="{lead['path']}" class="lead-media" tabindex="-1" aria-hidden="true">{img_tag(lead, sizes="(max-width: 900px) 100vw, 60vw", eager=True)}</a>
      <div class="lead-body">{chip(lead)}
        <h2 class="lead-title"><a href="{lead['path']}">{esc(lead['title'])}</a></h2>
        <p>{esc(lead['description'])}</p>{meta_line(lead)}
      </div>
    </article>
    <div class="stack">{side_html}</div>
  </div>
</section>
<section class="stats-strip">
  <div class="wrap stats-in">
    <div class="stat reveal"><strong data-count="{len(ARTICLES)}">{len(ARTICLES)}</strong><span>stories published</span></div>
    <div class="stat reveal"><strong data-count="{fires}">{fires}</strong><span>fire reports tracked</span></div>
    <div class="stat reveal"><strong data-count="{stats_cities}">{stats_cities}</strong><span>cities covered</span></div>
    <div class="stat reveal"><strong data-count="{len(TOOLS)}">{len(TOOLS)}</strong><span>free renter tools</span></div>
    <a class="stat stat-link reveal" href="/fire-map/">{icon("map")}<span>Explore the<br>Fire Map</span></a>
  </div>
</section>
<div class="wrap layout">
  <div class="primary">
    <section>
      <div class="section-head"><h1 class="h-section">Latest Renter News</h1><a href="/news/">All news {icon("arrow", "ico ico-sm")}</a></div>
      <div class="filters" role="group" aria-label="Filter by section">{filters}</div>
      <div class="grid-3" data-filter-grid>{"".join(card(a) for a in rest)}</div>
      <p class="center"><a class="btn" href="/news/">Browse all {len(ARTICLES)} stories {icon("arrow", "ico ico-sm")}</a></p>
    </section>
    {sections}
  </div>
  {sidebar()}
</div>
{tools_band()}
<section class="band band-weather">
  <div class="wrap wx-band" data-wx-band>
    <div><span class="kicker">Live</span><h2>Weather where you live</h2>
      <p>Current conditions, hourly and 7-day forecasts and National Weather Service alerts for any US city or ZIP code.</p>
      <a class="btn btn-light" href="/weather/">Open live weather {icon("arrow", "ico ico-sm")}</a></div>
    <div class="wx-band-now" data-wx-band-now><div class="skeleton" style="height:120px"></div></div>
  </div>
</section>
"""
    schema = [org_schema(), website_schema(),
              {"@type": "CollectionPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": f"{SITE} - {TAGLINE}",
               "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#organization"},
               "description": HOME_DESC, "inLanguage": "en-US"},
              {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": url(a["path"])} for i, a in enumerate(ARTICLES[:10])]}]
    page = {"path": "/", "title": f"{SITE} - {TAGLINE}", "description": HOME_DESC, "schema": schema}
    write("/", page_html(page, body, "/"))


def build_listing(base, title, h1, desc, items, crumbs_items, blurb="", color=None, active=""):
    pages = max(1, math.ceil(len(items) / PER_PAGE))
    for n in range(1, pages + 1):
        chunk = items[(n - 1) * PER_PAGE:n * PER_PAGE]
        path = base if n == 1 else f"{base}page/{n}/"
        t = title if n == 1 else f"{title} - Page {n}"
        d = desc if n == 1 else f"Page {n} of {pages}: {desc}"
        style = f' style="--c:{color}"' if color else ""
        lead = ""
        grid = chunk
        if n == 1 and len(chunk) >= 4:
            lead = f'<div class="grid-2 feature-pair">{card(chunk[0], "card-wide", eager=True)}{card(chunk[1], "card-wide")}</div>'
            grid = chunk[2:]
        body = f"""<section class="page-hero"{style}>
  <div class="hero-bg" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap">{crumb_html(crumbs_items)}<h1>{esc(h1)}</h1><p>{esc(blurb or desc)}</p>
  <span class="count-pill">{len(items)} stories</span></div>
</section>
<div class="wrap layout">
  <div class="primary">{lead}<div class="grid-3">{"".join(card(a) for a in grid)}</div>{pager(base, n, pages)}</div>
  {sidebar()}
</div>
{tools_band()}"""
        schema = [org_schema(), website_schema(), crumbs(crumbs_items),
                  {"@type": "CollectionPage", "url": url(path), "name": t, "description": d,
                   "isPartOf": {"@id": ORIGIN + "/#website"}, "inLanguage": "en-US",
                   "mainEntity": {"@type": "ItemList", "itemListElement": [
                       {"@type": "ListItem", "position": i + 1, "url": url(a["path"])} for i, a in enumerate(chunk)]}}]
        page = {"path": path, "title": t, "description": d, "schema": schema}
        write(path, page_html(page, body, active))


def share_bar(a):
    u = esc(url(a["path"]))
    t = esc(a["title"])
    return f"""<div class="share" data-share data-url="{u}" data-title="{t}">
  <span>Share</span>
  <a href="https://twitter.com/intent/tweet?url={u}&amp;text={t}" target="_blank" rel="noopener" aria-label="Share on X">{icon("x")}</a>
  <a href="https://www.facebook.com/sharer/sharer.php?u={u}" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon("facebook")}</a>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{icon("linkedin")}</a>
  <a href="mailto:?subject={t}&amp;body={u}" aria-label="Share by email">{icon("mail")}</a>
  <button type="button" data-copy aria-label="Copy link">{icon("link")}</button>
  <button type="button" data-native-share aria-label="Share" hidden>{icon("share")}</button>
</div>"""


def prep_body(h):
    h = re.sub(r"<iframe(?![^>]*loading=)", '<iframe loading="lazy"', h)
    h = re.sub(r"(<iframe[^>]*google\.com/maps[^>]*>\s*</iframe>)", r'<div class="embed embed-map">\1</div>', h)
    h = re.sub(r"(<iframe[^>]*youtube\.com[^>]*>\s*</iframe>)", r'<div class="embed embed-video">\1</div>', h)
    h = re.sub(r'<img(?![^>]*loading=)', '<img loading="lazy" decoding="async"', h)
    # Add ids to h2 for the table of contents.
    toc = []
    def add_id(m):
        attrs, inner = m.group(1), m.group(2)
        txt = plain(inner).strip()
        if 'id="' in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            hid = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")[:60] or f"s{len(toc)}"
            attrs += f' id="{hid}"'
        toc.append((hid, txt))
        return f"<h2{attrs}>{inner}</h2>"
    h = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, h, flags=re.S)
    return h, toc


def build_article(a, idx):
    body_html, toc = prep_body(a["body_html"])
    related = [x for x in ARTICLES if x is not a and x["category"] == a["category"]][:3]
    if len(related) < 3:
        related += [x for x in ARTICLES if x is not a and x not in related][:3 - len(related)]
    newer = ARTICLES[idx - 1] if idx > 0 else None
    older = ARTICLES[idx + 1] if idx + 1 < len(ARTICLES) else None
    kp = ""
    if a.get("key_points"):
        kp = '<div class="key-points"><h2>Key points</h2><ul>' + "".join(f"<li>{esc(k)}</li>" for k in a["key_points"]) + "</ul></div>"
    toc_html = ""
    if len(toc) >= 3:
        toc_html = ('<details class="toc" open><summary>In this article</summary><ol>'
                    + "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in toc) + "</ol></details>")
    src = ""
    if a.get("sources"):
        src = ('<section class="sources"><h2>Sources</h2><ol>'
               + "".join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener nofollow">{esc(s["name"])}</a></li>' for s in a["sources"])
               + "</ol></section>")
    tags = ""
    if a.get("tags"):
        tags = '<div class="tags">' + "".join(f'<a href="/search/?q={esc(t)}">#{esc(t)}</a>' for t in a["tags"]) + "</div>"
    updated = ""
    if (a["mdt"] - a["dt"]).total_seconds() > 86400:
        updated = f' · Updated <time datetime="{a["mdt"].isoformat()}">{nice_date(a["mdt"])}</time>'
    scripts = ""
    if "twitter-tweet" in body_html:
        scripts += '<script async src="https://platform.twitter.com/widgets.js"></script>\n'
    if "instagram-media" in body_html:
        scripts += '<script async src="https://www.instagram.com/embed.js"></script>\n'
    body_html = re.sub(r'<script[^>]*src="[^"]*(?:twitter|instagram)[^"]*"[^>]*></script>', "", body_html)
    adjacent = '<nav class="adjacent" aria-label="More stories">'
    if older:
        adjacent += f'<a href="{older["path"]}"><small>← Previous story</small>{esc(older["title"])}</a>'
    if newer:
        adjacent += f'<a class="next" href="{newer["path"]}"><small>Next story →</small>{esc(newer["title"])}</a>'
    adjacent += "</nav>"
    cr = [("Home", "/"), ("News", "/news/"), (a["cat"]["name"], f"/news/category/{a['category']}/"), (a["title"], a["path"])]
    tool = {"fire": "fire-safety-checklist", "safety": "fire-safety-checklist", "rent-prices": "rent-affordability-calculator",
            "housing-policy": "rent-increase-calculator", "tenant-rights": "lease-notice-calculator",
            "guides": "renters-insurance-calculator"}[a["category"]]
    t = next(x for x in TOOLS if x["slug"] == tool)
    body = f"""<article class="article" style="--c:{a['cat']['color']}">
  <header class="article-head">
    <div class="hero-bg" aria-hidden="true"><span></span><span></span></div>
    <div class="wrap narrow">
      {crumb_html(cr[:-1])}
      {chip(a)}
      <h1>{esc(a['title'])}</h1>
      <p class="dek">{esc(a['description'])}</p>
      <div class="byline">
        <img src="{ICON}-192x192.webp" alt="" width="40" height="40">
        <div><a href="{AUTHOR['path']}" rel="author">{AUTHOR['name']}</a>
        <span><time datetime="{a['dt'].isoformat()}">{nice_date(a['dt'])}</time>{updated} · {a['minutes']} min read{(' · ' + esc(a['city'])) if a.get('city') else ''}</span></div>
      </div>
    </div>
  </header>
  <div class="wrap narrow">
    <figure class="article-figure">{img_tag(a, sizes="(max-width: 860px) 100vw, 860px", eager=True)}</figure>
  </div>
  <div class="wrap article-layout">
    <div class="article-main">
      {share_bar(a)}
      {kp}{toc_html}
      <div class="prose">{body_html}</div>
      {src}{tags}
      <div class="tool-cta"><span class="tool-ico">{icon(t['icon'])}</span><div><strong>{t['name']}</strong><p>{t['desc']}</p></div>
        <a class="btn" href="/tools/{t['slug']}/">Try it free</a></div>
      {share_bar(a)}
      {adjacent}
    </div>
    {sidebar(exclude=a)}
  </div>
  <section class="wrap related"><div class="section-head"><h2>Related stories</h2><a href="/news/category/{a['category']}/">More {a['cat']['name']} {icon("arrow", "ico ico-sm")}</a></div>
    <div class="grid-3">{"".join(card(x) for x in related)}</div></section>
</article>
"""
    article_schema = {
        "@type": "NewsArticle", "@id": url(a["path"]) + "#article",
        "mainEntityOfPage": {"@type": "WebPage", "@id": url(a["path"])},
        "headline": a["title"][:110], "description": a["description"],
        "image": [{"@type": "ImageObject", "url": url(a["image"]), "width": a.get("image_w") or 1200, "height": a.get("image_h") or 675}],
        "datePublished": a["dt"].isoformat(), "dateModified": a["mdt"].isoformat(),
        "author": [{"@type": "Organization", "name": AUTHOR["name"], "url": url(AUTHOR["path"])}],
        "publisher": {"@id": ORIGIN + "/#organization"},
        "articleSection": a["cat"]["name"], "wordCount": words(a["body_html"]), "inLanguage": "en-US",
        "isAccessibleForFree": True,
    }
    if a.get("tags"):
        article_schema["keywords"] = a["tags"]
    if a.get("city") and a["city"] in GEO:
        lat, lon = GEO[a["city"]]
        article_schema["contentLocation"] = {"@type": "Place", "name": a["city"],
                                             "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon}}
    if a.get("sources"):
        article_schema["citation"] = [s["url"] for s in a["sources"]]
    extra = (f'<meta property="article:published_time" content="{a["dt"].isoformat()}">\n'
             f'<meta property="article:modified_time" content="{a["mdt"].isoformat()}">\n'
             f'<meta property="article:section" content="{esc(a["cat"]["name"])}">\n'
             f'<meta name="author" content="{AUTHOR["name"]}">\n')
    page = {"path": a["path"], "title": a.get("seo_title") or a["title"], "description": a["description"],
            "image": a["image"], "og_type": "article", "head_extra": extra,
            "schema": [org_schema(), website_schema(), crumbs(cr), article_schema]}
    write(a["path"], page_html(page, body, "", scripts))


def simple_page(path, title, desc, inner, h1=None, crumbs_items=None, schema_extra=None, wide=False, scripts="", active="", lede=""):
    inner = re.sub(r"\{icon:(\w+)\}", lambda m: icon(m.group(1)), inner)
    cr = crumbs_items or [("Home", "/"), (h1 or title, path)]
    body = f"""<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap">{crumb_html(cr)}<h1>{esc(h1 or title)}</h1>{f'<p>{lede}</p>' if lede else ''}</div>
</section>
<div class="wrap {'' if wide else 'narrow'} page-body">{inner}</div>
"""
    schema = [org_schema(), website_schema(), crumbs(cr),
              {"@type": "WebPage", "url": url(path), "name": title, "description": desc, "isPartOf": {"@id": ORIGIN + "/#website"}}]
    schema += schema_extra or []
    page = {"path": path, "title": title, "description": desc, "schema": schema}
    write(path, page_html(page, body, active, scripts))


def build_pages():
    legacy = {p["slug"]: p for p in json.load(open(os.path.join(ROOT, "content/legacy_pages.json")))}
    from content.pages import PAGES
    for slug in ["frequently-asked-questions", "privacy-policy", "terms-of-service"]:
        p = legacy[slug]
        inner = '<div class="prose">' + p["body_html"] + PAGES.get(slug + "-append", "") + "</div>"
        simple_page(f"/{slug}/", p["title"], p["description"] or PAGES[slug + "-desc"], inner)
    for slug in ["about", "contact", "editorial-policy", "corrections-policy"]:
        p = PAGES[slug]
        simple_page(f"/{slug}/", p["title"], p["description"], p["html"], h1=p.get("h1"), lede=p.get("lede", ""),
                    schema_extra=p.get("schema"))
    # Author page
    items = ARTICLES
    body = f"""<div class="author-card"><img src="{ICON}-192x192.webp" alt="" width="96" height="96">
<div><p>The {SITE} staff covers apartment fires and building emergencies, rent and housing-market data, tenant rights and housing policy across the United States.
Stories are reported from public records, fire-department and government statements and other named sources, which are linked in each article. Read our <a href="/editorial-policy/">editorial policy</a> or <a href="/contact/">contact the newsroom</a>.</p></div></div>
<h2 class="h-section">Stories by {AUTHOR['name']}</h2><div class="grid-3">{"".join(card(a) for a in items)}</div>"""
    simple_page(AUTHOR["path"], AUTHOR["name"], f"News and guides for renters by the {SITE} staff.", body, wide=True,
                crumbs_items=[("Home", "/"), ("News", "/news/"), (AUTHOR["name"], AUTHOR["path"])],
                schema_extra=[{"@type": "ProfilePage", "url": url(AUTHOR["path"]),
                               "mainEntity": {"@type": "Organization", "name": AUTHOR["name"], "url": url(AUTHOR["path"]),
                                              "parentOrganization": {"@id": ORIGIN + "/#organization"}}}])


def build_tools():
    from content.tools import TOOL_HTML, TOOL_FAQ
    tiles = "".join(f"""<a class="tool-card reveal" href="/tools/{t['slug']}/">
  <span class="tool-ico">{icon(t['icon'])}</span><h2>{t['name']}</h2><p>{t['desc']}</p><span class="go">Open tool {icon("arrow", "ico ico-sm")}</span></a>""" for t in TOOLS)
    simple_page("/tools/", "Free Renter Tools & Calculators",
                "Free calculators for renters: rent affordability, roommate rent split, rent increases, move-in costs, rent vs. buy, renters insurance and lease notice dates.",
                f'<div class="tool-cards">{tiles}</div>', wide=True, active="/tools/",
                lede="Interactive calculators and checklists that run in your browser. Nothing you type is sent anywhere.",
                schema_extra=[{"@type": "ItemList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": url(f"/tools/{t['slug']}/"), "name": t["name"]} for i, t in enumerate(TOOLS)]}])
    for t in TOOLS:
        path = f"/tools/{t['slug']}/"
        faq = TOOL_FAQ.get(t["slug"], [])
        faq_html = ""
        schema = [{"@type": "WebApplication", "name": t["name"], "url": url(path), "applicationCategory": "FinanceApplication",
                   "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": t["desc"]}]
        if faq:
            faq_html = '<section class="faq"><h2>Frequently asked questions</h2>' + "".join(
                f"<details><summary>{esc(q)}</summary><div>{a_}</div></details>" for q, a_ in faq) + "</section>"
            schema.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a_).strip()}} for q, a_ in faq]})
        others = "".join(f'<a href="/tools/{o["slug"]}/">{icon(o["icon"], "ico ico-sm")}{o["name"]}</a>' for o in TOOLS if o is not t)
        inner = f"""<div class="tool-app" data-tool="{t['slug']}">{TOOL_HTML[t['slug']]}</div>
<p class="disclaimer">Estimates are for planning only and are not financial, legal or insurance advice. Rules and costs vary by state, city and lease.</p>
{faq_html}
<section class="more-tools"><h2>More renter tools</h2><div class="side-tools">{others}</div></section>"""
        simple_page(path, t["name"], t["desc"], inner, wide=True, active="/tools/", lede=esc(t["desc"]),
                    crumbs_items=[("Home", "/"), ("Tools", "/tools/"), (t["name"], path)], schema_extra=schema,
                    scripts=f'<script src="/assets/js/tools.js?v={ASSET_V}" defer></script>\n')


def build_weather():
    inner = """<div class="weather-app" data-weather-app>
  <div class="wx-toolbar">
    <form class="wx-search" data-wx-search autocomplete="off" role="search">
      <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <label class="sr" for="wxq">Search a city</label>
      <input id="wxq" type="search" placeholder="Search a US city or ZIP code…" data-wx-input>
      <ul class="wx-suggest" data-wx-suggest role="listbox"></ul>
    </form>
    <button class="btn btn-ghost" data-wx-locate type="button">Use my location</button>
    <div class="unit-toggle" role="group" aria-label="Units"><button data-unit="f" class="is-on" type="button">°F</button><button data-unit="c" type="button">°C</button></div>
  </div>
  <div class="wx-quick" data-wx-quick></div>
  <div class="wx-alerts" data-wx-alerts></div>
  <section class="wx-hero" data-wx-hero><div class="skeleton" style="height:260px"></div></section>
  <section class="wx-panel"><h2>Next 24 hours</h2><div class="wx-hourly" data-wx-hourly><div class="skeleton" style="height:180px"></div></div></section>
  <div class="wx-cols">
    <section class="wx-panel"><h2>7-day forecast</h2><div class="wx-daily" data-wx-daily><div class="skeleton" style="height:320px"></div></div></section>
    <section class="wx-panel"><h2>Conditions</h2><div class="wx-details" data-wx-details><div class="skeleton" style="height:320px"></div></div></section>
  </div>
  <section class="wx-panel wx-tips"><h2>Weather tips for renters</h2><div data-wx-tips></div></section>
  <p class="wx-credit">Forecasts, observations and alerts: <a href="https://www.weather.gov/" target="_blank" rel="noopener">NOAA National Weather Service</a> (US locations). Place search: <a href="https://www.geonames.org/" target="_blank" rel="noopener">GeoNames</a> (CC BY 4.0). Updated every 10 minutes while this page is open.</p>
</div>"""
    simple_page("/weather/", "Live Weather Forecast for Renters",
                "Live local weather from the National Weather Service: current conditions, hourly and 7-day forecasts and active alerts for any US city or ZIP code, plus renter tips.",
                inner, h1="Live Weather", wide=True, active="/weather/",
                lede="Current conditions, hourly and 7-day forecasts and active alerts from the National Weather Service for any US city or ZIP code.",
                scripts=f'<script src="/assets/js/weather.js?v={ASSET_V}" defer></script>\n')


def build_fire_map():
    pts = []
    for a in ARTICLES:
        if a.get("city") and a["city"] in GEO:
            lat, lon = GEO[a["city"]]
            pts.append({"t": a["title"], "u": a["path"], "c": a["category"], "n": a["cat"]["name"], "col": a["cat"]["color"],
                        "d": a["dt"].strftime("%b %-d, %Y"), "y": a["dt"].year, "city": a["city"], "lat": lat, "lon": lon,
                        "img": a["image"]})
    years = sorted({p["y"] for p in pts}, reverse=True)
    cats = [k for k in CATS if any(p["c"] == k for p in pts)]
    filt = ('<button class="filter is-on" data-mf="all">All</button>'
            + "".join(f'<button class="filter" data-mf="{k}" style="--c:{CATS[k]["color"]}">{CATS[k]["name"]}</button>' for k in cats)
            + '<span class="sepv"></span><button class="filter is-on" data-my="all">All years</button>'
            + "".join(f'<button class="filter" data-my="{y}">{y}</button>' for y in years))
    inner = f"""<div class="map-app">
  <div class="filters" role="group" aria-label="Filter map">{filt}</div>
  <div class="map-wrap"><div id="fire-map" class="fire-map" role="region" aria-label="Map of reported incidents"></div>
  <div class="map-count" data-map-count></div></div>
  <div class="map-list" data-map-list></div>
</div>
<script id="map-data" type="application/json">{json.dumps(pts, ensure_ascii=False).replace("</", "<\\/")}</script>"""
    head_extra = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" crossorigin="anonymous">\n'
    scripts = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" crossorigin="anonymous" defer></script>\n'
               f'<script src="/assets/js/firemap.js?v={ASSET_V}" defer></script>\n')
    cr = [("Home", "/"), ("Fire Map", "/fire-map/")]
    desc = "Interactive map of the apartment fires and renter safety incidents covered by Renter News, filterable by type and year."
    body = f"""<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap">{crumb_html(cr)}<h1>Apartment Fire &amp; Incident Map</h1><p>Every incident Renter News has reported, plotted by city. Tap a marker to read the story.</p></div>
</section>
<div class="wrap page-body">{inner}</div>"""
    page = {"path": "/fire-map/", "title": "Apartment Fire Map: Incidents Reported by Renter News", "description": desc,
            "head_extra": head_extra,
            "schema": [org_schema(), website_schema(), crumbs(cr), {"@type": "WebPage", "url": url("/fire-map/"), "name": "Apartment Fire Map", "description": desc}]}
    write("/fire-map/", page_html(page, body, "/fire-map/", scripts))


def build_search():
    idx = [{"t": a["title"], "d": a["description"], "u": a["path"], "c": a["cat"]["name"], "col": a["cat"]["color"],
            "dt": a["dt"].strftime("%b %-d, %Y"), "i": a["image"], "city": a.get("city") or "",
            "k": " ".join(a.get("tags", [])), "b": " ".join(plain(a["body_html"]).split())[:1500]} for a in ARTICLES]
    idx += [{"t": t["name"], "d": t["desc"], "u": f"/tools/{t['slug']}/", "c": "Tool", "col": "#1f5c99", "dt": "", "i": "",
             "city": "", "k": "calculator tool", "b": ""} for t in TOOLS]
    write("/search-index.json", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))
    inner = """<form class="search-big" action="/search/" role="search"><label class="sr" for="sq">Search Renter News</label>
<input id="sq" name="q" type="search" placeholder="Try “Chicago”, “renters insurance” or “rent increase”" data-search-input>
<button class="btn" type="submit">Search</button></form>
<p class="search-status" data-search-status aria-live="polite"></p>
<div class="grid-3" data-search-results></div>"""
    simple_page("/search/", "Search", "Search Renter News articles, guides and tools.", inner, h1="Search Renter News",
                wide=True, scripts=f'<script src="/assets/js/search.js?v={ASSET_V}" defer></script>\n')
    # noindex the search results page
    p = os.path.join(OUT, "search/index.html")
    s = open(p).read().replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">',
                               '<meta name="robots" content="noindex, follow">')
    open(p, "w").write(s)


def build_404():
    inner = f"""<div class="notfound"><p class="big">404</p><p>That page isn't here. It may have moved, or the link may be mistyped.</p>
<form class="search-big" action="/search/" role="search"><label class="sr" for="nq">Search</label><input id="nq" name="q" type="search" placeholder="Search Renter News"><button class="btn">Search</button></form>
<h2 class="h-section">Latest stories</h2><div class="grid-3">{"".join(card(a) for a in ARTICLES[:6])}</div></div>"""
    page = {"path": "/404.html", "title": "Page not found", "description": "The page you requested could not be found.",
            "robots": "noindex, follow", "schema": [org_schema()]}
    body = f"""<section class="page-hero"><div class="hero-bg" aria-hidden="true"><span></span><span></span></div><div class="wrap"><h1>Page not found</h1></div></section>
<div class="wrap page-body">{inner}</div>"""
    write("/404.html", page_html(page, body))


# --------------------------------------------------------------------------
# Feeds and sitemaps
# --------------------------------------------------------------------------

def xml_esc(s):
    return html.escape(str(s), quote=False)


def build_feeds():
    items = ""
    for a in ARTICLES[:30]:
        items += f"""<item><title>{xml_esc(a['title'])}</title><link>{url(a['path'])}</link><guid isPermaLink="true">{url(a['path'])}</guid>
<pubDate>{format_datetime(a['dt'])}</pubDate><category>{xml_esc(a['cat']['name'])}</category><dc:creator>{AUTHOR['name']}</dc:creator>
<description>{xml_esc(a['description'])}</description><media:content url="{url(a['image'])}" medium="image"/></item>
"""
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
<channel><title>{SITE}</title><link>{ORIGIN}/</link><description>{xml_esc(TAGLINE)}</description><language>en-us</language>
<atom:link href="{ORIGIN}/feed/" rel="self" type="application/rss+xml"/><lastBuildDate>{format_datetime(NOW)}</lastBuildDate>
<image><url>{url(LOGO)}</url><title>{SITE}</title><link>{ORIGIN}/</link></image>
{items}</channel></rss>
"""
    write("/feed.xml", rss)

    def urlset(entries):
        rows = "".join(f"<url><loc>{url(p)}</loc><lastmod>{m}</lastmod>{img}</url>\n" for p, m, img in entries)
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + rows + "</urlset>\n")

    today = NOW.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    post_entries = [(a["path"], a["mdt"].isoformat(), f"<image:image><image:loc>{url(a['image'])}</image:loc></image:image>") for a in ARTICLES]
    write("/post-sitemap.xml", urlset(post_entries))
    pages = ["/", "/news/", "/about/", "/contact/", "/frequently-asked-questions/", "/editorial-policy/", "/corrections-policy/",
             "/privacy-policy/", "/terms-of-service/", "/weather/", "/fire-map/", "/tools/", AUTHOR["path"]] + [f"/tools/{t['slug']}/" for t in TOOLS]
    write("/page-sitemap.xml", urlset([(p, today, "") for p in pages]))
    cat_entries = []
    for k in CATS:
        its = [a for a in ARTICLES if a["category"] == k]
        if its:
            cat_entries.append((f"/news/category/{k}/", its[0]["mdt"].isoformat(), ""))
    write("/category-sitemap.xml", urlset(cat_entries))

    # Google News sitemap: articles from the last 2 days only (per Google's spec).
    recent = [a for a in ARTICLES if NOW - a["dt"] <= timedelta(days=2)]
    news_rows = "".join(f"""<url><loc>{url(a['path'])}</loc><news:news><news:publication><news:name>{SITE}</news:name><news:language>en</news:language></news:publication>
<news:publication_date>{a['dt'].isoformat()}</news:publication_date><news:title>{xml_esc(a['title'])}</news:title></news:news></url>
""" for a in recent)
    write("/news-sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">\n' + news_rows + "</urlset>\n")

    idx = "".join(f"<sitemap><loc>{url('/' + n)}</loc><lastmod>{today}</lastmod></sitemap>\n"
                  for n in ["post-sitemap.xml", "page-sitemap.xml", "category-sitemap.xml", "news-sitemap.xml"])
    write("/sitemap_index.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + idx + "</sitemapindex>\n")
    write("/robots.txt", f"User-agent: *\nDisallow: /search/\nDisallow: /search-index.json\n\nSitemap: {ORIGIN}/sitemap_index.xml\nSitemap: {ORIGIN}/news-sitemap.xml\n")


def build_htaccess():
    shortlinks = "".join(
        f"RewriteCond %{{QUERY_STRING}} ^p={a['wp_id']}$\nRewriteRule ^$ {a['path']}? [R=301,L]\n" for a in ARTICLES if a.get("wp_id"))
    legacy_pages = json.load(open(os.path.join(ROOT, "content/legacy_pages.json")))
    shortlinks += "".join(
        f"RewriteCond %{{QUERY_STRING}} ^page_id={p['wp_id']}$\nRewriteRule ^$ /{p['slug']}/? [R=301,L]\n" for p in legacy_pages)
    tpl = open(os.path.join(ROOT, "templates/htaccess")).read()
    write("/.htaccess", tpl.replace("{{SHORTLINKS}}", shortlinks.rstrip()))


# --------------------------------------------------------------------------

def main():
    global ARTICLES, GEO, ASSET_V, HOME_DESC
    sys.path.insert(0, ROOT)
    ARTICLES = load_articles()
    ensure_covers(ARTICLES)
    GEO = json.load(open(os.path.join(ROOT, "content/geo.json")))
    HOME_DESC = ("Renter News covers apartment fires, renter safety, rent prices, tenant rights and housing policy across the US, "
                 "with free renter calculators and live weather.")
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    import hashlib
    h = hashlib.md5()
    for f in sorted(glob.glob(os.path.join(ROOT, "static/assets/**/*.*"), recursive=True)):
        if f.endswith((".css", ".js")):
            h.update(open(f, "rb").read())
    ASSET_V = h.hexdigest()[:8]

    build_home()
    build_listing("/news/", "All Renter News", "All Renter News",
                  "Every Renter News story: apartment fires, renter safety, rent prices, tenant rights, housing policy and renter guides.",
                  ARTICLES, [("Home", "/"), ("News", "/news/")], active="/news/")
    for k, c in CATS.items():
        items = [a for a in ARTICLES if a["category"] == k]
        if not items:
            continue
        build_listing(f"/news/category/{k}/", f"{c['name']} News", c["name"], c["blurb"], items,
                      [("Home", "/"), ("News", "/news/"), (c["name"], f"/news/category/{k}/")], color=c["color"],
                      active=f"/news/category/{k}/")
    for i, a in enumerate(ARTICLES):
        build_article(a, i)
    build_pages()
    build_tools()
    build_weather()
    build_fire_map()
    build_search()
    build_404()
    build_feeds()
    build_htaccess()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"built {len(ARTICLES)} articles, {n} files -> {OUT}")


ARTICLES, GEO, ASSET_V, HOME_DESC = [], {}, "1", ""

if __name__ == "__main__":
    main()
