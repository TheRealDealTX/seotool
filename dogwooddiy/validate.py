#!/usr/bin/env python3
"""Post-build checks for ./public: one H1, unique titles/descriptions, valid
JSON-LD, no broken internal links or missing assets, alt text on images, and
every legacy URL that had traffic or backlinks still present."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
LEGACY = ["/", "/about/", "/german-schmear-fireplace/", "/remove-overgrown-shrubs-easy/",
          "/replace-old-caulk-bathtub/", "/decorating-outdoor-spaces/", "/simple-wallpaper-removal/",
          "/painted-grout-bathroom/", "/beginner-gardening-tips/",
          "/simple-diy-boxwood-wreath-you-can-make-in-20-minutes/", "/category/decor-design/", "/disclaimer/"]


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.srcs, self.noalt, self.ld = [], [], 0, []
        self.title = self.desc = None
        self._in_title = self._in_ld = False
        self._buf = ""

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon"))):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "img":
            if not a.get("alt"):
                self.noalt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self.ld.append(self._buf)
            self._in_ld = False

    def handle_data(self, d):
        if self._in_title:
            self.title = (self.title or "") + d
        if self._in_ld:
            self._buf += d


def exists(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return os.path.exists(os.path.join(ROOT, "home.html"))
    full = os.path.join(ROOT, path.lstrip("/"))
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))


def main():
    errors, titles, descs = [], {}, {}
    pages = []
    for d, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".html") and not f.startswith("google"):
                pages.append(os.path.join(d, f))
    for fp in sorted(pages):
        rel = "/" + os.path.relpath(fp, ROOT)
        p = P()
        p.feed(open(fp, encoding="utf-8").read())
        if p.h1 != 1:
            errors.append(f"{rel}: {p.h1} h1 tags")
        if not p.title or not p.desc:
            errors.append(f"{rel}: missing title/description")
        titles.setdefault(p.title, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if p.noalt:
            errors.append(f"{rel}: {p.noalt} images without alt")
        for blob in p.ld:
            try:
                json.loads(blob)
            except ValueError as e:
                errors.append(f"{rel}: bad JSON-LD {e}")
        for href in p.links:
            if href.startswith(("http", "mailto:", "#")):
                continue
            if not exists(href):
                errors.append(f"{rel}: broken link {href}")
        for src in p.srcs:
            if src and src.startswith("/") and not exists(src):
                errors.append(f"{rel}: missing asset {src}")
        if "[[" in open(fp, encoding="utf-8").read():
            errors.append(f"{rel}: unexpanded token")
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f"duplicate title {t!r}: {ps}")
    for t, ps in descs.items():
        if len(ps) > 1:
            errors.append(f"duplicate description: {ps}")
    for u in LEGACY:
        if not exists(u):
            errors.append(f"legacy URL missing: {u}")
    for e in errors:
        print("FAIL", e)
    print(f"{len(pages)} pages checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
