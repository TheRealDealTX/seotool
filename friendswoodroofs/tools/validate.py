#!/usr/bin/env python3
"""Crawl a running copy of the site and check SEO/accessibility basics.

    php -S 127.0.0.1:8080 -t public_html tools/dev-router.php &
    python3 tools/validate.py http://127.0.0.1:8080

Python 3 standard library only. Not deployed.
"""
import json, re, sys, urllib.error, urllib.parse, urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080').rstrip('/')
PROD = 'https://friendswoodroofs.com'
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
problems, notes = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''; self._in_title = False
        self.meta = {}; self.links = []; self.canonical = None
        self.h1 = 0; self.headings = []; self.ids = []; self.imgs = []; self.iframes = []
        self.jsonld = []; self._in_ld = False; self._ld = ''
        self.text = []; self._skip = 0; self.labels_for = set(); self.inputs = []
        self.main_text = []; self._in_main = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'title': self._in_title = True
        elif tag == 'meta':
            k = a.get('name') or a.get('property')
            if k: self.meta[k] = a.get('content', '')
        elif tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        elif tag == 'a' and a.get('href'): self.links.append(a['href'])
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.headings.append(int(tag[1]))
            if tag == 'h1': self.h1 += 1
        elif tag == 'img': self.imgs.append(a)
        elif tag == 'iframe': self.iframes.append(a)
        elif tag == 'script' and a.get('type') == 'application/ld+json': self._in_ld = True; self._ld = ''
        elif tag in ('script', 'style'): self._skip += 1
        elif tag == 'label' and a.get('for'): self.labels_for.add(a['for'])
        elif tag in ('input', 'select', 'textarea') and a.get('type') not in ('hidden', 'submit'): self.inputs.append(a)
        elif tag == 'main': self._in_main = True

    def handle_endtag(self, tag):
        if tag == 'title': self._in_title = False
        elif tag == 'script' and self._in_ld:
            self._in_ld = False; self.jsonld.append(self._ld)
        elif tag in ('script', 'style') and self._skip: self._skip -= 1
        elif tag == 'main': self._in_main = False

    def handle_data(self, d):
        if self._in_title: self.title += d
        elif self._in_ld: self._ld += d
        elif not self._skip:
            self.text.append(d)
            if self._in_main: self.main_text.append(d)


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'fr-validate'})
    try:
        r = urllib.request.urlopen(req)
        return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), e.headers


# Seed from the sitemap so every published URL is checked.
code, xml, _ = fetch('/sitemap.xml')
assert code == 200, 'sitemap.xml not reachable'
urls = [urllib.parse.urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', xml)]
lastmods = dict(zip(urls, re.findall(r'<lastmod>([^<]+)</lastmod>', xml)))
for u in re.findall(r'<loc>([^<]+)</loc>', xml):
    if not u.startswith(PROD + '/'):
        problems.append(f'sitemap URL not on production domain: {u}')

queue = list(urls) + ['/thank-you/', '/this-page-does-not-exist/']
seen, pages = set(), {}
titles, descs = defaultdict(list), defaultdict(list)
link_targets = defaultdict(set)

while queue:
    path = queue.pop(0)
    if path in seen: continue
    seen.add(path)
    code, html, headers = fetch(path)
    if path == '/this-page-does-not-exist/':
        if code != 404: problems.append('unknown URL did not return 404')
        continue
    if code != 200:
        problems.append(f'{path}: HTTP {code}'); continue
    p = Page(); p.feed(html); pages[path] = p
    titles[p.title.strip()].append(path)
    descs[p.meta.get('description', '')].append(path)
    noindex = 'noindex' in p.meta.get('robots', '')

    if p.h1 != 1: problems.append(f'{path}: {p.h1} <h1> elements')
    prev = 0
    for lvl in p.headings:
        if prev and lvl > prev + 1: problems.append(f'{path}: heading level jumps h{prev}->h{lvl}'); break
        prev = lvl
    if not p.title.strip(): problems.append(f'{path}: missing <title>')
    if len(p.title) > 70: notes.append(f'{path}: title is {len(p.title)} chars')
    d = p.meta.get('description', '')
    if not d: problems.append(f'{path}: missing meta description')
    elif not 70 <= len(d) <= 170: notes.append(f'{path}: description is {len(d)} chars')
    if not noindex and p.canonical != PROD + path: problems.append(f'{path}: canonical {p.canonical!r}')
    for k in ('og:title', 'og:description', 'og:image', 'og:url', 'twitter:card'):
        if k not in p.meta and not noindex: problems.append(f'{path}: missing {k}')
    dup = [i for i, c in Counter(p.ids).items() if c > 1]
    if dup: problems.append(f'{path}: duplicate ids {dup}')
    for img in p.imgs:
        if 'alt' not in img: problems.append(f'{path}: <img> without alt {img.get("src")}')
        if not (img.get('width') and img.get('height')): problems.append(f'{path}: <img> without width/height {img.get("src")}')
    for f in p.iframes:
        for k in ('title', 'loading', 'width', 'height'):
            if not f.get(k): problems.append(f'{path}: iframe missing {k}')
    for i in p.inputs:
        if i.get('id') and i['id'] not in p.labels_for and i.get('name') != 'website' and i.get('type') != 'radio':
            problems.append(f'{path}: form control #{i["id"]} has no <label for>')
    for blob in p.jsonld:
        try: json.loads(blob)
        except ValueError as e: problems.append(f'{path}: invalid JSON-LD ({e})')
    visible = ' '.join(p.text)
    if EMAIL_RE.search(visible) or 'mailto:' in html:
        problems.append(f'{path}: email address visible in page')
    if 'teamwriteforus' in html: problems.append(f'{path}: recipient address leaked into HTML')
    if re.search(r'lorem ipsum', visible, re.I): problems.append(f'{path}: placeholder text')

    for href in p.links:
        u = urllib.parse.urlparse(href)
        if u.scheme in ('tel', 'mailto') or (u.scheme and u.netloc and u.netloc != 'friendswoodroofs.com'): continue
        if href.startswith('#'): continue
        target = u.path or path
        link_targets[target].add(path)
        if target.startswith('/assets/') or target.endswith(('.png', '.svg', '.ico', '.xml', '.txt', '.webmanifest')): continue
        if target not in seen and target not in queue: queue.append(target)

for t, ps in titles.items():
    if len(ps) > 1: problems.append(f'duplicate title {t!r}: {ps}')
for d, ps in descs.items():
    if len(ps) > 1: problems.append(f'duplicate description: {ps}')
for path in urls:
    if path != '/' and not link_targets.get(path): problems.append(f'{path}: no internal links point here')

# Article checks
arts = [u for u in urls if u.startswith('/blog/') and u != '/blog/']
for a in arts:
    p = pages[a]
    words = len(re.findall(r"[A-Za-z0-9'’-]+", ' '.join(p.main_text)))
    body = ' '.join(p.main_text)
    ld = [json.loads(x) for x in p.jsonld]
    posting = [g for x in ld for g in x.get('@graph', []) if g.get('@type') == 'BlogPosting']
    shown = re.findall(r'<time datetime="([0-9-]+)"', fetch(a)[1])
    if not posting: problems.append(f'{a}: no BlogPosting schema')
    elif shown and not posting[0]['datePublished'].startswith(shown[0]): problems.append(f'{a}: schema date != displayed date')
    if lastmods.get(a) != (shown[0] if shown else None): problems.append(f'{a}: sitemap lastmod != article date')
    if 'Friendswood Roofers Editorial Team' not in body: problems.append(f'{a}: missing author attribution')
    svc_links = [l for l in p.links if l.startswith('/services/') and l != '/services/']
    art_links = [l for l in p.links if l.startswith('/blog/') and l not in ('/blog/', a) and '?' not in l]
    if not svc_links or not art_links: problems.append(f'{a}: missing service or article links')
    notes.append(f'{a}: ~{words} words in <main> (incl. FAQs, CTA, related links), published {shown[0] if shown else "?"}')

# Keyword usage on the homepage
home = pages['/']
hv = ' '.join(home.main_text).lower()
for kw in ['friendswood roofers', 'roofers friendswood', 'roofers in friendswood', 'friendswood roofing', 'roofing company friendswood']:
    notes.append(f'homepage: "{kw}" appears {hv.count(kw)}x')
if 'friendswood roofers' not in home.title.lower(): problems.append('homepage title lacks primary keyword')

print(f'Checked {len(pages)} pages from {BASE}\n')
for n in notes: print('note:', n)
print()
if problems:
    for pr in problems: print('PROBLEM:', pr)
    print(f'\n{len(problems)} problem(s) found'); sys.exit(1)
print('All checks passed.')
