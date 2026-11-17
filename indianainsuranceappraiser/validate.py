#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any error."""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
KEYWORD = "Indiana Insurance Appraiser"
GSC_FILE = "googlecccfbf2f7e9e5ae4.html"
GSC_BODY = b"google-site-verification: googlecccfbf2f7e9e5ae4.html"
DESC_MIN, DESC_MAX = 110, 143
# Sister-site states that must never leak into this build.
BANNED = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
          "Hawaii", "Idaho", "Illinois", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
          "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
          "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
          "Washington", "West Virginia", "Wisconsin", "Wyoming"]
# Allowed in-context uses (e.g. Ohio River, Lake Michigan, neighboring-state facts). Matched case-sensitively and removed before the banned-word scan.
ALLOW = ["Ohio River", "Lake Michigan"]
MIN_HOME_MENTIONS = 14
errors, warns = [], []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.h1, self.ld, self.title, self.desc = [], 0, [], "", None
        self.meta = {}
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
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self.heads.append(int(tag[1]))
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        if tag == "meta" and (a.get("property") or a.get("name")):
            self.meta[a.get("property") or a.get("name")] = a.get("content", "")
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
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})
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


titles, descs, alld = {}, {}, []
files = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == GSC_FILE and dp == ROOT:
            continue
        if f.endswith(".html") or (f == "index.php" and dp != ROOT):
            files.append(os.path.join(dp, f))

for fp in sorted(files):
    rel = "/" + os.path.relpath(fp, ROOT)
    p = P()
    p.feed(page_html(fp))
    if p.h1 != 1:
        errors.append(f"{rel}: {p.h1} h1 tags")
    for block in p.ld:
        try:
            json.loads(block)
        except Exception as ex:
            errors.append(f"{rel}: bad JSON-LD {ex}")
    if p.imgs_noalt:
        errors.append(f"{rel}: {p.imgs_noalt} images without alt")
    t = html.unescape(p.title.strip())
    if not rel.endswith("404.html"):
        titles.setdefault(t, []).append(rel)
        if len(t) > 60:
            errors.append(f"{rel}: title {len(t)} chars (max 60): {t}")
        if title_px(t) > 580:
            errors.append(f"{rel}: title ~{title_px(t):.0f}px (max 580): {t}")
    if p.desc is None:
        errors.append(f"{rel}: missing meta description")
    else:
        if not rel.endswith("404.html"):
            descs.setdefault(p.desc, []).append(rel)
        if not DESC_MIN <= len(p.desc) <= DESC_MAX:
            errors.append(f"{rel}: description {len(p.desc)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not p.desc.rstrip().endswith((".", "!", "?")):
            errors.append(f"{rel}: description does not end with a complete sentence")
        alld.append((len(p.desc), rel))
        for k in ("og:description", "twitter:description"):
            if html.unescape(p.meta.get(k, "")) != html.unescape(p.desc):
                errors.append(f"{rel}: {k} differs from meta description")
    for k in ("og:image:width", "og:image:height", "og:image:alt", "twitter:card", "geo.region"):
        if k not in p.meta:
            errors.append(f"{rel}: missing {k}")
    if '<link rel="canonical" href="https://indianainsuranceappraiser.com/' not in page_html(fp):
        errors.append(f"{rel}: canonical missing or off-domain")
    ids, refs = set(), set()
    def walk(o):
        if isinstance(o, dict):
            if "@id" in o and len(o) > 1:
                ids.add(o["@id"])
            elif "@id" in o:
                refs.add(o["@id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for block in p.ld:
        try:
            walk(json.loads(block))
        except Exception:
            pass
    for r in refs - ids:
        errors.append(f"{rel}: JSON-LD @id reference does not resolve: {r}")
    gtypes = re.findall(r'"@type":"(WebPage|AboutPage|ContactPage|CollectionPage)"', "".join(p.ld))
    if len(gtypes) != 1:
        errors.append(f"{rel}: expected exactly one page node, found {gtypes}")
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
        target = os.path.join(ROOT, path.lstrip("/"))
        if path == "/":
            target = os.path.join(ROOT, "home.html")
        elif path.endswith("/"):
            target = os.path.join(target, "index.php")
        if not os.path.exists(target):
            errors.append(f"{rel}: broken link {href}")
    if rel == "/home.html":
        main = " ".join(p.text)
        main = re.sub(r"\s+", " ", main)
        body_only = main.split("Skip to content", 1)[-1]
        n_all = body_only.count(KEYWORD)
        # Count inside <main> only (exclude header/footer brand text)
        raw = page_html(fp)
        m = re.search(r"<main[^>]*>(.*)</main>", raw, re.S)
        mtext = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
        mtext = re.sub(r"<script.*?</script>", " ", mtext, flags=re.S)
        n_main = mtext.count(KEYWORD)
        print(f"homepage '{KEYWORD}': {n_main} in main content, {n_all} in all visible text")
        if n_main < MIN_HOME_MENTIONS:
            errors.append(f"homepage keyword count {n_main} < {MIN_HOME_MENTIONS}")

for t, ps in titles.items():
    if len(ps) > 1:
        errors.append(f"duplicate title '{t}': {ps}")
for d, ps in descs.items():
    if len(ps) > 1:
        errors.append(f"duplicate description: {ps}")

# Stray references to sister-state sites
scan = list(files) + [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT) for f in fs if f.endswith((".js", ".css", ".xml", ".txt", ".webmanifest", ".php")) and "/api/" not in dp]
for fp in sorted(set(scan)):
    s = open(fp, encoding="utf-8", errors="ignore").read()
    for a in ALLOW:
        s = s.replace(a, "")
    s = s.replace("indianainsuranceappraiser", "")
    for st in BANNED:
        if re.search(r"\b" + st + r"\b", s, re.I) or st.replace(" ", "").lower() + "insuranceappraiser" in s.lower():
            errors.append(f"{fp}: mentions sister state {st}")

# No photo-credits page, no dir/index.html, no root index.html
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f == "index.html":
            errors.append(f"{os.path.join(dp, f)}: index.html pages are not allowed (guard would be skipped)")
if os.path.exists(os.path.join(ROOT, "photo-credits")):
    errors.append("photo-credits page exists")
for fp in files:
    if "photo-credits" in open(fp, encoding="utf-8").read():
        errors.append(f"{fp}: links to photo-credits")
stray_html = [f for f in os.listdir(ROOT) if f.endswith(".html") and f not in ("home.html", "404.html", GSC_FILE)]
if stray_html:
    errors.append(f"unexpected root .html files: {stray_html}")

# Search Console verification file: exact bytes, not in sitemap
gp = os.path.join(ROOT, GSC_FILE)
if not os.path.isfile(gp) or open(gp, "rb").read() != GSC_BODY:
    errors.append(f"{GSC_FILE} missing or not byte-exact")
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
if GSC_FILE in sm or "photo-credits" in sm:
    errors.append("sitemap.xml lists the GSC file or photo-credits")
if GSC_FILE.replace(".html", "") in open(os.path.join(ROOT, "robots.txt")).read():
    errors.append("robots.txt mentions the GSC file")
for fp in files:
    if GSC_FILE in open(fp, encoding="utf-8").read():
        errors.append(f"{fp}: links to the GSC file")

if alld:
    alld.sort()
    print(f"descriptions: shortest {alld[0][0]} ({alld[0][1]}), longest {alld[-1][0]} ({alld[-1][1]}), all < 144: {all(n < 144 for n, _ in alld)}")

print(f"checked {len(files)} html files")
for w in warns:
    print("WARN ", w)
for er in errors:
    print("ERROR", er)
sys.exit(1 if errors else 0)
