# landscapelightingtexas.com — custom PHP rebuild

Replaces the WordPress/Elementor site with a hand-built PHP site: no database,
no plugins. Upload the contents of this folder to the website's `public_html/`.

## Structure

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical host/https, legacy WordPress redirects, feeds, sitemaps, routing, 404 |
| `inc/config.php` | Business details, navigation, services, areas, tools |
| `inc/registry.php` | **Every URL**: title, H1, meta description, image, dates. Add pages here |
| `inc/layout.php` | `<head>`, header, page hero, post layout, footer, JSON-LD |
| `inc/components.php` | Reusable sections (cards, FAQs + FAQPage schema, CTA, quote form, before/after…) |
| `inc/widgets.php` + `assets/js/tools.js` | The eight interactive tools |
| `inc/feeds.php` | `/feed/`, `sitemap_index.xml`, `page-/post-/category-sitemap.xml`, `robots.txt` |
| `inc/quote-handler.php` | Quote form: emails `info@` and saves a copy to `storage/` |
| `pages/`, `posts/` | Page and article content (see `CONTENT-GUIDE.md`) |
| `assets/` | `site.css`, `site.js`, optimized images |
| `wp-content/uploads/` | The old media library at its original URLs, so old image links keep working |

## URLs

All 11 URLs of the WordPress site are kept (`/`, `/about-us/`, `/quote/`,
`/areas/`, `/blog/`, `/category/general/`, `/landscape-lighting-complete-guide/`,
`/landscape-lighting-cost-calculator/`, `/privacy-policy/`, `/terms-of-service/`,
`/sitemap/`), plus `/feed/` and the Yoast-style sitemap URLs. New: `/services/`
(+8), `/areas/<region>/` (6), `/tools/` (+7), `/gallery/`, `/faq/` and six new
posts — 42 pages in total. WordPress-only paths (`/wp-admin/`, `/xmlrpc.php`,
`/comments/feed/`, `*/feed/`, `?p=`) 301 to their nearest equivalent.

## Working on it

```sh
php -S 127.0.0.1:8080 index.php     # local preview
php tests/render.php /about-us/     # render one URL (exit 1 on warnings)
python3 tests/validate.py           # titles, H1s, JSON-LD, links, keyword count
```

To add a blog post: add an entry to `$PAGES` in `inc/registry.php` with
`'type' => 'post'` and a `date`, then write `posts/<slug>.php`. It appears in
the blog, sitemap and feed automatically.

## Notes

- The homepage uses "Landscape Lighting Texas" 22 times in body copy (brief: 14+).
- Quote requests go to `QUOTE_TO` in `inc/config.php` via PHP `mail()`, and a
  copy is always written to `storage/quote-*.php` (guarded files, not web-readable).
- Prices are planning ranges and are labelled as such.

## Deploying

Live since 2026-10-06 on the Hostinger Agency website **UID `rs1D44oFt`**
(plain `php-fpm`, PHP 8.4). Upload with `./deploy.sh` (its header explains the
three File Browser credentials from `agency-hosting_files_generate-upload-url`),
then clear the cache with `agency-hosting_cache_clear-website`.

The previous WordPress website (**UID `BJyIEIRCP`**) was not deleted: the domain
was unlinked from it and moved to the new site, so its files and database are
intact as a fallback. To roll back, unlink the domain from `rs1D44oFt` and link
it to `BJyIEIRCP` again. Rendered copies of every old page and the old sitemaps
are in `../backup/landscapelightingtexas-wordpress-2026-10-06/`.

The H5G platform serves existing files directly and sends unknown paths to
`index.php`; it ignores `.htaccess` (kept for other hosts). Unknown `*.php`
paths get the platform's own 404, so `/wp-login.php` and `/xmlrpc.php` 404
rather than redirect.
