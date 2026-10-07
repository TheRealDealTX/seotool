# WordPress backup — cebudavao.com — taken 2026-10-07

Backup of the WordPress + Elementor site ("Cebu-Davao Travels – Texan Wanderlust
in the Philippines", Hostinger Agency website UID `IqzyizTeQ`) taken before
cebudavao.com moved to the new static/PHP build.

## What is here

- `api/` — WordPress REST exports: `posts.json` (all 51 posts with full
  `content.rendered`), `pages.json` (6 pages), `media.json` (95 attachments),
  `categories.json`, `tags.json`, `users.json`. The 51 posts are re-published
  from this export by `build.py` at their original URLs.
- `database/cebudavao-wordpress-db-2026-10-07.sql.gz` — full MySQL dump of
  `u914589053_IqzyizTeQ_9FhHheeLLnI0` (18 tables, every row; DROP/CREATE/INSERT;
  restore with `zcat … | mysql <db>` or phpMyAdmin). Taken with a one-off
  token-protected PHP script that was deleted from the server straight away.
  SHA-256 alongside.
- The media library itself is in `../../wp-content/uploads/` (every attachment
  plus every size used inside posts) and is served at the same URLs as before.

## Full files backup (too large for git)

`cebudavao-wordpress-files-2026-10-07.zip` — 163,828,142 bytes, 7,062 files: the
complete `public_html/` of the WordPress install (core, themes, plugins,
`wp-config.php`, uploads). SHA-256 in
`cebudavao-wordpress-files-2026-10-07.zip.sha256`.

Stored on the new website (UID `gLBQLhLT2`) at
`.h5g/cebudavao-wordpress-files-2026-10-07.zip`, outside the web root. Get it
from hPanel's file manager or the File Browser API behind
`agency-hosting_files_generate-upload-url`.

## The WordPress website still exists

The WordPress website `IqzyizTeQ` was **not deleted** — only the cebudavao.com
domain was moved off it. It still has its files and database. To roll back,
move the domain back to it (`agency-hosting_domains_change-website`) and clear
the cache. Delete it only once you're happy with the new site.
