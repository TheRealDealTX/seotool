#!/usr/bin/env python3
"""One-off importer: WordPress REST export -> app/content/posts/<slug>.php.

Reads backup/wordpress-2026-11-19/api/{posts,media}.json and tools/slugmap.tsv,
cleans each post body down to semantic HTML, copies its images into
public_html/assets/img/blog/ as WebP, rewrites internal links to the new URLs,
and writes app/data/legacy-media.php (old upload URL -> new image path) so the
router can 301 every image URL the WordPress site ever exposed.

Re-running is safe; it overwrites its own output. Run from the site root:
    python3 tools/import_wp.py
"""
import html
import json
import os
import re
from html.parser import HTMLParser
from io import BytesIO
from urllib.parse import urlparse

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BK = os.path.join(ROOT, 'backup', 'wordpress-2026-11-19')
POSTS_OUT = os.path.join(ROOT, 'app', 'content', 'posts')
IMG_OUT = os.path.join(ROOT, 'public_html', 'assets', 'img', 'blog')
DOMAIN = 'seattlenorthwesthomes.com'

PAGE_MAP = {
    '': '/', 'about-us': '/about-seattle-northwest-homes/', 'buying': '/buy-a-home-in-seattle/',
    'selling': '/sell-your-home-seattle/', 'contact-us': '/contact-seattle-real-estate-agents/',
    'blog': '/blog/', 'privacy-policy': '/privacy-policy/', 'category/articles': '/blog/',
}

ALLOWED = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'blockquote', 'table',
           'thead', 'tbody', 'tr', 'th', 'td', 'figure', 'figcaption', 'img', 'br', 'hr'}
RENAME = {'b': 'strong', 'i': 'em', 'h1': 'h2', 'h5': 'h4', 'h6': 'h4'}
VOID = {'img', 'br', 'hr'}

slugmap = {}
for line in open(os.path.join(ROOT, 'tools', 'slugmap.tsv')):
    old, new, cat = line.rstrip('\n').split('\t')
    slugmap[old] = (new, cat)

# Hand-written meta descriptions (WordPress only had truncated excerpts).
DESCRIPTIONS = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(ROOT, 'tools', 'descriptions.tsv')))

SEO_TITLES = dict(l.rstrip('\n').split('\t') for l in open(os.path.join(ROOT, 'tools', 'seo-titles.tsv')))

media_by_id = {m['id']: m for m in json.load(open(os.path.join(BK, 'api', 'media.json')))}
legacy_media = {}   # '/wp-content/uploads/...' -> '/assets/img/blog/x.webp'


def local_media_file(url):
    name = os.path.basename(urlparse(url).path)
    p = os.path.join(BK, 'media', name)
    if os.path.exists(p):
        return p
    # size variants like foo-300x200.jpg -> foo.jpg / foo-scaled.jpg
    base = re.sub(r'-\d+x\d+(?=\.\w+$)', '', name)
    for cand in (base, re.sub(r'(\.\w+)$', r'-scaled\1', base)):
        p = os.path.join(BK, 'media', cand)
        if os.path.exists(p):
            return p
    return None


def convert_image(url):
    """Copy an uploaded image into assets/img/blog as webp; return (path, w, h) or None."""
    src = local_media_file(url)
    if not src:
        return None
    stem = os.path.splitext(os.path.basename(src))[0].replace('-scaled', '').lower()
    stem = re.sub(r'[^a-z0-9-]+', '-', stem).strip('-')
    dest = os.path.join(IMG_OUT, stem + '.webp')
    im = Image.open(src)
    im = im.convert('RGB')
    im.thumbnail((1400, 1400))
    if not os.path.exists(dest):
        im.save(dest, quality=74, method=6)
        sm = im.copy()
        sm.thumbnail((720, 720))
        sm.save(os.path.join(IMG_OUT, stem + '-sm.webp'), quality=72, method=6)
    web = '/assets/img/blog/' + stem + '.webp'
    legacy_media[urlparse(url).path] = web
    return web, im.size[0], im.size[1]


def rewrite_href(href):
    u = urlparse(href)
    if u.netloc and u.netloc.replace('www.', '') != DOMAIN:
        return href
    if not u.netloc and not href.startswith('/'):
        return href
    path = u.path.strip('/')
    if path.startswith('wp-content/'):
        return href
    if path in slugmap:
        return '/blog/' + slugmap[path][0] + '/'
    if path in PAGE_MAP:
        return PAGE_MAP[path]
    return '/' + (path + '/' if path else '')


class Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        tag = RENAME.get(tag, tag)
        if tag not in ALLOWED:
            self.stack.append(None)
            return
        a = dict(attrs)
        keep = []
        if tag == 'a':
            href = a.get('href') or ''
            if not href:
                self.stack.append(None)
                return
            new = rewrite_href(href)
            keep.append(('href', new))
            if not new.startswith('/'):
                keep.append(('target', '_blank'))
                keep.append(('rel', 'noopener'))
        elif tag == 'img':
            src = a.get('src') or ''
            conv = convert_image(src) if 'wp-content/uploads' in src else None
            if not conv:
                return
            keep += [('src', conv[0]), ('alt', a.get('alt') or ''), ('width', str(conv[1])),
                     ('height', str(conv[2])), ('loading', 'lazy'), ('decoding', 'async')]
        elif tag in ('td', 'th'):
            for k in ('colspan', 'rowspan'):
                if a.get(k):
                    keep.append((k, a[k]))
        attr = ''.join(' %s="%s"' % (k, html.escape(v, quote=True)) for k, v in keep)
        self.out.append('<%s%s>' % (tag, attr))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        tag = RENAME.get(tag, tag)
        if tag not in VOID and self.stack:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = RENAME.get(tag, tag)
        if tag in VOID:
            return
        if not self.stack:
            return
        t = self.stack.pop()
        if t:
            self.out.append('</%s>' % t)

    def handle_data(self, data):
        self.out.append(data)

    def handle_entityref(self, name):
        self.out.append('&%s;' % name)

    def handle_charref(self, name):
        self.out.append('&#%s;' % name)

    def handle_comment(self, data):
        pass


def clean(body):
    body = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    body = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', '', body, flags=re.S | re.I)
    c = Cleaner()
    c.feed(body)
    c.close()
    out = ''.join(c.out)
    out = out.replace('&nbsp;', ' ').replace('\xa0', ' ')
    for _ in range(3):
        out = re.sub(r'<(p|strong|em|li|h2|h3|h4|figure|figcaption)>\s*</\1>', '', out)
    out = re.sub(r'<p>\s*(<img [^>]+>)\s*</p>', r'<figure>\1</figure>', out)
    # <li><p>x</p></li> -> <li>x</li>; bold wrappers inside headings are redundant
    out = re.sub(r'<li>\s*<p>(.*?)</p>\s*</li>', r'<li>\1</li>', out, flags=re.S)
    out = re.sub(r'<(h[234])>\s*(.*?)\s*</\1>', lambda m: '<%s>%s</%s>' % (m.group(1), re.sub(r'</?strong>', '', m.group(2)), m.group(1)), out, flags=re.S)
    out = re.sub(r'<li>\s+', '<li>', out)
    out = re.sub(r'\s+</li>', '</li>', out)
    out = re.sub(r'\n\s*\n+', '\n', out).strip()
    # block-level tags on their own lines for readable source
    out = re.sub(r'\s*(<(?:p|h2|h3|h4|ul|ol|li|blockquote|table|thead|tbody|tr|figure)[ >])', r'\n\1', out).strip()
    return out


def text(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def describe(p):
    y = p.get('yoast_head_json') or {}
    d = y.get('description') or y.get('og_description') or ''
    if not d or len(d) < 70:
        d = text(p['excerpt']['rendered']).replace(' [ …]', '').replace('[…]', '')
    d = d.replace('[…]', '').strip()
    if len(d) > 158:
        d = d[:155].rsplit(' ', 1)[0].rstrip(',;:—-') + '…'
    return d


def php_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def main():
    os.makedirs(POSTS_OUT, exist_ok=True)
    os.makedirs(IMG_OUT, exist_ok=True)
    posts = json.load(open(os.path.join(BK, 'api', 'posts.json')))
    for p in posts:
        new, cat = slugmap[p['slug']]
        title = text(p['title']['rendered'])
        img = alt = ''
        fm = media_by_id.get(p['featured_media'])
        if fm:
            conv = convert_image(fm['source_url'])
            if conv:
                img = os.path.basename(conv[0])
                alt = text(fm.get('alt_text') or '') or title
        body = clean(p['content']['rendered'])
        desc = DESCRIPTIONS.get(new) or describe(p)
        if '<<<' in body or '\nHTML' in body:
            raise SystemExit('heredoc clash in ' + new)
        words = len(text(body).split())
        src = (
            "<?php defined('SNW') || (http_response_code(404) && exit);\n"
            "// Imported from WordPress: /%s/ (%d words)\n"
            "return [\n"
            "    'title'       => %s,\n"
            "    'slug'        => %s,\n"
            "    'legacy_slug' => %s,\n"
            "    'description' => %s,\n"
            "    'keyword'     => %s,\n"
            "    'category'    => %s,\n"
            "    'date'        => %s,\n"
            "    'modified'    => %s,\n"
            "    'image'       => %s,\n"
            "    'image_alt'   => %s,\n"
            "    'faq'         => [],\n"
            "    'body'        => <<<'HTML'\n%s\nHTML,\n"
            "];\n"
        ) % (p['slug'], words, php_str(title), php_str(new), php_str(p['slug']), php_str(desc),
             php_str(new.replace('-', ' ')), php_str(cat), php_str(p['date'][:10]),
             php_str(p['modified'][:10]), php_str(img), php_str(alt), body)
        if new in SEO_TITLES:
            src = src.replace("\n    'slug'        =>", "\n    'seo_title'   => " + php_str(SEO_TITLES[new]) + ",\n    'slug'        =>", 1)
        open(os.path.join(POSTS_OUT, new + '.php'), 'w').write(src)
    # every attachment, not just those used in posts, so old image URLs keep resolving
    for m in media_by_id.values():
        convert_image(m['source_url'])
        for size in (m.get('media_details') or {}).get('sizes', {}).values():
            if size.get('source_url'):
                legacy_media[urlparse(size['source_url']).path] = legacy_media.get(
                    urlparse(m['source_url']).path, '/')
    lines = ["<?php defined('SNW') || (http_response_code(404) && exit);", '// Generated by tools/import_wp.py: old WordPress upload path => new image.', 'return [']
    for k in sorted(legacy_media):
        lines.append('    %s => %s,' % (php_str(k), php_str(legacy_media[k])))
    lines.append('];')
    open(os.path.join(ROOT, 'app', 'data', 'legacy-media.php'), 'w').write('\n'.join(lines) + '\n')
    print('posts', len(posts), 'media map', len(legacy_media))


if __name__ == '__main__':
    main()
