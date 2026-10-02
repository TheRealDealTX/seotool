#!/usr/bin/env python3
"""Post-build checks for dist/: keyword use, links, metadata, schema."""
import html, json, os, re, sys
DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
KW = "the colony public adjuster"
errors, rows = [], []
pages = {}
for base, _d, files in os.walk(DIST):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(base, f); rel = "/" + os.path.relpath(p, DIST).replace("index.html", "")
            pages[rel] = open(p, encoding="utf-8").read()
for url, s in sorted(pages.items()):
    main = re.search(r"<main.*?</main>", s, re.S).group(0)
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", main, flags=re.S)))
    text = re.sub(r"\s+", " ", text).lower()
    kw = text.count(KW)
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    desc = re.search(r'name="description" content="([^"]*)"', s).group(1)
    h1 = len(re.findall(r"<h1[\s>]", s))
    words = len(text.split())
    rows.append((url, kw, len(html.unescape(title)), len(html.unescape(desc)), h1, words))
    if h1 != 1: errors.append(f"{url}: {h1} h1 tags")
    if url == "/" and kw < 8: errors.append(f"homepage keyword count {kw} < 8")
    if url not in ("/404.html",) and kw < 1: errors.append(f"{url}: keyword missing")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as e: errors.append(f"{url}: bad JSON-LD {e}")
    for href in re.findall(r'(?:href|src)="(/[^"#?]*)', s):
        target = os.path.join(DIST, href.lstrip("/"))
        if href.endswith("/"): target = os.path.join(target, "index.html")
        if not os.path.exists(target): errors.append(f"{url}: broken link {href}")
    ids = re.findall(r'\sid="([^"]+)"', s)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup: errors.append(f"{url}: duplicate ids {dup}")
print(f"{'URL':55} KW  TITLE DESC H1 WORDS")
for r in rows: print(f"{r[0]:55} {r[1]:<3} {r[2]:<5} {r[3]:<4} {r[4]:<2} {r[5]}")
print("\n".join(sorted(set(errors))) or "All checks passed.")
sys.exit(1 if errors else 0)
