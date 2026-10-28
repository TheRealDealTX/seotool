#!/usr/bin/env python3
"""Crawl the local preview (php -S ... .dev/router.php) and check the build.

Checks: every page in the XML sitemaps + every legacy WordPress URL returns 200,
one <h1>, unique <title>/<meta description> with sane lengths, canonical matches
URL, valid JSON-LD, every internal link and asset resolves, every image has alt,
legacy blog heading anchors still exist, and the homepage says "Austin Roofing"
at least 14 times.

Usage: python3 .dev/validate.py [base_url]
"""
import json
import re
import sys
import urllib.request
import urllib.error
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080').rstrip('/')
ORIGIN = 'https://austinsroofing.com'

# Every URL the old WordPress site exposed (sitemaps + Search Console pages).
LEGACY = [
    '/', '/about-us/', '/services/', '/faqs/', '/sitemap/', '/privacy-policy/', '/terms-of-service/',
    '/contact-us/', '/blog/', '/category/general/',
    '/blog/what-is-a-square-in-roofing/', '/blog/residential-metal-roofing-lifespan/',
    '/blog/roof-replacement-permit-requirements/', '/blog/cost-of-asphalt-shingles-per-square/',
    '/blog/architectural-shingle-vs-asphalt-shingles/', '/blog/attic-ventilation-upgrade-benefits/',
    '/blog/ice-and-water-shield-installation-cost/', '/blog/roofing-underlayment-material-types/',
    '/blog/insurance-coverage-for-storm-damaged-roofs/',
    '/blog/residential-roofing-warranty-coverage-guide-for-homeowners/',
    '/blog/how-much-does-it-cost-to-replace-a-roof/',
    '/sitemap_index.xml', '/sitemap.xml', '/post-sitemap.xml', '/page-sitemap.xml', '/category-sitemap.xml',
    '/robots.txt', '/favicon.ico',
    '/wp-content/uploads/2026/01/Roofing-Underlayment-Material-Types-A-Complete-Guide.webp',
    '/wp-content/uploads/2025/11/Austin-Roofing-Logo.webp',
    '/wp-content/uploads/2025/12/Austin-Roofing-Site-Image.webp',
]
LEGACY_ANCHORS = {
    '/services/': ['Roof-Restoration', 'Wind-Damage-Repair', 'Hail-Damage-Repair', 'Commercial-Roof-Repair',
                   'Commercial-Roof-Replacement', 'Commercial-Roof-Types', 'Commercial-Roof-Coatings',
                   'Multifamily-Roofing'],
}

errors, warnings = [], []


def fetch(path):
    url = path if path.startswith('http') else BASE + path
    req = urllib.request.Request(url, headers={'User-Agent': 'validate'})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.title = ''
        self._in_title = False
        self.meta = {}
        self.canonical = None
        self.links, self.assets, self.ids = set(), set(), set()
        self.noalt = []
        self.ld = []
        self._in_ld = False
        self._buf = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'h1':
            self.h1 += 1
        elif tag == 'title':
            self._in_title = True
        elif tag == 'meta' and a.get('name') in ('description', 'robots'):
            self.meta[a['name']] = a.get('content', '')
        elif tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href')
        elif tag == 'link' and a.get('href') and a.get('rel') in ('stylesheet', 'icon', 'apple-touch-icon', 'manifest', 'preload'):
            self.assets.add(a['href'])
        elif tag == 'a' and a.get('href'):
            self.links.add(a['href'])
        elif tag in ('img', 'script') and a.get('src'):
            self.assets.add(a['src'])
            if tag == 'img' and not a.get('alt'):
                self.noalt.append(a['src'])
        elif tag == 'script' and a.get('type') == 'application/ld+json':
            self._in_ld, self._buf = True, ''

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        if tag == 'script' and self._in_ld:
            self.ld.append(self._buf)
            self._in_ld = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if self._in_ld:
            self._buf += d


def local(href, page_path):
    u = urlparse(urljoin(ORIGIN + page_path, href))
    if u.scheme not in ('http', 'https') or u.netloc != urlparse(ORIGIN).netloc:
        return None, None
    return u.path, u.fragment


def main():
    pages = set()
    for sm in ('/page-sitemap.xml', '/post-sitemap.xml', '/category-sitemap.xml'):
        st, xml = fetch(sm)
        if st != 200:
            errors.append(f'{sm} -> {st}')
        pages |= {urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', xml)}
    for p in LEGACY:
        st, _ = fetch(p)
        if st != 200:
            errors.append(f'LEGACY {p} -> {st}')

    titles, descs, checked, ids_by_page = {}, {}, {}, {}
    links_to_check = {}
    for path in sorted(pages):
        st, html = fetch(path)
        if st != 200:
            errors.append(f'{path} -> {st}')
            continue
        if re.search(r'<b>(Warning|Fatal error|Notice|Deprecated)</b>', html):
            errors.append(f'{path}: PHP error output')
        pg = Page()
        pg.feed(html)
        ids_by_page[path] = pg.ids
        if pg.h1 != 1:
            errors.append(f'{path}: {pg.h1} <h1>')
        t, d = unescape(pg.title.strip()), unescape(pg.meta.get('description', ''))
        titles.setdefault(t, []).append(path)
        descs.setdefault(d, []).append(path)
        if not 25 <= len(t) <= 70:
            warnings.append(f'{path}: title length {len(t)}: {t}')
        if not 110 <= len(d) <= 165:
            warnings.append(f'{path}: description length {len(d)}')
        if pg.canonical != ORIGIN + path:
            errors.append(f'{path}: canonical {pg.canonical}')
        if 'noindex' in pg.meta.get('robots', ''):
            errors.append(f'{path}: noindex but in sitemap')
        for raw in pg.ld:
            try:
                json.loads(raw)
            except ValueError as e:
                errors.append(f'{path}: bad JSON-LD {e}')
        for src in pg.noalt:
            errors.append(f'{path}: img without alt {src}')
        for href in pg.links | pg.assets:
            lp, frag = local(href, path)
            if lp is None:
                continue
            links_to_check.setdefault(lp, set()).add(path)
            if frag:
                links_to_check.setdefault(lp + '#' + frag, set()).add(path)
        if path == '/':
            body = html.split('<main id="main">')[1].split('</main>')[0]
            text = unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', body, flags=re.S)))
            n = len(re.findall(r'austin roofing', text, re.I))
            print(f'Homepage "Austin Roofing" mentions in main content: {n}')
            if n < 14:
                errors.append(f'homepage has only {n} "Austin Roofing" mentions')

    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f'duplicate title {t!r}: {ps}')
    for d, ps in descs.items():
        if len(ps) > 1:
            errors.append(f'duplicate description: {ps}')

    for target, srcs in sorted(links_to_check.items()):
        path, _, frag = target.partition('#')
        if frag:
            if path in ids_by_page and frag not in ids_by_page[path]:
                errors.append(f'missing anchor {target} (linked from {sorted(srcs)[:3]})')
            continue
        if path not in checked:
            checked[path] = fetch(path)[0]
        if checked[path] != 200:
            errors.append(f'broken link {path} -> {checked[path]} (from {sorted(srcs)[:3]})')

    for path, anchors in LEGACY_ANCHORS.items():
        for a in anchors:
            if a not in ids_by_page.get(path, set()):
                errors.append(f'{path}: legacy anchor #{a} missing')
    # Blog heading anchors from the WordPress posts
    try:
        cur = None
        for line in open(__file__.rsplit('/', 1)[0] + '/legacy-blog-anchors.txt'):
            line = line.strip()
            if line.startswith('== blog_'):
                cur = '/blog/' + line[8:].replace('.html', '') + '/'
            elif line and cur and line not in ids_by_page.get(cur, set()):
                errors.append(f'{cur}: legacy anchor #{line} missing')
    except FileNotFoundError:
        pass

    print(f'Pages checked: {len(pages)}, links/assets checked: {len(checked)}')
    for w in warnings:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print('OK' if not errors else f'{len(errors)} errors')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
