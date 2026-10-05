# WordPress backup — beltonbanners.com — taken 2026-10-05

Content-level backup of the WordPress/Elementor site (Hostinger Agency website
UID `yC3Lm7xR9`) taken before beltonbanners.com was moved to the custom
HTML/PHP rebuild.

What is here:

- `pages/` — the rendered HTML of every URL in the Yoast sitemaps: the
  homepage, the 5 pages, the blog index and post, the category archive and all
  17 `creation/` entries; plus the four Yoast sitemaps and the sitemap index.
- `api/` — WordPress REST API exports: `full_pages.json`, `full_posts.json`
  and `full_creation.json` (complete, with `content.rendered`), and the slimmer
  `rest_*.json` listings including `rest_media.json` (all 27 attachments with
  source URLs).
- Media: every attachment in the library, downloaded at original size, lives at
  its original path under `../../wp-content/uploads/2026/03/` so the old
  image URLs keep working on the new site.

The WordPress website itself was **not** deleted. It still exists with all
its files and database on `lavenderblush-fly-932440.hostingersite.com`
(website UID `yC3Lm7xR9`), so it is the complete rollback: link
`beltonbanners.com` back to it (`agency-hosting_domains_change-website`) and
the old site is live again. Delete it from hPanel once the new site has been
running for a while.
