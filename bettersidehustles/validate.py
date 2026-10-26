#!/usr/bin/env python3
"""Crawl a running copy of the site and check SEO and link integrity.

    php -S 127.0.0.1:8099 index.php &   # from this folder
    python3 validate.py [base_url]
"""
import json, re, sys, urllib.request, urllib.error
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8099').rstrip('/')
LEGACY = [u.strip().replace('https://bettersidehustles.com', '') for u in open('docs/legacy-urls.txt') if u.strip()]
ALLOWED_REDIRECTS = {'/write-for-us/': '/contact/', '/category/blog/': '/blog/'}
errors, warns = [], []

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
opener = urllib.request.build_opener(NoRedirect)

def get(path):
    try:
        r = opener.open(BASE + path, timeout=20)
        return r.status, r.headers, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode('utf-8', 'replace')

class Page(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.imgs = []; s.h1 = 0; s.ld = []; s._ld = False; s.text = []; s._skip = 0
        s.title = ''; s._t = False; s.desc = None; s.canon = None; s.ids = set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if a.get('id'): s.ids.add(a['id'])
        if t == 'a' and a.get('href'): s.links.append((a['href'], a.get('rel', '')))
        if t == 'img': s.imgs.append(a)
        if t == 'h1': s.h1 += 1
        if t == 'title': s._t = True
        if t == 'meta' and a.get('name') == 'description': s.desc = a.get('content')
        if t == 'link' and a.get('rel') == 'canonical': s.canon = a.get('href')
        if t == 'script' and a.get('type') == 'application/ld+json': s._ld = True
        if t in ('script', 'style', 'svg', 'canvas'): s._skip += 1
    def handle_endtag(s, t):
        if t == 'title': s._t = False
        if t == 'script': s._ld = False
        if t in ('script', 'style', 'svg', 'canvas'): s._skip -= 1
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld.append(d)
        elif not s._skip: s.text.append(d)

seen, queue, titles = {}, ['/'] + LEGACY, {}
while queue:
    path = queue.pop(0)
    if path in seen: continue
    code, hdr, body = get(path)
    seen[path] = code
    if code in (301, 302):
        loc = hdr.get('Location', '').replace('https://bettersidehustles.com', '')
        if ALLOWED_REDIRECTS.get(path) != loc and loc != path + '/':
            errors.append(f'{path}: unexpected redirect to {loc}')
        continue
    if code != 200:
        errors.append(f'{path}: HTTP {code}'); continue
    if 'text/html' not in hdr.get('Content-Type', ''): continue
    p = Page(); p.feed(body)
    if p.h1 != 1: errors.append(f'{path}: {p.h1} <h1> elements')
    if not p.desc or not (110 <= len(p.desc) <= 170): warns.append(f'{path}: meta description length {len(p.desc or "")}')
    if len(p.title) > 70: warns.append(f'{path}: title {len(p.title)} chars')
    if p.title in titles: errors.append(f'{path}: duplicate title with {titles[p.title]}')
    titles[p.title] = path
    if p.canon != 'https://bettersidehustles.com' + path: errors.append(f'{path}: canonical {p.canon}')
    for blob in p.ld:
        try: json.loads(blob)
        except Exception as e: errors.append(f'{path}: bad JSON-LD {e}')
    for img in p.imgs:
        if img.get('alt') is None: errors.append(f'{path}: img without alt {img.get("src")}')
        src = img.get('src', '')
        if src.startswith('/') and src not in seen:
            seen[src] = get(src)[0]
            if seen[src] != 200: errors.append(f'{path}: missing image {src}')
    for href, rel in p.links:
        if 'amazon.' in href:
            if 'tag=bettersidehustles-20' not in href: errors.append(f'{path}: Amazon link without tag {href}')
            if 'sponsored' not in rel: errors.append(f'{path}: Amazon link without rel=sponsored')
        if href.startswith('#') and len(href) > 1 and href[1:] not in p.ids:
            errors.append(f'{path}: broken anchor {href}')
        if href.startswith('/') and not href.startswith('//'):
            h = href.split('#')[0].split('?')[0]
            if h and h not in seen and h not in queue: queue.append(h)
    text = ' '.join(''.join(p.text).split())
    if 'JWeb' in body or 'Write for Us' in text: errors.append(f'{path}: JWeb / Write for Us still present')
    if path == '/':
        n = text.count('Better Side Hustles')
        print(f'Homepage visible mentions of "Better Side Hustles": {n}')
        if n < 14: errors.append(f'homepage mentions brand only {n} times')

# Bossier anchors Google indexed
_, _, b = get('/bossier-city-la-side-hustles-extra-income-with-local-opportunities/')
for a in ['h-1-become-a-casino-dealer', 'h-3-pet-sitting-and-dog-walking', 'h-4-sell-crafts-and-handmade-goods', 'h-5-refer-reserve-of-bossier-city-apartment-homes', 'h-6-freelance-writing-and-blogging']:
    if f'id="{a}"' not in b: errors.append(f'Bossier anchor #{a} missing')

ok = sum(1 for c in seen.values() if c == 200)
print(f'Crawled {len(seen)} URLs ({ok} OK). Legacy URLs checked: {len(LEGACY)}.')
for w in warns: print('WARN ', w)
for e in errors: print('ERROR', e)
sys.exit(1 if errors else 0)
