#!/usr/bin/env python3
"""Static site generator for ollieharperstudio.com.

    python3 build.py              # production build (indexable)
    STAGING=1 python3 build.py    # staging build: noindex everywhere, robots.txt disallows all

Writes the site into this directory. No dependencies beyond the standard library.
"""

import json
import os
from datetime import date
from html import escape
from pathlib import Path

from art import ART, FAVICON, SHADES

ROOT = Path(__file__).resolve().parent
ORIGIN = "https://ollieharperstudio.com"
NAME = "Ollie Harper Studio"
EMAIL = "hello@ollieharperstudio.com"
STAGING = os.environ.get("STAGING") == "1"
TODAY = date.today().isoformat()
FONTS = ("https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700"
         "&family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&display=swap")

NAV = [
    ("Commercial", "/"),
    ("Culinary", "/culinary/"),
    ("Fashion", "/images/"),
    ("Coloring Book", "/coloring-book/"),
    ("Styling", "/set-stylingdirection/"),
    ("Projects", "/projects/"),
    ("Thoughts", "/thoughts/"),
]

PAGES = []  # (path, lastmod) for the sitemap


# Royalty-free (CC0) photography, see assets/photos/credits.json and the README.
PHOTOS = json.loads((ROOT / "assets/photos/credits.json").read_text(encoding="utf-8"))


def photo(name, cls="photo", eager=False, sizes="(max-width: 920px) 100vw, 50vw"):
    """A framed, responsive WebP photo. Hero photos load eagerly, everything else lazily."""
    p = PHOTOS[name]
    srcset = ", ".join(f"/assets/photos/{name}-{w}.webp {w}w" for w in p["widths"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<div class="{cls}"><img src="/assets/photos/{name}-{p["widths"][-1]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{escape(p["alt"])}" width="960" height="720" {load} decoding="async"></div>')


def art(name, cls="photo", eager=False):
    return photo(name, cls, eager)


def img(name, alt=None, w=None, h=None):
    return photo(name, "tile-photo", sizes="(max-width: 920px) 50vw, 25vw")


def breadcrumbs(trail):
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + p} for i, (n, p) in enumerate(trail)]
    html = ' <span>/</span> '.join(f'<a href="{p}">{escape(n)}</a>' if i < len(trail) - 1 else escape(n)
                                   for i, (n, p) in enumerate(trail))
    return f'<nav class="crumbs" aria-label="Breadcrumb">{html}</nav>', {"@type": "BreadcrumbList", "itemListElement": items}


ORG = {
    "@type": "Organization", "@id": ORIGIN + "/#org", "name": NAME, "url": ORIGIN + "/",
    "logo": ORIGIN + "/favicon.svg", "email": EMAIL,
    "description": "Independent illustration studio for food, fashion, beauty and lifestyle brands.",
    "knowsAbout": ["Commercial illustration", "Food illustration", "Fashion illustration", "Coloring books",
                   "Prop styling", "Art direction"],
}
WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": NAME, "publisher": {"@id": ORIGIN + "/#org"}}


def layout(path, title, desc, body, schema=(), og_type="website", current=None):
    canonical = ORIGIN + path
    graph = [ORG, WEBSITE, *schema]
    nav = ''.join(f'<a href="{href}"{" aria-current=page" if href == (current or path) else ""}>{label}</a>'
                  for label, href in NAV)
    robots = '<meta name="robots" content="noindex, nofollow">' if STAGING else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f6efe6">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/site.css?v={TODAY}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark">OH</span><span>Ollie Harper<small>Illustration Studio</small></span></a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn" href="/contact/">Start a project</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="/"><span class="logo-mark">OH</span><span>Ollie Harper<small>Illustration Studio</small></span></a>
        <p>Hand-drawn illustration for food, fashion, beauty and lifestyle brands — menus, packaging, campaigns, editorial and coloring books.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Work</h4><ul>
        <li><a href="/">Commercial illustration</a></li><li><a href="/culinary/">Culinary illustration</a></li>
        <li><a href="/images/">Fashion &amp; beauty</a></li><li><a href="/coloring-book/">Coloring book</a></li>
        <li><a href="/set-stylingdirection/">Prop styling &amp; set direction</a></li></ul></div>
      <div><h4>Studio</h4><ul>
        <li><a href="/projects/">Projects</a></li><li><a href="/thoughts/">Thoughts (journal)</a></li>
        <li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
    </div>
    <div class="footer-word" aria-hidden="true">Ollie Harper Studio</div>
    <div class="legal"><span>© {date.today().year} {NAME}. Photography: CC0 / royalty-free.</span><span>Drawn with a lot of coffee.</span></div>
  </div>
</footer>
<script src="/assets/js/site.js?v={TODAY}" defer></script>
</body>
</html>
"""


def write(path, html, sitemap=True):
    out = ROOT / ("home.html" if path == "/" else path.strip("/") + "/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    if sitemap:
        PAGES.append(path)


def page_hero(trail, eyebrow, h1, lede, art_name, actions=""):
    crumbs, crumb_schema = breadcrumbs(trail)
    return f"""<section class="page-hero"><div class="wrap">
  <div>{crumbs}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lede">{lede}</p>{actions}</div>
  <div class="hero-art reveal">{art(art_name, "photo hero-photo", eager=True)}</div>
</div></section>""", crumb_schema


def cta(h2="Got a menu, a launch or a blank wall?", lede="Tell us what you're making. We'll reply within two working days with ideas, a timeline and a quote."):
    return f"""<section class="section dark cta"><div class="wrap reveal">
  <span class="eyebrow">Commissions open</span><h2>{h2}</h2><p class="lede">{lede}</p>
  <a class="btn" href="/contact/">Start a project <span class="arrow">→</span></a>
</div></section>"""


def faq(items):
    html = ''.join(f'<details class="reveal"><summary>{escape(q)}</summary><p>{a}</p></details>' for q, a in items)
    schema = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<div class="faq">{html}</div>', schema


def gallery(tiles):
    return '<div class="gallery">' + ''.join(
        f'<figure class="reveal">{img(n, cap)}<figcaption>{escape(cap)}</figcaption></figure>' for n, cap in tiles) + '</div>'


def marquee(words):
    run = ''.join(f'<span>{w}</span>' for w in words)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track">{run}{run}</div></div>'


# ---------------------------------------------------------------- pages

def home():
    cards = [
        ("/culinary/", "tile-latte", "Culinary", "Menus, latte art boards, recipe cards and packaging that make people hungry.", "c-tomato"),
        ("/images/", "tile-sunglasses", "Fashion &amp; beauty", "Lookbooks, product launches and beauty illustration with personality.", ""),
        ("/coloring-book/", "tile-plant", "Coloring book", "Line-art rooms and patterns to color — try one right in your browser.", "c-sage"),
        ("/set-stylingdirection/", "tile-chair", "Styling &amp; set direction", "Props, palettes and sets that make illustration and photography sing.", "c-mustard"),
    ]
    card_html = ''.join(
        f'<a class="card reveal {c}" href="{h}"><div class="art">{img(i, t.replace("&amp;", "and") + " illustration")}</div>'
        f'<h3>{t}</h3><p>{d}</p><span class="more">Explore <span class="arrow">→</span></span></a>' for h, i, t, d, c in cards)
    faq_html, faq_schema = faq([
        ("What is commercial illustration?",
         "Commercial illustration is artwork made to do a job for a business: sell a product, explain a menu, launch a "
         "campaign, decorate packaging or give a brand a recognizable look. Unlike gallery art, it's briefed, licensed "
         "for specific uses and delivered in the formats the brand needs."),
        ("How much does a custom illustration cost?",
         "It depends on the number of pieces, how detailed they are and how widely they'll be used. A single spot "
         "illustration for social media costs far less than a campaign hero image licensed for print, packaging and "
         "out-of-home. We quote every project individually after a short call."),
        ("How long does a commission take?",
         "Most single illustrations take one to two weeks from approved sketch to final files. Menu sets, packaging "
         "ranges and coloring books are scheduled in stages, typically four to eight weeks."),
        ("What files will I receive?",
         "Final artwork is delivered as layered source files plus print-ready PDF, high-resolution PNG and, for flat "
         "vector work, SVG — sized for every placement agreed in the brief."),
        ("Do you work with small businesses?",
         "Yes. Independent cafés, restaurants, boutiques and makers are some of our favorite clients. We scope projects "
         "so they fit the budget without cutting the craft."),
    ])
    body = f"""<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow">Ollie Harper — Commercial Illustration Studio</span>
    <h1><span class="line"><span>Illustration</span></span><span class="line"><span>with an <em class="hl">appetite</em></span></span><span class="line"><span>for color.</span></span></h1>
    <p class="lede">We draw for food, fashion, beauty and lifestyle brands — menus, packaging, campaigns, editorial and coloring books that people actually want to keep.</p>
    <div class="hero-actions"><a class="btn" href="/contact/">Start a project <span class="arrow">→</span></a><a class="btn ghost" href="/projects/">See how we work</a></div>
  </div>
  <div class="hero-art">{art("hero", "photo hero-photo", eager=True)}<div class="sticker" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="ring" d="M60 60 m-46 0 a46 46 0 1 1 92 0 a46 46 0 1 1 -92 0"/></defs><text font-family="DM Sans, sans-serif" font-size="10.5" font-weight="700" fill="#1d1a24"><textPath href="#ring" textLength="286" lengthAdjust="spacing">COMMISSIONS OPEN • DRAWN BY HAND • </textPath></text></svg><b>OH</b></div></div>
</div></section>
{marquee(["Menus", "Packaging", "Campaigns", "Editorial", "Lookbooks", "Coloring books", "Murals", "Merch"])}
<section class="section"><div class="wrap">
  <div class="section-head"><h2 class="reveal">Four ways we put pencil to paper.</h2>
  <p class="lede reveal">Every brief starts by hand. The artwork is then built for the places it has to work: on a cup sleeve, a billboard or a phone screen.</p></div>
  <div class="cards">{card_html}</div>
</div></section>
<section class="section alt"><div class="wrap split">
  <div class="reveal">{art("studio")}</div>
  <div class="reveal"><span class="eyebrow">Commercial illustration</span><h2>Artwork that does a job — and looks good doing it.</h2>
    <p>A good commercial illustration has to work harder than a photo. It has to explain a product, carry a brand's personality and still read at thumbnail size. We design every piece around where it will live, so the line weight, palette and composition hold up from a 30-second scroll to a six-foot window decal.</p>
    <p>Typical commissions include campaign key art, seasonal promo cards, product packaging, event posters, editorial spot illustrations, tote and tee graphics, and the small brand moments in between: thank-you cards, menu boards, stickers.</p>
    <ul class="chips"><li>Campaign key art</li><li>Packaging</li><li>Editorial spots</li><li>Promo postcards</li><li>Event posters</li><li>Merch</li></ul>
  </div>
</div></section>
<section class="section dark"><div class="wrap">
  <div class="section-head"><h2 class="reveal">Hand-drawn, digitally finished.</h2><p class="lede reveal">The studio process in four steps, built so you see the idea before you pay for polish.</p></div>
  <div class="stats">
    <div class="stat reveal"><b>01</b>Brief &amp; mood board — we pin down the audience, the uses and the feeling.</div>
    <div class="stat reveal"><b>02</b>Pencil roughs — two or three loose directions to react to.</div>
    <div class="stat reveal"><b>03</b>Color &amp; refine — one direction taken to final line and palette.</div>
    <div class="stat reveal"><b>04</b>Delivery — print, web and source files for every agreed placement.</div>
  </div>
</div></section>
<section class="section"><div class="wrap split flip">
  <div class="reveal">{art("lipsticks")}</div>
  <div class="reveal"><span class="eyebrow">From the journal</span><h2>Lipstick Theory: what your shade says about you.</h2>
  <p>One of the studio's favorite series: eight classic lipstick shades, illustrated and read like a horoscope. Bold red, sheer nude, deep plum — which one is yours?</p>
  <a class="btn ghost" href="/thoughts/lipstick-theory/">Read the theory <span class="arrow">→</span></a></div>
</div></section>
<section class="section alt"><div class="wrap layout">
  <div><span class="eyebrow">Questions</span><h2 class="reveal">Commissioning an illustrator, answered.</h2>{faq_html}</div>
  <aside class="aside"><div class="panel ink reveal"><h3>Quick brief</h3><p>Send what it's for, where it'll appear and when you need it. That's enough for a first quote.</p><a class="btn" href="/contact/">Contact the studio</a></div></aside>
</div></section>
{cta()}"""
    write("/", layout("/", "Ollie Harper Studio — Commercial Illustration for Food, Fashion & Lifestyle Brands",
                      "Ollie Harper is a commercial illustration studio drawing menus, packaging, campaigns, fashion and beauty artwork and coloring books for brands that love color.",
                      body, [faq_schema, {"@type": "WebPage", "@id": ORIGIN + "/#webpage", "url": ORIGIN + "/",
                                          "name": "Commercial Illustration Studio", "isPartOf": {"@id": ORIGIN + "/#website"},
                                          "about": {"@id": ORIGIN + "/#org"}}]))


def culinary():
    hero, crumb = page_hero([("Home", "/"), ("Culinary", "/culinary/")], "Food &amp; drink illustration",
                            "Culinary illustration that makes people hungry.",
                            "Menus, coffee and juice bar boards, recipe cards, packaging and seasonal promos for restaurants, cafés and food brands.",
                            "culinary", '<div class="hero-actions"><a class="btn" href="/contact/">Commission food art <span class="arrow">→</span></a></div>')
    faq_html, faq_schema = faq([
        ("Why use illustration instead of food photography?",
         "Illustration lets you show ingredients, process and personality at once, it stays consistent across a "
         "seasonal menu, and it never looks dated the way a styled photo can. Many brands use both: photography for "
         "the plate, illustration for the story."),
        ("Can you illustrate a full menu?",
         "Yes — from a single hero drawing to a complete set of item icons, section dividers and a cover. We deliver "
         "the artwork in layers so your designer or printer can update prices and items without redrawing."),
        ("Do you draw packaging?",
         "We create illustration for labels, cups, boxes and bags, and supply files set up to the die line your "
         "printer provides."),
    ])
    body = f"""{hero}
{marquee(["Seasonal lattes", "Menu boards", "Recipe cards", "Labels", "Juice bars", "Bakeries", "Pop-ups"])}
<section class="section"><div class="wrap layout">
  <article class="prose">
    <h2 class="reveal">Food illustration with flavor</h2>
    <p>Food is one of the most rewarding things to draw because everyone already has an opinion about it. A good culinary illustration taps into that: the curl of steam over a latte, the shine on a glazed bun, the drip of a cold-pressed juice. We exaggerate the details that make food appealing and leave out the ones that don't.</p>
    <p>Our culinary work is built for real-world use in hospitality. Menu illustrations are drawn to sit beside type without crowding it. Seasonal drink launches get a family of matching pieces so a café can roll out a new flavor on the board, the cup sleeve and Instagram on the same day. Packaging art is designed around the shape it wraps.</p>
    <h2 class="reveal">What we draw for food and beverage brands</h2>
    <ul>
      <li><strong>Menu illustration</strong> — covers, section headers, item icons and full illustrated menus.</li>
      <li><strong>Café and juice bar boards</strong> — chalkboard-style or full-color drink boards and seasonal specials.</li>
      <li><strong>Recipe and ingredient illustration</strong> — step-by-step cards, cookbook spots and ingredient breakdowns.</li>
      <li><strong>Packaging and labels</strong> — coffee bags, jars, bottles, boxes and cup sleeves.</li>
      <li><strong>Promo and social</strong> — launch posts, postcards and in-store signage.</li>
      <li><strong>Neighborhood food maps</strong> — illustrated guides for districts, hotels and tourism boards.</li>
    </ul>
    <h2 class="reveal">The ingredients-first approach</h2>
    <p>We start every food project in the kitchen or behind the bar. Tasting the product, watching how it's made and photographing references gives the drawings the small truths that make them believable — the exact color of a matcha, the way a particular pastry flakes. Then we simplify: a strong silhouette, a limited palette and a confident line so the artwork reads instantly from across a room.</p>
    <blockquote>The best menu art makes someone order something they didn't come in for.</blockquote>
    <h2 class="reveal">On the reference board</h2>
    {gallery([("tile-latte", "Seasonal latte"), ("tile-croissant", "Butter croissant"), ("tile-lemon", "Fresh lemons"), ("tile-pizza", "Slice of the day")])}
    <h2 class="reveal">Questions about food illustration</h2>{faq_html}
  </article>
  <aside class="aside">
    <div class="panel reveal"><h3>Good fits</h3><ul><li><a href="/contact/">Independent cafés &amp; roasters</a></li><li><a href="/contact/">Restaurants &amp; bars</a></li><li><a href="/contact/">Juice &amp; smoothie bars</a></li><li><a href="/contact/">Food &amp; drink brands</a></li><li><a href="/contact/">Cookbook publishers</a></li></ul></div>
    <div class="panel reveal"><h3>Read next</h3><ul><li><a href="/thoughts/artsdistrictingredients/">Arts District Ingredients: drawing a neighborhood food map</a></li><li><a href="/projects/">How a menu project runs</a></li></ul></div>
  </aside>
</div></section>
{cta("Hungry for a new menu?")}"""
    write("/culinary/", layout("/culinary/", "Culinary Illustration — Menus, Café Boards & Food Packaging | Ollie Harper",
                               "Food and drink illustration for restaurants, cafés and food brands: illustrated menus, seasonal drink boards, recipe cards and packaging.",
                               body, [crumb, faq_schema, {"@type": "Service", "name": "Culinary illustration", "serviceType": "Food illustration",
                                                          "provider": {"@id": ORIGIN + "/#org"}, "url": ORIGIN + "/culinary/"}]))


def fashion():
    hero, crumb = page_hero([("Home", "/"), ("Fashion & Beauty", "/images/")], "Fashion &amp; beauty illustration",
                            "Fashion illustration with a point of view.",
                            "Lookbooks, beauty launches, how-to guides, lingerie and accessories, editorial spots and window art — drawn with attitude.",
                            "fashion", '<div class="hero-actions"><a class="btn" href="/contact/">Commission fashion art <span class="arrow">→</span></a></div>')
    faq_html, faq_schema = faq([
        ("What is fashion illustration used for today?",
         "Brands use fashion illustration for campaign art, lookbooks, how-to-wear guides, product launches, packaging, "
         "social content and window displays. It signals craft and gives a collection a mood that photography alone "
         "can't."),
        ("Can you illustrate our actual products?",
         "Yes. We work from samples, tech packs or product photography, so colors, cuts and details are accurate — then "
         "style them with the attitude of the brand."),
        ("Do you do beauty and cosmetics illustration?",
         "Often. Lipstick, skincare and fragrance are a joy to draw: rich color, glossy surfaces and strong packaging "
         "shapes. See our Lipstick Theory series for an example."),
    ])
    body = f"""{hero}
{marquee(["Lookbooks", "Beauty launches", "How-to-wear", "Accessories", "Windows", "Editorial"])}
<section class="section"><div class="wrap layout">
  <article class="prose">
    <h2 class="reveal">Drawn, not just styled</h2>
    <p>Fashion illustration is the oldest form of fashion image, and it's back for a reason: in a feed full of near-identical product shots, a drawing stops the scroll. It lets a brand show the feeling of a collection — the swing of a coat, the shine of a lip — and not only the garment.</p>
    <p>Our fashion and beauty work leans graphic: confident outlines, saturated color and a little humor. We're happiest drawing accessories and beauty products with real personality, and "how to wear it" guides that make styling advice genuinely useful.</p>
    <h2 class="reveal">Fashion &amp; beauty services</h2>
    <ul>
      <li><strong>Campaign and seasonal artwork</strong> for fall, holiday and spring launches.</li>
      <li><strong>Beauty and cosmetics illustration</strong> — lipstick, skincare, fragrance and nail color.</li>
      <li><strong>How-to and styling guides</strong> — "five ways to wear boyfriend jeans" style explainers.</li>
      <li><strong>Lingerie and swim illustration</strong>, tasteful and on-brand.</li>
      <li><strong>Event posters and invitations</strong> for shows, pop-ups and launch parties.</li>
      <li><strong>Window and in-store art</strong> sized for vinyl, print or hand-painting.</li>
    </ul>
    <h2 class="reveal">A small accessories edit</h2>
    {gallery([("tile-sunglasses", "Cat-eye sunglasses"), ("tile-heel", "Night-out heels"), ("tile-lipstick", "The full palette"), ("tile-pencil", "Color pencils")])}
    <h2 class="reveal">Color that sells</h2>
    <p>We build a fashion palette from the product outward: the hero color of the collection, one supporting tone and one surprise accent. That discipline keeps a series of illustrations recognizable across a whole season, whether it's printed on a shopping bag or animated in a story.</p>
    <h2 class="reveal">Questions about fashion illustration</h2>{faq_html}
  </article>
  <aside class="aside">
    <div class="panel reveal"><h3>Read next</h3><ul><li><a href="/thoughts/lipstick-theory/">Lipstick Theory: what your shade says about you</a></li><li><a href="/set-stylingdirection/">Prop styling &amp; set direction</a></li></ul></div>
    <div class="panel ink reveal"><h3>Launching soon?</h3><p>Fashion calendars move fast. Send dates early and we'll hold space.</p><a class="btn" href="/contact/">Book a slot</a></div>
  </aside>
</div></section>
{cta("Let's dress up your next launch.")}"""
    write("/images/", layout("/images/", "Fashion & Beauty Illustration — Lookbooks, Launches & Editorial | Ollie Harper",
                             "Fashion and beauty illustration for campaigns, lookbooks, cosmetics launches, how-to-wear guides, event posters and window displays.",
                             body, [crumb, faq_schema, {"@type": "Service", "name": "Fashion and beauty illustration", "serviceType": "Fashion illustration",
                                                        "provider": {"@id": ORIGIN + "/#org"}, "url": ORIGIN + "/images/"}], current="/images/"))


def coloring():
    hero, crumb = page_hero([("Home", "/"), ("Coloring Book", "/coloring-book/")], "Coloring book",
                            "Rooms to color, dream up and make your own.",
                            "Hand-drawn interiors and patterns for all ages. Try a page right here — pick a color, click a shape, and download your finished room.",
                            "coloring", '<div class="hero-actions"><a class="btn" href="#studio">Start coloring <span class="arrow">↓</span></a></div>')
    palette = ''.join(
        f'<button type="button" style="--sw:{c}" data-color="{c}" aria-label="{n}" aria-pressed="{"true" if i == 0 else "false"}"></button>'
        for i, (n, c) in enumerate([("Tomato", "#ef5b3c"), ("Blush", "#f4a7b9"), ("Mustard", "#f2b134"), ("Sage", "#8fb39a"),
                                    ("Cobalt", "#3550d6"), ("Plum", "#6b2d5c"), ("Sand", "#e9d5b7"), ("Ink", "#1d1a24")]))
    faq_html, faq_schema = faq([
        ("Who is the coloring book for?",
         "Everyone. The rooms are drawn with big, friendly shapes for younger colorers and plenty of small pattern "
         "areas for adults who like detail."),
        ("Can I print the pages?",
         "Yes. Use the download button to save your page as an SVG, which prints crisply at any size. Blank pages "
         "print best on heavyweight matte paper."),
        ("Do you create custom coloring books?",
         "We do — for brands, hotels, restaurants, events and publishers. Custom books make great kids' menus, "
         "welcome gifts and merch."),
    ])
    body = f"""{hero}
<section class="section alt" id="studio"><div class="wrap">
  <div class="section-head"><h2 class="reveal">The living room — color it in.</h2><p class="lede reveal">Choose a swatch, then click or tap any shape. Undo, clear, or let us surprise you.</p></div>
  <div class="studio reveal" data-studio>
    <div class="canvas">{ART["coloring-room"]}</div>
    <div class="panel"><h3>Palette</h3><div class="palette">{palette}</div>
      <div class="studio-tools"><label class="form-note">Custom color <input type="color" value="#ef5b3c" aria-label="Pick a custom color"></label>
        <button class="btn ghost" type="button" data-undo>Undo</button><button class="btn ghost" type="button" data-surprise>Surprise me</button>
        <button class="btn ghost" type="button" data-clear>Clear page</button><button class="btn" type="button" data-download>Download page</button></div>
    </div>
  </div>
</div></section>
<section class="section"><div class="wrap layout">
  <article class="prose">
    <h2 class="reveal">A coloring book about the spaces we love</h2>
    <p>Our coloring pages are drawn around rooms: sunlit living rooms, cluttered studios, kitchens mid-recipe, reading nooks and tiny balconies full of plants. Each page is meant to be lived in. Stay inside the lines if you like — or invent your own wallpaper, rug and upholstery patterns in the blank spaces we leave on purpose.</p>
    <h2 class="reveal">Why adults color</h2>
    <p>Coloring is focused without being demanding. It gives your hands something to do while your mind slows down, there are no wrong answers, and you finish with something you made. Interiors are especially satisfying because every choice — a teal sofa, a blush wall, a mustard rug — is a tiny piece of interior design.</p>
    <h2 class="reveal">Tips for better pages</h2>
    <ol>
      <li><strong>Pick a palette first.</strong> Choose three main colors and one accent before you start; it keeps a busy room calm.</li>
      <li><strong>Go big to small.</strong> Color walls and floors first, then furniture, then the details.</li>
      <li><strong>Leave some white.</strong> Unpainted shapes read as light and give the eye a place to rest.</li>
      <li><strong>Add pattern.</strong> Stripes on a cushion or dots on a rug turn a flat page into a designed room.</li>
    </ol>
    <h2 class="reveal">Coloring book questions</h2>{faq_html}
  </article>
  <aside class="aside">
    <div class="panel reveal"><h3>Custom coloring books</h3><p>Kids' menus, hotel welcome packs, event giveaways and branded merch.</p><a class="btn" href="/contact/">Ask about a custom book</a></div>
    <div class="panel reveal"><h3>Read next</h3><ul><li><a href="/set-stylingdirection/">Styling a room for illustration</a></li><li><a href="/thoughts/">More from the journal</a></li></ul></div>
  </aside>
</div></section>
{cta("Want a coloring book of your own?", "Branded or bespoke, we'll draw a book your customers keep long after the visit.")}"""
    write("/coloring-book/", layout("/coloring-book/", "Coloring Book — Hand-Drawn Rooms to Color Online & Print | Ollie Harper",
                                    "Hand-drawn interior coloring pages for adults and kids. Color a room online, download it to print, or commission a custom coloring book.",
                                    body, [crumb, faq_schema, {"@type": "CreativeWork", "name": "Rooms to Color", "genre": "Coloring book",
                                                               "creator": {"@id": ORIGIN + "/#org"}, "url": ORIGIN + "/coloring-book/"}]))


def styling():
    hero, crumb = page_hero([("Home", "/"), ("Styling & Set Direction", "/set-stylingdirection/")], "Prop styling &amp; set direction",
                            "Sets, props and palettes with a story.",
                            "Art direction for shoots, launches and windows — where illustration, props and photography share one look.",
                            "styling", '<div class="hero-actions"><a class="btn" href="/contact/">Plan a shoot <span class="arrow">→</span></a></div>')
    body = f"""{hero}
<section class="section"><div class="wrap layout">
  <article class="prose">
    <h2 class="reveal">Where drawing meets the real world</h2>
    <p>An illustrator's eye is useful long before anything is drawn. Prop styling and set direction is about the same choices we make on paper — color, shape, rhythm, a focal point — made with real objects. We style product and editorial shoots, plan launch-event sets and design window displays so the photography and the illustration look like they belong to the same brand.</p>
    <h2 class="reveal">What set direction covers</h2>
    <ul>
      <li><strong>Concept and mood boards</strong> that lock in palette, props and lighting before the shoot day.</li>
      <li><strong>Prop sourcing and styling</strong> — vintage finds, handmade cut-outs and painted backdrops.</li>
      <li><strong>Illustrated set pieces</strong> — giant paper props, hand-painted flats and custom signage.</li>
      <li><strong>On-set direction</strong> for editorial, catalog and social shoots.</li>
      <li><strong>Window and pop-up design</strong> for retail and events.</li>
    </ul>
    <h2 class="reveal">Our styling kit</h2>
    {gallery([("tile-chair", "The cozy corner"), ("tile-plant", "Always a plant"), ("tile-lamp", "Pattern and light"), ("tile-pencil", "Color first")])}
    <h2 class="reveal">How we plan a set</h2>
    <ol class="steps">
      <li class="reveal"><h3>Story</h3><p>One sentence that describes the moment the picture captures.</p></li>
      <li class="reveal"><h3>Palette</h3><p>Three colors and a texture, pulled from the product.</p></li>
      <li class="reveal"><h3>Props</h3><p>Every object earns its place; we cut anything that competes.</p></li>
      <li class="reveal"><h3>Shoot</h3><p>Styled live on set, with illustrated elements ready to drop in.</p></li>
    </ol>
  </article>
  <aside class="aside">
    <div class="panel reveal"><h3>Great for</h3><ul><li><a href="/contact/">Catalog &amp; e-commerce shoots</a></li><li><a href="/contact/">Magazine editorials</a></li><li><a href="/contact/">Launch events</a></li><li><a href="/contact/">Shop windows</a></li></ul></div>
    <div class="panel reveal"><h3>Related</h3><ul><li><a href="/images/">Fashion &amp; beauty illustration</a></li><li><a href="/coloring-book/">Coloring book</a></li></ul></div>
  </aside>
</div></section>
{cta("Setting the scene for something new?")}"""
    write("/set-stylingdirection/", layout("/set-stylingdirection/", "Prop Styling & Set Direction for Shoots, Launches & Windows | Ollie Harper",
                                           "Prop styling, set design and art direction for product and editorial shoots, launch events and shop windows, with illustrated set pieces.",
                                           body, [crumb, {"@type": "Service", "name": "Prop styling and set direction", "serviceType": "Art direction",
                                                          "provider": {"@id": ORIGIN + "/#org"}, "url": ORIGIN + "/set-stylingdirection/"}]))


def projects():
    hero, crumb = page_hero([("Home", "/"), ("Projects", "/projects/")], "Projects", "How a project comes together.",
                            "From a coffee bar's seasonal drinks to a full coloring book — the kinds of projects we take on, and exactly how each one runs.",
                            "projects")
    types = [
        ("tile-latte", "Seasonal drink launch", "A family of drink illustrations for a café's new seasonal menu: board art, cup sleeve, postcards and social posts, all delivered for launch day.", "c-tomato"),
        ("tile-lipstick", "Beauty product series", "A set of product portraits for a cosmetics launch, each paired with a short personality line for social and packaging inserts.", ""),
        ("tile-croissant", "Illustrated menu", "Cover, section headers and item icons for a bakery or restaurant, supplied in layers so prices and items can change without redrawing.", "c-mustard"),
        ("tile-plant", "Custom coloring book", "A 12–24 page book for a hotel, restaurant or brand, printed as a kids' menu, welcome gift or merch item.", "c-sage"),
        ("tile-sunglasses", "Campaign key art", "One hero illustration adapted for print, out-of-home, web banners and social, with a palette built from the product.", "c-cobalt"),
        ("tile-chair", "Styled shoot", "Concept, props and on-set direction for a catalog or editorial shoot with illustrated set pieces.", ""),
    ]
    cards = ''.join(f'<div class="card reveal {c}"><div class="art">{img(i, t + " illustration")}</div><h3>{t}</h3><p>{d}</p></div>'
                    for i, t, d, c in types)
    body = f"""{hero}
<section class="section"><div class="wrap">
  <div class="section-head"><h2 class="reveal">Projects we love to take on</h2><p class="lede reveal">Scoped to fit independent businesses and big brands alike.</p></div>
  <div class="cards">{cards}</div>
</div></section>
<section class="section alt"><div class="wrap">
  <div class="section-head"><h2 class="reveal">Anatomy of a seasonal latte launch</h2><p class="lede reveal">A typical café commission, start to finish, in about three weeks.</p></div>
  <ol class="steps">
    <li class="reveal"><h3>Taste &amp; brief</h3><p>We visit, taste the new drinks, photograph references and agree where the art will appear.</p></li>
    <li class="reveal"><h3>Roughs</h3><p>Pencil roughs of each drink in two layouts: a hero board and a set of matching spots.</p></li>
    <li class="reveal"><h3>Color</h3><p>A palette pulled from the ingredients — spice, citrus, matcha — applied across the set.</p></li>
    <li class="reveal"><h3>Production</h3><p>Board, sleeve, postcard and social files delivered, plus a short guide for staff posting them.</p></li>
  </ol>
</div></section>
<section class="section"><div class="wrap split">
  <div class="reveal prose"><span class="eyebrow">Working together</span><h2>What to expect</h2>
    <ul><li>A written quote with usage rights spelled out before any drawing starts.</li><li>Two rounds of revisions at the rough stage and one at final.</li>
    <li>Layered source files and print-ready exports for every agreed placement.</li><li>Clear timelines — and we tell you early if anything moves.</li></ul>
    <a class="btn" href="/contact/">Tell us about your project <span class="arrow">→</span></a></div>
  <div class="reveal">{art("culinary")}</div>
</div></section>
{cta()}"""
    write("/projects/", layout("/projects/", "Illustration Projects — Menus, Launches, Coloring Books & Campaigns | Ollie Harper",
                               "The illustration projects Ollie Harper Studio takes on — seasonal drink launches, illustrated menus, beauty series, coloring books and campaign art — and how each one runs.",
                               body, [crumb, {"@type": "CollectionPage", "name": "Projects", "url": ORIGIN + "/projects/", "isPartOf": {"@id": ORIGIN + "/#website"}}]))


POSTS = [
    {
        "slug": "lipstick-theory", "date": "2016-01-04", "modified": TODAY, "color": "#ffd9e2", "art": "lipsticks",
        "title": "Lipstick Theory: What Your Lipstick Shade Says About You",
        "h1": "Lipstick Theory: what your shade says about you",
        "desc": "An illustrated guide to eight classic lipstick shades — red, coral, berry, nude, plum, fuchsia, brick and mauve — and the personality each one suggests.",
        "excerpt": "Eight classic shades, illustrated and read like a horoscope. Which one is yours?",
    },
    {
        "slug": "artsdistrictingredients", "date": "2015-11-14", "modified": TODAY, "color": "#ffe1c4", "art": "map",
        "title": "Arts District Ingredients: How to Illustrate a Neighborhood Food Map",
        "h1": "Arts District Ingredients: drawing a neighborhood food map",
        "desc": "How to research, sketch and design an illustrated neighborhood food map — from eating your way through the district to the final printed postcard set.",
        "excerpt": "Eating your way through a neighborhood, then drawing it: our process for illustrated food maps.",
    },
]

SHADE_NOTES = {
    "Classic Red": "Confident and unbothered. You'd rather make a statement than an excuse.",
    "Coral": "Warm, sunny and approachable — the friend who plans the picnic.",
    "Berry": "Romantic with an edge. You like your sweetness a little dark.",
    "Nude": "Quietly polished. You trust the details to do the talking.",
    "Plum": "Mysterious and thoughtful; the last to leave the bookshop.",
    "Fuchsia": "Playful, loud and impossible to ignore — in the best way.",
    "Brick": "Grounded and stylish, with a soft spot for vintage.",
    "Mauve": "Easygoing and effortlessly put together, day to night.",
}


def post_body(p):
    if p["slug"] == "lipstick-theory":
        shades = ''.join(f'<div class="shade reveal" style="--sw:{c}"><b>{n}</b><span>{SHADE_NOTES[n]}</span></div>' for n, c in SHADES)
        return f"""<p>Few things change a look as fast as lipstick. A deep red for a night out, a sheer nude for every day, a bright fuchsia when the week needs a lift — the shade you reach for says something about your mood, and maybe about you. <em>Lipstick Theory</em> is our illustrated series that takes eight classic shades and reads them like a horoscope. It's not science. It is fun to draw.</p>
<h2>The eight shades</h2>
<div class="shade-grid">{shades}</div>
<h2>Why lipstick is a joy to illustrate</h2>
<p>A lipstick bullet is a perfect little sculpture: a sharp angled tip, a glossy cylinder and a case that tells you everything about the brand. We draw each one with a bold outline, a single highlight and flat, saturated color, so the shade itself is the hero. Because the silhouette stays constant across the series, the color differences do all the work — which is exactly what makes the set read so well on a feed or a printed card.</p>
<h2>Using a series like this for a brand</h2>
<p>Beauty brands use illustrated series to launch a new range, explain a color story or build a "find your shade" quiz. The same eight drawings can become packaging inserts, a social carousel, in-store shelf talkers and an email header — one illustration job, a whole launch's worth of content.</p>
<blockquote>Pick the shade that matches your mood, not your outfit.</blockquote>
<p>Which one are you? Tell us — and if you're launching a beauty line of your own, we'd love to draw it. <a href="/images/">See our fashion &amp; beauty illustration</a>.</p>"""
    return """<p>Some neighborhoods are best understood through your stomach. When we set out to draw an illustrated food map of a downtown arts district, the research phase was mostly lunch — and dinner, and a lot of coffee. Here is how we turn a neighborhood's restaurants, bakeries and bars into a map people actually pin to the fridge.</p>
<h2>1. Eat your way through it</h2>
<p>There is no shortcut. We walk the district at different times of day, order the thing each place is known for and take reference photos of plates, signs and storefronts. The details that end up in the drawings — a blistered pizza crust, a striped awning, a neon sign — come from those visits.</p>
<h2>2. Pick the ingredients, not just the venues</h2>
<p>A good food map is about flavor as much as geography. For each stop we choose one "ingredient" to represent it: a sourdough loaf for the bakery, a pretzel for the beer hall, a scoop for the gelato counter. Those little ingredient icons become the map's visual language and make it scannable at a glance.</p>
<h2>3. Simplify the streets</h2>
<p>Real street grids are messy. We straighten them into friendly blocks, keep only the landmarks people navigate by and leave plenty of room for the illustrations. Accuracy matters for order and direction; exact distances don't.</p>
<h2>4. Color by mood</h2>
<p>We give the map a limited palette pulled from the neighborhood itself — brick, warm concrete, mural colors — and use one bright accent for the pins so every stop pops.</p>
<h2>5. Make it collectible</h2>
<p>The finished map works as a poster, but we also break it into a set of eight postcards, one per stop. Visitors collect them, venues hand them out, and the neighborhood gets a piece of marketing people keep.</p>
<blockquote>The best way to draw a neighborhood is to be hungry in it.</blockquote>
<p>Thinking about a food map for your district, hotel or tourism board? <a href="/culinary/">See our culinary illustration</a> or <a href="/contact/">get in touch</a>.</p>"""


def thoughts():
    for p in POSTS:
        path = f"/thoughts/{p['slug']}/"
        crumbs, crumb_schema = breadcrumbs([("Home", "/"), ("Thoughts", "/thoughts/"), (p["h1"].split(":")[0], path)])
        others = ''.join(f'<li><a href="/thoughts/{o["slug"]}/">{escape(o["h1"])}</a></li>' for o in POSTS if o is not p)
        body = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr">
  <div>{crumbs}<span class="eyebrow">Thoughts · <time datetime="{p['date']}">{date.fromisoformat(p['date']).strftime('%B %-d, %Y')}</time></span><h1>{escape(p['h1'])}</h1><p class="lede">{escape(p['desc'])}</p></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap layout">
  <article class="prose"><div class="reveal" style="margin-bottom:2rem">{art(p['art'])}</div>{post_body(p)}</article>
  <aside class="aside"><div class="panel reveal"><h3>More thoughts</h3><ul>{others}<li><a href="/thoughts/">All journal posts</a></li></ul></div>
  <div class="panel ink reveal"><h3>Like this style?</h3><p>We draw series like this for brands.</p><a class="btn" href="/contact/">Commission a series</a></div></aside>
</div></section>
{cta()}"""
        article = {"@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "datePublished": p["date"],
                   "dateModified": p["modified"], "author": {"@id": ORIGIN + "/#org"}, "publisher": {"@id": ORIGIN + "/#org"},
                   "mainEntityOfPage": ORIGIN + path, "image": f"{ORIGIN}/assets/photos/{p['art']}-960.webp"}
        write(path, layout(path, f"{p['title']} | Ollie Harper", p["desc"], body, [crumb_schema, article], og_type="article", current="/thoughts/"))

    hero, crumb = page_hero([("Home", "/"), ("Thoughts", "/thoughts/")], "The journal", "Thoughts, sketches &amp; ingredients.",
                            "Notes from the drawing table: illustrated series, process write-ups and the things we can't stop drawing.", "thoughts")
    cards = ''.join(f'<a class="post-card reveal" href="/thoughts/{p["slug"]}/" style="--c:{p["color"]}"><div class="art">{img(p["art"], p["h1"], 680, 300)}</div>'
                    f'<div class="body"><time datetime="{p["date"]}">{date.fromisoformat(p["date"]).strftime("%B %Y")}</time><h3>{escape(p["h1"])}</h3><p>{escape(p["excerpt"])}</p></div></a>'
                    for p in POSTS)
    body = f"""{hero}
<section class="section" style="padding-top:0"><div class="wrap"><div class="posts">{cards}</div></div></section>
{cta("Want something drawn?")}"""
    write("/thoughts/", layout("/thoughts/", "Thoughts — The Ollie Harper Illustration Journal",
                               "The Ollie Harper Studio journal: illustrated series like Lipstick Theory, food-map process notes and sketches from the drawing table.",
                               body, [crumb, {"@type": "Blog", "name": "Thoughts", "url": ORIGIN + "/thoughts/", "publisher": {"@id": ORIGIN + "/#org"}}]))


def about():
    hero, crumb = page_hero([("Home", "/"), ("About", "/about/")], "About the studio", "Small studio. Big color.",
                            "Ollie Harper is an independent illustration studio for brands that want artwork with warmth, wit and an appetite for color.", "about")
    body = f"""{hero}
<section class="section" style="padding-top:0"><div class="wrap layout">
  <article class="prose">
    <h2 class="reveal">What we believe</h2>
    <p>Illustration should make people feel something before they've read a word. We draw food you can almost taste, fashion with attitude and rooms you want to live in — always by hand first, then finished digitally so the work holds up everywhere it needs to go.</p>
    <p>We're a deliberately small studio. That means the person you brief is the person who draws, and every project gets a real conversation rather than a template.</p>
    <h2 class="reveal">What we make</h2>
    <ul><li><a href="/">Commercial illustration</a> for campaigns, packaging and editorial</li><li><a href="/culinary/">Culinary illustration</a> for restaurants, cafés and food brands</li>
    <li><a href="/images/">Fashion &amp; beauty illustration</a></li><li><a href="/coloring-book/">Coloring books</a>, standard and custom</li>
    <li><a href="/set-stylingdirection/">Prop styling &amp; set direction</a></li></ul>
    <h2 class="reveal">A note on this website</h2>
    <p>Ollie Harper Studio relaunched in {date.today().year} under new ownership. The studio is not affiliated with any illustrator or business that previously used this web address, and the photography used across the site is royalty-free (CC0) stock imagery for mood and reference, not client work.</p>
  </article>
  <aside class="aside"><div class="panel ink reveal"><h3>Say hello</h3><p>New projects, collaborations or just a favorite lipstick shade.</p><a class="btn" href="/contact/">Contact</a></div></aside>
</div></section>
{cta()}"""
    write("/about/", layout("/about/", "About Ollie Harper Studio — Independent Illustration Studio",
                            "About Ollie Harper Studio: an independent illustration studio drawing food, fashion, beauty, interiors and coloring books for brands.",
                            body, [crumb, {"@type": "AboutPage", "url": ORIGIN + "/about/", "about": {"@id": ORIGIN + "/#org"}}]))


def contact():
    hero, crumb = page_hero([("Home", "/"), ("Contact", "/contact/")], "Contact", "Let's make something delicious.",
                            f"Tell us what you're making and where it'll live. We reply within two working days. Prefer email? <a href=\"mailto:{EMAIL}\">{EMAIL}</a>",
                            "contact")
    body = f"""{hero}
<section class="section alt"><div class="wrap layout">
  <form class="form reveal" data-mailto="{EMAIL}">
    <div class="row"><label>Name<input name="name" required autocomplete="name"></label><label>Email<input name="email" type="email" required autocomplete="email"></label></div>
    <div class="row"><label>Company<input name="company" autocomplete="organization"></label>
      <label>Project type<select name="project"><option>Commercial / campaign</option><option>Culinary / menu</option><option>Fashion &amp; beauty</option>
      <option>Coloring book</option><option>Prop styling / set direction</option><option>Something else</option></select></label></div>
    <div class="row"><label>Timeline<input name="timeline" placeholder="e.g. launch in March"></label><label>Budget range<select name="budget"><option>Not sure yet</option><option>Under $1,000</option><option>$1,000–$5,000</option><option>$5,000+</option></select></label></div>
    <label>Tell us about it<textarea name="details" rows="6" required placeholder="What is it for, where will it appear, and what should it feel like?"></textarea></label>
    <button class="btn" type="submit">Send brief <span class="arrow">→</span></button>
    <p class="form-note">Sending opens your email app with the brief filled in — nothing is stored on this site.</p>
  </form>
  <aside class="aside">
    <div class="panel reveal"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    <div class="panel reveal"><h3>Good to include</h3><ul><li><a href="/projects/">Where the art will be used</a></li><li><a href="/projects/">Launch or print dates</a></li><li><a href="/projects/">Any brand guidelines</a></li></ul></div>
  </aside>
</div></section>"""
    write("/contact/", layout("/contact/", "Contact Ollie Harper Studio — Commission an Illustration",
                              "Commission an illustration from Ollie Harper Studio. Send a brief for menus, packaging, campaigns, fashion and beauty art, coloring books or set styling.",
                              body, [crumb, {"@type": "ContactPage", "url": ORIGIN + "/contact/", "about": {"@id": ORIGIN + "/#org"}}]))


def privacy():
    crumbs, crumb = breadcrumbs([("Home", "/"), ("Privacy Policy", "/privacy-policy/")])
    body = f"""<section class="page-hero"><div class="wrap" style="grid-template-columns:1fr"><div>{crumbs}<h1>Privacy policy</h1><p class="lede">Last updated {TODAY}.</p></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap prose">
<p>This website is a portfolio and does not use accounts, cookies for advertising or third-party tracking scripts.</p>
<h2>Information you send us</h2><p>The contact form does not submit data to this website. It opens your own email app with your message pre-filled; we receive only what you choose to send, and use it only to reply and to quote for your project.</p>
<h2>Server logs</h2><p>Our hosting provider keeps standard server logs (IP address, browser, pages requested) for security and performance. They are not used to identify visitors.</p>
<h2>Fonts</h2><p>Typefaces are loaded from Google Fonts, which receives your IP address when the fonts download.</p>
<h2>Contact</h2><p>Questions about privacy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    write("/privacy-policy/", layout("/privacy-policy/", "Privacy Policy | Ollie Harper Studio",
                                     "How Ollie Harper Studio handles information sent through this website.", body, [crumb]))


def error_pages():
    for name, code, title, msg in (
        ("404.html", "404", "Page not found", "This page wandered off the sketchbook. Try one of these instead."),
        ("410.html", "410", "This page is gone", "That page no longer exists on Ollie Harper Studio and won't be coming back."),
    ):
        body = f"""<section class="section notfound"><div class="wrap"><h1>{code}</h1><h2>{title}</h2><p class="lede" style="margin:0 auto 2rem">{msg}</p>
<div class="hero-actions" style="justify-content:center"><a class="btn" href="/">Home</a><a class="btn ghost" href="/culinary/">Culinary</a><a class="btn ghost" href="/coloring-book/">Coloring book</a></div></div></section>"""
        html = layout("/", f"{title} | Ollie Harper Studio", msg, body).replace(
            '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
        html = html.replace(f'<link rel="canonical" href="{ORIGIN}/">\n', '')
        (ROOT / name).write_text(html, encoding="utf-8")


def assets():
    (ROOT / "favicon.svg").write_text(FAVICON, encoding="utf-8")


def sitemap_and_robots():
    urls = ''.join(f"<url><loc>{ORIGIN}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    robots = ("User-agent: *\nDisallow: /\n" if STAGING else
              f"User-agent: *\nDisallow: /home.html\nDisallow: /*.php$\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


if __name__ == "__main__":
    assets()
    home(); culinary(); fashion(); coloring(); styling(); projects(); thoughts(); about(); contact(); privacy()
    error_pages()
    sitemap_and_robots()
    print(f"built {len(PAGES)} pages ({'STAGING noindex' if STAGING else 'production'})")
