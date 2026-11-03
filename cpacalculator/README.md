# cpacalculator.com — custom PHP rebuild

Custom HTML/PHP replacement for the WordPress site at https://cpacalculator.com.
No WordPress, no database, no Composer — plain PHP 8.x templates, one stylesheet, vanilla JS.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: routing, canonical host/scheme, legacy WordPress 301s, 404s |
| `app/bootstrap.php` | Site constants, `TOOLS` / `POSTS` / `SALARY_PAGES` registries, layout, schema and UI helpers |
| `app/data/tax.json` | **Single source of truth** for IRS figures (2026 + 2025). PHP reads it; it is inlined into pages as `window.TAX` for the JS |
| `app/pages/` | One PHP file per page (`calculators/`, `blog/`, legal, about, methodology, contact, 404) |
| `app/pages/calculators/salary.php` | Programmatic `/calculators/federal-income-tax/{amount}/` pages for the amounts in `SALARY_PAGES` |
| `app/mailer.php` | Tiny SMTP client used by the contact form |
| `app/sitemap.php` | Generates `/sitemap.xml` from the registries |
| `assets/css/site.css` | Design system |
| `assets/js/calc-core.js` | Shared tax engine (brackets, FICA, SE tax, QBI, CTC, LTCG stacking) + UI helpers |
| `assets/js/site.js` | Nav, scroll progress, reveal/parallax effects, counters, TOC, tabs |
| `assets/js/tools/*.js` | One script per calculator |
| `wp-content/uploads/` | The old WordPress media library, kept so old image URLs still return 200 |

## Hosting notes (Hostinger Agency / H5G, website UID `17XGw98Uo`)

- The platform serves existing files directly, **ignores `.htaccess`**, and sends `/` plus any unknown path to
  `index.php`. So all routing lives in `index.php`, and page URLs must not exist as real directories.
- Direct requests to `app/*.php` execute PHP and print nothing (each file starts with `defined('CPA') or exit;`).
- Only `public_html/` is writable through the File Browser API; nothing can be stored above it.

## URLs kept from WordPress

Every URL in the old Yoast sitemaps resolves: `/`, `/calculators/`, `/calculators/federal-income-tax/`,
`/calculators/1099-tax-calculator/`, `/blog/` and its 3 posts, `/topic/guides/`, `/about-us/`, `/our-methodology/`,
`/contact/`, `/disclaimer/`, `/privacy-policy/`, `/terms-of-use/`. Old `?p=`/`?page_id=` shortlinks, Yoast sitemap
URLs, feeds, `/category/`, `/author/` and `wp-admin`/`wp-login.php` 301 to the nearest equivalent.

## Contact form

Posts to `/contact/`, sends through `smtp.hostinger.com:465` as `info@cpacalculator.com` with the visitor as Reply-To.
Honeypot + minimum-time check against bots. **The mailbox password is not in git**: it lives only on the server
in `public_html/app/config.local.php` (git-ignored, excluded by `deploy.sh`):

```php
<?php defined('CPA') or exit;
return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@cpacalculator.com', 'pass' => '…'];
```

## Updating tax figures each year

1. Add the new year to `app/data/tax.json` and set `"default"` to it.
2. Review copy that mentions law changes (search for `OBBBA`, `Rev. Proc.`).
3. Deploy. Every calculator, table, worked example and salary page recalculates from the data file.

## Local preview

```bash
php -S 127.0.0.1:8099 -t . dev-router.php
```

where `dev-router.php` returns `false` for existing static files and otherwise requires `index.php`.

## Deploying

```bash
export FB_URL=… FB_AUTH=… FB_REST=…   # from agency-hosting_files_generate-upload-url
./deploy.sh
```

Then clear the site cache in hPanel if pages look stale.
