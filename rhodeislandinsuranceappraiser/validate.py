#!/usr/bin/env python3
"""Post-build checks for ./public. Exits 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
HOST = "rhodeislandinsuranceappraiser.com"
DOMAIN = "https://" + HOST
KEYWORD = "Rhode Island Insurance Appraiser"
MIN_HOME_MENTIONS = 14
# Sister-site states: none of these names may appear anywhere in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland",
          "Massachusetts", "Missouri", "Montana", "Nevada", "New Jersey", "New York", "North Carolina", "Ohio",
          "South Carolina", "West Virginia", "Wyoming"]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", ""
        self._in, self.ids, self.imgs_noalt, self.heads, self.meta, self.canon = None, set(), 0, [], {}, None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            if a["id"] in self.ids:
                errors.append(f"{self.rel}: duplicate id #{a['id']}")
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
            if tag == "link" and a.get("rel") == "canonical":
                self.canon = a["href"]
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if re.fullmatch(r"h[1-6]", tag):
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


# Arial widths (per 1000 em) to estimate Google's ~580px title cutoff at 20px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, "–": 556, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp, rel):
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        m = GUARD.match(s)
        if not m:
            errors.append(f"{rel}: page does not start with the canonical-host guard")
        elif int(m.group(1)) != rel.strip("/").count("/"):
            errors.append(f"{rel}: guard depth {m.group(1)} is wrong")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{rel}: stray PHP tag in page HTML")
    return s


def check_graph(rel, data, is_404):
    graph = data.get("@graph", [])
    defined = {}

    def walk(o, top):
        if isinstance(o, dict):
            if "@id" in o and len(o) > 1:
                defined[o["@id"]] = o
            for v in o.values():
                walk(v, False)
        elif isinstance(o, list):
            for v in o:
                walk(v, False)
    walk(graph, True)
    refs = []

    def refs_of(o):
        if isinstance(o, dict):
            if set(o) == {"@id"}:
                refs.append(o["@id"])
            for v in o.values():
                refs_of(v)
        elif isinstance(o, list):
            for v in o:
                refs_of(v)
    refs_of(graph)
    for r in refs:
        if r not in defined:
            errors.append(f"{rel}: JSON-LD @id reference {r} does not resolve")
    types = [n.get("@type") for n in graph]
    biz = next((n for n in graph if n.get("@type") == "ProfessionalService"), None)
    if not biz:
        errors.append(f"{rel}: no ProfessionalService node")
    else:
        for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
            if k not in biz:
                errors.append(f"{rel}: ProfessionalService missing {k}")
        if biz.get("address", {}).get("addressRegion") != "RI":
            errors.append(f"{rel}: addressRegion should be RI")
    if "WebSite" not in types:
        errors.append(f"{rel}: no WebSite node")
    pages_ = [n for n in graph if n.get("@type") in PAGE_TYPES]
    if is_404:
        return
    if len(pages_) != 1:
        errors.append(f"{rel}: expected exactly one page node, found {len(pages_)}")
        return
    pg = pages_[0]
    for k in ("primaryImageOfPage", "mainEntity"):
        if k not in pg:
            errors.append(f"{rel}: page node missing {k}")
    if rel != "/home.html" and "breadcrumb" not in pg:
        errors.append(f"{rel}: page node missing breadcrumb")


titles, descs, files = {}, {}, []
for dp, dirs, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        if f == "index.html":
            errors.append(f"{full}: index.html pages are not allowed (the host would bypass the guard)")
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(full)
for need in ("_guard.php", "index.php", "home.html", "404.html", "robots.txt", "sitemap.xml", "favicon.ico", "favicon.svg", "apple-touch-icon.png", "site.webmanifest", "assets/img/og-image.jpg"):
    if not os.path.exists(os.path.join(ROOT, need)):
        errors.append(f"missing /{need}")

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.rel = rel
    src = page_html(fp, rel)
    p.feed(src)
    is_404 = rel.endswith("404.html")
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            check_graph(rel, json.loads(block), is_404)
        except json.JSONDecodeError as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if not p.ld:
        errors.append(f"{rel}: no JSON-LD")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    if not is_404:
        expect = DOMAIN + ("/" if rel == "/home.html" else rel[:-len("index.php")])
        if p.canon != expect:
            errors.append(f"{rel}: canonical {p.canon} != {expect}")
        for k in ("og:title", "og:description", "og:image", "og:image:width", "og:image:height", "og:image:alt", "og:url", "twitter:card", "twitter:image", "geo.region"):
            if not p.meta.get(k):
                errors.append(f"{rel}: missing meta {k}")
        titles.setdefault(t, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if len(t) > 60:
            errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
        if title_px(t) > 580:
            errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
        if not 110 <= len(p.desc) <= 150:
            errors.append(f"{rel}: description {len(p.desc)} chars (want 110-150): {p.desc}")
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
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
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
            tp.rel = path
            tp.feed(open(target, encoding="utf-8").read())
            if frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
    if rel == "/home.html":
        m = re.search(r"<main[^>]*>(.*)</main>", src, re.S)
        mtext = re.sub(r"<script.*?</script>", " ", m.group(1), flags=re.S) if m else ""
        mtext = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", mtext)))
        n_main = mtext.count(KEYWORD)
        print(f"homepage '{KEYWORD}': {n_main} in main content")
        if n_main < MIN_HOME_MENTIONS:
            errors.append(f"homepage keyword count {n_main} < {MIN_HOME_MENTIONS}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# No sister-state names anywhere in the build (pages, scripts, styles, data).
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            fp = os.path.join(dp, f)
            for mm in set(x.group(1) for x in BANNED_RE.finditer(open(fp, encoding="utf-8", errors="ignore").read())):
                errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions sister state '{mm}'")

# Sitemap entries must map to real page files.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "sitemap.xml")) else ""
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    path = loc.replace(DOMAIN, "")
    tgt = os.path.join(ROOT, "home.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.php")
    if not os.path.exists(tgt):
        errors.append(f"sitemap entry without a page: {loc}")

print(f"checked {len(files)} pages, {len(re.findall('<loc>', sm))} sitemap URLs")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
