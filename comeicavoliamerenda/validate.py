#!/usr/bin/env python3
"""Post-build checks for dist/. Exits non-zero on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
errors, titles, descs = [], {}, {}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.h1, self.imgs_no_alt, self.ids, self.ld = [], [], 0, 0, [], []
        self._ld = False; self._buf = ""; self.title = None; self._t = False; self.desc = None; self.canon = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon") and a.get("href"))):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "img":
            if not a.get("alt"):
                self.imgs_no_alt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True; self._buf = ""
        if tag == "title":
            self._t = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")

    def handle_endtag(self, tag):
        if tag == "script" and self._ld:
            self.ld.append(self._buf); self._ld = False
        if tag == "title":
            self._t = False

    def handle_data(self, d):
        if self._ld:
            self._buf += d
        if self._t:
            self.title = (self.title or "") + d


def exists(url):
    url = url.split("#")[0].split("?")[0]
    if url in ("", "/"):
        return True
    p = os.path.join(DIST, url.lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))


pages = []
for dp, dn, fn in os.walk(DIST):
    for f in fn:
        if f.endswith(".html") and not f.startswith("google"):  # skip the Search Console verification file
            pages.append(os.path.join(dp, f))

for path in sorted(pages):
    rel = "/" + os.path.relpath(path, DIST)
    p = P()
    p.feed(open(path).read())
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1")
    if p.imgs_no_alt:
        errors.append(f"{rel}: {p.imgs_no_alt} img without alt")
    for raw in p.ld:
        try:
            json.loads(raw)
        except Exception as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for href in p.links:
        if href.startswith("#"):
            if href[1:] not in p.ids:
                errors.append(f"{rel}: anchor {href} missing")
        elif href.startswith("/") and not exists(href):
            errors.append(f"{rel}: broken link {href}")
    for s in p.srcs:
        if s.startswith("/") and not exists(s):
            errors.append(f"{rel}: missing asset {s}")
    og = re.search(r'property="og:image" content="https://comeicavoliamerenda.com(/[^"]+)"', open(path).read())
    if not og or not exists(og.group(1)):
        errors.append(f"{rel}: og:image missing")
    if len(set(p.ids)) != len(p.ids):
        errors.append(f"{rel}: duplicate ids")
    if rel.endswith("404.html"):
        continue
    if not p.title or not p.desc or not p.canon:
        errors.append(f"{rel}: missing title/description/canonical")
        continue
    if len(html.unescape(p.title)) > 60:
        errors.append(f"{rel}: title {len(p.title)} chars")
    if not 110 <= len(p.desc) <= 160:
        errors.append(f"{rel}: description {len(p.desc)} chars")
    if p.title in titles:
        errors.append(f"{rel}: duplicate title with {titles[p.title]}")
    if p.desc in descs:
        errors.append(f"{rel}: duplicate description with {descs[p.desc]}")
    titles[p.title] = rel; descs[p.desc] = rel

GTAG_ID = "G-5HJ1T79TVS"
for path in pages:
    src = open(path).read()
    head = src.split("</head>")[0]
    if f"googletagmanager.com/gtag/js?id={GTAG_ID}" not in head or f"gtag('config', '{GTAG_ID}')" not in head:
        errors.append(f"{path}: Google tag missing from <head>")
    if 'rel="icon"' not in head or 'rel="manifest"' not in head:
        errors.append(f"{path}: favicon/manifest links missing")
for f in ["googlecccfbf2f7e9e5ae4.html", "favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png",
          "site.webmanifest", "web-app-manifest-192x192.png", "web-app-manifest-512x512.png", "robots.txt", "sitemap.xml"]:
    if not os.path.isfile(os.path.join(DIST, f)):
        errors.append(f"missing root file {f}")
if open(os.path.join(DIST, "googlecccfbf2f7e9e5ae4.html")).read().strip() != "google-site-verification: googlecccfbf2f7e9e5ae4.html":
    errors.append("GSC verification file content changed")

if os.path.exists(os.path.join(DIST, "index.html")):
    errors.append("dist/index.html must not exist (host would serve it for unknown URLs)")

# Every old URL that had organic traffic must resolve to a live page.
sys.path.insert(0, ROOT)
red_src = open(os.path.join(DIST, "redirects.php")).read()
red = dict(re.findall(r"^'(.*?)'=>'(.*?)',$", red_src, re.M))
with open(os.path.join(ROOT, "data", "old-organic-urls.tsv")) as f:
    next(f)
    for line in f:
        path, traffic, _ = line.rstrip("\n").split("\t")
        if int(traffic) > 0 and not (exists(path) or path in red):
            errors.append(f"old URL with traffic not handled: {path}")
for k, v in red.items():
    if not exists(v):
        errors.append(f"redirect {k} -> {v} target missing")

print(f"checked {len(pages)} pages, {len(red)} redirects")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
