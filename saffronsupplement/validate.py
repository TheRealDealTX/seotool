#!/usr/bin/env python3
"""Crawl every route on a running copy of the site and check SEO + link basics.

Usage: php -S 127.0.0.1:8099 index.php &   then   python3 validate.py [base_url]
"""
import json, re, sys, urllib.request, urllib.error, html
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8099").rstrip("/")
TAG = "saffronsupplement-20"
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
errors, seen_titles, seen_desc = [], {}, {}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.bad=[]; s.links=[]; s.ids=[]; s.h1=0; s.ld=[]; s._ld=False; s.title=""; s._t=False; s.desc=None
    def handle_starttag(s, t, a):
        a=dict(a)
        if t not in VOID: s.stack.append(t)
        if t=="a" and a.get("href"): s.links.append((a["href"], a.get("rel","")))
        if a.get("id"): s.ids.append(a["id"])
        if t=="h1": s.h1+=1
        if t=="script" and a.get("type")=="application/ld+json": s._ld=True; s.ld.append("")
        if t=="title": s._t=True
        if t=="meta" and a.get("name")=="description": s.desc=a.get("content")
    def handle_endtag(s, t):
        if t in VOID: return
        if t=="script": s._ld=False
        if t=="title": s._t=False
        if s.stack and s.stack[-1]==t: s.stack.pop()
        else: s.bad.append(f"</{t}> (open: {s.stack[-3:]})")
    def handle_data(s, d):
        if s._ld: s.ld[-1]+=d
        if s._t: s.title+=d

def get(path):
    req=urllib.request.Request(BASE+path, headers={"User-Agent":"validate"})
    class NR(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**k): return None
    op=urllib.request.build_opener(NR)
    try:
        r=op.open(req); return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")

status, sm = get("/sitemap.xml")
paths=[u.replace("https://saffronsupplement.com","") for u in re.findall(r"<loc>(.*?)</loc>", sm)]
print(f"{len(paths)} URLs in sitemap")
internal=set(); amz=0
for p in paths:
    st, body = get(p)
    if st!=200: errors.append(f"{p}: HTTP {st}"); continue
    if re.search(r"(Warning|Notice|Fatal error|Deprecated)</b>:|on line <b>", body): errors.append(f"{p}: PHP error output")
    x=P(); x.feed(body)
    if x.bad: errors.append(f"{p}: tag nesting {x.bad[:3]}")
    if x.h1!=1: errors.append(f"{p}: {x.h1} h1")
    if not x.desc or not (70<=len(x.desc)<=170): errors.append(f"{p}: meta description length {len(x.desc or '')}")
    if len(x.title)>65: errors.append(f"{p}: title {len(x.title)} chars")
    if x.title in seen_titles: errors.append(f"{p}: duplicate title with {seen_titles[x.title]}")
    seen_titles[x.title]=p
    if x.desc in seen_desc: errors.append(f"{p}: duplicate description")
    seen_desc[x.desc]=p
    dup=[i for i in set(x.ids) if x.ids.count(i)>1]
    if dup: errors.append(f"{p}: duplicate ids {dup}")
    for blob in x.ld:
        try: json.loads(blob)
        except Exception as e: errors.append(f"{p}: bad JSON-LD {e}")
    for href, rel in x.links:
        if "amazon." in href:
            amz+=1
            if f"tag={TAG}" not in href: errors.append(f"{p}: amazon link without tag {href}")
            if "sponsored" not in rel: errors.append(f"{p}: amazon link missing rel=sponsored")
        elif href.startswith("/"): internal.add(href.split("#")[0])
for h in sorted(internal):
    st,_=get(h)
    if st!=200: errors.append(f"internal link {h}: HTTP {st}")
for path, want in [("/nope/",404),("/contact-us/",301),("/best-saffron-supplements",301),("/robots.txt",200),("/assets/css/style.css",200),("/favicon.svg",200),("/app/config.php",None)]:
    st, body = get(path)
    if want and st!=want: errors.append(f"{path}: expected {want}, got {st}")
    if path.startswith("/app/") and body.strip(): errors.append(f"{path}: app file leaks output")
print(f"{len(internal)} internal links checked, {amz} Amazon links checked")
print("\n".join(errors) if errors else "OK: no errors")
sys.exit(1 if errors else 0)
