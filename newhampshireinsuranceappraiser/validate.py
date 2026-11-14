#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://newhampshireinsuranceappraiser.com"
KEYWORD = "New Hampshire Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never appear. "Mount Washington" (the NH mountain) is the only allowed use of Washington.
SISTER_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Illinois", "Kentucky", "Maine",
                 "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New Mexico", "New York",
                 "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Rhode Island", "South Carolina", "South Dakota", "Utah",
                 "Washington", "West Virginia", "Wisconsin", "Wyoming"]
BANNED = re.compile(r"\b(" + "|".join(re.escape(s).replace(r"\ ", r"\s+") for s in SISTER_STATES) + r")\b", re.I)
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.metas, self.ids, self.imgs_noalt, self.heads = {}, set(), 0, []
        self._in, self.n_desc = None, 0

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
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
            if tag == "h1":
                self.h1 += 1
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.metas[k] = a.get("content", "")
            if a.get("name") == "description":
                self.desc = a.get("content", "")
                self.n_desc += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
            self.ld.append("")
        elif tag == "title":
            self._in = "title"

    def handle_endtag(self, tag):
        self._in = None

    def handle_data(self, d):
        if self._in == "ld":
            self.ld[-1] += d
        elif self._in == "title":
            self.title += d


# Approximate Arial widths (per 1000 em) to estimate Google's ~580px title cutoff at 20px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


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
        elif int(m.group(1)) != os.path.relpath(fp, ROOT).count("/"):
            errors.append(f"{fp}: guard depth {m.group(1)} is wrong")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{fp}: stray PHP tag in page HTML")
    return s


def check_ids(rel, graph):
    defined, refs = set(), []

    def walk(o):
        if isinstance(o, dict):
            if "@id" in o and len(o) > 1:
                defined.add(o["@id"])
            elif "@id" in o:
                refs.append(o["@id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(graph)
    for r in refs:
        if r not in defined:
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    nodes = graph.get("@graph", [])
    types = [n.get("@type") for n in nodes]
    pages_ = [n for n in nodes if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
    if "ProfessionalService" not in types or "WebSite" not in types:
        errors.append(f"{rel}: JSON-LD missing ProfessionalService or WebSite")
    if len(pages_) != 1:
        errors.append(f"{rel}: JSON-LD has {len(pages_)} page nodes (want 1)")
    else:
        pg = pages_[0]
        for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
            if k not in pg:
                errors.append(f"{rel}: page node missing {k}")


# ---- structural checks on the build output
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist (host would serve it before index.php)")
for need in ("index.php", "_guard.php", "home.html", "404.html", "sitemap.xml", "robots.txt", GSC_FILE):
    if not os.path.exists(os.path.join(ROOT, need)):
        errors.append(f"missing {need}")
gsc = os.path.join(ROOT, GSC_FILE)
if os.path.exists(gsc) and open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} content is not exactly the verification line")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits/ must not exist")

files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        if f == "index.html" and dp != ROOT:
            errors.append(f"{full}: dir/index.html pages are not allowed (use dir/index.php)")
        if f.endswith(".html") and dp == ROOT and f not in ("home.html", "404.html", GSC_FILE):
            errors.append(f"{full}: unexpected root .html file")
        if (f.endswith(".html") and f != GSC_FILE) or (f == "index.php" and dp != ROOT):
            files.append(full)

titles, descs, longest = {}, {}, []
sitemap = open(os.path.join(ROOT, "sitemap.xml")).read() if os.path.exists(os.path.join(ROOT, "sitemap.xml")) else ""
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if not p.ld:
        errors.append(f"{rel}: no JSON-LD")
    for block in p.ld:
        try:
            check_ids(rel, json.loads(block))
        except json.JSONDecodeError as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    d = p.desc
    if d is None or p.n_desc != 1:
        errors.append(f"{rel}: needs exactly one meta description (found {p.n_desc})")
        d = ""
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    longest.append((len(d), rel, d))
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description doesn't end with a full sentence")
    for k in ("og:description", "twitter:description"):
        if p.metas.get(k) != d:
            errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:title", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:card", "geo.region"):
        if not p.metas.get(k):
            errors.append(f"{rel}: missing meta {k}")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', raw)
    if not m or not m.group(1).startswith(DOMAIN + "/"):
        errors.append(f"{rel}: canonical missing or off-domain")
    elif not rel.endswith("404.html") and f"<loc>{m.group(1)}</loc>" not in sitemap:
        errors.append(f"{rel}: canonical not in sitemap.xml")
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
        if "photo-credits" in path:
            errors.append(f"{rel}: links to photo credits")
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
        mm = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = mm.group(1) if mm else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
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

# Sister-state names anywhere in pages, scripts or styles (Mount Washington excepted)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            fp = os.path.join(dp, f)
            s = open(fp, encoding="utf-8", errors="ignore").read()
            s = re.sub(r"Mount\s+Washington", "", s)
            for m in BANNED.finditer(s):
                errors.append(f"{fp}: mentions sister state '{m.group(0)}'")

# sitemap/robots must not reference the verification file; robots must not block it
rb = open(os.path.join(ROOT, "robots.txt")).read() if os.path.exists(os.path.join(ROOT, "robots.txt")) else ""
if GSC_FILE in sitemap or GSC_FILE in rb:
    errors.append("verification file must not be listed in sitemap.xml or robots.txt")

longest.sort()
print(f"checked {len(files)} pages; descriptions {longest[0][0]}–{longest[-1][0]} chars")
print(f"  shortest: {longest[0][0]} {longest[0][1]}: {longest[0][2]}")
print(f"  longest:  {longest[-1][0]} {longest[-1][1]}: {longest[-1][2]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
