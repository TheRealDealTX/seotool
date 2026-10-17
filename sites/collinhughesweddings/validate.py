#!/usr/bin/env python3
"""SEO / integrity checks for ./public. Run after build.py; exits non-zero on failure."""
import glob, html, json, os, re, sys
from xml.etree import ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
SITE = "https://collinhughesweddings.com"
GA = "G-3FFZD336L6"
errors, titles, descs = [], {}, {}


def err(f, m):
    errors.append(f"{f}: {m}")


def url_for(rel):
    if rel == "home.html":
        return "/"
    return "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel


def exists(path):
    p = path.split("#")[0].split("?")[0]
    if p == "/":
        return True
    fp = os.path.join(ROOT, p.lstrip("/"))
    return os.path.isfile(fp) or os.path.isfile(os.path.join(fp, "index.html"))


for f in sorted(glob.glob(ROOT + "/**/*.html", recursive=True)):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith("google"):
        continue
    s = open(f, encoding="utf-8").read()
    noindex = 'content="noindex' in s
    t = re.search(r"<title>(.*?)</title>", s)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    title = html.unescape(t.group(1)) if t else ""
    desc = html.unescape(d.group(1)) if d else ""
    if not (30 <= len(title) <= 60): err(rel, f"title length {len(title)}: {title}")
    if not noindex and not (110 <= len(desc) <= 160): err(rel, f"description length {len(desc)}")
    if not noindex:
        titles.setdefault(title, []).append(rel); descs.setdefault(desc, []).append(rel)
        c = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not c or c.group(1) != SITE + url_for(rel): err(rel, f"canonical {c and c.group(1)}")
        for tag in ("og:title", "og:description", "og:image", "og:url", "og:image:alt", "twitter:card", "twitter:image"):
            if f'"{tag}"' not in s: err(rel, f"missing {tag}")
        og = re.search(r'property="og:image" content="([^"]+)"', s)
        if og and not exists(og.group(1).replace(SITE, "")): err(rel, "og:image file missing")
    if s.count("<h1") != 1: err(rel, f"{s.count('<h1')} h1 tags")
    if s.count(f"googletagmanager.com/gtag/js?id={GA}") != 1 or f"gtag('config', '{GA}')" not in s: err(rel, "Google tag missing")
    if s.index("gtag/js") > s.index("</head>"): err(rel, "Google tag not in <head>")
    for ico in ('href="/favicon.ico"', 'href="/favicon.svg"', 'href="/apple-touch-icon.png"', 'href="/site.webmanifest"'):
        if ico not in s: err(rel, f"missing icon link {ico}")
    if '<html lang="en">' not in s: err(rel, "lang")
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(m)
        except Exception as ex: err(rel, f"bad JSON-LD {ex}")
    for i in re.findall(r"<img [^>]*>", s):
        if not re.search(r'alt="[^"]+"', i): err(rel, f"img without alt {i[:80]}")
        if "width=" not in i or "height=" not in i: err(rel, f"img without dimensions {i[:80]}")
    for h in re.findall(r'(?:href|src)="(/[^"]*)"', s):
        if not h.startswith("//") and not exists(h): err(rel, f"broken internal link {h}")
    heads = re.findall(r"<h([1-6])", s)
    for a, b in zip(heads, heads[1:]):
        if int(b) - int(a) > 1: err(rel, f"heading jump h{a}->h{b}"); break

for k, v in list(titles.items()) + list(descs.items()):
    if len(v) > 1: err(", ".join(v), f"duplicate title/description: {k[:50]}")

sm = ET.parse(os.path.join(ROOT, "sitemap.xml")).getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
for loc in sm.findall(".//s:url/s:loc", ns):
    if not exists(loc.text.replace(SITE, "")): err("sitemap.xml", f"dead {loc.text}")
for keep in ("/", "/wedding-chrisjasmine/", "/maddy-ben-surrey-uk/"):
    if SITE + keep not in [l.text for l in sm.findall(".//s:url/s:loc", ns)]: err("sitemap.xml", f"missing {keep}")
for need in ("googlecccfbf2f7e9e5ae4.html", "favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png",
             "site.webmanifest", "web-app-manifest-192x192.png", "web-app-manifest-512x512.png", "robots.txt", "index.php"):
    if not os.path.isfile(os.path.join(ROOT, need)): err(need, "missing")
if "google-site-verification: googlecccfbf2f7e9e5ae4.html" not in open(os.path.join(ROOT, "googlecccfbf2f7e9e5ae4.html")).read():
    err("googlecccfbf2f7e9e5ae4.html", "wrong contents")
if os.path.exists(os.path.join(ROOT, "index.html")): err("index.html", "must not exist (host serves it for unknown URLs)")

print("\n".join(errors) if errors else "all checks passed")
sys.exit(1 if errors else 0)
