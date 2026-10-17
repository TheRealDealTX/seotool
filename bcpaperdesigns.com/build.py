#!/usr/bin/env python3
"""Static site generator for bcpaperdesigns.com.

Writes the site into ./public. Content lives in ./content (themes_a.py,
themes_b.py, blog.py); constants in siteconfig.py. Standard library + Pillow
(only for reading image sizes and drawing the icons/OG image).
"""
import html
import importlib.util
import json
import os
import re
import shutil
from datetime import date

from siteconfig import (COLLECTIONS, FEATURED, NAV, PRODUCT_ALIASES, SITE,
                        THEME_TAGS)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
IMG_DIR = os.path.join(OUT, "assets", "img")
TODAY = date.today().isoformat()
ORIGIN = SITE["origin"]
EMAIL = SITE["email"]
ASSET_V = "3"


def load(name, var):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "content", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, var)


THEMES = load("themes_a", "THEMES") + load("themes_b", "THEMES")
BY_SLUG = {t["slug"]: t for t in THEMES}
POSTS = sorted(load("blog", "POSTS"), key=lambda p: p["date"], reverse=True)
PAGES = []  # (path, lastmod, priority) for sitemap.xml

esc = html.escape


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", strip_tags(s).lower()).strip("-")[:60]


_sizes = {}


def img_size(key):
    if key not in _sizes:
        from PIL import Image
        with Image.open(os.path.join(IMG_DIR, key + ".webp")) as im:
            _sizes[key] = im.size
    return _sizes[key]


def img(key, alt, cls="", lazy=True, sizes=None, extra=""):
    w, h = img_size(key)
    return (f'<img src="/assets/img/{key}.webp" alt="{esc(alt)}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}'
            f'{f" class=\"{cls}\"" if cls else ""}{extra}>')


# ---------------------------------------------------------------- icons
ICONS = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "chev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M2 5c4 2 16 2 20 0"/><path d="M5 6v6l2.5 4L10 12V6.6M14 6.6V12l2.5 4L19 12V6"/></svg>',
    "cake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21h16v-8a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2z"/><path d="M4 16c2 1.5 4 1.5 5.3 0 1.4 1.5 4 1.5 5.4 0 1.3 1.5 3.3 1.5 5.3 0M12 11V7M12 4.5v-.01"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M8 14h2M14 14h2M8 17h2"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2z"/></svg>',
    "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
    "print": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M7 9V3h10v6M7 17H4v-6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v6h-3"/><path d="M7 14h10v7H7z"/></svg>',
}

LOGO = ('<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true">'
        '<path fill="#ff6f61" d="M24 2l4.2 3.3 5.3-.6 2.3 4.8 4.9 2.2-.5 5.3L43.5 21l-1.9 5 2 5-4.2 3.2.3 5.3-5 2.1-2.4 4.8-5.3-.7L23.9 47l-4.2-3.3-5.3.6-2.3-4.8-4.9-2.2.5-5.3L4.5 27l1.9-5-2-5 4.2-3.2-.3-5.3 5-2.1 2.4-4.8 5.3.7z"/>'
        '<circle cx="24" cy="24" r="15.5" fill="none" stroke="#fff" stroke-width="1.4" stroke-dasharray="2.2 2.4"/>'
        '<text x="24" y="29.5" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-style="italic" font-weight="700" font-size="17" fill="#fff">bc</text></svg>')


def logo(tag="a"):
    return (f'<a class="logo" href="/" aria-label="{SITE["name"]} home">{LOGO}'
            f'<span class="logo-text">BC Paper<small>Designs &middot; Party Studio</small></span></a>')


EDGE = ('<svg class="edge {cls}" viewBox="0 0 1440 42" preserveAspectRatio="none" aria-hidden="true">'
        '<path fill="currentColor" d="M0 42V20c60 8 120 14 180 8s120-22 180-20 120 18 180 20 120-14 180-18 120 8 180 12 120 4 180-2 120-16 180-14 120 12 180 14V42z"/></svg>')


def edge(cls="edge--top"):
    return EDGE.format(cls=cls)


BUNTING_COLORS = ["#ff6f61", "#ffcf5a", "#5cc9b5", "#ab97ff", "#8fd3ff", "#ffc6c0"]


def bunting_strip(n=22, colors=None):
    """Decorative swinging bunting (static SVG; CSS animates each flag)."""
    colors = colors or BUNTING_COLORS
    w = 1440 / n
    parts = ['<div class="bunting" aria-hidden="true"><svg viewBox="0 0 1440 64" preserveAspectRatio="none">',
             '<path d="M0 6 Q360 30 720 14 T1440 8" fill="none" stroke="#2a2140" stroke-opacity=".35" stroke-width="2"/>']
    for i in range(n):
        x = i * w + 6
        t = (i * w) / 1440
        y = 6 + 24 * (1 - (2 * t - 1) ** 2) * 0.6
        parts.append(f'<path class="flag" style="animation-delay:-{i * 0.23:.2f}s" fill="{colors[i % len(colors)]}" '
                     f'd="M{x:.1f} {y:.1f}h{w - 12:.1f}l-{(w - 12) / 2:.1f} 40z"/>')
    parts.append("</svg></div>")
    return "".join(parts)


def shapes(seed=0, palette=None):
    p = palette or ["#ffcf5a", "#ff6f61", "#5cc9b5", "#ab97ff", "#8fd3ff"]
    spots = [("s-circle", "6%", "12%", 26), ("s-tri", "88%", "18%", 30), ("s-ring", "46%", "6%", 34),
             ("s-squig", "80%", "78%", 64), ("s-circle", "93%", "52%", 16), ("s-tri", "4%", "70%", 24),
             ("s-ring", "58%", "88%", 26), ("s-circle", "36%", "92%", 14)]
    out = ['<div class="float-shapes" aria-hidden="true">']
    for i, (cls, x, y, s) in enumerate(spots):
        c = p[(i + seed) % len(p)]
        out.append(f'<i style="left:{x};top:{y}"><i class="{cls} bob" style="--c:{c};--s:{s}px;--d:{6 + i % 4}s"></i></i>')
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------- layout
def nav_html(current):
    items = []
    for label, href, sub in NAV:
        active = current.startswith(href) and href != "/"
        if sub:
            sid = "sub-" + slugify(label)
            links = "".join(f'<li><a href="{h}">{esc(t)}<span>{esc(d)}</span></a></li>' for t, h, d in sub)
            items.append(f'<li class="has-sub"><button class="nav-sub-toggle" type="button" aria-expanded="false" aria-controls="{sid}">'
                         f'{label}{ICONS["chev"]}</button><ul class="sub" id="{sid}">{links}</ul></li>')
        else:
            cur = ' aria-current="page"' if active else ""
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return (f'<nav class="site-nav" id="site-nav" aria-label="Main"><ul>{"".join(items)}</ul>'
            f'<div class="nav-cta"><a class="btn btn--sm" href="/contact/">Contact us</a></div>'
            f'<div class="mnav-extra"><strong>Planning a party?</strong><br>Email us at <a href="mailto:{EMAIL}">{EMAIL}</a></div></nav>')


def header(current):
    return (f'<a class="skip" href="#main">Skip to content</a>'
            f'<div class="read-progress" aria-hidden="true"></div>'
            f'<header class="site-header"><div class="wrap header-inner">{logo()}'
            f'<button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>'
            f'{nav_html(current)}</div></header><button class="nav-backdrop" type="button" tabindex="-1" aria-label="Close menu"></button>')


def footer():
    themes_b = [t for t in THEMES if t["occasion"] in ("baby-shower",)][:5]
    themes_bd = [t for t in THEMES if t["occasion"] == "birthday"][:5]
    li = lambda items: "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for t, h in items)
    return f"""<footer class="site-footer"><div class="wrap"><div class="foot-grid">
<div>{logo()}<p class="foot-about">Theme guides, DIY paper decorations and free planning tools for baby showers and kids' birthday parties. Made with heavyweight cardstock and a lot of glue dots since {SITE['founded']}.</p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h4>Party themes</h4><ul>{li([(short_name(t), theme_url(t)) for t in themes_b + themes_bd[:2]])}<li><a href="/collections/">All themes &rarr;</a></li></ul></div>
<div><h4>Free tools</h4><ul>{li([(t, h) for t, h, _ in NAV[1][2]])}</ul></div>
<div><h4>Studio</h4><ul>{li([("Ideas blog", "/blog/"), ("About us", "/about/"), ("Contact", "/contact/"), ("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/"), ("Sitemap", "/sitemap/")])}</ul></div>
</div><div class="foot-bottom"><span>&copy; <span data-year>{TODAY[:4]}</span> {SITE['name']}. All rights reserved.</span><span>Character names mentioned on this site belong to their owners; we are not affiliated with them.</span></div></div></footer>
<button class="to-top" type="button" aria-label="Back to top">{ICONS['up']}</button>"""


def org_schema():
    return {
        "@type": "Organization", "@id": ORIGIN + "/#org", "name": SITE["name"], "url": ORIGIN + "/",
        "email": EMAIL, "logo": ORIGIN + "/web-app-manifest-512x512.png", "foundingDate": SITE["founded"],
        "description": SITE["tagline"],
    }


def website_schema():
    return {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": SITE["name"],
            "publisher": {"@id": ORIGIN + "/#org"}, "inLanguage": "en-US"}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": strip_tags(n), "item": ORIGIN + u} for i, (n, u) in enumerate(trail)]}


def crumbs_html(trail):
    lis = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{esc(n)}</li>'
                  for i, (n, u) in enumerate(trail))
    return f'<nav aria-label="Breadcrumb"><ol class="crumbs">{lis}</ol></nav>'


def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faq]}


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details class="reveal"><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq) + "</div>"


def page(path, title, description, body, *, schema=None, og_image="og-default.jpg", og_type="website",
         priority="0.6", lastmod=None, scripts=(), body_class="", sitemap=True, head_extra=""):
    canonical = ORIGIN + path
    full_title = title if title.endswith(SITE["name"]) else f"{title} | {SITE['name']}"
    graph = [org_schema(), website_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    og_url = og_image if og_image.startswith("http") else f"{ORIGIN}/assets/img/{og_image}"
    scr = "".join(f'<script src="/assets/js/{s}?v={ASSET_V}" defer></script>' for s in ("site.js",) + tuple(scripts))
    doc = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fffaf3">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Fraunces:ital,opsz,wght,SOFT@0,9..144,500..800,100;1,9..144,600..700,100&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{head_extra}<script type="application/ld+json">{ld}</script>
</head>
<body{f' class="{body_class}"' if body_class else ""}>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
{scr}
</body>
</html>
"""
    write(path, doc)
    if sitemap:
        PAGES.append((path, lastmod or TODAY, priority))


def write(path, doc):
    if path == "/":
        fp = os.path.join(OUT, "home.html")
    elif path.endswith("/"):
        fp = os.path.join(OUT, path.strip("/"), "index.html")
    else:
        fp = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------------------------------------------------------- shared bits
def theme_url(t):
    return f"/products/{t['slug']}/"


def short_name(t):
    n = re.sub(r"\s*(&amp;|&|and)?\s*(Decorations|Ideas)(\s*(&amp;|&|and)\s*\w+)*$", "", t["name"]).strip()
    n = re.sub(r"\s+(or|and)\s+(Birthday|Baby Shower)\s*$", "", n)
    return n


OCC_LABEL = {"baby-shower": "Baby shower", "birthday": "Birthday", "both": "Shower or birthday"}


def theme_tags(t):
    tags = list(t.get("collections", []))
    if t["occasion"] in ("baby-shower", "both") and "baby-shower-decorations" not in tags:
        tags.append("baby-shower-decorations")
    if t["occasion"] in ("birthday", "both") and "birthday-party-decorations" not in tags:
        tags.append("birthday-party-decorations")
    return tags


def theme_card(t, i=0):
    dots = "".join(f'<i style="background:{c}"></i>' for c, _ in t["palette"][:5])
    return (f'<a class="tcard reveal" style="--delay:{(i % 4) * 0.07:.2f}s" href="{theme_url(t)}" data-tilt data-tags="{" ".join(theme_tags(t))}">'
            f'<div class="tcard-img">{img(t["image"], t["image_alt"])}<span class="tcard-tag">{OCC_LABEL[t["occasion"]]}</span></div>'
            f'<div class="tcard-body"><h3>{short_name(t)}</h3><p>{t["tagline"]}</p><div class="dots">{dots}</div></div>'
            f'<span class="go">View theme &rarr;</span></a>')


def post_card(p, i=0):
    return (f'<a class="pcard reveal" style="--delay:{(i % 3) * 0.08:.2f}s" href="/blog/{p["slug"]}/" data-cat="{slugify(p["category"])}">'
            f'<div class="pcard-img">{img(p["image"], p["image_alt"])}</div><div class="pcard-body">'
            f'<div class="meta"><span class="cat">{esc(p["category"])}</span><span>{read_time(p)} min read</span></div>'
            f'<h3>{p["title"]}</h3><p>{p["excerpt"]}</p></div></a>')


def read_time(p):
    return max(3, round(len(strip_tags(p["body"]).split()) / 230))


TOOLS = [
    ("party-banner-maker", "Party Banner Maker", "Type any message, choose colors and pennant shape, then print one letter per page.", "flag", "#ffcf5a"),
    ("party-food-calculator", "Party Food Calculator", "How many cupcakes, drinks, plates and pounds of ice for your guest list.", "cake", "#ffc6c0"),
    ("party-planning-timeline", "Party Planning Timeline", "Enter the date and get a dated countdown checklist you can tick off.", "calendar", "#5cc9b5"),
    ("party-theme-finder", "Party Theme Finder", "Five quick questions, three themes that fit your party.", "spark", "#ab97ff"),
    ("baby-shower-bingo-generator", "Baby Shower Bingo", "Generate and print unique bingo cards for every guest.", "grid", "#8fd3ff"),
]


def tools_grid():
    return '<div class="tools-grid">' + "".join(
        f'<a class="tool-card reveal" style="--delay:{i * 0.06:.2f}s" href="/tools/{s}/"><div class="ico" style="--c:{c}">{ICONS[ic]}</div>'
        f'<h3>{n}</h3><p>{d}</p></a>' for i, (s, n, d, ic, c) in enumerate(TOOLS)) + "</div>"


def cta_band(title="Planning something special?", text=None):
    text = text or "Tell us about your theme, colors and date. We are happy to point you to the right ideas or talk through a custom paper set."
    return (f'<section class="section" style="padding-top:0"><div class="wrap"><div class="cta-band reveal">'
            f'<h2>{title}</h2><p>{text}</p><p style="margin:1.6rem 0 0"><a class="btn" href="/contact/" data-confetti>Get in touch {ICONS["arrow"]}</a></p></div></div></section>')


# ================================================================ pages
def build_theme(t):
    url = theme_url(t)
    pal = t["palette"]
    occ_coll = "baby-shower-decorations" if t["occasion"] == "baby-shower" else "birthday-party-decorations"
    if t["occasion"] == "both":
        occ_coll = "baby-shower-decorations" if "baby" in t["keyword"] or "shower" in t["keyword"] else "birthday-party-decorations"
    trail = [("Home", "/"), (COLLECTIONS[occ_coll]["name"], f"/collections/{occ_coll}/"), (short_name(t), url)]
    chips = "".join(f'<a href="/collections/{c}/">{COLLECTIONS[c]["name"]}</a>' for c in theme_tags(t) if c in COLLECTIONS)
    swatches = "".join(f'<button class="swatch" type="button" data-hex="{c}" aria-label="Copy {esc(n)} {c}"><i style="background:{c}"></i>'
                       f'<span>{esc(n)}<small>{c}</small></span></button>' for c, n in pal)
    banner_colors = ",".join(c.lstrip("#") for c, _ in pal if c.upper() not in ("#FFFFFF", "#FFF"))[:27]
    banner_text = "OH BABY" if t["occasion"] == "baby-shower" else "HAPPY BIRTHDAY"
    banner_link = f"/tools/party-banner-maker/?text={banner_text.replace(' ', '+')}&amp;colors={banner_colors}"

    toc, body = [], []
    body.append("".join(f"<p>{p}</p>" for p in t["intro"]))
    # paper set
    sid = "paper-set"
    toc.append((sid, "What goes in the paper set"))
    dark = [c for c, _ in pal if sum(int(c[k:k + 2], 16) for k in (1, 3, 5)) < 640] or ["#ff6f61"]
    items = "".join(f'<div class="set-item reveal" style="--c:{dark[i % len(dark)]};--delay:{(i % 3) * .06:.2f}s"><b>{n}</b><p>{d}</p></div>'
                    for i, (n, d) in enumerate(t["set_items"]))
    body.append(f'<h2 id="{sid}">What goes in the {short_name(t).lower()} paper set</h2><div class="set-grid">{items}</div>')
    for sec in t["sections"]:
        h, paras = sec[0], sec[1]
        sid = slugify(h)
        toc.append((sid, strip_tags(h)))
        block = f'<h2 id="{sid}">{h}</h2>' + "".join(f"<p>{p}</p>" for p in paras)
        if len(sec) > 2 and sec[2]:
            block += '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in sec[2]) + "</ol>"
        body.append(block)
    toc.append(("menu-and-games", "Menu and games"))
    body.append('<h2 id="menu-and-games">Menu and party games</h2><div class="two-col">'
                f'<div class="listcard reveal"><h3>On the menu</h3><ul>{"".join(f"<li>{m}</li>" for m in t["menu"])}</ul></div>'
                f'<div class="listcard reveal" style="--delay:.08s"><h3>Games and activities</h3><ul>{"".join(f"<li>{a}</li>" for a in t["activities"])}</ul></div></div>')
    toc.append(("checklist", "Decor checklist"))
    checks = "".join(f'<li><label><input type="checkbox" value="{slugify(n)}"><span>{n}</span></label></li>' for n, _ in t["set_items"])
    extra = [("venue", "Venue, date and guest list confirmed"), ("invites-sent", "Invitations sent"), ("cake", "Cake or cupcakes ordered"), ("favors", "Favors packed and tagged")]
    checks += "".join(f'<li><label><input type="checkbox" value="{v}"><span>{n}</span></label></li>' for v, n in extra)
    body.append(f'<div class="checklist" id="checklist" data-checklist="{t["slug"][:60]}"><div class="checklist-head"><div class="ring" aria-hidden="true"><span>0%</span></div>'
                f'<div><h3>Your {short_name(t).lower()} checklist</h3><p>Tick items off as you make or buy them. Your progress is saved in this browser.</p></div></div>'
                f'<ul class="checks">{checks}</ul><div class="checklist-actions no-print"><button class="btn btn--sm btn--ink" type="button" data-print>{ICONS["print"]} Print checklist</button>'
                f'<button class="btn btn--sm btn--ghost" type="button" data-reset>Reset</button></div></div>')
    toc.append(("faq", "FAQ"))
    body.append(f'<h2 id="faq">{short_name(t)} FAQ</h2>' + faq_html(t["faq"]))

    toc_html = "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc)
    aside = (f'<aside class="aside"><div class="box"><h4>On this page</h4><ol class="toc">{toc_html}</ol></div>'
             f'<div class="box box--ink"><h4>Make the banner</h4><p>Open our free banner maker with this palette already loaded, type your message and print.</p>'
             f'<a class="btn btn--sm" href="{banner_link}">Open banner maker</a></div>'
             f'<div class="box"><h4>Feeding a crowd?</h4><p style="font-size:.92rem">Work out cupcakes, drinks and plates for your guest count.</p>'
             f'<a href="/tools/party-food-calculator/">Party food calculator &rarr;</a></div></aside>')
    related = [BY_SLUG[s] for s in t.get("related", []) if s in BY_SLUG][:3]
    rel_html = ""
    if related:
        rel_html = (f'<section class="section section--tint" style="padding-top:40px">'
                    f'<div class="wrap"><div class="section-head"><span class="eyebrow">Keep browsing</span><h2>Themes that pair well</h2></div>'
                    f'<div class="grid-cards">{"".join(theme_card(r, i) for i, r in enumerate(related))}</div></div></section>')
    hero = f"""<section class="page-hero">{shapes(2, [c for c, _ in pal])}<div class="wrap">{crumbs_html(trail)}
<div class="theme-hero"><div><div class="chips">{chips}</div><h1>{t['name']}</h1><p class="lead">{t['tagline']}</p>
<div class="swatches" aria-label="Theme color palette (click to copy)">{swatches}</div>
<div class="hero-ctas" style="margin:0"><a class="btn" href="#checklist">Plan this party {ICONS['arrow']}</a><a class="btn btn--ghost" href="{banner_link}">Make the banner</a></div></div>
<figure class="framed" style="--tape:{pal[0][0]}cc;--tape2:{pal[min(2, len(pal) - 1)][0]}bb;margin:0">{img(t['image'], t['image_alt'], lazy=False)}</figure></div></div></section>"""
    main = (f'{hero}<section class="section" style="padding-top:20px"><div class="wrap layout"><article class="prose" data-progress>'
            f'{"".join(body)}</article>{aside}</div></section>{rel_html}{cta_band()}')
    schema = [
        {"@type": "Article", "headline": strip_tags(t["name"]), "description": t["description"], "image": f"{ORIGIN}/assets/img/{t['image']}.webp",
         "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"}, "mainEntityOfPage": ORIGIN + url,
         "datePublished": "2026-10-17", "dateModified": TODAY, "about": t["keyword"]},
        crumbs_schema(trail), faq_schema(t["faq"])]
    page(url, t["title"], t["description"], main, schema=schema, og_image=t["image"] + ".webp", og_type="article", priority="0.8")


def filter_bar(grid_id, show_occ=True):
    chips = ""
    if show_occ:
        chips = ('<button class="chip" type="button" data-filter="all" aria-pressed="true">All themes</button>'
                 '<button class="chip" type="button" data-filter="baby-shower-decorations" aria-pressed="false">Baby showers</button>'
                 '<button class="chip" type="button" data-filter="birthday-party-decorations" aria-pressed="false">Birthdays</button>'
                 '<button class="chip" type="button" data-filter="banners" aria-pressed="false">Banners</button>')
    return (f'<div class="filters" data-filter-grid="#{grid_id}">{chips}<label class="search"><span class="visually-hidden">Search themes</span>'
            f'{ICONS["search"]}<input type="search" placeholder="Search: elephant, truck, pink..." autocomplete="off"></label></div>')


def build_collections():
    all_t = THEMES
    trail = [("Home", "/"), ("Party themes", "/collections/")]
    body = (f'<section class="page-hero">{shapes(0)}<div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">{len(all_t)} party themes</span>'
            f'<h1>Party Themes &amp; Decoration Ideas</h1><p class="lead mx-auto" style="max-width:680px">Baby shower and birthday party themes with color palettes, '
            f'decor lists, DIY projects and printable checklists. Filter by occasion or search for an animal, color or idea.</p></div></section>'
            f'<section class="section" style="padding-top:0"><div class="wrap">{filter_bar("theme-grid")}'
            f'<div class="grid-cards" id="theme-grid">{"".join(theme_card(t, i) for i, t in enumerate(all_t))}</div>'
            f'<p class="empty">No themes match that search. Try "baby", "truck" or a color.</p></div></section>{cta_band()}')
    schema = [crumbs_schema(trail), {"@type": "CollectionPage", "name": "Party themes", "url": ORIGIN + "/collections/",
              "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": ORIGIN + theme_url(t), "name": strip_tags(t["name"])} for i, t in enumerate(all_t)]}}]
    page("/collections/", "Party Themes: Shower & Birthday Decor Ideas",
         "Browse 30+ baby shower and kids birthday party themes with color palettes, decoration lists, DIY printables and checklists. Filter by occasion or color.",
         body, schema=schema, priority="0.9")
    for key, c in COLLECTIONS.items():
        items = [t for t in THEMES if key in theme_tags(t)]
        url = f"/collections/{key}/"
        trail = [("Home", "/"), ("Party themes", "/collections/"), (c["name"], url)]
        others = "".join(f'<a class="chip" href="/collections/{k}/">{v["name"]}</a>' for k, v in COLLECTIONS.items() if k != key)
        body = (f'<section class="page-hero">{shapes(1)}<div class="wrap"><div class="theme-hero"><div>{crumbs_html(trail)}<span class="eyebrow">{len(items)} themes</span>'
                f'<h1>{c["name"]}</h1><p class="lead">{c["intro"]}</p><div class="filters" style="justify-content:flex-start;margin:0">{others}<a class="chip" href="/collections/">All themes</a></div></div>'
                f'<figure class="framed" style="margin:0">{img(c["image"], c["name"] + " ideas", lazy=False)}</figure></div></div></section>'
                f'<section class="section" style="padding-top:0"><div class="wrap">{filter_bar("theme-grid", False)}'
                f'<div class="grid-cards" id="theme-grid">{"".join(theme_card(t, i) for i, t in enumerate(items))}</div>'
                f'<p class="empty">No themes match that search.</p></div></section>')
        if key == "banners":
            body += (f'<section class="section section--tint"><div class="wrap demo" style="margin-top:0"><div><span class="eyebrow">Free tool</span><h2>Print any banner in minutes</h2>'
                     f'<p class="lead">Type a name or message, pick your theme colors and pennant shape, and print one big letter per sheet of cardstock.</p>'
                     f'<a class="btn" href="/tools/party-banner-maker/">Open the banner maker {ICONS["arrow"]}</a></div>'
                     f'<div class="live-bunting" data-live-bunting="" data-text="HOORAY" data-per="8"></div></div></section>')
        body += cta_band()
        schema = [crumbs_schema(trail), {"@type": "CollectionPage", "name": c["name"], "url": ORIGIN + url,
                  "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": ORIGIN + theme_url(t), "name": strip_tags(t["name"])} for i, t in enumerate(items)]}}]
        page(url, c["title"], c["description"], body, schema=schema, og_image=c["image"] + ".webp", priority="0.8")


EXPLORER = [
    ("Welcome banner", "The piece every photo ends up including. Ours were 5x7 or 8x10 pennants, one letter each, strung on clear line or baker's twine so the banner floats.", ["5x7 or 8x10 pennants", "1 letter per flag", "Clear line or twine"], None),
    ("Cake topper", "A cut-out silhouette on two skewers turns a plain bakery cake into a theme cake. Size it to about 75% of the cake's width so it doesn't topple.", ["5-7 in wide", "Double skewers", "Layered cardstock"], "birthday-candles-sprinkles"),
    ("Cupcake toppers", "Two-inch circles on toothpicks, backed with a second circle so the stick is hidden and the topper looks finished from every side.", ["2 in circles", "Backed and glued", "1 per cupcake + extras"], "frosted-cupcakes"),
    ("Centerpieces", "A double-sided character on a skewer, tucked into a jar of flowers, candy or paper shred. One per table plus one for the food table.", ["8 in characters", "Double-sided", "1 per table"], "party-table-candles"),
    ("Door sign", "The first thing guests see. A welcome sign with the guest of honor's name tells them they're in the right place and sets the colors.", ["8x10 sign", "Ribbon hanger", "Name personalized"], "hand-lettering"),
    ("Invitations", "Flat 5x7 cards on heavy stock with the date, time, place and RSVP. Mailed 4-6 weeks ahead for showers, 3-4 weeks for birthdays.", ["5x7 flat cards", "A7 envelopes", "Digital option"], "invitation-envelope"),
    ("Favor tags", "Small scalloped tags with a thank-you line, tied to favor bags with twine. The cheapest piece that makes favors look intentional.", ["2 in tags", "Twine or ribbon", "Hole-punched"], "gift-wrap-ribbon-scissors"),
    ("Thank-you cards", "Folded cards that match the party, left blank inside for a handwritten note after the gifts are opened.", ["A2 folded cards", "Blank inside", "Matching envelopes"], "paper-flatlay-scissors"),
]

HOME_FAQ = [
    ("What kinds of party themes do you cover?", "Baby showers and kids' birthday parties: elephants in pink, blue and yellow, woodland and safari animals, whales and ducks, trucks, dinosaurs, monsters, reptiles, sports and holiday birthdays. Every theme has its own guide with a palette, decor list and checklist."),
    ("Are the party tools really free?", "Yes. The banner maker, food calculator, planning timeline, theme finder and bingo generator all run in your browser, need no account and print on a home printer."),
    ("What paper should I use for printable party decorations?", "Use heavy cardstock: 65-80 lb for most home printers, and 100-110 lb if your printer has a straight paper path. Our original sets were printed on 110 lb cardstock so banners and toppers never curled. Our guide to <a href=\"/blog/how-to-print-party-printables-at-home/\">printing party printables at home</a> covers settings and cutting."),
    ("How far ahead should I start planning a baby shower?", "Six to eight weeks is comfortable. Invitations go out four to six weeks before, and decorations and favors can be made in the final two weeks. Our <a href=\"/tools/party-planning-timeline/\">planning timeline</a> builds a dated checklist from your party date."),
    ("Can you make a custom design for my party?", f"Tell us about your theme, colors and date at <a href=\"mailto:{EMAIL}\">{EMAIL}</a> and we will reply with ideas and what we can do."),
]


def build_home():
    feat = [BY_SLUG[s] for s in FEATURED if s in BY_SLUG]
    marquee_items = "".join(f'<a href="{theme_url(t)}">{short_name(t)}</a>' for t in THEMES[:16])
    occ_counts = {k: len([t for t in THEMES if k in theme_tags(t)]) for k in COLLECTIONS}
    occ = "".join(
        f'<a class="occ reveal" style="--delay:{i * .08:.2f}s" href="/collections/{k}/">{img(c["image"], c["name"])}'
        f'<span class="arrow">{ICONS["arrow"]}</span><div class="occ-body"><span class="count">{occ_counts[k]} themes</span><h3>{c["name"]}</h3><p>{d}</p></div></a>'
        for i, (k, c, d) in enumerate([
            ("baby-shower-decorations", COLLECTIONS["baby-shower-decorations"], "Elephants, woodland, safari, ducks, books and balloons."),
            ("birthday-party-decorations", COLLECTIONS["birthday-party-decorations"], "Trucks, dinosaurs, monsters, reptiles and sports."),
            ("banners", COLLECTIONS["banners"], "Pennant banners, wording ideas and a free printable maker.")]))
    tabs, panels = [], []
    for i, (name, desc, spec, image) in enumerate(EXPLORER):
        pid = f"set-{slugify(name)}"
        tabs.append(f'<button role="tab" type="button" id="tab-{pid}" aria-controls="{pid}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
                    f'<span class="n">{i + 1}</span>{name}</button>')
        art = (f'<div class="live-bunting" data-live-bunting="" data-text="OH BABY" data-per="8" style="margin:0 0 18px"></div>' if image is None
               else f'<div class="art">{img(image, name + " for a themed party")}</div>')
        panels.append(f'<div class="explorer-panel" role="tabpanel" id="{pid}" aria-labelledby="tab-{pid}"{"" if i == 0 else " hidden"}>{art}<span class="hand">piece {i + 1} of 8</span>'
                      f'<h3>{name}</h3><p>{desc}</p><ul class="spec">{"".join(f"<li>{s}</li>" for s in spec)}</ul></div>')
    posts = "".join(post_card(p, i) for i, p in enumerate(POSTS[:3]))
    body = f"""
{bunting_strip()}<section class="hero">{shapes(0)}<div class="wrap hero-grid">
<div><span class="eyebrow">Baby showers &amp; kids' birthdays</span>
<h1>Paper party decor that <span class="mark">steals the show<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 14 C 60 4, 140 4, 297 10" fill="none" stroke="#ffcf5a" stroke-width="7" stroke-linecap="round"/></svg></span></h1>
<p class="lead">BC Paper Designs has been making themed banners, cake toppers and centerpieces since {SITE['founded']}. Find your party theme, borrow our color palettes and DIY ideas, and use our free tools to plan, print and celebrate.</p>
<div class="hero-ctas"><a class="btn" href="/collections/">Browse party themes {ICONS['arrow']}</a><a class="btn btn--ghost" href="/tools/party-banner-maker/" data-confetti>Make a free banner</a></div>
<ul class="hero-note"><li>{len(THEMES)} theme guides</li><li>5 free party tools</li><li>Printable checklists</li></ul></div>
<div class="collage" data-confetti-load>
<figure class="polaroid p1">{img('hero-balloons-cake', 'First birthday cake on a wooden crate with two balloons outdoors', lazy=False)}<figcaption>first birthday!</figcaption></figure>
<figure class="polaroid p2">{img('baby-feet-pink', 'Newborn baby feet on a soft pink blanket', lazy=False)}<figcaption>oh baby</figcaption></figure>
<figure class="polaroid p3">{img('sprinkle-cake-party-table', 'Sprinkle cake slices, party hats and confetti on a turquoise table', lazy=False)}<figcaption>party time</figcaption></figure>
<div class="sticker"><span><b>{len(THEMES)}</b>party themes inside</span></div></div>
</div></section>
<div class="marquee-wrap"><div class="marquee" aria-label="Popular party themes"><div class="marquee-track">{marquee_items}{marquee_items.replace('<a ', '<a tabindex="-1" aria-hidden="true" ')}</div></div></div>

<section class="section"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Shop the ideas by occasion</span>
<h2>What are you celebrating?</h2><p class="lead">Start with the occasion, then pick a theme. Every guide is free to use and built to print at home.</p></div>
<div class="occasions">{occ}</div></div></section>

{edge()}<section class="section section--tint"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Most-loved themes</span>
<h2>Party themes our readers keep coming back to</h2><p class="lead">The pink elephant shower, the construction truck birthday and the gender-neutral yellow elephant banner have been favorites for years.</p></div>
<div class="grid-cards">{"".join(theme_card(t, i) for i, t in enumerate(feat))}</div>
<p class="center" style="margin-top:36px"><a class="btn btn--ink" href="/collections/">See all {len(THEMES)} themes {ICONS['arrow']}</a></p></div></section>{edge("edge--bottom")}

<section class="section"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Anatomy of a party</span>
<h2>The eight paper pieces that make a party</h2><p class="lead">Every themed set we designed was built from the same eight pieces. Click through to see what each one does and the sizes that work.</p></div>
<div class="explorer" data-tabs><div class="explorer-tabs" role="tablist" aria-label="Paper party pieces">{"".join(tabs)}</div><div>{"".join(panels)}</div></div></div></section>

{edge("edge--top edge--ink")}<section class="section section--ink"><div class="wrap"><div class="section-head reveal"><span class="eyebrow" style="color:var(--butter)">Free party tools</span>
<h2>Plan it, print it, party</h2><p class="lead">Five free tools that run right in your browser. No sign-up, nothing to install.</p></div>
{tools_grid()}
<div class="demo"><div><span class="hand" style="color:var(--butter)">try it right here</span><h3 style="font-size:1.8rem;margin-top:.4em">Type a name, watch the banner appear</h3>
<p style="color:#cfc7e6">This is a live preview of our banner maker. The full tool lets you pick colors, pennant shapes and fonts, then prints one letter per page.</p>
<div class="demo-input"><label class="visually-hidden" for="demo-text">Banner text</label><input id="demo-text" type="text" maxlength="24" value="HAPPY BIRTHDAY"><a class="btn btn--mint" href="/tools/party-banner-maker/">Open full tool</a></div></div>
<div class="live-bunting" data-live-bunting="demo-text" data-per="9" data-string="#cfc7e6"></div></div>
</div></section>{edge("edge--bottom edge--ink")}

<section class="section"><div class="wrap story"><div class="story-img reveal">{img('paper-hearts-scissors', 'Paper hearts, a red rose and scissors on a wooden craft table')}<div class="note">110 lb cardstock, cut by hand, glued to last</div></div>
<div class="reveal" style="--delay:.1s"><span class="eyebrow">Our story</span><h2>A paper studio that grew into an idea library</h2>
<p>BC Paper Designs started as a small studio making themed party sets: banners, door signs, cake toppers, centerpieces, cupcake toppers, favor tags and invitations, all printed on heavyweight cardstock and shipped cut and assembled. Every set could be personalized with any message.</p>
<p>Those themes are still here, rebuilt as free guides. Each one shares the palette, the pieces we would make, the projects you can do yourself and the little details that make a party feel finished.</p>
<ul class="facts"><li><b>110 lb</b>cardstock on every printed piece</li><li><b>{len(THEMES)}</b>baby shower and birthday themes</li><li><b>8</b>paper pieces in a full party set</li><li><b>5</b>free tools for planning and printing</li></ul>
<p style="margin-top:1.6rem"><a class="btn btn--ghost" href="/about/">More about the studio</a></p></div></div></section>

{edge()}<section class="section section--tint"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">From the ideas blog</span><h2>Fresh party planning guides</h2></div>
<div class="posts">{posts}</div><p class="center" style="margin-top:36px"><a class="btn btn--ink" href="/blog/">Read the blog {ICONS['arrow']}</a></p></div></section>{edge("edge--bottom")}

<section class="section"><div class="wrap"><div class="section-head reveal"><span class="eyebrow">Good to know</span><h2>Party planning questions</h2></div>{faq_html(HOME_FAQ)}</div></section>
{cta_band("Let's make your party unforgettable")}"""
    schema = [faq_schema(HOME_FAQ), {"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/", "name": "BC Paper Designs",
              "isPartOf": {"@id": ORIGIN + "/#website"}, "about": {"@id": ORIGIN + "/#org"}}]
    page("/", "Baby Shower & Birthday Party Decorations | BC Paper Designs",
         "BC Paper Designs: baby shower and kids birthday party decoration ideas, 30+ theme guides, DIY paper banners and toppers, and free party planning tools.",
         body, schema=schema, priority="1.0", body_class="home")


def build_blog():
    cats = sorted({p["category"] for p in POSTS})
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All posts</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{slugify(c)}" aria-pressed="false">{c}</button>' for c in cats)
    cards = "".join(post_card(p, i).replace('data-cat="', 'data-tags="') for i, p in enumerate(POSTS))
    trail = [("Home", "/"), ("Blog", "/blog/")]
    body = (f'<section class="page-hero">{shapes(3)}<div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Ideas blog</span><h1>Party Ideas &amp; Planning Guides</h1>'
            f'<p class="lead mx-auto" style="max-width:660px">Practical guides for baby showers and kids\' birthdays: planning timelines, themes, games, food quantities and DIY paper decorations.</p></div></section>'
            f'<section class="section" style="padding-top:0"><div class="wrap"><div class="filters" data-filter-grid="#post-grid">{chips}</div>'
            f'<div class="posts" id="post-grid">{cards}</div></div></section>{cta_band()}')
    schema = [crumbs_schema(trail), {"@type": "Blog", "name": "BC Paper Designs Ideas Blog", "url": ORIGIN + "/blog/",
              "blogPost": [{"@type": "BlogPosting", "headline": strip_tags(p["title"]), "url": f"{ORIGIN}/blog/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]}]
    page("/blog/", "Party Ideas Blog: Shower & Birthday Planning",
         "Party planning guides for baby showers and kids' birthdays: themes, games, checklists, food quantities and DIY paper banners, toppers and printables.",
         body, schema=schema, priority="0.8")
    for p in POSTS:
        build_post(p)


def add_ids(body):
    toc = []

    def rep(m):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            i = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            i = slugify(inner)
            attrs = f' id="{i}"' + attrs
        toc.append((i, strip_tags(inner)))
        return f"<h2{attrs}>{inner}</h2>"
    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S)
    body = re.sub(r"(<table.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)
    return body, toc


def build_post(p):
    url = f"/blog/{p['slug']}/"
    trail = [("Home", "/"), ("Blog", "/blog/"), (strip_tags(p["title"]), url)]
    body_html, toc = add_ids(p["body"])
    if p.get("faq"):
        toc.append(("faq", "FAQ"))
        body_html += '<h2 id="faq">Frequently asked questions</h2>' + faq_html(p["faq"])
    pretty = date.fromisoformat(p["date"]).strftime("%B %-d, %Y")
    related = [q for q in POSTS if q is not p and q["category"] == p["category"]][:3]
    related += [q for q in POSTS if q is not p and q not in related][: 3 - len(related)]
    toc_html = "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc)
    feat = [t for t in THEMES if any(f"/products/{t['slug']}/" in p["body"] for _ in [0])][:2] or [BY_SLUG[FEATURED[0]]]
    aside = (f'<aside class="aside"><div class="box"><h4>In this guide</h4><ol class="toc">{toc_html}</ol></div>'
             f'<div class="box box--ink"><h4>Free party tools</h4><p>Banner maker, food calculator, planning timeline, theme quiz and bingo cards.</p>'
             f'<a class="btn btn--sm" href="/tools/">See the tools</a></div>'
             + "".join(f'<a class="tcard" href="{theme_url(t)}"><div class="tcard-img">{img(t["image"], t["image_alt"])}</div><div class="tcard-body"><h3>{short_name(t)}</h3></div></a>' for t in feat)
             + "</aside>")
    hero = (f'<section class="page-hero">{shapes(4)}<div class="wrap">{crumbs_html(trail)}<div class="theme-hero"><div>'
            f'<div class="meta" style="margin-bottom:1rem"><span class="cat">{esc(p["category"])}</span><span>{pretty}</span><span>{read_time(p)} min read</span></div>'
            f'<h1>{p["title"]}</h1><p class="lead">{p["excerpt"]}</p></div>'
            f'<figure class="framed" style="margin:0">{img(p["image"], p["image_alt"], lazy=False)}</figure></div></div></section>')
    rel = "".join(post_card(q, i) for i, q in enumerate(related))
    main = (f'{hero}<section class="section" style="padding-top:20px"><div class="wrap layout"><article class="prose" data-progress>{body_html}'
            f'<p style="margin-top:2.5rem;color:var(--ink-3);font-size:.92rem">Written by the {SITE["name"]} studio. Questions or a party to plan? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'
            f'</article>{aside}</div></section><section class="section section--tint" style="padding-top:50px"><div class="wrap"><div class="section-head"><h2>Keep reading</h2></div>'
            f'<div class="posts">{rel}</div></div></section>{cta_band()}')
    schema = [crumbs_schema(trail), {"@type": "BlogPosting", "headline": strip_tags(p["title"]), "description": p["description"],
              "image": f"{ORIGIN}/assets/img/{p['image']}.webp", "datePublished": p["date"], "dateModified": p["date"],
              "author": {"@type": "Organization", "name": SITE["name"], "url": ORIGIN + "/"}, "publisher": {"@id": ORIGIN + "/#org"},
              "mainEntityOfPage": ORIGIN + url, "keywords": p["keyword"], "articleSection": p["category"],
              "wordCount": len(strip_tags(p["body"]).split())}]
    if p.get("faq"):
        schema.append(faq_schema(p["faq"]))
    page(url, p["meta_title"], p["description"], main, schema=schema, og_image=p["image"] + ".webp", og_type="article",
         priority="0.7", lastmod=p["date"])


# ================================================================ tools
def tool_page(slug, h1, title, desc, ui, guide, faq, eyebrow="Free party tool"):
    url = f"/tools/{slug}/"
    trail = [("Home", "/"), ("Party tools", "/tools/"), (h1, url)]
    others = [t for t in TOOLS if t[0] != slug]
    other_html = '<div class="tools-grid">' + "".join(
        f'<a class="tool-card" href="/tools/{s}/"><div class="ico" style="--c:{c}">{ICONS[ic]}</div><h3>{n}</h3><p>{d}</p></a>' for s, n, d, ic, c in others) + "</div>"
    body = (f'<section class="page-hero" style="padding-bottom:70px">{shapes(1)}<div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">{eyebrow}</span>'
            f'<h1>{h1}</h1><p class="lead mx-auto" style="max-width:680px">{desc}</p></div></section>'
            f'<section class="no-print-wrap"><div class="wrap"><div class="tool-shell">{ui}</div></div></section>'
            f'<section class="section"><div class="wrap layout"><article class="prose">{guide}<h2 id="faq">Questions</h2>{faq_html(faq)}</article>'
            f'<aside class="aside"><div class="box box--ink"><h4>Need a theme?</h4><p>Browse {len(THEMES)} baby shower and birthday themes with palettes you can load into the banner maker.</p>'
            f'<a class="btn btn--sm" href="/collections/">Browse themes</a></div></aside></div></section>'
            f'<section class="section section--tint" style="padding-top:50px"><div class="wrap"><div class="section-head"><h2>More free party tools</h2></div>{other_html}</div></section>')
    schema = [crumbs_schema(trail), faq_schema(faq), {"@type": "WebApplication", "name": h1, "url": ORIGIN + url, "description": desc,
              "applicationCategory": "LifestyleApplication", "operatingSystem": "Any (runs in the browser)", "isAccessibleForFree": True,
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@id": ORIGIN + "/#org"}}]
    page(url, title, strip_tags(desc)[:158], body, schema=schema, scripts=("tools.js",), priority="0.8")


PRESETS = [("Blush elephant", "#f4b6c2,#9aa5b1,#e8c07d,#5e6b78", "#ffffff"), ("Baby blue", "#9cc9e8,#1f3a5f,#c7d3dd,#5b8db8", "#ffffff"),
           ("Sunny neutral", "#f6c945,#9a9a9a,#f9e7a6,#5f6368", "#2a2140"), ("Construction", "#ffc61a,#111111,#ff7a00,#6b6b6b", "#ffffff"),
           ("Woodland", "#c8693a,#7a8b5a,#e7d3b5,#5a3e2b", "#ffffff"), ("Rainbow", "#ff6f61,#ffcf5a,#5cc9b5,#ab97ff", "#ffffff"),
           ("Navy & teal", "#1f3a5f,#2bb3a3,#9fd8d0,#f2b880", "#ffffff"), ("Halloween", "#ff7a1a,#2a2140,#7fc241,#8b5cf6", "#ffffff")]


def seg_html(id_, opts, sel):
    return f'<div class="seg" id="{id_}">' + "".join(
        f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == sel else "false"}">{n}</button>' for v, n in opts) + "</div>"


def build_tools():
    # Banner maker
    presets = "".join(f'<button class="preset" type="button" data-colors="{c}" data-ink="{ink}" aria-label="{n} palette" title="{n}">'
                      + "".join(f'<i style="background:{x}"></i>' for x in c.split(",")) + "</button>" for n, c, ink in PRESETS)
    ui = f"""<div class="tool-layout" data-tool="banner"><div>
<div class="field"><label for="bm-text">Banner message</label><input class="input" id="bm-text" type="text" maxlength="60" value="HAPPY BIRTHDAY"><small id="bm-count"></small></div>
<div class="field"><span class="lbl">Flag colors (repeat in order)</span><div class="colors" id="bm-colors">
<input type="color" value="#ff6f61" aria-label="Color 1"><input type="color" value="#ffcf5a" aria-label="Color 2"><input type="color" value="#5cc9b5" aria-label="Color 3"><input type="color" value="#ab97ff" aria-label="Color 4"></div></div>
<div class="field"><span class="lbl">Palette presets</span><div class="presets">{presets}</div></div>
<div class="row2"><div class="field"><label for="bm-ink">Letter color</label><input class="input" id="bm-ink" type="color" value="#ffffff" style="height:46px;padding:4px"></div>
<div class="field"><span class="lbl">Font</span>{seg_html("bm-font", [("serif", "Serif"), ("sans", "Sans"), ("script", "Script")], "serif")}</div></div>
<div class="field"><span class="lbl">Flag shape</span>{seg_html("bm-shape", [("pennant", "Pennant"), ("swallow", "Swallowtail"), ("scallop", "Scallop"), ("circle", "Circle")], "pennant")}</div>
<div class="checklist-actions"><button class="btn" type="button" id="bm-print">{ICONS['print']} Print banner</button><button class="btn btn--ghost" type="button" id="bm-party">Celebrate!</button></div>
</div><div><div class="stage" id="bm-stage" aria-live="polite"></div><p class="form-note" style="margin-top:12px">Prints one flag per letter-size page with a dashed cut line. Choose "Actual size" and turn on background graphics in your print dialog.</p></div></div>"""
    guide = """<h2>How to print and hang your banner</h2><ol class="steps"><li>Type your message. Short messages ("OH BABY", "HAPPY 1ST", a first name) read best from across a room.</li>
<li>Pick colors that match your theme. Every <a href="/collections/">theme guide</a> has a "Make the banner" button that loads its palette here.</li>
<li>Load heavy cardstock (65-110 lb, depending on your printer) and print at actual size with background graphics on.</li>
<li>Cut along the dashed line. Scissors are fine; a paper trimmer makes the straight edges faster.</li>
<li>Punch two holes near the top corners, about 3/4 inch in, and thread twine or ribbon through the front of each flag.</li>
<li>Hang it with removable hooks and slide the flags so the spacing is even, about 1 inch apart.</li></ol>
<h2>How long will my banner be?</h2><p>Each flag prints about 7.4 inches wide. With 1 inch between flags, a 10-letter message plus one blank flag between words runs roughly 8 feet. For a long wall, add a garland of paper hearts or extra blank flags at each end.</p>
<div class="tip"><strong>Tip:</strong> Printing "HAPPY BIRTHDAY" uses 13 sheets. Print a couple of spare blank flags in your accent color to fill gaps and make the ends drape nicely.</div>"""
    faq = [("Is the banner maker free?", "Yes, completely. It runs in your browser and nothing is uploaded."),
           ("What paper should I use?", "Cardstock between 65 and 110 lb. Thinner paper curls and lets light through when hung in front of a window."),
           ("Why are my colors missing when I print?", "Turn on \"Background graphics\" (Chrome, Edge) or \"Print backgrounds\" (Safari, Firefox) in the print dialog.")]
    tool_page("party-banner-maker", "Free Printable Party Banner Maker", "Party Banner Maker: Free Printable Birthday Banner",
              "Type any message, pick your colors, font and pennant shape, then print a happy birthday or baby shower banner at home, one big letter per page.", ui, guide, faq)

    # Food calculator
    ui = f"""<div class="tool-layout" data-tool="food"><div>
<div class="field"><span class="lbl">Type of party</span>{seg_html("fc-type", [("birthday", "Kids birthday"), ("shower", "Baby shower")], "birthday")}</div>
<div class="row2"><div class="field"><label for="fc-adults">Adults</label><input class="input" id="fc-adults" type="number" min="0" max="500" value="12" inputmode="numeric"></div>
<div class="field"><label for="fc-kids">Kids</label><input class="input" id="fc-kids" type="number" min="0" max="500" value="10" inputmode="numeric"></div></div>
<div class="field"><label for="fc-hours">Party length: <span id="fc-hours-out"></span></label><input class="range" id="fc-hours" type="range" min="1" max="5" step="0.5" value="2"></div>
<div class="field"><label for="fc-meal">What are you serving?</label><select class="input" id="fc-meal"><option value="snacks">Snacks and finger food</option><option value="meal">A full meal (lunch or dinner)</option><option value="dessert">Dessert and drinks only</option></select></div>
<button class="btn btn--ink" type="button" id="fc-print">{ICONS['print']} Print shopping list</button></div>
<div><div class="results" id="fc-out" aria-live="polite"></div></div></div>"""
    guide = """<h2>How the calculator works</h2><p>The numbers follow the rules of thumb caterers use, adjusted for kids' parties:</p>
<ul><li><strong>Finger food:</strong> about 6 pieces per adult in the first hour and 3 per hour after. Kids count as roughly two-thirds of an adult. If you serve a meal, the starter count drops.</li>
<li><strong>Drinks:</strong> 2 per adult in the first hour and 1 per hour after; kids drink a little less.</li>
<li><strong>Cupcakes:</strong> 1.25 per guest at birthdays (siblings and parents take one too), rounded to full dozens.</li>
<li><strong>Ice:</strong> 1 lb per guest, plus half a pound more each for parties over 2 hours.</li>
<li><strong>Paper goods:</strong> 1.5 plates, 2 cups and 3 napkins per guest.</li></ul>
<p>For menus that suit each theme, see our <a href="/blog/how-much-food-for-a-party/">guide to how much food to serve at a party</a>.</p>"""
    faq = [("How many cupcakes do I need for 20 kids?", "Plan about 25 to 30, since parents and siblings usually take one. The calculator rounds up to full dozens."),
           ("How much cake for 30 people?", "A two-layer 10-inch round or a quarter sheet cake serves about 30 to 38 party-size slices."),
           ("Does the calculator save my numbers?", "Yes, in this browser only, so you can come back and adjust.")]
    tool_page("party-food-calculator", "Party Food Calculator", "Party Food Calculator: How Much Food to Buy",
              "Enter your guest count and party length to see how many cupcakes, finger-food pieces, drinks, plates, cups and pounds of ice to buy.", ui, guide, faq)

    # Timeline
    ui = f"""<div class="tool-layout" data-tool="timeline"><div>
<div class="field"><span class="lbl">What are you planning?</span>{seg_html("tl-type", [("shower", "Baby shower"), ("birthday", "Birthday party")], "shower")}</div>
<div class="field"><label for="tl-date">Party date</label><input class="input" id="tl-date" type="date"></div>
<div class="field"><label for="tl-name">Party name (optional)</label><input class="input" id="tl-name" type="text" placeholder="e.g. Maya's baby shower" maxlength="60"></div>
<div class="checklist-actions"><button class="btn btn--ink" type="button" id="tl-print">{ICONS['print']} Print</button><button class="btn btn--ghost" type="button" id="tl-ics">{ICONS['calendar']} Add to calendar</button></div>
<p class="form-note" style="margin-top:14px">Your date and ticks are saved in this browser.</p></div>
<div><div class="countdown" id="tl-countdown"></div><ol class="tl" id="tl-list"></ol></div></div>"""
    guide = """<h2>Why a dated timeline helps</h2><p>Most party stress comes from tasks bunching up in the final week. Working backward from the date spreads the jobs out: invitations four to six weeks ahead, decor in the last two weeks, fresh food in the final two days.</p>
<p>The baby shower plan follows the steps in our <a href="/blog/how-to-plan-a-baby-shower/">week-by-week baby shower guide</a>; the birthday plan is shorter because invitations go out three to four weeks ahead.</p>
<div class="tip"><strong>Tip:</strong> Do the decorations a full week early. Paper pieces keep perfectly in a flat box, and the last few days are always busier than you expect.</div>"""
    faq = [("When should baby shower invitations go out?", "Four to six weeks before the shower, so guests can plan travel and shop the registry."),
           ("When should birthday invitations go out?", "Three to four weeks before for kids' parties. Two weeks is fine for a small family gathering."),
           ("Can I print the timeline?", "Yes. Use the Print button; the checklist prints cleanly without the site header and footer.")]
    tool_page("party-planning-timeline", "Party Planning Timeline & Countdown", "Party Planning Timeline: Baby Shower & Birthday",
              "Enter your party date to get a dated countdown checklist for a baby shower or birthday, from invitations to party day. Tick tasks off and add it to your calendar.", ui, guide, faq)

    # Quiz
    qs = [("occasion", "What are you celebrating?", [("shower", "&#x1F37C;", "A baby shower", "Welcoming a little one"), ("birthday", "&#x1F382;", "A birthday", "Kids, toddlers or a first birthday")]),
          ("who", "Who is the guest of honor?", [("girl", "&#x1F338;", "Baby girl", ""), ("boy", "&#x1F42C;", "Baby boy", ""), ("neutral", "&#x2728;", "It's a surprise", "Or keeping it neutral"), ("little", "&#x1F9F8;", "A little one (1-5)", ""), ("big", "&#x26BD;", "A big kid (6+)", "")]),
          ("vibe", "Pick a party mood", [("sweet", "&#x1F380;", "Sweet and soft", "Pastels, florals, gentle"), ("bold", "&#x1F525;", "Big and bold", "Bright colors, big shapes"), ("natural", "&#x1F33F;", "Natural and earthy", "Greens, woods, kraft paper"), ("playful", "&#x1F389;", "Silly and playful", "Games, giggles, confetti")]),
          ("color", "Which colors make you smile?", [("pink", "&#x1F497;", "Pinks and corals", ""), ("blue", "&#x1F499;", "Blues and navy", ""), ("neutral", "&#x1F90D;", "Yellow, grey, cream", ""), ("bright", "&#x1F308;", "Rainbow brights", "")]),
          ("world", "Which world would they love?", [("animals", "&#x1F418;", "Animals", "Elephants, foxes, lions"), ("vehicles", "&#x1F69C;", "Trucks and vehicles", ""), ("ocean", "&#x1F433;", "Under the sea", "Whales, turtles, ducks"), ("storybook", "&#x1F4DA;", "Storybook and whimsy", "Books, balloons, monsters"), ("games", "&#x1F3B3;", "Games and holidays", "Sports, emoji, Halloween")])]
    qhtml = ""
    for i, (k, q, opts) in enumerate(qs):
        btns = "".join(f'<button type="button" data-v="{v}"><span aria-hidden="true">{e}</span>{n}{f"<small>{s}</small>" if s else ""}</button>' for v, e, n, s in opts)
        back = '<p style="margin:16px 0 0"><button class="btn btn--sm btn--ghost quiz-back" type="button">&larr; Back</button></p>' if i else ""
        qhtml += f'<div class="quiz-q" data-q="{k}"><span class="hand">question {i + 1} of {len(qs)}</span><h2 style="margin-top:.3em">{q}</h2><div class="quiz-opts">{btns}</div>{back}</div>'
    data = [{"url": theme_url(t), "name": short_name(t), "tagline": strip_tags(t["tagline"]), "img": f"/assets/img/{t['image']}.webp",
             "palette": [c for c, _ in t["palette"]][:5], "occasion": t["occasion"], "tags": THEME_TAGS.get(t["slug"], "").split()} for t in THEMES]
    ui = (f'<div data-tool="quiz"><div class="progress" aria-hidden="true"><i></i></div>{qhtml}<div id="quiz-result" hidden></div></div>'
          f'<script type="application/json" id="theme-data">{json.dumps(data).replace("</", "<\\/")}</script>')
    guide = """<h2>How to choose a party theme</h2><p>The best themes start with the guest of honor. A toddler who lines up toy trucks will light up at a <a href="/products/construction-truck-birthday-decorations/">construction party</a>; a parent-to-be who loves calm colors will feel at home with a <a href="/products/woodland-baby-shower-decorations/">woodland shower</a>.</p>
<ul><li><strong>Start with color.</strong> A palette of three or four colors does more for a room than any single decoration.</li><li><strong>Check the venue.</strong> Earthy themes suit parks and patios; bright themes lift a plain community room.</li><li><strong>Think about photos.</strong> The banner and cake table are in every picture, so make those match the theme first.</li></ul>
<p>Still undecided? Our list of <a href="/blog/baby-shower-themes/">baby shower themes</a> and <a href="/blog/kids-birthday-party-themes/">kids birthday party themes by age</a> has more ideas.</p>"""
    faq = [("How does the theme finder pick themes?", "Each theme is tagged by occasion, age, mood, colors and subject. Your answers score every theme and the top three are shown."),
           ("Can I mix two themes?", "Yes. Keep one palette and let the second theme appear in small details like cupcake toppers or favor tags.")]
    tool_page("party-theme-finder", "Party Theme Finder Quiz", "Party Theme Finder: Baby Shower & Birthday Quiz",
              "Answer five quick questions about the occasion, the guest of honor, mood and colors, and get three party themes that fit, each with a full decoration guide.", ui, guide, faq)

    # Bingo
    ui = f"""<div class="tool-layout" data-tool="bingo"><div>
<div class="field"><label for="bg-title">Card title</label><input class="input" id="bg-title" type="text" value="Baby Shower Bingo" maxlength="40"></div>
<div class="field"><label for="bg-list">Word list</label><select class="input" id="bg-list"><option value="gifts">Baby shower gifts (40 words)</option><option value="books">Book-themed shower (36 words)</option><option value="birthday">Birthday party (36 words)</option><option value="custom">My own words</option></select></div>
<div class="field" id="bg-custom-wrap" hidden><label for="bg-custom">Your words (one per line, at least 24)</label><textarea class="input" id="bg-custom" placeholder="Onesies&#10;Diapers&#10;..."></textarea></div>
<div class="row2"><div class="field"><label for="bg-num">Number of cards</label><input class="input" id="bg-num" type="number" min="1" max="40" value="12" inputmode="numeric"></div>
<div class="field"><label for="bg-color">Accent color</label><input class="input" id="bg-color" type="color" value="#5cc9b5" style="height:46px;padding:4px"></div></div>
<div class="checklist-actions"><button class="btn" type="button" id="bg-print">{ICONS['print']} Print cards</button><button class="btn btn--ghost" type="button" id="bg-new">Shuffle again</button></div>
<p class="form-note" style="margin-top:14px">Every card is unique. Prints two cards per letter-size page.</p></div>
<div><div class="bingo-preview" id="bg-preview" aria-live="polite"></div></div></div>"""
    guide = """<h2>How to play baby shower gift bingo</h2><ol class="steps"><li>Hand each guest a card and a pen as they arrive.</li><li>As the parents-to-be open gifts, guests mark any square that matches.</li><li>The first guest with five in a row (across, down or diagonal) shouts "Bingo!" and wins a prize.</li><li>Keep playing for a second winner with a full card, or "four corners".</li></ol>
<p>For a book-themed shower, choose the book word list and pair it with our <a href="/products/book-themed-baby-shower-games-printable-instant-download/">book themed baby shower games</a>. More ideas are in <a href="/blog/baby-shower-games/">15 baby shower games guests actually enjoy</a>.</p>"""
    faq = [("How many bingo cards should I print?", "One per guest plus three or four spares. The generator makes up to 40 unique cards."),
           ("Can I use my own words?", "Yes. Choose \"My own words\" and enter at least 24, one per line or separated by commas.")]
    tool_page("baby-shower-bingo-generator", "Baby Shower Bingo Card Generator", "Free Printable Baby Shower Bingo Card Generator",
              "Make and print unique baby shower bingo cards for every guest: gift bingo, book-themed bingo or your own words, two cards per page.", ui, guide, faq)

    # Tools hub
    trail = [("Home", "/"), ("Party tools", "/tools/")]
    body = (f'<section class="page-hero">{shapes(2)}<div class="wrap center">{crumbs_html(trail)}<span class="eyebrow">Free, no sign-up</span><h1>Free Party Planning Tools</h1>'
            f'<p class="lead mx-auto" style="max-width:640px">Make a printable banner, work out how much food to buy, build a planning countdown, find a theme and print bingo cards. Everything runs in your browser.</p></div></section>'
            f'<section class="section" style="padding-top:0"><div class="wrap">{tools_grid()}</div></section>'
            f'<section class="section section--tint"><div class="wrap demo" style="margin-top:0"><div><span class="eyebrow">Try the banner maker</span><h2>Your message, in paper flags</h2>'
            f'<div class="demo-input"><label class="visually-hidden" for="hub-text">Banner text</label><input id="hub-text" type="text" maxlength="24" value="OH BABY" style="background:#fff;color:var(--ink);border-color:var(--line)">'
            f'<a class="btn" href="/tools/party-banner-maker/">Customize &amp; print</a></div></div><div class="live-bunting" data-live-bunting="hub-text" data-per="9"></div></div></section>{cta_band()}')
    page("/tools/", "Free Party Planning Tools & Printables",
         "Free party planning tools: printable banner maker, party food calculator, planning timeline, party theme finder quiz and baby shower bingo card generator.",
         body, schema=[crumbs_schema(trail)], priority="0.8")


# ================================================================ static pages
def simple_page(path, h1, title, desc, inner, trail_name=None, eyebrow=None, priority="0.4", schema=None):
    trail = [("Home", "/"), (trail_name or h1, path)]
    body = (f'<section class="page-hero" style="padding-bottom:30px">{shapes(4)}<div class="wrap">{crumbs_html(trail)}'
            f'{f"<span class=\"eyebrow\">{eyebrow}</span>" if eyebrow else ""}<h1>{h1}</h1></div></section>'
            f'<section class="section" style="padding-top:10px"><div class="wrap">{inner}</div></section>')
    page(path, title, desc, body, schema=[crumbs_schema(trail)] + (schema or []), priority=priority)


def build_static():
    about = f"""<div class="story"><div class="prose"><p class="lead">BC Paper Designs is a paper party studio for baby showers and kids' birthday parties. We design themed decorations, share how to make them, and build free tools that take the guesswork out of planning.</p>
<h2>Where we started</h2><p>The studio began in {SITE['founded']} making complete party sets: welcome banners, door signs, cake toppers, centerpieces, cupcake toppers, favor tags, place cards, invitations and thank-you cards. Pieces were printed on a photo-quality printer on 110 lb heavyweight cardstock, then cut by hand and assembled with hot glue, skewers, toothpicks and clear string, so they arrived ready to hang. Any set could carry any message.</p>
<p>Pink elephants, construction trucks, monsters, reptiles, whales, woodland animals and safari prints were some of the themes parents asked for again and again. Those themes live on here as free guides.</p>
<h2>What you will find here</h2><ul><li><a href="/collections/">{len(THEMES)} party theme guides</a> with palettes, decor lists, DIY projects and checklists</li><li><a href="/tools/">Five free tools</a>: a printable banner maker, food calculator, planning timeline, theme quiz and bingo generator</li><li><a href="/blog/">Planning guides</a> on themes, games, printing and quantities</li></ul>
<h2>How we write our guides</h2><p>Everything is practical: real sizes, quantities and timings, colors given as hex codes so you can match paper, balloons and frosting. When we mention a popular character theme, we design around generic animals and shapes; we are not affiliated with any brand or rights holder.</p>
<p>Questions, corrections or a party you would like help with? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
<div class="story-img">{img('watercolor-craft-desk', 'Watercolor paints, brushes and a notebook on a wooden craft desk')}<div class="note">Made with paper, patience and a lot of glue dots</div></div></div>"""
    simple_page("/about/", "About BC Paper Designs", "About BC Paper Designs: Our Paper Party Studio",
                "BC Paper Designs is a paper party studio for baby showers and kids' birthdays, sharing theme guides, DIY paper decor and free planning tools since 2017.",
                about, eyebrow="Our studio", priority="0.5", schema=[{"@type": "AboutPage", "url": ORIGIN + "/about/", "about": {"@id": ORIGIN + "/#org"}}])
    theme_opts = "".join(f"<option>{short_name(t)}</option>" for t in THEMES)
    contact = f"""<div class="contact-grid"><div><p class="lead">Planning a baby shower or birthday? Tell us about your theme, colors and date. We read every message and usually reply within two business days.</p>
<a class="contact-card" href="mailto:{EMAIL}"><span class="ico">{ICONS['mail']}</span><span><strong>Email</strong><br>{EMAIL}</span></a>
<div class="box"><h4>Good things to include</h4><ul style="margin:0;padding-left:1.1em;font-size:.95rem"><li>The occasion and party date</li><li>Your theme or the colors you love</li><li>Guest count and venue</li><li>Any names or wording for banners and signs</li></ul></div></div>
<form class="box" id="contact-form" data-to="{EMAIL}" novalidate><h3 style="margin-top:0">Send us a message</h3>
<div class="row2"><div class="field"><label for="cf-name">Your name</label><input class="input" id="cf-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="cf-email">Your email</label><input class="input" id="cf-email" name="email" type="email" required autocomplete="email"></div></div>
<div class="row2"><div class="field"><label for="cf-topic">Topic</label><select class="input" id="cf-topic" name="topic"><option>Party ideas</option><option>Custom design</option><option>Question about a tool</option><option>Something else</option></select></div>
<div class="field"><label for="cf-date">Party date</label><input class="input" id="cf-date" name="event_date" type="date"></div></div>
<div class="field"><label for="cf-theme">Theme</label><select class="input" id="cf-theme" name="theme"><option>Not sure yet</option>{theme_opts}</select></div>
<div class="field"><label for="cf-msg">Message</label><textarea class="input" id="cf-msg" name="message" required></textarea></div>
<button class="btn" type="submit" data-confetti>Send message {ICONS['arrow']}</button><p class="form-note" style="margin-top:12px">Sending opens your email app with the message filled in.</p><p class="form-status" role="status"></p></form></div>"""
    simple_page("/contact/", "Contact Us", "Contact BC Paper Designs",
                f"Contact BC Paper Designs about baby shower and birthday party ideas, custom paper decorations or our free party tools. Email {EMAIL}.",
                contact, eyebrow="Say hello", priority="0.5", schema=[{"@type": "ContactPage", "url": ORIGIN + "/contact/"}])
    legal_date = "October 17, 2026"
    privacy = f"""<div class="prose"><p><em>Last updated {legal_date}</em></p>
<p>This policy explains what information bcpaperdesigns.com ("we", "us") handles when you use this website.</p>
<h2>Information you give us</h2><p>If you email us, including through the contact form (which opens your own email app), we receive your name, email address and whatever you write. We use it only to reply and keep it no longer than needed for that conversation.</p>
<h2>Information stored in your browser</h2><p>Our tools and checklists save your inputs, such as a party date, guest counts or ticked items, in your browser's local storage so they are there when you return. This data stays on your device; it is not sent to us. You can clear it at any time through your browser settings.</p>
<h2>Cookies and analytics</h2><p>We do not set advertising cookies. Our pages load fonts from Google Fonts, which receives your IP address and browser details to deliver the font files, under Google's own privacy policy. If we add privacy-friendly analytics in future, this page will be updated first.</p>
<h2>Children</h2><p>This site is written for adults planning parties. We do not knowingly collect information from children under 13.</p>
<h2>Your choices</h2><p>You can ask us to delete any email correspondence by writing to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest version.</p></div>"""
    simple_page("/privacy-policy/", "Privacy Policy", "Privacy Policy",
                "How BC Paper Designs handles your information: email enquiries, tool data saved in your own browser, fonts and cookies. No advertising cookies.",
                privacy, priority="0.2")
    terms = f"""<div class="prose"><p><em>Last updated {legal_date}</em></p>
<h2>Using this site</h2><p>The guides, ideas and tools on bcpaperdesigns.com are provided free for personal, non-commercial party planning. You may print banners, checklists and bingo cards made with our tools for your own events.</p>
<h2>Our content</h2><p>Text, layouts and designs on this site belong to {SITE['name']}. Please do not republish our guides or sell printables made from our designs without written permission.</p>
<h2>Trademarks</h2><p>Some guides mention popular character themes because that is what people search for. Our ideas use generic designs; we are not affiliated with, sponsored or endorsed by any rights holder, and all trademarks belong to their owners.</p>
<h2>No warranty</h2><p>Quantities, sizes and timelines are planning guides, not guarantees. Check food allergies with your guests, supervise children around small decorations, balloons and skewers, and follow your printer's paper limits.</p>
<h2>Contact</h2><p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""
    simple_page("/terms-of-use/", "Terms of Use", "Terms of Use",
                "Terms for using BC Paper Designs: free personal use of party guides and printable tools, content ownership, trademark notice and planning disclaimers.",
                terms, priority="0.2")


def build_sitemap_page():
    groups = [("Main pages", [("Home", "/"), ("Party themes", "/collections/"), ("Party tools", "/tools/"), ("Ideas blog", "/blog/"), ("About", "/about/"), ("Contact", "/contact/")]),
              ("Collections", [(c["name"], f"/collections/{k}/") for k, c in COLLECTIONS.items()]),
              ("Baby shower themes", [(short_name(t), theme_url(t)) for t in THEMES if t["occasion"] == "baby-shower"]),
              ("Birthday themes", [(short_name(t), theme_url(t)) for t in THEMES if t["occasion"] == "birthday"]),
              ("Shower or birthday themes", [(short_name(t), theme_url(t)) for t in THEMES if t["occasion"] == "both"]),
              ("Party tools", [(n, f"/tools/{s}/") for s, n, *_ in TOOLS]),
              ("Blog", [(strip_tags(p["title"]), f"/blog/{p['slug']}/") for p in POSTS]),
              ("Legal", [("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms-of-use/")])]
    inner = '<div class="sm-cols">' + "".join(
        f'<section><h2 style="font-size:1.3rem">{g}</h2><ul>{"".join(f"<li><a href=\"{u}\">{esc(n)}</a></li>" for n, u in items)}</ul></section>' for g, items in groups) + "</div>"
    simple_page("/sitemap/", "Sitemap", "Sitemap", "Every page on BC Paper Designs: party theme guides, collections, free party tools, blog posts and site information.", inner, priority="0.2")


def build_404():
    body = (f'<section class="notfound">{shapes(0)}<div class="wrap"><span class="big">404</span><h1>This party moved</h1>'
            f'<p class="lead mx-auto" style="max-width:560px">The page you were looking for isn\'t here. Our old shop pages are now free theme guides; try the full list.</p>'
            f'<div class="hero-ctas" style="justify-content:center"><a class="btn" href="/collections/">Browse party themes</a><a class="btn btn--ghost" href="/">Go home</a></div></div></section>')
    page("/404.html", "Page not found", "This page could not be found. Browse baby shower and birthday party themes at BC Paper Designs.", body, sitemap=False,
         head_extra='<meta name="robots" content="noindex">\n')
    # the generic robots meta from page() also appears; drop it for the 404
    fp = os.path.join(OUT, "404.html")
    s = open(fp, encoding="utf-8").read().replace('<meta name="robots" content="index, follow, max-image-preview:large">\n', "")
    open(fp, "w", encoding="utf-8").write(s)


# ================================================================ root files
INDEX_PHP = r"""<?php
// bcpaperdesigns.com front controller. The host serves existing files directly and
// sends "/" and unknown paths here (see README, "Hosting").
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$home = 'https://bcpaperdesigns.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Relative so redirects also work on the preview domain before DNS moves
function go($to) { header('Location: ' . $to, true, 301); exit; }

// Canonical host and scheme, only once the real domain points here
if ($host === 'www.bcpaperdesigns.com' || ($host === 'bcpaperdesigns.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$aliases = __ALIASES__;
$themes  = __THEMES__;
$collections = __COLLECTIONS__;

// Old Shopify product URLs, including /collections/<c>/products/<slug>
if (preg_match('#^(?:/collections/[^/]+)?/products/([^/.]+)#', $path, $m)) {
    $slug = strtolower($m[1]);
    if (isset($aliases[$slug])) $slug = $aliases[$slug];
    if (in_array($slug, $themes, true)) go('/products/' . $slug . '/');
    go('/collections/');
}
if (preg_match('#^/collections/([^/]+)/?$#', $path, $m)) {
    go(in_array($m[1], $collections, true) ? '/collections/' . $m[1] . '/' : '/collections/');
}
if (preg_match('#^/(collections|products)/?$#', $path)) go('/collections/');
if (preg_match('#^/pages/(about[^/]*)/?$#', $path)) go('/about/');
if (preg_match('#^/pages/(contact[^/]*)/?$#', $path)) go('/contact/');
if (preg_match('#^/blogs?(/.*)?$#', $path) && !is_dir(__DIR__ . $path)) go('/blog/');
if (preg_match('#^/(cart|account|search|checkout|index\.php/.*|my-account|wp-admin|wp-login\.php|feed)(/.*)?$#', $path)) go('/');
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) go($path . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""


def php_array(d):
    if isinstance(d, dict):
        return "[" + ", ".join(f"'{k}' => '{v}'" for k, v in d.items()) + "]"
    return "[" + ", ".join(f"'{v}'" for v in d) + "]"


def build_root():
    php = (INDEX_PHP.replace("__ALIASES__", php_array(PRODUCT_ALIASES)).replace("__THEMES__", php_array([t["slug"] for t in THEMES]))
           .replace("__COLLECTIONS__", php_array(list(COLLECTIONS))))
    write("/index.php", php)
    urls = "".join(f"<url><loc>{ORIGIN}{p}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>\n" for p, lm, pr in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /home.html\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    write("/site.webmanifest", json.dumps({"name": SITE["name"], "short_name": "BC Paper", "start_url": "/", "display": "standalone",
                                           "background_color": "#fffaf3", "theme_color": "#ff6f61",
                                           "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png"},
                                                     {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    write("/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">' + LOGO.split(">", 1)[1].replace("Fraunces, Georgia, serif", "Georgia, serif"))
    make_icons()


def make_icons():
    from PIL import Image, ImageDraw, ImageFont
    font_path = None
    for cand in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(cand):
            font_path = cand
            break
    for size, name in [(96, "favicon-96x96.png"), (180, "apple-touch-icon.png"), (192, "web-app-manifest-192x192.png"), (512, "web-app-manifest-512x512.png")]:
        S = size * 4
        im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        import math
        pts = []
        for i in range(48):
            r = S * (0.5 if i % 2 == 0 else 0.455)
            a = math.pi * 2 * i / 48
            pts.append((S / 2 + r * math.cos(a), S / 2 + r * math.sin(a)))
        d.polygon(pts, fill=(255, 111, 97, 255))
        f = ImageFont.truetype(font_path, int(S * 0.42)) if font_path else ImageFont.load_default()
        d.text((S / 2, S / 2 + S * 0.01), "bc", font=f, fill="white", anchor="mm")
        im.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name))
    # favicon.ico
    Image.open(os.path.join(OUT, "favicon-96x96.png")).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    # OG image 1200x630
    base = Image.open(os.path.join(IMG_DIR, "sprinkle-cake-party-table.webp")).convert("RGB")
    W, H = 1200, 630
    scale = max(W / base.width, H / base.height)
    base = base.resize((int(base.width * scale) + 1, int(base.height * scale) + 1)).crop((0, 0, W, H))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle((60, 170, 760, 460), 36, fill=(255, 250, 243, 238))
    ft = ImageFont.truetype(font_path, 64) if font_path else ImageFont.load_default()
    fs = ImageFont.truetype(font_path.replace("Serif-BoldItalic", "Sans").replace("Serif-Bold", "Sans"), 30) if font_path else ImageFont.load_default()
    d.text((100, 215), "BC Paper Designs", font=ft, fill=(42, 33, 64))
    d.text((100, 315), "Baby shower & birthday party themes,", font=fs, fill=(93, 86, 114))
    d.text((100, 360), "DIY paper decor and free party tools", font=fs, fill=(93, 86, 114))
    Image.alpha_composite(base.convert("RGBA"), ov).convert("RGB").save(os.path.join(IMG_DIR, "og-default.jpg"), quality=86)


def main():
    keep = {"assets"}
    for name in os.listdir(OUT):
        p = os.path.join(OUT, name)
        if name in keep:
            continue
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    build_home()
    build_collections()
    for t in THEMES:
        build_theme(t)
    build_blog()
    build_tools()
    build_static()
    build_sitemap_page()
    build_404()
    build_root()
    print(f"built {len(PAGES)} pages ({len(THEMES)} themes, {len(POSTS)} posts) into {OUT}")


if __name__ == "__main__":
    main()
