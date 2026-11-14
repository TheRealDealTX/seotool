#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://nebraskainsuranceappraiser.com"
KEYWORD = "Nebraska Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
# Every other state's name: sister sites exist for many of them, so none may leak into this build.
# "Missouri River" is the state's eastern border river and is allowed; the state name alone is not.
OTHER_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
                "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
                "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nevada", "New Hampshire",
                "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
                "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
BANNED = re.compile(r"\b(" + "|".join(re.escape(s) for s in OTHER_STATES) + r")\b(?! River)", re.I)
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.ids, self.imgs_noalt = [], 0, [], "", set(), 0
        self.meta, self.canon, self.heads, self._in = {}, None, [], None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            if tag == "link" and a.get("rel") == "canonical":
                self.canon = a["href"]
            elif tag == "a" or a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest", "preload"):
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
                self.meta.setdefault(k, []).append(a.get("content", ""))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
            self.ld.append("")
        elif tag == "title":
            self._in = "title"

    def handle_endtag(self, tag):
        if tag in ("script", "title"):
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
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "–": 556})


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


def walk_ids(o, defined, refs):
    if isinstance(o, dict):
        if "@id" in o:
            (refs if set(o) == {"@id"} else defined).add(o["@id"])
        for v in o.values():
            walk_ids(v, defined, refs)
    elif isinstance(o, list):
        for v in o:
            walk_ids(v, defined, refs)


# ---------------------------------------------------------------- file layout rules
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist (the host would serve it instead of index.php)")
allowed_root_html = {"home.html", "404.html", GSC_FILE}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        if f.endswith(".html"):
            if dp == ROOT and f not in allowed_root_html:
                errors.append(f"unexpected root html file {f}")
            elif dp != ROOT:
                errors.append(f"{full}: static dir/*.html pages bypass the guard; write dir/index.php")
            if f != GSC_FILE:
                files.append(full)
        elif f == "index.php" and dp != ROOT:
            files.append(full)
if os.path.isdir(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page must not exist")

# Search Console file: exact bytes
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc):
    errors.append(f"{GSC_FILE} missing")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} content is not exactly the verification line")

titles, descs, all_desc = {}, {}, []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.heads and p.heads[0] != 1:
        errors.append(f"{rel}: first heading is h{p.heads[0]}")
    prev = 0
    for lv in p.heads:
        if prev and lv > prev + 1:
            errors.append(f"{rel}: heading jump h{prev} -> h{lv}")
            break
        prev = lv
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    # head tags
    t = html.unescape(p.title.strip())
    d = (p.meta.get("description") or [""])[0]
    if len(p.meta.get("description", [])) != 1:
        errors.append(f"{rel}: needs exactly one meta description")
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
        errors.append(f"{rel}: description should end with a complete sentence")
    for k in ("og:description", "twitter:description"):
        if (p.meta.get(k) or [None])[0] != d:
            errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:title", "og:image", "og:image:width", "og:image:height", "og:image:alt", "og:url", "twitter:card", "twitter:image", "geo.region"):
        if not p.meta.get(k):
            errors.append(f"{rel}: missing {k}")
    if not (p.canon or "").startswith(DOMAIN + "/"):
        errors.append(f"{rel}: canonical missing or off-domain: {p.canon}")
    # JSON-LD
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        pn = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if len(pn) != 1:
            errors.append(f"{rel}: JSON-LD needs exactly one page node, found {len(pn)}")
        else:
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pn[0]:
                    errors.append(f"{rel}: page node missing {k}")
        for need in ("ProfessionalService", "WebSite", "BreadcrumbList"):
            if need not in types:
                errors.append(f"{rel}: JSON-LD missing {need}")
        defined, refs = set(), set()
        walk_ids(data, defined, refs)
        for r in sorted(refs - defined):
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    if not p.ld:
        errors.append(f"{rel}: no JSON-LD")
    # links
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
        if GSC_FILE in path:
            errors.append(f"{rel}: links to the Search Console file")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif frag and target.endswith((".php", ".html")):
            if f'id="{frag}"' not in open(target, encoding="utf-8").read():
                errors.append(f"{rel}: missing anchor {href}")
    # banned sister-state names (visible text, attributes and JSON-LD alike)
    for m in BANNED.finditer(raw):
        errors.append(f"{rel}: mentions another state: {m.group(0)}")
    if rel == "/home.html":
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = re.sub(r"<script.*?</script>", " ", m.group(1), flags=re.S) if m else ""
        mtext = html.unescape(re.sub(r"<[^>]+>", " ", mtext))
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

# sitemap.xml: every URL exists, no GSC file, no 404, no photo credits
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    path = u.replace(DOMAIN, "")
    target = os.path.join(ROOT, "home.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.php")
    if not os.path.exists(target):
        errors.append(f"sitemap URL has no page: {u}")
    if GSC_FILE in u or "404" in u or "photo-credits" in u:
        errors.append(f"sitemap must not list {u}")
robots = open(os.path.join(ROOT, "robots.txt")).read()
if GSC_FILE in robots:
    errors.append("robots.txt must not mention the Search Console file")

all_desc.sort()
print(f"checked {len(files)} pages, {len(locs)} sitemap URLs")
print(f"shortest description: {all_desc[0][0]} chars {all_desc[0][1]}")
print(f"longest description:  {all_desc[-1][0]} chars {all_desc[-1][1]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
