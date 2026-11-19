# vintiqueflea.com: custom PHP site

A hand-built PHP site that replaces the old WordPress/Elementor install on Hostinger
(Agency Growth plan). It runs on its own plain-PHP website, UID `yGuW887Xv` (php-fpm, PHP 8.4,
temporary address `comic-lightcoral-shark-66.hostingersite.com`). The old WordPress website is `67Tls7oNq`.
Its core files are locked and nginx ignores `.htaccess` there, so it can't host a custom app.

nginx on the PHP site sends every non-file request to `index.php`, which loads `app.php`. The `.htaccess`
is kept for Apache/LiteSpeed hosts. It has no database, no plugins and no framework:
one front controller, PHP templates, one stylesheet and vanilla JavaScript.

## Structure

| Path | Purpose |
| --- | --- |
| `index.php` → `app.php` | Front controller: legacy redirects, 410s, trailing slashes, routing |
| `.htaccess` | Sends everything that isn't a real file to `app.php`; blocks `inc/`, `data/` and leftover WordPress files |
| `inc/config.php` | **Edit me:** business details, contact email, Amazon tag, **upcoming market dates** |
| `inc/data.php` | Shop categories and Amazon picks, game metadata, seasonal editions |
| `inc/routes.php` | Static page routes, old→new URL map (301), removed URLs (410) |
| `inc/guides/*.php` | One file per guide article (drop in a new file and it's live and in the sitemap) |
| `inc/pages/*.php` | Page templates |
| `inc/layout.php` | Head/header/footer, SEO meta, JSON-LD schema, product cards |
| `inc/forms.php` | Contact, vendor application and newsletter handling (emailed + logged to `data/*.jsonl.php`, which start with `exit` so they are never downloadable) |
| `assets/` | CSS, JS (site + one file per game), images |
| `inc/amazon.php`, `tools/refresh-amazon.php` | PA-API client and daily cache refresh |
| `data/` | Private, writable: form submissions and the CSRF secret. Never web-accessible |
| `rollback/` | Backups of the old WordPress site's `.htaccess` + `index.php` |
| `wp-loader/` | Unused alternative (WordPress must-use plugin loader); the platform locks `mu-plugins` |

## URL map

- Kept and rewritten (301): `/about-us/`→`/about/`, `/our-events/`→`/events/`, `/contact-us/`→`/contact/`,
  `/write-for-us/`→`/vendors/`, the four event posts→`/events/{season}-vintage-market-houston/`, and the relevant
  Houston, decorating and shopping posts→`/guides/…`. Categories redirect to the closest hub.
- Removed (410 Gone): about 36 off-topic apartment, salary, real-estate and roofing posts, plus all `wp-*` paths.
- New: `/shop/` with 8 category pages (64 Amazon picks tagged `josephrayditt-20`), `/play/` with 5 games,
  `/food-trucks/`, `/vendors/`, `/affiliate-disclosure/`, `/privacy-policy/`, dynamic `/sitemap.xml`.

## Amazon product images (Product Advertising API)

Shop cards show real Amazon product images and link straight to the product page. That data must come
from Amazon's Product Advertising API, the Associates-approved source; Amazon hosts the images, and the
site only caches their URLs.

1. In Associates Central go to Tools → Product Advertising API and create credentials
   (your account needs qualifying sales to be eligible).
2. On the server, create `data/amazon.php` (never commit it):
   `<?php return ['access' => 'AKIA…', 'secret' => '…'];`
3. Hostinger cron (already set up) runs `php …/public_html/tools/refresh-amazon.php` daily at 09:17.
   It searches Amazon for each pick (or uses its `asin`), saves the image, link and title to `data/amazon-cache.php`.
   Entries older than 48h are ignored, so cards fall back to the photo style rather than show stale data.

Without keys, cards use the category photo plus an icon, and links go to tagged Amazon searches.

## Common edits

- **Announce market dates:** add an entry to `UPCOMING_EVENTS` in `inc/config.php`. It appears on the home,
  events and season pages and produces Event schema.
- **Link a specific Amazon product:** add `'asin' => 'B0…'` to a product in `inc/data.php`. Otherwise the
  links go to tagged Amazon searches, so they never break.
- **Social links:** fill in `SOCIAL` in `inc/config.php`.

## Local preview

```sh
php -S 127.0.0.1:8000 -t . app.php
```

## Deploy

See `deploy.sh`. It uploads via the Hostinger file-browser TUS API, sending `.htaccess` last (that is the switch-over).
Switching back to WordPress means pointing the domain at website `67Tls7oNq` again. That site is untouched.
