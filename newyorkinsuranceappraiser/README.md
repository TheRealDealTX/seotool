# newyorkinsuranceappraiser.com — static site

New York Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency
Growth website. Engineering is copied from `georgiainsuranceappraiser/`. The content, URL slugs and
design are new.

| | |
| --- | --- |
| Hostinger website UID | `nFY9v8sgn` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter selected) |
| Live domain | https://newyorkinsuranceappraiser.com (live Nov 12, 2026; SSL covers apex + www; www, http and `/dir/index.php` 301 to the https apex) |
| Preview URL | https://goldenrod-gaur-817128.hostingersite.com (sends `X-Robots-Tag: noindex`; Hostinger also serves its own blocking robots.txt there) |
| Nameservers | `athena.dns-parking.com`, `apollo.dns-parking.com` (set) |
| Google Tag Manager | `GTM-NTJK9Q3X`: owner's head snippet used verbatim (`GTM_SNIPPET`) + noscript iframe after `<body>` on every page |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@newyorkinsuranceappraiser.com: form delivers over authenticated SMTP (verified `"via":"smtp"`) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 New York location pages |
| `src/tools.py` | 7 calculators (markup + copy). The logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Process walkthrough (8 steps), FAQ (5 topics), glossary (43 terms), 6 guides |
| `src/photos.json` | Photo metadata: title, creator, license, source, size and alt text |
| `src/photomap.py` | Which photo each service, location, tool and guide uses |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`, copied into `public/` as-is |
| `public/` | **Build output**, which is what gets deployed (committed) |
| `validate.py` | Post-build checks. The build must show zero errors |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over TUS |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh creds: Hostinger API agency-hosting_files_generate-upload-url (website_uid nFY9v8sgn)
export NYIA_FB_URL='https://…/api/tus' NYIA_FB_AUTH='…' NYIA_FB_REST='…'
./deploy.sh            # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`curl -X DELETE -H "X-Auth: $NYIA_FB_AUTH" -H "X-Auth-Rest: $NYIA_FB_REST" "${NYIA_FB_URL%/tus}/resources/public_html/<path>"`.
Hostinger's placeholder `public_html/default.php` has already been deleted.

To preview locally the way the host serves files (real files served directly, a directory's
`index.php` executed, everything else sent to the root `index.php`), use a router like the one
used in QA:

```sh
php -S 127.0.0.1:8088 -t public router.php
curl -sI -H 'Host: www.newyorkinsuranceappraiser.com' http://127.0.0.1:8088/where-we-appraise/buffalo/   # 301 to https apex
```

## Pages (51 in sitemap, plus the 404)

URL scheme (different from every sister site):

- `/`, `/our-practice/`, `/reach-us/`
- `/claim-appraisals/` + 11 services (appraisal clause representation, homeowners, co-op/condo/commercial,
  roof & hail, windstorm & tornado, hurricane & nor’easter, water, fire & smoke, **snow load & ice dam**
  (the New York-specific peril), estimate review, umpire services)
- `/where-we-appraise/` + 12 locations: Manhattan, Brooklyn, Queens, Staten Island, Hempstead, Islip,
  White Plains, Albany, Syracuse, Rochester, Buffalo, Binghamton
- `/appraisal-calculators/` + 7 tools: settlement gap & fee estimator (with a 3-outcome table), ACV vs RCV
  holdback calculator (with a holdback due date), roof area & pitch estimator (with multi-layer tear-off),
  hurricane deductible calculator (1–5% comparison table), claim calendar builder (.ics export; proof of
  loss counted from the request date), appraisal readiness checkup, and a new **co-op & condo claim splitter**
  (master policy vs HO-6, with deductible chargeback and loss assessment)
- `/appraisal-walkthrough/`, `/ask-an-appraiser/`, `/claim-vocabulary/` (searchable), `/policyholder-guides/` + 6 guides
- `/privacy-practices/`, `/site-terms/`, `/professional-disclaimer/`, `/photo-credits/`, `/site-directory/`
- `404.html` (served with a real 404 status), `sitemap.xml`, `robots.txt`

All calculators run in the browser and store nothing.

## Design

- **Palette:** NYC blue `#1550a8` with a deep navy `#0a1a3a`, a light tint `#ecf2fb` and NYC orange `#f26a1b` as
  the complementary accent (`#b9480a` for orange text on white), plus slate neutrals.
- **Fonts:** Archivo (display, set slightly expanded) and IBM Plex Sans (body). No sister site uses either.
- **Concept:** a civic "transit line" look. The services are subway-style stations on a vertical line, the
  process is a six-stop route, the hero has an orange ticker of boroughs and regions, the logo is a roofline
  over an orange "fair value" bar, and corners are kept square.
- **Homepage order:** hero with lead form → region ticker → intro + counters → "who we work for" photo cards →
  service stations → region tabs (6 regions, with photos) → storm record (7 storms) → three questions + gap
  check → route → calculators → locations → FAQ → guides → contact.
- **Effects:** scroll progress bar, header that gains a shadow and orange rule on scroll (the utility bar
  collapses), slow hero zoom, staggered reveal on scroll, animated counters, hover zoom on photo cards,
  marquee ticker, region tabs, back-to-top button. No tilt, parallax or timeline fill. Motion respects
  `prefers-reduced-motion`. Without JavaScript all content shows, all region panels are visible and the menu
  falls back to a link to the site directory.
- **Mobile:** an off-canvas drawer (`#drawer`) that sits outside the sticky header. The header has no
  `backdrop-filter`. The drawer has accordion submenus and scroll lock, and closes on ×, a scrim tap, a link tap
  or Escape. It uses `inert`/`aria-hidden`, and its shadow and visibility only apply while open. A fixed call
  bar sits at the bottom.
- **Logo:** the logo (`brand`) link in the header, drawer and footer never changes colour or underline on hover.

## Photos

36 royalty-free photos (CC0 or public domain), found through the Openverse API (`license=cc0,pdm`) and
Wikimedia Commons. They were downloaded one at a time with backoff, using Wikimedia's standard thumbnail sizes.
Sources are Flickr CC0/PD (including U.S. Fish & Wildlife Service and NOAA), rawpixel, StockSnap, Wikimedia
Commons and NARA DOCUMERICA (the Brooklyn brownstones). Each photo is saved as 1200px (or its source width) and
640px WebP with `srcset`, `sizes`, width and height. Decorative backgrounds use `alt=""`. All are listed with
license and source on `/photo-credits/`. Some location pages use a regional stand-in photo (snow, river,
houses), and the alt text describes what is actually shown. The OG image (`assets/img/og-image.jpg`, 1200×630)
is built from the hero photo.

Icons: `favicon.svg`, `favicon.ico` (16/32/48, bolder mark), `favicon-96x96.png`, full-bleed 180px
`apple-touch-icon.png`, and maskable `favicon-192.png`/`favicon-512.png` in `site.webmanifest`, all linked with `?v=1`.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS", and **serves real files directly**
  without running the root `index.php`. A `dir/index.html` would therefore skip any redirect logic.
- So every page is written as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML containing no other PHP.
  The homepage is `home.html`. There is no root `index.html`, and `deploy.sh` refuses to upload any `index.html`.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://newyorkinsuranceappraiser.com`, but only on the real domain. It 301s `/dir/index.php` and `/index.php`
  to the directory, sends `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview) and returns 404
  if requested directly.
- `index.php` (the front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with status 404.
- Tested locally with a router that mimics the host. An interior page with `Host: www.…`, and with the apex
  host plus `X-Forwarded-Proto: http`, both 301 to `https://newyorkinsuranceappraiser.com/where-we-appraise/buffalo/`,
  and `/where-we-appraise/buffalo/index.php` 301s to the directory.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150 characters.
  Titles and descriptions are unique
- Exactly one H1, which is the first heading, and no skipped heading levels anywhere (footer, sidebar and tool
  widgets included)
- Valid JSON-LD, and every `@id` reference resolves on the page
- No broken internal links or anchors, and an `alt` attribute on every image
- The homepage main content uses "New York Insurance Appraiser" at least 14 times (currently 19)
- No sister-state names (Alabama, Florida, Georgia, North Carolina, Nevada, Arizona, Missouri, Montana,
  Massachusetts, Wyoming, West Virginia) in pages, sitemap, JS or the form handler
- Each `dir/index.php` starts with the guard line and contains no other PHP

Every page has a canonical URL, Open Graph tags (including image size and alt), Twitter tags and `geo.region`
`US-NY`. The JSON-LD `@graph` holds the ProfessionalService (with logo ImageObject, contactPoint, NY/US address,
state and cities in areaServed, and an OfferCatalog), the WebSite, and one page node (WebPage, AboutPage,
ContactPage or CollectionPage) with breadcrumb, primaryImageOfPage and mainEntity. It adds Service, FAQPage,
ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply.

## Contact form

`/api/contact.php` uses a honeypot, a per-IP limit of 5 submissions per 10 minutes, and validation (name, a
valid email or a phone number, and consent). It sends through `info@newyorkinsuranceappraiser.com` over
authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, and otherwise falls back
to `mail()`. It always appends a JSON line to `api/_private/leads.log.php`, whose `<?php http_response_code(404); exit; ?>`
header makes it 404 with 0 bytes. `_private/` is git-ignored. **Never commit credentials.**

**Status:** live. `public_html/api/_private/config.php` is on the server (not in git); its URL returns 404 with
0 bytes, and a test submission on Nov 12, 2026 logged `"via":"smtp"`. To change the password, re-upload the file
in this shape (keep any local copy outside the repo and delete it after upload):

```php
<?php
if (!defined('NYIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@newyorkinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test, and check that
the log shows `"via":"smtp"` (read it through the file API: `GET {url-without-/tus}/raw/public_html/api/_private/leads.log.php`).

## Google Tag Manager

`GTM_ID = "GTM-NTJK9Q3X"` in `build.py`. `GTM_SNIPPET` holds the head snippet exactly as the owner supplied it;
set it to `None` to fall back to the standard GTM loader. The `<noscript>` iframe is output right after `<body>`.

## Go-live (done Nov 12, 2026)

1. ~~Nameservers pointed~~: SSL is active for `newyorkinsuranceappraiser.com` and `www.newyorkinsuranceappraiser.com`.
2. ~~Canonical-host checks~~: on the homepage and interior pages, http, `www` and `/dir/index.php` all 301 to the
   https apex. All 51 sitemap URLs return 200. The live domain sends no `X-Robots-Tag` and serves our `robots.txt`.
3. ~~GTM and SMTP~~: added and verified, then rebuilt, validated (zero errors), redeployed and cache cleared.
4. **To do:** submit `https://newyorkinsuranceappraiser.com/sitemap.xml` to Google Search Console.

If a `www` URL ever returns 200 with `x-hcdn-cache-status: HIT`, the CDN is serving a stale copy. Clear the cache
(`agency-hosting_cache_clear-website`) and recheck after a few minutes.
