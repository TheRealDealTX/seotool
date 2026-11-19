# exitrealestate540.com — custom PHP site

Hand-built PHP site (no WordPress, no database, no framework) replacing the old
WordPress blog. Texas / Houston real estate guides, 12 free calculators and
Amazon affiliate gear recommendations (tag `josephrayditt-20`).

## Hosting

- Hostinger Agency Growth, website UID **`uiVmbjn30`** (plain `php-fpm`, PHP 8.4, Phoenix DC).
- The platform serves existing files directly, **ignores `.htaccess`**, and sends every
  other request to `index.php`, which routes all clean URLs.
- The old WordPress site (UID `btCAGwKUL`) was **not deleted**; it is still reachable on its
  preview domain `brown-wasp-183513.hostingersite.com`. Its REST export (53 posts, pages,
  categories) is in `../exitrealestate540-wp-backup/`.

## Layout

| Path | What |
| --- | --- |
| `index.php` | Front controller / router, canonical host + 301s for legacy WordPress URLs |
| `inc/config.php` | Site settings, categories, product groups, legacy redirect map, contact email |
| `inc/functions.php` | Helpers: posts, products, Amazon links, schema.org, icons |
| `inc/layout.php` | `<head>` (meta, OG, JSON-LD), header, footer, post cards |
| `inc/pages/*.php` | Page templates (home, blog, post, category, tools, tool, gear, contact, static, sitemap, feed, 404) |
| `inc/tools.php` + `inc/tool-views.php` | Tool registry (SEO copy, FAQ) and calculator markup |
| `assets/js/tools.js` | All calculator logic (vanilla JS, runs in the browser) |
| `content/posts/<slug>.php` | One blog post per file — see `content/POST_FORMAT.md` |
| `content/products.php` | Amazon product catalog |
| `scripts/make_images.py` | Regenerates logo, favicons and per-post OG images |

## Adding a post

1. Create `content/posts/<slug>.php` following `content/POST_FORMAT.md`.
2. `python3 scripts/make_images.py` to make its share image.
3. Upload the new files (`./deploy.sh` uploads everything). The post appears on the blog,
   its category, the sitemap and the RSS feed automatically.

## Deploying

```sh
export HR_FB_URL=... HR_FB_AUTH=... HR_FB_REST=...   # from agency-hosting_files_generate-upload-url
./deploy.sh
```
Then clear the cache (`agency-hosting_cache_clear-website`).

## Contact form

Messages are appended to `site-data/messages.php` on the server (a PHP file that exits
immediately, so it cannot be read over the web — open it in hPanel's File Manager).
Set `contact_email` in `inc/config.php` to also receive them by email.

## Local preview

`php -S 127.0.0.1:8000 router.php` with a router that returns `false` for existing files
and otherwise requires `index.php`.
