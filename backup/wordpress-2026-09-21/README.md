# WordPress backup — huttoroofs.com — taken 2026-09-21

Content-level backup of the WordPress site (Hostinger Agency, website UID
Kq0nqTlGe) taken before it was replaced by the static build.

What is here:
- `pages/` — the rendered HTML of every URL in the WordPress sitemap
  (/, /terms-of-use/, /privacy-policy/, /sitemap/), both Rank Math sitemaps,
  and the combined LiteSpeed CSS bundle.
- `api/` — WordPress REST API exports: `pages.json` (all 4 pages with full
  `content.rendered`), `media.json` (all 11 attachments with metadata),
  `posts.json` (empty — the site had no posts), `categories.json`, `tags.json`,
  `types.json`; plus `pages-content.md` for reading.
- `media/` — every attachment in the media library, downloaded at original size.

- `database/huttoroofs-wordpress-db-2026-09-21.sql.gz` — full MySQL export of
  database `u914589053_Kq0nqTlGe_3t5IOGo8gom2` (27 tables, all rows, with
  `DROP TABLE IF EXISTS` + `CREATE TABLE` + `INSERT` statements; restores with
  `zcat file.sql.gz | mysql <db>` or a phpMyAdmin import). Taken with a
  one-off token-protected PHP script that was deleted from the server
  immediately afterwards. SHA-256 alongside.

## Full files backup (too large for git)

`huttoroofs-wordpress-files-2026-09-21.zip` — 340,271,692 bytes, 15,638
files: the complete `public_html/` of the WordPress install (core, themes,
plugins, `wp-config.php`, all uploads). SHA-256 in
`huttoroofs-wordpress-files-2026-09-21.zip.sha256`.

Stored on the Hostinger website's own file storage, outside the document
root, at `.h5g/huttoroofs-wordpress-files-2026-09-21.zip` (website UID
Kq0nqTlGe). Retrieve it through hPanel's file manager, or with the File
Browser API behind `agency-hosting_generateUploadURLV1`. Hostinger's own
automatic backups for the Agency plan remain available in hPanel as well.

## Restoring WordPress

1. hPanel → the website → File manager: extract the zip so its
   `public_html/` replaces the current document root.
2. Import `database/…sql.gz` into the same database (its credentials are in
   the restored `wp-config.php`).
3. Clear the site cache.
