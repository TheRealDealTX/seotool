"""Searches Openverse for commercially usable (CC0 / public domain / CC BY) photos
for each product kind, downloads candidates and builds numbered contact sheets
for picking. Output: work/photos/<kind>/NN.jpg, work/photos/<kind>/meta.json,
work/photos/sheets/<kind>.jpg.   python3 scripts/fetch_photos.py [kind ...]"""
import json, os, sys, time, urllib.parse, urllib.request
from io import BytesIO
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work', 'photos')
UA = {'User-Agent': 'GapArboristSupply/1.0 (info@gaparboristsupply.com)'}
QUERIES = {
 'chainsaw': ['husqvarna chainsaw', 'chainsaw logging'], 'top-handle': ['arborist chainsaw tree'], 'pole-saw': ['pole saw pruning'],
 'hand-saw': ['pruning saw', 'folding saw'], 'pruner': ['pruning shears'], 'chain-bar': ['chainsaw chain'], 'spark-plug': ['spark plug'],
 'parts': ['small engine repair'], 'fluid': ['jerry can'], 'wedge-axe': ['axe wood'], 'log-tool': ['peavey logging'], 'wrench-file': ['chainsaw sharpening'],
 'case-bag': ['climbing gear bag'], 'chaps-pants': ['chainsaw chaps'], 'boot': ['leather work boots'], 'apparel': ['work clothes flannel'],
 'helmet': ['climbing helmet'], 'eye-ear': ['safety glasses', 'ear muffs hearing protection'], 'gloves': ['work gloves'], 'first-aid': ['first aid kit'],
 'traffic': ['traffic cone'], 'carabiner': ['carabiner'], 'pulley': ['climbing pulley'], 'ascender': ['rope ascender'], 'friction-device': ['belay device'],
 'lanyard': ['arborist climbing lanyard'], 'saddle': ['tree climbing harness', 'arborist climbing'], 'spur': ['climbing spikes tree'],
 'rope': ['climbing rope coil'], 'throw-line': ['arborist tree climbing rope'], 'sling': ['rigging sling'], 'rigging-device': ['tree removal rigging'],
 'cable-hardware': ['eye bolt'], 'power-tool': ['leaf blower', 'string trimmer'], 'battery': ['cordless tool battery'], 'book': ['books stack'],
 'jobsite': ['bucket truck tree', 'wood chipper'], 'hero': ['arborist', 'tree surgeon', 'tree removal crew'],
}
def api(q):
    u = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0,pdm,by', 'page_size': 20, 'mature': 'false'})
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))['results']
# Extra passes: "folder=query one|query two" adds a new candidate folder.
for a in sys.argv[1:]:
    if '=' in a: k, q = a.split('=', 1); QUERIES[k] = q.split('|')
kinds = [a.split('=')[0] for a in sys.argv[1:]] or list(QUERIES)
os.makedirs(os.path.join(ROOT, 'sheets'), exist_ok=True)
for kind in kinds:
    d = os.path.join(ROOT, kind); os.makedirs(d, exist_ok=True)
    meta, seen = [], set()
    for q in QUERIES[kind]:
        try: res = api(q)
        except Exception as e: print('search fail', kind, q, e); time.sleep(5); continue
        time.sleep(3.5)
        for r in res:
            if r['id'] in seen or (r.get('width') or 0) < 600: continue
            seen.add(r['id'])
            try:
                raw = urllib.request.urlopen(urllib.request.Request(r['url'], headers=UA), timeout=40).read()
                im = Image.open(BytesIO(raw)).convert('RGB')
            except Exception as e:
                continue
            n = len(meta); im.save(os.path.join(d, f'{n:02d}.jpg'), quality=88)
            meta.append({k: r.get(k) for k in ('id', 'title', 'creator', 'creator_url', 'license', 'license_version', 'license_url', 'foreign_landing_url', 'attribution', 'source', 'url')} | {'n': n, 'q': q, 'size': im.size})
    json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), indent=1)
    # contact sheet
    cols, tw, th = 6, 260, 195
    rows = max(1, -(-len(meta) // cols))
    sheet = Image.new('RGB', (cols * tw, rows * th), 'white'); dr = ImageDraw.Draw(sheet)
    for m in meta:
        im = Image.open(os.path.join(d, f"{m['n']:02d}.jpg")); im.thumbnail((tw - 6, th - 6))
        x, y = (m['n'] % cols) * tw, (m['n'] // cols) * th
        sheet.paste(im, (x + 3, y + 3)); dr.rectangle([x + 3, y + 3, x + 33, y + 25], fill='black'); dr.text((x + 8, y + 7), str(m['n']), fill='yellow')
    sheet.save(os.path.join(ROOT, 'sheets', f'{kind}.jpg'), quality=80)
    print(kind, len(meta), flush=True)
