#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: titles (<= 60 chars, <= ~580px), meta descriptions on every page (110-143 chars, unique, ending
in a full sentence, same text in og/twitter), one H1 that comes first, no skipped heading levels, valid
JSON-LD whose @id references resolve, internal links and anchors, alt attributes, homepage keyword count,
no sister-state names, the canonical-host guard on every dir/index.php page, and the Search Console file.
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "Vermont Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states: none of these may appear anywhere in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
          "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
          "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island",
          "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
# Vermont's Washington County is the one legitimate match.
ALLOWED = ["Washington County", "Washington, Windham"]  # Vermont county name
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title = [], 0, [], ""
        self.desc, self.ogdesc, self.twdesc, self.ndesc = None, None, None, 0
        self._in, self.ids, self.imgs_noalt, self.heads = None, set(), 0, []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href") and a.get("rel") not in ("preconnect", "canonical"):
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
                self.ndesc += 1
            if a.get("property") == "og:description":
                self.ogdesc = a.get("content", "")
            if a.get("name") == "twitter:description":
                self.twdesc = a.get("content", "")
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
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "–": 556})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp):
    """Page HTML; dir/index.php pages must start with the guard (right depth) and contain no other PHP."""
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        m = GUARD.match(s)
        depth = os.path.relpath(fp, ROOT).count(os.sep)
        if not m:
            errors.append(f"{fp}: page does not start with the canonical-host guard")
        elif int(m.group(1)) != depth:
            errors.append(f"{fp}: guard depth {m.group(1)} != {depth}")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{fp}: stray PHP tag in page HTML")
    return s


files = []
for dp, _, fs in os.walk(ROOT):
    rel_dp = os.path.relpath(dp, ROOT)
    if rel_dp.split(os.sep)[0] in ("api", "assets"):
        continue
    for f in fs:
        if f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: index.html pages are not allowed (the host would skip the guard)")
        if f == GSC_FILE and dp == ROOT:
            continue  # verification file: checked separately, never parsed as a page
        if (f.endswith(".html") and dp == ROOT) or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))
        elif f.endswith(".html"):
            errors.append(f"{os.path.join(dp, f)}: unexpected static .html file")

allowed_root_html = {"home.html", "404.html", GSC_FILE}
for f in os.listdir(ROOT):
    if f.endswith(".html") and f not in allowed_root_html:
        errors.append(f"/{f}: unexpected root .html file")

# Search Console verification file: exact bytes.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing {GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE}: contents differ from the required single line")

titles, descs, all_desc = {}, {}, []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    ids, refs = set(), set()
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue

        def walk(o, top=False):
            if isinstance(o, dict):
                if "@id" in o and (len(o) > 1):
                    ids.add(o["@id"])
                elif "@id" in o:
                    refs.add(o["@id"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        pagetypes = [t for t in types if t in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
        if len(pagetypes) != 1:
            errors.append(f"{rel}: expected one page node, found {pagetypes}")
        for need in ("ProfessionalService", "WebSite"):
            if need not in types:
                errors.append(f"{rel}: JSON-LD missing {need}")
        for n in graph:
            if n.get("@type") in pagetypes and rel != "/home.html" and rel != "/404.html":
                if "breadcrumb" not in n:
                    errors.append(f"{rel}: page node has no breadcrumb")
            if n.get("@type") in pagetypes:
                for k in ("primaryImageOfPage", "mainEntity"):
                    if k not in n:
                        errors.append(f"{rel}: page node missing {k}")
    for r in refs - ids:
        errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    titles.setdefault(t, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    d = p.desc
    if d is None or p.ndesc != 1:
        errors.append(f"{rel}: needs exactly one meta description (found {p.ndesc})")
    else:
        descs.setdefault(d, []).append(rel)
        all_desc.append((len(d), rel, d))
        if not DESC_MIN <= len(d) <= DESC_MAX:
            errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not d.rstrip().endswith((".", "!", "?")) or d.rstrip().endswith("..."):
            errors.append(f"{rel}: description must end with a complete sentence")
        if p.ogdesc != d or p.twdesc != d:
            errors.append(f"{rel}: og/twitter description differs from meta description")
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
        if path.endswith("/photo-credits/") or GSC_FILE in path:
            errors.append(f"{rel}: must not link to {path}")
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
        raw = page_html(fp)
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = m.group(1) if m else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
        mtext = html.unescape(re.sub(r"<[^>]+>", " ", mtext))
        mtext = re.sub(r"\s+", " ", mtext)
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

# Sister-state names anywhere in the build (pages, sitemap, robots, JS, CSS, PHP).
pat = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            continue
        fp = os.path.join(dp, f)
        s = open(fp, encoding="utf-8", errors="ignore").read()
        for a in ALLOWED:
            s = s.replace(a, "")
        for m in pat.finditer(s):
            errors.append(f"{fp}: mentions sister state '{m.group(1)}'")
            break

# sitemap.xml must not list the verification file, 404 or home.html
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
for bad in (GSC_FILE, "404.html", "home.html", "photo-credits"):
    if bad in sm:
        errors.append(f"sitemap.xml lists {bad}")
if "photo-credits" in "".join(os.listdir(ROOT)):
    errors.append("photo-credits page exists")

all_desc.sort()
print(f"checked {len(files)} pages; descriptions {all_desc[0][0]}-{all_desc[-1][0]} chars")
print(f"  shortest: {all_desc[0][0]} {all_desc[0][1]}: {all_desc[0][2]}")
print(f"  longest:  {all_desc[-1][0]} {all_desc[-1][1]}: {all_desc[-1][2]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
