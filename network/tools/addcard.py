#!/usr/bin/env python3
"""Insert a listing card and a sitemap entry for a post.
Usage (repo root): python3 -I network/tools/addcard.py <domain> <new-slug> <reference-slug>
The reference slug is an already-listed post whose card is cloned (normally last week's post)."""
import re, sys, glob, html, datetime
LISTING = {'hatetolovethesplit.com': ['home.html', 'index.html'], 'agadecor.com': ['blog/index.html'], 'ohmtoherminediy.com': ['blog/index.html'],
           'fraserandmorris.com': ['blog/index.html'], 'rjbledlcdtvservicecentre.com': ['home.html', 'index.html'], 'asmith.photography': ['journal/index.html'],
           'michellewhitephoto.com': ['blog/index.html'], 'comeicavoliamerenda.com': ['home.html', 'index.html'], 'findsforfitness.com': ['blog/index.html']}

def fm_of(d, slug):
    t = open(f'network/sites/{d}/posts/{slug}.md').read(); m = re.match(r'---\n(.*?)\n---', t, re.S); fm = {}
    for line in m.group(1).splitlines():
        k, v = line.split(':', 1); fm[k.strip()] = v.strip().strip('"')
    return fm

def find_card(s, slug):
    for tag in ['article', 'a']:
        pat = re.compile(r'<(/?)%s\b[^>]*>' % tag)
        for m in re.finditer(r'<%s\b[^>]*>' % tag, s):
            depth = 0
            for mm in pat.finditer(s, m.start()):
                depth += -1 if mm.group(1) else 1
                if depth == 0:
                    blk = s[m.start():mm.end()]
                    if slug in blk and len(blk) < 4000: return m.start(), mm.end(), blk
                    break
    return None

def main(d, new, ref):
    f1 = fm_of(d, ref); f2 = fm_of(d, new)
    t1 = html.escape(f1['title'], quote=False); t2 = html.escape(f2['title'], quote=False)
    d1 = html.escape(f1['description'], quote=False); d2 = html.escape(f2['description'], quote=False)
    p1 = f1['path'].rstrip('/'); p2 = f2['path'].rstrip('/')
    date1 = datetime.date.fromisoformat(f1['date']); date2 = datetime.date.fromisoformat(f2['date'])
    for lf in LISTING[d]:
        path = f'network/sites/{d}/live/{lf}'; s = open(path).read()
        if p2 + '/' in s or p2 + '"' in s: print('already listed', d, lf); continue
        r = find_card(s, ref)
        if not r: print('NO CARD for', ref, 'in', lf); continue
        st, en, blk = r; n = blk
        n = n.replace(p1 + '/', p2 + '/').replace(p1 + '"', p2 + '"')
        n = n.replace(t1, t2).replace(d1, d2)
        n = n.replace(html.escape(f1['title'], quote=True), html.escape(f2['title'], quote=True))
        n = n.replace(f1['date'], f2['date'])
        for fmt in ('%B %-d, %Y', '%-d %B %Y', '%B %Y'):
            n = n.replace(date1.strftime(fmt), date2.strftime(fmt))
        if 'image' in f1 and 'image' in f2 and f1['image'] != f2['image']:
            b1 = f1['image'].replace('.webp', ''); b2 = f2['image'].replace('.webp', '')
            n = n.replace(b1, b2)
        if 'category' in f1 and 'category' in f2 and f1['category'] != f2['category']:
            n = n.replace('>' + html.escape(f1['category']) + '<', '>' + html.escape(f2['category']) + '<')
        if 'data-text="' in n:
            n = re.sub(r'data-text="[^"]*"', 'data-text="' + html.escape((f2['title'] + ' ' + f2['description']).lower(), quote=True) + '"', n)
        if n == blk: print('UNCHANGED clone', d, lf); continue
        open(path, 'w').write(s[:st] + n + '\n' + s[st:]); print('inserted', d, lf)
    sm = f'network/sites/{d}/live/sitemap.xml'; x = open(sm).read(); loc = f'https://{d}{f2["path"]}'
    if loc not in x:
        sample = re.search(r'<url>.*?</url>', x, re.S).group(0)
        e = re.sub(r'<image:image>.*?</image:image>', '', sample, flags=re.S)
        e = re.sub(r'<loc>[^<]*</loc>', f'<loc>{loc}</loc>', e); e = re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{f2["date"]}</lastmod>', e)
        e = re.sub(r'<priority>[^<]*</priority>', '<priority>0.7</priority>', e); e = re.sub(r'<changefreq>[^<]*</changefreq>', '<changefreq>monthly</changefreq>', e)
        i = x.rfind('</urlset>'); open(sm, 'w').write(x[:i] + e + '\n' + x[i:]); print('sitemap +', loc)

if __name__ == '__main__':
    main(*sys.argv[1:4])
