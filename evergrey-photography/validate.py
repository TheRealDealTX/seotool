#!/usr/bin/env python3
"""Post-build checks for the generated site in public/_pages."""
import glob, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
PAGES = os.path.join(PUB, "_pages")
errors, titles, descs = [], {}, {}
routes = {os.path.relpath(f, PAGES)[:-5] for f in glob.glob(PAGES + "/**/*.html", recursive=True)}


def route_ok(href):
    path = href.split("#")[0].split("?")[0]
    if path == "/":
        return True
    if path.startswith("/assets/") or path in ("/favicon.svg", "/favicon.png", "/apple-touch-icon.png", "/contact.php"):
        return os.path.exists(PUB + path)
    return path.lstrip("/") in routes and path.lstrip("/") != "404"


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1 = 0; self.links = []; self.imgs = []; self.ld = []; self._ld = False
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "h1": self.h1 += 1
        if t == "a" and a.get("href", "").startswith("/"): self.links.append(a["href"])
        if t == "img": self.imgs.append(a)
        if t == "script" and a.get("type") == "application/ld+json": self._ld = True
    def handle_endtag(self, t):
        if t == "script": self._ld = False
    def handle_data(self, d):
        if self._ld: self.ld.append(d)


for r in sorted(routes):
    s = open(os.path.join(PAGES, r + ".html"), encoding="utf-8").read()
    p = P(); p.feed(s)
    if p.h1 != 1: errors.append(f"{r}: {p.h1} h1 tags")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    if r != "404":
        titles.setdefault(t, []).append(r); descs.setdefault(d, []).append(r)
        if not (25 <= len(t) <= 75): errors.append(f"{r}: title length {len(t)}")
        if not (110 <= len(d) <= 165): errors.append(f"{r}: description length {len(d)}")
    for h in p.links:
        if not route_ok(h): errors.append(f"{r}: broken link {h}")
    for i in p.imgs:
        if "alt" not in i: errors.append(f"{r}: img without alt {i.get('src')}")
        src = i.get("src", "")
        if src.startswith("/") and not os.path.exists(PUB + src): errors.append(f"{r}: missing image {src}")
        for part in (i.get("srcset") or "").split(","):
            u = part.strip().split(" ")[0]
            if u and not os.path.exists(PUB + u): errors.append(f"{r}: missing srcset image {u}")
        if i.get("data-src") and not os.path.exists(PUB + i["data-src"]): errors.append(f"{r}: missing {i['data-src']}")
    for block in p.ld:
        try: json.loads(block)
        except ValueError as e: errors.append(f"{r}: bad JSON-LD {e}")
    if re.search(r"\{(ARROW|img:|icon)", s): errors.append(f"{r}: unrendered placeholder")

for k, v in list(titles.items()) + list(descs.items()):
    if len(v) > 1: errors.append(f"duplicate title/description on {v}")

# legacy URLs that carry traffic or backlinks must exist
for need in ("index", "about", "post/kasha-justin", "post/sarina-riley", "post/florence-kyle", "blog", "contact"):
    if need not in routes: errors.append(f"missing legacy page /{need}")

print("\n".join(errors) if errors else f"OK — {len(routes)} pages checked")
sys.exit(1 if errors else 0)
