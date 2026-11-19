#!/usr/bin/env python3
"""Build seed files for new articles and Amazon products.

Reads  content/articles-2026-11/*.json   (one article per file: slug, topic, title,
                                          seo_title, meta_description, body_html, products[])
Photos: content/articles-2026-11/_images.json maps slug -> {w, h, credit, credit_url}
for a real photo already saved at public_html/media/blog/<slug>.webp; otherwise a title card is generated.
Writes public_html/app/seed/articles-2026-11.php
       public_html/app/seed/products.php
       public_html/media/blog/<slug>.webp  (generated title-card featured images)

Checks every internal /blog/ link resolves to a real article. Idempotent.
"""
import glob
import html
import json
import os
import re
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'articles-2026-11')
SEED = os.path.join(ROOT, 'public_html', 'app', 'seed')
MEDIA = os.path.join(ROOT, 'public_html', 'media', 'blog')
ICON = os.path.join(ROOT, 'public_html', 'assets', 'img', 'my1secret-icon-512.png')
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
PUBLISHED = '2026-11-19'

TOPIC_STYLE = {   # gradient colors + label
    'renting': ((15, 34, 51), (26, 127, 191), 'Renting & Apartment Life'),
    'home-design': ((40, 24, 77), (124, 92, 255), 'Small-Space Design'),
    'insurance-claims': ((60, 22, 8), (232, 89, 12), 'Insurance & Claims'),
    'texas-living': ((58, 12, 12), (201, 42, 42), 'Texas Living'),
    'lifestyle': ((12, 46, 22), (43, 138, 62), 'Lifestyle & Wellness'),
}

# Topic-level picks: shown on every article in the topic (after its own picks) and on /shop/.
TOPIC_PRODUCTS = {
    'renting': [
        ('Video doorbell (renter-friendly, battery)', 'battery video doorbell no wiring', 'See who is at the door without drilling or rewiring, and take it with you when you move.'),
        ('Portable door security bar', 'door security bar portable', 'Adds a solid second barrier to any door, no tools or holes needed.'),
        ('Moving boxes kit with tape', 'moving boxes kit with tape', 'A matched set of boxes in a few sizes makes packing and labeling far easier.'),
        ('Command strips and hooks variety pack', 'damage free hanging strips hooks variety pack', 'Hang art, hooks and organizers without nail holes that cost you deposit money.'),
        ('Fireproof document bag', 'fireproof document bag', 'Keeps your lease, IDs and insurance papers together and protected.'),
    ],
    'home-design': [
        ('Over-the-door organizer', 'over the door organizer', 'Turns the back of any door into storage for shoes, pantry items or cleaning supplies.'),
        ('Under-bed storage bins with wheels', 'under bed storage bins with wheels', 'Uses dead space under the bed for seasonal clothes and linens.'),
        ('Stackable clear storage bins', 'stackable clear storage bins', 'See what is inside at a glance and stack them to use vertical space.'),
        ('Floor mirror', 'full length floor mirror', 'A large mirror bounces light around and makes a small room feel bigger.'),
        ('Peel-and-stick wallpaper', 'peel and stick wallpaper removable', 'Adds pattern and personality to a rental, then peels off at move-out.'),
    ],
    'insurance-claims': [
        ('Fireproof and waterproof document bag', 'fireproof waterproof document bag', 'Protects policies, receipts and your home inventory backup.'),
        ('Water leak detector alarm', 'water leak detector alarm', 'Sounds an alert at the first sign of a leak so damage stays small.'),
        ('Moisture meter', 'moisture meter for walls', 'Shows whether walls and floors are still wet after a leak, useful for documenting damage.'),
        ('Wet/dry shop vacuum', 'wet dry shop vacuum', 'Removes standing water fast, part of your duty to limit further damage.'),
    ],
    'texas-living': [
        ('NOAA weather radio', 'noaa weather radio hand crank', 'Gets emergency alerts even when power and cell service are down.'),
        ('Portable power station', 'portable power station', 'Keeps phones, lights and small fans running during outages, safe to use indoors.'),
        ('Blackout thermal curtains', 'blackout thermal curtains', 'Block Texas sun and heat to keep rooms cooler and bills lower.'),
        ('Tower fan', 'oscillating tower fan', 'Moves air so you can set the thermostat a few degrees higher.'),
        ('Emergency go-bag kit', 'emergency preparedness kit', 'A ready-made start for a hurricane or evacuation kit.'),
    ],
    'lifestyle': [
        ('HEPA air purifier', 'hepa air purifier small room', 'Captures dust, pollen and pet dander in a bedroom or living room.'),
        ('Digital hygrometer', 'digital hygrometer indoor', 'Shows indoor humidity so you can head off mold and dry air.'),
        ('Microfiber cleaning cloths', 'microfiber cleaning cloths', 'Clean most surfaces with just water and wash them for reuse.'),
        ('Essential oil diffuser', 'essential oil diffuser', 'An easy way to add calming or energizing scents to your space.'),
        ('Rechargeable LED lanterns', 'rechargeable led lantern', 'Bright, safe light for outages, no candles needed.'),
    ],
}

# Picks for specific migrated articles.
ARTICLE_PRODUCTS = {
    'smart-home-gadgets-for-apartments': [
        ('Smart lock (no-drill retrofit)', 'smart lock retrofit deadbolt', 'Fits over your existing deadbolt so you can keep the original key cylinder.'),
        ('Smart plugs', 'smart plug wifi', 'Schedule lamps and small appliances from your phone.'),
        ('Smart LED bulbs', 'smart led light bulbs', 'Dim, schedule and change color without new wiring.'),
        ('Robot vacuum', 'robot vacuum', 'Keeps floors tidy on a schedule while you are out.'),
        ('Smart thermostat', 'smart thermostat', 'Learns your schedule; ask your landlord before swapping the thermostat.'),
    ],
    'what-to-do-during-a-power-outage': [
        ('Portable power station', 'portable power station', 'Runs phones, lights and a fan for hours, and is safe to use indoors.'),
        ('Rechargeable LED lanterns', 'rechargeable led lantern', 'Safer than candles and bright enough to move around at night.'),
        ('Power bank', 'portable power bank high capacity', 'Keeps your phone charged for calls and alerts.'),
        ('Hand-crank NOAA weather radio', 'noaa weather radio hand crank', 'Emergency updates when internet and cell service are down.'),
    ],
    'apartment-security-tips': [
        ('Portable door security bar', 'door security bar portable', 'A no-install brace that makes forced entry much harder.'),
        ('Battery video doorbell', 'battery video doorbell no wiring', 'See and talk to visitors from your phone.'),
        ('Window and door alarm sensors', 'window door alarm sensor', 'Loud alerts when a door or window opens.'),
        ('Small home safe', 'small home safe', 'Protects passports, cash and valuables.'),
    ],
    'furnish-an-apartment-for-under-1000': [
        ('Futon or sleeper sofa', 'futon sofa bed', 'Seating by day, guest bed by night.'),
        ('Folding dining table set', 'folding dining table set', 'Saves space when you are not using it.'),
        ('Bed frame with storage', 'bed frame with storage drawers', 'Combines your bed and dresser in one piece.'),
        ('Floor lamp', 'floor lamp', 'Warm, layered light without hardwiring.'),
    ],
    'one-bedroom-apartment-organization-ideas': [
        ('Over-the-door organizer', 'over the door organizer', 'Adds storage without taking floor space.'),
        ('Drawer dividers', 'drawer dividers adjustable', 'Keeps small items sorted so drawers stay tidy.'),
        ('Under-bed storage bins', 'under bed storage bins with wheels', 'Hidden storage for out-of-season items.'),
    ],
    'scents-for-apartment-wellness': [
        ('Essential oil diffuser', 'essential oil diffuser', 'Fills a room with scent without an open flame.'),
        ('Reed diffuser', 'reed diffuser', 'A steady, low-effort scent for small rooms.'),
    ],
}


def php_str(s):
    return "'" + str(s).replace('\\', '\\\\').replace("'", "\\'") + "'"


def php_export(v, ind=0):
    pad = '    ' * ind
    if isinstance(v, dict):
        return '[\n' + ',\n'.join('%s    %s => %s' % (pad, php_str(k), php_export(x, ind + 1)) for k, x in v.items()) + ',\n' + pad + ']'
    if isinstance(v, list):
        return '[\n' + ',\n'.join('%s    %s' % (pad, php_export(x, ind + 1)) for x in v) + ',\n' + pad + ']' if v else '[]'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if v is None:
        return 'null'
    return php_str(v)


def title_card(slug, title, topic):
    """1200x675 gradient card with the topic label, the title and the brand icon."""
    c1, c2, label = TOPIC_STYLE[topic]
    w, h = 1200, 675
    img = Image.new('RGB', (w, h), c1)
    px = img.load()
    for y in range(h):
        for x in range(0, w, 4):
            t = (x / w * 0.65 + y / h * 0.35)
            col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            for dx in range(4):
                if x + dx < w:
                    px[x + dx, y] = col
    d = ImageDraw.Draw(img)
    d.text((80, 90), label.upper(), font=ImageFont.truetype(FONT_B, 30), fill=(255, 255, 255, 220))
    size = 64
    lines = textwrap.wrap(title, 26)
    while len(lines) > 4 and size > 44:
        size -= 6
        lines = textwrap.wrap(title, int(26 * 64 / size))
    f = ImageFont.truetype(FONT_B, size)
    y = 160
    for line in lines[:5]:
        d.text((80, y), line, font=f, fill=(255, 255, 255))
        y += int(size * 1.22)
    icon = Image.open(ICON).convert('RGBA').resize((96, 96), Image.LANCZOS)
    white = Image.new('RGBA', icon.size, (255, 255, 255, 255))
    white.putalpha(icon.getchannel('A'))
    img.paste(white, (80, h - 150), white)
    d.text((196, h - 122), 'my1secret.com', font=ImageFont.truetype(FONT_R, 34), fill=(255, 255, 255))
    path = os.path.join(MEDIA, slug + '.webp')
    img.save(path, 'WEBP', quality=82, method=6)
    return '/media/blog/%s.webp' % slug


def main():
    existing = set()
    with open(os.path.join(SEED, 'articles.php')) as fh:
        existing.update(re.findall(r"'slug' => '([a-z0-9-]+)'", fh.read()))
    photos = json.load(open(os.path.join(SRC, '_images.json'))) if os.path.exists(os.path.join(SRC, '_images.json')) else {}
    files = sorted(f for f in glob.glob(os.path.join(SRC, '*.json')) if not os.path.basename(f).startswith('_'))
    new = [json.load(open(f)) for f in files]
    slugs = existing | {a['slug'] for a in new}
    articles, products, errors = [], [], []
    for i, a in enumerate(new):
        b = a['body_html']
        for link in re.findall(r'href="(/[^"#]*)"', b):
            m = re.match(r'^/blog/([a-z0-9-]+)/$', link)
            if m and m.group(1) not in slugs:
                errors.append('%s: broken internal link %s' % (a['slug'], link))
            elif not m and not re.match(r'^/forum/[a-z-]+/$', link):
                errors.append('%s: unexpected internal link %s' % (a['slug'], link))
        for bad in ('<h1', '<script', ' style=', '<img', '<iframe'):
            if bad in b:
                errors.append('%s: contains %s' % (a['slug'], bad))
        if len(a['seo_title']) > 60 or len(a['meta_description']) > 145:
            errors.append('%s: title/description too long' % a['slug'])
        # external links open in a new tab
        b = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', b)
        text = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', b))).strip()
        ph = photos.get(a['slug'])
        if ph and os.path.exists(os.path.join(MEDIA, a['slug'] + '.webp')):
            image = {'src': '/media/blog/%s.webp' % a['slug'], 'w': ph['w'], 'h': ph['h'], 'alt': a['title'],
                     'credit': ph['credit'], 'credit_url': ph['credit_url']}
        else:
            image = {'src': title_card(a['slug'], a['title'], a['topic']), 'w': 1200, 'h': 675, 'alt': a['title']}
        articles.append({
            'wp_id': None, 'slug': a['slug'], 'legacy_slug': None, 'title': a['title'], 'seo_title': a['seo_title'],
            'meta_description': a['meta_description'], 'excerpt': text[:260].rsplit(' ', 1)[0] + '…', 'topic': a['topic'],
            'author': 'team', 'published_at': '%s %02d:%02d:00' % (PUBLISHED, 2 + i // 4, (i * 13) % 60),
            'updated_at': '%s %02d:%02d:00' % (PUBLISHED, 2 + i // 4, (i * 13) % 60),
            'reading_minutes': max(1, round(len(text.split()) / 230)),
            'image': image, 'body_html': b,
        })
        for p in a['products']:
            products.append({'name': p['name'], 'query': p['query'], 'blurb': p['blurb'], 'tags': 'article:' + a['slug']})
    for slug, items in ARTICLE_PRODUCTS.items():
        assert slug in existing, slug
        products += [{'name': n, 'query': q, 'blurb': b, 'tags': 'article:' + slug} for n, q, b in items]
    for topic, items in TOPIC_PRODUCTS.items():
        products += [{'name': n, 'query': q, 'blurb': b, 'tags': 'topic:' + topic} for n, q, b in items]
    if errors:
        print('\n'.join(errors))
        return 1
    with open(os.path.join(SEED, 'articles-2026-11.php'), 'w') as fh:
        fh.write("<?php\n// Generated by tools/import_articles.py from content/articles-2026-11/. Do not edit by hand.\n"
                 "defined('M1S') || exit;\nreturn " + php_export({'articles': articles}) + ";\n")
    with open(os.path.join(SEED, 'products.php'), 'w') as fh:
        fh.write("<?php\n// Generated by tools/import_articles.py. Amazon product picks (search links; tag added at render).\n"
                 "defined('M1S') || exit;\nreturn " + php_export(products) + ";\n")
    print('articles=%d products=%d' % (len(articles), len(products)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
