"""Mirror coveragestimate.com (WordPress/Elementor output) into a static tree.

Downloads each page's final HTML plus every same-origin asset it references
(CSS, JS, fonts, images, srcset variants, CSS url() targets, Elementor webpack
chunks), keeping the original paths so every URL stays identical.

usage: python3 mirror.py OUT_DIR [extra_asset_list.txt]
"""
import os, re, sys, json, urllib.request, urllib.parse, concurrent.futures, html

ORIGIN = 'https://coveragestimate.com'
HOST = 'coveragestimate.com'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
OUT = os.path.abspath(sys.argv[1])
RAW = os.path.join(OUT, '_raw')          # untouched downloads (pages)
WEB = os.path.join(OUT, 'public_html')   # deployable tree

PAGES = [l.strip().replace(ORIGIN, '') or '/' for l in open(os.path.join(os.path.dirname(__file__), 'urls.txt')) if l.strip()]
EXTRA_PAGES = ['/category/general/']
FEEDS = ['/feed/', '/comments/feed/', '/category/tools/feed/']
ROOT_FILES = ['/robots.txt', '/sitemap_index.xml', '/post-sitemap.xml', '/page-sitemap.xml', '/category-sitemap.xml',
              '/main-sitemap.xsl', '/favicon.ico']

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read(), r.headers.get('Content-Type', '')

def fetch_status(url):
    try:
        return fetch(url)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get('Content-Type', '')

def local_path(path):
    path = urllib.parse.unquote(path.split('?')[0].split('#')[0])
    if path.endswith('/'):
        path += 'index.html'
    return os.path.join(WEB, path.lstrip('/'))

URL_RE = re.compile(r'''(?:https?:)?(?:\\?/\\?/)(?:www\.)?coveragestimate\.com((?:\\?/[^\s"'<>()\\]*)*)''')
REL_RE = re.compile(r'''["'(\s,](/(?:wp-content|wp-includes)/[^\s"'<>()]+)''')

def asset_paths_from_text(text):
    found = set()
    for m in URL_RE.finditer(text):
        p = m.group(1).replace('\\/', '/')
        if p:
            found.add(p)
    for m in REL_RE.finditer(text):
        found.add(m.group(1))
    out = set()
    for p in found:
        p = html.unescape(p).split('#')[0]
        clean = p.split('?')[0]
        if re.search(r'\.(css|js|mjs|png|jpe?g|gif|webp|avif|svg|ico|woff2?|ttf|otf|eot|json|xsl|mp4|webm|pdf)$', clean, re.I):
            out.add(clean)
    return out

def css_refs(css_text, css_path):
    refs = set()
    for m in re.finditer(r'url\(\s*([\'"]?)([^\'")]+)\1\s*\)', css_text):
        u = m.group(2).strip()
        if u.startswith('data:') or u.startswith('#'):
            continue
        full = urllib.parse.urljoin(ORIGIN + css_path, u)
        pu = urllib.parse.urlparse(full)
        if pu.netloc.replace('www.', '') == HOST:
            refs.add(pu.path)
    for m in re.finditer(r'@import\s+(?:url\()?\s*[\'"]([^\'"]+)', css_text):
        full = urllib.parse.urljoin(ORIGIN + css_path, m.group(1))
        pu = urllib.parse.urlparse(full)
        if pu.netloc.replace('www.', '') == HOST:
            refs.add(pu.path)
    return refs

downloaded, failed = set(), {}

def download_asset(path):
    if path in downloaded:
        return set()
    downloaded.add(path)
    dest = local_path(path)
    try:
        status, body, ctype = fetch_status(ORIGIN + urllib.parse.quote(path))
    except Exception as e:  # network error
        failed[path] = str(e)
        return set()
    if status != 200:
        failed[path] = status
        return set()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f:
        f.write(body)
    more = set()
    if path.endswith('.css'):
        more |= css_refs(body.decode('utf-8', 'replace'), path)
    if path.endswith('.js'):
        more |= webpack_chunks(body.decode('utf-8', 'replace'), path)
    return more

def webpack_chunks(js, path):
    """Elementor's webpack runtimes map chunk ids to file names; fetch them all."""
    if 'webpack' not in path and 'runtime' not in path:
        return set()
    base = path.rsplit('/', 1)[0] + '/'
    names = set()
    # pattern: e+"."+{id:"hash",...}[e]+".bundle.min.js" with a separate {id:"name"} map
    m_names = re.search(r'\(\{([^{}]*)\}\[e\]\|\|e\)\s*\+\s*"\."\s*\+\s*\{([^{}]*)\}\[e\]\s*\+\s*"(\.bundle(?:\.min)?\.js)"', js)
    if m_names:
        nmap = dict(re.findall(r'(\d+|"[^"]+"):"([^"]+)"', m_names.group(1)))
        hmap = dict(re.findall(r'(\d+|"[^"]+"):"([^"]+)"', m_names.group(2)))
        for k, h in hmap.items():
            names.add(base + nmap.get(k, k.strip('"')) + '.' + h + m_names.group(3))
    return names

def crawl_assets(seed):
    todo = set(seed)
    while todo:
        batch = [p for p in todo if p not in downloaded]
        todo = set()
        with concurrent.futures.ThreadPoolExecutor(12) as ex:
            for more in ex.map(download_asset, batch):
                todo |= more

def main():
    os.makedirs(RAW, exist_ok=True)
    seeds, report = set(), {}
    for path in PAGES + EXTRA_PAGES:
        status, body, ctype = fetch_status(ORIGIN + path)
        report[path] = status
        rawf = os.path.join(RAW, (path.strip('/').replace('/', '__') or 'home') + '.html')
        open(rawf, 'wb').write(body)
        seeds |= asset_paths_from_text(body.decode('utf-8', 'replace'))
    status, body, _ = fetch_status(ORIGIN + '/this-page-does-not-exist-ce404/')
    report['404'] = status
    open(os.path.join(RAW, '__404.html'), 'wb').write(body)
    seeds |= asset_paths_from_text(body.decode('utf-8', 'replace'))
    for path in FEEDS + ROOT_FILES:
        status, body, ctype = fetch_status(ORIGIN + path)
        report[path] = status
        if status == 200:
            name = path.strip('/').replace('/', '__') or 'root'
            open(os.path.join(RAW, name + ('.xml' if 'feed' in path else '')), 'wb').write(body)
    if len(sys.argv) > 2:
        seeds |= {l.strip() for l in open(sys.argv[2]) if l.strip()}
    crawl_assets(seeds)
    json.dump({'pages': report, 'assets': sorted(downloaded), 'failed': failed}, open(os.path.join(OUT, 'mirror_report.json'), 'w'), indent=1)
    print('pages', len(report), 'assets', len(downloaded), 'failed', len(failed))
    for k, v in list(failed.items())[:40]:
        print('  FAIL', v, k)

if __name__ == '__main__':
    main()
