# wisconsininsuranceappraiser.com — static site

Wisconsin Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a tiny
PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `sJXNwa420` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter) |
| Live domain | https://wisconsininsuranceappraiser.com (SSL covers the apex and `www`; www and http 301 to the https apex) |
| Preview URL | https://ghostwhite-jay-318854.hostingersite.com (always sends `X-Robots-Tag: noindex`) |
| Nameservers to set at the registrar | `pixel.dns-parking.com`, `byte.dns-parking.com` (from `agency-hosting_websites_get`) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@wisconsininsuranceappraiser.com (form delivers over SMTP) |
| Google Tag Manager | `GTM-WWPMQZ85`: the owner's head snippet, verbatim (`GTM_HEAD_SNIPPET` in `build.py`), plus the noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 Wisconsin city pages (county, region, housing mix, storm history, neighborhoods) |
| `src/tools.py` | 7 calculators (markup and copy); the math is in `static/assets/js/app.js` |
| `src/learn.py` | 8-step process guide, grouped FAQ, 40-term dictionary, 6 guides |
| `src/photos.json` | Photo metadata (title, creator, license, source, size, alt text), used by `img()` |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`, copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# fresh credentials: agency-hosting_files_generate-upload-url (website_uid sJXNwa420); they expire after a few hours
export WIA_FB_URL='…/api/tus' WIA_FB_AUTH='…' WIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid sJXNwa420)
```

`deploy.sh` only adds and overwrites. If you remove or rename a page, delete its old file on the server:
`curl -X DELETE -H "X-Auth: $WIA_FB_AUTH" -H "X-Auth-Rest: $WIA_FB_REST" "${WIA_FB_URL%/tus}/resources/public_html/<path>"`.
Hostinger's placeholder `public_html/default.php` was deleted after the first deploy, and `/photo-credits/` was removed
on request (Nov 13, 2026).

The server also holds files that are deliberately not in git: `googlecccfbf2f7e9e5ae4.html` (Google Search Console
verification, in the `public_html` root) and `api/_private/` (SMTP config and lead log). `deploy.sh` never touches them.

Local preview that behaves like the host (real files served directly, a directory's `index.php` executed, everything
else through the root `index.php`): `php -S 127.0.0.1:8765 -t public router.php` (`router.php` is in this folder).

## Pages (51 in the sitemap, plus the 404)

- Home, `/about-us/`, `/contact-us/`
- `/appraisal-solutions/` + 12 services: appraisal demand representation, home, commercial & HOA, hail & roof,
  tornado & straight-line wind, snow load & roof collapse, water & sewer backup, fire & smoke, ice dam & frozen pipe
  (the Wisconsin-specific peril), farm & barn, carrier estimate review, umpire services
- `/local-appraisers/` + 12 cities grouped by region: Milwaukee, Madison, Green Bay, Kenosha, Racine, Appleton,
  Waukesha, Eau Claire, Oshkosh, Janesville, La Crosse, Wausau
- `/insurance-claim-calculators/` + 7 tools: settlement gap (with fees and a break-even point), RCV/ACV holdback,
  roof pitch & squares (with an eave ice-barrier estimate), percentage deductible (with a 0.5–5% comparison table),
  claim timeline planner (.ics export and a spring-thaw re-inspection reminder), appraisal readiness quiz, and
  roof snow load (new for this site). Everything runs in the browser and nothing is stored
- `/appraisal-process-guide/`, `/insurance-appraisal-faq/` (5 topic groups), `/claims-dictionary/` (40 terms, searchable),
  `/learning-center/` + 6 guides
- `/privacy/`, `/terms/`, `/disclaimer/`, `/html-sitemap/`, `404.html` (real 404 status),
  `sitemap.xml`, `robots.txt`

URL slugs, copy, section order and design were written fresh and differ from the 22 sister `*insuranceappraiser*`
sites on the same Hostinger order.

## Design

- **Palette:** navy `#002986` (deep `#001A5C`, deepest `#000F38`), gold `#FFCC18` (deep `#C99A00`, tint `#FFF6D1`),
  light tint `#EEF2FB`, one complementary accent (cranberry `#B3263E`, a nod to Wisconsin's cranberry bogs) and
  neutrals `#F7F6F2` / `#E4E6EC` / `#5A6175` / `#141A2E`. Gradients only on photo overlays.
- **Fonts:** Epilogue (display) + Mulish (body). No sister site uses either.
- **Logo:** navy tile with a gold "W" drawn as a valuation line under a white roof gable. The same SVG is used in the
  header, drawer and footer. `favicon.svg`, `favicon.ico` (16/32/48 from a bolder variant), 96px PNG, full-bleed
  180px `apple-touch-icon.png`, maskable 192/512 PNGs in `site.webmanifest`. Every icon link has `?v=1`.
  OG image: 1200×630 JPG built from the hero photo.
- **Homepage order:** full-bleed photo hero with a lead form and a gold peril strip → intro split with counters →
  four-season claim calendar (tabs with photos) → 12-service photo grid → scroll-filled process timeline → gap check
  and calculator cards (3D tilt) → city photo list → storm-record rail → appraiser / adjuster / attorney cards → FAQ →
  guides → parallax CTA → contact form.
- **Effects:** scroll progress bar, header that turns solid on scroll, hero Ken Burns zoom, staggered reveal, animated
  counters, card hover zoom, 3D tilt on calculator cards, timeline fill, season tabs, parallax CTA and page heroes,
  back-to-top. All respect `prefers-reduced-motion`. Reveal styles only apply once JS adds `html.js`, so the site
  renders fully without JavaScript.
- **Mobile:** off-canvas drawer (`#drawer`) outside the fixed header (the header has no `backdrop-filter`), with
  accordion submenus, scroll lock, close on ×, overlay tap, link tap or Escape, `inert`/`aria-hidden` handling, and
  shadow and visibility only while open. Fixed call bar at the bottom. The brand link never changes color on hover.

## Photos

30 photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`): rawpixel, StockSnap, Flickr
CC0/PD (including USDA and U.S. Fish & Wildlife Service photos) and Wikimedia Commons (Milwaukee skyline, the State
Capitol in Madison, Rib Mountain near Wausau). Each is served as 1200px (or the largest the source offers, 960–1200px)
and 640px WebP with `srcset`, `sizes`, `width` and `height`. Alt text is descriptive; decorative backgrounds use
`alt=""`. The creator, source and license of every photo are kept in `src/photos.json` (the public photo credits page
was removed at the owner's request; attribution isn't required for CC0/PD images).

Downloads ran one file at a time with pauses and backoff; Wikimedia thumbnails used the standard 330px (contact
sheets) and 1280px (finals) widths. Wikimedia rate-limited a La Crosse photo and Flickr refused two downloads, so
those were skipped. Cities without a usable CC0/PD photo use a regional stand-in (lakeshore, farmland or homes).
Photos whose titles named other states were dropped so the banned-word check stays clean.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly** without
  running the root `index.php` (a directory's `index.php` is executed). A `dir/index.html` page would skip any redirect.
- So every page is written as `dir/index.php`. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP.
  The homepage is `home.html`, served by the front controller. There is no root `index.html`, and there must never be a
  `dir/index.html` on the server.
- `_guard.php`: 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://wisconsininsuranceappraiser.com` on the real domain only; 301s `/dir/index.php` and `/index.php` to the
  directory; sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL); returns 404 when requested.
- `index.php` front controller: requires the guard, serves `home.html` for `/`, 301s directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Hostinger serves its own Googlebot-blocking `robots.txt` on preview URLs. Ours is served once the real domain is live.
- Verified locally with a host-like router: `Host: www.wisconsininsuranceappraiser.com` and
  `Host: wisconsininsuranceappraiser.com` + `X-Forwarded-Proto: http` on `/local-appraisers/milwaukee/` both 301 to
  `https://wisconsininsuranceappraiser.com/local-appraisers/milwaukee/`, and `/local-appraisers/milwaukee/index.php`
  301s to the directory.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; both unique
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer and sidebar included)
- Valid JSON-LD; every `@id` reference resolves; each graph has the ProfessionalService, WebSite and exactly one page
  node (WebPage, AboutPage, ContactPage or CollectionPage), plus a BreadcrumbList on interior pages
- Canonical to `https://wisconsininsuranceappraiser.com/…`, Open Graph image size and alt, Twitter card, `geo.region`
- No broken internal links or anchors; every image has `alt`
- The homepage's `<main>` says "Wisconsin Insurance Appraiser" at least 14 times (currently 20, 25 counting header
  and footer)
- None of the 22 sister-site state names appear anywhere in the build
- Every `dir/index.php` starts with the guard line and contains no other PHP

The page node links to its BreadcrumbList, primary image and main entity (Service, WebApplication, BlogPosting,
HowTo, DefinedTermSet or ItemList). FAQPage is added where FAQs appear, ItemList on index pages.

## Contact form

`/api/contact.php` has a honeypot, a per-IP limit (5 per 10 minutes) and validation (name, a valid email or phone,
consent). It sends through `info@wisconsininsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `public_html/api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php`. The log starts with a PHP exit header, and the config is guarded by a `define` check,
so both return 404 when requested directly. They sit inside `public_html` because the file API can't write outside it.
`_private/` is in `.gitignore`. Never commit credentials.

Config file to upload once the mailbox exists (keep any local copy outside the repo and delete it after upload):

```php
<?php
if (!defined('WIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@wisconsininsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and check that
the log shows `"via":"smtp"`.

## Go-live status (Nov 13, 2026)

1. Nameservers point to Hostinger and SSL is active for `wisconsininsuranceappraiser.com` and
   `www.wisconsininsuranceappraiser.com` (`ssl_cert.names`, expires Feb 11, 2027; Hostinger renews it).
2. Checked on the live domain (homepage plus four interior pages): http, http-www and https-www all 301 to
   `https://wisconsininsuranceappraiser.com/page/`; `/page/index.php` and `/index.php` 301 to the directory; all 51 sitemap
   URLs return 200 with no `X-Robots-Tag`; our own `robots.txt` is served; unknown URLs return 404.
3. SMTP is wired: `/api/_private/config.php` returns 404 with 0 bytes, and a submission labelled as a test was logged
   with `"via":"smtp"`.
4. GTM `GTM-WWPMQZ85` is on every page, and the Search Console verification file is uploaded.
5. Still to do by the owner: submit `https://wisconsininsuranceappraiser.com/sitemap.xml` in Google Search Console.

If a www URL ever returns 200 with `x-hcdn-cache-status: HIT`, clear the cache (`agency-hosting_cache_clear-website`).
