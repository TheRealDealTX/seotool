#!/usr/bin/env python3
"""Post-build checks for public/. Run after build.py; exits non-zero on any problem."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).parent / "public"
KEYWORD = "texas landscape lights"
MIN_HOME_KEYWORD = 14
problems = []


def visible_text(html):
    main = re.search(r"<main.*?</main>", html, re.S).group(0)
    main = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", main, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main)).replace("&amp;", "&")


pages = {}
for f in OUT.rglob("*.html"):
    if f.name.startswith("google"):
        continue
    rel = "/" + str(f.relative_to(OUT))
    url = "/" if rel == "/home.html" else rel.removesuffix("index.html")
    pages[url] = f.read_text()

titles = Counter()
for url, h in pages.items():
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
    titles[t] += 1
    if len(re.findall(r"<h1[\s>]", h)) != 1:
        problems.append(f"{url}: expected one <h1>")
    if not 25 <= len(t) <= 75:
        problems.append(f"{url}: title length {len(t)}")
    if not 40 <= len(d) <= 170:
        problems.append(f"{url}: description length {len(d)}")
    for js in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(js)
        except ValueError as e:
            problems.append(f"{url}: bad JSON-LD ({e})")
    for href in re.findall(r'href="(/[^"#?]*)', h):
        if href.startswith("//"):
            continue
        target = OUT / href.lstrip("/")
        ok = href == "/" or (target.is_file()) or (target / "index.html").is_file()
        if not ok:
            problems.append(f"{url}: broken link {href}")
    if re.search(r"spring ?landscape|springlandscapelighting", h, re.I):
        problems.append(f"{url}: mentions the Spring site")

for t, n in titles.items():
    if n > 1:
        problems.append(f"duplicate title x{n}: {t}")

home = pages["/"]
n = visible_text(home).lower().count(KEYWORD)
print(f'homepage: "{KEYWORD}" appears {n} times in visible copy')
if n < MIN_HOME_KEYWORD:
    problems.append(f"homepage keyword count {n} < {MIN_HOME_KEYWORD}")
if "(281) 704-7210" not in re.search(r"<title>(.*?)</title>", home).group(1):
    problems.append("homepage title is missing the phone number")

for url, h in pages.items():
    if h.count("G-CCJ95Y61X4") != 2:
        problems.append(f"{url}: Google tag missing")
if not (OUT / "googlecccfbf2f7e9e5ae4.html").is_file():
    problems.append("Search Console verification file missing")
sm = (OUT / "sitemap.xml").read_text()
print(f"{len(pages)} html files, {sm.count('<loc>')} sitemap URLs")
for p in problems:
    print("PROBLEM:", p)
sys.exit(1 if problems else 0)
