#!/usr/bin/env python3
"""Guest-contribution test (no account: name + email).

    python3 tools/guest_test.py BASE_URL GUEST_EMAIL MAIL_SOURCE

MAIL_SOURCE is a local mail-log file (dev config 'mail_log'), or the word "manual":
the script then pauses and asks you to paste the confirmation link from the inbox.
"""
import re
import sys
import time
import urllib.parse

sys.path.insert(0, __import__('os').path.dirname(__file__))
sys.argv, args = sys.argv[:2], sys.argv[1:]
import smoke_test as t  # noqa: E402  (reuses its HTTP client)

BASE, EMAIL, MAIL = args[0].rstrip('/'), args[1], args[2]
t.BASE = BASE
fails = []


def check(name, cond, info=''):
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  ' + str(info)[:300]))
    if not cond:
        fails.append(name)


def form_fields(html):
    return {k: re.search(r'name="%s" value="([^"]*)"' % k, html).group(1) for k in ('_ts', '_tss')}


def latest_link(before_size):
    if MAIL == 'manual':
        return input('Paste the confirmation link from the email: ').strip()
    for _ in range(20):
        data = open(MAIL).read()[before_size:]
        m = re.findall(r'https?://\S+/confirm/\?id=\d+&t=[0-9a-f]+', data)
        if m:
            return m[-1]
        time.sleep(0.5)
    return ''


def main():
    g = t.Client()
    path = '/blog/how-to-soundproof-an-apartment/'
    st, h, html = g.get(path)
    check('article 200', st == 200)
    check('anonymous view sets no session cookie', 'm1s_sid' not in (h.get('Set-Cookie') or ''), h.get('Set-Cookie'))
    check('guest comment form shown', 'name="guest_email"' in html and 'name="_csrf"' not in html)
    check('product box with affiliate tag', 'tag=josephrayditt-20' in html and 'rel="sponsored nofollow noopener"' in html)
    check('amazon disclosure', 'Amazon Associate' in html)
    aid = re.search(r'name="target_id" value="(\d+)"', html).group(1)
    ff = form_fields(html)
    time.sleep(2.2)

    # cross-site POST is refused
    st, _, _ = g.post('/comment/', {'target_type': 'article', 'target_id': aid, 'body': 'x' * 10, **ff,
                                     'guest_name': 'Evil', 'guest_email': EMAIL}, headers={'Origin': 'https://evil.example'})
    check('cross-site guest POST blocked', st == 403, st)
    # bad email domain
    st, h, _ = g.post('/comment/', {'target_type': 'article', 'target_id': aid, 'body': 'Hello there', **ff, 'website': '',
                                     'guest_name': 'Sam', 'guest_email': 'sam@no-such-domain-m1s-test.invalid'}, headers={'Origin': BASE})
    _, _, page = g.get(path)
    check('invalid email domain rejected', 'does not accept mail' in page or 'valid email' in page, page[:200])

    import os
    size = os.path.getsize(MAIL) if MAIL != 'manual' else 0
    body = 'Guest test comment %d: rubber door sweeps made a big difference for me.' % int(time.time())
    _, _, html = g.get(path)
    ff = form_fields(html)
    time.sleep(2.2)
    st, h, _ = g.post('/comment/', {'target_type': 'article', 'target_id': aid, 'body': body, **ff, 'website': '',
                                     'guest_name': 'Taylor Test', 'guest_email': EMAIL}, headers={'Origin': BASE})
    loc = h.get('Location', '')
    check('first guest comment held for confirmation', st == 302 and '/confirm/sent/' in loc, (st, loc))
    _, _, page = t.Client().get(path)
    check('pending comment not public yet', body not in page)
    link = latest_link(size)
    check('confirmation email sent', bool(link), link)
    if link:
        lp = urllib.parse.urlsplit(link)
        st, h, _ = g.get(lp.path + '?' + lp.query)
        check('confirm link publishes', st == 302 and '#c' in h.get('Location', ''), (st, h.get('Location')))
        _, _, page = t.Client().get(path)
        check('confirmed comment is public', body in page and 'Taylor Test' in page and '>guest<' in page)
        check('guest email never shown', EMAIL not in page)

        # second contribution from the same (now trusted) browser publishes instantly
        _, _, html = g.get('/submit/?c=renting')
        check('guest submit form prefilled', 'value="Taylor Test"' in html)
        ff = form_fields(html)
        time.sleep(2.2)
        title = 'Guest test post %d: best renter-friendly soundproofing?' % int(time.time())
        st, h, _ = g.post('/submit/', {'community': 'renting', 'title': title, 'body': 'Looking for ideas that will not cost my deposit.',
                                        **ff, 'website': '', 'guest_name': 'Taylor Test', 'guest_email': EMAIL}, headers={'Origin': BASE})
        loc = h.get('Location', '')
        check('trusted guest post publishes instantly', st == 302 and '/forum/renting/' in loc, (st, loc))
        if '/forum/renting/' in loc:
            _, _, page = t.Client().get(urllib.parse.urlsplit(loc).path)
            check('guest thread public with guest badge', title in page and '>guest<' in page)
        st, _, _ = g.post('/vote/', {'type': 'article', 'id': aid, 'value': '1'}, headers={'Accept': 'application/json', 'Origin': BASE})
        check('guests cannot vote', st in (401, 419), st)
    print('\n%d failure(s)' % len(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
