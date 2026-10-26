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
**Live:** betteroutdoors.net on the existing Hostinger web hosting account
(user `u401386392`, order 64270646, LiteSpeed, `.htaccess` honored), document root
`domains/betteroutdoors.net/public_html`. Went live 2026-10-26.

The old WordPress install was moved, untouched, into
`public_html/wp-backup-2026-10-26/` (database left in place; `wp-config.php` is in that
folder). The folder has its own `Require all denied` `.htaccess`, so it is not
reachable from the web. Kept in the web root: the two Google Search Console
verification files and Hostinger's `.private` folder. Only the WordPress root
`.htaccess` was not preserved (WordPress regenerates it from Settings → Permalinks).

To restore WordPress: move the contents of `wp-backup-2026-10-26/` (except its
`.htaccess`) back into `public_html/`, remove the new site's files, re-save permalinks,
and clear the cache.

Deploy: get credentials with `hosting_files_generate-upload-url`
(username `u401386392`, domain `betteroutdoors.net`); its `url` already ends in
`/public_html`, so upload paths are relative to the web root. Then clear the cache
with `hosting_cache_clear-website` (LiteSpeed caches pages).

`index.php` forces https (via `X-Forwarded-Proto` or `HTTPS`) and strips `www` on the
real domain; other hosts get `X-Robots-Tag: noindex`.

The Agency Growth preview copy (`yBoxhCPNC`) was deleted on 2026-10-26; `deploy.sh` still
works for an Agency-plan layout if one is ever needed.

## Scheduled publishing
A post goes live automatically when its `date` (US Central) arrives: until then its URL
404s and it is left out of listings, search, related posts and the sitemaps. Pages are
cached by LiteSpeed for at most 3 hours (`X-LiteSpeed-Cache-Control`), so a new post can
take up to 3 hours after midnight to appear in the homepage/blog lists. Preview everything
locally with `BO_SHOW_SCHEDULED=1 php -S 127.0.0.1:8098 index.php`.

Current schedule: Oct 26 draw length, Oct 29 RTH packages, Nov 2 Species XT, Nov 5 sight-in,
Nov 9 Legit Maxx, Nov 13 Mathews sights, Nov 17 arrow weight, Nov 20 bow press,
Nov 24 treestand tips, Nov 28 camping bow.

## Adding a post
1. Add an entry to `$POSTS` in `inc/config.php` (title, h1, desc, kw, image, dates, cat).
   Featured images for `/assets/img/posts/` entries come from `python3 scripts/post_images.py`.
2. Create `content/posts/<slug>.php` — copy an existing post; use the helpers.
3. Upload images to `wp-content/uploads/2026/01/` (or any path) and reference by filename.

## Favicons and analytics
`python3 scripts/favicons.py` rebuilds `favicon.ico` (16/32/48), the PNG favicons,
`apple-touch-icon.png`, the web-app manifest icons and `site.webmanifest` from the
original mountain icon (white on navy). Google Analytics (`GA_ID` in `inc/config.php`,
G-XXMML8G00W) is printed in every page's `<head>` by `inc/layout.php`, only when the
host is betteroutdoors.net, so local/preview traffic is not counted.

## Contact form
`/contact-us/` sends mail with PHP `mail()` to info@betteroutdoors.net (honeypot +
timing check). Make sure that mailbox exists / forwards somewhere.
