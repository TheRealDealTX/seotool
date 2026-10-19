#!/usr/bin/env python3
"""Validate dist/: links, assets, JSON-LD, titles, H1s, keyword counts, hidden email, blog dates."""
import datetime as dt
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
errors, notes = [], []


def text_of(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


pages = {}
for base, _, files in os.walk(DIST):
    for fn in files:
        if fn.endswith(".html") and not fn.startswith("google"):
            full = os.path.join(base, fn)
            rel = os.path.relpath(full, DIST)
            url = "/" if rel == "home.html" else "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
            pages[url] = open(full, encoding="utf-8").read()

titles, descs = {}, {}
for url, h in pages.items():
    if h.count("G-K3YRCSMJKS") != 2 or h.find("googletagmanager.com/gtag/js") > h.find("<meta charset"):
        errors.append(f"{url}: Google tag missing or not first in <head>")
    for bad in ("katy", "rooferkaty", "cinco ranch", "fulshear", "gmail", "hutto"):
        if bad in h.lower():
            errors.append(f"{url}: leftover text '{bad}'")
    if "noindex" not in h and 'id="lead-popup"' not in h and url not in ("/free-roof-inspection/", "/contact/"):
        errors.append(f"{url}: popup form missing")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(m.group(1))
        except Exception as ex:
            errors.append(f"{url}: bad JSON-LD {ex}")
    h1 = re.findall(r"<h1[ >]", h)
    if len(h1) != 1:
        errors.append(f"{url}: {len(h1)} h1 tags")
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
    if "noindex" not in h:
        titles.setdefault(t, []).append(url)
        descs.setdefault(d, []).append(url)
        if len(t) > 70:
            notes.append(f"{url}: title {len(t)} chars")
    for img in re.findall(r"<img [^>]*>", h):
        if 'alt="' not in img or 'alt=""' in img:
            errors.append(f"{url}: img without alt")
    page_dir = os.path.dirname(os.path.join(DIST, "home.html" if url == "/" else url.lstrip("/") + ("index.html" if url.endswith("/") else "")))
    for rel_asset in re.findall(r'(?:href|src)="((?:\.\./)*(?:assets|favicon|apple-touch|site\.web|web-app)[^"#?]*)', h) + re.findall(r"url\(((?:\.\./)*assets/[^)]+)\)", h):
        if not os.path.isfile(os.path.normpath(os.path.join(page_dir, rel_asset))):
            errors.append(f"{url}: missing asset {rel_asset}")
    for href in re.findall(r'(?:href|src)="(/[^"#?]*)', h):
        if href.startswith("//"):
            continue
        path = os.path.join(DIST, href.lstrip("/"))
        if href == "/" or href in pages or os.path.isfile(path) or href == "/send.php":
            continue
        if os.path.isdir(path) and os.path.isfile(os.path.join(path, "index.html")):
            continue
        errors.append(f"{url}: broken link {href}")
    for bg in re.findall(r"url\((/assets/[^)]+)\)", h):
        if not os.path.isfile(os.path.join(DIST, bg.lstrip("/"))):
            errors.append(f"{url}: missing bg {bg}")

for u, h in pages.items():
    m = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if not m or (u not in ("/404.html",) and m.group(1) != "https://missouricityroofs.com" + u):
        errors.append(f"{u}: canonical wrong")
for t, us in titles.items():
    if len(us) > 1:
        errors.append(f"duplicate title {t}: {us}")
for d, us in descs.items():
    if len(us) > 1:
        errors.append(f"duplicate description: {us}")

# homepage keyword usage (main content only, header/footer excluded)
home = pages["/"]
main = text_of(home.split('<main id="main">')[1].split("</main>")[0]).lower()
counts = {k: len(re.findall(r"\b" + k + r"\b", main)) for k in
          ["missouri city roofers", "missouri city roofer", "missouri city roofing", "free roof inspection"]}
print("homepage keyword counts (main content):", counts)
if counts["missouri city roofers"] < 14:
    errors.append("homepage: 'Missouri City roofers' used fewer than 14 times")
title = re.search(r"<title>(.*?)</title>", home).group(1)
if "(512) 297-7580" not in title or "Missouri City Roofers" not in title:
    errors.append("homepage title must contain the keyword and phone")
cfg = open(os.path.join(DIST, "includes", "config.php")).read()
if "'to'        => 'info@missouricityroofs.com'" not in cfg:
    errors.append("config.php recipient is not info@missouricityroofs.com")

# blog: >= 10 posts, 3 days apart
dates = sorted(dt.date.fromisoformat(re.search(r'article:published_time" content="(\d{4}-\d\d-\d\d)', h).group(1))
               for u, h in pages.items() if u.startswith("/blog/") and u != "/blog/")
gaps = {(b - a).days for a, b in zip(dates, dates[1:])}
print(f"blog posts: {len(dates)}, dates {dates[0]} .. {dates[-1]}, gaps {gaps}")
if len(dates) < 10 or gaps != {3}:
    errors.append("blog dates are not >=10 posts spaced 3 days apart")

# required files
if open(os.path.join(DIST, "googlecccfbf2f7e9e5ae4.html")).read().strip() != "google-site-verification: googlecccfbf2f7e9e5ae4.html":
    errors.append("Search Console verification file missing or wrong")
for f in ["index.php", "favicon-96x96.png", "apple-touch-icon.png", "site.webmanifest", "home.html", "send.php", "includes/config.php", "404.html", "sitemap.xml", "robots.txt", ".htaccess",
          "favicon.ico", "favicon.svg", "assets/img/og-image.jpg"]:
    if not os.path.isfile(os.path.join(DIST, f)):
        errors.append(f"missing {f}")
if os.path.exists(os.path.join(DIST, "index.html")):
    errors.append("dist/index.html must not exist (index.php serves the homepage)")
sm = open(os.path.join(DIST, "sitemap.xml")).read()
print("sitemap urls:", sm.count("<url>"), "| images:", sm.count("<image:image>"), "| html pages:", len(pages))
indexable = {u for u, h in pages.items() if "noindex" not in h}
in_sm = {l.replace("https://missouricityroofs.com", "") for l in re.findall(r"<url><loc>([^<]+)", sm)}
if indexable != in_sm:
    errors.append(f"sitemap mismatch: missing {sorted(indexable - in_sm)} extra {sorted(in_sm - indexable)}")

z = zipfile.ZipFile(os.path.join(ROOT, "missouricityroofs-hostinger-upload.zip"))
names = z.namelist()
if "index.php" not in names or any(n.startswith("dist/") for n in names):
    errors.append("zip layout wrong (files must be at zip root)")
print("zip entries:", len(names))

for n in notes:
    print("note:", n)
if errors:
    print("\n".join("ERROR: " + e for e in errors))
    sys.exit(1)
print("OK")
