#!/usr/bin/env python3
"""One-shot transformation of the generated San Antonio build:
- wire every CONNECT FORM placeholder to the existing /contact.php handler (field names it expects, honeypot, JS submit)
- carry over the old logo (mark.svg) as favicon + header mark, the GA4 tag, and the GSC verification file
- noindex the 404 and thank-you pages
- rename root index.html -> home.html (Hostinger H5G platform requirement, see db.php)
Idempotent: safe to re-run.
"""
import os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'_old-site', 'tools', '.git'}

GA = ('<!-- Google tag (gtag.js) -->\n'
      '<script async src="https://www.googletagmanager.com/gtag/js?id=G-8DDXM4V05D"></script>\n'
      '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
      "gtag('js',new Date());gtag('config','G-8DDXM4V05D');</script>\n")
ICON = '<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">\n'
FORM_CSS = '.form-status{margin-top:10px;font-size:14px;min-height:1.2em}.form-status.err{color:#b42318}\n'
FORM_JS = ('<script>(function(){var f=document.getElementById("claim-form");if(!f)return;'
           'var s=document.getElementById("form-status");'
           'f.addEventListener("submit",function(e){e.preventDefault();'
           'if(f.website&&f.website.value){return;}'
           's.className="form-status";s.textContent="Sending…";'
           'fetch(f.getAttribute("action"),{method:"POST",body:new FormData(f),headers:{"Accept":"application/json"}})'
           '.then(function(r){return r.ok?r.json():Promise.reject(r.status)})'
           '.then(function(j){if(j&&j.ok){window.location.href="/contact/thanks/";}else{throw new Error("bad");}})'
           '.catch(function(){s.className="form-status err";'
           's.innerHTML=\'The form could not send. Call or text <a href="tel:+18325035866">(832) 503-5866</a> and we will take it from there.\';});});})();</script>\n')
HONEYPOT = ('<div style="position:absolute;left:-9999px" aria-hidden="true"><label for="w">Leave blank</label>'
            '<input id="w" name="website" type="text" tabindex="-1" autocomplete="off"></div>\n')
STATUS = '<div class="form-status" id="form-status" role="status" aria-live="polite"></div>\n'
OLD_LOGO_RE = re.compile(r'<a class="logo" href="/"><svg[^>]*>.*?</svg>', re.S)
NEW_LOGO = '<a class="logo" href="/"><img class="mark" src="/assets/mark.svg" alt="" width="34" height="34">'

def pages():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith('.html'):
                yield os.path.join(dp, fn)

def fix_form(html):
    html = html.replace('<!-- CONNECT FORM: replace action with your existing form endpoint (the callback form on the old site) -->\n', '')
    html = html.replace('<form class="lead" action="/contact/thanks/" method="post" name="claim-review">',
                        '<form class="lead" id="claim-form" action="/contact.php" method="post" name="claim-review">')
    html = html.replace('<input id="c" name="city" placeholder="San Antonio 78258">',
                        '<input id="c" name="address" placeholder="San Antonio 78258" autocomplete="postal-code">')
    html = html.replace('<select id="t" name="claim_type">', '<select id="t" name="damage">')
    if 'id="claim-form"' in html and 'name="website"' not in html:
        html = html.replace('<button class="btn" type="submit">Get My Free Claim Review</button>\n',
                            HONEYPOT + '<button class="btn" type="submit">Get My Free Claim Review</button>\n' + STATUS)
    if 'id="claim-form"' in html and 'getElementById("claim-form")' not in html:
        html = html.replace('</body></html>', FORM_JS + '</body></html>')
    if '.form-status{' not in html:
        html = html.replace('</style>', FORM_CSS + '</style>', 1)
    return html

def fix_head(html, rel):
    if 'rel="icon"' not in html:
        html = html.replace('<meta name="theme-color" content="#132436">\n',
                            '<meta name="theme-color" content="#132436">\n' + ICON, 1)
    if 'G-8DDXM4V05D' not in html:
        html = html.replace('</head>', GA + '</head>', 1)
    html = OLD_LOGO_RE.sub(NEW_LOGO, html, count=1)
    # 404 and thank-you pages must not be indexed; the 404's placeholder canonical goes away.
    if rel in ('404.html', 'contact/thanks/index.html'):
        html = html.replace('<meta name="robots" content="index,follow,max-image-preview:large">',
                            '<meta name="robots" content="noindex,follow">')
        if rel == '404.html':
            html = re.sub(r'<link rel="canonical" href="[^"]*">\n', '', html)
            html = html.replace('<meta property="og:url" content="https://conversepublicadjuster.com/404-tmp/">', '')
    return html

def main():
    n = 0
    for p in sorted(pages()):
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        html = open(p, encoding='utf-8').read()
        new = fix_head(fix_form(html), rel)
        if new != html:
            open(p, 'w', encoding='utf-8').write(new); n += 1
    # Homepage file name: the Hostinger H5G platform serves a root index.html for every unknown path,
    # so the homepage is shipped as home.html and wp-content/db.php maps "/" to it.
    if os.path.exists(os.path.join(ROOT, 'index.html')):
        os.replace(os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'home.html')); n += 1
    print(f'transform: {n} files changed')

if __name__ == '__main__':
    main()
