# springlandscapelighting.com — custom PHP rebuild

Custom HTML/PHP site replacing the WordPress/Elementor build (no CMS, no database).
Live since 2026-10-06 on the Hostinger Agency website **o4crWzsNE** (plain php-fpm, PHP 8.4).

## Layout

| Path | What it is |
| --- | --- |
| `public_html/index.php` | Front controller; loads `app/bootstrap.php` |
| `app/config.php` | Business details + registries: `SERVICES`, `AREAS`, `TOOLS`, `CATEGORIES`, `POSTS`, `NAV` |
| `app/routes.php` | Static page map, redirects, routing, 404 |
| `app/layout.php` | `<head>`, header/mega-menu, footer, site-wide JSON-LD |
| `app/helpers.php` | Components: heroes, cards, `faq_block()` (+FAQPage schema), `cta_box()`, `tool_embed()`, quote form |
| `app/pages/` | Page templates (home, about, services, process, faq, tools, inspiration, blog, post, service, area, tool, legal, 404) |
| `app/posts/`, `app/services/`, `app/areas/` | Body copy for blog posts, service pages and area pages |
| `app/tools/{slug}.php` / `{slug}-guide.php` | Interactive tool markup / explainer copy under each tool |
| `app/partials/house-scene.php` | SVG night scene with switchable lighting layers (homepage scroll scene, visualizer, inspiration) |
| `app/sitemaps.php` | `sitemap_index.xml`, `page-`/`post-`/`category-sitemap.xml` (same URLs as Yoast), `/feed/` |
| `app/lead.php` | Quote/contact form handler: emails `LEAD_TO` and appends to `app/data/leads.php` |
| `assets/css/main.css`, `assets/js/main.js`, `assets/js/tools.js` | Styles, scroll/visual effects, calculators |
| `wp-content/uploads/2026/07/` | Old WordPress media, kept so every old image URL still resolves |
| `backup-wordpress/` | Original `.htaccess`, `index.php`, `robots.txt`, `llms.txt` and text of the old pages |

`app/` files exit unless loaded through the front controller. `app/data/` holds server-written
files (form HMAC secret, lead log) and is never deployed or committed.

## URLs

All original URLs are preserved: `/`, `/about-us/`, `/quote/`, `/blog/`, `/privacy-policy/`,
`/terms-of-service/`, `/electricity-landscape-lighting-use/`, `/category/general/` and the Yoast
sitemap URLs. The old homepage hash links got their own pages — `#services` → `/services/`,
`#process` → `/our-process/`, `#faq` → `/faq/` — and the homepage keeps those ids too.

New: 6 service pages, 6 service-area pages, 7 tools, 9 new posts, 3 new categories,
`/inspiration/`, `/contact/`, `/service-areas/`, `/tools/`, `/thank-you/` (noindex).

## Adding a blog post

1. Add an entry to `POSTS` in `app/config.php` (slug → title, seo, desc, date, cat, img, excerpt).
2. Create `app/posts/{slug}.php` (start with `<?php defined('SLT') || exit; ?>`; see `CONTENT_BRIEF.md`).
Sitemaps, feed, blog index and related posts pick it up automatically.

## Local preview

```sh
php -S 127.0.0.1:8099 -t public_html dev-router.php
```

## Deploy

`./deploy.sh` (credentials from `agency-hosting_files_generate-upload-url` for website
`o4crWzsNE`), then clear the cache (`agency-hosting_cache_clear-website`). Bump `ASSET_VER`
in `config.php` when CSS/JS change.

## Hosting history

The old WordPress website (`Vylg5liat`) has a locked, symlinked core (`index.php`,
`mu-plugins`), so a custom front controller could not be installed there. A new plain PHP
website was created, tested on its temporary domain, and the domain was moved to it on
2026-10-06 (same server IP, SSL carried over). `Vylg5liat` still exists with its files and
database intact but no domain attached — relink the domain to it to roll back, or delete it
once the new site is confirmed.
