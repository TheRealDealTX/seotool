#!/usr/bin/env python3
"""Post-build checks for public/ (run after build.py). Exits 1 on any error."""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://hurricaneflood.com"
KEYWORD = "hurricane flood"          # exact-match phrase, case-insensitive
HOME_MIN, HOME_MAX = 6, 10           # visible uses on the homepage
GUIDE_MIN, GUIDE_MAX = 900, 2000     # words in the article body of each guide

errors, notes = [], []


def visible(doc):
    body = doc.split("<body", 1)[1]
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body))


def url_for(rel):
    if rel == "home.html":
        return ORIGIN + "/"
    if rel == "404.html":
        return ORIGIN + "/404.html"
    return ORIGIN + "/" + rel[: -len("index.html")]


pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(d, f)
            pages[os.path.relpath(p, OUT).replace(os.sep, "/")] = open(p, encoding="utf-8").read()

for req in ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt", "favicon.svg", "api/lead.php", "api/_lib.php"]:
    if not os.path.exists(os.path.join(OUT, req)):
        errors.append(f"missing public/{req}")

robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.exists(os.path.join(OUT, "robots.txt")) else ""
if "Disallow: /\n" in robots or f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

titles, descs = {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded shortcode")
    if len(re.findall(r"<h1[\s>]", doc)) != 1:
        errors.append(f"{rel}: expected exactly one <h1>")
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not m or len(m.group(1)) < 50:
        errors.append(f"{rel}: missing or short meta description")
    else:
        descs.setdefault(m.group(1), []).append(rel)
        if len(html.unescape(m.group(1))) > 170:
            notes.append(f"{rel}: meta description {len(html.unescape(m.group(1)))} chars")
    if not c:
        errors.append(f"{rel}: missing canonical")
    elif c.group(1) != url_for(rel):
        errors.append(f"{rel}: canonical {c.group(1)} != {url_for(rel)}")
    if 'noindex' in doc and rel != "404.html":
        errors.append(f"{rel}: page is noindex")
    if 'href="#"' in doc or "href=''" in doc or 'href=""' in doc:
        errors.append(f"{rel}: placeholder href")
    for href in re.findall(r'href="(/[^"#?]*)', doc):
        if href == "/":
            continue
        target = os.path.join(OUT, href.lstrip("/"))
        ok = os.path.isfile(os.path.join(target, "index.html")) if href.endswith("/") else os.path.exists(target)
        if not ok:
            errors.append(f"{rel}: broken internal link {href}")
    for page, frag in re.findall(r'href="(/[^"#]*)?#([\w-]+)"', doc):
        tgt = rel if not page else ("home.html" if page == "/" else page.strip("/") + "/index.html")
        if tgt in pages and f'id="{frag}"' not in pages[tgt]:
            errors.append(f"{rel}: missing anchor #{frag}")
    for block in re.findall(r'(?s)<script type="application/ld\+json">(.*?)</script>', doc):
        try:
            graph = json.loads(block)["@graph"]
        except Exception as e:  # noqa: BLE001
            errors.append(f"{rel}: invalid JSON-LD ({e})")
            continue
        types = {g["@type"] for g in graph}
        need = {"WebSite", "LegalService", "WebPage"}
        if rel != "home.html" and rel != "404.html":
            need.add("BreadcrumbList")
        if 'class="pg-guide"' in doc:
            need |= {"Article", "FAQPage"}
        if not need <= types:
            errors.append(f"{rel}: JSON-LD missing {sorted(need - types)}")
    if 'class="pg-guide"' in doc:
        art = re.search(r'(?s)<article class="prose">(.*?)</article>', doc)
        words = len(visible("<body>" + art.group(1)).split()) if art else 0
        notes.append(f"{rel}: {words} words")
        if not GUIDE_MIN <= words <= GUIDE_MAX:
            errors.append(f"{rel}: guide body has {words} words (want {GUIDE_MIN}-{GUIDE_MAX})")
        if "Last reviewed: October 2026" not in doc:
            errors.append(f"{rel}: missing 'Last reviewed' line")
    foot = doc[doc.find('<footer'):]
    for must in ("Attorney advertising", "The Lawgical Firm, P.A.", "Orlando", "Destin", "(407) 433-4131", 'href="/disclaimer/"', "attorney-client relationship"):
        if must not in foot:
            errors.append(f"{rel}: footer missing {must!r}")
    for w in re.findall(r"\b(best|experts?|expertise|specialists?|speciali[sz]\w*|guaranteed|top-rated|leading)\b", visible(doc), re.I):
        errors.append(f"{rel}: Florida Bar-sensitive word {w!r}")

for t, rels in titles.items():
    if len(rels) > 1:
        errors.append(f"duplicate title {t!r}: {rels}")
for d, rels in descs.items():
    if len(rels) > 1:
        errors.append(f"duplicate description: {rels}")

home = pages.get("home.html", "")
if home:
    n = visible(home).lower().count(KEYWORD)
    print(f"homepage visible uses of '{KEYWORD}': {n}")
    if not HOME_MIN <= n <= HOME_MAX:
        errors.append(f"homepage keyword count {n} outside {HOME_MIN}-{HOME_MAX}")
    title = re.search(r"<title>(.*?)</title>", home).group(1).lower()
    if not title.startswith(KEYWORD):
        errors.append("homepage <title> does not start with the keyword")
    h1 = visible("<body>" + re.search(r"(?s)<h1.*?</h1>", home).group(0)).lower()
    if KEYWORD not in h1:
        errors.append("homepage H1 lacks the keyword")
    if not any(KEYWORD in visible("<body>" + h).lower() for h in re.findall(r"(?s)<h2.*?</h2>", home)):
        errors.append("no homepage H2 contains the keyword")
    first_p = re.search(r'(?s)<p class="lede">(.*?)</p>', home)
    if not first_p or KEYWORD not in visible("<body>" + first_p.group(1)).lower():
        errors.append("homepage first paragraph lacks the keyword")
    if KEYWORD not in re.search(r'<meta name="description" content="([^"]*)"', home).group(1).lower():
        errors.append("homepage meta description lacks the keyword")

sm = open(os.path.join(OUT, "sitemap.xml")).read() if os.path.exists(os.path.join(OUT, "sitemap.xml")) else ""
for rel in pages:
    if rel != "404.html" and f"<loc>{url_for(rel)}</loc>" not in sm:
        errors.append(f"sitemap.xml missing {url_for(rel)}")

for n_ in notes:
    print("note  " + n_)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
