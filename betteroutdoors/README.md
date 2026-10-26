# betteroutdoors.net — custom PHP rebuild

Replaces the WordPress/Elementor site with a small PHP site: no database, no
plugins. Same logo, icons (Font Awesome), fonts (Roboto Slab / Roboto) and
colors (navy `#061E29`, teal `#1D546D`, sage `#5F9598`, orange `#FF6930`).

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: routes, legacy WordPress redirects, sitemaps, 404 |
| `inc/config.php` | Site constants, Amazon tag (`betteroutdoors-20`), post + tool registry, nav |
| `inc/helpers.php` | Amazon links, product cards, tables, callouts, verdict, FAQ (+schema), TOC |
| `inc/layout.php` | `<head>`, header, search overlay, CTA band, footer |
| `pages/` | Page templates (home, post, tool, blog, category, about, contact, legal, 404, sitemap) |
| `content/posts/<slug>.php` | Article bodies — slugs are the original WordPress URLs |
| `content/tools/<slug>.php` | Interactive tools (markup + explainer copy) |
| `assets/` | `site.css`, `site.js` (effects, search, filters), `tools.js` (calculators) |
| `wp-content/uploads/` | The old WordPress media library, same paths, so every old image URL still works |
| `validate.py` | Crawls a running copy and checks status codes, links, schema, anchors, Amazon tags |

## URLs kept (no 404s)
All 16 URLs from the old Yoast sitemaps return 200 at the same address, and every
`#h-…` heading anchor from the old posts is preserved. Old WordPress paths
(`/feed/`, `/wp-admin/`, `/author/…`, `/tag/…`, `/{post}/feed/`, `?s=`, `/pages/contact-us`,
`/collections/…`) 301 to the nearest page. `sitemap.xml`, `sitemap_index.xml`,
`post-sitemap.xml`, `page-sitemap.xml` and `category-sitemap.xml` all still resolve.

New pages: `/tools/` plus five tools (draw length, arrow speed, kinetic energy,
bow finder quiz, bowhunting checklist).

## Local preview
```sh
php -S 127.0.0.1:8099 index.php
python3 validate.py http://127.0.0.1:8099
```

## Hosting
Hostinger Agency Growth plan, plain `php-fpm` website. The platform serves real
files directly, ignores `.htaccess`, and sends unknown paths to `index.php`.
Internal PHP files exit immediately unless loaded through `index.php`.
Non-production hosts (the `*.hostingersite.com` preview) send `X-Robots-Tag: noindex`;
on betteroutdoors.net, `index.php` also forces https and strips `www`.

Website UID `yBoxhCPNC` (order 1008744732, Boston DC, PHP 8.3), preview host
olive-badger-748849.hostingersite.com. Deployed 2026-10-26.

Deploy with `./deploy.sh` (see header comment), then clear the site cache.

## Adding a post
1. Add an entry to `$POSTS` in `inc/config.php` (title, h1, desc, kw, image, dates, cat).
2. Create `content/posts/<slug>.php` — copy an existing post; use the helpers.
3. Upload images to `wp-content/uploads/2026/01/` (or any path) and reference by filename.

## Contact form
`/contact-us/` sends mail with PHP `mail()` to info@betteroutdoors.net (honeypot +
timing check). Make sure that mailbox exists / forwards somewhere.
