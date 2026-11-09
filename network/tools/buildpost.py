#!/usr/bin/env python3
"""Build network/sites/<domain>/live<path> from posts/<slug>.md and the site's template.html.
Usage (repo root): python3 -I network/tools/buildpost.py <domain> [<domain> ...]"""
import re, sys, os, html, datetime, json

CFG = {
 'hatetolovethesplit.com':      dict(date='%B %-d, %Y', lead='lead',    img='/assets/img/paint-roller.webp'),
 'agadecor.com':                dict(date='%B %-d, %Y', lead='dropcap', img='/assets/img/hero-aisle.webp'),
 'ohmtoherminediy.com':         dict(date='%B %-d, %Y', lead=None,      img='/assets/img/plants-shelf.webp'),
 'fraserandmorris.com':         dict(date='%-d %B %Y',  lead='lead',    img='/assets/img/dahlias.webp'),
 'rjbledlcdtvservicecentre.com':dict(date='%B %-d, %Y', lead=None,      img='/assets/img/soldering-board.webp'),
 'asmith.photography':          dict(date='%B %-d, %Y', lead=None,      img='/assets/img/nike-sb.webp'),
 'michellewhitephoto.com':      dict(date='%B %Y',      lead=None,      img='/assets/img/lake-couple.webp'),
 'comeicavoliamerenda.com':     dict(date='%B %-d, %Y', lead=None,      img='/assets/img/diamond-studs.webp'),
 'findsforfitness.com':         dict(date='%B %-d, %Y', lead=None,      img='/assets/img/runners-at-sunrise.webp'),
}
FFF_CATS = {'Workouts': '/category/workout/', 'Health Tips': '/category/health-tips/', 'Gear Guides': '/category/product-reviews/',
            'Weight Loss': '/category/weight_loss/', 'Skin Care': '/category/skin_care/'}

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:60]

def parse_md(text):
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S); fm = {}
    for line in m.group(1).splitlines():
        k, v = line.split(':', 1); fm[k.strip()] = v.strip().strip('"')
    return fm, m.group(2)

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}"{" rel=\"noopener\" target=\"_blank\"" if m.group(2).startswith("http") else ""}>{m.group(1)}</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', s)
    return s

def md2html(md, lead_class):
    out = []; lines = md.strip().splitlines(); i = 0; h2s = []; first_p = True
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith('## '):
            t = l[3:].strip(); sid = slug(t); h2s.append((sid, t)); out.append(f'<h2 id="{sid}">{inline(t)}</h2>'); i += 1; continue
        if l.startswith('### '): out.append(f'<h3>{inline(l[4:])}</h3>'); i += 1; continue
        if l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'): rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            rows = [r for r in rows if not all(re.match(r'^:?-+:?$', c) for c in r)]
            head = '<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in rows[0]) + '</tr></thead>'
            body = '<tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody>'
            out.append(f'<table>{head}{body}</table>'); continue
        if re.match(r'^\d+\. ', l):
            items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]): items.append(re.sub(r'^\d+\. ', '', lines[i])); i += 1
            out.append('<ol>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ol>'); continue
        if l.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '): items.append(lines[i][2:]); i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue
        para = [l]; i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('## ', '### ', '- ', '|')) and not re.match(r'^\d+\. ', lines[i]): para.append(lines[i]); i += 1
        cls = f' class="{lead_class}"' if (first_p and lead_class) else ''
        first_p = False
        out.append(f'<p{cls}>{inline(" ".join(para))}</p>')
    return '\n'.join(out), h2s

def category_url(domain, cat):
    if domain == 'findsforfitness.com': return FFF_CATS.get(cat, '/blog/')
    if domain in ('hatetolovethesplit.com', 'ohmtoherminediy.com'):
        u = f'/category/{slug(cat)}/'
        return u if os.path.isdir(f'network/sites/{domain}/live{u}') else ('/blog/' if domain == 'ohmtoherminediy.com' else '/archives/')
    if domain == 'comeicavoliamerenda.com': return '/earring-guides/'
    if domain == 'agadecor.com': return '/blog/'
    if domain == 'asmith.photography': return f'/journal#{slug(cat)}'
    if domain == 'michellewhitephoto.com': return '/blog/'
    if domain == 'fraserandmorris.com': return '/blog/'
    return '/'

def build(domain, mdpath):
    cfg = CFG[domain]
    fm, body = parse_md(open(mdpath, encoding='utf-8').read())
    tpl = open(f'network/sites/{domain}/template.html', encoding='utf-8').read()
    content, h2s = md2html(body, cfg['lead'])
    words = len(re.sub('<[^>]+>', ' ', content).split())
    d = datetime.date.fromisoformat(fm['date'])
    img = fm.get('image', cfg['img'])
    cat = fm.get('category', 'Guides')
    vals = {
        'title': html.escape(fm['title'], quote=False),
        'title_json': json.dumps(fm['title'])[1:-1],
        'description': html.escape(fm['description'], quote=True),
        'description_json': json.dumps(fm['description'])[1:-1],
        'canonical': f"https://{domain}{fm['path']}",
        'author': html.escape(fm['author']),
        'date': d.strftime(cfg['date']),
        'date_iso': fm['date'],
        'category': html.escape(cat),
        'category_url': category_url(domain, cat),
        'category_slug': slug(cat),
        'readtime': str(max(1, round(words / 220))),
        'image': img, 'image_sm': img.replace('.webp', '-sm.webp'), 'image_800': img.replace('.webp', '-800.webp'),
        'toc': ''.join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in h2s),
        'toc_links': ''.join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in h2s),
        'content': content,
    }
    page = tpl
    for k, v in vals.items(): page = page.replace('{{' + k + '}}', v)
    out = f'network/sites/{domain}/live{fm["path"]}'
    if out.endswith('/'): out += 'index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w', encoding='utf-8').write(page)
    return fm, out, words, re.findall(r'\{\{[a-z_0-9]+\}\}', page)

if __name__ == '__main__':
    for dom in sys.argv[1:]:
        for md in sorted(os.listdir(f'network/sites/{dom}/posts')):
            if md.endswith('.md'):
                fm, out, words, left = build(dom, f'network/sites/{dom}/posts/{md}')
                print(f'{dom:30} {fm["path"]:45} words={words:5} leftover={sorted(set(left))}')
