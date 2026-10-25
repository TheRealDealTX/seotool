# coveragestimate.com — static rebuild (replaces WordPress)

An exact static copy of the WordPress/Elementor site, served as plain files with a
small PHP layer. Every URL, title, meta tag, canonical, schema block, image path and
script is identical to the WordPress output, so nothing changes for visitors or Google.

| Path | What it is |
| --- | --- |
| `public_html/` | The deployable site (upload this folder's contents to the host's `public_html`) |
| `server/` | Hand-written server layer copied into `public_html/` by the build: `.htaccess`, form handler, router |
| `server/wp-admin/admin-ajax.php` | Replaces WordPress for Elementor form posts; sends mail over SMTP and logs submissions |
| `server/ce-private/` | Form config, ID map for legacy `?p=` links, SMTP client. Blocked from the web |
| `tools/mirror.py` | Downloads every page and every asset from the live WordPress site |
| `tools/build_static.py` | Turns the download into `public_html/` (root-relative links, keeps SEO URLs absolute) |
| `tests/` | Visual comparison (live vs new), form tests, local PHP router |

## Rebuild from the live WordPress site

```sh
cd tools
python3 mirror.py ../out extra.txt        # extra.txt = netcap.txt + chunks.txt
python3 build_static.py ../out
rsync -a --delete ../out/public_html/ ../public_html/   # keep ce-private/mail-config.php out of git
```

`netcap.txt` lists files the browser requests at runtime (recorded with `tests/netcap.js`);
`chunks.txt` lists every Elementor webpack chunk so lazily loaded scripts are present.

## Server behavior (`server/.htaccess`)

- HTTPS and non-www, like WordPress.
- Trailing-slash redirects (`/about-us` → `/about-us/`).
- Legacy WordPress links: `/?p=117`, `/?page_id=14`, `/?cat=7` → 301 to the real URL; `/?s=` → `/blog/`.
- `/home/`, `/author/*` → `/`; `/sitemap.xml`, `/wp-sitemap.xml` → `/sitemap_index.xml`.
- `/feed/`, `/comments/feed/`, `/category/tools/feed/` served from static RSS files.
- `wp-login.php`, `xmlrpc.php`, `wp-json`, `wp-admin/*` (except `admin-ajax.php`) → 404.
- Any host other than `coveragestimate.com` gets `X-Robots-Tag: noindex, nofollow` (staging safety).

## Forms

The homepage form, Contact form and the blog-post "Fillup Form" popup still use Elementor's
own front-end script. It posts to `/wp-admin/admin-ajax.php`, which is now the PHP handler:
same validation, same success/error messages, same email (subject, recipients, Reply-To,
field list, date/time/page URL), plus the popup "close" action. Mail is sent through
`smtp.hostinger.com:465` as `appraisals@coveragestimate.com`.

The SMTP password lives only on the server in `public_html/ce-private/mail-config.php`
(see `mail-config.example.php`). Submissions are also appended to `ce-private/submissions.log`.

## Cutover checklist (temporary domain → coveragestimate.com)

1. Re-run the mirror right before cutover so any WordPress changes (including scheduled
   posts that have published) are included, then rebuild and redeploy.
2. Point coveragestimate.com at the new site (Hostinger: connect the domain to the website).
3. Confirm HTTPS, then spot-check pages, forms, redirects, sitemaps and the noindex header is gone.
4. Resubmit `sitemap_index.xml` in Google Search Console and monitor indexing for 2–4 weeks.
5. Keep the WordPress site and a full backup available until everything is confirmed.

Scheduled posts (Nov 14, Dec 5, Dec 26, Jan 16, Feb 6) publish on WordPress until cutover;
after cutover they must be added to the static site on their dates.
