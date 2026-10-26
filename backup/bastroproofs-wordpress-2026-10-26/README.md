# WordPress backup: bastroproofs.com, taken 2026-10-26

This is a content-level backup of the WordPress site (Hostinger Agency website
UID `uXznqPatC`). It was taken before bastroproofs.com moved to the custom PHP
site (UID `wIZQiliPf`, source in `/bastroproofs`).

What is here:
- `pages/`: the rendered HTML of every URL in the WordPress sitemap (/,
  /terms-of-use/, /privacy-policy/, /sitemap/), both Rank Math sitemaps, and
  the combined LiteSpeed CSS bundle.
- `api/`: WordPress REST API exports. `pages.json` holds all 4 pages with full
  content, and `media.json` holds the 15 media-library items. `posts.json` and
  `tags.json` are empty because the site had none. There are also
  `categories.json` and `types.json`, plus `pages-content.md` for reading.
- `media/`: the media library at original size. That is 14 files for 15
  library items, because two items share one filename.

This backup does **not** include a database dump or a zip of the full
`public_html/`. Neither is needed yet, because the WordPress website itself was
**kept**. Its domain was unlinked, but its files and database are untouched on
Hostinger. Take a database export and a files zip from hPanel (or with
phpMyAdmin) before that website is ever deleted.

## Rolling back

Point bastroproofs.com at `uXznqPatC` again:

1. Change the domain on `wIZQiliPf` to a temporary domain.
2. Link bastroproofs.com to `uXznqPatC`.
3. Clear the cache.
