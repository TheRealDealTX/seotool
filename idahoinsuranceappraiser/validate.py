#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://idahoinsuranceappraiser.com"
KEYWORD = "Idaho Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never appear in this build (word-boundary, case-sensitive proper nouns).
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Illinois", "Kentucky",
          "Maine", "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey",
          "New Mexico", "New York", "North Carolina", "South Carolina", "North Dakota", "South Dakota", "Ohio",
          "Oklahoma", "Rhode Island", "Utah", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Texas",
          "Oregon", "Tennessee", "Louisiana", "Mississippi", "Virginia", "Colorado", "California"]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b")
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.og_desc = self.tw_desc = None
        self._in, self.ids, self.imgs_noalt = None, set(), 0
        self.heads, self.canonical = [], None

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
            elif a.get("property") == "og:description":
                self.og_desc = a.get("content", "")
            elif a.get("name") == "twitter:description":
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
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, "–": 556, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "²": 333})


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
                refs.append(node["@id"])
            else:
                defined.setdefault(node["@id"], []).append(node.get("@type"))
        for v in node.values():
            walk_ld(v, defined, refs)
    elif isinstance(node, list):
        for v in node:
            walk_ld(v, defined, refs)


# ---------- file inventory
files, static_html = [], []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, ROOT)
        if f == "index.html":
            errors.append(f"/{rel}: index.html pages are not allowed (the host serves them without the guard)")
        if f.endswith(".html"):
            if dp != ROOT:
                errors.append(f"/{rel}: static .html page outside the root")
            elif f not in ("home.html", "404.html", GSC_FILE):
                errors.append(f"/{rel}: unexpected root .html file")
        if f == GSC_FILE:
            continue  # verification file: excluded from page checks
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(full)

# ---------- Search Console verification file
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing /{GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"/{GSC_FILE}: content is not exactly the verification line")

titles, descs = {}, {}
desc_lens = []
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    url_path = "/" if rel == "/home.html" else rel.replace("index.php", "")
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    # JSON-LD validity + @id resolution + one page node
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        defined, refs = {}, []
        walk_ld(data, defined, refs)
        for r in refs:
            if r not in defined:
                errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
        for k, types in defined.items():
            if len(types) > 1:
                errors.append(f"{rel}: JSON-LD @id defined more than once: {k}")
        pnodes = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if len(pnodes) != 1:
            errors.append(f"{rel}: expected exactly one page node, found {len(pnodes)}")
        else:
            pn = pnodes[0]
            for key in ("primaryImageOfPage", "mainEntity"):
                if key not in pn:
                    errors.append(f"{rel}: page node lacks {key}")
            if url_path != "/" and not rel.endswith("404.html") and "breadcrumb" not in pn:
                errors.append(f"{rel}: page node lacks breadcrumb")
        if not any(n.get("@type") == "ProfessionalService" for n in graph):
            errors.append(f"{rel}: no ProfessionalService node")
        if not any(n.get("@type") == "WebSite" for n in graph):
            errors.append(f"{rel}: no WebSite node")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    if not rel.endswith("404.html") and p.canonical != DOMAIN + url_path:
        errors.append(f"{rel}: canonical {p.canonical} != {DOMAIN + url_path}")
    t = html.unescape(p.title.strip())
    titles.setdefault(t, []).append(rel)
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if p.desc is None:
        errors.append(f"{rel}: missing meta description")
    else:
        d = html.unescape(p.desc)
        descs.setdefault(d, []).append(rel)
        desc_lens.append((len(d), rel, d))
        if not DESC_MIN <= len(d) <= DESC_MAX:
            errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not d.rstrip().endswith((".", "!", "?")):
            errors.append(f"{rel}: description doesn't end with a complete sentence")
        if p.og_desc != p.desc or p.tw_desc != p.desc:
            errors.append(f"{rel}: og:description / twitter:description differ from the meta description")
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
        if "photo-credits" in path:
            errors.append(f"{rel}: links to a photo credits page")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
        elif "#" in href and path.endswith("/"):
            frag = href.split("#", 1)[1]
            tp = P()
            tp.feed(page_html(target) if target.endswith(".php") else open(target, encoding="utf-8").read())
            if frag and frag not in tp.ids:
                errors.append(f"{rel}: missing anchor {href}")
        if GSC_FILE in href:
            errors.append(f"{rel}: links to the Search Console verification file")
    if rel == "/home.html":
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

# Sitemap: every URL resolves to a page; the verification file and credits page are not listed.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    pth = u.replace(DOMAIN, "")
    target = os.path.join(ROOT, "home.html") if pth == "/" else os.path.join(ROOT, pth.lstrip("/"), "index.php")
    if not os.path.isfile(target):
        errors.append(f"sitemap URL without a page: {u}")
    if GSC_FILE in u or "photo-credits" in u:
        errors.append(f"sitemap lists {u}")
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if "google" in robots.lower():
    errors.append("robots.txt mentions the verification file")
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page exists")

# Stray references to sister-site states, anywhere in the build's text files.
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".json")):
            fp = os.path.join(dp, f)
            for mt in set(BANNED_RE.findall(open(fp, encoding="utf-8", errors="ignore").read())):
                errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions {mt}")

print(f"checked {len(files)} pages, {len(locs)} sitemap URLs")
if desc_lens:
    desc_lens.sort()
    print(f"descriptions: shortest {desc_lens[0][0]} ({desc_lens[0][1]}), longest {desc_lens[-1][0]} ({desc_lens[-1][1]})")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
