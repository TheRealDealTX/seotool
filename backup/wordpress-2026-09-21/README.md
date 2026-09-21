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

What is NOT here: a MySQL dump or the raw wp-content directory. The Hostinger
API exposes neither for Agency (H5G) websites, and SSH/SFTP was disabled on the
account. The database `3t5IOGo8gom2` is not touched by a static-file
deployment and remains restorable from Hostinger's automatic backups in hPanel.
