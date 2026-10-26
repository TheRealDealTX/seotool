"""Post-build checks for the Better Outdoors PHP site. Run against a local server:
    php -S 127.0.0.1:8099 index.php &   then   python3 validate.py [base_url]
"""
import json, re, sys, html, urllib.request, urllib.error
from pathlib import Path

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8099'
SCRATCH_IDS = Path('/tmp/claude-0/-home-user-seotool/a27cbd69-c2e7-5cb0-9217-5edc7f8923a2/scratchpad/ids')

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
opener = urllib.request.build_opener(NoRedirect)

def get(path):
    try:
        r = opener.open(BASE + path)
        return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace'), e.headers

errors = []
def err(m): errors.append(m); print('FAIL', m)

# Old WordPress URLs (from the live sitemaps) must all still return 200.
OLD = ['/', '/blog/', '/category/tips/', '/about-us/', '/contact-us/', '/privacy-policy/', '/terms-of-use/',
       '/2016-pse-draw-length-adjustment/', '/bear-archery-persist-compound-bow/', '/bear-archery-bear-paw-grip/',
       '/understanding-mathews-compound-bow-packages/', '/mathews-prima-level-1-package/',
       '/bear-archery-whitetail-maxx-rth-compound-bow/', '/bear-archery-alaskan-xt-rth-compound-bow/',
       '/2018-pse-evolve-28/', '/mathews-lift-29-5/']
NEW = ['/tools/', '/tools/draw-length-calculator/', '/tools/arrow-speed-calculator/', '/tools/kinetic-energy-calculator/',
       '/tools/bow-finder/', '/tools/bowhunting-checklist/']
REDIRECTS = {'/feed/': '/blog/', '/wp-admin/': '/', '/pages/contact-us': '/contact-us/', '/mathews-lift-29-5': '/mathews-lift-29-5/',
             '/collections/mathews-official-parts-acc?page=5': '/understanding-mathews-compound-bow-packages/',
             '/2016-pse-draw-length-adjustment/feed/': '/2016-pse-draw-length-adjustment/', '/?s=bear': '/blog/?q=bear',
             '/blog/page/2/': '/blog/', '/author/admin/': '/blog/'}
STATIC = ['/wp-content/uploads/2026/01/Bear-Archery-Persist-Compound-Bow.webp', '/wp-content/uploads/2026/01/Bear-Archery-Bear-Paw-Grip-3-1-1024x683.webp',
          '/wp-content/uploads/2026/01/2016-PSE-Draw-Length-Adjustment-300x200.webp', '/wp-content/uploads/2026/01/Mathews-Lift-29.5-2-1024x683.webp',
          '/robots.txt', '/assets/css/site.css', '/assets/js/site.js', '/assets/js/tools.js']
for x in ['sitemap.xml', 'sitemap_index.xml', 'post-sitemap.xml', 'page-sitemap.xml', 'category-sitemap.xml', 'tool-sitemap.xml']:
    STATIC.append('/' + x)

titles, descs, links = {}, {}, set()
# Every post in the sitemap (includes scheduled posts when the server runs with BO_SHOW_SCHEDULED=1).
_, sm, _ = get('/post-sitemap.xml')
EXTRA = [u.replace('https://betteroutdoors.net', '') for u in re.findall(r'<loc>(https://betteroutdoors\.net/[^<]*)</loc>', sm)]
EXTRA = [u for u in EXTRA if u not in OLD]
for p in OLD + NEW + EXTRA:
    code, body, _ = get(p)
    if code != 200: err(f'{p} -> {code}'); continue
    if re.search(r'(Fatal error|Warning:|Parse error|Notice:|Deprecated:)', body): err(f'{p} PHP error output')
    h1 = re.findall(r'<h1[\s>]', body)
    if len(h1) != 1: err(f'{p} has {len(h1)} h1')
    t = re.search(r'<title>(.*?)</title>', body).group(1); d = re.search(r'<meta name="description" content="([^"]*)"', body).group(1)
    if t in titles: err(f'{p} duplicate title with {titles[t]}')
    if d in descs: err(f'{p} duplicate description with {descs[d]}')
    titles[t] = p; descs[d] = p
    if not 30 <= len(html.unescape(t)) <= 70: print(f'note {p} title length {len(html.unescape(t))}')
    if not 110 <= len(html.unescape(d)) <= 165: print(f'note {p} description length {len(html.unescape(d))}')
    if f'<link rel="canonical" href="https://betteroutdoors.net{p}">' not in body: err(f'{p} canonical')
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try: json.loads(blob)
        except Exception as e: err(f'{p} bad JSON-LD {e}')
    for a in re.findall(r'href="(https://www\.amazon\.com[^"]*)"', body):
        if 'tag=betteroutdoors-20' not in html.unescape(a): err(f'{p} amazon link without tag {a}')
    for m in re.findall(r'<img [^>]*>', body):
        if 'alt=' not in m: err(f'{p} img without alt {m[:80]}')
    for h in re.findall(r'(?:href|src)="(/[^"#?]*)', body):
        links.add(h)
    # Legacy heading anchors (Google has indexed some of them).
    slug = p.strip('/') or 'home'
    idf = SCRATCH_IDS / f'{slug.replace("/", "_")}.txt'
    if idf.exists() and slug not in ('home', 'blog', 'category/tips'):
        for line in idf.read_text().splitlines():
            i = line.split(' | ')[0].strip()
            if i and f'id="{i}"' not in body: err(f'{p} lost legacy anchor #{i}')
    if p == '/':
        text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', body, flags=re.S)
        text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
        n = text.count('Better Outdoors')
        print(f'homepage visible "Better Outdoors" mentions: {n}')
        if n < 14: err('homepage brand mentions < 14')

for p in sorted(links):
    if p.startswith('/wp-content') or p.startswith('/assets') or p.endswith('.xml') or p.endswith('.txt'):
        code, _, _ = get(p)
    else:
        code, _, _ = get(p)
    if code != 200: err(f'broken internal link {p} -> {code}')
for p in STATIC:
    code, _, _ = get(p)
    if code != 200: err(f'{p} -> {code}')
for src, dst in REDIRECTS.items():
    code, _, hd = get(src)
    if code != 301 or hd.get('Location') != dst: err(f'redirect {src} -> {code} {hd.get("Location")} (want {dst})')
code, _, _ = get('/no-such-page/')
if code != 404: err(f'404 page returns {code}')
code, b, _ = get('/inc/config.php')
if code != 403 and b.strip(): err('/inc/config.php leaks output')
print(f'checked {len(OLD + NEW + EXTRA)} pages, {len(links)} internal links; {len(errors)} failures')
sys.exit(1 if errors else 0)
