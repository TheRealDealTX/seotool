#!/usr/bin/env python3
"""Post-build checks for claimsconsultant.com.

Run after every build. Checks markup balance, JSON-LD validity, internal
links, and the SEO basics that are easy to break and hard to notice.

    python3 validate.py
"""

import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {".git", "assets", "__pycache__", "node_modules"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

errors, warnings = [], []


class Checker(HTMLParser):
    """Tag balance plus a few structural counts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.bad = []
        self.h1 = 0
        self.main = 0
        self.titles = 0
        self.p_depth = 0
        self.nested_p = 0
        self.imgs_without_alt = 0
        self.links = []
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "main":
            self.main += 1
        elif tag == "title":
            self.titles += 1
            self.in_title = True
        elif tag == "img" and not a.get("alt") and a.get("alt") != "":
            self.imgs_without_alt += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "p":
            if self.p_depth:
                self.nested_p += 1
            self.p_depth += 1
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "p":
            self.p_depth = max(self.p_depth - 1, 0)
        if tag == "title":
            self.in_title = False
        if not self.stack:
            self.bad.append("stray </%s>" % tag)
        elif self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.bad.append("unclosed <%s> before </%s>" % (self.stack.pop(), tag))
            if self.stack:
                self.stack.pop()
        else:
            self.bad.append("stray </%s>" % tag)

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


def html_files():
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)


def site_path(fp):
    rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel.lstrip("/")


def main():
    files = sorted(html_files())
    if not files:
        errors.append("no HTML found — run build.py first")
        report()

    known = set()
    for fp in files:
        p = site_path(fp)
        known.add(p)
        if p.endswith("/index.html"):
            known.add(p[: -len("index.html")])

    titles, descriptions, canonicals = {}, {}, {}

    for fp in files:
        path = site_path(fp)
        html = open(fp, encoding="utf-8").read()
        c = Checker()
        c.feed(html)
        c.close()

        # --- markup
        for b in c.bad:
            errors.append("%s: %s" % (path, b))
        if c.stack:
            errors.append("%s: unclosed at EOF: %s" % (path, ", ".join(c.stack[:6])))
        if c.nested_p:
            errors.append("%s: %d nested <p> (a block emitted its own <p>)" % (path, c.nested_p))
        if c.h1 != 1:
            errors.append("%s: %d <h1> (expected exactly 1)" % (path, c.h1))
        if c.main != 1:
            errors.append("%s: %d <main> (expected exactly 1)" % (path, c.main))
        if c.imgs_without_alt:
            errors.append("%s: %d <img> without alt" % (path, c.imgs_without_alt))

        # --- head
        title = c.title_text.strip()
        if not title:
            errors.append("%s: missing <title>" % path)
        elif len(title) > 65:
            warnings.append("%s: title %d chars (>65 may truncate): %s" % (path, len(title), title))
        titles.setdefault(title, []).append(path)

        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        desc = m.group(1) if m else ""
        if not desc:
            errors.append("%s: missing meta description" % path)
        elif not (70 <= len(desc) <= 175):
            warnings.append("%s: description %d chars (aim 70–175)" % (path, len(desc)))
        descriptions.setdefault(desc, []).append(path)

        m = re.search(r'<link rel="canonical" href="([^"]*)"', html)
        if not m:
            errors.append("%s: missing canonical" % path)
        else:
            canonicals.setdefault(m.group(1), []).append(path)

        if 'name="viewport"' not in html:
            errors.append("%s: missing viewport" % path)
        if 'property="og:title"' not in html:
            warnings.append("%s: missing Open Graph title" % path)

        # --- JSON-LD
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if not blocks:
            errors.append("%s: no JSON-LD" % path)
        for blk in blocks:
            try:
                data = json.loads(blk)
            except ValueError as exc:
                errors.append("%s: invalid JSON-LD (%s)" % (path, exc))
                continue
            graph = data.get("@graph", [])
            types = [n.get("@type") for n in graph if isinstance(n, dict)]
            if not graph:
                warnings.append("%s: JSON-LD has no @graph" % path)
            if not any("WebPage" in str(t) or "Article" in str(t) or
                       "CollectionPage" in str(t) or "WebApplication" in str(t) for t in types):
                warnings.append("%s: JSON-LD has no page node" % path)

        # --- links
        for href in c.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if not target.startswith("/"):
                warnings.append("%s: relative link %s" % (path, href))
                continue
            if target in known:
                continue
            if os.path.exists(os.path.join(ROOT, target.lstrip("/"))):
                continue
            errors.append("%s: broken internal link -> %s" % (path, href))

        # --- URLs must not contain spaces (a stray comma-space in a query
        #     string silently breaks webfonts and canonical tags)
        for m in re.finditer(r'(?:href|src|content)="((?:https?:)?//[^"]*)"', html):
            if " " in m.group(1):
                errors.append("%s: space inside URL -> %s" % (path, m.group(1)[:90]))

        # --- US spelling (a Texas firm writing "labour" is a tell)
        brit = re.findall(
            r"\b(?:vapour|colour|odour|armour|honour|labour|rumour|savour|harbour|valour|"
            r"vigour|endeavour|flavour|humour|candour|clamour|glamour|ardour|fervour|rigour|"
            r"demeanour|neighbour|behaviour|favour|mould|smoulder|offence|pretence|licence|"
            r"defence|metre|litre|fibre|theatre|calibre|sombre|lustre|spectre|manoeuvre|"
            r"aluminium|sulphur|draught|jewellery|woollen|labelled|signalling|marvellous|"
            r"skilful|instalment|learnt|spelt|dreamt|leapt|spoilt|tyre|plough|cheque|"
            r"organise|recognise|prioritise|specialise|standardise|apologise|utilise|analyse|"
            r"summarise|minimise|emphasise|criticise|authorise|itemise|customise|finalise|"
            r"optimise|penalise|realise|scrutinise|whilst|amongst|programme|fortnight)\w*",
            html, re.I)
        for b in sorted(set(brit)):
            errors.append("%s: British spelling %r" % (path, b))

        # --- content smells
        if "&amp;amp;" in html or "&amp;mdash;" in html or "&amp;rsquo;" in html:
            errors.append("%s: double-escaped entity" % path)
        if re.search(r"<p>\s*</p>", html):
            warnings.append("%s: empty paragraph" % path)
        if "TODO" in html:
            warnings.append("%s: contains TODO" % path)

    # --- cross-page
    for t, paths in titles.items():
        if len(paths) > 1 and t:
            errors.append("duplicate <title> %r on: %s" % (t, ", ".join(paths)))
    for d, paths in descriptions.items():
        if len(paths) > 1 and d:
            errors.append("duplicate meta description on: %s" % ", ".join(paths))
    for cn, paths in canonicals.items():
        if len(paths) > 1:
            errors.append("duplicate canonical %s on: %s" % (cn, ", ".join(paths)))

    # --- supporting files
    for f in ("sitemap.xml", "robots.txt", ".htaccess", "site.webmanifest", "favicon.svg",
              "assets/css/site.css", "assets/js/site.js", "404.html"):
        if not os.path.exists(os.path.join(ROOT, f)):
            errors.append("missing %s" % f)

    sm = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm):
        xml = open(sm, encoding="utf-8").read()
        locs = re.findall(r"<loc>([^<]+)</loc>", xml)
        for loc in locs:
            p = re.sub(r"^https?://[^/]+", "", loc)
            if p not in known and not os.path.exists(os.path.join(ROOT, p.lstrip("/"))):
                errors.append("sitemap lists missing page: %s" % p)
        indexable = {p for p in known if not p.endswith("/index.html")}
        listed = {re.sub(r"^https?://[^/]+", "", l) for l in locs}
        for p in sorted(indexable - listed):
            if p != "/404.html":
                warnings.append("page not in sitemap: %s" % p)

    report(len(files))


def report(n=0):
    for w in warnings:
        print("warn  %s" % w)
    for e in errors:
        print("ERROR %s" % e)
    print("\n%d pages checked — %d errors, %d warnings" % (n, len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
