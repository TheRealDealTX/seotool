"""Turns url-plan.json into the build plan: the category tree, the canonical
category of every product URL, and which products get full pages (the rest
301 to their category). Writes seo-data/build-plan.json."""
import json, os, collections
SEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'seo-data')
plan = json.load(open(os.path.join(SEO, 'url-plan.json')))['urls']
SHORT = {
 '16-strand-climbing-rope': '/rope/climbing-rope/16-strand-climbing-rope/',
 '24-strand-climbing-rope': '/rope/climbing-rope/24-strand-climbing-rope/',
 'static-climbing-rope': '/rope/climbing-rope/static-climbing-rope/',
 'climbing-rope': '/rope/climbing-rope/',
 'accessory-carabiners': '/climbing/climbing-gear/carabiners-and-hardware/accessory-carabiners/',
 'adjustable-slings': '/rigging/rigging-slings/adjustable-slings/',
 'arborist-boots': '/clothing/arborist-boots/',
 'auto-locking-carabiners': '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/',
 'battery-powered-equipment': '/jobsite/power-equipment/battery-powered-equipment/',
 'blades': '/cutting-and-pruning/blades/',
 'blowers-and-other-equipment': '/jobsite/power-equipment/blowers-and-other-equipment/',
 'chainsaw-bars': '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-bars/',
 'chainsaw-chain': '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-chain/',
 'chainsaw-chaps': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-chaps/',
 'chainsaw-pants': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-pants/',
 'chainsaw-lanyards': '/climbing/climbing-gear/chainsaw-lanyards/',
 'chainsaws': '/jobsite/power-equipment/chainsaws/',
 'climber-pads': '/climbing/spurs/climber-pads/',
 'communication': '/safety/communication/',
 'crane-slings': '/rigging/rigging-slings/crane-slings/',
 'devices-for-mrs': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/',
 'european-saddles': '/climbing/saddles-and-harnesses/european-saddles/',
 'eye-and-eye-prusiks': '/climbing/climbing-gear/hitch-cord-and-split-tails/eye-and-eye-prusiks/',
 'fall-protection': '/safety/fall-protection/',
 'fluids': '/jobsite/chainsaw-accessories/fluids/',
 'foot-ascenders-and-foot-loops': '/climbing/climbing-gear/ascent-and-descent/foot-ascenders-and-foot-loops/',
 'gear-bags': '/climbing/climbing-gear/gear-storage/gear-bags/',
 'heavy-duty-slings': '/rigging/rigging-slings/heavy-duty-slings/',
 'helmets': '/safety/hearing-protection/',
 'landscaper-tools': '/jobsite/landscaper-tools/',
 'lanyard-kits': '/climbing/climbing-gear/fliplines-and-lanyards/lanyard-kits/',
 'lowering-devices': '/rigging/lowering-devices/',
 'micro-pulleys': '/climbing/climbing-gear/micro-pulleys/',
 'other-gear': '/climbing/climbing-gear/other-gear/',
 'parts': '/jobsite/power-equipment/parts/',
 'parts-and-accessories': '/jobsite/power-equipment/parts/',
 'planting': '/plant-care/planting/',
 'replacement-gaffs-and-parts': '/climbing/spurs/replacement-gaffs-and-parts/',
 'rigging-kits': '/rigging/rigging-kits/',
 'rigging-pulleys': '/rigging/blocks-and-other-hardware/rigging-pulleys/',
 'rope-bags': '/climbing/climbing-gear/gear-storage/rope-bags/',
 'rope-grabs': '/climbing/climbing-gear/ascent-and-descent/rope-grabs/',
 'rope-lanyards': '/climbing/climbing-gear/fliplines-and-lanyards/rope-lanyards/',
 'saddle-parts-and-shoulder-harnesses': '/climbing/saddles-and-harnesses/saddle-parts-and-shoulder-harnesses/',
 'saddle-storage': '/climbing/climbing-gear/carabiners-and-hardware/saddle-storage/',
 'spurs': '/climbing/spurs/aluminum-spurs/',
 'stump-grinding': '/jobsite/stump-grinding/',
 'swivels': '/climbing/climbing-gear/swivels/',
 'throw-line': '/climbing/throw-weight-and-line/throw-line/',
 'tree-climbing-pants': '/clothing/tree-climbing-pants/',
 'wedges': '/jobsite/chainsaw-accessories/wedges/',
 'wrenches-and-files': '/jobsite/chainsaw-accessories/wrenches-and-files/',
 'books-and-training-materials': '/books-and-training-materials/',
 'shop-all': None,  # decided per product below
}
SHOP_ALL = {
 '1-2-eye-bolt': '/plant-care/cabling-and-bracing/cabling-hardware/',
 '10-5mm-replacement-rope-bridge-with-sewn-eyes': '/climbing/saddles-and-harnesses/saddle-parts-and-shoulder-harnesses/',
 '4-endless-loop-polyester-round-sling': '/rigging/rigging-slings/crane-slings/',
 'arbortec-breatheflex-pro-realtree-camo-jacket-orange': '/clothing/sweatshirts-and-jackets/',
 'clogger-zero-light-and-cool-ul-chainsaw-chaps-apron-style': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-chaps/',
 'endless-loop-polyester-round-sling-7-x-20-blue': '/rigging/rigging-slings/crane-slings/',
 'endless-loop-round-slings-1': '/rigging/rigging-slings/crane-slings/',
 'husqvarna-530ipt-battery-powered-pole-saw-without-batteries-or-charger': '/jobsite/power-equipment/battery-powered-equipment/',
 'husqvarna-chainsaw-maintenance-kit-for-340-353-346xp': '/jobsite/power-equipment/parts/',
 'husqvarna-k770-power-cutter': '/jobsite/power-equipment/blowers-and-other-equipment/',
 'husqvarna-titanium-xpro-trimmer-line': '/jobsite/landscaper-tools/',
 'husqvarna-trimforce-trimmer-line': '/jobsite/landscaper-tools/',
 'kask-zenith-x2-hi-viz-climbing-helmet': '/climbing/helmets/',
 'notch-fusion-rope-wrench-tether': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/',
 'pferd-guide-bar-dresser': '/jobsite/chainsaw-accessories/wrenches-and-files/',
 'polymer-hook-with-standard-end': '/climbing/climbing-gear/carabiners-and-hardware/saddle-storage/',
 'premium-5-8-crane-sling-kit': '/rigging/rigging-slings/crane-slings/',
 'standard-5-8-crane-sling-kit': '/rigging/rigging-slings/crane-slings/',
 'stars-and-stripes-adjustable-friction-saver': '/climbing/climbing-gear/friction-savers/',
}
CAT_ALIAS = {  # odd old category URLs -> where they now live
 '/climbing-gear/': '/climbing/climbing-gear/',
 '/climbing/climbing-gear/mechanical-friction-devices/': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/',
 '/climbing/climbing-gear/mechanical-friction-devices/mrs-climbing-devices/': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/',
 '/climbing/climbing-gear/mechanical-friction-devices/srs-climbing-devices/': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/',
 '/climbing/climbing-gear/fliplines-and-lanyards/rope-grabs-and-lanyard-adjusters/': '/climbing/climbing-gear/ascent-and-descent/rope-grabs/',
 '/climbing/climbing-gear/carabiners-and-hardware/steel-carabiners/': '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/',
 '/climbing/spurs/straps/': '/climbing/spurs/replacement-gaffs-and-parts/',
 '/climbing/throw-weight-and-line/throw-line-storage/': '/climbing/throw-weight-and-line/',
 '/climbing/saddles-and-harnesses/saddle-accessories/': '/climbing/saddles-and-harnesses/saddle-parts-and-shoulder-harnesses/',
 '/climbing/saddles-and-harnesses/full-body-harnesses/': '/safety/fall-protection/',
 '/climbing/climbing-gear/srs-basal-and-canopy-anchors/': '/climbing/climbing-gear/other-gear/',
 '/climbing/climbing-gear/hitch-cord-and-split-tails/prusik-loops/': '/climbing/climbing-gear/hitch-cord-and-split-tails/',
 '/climbing/climbing-gear/hitch-cord-and-split-tails/split-tails/': '/climbing/climbing-gear/hitch-cord-and-split-tails/',
 '/climbing/climbing-gear/fliplines-and-lanyards/2-in-1-lanyards/': '/climbing/climbing-gear/fliplines-and-lanyards/',
 '/climbing/climbing-gear/fliplines-and-lanyards/wire-core-lanyards/': '/climbing/climbing-gear/fliplines-and-lanyards/',
 '/climbing/climbing-gear/fliplines-and-lanyards/basic-adjustable-lanyards/': '/climbing/climbing-gear/fliplines-and-lanyards/',
 '/climbing/climbing-gear/carabiners-and-hardware/configuration-aids-and-corner-traps/': '/climbing/climbing-gear/carabiners-and-hardware/hardware/',
 '/climbing/climbing-gear/carabiners-and-hardware/screw-gate-carabiners/': '/climbing/climbing-gear/carabiners-and-hardware/',
 '/climbing/climbing-gear/carabiners-and-hardware/non-locking-carabiners/': '/climbing/climbing-gear/carabiners-and-hardware/',
 '/climbing/climbing-gear/rings/': '/climbing/climbing-gear/carabiners-and-hardware/hardware/',
 '/climbing/climbing-gear/swivels/': '/climbing/climbing-gear/carabiners-and-hardware/hardware/',
 '/climbing/climbing-gear/ascent-and-descent/descenders/': '/climbing/climbing-gear/ascent-and-descent/',
 '/climbing/climbing-gear/ascent-and-descent/handled-ascenders/': '/climbing/climbing-gear/ascent-and-descent/',
 '/climbing/climbing-gear/ascent-and-descent/non-handled-ascenders/': '/climbing/climbing-gear/ascent-and-descent/',
 '/climbing/spurs/lightweight-spurs/': '/climbing/spurs/aluminum-spurs/',
 '/safety/helmets/': '/climbing/helmets/',
 '/safety/chainsaw-protection/': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/',
 '/rigging/rigging-slings/ring-slings/': '/rigging/rigging-slings/heavy-duty-slings/',
 '/rigging/rigging-slings/light-duty-slings/': '/rigging/rigging-slings/',
 '/rigging/rigging-slings/heavy-duty-webbing-slings/': '/rigging/rigging-slings/heavy-duty-slings/',
 '/rigging/blocks-and-other-hardware/rigging-plates/': '/rigging/blocks-and-other-hardware/',
 '/rigging/blocks-and-other-hardware/rigging-blocks/': '/rigging/blocks-and-other-hardware/',
 '/rigging/blocks-and-other-hardware/rings-and-other-hardware/': '/rigging/blocks-and-other-hardware/',
 '/rope/accessory-cord/': '/rope/tech-cordage/',
 '/rope/winch-line-and-synthetic-cable/': '/rope/rigging-rope/',
 '/rope/climbing-rope/12-strand-climbing-rope/': '/rope/climbing-rope/',
 '/rope/climbing-rope/16-strand-climbing-rope/': '/rope/climbing-rope/',
 '/rope/climbing-rope/24-strand-climbing-rope/': '/rope/climbing-rope/',
 '/rope/climbing-rope/static-climbing-rope/': '/rope/climbing-rope/',
 '/cutting-and-pruning/parts-and-accessories/': '/cutting-and-pruning/poles-and-kits/',
 '/plant-care/plant-health-care/': '/plant-care/',
 '/plant-care/cabling-and-bracing/cable/': '/plant-care/cabling-and-bracing/',
 '/plant-care/cabling-and-bracing/bracing/': '/plant-care/cabling-and-bracing/',
 '/plant-care/cabling-and-bracing/bracing/bracing-rods/': '/plant-care/cabling-and-bracing/',
 '/plant-care/cabling-and-bracing/cabling-accessories/': '/plant-care/cabling-and-bracing/',
 '/plant-care/cabling-and-bracing/cabling-hardware/': '/plant-care/cabling-and-bracing/',
 '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-bars/': '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/',
 '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-chain/': '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/',
 '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-pants/': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/',
 '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-chaps/': '/jobsite/chainsaw-accessories/chaps-and-protective-gear/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/bucket-truck-accessories/': '/jobsite/bucket-truck-and-aerial-lift-gear/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/ground-protection-mats/': '/jobsite/bucket-truck-and-aerial-lift-gear/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/bucket-truck-and-aerial-lift-scabbards/': '/jobsite/bucket-truck-and-aerial-lift-gear/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/fall-arrest-for-aerial-lifts/': '/jobsite/bucket-truck-and-aerial-lift-gear/',
 '/jobsite/logging-tools/forestry-tools/': '/jobsite/logging-tools/',
 '/jobsite/logging-tools/axes-and-mauls/': '/jobsite/logging-tools/',
 '/jobsite/logging-tools/log-handling-tools/': '/jobsite/logging-tools/',
 '/climbing/climbing-gear/gear-storage/gear-bags/': '/climbing/climbing-gear/gear-storage/',
 '/climbing/climbing-gear/gear-storage/rope-bags/': '/climbing/climbing-gear/gear-storage/',
 '/climbing/throw-weight-and-line/throw-line/': '/climbing/throw-weight-and-line/',
 '/climbing/throw-weight-and-line/throw-line-kits/': '/climbing/throw-weight-and-line/',
 '/climbing/throw-weight-and-line/throw-weights/': '/climbing/throw-weight-and-line/',
 '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/',
 '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/': '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/',
 '/climbing/climbing-gear/ascent-and-descent/rope-grabs/': '/climbing/climbing-gear/ascent-and-descent/',
 '/climbing/climbing-gear/fliplines-and-lanyards/lanyard-kits/': '/climbing/climbing-gear/fliplines-and-lanyards/',
 '/climbing/spurs/replacement-gaffs-and-parts/': '/climbing/spurs/',
 '/climbing/spurs/climber-pads/': '/climbing/spurs/',
 '/climbing/saddles-and-harnesses/european-saddles/': '/climbing/saddles-and-harnesses/',
 '/jobsite/chainsaw-accessories/fluids/': '/jobsite/chainsaw-accessories/',
 '/jobsite/chainsaw-accessories/wedges/': '/jobsite/chainsaw-accessories/',
 '/jobsite/chainsaw-accessories/chainsaw-cases-and-scabbards/': '/jobsite/chainsaw-accessories/',
 '/jobsite/chainsaw-accessories/wrenches-and-files/': '/jobsite/chainsaw-accessories/',
 '/rigging/rigging-slings/adjustable-slings/': '/rigging/rigging-slings/',
 '/rigging/blocks-and-other-hardware/rigging-pulleys/': '/rigging/blocks-and-other-hardware/',
 '/climbing/climbing-gear/carabiners-and-hardware/accessory-carabiners/': '/climbing/climbing-gear/carabiners-and-hardware/',
 '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/': '/climbing/climbing-gear/carabiners-and-hardware/',
 '/climbing/climbing-gear/hitch-cord-and-split-tails/eye-and-eye-prusiks/': '/climbing/climbing-gear/hitch-cord-and-split-tails/',
 '/jobsite/power-equipment/parts/': '/jobsite/power-equipment/',
 '/rope/tech-cordage/': '/rope/',
 '/rope/rope-care-and-splicing/': '/rope/',
}
# A category in CAT_ALIAS is "merged": its products list under the target and its URL 301s there,
# UNLESS it is kept (has traffic/backlinks or is a hub). Keep list:
KEEP = {'/climbing/climbing-gear/carabiners-and-hardware/screw-gate-carabiners/', '/climbing/climbing-gear/carabiners-and-hardware/non-locking-carabiners/',
 '/climbing/climbing-gear/fliplines-and-lanyards/lanyard-kits/', '/climbing/spurs/climber-pads/', '/climbing/spurs/replacement-gaffs-and-parts/',
 '/climbing/climbing-gear/gear-storage/gear-bags/', '/climbing/climbing-gear/gear-storage/rope-bags/', '/climbing/throw-weight-and-line/throw-line/',
 '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/', '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/',
 '/climbing/climbing-gear/hitch-cord-and-split-tails/eye-and-eye-prusiks/', '/climbing/saddles-and-harnesses/european-saddles/',
 '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/', '/climbing/climbing-gear/carabiners-and-hardware/hardware/',
 '/climbing/climbing-gear/ascent-and-descent/rope-grabs/', '/climbing/climbing-gear/fliplines-and-lanyards/rope-lanyards/',
 '/rope/climbing-rope/static-climbing-rope/', '/rope/climbing-rope/24-strand-climbing-rope/',
 '/plant-care/cabling-and-bracing/cabling-hardware/', '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-chaps/',
 '/jobsite/chainsaw-accessories/chaps-and-protective-gear/chainsaw-pants/', '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-chain/',
 '/jobsite/chainsaw-accessories/chainsaw-bars-and-chain/chainsaw-bars/', '/jobsite/chainsaw-accessories/fluids/', '/jobsite/chainsaw-accessories/wedges/',
 '/jobsite/chainsaw-accessories/chainsaw-cases-and-scabbards/', '/jobsite/chainsaw-accessories/wrenches-and-files/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/fall-arrest-for-aerial-lifts/', '/jobsite/bucket-truck-and-aerial-lift-gear/bucket-truck-and-aerial-lift-scabbards/',
 '/jobsite/bucket-truck-and-aerial-lift-gear/ground-protection-mats/', '/jobsite/bucket-truck-and-aerial-lift-gear/bucket-truck-accessories/',
 '/jobsite/logging-tools/log-handling-tools/', '/jobsite/logging-tools/forestry-tools/', '/jobsite/logging-tools/axes-and-mauls/',
 '/rigging/rigging-slings/adjustable-slings/', '/rigging/blocks-and-other-hardware/rigging-pulleys/', '/rigging/blocks-and-other-hardware/rigging-blocks/',
 '/climbing/throw-weight-and-line/throw-line-kits/', '/jobsite/power-equipment/parts/', '/rope/tech-cordage/', '/rope/rope-care-and-splicing/',
 '/rope/climbing-rope/16-strand-climbing-rope/', '/rigging/blocks-and-other-hardware/rings-and-other-hardware/', '/climbing/climbing-gear/swivels/',
 '/climbing/climbing-gear/rings/',
}

def cat_of(path):
    segs = path.strip('/').split('/')
    if len(segs) >= 3 or (len(segs) == 2 and segs[0] in ('climbing','rigging','rope','safety','jobsite','clothing','plant-care','cutting-and-pruning','books-and-training-materials')):
        c = '/' + '/'.join(segs[:-1]) + '/'
        if segs[0] == 'shop-all': c = SHOP_ALL[segs[-1]]
    elif segs[0] == 'shop-all':
        c = SHOP_ALL[segs[1]]
    else:
        c = SHORT[segs[0]]
    # resolve merged categories
    seen = 0
    while c in CAT_ALIAS and c not in KEEP and seen < 5:
        c = CAT_ALIAS[c]; seen += 1
    return c

products = [u for u in plan if u['type'] == 'product']
for p in products:
    p['category'] = cat_of(p['path'])
sel = {p['path'] for p in products if p['traffic'] >= 1 or p['top_volume'] >= 390 or p['backlinks'] > 0}
by_cat = collections.defaultdict(list)
for p in products: by_cat[p['category']].append(p)
for c, ps in by_cat.items():
    ps.sort(key=lambda x: (-x['traffic'], -x['top_volume']))
    have = sum(1 for p in ps if p['path'] in sel)
    for p in ps:
        if have >= 3: break
        if p['path'] not in sel: sel.add(p['path']); have += 1
built = [dict(p, build=True) for p in products if p['path'] in sel]
redirected = [{'path': p['path'], 'to': p['category']} for p in products if p['path'] not in sel]

# category set: every category a built product sits in, plus all ancestors, plus kept old category URLs
cats = set()
for p in built:
    c = p['category']
    while c and c != '/':
        cats.add(c); c = '/' + '/'.join(c.strip('/').split('/')[:-1]) + '/' if c.strip('/').count('/') else None
cats |= {u['path'] for u in plan if u['type'] == 'category' and (u['path'] not in CAT_ALIAS or u['path'] in KEEP)}
cats -= {'/brands/', '/shop-all/', '/volume-purchasing/', '/climbing-gear/'}
cat_redirects = []
for u in plan:
    if u['type'] == 'category' and u['path'] not in cats and u['path'] not in ('/brands/', '/shop-all/', '/volume-purchasing/'):
        t = u['path']
        while t not in cats and t in CAT_ALIAS: t = CAT_ALIAS[t]
        cat_redirects.append({'path': u['path'], 'to': t})
kwmap = {u['path']: u for u in plan}
catlist = []
for c in sorted(cats):
    u = kwmap.get(c, {})
    n = sum(1 for p in built if p['category'] == c or p['category'].startswith(c))
    catlist.append({'path': c, 'keywords': u.get('keywords', []), 'traffic': u.get('traffic', 0), 'backlinks': u.get('backlinks', 0), 'built_products': n})
json.dump({'categories': catlist, 'products': built, 'product_redirects': redirected, 'category_redirects': cat_redirects,
           'brands': [u for u in plan if u['type'] == 'brand']}, open(os.path.join(SEO, 'build-plan.json'), 'w'), indent=1)
print('categories', len(catlist), 'built products', len(built), 'redirected products', len(redirected), 'cat redirects', len(cat_redirects))
for c in catlist:
    if c['built_products'] == 0: print('EMPTY', c['path'])
for r in cat_redirects:
    if r['to'] not in cats: print('BAD REDIRECT', r)
