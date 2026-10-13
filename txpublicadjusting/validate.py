#!/usr/bin/env python3
"""Crawl a running copy of the site and check it.

    php -S 127.0.0.1:8088 -t site site/index.php &
    python3 validate.py http://127.0.0.1:8088

Checks: every internal link returns 200 (no redirects or 404s), one <h1> per page,
unique titles and meta descriptions within length limits, parseable JSON-LD,
canonical tags, no banned filler phrases, no leftover [[shortcodes]], and that
every URL in the sitemap was reached by the crawl. Exits non-zero on errors.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8088").rstrip("/")
BANNED = ["navigate", "navigating", "delve", "in today's", "it's important to note", "peace of mind",
          "game-changer", "unlock", "empower", "seamless", "rest assured", "look no further", "battlefield"]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def fetch(path):
    try:
        r = opener.open(BASE + path, timeout=30)
        return r.status, r.read().decode("utf-8", "replace"), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), e.headers


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.title, self.desc, self.canon, self.ld = [], 0, "", "", "", []
        self._in, self._buf = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") == "stylesheet")):
            self.links.append(a.get("src") or a.get("href"))
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in, self._buf = "title", []
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in, self._buf = "ld", []

    def handle_endtag(self, tag):
        if self._in == "title" and tag == "title":
            self.title = "".join(self._buf).strip()
            self._in = None
        if self._in == "ld" and tag == "script":
            self.ld.append("".join(self._buf))
            self._in = None

    def handle_data(self, data):
        if self._in:
            self._buf.append(data)


errors, warnings = [], []
seen, queue = {}, ["/"]
titles, descs = defaultdict(list), defaultdict(list)
assets = set()

while queue:
    path = queue.pop(0)
    if path in seen:
        continue
    status, body, headers = fetch(path)
    seen[path] = status
    if status != 200:
        continue
    if "text/html" not in headers.get("Content-Type", ""):
        continue
    p = Page()
    p.feed(body)
    if p.h1 != 1:
        errors.append(f"{path}: {p.h1} <h1> tags")
    titles[p.title].append(path)
    descs[p.desc].append(path)
    if not (20 <= len(p.title) <= 75):
        warnings.append(f"{path}: title length {len(p.title)}: {p.title}")
    if path != "/404/" and not (90 <= len(p.desc) <= 165):
        warnings.append(f"{path}: description length {len(p.desc)}")
    if not p.canon.endswith(path):
        errors.append(f"{path}: canonical {p.canon}")
    for blob in p.ld:
        try:
            json.loads(blob)
        except ValueError as e:
            errors.append(f"{path}: bad JSON-LD ({e})")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text).lower()
    for b in BANNED:
        if re.search(r"\b" + re.escape(b) + r"\b", text):
            warnings.append(f"{path}: banned phrase '{b}'")
    if "[[" in text:
        errors.append(f"{path}: unrendered shortcode")
    for href in p.links:
        if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "sms:", "#", "data:")):
            continue
        href = href.split("#")[0].split("?")[0]
        if not href:
            continue
        if href.startswith("/assets/") or re.search(r"\.(ico|png|jpg|webp|webmanifest|css|js|json|xml|txt)$", href):
            assets.add(href)
        elif href not in seen and href not in queue:
            queue.append(href)

for path, status in sorted(seen.items()):
    if status != 200:
        errors.append(f"link target {path} returned {status}")
for a in sorted(assets):
    st, _, _ = fetch(a)
    if st != 200:
        errors.append(f"asset {a} returned {st}")
for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1 and d:
        errors.append(f"duplicate description on {ps}")

st, sm, _ = fetch("/sitemap.xml")
locs = [re.sub(r"^https://[^/]+", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
for u in locs:
    if seen.get(u) != 200:
        errors.append(f"sitemap URL {u} not reachable by crawl (status {seen.get(u)})")

print(f"Crawled {len(seen)} URLs, {len(assets)} assets, sitemap {len(locs)} URLs")
for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
