#!/usr/bin/env python3
"""QA against a running copy of the site: status codes, PHP errors, one H1, keyword counts.

Usage: python3 tools/check.py [base_url]   (default http://127.0.0.1:8099)
Keyword counts are over visible text (head, scripts and styles removed), case-insensitive.
"""
import html, json, re, sys, urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8099').rstrip('/')
PAGES = ['/', '/about/', '/twia-claims-expert/', '/galveston-fire-claims/', '/calculators/', '/texas-windstorm-rules/',
         '/galveston-local-code/', '/galveston-storm-history/', '/weather-events/', '/blog/', '/contact/', '/privacy-policy/']
TARGETS = {'/': {'galveston public adjuster': 14, 'twia expert': 4}, '/twia-claims-expert/': {'twia expert': 14}}

def get(p):
    with urllib.request.urlopen(BASE + p) as r:
        return r.read().decode()

def visible(doc):
    doc = re.sub(r'(?is)<head.*?</head>|<script.*?</script>|<style.*?</style>', ' ', doc)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', doc))).lower()

bad = 0
posts = re.findall(r'<loc>[^<]*(/blog/[^<]+/)</loc>', get('/sitemap.xml'))
for p in PAGES + posts:
    doc = get(p)
    errs = re.findall(r'(Warning|Notice|Fatal error|Deprecated)</b>:|(Warning|Deprecated|Fatal error): ', doc)
    h1 = len(re.findall(r'<h1[\s>]', doc))
    title = re.search(r'<title>(.*?)</title>', doc).group(1)
    ld = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S)]
    t = visible(doc)
    counts = {k: len(re.findall(re.escape(k), re.sub(r'\s+', ' ', t))) for k in ('galveston public adjuster', 'twia expert')}
    flag = []
    if errs: flag.append('PHP-ERR')
    if h1 != 1: flag.append(f'H1={h1}')
    for k, want in TARGETS.get(p, {}).items():
        if counts[k] != want: flag.append(f'{k}={counts[k]}≠{want}')
    bad += bool(flag)
    if 'type="application/rss+xml"' not in doc: flag.append('NO-RSS-LINK')
    print(f"{'FAIL' if flag else 'ok  '} {p:55} gpa={counts['galveston public adjuster']:2} twia={counts['twia expert']:2} title={len(title):2} {' '.join(flag)}")

# Sitemap: every <lastmod> is a real date, never in the future, never before launch (see PAGE_UPDATED in inc/config.php).
import datetime
today = datetime.date.today().isoformat()
sm = get('/sitemap.xml')
dates = re.findall(r'<lastmod>([^<]*)</lastmod>', sm)
smflag = [d for d in dates if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d) or d > today or d < '2026-09-28']
if len(dates) != sm.count('<url>'): smflag.append('missing lastmod')
bad += bool(smflag)
print(f"{'FAIL' if smflag else 'ok  '} /sitemap.xml ({len(dates)} urls, lastmod {min(dates)}..{max(dates)}) {' '.join(smflag)}")
sys.exit(1 if bad else 0)
