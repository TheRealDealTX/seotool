#!/usr/bin/env python3
"""Post-build checks for connectedrenter.com. Exit code 1 on any failure."""
import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
errors = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.ids, self.h1, self.ld, self.imgs_noalt = [], [], set(), 0, [], 0
        self._ld = False
        self.title = self.desc = None
        self._t = False
        self.text, self._skip, self._main = [], 0, 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest") and a.get("href"))):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "img" and not a.get("alt"):
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
        if tag == "title":
            self._t = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "main":
            self._main += 1
        if tag in ("script", "style", "svg", "template") or a.get("aria-hidden") == "true":
            self._skip += 1 if tag not in ("img", "input", "br", "meta", "link") else 0

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False
        if tag == "title":
            self._t = False
        if tag == "main":
            self._main -= 1

    def handle_data(self, d):
        if self._ld:
            self.ld.append(d)
        if self._t:
            self.title = (self.title or "") + d
        if self._main:
            self.text.append(d)


def target(href):
    p = href.split("#")[0].split("?")[0]
    if p == "/":
        return os.path.join(ROOT, "home.html")
    f = os.path.join(ROOT, p.lstrip("/"))
    return os.path.join(f, "index.html") if p.endswith("/") else f


files = [os.path.join(ROOT, "home.html"), os.path.join(ROOT, "404.html")] + glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True)
titles, descs = {}, {}
for f in files:
    rel = os.path.relpath(f, ROOT)
    s = open(f, encoding="utf-8").read()
    p = P()
    p.feed(s)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    for block in p.ld:
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for h in p.links:
        if h.startswith(("http", "mailto:", "tel:")):
            continue
        if h.startswith("#"):
            if h[1:] and h[1:] not in p.ids:
                errors.append(f"{rel}: missing anchor {h}")
            continue
        if not os.path.exists(target(h)):
            errors.append(f"{rel}: broken link {h}")
    for src in p.srcs:
        if src.startswith("http"):
            continue
        if not os.path.exists(target(src)):
            errors.append(f"{rel}: missing asset {src}")
    if rel != "404.html":
        if p.title in titles:
            errors.append(f"{rel}: duplicate title with {titles[p.title]}")
        titles[p.title] = rel
        if p.desc in descs:
            errors.append(f"{rel}: duplicate description with {descs[p.desc]}")
        descs[p.desc] = rel
        if not p.desc or len(p.desc) > 165:
            errors.append(f"{rel}: description length {len(p.desc or '')}")
    for need in ('href="/favicon.svg"', 'href="/favicon-96x96.png" sizes="96x96"', 'name="apple-mobile-web-app-title"'):
        if need not in s:
            errors.append(f"{rel}: missing favicon tag {need}")
    if "googletagmanager.com/gtag/js?id=G-E1CR5DK1LV" not in s or "gtag('config', 'G-E1CR5DK1LV')" not in s:
        errors.append(f"{rel}: missing Google tag")
    if rel != "404.html":
        if p.title and len(html.unescape(p.title)) > 60:
            errors.append(f"{rel}: title over 60 chars")
        if not re.search(r'<link rel="canonical" href="https://connectedrenter\.com/[^"]*">', s):
            errors.append(f"{rel}: missing https canonical")
        for og in re.findall(r'<meta property="og:image" content="https://connectedrenter\.com(/[^"]+)">', s):
            if not os.path.exists(os.path.join(ROOT, og.lstrip("/"))):
                errors.append(f"{rel}: og:image file missing {og}")
    if re.search(r"lorem ipsum|TODO|__ICON_|__TOOL_", s, re.I):
        errors.append(f"{rel}: placeholder text")
    if rel == "home.html":
        main_text = re.sub(r"\s+", " ", " ".join(p.text))
        n = len(re.findall(r"connected renter", main_text, re.I))
        print(f"homepage: 'connected renter' appears {n} times in <main> text")
        if n < 14:
            errors.append(f"home.html: keyword appears only {n} times in main content")

# sitemap: every page listed exactly once, nothing that 404s
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
locs = re.findall(r"<loc>https://connectedrenter\.com(/[^<]*)</loc>", sm)
if len(locs) != len(set(locs)):
    errors.append("sitemap: duplicate URLs")
for u in locs:
    if not os.path.exists(target(u)):
        errors.append(f"sitemap: {u} has no page")
if len(locs) != len(files) - 1:
    errors.append(f"sitemap lists {len(locs)} URLs for {len(files) - 1} pages")
for f in ("robots.txt", "favicon.ico", "favicon.svg", "favicon-96x96.png", "favicon-32.png", "apple-touch-icon.png", "site.webmanifest", "googlecccfbf2f7e9e5ae4.html"):
    if not os.path.exists(os.path.join(ROOT, f)):
        errors.append(f"missing root file {f}")
print(f"sitemap: {len(locs)} URLs")
print(f"checked {len(files)} pages")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
