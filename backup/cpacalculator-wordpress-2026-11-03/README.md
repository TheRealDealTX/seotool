# WordPress backup — cpacalculator.com — taken 2026-11-03

Backup of the WordPress site (Hostinger Agency website UID `6EmAVU1aW`, WP 6.9.4,
Yoast SEO) taken before it was replaced by the custom PHP site in `/cpacalculator`.

- `urls.txt` — every URL in the Yoast sitemaps (15). All of them still resolve on the new site.
- `pages/` — rendered HTML of every sitemap URL.
- `api/` — WordPress REST exports: pages, posts (full `content.rendered`), categories, media.
- `database/…sql.gz` — full MySQL export of `u914589053_6EmAVU1aW_dL1wJpTpUHwl` (26 tables,
  `DROP TABLE IF EXISTS` + `CREATE TABLE` + `INSERT`). Restore with `zcat file.sql.gz | mysql <db>`.
- `gsc-performance-2026-11-03.xlsx` — the Search Console report used to plan the rebuild.
- Media library: all 42 files (every size) are kept in the new site at `cpacalculator/wp-content/uploads/`,
  so old image URLs keep returning 200.

## Full files backup (not in git, 34 MB)

`cpacalculator-wordpress-files-2026-11-03.zip` — 6,685 files: the complete `public_html/`
(core, themes, plugins, `wp-config.php`, uploads). SHA-256 alongside. The platform does not allow
folders outside `public_html/`, so it is stored on the new website (Agency UID `17XGw98Uo`) as
`public_html/app/private/wpbackup-8cfe8e5c75459955.zip.php`: the zip with a 55-byte PHP guard
(`<?php http_response_code(404); exit; __halt_compiler();`) prepended, so a web request returns 404
and never the contents. To restore: download it via hPanel's file manager and strip the first 55 bytes
(`tail -c +56 file.zip.php > files.zip`).

## Restoring WordPress

1. Create a WordPress website on the Agency plan.
2. Extract the zip over its `public_html/`, set `wp-config.php` to the new database credentials.
3. Import the SQL dump, then move cpacalculator.com to it and clear the cache.
