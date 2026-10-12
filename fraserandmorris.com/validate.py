#!/usr/bin/env python3
"""Post-build checks for fraserandmorris.com. Run after build.py."""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# URLs that ranked or carried backlinks on the old site and must keep resolving.
LEGACY = ["about.html", "contact.html", "services.html", "gardens.html", "gardens/courtyard.html", "gardens/print.html",
          "gardens/family.html", "gardens/artists.html", "gardens/fox.html", "gardens/study.html", "gardens/belsize.html",
          "gardens/highgate.html", "gardens/country.html", "gardens/courtyard/courtyard2.jpg"]

errors = []
titles, descs = {}, {}
files = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "gardens", "*.html"))
               + glob.glob(os.path.join(ROOT, "blog", "*.html")))
for f in files:
    rel = os.path.relpath(f, ROOT)
    s = open(f, encoding="utf-8").read()
    h1 = len(re.findall(r"<h1[\s>]", s))
    if h1 != 1:
        errors.append(f"{rel}: {h1} h1 tags")
    t = re.search(r"<title>(.*?)</title>", s)
    d = re.search(r'<meta name="description" content="(.*?)">', s)
    if not t or not d:
        errors.append(f"{rel}: missing title/description")
        continue
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
        target = os.path.join(ROOT, ref.lstrip("/"))
        if not os.path.exists(target) and ref not in ("/contact.php",):
            errors.append(f"{rel}: broken link {ref}")
for rel in LEGACY:
    if not os.path.exists(os.path.join(ROOT, rel)):
        errors.append(f"legacy URL missing: /{rel}")
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
    if not os.path.exists(os.path.join(ROOT, "blog", p["slug"] + ".html")):
        errors.append(f"missing post {p['slug']}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(files)} pages, {len(LEGACY)} legacy URLs present")
