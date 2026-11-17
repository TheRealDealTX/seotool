# coloradoinsuranceappraiser.com — static site

Colorado Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served by a tiny PHP front controller on a Hostinger Agency Growth website.
Engineering (generator, validator, deploy script, form handler, tool logic, favicon/photo
pipelines, canonical-host guard) was adapted from the Georgia template; content, URL slugs and
design are new and differ from every sister state site.

| | |
| --- | --- |
| Hostinger website UID | `Y6aPtGE0b` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | https://coloradoinsuranceappraiser.com (attached at creation) |
| Preview URL | https://storied-darksalmon-crow-87.hostingersite.com |
| Nameservers to set at the registrar | `helios.dns-parking.com`, `aster.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@coloradoinsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Colorado city pages |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, FAQ by topic, glossary (42 terms), 6 guides |
| `src/photos.json` | Photo manifest: alt text, source URL, landing page, creator, license (internal record only) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `tools/fetch_photos.py` | Downloads manifest photos → 1200px + 640px WebP |
| `tools/make_icons.py` | Favicon set, apple-touch, maskable icons, manifest, 1200×630 OG image |
| `public/` | **Build output** — what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` via the TUS API |

## Build & deploy

```sh
python3 tools/fetch_photos.py     # only when photos change
python3 tools/make_icons.py       # only when the mark or hero photo changes
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid Y6aPtGE0b)
export CIA_FB_URL='…' CIA_FB_AUTH='…' CIA_FB_REST='…'
./deploy.sh                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the
server: `DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` /
`X-Auth-Rest` headers.

Local preview that mimics the host: `php -S localhost:8000 -t public tools/router.php`. The router
serves real files directly, runs a directory's `index.php`, and sends everything else to `/index.php`
(it isn't deployed).

## Pages (51 in sitemap, plus the 404)

- Home, `/about-us/`, `/contact-us/`
- `/colorado-claim-appraisal/` + 11 services (appraisal clause representation, homeowner, commercial & HOA,
  hail & roof, wind & tornado, snow load & ice dam, water & burst pipe, fire & smoke, wildfire,
  carrier estimate review, umpire)
- `/colorado-service-areas/` + 12 cities: Denver, Colorado Springs, Aurora, Fort Collins, Boulder, Lakewood,
  Pueblo, Greeley, Longmont, Castle Rock, Grand Junction, Durango
- `/claim-planning-tools/` + 7 tools: award gap & fee estimator, RCV/ACV holdback, roof pitch & squares
  (plane by plane), hail percentage deductible, claim timeline builder (.ics export), appraisal file
  readiness check (Yes/Partly/No), hail size & roof impact checker (Colorado-specific)
- `/resources/` hub, `/resources/appraisal-process/`, `/resources/faq/`, `/resources/glossary/`,
  `/resources/guides/` + 6 guides
- `/privacy/`, `/terms/`, `/disclaimer/`, `/html-sitemap/`, `404.html` (real 404 status)
- No photo credits page (all photos are CC0/public domain).

## Design

- Palette from `#002868`: deep `#001a45` / `#000f2b`, mid `#22488f`, light tint `#e8eef8` / `#f4f7fc`,
  one complementary accent (aspen gold `#f2a900`), granite neutrals (`#0e1a2f`, `#2b3546`, `#5a6577`, `#d8dfea`).
- Fonts: **Raleway** (display) + **Atkinson Hyperlegible** (body) — no sister site uses either.
- Mountain-ridge SVG dividers under heroes and above the footer; full-bleed photo hero with a white lead
  card; offset stats band; sticky-heading service list with photo thumbnails; region tabs; parallax
  "Hail Alley" band with the quick gap check; horizontal process timeline that fills on scroll; photo
  cards for tools, cities and guides; parallax CTA; two-column interiors with a sticky sidebar.
- Effects: scroll progress bar, header solid on scroll, hero slow zoom, staggered reveals, counters,
  hover zoom, region tabs, filling timeline, parallax bands, back-to-top. No marquee or 3D tilt.
  All motion respects `prefers-reduced-motion`; pages render fully without JavaScript.
- Mobile: off-canvas drawer rendered outside the sticky header (accordion submenus, scroll lock, closes on ×,
  overlay, link tap or Escape, `inert`/`aria-hidden`, shadow only while open) plus a fixed call bar.
- Logo: navy tile, gold sun, twin white peaks. Same SVG in header, drawer and footer; favicon.ico (16/32/48,
  bolder glyph), 96px PNG, 180px full-bleed apple-touch, maskable 192/512 in `site.webmanifest`, `?v=` busters.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` would bypass any redirect, so:
  - every page is written as `dir/index.php` whose first line is
    `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML (no other PHP);
  - the homepage is `home.html`, served by the front controller; there is no root `index.html`;
  - the only root `.html` files are `home.html`, `404.html` and the Search Console file.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://coloradoinsuranceappraiser.com` (real domain only), 301s `/dir/index.php` → `/dir/`, sends
  `X-Robots-Tag: noindex, nofollow` on any other host (the preview domain), and 404s when requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, adds trailing slashes, includes `dir/index.php`
  for directory URLs that reach it, and returns `404.html` with a real 404.
- Hostinger serves its own Googlebot-blocking `robots.txt` on the preview domain; that's expected.

## Google Search Console verification

`googlecccfbf2f7e9e5ae4.html` is written at the site root on every build (constant `GSC_BODY` in
`build.py`). Its exact contents — one line, no newline, no HTML:

```
google-site-verification: googlecccfbf2f7e9e5ae4.html
```

It must stay at the root permanently: Google rechecks it, and removing it unverifies the property. It is
excluded from page checks, the sitemaps and internal links; `validate.py` checks its bytes. HTML-file
verification works only for the **URL-prefix** property `https://coloradoinsuranceappraiser.com/`.

## Photos

All photos are **CC0 or public domain only** (no attribution required; no public credits page), found via
the Openverse API (`license=cc0,pdm`) from StockSnap, rawpixel, Flickr CC0/PDM and U.S. government
sources. Each is served as 1200px and 640px WebP with `srcset`/`sizes` and width/height. The source URL,
landing page, creator and license of every photo are recorded in `src/photos.json` and listed below for
our records.

| Key | Title | Creator | License | Source |
| --- | --- | --- | --- | --- |
| `hero` | snow covered log cabin forest | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/3299325/free-photo-image-log-cabin-house-cabins) |
| `denver` | Downtown Denver skyline | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/3338734/free-photo-image-architecture-asphalt-building) |
| `cosprings` | View Rocky Mountains, Colorado USA | Carol M Highsmith | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/434345/free-photo-image-landscape-america-americas-public-domain) |
| `aurora` | Simple home exterior design photo | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5912682/image-public-domain-house-home) |
| `fortcollins` | Horsetooth Reservoir | rootbeer667788 | CC0 1.0 | [flickr](https://www.flickr.com/photos/188344895@N02/52470624654) |
| `boulder` | Aerial8 | cuboulder | CC0 1.0 | [flickr](https://www.flickr.com/photos/38587132@N02/23928920228) |
| `lakewood` | Storm clouds | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/3372029/free-photo-image-asphalt-cc0-cloud) |
| `pueblo` | Pueblo, Colorado, trainyards. Original image | Carol M Highsmith | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/434304/free-photo-image-bridge-train-carol-highsmith) |
| `longmont` | Longs Peak | Thomson20192 | CC0 1.0 | [flickr](https://www.flickr.com/photos/93558439@N05/28251303182) |
| `castlerock` | Modern house, real estate | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/6040724/photo-image-public-domain-house-home) |
| `gj` | Scenery Colorado National Monument, USA | Carol M Highsmith | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/434314/free-photo-image-carol-highsmith-tourism-america) |
| `durango` | Durango & Silverton Narrow Gauge | Carol M Highsmith | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/434301/free-photo-image-america-americas-public-domain-carol-highsmith) |
| `plains` | Supercell thunderstorm | NOAA NSSL | Public domain (PDM) | [flickr](https://www.flickr.com/photos/47838549@N08/48044614641) |
| `mtntown` | Cabins laden heavy snow outside | Carol M Highsmith | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/582523/carol-highsmiths-colorado-photograph) |
| `hail` | Nebraska Supercell thunderstorm | NOAA NSSL | Public domain (PDM) | [flickr](https://www.flickr.com/photos/47838549@N08/48044614771) |
| `cta` | Lightning Tornado | Lucy Chian | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/lightning-tornado-9WTNHBFJUX) |
| `roofer` | untitled | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5942657/free-public-domain-cc0-photo) |
| `clipboard` | Checklist Goals | Glenn Carstens-Peters | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/checklist-goals-TBJ9OPDGMK) |
| `inspect` | construction worker goes plans site | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5928035/photo-image-public-domain-hands-person) |
| `calc` | Calculator Numbers | Martin Vorel | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/calculator-numbers-VVXW9WBTB8) |
| `calc2` | Calculator Numbers | Negative Space | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD) |
| `meeting` | Free business meeting image | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5904074/photo-image-public-domain-people-office) |
| `meeting2` | Business Meeting | Direct Media | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/business-meeting-SSKSJIBMMP) |
| `consult` | Business Meeting | Christina Morillo | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/business-meeting-SKBXLJOILI) |
| `interior` | Housing improvement project goal 1: two-bedroom unit, living room | YellowstoneNPS | Public domain (PDM) | [flickr](https://www.flickr.com/photos/80223459@N05/52067485855) |
| `office` | Office Building | Open Grid Scheduler / Grid Engine | CC0 1.0 | [flickr](https://www.flickr.com/photos/29155878@N03/26930332206) |
| `townhomes` | Townhouses | Open Grid Scheduler / Grid Engine | CC0 1.0 | [flickr](https://www.flickr.com/photos/29155878@N03/40643717184) |
| `hailroof` | 20220127-RD-LSC-0692 | USDAgov | Public domain (PDM) | [flickr](https://www.flickr.com/photos/41284017@N08/51867761912) |
| `wind` | Project Vortex-99: Occluded mesocyclone tornado (NOAA/unidentified fotog) | pingnews.com | Public domain (PDM) | [flickr](https://www.flickr.com/photos/39735679@N00/452392668) |
| `water` | 171012-O-JA419-247 | USDAgov | Public domain (PDM) | [flickr](https://www.flickr.com/photos/41284017@N08/23949764608) |
| `burned` | Burning house | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5918064/burning-house-free-public-domain-cc0-photo) |
| `wildfire` | Wild Cow Fire | National Interagency Fire Center | Public domain (PDM) | [flickr](https://www.flickr.com/photos/165415395@N07/51285917069) |
| `review` | Business Document | Daria Nepriakhina | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/business-document-AB4F938C85) |
| `shingles` | House Roof | Oliur Rahman | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/house-roof-KJMQM11A8G) |
| `home` | Suburban housing, real estate | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/6023013/photo-image-public-domain-house-free) |
| `snowroof` | Free suburban house winter photo | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5913696/image-public-domain-house-interior) |
| `icicles` | Closeup icicles roof | unknown | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/6018207/photo-image-public-domain-nature-ice) |

## SEO rules enforced by `validate.py`

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique titles
- Meta description **110–143 characters**, unique, ends with a complete sentence, identical to
  `og:description` and `twitter:description`
- Exactly one H1, first heading is H1, no skipped heading levels (footer, sidebars and tools included)
- Canonical URL on every page; valid JSON-LD with ProfessionalService, WebSite, one page node linked to its
  BreadcrumbList, primary image and main entity; every `@id` reference resolves
- No broken internal links or anchors, `alt` on every image, no photo-credits links
- Homepage main content mentions "Colorado Insurance Appraiser" ≥ 14 times
- No sister-state names anywhere in the build
- Every `dir/index.php` starts with the guard line and contains no other PHP; no `index.html` pages
- Search Console file present with exact bytes; sitemap entries all exist

## Contact form

`/api/contact.php` has a honeypot, a per-IP rate limit (5 per 10 minutes) and validation. It sends through
`info@coloradoinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php`. Both private files 404 when requested directly (config: defines-guard;
log: `<?php http_response_code(404); exit; ?>` header). They live in `public_html` because the file API
can't write outside it. **Never commit credentials** — `_private/` is git-ignored. Config format:

```php
<?php
if (!defined('CIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@coloradoinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading: confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test,
and confirm the log shows `"via":"smtp"`.

## Going-live checklist

1. Point the domain's nameservers to `helios.dns-parking.com` / `aster.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check the www/http redirects and `/page/index.php` redirects on the live domain; clear the CDN cache if a
   stale `x-hcdn-cache-status: HIT` appears.
4. Create the mailbox, upload `api/_private/config.php`, test the form.
5. Verify the URL-prefix property in Search Console, then submit `/sitemap.xml`.
