# tinyhomesblueprint.com: custom PHP rebuild

This replaces the WordPress/WooCommerce site at https://tinyhomesblueprint.com with a lightweight
custom PHP site. It needs no database and no plugins: one front controller, PHP page templates,
one stylesheet and vanilla JS tools.

Hosting: Hostinger, account `u401386392`, document root
`/home/u401386392/domains/tinyhomesblueprint.com/public_html`.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical redirects, old-URL 301s, `/sitemap.xml`, 404, page dispatch |
| `.htaccess` | https + non-www, blocks source folders and old WP entry points, routes everything else to `index.php` |
| `inc/config.php` | Business details, navigation, **route registry** (`$ROUTES`), old-URL redirects |
| `inc/plans.php` | **The plan catalog** (`$PLANS`): specs, copy and room-by-room geometry for every plan |
| `inc/plan-svg.php`, `build-plans.php` | Draw each plan's floor plan and front elevation SVG into `assets/plans/` from that geometry |
| `inc/mailer.php` | Contact-form email over SMTP through the contact@ mailbox |
| `inc/layout.php` | `page_start()` / `page_end()` (head, meta, schema, header, footer) and components (`plan_grid`, `faq_block`, `route_cards`, `cta_band`, `icon`, ...) |
| `pages/` | One template per page: `home.php`, `catalog.php`, `plan.php`, `styles/`, `tools/`, `guides/`, `company/` |
| `assets/css/site.css`, `assets/css/tools.css` | Styles |
| `assets/js/site.js`, `assets/js/tools/*.js` | Mobile nav, plan filters, the interactive tools |
| `validate.php` | Crawls a running copy of the site and checks every route (see below) |
| `deploy.sh` | Uploads the site to Hostinger through the File Browser API |
| `backup-wordpress/` | The original WordPress `index.php` and `.htaccess` (not deployed) |

## Adding a page

1. Add an entry to `$ROUTES` in `inc/config.php` (path, file, type, title, description).
2. Create the template in `pages/`, calling `page_start([...])` and `page_end()`.

It then appears automatically in `sitemap.xml`, the HTML sitemap, the footer and the matching hub
(style, tool and guide cards).

## Adding a plan

1. Add an entry to `$PLANS` in `inc/plans.php`: specs, copy, the `styles` it belongs to, and its
   `rooms` (and optional `loft` / `porch`) as `[label, x, y, w, d]` rectangles in feet. Rooms must
   tile the `W` x `D` footprint exactly; `sqft` is computed as main floor + loft.
2. Run `php build-plans.php` to draw its floor plan and elevation.
3. Run `php validate.php`; it fails on gaps or overlaps between rooms, a missing drawing, or an
   intro that doesn't state the right square footage.

The plan page at `/plans/<slug>/`, its catalog card, filters and style-page listings are generated.

## Local preview and checks

```sh
php -S 127.0.0.1:8099 -t . dev-router.php
php validate.php            # in another terminal
```

## Deploying

```sh
# credentials from the Hostinger API call hosting_files_generate-upload-url
export THB_FB_URL=... THB_FB_AUTH=... THB_FB_REST=...
./deploy.sh
```

`index.php` and `.htaccess` upload last, so the live site switches over only once every page is
in place.

## Old WordPress install

The WordPress files were removed from `public_html` on 2026-10-25. A full zip of them (wp-admin,
wp-includes, wp-content including uploads, wp-config.php) is kept on the server outside the web
root at `/home/u401386392/domains/tinyhomesblueprint.com/wordpress-backup-2026-10-25.zip`. The
WordPress MySQL database was not touched. `backup-wordpress/` holds the original `index.php` and
`.htaccess`.

## Contact form

`/contact/` emails `contact@tinyhomesblueprint.com` through authenticated SMTP
(smtp.hostinger.com:465) as the contact@ mailbox, sends the visitor a short confirmation, and
writes a copy of every lead to `thb-leads.log`, one level above `public_html`, in case delivery
fails. The SMTP password lives in `thb-secrets.php`, also one level above `public_html` and never
in this repo (format in `inc/mailer.php`); without it the form falls back to PHP `mail()`.
Spam protection: honeypot field, session token and a minimum fill time.

Analytics: Google Analytics 4 (`GA_ID` in `inc/config.php`) is loaded on every page.

## SEO notes

- Old WooCommerce URLs (`/shop/`, `/plan-category/styles/*`, `/cart/`, Yoast sitemaps, ...) are
  301-redirected to their new equivalents (`$REDIRECTS` in `inc/config.php`).
- `/embracing-tiny-homes-unlocking-the-advantages-of-compact-living/`, the only URL that ranked
  (for "compact living"), keeps its URL and was rewritten and expanded.
- Each page targets one primary keyword, chosen from DataForSEO search volumes (Oct 2026):
  tiny house plans / blueprints (22.2k), tiny house kits (22.2k), a frame house plans (6.6k),
  tiny house floor plans (5.4k), how much does a tiny house cost (5.4k), adu plans (5.4k),
  shipping container home plans (3.6k), shed to tiny house (2.9k), small cabin plans (2.9k),
  tiny house layout (2.4k), small farmhouse plans (1.3k), free tiny house plans (1.6k), and others.
- Schema: Organization + WebSite on every page, plus BreadcrumbList, FAQPage, Article (guides),
  Product (plans), ItemList / CollectionPage and WebApplication (tools).
