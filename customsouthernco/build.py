#!/usr/bin/env python3
"""Generate the customsouthernco.com static site into ./site/.

Stdlib + Pillow (only for reading image dimensions). Run from anywhere:
    python3 customsouthernco/build.py && python3 customsouthernco/validate.py
"""
import html
import importlib.util
import json
import re
import shutil
from datetime import date
from pathlib import Path

from siteconfig import CATEGORIES, NAV, SEASONS, SITE, TOOLS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
IMG = ROOT / "assets" / "img"
TODAY = date.today().isoformat()
ASSET_V = "1"

esc = html.escape


# --------------------------------------------------------------------------- content

def load_posts():
    posts = []
    for f in sorted((ROOT / "content").glob("posts_*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        posts.extend(mod.POSTS)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


POSTS = load_posts()
BY_SLUG = {p["slug"]: p for p in POSTS}
TOOL_BY_KEY = {t["key"]: t for t in TOOLS}


def img_size(key, small=False):
    try:
        from PIL import Image
        with Image.open(IMG / f"{key}{'-sm' if small else ''}.webp") as im:
            return im.size
    except Exception:
        return (1600, 1067) if not small else (720, 480)


def picture(key, alt, cls="", eager=False, sizes="(max-width: 760px) 100vw, 760px"):
    w, h = img_size(key)
    sw, _ = img_size(key, small=True)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{key}.webp" srcset="/assets/img/{key}-sm.webp {sw}w, '
            f'/assets/img/{key}.webp {w}w" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{esc(alt, quote=True)}" {load}>')


def words(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


def reading_time(p):
    n = words(p["body"]) + sum(words(a) + words(b) for a, b in p.get("steps", []))
    return max(3, round(n / 220))


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%B %-d, %Y")


# --------------------------------------------------------------------------- icons

ICONS = {
    "tin": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="6" width="14" height="15" rx="2"/><path d="M5 9h14M8 3h8l1 3H7z"/></svg>',
    "jar": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 3h8v3H8zM7 6h10l1 3v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V9z"/><path d="M6 12h12"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9 15a3 3 0 0 0 3 3"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "search": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>',
    "pinterest": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M11 8.5c3-1 5 1 4.2 3.6-.6 2-2.6 2.6-3.6 1.4M11.5 10l-2 9"/></svg>',
    "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/></svg>',
    "link": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
}


def icon(name):
    return f'<span class="ico">{ICONS[name]}</span>'


LOGO = ('<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/>'
        '<circle cx="24" cy="24" r="17" class="ring"/><text x="24" y="29.5" text-anchor="middle">CS</text></svg>')


# --------------------------------------------------------------------------- layout

def org_schema():
    return {
        "@type": "Organization",
        "@id": SITE["url"] + "/#org",
        "name": SITE["name"],
        "url": SITE["url"] + "/",
        "email": SITE["email"],
        "logo": {"@type": "ImageObject", "url": SITE["url"] + "/favicon-512.png", "width": 512, "height": 512},
        "description": SITE["description"],
    }


def website_schema():
    return {
        "@type": "WebSite",
        "@id": SITE["url"] + "/#website",
        "url": SITE["url"] + "/",
        "name": SITE["name"],
        "description": SITE["tagline"],
        "publisher": {"@id": SITE["url"] + "/#org"},
        "inLanguage": "en-US",
    }


def crumbs_schema(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + u}
            for i, (n, u) in enumerate(items)
        ],
    }


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(parts) + "</nav>"


def header(active=""):
    links = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if active == u else ""}>{esc(n)}</a></li>' for n, u in NAV
    )
    tools = "".join(
        f'<li><a href="/tools/{t["slug"]}/">{icon(t["icon"])}<span><strong>{esc(t["name"])}</strong>'
        f'<small>{esc(t["short"])}</small></span></a></li>'
        for t in TOOLS
    )
    mobile_tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in TOOLS)
    mobile_links = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{esc(SITE['name'])} home">{LOGO}<span class="brand-text">Custom Southern<em>Co.</em></span></a>
    <nav class="main-nav" aria-label="Main">
      <ul>
        {links}
        <li class="has-drop">
          <button class="drop-btn" aria-expanded="false" aria-controls="tools-menu">Tools <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
          <ul class="drop" id="tools-menu">{tools}</ul>
        </li>
      </ul>
    </nav>
    <a class="btn btn-sm header-cta" href="/contact/">Say hello</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav" aria-hidden="true">
  <div class="mobile-nav-inner">
    <ul class="m-primary">
      <li><a href="/">Home</a></li>
      {mobile_links}
    </ul>
    <p class="m-label">Tools</p>
    <ul class="m-tools">{mobile_tools}</ul>
    <ul class="m-secondary">
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Contact</a></li>
    </ul>
    <a class="m-mail" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
  </div>
</div>"""


def footer():
    cats = "".join(f'<li><a href="/category/{k}/">{esc(c["name"])}</a></li>' for k, c in CATEGORIES.items())
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in TOOLS)
    popular = "".join(
        f'<li><a href="/{s}/">{esc(BY_SLUG[s]["title"])}</a></li>'
        for s in ["history-of-prince-albert-tins", "how-to-make-laundry-detergent-with-3-ingredients",
                  "how-to-repurpose-antique-light-globes", "easy-vintage-cutting-board-decor"]
        if s in BY_SLUG
    )
    return f"""<footer class="site-footer">
  <div class="footer-wave" aria-hidden="true"><svg viewBox="0 0 1440 60" preserveAspectRatio="none"><path d="M0 30c120-20 240-20 360 0s240 20 360 0 240-20 360 0 240 20 360 0v30H0z"/></svg></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand" href="/">{LOGO}<span class="brand-text">Custom Southern<em>Co.</em></span></a>
      <p>{esc(SITE['description'])}</p>
      <a class="footer-mail" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
    </div>
    <div><h2>Explore</h2><ul>{cats}<li><a href="/blog/">All articles</a></li></ul></div>
    <div><h2>Tools</h2><ul>{tools}</ul></div>
    <div><h2>Popular</h2><ul>{popular}</ul></div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; {date.today().year} {esc(SITE['name'])} All rights reserved.</p>
    <ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy</a></li><li><a href="/terms-of-use/">Terms</a></li><li><a href="/sitemap/">Sitemap</a></li></ul>
  </div>
  <a class="to-top" href="#top" aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 15 6-6 6 6"/></svg></a>
</footer>"""


def page(path, title, description, body, *, schema=None, og_image="hero", og_type="website",
         active="", body_class="", extra_head="", noindex=False, scripts=("site",)):
    canonical = SITE["url"] + path
    graph = [org_schema(), website_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    full_title = title if SITE["name"] in title else f"{title} | {SITE['name']}"
    img_url = f"{SITE['url']}/assets/img/{og_image}.webp"
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    js = "".join(f'<script src="/assets/js/{s}.js?v={ASSET_V}" defer></script>' for s in scripts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description, quote=True)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{esc(SITE['name'], quote=True)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title, quote=True)}">
<meta property="og:description" content="{esc(description, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img_url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title, quote=True)}">
<meta name="twitter:description" content="{esc(description, quote=True)}">
<meta name="twitter:image" content="{img_url}">
<meta name="theme-color" content="#2f3b2b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..700&family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{extra_head}<script type="application/ld+json">{ld}</script>
</head>
<body class="{body_class}">
{header(active)}
<main id="main">
{body}
</main>
{footer()}
{js}
</body>
</html>
"""


def write(path, content):
    target = OUT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------- components

def card(p, cls="card", eager=False):
    cat = CATEGORIES[p["category"]]["name"]
    meta = f'{icon("clock")}{reading_time(p)} min read'
    return f"""<article class="{cls} reveal">
  <a class="card-img" href="/{p['slug']}/" tabindex="-1" aria-hidden="true">{picture(p['image'], p['image_alt'], eager=eager, sizes="(max-width: 760px) 100vw, 400px")}</a>
  <div class="card-body">
    <a class="chip" href="/category/{p['category']}/">{esc(cat)}</a>
    <h3><a href="/{p['slug']}/">{esc(p['title'])}</a></h3>
    <p>{esc(p['excerpt'])}</p>
    <span class="card-meta">{meta}</span>
  </div>
</article>"""


def tool_widget(key):
    t = TOOL_BY_KEY[key]
    inner = TOOL_MARKUP[key]
    return f"""<section class="tool" data-tool="{key}" aria-labelledby="tool-{key}">
  <div class="tool-head">{icon(t['icon'])}<div><p class="eyebrow">Interactive tool</p><h2 id="tool-{key}">{esc(t['name'])}</h2><p>{esc(t['short'])}</p></div></div>
  {inner}
</section>"""


TIN_CLUES = [
    ("patent", "Lid reads “Patented July 30th 1907” (or a similar 1907 patent line)", 1907, 1930, "The 1907 patent line shows up on early pocket tins; it was dropped from later lids."),
    ("price", "A price such as “5¢” or “10¢” is printed on the tin", 1907, 1945, "Printed prices are typical of earlier tins, before inflation made them impractical."),
    ("stamp", "A paper federal tax-stamp strip runs over the lid", 1907, 1959, "Federal tobacco tax stamps were discontinued at the end of the 1950s."),
    ("noZip", "Address reads “Winston-Salem, N.C.” with no ZIP code", 1907, 1965, "ZIP codes arrived in 1963 and took a couple of years to reach packaging."),
    ("zip", "A ZIP code (27102) appears after Winston-Salem", 1963, 1987, "ZIP codes were introduced in July 1963."),
    ("upc", "There is a UPC barcode", 1974, 2026, "UPC barcodes went into use in 1974 and spread through the late 1970s."),
    ("middleton", "The maker is John Middleton, not R.J. Reynolds", 1987, 2026, "Reynolds sold Prince Albert to John Middleton in 1987."),
    ("plastic", "Plastic lid or a mostly cardboard can", 1970, 2026, "Composite and plastic-lid cans are later packaging."),
    ("hinged", "Flat pocket tin with a hinged flip-top lid", 1907, 1990, "The classic pocket tin; made for decades, so on its own it only rules out modern cans."),
]


def tin_markup():
    items = "".join(
        f'<label class="check"><input type="checkbox" name="{k}" data-min="{a}" data-max="{b}" data-note="{esc(n, quote=True)}"><span>{esc(t)}</span></label>'
        for k, t, a, b, n in TIN_CLUES
    )
    return f"""<div class="tool-grid">
    <fieldset><legend>Tick every clue you can see on your tin</legend>{items}</fieldset>
    <div class="tool-out" aria-live="polite">
      <div class="timeline" aria-hidden="true"><div class="tl-bar"><span class="tl-range"></span></div><div class="tl-ticks"><span>1907</span><span>1930</span><span>1960</span><span>1990</span><span>Today</span></div></div>
      <p class="result-big" data-out="range">Tick a clue to start</p>
      <ul class="result-notes" data-out="notes"></ul>
      <p class="fine">An estimate from printed clues only. Condition, rarity and graphics drive value. See our <a href="/vintage-tobacco-tin-values/">tobacco tin value guide</a>.</p>
    </div>
  </div>"""


JAR_LOGOS = [
    ("buck", "BALL", "Block capital letters, no script", "about 1885–1895", "Early block-letter jars, often with no “Ball” script at all. Usually aqua."),
    ("triple", "Ball", "Script with a long looping tail under the word (the “3-L” loop)", "about 1895–1910", "The tail of the final “l” loops back under the word. Aqua glass is common."),
    ("dropped", 'B<span class="drop-a">a</span>ll', "Script where the “a” sits lower than the other letters (the “dropped A”)", "about 1910–1923", "Look for the “a” hanging below the line and an underline that does not connect."),
    ("underline", "Ball", "Script with a straight underline beneath the word", "about 1923–1933", "Clean script with a separate underscore. Ball Blue glass is typical."),
    ("nounder", "Ball", "Script with no underline", "about 1933–1962", "The classic mid-century look. Clear glass becomes common from the late 1930s."),
    ("modern", "Ball", "Modern simplified script, often with a ® mark", "about 1960 to today", "Current-production style. The ® registered-trademark mark points to newer jars."),
]


def jar_markup():
    opts = "".join(
        f'<button type="button" class="logo-opt" data-key="{k}" data-era="{esc(era, quote=True)}" data-note="{esc(n, quote=True)}" aria-pressed="false">'
        f'<span class="logo-sample logo-{k}">{w}</span><span class="logo-label">{esc(lbl)}</span></button>'
        for k, w, lbl, era, n in JAR_LOGOS
    )
    return f"""<div class="jar-tool">
    <p class="step-label"><span>1</span> Which logo matches your jar?</p>
    <div class="logo-grid">{opts}</div>
    <p class="step-label"><span>2</span> What color is the glass?</p>
    <div class="seg" role="radiogroup" aria-label="Glass color">
      <label><input type="radio" name="glass" value="aqua"><span class="sw sw-aqua"></span>Aqua</label>
      <label><input type="radio" name="glass" value="blue"><span class="sw sw-blue"></span>Ball Blue</label>
      <label><input type="radio" name="glass" value="clear"><span class="sw sw-clear"></span>Clear</label>
      <label><input type="radio" name="glass" value="color"><span class="sw sw-color"></span>Amber / green / purple</label>
    </div>
    <div class="tool-out jar-out" aria-live="polite">
      <p class="result-big" data-out="era">Pick a logo to see its era</p>
      <p data-out="note"></p>
      <p data-out="glass" class="glass-note"></p>
      <p class="fine">The number on the bottom is a mold number, not a year, and “Patent Nov 30th 1858” refers to John Mason's patent, not the jar's age.</p>
    </div>
  </div>"""


def detergent_markup():
    return """<div class="tool-grid calc">
    <form class="calc-form" onsubmit="return false">
      <label>Loads of laundry per week <output data-for="loads">6</output><input type="range" name="loads" min="1" max="20" value="6"></label>
      <label>Weeks you want to cover <output data-for="weeks">8</output><input type="range" name="weeks" min="1" max="52" value="8"></label>
      <label>Scoop per load
        <select name="scoop"><option value="1">1 tablespoon (HE / soft water)</option><option value="1.5" selected>1½ tablespoons</option><option value="2">2 tablespoons (heavy soil / hard water)</option></select></label>
      <details class="prices"><summary>Adjust prices</summary>
        <label>Bar soap, per bar <span class="pre">$</span><input type="number" name="pSoap" value="1.79" step="0.01" min="0"></label>
        <label>Washing soda, per box (about 6½ cups) <span class="pre">$</span><input type="number" name="pSoda" value="6.49" step="0.01" min="0"></label>
        <label>Borax, per box (about 8 cups) <span class="pre">$</span><input type="number" name="pBorax" value="6.99" step="0.01" min="0"></label>
        <label>Store detergent, cost per load <span class="pre">$</span><input type="number" name="pStore" value="0.22" step="0.01" min="0"></label>
      </details>
    </form>
    <div class="tool-out" aria-live="polite">
      <div class="stats">
        <div><span class="stat" data-out="batches">1</span><small>batches to mix</small></div>
        <div><span class="stat" data-out="perLoad">$0.00</span><small>DIY cost per load</small></div>
        <div><span class="stat" data-out="save">$0.00</span><small>saved vs. store</small></div>
      </div>
      <h3>Your shopping &amp; mixing list</h3>
      <ul class="mix" data-out="mix"></ul>
      <div class="bars" aria-hidden="true"><div><span>DIY</span><i data-bar="diy"></i></div><div><span>Store</span><i data-bar="store"></i></div></div>
      <p class="fine">One batch = 1 bar grated soap + 1 cup washing soda + 1 cup borax, about 3½ cups. Prices are typical US shelf prices; edit them to match your store.</p>
    </div>
  </div>"""


def finder_markup():
    return """<div class="finder">
    <div class="finder-filters">
      <div class="seg" role="radiogroup" aria-label="Season">
        <label><input type="radio" name="season" value="any" checked><span>Any season</span></label>
        <label><input type="radio" name="season" value="spring"><span>Spring</span></label>
        <label><input type="radio" name="season" value="summer"><span>Summer</span></label>
        <label><input type="radio" name="season" value="fall"><span>Fall</span></label>
        <label><input type="radio" name="season" value="christmas"><span>Christmas</span></label>
        <label><input type="radio" name="season" value="valentine"><span>Valentine's</span></label>
        <label><input type="radio" name="season" value="year"><span>Year-round</span></label>
      </div>
      <div class="finder-row">
        <label>Time I have <select name="time"><option value="any">Any</option><option value="60">Under an hour</option><option value="180">An afternoon</option><option value="9999">A weekend</option></select></label>
        <label>Budget <select name="budget"><option value="any">Any</option><option value="15">Under $15</option><option value="30">Under $30</option><option value="9999">Whatever it takes</option></select></label>
        <label>Skill <select name="skill"><option value="any">Any</option><option value="Easy">Easy only</option><option value="Moderate">Up for a challenge</option></select></label>
        <button type="button" class="btn btn-ghost btn-sm" data-act="surprise">Surprise me</button>
      </div>
    </div>
    <p class="finder-count" aria-live="polite" data-out="count"></p>
    <div class="finder-results" data-out="results"></div>
  </div>"""


TOOL_MARKUP = {}


def init_tool_markup():
    TOOL_MARKUP.update({
        "tin-dater": tin_markup(),
        "jar-dater": jar_markup(),
        "detergent": detergent_markup(),
        "project-finder": finder_markup(),
    })


def minutes(t):
    """Rough minutes from strings like '45 minutes', '2 hours', '1-2 hours', 'An afternoon'."""
    t = t.lower()
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", t)]
    n = max(nums) if nums else 3
    if "day" in t or "weekend" in t:
        return 600
    if "hour" in t or "hr" in t:
        return int(n * 60)
    if "afternoon" in t:
        return 180
    return int(n)


def dollars(c):
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", c or "")]
    return max(nums) if nums else 0


def finder_data():
    rows = []
    for p in POSTS:
        if "steps" not in p:
            continue
        rows.append({
            "s": p["slug"], "t": p["title"], "e": p["excerpt"], "i": p["image"],
            "season": SEASONS.get(p["slug"], "year"), "min": minutes(p.get("time", "")),
            "time": p.get("time", ""), "cost": p.get("cost", ""), "usd": dollars(p.get("cost")),
            "skill": p.get("difficulty", "Easy"),
        })
    return rows


# --------------------------------------------------------------------------- post page

def howto_block(p):
    sup = "".join(f"<li><label><input type=\"checkbox\"><span>{esc(s)}</span></label></li>" for s in p["supplies"])
    steps = "".join(
        f'<li class="reveal"><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for n, d in p["steps"]
    )
    return f"""<div class="howto" id="how-to">
  <div class="howto-meta">
    <div><small>Time</small><strong>{esc(p.get('time', ''))}</strong></div>
    <div><small>Difficulty</small><strong>{esc(p.get('difficulty', ''))}</strong></div>
    <div><small>Cost</small><strong>{esc(p.get('cost', ''))}</strong></div>
  </div>
  <div class="supplies"><h2>What you'll need</h2><p class="fine">Tap to check items off as you gather them.</p><ul>{sup}</ul></div>
  <h2>How to make it</h2>
  <ol class="steps">{steps}</ol>
</div>"""


def render_body(p):
    b = p["body"]
    b = re.sub(r"<p>\s*(\{\{[^}]+\}\})\s*</p>", r"\1", b)

    def img_sub(m):
        key, _, cap = m.group(1).partition("|")
        key = key.strip()
        cap = cap.strip()
        return f'<figure class="inline-fig reveal">{picture(key, cap or p["image_alt"])}<figcaption>{esc(cap)}</figcaption></figure>'

    b = re.sub(r"\{\{img:([^}]+)\}\}", img_sub, b)
    b = re.sub(r"\{\{tool:([a-z-]+)\}\}", lambda m: tool_widget(m.group(1)), b)
    if "steps" in p:
        if "{{howto}}" in b:
            b = b.replace("{{howto}}", howto_block(p), 1)
        else:
            parts = b.split("</p>", 2)
            b = "</p>".join(parts[:2]) + "</p>" + howto_block(p) + (parts[2] if len(parts) > 2 else "")
    b = b.replace("{{howto}}", "")
    # give every h2 an id for the table of contents
    seen = set()

    def h2_sub(m):
        text = re.sub(r"<[^>]+>", "", m.group(1))
        sid = re.sub(r"[^a-z0-9]+", "-", html.unescape(text).lower()).strip("-")[:60]
        while sid in seen:
            sid += "-2"
        seen.add(sid)
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    b = re.sub(r"<h2>(.*?)</h2>", h2_sub, b)
    return b


def toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    if len(items) < 3:
        return ""
    lis = "".join(f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="In this article"><p>In this article</p><ol>{lis}</ol></nav>'


def build_post(p):
    cat = CATEGORIES[p["category"]]
    url = f"/{p['slug']}/"
    body = render_body(p)
    faq = "".join(
        f'<details class="faq-item"><summary>{esc(q)}</summary><div><p>{esc(a)}</p></div></details>' for q, a in p["faq"]
    )
    related = [BY_SLUG[s] for s in p.get("related", []) if s in BY_SLUG and s != p["slug"]]
    if len(related) < 3:
        related += [x for x in POSTS if x["category"] == p["category"] and x not in related and x is not p][: 3 - len(related)]
    rel_cards = "".join(card(r) for r in related[:3])
    tools_used = re.findall(r'data-tool="([a-z-]+)"', body)
    tool_side = "".join(
        f'<a class="side-tool" href="/tools/{t["slug"]}/">{icon(t["icon"])}<span><strong>{esc(t["name"])}</strong><small>{esc(t["short"])}</small></span></a>'
        for t in TOOLS if t["key"] not in tools_used
    )[:5000]
    crumbs = [("Home", "/"), (cat["name"], f"/category/{p['category']}/"), (p["title"], url)]
    schema = [
        {
            "@type": "BlogPosting",
            "@id": SITE["url"] + url + "#article",
            "headline": p["title"],
            "description": p["description"],
            "image": f"{SITE['url']}/assets/img/{p['image']}.webp",
            "datePublished": p["date"],
            "dateModified": p.get("updated", p["date"]),
            "author": {"@type": "Organization", "name": SITE["author"], "url": SITE["url"] + "/about/"},
            "publisher": {"@id": SITE["url"] + "/#org"},
            "mainEntityOfPage": SITE["url"] + url,
            "articleSection": cat["name"],
            "keywords": p["keyword"],
            "wordCount": words(p["body"]),
        },
        crumbs_schema(crumbs),
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]
            ],
        },
    ]
    if "steps" in p:
        schema.append({
            "@type": "HowTo",
            "name": p["title"],
            "description": p["description"],
            "image": f"{SITE['url']}/assets/img/{p['image']}.webp",
            "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": str(dollars(p.get("cost")) or "")},
            "supply": [{"@type": "HowToSupply", "name": s} for s in p["supplies"]],
            "step": [
                {"@type": "HowToStep", "position": i + 1, "name": n, "text": d, "url": f"{SITE['url']}{url}#how-to"}
                for i, (n, d) in enumerate(p["steps"])
            ],
        })
    share = SITE["url"] + url
    meta_bits = [f"{fmt_date(p['date'])}", f"{reading_time(p)} min read"]
    content = f"""<article class="post">
  <header class="post-hero">
    <div class="post-hero-img">{picture(p['image'], p['image_alt'], eager=True, sizes="100vw")}</div>
    <div class="wrap post-hero-inner">
      {crumbs_html(crumbs)}
      <a class="chip chip-light" href="/category/{p['category']}/">{esc(cat['name'])}</a>
      <h1>{esc(p['title'])}</h1>
      <p class="post-meta">By {esc(SITE['author'])} <span>·</span> {' <span>·</span> '.join(meta_bits)}</p>
    </div>
  </header>
  <div class="wrap post-layout">
    <div class="prose">
      <p class="lede">{esc(p['excerpt'])}</p>
      {body}
      <section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{faq}</section>
      <div class="share">
        <span>Share this:</span>
        <a href="https://www.pinterest.com/pin/create/button/?url={share}&amp;media={SITE['url']}/assets/img/{p['image']}.webp&amp;description={esc(p['title'], quote=True)}" target="_blank" rel="noopener" aria-label="Pin on Pinterest">{icon('pinterest')}</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={share}" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon('facebook')}</a>
        <button type="button" class="copy-link" data-url="{share}" aria-label="Copy link">{icon('link')}<span>Copy link</span></button>
      </div>
    </div>
    <aside class="sidebar">
      {toc(body)}
      <div class="side-box"><p class="side-title">Handy tools</p>{tool_side}</div>
      <div class="side-box side-note">{LOGO}<p>Found something old and curious? Send us a photo at <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p></div>
    </aside>
  </div>
</article>
<section class="section related">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Keep reading</p><h2>More from {esc(cat['name'])}</h2></div>
    <div class="grid-3">{rel_cards}</div>
  </div>
</section>"""
    write(url, page(url, p["seo_title"], p["description"], content, schema=schema, og_image=p["image"],
                    og_type="article", body_class="is-post", scripts=("site", "tools") if tools_used else ("site",)))


# --------------------------------------------------------------------------- listings

def build_category(key):
    c = CATEGORIES[key]
    url = f"/category/{key}/"
    items = [p for p in POSTS if p["category"] == key]
    crumbs = [("Home", "/"), (c["name"], url)]
    chips = "".join(
        f'<a class="chip{" is-active" if k == key else ""}" href="/category/{k}/">{esc(v["name"])}</a>' for k, v in CATEGORIES.items()
    )
    body = f"""<section class="page-hero page-hero-img">
  <div class="page-hero-bg">{picture(c['image'], c['name'], eager=True, sizes="100vw")}</div>
  <div class="wrap">{crumbs_html(crumbs)}<h1>{esc(c['name'])}</h1><p>{esc(c['blurb'])}</p></div>
</section>
<section class="section">
  <div class="wrap">
    <div class="chips-row">{chips}</div>
    <div class="grid-3">{''.join(card(p) for p in items)}</div>
  </div>
</section>"""
    schema = [crumbs_schema(crumbs), {
        "@type": "CollectionPage", "name": c["name"], "url": SITE["url"] + url, "description": c["blurb"],
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE['url']}/{p['slug']}/"} for i, p in enumerate(items)]},
    }]
    write(url, page(url, f"{c['name']}: Ideas & Guides", f"{c['blurb']} Browse every {c['name'].lower()} article from Custom Southern Co.",
                    body, schema=schema, og_image=c["image"], active=url))


def build_blog():
    url = "/blog/"
    chips = '<button class="chip is-active" data-filter="all">All</button>' + "".join(
        f'<button class="chip" data-filter="{k}">{esc(v["name"])}</button>' for k, v in CATEGORIES.items()
    )
    cards = "".join(
        card(p).replace('<article class="card reveal">',
                        f'<article class="card reveal" data-cat="{p["category"]}" data-search="{esc((p["title"] + " " + p["excerpt"] + " " + p["keyword"]).lower(), quote=True)}">', 1)
        for p in POSTS
    )
    feat = BY_SLUG.get("history-of-prince-albert-tins", POSTS[0])
    body = f"""<section class="page-hero">
  <div class="wrap">{crumbs_html([("Home", "/"), ("Blog", url)])}<h1>The Custom Southern Co. Blog</h1>
  <p>Vintage history, repurposed decor tutorials and Southern home know-how, {len(POSTS)} articles and counting.</p></div>
</section>
<section class="section">
  <div class="wrap">
    <a class="feature-wide reveal" href="/{feat['slug']}/">
      <div class="fw-img">{picture(feat['image'], feat['image_alt'], sizes="(max-width: 760px) 100vw, 600px")}</div>
      <div class="fw-body"><span class="chip">Most read</span><h2>{esc(feat['title'])}</h2><p>{esc(feat['excerpt'])}</p><span class="link-arrow">Read the story {icon('arrow')}</span></div>
    </a>
    <div class="blog-tools">
      <div class="chips-row" role="group" aria-label="Filter by category">{chips}</div>
      <label class="search">{icon('search')}<span class="sr">Search articles</span><input type="search" placeholder="Search articles…" data-blog-search></label>
    </div>
    <div class="grid-3" data-blog-grid>{cards}</div>
    <p class="empty" hidden data-blog-empty>No articles match that search. Try “jar”, “Christmas” or “tin”.</p>
  </div>
</section>"""
    schema = [crumbs_schema([("Home", "/"), ("Blog", url)]), {
        "@type": "Blog", "name": "The Custom Southern Co. Blog", "url": SITE["url"] + url,
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE['url']}/{p['slug']}/", "datePublished": p["date"]} for p in POSTS],
    }]
    write(url, page(url, "Blog: Vintage Finds, DIY Decor & Southern Home",
                    "Read the Custom Southern Co. blog: the history of vintage finds, easy repurposed decor tutorials, seasonal farmhouse DIY and Southern home tips.",
                    body, schema=schema, active=url))


# --------------------------------------------------------------------------- tools

def build_tools():
    data = json.dumps(finder_data(), ensure_ascii=False)
    for t in TOOLS:
        url = f"/tools/{t['slug']}/"
        crumbs = [("Home", "/"), ("Tools", "/tools/"), (t["name"], url)]
        rel = "".join(card(BY_SLUG[s]) for s in t["related"] if s in BY_SLUG)
        intro = TOOL_INTRO[t["key"]]
        extra = f'<script>window.CSC_PROJECTS={data};</script>' if t["key"] == "project-finder" else ""
        body = f"""<section class="page-hero page-hero-tool">
  <div class="wrap">{crumbs_html(crumbs)}<p class="eyebrow">Free tool</p><h1>{esc(t['name'])}</h1><p>{esc(t['short'])}</p></div>
</section>
<section class="section section-tight">
  <div class="wrap narrow">{tool_widget(t['key'])}</div>
</section>
<section class="section section-tight">
  <div class="wrap narrow prose">{intro}</div>
</section>
<section class="section related"><div class="wrap"><div class="section-head"><p class="eyebrow">Learn more</p><h2>Related guides</h2></div><div class="grid-3">{rel}</div></div></section>"""
        schema = [crumbs_schema(crumbs), {
            "@type": "WebApplication", "name": t["name"], "url": SITE["url"] + url, "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "Any (web browser)", "description": t["description"],
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        }]
        write(url, page(url, t["seo_title"], t["description"], body, schema=schema, extra_head=extra,
                        scripts=("site", "tools")))
    # tools hub
    url = "/tools/"
    cards = "".join(
        f"""<a class="tool-card reveal" href="/tools/{t['slug']}/">{icon(t['icon'])}<h2>{esc(t['name'])}</h2><p>{esc(t['short'])}</p><span class="link-arrow">Open tool {icon('arrow')}</span></a>"""
        for t in TOOLS
    )
    body = f"""<section class="page-hero page-hero-tool"><div class="wrap">{crumbs_html([("Home", "/"), ("Tools", url)])}<h1>Free Tools for Vintage Lovers</h1>
<p>Date a tobacco tin or a Ball jar, price out homemade laundry detergent, or find your next weekend project.</p></div></section>
<section class="section"><div class="wrap"><div class="tool-cards">{cards}</div></div></section>"""
    write(url, page(url, "Free Tools for Vintage Collectors & DIYers",
                    "Free interactive tools from Custom Southern Co.: Prince Albert tin dater, Ball jar age finder, DIY laundry detergent calculator and a DIY project finder.",
                    body, schema=[crumbs_schema([("Home", "/"), ("Tools", url)])]))


TOOL_INTRO = {
    "tin-dater": """<h2>How the tin dater works</h2>
<p>Prince Albert tins changed in small, datable ways over more than a century. Each clue you tick sets an earliest or latest possible year, and the tool shows the window where all of your clues overlap. The more clues you can find, the tighter the range.</p>
<h2>Where to look on your tin</h2>
<ul><li><strong>The lid:</strong> early pocket tins carry a 1907 patent line, and many older tins still have a strip of paper tax stamp across the lid or remnants of the glue.</li>
<li><strong>The back panel:</strong> the maker's name and address. “R.J. Reynolds Tobacco Co., Winston-Salem, N.C.” with no ZIP code points to an older tin, a ZIP code means 1963 or later, and a barcode means mid-1970s or newer.</li>
<li><strong>The material:</strong> all-metal lithographed tins came first. Cardboard bodies and plastic lids are later packaging.</li></ul>
<div class="tip"><strong>Tip:</strong> Clues can conflict if a tin has been repaired or a lid has been swapped. If the tool says the clues do not overlap, check whether the lid matches the body.</div>
<p>Want the full story of the brand, the famous prank-call joke and what tins sell for? Read our <a href="/history-of-prince-albert-tins/">history of Prince Albert tins</a> and the <a href="/vintage-tobacco-tin-values/">vintage tobacco tin value guide</a>.</p>""",
    "jar-dater": """<h2>Dating a Ball jar by its logo</h2>
<p>Ball changed the script on its jars several times, and collectors use those logo styles as the quickest way to date a jar. The ranges overlap because old molds stayed in use after new ones arrived, so treat the result as an era, not an exact year.</p>
<h2>Three things that do not tell you the age</h2>
<ul><li><strong>“Patent Nov 30th 1858”:</strong> that is the date of John Landis Mason's patent, and it was embossed on jars for decades afterward.</li>
<li><strong>The number on the bottom:</strong> it identifies the mold, not the year.</li>
<li><strong>The lid:</strong> lids and bands are easily swapped, so judge the glass, not the closure.</li></ul>
<p>For the full walk-through, with glass colors, rare variants and what to collect, read <a href="/how-to-date-ball-mason-jars/">how to date Ball mason jars</a> and <a href="/what-vintage-jars-to-look-for/">what vintage jars to look for</a>.</p>""",
    "detergent": """<h2>About the recipe</h2>
<p>The calculator uses the classic three-ingredient homemade laundry detergent: one bar of grated laundry soap, one cup of washing soda and one cup of borax. That makes about three and a half cups of powder, enough for roughly 28 to 56 loads depending on your scoop.</p>
<h2>How the cost per load is worked out</h2>
<p>We divide the price of each box by the number of cups in it to get a cost per cup, add the bar of soap, and divide the batch cost by the number of loads it makes. Edit the prices to match your store.</p>
<div class="tip"><strong>Tip:</strong> Use the 1-tablespoon setting for high-efficiency (HE) machines. Powder this low-sudsing is generally fine in HE washers, but check your machine's manual first.</div>
<p>Step-by-step mixing instructions, safety notes and troubleshooting are in our <a href="/how-to-make-laundry-detergent-with-3-ingredients/">3-ingredient laundry detergent guide</a>. Pair it with our <a href="/homemade-fabric-softener/">homemade fabric softener</a>.</p>""",
    "project-finder": """<h2>How to use the project finder</h2>
<p>Every project on Custom Southern Co. is tagged by season, how long it takes, what it costs and how tricky it is. Choose what matters to you and the list updates instantly, or hit <em>Surprise me</em> to pick at random.</p>
<p>Most of our projects start with something secondhand: a cutting board, an old window, a light globe or a stack of hymnals. Browse the <a href="/category/diy-repurpose/">DIY &amp; Repurpose</a> and <a href="/category/seasonal/">Seasonal Decor</a> collections for even more ideas.</p>""",
}


# --------------------------------------------------------------------------- home

def build_home():
    feat = BY_SLUG.get("history-of-prince-albert-tins", POSTS[0])
    side = [BY_SLUG[s] for s in ["how-to-make-laundry-detergent-with-3-ingredients", "how-to-repurpose-antique-light-globes", "pie-bird"] if s in BY_SLUG]
    side_html = "".join(
        f"""<a class="mini reveal" href="/{p['slug']}/"><span class="mini-img">{picture(p['image'], p['image_alt'], sizes="160px")}</span>
<span><small>{esc(CATEGORIES[p['category']]['name'])}</small><strong>{esc(p['title'])}</strong></span></a>"""
        for p in side
    )
    cats = "".join(
        f"""<a class="cat-tile reveal" href="/category/{k}/">{picture(c['image'], c['name'], sizes="(max-width: 760px) 100vw, 300px")}
<span class="cat-body"><strong>{esc(c['name'])}</strong><small>{sum(1 for p in POSTS if p['category'] == k)} articles</small></span></a>"""
        for k, c in CATEGORIES.items()
    )
    tools = "".join(
        f"""<a class="tool-card reveal" href="/tools/{t['slug']}/">{icon(t['icon'])}<h3>{esc(t['name'])}</h3><p>{esc(t['short'])}</p><span class="link-arrow">Try it {icon('arrow')}</span></a>"""
        for t in TOOLS
    )
    diy = [p for p in POSTS if "steps" in p][:6]
    latest = "".join(card(p) for p in diy)
    seasons = [("christmas", "Christmas"), ("fall", "Fall"), ("spring", "Spring"), ("valentine", "Valentine's"), ("summer", "Summer")]
    tabs = "".join(
        f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>'
        for i, (k, n) in enumerate(seasons)
    )
    panels = ""
    for i, (k, n) in enumerate(seasons):
        items = [p for p in POSTS if SEASONS.get(p["slug"]) == k][:4]
        inner = "".join(
            f"""<a class="season-item" href="/{p['slug']}/">{picture(p['image'], p['image_alt'], sizes="(max-width: 760px) 50vw, 280px")}<span>{esc(p['title'])}</span></a>"""
            for p in items
        )
        panels += f'<div class="season-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>{inner}</div>'
    marquee_words = ["Prince Albert tins", "Ball jars", "Pie birds", "Barn wood", "Spindles", "Hymnals", "Jello molds",
                     "Light globes", "Yardsticks", "Spice tins", "Old windows", "Cutting boards", "Door knobs", "Funnels"]
    marquee = "".join(f"<span>{w}</span><i>✦</i>" for w in marquee_words)
    n_tools = len(TOOLS)
    n_diy = sum(1 for p in POSTS if "steps" in p)
    body = f"""<section class="hero">
  <div class="hero-bg">{picture('hero', 'Vintage farmhouse decor with old jars, tins and weathered wood', eager=True, sizes="100vw")}</div>
  <div class="hero-grain" aria-hidden="true"></div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow eyebrow-light">Vintage · Repurposed · Southern</p>
      <h1>Old things,<br><span class="hand">new stories.</span></h1>
      <p class="hero-sub">Custom Southern Co. digs into the history of vintage finds, from Prince Albert tins to Ball jars, and turns flea-market treasures into easy, handmade decor.</p>
      <div class="hero-ctas"><a class="btn" href="/blog/">Explore the blog {icon('arrow')}</a><a class="btn btn-ghost-light" href="/tools/">Try our free tools</a></div>
    </div>
    <div class="stamp" aria-hidden="true">
      <svg viewBox="0 0 200 200"><defs><path id="circ" d="M100 100 m-78 0 a78 78 0 1 1 156 0 a78 78 0 1 1 -156 0"/></defs>
      <text><textPath href="#circ">VINTAGE FINDS ✦ SOUTHERN MADE ✦ REPURPOSED DECOR ✦ </textPath></text></svg>
      <span>CS<small>Co.</small></span>
    </div>
  </div>
  <a class="scroll-cue" href="#featured" aria-label="Scroll to featured stories"><span></span></a>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}{marquee}</div></div>

<section class="section" id="featured">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Reader favorite</p><h2>Stories behind the stuff</h2></div>
    <div class="feature-grid">
      <a class="feature-main reveal" href="/{feat['slug']}/">
        {picture(feat['image'], feat['image_alt'], sizes="(max-width: 760px) 100vw, 700px")}
        <span class="fm-body"><span class="chip chip-light">{esc(CATEGORIES[feat['category']]['name'])}</span><strong>{esc(feat['title'])}</strong><small>{esc(feat['excerpt'])}</small></span>
      </a>
      <div class="feature-side">{side_html}</div>
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="wrap">
    <div class="section-head center"><p class="eyebrow">Browse by topic</p><h2>Find your kind of vintage</h2></div>
    <div class="cat-grid">{cats}</div>
  </div>
</section>

<section class="section section-dark tools-band">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow eyebrow-light">Free &amp; interactive</p><h2>Tools for collectors &amp; makers</h2>
    <p>Date your tin, identify your jar, price out homemade detergent or find your next project.</p></div>
    <div class="tool-cards">{tools}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split"><div><p class="eyebrow">Weekend projects</p><h2>Fresh from the workbench</h2></div><a class="link-arrow" href="/category/diy-repurpose/">All DIY projects {icon('arrow')}</a></div>
    <div class="grid-3">{latest}</div>
  </div>
</section>

<section class="section section-cream">
  <div class="wrap">
    <div class="section-head center"><p class="eyebrow">Decorate by the calendar</p><h2>What are you decorating for?</h2></div>
    <div class="tabs" role="tablist" aria-label="Seasons">{tabs}</div>
    {panels}
  </div>
</section>

<section class="section">
  <div class="wrap about-band">
    <div class="about-img reveal">{picture('about', 'Hands at a workbench restoring a vintage find', sizes="(max-width: 760px) 100vw, 520px")}</div>
    <div class="about-copy reveal">
      <p class="eyebrow">How we pick</p>
      <h2>Every piece has a past</h2>
      <ol class="process">
        <li><strong>Hunt.</strong> Flea markets, barn sales, estate sales and Grandma's attic.</li>
        <li><strong>Learn.</strong> We dig into who made it, when, and why it mattered.</li>
        <li><strong>Make.</strong> Then we give it a second life with simple, budget-friendly DIY.</li>
      </ol>
      <div class="counters">
        <div><span class="count" data-count="{len(POSTS)}">0</span><small>articles</small></div>
        <div><span class="count" data-count="{n_diy}">0</span><small>DIY projects</small></div>
        <div><span class="count" data-count="{n_tools}">0</span><small>free tools</small></div>
      </div>
      <a class="btn" href="/about/">Our story {icon('arrow')}</a>
    </div>
  </div>
</section>

<section class="section cta-band">
  <div class="wrap cta-inner reveal">
    <div><h2>Found something old and curious?</h2><p>Send us a photo of your tin, jar or junk-pile mystery and we may feature it in a future post.</p></div>
    <a class="btn btn-light" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
  </div>
</section>"""
    schema = [{
        "@type": "WebPage", "@id": SITE["url"] + "/#webpage", "url": SITE["url"] + "/", "name": SITE["name"],
        "isPartOf": {"@id": SITE["url"] + "/#website"}, "about": {"@id": SITE["url"] + "/#org"},
        "description": SITE["description"],
    }]
    html_out = page("/", f"{SITE['name']} | Vintage Finds & Repurposed DIY Decor",
                    "Custom Southern Co. shares the history of vintage finds like Prince Albert tins and Ball jars, plus easy repurposed decor DIY and Southern home tips.",
                    body, schema=schema, body_class="is-home")
    (OUT / "home.html").write_text(html_out, encoding="utf-8")


# --------------------------------------------------------------------------- static pages

def simple_page(url, title, seo_title, desc, inner, crumbs_name=None, schema_extra=None):
    crumbs = [("Home", "/"), (crumbs_name or title, url)]
    body = f"""<section class="page-hero"><div class="wrap">{crumbs_html(crumbs)}<h1>{esc(title)}</h1></div></section>
<section class="section section-tight"><div class="wrap narrow prose">{inner}</div></section>"""
    write(url, page(url, seo_title, desc, body, schema=[crumbs_schema(crumbs)] + (schema_extra or [])))


def build_static():
    simple_page("/about/", "About Custom Southern Co.", "About Us",
                "Custom Southern Co. is a vintage and DIY blog about the history of everyday antiques, repurposed decor and old-fashioned Southern home know-how.",
                f"""<figure class="inline-fig">{picture('about', 'Restoring a vintage find at the workbench')}</figure>
<p class="lede">Custom Southern Co. is a home for people who can't walk past a box of old tins at a yard sale.</p>
<p>We write about the everyday antiques that turn up at flea markets, barn sales and estate sales across the South: Prince Albert tobacco tins, Ball mason jars, pie birds, hymnals, spindles, yardsticks and light globes. For each one we dig into where it came from and how to date it, then share simple ways to give it a second life as decor.</p>
<h2>What you'll find here</h2>
<ul><li><strong><a href="/category/vintage-finds/">Vintage Finds</a>:</strong> history, dating and collecting guides.</li>
<li><strong><a href="/category/diy-repurpose/">DIY &amp; Repurpose</a>:</strong> step-by-step projects using secondhand pieces.</li>
<li><strong><a href="/category/seasonal/">Seasonal Decor</a>:</strong> Christmas, fall, spring, Valentine's and summer ideas.</li>
<li><strong><a href="/category/southern-home/">Southern Home</a>:</strong> homemade laundry basics, porch decor and practical care tips.</li>
<li><strong><a href="/tools/">Free tools</a>:</strong> a Prince Albert tin dater, a Ball jar age finder, a laundry detergent calculator and a project finder.</li></ul>
<h2>Our approach</h2>
<p>We keep projects budget-friendly and beginner-friendly, and we say so when a technique needs extra care, such as old paint that may contain lead or a vintage light fixture that needs rewiring. Dates and values in our collecting guides are estimates; condition and rarity always have the final say.</p>
<h2>Say hello</h2>
<p>Questions, corrections or a mystery find you'd like identified? Email us at <a href="mailto:{SITE['email']}">{SITE['email']}</a> or use the <a href="/contact/">contact page</a>.</p>""",
                schema_extra=[{"@type": "AboutPage", "url": SITE["url"] + "/about/", "name": "About Custom Southern Co."}])

    simple_page("/contact/", "Contact Us", "Contact Custom Southern Co.",
                "Contact Custom Southern Co. with questions, corrections, collaboration ideas or a vintage find you'd like identified. Email info@customsouthernco.com.",
                f"""<p class="lede">We'd love to hear from you, whether it's a question about a project, a correction, or a photo of a mystery find.</p>
<div class="contact-grid">
  <form class="contact-form" action="/contact.php" method="post">
    <label>Your name<input name="name" autocomplete="name" required></label>
    <label>Email<input type="email" name="email" autocomplete="email" required></label>
    <label>Subject<select name="subject"><option>General question</option><option>Identify my find</option><option>Correction</option><option>Collaboration</option></select></label>
    <label>Message<textarea name="message" rows="6" required></textarea></label>
    <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
    <button class="btn" type="submit">Send message {icon('arrow')}</button>
    <p class="form-status" role="status" hidden></p>
  </form>
  <div class="contact-card">
    <p class="side-title">Email us directly</p>
    <a class="big-mail" href="mailto:{SITE['email']}">{icon('mail')}{SITE['email']}</a>
    <p>We read every message and usually reply within a few days.</p>
    <p class="side-title">Identifying a find?</p>
    <p>Include clear photos of the front, back, bottom and any maker's marks. Try our <a href="/tools/prince-albert-tin-dater/">tin dater</a> or <a href="/tools/ball-jar-age-finder/">jar age finder</a> first.</p>
  </div>
</div>""", schema_extra=[{"@type": "ContactPage", "url": SITE["url"] + "/contact/", "name": "Contact Custom Southern Co."}])

    simple_page("/privacy-policy/", "Privacy Policy", "Privacy Policy",
                "Read the Custom Southern Co. privacy policy: what information we collect, how we use it, cookies, third-party services and how to contact us.",
                f"""<p><em>Last updated {fmt_date(TODAY)}</em></p>
<p>This policy explains how {SITE['name']} (“we”, “us”) handles information when you visit {SITE['domain']}.</p>
<h2>Information we collect</h2>
<p>We do not require an account and we do not sell personal information. If you email us or use our contact form, we receive the name, email address and message you choose to send, and we use it only to reply. Our web host keeps standard server logs (IP address, browser type, pages requested and time of visit) for security and troubleshooting.</p>
<h2>Cookies and local storage</h2>
<p>Our pages do not set advertising cookies. Some interactive tools remember your last inputs in your own browser's local storage; that data never leaves your device. Fonts are loaded from Google Fonts, which may log your IP address under Google's privacy policy.</p>
<h2>Sharing links</h2>
<p>Share buttons link to Pinterest and Facebook. Those services only receive information if you click them, under their own privacy policies.</p>
<h2>Children</h2>
<p>This site is not directed at children under 13, and we do not knowingly collect their information.</p>
<h2>Changes and contact</h2>
<p>We may update this policy and will change the date above when we do. Questions? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>""")

    simple_page("/terms-of-use/", "Terms of Use", "Terms of Use",
                "The terms of use for customsouthernco.com, covering use of our content, DIY project safety, collecting estimates, interactive tools and external links.",
                f"""<p><em>Last updated {fmt_date(TODAY)}</em></p>
<p>By using {SITE['domain']} you agree to these terms.</p>
<h2>Content</h2>
<p>Articles, tools and graphics on this site are for personal, non-commercial use. You're welcome to share a link or a single image with a link back to the original post; please don't republish full articles.</p>
<h2>DIY projects and safety</h2>
<p>Projects are shared for general information. Use appropriate safety gear, follow product labels, test finishes first, and take extra care with old paint that may contain lead, sharp or rusty metal, glass and any electrical work. You are responsible for your own projects.</p>
<h2>Dates, values and tool results</h2>
<p>Dates, price ranges and tool results are estimates for general guidance, not appraisals. Condition, rarity and market demand determine real value.</p>
<h2>Liability</h2>
<p>The site is provided “as is” without warranties. To the fullest extent permitted by law, {SITE['name']} is not liable for any loss arising from use of the site.</p>
<h2>Contact</h2>
<p>Questions about these terms? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>""")

    # html sitemap
    groups = ""
    for k, c in CATEGORIES.items():
        lis = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["title"])}</a></li>' for p in POSTS if p["category"] == k)
        groups += f'<h2><a href="/category/{k}/">{esc(c["name"])}</a></h2><ul>{lis}</ul>'
    tl = "".join(f'<li><a href="/tools/{t["slug"]}/">{esc(t["name"])}</a></li>' for t in TOOLS)
    simple_page("/sitemap/", "Sitemap", "Sitemap",
                "Every page on Custom Southern Co. in one place: vintage history guides, DIY repurposed decor projects, seasonal ideas, free tools and site information.",
                f"""<ul><li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li><li><a href="/tools/">Tools</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul>
<h2><a href="/tools/">Tools</a></h2><ul>{tl}</ul>{groups}""")

    # 404
    picks = "".join(card(BY_SLUG[s]) for s in ["history-of-prince-albert-tins", "easy-vintage-cutting-board-decor", "how-to-make-laundry-detergent-with-3-ingredients"] if s in BY_SLUG)
    body = f"""<section class="page-hero"><div class="wrap"><p class="eyebrow">Error 404</p><h1>This page wandered off to a flea market</h1>
<p>We couldn't find what you were looking for. Try the <a href="/blog/">blog</a> or one of these favorites.</p></div></section>
<section class="section"><div class="wrap"><div class="grid-3">{picks}</div></div></section>"""
    (OUT / "404.html").write_text(page("/404.html", "Page Not Found", "The page you were looking for could not be found.", body, noindex=True), encoding="utf-8")


# --------------------------------------------------------------------------- root files

INDEX_PHP = """<?php
// customsouthernco.com - static site front controller.
// The host serves existing files directly and sends / and unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://customsouthernco.com';

$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';   // TLS ends upstream
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.customsouthernco.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// Old WordPress-era URLs and short links -> closest new page.
$moved = [
    '/feed/' => '/blog/', '/feed' => '/blog/', '/comments/feed/' => '/blog/',
    '/d05b' => '/', '/u2ur' => '/', '/shop/' => '/', '/about-me/' => '/about/', '/contact-me/' => '/contact/',
    '/blog-2/' => '/blog/', '/home/' => '/',
];
if (isset($moved[$path])) {
    header('Location: ' . $home . $moved[$path], true, 301);
    exit;
}
if (preg_match('#^/category/[^/]+/feed/?$#', $path) || preg_match('#^/[a-z0-9-]+/feed/?$#', $path)) {
    header('Location: ' . $home . preg_replace('#feed/?$#', '', $path), true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\\.php|xmlrpc\\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}
if (preg_match('#^/(tag|author|page)/#', $path) || preg_match('#^/\\d{4}/\\d{2}/#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
"""

CONTACT_PHP = """<?php
// Minimal contact form handler: validates, drops spam, mails info@customsouthernco.com.
$to = 'info@customsouthernco.com';
$back = '/contact/';
$ajax = ($_SERVER['HTTP_ACCEPT'] ?? '') === 'application/json';
function done($ok, $msg, $ajax, $back) {
    if ($ajax) { header('Content-Type: application/json'); echo json_encode(['ok' => $ok, 'message' => $msg]); exit; }
    header('Location: ' . $back . '?sent=' . ($ok ? '1' : '0'), true, 303); exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: ' . $back, true, 303); exit; }
if (!empty($_POST['website'])) { done(true, 'Thanks!', $ajax, $back); }
$name = trim(substr(strip_tags($_POST['name'] ?? ''), 0, 120));
$email = filter_var(trim($_POST['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$subject = trim(substr(strip_tags($_POST['subject'] ?? 'General question'), 0, 80));
$message = trim(substr(strip_tags($_POST['message'] ?? ''), 0, 5000));
if (!$name || !$email || !$message) { done(false, 'Please fill in your name, a valid email and a message.', $ajax, $back); }
$name = str_replace(["\\r", "\\n"], ' ', $name);
$headers = "From: Custom Southern Co. <{$to}>\\r\\nReply-To: {$name} <{$email}>\\r\\nContent-Type: text/plain; charset=utf-8";
$ok = @mail($to, "[Contact] {$subject} - {$name}", "Name: {$name}\\nEmail: {$email}\\n\\n{$message}", $headers);
done($ok, $ok ? "Thanks, {$name}! Your message is on its way." : 'Sorry, the message could not be sent. Please email ' . $to . ' directly.', $ajax, $back);
"""


def build_root_files():
    (OUT / "index.php").write_text(INDEX_PHP, encoding="utf-8")
    (OUT / "contact.php").write_text(CONTACT_PHP, encoding="utf-8")
    urls = [("/", TODAY, "1.0"), ("/blog/", TODAY, "0.8"), ("/tools/", TODAY, "0.7")]
    urls += [(f"/tools/{t['slug']}/", TODAY, "0.7") for t in TOOLS]
    urls += [(f"/category/{k}/", TODAY, "0.6") for k in CATEGORIES]
    urls += [(f"/{p['slug']}/", p.get("updated", p["date"]), "0.8") for p in POSTS]
    urls += [(u, TODAY, "0.3") for u in ["/about/", "/contact/", "/privacy-policy/", "/terms-of-use/", "/sitemap/"]]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE['url']}{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
    sm += "</urlset>\n"
    (OUT / "sitemap.xml").write_text(sm, encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": SITE["name"], "short_name": SITE["short"], "start_url": "/", "display": "standalone",
        "background_color": "#f6efe3", "theme_color": "#2f3b2b",
        "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/favicon-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=1), encoding="utf-8")


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="31" fill="#2f3b2b"/><circle cx="32" cy="32" r="25" fill="none" stroke="#d9a441" stroke-width="2" stroke-dasharray="3 3"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="24" font-weight="700" fill="#f6efe3">CS</text></svg>"""


def build_icons():
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "favicon-192.png"), (512, "favicon-512.png")]:
        s = size * 4
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse([0, 0, s - 1, s - 1], fill="#2f3b2b")
        m = s * 0.11
        d.ellipse([m, m, s - m, s - m], outline="#d9a441", width=max(2, s // 40))
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", int(s * 0.38))
        except OSError:
            font = ImageFont.load_default()
        d.text((s / 2, s / 2 + s * 0.02), "CS", fill="#f6efe3", font=font, anchor="mm")
        im.resize((size, size), Image.LANCZOS).save(OUT / name)
    Image.open(OUT / "favicon-32.png").save(OUT / "favicon.ico", sizes=[(32, 32)])


# --------------------------------------------------------------------------- main

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets", ignore=shutil.ignore_patterns("SOURCES.json"))
    init_tool_markup()
    for p in POSTS:
        build_post(p)
    for k in CATEGORIES:
        build_category(k)
    build_blog()
    build_tools()
    build_home()
    build_static()
    build_root_files()
    build_icons()
    print(f"built {len(POSTS)} posts, {len(CATEGORIES)} categories, {len(TOOLS)} tools -> {OUT}")


if __name__ == "__main__":
    main()
