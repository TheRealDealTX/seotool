#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: titles (<=60 chars, <=~580px Arial 20px), meta descriptions (110-143 chars, unique, mirrored in
og:/twitter:description), one H1 that is the first heading, no skipped heading levels, valid JSON-LD with
resolvable @id references and a page node, no broken internal links/anchors, alt on every image, homepage
keyword count, no sister-state names, canonical-host guard on every dir/index.php, no dir/index.html,
sitemap/robots sanity and the Search Console verification file (byte-exact, left out of page checks).
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://mississippiinsuranceappraiser.com"
KEYWORD = "Mississippi Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never appear. "Washington County" (Greenville, MS) is allowed.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Connecticut", "Delaware", "Florida", "Georgia",
          "Idaho", "Illinois", "Kentucky", "Maine", "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana",
          "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
          "Ohio", "Oklahoma", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Texas", "Utah",
          "Vermont", "Virginia", "West Virginia", "Wisconsin", "Wyoming"]
BANNED_RE = re.compile(r"\b(" + "|".join(BANNED) + r")\b|\bwashington\b(?![\s-]+county)|\btx\b", re.I)
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.og_desc = self.tw_desc = self.canonical = None
        self._in, self.ids, self.imgs_noalt, self.heads, self.text, self._skip = None, set(), 0, [], [], 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href") and a.get("rel") not in ("preconnect",):
            self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
            self.h1 += tag == "h1"
        if tag == "meta":
            if a.get("name") == "description":
                self.desc = a.get("content", "")
            if a.get("property") == "og:description":
                self.og_desc = a.get("content", "")
            if a.get("name") == "twitter:description":
                self.tw_desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
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


_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp):
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


def walk_ids(o, defined, refs):
    if isinstance(o, dict):
        if "@id" in o:
            (defined if len(o) > 1 else refs).add(o["@id"])
        for v in o.values():
            walk_ids(v, defined, refs)
    elif isinstance(o, list):
        for v in o:
            walk_ids(v, defined, refs)


files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        fp = os.path.join(dp, f)
        if f == "index.html":
            errors.append(f"{fp}: dir/index.html pages are not allowed (host would skip the guard)")
        if dp == ROOT and f == GSC_FILE:
            continue  # verification file: not a page
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(fp)
root_html = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
if root_html != sorted(["404.html", "home.html", GSC_FILE]):
    errors.append(f"unexpected root .html files: {root_html}")

titles, descs = {}, {}
desc_lens = []
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
    # JSON-LD
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        for need in ("ProfessionalService", "WebSite"):
            if need not in types:
                errors.append(f"{rel}: JSON-LD missing {need}")
        pnodes = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if len(pnodes) != 1:
            errors.append(f"{rel}: expected one page node, found {len(pnodes)}")
        else:
            pn = pnodes[0]
            for k in ("primaryImageOfPage", "mainEntity"):
                if k not in pn:
                    errors.append(f"{rel}: page node missing {k}")
            if "BreadcrumbList" in types and "breadcrumb" not in pn:
                errors.append(f"{rel}: page node not linked to BreadcrumbList")
        defined, refs = set(), set()
        walk_ids(graph, defined, refs)
        for r in refs - defined:
            errors.append(f"{rel}: unresolved @id {r}")
    # meta
    t = html.unescape(p.title.strip())
    d = p.desc
    if d is None:
        errors.append(f"{rel}: missing meta description")
        d = ""
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    desc_lens.append((len(d), rel, d))
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description does not end with a full sentence")
    if p.og_desc != d or p.tw_desc != d:
        errors.append(f"{rel}: og:description / twitter:description differ from meta description")
    if not (p.canonical or "").startswith(DOMAIN + "/"):
        errors.append(f"{rel}: canonical missing or off-domain")
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
        if path == "/" + GSC_FILE:
            errors.append(f"{rel}: links to the Search Console file")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
    # homepage keyword count (inside <main> only)
    if rel == "/home.html":
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

# sister-state names anywhere in the build (text assets)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            fp = os.path.join(dp, f)
            for m in BANNED_RE.finditer(open(fp, encoding="utf-8", errors="ignore").read()):
                errors.append(f"{fp}: mentions sister state '{m.group(0)}'")
                break

# sitemap / robots / verification file
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
if any(GSC_FILE in u or u.endswith("404.html") for u in locs):
    errors.append("sitemap.xml lists the verification file or 404")
for u in locs:
    pth = u.replace(DOMAIN, "")
    tgt = os.path.join(ROOT, "home.html") if pth == "/" else os.path.join(ROOT, pth.strip("/"), "index.php")
    if not os.path.exists(tgt):
        errors.append(f"sitemap URL has no page: {u}")
if len(locs) != len(files) - 1:
    errors.append(f"sitemap has {len(locs)} URLs but there are {len(files) - 1} indexable pages")
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if GSC_FILE in robots or re.search(r"Disallow:\s*/\s*$", robots, re.M):
    errors.append("robots.txt blocks the verification file or the whole site")
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc) or open(gsc, "rb").read() != GSC_BODY:
    errors.append("Search Console verification file missing or not byte-exact")

desc_lens.sort()
print(f"checked {len(files)} page files, {len(locs)} sitemap URLs")
print(f"shortest description {desc_lens[0][0]} chars: {desc_lens[0][1]}")
print(f"longest description  {desc_lens[-1][0]} chars: {desc_lens[-1][1]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
