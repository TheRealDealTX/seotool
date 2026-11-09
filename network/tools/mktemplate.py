#!/usr/bin/env python3
"""Derive network/sites/<domain>/template.html from a real post page on each live site.
The whole page is kept (hero, breadcrumbs, meta, sidebars, related posts); only the
post-specific parts become placeholders that buildpost.py fills.
Run from the repo root: python3 -I network/tools/mktemplate.py [domain ...]"""
import re, sys, html, json

SRC = {
 'hatetolovethesplit.com': '2014/03/17/carpet-countertop-beer/index.html',
 'agadecor.com': 'blog/wedding-flower-decoration-ideas/index.html',
 'ohmtoherminediy.com': 'blog/how-to-paint-furniture-with-chalk-paint/index.html',
 'fraserandmorris.com': 'blog/choosing-trees-for-a-small-garden.html',
 'rjbledlcdtvservicecentre.com': 'led-lcd-tv-repairing-in-kolkata/index.html',
 'asmith.photography': 'florsheim-shoes/index.html',
 'michellewhitephoto.com': 'blog/mandi-and-riley-nelson/index.html',
 'comeicavoliamerenda.com': '5mm-earrings-actual-size/index.html',
 'findsforfitness.com': 'best-tennis-shoes-for-flat-feet/index.html',
}

def sub1(s, pat, rep, flags=re.S, must=True):
    new, n = re.subn(pat, rep, s, count=1, flags=flags)
    if must and n == 0:
        raise SystemExit(f'pattern not found: {pat[:90]}')
    return new

def inner(s, open_pat, close_tag, replacement):
    """Replace the inner HTML of the first element matching open_pat (regex for the opening tag)
    up to its matching close tag (depth-aware for the same tag name)."""
    m = re.search(open_pat, s, re.S)
    if not m: raise SystemExit(f'container not found: {open_pat[:80]}')
    tag = re.match(r'<(\w+)', m.group(0)).group(1)
    depth = 0; i = m.start()
    for mm in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[m.start():]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            end = m.start() + mm.start()
            return s[:m.end()] + replacement + s[end:]
    raise SystemExit('unbalanced container')

def remove(s, open_pat, must=True):
    m = re.search(open_pat, s, re.S)
    if not m:
        if must: raise SystemExit(f'remove target not found: {open_pat[:80]}')
        return s
    tag = re.match(r'<(\w+)', m.group(0)).group(1)
    depth = 0
    for mm in re.finditer(r'<(/?)%s\b[^>]*>' % tag, s[m.start():]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            end = m.start() + mm.end()
            return s[:m.start()] + s[end:]
    raise SystemExit('unbalanced remove')

def head_params(s, d, src_path):
    """Title, description, canonical, og/twitter and JSON-LD fields -> placeholders."""
    cands = set()
    hm = re.search(r'"headline":\s*"([^"]+)"', s); head = hm.group(1) if hm else None
    if head: cands.add(head)
    for pat in (r'<meta property="og:title" content="([^"]*)"', r'<meta name="twitter:title" content="([^"]*)"', r'<title>([^<]*)</title>'):
        m = re.search(pat, s)
        if m:
            t = m.group(1)
            cands.add(t)
            for sep in (' | ', ' — ', ' – ', ' - '):
                if sep in t: cands.add(t.split(sep)[0])
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    if h1: cands.add(re.sub(r'<[^>]+>', '', h1.group(1)).strip())
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = desc_m.group(1) if desc_m else None
    src_url = f'https://{d}{src_path}'.rstrip('/')
    s = re.sub(re.escape(src_url) + r'/?(?![\w/-])(#[A-Za-z]+)?', lambda m: '{{canonical}}' + (m.group(1) or ''), s)
    def fix_ld(m):
        j = m.group(0)
        if head:
            j = re.sub(r'("headline":\s*)"' + re.escape(head) + '"', r'\1"{{title_json}}"', j)
            j = re.sub(r'("headline":\s*"\{\{title_json\}\}",\s*"description":\s*)"[^"]*"', r'\1"{{description_json}}"', j)
            j = re.sub(r'("name":\s*)"' + re.escape(head) + '"', r'\1"{{title_json}}"', j)
        j = re.sub(r'("date(?:Published|Modified)":\s*)"[^"]*"', r'\1"{{date_iso}}"', j)
        j = re.sub(r'"name":\s*"[^"]*"(,\s*"item":\s*"\{\{canonical\}\}")', r'"name": "{{title_json}}"\1', j)
        j = re.sub(r'("item":\s*"\{\{canonical\}\}",\s*)"name":\s*"[^"]*"', r'\1"name": "{{title_json}}"', j)
        return j
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', fix_ld, s, flags=re.S)
    # longest candidates first so a suffixed <title> is handled before its prefix
    for raw in sorted((c for c in cands if c and c != '{{title}}'), key=len, reverse=True):
        for v in {raw, html.escape(raw, quote=False), html.escape(raw, quote=True), html.unescape(raw)}:
            s = s.replace(v, '{{title}}')
    if desc:
        for v in {desc, html.escape(desc, quote=False), html.escape(desc, quote=True), html.unescape(desc)}:
            s = s.replace(v, '{{description}}')
    # h1 may contain <em> markup around part of the title: normalise to the bare placeholder
    s = re.sub(r'(<h1[^>]*>)(?:(?!</h1>).)*\{\{title\}\}(?:(?!</h1>).)*</h1>', r'\1{{title}}</h1>', s, count=1, flags=re.S)
    return s

def make(d):
    path = f'network/sites/{d}/live/{SRC[d]}'
    s = open(path, encoding='utf-8').read()
    src_path = '/' + SRC[d].replace('index.html', '')
    s = head_params(s, d, src_path)
    s = s.replace(' aria-current="page"', '')

    if d == 'hatetolovethesplit.com':
        s = sub1(s, r'<div class="post-hero-bg"><img src="[^"]*" alt="[^"]*"', '<div class="post-hero-bg"><img src="{{image}}" alt="{{title}}"')
        s = sub1(s, r'<a class="chip chip-light" href="[^"]*">[^<]*</a>', '<a class="chip chip-light" href="{{category_url}}">{{category}}</a>')
        s = sub1(s, r'<p class="meta">By the Split · <time datetime="[^"]*">[^<]*</time> · \d+ min read</p>', '<p class="meta">By the Split · <time datetime="{{date_iso}}">{{date}}</time> · {{readtime}} min read</p>')
        s = sub1(s, r'<li><a href="/category/[^"]*">[^<]*</a></li><li>\{\{title\}\}</li>', '<li><a href="{{category_url}}">{{category}}</a></li><li>{{title}}</li>')
        s = inner(s, r'<div class="prose">', 'div', '{{content}}')
        s = remove(s, r'<div class="post-tags">')
        s = remove(s, r'<nav class="post-nav"')
    elif d == 'agadecor.com':
        s = sub1(s, r'<div class="bg" data-parallax="10"><img src="[^"]*" srcset="[^"]*"', '<div class="bg" data-parallax="10"><img src="{{image}}" srcset="{{image_sm}} 640w, {{image}} 1024w"')
        s = sub1(s, r'<li>Wedding flower decoration ideas</li>', '<li>{{title}}</li>')
        s = sub1(s, r'(<p class="eyebrow fade-up"[^>]*>)[^<]*(</p>)', r'\1{{category}}\2')
        s = sub1(s, r'<span>Updated October 2026</span><span>\d+ min read</span>', '<span>{{date}}</span><span>{{readtime}} min read</span>')
        s = inner(s, r'<div class="narrow prose">', 'div',
                  '\n    <nav class="toc"><strong>In this article</strong><ol>{{toc}}</ol></nav>\n{{content}}\n'
                  '<div class="callout reveal"><h3>Planning something?</h3><p>Want a decor plan built around your palette and venue? Send us your date and a few photos you love.</p><a class="btn" href="/contact-us">Start your inquiry <span class="arrow">→</span></a></div>\n  ')
    elif d == 'ohmtoherminediy.com':
        s = sub1(s, r'<li><a href="/category/[^"]*">[^<]*</a></li><li>\{\{title\}\}</li>', '<li><a href="{{category_url}}">{{category}}</a></li><li>{{title}}</li>')
        s = sub1(s, r'<a class="eyebrow reveal" href="[^"]*" style="text-decoration:none">[^<]*</a>', '<a class="eyebrow reveal" href="{{category_url}}" style="text-decoration:none">{{category}}</a>')
        s = sub1(s, r'<time datetime="[^"]*">[^<]*</time>', '<time datetime="{{date_iso}}">{{date}}</time>')
        s = sub1(s, r'(</svg>)\d+ min read(</span>)', r'\1{{readtime}} min read\2')
        s = sub1(s, r'<div class="post-cover reveal reveal-zoom"><img src="[^"]*" alt="[^"]*" srcset="[^"]*"', '<div class="post-cover reveal reveal-zoom"><img src="{{image}}" alt="{{title}}" srcset="{{image_sm}} 720w, {{image}} 1024w"')
        s = remove(s, r'<div class="project-facts reveal">')
        s = inner(s, r'<div class="prose">', 'div', '\n{{content}}\n' + re.search(r'<div class="author-box">.*?</div></div>', s, re.S).group(0) + '\n  ')
        s = sub1(s, r'(<nav class="side-box toc" aria-label="On this page"><h3>On this page</h3><ol>).*?(</ol></nav>)', r'\1{{toc}}\2')
    elif d == 'fraserandmorris.com':
        s = sub1(s, r'<div class="hero__media" data-parallax="0.25"><img src="[^"]*" srcset="[^"]*"[^>]*alt="[^"]*"', '<div class="hero__media" data-parallax="0.25"><img src="{{image}}" srcset="{{image_800}} 800w, {{image}} 1600w" sizes="100vw" alt="{{title}}"')
        s = sub1(s, r'<span>Choosing trees for a small garden</span></nav>', '<span>{{title}}</span></nav>', must=False)
        s = sub1(s, r'<h1 class="fade-up">.*?</h1>', '<h1 class="fade-up">{{title}}</h1>')
        s = sub1(s, r'<p class="lead fade-up d2">.*?</p>', '<p class="lead fade-up d2">{{description}}</p>')
        s = sub1(s, r'<p class="post-meta post-meta--hero fade-up d2"><time datetime="[^"]*">[^<]*</time><span>&middot;</span>[^<]*<span>&middot;</span>\d+ min read</p>',
                 '<p class="post-meta post-meta--hero fade-up d2"><time datetime="{{date_iso}}">{{date}}</time><span>&middot;</span>{{category}}<span>&middot;</span>{{readtime}} min read</p>')
        s = inner(s, r'<article class="prose reveal">', 'article', '{{content}}\n')
        s = sub1(s, r'<div><dt>Published</dt><dd><time datetime="[^"]*">[^<]*</time></dd></div>\s*<div><dt>Category</dt><dd>[^<]*</dd></div>\s*<div><dt>Reading time</dt><dd>\d+ minutes</dd></div>',
                 '<div><dt>Published</dt><dd><time datetime="{{date_iso}}">{{date}}</time></dd></div>\n      <div><dt>Category</dt><dd>{{category}}</dd></div>\n      <div><dt>Reading time</dt><dd>{{readtime}} minutes</dd></div>')
    elif d == 'rjbledlcdtvservicecentre.com':
        s = sub1(s, r'<section class="page-hero scanlines">\s*<img src="[^"]*" alt="[^"]*"', '<section class="page-hero scanlines">\n  <img src="{{image}}" alt="{{title}}"')
        s = sub1(s, r'<li><a href="/">Home</a></li><li>\{\{title\}\}</li>', '<li><a href="/">Home</a></li><li><a href="/">Guides</a></li><li>{{title}}</li>')
        s = sub1(s, r'(<p class="eyebrow"><span class="subpx"><i></i><i></i><i></i></span>)[^<]*(</p>)', r'\1{{category}} · {{date}}\2')
        s = sub1(s, r'<p class="lead">.*?</p>', '<p class="lead">{{description}}</p>')
        s = inner(s, r'<article class="prose">', 'article', '\n{{content}}\n')
        s = s.replace('</head>', '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BlogPosting", "headline": "{{title_json}}", "description": "{{description_json}}", "datePublished": "{{date_iso}}", "dateModified": "{{date_iso}}", "mainEntityOfPage": "{{canonical}}", "author": {"@type": "Organization", "name": "RJB TV Service"}, "publisher": {"@id": "https://rjbledlcdtvservicecentre.com/#website"}}</script>\n</head>', 1)
    elif d == 'asmith.photography':
        s = sub1(s, r'<div class="hero-media"><img src="[^"]*" srcset="[^"]*"', '<div class="hero-media"><img src="{{image}}" srcset="{{image_sm}} 800w, {{image}} 1600w"')
        s = sub1(s, r'<a href="/journal#[^"]*">[^<]*</a></nav>', '<a href="/journal#{{category_slug}}">{{category}}</a></nav>')
        s = sub1(s, r'<p class="dek">.*?</p>', '<p class="dek">{{description}}</p>')
        s = sub1(s, r'<div class="meta"><span>[^<]*</span><span>\d+ min read</span><span>Frame [^<]*</span></div>', '<div class="meta"><span>{{category}}</span><span>{{readtime}} min read</span><span>{{date}}</span></div>')
        s = inner(s, r'<div class="prose">', 'div', '{{content}}')
        s = remove(s, r'<nav class="more-list"', must=False)
        s = sub1(s, r'(<nav class="toc" aria-label="Contents">).*?(</nav>)', r'\1{{toc_links}}\2')
        s = remove(s, r'<div class="notes">', must=False)
    elif d == 'michellewhitephoto.com':
        s = sub1(s, r'<section class="page-hero">\s*<img src="[^"]*" srcset="[^"]*"[^>]*alt="[^"]*"', '<section class="page-hero">\n  <img src="{{image}}" srcset="{{image_sm}} 800w, {{image}} 1600w" sizes="100vw" width="1600" height="1067" alt="{{title}}"')
        s = sub1(s, r'<span aria-current="page" style="margin:0;opacity:1">[^<]*</span></nav>', '<span style="margin:0;opacity:1">{{title}}</span></nav>', must=False)
        s = sub1(s, r'<span style="margin:0;opacity:1">[^<]*</span></nav>', '<span style="margin:0;opacity:1">{{title}}</span></nav>')
        s = sub1(s, r'<span class="eyebrow">[^<]*</span>\s*<h1>.*?</h1>', '<span class="eyebrow">{{category}}</span>\n    <h1>{{title}}</h1>')
        s = sub1(s, r'<div class="post-meta"><span>[^<]*</span><span>\d+ min read</span>', '<div class="post-meta"><span>{{date}}</span><span>{{readtime}} min read</span>')
        s = inner(s, r'<article class="prose">', 'article', '\n{{content}}\n    ')
        s = sub1(s, r'<h3>Planning a wedding\?</h3>\s*<p>[^<]*</p>\s*<a class="link-line" href="/contact/">Check your date</a>',
                 '<h3>Have a story or a question?</h3>\n        <p>MW Photo Journal is an independent journal about wedding, elopement and interior photography in Utah.</p>\n        <a class="link-line" href="/contact/">Write to the editors</a>')
    elif d == 'comeicavoliamerenda.com':
        s = sub1(s, r'(<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/earring-guides/">Earring Guides</a>)</nav>\s*<h1>.*?</h1>\s*<p>.*?</p>',
                 r'\1<span>/</span><span>{{title}}</span></nav>\n    <h1>{{title}}</h1>\n    <p>{{description}}</p>')
        s = sub1(s, r'<div class="meta-row"><a class="pill" href="/earring-guides/">[^<]*</a><span>\d+ min read</span><span>Updated [^<]*</span></div>', '<div class="meta-row"><a class="pill" href="/earring-guides/">{{category}}</a><span>{{readtime}} min read</span><span>Updated {{date}}</span></div>')
        s = sub1(s, r'<figure class="feature-img"><img src="[^"]*" srcset="[^"]*"[^>]*alt="[^"]*"', '<figure class="feature-img"><img src="{{image_800}}" srcset="{{image_800}} 800w, {{image}} 1600w" sizes="(max-width: 1000px) 100vw, 820px" width="1600" height="1034" alt="{{title}}"')
        s = remove(s, r'<div class="quick">')
        s = inner(s, r'<div class="prose">', 'div', '\n{{content}}\n      ')
        s = remove(s, r'<section class="faq"', must=False)
        s = sub1(s, r'(<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>).*?(</ol></nav>)', r'\1{{toc}}\2')
    elif d == 'findsforfitness.com':
        s = sub1(s, r'<div class="post-hero-bg" aria-hidden="true"><img src="[^"]*" srcset="[^"]*"', '<div class="post-hero-bg" aria-hidden="true"><img src="{{image}}" srcset="{{image_sm}} 720w, {{image}} 1600w"')
        s = sub1(s, r'<a href="/category/[^"]*">[^<]*</a><span class="sep">/</span><span>\{\{title\}\}</span>', '<a href="{{category_url}}">{{category}}</a><span class="sep">/</span><span>{{title}}</span>')
        s = sub1(s, r'<a class="pill pill-sky" href="[^"]*">[^<]*</a>', '<a class="pill pill-sky" href="{{category_url}}">{{category}}</a>')
        s = sub1(s, r'Updated <time datetime="[^"]*">[^<]*</time>', 'Updated <time datetime="{{date_iso}}">{{date}}</time>')
        s = sub1(s, r'(</svg>)\d+ min read(</span>)', r'\1{{readtime}} min read\2')
        s = sub1(s, r'(<details class="toc-box" open data-toc>\s*<summary>.*?</summary>\s*<ol>).*?(</ol>)', r'\1{{toc}}\2')
        s = sub1(s, r'<figure class="post-cover"><img src="[^"]*" srcset="[^"]*"[^>]*alt="[^"]*"[^>]*>(<figcaption>.*?</figcaption>)?</figure>', '<figure class="post-cover"><img src="{{image}}" srcset="{{image_sm}} 720w, {{image}} 1600w" sizes="(max-width: 900px) 100vw, 760px" width="1600" height="1067" alt="{{title}}" loading="eager" decoding="async"></figure>')
        s = inner(s, r'<div class="prose">', 'div', '\n{{content}}\n')
        s = remove(s, r'<section class="faq"', must=False)
        s = sub1(s, r'<p class="post-lede">.*?</p>', '<p class="post-lede">{{description}}</p>')
    # hero image of the source page -> {{image}} everywhere (preload, og/twitter image, ImageObject)
    src = open(path, encoding='utf-8').read()
    main = src[src.find('<main'):]
    im = re.search(r'<img src="/assets/img/([a-z0-9-]+?)(?:-800|-sm)?\.webp"', main)
    if im:
        base = im.group(1)
        s = s.replace(f'/assets/img/{base}-sm.webp', '{{image_sm}}').replace(f'/assets/img/{base}-800.webp', '{{image_800}}').replace(f'/assets/img/{base}.webp', '{{image}}')
        s = re.sub(r'https://' + re.escape(d) + r'/assets/(?:og|img/og)/' + re.escape(base) + r'\.jpg', 'https://' + d + '{{image}}', s)
        s = re.sub(r'https://' + re.escape(d) + r'\{\{image(?:_sm|_800)?\}\}', 'https://' + d + '{{image}}', s)
    s = re.sub(r'"articleSection":\s*"[^"]*"', '"articleSection": "{{category}}"', s)
    s = re.sub(r',\s*"keywords":\s*"[^"]*"', '', s)
    out = f'network/sites/{d}/template.html'
    open(out, 'w', encoding='utf-8').write(s)
    need = ['{{title}}', '{{description}}', '{{canonical}}', '{{content}}', '{{date_iso}}']
    missing = [p for p in need if p not in s]
    leftovers = re.findall(r'(?:Carpet, Countertops|Florsheim|Mandi|5mm Earrings|Best Tennis Shoes|Choosing <em>trees|LED LCD TV Repairing in Kolkata</h1>|flower decoration ideas|Chalk Paint \(Even)', s)
    print(f'{d:30} h1={s.count("<h1")} missing={missing} leftovers={len(leftovers)} placeholders={sorted(set(re.findall(r"{{[a-z_0-9]+}}", s)))}')

if __name__ == '__main__':
    for d in (sys.argv[1:] or SRC):
        make(d)
