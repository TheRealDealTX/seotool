# newmexicoinsuranceappraiser.com — static site

New Mexico Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served on a Hostinger Agency Growth website (php-fpm, PHP 8.3).

| | |
| --- | --- |
| Hostinger website UID | `3dr5vg4G5` (Agency Growth, order 1008744732, php-fpm 8.3, Phoenix datacenter) |
| Domain | `newmexicoinsuranceappraiser.com` (attached at creation) |
| Preview URL | https://brown-gaur-609134.hostingersite.com |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@newmexicoinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php`, GSC file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 estimators (markup + copy) |
| `src/learn.py` | Process guide, grouped FAQ, 45-term glossary, 6 reading-room guides |
| `src/photos.json` | Photo manifest: alt text, sizes, **source URL and license** for every photo (internal record) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS upload API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 3dr5vg4G5)
export NMIA_FB_URL=… NMIA_FB_AUTH=… NMIA_FB_REST=…
./deploy.sh
# then: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the
server: `DELETE {upload-url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and
`X-Auth-Rest` headers.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed,
everything else to the root `index.php`): `cd public && php -S 127.0.0.1:8090 ../dev-router.php`.

## Pages (51 in sitemap.xml, plus the 404)

- Home, About (`/about-the-company/`), Contact (`/contact-new-mexico-appraiser/`)
- `/appraiser-services/` + 12 services: appraisal demand representation, home, commercial & HOA, hail & roof,
  high wind, water, fire & smoke, **wildfire** (state-specific), **flat roof & stucco** (state-specific),
  winter freeze, estimate review, umpire
- `/cities-we-serve/` + 12 cities: Albuquerque, Las Cruces, Rio Rancho, Santa Fe, Roswell, Farmington, Hobbs,
  Clovis, Carlsbad, Alamogordo, Los Alamos, Ruidoso
- `/claim-estimators/` + 7 tools: claim gap net-recovery estimator, depreciation holdback splitter, roof area &
  pitch converter, percentage deductible converter, claim calendar builder (.ics), appraisal file checkup,
  **wildfire contents inventory estimator** (new). All run in the browser; nothing is stored.
- `/inside-the-appraisal-process/`, `/frequently-asked/`, `/claim-terms-a-to-z/` (searchable), `/reading-room/` + 6 guides
- `/privacy-and-cookies/`, `/terms-of-website-use/`, `/important-notices/`, `/all-site-pages/` (HTML site map), 404
- **No photo-credits page.** All photos are CC0 / public domain; `validate.py` fails if one appears or is linked.

URL slugs, copy, layout, palette and fonts were chosen to differ from every sister `*insuranceappraiser*` site
(checked against all 27 on the Agency account and in this repo). `validate.py` bans every sister-state name
(plus Texas and Colorado) across pages, sitemap, robots, CSS, JS, manifest and `contact.php`.

## Design

- Palette: flag red `#BF0A30` (primary), sun gold `#FFD700` (accent/buttons), deep red `#5E0718`/`#33040D`,
  light tint `#FFF6CC`/`#FFFBEA`, complementary turquoise `#127C80`, sand `#F6F0E4` and charcoal `#1F1A17` neutrals.
- Fonts: **Unbounded** (display) + **DM Sans** (text) — not used by any sister site.
- Squared corners, stepped "terrace" dividers, full-bleed photo hero with a solid lead-form card, gold peril band,
  photo cards with hover zoom, horizontally scrolling region cards, a horizontal process stepper that fills on
  scroll (vertical on mobile), animated counters, staggered reveals, hero/page-hero parallax, header that turns
  solid on scroll, back-to-top button. No progress bar, marquee, 3D tilt or tabs. All motion respects
  `prefers-reduced-motion`; reveals only hide content when JS runs (`html.no-js` is removed by `app.js`).
- Mobile nav: off-canvas drawer (`#drawer`) rendered **outside** the sticky header (the header has no
  `backdrop-filter`), accordion submenus, scroll lock, close on ×/overlay/link/Escape, `inert` + `aria-hidden`,
  shadow/visibility only while open. Fixed mobile call bar.
- Logo mark: red tile, gold stepped roofline and sun disc (deliberately not the Zia symbol). `favicon.svg`,
  `favicon.ico` (16/32/48, bolder art), 96px PNG, full-bleed 180px apple-touch icon, maskable 192/512 PNGs in
  `site.webmanifest`; every icon link has `?v=`. OG image: 1200×630 JPG from a site photo.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` would skip any redirect, so
  `http://www.…/page/` would load with a 200.
- Therefore the homepage is `home.html` and **every other page is `dir/index.php`** whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP.
  There is no root `index.html` and no `dir/index.html` anywhere (`build.py` asserts this, `validate.py` checks it).
- `_guard.php` 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://newmexicoinsuranceappraiser.com` on the real domain only; 301s `/dir/index.php` and `/index.php` to the
  directory; sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL); 404s if requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs without a
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Root static `.html` files allowed: `home.html`, `404.html` and the Search Console file only.
- Hostinger serves its own Googlebot-blocking `robots.txt` on `*.hostingersite.com` preview URLs; that's expected.

## Google Search Console verification file

- File: `public/googlecccfbf2f7e9e5ae4.html`, written by `build.py` (`GSC_FILE` / `GSC_BODY`) on every build.
- Exact contents (one line, no newline, no HTML, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- It must stay at the site root permanently: Google rechecks it, and removing it unverifies the URL-prefix
  property `https://newmexicoinsuranceappraiser.com/`. It's excluded from page checks, `sitemap.xml`, the HTML site
  map and internal links, `robots.txt` doesn't block it, and `validate.py` checks it is byte-exact. The host serves
  it directly, so the guard doesn't run for it (expected).

## Photos (internal record — not published on the site)

All photos are **CC0 or public domain only** (no CC BY), found via the Openverse API (`license=cc0,pdm`) and
Wikimedia Commons (license filtered to public domain / CC0). Each is saved as 1200px and 640px WebP
(`static/assets/img/photos/<key>.webp` and `<key>-640.webp`) with `srcset`, `sizes`, width and height. Decorative
backgrounds use `alt=""`. The source URL, creator and license of every photo are in `src/photos.json`; the table
below mirrors it.

| Key | License | Source | Original |
| --- | --- | --- | --- |
| `abq-skyline` | Public domain | wikimedia-commons | [Downtown Albuquerque, New Mexico (31780770537).jpg](https://commons.wikimedia.org/wiki/File:Downtown_Albuquerque,_New_Mexico_(31780770537).jpg) |
| `calculator` | CC0 1.0 | stocksnap | [Accounting Finance](https://stocksnap.io/photo/accounting-finance-JONMP7TPGK) |
| `carlsbad-caverns` | CC0 1.0 | openverse/flickr | [Carlsbad Caverns Natural Entrance](https://www.flickr.com/photos/27784370@N05/16212008651) |
| `clipboard` | CC0 1.0 | stocksnap | [Construction Plans](https://stocksnap.io/photo/construction-plans-69YZFGFBSY) |
| `commercial-center` | CC0 1.0 | stocksnap | [Buildings Architecture](https://stocksnap.io/photo/buildings-architecture-XHNZ9PZ1IM) |
| `consultation` | CC0 1.0 | stocksnap | [Business Meeting](https://stocksnap.io/photo/business-meeting-SKBXLJOILI) |
| `dust-storm` | CC0 1.0 | openverse/flickr | [Dust Storms](https://www.flickr.com/photos/27784370@N05/12068809836) |
| `farmington` | Public domain | wikimedia-commons | [2015-08-14 DurangoFarmington 148 (21262719622).jpg](https://commons.wikimedia.org/wiki/File:2015-08-14_DurangoFarmington_148_(21262719622).jpg) |
| `flat-roof` | Public domain | wikimedia-commons | [Flat roof (1).jpg](https://commons.wikimedia.org/wiki/File:Flat_roof_(1).jpg) |
| `hail-hand` | CC0 1.0 | wikimedia-commons | [Kroupy.jpg](https://commons.wikimedia.org/wiki/File:Kroupy.jpg) |
| `hail-stones` | CC0 1.0 | wikimedia-commons | [Hail on the Docks, Port Edward, British Columbia.jpg](https://commons.wikimedia.org/wiki/File:Hail_on_the_Docks,_Port_Edward,_British_Columbia.jpg) |
| `hero-adobe-home` | CC0 1.0 | openverse/rawpixel | [Old-style adobe building adorned hot-pepper](https://www.rawpixel.com/image/8042649/photo-image-plant-art-mountains) |
| `house-fire` | CC0 1.0 | rawpixel | [Burning house](https://www.rawpixel.com/image/5918064/burning-house-free-public-domain-cc0-photo) |
| `lightning` | Public domain | wikimedia-commons | [Lightning3.jpg](https://commons.wikimedia.org/wiki/File:Lightning3.jpg) |
| `living-room` | CC0 1.0 | stocksnap | [House Interior](https://stocksnap.io/photo/house-interior-WDVIQZEXML) |
| `los-alamos` | Public domain | wikimedia-commons | [NRCSNM02089 - New Mexico (5463)(NRCS Photo Gallery).jpg](https://commons.wikimedia.org/wiki/File:NRCSNM02089_-_New_Mexico_(5463)(NRCS_Photo_Gallery).jpg) |
| `metal-roof` | CC0 1.0 | openverse/wikimedia | [Rubber roof shingle 04](https://commons.wikimedia.org/w/index.php?curid=143615048) |
| `office-building` | CC0 1.0 | stocksnap | [Office Building](https://stocksnap.io/photo/office-building-7HRFNYC7GU) |
| `oilfield` | Public domain | wikimedia-commons | [Oil pump Talara Peru.JPG](https://commons.wikimedia.org/wiki/File:Oil_pump_Talara_Peru.JPG) |
| `organ-mountains` | Public domain | wikimedia-commons | [A walking trail with a view of the Organ Mountains at Dripping Springs](https://commons.wikimedia.org/wiki/File:A_walking_trail_with_a_view_of_the_Organ_Mountains_at_Dripping_Springs_Natural_Area_east_of_Las_Cruces,_NM_(0031d05b-07fe-4538-94fb-6fae0eecb26d).JPG) |
| `paperwork` | CC0 1.0 | stocksnap | [Calculator Calendar](https://stocksnap.io/photo/calculator-calendar-RFVHCUGML3) |
| `plains-farm` | Public Domain Mark | openverse/flickr | [ATSF Alco PA-1s power for Train #76, The California Special on ready t](https://www.flickr.com/photos/129679309@N05/22071680463) |
| `rio-grande` | CC0 1.0 | wikimedia-commons | [Sunset Sandias Bosque (31865031022).jpg](https://commons.wikimedia.org/wiki/File:Sunset_Sandias_Bosque_(31865031022).jpg) |
| `roof-shingles` | CC0 1.0 | openverse/wikimedia | [Rubber roof shingle 05](https://commons.wikimedia.org/w/index.php?curid=143615050) |
| `roofer` | CC0 1.0 | stocksnap | [Construction Zone](https://stocksnap.io/photo/construction-zone-6EAB6C3900) |
| `ruidoso-pines` | Public domain | wikimedia-commons | [Billy the Kid Trail - Downtown Ruidoso - NARA - 7717320.jpg](https://commons.wikimedia.org/wiki/File:Billy_the_Kid_Trail_-_Downtown_Ruidoso_-_NARA_-_7717320.jpg) |
| `sandia-mountains` | Public domain | wikimedia-commons | [Albuquerque Sandia Mountains (49879402773).jpg](https://commons.wikimedia.org/wiki/File:Albuquerque_Sandia_Mountains_(49879402773).jpg) |
| `santa-fe-adobe` | Public domain | wikimedia-commons | [AN ADOBE HOUSE, IN SANTA FE, NEW MEXICO, CONVERTED TO SOLAR ENERGY HEA](https://commons.wikimedia.org/wiki/File:AN_ADOBE_HOUSE,_IN_SANTA_FE,_NEW_MEXICO,_CONVERTED_TO_SOLAR_ENERGY_HEATING._INSIDE_THE_GLASS-COVERED_ROOF_PANELS..._-_NARA_-_555286.jpg) |
| `storm-desert` | Public Domain Mark | openverse/flickr | [JUL 24 Lightning](https://www.flickr.com/photos/165415395@N07/51284172000) |
| `storm-plains` | Public domain | wikimedia-commons | [Chaparral Supercell 2.JPG](https://commons.wikimedia.org/wiki/File:Chaparral_Supercell_2.JPG) |
| `stucco-home` | CC0 1.0 | wikimedia-commons | [Employee Housing, Spruce Tree Point, Mesa Verde National Park, Mancos,](https://commons.wikimedia.org/wiki/File:Employee_Housing,_Spruce_Tree_Point,_Mesa_Verde_National_Park,_Mancos,_CO_-_27224105047.jpg) |
| `stucco-wall` | CC0 1.0 | openverse/flickr | [mustard-colored stucco wall](https://www.flickr.com/photos/136594255@N06/28722496325) |
| `water-ceiling` | CC0 1.0 | stocksnap | [Raining Raindrops](https://stocksnap.io/photo/raining-raindrops-3AKFOCTZEQ) |
| `wildfire-burned` | Public domain | wikimedia-commons | [FEMA - 33566 - The burned landscape of California.jpg](https://commons.wikimedia.org/wiki/File:FEMA_-_33566_-_The_burned_landscape_of_California.jpg) |
| `wildfire-night` | Public domain | wikimedia-commons | [Calf Canyon Fire 2022 05 03-13.54.08.312-CDT.jpg](https://commons.wikimedia.org/wiki/File:Calf_Canyon_Fire_2022_05_03-13.54.08.312-CDT.jpg) |
| `wildfire-smoke` | Public domain | wikimedia-commons | [Calf Canyon Hermits Peak Fire Apr 29 2022.jpg](https://commons.wikimedia.org/wiki/File:Calf_Canyon_Hermits_Peak_Fire_Apr_29_2022.jpg) |

## Contact form

`/api/contact.php`: honeypot (`website`), per-IP rate limit (5 per 10 minutes), validation (name, email or phone,
consent). Sends through `info@newmexicoinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (starts with `<?php http_response_code(404); exit; ?>`, so it 404s if requested).

The config is **never committed** (`_private/` is in `.gitignore`). Hostinger's file API can't write outside
`public_html`, so it lives at `public_html/api/_private/config.php`:

```php
<?php
if (!defined('NMIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@newmexicoinsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives: upload the config (keep any local copy outside the repo and delete it after),
confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and confirm
the log line shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique
- Meta description present, **110–143 characters**, ends with a full sentence, unique; `og:description` and
  `twitter:description` identical to it
- Exactly one H1, first heading is the H1, no skipped heading levels (footer, sidebar boxes and tools included)
- Valid JSON-LD; one page node (WebPage/AboutPage/ContactPage/CollectionPage) per graph with `breadcrumb`,
  `primaryImageOfPage` and `mainEntity`; ProfessionalService and WebSite present; every `@id` reference resolves
- No broken internal links or anchors, `alt` on every image
- Homepage main content contains "New Mexico Insurance Appraiser" at least 14 times
- No sister-state names, no photo-credits page or link
- Every `dir/index.php` starts with the guard line and has no other PHP; no `index.html` pages
- Search Console file present and byte-exact, and not in the sitemap

## Going live

1. Point the domain's nameservers to `orbit.dns-parking.com` and `horizon.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Verify the www/http/index.php redirects on the live domain, that the real domain sends no `X-Robots-Tag`,
   and that every sitemap URL returns 200. If a www URL returns 200 with `x-hcdn-cache-status: HIT`, clear the cache.
4. In Search Console, verify the **URL-prefix** property `https://newmexicoinsuranceappraiser.com/` (HTML-file
   verification doesn't work for Domain properties), then submit `/sitemap.xml`.
