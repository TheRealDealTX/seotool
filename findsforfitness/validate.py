#!/usr/bin/env python3
"""Post-build checks for ./public: one H1, unique titles/descriptions, valid JSON-LD,
no broken internal links or missing assets, alt text on every image."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

OUT = Path(__file__).resolve().parent / "public"
errors = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ""
        self.desc = ""
        self.refs = []
        self.ld = []
        self._in_title = self._in_ld = False
        self.imgs_no_alt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self.ld.append("")
        if tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        for k in ("href", "src"):
            v = a.get(k)
            if v and v.startswith("/") and not v.startswith("//"):
                self.refs.append(v)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self.ld[-1] += data


def resolve(ref):
    path = ref.split("#")[0].split("?")[0]
    if path in ("/", ""):
        return OUT / "home.html"
    p = OUT / path.lstrip("/")
    if path.endswith("/"):
        return p / "index.html"
    return p


titles, descs = {}, {}
files = [p for p in OUT.rglob("*.html")]
for f in files:
    rel = "/" + str(f.relative_to(OUT))
    pg = Page()
    pg.feed(f.read_text(encoding="utf-8"))
    if pg.h1 != 1:
        errors.append(f"{rel}: {pg.h1} h1 tags")
    if pg.imgs_no_alt:
        errors.append(f"{rel}: {pg.imgs_no_alt} images without alt")
    for block in pg.ld:
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    if rel != "/404.html":
        titles.setdefault(pg.title, []).append(rel)
        descs.setdefault(pg.desc, []).append(rel)
        if not 20 <= len(pg.title) <= 65:
            errors.append(f"{rel}: title length {len(pg.title)}: {pg.title}")
        if not 70 <= len(pg.desc) <= 170:
            errors.append(f"{rel}: description length {len(pg.desc)}")
    for ref in set(pg.refs):
        if ref.startswith("/contact.php"):
            continue
        if not resolve(ref).exists():
            errors.append(f"{rel}: broken link {ref}")
for t, pages in titles.items():
    if len(pages) > 1:
        errors.append(f"duplicate title {t!r}: {pages}")
for d, pages in descs.items():
    if len(pages) > 1:
        errors.append(f"duplicate description: {pages}")

# legacy URLs that must keep resolving
for legacy in ("/best-tennis-shoes-for-flat-feet/", "/healthy-breakfast-foods-for-weight-loss/",
               "/category/skin_care/", "/category/weight_loss/", "/category/workout/", "/category/product-reviews/",
               "/category/health-tips/", "/privacy-policy/", "/terms-of-service/", "/affiliate-disclosure/", "/disclaimers/"):
    if not resolve(legacy).exists():
        errors.append(f"legacy URL missing: {legacy}")

sitemap = (OUT / "sitemap.xml").read_text()
for loc in re.findall(r"<loc>https://findsforfitness\.com(/[^<]*)</loc>", sitemap):
    if not resolve(loc).exists():
        errors.append(f"sitemap url missing: {loc}")

print(f"checked {len(files)} html files")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("all checks passed")
