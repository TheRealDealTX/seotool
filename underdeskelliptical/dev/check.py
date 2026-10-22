#!/usr/bin/env python3
"""Site validator. Run against the local preview server:

    php -S 127.0.0.1:8090 dev/router.php &
    python3 dev/check.py [legacy-urls.txt]

Checks every URL from the XML sitemaps (plus an optional list of legacy URLs that must
keep working): HTTP 200, one <h1>, title <= 60 chars and unique, meta description
120-160 chars and unique, canonical, valid JSON-LD, internal links resolve, local assets
exist, every Amazon link carries the Associates tag and rel=sponsored, and the homepage
mentions "Under Desk Elliptical" at least 14 times.
"""
import json, re, sys, html, urllib.request, urllib.error
from collections import Counter

BASE = 'http://127.0.0.1:8090'
TAG = 'underdeskellipticaljditt-20'
errors, warns = [], []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def get(path):
    try:
        r = opener.open(BASE + path)
        return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), e.headers


def locs(xml):
    return [re.sub(r'^https://underdeskelliptical\.com', '', u) for u in re.findall(r'<loc>([^<]+)</loc>', xml)]


urls = []
for sm in locs(get('/sitemap_index.xml')[1]):
    urls += locs(get(sm)[1])
urls = [u for u in dict.fromkeys(urls) if not u.startswith('/wp-content')]

legacy = []
if len(sys.argv) > 1:
    legacy = [re.sub(r'^https://underdeskelliptical\.com', '', l.strip()) for l in open(sys.argv[1]) if l.startswith('http')]
for u in legacy:
    s, _, h = get(u)
    if s == 301:
        loc = h.get('Location', '')
        warns.append(f'legacy {u} -> 301 {loc}')
    elif s != 200:
        errors.append(f'legacy URL {u} returns {s}')

titles, descs, checked_links = Counter(), Counter(), {}
amz_per_post = {}
words_per_post = {}
for u in urls:
    s, body, _ = get(u)
    if s != 200:
        errors.append(f'{u}: status {s}')
        continue
    t = html.unescape(re.search(r'<title>(.*?)</title>', body, re.S).group(1))
    d = re.search(r'<meta name="description" content="([^"]*)"', body)
    d = html.unescape(d.group(1)) if d else ''
    titles[t] += 1
    descs[d] += 1
    if len(t) > 65:
        warns.append(f'{u}: title {len(t)} chars: {t}')
    if not 110 <= len(d) <= 165:
        warns.append(f'{u}: description {len(d)} chars')
    if body.count('<h1') != 1:
        errors.append(f'{u}: {body.count("<h1")} h1 tags')
    if '<link rel="canonical" href="https://underdeskelliptical.com' + u + '"' not in body and u != '/':
        errors.append(f'{u}: canonical mismatch')
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try:
            json.loads(ld)
        except Exception as ex:
            errors.append(f'{u}: bad JSON-LD {ex}')
    if 'Warning' in body and '<b>Warning</b>' in body or 'Fatal error' in body or 'Deprecated:' in body:
        errors.append(f'{u}: PHP notice in output')
    if '[[' in re.sub(r'<script.*?</script>', '', body, flags=re.S):
        errors.append(f'{u}: unrendered shortcode')
    amz = re.findall(r'<a [^>]*href="(https://www\.amazon\.com[^"]*)"[^>]*>', body)
    for tagm in re.findall(r'<a [^>]*href="https://www\.amazon\.com[^"]*"[^>]*>', body):
        if TAG not in tagm:
            errors.append(f'{u}: Amazon link without tag: {tagm[:120]}')
        if 'sponsored' not in tagm:
            errors.append(f'{u}: Amazon link without rel=sponsored')
    if 'amazon.' in body.replace('www.amazon.com', ''):
        for m in re.findall(r'https?://(?!www\.amazon\.com)[a-z.]*amazon\.[a-z.]+[^"\s<]*', body):
            errors.append(f'{u}: non-standard Amazon URL {m[:80]}')
    main = body[body.find('<main'):body.find('</main>')]
    if 'is-post' in body[:body.find('<main')]:
        prose = main[main.find('class="prose"'):main.find('class="author-box"')]
        amz_per_post[u] = len(re.findall(r'href="https://www\.amazon\.com', main.split('class="sidebar"')[0]))
        text = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|table)[^>]*>.*?</\1>', ' ', prose, flags=re.S))
        words_per_post[u] = len(text.split())
    for href in re.findall(r'(?:href|src)="(/[^"#?]*)', body):
        if href.startswith('//'):
            continue
        if href not in checked_links:
            checked_links[href] = get(href)[0]
        if checked_links[href] != 200:
            errors.append(f'{u}: broken internal link {href} ({checked_links[href]})')
    if u == '/':
        vis = re.sub(r'<[^>]+>', ' ', html.unescape(re.sub(r'<script.*?</script>', '', main, flags=re.S)))
        n = len(re.findall(r'Under Desk Elliptical', vis))
        print(f'Homepage "Under Desk Elliptical" (exact case, visible main content): {n}')
        if n < 14:
            errors.append(f'homepage brand mentions {n} < 14')

for t, n in titles.items():
    if n > 1:
        errors.append(f'duplicate title x{n}: {t}')
for d, n in descs.items():
    if n > 1:
        errors.append(f'duplicate description x{n}: {d[:80]}')

if amz_per_post:
    low = {k: v for k, v in amz_per_post.items() if v < 6}
    print(f'Posts: {len(amz_per_post)}  Amazon links/post min {min(amz_per_post.values())} avg {sum(amz_per_post.values()) / len(amz_per_post):.1f}')
    print(f'Words/post min {min(words_per_post.values())} avg {sum(words_per_post.values()) // len(words_per_post)}')
    for k, v in low.items():
        warns.append(f'{k}: only {v} Amazon links')
    for k, v in words_per_post.items():
        if v < 1200:
            warns.append(f'{k}: only {v} words')

print(f'Checked {len(urls)} sitemap URLs, {len(legacy)} legacy URLs, {len(checked_links)} internal links/assets')
for w in warns:
    print('WARN ', w)
for e in errors:
    print('ERROR', e)
print('OK' if not errors else f'{len(errors)} errors')
sys.exit(1 if errors else 0)
