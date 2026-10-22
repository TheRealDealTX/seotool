# underdeskelliptical.com: custom PHP rebuild

A hand-built PHP site that replaces the WordPress/Elementor install on
underdeskelliptical.com. It has no database, no plugins and no build step. PHP renders
every page from plain content files.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: the whole URL map, legacy WordPress 301s and the XML sitemaps |
| `inc/config.php` | Site name, **Amazon tag (`underdeskellipticaljditt-20`)**, categories, tags, nav, contact email |
| `inc/products.php` | Product catalog (ASINs, pros/cons). All Amazon links are generated from it |
| `inc/functions.php` | Affiliate link builders, shortcodes, product cards, compare tables, schema |
| `inc/tools.php` | The six interactive tools (markup). Behavior is in `assets/js/site.js` |
| `inc/layout.php` | `<head>`, header and footer |
| `inc/contact.php` | Contact form handler |
| `templates/` | Page templates: home, post, archive (blog/topic/tag), page, tool, search, sitemaps, 404 |
| `content/posts/<slug>.php` | One file per article. The filename is the URL slug |
| `content/pages/` | About, contact, affiliate disclosure, privacy, terms |
| `content/tools/` | SEO copy and FAQs under each tool |
| `wp-content/uploads/` | The original featured images at their original URLs |
| `assets/img/thumbs/` | 768px card versions of the featured images |
| `dev/` | Local preview router, CLI renderer and the validator. Not deployed |

## URLs: nothing 404s

Every URL from the old Yoast sitemaps still works at the same address. That covers 55
posts, `/blog/`, 7 pages, 10 `/topic/` categories and 8 `/tag/` archives.
`dev/legacy-urls.txt` lists them, and `dev/check.py` verifies them. The same sitemap
URLs (`/sitemap_index.xml`, `/post-sitemap.xml`, …) are served live, so Search Console
needs no changes.

WordPress leftovers redirect with a 301: `/feed/`, `/<post>/feed/`, `/category/x/`,
`/author/…`, `/blog/page/N/`, `/wp-admin`, `/wp-login.php`, `?p=`, and resized
`…-300x200.webp` image URLs (which redirect to the full-size image). Unknown paths get
a real 404.

New URLs: `/tools/` and six tool pages, and search at `/?s=` (noindexed).

## Affiliate links

Never paste Amazon URLs into content. Use the shortcodes, and `amz_url()` adds the tag
and `rel="sponsored nofollow noopener"`:

```
[[amazon:cubii-jr2]]                 inline link with the product name
[[amazon:cubii-jr2|anchor text]]     inline link, custom text
[[button:cubii-jr2]]                 "Check Price on Amazon" button
[[product:cubii-jr2|1]]              product card (ranked #1)
[[compare:cubii-jr2,deskcycle-ellipse,ancheer]]   comparison table
[[search:query|anchor]]              tagged Amazon search link
[[tool:calories]]                    calories | steps | clearance | timer | quiz | finder
```

Brands without a stable ASIN (Geoneo, Flex Fitness, Viamotion, Fousae, Fntkech, Yosuda
manual, Cubii Pro) link to a tagged Amazon search. To switch one to a direct product
link, add its `asin` in `inc/products.php`.

## Adding a post

Copy any file in `content/posts/` to `content/posts/<new-slug>.php` and edit it. It
appears automatically on `/blog/`, its category and tag pages, the sitemaps, related
posts and search. Then run the checks below.

## Local preview and checks

```sh
php -S 127.0.0.1:8090 dev/router.php      # mimics Hostinger routing
python3 dev/check.py dev/legacy-urls.txt  # validator: must print OK
php dev/render.php /some-slug/            # render one page in the CLI
```

`check.py` crawls every sitemap URL and verifies:
- status 200 on every page and every legacy URL
- one H1 per page, plus unique titles and meta descriptions
- canonical tags and valid JSON-LD
- no broken internal links or missing assets
- every Amazon link carries the tag and `rel=sponsored`
- the homepage says "Under Desk Elliptical" at least 14 times

## Hosting and deploying

The site runs on a plain **php-fpm** website on the Hostinger Agency plan (UID
`FQYNNuIDk`, Phoenix, PHP 8.5, created 2026-10-22). It replaced the WordPress website
`wdHcdWujW`, whose `index.php` was locked by Hostinger's WordPress config lock and could
not be overwritten. That platform serves existing files directly, ignores `.htaccess`, and
sends unknown *directory-style* paths to `index.php`. Unknown `.php`/image paths get the
platform's own 404 and never reach the router, which is why:

- the old WordPress resized images (`…-300x200.webp`, `…-1024x683.webp`, 783 files) were
  copied onto the server from the WordPress backup instead of redirected. They are not in
  git; re-copy them from the backup zip if the website is ever rebuilt from scratch.
- every file under `inc/`, `templates/` and `content/` starts with a guard that returns 404
  when requested directly.

Do **not** add `index.html` files: an `index.html` would be served for unknown paths
instead of `index.php`.

Deploy: `./deploy.sh` (see its header for the three File Browser credentials), then clear
the site cache. The WordPress backup is described in
`../backup/underdeskelliptical-wordpress-2026-10-22/README.md`.

## Contact form

Messages are saved to `data/messages.php` on the server (its first line is `exit`, so
it cannot be viewed over the web; read it in File Manager). To also receive them by
email, set `CONTACT_TO` in `inc/config.php`.
