#!/usr/bin/env python3
"""Post-build checks for renternews.net. Run after build.py; exits 1 on failure.

- every URL from the original WordPress site (content/legacy_urls.txt) exists
- every internal link and asset in every page resolves to a file
- JSON-LD parses; exactly one <h1>; unique <title> and meta description
- every <img> has alt text and every article has a NewsArticle graph
- the XML sitemaps and the RSS feed are well-formed
"""
import glob
import json
import os
import re
import sys
import xml.dom.minidom
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
errors = []


def resolve(path):
    path = unquote(urlparse(path).path)
    f = os.path.join(PUB, path.lstrip("/"))
    if path.endswith("/"):
        f = os.path.join(f, "index.html")
    return os.path.exists(f) or path in ("/feed/", "/contact.php")


for line in open(os.path.join(ROOT, "content/legacy_urls.txt")):
    u = line.strip()
    if u and not u.startswith("#") and not resolve(urlparse(u).path):
        errors.append(f"legacy URL missing: {u}")

titles, descs = {}, {}
pages = glob.glob(os.path.join(PUB, "**/*.html"), recursive=True)
for f in pages:
    rel = "/" + os.path.relpath(f, PUB)
    if "/wp-content/" in rel:
        continue
    h = open(f, encoding="utf-8").read()
    if len(re.findall(r"<h1[\s>]", h)) != 1:
        errors.append(f"{rel}: expected one <h1>, found {len(re.findall(r'<h1[\\s>]', h))}")
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    if rel != "/404.html":
        titles.setdefault(t, []).append(rel)
        descs.setdefault(d, []).append(rel)
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(blk)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD ({e})")
    for img in re.findall(r"<img\b[^>]*>", h):
        if not re.search(r'\salt="', img):
            errors.append(f"{rel}: <img> without alt: {img[:80]}")
    for link in re.findall(r'(?:href|src)="(/[^"]*)"', h):
        if link.startswith("//"):
            continue
        if not resolve(link):
            errors.append(f"{rel}: broken internal link {link}")
    if rel.startswith("/news/") and rel.count("/") == 3 and "/category/" not in rel and "/page/" not in rel and "/author/" not in rel:
        if '"NewsArticle"' not in h:
            errors.append(f"{rel}: missing NewsArticle schema")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title {t!r}: {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description on {ps}")

for x in glob.glob(os.path.join(PUB, "*.xml")):
    try:
        xml.dom.minidom.parse(x)
    except Exception as e:  # noqa: BLE001
        errors.append(f"{os.path.basename(x)}: invalid XML ({e})")

if errors:
    print("\n".join(errors[:80]))
    print(f"FAILED: {len(errors)} problems")
    sys.exit(1)
print(f"OK: {len(pages)} HTML files checked, all legacy URLs present")
