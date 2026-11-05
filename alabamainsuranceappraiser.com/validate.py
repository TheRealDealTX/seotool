#!/usr/bin/env python3
"""Post-build checks for ./public_html. Exit code 1 on any error.

Checks: one H1 per page, unique titles/descriptions with sane lengths,
canonical + robots present, valid JSON-LD, every internal link and asset
resolves, every <img> has alt/width/height, homepage keyword count, all
original WordPress URLs still resolve, and no leftover template text.
"""

import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public_html")
KW = "Alabama Insurance Appraiser"
LEGACY = ["/", "/about-us/", "/services/", "/contact/", "/blog/", "/what-does-an-insurance-appraiser-do/",
          "/category/general/", "/privacy-policy/", "/terms-of-use/"]
LEGACY_IMG = glob.glob(os.path.join(HERE, "static/wp-content/uploads/2026/08/*.webp"))

errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.imgs, self.srcs = [], [], []
        self.title = ""
        self._in_title = False
        self.meta = {}
        self.canonical = None
        self.jsonld = []
        self._in_ld = False
        self._ld = ""
        self.main_text = []
        self._main = 0
        self._skip = 0
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if tag in ("script", "link") and (a.get("src") or a.get("href")):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "title":
            self._in_title = True
        if tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld = ""
        if tag == "main":
            self._main += 1
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self._in_ld = False
            self.jsonld.append(self._ld)
        if tag == "main":
            self._main -= 1
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._in_ld:
            self._ld += d
        if self._main and not self._skip:
            self.main_text.append(d)


def page_url(f):
    rel = os.path.relpath(f, OUT).replace(os.sep, "/")
    if rel == "home.html":
        return "/"
    if rel.endswith("index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def resolves(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return True
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        return os.path.isfile(os.path.join(full, "index.html"))
    return os.path.isfile(full)


def main():
    files = [f for f in glob.glob(os.path.join(OUT, "**/*.html"), recursive=True)
             if "/wp-content/" not in f]
    titles, descs = {}, {}
    for f in sorted(files):
        u = page_url(f)
        src = open(f, encoding="utf-8").read()
        p = P()
        p.feed(src)
        noindex = "noindex" in p.meta.get("robots", "")
        if p.h1 != 1:
            errors.append(f"{u}: {p.h1} <h1> tags")
        t = html.unescape(p.title.strip())
        d = p.meta.get("description", "")
        if not t:
            errors.append(f"{u}: missing title")
        elif not (25 <= len(t) <= 70) and not noindex:
            warns.append(f"{u}: title length {len(t)}: {t}")
        if not (70 <= len(d) <= 165) and not noindex:
            warns.append(f"{u}: description length {len(d)}")
        if not noindex:
            if t in titles:
                errors.append(f"{u}: duplicate title with {titles[t]}")
            titles[t] = u
            if d in descs:
                errors.append(f"{u}: duplicate description with {descs[d]}")
            descs[d] = u
        if not p.canonical:
            errors.append(f"{u}: no canonical")
        if not p.jsonld:
            errors.append(f"{u}: no JSON-LD")
        for ld in p.jsonld:
            try:
                data = json.loads(ld)
                types = [g.get("@type") for g in data.get("@graph", [])]
                if not types:
                    errors.append(f"{u}: JSON-LD without @graph")
            except Exception as e:
                errors.append(f"{u}: invalid JSON-LD: {e}")
        for href in p.links:
            if href.startswith(("http://", "https://")):
                if "alabamainsuranceappraiser.com" in href:
                    errors.append(f"{u}: absolute internal link {href}")
                continue
            if href.startswith(("tel:", "mailto:")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    errors.append(f"{u}: missing anchor {href}")
                continue
            if not resolves(href):
                errors.append(f"{u}: broken link {href}")
        for s in p.srcs:
            if s.startswith("/") and not s.startswith("//") and not resolves(s):
                errors.append(f"{u}: missing asset {s}")
        for im in p.imgs:
            if not im.get("alt"):
                errors.append(f"{u}: img without alt {im.get('src')}")
            if not (im.get("width") and im.get("height")):
                errors.append(f"{u}: img without dimensions {im.get('src')}")
            for part in [im.get("src", "")] + [x.strip().split(" ")[0] for x in im.get("srcset", "").split(",") if x.strip()]:
                if part.startswith("/") and not resolves(part):
                    errors.append(f"{u}: missing image {part}")
        for bad in ("{{", "lorem", "TODO", "huttoroofs", "Hutto", "wp-json", "elementor"):
            if bad.lower() in src.lower():
                errors.append(f"{u}: leftover text '{bad}'")
        if u == "/":
            text = html.unescape(" ".join(p.main_text))
            n = text.count(KW)
            print(f"homepage: '{KW}' appears {n} times in visible <main> content "
                  f"({src.count(KW)} times in the full HTML incl. title/meta/schema)")
            if n < 14:
                errors.append(f"homepage keyword count {n} < 14")
    for u in LEGACY:
        if not resolves(u):
            errors.append(f"legacy URL no longer resolves: {u}")
    for f in LEGACY_IMG:
        rel = os.path.relpath(f, os.path.join(HERE, "static"))
        if not os.path.isfile(os.path.join(OUT, rel)):
            errors.append(f"legacy image missing: /{rel}")
    for need in ("index.php", "404.html", "home.html", "sitemap.xml", "robots.txt", "api/contact.php", "site.webmanifest", "favicon.ico"):
        if not os.path.isfile(os.path.join(OUT, need)):
            errors.append(f"missing {need}")
    if os.path.exists(os.path.join(OUT, "index.html")):
        errors.append("root index.html must not exist (see README hosting note)")
    sm = open(os.path.join(OUT, "sitemap.xml")).read()
    locs = re.findall(r"<loc>https://alabamainsuranceappraiser\.com([^<]+)</loc>", sm)
    for l in locs:
        if not resolves(l):
            errors.append(f"sitemap URL does not resolve: {l}")
    print(f"checked {len(files)} HTML files, {len(locs)} sitemap URLs")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
