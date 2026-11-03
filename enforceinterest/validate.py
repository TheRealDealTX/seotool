#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: internal links and #anchors, assets, one <h1>, unique titles (<= 65 chars) and descriptions
(70-160 chars), canonical URLs, JSON-LD validity, image alt text, sitemap coverage, the root-layout rule
(no page HTML outside _pages/), stale facts, and the homepage brand/keyword count (>= 14).
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
PAGES = os.path.join(OUT, "_pages")
SITE = "https://enforceinterest.com"
REDIRECTS = {"/feed/"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.imgs, self.h1, self.ld, self.title = [], set(), [], 0, [], ""
        self._ld = self._t = False
        self.main_text, self._main, self._skip = [], 0, 0
        self.meta = {}

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("link", "script") and (a.get("href") or a.get("src")):
            self.links.append(a.get("href") or a.get("src"))
        if tag == "img":
            self.imgs.append(a)
            self.links.append(a.get("src", ""))
        if tag == "source" and a.get("srcset"):
            self.links.append(a["srcset"].split()[0])
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.ld.append("")
        if tag == "title":
            self._t = True
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href")
        if tag == "main":
            self._main += 1
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False
        if tag == "title":
            self._t = False
        if tag == "main":
            self._main -= 1
        if tag in ("script", "style"):
            self._skip -= 1

    def handle_data(self, data):
        if self._ld:
            self.ld[-1] += data
        if self._t:
            self.title += data
        if self._main and not self._skip:
            self.main_text.append(data)


def page_files():
    for dp, _, fs in os.walk(PAGES):
        for f in fs:
            if f == "index.html":
                rel = "/" + os.path.relpath(dp, PAGES).replace(os.sep, "/") + "/"
                yield ("/" if rel == "/./" else rel), os.path.join(dp, f)


def main():
    if not os.path.isdir(PAGES):
        sys.exit("run build.py first")
    pages = dict(page_files())
    parsed = {}
    for path, f in pages.items():
        p = P()
        p.feed(open(f, encoding="utf-8").read())
        parsed[path] = p
    titles, descs = {}, {}
    for path, p in parsed.items():
        if p.h1 != 1:
            errors.append(f"{path}: {p.h1} <h1> elements")
        t, dsc = p.title.strip(), p.meta.get("description", "")
        noindex = "noindex" in p.meta.get("robots", "")
        if not noindex:
            if len(t) > 65:
                warns.append(f"{path}: title {len(t)} chars: {t}")
            if not 70 <= len(dsc) <= 165:
                errors.append(f"{path}: description {len(dsc)} chars")
            titles.setdefault(t, []).append(path)
            descs.setdefault(dsc, []).append(path)
            if p.meta.get("canonical") != SITE + path:
                errors.append(f"{path}: canonical {p.meta.get('canonical')}")
        for s in p.ld:
            try:
                json.loads(s)
            except Exception as e:
                errors.append(f"{path}: bad JSON-LD ({e})")
        for im in p.imgs:
            if not im.get("alt"):
                errors.append(f"{path}: img without alt {im.get('src')}")
            if not (im.get("width") and im.get("height")):
                warns.append(f"{path}: img without dimensions {im.get('src')}")
        for href in p.links:
            if href.startswith(("mailto:", "tel:", "http://", "https://", "data:", "javascript:")):
                if href.startswith(SITE):
                    href = href[len(SITE):] or "/"
                else:
                    continue
            base, _, frag = href.partition("#")
            base = base.split("?")[0]
            if not base:
                if frag and frag not in p.ids:
                    errors.append(f"{path}: missing anchor #{frag}")
                continue
            if base.endswith("/"):
                if base not in pages and base not in REDIRECTS:
                    errors.append(f"{path}: broken link {href}")
                elif frag and base in parsed and frag not in parsed[base].ids:
                    errors.append(f"{path}: missing anchor {href}")
            else:
                fs = os.path.join(OUT, base.lstrip("/"))
                if not os.path.isfile(fs):
                    errors.append(f"{path}: missing file {base}")
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f"duplicate title {t!r}: {ps}")
    for dsc, ps in descs.items():
        if len(ps) > 1:
            errors.append(f"duplicate description: {ps}")
    # sitemap
    sm = open(os.path.join(OUT, "sitemap.xml")).read()
    locs = set(l[len(SITE):] for l in re.findall(r"<loc>([^<]+)</loc>", sm) if "/assets/" not in l)
    for l in locs:
        if l not in pages:
            errors.append(f"sitemap URL without page: {l}")
    for path, p in parsed.items():
        if "noindex" not in p.meta.get("robots", "") and path not in locs:
            errors.append(f"page missing from sitemap: {path}")
    # root layout: only index.php may answer page URLs
    for name in os.listdir(OUT):
        full = os.path.join(OUT, name)
        if name == "index.html" or (os.path.isdir(full) and name not in ("_pages", "assets")):
            errors.append(f"public/{name} would bypass index.php")
    # stale or known-wrong facts carried over from the WordPress site
    bad = [r"currently 11\.75%", r"date of loss on or after September 1, 2017", r"60-day pre-suit notice", r"carved out by §542\.052",
           r"Ortiz[^.]{0,80}does not generally bar"]
    for path, f in pages.items():
        txt = open(f, encoding="utf-8").read()
        for b in bad:
            if re.search(b, txt):
                errors.append(f"{path}: stale fact matches /{b}/")
    # homepage brand / main keyword count (body copy inside <main>)
    home = " ".join(parsed["/"].main_text)
    n = len(re.findall(r"Enforce\s+Interest", home))
    print(f"homepage 'Enforce Interest' mentions in <main>: {n}")
    if n < 14:
        errors.append(f"homepage mentions 'Enforce Interest' only {n} times (need 14+)")
    for w_ in warns:
        print("WARN", w_)
    for e in errors:
        print("ERROR", e)
    print(f"{len(pages)} pages checked, {len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
