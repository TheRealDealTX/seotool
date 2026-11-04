#!/usr/bin/env python3
"""Flag titles over 55 chars / 540px (Arial 20px) and descriptions over 150 chars.

Usage: python3 tools/meta_report.py [base-url]  (default: local preview)
"""
import re, sys, html, urllib.request
from PIL import ImageFont
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080'
try: font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', 20)  # metric-compatible with Arial
except Exception: font = None
px = lambda s: round(font.getlength(s)) if font else len(s) * 9
sm = urllib.request.urlopen(BASE + '/sitemap.xml').read().decode()
bad = 0
for u in re.findall(r'<loc>https://solarcctvcamera\.com([^<]+)</loc>', sm):
    b = urllib.request.urlopen(BASE + u).read().decode()
    t = html.unescape(re.search(r'<title>(.*?)</title>', b, re.S).group(1))
    d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', b).group(1))
    flag = []
    if len(t) > 55 or px(t) > 540: flag.append(f'TITLE {len(t)}c/{px(t)}px')
    if len(d) > 150: flag.append(f'DESC {len(d)}c')
    if flag: bad += 1; print(u, '|', ' '.join(flag), '|', t)
print('pages over limit:', bad)
