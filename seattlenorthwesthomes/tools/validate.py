#!/usr/bin/env python3
"""Crawl the site and check SEO + link health.

    php -S 127.0.0.1:8080 -t public_html public_html/index.php &
    python3 tools/validate.py [base_url]

Checks every URL in sitemap.xml plus every internal link found: HTTP 200,
exactly one <h1>, unique <title> (<= 70 chars warned) and meta description,
canonical present, JSON-LD parses, images/assets load, internal links resolve,
and every legacy WordPress URL 301s to a live page.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080').rstrip('/')
ROOT = __file__.rsplit('/tools/', 1)[0]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


opener = urllib.request.build_opener(NoRedirect)
cache = {}


def fetch(path):
    if path in cache:
        return cache[path]
    try:
        r = opener.open(BASE + path, timeout=30)
        res = (r.status, r.headers.get('Location'), r.read().decode('utf-8', 'replace'))
    except urllib.error.HTTPError as e:
        res = (e.code, e.headers.get('Location'), e.read().decode('utf-8', 'replace'))
    cache[path] = res
    return res


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ''
        self._t = False
        self.desc = None
        self.canon = None
        self.links, self.assets, self.ld = set(), set(), []
        self._ld = None
        self.noindex = False
        self.img_no_alt = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'h1':
            self.h1 += 1
        elif tag == 'title':
            self._t = True
        elif tag == 'meta' and a.get('name') == 'description':
            self.desc = a.get('content')
        elif tag == 'meta' and a.get('name') == 'robots' and 'noindex' in (a.get('content') or ''):
            self.noindex = True
        elif tag == 'link' and a.get('rel') == 'canonical':
            self.canon = a.get('href')
        elif tag == 'a' and a.get('href'):
            self.links.add(a['href'])
        elif tag == 'img':
            self.assets.add(a.get('src', ''))
            if a.get('alt') is None:
                self.img_no_alt += 1
        elif tag in ('script', 'link') and (a.get('src') or (tag == 'link' and a.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon', 'manifest'))):
            self.assets.add(a.get('src') or a.get('href'))
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self._ld = ''

    def handle_endtag(self, tag):
        if tag == 'title':
            self._t = False
        if tag == 'script' and self._ld is not None:
            self.ld.append(self._ld)
            self._ld = None

    def handle_data(self, d):
        if self._t:
            self.title += d
        if self._ld is not None:
            self._ld += d


def local(href, page):
    u = urlparse(urljoin(BASE + page, href))
    if u.scheme not in ('http', 'https') or u.netloc not in (urlparse(BASE).netloc, 'seattlenorthwesthomes.com'):
        return None
    return u.path + ('?' + u.query if u.query else '')


def main():
    errors, warns = [], []
    status, _, sm = fetch('/sitemap.xml')
    assert status == 200, 'sitemap missing'
    queue = [urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
    seen, titles, descs, assets = set(), {}, {}, set()
    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        seen.add(path)
        st, loc, body = fetch(path)
        if st in (301, 302, 303):
            tgt = urlparse(loc).path
            if fetch(tgt)[0] != 200:
                errors.append(f'{path}: redirects to broken {tgt}')
            continue
        if st != 200:
            errors.append(f'{path}: HTTP {st}')
            continue
        if '<html' not in body[:200]:
            continue
        p = Page()
        p.feed(body)
        if p.h1 != 1:
            errors.append(f'{path}: {p.h1} <h1> tags')
        if not p.desc:
            errors.append(f'{path}: no meta description')
        if not p.canon:
            errors.append(f'{path}: no canonical')
        if p.img_no_alt:
            errors.append(f'{path}: {p.img_no_alt} images without alt')
        for ld in p.ld:
            try:
                json.loads(ld)
            except ValueError as e:
                errors.append(f'{path}: bad JSON-LD {e}')
        if not p.noindex and '?' not in path:
            t = p.title.strip()
            if len(t) > 75:
                warns.append(f'{path}: title {len(t)} chars')
            if p.desc and not 50 <= len(p.desc) <= 165:
                warns.append(f'{path}: description {len(p.desc)} chars')
            titles.setdefault(t, []).append(path)
            descs.setdefault(p.desc, []).append(path)
        if re.search(r'\brealtor\b', re.sub(r'<[^>]+>', ' ', body), re.I):
            warns.append(f'{path}: uses the word "Realtor"')
        for h in p.links:
            lp = local(h, path)
            if lp and lp not in seen and not lp.startswith('/submit'):
                queue.append(lp)
        for a in p.assets:
            ap = local(a, path)
            if ap:
                assets.add(ap)
    for a in sorted(assets):
        if fetch(a.split('?')[0])[0] != 200:
            errors.append(f'missing asset {a}')
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f'duplicate title "{t}": {ps}')
    for d, ps in descs.items():
        if len(ps) > 1:
            errors.append(f'duplicate description: {ps}')
    # legacy URLs
    legacy = [l.split('\t')[0] for l in open(ROOT + '/tools/slugmap.tsv')]
    legacy = ['/' + s + '/' for s in legacy] + ['/about-us/', '/buying/', '/selling/', '/contact-us/',
              '/category/articles/', '/author/selena/', '/post-sitemap.xml', '/page-sitemap.xml', '/sitemap_index.xml',
              '/wp-content/uploads/2023/07/Seattle-Northwest-Homes-Logo.webp']
    for lp in legacy:
        st, loc, _ = fetch(lp)
        if st == 200 and lp.startswith('/wp-content/'):
            continue
        if st != 301 or fetch(urlparse(loc).path)[0] != 200:
            errors.append(f'legacy {lp}: {st} -> {loc}')
    print(f'pages crawled: {len(seen)}, assets: {len(assets)}, legacy URLs: {len(legacy)}')
    for w in warns:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
