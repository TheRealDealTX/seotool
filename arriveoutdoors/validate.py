#!/usr/bin/env python3
"""Post-build checks for public/. Exits non-zero on any error."""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from siteconfig import REDIRECTS, GONE  # noqa: E402

OUT = os.path.join(ROOT, "public")
errors, warns = [], []


def exists(path):
    path = path.split("#")[0].split("?")[0]
    if not path.startswith("/"):
        return True
    fp = OUT + path
    if path.endswith("/"):
        return os.path.exists(fp + "index.html") or os.path.exists(fp + "index.php")
    return os.path.exists(fp)


pages = glob.glob(OUT + "/**/index.html", recursive=True) + glob.glob(OUT + "/**/index.php", recursive=True) + [OUT + "/404.html"]
titles = {}
for fp in pages:
    rel = fp[len(OUT):]
    h = open(fp, encoding="utf-8").read()
    if rel.endswith("/index.php") and rel != "/index.php" and "/contact/" not in rel:
        continue
    if rel == "/index.php":
        continue
    t = re.search(r"<title>(.*?)</title>", h)
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    if not t:
        errors.append(f"{rel}: no title")
    else:
        titles.setdefault(t.group(1), []).append(rel)
        if len(t.group(1)) > 75:
            warns.append(f"{rel}: long title ({len(t.group(1))})")
    if not d or len(d.group(1)) < 50:
        errors.append(f"{rel}: missing/short description")
    if h.count("<h1") != 1:
        errors.append(f"{rel}: {h.count('<h1')} h1 tags")
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(s)
        except Exception as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for href in re.findall(r'href="([^"]+)"', h):
        if href.startswith(("http", "mailto:", "#", "tel:")):
            continue
        href = href.replace("&amp;", "&")
        if not exists(href):
            errors.append(f"{rel}: broken link {href}")
    for m in re.findall(r'<a [^>]*href="https://(?:www\.)?amazon\.com[^"]*"[^>]*>', h):
        if "sponsored" not in m:
            errors.append(f"{rel}: amazon link without rel=sponsored")
    ids = re.findall(r'\sid="([^"]+)"', h)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        warns.append(f"{rel}: duplicate ids {sorted(dup)[:5]}")
for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title {t!r}: {rels}")

# redirects: targets must exist, no chains, no redirect onto a live page
for old, (new, _) in REDIRECTS.items():
    if not exists(new):
        errors.append(f"redirect target missing: {old} -> {new}")
    if new.split("#")[0] in REDIRECTS:
        errors.append(f"redirect chain: {old} -> {new}")
    if exists(old):
        errors.append(f"redirect source is a live page: {old}")
for g in GONE:
    if exists(g):
        errors.append(f"410 path is a live page: {g}")

sm = open(OUT + "/sitemap.xml").read()
for loc in re.findall(r"<loc>https://arriveoutdoors.com([^<]+)</loc>", sm):
    if not exists(loc):
        errors.append(f"sitemap URL missing: {loc}")

for w in warns:
    print("warn:", w)
for e in errors:
    print("ERROR:", e)
print(f"checked {len(pages)} pages, {len(REDIRECTS)} redirects, {len(GONE)} gone: {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
