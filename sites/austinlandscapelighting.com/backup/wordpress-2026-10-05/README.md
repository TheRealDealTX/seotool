# WordPress backup — austinlandscapelighting.com — taken 2026-10-05

Content-level backup of the WordPress site (Hostinger Agency website UID
`1AbSzNVGl`, now on temporary domain `ghostwhite-flamingo-551464.hostingersite.com`) taken before
austinlandscapelighting.com was moved to the custom PHP site (UID `64Mujs88W`).

- `pages/` — rendered HTML of every URL in the Yoast sitemaps: home, service-areas,
  contact, about-us, privacy-policy, terms-of-service, sitemap, blog, the two posts
  and the two category archives.
- `api/` — WordPress REST exports: `pages.json` (8 pages, full `content.rendered`),
  `posts.json` (2 posts), `media.json` + `media-2.json` (145 attachments),
  `categories.json`, `tags.json`, `types.json`.
- `media-urls.txt` — the original URL of every attachment. The originals (65 MB)
  are not committed; resized copies live in `../../assets/img/`.

No database dump or full-files archive was taken from this session. The
WordPress website itself was **not deleted**: it still exists on its temporary
domain with its database, so a full backup can be taken from hPanel (Files →
Backups) at any time, and the domain can be re-linked to it to roll back.
