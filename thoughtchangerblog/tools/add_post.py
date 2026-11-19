#!/usr/bin/env python3
"""Publish a new article into public/content (images, body, metadata, llms.txt, interlinks).

  python3 tools/add_post.py tools/drafts/<slug>.json

The draft JSON holds:
  slug, title, seo_title, description, categories, products[3], faq[6+],
  interlink_phrases ("phrase a|phrase b" that should link TO this post from other posts),
  featured: {url, alt}, inline: {url, alt, caption}
and the body lives next to it as tools/drafts/<slug>.html with one <!--tc:image--> marker where
the inline photo goes, ending with <!--tc:products-->, <h2 id="h-faqs">FAQs</h2>, <!--tc:faq-->.

Images are downloaded (CC0 sources only), cropped to 3:2 and saved as WebP under
/wp-content/uploads/YYYY/MM/ in WordPress-style sizes (300x200, 768x512, 1024x683, full 1536x1024)
so the existing srcset/thumbnail helpers work. Prints the list of changed files (relative to public/)
for `FILES=... tools/deploy.sh production`.
"""
import datetime as dt, html, io, json, os, re, sys, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
draft_path = sys.argv[1]
d = json.load(open(draft_path))
body = open(draft_path[:-5] + '.html').read()
slug = d['slug']
assert re.fullmatch(r'[a-z0-9-]+', slug), 'bad slug'
posts = json.load(open(os.path.join(PUB, 'content/posts.json')))
assert slug not in {p['slug'] for p in posts}, 'slug already exists'
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
ym = now.strftime('%Y/%m')
updir = os.path.join(PUB, 'wp-content/uploads', ym)
os.makedirs(updir, exist_ok=True)
changed = []

def save_image(url, name):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (thoughtchangerblog publisher)'})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert('RGB')
    w, h = im.size
    tw, th = (w, int(w * 2 / 3)) if w * 2 / 3 <= h else (int(h * 3 / 2), h)   # centre-crop to 3:2
    im = im.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th))
    full = im.resize((1536, 1024), Image.LANCZOS) if im.width >= 1536 else im
    full.save(os.path.join(updir, name + '.webp'), 'WEBP', quality=80, method=6)
    changed.append(f'wp-content/uploads/{ym}/{name}.webp')
    for (sw, sh) in [(300, 200), (768, 512), (1024, 683)]:
        im.resize((sw, sh), Image.LANCZOS).save(os.path.join(updir, f'{name}-{sw}x{sh}.webp'), 'WEBP', quality=80, method=6)
        changed.append(f'wp-content/uploads/{ym}/{name}-{sw}x{sh}.webp')
    return f'/wp-content/uploads/{ym}/{name}.webp'

feat = save_image(d['featured']['url'], slug)
inl = save_image(d['inline']['url'], slug + '-2')
base = inl[:-5]
fig = (f'<figure class="inline-photo"><img src="{inl}" srcset="{base}-300x200.webp 300w, {base}-768x512.webp 768w, '
       f'{base}-1024x683.webp 1024w, {inl} 1536w" sizes="(max-width: 800px) 100vw, 760px" width="1536" height="1024" '
       f'alt="{html.escape(d["inline"]["alt"])}" loading="lazy" decoding="async">'
       + (f'<figcaption>{html.escape(d["inline"]["caption"])}</figcaption>' if d['inline'].get('caption') else '') + '</figure>')
assert '<!--tc:image-->' in body, 'body needs a <!--tc:image--> marker'
body = body.replace('<!--tc:image-->', fig, 1)
for m in ('<!--tc:products-->', '<!--tc:faq-->', 'id="h-faqs"'):
    assert m in body, f'body missing {m}'
open(os.path.join(PUB, 'content/posts', slug + '.html'), 'w').write(body.strip() + '\n')
changed.append(f'content/posts/{slug}.html')

text = re.sub(r'<[^>]+>', ' ', body)
words = len(text.split()) + sum(len((f['q'] + ' ' + f['a']).split()) for f in d['faq'])
posts.append({
    'slug': slug, 'id': None, 'title': d['title'], 'seo_title': d['seo_title'], 'description': d['description'],
    'published': now.isoformat(), 'modified': now.isoformat(), 'image': feat, 'image_alt': d['featured']['alt'],
    'categories': d.get('categories') or ['General'], 'words': words, 'status': 'new',
    'products': d['products'], 'faq': d['faq'],
    'image_credit': {'featured': d['featured']['url'], 'inline': d['inline']['url'], 'license': 'CC0'},
})
posts.sort(key=lambda p: p['published'], reverse=True)
json.dump(posts, open(os.path.join(PUB, 'content/posts.json'), 'w'), indent=1, ensure_ascii=False)
changed.append('content/posts.json')

if d.get('interlink_phrases'):
    il_path = os.path.join(PUB, 'content/interlinks.json')
    il = json.load(open(il_path))
    il[d['interlink_phrases']] = slug
    json.dump(il, open(il_path, 'w'), indent=1, ensure_ascii=False)
    changed.append('content/interlinks.json')

# llms.txt
L = open(os.path.join(PUB, 'llms.txt')).read().split('\n')
i = L.index('## Posts') + 1
L.insert(i, f"- [{d['title']}](https://thoughtchangerblog.com/{slug}/): {d['description']}")
open(os.path.join(PUB, 'llms.txt'), 'w').write('\n'.join(L))
changed.append('llms.txt')

print(f'published {slug}: {words} words')
print('FILES=' + ' '.join(changed))
