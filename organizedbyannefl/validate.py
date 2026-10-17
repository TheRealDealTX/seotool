#!/usr/bin/env python3
"""Post-build checks for organizedbyannefl.com. Run after build.py; exits 1 on failure."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
routes = json.load(open(os.path.join(ROOT, "routes.json")))
REQUIRED = ["/", "/about", "/services", "/contact"]  # URLs from the original site (and its backlinks)
errors = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.srcs, self.ld, self.noalt = [], [], [], 0
        self.title = self.desc = None
        self._t = self._ld = False
        self.ids = set()

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") == "stylesheet")):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "img":
            if not a.get("alt"):
                self.noalt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.split()[0])
        if tag == "title":
            self._t = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        if tag == "script":
            self._ld = False

    def handle_data(self, d):
        if self._t:
            self.title = (self.title or "") + d
        if self._ld:
            self.ld[-1] += d


def page_file(r):
    return os.path.join(ROOT, "pages", "home.html" if r == "/" else r.strip("/") + ".html")


for r in REQUIRED:
    if r not in routes:
        errors.append("missing legacy route " + r)

titles, descs = {}, {}
for r in routes:
    src = open(page_file(r)).read()
    p = P()
    p.feed(src)
    if p.h1 != 1:
        errors.append("%s: %d h1" % (r, p.h1))
    if p.noalt:
        errors.append("%s: %d images without alt" % (r, p.noalt))
    for blob in p.ld:
        try:
            json.loads(blob)
        except ValueError as e:
            errors.append("%s: bad JSON-LD %s" % (r, e))
    if r != "/404":
        if p.title in titles:
            errors.append("%s: duplicate title with %s" % (r, titles[p.title]))
        titles[p.title] = r
        if not p.desc or p.desc in descs:
            errors.append("%s: missing/duplicate description" % r)
        descs[p.desc] = r
        if not (50 <= len(p.desc or "") <= 170):
            errors.append("%s: description length %d" % (r, len(p.desc or "")))
    for href in p.links:
        if href.startswith(("mailto:", "http", "tel:")):
            continue
        path, _, frag = href.partition("#")
        if path and path not in routes and not os.path.isfile(os.path.join(ROOT, path.lstrip("/"))):
            errors.append("%s: broken link %s" % (r, href))
        if frag and not path and frag not in p.ids:
            errors.append("%s: missing anchor #%s" % (r, frag))
    for s in p.srcs:
        if s.startswith("/") and not os.path.isfile(os.path.join(ROOT, s.split("?")[0].lstrip("/"))):
            errors.append("%s: missing asset %s" % (r, s))
    text = re.sub(r"<[^>]+>", " ", src)
    if re.search(r"\(\d{3}\)\s*\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b", text):
        errors.append("%s: contains a phone number" % r)
    if "{" in text and re.search(r"\{[a-z_]+\}", text):
        errors.append("%s: unformatted template placeholder" % r)

print("checked %d pages" % len(routes))
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("all checks passed")
