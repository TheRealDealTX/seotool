#!/usr/bin/env python3
"""End-to-end smoke test of the community features.

    python3 tools/smoke_test.py http://127.0.0.1:8080 [admin_user admin_pass]

Creates two throwaway accounts, posts, comments, replies, votes, reports, and
(if admin credentials are given) moderates and cleans up. Stdlib only.
"""
import http.cookiejar
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip('/')
ADMIN = sys.argv[2:4] if len(sys.argv) >= 4 else None
failures = []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class Client:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar), NoRedirect)

    def req(self, method, path, data=None, headers=None):
        url = path if path.startswith('http') else BASE + path
        body = urllib.parse.urlencode(data).encode() if data is not None else None
        r = urllib.request.Request(url, data=body, method=method, headers={'User-Agent': 'm1s-smoke', **(headers or {})})
        try:
            resp = self.op.open(r, timeout=30)
            return resp.status, resp.headers, resp.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read().decode('utf-8', 'replace')

    def get(self, path):
        return self.req('GET', path)

    def post(self, path, data, **kw):
        return self.req('POST', path, data, **kw)

    def csrf(self, path):
        _, _, html = self.get(path)
        m = re.search(r'name="_csrf" value="([0-9a-f]+)"', html)
        return m.group(1) if m else '', html


def check(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(info)[:300]))
    if not cond:
        failures.append(name)


def register(c, name):
    tok, html = c.csrf('/register/')
    ts = re.search(r'name="_ts" value="(\d+)"', html).group(1)
    tss = re.search(r'name="_tss" value="([0-9a-f]+)"', html).group(1)
    time.sleep(3.2)
    st, h, _ = c.post('/register/', {'_csrf': tok, '_ts': ts, '_tss': tss, 'website': '', 'username': name,
                                     'email': name + '@example.com', 'password': 'correct-horse-battery', 'agree': '1', 'next': ''})
    return st, h.get('Location', '')


def main():
    suffix = str(random.randint(10000, 99999))
    a, b = Client(), Client()

    # anonymous pages carry no per-user state and are cacheable
    st, h, html = Client().get('/')
    check('home 200', st == 200, st)
    check('home has no csrf token', '_csrf' not in html)
    check('home cache public', 'public' in (h.get('Cache-Control') or ''), h.get('Cache-Control'))
    check('home jsonld', 'application/ld+json' in html)

    st, loc = register(a, 'smokeA' + suffix)
    check('register A redirects', st == 302, (st, loc))
    st, _ = register(b, 'smokeB' + suffix)
    check('register B redirects', st == 302, st)

    # honeypot rejects bots
    bot = Client()
    tok, html = bot.csrf('/register/')
    st, h, _ = bot.post('/register/', {'_csrf': tok, 'website': 'spam', 'username': 'bot' + suffix,
                                       'email': 'bot' + suffix + '@example.com', 'password': 'x' * 12, 'agree': '1'})
    _, _, html = bot.get('/register/')
    check('honeypot blocks bot', 'automated' in html, html[:200])

    # CSRF required
    st, _, _ = a.post('/vote/', {'type': 'thread', 'id': '1', 'value': '1'})
    check('vote without csrf rejected', st in (302, 419), st)

    # create a thread
    tok, html = a.csrf('/submit/?c=renting')
    check('submit page loads', 'Create a post' in html)
    title = 'Smoke test: is renters insurance worth it for a studio ' + suffix
    st, h, _ = a.post('/submit/', {'_csrf': tok, 'community': 'renting', 'title': title,
                                   'body': 'Asking for a **friend**. Details:\n\n- small studio\n- Houston\n\n<script>alert(1)</script>'})
    loc = h.get('Location', '')
    check('thread created', st == 302 and '/forum/renting/' in loc, (st, loc))
    path = urllib.parse.urlsplit(loc).path
    tid = re.search(r'/(\d+)-', path).group(1)
    st, h, html = a.get(path)
    check('thread page 200', st == 200, st)
    check('markdown rendered', '<strong>friend</strong>' in html and '<li>small studio</li>' in html)
    check('script escaped', '<script>alert(1)</script>' not in html and '&lt;script&gt;' in html)
    check('DiscussionForumPosting schema', 'DiscussionForumPosting' in html)
    check('new thread without comments is noindex', 'noindex' in html)
    check('logged-in page private', 'no-store' in (h.get('Cache-Control') or ''), h.get('Cache-Control'))

    # wrong slug 301s to canonical
    st, h, _ = a.get('/forum/texas/%s-wrong/' % tid)
    check('wrong community/slug 301', st == 301 and h.get('Location', '').endswith(path), (st, h.get('Location')))

    # B comments, A replies
    tok, _ = b.csrf(path)
    st, h, _ = b.post('/comment/', {'_csrf': tok, 'target_type': 'thread', 'target_id': tid, 'body': 'Yes, absolutely worth it. Mine was $12/month.'})
    cid = re.search(r'#c(\d+)', h.get('Location', ''))
    check('comment created', st == 302 and cid, (st, h.get('Location')))
    cid = cid.group(1) if cid else '0'
    tok, _ = a.csrf(path)
    st, h, _ = a.post('/comment/', {'_csrf': tok, 'target_type': 'thread', 'target_id': tid, 'parent_id': cid, 'body': 'Thanks! That is cheaper than I thought.'})
    check('reply created', st == 302 and '#c' in h.get('Location', ''), (st, dict(h)))
    _, _, html = Client().get(path)
    check('thread now indexable (has comments)', 'name="robots" content="index' in html)
    check('nested reply rendered', html.count('class="comments"') >= 2)
    check('2 comments counted', '2 comments' in html)

    # JSON vote
    tok, _ = b.csrf(path)
    st, _, body = b.post('/vote/', {'_csrf': tok, 'type': 'thread', 'id': tid, 'value': '1'}, headers={'Accept': 'application/json'})
    check('vote json', st == 200 and json.loads(body).get('score') == 2, (st, body))
    st, _, body = b.post('/vote/', {'_csrf': tok, 'type': 'thread', 'id': tid, 'value': '-1'}, headers={'Accept': 'application/json'})
    check('vote flip', st == 200 and json.loads(body).get('score') == 0, body)
    st, _, body = b.post('/vote/', {'_csrf': tok, 'type': 'thread', 'id': tid, 'value': '0'}, headers={'Accept': 'application/json'})
    check('vote clear', st == 200 and json.loads(body).get('score') == 1, body)
    st, _, body = Client().post('/vote/', {'type': 'thread', 'id': tid, 'value': '1'}, headers={'Accept': 'application/json'})
    check('anon vote needs login', st in (401, 419), (st, body))

    # article comment + helpful vote
    st, _, html = b.get('/blog/apartment-security-tips/')
    aid = re.search(r'name="target_id" value="(\d+)"', html).group(1)
    tok = re.search(r'name="_csrf" value="([0-9a-f]+)"', html).group(1)
    st, h, _ = b.post('/comment/', {'_csrf': tok, 'target_type': 'article', 'target_id': aid, 'body': 'Great tips, the doorbell camera one helped.'})
    check('article comment', st == 302 and '/blog/apartment-security-tips/#c' in h.get('Location', ''), (st, h.get('Location')))
    st, _, body = b.post('/vote/', {'_csrf': tok, 'type': 'article', 'id': aid, 'value': '1'}, headers={'Accept': 'application/json'})
    check('article helpful vote', st == 200 and json.loads(body)['vote'] == 1, body)

    # report
    tok, _ = b.csrf('/report/?type=thread&id=' + tid)
    st, _, _ = b.post('/report/', {'_csrf': tok, 'type': 'thread', 'id': tid, 'reason': 'Spam or advertising'})
    check('report filed', st == 302, st)

    # B cannot edit A's thread
    st, _, _ = b.get(path + 'edit/')
    check('non-owner edit forbidden', st == 403, st)
    # A edits
    tok, _ = a.csrf(path + 'edit/')
    st, h, _ = a.post(path + 'edit/', {'_csrf': tok, 'title': title + ' (edited)', 'body': 'Updated body', 'link_url': ''})
    check('owner edit', st == 302, st)

    # profile + search
    st, _, html = Client().get('/u/smokeA%s/' % suffix)
    check('profile 200', st == 200 and title[:30] in html, st)
    st, _, html = Client().get('/search/?q=' + urllib.parse.quote('renters insurance worth'))
    check('search finds thread', suffix in html)

    # admin
    if ADMIN:
        adm = Client()
        tok, _ = adm.csrf('/login/')
        st, h, _ = adm.post('/login/', {'_csrf': tok, 'username': ADMIN[0], 'password': ADMIN[1], 'next': '/admin/'})
        check('admin login', st == 302 and h.get('Location') == '/admin/', (st, h.get('Location')))
        st, _, html = adm.get('/admin/reports/')
        check('report visible to admin', 'Spam or advertising' in html)
        rid = re.search(r'name="id" value="(\d+)"><input type="hidden" name="action" value="remove"', html)
        tok = re.search(r'name="_csrf" value="([0-9a-f]+)"', html).group(1)
        if rid:
            st, _, _ = adm.post('/admin/reports/', {'_csrf': tok, 'id': rid.group(1), 'action': 'remove'})
            check('admin removes reported thread', st == 302, st)
        st, _, _ = Client().get(urllib.parse.urlsplit(BASE + path).path)
        _, h, _ = Client().get(path)
        st2, _, _ = Client().get('/forum/renting/%s-x/' % tid)
        st3, _, html = Client().get('/forum/renting/' + tid + '-' + re.sub(r'[^a-z0-9]+', '-', (title + ' (edited)').lower()).strip('-')[:70].rsplit('-', 1)[0] + '/')
        check('removed thread hidden from public', 'This post was removed' in html or st3 in (301, 410), st3)
        # ban the throwaway users and remove their content
        _, _, html = adm.get('/admin/users/?q=smoke' + suffix[:0])
        for name in ('smokeA' + suffix, 'smokeB' + suffix):
            m = re.search(r'name="id" value="(\d+)"><input type="hidden" name="q" value="[^"]*">\s*<input type="hidden" name="action" value="ban">', html.split('>' + name + '<', 1)[1] if ('>' + name + '<') in html else '')
            if m:
                adm.post('/admin/users/', {'_csrf': tok, 'id': m.group(1), 'action': 'ban', 'purge': '1', 'q': ''})
        st, _, html = adm.get('/admin/users/?q=smoke')
        check('test users banned', html.count('Unban') >= 2, html.count('Unban'))

    print('\n%d failure(s)' % len(failures))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
