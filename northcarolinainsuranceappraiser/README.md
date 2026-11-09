# northcarolinainsuranceappraiser.com — static site

North Carolina Insurance Appraiser is a static site with no database and no plugins. A Python
generator builds it, and a small PHP front controller serves it on a Hostinger Agency Growth website.
The engineering came from `georgiainsuranceappraiser/` (generator pattern, `validate.py`,
`deploy.sh`, `api/contact.php`, tool logic). The copy, URL slugs, palette, fonts and layout
are new and differ from every sister site (Alabama, Florida, Georgia).

| | |
| --- | --- |
| Hostinger website UID | `45jUap7vr` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter) |
| Temporary URL | https://antiquewhite-ibis-687336.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Final domain | https://northcarolinainsuranceappraiser.com (not connected yet) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@northcarolinainsuranceappraiser.com (mailbox still to be created) |
| Google Tag Manager | Off. Set `GTM_ID` in `build.py` to turn it on |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD graph, sitemap, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 local pages (county, neighborhoods, housing, storm history, FAQs) |
| `src/tools.py` | 7 tools (markup + copy); the logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 stages), FAQ (24 Qs in 5 groups), glossary (43 terms), 6 guides |
| `src/photo_sources.json` → `src/photos.json` | Photo sources and processed metadata (size, license, creator, landing page) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This folder is what gets deployed (it is committed) |
| `tools/make_icons.py` | Favicon + logo pipeline (SVG, ICO 16/32/48 with bolder strokes, 96px, 180px touch icon, maskable 192/512) |
| `tools/photos.py` | Photo pipeline: download → 1200px and 640px WebP + `photos.json` |
| `tools/make_og.js` | Renders the 1200×630 `og-image.jpg` with Playwright, using the site fonts |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
```

```sh
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 45jUap7vr); they expire after a few hours
export NCIA_FB_URL='…' NCIA_FB_AUTH='…' NCIA_FB_REST='…'
./deploy.sh
```

Then clear the cache with `agency-hosting_cache_clear-website` (website_uid `45jUap7vr`).
When CSS or JS changes, bump `VER` in `build.py`. When icons change, bump `FAV`
(the manifest has its own `?v=`).

Local preview with real routing: `php -S 127.0.0.1:8765 -t public router.php`, where the router
returns `false` for existing files and otherwise requires `public/index.php`. Or run
`python3 -m http.server` in `public/` and open `/home.html`.

## Pages (51 in sitemap + 404)

URL scheme, with one main keyword per page:

- `/` home (*North Carolina Insurance Appraiser*), `/who-we-are/`, `/contact-us/`
- `/claim-appraisal/` + 11 services: appraisal-panel-representation, residential-claim-disputes,
  commercial-hoa-condo-claims, roof-hail-loss-appraisal, wind-tornado-loss-appraisal,
  hurricane-tropical-storm-claims, water-plumbing-loss-appraisal, fire-smoke-loss-appraisal,
  ice-storm-freeze-damage (the state-specific peril), carrier-estimate-audit, neutral-umpire-services
- `/areas-we-serve/` + 12 areas: raleigh, charlotte, greensboro, durham, winston-salem, fayetteville,
  cary, wilmington, asheville, greenville, new-bern, outer-banks
- `/calculators/` + 7 tools: settlement-gap-estimator (3-outcome net after fees),
  rcv-acv-holdback-calculator, roof-area-pitch-estimator, named-storm-deductible-calculator,
  claim-timeline-planner (.ics export), appraisal-preparedness-checkup, wind-flood-damage-splitter (new)
- `/appraisal-process-guide/` (HowTo), `/common-questions/` (FAQ grouped by topic), `/insurance-terms/`
  (searchable glossary), `/guides/` + 6 articles
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/photo-credits/`, `/all-pages/` (HTML site map),
  `/404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** pine green `#1f5136` (deep `#0d2b1b`/`#14361f`), sage tint `#e8efe9`, a complementary
  clay accent (`#b8522c` for buttons, `#e27a4f` for highlights), and cream/stone neutrals.
- **Type:** Fraunces (display serif) + Manrope (body). No sister site uses either.
- **Layout:** full-bleed photo hero with an inline "strip" lead form, a trust strip, service photo cards,
  a horizontal storm-history timeline, a region rail, five numbered process cards, tool rows, location
  photo tiles and a comparison of who-does-what. Interior pages use photo heroes and a two-column
  layout with a sticky sidebar (call box + related links).
- **Effects:** header goes from transparent to solid on scroll, hero and CTA parallax, staggered
  reveal, animated counters in the clay ribbon, hover zoom on cards, and a back-to-top button with a
  scroll-progress ring. Sister sites use a top progress bar, marquee, tilt, region tabs and a filling
  timeline; this site deliberately leaves those out. All motion respects `prefers-reduced-motion`.
  Without JS, content stays visible and the header is solid.
- **Mobile nav:** an off-canvas `#drawer` rendered outside the fixed header. There is no
  `backdrop-filter` anywhere in the CSS. The drawer has accordion submenus, scroll lock, and closes
  on ×, overlay tap, link tap or Escape. It toggles `inert`/`aria-hidden`/`aria-expanded`, and its
  shadow and visibility apply only while open. A fixed call bar sits at the bottom below 760px.

## Photos

The site uses 38 photos, all CC0 or public domain, found through the Openverse API
(`license=cc0,pdm`). Sources: Flickr CC0/PDM (including NOAA, USGS, USDA, HUD, NPS and National
Guard uploads), StockSnap, rawpixel and Wikimedia CC0. Each photo was reviewed on contact sheets
labelled by file ID. Photos with political figures, text overlays or artwork were skipped, and so
were any already used on the Georgia site. Each is served as ≤1200px and 640px WebP with
`srcset`/`sizes` and width/height. Every photo is listed with its license and source on
`/photo-credits/`. Re-run `python3 tools/photos.py` after editing `src/photo_sources.json`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150
  characters. Titles and descriptions are unique.
- Exactly one H1, the first heading is the H1, and no skipped levels (footer, sidebar and tool
  widgets included).
- Valid JSON-LD. Every `{"@id": …}` reference must resolve within the page graph. The graph has
  ProfessionalService (logo, contactPoint, address, areaServed, OfferCatalog) + WebSite + exactly
  one page node with breadcrumb, primaryImageOfPage and mainEntity.
- Canonical equals `https://northcarolinainsuranceappraiser.com/...`. OG (with image size/alt),
  Twitter and `geo.region` tags are present.
- No broken internal links or anchors. Every image has `alt` and width/height.
- The homepage's `<main>` contains "North Carolina Insurance Appraiser" at least 14 times
  (currently 19).
- No sister-state name (Alabama, Florida, Georgia, Texas) appears anywhere in the output.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown paths to
  `index.php`. Don't add a root `index.html`: the homepage is `home.html`.
- `index.php` serves `home.html` for `/`, 301-redirects directory URLs to the trailing-slash
  form, serves `404.html` with a real 404 status, sends `X-Robots-Tag: noindex` on any host other
  than the real domain, and 301-redirects `www.` and plain http to `https://northcarolinainsuranceappraiser.com`
  (only on the real domain).
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation. It sends each
lead through `info@northcarolinainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (it starts with a 404-and-exit PHP header, so it can't be read over the web).

The password is **never committed** (`_private/` is in `.gitignore`). Once the mailbox exists, upload this file
to `public_html/api/_private/config.php` with the File Browser API (it can't write outside `public_html`):

```php
<?php
if (!defined('NCIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@northcarolinainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled TEST, and
check that the log line shows `"via":"smtp"`.

## Going live checklist

1. Connect the domain to website `45jUap7vr` and wait for SSL to become active.
2. Check that `www.` and `http://` 301 to `https://northcarolinainsuranceappraiser.com` and that the real domain
   sends no `X-Robots-Tag: noindex`.
3. Create the mailbox, then wire up SMTP (above). If you have a GTM container, set `GTM_ID`.
4. `python3 build.py && python3 validate.py`, redeploy, then clear the cache.
5. Submit `https://northcarolinainsuranceappraiser.com/sitemap.xml` in Google Search Console.
