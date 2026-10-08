#!/usr/bin/env python3
"""Static site generator for pensacolahurricane.com.

Each page body lives in src/pages/*.html and starts with a one-line JSON
header in an HTML comment:

    <!--{"path": "/weather/", "title": "...", "description": "...", "nav": "/weather/"}-->

build.py wraps every body in the shared layout and writes the finished site
to public/, together with everything under src/static/ (CSS, JS, PHP APIs).

    python3 build.py            # writes ./public
"""

import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")

# The site runs on a temporary *.hostingersite.com address until the
# pensacolahurricane.com domain is pointed at it. While STAGING is True every
# page is noindex and robots.txt blocks crawlers, so the temporary address
# never gets indexed. Flip it to False (and rebuild + redeploy) at launch.
STAGING = True

SITE = {
    "name": "Pensacola Hurricane",
    "origin": "https://pensacolahurricane.com",
    "tagline": "Hurricane tracking, preparedness and recovery for Pensacola, Florida",
    "lat": 30.4213,
    "lon": -87.2169,
}

# Claims-help resource referenced (lightly) on the claims, recovery and tools pages.
FIRM = {
    "name": "The Lawgical Firm",
    "url": "https://thelawgicalfirm.com/residential-property-insurance-claims/hurricane-windstorm/",
    "phone_display": "(407) 433-4131",
    "phone_href": "+14074334131",
}

NAV = [
    ("Storm Tracker", "/hurricane-tracker/"),
    ("Weather", "/weather/"),
    ("Evacuation", "/evacuation-zones/"),
    ("Prepare", "/preparedness/"),
    ("Tools", "/tools/"),
    ("History", "/hurricane-history/"),
    ("Claims", "/insurance-claims/"),
    ("Communities", "/communities/"),
    ("News", "/news/"),
]

TODAY = date.today().isoformat()


def asset_version(rel):
    """Short content hash so a changed CSS/JS file gets a new URL (CDN and browser caches)."""
    import hashlib
    with open(os.path.join(SRC, "static", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def head(page):
    canonical = SITE["origin"] + page["path"]
    robots = "noindex, nofollow" if STAGING else page.get("robots", "index, follow, max-image-preview:large")
    schema = page.get("schema")
    graph = [
        {
            "@type": "WebSite",
            "@id": SITE["origin"] + "/#website",
            "url": SITE["origin"] + "/",
            "name": SITE["name"],
            "description": SITE["tagline"],
            "inLanguage": "en-US",
        },
        {
            "@type": "WebPage",
            "@id": canonical + "#webpage",
            "url": canonical,
            "name": page["title"],
            "description": page["description"],
            "isPartOf": {"@id": SITE["origin"] + "/#website"},
            "about": {"@type": "Place", "name": "Pensacola, Florida",
                      "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lon"]}},
            "dateModified": page.get("modified", TODAY),
        },
    ]
    if page["path"] != "/" and not page["path"].endswith(".html"):
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["origin"] + "/"}]
        parts = [p for p in page["path"].strip("/").split("/") if p]
        for i, _ in enumerate(parts):
            sub = "/" + "/".join(parts[: i + 1]) + "/"
            name = page["title"].split(" | ")[0] if i == len(parts) - 1 else page.get("parent_name", parts[i].replace("-", " ").title())
            crumbs.append({"@type": "ListItem", "position": i + 2, "name": name, "item": SITE["origin"] + sub})
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if schema:
        graph.extend(schema)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    og_type = page.get("og_type", "website")
    article = ""
    if page.get("published"):
        article = (f'<meta property="article:published_time" content="{page["published"]}">\n'
                   f'<meta property="article:modified_time" content="{page.get("modified", page["published"])}">\n')
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page['title'])}</title>
<meta name="description" content="{esc(page['description'])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0b1b2b">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(page['title'])}">
<meta property="og:description" content="{esc(page['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['origin']}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{article}<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Pensacola, Florida">
<meta name="geo.position" content="{SITE['lat']};{SITE['lon']}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&amp;family=Inter:wght@400;500;600;700&amp;display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={asset_version("assets/css/site.css")}">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
"""


def header(active):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for label, href in NAV
    )
    return f"""<div class="alertbar" data-alertbar role="status" aria-live="polite">
<div class="container alertbar-inner">
<span class="alertbar-dot" aria-hidden="true"></span>
<span class="alertbar-text" data-alertbar-text>Checking National Weather Service alerts for Pensacola&hellip;</span>
<a class="alertbar-link" href="/hurricane-tracker/">Live tracker &rarr;</a>
</div>
</div>
<header class="site-header">
<div class="container nav-wrap">
<a class="brand" href="/" aria-label="Pensacola Hurricane home">
<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="23" fill="#e4572e"/><path d="M24 9c-6 0-11 3-13 8 4-3 9-4 13-3-5 2-8 6-8 10 0 5 4 9 9 9 6 0 11-3 13-8-4 3-9 4-13 3 5-2 8-6 8-10 0-5-4-9-9-9z" fill="#fff"/><circle cx="24" cy="24" r="3.2" fill="#e4572e"/></svg>
<span class="brand-copy"><strong>Pensacola Hurricane</strong><span>Escambia &amp; Santa Rosa storm center</span></span>
</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" data-menu-btn>Menu</button>
<nav class="nav-links" id="primary-nav" aria-label="Primary">{links}</nav>
</div>
</header>
<main id="content">
"""


def footer():
    return f"""</main>
<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-about">
<a class="brand brand-footer" href="/"><strong>Pensacola Hurricane</strong></a>
<p>An independent hurricane information center for Pensacola, Pensacola Beach, Perdido Key, Gulf Breeze,
Warrington, Milton, Pace and Navarre. Live data comes from the National Hurricane Center, the National
Weather Service (Mobile/Pensacola office) and Escambia and Santa Rosa County emergency management.</p>
<p class="footer-emergency"><strong>Life-threatening emergency? Call 911.</strong> Follow evacuation orders from
Escambia County and Santa Rosa County officials. This site does not replace official instructions.</p>
</div>
<div>
<div class="footer-title">Track &amp; Prepare</div>
<div class="footer-links">
<a href="/hurricane-tracker/">Live Hurricane Tracker</a>
<a href="/weather/">Pensacola Weather Center</a>
<a href="/evacuation-zones/">Evacuation Zone Checker</a>
<a href="/preparedness/">Preparedness Checklist</a>
<a href="/storm-surge-flood-risk/">Storm Surge &amp; Flood Risk</a>
<a href="/alerts/">Hurricane Alerts Sign-Up</a>
</div>
</div>
<div>
<div class="footer-title">During &amp; After</div>
<div class="footer-links">
<a href="/shelters-roads-outages/">Shelters, Roads &amp; Outages</a>
<a href="/tools/">Hurricane Calculators</a>
<a href="/insurance-claims/">Insurance Claims Center</a>
<a href="/recovery/">Recovery Resources</a>
<a href="/hurricane-history/">Hurricane History</a>
<a href="/news/">Hurricane News</a>
</div>
</div>
<div>
<div class="footer-title">Communities</div>
<div class="footer-links">
<a href="/communities/pensacola-beach/">Pensacola Beach</a>
<a href="/communities/perdido-key/">Perdido Key</a>
<a href="/communities/gulf-breeze/">Gulf Breeze</a>
<a href="/communities/warrington/">Warrington</a>
<a href="/communities/milton/">Milton</a>
<a href="/communities/navarre/">Navarre</a>
<a href="/communities/pace/">Pace</a>
<a href="/communities/downtown-pensacola/">Downtown Pensacola</a>
</div>
</div>
</div>
<div class="footer-bottom">
<span>&copy; {date.today().year} Pensacola Hurricane. Educational information only &mdash; not legal, insurance or engineering advice.</span>
<span><a href="/about/">About</a> &middot; <a href="/disclaimer/">Disclaimer</a> &middot; <a href="/privacy-policy/">Privacy</a> &middot; <a href="/sitemap/">Sitemap</a></span>
</div>
</div>
</footer>
<script src="/assets/js/site.js?v={asset_version("assets/js/site.js")}" defer></script>
</body>
</html>
"""


def expand(body):
    """Small shortcodes so pages stay readable."""
    body = body.replace("{{FIRM_URL}}", FIRM["url"])
    body = body.replace("{{FIRM_NAME}}", FIRM["name"])
    body = body.replace("{{FIRM_PHONE}}", FIRM["phone_display"])
    body = body.replace("{{FIRM_TEL}}", FIRM["phone_href"])
    body = body.replace("{{TODAY}}", TODAY)
    return body


HEADER_RE = re.compile(r"^\s*<!--(\{.*?\})-->\s*", re.S)


def load_pages():
    pages = []
    for name in sorted(os.listdir(os.path.join(SRC, "pages"))):
        if not name.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, "pages", name), encoding="utf-8").read()
        m = HEADER_RE.match(raw)
        if not m:
            raise SystemExit(f"{name}: missing JSON header comment")
        meta = json.loads(m.group(1))
        meta["body"] = expand(raw[m.end():])
        meta["source"] = name
        pages.append(meta)
    return pages


def out_file(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_html(pages):
    groups = {}
    for p in pages:
        if p.get("sitemap") is False:
            continue
        groups.setdefault(p.get("group", "Pages"), []).append(p)
    order = ["Main", "Tools", "Communities", "News", "Pages"]
    html = ""
    for g in order:
        if g not in groups:
            continue
        items = "".join(f'<li><a href="{p["path"]}">{esc(p["title"].split(" | ")[0])}</a></li>'
                        for p in sorted(groups[g], key=lambda x: x["path"]))
        html += f"<h2>{g}</h2><ul class=\"sitemap-list\">{items}</ul>"
    return html


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "static"), OUT)
    pages = load_pages()
    for p in pages:
        body = p["body"].replace("{{SITEMAP}}", sitemap_html(pages))
        html = head(p) + header(p.get("nav")) + body + footer()
        f = out_file(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(html)
    urls = "".join(
        f"<url><loc>{SITE['origin']}{p['path']}</loc><lastmod>{p.get('modified', TODAY)}</lastmod></url>\n"
        for p in pages if p.get("sitemap") is not False
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        if STAGING:
            fh.write("# Staging (temporary domain) - do not index\nUser-agent: *\nDisallow: /\n")
        else:
            fh.write(f"User-agent: *\nDisallow: /api/\n\nSitemap: {SITE['origin']}/sitemap.xml\n")
    print(f"built {len(pages)} pages into {os.path.relpath(OUT, ROOT)}/ (staging={STAGING})")


if __name__ == "__main__":
    main()
