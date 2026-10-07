#!/usr/bin/env python3
"""Post-build checks for public/: structure, SEO basics, links, assets, legacy URL coverage."""
import json, os, re, subprocess, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
errors, warnings = [], []
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.bad=[]; s.h1=0; s.links=[]; s.imgs=[]; s.ld=[]; s._ld=False; s.buf=""
        s.title=""; s._t=False; s.desc=None; s.canon=None; s.ids=[]
    def handle_starttag(s, t, a):
        a=dict(a)
        if t not in VOID: s.stack.append(t)
        if t=="h1": s.h1+=1
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t=="img":
            s.imgs.append(a.get("src"))
            if a.get("alt") is None: s.bad.append("img without alt")
        if t=="link" and a.get("rel")=="stylesheet" and a.get("href","").startswith("/"): s.links.append(a["href"])
        if t=="script" and a.get("type")=="application/ld+json": s._ld=True; s.buf=""
        if t=="title": s._t=True
        if t=="meta" and a.get("name")=="description": s.desc=a.get("content")
        if t=="link" and a.get("rel")=="canonical": s.canon=a.get("href")
        if a.get("id"): s.ids.append(a["id"])
    def handle_endtag(s, t):
        if t=="script" and s._ld: s.ld.append(s.buf); s._ld=False
        if t=="title": s._t=False
        if t in VOID: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        elif t in s.stack:
            while s.stack[-1]!=t: s.bad.append(f"unclosed <{s.stack.pop()}>")
            s.stack.pop()
        else: s.bad.append(f"stray </{t}>")
    def handle_data(s, d):
        if s._ld: s.buf+=d
        if s._t: s.title+=d

def site_path(fs):
    rel=os.path.relpath(fs,PUB).replace(os.sep,"/")
    if rel=="home.html": return "/"
    return "/"+rel[:-10] if rel.endswith("index.html") else "/"+rel

redir = {}
for m in re.finditer(r'^\s+"([^"]+)" => "([^"]*)",', open(os.path.join(PUB,"redirects.php")).read(), re.M):
    redir[m.group(1)] = m.group(2)

def exists(path):
    path=unquote(path.split("#")[0].split("?")[0])
    if path in ("/", "/feed/"): return True
    fs=os.path.join(PUB,path.lstrip("/"))
    if os.path.isfile(fs): return True
    if os.path.isfile(os.path.join(fs,"index.html")): return True
    return False

titles, descs = {}, {}
pages = []
for dp,_,fs in os.walk(PUB):
    if "/assets" in dp or "/wp-content" in dp: continue
    for f in fs:
        if f.endswith(".html"): pages.append(os.path.join(dp,f))
for fp in pages:
    sp=site_path(fp); html=open(fp,encoding="utf-8").read(); p=P(); p.feed(html)
    for b in set(p.bad): errors.append(f"{sp}: {b}")
    if p.h1!=1: errors.append(f"{sp}: {p.h1} h1")
    if sp!="/404.html":
        titles.setdefault(p.title,[]).append(sp)
        if not p.desc or not (70<=len(p.desc)<=170): warnings.append(f"{sp}: description length {len(p.desc or '')}")
        else: descs.setdefault(p.desc,[]).append(sp)
        if p.canon!="https://cebudavao.com"+sp: errors.append(f"{sp}: canonical {p.canon}")
    if len(p.title)>75: warnings.append(f"{sp}: title {len(p.title)} chars")
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: errors.append(f"{sp}: bad JSON-LD {e}")
    for l in p.links:
        u=urlparse(l)
        if u.scheme in ("mailto","tel") or (u.netloc and u.netloc!="cebudavao.com"): continue
        if l.startswith("#"):
            if l[1:] and l[1:] not in p.ids and l!="#top": errors.append(f"{sp}: missing anchor {l}")
            continue
        path=u.path or "/"
        if not exists(path):
            if path in redir: warnings.append(f"{sp}: links to redirected {path}")
            else: errors.append(f"{sp}: broken link {path}")
    for s in p.imgs:
        if s and s.startswith("/") and not os.path.isfile(os.path.join(PUB,s.lstrip("/"))): errors.append(f"{sp}: missing image {s}")
for t,v in titles.items():
    if len(v)>1: errors.append(f"duplicate title '{t}': {v[:3]}")
for t,v in descs.items():
    if len(v)>1 and not all("/page/" in x for x in v[1:]): warnings.append(f"duplicate description: {v[:3]}")
# legacy coverage
for l in open(os.path.join(ROOT,"data","legacy-urls.txt")):
    l=l.strip()
    if l and not exists(l) and l not in redir:
        seg=l.strip("/").split("/")[0]
        warnings.append(f"legacy {l} not live/redirected (falls to router rules)")
# php lint
for f in ("index.php","api/news.php","api/contact.php","api/subscribe.php","api/lib.php","redirects.php","sections.php"):
    r=subprocess.run(["php","-l",os.path.join(PUB,f)],capture_output=True,text=True)
    if r.returncode: errors.append(r.stdout+r.stderr)
print(f"{len(pages)} pages checked, {len(redir)} redirects")
for w in warnings[:60]: print("WARN", w)
if len(warnings)>60: print(f"... {len(warnings)-60} more warnings")
for e in errors[:80]: print("ERR ", e)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
