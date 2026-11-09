# montanainsuranceappraiser.com — static site

Montana Insurance Appraiser is a static site with no database and no plugins. A Python generator builds it, and a small
PHP front controller serves it on a Hostinger Agency Growth website. The engineering came from `georgiainsuranceappraiser/`
(generator pattern, `validate.py`, `deploy.sh`, `api/contact.php`, tool logic), with the favicon, photo and OG-image
pipelines from the sister builds. The copy, URL slugs, palette, fonts and layout are new and differ from every sister site
(Alabama, Florida, Georgia, North Carolina).

| | |
| --- | --- |
| Hostinger website UID | `0rnHX7sNJ` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Temporary URL | https://slateblue-spoonbill-201486.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Final domain | https://montanainsuranceappraiser.com (not connected yet) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@montanainsuranceappraiser.com (mailbox still to be created) |
| Google Tag Manager | Off. Set `GTM_ID` in `build.py` to turn it on |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD graph, sitemap, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages (county, region, neighborhoods, housing mix, weather history, FAQs) |
| `src/tools.py` | 7 tools (markup + copy); the logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Appraisal roadmap (8 stages), FAQ (25 Qs in 5 groups), claim dictionary (45 terms), 6 field notes |
| `src/photo_sources.json` → `src/photos.json` | Photo sources and processed metadata (size, license, creator, landing page) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This folder is what gets deployed (it is committed) |
| `tools/make_icons.py` | Favicon + logo pipeline (SVG, ICO 16/32/48 with bolder strokes, 96px, 180px touch icon, maskable 192/512) |
| `tools/photos.py` | Photo pipeline: download → ≤1200px and 640px WebP + `photos.json` |
| `tools/make_og.js` | Renders the 1200×630 `og-image.jpg` with Playwright, using the site fonts |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
```

```sh
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 0rnHX7sNJ); they expire after a few hours
export MTIA_FB_URL='…' MTIA_FB_AUTH='…' MTIA_FB_REST='…'
./deploy.sh
```

Then clear the cache with `agency-hosting_cache_clear-website` (website_uid `0rnHX7sNJ`). When CSS or JS changes, bump
`VER` in `build.py`. When icons change, bump `FAV` (the manifest has its own `?v=`).

Local preview with real routing: `php -S 127.0.0.1:8765 -t public router.php`, where `router.php` returns `false` for
existing files and otherwise requires `public/index.php`. Or run `python3 -m http.server` in `public/` and open `/home.html`.

## Pages (52 in sitemap + 404)

URL scheme, with one main keyword per page:

- `/` home (*Montana Insurance Appraiser*), `/about-our-firm/`, `/get-in-touch/`
- `/claim-services/` + 12 services: appraisal-clause-representation, homeowner-claim-appraisal, commercial-hoa-claim-appraisal,
  hail-roof-damage-appraisal, wind-tornado-damage-appraisal, water-damage-claim-appraisal, fire-smoke-claim-appraisal,
  wildfire-claim-appraisal and snow-load-ice-dam-freeze-claims (the state-specific perils), ranch-farm-outbuilding-claims,
  insurance-estimate-review, umpire-services. No hurricane page: Montana is landlocked.
- `/montana-cities/` + 12 cities: billings, missoula, great-falls, bozeman, butte, helena, kalispell, whitefish, livingston,
  havre, polson, miles-city
- `/claim-toolkit/` + 7 tools: claim-gap-calculator (fees + break-even point), depreciation-holdback-calculator,
  roof-pitch-squares-calculator, wind-hail-deductible-calculator (adds a second storm in one season),
  claim-deadline-calendar (.ics export, includes a "before winter" building-season date), appraisal-readiness-quiz,
  roof-snow-load-estimator (new: layer-by-layer psf vs. a design load)
- `/appraisal-roadmap/` (HowTo), `/appraisal-questions/` (FAQ grouped by topic), `/claim-dictionary/` (searchable glossary),
  `/field-notes/` + 6 articles
- `/privacy-notice/`, `/terms-of-service/`, `/site-disclaimer/`, `/photo-credits/`, `/site-index/` (HTML site map),
  `/404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** dark blue `#13306b` (deep `#0a1736`, ink `#0e1d42`, lighter `#1e428c`), light tint `#e9eef9`/`#f4f6fb`,
  a complementary amber accent `#f28c28` (dark `#c9650f`, light `#fde9d4`), slate neutrals.
- **Type:** Bricolage Grotesque (display) + Figtree (body). No sister site uses either.
- **Logo:** a white twin-peak ridgeline (an "M") over an amber measuring rule, with an amber sun, on a dark-blue tile.
  The same mark is used in the header, drawer and footer.
- **Layout:** full-bleed storm-photo hero with a "ticket" lead form, an amber marquee of perils and cities, an intro with
  three pledges, tall photo-overlay service cards, a four-season claim calendar, a "Four Montanas" region grid, a numbered
  process trail, a homepage snow-load quick check, photo tool cards (the last one featured full width), city photo tiles,
  a fit / not-a-fit comparison, an FAQ, field-note cards and a photo-backed contact section. Interior pages use a split
  hero (dark-blue text panel left, photo right) and a two-column layout with a sticky sidebar (call box + related links).
- **Effects:** scroll progress bar in the header, header turns solid on scroll, marquee, staggered reveal, hover zoom on
  cards, back-to-top button. All motion respects `prefers-reduced-motion`. Without JS, content stays visible and the
  header is solid. Sister sites use counters, tilt, parallax, region tabs and a filling timeline; this site leaves those out.
- **Mobile nav:** an off-canvas `#drawer` rendered outside the fixed header. There is no `backdrop-filter` anywhere in the
  CSS. The drawer has accordion submenus, scroll lock, and closes on ×, overlay tap, link tap or Escape. It toggles
  `inert`/`aria-hidden`/`aria-expanded`, and its shadow and visibility apply only while open. A fixed call bar sits at the
  bottom below 760px.

## Photos

The site uses 46 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`). Sources: Flickr
PDM/CC0 (NOAA NSSL, USDA and Forest Service, NRCS Montana, BLM Montana/Dakotas, Yellowstone and Glacier NPS, USFWS,
National Interagency Fire Center), StockSnap, rawpixel and wordpress.org photos. Each was reviewed on contact sheets
labelled by file ID. Photos with political figures, text overlays or artwork were skipped. Each is served as ≤1200px and
640px WebP with `srcset`/`sizes` and width/height (Flickr's public CDN size tops out at 1024px). Alt text is descriptive
and never claims a place the photo doesn't show; decorative hero and card backgrounds use `alt=""`. Every photo is listed
with its license and source on `/photo-credits/`. Re-run `python3 tools/photos.py` after editing `src/photo_sources.json`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150 characters. Titles and
  descriptions are unique.
- Exactly one H1, the first heading is the H1, and no skipped levels (footer, sidebar and tool widgets included).
- Valid JSON-LD. Every `{"@id": …}` reference must resolve within the page graph. The graph has ProfessionalService (logo,
  contactPoint, address, areaServed, OfferCatalog) + WebSite + exactly one page node with breadcrumb, primaryImageOfPage
  and mainEntity (Service, WebApplication, BlogPosting, HowTo, DefinedTermSet, ItemList or FAQPage as applicable).
- Canonical equals `https://montanainsuranceappraiser.com/...`. OG (with image size/alt), Twitter and `geo.region` tags are present.
- No broken internal links or anchors. Every image has `alt` and width/height.
- The homepage's `<main>` contains "Montana Insurance Appraiser" at least 14 times (currently 17).
- No sister-state name (Alabama, Florida, Georgia, North Carolina/Carolina, Texas) appears anywhere in the output.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown paths to `index.php`. Don't add a
  root `index.html`: the homepage is `home.html`.
- `index.php` serves `home.html` for `/`, 301-redirects directory URLs to the trailing-slash form, serves `404.html` with a
  real 404 status, sends `X-Robots-Tag: noindex` on any host other than the real domain, and 301-redirects `www.` and plain
  http to `https://montanainsuranceappraiser.com` (only on the real domain).
- On the temporary `*.hostingersite.com` domain the platform serves its own `robots.txt` (blocking Googlebot). The site's
  own `robots.txt` takes effect once the real domain is connected.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation. It sends each lead through
`info@montanainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php`
exists, falls back to PHP `mail()`, and always appends a JSON line to `api/_private/leads.log.php` (it starts with a
404-and-exit PHP header, so it can't be read over the web).

The password is **never committed** (`_private/` is in `.gitignore`). Once the mailbox exists, upload this file to
`public_html/api/_private/config.php` with the File Browser API (it can't write outside `public_html`):

```php
<?php
if (!defined('MTIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@montanainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled TEST, and check that the log
line shows `"via":"smtp"`.

## Going live checklist

1. Connect the domain to website `0rnHX7sNJ` and wait for SSL to become active.
2. Check that `www.` and `http://` 301 to `https://montanainsuranceappraiser.com` and that the real domain sends no
   `X-Robots-Tag: noindex`.
3. Create the mailbox, then wire up SMTP (above). If you have a GTM container, set `GTM_ID`.
4. `python3 build.py && python3 validate.py`, redeploy, then clear the cache.
5. Submit `https://montanainsuranceappraiser.com/sitemap.xml` in Google Search Console.
