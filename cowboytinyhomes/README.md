# cowboytinyhomes.com — custom PHP rebuild

Replaces the WordPress/Elementor site with a hand-built PHP site (code kept PHP 7.4-compatible — the server's PHP is older than 8), which runs on
Hostinger Cloud Enterprise (account `u401386392`, document root
`domains/cowboytinyhomes.com/public_html`). It needs no database and no plugins.

## Layout

| Path | What it is |
| --- | --- |
| `public_html/index.php` | Front controller: clean URLs, 301s for old WordPress URLs, `sitemap.xml`, real 404s |
| `public_html/.htaccess` | Sends non-file requests to `index.php`, blocks `inc/`, `pages/` and the WP backup, and sets caching and security headers |
| `public_html/inc/config.php` | Business details (name, phone, email, cities) and navigation |
| `public_html/inc/pages.php` | Route table with each page's title, meta description, type and sitemap priority, plus the old→new redirect map |
| `public_html/inc/layout.php` | Page shell (head, header, footer), helpers (`hero`, `faq_section`, `cta_band`, `related`) and the JSON-LD builder |
| `public_html/inc/contact.php` | Contact-form handler: validates input, applies honeypot and timing spam checks, emails `contact@`, and saves a copy to `inc/data/leads.csv` |
| `public_html/inc/smtp.php` | Sends leads through the contact@ mailbox over authenticated SMTP (smtp.hostinger.com:465), falling back to `mail()`. Failures are logged to `inc/data/mail.log` |
| `public_html/inc/secrets.php` | **Server only, git-ignored.** The SMTP login: `<?php return ['host'=>'smtp.hostinger.com','port'=>465,'user'=>'contact@cowboytinyhomes.com','pass'=>'…'];` Recreate it on the server if the mailbox password changes |
| `public_html/pages/` | One template per page: services, areas, guides, tools, and core pages |
| `public_html/assets/` | `css/site.css`, `js/site.js` (nav, FAQ search, filters), `js/tools.js` (all calculators), and images |
| `validate.py` | Crawls a running copy and checks status codes, single H1, unique titles and descriptions, canonicals, JSON-LD, links, alt text, and the homepage brand count |
| `featured_images.py` | Generates the 1200×675 blog featured images from the site photos (needs Montserrat TTFs) |
| `deploy.py` | Uploads to Hostinger through the File Browser API; `launch` also moved WordPress into the backup folder |

## Local preview

```sh
cd public_html && php -S 127.0.0.1:8099 router-dev.php
python3 validate.py            # in another shell
```

## Adding a page

1. Add the route and its metadata to `PAGES` in `inc/pages.php`.
2. Create `pages/<file>.php`. It only needs to echo the content of `<main>`.
3. Run `validate.py`, then deploy. `sitemap.xml` updates automatically.

## Pages (38)

- **Home** — "tiny home builders texas" (also targets tiny house / small house builders texas, texas built tiny homes, custom tiny homes texas)
- **Services** — custom tiny homes, ADU builders, tiny homes on wheels, park model homes, design services, remodel design
- **Service areas** — San Antonio, Austin, Dallas, Fort Worth, Houston, plus a hub page
- **Guides** — Texas tiny house laws (with an interactive permit checklist), cost to build, ADU vs park model vs THOW, choosing a builder, financing
- **Tools** — cost calculator, "which tiny home" quiz, size planner, ADU rental income calculator, loan calculator
- **Blog** (`/blog/`, RSS at `/blog/feed.xml`) — five dated posts, each with a featured image: western tiny homes (2026-05-14), backyard casita ideas (2026-06-25), gooseneck vs bumper pull (2026-08-06), tiny home design for Texas heat (2026-09-17), tiny house communities in Texas (2026-10-22). To add a post, add a `'type' => 'post'` route with `published`, `category`, `read` and `image` set, then create a template using `post_hero()` and `post_sidebar()`. The blog index, homepage cards, RSS and sitemap all pick it up automatically.
- **Core** — house designs (filterable), Gonzales Modern Living, our process, FAQs (searchable), contact (Design/Build and Remodel forms), write for us, privacy

Old WordPress URLs (`/category/*`, Yoast sitemaps, `/feed/`, `/wp-admin` and others) 301 to their new equivalents. Old `/wp-content/uploads/...` image URLs 301 to the same image in `/assets/img/`.

## WordPress backup

The original WordPress files (core, Elementor and the other plugins, theme, uploads and `wp-config.php`; the old root `.htaccess` is saved there as `.htaccess.wordpress`) were moved, not deleted, into
`public_html/wordpress-backup-2026-10-28/` on 2026-10-28. That folder holds its own `Require all denied` `.htaccess`, and the main `.htaccess` also blocks it, so none of it is web-accessible. The WordPress database was left untouched; its credentials are in the backed-up `wp-config.php`.

To roll back, move the contents of that folder back into `public_html/`, replacing `index.php`, and rename `.htaccess.wordpress` to `.htaccess`. You can do this in hPanel File Manager. Then delete the new site's files.

## Deploying updates

Get fresh credentials from the Hostinger API `hosting_files_generate-upload-url` (username `u401386392`, domain `cowboytinyhomes.com`), export `FB_URL`, `FB_AUTH` and `FB_REST`, and run `python3 deploy.py upload`. Bump `ASSET_VER` in `inc/config.php` when CSS or JS changes.
