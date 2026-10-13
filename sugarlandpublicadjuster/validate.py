#!/usr/bin/env python3
"""Crawl a running copy of the site and check it.

    php -S 127.0.0.1:8090 -t public_html dev-router.php &
    python3 validate.py [http://127.0.0.1:8090]

Checks every page reachable from / and the sitemaps: HTTP 200, no PHP errors,
one <h1>, unique <title>/meta description, canonical, valid JSON-LD, internal
links and images that resolve, alt text, and the homepage keyword targets.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8090").rstrip("/")
ORIGIN = "https://sugarlandpublicadjuster.com"
KEYWORDS = {
    "sugar land public adjuster": 14,
    "public adjuster sugar land": 1,
    "sugar land public adjusters": 1,
    "public adjuster in sugar land": 1,
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.h1, self.ld = [], [], 0, []
        self.title = self.desc = self.canonical = None
        self._in = None
        self._buf = ""
        self.text = []
        self._skip = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append((a.get("src"), a.get("alt")))
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "title" or (tag == "script" and a.get("type") == "application/ld+json"):
            self._in, self._buf = tag, ""
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == self._in:
            if tag == "title":
                self.title = self._buf.strip()
            else:
                self.ld.append(self._buf)
            self._in = None
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_data(self, d):
        if self._in:
            self._buf += d
        elif not self._skip:
            self.text.append(d)


def fetch(path):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


errors, seen, titles, descs = [], {}, {}, {}
queue = ["/"]
_, idx = fetch("/page-sitemap.xml")
_, posts = fetch("/post-sitemap.xml")
for loc in re.findall(r"<loc>([^<]+)</loc>", idx + posts):
    queue.append(loc.replace(ORIGIN, ""))

checked_assets = {}
while queue:
    path = queue.pop(0)
    if path in seen:
        continue
    status, html = fetch(path)
    seen[path] = status
    if status != 200:
        errors.append(f"{path}: HTTP {status}")
        continue
    if re.search(r"(Fatal error|Warning: |Notice: |Deprecated: |Parse error)", html):
        errors.append(f"{path}: PHP error in output")
    p = Page()
    p.feed(html)
    if p.h1 != 1:
        errors.append(f"{path}: {p.h1} <h1> tags")
    if not p.title:
        errors.append(f"{path}: missing <title>")
    if not p.desc:
        errors.append(f"{path}: missing meta description")
    elif not 70 <= len(p.desc) <= 170:
        errors.append(f"{path}: meta description length {len(p.desc)}")
    if p.canonical != ORIGIN + path:
        errors.append(f"{path}: canonical {p.canonical}")
    titles.setdefault(p.title, []).append(path)
    descs.setdefault(p.desc, []).append(path)
    for blob in p.ld:
        try:
            json.loads(blob)
        except ValueError as e:
            errors.append(f"{path}: bad JSON-LD ({e})")
    for src, alt in p.imgs:
        if alt is None:
            errors.append(f"{path}: img without alt {src}")
        if src and src.startswith("/"):
            u = src.split("?")[0]
            if u not in checked_assets:
                checked_assets[u] = fetch(u)[0]
            if checked_assets[u] != 200:
                errors.append(f"{path}: missing image {u}")
    for href in p.links:
        u = urlparse(urljoin(ORIGIN + path, href))
        if u.netloc != urlparse(ORIGIN).netloc or u.scheme not in ("http", "https"):
            continue
        target = u.path or "/"
        if re.search(r"\.(webp|png|jpg|ico|xml|txt|css|js)$", target):
            if target not in checked_assets:
                checked_assets[target] = fetch(target)[0]
            if checked_assets[target] != 200:
                errors.append(f"{path}: broken link {target}")
            continue
        if not target.endswith("/"):
            errors.append(f"{path}: link without trailing slash {target}")
        if target not in seen and target not in queue:
            queue.append(target)
    if path == "/":
        text = re.sub(r"\s+", " ", " ".join(p.text)).lower()
        for kw, need in KEYWORDS.items():
            n = text.count(kw)
            print(f"homepage visible-text count {kw!r}: {n}")
            if n < need:
                errors.append(f"/: keyword {kw!r} appears {n}x, need {need}")
        print(f"homepage words: {len(text.split())}")

for t, paths in titles.items():
    if len(paths) > 1:
        errors.append(f"duplicate title {t!r}: {paths}")
for d, paths in descs.items():
    if d and len(paths) > 1:
        errors.append(f"duplicate description: {paths}")

print(f"pages checked: {len(seen)}; assets checked: {len(checked_assets)}")
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
