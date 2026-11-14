#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://southdakotainsuranceappraiser.com"
KEYWORD = "South Dakota Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never appear in the build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland",
          "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New York", "North Carolina",
          "North Dakota", "Ohio", "Rhode Island", "South Carolina", "Utah", "West Virginia", "Wisconsin", "Wyoming"]
# Real South Dakota geography that happens to contain a banned word.
ALLOWED_PHRASES = ["Missouri River", "Missouri National Recreational River"]
PAGE_TYPES = {"WebPage", "AboutPage", "ContactPage", "CollectionPage"}
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title = [], 0, [], ""
        self.desc = self.ogdesc = self.twdesc = self.canonical = None
        self.meta = {}
        self._in, self.ids, self.imgs_noalt, self.heads = None, set(), 0, []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("a", "link") and a.get("href"):
            if tag == "link" and a.get("rel") == "canonical":
                self.canonical = a["href"]
            elif tag == "a" or a.get("rel") in ("icon", "apple-touch-icon", "manifest", "stylesheet", "preload"):
                self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
        if tag == "img" and "alt" not in a:
            self.imgs_noalt += 1
        if tag == "h1":
            self.h1 += 1
        if re.fullmatch(r"h[1-6]", tag):
            self.heads.append(int(tag[1]))
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
            if a.get("name") == "description":
                self.desc = a.get("content", "")
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


# Arial widths (per 1000 em) to estimate Google's ~580px title cutoff at 20px.
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_W.update({c: 556 for c in "0123456789"})
_W.update({" ": 278, "|": 260, "&": 667, "-": 333, "–": 556, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889, "+": 584})


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


GUARD = re.compile(r"^<\?php require_once dirname\(__DIR__, (\d+)\) \. '/_guard\.php'; \?>\n")


def page_html(fp, rel):
    """Page HTML; dir/index.php pages must start with the guard line (right depth) and contain no other PHP."""
    s = open(fp, encoding="utf-8").read()
    if fp.endswith(".php"):
        m = GUARD.match(s)
        if not m:
            errors.append(f"{rel}: page does not start with the canonical-host guard line")
        elif int(m.group(1)) != rel.strip("/").count("/"):
            errors.append(f"{rel}: guard depth {m.group(1)} is wrong")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{rel}: stray PHP tag in page HTML")
    return s


def check_ld(rel, blocks):
    for block in blocks:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
        graph = data.get("@graph", [data])
        defined, refs = set(), []

        def walk(o):
            if isinstance(o, dict):
                if "@id" in o and len(o) > 1:
                    defined.add(o["@id"])
                elif "@id" in o:
                    refs.append(o["@id"])
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(graph)
        for r in refs:
            if r not in defined:
                errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
        types = [n.get("@type") for n in graph]
        pnodes = [n for n in graph if n.get("@type") in PAGE_TYPES]
        if "ProfessionalService" not in types or "WebSite" not in types:
            errors.append(f"{rel}: JSON-LD graph lacks ProfessionalService or WebSite")
        if len(pnodes) != 1:
            errors.append(f"{rel}: JSON-LD graph has {len(pnodes)} page nodes (want 1)")
        else:
            pn = pnodes[0]
            for k in ("primaryImageOfPage", "mainEntity"):
                if k not in pn:
                    errors.append(f"{rel}: page node lacks {k}")
            if "BreadcrumbList" in types and "breadcrumb" not in pn:
                errors.append(f"{rel}: page node not linked to its BreadcrumbList")
        biz = next((n for n in graph if n.get("@type") == "ProfessionalService"), {})
        for k in ("logo", "contactPoint", "address", "areaServed", "hasOfferCatalog"):
            if k not in biz:
                errors.append(f"{rel}: ProfessionalService lacks {k}")


titles, descs, desc_len = {}, {}, {}
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        full = os.path.join(dp, f)
        relp = "/" + os.path.relpath(full, ROOT)
        if f == "index.html":
            errors.append(f"{relp}: index.html pages are not allowed (the host would bypass the guard)")
        if f.endswith(".html") and dp != ROOT:
            errors.append(f"{relp}: static .html below the root is not allowed")
        if f.endswith(".html") and dp == ROOT and f not in ("home.html", "404.html", GSC_FILE):
            errors.append(f"{relp}: unexpected root .html file")
        if f in ("home.html", "404.html") and dp == ROOT:
            files.append(full)
        elif f == "index.php" and dp != ROOT and not os.path.relpath(dp, ROOT).startswith("api"):
            files.append(full)

if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("/photo-credits/ exists but must not")

# Search Console verification file: exact bytes, never rewritten.
gsc = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gsc):
    errors.append(f"/{GSC_FILE} is missing")
elif open(gsc, "rb").read() != GSC_BODY:
    errors.append(f"/{GSC_FILE} contents differ from the required single line")

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    raw = page_html(fp, rel)
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    check_ld(rel, p.ld)
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
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
        desc_len[rel] = (len(d), d)
        if not DESC_MIN <= len(d) <= DESC_MAX:
            errors.append(f"{rel}: description {len(d)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not d.rstrip().endswith((".", "!", "?")):
            errors.append(f"{rel}: description does not end with a full sentence")
        if p.ogdesc != p.desc or p.twdesc != p.desc:
            errors.append(f"{rel}: og/twitter description differs from meta description")
    for k in ("og:title", "og:image", "og:image:width", "og:image:height", "og:image:alt", "twitter:card", "twitter:title", "twitter:image", "geo.region"):
        if not p.meta.get(k):
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
        if href.startswith(("http", "mailto:", "tel:", "//")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path:
            frag = href.split("#")[1] if "#" in href else ""
            if frag and frag not in p.ids:
                errors.append(f"{rel}: missing anchor #{frag}")
            continue
        if "photo-credits" in path:
            errors.append(f"{rel}: links to photo credits")
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
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

# Sister-state names anywhere in the deployable output (text files only).
ban = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith((".html", ".php", ".xml", ".txt", ".js", ".css", ".webmanifest", ".svg")):
            continue
        fp = os.path.join(dp, f)
        s = open(fp, encoding="utf-8", errors="ignore").read()
        for ph in ALLOWED_PHRASES:
            s = re.sub(re.escape(ph), "", s, flags=re.I)
        for m in set(x.group(1) for x in ban.finditer(s)):
            errors.append(f"/{os.path.relpath(fp, ROOT)}: mentions sister state '{m}'")

# sitemap.xml must list only real pages and never the verification file.
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
if GSC_FILE in sm or "photo-credits" in sm:
    errors.append("sitemap.xml lists the verification file or photo credits")
for loc in re.findall(r"<loc>(.*?)</loc>", sm):
    path = loc.replace(DOMAIN, "")
    target = os.path.join(ROOT, "home.html") if path == "/" else os.path.join(ROOT, path.strip("/"), "index.php")
    if not os.path.exists(target):
        errors.append(f"sitemap.xml: {loc} has no page")

print(f"checked {len(files)} pages")
if desc_len:
    srt = sorted(desc_len.items(), key=lambda kv: kv[1][0])
    print(f"meta descriptions: shortest {srt[0][1][0]} ({srt[0][0]}), longest {srt[-1][1][0]} ({srt[-1][0]}), all <= {DESC_MAX}: {all(v[0] <= DESC_MAX for v in desc_len.values())}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
