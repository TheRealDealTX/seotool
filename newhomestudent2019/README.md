# newhomestudent2019.com — custom PHP rebuild

Replaces the WordPress/Astra/Elementor site with a small hand-written PHP site:
no database, no plugins, no build step. Every URL the old site had still works.

## Hosting

| | |
| --- | --- |
| Hostinger Agency website UID | `orKz31Eb7` (php-fpm, PHP 8.3, Boston) |
| Live URL | https://newhomestudent2019.com (domain moved here 2026-11-19; the temporary utmost-olive-woodcock-71.hostingersite.com address was replaced) |
| Old WordPress website | `7XTGiOm4A` — domain unlinked 2026-11-19; files and database kept on the plan as a fallback |

The platform serves real files directly, **ignores `.htaccess`**, and sends every
other request to `index.php`. So all routing, redirects and 404s live in `index.php`,
and there must never be an `index.html` in the web root.

### Deploying

```sh
php validate.php          # must report 0 errors
export NH_FB_URL=… NH_FB_AUTH=… NH_FB_REST=…   # from agency-hosting_files_generate-upload-url (website orKz31Eb7)
./deploy.sh
```

`deploy.sh` uploads everything except `backup/`, `storage/`, Markdown files and the
dev scripts. `storage/` exists on the server only: it holds `leads.php` (free-training
sign-ups as CSV behind an `exit` line), the form signing secret, and
`mail-config.php` — the SMTP login for info@newhomestudent2019.com that `inc/mailer.php` uses to
email sign-ups (smtp.hostinger.com:465). If you change the mailbox password, update that file on the
server (File Manager → public_html/storage/mail-config.php); it is deliberately not in git.

### Cut-over checklist (done 2026-11-19 except where noted)

1. Detach `newhomestudent2019.com` from the WordPress website `7XTGiOm4A`.
2. Attach it to `orKz31Eb7` as the primary domain and enable SSL.
3. Clear the CDN cache; spot-check `/`, a post, `/feed/`, `/sitemap.xml`, an old `/wp-content/uploads/…` image URL.
4. **To do:** resubmit `https://newhomestudent2019.com/sitemap.xml` in Google Search Console.
5. **To do:** send a test sign-up from `/free-training/` and confirm the email arrives at info@ (SMTP login verified from the server 2026-11-19; no test message sent).
6. Keep the WordPress site (or a full backup of it) for a few weeks before deleting it.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical host, legacy redirects, routing |
| `inc/config.php` | Site name, contact details, Amazon tag, categories, nav, legacy redirects |
| `inc/functions.php` | Post loader, body renderer (product markers, link hardening, TOC), JSON-LD |
| `inc/products.php` | Amazon link builder and product cards |
| `inc/layout.php` | `<head>`, header, footer |
| `inc/views.php`, `inc/views-special.php` | Post, archive, page, home, free-training form, products hub, sitemap, RSS |
| `content/posts/<slug>.php` | One file per blog post (URL = `/<slug>/`) |
| `content/pages/<slug>.php` | Simple pages (about, contact, legal, resources, build-a-home-yourself, write-for-us) |
| `data/product-meta.php` | Product catalog: name, blurb, group, fallback search query |
| `data/asins.php` | Verified Amazon ASINs per product key |
| `inc/mailer.php` | Authenticated SMTP sender for the free-training form (reads `storage/mail-config.php`) |
| `data/site.webmanifest.json` | Web app manifest, served at `/site.webmanifest` by index.php with the correct MIME type |
| `data/legacy-images.php` | Old `/wp-content/uploads/…` featured-image paths → new WebP files |
| `assets/` | CSS, JS (mobile menu only), images |
| `googlecccfbf2f7e9e5ae4.html` | Google Search Console verification file — keep it |
| `backup/` | WordPress REST export of all posts/pages/media + original images (not deployed) |
| `CONTENT-SPEC.md` | Writing/format rules for posts |

## Analytics

Google Tag Manager container `GTM-N59TH97L` (`SITE['gtm_id']` in `inc/config.php`) is on every page:
the standard GTM head snippet plus the `<noscript>` iframe after `<body>`, and a `gtag()` helper on
`dataLayer`. Add GA4 and other tags inside GTM, not in the templates.

## Amazon affiliate links

Tag: `newhomestudent2019-20` (in `inc/config.php`). Writers never paste Amazon URLs; in a
post body use:

- `<!--products:laser_measure,moisture_meter|Optional heading-->` → product card grid
- `[[amz:books_heldmann|anchor text]]` → inline affiliate link

Keys come from `data/product-meta.php`. A key with an ASIN in `data/asins.php` links to
`amazon.com/dp/<ASIN>?tag=…`; one without falls back to an Amazon search link with the tag
(still earns commission). Links carry `rel="sponsored nofollow noopener"`. Following Amazon's
Associates rules, the site shows **no prices, star ratings or Amazon images** — only our own
blurbs and a "Check price on Amazon" button — and carries the required disclosure in the
footer, on every post with products, and at `/affiliate-disclosure/`.

To add a product: add a row to `data/product-meta.php`, put its ASIN in `data/asins.php`,
then reference the key from posts. The `/our-products/` hub lists every product automatically.

## Adding a blog post

Create `content/posts/<slug>.php` following `CONTENT-SPEC.md` (an existing post is the best
template), run `php validate.php`, deploy. The post appears on `/blog/`, its category page,
`/feed/` and `/sitemap.xml` automatically. A featured image is optional: drop a 1200px-wide
`assets/img/posts/<slug>.webp`.

## URLs and redirects

- All 55 old post URLs and 8 page URLs are kept; content was rewritten and re-optimized.
- 12 new posts added for new home builders (owner-builder guide, timeline, inspections,
  costs, financing, floor plans, tools, books, smart home, subcontractors, punch list,
  new-homeowner essentials).
- Categories: `building-tips` and `tips` keep their old URLs; `real-estate-investing` and
  `apartment-living` are new. `/category/uncategorized/` → `/blog/`; old tags → closest page.
- `/feed/`, `/sitemap.xml` are generated; `wp-sitemap*.xml`, `sitemap_index.xml`, `wp-admin`,
  `wp-json`, `?p=` and date-style permalinks all 301 to their new equivalents.
- Old featured-image URLs: the 55 original files sit at their exact old paths under `wp-content/uploads/` (Hostinger serves file-extension URLs directly, so they can't be redirected from index.php). Resized variants like `-300x200` are not kept.

## Local preview

```sh
php -S 127.0.0.1:8099 -t . dev-router.php
```
