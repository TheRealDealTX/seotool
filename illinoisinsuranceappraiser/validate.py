#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://illinoisinsuranceappraiser.com"
KEYWORD = "Illinois Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states (every other *insuranceappraiser* site on the account) must never appear in the build.
SISTER_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland",
    "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New York", "North Carolina",
    "North Dakota", "Ohio", "Oklahoma", "Rhode Island", "South Carolina", "Utah", "West Virginia", "Wisconsin", "Wyoming",
]
STATE_RE = re.compile(r"\b(" + "|".join(re.escape(s) for s in SISTER_STATES) + r")\b")
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.og_desc = self.tw_desc = None
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self.heads, self.canonical = [], None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            if not (tag == "link" and a.get("rel") in ("canonical", "preconnect")):
                self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            if a.get("name") == "description":
                self.desc = a.get("content", "")
            if a.get("property") == "og:description":
                self.og_desc = a.get("content", "")
            if a.get("name") == "twitter:description":
                self.tw_desc = a.get("content", "")
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
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, "–": 556, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, \d+\) \. '/_guard\.php'; \?>\n")


def page_html(fp):
    """Page HTML; dir/index.php pages must start with the canonical-host guard and contain no other PHP."""
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        if not GUARD.match(s):
            errors.append(f"{fp}: page does not start with the canonical-host guard")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{fp}: stray PHP tag in page HTML")
    return s


def walk_ids(node, defined, refs):
    if isinstance(node, dict):
        if "@id" in node:
            (refs if len(node) == 1 else defined).add(node["@id"])
        for v in node.values():
            walk_ids(v, defined, refs)
    elif isinstance(node, list):
        for v in node:
            walk_ids(v, defined, refs)


# ---- structural rules for the host
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist (host would serve it before index.php)")
for dp, _, fs in os.walk(ROOT):
    if dp != ROOT and "index.html" in fs:
        errors.append(f"{os.path.relpath(dp, ROOT)}/index.html exists: pages must be dir/index.php")
root_html = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
if root_html != sorted(["404.html", "home.html", GSC_FILE]):
    errors.append(f"unexpected root .html files: {root_html}")
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc) or open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} missing or not byte-exact")
for must in ("_guard.php", "index.php", "robots.txt", "sitemap.xml", "favicon.ico", "favicon.svg", "apple-touch-icon.png", "site.webmanifest", "assets/img/og-image.jpg"):
    if not os.path.exists(os.path.join(ROOT, must)):
        errors.append(f"missing {must}")
robots = open(os.path.join(ROOT, "robots.txt")).read()
if GSC_FILE in robots:
    errors.append("robots.txt mentions the Search Console file")
smap = open(os.path.join(ROOT, "sitemap.xml")).read()
if GSC_FILE in smap or "photo-credits" in smap:
    errors.append("sitemap.xml lists the Search Console file or photo credits")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page exists")

files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == GSC_FILE and dp == ROOT:
            continue
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

titles, descs, all_desc = {}, {}, []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    graph_ok = False
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        pages_n = [n for n in graph if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
        if "ProfessionalService" not in types or "WebSite" not in types or len(pages_n) != 1:
            errors.append(f"{rel}: JSON-LD graph needs ProfessionalService, WebSite and exactly one page node (has {types})")
        else:
            pn = pages_n[0]
            for k in ("primaryImageOfPage", "mainEntity", "breadcrumb"):
                if k not in pn and not (k == "breadcrumb" and rel.endswith("404.html")):
                    errors.append(f"{rel}: page node missing {k}")
            graph_ok = True
        defined, refs = set(), set()
        walk_ids(graph, defined, refs)
        for r in refs - defined:
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    if not graph_ok and not p.ld:
        errors.append(f"{rel}: no JSON-LD")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    if "photo-credits" in raw:
        errors.append(f"{rel}: links to photo credits")
    t = html.unescape(p.title.strip())
    if p.desc is None:
        errors.append(f"{rel}: missing meta description")
        d = ""
    else:
        d = html.unescape(p.desc)
    if p.og_desc is None or html.unescape(p.og_desc) != d or p.tw_desc is None or html.unescape(p.tw_desc) != d:
        errors.append(f"{rel}: og:description / twitter:description must equal the meta description")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description should end with a full sentence: {d}")
    all_desc.append((len(d), rel, d))
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if p.canonical is None or not p.canonical.startswith(DOMAIN + "/"):
        errors.append(f"{rel}: canonical missing or off-domain")
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

# Sister-state names must not leak into any published text file.
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest")):
            fp = os.path.join(dp, f)
            for mm in set(STATE_RE.findall(open(fp, encoding="utf-8", errors="ignore").read())):
                errors.append(f"{os.path.relpath(fp, ROOT)}: mentions {mm}")

all_desc.sort()
print(f"checked {len(files)} pages; descriptions {all_desc[0][0]}–{all_desc[-1][0]} chars")
print(f"  shortest: {all_desc[0][0]} {all_desc[0][1]}")
print(f"  longest:  {all_desc[-1][0]} {all_desc[-1][1]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
