# WordPress backup — enforceinterest.com — taken 2026-11-03

Backup of the WordPress/Elementor site (Hostinger Agency website UID `UXdKlalnO`, WordPress 6.9.4,
Hello Elementor theme, Yoast SEO, LiteSpeed Cache, Elementor Pro forms) taken before it was replaced by
the custom HTML/PHP build in `../../`.

In git (this folder):
- `pages/` — rendered HTML of every URL in the Yoast sitemaps (13 pages + 2 posts + blog index) and the
  sitemaps / robots.txt themselves.
- `api/` — WordPress REST exports: `pages.json`, `posts.json` (full `content.rendered`), `media.json`,
  `categories.json`, `tags.json`, `types.json`.
- `media/` — the whole media library (6 images) at original size.
- `root-files/` — `.htaccess`, `robots.txt`, `llms.txt` and the Search Console verification file
  `google9d8d740410b54935.html` (carried over to the new site).

Not in git (they contain personal data) — stored on the new Hostinger website, outside the web root, in
its `.h5g/` folder (website UID `1WCLLtRIk`):
- `enforceinterest-wordpress-db-2026-11-03.sql.gz` — full MySQL dump of `u914589053_UXdKlalnO_zk7WWM8Rn7e9`
  (25 tables, all rows; `DROP TABLE IF EXISTS` + `CREATE TABLE` + `INSERT`). SHA-256
  `28962f553fab839b6d091bb87e49736afa6776f353eac24d4333465f64349ad9`.
- `enforceinterest-wordpress-files-2026-11-03.zip` — complete `public_html/` (6,580 files, 33.7 MB:
  core, themes, plugins, `wp-config.php`, uploads). SHA-256
  `8657fcce9825379543148e6304dafcbbfabf15915d7cb263d168ce113523bcf4`.
- `enforceinterest-form-submissions-2026-11-03.csv` — the 50 Elementor form submissions
  (`wp_e_submissions*` tables) exported to CSV, May 1 – Nov 2, 2026.

The WordPress website `UXdKlalnO` and its database were deleted on 2026-11-03 after the domain moved,
so this folder plus the three files above are now the only copies.

The dump and zip were produced by a one-off, token-protected PHP script that was deleted from the server
immediately afterwards (verified 404).

## Restoring WordPress
1. Create a WordPress website on the Agency plan (`agency-hosting_website-setups_create` with a `wp-*` flavor).
2. Extract the zip so its `public_html/` replaces the new document root; update `wp-config.php` with the new
   database credentials.
3. Import the SQL dump (`zcat file.sql.gz | mysql <db>` or phpMyAdmin), then point the domain at it.
