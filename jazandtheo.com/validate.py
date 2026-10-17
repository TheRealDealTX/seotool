#!/usr/bin/env python3
"""Post-build checks for jazandtheo.com. Run after build.py; exits non-zero on errors."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
errors, warnings = [], []

# Names from the old post slugs must never appear in page copy (only in URLs).
COUPLE_NAMES = ["mikayla", "shung", "erin and ricky", "erin &amp; ricky", "yasmin", "jared", "jordanne", "aidan", "becca", "tanner", "tia and marco", "tia &amp; marco",
                "hannah and caleb", "hannah &amp; caleb", "ryker", "hannah kathleen"]
BANNED = ["delve", "game-changer", "in today's world", "unlock"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.srcs, self.ld, self.text = [], [], [], []
        self.title = self.desc = self.canonical = None
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.srcs.append(a.get("src"))
            if "alt" not in a or not a["alt"].strip():
                errors.append(f"{self.path}: img without alt ({a.get('src')})")
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
        if tag == "button" and a.get("data-full"):
            self.srcs.append(a["data-full"])
        if tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest") and a.get("href", "").startswith("/"):
            self.srcs.append(a["href"].split("?")[0])
        if tag == "script" and a.get("src", "").startswith("/"):
            self.srcs.append(a["src"].split("?")[0])
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "title":
            self._in = "title"
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title = (self.title or "") + data
        elif self._in == "ld":
            self.ld.append(data)


def target_exists(href):
    href = href.split("#")[0].split("?")[0]
    if not href:
        return True
    if href == "/":
        return os.path.isfile(os.path.join(ROOT, "home.html"))
    p = os.path.join(ROOT, href.lstrip("/"))
    if href.endswith("/"):
        return os.path.isfile(os.path.join(p, "index.html"))
    return os.path.isfile(p)


def main():
    pages = []
    gen = open(os.path.join(ROOT, ".generated")).read().split()
    for rel in gen + ["404.html"]:
        path = "/" + rel.replace("index.html", "") if rel != "home.html" else "/"
        pg = Page()
        pg.path = path
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        pg.feed(src)
        pg.raw = src
        pages.append(pg)
        if pg.h1 != 1:
            errors.append(f"{path}: {pg.h1} h1 tags")
        if not pg.title:
            errors.append(f"{path}: no title")
        elif len(pg.title) > 70:
            warnings.append(f"{path}: title {len(pg.title)} chars")
        if not pg.desc:
            errors.append(f"{path}: no meta description")
        elif not 70 <= len(pg.desc) <= 165:
            warnings.append(f"{path}: description {len(pg.desc)} chars")
        for block in pg.ld:
            try:
                json.loads(block)
            except ValueError as ex:
                errors.append(f"{path}: bad JSON-LD ({ex})")
        for href in pg.links:
            if href.startswith("/") and not href.startswith("//") and not target_exists(href):
                errors.append(f"{path}: broken link {href}")
        for s in pg.srcs:
            if s and s.startswith("/") and not target_exists(s):
                errors.append(f"{path}: missing asset {s}")
        body = re.sub(r"<script.*?</script>|<head>.*?</head>", "", src, flags=re.S).lower()
        body = re.sub(r'(href|src|srcset|data-full|data-copy)="[^"]*"', "", body)
        for n in COUPLE_NAMES:
            if re.search(r"\b" + re.escape(n) + r"\b", body):
                errors.append(f"{path}: couple name '{n}' in copy")
        for b in BANNED:
            if b in body:
                warnings.append(f"{path}: banned phrase '{b}'")
    seen_t, seen_d = {}, {}
    for pg in pages:
        if pg.path == "/404.html":
            continue
        if pg.title in seen_t:
            errors.append(f"duplicate title: {pg.path} and {seen_t[pg.title]}")
        seen_t[pg.title] = pg.path
        if pg.desc in seen_d:
            errors.append(f"duplicate description: {pg.path} and {seen_d[pg.desc]}")
        seen_d[pg.desc] = pg.path
    # Every URL that had traffic or backlinks must resolve.
    legacy = [l.strip() for l in open(os.path.join(ROOT, "content", "legacy-urls.txt")) if l.strip() and not l.startswith("#")]
    for u in legacy:
        if u.startswith("/wp-content/"):
            ok = target_exists(u)
        elif u in ("/weddings", "/portraits", "/lifestyle", "/shop"):
            ok = target_exists(u + "/")
        else:
            ok = target_exists(u)
        if not ok:
            errors.append(f"legacy URL does not resolve: {u}")
    sm = open(os.path.join(ROOT, "sitemap.xml")).read()
    for pg in pages:
        if pg.path not in ("/404.html", "/contact/thanks/") and f"<loc>https://jazandtheo.com{pg.path}</loc>" not in sm:
            errors.append(f"{pg.path}: missing from sitemap.xml")
    for w in warnings:
        print("warn:", w)
    for er in errors:
        print("ERROR:", er)
    print(f"{len(pages)} pages checked, {len(legacy)} legacy URLs, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
