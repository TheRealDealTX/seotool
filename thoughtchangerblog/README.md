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

1. Back up the WordPress site (hPanel → Backups, or Files + DB export).
2. Move the WordPress files out of `public_html` (keep them for rollback).
3. Upload everything in `public/` into `public_html` (including `.htaccess`).
4. Create `tc-config.php` above `public_html` as shown above.
5. Clear LiteSpeed/CDN cache; run `python3 tools/validate.py https://thoughtchangerblog.com`.
6. In Search Console: resubmit `sitemap_index.xml`, and use URL Inspection on the top pages.

Rollback = put the WordPress files back; the database is untouched.

## Adding a post

Add the body as `public/content/posts/<slug>.html` (h2/h3 with `id="h-…"`, end with
`<!--tc:products-->`, `<h2 id="h-faqs">FAQs</h2>`, `<!--tc:faq-->`). Then add an entry to
`public/content/posts.json` (copy an existing one). Listings, sitemap, feed and related posts update automatically.
