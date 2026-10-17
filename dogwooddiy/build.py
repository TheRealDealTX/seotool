#!/usr/bin/env python3
"""Static site generator for dogwooddiy.com.

    python3 build.py        # writes the site into ./public

Pure standard library. Page copy lives in content/; this file holds the
layout, page templates, calculators and structured data.
"""

import html
import json
import os
import re
import shutil

from content.site import SITE, CATS, NAV
from content.posts_legacy import POSTS as LEGACY
from content.posts_new import POSTS as NEW
from content.pages import ABOUT, PRIVACY, DISCLAIMER, TERMS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
POSTS = sorted(LEGACY + NEW, key=lambda p: p["date"], reverse=True)
BY_SLUG = {p["slug"]: p for p in POSTS}
ASSET_V = "3"


def esc(s):
    return html.escape(str(s), quote=True)


def url(path):
    return SITE["origin"] + path


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60].strip("-")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def read_minutes(body, extra=""):
    text = strip_tags(re.sub(r"\[\[[^\]]+\]\]", "", body + " " + extra))
    return max(3, round(len(text.split()) / 220))


def post_minutes(p):
    extra = " ".join(p.get("takeaways", [])) + " ".join(q + " " + a for q, a in p.get("faq", []))
    return read_minutes(p["body"], extra)


def fmt_date(d):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    y, m, day = d.split("-")
    return f"{months[int(m) - 1]} {int(day)}, {y}"


def img_tag(name, alt, cls="", eager=False, sizes="100vw", w=1600, h=1000):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="/assets/img/{name}.webp" srcset="/assets/img/{name}-sm.webp 720w, '
            f'/assets/img/{name}.webp 1600w" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{esc(alt)}"{c} {loading}>')


LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><g transform="translate(32 32)">'
        + "".join(
            f'<path transform="rotate({a})" d="M0-3C-9-8-12-20-6-27c2 2 4 3 6 3s4-1 6-3c6 7 3 19-6 24z" '
            f'fill="{"#fffaf2" if i % 2 == 0 else "#fbe9ed"}" stroke="#2f4a3a" stroke-width="2.2" stroke-linejoin="round"/>'
            for i, a in enumerate((0, 90, 180, 270)))
        + '<circle r="5.5" fill="#8fa98f" stroke="#2f4a3a" stroke-width="2"/>'
        '<circle r="1.6" fill="#2f4a3a"/></g></svg>')

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


# --------------------------------------------------------------------------
# Structured data
# --------------------------------------------------------------------------

def org_graph():
    return [
        {
            "@type": "Organization", "@id": url("/#org"), "name": SITE["name"], "url": url("/"),
            "email": SITE["email"], "logo": url("/assets/img/logo.png"),
            "founder": [{"@type": "Person", "name": n} for n in SITE["authors"]],
        },
        {
            "@type": "WebSite", "@id": url("/#website"), "name": SITE["name"], "url": url("/"),
            "publisher": {"@id": url("/#org")}, "inLanguage": "en-US",
        },
    ]


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faq]}


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

def head(page):
    canonical = url(page["path"])
    og_img = url(f"/assets/img/{page.get('img', 'hero-farmhouse')}.webp")
    graph = org_graph() + page.get("ld", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    robots = '<meta name="robots" content="noindex, follow">\n' if page.get("noindex") else ""
    art = ""
    if page.get("published"):
        art = (f'<meta property="article:published_time" content="{page["published"]}">\n'
               f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    extra_js = '<script src="/assets/js/tools.js?v=' + ASSET_V + '" defer></script>\n' if page.get("tools") else ""
    preload = ""
    if page.get("preload"):
        preload = (f'<link rel="preload" as="image" href="/assets/img/{page["preload"]}.webp" '
                   f'imagesrcset="/assets/img/{page["preload"]}-sm.webp 720w, /assets/img/{page["preload"]}.webp 1600w" imagesizes="100vw">\n')
    return f"""<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page["desc"])}">
{robots}<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{"article" if page.get("published") else "website"}">
<meta property="og:site_name" content="{SITE["name"]}">
<meta property="og:title" content="{esc(page.get("og_title", page["title"]))}">
<meta property="og:description" content="{esc(page["desc"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
{art}<meta name="theme-color" content="#2f4a3a">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500;1,9..144,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
{preload}<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
{extra_js}<script type="application/ld+json">{ld}</script>
</head>"""


def header(active):
    links = "".join(
        f'<a href="{p}"{" aria-current=\"page\"" if p == active else ""}>{n}</a>' for n, p in NAV)
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{SITE["name"]} home">{LOGO}<span>Dogwood <em>DIY</em></span></a>
    <button class="menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
    <nav class="main-nav" id="main-nav" aria-label="Main">{links}<a class="nav-cta" href="/tools/">DIY Tools</a></nav>
  </div>
</header>
<div class="nav-backdrop" aria-hidden="true"></div>
<main id="main">"""


def footer():
    cats = "".join(f'<li><a href="/category/{k}/">{c["name"]}</a></li>' for k, c in CATS.items())
    popular = "".join(f'<li><a href="/{s}/">{BY_SLUG[s]["short"]}</a></li>' for s in SITE["popular"])
    return f"""</main>
<footer class="site-footer">
  <svg class="footer-flower" viewBox="0 0 64 64" aria-hidden="true">{LOGO[LOGO.index('<g'):LOGO.rindex('</svg>')]}</svg>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/">{LOGO}<span>Dogwood <em>DIY</em></span></a>
        <p>{SITE["tagline"]} Real projects, honest costs and step-by-step guides from the Dogwood House - a 1960s brick ranch we're turning into a modern farmhouse.</p>
        <p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>
      </div>
      <div><h4>Explore</h4><ul>{cats}<li><a href="/blog/">All projects</a></li><li><a href="/tools/">DIY calculators</a></li></ul></div>
      <div><h4>Popular</h4><ul>{popular}</ul></div>
      <div><h4>Dogwood DIY</h4><ul><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/disclaimer/">Disclosure</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>&copy; 2026 {SITE["name"]}. Made with sawdust and sweet tea in North Carolina.</span><span>DIY at your own risk - always follow product directions and local codes.</span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">↑</button>
</body>
</html>
"""


def page_html(page, body):
    return head(page) + "\n" + header(page.get("nav", page["path"])) + "\n" + body + "\n" + footer()


def write(path, content):
    target = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        target = os.path.join(target, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------

def page_hero(title, lead, crumbs, eyebrow=""):
    cr = ' <span>/</span> '.join(f'<a href="{p}">{esc(n)}</a>' for n, p in crumbs[:-1])
    cr += f' <span>/</span> {esc(crumbs[-1][0])}' if len(crumbs) > 1 else ""
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    return f"""<section class="page-hero"><div class="blob b1"></div><div class="blob b2"></div>
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>{eb}
  <h1>{title}</h1><p class="lead">{lead}</p></div></section>"""


def post_card(p, delay=0):
    cat = CATS[p["cat"]]
    tags = " ".join([p["cat"]] + p.get("tags", []))
    d = f" d{delay}" if delay else ""
    return f"""<article class="card reveal{d}" data-tags="{tags}">
  <div class="media">{img_tag(p["img"], p["img_alt"], sizes="(max-width: 640px) 100vw, (max-width: 1020px) 50vw, 400px")}<span class="chip c-{p["cat"]}">{cat["name"]}</span></div>
  <div class="body"><h3><a href="/{p["slug"]}/">{p["h1"]}</a></h3><p>{p["excerpt"]}</p>
  <div class="meta"><span>{fmt_date(p.get("updated", p["date"]))}</span><span>{post_minutes(p)} min read</span></div></div>
</article>"""


def cta_band():
    return f"""<section class="section tight"><div class="wrap"><div class="cta-band reveal">
  <span class="eyebrow" style="color:var(--blossom)">Got a project question?</span>
  <h2>Stuck halfway through a project? Ask us.</h2>
  <p>Tell us what you're working on - a brick fireplace, a stubborn shrub, a bathroom that needs some love - and we'll point you to the guide (or write one).</p>
  <div class="hero-actions"><a class="btn btn-light" href="/contact/">Send us a note {ARROW}</a><a class="btn btn-ghost" href="/tools/">Try the DIY calculators</a></div>
</div></div></section>"""


# --------------------------------------------------------------------------
# Calculators (shared by /tools/ pages and embedded in posts)
# --------------------------------------------------------------------------

def field(name, label, value, step="any", unit="", typ="number", minv="0"):
    return (f'<div class="field"><label for="{{id}}-{name}">{label}{" (" + unit + ")" if unit else ""}</label>'
            f'<input id="{{id}}-{name}" name="{name}" type="{typ}" inputmode="decimal" min="{minv}" step="{step}" value="{value}"></div>')


def result(key, label):
    return f'<div class="result"><b data-out="{key}">-</b><span>{label}</span></div>'


TOOLS = {
    "schmear": {
        "slug": "german-schmear-calculator", "name": "German Schmear Mortar Calculator", "icon": "🧱",
        "short": "Mortar, cost and time for a German schmear fireplace or brick wall - with a live preview.",
        "title": "German Schmear Calculator: How Much Mortar Do You Need?",
        "desc": "Free German schmear calculator. Enter your fireplace or brick wall size and coverage to estimate mortar, buckets, cost and time - with a live schmear preview.",
        "img": "german-schmear-fireplace", "related": "german-schmear-fireplace",
    },
    "paint": {
        "slug": "paint-calculator", "name": "Room Paint Calculator", "icon": "🎨",
        "short": "Gallons of paint and primer for any room, minus doors and windows.",
        "title": "Room Paint Calculator: How Many Gallons Do I Need?",
        "desc": "Work out how many gallons of paint and primer a room needs. Enter wall size, doors, windows and coats - perfect after wallpaper removal or a cabinet makeover.",
        "img": "wallpaper-paint-roller", "related": "simple-wallpaper-removal",
    },
    "wallpaper": {
        "slug": "wallpaper-removal-calculator", "name": "Wallpaper Remover Mix Calculator", "icon": "🧽",
        "short": "How much homemade remover solution to mix - fabric softener or vinegar recipe.",
        "title": "Homemade Wallpaper Remover Calculator (Fabric Softener or Vinegar)",
        "desc": "Mix the right amount of homemade wallpaper remover. Enter room size and layers to get gallons of solution, the hot water ratio and a time estimate.",
        "img": "wallpaper-paint-roller", "related": "simple-wallpaper-removal",
    },
    "caulk": {
        "slug": "caulk-grout-calculator", "name": "Caulk & Grout Paint Calculator", "icon": "🛁",
        "short": "Tubes of caulk for a tub or shower and bottles of grout paint for any tiled area.",
        "title": "Caulk & Grout Paint Calculator for Tubs, Showers and Tile",
        "desc": "Estimate tubes of caulk for a bathtub or shower and bottles of grout paint for tile floors and walls. Free bathroom refresh calculator.",
        "img": "grout-tile", "related": "replace-old-caulk-bathtub",
    },
    "mulch": {
        "slug": "mulch-soil-calculator", "name": "Mulch & Soil Calculator", "icon": "🌱",
        "short": "Cubic yards and bags of mulch or soil for a new flower bed.",
        "title": "Mulch & Soil Calculator: Cubic Yards and Bags for Flower Beds",
        "desc": "Calculate how much mulch, compost or garden soil you need in cubic yards and 2 or 3 cu ft bags - ideal after removing old shrubs.",
        "img": "garden-soil", "related": "remove-overgrown-shrubs-easy",
    },
    "budget": {
        "slug": "diy-project-budget-planner", "name": "DIY Project Budget Planner", "icon": "📋",
        "short": "List materials, add a buffer and keep a running total - saved in your browser.",
        "title": "DIY Project Budget Planner (Free, Printable)",
        "desc": "Plan your next DIY project budget. Add materials and quantities, include a contingency buffer and print your list - it saves automatically in your browser.",
        "img": "woodworking", "related": "1960s-ranch-house-renovation-ideas",
    },
}


def tool_html(key, uid):
    t = TOOLS[key]
    if key == "schmear":
        inner = f"""<div class="tool-grid">{field("width", "Brick area width", 6, unit="ft")}{field("height", "Brick area height", 5, unit="ft")}
<div class="field"><label for="{{id}}-coats">Coats</label><select id="{{id}}-coats" name="coats"><option value="1">1 coat</option><option value="1.5" selected>1 coat + touch-ups</option><option value="2">2 full coats</option></select></div>
{field("price", "Mortar price per gallon", 25, unit="$")}</div>
<div class="field"><label for="{{id}}-coverage">Mortar coverage - how much brick do you want to hide?</label>
<div class="range-row"><input id="{{id}}-coverage" name="coverage" type="range" min="20" max="95" value="60" data-unit="%"><output for="{{id}}-coverage">60%</output></div></div>
<canvas class="schmear-canvas" width="960" height="540" role="img" aria-label="Live preview of brick with German schmear mortar coverage"></canvas>
<div class="results" style="margin-top:16px">{result("area", "Brick surface")}{result("gallons", "Mortar needed")}{result("buckets", "1-gal buckets to buy")}{result("cost", "Estimated cost")}{result("time", "Working time")}</div>
<p class="tool-note">Based on roughly 18 sq ft per gallon of pre-mixed mortar at full coverage. Cost includes about $22 for a sponge, putty knife and drop cloth. Slide coverage to preview the look.</p>"""
    elif key == "paint":
        inner = f"""<div class="tool-grid">{field("length", "Room length", 12, unit="ft")}{field("width", "Room width", 10, unit="ft")}{field("height", "Wall height", 8, unit="ft")}{field("doors", "Doors", 1, step="1")}{field("windows", "Windows", 2, step="1")}
<div class="field"><label for="{{id}}-coats">Coats</label><select id="{{id}}-coats" name="coats"><option value="1">1</option><option value="2" selected>2</option><option value="3">3</option></select></div></div>
<label style="display:flex;gap:10px;align-items:center;font-weight:600;margin-bottom:12px"><input type="checkbox" name="ceiling"> Paint the ceiling too</label>
<div class="results">{result("wall", "Paintable area")}{result("gallons", "Paint needed")}{result("buy", "What to buy")}{result("primer", "Primer (1 coat)")}</div>
<p class="tool-note">Assumes 350 sq ft per gallon, 21 sq ft per door and 15 sq ft per window. Textured or freshly patched drywall drinks more - round up.</p>"""
    elif key == "wallpaper":
        inner = f"""<div class="tool-grid">{field("length", "Room length", 8, unit="ft")}{field("width", "Room width", 6, unit="ft")}{field("height", "Wall height", 8, unit="ft")}
<div class="field"><label for="{{id}}-layers">Layers of paper</label><select id="{{id}}-layers" name="layers"><option value="1">1 layer</option><option value="1.6">2 layers</option><option value="2.2">3+ layers</option></select></div>
<div class="field"><label for="{{id}}-recipe">Recipe</label><select id="{{id}}-recipe" name="recipe"><option value="softener">Fabric softener (3:1)</option><option value="vinegar">White vinegar (1:1)</option></select></div></div>
<div class="results">{result("area", "Wall area")}{result("gallons", "Solution to mix")}{result("mix1", "Hot water")}{result("mix2", "Add")}{result("time", "Rough working time")}</div>
<p class="tool-note">Mix in small batches - the solution works best hot. Plan on about a gallon for every 80 sq ft per layer, re-wetting stubborn spots.</p>"""
    elif key == "caulk":
        inner = f"""<h4 style="margin:6px 0 0">Caulk</h4><div class="tool-grid">{field("linear", "Total joint length", 16, unit="ft")}
<div class="field"><label for="{{id}}-bead">Bead size</label><select id="{{id}}-bead" name="bead"><option value="0.125">1/8 in</option><option value="0.25" selected>1/4 in</option><option value="0.375">3/8 in</option><option value="0.5">1/2 in</option></select></div></div>
<div class="results">{result("pertube", "Per 10.1 oz tube")}{result("tubes", "Tubes to buy")}</div>
<h4 style="margin:22px 0 0">Grout paint</h4><div class="tool-grid">{field("tilearea", "Tiled area", 40, unit="sq ft")}{field("tilesize", "Tile size", 4, unit="in")}{field("perbottle", "Coverage per bottle", 150, unit="linear ft")}</div>
<div class="results">{result("gline", "Grout lines")}{result("bottles", "Bottles to buy")}</div>
<p class="tool-note">A standard 5 ft tub has about 14-16 ft of joint (back wall plus two ends, plus a little up each corner). Caulk adds a 15% waste factor. Grout coverage varies by brand and joint width - check your bottle and adjust.</p>"""
    elif key == "mulch":
        inner = f"""<div class="tool-grid">{field("length", "Bed length", 20, unit="ft")}{field("width", "Bed width", 4, unit="ft")}
<div class="field"><label for="{{id}}-depth">Depth</label><select id="{{id}}-depth" name="depth"><option value="2">2 in (top-up)</option><option value="3" selected>3 in (mulch)</option><option value="4">4 in</option><option value="6">6 in (new soil)</option><option value="8">8 in (raised bed)</option></select></div></div>
<div class="results">{result("area", "Bed area")}{result("yards", "Bulk volume")}{result("bags2", "2 cu ft bags")}{result("bags3", "3 cu ft bags")}</div>
<p class="tool-note">Bulk is usually cheaper above about 2 cubic yards. Keep mulch a few inches away from foundations and plant stems.</p>"""
    else:  # budget
        inner = """<table class="budget-table"><thead><tr><th>Item</th><th style="width:90px">Qty</th><th style="width:120px">Unit price</th><th style="width:44px"></th></tr></thead><tbody></tbody></table>
<div class="budget-actions"><button type="button" class="btn btn-sm" data-add>+ Add item</button><button type="button" class="btn btn-sm btn-outline" data-print>Print list</button><button type="button" class="btn btn-sm btn-outline" data-clear>Start over</button></div>
<div class="tool-grid" style="max-width:260px"><div class="field"><label for="{id}-buffer">Contingency buffer</label><div class="range-row"><input id="{id}-buffer" name="buffer" type="range" min="0" max="30" value="15" data-unit="%"><output for="{id}-buffer">15%</output></div></div></div>
<div class="results">""" + result("subtotal", "Materials") + result("buffer", "Buffer") + result("total", "Plan to spend") + """</div>
<p class="tool-note">Your list saves automatically in this browser. Nothing is sent anywhere.</p>"""
    inner = inner.replace("{id}", uid)
    return f'<div class="tool" data-tool="{key}"><h3><span aria-hidden="true">{t["icon"]}</span> {t["name"]}</h3>{inner}</div>'


# --------------------------------------------------------------------------
# Body token expansion
# --------------------------------------------------------------------------

def expand(body, ctx):
    n = {"i": 0}

    def tool(m):
        n["i"] += 1
        ctx["tools"] = True
        return tool_html(m.group(1), f"t{n['i']}")

    def figure(m):
        name, alt, cap = (m.group(1).split("|") + ["", ""])[:3]
        c = f"<figcaption>{cap}</figcaption>" if cap else ""
        return f'<figure class="reveal">{img_tag(name, alt, sizes="(max-width: 1020px) 100vw, 760px")}{c}</figure>'

    def link(m):
        p = BY_SLUG[m.group(1)]
        return f'<a href="/{p["slug"]}/">{m.group(2) or p["short"]}</a>'

    body = re.sub(r"\[\[tool_link:(\w+)\]\]", lambda m: f'<a href="/tools/{TOOLS[m.group(1)]["slug"]}/">{TOOLS[m.group(1)]["name"].lower()}</a>', body)
    body = re.sub(r"\[\[tool:(\w+)\]\]", tool, body)
    body = re.sub(r"\[\[img:([^\]]+)\]\]", figure, body)
    body = re.sub(r"\[\[post:([\w-]+)(?:\|([^\]]+))?\]\]", link, body)

    toc = []

    def h2(m):
        attrs, text = m.group(1), m.group(2)
        if "id=" in attrs:
            return m.group(0)
        hid = slugify(text)
        toc.append((hid, strip_tags(text)))
        return f'<h2 id="{hid}"{attrs}>{text}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, body)
    body = body.replace("<p><em>Disclosure", '<p class="note"><em>Disclosure')
    body = body.replace("<p>", '<p class="dropcap">', 1)
    return body, toc


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------

def build_post(p):
    cat = CATS[p["cat"]]
    ctx = {}
    body, toc = expand(p["body"], ctx)
    path = f'/{p["slug"]}/'
    updated = p.get("updated", p["date"])
    faq_html = ""
    ld = [crumbs_ld([("Home", "/"), (cat["name"], f'/category/{p["cat"]}/'), (p["short"], path)]),
          {"@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "image": url(f'/assets/img/{p["img"]}.webp'),
           "datePublished": p["date"], "dateModified": updated, "mainEntityOfPage": url(path),
           "author": {"@type": "Person", "name": p.get("author", SITE["authors"][0]), "url": url("/about/")},
           "publisher": {"@id": url("/#org")}, "articleSection": cat["name"]}]
    if p.get("faq"):
        ld.append(faq_ld(p["faq"]))
        items = "".join(f"<details><summary>{esc(q)}</summary><div><p>{a}</p></div></details>" for q, a in p["faq"])
        faq_html = f'<section class="faq"><h2 id="faq">Frequently asked questions</h2>{items}</section>'
        toc.append(("faq", "FAQ"))
    takeaways = ""
    if p.get("takeaways"):
        lis = "".join(f"<li>{t}</li>" for t in p["takeaways"])
        takeaways = f'<div class="takeaways"><h2 id="quick-answer">The short version</h2><ul>{lis}</ul></div>'
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    related = [x for x in POSTS if x["slug"] != p["slug"] and (x["cat"] == p["cat"] or x["slug"] in p.get("related", []))]
    related = sorted(related, key=lambda x: (x["slug"] not in p.get("related", []), x["date"]))[:3]
    if len(related) < 3:
        related += [x for x in POSTS if x["slug"] != p["slug"] and x not in related][: 3 - len(related)]
    rel_html = "".join(post_card(x, i) for i, x in enumerate(related))
    tool_link = ""
    if p.get("tool"):
        t = TOOLS[p["tool"]]
        tool_link = f'<div class="side-box"><h3>Handy calculator</h3><p style="margin:0 0 12px;font-size:.95rem">{t["short"]}</p><a class="link-arrow" href="/tools/{t["slug"]}/">{t["name"]}</a></div>'
    author = p.get("author", SITE["authors"][0])
    initials = "".join(w[0] for w in author.split()[:2])
    share_u = esc(url(path))
    share_t = esc(p["h1"])
    page = {
        "path": path, "title": p["title"], "desc": p["desc"], "img": p["img"], "ld": ld,
        "published": p["date"], "modified": updated, "tools": ctx.get("tools"), "nav": "/blog/", "preload": p["img"],
    }
    original = f' · Originally published {fmt_date(p["date"])}' if p.get("updated") and p["updated"] != p["date"] else ""
    content = f"""<section class="article-hero"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <a href="/category/{p["cat"]}/">{cat["name"]}</a></nav>
  <a class="chip c-{p["cat"]}" href="/category/{p["cat"]}/">{cat["name"]}</a>
  <h1 style="margin-top:14px">{p["h1"]}</h1>
  <div class="article-meta"><span class="author"><span class="avatar">{initials}</span>{author}</span><span>Updated {fmt_date(updated)}{original}</span><span>{post_minutes(p)} min read</span></div>
</div>
<div class="article-cover">{img_tag(p["img"], p["img_alt"], eager=True, sizes="(max-width: 1100px) 100vw, 1100px")}</div></section>
<div class="article-layout">
  <article class="prose">
    {takeaways}
    {body}
    {faq_html}
    <div class="share"><span>Share this project:</span>
      <a href="https://www.pinterest.com/pin/create/button/?url={share_u}&amp;description={share_t}" target="_blank" rel="noopener">Pinterest</a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={share_u}" target="_blank" rel="noopener">Facebook</a>
      <a href="mailto:?subject={share_t}&amp;body={share_u}">Email</a>
      <button type="button" data-copy>Copy link</button></div>
  </article>
  <aside class="sidebar"><div class="sticky">
    <nav class="side-box toc" aria-label="On this page"><h3>On this page</h3><ol>{toc_html}</ol></nav>
    {tool_link}
    <div class="side-box"><div class="author-box"><span class="avatar">{initials}</span><div><strong>{author}</strong><p>Half of the Dogwood DIY duo. Renovating a 1960s brick ranch in North Carolina with Jared - one weekend project at a time.</p><a class="link-arrow" href="/about/" style="font-size:.9rem">Our story</a></div></div></div>
  </div></aside>
</div>
<section class="section alt"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Keep going</span><h2>More projects you'll like</h2></div><a class="link-arrow" href="/category/{p["cat"]}/">All {cat["name"]} projects</a></div>
<div class="grid grid-3">{rel_html}</div></div></section>"""
    write(path, page_html(page, content))


def build_home():
    feat = BY_SLUG[SITE["featured"]]
    finder_tags = [("all", "Everything"), ("fireplace", "Brick & fireplace"), ("bathroom", "Bathroom"),
                   ("walls", "Walls & paint"), ("yard", "Yard & garden"), ("decor", "Decor & seasonal"), ("kitchen", "Kitchen")]
    finder = "".join(f'<button type="button" data-tag="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in finder_tags)
    cards = "".join(post_card(p, i % 3) for i, p in enumerate([x for x in POSTS if x["slug"] != feat["slug"]][:9]))
    cat_tiles = "".join(
        f"""<a class="cat-tile reveal d{i}" href="/category/{k}/">{img_tag(c["img"], c["name"], sizes="(max-width: 640px) 100vw, 33vw")}
<span class="count">{sum(1 for p in POSTS if p["cat"] == k)} projects</span><div class="inner"><h3>{c["name"]}</h3><p>{c["blurb"]}</p></div></a>"""
        for i, (k, c) in enumerate(CATS.items()))
    tools = "".join(
        f'<a class="tool-card reveal d{i % 3}" href="/tools/{t["slug"]}/"><div class="ico" aria-hidden="true">{t["icon"]}</div><h3>{t["name"]}</h3><p>{t["short"]}</p></a>'
        for i, t in enumerate(TOOLS.values()))
    words = ["German schmear", "Shrub removal", "Painted grout", "Fresh caulk", "Boxwood wreaths", "Wallpaper begone", "Red clay gardening", "Porch makeovers", "Farmhouse style"]
    marquee = "".join(f"<span>{w}</span>" for w in words * 2)
    ld = [{"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": url(f'/{p["slug"]}/'), "name": p["h1"]} for i, p in enumerate(POSTS[:10])]}]
    page = {"path": "/", "title": SITE["home_title"], "desc": SITE["home_desc"], "img": "hero-farmhouse", "ld": ld, "preload": "hero-farmhouse"}
    content = f"""<section class="hero">
  <div class="hero-bg">{img_tag("hero-farmhouse", "White farmhouse-style home with a wraparound porch and green lawn", eager=True)}</div>
  <canvas id="petals" aria-hidden="true"></canvas>
  <div class="wrap"><div class="hero-content">
    <span class="eyebrow">Home renovation &amp; garden DIY</span>
    <h1>Turning a 1960s brick ranch into our <em>dream farmhouse</em>.</h1>
    <p class="lead">We're Jared and Stephanie. We fix, paint, schmear, plant and pull things out of the ground on a real-life budget - and write down exactly how we did it so you can too.</p>
    <div class="hero-actions"><a class="btn" href="/blog/">Browse projects {ARROW}</a><a class="btn btn-ghost" href="/about/">Meet the Dogwood House</a></div>
    <div class="hero-stats">
      <div><b data-count="{len(POSTS)}">{len(POSTS)}</b><span>step-by-step guides</span></div>
      <div><b>$<span data-count="55">55</span></b><span>our German schmear fireplace</span></div>
      <div><b data-count="{len(TOOLS)}">{len(TOOLS)}</b><span>free DIY calculators</span></div>
    </div>
  </div></div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>
<div class="marquee" aria-hidden="true"><div class="track">{marquee}</div></div>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Most-loved project</span><h2>Start with the one everyone asks about</h2></div></div>
  <article class="feature-card reveal">
    <div class="media">{img_tag(feat["img"], feat["img_alt"], sizes="(max-width: 820px) 100vw, 640px")}</div>
    <div class="body"><span class="chip c-{feat["cat"]}" style="align-self:flex-start">{CATS[feat["cat"]]["name"]}</span>
      <h3><a href="/{feat["slug"]}/">{feat["h1"]}</a></h3><p>{feat["excerpt"]}</p>
      <span class="link-arrow">Read the tutorial</span></div>
  </article>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Project finder</span><h2>What are you tackling this weekend?</h2></div><p>Pick a room or job and we'll show you the guides that fit.</p></div>
  <div class="finder reveal" data-finder="#home-posts" role="group" aria-label="Filter projects">{finder}</div>
  <div class="grid grid-3" id="home-posts">{cards}</div>
  <p style="text-align:center;margin-top:40px"><a class="btn" href="/blog/">See every project {ARROW}</a></p>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Explore</span><h2>Three ways to make a house a home</h2></div></div>
  <div class="grid grid-3">{cat_tiles}</div>
</div></section>

<section class="section dark"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow" style="color:var(--blossom)">Free &amp; interactive</span><h2>Measure twice. Calculate once.</h2></div><p>Our calculators answer the "how much do I buy?" question before you drive to the hardware store.</p></div>
  <div class="grid grid-3">{tools}</div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="stack reveal">{img_tag("brick-house", "Red brick house surrounded by tall trees at sunset", sizes="(max-width: 900px) 100vw, 560px")}
    {img_tag("dogwood-blossom", "White dogwood blossoms in spring", cls="inset", sizes="260px", w=1205, h=1600)}
    <div class="badge-float"><b>2018</b> the year we found her</div></div>
  <div class="reveal d1"><span class="eyebrow">Our story</span><h2>Hi, we're Jared &amp; Stephanie.</h2>
    <p>We swung our first hammers together back in 2008 in a 1960s brick ranch we bought with more enthusiasm than money. A few houses later, a week before Thanksgiving, Stephanie found another fixer-upper on Realtor.com - an established neighborhood, mature trees, two brick fireplaces and a front yard full of shrubs that hadn't been trimmed since the '90s.</p>
    <p>We named her the Dogwood House. Dogwood DIY is where we share every project: what worked, what didn't, what it really cost, and what we'd do differently.</p>
    <a class="btn" href="/about/">Read our story {ARROW}</a></div>
</div></section>
{cta_band()}"""
    write("/home.html", page_html(page, content))


def build_blog():
    finder_tags = [("all", "All")] + [(k, c["name"]) for k, c in CATS.items()]
    finder = "".join(f'<button type="button" data-tag="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in finder_tags)
    cards = "".join(post_card(p, i % 3) for i, p in enumerate(POSTS))
    page = {"path": "/blog/", "title": "All DIY Projects & Home Renovation Guides | Dogwood DIY",
            "desc": "Every Dogwood DIY project in one place: German schmear, shrub removal, bathroom updates, wallpaper removal, farmhouse decor and beginner gardening guides.",
            "ld": [crumbs_ld([("Home", "/"), ("Projects", "/blog/")])]}
    content = page_hero("Every project from the Dogwood House", "Brick, bathrooms, walls, gardens and the occasional wreath. Filter by category or just scroll and get inspired.",
                        [("Home", "/"), ("Projects", "/blog/")], "The project archive") + \
        f"""<section class="section"><div class="wrap"><div class="finder" data-finder="#all-posts" role="group" aria-label="Filter by category">{finder}</div>
<div class="grid grid-3" id="all-posts">{cards}</div></div></section>{cta_band()}"""
    write("/blog/", page_html(page, content))


def build_categories():
    for k, c in CATS.items():
        posts = [p for p in POSTS if p["cat"] == k]
        cards = "".join(post_card(p, i % 3) for i, p in enumerate(posts))
        path = f"/category/{k}/"
        page = {"path": path, "title": c["title"], "desc": c["desc"], "img": c["img"], "nav": "/blog/",
                "ld": [crumbs_ld([("Home", "/"), (c["name"], path)]),
                       {"@type": "CollectionPage", "name": c["name"], "url": url(path)}]}
        content = page_hero(c["h1"], c["intro"], [("Home", "/"), ("Projects", "/blog/"), (c["name"], path)], f"{len(posts)} projects") + \
            f'<section class="section"><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>{cta_band()}'
        write(path, page_html(page, content))


def build_tools():
    cards = "".join(
        f'<a class="tool-card reveal d{i % 3}" href="/tools/{t["slug"]}/"><div class="ico" aria-hidden="true">{t["icon"]}</div><h3>{t["name"]}</h3><p>{t["short"]}</p></a>'
        for i, t in enumerate(TOOLS.values()))
    page = {"path": "/tools/", "title": "Free DIY Calculators for Home & Garden Projects | Dogwood DIY",
            "desc": "Free interactive DIY calculators: German schmear mortar, room paint, wallpaper remover mix, caulk and grout paint, mulch and soil, and a project budget planner.",
            "img": "woodworking", "ld": [crumbs_ld([("Home", "/"), ("DIY Tools", "/tools/")])]}
    content = page_hero("Free DIY calculators", "Quick answers to \"how much do I need?\" - built from the numbers we use on our own projects.",
                        [("Home", "/"), ("DIY Tools", "/tools/")], "Interactive tools") + \
        f'<section class="section"><div class="wrap"><div class="grid grid-3">{cards}</div></div></section>{cta_band()}'
    write("/tools/", page_html(page, content))
    for key, t in TOOLS.items():
        path = f'/tools/{t["slug"]}/'
        rel = BY_SLUG[t["related"]]
        others = "".join(f'<li><a href="/tools/{o["slug"]}/">{o["name"]}</a></li>' for kk, o in TOOLS.items() if kk != key)
        page = {"path": path, "title": t["title"], "desc": t["desc"], "img": t["img"], "tools": True, "nav": "/tools/",
                "ld": [crumbs_ld([("Home", "/"), ("DIY Tools", "/tools/"), (t["name"], path)]),
                       {"@type": "WebApplication", "name": t["name"], "url": url(path), "applicationCategory": "UtilitiesApplication",
                        "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]}
        content = page_hero(t["name"], t["short"], [("Home", "/"), ("DIY Tools", "/tools/"), (t["name"], path)], "Free calculator") + f"""
<div class="article-layout"><div class="prose" style="font-size:1rem">{tool_html(key, "t1")}
<p>Want the full walkthrough? Read <a href="/{rel["slug"]}/">{rel["h1"]}</a> for the step-by-step method, the supplies we used and the mistakes to avoid.</p></div>
<aside class="sidebar"><div class="side-box"><h3>More calculators</h3><ul style="margin:0;padding-left:18px">{others}</ul></div>
<div class="side-box"><h3>Related guide</h3><a href="/{rel["slug"]}/">{img_tag(rel["img"], rel["img_alt"], sizes="300px")}</a><p style="margin:12px 0 0;font-weight:700"><a href="/{rel["slug"]}/">{rel["short"]}</a></p></div></aside></div>"""
        write(path, page_html(page, content))


def build_about():
    a = ABOUT
    page = {"path": "/about/", "title": a["title"], "desc": a["desc"], "img": "brick-house",
            "ld": [crumbs_ld([("Home", "/"), ("About", "/about/")]),
                   {"@type": "AboutPage", "name": "About Dogwood DIY", "url": url("/about/"), "about": {"@id": url("/#org")}}]}
    content = page_hero(a["h1"], a["lead"], [("Home", "/"), ("About", "/about/")], "About Dogwood DIY") + a["body"] + cta_band()
    write("/about/", page_html(page, content))


def build_contact():
    page = {"path": "/contact/", "title": "Contact Dogwood DIY | Questions, Collaborations & Project Help",
            "desc": f"Get in touch with Jared and Stephanie at Dogwood DIY. Ask a project question, suggest a tutorial or talk collaborations - email {SITE['email']}.",
            "ld": [crumbs_ld([("Home", "/"), ("Contact", "/contact/")]), {"@type": "ContactPage", "url": url("/contact/")}]}
    content = page_hero("Say hello", "Project questions, tutorial requests, collaboration ideas or a photo of your own German schmear fireplace - we read everything.",
                        [("Home", "/"), ("Contact", "/contact/")], "Contact") + f"""
<section class="section"><div class="wrap split" style="align-items:start">
  <div class="reveal"><h2>We'd love to hear from you</h2>
    <p>We're a two-person team renovating a house in our spare time, so replies can take a few days - but we do answer. If your question is about a specific project, include a photo and the products you're using; it helps us give you a useful answer.</p>
    <ul class="contact-list">
      <li><span class="ico" aria-hidden="true">✉️</span><div><strong>Email</strong><br><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></li>
      <li><span class="ico" aria-hidden="true">🏡</span><div><strong>Where we are</strong><br>North Carolina, USA (we don't do in-person projects or quotes)</div></li>
      <li><span class="ico" aria-hidden="true">🤝</span><div><strong>Brands &amp; collaborations</strong><br>Products we'd genuinely use in the Dogwood House only.</div></li>
    </ul></div>
  <div class="form-card reveal d1">
    <p class="notice" data-form-status hidden></p>
    <form action="/contact.php" method="post">
      <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>Project question</option><option>Tutorial request</option><option>Collaboration</option><option>Something else</option></select></div>
      <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>
      <div class="hp" aria-hidden="true"><label for="c-web">Website</label><input id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
      <button class="btn" type="submit">Send message {ARROW}</button>
    </form></div>
</div></section>"""
    write("/contact/", page_html(page, content))


def build_plain(path, data):
    page = {"path": path, "title": data["title"], "desc": data["desc"],
            "ld": [crumbs_ld([("Home", "/"), (data["h1"], path)])]}
    content = page_hero(data["h1"], data["lead"], [("Home", "/"), (data["h1"], path)]) + f'<div class="plain prose">{data["body"]}</div>'
    write(path, page_html(page, content))


def build_404():
    cards = "".join(post_card(BY_SLUG[s], i) for i, s in enumerate(SITE["popular"][:3]))
    page = {"path": "/404.html", "title": "Page not found | Dogwood DIY", "desc": "That page has moved or never existed.", "noindex": True}
    content = page_hero("Well, that didn't go to plan.", "This page has wandered off like a runaway shrub root. Try one of our most popular projects instead.",
                        [("Home", "/"), ("Not found", "/404.html")], "404") + \
        f'<section class="section"><div class="wrap"><div class="grid grid-3">{cards}</div><p style="text-align:center;margin-top:36px"><a class="btn" href="/">Back to the homepage {ARROW}</a></p></div></section>'
    write("/404.html", page_html(page, content))


def build_meta():
    urls = [("/", "2026-10-17", "1.0")]
    urls += [(f'/{p["slug"]}/', p.get("updated", p["date"]), "0.8") for p in POSTS]
    urls += [("/blog/", "2026-10-17", "0.7"), ("/tools/", "2026-10-17", "0.7"), ("/about/", "2026-10-17", "0.6"), ("/contact/", "2026-10-17", "0.4")]
    urls += [(f'/tools/{t["slug"]}/', "2026-10-17", "0.6") for t in TOOLS.values()]
    urls += [(f"/category/{k}/", "2026-10-17", "0.5") for k in CATS]
    urls += [(p, "2026-10-17", "0.2") for p in ("/disclaimer/", "/privacy-policy/", "/terms/")]
    body = "".join(f"<url><loc>{url(u)}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {url('/sitemap.xml')}\n")
    favicon = LOGO.replace('<svg viewBox="0 0 64 64" aria-hidden="true">', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">')
    write("/favicon.svg", favicon)


def copy_static():
    for d in ("assets",):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d), dirs_exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), os.path.join(OUT, f))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_static()
    for p in POSTS:
        build_post(p)
    build_home()
    build_blog()
    build_categories()
    build_tools()
    build_about()
    build_contact()
    build_plain("/disclaimer/", DISCLAIMER)
    build_plain("/privacy-policy/", PRIVACY)
    build_plain("/terms/", TERMS)
    build_404()
    build_meta()
    n = sum(len([f for f in fs if f.endswith(".html")]) for _, _, fs in os.walk(OUT))
    print(f"built {n} html files, {len(POSTS)} posts -> {OUT}")


if __name__ == "__main__":
    main()
