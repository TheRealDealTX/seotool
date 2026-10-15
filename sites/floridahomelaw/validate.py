#!/usr/bin/env python3
"""Post-build checks for public/ (run after build.py)."""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://floridahomelaw.com"
KEYWORD = "florida home law"          # exact-match phrase, counted case-insensitively
HOME_MIN, HOME_MAX = 6, 12            # visible uses inside <main> on the homepage
REQUIRED = ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt",
            "favicon.svg", "api/lead.php", "api/_lib.php"]

errors, warnings = [], []


def visible(fragment):
    fragment = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", fragment)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment))


def path_for(rel):
    if rel == "home.html":
        return "/"
    if rel == "404.html":
        return "/404.html"
    return "/" + rel[: -len("index.html")]


for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing required file public/{f}")

pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            full = os.path.join(d, f)
            pages[os.path.relpath(full, OUT)] = open(full, encoding="utf-8").read()

titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    n_h1 = len(re.findall(r"<h1[\s>]", doc))
    if n_h1 != 1:
        errors.append(f"{rel}: expected one <h1>, found {n_h1}")
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
        if len(html.unescape(t.group(1))) > 65:
            warnings.append(f"{rel}: title is {len(html.unescape(t.group(1)))} chars")
    if not m or not m.group(1).strip():
        errors.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(m.group(1), []).append(rel)
        if len(html.unescape(m.group(1))) > 170:
            warnings.append(f"{rel}: description is {len(html.unescape(m.group(1)))} chars")
    expected = ORIGIN + path_for(rel)
    if not c:
        errors.append(f"{rel}: missing canonical")
    elif c.group(1) != expected:
        errors.append(f"{rel}: canonical {c.group(1)} != {expected}")
    if re.search(r'href="#"', doc):
        errors.append(f'{rel}: placeholder href="#"')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    for href in re.findall(r'href="(/[^"]*)"', doc):
        target, _, frag = href.partition("#")
        target = target.split("?")[0]
        if target == "/":
            tgt_rel = "home.html"
        elif target.endswith("/"):
            tgt_rel = target.strip("/") + "/index.html"
        else:
            tgt_rel = target.lstrip("/")
        if not os.path.exists(os.path.join(OUT, tgt_rel)):
            errors.append(f"{rel}: broken internal link {href}")
        elif frag and tgt_rel in pages and f'id="{frag}"' not in pages[tgt_rel]:
            errors.append(f"{rel}: missing anchor {href}")
    for frag in re.findall(r'href="#([^"]+)"', doc):
        if f'id="{frag}"' not in doc:
            errors.append(f"{rel}: missing in-page anchor #{frag}")
    if 'robots" content="noindex' in doc and rel != "404.html":
        errors.append(f"{rel}: page is noindex")

for label, seen in (("title", titles), ("description", descs)):
    for value, rels in seen.items():
        if len(rels) > 1:
            errors.append(f"duplicate {label} on {', '.join(rels)}")

home = pages.get("home.html", "")
if home:
    main = home.split('<main id="main">', 1)[-1].split("</main>", 1)[0]
    count = visible(main).lower().count(KEYWORD)
    whole = visible(home.split("<body", 1)[1]).lower().count(KEYWORD)
    print(f"homepage '{KEYWORD}': {count} in main content, {whole} in all visible text (incl. header/footer brand)")
    if not HOME_MIN <= count <= HOME_MAX:
        errors.append(f"homepage keyword count {count} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1).lower()
    if not title.startswith(KEYWORD):
        errors.append("homepage title does not start with the keyword")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S).group(1).lower()
    if KEYWORD not in h1:
        errors.append("homepage H1 lacks the keyword")
    if KEYWORD not in re.search(r'name="description" content="([^"]*)"', home).group(1).lower():
        errors.append("homepage description lacks the keyword")
    first_p = re.search(r"<h1.*?</h1>\s*<p[^>]*>(.*?)</p>", home, re.S).group(1).lower()
    if KEYWORD not in first_p:
        errors.append("homepage first paragraph lacks the keyword")
    if not any(KEYWORD in visible(h).lower() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", home, re.S)):
        errors.append("no homepage H2 contains the keyword")

for rel, doc in pages.items():
    if '"Article"' in doc:
        main = doc.split('<main id="main">', 1)[-1].split("</main>", 1)[0]
        words = len(visible(main).split())
        print(f"  {rel}: {words} words")
        if not 900 <= words <= 2000:
            errors.append(f"{rel}: {words} words (target 900-2000)")
        if '"FAQPage"' not in doc:
            errors.append(f"{rel}: no FAQPage schema")
        if "Last reviewed" not in doc:
            errors.append(f"{rel}: missing 'Last reviewed' line")

for w in warnings:
    print("WARN " + w)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
