#!/usr/bin/env python3
"""Crawl a running copy of the site and check every page.

    php -S 127.0.0.1:8765 router.php &   (see README)
    python3 validate.py [base_url]
"""
import json, re, sys, urllib.request, urllib.error, html
from urllib.parse import urljoin, urlparse

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8765'
errors, warns = [], []

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
opener = urllib.request.build_opener(NoRedirect)

def get(path):
    try:
        r = opener.open(BASE + path, timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')

st, sm = get('/sitemap.xml')
pages = [urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
print(len(pages), 'pages in sitemap')
titles, descs, checked = {}, {}, {}

def visible_text(doc):
    doc = re.sub(r'(?s)<(script|style|head)[^>]*>.*?</\1>', ' ', doc)
    return html.unescape(re.sub(r'<[^>]+>', ' ', doc))

for p in pages:
    st, doc = get(p)
    if st != 200:
        errors.append(f'{p}: HTTP {st}'); continue
    if re.search(r'(Warning|Notice|Fatal error|Deprecated)</b>:|Uncaught ', doc):
        errors.append(f'{p}: PHP error in output')
    h1 = re.findall(r'<h1[\s>]', doc)
    if len(h1) != 1: errors.append(f'{p}: {len(h1)} h1 tags')
    t = re.search(r'<title>(.*?)</title>', doc, re.S).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', doc).group(1)
    if len(html.unescape(t)) > 65: warns.append(f'{p}: title {len(html.unescape(t))} chars')
    if not 110 <= len(html.unescape(d)) <= 165: warns.append(f'{p}: description {len(html.unescape(d))} chars')
    if t in titles: errors.append(f'{p}: duplicate title with {titles[t]}')
    if d in descs: errors.append(f'{p}: duplicate description with {descs[d]}')
    titles[t] = p; descs[d] = p
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', doc).group(1)
    if urlparse(canon).path != p: errors.append(f'{p}: canonical {canon}')
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        try: json.loads(blob)
        except Exception as e: errors.append(f'{p}: bad JSON-LD {e}')
    for img in re.findall(r'<img [^>]*>', doc):
        if 'alt=' not in img: errors.append(f'{p}: img without alt {img[:80]}')
    for href in set(re.findall(r'(?:href|src)="(/[^"#?]*)', doc)):
        if href.startswith('//'): continue
        if href not in checked:
            s, _ = get(href)
            checked[href] = s
        if checked[href] != 200: errors.append(f'{p}: link {href} -> {checked[href]}')

st, home = get('/')
n = visible_text(home).count('Luxury Apartment Design')
print('Homepage visible "Luxury Apartment Design" mentions:', n)
if n < 14: errors.append(f'homepage has only {n} brand mentions')
print('Links/assets checked:', len(checked))
for w in warns: print('WARN', w)
for e in errors: print('ERROR', e)
print('OK' if not errors else f'{len(errors)} errors')
sys.exit(1 if errors else 0)
