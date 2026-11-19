#!/usr/bin/env python3
"""Search royalty-free (CC0 / public-domain) real photos via the Openverse API.

  python3 tools/find_photos.py "hourglass sunset" [--n 12]

Default source is the WordPress Photo Directory (pd.w.org): CC0 photographs, no attribution
required, direct 2048px downloads. Falls back to Flickr public-domain/CC0 photos.
Prints: url | WxH | source | title — pick landscape images (width > height) for posts.
"""
import json, sys, urllib.parse, urllib.request
q = sys.argv[1]; n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 12
def search(source, lic):
    u = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode(
        {'q': q, 'license': lic, 'source': source, 'page_size': n, 'aspect_ratio': 'wide', 'mature': 'false'})
    with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'tc-photo-finder'}), timeout=30) as r:
        return json.load(r)['results']
res = search('wordpress', 'cc0')
if len(res) < 4: res += search('flickr', 'cc0,pdm')
for r in res:
    if (r.get('width') or 0) < 1200: continue
    print(f"{r['url']} | {r.get('width')}x{r.get('height')} | {r['source']} {r['license']} | {r['title'][:90]}")
