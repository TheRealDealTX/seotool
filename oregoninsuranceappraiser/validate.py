#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://oregoninsuranceappraiser.com"
KEYWORD = "Oregon Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143          # meta description must be 110-143 characters (under 144)
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never leak into this build. "Washington" is allowed only as
# "Washington County" (a real Oregon county that holds Beaverton and Hillsboro).
SISTER_STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "Connecticut", "Delaware", "Florida", "Georgia", "Idaho",
                 "Illinois", "Kentucky", "Maine", "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nebraska",
                 "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                 "Oklahoma", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Texas", "Utah", "Virginia",
                 "Washington", "West Virginia", "Wisconsin", "Wyoming"]
STATE_RE = re.compile(r"\b(" + "|".join(re.escape(s) for s in SISTER_STATES if s != "Washington") + r")\b|\bWashington\b(?! County)", re.I)
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.descs = [], 0, [], "", []
        self._in, self.ids, self.imgs_noalt, self.heads = None, set(), 0, []
        self.metas = {}

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
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            if a.get("name") == "description":
                self.descs.append(a.get("content", ""))
            key = a.get("property") or a.get("name")
            if key:
                self.metas[key] = a.get("content", "")
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
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "–": 556, "—": 1000})


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


def walk_ld(node, defined, refs):
    if isinstance(node, dict):
        if "@id" in node:
            if len(node) == 1:
                refs.add(node["@id"])
            else:
                defined.add(node["@id"])
        for v in node.values():
            walk_ld(v, defined, refs)
    elif isinstance(node, list):
        for v in node:
            walk_ld(v, defined, refs)


# ---- collect page files (the GSC verification file is not a page)
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        fp = os.path.join(dp, f)
        if f == "index.html":
            errors.append(f"{fp}: index.html pages are not allowed (the host would serve it and skip the guard)")
        if dp == ROOT and f == GSC_FILE:
            continue
        if dp == ROOT and f.endswith(".html") and f not in ("home.html", "404.html"):
            errors.append(f"{fp}: unexpected root .html file")
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(fp)

titles, descs = {}, {}
desc_lens = []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    defined, refs = set(), set()
    for block in p.ld:
        try:
            walk_ld(json.loads(block), defined, refs)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    for r in sorted(refs - defined):
        errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    titles.setdefault(t, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if len(p.descs) != 1:
        errors.append(f"{rel}: {len(p.descs)} meta descriptions (need exactly 1)")
    d = html.unescape(p.descs[0]) if p.descs else ""
    descs.setdefault(d, []).append(rel)
    desc_lens.append((len(d), rel, d))
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description does not end with a full sentence")
    for k in ("og:description", "twitter:description"):
        if html.unescape(p.metas.get(k, "")) != d:
            errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:image:width", "og:image:height", "og:image:alt", "twitter:card", "geo.region"):
        if not p.metas.get(k):
            errors.append(f"{rel}: missing {k}")
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
        if not path:
            frag = href.split("#")[1] if "#" in href else ""
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        if path.strip("/") == GSC_FILE:
            errors.append(f"{rel}: links to the Search Console verification file")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        if "#" in href and path.endswith("/") and os.path.exists(target):
            frag = href.split("#")[1]
            tp = P()
            tp.feed(page_html(target))
            if frag and frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
    if rel == "/home.html":
        raw = page_html(fp)
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

# ---- sister-state names in any text asset
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg", ".json")):
            fp = os.path.join(dp, f)
            for mm in STATE_RE.finditer(open(fp, encoding="utf-8", errors="ignore").read()):
                errors.append(f"{fp}: mentions sister state '{mm.group(0)}'")
                break

# ---- sitemap.xml: every URL maps to a page; no 404 / verification file / photo credits
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    path = u.replace(DOMAIN, "")
    target = os.path.join(ROOT, "home.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.php")
    if not os.path.exists(target):
        errors.append(f"sitemap.xml: {u} has no page")
    if GSC_FILE in u or "404" in u or "photo-credits" in u:
        errors.append(f"sitemap.xml: must not list {u}")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits/ must not exist")

# ---- robots.txt must not block the verification file
rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
for line in rb.splitlines():
    if line.lower().startswith("disallow:"):
        rule = line.split(":", 1)[1].strip()
        if rule and ("/" + GSC_FILE).startswith(rule) and rule != "/":
            errors.append(f"robots.txt rule '{rule}' blocks {GSC_FILE}")
        if rule == "/":
            errors.append("robots.txt blocks the whole site")

# ---- Search Console verification file: exact bytes
gp = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gp):
    errors.append(f"missing {GSC_FILE}")
elif open(gp, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} contents differ from the required single line")

for req in ("index.php", "_guard.php", "home.html", "404.html", "robots.txt", "sitemap.xml", "favicon.ico", "favicon.svg", "apple-touch-icon.png", "site.webmanifest"):
    if not os.path.exists(os.path.join(ROOT, req)):
        errors.append(f"missing {req}")
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist")

desc_lens.sort()
print(f"checked {len(files)} pages, {len(locs)} sitemap URLs")
print(f"descriptions: shortest {desc_lens[0][0]} ({desc_lens[0][1]}), longest {desc_lens[-1][0]} ({desc_lens[-1][1]}), all < 144: {all(n < 144 for n, _, _ in desc_lens)}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
