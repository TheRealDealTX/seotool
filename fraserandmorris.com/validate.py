#!/usr/bin/env python3
"""Post-build checks for fraserandmorris.com. Run after build.py."""

import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# URLs that ranked or carried backlinks on the old site and must keep resolving.
LEGACY = ["/", "/about.html", "/contact.html", "/services.html", "/gardens.html", "/gardens/courtyard.html", "/gardens/print.html",
          "/gardens/family.html", "/gardens/artists.html", "/gardens/fox.html", "/gardens/study.html", "/gardens/belsize.html",
          "/gardens/highgate.html", "/gardens/country.html", "/gardens/courtyard/courtyard2.jpg"]
PAGES = os.path.join(ROOT, "_pages")
GUARD = "<?php if (!defined('FM_PAGE')) { http_response_code(404); exit; } ?>\n"


def resolves(url):
    """True if index.php (a page in _pages/) or the host (a static file) answers this URL."""
    if url.endswith("/"):
        return os.path.exists(os.path.join(PAGES, url.lstrip("/"), "index.html.php"))
    return os.path.exists(os.path.join(PAGES, url.lstrip("/") + ".php")) or os.path.isfile(os.path.join(ROOT, url.lstrip("/")))

errors = []
titles, descs = {}, {}
files = sorted(glob.glob(os.path.join(PAGES, "**", "*.php"), recursive=True))
GA = "G-NV7KRXJDDG"
for f in files:
    rel = os.path.relpath(f, PAGES)
    s = open(f, encoding="utf-8").read()
    if not s.startswith(GUARD):
        errors.append(f"{rel}: missing page guard")
    s = s[len(GUARD):]
    if "<?" in s:
        errors.append(f"{rel}: stray PHP open tag")
    head = s.split("</head>")[0]
    if head.count(GA) != 2 or not head.split("<head>")[1].lstrip().startswith("<!-- Google tag"):
        errors.append(f"{rel}: Google tag missing or not first in <head>")
    for needle in ('rel="canonical"', 'rel="icon" href="/favicon.ico"', 'rel="apple-touch-icon"', 'rel="manifest"', 'property="og:image"'):
        if needle not in head:
            errors.append(f"{rel}: missing {needle}")
    if "404" not in rel and 'content="noindex' in head:
        errors.append(f"{rel}: unexpected noindex")
    h1 = len(re.findall(r"<h1[\s>]", s))
    if h1 != 1:
        errors.append(f"{rel}: {h1} h1 tags")
    t = re.search(r"<title>(.*?)</title>", s)
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    if not t or not d:
        errors.append(f"{rel}: missing title/description")
        continue
    tl, dl = len(html.unescape(t.group(1))), len(html.unescape(d.group(1)))
    if "404" not in rel and not (25 <= tl <= 65):
        errors.append(f"{rel}: title length {tl}")
    if "404" not in rel and not (110 <= dl <= 165):
        errors.append(f"{rel}: description length {dl}")
    if t.group(1) in titles:
        errors.append(f"{rel}: duplicate title with {titles[t.group(1)]}")
    titles[t.group(1)] = rel
    if d.group(1) in descs:
        errors.append(f"{rel}: duplicate description with {descs[d.group(1)]}")
    descs[d.group(1)] = rel
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for tag in re.findall(r"<img\b[^>]*>", s):
        if "alt=" not in tag:
            errors.append(f"{rel}: img without alt {tag[:80]}")
    for ref in re.findall(r'(?:href|src)="(/[^"#?]*)', s):
        if ref == "/" or ref.startswith("//"):
            continue
        if not resolves(ref):
            errors.append(f"{rel}: broken link {ref}")
for url in LEGACY:
    if not resolves(url):
        errors.append(f"legacy URL missing: {url}")
for static in ("favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png", "site.webmanifest",
               "web-app-manifest-192x192.png", "web-app-manifest-512x512.png", "googlecccfbf2f7e9e5ae4.html", "robots.txt", "sitemap.xml"):
    if not os.path.isfile(os.path.join(ROOT, static)):
        errors.append(f"missing {static}")
if open(os.path.join(ROOT, "googlecccfbf2f7e9e5ae4.html")).read() != "google-site-verification: googlecccfbf2f7e9e5ae4.html":
    errors.append("GSC verification file content changed")
# Static .html files would be served by the host and bypass index.php.
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if os.path.basename(f) != "googlecccfbf2f7e9e5ae4.html" and "/templates/" not in f:
        errors.append(f"static html would bypass the router: {os.path.relpath(f, ROOT)}")
if not os.path.exists(os.path.join(ROOT, "index.php")) or os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("expected index.php and no index.html (see README)")

# Blog posts must be published exactly three days apart.
from datetime import date
sys.path.insert(0, ROOT)
from content_blog import POSTS
dates = sorted(date.fromisoformat(p["date"]) for p in POSTS)
for a, b in zip(dates, dates[1:]):
    if (b - a).days != 3:
        errors.append(f"blog dates not 3 days apart: {a} -> {b}")
for p in POSTS:
    if not resolves(f"/blog/{p['slug']}.html"):
        errors.append(f"missing post {p['slug']}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(files)} pages, {len(LEGACY)} legacy URLs present")
