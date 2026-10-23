#!/usr/bin/env python3
"""Static site generator for dogearcleaner.com.

Reads article bodies from content/posts and content/pages (format in
CONTENT_SPEC.md), wraps them in the shared layout, expands affiliate/tool
shortcodes, and writes the deployable site into ./site/. Standard library only,
plus Pillow for image resizing (skipped if images are already built).

    python3 build.py && python3 validate.py
"""

import html
import json
import math
import re
import shutil
from pathlib import Path

from products import ACCESSORIES, AMAZON_TAG, PRODUCTS, amazon_search_url
from siteconfig import AUTHOR, CATEGORIES, NAV, SITE, TODAY
import pages as P
import tools as T

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "site"
SRC = ROOT / "src"
ORIGIN = SITE["origin"]
ASSET_VER = TODAY.replace("-", "")

esc = html.escape

# Google Analytics 4 (property G-FCFG03CMQB), emitted on every page by layout().
GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-FCFG03CMQB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-FCFG03CMQB');
</script>
"""


# --------------------------------------------------------------------------- content loading

def load_dir(d):
    items = {}
    for f in sorted((ROOT / "content" / d).glob("*.html")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta(.*?)-->", text, re.S)
        if not m:
            raise SystemExit(f"{f}: missing <!--meta ... --> block")
        meta = json.loads(m.group(1))
        meta["slug"] = f.stem
        meta["path"] = f"/{f.stem}/"
        meta["body"] = text[m.end():].strip()
        meta.setdefault("updated", TODAY)
        items[f.stem] = meta
    return items


# --------------------------------------------------------------------------- shortcodes

def product_card(key, compact=False):
    p = PRODUCTS[key]
    review = (f'<a class="pc-review" href="{p["review"]}">Read our full review</a>'
              if p["review"] else "")
    cls = "product-card compact" if compact else "product-card"
    return (f'<div class="{cls}">'
            f'<div class="pc-body"><span class="pc-brand">{esc(p["brand"])}</span>'
            f'<p class="pc-name">{esc(p["name"])}</p>'
            f'<p class="pc-best">{esc(p["best_for"])}</p>'
            f'<div class="pc-actions"><a class="btn-amazon" href="{p["url"]}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a>{review}</div>'
            f'</div></div>')


TAG_LABELS = {
    "alcohol-free": "Alcohol-free", "drying": "Drying agents", "ph-balanced": "pH-balanced",
    "vet-brand": "Vet-clinic brand", "enzymatic": "Enzymatic", "gentle": "Gentle",
    "hydrocortisone": "Hydrocortisone", "treatment": "Treatment", "no-sting": "No-sting",
    "hypochlorous": "Hypochlorous", "tris-edta": "Tris-EDTA", "budget": "Budget",
    "scented": "Scented", "wipes": "Wipes", "aloe": "Aloe", "natural": "Plant-based",
    "probiotic": "Probiotic", "ketoconazole": "Ketoconazole",
}


def compare_table(keys):
    rows = []
    for k in keys:
        p = PRODUCTS[k]
        tags = " ".join(f'<span class="tag">{TAG_LABELS.get(t, t)}</span>' for t in p["tags"])
        name = (f'<a href="{p["review"]}">{esc(p["name"])}</a>' if p["review"] else esc(p["name"]))
        rows.append(f'<tr><td data-label="Product"><strong>{name}</strong></td>'
                    f'<td data-label="Best for">{esc(p["best_for"])}</td>'
                    f'<td data-label="Highlights">{tags}</td>'
                    f'<td data-label="Buy"><a class="btn-amazon sm" href="{p["url"]}" rel="nofollow sponsored noopener" target="_blank">View on Amazon</a></td></tr>')
    return ('<div class="table-wrap"><table class="data compare"><thead><tr><th>Product</th><th>Best for</th>'
            '<th>Highlights</th><th>Buy</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')


def cta_banner():
    p = PRODUCTS["epi-otic"]
    return ('<aside class="cta-banner"><div><p class="cta-kicker">Dog Ear Cleaner top pick</p>'
            '<p class="cta-title">Virbac Epi-Otic Advanced Ear Cleanser</p>'
            '<p>Gentle, alcohol-free and the cleaner vets hand out most. Not sure it fits your dog? '
            '<a href="/best-dog-ear-cleaner/">Compare the best dog ear cleaners</a>.</p></div>'
            f'<a class="btn-amazon" href="{p["url"]}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a></aside>')


def expand(body):
    def block(m):
        kind, arg = m.group(1), m.group(2)
        if kind == "product":
            return product_card(arg.strip())
        if kind == "compare":
            return compare_table([k.strip() for k in arg.split(",")])
        if kind == "tool":
            return T.render(arg.strip())
        raise SystemExit(f"unknown block shortcode {kind}")

    body = re.sub(r"(?:<p>\s*)?\[\[(product|compare|tool):([^\]]+)\]\](?:\s*</p>)?", block, body)
    body = re.sub(r"(?:<p>\s*)?\[\[cta\]\](?:\s*</p>)?", lambda m: cta_banner(), body)

    def inline(m):
        kind, key, text = m.group(1), m.group(2).strip(), m.group(3)
        if kind == "amazon":
            url = PRODUCTS[key]["url"]
        else:
            q = ACCESSORIES[key][1] if key in ACCESSORIES else key
            url = amazon_search_url(q)
        return f'<a class="aff" href="{url}" rel="nofollow sponsored noopener" target="_blank">{text}</a>'

    body = re.sub(r"\[\[(amazon|amazon-search):([^|\]]+)\|([^\]]+)\]\]", inline, body)
    # Wrap bare article tables so they scroll sideways on phones instead of widening the page.
    body = re.sub(r"(?<!<div class=\"table-wrap\">)(<table\b.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)
    left = re.findall(r"\[\[[^\]]*\]\]", body)
    if left:
        raise SystemExit(f"unexpanded shortcodes: {left}")
    return body


def slugify(s):
    s = re.sub(r"<[^>]+>", "", html.unescape(s)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def add_heading_ids(body):
    """Give every h2 an id and return (body, toc entries)."""
    toc, seen = [], set()

    def rep(m):
        attrs, inner = m.group(1), m.group(2)
        if "id=" in attrs:
            hid = re.search(r'id="([^"]+)"', attrs).group(1)
        else:
            hid = slugify(inner) or "section"
            while hid in seen:
                hid += "-2"
        seen.add(hid)
        if re.sub(r"<[^>]+>", "", inner).strip().lower() != "key takeaways":
            toc.append((hid, re.sub(r"<[^>]+>", "", inner)))
        return f'<h2 id="{hid}"{re.sub(r" id=\"[^\"]+\"", "", attrs)}>{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S)
    return body, toc


def word_count(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


# --------------------------------------------------------------------------- layout

def org_schema():
    return [
        {"@type": "Organization", "@id": f"{ORIGIN}/#org", "name": SITE["name"], "url": f"{ORIGIN}/",
         "logo": {"@type": "ImageObject", "url": ORIGIN + SITE["logo"], "width": 1968, "height": 360},
         "description": SITE["tagline"]},
        {"@type": "WebSite", "@id": f"{ORIGIN}/#website", "name": SITE["name"], "url": f"{ORIGIN}/",
         "publisher": {"@id": f"{ORIGIN}/#org"}, "inLanguage": "en-US"},
    ]


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + u}
        for i, (n, u) in enumerate(crumbs)]}


def breadcrumbs_html(crumbs):
    parts = []
    for i, (n, u) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <span class="sep">/</span> '.join(parts) + '</nav>'


def header_html(path):
    links = "".join(
        f'<li><a href="{u}"{" aria-current=\"page\"" if path.startswith(u) else ""}>{n}</a></li>' for n, u in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">Free tools: <a href="/tools/ear-symptom-checker/">ear symptom checker</a> &middot; <a href="/tools/ear-cleaning-schedule/">cleaning schedule</a> &middot; <a href="/tools/ear-cleaner-finder/">ear cleaner finder</a></div></div>
<header class="site-header"><div class="wrap header-row">
<a class="brand" href="/" aria-label="Dog Ear Cleaner home"><img src="/assets/img/Dog-Ear-Cleaner-Logo.webp" alt="Dog Ear Cleaner" width="230" height="42"></a>
<button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
<nav id="site-nav" class="site-nav" aria-label="Main"><ul>{links}</ul></nav>
</div></header>'''


def footer_html():
    reviews = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [
        ("Best Dog Ear Cleaners", "/best-dog-ear-cleaner/"),
        ("Virbac Epi-Otic Review", "/virbac-epi-otic-flush-review/"),
        ("Zymox Ear Cleanser Review", "/zymox-ear-cleanser-review/"),
        ("Vetericyn Plus Ear Rinse Review", "/vetericyn-plus-ear-rinse-review/"),
        ("Pet MD Ear Flush Review", "/pet-md-ear-flush-review/")])
    guides = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [
        ("How to Clean Dog Ears", "/how-to-clean-dog-earss-matters/"),
        ("Dog Ear Infection Signs", "/ear-infection-signs/"),
        ("Ear Cleaning Routines", "/cleaning-routines/"),
        ("Floppy-Ear Breeds", "/floppy-ear-breeds/"),
        ("After-Bath Ear Care", "/after-bath-care/"),
        ("All Articles", "/resources/")])
    tools = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [
        ("Ear Symptom Checker", "/tools/ear-symptom-checker/"),
        ("Cleaning Schedule Calculator", "/tools/ear-cleaning-schedule/"),
        ("Ear Cleaner Finder Quiz", "/tools/ear-cleaner-finder/"),
        ("Ear Cleaner Dose Calculator", "/tools/ear-cleaner-dose-calculator/")])
    site = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [
        ("About Us", "/about-us/"), ("Contact Us", "/contact-us/"),
        ("Affiliate Disclosure", "/affiliate-disclosure/"), ("Disclaimer", "/disclaimer/"),
        ("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/")])
    return f'''<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div class="footer-about"><img src="/assets/img/Dog-Ear-Cleaner-Logo-Alt.webp" alt="Dog Ear Cleaner" width="200" height="37" loading="lazy">
<p>Dog Ear Cleaner is an independent resource for safe, simple dog ear care: step-by-step cleaning guides, honest ear cleaner reviews and free interactive tools.</p>
<p class="small">Our content is educational and is not a substitute for veterinary care. If your dog's ear is painful, swollen, bleeding or your dog is tilting its head, see a vet.</p></div>
<div><p class="footer-h">Reviews</p><ul>{reviews}</ul></div>
<div><p class="footer-h">Guides</p><ul>{guides}</ul></div>
<div><p class="footer-h">Free Tools</p><ul>{tools}</ul><p class="footer-h">Site</p><ul>{site}</ul></div>
</div>
<p class="footer-legal">As an Amazon Associate, Dog Ear Cleaner earns from qualifying purchases. &copy; {TODAY[:4]} Dog Ear Cleaner. All rights reserved.</p>
</div></footer>'''


def layout(*, path, title, description, body, schema=(), og_type="website", image=None,
           noindex=False, extra_head="", body_class=""):
    canonical = ORIGIN + path
    img = ORIGIN + (image or SITE["social_image"])
    graph = {"@context": "https://schema.org", "@graph": org_schema() + list(schema)}
    robots = '<meta name="robots" content="noindex,follow">' if noindex else \
        '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">'
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GA_TAG}<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Dog Ear Cleaner">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{img}">
{extra_head}<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#2f7466">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_VER}">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body class="{body_class}">
{header_html(path)}
<main id="main">
{body}
</main>
{footer_html()}
<script src="/assets/js/site.js?v={ASSET_VER}" defer></script>
</body>
</html>
'''


# --------------------------------------------------------------------------- shared pieces

def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def img_tag(name, alt, size="full", eager=False, cls=""):
    base = "/assets/img/" if size == "full" else "/assets/img/thumb/"
    w, h = (1200, 800) if size == "full" else (600, 400)
    if name.startswith("Dog-Ear-Cleaner-Site-Image"):
        h = 675 if size == "full" else 338
    if name.startswith("Dog-Ear-Cleaner-Hero-Image"):
        w, h = (900, 600) if size == "full" else (600, 400)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{base}{name}" alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async">'


def post_card(p):
    cat = CATEGORIES[p["category"]]
    return (f'<article class="card"><a class="card-img" href="{p["path"]}">{img_tag(p["image"], p["image_alt"], "thumb")}</a>'
            f'<div class="card-body"><a class="card-cat" href="{cat["path"]}">{cat["short"]}</a>'
            f'<h3><a href="{p["path"]}">{esc(p["h1"])}</a></h3><p>{esc(p["excerpt"])}</p>'
            f'<a class="card-more" href="{p["path"]}">Read more <span aria-hidden="true">&rarr;</span></a></div></article>')


def faq_html(faq, heading="Frequently asked questions"):
    items = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    return f'<section class="faq"><h2 id="faq">{heading}</h2>{items}</section>'


def faq_schema(faq, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


def disclosure_note():
    return ('<p class="disclosure"><strong>Affiliate note:</strong> Dog Ear Cleaner is reader-supported. '
            'We may earn a commission when you buy through links on this page, at no extra cost to you. '
            '<a href="/affiliate-disclosure/">Learn more</a>.</p>')


def stars(rating):
    full = int(rating)
    half = rating - full >= 0.25
    s = "★" * full + ("½" if half else "")
    return f'<span class="stars" aria-label="{rating} out of 5">{s}</span>'


def review_box(rv):
    p = PRODUCTS[rv["product"]]
    pros = "".join(f"<li>{esc(x)}</li>" for x in rv["pros"])
    cons = "".join(f"<li>{esc(x)}</li>" for x in rv["cons"])
    return (f'<section class="verdict" aria-label="Our verdict"><div class="verdict-head">'
            f'<div class="score"><span class="score-num">{rv["rating"]:.1f}</span><span class="score-of">/ 5</span>{stars(rv["rating"])}</div>'
            f'<div><p class="verdict-kicker">Dog Ear Cleaner verdict</p><p class="verdict-text">{esc(rv["verdict"])}</p></div></div>'
            f'<div class="proscons"><div class="pros"><p class="pc-h">What we like</p><ul>{pros}</ul></div>'
            f'<div class="cons"><p class="pc-h">Watch-outs</p><ul>{cons}</ul></div></div>'
            f'<a class="btn-amazon wide" href="{p["url"]}" rel="nofollow sponsored noopener" target="_blank">Check the current price on Amazon</a></section>')


def sidebar(current_path):
    links = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [
        ("Ear symptom checker", "/tools/ear-symptom-checker/"),
        ("How often to clean ears", "/tools/ear-cleaning-schedule/"),
        ("Find the right ear cleaner", "/tools/ear-cleaner-finder/"),
        ("How much cleaner to use", "/tools/ear-cleaner-dose-calculator/")])
    return (f'<aside class="sidebar"><div class="side-box"><p class="side-h">Our top pick</p>{product_card("epi-otic", compact=True)}</div>'
            f'<div class="side-box"><p class="side-h">Free dog ear tools</p><ul class="side-links">{links}</ul></div>'
            f'<div class="side-box side-vet"><p class="side-h">When to call the vet</p><p>Head tilt, loss of balance, a swollen ear flap, bleeding, or yelping when the ear is touched? Skip the cleaner and call your vet today.</p>'
            f'<a href="/ear-infection-signs/">See all warning signs</a></div></aside>')


def toc_html(toc):
    if len(toc) < 3:
        return ""
    items = "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc)
    return f'<details class="toc" open><summary>In this article</summary><ol>{items}</ol></details>'


# --------------------------------------------------------------------------- page renderers

def render_post(p, posts):
    url = ORIGIN + p["path"]
    cat = CATEGORIES[p["category"]]
    crumbs = [("Home", "/"), (cat["short"], cat["path"]), (p["h1"] if len(p["h1"]) < 60 else p["title"].split(":")[0], p["path"])]
    body = expand(p["body"])
    body, toc = add_heading_ids(body)
    faq = p.get("faq", [])
    if faq:
        toc.append(("faq", "Frequently asked questions"))
    words = word_count(body) + sum(word_count(q + " " + a) for q, a in faq)
    minutes = max(3, math.ceil(words / 230))
    related = [x for x in posts.values() if x["slug"] != p["slug"] and x["category"] == p["category"]]
    related += [x for x in posts.values() if x["slug"] != p["slug"] and x["category"] != p["category"]]
    related_html = "".join(post_card(x) for x in related[:3])
    rv = p.get("review")
    article = f'''<div class="wrap article-layout">
<article class="article">
{breadcrumbs_html(crumbs)}
<header class="article-head">
<a class="card-cat" href="{cat["path"]}">{cat["short"]}</a>
<h1>{esc(p["h1"])}</h1>
<p class="byline">By <a href="{AUTHOR["url"]}">{AUTHOR["name"]}</a> &middot; Updated <time datetime="{p["updated"]}">{fmt_date(p["updated"])}</time> &middot; {minutes} min read</p>
</header>
{disclosure_note()}
<figure class="hero-fig">{img_tag(p["image"], p["image_alt"], eager=True)}</figure>
{review_box(rv) if rv else ""}
{toc_html(toc)}
<div class="prose">
{body}
{faq_html(faq) if faq else ""}
</div>
<div class="author-box"><img src="/assets/img/Dog-Ear-Cleaner-Site-Icon.webp" alt="" width="64" height="64" loading="lazy"><div><p class="author-name">{AUTHOR["name"]}</p><p>{AUTHOR["bio"]} <a href="/about-us/">How we research</a>.</p></div></div>
</article>
{sidebar(p["path"])}
</div>
<section class="related"><div class="wrap"><h2>Keep reading</h2><div class="card-grid">{related_html}</div></div></section>'''
    schema = [breadcrumb_schema(crumbs), {
        "@type": "BlogPosting", "@id": url + "#article", "headline": p["h1"][:110],
        "description": p["description"], "image": ORIGIN + "/assets/img/" + p["image"],
        "datePublished": p["published"], "dateModified": p["updated"], "wordCount": words,
        "author": {"@type": "Organization", "name": AUTHOR["name"], "url": ORIGIN + AUTHOR["url"]},
        "publisher": {"@id": f"{ORIGIN}/#org"}, "mainEntityOfPage": url,
        "articleSection": cat["short"], "keywords": ", ".join([p["keyword"]] + p.get("secondary", [])),
        "inLanguage": "en-US"}]
    if faq:
        schema.append(faq_schema(faq, url))
    if rv:
        prod = PRODUCTS[rv["product"]]
        schema.append({
            "@type": "Product", "@id": url + "#product", "name": prod["name"],
            "brand": {"@type": "Brand", "name": prod["brand"]}, "sku": prod["asin"],
            "image": ORIGIN + "/assets/img/" + p["image"],
            "review": {"@type": "Review", "name": p["h1"], "url": url,
                       "author": {"@type": "Organization", "name": SITE["name"], "url": ORIGIN + "/"},
                       "datePublished": p["published"], "reviewBody": rv["verdict"],
                       "reviewRating": {"@type": "Rating", "ratingValue": rv["rating"], "bestRating": 5, "worstRating": 1},
                       "positiveNotes": {"@type": "ItemList", "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "name": x} for i, x in enumerate(rv["pros"])]},
                       "negativeNotes": {"@type": "ItemList", "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "name": x} for i, x in enumerate(rv["cons"])]}}})
    return layout(path=p["path"], title=p["title"], description=p["description"], body=article,
                  schema=schema, og_type="article", image="/assets/img/" + p["image"],
                  extra_head=f'<meta property="article:published_time" content="{p["published"]}">\n'
                             f'<meta property="article:modified_time" content="{p["updated"]}">\n'
                             + (T.data_script() if "data-tool=" in body else ""))


def render_page(p):
    """Static info pages (about, legal, contact)."""
    url = ORIGIN + p["path"]
    crumbs = [("Home", "/"), (p["h1"], p["path"])]
    body = expand(p["body"])
    body, toc = add_heading_ids(body)
    faq = p.get("faq", [])
    content = f'''<div class="page-hero"><div class="wrap narrow">{breadcrumbs_html(crumbs)}<h1>{esc(p["h1"])}</h1>
{f'<p class="page-intro">{esc(p["intro"])}</p>' if p.get("intro") else ""}
{f'<p class="byline">Last updated <time datetime="{p["updated"]}">{fmt_date(p["updated"])}</time></p>' if p.get("show_updated") else ""}</div></div>
<div class="wrap narrow prose page-prose">
{body}
{faq_html(faq) if faq else ""}
</div>'''
    schema = [breadcrumb_schema(crumbs), {"@type": p.get("schema_type", "WebPage"), "@id": url, "url": url,
                                          "name": p["title"], "description": p["description"],
                                          "isPartOf": {"@id": f"{ORIGIN}/#website"}}]
    if faq:
        schema.append(faq_schema(faq, url))
    return layout(path=p["path"], title=p["title"], description=p["description"], body=content, schema=schema)


def render_listing(path, title, description, h1, intro, items, crumbs, item_list_name):
    url = ORIGIN + path
    cards = "".join(post_card(x) for x in items)
    body = f'''<div class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<h1>{esc(h1)}</h1><p class="page-intro">{esc(intro)}</p></div></div>
<div class="wrap listing"><div class="card-grid">{cards}</div>
<aside class="listing-tools"><h2>Free dog ear care tools</h2>{T.tool_grid()}</aside></div>'''
    schema = [breadcrumb_schema(crumbs),
              {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": description,
               "isPartOf": {"@id": f"{ORIGIN}/#website"},
               "mainEntity": {"@type": "ItemList", "name": item_list_name, "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "url": ORIGIN + x["path"], "name": x["h1"]}
                   for i, x in enumerate(items)]}}]
    return layout(path=path, title=title, description=description, body=body, schema=schema)


def render_tool_page(t):
    url = ORIGIN + t["path"]
    crumbs = [("Home", "/"), ("Free Tools", "/tools/"), (t["name"], t["path"])]
    body = f'''<div class="page-hero tool-hero"><div class="wrap narrow">{breadcrumbs_html(crumbs)}<h1>{esc(t["h1"])}</h1><p class="page-intro">{esc(t["intro"])}</p></div></div>
<div class="wrap narrow">
{T.render(t["key"], standalone=True)}
<div class="prose page-prose">{expand(t["body"])}
{faq_html(t["faq"])}</div>
<h2 class="more-tools-h">More free tools from Dog Ear Cleaner</h2>
{T.tool_grid(exclude=t["key"])}
</div>'''
    schema = [breadcrumb_schema(crumbs),
              {"@type": "WebApplication", "@id": url + "#app", "name": t["name"], "url": url,
               "applicationCategory": "HealthApplication", "operatingSystem": "Any (web browser)",
               "browserRequirements": "Requires JavaScript",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
               "description": t["description"], "publisher": {"@id": f"{ORIGIN}/#org"}},
              faq_schema(t["faq"], url)]
    return layout(path=t["path"], title=t["title"], description=t["description"], body=body,
                  schema=schema, extra_head=T.data_script())


def render_tools_hub():
    path = "/tools/"
    crumbs = [("Home", "/"), ("Free Tools", path)]
    title = "Free Dog Ear Care Tools: Symptom Checker & Calculators"
    desc = ("Free dog ear care tools from Dog Ear Cleaner: an ear symptom checker, cleaning schedule "
            "calculator, ear cleaner finder quiz and a dose calculator. No sign-up.")
    body = f'''<div class="page-hero"><div class="wrap">{breadcrumbs_html(crumbs)}<h1>Free Dog Ear Care Tools</h1>
<p class="page-intro">Four quick, free tools from Dog Ear Cleaner to help you decide what your dog's ears need today: whether to clean or call the vet, how often to clean, which cleaner fits, and how much to use. Everything runs in your browser; nothing is stored or sent anywhere.</p></div></div>
<div class="wrap">{T.tool_grid(large=True)}
<div class="prose narrow page-prose"><h2>How these tools work</h2>
<p>Each tool turns the advice in our guides into a few quick questions. The answers come from the same sources we use for every Dog Ear Cleaner article: manufacturer directions, published veterinary guidance on ear care, and the patterns we see in owner feedback. They are planning aids, not a diagnosis. If anything about your dog's ear worries you, a vet visit beats any online tool.</p>
<p>Prefer to read? Start with <a href="/how-to-clean-dog-earss-matters/">how to clean dog ears</a>, check the <a href="/ear-infection-signs/">signs of a dog ear infection</a>, or jump to <a href="/best-dog-ear-cleaner/">the best dog ear cleaners</a>.</p></div></div>'''
    schema = [breadcrumb_schema(crumbs), {"@type": "CollectionPage", "@id": ORIGIN + path, "url": ORIGIN + path,
              "name": title, "description": desc, "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": ORIGIN + t["path"], "name": t["name"]}
                  for i, t in enumerate(T.TOOLS.values())]}}]
    return layout(path=path, title=title, description=desc, body=body, schema=schema)


def render_404():
    body = '''<div class="page-hero"><div class="wrap narrow"><h1>Page not found</h1>
<p class="page-intro">Sorry, that page has wandered off. Try one of these instead:</p></div></div>
<div class="wrap narrow prose page-prose"><ul>
<li><a href="/">Dog Ear Cleaner home</a></li>
<li><a href="/best-dog-ear-cleaner/">The best dog ear cleaners</a></li>
<li><a href="/how-to-clean-dog-earss-matters/">How to clean dog ears</a></li>
<li><a href="/virbac-epi-otic-flush-review/">Virbac Epi-Otic review</a></li>
<li><a href="/tools/">Free dog ear care tools</a></li>
<li><a href="/resources/">All articles</a></li></ul></div>'''
    return layout(path="/404.html", title="Page Not Found | Dog Ear Cleaner",
                  description="The page you were looking for could not be found.", body=body, noindex=True)


# --------------------------------------------------------------------------- assets

def build_images():
    out_full, out_thumb = OUT / "assets/img", OUT / "assets/img/thumb"
    out_full.mkdir(parents=True, exist_ok=True)
    out_thumb.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
    except ImportError:
        Image = None
    for f in sorted((SRC / "img").glob("*.webp")):
        if f.name.startswith("Dog-Ear-Cleaner-Logo") or f.name.startswith("Dog-Ear-Cleaner-Site-Icon"):
            shutil.copy2(f, out_full / f.name)
            continue
        for dest, width in ((out_full / f.name, 1200), (out_thumb / f.name, 600)):
            if dest.exists() and dest.stat().st_mtime >= f.stat().st_mtime:
                continue
            if Image is None:
                shutil.copy2(f, dest)
                continue
            im = Image.open(f)
            if im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            if dest.parent == out_thumb and im.height > 400 and width == 600:
                top = (im.height - 400) // 2
                im = im.crop((0, top, 600, top + 400))
            im.save(dest, "WEBP", quality=80, method=6)
    # Old WordPress media URLs keep working (Google Images, external links).
    legacy = OUT / "wp-content/uploads/2026/05"
    legacy.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "backup/wordpress-2026-10-23/media").glob("*.webp"):
        shutil.copy2(f, legacy / f.name)
    # Favicons from the site icon.
    icon_src = SRC / "img/Dog-Ear-Cleaner-Site-Icon.webp"
    if Image and not (OUT / "favicon.ico").exists():
        im = Image.open(icon_src).convert("RGBA")
        im.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
        for name, s in (("favicon-32x32.png", 32), ("apple-touch-icon.png", 180),
                        ("web-app-manifest-192x192.png", 192), ("web-app-manifest-512x512.png", 512)):
            im.resize((s, s), Image.LANCZOS).save(OUT / name)


# The host serves static .html with a one-year Cache-Control, which pins old
# pages in the CDN and in browsers. So each page is written as a hidden
# .page.html (the host 403s dot-files) and served by a stub index.php that
# sets a short cache lifetime.
PAGE_STUB = """<?php
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=600');
readfile(__DIR__ . '/.page.html');
"""


def write(path, text):
    f = OUT / path.lstrip("/")
    if path.endswith("/"):
        f.mkdir(parents=True, exist_ok=True)
        (f / "index.php").write_text(PAGE_STUB, encoding="utf-8")
        f = f / ".page.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def main():
    posts = load_dir("posts")
    pages = load_dir("pages")
    order = ["best-dog-ear-cleaner", "virbac-epi-otic-flush-review", "how-to-clean-dog-earss-matters",
             "ear-infection-signs", "zymox-ear-cleanser-review", "cleaning-routines",
             "vetericyn-plus-ear-rinse-review", "pet-md-ear-flush-review", "floppy-ear-breeds", "after-bath-care"]
    posts = {k: posts[k] for k in order if k in posts} | {k: v for k, v in posts.items() if k not in order}

    if OUT.exists():  # start clean so no stale index.html survives the switch to .page.html
        shutil.rmtree(OUT)
    OUT.mkdir()
    for d in ("assets/css", "assets/js"):
        (OUT / d).mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC / "css/site.css", OUT / "assets/css/site.css")
    shutil.copy2(SRC / "js/site.js", OUT / "assets/js/site.js")
    for f in (SRC / "root").glob("*"):
        shutil.copy2(f, OUT / f.name)
    build_images()

    urls = []  # (path, lastmod, priority)

    write("/home.html", P.render_home(layout=layout, posts=posts, helpers=globals()))
    urls.append(("/", TODAY, "1.0"))

    for p in posts.values():
        write(p["path"], render_post(p, posts))
        urls.append((p["path"], p["updated"], "0.9" if p["category"] == "reviews" else "0.8"))

    for p in pages.values():
        write(p["path"], render_page(p))
        urls.append((p["path"], p["updated"], "0.3" if p.get("legal") else "0.5"))

    all_posts = list(posts.values())
    write("/resources/", render_listing(
        "/resources/", "Dog Ear Care Resources: All Guides & Reviews | Dog Ear Cleaner",
        "Every Dog Ear Cleaner guide and review in one place: how to clean dog ears, ear infection signs, "
        "routines, breed tips and honest dog ear cleaner reviews.",
        "Dog Ear Care Resources", "Every guide, review and how-to on Dog Ear Cleaner, newest and most useful first.",
        all_posts, [("Home", "/"), ("Resources", "/resources/")], "Dog Ear Cleaner articles"))
    urls.append(("/resources/", TODAY, "0.6"))
    for key, c in CATEGORIES.items():
        items = [x for x in all_posts if x["category"] == key]
        write(c["path"], render_listing(c["path"], c["title"], c["description"], c["name"], c["intro"], items,
                                        [("Home", "/"), (c["short"], c["path"])], c["name"]))
        urls.append((c["path"], TODAY, "0.6"))

    write("/tools/", render_tools_hub())
    urls.append(("/tools/", TODAY, "0.8"))
    for t in T.TOOLS.values():
        write(t["path"], render_tool_page(t))
        urls.append((t["path"], TODAY, "0.7"))

    write("/404.html", render_404())

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod, prio in urls:
        sm.append(f"<url><loc>{ORIGIN}{path}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "User-agent: *\nDisallow: /home.html\nDisallow: /contact-submit.php\n\n"
        f"Sitemap: {ORIGIN}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(urls)} indexable pages into {OUT.relative_to(ROOT.parent)} (amazon tag {AMAZON_TAG})")


if __name__ == "__main__":
    main()
