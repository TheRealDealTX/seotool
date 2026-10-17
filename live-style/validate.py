#!/usr/bin/env python3
"""Post-build checks for public/: links, assets, headings, metadata, JSON-LD, required URLs."""
import json, os, re, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
REQUIRED = """/ /2013/06/30/open-shelving-in-kitchens/ /2013/11/28/open-studio-and-christmas-fair-in-london/
/2013/08/25/swedish-charms/ /2014/03/28/comic-art-ltd-by-john-patrick-reynolds/ /tag/west-elm-james-harrison-rocker/
/2016/02/02/bbc2-great-interior-design-challenge-tennis-racket-upcycle/ /2014/01/26/home-with-house-of-fraser/
/2013/09/28/introducing-made-by-jason/ /2014/09/19/alberto-alessi-living-on-the-line/ /2014/01/03/apartment-therapy-january-cure/
/2016/01/31/why-its-important-to-take-your-pleasure-seriously/ /2014/01/02/west-elm-london/ /2013/11/10/outline-editions/
/2016/01/08/aram-store/ /2015/07/16/final-paint-selections/ /2013/11/26/carine-roitfeld-irreverent/
/2013/08/28/stunning-lighting-by-bocci-exclusively-for-heals/ /2014/02/16/apartment-therapys-january-cure-better-late-than-never/
/2014/07/04/nigella-lawson-almond-cake-recipe/ /tag/wallsandfloors-co-uk/ /2016/04/08/pick-me-up-graphic-arts-festival/
/2013/09/27/eleanor-pritchard-textiles/ /2013/07/14/my-live-style-challenge-favourite-restaurants/ /tag/custard-cream-photography/
/2014/10/18/back-online-with-kakkoii-pantone-speakers/ /2013/11/18/cubit-shelving/ /2016/01/15/one-partially-failed-diy-and-one-gorgeous-runner/
/2014/06/06/the-weekly-crave-heavenly-hammocks/ /2013/08/29/101-things-i-learned-in-architecture-school/
/2016/01/22/end-of-sale-edit/christine-lemieux/ /2013/10/20/house-of-twenty/ /2014/02/02/two-east-london-hotspots/
/2016/01/07/a-p-c-in-the-house/ /category/january-cure/""".split()

def exists(url):
    p = url.split("#")[0].split("?")[0]
    if p == "/": return os.path.isfile(os.path.join(OUT, "home.html"))
    if p in ("/contact.php", "/robots.txt"): return True   # served by PHP
    f = os.path.join(OUT, p.strip("/"))
    return os.path.isfile(os.path.join(f, "index.html")) if p.endswith("/") else os.path.isfile(f)

errors, titles, descs = [], {}, {}
pages = [os.path.join(d, f) for d, _, fs in os.walk(OUT) for f in fs if f.endswith(".html")]
for path in pages:
    rel = os.path.relpath(path, OUT)
    h = open(path, encoding="utf-8").read()
    if h.count("<h1") != 1: errors.append(f"{rel}: {h.count('<h1')} h1")
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
    titles.setdefault(t, []).append(rel); descs.setdefault(d, []).append(rel)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(m.group(1))
        except ValueError as e: errors.append(f"{rel}: bad JSON-LD {e}")
    for m in re.finditer(r'(?:href|src)="(/[^"]*)"', h):
        if not exists(m.group(1)): errors.append(f"{rel}: broken {m.group(1)}")
    for m in re.finditer(r'srcset="([^"]+)"', h):
        for part in m.group(1).split(","):
            if not exists(part.split()[0]): errors.append(f"{rel}: broken srcset {part}")
    for m in re.finditer(r"<img [^>]*>", h):
        if 'alt="' not in m.group(0) or 'alt=""' in m.group(0): errors.append(f"{rel}: img without alt")
for k, v in titles.items():
    if len(v) > 1: errors.append(f"duplicate title {k}: {v}")
for k, v in descs.items():
    if len(v) > 1: errors.append(f"duplicate description: {v}")
for u in REQUIRED:
    if not exists(u): errors.append(f"required URL missing: {u}")
print(f"{len(pages)} pages checked, {len(errors)} problems")
for e in errors[:80]: print(" ", e)
sys.exit(1 if errors else 0)
