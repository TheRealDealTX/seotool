# WordPress backup: underdeskelliptical.com, taken 2026-10-22

Taken before the WordPress site (Hostinger Agency website UID `wdHcdWujW`) is replaced
by the custom PHP build in `underdeskelliptical/`.

- `database/underdeskelliptical-wordpress-db-2026-10-22.sql.gz`: full MySQL export
  (25 tables, 4,636 rows, `DROP TABLE IF EXISTS` + `CREATE TABLE` + `INSERT`). Restore with
  `zcat file.sql.gz | mysql <db>` or a phpMyAdmin import. SHA-256 alongside.
- Full files backup (too large for git): `.h5g/underdeskelliptical-wordpress-files-2026-10-22.zip`
  on the website's own file storage, outside the document root. It is 87,006,262 bytes and
  holds all 7,378 files of `public_html/` (core, themes, plugins, `wp-config.php`, uploads).
  SHA-256 `4647af99dbfe9e0ef6cf807e8cc8af0bc9ebb82add028c4d6eb3ffa60ec4b241`, verified
  after download with `unzip -t`. A copy of the database export sits next to it in `.h5g/`.

Both were produced by a one-off token-protected PHP script that was deleted from the
server right after use.
