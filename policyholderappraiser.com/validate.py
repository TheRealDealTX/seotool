#!/usr/bin/env python3
"""Post-build checks for public/: well-formed HTML, valid JSON-LD, internal
links resolve, unique titles/descriptions, sensible lengths."""

import html as htmlmod
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
            if f.endswith(".html") and not f.startswith("google"):
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
        title, desc = htmlmod.unescape(t.group(1)), htmlmod.unescape(d.group(1))
        if title in titles:
            errors.append(f"{sp}: duplicate title with {titles[title]}")
        if desc in descs and sp != "/404.html":
            errors.append(f"{sp}: duplicate description with {descs[desc]}")
        titles[title], descs[desc] = sp, sp
        if len(title) > 60:
            warnings.append(f"{sp}: title {len(title)} chars")
        if len(desc) > 145:
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

CITY_NAMES = []
try:
    import sys as _sys
    _sys.path.insert(0, ROOT)
    from content.cities import CITIES as _C
    CITY_NAMES = [c["name"] for c in _C]
except Exception:
    pass
# --- city pages and blog posts: no body paragraph may repeat on another page ---
seen = {}
for fs in sorted(pages()):
    sp = site_path(fs)
    is_city = sp.startswith("/service-areas/") and sp.endswith("-tx/")
    is_post = sp.startswith("/blog/") and sp != "/blog/"
    if not (is_city or is_post):
        continue
    html = open(fs, encoding="utf-8").read()
    m = re.search(r'<article class="prose">(.*?)<div class="author-box">', html, re.S)
    body = m.group(1) if m else ""
    if is_city:
        city = sp[len("/service-areas/"):-len("-tx/")].replace("-", " ")
        main = re.search(r"<main[^>]*>(.*?)</main>", html, re.S).group(1)
        text = htmlmod.unescape(re.sub(r"<[^>]+>", " ", main)).lower()
        n = len(re.findall(re.escape(city.lower()) + r"\s+insurance\s+appraiser", text))
        n_other = sum(len(re.findall(re.escape(o.lower()) + r"\s+insurance\s+appraiser", text)) for o in [c2 for c2 in CITY_NAMES if c2.lower() != city.lower()])
        # the "other cities" strip and nav dropdown mention other cities; only this city's phrase counts
        if n != 14:
            (errors if n < 14 else warnings).append(f"{sp}: '{city} insurance appraiser' appears {n} times (target 14)")
    for para in re.findall(r"<(?:p|li)>(.*?)</(?:p|li)>", body, re.S):
        key = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", para)).strip().lower()
        if len(key) < 60:
            continue
        if key in seen and seen[key] != sp:
            errors.append(f"{sp}: paragraph duplicated from {seen[key]}: {key[:70]}...")
        seen.setdefault(key, sp)

print(f"checked {len(titles)} pages")
for w in warnings:
    print("WARN", w)
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
