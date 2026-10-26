#!/usr/bin/env python3
"""One-time migration of the old houstonapartments.com WordPress content.

Pulls every post and page from the public WP REST API, cleans the HTML,
rewrites absolute links to root-relative ones, downloads every referenced
upload to public/wp-content/uploads/ (same paths, so old image URLs keep
resolving) and writes public/app/content/{posts,pages}.json.

    python3 tools/migrate_wp.py            # content + images
    python3 tools/migrate_wp.py --no-media # content only
"""
import concurrent.futures as cf
import html
import json
import os
import re
import sys
import urllib.request

SRC = 'https://houstonapartments.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
OUT = os.path.join(PUB, 'app', 'content')
UA = {'User-Agent': 'Mozilla/5.0 (HoustonApartments migration)'}
UPLOAD_RE = re.compile(r'https?://(?:www\.)?houstonapartments\.com(/wp-content/uploads/[^"\'\s)>,]+)')


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fetch_all(kind):
    items, page = [], 1
    while True:
        data = json.loads(get(f'{SRC}/wp-json/wp/v2/{kind}?per_page=100&page={page}&_embed=wp:featuredmedia,wp:term'))
        items += data
        if len(data) < 100:
            return items
        page += 1


def clean(c):
    c = re.sub(r'\s(srcset|sizes|decoding|loading|fetchpriority)="[^"]*"', '', c)
    c = re.sub(r'<p>\s*(&nbsp;)?\s*</p>', '', c)
    c = re.sub(r'<div style="height:\d+px" aria-hidden="true" class="wp-block-spacer"></div>', '', c)
    # Inline <script>/<form> blocks from old plugins don't belong in migrated copy
    c = re.sub(r'<script\b.*?</script>', '', c, flags=re.S)
    c = re.sub(r'<form\b.*?</form>', '', c, flags=re.S)
    c = re.sub(r'https?://(?:www\.)?houstonapartments\.com(/[^"\']*)', r'\1', c)
    return c.strip()


def media_path(url):
    m = UPLOAD_RE.match(url)
    return m.group(1) if m else None


def main():
    os.makedirs(OUT, exist_ok=True)
    media = set()
    out = {}
    for kind in ('posts', 'pages'):
        rows = []
        for x in fetch_all(kind):
            raw = x['content']['rendered']
            media |= {m for m in UPLOAD_RE.findall(raw)}
            y = x.get('yoast_head_json') or {}
            fm = (x.get('_embedded') or {}).get('wp:featuredmedia') or [{}]
            img = fm[0].get('source_url', '')
            if img:
                media.add(media_path(img))
            terms = [t['name'] for grp in (x.get('_embedded') or {}).get('wp:term', []) for t in grp if t.get('taxonomy') == 'category']
            rows.append({
                'id': x['id'],
                'slug': x['slug'],
                'path': re.sub(r'https?://[^/]+', '', x['link']),
                'title': html.unescape(x['title']['rendered']),
                'seo_title': html.unescape(y.get('title') or ''),
                'description': html.unescape(y.get('description') or y.get('og_description') or ''),
                'date': x['date'],
                'modified': x['modified'],
                'excerpt': html.unescape(re.sub(r'<[^>]+>', '', x.get('excerpt', {}).get('rendered', ''))).strip(),
                'image': media_path(img) or '',
                'image_alt': fm[0].get('alt_text', ''),
                'categories': terms,
                'content': clean(raw),
            })
        rows.sort(key=lambda r: r['date'], reverse=True)
        out[kind] = rows
        with open(os.path.join(OUT, f'{kind}.json'), 'w') as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print(kind, len(rows))

    media.discard(None)
    # srcset variants were stripped; fetch the size actually referenced plus the original
    extra = {re.sub(r'-\d+x\d+(\.\w+)$', r'\1', m) for m in media}
    media |= extra
    if '--no-media' in sys.argv:
        return

    def dl(p):
        dest = os.path.join(PUB, p.lstrip('/'))
        if os.path.exists(dest):
            return 'skip'
        try:
            data = get(SRC + p)
        except Exception as e:  # noqa: BLE001 - report and continue
            return f'fail {p} {e}'
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(data)
        return 'ok'

    with cf.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(dl, sorted(media)))
    print('media', len(media), {k: sum(1 for r in res if r.startswith(k)) for k in ('ok', 'skip', 'fail')})
    for r in res:
        if r.startswith('fail'):
            print(r)


if __name__ == '__main__':
    main()
