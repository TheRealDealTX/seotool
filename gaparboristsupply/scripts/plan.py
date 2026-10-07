"""Builds seo-data/url-plan.json from the Semrush exports: every ranking or
backlinked URL, its keywords, traffic and referring links, classified as
category / brand / product, plus which products get full pages."""
import csv, json, re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
SEO = os.path.join(HERE, '..', 'seo-data')
strip = lambda u: re.sub(r'^https?://(www\.)?gaparboristsupply\.com', '', u)

kw = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(SEO, 'organic-positions-2026-06.csv'), encoding='utf-8-sig')):
    u = strip(r['URL']).split('?')[0] or '/'
    kw[u].append({'kw': r['Keyword'], 'vol': int(r['Search Volume'] or 0), 'pos': int(r['Position']), 'traffic': float(r['Traffic'] or 0)})
bl = collections.Counter(); bl_domains = collections.defaultdict(set); bl_raw = collections.Counter()
for r in csv.DictReader(open(os.path.join(SEO, 'backlinks-2026-10.csv'), encoding='utf-8-sig')):
    raw = strip(r['Target url']) or '/'
    bl_raw[raw] += 1
    u = raw.split('?')[0] or '/'
    bl[u] += 1; bl_domains[u].add(re.sub(r'^https?://([^/]+).*', r'\1', r['Source url']))

paths = set(kw) | {u for u in bl if u.endswith('/') and u.islower()}
TOP = {'climbing','rigging','rope','safety','jobsite','clothing','plant-care','cutting-and-pruning',
       'books-and-training-materials','shop-all','brands','volume-purchasing'}
BRANDS = {'3m','all-gear','alliance-equipment','arbortec','arborwear','arbpro','ars','art','buckingham','camp',
 'climb-right','climbing-innovations','climbing-technology','corona','courant','distel','dmm','eagle-safety','echo',
 'edelrid','fanno','felco','forester','ftc','good-rigging','green-manufacturing','hasegawa','irwin','isc','jameson',
 'k-h-distributing','kask','klein','kong','logrite','marlow','marvin','notch-equipment','oregon','petzl','pfanner',
 'pferd','pro-climb','pullr-holdings','rock-exotica','safetree-products','safewaze','samson-rope','sawpod','sena',
 'silky','simonds','smc','stein','sterling-rope','teufelberger','weaver','wesco-boots','westcoast-saw','westcoast-saws','yale-cordage'}
out = []
for p in sorted(paths):
    segs = [s for s in p.strip('/').split('/') if s]
    if p == '/': t = 'home'
    elif len(segs) == 1 and segs[0] in BRANDS: t = 'brand'
    elif len(segs) == 1: t = 'category'
    elif any(q != p and q.startswith(p) for q in paths) and segs[0] in TOP: t = 'category'
    elif segs[0] in TOP and segs[-1] in {'hardware','fluids','blades','gear-bags','rope-bags','throw-line','throw-weights','straps','rings','swivels','prusik-loops','split-tails'}: t='category'
    else: t = 'product'
    k = sorted(kw.get(p, []), key=lambda x: -x['vol'])
    out.append({'path': p, 'type': t, 'traffic': round(sum(x['traffic'] for x in k), 1),
                'top_volume': k[0]['vol'] if k else 0,
                'keywords': [f"{x['kw']} (vol {x['vol']}, pos {x['pos']})" for x in k[:6]],
                'backlinks': bl.get(p, 0), 'ref_domains': len(bl_domains.get(p, ()))})
json.dump({'urls': out, 'raw_backlink_targets': bl_raw.most_common()}, open(os.path.join(SEO, 'url-plan.json'), 'w'), indent=1)
c = collections.Counter(o['type'] for o in out); print(c)
