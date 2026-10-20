"""Post-build checks against a running copy of the site.

    php -S 127.0.0.1:8099 index.php &      # from the site root
    python3 _build/validate.py http://127.0.0.1:8099 [old-url-list.txt ...]

1. Every URL in the given lists (the old site's sitemap, Search Console pages and
   image URLs) must end in a 200, directly or through one redirect.
2. Crawls every page linked from the site and fails on any internal link or
   image that does not resolve, on missing titles/descriptions/canonicals,
   on pages with other than exactly one <h1>, and on invalid JSON-LD.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import quote, urljoin, urlparse

BASE = sys.argv[1].rstrip('/')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)


def fetch(path):
    try:
        r = opener.open(BASE + quote(path, safe='/?=&%:'), timeout=30)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def resolve(path, hops=0):
    code, headers, body = fetch(path)
    if code in (301, 302) and hops < 3:
        loc = headers['Location']
        return resolve(urlparse(urljoin(BASE + path, loc)).path + (('?' + urlparse(loc).query) if urlparse(loc).query else ''), hops + 1)
    return code, path, hops, body


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.imgs, self.h1, self.ld, self._ld, self.meta = set(), set(), 0, [], None, {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'a' and a.get('href'):
            self.links.add(a['href'])
        if tag == 'img' and a.get('src'):
            self.imgs.add(a['src'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self._ld = ''
        if tag == 'meta' and a.get('name') in ('description', 'robots'):
            self.meta[a['name']] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical':
            self.meta['canonical'] = a.get('href')

    def handle_data(self, data):
        if self._ld is not None:
            self._ld += data

    def handle_endtag(self, tag):
        if tag == 'script' and self._ld is not None:
            self.ld.append(self._ld)
            self._ld = None


errors = []

for listfile in sys.argv[2:]:
    for line in open(listfile):
        url = line.strip()
        if not url:
            continue
        p = urlparse(url)
        path = p.path + ('?' + p.query if p.query else '')
        code, final, hops, _ = resolve(path)
        if code != 200:
            errors.append(f'OLD URL {url} -> {final} [{code}]')

seen, queue, assets = set(), ['/'], set()
while queue:
    path = queue.pop()
    if path in seen:
        continue
    seen.add(path)
    code, final, hops, body = resolve(path)
    if code != 200:
        errors.append(f'LINK {path} -> {final} [{code}]')
        continue
    if hops:
        errors.append(f'LINK {path} redirects to {final} (link to the final URL)')
    if not final.endswith('/') or final.startswith('/wp-content/'):
        continue
    page = Page()
    page.feed(body.decode('utf-8', 'replace'))
    if page.h1 != 1:
        errors.append(f'{final}: {page.h1} <h1> elements')
    if not page.meta.get('description'):
        errors.append(f'{final}: no meta description')
    if not page.meta.get('canonical'):
        errors.append(f'{final}: no canonical')
    for blob in page.ld:
        try:
            json.loads(blob)
        except ValueError as e:
            errors.append(f'{final}: bad JSON-LD {e}')
    for href in page.links:
        u = urlparse(urljoin(BASE + final, href))
        if u.netloc == urlparse(BASE).netloc and not u.path.startswith('/feed'):
            queue.append(u.path + ('?' + u.query if u.query else ''))
    for src in page.imgs:
        u = urlparse(urljoin(BASE + final, src))
        if u.netloc == urlparse(BASE).netloc:
            assets.add(u.path)

for a in sorted(assets):
    code, *_ = fetch(a)
    if code != 200:
        errors.append(f'IMG {a} [{code}]')

print(f'crawled {len(seen)} URLs, {len(assets)} images')
for e in errors:
    print('ERROR', e)
sys.exit(1 if errors else 0)
