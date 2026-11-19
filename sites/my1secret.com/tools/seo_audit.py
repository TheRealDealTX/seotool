#!/usr/bin/env python3
"""SEO audit of every URL in /sitemap.xml:  python3 tools/seo_audit.py http://127.0.0.1:8080"""
import json, re, sys, urllib.request, urllib.error, html as H
from collections import Counter
base = sys.argv[1].rstrip('/')
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'm1s-audit'}), timeout=30); return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''
_, sm = get(base + '/sitemap.xml')
canon_base = re.search(r'<loc>(https?://[^/]+)', sm).group(1)
urls = [u.replace(canon_base, base) for u in re.findall(r'<loc>([^<]+)</loc>', sm) if '/media/' not in u]
titles, descs, problems, links = Counter(), Counter(), [], set()
for u in urls:
    st, h = get(u)
    if st != 200: problems.append((u, 'status %d' % st)); continue
    t = H.unescape(re.search(r'<title>(.*?)</title>', h, re.S).group(1)); titles[t] += 1
    d = re.search(r'<meta name="description" content="([^"]*)"', h); d = H.unescape(d.group(1)) if d else ''; descs[d] += 1
    if not (20 <= len(t) <= 60): problems.append((u, 'title length %d: %s' % (len(t), t)))
    if not (70 <= len(d) <= 145): problems.append((u, 'desc length %d' % len(d)))
    if h.count('<h1') != 1: problems.append((u, 'h1 count %d' % h.count('<h1')))
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if not c or c.group(1).replace(canon_base, base) != u: problems.append((u, 'canonical %s' % (c and c.group(1))))
    if 'noindex' in h: problems.append((u, 'noindex page in sitemap'))
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(j)
        except Exception as e: problems.append((u, 'bad json-ld %s' % e))
    for img in re.findall(r'<img [^>]*>', h):
        if 'alt=' not in img: problems.append((u, 'img without alt'))
    links.update(l for l in re.findall(r'href="(/[^"#?]*)', h) if not l.startswith('//'))
for t, n in titles.items():
    if n > 1: problems.append(('-', 'duplicate title x%d: %s' % (n, t)))
for d, n in descs.items():
    if n > 1: problems.append(('-', 'duplicate desc x%d: %s' % (n, d[:60])))
for l in sorted(links):
    if l.startswith(('/logout', '/vote', '/comment', '/thread/')): continue
    st, _ = get(base + l)
    if st not in (200,): problems.append((l, 'internal link status %d' % st))
print('urls=%d internal_links=%d problems=%d' % (len(urls), len(links), len(problems)))
for p in problems: print('  ', *p)
