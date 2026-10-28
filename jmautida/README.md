# jmautida.com

Portfolio and free toolbox of John Raymond Autida. Static HTML + a small PHP API, hosted on
Hostinger web hosting (account u401386392, Cloud Enterprise), document root `public_html`.

| Path | What it is |
| --- | --- |
| `build.py` | Generates every HTML page, `.htaccess`, sitemap, manifest and the tool catalog into `public/` |
| `public/assets/css/site.css` | Design system, effects and tool styles |
| `public/assets/js/site.js`, `fx.js` | Theme, ⌘K palette, launcher, reveal/tilt effects; hero canvas + terminal |
| `public/assets/js/tools/*.js` | One script per tool (`common.js` holds shared helpers) |
| `public/assets/js/time-math.js` | Shift/timesheet math, unit-tested in `tests/time-math.test.js` |
| `public/api/check.php`, `lib.php` | Meta tags + favicon checkers (SSRF-guarded fetcher, rate limited) |
| `public/api/contact.php`, `mailer.php` | Contact form → SMTP (smtp.hostinger.com:465) to autida@jmautida.com |
| `public/api/config.php` | **Server-only secrets, git-ignored.** Copy `config.sample.php` and fill in the mailbox password |
| `backup/live-2026-10-28/` | The previous live site, for rollback |

## Work on it

```sh
python3 jmautida/build.py                       # regenerate pages after editing build.py
node jmautida/tests/time-math.test.js
php -S 127.0.0.1:8080 -t jmautida/public jmautida/tests/router.php   # local preview with clean URLs
```

## Deploy

Get File Browser credentials with the Hostinger API operation `hosting_files_generate-upload-url`
(username `u401386392`, domain `jmautida.com`), then:

```sh
BASE=https://srvNNNN-files.hstgr.io/rest/<id>/api AK=<auth_key> RK=<rest_auth_key> ./jmautida/deploy.sh
```

Upload `.htaccess` last when deploying a large change. Bump `VERSION` in `build.py` to bust CSS/JS caches.
