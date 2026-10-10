#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any problem."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

OUT = Path(__file__).resolve().parent / "public"
problems = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ""
        self.desc = None
        self.canonical = None
        self.refs = []
        self.imgs_no_alt = 0
        self.ld = []
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in = "title"
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
            self.ld.append("")
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        for k in ("href", "src"):
            if a.get(k):
                self.refs.append(a[k])

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "ld":
            self.ld[-1] += data


def exists(ref):
    path = urlparse(ref).path
    if path in ("/", ""):
        return True
    f = OUT / path.lstrip("/")
    return f.is_file() or (f / "index.html").is_file()


titles, descs = {}, {}
pages = [p for p in OUT.rglob("*.html")]
for f in pages:
    rel = "/" + str(f.relative_to(OUT))
    pg = Page()
    pg.feed(f.read_text(encoding="utf-8"))
    if pg.h1 != 1:
        problems.append(f"{rel}: {pg.h1} <h1>")
    if not pg.title or not pg.desc or not pg.canonical:
        problems.append(f"{rel}: missing title/description/canonical")
    if rel != "/404.html":
        titles.setdefault(pg.title, []).append(rel)
        descs.setdefault(pg.desc, []).append(rel)
    if len(pg.title) > 65:
        problems.append(f"{rel}: title {len(pg.title)} chars")
    if pg.desc and not 70 <= len(pg.desc) <= 170:
        problems.append(f"{rel}: description {len(pg.desc)} chars")
    if pg.imgs_no_alt:
        problems.append(f"{rel}: {pg.imgs_no_alt} <img> without alt")
    for block in pg.ld:
        try:
            json.loads(block)
        except ValueError as e:
            problems.append(f"{rel}: bad JSON-LD ({e})")
    for ref in pg.refs:
        if ref.startswith(("http", "mailto:", "#", "data:")) or ref.startswith("//"):
            continue
        if not exists(ref):
            problems.append(f"{rel}: broken link {ref}")
    if re.search(r"huttoroof|Hutto", f.read_text(encoding="utf-8")):
        problems.append(f"{rel}: leftover text from the other site")
for t, where in titles.items():
    if len(where) > 1:
        problems.append(f"duplicate title {t!r}: {where}")
for d, where in descs.items():
    if len(where) > 1:
        problems.append(f"duplicate description: {where}")
for need in ("home.html", "index.php", "404.html", "robots.txt", "sitemap.xml", "favicon.ico"):
    if not (OUT / need).is_file():
        problems.append(f"missing {need}")
if (OUT / "index.html").exists():
    problems.append("index.html must not exist (see README, Hosting)")
for loc in re.findall(r"<loc>https://hotsbuzz\.com([^<]*)</loc>", (OUT / "sitemap.xml").read_text()):
    if not exists(loc):
        problems.append(f"sitemap URL has no page: {loc}")

print("\n".join(problems) or f"OK: {len(pages)} pages checked")
sys.exit(1 if problems else 0)
