# stonecoatedroofs.com — static rebuild

Static rebuild of [stonecoatedroofs.com](https://stonecoatedroofs.com) (Stone Coated Roofs — Texas's
specialist installer of stone coated steel roofing), replacing the WordPress/Elementor/Yoast site.
No database or plugins: generated HTML, one CSS file, two JS files, a tiny PHP front controller and
a PHP lead handler.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | **The deliverable** — upload its contents to `public_html/` |
| `public/home.html` + `public/index.php` | Homepage, served for `/` by the front controller (see Hosting) |
| `public/quote.php` | Handler for every estimate form and the popup |
| `public/redirects.php` | Generated 301 map for dead links the old posts pointed at |
| `public/assets/css/site.css` | Design system |
| `public/assets/js/site.js` | Header, motion effects, hail canvas, tabs, comparison, TOC, 3-second popup, form submit |
| `public/assets/js/tools.js` | The six reader tools |
| `public/wp-content/uploads/` | Mirror of the whole WordPress media library, every size (keeps old image URLs live) |
| `build.py`, `homepage.py`, `tools.py`, `siteconfig.py` | Generator |
| `content/wp.json` | Cleaned WordPress pages/posts (made by `extract.py` from the backup) |
| `content/new/*.html` | Pages added in the rebuild (meta JSON comment + body) |
| `validate.py` | Post-build checks |
| `backup/wordpress-2026-10-06/` | REST exports and rendered HTML of every URL on the WordPress site |

```sh
python3 build.py && python3 validate.py
```

`validate.py` fails the build if any of the 81 WordPress URLs or 923 media URLs is missing, any internal
link or image is broken, a page has ≠1 H1 / no canonical / bad JSON-LD, titles or descriptions repeat,
or the homepage names "Stone Coated Roofs" fewer than 14 times in its main content (currently 15).

## What changed vs. WordPress

- **URLs kept**: all 17 pages, 58 posts, 4 `/topic/` archives, `/blog/page/2/`, all sitemaps
  (`sitemap_index.xml`, `page-`, `post-`, `category-sitemap.xml`). Feeds, `/wp-admin`, `/author/`,
  `/topic/*/page/N/`, `*/feed/` and the ~40 dead `/blog/<slug>/` links in old posts 301 to the right page.
- **Design**: copper-on-charcoal from the logo, Fraunces + Inter, animated hail canvas in the hero, word-by-word
  headline reveals, scroll reveals, count-up stats, an exploded "layers" diagram, card tilt/glow, magnetic
  buttons, brand marquee, animated Texas map, reading-progress bar. All motion respects `prefers-reduced-motion`
  and content stays visible without JS.
- **Popup**: estimate form opens 3 s after load; after a close it stays away for 24 h, and never shows again after a
  submission or on `/free-quote/`. Mobile renders it as a bottom sheet.
- **Tools** (`/tools/`): stone coated roof cost calculator, lifetime cost (vs asphalt, with break-even), Class 4 insurance
  discount estimator, hail damage checklist ("do I need a new roof after hail"), roof maintenance checklist + log
  (save/print/CSV), roof weight calculator. Planning figures follow the site's own ($10–$18/sq ft installed; 5–25% Class 4 discounts).
- **SEO from Search Console**: titles/descriptions/H1s retuned for the queries with impressions (`SEO` and
  `AREA_KEYWORDS` in `siteconfig.py`); city pages get "Stone Coated Steel Roofing in <City>, TX" H1s.
  New pages: 14 DFW city pages (Frisco, Coppell, Colleyville, Denton, Prosper, McKinney, Westlake, Keller, Southlake,
  Grapevine, Grand Prairie, Mesquite, Irving, Lewisville) and 3 guides (`/storm-damage-roof-replacement/`,
  `/roof-types-for-insurance/`, `/stone-coated-steel-roofing-market/`). JSON-LD: RoofingContractor, BreadcrumbList,
  BlogPosting, Service, FAQPage, WebApplication, ItemList.

## Leads

`quote.php` validates the form (name, 10-digit phone, city), drops honeypot spam, rate-limits per IP, appends each
request to `scr-leads/quote-requests.php` (the host doesn't let PHP write above `public_html`, so the file starts with a
`<?php … exit; ?>` guard — fetching it over the web returns an empty 404; read it in the file manager), and — if
`scr-config.php` exists in `public_html/` or one level up — emails it:

```php
<?php return ['to' => 'you@example.com', 'from' => 'no-reply@stonecoatedroofs.com'];
```

## Hosting

Hostinger Agency (Agency Growth plan, order 1008744732).

- **Live:** website UID `VgoSvHI3B` (plain php-fpm, PHP 8.5), created 2026-10-06; stonecoatedroofs.com moved onto it the same day.
- **Old WordPress site:** UID `MSMw69clR` (wp-6.9.4) — **left intact**, only the domain was unlinked. To roll back, unlink the
  domain from `VgoSvHI3B` and link it to `MSMw69clR` again. Delete it once you're happy with the rebuild.
- **First deploy** used `agency-hosting_files_import-website-from-archive` (zip uploaded to `.h5g/`). That import *replaces the whole
  site*, including `scr-leads/`, so **redeploy with `./deploy.sh`** (file-by-file, never deletes).

The platform ignores `.htaccess`, serves existing files
directly and sends `/` and unknown paths to `index.php`, so the homepage is `home.html` and `index.php` serves it,
issues the redirects and returns `404.html` with a real 404. (`home.html` canonicalises to `/` and is disallowed in
robots.txt.) Deploy with `./deploy.sh` (header explains credentials), then clear the cache.

Local preview: `php -S 127.0.0.1:8099` needs a small router (static files, `dir/index.html`, then `index.php`).

## Review before relying on it

- The three "field report" testimonials are carried over from the old homepage — keep them only if they are genuine.
- Cost, discount and weight figures are planning ranges, labelled as such.
- City pages were written for this rebuild; skim the local details (roads, neighborhoods, storms) for accuracy.
