# puregoatfarms.com — custom PHP rebuild

A hand-built PHP site replacing the WordPress/Elementor install at
[puregoatfarms.com](https://puregoatfarms.com). No database, no plugins, no
build step: upload this folder's contents to `public_html` and it runs on any
PHP 8.1+ host.

## What was carried over

| Item | Where |
| --- | --- |
| Every live URL (home, about, blog, contact, privacy, terms, both posts, all 4 categories) | Same paths, same trailing slashes |
| All 38 files of the WordPress media library | `wp-content/uploads/2026/07/` — old image URLs keep returning 200 |
| Logos, site icon, OG image, photos | Used from the same upload paths |
| Colors & fonts (Elementor kit) | `assets/css/style.css` `:root` — #3B2A1E, #A34B2A, #6B5642, #C89A3B, #202A19, #FFFCF6; Fraunces / Libre Franklin / Space Mono |
| Google Search Console verification file | `google9d8d740410b54935.html` (byte-identical to the live one) |
| Google Analytics tag `G-9578859YFV` | Same snippet in every page `<head>` (`app/layout.php`) |
| Amazon affiliate links (`josephrayditt-20`) and disclosure boxes | Posts + `AFF` catalogue in `app/helpers.php` |
| Yoast sitemaps | `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml` (+ new `/tool-sitemap.xml`), generated live |
| RSS feed, llms.txt, robots.txt | `/feed/` (generated), `llms.txt`, `robots.txt` |
| Original in-post calculators | Kept inside the two original posts |

Legacy WordPress URLs 301 to the closest page: `/feed/` variants, `/wp-admin/`,
`/wp-login.php`, `/xmlrpc.php`, `/category/uncategorized/`, `/blog/page/N/`,
`/author/*`, `/tag/*`, date archives, `?p=` / `?page_id=` / `?s=`, `/<post>/amp/`,
`/sitemap.xml`. `www.` and plain-http requests 301 to `https://puregoatfarms.com`.

## What's new

- **5 new posts** targeting the GSC query clusters (dated 24 Jul, 12 Aug, 29 Aug,
  17 Sep, 6 Oct 2026): milk per day by breed, how often to milk, milk without
  pregnancy, best dairy breeds, how to increase milk production.
- **7 interactive tools** under `/tools/`: milk yield, production estimator
  (lactation-curve chart), cheese herd, gestation/kidding timeline (.ics export),
  feed & hay, breed-finder quiz, milk unit converter. Plus a live milk estimator
  on the homepage.
- **New pages:** `/tools/`, `/start-here/`, `/faq/`, `/affiliate-disclosure/`,
  `/sitemap/`, a real 404 page.
- The two original posts got a featured-snippet "Quick answer", FAQ schema,
  a breed table and internal links to the new posts; their bodies are otherwise
  unchanged.

## Layout

```
index.php            front controller (all routing in app/routes.php)
app/config.php       site constants, categories, tools, nav
app/posts.php        blog post registry (title, SEO title, dates, FAQ, image)
app/posts/*.php      post bodies
app/pages/*.php      page templates
app/tools/*.php      tool widgets + copy
app/layout.php       <head>, header, footer (GA tag lives here)
app/helpers.php      escaping, icons, cards, JSON-LD, affiliate boxes
app/forms.php        contact + newsletter handlers
assets/css|js|img    styles, site JS (main.js), tool JS (tools.js), blog covers
```

**Add a post:** add an entry to `POSTS` in `app/posts.php` and a body file
`app/posts/<slug>.php`. It appears on the blog, its categories, the sitemap,
the RSS feed and related-post blocks automatically.

## Hosting notes

The new site runs on its own **plain PHP website** on the Hostinger Agency
plan: UID `6frlLGPcw`, PHP 8.3, Phoenix, preview address
`https://darkorchid-squid-604225.hostingersite.com` (created 2026-10-19). The
old WordPress site is UID `VSUHIRjmA`. It can't be overwritten in place: the
platform locks WordPress core on managed WP sites (`index.php`, `wp-config.php`,
`wp-admin`, `wp-includes` refuse moves/overwrites).

The platform serves real files directly, ignores `.htaccess`, and sends any
other path to `index.php` — except nonexistent `*.php` paths (e.g.
`/wp-login.php`), which get the platform's own 404. `.htaccess` is included
for Apache/LiteSpeed hosts that honour it.

On a `*.hostingersite.com` address the router keeps redirects on that host and
sends `X-Robots-Tag: noindex`, so the preview can be tested without bouncing
to the live domain or being indexed.

`app/` and `storage/` are not protected by `.htaccess` here; every PHP file in
them exits immediately with an empty response, so nothing is exposed.

**Forms.** Contact and newsletter submissions are emailed to
`info@puregoatfarms.com` with PHP `mail()` and logged to `pgf-storage/` one
level above the web root when writable, otherwise `storage/` (the case on
this host). Logs are `.php` files that exit on request, so they are never
served. If mail doesn't arrive, point `send_mail()` in `app/forms.php` at SMTP.

## Deploying

Upload changed files to website `6frlLGPcw` through the File Browser TUS
endpoint (`agency-hosting_files_generate-upload-url` gives the URL and keys;
credentials expire after a few hours), then clear the site cache.

**Live since 2026-10-19 03:37 UTC.** `puregoatfarms.com` was unlinked from the
WordPress website `VSUHIRjmA` and assigned to `6frlLGPcw`; the existing SSL
certificate (apex + www) moved with it and the cache was cleared. The
WordPress website still exists with its files and database intact but no
domain. To roll back, unlink `puregoatfarms.com` from `6frlLGPcw` and link it
to `VSUHIRjmA` again. Delete `VSUHIRjmA` once the new site has proven itself.

Hostinger's CDN challenges headless browsers once (a 403 followed by a
reload to 200); regular browsers, curl and Googlebot get a 200 directly.

## Open items

- Terms of Use had `[Insert State/Country]` placeholders; they now read
  "the laws of the United States and the state in which Pure Goat Farms
  operates". Name the state if you want it specific.
- The original contact page linked `mailto:@puregoatfarms.com` (missing
  "info"); fixed to `info@puregoatfarms.com`.
- Breed milk figures are typical published ranges, labelled as estimates.
