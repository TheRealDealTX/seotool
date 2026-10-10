#!/usr/bin/env python3
"""Build the asmith.photography static site into public/.

    python3 build.py && python3 validate.py

Content lives in content/ (plan.json, pages/*.json, credits.json). Output is
plain HTML served by public/index.php, which maps the original extensionless
URLs (/nike-sb, /contact ...) to public/pages/<slug>.html.
"""
import hashlib, html, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUB = ROOT / "public"
SITE = "https://asmith.photography"
NAME = "asmith.photography"
EMAIL = "info@asmith.photography"
TAGLINE = "Los Angeles Photography Journal"
PUBLISHED = "2026-10-10"

plan = json.loads((ROOT / "content/plan.json").read_text())
CATS = plan["categories"]
REDIRECTS = plan["redirects"]
CREDITS = json.loads((ROOT / "content/credits.json").read_text())
PAGES = []
for slug, cat, kw, _angle in plan["pages"]:
    p = json.loads((ROOT / f"content/pages/{slug}.json").read_text())
    p["cat"], p["kw"] = cat, kw
    p["words"] = sum(len(x.split()) for s in p["sections"] for x in s["paras"])
    PAGES.append(p)
BY_SLUG = {p["slug"]: p for p in PAGES}
for i, p in enumerate(PAGES):
    p["frame"] = f"{i + 1:02d}A"

e = lambda s: html.escape(str(s), quote=True)


def asset_v(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


CSS_V, JS_V = asset_v("src/site.css"), asset_v("src/site.js")
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'


def img_tag(key, alt, cls="", eager=False, sizes="100vw"):
    return (f'<img src="/assets/img/{key}.webp" srcset="/assets/img/{key}-sm.webp 800w, /assets/img/{key}.webp 1600w" '
            f'sizes="{sizes}" alt="{e(alt)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} '
            f'{"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async" width="1600" height="1067">')


def credit_line(key):
    c = CREDITS.get(key)
    if not c:
        return ""
    lic = {"cc0": "CC0", "pdm": "Public Domain Mark", "by": "CC BY"}.get(c["license"], c["license"].upper())
    if c.get("license_version") and c["license"] not in ("cc0", "pdm"):
        lic += " " + c["license_version"]
    who = f'<a href="{e(c["creator_url"])}" rel="nofollow noopener">{e(c["creator"])}</a>' if c.get("creator_url") else e(c["creator"])
    title = f'<a href="{e(c["landing"])}" rel="nofollow noopener">{e(c["title"])}</a>' if c.get("landing") else e(c["title"])
    licl = f'<a href="{e(c["license_url"])}" rel="nofollow noopener">{lic}</a>' if c.get("license_url") else lic
    return f'Photo: {title} by {who}, {licl}. Illustrative image; not from the shoot described.'


NAV = [("/journal", "Journal"), ("/journal#skate", "Skate"), ("/journal#footwear", "Footwear"),
       ("/journal#editorial", "Editorial"), ("/journal#sport", "Sport"), ("/about", "About")]


def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header"><div class="wrap">
<a class="logo" href="/" aria-label="{NAME} home"><i aria-hidden="true"></i>asmith<em>.photography</em></a>
<button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav class="nav" id="nav" aria-label="Main">{links}<a class="cta" href="/contact"{" aria-current=\"page\"" if current == "/contact" else ""}>Contact</a></nav>
</div></header>'''


def footer():
    cats = "".join(f'<li><a href="/journal#{k}">{e(v)}</a></li>' for k, v in CATS.items())
    picks = "".join(f'<li><a href="/{s}">{t}</a></li>' for s, t in [
        ("nike-sb", "Nike SB photography"), ("johnny-layton-for-vans", "Vans skate shoe shoots"),
        ("stacy-adams-shoes", "Stacy Adams shoes"), ("skateboarding", "Skateboard photography"),
        ("ucla-water-polo", "UCLA water polo")])
    return f'''<footer class="site-footer"><div class="wrap">
<p class="foot-big" aria-hidden="true">asmith<b>.</b>photo</p>
<div class="foot-cols">
<div><h2>About this journal</h2><p>Stories on how commercial, editorial, skate and sport photography gets made in Los Angeles.</p><p style="margin-top:14px"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h2>Sections</h2><ul>{cats}</ul></div>
<div><h2>Most read</h2><ul>{picks}</ul></div>
<div><h2>Site</h2><ul><li><a href="/journal">All stories</a></li><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div>
<div class="foot-base"><span>&copy; <span data-year>2026</span> {NAME}</span></div>
</div></footer>'''


ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
       "email": EMAIL, "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-512.png"},
       "contactPoint": {"@type": "ContactPoint", "contactType": "editorial", "email": EMAIL}}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "name": NAME, "url": SITE + "/",
           "description": "An independent Los Angeles photography journal: skate, footwear, editorial, sport and personal work.",
           "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}


def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}


def page(path, title, desc, body, current="", image="home-hero", ld=None, og_type="website", extra_head="", iris=False):
    url = SITE + ("/" if path == "/" else path)
    graph = [ORG, WEBSITE] + (ld or [])
    full_title = title if NAME in title or len(title) + len(NAME) + 3 > 66 else f"{title} | {NAME}"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0c0b0a">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{image}.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/{image}.webp">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={CSS_V}">
{extra_head}<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
{'<div class="iris" aria-hidden="true"><span>LOADING FILM</span></div>' if iris else ''}<div class="grain" aria-hidden="true"></div>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
'''


def card(p, cls="", sizes="(max-width: 620px) 100vw, (max-width: 960px) 50vw, 33vw"):
    text = e(" ".join([p["h1"], p["dek"], p["kw"], CATS[p["cat"]]]).lower())
    return f'''<a class="card {cls} develop" href="/{p["slug"]}" data-cat="{p["cat"]}" data-text="{text}">
<div class="frame" data-frame="&#9656; {p["frame"]}">{img_tag(p["slug"], p["h1"], sizes=sizes)}</div>
<span class="tag">{e(CATS[p["cat"]])} &middot; {max(1, round(p["words"] / 230))} min</span>
<h3><span>{e(p["h1"])}</span></h3>
<p>{e(p["dek"])}</p></a>'''


# ---------------------------------------------------------------- home
def build_home():
    feat = ["nike-sb", "johnny-layton-for-vans", "skateboarding", "stacy-adams-shoes", "ucla-water-polo",
            "florsheim-shoes", "bello-magazine-december-cover-story"]
    layout = ["wide", "", "", "", "", "half", "half"]
    cards = "".join(card(BY_SLUG[s], c, "(max-width: 960px) 100vw, 66vw" if c == "wide" else
                         "(max-width: 620px) 100vw, 50vw") for s, c in zip(feat, layout))
    more = [p for p in PAGES if p["slug"] not in feat][:6]
    more_cards = "".join(card(p) for p in more)
    counts = {k: sum(1 for p in PAGES if p["cat"] == k) for k in CATS}
    blurbs = {"skate": "Fisheyes, flashes, ledges and the culture of skate print.",
              "footwear": "Leather, suede and canvas: lighting shoes on foot and on set.",
              "editorial": "Magazine portraits, cover stories and indie print.",
              "sport": "Pools, diamonds, velodromes and Friday night lights.",
              "campaign": "Brand shoots from surf to eyewear to instant cameras.",
              "personal": "Road trips, weekly projects and documentary work."}
    cats = "".join(f'<a class="cat reveal" href="/journal#{k}"><span class="n">0{i + 1} / {counts[k]:02d} stories</span>'
                   f'<strong>{e(v)}</strong><span class="c">{blurbs[k]}</span></a>' for i, (k, v) in enumerate(CATS.items()))
    strip_items = "".join(f'<a href="/journal#{k}">{e(v)}</a>' for k, v in CATS.items())
    statement = ("A field journal for people who make pictures in Los Angeles. How skate, footwear, "
                 "fashion and sport photography actually gets made: the light, the lenses, the spots and the "
                 "decisions behind every frame.")
    st = " ".join(f'<span class="dim">{e(w)}</span>' for w in statement.split())
    body = f'''<section class="hero" aria-label="Introduction">
<div class="hero-media">{img_tag("home-hero", "Los Angeles street at night", eager=True)}</div>
<div class="leak" aria-hidden="true"></div>
<div class="viewfinder" aria-hidden="true"><b></b><b></b><b></b><b></b><div class="focus"></div>
<div class="hud"><span class="rec">REC</span><span class="hide-sm">ISO 400 &nbsp; 1/250 &nbsp; f/2.8</span><span data-counter>01/36</span></div></div>
<div class="hero-copy">
<span class="eyebrow">{TAGLINE}</span>
<h1 class="split">Light, motion &amp; the streets of <em>Los Angeles.</em></h1>
<p class="lede">Stories on skate, footwear, editorial and sport photography: how the pictures are planned, lit and shot, from Venice ledges to the velodrome in Carson.</p>
<p><a class="btn" href="/journal">Read the journal {ARROW}</a> &nbsp; <a class="btn ghost" href="#lab">Try the exposure lab</a></p>
</div>
<div class="scroll-cue" aria-hidden="true">SCROLL</div>
</section>
<div class="strip" aria-label="Sections"><div class="strip-track">{strip_items}{strip_items.replace("<a ", "<a tabindex=\"-1\" aria-hidden=\"true\" ")}</div></div>
<section class="section"><div class="wrap"><p class="statement">{st}</p></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="section-head reveal"><div><span class="eyebrow">Featured</span><h2>From the contact sheet</h2></div>
<p>Start with the stories readers come back to most: skate footwear, shoe still life and pool-deck sport.</p></div>
<div class="grid">{cards}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="section-head reveal"><div><span class="eyebrow">Sections</span><h2>Six ways in</h2></div></div>
<div class="cats">{cats}</div></div></section>
<section class="section" id="lab" style="background:var(--ink-2)"><div class="wrap">
<div class="section-head reveal"><div><span class="eyebrow">Interactive</span><h2>The exposure lab</h2></div>
<p>Every story here comes back to three dials. Move them and watch the frame: brightness, motion, depth and grain.</p></div>
<div class="lab reveal">
<div class="lab-view">{img_tag("home-skate", "Skateboarder rolling through a city street", sizes="(max-width: 860px) 100vw, 60vw")}<div class="noise"></div>
<div class="readout"><span id="apv">f/4</span><span class="meter" aria-hidden="true"></span><span id="shv">1/250</span><span id="isov">ISO 400</span></div></div>
<div class="lab-controls">
<label><span class="row">Aperture <output>wider &larr; &rarr; deeper</output></span><input id="ap" type="range" min="0" max="7" value="3" aria-label="Aperture"></label>
<label><span class="row">Shutter <output>slower &larr; &rarr; faster</output></span><input id="sh" type="range" min="0" max="7" value="3" aria-label="Shutter speed"></label>
<label><span class="row">ISO <output>cleaner &larr; &rarr; brighter</output></span><input id="iso" type="range" min="0" max="6" value="2" aria-label="ISO"></label>
<p class="lab-note" aria-live="polite"></p>
</div></div></div></section>
<section class="section"><div class="wrap">
<div class="section-head reveal"><div><span class="eyebrow">More stories</span><h2>Keep reading</h2></div>
<p><a class="btn ghost" href="/journal">All {len(PAGES)} stories {ARROW}</a></p></div>
<div class="grid">{more_cards}</div></div></section>'''
    ld = [{"@type": "CollectionPage", "@id": SITE + "/#page", "url": SITE + "/", "name": f"{NAME} — {TAGLINE}",
           "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{s}"} for i, s in enumerate(feat)]}}]
    return page("/", f"{NAME} — {TAGLINE}",
                "An independent Los Angeles photography journal: how skate, footwear, editorial and sport photography is planned, lit and shot, with an interactive exposure lab.",
                body, current="/", ld=ld, iris=True)


# ---------------------------------------------------------------- article
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def build_article(p):
    secs, toc = [], []
    for i, s in enumerate(p["sections"]):
        sid = slugify(s["h2"])[:48]
        toc.append(f'<a href="#{sid}">{e(s["h2"])}</a>')
        paras = "".join(f"<p>{e(x)}</p>" for x in s["paras"])
        secs.append(f'<h2 id="{sid}">{e(s["h2"])}</h2>{paras}')
        if i == 1 and p.get("pull_quote"):
            secs.append(f'<blockquote class="pull">{e(p["pull_quote"])}</blockquote>')
    notes = "".join(f"<li>{e(n)}</li>" for n in p.get("notes", []))
    related = "".join(card(BY_SLUG[s]) for s in p.get("related", []) if s in BY_SLUG)
    mins = max(1, round(p["words"] / 230))
    cat = CATS[p["cat"]]
    body = f'''<article>
<header class="a-hero">
<div class="hero-media">{img_tag(p["slug"], p["h1"], eager=True)}</div>
<div class="hero-copy">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/journal">Journal</a><span>/</span><a href="/journal#{p["cat"]}">{e(cat)}</a></nav>
<h1>{e(p["h1"])}</h1>
<p class="dek">{e(p["dek"])}</p>
<div class="meta"><span>{e(cat)}</span><span>{mins} min read</span><span>Frame {p["frame"]}</span></div>
</div></header>
<div class="wrap article">
<div class="prose">{"".join(secs)}</div>
<aside class="aside"><div class="aside-inner">
<div class="toc-box"><p class="mono" style="color:var(--muted);margin:0 0 12px">In this story</p><nav class="toc" aria-label="Contents">{"".join(toc)}</nav></div>
{f'<div class="notes"><h2>{e(p.get("notes_title") or "Field notes")}</h2><ol>{notes}</ol></div>' if notes else ""}
<a class="btn ghost" href="/journal#{p["cat"]}">More {e(cat)} {ARROW}</a>
</div></aside>
</div>
</article>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="section-head reveal"><div><span class="eyebrow">Related</span><h2>Next on the reel</h2></div></div>
<div class="grid">{related}</div></div></section>'''
    url = f"{SITE}/{p['slug']}"
    ld = [{"@type": "Article", "@id": url + "#article", "headline": p["h1"], "description": p["description"],
           "image": [f"{SITE}/assets/img/{p['slug']}.webp"], "datePublished": PUBLISHED, "dateModified": PUBLISHED,
           "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"},
           "mainEntityOfPage": url, "articleSection": cat, "keywords": p["kw"], "wordCount": p["words"],
           "inLanguage": "en-US"},
          crumbs_ld([("Home", "/"), ("Journal", "/journal"), (cat, f"/journal#{p['cat']}"), (p["h1"], "/" + p["slug"])])]
    head = f'<meta property="article:published_time" content="{PUBLISHED}">\n<meta property="article:section" content="{e(cat)}">\n'
    return page("/" + p["slug"], p["title"], p["description"], body, current="/journal", image=p["slug"], ld=ld,
                og_type="article", extra_head=head)


# ---------------------------------------------------------------- simple pages
def head_block(eyebrow, h1, lede):
    return f'''<section class="page-head"><div class="wrap"><span class="eyebrow">{e(eyebrow)}</span>
<h1 class="split">{h1}</h1><p class="reveal">{lede}</p></div></section>'''


def build_journal():
    chips = f'<button class="chip" data-filter="all" aria-pressed="true">All<sup>{len(PAGES)}</sup></button>' + "".join(
        f'<button class="chip" data-filter="{k}" aria-pressed="false">{e(v)}<sup>{sum(1 for p in PAGES if p["cat"] == k)}</sup></button>'
        for k, v in CATS.items())
    order = sorted(PAGES, key=lambda p: (list(CATS).index(p["cat"]), p["frame"]))
    body = head_block("The journal", "Every <em>story</em>", f"{len(PAGES)} stories on how photographs get made in Los Angeles. Filter by section or search for a subject, a lens or a location.") + f'''
<section style="padding-bottom:clamp(64px,9vw,120px)"><div class="wrap">
<div class="filters" role="toolbar" aria-label="Filter stories">{chips}
<div class="search"><label class="hp" for="q">Search stories</label><input id="q" type="search" placeholder="Search: fisheye, Venice, loafers…" autocomplete="off"></div></div>
<div class="grid journal-grid">{"".join(card(p) for p in order)}</div>
<p class="empty">Nothing on the reel matches that. Try another word.</p>
</div></section>'''
    ld = [{"@type": "CollectionPage", "url": SITE + "/journal", "name": "Journal", "isPartOf": {"@id": SITE + "/#website"},
           "mainEntity": {"@type": "ItemList", "numberOfItems": len(order), "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{p['slug']}"} for i, p in enumerate(order)]}},
          crumbs_ld([("Home", "/"), ("Journal", "/journal")])]
    return page("/journal", "The Journal: Skate, Footwear, Editorial & Sport",
                f"All {len(PAGES)} stories from the {NAME} journal: skate, footwear, editorial, sport, brand campaign and personal photography in Los Angeles.",
                body, current="/journal", image="journal", ld=ld)


def build_about():
    body = head_block("About", "A journal, <em>not</em> a portfolio", "Notes on how commercial and editorial photographs are made, written for photographers, producers, art directors and anyone curious about the frame.") + f'''
<section><div class="wrap two">
<div class="plain">
<h2>What this is</h2>
<p>{NAME} is an independent publication about photography in and around Los Angeles. Each story takes one kind of job — a skate shoe shoot, a magazine cover, a water polo match, a heritage footwear lookbook — and explains how that work is usually approached: casting, locations, light, lenses, timing and the edit.</p>
<p>The stories are practical. Expect specific focal lengths, shutter speeds and spot names rather than mood boards and adjectives.</p>
<h2>What this is not</h2>
<p>This site does not represent any photographer, and it does not claim to have photographed the brands, athletes, musicians or publications that appear in story titles. Those names describe the genre of work being discussed. Nothing here is sponsored or endorsed by them.</p>
<p>This domain previously hosted a photographer's portfolio. The journal is a new and separate publication with no connection to that photographer. If you came looking for their work, search for them directly.</p>
</div>
<div class="develop reveal">{img_tag("about", "Vintage camera and accessories laid out on a table", sizes="(max-width: 860px) 100vw, 45vw")}
</div>
</div></section>'''
    return page("/about", "About This Los Angeles Photography Journal",
                f"About {NAME}: an independent journal on how skate, footwear, editorial and sport photography is made in Los Angeles.",
                body, current="/about", image="about", ld=[crumbs_ld([("Home", "/"), ("About", "/about")])])


def build_contact():
    body = head_block("Contact", "Say <em>hello</em>", f'Story ideas, corrections, collaborations or a spot we should know about. Use the form or email <a href="mailto:{EMAIL}">{EMAIL}</a>.') + f'''
<section style="padding-bottom:clamp(64px,9vw,120px)"><div class="wrap two">
<div>
<div class="notice" role="status">Thanks, your message is in. Expect a reply within a few days.</div>
<form class="form" id="contact-form" method="post" action="/contact">
<div class="field"><label for="name">Name</label><input id="name" name="name" required maxlength="120" autocomplete="name"></div>
<div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required maxlength="200" autocomplete="email"></div>
<div class="field"><label for="topic">About</label><select id="topic" name="topic"><option>Story idea</option><option>Correction</option><option>Something else</option></select></div>
<div class="field"><label for="message">Message</label><textarea id="message" name="message" required maxlength="5000"></textarea></div>
<div class="hp" aria-hidden="true"><label for="website">Leave empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
<p><button class="btn" type="submit">Send message {ARROW}</button></p>
</form></div>
<div class="develop reveal">{img_tag("contact", "Photographer holding a camera lens up to the viewer", sizes="(max-width: 860px) 100vw, 45vw")}
</div>
</div></section>'''
    return page("/contact", "Contact the Journal",
                f"Contact {NAME}: send story ideas, corrections, Los Angeles photo spots and collaboration ideas to the journal's editors.",
                body, current="/contact", image="contact", ld=[crumbs_ld([("Home", "/"), ("Contact", "/contact")])])



def build_404():
    body = f'''<section class="lost"><div><p class="mono" style="color:var(--film)">Frame not found</p><h1>404</h1>
<p>That negative is missing from the sleeve. Try the journal instead.</p>
<p><a class="btn" href="/journal">Open the journal {ARROW}</a></p></div></section>'''
    return page("/404", "Page Not Found", "This page could not be found.", body).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')


# ---------------------------------------------------------------- server files
def index_php(slugs):
    routes = ",\n    ".join(f"'{s}' => 1" for s in sorted(slugs))
    redirects = ",\n    ".join(f"'{k}' => '{v}'" for k, v in REDIRECTS.items())
    return f'''<?php
// {NAME} front controller. The host serves real files directly and routes
// everything else here (it ignores .htaccess). See README.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
$canon = '{SITE}';

// Production host: force https and the bare domain. TLS terminates upstream.
$prod = ($host === 'asmith.photography' || $host === 'www.asmith.photography');
if ($prod && (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.asmith.photography')) {{
    header('Location: ' . $canon . $uri, true, 301);
    exit;
}}
// Temporary/preview hosts must not be indexed.
if (!$prod) {{
    header('X-Robots-Tag: noindex, nofollow');
}}

$routes = [
    {routes}
];
$redirects = [
    {redirects}
];

function send_page($file, $code = 200) {{
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/' . $file);
    exit;
}}

if ($path === '/' || $path === '/index.php' || $path === '/home') {{
    if ($path !== '/') {{ header('Location: /' . $qs, true, 301); exit; }}
    send_page('home.html');
}}
if (isset($redirects[$path])) {{
    header('Location: ' . $redirects[$path], true, 301);
    exit;
}}
// Old portfolio used /m/<slug> for mobile pages.
if (preg_match('#^/m/+([a-z0-9-]+)/?$#', $path, $m) && isset($routes[$m[1]])) {{
    header('Location: /' . $m[1], true, 301);
    exit;
}}
$slug = trim($path, '/');
if ($slug !== '' && $path !== '/' . $slug && isset($routes[$slug])) {{
    header('Location: /' . $slug . $qs, true, 301);   // strip trailing slash
    exit;
}}
if (strtolower($slug) !== $slug && isset($routes[strtolower($slug)])) {{
    header('Location: /' . strtolower($slug) . $qs, true, 301);
    exit;
}}

if ($slug === 'contact' && ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {{
    $f = function ($k, $n) {{ return mb_substr(trim((string)($_POST[$k] ?? '')), 0, $n); }};
    if ($f('website', 10) === '' && filter_var($f('email', 200), FILTER_VALIDATE_EMAIL) && $f('message', 5000) !== '') {{
        $dir = dirname(__DIR__) . '/asmith-messages';
        if (!is_dir($dir)) {{ @mkdir($dir, 0700, true); }}
        $row = ['at' => gmdate('c'), 'ip' => $_SERVER['REMOTE_ADDR'] ?? '', 'name' => $f('name', 120),
                'email' => $f('email', 200), 'topic' => $f('topic', 40), 'message' => $f('message', 5000)];
        @file_put_contents($dir . '/messages.jsonl', json_encode($row) . "\\n", FILE_APPEND | LOCK_EX);
        $from = filter_var($row['email'], FILTER_VALIDATE_EMAIL) ? str_replace(["\\r", "\\n"], '', $row['email']) : '';
        @mail('{EMAIL}', '[{NAME}] ' . $row['topic'] . ' from ' . str_replace(["\\r", "\\n"], ' ', $row['name']),
              $row['message'] . "\\n\\n-- " . $row['name'] . ' <' . $from . '>',
              'From: {EMAIL}' . "\\r\\n" . ($from ? 'Reply-To: ' . $from : ''));
    }}
    header('Location: /contact?sent=1', true, 303);
    exit;
}}
if (isset($routes[$slug])) {{
    send_page('pages/' . $slug . '.html');
}}
send_page('404.html', 404);
'''


def main():
    if PUB.exists():
        for sub in ["pages"]:
            shutil.rmtree(PUB / sub, ignore_errors=True)
    (PUB / "pages").mkdir(parents=True, exist_ok=True)
    (PUB / "assets/css").mkdir(parents=True, exist_ok=True)
    (PUB / "assets/js").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "src/site.css", PUB / "assets/css/site.css")
    shutil.copy(ROOT / "src/site.js", PUB / "assets/js/site.js")
    for f in (ROOT / "src/static").glob("*"):
        shutil.copy(f, PUB / f.name)

    (PUB / "home.html").write_text(build_home())
    out = {"journal": build_journal(), "about": build_about(), "contact": build_contact()}
    for p in PAGES:
        out[p["slug"]] = build_article(p)
    for slug, h in out.items():
        (PUB / "pages" / f"{slug}.html").write_text(h)
    (PUB / "404.html").write_text(build_404())
    (PUB / "index.php").write_text(index_php(out.keys()))
    (PUB / "robots.txt").write_text(f"User-agent: *\nDisallow: /pages/\nDisallow: /home.html\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = [("/", "1.0")] + [("/journal", "0.9")] + [(f"/{p['slug']}", "0.8") for p in PAGES] + \
           [("/about", "0.5"), ("/contact", "0.5")]
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{PUBLISHED}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
    (PUB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    print(f"built home + {len(out)} pages + 404")


if __name__ == "__main__":
    main()
