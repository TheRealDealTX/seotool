#!/usr/bin/env python3
"""Post-build SEO and integrity checks for ollieharperstudio.com.

    python3 build.py && python3 validate.py

Exits non-zero on any error. Run it on the production build before deploying.
"""

import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
ORIGIN = "https://ollieharperstudio.com"
GA_ID = "G-7Q3VFC1CX1"
errors, warnings = [], []


def err(f, m): errors.append(f"{f}: {m}")
def warn(f, m): warnings.append(f"{f}: {m}")


def url_to_file(path):
    """Pages are served by index.php from _pages/<slug>.php; everything else is a plain file."""
    path = urlparse(path).path
    if path.endswith("/"):
        return ROOT / "_pages" / ((path.strip("/") or "home") + ".php")
    return ROOT / path.lstrip("/")


def page_url(f):
    rel = f.relative_to(ROOT / "_pages").with_suffix("")
    return "/" if str(rel) == "home" else f"/{rel}/"


pages = sorted((ROOT / "_pages").rglob("*.php")) + [ROOT / "404.html", ROOT / "410.html"]
stray = [p for p in ROOT.rglob("index.html")] + ([ROOT / "home.html"] if (ROOT / "home.html").exists() else [])
for p in stray:
    err(str(p.relative_to(ROOT)), "stray static page: would bypass index.php's https/www redirect")
titles, descs = {}, {}
for f in pages:
    rel = str(f.relative_to(ROOT))
    s = f.read_text(encoding="utf-8")
    if rel.startswith("_pages/"):
        if not s.startswith("<?php if (!defined('OH_PAGE'))"):
            err(rel, "missing direct-access guard")
        s = s.split("?>\n", 1)[1]
    is_error = rel in ("404.html", "410.html")

    if s.count(f"googletagmanager.com/gtag/js?id={GA_ID}") != 1 or s.count(f"gtag('config', '{GA_ID}')") != 1:
        err(rel, "Google tag missing or duplicated")
    elif s.index("gtag/js") > s.index("<title>"):
        warn(rel, "Google tag is not near the top of <head>")

    robots = re.search(r'<meta name="robots" content="([^"]+)"', s)
    if not robots:
        err(rel, "no robots meta")
    elif is_error and "noindex" not in robots.group(1):
        err(rel, "error page must be noindex")
    elif not is_error and "noindex" in robots.group(1):
        err(rel, "page is noindex (staging build deployed?)")

    for icon in ('href="/favicon.ico"', 'href="/favicon.svg"', 'href="/apple-touch-icon.png"', 'href="/site.webmanifest"'):
        if icon not in s:
            err(rel, f"missing icon link {icon}")
    if "hostingersite.com" in s:
        err(rel, "temporary domain leaked into the page")

    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(m.group(1))
        except ValueError as e:
            err(rel, f"invalid JSON-LD: {e}")

    for m in re.finditer(r'<img\b[^>]*>', s):
        if 'alt="' not in m.group(0) or 'alt=""' in m.group(0):
            err(rel, f"image without alt text: {m.group(0)[:80]}")

    for attr in re.findall(r'(?:href|src)="(/[^"#]*)"', s) + [u.split()[0] for ss in re.findall(r'srcset="([^"]+)"', s) for u in ss.split(", ")]:
        if attr.startswith("//"):
            continue
        if not url_to_file(attr.split("?")[0]).exists():
            err(rel, f"broken internal link/asset {attr}")

    if is_error:
        continue
    if s.count("<h1") != 1:
        err(rel, f"{s.count('<h1')} <h1> tags")
    title = unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    desc = unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    if not 25 <= len(title) <= 60:
        err(rel, f"title length {len(title)} (want 25-60): {title}")
    if not 110 <= len(desc) <= 160:
        err(rel, f"description length {len(desc)} (want 110-160)")
    if title in titles:
        err(rel, f"duplicate title with {titles[title]}")
    if desc in descs:
        err(rel, f"duplicate description with {descs[desc]}")
    titles[title], descs[desc] = rel, rel
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    expected = ORIGIN + page_url(f)
    if not canon or canon.group(1) != expected:
        err(rel, f"canonical {canon and canon.group(1)} != {expected}")
    for prop in ("og:title", "og:description", "og:url", "og:image", "twitter:card", "twitter:image"):
        if f'"{prop}"' not in s:
            err(rel, f"missing {prop}")

# robots.txt / sitemap / root files
robots = (ROOT / "robots.txt").read_text()
if "Disallow: /\n" in robots:
    err("robots.txt", "blocks the whole site (staging build?)")
if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
    err("robots.txt", "missing Sitemap line")
locs = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text())
for loc in locs:
    if not loc.startswith(ORIGIN + "/") or not url_to_file(loc[len(ORIGIN):]).exists():
        err("sitemap.xml", f"bad loc {loc}")
for f in ("favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png", "site.webmanifest",
          "web-app-manifest-192x192.png", "web-app-manifest-512x512.png", "googlecccfbf2f7e9e5ae4.html", "assets/img/og.png"):
    if not (ROOT / f).exists():
        err(f, "missing")
gsc = (ROOT / "googlecccfbf2f7e9e5ae4.html").read_text()
if gsc.strip() != "google-site-verification: googlecccfbf2f7e9e5ae4.html":
    err("googlecccfbf2f7e9e5ae4.html", "content altered")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"checked {len(pages)} pages, {len(locs)} sitemap URLs: {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
