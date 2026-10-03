#!/usr/bin/env python3
"""Crawl the local site and check SEO + links.

Usage: python3 tools/test/crawl.py [base]   (default http://127.0.0.1:8081)
Checks every URL in sitemap.xml plus every internal link found:
  status codes, one <h1>, unique <title>/description, description length, canonical,
  JSON-LD parses, images exist + have alt, internal links resolve, no PHP warnings,
  no internal-only email on any page, keyword count on the homepage.
"""
import json, re, sys, html
from collections import Counter, defaultdict
from urllib.parse import urljoin, urlparse
import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8081'
PROD = 'https://mcallenpublicadjuster.com'
s = requests.Session()
problems = []
def bad(url, msg): problems.append(f'{url}: {msg}')

sm = s.get(BASE + '/sitemap.xml').text
urls = [u.replace(PROD, '') for u in re.findall(r'<loc>([^<]+)</loc>', sm) if '/wp-content/' not in u and u.startswith(PROD)]
urls = [u for u in urls if not u.endswith('.webp')]
queue = list(dict.fromkeys(urls))
seen, titles, descs, link_targets, statuses = set(), defaultdict(list), defaultdict(list), set(), {}
pages = {}
while queue:
    path = queue.pop(0)
    if path in seen:
        continue
    seen.add(path)
    r = s.get(BASE + path, allow_redirects=False)
    statuses[path] = r.status_code
    if r.status_code != 200:
        bad(path, f'status {r.status_code}')
        continue
    if 'text/html' not in r.headers.get('content-type', ''):
        continue
    t = r.text
    pages[path] = t
    if re.search(r'(Warning|Fatal error|Notice|Deprecated):', t):
        bad(path, 'PHP warning in output')
    if 'jditt@' in t or 'risepublicadjusting.com' in t.replace('Rise Public Adjusting', ''):
        bad(path, 'internal email exposed')
    h1 = re.findall(r'<h1[\s>]', t)
    if len(h1) != 1:
        bad(path, f'{len(h1)} h1 tags')
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = html.unescape(m.group(1)) if m else ''
    titles[title].append(path)
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = html.unescape(m.group(1)) if m else ''
    descs[desc].append(path)
    noindex = 'noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', t) or [None, ''])[1]
    if not desc:
        bad(path, 'missing meta description')
    elif len(desc) > 160:
        bad(path, f'description {len(desc)} chars')
    if len(title) > 70:
        bad(path, f'title {len(title)} chars: {title}')
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not can or can.group(1) != PROD + path.split('?')[0]:
        bad(path, f'canonical {can.group(1) if can else None}')
    if noindex and path in urls:
        bad(path, 'noindex page listed in sitemap')
    for js in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(js)
        except Exception as e:
            bad(path, f'bad JSON-LD {e}')
    for tag in re.findall(r'<img\b[^>]*>', t):
        src = re.search(r'src="([^"]+)"', tag)
        if not re.search(r'\salt="', tag):
            bad(path, f'img without alt {tag[:80]}')
        if src and src.group(1).startswith('/'):
            link_targets.add(src.group(1))
    for href in re.findall(r'href="([^"#]+)', t):
        href = html.unescape(href)
        if href.startswith(PROD):
            href = href[len(PROD):] or '/'
        if href.startswith('/') and not href.startswith('//'):
            p = urlparse(href).path
            link_targets.add(p)
            if not re.search(r'\.(css|js|png|webp|ico|svg|xml|php|webmanifest|txt|woff2)$', p) and p not in seen and p not in queue and '?' not in href:
                queue.append(p)

for target in sorted(link_targets):
    if target in statuses:
        continue
    r = s.get(BASE + target, allow_redirects=False)
    statuses[target] = r.status_code
    if r.status_code not in (200,):
        bad(target, f'linked resource returns {r.status_code}')

for title, ps in titles.items():
    if len(ps) > 1:
        bad(','.join(ps), f'duplicate title "{title}"')
for d, ps in descs.items():
    if len(ps) > 1 and d:
        bad(','.join(ps), 'duplicate description')

home = re.sub(r'<script.*?</script>', '', pages.get('/', ''), flags=re.S)
home_text = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<head>.*?</head>', '', home, flags=re.S)))
kw = len(re.findall(r'McAllen Public Adjuster', home_text))
print(f'Crawled {len(pages)} HTML pages; checked {len(link_targets)} internal link targets.')
print(f'Homepage visible-text count of "McAllen Public Adjuster": {kw}')
if kw < 8:
    bad('/', f'keyword appears only {kw} times')
print('\n'.join(problems) if problems else 'No problems found.')
sys.exit(1 if problems else 0)
