#!/usr/bin/env python3
"""One-time importer: WordPress crawl -> public/content (posts.json + per-post HTML).

Usage: python3 tools/import_wp.py <crawl-dir-with-html/> <scores.json>
The crawl dir holds one saved HTML file per live URL (slug.html). Kept for the
record; the site no longer depends on WordPress.
"""
import json, os, re, sys, html, urllib.parse
from bs4 import BeautifulSoup, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
OUT = os.path.join(PUB, 'content')
crawl, scores_path = sys.argv[1], sys.argv[2]
scores = json.load(open(scores_path))
PAGES = {'_home', 'about-us', 'blog', 'category__general', 'contact-us', 'mindset',
         'privacy-policy', 'quotes', 'terms-of-use', 'blog__page__2'}
SITE = re.compile(r'^https?://(www\.)?thoughtchangerblog\.com')
KEEP_ATTR = {'a': {'href', 'rel', 'target', 'title'}, 'img': {'src', 'alt', 'width', 'height', 'srcset', 'sizes'},
             'td': {'colspan', 'rowspan'}, 'th': {'colspan', 'rowspan', 'scope'}, 'ol': {'start'}}


def local(url):
    if not url:
        return url
    return SITE.sub('', url) or '/'


def blogger_to_slug(url):
    m = re.match(r'^https?://(www\.)?thoughtchangerblog\.com/\d{4}/\d{2}/([^/?#]+)\.html', url)
    return m.group(2) if m else None


def parse_products(block):
    out = []
    for li in block.find_all('li'):
        a = li.find('a')
        if not a or 'amazon.' not in a.get('href', ''):
            continue
        q = urllib.parse.parse_qs(urllib.parse.urlparse(a['href']).query).get('k', [''])[0]
        title = a.get_text(' ', strip=True)
        rest = li.get_text(' ', strip=True)[len(title):].strip()
        by, blurb = '', rest
        m = re.match(r'^by\s+(.+?)\s+[—–-]\s+(.*)$', rest)
        if m:
            by, blurb = m.group(1), m.group(2)
        out.append({'title': title, 'by': by, 'blurb': blurb, 'q': q})
    return out


def clean(node, slugs):
    for c in node.find_all(string=lambda t: isinstance(t, Comment)):
        if not c.strip().startswith('tc:'):
            c.extract()
    for t in node.find_all(True):
        if t.name in ('h2', 'h3', 'h4') and t.get('id'):
            keep = {'id'}
        else:
            keep = KEEP_ATTR.get(t.name, set())
        cls = t.get('class') or []
        for a in list(t.attrs):
            if a not in keep:
                del t[a]
        if t.name == 'figure' and 'wp-block-table' in cls:
            t['class'] = 'table-wrap'
        if t.name == 'a':
            href = t.get('href', '')
            b = blogger_to_slug(href)
            if b:
                t['href'] = '/' + (b if b in slugs else '') + ('/' if b in slugs else '')
                if b not in slugs:
                    t['href'] = '/' + fuzzy(b, slugs) + '/'
            elif SITE.match(href):
                t['href'] = local(href)
            if 'amazon.' in t.get('href', ''):
                t['rel'] = 'sponsored nofollow noopener'
                t['target'] = '_blank'
        if t.name == 'img':
            t['src'] = local(t['src'])
            if t.get('srcset'):
                t['srcset'] = ', '.join(local(p.strip()) for p in t['srcset'].split(','))
            t['loading'] = 'lazy'
            t['decoding'] = 'async'
    return node


def fuzzy(s, slugs):
    import difflib
    m = difflib.get_close_matches(s, slugs, 1, 0.5)
    return m[0] if m else ''


def main():
    raw = {}
    for f in sorted(os.listdir(os.path.join(crawl, 'html'))):
        raw[f[:-5]] = open(os.path.join(crawl, 'html', f), encoding='utf-8').read()
    slugs = [k for k in raw if k not in PAGES]
    os.makedirs(os.path.join(OUT, 'posts'), exist_ok=True)
    posts, ids = [], {}
    for slug in slugs:
        soup = BeautifulSoup(raw[slug], 'lxml')
        meta = lambda p, a='property': (soup.find('meta', {a: p}) or {}).get('content') or ''
        sl = soup.find('link', rel='shortlink')
        if sl:
            ids[re.sub(r'\D', '', sl['href'])] = slug
        ld = json.loads(soup.find('script', type='application/ld+json').string)
        art = next(g for g in ld['@graph'] if g.get('@type') == 'Article')
        pc = soup.select_one('.elementor-widget-theme-post-content')
        for c in pc.find_all(string=lambda t: isinstance(t, Comment)):
            c.extract()
        products = []
        for blk in pc.select('.tc-recommended-reads'):
            products = parse_products(blk)
            blk.replace_with(BeautifulSoup('<!--tc:products-->', 'html.parser'))
        faq = []
        for blk in pc.select('.schema-faq'):
            for sec in blk.select('.schema-faq-section'):
                q = sec.select_one('.schema-faq-question').get_text(' ', strip=True)
                a = sec.select_one('.schema-faq-answer').decode_contents().strip()
                faq.append({'q': q, 'a': a})
            blk.replace_with(BeautifulSoup('<!--tc:faq-->', 'html.parser'))
        clean(pc, slugs)
        body = pc.decode_contents()
        body = re.sub(r'\n{3,}', '\n\n', body).strip()
        title_tag = html.unescape(soup.title.string)
        og = meta('og:image')
        img = soup.select_one('.elementor-widget-theme-post-featured-image img') or soup.select_one('.elementor-widget-image img[class*="wp-image"]')
        alt = ''
        for im in soup.select('.elementor-widget-image img'):
            if og and os.path.splitext(os.path.basename(og))[0] in (im.get('src') or ''):
                alt = im.get('alt', '')
        sc = scores.get(slug, {})
        posts.append({
            'slug': slug,
            'id': int(re.sub(r'\D', '', sl['href'])) if sl else None,
            'title': soup.find('h1').get_text(' ', strip=True),
            'seo_title': title_tag,
            'description': html.unescape(meta('description', 'name')),
            'published': meta('article:published_time'),
            'modified': meta('article:modified_time'),
            'image': local(og),
            'image_alt': alt or soup.find('h1').get_text(' ', strip=True),
            'categories': art.get('articleSection', []) or ['General'],
            'words': art.get('wordCount'),
            'status': 'kept' if sc.get('keep') else 'rewrite',
            'products': products,
            'faq': faq,
        })
        # Rewritten posts are owned by tools/rewrites/ — never overwrite them.
        if sc.get('keep') or not os.path.exists(os.path.join(OUT, 'posts', slug + '.html')):
            open(os.path.join(OUT, 'posts', slug + '.html'), 'w').write(body + '\n')
    posts.sort(key=lambda p: p['published'], reverse=True)
    json.dump(posts, open(os.path.join(OUT, 'posts.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(ids, open(os.path.join(OUT, 'legacy-ids.json'), 'w'), indent=1)
    print(len(posts), 'posts;', sum(p['status'] == 'kept' for p in posts), 'kept')


main()
