#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: title length/pixel width, meta description 110-143 chars (all pages incl. 404) and equal to
og:description and twitter:description, unique titles/descriptions, exactly one H1 which is the first
heading, no skipped heading levels, valid JSON-LD with resolvable @id references and the required
nodes, no broken internal links or anchors, alt on every image, homepage keyword count, no sister-state
names, canonical-host guard on every dir/index.php, no dir/index.html or root index.html, and the
Search Console file byte-for-byte (excluded from page checks and the sitemap).
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "public")
DOMAIN = "https://tennesseeinsuranceappraiser.com"
KEYWORD = "Tennessee Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_CONTENT = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
ALLOWED_ROOT_HTML = {"home.html", "404.html", GSC_FILE}

# Every other state's name is banned so no sister-site name leaks into the build.
STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
          "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
          "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
          "South Carolina", "South Dakota", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
# Tennessee place names that legitimately contain a state word.
ALLOW_PHRASES = ["Mississippi River", "Washington County"]
BANNED = re.compile(r"\b(" + "|".join(re.escape(s) for s in STATES) + r")\b", re.I)

errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.ogd = self.twd = None
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self.heads = []
        self.canonical = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            if tag == "link" and a.get("rel") == "canonical":
                self.canonical = a["href"]
            self.links.append(a["href"])
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
                self.ogd = a.get("content", "")
            if a.get("name") == "twitter:description":
                self.twd = a.get("content", "")
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


def check_ld(rel, blocks):
    nodes, refs, types = {}, [], []

    def walk(o, top=False):
        if isinstance(o, dict):
            if "@id" in o and len(o) > 1:
                nodes[o["@id"]] = o
            elif "@id" in o and len(o) == 1:
                refs.append(o["@id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for block in blocks:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types += [n.get("@type") for n in graph]
        walk(data)
    for r in refs:
        if r not in nodes:
            errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    page_nodes = [n for n in nodes.values() if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
    if len(page_nodes) != 1:
        errors.append(f"{rel}: expected exactly one page node, found {len(page_nodes)}")
    else:
        pn = page_nodes[0]
        for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
            if k not in pn:
                errors.append(f"{rel}: page node missing {k}")
    for t in ("ProfessionalService", "WebSite", "BreadcrumbList"):
        if t not in types:
            errors.append(f"{rel}: JSON-LD graph missing {t}")
    biz = next((n for n in nodes.values() if n.get("@type") == "ProfessionalService"), {})
    for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
        if k not in biz:
            errors.append(f"{rel}: ProfessionalService missing {k}")
    return types


# --- structural checks on the build folder
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist (host would serve it instead of index.php)")
for f in os.listdir(ROOT):
    if f.endswith(".html") and f not in ALLOWED_ROOT_HTML:
        errors.append(f"unexpected root html file: {f}")
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc):
    errors.append(f"missing Search Console file {GSC_FILE}")
elif open(gsc, "rb").read() != GSC_CONTENT:
    errors.append(f"Search Console file {GSC_FILE} content differs from the required single line")
for f in ("_guard.php", "index.php", "home.html", "404.html", "robots.txt", "sitemap.xml"):
    if not os.path.exists(os.path.join(ROOT, f)):
        errors.append(f"missing {f}")

titles, descs = {}, {}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if dp != ROOT and f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: dir/index.html is not allowed (skips the guard)")
        if f == GSC_FILE and dp == ROOT:
            continue
        if (f.endswith(".html") and dp == ROOT) or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

desc_lengths = []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    check_ld(rel, p.ld)
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    d = html.unescape(p.desc) if p.desc is not None else None
    titles.setdefault(t, []).append(rel)
    if d is None:
        errors.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(d, []).append(rel)
        desc_lengths.append((len(d), rel, d))
        if not DESC_MIN <= len(d) <= DESC_MAX:
            errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not d.rstrip().endswith((".", "!", "?")):
            errors.append(f"{rel}: description does not end with a complete sentence")
        if html.unescape(p.ogd or "") != d or html.unescape(p.twd or "") != d:
            errors.append(f"{rel}: og:description / twitter:description differ from meta description")
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not rel.endswith("404.html"):
        want = DOMAIN + ("/" if rel == "/home.html" else rel[: -len("index.php")])
        if p.canonical != want:
            errors.append(f"{rel}: canonical {p.canonical} != {want}")
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
        if path.rstrip("/").endswith("photo-credits"):
            errors.append(f"{rel}: link to a photo-credits page")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif frag and target.endswith((".php", ".html")):
            tp = P()
            tp.feed(page_html(target))
            if frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
    if rel == "/home.html":
        raw = page_html(fp)
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
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

# Sister-state names anywhere in the built text files
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".json")):
            continue
        fp = os.path.join(dp, f)
        s = open(fp, encoding="utf-8", errors="ignore").read()
        for a in ALLOW_PHRASES:
            s = s.replace(a, "")
        hit = BANNED.search(s)
        if hit:
            errors.append(f"{fp}: mentions another state ({hit.group(0)})")

# sitemap: every page except 404, no GSC file, no photo credits
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
if any(GSC_FILE in l or "photo-credits" in l or "404" in l for l in locs):
    errors.append("sitemap.xml lists the GSC file, a 404 or photo credits")
if len(locs) != len(files) - 1:
    errors.append(f"sitemap.xml has {len(locs)} URLs, expected {len(files) - 1}")
robots = open(os.path.join(ROOT, "robots.txt")).read()
if GSC_FILE in robots:
    errors.append("robots.txt mentions the GSC file")

desc_lengths.sort()
print(f"checked {len(files)} pages, {len(locs)} in sitemap")
print(f"meta descriptions: shortest {desc_lengths[0][0]} ({desc_lengths[0][1]}), longest {desc_lengths[-1][0]} ({desc_lengths[-1][1]})")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print(f"{len(errors)} errors")
sys.exit(1 if errors else 0)
