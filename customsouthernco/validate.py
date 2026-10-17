#!/usr/bin/env python3
"""Post-build checks for ./site/. Exits non-zero on any error."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.srcs, self.imgs_no_alt, self.ids = [], [], 0, []
        self.ld, self._in_ld, self.title, self._in_title, self.meta = [], False, "", False, {}

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") == "stylesheet" and a.get("href"))):
            self.srcs.append(a.get("src") or a.get("href"))
        if tag == "img":
            if a.get("alt") is None:
                self.imgs_no_alt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.srcs.append(part.strip().split()[0])
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self.ld.append("")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href")

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_ld:
            self.ld[-1] += d
        if self._in_title:
            self.title += d


def url_to_file(u):
    u = u.split("#")[0].split("?")[0]
    if u in ("", "/"):
        return SITE / "home.html"
    f = SITE / u.lstrip("/")
    return f / "index.html" if u.endswith("/") else f


titles, descs = {}, {}
pages = sorted(SITE.rglob("*.html"))
for f in pages:
    rel = "/" + str(f.relative_to(SITE)).replace("index.html", "")
    p = P()
    text = f.read_text(encoding="utf-8")
    p.feed(text)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_no_alt:
        errors.append(f"{rel}: {p.imgs_no_alt} images without alt")
    for block in p.ld:
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD {e}")
    for d in set(i for i in p.ids if p.ids.count(i) > 1):
        errors.append(f"{rel}: duplicate id {d}")
    if "{{" in text:
        errors.append(f"{rel}: unrendered placeholder")
    for u in p.links:
        if u.startswith(("http", "mailto:", "#")):
            if u.startswith("http") and "customsouthernco.com" in u and "sharer" not in u and "pinterest" not in u:
                warns.append(f"{rel}: absolute internal link {u}")
            continue
        if u == "/contact.php":
            continue
        if not url_to_file(u).exists():
            errors.append(f"{rel}: broken link {u}")
    for s in p.srcs:
        if s.startswith("http"):
            continue
        if not url_to_file(s).exists():
            errors.append(f"{rel}: missing asset {s}")
    if f.name != "404.html" and rel != "/home.html":
        titles.setdefault(p.title, []).append(rel)
        descs.setdefault(p.meta.get("description"), []).append(rel)
        d = p.meta.get("description", "")
        if not (70 <= len(d) <= 170):
            warns.append(f"{rel}: description length {len(d)}")
        if len(p.title) > 75:
            warns.append(f"{rel}: title length {len(p.title)}: {p.title}")
for t, r in titles.items():
    if len(r) > 1:
        errors.append(f"duplicate title {t!r}: {r}")
for t, r in descs.items():
    if len(r) > 1:
        errors.append(f"duplicate description: {r}")

# every URL that had traffic or backlinks must exist
MUST = """history-of-prince-albert-tins how-to-make-laundry-detergent-with-3-ingredients how-to-make-a-faux-tinsel-tree pie-bird
diy-spindle-snowman-ornament how-to-make-faux-bread easy-vintage-photo-shelf-sitter rustic-patriotic-decor-diy quick-vintage-door-knob-tree
easy-vintage-spice-tin-diy easy-christmas-spindle-ornaments easy-ball-jar-decor-diy how-to-clean-old-jars easy-vintage-valentine-banner
repurposed-yardstick-decor-project easy-pumpkin-funnel-diy what-vintage-jars-to-look-for rustic-cloche-diy-for-spring vintage-jello-mold-pumpkin-diy
succulent-dustpan-decor history-of-the-red-barn simple-barn-wood-christmas-trees upcycled-vintage-cutting-board-for-spring lets-go-pickin-for-antiques
easy-hymn-tea-stain-diy old-window-decoupage-mirror how-to-repurpose-antique-light-globes easy-vintage-cutting-board-decor the-christmas-barn-sale-trail
rustic-tiered-tray-diy easy-valentine-book-decor-diy""".split()
for s in MUST:
    if not (SITE / s / "index.html").exists():
        errors.append(f"missing legacy URL /{s}/")
sm = (SITE / "sitemap.xml").read_text()
for s in MUST:
    if f"/{s}/</loc>" not in sm:
        errors.append(f"/{s}/ not in sitemap.xml")
if (SITE / "index.html").exists():
    errors.append("site/index.html must not exist (see README hosting note)")

for w in warns:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(pages)} pages checked, {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
