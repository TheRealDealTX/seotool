#!/usr/bin/env python3
"""Crawl the site from a running server and check SEO/link basics.

    cd public_html && php -S 127.0.0.1:8099 router-dev.php &
    python3 validate.py [base_url]

Checks every route in inc/pages.php: HTTP 200, one <h1>, unique title and
meta description (with length warnings), canonical, valid JSON-LD, no PHP
warnings in the output, every internal link and asset resolves, every <img>
has alt text, and the homepage names "Cowboy Tiny Homes" at least 14 times.
"""
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8099').rstrip('/')
ROOT = Path(__file__).parent / 'public_html'
routes = re.findall(r"^    '(/[^']*)' => \[", (ROOT / 'inc/pages.php').read_text(), re.M)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None

opener = urllib.request.build_opener(NoRedirect)

def fetch(path):
    try:
        r = opener.open(BASE + path, timeout=20)
        return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), e.headers

errors, warns = [], []
titles, descs = {}, {}
links = set()

for path in routes:
    status, body, _ = fetch(path)
    if status != 200:
        errors.append(f'{path}: HTTP {status}')
        continue
    if re.search(r'(Warning|Notice|Deprecated|Fatal error)</b>:|Warning: |Notice: ', body):
        errors.append(f'{path}: PHP warning/notice in output')
    h1 = re.findall(r'<h1[\s>]', body)
    if len(h1) != 1:
        errors.append(f'{path}: {len(h1)} <h1> tags')
    t = html.unescape(re.search(r'<title>(.*?)</title>', body, re.S).group(1))
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', body).group(1))
    titles.setdefault(t, []).append(path)
    descs.setdefault(d, []).append(path)
    if len(t) > 65: warns.append(f'{path}: title {len(t)} chars')
    if not 110 <= len(d) <= 165: warns.append(f'{path}: description {len(d)} chars')
    if f'<link rel="canonical" href="https://cowboytinyhomes.com{path}">' not in body:
        errors.append(f'{path}: canonical missing/wrong')
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try:
            json.loads(block)
        except ValueError as ex:
            errors.append(f'{path}: bad JSON-LD ({ex})')
    for img in re.findall(r'<img\b[^>]*>', body):
        if not re.search(r'\balt="[^"]+"', img):
            errors.append(f'{path}: img without alt: {img[:80]}')
    for href in re.findall(r'(?:href|src)="(/[^"#]*)', body):
        links.add(html.unescape(href).split('?')[0] or '/')
    for href in re.findall(r'href="https://cowboytinyhomes\.com(/[^"#?]*)', body):
        links.add(href)
    if path == '/':
        main = re.search(r'<main.*?</main>', body, re.S).group(0)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', main, flags=re.S)))
        n = text.count('Cowboy Tiny Homes')
        words = len(text.split())
        print(f'homepage: "Cowboy Tiny Homes" x{n} in visible main content, {words} words')
        if n < 14:
            errors.append(f'homepage: brand named only {n} times (< 14)')

for t, ps in titles.items():
    if len(ps) > 1: errors.append(f'duplicate title {t!r}: {ps}')
for d, ps in descs.items():
    if len(ps) > 1: errors.append(f'duplicate description: {ps}')

for link in sorted(links):
    status, _, hdr = fetch(link)
    if status == 301 and link.rstrip('/') + '/' in routes:
        continue
    if status != 200:
        errors.append(f'broken link/asset {link}: HTTP {status}')

# Spot-check redirects and 404s.
for old, new in [('/category/park-models/', '/park-model-homes-texas/'), ('/faqs', '/faqs/'), ('/wp-admin/', '/')]:
    status, _, hdr = fetch(old)
    if status != 301 or not (hdr.get('Location') or '').endswith(new):
        errors.append(f'redirect {old} -> {new} failed ({status} {hdr.get("Location")})')
status, _, _ = fetch('/no-such-page/')
if status != 404:
    errors.append(f'unknown URL returned {status}, expected 404')

print(f'{len(routes)} routes, {len(links)} unique internal links/assets checked')
for w in warns: print('WARN ', w)
for e in errors: print('ERROR', e)
print('OK' if not errors else f'{len(errors)} error(s)')
sys.exit(1 if errors else 0)
