# WordPress backup — solarcctvcamera.com — taken 2026-11-03

Taken before the WordPress website (Hostinger Agency UID `f5Tzp57oS`, WordPress 6.9.4 +
Elementor + Yoast) was replaced by the PHP rebuild and deleted.

In this repo (content only, safe to publish):
- `pages/` — rendered HTML of all 46 sitemap URLs, the Yoast sitemaps, `llms.txt`, `robots.txt`.
- `api/` — WordPress REST exports: `posts.json` (20 posts), `pages.json` (9), `media.json`,
  `categories.json`, `tags.json`; `pages-content.md` is a plain-text version for reading.
- `SHA256SUMS` — checksums of the two private archives below.

Not in git (the repository is public), stored on the new website’s private storage outside the
document root, folder `.h5g/wordpress-backup/` on website `IhhWxQZAx`:
- `solarcctvcamera-wordpress-files-2026-11-03.zip` — 68,452,234 bytes, 9,272 files: the complete
  `public_html` (core, themes, plugins, `wp-config.php`, all uploads).
- `solarcctvcamera-wordpress-db-2026-11-03.sql.gz` — full MySQL dump of
  `u914589053_f5Tzp57oS_oKP4AmJSqTds` (24 tables, 4,268 rows, DROP/CREATE/INSERT). Includes the 53
  Elementor form submissions (all spam) and user password hashes, hence not in git.

Retrieve them in hPanel → File Manager for that website, or via the File Browser API behind
`agency-hosting_files_generate-upload-url` (`GET {url without /tus}/raw/.h5g/wordpress-backup/<file>`).

## Restoring WordPress
1. Create a WordPress website on the Agency plan (`agency-hosting_website-setups_create` with a `wp-*` flavor).
2. Extract the zip so its `public_html/` replaces the new site’s document root; update `wp-config.php`
   with the new database credentials.
3. Import the SQL dump (`zcat file.sql.gz | mysql <db>` or phpMyAdmin).
4. Point solarcctvcamera.com at it and clear the cache.
