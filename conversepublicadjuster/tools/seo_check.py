#!/usr/bin/env python3
"""Static SEO checks for the build. Run from anywhere: python3 -I tools/seo_check.py [--fix-report]
Checks: one <h1> containing "San Antonio" or "<city> Public Adjuster"; <title> <= 65 chars; meta description
<= 158; canonical present and matching the page URL; every JSON-LD block parses; every internal href/src
resolves to a file; sitemap.xml lists exactly the indexable pages.
"""
import os, re, json, sys, html as H
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = 'https://conversepublicadjuster.com'
SKIP_DIRS = {'_old-site', 'tools', '.git', 'wp-content'}
NOINDEX = {'404.html', 'contact/thanks/index.html', 'googlecccfbf2f7e9e5ae4.html'}

def pages():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, '/')

def url_of(rel):
    if rel == 'home.html': return ORIGIN + '/'
    if rel.endswith('/index.html'): return ORIGIN + '/' + rel[:-len('index.html')]
    return ORIGIN + '/' + rel

def resolve(path):
    """Does an internal path resolve to a file in the build (or a server-side endpoint)?"""
    p = path.split('#')[0].split('?')[0]
    if p in ('/contact.php', '/sitemap.xml', '/robots.txt'): return True
    if p == '/': return os.path.isfile(os.path.join(ROOT, 'home.html'))
    fs = os.path.join(ROOT, p.lstrip('/'))
    if p.endswith('/'): return os.path.isfile(os.path.join(fs, 'index.html'))
    return os.path.isfile(fs) or os.path.isfile(os.path.join(fs, 'index.html'))

problems = []
def bad(rel, msg): problems.append((rel, msg))

all_urls = set()
for rel in sorted(pages()):
    if rel in NOINDEX and rel != '404.html' and rel != 'contact/thanks/index.html':
        continue
    t = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    url = url_of(rel)
    indexable = rel not in NOINDEX
    if indexable: all_urls.add(url)
    # h1
    h1s = [re.sub(r'<[^>]+>', '', m).strip() for m in re.findall(r'<h1[^>]*>(.*?)</h1>', t, re.S)]
    if len(h1s) != 1: bad(rel, f'{len(h1s)} <h1> tags')
    elif indexable:
        h = H.unescape(h1s[0])
        if 'San Antonio' not in h and not re.search(r'Public Adjuster', h):
            bad(rel, f'h1 lacks San Antonio / Public Adjuster: {h!r}')
    # title / description
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = H.unescape(m.group(1).strip()) if m else ''
    if not title: bad(rel, 'no <title>')
    elif len(title) > 65: bad(rel, f'title {len(title)} chars: {title!r}')
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = H.unescape(m.group(1)) if m else ''
    if not desc: bad(rel, 'no meta description')
    elif len(desc) > 158: bad(rel, f'description {len(desc)} chars')
    # canonical
    cans = re.findall(r'<link rel="canonical" href="([^"]*)"', t)
    if indexable:
        if len(cans) != 1: bad(rel, f'{len(cans)} canonical tags')
        elif cans[0] != url: bad(rel, f'canonical {cans[0]} != {url}')
    elif cans and cans[0] != url: bad(rel, f'canonical {cans[0]} != {url}')
    if not indexable and 'noindex' not in t: bad(rel, 'should be noindex')
    # JSON-LD
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)):
        try: json.loads(block)
        except Exception as e: bad(rel, f'JSON-LD block {i} invalid: {e}')
    # internal links
    for attr, val in re.findall(r'\b(href|src|action)="(/[^"]*)"', t):
        if not resolve(val): bad(rel, f'broken internal {attr}: {val}')
    for val in re.findall(r'(?:href|src)="(https?://(?:www\.)?conversepublicadjuster\.com[^"]*)"', t):
        if not resolve(val.split('.com', 1)[1] or '/'): bad(rel, f'broken absolute link: {val}')

# sitemap
sm = ET.parse(os.path.join(ROOT, 'sitemap.xml'))
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
sm_urls = [u.text.strip() for u in sm.findall('.//s:loc', ns)]
dups = {u for u in sm_urls if sm_urls.count(u) > 1}
for u in dups: bad('sitemap.xml', f'duplicate {u}')
for u in sorted(all_urls - set(sm_urls)): bad('sitemap.xml', f'missing {u}')
for u in sorted(set(sm_urls) - all_urls): bad('sitemap.xml', f'lists non-page {u}')

npages = len(all_urls)
print(f'checked {npages} indexable pages + noindex pages; sitemap has {len(sm_urls)} urls')
for rel, msg in problems: print(f'{rel}: {msg}')
print(f'{len(problems)} problem(s)')
sys.exit(1 if problems else 0)
