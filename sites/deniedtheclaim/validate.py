#!/usr/bin/env python3
"""Post-build checks for deniedtheclaim.com. Run after build.py; exits 1 on any error."""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://deniedtheclaim.com"
KEYWORD = "denied the claim"
HOME_MIN, HOME_MAX = 6, 10
GUIDE_MIN_WORDS, GUIDE_MAX_WORDS = 900, 2000
REQUIRED = ["index.php", ".htaccess", "home.html", "404.html", "sitemap.xml", "robots.txt",
            "favicon.svg", "api/lead.php", "api/_lib.php"]
BANNED = re.compile(r"\b(best|top-rated|expert|experts|specialist|specialists|specialize|specializes|guarantee|guaranteed)\b", re.I)

errors, warnings = [], []


def visible(doc, main_only=False):
    body = doc.split("<body", 1)[1]
    if main_only:
        body = body.split('<main id="main">', 1)[1].split("</main>", 1)[0]
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


for f in REQUIRED:
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"public/{f} missing")

robots = open(os.path.join(OUT, "robots.txt")).read() if os.path.exists(os.path.join(OUT, "robots.txt")) else ""
if "Disallow: /\n" in robots or f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
    errors.append("robots.txt must allow crawling and list the sitemap")

pages = {}
for d, _, files in os.walk(OUT):
    for f in files:
        if f.endswith(".html"):
            p = os.path.join(d, f)
            pages[os.path.relpath(p, OUT)] = open(p, encoding="utf-8").read()

titles, descs, canons = {}, {}, {}
for rel, doc in sorted(pages.items()):
    if "{{" in doc:
        errors.append(f"{rel}: unexpanded placeholder")
    if len(re.findall(r"<h1[\s>]", doc)) != 1:
        errors.append(f"{rel}: expected exactly one <h1>")
    t = re.search(r"<title>(.*?)</title>", doc)
    m = re.search(r'<meta name="description" content="([^"]*)"', doc)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', doc)
    if not t or not t.group(1).strip():
        errors.append(f"{rel}: missing <title>")
    else:
        titles.setdefault(t.group(1), []).append(rel)
    if not m or len(m.group(1)) < 50:
        errors.append(f"{rel}: missing/short meta description")
    else:
        descs.setdefault(m.group(1), []).append(rel)
        if len(html.unescape(m.group(1))) > 165:
            warnings.append(f"{rel}: meta description {len(html.unescape(m.group(1)))} chars")
    if not c:
        errors.append(f"{rel}: missing canonical")
    else:
        expect = ORIGIN + ("/" if rel == "home.html" else "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel))
        if c.group(1) != expect:
            errors.append(f"{rel}: canonical {c.group(1)} != {expect}")
        canons.setdefault(c.group(1), []).append(rel)
    if 'href="#"' in doc:
        errors.append(f"{rel}: href=\"#\" placeholder")
    for href in re.findall(r'href="(/[^"]*)"', doc):
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if path == "/":
            target = "home.html"
        elif path.endswith("/"):
            target = path.strip("/") + "/index.html"
        else:
            target = path.lstrip("/")
        if not os.path.exists(os.path.join(OUT, target)):
            errors.append(f"{rel}: broken internal link {href}")
        elif frag and target.endswith(".html") and f'id="{frag}"' not in pages.get(target, ""):
            errors.append(f"{rel}: missing anchor {href}")
    for frag in re.findall(r'href="#([\w-]+)"', doc):
        if f'id="{frag}"' not in doc:
            errors.append(f"{rel}: missing in-page anchor #{frag}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        try:
            graph = json.loads(block)["@graph"]
        except Exception as e:  # noqa: BLE001
            errors.append(f"{rel}: invalid JSON-LD ({e})")
            continue
        types = {n["@type"] for n in graph}
        for need in ("WebSite", "LegalService", "WebPage"):
            if need not in types:
                errors.append(f"{rel}: JSON-LD missing {need}")
        if rel not in ("home.html", "404.html") and "BreadcrumbList" not in types:
            errors.append(f"{rel}: JSON-LD missing BreadcrumbList")
        if '"article": true' in doc or "Last reviewed" in doc and rel != "home.html":
            for need in ("Article", "FAQPage"):
                if need not in types:
                    errors.append(f"{rel}: guide missing {need} schema")
    text = visible(doc)
    for word in BANNED.findall(visible(doc)):
        errors.append(f"{rel}: restricted advertising word '{word}'")
    for need in ("Attorney advertising", "The Lawgical Firm, P.A.", "Orlando", "Destin", "(407) 433-4131",
                 "does not create an attorney-client relationship"):
        if need not in text:
            errors.append(f"{rel}: footer/disclosure missing '{need}'")
    if 'href="/disclaimer/"' not in doc:
        errors.append(f"{rel}: no link to /disclaimer/")
    if "Last reviewed" in doc and rel != "home.html":
        words = len(visible(doc, main_only=True).split())
        print(f"  {rel:70s} {words:5d} words")
        if not GUIDE_MIN_WORDS <= words <= GUIDE_MAX_WORDS + 400:
            errors.append(f"{rel}: guide has {words} words (want ~{GUIDE_MIN_WORDS}-{GUIDE_MAX_WORDS})")

for label, seen in (("title", titles), ("meta description", descs), ("canonical", canons)):
    for value, rels in seen.items():
        if len(rels) > 1:
            errors.append(f"duplicate {label} on {', '.join(rels)}")

home = pages.get("home.html", "")
if home:
    kw = KEYWORD
    text = visible(home)
    lower_exact = text.count(kw)
    any_case = text.lower().count(kw)
    print(f"homepage visible uses of '{kw}': {lower_exact} (plus brand-name uses: {any_case - lower_exact})")
    if not HOME_MIN <= lower_exact <= HOME_MAX:
        errors.append(f"homepage uses '{kw}' {lower_exact} times (want {HOME_MIN}-{HOME_MAX})")
    t = re.search(r"<title>(.*?)</title>", home).group(1)
    if not t.lower().startswith(kw):
        errors.append("homepage <title> must start with the keyword")
    if kw not in strip(re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S).group(1)).lower():
        errors.append("homepage H1 lacks the keyword")
    if kw not in html.unescape(re.search(r'name="description" content="([^"]*)"', home).group(1)).lower():
        errors.append("homepage meta description lacks the keyword")
    first_p = re.search(r'<main id="main">.*?<p class="lede">(.*?)</p>', home, re.S)
    if not first_p or kw not in strip(first_p.group(1)).lower():
        errors.append("homepage first paragraph lacks the keyword")
    if not any(kw in strip(h).lower() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", home, re.S)):
        errors.append("homepage has no H2 with the keyword")

for w in warnings:
    print("warn  " + w)
if errors:
    print("\n".join("ERROR " + e for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK - {len(pages)} HTML files checked")
