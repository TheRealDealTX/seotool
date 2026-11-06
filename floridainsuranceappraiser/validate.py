#!/usr/bin/env python3
"""Post-build checks for dist/. Exit 1 on any failure."""
import json
import os
import re
import sys
from html.parser import HTMLParser

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
KEY = "Florida Insurance Appraiser"
errors, titles, descs = [], {}, {}


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip, self.parts = 0, []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.parts.append(d)


def target_exists(href):
    path = href.split("#")[0].split("?")[0]
    if not path or path == "/":
        return True
    full = os.path.join(DIST, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.isfile(os.path.join(full, "index.html"))
    return os.path.isfile(full)


pages = []
for root, _, files in os.walk(DIST):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))

for fp in sorted(pages):
    rel = os.path.relpath(fp, DIST)
    html = open(fp, encoding="utf-8").read()
    if len(re.findall(r"<h1[\s>]", html)) != 1:
        errors.append(f"{rel}: expected exactly one <h1>")
    t = re.search(r"<title>(.*?)</title>", html).group(1)
    d = re.search(r'<meta name="description" content="(.*?)"', html).group(1)
    if len(t.replace("&amp;", "&")) > 65:
        errors.append(f"{rel}: title too long ({len(t)}): {t}")
    if not 120 <= len(d.replace("&amp;", "&")) <= 160 and rel != "404.html":
        errors.append(f"{rel}: description length {len(d)}")
    if t in titles:
        errors.append(f"{rel}: duplicate title with {titles[t]}")
    titles[t] = rel
    if d in descs:
        errors.append(f"{rel}: duplicate description with {descs[d]}")
    descs[d] = rel
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(m)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for href in re.findall(r'(?:href|src)="(/[^"]*)"', html):
        if href.startswith("//"):
            continue
        if not target_exists(href):
            errors.append(f"{rel}: broken link {href}")
    for bad in ("alabamainsuranceappraiser", "Alabama Insurance Appraiser", "{{", "TODO", "lorem"):
        if bad in html:
            errors.append(f"{rel}: contains '{bad}'")

home = open(os.path.join(DIST, "home.html"), encoding="utf-8").read()
p = Text()
p.feed(home)
body_text = " ".join(p.parts)
n = body_text.count(KEY)
print(f"homepage visible mentions of '{KEY}': {n}")
if n < 14:
    errors.append(f"home.html: only {n} visible mentions of {KEY}")

print(f"checked {len(pages)} pages")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("OK")
