# WordPress backup — my1secret.com — taken 2026-11-19

Taken before the WordPress site (Hostinger Agency website UID `gQNgYkvrL`,
WordPress 6.9.4, Yoast SEO) was replaced by the custom PHP site.

- `api/` — WordPress REST exports: `posts.json` (all 54 posts with full
  `content.rendered` and embedded media/terms), `media-1.json` (62 attachments),
  `categories.json`, `tags.json`, `users.json`, `comments.json` (the only comment
  was a vulnerability-scanner probe), `pages.json` (none), `types.json`.
- `pages/` — rendered HTML of every URL in the Yoast sitemaps (65 URLs) plus the
  sitemaps themselves and `urls.txt`.
- `media/` — every media-library file at original size.
- `database/my1secret-wordpress-db-2026-11-19.sql.gz` — full MySQL export
  (24 tables, 2,317 rows, `DROP TABLE IF EXISTS` + `CREATE TABLE` + `INSERT`).
  Restore with `zcat … | mysql <db>` or phpMyAdmin. SHA-256 alongside.
  Contains the WordPress user table (password hashes and the author's email) —
  keep this repository private.

## Full files backup (too large for git)

`my1secret-wordpress-files-2026-11-19.zip` — 52,148,795 bytes, 5,985 files: the
complete `public_html/` (core, themes, plugins, `wp-config.php`, uploads).
SHA-256 in `my1secret-wordpress-files-2026-11-19.zip.sha256`.

A copy is stored outside the web root in the `.h5g/` folder of the new site
`BdYjkjNdE` (the DB dump is there too). The copy that was on the old WordPress
site was deleted with it. Retrieve with hPanel's file manager or the File Browser API behind
`agency-hosting_files_generate-upload-url`.

Both were taken with a one-off token-protected PHP script that was deleted from
the server immediately afterwards.

## State of the old site

On 2026-11-19 my1secret.com was unlinked from the WordPress website `gQNgYkvrL`
and attached to the new site `BdYjkjNdE`. After the new site was verified live
(homepage served fresh after a CDN flush, 0 SEO-audit problems across 71 URLs,
legacy redirects working), **`gQNgYkvrL` was deleted** at the owner's request.
This directory plus the zip and dump on `BdYjkjNdE/.h5g/` are now the only copies.

## Restoring WordPress elsewhere

1. Create a WordPress website on the Agency plan.
2. Extract the zip so its `public_html/` replaces the new document root, then put
   the new database credentials in `wp-config.php`.
3. Import the SQL dump into that database.
4. Point the domain at it and clear the cache.
