#!/usr/bin/env python3
"""Post-build checks for thepropertylaw.com. Run after build.py; exits 1 on any error.

Checks: one <h1> per page; <title>, meta description and canonical present,
titles and descriptions unique; canonical = https://thepropertylaw.com + path;
internal links and #anchors resolve; no href="#" placeholders or unexpanded
{{...}}; guide pages have 900-2000 words, an FAQ and FAQPage schema; the
homepage uses the exact phrase "property law" 6-10 times in visible text and
in the title, H1, first paragraph, an H2 and the meta description; no wording
barred by the Florida Bar advertising rules; required files exist.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://thepropertylaw.com"
KEYWORD = re.compile(r"\bproperty law\b", re.I)
HOME_MIN, HOME_MAX = 6, 10
BANNED = re.compile(r"\b(best|top|experts?|expertise|specialists?|speciali[sz]e[sd]?|speciali[sz]ing|guaranteed?|guarantees)\b", re.I)
REQUIRED = ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php", "api/_lib.php"]

errors = []


def text(fragment):
    fragment = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def body_text(doc):
    return text(doc.split("<body", 1)[1])


for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing public/{f}")

pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(d, f)
            pages[os.path.relpath(p, OUT)] = open(p, encoding="utf-8").read()


def url_path(rel):
    if rel == "home.html":
        return "/"
    if rel == "404.html":
        return "/404.html"
    return "/" + rel[: -len("index.html")]


titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    if len(re.findall(r"<h1[\s>]", doc)) != 1:
        errors.append(f"{rel}: expected exactly one <h1>")
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not m or len(m.group(1)) < 50:
        errors.append(f"{rel}: missing or short meta description")
    else:
        descs.setdefault(m.group(1), []).append(rel)
        if len(html.unescape(m.group(1))) > 170:
            errors.append(f"{rel}: meta description over 170 characters")
    if not c:
        errors.append(f"{rel}: missing canonical")
    elif c.group(1) != ORIGIN + url_path(rel):
        errors.append(f"{rel}: canonical {c.group(1)} != {ORIGIN + url_path(rel)}")
    if 'href="#"' in doc:
        errors.append(f'{rel}: href="#" placeholder')
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        try:
            json.loads(raw)
        except ValueError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    for href in re.findall(r'href="([^"]+)"', doc):
        if href.startswith(("http", "tel:", "mailto:")):
            continue
        path, _, frag = href.partition("#")
        if not path:
            target = rel
        elif path == "/":
            target = "home.html"
        elif path.endswith("/"):
            target = os.path.join(path.strip("/"), "index.html")
        else:
            target = path.split("?")[0].lstrip("/")
            if not os.path.exists(os.path.join(OUT, target)):
                errors.append(f"{rel}: broken link {href}")
            continue
        if target not in pages:
            errors.append(f"{rel}: broken link {href}")
        elif frag and f'id="{frag}"' not in pages[target]:
            errors.append(f"{rel}: missing anchor {href}")
    hit = BANNED.search(body_text(doc) + " " + (t.group(1) if t else "") + " " + (m.group(1) if m else ""))
    if hit:
        errors.append(f"{rel}: barred advertising word '{hit.group(0)}'")
    if 'data-kind="guide"' in doc:
        article = re.search(r'<article class="prose">(.*?)</article>', doc, re.S).group(1)
        words = len(text(article).split())
        print(f"  {rel}: {words} words")
        if not 900 <= words <= 2000:
            errors.append(f"{rel}: {words} words (want 900-2000)")
        if '"FAQPage"' not in doc or 'class="faq"' not in doc:
            errors.append(f"{rel}: missing FAQ section/schema")
        if '"Article"' not in doc or "Last reviewed: October 2026" not in doc:
            errors.append(f"{rel}: missing Article schema or review date")
    if "Attorney advertising." not in doc or "/disclaimer/" not in doc or "Orlando" not in doc or "Destin" not in doc:
        errors.append(f"{rel}: footer disclosures incomplete")

for d, rels in list(titles.items()) + list(descs.items()):
    if len(rels) > 1:
        errors.append(f"duplicate title/description on {', '.join(rels)}")

home = pages.get("home.html", "")
if home:
    n = len(KEYWORD.findall(body_text(home)))
    print(f"homepage visible uses of 'property law': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} not in {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1)
    if not title.lower().startswith("property law"):
        errors.append("homepage title does not start with the keyword")
    checks = {
        "H1": re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S).group(1),
        "first paragraph": re.search(r"<p[^>]*>(.*?)</p>", home.split("<main", 1)[1], re.S).group(1),
        "meta description": re.search(r'<meta name="description" content="([^"]*)"', home).group(1),
        "an H2": " ".join(re.findall(r"<h2[^>]*>(.*?)</h2>", home, re.S)),
    }
    for where, frag in checks.items():
        if not KEYWORD.search(text(frag)):
            errors.append(f"homepage {where} lacks the keyword")

robots = open(os.path.join(OUT, "robots.txt")).read()
if "Disallow: /\n" in robots or "Sitemap: " + ORIGIN + "/sitemap.xml" not in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

if errors:
    print("\n".join("ERROR " + e for e in errors))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
