# georgiainsuranceappraiser.com — static site

Georgia Insurance Appraiser: a static site with no database and no plugins. It is built
by a Python generator and served by a tiny PHP front controller on a Hostinger Agency
Growth website.

| | |
| --- | --- |
| Hostinger website UID | `NtH7QOTDM` (Agency Growth, order 1008744732, php-fpm 8.3) |
| Temporary URL | https://snow-chinchilla-788360.hostingersite.com |
| Live domain | https://georgiainsuranceappraiser.com (SSL; www and http 301 to it) |
| Google Tag Manager | `GTM-K6P2TP3Z` (head snippet + noscript iframe on every page) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@georgiainsuranceappraiser.com |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Georgia location pages |
| `src/tools.py` | 6 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, FAQ, glossary, 5 insight posts |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `src/photos.json` | Photo metadata (title, creator, license, source URL, size) used for `img()` and `/photo-credits/` |
| `public/` | **Build output.** This folder is what gets deployed (committed) |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads `public/` to the website's `public_html` |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# get creds from the Hostinger API: agency-hosting_files_generate-upload-url (website_uid NtH7QOTDM)
export GIA_FB_URL=… GIA_FB_AUTH=… GIA_FB_REST=…
./deploy.sh        # then clear cache: agency-hosting_cache_clear-website
```

Local preview: `cd public && php -S localhost:8000` (or `python3 -m http.server` and open `/home.html`).

## Pages (48 in sitemap)

- Home, About, Contact
- `/appraisal-services/` + 11 services
- `/locations/` + 12 cities (`/locations/<city>-ga/`)
- `/claim-tools/` + 6 tools: appraisal value estimator, depreciation & holdback,
  roof squares & pitch, wind/hail deductible, claim deadline planner (.ics export),
  appraisal readiness score
- `/how-appraisal-works/`, `/appraisal-faq/`, `/claim-glossary/`, `/insights/` + 5 posts
- Privacy, Terms, Disclaimer, HTML site map, 404

The URL scheme, copy and design differ from the sister Alabama site on purpose.
`validate.py` fails the build if the word "Alabama" appears anywhere. It also checks
that the homepage's main content mentions "Georgia Insurance Appraiser" at least 14 times
(currently 18, or 22 counting the header and footer). It checks for broken links, one H1
per page, valid JSON-LD, and unique titles and descriptions.

## Design

Maroon base (`#7a1d33`, deep `#2b0b14`) with warm gold (`#e3a94f`) and blush accents;
Outfit headings, Inter body. Photo-led: full-bleed hero with slow zoom and a glass lead form,
animated stat counters, a bento grid of service photo cards, a scroll-filled process
timeline, region tabs with photos, 3D-tilt tool cards, parallax banners, scroll progress bar,
staggered reveal animations and a header that goes from transparent to frosted on scroll.
All motion respects `prefers-reduced-motion`.

Mobile nav is an off-canvas drawer (`#drawer`) rendered *outside* the sticky header, with
accordion submenus, scroll lock, and close on ×, overlay tap, link tap or Escape.

## Photos

All 30 photos are royalty-free: CC0 (StockSnap, rawpixel, Flickr CC0) or public domain
(U.S. government agency photos), found through the Openverse API. Each is served as
1200px and 640px WebP in `static/assets/img/photos/`. Sources and creators are listed on
`/photo-credits/` (attribution isn't required, but it's included). The StockSnap originals
are limited to 960px wide via their CDN, so hero images sit behind overlays.

## Hosting notes

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting. It serves real files
  directly (running a directory's `index.php`) and sends `/` and unknown paths to the root `index.php`.
- Every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by the static HTML.
  `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`) to `https://georgiainsuranceappraiser.com`,
  sends `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview domain), and returns 404
  if requested directly. Pages used to be plain `dir/index.html`, which the host served without PHP, so
  until Nov 12, 2026 `http://www.…/locations/atlanta-ga/` loaded with a 200 instead of redirecting.
- The root `index.php` front controller requires the same guard, serves `home.html` for `/`, 301s
  directory URLs to add the trailing slash and returns `404.html` with a real 404 status.
  Don't add a root `index.html`, and never leave a `dir/index.html` on the server: the host would serve
  it before `index.php` and skip the guard. `deploy.sh` only adds and overwrites, so delete removed or
  renamed pages on the server with `DELETE {url-without-/tus}/resources/public_html/<path>` and the
  same two auth headers.
- `validate.py` reads the `dir/index.php` pages, checks each starts with the guard line, and checks
  no other PHP tag appears in the page HTML.
- The server also holds `googlecccfbf2f7e9e5ae4.html` (Google Search Console verification) and
  `api/_private/` (SMTP config and lead log). None of them are in git. Leave them in place.

## Contact form delivery

`/api/contact.php` sends each lead through `info@georgiainsuranceappraiser.com` over
authenticated SMTP (`smtp.hostinger.com:465`). It falls back to PHP `mail()` and always
appends a JSON-lines backup to `api/_private/leads.log.php` on the server.

The SMTP password is **not in git**. It lives only on the server in
`public_html/api/_private/config.php`. That file returns the settings and answers direct
requests with a 404, and so does the log. The Hostinger file API can't write outside
`public_html`, which is why they sit there. To change the password, re-upload that file:

```php
<?php
if (!defined('GIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@georgiainsuranceappraiser.com', 'smtp_pass' => '…'];
```

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (estimated with Arial metrics at 20px)
- Meta description 110–150 characters; unique titles and descriptions
- Exactly one H1, the first heading is H1, and no skipped levels (H2 → H4)
- Valid JSON-LD, no broken internal links, alt attributes on every image

Each page's JSON-LD graph holds the ProfessionalService (logo, contact point, service
catalog), the WebSite, and a WebPage node (or AboutPage, ContactPage or CollectionPage).
The page node links to its BreadcrumbList, primary image and main entity (Service,
BlogPosting, WebApplication, HowTo or DefinedTermSet), plus FAQPage and ItemList where they apply.

## Going live checklist (done)

1. ~~Attach the domain and wait for SSL~~ — done.
2. ~~Create the mailbox~~ — done, and the form delivers through it over SMTP. The form at `/api/contact.php`
   sends to it with PHP `mail()`. It also keeps a JSON-lines backup at `../gia-leads.log`,
   outside `public_html`.
3. Submit `https://georgiainsuranceappraiser.com/sitemap.xml` to Google Search Console.
