# bettersidehustles.com — custom PHP rebuild

A custom HTML/PHP replacement for the WordPress/Elementor site, built for
Hostinger shared hosting (Apache/LiteSpeed + PHP 8.1+). It has no database, no
plugins and no build step: upload this folder's contents to `public_html/`.

## Structure

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: routing, legacy-URL redirects, sitemaps, feed |
| `.htaccess` | https + bare-domain redirect, sends non-file requests to `index.php`, blocks source folders |
| `inc/config.php` | Site name, nav, platforms, tools, **contact email**, Amazon tag |
| `inc/functions.php` | Rendering, shortcodes, Amazon links, schema, icons |
| `inc/tools.php` + `assets/js/tools.js` | The quiz and 7 calculators |
| `inc/templates/` | Layout and page templates |
| `content/posts/*.php` | One file per article: 75 posts, each at its original URL |
| `content/pages/*.php` | About, Privacy Policy, Affiliate Disclosure, Terms |
| `data/amazon.php` | Amazon gear catalog (tag `bettersidehustles-20`) |
| `data/tool-copy.php` | SEO copy for each `/tools/…/` page |
| `wp-content/uploads/` | Original images at their original URLs |
| `docs/content-format.md` | How to add or edit a post |
| `docs/legacy-urls.txt` | All 89 URLs from the old Yoast sitemaps |
| `validate.py` | Crawls a running copy and checks links, SEO tags and legacy URLs |

## URLs kept

Every URL in the old sitemaps still returns 200 with the same path. The
exceptions are `/write-for-us/` (removed as requested, 301 → `/contact/`)
and `/category/blog/` (301 → `/blog/`). Old WordPress paths also redirect:
author pages, date archives, `/feed/` (now a real RSS feed), `?s=` searches
and resized thumbnails (`image-300x200.webp` → the original image).
`sitemap_index.xml`, `post-sitemap.xml` and `page-sitemap.xml` keep their
Yoast names, so Search Console needs no change.

New pages: `/tools/` and 8 tool pages, `/side-hustle-gear/`, `/about/`,
`/affiliate-disclosure/`, `/terms-of-use/`.

## Content

- **Rewritten for the GSC queries** (17): Indianapolis, Sacramento, Santa Ana,
  Bossier City (indexed `#h-…` anchors kept), Hawaii, smartphone side hustles,
  digital marketing, Texas, the 2023 overview, and the Fiverr, Uber/Lyft,
  Thinkific, Skillshare, Udemy, Coursera, Shopify and Semrush guides.
- **Ported** (58 city guides): the original article copy, cleaned, with new
  2026 title tags, FAQ schema, a top-picks jump list, a sidebar calculator,
  Amazon gear and related-city links.
- Homepage mentions "Better Side Hustles" 20 times in visible text.

## Run locally

```sh
php -S 127.0.0.1:8099 index.php
python3 validate.py            # in another shell
```

## Deploy to Hostinger

1. Back up the current WordPress site (hPanel → Backups, or download
   `public_html` and export the database).
2. Edit `CONTACT_TO` in `inc/config.php` to a real mailbox on the domain.
3. In hPanel → File Manager, empty `public_html` (or move the WordPress files
   into a backup folder) and upload this folder's contents, including
   `.htaccess`. `README.md`, `validate.py` and `docs/` are optional; they're
   blocked from the web either way.
4. Purge the LiteSpeed/CDN cache, then open a few old URLs to confirm.
5. In Search Console, resubmit `sitemap_index.xml`.

## Before launch — please check

- Platform fees and rates (Udemy, Skillshare, Thinkific, Semrush, Fiverr,
  Shopify, IRS mileage) were checked in October 2026 but change often.
- A few local details in the rewritten city guides are flagged as unverified
  in the commit notes (for example Santa Ana ZIP boundaries).
