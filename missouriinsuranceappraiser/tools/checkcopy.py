#!/usr/bin/env python3
"""Pre-build copy check for the content modules in src/ (run: python3 tools/checkcopy.py [services|locations|learn]).

Checks SEO titles (<=60 chars, <=~580px at 20px Arial), meta descriptions (110-150 chars), uniqueness,
banned sister-state names, and heading order inside HTML bodies (no h1, first heading h2, no skipped levels)."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_px import title_px  # noqa: E402

BANNED = ["Alabama", "Florida", "Georgia", "Texas", "Carolina"]
errs = []


def heads(where, html, start=1):
    """start = level of the heading that precedes this HTML on the page (h1 in the hero)."""
    if re.search(r"<h1[\s>]", html):
        errs.append(f"{where}: contains <h1>")
    prev = start
    for lv in [int(x) for x in re.findall(r"<h([1-6])[\s>]", html)]:
        if lv > prev + 1:
            errs.append(f"{where}: heading jump h{prev}->h{lv}")
            break
        prev = lv


def banned(where, text):
    for w in BANNED:
        if re.search(w, text, re.I):
            errs.append(f"{where}: banned word {w}")


def seo(where, title, desc):
    if len(title) > 60:
        errs.append(f"{where}: title {len(title)} chars: {title}")
    if title_px(title) > 580:
        errs.append(f"{where}: title ~{title_px(title):.0f}px: {title}")
    if not 110 <= len(desc) <= 150:
        errs.append(f"{where}: desc {len(desc)} chars: {desc}")


def walk_strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk_strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from walk_strings(v)


which = sys.argv[1:] or ["services", "locations", "learn"]
titles, descs = {}, {}
for mod in which:
    m = __import__(mod)
    for name in dir(m):
        if name.isupper():
            banned(f"{mod}.{name}", " ".join(walk_strings(getattr(m, name))))
    if mod == "services":
        for s in m.SERVICES:
            for k in ("slug", "name", "short", "kw", "h1", "lede", "facts", "body", "faqs", "title", "desc"):
                if k not in s:
                    errs.append(f"service {s.get('slug')}: missing {k}")
            seo(f"service {s['slug']}", s["title"], s["desc"])
            heads(f"service {s['slug']}", s["body"])
            titles.setdefault(s["title"], []).append(s["slug"]); descs.setdefault(s["desc"], []).append(s["slug"])
        print(len(m.SERVICES), "services")
    if mod == "locations":
        slugs = {l["slug"] for l in m.LOCATIONS}
        for l in m.LOCATIONS:
            for k in ("slug", "city", "geo", "county", "region", "perils", "housing", "hoods", "storms", "near", "lede", "body", "faqs", "title", "desc"):
                if k not in l:
                    errs.append(f"location {l.get('slug')}: missing {k}")
            for n in l.get("near", []):
                if n not in slugs:
                    errs.append(f"location {l['slug']}: near '{n}' is not a location slug")
            seo(f"location {l['slug']}", l["title"], l["desc"])
            heads(f"location {l['slug']}", l["body"])
            titles.setdefault(l["title"], []).append(l["slug"]); descs.setdefault(l["desc"], []).append(l["slug"])
        print(len(m.LOCATIONS), "locations")
    if mod == "learn":
        heads("PROCESS_INTRO", m.PROCESS_INTRO)
        for n, h in m.PROCESS_STEPS:
            heads(f"process step {n}", h, start=2)
        heads("PROCESS_OUTRO", m.PROCESS_OUTRO)
        print(len(m.PROCESS_STEPS), "process steps,", sum(len(q) for _, q in m.FAQ), "FAQs in", len(m.FAQ), "groups,", len(m.GLOSSARY), "terms,", len(m.POSTS), "posts")
        for p in m.POSTS:
            for k in ("slug", "title", "seo", "desc", "summary", "date", "read", "body"):
                if k not in p:
                    errs.append(f"post {p.get('slug')}: missing {k}")
            seo(f"post {p['slug']}", p["seo"], p["desc"])
            heads(f"post {p['slug']}", p["body"])
            titles.setdefault(p["seo"], []).append(p["slug"]); descs.setdefault(p["desc"], []).append(p["slug"])
for d in (titles, descs):
    for k, v in d.items():
        if len(v) > 1:
            errs.append(f"duplicate title/desc {k!r}: {v}")
for e in errs:
    print("ERROR", e)
print("OK" if not errs else f"{len(errs)} errors")
sys.exit(1 if errs else 0)
