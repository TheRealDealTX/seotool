#!/usr/bin/env python3
"""Static checks for ./dist: links, assets, SEO tags, schema, name count.

    python3 check.py
"""
import os, re, json, sys, html
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
NAME = "Studio at 1660 Richmond"
errors, warns = [], []

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.ids = set(); self.text = []; self.skip = 0; self.hidden = []
        self.jsonld = []; self._in_ld = False; self.meta = {}; self.title = ""; self._in_title = False; self.h1 = 0
    def handle_starttag(self, t, a):
        a = dict(a)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src", "data-src", "data-full", "data-map"):
            if a.get(k): self.refs.append((t, k, a[k]))
        for k in ("srcset", "data-srcset", "imagesrcset"):
            if a.get(k):
                for part in a[k].split(","):
                    self.refs.append((t, k, part.strip().split(" ")[0]))
        if t == "script" and a.get("type") == "application/ld+json": self._in_ld = True
        if t in ("script", "style"): self.skip += 1
        if t == "meta" and a.get("name"): self.meta[a["name"]] = a.get("content", "")
        if t == "title": self._in_title = True
        if t == "h1": self.h1 += 1
        if t == "img" and "alt" not in a: errors.append(f"img without alt: {a.get('src')}")
    def handle_endtag(self, t):
        if t in ("script", "style"): self.skip -= 1; self._in_ld = False
        if t == "title": self._in_title = False
    def handle_data(self, d):
        if self._in_ld: self.jsonld.append(d)
        elif self._in_title: self.title += d
        elif not self.skip: self.text.append(d)

titles, descs = {}, {}
pages = []
for dp, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith(".html"):
            pages.append(os.path.join(dp, f))

for path in sorted(pages):
    rel = "/" + os.path.relpath(path, DIST).replace("index.html", "")
    src = open(path, encoding="utf-8").read()
    p = P(); p.feed(src)
    if path.endswith("index.html") and not os.path.exists(path[:-4] + "php"):
        errors.append(f"{rel}: missing index.php")
    if p.meta.get("robots") != "noindex, nofollow": errors.append(f"{rel}: robots meta missing")
    if not p.meta.get("description"): errors.append(f"{rel}: description missing")
    if p.h1 != 1: errors.append(f"{rel}: {p.h1} h1 elements")
    titles.setdefault(p.title, []).append(rel); descs.setdefault(p.meta.get("description"), []).append(rel)
    for blob in p.jsonld:
        try:
            data = json.loads(blob)
            types = [g.get("@type") for g in data.get("@graph", [])]
            if not any(isinstance(t, list) and "ApartmentComplex" in t for t in types): errors.append(f"{rel}: ApartmentComplex schema missing")
        except Exception as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for tag, attr, ref in p.refs:
        if ref.startswith(("http", "mailto:", "tel:", "data:")): continue
        if ref.startswith("#"):
            if len(ref) > 1 and ref[1:] not in p.ids and not any(ref == u for u in ("#apply-online", "#pay-rent", "#maintenance-request", "#resident-portal", "#instagram", "#facebook")):
                errors.append(f"{rel}: missing anchor {ref}")
            continue
        url = ref.split("#")[0].split("?")[0]
        target = os.path.join(DIST, url.lstrip("/"))
        if url.endswith("/"): target = os.path.join(target, "index.html")
        if not os.path.exists(target): errors.append(f"{rel}: broken {attr} -> {ref}")
    if rel == "/":
        text = html.unescape(" ".join(p.text))
        text = re.sub(r"\s+", " ", text)
        n = text.count(NAME)
        print(f"Homepage visible mentions of '{NAME}': {n}")
        if n < 14: errors.append(f"homepage has only {n} mentions of the property name")
    if "[confirm]" in re.sub(r"<!--.*?-->", "", src, flags=re.S): errors.append(f"{rel}: [confirm] visible outside a comment")

for t, ps in titles.items():
    if len(ps) > 1: errors.append(f"duplicate title {t!r}: {ps}")
for d, ps in descs.items():
    if len(ps) > 1: errors.append(f"duplicate description: {ps}")
if open(os.path.join(DIST, "robots.txt")).read().split() != ["User-agent:", "*", "Disallow:", "/"]:
    errors.append("robots.txt is not disallow-all")

print(f"Checked {len(pages)} pages")
for e in errors: print("ERROR", e)
for w in warns: print("WARN", w)
sys.exit(1 if errors else 0)
