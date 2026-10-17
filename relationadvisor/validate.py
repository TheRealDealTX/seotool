#!/usr/bin/env python3
"""Post-build checks for the relationadvisor.com rebuild.

    python3 validate.py                      # content + output checks
    python3 validate.py http://127.0.0.1:8765  # also request every archived URL against a running server
"""
import glob
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'public')
errors, warns = [], []
err = errors.append
warn = warns.append

plan = {p['slug']: p for p in json.load(open(os.path.join(ROOT, 'content', 'plan.json')))}
ALLOWED = {'h2', 'h3', 'p', 'ul', 'ol', 'li', 'strong', 'em', 'blockquote', 'a', 'div', 'br'}
ALLOWED_CLASSES = {'tip', 'lines', 'note-card'}
LIST_CATS = {'pickup-lines', 'questions', 'captions', 'quotes'}

# ---- content
for slug, meta in plan.items():
    f = os.path.join(ROOT, 'content', 'posts', slug + '.json')
    if not os.path.exists(f):
        err(f'missing post content: {slug}')
        continue
    try:
        p = json.load(open(f, encoding='utf-8'))
    except Exception as ex:
        err(f'{slug}: invalid JSON ({ex})')
        continue
    for k in ('title', 'description', 'excerpt', 'intro', 'body', 'faq', 'takeaways'):
        if not p.get(k):
            err(f'{slug}: missing field {k}')
    if p.get('slug') and p['slug'] != slug:
        err(f'{slug}: slug field mismatch ({p["slug"]})')
    t, d = p.get('title', ''), p.get('description', '')
    if len(t) > 70:
        warn(f'{slug}: title {len(t)} chars')
    if not 110 <= len(d) <= 165:
        warn(f'{slug}: description {len(d)} chars')
    htm = p.get('intro', '') + p.get('body', '')
    for tag in set(re.findall(r'<\s*([a-zA-Z0-9]+)', htm)):
        if tag.lower() not in ALLOWED:
            err(f'{slug}: disallowed tag <{tag}>')
    for cls in re.findall(r'class="([^"]*)"', htm):
        if cls not in ALLOWED_CLASSES:
            err(f'{slug}: disallowed class "{cls}"')
    if re.search(r'style=|<script|on\w+=', htm, re.I):
        err(f'{slug}: inline style/script')
    for href in re.findall(r'href="([^"]+)"', htm):
        m = re.match(r'^/([a-z0-9-]+)/$', href)
        mc = re.match(r'^/category/([a-z-]+)/$', href)
        if mc:
            continue
        if m and m.group(1) in plan:
            continue
        if href.startswith(('https://', 'http://', 'mailto:', 'tel:', 'sms:')):
            continue
        if href in ('/', '/blog/', '/contact/', '/about/'):
            continue
        err(f'{slug}: bad link {href}')
    wc = len(re.sub('<[^>]+>', ' ', htm).split())
    if wc < (900 if meta['cat'] in LIST_CATS else 1100):
        warn(f'{slug}: only {wc} words')
    if len(re.findall(r'<h2', p.get('body', ''))) < 4:
        warn(f'{slug}: fewer than 4 H2s')
    for bad in ('As an AI', "In today's world", 'In today’s world', 'lorem ipsum', '2019'):
        if bad.lower() in (htm + t).lower():
            warn(f'{slug}: contains "{bad}"')
    if htm.count('<') - htm.count('</') - htm.count('<br') < 0:
        warn(f'{slug}: possible unbalanced tags')

# ---- output
pages = sorted(glob.glob(os.path.join(OUT, '**', 'index.html'), recursive=True)) + [os.path.join(OUT, 'home.html'), os.path.join(OUT, '404.html')]
titles, descs = {}, {}
for f in pages:
    rel = os.path.relpath(f, OUT)
    s = open(f, encoding='utf-8').read()
    if len(re.findall(r'<h1[\s>]', s)) != 1:
        err(f'{rel}: expected exactly one <h1>')
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    dsc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    if t in titles:
        err(f'{rel}: duplicate title with {titles[t]}')
    titles[t] = rel
    if dsc in descs:
        err(f'{rel}: duplicate description with {descs[dsc]}')
    descs[dsc] = rel
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(m)
        except Exception as ex:
            err(f'{rel}: bad JSON-LD ({ex})')
    for img in re.findall(r'<img [^>]*>', s):
        if 'alt="' not in img or 'alt=""' in img:
            err(f'{rel}: image without alt')
    for href in set(re.findall(r'(?:href|src)="(/[^"#?]*)', s)):
        target = os.path.join(OUT, href.lstrip('/'))
        if href == '/' or os.path.isfile(target) or os.path.isfile(os.path.join(target, 'index.html')):
            continue
        if href.endswith('.php') and os.path.isfile(target):
            continue
        err(f'{rel}: broken internal link/asset {href}')
    if s.count("gtag('config', 'G-T8DR7RLN6E')") != 1 or 'googletagmanager.com/gtag/js?id=G-T8DR7RLN6E' not in s:
        err(f'{rel}: Google tag missing or duplicated')
    if rel != '404.html' and 'noindex' in s and os.environ.get('STAGING') != '1':
        err(f'{rel}: noindex in a production build')
    if not re.search(r'<link rel="canonical" href="https://relationadvisor\.com/', s):
        err(f'{rel}: missing canonical')
    og = re.search(r'<meta property="og:image" content="https://relationadvisor\.com(/[^"]+)"', s)
    if not og or not os.path.isfile(os.path.join(OUT, og.group(1).lstrip('/'))):
        err(f'{rel}: og:image missing')
    if 'hostingersite' in s:
        err(f'{rel}: temp domain leaked into page')

# ---- archived URLs against a live server
if len(sys.argv) > 1:
    base = sys.argv[1].rstrip('/')
    old = [u.strip() for u in open(os.path.join(ROOT, 'content', 'old-urls.txt')) if u.strip()]

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)

    def fetch(path):
        try:
            r = opener.open(base + path, timeout=20)
            return r.status, None
        except urllib.error.HTTPError as ex:
            return ex.code, ex.headers.get('Location')
    bad = 0
    for path in old:
        code, loc = fetch(path)
        hops = 0
        while code in (301, 302) and loc and hops < 3:
            path2 = re.sub(r'^https?://[^/]+', '', loc)
            code, loc = fetch(path2)
            hops += 1
        if code != 200:
            bad += 1
            err(f'archived URL {path} -> {code}')
    print(f'checked {len(old)} archived URLs, {bad} failing')

for w in warns:
    print('WARN ', w)
for x in errors:
    print('ERROR', x)
print(f'{len(pages)} pages, {len(errors)} errors, {len(warns)} warnings')
sys.exit(1 if errors else 0)
