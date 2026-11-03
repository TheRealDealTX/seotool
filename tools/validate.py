#!/usr/bin/env python3
"""Crawl the local preview (php -S 127.0.0.1:8080 -t public tools/dev-router.php) and check every page."""
import json, re, sys, urllib.request, urllib.error, html
from urllib.parse import urljoin, urlparse
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080'
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedir)
def get(path):
    try:
        r = op.open(BASE + path, timeout=20); return r.status, r.read().decode('utf-8', 'replace'), r.headers
    except urllib.error.HTTPError as e: return e.code, e.read().decode('utf-8', 'replace'), e.headers
code, sm, _ = get('/sitemap.xml')
pages = [urlparse(u).path for u in re.findall(r'<loc>([^<]+)</loc>', sm) if '/assets/' not in u]
errs, titles, descs, seen_links = [], {}, {}, set()
for p in pages:
    c, body, _ = get(p)
    if c != 200: errs.append(f'{p}: HTTP {c}'); continue
    if re.search(r'(Warning|Notice|Fatal error|Deprecated)</b>:|on line <b>', body): errs.append(f'{p}: PHP error output')
    h1 = re.findall(r'<h1[\s>]', body)
    if len(h1) != 1: errs.append(f'{p}: {len(h1)} h1')
    t = html.unescape(re.search(r'<title>(.*?)</title>', body, re.S).group(1))
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', body).group(1))
    if not (25 <= len(t) <= 65): errs.append(f'{p}: title length {len(t)}: {t}')
    if not (110 <= len(d) <= 165): errs.append(f'{p}: description length {len(d)}')
    if t in titles: errs.append(f'{p}: duplicate title with {titles[t]}')
    if d in descs: errs.append(f'{p}: duplicate description with {descs[d]}')
    titles[t] = p; descs[d] = p
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', body).group(1)
    if urlparse(canon).path != p: errs.append(f'{p}: canonical {canon}')
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S):
        try: json.loads(blk)
        except Exception as e: errs.append(f'{p}: bad JSON-LD {e}')
    for img in re.findall(r'<img [^>]*>', body):
        if 'alt="' not in img: errs.append(f'{p}: img without alt {img[:80]}')
    for href in re.findall(r'(?:href|src)="([^"#]*)', body):
        if href.startswith(('mailto:', 'tel:', 'data:', 'javascript:')) or not href: continue
        u = urlparse(urljoin('https://solarcctvcamera.com' + p, href))
        if u.netloc not in ('solarcctvcamera.com', ''): continue
        seen_links.add(u.path)
for l in sorted(seen_links):
    c, _, h = get(l)
    if c != 200: errs.append(f'link {l}: HTTP {c} {h.get("Location","")}')
# legacy redirects
for old in ['/guides/how-does-solar-camera-work/', '/category/guides/', '/tag/rv-camera/', '/wp-admin/', '/sitemap_index.xml', '/guides/solar-camera-panel-angle', '/reviews/are-solar-powered-cctv-cameras-any-good/']:
    c, _, h = get(old)
    if c != 301: errs.append(f'redirect {old}: {c}')
    else:
        tgt = urlparse(h['Location']).path
        if get(tgt)[0] != 200: errs.append(f'redirect {old} -> {tgt} not 200')
for bad in ['/nope/', '/inc/bootstrap.php', '/content/solar-vs-wired.php', '/pages/home.php']:
    c, b, _ = get(bad)
    if c != 404 or 'SCC' in b[:20]: errs.append(f'{bad}: expected 404 got {c}')
print(f'{len(pages)} pages, {len(seen_links)} internal URLs checked')
print('\n'.join(errs) or 'ALL OK')
sys.exit(1 if errs else 0)
