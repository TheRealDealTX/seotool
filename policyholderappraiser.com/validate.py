#!/usr/bin/env python3
"""Post-build checks for public/: well-formed HTML, valid JSON-LD, internal
links resolve, unique titles/descriptions, sensible lengths."""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
errors, warnings = [], []


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.bad, self.links, self.imgs = [], [], [], []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "h1":
            self.h1 += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.bad.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            self.stack.pop()
        else:
            self.bad.append(f"stray </{tag}>")


def pages():
    for dp, _d, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(dp, f)


def site_path(fs):
    rel = os.path.relpath(fs, OUT)
    if rel.endswith("index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


all_paths = {site_path(p) for p in pages()}
for dp, _d, files in os.walk(OUT):
    for f in files:
        all_paths.add("/" + os.path.relpath(os.path.join(dp, f), OUT))

titles, descs = {}, {}
for fs in sorted(pages()):
    sp = site_path(fs)
    html = open(fs, encoding="utf-8").read()
    c = Checker()
    c.feed(html)
    for b in c.bad:
        errors.append(f"{sp}: {b}")
    if c.stack:
        errors.append(f"{sp}: unclosed at EOF: {c.stack[-5:]}")
    if c.h1 != 1:
        errors.append(f"{sp}: {c.h1} h1 tags")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{sp}: bad JSON-LD: {e}")
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', html)
    if not t or not d:
        errors.append(f"{sp}: missing title/description")
    else:
        title, desc = t.group(1), d.group(1)
        if title in titles:
            errors.append(f"{sp}: duplicate title with {titles[title]}")
        if desc in descs and sp != "/404.html":
            errors.append(f"{sp}: duplicate description with {descs[desc]}")
        titles[title], descs[desc] = sp, sp
        if len(title) > 70:
            warnings.append(f"{sp}: title {len(title)} chars")
        if len(desc) > 165:
            warnings.append(f"{sp}: description {len(desc)} chars")
    for href in c.links:
        if href.startswith(("http", "mailto:", "tel:", "sms:", "#")):
            continue
        target = href.split("#")[0].split("?")[0]
        if target and target not in all_paths:
            errors.append(f"{sp}: broken link {href}")
    for a in c.imgs:
        if "alt" not in a:
            errors.append(f"{sp}: img without alt {a.get('src')}")
        src = a.get("src", "")
        if src.startswith("/") and src not in all_paths:
            errors.append(f"{sp}: missing image {src}")
    if "huttoroofs" in html or "Hutto Roofers" in html:
        errors.append(f"{sp}: leftover copy from another site")

print(f"checked {len(titles)} pages")
for w in warnings:
    print("WARN", w)
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
