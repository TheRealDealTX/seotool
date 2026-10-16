#!/usr/bin/env python3
"""Static site generator for the relationadvisor.com rebuild.

    python3 build.py              # staging build (noindex, robots Disallow)
    STAGING=0 python3 build.py    # production build for relationadvisor.com

Reads content/posts/*.json + content/plan.json, writes the site into public/.
"""
import hashlib
import html
import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'public')
SITE = 'https://relationadvisor.com'
NAME = 'RelationAdvisor'
EMAIL = 'info@relationadvisor.com'
TAGLINE = 'Let the relationship flow.'
STAGING = os.environ.get('STAGING', '1') != '0'
TODAY = date.today()
UPDATED_ISO = TODAY.isoformat()
UPDATED_HUMAN = TODAY.strftime('%B %Y')
ASSET_V = TODAY.strftime('%Y%m%d')

CATS = {
    'relationships': dict(name='Love & Relationships', short='Relationships', emoji='💞',
        blurb='Signs of love, trust, communication and keeping the spark alive.',
        lead='Practical, kind advice for the everyday work of loving someone — reading the signs, talking through the hard stuff and growing together.'),
    'dating': dict(name='Dating Advice', short='Dating', emoji='🌹',
        blurb='Crushes, first moves, conversations and confident dating.',
        lead='From the first hello to the first kiss: honest, respectful guidance on attraction, conversation and asking someone out.'),
    'breakups': dict(name='Breakups & Healing', short='Breakups', emoji='🌱',
        blurb='Ending it well, moving on, and rebuilding after heartbreak.',
        lead='Whether you are deciding to leave, picking up the pieces or wondering about an ex, these guides help you heal and move forward.'),
    'questions': dict(name='Questions & Games', short='Questions', emoji='💬',
        blurb='Conversation starters, deep questions and games for two.',
        lead='Hundreds of questions, challenges and games to break the ice, go deeper and have more fun together.'),
    'pickup-lines': dict(name='Pickup Lines', short='Pickup Lines', emoji='😉',
        blurb='Clever, cheesy and sweet lines that get a smile.',
        lead='Clever, cheesy, sweet and downright silly pickup lines — plus tips on delivering them with confidence and good humor.'),
    'quotes': dict(name='Love Notes & Quotes', short='Quotes', emoji='💌',
        blurb='Paragraphs, letters and texts that say what you feel.',
        lead='Ready-to-send paragraphs, love letters, texts and quotes for the moments when you want to say it just right.'),
    'captions': dict(name='Captions', short='Captions', emoji='📸',
        blurb='Couple and wedding captions for your photos.',
        lead='Caption ideas for couple selfies, date nights, anniversaries and wedding photos.'),
    'wedding': dict(name='Marriage & Wedding', short='Marriage', emoji='💍',
        blurb='Vows, anniversaries and building a strong marriage.',
        lead='Advice for married life and the big day — from wedding vows and anniversary wishes to navigating the hard seasons.'),
    'zodiac': dict(name='Zodiac & Love', short='Zodiac', emoji='✨',
        blurb='Love compatibility and romance by star sign.',
        lead='A playful look at love through the zodiac — compatibility, date ideas and how each sign shows affection.'),
}
CAT_ORDER = ['relationships', 'dating', 'breakups', 'questions', 'pickup-lines', 'quotes', 'captions', 'wedding', 'zodiac']

# Home page "where are you right now?" tabs
STAGES = [
    ('Crushing on someone', ['does-my-crush-like-me', 'signs-he-likes-you-more-than-a-friend', 'things-to-talk-about-with-your-crush',
                             'how-to-ask-someone-out', 'how-to-get-a-guy-to-like-you', 'cute-paragraphs-for-your-crush']),
    ('Dating', ['first-date-questions', 'how-to-keep-a-conversation-going', 'second-date-questions',
                'how-to-impress-a-girl', 'how-to-compliment-a-guy-8-tips-to-help-you-the-quick-way', 'expectations-about-dating']),
    ('In a relationship', ['how-to-show-love', 'how-to-improve-your-relationship-with-your-boyfriend', 'long-distance-relationship-advice',
                           'how-to-deal-with-jealousy', 'how-to-save-a-relationship', 'deep-questions-to-ask-your-boyfriend']),
    ('Healing', ['how-to-move-on-after-a-break-up', 'how-to-get-over-a-broken-heart', 'how-to-stop-thinking-about-your-ex',
                 'how-to-get-over-being-cheated-on', 'how-to-be-happy-with-yourself', 'how-to-deal-with-loneliness']),
    ('Married', ['how-to-be-a-better-wife', 'wedding-vow-examples', 'anniversary-wishes-for-husband-and-wife',
                 'what-men-want-in-a-relationship', 'how-to-handle-a-wife', 'zodiac-signs-love-languages']),
]
FEATURED = ['how-do-you-know-you-are-in-love', 'first-date-questions', 'how-to-move-on-after-a-break-up',
            'signs-he-loves-you-deeply', 'truth-or-dare-questions-for-adults']

# Old URLs (from the archive) that never existed as clean slugs
OLD_REDIRECTS = {
    '/how-do-you-know-…-someone-special/': '/how-do-you-know-when-you-love-someone/',
    '/how-do-you-know-…you-love-someone/': '/how-do-you-know-when-you-love-someone/',
    '/how-to-start-a-c…ationadvisor-com/': '/how-to-start-a-conversation-with-a-girl/',
    '/dirty-things-to-say-to-your-girlfriend/': '/romantic-things-to-say-to-your-girlfriend/',
    '/contact-us/': '/contact/',
    '/about-us/': '/about/',
    '/privacy-policy-2/': '/privacy-policy/',
}
# Hand-picked targets for archived tag pages where word overlap picks badly
TAG_OVERRIDES = {
    'comforting-her': '/how-to-cheer-someone-up/', 'dating': '/category/dating/', 'dating-tips': '/category/dating/',
    'how-to-be-a-good-wife-and-mother': '/how-to-be-a-better-wife/', 'how-to-be-the-best-wife-ever': '/how-to-be-a-better-wife/',
    'how-to-be-in-a-good-relatiosnhi': '/how-to-save-a-relationship/', 'how-to-be-with-her': '/how-to-understand-woman/',
    'how-to-control-your-husband': '/how-to-handle-husband-10-easiest-ways-to-handle-husband/',
    'how-to-protect-your-husband': '/how-to-handle-husband-10-easiest-ways-to-handle-husband/',
    'how-to-love-with-your-husband': '/how-to-show-love/', 'how-to-gain-her-faith': '/how-to-get-her-on-the-bed/',
    'how-to-leave-a-toxic-relationship': '/get-out-of-bad-relationship/', 'how-to-make-freind': '/how-to-make-friends-as-an-adult/',
    'how-to-say-sorry-to-your-girlfriend-in-a-romantic-way': '/how-to-apologize-to-your-girlfriend/',
    'kissing': '/how-to-get-a-girl-to-kiss-you/', 'kiss-on-lips': '/tips-to-make-out/', 'leaving-spouse-in-easy-way': '/how-to-leave-your-husband/',
    'one-word-compliments': '/how-to-compliment-a-girl/', 'relationship-advice': '/category/relationships/',
    'self-love': '/how-to-be-happy-with-yourself/', 'signs-you-need-to-breakup': '/how-to-know-when-to-break-up/',
    'why-to-give-her-what-she-wants': '/how-to-understand-woman/', 'woman-love': '/how-to-understand-woman/',
    'women-empowerment': '/date-an-intimidating-woman/', 'best-compliments-for-a-woman': '/how-to-compliment-a-girl/',
    'text-messages-to-make-him-want-you': '/texts-to-make-him-miss-you/', 'how-to-forget-your-ex-girlfriend': '/how-to-stop-thinking-about-your-ex/',
}

# ---------------------------------------------------------------- helpers
e = lambda s: html.escape(str(s), quote=True)


def slugify(s):
    s = html.unescape(re.sub('<[^>]+>', '', s)).lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:70].rstrip('-') or 'section'


def words(htm):
    return len(re.sub('<[^>]+>', ' ', htm).split())


def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)


def icon(name):
    paths = {
        'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'chev': '<path d="m6 9 6 6 6-6"/>',
        'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
        'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        'up': '<path d="m6 15 6-6 6 6"/>',
        'link': '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
        'x': '<path d="M4 4l16 16M20 4 4 20"/>',
        'fb': '<path d="M15 3h-2.5A4.5 4.5 0 0 0 8 7.5V10H5v4h3v7h4v-7h3l1-4h-4V7.5a.5.5 0 0 1 .5-.5H15z"/>',
        'pin': '<circle cx="12" cy="12" r="9"/><path d="m10 21 2-9M9.5 14.5C10 16 11 16.5 12.5 16.5c2.5 0 4-2 4-4.7C16.5 9.2 14.4 7.5 12 7.5 9 7.5 7.5 9.6 7.5 11.5c0 1 .4 1.9 1.1 2.3"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'heart': '<path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.3 3.1 4.5 6.9 4.5c2.1 0 3.6 1.1 5.1 2.9 1.5-1.8 3-2.9 5.1-2.9 3.8 0 6 3.8 4.5 7.2C19.5 16.4 12 21 12 21z"/>',
    }
    fill = 'currentColor' if name == 'heart' else 'none'
    return (f'<svg viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


# ---------------------------------------------------------------- data
def load():
    plan = {p['slug']: p for p in json.load(open(os.path.join(ROOT, 'content', 'plan.json')))}
    posts = []
    for slug, meta in plan.items():
        f = os.path.join(ROOT, 'content', 'posts', slug + '.json')
        if not os.path.exists(f):
            print('  ! missing content for', slug)
            continue
        p = json.load(open(f, encoding='utf-8'))
        p['slug'] = slug
        p['cat'] = meta['cat']
        p['url'] = f'/{slug}/'
        posts.append(p)
    return posts


IMAGES = {}


def load_images():
    f = os.path.join(ROOT, 'assets', 'img', 'images.json')
    if os.path.exists(f):
        IMAGES.update(json.load(open(f)))


def pool(cat):
    return sorted(k for k in IMAGES if k.startswith(f'cat-{cat}-'))


def img_tag(name, cls='', eager=False, sizes='(max-width: 700px) 100vw, 600px'):
    if not name or name not in IMAGES:
        return ''
    m = IMAGES[name]
    sm = f'/assets/img/{name}-sm.webp'
    has_sm = os.path.exists(os.path.join(ROOT, 'assets', 'img', f'{name}-sm.webp'))
    srcset = f' srcset="{sm} 640w, /assets/img/{name}.webp {m.get("width", 1600)}w" sizes="{sizes}"' if has_sm else ''
    load_attr = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img src="/assets/img/{name}.webp"{srcset} alt="{e(m.get("alt", ""))}" '
            f'width="{m.get("width", 1600)}" height="{m.get("height", 1067)}" {load_attr}{c}>')


def process_body(body):
    """Give every h2/h3 a unique id; return (html, toc)."""
    seen = {}
    toc = []

    def rep(m):
        tag, attrs, inner = m.group(1), m.group(2), m.group(3)
        base = slugify(inner)
        n = seen.get(base, 0)
        seen[base] = n + 1
        hid = base if n == 0 else f'{base}-{n + 1}'
        if tag == 'h2':
            toc.append((hid, html.unescape(re.sub('<[^>]+>', '', inner))))
        return f'<{tag} id="{hid}">{inner}</{tag}>'
    out = re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', rep, body, flags=re.S)
    # keep numbering continuous when a list of lines starts mid-way (CSS counters ignore start=)
    out = re.sub(r'<ol class="lines" start="(\d+)">', lambda m: f'<ol class="lines" start="{m.group(1)}" style="counter-reset: ln {int(m.group(1)) - 1}">', out)
    return out, toc


# ---------------------------------------------------------------- layout
def nav_html(active=''):
    subs = ''.join(
        f'<li><a href="/category/{c}/"><span class="ico" aria-hidden="true">{CATS[c]["emoji"]}</span>'
        f'<span>{e(CATS[c]["short"])}<small>{e(CATS[c]["blurb"])}</small></span></a></li>' for c in CAT_ORDER)

    def item(href, label, key):
        cur = ' aria-current="page"' if active == key else ''
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f'''<nav class="main-nav" id="site-nav" aria-label="Main">
  <ul>
    {item('/', 'Home', 'home')}
    <li class="has-sub"><button type="button" aria-expanded="false" aria-controls="topics-menu">Topics {icon('chev')}</button>
      <ul class="sub" id="topics-menu">{subs}</ul></li>
    {item('/category/dating/', 'Dating', 'dating')}
    {item('/category/questions/', 'Questions', 'questions')}
    {item('/category/pickup-lines/', 'Pickup Lines', 'pickup-lines')}
    {item('/blog/', 'All Articles', 'blog')}
    {item('/about/', 'About', 'about')}
    <li class="nav-cta"><a href="/contact/"{' aria-current="page"' if active == 'contact' else ''}>Contact</a></li>
  </ul>
</nav>'''


LOGO = (f'<a class="logo" href="/" aria-label="{NAME} home"><span class="logo-mark">{icon("heart")}</span>'
        f'<span>Relation<b>Advisor</b></span></a>')


def page(title, desc, path, body, active='', schema=None, og_image=None, og_type='website', extra_head=''):
    canonical = SITE + path
    og_img = SITE + '/assets/img/' + (og_image or 'hero') + '.webp'
    robots = '<meta name="robots" content="noindex, nofollow">' if STAGING else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ld = ''
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': schema}, ensure_ascii=False) + '</script>'
    cats_footer = ''.join(f'<li><a href="/category/{c}/">{e(CATS[c]["name"])}</a></li>' for c in CAT_ORDER[:6])
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ff5d73">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_V}">
{extra_head}{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap header-inner">
    {LOGO}
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    {nav_html(active)}
  </div>
</header>
<div class="nav-overlay" aria-hidden="true"></div>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        {LOGO}
        <p style="margin-top:16px;max-width:30em">Friendly, practical relationship advice — from first crushes and first dates to marriage, breakups and everything in between. {e(TAGLINE)}</p>
        <a class="footer-mail" href="mailto:{EMAIL}">{icon('mail')} {EMAIL}</a>
      </div>
      <div><h2>Topics</h2><ul>{cats_footer}</ul></div>
      <div><h2>Popular</h2><ul>
        <li><a href="/first-date-questions/">First date questions</a></li>
        <li><a href="/how-do-you-know-you-are-in-love/">Signs you're in love</a></li>
        <li><a href="/clever-pick-up-lines/">Clever pickup lines</a></li>
        <li><a href="/how-to-move-on-after-a-break-up/">Moving on after a breakup</a></li>
        <li><a href="/truth-or-dare-questions-for-adults/">Truth or dare questions</a></li>
      </ul></div>
      <div><h2>RelationAdvisor</h2><ul>
        <li><a href="/about/">About us</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/blog/">All articles</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© {TODAY.year} {NAME}. Advice for information only — not a substitute for professional counseling.</span>
      <nav aria-label="Legal"><a href="/privacy-policy/">Privacy</a><a href="/terms-of-use/">Terms</a><a href="/disclaimer/">Disclaimer</a></nav>
    </div>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">{icon('up')}</button>
<script src="/assets/js/site.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def org_schema():
    return [
        {'@type': 'Organization', '@id': SITE + '/#org', 'name': NAME, 'url': SITE + '/', 'email': EMAIL,
         'logo': {'@type': 'ImageObject', 'url': SITE + '/apple-touch-icon.png'}},
        {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': NAME, 'description': 'Relationship advice, dating tips, questions and love notes.',
         'publisher': {'@id': SITE + '/#org'},
         'potentialAction': {'@type': 'SearchAction', 'target': SITE + '/blog/?q={search_term_string}', 'query-input': 'required name=search_term_string'}},
    ]


def crumbs_schema(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{e(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{e(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(parts) + '</nav>'


def read_time(p):
    return max(3, round(words(p.get('intro', '') + p.get('body', '')) / 230))


def card(p, cls='', with_img=True, delay=''):
    im = img_tag(p['img'], sizes='(max-width: 620px) 100vw, (max-width: 900px) 50vw, 400px') if with_img else ''
    thumb = f'<div class="thumb">{im}</div>' if im else ''
    c = CATS[p['cat']]
    return (f'<a class="card tilt reveal {delay} {cls}{"" if im else " noimg"}" href="{p["url"]}" data-cat="{p["cat"]}">{thumb}<div class="body">'
            f'<span><span class="chip">{c["emoji"]} {e(c["short"])}</span></span><h3>{e(p["h1"])}</h3><p>{e(p["excerpt"])}</p>'
            f'<div class="meta"><span>{read_time(p)} min read</span></div></div></a>')


def distinct(cands, n, used=None):
    """First n posts whose photos differ from each other (and from `used`)."""
    used, out = set(used or ()), []
    for p in cands:
        if p['img'] not in used:
            out.append(p)
            used.add(p['img'])
        if len(out) == n:
            break
    return out


# ---------------------------------------------------------------- pages
def build_post(p, posts_by_cat, by_slug):
    body, toc = process_body(p['body'])
    c = CATS[p['cat']]
    crumbs = [('Home', '/'), (c['name'], f'/category/{p["cat"]}/'), (p['h1'], p['url'])]
    toc_items = ''.join(f'<li><a href="#{hid}">{e(t)}</a></li>' for hid, t in toc)
    takeaways = ''.join(f'<li>{e(t)}</li>' for t in p.get('takeaways', []))
    faq = ''.join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in p.get('faq', []))
    # related: same category first, then posts this one links to
    linked = [s for s in re.findall(r'href="/([a-z0-9-]+)/"', p['body']) if s in by_slug and s != p['slug']]
    h = int(hashlib.md5(p['slug'].encode()).hexdigest(), 16)
    same = [x for x in posts_by_cat[p['cat']] if x['slug'] != p['slug']]
    k = h % max(1, len(same))
    cands = same[k:] + same[:k] + [by_slug[s] for s in linked if by_slug[s] not in same]
    rel_posts = distinct(cands, 3, {p['img']})
    rel_posts += [x for x in cands if x not in rel_posts][:3 - len(rel_posts)]
    related = ''.join(card(x) for x in rel_posts[:3])
    share_url = SITE + p['url']
    from urllib.parse import quote
    su, st = quote(share_url, safe=''), quote(p['h1'], safe='')
    cover = img_tag(p['img'], eager=True, sizes='(max-width: 1200px) 100vw, 1160px')
    art = {'@type': 'BlogPosting', '@id': share_url + '#article', 'headline': p['h1'][:110], 'description': p['description'],
           'mainEntityOfPage': share_url, 'datePublished': UPDATED_ISO, 'dateModified': UPDATED_ISO,
           'author': {'@type': 'Organization', 'name': f'{NAME} Editorial Team', 'url': SITE + '/about/'},
           'publisher': {'@id': SITE + '/#org'}, 'articleSection': c['name'], 'wordCount': words(p['intro'] + p['body'])}
    if p['img']:
        art['image'] = SITE + f'/assets/img/{p["img"]}.webp'
    schema = org_schema() + [art, crumbs_schema(crumbs)]
    if p.get('faq'):
        schema.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['a']}} for q in p['faq']]})
    html_body = f'''
<section class="post-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(crumbs)}
    <a class="chip" href="/category/{p['cat']}/">{c['emoji']} {e(c['name'])}</a>
    <h1 style="margin-top:.5em">{e(p['h1'])}</h1>
    <div class="post-meta">
      <span>{icon('user')} {NAME} Editorial Team</span>
      <span>{icon('cal')} Updated {UPDATED_HUMAN}</span>
      <span>{icon('clock')} {read_time(p)} min read</span>
    </div>
    {f'<div class="post-cover">{cover}</div>' if cover else ''}
  </div>
</section>
<div class="wrap post-layout">
  <article class="prose">
    {f'<div class="takeaways"><h2>Key takeaways</h2><ul>{takeaways}</ul></div>' if takeaways else ''}
    <details class="toc-mobile"><summary>In this article</summary><ol>{toc_items}</ol></details>
    <div class="intro">{p['intro']}</div>
    {body}
    {f'<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{faq}</section>' if faq else ''}
    <div class="share"><span>Share this:</span>
      <a href="https://www.facebook.com/sharer/sharer.php?u={su}" target="_blank" rel="noopener" aria-label="Share on Facebook">{icon('fb')}</a>
      <a href="https://twitter.com/intent/tweet?url={su}&amp;text={st}" target="_blank" rel="noopener" aria-label="Share on X">{icon('x')}</a>
      <a href="https://pinterest.com/pin/create/button/?url={su}&amp;description={st}" target="_blank" rel="noopener" aria-label="Save to Pinterest">{icon('pin')}</a>
      <a href="mailto:?subject={st}&amp;body={su}" aria-label="Share by email">{icon('mail')}</a>
      <button type="button" data-share-copy aria-label="Copy link">{icon('link')}</button>
    </div>
  </article>
  <aside class="aside" aria-label="Article tools">
    <div class="aside-inner">
      <nav class="toc" aria-label="Table of contents"><h2>In this article</h2><ol>{toc_items}</ol></nav>
      <div class="aside-cta"><h3>Have a question?</h3><p>Send us your relationship question — it might inspire our next guide.</p><a class="btn" href="/contact/">Ask us {icon('arrow')}</a></div>
    </div>
  </aside>
</div>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow">Keep reading</span><h2>More in {e(c['name'])}</h2></div>
      <a class="link-arrow" href="/category/{p['cat']}/">View all {icon('arrow')}</a></div>
    <div class="grid grid-3">{related}</div>
  </div>
</section>'''
    write(f'{p["slug"]}/index.html', page(p['title'] if len(p['title']) > 45 else f'{p["title"]} | {NAME}', p['description'], p['url'], html_body,
                                         active=p['cat'], schema=schema, og_image=p['img'], og_type='article'))


def build_category(cat, items):
    c = CATS[cat]
    path = f'/category/{cat}/'
    crumbs = [('Home', '/'), (c['name'], path)]
    img = (pool(cat) or [None])[0]
    cards = ''.join(card(p, delay=f'd{i % 3}') for i, p in enumerate(items))
    others = ''.join(f'<a class="chip" href="/category/{o}/">{CATS[o]["emoji"]} {e(CATS[o]["short"])}</a>' for o in CAT_ORDER if o != cat)
    body = f'''
<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div>
  <div class="wrap cat-hero">
    <div>
      {crumbs_html(crumbs)}
      <span class="eyebrow">{c['emoji']} {len(items)} guides</span>
      <h1>{e(c['name'])}</h1>
      <p class="lead">{e(c['lead'])}</p>
      <div class="hero-tags">{others}</div>
    </div>
    {f'<div class="ph">{img_tag(img, eager=True)}</div>' if img else ''}
  </div>
</section>
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <div class="filters"><label class="sr-only" for="cat-q">Filter {e(c['short'])} articles</label><input id="cat-q" type="search" placeholder="Filter {len(items)} articles…"></div>
    <div class="grid grid-3">{cards}</div>
    <p class="no-results">No articles match that filter.</p>
  </div>
</section>'''
    schema = org_schema() + [crumbs_schema(crumbs), {'@type': 'CollectionPage', 'name': c['name'], 'url': SITE + path,
        'mainEntity': {'@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE + p['url'], 'name': p['h1']} for i, p in enumerate(items)]}}]
    write(f'category/{cat}/index.html', page(f'{c["name"]}: {len(items)} Guides & Ideas | {NAME}',
          f'{c["lead"]} Browse {len(items)} {c["short"].lower()} articles on {NAME}.'[:158], path, body, active=cat, schema=schema, og_image=img))


def build_blog(posts):
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>' + ''.join(
        f'<button class="chip" type="button" data-filter="{c}" aria-pressed="false">{CATS[c]["emoji"]} {e(CATS[c]["short"])}</button>' for c in CAT_ORDER)
    cards = ''.join(card(p, with_img=True) for p in posts)
    crumbs = [('Home', '/'), ('All articles', '/blog/')]
    body = f'''
<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(crumbs)}
    <span class="eyebrow">The library</span>
    <h1>All relationship articles</h1>
    <p class="lead">{len(posts)} guides, lists and love notes — filter by topic or search for exactly what you need.</p>
  </div>
</section>
<section class="section" style="padding-top:30px">
  <div class="wrap">
    <div class="filters">{chips}<label class="sr-only" for="blog-q">Search articles</label><input id="blog-q" type="search" placeholder="Search articles…"></div>
    <div class="grid grid-3">{cards}</div>
    <p class="no-results">No articles match — try a different word or topic.</p>
  </div>
</section>
<script>(function(){{var q=new URLSearchParams(location.search).get('q');if(q){{document.getElementById('blog-q').value=q;}}}})();</script>'''
    write('blog/index.html', page(f'All Relationship Articles & Guides | {NAME}',
          f'Browse all {len(posts)} RelationAdvisor articles: dating advice, signs of love, breakup recovery, questions to ask, pickup lines, love notes and more.',
          '/blog/', body, active='blog', schema=org_schema() + [crumbs_schema(crumbs)]))


def harvest_lines(posts):
    out = []
    for p in posts:
        if p['cat'] not in ('pickup-lines', 'quotes', 'captions'):
            continue
        for ol in re.findall(r'<ol class="lines"[^>]*>(.*?)</ol>', p['body'], re.S):
            for li in re.findall(r'<li>(.*?)</li>', ol, re.S)[:6]:
                t = html.unescape(re.sub('<[^>]+>', '', li)).strip()
                if 25 < len(t) < 150:
                    out.append({'l': t, 't': p['h1'], 'u': p['url']})
    h = lambda x: hashlib.md5(x['l'].encode()).hexdigest()
    return sorted(out, key=h)[:40]


def count_lines(posts):
    return sum(len(re.findall(r'<li>', ol)) for p in posts for ol in re.findall(r'<ol class="lines"[^>]*>(.*?)</ol>', p['body'], re.S))


def build_home(posts, by_slug, posts_by_cat):
    feat = [by_slug[s] for s in FEATURED if s in by_slug]
    bento = ''
    for i, p in enumerate(feat):
        bento += card(p, cls='big' if i == 0 else '', delay=f'd{i % 3}')
    topics = ''
    for i, c in enumerate(CAT_ORDER):
        im = img_tag((pool(c) or [None])[-1] if pool(c) else None, sizes='(max-width: 620px) 100vw, 300px')
        topics += (f'<a class="topic reveal d{i % 3}" href="/category/{c}/">{im}<span class="count">{len(posts_by_cat[c])} articles</span>'
                   f'<div class="t-inner"><h3>{CATS[c]["emoji"]} {e(CATS[c]["short"])}</h3><p>{e(CATS[c]["blurb"])}</p></div></a>')
    tabs, panels = '', ''
    for i, (label, slugs) in enumerate(STAGES):
        sel = 'true' if i == 0 else 'false'
        tabs += f'<button class="tab" role="tab" id="tab-{i}" aria-selected="{sel}" aria-controls="panel-{i}" tabindex="{0 if i == 0 else -1}">{e(label)}</button>'
        links = ''.join(f'<a href="{by_slug[s]["url"]}">{e(by_slug[s]["h1"])}{icon("arrow")}</a>' for s in slugs if s in by_slug)
        panels += f'<div class="tab-panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}>{links}</div>'
    feat_imgs = {p['img'] for p in feat}
    latest = distinct([p for p in sorted(posts, key=lambda p: int(hashlib.md5(p['slug'].encode()).hexdigest(), 16)) if p not in feat], 6, feat_imgs)
    latest_cards = ''.join(card(p, delay=f'd{i % 3}') for i, p in enumerate(latest))
    lines = harvest_lines(posts)
    marquee_items = ['First date questions', 'Signs he loves you', 'Moving on', 'Cute paragraphs', 'Long-distance love', 'Pickup lines',
                     'Truth or dare', 'Wedding vows', 'Zodiac matches', 'How to apologize', 'Love letters', 'Self-love']
    marquee_links = {'First date questions': '/first-date-questions/', 'Signs he loves you': '/signs-he-loves-you-deeply/',
                     'Moving on': '/how-to-move-on-after-a-break-up/', 'Cute paragraphs': '/cute-paragraphs-for-your-crush/',
                     'Long-distance love': '/long-distance-relationship-advice/', 'Pickup lines': '/category/pickup-lines/',
                     'Truth or dare': '/truth-or-dare-questions-for-adults/', 'Wedding vows': '/wedding-vow-examples/',
                     'Zodiac matches': '/most-compatible-zodiac-signs/', 'How to apologize': '/how-to-apologize-to-your-girlfriend/',
                     'Love letters': '/i-love-you-letters/', 'Self-love': '/how-to-be-happy-with-yourself/'}
    mq = ''.join(f'<a href="{marquee_links[m]}">{e(m)}</a>' for m in marquee_items)
    n_lines = count_lines(posts)
    lotd = ''
    if lines:
        lotd = f'''
<section class="section">
  <div class="wrap lotd">
    <div class="reveal">
      <span class="eyebrow">Line of the day</span>
      <h2>Need the <em class="accent grad-text">perfect words?</em></h2>
      <p class="muted" style="color:var(--muted)">Pickup lines, love notes and captions from our collections. Shuffle for a new one, then copy it with one tap.</p>
      <div class="hero-tags">
        <a class="chip" href="/category/pickup-lines/">😉 Pickup lines</a><a class="chip" href="/category/quotes/">💌 Love notes</a><a class="chip" href="/category/captions/">📸 Captions</a>
      </div>
    </div>
    <div class="lotd-card reveal d1" aria-live="polite">
      <blockquote>{e(lines[0]['l'])}</blockquote>
      <div class="row"><a class="src" href="{lines[0]['u']}">From: {e(lines[0]['t'])}</a>
        <span style="display:flex;gap:8px"><button class="btn" type="button" data-copy>Copy</button><button class="btn" type="button" data-next>Shuffle ↻</button></span></div>
    </div>
  </div>
  <script type="application/json" id="lotd-data">{json.dumps(lines, ensure_ascii=False).replace("</", "<\\/")}</script>
</section>'''
    body = f'''
<section class="hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div><div class="blob b3" aria-hidden="true"></div>
  <div class="hearts" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="reveal in">
      <span class="eyebrow">♥ Relationship advice that actually helps</span>
      <h1>Let the relationship <span class="grad-text"><em class="accent swap" data-words="flow.|grow.|glow.|heal.">flow.</em></span></h1>
      <p class="lead">Honest, warm guidance for every stage of love — crushes and first dates, the everyday work of a relationship, heartbreak and healing, and happily ever after.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/blog/">Explore {len(posts)} guides {icon('arrow')}</a>
        <a class="btn btn-ghost" href="/category/questions/">Questions to ask</a>
      </div>
      <div class="search-box" role="search">
        {icon('search')}
        <label class="sr-only" for="hero-q">Search RelationAdvisor</label>
        <input id="hero-q" type="search" placeholder="What's on your heart? Try “first date”…" autocomplete="off">
        <ul class="search-results" aria-label="Search results"></ul>
      </div>
      <div class="hero-tags">
        <a class="chip" href="/does-my-crush-like-me/">Does my crush like me?</a>
        <a class="chip" href="/how-to-move-on-after-a-break-up/">Moving on</a>
        <a class="chip" href="/truth-or-dare-questions-for-adults/">Truth or dare</a>
      </div>
    </div>
    <div class="hero-art reveal in d1">
      <div class="hero-photo">{img_tag('hero', eager=True, sizes='(max-width: 900px) 92vw, 560px')}</div>
      <a class="float-card f1" href="/first-date-questions/"><span class="ico">💬</span><span>200+ first date questions<small>Never run out of things to say</small></span></a>
      <a class="float-card f2" href="/signs-he-loves-you-deeply/"><span class="ico">💞</span><span>Signs he loves you deeply<small>Read the quiet clues</small></span></a>
    </div>
  </div>
</section>
<div class="marquee-wrap"><div class="marquee" aria-label="Popular topics"><div class="marquee-track">{mq}{mq.replace('<a ', '<a tabindex="-1" aria-hidden="true" ')}</div></div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Editor's picks</span><h2>Our most-loved guides</h2>
      <p>The articles readers come back to again and again.</p></div>
      <a class="link-arrow" href="/blog/">See all articles {icon('arrow')}</a></div>
    <div class="bento">{bento}</div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Browse by topic</span><h2>Find advice for where you are</h2></div></div>
    <div class="grid grid-3">{topics}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="stage reveal">
      <span class="eyebrow" style="color:#ffb3bf">Start here</span>
      <h2>Where are you in your love story?</h2>
      <p class="muted">Pick your stage and we'll point you to the guides that matter most right now.</p>
      <div class="tabs" role="tablist" aria-label="Relationship stage">{tabs}</div>
      {panels}
    </div>
  </div>
</section>
{lotd}
<section class="section alt">
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><b data-count="{len(posts)}">{len(posts)}</b><span>in-depth guides</span></div>
      <div class="stat reveal d1"><b data-count="{n_lines}" data-suffix="+">{n_lines:,}+</b><span>questions, lines &amp; captions</span></div>
      <div class="stat reveal d2"><b data-count="{len(CAT_ORDER)}">{len(CAT_ORDER)}</b><span>topics covered</span></div>
      <div class="stat reveal d3"><b>100%</b><span>free to read</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="eyebrow">Fresh reads</span><h2>More from the blog</h2></div>
      <a class="link-arrow" href="/blog/">Browse the library {icon('arrow')}</a></div>
    <div class="grid grid-3">{latest_cards}</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta reveal">
      {img_tag('about', sizes='100vw')}
      <span class="eyebrow" style="color:#ffb3bf">We'd love to hear from you</span>
      <h2>Have a relationship question on your mind?</h2>
      <p>Tell us what you're going through or what you'd like us to write about next. Every message is read by a real person.</p>
      <div class="hero-actions" style="margin-bottom:0"><a class="btn btn-primary" href="/contact/">Send us a message {icon('arrow')}</a>
        <a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
  </div>
</section>'''
    write('home.html', page(f'{NAME} — Relationship Advice, Dating Tips & Love Notes',
          'RelationAdvisor is your friendly guide to love: relationship advice, dating tips, questions to ask, breakup help, pickup lines, love notes and more.',
          '/', body, active='home', schema=org_schema()))


def simple_page(path, title, desc, h1, lead, inner, active='', eyebrow='', img=None):
    crumbs = [('Home', '/'), (h1, path)]
    body = f'''
<section class="page-hero">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(crumbs)}
    {f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else ''}
    <h1>{e(h1)}</h1>
    {f'<p class="lead">{lead}</p>' if lead else ''}
  </div>
</section>
<section class="section" style="padding-top:20px"><div class="wrap">{inner}</div></section>'''
    write(path.strip('/') + '/index.html', page(title, desc, path, body, active=active, schema=org_schema() + [crumbs_schema(crumbs)], og_image=img))


def build_static(posts, posts_by_cat):
    # About
    about = f'''
<div class="about-grid">
  <div class="reveal">
    <h2>Love is complicated. Good advice shouldn't be.</h2>
    <p>{NAME} started with a simple idea: people deserve relationship advice that is honest, warm and actually useful — whether they are working up the nerve to text a crush, trying to keep a long-distance relationship alive, or learning to breathe again after a breakup.</p>
    <p>Today the site is home to {len(posts)} guides across {len(CAT_ORDER)} topics, from <a href="/category/dating/">dating advice</a> and <a href="/category/relationships/">relationship skills</a> to <a href="/category/breakups/">breakup recovery</a>, <a href="/category/questions/">conversation starters</a> and <a href="/category/quotes/">love notes</a> you can send tonight.</p>
    <a class="btn btn-primary" href="/blog/">Explore the guides {icon('arrow')}</a>
  </div>
  <div class="photo-rounded reveal d1">{img_tag('about')}</div>
</div>
<div style="margin-top:80px">
  <div class="section-head reveal"><div><span class="eyebrow">What we believe</span><h2>Our approach</h2></div></div>
  <div class="values">
    <div class="value reveal"><div class="ico">🤝</div><h3>Respect first</h3><p>Healthy relationships are built on consent, honesty and mutual respect. We never teach games that hurt people.</p></div>
    <div class="value reveal d1"><div class="ico">🧭</div><h3>Practical over preachy</h3><p>Every guide ends with things you can actually say or do — scripts, steps, questions and examples.</p></div>
    <div class="value reveal d2"><div class="ico">🌈</div><h3>For everyone</h3><p>Love looks different for everyone. Our advice is written to be useful whoever you are and whoever you love.</p></div>
  </div>
</div>
<div class="plain" style="margin-top:80px">
  <h2>How our content is made</h2>
  <p>Articles are written and reviewed by the {NAME} editorial team and updated regularly. We draw on widely accepted relationship research and communication practices, and we keep things simple and judgment-free.</p>
  <p>Our content is for general information and entertainment. It is not a substitute for advice from a licensed therapist, counselor or medical professional. If you are in an abusive situation or feel unsafe, please contact the National Domestic Violence Hotline at 1-800-799-7233 (or text START to 88788), or call 911 in an emergency.</p>
  <h2>Get in touch</h2>
  <p>Questions, feedback, corrections or topic ideas? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="/contact/">contact form</a>.</p>
</div>'''
    simple_page('/about/', f'About {NAME} — Who We Are & How We Help', f'Learn about {NAME}: friendly, practical relationship advice for dating, love, marriage and breakups — and how our content is made.',
                f'About {NAME}', 'Friendly, practical relationship advice — for every stage of love.', about, active='about', eyebrow='Our story', img='about')

    # Contact
    contact = f'''
<div class="contact-grid">
  <div class="reveal">
    <h2>Let's talk.</h2>
    <p>Have a question about your relationship, a topic you'd love us to cover, or feedback on an article? Send us a note — we read every message and reply within two business days.</p>
    <ul class="info-list">
      <li><span class="ico">✉️</span><span>Email us<br><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
      <li><span class="ico">⏱️</span><span>Response time<br><strong>Within 2 business days</strong></span></li>
      <li><span class="ico">💡</span><span>Story ideas &amp; corrections<br><strong>Always welcome</strong></span></li>
    </ul>
    <div class="photo-rounded" style="aspect-ratio:16/10">{img_tag('contact')}</div>
  </div>
  <div class="contact-card reveal d1">
    <h2 style="font-size:1.6rem">Send a message</h2>
    <form id="contact-form" class="form" action="/contact.php" method="post" novalidate>
      <div class="row2">
        <label>Your name<input name="name" type="text" autocomplete="name" required maxlength="100"></label>
        <label>Email address<input name="email" type="email" autocomplete="email" required maxlength="150"></label>
      </div>
      <label>Topic
        <select name="topic">
          <option>Relationship question</option><option>Article suggestion</option><option>Feedback or correction</option><option>Partnerships</option><option>Something else</option>
        </select>
      </label>
      <label>Message<textarea name="message" required maxlength="5000"></textarea></label>
      <label class="hp" aria-hidden="true">Leave this empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label>
      <input type="hidden" name="ts" value="0" id="form-ts">
      <button class="btn btn-primary" type="submit" style="justify-content:center">Send message</button>
      <p class="form-note">By sending this form you agree to our <a href="/privacy-policy/">privacy policy</a>. Please don't include sensitive personal details.</p>
    </form>
    <div class="alert" role="status" aria-live="polite" style="margin-top:14px"></div>
  </div>
</div>
<script>document.getElementById('form-ts').value=Math.floor(Date.now()/1000);</script>'''
    simple_page('/contact/', f'Contact {NAME} — Ask a Relationship Question', f'Contact {NAME} at {EMAIL}. Send us a relationship question, an article idea, feedback or a correction — we reply within two business days.',
                'Contact us', f'Questions, ideas or feedback? Reach us at <a href="mailto:{EMAIL}">{EMAIL}</a>.', contact, active='contact', eyebrow='Say hello', img='contact')

    legal_privacy = f'''<div class="plain">
<p><em>Last updated: {TODAY.strftime('%B %d, %Y')}</em></p>
<p>This privacy policy explains how {NAME} ("we", "us") collects and uses information when you visit {SITE.replace('https://', '')} (the "Site").</p>
<h2>Information we collect</h2>
<ul><li><strong>Information you send us.</strong> If you use our contact form or email us, we receive your name, email address and the contents of your message.</li>
<li><strong>Technical information.</strong> Like most websites, our hosting provider automatically logs basic technical data such as IP address, browser type, pages visited and the date and time of the visit, for security and performance purposes.</li>
<li><strong>Cookies.</strong> The Site itself does not set advertising or tracking cookies. Your browser may store small preferences locally. If we add analytics or advertising in the future, we will update this policy.</li></ul>
<h2>How we use information</h2>
<p>We use the information you send us only to reply to you, improve our content and keep the Site secure. We do not sell your personal information.</p>
<h2>Third-party services</h2>
<p>The Site loads web fonts from Google Fonts, which may receive your IP address as part of delivering the font files. Share buttons link to third-party websites (such as Facebook, X and Pinterest) that have their own privacy policies; nothing is sent to them unless you click.</p>
<h2>Data retention</h2>
<p>We keep contact messages only as long as needed to respond and for reasonable record-keeping, then delete them.</p>
<h2>Your rights</h2>
<p>Depending on where you live (for example under the GDPR or the CCPA), you may have the right to access, correct or delete personal information we hold about you. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will respond within 30 days.</p>
<h2>Children</h2>
<p>The Site is intended for adults and is not directed to children under 13. We do not knowingly collect information from children.</p>
<h2>Changes and contact</h2>
<p>We may update this policy from time to time; the date above shows the latest version. Questions? Contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    simple_page('/privacy-policy/', f'Privacy Policy | {NAME}', f'How {NAME} collects, uses and protects information when you visit our website or contact us.', 'Privacy policy', '', legal_privacy, eyebrow='Legal')

    legal_terms = f'''<div class="plain">
<p><em>Last updated: {TODAY.strftime('%B %d, %Y')}</em></p>
<p>By using {SITE.replace('https://', '')} (the "Site") you agree to these terms. If you do not agree, please do not use the Site.</p>
<h2>Content is for information only</h2>
<p>Articles on the Site are general information and entertainment. They are not professional, medical, psychological or legal advice, and they do not create any professional relationship. See our <a href="/disclaimer/">disclaimer</a>.</p>
<h2>Using our content</h2>
<p>You are welcome to read, share links to and quote short excerpts of our articles with a link back to the original page. You may freely use individual lines, questions, captions and messages from our lists in your own personal conversations and posts. You may not republish full articles or substantial portions of the Site without written permission.</p>
<h2>Acceptable use</h2>
<p>Do not use the Site or our contact form to send spam, harass anyone, attempt to break the Site's security, or break any law.</p>
<h2>Links to other sites</h2>
<p>We may link to other websites for your convenience. We are not responsible for their content or practices.</p>
<h2>No warranty and limitation of liability</h2>
<p>The Site is provided "as is" without warranties of any kind. To the fullest extent permitted by law, {NAME} is not liable for any damages arising from your use of the Site.</p>
<h2>Changes</h2>
<p>We may update these terms at any time by posting a new version here. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    simple_page('/terms-of-use/', f'Terms of Use | {NAME}', f'The terms that apply when you use the {NAME} website and its relationship advice content.', 'Terms of use', '', legal_terms, eyebrow='Legal')

    disclaimer = f'''<div class="plain">
<p>{NAME} publishes general relationship and dating information for educational and entertainment purposes. Our writers are not acting as your therapist, counselor, doctor or lawyer, and nothing on this Site is a substitute for professional advice tailored to your situation.</p>
<p>Every relationship is different. Use your own judgment, and when decisions affect your health, safety, finances or legal rights, talk with a qualified professional.</p>
<h2>If you feel unsafe</h2>
<p>If you are experiencing abuse or feel unsafe, contact the <strong>National Domestic Violence Hotline</strong> at 1-800-799-7233, text START to 88788, or visit thehotline.org. If you are in immediate danger, call 911. If you are struggling emotionally, you can call or text <strong>988</strong> (Suicide &amp; Crisis Lifeline in the US).</p>
<h2>Affiliate and advertising disclosure</h2>
<p>We do not currently run ads or affiliate links. If that changes, we will clearly disclose it on the relevant pages.</p>
<p>Questions about this disclaimer? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>'''
    simple_page('/disclaimer/', f'Disclaimer | {NAME}', f'{NAME} provides general relationship information, not professional counseling. Read our full disclaimer and where to find help.', 'Disclaimer', '', disclaimer, eyebrow='Legal')

    # HTML sitemap
    cols = ''
    for c in CAT_ORDER:
        cols += f'<section><h2><a href="/category/{c}/">{CATS[c]["emoji"]} {e(CATS[c]["name"])}</a></h2><ul>' + ''.join(
            f'<li><a href="{p["url"]}">{e(p["h1"])}</a></li>' for p in posts_by_cat[c]) + '</ul></section>'
    cols += ('<section><h2>Pages</h2><ul><li><a href="/">Home</a></li><li><a href="/blog/">All articles</a></li><li><a href="/about/">About</a></li>'
             '<li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms-of-use/">Terms of use</a></li>'
             '<li><a href="/disclaimer/">Disclaimer</a></li></ul></section>')
    simple_page('/sitemap/', f'Sitemap | {NAME}', f'Every page on {NAME}, organized by topic.', 'Sitemap', 'Every guide on the site, organized by topic.',
                f'<div class="sitemap-cols">{cols}</div>')


def build_404(posts, by_slug):
    picks = ''.join(card(by_slug[s]) for s in FEATURED[:3] if s in by_slug)
    body = f'''
<section class="hero" style="padding-bottom:40px">
  <div class="blob b1" aria-hidden="true"></div><div class="blob b2" aria-hidden="true"></div>
  <div class="wrap" style="text-align:center;max-width:720px">
    <span class="eyebrow">Error 404</span>
    <h1>This page <em class="accent grad-text">ghosted</em> you.</h1>
    <p class="lead" style="margin:0 auto 26px">We couldn't find that page — but plenty of great advice is still here for you. Try a search:</p>
    <div class="search-box" role="search" style="margin:0 auto;text-align:left">{icon('search')}<label class="sr-only" for="nf-q">Search</label>
      <input id="nf-q" type="search" placeholder="Search articles…" autocomplete="off"><ul class="search-results"></ul></div>
    <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary" href="/">Back to home</a><a class="btn btn-ghost" href="/blog/">All articles</a></div>
  </div>
</section>
<section class="section" style="padding-top:20px"><div class="wrap"><div class="grid grid-3">{picks}</div></div></section>'''
    out = page(f'Page Not Found | {NAME}', 'The page you were looking for could not be found.', '/404.html', body)
    out = out.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    write('404.html', out)


# ---------------------------------------------------------------- non-HTML outputs
def build_meta_files(posts):
    urls = ['/', '/blog/', '/about/', '/contact/', '/sitemap/', '/privacy-policy/', '/terms-of-use/', '/disclaimer/'] + \
           [f'/category/{c}/' for c in CAT_ORDER] + [p['url'] for p in posts]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED_ISO}</lastmod></url>')
    sm.append('</urlset>')
    write('sitemap.xml', '\n'.join(sm) + '\n')
    if STAGING:
        write('robots.txt', '# Staging build — not for indexing\nUser-agent: *\nDisallow: /\n')
    else:
        write('robots.txt', f'User-agent: *\nDisallow: /home.html\nDisallow: /contact.php\n\nSitemap: {SITE}/sitemap.xml\n')
    idx = [{'t': p['h1'], 'u': p['url'], 'c': CATS[p['cat']]['short'], 'k': p.get('keyword', '') + ' ' + p.get('excerpt', '')} for p in posts]
    write('assets/search.json', json.dumps(idx, ensure_ascii=False, separators=(',', ':')))
    write('site.webmanifest', json.dumps({'name': NAME, 'short_name': NAME, 'icons': [
        {'src': '/web-app-manifest-192x192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': '/web-app-manifest-512x512.png', 'sizes': '512x512', 'type': 'image/png'}],
        'theme_color': '#ff5d73', 'background_color': '#fff8f3', 'display': 'standalone'}, indent=1))
    write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
          '<stop offset="0" stop-color="#ff5d73"/><stop offset="1" stop-color="#ff8a5b"/></linearGradient></defs>'
          '<rect width="64" height="64" rx="16" fill="url(#g)"/><path fill="#fff" d="M32 50s-15-9.2-19.2-18.6C9.8 24.6 14.2 17 21.8 17c4.2 0 7.2 2.2 10.2 5.8 3-3.6 6-5.8 10.2-5.8 7.6 0 12 7.6 9 14.4C47 40.8 32 50 32 50z"/></svg>\n')


def tag_redirects(posts):
    """Map archived /tag/<slug>/ URLs to the closest new article."""
    tags_file = os.path.join(ROOT, 'content', 'old-tags.txt')
    if not os.path.exists(tags_file):
        return {}
    stop = {'to', 'a', 'the', 'how', 'for', 'of', 'in', 'on', 'with', 'and', 'you', 'your', 'her', 'him', 'is', 'my', 'do', 'be', 'when', 'what', 'why', 'u', 'are', 'that', 'can'}
    toks = lambda s: {t for t in re.split(r'[-\s]+', s.lower()) if t and t not in stop}
    out = {}
    for tag in open(tags_file).read().split():
        tt = toks(tag)
        best, score = None, 0
        for p in posts:
            st = toks(p['slug']) | toks(p.get('keyword', ''))
            s = len(tt & st) / (len(tt | st) or 1)
            if tag == p['slug']:
                s = 2
            if s > score:
                best, score = p, s
        if tag in TAG_OVERRIDES:
            out[f'/tag/{tag}/'] = TAG_OVERRIDES[tag]
            continue
        out[f'/tag/{tag}/'] = best['url'] if best and score >= 0.2 else f'/category/{best["cat"]}/' if best and score > 0 else '/blog/'
    return out


def build_php(posts):
    redirects = dict(OLD_REDIRECTS)
    redirects.update(tag_redirects(posts))
    arr = ',\n'.join(f'    {json.dumps(k, ensure_ascii=False)} => {json.dumps(v)}' for k, v in sorted(redirects.items()))
    cats = '|'.join(CAT_ORDER)
    php = f'''<?php
// {NAME} static site front controller (generated by build.py — do not edit by hand).
// The host serves existing files directly; every other path lands here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = ($host === 'relationadvisor.com' || $host === 'www.relationadvisor.com') ? 'https://relationadvisor.com' : 'https://' . $host;

function go($to) {{ global $home; header('Location: ' . $home . $to, true, 301); exit; }}

// Canonical scheme/host for the production domain (TLS terminates upstream).
if ($host === 'www.relationadvisor.com' || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' && $host === 'relationadvisor.com')) {{
    go($uri);
}}
if ($path === '/' || $path === '/index.php') {{
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}}

$map = [
{arr}
];
$p = rtrim($path, "/ \\u{{200E}}") . '/';
if (isset($map[$p])) go($map[$p]);

// WordPress-era URL patterns
if (preg_match('#^/tag/[^/]+/page/\\d+/?$#', $path)) {{ $t = preg_replace('#/page/\\d+/?$#', '/', $path); if (isset($map[$t])) go($map[$t]); go('/blog/'); }}
if (preg_match('#^/tag/#', $path)) go('/blog/');
if (preg_match('#^/category/({cats})/page/\\d+/?$#', $path, $m)) go('/category/' . $m[1] . '/');
if (preg_match('#^/category/#', $path)) go('/blog/');
if (preg_match('#^/author/#', $path)) go('/about/');
if (preg_match('#^/page/\\d+/?$#', $path)) go('/blog/');
if (preg_match('#^/(feed|comments/feed|rss)/?$#', $path)) go('/');
if (preg_match('#^/([a-z0-9-]+)/(feed|amp|embed|attachment)(/.*)?$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) go('/' . $m[1] . '/');
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\\.php|xmlrpc\\.php)(/|$)#', $path)) go('/');
if (preg_match('#^/([a-z0-9-]+)$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) go('/' . $m[1] . '/');
if (preg_match('#^/([a-z0-9-]+)/(.+)$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1]) && !is_file(__DIR__ . $path)) go('/' . $m[1] . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
'''
    write('index.php', php)
    return len(redirects)


CONTACT_PHP = r'''<?php
// Contact form handler: emails messages to the site inbox.
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');
function out($ok, $err = null) { echo json_encode(['ok' => $ok, 'error' => $err]); exit; }
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); out(false, 'Method not allowed.'); }

$to = '__EMAIL__';
$name = trim(substr($_POST['name'] ?? '', 0, 100));
$email = trim(substr($_POST['email'] ?? '', 0, 150));
$topic = trim(substr($_POST['topic'] ?? 'Message', 0, 60));
$msg = trim(substr($_POST['message'] ?? '', 0, 5000));
$ts = (int)($_POST['ts'] ?? 0);

// Spam checks: honeypot field and a minimum time on the page.
if (!empty($_POST['website'])) out(true);
if ($ts > 0 && time() - $ts < 3) out(true);
if ($name === '' || $msg === '') out(false, 'Please fill in your name and message.');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(false, 'Please enter a valid email address.');
if (preg_match('/[\r\n]/', $name . $email . $topic)) out(false, 'Invalid input.');

$subject = '[RelationAdvisor] ' . $topic . ' — ' . $name;
$body = "Name: $name\nEmail: $email\nTopic: $topic\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n\n$msg\n";
$headers = "From: RelationAdvisor <__EMAIL__>\r\nReply-To: $name <$email>\r\nContent-Type: text/plain; charset=UTF-8\r\n";
$sent = @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
out($sent, $sent ? null : 'Sorry, we could not send your message. Please email __EMAIL__ directly.');
'''


# ---------------------------------------------------------------- main
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'),
                    ignore=shutil.ignore_patterns('images.json', '*.jpg', '*.jpeg', '*.png'))
    for f in os.listdir(os.path.join(ROOT, 'static')) if os.path.isdir(os.path.join(ROOT, 'static')) else []:
        shutil.copy(os.path.join(ROOT, 'static', f), os.path.join(OUT, f))
    load_images()
    posts = load()
    # spread each category's photo pool round-robin so neighbours in a listing differ
    for c in CAT_ORDER:
        imgs = pool(c) or pool('relationships')
        for i, p in enumerate(sorted((x for x in posts if x['cat'] == c), key=lambda x: x['slug'])):
            p['img'] = imgs[i % len(imgs)] if imgs else None
    for p in posts:
        p.setdefault('h1', p['title'])
    posts.sort(key=lambda p: p['h1'].lower())
    by_slug = {p['slug']: p for p in posts}
    posts_by_cat = {c: [p for p in posts if p['cat'] == c] for c in CAT_ORDER}
    for p in posts:
        build_post(p, posts_by_cat, by_slug)
    for c in CAT_ORDER:
        build_category(c, posts_by_cat[c])
    build_blog(posts)
    build_home(posts, by_slug, posts_by_cat)
    build_static(posts, posts_by_cat)
    build_404(posts, by_slug)
    build_meta_files(posts)
    n_redirects = build_php(posts)
    write('contact.php', CONTACT_PHP.replace('__EMAIL__', EMAIL))
    write('.htaccess', 'DirectoryIndex index.html index.php\nErrorDocument 404 /404.html\nOptions -Indexes\n')
    print(f'built {len(posts)} posts, {len(CAT_ORDER)} categories, {n_redirects} redirects -> {OUT} ({"STAGING" if STAGING else "PRODUCTION"})')


if __name__ == '__main__':
    main()
