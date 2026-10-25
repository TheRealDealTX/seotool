"""Turn the raw mirror (out/_raw) into the deployable tree (out/public_html).

- Pages keep their exact paths: /about-us/ -> about-us/index.html
- Same-site URLs become root-relative so the site works on any host
  (temporary domain now, coveragestimate.com later), EXCEPT where an absolute
  URL is required for SEO: canonical, og:/twitter: meta, JSON-LD, sitemaps, feeds.
- WordPress-only head tags (REST API, oEmbed, RSD/xmlrpc) are removed.
- Copies the PHP/htaccess layer from ./server into the tree.

usage: python3 build_static.py OUT_DIR
"""
import os, re, sys, shutil, json

OUT = os.path.abspath(sys.argv[1])
RAW = os.path.join(OUT, '_raw')
WEB = os.path.join(OUT, 'public_html')
HERE = os.path.dirname(os.path.abspath(__file__))

SITE_RE = re.compile(r'(?:https?:)?(\\?/\\?/)(?:www\.)?coveragestimate\.com(?=([\\/"\'?#\s)<,]|$))')

def relativize(text):
    def sub(m):
        slash = m.group(1)
        nxt = m.group(2)
        escaped = '\\' in slash
        if nxt in ('/', '\\'):
            return ''                       # "https://site/x" -> "/x"
        return '\\/' if escaped else '/'    # "https://site" -> "/"
    return SITE_RE.sub(sub, text)

PROTECT = [
    re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I),
    re.compile(r'<meta[^>]+(?:property|name)=["\'](?:og:|twitter:|article:)[^>]*>', re.I),
    re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', re.I | re.S),
    re.compile(r'<link[^>]+type=["\']application/rss\+xml["\'][^>]*>', re.I),
]
REMOVE = [
    re.compile(r'<link[^>]+rel=["\']https://api\.w\.org/["\'][^>]*>\s*', re.I),
    re.compile(r'<link[^>]+type=["\']application/json["\'][^>]*wp-json[^>]*>\s*', re.I),
    re.compile(r'<link[^>]+rel=["\']EditURI["\'][^>]*>\s*', re.I),
    re.compile(r'<link[^>]+type=["\'](?:application/json\+oembed|text/xml\+oembed)["\'][^>]*>\s*', re.I),
    re.compile(r'<link[^>]+rel=["\']wlwmanifest["\'][^>]*>\s*', re.I),
]

ATTR_RE = re.compile(r'(\s(?:href|src|srcset|action|poster|style|data-[\w-]+)=["\'])([^"\']*)(["\'])', re.I)
BLOCK_RE = re.compile(r'(<(?:script|style)\b[^>]*>)(.*?)(</(?:script|style)>)', re.I | re.S)

def process_html(text):
    for rx in REMOVE:
        text = rx.sub('', text)
    keep = {}
    def stash(m):
        key = '\x00CE%d\x00' % len(keep)
        keep[key] = m.group(0)
        return key
    for rx in PROTECT:
        text = rx.sub(stash, text)
    # Only rewrite inside attributes, <style> and <script> blocks; never visible text.
    text = ATTR_RE.sub(lambda m: m.group(1) + relativize(m.group(2)) + m.group(3), text)
    text = BLOCK_RE.sub(lambda m: m.group(1) + relativize(m.group(2)) + m.group(3), text)
    for k, v in keep.items():
        text = text.replace(k, v)
    return text

def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'wb' if isinstance(data, bytes) else 'w'
    with open(path, mode) as f:
        f.write(data)

def main():
    report = json.load(open(os.path.join(OUT, 'mirror_report.json')))
    pages = [p for p in report['pages'] if p.startswith('/') and p.endswith('/') and 'feed' not in p]
    for p in pages:
        name = (p.strip('/').replace('/', '__') or 'home') + '.html'
        text = open(os.path.join(RAW, name), encoding='utf-8').read()
        write(os.path.join(WEB, p.lstrip('/'), 'index.html'), process_html(text))
    # pages are served by index.php from ce-pages/ (see server/index.php)
    for p in pages:
        src = os.path.join(WEB, p.lstrip('/'), 'index.html')
        dst = os.path.join(WEB, 'ce-pages', 'home.html') if p == '/' else os.path.join(WEB, 'ce-pages', p.strip('/'), 'index.html')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.replace(src, dst)
        d = os.path.dirname(src)
        while d != WEB and os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)
            d = os.path.dirname(d)
    write(os.path.join(WEB, '404.html'), process_html(open(os.path.join(RAW, '__404.html'), encoding='utf-8').read()))
        # feeds are served by index.php from ce-feeds/ (no /feed/ directory, so it works without .htaccess)
    for f in ('feed', 'comments__feed', 'category__tools__feed'):
        src = os.path.join(RAW, f + '.xml')
        if os.path.exists(src):
            write(os.path.join(WEB, 'ce-feeds', f.replace('__', '-') + '.xml'), open(src, 'rb').read())
    # root files (absolute URLs kept: sitemaps must list the real domain)
    for f in ('robots.txt', 'sitemap_index.xml', 'post-sitemap.xml', 'page-sitemap.xml', 'category-sitemap.xml', 'main-sitemap.xsl', 'favicon.ico'):
        src = os.path.join(RAW, f)
        if os.path.exists(src):
            data = open(src, 'rb').read()
            if f.endswith('.xml'):
                # the XSL reference must load from whichever host serves the sitemap
                data = data.replace(b'//coveragestimate.com/main-sitemap.xsl', b'/main-sitemap.xsl')
            write(os.path.join(WEB, f), data)
    # CSS files may contain absolute self-references
    for root, _, files in os.walk(os.path.join(WEB, 'wp-content')):
        for fn in files:
            if fn.endswith(('.css', '.js')):
                fp = os.path.join(root, fn)
                t = open(fp, encoding='utf-8', errors='surrogateescape').read()
                n = relativize(t)
                if n != t:
                    open(fp, 'w', encoding='utf-8', errors='surrogateescape').write(n)
    # server layer (.htaccess, PHP form handler, router)
    srv = os.path.join(HERE, 'server')
    for root, _, files in os.walk(srv):
        for fn in files:
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, srv)
            write(os.path.join(WEB, rel), open(src, 'rb').read())
    print('built', len(pages), 'pages')

if __name__ == '__main__':
    main()
