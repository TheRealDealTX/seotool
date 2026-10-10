#!/usr/bin/env python3
"""Build amandahornby.com (The Painted Room) into ./public.

Standard library only. Pages are written to public/_pages/<name>.html and
served at extensionless URLs (/about, /press, ...) by public/index.php, which
keeps the URL shape of the original site.
"""

import html
import json
import shutil
from datetime import date
from pathlib import Path

from content import GUIDES, PRESS, PROJECTS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
ORIGIN = "https://amandahornby.com"
BRAND = "The Painted Room"
EMAIL = "info@amandahornby.com"
TODAY = date.today().isoformat()
FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Manrope:wght@400;500;600&display=swap"

NAV = [("Home", "/"), ("About", "/about"), ("Projects", "/projects-1"), ("Journal", "/journal"), ("Press", "/press"), ("Contact", "/contact")]

e = html.escape


# Photographs: StockSnap.io, CC0 (public domain). name -> (alt text, width, height of the 960px file)
IMAGES = {
    "english-sitting-room-fireplace": ("A sitting room with striped sofas, a fireplace and built-in bookshelves", 960, 540),
    "living-room-piano-lounge-chair": ("A living room with an upright piano, a leather lounge chair and a Persian rug", 960, 622),
    "painted-kitchen-island-blue-stools": ("A white kitchen with a painted island and blue bar stools", 960, 640),
    "paint-roller-dark-paint": ("A paint roller applying dark paint to a wall", 960, 643),
    "kitchen-paint-colour-tins": ("Four open tins of paint in pink, teal, saffron and oxblood", 960, 640),
    "warm-kitchen-worktop": ("A kitchen worktop in warm window light with a coffee maker and a range cooker", 960, 641),
    "dark-green-tiled-bathroom": ("A bathroom with dark green tiles, a round lit mirror and a timber vanity", 960, 1438),
    "grey-tiled-bathroom-basin": ("A grey tiled bathroom wall above a white basin", 960, 640),
    "beamed-ceiling-pendant-lights": ("A vaulted ceiling with exposed timber beams and copper pendant lights", 960, 640),
    "timber-ceiling-detail": ("A boarded timber ceiling radiating from an octagonal centre", 960, 640),
    "grey-feature-wall-living-room": ("A living room with a dark grey feature wall and a lime green armchair", 960, 629),
    "teal-painted-wall-drawers": ("A teal painted wall behind a small wooden chest of drawers", 960, 1354),
    "garden-room-open-doors": ("Glazed doors open onto a garden room full of plants", 960, 600),
    "kitchen-bay-window-sink": ("A farmhouse kitchen sink beneath a bay window", 960, 640),
    "light-bedroom-curtains": ("A light bedroom with sheer curtains, a timber floor and plum cushions", 960, 634),
    "vintage-dining-room": ("A dining room with dark carved chairs and sunlight from tall windows", 960, 640),
    "cloakroom-roll-top-bath": ("A small bathroom with a roll-top bath and dark panelled walls", 960, 1438),
    "dark-snug-sofa-lamp": ("A dark snug with a sofa, cushions and a brass table lamp", 960, 640),
    "patterned-armchair": ("A mustard patterned armchair in a white room", 960, 640),
    "pale-blue-loveseat": ("A pale blue loveseat with patterned cushions", 960, 640),
    "decorating-paintbrush": ("A clean decorating paintbrush on a pale grey background", 960, 640),
    "eclectic-drawing-room": ("An eclectic drawing room with a chandelier, flowers and a brick wall", 960, 640),
    "blue-sofa-white-wall": ("A pale blue sofa against a plain wall with a framed print", 960, 638),
}


def photo(name, cls="", eager=False, sizes="(max-width: 860px) 100vw, 50vw"):
    alt, w, h = IMAGES[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    # Arch frames crop landscape photos hard, so they always get the full 960px file.
    srcset = "" if "arch" in cls else f'srcset="/assets/img/{name}-560.webp 560w, /assets/img/{name}.webp 960w" sizes="{sizes}" '
    return (f'<figure class="photo {cls}"><img src="/assets/img/{name}.webp" {srcset}'
            f'width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"></figure>')


def layout(path, title, desc, body, schema=None, current=None):
    canon = ORIGIN + path
    menu = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{n}</a></li>' for n, h in NAV)
    ld = [{
        "@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": ORIGIN + "/",
    }]
    if schema:
        ld.append(schema)
    guides = "".join(f'<li><a href="/journal/{g["slug"]}">{e(g["short"])}</a></li>' for g in GUIDES)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#f5f0e7">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/site.css?v={TODAY}">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <nav class="nav wrap" aria-label="Main">
    <a class="brand" href="/"><span class="brand-mark" aria-hidden="true"></span>{BRAND}</a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <ul class="menu">{menu}</ul>
  </nav>
</header>
<main id="main">
{body}
</main>
<section class="cta-band">
  <div class="wrap reveal">
    <span class="eyebrow" style="color:#fff">Start a room</span>
    <h2>Every room deserves a point of view.</h2>
    <p class="lede" style="color:#fbe7dc;margin:0 auto 2rem">Questions about colour, paper or a scheme you're planning? Write to us.</p>
    <a class="btn" href="/contact">Get in touch <span class="arr">→</span></a>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="brand" href="/"><span class="brand-mark" aria-hidden="true"></span>{BRAND}</a>
        <p>An independent journal about colour, pattern and rooms that feel lived in — paint, paper, panelling and the confidence to use them.</p>
      </div>
      <div><h4>Explore</h4><ul>{menu}</ul></div>
      <div><h4>Journal</h4><ul>{guides}</ul></div>
    </div>
    <div class="foot-bottom"><span>© {date.today().year} {BRAND}</span><span><a href="/privacy">Privacy</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
  </div>
</footer>
<script src="/assets/site.js?v={TODAY}" defer></script>
</body>
</html>
"""


def page_hero(eyebrow, h1, lede, crumbs=None, blob="var(--plaster)", img=None):
    c = ""
    if crumbs:
        c = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
            f'<a href="{h}">{e(n)}</a>' if h else e(n) for n, h in crumbs) + "</nav>"
    media = (f'<div class="page-hero-photo reveal">{photo(img, "arch", eager=True, sizes="(max-width: 860px) 90vw, 420px")}</div>'
             if img else f'<div class="blob" style="--blob:{blob}" data-speed=".15" aria-hidden="true"></div>')
    return f"""<section class="page-hero{' has-photo' if img else ''}">
  {media}
  <div class="wrap" style="position:relative">
    {c}
    <span class="eyebrow reveal">{eyebrow}</span>
    <h1 class="reveal">{h1}</h1>
    <p class="lede reveal">{lede}</p>
  </div>
</section>"""


def guide_card(g):
    return f"""<a class="card" href="/journal/{g['slug']}">
  <div class="thumb">{photo(g['img'], sizes="(max-width: 700px) 100vw, 400px")}</div>
  <div class="body"><span class="meta">{e(g['kicker'])}</span><h3>{e(g['short'])}</h3><p>{e(g['desc'][:118].rsplit(' ', 1)[0])}…</p></div>
</a>"""


def home():
    chips = [
        ("#b4552e", "Terracotta", "Earthy, warm and sociable — lovely in kitchens and dining rooms.", ""),
        ("#7c8a68", "Sage", "The great calm-maker. Works with oak, linen and brass.", ""),
        ("#22314a", "Inky navy", "A deep neutral. Try it on kitchen units or a study ceiling.", ""),
        ("#c8952c", "Ochre", "Bottled sunshine for north-facing rooms.", ""),
        ("#e9c6b1", "Plaster pink", "Soft, skin-warm and surprisingly grown-up.", "light"),
        ("#2f5d5a", "Deep teal", "Rich and enveloping — beautiful in bathrooms.", ""),
        ("#6e2a25", "Oxblood", "Candlelit drama for dining rooms and snugs.", ""),
        ("#efe4cf", "Parchment", "The warm white that flatters everything.", "light"),
    ]
    chip_html = "".join(
        f'<div class="chip {c}" style="background:{hx}"><span class="hex">{hx.upper()}</span><h3>{n}</h3><p>{t}</p></div>'
        for hx, n, t, c in chips)
    marquee_words = ["Colour drenching", "Painted ceilings", "Bathroom wallpaper", "Feature walls", "Kitchen cupboards", "Panelling", "Pattern", "Limewash"]
    mq = "".join(f"<span>{w}</span>" for w in marquee_words) * 2

    def dots(prop, opts):
        return f'<div class="dots" data-prop="{prop}">' + "".join(
            f'<button class="dot" type="button" style="background:{c}" data-color="{c}" data-name="{n}" data-tip="{e(t)}" aria-label="{n}" aria-pressed="{"true" if i == 0 else "false"}"></button>'
            for i, (c, n, t) in enumerate(opts)) + "</div>"

    mixer = f"""<div class="mixer">
  <div class="reveal-l mixer-photo" style="--wall:#9aa889">{photo("blue-sofa-white-wall")}<div class="tint" aria-hidden="true"></div></div>
  <div class="mixer-controls reveal">
    <div><span class="eyebrow">Try it</span><h2>Paint the wall</h2>
    <p class="lede">The same sofa, the same print — a completely different room. Tap a colour to see how the wall changes the mood.</p></div>
    <div class="mixer-group"><h4>Wall colour</h4>{dots("wall", [("#9aa889", "sage", "calm and easy to live with, and lovely with pale blue."), ("#c9734f", "terracotta", "warm and sociable; the blue sofa suddenly looks cooler and crisper."), ("#3d4c66", "navy", "deep and cocooning — the sofa and print glow against it."), ("#d9a441", "ochre", "sunny even on grey days, with the blue as a fresh contrast."), ("#e3b9a6", "plaster pink", "soft and skin-warm; a gentle partner for blue."), ("#4f7a72", "deep teal", "rich and tonal with the sofa — a very grown-up look."), ("#f1ebe0", "warm white", "light and simple, letting the furniture carry the colour.")])}</div>
    <p class="mixer-note" aria-live="polite">Sage — calm and easy to live with, and lovely with pale blue.</p>
  </div>
</div>"""

    body = f"""
<section class="hero">
  <div class="hero-photo">{photo("english-sitting-room-fireplace", "arch", eager=True, sizes="(max-width: 820px) 80vw, 560px")}</div>
  <div class="swatches" aria-hidden="true">
    <div class="sw a" data-name="Terracotta" data-speed=".35" data-rot=".02"></div>
    <div class="sw d" data-name="" data-speed=".6"></div>
    <div class="sw e" data-name="Stripe" data-speed=".2" data-rot="-.015"></div>
    <div class="sw b" data-name="Sage" data-speed=".5" data-rot="-.02"></div>
    <div class="sw c" data-name="Navy" data-speed=".75"></div>
  </div>
  <div class="wrap">
    <span class="eyebrow">Interior design &amp; decorating journal</span>
    <h1><span class="line"><span>Rooms with</span></span><span class="line"><span>a point of <em>view</em></span></span></h1>
    <p class="lede">Ideas for painting, papering and furnishing homes that feel personal — from kitchen cupboard colours to tented ceilings and feature walls.</p>
    <div class="cta-row"><a class="btn" href="/journal">Read the journal <span class="arr">→</span></a><a class="btn ghost" href="/projects-1">See room schemes</a></div>
  </div>
  <div class="scroll-cue" aria-hidden="true"></div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section">
  <div class="wrap split">
    <div class="reveal-l">{photo("living-room-piano-lounge-chair", "tall parallax-wrap")}</div>
    <div class="reveal">
      <span class="eyebrow">Our approach</span>
      <h2>Homes should look like the people who live in them.</h2>
      <p class="lede">The best interiors are never a designer's showcase. They reflect the lifestyle, interests and personality of the household — and they're practical enough to live in every day.</p>
      <p>That's the thinking behind everything we publish: interior design advice for real London flats and country houses alike, with an eye for detail and a respect for budget and timescale. Clear, honest guidance on colour, paint, wallpaper and the finishing touches that make a room feel complete.</p>
      <a class="btn ghost" href="/about">About the journal <span class="arr">→</span></a>
    </div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <span class="eyebrow reveal">Four principles</span>
    <h2 class="reveal" style="max-width:18ch">How we think about a room</h2>
    <div class="stack">
      <article class="stack-card"><span class="num">01</span><div><h3>Start with the light</h3><p>Which way does the room face? When is it used? North light cools colours; south light warms them. Choose paint at the time of day you'll use the room most.</p></div></article>
      <article class="stack-card"><span class="num">02</span><div><h3>One hero, two supports</h3><p>A scheme hangs together when one colour leads and two others support it — repeated across walls, fabrics and accessories.</p></div></article>
      <article class="stack-card"><span class="num">03</span><div><h3>Don't forget the fifth wall</h3><p>Ceilings, woodwork and the insides of cupboards are where a good room becomes a memorable one.</p></div></article>
      <article class="stack-card"><span class="num">04</span><div><h3>Live with it first</h3><p>Paint big sample boards, tape up wallpaper lengths, and live with them for a week. The right choice usually reveals itself.</p></div></article>
    </div>
  </div>
</section>

<section class="hscroll" aria-label="A palette we love">
  <div class="hscroll-pin">
    <div class="wrap hscroll-head reveal"><span class="eyebrow">Colour library</span><h2>A palette we keep coming back to</h2></div>
    <div class="hscroll-track">{chip_html}</div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <p class="big-quote" data-words>Not one room should be the same, because no two households are. Colour is how a house starts to tell you who lives there.</p>
    <div class="stats">
      <div class="stat"><b data-count="5">0</b><span>in-depth decorating guides</span></div>
      <div class="stat"><b data-count="6">0</b><span>room schemes to borrow</span></div>
      <div class="stat"><b data-count="40" data-suffix="+">0</b><span>colour pairings explored</span></div>
      <div class="stat"><b data-count="5">0</b><span>rooms: kitchens to ceilings</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">{mixer}</div>
</section>

<section class="section tint">
  <div class="wrap">
    <span class="eyebrow reveal">From the journal</span>
    <h2 class="reveal">Interior design ideas &amp; home inspiration</h2>
    <div class="grid stagger">{"".join(guide_card(g) for g in GUIDES)}</div>
  </div>
</section>
"""
    return layout("/", f"Interior Design Ideas & Home Inspiration | {BRAND}",
                  "Interior design ideas and home inspiration: kitchen cupboard paint, colourful kitchens, bathroom wallpaper, ceiling design and feature walls — with room schemes to borrow.",
                  body, current="/")


def about():
    body = page_hero("About", "A journal for people who love <em>rooms</em>",
                     "Practical, honest decorating advice — colour, paper, panelling and the details that make a house a home.",
                     [("Home", "/"), ("About", None)], img="eclectic-drawing-room") + f"""
<section class="section">
  <div class="wrap split">
    <div class="reveal-l">{photo("patterned-armchair", "tall")}</div>
    <div class="prose reveal">
      <h2>What we believe</h2>
      <p>Good interior design is less about following trends and more about understanding how a household lives. A kitchen used by a family of five needs different paint from a weekend cottage; a north-facing bedroom needs a different white from a sunny sitting room.</p>
      <p>We write about the decisions that make the biggest difference — the colour of the cupboards, the paper in the cloakroom, the ceiling nobody thought to paint — and we explain the practical side too: preparation, finishes, durability and cost.</p>
      <h3>How we work</h3>
      <ul>
        <li><strong>Client-first thinking.</strong> The end result must work aesthetically and practically for the people who live there.</li>
        <li><strong>Attention to detail.</strong> From initial concept to finishing touches.</li>
        <li><strong>Realism.</strong> Advice that respects budgets, timescales and old houses with wonky walls.</li>
      </ul>
      <h3>About this domain</h3>
      <p>amandahornby.com was previously the website of an interior designer of the same name. {BRAND} is an independent publication; it is not affiliated with, endorsed by or written by the previous owner of the domain.</p>
    </div>
  </div>
</section>"""
    return layout("/about", f"About | {BRAND}", f"About {BRAND}: an independent interior design journal with practical advice on colour, paint, wallpaper and room schemes.", body,
                  schema={"@context": "https://schema.org", "@type": "AboutPage", "name": f"About {BRAND}", "url": ORIGIN + "/about"}, current="/about")


def projects():
    cards = "".join(f"""<article class="card">
  <div class="thumb">{photo(p['img'], sizes="(max-width: 700px) 100vw, 400px")}</div>
  <div class="body"><span class="meta">{e(p['place'])}</span><h3>{e(p['name'])}</h3><p>{e(p['text'])}</p></div>
</article>""" for p in PROJECTS)
    body = page_hero("Projects", "Room schemes to <em>borrow</em>",
                     "Six rooms we keep coming back to — garden rooms, kitchens, bedrooms and more, with the ideas worth borrowing from each.",
                     [("Home", "/"), ("Projects", None)], blob="#c9d1bb") + f"""
<section class="section">
  <div class="wrap">
    <div class="grid stagger">{cards}</div>
    <p class="reveal" style="margin-top:3rem;color:var(--ink-2);font-size:.92rem">These are inspiration images (royalty-free CC0 photography), not photographs of client projects.</p>
  </div>
</section>"""
    return layout("/projects-1", f"Projects: Room Schemes | {BRAND}", "Interior design room schemes to borrow: country sitting room, townhouse kitchen, striped attic bedroom, midnight dining room, papered cloakroom and terracotta snug.", body, current="/projects-1")


def press():
    rows = "".join(f'<li><a href="{u}" rel="noopener" target="_blank"><span class="src">{e(s)}</span><span class="t">{e(t)}</span><span aria-hidden="true">↗</span></a></li>' for s, t, u, _ in PRESS)
    body = page_hero("Press", "Further <em>reading</em>",
                     "Decorating features from around the web that we return to again and again, paired with our own guides on the same subjects.",
                     [("Home", "/"), ("Press", None)], img="decorating-paintbrush") + f"""
<section class="section">
  <div class="wrap">
    <ul class="press-list reveal">{rows}</ul>
    <h2 class="reveal" style="margin-top:5rem">Our guides on the same topics</h2>
    <div class="grid stagger">{"".join(guide_card(g) for g in GUIDES)}</div>
  </div>
</section>"""
    return layout("/press", f"Press & Further Reading | {BRAND}", "Recommended decorating features on kitchen paint, bathroom wallpaper, ceilings and feature walls, alongside our own interior design guides.", body, current="/press")


def contact():
    body = page_hero("Contact", "Say <em>hello</em>",
                     "Questions about a guide, a colour you can't decide on, or an idea for a feature? We'd love to hear from you.",
                     [("Home", "/"), ("Contact", None)], img="pale-blue-loveseat") + f"""
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="reveal-l">
      <h2>Enquiries</h2>
      <p class="lede">Email <a href="mailto:{EMAIL}">{EMAIL}</a>, or use the form — it opens a pre-filled email in your mail app, so nothing is stored on this website.</p>
      <div class="palette-row" style="max-width:420px"><div style="background:#b4552e"></div><div style="background:#7c8a68"></div><div style="background:#22314a"></div></div>
    </div>
    <form class="form reveal" data-mailto="{EMAIL}">
      <div class="row"><label>First name<input name="first_name" required autocomplete="given-name"></label><label>Last name<input name="last_name" autocomplete="family-name"></label></div>
      <label>Email address<input type="email" name="email" required autocomplete="email"></label>
      <label>Subject<select name="subject"><option>A question about a guide</option><option>Colour advice</option><option>Feature or collaboration idea</option><option>Something else</option></select></label>
      <label>Message<textarea name="message" required></textarea></label>
      <div><button class="btn" type="submit">Send message <span class="arr">→</span></button></div>
    </form>
  </div>
</section>"""
    return layout("/contact", f"Contact | {BRAND}", f"Contact {BRAND} with questions about colour, paint, wallpaper or our interior design guides.", body,
                  schema={"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {BRAND}", "url": ORIGIN + "/contact"}, current="/contact")


def journal_index():
    body = page_hero("Journal", "Decorating <em>guides</em>",
                     "In-depth, practical guides to the decisions that change a room the most.",
                     [("Home", "/"), ("Journal", None)], blob="#e9c6b1") + f"""
<section class="section"><div class="wrap"><div class="grid stagger">{"".join(guide_card(g) for g in GUIDES)}</div></div></section>"""
    return layout("/journal", f"Journal: Decorating Guides | {BRAND}", "Interior decorating guides: painting kitchen cupboards, colourful kitchens, bathroom wallpaper, ceiling design ideas and feature walls.", body, current="/journal")


def slugify(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-").replace("--", "-")


def guide(g):
    path = f"/journal/{g['slug']}"
    toc = "".join(f'<li><a href="#{slugify(h)}">{e(h)}</a></li>' for h, _ in g["sections"])
    img2, cap2 = g["img2"]
    fig2 = f'<div class="reveal inline-photo">{photo(img2, "wide", sizes="(max-width: 960px) 100vw, 700px")}<p class="caption">{e(cap2)}</p></div>'
    secs = "".join(f'<h2 id="{slugify(h)}">{e(h)}</h2>{b}' + (fig2 if i == 0 else "") for i, (h, b) in enumerate(g["sections"]))
    pal = "".join(f'<div class="{"light" if len(p) > 2 else ""}" style="background:{p[1]}">{e(p[0])}<br>{p[1].upper()}</div>' for p in g["palette"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faq"])
    others = [o for o in GUIDES if o is not g][:3]
    schema = [{
        "@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
        "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": ORIGIN + path,
        "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND},
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]],
    }]
    body = page_hero(g["kicker"], e(g["title"]), e(g["intro"]),
                     [("Home", "/"), ("Journal", "/journal"), (g["short"], None)], img=g["img"]) + f"""
<section class="section">
  <div class="wrap article">
    <article class="prose">
      <h3 style="margin-top:0">The palette</h3>
      <div class="palette-row stagger">{pal}</div>
      {secs}
      <h2 id="faq">Frequently asked questions</h2>
      <div class="faq">{faq}</div>
    </article>
    <aside class="aside">
      <div class="aside-box toc"><h4>In this guide</h4><ol>{toc}<li><a href="#faq">FAQs</a></li></ol></div>
      <div class="aside-box"><h4>More guides</h4><ol>{"".join(f'<li><a href="/journal/{o["slug"]}">{e(o["short"])}</a></li>' for o in others)}</ol></div>
    </aside>
  </div>
</section>
<section class="section tint"><div class="wrap"><h2 class="reveal">Keep reading</h2><div class="grid stagger">{"".join(guide_card(o) for o in others)}</div></div></section>"""
    return layout(path, f"{g['title']} | {BRAND}", g["desc"], body, schema=schema, current="/journal")


def privacy():
    body = page_hero("Privacy", "Privacy notice", "Short and simple.", [("Home", "/"), ("Privacy", None)]) + f"""
<section class="section"><div class="wrap prose">
<p>{BRAND} does not use analytics, advertising cookies or tracking scripts, and does not store personal data on this website. Our contact form opens an email in your own mail application; we only receive what you choose to send.</p>
<p>Photography is from <a href="https://stocksnap.io/" rel="noopener">StockSnap</a> and released under the CC0 public-domain licence.</p>
<p>Web fonts are loaded from Google Fonts, which may log your IP address as part of serving the files. Our host keeps standard server logs for security purposes.</p>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    return layout("/privacy", f"Privacy | {BRAND}", f"Privacy notice for {BRAND}.", body)


def not_found():
    body = page_hero("404", "This room is <em>empty</em>", "The page you were looking for has moved or never existed.", blob="#e8d3a8") + """
<section class="section"><div class="wrap"><a class="btn" href="/">Back to the homepage <span class="arr">→</span></a></div></section>"""
    return layout("/404", f"Page not found | {BRAND}", "Page not found.", body).replace(
        '<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"', 1)


FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><path d="M16 2a14 14 0 0 1 14 14v14H16A14 14 0 0 1 16 2z" fill="#b4552e"/><path d="M16 2v14h14A14 14 0 0 0 16 2z" fill="#c8952c"/><path d="M16 16v14h14V16z" fill="#22314a"/><path d="M2 16a14 14 0 0 0 14 14V16z" fill="#7c8a68"/></svg>"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "_pages").mkdir(parents=True)
    (OUT / "assets").mkdir()
    pages = {"home": home(), "about": about(), "projects-1": projects(), "press": press(), "contact": contact(),
             "journal": journal_index(), "privacy": privacy(), "404": not_found()}
    for g in GUIDES:
        pages["journal--" + g["slug"]] = guide(g)
    for name, src in pages.items():
        (OUT / "_pages" / f"{name}.html").write_text(src, encoding="utf-8")
    shutil.copy(ROOT / "src" / "site.css", OUT / "assets" / "site.css")
    shutil.copy(ROOT / "src" / "site.js", OUT / "assets" / "site.js")
    shutil.copy(ROOT / "src" / "index.php", OUT / "index.php")
    shutil.copytree(ROOT / "src" / "img", OUT / "assets" / "img")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    urls = ["/", "/about", "/projects-1", "/journal", "/press", "/contact", "/privacy"] + [f"/journal/{g['slug']}" for g in GUIDES]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_pages/\n\nSitemap: {ORIGIN}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(pages)} pages into {OUT}")


if __name__ == "__main__":
    main()
