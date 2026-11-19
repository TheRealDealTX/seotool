#!/usr/bin/env python3
"""Migration QA against a running copy of the site (default: local dev server).

  php -S localhost:8080 -t public tools/dev-router.php &
  python3 tools/validate.py [base-url]

Checks: every old sitemap URL and every URL Google reported (GSC export) resolves
to a 200 page (directly or via one 301); every #h- anchor Google shows still exists;
every old image URL still returns 200; unique titles/descriptions; one H1; valid JSON-LD;
no broken internal links or images; affiliate links carry the tag.
"""
import json, re, sys, os, urllib.request, urllib.error, urllib.parse, html
from collections import defaultdict
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080').rstrip('/')
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
LIVE = BASE if BASE.startswith('https://') else 'https://thoughtchangerblog.com'

class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedir)

def get(path):
    url = BASE + path
    try:
        r = op.open(urllib.request.Request(url, headers={'User-Agent': 'tc-validate'}), timeout=30)
        return r.status, r.headers.get('Location'), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Location'), e.read().decode('utf-8', 'replace')

def to_path(u):
    p = urllib.parse.urlsplit(u.replace('https://thoughtchangerblog.com', ''))
    return urllib.parse.quote(p.path, safe="/%:@*_-.~♍") + ('?' + p.query if p.query else '')

errors, warns = [], []
cache = {}
def resolve(path):
    key = path
    if key in cache: return cache[key]
    st, loc, body = get(path)
    hops = 0
    while st in (301, 302, 308) and hops < 3:
        hops += 1
        path = loc.replace(LIVE, '') if loc else '/'
        st, loc, body = get(path)
    cache[key] = (st, hops, path, body)
    return cache[key]

# 1. URLs
gsc = json.load(open(os.path.join(D, 'gsc-pages.json')))
urls = set(open(os.path.join(D, 'wp-sitemap-urls.txt')).read().split()) | {r[0] for r in gsc}
anchors = defaultdict(set)
for u in urls:
    base, _, frag = u.partition('#')
    if frag: anchors[base].add(frag)
checked = 0
slug_status = {p['slug']: p['status'] for p in json.load(open(os.path.join(os.path.dirname(D), '..', 'public/content/posts.json')))}
for u in sorted({u.partition('#')[0] for u in urls}):
    st, hops, final, body = resolve(to_path(u))
    checked += 1
    if st != 200: errors.append(f'URL {u} -> {st} (final {final})')
    elif hops > 1: warns.append(f'URL {u} took {hops} redirects')
    for a in anchors.get(u, ()):
        if f'id="{a}"' not in body:
            (warns if slug_status.get(final.strip('/')) == 'rewritten' else errors).append(f'ANCHOR missing {u}#{a}')
print(f'checked {checked} legacy URLs, {sum(len(v) for v in anchors.values())} anchors')

# 2. Old image URLs
imgs = open(os.path.join(D, 'wp-image-urls.txt')).read().split()
bad = [i for i in imgs if get(to_path(i.replace('http://', 'https://')))[0] != 200]
print(f'checked {len(imgs)} image URLs, {len(bad)} missing')
errors += [f'IMG {b}' for b in bad[:20]]

# 3. Pages in the new sitemap
st, _, sm = get('/sitemap_index.xml')
locs = []
for s in re.findall(r'<loc>([^<]+)</loc>', sm):
    locs += re.findall(r'<loc>([^<]+)</loc>', get(s.replace(LIVE, ''))[2])
titles, descs = defaultdict(list), defaultdict(list)
internal = set()
for u in locs:
    if u.endswith(('.webp', '.png', '.jpg')): continue
    p = u.replace(LIVE, '')
    st, _, body = get(p)
    if st != 200: errors.append(f'SITEMAP {p} -> {st}'); continue
    t = re.search(r'<title>(.*?)</title>', body, re.S); titles[html.unescape(t.group(1))].append(p)
    d = re.search(r'<meta name="description" content="([^"]*)"', body)
    if d: descs[d.group(1)].append(p)
    else: warns.append(f'no description {p}')
    if len(re.findall(r'<h1[\s>]', body)) != 1: errors.append(f'H1 count {p}')
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try: json.loads(ld)
        except Exception as ex: errors.append(f'JSON-LD {p}: {ex}')
    for h in re.findall(r'(?:href|src)="(/[^"#]*)', body): internal.add(html.unescape(h))
    for h in re.findall(r'srcset="([^"]+)"', body):
        for part in h.split(','): internal.add(part.strip().split(' ')[0])
    for a in re.findall(r'href="(https://www\.amazon\.com/[^"]+)"', body):
        if 'tag=thoughtchangerblog-20' not in html.unescape(a): errors.append(f'AMAZON tag missing {p}: {a}')
    ids = re.findall(r'id="([^"]+)"', body)
    for h in re.findall(r'href="#([^"]+)"', body):
        if h not in ids and h != 'top': errors.append(f'in-page anchor #{h} missing on {p}')
for k, v in titles.items():
    if len(v) > 1: errors.append(f'DUP title {k}: {v}')
for k, v in descs.items():
    if len(v) > 1: errors.append(f'DUP description: {v}')
for h in sorted(internal):
    if h.startswith(('/?s=', '//')): continue
    st, hops, final, _ = resolve(urllib.parse.quote(h, safe="/%?=&:@*_-.~"))
    if st != 200: errors.append(f'BROKEN internal {h} -> {st}')
    elif hops: warns.append(f'internal link redirects: {h} -> {final}')
print(f'checked {len(locs)} sitemap pages, {len(internal)} internal links/assets')

for w in warns[:40]: print('WARN', w)
for e in errors: print('ERROR', e)
print(f'{len(errors)} errors, {len(warns)} warnings')
sys.exit(1 if errors else 0)
