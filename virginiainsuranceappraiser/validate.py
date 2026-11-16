#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error.

Checks: titles (<=60 chars, ~<=580px Arial 20px), meta descriptions (110-143 chars, unique, mirrored in
og:/twitter:description), one H1 that is the first heading and no skipped heading levels, valid JSON-LD with
one page node and resolvable @id references, canonical/OG/Twitter/geo tags, internal links and anchors, img
alt attributes, homepage keyword count, banned sister-state names, the canonical-host guard on every
dir/index.php page, the Search Console verification file, and sitemap.xml coverage.
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://virginiainsuranceappraiser.com"
KEYWORD = "Virginia Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
ALLOWED_ROOT_HTML = {"home.html", "404.html", GSC_FILE}
# Sister sites on the same Hostinger Agency account. None of these names may appear in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Georgian", "Illinois",
          "Kentucky", "Maine", "Maryland", "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada",
          "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
          "Rhode Island", "South Carolina", "South Dakota", "Utah", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ld, self.title, self.ids, self.imgs_noalt, self.heads = [], [], "", set(), 0, []
        self.meta, self.prop, self.canonical = {}, {}, None
        self._in = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href") and a.get("rel") not in ("preconnect",):
            if tag == "link" and a.get("rel") == "canonical":
                self.canonical = a["href"]
            elif tag == "a" or a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest", "preload"):
                self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            if a.get("name"):
                self.meta[a["name"]] = a.get("content", "")
            if a.get("property"):
                self.prop[a["property"]] = a.get("content", "")
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
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "+": 584, "§": 556})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp, rel):
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        m = GUARD.match(s)
        if not m:
            errors.append(f"{rel}: page does not start with the canonical-host guard")
        elif int(m.group(1)) != rel.strip("/").count("/"):
            errors.append(f"{rel}: guard depth {m.group(1)} is wrong")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{rel}: stray PHP tag in page HTML")
    return s


def url_of(rel):
    if rel == "/home.html":
        return "/"
    if rel.endswith("/index.php"):
        return rel[: -len("index.php")]
    return rel


def target_of(path):
    if path == "/":
        return os.path.join(ROOT, "home.html")
    t = os.path.join(ROOT, path.lstrip("/"))
    return os.path.join(t, "index.php") if path.endswith("/") else t


def walk_ids(o, defined, refs):
    if isinstance(o, dict):
        if "@id" in o:
            (refs if len(o) == 1 else defined).add(o["@id"])
        for v in o.values():
            walk_ids(v, defined, refs)
    elif isinstance(o, list):
        for v in o:
            walk_ids(v, defined, refs)


# ---------------------------------------------------------------- collect files
files = []
for dp, dns, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        rel = "/" + os.path.relpath(full, ROOT)
        if f.endswith(".html"):
            if dp != ROOT or f not in ALLOWED_ROOT_HTML:
                errors.append(f"{rel}: static .html page not allowed (pages must be dir/index.php)")
            if f != GSC_FILE:
                files.append(full)
        elif f == "index.php" and dp != ROOT:
            files.append(full)
if "photo-credits" in os.listdir(ROOT):
    errors.append("/photo-credits/ exists")

# Search Console file: exact bytes.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gsc):
    errors.append(f"missing {GSC_FILE}")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} contents differ from the required single line")

parsed = {}
for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp, rel))
    parsed[rel] = p

titles, descs = {}, {}
desc_lens = []
for rel, p in parsed.items():
    url = url_of(rel)
    is404 = rel == "/404.html"
    if p.heads.count(1) != 1:
        errors.append(f"{rel}: {p.heads.count(1)} h1 tags")
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

    t = html.unescape(p.title.strip())
    d = p.meta.get("description", "")
    titles.setdefault(t, []).append(rel)
    descs.setdefault(d, []).append(rel)
    desc_lens.append((len(d), rel, d))
    if len(t) > 60:
        errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
    if title_px(t) > 580:
        errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if not d:
        errors.append(f"{rel}: missing meta description")
    elif not DESC_MIN <= len(d) <= DESC_MAX:
        errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
    elif not d.rstrip().endswith((".", "!", "?")):
        errors.append(f"{rel}: description doesn't end with a full sentence")
    if p.prop.get("og:description") != d or p.meta.get("twitter:description") != d:
        errors.append(f"{rel}: og:/twitter:description differ from meta description")
    for k in ("og:title", "og:url", "og:image", "og:image:width", "og:image:height", "og:image:alt", "og:type"):
        if not p.prop.get(k):
            errors.append(f"{rel}: missing {k}")
    for k in ("twitter:card", "twitter:title", "twitter:image", "geo.region"):
        if not p.meta.get(k):
            errors.append(f"{rel}: missing {k}")
    if not is404:
        if p.canonical != DOMAIN + url:
            errors.append(f"{rel}: canonical {p.canonical} != {DOMAIN + url}")
        if not p.meta.get("robots", "").startswith("index"):
            errors.append(f"{rel}: robots meta not indexable")

    # JSON-LD
    if len(p.ld) != 1:
        errors.append(f"{rel}: {len(p.ld)} JSON-LD blocks")
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        page_nodes = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if len(page_nodes) != 1:
            errors.append(f"{rel}: {len(page_nodes)} page nodes in @graph")
        else:
            pn = page_nodes[0]
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pn:
                    errors.append(f"{rel}: page node missing {k}")
        for need in ("ProfessionalService", "WebSite", "BreadcrumbList"):
            if need not in types:
                errors.append(f"{rel}: @graph missing {need}")
        org = next((n for n in graph if n.get("@type") == "ProfessionalService"), {})
        for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
            if k not in org:
                errors.append(f"{rel}: ProfessionalService missing {k}")
        defined, refs = set(), set()
        walk_ids(data, defined, refs)
        for r in refs - defined:
            errors.append(f"{rel}: unresolved @id {r}")

    # links and anchors
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "//", "data:")):
            continue
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if not path:
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        if GSC_FILE in path:
            errors.append(f"{rel}: links to the Search Console file")
        tgt = target_of(path)
        if not os.path.exists(tgt):
            errors.append(f"{rel}: broken link {href}")
            continue
        if frag:
            trel = "/" + os.path.relpath(tgt, ROOT)
            if trel in parsed and frag not in parsed[trel].ids:
                errors.append(f"{rel}: missing anchor {href}")

    if rel == "/home.html":
        raw = page_html(fp if False else os.path.join(ROOT, "home.html"), rel)
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        main = m.group(1) if m else ""
        main = re.sub(r"<script.*?</script>", " ", main, flags=re.S)
        mtext = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main)))
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

# sitemap.xml: every indexable page listed, every URL resolves, no GSC file / 404.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for loc in locs:
    if not loc.startswith(DOMAIN):
        errors.append(f"sitemap: foreign URL {loc}")
        continue
    path = loc[len(DOMAIN):]
    if GSC_FILE in path or path.endswith(".html"):
        errors.append(f"sitemap: should not list {path}")
    elif not os.path.exists(target_of(path)):
        errors.append(f"sitemap: {path} has no file")
want = {url_of(r) for r in parsed if r != "/404.html"}
missing = want - {l[len(DOMAIN):] for l in locs}
for m_ in sorted(missing):
    errors.append(f"sitemap: missing {m_}")
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
if "googlecccfbf2f7e9e5ae4" in robots or "Disallow: /\n" in robots:
    errors.append("robots.txt blocks the Search Console file or the whole site")

# Sister-state names and photo-credit links anywhere in text output.
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".xml", ".txt", ".webmanifest", ".svg")):
            fp = os.path.join(dp, f)
            s = open(fp, encoding="utf-8", errors="ignore").read()
            for m_ in set(x.group(0) for x in BANNED_RE.finditer(s)):
                errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions sister state '{m_}'")
            if "photo-credits" in s or "Photo credits" in s:
                errors.append(f"/{os.path.relpath(fp, ROOT)}: references photo credits")

desc_lens.sort()
print(f"checked {len(parsed)} pages; {len(locs)} sitemap URLs")
print(f"shortest description: {desc_lens[0][0]} chars ({desc_lens[0][1]})")
print(f"longest description:  {desc_lens[-1][0]} chars ({desc_lens[-1][1]})")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
