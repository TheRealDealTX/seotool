#!/usr/bin/env python3
"""Search for and download royalty-free photos (CC0, public domain or CC BY) via the Openverse API.

  python3 _dev/fetch_image.py search "hail damage roof" [more queries...]
      -> lists candidates: id, license, size, source, title, creator

  python3 _dev/fetch_image.py get <openverse-id> <file-stem> "<alt text>" ["caption"]
      -> downloads the original, saves assets/img/blog/<file-stem>.webp (max 1400px wide)
         and prints a ready-to-paste <figure> with the required attribution.

Only cc0, pdm and by licenses are requested, so every image may be used commercially;
CC BY images carry a visible credit line in the figcaption (required by the license).
"""
import json, os, sys, urllib.parse, urllib.request, io, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = 'https://api.openverse.org/v1/images/'
UA = {'User-Agent': 'TXIA-content-bot/1.0 (https://txinsuranceappraiser.com/contact-us/)'}
LICENSE_NAMES = {'cc0': 'CC0', 'pdm': 'Public Domain', 'by': 'CC BY'}


def api(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode())


def search(queries):
    for q in queries:
        url = API + '?' + urllib.parse.urlencode({'q': q, 'license': 'cc0,pdm,by', 'page_size': 12, 'mature': 'false', 'excluded_source': 'flickr'})
        print(f'== {q}')
        for r in api(url).get('results', []):
            if (r.get('width') or 0) < 800:
                continue
            print(f"  {r['id']}  {r['license']:3s} {r.get('width')}x{r.get('height')} {r['source']:10s} | {r['title'][:60]} | {(r.get('creator') or '')[:24]}")


def get(img_id, stem, alt, caption=''):
    from PIL import Image
    r = api(API + img_id + '/')
    if r['license'] not in LICENSE_NAMES:
        sys.exit(f"license {r['license']} not allowed")
    src = r['url']
    cands = [src]
    m = __import__('re').match(r'(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/(.+)$', src)
    if m:  # Wikimedia asks bots to use standard thumbnail sizes instead of originals
        w = r.get('width') or 0
        sizes = ['1280px', '960px'] if w > 1280 else ['960px', '500px']
        cands = [f'{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{sz}-{m.group(3)}' for sz in sizes] + [src]
    data = None
    for attempt in range(4):
        for u in cands:
            # curl is used for the download: Wikimedia throttles Python's urllib far more aggressively
            p = __import__('subprocess').run(['curl', '-sS', '-f', '-L', '--max-time', '90', '-A', UA['User-Agent'], u],
                                             capture_output=True)
            if p.returncode == 0 and len(p.stdout) > 10000:
                data = p.stdout
                break
        if data:
            break
        __import__('time').sleep(5 * (attempt + 1))
    if not data:
        sys.exit('download failed (rate limited) — try again later or pick another image')
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    out = os.path.join(ROOT, 'assets/img/blog', stem + '.webp')
    im.save(out, 'WEBP', quality=80, method=6)
    creator = r.get('creator') or 'Unknown'
    lic = LICENSE_NAMES[r['license']]
    lic_url = r.get('license_url') or ''
    landing = r.get('foreign_landing_url') or src
    credit = f'Photo: <a href="{html.escape(landing)}" target="_blank" rel="noopener nofollow">{html.escape(r["title"][:80])}</a> by {html.escape(creator)}'
    credit += f', <a href="{html.escape(lic_url)}" target="_blank" rel="noopener nofollow">{lic}</a>' if lic_url else f', {lic}'
    cap = (html.escape(caption) + ' ') if caption else ''
    print(json.dumps({
        'file': f'/assets/img/blog/{stem}.webp', 'width': im.width, 'height': im.height,
        'figure': f'<figure><img src="/assets/img/blog/{stem}.webp" alt="{html.escape(alt)}" width="{im.width}" height="{im.height}" loading="lazy"><figcaption>{cap}<span class="credit">{credit}</span></figcaption></figure>',
    }, indent=1))


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'search':
        search(sys.argv[2:])
    elif len(sys.argv) >= 5 and sys.argv[1] == 'get':
        get(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else '')
    else:
        print(__doc__)
