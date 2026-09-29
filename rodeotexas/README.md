# RodeoTexas.org — Texas rodeo event directory

A fast, accessible directory of rodeos held in Texas, built with plain **PHP 8 + MySQL/MariaDB**,
vanilla JavaScript and CSS. It runs on Hostinger shared/cloud PHP hosting: no Node.js, no
long-running process, no page builder. The weekly event import is a PHP command-line script run
by Hostinger's cron.

| Document | What it covers |
| --- | --- |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Database, HTTPS, PHP settings, cron (Monday 7 AM Central), backups & restore |
| [docs/ADMIN-GUIDE.md](docs/ADMIN-GUIDE.md) | Day-to-day administration |
| [docs/SOURCES.md](docs/SOURCES.md) | Event sources, adapters, import rules, adding a source, CSV fallback |
| [docs/AUDIT.md](docs/AUDIT.md) | Audit of the old WordPress site and the reference site, URL migration |
| [docs/VERIFICATION.md](docs/VERIFICATION.md) | Test results (automated + manual) |
| [docs/SERVICES.md](docs/SERVICES.md) | External services, costs, unresolved dependencies |

## Layout (mirrors Hostinger: `domains/rodeotexas.org/…`)

```
app/                         ← OUTSIDE the web root (never downloadable)
  config.example.php         example configuration (copy to config.php)
  bootstrap.php              loaded by every entry point
  lib/                       core classes (Db, Auth, Importer, EventRepo, Seo, Ics, …)
  adapters/                  one file per source type: TribeRestAdapter, IcalAdapter, JsonLdAdapter, CsvAdapter
  admin/                     admin templates (served through public_html/admin/index.php)
  bin/                       CLI: import.php, migrate.php, seed-content.php, create-admin.php, check-links.php
  migrations/                SQL schema + seed data
  data/                      one-time migration data from the old WordPress site
  storage/                   logs, lock file, sessions, uploaded CSVs (runtime)
public_html/                 ← web root
  index.php                  public front controller (routes every URL)
  .htaccess                  HTTPS/canonical host, security rules, front controller
  includes/head.php          shared <head>: meta, CSS, SITE-WIDE TRACKING SCRIPTS
  includes/header.php        logo + main navigation
  includes/footer.php        footer
  includes/scripts.php       shared end-of-body JavaScript
  pages/                     page templates (home, directory, event, article, forms, sitemap …)
  admin/index.php            admin front controller (/admin/)
  assets/                    css, js, fonts, images
deploy/install.php           one-time web installer used when there is no SSH
tools/                       build-package.sh, migration data builder, image generator, dev router
tests/                       run.php (integration tests), http.php (end-to-end), fixtures
```

## Where to make site-wide changes

| Change | File |
| --- | --- |
| Google Analytics, Meta Pixel, Search Console / Bing verification, any `<head>` script | `public_html/includes/head.php` — the marked **SITE-WIDE HEAD CODE** block. Appears on every public page (including event and article pages and the 404), never in the admin. |
| Scripts that must load at the end of `<body>` (chat widgets etc.) | `public_html/includes/scripts.php` |
| Menu items, logo | `public_html/includes/header.php` |
| Footer links / text | `public_html/includes/footer.php` |
| Default title / description / social image | `public_html/includes/head.php` (defaults at the top) |
| Colours, fonts, spacing | `public_html/assets/css/site.css` (`:root` variables) |
| Per-page title, description, canonical, social image, structured data | the `$page = [...]` array at the top of each file in `public_html/pages/` (set **before** `require_once …/includes/head.php`) |

Every public page loads the includes with `require_once RT_PUBLIC . '/includes/…'`
(`RT_PUBLIC` is the absolute web-root path), so they work at any URL depth.

## Local development

```sh
cp app/config.example.php /tmp/rt-config.php     # point db at a local MySQL/MariaDB
export RT_CONFIG=/tmp/rt-config.php
php app/bin/migrate.php && php app/bin/seed-content.php && php app/bin/import.php
php app/bin/create-admin.php --email=you@example.com --name=You
php -S localhost:8080 -t public_html tools/dev-router.php
RT_CONFIG=/path/to/test-config.php php tests/run.php          # needs an empty *test* database
php tests/http.php http://localhost:8080 you@example.com 'password'
```
