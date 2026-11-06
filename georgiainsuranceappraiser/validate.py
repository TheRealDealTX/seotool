#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "Georgia Insurance Appraiser"
MIN_HOME_MENTIONS = 14
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", ""
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self._skip = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and not a.get("alt"):
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
        elif tag == "title":
            self._in = "title"
        if tag in ("script", "style", "head"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip -= 1
        self._in = None

    def handle_data(self, d):
        if self._in == "ld":
            self.ld.append(d)
        elif self._in == "title":
            self.title += d
        if not self._skip:
            self.text.append(d)


titles, descs = {}, {}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            files.append(os.path.join(dp, f))

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(open(fp, encoding="utf-8").read())
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = p.title.strip()
    if not rel.endswith("404.html"):
        titles.setdefault(t, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if len(t) > 65:
            warns.append(f"{rel}: title {len(t)} chars")
        if not 70 <= len(p.desc) <= 165:
            warns.append(f"{rel}: description {len(p.desc)} chars")
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "//")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path:
            frag = href.split("#")[1] if "#" in href else ""
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
    if rel == "/home.html":
        main = " ".join(p.text)
        main = re.sub(r"\s+", " ", main)
        body_only = main.split("Skip to content", 1)[-1]
        n_all = body_only.count(KEYWORD)
        # Count inside <main> only (exclude header/footer brand text)
        raw = open(fp, encoding="utf-8").read()
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
        n_main = mtext.count(KEYWORD)
        print(f"homepage '{KEYWORD}': {n_main} in main content, {n_all} in all visible text")
        if n_main < MIN_HOME_MENTIONS:
            errors.append(f"homepage keyword count {n_main} < {MIN_HOME_MENTIONS}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# Stray references to the sister site
for fp in files:
    s = open(fp, encoding="utf-8").read()
    if re.search(r"alabama", s, re.I):
        errors.append(f"{fp}: mentions Alabama")

print(f"checked {len(files)} html files")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
