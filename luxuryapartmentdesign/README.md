# luxuryapartmentdesign.com — custom PHP site

Replaces the WordPress/Elementor site. Plain PHP 8 (no framework, no database,
no Composer), one stylesheet, vanilla JavaScript. Hosted on Hostinger
(Cloud Enterprise, account `u401386392`), document root
`/home/u401386392/domains/luxuryapartmentdesign.com/public_html`.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller / router (`.htaccess` sends every non-file request here) |
| `inc/config.php` | Site constants, categories, tools, navigation, Google tag |
| `inc/functions.php` | Content loading, card/FAQ helpers, schema builders |
| `inc/layout.php` | `<head>`, header, footer |
| `inc/redirects.php` | 301 map for retired WordPress URLs |
| `pages/` | One view per page type (home, article, category, tool, blog, contact…) |
| `content/articles/<slug>.json` + `.html` | Article metadata + body (see `CONTENT-SPEC.md`) |
| `content/tools/<slug>.json` + `.html` | Tool page copy |
| `templates/tools/<slug>.php` + `assets/js/tools/<slug>.js` | The interactive tools |
| `assets/` | CSS, JS, images (`assets/img/articles/<stem>.webp` and `-600.webp`) |
| `deploy.sh`, `deploy/migrate.php` | Upload script and the one-time WordPress → PHP switchover |
| `validate.py` | Crawls a running copy and checks every page |

## Adding an article

Write `content/articles/<slug>.json` and `<slug>.html` following
`CONTENT-SPEC.md`, add a hero image to `assets/img/articles/` (1200 px wide plus a
600 px `-600` version), and upload. The article appears automatically on its
category page, `/blogs/`, the sitemap, RSS, and search.

## Local preview and checks

```sh
php -S 127.0.0.1:8765 router.php   # router.php: serve real files, else require index.php
python3 validate.py
```

## Deploying

`./deploy.sh` uploads every site file through the Hostinger File Browser API
(credentials from `hosting_files_generate-upload-url`, see the script header).

## WordPress backup

On 2026-10-28 every WordPress file was moved into
`public_html/wp-backup-2026-10-28/` (deny-all `.htaccess`; the original is kept
as `.htaccess.wordpress`), together with a SQL dump in `database/`. The WordPress
database was left in place. Old `/wp-content/uploads/…` image URLs are still
served from the backup by a rewrite rule. Restore steps are in the backup's
`README.txt`.

## Forms and email

Contact messages and newsletter sign-ups are appended to CSV files in
`/home/u401386392/domains/luxuryapartmentdesign.com/lad-data/` (outside the web
root) and emailed to `CONTACT_EMAIL` (info@luxuryapartmentdesign.com) through
Hostinger SMTP (`inc/mailer.php`, ssl://smtp.hostinger.com:465). Contact emails
carry the visitor's address as Reply-To.

The SMTP login lives only on the server, in `lad-data/mail.php` (chmod 600):

```php
<?php return ['host' => 'smtp.hostinger.com', 'port' => 465,
              'user' => 'info@luxuryapartmentdesign.com', 'pass' => '…'];
```

If the mailbox password changes, edit that file in hPanel's File Manager
(one level above public_html). Without it the form falls back to PHP `mail()`.
