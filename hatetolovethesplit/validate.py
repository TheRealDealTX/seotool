#!/usr/bin/env python3
"""Post-build checks: every legacy URL exists, no broken internal links/assets, one H1, unique titles."""
import csv, glob, html, json, os, re, sys
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
noindexed = set()
files = [f for f in glob.glob(OUT + "/**/*.html", recursive=True) if not f.endswith("googlecccfbf2f7e9e5ae4.html")]
for f in files + [os.path.join(OUT, "index.php")]:
    s = open(f, encoding="utf-8").read(); rel = os.path.relpath(f, OUT)
    if rel == "index.php": s = s.split("?>", 1)[1]
    if s.count("gtag/js?id=G-8PT60RX4Q9") != 1: errors.append(f"{rel}: google tag missing/duplicated")
    if "<head>\n<!-- Google tag (gtag.js) -->" not in s: errors.append(f"{rel}: google tag not at top of head")
    for need in ('rel="canonical"', 'name="description"', 'og:image', 'favicon.ico', 'apple-touch-icon', 'site.webmanifest'):
        if need not in s: errors.append(f"{rel}: missing {need}")
    t_len = len(html.unescape(re.search(r"<title>(.*?)</title>", s).group(1)))
    d_len = len(html.unescape(re.search(r'name="description" content="(.*?)"', s).group(1)))
    if rel != "404.html" and not (20 <= t_len <= 62): errors.append(f"{rel}: title length {t_len}")
    if rel != "404.html" and not (110 <= d_len <= 160): errors.append(f"{rel}: description length {d_len}")
    if 'content="noindex' in s: noindexed.add(re.search(r'rel="canonical" href="https://hatetolovethesplit.com([^"]*)"', s).group(1))
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s): json.loads(m.group(1))
    if len(re.findall(r"<h1[ >]", s)) != 1: errors.append(f"{rel}: h1 count")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    if rel != "404.html": titles.setdefault(t, []).append(rel)
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', s):
        if not exists(m.group(1)): errors.append(f"{rel}: broken {m.group(1)}")
    for m in re.finditer(r"<img (?![^>]*alt=)", s): errors.append(f"{rel}: img without alt")
sm = re.findall(r"<loc>https://hatetolovethesplit.com([^<]*)</loc>", open(os.path.join(OUT, "sitemap.xml")).read())
for u in sm:
    if not exists(u): errors.append(f"sitemap URL missing: {u}")
    if u in noindexed: errors.append(f"noindex URL in sitemap: {u}")
for u in open(legacy).read().split():
    if urlparse(u).path in noindexed: errors.append(f"ranked legacy URL is noindex: {u}")
if open(os.path.join(OUT, "googlecccfbf2f7e9e5ae4.html")).read().strip() != "google-site-verification: googlecccfbf2f7e9e5ae4.html":
    errors.append("GSC verification file wrong")
print(f"{len(files) + 1} pages, {len(sm)} in sitemap, {len(noindexed)} noindex")
for t, fs in titles.items():
    if len(fs) > 1: errors.append(f"duplicate title {t!r}: {fs}")
print("\n".join(errors) or "OK: all checks passed"); sys.exit(1 if errors else 0)
