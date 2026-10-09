#!/usr/bin/env python3
"""Post-build checks for agadecor.com. Exit code 1 on any failure."""

import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "public")
routes = dict(re.findall(r"^  '([^']*)' => \['([^']+)'", open(os.path.join(PUB, "routes.php")).read(), re.M))
errors = []

# URLs that carry backlinks or rankings on the old site: must resolve to a page.
MUST_EXIST = ["/", "/decor-rental", "/single-post/2014/03/01/Modern-Luxury-Bride-Northshore-Magazine",
              "/single-post/2015/09/27/Give-me-everything-that-sparkles", "/single-post/2015/11/15/Trends-of-2016",
              "/about-us", "/services", "/wedding-planing", "/destination-weddings", "/linens", "/furniture",
              "/vases", "/extras", "/vendors", "/contact-us", "/blog"]
for u in MUST_EXIST:
    if u not in routes:
        errors.append(f"missing legacy route {u}")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.links = []; self.imgs = []; self.title = ""; self.desc = ""; self.ld = []; self._t = None; self.canon = ""
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "h1": self.h1 += 1
        if t == "a" and a.get("href"): self.links.append(a["href"])
        if t == "img": self.imgs.append(a)
        if t == "title": self._t = "title"
        if t == "script" and a.get("type") == "application/ld+json": self._t = "ld"
        if t == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": self.canon = a.get("href", "")
    def handle_endtag(self, t): self._t = None
    def handle_data(self, d):
        if self._t == "title": self.title += d
        if self._t == "ld": self.ld.append(d)


titles, descs = {}, {}
banned = re.compile(r"224-427-0220|Aga Galus|wixstatic|Lorem ipsum", re.I)
for path, f in routes.items():
    src = open(os.path.join(PUB, "pages", f)).read()
    p = P(); p.feed(src)
    where = f"{path} ({f})"
    if p.h1 != 1: errors.append(f"{where}: {p.h1} h1")
    for ld in p.ld:
        try: json.loads(ld)
        except Exception as e: errors.append(f"{where}: bad JSON-LD {e}")
    if not p.desc or len(p.desc) > 165: errors.append(f"{where}: description length {len(p.desc)}")
    if len(p.title) > 90: errors.append(f"{where}: title too long ({len(p.title)})")
    if p.title in titles: errors.append(f"{where}: duplicate title with {titles[p.title]}")
    if p.desc in descs: errors.append(f"{where}: duplicate description with {descs[p.desc]}")
    titles[p.title] = path; descs[p.desc] = path
    if p.canon != "https://agadecor.com" + path: errors.append(f"{where}: canonical {p.canon}")
    if banned.search(src): errors.append(f"{where}: banned string {banned.search(src).group(0)}")
    for href in p.links:
        if href.startswith(("http", "mailto:", "#")): continue
        u = href.split("#")[0].split("?")[0]
        if u and u not in routes and u not in ("/sitemap.xml",):
            errors.append(f"{where}: broken link {href}")
    for im in p.imgs:
        if "alt" not in im: errors.append(f"{where}: img without alt {im.get('src')}")
        s = im.get("src", "")
        if s.startswith("/") and not os.path.exists(os.path.join(PUB, s.lstrip("/"))):
            errors.append(f"{where}: missing image {s}")
        for part in (im.get("srcset") or "").split(","):
            s2 = part.strip().split(" ")[0]
            if s2 and not os.path.exists(os.path.join(PUB, s2.lstrip("/"))): errors.append(f"{where}: missing srcset {s2}")

if errors:
    print("\n".join(errors)); print(f"FAILED: {len(errors)} problems"); sys.exit(1)
print(f"OK: {len(routes)} pages valid")
