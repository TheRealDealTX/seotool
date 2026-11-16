#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://connecticutinsuranceappraiser.com"
KEYWORD = "Connecticut Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states: none of these may appear anywhere in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Idaho", "Illinois", "Kentucky",
          "Maine", "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
          "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Pennsylvania",
          "Rhode Island", "South Carolina", "South Dakota", "Texas", "Utah", "Virginia", "West Virginia", "Washington",
          "Wisconsin", "Wyoming"]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc, self.descs = [], 0, [], "", None, 0
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self._skip = 0
        self.heads, self.meta = [], {}

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
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
            if a.get("name") == "description":
                self.desc = a.get("content", "")
                self.descs += 1
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


def collect_ids(o, defined, refs):
    if isinstance(o, dict):
        if "@id" in o:
            if len(o) == 1:
                refs.add(o["@id"])
            else:
                defined.add(o["@id"])
        for k, v in o.items():
            if k == "inDefinedTermSet" and isinstance(v, str):
                refs.add(v)
            collect_ids(v, defined, refs)
    elif isinstance(o, list):
        for v in o:
            collect_ids(v, defined, refs)


# ---- Search Console file: exact bytes, at the root
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing {GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} contents differ from the required single line")

# ---- forbidden files
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), ROOT)
        if f == "index.html":
            errors.append(f"/{rel}: index.html pages are not allowed (the host would skip the guard)")
        if f.endswith(".html") and dp == ROOT and f not in ("home.html", "404.html", GSC_FILE):
            errors.append(f"/{rel}: unexpected root .html file")
        if f.endswith(".html") and dp != ROOT:
            errors.append(f"/{rel}: static .html page outside the root")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page must not exist")

titles, descs = {}, {}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if (f.endswith(".html") and f != GSC_FILE) or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

sitemap_urls = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "sitemap.xml")).read())
desc_lens = []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    url_path = "/" if rel == "/home.html" else rel[:-len("index.php")] if rel.endswith("index.php") else rel
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    defined, refs = set(), set()
    for block in p.ld:
        try:
            collect_ids(json.loads(block), defined, refs)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    for r in sorted(refs - defined):
        errors.append(f"{rel}: JSON-LD @id {r} does not resolve")
    if not rel.endswith("404.html"):
        types = " ".join(p.ld)
        if not re.search(r'"@type":"(WebPage|AboutPage|ContactPage|CollectionPage)"', types):
            errors.append(f"{rel}: no page node in JSON-LD")
        if DOMAIN + url_path not in sitemap_urls:
            errors.append(f"{rel}: not in sitemap.xml")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    d = p.desc
    if p.descs != 1 or d is None:
        errors.append(f"{rel}: {p.descs} meta descriptions")
        d = d or ""
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    desc_lens.append((len(d), rel))
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX}): {d}")
    if d and not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description does not end with a full sentence")
    for k in ("og:description", "twitter:description"):
        if p.meta.get(k) != d:
            errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:title", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:card", "geo.region"):
        if not p.meta.get(k):
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
            tp.feed(page_html(target))
            if frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
        if GSC_FILE in href:
            errors.append(f"{rel}: links to the Search Console file")
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

# Sister-state names anywhere in the published text files
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest")):
            fp = os.path.join(dp, f)
            m = BANNED_RE.search(open(fp, encoding="utf-8", errors="ignore").read())
            if m:
                errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions sister state '{m.group(0)}'")

robots = open(os.path.join(ROOT, "robots.txt")).read()
if re.search(r"Disallow:\s*/google", robots):
    errors.append("robots.txt blocks the Search Console file")
if any(GSC_FILE in u for u in sitemap_urls):
    errors.append("sitemap.xml lists the Search Console file")

desc_lens.sort()
print(f"checked {len(files)} pages; sitemap has {len(sitemap_urls)} URLs")
print(f"shortest description: {desc_lens[0][0]} chars ({desc_lens[0][1]})")
print(f"longest description:  {desc_lens[-1][0]} chars ({desc_lens[-1][1]})")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
