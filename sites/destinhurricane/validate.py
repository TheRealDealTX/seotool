#!/usr/bin/env python3
"""Checks the built site in public/. Run after build.py; exits 1 on any error."""

import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://destinhurricane.com"
PHRASE = "destin hurricane"      # exact-match keyword, counted case-insensitively
MIN_HOME = 14

errors = []


def visible_text(doc):
    """What a visitor reads: the <body> without scripts, styles, tags or attributes."""
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body))


def first(pattern, doc):
    m = re.search(pattern, doc, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


pages = {}
for dirpath, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(dirpath, f)
            pages[os.path.relpath(path, OUT)] = open(path, encoding="utf-8").read()

for required in ("index.php", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php"):
    if not os.path.exists(os.path.join(OUT, required)):
        errors.append(f"missing public/{required}")

home = pages.get("home.html", "")
if home:
    text = visible_text(home)
    n = text.lower().count(PHRASE)
    print(f"homepage visible uses of '{PHRASE}' (case-insensitive): {n}")
    if n < MIN_HOME:
        errors.append(f"homepage uses the keyword {n} times (< {MIN_HOME})")
    title = first(r"<title>(.*?)</title>", home)
    if not title.lower().startswith(PHRASE):
        errors.append("homepage <title> does not start with the keyword")
    for label, pat in (("H1", r"<h1[^>]*>(.*?)</h1>"), ("meta description", r'name="description" content="([^"]*)"')):
        if PHRASE not in re.sub(r"<[^>]+>", "", first(pat, home)).lower():
            errors.append(f"homepage {label} lacks the keyword")
    if not any(PHRASE in re.sub(r"<[^>]+>", "", h).lower() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", home, re.S)):
        errors.append("no homepage H2 contains the keyword")
    lede = re.sub(r"<[^>]+>", "", first(r'<section class="hero">.*?<p class="lede">(.*?)</p>', home)).lower()
    if PHRASE not in lede:
        errors.append("homepage first paragraph lacks the keyword")

titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    if doc.count("<h1") != 1:
        errors.append(f"{rel}: expected one <h1>, found {doc.count('<h1')}")
    title = first(r"<title>(.*?)</title>", doc)
    desc = first(r'<meta name="description" content="([^"]*)"', doc)
    canon = first(r'<link rel="canonical" href="([^"]*)"', doc)
    if not title:
        errors.append(f"{rel}: missing <title>")
    if not desc:
        errors.append(f"{rel}: missing meta description")
    titles.setdefault(title, []).append(rel)
    descs.setdefault(desc, []).append(rel)
    expected = "/" if rel == "home.html" else ("/" + rel if rel == "404.html" else "/" + rel[: -len("index.html")])
    if canon != ORIGIN + expected:
        errors.append(f"{rel}: canonical {canon!r} should be {ORIGIN + expected!r}")
    if 'href="#"' in doc:
        errors.append(f"{rel}: href=\"#\" placeholder")
    for href in re.findall(r'href="(/[^"#?]*)', doc):
        if href == "/":
            continue
        target = os.path.join(OUT, href.lstrip("/"))
        ok = os.path.isfile(os.path.join(target, "index.html")) if href.endswith("/") else os.path.exists(target)
        if not ok:
            errors.append(f"{rel}: broken internal link {href}")
    for page, frag in re.findall(r'href="(/[^"#]*)#([\w-]+)"', doc):
        target = "home.html" if page == "/" else os.path.join(page.strip("/"), "index.html")
        if target in pages and f'id="{frag}"' not in pages[target]:
            errors.append(f"{rel}: missing anchor {page}#{frag}")
    for frag in re.findall(r'href="#([\w-]+)"', doc):
        if f'id="{frag}"' not in doc:
            errors.append(f"{rel}: missing in-page anchor #{frag}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate <title> {t!r}: {', '.join(rels)}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate meta description on {', '.join(rels)}")

if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
