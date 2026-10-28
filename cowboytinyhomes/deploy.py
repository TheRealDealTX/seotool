#!/usr/bin/env python3
"""Deploy public_html/ to cowboytinyhomes.com through Hostinger's File Browser API.

Credentials come from the Hostinger API call `hosting_files_generate-upload-url`
(username u401386392, domain cowboytinyhomes.com). They expire after a few
hours. Export them before running:

    export FB_URL='https://srvNNNN-files.hstgr.io/rest/<id>/api/tus/public_html'   # "url"
    export FB_AUTH='…'   # "auth_key"
    export FB_REST='…'   # "rest_auth_key"

    python3 deploy.py upload          # upload/overwrite every site file
    python3 deploy.py backup-wp       # one-time: move WordPress into the backup folder
    python3 deploy.py launch          # one-time: upload site, back up WP, then swap index.php/.htaccess

`launch` uploads everything except index.php and .htaccess first (WordPress
keeps serving meanwhile), moves the WordPress files into
public_html/wordpress-backup-2026-10-28/ (locked with "Require all denied"),
then uploads index.php and .htaccess last, so the switch takes seconds.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent / 'public_html'
BACKUP = 'wordpress-backup-2026-10-28'
KEEP_IN_ROOT = {'.private', BACKUP}           # Hostinger's own folder + the backup itself
SKIP = {'router-dev.php'}                     # local preview helper
SKIP_DIRS = {'inc/data'}                      # leads written by the live site
LAST = ['index.php', '.htaccess']             # swapped in at the very end

url = os.environ.get('FB_URL', '').rstrip('/')
auth = os.environ.get('FB_AUTH', '')
rest = os.environ.get('FB_REST', '')
if not (url and auth and rest):
    sys.exit('Set FB_URL, FB_AUTH and FB_REST (see the header of this file).')
api = url.split('/tus/')[0]                   # …/api
HDR = {'X-Auth': auth, 'X-Auth-Rest': rest}


def req(method, full_url, data=None, headers=None):
    r = urllib.request.Request(full_url, data=data, method=method, headers={**HDR, **(headers or {})})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def q(path):
    return urllib.parse.quote(path)


def upload(rel):
    data = (ROOT / rel).read_bytes()
    target = f'{url}/{q(rel)}?override=true'
    c, _ = req('POST', target, headers={'Tus-Resumable': '1.0.0', 'Upload-Length': str(len(data)), 'Upload-Offset': '0'})
    p, _ = req('PATCH', target, data=data, headers={'Tus-Resumable': '1.0.0', 'Upload-Offset': '0',
                                                    'Content-Type': 'application/offset+octet-stream'})
    ok = c == 201 and p == 204
    print(('ok   ' if ok else f'FAIL {c}/{p} ') + rel)
    return ok


def site_files():
    out = []
    for f in sorted(ROOT.rglob('*')):
        rel = f.relative_to(ROOT).as_posix()
        if f.is_dir() or rel in SKIP or any(rel.startswith(d + '/') for d in SKIP_DIRS) or '__pycache__' in rel:
            continue
        out.append(rel)
    return out


def upload_all(exclude=()):
    files = [f for f in site_files() if f not in exclude]
    bad = [f for f in files if not upload(f)]
    print(f'uploaded {len(files) - len(bad)}/{len(files)}')
    return not bad


def listing(path):
    s, body = req('GET', f'{api}/resources/{q(path)}/')
    if s != 200:
        sys.exit(f'cannot list {path}: HTTP {s}')
    return json.loads(body)['items']


def backup_wp():
    names = {i['name'] for i in listing('public_html')}
    if BACKUP not in names:
        s, _ = req('POST', f'{api}/resources/public_html/{BACKUP}/')
        print(f'mkdir {BACKUP}: HTTP {s}')
    # Lock the backup folder before anything moves into it.
    tmp = ROOT.parent / '.backup-htaccess'
    tmp.write_text('Require all denied\n')
    data = tmp.read_bytes()
    target = f'{url}/{BACKUP}/.htaccess?override=true'
    req('POST', target, headers={'Tus-Resumable': '1.0.0', 'Upload-Length': str(len(data)), 'Upload-Offset': '0'})
    req('PATCH', target, data=data, headers={'Tus-Resumable': '1.0.0', 'Upload-Offset': '0', 'Content-Type': 'application/offset+octet-stream'})
    tmp.unlink()

    new_site = {p.split('/')[0] for p in site_files()} - set(LAST)
    moved = 0
    for item in listing('public_html'):
        n = item['name']
        if n in KEEP_IN_ROOT or n in new_site:
            continue
        dest = q(f'/public_html/{BACKUP}/{n}')
        s, body = req('PATCH', f'{api}/resources/public_html/{q(n)}?action=rename&destination={dest}&override=false&rename=false')
        print(('moved ' if s == 200 else f'FAIL {s} {body[:120]!r} ') + n)
        moved += s == 200
    print(f'moved {moved} WordPress items into {BACKUP}/')


cmd = sys.argv[1] if len(sys.argv) > 1 else ''
if cmd == 'upload':
    sys.exit(0 if upload_all() else 1)
elif cmd == 'backup-wp':
    backup_wp()
elif cmd == 'launch':
    if not upload_all(exclude=LAST):
        sys.exit('aborting: some files failed to upload; WordPress is untouched')
    backup_wp()
    ok = all(upload(f) for f in LAST)
    sys.exit(0 if ok else 1)
else:
    sys.exit(__doc__)
