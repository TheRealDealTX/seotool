#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: titles (<=60 chars, <=~580px), meta descriptions (110-143 chars, present, unique, matching og/twitter),
one H1 that is the first heading, no skipped heading levels, valid JSON-LD with resolvable @id references and the
required node types, internal links and anchors, image alt text, homepage keyword count, sister-state names,
the canonical-host guard line on every dir/index.php, no dir/index.html pages, and the Search Console file bytes.
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
HOST = "washingtoninsuranceappraiser.com"
KEYWORD = "Washington Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states. None of these names may appear anywhere in the build.
SISTER_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Illinois", "Kentucky", "Maine",
                 "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New Mexico", "New York",
                 "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Rhode Island", "South Carolina", "South Dakota", "Utah",
                 "West Virginia", "Wisconsin", "Wyoming"]
STATE_RE = re.compile(r"\b(" + "|".join(re.escape(s) for s in SISTER_STATES) + r")\b", re.I)
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc, self.meta = [], 0, [], "", None, {}
        self._in, self.ids, self.imgs_noalt, self.heads, self.canonical = None, set(), 0, [], None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("href") and a.get("rel") not in ("preconnect",):
            self.links.append(a["href"])
            if a.get("rel") == "canonical":
                self.canonical = a["href"]
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
            if a.get("name") == "description":
                self.desc = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
        elif tag == "title":
            self._in = "title"

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, d):
        if self._in == "ld":
            self.ld.append(d)
        elif self._in == "title":
            self.title += d


# Approximate Arial widths (per 1000 em) to estimate Google's ~580px title cutoff at 20px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "—": 1000, "–": 556})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp):
    """Page HTML; dir/index.php pages must start with the canonical-host guard and contain no other PHP."""
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        m = GUARD.match(s)
        if not m:
            errors.append(f"{fp}: page does not start with the canonical-host guard")
        else:
            depth = os.path.relpath(fp, ROOT).count("/")
            if int(m.group(1)) != depth:
                errors.append(f"{fp}: guard depth {m.group(1)} != {depth}")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{fp}: stray PHP tag in page HTML")
    return s


def walk_ids(node, defined, refs):
    if isinstance(node, dict):
        if "@id" in node:
            if len(node) == 1:
                refs.append(node["@id"])
            else:
                defined.add(node["@id"])
        for v in node.values():
            walk_ids(v, defined, refs)
    elif isinstance(node, list):
        for v in node:
            walk_ids(v, defined, refs)


def check_ld(rel, blocks, canonical):
    if len(blocks) != 1:
        errors.append(f"{rel}: expected 1 JSON-LD block, found {len(blocks)}")
    for block in blocks:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        defined, refs = set(), []
        walk_ids(data, defined, refs)
        for r in refs:
            if r not in defined:
                errors.append(f"{rel}: unresolved @id reference {r}")
        if "ProfessionalService" not in types or "WebSite" not in types:
            errors.append(f"{rel}: JSON-LD missing ProfessionalService or WebSite")
        pages_ = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if len(pages_) != 1:
            errors.append(f"{rel}: expected exactly one page node, found {len(pages_)}")
            continue
        pn = pages_[0]
        for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
            if k not in pn:
                errors.append(f"{rel}: page node missing {k}")
        if "BreadcrumbList" not in types:
            errors.append(f"{rel}: no BreadcrumbList")
        if canonical and pn.get("url") != canonical:
            errors.append(f"{rel}: page node url {pn.get('url')} != canonical {canonical}")
        biz = next(n for n in graph if n.get("@type") == "ProfessionalService")
        for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
            if k not in biz:
                errors.append(f"{rel}: ProfessionalService missing {k}")
        return types
    return []


titles, descs = {}, {}
files, all_desc = [], []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        if f == "index.html":
            errors.append(f"{full}: index.html pages are not allowed (the host serves them without the guard)")
        if f.endswith(".html") and dp == ROOT and f not in ("home.html", "404.html", GSC_FILE):
            errors.append(f"{full}: unexpected root .html file")
        if f.endswith(".html") and dp != ROOT:
            errors.append(f"{full}: unexpected .html file outside the root")
        if f == GSC_FILE:
            continue  # verification file: checked separately, never treated as a page
        if (f.endswith(".html") and dp == ROOT) or (f == "index.php" and dp != ROOT and "/api" not in dp):
            files.append(full)

# Search Console verification file must exist with exact bytes.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing {GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE}: contents differ from the required single line")

sitemap = open(os.path.join(ROOT, "sitemap.xml")).read()
if GSC_FILE in sitemap:
    errors.append("sitemap.xml lists the Search Console file")
robots = open(os.path.join(ROOT, "robots.txt")).read()
if GSC_FILE in robots or "Disallow: /\n" in robots:
    errors.append("robots.txt blocks the site or the Search Console file")
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page must not exist")

home_count = None
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if GSC_FILE in raw:
        errors.append(f"{rel}: links to the Search Console file")
    if "photo-credits" in raw.lower() or "photo credits" in raw.lower():
        errors.append(f"{rel}: mentions photo credits")
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    url_path = "/" if rel == "/home.html" else ("/404.html" if rel == "/404.html" else rel[:-len("index.php")])
    expect = f"https://{HOST}{url_path}"
    if p.canonical != expect:
        errors.append(f"{rel}: canonical {p.canonical} != {expect}")
    check_ld(rel, p.ld, expect)
    for k in ("og:title", "og:description", "og:image", "og:image:width", "og:image:height", "og:image:alt", "og:url", "twitter:card", "twitter:description", "geo.region"):
        if not p.meta.get(k):
            errors.append(f"{rel}: missing meta {k}")
    t = html.unescape(p.title.strip())
    d = p.desc
    if d is None or not d.strip():
        errors.append(f"{rel}: missing meta description")
        d = ""
    if p.meta.get("og:description") != d or p.meta.get("twitter:description") != d:
        errors.append(f"{rel}: og/twitter description differs from meta description")
    all_desc.append((len(d), rel, d))
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description does not end with a complete sentence")
    prev = 0
    for lv in p.heads:
        if prev and lv > prev + 1:
            errors.append(f"{rel}: heading jump h{prev} -> h{lv}")
            break
        prev = lv
    if p.heads and p.heads[0] != 1:
        errors.append(f"{rel}: first heading is h{p.heads[0]}")
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "//", "data:")):
            continue
        path = href.split("#")[0].split("?")[0]
        frag = href.split("#")[1] if "#" in href else ""
        if not path:
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif frag and target.endswith((".php", ".html")):
            tp = P()
            tp.feed(page_html(target) if target.endswith(".php") else open(target, encoding="utf-8").read())
            if frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
    if rel == "/home.html":
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = m.group(1) if m else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
        mtext = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", mtext)))
        home_count = mtext.count(KEYWORD)
        print(f"homepage '{KEYWORD}': {home_count} in main content")
        if home_count < MIN_HOME_MENTIONS:
            errors.append(f"homepage keyword count {home_count} < {MIN_HOME_MENTIONS}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# Sister-state names anywhere in the text build (pages, scripts, styles, sitemap, PHP).
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg", ".json")):
            fp = os.path.join(dp, f)
            for i, line in enumerate(open(fp, encoding="utf-8", errors="ignore"), 1):
                mm = STATE_RE.search(line)
                if mm:
                    errors.append(f"{fp}:{i}: mentions sister state '{mm.group(1)}'")
                    break

all_desc.sort()
print(f"checked {len(files)} pages")
if all_desc:
    print(f"shortest description {all_desc[0][0]} chars: {all_desc[0][1]} — {all_desc[0][2]}")
    print(f"longest description  {all_desc[-1][0]} chars: {all_desc[-1][1]} — {all_desc[-1][2]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK: 0 errors" if not errors else f"FAILED: {len(errors)} errors")
sys.exit(1 if errors else 0)
