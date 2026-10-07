"""Requests every URL from the Semrush exports (ranking pages + backlink targets)
against a running server and checks each one ends at a 200 within two redirects.

    python3 scripts/check_urls.py http://127.0.0.1:8080
"""
import collections
import csv
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

base = sys.argv[1].rstrip('/')
SEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'seo-data')
strip = lambda u: re.sub(r'^https?://(www\.)?gaparboristsupply\.com', '', u) or '/'

urls = collections.OrderedDict()
for r in csv.DictReader(open(os.path.join(SEO, 'organic-positions-2026-06.csv'), encoding='utf-8-sig')):
    urls[strip(r['URL'])] = 'organic'
for r in csv.DictReader(open(os.path.join(SEO, 'backlinks-2026-10.csv'), encoding='utf-8-sig')):
    urls.setdefault(strip(r['Target url']), 'backlink')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def hit(u):
    try:
        return opener.open(base + u).status, None
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Location')


bad = 0
stats = collections.Counter()
for u, src in urls.items():
    cur = urllib.parse.quote(u, safe='/?=&%:+*,')
    chain = []
    for _ in range(4):
        code, loc = hit(cur)
        chain.append((code, cur))
        if code in (301, 302) and loc:
            s = urllib.parse.urlsplit(loc)
            cur = s.path + ('?' + s.query if s.query else '')
            continue
        break
    stats[f'{chain[0][0]}->{chain[-1][0]}'] += 1
    if chain[-1][0] != 200 or len(chain) > 3:
        bad += 1
        print('BAD', src, u, chain)
print(dict(stats))
print('checked', len(urls), 'bad', bad)
sys.exit(1 if bad else 0)
