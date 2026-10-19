#!/usr/bin/env python3
"""Post-build checks for ./public. Exits non-zero on any problem."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ""
        self._in_title = False
        self.desc = None
        self.links = []
        self.assets = []
        self.ld = []
        self._in_ld = False
        self.imgs_no_alt = 0
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.assets.append(a.get("src", ""))
            if "alt" not in a:
                self.imgs_no_alt += 1
        elif tag in ("script", "link") and (a.get("src") or a.get("href")):
            if tag == "script" and a.get("type") == "application/ld+json":
                pass
            self.assets.append(a.get("src") or a.get("href"))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self.ld.append(data)


def url_to_file(u):
    u = u.split("#")[0].split("?")[0]
    if u == "/":
        return os.path.join(ROOT, "home.html")
    p = os.path.join(ROOT, u.lstrip("/"))
    if u.endswith("/"):
        return os.path.join(p, "index.html")
    return p


pages = {}
for dp, _, files in os.walk(ROOT):
    for f in files:
        if f.endswith(".html") and not f.startswith("google"):
            full = os.path.join(dp, f)
            rel = "/" + os.path.relpath(full, ROOT)
            p = Page()
            with open(full, encoding="utf-8") as fh:
                p.feed(fh.read())
            pages[rel] = p

titles, descs = {}, {}
for rel, p in sorted(pages.items()):
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if not p.title:
        errors.append(f"{rel}: missing title")
    if not p.desc:
        errors.append(f"{rel}: missing meta description")
    if p.imgs_no_alt:
        errors.append(f"{rel}: {p.imgs_no_alt} img without alt")
    titles.setdefault(p.title, []).append(rel)
    descs.setdefault(p.desc, []).append(rel)
    for block in p.ld:
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD ({e})")
    for href in p.links:
        if href.startswith(("mailto:", "http://", "https://", "tel:")):
            if "shopvipgifts.com" in href and not href.startswith("mailto:"):
                errors.append(f"{rel}: absolute internal link {href}")
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids:
                errors.append(f"{rel}: missing anchor {href}")
            continue
        if not os.path.exists(url_to_file(href)):
            errors.append(f"{rel}: broken link {href}")
    for src in p.assets:
        if src.startswith("http"):
            continue
        if not os.path.exists(url_to_file(src)):
            errors.append(f"{rel}: missing asset {src}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title {t!r}: {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description: {rels}")

# Images referenced from JS
with open(os.path.join(ROOT, "assets/js/tools.js"), encoding="utf-8") as fh:
    for name in set(re.findall(r'img: "([\w-]+)"', fh.read())):
        if not os.path.exists(os.path.join(ROOT, "assets/img", name + ".webp")):
            errors.append(f"tools.js: missing image {name}")

# Sitemap URLs resolve
with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
    for loc in re.findall(r"<loc>https://shopvipgifts\.com(/[^<]*)</loc>", fh.read()):
        if not os.path.exists(url_to_file(loc)):
            errors.append(f"sitemap: {loc} missing")

# Homepage targets the ranking keywords
home = open(os.path.join(ROOT, "home.html"), encoding="utf-8").read().lower()
for kw in ("vip gift", "vip gifts"):
    if kw not in home:
        errors.append(f"home: keyword {kw!r} missing")

# Site-wide SEO requirements
import html as _html
for dp, _, files in os.walk(ROOT):
    for f in files:
        if not f.endswith(".html") or f.startswith("google"):
            continue
        rel = "/" + os.path.relpath(os.path.join(dp, f), ROOT)
        t = open(os.path.join(dp, f), encoding="utf-8").read()
        for needle in ("googletagmanager.com/gtag/js?id=G-PTQD14707B", "gtag('config', 'G-PTQD14707B')",
                       'rel="canonical"', 'href="/favicon.ico"', 'href="/apple-touch-icon.png"', 'property="og:image"'):
            if needle not in t:
                errors.append(f"{rel}: missing {needle}")
        if t.index("googletagmanager") > t.index("</head>"):
            errors.append(f"{rel}: gtag not in <head>")
        if "noindex" in t:
            continue
        ti = _html.unescape(re.search(r"<title>(.*?)</title>", t).group(1))
        d = _html.unescape(re.search(r'name="description" content="(.*?)"', t).group(1))
        if len(ti) > 60:
            errors.append(f"{rel}: title {len(ti)} chars")
        if not 110 <= len(d) <= 160:
            errors.append(f"{rel}: description {len(d)} chars")

for f in ("favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png", "web-app-manifest-192x192.png",
          "web-app-manifest-512x512.png", "site.webmanifest", "robots.txt", "sitemap.xml", "blog/feed.xml",
          "googlecccfbf2f7e9e5ae4.html", "index.php", "contact.php"):
    if not os.path.exists(os.path.join(ROOT, f)):
        errors.append(f"missing root file {f}")

print(f"checked {len(pages)} html files")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
