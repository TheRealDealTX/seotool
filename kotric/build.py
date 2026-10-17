#!/usr/bin/env python3
"""Build the kotric.com static site into ./public.

    python3 build.py && python3 validate.py

Only the Python standard library is needed. Page copy lives in content/.
"""
import html
import json
import os
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
sys.path.insert(0, ROOT)

from content import posts as POSTS_MOD  # noqa: E402
from content import pages as PAGES_MOD  # noqa: E402
from content import tools as TOOLS_MOD  # noqa: E402

SITE = "https://kotric.com"
NAME = "Kotric"
TAGLINE = "Fabric Crafts, DIY Projects & Sewing"
EMAIL = "info@kotric.com"
BUILD_DATE = date.today().isoformat()
ASSET_V = BUILD_DATE.replace("-", "")

CATEGORIES = {
    "fabric-crafts": ("Fabric Crafts", "No-sew and low-sew projects that turn fabric into something useful or beautiful.", "colorful-fabrics"),
    "diy-projects": ("DIY Projects", "Weekend makes for your home, your kids and the people you love.", "home-cushions"),
    "sewing": ("Sewing", "Beginner-friendly sewing tutorials, stitches, tools and hacks.", "sewing-machine-orange-felt"),
    "organization": ("Organization", "Tame the fabric stash, plan projects and set up a craft space that works.", "craft-desk"),
}

# Image sizes (all images are 960px wide; height varies).
IMG = {
    "sewing-machine-orange-felt": 640, "pincushion-and-thread": 625, "thread-bobbins": 640, "thread-colors": 640,
    "colorful-fabrics": 641, "felt-fabric-stack": 1280, "embroidered-denim-pocket": 641, "old-jeans": 641,
    "buttons": 641, "plaid-patchwork": 641, "folded-blankets": 624, "linen-pillow": 487, "home-cushions": 1440,
    "scissors-and-thread": 640, "scissors-and-spool": 638, "craft-desk": 592, "vintage-sewing-machine": 663,
    "sewing-station": 1440, "thread-spools": 640, "thimble-and-spools": 640, "spools-on-wood": 641,
    "linen-swatches": 640, "cozy-craft-flatlay": 640, "block-printed-fabric": 641, "dyed-fabric": 641,
    "blue-thread-spools": 704, "green-damask-fabric": 641, "vintage-spools": 639,
}

esc = html.escape


def img_url(name, ext="jpg"):
    return f"/assets/img/{name}.{ext}"


def pic(name, alt, cls="", eager=False, sizes="(max-width: 960px) 100vw, 960px"):
    if name not in IMG:
        raise KeyError(f"unknown image {name}")
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/webp" srcset="{img_url(name, "webp")}">'
            f'<img src="{img_url(name)}" alt="{esc(alt)}" width="960" height="{IMG[name]}" {load}{c}></picture>')


LOGO_SVG = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#cf5a35"/>'
            '<path d="M12 10v20M12 21l11-11M16 17l9 13" stroke="#fbf6ef" stroke-width="3.2" stroke-linecap="round" fill="none"/>'
            '<path d="M27 8c5 4 6 12 1 18" stroke="#e3a83a" stroke-width="1.8" stroke-dasharray="2.5 2.5" fill="none" stroke-linecap="round"/></svg>')

NAV = [("/", "Home"), ("/no-sew-fabric-craft-projects/", "No-Sew Projects"), ("/blog/", "Blog"),
       ("/tools/", "Craft Tools"), ("/about/", "About")]


def header(path):
    def cur(href):
        return ' aria-current="page"' if href == path else ""
    desk = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    mob = "".join(f'<a href="{h}"{cur(h)}>{t}</a>' for h, t in NAV + [("/contact/", "Contact")])
    cats = "".join(f'<a href="/category/{s}/">{v[0]}</a>' for s, v in CATEGORIES.items())
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap hdr-in">
    <a class="logo" href="/" aria-label="{NAME} home">{LOGO_SVG}<span>Kot<em>ric</em></span></a>
    <nav class="nav-desktop" aria-label="Main">{desk}<a class="btn btn-primary" href="/contact/">Contact</a></nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
  <nav class="nav-mobile" id="mobile-nav" aria-label="Mobile" aria-hidden="true">
    {mob}
    <div class="nav-sub">{cats}</div>
    <p class="mob-mail">Say hello: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </nav>
</header>'''


def footer():
    cats = "".join(f'<li><a href="/category/{s}/">{v[0]}</a></li>' for s, v in CATEGORIES.items())
    tools = "".join(f'<li><a href="/tools/{t["slug"]}/">{t["short"]}</a></li>' for t in TOOLS_MOD.TOOLS)
    year = BUILD_DATE[:4]
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">{LOGO_SVG}<span>Kot<em>ric</em></span></a>
        <p>{TAGLINE}. Easy fabric craft ideas, no-sew projects, sewing tutorials and organizing tips for makers of every skill level.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Explore</h4><ul><li><a href="/no-sew-fabric-craft-projects/">41 No-Sew Projects</a></li><li><a href="/4no-sew-diy-fabric-projects/">4 Weekend No-Sew Tutorials</a></li><li><a href="/blog/">All Articles</a></li>{cats}</ul></div>
      <div><h4>Free Tools</h4><ul>{tools}<li><a href="/tools/">All tools</a></li></ul></div>
      <div><h4>Kotric</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-use/">Terms of Use</a></li><li><a href="/disclaimer/">Disclaimer</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>© {year} {NAME}. All rights reserved.</span><span>Made with fabric scraps &amp; good intentions ✂</span></div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">↑</button>'''


def breadcrumbs(trail):
    """trail: list of (name, url); last item is the current page."""
    parts = []
    for i, (n, u) in enumerate(trail):
        if i < len(trail) - 1:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
        else:
            parts.append(f'<span aria-current="page" style="margin:0">{esc(n)}</span>')
    vis = '<span>/</span>'.join(parts)
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb">{vis}</nav>', ld


def page(path, title, desc, body, schema=None, og_img="sewing-machine-orange-felt", og_type="website", progress=False, robots="index, follow"):
    url = SITE + path
    schemas = schema or []
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    prog = '<div class="read-progress" aria-hidden="true"></div>' if progress else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{img_url(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#cf5a35">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{ld}
</head>
<body>
{prog}{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": NAME, "url": SITE + "/",
       "logo": SITE + "/apple-touch-icon.png", "email": EMAIL}


def write(path, content):
    """path is a URL path like /blog/ or a file like /404.html."""
    if path.endswith("/"):
        fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "home.html")
    else:
        fp = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)


def post_card(p, feature=False):
    cat = CATEGORIES[p["cat"]][0]
    cls = "post-card reveal" + (" feature" if feature else "")
    return f'''<a class="{cls}" href="/{p["slug"]}/" data-cat="{p["cat"]}">
  <div class="pic">{pic(p["img"], p["img_alt"])}<span class="tag">{cat}</span></div>
  <div class="body"><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p><div class="meta"><span>{p["read"]} min read</span><span>{fmt_date(p["date"])}</span></div></div>
</a>'''


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{months[int(m) - 1]} {int(d)}, {y}"


def expand_images(body_html):
    import re
    return re.sub(r"__IMG:([a-z0-9-]+):([^_]+)__", lambda m: pic(m.group(1), m.group(2)), body_html)


def toc_and_ids(body_html):
    """Collect <h2 id=...> headings for the table of contents."""
    import re
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
    return heads


def faq_html(faq):
    if not faq:
        return "", None
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in faq)
    import re
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}
    return f'<section class="faq" aria-labelledby="faq"><h2 id="faq">Frequently asked questions</h2>{items}</section>', ld


def article(p, related):
    path = f'/{p["slug"]}/'
    p = dict(p, body=expand_images(p["body"]))
    cat_name = CATEGORIES[p["cat"]][0]
    crumbs, crumb_ld = breadcrumbs([("Home", "/"), (cat_name, f'/category/{p["cat"]}/'), (p["title"], path)])
    heads = toc_and_ids(p["body"])
    fq, fq_ld = faq_html(p.get("faq"))
    if fq:
        heads.append(("faq", "FAQ"))
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads)
    rel = "".join(post_card(r) for r in related)
    share_url = SITE + path
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs}
    <h1 class="reveal">{esc(p["h1"])}</h1>
    <div class="post-meta reveal d1"><a class="tagl" href="/category/{p["cat"]}/">{cat_name}</a><span>By the Kotric Team</span><span>Updated {fmt_date(p["date"])}</span><span>{p["read"]} min read</span></div>
    <div class="hero-img reveal d2">{pic(p["img"], p["img_alt"], eager=True)}</div>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <div class="wrap article-layout">
    <article class="prose">
      {p["body"]}
      {fq}
      <div class="share"><span>Share:</span>
        <a href="https://www.pinterest.com/pin/create/button/?url={share_url}&amp;description={esc(p["title"])}" target="_blank" rel="noopener">Pinterest</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" rel="noopener">Facebook</a>
        <button type="button" data-copy>Copy link</button>
      </div>
      <div class="author-box"><div class="av">K</div><p><strong>The Kotric Team</strong> writes practical, tested fabric craft and sewing guides for beginners and busy makers. Questions or a project to share? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    </article>
    <aside>
      <nav class="toc" aria-label="On this page"><h4>On this page</h4><ol>{toc}</ol></nav>
      <div class="side-card"><h4>Try our free craft tools</h4><p>Work out fabric yardage, fleece blanket sizes and sewing conversions in seconds.</p><a class="btn btn-primary" href="/tools/">Open the tools</a></div>
    </aside>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Keep making</span><h2>You might also like</h2></div>
    <div class="post-grid">{rel}</div>
  </div>
</section>'''
    art_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
              "image": SITE + img_url(p["img"]), "datePublished": p.get("published", p["date"]), "dateModified": p["date"],
              "author": {"@type": "Organization", "name": "The Kotric Team", "url": SITE + "/about/"},
              "publisher": ORG, "mainEntityOfPage": SITE + path, "articleSection": cat_name}
    schemas = [art_ld, crumb_ld] + ([fq_ld] if fq_ld else [])
    return page(path, p["seo_title"], p["desc"], body, schemas, og_img=p["img"], og_type="article", progress=True)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(ROOT, "static")):
        shutil.copy(os.path.join(ROOT, "static", f), os.path.join(OUT, f))

    posts = sorted(POSTS_MOD.POSTS, key=lambda p: p["date"], reverse=True)
    urls = []  # (path, lastmod, priority)

    ctx = dict(SITE=SITE, NAME=NAME, EMAIL=EMAIL, CATEGORIES=CATEGORIES, pic=pic, post_card=post_card,
               breadcrumbs=breadcrumbs, page=page, posts=posts, tools=TOOLS_MOD.TOOLS, esc=esc, ORG=ORG,
               img_url=img_url, faq_html=faq_html, fmt_date=fmt_date, BUILD_DATE=BUILD_DATE)

    # Blog posts
    for p in posts:
        same = [r for r in posts if r["cat"] == p["cat"] and r is not p]
        other = [r for r in posts if r["cat"] != p["cat"]]
        write(f'/{p["slug"]}/', article(p, (same + other)[:3]))
        urls.append((f'/{p["slug"]}/', p["date"], "0.7"))

    # Static pages, pillar pages, hubs
    for path, html_out, prio in PAGES_MOD.build_pages(ctx):
        write(path, html_out)
        if prio is not None:
            urls.append((path, BUILD_DATE, prio))

    # Tools
    for path, html_out in TOOLS_MOD.build_tools(ctx):
        write(path, html_out)
        urls.append((path, BUILD_DATE, "0.7"))

    # sitemap.xml
    urls.sort(key=lambda u: (u[0] != "/", u[0]))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pr in urls:
        sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm) + "\n")
    print(f"built {len(urls)} indexable pages into {OUT}")


if __name__ == "__main__":
    build()
