#!/usr/bin/env python3
"""Shorten <title> (<=65 chars) and meta descriptions (<=158) and fix the one blog H1 without a location.
Rules: drop the phone-number suffix from titles; drop the brand suffix from blog titles; then explicit
overrides for the handful still over the limit. og:title / og:description are kept in sync. Idempotent."""
import os, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'_old-site', 'tools', '.git', 'wp-content'}
PHONE_SUFFIX = ' | (832) 503-5866'
BRAND_SUFFIX = ' | San Antonio Public Adjuster'

TITLE_OVERRIDES = {
    'blog/acv-vs-rcv-insurance-check-explained/index.html': 'ACV vs. RCV in San Antonio: Why the First Check Is Smaller',
    'service-areas/index.html': 'San Antonio Public Adjuster Service Areas | Bexar County & Beyond',
    'service-areas/downtown-san-antonio-public-adjuster/index.html': 'Downtown & Central San Antonio Public Adjuster | Storm Claims',
    'services/commercial-property-claims/index.html': 'San Antonio Commercial Public Adjuster | Business & Rental Claims',
    'services/denied-insurance-claims/index.html': 'Denied Insurance Claims | San Antonio Public Adjuster',
    'services/fire-smoke-damage-claims/index.html': 'San Antonio Fire Damage Public Adjuster | Fire & Smoke Claims',
    'services/underpaid-insurance-claims/index.html': 'San Antonio Underpaid Insurance Claim Help | Supplemental Claims',
    'services/water-damage-claims/index.html': 'San Antonio Water Damage Public Adjuster | Plumbing Leak Claims',
    'services/wind-storm-damage-claims/index.html': 'San Antonio Wind Damage Public Adjuster | Wind & Storm Claims',
}
DESC_OVERRIDES = {
    'about/index.html': 'San Antonio Public Adjuster is a trade name of Rise Public Adjusting LLC, TDI license #3356839. We represent policyholders only on hail, wind, water and fire claims.'
        .replace('We represent policyholders only on hail, wind, water and fire claims.', 'Policyholders only: hail, wind, water and fire claims.'),
    'home.html': 'Licensed San Antonio public adjuster for hail, wind, water, fire, denied and underpaid claims across Bexar County. Free claim review, no upfront fee.',
    'service-areas/index.html': 'Our San Antonio public adjusters serve every part of San Antonio plus Converse, Live Oak, Schertz, Cibolo, New Braunfels, Boerne, Helotes and more.',
    'services/index.html': 'Claim services from a licensed San Antonio public adjuster: hail, wind, water, fire, roof, denied, underpaid, appraisal and commercial property claims.',
}
H1_FIX = ('blog/acv-vs-rcv-insurance-check-explained/index.html',
          'ACV vs. RCV: Why Your First Insurance Check Is Smaller Than the Estimate',
          'ACV vs. RCV: Why Your First San Antonio Insurance Check Is Smaller Than the Estimate')

def esc(s):  # match the generator's escaping (&amp; and &#x27;)
    return s.replace('&', '&amp;').replace("'", '&#x27;')

def pages():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.relpath(os.path.join(dp, fn), ROOT).replace(os.sep, '/')

n = 0
for rel in sorted(pages()):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding='utf-8').read(); orig = t
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    if m:
        old_raw = m.group(1); old = H.unescape(old_raw)
        new = TITLE_OVERRIDES.get(rel)
        if new is None:
            new = old
            if new.endswith(PHONE_SUFFIX): new = new[:-len(PHONE_SUFFIX)]
            if rel.startswith('blog/') and rel != 'blog/index.html' and new.endswith(BRAND_SUFFIX):
                new = new[:-len(BRAND_SUFFIX)]
        if new != old:
            t = t.replace(f'<title>{old_raw}</title>', f'<title>{esc(new)}</title>')
            t = t.replace(f'<meta property="og:title" content="{old_raw}">', f'<meta property="og:title" content="{esc(new)}">')
    if rel in DESC_OVERRIDES:
        m = re.search(r'<meta name="description" content="([^"]*)"', t)
        if m and m.group(1) != esc(DESC_OVERRIDES[rel]):
            t = t.replace(f'content="{m.group(1)}"', f'content="{esc(DESC_OVERRIDES[rel])}"')
    if rel == H1_FIX[0]:
        t = re.sub(r'(<h1[^>]*>)' + re.escape(H1_FIX[1]) + '(</h1>)', r'\g<1>' + H1_FIX[2] + r'\g<2>', t)
        # keep the JSON-LD headline in step with the H1
        t = t.replace('"headline":"' + H1_FIX[1] + '"', '"headline":"' + H1_FIX[2] + '"')
    if t != orig:
        open(p, 'w', encoding='utf-8').write(t); n += 1
print(f'fix_meta: {n} files changed')
