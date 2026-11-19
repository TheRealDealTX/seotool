#!/usr/bin/env python3
"""Turn the WordPress export into seed data for the PHP site.

Reads  backup/wordpress-2026-11-19/api/posts.json + media/
Writes public_html/app/seed/articles.php   (34 articles, cleaned HTML)
       public_html/app/seed/legacy.php     (old URL -> new URL / 410 map)
       public_html/media/blog/*.webp       (resized, renamed images)

Run from anywhere:  python3 tools/migrate_wp.py
Needs Pillow. Idempotent: re-running overwrites the outputs.
"""
import html
import json
import os
import re
import sys
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = os.path.join(ROOT, 'backup', 'wordpress-2026-11-19')
OUT_SEED = os.path.join(ROOT, 'public_html', 'app', 'seed')
OUT_MEDIA = os.path.join(ROOT, 'public_html', 'media', 'blog')
MAX_W = 1400

# Blog topics (replace the old WordPress categories + tags)
TOPICS = [
    ('renting', 'Renting & Apartment Life', 'Apartment Living Tips & Renting Advice',
     'Practical apartment living tips: finding a place, saving on rent, moving, security, and getting along with neighbors and roommates.'),
    ('home-design', 'Small-Space Design', 'Small Apartment Design & Organization Ideas',
     'Small apartment design, budget furnishing, and organization ideas that make any rental feel bigger and work harder.'),
    ('insurance-claims', 'Insurance & Claims', 'Renters & Homeowners Insurance Claim Help',
     'Plain-English guides to renters and homeowners insurance claims, storm damage, appraisal, and when a public adjuster can help.'),
    ('texas-living', 'Texas Living', 'Texas Living: Cities, Apartments & Moving Guides',
     'Guides to living in Texas: Houston, Dallas, Leander and Lewisville apartments, Texas weather, moving, and travel on a budget.'),
    ('lifestyle', 'Lifestyle & Wellness', 'Lifestyle, Wellness & Productivity Tips',
     'Everyday lifestyle secrets: wellness at home, time-saving habits, nature therapy, and staying ready for the unexpected.'),
]

# WordPress post id -> (new slug, SEO <title>, H1, meta description, topic)
POSTS = {
    322: ('best-time-to-buy-or-sell-a-house',
          'Best Time to Buy or Sell a House: Real Estate Timing Secrets',
          'The Secret Power of Timing in Real Estate',
          'When to buy or sell a house: how market cycles, seasons, interest rates and life events decide whether you get a great deal or regret it.',
          'renting'),
    318: ('psychology-of-decorating-a-rental',
          'The Psychology of Decorating a Rental',
          'The Secret Psychology Behind Decorating a Rental',
          'Why decorating a rental matters more than you think: control, comfort, identity, and mood, plus renter-friendly ways to make a space your own.',
          'home-design'),
    314: ('one-bedroom-apartment-organization-ideas',
          'One-Bedroom Apartment Organization Ideas That Actually Work',
          'The Secret Formula for Staying Organized in a One-Bedroom',
          'Keep a one-bedroom organized with zoning, vertical and hidden storage, multipurpose furniture and small daily habits that stop clutter.',
          'home-design'),
    310: ('insurance-appraisal-tips',
          'Insurance Appraisal Tips That Could Save You Thousands',
          'Little-Known Insurance Appraisal Tips That Could Save You Thousands',
          'How the insurance appraisal clause works, when to invoke it, how to choose an appraiser, and mistakes that cost homeowners money on a claim.',
          'insurance-claims'),
    305: ('roommates-renters-insurance-claim',
          'Roommates & Renters Insurance: One Claim or Separate Claims?',
          'Should Roommates File One Claim or Separate Ones?',
          'Does one renters insurance policy cover every roommate? When roommates should file one claim or separate ones, and how to document a shared loss.',
          'insurance-claims'),
    301: ('long-distance-apartment-move-checklist',
          'Long-Distance Apartment Move Checklist: A Renter\'s Roadmap',
          'Planning a Long-Distance Apartment Move: A Renter\'s Roadmap',
          'A step-by-step plan for a long-distance apartment move: budgeting, choosing a place sight unseen, movers vs. DIY, and settling in smoothly.',
          'renting'),
    297: ('apartment-living-with-teenagers',
          'Apartment Living With Teenagers: Space & Privacy Tips',
          'Apartment Living with Teenagers: Space and Privacy Tips',
          'How to give teenagers space and privacy in an apartment: personal zones, smart storage, quiet hours, tech-free areas, and shared decisions.',
          'renting'),
    293: ('scents-for-apartment-wellness',
          'How Scent Can Boost Wellness in Your Apartment',
          'How Scent Can Boost Wellness in Apartments',
          'The right scents can calm, energize, and make a rental feel like home. Which aromas to use where, and how to scent an apartment safely.',
          'lifestyle'),
    289: ('public-adjuster-for-property-investors',
          'Protecting Your Property Investment With a Public Adjuster',
          'Protecting Your Property Investment with a Public Adjuster',
          'What a public adjuster does for property owners after fire, flood, or storm damage, when to hire one, and what to look for before you sign.',
          'insurance-claims'),
    285: ('how-public-adjusters-help-with-insurance-claims',
          'How Public Adjusters Help You Get a Fair Insurance Claim',
          'How Public Adjusters Help Level the Playing Field with Insurance Companies',
          'Why insurers have the upper hand on claims, how a licensed public adjuster evens the odds, and when it makes sense to hire one.',
          'insurance-claims'),
    278: ('small-apartment-design-ideas',
          'Small Apartment Design Ideas That Make Your Space Feel Huge',
          'Design Secrets That Make Small Apartments Feel Huge',
          'Light colors, mirrors, multifunctional furniture, vertical storage, and zoning: small apartment design ideas that make a studio feel open.',
          'home-design'),
    274: ('furnish-an-apartment-for-under-1000',
          'How to Furnish an Apartment for Under $1,000',
          'How to Furnish an Apartment for Under $1,000',
          'Furnish a whole apartment for under $1,000: what to buy first, a sample budget breakdown, where to find deals, and how to decorate for less.',
          'home-design'),
    266: ('apartment-living-tips',
          'Apartment Living Tips Nobody Tells You Before Move-In',
          'What No One Tells You About Apartment Life, Until Now',
          'Noise, maintenance, neighbors, renters insurance and more: honest apartment living tips nobody mentions until after you sign the lease.',
          'renting'),
    260: ('spring-branch-houston-apartments',
          'Spring Branch Houston: Why Renters Are Moving Here',
          'Houston\'s Hidden Treasure: Why Renters Are Flocking to Spring Branch',
          'Why Spring Branch is one of Houston\'s most popular neighborhoods for renters: location, apartments for every budget, schools, food, and culture.',
          'texas-living'),
    254: ('renters-storm-damage-claim',
          'Storm Damage in a Rental: What Renters Should Know',
          'Post-Storm Rentals: What Renters Should Know About Property Damage and Adjusters',
          'After a storm damages your rental, who pays for what? Landlord vs. renter duties, filing a renters insurance claim, and adjusters explained.',
          'insurance-claims'),
    250: ('best-time-of-year-to-rent-an-apartment',
          'Best Time of Year to Rent an Apartment for Lower Prices',
          'The Best Time of Year to Rent an Apartment for Lower Prices',
          'Which months have the cheapest rent and why, plus negotiating tips to get a better apartment deal no matter when you sign your lease.',
          'renting'),
    244: ('what-to-do-during-a-power-outage',
          'What to Do During a Power Outage at Home',
          'What to Do If You Have a Power Outage at Home',
          'How to prepare for a power outage, stay safe and comfortable while the lights are out, and what to check when the power comes back on.',
          'lifestyle'),
    239: ('texas-travel-tips-on-a-budget',
          'Texas on a Budget: Travel Tips & Hacks to Cut Your Costs',
          'Travel Smart: Top Tips and Hacks to Cut Your Expenses When Traveling to Texas',
          'Save money traveling in Texas: when to book flights, cheap ways to get around, affordable stays, eating like a local, and free attractions.',
          'texas-living'),
    231: ('public-adjuster-for-texas-condo-complex',
          'Should You Hire a Public Adjuster for a Texas Condo Complex?',
          'Should You Trust a Public Adjuster for Your Texas Condo Complex?',
          'How Texas condo associations can vet a public adjuster: licensing, red flags, unrealistic promises and why complex claims need expert help.',
          'insurance-claims'),
    219: ('moving-to-houston-tx',
          'Moving to Houston, TX: Why It\'s a Great Place to Start Over',
          'Why Houston, TX Is the Perfect Place to Start Your New Life',
          'Thinking about moving to Houston? Jobs, cost of living, neighborhoods, and some of the best Houston apartments for a fresh start.',
          'texas-living'),
    210: ('texas-climate-regions-guide',
          'Texas Climate Regions Explained: A Guide to Texas Weather',
          'Understanding the Diverse Climates of Texas: A Comprehensive Guide',
          'From the humid Gulf Coast to the Trans-Pecos desert: a guide to the climate regions of Texas, seasonal weather, and storm risks in each.',
          'texas-living'),
    206: ('apartments-with-renewable-energy',
          'Apartments With Renewable Energy: Benefits for Renters',
          'Apartments with Renewable Energy Sources: A Look at the Benefits',
          'Solar, wind and geothermal apartments can mean lower bills, cleaner living, and more resilient power. The real benefits for renters.',
          'renting'),
    202: ('social-media-and-apartment-living',
          'How Social Media Is Changing Apartment Living',
          'The Role of Social Media in Apartment Living',
          'From apartment hunting to resident groups and decor inspiration, here is how social media is changing the way people rent and live.',
          'renting'),
    198: ('functional-apartment-design-busy-lifestyle',
          'Functional Apartment Design for Busy City Lifestyles',
          'Urban Living: Designing a Functional Apartment for Busy Lifestyles',
          'Design an apartment that keeps up with a busy life: multifunctional furniture, smart storage, activity zones, lighting, and helpful tech.',
          'home-design'),
    194: ('smart-home-gadgets-for-apartments',
          'Best Smart Home Gadgets for Apartments',
          'Top Smart Gadgets to Make Apartment Living Easier',
          'Renter-friendly smart gadgets that make apartment life easier: smart locks, thermostats, bulbs, plugs, video doorbells, robot vacuums and more.',
          'home-design'),
    184: ('dallas-apartments-with-the-best-ac',
          'Dallas Apartments With the Best AC for Hot Texas Summers',
          'Cool Living in Dallas: Apartments with the Best AC for Hot Summers',
          'Beat 100-degree Dallas summers: apartments known for strong, efficient air conditioning, and what to ask about AC before you sign a lease.',
          'texas-living'),
    176: ('apartment-community-wifi-benefits',
          'Community Wi-Fi in Apartments: Benefits & Is It Worth It?',
          'The Benefits of Choosing an Apartment with Community Wi-Fi',
          'Is building-wide Wi-Fi worth it? The cost savings, convenience, coverage, and trade-offs of choosing an apartment with community Wi-Fi.',
          'renting'),
    172: ('apartment-community-events-and-amenities',
          'Apartment Community Events & Social Amenities',
          'Apartment Communities with Events: How Social Amenities Change Living Spaces',
          'Resident events, fitness programs, pet meetups and shared spaces are changing apartment life. What social amenities are worth looking for.',
          'renting'),
    168: ('apartment-security-tips',
          'Apartment Security Tips to Keep Your New Home Safe',
          'Top Apartment Security Tips: Keeping Your New Home Safe',
          'Practical apartment security tips: check building security, upgrade locks, add a doorbell camera, secure windows, and protect your belongings.',
          'renting'),
    158: ('best-1-and-2-bedroom-apartments-houston',
          'Best 1 & 2-Bedroom Apartments in Houston for Every Lifestyle',
          'Houston Hideaways: The Best 1 and 2-Bedroom Apartments for Every Lifestyle',
          'Our picks for Houston 1- and 2-bedroom apartments, from Cypress to Westchase and Midtown, with what makes each community stand out.',
          'texas-living'),
    154: ('time-saving-tips-for-busy-professionals',
          '10 Time-Saving Tips for Busy Professionals',
          '10 Time-Saving Tips and Tricks for Busy Professionals',
          'Ten proven time-saving tips for busy professionals: the Eisenhower matrix, time blocking, the two-minute rule, batching, automation and more.',
          'lifestyle'),
    145: ('forest-bathing-benefits',
          'Forest Bathing Benefits: The Nature Therapy You Need',
          'Why Forest Bathing Is the Nature Therapy You Didn\'t Know You Needed',
          'What forest bathing is, the science behind its mental health benefits, and how to practice it, even if you live in the city.',
          'lifestyle'),
    131: ('leander-tx-apartments-with-pools',
          'Best Leander, TX Apartments With Luxury Pools',
          'The Best Leander, TX Apartments Featuring Luxury Pools',
          'Beat the Texas heat in Leander: apartment communities with resort-style and luxury pools, plus what else each one offers residents.',
          'texas-living'),
    126: ('new-apartments-in-lewisville-tx',
          'New Apartments in Lewisville, TX Worth Touring',
          'New Apartments in Lewisville, TX to Consider for Your Next Move',
          'Lewisville is booming. Here are new apartment communities between Dallas and Fort Worth worth touring before your next move.',
          'texas-living'),
}

# Old category / tag archive URLs -> new topic (None = blog index)
OLD_ARCHIVES = {
    '/topics/discussion/': '/blog/',
    '/topics/real-estate/': '/blog/topic/renting/',
    '/topics/activity/': '/blog/',
    '/topics/others/': '/blog/',
    '/categories/feeling-good/': '/blog/topic/lifestyle/',
    '/categories/food/': '/blog/topic/lifestyle/',
    '/categories/health/': '/blog/topic/lifestyle/',
    '/categories/hobbies/': '/blog/topic/lifestyle/',
    '/categories/general/': '/blog/',
    '/categories/parenting/': '/blog/topic/renting/',
    '/categories/travel/': '/blog/topic/texas-living/',
    '/categories/lgbt/': '/forum/',
    '/categories/movies-tv/': '/forum/',
    '/categories/relationships/': '/forum/',
    '/discussion/author/meagan/': '/author/meagan/',
    '/discussion/': '/blog/',
}

TRACKING = re.compile(r'^(utm_|gclid|gclsrc|gad_source|gbraid|wbraid|fbclid|campaign$|verified$)')


def clean_url(u):
    u = html.unescape(u)
    s = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True) if not TRACKING.match(k)]
    return urlunsplit((s.scheme, s.netloc, s.path, urlencode(q), ''))


def slugify(s):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:70].strip('-')


def convert_image(src_name, dest_base):
    """Resize + convert one media file to WebP. Returns (path, w, h) or None."""
    src = os.path.join(BACKUP, 'media', src_name)
    if not os.path.exists(src):
        return None
    im = Image.open(src)
    im = im.convert('RGBA') if im.mode in ('P', 'LA', 'RGBA') else im.convert('RGB')
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    name = dest_base + '.webp'
    im.save(os.path.join(OUT_MEDIA, name), 'WEBP', quality=80, method=6)
    return '/media/blog/' + name, im.width, im.height


def media_name(url):
    """WordPress size variants (foo-768x512.jpg) -> original file name in the backup."""
    base = os.path.basename(urlsplit(url).path)
    if os.path.exists(os.path.join(BACKUP, 'media', base)):
        return base
    orig = re.sub(r'-\d+x\d+(?=\.\w+$)', '', base)
    if os.path.exists(os.path.join(BACKUP, 'media', orig)):
        return orig
    scaled = re.sub(r'(?=\.\w+$)', '-scaled', orig)
    if os.path.exists(os.path.join(BACKUP, 'media', scaled)):
        return scaled
    return None


legacy_media = {}   # old /wp-content/uploads path -> new /media path


def clean_body(raw, slug, title):
    h = raw
    # strip editor junk attributes
    h = re.sub(r'\s(?:data-[\w-]+|class|id|style|dir|aria-[\w-]+|loading|decoding|fetchpriority|sizes|srcset)="[^"]*"', '', h)
    h = re.sub(r'<span>(.*?)</span>', r'\1', h, flags=re.S)
    h = re.sub(r'</?(?:div|figure|figcaption)[^>]*>', '\n', h)
    h = re.sub(r'<!--.*?-->', '', h, flags=re.S)
    h = re.sub(r'<h1(\W)', r'<h2\1', h).replace('</h1>', '</h2>')
    # emojis / stray chars at heading starts
    h = re.sub(r'(<h[23][^>]*>)\s*[☀-⟿\U0001F000-\U0001FFFF️‍]+\s*', r'\1', h)
    # empty headings / paragraphs
    h = re.sub(r'<(h[2-4]|p)>\s*(?:&nbsp;|<br\s*/?>)*\s*</\1>', '', h)
    h = re.sub(r'<strong>\s*</strong>', '', h)
    h = re.sub(r'(<h[2-4]>)(.*?)(</h[2-4]>)',
               lambda m: m.group(1) + re.sub(r'</?(?:strong|b|em)>', '', m.group(2)).strip().rstrip(':') + m.group(3), h, flags=re.S)

    # links
    def fix_link(m):
        attrs = m.group(1)
        href = re.search(r'href="([^"]+)"', attrs)
        if not href:
            return '<a>'
        u = href.group(1)
        if 'my1secret.com' in u:
            path = urlsplit(html.unescape(u)).path
            old = re.match(r'^/discussion/([^/]+)/?$', path)
            for pid, info in POSTS.items():
                if old and SLUG_BY_ID.get(pid) == old.group(1):
                    return '<a href="/blog/%s/">' % info[0]
            return '<a href="%s">' % (path or '/')
        u = clean_url(u)
        return '<a href="%s" target="_blank" rel="noopener">' % html.escape(u, quote=True)
    h = re.sub(r'<a\s([^>]*)>', fix_link, h)

    # images
    n = [0]

    def fix_img(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        if not src:
            return ''
        name = media_name(src.group(1))
        if not name:
            return ''
        n[0] += 1
        res = convert_image(name, '%s-%d' % (slug, n[0]))
        if not res:
            return ''
        path, w, hgt = res
        legacy_media[urlsplit(src.group(1)).path] = path
        legacy_media['/wp-content/uploads/' + name] = path
        a = html.unescape(alt.group(1)).strip() if alt and alt.group(1).strip() else ''
        if not a:
            a = re.sub(r'[-_]+', ' ', os.path.splitext(name)[0]).replace(' scaled', '').strip()
        return '<img src="%s" alt="%s" width="%d" height="%d" loading="lazy">' % (path, html.escape(a, quote=True), w, hgt)
    h = re.sub(r'<img[^>]*>', fix_img, h)
    h = re.sub(r'<p>\s*(<img[^>]+>)\s*</p>', r'<figure>\1</figure>', h)
    h = re.sub(r'(?m)^\s*(<img[^>]+>)\s*$', r'<figure>\1</figure>', h)

    h = re.sub(r'\n{2,}', '\n', h).strip()
    return h


def php_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def php_export(v, ind=0):
    pad = '    ' * ind
    if isinstance(v, dict):
        items = ['%s    %s => %s' % (pad, php_str(str(k)), php_export(x, ind + 1)) for k, x in v.items()]
        return '[\n' + ',\n'.join(items) + ',\n' + pad + ']'
    if isinstance(v, list):
        items = ['%s    %s' % (pad, php_export(x, ind + 1)) for x in v]
        return '[\n' + ',\n'.join(items) + ',\n' + pad + ']' if items else '[]'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if v is None:
        return 'null'
    return php_str(str(v))


SLUG_BY_ID = {}


def main():
    os.makedirs(OUT_SEED, exist_ok=True)
    os.makedirs(OUT_MEDIA, exist_ok=True)
    posts = json.load(open(os.path.join(BACKUP, 'api', 'posts.json')))
    for p in posts:
        SLUG_BY_ID[p['id']] = p['slug']

    articles, redirects, gone = [], {}, []
    for p in posts:
        old_path = '/discussion/%s/' % p['slug']
        if p['id'] not in POSTS:
            gone.append(old_path)
            continue
        slug, seo_title, h1, desc, topic = POSTS[p['id']]
        assert len(desc) <= 145, (slug, len(desc))
        assert len(seo_title) <= 60, (slug, len(seo_title))
        body = clean_body(p['content']['rendered'], slug, h1)
        text = re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', body))).strip()
        words = len(text.split())
        excerpt = text[:260].rsplit(' ', 1)[0] + '…'

        img = None
        fm = (p.get('_embedded') or {}).get('wp:featuredmedia') or []
        if fm and fm[0].get('source_url'):
            name = media_name(fm[0]['source_url'])
            if name:
                res = convert_image(name, slug)
                if res:
                    alt = html.unescape(fm[0].get('alt_text') or '').strip() or h1
                    img = {'src': res[0], 'w': res[1], 'h': res[2], 'alt': alt}
                    legacy_media[urlsplit(fm[0]['source_url']).path] = res[0]
                    for size in ((fm[0].get('media_details') or {}).get('sizes') or {}).values():
                        if size.get('source_url'):
                            legacy_media[urlsplit(size['source_url']).path] = res[0]
        articles.append({
            'wp_id': p['id'],
            'slug': slug,
            'legacy_slug': p['slug'],
            'title': h1,
            'seo_title': seo_title,
            'meta_description': desc,
            'excerpt': excerpt,
            'topic': topic,
            'author': 'meagan',
            'published_at': p['date_gmt'].replace('T', ' '),
            'updated_at': p['modified_gmt'].replace('T', ' '),
            'reading_minutes': max(1, round(words / 230)),
            'image': img,
            'body_html': body,
        })
        redirects[old_path] = '/blog/%s/' % slug
        redirects['/%s/' % p['slug']] = '/blog/%s/' % slug   # bare-slug variant
        redirects['/?p=%d' % p['id']] = '/blog/%s/' % slug

    redirects.update(OLD_ARCHIVES)
    articles.sort(key=lambda a: a['published_at'])

    with open(os.path.join(OUT_SEED, 'articles.php'), 'w') as f:
        f.write("<?php\n// Generated by tools/migrate_wp.py from the WordPress export. Do not edit by hand.\n"
                "defined('M1S') || exit;\nreturn " + php_export({'topics': [
                    {'slug': t[0], 'name': t[1], 'seo_title': t[2], 'description': t[3], 'sort': i}
                    for i, t in enumerate(TOPICS)], 'articles': articles}) + ";\n")
    with open(os.path.join(OUT_SEED, 'legacy.php'), 'w') as f:
        f.write("<?php\n// Generated by tools/migrate_wp.py. Old WordPress URLs.\n"
                "// 'redirect': 301 targets. 'gone': thin/off-topic posts removed for good (410).\n"
                "defined('M1S') || exit;\nreturn " + php_export({
                    'redirect': redirects, 'gone': sorted(gone),
                    'media': dict(sorted(legacy_media.items()))}) + ";\n")
    print('articles=%d redirects=%d gone=%d media_map=%d images=%d' % (
        len(articles), len(redirects), len(gone), len(legacy_media), len(os.listdir(OUT_MEDIA))))


if __name__ == '__main__':
    sys.exit(main())
