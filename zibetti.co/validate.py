#!/usr/bin/env python3
"""Post-build checks for zibetti.co: links, assets, headings, meta and JSON-LD."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
errors = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.h1, self.ids, self.ld, self.imgs_noalt = [], [], 0, set(), [], 0
        self._in_ld = False
        self.title = self.desc = None
        self._in_title = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "img":
            if "alt" not in a:
                self.imgs_noalt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
            if a.get("data-full"):
                self.srcs.append(a["data-full"])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon") and a.get("href", "").startswith("/"):
            self.srcs.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_ld:
            self.ld.append(d)
        if self._in_title:
            self.title = (self.title or "") + d


def resolve(url):
    path = url.split("#")[0].split("?")[0]
    if path == "/":
        return os.path.join(ROOT, "home.html")
    full = os.path.join(ROOT, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.join(full, "index.html")
    return full


titles, descs = {}, {}
pages = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            pages.append(os.path.join(dp, f))

for page in sorted(pages):
    rel = os.path.relpath(page, ROOT)
    p = P()
    p.feed(open(page, encoding="utf-8").read())
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    if not p.title or not p.desc:
        errors.append(f"{rel}: missing title/description")
    else:
        if len(p.desc) > 165:
            errors.append(f"{rel}: description {len(p.desc)} chars")
        titles.setdefault(p.title, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
    for blob in p.ld:
        try:
            json.loads(blob)
        except Exception as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for href in p.links:
        if href.startswith(("mailto:", "http://", "https://", "tel:")):
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids:
                errors.append(f"{rel}: missing anchor {href}")
            continue
        if not os.path.exists(resolve(href)):
            errors.append(f"{rel}: broken link {href}")
    for src in p.srcs:
        if src.startswith(("http", "data:")):
            continue
        if not os.path.exists(resolve(src)):
            errors.append(f"{rel}: missing asset {src}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title {t!r}: {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# Copy carried over from the old owners must not reappear.
for page in pages:
    text = open(page, encoding="utf-8").read()
    for bad in ("Ashley", "Trevor", "Kambria", "Halle", "Alisabeth", "Narrative blog", "lorem ipsum"):
        if bad in text:
            errors.append(f"{os.path.relpath(page, ROOT)}: contains {bad!r}")

sm = open(os.path.join(ROOT, "sitemap.xml")).read()
for loc in re.findall(r"<loc>https://zibetti\.co(.*?)</loc>", sm):
    if not os.path.exists(resolve(loc)):
        errors.append(f"sitemap: {loc} missing")

if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s)")
    sys.exit(1)
print(f"OK — {len(pages)} pages checked")
