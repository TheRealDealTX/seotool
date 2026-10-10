#!/usr/bin/env python3
"""Post-build checks for ./public: run after every build."""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
errors, titles, descs = [], {}, {}

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h1 = 0; s.links = []; s.ld = []; s._ld = False; s.title = ""; s._t = False; s.desc = None; s.canon = None
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "h1": s.h1 += 1
        if t == "a" and a.get("href"): s.links.append(a["href"])
        if t in ("link", "script", "img") and (a.get("href") or a.get("src")):
            u = a.get("href") or a.get("src")
            if a.get("rel") == "canonical": s.canon = u
            elif u.startswith("/"): s.links.append(u)
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
        if t == "title": s._t = True
        if t == "meta" and a.get("name") == "description": s.desc = a.get("content")
    def handle_endtag(s, t):
        if t == "script": s._ld = False
        if t == "title": s._t = False
    def handle_data(s, d):
        if s._ld: s.ld[-1] += d
        if s._t: s.title += d

def exists(u):
    p = unquote(u.split("#")[0].split("?")[0])
    if p in ("", "/"): return True
    f = os.path.join(OUT, p.lstrip("/"))
    return os.path.isfile(f) or os.path.isfile(os.path.join(f, "index.html"))

for dp, _, fs in os.walk(OUT):
    for fn in fs:
        if not fn.endswith(".html"): continue
        path = os.path.join(dp, fn); rel = os.path.relpath(path, OUT)
        p = P(); p.feed(open(path, encoding="utf-8").read())
        if p.h1 != 1: errors.append(f"{rel}: {p.h1} h1")
        if not p.desc or not (50 <= len(p.desc) <= 170): errors.append(f"{rel}: description length {len(p.desc or '')}")
        if not (10 <= len(p.title) <= 75): errors.append(f"{rel}: title length {len(p.title)}: {p.title}")
        if rel != "404.html":
            titles.setdefault(p.title, []).append(rel); descs.setdefault(p.desc, []).append(rel)
            if not p.canon: errors.append(f"{rel}: no canonical")
        for b in p.ld:
            try: json.loads(b)
            except Exception as e: errors.append(f"{rel}: bad JSON-LD {e}")
        for u in p.links:
            if u.startswith("/") and not exists(u): errors.append(f"{rel}: broken link {u}")
for k, v in list(titles.items()) + list(descs.items()):
    if len(v) > 1: errors.append(f"duplicate title/description in {v}")
# every legacy URL must be built
import csv
up = "/root/.claude/uploads/dfbe6e78-9c04-56bf-8b56-8b2fb6e92580/"
for f, col in [("7f8dfcc6-yasminsblog.com-organic.Positions-us-20220115-2026-10-10T00_20_44Z.csv", "URL"), ("a59530b5-yasminsblog.com-backlinks.csv", "Target url")]:
    if os.path.exists(up + f):
        for r in csv.DictReader(open(up + f)):
            u = re.sub(r"^https?://(www\.)?yasminsblog\.com", "", r[col]) or "/"
            if not exists(u): errors.append(f"legacy URL not built: {u}")
print("\n".join(errors) or "OK: all checks passed")
sys.exit(1 if errors else 0)
