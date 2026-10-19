#!/usr/bin/env python3
"""Post-build checks: pages (./public/_pages) and assets (./public) resolve, SEO tags are complete, JSON-LD parses."""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public")
PAGES = os.path.join(OUT, "_pages")
GTAG_ID = "G-Q1D6K5T4D2"
problems, titles, descs = [], {}, {}


def target_exists(href):
    p = href.split("#")[0].split("?")[0]
    if p in ("", "/"):
        return os.path.exists(os.path.join(PAGES, "index.html"))
    if p == "/feed/":
        return os.path.isfile(os.path.join(PAGES, "feed.xml"))
    if p.endswith("/"):
        return os.path.isfile(os.path.join(PAGES, p.strip("/"), "index.html"))
    return os.path.isfile(os.path.join(OUT, p.lstrip("/")))


pages = []
for root, _, files in os.walk(PAGES):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))

for fp in pages:
    rel = os.path.relpath(fp, PAGES)
    s = open(fp, encoding="utf-8").read()
    for attr in re.findall(r'(?:href|src|srcset)="(/[^"]*)"', s):
        if not target_exists(attr):
            problems.append(f"{rel}: broken internal reference {attr}")
    ids = set(re.findall(r'id="([^"]+)"', s))
    for frag in re.findall(r'href="#([^"]+)"', s):
        if frag not in ids:
            problems.append(f"{rel}: missing anchor #{frag}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            problems.append(f"{rel}: bad JSON-LD ({e})")
    if f"gtag/js?id={GTAG_ID}" not in s or f"gtag('config', '{GTAG_ID}')" not in s:
        problems.append(f"{rel}: missing Google tag")
    if s.index("googletagmanager") > s.index("<title>"):
        problems.append(f"{rel}: Google tag should come first in <head>")
    if rel == "404.html":
        if "noindex" not in s:
            problems.append("404.html must be noindex")
        continue
    if '<link rel="canonical" href="https://kotric.com/' not in s:
        problems.append(f"{rel}: missing canonical")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    if not 25 <= len(html.unescape(t)) <= 60:
        problems.append(f"{rel}: title length {len(html.unescape(t))}")
    if not 70 <= len(html.unescape(d)) <= 160:
        problems.append(f"{rel}: description length {len(html.unescape(d))}")
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    if len(re.findall(r"<h1[ >]", s)) != 1:
        problems.append(f"{rel}: expected exactly one <h1>")
    for img in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in img:
            problems.append(f"{rel}: img without alt")

problems += [f"duplicate title on {v}" for v in titles.values() if len(v) > 1]
problems += [f"duplicate description on {v}" for v in descs.values() if len(v) > 1]
for root, _, files in os.walk(OUT):
    if root.startswith(PAGES):
        continue
    for f in files:
        if f.endswith(".html") and f != "googlecccfbf2f7e9e5ae4.html":
            problems.append(f"public/ must hold no pages (they would bypass index.php): {f}")
for must in ["index.php", "contact.php", "sitemap.xml", "robots.txt", "googlecccfbf2f7e9e5ae4.html", "favicon.ico", "favicon.svg",
             "favicon-96x96.png", "apple-touch-icon.png", "site.webmanifest", "web-app-manifest-192x192.png", "web-app-manifest-512x512.png"]:
    if not os.path.exists(os.path.join(OUT, must)):
        problems.append(f"missing public/{must}")
for must in ["index.html", "404.html", "feed.xml", "no-sew-fabric-craft-projects/index.html", "4no-sew-diy-fabric-projects/index.html"]:
    if not os.path.exists(os.path.join(PAGES, must)):
        problems.append(f"missing public/_pages/{must}")
sm = open(os.path.join(OUT, "sitemap.xml")).read()
for loc in re.findall(r"<loc>https://kotric.com(/[^<]*)</loc>", sm):
    if not target_exists(loc):
        problems.append(f"sitemap entry does not resolve: {loc}")
if "Sitemap: https://kotric.com/sitemap.xml" not in open(os.path.join(OUT, "robots.txt")).read():
    problems.append("robots.txt does not reference the sitemap")

print(f"checked {len(pages)} pages, {sm.count('<url>')} sitemap URLs")
for p in problems:
    print("FAIL", p)
sys.exit(1 if problems else 0)
