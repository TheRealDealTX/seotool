#!/usr/bin/env python3
"""Post-build checks for public/. Exit 1 on any failure."""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUB = ROOT / "public"
plan = json.loads((ROOT / "content/plan.json").read_text())
errors = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.links = []; self.imgs = []; self.title = ""; self.desc = ""; self.canon = ""; self.ld = []
        self._t = False; self._ld = False; self.text = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1": self.h1 += 1
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "img": self.imgs.append(a)
        if tag == "title": self._t = True
        if tag == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": self.canon = a.get("href", "")
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = True
        for k in ("src", "href"):
            v = a.get(k, "")
            if tag in ("img", "script", "link") and v.startswith("/") and not v.startswith("//"):
                self.links.append(v)

    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag == "script": self._ld = False

    def handle_data(self, d):
        if self._t: self.title += d
        elif self._ld: self.ld.append(d)
        else: self.text.append(d)


routes = {"/", "/journal", "/about", "/contact", "/credits"} | {"/" + p[0] for p in plan["pages"]}
files = {"/": PUB / "home.html"} | {r: PUB / "pages" / f"{r[1:]}.html" for r in routes if r != "/"}
titles, descs = {}, {}
for route, f in files.items():
    if not f.exists():
        errors.append(f"missing page {route}"); continue
    p = P(); p.feed(f.read_text())
    if p.h1 != 1: errors.append(f"{route}: {p.h1} h1")
    if not (10 < len(p.title) <= 75): errors.append(f"{route}: title length {len(p.title)}")
    if not (100 <= len(p.desc) <= 165): errors.append(f"{route}: description length {len(p.desc)}")
    if p.canon != "https://asmith.photography" + ("/" if route == "/" else route): errors.append(f"{route}: canonical {p.canon}")
    for blob in p.ld:
        try: json.loads(blob)
        except Exception as ex: errors.append(f"{route}: bad JSON-LD {ex}")
    for img in p.imgs:
        if not img.get("alt"): errors.append(f"{route}: img without alt {img.get('src')}")
    for href in p.links:
        h = href.split("#")[0].split("?")[0]
        if not h.startswith("/") or h.startswith("//"): continue
        if h in routes or (PUB / h.lstrip("/")).is_file(): continue
        errors.append(f"{route}: broken link {href}")
    titles.setdefault(p.title, []).append(route); descs.setdefault(p.desc, []).append(route)
    body = " ".join(p.text).lower()
    if "aaron" in body and route not in ():
        errors.append(f"{route}: mentions Aaron")
for t, r in titles.items():
    if len(r) > 1: errors.append(f"duplicate title {t!r}: {r}")
for d, r in descs.items():
    if len(r) > 1: errors.append(f"duplicate description: {r}")

# Every old URL with traffic or backlinks must resolve (page or 301 target that exists).
php = (PUB / "index.php").read_text()
for slug, *_ in plan["pages"]:
    if f"'{slug}' => 1" not in php: errors.append(f"index.php missing route {slug}")
for src, dst in plan["redirects"].items():
    if dst not in routes: errors.append(f"redirect {src} -> {dst} target missing")
if (PUB / "index.html").exists():
    errors.append("public/index.html must not exist (host would serve it for unknown URLs)")

for e in errors: print("FAIL", e)
print(f"checked {len(files)} pages: {'OK' if not errors else str(len(errors)) + ' problems'}")
sys.exit(1 if errors else 0)
