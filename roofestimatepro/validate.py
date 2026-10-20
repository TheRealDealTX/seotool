#!/usr/bin/env python3
"""Post-build checks for roofestimatepro.com. Run after build.py:

    python3 build.py && python3 validate.py

Checks every generated page for: one <h1>, unique title (≤ 70 chars) and
description (70–170 chars), canonical, valid JSON-LD, images with alt text and
existing files, internal links and assets that resolve, tool pages wired to
their script, and leftovers from the old site (WordPress paths, the unrelated
restoration services, city-page URLs).
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("REP_OUT") or os.path.join(ROOT, "public")
sys.path.insert(0, ROOT)
from siteconfig import TOOLS  # noqa: E402

errors, warnings = [], []
titles, descs = {}, {}

BANNED = [r"wp-content/(plugins|themes)", r"elementor", r"Crime Scene", r"Laundry", r"Mold Removal",
          r"Moving &amp; Storage", r"-roof-estimates-services", r"jmautida", r"Designed (&amp;|and) Developed",
          r"lorem ipsum", r"TODO", r"\bunlock\b", r"\belevate\b"]


def page_files():
    for d, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(d, f)


def url_for(fp):
    rel = os.path.relpath(fp, OUT).replace(os.sep, "/")
    if rel == "home.html":
        return "/"
    if rel.endswith("index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def resolves(href):
    path = href.split("#")[0].split("?")[0]
    if not path or path == "/":
        return True
    fp = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.isfile(os.path.join(fp, "index.html"))
    return os.path.isfile(fp)


for fp in sorted(page_files()):
    u = url_for(fp)
    if u in ("/index.html",):
        continue
    s = open(fp, encoding="utf-8").read()
    is404 = u == "/404.html"

    h1 = re.findall(r"<h1[\s>]", s)
    if len(h1) != 1:
        errors.append(f"{u}: {len(h1)} <h1>")
    t = re.findall(r"<title>(.*?)</title>", s, re.S)
    d = re.findall(r'<meta name="description" content="([^"]*)"', s)
    if not t or not d:
        errors.append(f"{u}: missing title/description")
    else:
        tt, dd = html.unescape(t[0]), html.unescape(d[0])
        if len(tt) > 72:
            warnings.append(f"{u}: title {len(tt)} chars")
        if not 70 <= len(dd) <= 170:
            warnings.append(f"{u}: description {len(dd)} chars")
        if tt in titles:
            errors.append(f"{u}: duplicate title with {titles[tt]}")
        if dd in descs:
            errors.append(f"{u}: duplicate description with {descs[dd]}")
        titles[tt], descs[dd] = u, u
    if not is404 and f'<link rel="canonical" href="https://roofestimatepro.com{u}">' not in s:
        errors.append(f"{u}: canonical missing or wrong")

    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(blk)
        except ValueError as e:
            errors.append(f"{u}: bad JSON-LD ({e})")

    for img in re.findall(r"<img\b[^>]*>", s):
        if not re.search(r'\balt="', img):
            errors.append(f"{u}: img without alt: {img[:80]}")
        src = re.search(r'\bsrc="([^"]+)"', img)
        if src and src.group(1).startswith("/") and not resolves(src.group(1)):
            errors.append(f"{u}: missing image {src.group(1)}")

    for href in re.findall(r'(?:href|src)="(/[^"]*)"', s):
        if href.startswith("//") or href.startswith("/api/"):
            continue
        if not resolves(href):
            errors.append(f"{u}: broken link {href}")

    for pat in BANNED:
        if re.search(pat, s, re.I):
            errors.append(f"{u}: banned pattern {pat!r}")

    if u.startswith("/tools/") and u != "/tools/":
        slug = u.strip("/").split("/")[1]
        if f"/assets/js/tools/{slug}.js" not in s:
            errors.append(f"{u}: tool script not referenced")
        if 'id="tool-form"' not in s or 'id="results"' not in s:
            errors.append(f"{u}: tool form/results missing")
        words = len(re.sub(r"<[^>]+>", " ", re.search(r'<article class="prose">(.*?)</article>', s, re.S).group(1)).split())
        if words < 600:
            warnings.append(f"{u}: explainer only {words} words")

for t in TOOLS:
    if not os.path.isfile(os.path.join(OUT, "tools", t["slug"], "index.html")):
        errors.append(f"tool page missing: {t['slug']}")
    if not os.path.isfile(os.path.join(OUT, "assets", "js", "tools", t["slug"] + ".js")):
        errors.append(f"tool script missing: {t['slug']}")

sm = open(os.path.join(OUT, "sitemap.xml")).read()
for loc in re.findall(r"<loc>https://roofestimatepro.com([^<]*)</loc>", sm):
    if not resolves(loc):
        errors.append(f"sitemap: {loc} does not exist")
if os.path.exists(os.path.join(OUT, "index.html")):
    errors.append("public/index.html must not exist (the host would serve it for every unknown path)")

for w in warnings:
    print("warn:", w)
for e in errors:
    print("ERROR:", e)
n = len(list(page_files()))
print(f"{n} html files checked, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
