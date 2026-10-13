# WordPress — sugarlandpublicadjuster.com (removed 2026-10-13)

The custom PHP site went live on 2026-10-13 and WordPress was then deleted:

- **Files removed:** `wp-admin/`, `wp-includes/`, every root `wp-*.php` file,
  `xmlrpc.php`, and `wp-content/` plugins, themes, caches and upgrade folders.
- **Kept:** `wp-content/uploads/2026/` (the media library), so every old image URL
  still resolves. A full copy is in this repo under `public_html/wp-content/uploads/`.
- **Database removed:** `u401386392_h7RiH` (the only database assigned to this
  domain). The other databases on account `u401386392` belong to other sites and
  were not touched.
- `index.php.txt` and `htaccess.txt` here are the WordPress originals, kept for reference.

Before deletion the site's content was verified against the Yoast sitemaps:
6 pages (home, about-us, contact, privacy-policy, services, terms-of-use), the
`/blog/` posts page, 3 posts and 1 category (`general`) — all rebuilt at the same
URLs. The Yoast redirects file was empty, and the media library had no uploads
after March 2026.

Restoring WordPress now requires a Hostinger backup (hPanel → Files → Backups;
Cloud plans keep daily backups) for both files and the database.
