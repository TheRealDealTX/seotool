# thoughtchangerblog.com — custom PHP rebuild

Replaces the WordPress/Elementor install with a small, dependency-free PHP site.
Every URL the old site exposed (posts, pages, archives, sitemaps, feed, images, heading
anchors) keeps working. Upload the contents of `public/` to `public_html`.

## Layout

| Path | What it is |
| --- | --- |
| `public/index.php` | Front controller: routing, canonical host/HTTPS, legacy redirects, 404s |
| `public/.htaccess` | HTTPS/non-www redirects, sends non-file requests to `index.php`, blocks `app/` + `content/`, caching |
| `public/app/bootstrap.php` | Site constants (GA4 ID, Amazon tag, email), data helpers, config loader |
| `public/app/views/` | Templates: `home`, `post`, `archive`, `page`, `contact`, `bookshelf`, `search`, `404`, `feed`, `sitemap` |
| `public/app/pages/` | Body copy for About, Privacy, Terms, Affiliate Disclosure |
| `public/app/forms.php`, `mailer.php` | Contact + newsletter handling; SMTP client (no Composer) |
| `public/content/posts.json` | Metadata for all 74 posts (title, SEO title, description, dates, image, categories, products, FAQ) |
| `public/content/posts/<slug>.html` | Each post's body. `<!--tc:products-->` and `<!--tc:faq-->` mark where product cards and the FAQ render |
| `public/content/legacy-ids.json` | Old WordPress `?p=ID` → slug |
| `public/wp-content/uploads/` | The full WordPress media library at its **original paths** (863 files) |
| `public/assets/` | `site.css`, `site.js` |
| `tools/` | Import + QA scripts, rewrite briefs, Search Console/sitemap data used for QA |

## Content decisions (from GSC + GA4, May–Nov 2026)

* **41 posts kept verbatim.** Any post with ≥ 5 clicks, ≥ 3,000 impressions, ≥ 20 GA views,
  or a top-6 average position: title tag, H1, meta description, body text, heading IDs
  (`#h-…` anchors Google shows as sitelinks), dates and featured image are unchanged.
  `status: "kept"` in `posts.json`.
* **33 posts rewritten** (`status: "rewritten"`). Same URL and featured image, new
  1,500–2,100 word article aimed at one clear keyword, new title/description,
  FAQ and reading list. Briefs: `tools/rewrite-briefs.json`; metadata: `tools/rewrites/*.json`.
  `dateModified` is 2026-11-19.

## URL continuity

* Posts `/<slug>/`, pages, `/blog/` + `/blog/page/2/`, `/mindset/`, `/quotes/`,
  `/category/general/` — same URLs, same titles.
* `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml`
  keep Yoast's filenames, so the sitemap submitted in Search Console keeps working. `/feed/` is a live RSS feed.
* 301s: `?p=ID`, Blogger-era `/YYYY/MM/slug.html`, `/category/mindset|quotes/`,
  `/slug/feed|amp|embed/`, missing trailing slash, uppercase slugs, and misspelled slugs
  (fuzzy match, e.g. `/i-had-an-epiphany/`, `/11-signs-you-re-stuck-in-complacency/`).
* `/?s=` search still works (noindex). WordPress internals (`/wp-admin`, `/wp-login.php`, `xmlrpc.php`) return 404.
* Same GA4 property (`G-BJ6HPX7KCP`) on every page.

`python3 tools/validate.py` checks all of this against a running copy (local or live):
every old sitemap URL and every URL in the GSC export, all 216 GSC anchors on kept posts,
all 863 old image URLs, plus unique titles, one H1, valid JSON-LD, no broken internal links,
and the affiliate tag on every Amazon link.

## Amazon affiliate

Tag `thoughtchangerblog-20` (constant `AMAZON_TAG`). Every post has a 3-book
"Recommended Reading" block, a mid-article "Reader pick", and a sidebar shelf. The home
page has a bookshelf strip, and `/recommended-reads/` collects every recommendation. Links are
Amazon search links (`/s?k=Title+Author&tag=…`) marked `rel="sponsored nofollow"`. To
link a specific edition, add `"asin": "B0…"` to the product in `posts.json`. Covers are
drawn in CSS, because Amazon's terms only allow product images from their API/SiteStripe.
Affiliate clicks are sent to GA4 as `affiliate_click` events.

## Forms → info@thoughtchangerblog.com

The contact form and the newsletter signup email every submission to
info@thoughtchangerblog.com via authenticated SMTP (smtp.hostinger.com:465, SSL). Spam
protection: honeypot, signed timestamp, link limit, 6 submissions/hour per IP.

**The mailbox password is not in git.** Create `tc-config.php` one level **above**
`public_html` (e.g. `/home/<user>/domains/thoughtchangerblog.com/tc-config.php`):

```php
<?php
return ['smtp_pass' => 'THE-MAILBOX-PASSWORD'];
```

(`public/app/config.local.php` also works and is git-ignored.) If sending ever fails, the
submission is appended to `tc-submissions.log` next to that file, so nothing is lost.

## Local preview

```bash
php -S localhost:8080 -t public tools/dev-router.php
```

```bash
python3 tools/validate.py http://localhost:8080
```

## Deploying (Hostinger Cloud Enterprise)

Hosting account `u401386392`, website `thoughtchangerblog.com`.

* **Password file:** `/home/u401386392/domains/thoughtchangerblog.com/tc-config.php`, which sits above
  `public_html`. Both staging and production read it (see `private_dir()`). It is already in place.
* **Staging (removed 2026-11-19; see below to re-create):** https://staging.thoughtchangerblog.com was served from `public_html/staging/`. It sent
  `noindex` headers, has a `Disallow: /` robots.txt, and returns 404 if requested through the main domain.
  Deployed 2026-11-19, `validate.py` passed with 0 errors, and a test contact message was delivered.
* **Upload:** `tools/deploy.sh staging|production` (TUS upload API; its header explains the credentials).

**Live since 2026-11-19.** How it went live:
1. The WordPress `index.php` and `.htaccess` were copied to `/home/u401386392/domains/thoughtchangerblog.com/wp-backup-20261119/public_html/`.
2. `SKIP_MEDIA=1 tools/deploy.sh production` uploaded the new site. `wp-content/uploads/` was left in place: it holds all 1,186 original media files, so every old image URL still works.
3. The rest of WordPress (core, `wp-config.php`, plugins, themes, LiteSpeed and upgrade folders) was moved into the same backup folder, outside the web root.
4. The server and CDN caches were cleared, and `validate.py` was run against the live domain.

Kept in `public_html`: both Google Search Console verification files (`google*.html`),
Hostinger's `.private/` and `wp-content/uploads/`. `llms.txt` is regenerated from `posts.json`.

**Rollback:** move everything in `wp-backup-20261119/public_html/` back into `public_html/` (overwriting
`index.php` and `.htaccess`), then clear the cache. The WordPress database was never touched.

The staging subdomain and `public_html/staging/` were removed on 2026-11-19. To preview a change later, re-create the
subdomain (`hosting_websites_add-domain`, name `staging`, directory `staging`) and run `tools/deploy.sh staging`.

**Later updates:** `SKIP_MEDIA=1 tools/deploy.sh production`, then clear the cache and run `validate.py` against the live site.

## Adding a post

Add the body as `public/content/posts/<slug>.html` (h2/h3 with `id="h-…"`, end with
`<!--tc:products-->`, `<h2 id="h-faqs">FAQs</h2>`, `<!--tc:faq-->`). Then add an entry to
`public/content/posts.json` (copy an existing one). Listings, sitemap, feed and related posts update automatically.
