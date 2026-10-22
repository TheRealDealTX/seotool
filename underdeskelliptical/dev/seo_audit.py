#!/usr/bin/env python3
"""Extra on-page SEO audit over every sitemap URL (run alongside check.py).

Checks each HTML page for: the GA4 tag, favicon/manifest links, og/twitter image tags
with dimensions, <img> alt text and width/height, heading order (no skipped levels
after the H1), and https-only asset URLs.
"""
import os, re, sys, urllib.request
BASE = os.environ.get('BASE', 'http://127.0.0.1:8090')
GA = 'G-XZNNQ99Z4G'
get = lambda p: urllib.request.urlopen(BASE + p).read().decode()
urls = []
for sm in re.findall(r'<loc>https://underdeskelliptical\.com([^<]+)</loc>', get('/sitemap_index.xml')):
    urls += re.findall(r'<loc>https://underdeskelliptical\.com([^<]+)</loc>', get(sm))
problems = []
for u in urls:
    h = get(u)
    head = h[:h.find('</head>')]
    need = [f"gtag/js?id={GA}", f"gtag('config', '{GA}')", 'rel="icon" href="/favicon.ico"', 'rel="apple-touch-icon"',
            'rel="manifest"', 'og:image:width', 'twitter:image', 'name="theme-color"', 'application/rss+xml']
    for n in need:
        if n not in head:
            problems.append(f'{u}: missing {n}')
    if head.find('gtag/js') > 200:
        problems.append(f'{u}: Google tag is not at the top of <head>')
    body = h[h.find('<body'):]
    for img in re.findall(r'<img\b[^>]*>', body):
        if not re.search(r'\salt="[^"]+"', img) and 'alt=""' not in img:
            problems.append(f'{u}: img without alt {img[:80]}')
        if 'width=' not in img or 'height=' not in img:
            problems.append(f'{u}: img without dimensions {img[:80]}')
    levels = [int(x) for x in re.findall(r'<h([1-6])[\s>]', body)]
    for a, b in zip(levels, levels[1:]):
        if b > a + 1:
            problems.append(f'{u}: heading jumps h{a} -> h{b}')
            break
    if re.search(r'(src|href)="http://', h):
        problems.append(f'{u}: insecure http:// asset')
print(f'audited {len(urls)} pages')
for p in sorted(set(problems)):
    print('PROBLEM', p)
print('OK' if not problems else f'{len(set(problems))} problems')
