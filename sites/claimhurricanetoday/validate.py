#!/usr/bin/env python3
"""Checks the built site in ./public. Run after build.py; exits 1 on any error."""

import html
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://claimhurricanetoday.com"
KEYWORD = "hurricane claim"          # exact-match phrase (singular, case-insensitive)
HOME_MIN, HOME_MAX = 6, 10
REQUIRED = ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt",
            "favicon.svg", "api/lead.php", "api/_lib.php"]

errors, notes = [], []


def visible(doc):
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body))


def kw_count(text):
    return len(re.findall(r"\b" + re.escape(KEYWORD) + r"\b", text, re.I))


for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing public/{f}")

docs = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(d, f)
            docs[os.path.relpath(p, OUT)] = open(p, encoding="utf-8").read()


def url_for(rel):
    if rel == "home.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


titles, descs = {}, {}
for rel, doc in sorted(docs.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded shortcode")
    n_h1 = len(re.findall(r"<h1\b", doc))
    if n_h1 != 1:
        errors.append(f"{rel}: {n_h1} <h1> tags (need exactly 1)")
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not m or not m.group(1).strip():
        errors.append(f"{rel}: missing meta description")
    else:
        descs.setdefault(m.group(1), []).append(rel)
        if not 70 <= len(html.unescape(m.group(1))) <= 170:
            notes.append(f"{rel}: description length {len(html.unescape(m.group(1)))}")
    if not c:
        errors.append(f"{rel}: missing canonical")
    elif c.group(1) != ORIGIN + url_for(rel):
        errors.append(f"{rel}: canonical {c.group(1)} != {ORIGIN + url_for(rel)}")
    if 'href="#"' in doc or "href=''" in doc or 'href=""' in doc:
        errors.append(f"{rel}: placeholder href")
    if "Attorney advertising." not in doc or 'href="/disclaimer/"' not in doc:
        errors.append(f"{rel}: footer advertising disclosure missing")
    if rel != "404.html" and "noindex" in doc:
        errors.append(f"{rel}: noindex on an indexable page")
    for href in re.findall(r'href="(/[^"]*)"', doc):
        path = urlparse(href).path
        frag = urlparse(href).fragment
        if path == "/":
            target = "home.html"
        elif path.endswith("/"):
            target = path.strip("/") + "/index.html"
        else:
            target = path.lstrip("/")
        if not os.path.exists(os.path.join(OUT, target)):
            errors.append(f"{rel}: broken internal link {href}")
        elif frag and target in docs and f'id="{frag}"' not in docs[target]:
            errors.append(f"{rel}: missing anchor {href}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title on {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description on {rels}")

home = docs.get("home.html", "")
if home:
    n = kw_count(visible(home))
    print(f"homepage visible exact-match '{KEYWORD}': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1)
    if not title.lower().startswith(KEYWORD):
        errors.append("homepage <title> must start with the keyword")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S).group(1)
    if KEYWORD not in h1.lower():
        errors.append("homepage H1 lacks the keyword")
    if not any(KEYWORD in re.sub(r"<[^>]+>", "", h).lower() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", home, re.S)):
        errors.append("no homepage H2 contains the keyword")
    if KEYWORD not in re.search(r'<meta name="description" content="([^"]*)"', home).group(1).lower():
        errors.append("homepage meta description lacks the keyword")
    first_p = re.search(r'<p class="lede">(.*?)</p>', home, re.S)
    if not first_p or KEYWORD not in first_p.group(1).lower():
        errors.append("homepage first paragraph lacks the keyword")

# Guide pages: word count, FAQ schema, review stamp
for rel, doc in sorted(docs.items()):
    if '"@type": "Article"' not in doc:
        continue
    art = re.search(r'<article class="prose">(.*?)</article>', doc, re.S)
    words = len(visible("<body>" + art.group(1)).split()) if art else 0
    print(f"  {rel}: {words} words")
    if not 900 <= words <= 2000:
        errors.append(f"{rel}: {words} words (need 900-2000)")
    if '"FAQPage"' not in doc:
        errors.append(f"{rel}: no FAQPage schema")
    if "Last reviewed: October 2026" not in doc:
        errors.append(f"{rel}: no review stamp")

sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(OUT, "sitemap.xml")) else ""
for loc in re.findall(r"<loc>(.*?)</loc>", sm):
    if not loc.startswith(ORIGIN + "/"):
        errors.append(f"sitemap: bad loc {loc}")
robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.exists(os.path.join(OUT, "robots.txt")) else ""
if "Sitemap: " + ORIGIN + "/sitemap.xml" not in robots or "Disallow: /\n" in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

for n in notes:
    print("note  " + n)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(docs)} HTML files checked")
