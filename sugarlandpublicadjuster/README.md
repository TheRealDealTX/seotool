# sugarlandpublicadjuster.com — custom PHP rebuild

Replaces the WordPress/Elementor site on Hostinger Cloud Enterprise
(account `u401386392`, order 64270646). Plain PHP 8 + one CSS file + vanilla JS.
No database, no plugins. `public_html/` is uploaded as-is.

| Path | What it is |
| --- | --- |
| `public_html/inc/config.php` | Business details (phone, lead email, firm/license), author, navigation |
| `public_html/inc/layout.php` | `<head>`, JSON-LD graph, header, footer, 4-second lead popup, components |
| `public_html/inc/posts.php` | Blog registry — posts live at `/{slug}/`, bodies in `content/posts/{slug}.html` |
| `public_html/inc/pages.php` | Page list for the XML and HTML sitemaps |
| `public_html/lead.php` + `inc/mailer.php` | Form handler: emails every lead **from info@sugarlandpublicadjuster.com to jditt@risepublicadjusting.com** and keeps a CSV copy outside the web root (`../slpa-leads/leads.csv`, send log in `../slpa-leads/mail.log`) |
| `public_html/sitemap.php` | Serves the Yoast-era URLs `/sitemap_index.xml`, `/page-sitemap.xml`, `/post-sitemap.xml`, `/category-sitemap.xml` |
| `public_html/assets/js/tools.js` | All calculators/tools |
| `public_html/assets/js/weather.js` | Live weather (NWS API, NOAA river gauge — no API keys) |
| `public_html/wp-content/uploads/` | The original WordPress media, kept at the same URLs |
| `backup/` | Notes on the WordPress removal (files + database deleted 2026-10-13) |

## URLs kept from WordPress
`/`, `/about-us/`, `/services/`, `/contact/`, `/blog/`, `/category/general/`,
`/privacy-policy/`, `/terms-of-use/`, `/why-use-a-public-adjuster/`,
`/fire-insurance-adjuster-secrets/`, `/the-smart-homeowners-guide-to-finding-the-right-public-adjuster/`,
the four Yoast sitemaps, every `/wp-content/uploads/…` image, `/llms.txt` and the
Google verification file. Old WordPress endpoints (`/wp-admin/`, `/wp-login.php`,
`/feed/`, `/author/…`) 301 to their nearest equivalent.

## Local preview and checks
```sh
php -S 127.0.0.1:8090 -t public_html dev-router.php   # emulates .htaccess
python3 validate.py                                   # crawl + SEO checks
```
`validate.py` checks status codes, PHP errors, one H1, unique titles/descriptions,
canonical URLs, JSON-LD, broken links/images, alt text, and that the homepage uses
"sugar land public adjuster" at least 14 times (plus the three related phrases).

## Deploy
See the header of `deploy.sh`, then clear the cache with `hosting_cache_clear-website`.

## Adding a blog post
1. Add an entry at the top of `POSTS` in `inc/posts.php`.
2. Save the body HTML as `content/posts/{slug}.html` (no H1; end with an optional FAQ block of `<details class="faq-item">`).
3. Create `{slug}/index.php` with the same two lines as the other post folders.
Posts are authored by Joseph Dittman automatically; sitemaps and the blog index update themselves.

## Lead email delivery
Leads are sent as `info@sugarlandpublicadjuster.com` (an active Hostinger mailbox).
If `../slpa-private/smtp.php` exists next to `public_html` (outside the web root),
`inc/mailer.php` sends through Hostinger's authenticated SMTP as that mailbox;
otherwise it falls back to PHP `mail()` with info@ as the From and envelope sender.
The private file looks like:

```php
<?php return ['host' => 'smtp.hostinger.com', 'port' => 465, 'secure' => 'ssl',
              'user' => 'info@sugarlandpublicadjuster.com', 'pass' => 'MAILBOX PASSWORD'];
```
Never commit that file.
