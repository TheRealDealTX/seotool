# houstonpublicadjusting.com — custom PHP rebuild ("Houston Public Adjusters")

Replaces the WordPress/Elementor site with a hand-built PHP site. No database, no
plugins. Upload this folder's contents to `public_html/` on Hostinger.

## Every old URL is kept

| Old WordPress URL | Now |
| --- | --- |
| `/`, `/about-us/`, `/services/`, `/contact/`, `/blog/`, `/privacy-policy/`, `/terms-of-use/`, `/category/general/` | Rebuilt, same URL, content kept and expanded |
| 9 blog posts (`/fire-insurance-adjuster/` etc.) | Same URLs, full original text, now authored by Joseph Dittman |
| `/wp-content/uploads/2026/...` images | Same paths (downloaded from the live site) |
| `post-/page-/category-sitemap.xml`, `/feed/`, `/wp-admin`, `/author/...` | 301 redirects in `.htaccess` |

## New pages

- `/tools/` + 7 calculators: claim settlement, public adjuster fee, hurricane deductible, depreciation, Texas claim deadlines (Prompt Payment Act), ALE, contents inventory builder
- `/houston-weather/` — live tracker (National Weather Service API: conditions, alerts, 7-day forecast; KHGX radar; NHC tropical outlook; SPC outlook and storm reports). Homepage has a live mini widget; every page shows a red banner when a NWS watch/warning is active for Harris County.
- `/houston-storm-history/` — filterable timeline (Alicia → Beryl) + seasonal hazard table
- `/author/joseph-dittman/`, `/service-areas/`, `/faq/`, `/hurricane-preparedness-checklist/`, `/insurance-claim-glossary/`, `/thank-you/`

## Leads

- Popup opens 4 seconds after page load (once per browser session; not on Contact/Thank-you).
- Every form posts to `submit-lead.php`, which emails **jditt@risepublicadjusting.com** and also appends
  the lead to `leads/leads-YYYY-MM.jsonl` (web access blocked) as a backup.
- Spam protection: honeypot field, 3-second minimum fill time, 5 submissions/hour per IP.
- **Before launch:** lead emails are sent from the existing mailbox `info@houstonpublicadjusting.com`
  (`LEAD_FROM` in `inc/config.php`). For best deliverability fill in the `SMTP_*`
  constants (smtp.hostinger.com, port 465) — otherwise PHP `mail()` is used.

## Editing

- Business details, phone, email, author bio, nav, service areas: `inc/config.php`
- Layout/header/footer/schema/forms: `inc/layout.php`; blog template: `inc/post-template.php`
- Blog post list + metadata: `inc/posts.php`; post body: `<slug>/index.php`
- New post: copy any post folder, change the slug, add an entry at the top of `POSTS`, then run
  `php inc/build-sitemap.php` to refresh `sitemap.xml`.

## Deploying to Hostinger

1. Back up the WordPress site (hPanel → Files → Backups, or download `public_html` + the database).
2. Zip this folder's contents: `cd houstonpublicadjusting && zip -r ../site.zip . -x 'README.md'`
3. hPanel → File Manager → `public_html`: move the WordPress files to a backup folder, upload and
   extract `site.zip`. PHP 8.1+ required (8.2/8.3 recommended).
4. Create the noreply mailbox (above), submit a test lead, clear the Hostinger/LiteSpeed cache.
5. In Google Search Console, resubmit `https://houstonpublicadjusting.com/sitemap_index.xml`.

Local preview: `php -S 127.0.0.1:8000 -t houstonpublicadjusting`

## Live deployment

Live on Hostinger Cloud account `u401386392` (`public_html` of houstonpublicadjusting.com), deployed
2026-10-13 by uploading files through the hPanel file manager (TUS upload API), then clearing the cache.

WordPress was removed on 2026-10-13: core files, plugins, themes, `wp-config.php`, the WordPress
installation record and its database (`u401386392_gJKEC`). Kept on the server: `wp-content/uploads/2026/`
(all 248 original media files, so old image URLs still resolve; also committed here),
`google9d8d740410b54935.html` (Search Console verification) and `.private/` (Hostinger's own).
There is no WordPress rollback any more; Hostinger's automatic account backups are the only copy.

Leads are emailed from `info@houstonpublicadjusting.com` to `jditt@risepublicadjusting.com`.
