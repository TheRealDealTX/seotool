#!/usr/bin/env python3
"""Post-build checks for beltonbanners.com. Run after build.py.

Checks: every page has one H1, a unique title and description, a canonical,
valid JSON-LD; no broken internal links or missing assets; alt text on every
image; the primary keyword appears on the homepage at least 14 times; every
URL from the old WordPress sitemaps still exists; no WordPress fingerprints.
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "backup", "__pycache__", "wp-content"}
KEYWORD = "belton banners"
MIN_KEYWORD = 14

LEGACY_URLS = [
    "/", "/about-christina-dittman-creations/", "/contact-us/", "/gallery/", "/privacy-policy/",
    "/blog/", "/hand-painted-banner/", "/category/general/",
] + [f"/creation/{s}/" for s in [
    "custom-hand-painted-birthday-banner", "custom-hand-painted-birthday-banner-2", "hand-painted-over-then-moon-banner",
    "childrens-church-hand-painted-banner", "custom-hand-painted-birthday-banner-3", "custom-hand-painted-birthday-banner-4",
    "custom-painted-verse-banner", "childrens-church-hand-painted-banner-2", "custom-painted-verse-banner-2",
    "custom-painted-fall-banner", "custom-painted-verse-banner-3", "custom-hand-painted-banner",
    "custom-hand-painted-birthday-banner-5", "custom-painted-verse-banner-4", "custom-painted-verse-banner-5",
    "custom-hand-painted-birthday-banner-6", "custom-hand-painted-birthday-banner-7"]]

errors = []
warnings = []


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)


def path_exists(href):
    href = href.split("#")[0].split("?")[0]
    if not href or href.startswith(("http", "mailto:", "tel:", "sms:", "javascript:")):
        return True
    if href == "/":
        return os.path.exists(os.path.join(ROOT, "home.html"))
    local = os.path.join(ROOT, href.lstrip("/"))
    if href.endswith("/"):
        return os.path.exists(os.path.join(local, "index.html"))
    if href.endswith(".php"):
        return os.path.exists(local)
    return os.path.exists(local)


titles, descs = {}, {}
for p in pages():
    rel = "/" + os.path.relpath(p, ROOT).replace(os.sep, "/")
    s = open(p, encoding="utf-8").read()
    h1s = re.findall(r"<h1[\s>]", s)
    if len(h1s) != 1:
        errors.append(f"{rel}: {len(h1s)} H1s")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing title")
    else:
        titles.setdefault(t.group(1).strip(), []).append(rel)
        if len(t.group(1)) > 70:
            warnings.append(f"{rel}: title {len(t.group(1))} chars")
    if not d or not d.group(1).strip():
        errors.append(f"{rel}: missing description")
    else:
        descs.setdefault(d.group(1).strip(), []).append(rel)
        if len(d.group(1)) > 165:
            warnings.append(f"{rel}: description {len(d.group(1))} chars")
    if '<link rel="canonical"' not in s:
        errors.append(f"{rel}: missing canonical")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    for href in re.findall(r'(?:href|src)="([^"]+)"', s):
        href = html.unescape(href)
        if href.startswith("/") and not path_exists(href):
            errors.append(f"{rel}: broken link {href}")
    for srcset in re.findall(r'srcset="([^"]+)"', s):
        for part in srcset.split(","):
            u = part.strip().split(" ")[0]
            if u.startswith("/") and not path_exists(u):
                errors.append(f"{rel}: missing srcset file {u}")
    for tag in re.findall(r"<img[^>]*>", s):
        if 'alt="' not in tag:
            errors.append(f"{rel}: img without alt: {tag[:80]}")
    if re.search(r"wp-content/(themes|plugins)|elementor|wp-json|xmlrpc", s):
        errors.append(f"{rel}: WordPress fingerprint")
    if re.search(r"(Hutto|huttoroofs|Roofers)", s):
        errors.append(f"{rel}: leftover source-site text")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title '{t}': {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description: {rels}")

home = open(os.path.join(ROOT, "home.html"), encoding="utf-8").read()
body = re.sub(r"<script[^>]*>.*?</script>", "", home.split("<body", 1)[1], flags=re.S)
text = html.unescape(re.sub("<[^>]+>", " ", body))
n = len(re.findall(KEYWORD, text, re.I))
if n < MIN_KEYWORD:
    errors.append(f"homepage mentions '{KEYWORD}' {n} times (< {MIN_KEYWORD})")
print(f"homepage: '{KEYWORD}' x{n}, 'christina dittman creations' x{len(re.findall('christina dittman creations', text, re.I))}")

for u in LEGACY_URLS:
    if not path_exists(u):
        errors.append(f"legacy URL missing: {u}")

sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
for loc in re.findall(r"<loc>https://beltonbanners\.com([^<]*)</loc>", sitemap):
    if not path_exists(loc):
        errors.append(f"sitemap URL missing: {loc}")

for w in warnings:
    print("warn:", w)
for e in errors:
    print("ERROR:", e)
print(f"{len(list(pages()))} pages checked, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
