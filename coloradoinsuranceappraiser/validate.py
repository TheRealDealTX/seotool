#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://coloradoinsuranceappraiser.com"
KEYWORD = "Colorado Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states: none of these names may appear anywhere in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Connecticut", "Delaware", "Florida", "Georgia", "Idaho",
          "Illinois", "Indiana", "Kentucky", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
          "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
          "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
          "Texas", "Utah", "Vermont", "Virginia", "West Virginia", "Washington", "Wisconsin", "Wyoming", "policyholderappraiser"]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.ndesc, self.og_desc, self.tw_desc, self.canon = 0, None, None, None
        self._in, self.ids, self.imgs_noalt = None, set(), 0
        self.heads = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href") and a.get("rel") not in ("preconnect", "canonical"):
            self.links.append(a["href"])
        if tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
            self.ndesc += 1
        if tag == "meta" and a.get("property") == "og:description":
            self.og_desc = a.get("content", "")
        if tag == "meta" and a.get("name") == "twitter:description":
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
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


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
            if len(node) == 1:
                refs.append(node["@id"])
            else:
                defined.add(node["@id"])
        for v in node.values():
            walk_ids(v, defined, refs)
    elif isinstance(node, list):
        for v in node:
            walk_ids(v, defined, refs)


# ---------------------------------------------------------------- file inventory
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, ROOT)
        if f == "index.html":
            errors.append(f"/{rel}: index.html pages are not allowed (the host would serve them without the guard)")
        if f.endswith(".html") and dp != ROOT:
            errors.append(f"/{rel}: static .html page outside the root")
        if dp == ROOT and f.endswith(".html") and f not in ("home.html", "404.html", GSC_FILE):
            errors.append(f"/{rel}: unexpected root .html file")
        if f == GSC_FILE:
            continue  # verification file: checked byte-for-byte below, not a page
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(full)

# Search Console file: exact bytes.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing /{GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"/{GSC_FILE} content is not exactly {GSC_BODY!r}")

for need in ("index.php", "_guard.php", "home.html", "404.html", "sitemap.xml", "robots.txt"):
    if not os.path.isfile(os.path.join(ROOT, need)):
        errors.append(f"missing /{need}")

titles, descs, all_desc = {}, {}, []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    url = "/" if rel == "/home.html" else rel.replace("index.php", "")
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    exp_canon = DOMAIN + url
    if p.canon != exp_canon:
        errors.append(f"{rel}: canonical {p.canon} != {exp_canon}")
    # JSON-LD
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        pages_n = [n for n in graph if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
        if len(pages_n) != 1:
            errors.append(f"{rel}: expected one page node, found {len(pages_n)}")
        else:
            pn = pages_n[0]
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pn:
                    errors.append(f"{rel}: page node missing {k}")
        for t in ("ProfessionalService", "WebSite", "BreadcrumbList"):
            if t not in types:
                errors.append(f"{rel}: JSON-LD missing {t}")
        defined, refs = set(), []
        walk_ids(data, defined, refs)
        for r in refs:
            if r not in defined:
                errors.append(f"{rel}: unresolved @id {r}")
    # title & description
    t = html.unescape(p.title.strip())
    d = html.unescape(p.desc or "")
    all_desc.append((len(d), rel, d))
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if p.ndesc != 1:
        errors.append(f"{rel}: {p.ndesc} meta descriptions")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description doesn’t end with a complete sentence")
    if html.unescape(p.og_desc or "") != d or html.unescape(p.tw_desc or "") != d:
        errors.append(f"{rel}: og/twitter description differs from meta description")
    # headings
    prev = 0
    for lv in p.heads:
        if prev and lv > prev + 1:
            errors.append(f"{rel}: heading jump h{prev} -> h{lv}")
            break
        prev = lv
    if p.heads and p.heads[0] != 1:
        errors.append(f"{rel}: first heading is h{p.heads[0]}")
    # links
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "//", "data:")):
            continue
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if not path:
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        if "photo-credits" in path:
            errors.append(f"{rel}: link to photo credits")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif frag and path.endswith("/"):
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

# Sister-state names anywhere in text output (pages, sitemap, scripts, manifest).
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".xml", ".txt", ".js", ".css", ".webmanifest", ".json", ".svg")):
            fp = os.path.join(dp, f)
            s = open(fp, encoding="utf-8", errors="ignore").read()
            for mm in BANNED_RE.finditer(s):
                errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions sister state '{mm.group(0)}'")
                break

# sitemap.xml: every URL exists; no 404/GSC/photo-credits entries.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for loc in locs:
    pth = loc.replace(DOMAIN, "")
    tgt = os.path.join(ROOT, "home.html") if pth == "/" else os.path.join(ROOT, pth.strip("/"), "index.php")
    if not os.path.exists(tgt) or "404" in pth or GSC_FILE in pth or "photo-credits" in pth:
        errors.append(f"sitemap.xml: bad entry {loc}")
if "Disallow: /google" in open(os.path.join(ROOT, "robots.txt")).read():
    errors.append("robots.txt blocks the Search Console file")

all_desc.sort()
print(f"checked {len(files)} pages; sitemap has {len(locs)} URLs")
print(f"shortest description ({all_desc[0][0]}): {all_desc[0][1]}")
print(f"longest description ({all_desc[-1][0]}): {all_desc[-1][1]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK — zero errors" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
