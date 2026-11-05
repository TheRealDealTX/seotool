#!/usr/bin/env python3
"""Check every page: internal links resolve, one H1, title/description length, canonical = own URL, CTA present on directory pages."""
import glob, os, re, sys, json
from urllib.parse import unquote, urlsplit
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = 0
def exists(path):
    p = unquote(urlsplit(path).path)
    full = os.path.join(ROOT, p.lstrip("/"))
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html"))
for f in sorted(glob.glob(os.path.join(ROOT, "**/index.html"), recursive=True)):
    if "/_build/" in f: continue
    rel = "/" + os.path.relpath(os.path.dirname(f), ROOT) + "/"
    rel = "/" if rel == "/./" else rel
    t = open(f, encoding="utf-8").read()
    errs = []
    title = re.search(r"<title>(.*?)</title>", t).group(1)
    desc = re.search(r'name="description" content="([^"]*)"', t).group(1)
    import html as H
    if len(H.unescape(title)) > 60: errs.append(f"title {len(H.unescape(title))}")
    if not 70 <= len(H.unescape(desc)) <= 160: errs.append(f"desc {len(H.unescape(desc))}")
    if t.count("<h1") != 1: errs.append("h1 count")
    can = re.search(r'rel="canonical" href="([^"]+)"', t).group(1)
    if unquote(urlsplit(can).path) != rel: errs.append(f"canonical {can}")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S): json.loads(m)
    for h in re.findall(r'href="(/[^"#]*)', t):
        if h.startswith("//"): continue
        if not exists(H.unescape(h)): errs.append(f"broken {h}")
    if rel.count("/") == 3 and rel.startswith(("/SBA-Loan/", "/SBA-Loans/", "/listings/")) and "<!--cta-->" not in t: errs.append("no CTA")
    if errs:
        bad += 1; print(rel, errs[:6])
print("pages with problems:", bad); sys.exit(1 if bad else 0)
