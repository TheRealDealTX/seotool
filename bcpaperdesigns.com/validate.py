#!/usr/bin/env python3
"""Post-build checks for bcpaperdesigns.com. Run after build.py; exits non-zero on failure."""
import csv
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
sys.path.insert(0, ROOT)
from siteconfig import PRODUCT_ALIASES  # noqa: E402

errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.h1, self.ids, self.imgs_noalt, self.ld = [], [], 0, [], 0, []
        self.title, self.desc, self.canon = "", "", ""
        self._in_title = self._in_ld = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest") and a.get("href", "").startswith("/"):
            self.srcs.append(a["href"])
        if tag == "img" and not a.get("alt") and a.get("alt") != "":
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        self._in_title = self._in_title and tag != "title"
        self._in_ld = self._in_ld and tag != "script"

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._in_ld:
            self.ld[-1] += d


def url_to_file(u):
    u = u.split("#")[0].split("?")[0]
    if u == "/":
        return os.path.join(OUT, "home.html")
    if u.endswith("/"):
        return os.path.join(OUT, u.strip("/"), "index.html")
    return os.path.join(OUT, u.lstrip("/"))


files = [f for f in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True)]
titles, descs = {}, {}
for f in files:
    rel = os.path.relpath(f, OUT)
    p = P()
    p.feed(open(f, encoding="utf-8").read())
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} img without alt")
    if len(set(p.ids)) != len(p.ids):
        dup = {i for i in p.ids if p.ids.count(i) > 1}
        errors.append(f"{rel}: duplicate ids {dup}")
    for blob in p.ld:
        try:
            json.loads(blob)
        except Exception as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    if rel != "404.html":
        titles.setdefault(p.title, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if not (100 <= len(p.desc) <= 165):
            warns.append(f"{rel}: description length {len(p.desc)}")
        if len(p.title) > 70:
            warns.append(f"{rel}: title length {len(p.title)}: {p.title}")
        if not p.canon.startswith("https://bcpaperdesigns.com/"):
            errors.append(f"{rel}: canonical {p.canon}")
    for u in p.links:
        if u.startswith(("mailto:", "http", "#", "tel:")):
            if u.startswith("#") and len(u) > 1 and u[1:] not in p.ids:
                errors.append(f"{rel}: missing anchor {u}")
            continue
        target = url_to_file(u.replace("&amp;", "&"))
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {u}")
        elif not u.split("#")[0].split("?")[0].endswith(("/", ".html", ".xml", ".txt")):
            warns.append(f"{rel}: link without trailing slash {u}")
    for s in p.srcs:
        if s.startswith("/") and not os.path.exists(url_to_file(s)):
            errors.append(f"{rel}: missing asset {s}")
for t, fs in titles.items():
    if len(fs) > 1:
        errors.append(f"duplicate title {t!r}: {fs}")
for d, fs in descs.items():
    if len(fs) > 1:
        errors.append(f"duplicate description: {fs}")

# every old URL with traffic must be a page or a known 301
csvs = glob.glob("/root/.claude/uploads/*/*organic.Positions*.csv")
if csvs:
    old = {r["URL"] for r in csv.DictReader(open(csvs[0], encoding="utf-8"))}
    for u in sorted(old):
        path = re.sub(r"^https?://[^/]+", "", u).split("?")[0]
        m = re.match(r"^(?:/collections/[^/]+)?/products/([^/]+)", path)
        if m:
            slug = PRODUCT_ALIASES.get(m.group(1), m.group(1))
            if not os.path.exists(os.path.join(OUT, "products", slug, "index.html")):
                errors.append(f"old URL has no page: {u}")
        elif not os.path.exists(url_to_file(path if path.endswith("/") else path + "/")):
            errors.append(f"old URL has no page: {u}")

for w in warns:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(files)} html files checked: {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
