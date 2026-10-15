#!/usr/bin/env python3
"""Post-build checks for public/ (run after build.py)."""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://deniedfloodclaim.com"
KEYWORD = "denied flood claim"
HOME_MIN, HOME_MAX = 6, 10
GUIDE_MIN, GUIDE_MAX = 900, 2000
BANNED = [r"\bbest\b", r"\btop\b", r"\bexpert", r"\bspecialist", r"\bspecializ", r"\bguarantee(d)?\b(?! a similar)"]
REQUIRED = ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php", "api/_lib.php"]

errors, warnings = [], []


def visible(doc):
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?s)<(script|style|svg)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def article_text(doc):
    m = re.search(r'(?s)<article class="prose">(.*?)</article>', doc)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", html.unescape(t))


for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing public/{f}")

pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(d, f)
            pages[os.path.relpath(p, OUT)] = open(p, encoding="utf-8").read()

titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    n_h1 = len(re.findall(r"<h1[\s>]", doc))
    if n_h1 != 1:
        errors.append(f"{rel}: {n_h1} <h1> tags")
    t = re.search(r"<title>(.*?)</title>", doc)
    dsc = re.search(r'<meta name="description" content="([^"]*)"', doc)
    can = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing title")
    else:
        titles.setdefault(t.group(1), []).append(rel)
        if len(html.unescape(t.group(1))) > 70:
            warnings.append(f"{rel}: title {len(html.unescape(t.group(1)))} chars")
    if not dsc or not dsc.group(1).strip():
        errors.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(dsc.group(1), []).append(rel)
        if not 70 <= len(html.unescape(dsc.group(1))) <= 170:
            warnings.append(f"{rel}: description {len(html.unescape(dsc.group(1)))} chars")
    if not can:
        errors.append(f"{rel}: missing canonical")
    else:
        expect = ORIGIN + ("/" if rel == "home.html" else "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel)
        if can.group(1) != expect:
            errors.append(f"{rel}: canonical {can.group(1)} != {expect}")
    if 'href="#"' in doc:
        errors.append(f'{rel}: href="#" placeholder')
    for href in re.findall(r'href="(/[^"#?]*)', doc):
        if href == "/":
            continue
        target = os.path.join(OUT, href.lstrip("/"))
        ok = os.path.isfile(os.path.join(target, "index.html")) if href.endswith("/") else os.path.exists(target)
        if not ok:
            errors.append(f"{rel}: broken internal link {href}")
    for frag in re.findall(r'href="#([^"]+)"', doc):
        if f'id="{frag}"' not in doc:
            errors.append(f"{rel}: missing in-page anchor #{frag}")
    for block in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', doc):
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    text = visible(doc)
    for pat in BANNED:
        for m in re.finditer(pat, text, re.I):
            errors.append(f"{rel}: banned advertising word '{m.group(0)}' near '{text[max(0, m.start()-40):m.end()+40]}'")
    if "Attorney advertising." not in text or "/disclaimer/" not in doc:
        errors.append(f"{rel}: missing attorney advertising footer")
    if rel != "404.html" and "article" in doc and '<article class="prose">' in doc:
        words = len(article_text(doc).split())
        if not GUIDE_MIN <= words <= GUIDE_MAX:
            errors.append(f"{rel}: guide body {words} words (want {GUIDE_MIN}-{GUIDE_MAX})")
        if '"FAQPage"' not in doc:
            errors.append(f"{rel}: guide without FAQPage schema")
        if '"Article"' not in doc:
            errors.append(f"{rel}: guide without Article schema")
        if "Last reviewed" not in doc:
            errors.append(f"{rel}: guide without Last reviewed line")
        print(f"  {rel}: {words} words")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title on {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description on {rels}")

home = pages.get("home.html", "")
if home:
    n = visible(home).lower().count(KEYWORD)
    print(f"homepage visible uses of '{KEYWORD}': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1).lower()
    if not title.startswith(KEYWORD):
        errors.append("homepage title does not start with the keyword")
    h1 = re.search(r"(?s)<h1[^>]*>(.*?)</h1>", home).group(1)
    if KEYWORD not in re.sub(r"<[^>]+>", "", h1).lower():
        errors.append("keyword missing from homepage H1")
    if not any(KEYWORD in re.sub(r"<[^>]+>", "", h).lower() for h in re.findall(r"(?s)<h2[^>]*>(.*?)</h2>", home)):
        errors.append("keyword missing from homepage H2s")
    if KEYWORD not in re.search(r'name="description" content="([^"]*)"', home).group(1).lower():
        errors.append("keyword missing from homepage meta description")
    first_p = re.search(r'(?s)<p class="lede">(.*?)</p>', home).group(1).lower()
    if KEYWORD not in first_p:
        errors.append("keyword missing from homepage first paragraph")

sm = open(os.path.join(OUT, "sitemap.xml")).read() if os.path.exists(os.path.join(OUT, "sitemap.xml")) else ""
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    path = loc[len(ORIGIN):]
    f = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if f not in pages:
        errors.append(f"sitemap.xml lists missing page {loc}")
robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.exists(os.path.join(OUT, "robots.txt")) else ""
if "Sitemap: " + ORIGIN + "/sitemap.xml" not in robots or "Disallow: /\n" in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

for w in warnings:
    print("WARN  " + w)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
