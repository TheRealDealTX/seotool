#!/usr/bin/env python3
"""Post-build checks for public/ (run after build.py). Exits 1 on any error."""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://deniedclaimlaw.com"
KEYWORD = "denied claim law"          # exact match, whole words (so "denied claim lawyer" does not count)
HOME_MIN, HOME_MAX = 6, 10
GUIDE_MIN_WORDS, GUIDE_MAX_WORDS = 900, 2000
BANNED = [r"\bbest\b", r"\btop\b(?!-)", r"\bexpert", r"\bspeciali[sz]", r"\bguarantee(?!s? a similar)", r"\bnumber one\b", r"\b#1\b"]

errors = []


def visible(doc):
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def article_text(doc):
    m = re.search(r'(?s)<article class="prose">(.*?)</article>', doc)
    return visible("<body>" + m.group(1)) if m else ""


pages = {}
for dirpath, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(dirpath, f)
            pages[os.path.relpath(p, OUT)] = open(p, encoding="utf-8").read()

for req in ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php", "api/_lib.php"]:
    if not os.path.exists(os.path.join(OUT, req)):
        errors.append(f"missing public/{req}")

robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.exists(os.path.join(OUT, "robots.txt")) else ""
if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots or "Disallow: /\n" in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

titles, descs = {}, {}
kw_re = re.compile(r"\b" + re.escape(KEYWORD) + r"\b", re.I)

for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    n_h1 = len(re.findall(r"<h1[\s>]", doc))
    if n_h1 != 1:
        errors.append(f"{rel}: expected one <h1>, found {n_h1}")
    t = re.search(r"<title>(.*?)</title>", doc)
    d = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not d or len(d.group(1)) < 50:
        errors.append(f"{rel}: missing/short meta description")
    else:
        descs.setdefault(d.group(1), []).append(rel)
        if len(html.unescape(d.group(1))) > 170:
            errors.append(f"{rel}: meta description over 170 chars")
    expected = ORIGIN + ("/" if rel == "home.html" else "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel))
    if not c or c.group(1) != expected:
        errors.append(f"{rel}: canonical {c.group(1) if c else None} != {expected}")
    if 'noindex' in doc and rel != "404.html":
        errors.append(f"{rel}: page is noindex")
    if 'href="#"' in doc:
        errors.append(f'{rel}: href="#" placeholder')
    for ld in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', doc):
        try:
            json.loads(ld)
        except ValueError as e:
            errors.append(f"{rel}: invalid JSON-LD ({e})")
    for href in re.findall(r'href="(/[^"#?]*)', doc):
        if href == "/":
            continue
        target = os.path.join(OUT, href.lstrip("/"))
        ok = os.path.isfile(os.path.join(target, "index.html")) if href.endswith("/") else os.path.exists(target)
        if not ok:
            errors.append(f"{rel}: broken internal link {href}")
    for page, frag in re.findall(r'href="(/[^"#]*)?#([\w-]+)"', doc):
        tgt = rel if not page else ("home.html" if page == "/" else os.path.join(page.strip("/"), "index.html"))
        if tgt in pages and f'id="{frag}"' not in pages[tgt]:
            errors.append(f"{rel}: missing anchor {page}#{frag}")
    text = visible(doc)
    for pat in BANNED:
        for m in re.finditer(pat, text, re.I):
            errors.append(f"{rel}: banned advertising word '{m.group(0)}' near: ...{text[max(0, m.start() - 40):m.end() + 40]}...")
    for need in ("Attorney advertising", "The Lawgical Firm, P.A.", "Orlando", "Destin", "(407) 433-4131", "not legal advice", "attorney-client relationship"):
        if need not in text:
            errors.append(f"{rel}: footer disclosure missing '{need}'")
    if '"Article"' in doc:
        words = len(article_text(doc).split())
        print(f"  {rel}: {words} words")
        if not GUIDE_MIN_WORDS <= words <= GUIDE_MAX_WORDS:
            errors.append(f"{rel}: guide has {words} words (want {GUIDE_MIN_WORDS}-{GUIDE_MAX_WORDS})")
        for need in ('"FAQPage"', "Last reviewed: October 2026", '"BreadcrumbList"'):
            if need not in doc:
                errors.append(f"{rel}: guide missing {need}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title on {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description on {rels}")

home = pages.get("home.html", "")
if home:
    n = len(kw_re.findall(visible(home)))
    print(f"homepage visible uses of '{KEYWORD}': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1)
    if not title.lower().startswith(KEYWORD):
        errors.append("homepage <title> must start with the keyword")
    if not kw_re.search(re.search(r'name="description" content="([^"]*)"', home).group(1)):
        errors.append("homepage meta description lacks keyword")
    if not kw_re.search(re.search(r"(?s)<h1.*?</h1>", home).group(0)):
        errors.append("homepage H1 lacks keyword")
    if not any(kw_re.search(h) for h in re.findall(r"(?s)<h2.*?</h2>", home)):
        errors.append("no homepage H2 contains keyword")
    first_p = re.search(r"(?s)<h1.*?</h1>\s*<p[^>]*>(.*?)</p>", home)
    if not first_p or not kw_re.search(first_p.group(1)):
        errors.append("homepage first paragraph lacks keyword")
    for typ in ('"WebSite"', '"LegalService"', '"WebPage"'):
        if typ not in home:
            errors.append(f"homepage schema missing {typ}")

n_pages = len([r for r in pages])
print(f"{n_pages} HTML pages")
if not 10 <= n_pages <= 16:
    errors.append(f"{n_pages} pages (want 10-16)")

if errors:
    print("\n".join("ERROR " + e for e in errors))
    sys.exit(1)
print(f"OK - {n_pages} HTML files checked")
