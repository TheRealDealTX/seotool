#!/usr/bin/env python3
"""Post-build checks for claimroofleak.com. Run after build.py; exits 1 on any error."""

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public")
ORIGIN = "https://claimroofleak.com"
KEYWORD = "roof leak claim"
HOME_MIN, HOME_MAX = 6, 10
GUIDE_MIN_WORDS, GUIDE_MAX_WORDS = 900, 2000

errors, notes = [], []


def visible(doc):
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?is)<(script|style|svg)\b.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def article_text(doc):
    m = re.search(r'(?s)<article class="prose">(.*?)</article>', doc)
    return visible("<body>" + m.group(1)) if m else ""


pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            full = os.path.join(d, f)
            pages[os.path.relpath(full, OUT).replace(os.sep, "/")] = open(full, encoding="utf-8").read()

for need in ("index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php", "api/_lib.php"):
    if not os.path.isfile(os.path.join(OUT, need)):
        errors.append(f"missing public/{need}")

robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.isfile(os.path.join(OUT, "robots.txt")) else ""
if "Disallow: /\n" in robots or f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    expected = "/" if rel == "home.html" else ("/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel)
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    n_h1 = len(re.findall(r"<h1[\s>]", doc))
    if n_h1 != 1:
        errors.append(f"{rel}: {n_h1} <h1> tags (need 1)")
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    dsc = re.search(r'<meta name="description" content="([^"]*)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not dsc or len(dsc.group(1)) < 50:
        errors.append(f"{rel}: missing/short meta description")
    else:
        descs.setdefault(dsc.group(1), []).append(rel)
        if len(dsc.group(1)) > 165:
            notes.append(f"{rel}: meta description {len(dsc.group(1))} chars")
    can = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not can:
        errors.append(f"{rel}: missing canonical")
    elif rel != "404.html" and can.group(1) != ORIGIN + expected:
        errors.append(f"{rel}: canonical {can.group(1)} != {ORIGIN + expected}")
    if 'href="#"' in doc:
        errors.append(f'{rel}: href="#" placeholder')
    if "noindex" in doc and rel != "404.html":
        errors.append(f"{rel}: noindex present (STAGING?)")
    for block in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', doc):
        try:
            json.loads(block)
        except ValueError as e:
            errors.append(f"{rel}: bad JSON-LD ({e})")
    for href in re.findall(r'href="(/[^"]*)"', doc):
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if path in ("", "/"):
            tgt = "home.html"
        elif path.endswith("/"):
            tgt = path.strip("/") + "/index.html"
        else:
            tgt = path.lstrip("/")
        if not os.path.exists(os.path.join(OUT, tgt)):
            errors.append(f"{rel}: broken link {href}")
        elif frag and tgt in pages and f'id="{frag}"' not in pages[tgt]:
            errors.append(f"{rel}: missing anchor {href}")
    for frag in re.findall(r'href="#([^"]+)"', doc):
        if f'id="{frag}"' not in doc:
            errors.append(f"{rel}: missing in-page anchor #{frag}")
    for must in ("Attorney advertising.", "The Lawgical Firm, P.A.", "Orlando", "Destin", "(407) 433-4131",
                 'href="/disclaimer/"', "does not create an attorney-client relationship"):
        if must not in doc:
            errors.append(f"{rel}: footer disclosure missing {must!r}")
    low = visible(doc).lower()
    for banned in (" best ", " top-rated", " expert", "specialist", "specialize", "guarantee"):
        if banned in low and not (banned == "guarantee" and "no guarantee" in low and low.count("guarantee") == low.count("no guarantee")):
            errors.append(f"{rel}: banned advertising word {banned.strip()!r}")
    if 'class="guide"' in doc or '<body class="guide"' in doc:
        words = len(article_text(doc).split())
        notes.append(f"{rel}: {words} words")
        if not (GUIDE_MIN_WORDS <= words <= GUIDE_MAX_WORDS):
            errors.append(f"{rel}: guide is {words} words (need {GUIDE_MIN_WORDS}-{GUIDE_MAX_WORDS})")
        for need in ('"FAQPage"', '"Article"', "Last reviewed:"):
            if need not in doc:
                errors.append(f"{rel}: guide missing {need}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title {t!r}: {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description: {rels}")

home = pages.get("home.html", "")
if home:
    text = visible(home).lower()
    n = text.count(KEYWORD)
    print(f"homepage visible uses of '{KEYWORD}': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1).lower()
    if not title.startswith(KEYWORD):
        errors.append("homepage <title> must start with the keyword")
    h1 = re.search(r"(?s)<h1[^>]*>(.*?)</h1>", home).group(1).lower()
    if KEYWORD not in h1:
        errors.append("homepage H1 lacks keyword")
    if not any(KEYWORD in re.sub("<[^>]+>", "", h).lower() for h in re.findall(r"(?s)<h2[^>]*>(.*?)</h2>", home)):
        errors.append("no homepage H2 contains keyword")
    if KEYWORD not in re.search(r'<meta name="description" content="([^"]*)"', home).group(1).lower():
        errors.append("homepage meta description lacks keyword")
    first_p = re.search(r'(?s)<p class="lead">(.*?)</p>', home)
    if not first_p or KEYWORD not in first_p.group(1).lower():
        errors.append("homepage first paragraph lacks keyword")

sm = open(os.path.join(OUT, "sitemap.xml")).read() if os.path.isfile(os.path.join(OUT, "sitemap.xml")) else ""
for loc in re.findall(r"<loc>([^<]+)</loc>", sm):
    path = loc[len(ORIGIN):]
    tgt = "home.html" if path == "/" else path.strip("/") + "/index.html"
    if tgt not in pages:
        errors.append(f"sitemap lists missing page {loc}")

for n in notes:
    print("  " + n)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML pages validated")
