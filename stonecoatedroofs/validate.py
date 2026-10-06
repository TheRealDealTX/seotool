"""Post-build checks for stonecoatedroofs.com. Run after build.py; exits non-zero on failure."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
BACKUP = ROOT / "backup" / "wordpress-2026-10-06"
ORIGIN = "https://stonecoatedroofs.com"
errors, warns = [], []


def target(path):
    path = path.split("#")[0].split("?")[0]
    if path == "/":
        return OUT / "home.html"
    if path.endswith("/"):
        return OUT / path.strip("/") / "index.html"
    return OUT / path.lstrip("/")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.title = ""; self.desc = None; self.canon = None; self.ld = []; self.links = []; self.imgs = []
        self._t = None; self.text = []; self.in_main = 0; self.skip = 0; self.main_text = []; self.robots = ""

    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "h1": self.h1 += 1
        if t == "title": self._t = "title"
        if t == "script" and a.get("type") == "application/ld+json": self._t = "ld"
        elif t in ("script", "style"): self.skip += 1
        if t == "meta" and a.get("name") == "description": self.desc = a.get("content")
        if t == "meta" and a.get("name") == "robots": self.robots = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        if t == "a" and a.get("href"): self.links.append(a["href"])
        if t == "img": self.imgs.append(a)
        if t == "main": self.in_main = 1
        if t in ("link",) and a.get("rel") == "stylesheet" and a["href"].startswith("/"): self.links.append(a["href"])
        if t == "script" and a.get("src", "").startswith("/"): self.links.append(a["src"])

    def handle_endtag(self, t):
        if t in ("title", "script") and self._t: self._t = None; return
        if t in ("script", "style") and self.skip: self.skip -= 1
        if t == "main": self.in_main = 0

    def handle_data(self, d):
        if self._t == "title": self.title += d
        elif self._t == "ld": self.ld.append(d)
        elif not self.skip:
            self.text.append(d)
            if self.in_main: self.main_text.append(d)


pages = {}
for f in sorted(OUT.rglob("*.html")):
    if "wp-content" in f.parts:
        continue
    rel = "/" if f.name == "home.html" else "/" + str(f.relative_to(OUT)).replace("index.html", "")
    p = Page(); p.feed(f.read_text()); pages[rel] = p

# 1. every WordPress URL still resolves
old = set()
for sm in ("page-sitemap.xml", "post-sitemap.xml", "category-sitemap.xml"):
    old |= {u.replace(ORIGIN, "") for u in re.findall(r"<loc>([^<]+)</loc>", (BACKUP / "pages" / sm).read_text()) if "/wp-content/" not in u}
for k in ("pages", "posts"):
    old |= {x["link"].replace(ORIGIN, "") for x in json.loads((BACKUP / "api" / f"{k}.json").read_text())}
old.add("/blog/page/2/")
for u in sorted(old):
    if not target(u).exists():
        errors.append(f"old URL missing: {u}")
# every media URL the old site exposed
media = 0
for x in json.loads((BACKUP / "api" / "media_all.json").read_text()):
    urls = [x["source_url"]] + [s["source_url"] for s in (x.get("media_details", {}).get("sizes") or {}).values()]
    for u in urls:
        media += 1
        if not target(u.replace(ORIGIN, "")).exists():
            errors.append(f"media missing: {u}")

# 2. per-page SEO and links
titles, descs = {}, {}
for rel, p in pages.items():
    if rel == "/404.html":
        continue
    if p.h1 != 1: errors.append(f"{rel}: {p.h1} h1 tags")
    if not p.title.strip(): errors.append(f"{rel}: no title")
    if len(p.title) > 70: warns.append(f"{rel}: title {len(p.title)} chars")
    if not p.desc: errors.append(f"{rel}: no meta description")
    elif not 70 <= len(p.desc) <= 165: warns.append(f"{rel}: description {len(p.desc)} chars")
    if p.canon != ORIGIN + rel: errors.append(f"{rel}: canonical {p.canon}")
    titles.setdefault(p.title, []).append(rel); descs.setdefault(p.desc, []).append(rel)
    for blob in p.ld:
        try: json.loads(blob)
        except Exception as e: errors.append(f"{rel}: bad JSON-LD {e}")
    for h in p.links:
        if h.startswith(ORIGIN): h = h[len(ORIGIN):] or "/"
        if h.startswith("/") and not h.startswith("//"):
            h = h.split("?")[0]
            if h in ("/quote.php",): continue
            if not target(h).exists(): errors.append(f"{rel}: broken link {h}")
    for i in p.imgs:
        if not i.get("alt"): errors.append(f"{rel}: img without alt {i.get('src')}")
        if i.get("src", "").startswith("/") and not target(i["src"]).exists(): errors.append(f"{rel}: missing img {i['src']}")
    txt = " ".join(p.text)
    for bad in ("SC Roofs", "utm_source", "lorem", "{{", "None</", "undefined"):
        if bad in txt: errors.append(f"{rel}: contains {bad!r}")
for t, rs in titles.items():
    if len(rs) > 1: errors.append(f"duplicate title {t!r}: {rs}")
for d, rs in descs.items():
    if len(rs) > 1: errors.append(f"duplicate description: {rs}")

# 3. homepage brand mentions (visible main content only)
home = re.sub(r"\s+", " ", " ".join(pages["/"].main_text))
n = home.count("Stone Coated Roofs")
print(f"homepage: 'Stone Coated Roofs' appears {n}x in main content")
if n < 14: errors.append(f"homepage names the brand only {n} times (need 14+)")

# 4. new pages carry their primary keyword
for f in sorted((ROOT / "content" / "new").glob("*.html")):
    m = json.loads(re.match(r"\s*<!--META (.*?) -->", f.read_text(), re.S).group(1))
    rel = f"/service-area/{m['slug']}/" if m["kind"] == "area" else f"/{m['slug']}/"
    p = pages.get(rel)
    if not p: errors.append(f"new page not built: {rel}"); continue
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " "))  # noqa: E731
    if norm(m["keyword"]) not in norm(p.title + " " + (p.desc or "")):
        warns.append(f"{rel}: keyword {m['keyword']!r} not in title/description")

# 5. sitemap entries exist
for u in re.findall(r"<loc>([^<]+)</loc>", (OUT / "sitemap.xml").read_text()):
    if not target(u.replace(ORIGIN, "")).exists(): errors.append(f"sitemap lists missing {u}")
    if u.replace(ORIGIN, "") in pages and "noindex" in pages[u.replace(ORIGIN, "")].robots: errors.append(f"sitemap lists noindex {u}")

print(f"pages={len(pages)} old_urls={len(old)} media_urls={media}")
for w in warns: print("WARN", w)
for e in errors: print("ERROR", e)
print("OK" if not errors else f"{len(errors)} errors")
sys.exit(1 if errors else 0)
