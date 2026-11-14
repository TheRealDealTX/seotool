#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "New Mexico Insurance Appraiser"
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
DESC_MIN, DESC_MAX = 110, 143
# Sister-site states (and neighbors) that must never leak into this build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland",
          "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New York", "North Carolina",
          "North Dakota", "Ohio", "Oklahoma", "Rhode Island", "South Carolina", "Utah", "West Virginia", "Wisconsin",
          "Wyoming", "Texas", "Colorado"]
MIN_HOME_MENTIONS = 14
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.meta = {}
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self._skip = 0
        self.heads = []

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


titles, descs = {}, {}
all_descs = []
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == GSC_FILE and dp == ROOT:
            continue
        if f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: index.html pages are not allowed (host serves them without the guard)")
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        defined, refs = set(), set()
        def walk(o):
            if isinstance(o, dict):
                if "@id" in o:
                    (refs if len(o) == 1 else defined).add(o["@id"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        for r in sorted(refs - defined):
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
        graph = data.get("@graph", [])
        pnodes = [n for n in graph if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
        if len(pnodes) != 1:
            errors.append(f"{rel}: expected exactly one page node in @graph, found {len(pnodes)}")
        else:
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pnodes[0] and not rel.endswith("404.html"):
                    errors.append(f"{rel}: page node missing {k}")
        if not any(n.get("@type") == "ProfessionalService" for n in graph) or not any(n.get("@type") == "WebSite" for n in graph):
            errors.append(f"{rel}: graph missing ProfessionalService or WebSite")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    if p.desc is None:
        errors.append(f"{rel}: missing meta description")
        p.desc = ""
    else:
        if not DESC_MIN <= len(p.desc) <= DESC_MAX:
            errors.append(f"{rel}: description {len(p.desc)} chars (want {DESC_MIN}-{DESC_MAX}): {p.desc}")
        if not p.desc.rstrip().endswith((".", "!", "?")):
            errors.append(f"{rel}: description doesn't end with a complete sentence")
        for k in ("og:description", "twitter:description"):
            if p.meta.get(k) != p.desc:
                errors.append(f"{rel}: {k} differs from meta description")
    all_descs.append((len(p.desc), rel))
    if not rel.endswith("404.html"):
        titles.setdefault(t, []).append(rel)
        descs.setdefault(p.desc, []).append(rel)
        if len(t) > 60:
            errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
        if title_px(t) > 580:
            errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
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
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
    if rel == "/home.html":
        main = " ".join(p.text)
        main = re.sub(r"\s+", " ", main)
        body_only = main.split("Skip to content", 1)[-1]
        n_all = body_only.count(KEYWORD)
        # Count inside <main> only (exclude header/footer brand text)
        raw = page_html(fp)
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

# Stray references to sister-site states, and no photo-credits page or link anywhere
ban = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
scan = files + [os.path.join(ROOT, f) for f in ("sitemap.xml", "robots.txt")]
for dp, _, fs in os.walk(os.path.join(ROOT, "assets")):
    scan += [os.path.join(dp, f) for f in fs if f.endswith((".js", ".css", ".svg", ".webmanifest"))]
scan += [os.path.join(ROOT, "site.webmanifest"), os.path.join(ROOT, "api", "contact.php")]
for fp in scan:
    if not os.path.exists(fp):
        continue
    s = open(fp, encoding="utf-8").read()
    m = ban.search(s)
    if m:
        errors.append(f"{fp}: mentions sister state '{m.group(0)}'")
    if re.search(r"photo[- ]credits", s, re.I):
        errors.append(f"{fp}: references photo credits")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits/ exists")

# Search Console file: exact bytes at the root, never in the sitemap
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc) or open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} missing or not byte-exact")
if GSC_FILE in open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read():
    errors.append(f"{GSC_FILE} must not be in sitemap.xml")
# Root-level static html allowed: only home.html, 404.html and the GSC file
for f in os.listdir(ROOT):
    if f.endswith(".html") and f not in ("home.html", "404.html", GSC_FILE):
        errors.append(f"unexpected root html file: {f}")

all_descs.sort()
print(f"descriptions: shortest {all_descs[0][0]} ({all_descs[0][1]}), longest {all_descs[-1][0]} ({all_descs[-1][1]}), all < 144: {all(n < 144 for n, _ in all_descs)}")

print(f"checked {len(files)} html files")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
