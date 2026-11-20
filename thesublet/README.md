# thesublet.com

Custom PHP 8 + MySQL marketplace for furnished sublets and 1–12 month rentals. No framework, no WordPress.

## Layout
| Path | What |
| --- | --- |
| `index.php` | Front controller + route table (nginx sends unknown paths here; `.htaccess` is ignored) |
| `robots.txt` | Real file: nginx doesn't route it to PHP |
| `app/bootstrap.php`, `app/lib/` | DB (MySQL/SQLite, auto-migrating schema, DB sessions), helpers (CSRF, honeypot, rate limits), SMTP mailer, Stripe, GD→WebP images, auth, layout, schema.org |
| `app/pages/` | One file per route (public, `account/`, `admin/`) |
| `app/views/` | Shared templates + `emails/` |
| `app/content/cities/*.php` | 74 city guides (50 metros + 24 college towns) |
| `app/content/blog/*.php` | 20 blog posts with FAQs + Amazon product queries |
| `app/content/tools.php` | Copy for the 6 interactive tools (`assets/js/tools.js`) |
| `app/legacy.php` | 301/410 map for the old WordPress URLs |
| `app/config.sample.php` | Copy to `app/config.php` **on the server only** (git-ignored) |
| `dev/` | Local test harness (not deployed) |

Every PHP file starts with `defined('APP') || exit;`. Photos are stored as WebP BLOBs in MySQL and served from `/photo/{id}.webp`.

## Local testing
```
cp app/config.sample.php app/config.php   # set env=dev, db.driver=sqlite, db.path=…/dev/data/dev.sqlite
php -S 127.0.0.1:8099 index.php
node dev/e2e.js && node dev/e2e-owner.js   # Playwright, desktop + 390px mobile
```
In dev with no SMTP password, emails are written to `dev/mail.log`.

## Deploy (Hostinger Agency, website UID `YmzW9m4Jg`)
1. `zip -r site.zip . -x 'dev/*' '.gitignore' 'app/config.php' '*.md'`
2. `agency-hosting_files_generate-upload-url` → TUS-upload `site.zip` and a one-time token-protected extractor PHP script to `public_html/`, hit the extractor (it unzips, then deletes the zip and itself).
3. `app/config.php` is uploaded separately and never committed.
4. Flush CDN in hPanel → Performance → CDN after big changes.

Expiry/reminders: hourly cron `curl …/cron/run/?key=<cron_key>`, plus an opportunistic run at most once an hour on page views.
