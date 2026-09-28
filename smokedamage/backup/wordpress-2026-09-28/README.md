# WordPress backup — smokedamage.com — taken 2026-09-28

Content-level snapshot of the WordPress site (Hostinger Agency website UID
`1Sz13eGkC`, WordPress 7.0.3) taken before smokedamage.com was moved to the
static rebuild.

- `pages/` — rendered HTML of every URL in the Rank Math sitemap (/, /terms-of-use/, /privacy-policy/) plus the sitemap.
- `api/` — WordPress REST exports: `pages.json` (3 pages with full content), `media.json` (8 attachments), `posts.json` (empty — no posts).
- `media/` — every media-library file at original size.

The WordPress website itself (files and database) was **not deleted**. It was left
in place on the Agency plan with its temporary domain
(palegoldenrod-snail-811280.hostingersite.com), so it can be restored by moving
smokedamage.com back to website `1Sz13eGkC`. Delete it from hPanel only once
you're satisfied with the new site.
