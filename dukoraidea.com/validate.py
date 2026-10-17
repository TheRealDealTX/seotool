#!/usr/bin/env python3
"""Post-build checks for dukoraidea.com. Run after build.py; exits non-zero on failure."""

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "_pages"
ORIGIN = "https://dukoraidea.com"

# URLs from the old Shopify store that must resolve (traffic or backlinks).
LEGACY = [
    "/", "/blogs/blog",
    "/blogs/blog/create-your-mason-jar-fairy-lights-in-5-minutes",
    "/blogs/blog/how-to-make-diy-fairy-lights-to-decorate-your-home",
    "/blogs/blog/best-strip-lights-for-diy-project",
    "/blogs/blog/beautiful-diy-fairy-light-decor-ideas",
    "/blogs/blog/gorgeous-fairy-lights-for-your-bedroom-decor-event-or-party",
    "/blogs/blog/9-innovative-ways-to-use-fairy-lihgts-in-you-diy-porject",
    "/blogs/blog/strip-lights-sofa",
    "/blogs/blog/give-your-child-a-dream-of-starry-sky-with-fairy-lights-super-simple-starlight-bottle-diy",
    "/blogs/blog/most-significant-wedding-celebration-motif-patterns",
    "/blogs/blog/smart-bulbs",
    "/products/outdoor-fairy-lights", "/products/wifi-smart-led-strip-lights", "/products/battery-operated-fairy-lights",
    "/products/fake-ivy-leaves", "/products/outdoor-string-lights", "/products/garland-fairy-string-light",
    "/products/led-controller", "/products/fairy-lights", "/products/string-lights", "/products/smart-led-light-bulbs",
    "/products/indoor-fairy-lights", "/collections/smart-lights",
]

errors = []


def err(msg):
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.srcs, self.ids, self.jsonld = [], [], set(), []
        self.title = self.desc = self.canonical = None
        self.missing_alt = 0
        self._in_ld = self._in_title = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                err(f"{self.name}: duplicate id {a['id']}")
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.srcs.append(a.get("src", ""))
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.split()[0])
            if "alt" not in a:
                self.missing_alt += 1
        elif tag == "link" and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest") and a.get("href", "").startswith("/"):
            self.srcs.append(a["href"])
        elif tag == "script" and a.get("src", "").startswith("/"):
            self.srcs.append(a["src"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, ""
        elif tag == "title":
            self._in_title, self._buf = True, ""
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self.jsonld.append(self._buf)
            self._in_ld = False
        if tag == "title" and self._in_title:
            self.title, self._in_title = self._buf, False

    def handle_data(self, data):
        if self._in_ld or self._in_title:
            self._buf += data


def page_file(path):
    return PAGES / ("home.html" if path == "/" else path.lstrip("/") + ".html")


def main():
    files = sorted(PAGES.rglob("*.html"))
    paths = {}
    for f in files:
        rel = f.relative_to(PAGES).as_posix()[:-5]
        paths["/" if rel == "home" else "/" + rel] = f
    titles, descs = {}, {}
    for path, f in paths.items():
        p = Page()
        p.name = path
        p.feed(f.read_text(encoding="utf-8"))
        if p.h1 != 1:
            err(f"{path}: {p.h1} h1 tags")
        if p.missing_alt:
            err(f"{path}: {p.missing_alt} img without alt")
        if path != "/404":
            exp = ORIGIN + ("/" if path == "/" else path)
            if p.canonical != exp:
                err(f"{path}: canonical {p.canonical} != {exp}")
            if p.title in titles:
                err(f"{path}: duplicate title with {titles[p.title]}")
            titles[p.title] = path
            if p.desc in descs:
                err(f"{path}: duplicate description with {descs[p.desc]}")
            descs[p.desc] = path
            if not p.desc or not (70 <= len(p.desc) <= 165):
                err(f"{path}: description length {len(p.desc or '')}")
            if not p.title or len(p.title) > 70:
                err(f"{path}: title length {len(p.title or '')}: {p.title}")
        for blob in p.jsonld:
            try:
                json.loads(blob)
            except ValueError as e:
                err(f"{path}: bad JSON-LD {e}")
        for href in p.links:
            if href.startswith(("mailto:", "http://", "https://", "tel:")):
                if href.startswith("http") and not href.startswith(ORIGIN):
                    err(f"{path}: external link {href}")
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in p.ids:
                    err(f"{path}: missing anchor {href}")
                continue
            target, _, frag = href.partition("#")
            if target in ("/sitemap.xml",):
                continue
            if target != "/" and target.endswith("/"):
                err(f"{path}: trailing slash link {href}")
            if target not in paths:
                err(f"{path}: broken link {href}")
        for src in p.srcs:
            s = src.split("?")[0]
            if not (ROOT / s.lstrip("/")).is_file():
                err(f"{path}: missing asset {src}")
    for u in LEGACY:
        if u not in paths:
            err(f"legacy URL not rebuilt: {u}")
    # sitemap
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [e.text for e in ET.parse(ROOT / "sitemap.xml").getroot().findall("s:url/s:loc", ns)]
    for loc in locs:
        pth = loc[len(ORIGIN):] or "/"
        if pth not in paths:
            err(f"sitemap: {loc} has no page")
    if errors:
        print("\n".join(errors))
        print(f"FAILED: {len(errors)} problem(s)")
        sys.exit(1)
    print(f"OK: {len(paths)} pages, {len(locs)} sitemap URLs, {len(LEGACY)} legacy URLs present")


if __name__ == "__main__":
    main()
