#!/usr/bin/env python3
"""Post-build checks for public/. Run after build.py."""

import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
PHRASE = "pensacola hurricane"
MIN_HOME = 14

errors = []


def visible_text(doc):
    """Body text a visitor sees: drop <head>, scripts, styles, tags and alt/title attributes."""
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body))


pages = {}
for dirpath, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(dirpath, f)
            pages[os.path.relpath(path, OUT)] = open(path, encoding="utf-8").read()

home = pages.get("home.html")
if not home:
    errors.append("home.html missing")
else:
    n = visible_text(home).lower().count(PHRASE)
    print(f"homepage visible uses of 'Pensacola Hurricane': {n}")
    if n < MIN_HOME:
        errors.append(f"homepage uses the phrase {n} times (< {MIN_HOME})")

for rel, doc in pages.items():
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    if doc.count("<h1") != 1:
        errors.append(f"{rel}: expected exactly one <h1>, found {doc.count('<h1')}")
    for tag in ("<title>", 'name="description"', 'rel="canonical"'):
        if tag not in doc:
            errors.append(f"{rel}: missing {tag}")
    for href in re.findall(r'href="(/[^"#?]*)', doc):
        target = os.path.join(OUT, href.lstrip("/"))
        if href == "/":
            continue
        if href.endswith("/"):
            ok = os.path.isfile(os.path.join(target, "index.html"))
        else:
            ok = os.path.exists(target)
        if not ok:
            errors.append(f"{rel}: broken internal link {href}")
    for anchor in re.findall(r'href="(/[^"#]*)#([\w-]+)"', doc):
        page, frag = anchor
        target = "home.html" if page == "/" else os.path.join(page.strip("/"), "index.html")
        if target in pages and f'id="{frag}"' not in pages[target]:
            errors.append(f"{rel}: missing anchor {page}#{frag}")

if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
