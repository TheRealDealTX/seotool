# my1secret.com — custom PHP blog + community forum

Replaces the old WordPress site with a hand-written PHP 8 / MySQL application:
an editorial **blog** (34 migrated guides) plus a **Reddit-style community forum**
(communities, posts, threaded comments, up/down votes, karma, moderation).
No framework, no Composer, no WordPress.

## Hosting

| | |
| --- | --- |
| Host | Hostinger Agency Growth, order `1008744732`, Phoenix (`us-phx-h5g-node3`) |
| Website | UID **`BdYjkjNdE`**, plain `php-fpm`, PHP 8.3, domain `my1secret.com` |
| Database | `u914589053_BdYjkjNdE_m1sforum`, user `u914589053_BdYjkjNdE_m1sapp` (localhost) |
| Config | `.h5g/my1secret-config.php` on the website storage, **outside** `public_html`; never in git. Keys in `config.sample.php` |
| Old WordPress site | UID `gQNgYkvrL` — domain moved and site **deleted** on 2026-11-19 (backup in `backup/` and `.h5g/`) |

Platform behaviour that shaped the code (tested, not assumed):

- nginx serves existing files directly and routes unknown *page* paths (and `.xml`) to
  `index.php`; it ignores `.htaccess`. Missing `.txt`, `.php` and image paths get the
  platform's own 404 and never reach PHP — hence the static `robots.txt`, and old
  `/wp-content/uploads/…` image URLs simply 404.
- `pdo_sqlite` is not installed on the server; MySQL only. `mail()` works.
- PHP can write inside `public_html` (used for `/uploads/`) but not its parent.
- Hostinger's CDN (hcdn) sits in front. HTML is sent `Cache-Control: public, max-age=0,
  must-revalidate` for anonymous pages and `private, no-store` for anything per-user
  (logged in, CSRF token, flash message), so the CDN never caches a personalised page.
- DB names/users get the `u914589053_<websiteUID>_` prefix even though the API
  reports the short name.

## Layout

```
public_html/
  index.php                 front controller (all routes)
  robots.txt                static (see above)
  assets/css/app.css        single stylesheet, light + dark
  assets/js/app.js          progressive enhancement only (votes, replies, menus)
  assets/img/               logo, icons, default OG image
  media/blog/               61 article images, resized to WebP by the migration
  uploads/                  user images (runtime; re-encoded to WebP; gitignored)
  app/
    bootstrap.php           config lookup, error handling
    routes.php              route table, canonical host, legacy WordPress 301/410
    schema.php              tables + first-run seed (articles, topics, communities, welcome posts)
    lib/                    db, helpers, DB sessions, auth, safe markdown, SEO/JSON-LD, content/votes
    controllers/            blog, forum, account, site (search/sitemap/feed/install), admin
    views/                  PHP templates
    seed/articles.php       generated: 34 articles + 5 topics
    seed/legacy.php         generated: old URL -> new URL map, 410 list
tools/
  migrate_wp.py             WordPress export -> seed files + WebP images
  install.php               CLI installer (local)
  dev-router.php            php -S router (local)
  smoke_test.py             end-to-end test: register, post, comment, reply, vote, report, moderate
  guest_test.py             guest flow: post with name+email, confirmation email, publish, trusted reposting
  import_articles.py        new article JSON -> seed files, product seed, title-card images
  seo_audit.py              titles, descriptions, H1, canonical, JSON-LD, internal links for every sitemap URL
backup/wordpress-2026-11-19 WordPress backup (see its README)
deploy.sh                   upload public_html via the File Browser TUS API
```

All files under `app/` start with `defined('M1S') || exit;`, so requesting them
directly returns nothing.

## Features

**Blog** — 50 articles: 34 migrated from WordPress plus 16 new guides added
2026-11-19 (security deposits, lease questions, move-out cleaning, soundproofing,
renter-friendly upgrades, kitchen/closet organization, low-light plants, renters
insurance coverage, home inventory, water and hail damage claims, Texas hurricane
prep, lowering summer electric bills, indoor air quality, cleaning schedule).
Featured images are real photos, CC0/public domain where possible, otherwise
CC BY / BY-SA; each is credited under the image with a link to its source
(`image_credit`, `image_credit_url`; also editable in admin). Photo choices and
credits are in `content/articles-2026-11/_images.json`. Their source is `content/articles-2026-11/*.json`; `tools/import_articles.py`
validates them (internal links, markup, lengths), generates the title-card images
and writes `app/seed/articles-2026-11.php` + `app/seed/products.php`, which the
installer imports (existing slugs are skipped). `/blog/`, `/blog/<slug>/`, `/blog/topic/<topic>/`, `/author/<name>/`.
Table of contents from H2s, related guides, "was this helpful" votes, threaded
comments on every article, a link into the matching forum community, RSS at `/feed/`.
Admins write and edit articles (HTML body, SEO title, meta description, slug,
topic, image, draft/publish date) at `/admin/articles/`.

**Forum** — `/forum/`, `/forum/<community>/`, `/forum/<community>/<id>-<slug>/`.
Six communities: Renting, Small-Space Living, Insurance Claims, Texas Living,
Lifestyle, One Secret (each opens with a pinned welcome post). Hot / New / Top
(day…all) / Most discussed sorting with Reddit's hot formula; text, link and
image posts; Markdown (escaped first, so no user HTML ever renders); nested
replies; up/down votes on posts and comments; karma; user profiles `/u/<name>/`;
edit/delete own content; search.

**Guest contributions** — anyone can post or comment with just a name and an
email (no account). The email must be well-formed with a domain that accepts
mail; disposable domains are refused. A guest's first contribution is held and a
one-click confirmation link is emailed from support@my1secret.com; confirming
publishes it (and any other pending posts from that address) and sets a signed
cookie so that browser's later posts publish instantly. Unconfirmed posts are
deleted after 7 days. Guests are shown as "Name · guest", their email is never
displayed, they get one link per post, they're rate limited per IP and per email,
and they can't vote or report (that needs an account). Guest POSTs use a
stateless same-origin check instead of a session, so anonymous visitors and
crawlers never create session rows. Admins can ban a guest email (removing all
its posts) under `/admin/users/`. Code: `app/lib/guest.php`.

**Email** — transactional mail (password resets, guest confirmations) is sent
over authenticated SMTP (`smtp.hostinger.com:465`) as support@my1secret.com;
credentials live only in the server config (`smtp` key). `app/lib/mailer.php`.

**Amazon affiliate products** — `products` table, managed at `/admin/products/`.
Every link gets the Associates tag `josephrayditt-20` (config `amazon_tag`)
re-applied at render time and is `rel="sponsored nofollow"`. A product links to an
Amazon search for its terms by default, or to a specific product URL/ASIN an
admin pastes. Tags place it: `article:<slug>` (that article's "Helpful finds"
box), `topic:<slug>` (every article in the topic after its own picks, and the
`/shop/` page). The Amazon Associates disclosure appears in every product box,
on `/shop/`, in the footer and in the privacy policy. 121 picks seeded.

**Accounts** — register (honeypot + signed timing field), login (rate limited
per IP and per username), password reset by email (1-hour token), settings
(profile, email, password; changing the password signs out other devices).
Sessions are stored in MySQL, not the shared `/tmp`.

**Moderation** — roles `member` / `mod` / `admin`. Report button on every post
and comment → `/admin/reports/`. Mods remove/restore, pin, lock; admins also
manage roles, bans (optionally removing all of a user's content), communities,
topics and articles. New accounts (< 48 h and < 5 karma) are limited to one link
per post/comment and lower posting rates. All links in user content are
`rel="nofollow ugc"`.

**Security** — CSRF token on every POST, prepared statements everywhere, output
escaping, CSP (`script-src 'self'`), HSTS, `X-Frame-Options`, uploads validated
and re-encoded through GD (strips metadata and any non-image payload).

## SEO

- **New URL scheme**: `/discussion/<long-wp-slug>/` → `/blog/<short-keyword-slug>/`,
  each with a rewritten `<title>` (≤ 70 chars) and a hand-written meta description
  (≤ 160 chars). Full mapping in `tools/migrate_wp.py` (`POSTS`).
- **301s** for every old URL: posts, `?p=ID`, bare slugs, `/feed/`/`/amp/` variants,
  category (`/topics/…`) and tag (`/categories/…`) archives → matching topic,
  author archive, `/page/N/`, all Yoast sitemaps → `/sitemap.xml`.
- **410 Gone** for the 20 removed posts (the 2014 and 2023-09-18 spun articles:
  "how to find facebook password", gambling, title loans, "lose weight fast",
  cosmetic surgery, etc.) and for `/wp-admin/`, `/wp-json/`.
- Structured data: `Organization` + `WebSite` (with SearchAction) on the homepage,
  `BlogPosting` with author, dates, image and nested `Comment`s on articles,
  `DiscussionForumPosting` with interaction counts and nested comments on forum
  threads, `BreadcrumbList` everywhere, `CollectionPage`/`ItemList` on lists,
  `ProfilePage` on author/user pages.
- Thin-content guards: forum threads are `noindex` until they have a reply or a
  ≥ 280-character body; user profiles until they have 5+ contributions; sort
  variants, page 2+ of forum lists, search, login and admin are `noindex`.
  `/sitemap.xml` (dynamic) lists only indexable URLs, with image entries for articles.
- `www` and `http` 301 to `https://my1secret.com`; trailing slashes enforced.

`tools/seo_audit.py https://my1secret.com` re-checks all of this; it reported
0 problems across 60 URLs and 69 internal links at launch.

## Local development

```sh
cat > /tmp/m1s.php <<'EOF'
<?php return ['base_url' => 'http://127.0.0.1:8080', 'db' => ['dsn' => 'sqlite:/tmp/m1s.sqlite'],
  'secret' => 'dev', 'mail_log' => '/tmp/m1s-mail.log', 'enforce_host' => false, 'debug' => true];
EOF
M1S_CONFIG=/tmp/m1s.php php tools/install.php                      # prints the admin password
M1S_CONFIG=/tmp/m1s.php php -S 127.0.0.1:8080 -t public_html tools/dev-router.php
python3 tools/smoke_test.py http://127.0.0.1:8080 my1secret '<admin password>'
python3 tools/seo_audit.py http://127.0.0.1:8080
```

Re-run `python3 tools/migrate_wp.py` only if you change the article mapping; the
installer imports articles once (it skips slugs that already exist).

## Deploying

```sh
# credentials from Hostinger API agency-hosting_files_generate-upload-url (website BdYjkjNdE)
export FB_URL=… FB_AUTH=… FB_REST=…
./deploy.sh                 # everything in public_html (except uploads/)
./deploy.sh app assets      # just these folders
```

Then clear the cache (`agency-hosting_cache_clear-website`, website `BdYjkjNdE`).
Schema changes: add them to `schema.php` (it is idempotent) and run `/install/` by
temporarily setting `install_token` in the server config, then blank it again.

## Admin access

The installer created the admin account **`my1secret`** with a random password
(given to the site owner separately; change it under Settings, and set an email
there so password reset works). The blog author account **`meagan`** has a random
unusable password; an admin can promote/demote roles at `/admin/users/`.
