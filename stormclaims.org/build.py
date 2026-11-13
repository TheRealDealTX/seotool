#!/usr/bin/env python3
"""Builds stormclaims.org.

Generated from content/resources.py:
  resources/index.html, resources/<slug>/index.html, and the Resources section
  of the homepage (between the resources:start / resources:end markers).

Shared blocks injected into the hand-written pages (index.html,
upload/index.html, 404.html) between their head / header / footer markers, so
every page carries the same <head> (Google tag, canonical, Open Graph, Twitter
card, icons, manifest, JSON-LD), the same nav and the same footer.

Also writes sitemap.xml and robots.txt, and stamps ?v=<hash> on the CSS/JS
links so browsers pick up new versions after a deploy.

Icons and the Open Graph image are made once by tools/make_images.py.
"""

import hashlib
import json
import os
import re
from datetime import date
from html import escape

from content.resources import RESOURCES

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN = "https://stormclaims.org"
GTM_ID = "GTM-5N3BSV7Z"
PHONE_E164 = "+18325035866"
PHONE_HUMAN = "(832) 503-5866"
EMAIL = "jditt@risepublicadjusting.com"
OG_IMAGE = f"{ORIGIN}/assets/og-image.png"
LOGO = f"{ORIGIN}/web-app-manifest-512x512.png"
SITE_NAME = "StormClaims.org"

ORG = {
    "@type": "ProfessionalService",
    "@id": f"{ORIGIN}/#org",
    "name": "Rise Public Adjusting LLC",
    "alternateName": "Rise Public Adjusting",
    "description": "Licensed Texas public adjusters handling storm, hail, wind and water insurance claims for homeowners, with a referral portal for contractors and roofers.",
    "url": f"{ORIGIN}/",
    "logo": LOGO,
    "image": OG_IMAGE,
    "telephone": PHONE_E164,
    "email": EMAIL,
    "address": {"@type": "PostalAddress", "addressLocality": "Houston", "addressRegion": "TX", "addressCountry": "US"},
    "areaServed": {"@type": "State", "name": "Texas"},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "09:00", "closes": "18:00",
    }],
    "employee": {"@type": "Person", "name": "Joseph Dittman", "jobTitle": "Licensed Texas Public Adjuster"},
    "knowsAbout": ["Storm damage insurance claims", "Hail damage claims", "Wind damage claims", "Roof insurance claims"],
}
ORG_REF = {"@id": f"{ORIGIN}/#org"}
WEBSITE = {
    "@type": "WebSite", "@id": f"{ORIGIN}/#website", "url": f"{ORIGIN}/",
    "name": SITE_NAME, "publisher": ORG_REF, "inLanguage": "en-US",
}


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def asset_version():
    h = hashlib.sha1()
    for name in sorted(os.listdir(os.path.join(ROOT, "assets"))):
        if name.endswith((".css", ".js")):
            h.update(open(os.path.join(ROOT, "assets", name), "rb").read())
    return h.hexdigest()[:8]


def breadcrumbs(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{ORIGIN}{path}"}
            for i, (name, path) in enumerate(items)
        ],
    }


# ---------------------------------------------------------------- shared blocks

def head(title, description, path, noindex=False, og_type="website", graph=None, canonical=True):
    url = f"{ORIGIN}{path}"
    t, d = escape(title), escape(description)
    lines = [
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        f'<script async src="https://www.googletagmanager.com/gtm.js?id={GTM_ID}"></script>',
        "<script>",
        "  window.dataLayer = window.dataLayer || [];",
        "  function gtag(){dataLayer.push(arguments);}",
        "  gtag('js', new Date());",
        "</script>",
        "<script>document.documentElement.className='js'</script>",
        f"<title>{t}</title>",
        f'<meta name="description" content="{d}">',
    ]
    if noindex:
        lines.append('<meta name="robots" content="noindex">')
    if canonical:
        lines.append(f'<link rel="canonical" href="{url}">')
    lines += [
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="StormClaims.org: send us a storm claim in one upload. Rise Public Adjusting referral portal.">',
        '<meta property="og:locale" content="en_US">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        '<meta name="theme-color" content="#133a6b">',
        '<meta name="mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-title" content="StormClaims">',
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">',
        '<meta name="format-detection" content="telephone=no">',
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '<link rel="manifest" href="/site.webmanifest">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">',
        '<link rel="stylesheet" href="/assets/site.css">',
        '<script src="/assets/site.js" defer></script>',
    ]
    if graph:
        data = {"@context": "https://schema.org", "@graph": graph}
        lines.append('<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>")
    lines.append("</head>")
    return "\n".join(lines)


NAV = [("How it works", "/#how"), ("What to send", "/#checklist"), ("Resources", "/resources/"), ("Contact", "/#contact")]


def header(current="", tagline="Referral portal · StormClaims.org", on_upload=False):
    links = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'        <a href="{href}"{cur}>{label}</a>')
    if on_upload:
        cta = f'<a class="cta" href="sms:{PHONE_E164}">Text {PHONE_HUMAN}</a>'
        menu_extra = f'        <a class="m-only m-call" href="tel:{PHONE_E164}">Call or text {PHONE_HUMAN}</a>'
    else:
        cta = '<a class="cta" href="/upload/">Upload files</a>'
        menu_extra = (f'        <a class="m-only m-cta" href="/upload/">Upload claim files</a>\n'
                      f'        <a class="m-only m-call" href="tel:{PHONE_E164}">Call or text {PHONE_HUMAN}</a>')
    return f"""<header class="top" id="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Rise Public Adjusting, StormClaims.org home">
      <span class="mark" aria-hidden="true">R</span>
      <span class="brand-text"><b>Rise Public Adjusting</b><span>{escape(tagline)}</span></span>
    </a>
    <nav class="nav" aria-label="Site">
      <div class="nav-menu" id="nav-menu">
{chr(10).join(links)}
{menu_extra}
      </div>
      {cta}
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-menu" aria-label="Open menu">
        <span class="bars" aria-hidden="true"><i></i><i></i><i></i></span>
      </button>
    </nav>
  </div>
</header>"""


def footer(mobile_bar=True):
    bar = ""
    if mobile_bar:
        bar = f"""
<div class="mbar" role="navigation" aria-label="Quick actions">
  <a class="btn btn-primary" href="/upload/">Upload files</a>
  <a class="btn btn-ghost" href="sms:{PHONE_E164}">Text Joseph</a>
</div>"""
    return f"""<footer>
  <div class="wrap">
    <span>© 2026 Rise Public Adjusting LLC · Texas Public Adjuster License #3356839 · Houston, TX</span>
    <span>Public adjusters, not attorneys. <a href="/upload/">Direct upload link</a> · <a href="/resources/">Resources</a></span>
  </div>
</footer>{bar}"""


def page(head_html, header_html, body, footer_html):
    return f"""<!doctype html>
<html lang="en" class="no-js">
{head_html}
<body>
{header_html}
{body}
{footer_html}
</body>
</html>
"""


# ------------------------------------------------------------- resource pages

def card(r):
    file_bit = f'<span class="res-file">{escape(r["file_label"])}</span>' if r.get("file") else ""
    return f"""        <article class="post">
          <div class="post-meta"><span class="post-cat">{escape(r["category"])}</span> · {nice_date(r["published"])}{file_bit}</div>
          <h2><a href="/resources/{r["slug"]}/">{escape(r["title"])}</a></h2>
          <p class="post-src">{escape(r["source"])}</p>
          <p>{escape(r["summary"])}</p>
          <a class="post-more" href="/resources/{r["slug"]}/">{'Read and download' if r.get('file') else 'Read more'} →</a>
        </article>"""


def index_page():
    path = "/resources/"
    title = "Resources | StormClaims.org"
    desc = "Reference documents and guides for Rise Public Adjusting referrals: industry bulletins, claim documentation tips and what to attach to an estimate."
    graph = [
        ORG, WEBSITE,
        {"@type": "CollectionPage", "@id": f"{ORIGIN}{path}#webpage", "url": f"{ORIGIN}{path}", "name": "Resources",
         "description": desc, "isPartOf": {"@id": f"{ORIGIN}/#website"}, "publisher": ORG_REF,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}/resources/{r['slug']}/", "name": r["title"]}
             for i, r in enumerate(RESOURCES)]}},
        breadcrumbs([("Home", "/"), ("Resources", path)]),
    ]
    cards = "\n".join(card(r) for r in RESOURCES)
    body = f"""<main>
  <section class="hero hero-sm">
    <div class="wrap">
      <h1>Resources</h1>
      <p>Reference documents contractors ask us for, each with a short write-up on when it helps and how to use it on a claim. Attach them to your estimate or send the link to the homeowner.</p>
    </div>
  </section>
  <section class="posts-sec">
    <div class="wrap posts">
{cards}
    </div>
  </section>
</main>"""
    return page(head(title, desc, path, graph=graph), header(current=path), body, footer())


def resource_page(r):
    path = f"/resources/{r['slug']}/"
    title = f"{r['title']} | Resources | StormClaims.org"
    desc = r["summary"]
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    graph = [
        ORG, WEBSITE,
        {"@type": "Article", "@id": f"{ORIGIN}{path}#article", "headline": r["title"][:110],
         "description": r["summary"], "image": OG_IMAGE, "datePublished": r["published"],
         "dateModified": r.get("modified", r["published"]), "author": ORG_REF, "publisher": ORG_REF,
         "mainEntityOfPage": f"{ORIGIN}{path}", "articleSection": r["category"], "inLanguage": "en-US",
         "isPartOf": {"@id": f"{ORIGIN}/#website"}},
        breadcrumbs([("Home", "/"), ("Resources", "/resources/"), (r["title"], path)]),
    ]
    file_block = ""
    if r.get("file"):
        href = f"/resources/{r['file']}"
        file_block = f"""
      <div class="dl">
        <a class="btn btn-primary" href="{href}" download>Download the PDF</a>
        <a class="btn btn-ghost" href="{href}" target="_blank" rel="noopener">Open in a new tab</a>
        <span class="dl-meta">{escape(r["file_label"])}</span>
      </div>"""
    preview = ""
    if r.get("file") and r["file"].lower().endswith(".pdf"):
        href = f"/resources/{r['file']}"
        preview = f"""
      <section class="preview">
        <h2>Preview</h2>
        <object data="{href}#view=FitH" type="application/pdf" aria-label="PDF preview">
          <p>Your browser can't show the PDF inline. <a href="{href}">Download it instead.</a></p>
        </object>
      </section>"""
    body = f"""<main class="wrap article-wrap">
  <article class="article">
    <p class="crumbs"><a href="/resources/">Resources</a> › {escape(r["category"])}</p>
    <h1>{escape(r["title"])}</h1>
    <p class="post-meta">{escape(r["source"])} · Document dated {nice_date(r["date"])} · Posted {nice_date(r["published"])}</p>
    <p class="lede">{escape(r["summary"])}</p>{file_block}
    <div class="prose">
{r["body"].strip()}
    </div>{preview}
    <div class="article-foot">
      <a class="btn btn-ghost" href="/resources/">← All resources</a>
      <a class="btn btn-primary" href="/upload/">Upload a claim</a>
    </div>
  </article>
</main>"""
    return page(head(title, desc, path, og_type="article", graph=graph), header(current="/resources/"), body, footer())


def home_section():
    latest = RESOURCES[:3]
    items = "\n".join(f"""        <a class="res" href="/resources/{r["slug"]}/">
          <span class="res-icon" aria-hidden="true">{'PDF' if (r.get('file') or '').lower().endswith('.pdf') else 'GUIDE'}</span>
          <span class="res-body">
            <b>{escape(r["title"])}</b>
            <span>{escape(r["summary"])}</span>
          </span>
          <span class="res-meta">{escape(r["category"])}</span>
        </a>""" for r in latest)
    return f"""<!-- resources:start -->
  <section id="resources">
    <div class="wrap">
      <div class="section-head">
        <h2>Resources</h2>
        <p><a href="/resources/">See all resources →</a></p>
      </div>
      <div class="resources">
{items}
      </div>
    </div>
  </section>
<!-- resources:end -->"""


# ------------------------------------------------------ hand-written pages

def home_faq(html):
    """FAQPage from the <details> on the homepage, so the schema always
    matches what's visible."""
    out = []
    for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", html, flags=re.S):
        strip = lambda s: re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&#x27;", "'").strip()
        out.append({"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}})
    return out


def hand_pages(home_html):
    title = "StormClaims.org | Rise Public Adjusting referral portal"
    desc = "Referral portal for Rise Public Adjusting. Send claim documents, photos, estimates and policy files for a homeowner in one place."
    home_graph = [
        ORG, WEBSITE,
        {"@type": "WebPage", "@id": f"{ORIGIN}/#webpage", "url": f"{ORIGIN}/", "name": title, "description": desc,
         "isPartOf": {"@id": f"{ORIGIN}/#website"}, "about": ORG_REF, "primaryImageOfPage": OG_IMAGE},
        {"@type": "FAQPage", "@id": f"{ORIGIN}/#faq", "mainEntity": home_faq(home_html)},
    ]
    up_title = "Upload claim documents | Rise Public Adjusting"
    up_desc = "Secure claim document upload for Rise Public Adjusting referrals. Drop the carrier's estimate and the claim details fill in automatically."
    up_graph = [
        ORG,
        {"@type": "WebApplication", "@id": f"{ORIGIN}/upload/#app", "name": "StormClaims.org claim upload",
         "url": f"{ORIGIN}/upload/", "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
         "browserRequirements": "Requires JavaScript", "description": up_desc, "provider": ORG_REF,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
    ]
    return {
        "index.html": (head(title, desc, "/", graph=home_graph), header(), footer()),
        "upload/index.html": (head(up_title, up_desc, "/upload/", noindex=True, graph=up_graph),
                              header(tagline="Claim document upload", on_upload=True), footer(mobile_bar=False)),
        "404.html": (head("Page not found | StormClaims.org", "That page isn't on StormClaims.org.", "/404", noindex=True, canonical=False),
                     header(tagline="Referral portal"), footer()),
    }


def replace_block(text, name, content, path):
    pat = rf"<!-- {name}:start -->.*?<!-- {name}:end -->"
    new, n = re.subn(pat, lambda m: f"<!-- {name}:start -->\n{content}\n<!-- {name}:end -->", text, flags=re.S)
    if not n:
        raise SystemExit(f"{path} is missing the {name}:start / {name}:end markers")
    return new


# ---------------------------------------------------------------- output

def stamp(html, ver):
    return re.sub(r'(/assets/[\w.-]+\.(?:css|js))(\?v=\w+)?"', rf'\1?v={ver}"', html)


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


def main():
    ver = asset_version()
    write("resources/index.html", stamp(index_page(), ver))
    for r in RESOURCES:
        write(f"resources/{r['slug']}/index.html", stamp(resource_page(r), ver))

    home_path = os.path.join(ROOT, "index.html")
    t = open(home_path).read()
    t, n = re.subn(r"<!-- resources:start -->.*?<!-- resources:end -->", lambda m: home_section(), t, flags=re.S)
    if not n:
        raise SystemExit("index.html is missing the resources:start / resources:end markers")
    open(home_path, "w").write(t)

    for path, (h, hd, ft) in hand_pages(t).items():
        full = os.path.join(ROOT, path)
        text = open(full).read()
        text = replace_block(text, "head", h, path)
        text = replace_block(text, "header", hd, path)
        text = replace_block(text, "footer", ft, path)
        write(path, stamp(text, ver))

    today = date.today().isoformat()
    urls = [("/", today), ("/resources/", today)] + [(f"/resources/{r['slug']}/", r.get("modified", r["published"])) for r in RESOURCES]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{ORIGIN}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls]
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")


if __name__ == "__main__":
    main()
