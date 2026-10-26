#!/usr/bin/env python3
"""Crawl a running copy of the site and check SEO/link hygiene.

    php -S 127.0.0.1:8099 &        # from the bastroproofs/ directory
    python3 bin/validate.py [http://127.0.0.1:8099]
"""
import html, json, re, sys, urllib.request, urllib.error
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8099").rstrip("/")
ORIGIN = "https://bastroproofs.com"
HOME_MIN = 14  # brief: "Bastrop Roofing" at least 14 times on the homepage


def fetch(path):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0; self.links = set(); self.assets = set(); self.imgs_no_alt = 0
        self.ld = []; self._ld = False; self.text = []; self._skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "a" and a.get("href", "").startswith("/"): self.links.add(a["href"].split("#")[0].split("?")[0])
        if tag == "img":
            self.assets.add(a.get("src", ""))
            if "alt" not in a: self.imgs_no_alt += 1
        if tag in ("link", "script") and (a.get("href") or a.get("src") or "").startswith("/"):
            self.assets.add((a.get("href") or a.get("src")).split("?")[0])
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = True
        if tag in ("script", "style"): self._skip += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style"): self._skip -= 1; self._ld = False
    def handle_data(self, d):
        if self._ld: self.ld.append(d)
        elif not self._skip: self.text.append(d)


errors = []
status, sm = fetch("/sitemap.xml")
paths = [u.replace(ORIGIN, "") for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
titles, descs, checked = {}, {}, set()
for path in paths:
    status, body = fetch(path)
    if status != 200: errors.append(f"{path}: HTTP {status}"); continue
    if re.search(r"(Warning|Fatal error|Notice|Deprecated):", body): errors.append(f"{path}: PHP error output")
    p = Page(); p.feed(body)
    t = html.unescape(re.search(r"<title>(.*?)</title>", body).group(1))
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', body).group(1))
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', body).group(1)
    if canon != ORIGIN + path: errors.append(f"{path}: canonical {canon}")
    if p.h1 != 1: errors.append(f"{path}: {p.h1} h1 tags")
    if not 30 <= len(t) <= 70: errors.append(f"{path}: title length {len(t)}")
    if not 110 <= len(d) <= 165: errors.append(f"{path}: description length {len(d)}")
    if t in titles: errors.append(f"{path}: duplicate title with {titles[t]}")
    if d in descs: errors.append(f"{path}: duplicate description with {descs[d]}")
    titles[t] = path; descs[d] = path
    if p.imgs_no_alt: errors.append(f"{path}: {p.imgs_no_alt} img without alt")
    for block in p.ld:
        try: json.loads(block)
        except Exception as e: errors.append(f"{path}: bad JSON-LD {e}")
    for link in p.links | p.assets:
        if link in checked or link.startswith("//"): continue
        checked.add(link)
        if link.startswith("tel:") or link.startswith("mailto:"): continue
        s, _ = fetch(link)
        if s not in (200, 302): errors.append(f"{path}: broken link/asset {link} ({s})")
    if path == "/":
        text = " ".join(p.text)
        n = len(re.findall(r"bastrop roofing", text, re.I))
        title_meta = len(re.findall(r"bastrop roofing", t + " " + d, re.I))
        print(f"Homepage: 'Bastrop Roofing' x{n} in visible body (+{title_meta} in title/description)")
        for kw in ["roofing bastrop", "bastrop roofer", "roofing bastrop tx", "bastrop metal roofing", "bastrop metal roofer"]:
            print(f"  '{kw}': {len(re.findall(kw, text, re.I))}")
        if n < HOME_MIN: errors.append(f"/: only {n} 'Bastrop Roofing' mentions")
    if re.search(r"\bhutto\b|78634|williamson", body, re.I): errors.append(f"{path}: leftover Hutto reference")

print(f"Checked {len(paths)} pages, {len(checked)} unique links/assets.")
if errors:
    print("\n".join("FAIL " + e for e in errors)); sys.exit(1)
print("All checks passed.")
