#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
DOMAIN = "https://oklahomainsuranceappraiser.com"
KEYWORD = "Oklahoma Insurance Appraiser"
MIN_HOME_MENTIONS = 14
DESC_MIN, DESC_MAX = 110, 143          # meta description length (characters), inclusive
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"  # Search Console file: not a page, never checked/renamed/removed here
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
# Sister-site states that must never appear in this build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia", "Kentucky", "Maine", "Maryland",
          "Massachusetts", "Minnesota", "Missouri", "Montana", "Nevada", "New Jersey", "New York", "North Carolina",
          "North Dakota", "Ohio", "Rhode Island", "South Carolina", "Utah", "West Virginia", "Wisconsin", "Wyoming"]
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.ogdesc = self.twdesc = None
        self._in, self.text, self.ids, self.imgs_noalt = None, [], set(), 0
        self._skip = 0
        self.heads = []

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
                self.desc = a.get("content", "")
            if a.get("property") == "og:description":
                self.ogdesc = a.get("content", "")
            if a.get("name") == "twitter:description":
                self.twdesc = a.get("content", "")
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
_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, "–": 556, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


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
        elif int(m.group(1)) != os.path.relpath(fp, ROOT).count("/"):
            errors.append(f"{fp}: guard dirname depth is wrong")
        s = GUARD.sub("", s, count=1)
        if "<?" in s:
            errors.append(f"{fp}: stray PHP tag in page HTML")
    return s


titles, descs, desc_lens = {}, {}, []
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        fp = os.path.join(dp, f)
        if dp == ROOT and f == GSC_FILE:
            continue
        if f.endswith(".html"):
            if dp != ROOT or f not in ("home.html", "404.html"):
                errors.append(f"{fp}: static .html page not allowed (the host would serve it without the guard)")
            files.append(fp)
        elif f == "index.php" and dp != ROOT:
            files.append(fp)
if os.path.exists(os.path.join(ROOT, "index.html")):
    errors.append("root index.html must not exist")

# Search Console verification file: present, exact bytes.
gp = os.path.join(ROOT, GSC_FILE)
if not os.path.exists(gp):
    errors.append(f"missing {GSC_FILE}")
elif open(gp, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} contents differ from the required single line")

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    raw = page_html(fp)
    p = P()
    p.feed(raw)
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            data = json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
            continue
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
        walk(data)
        for r in refs:
            if r not in defined:
                errors.append(f"{rel}: JSON-LD @id reference not resolved: {r}")
        graph = data.get("@graph", [])
        types = [n.get("@type") for n in graph]
        for need in ("ProfessionalService", "WebSite", "BreadcrumbList"):
            if need not in types:
                errors.append(f"{rel}: JSON-LD graph missing {need}")
        pn = [n for n in graph if n.get("@type") in ("WebPage", "AboutPage", "ContactPage", "CollectionPage")]
        if len(pn) != 1:
            errors.append(f"{rel}: JSON-LD needs exactly one page node, found {len(pn)}")
        else:
            for k in ("breadcrumb", "primaryImageOfPage", "mainEntity"):
                if k not in pn[0]:
                    errors.append(f"{rel}: page node missing {k}")
        biz = next((n for n in graph if n.get("@type") == "ProfessionalService"), {})
        for k in ("logo", "contactPoint", "areaServed", "hasOfferCatalog", "address"):
            if k not in biz:
                errors.append(f"{rel}: ProfessionalService missing {k}")
    head = raw.split("</head>")[0]
    for tag in ('rel="canonical" href="' + DOMAIN, 'property="og:image:width"', 'property="og:image:alt"', 'name="twitter:card"', 'name="geo.region"'):
        if tag not in head:
            errors.append(f"{rel}: head missing {tag}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
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
        errors.append(f"{rel}: description doesn't end with a full sentence")
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
        if GSC_FILE in path:
            errors.append(f"{rel}: links to the Search Console file")
        if "photo-credits" in path:
            errors.append(f"{rel}: links to a photo credits page")
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

# sitemap.xml must list every indexable page, and nothing else.
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
for u in locs:
    pth = u.replace(DOMAIN, "")
    tgt = os.path.join(ROOT, "home.html") if pth == "/" else os.path.join(ROOT, pth.strip("/"), "index.php")
    if not os.path.exists(tgt):
        errors.append(f"sitemap.xml lists missing page {u}")
    if GSC_FILE in u or "photo-credits" in u:
        errors.append(f"sitemap.xml must not list {u}")
if len(locs) != len(files) - 1:
    errors.append(f"sitemap.xml has {len(locs)} URLs but there are {len(files) - 1} indexable pages")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page must not exist")

# Stray references to sister-site states (pages, scripts, styles, PHP and text files)
ban_re = re.compile(r"\b(" + "|".join(re.escape(b) for b in BANNED) + r")\b", re.I)
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith((".html", ".php", ".js", ".css", ".txt", ".xml", ".webmanifest", ".json", ".svg")):
            fp = os.path.join(dp, f)
            for m in set(x.group(0) for x in ban_re.finditer(open(fp, encoding="utf-8", errors="ignore").read())):
                errors.append(f"{fp}: mentions sister state '{m}'")

desc_lens.sort()
print(f"checked {len(files)} pages; meta descriptions {desc_lens[0][0]}–{desc_lens[-1][0]} chars")
print(f"  shortest: {desc_lens[0][0]} {desc_lens[0][1]}")
print(f"  longest:  {desc_lens[-1][0]} {desc_lens[-1][1]}")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
print("OK — zero errors" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
