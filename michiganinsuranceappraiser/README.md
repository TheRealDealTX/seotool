# michiganinsuranceappraiser.com — Michigan Insurance Appraiser

Static site generator + deploy kit for **Michigan Insurance Appraiser**, an independent insurance appraisal,
estimate review and umpire practice serving all 83 Michigan counties. Engineering is derived from the
`georgiainsuranceappraiser/` template (generator, `validate.py`, `deploy.sh`, `api/contact.php`, tool logic,
favicon/photo pipelines, canonical-host guard). Content, URL slugs and design are new and specific to this site.

## Hosting

| Item | Value |
| --- | --- |
| Domain | `michiganinsuranceappraiser.com` (attached at creation) |
| Hostinger website UID | `FH8r2crE9` (Agency Growth, order `1008744732`, php-fpm, PHP 8.3) |
| Preview URL | https://premium-teal-squirrel-38.hostingersite.com |
| Nameservers to set at the registrar | `hermes.dns-parking.com`, `artemis.dns-parking.com` |
| Server | requested the Boston datacenter; the API reports the site on `us-phx-h5g-node3.hstgr.io` (IP `72.60.128.114`) |
| DNS / SSL | live since 2026-11-18; certificate covers `michiganinsuranceappraiser.com` and `www.michiganinsuranceappraiser.com` (expires 2027-02-15, auto-renewed by Hostinger) |
| Google Tag Manager | `GTM-MNMHPK67`, owner-supplied snippet used verbatim |
| Form delivery | SMTP via `info@michiganinsuranceappraiser.com`, verified with a labelled test submission (`"via":"smtp"`) |

Go-live checks (2026-11-18): `http://`, `http://www.` and `https://www.` versions of the homepage and four interior pages
all 301 to `https://michiganinsuranceappraiser.com/...`; `/page/index.php` 301s to `/page/`; all 51 sitemap URLs return 200
with no `X-Robots-Tag`; our own `robots.txt` is served; the Search Console file returns 200, byte-identical, with no
`X-Robots-Tag`; `/api/_private/config.php` returns 404 with 0 bytes. Hostinger serves its own Googlebot-blocking `robots.txt` on preview hosts; that's expected. Our guard also
sends `X-Robots-Tag: noindex, nofollow` on every host that isn't the real domain.

### Why pages are `dir/index.php` (the guard setup)

The Agency host **ignores `.htaccess`**, has **no "force HTTPS" switch** and **serves real files directly without running
the root `index.php`**. A static `dir/index.html` page would therefore skip any redirect in the front controller, and
`http://www.michiganinsuranceappraiser.com/any-page/` would load with a 200. So:

- The homepage is rendered as `home.html` (served by the front controller); **there is no root `index.html`**.
- Every other page is `dir/index.php`. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by plain static HTML (no other PHP).
  `validate.py` fails the build if any page lacks that line, contains another `<?`, or if any `index.html` exists.
- `_guard.php` (generated):
  - 301s `www.` and plain `http` (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://michiganinsuranceappraiser.com`, **only on the real domain**;
  - 301s `/dir/index.php` (and `/index.php`) to `/dir/`;
  - sends `X-Robots-Tag: noindex, nofollow` on any other host (preview URLs);
  - returns 404 when requested directly.
- `index.php` (generated front controller) requires the same guard, serves `home.html` for `/`, 301s directory URLs
  missing a trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- The only static `.html` files at the root are `home.html`, `404.html` and the Search Console file.

Test the guard locally with the host-mimicking router:

```sh
php -S 127.0.0.1:8099 -t public tools/router.php
curl -sI -H 'Host: www.michiganinsuranceappraiser.com' http://127.0.0.1:8099/mi-claim-calculators/            # 301 -> https://michiganinsuranceappraiser.com/mi-claim-calculators/
curl -sI -H 'Host: michiganinsuranceappraiser.com' -H 'X-Forwarded-Proto: http' http://127.0.0.1:8099/mi-claim-calculators/   # 301
curl -sI -H 'Host: michiganinsuranceappraiser.com' -H 'X-Forwarded-Proto: https' http://127.0.0.1:8099/mi-claim-calculators/index.php   # 301 -> /mi-claim-calculators/
```

### Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents (one line, no trailing newline, no HTML, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it byte-for-byte on every build from the `GSC_FILE` / `GSC_BODY` constants, so a rebuild never drops it.
  `validate.py` checks the bytes, keeps it out of page checks, `sitemap.xml`, the HTML site map and internal links, and
  fails if `robots.txt` blocks it.
- It's a real file, so the host serves it directly and the guard doesn't run for it (no redirect, no `X-Robots-Tag`).
- **Keep it on the server permanently.** Google rechecks it; deleting it unverifies the property. HTML-file verification works
  only for the **URL-prefix** property `https://michiganinsuranceappraiser.com/` (a Domain property needs a DNS TXT record).

## Build & deploy

```sh
python3 tools/make_icons.py   # only after changing the mark or the OG photo
python3 build.py              # writes ./public
python3 validate.py           # must print OK (zero errors)
```

Deploy `public/` with the TUS uploader. Get fresh credentials from the Hostinger API call
`agency-hosting_files_generate-upload-url` (website_uid `FH8r2crE9`); they expire after a few hours.

```sh
export MIA_FB_URL='https://…/tus'  MIA_FB_AUTH='…'  MIA_FB_REST='…'
./deploy.sh
```

Then clear the cache (`agency-hosting_cache_clear-website`). `deploy.sh` only adds and overwrites. If a page is removed or
renamed, delete its old file on the server: `DELETE {url-without-/tus}/resources/public_html/<path>` with the same
`X-Auth` and `X-Auth-Rest` headers. Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Site structure (52 pages: 51 in `sitemap.xml` + the 404)

| Section | URL | Count |
| --- | --- | --- |
| Home | `/` | 1 |
| Services | `/michigan-claim-appraisal/` + 12 service pages | 13 |
| Cities | `/mi-cities-served/` + `/mi-cities-served/<city>-insurance-appraiser/` | 13 |
| Free calculators | `/mi-claim-calculators/` + 7 tools | 8 |
| Resources | `/michigan-appraisal-process/`, `/michigan-appraisal-questions/`, `/insurance-claim-terms/` | 3 |
| Guides | `/great-lakes-claim-guides/` + 6 articles | 7 |
| Company & legal | `/about-our-appraisers/`, `/request-claim-review/`, `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/all-pages/` | 6 |
| Errors | `404.html` (real 404 via the front controller) | 1 |

There is **no Photo Credits page** and nothing links to one: every photo is CC0 or public domain.

Source files: `build.py` (layout, schema, pages), `src/services.py`, `src/locations.py`, `src/learn.py` (process guide,
FAQ, glossary, guides), `src/tools.py` (tool markup), `src/photos.json` (photo manifest), `static/` (CSS, JS, icons,
photos, `api/contact.php`), `tools/make_icons.py`, `tools/router.php`.

### Tools (all run in the browser; nothing is stored)

Claim gap & fee estimator · RCV/ACV holdback calculator · Roof squares & pitch calculator (with eave ice-barrier rows) ·
Percentage deductible calculator · Claim deadline planner (general Michigan one-year suit limitation with notice-to-denial
tolling, `.ics` export) · Appraisal readiness score · Ice dam risk & repair cost estimator (Michigan-specific).

## Design

- Palette: Michigan blue `#00274C` (deep `#00182F`, mid `#0E3B67`), maize `#FFCB05` (deep `#E3B300`, tint `#FFF6D1`),
  ice-blue tint `#EEF3F8`, complementary ember accent `#D4552E` (used sparingly for warnings), neutrals `#122030` / `#566474` / `#FBFBF8`.
- Fonts (Google Fonts): **Sofia Sans Condensed** (display) + **Atkinson Hyperlegible** (body); neither is used by a sister site.
- Mark: twin roof peaks forming an "M" in maize over a white estimate line on a blue tile (`static/favicon.svg`).
  `make_icons.py` builds `favicon.ico` (16/32/48, bolder strokes), 96px PNG, full-bleed 180px apple-touch icon,
  maskable 192/512 PNGs in `site.webmanifest`, and the 1200×630 OG image. Every icon link carries `?v=`.
- Effects: header turns solid navy (with a maize rule) on scroll, slow hero zoom, staggered reveals, animated counters,
  hover zoom on photo cards, region tabs with photos, a process timeline that fills as you scroll, a scroll-snap tool rail,
  parallax CTA and a back-to-top button. `prefers-reduced-motion` disables motion; without JS everything renders
  (reveals visible, all region panels shown, header solid, timeline filled).
- Mobile: off-canvas drawer **outside** the fixed header (no `backdrop-filter` anywhere), accordion submenus, scroll lock,
  closes with ×, overlay tap, link tap or Escape, `inert`/`aria-hidden` handling, and its shadow/visibility applied only
  while open. Fixed call bar at the bottom.

## SEO rules (enforced by `validate.py`)

- Titles ≤ 60 characters and ≈ ≤ 580px (Arial metrics at 20px); unique.
- Meta descriptions **110–143 characters** (under 144), hand-written per page, ending with a full sentence; unique;
  `og:description` and `twitter:description` must match.
- Exactly one H1, first heading is the H1, no skipped heading levels (footer, sidebar boxes and tools included).
- Valid JSON-LD where every `@id` reference resolves: ProfessionalService (logo, contactPoint, MI address region,
  areaServed state + cities, OfferCatalog), WebSite, one page node (WebPage/AboutPage/ContactPage/CollectionPage) linked
  to its BreadcrumbList, primaryImageOfPage and mainEntity, plus Service, FAQPage, ItemList, WebApplication,
  BlogPosting, HowTo and DefinedTermSet where they apply.
- Canonical to `https://michiganinsuranceappraiser.com/...`, Open Graph (with image size and alt), Twitter card, `geo.region`.
- No broken internal links or anchors; every image has `alt`.
- Homepage: "Michigan Insurance Appraiser" at least **14 times in main content** (currently 16).
- No sister-state names anywhere in the build (banned-word list in `validate.py`).
- Every `dir/index.php` starts with the guard line and contains no other PHP; no `index.html` anywhere.

## Contact form

`api/contact.php`: honeypot, per-IP rate limit (5 per 10 minutes), validation. It sends through
`info@michiganinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (`"via":"smtp"` when SMTP succeeded).

Both private files return 404 when requested directly: the config starts with a defines-guard and the log starts with a
`<?php http_response_code(404); exit; ?>` header. They live inside `public_html` because Hostinger's file API can't write
outside it. **Never commit credentials**: `_private/` is in `.gitignore`. Config format (upload it, then delete any local copy):

```php
<?php defined('MIA_CONFIG_OK') or (http_response_code(404) and exit);
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465, 'smtp_user' => 'info@michiganinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Status: the config was uploaded on 2026-11-18 (local copy deleted), `/api/_private/config.php` returns 404 with 0 bytes, and a
submission labelled as a test was logged with `"via":"smtp"`. To read the log, download
`public_html/api/_private/leads.log.php` with the file API (`GET {url-without-/tus}/raw/public_html/api/_private/leads.log.php`).
If the mailbox password changes, upload a new config the same way.

## Google Tag Manager

`GTM_ID` in `build.py` is set to `GTM-MNMHPK67`, and `GTM_HEAD_SNIPPET` holds the owner-supplied head snippet exactly as given
(output right after `<meta charset>`); the `<noscript>` iframe for the same ID is output right after `<body>`. Set `GTM_ID = ""`
to remove both.

## Photos (internal record — not published on the site)

All photos are **CC0 or public domain** (Openverse `license=cc0,pdm`), so no attribution is required and the site has
no credits page. Each is saved as 1200px and 640px WebP with `srcset`/`sizes` and width/height. Rawpixel's clean
download rendition is 1024px wide (its larger rendition is watermarked), so those files were scaled to 1200px. StockSnap's
full-size download sits behind a bot check, so no StockSnap files are used. Wikimedia was fetched one file at a time
with pauses and backoff at its standard thumbnail widths. The manifest with source URL, landing page, creator and
license for every file is `src/photos.json`; summary:

| Key | Source | License | Creator | Original |
| --- | --- | --- | --- | --- |
| `apartment-block` | rawpixel | CC0 | — | [Free apartment building image](https://www.rawpixel.com/image/5926811/photo-image-public-domain-windows-white) |
| `calculator` | rawpixel | CC0 | — | [Free calculator working desk image](https://www.rawpixel.com/image/5912338/image-background-public-domain-note) |
| `calculator-papers` | rawpixel | CC0 | — | [Office Calculator](https://www.rawpixel.com/image/5917036/office-calculator-free-public-domain-cc0-image) |
| `city-ann-arbor` | rawpixel | CC0 | — | [city-ann-arbor](https://www.rawpixel.com/image/5951579/free-public-domain-cc0-photo) |
| `city-dearborn` | rawpixel | CC0 | Carol M Highsmith | [Aerial view Detroit, Michigan, skyline](https://www.rawpixel.com/image/8071787/photo-image-public-domain-united-states-skyline) |
| `city-grand-rapids` | rawpixel | CC0 | Carol M Highsmith | [Lake Michigan February Weko Beach](https://www.rawpixel.com/image/3091358/free-photo-image-america-beautiful-blue-sky) |
| `city-marquette` | rawpixel | CC0 | — | [Sunrise Lake Superior Black Rocks](https://www.rawpixel.com/image/5966014/photo-image-light-public-domain-nature) |
| `city-traverse-city` | rawpixel | CC0 | Carol M Highsmith | [Seul Choix Point Lighthouse MIchigan's](https://www.rawpixel.com/image/595037/carol-highsmiths-michigan-photograph) |
| `clipboard` | rawpixel | CC0 | — | [clipboard](https://www.rawpixel.com/image/5942959/free-public-domain-cc0-photo) |
| `detroit-skyline` | wikimedia | CC0 | TheWxResearcher | [Detroit Skyline from Windsor 2025-09-01](https://commons.wikimedia.org/w/index.php?curid=174169194) |
| `flood-street` | rawpixel | CC0 | — | [stop sign stands flooded street](https://www.rawpixel.com/image/8723819/photo-image-border-public-domain) |
| `flooded-basement` | flickr | PDM | NRCS Montana | [Floods32.tif](https://www.flickr.com/photos/160831427@N06/37971533465) |
| `handshake` | rawpixel | CC0 | — | [Free hand shaking business meeting](https://www.rawpixel.com/image/5926299/photo-image-public-domain-hand-person) |
| `hero-home` | rawpixel | CC0 | — | [Suburban housing, real estate](https://www.rawpixel.com/image/6023013/photo-image-public-domain-house-free) |
| `house-fire` | rawpixel | CC0 | — | [Burning house](https://www.rawpixel.com/image/5918064/burning-house-free-public-domain-cc0-photo) |
| `ice-storm-tree` | rawpixel | CC0 | — | [ice-storm-tree](https://www.rawpixel.com/image/5945908/free-public-domain-cc0-photo) |
| `icicles` | wordpress | CC0 | Tinjure20 | [Roof gutter snow icicles against the sun](https://wordpress.org/photos/photo/928622e651/) |
| `lansing-capitol` | rawpixel | CC0 | Carol M Highsmith | [Michigan state capitol Lansing dusk](https://www.rawpixel.com/image/3091337/free-photo-image-america-architecture-blue-sky) |
| `lightning` | rawpixel | CC0 | — | [Thunderstorm lightning night sky photo](https://www.rawpixel.com/image/5904840/photo-image-public-domain-nature-free) |
| `living-room` | rawpixel | CC0 | Scott Webb | [White simple living room interior](https://www.rawpixel.com/image/430394/free-photo-image-living-room-interior-house) |
| `mackinac-bridge` | flickr | PDM | U.S. Fish and Wildlife Service - Midwest Region | [The Mackinac Bridge](https://www.flickr.com/photos/49208525@N08/27163805468) |
| `meeting` | rawpixel | CC0 | — | [Team meeting. View](https://www.rawpixel.com/image/8812100/photo-image-laptop-people-business) |
| `meeting-table` | rawpixel | CC0 | — | [Free close two people hands](https://www.rawpixel.com/image/5927609/photo-image-background-public-domain-hands) |
| `office-tower` | rawpixel | CC0 | Carol M Highsmith | [General Motors Technical Center Building](https://www.rawpixel.com/image/595027/carol-highsmiths-michigan-photograph) |
| `paperwork` | rawpixel | CC0 | — | [paperwork](https://www.rawpixel.com/image/5958827/free-public-domain-cc0-photo) |
| `roof-shingles` | rawpixel | CC0 | — | [Roof texture pattern](https://www.rawpixel.com/image/6019604/photo-image-texture-public-domain-wooden) |
| `roofers` | rawpixel | CC0 | — | [Free men fixing roof image](https://www.rawpixel.com/image/5925457/photo-image-public-domain-house-person) |
| `snow-roofs` | rawpixel | CC0 | — | [cabin woods winter snow roof](https://www.rawpixel.com/image/3296963/free-photo-image-blizzard-building-cabin) |
| `storm-sky` | rawpixel | CC0 | — | [Storm Clouds Sky](https://www.rawpixel.com/image/5968472/storm-clouds-sky) |
| `suburban-home` | rawpixel | CC0 | — | [Free suburban house winter photo](https://www.rawpixel.com/image/5913696/image-public-domain-house-interior) |
| `tornado-damage` | rawpixel | CC0 | — | [Oklahoma County, OK, May 24](https://www.rawpixel.com/image/8717902/photo-image-public-domain-home) |
| `winter-street` | wordpress | CC0 | Tinjure20 | [A street view of houses with snow covered roofs an](https://wordpress.org/photos/photo/78561fadfd/) |

32 photos in total. Regenerate a file with the same key to replace it; keep `src/photos.json` in sync.
