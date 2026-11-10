# arizonainsuranceappraiser.com — static site

Arizona Insurance Appraiser is a static site with no database and no plugins. A Python generator
builds it, and a small PHP front controller serves it on a Hostinger Agency Growth website.
The engineering came from `georgiainsuranceappraiser/` (generator pattern, `validate.py`,
`deploy.sh`, `api/contact.php`, tool logic), with the stricter validator and the icon/photo/OG
pipelines from the North Carolina build. The copy, URL slugs, palette, fonts and layout are new
and differ from every sister site (Alabama, Florida, Georgia, North Carolina).

| | |
| --- | --- |
| Hostinger website UID | `M07QR10Uv` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Live domain | https://arizonainsuranceappraiser.com (SSL; www and http redirect to it) |
| Preview URL | https://deepskyblue-beaver-435823.hostingersite.com (sends `X-Robots-Tag: noindex`; first temporary URL was darkslateblue-sparrow-415541) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@arizonainsuranceappraiser.com (form delivers over SMTP, verified) |
| Google Tag Manager | `GTM-KFJD7RGX`: the owner's head snippet verbatim (`GTM_HEAD_SNIPPET`) + noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD graph, sitemap, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 city pages (county, neighborhoods, housing mix, storm history, FAQs) |
| `src/tools.py` | 7 tools (markup + copy); the logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Appraisal roadmap (8 steps, HowTo), FAQ (22 Qs in 5 groups), glossary (42 terms), 6 articles |
| `src/photo_sources.json` → `src/photos.json` | Photo sources and processed metadata |
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
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid M07QR10Uv); they expire after a few hours
export AIA_FB_URL='…' AIA_FB_AUTH='…' AIA_FB_REST='…'
./deploy.sh
```

Then clear the cache with `agency-hosting_cache_clear-website` (website_uid `M07QR10Uv`).
Bump `VER` in `build.py` when CSS or JS change, and `FAV` when icons change (the manifest has its own `?v=`).

Local preview with real routing: `php -S 127.0.0.1:8765 -t public router.php`, where the router
returns `false` for existing files and otherwise requires `public/index.php`.

## Pages (51 in sitemap + 404)

One main keyword per page. URL scheme:

- `/` home (*Arizona Insurance Appraiser*), `/our-firm/`, `/get-in-touch/`
- `/appraisal/` + 11 services: appraisal-clause-appointment, home-insurance-appraisal,
  commercial-and-hoa-appraisal, tile-roof-and-hail-claims, monsoon-wind-microburst-claims,
  water-and-slab-leak-claims, fire-and-smoke-damage-appraisal, wildfire-and-ash-claims
  (state-specific peril), snow-load-and-freeze-claims, claim-estimate-second-opinion,
  umpire-selection-and-service. No hurricane page: Arizona isn't a hurricane state, so tropical
  remnants are covered on the monsoon page.
- `/cities/` + 12 cities: phoenix, tucson, mesa, chandler, gilbert, scottsdale, glendale, flagstaff,
  prescott, yuma, lake-havasu-city, sierra-vista
- `/claim-calculators/` + 7 tools: appraisal-payoff-estimator (fees + break-even point),
  depreciation-recovery-calculator, roof-squares-by-material (tile/shingle/metal/foam),
  percentage-deductible-calculator, claim-deadline-calendar (.ics export),
  claim-file-readiness-check, tile-roof-repair-or-replace-checker (new, Arizona-specific)
- `/appraisal-roadmap/` (HowTo), `/questions/` (FAQ by topic), `/claim-dictionary/` (searchable
  glossary), `/articles/` + 6 articles
- `/privacy-notice/`, `/website-terms/`, `/disclosures/`, `/photo-credits/`, `/page-index/` (HTML
  site map), `/404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** dark red `#8e1b1b` (deep `#3a0909`, ink `#5c1010`), tint `#fbefec`, complementary
  turquoise accent `#1f9e95` (light `#6fd6cd` on dark), and sand/stone neutrals (`#f7f1ea`).
- **Type:** Bricolage Grotesque (display) + Figtree (body). No sister site uses either.
- **Logo/favicon:** a turquoise sun rising behind a sandstone mesa line on a dark-red tile.
- **Layout:** floating pill header; full-bleed photo hero (haboob over Phoenix) with a slanted
  bottom edge and a lead form card; overlapping counter strip; photo-pair intro; an Arizona
  claim calendar (perils by month); bento of service photo cards with chips; red gap-check band;
  sticky stacking process cards; "Four Arizonas" region photo panels; tool rows with thumbnails;
  city photo tiles; myth vs. fact cards; FAQ; articles; parallax CTA; contact form.
  Interior pages use photo heroes and a two-column layout with a sticky sidebar.
- **Effects:** header turns solid on scroll, hero/CTA parallax (clamped so the photo always
  covers), staggered reveal, animated counters, calendar bars that draw in, card hover zoom,
  sticky-stack process cards and a back-to-top button. Deliberately not used (sister sites
  have them): progress bar, marquee, 3D tilt, region tabs, scroll-filled timeline, ribbon.
  All motion respects `prefers-reduced-motion`; without JS, all content is visible.
- **Mobile nav:** off-canvas `#drawer` rendered outside the header. There is no
  `backdrop-filter` in the CSS. Accordion submenus, scroll lock, closes on ×, overlay tap,
  link tap or Escape; toggles `inert`/`aria-hidden`/`aria-expanded`; shadow and visibility
  apply only while open. Fixed call bar below 760px.

## Photos

38 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`):
Flickr CC0/PDM (including U.S. Forest Service wildfire and NOAA hail photos), StockSnap,
rawpixel and the WordPress Photo Directory. Wikimedia was rate-limited from this environment
and skipped. Contact sheets were reviewed by file ID; photos with political figures, text
overlays or artwork were skipped, and so were photos already used on the Georgia or North
Carolina sites. Each is served as ≤1200px and 640px WebP with `srcset`/`sizes` and
width/height, and listed on `/photo-credits/`. CC0 city photos exist for Phoenix, Tucson-area
saguaros and Flagstaff's San Francisco Peaks; other city tiles use regional photos with
alt text that doesn't claim a specific city. Re-run `python3 tools/photos.py` after editing
`src/photo_sources.json`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150
  characters. Titles and descriptions are unique.
- Exactly one H1, the first heading is the H1, no skipped levels (footer, sidebar and tool
  widgets included).
- Valid JSON-LD. Every `{"@id": …}` reference resolves within the page graph. The graph has
  ProfessionalService (logo, contactPoint, address, areaServed, OfferCatalog) + WebSite + one
  page node with breadcrumb, primaryImageOfPage and mainEntity, plus Service, FAQPage,
  ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply.
- Canonical equals `https://arizonainsuranceappraiser.com/...`; OG (with image size/alt),
  Twitter and `geo.region` tags present.
- No broken internal links or anchors. Every image has `alt` and width/height.
- The homepage's `<main>` contains "Arizona Insurance Appraiser" at least 14 times (currently 17).
- No sister-state name (Alabama, Florida, Georgia, North Carolina/Carolina, Texas) appears anywhere in the output.

## Hosting notes

- The host ignores `.htaccess`, serves real files directly, and sends `/` and unknown paths to
  `index.php`. That file serves `home.html` for `/`, adds a trailing slash to directory URLs
  (301), returns `404.html` with a real 404, and sends `X-Robots-Tag: noindex` on any host
  other than the real domain. Don't add a root `index.html`.
- On the real domain only, `index.php` 301-redirects `www.` and plain http (via
  `X-Forwarded-Proto`) to `https://arizonainsuranceappraiser.com`. Existing files (interior
  pages) are served by the host without `index.php`, so a one-line script at the top of every
  `<head>` sends www/http visitors on the real domain to https; canonicals already point there.
- On `*.hostingersite.com` preview domains Hostinger serves its own `robots.txt` (blocking
  Googlebot). Ours is served once the domain is connected.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy
  (File Browser REST `DELETE /api/resources/public_html/default.php`).

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation.
It sends each lead through `info@arizonainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`,
and always appends a JSON line (with `"via"`) to `api/_private/leads.log.php`.

The SMTP password is **never in git** (`_private/` is in `.gitignore`, and `deploy.sh` never
uploads it). The Hostinger file API can't write outside `public_html`, so both private files
live there and answer direct requests with an empty 404: the config through its defines-guard,
the log through its `<?php http_response_code(404); exit; ?>` header. Once the mailbox exists,
upload this as `public_html/api/_private/config.php`:

```php
<?php
if (!defined('AIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@arizonainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then: confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test,
and confirm the log line shows `"via":"smtp"`.

## Go-live status (2026-11-10)

1. Domain connected to `M07QR10Uv`; SSL active (apex certificate plus a wildcard covering www).
2. `/` on www and http returns 301 to `https://arizonainsuranceappraiser.com/`; interior
   pages redirect in the browser. The real domain sends no noindex header and serves our robots.txt.
3. GTM `GTM-KFJD7RGX` is on every page. SMTP config uploaded: the config and log URLs return
   404 with 0 bytes, and one labelled test submission logged `"via":"smtp"`.
4. `validate.py` passes with zero errors; redeployed and cache cleared.
5. Still to do by the owner: submit `https://arizonainsuranceappraiser.com/sitemap.xml` to Google Search Console.
