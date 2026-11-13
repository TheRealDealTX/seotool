# alaskainsuranceappraiser.com: static site

Alaska Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and it runs on a Hostinger Agency Growth website behind a small PHP canonical-host guard.

| | |
| --- | --- |
| Hostinger website UID | `FOmBEpQf5` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Live domain | https://alaskainsuranceappraiser.com (SSL covers apex and www; www and http 301 to the https apex) |
| Preview URL | https://darkcyan-squirrel-104297.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Nameservers | `atlas.dns-parking.com`, `hyperion.dns-parking.com` (pointed Nov 13, 2026) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@alaskainsuranceappraiser.com (form delivers over SMTP) |
| Google Tag Manager | `GTM-W3M89TSN` (client's snippet in `<head>` + noscript iframe after `<body>`) |
| Search Console | `googlecccfbf2f7e9e5ae4.html` verification file in `static/` (skipped by `validate.py`) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 community pages (borough, neighborhoods, housing mix, events, perils) |
| `src/tools.py` | 7 interactive tools (markup and copy; the math is in `static/assets/js/app.js`) |
| `src/learn.py` | Process guide (8 steps), grouped FAQ, 44-term glossary, 5 guide articles |
| `src/photos.json` | Photo metadata: title, creator, license, source, size, alt text |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`, copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the File Browser TUS API |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid FOmBEpQf5); they expire after a few hours
export AIA_FB_URL=… AIA_FB_AUTH=… AIA_FB_REST=…
./deploy.sh        # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete its old file on the server:
`DELETE {AIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` was deleted this way.

Local preview that behaves like the host: `cd public && php -S 127.0.0.1:8080 router.php`, with a router
that serves real files directly, runs a directory's `index.php`, and sends everything else to the root `index.php`.

## Pages (51 in the sitemap, plus the 404)

- Home, `/about-the-practice/`, `/contact-an-appraiser/`
- `/appraisal-practice/` + 12 services (appraisal clause representation, homeowner, commercial/HOA/condo,
  roof/hail/ice, windstorm, snow load & ice dam, frozen pipe & water, fire/smoke/wildfire, earthquake
  endorsement, remote/off-road-system properties, carrier estimate review, neutral umpire)
- `/communities-served/` + 12 communities (`/communities-served/<slug>-insurance-appraiser/`): Anchorage,
  Eagle River & Chugiak, Wasilla, Palmer, Fairbanks, Juneau, Ketchikan, Sitka, Kenai & Soldotna, Homer, Kodiak, Valdez
- `/appraisal-tools/` + 7 tools: appraisal gap & fee estimator (with remote-travel costs), RCV/ACV depreciation
  worksheet, roof area & pitch calculator (with eave ice-and-water shield), earthquake/wind percentage deductible
  calculator, claim timeline planner (.ics export), appraisal file checkup, roof snow load calculator
- `/appraisal-clause-process/`, `/alaska-appraisal-faq/`, `/insurance-claim-glossary/`, `/alaska-claim-guides/` + 5 guides
- `/privacy-and-data/`, `/website-use-terms/`, `/appraisal-disclaimer/`, `/photo-credits/`, `/full-site-map/`, `404.html`

The URL scheme, copy and design differ from every sister `*insuranceappraiser*` site in the Hostinger account.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly**
  (running a directory's `index.php`) without going through the root `index.php`. A `dir/index.html` page would
  skip any redirect, so `http://www.…/page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by plain HTML with no other PHP.
  The homepage is `home.html` (served by the front controller). There is no root `index.html`, and there must
  never be a `dir/index.html` on the server.
- `_guard.php`: on the real domain, 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`)
  to `https://alaskainsuranceappraiser.com`; 301s `/dir/index.php` and `/index.php` to the directory; sends
  `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview URL); returns 404 if requested directly.
- `index.php` front controller: requires the guard, serves `home.html` for `/`, 301s directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Hostinger serves its own Googlebot-blocking `robots.txt` on preview domains. That is expected; ours is served on
  the real domain.
- Verified locally (host-like router) and on the preview URL: an interior page requested with `Host: www.…` or
  with `X-Forwarded-Proto: http` 301s to `https://alaskainsuranceappraiser.com/that-page/`, and `/that-page/index.php`
  301s to `/that-page/`.

## Design

- Palette from `#FFB612` (gold): deep shade `#7A4F00` (links and accents on light), light tint `#FFF3D1` / wash
  `#FFFAEE`, complementary glacier blue `#1F6FA8` (`#8FD0F7` on dark), neutrals midnight `#0E1621`, slate and snow.
- Fonts: Space Grotesk (display) + Albert Sans (body), not used on any sister site.
- Layout: full-bleed photo hero with a horizontal lead-form bar, gold counter band, photo cards with icon
  badges, a horizontal process trail that fills as you scroll (vertical on mobile), alternating region rows, a
  sideways-scrolling community strip, split photo heroes on interior pages (diagonal photo edge) and a
  two-column layout with a sticky sidebar (call box + related links).
- Effects: header that turns solid on scroll, hero parallax, staggered reveal, animated counters, card hover zoom,
  scroll-filled process trail, back-to-top button. All respect `prefers-reduced-motion`, and content is visible
  without JavaScript (reveal styles only apply when the `js` class is set).
- Mobile: off-canvas drawer outside the sticky header (accordion, scroll lock, close on ×/overlay/link/Escape,
  `inert` + `aria-hidden`, shadow and visibility only while open) and a fixed bottom call bar. The logo link never
  changes color or underlines on hover (header, drawer, footer).
- Logo mark: gold peak with a snow cap over a glacier-blue ledger line on a midnight tile. Favicons: `favicon.svg`,
  `favicon.ico` (16/32/48, bolder small-size variant), 96px PNG, full-bleed 180px `apple-touch-icon`, maskable
  192/512 PNGs in `site.webmanifest`, all with `?v=` cache-busters. OG image: 1200×630 JPG built from the hero photo.

## Photos

38 photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`): Flickr CC0/PD (including
U.S. government accounts such as USFWS Alaska, Alaska NPS, Alaska National Guard, USDA, NIFC), StockSnap, rawpixel,
Wikimedia Commons and the WordPress photo directory. Downloads ran one at a time with pauses and backoff; Wikimedia
images used the 1280px thumbnail width and contact sheets were reviewed by file label. Each photo is saved as 1200px
and 640px WebP with `srcset`, `sizes`, width and height. Most sources top out at 960–1024px, so the 1200px files are
mildly upscaled; one (water damage) started at 683px. Every photo is listed with its license and source on
`/photo-credits/`. Decorative backgrounds use `alt=""`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; both unique
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; each graph has the ProfessionalService (logo, contact point,
  AK region, state + cities served, OfferCatalog), the WebSite and exactly one page node linked to its breadcrumb,
  primary image and main entity. Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo and DefinedTermSet
  appear where they apply
- Canonical to `https://alaskainsuranceappraiser.com/...`, Open Graph image size and alt, Twitter card, `geo.region` US-AK
- No broken internal links or anchors; `alt` on every image
- Homepage main content mentions "Alaska Insurance Appraiser" at least 14 times (currently 19; 24 with header/footer)
- No sister-state name anywhere in the build (Alabama, Arizona, Arkansas, Delaware, Florida, Georgia, Kentucky, Maine,
  Maryland, Massachusetts, Missouri, Montana, Nevada, New York, North Carolina, West Virginia, Wyoming)
- Every `dir/index.php` starts with the guard line and contains no other PHP

## Contact form

`/api/contact.php` has a honeypot, a per-IP rate limit (5 per 10 minutes) and validation (name, valid email or
phone, consent). It sends through `info@alaskainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to `mail()`, and always appends a JSON
line to `api/_private/leads.log.php`. The log starts with `<?php http_response_code(404); exit; ?>` and the config
checks a constant, so both return 404 when requested directly. They live in `public_html` because the file API can't
write outside it. `_private/` is git-ignored: **never commit credentials.**

SMTP is live (Nov 13, 2026): the config below was uploaded, its URL returns 404 with 0 bytes, and a
submission labelled as a test logged `"via":"smtp"`. To change the password, upload this as `public_html/api/_private/config.php` (keep any local copy outside the
repo and delete it after upload), confirm the URL returns 404 with 0 bytes, send one submission labelled as a
test, and check the log shows `"via":"smtp"`:

```php
<?php
if (!defined('AIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@alaskainsuranceappraiser.com', 'smtp_pass' => '…'];
```

## Google Tag Manager

`GTM_ID = "GTM-W3M89TSN"` in `build.py`. `gtm_head()` prints the client's snippet exactly as provided (async
`gtm.js` loader plus the `dataLayer`/`gtag` stub) and `gtm_body()` prints the `<noscript>` iframe right after `<body>`.
Set `GTM_ID = ""` to remove both.

## Going live checklist

1. ~~Point the nameservers~~ done; SSL `ssl_cert.names` covers the apex and www, and both present valid certificates.
2. ~~Canonical-host check on the live domain~~ done on the homepage and four interior pages: http, http-www and
   https-www all 301 to the https apex, `/page/index.php` 301s to `/page/`, all 51 sitemap URLs return 200 with no
   `X-Robots-Tag`, and our own `robots.txt` is served. (If a www URL ever returns 200 with `x-hcdn-cache-status: HIT`,
   clear the cache and recheck.)
3. ~~GTM, SMTP and the Search Console file~~ done, validated, redeployed and cache cleared.
4. Submit `https://alaskainsuranceappraiser.com/sitemap.xml` in Google Search Console.
