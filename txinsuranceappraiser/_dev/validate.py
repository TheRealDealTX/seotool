#!/usr/bin/env python3
"""Post-build checks. Run the dev server first:
   php -S 127.0.0.1:8090 _dev/router.php     then   python3 _dev/validate.py
"""
import re, json, sys, os, urllib.request, urllib.error, html, collections
BASE = os.environ.get('BASE', 'http://127.0.0.1:8090')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedir)
def get(path):
    try:
        r = op.open(BASE + path); return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), e.headers
errors = []
def err(m): errors.append(m)

# 1. every legacy URL must resolve (200, or 301 to a 200)
legacy = [u.strip().replace('https://txinsuranceappraiser.com', '') for u in open(os.path.join(ROOT, '_dev/legacy-urls.txt')) if u.strip()]
for p in legacy:
    s, b, h = get(p)
    if s in (301, 302):
        to = h['Location'].replace('https://txinsuranceappraiser.com', '')
        s2, _, _ = get(to)
        if s2 != 200: err(f'legacy {p} -> {to} -> {s2}')
    elif s != 200: err(f'legacy {p} -> {s}')
print('legacy URLs checked:', len(legacy))

# 2. crawl sitemap pages
s, sm, _ = get('/sitemap.xml')
pages = [u.replace('https://txinsuranceappraiser.com', '') for u in re.findall(r'<loc>([^<]+)</loc>', sm) if '/assets/' not in u]
print('sitemap pages:', len(pages))
titles, descs = collections.defaultdict(list), collections.defaultdict(list)
links, assets = set(), set()
brand_home = 0
for p in pages:
    s, b, _ = get(p)
    if s != 200: err(f'{p} status {s}'); continue
    if re.search(r'(Fatal error|Warning:|Notice:|Deprecated:|Parse error)', b): err(f'{p} PHP error')
    t = re.search(r'<title>(.*?)</title>', b, re.S); t = html.unescape(t.group(1)) if t else ''
    dsc = re.search(r'<meta name="description" content="([^"]*)"', b); dsc = html.unescape(dsc.group(1)) if dsc else ''
    titles[t].append(p); descs[dsc].append(p)
    if not t or len(t) > 70: err(f'{p} title length {len(t)}: {t}')
    if not (70 <= len(dsc) <= 145): err(f'{p} description length {len(dsc)}')
    h1 = re.findall(r'<h1[ >]', b)
    if len(h1) != 1: err(f'{p} has {len(h1)} h1')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S):
        try: json.loads(j)
        except Exception as e: err(f'{p} bad JSON-LD {e}')
    if f'<link rel="canonical" href="https://txinsuranceappraiser.com{p}">' not in b: err(f'{p} canonical mismatch')
    for img in re.findall(r'<img [^>]*>', b):
        if 'alt="' not in img or 'alt=""' in img: err(f'{p} img missing alt')
    for a in re.findall(r'href="(/[^"#?]*)', b): links.add(a)
    for a in re.findall(r'(?:src|href)="(/assets/[^"?]+)', b): assets.add(a)
    for a in re.findall(r'url\((/assets/[^)]+)\)', b): assets.add(a)
    if p == '/':
        m = re.search(r'<main id="main">(.*)</main>', b, re.S).group(1)
        txt = html.unescape(re.sub('<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', m, flags=re.S)))
        brand_home = len(re.findall('TX Insurance Appraiser', txt))
for t, ps in titles.items():
    if len(ps) > 1: err(f'duplicate title "{t}": {ps[:3]}')
for t, ps in descs.items():
    if len(ps) > 1: err(f'duplicate description: {ps[:3]}')
for l in sorted(links):
    if l.startswith('/assets/') or l in ('/favicon.ico', '/apple-touch-icon.png'): continue
    s, _, _ = get(l)
    if s != 200: err(f'internal link {l} -> {s}')
for a in sorted(assets):
    if not os.path.exists(ROOT + a): err(f'missing asset {a}')
print('internal links:', len(links), 'assets:', len(assets))
print('homepage "TX Insurance Appraiser" mentions in <main>:', brand_home)
if brand_home < 14: err('homepage brand mentions < 14')
print('\n'.join(errors[:80]) if errors else 'ALL CHECKS PASSED')
print('errors:', len(errors))
sys.exit(1 if errors else 0)
