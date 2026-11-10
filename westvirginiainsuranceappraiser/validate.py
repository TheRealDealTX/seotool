#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "West Virginia Insurance Appraiser"
DOMAIN = "https://westvirginiainsuranceappraiser.com"
# Sister sites on the same Hostinger account: their state names must never leak into this build.
# ("Virginia" alone can't be banned: it is part of this state's name.)
BANNED = ["Alabama", "Florida", "Georgia", "Carolina", "Arizona", "Missouri", "Montana", "Nevada", "Texas"]
MIN_HOME_MENTIONS = 14
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", ""
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self._skip = 0
        self.heads = []
        self.meta, self.canon = {}, ""
        self.imgs_nosize = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "meta" and (a.get("property") or a.get("name")):
            self.meta[a.get("property") or a.get("name")] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href", "")
        if tag == "img" and not (a.get("width") and a.get("height")):
            self.imgs_nosize += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
        elif tag == "title":
            self._in = "title"
        if tag in ("script", "style", "head"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip -= 1
        self._in = None

    def handle_data(self, d):
        if self._in == "ld":
            self.ld.append(d)
        elif self._in == "title":
            self.title += d
        if not self._skip:
            self.text.append(d)


# Approximate Arial widths (per 1000 em) to estimate Google's ~580px title cutoff at 20px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})
def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}


def check_graph(rel, data):
    """Every {"@id": x} reference must resolve to a node defined in the same graph; one page node with links."""
    graph = data.get("@graph", [])
    defined, refs = set(), []

    def walk(o):
        if isinstance(o, dict):
            if "@id" in o and len(o) == 1:
                refs.append(o["@id"])
            elif "@id" in o:
                defined.add(o["@id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(graph)
    for r in refs:
        if r not in defined:
            errors.append(f"{rel}: unresolved @id reference {r}")
    types = [n.get("@type") for n in graph]
    for t in ("ProfessionalService", "WebSite"):
        if t not in types:
            errors.append(f"{rel}: JSON-LD graph lacks {t}")
    pagen = [n for n in graph if n.get("@type") in PAGE_TYPES]
    if rel.endswith("404.html"):
        return
    if len(pagen) != 1:
        errors.append(f"{rel}: expected exactly one page node, found {len(pagen)}")
        return
    pn = pagen[0]
    for k in ("primaryImageOfPage", "mainEntity", "isPartOf"):
        if k not in pn:
            errors.append(f"{rel}: page node missing {k}")
    if rel != "/home.html" and "breadcrumb" not in pn:
        errors.append(f"{rel}: page node missing breadcrumb")
    org = next(n for n in graph if n.get("@type") == "ProfessionalService")
    for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
        if k not in org:
            errors.append(f"{rel}: ProfessionalService missing {k}")


titles, descs = {}, {}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            files.append(os.path.join(dp, f))

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(open(fp, encoding="utf-8").read())
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            check_graph(rel, json.loads(block))
        except ValueError as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if p.imgs_nosize:
        errors.append(f"{rel}: {p.imgs_nosize} images without width/height")
    want = DOMAIN + ("/" if rel == "/home.html" else rel[:-len("index.html")] if rel.endswith("/index.html") else rel)
    if p.canon != want:
        errors.append(f"{rel}: canonical {p.canon!r} != {want!r}")
    for k in ("og:title", "og:description", "og:url", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:card", "twitter:image", "geo.region"):
        if not p.meta.get(k):
            errors.append(f"{rel}: missing meta {k}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    if not rel.endswith("404.html"):
        titles.setdefault(t, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if len(t) > 60:
            errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
        if title_px(t) > 580:
            errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
        if not 110 <= len(p.desc) <= 150:
            errors.append(f"{rel}: description {len(p.desc)} chars (want 110-150)")
    prev = 0
    for lv in p.heads:
        if prev and lv > prev + 1:
            errors.append(f"{rel}: heading jump h{prev} -> h{lv}")
            break
        prev = lv
    if p.heads and p.heads[0] != 1:
        errors.append(f"{rel}: first heading is h{p.heads[0]}")
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "//")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path:
            frag = href.split("#")[1] if "#" in href else ""
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
    if rel == "/home.html":
        main = " ".join(p.text)
        main = re.sub(r"\s+", " ", main)
        body_only = main.split("Skip to content", 1)[-1]
        n_all = body_only.count(KEYWORD)
        # Count inside <main> only (exclude header/footer brand text)
        raw = open(fp, encoding="utf-8").read()
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
        n_main = mtext.count(KEYWORD)
        print(f"homepage '{KEYWORD}': {n_main} in main content, {n_all} in all visible text")
        if n_main < MIN_HOME_MENTIONS:
            errors.append(f"homepage keyword count {n_main} < {MIN_HOME_MENTIONS}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# Stray references to sister-site states (also check JS/CSS/XML/PHP output)
other = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith((".js", ".css", ".xml", ".txt", ".php", ".webmanifest", ".svg"))]
for fp in files + other:
    s = open(fp, encoding="utf-8").read()
    for word in BANNED:
        if re.search(word, s, re.I):
            errors.append(f"{os.path.relpath(fp, ROOT)}: mentions sister state {word}")

print(f"checked {len(files)} html files")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
