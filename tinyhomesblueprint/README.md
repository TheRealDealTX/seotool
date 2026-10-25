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
| `inc/config.php` | Business details, navigation, **plans** (`$PLANS`), **route registry** (`$ROUTES`), old-URL redirects |
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
(style, tool and guide cards). To add a plan, add it to `$PLANS` and drop its image in
`assets/img/`; its page at `/plans/<slug>/` is generated.

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

## Rollback

The WordPress install (wp-admin, wp-content, database) was left untouched on the server. Only
`index.php` and `.htaccess` were replaced. To roll back, upload
`backup-wordpress/index.php.wordpress` as `index.php` and `backup-wordpress/htaccess.wordpress`
as `.htaccess`.

## Contact form

`/contact/` emails `contact@tinyhomesblueprint.com` with PHP `mail()`, and writes a copy of every
lead to `thb-leads.log`, one level above `public_html` (outside the web root), in case mail
delivery fails. Spam protection: honeypot field, session token and a minimum fill time.

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
