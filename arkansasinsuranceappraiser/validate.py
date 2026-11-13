#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "Arkansas Insurance Appraiser"
MIN_HOME_MENTIONS = 14
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", ""
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
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if (f.endswith(".html") and not f.startswith("google")) or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
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

# Sister-state names must never leak into the build (copied text, photo titles, URLs).
SISTERS = ["Alabama", "Arizona", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland", "Massachusetts",
           "Missouri", "Montana", "Nevada", "New York", "North Carolina", "West Virginia", "Wyoming"]
SISTER_RE = re.compile(r"\b(" + "|".join(re.escape(x) for x in SISTERS) + r")\b", re.I)
scan = files + [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith((".js", ".css", ".xml", ".txt", ".webmanifest", ".php", ".svg"))]
for fp in sorted(set(scan)):
    m = SISTER_RE.search(open(fp, encoding="utf-8", errors="ignore").read())
    if m:
        errors.append(f"{fp}: mentions sister state '{m.group(1)}'")

# Every page needs canonical, OG image size/alt, Twitter card and geo.region.
for fp in files:
    s = open(fp, encoding="utf-8").read()
    rel = "/" + os.path.relpath(fp, ROOT)
    for needle in ('rel="canonical" href="https://arkansasinsuranceappraiser.com/', 'property="og:image:width"', 'property="og:image:alt"',
                   'name="twitter:card"', 'name="geo.region" content="US-AR"'):
        if needle not in s:
            errors.append(f"{rel}: missing {needle}")

# JSON-LD @id references must resolve; indexable pages need one page node with breadcrumb, image and mainEntity.
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
for fp in files:
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = open(fp, encoding="utf-8").read()
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try:
            g = json.loads(block).get("@graph", [])
        except Exception:
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
        walk(g)
        for r_ in sorted(refs - defined):
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r_}")
        if rel.endswith("404.html"):
            continue
        pn = [n for n in g if n.get("@type") in PAGE_TYPES]
        if len(pn) != 1:
            errors.append(f"{rel}: {len(pn)} page nodes in JSON-LD (want 1)")
        else:
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pn[0]:
                    errors.append(f"{rel}: page node missing {k}")
        biz = [n for n in g if n.get("@type") == "ProfessionalService"]
        if not biz or not all(k in biz[0] for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog")):
            errors.append(f"{rel}: ProfessionalService node incomplete")

# The host would serve these without running the guard.
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: index.html must not exist (would bypass the guard)")

print(f"checked {len(files)} html files")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
