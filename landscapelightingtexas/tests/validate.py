#!/usr/bin/env python3
"""Render every registered URL with PHP and check SEO/link basics.
   python3 tests/validate.py"""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = subprocess.run(['php', '-r', 'define("LLT",1); require "inc/config.php"; require "inc/registry.php"; echo implode("\n", array_keys($PAGES));'],
                      cwd=ROOT, capture_output=True, text=True).stdout.split()
def render(u):
    r = subprocess.run(['php', 'tests/render.php', u], cwd=ROOT, capture_output=True, text=True)
    return r.stdout, r.stderr, r.returncode
errs, titles, descs = [], {}, {}
legacy = ['/', '/about-us/', '/quote/', '/areas/', '/blog/', '/category/general/', '/landscape-lighting-complete-guide/',
          '/landscape-lighting-cost-calculator/', '/privacy-policy/', '/terms-of-service/', '/sitemap/']
for u in legacy:
    if u not in urls: errs.append(f'legacy URL missing: {u}')
for u in urls:
    html, err, code = render(u)
    if err.strip() or code: errs.append(f'{u}: render error {err.strip()[:200]}')
    t = re.search(r'<title>(.*?)</title>', html); d = re.search(r'name="description" content="([^"]*)"', html)
    titles.setdefault(t and t.group(1), []).append(u); descs.setdefault(d and d.group(1), []).append(u)
    if len(re.findall(r'<h1[\s>]', html)) != 1: errs.append(f'{u}: {len(re.findall(r"<h1[\s>]", html))} h1')
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: json.loads(m)
        except Exception as e: errs.append(f'{u}: bad JSON-LD {e}')
    for href in set(re.findall(r'(?:href|src|data-full)="(/[^"#?]*)', html)):
        if href.startswith('//'): continue
        if href in urls or os.path.isfile(ROOT + href) or href in ('/feed/',): continue
        errs.append(f'{u}: broken link {href}')
    for img in re.findall(r'<img [^>]*>', html):
        if 'alt=' not in img: errs.append(f'{u}: img without alt')
for k, v in titles.items():
    if len(v) > 1: errs.append(f'duplicate title {k}: {v}')
for k, v in descs.items():
    if len(v) > 1: errs.append(f'duplicate description: {v}')
home = render('/')[0]
main = home[home.index('<main'):home.index('</main>')]
kw = re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', main, flags=re.S)).count('Landscape Lighting Texas')
if kw < 14: errs.append(f'homepage keyword count {kw} < 14')
print(f'{len(urls)} pages checked; homepage keyword uses: {kw}')
print('\n'.join(errs) or 'OK')
sys.exit(1 if errs else 0)
