#!/usr/bin/env python3
"""Merge tools/rewrites/<slug>.json (new title/meta/FAQ/products) into public/content/posts.json."""
import json, os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pj = os.path.join(ROOT, 'public/content/posts.json')
posts = json.load(open(pj))
by = {p['slug']: p for p in posts}
n = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'tools/rewrites/*.json'))):
    slug = os.path.basename(f)[:-5]
    if slug not in by: continue
    r = json.load(open(f)); p = by[slug]
    for k in ('title', 'seo_title', 'description', 'categories', 'products', 'faq'):
        if r.get(k): p[k] = r[k]
    body = open(os.path.join(ROOT, 'public/content/posts', slug + '.html')).read()
    text = re.sub(r'<[^>]+>', ' ', body)
    p['words'] = len(text.split()) + sum(len((x['q'] + ' ' + x['a']).split()) for x in p['faq'])
    p['modified'] = r.get('modified', '2026-11-19T09:00:00+00:00')
    p['status'] = 'rewritten'
    n += 1
# Kept posts that shipped without a reading list get one (content itself untouched).
EXTRA = {'heres-what-happens-when-youre-not-present': [
    {'title': 'The Power of Now', 'by': 'Eckhart Tolle', 'blurb': 'The modern classic on stepping out of your head and into this moment.', 'q': 'The Power of Now Eckhart Tolle'},
    {'title': 'Wherever You Go, There You Are', 'by': 'Jon Kabat-Zinn', 'blurb': 'Short, practical chapters on mindfulness in everyday life.', 'q': 'Wherever You Go There You Are Jon Kabat-Zinn'},
    {'title': 'How to Do Nothing', 'by': 'Jenny Odell', 'blurb': 'Reclaiming attention from the attention economy.', 'q': 'How to Do Nothing Jenny Odell'}]}
for slug, prods in EXTRA.items():
    if slug in by and not by[slug]['products']: by[slug]['products'] = prods
json.dump(posts, open(pj, 'w'), indent=1, ensure_ascii=False)
print('applied', n)
