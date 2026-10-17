#!/usr/bin/env python3
"""Post-build checks for ./public: internal links and assets resolve, titles/descriptions unique, JSON-LD parses."""
import json
import os
import re
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
problems, titles, descs = [], {}, {}


def target_exists(href):
    p = href.split("#")[0].split("?")[0]
    if p in ("", "/"):
        return os.path.exists(os.path.join(OUT, "home.html"))
    full = os.path.join(OUT, p.lstrip("/"))
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))


pages = []
for root, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))

for fp in pages:
    rel = os.path.relpath(fp, OUT)
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
    if rel == "404.html":
        continue
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    if len(re.findall(r"<h1[ >]", s)) != 1:
        problems.append(f"{rel}: expected exactly one <h1>")
    for img in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in img:
            problems.append(f"{rel}: img without alt")

problems += [f"duplicate title on {v}" for v in titles.values() if len(v) > 1]
problems += [f"duplicate description on {v}" for v in descs.values() if len(v) > 1]
if os.path.exists(os.path.join(OUT, "index.html")):
    problems.append("public/index.html must not exist (it would swallow 404s on the host)")
for must in ["home.html", "index.php", "404.html", "sitemap.xml", "robots.txt", "no-sew-fabric-craft-projects/index.html", "4no-sew-diy-fabric-projects/index.html"]:
    if not os.path.exists(os.path.join(OUT, must)):
        problems.append(f"missing {must}")

print(f"checked {len(pages)} pages")
for p in problems:
    print("FAIL", p)
sys.exit(1 if problems else 0)
