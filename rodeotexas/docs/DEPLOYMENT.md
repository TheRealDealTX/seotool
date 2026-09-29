# Deployment & operations (Hostinger)

Verified against the account on 2026-09-29: plan **Cloud Enterprise**, user `u401386392`,
website `rodeotexas.org` (addon domain), document root
`/home/u401386392/domains/rodeotexas.org/public_html`, PHP 8.2 (web) with `pdo_mysql`, `curl`,
`intl`, `zip`, `gd`, `mbstring`; `exec`/`shell_exec` are disabled (not needed). Server clock: UTC.

## 1. Directory structure

```
/home/u401386392/domains/rodeotexas.org/
├── app/                ← code, config.php (secrets), storage/ — NOT web-accessible
├── backups/            ← installer's WordPress backup (wp-YYYYMMDD/)
└── public_html/        ← web root (the contents of this repo's public_html/)
    └── wp-content/uploads/   ← kept from WordPress: article images still live here
```

## 2. Database

1. hPanel → **Databases → Management** → create a database and user (or API
   `hosting_databases_create`). Name used in production: `u401386392_rodeo`.
2. Put the name, user and password in `app/config.php` (`db.host` = `127.0.0.1`, port 3306).
3. Create tables: `php app/bin/migrate.php` (or installer step `migrate`). Re-running is safe.
4. Migrate old content: `php app/bin/seed-content.php` (21 articles, 184 Texas legacy events,
   199 redirects). Idempotent.
5. Create the admin: `php app/bin/create-admin.php --email=… --name=…` (prompts for password).
   The same command resets a forgotten password.

## 3. Configuration (`app/config.php`)

Copy `app/config.example.php`. Required: `base_url`, `db.*`, `admin_email` (receives
submissions and failure alerts; never shown on the site), `mail_from`, and `app_secret`
(`php -r "echo bin2hex(random_bytes(32));"`). Permissions: `chmod 600 app/config.php`.

## 4. HTTPS

rodeotexas.org already serves a valid certificate (Hostinger's free SSL). `public_html/.htaccess`
301-redirects `http://` and `www.` to `https://rodeotexas.org`. HSTS is sent by PHP once HTTPS is
active. If the certificate ever lapses: hPanel → **Security → SSL** → install/renew (free).

## 5. PHP settings (hPanel → Advanced → PHP Configuration)

| Setting | Value | Why |
| --- | --- | --- |
| PHP version | 8.2 or newer (8.3 fine) | code targets PHP ≥ 8.0 |
| Extensions | pdo_mysql, curl, intl, mbstring, zip, gd | already enabled |
| `display_errors` | Off | errors go to `app/storage/logs/` |
| `max_execution_time` | ≥ 300 | manual “Run import” from the admin |
| `session.cookie_secure/httponly/samesite` | set by the app itself | no change needed |
| `allow_url_fopen` | may stay On | the app uses cURL |

## 6. Cron — weekly import, Monday 7:00 AM Central

Hostinger cron runs in **server time (UTC)** and Chicago shifts between UTC−6 (CST) and UTC−5
(CDT). Schedule both candidate hours; the script checks the Chicago clock and runs once:

```
0 12,13 * * 1   /usr/bin/php /home/u401386392/domains/rodeotexas.org/app/bin/import.php --cron --quiet
```

* 12:00 UTC = 7:00 CDT (Mar–Nov) · 13:00 UTC = 7:00 CST (Nov–Mar). The other trigger exits
  immediately ("not the scheduled hour" in `app/storage/logs/cron.log`).
* A second guard skips the run if a weekly cron import already ran in the last 6 days.
* To change the day/hour edit `import.weekly_weekday` / `import.weekly_hour_local` in config and
  the cron hours accordingly.

hPanel → **Advanced → Cron Jobs** → “Custom” → paste the schedule and command (or create it with
the Hostinger API operation `hosting_cron-jobs_create`). After the first Monday, check
Admin → Import history for a run started by `cron`.

### Optional daily 7-day check

Re-checks sources flagged “daily check” for events in the next 7 days (catches last-minute
cancellations/time changes). Enable with both:

1. `app/config.php`: `'daily_enabled' => true` (`daily_hour_local` default 6 → 6 AM Central).
2. Cron: `0 11,12 * * *   /usr/bin/php /home/u401386392/domains/rodeotexas.org/app/bin/import.php --daily --quiet`
3. Admin → Sources → tick “Also include in the optional daily 7-day check” for each source.

### Optional link check

`30 13 * * 2   /usr/bin/php /home/u401386392/domains/rodeotexas.org/app/bin/check-links.php`

## 7. Deploying updates

* **With SSH/SFTP (recommended):** upload changed files to the same paths, then run
  `php app/bin/migrate.php`. Never overwrite `app/config.php` or `app/storage/`.
* **Without SSH:** `tools/build-package.sh OUTDIR app/config.php admin@email '<bcrypt hash>'` builds
  `rodeotexas-package.zip` + a one-time `_install_<token>.php`; upload both to `public_html/`
  (File Manager or API) and call the steps `extract`, `migrate`, `cleanup` with the token.

## 8. Backups

* **Hostinger automatic backups:** Cloud plans keep daily backups (hPanel → **Files → Backups**),
  covering files and databases. Use “Generate new backup” before big changes.
* **Database export:** hPanel → Databases → phpMyAdmin → Export (SQL), or
  `mysqldump -h 127.0.0.1 -u USER -p u401386392_rodeo | gzip > rodeo-$(date +%F).sql.gz` over SSH.
* **What must be backed up:** the database, `app/config.php`, `app/storage/imports/` (uploaded CSVs),
  `public_html/wp-content/uploads/` (article images). Everything else is in this repository.
* **The pre-launch WordPress backup** is in `domains/rodeotexas.org/backups/wp-20260929/`
  (`wordpress-database.sql.gz` + all WordPress files). Keep it at least a few months.

## 9. Restore

* **New site, from backup:** restore the database (phpMyAdmin → Import the `.sql.gz`), upload the
  repository files, restore `app/config.php`, run `php app/bin/migrate.php`.
* **Roll back to WordPress** (emergency): in File Manager move the new files out of `public_html`
  (keep `wp-content/uploads`), move everything from `backups/wp-20260929/public_html/` back into
  `public_html/`. The WordPress database was never modified, so no DB restore is needed (the dump is
  there in case). 

## 10. Monitoring

* Admin dashboard shows the last import, failing sources and the review queue.
* Failure alerts are e-mailed to `admin_email`. Mail is sent with PHP `mail()` from `mail_from`;
  for best deliverability create that mailbox (or an SPF-covered alias) in hPanel → Emails.
* Logs: `app/storage/logs/` (`import`, `cron`, `mail`, `php-error`), and Admin → Import history.
