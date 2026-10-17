#!/usr/bin/env python3
"""Post-build checks: one H1, unique titles/descriptions, valid JSON-LD, no broken internal links or images."""
import json, re, sys
from pathlib import Path
OUT = Path(__file__).parent / "public"
errs, titles, descs = [], {}, {}
pages = [p for p in OUT.rglob("*.html") if not p.name.startswith("google")]
def exists(href):
    path = href.split("#")[0].split("?")[0]
    if path in ("", "/"): return True
    f = OUT / path.lstrip("/")
    return f.is_file() or (f / "index.html").is_file()
for p in pages:
    s = p.read_text()
    rel = "/" + str(p.relative_to(OUT))
    if "gtag/js?id=G-GJD2ZCQXYM" not in s: errs.append(f"{rel}: missing Google tag")
    if 'name="robots" content="noindex' in s and "404" not in rel: errs.append(f"{rel}: noindex")
    if s.count("<h1") != 1: errs.append(f"{rel}: {s.count('<h1')} h1")
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="(.*?)"', s).group(1)
    if t in titles: errs.append(f"{rel}: duplicate title with {titles[t]}")
    if d in descs: errs.append(f"{rel}: duplicate description with {descs[d]}")
    titles[t] = descs[d] = rel
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as e: errs.append(f"{rel}: bad JSON-LD {e}")
    for href in re.findall(r'(?:href|src)="(/[^"]*)"', s):
        if href.startswith("//") or href.startswith("/send.php"): continue
        if not exists(href): errs.append(f"{rel}: broken {href}")
    for tag in re.findall(r"<img [^>]*>", s):
        if 'alt="' not in tag: errs.append(f"{rel}: img without alt")
print(f"{len(pages)} pages checked, {len(errs)} problems")
for e in errs: print(" -", e)
sys.exit(1 if errs else 0)
