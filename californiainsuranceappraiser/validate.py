#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://californiainsuranceappraiser.com"
KEYWORD = "California Insurance Appraiser"
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
        self.links, self.h1, self.ld, self.title = [], 0, [], ""
        self.meta = {}
        self.canonical = None
        self._in, self.ids, self.imgs_noalt = None, set(), 0
        self.heads = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and a.get("href"):
            if a.get("rel") == "canonical":
                self.canonical = a["href"]
            elif a.get("rel") not in ("preconnect",):
                self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img":
            if "alt" not in a:
                self.imgs_noalt += 1
            for part in (a.get("srcset") or "").split(","):
                if part.strip():
                    self.links.append(part.strip().split(" ")[0])
        if tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta.setdefault(k, []).append(a.get("content", ""))
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
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "§": 556})


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


def target_of(path):
    if path == "/":
        return os.path.join(ROOT, "home.html")
    t = os.path.join(ROOT, path.lstrip("/"))
    return os.path.join(t, "index.php") if path.endswith("/") else t


def ld_check(rel, graph):
    defined, refs = set(), []

    def walk(o):
        if isinstance(o, dict):
            if "@id" in o:
                if len(o) == 1:
                    refs.append(o["@id"])
                else:
                    defined.add(o["@id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(graph)
    for r in refs:
        if r not in defined:
            errors.append(f"{rel}: JSON-LD @id reference not defined: {r}")
    pages = [n for n in graph if isinstance(n, dict) and n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
    if len(pages) != 1:
        errors.append(f"{rel}: expected exactly one page node, found {len(pages)}")
    else:
        pg = pages[0]
        for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
            if k not in pg:
                errors.append(f"{rel}: page node missing {k}")
    types = {n.get("@type") for n in graph if isinstance(n, dict)}
    for t in ("ProfessionalService", "WebSite", "BreadcrumbList"):
        if t not in types:
            errors.append(f"{rel}: JSON-LD graph missing {t}")


# Never ship a static index.html page: the host would serve it before index.php and skip the guard.
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: index.html is not allowed (pages must be dir/index.php)")
        if f.endswith(".html") and dp != ROOT:
            errors.append(f"{os.path.join(dp, f)}: static .html outside the root")

root_html = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
if root_html != sorted(["404.html", "home.html", GSC_FILE]):
    errors.append(f"unexpected root .html files: {root_html}")

# Search Console file: exact bytes.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc) or open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE}: missing or contents differ from the exact verification line")

files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if (f.endswith(".html") and f != GSC_FILE) or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

parsed, titles, descs = {}, {}, {}
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    parsed[fp] = p

for fp, p in sorted(parsed.items()):
    rel = "/" + os.path.relpath(fp, ROOT)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            data = json.loads(block)
            ld_check(rel, data.get("@graph", []))
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if not p.ld:
        errors.append(f"{rel}: no JSON-LD")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    desc = html.unescape((p.meta.get("description") or [""])[0])
    titles.setdefault(t, []).append(rel)
    descs.setdefault(desc, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if len(p.meta.get("description", [])) != 1:
        errors.append(f"{rel}: expected one meta description, found {len(p.meta.get('description', []))}")
    if not DESC_MIN <= len(desc) <= DESC_MAX:
        errors.append(f"{rel}: description {len(desc)} chars (want {DESC_MIN}-{DESC_MAX}): {desc}")
    elif not desc.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description does not end with a complete sentence")
    for k in ("og:description", "twitter:description"):
        if html.unescape((p.meta.get(k) or [""])[0]) != desc:
            errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:title", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:card", "twitter:title", "twitter:image", "geo.region"):
        if k not in p.meta:
            errors.append(f"{rel}: missing meta {k}")
    if not (p.canonical or "").startswith(DOMAIN + "/"):
        errors.append(f"{rel}: canonical missing or off-domain: {p.canonical}")
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
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if not path:
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        target = target_of(path)
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif frag and target in parsed and frag not in parsed[target].ids:
            errors.append(f"{rel}: missing anchor {href}")
        if GSC_FILE in path:
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

# Sitemap: every URL resolves, and the GSC file is not in it.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    if not u.startswith(DOMAIN + "/"):
        errors.append(f"sitemap: off-domain {u}")
    elif not os.path.exists(target_of(u[len(DOMAIN):])):
        errors.append(f"sitemap: missing page for {u}")
    if GSC_FILE in u or "photo-credits" in u:
        errors.append(f"sitemap: should not list {u}")
if "Disallow: /" + GSC_FILE in open(os.path.join(ROOT, "robots.txt")).read():
    errors.append("robots.txt blocks the Search Console file")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page must not exist")

# Sister-state names anywhere in the build (text files).
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            fp = os.path.join(dp, f)
            for mm in set(x.group(1) for x in BANNED_RE.finditer(open(fp, encoding="utf-8").read())):
                errors.append(f"{fp}: mentions sister state '{mm}'")
            if "photo-credits" in open(fp, encoding="utf-8").read():
                errors.append(f"{fp}: references photo-credits")

lens = sorted((len(html.unescape((p.meta.get('description') or [''])[0])), "/" + os.path.relpath(fp, ROOT)) for fp, p in parsed.items())
print(f"checked {len(files)} pages, {len(locs)} sitemap URLs")
print(f"descriptions: shortest {lens[0][0]} ({lens[0][1]}), longest {lens[-1][0]} ({lens[-1][1]})")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
