#!/usr/bin/env python3
"""Post-build checks: every legacy URL exists, no broken internal links/assets, one H1, unique titles."""
import csv, os, re, sys, glob
from urllib.parse import urlparse
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "public")
def exists(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"): return True
    f = os.path.join(OUT, path.lstrip("/"))
    return os.path.isfile(f) or os.path.isfile(os.path.join(f, "index.html"))
errors = []
legacy = os.path.join(ROOT, "legacy-urls.txt")
for u in open(legacy).read().split():
    if not exists(urlparse(u).path): errors.append(f"legacy URL missing: {u}")
titles = {}
for f in glob.glob(OUT + "/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read(); rel = os.path.relpath(f, OUT)
    if len(re.findall(r"<h1[ >]", s)) != 1: errors.append(f"{rel}: h1 count")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    if rel != "404.html": titles.setdefault(t, []).append(rel)
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', s):
        if not exists(m.group(1)): errors.append(f"{rel}: broken {m.group(1)}")
    for m in re.finditer(r"<img (?![^>]*alt=)", s): errors.append(f"{rel}: img without alt")
for t, fs in titles.items():
    if len(fs) > 1: errors.append(f"duplicate title {t!r}: {fs}")
print("\n".join(errors) or "OK: all checks passed"); sys.exit(1 if errors else 0)
