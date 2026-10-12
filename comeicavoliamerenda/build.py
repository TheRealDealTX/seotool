#!/usr/bin/env python3
"""Static site generator for comeicavoliamerenda.com.

    python3 build.py      # writes the site into dist/
    python3 validate.py   # checks the output

Standard library only. Content lives in content/*.py (one ARTICLES list per category).
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
sys.path.insert(0, os.path.join(ROOT, "content"))

SITE = "https://comeicavoliamerenda.com"
NAME = "Come i Cavoli a Merenda"
EMAIL = "info@comeicavoliamerenda.com"
TODAY = datetime.date(2026, 10, 12)
PUBLISHED = "2026-10-12"
VERSION = "1"

CATS = {
    "guides": dict(slug="earring-guides", name="Earring Guides", short="Guides",
                   blurb="Actual-size charts, gauges, backs and the everyday questions nobody else answers properly.",
                   image="diamond-studs"),
    "piercings": dict(slug="piercings", name="Ear Piercings", short="Piercings",
                      blurb="Helix, rook, tragus, double lobes and more: placement, healing and the jewelry that fits.",
                      image="ear-stack"),
    "celebrity": dict(slug="celebrity-earrings", name="Celebrity Earrings", short="Celebrity",
                      blurb="The famous earrings people still search for, and how to get the look without the price tag.",
                      image="portrait-gold"),
    "popculture": dict(slug="pop-culture-earrings", name="Pop Culture Earrings", short="Pop Culture",
                       blurb="Anime, games and fandom jewelry, from Potara fusions to Luna Lovegood's radishes.",
                       image="sapphire-drops"),
    "style": dict(slug="earring-styles", name="Earring Styles & Brands", short="Styles",
                  blurb="Designer names, decade trends, jhumkas and a straight-talking guide to earrings for guys.",
                  image="twist-hoops"),
}
CAT_ORDER = ["guides", "piercings", "celebrity", "popculture", "style"]

NAV = [("Guides", "/earring-guides/"), ("Piercings", "/piercings/"), ("Celebrity", "/celebrity-earrings/"),
       ("Pop Culture", "/pop-culture-earrings/"), ("Styles", "/earring-styles/"), ("About", "/about/")]

IMG_DIR = os.path.join(ROOT, "assets", "img")


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]


def webp_size(path):
    """Return (width, height) of a lossy/lossless/extended WebP without PIL."""
    with open(path, "rb") as f:
        d = f.read(40)
    fmt = d[12:16]
    if fmt == b"VP8 ":
        return int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF
    if fmt == b"VP8L":
        b = d[21:25]
        w = 1 + (((b[1] & 0x3F) << 8) | b[0])
        h = 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
        return w, h
    if fmt == b"VP8X":
        return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    raise ValueError(path)


def img(key, alt, cls="", sizes="(max-width: 700px) 100vw, 50vw", eager=False):
    w, h = webp_size(os.path.join(IMG_DIR, key + ".webp"))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/assets/img/{key}-800.webp" srcset="/assets/img/{key}-800.webp 800w, '
            f'/assets/img/{key}.webp 1600w" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" {load}>')


# --------------------------------------------------------------------------- content
def load_articles():
    arts = []
    for mod in ["guides", "piercings", "celebrity", "popculture", "style"]:
        m = __import__(mod)
        for a in m.ARTICLES:
            a = dict(a)
            a.setdefault("image", None)
            a["url"] = f"/{a['slug']}/"
            arts.append(a)
    return arts


ARTICLES = load_articles()
BY_SLUG = {a["slug"]: a for a in ARTICLES}


# --------------------------------------------------------------------------- layout
def org_schema():
    return {
        "@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
        "email": EMAIL, "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo.png"},
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": NAME,
            "alternateName": "Cavoli a Merenda", "inLanguage": "en-US", "publisher": {"@id": SITE + "/#org"},
            "description": "An independent earring and ear-piercing guide: actual-size charts, gauges, piercing guides and style stories."}


def breadcrumb_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def header(active=""):
    lis = []
    for label, url in NAV:
        cur = ' aria-current="page"' if url == active else ""
        lis.append(f'<li><a href="{url}"{cur}>{label}</a></li>')
    cur = ' aria-current="page"' if active == "/earring-size-tool/" else ""
    lis.append(f'<li><a class="nav-cta" href="/earring-size-tool/"{cur}>Size Tool</a></li>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap nav-bar">
    <a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark" aria-hidden="true"></span><span>Come i Cavoli <em>a Merenda</em></span></a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="main-nav"><span></span><span></span><span></span></button>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{''.join(lis)}</ul>
    </nav>
  </div>
</header>"""


def footer():
    cats = "".join(f'<li><a href="/{CATS[c]["slug"]}/">{CATS[c]["name"]}</a></li>' for c in CAT_ORDER)
    pop = "".join(f'<li><a href="/{s}/">{esc(BY_SLUG[s]["h1"] if len(BY_SLUG[s]["h1"]) < 34 else BY_SLUG[s]["keyword"].capitalize())}</a></li>'
                  for s in ["5mm-earrings-actual-size", "what-gauge-are-regular-earrings", "ear-gauge-size-chart",
                            "triple-forward-helix-earrings", "types-of-earring-backs"] if s in BY_SLUG)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/"><span class="logo-mark" aria-hidden="true"></span><span>Come i Cavoli <em>a Merenda</em></span></a>
        <p>An independent guide to earrings and ear piercings, for ears that don't have to match. Size charts, gauges, piercing guides and the stories behind famous earrings.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h3>Explore</h3><ul>{cats}<li><a href="/earring-size-tool/">Earring Size Tool</a></li></ul></div>
      <div><h3>Popular</h3><ul>{pop}</ul></div>
      <div><h3>The site</h3><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/sitemap/">Sitemap</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>&copy; <span data-year>{TODAY.year}</span> {NAME}. Independent and not affiliated with any brand mentioned.</span><span>Made with mismatched earrings in mind.</span></div>
  </div>
  <div class="big-word" aria-hidden="true">cavoli a merenda</div>
</footer>"""


def page(path, title, description, body, schema=None, active="", og_image="hoops-book", og_type="website",
         robots="index, follow", body_class=""):
    url = SITE + path
    graph = [org_schema(), website_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    ogimg = f"{SITE}/assets/img/{og_image}.webp"
    bc = f' class="{body_class}"' if body_class else ""
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimg}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d1424">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
<script type="application/ld+json">{ld}</script>
</head>
<body{bc}>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


# --------------------------------------------------------------------------- components
def card(a, delay=0):
    cat = CATS[a["category"]]
    if a.get("image"):
        media = img(a["image"], a.get("image_alt", a["h1"]), sizes="(max-width: 620px) 100vw, (max-width: 1000px) 50vw, 380px")
    else:
        media = f'<div class="art art-{a["category"]}" aria-hidden="true"><span>{esc(short_label(a))}</span></div>'
    d = f" d{delay}" if delay else ""
    return f"""<a class="card reveal{d}" href="{a['url']}">
  <div class="card-media">{media}</div>
  <div class="card-body"><span class="tag">{cat['short']}</span><h3>{esc(a['h1'])}</h3><p>{esc(trim(a['description'], 120))}</p><span class="more">Read the guide</span></div>
</a>"""


def short_label(a):
    return " ".join(w if w[:1].isdigit() else w[:1].upper() + w[1:] for w in a["keyword"].split())


def trim(s, n):
    s = strip_tags(s)
    return s if len(s) <= n else s[: s.rfind(" ", 0, n)].rstrip(",.;:") + "…"


def sizer_widget(start=5, compact=False):
    chips = "".join(f'<button type="button" class="chip" data-v="{v}">{v} mm</button>' for v in [2, 3, 4, 5, 6, 7, 8, 10, 12])
    cal = "" if compact else """
  <div class="calib" data-calibrate>
    <h3>Make it truly actual size</h3>
    <p class="note">Screens differ. Hold a credit card (or any ID-1 card) against the screen and drag until the dashed outline matches it exactly. We remember the setting on this device.</p>
    <div class="card-outline">Match a bank card here</div>
    <input type="range" min="150" max="900" step="1" value="323" aria-label="Calibrate card width">
    <p><button type="button" class="chip" data-reset>Reset calibration</button></p>
  </div>"""
    more = '<p class="note">Want it calibrated to your screen? <a href="/earring-size-tool/">Open the full Earring Size Tool</a>.</p>' if compact else ""
    return f"""<div class="sizer" data-sizer>
  <div class="sizer-stage"><span class="gem" aria-hidden="true"></span><span class="coin" aria-hidden="true">1¢</span></div>
  <div class="sizer-controls">
    <div class="sizer-readout"><b data-mm>{start} mm</b><span><span data-in></span> · <span data-cmp></span></span></div>
    <input type="range" min="2" max="14" step="0.5" value="{start}" aria-label="Stud diameter in millimeters">
    <div class="chip-row">{chips}</div>
    <p class="note">The copper coin is a US penny (19.05 mm) for scale.</p>
  </div>{cal}
  {more}
</div>"""


def gauge_widget():
    return """<div class="sizer" data-gauge>
  <div class="sizer-stage"><span class="gem gold" aria-hidden="true"></span></div>
  <label class="note" for="gauge-select"><strong>Pick a gauge</strong> (dot shown 3× magnified so thin wires are visible)</label>
  <div class="form" style="padding:0;border:0;box-shadow:none;background:none"><select id="gauge-select"></select></div>
  <p data-gout style="margin-top:14px"></p>
</div>"""


def add_ids(body):
    seen = set()
    toc = []

    def rep(m):
        attrs, inner = m.group(1), m.group(2)
        hid = slugify(inner) or "section"
        base, i = hid, 2
        while hid in seen:
            hid = f"{base}-{i}"; i += 1
        seen.add(hid)
        toc.append((hid, strip_tags(inner)))
        return f'<h2 id="{hid}"{attrs}>{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S)
    body = body.replace('<table class="tbl">', '<div class="tbl-wrap"><table class="tbl">').replace("</table>", "</table></div>")
    return body, toc


# --------------------------------------------------------------------------- pages
def article_page(a):
    cat = CATS[a["category"]]
    body_html, toc = add_ids(a["body"])
    words = len(strip_tags(a["body"]).split()) + sum(len((q + " " + ans).split()) for q, ans in a["faqs"])
    mins = max(3, round(words / 230))
    quick = "".join(f"<li>{q}</li>" for q in a["quick"])
    widget = ""
    if a["slug"] in ("5mm-earrings-actual-size", "8mm-earrings-actual-size"):
        widget = f'<h2 id="see-it">See it to scale</h2>{sizer_widget(8 if a["slug"].startswith("8mm") else 5, compact=True)}'
        toc.insert(0, ("see-it", "See it to scale"))
    elif a["slug"] in ("what-gauge-are-regular-earrings", "ear-gauge-size-chart"):
        widget = f'<h2 id="gauge-converter">Gauge converter</h2>{gauge_widget()}'
        toc.insert(0, ("gauge-converter", "Gauge converter"))
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{ans}</p></details>" for q, ans in a["faqs"])
    toc_html = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    related = [BY_SLUG[s] for s in a.get("related", []) if s in BY_SLUG and s != a["slug"]]
    if len(related) < 3:
        related += [x for x in ARTICLES if x["category"] == a["category"] and x["slug"] != a["slug"] and x not in related][: 3 - len(related)]
    rel = "".join(card(r, i % 3 + 1) for i, r in enumerate(related[:3]))
    feature = ""
    if a.get("image"):
        feature = f'<figure class="feature-img">{img(a["image"], a.get("image_alt", a["h1"]), sizes="(max-width: 1000px) 100vw, 820px", eager=True)}</figure>'
    crumbs = [("Home", "/"), (cat["name"], f"/{cat['slug']}/"), (a["h1"], a["url"])]
    schema = [
        {"@type": "Article", "@id": SITE + a["url"] + "#article", "headline": a["h1"], "description": a["description"],
         "mainEntityOfPage": SITE + a["url"], "datePublished": PUBLISHED, "dateModified": PUBLISHED,
         "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US",
         "articleSection": cat["name"], "keywords": a["keyword"],
         "image": f"{SITE}/assets/img/{a.get('image') or cat['image']}.webp", "wordCount": words},
        breadcrumb_schema(crumbs),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
                                             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(ans)}} for q, ans in a["faqs"]]},
    ]
    body = f"""<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>
  <div class="sparkles" data-n="14" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/{cat['slug']}/">{cat['name']}</a></nav>
    <h1>{esc(a['h1'])}</h1>
    <p>{esc(a['description'])}</p>
    <div class="meta-row"><a class="pill" href="/{cat['slug']}/">{cat['short']}</a><span>{mins} min read</span><span>Updated {TODAY.strftime('%B %-d, %Y')}</span></div>
  </div>
</section>
<div class="wrap">
  <div class="article-wrap">
    <article>
      {feature}
      <div class="quick"><h2>Quick answer</h2><ul>{quick}</ul></div>
      <div class="prose">
        {widget}
        {body_html}
      </div>
      <section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{faqs}</section>
    </article>
    <aside class="sidebar">
      <nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc_html}<li><a href="#faq-h">FAQs</a></li></ol></nav>
      <div class="promo"><span class="gem" aria-hidden="true"></span><h3>How big is 5mm, really?</h3><p>See any stud size at true scale on your own screen, from 2mm to 14mm.</p><a class="btn btn-gold" href="/earring-size-tool/">Open the Size Tool</a></div>
    </aside>
  </div>
</div>
<section class="related"><div class="wrap"><div class="section-head"><h2>Keep reading</h2><a class="btn btn-dark" href="/{cat['slug']}/">All {cat['short'].lower()}</a></div><div class="cards">{rel}</div></div></section>"""
    body_class = "has-feature" if feature else ""
    return page(a["url"], a["title"], a["description"], body, schema, active=f"/{cat['slug']}/",
                og_image=a.get("image") or cat["image"], og_type="article", body_class=body_class)


def hub_page(key):
    cat = CATS[key]
    arts = [a for a in ARTICLES if a["category"] == key]
    url = f"/{cat['slug']}/"
    cards = "".join(card(a, i % 3 + 1) for i, a in enumerate(arts))
    intro = HUB_INTROS[key]
    schema = [breadcrumb_schema([("Home", "/"), (cat["name"], url)]),
              {"@type": "CollectionPage", "name": cat["name"], "url": SITE + url, "description": cat["blurb"],
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": SITE + a["url"], "name": a["h1"]} for i, a in enumerate(arts)]}}]
    body = f"""<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div>
  <div class="sparkles" data-n="16" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>{cat['name']}</nav>
    <h1>{cat['name']}</h1>
    <p>{cat['blurb']}</p>
  </div>
</section>
<section class="section tight"><div class="wrap">
  <div class="prose reveal" style="max-width:820px;margin-bottom:46px">{intro}</div>
  <div class="cards">{cards}</div>
</div></section>"""
    titles = {"guides": "Earring Guides: Sizes, Gauges, Backs & Care",
              "piercings": "Ear Piercing Guides: Helix, Rook, Tragus & More",
              "celebrity": "Celebrity Earrings: Famous Looks & How to Get Them",
              "popculture": "Pop Culture Earrings: Anime, Games & Fandom",
              "style": "Earring Styles & Brands: Trends, Jhumkas, Men's"}
    return page(url, titles[key] + " | Cavoli a Merenda" if len(titles[key]) < 42 else titles[key],
                f"{cat['blurb']} Browse every {cat['short'].lower()} guide on {NAME}."[:158], body, schema,
                active=url, og_image=cat["image"])


HUB_INTROS = {
    "guides": "<p>Earrings are tiny, and the numbers that describe them are confusing: millimeters for stud faces, gauges for posts, carats for stones. These guides turn the numbers into something you can picture, then cover the practical stuff like backs, storage and that smell. Start with the <a href=\"/5mm-earrings-actual-size/\">actual-size stud chart</a> or the <a href=\"/ear-gauge-size-chart/\">gauge size chart</a>.</p>",
    "piercings": "<p>Every ear is shaped differently, which is exactly why a curated ear looks so personal. Here is what to expect from each cartilage and lobe placement: where it sits, how long it really takes to heal, and which jewelry actually fits once it has. Always book with a reputable professional piercer, and treat our guides as the homework you do before the appointment.</p>",
    "celebrity": "<p>Some earrings outlive the moment they were worn. Janet's key, Bowie's single drop, Harry's pearl: people are still searching for them years later. We cover the story behind each look and how to recreate it with pieces you can actually buy.</p>",
    "popculture": "<p>Fandom jewelry is where earrings get fun. Fusion earrings from Dragon Ball, Erza's armor-matching studs, the earrings Skyrim never gave you: here is the lore, the cosplay tips and how to tell a well-made fan piece from a cheap one.</p>",
    "style": "<p>Logos, decades and traditions: this is where we cover the names and shapes people search for most, from Chanel's interlocking Cs to bell-shaped jhumkas and big 80s hoops. Plus an honest look at earrings for guys, because men have worn earrings for thousands of years. We are independent and never paid to mention a brand.</p>",
}


def home_page():
    def pick(slugs):
        return [BY_SLUG[s] for s in slugs if s in BY_SLUG]
    top = pick(["5mm-earrings-actual-size", "what-gauge-are-regular-earrings", "triple-forward-helix-earrings",
                "why-do-my-earrings-smell", "jason-aldean-earrings", "8mm-earrings-actual-size"])
    top_cards = "".join(card(a, i % 3 + 1) for i, a in enumerate(top))
    counts = {k: sum(1 for a in ARTICLES if a["category"] == k) for k in CATS}
    tiles = []
    for i, k in enumerate(CAT_ORDER):
        c = CATS[k]
        wide = " wide" if i < 2 else ""
        tiles.append(f"""<a class="cat-tile{wide} reveal d{i % 3 + 1}" href="/{c['slug']}/">{img(c['image'], c['name'] + ' — ' + c['blurb'], sizes='(max-width: 900px) 100vw, 50vw')}
  <span class="count">{counts[k]} guides</span><div><h3>{c['name']}</h3><p>{c['blurb']}</p></div></a>""")
    piercings = [("Lobe", "double-lobe-piercing-earrings", 2, 15, "6–8 weeks"),
                 ("Helix", "helix-earrings", 5, 70, "6–12 months"),
                 ("Forward helix", "triple-forward-helix-earrings", 6, 75, "6–12 months"),
                 ("Tragus", "tragus-piercing-earrings", 5, 65, "6–12 months"),
                 ("Rook", "rook-earrings", 7, 85, "6–12 months"),
                 ("Cartilage", "cute-cartilage-earrings", 5, 70, "6–12 months"),
                 ("Dermal", "dermal-earring", 5, 45, "1–3 months+"),
                 ("Behind the ear", "behind-the-ear-earrings", 1, 5, "No piercing needed")]
    pcards = "".join(f"""<a class="pierce reveal d{i % 3 + 1}" href="/{s}/"><h3>{n}</h3>
  <div class="meter"><span>Pain: {p}/10</span><div class="bar"><i data-w="{p * 10}"></i></div></div>
  <div class="meter heal"><span>Healing: {t}</span><div class="bar"><i data-w="{h}"></i></div></div></a>""" for i, (n, s, p, h, t) in enumerate(piercings))
    pop = pick(["janet-jackson-key-earring", "harry-styles-earring", "potara-earrings", "jhumka-earrings"])
    pop_cards = "".join(card(a, i % 3 + 1) for i, a in enumerate(pop))
    faq = [("What is Come i Cavoli a Merenda?", "An independent guide to earrings and ear piercings: actual-size charts, gauge conversions, piercing placement guides and the stories behind famous earrings."),
           ("What does “come i cavoli a merenda” mean?", "It is an Italian saying, literally “like cabbages at snack time.” Italians use it for two things that don’t go together. We think mismatched earrings go together beautifully."),
           ("How big is a 5mm earring?", "A 5mm stud is about 0.2 inches across, a little smaller than a pencil eraser. It reads as a noticeable but still everyday stud."),
           ("What gauge are regular earrings?", "Most standard lobe earrings are 20 gauge (0.8mm) or 18 gauge (1.0mm). Cartilage jewelry is usually 16 gauge (1.2mm).")]
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    schema = [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    words = ["studs", "huggies", "helix", "hoops", "rook", "jhumkas", "tragus", "ear cuffs", "threaders", "drops", "conch", "climbers"]
    marquee = "".join(f"<span>{w}</span>" for w in words * 2)
    body = f"""<section class="hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>
  <div class="sparkles" data-n="26" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">The earring &amp; piercing guide</span>
      <h1>Earrings that go together like <span class="shimmer"><em>cabbages at snack time.</em></span></h1>
      <p class="lead">Actual-size charts, gauge conversions, piercing guides and the stories behind the world’s most-searched earrings, for ears that don’t have to match.</p>
      <div class="hero-actions"><a class="btn btn-gold" href="/earring-size-tool/">Try the size tool</a><a class="btn btn-ghost" href="/earring-guides/">Browse the guides</a></div>
    </div>
    <div class="collage" aria-hidden="false">
      <figure class="c1">{img('ear-stack', 'Ear with a curated stack of small studs and a thin gold hoop', sizes='(max-width: 900px) 60vw, 330px', eager=True)}</figure>
      <figure class="c2">{img('sapphire-drops', 'Blue stone and crystal drop earrings resting on a green leaf', sizes='(max-width: 900px) 46vw, 260px', eager=True)}</figure>
      <figure class="c3">{img('twist-hoops', 'Twisted gold hoop earrings on white pebbles', sizes='(max-width: 900px) 44vw, 250px')}</figure>
      <div class="badge-float"><b>{len(ARTICLES)}</b> in-depth guides</div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Most read</span><h2>The questions everyone asks</h2></div><p>Our most-visited guides: the sizes, gauges and piercings people look up before they buy or book.</p></div>
  <div class="cards">{top_cards}</div>
</div></section>

<section class="section cream"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">Interactive</span>
    <h2>How big is 5mm, really?</h2>
    <p>Product photos are zoomed in, and “5mm” means nothing until it is on your ear. Slide to any stud size and see it next to a US penny. Calibrate it with a bank card in the <a href="/earring-size-tool/">full Size Tool</a> and it becomes true actual size on your screen.</p>
    <p><a class="btn btn-dark" href="/5mm-earrings-actual-size/">Read the stud size guide</a></p>
  </div>
  <div class="reveal d2">{sizer_widget(5, compact=True)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Explore</span><h2>Find your rabbit hole</h2></div><p>Five collections, one obsession. Pick a door.</p></div>
  <div class="cat-grid">{''.join(tiles)}</div>
</div></section>

<section class="section dark" style="position:relative;overflow:hidden;isolation:isolate">
  <div class="blob b1" aria-hidden="true" style="opacity:.25"></div>
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow" style="color:var(--gold-2)">Piercing at a glance</span><h2>Pain vs healing, side by side</h2></div><p>Typical ranges reported by piercers and people who have been there. Everyone heals differently; tap a card for the full guide.</p></div>
    <div class="pierce-grid">{pcards}</div>
  </div>
</section>

<section class="section cream"><div class="wrap split rev">
  <div class="split-media reveal"><span class="ring" aria-hidden="true"></span>{img('portrait-gold', 'Woman in profile wearing a chunky gold earring and gold chain', sizes='(max-width: 860px) 100vw, 560px')}</div>
  <div class="reveal d2">
    <span class="eyebrow">About the name</span>
    <h2>Why “like cabbages at snack time”?</h2>
    <blockquote class="idiom">“Come i cavoli a merenda.”<small>Italian saying, literally “like cabbages at an afternoon snack”: said of things that don’t belong together.</small></blockquote>
    <p>Italians say it about anything that seems out of place. We borrowed it because the best ears break that rule: a pearl next to a spike, a gold hoop with a silver huggie, three different studs climbing a helix.</p>
    <p>This site is our love letter to that kind of mismatch, backed by the boring-but-important details: sizes, gauges, metals and aftercare.</p>
    <p><a class="btn btn-dark" href="/about/">More about us</a></p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Famous earrings</span><h2>Icons, characters &amp; traditions</h2></div><p>From Janet Jackson’s key to Dragon Ball’s Potara fusion earrings: the backstory, and how to get the look.</p></div>
  <div class="cards four">{pop_cards}</div>
</div></section>

<section class="section tight cream"><div class="wrap">
  <div class="stats reveal"><div><b>{len(ARTICLES)}</b><span>in-depth guides</span></div><div><b>19</b><span>gauge sizes converted</span></div><div><b>2–14mm</b><span>stud sizes to scale</span></div><div><b>0</b><span>sponsored posts</span></div></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="split" style="align-items:start">
    <div class="reveal"><span class="eyebrow">FAQ</span><h2>Good to know</h2><p>Short answers to the things readers ask us most.</p></div>
    <div class="faq reveal d2" style="margin:0">{faq_html}</div>
  </div>
</div></section>

<section class="section tight"><div class="wrap">
  <div class="cta-band reveal"><div class="blob b2" aria-hidden="true"></div>
    <div><h2>Got an earring question we haven’t answered?</h2><p>Tell us what you’re trying to figure out: a size, a piercing, an earring you saw once and can’t stop thinking about. The best questions become guides.</p></div>
    <div><a class="btn btn-gold" href="/contact/">Ask us</a> <a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
</div></section>"""
    return page("/", f"{NAME}: Earring Sizes, Piercings & Style Guide",
                "Actual-size earring charts, gauge conversions, ear piercing guides and the stories behind famous earrings. An independent guide for beautifully mismatched ears.",
                body, schema, active="/", og_image="ear-stack")


def tool_page():
    schema = [breadcrumb_schema([("Home", "/"), ("Earring Size Tool", "/earring-size-tool/")]),
              {"@type": "WebApplication", "name": "Earring Size Tool", "url": SITE + "/earring-size-tool/",
               "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    rows = "".join(f"<tr><td>{mm} mm</td><td>{mm / 25.4:.3f} in</td><td>{c}</td></tr>" for mm, c in [
        (2, "A pinhead; ultra-minimal second-hole stud"), (3, "Tiny sparkle, great for cartilage"), (4, "Classic small stud, kid-friendly"),
        (5, "Everyday stud, slightly smaller than a pencil eraser"), (6, "About a pencil eraser; noticeable"), (7, "A pea; reads as a statement for small lobes"),
        (8, "A chickpea; bold everyday stud"), (10, "Statement stud or small button earring"), (12, "Button earring; covers most of a small lobe")])
    body = f"""<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>
  <div class="sparkles" data-n="18" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Earring Size Tool</nav>
    <h1>Earring Size Tool: See Studs &amp; Gauges at Actual Size</h1>
    <p>Calibrate your screen with a bank card, then preview any stud size from 2mm to 14mm at true scale, and convert ear gauges to millimeters and inches.</p>
  </div>
</section>
<section class="section tight"><div class="wrap split" style="align-items:start">
  <div class="reveal">{sizer_widget(5)}</div>
  <div class="reveal d2 prose">
    <h2>How to use it</h2>
    <ol><li>Hold any standard bank, ID or gift card flat against your screen.</li><li>Drag the calibration slider until the dashed outline matches the card edges exactly.</li><li>Now slide through stud sizes. What you see is the real diameter of the earring face.</li></ol>
    <div class="callout"><p>Without calibration we use the standard CSS scale (96 px per inch), which is close on most laptops but can be off on phones and high-density displays.</p></div>
    <h2>Stud sizes at a glance</h2>
    <table class="tbl"><thead><tr><th>Size</th><th>Inches</th><th>Looks like</th></tr></thead><tbody>{rows}</tbody></table>
    <p>More detail in our <a href="/5mm-earrings-actual-size/">5mm earrings actual size</a> and <a href="/8mm-earrings-actual-size/">8mm earrings actual size</a> guides.</p>
  </div>
</div></section>
<section class="section cream"><div class="wrap split" style="align-items:start">
  <div class="reveal prose"><h2>Ear gauge converter</h2><p>Gauge numbers run backwards: the bigger the number, the thinner the post. Most lobe earrings are 20g or 18g; cartilage jewelry is usually 16g. Pick a size to see it in millimeters and inches.</p><p>Full chart and stretching advice: <a href="/ear-gauge-size-chart/">ear gauge size chart</a> · <a href="/what-gauge-are-regular-earrings/">what gauge are regular earrings?</a></p></div>
  <div class="reveal d2">{gauge_widget()}</div>
</div></section>"""
    return page("/earring-size-tool/", "Earring Size Tool: Actual Size Studs & Gauge Converter",
                "Preview earring stud sizes from 2mm to 14mm at true actual size on your screen, calibrated with a bank card, plus an ear gauge to mm and inch converter.",
                body, schema, active="/earring-size-tool/", og_image="diamond-studs")


def simple_page(path, title, desc, h1, lead, inner, crumbs_name, schema_type="WebPage", active=""):
    schema = [breadcrumb_schema([("Home", "/"), (crumbs_name, path)]),
              {"@type": schema_type, "name": h1, "url": SITE + path, "description": desc}]
    body = f"""<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div>
  <div class="sparkles" data-n="12" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>{esc(crumbs_name)}</nav>
    <h1>{esc(h1)}</h1>
    <p>{lead}</p>
  </div>
</section>
<section class="page-body"><div class="wrap">{inner}</div></section>"""
    return page(path, title, desc, body, schema, active=active)


def about_page():
    inner = f"""<div class="split" style="align-items:start">
  <div class="prose reveal">
    <h2>An earring guide for real ears</h2>
    <p>Come i Cavoli a Merenda is an independent guide to earrings and ear piercings. We answer the questions that come up right before you buy or book: how big a 5mm stud really is, what gauge your earrings are, how long a rook takes to heal, and why your earring backs smell.</p>
    <p>We also love the stories behind famous earrings, from Janet Jackson’s key to the Potara fusion earrings of Dragon Ball, because jewelry is never just metal.</p>
    <h2>The name</h2>
    <p><em>Come i cavoli a merenda</em> is an Italian saying: “like cabbages at snack time.” It describes things that don’t belong together. We think the most interesting ears are exactly that: mismatched, curated, a little unexpected.</p>
    <h2>How we write</h2>
    <ul><li><strong>Independent.</strong> No brand pays to appear here, and we are not affiliated with any brand we mention.</li><li><strong>Practical.</strong> Sizes in millimeters and inches, typical healing ranges, materials that are kind to skin.</li><li><strong>Careful.</strong> Piercing content is general information, not medical advice. Book with a reputable professional piercer and see a doctor about signs of infection.</li></ul>
    <h2>Get in touch</h2>
    <p>Questions, corrections or ideas for a guide: <a href="mailto:{EMAIL}">{EMAIL}</a> or use the <a href="/contact/">contact form</a>.</p>
  </div>
  <div class="split-media reveal d2"><span class="ring" aria-hidden="true"></span>{img('hoops-book', 'Chunky gold double hoop earrings resting on an open book', sizes='(max-width: 860px) 100vw, 560px')}</div>
</div>"""
    return simple_page("/about/", f"About {NAME}", "Come i Cavoli a Merenda is an independent earring and ear-piercing guide. Learn what the Italian name means and how we write our guides.",
                       "About Come i Cavoli a Merenda", "An independent guide for beautifully mismatched ears.", inner, "About", "AboutPage", active="/about/")


def contact_page():
    inner = f"""<div class="contact-grid">
  <div class="prose reveal">
    <h2>Say ciao</h2>
    <p>Have an earring question, spotted something we should correct, or want to suggest a guide? We read everything.</p>
    <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="callout"><p>We can’t give medical advice. If a piercing is hot, swollen, very painful or leaking yellow-green discharge, please see a doctor or your piercer.</p></div>
    <p>We usually reply within a few days.</p>
  </div>
  <form class="form reveal d2" action="/contact.php" method="post">
    <div id="form-status" aria-live="polite"></div>
    <label>Your name<input name="name" autocomplete="name" required maxlength="100"></label>
    <label>Email<input type="email" name="email" autocomplete="email" required maxlength="200"></label>
    <label>Topic<select name="topic"><option>Earring question</option><option>Guide suggestion</option><option>Correction</option><option>Something else</option></select></label>
    <label>Message<textarea name="message" rows="6" required maxlength="5000"></textarea></label>
    <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
    <button class="btn btn-gold" type="submit">Send message</button>
  </form>
</div>
<script>
(function(){{var p=new URLSearchParams(location.search),s=document.getElementById('form-status');
if(p.get('sent')==='1')s.innerHTML='<div class="alert ok">Thanks! Your message is on its way.</div>';
else if(p.get('sent')==='0')s.innerHTML='<div class="alert err">Sorry, that didn\\'t send. Please email {EMAIL} directly.</div>';}})();
</script>"""
    return simple_page("/contact/", f"Contact {NAME}", f"Contact Come i Cavoli a Merenda with earring questions, corrections or guide ideas. Email {EMAIL} or use our contact form.",
                       "Contact us", "Questions, corrections and guide ideas are all welcome.", inner, "Contact", "ContactPage")


def legal_page(kind):
    if kind == "privacy":
        inner = f"""<div class="prose">
<p><em>Last updated {TODAY.strftime('%B %-d, %Y')}</em></p>
<h2>Who we are</h2><p>{NAME} ({SITE.replace('https://', '')}) is an independent informational website about earrings and ear piercings. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What we collect</h2><p>We do not require accounts. If you use the contact form or email us, we receive the name, email address and message you send, and use them only to reply. Our host keeps standard server logs (IP address, browser, pages requested, time) for security and troubleshooting.</p>
<h2>Cookies and local storage</h2><p>We don’t set advertising or tracking cookies. The Earring Size Tool saves your screen calibration in your browser’s local storage so you don’t have to repeat it; it never leaves your device. Fonts are loaded from Google Fonts, which receives your IP address as part of delivering them.</p>
<h2>Sharing</h2><p>We don’t sell or rent personal information. We share it only if required by law.</p>
<h2>Retention</h2><p>Messages are kept only as long as needed to handle your request.</p>
<h2>Your choices</h2><p>You can ask us to access or delete any message you sent by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Children</h2><p>This site is intended for a general audience and does not knowingly collect information from children under 13.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest version.</p></div>"""
        return simple_page("/privacy-policy/", f"Privacy Policy | {NAME}", "How Come i Cavoli a Merenda handles contact form messages, server logs and the local storage used by our Earring Size Tool.",
                           "Privacy Policy", "Short version: we collect very little, and we never sell it.", inner, "Privacy Policy")
    inner = f"""<div class="prose">
<p><em>Last updated {TODAY.strftime('%B %-d, %Y')}</em></p>
<h2>Information only</h2><p>Content on {NAME} is general information about jewelry and piercing. It is not medical advice. Consult a qualified professional piercer or a doctor about your own situation.</p>
<h2>Accuracy</h2><p>We work to keep sizes, conversions and facts accurate, but we make no warranty that everything is complete or current. The Earring Size Tool is an approximation that depends on your screen and calibration.</p>
<h2>Trademarks</h2><p>Brand, character and product names belong to their owners. We are independent and not affiliated with, sponsored or endorsed by any brand, studio or person mentioned.</p>
<h2>Copyright</h2><p>Text and design are &copy; {NAME}. You may quote short excerpts with a link back. Please don’t republish whole articles.</p>
<h2>Links</h2><p>We are not responsible for the content of websites we link to.</p>
<h2>Liability</h2><p>To the extent permitted by law, we are not liable for any loss arising from use of this site.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>"""
    return simple_page("/terms-of-use/", f"Terms of Use | {NAME}", "The terms for using Come i Cavoli a Merenda: informational content only, not medical advice, independent of all brands mentioned.",
                       "Terms of Use", "The fine print, kept short.", inner, "Terms of Use")


def sitemap_page():
    secs = []
    for k in CAT_ORDER:
        c = CATS[k]
        lis = "".join(f'<li><a href="{a["url"]}">{esc(a["h1"])}</a></li>' for a in ARTICLES if a["category"] == k)
        secs.append(f'<section><h2><a href="/{c["slug"]}/">{c["name"]}</a></h2><ul>{lis}</ul></section>')
    secs.append('<section><h2>Site</h2><ul><li><a href="/">Home</a></li><li><a href="/earring-size-tool/">Earring Size Tool</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li></ul></section>')
    inner = f'<div class="prose sitemap-cols" style="max-width:none">{"".join(secs)}</div>'
    return simple_page("/sitemap/", f"Sitemap | {NAME}", "Every guide on Come i Cavoli a Merenda in one place: earring sizes, gauges, piercings, celebrity earrings, pop culture and styles.",
                       "Sitemap", "Every page on the site, in one place.", inner, "Sitemap")


def notfound_page():
    body = """<section class="notfound"><div class="wrap">
  <span class="gem" aria-hidden="true"></span>
  <h1>This earring rolled under the dresser.</h1>
  <p>The page you’re looking for isn’t here. Try one of these instead:</p>
  <p><a class="btn btn-dark" href="/">Home</a> <a class="btn btn-gold" href="/earring-size-tool/">Size Tool</a> <a class="btn btn-dark" href="/sitemap/">Sitemap</a></p>
</div></section>"""
    return page("/404.html", f"Page not found | {NAME}", "This page could not be found.", body, robots="noindex, follow")


# --------------------------------------------------------------------------- redirects
RULES = [
    (r"aldean", "jason-aldean-earrings"), (r"barry-bonds", "barry-bonds-earring"),
    (r"janet-jackson", "janet-jackson-key-earring"), (r"harry-styles", "harry-styles-earring"),
    (r"bowie", "david-bowie-earrings"), (r"harrison-ford", "harrison-ford-earring"),
    (r"felicity|smoak|arrow-ear", "felicity-smoak-earrings"), (r"kylie", "kylie-jenner-ear-piercings"),
    (r"mr-clean", "why-does-mr-clean-have-an-earring"), (r"fairy-tail|erza", "fairy-tail-earrings"),
    (r"skyrim", "skyrim-earrings"), (r"potara|fusion|dbz|dragon-ball|goku|vegeta", "potara-earrings"),
    (r"dirigible|lovegood|radish", "dirigible-plum-earrings"), (r"eevee|pokemon|pikachu", "eevee-earrings"),
    (r"coach", "coach-earrings"), (r"nike", "nike-earrings"), (r"chanel", "chanel-earrings"),
    (r"(^|-)80s|eighties", "80s-earrings"), (r"jhumk", "jhumka-earrings"), (r"ebay", "ebay-earrings"),
    (r"jordan", "jordan-earrings-for-guys"), (r"cross-earring|dangling-cross|(^|-)cross-", "dangling-cross-earrings-for-mens"),
    (r"(^|-)(guys?|men|mens|boys?|male|man)(-|$)", "guys-with-earrings"),
    (r"forward-helix|triple-helix", "triple-forward-helix-earrings"), (r"helix", "helix-earrings"),
    (r"(^|-)rook", "rook-earrings"), (r"tragus", "tragus-piercing-earrings"), (r"dermal", "dermal-earring"),
    (r"double-lobe|second-hole|double-piercing|third-hole|double-ear|multiple-ear|second-piercing", "double-lobe-piercing-earrings"),
    (r"behind-the-ear|ear-jacket|front-back|front-and-back", "behind-the-ear-earrings"),
    (r"cartilage|conch|daith|industrial", "cute-cartilage-earrings"),
    (r"gauge-size-chart|stretch|size-chart|plug|tunnel|look-like-gauges", "ear-gauge-size-chart"),
    (r"gauge", "what-gauge-are-regular-earrings"),
    (r"(^|-)(8|9|10|11|12)-?mm", "8mm-earrings-actual-size"), (r"(^|-)\d+(-\d+)?-?mm", "5mm-earrings-actual-size"),
    (r"actual-size", "5mm-earrings-actual-size"), (r"smell", "why-do-my-earrings-smell"),
    (r"earring-back|(^|-)backs?(-|$)|closure|backless|screw-back|lever-back", "types-of-earring-backs"),
    (r"holder|organi[sz]er|jewelry-stand|earring-stand|earring-tree|jewelry-box|storage", "earring-holder-target"),
    (r"self-piercing", "self-piercing-earrings"), (r"spanish", "earrings-in-spanish"),
    (r"clip-on|clip-earring|kids|toddler|little-girl|baby", "kids-clip-on-earrings"),
    (r"types-of-earring|earring-types|kinds-of-earring|earring-styles|styles-of-earring", "earring-types"),
    (r"piercing", "/piercings/"),
    (r"diamond.*stud|stud.*diamond|carat", "5mm-earrings-actual-size"),
    (r"itsy-bitsy|american-girl", "kids-clip-on-earrings"),
    (r"taeyang|bigbang", "guys-with-earrings"),
    (r"tumblr|bluetooth|image-unavailable", "earring-types"),
    (r"pacman|perler", "/pop-culture-earrings/"), (r"lil-jojo", "/celebrity-earrings/"),
    (r"walmart|zales|tiffany|silpada|kendra-scott|victoria-lynn|diamonds-in-rhythm|luxurman|amber|swarovski|michael-hill", "/earring-styles/"),
]


def target_for(path):
    p = path.lower()
    if p.endswith(".pdf"):
        return "GONE"
    if re.match(r"^/(19|20)\d\d/\d\d/", p) or p.startswith(("/search/label", "/feeds/", "/search?")):
        return "/"  # old Blogger-era food blog posts: send their links to the homepage
    name = p.strip("/")
    name = re.sub(r"-[0-9a-f]{16}\.html$", "", name)
    name = re.sub(r"\.html?$", "", name)
    for rx, slug in RULES:
        if re.search(rx, name):
            return slug if slug.startswith("/") else f"/{slug}/"
    return None


def read_tsv(name):
    with open(os.path.join(ROOT, "data", name)) as f:
        next(f)
        return [line.rstrip("\n").split("\t") for line in f if line.strip()]


def build_redirects():
    live = {a["url"] for a in ARTICLES} | {f"/{c['slug']}/" for c in CATS.values()} | {"/"}
    red, gone, unmatched = {}, [], []
    paths = [r[0] for r in read_tsv("old-organic-urls.tsv")] + [r[0] for r in read_tsv("backlink-targets.tsv")]
    for p in paths:
        clean = p.split("?")[0]
        if clean in live or clean == "/" or clean in red:
            continue
        t = target_for(clean)
        if t == "GONE":
            gone.append(clean)
        elif t:
            assert t in live, (clean, t)
            red[clean] = t
        else:
            unmatched.append(clean)
    return red, sorted(set(gone)), unmatched


def php_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def write_php(red, gone):
    with open(os.path.join(DIST, "redirects.php"), "w") as f:
        f.write("<?php\n// Generated by build.py: old comeicavoliamerenda.com URLs -> new pages. Do not edit.\n")
        f.write("return [\n" + "".join(f"{php_str(k)}=>{php_str(v)},\n" for k, v in sorted(red.items())) + "];\n")
    with open(os.path.join(DIST, "gone.php"), "w") as f:
        f.write("<?php\n// Generated by build.py: old spam PDF URLs answered with 410 Gone.\n")
        f.write("return [\n" + "".join(f"{php_str(k)}=>1,\n" for k in gone) + "];\n")
    shutil.copy(os.path.join(ROOT, "php", "index.php"), os.path.join(DIST, "index.php"))
    shutil.copy(os.path.join(ROOT, "php", "contact.php"), os.path.join(DIST, "contact.php"))


# --------------------------------------------------------------------------- write
def write(path, content):
    if path == "/":
        out = os.path.join(DIST, "home.html")
    elif path.endswith(".html"):
        out = os.path.join(DIST, path.lstrip("/"))
    else:
        out = os.path.join(DIST, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(content)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), DIST)

    urls = ["/"]
    write("/", home_page())
    for k in CAT_ORDER:
        write(f"/{CATS[k]['slug']}/", hub_page(k)); urls.append(f"/{CATS[k]['slug']}/")
    for a in ARTICLES:
        write(a["url"], article_page(a)); urls.append(a["url"])
    write("/earring-size-tool/", tool_page()); urls.append("/earring-size-tool/")
    write("/about/", about_page()); urls.append("/about/")
    write("/contact/", contact_page()); urls.append("/contact/")
    write("/privacy-policy/", legal_page("privacy")); urls.append("/privacy-policy/")
    write("/terms-of-use/", legal_page("terms")); urls.append("/terms-of-use/")
    write("/sitemap/", sitemap_page()); urls.append("/sitemap/")
    write("/404.html", notfound_page())

    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            pr = "1.0" if u == "/" else "0.8" if u in {a["url"] for a in ARTICLES} or u.count("/") == 2 and u[1:-1] in [c["slug"] for c in CATS.values()] else "0.5"
            f.write(f"  <url><loc>{SITE}{u}</loc><lastmod>{PUBLISHED}</lastmod><priority>{pr}</priority></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {SITE}/sitemap.xml\n")

    red, gone, unmatched = build_redirects()
    write_php(red, gone)
    with open(os.path.join(ROOT, "data", "redirect-report.tsv"), "w") as f:
        f.write("old_path\taction\n")
        for k, v in sorted(red.items()):
            f.write(f"{k}\t301 {v}\n")
        for k in gone:
            f.write(f"{k}\t410\n")
        for k in sorted(unmatched):
            f.write(f"{k}\t404\n")
    print(f"pages={len(urls)} articles={len(ARTICLES)} redirects={len(red)} gone={len(gone)} unmatched(404)={len(unmatched)}")


if __name__ == "__main__":
    main()
