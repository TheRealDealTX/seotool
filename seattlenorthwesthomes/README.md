# seattlenorthwesthomes.com — custom PHP rebuild

A hand-built PHP property-listing + blog site that replaces the WordPress/Elementor
install. No database, no plugins, no framework: PHP 8 files, one CSS file, one JS file.

**Live:** https://seattlenorthwesthomes.com — Hostinger Agency website `D5jnILeBy` (php-fpm,
PHP 8.5). The domain was moved here from the WordPress website `HSLdABjjL` on 2026-11-19;
that website is untouched (files + database) and reachable at its preview domain
silver-shrew-111207.hostingersite.com as a fallback. `force_canonical_host` is on.

## Layout

| Path | What it is |
| --- | --- |
| `public_html/index.php` | Front controller: canonical host, every legacy WordPress 301, routing |
| `public_html/assets/` | `css/site.css`, `js/site.js`, images (`photos/` listings + new posts, `blog/` imported posts, `brand/`) |
| `public_html/wp-content/uploads/` | Original WordPress media at their old URLs (the host 404s missing image paths without asking PHP) |
| `app/config.php` | Business name, email, phone, brokerage, listing disclaimer, canonical-host switch |
| `app/data/listings.php` | Property listings — add/edit homes here |
| `app/data/neighborhoods.php` | Neighborhood guide content |
| `app/data/categories.php` | Blog categories |
| `app/content/posts/*.php` | One file per blog post (meta + HTML body) |
| `app/routes/`, `app/views/`, `app/lib/` | Controllers, templates, schema + form handling |
| `tools/` | `import_wp.py` (WordPress importer), `validate.py` (crawler/QA), slug + description maps |
| `backup/wordpress-2026-11-19/` | REST export of every post/page/media item and the rendered HTML of the old pages |

On the server `app/` sits inside `public_html/` (the File Browser exposes nothing else).
Every file in it begins `defined('SNW') || (http_response_code(404) && exit);`, so requesting
one directly returns an empty 404.

## URLs

| Old (WordPress) | New |
| --- | --- |
| `/about-us/` | `/about-seattle-northwest-homes/` |
| `/buying/` | `/buy-a-home-in-seattle/` |
| `/selling/` | `/sell-your-home-seattle/` |
| `/contact-us/` | `/contact-seattle-real-estate-agents/` |
| `/blog/` | `/blog/` (paginated, plus `/blog/category/<slug>/`) |
| `/<long-post-slug>/` (53 posts) | `/blog/<short-keyword-slug>/` — map in `tools/slugmap.tsv` |
| `/category/articles/`, `/author/selena/` | `/blog/`, about page |
| `/*-sitemap.xml`, `/sitemap_index.xml` | `/sitemap.xml` |
| `/feed/` | still the RSS feed |

New sections: `/homes-for-sale/` (filterable), `/homes-for-sale/<listing>/`,
`/neighborhoods/` and 12 `/neighborhoods/<slug>/` guides, `/terms-of-use/`.

All old URLs return a single 301 to their new home (`tools/validate.py` checks all 63).

## SEO

Unique title/description per page, one H1, canonical, Open Graph/Twitter, `robots`
meta, XML sitemap, RSS. JSON-LD `@graph` on every page: `RealEstateAgent` + `WebSite`
(with SearchAction), plus `RealEstateListing`/`Offer`, `BlogPosting`, `FAQPage`,
`BreadcrumbList`, `ItemList`, `Place` as relevant. Filtered listing URLs are `noindex`
and canonicalise to `/homes-for-sale/`. `*.hostingersite.com` hosts send
`X-Robots-Tag: noindex`.

## Content

- 53 WordPress posts imported verbatim (HTML cleaned, internal links rewritten, images
  localised, new hand-written meta descriptions in `tools/descriptions.tsv`). Outbound links,
  including links to partner sites, are preserved.
- 12 new Seattle posts (first-time buyers, closing costs, inspections, best time to sell,
  pricing, ADUs, neighborhoods, suburbs, light rail, maintenance, condo vs townhouse, moving
  from Texas), each with FAQ schema.
- 40 listings and 16 neighborhood guides. **The listings are representative examples, not
  live MLS inventory** — `listing_note` in `config.php` prints a disclaimer on every listing
  until you replace them with real homes (then set it to `''`).
- Listing/post photography: Unsplash (free licence), credits in `tools/photo-credits.tsv`.

## Forms

Buy, sell, contact, showing-request and newsletter forms post to `/submit/`. Stateless
HMAC token (works through the CDN), honeypot, minimum fill time, 8-per-hour IP limit.
Each lead is emailed to `config.php` `email` (info@seattlenorthwesthomes.com) through
authenticated SMTP (`app/lib/mailer.php`, smtp.hostinger.com:465, sent from and to the info@
mailbox, Reply-To set to the visitor) and appended to `app/storage/leads-YYYY-MM.php`
(guarded; read it in hPanel's file manager).

The SMTP password lives only in `app/secrets.php` on the server — git-ignored, never committed.
To recreate it, copy the format from the header comment in `app/lib/mailer.php` and deploy it
with `./deploy.sh app/secrets.php`. Without it the site falls back to PHP `mail()`.

## Local dev

```sh
php -S 127.0.0.1:8080 -t public_html public_html/index.php
python3 tools/validate.py            # or: python3 tools/validate.py https://<staging-host>
```

## Deploying

```sh
# credentials from Hostinger API agency-hosting_files_generate-upload-url (website D5jnILeBy)
export SNW_FB_URL=… SNW_FB_AUTH=… SNW_FB_REST=…
./deploy.sh                 # or ./deploy.sh app   to push only app/
```

## Launch checklist (domain moved 2026-11-19)

1. Fill in `brokerage` (Washington requires the firm name on real estate ads) and `phone`
   in `app/config.php`; replace sample listings with real ones.
2. ~~Set `force_canonical_host` to `true`.~~ Done.
3. ~~Move the domain to `D5jnILeBy`, SSL, clear CDN cache.~~ Done (Let's Encrypt cert valid to Jan 2027).
   To roll back: unlink the domain from `D5jnILeBy` and link it to `HSLdABjjL`.
4. Re-run `tools/validate.py https://seattlenorthwesthomes.com`, then submit
   `/sitemap.xml` in Google Search Console.
5. Keep the WordPress website for a week or two as a fallback, then back it up and delete it.
