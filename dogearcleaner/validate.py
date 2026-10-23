#!/usr/bin/env python3
"""Post-build checks for dogearcleaner.com. Run after every build:  python3 validate.py

Enforces the brief: every old WordPress URL still resolves, every Amazon link
carries the dogearcleanerjditt-20 tag, and the homepage's visible copy says
"Dog Ear Cleaner" at least 14 times. Plus standard SEO/HTML hygiene.
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from products import AMAZON_TAG

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
BRAND_MIN = 14

# Every URL in the old Yoast sitemaps (2026-10-23). These must never 404.
OLD_URLS = """/ /resources/ /how-to-clean-dog-earss-matters/ /ear-infection-signs/ /cleaning-routines/
/floppy-ear-breeds/ /after-bath-care/ /zymox-ear-cleanser-review/ /virbac-epi-otic-flush-review/
/pet-md-ear-flush-review/ /vetericyn-plus-ear-rinse-review/ /about-us/ /affiliate-disclosure/ /disclaimer/
/privacy-policy/ /terms-of-use/ /contact-us/ /topic/how-to/ /topic/reviews/ /topic/guides/""".split()
OLD_IMAGES = [p.name for p in (ROOT / "backup/wordpress-2026-10-23/media").glob("*.webp")]

errors, warnings = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.imgs, self.scripts_ld = [], [], []
        self.title = self.desc = self.canonical = None
        self._in_title = self._in_ld = False
        self._skip = 0
        self._in_body = False
        self.text = []
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body":
            self._in_body = True
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "a" and a.get("href"):
            self.links.append((a["href"], a.get("rel", "")))
        if tag == "img":
            self.imgs.append(a)
        if tag == "script":
            self._skip += 1
            if a.get("type") == "application/ld+json":
                self._in_ld, self._buf = True, ""
        if tag == "style":
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("script", "style"):
            self._skip -= 1
            if self._in_ld:
                self.scripts_ld.append(self._buf)
                self._in_ld = False

    def handle_data(self, d):
        if self._in_title:
            self.title = (self.title or "") + d
        if self._in_ld:
            self._buf += d
        elif self._in_body and not self._skip:
            self.text.append(d)


def resolve(path):
    path = path.split("#")[0].split("?")[0]
    if path in ("", "/"):
        return (SITE / "home.html").exists()
    f = SITE / path.lstrip("/")
    if path.endswith("/"):
        return (f / "index.html").exists()
    return f.exists()


def main():
    pages = sorted(p for p in SITE.rglob("*.html") if "wp-content" not in p.parts)
    titles, descs = {}, {}
    amazon = 0
    for f in pages:
        rel = "/" + str(f.relative_to(SITE)).replace("index.html", "")
        html = f.read_text(encoding="utf-8")
        pg = Page()
        pg.feed(html)
        if pg.h1 != 1:
            errors.append(f"{rel}: {pg.h1} <h1> tags")
        if not pg.title:
            errors.append(f"{rel}: missing <title>")
        elif rel != "/404.html":
            if len(pg.title) > 66:
                warnings.append(f"{rel}: title {len(pg.title)} chars")
            titles.setdefault(pg.title, []).append(rel)
        if not pg.desc:
            errors.append(f"{rel}: missing meta description")
        elif rel != "/404.html":
            if not 110 <= len(pg.desc) <= 165:
                warnings.append(f"{rel}: description {len(pg.desc)} chars")
            descs.setdefault(pg.desc, []).append(rel)
        if not pg.canonical:
            errors.append(f"{rel}: missing canonical")
        for ld in pg.scripts_ld:
            try:
                json.loads(ld)
            except ValueError as e:
                errors.append(f"{rel}: bad JSON-LD ({e})")
        if "[[" in html:
            errors.append(f"{rel}: unexpanded shortcode")
        for href, rel_attr in pg.links:
            if "amazon." in href:
                amazon += 1
                if f"tag={AMAZON_TAG}" not in href:
                    errors.append(f"{rel}: Amazon link without tag: {href}")
                if "sponsored" not in rel_attr:
                    errors.append(f"{rel}: Amazon link without rel=sponsored")
            elif href.startswith("/") and not href.startswith("//"):
                if not resolve(href):
                    errors.append(f"{rel}: broken internal link {href}")
            elif href.startswith("#") and len(href) > 1 and f'id="{href[1:]}"' not in html:
                errors.append(f"{rel}: missing anchor {href}")
        for im in pg.imgs:
            if im.get("alt") is None:
                errors.append(f"{rel}: <img> without alt ({im.get('src')})")
            src = im.get("src", "")
            if src.startswith("/") and not (SITE / src.lstrip("/").split("?")[0]).exists():
                errors.append(f"{rel}: missing image {src}")
        if rel == "/home.html":
            visible = re.sub(r"\s+", " ", " ".join(pg.text))
            n = visible.count("Dog Ear Cleaner")
            print(f'homepage: "Dog Ear Cleaner" appears {n} times in visible copy (min {BRAND_MIN})')
            if n < BRAND_MIN:
                errors.append(f"homepage brand mentions {n} < {BRAND_MIN}")
        for asset in re.findall(r'(?:href|src)="(/assets/[^"?]+)', html):
            if not (SITE / asset.lstrip("/")).exists():
                errors.append(f"{rel}: missing asset {asset}")

    for t, where in titles.items():
        if len(where) > 1:
            errors.append(f"duplicate title {t!r}: {where}")
    for d, where in descs.items():
        if len(where) > 1:
            errors.append(f"duplicate description: {where}")
    for u in OLD_URLS:
        if not resolve(u):
            errors.append(f"old URL would 404: {u}")
    for name in OLD_IMAGES:
        if not (SITE / "wp-content/uploads/2026/05" / name).exists():
            errors.append(f"old image URL would 404: {name}")
    if (SITE / "index.html").exists():
        errors.append("site/index.html must not exist (host would serve it for unknown paths); use home.html")
    sm = (SITE / "sitemap.xml").read_text()
    for loc in re.findall(r"<loc>https://dogearcleaner\.com([^<]*)</loc>", sm):
        if not resolve(loc):
            errors.append(f"sitemap URL missing: {loc}")
    for u in OLD_URLS:
        if f"https://dogearcleaner.com{u}<" not in sm:
            errors.append(f"old URL not in sitemap: {u}")

    print(f"checked {len(pages)} HTML files, {amazon} Amazon links, {len(OLD_URLS)} legacy URLs")
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    if errors:
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
