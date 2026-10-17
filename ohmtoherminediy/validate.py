#!/usr/bin/env python3
"""Post-build checks for ./public. Exit code 1 on any problem."""
import html, json, os, re, sys
from html.parser import HTMLParser

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
errors, titles, descs = [], {}, {}

class P(HTMLParser):
    def __init__(s): super().__init__(); s.links, s.srcs, s.h1, s.ld, s._ld, s.imgs_noalt, s.ids = [], [], 0, [], False, 0, set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if t == "a" and a.get("href"): s.links.append(a["href"])
        if t in ("img", "script", "link") and (a.get("src") or (t == "link" and a.get("rel") in ("stylesheet", "icon", "manifest", "apple-touch-icon"))):
            s.srcs.append(a.get("src") or a.get("href"))
        if t == "img" and "alt" not in a: s.imgs_noalt += 1
        if t == "img" and a.get("srcset"): s.srcs += [x.strip().split()[0] for x in a["srcset"].split(",")]
        if t == "h1": s.h1 += 1
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
    def handle_endtag(s, t):
        if t == "script": s._ld = False
    def handle_data(s, d):
        if s._ld: s.ld[-1] += d

def exists(u):
    u = u.split("#")[0].split("?")[0]
    if not u: return True
    f = os.path.join(OUT, u.lstrip("/"))
    if u == "/": return os.path.exists(os.path.join(OUT, "home.html"))
    return os.path.isfile(f) or os.path.isfile(os.path.join(f, "index.html"))

for root, _, files in os.walk(OUT):
    for fn in files:
        if not fn.endswith(".html") or fn.startswith("google"): continue
        path = os.path.join(root, fn); rel = os.path.relpath(path, OUT)
        src = open(path, encoding="utf-8").read()
        p = P(); p.feed(src)
        if p.h1 != 1: errors.append("%s: %d h1" % (rel, p.h1))
        if p.imgs_noalt: errors.append("%s: %d img without alt" % (rel, p.imgs_noalt))
        if "{{" in src: errors.append("%s: unreplaced token" % rel)
        if src.count("googletagmanager.com/gtag/js?id=G-9RMEEF538Z") != 1 or "gtag('config', 'G-9RMEEF538Z')" not in src:
            errors.append("%s: Google tag missing or duplicated" % rel)
        if src.find("googletagmanager") > src.find("</head>"): errors.append("%s: Google tag not in <head>" % rel)
        for m in re.findall(r'<meta (?:property|name)="(?:og|twitter):image" content="https://ohmtoherminediy.com(/[^"]+)"', src):
            if not exists(m): errors.append("%s: missing social image %s" % (rel, m))
        if not re.search(r'<link rel="canonical" href="https://ohmtoherminediy.com/', src): errors.append("%s: no canonical" % rel)
        t = re.search(r"<title>(.*?)</title>", src).group(1); d = re.search(r'name="description" content="(.*?)"', src).group(1)
        if rel != "404.html":
            if t in titles: errors.append("dup title %s / %s" % (rel, titles[t]))
            if d in descs: errors.append("dup desc %s / %s" % (rel, descs[d]))
            titles[t], descs[d] = rel, rel
            if len(d) > 165 or len(d) < 110: errors.append("%s: description length %d" % (rel, len(d)))
            if len(html.unescape(t)) > 60: errors.append("%s: title %d chars" % (rel, len(html.unescape(t))))
        for l in p.ld:
            try: json.loads(l)
            except Exception as e: errors.append("%s: bad JSON-LD %s" % (rel, e))
        for l in p.links:
            if l.startswith("#"):
                if l[1:] and l[1:] not in p.ids: errors.append("%s: missing anchor %s" % (rel, l))
            elif l.startswith("/") and not exists(l): errors.append("%s: broken link %s" % (rel, l))
        for s_ in p.srcs:
            if s_ and s_.startswith("/") and not exists(s_): errors.append("%s: missing asset %s" % (rel, s_))

for f in ("sitemap.xml", "robots.txt", "feed.xml", "favicon.ico", "favicon.svg", "favicon-96x96.png", "apple-touch-icon.png",
          "site.webmanifest", "googlecccfbf2f7e9e5ae4.html", "index.php", "home.html", "404.html"):
    if not os.path.isfile(os.path.join(OUT, f)): errors.append("missing root file " + f)
import xml.dom.minidom
for f in ("sitemap.xml", "feed.xml"):
    try: xml.dom.minidom.parse(os.path.join(OUT, f))
    except Exception as e: errors.append("%s invalid XML: %s" % (f, e))
locs = re.findall(r"<loc>https://ohmtoherminediy.com(/[^<]*)</loc>", open(os.path.join(OUT, "sitemap.xml")).read())
for l in locs:
    if not exists(l): errors.append("sitemap url missing: " + l)
print("%d pages checked, %d sitemap urls" % (len(titles), len(locs)))
for e in errors: print("ERROR", e)
sys.exit(1 if errors else 0)
