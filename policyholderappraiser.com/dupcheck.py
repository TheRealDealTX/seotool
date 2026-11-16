#!/usr/bin/env python3
"""Cross-page duplicate-content report for public/.

For every page, takes the text inside <main>, splits it into sentences and
counts how many of them (by word count) appear verbatim on at least one other
page. Prints the worst pages and the most-repeated sentences.

    python3 dupcheck.py            # report
    python3 dupcheck.py --max 15   # exit 1 if any page is over 15% shared
"""
import html as htmlmod
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")


def pages():
    for dp, _d, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html") and not f.startswith("google"):
                yield os.path.join(dp, f)


def site_path(fs):
    rel = os.path.relpath(fs, OUT)
    return "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def sentences(fs):
    h = open(fs, encoding="utf-8").read()
    m = re.search(r"<main[^>]*>(.*?)</main>", h, re.S)
    body = m.group(1) if m else h
    body = re.sub(r"<(script|style|form|nav|aside)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r'<(ul|p|div)[^>]*class="[^"]*(?:side-list|footer-cities|pill-row|city-pills|faq-links|crumbs)[^"]*"[^>]*>.*?</\1>', " ", body, flags=re.S | re.I)
    body = re.sub(r'<div class="author-box">.*?</div>\s*</div>', " ", body, flags=re.S)
    body = re.sub(r"<(?:h[1-6]|p|li|dt|dd|td|th|summary|div|section|article|aside|span)[^>]*>", "\n", body)
    text = htmlmod.unescape(re.sub(r"<[^>]+>", " ", body))
    out = []
    for chunk in re.split(r"\n|(?<=[.!?])\s+", text):
        s = re.sub(r"\s+", " ", chunk).strip().lower()
        if len(s.split()) >= 6:
            out.append(s)
    return out


data = {site_path(f): sentences(f) for f in pages()}
where = defaultdict(set)
for p, sents in data.items():
    for s in set(sents):
        where[s].add(p)

rows = []
for p, sents in data.items():
    total = sum(len(s.split()) for s in sents)
    shared = sum(len(s.split()) for s in sents if len(where[s]) > 1)
    rows.append((shared / total * 100 if total else 0, shared, total, p))
rows.sort(reverse=True)

limit = None
if "--max" in sys.argv:
    limit = float(sys.argv[sys.argv.index("--max") + 1])

print(f"{'shared%':>8} {'shared':>7} {'words':>6}  page")
for pct, shared, total, p in rows[:25]:
    print(f"{pct:8.1f} {shared:7d} {total:6d}  {p}")
avg = sum(r[0] for r in rows) / len(rows)
print(f"\naverage shared words across {len(rows)} pages: {avg:.1f}%")

print("\nmost repeated sentences (pages, words):")
rep = sorted(((len(ps), len(s.split()), s) for s, ps in where.items() if len(ps) > 1), reverse=True)
for n, w, s in rep[:20]:
    print(f"{n:4d} {w:3d}  {s[:110]}")

if limit is not None:
    bad = [r for r in rows if r[0] > limit]
    if bad:
        print(f"\nFAIL: {len(bad)} pages over {limit}% shared")
        sys.exit(1)
