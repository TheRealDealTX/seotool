# californiainsuranceappraiser.com — static site

California Insurance Appraiser: a static site with no database and no plugins. It is built by a
Python generator (standard library only) and served by a tiny PHP front controller plus a
canonical-host guard on a Hostinger Agency Growth website. Engineering is adapted from the
Georgia template; content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `fsNH7cfZ4` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain (attached at creation) | `californiainsuranceappraiser.com` — live; nameservers pointed Nov 17, 2026; SSL covers the apex and `www.` (reissued Nov 17, 2026) |
| Preview URL | https://lawngreen-clam-940848.hostingersite.com (Hostinger serves its own Googlebot-blocking robots.txt here; every page also sends `X-Robots-Tag: noindex, nofollow` off-domain) |
| Nameservers to set at the registrar | `pixel.dns-parking.com`, `byte.dns-parking.com` |
| Server | `us-phx-h5g-node3.hstgr.io`, IPv4 72.60.128.114 |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@californiainsuranceappraiser.com — form delivers over authenticated SMTP (verified with a labeled test submission, log shows `"via":"smtp"`) |
| Google Tag Manager | `GTM-KRLKWZKJ` — head snippet exactly as provided (`GTM_HEAD` in `build.py`) + `<noscript>` iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages + hand-written meta descriptions (`LOC_DESC`) |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide (8 steps), grouped FAQ, 41-term glossary, 6 guide articles |
| `src/photos.py`, `src/photos.json` | Photo alt text, page mappings, and the internal source/license manifest |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `make_icons.py` | Favicon / app icon / OG image pipeline (Pillow) |
| `dev/router.php` | Local router that mimics the host, for `php -S` testing |
| `public/` | **Build output** — what gets deployed (committed) |
| `validate.py` | Post-build checks (must exit 0) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` (TUS) |

## Build, test, deploy

```sh
python3 build.py && python3 validate.py
cd public && php -S 127.0.0.1:8099 ../dev/router.php      # local preview that behaves like the host
```

Deploy (credentials from `agency-hosting_files_generate-upload-url`, website_uid `fsNH7cfZ4`; they expire after a few hours):

```sh
export CIA_FB_URL='https://…/api/tus' CIA_FB_AUTH='…' CIA_FB_REST='…'
./deploy.sh                      # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server:
`DELETE {CIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` / `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` was deleted after the first deploy. No `photo-credits/` files were ever uploaded.

Icons/OG: `python3 make_icons.py BodoniModa.ttf Jost.ttf` (TTFs from Google Fonts; falls back to DejaVu). Bump `FAV` in `build.py` and `make_icons.py` when icons change.

## Pages (51 in sitemap, 52 HTML pages with the 404)

- Home `/`, About `/about-the-firm/`, Contact `/get-in-touch/`
- `/disputed-claim-services/` + 12 services (appraisal clause representation, homeowner, commercial & HOA, roof (tile/shingle),
  Santa Ana/Diablo wind, atmospheric river & storm, water leak, fire/smoke/ash, **wildfire total loss** (the state peril), contents,
  estimate review, umpire)
- `/city-coverage/` + 12 cities at `/city-coverage/<city>-insurance-appraiser/`: Los Angeles, San Diego, San Jose, San Francisco,
  Sacramento, Fresno, Santa Rosa, Oakland, Riverside, Irvine, Ventura, Chico
- `/claim-check-tools/` + 7 tools: appraisal payoff estimator (gap + fees), ACV & holdback calculator, roof area & pitch calculator
  (tile/shingle/shake/membrane counts), earthquake (percentage) deductible calculator, California claim timeline builder (.ics export,
  declared-emergency toggle), appraisal readiness check, rebuild cost & underinsurance check (new, wildfire-specific)
- `/the-appraisal-process/`, `/appraisal-questions/` (grouped FAQ), `/claim-terms-defined/` (searchable, 41 terms), `/appraisal-playbook/` + 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/all-pages/` (HTML site map), `404.html` (real 404 status)
- **No photo credits page.** All photos are CC0 / public domain.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly** (executing a
  directory's `index.php`) — only `/` and unknown paths reach the root `index.php`. A static `dir/index.html` would therefore skip
  any redirect logic, and `http://www.<domain>/page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML containing no other PHP.
  The homepage is `home.html` (served by `index.php`). There is **no root `index.html` and never a `dir/index.html`**;
  `validate.py` fails the build if one appears.
- `_guard.php`: 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://californiainsuranceappraiser.com`
  only on the real domain; 301s `/dir/index.php` (and `/index.php`) to `/dir/`; sends `X-Robots-Tag: noindex, nofollow` on any other
  host (the preview URL); returns 404 when requested directly.
- `index.php` front controller: requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.
- Verified locally with `dev/router.php` (www and http → 301 to `https://californiainsuranceappraiser.com/city-coverage/fresno-insurance-appraiser/`,
  `/…/index.php` → 301 to `/…/`) and on the preview (all 51 sitemap URLs 200 + noindex, missing page 404, no-slash URL 301).

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Contents, exactly one line, no newline, no HTML, no BOM:
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it on every build from the `GSC_FILE` / `GSC_BODY` constants, so a rebuild never drops it. `validate.py`
  checks the exact bytes, skips it in page checks, and fails if it is linked, listed in `sitemap.xml` or blocked in `robots.txt`.
- It is a real file, so the host serves it directly and the guard doesn't run for it (expected).
- It must stay at the root **permanently**: Google rechecks it, and removing it unverifies the property. Verification works only for a
  **URL-prefix** property `https://californiainsuranceappraiser.com/` (a Domain property needs a DNS TXT record).

## Design

- Palette from the brand colors: copper `#B58150` (light `#E2B07E`, tint `#F6ECE1`), crimson `#BA0C2F` (deep `#7D0820`,
  darkest `#4A0613`), complementary teal accent `#1F6F72`, neutrals ink `#1F1613`, espresso `#1D1310`, cream `#FBF7F2`.
- Fonts: **Bodoni Moda** (display) + **Jost** (text) — a pairing no sister site uses.
- Layout: full-bleed photo hero with a 3-field lead form; ledger stat band; photo cards; a crimson wildfire feature band;
  horizontal process timeline that fills on scroll; a horizontally scrolling region rail; comparison table (appraisal vs CDI
  complaint vs mediation vs attorney); interior photo heroes; two-column interior with a sticky sidebar.
- Effects: header turns solid on scroll, slow hero zoom, staggered reveals, animated counters, card image hover zoom, timeline fill,
  parallax CTA, back-to-top. (No progress bar, marquee, tilt or region tabs, to differ from the template.) All honor
  `prefers-reduced-motion`; the page renders fully without JavaScript.
- Mobile: off-canvas drawer **outside** the sticky header (no `backdrop-filter`), accordion submenus, scroll lock, closes on ×,
  overlay, link tap or Escape, `inert`/`aria-hidden` toggled, shadow/visibility only while open. Fixed bottom call bar.
- Brand mark: crimson tile, copper roofline over two white bars ("a fair valuation"). Same SVG in header, drawer and footer; the brand
  link never changes color on hover. Icons: `favicon.svg`, `favicon.ico` (16/32/48, bolder mark), 96px PNG, full-bleed 180px
  apple-touch-icon, maskable 192/512 in `site.webmanifest`, all with `?v=1`. OG image 1200×630 JPG from the hero photo.

## Photos (internal record — not published on the site)

38 photos, all **CC0 1.0 or public domain** (no attribution required, so there is no credits page). Found via the Openverse API
(`license=cc0,pdm`), downloaded one at a time with pauses; Wikimedia via 1280px thumbnails. Each is served as 1200px (or the source
width if smaller, mostly 1024px Flickr/960px StockSnap) and 640px WebP with `srcset`/`sizes` and width/height. Hero/background
photos use `alt=""`; content photos have descriptive alt text. Full metadata (title, creator, license, source page, download URL,
Openverse id) is in `src/photos.json`.

| Key | Title | Creator | License | Source | Source page |
| --- | --- | --- | --- | --- | --- |
| `hero-home` | Kosy Knook Court | TheCatalyst31 | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=33256502 |
| `wildfire-ruins` | 171212-F-BP133-136.jpg | Forest Service Photography | Public domain mark | flickr | https://www.flickr.com/photos/140082569@N07/28206733859 |
| `wildfire-hills` | Fire and smoke from the June 2015 Lake Fire above Yucca Valley as viewed from Covington Flats | Joshua Tree National Park | Public domain mark | flickr | https://www.flickr.com/photos/115357548@N08/19197957859 |
| `smoke-home` | 20130821-FS-LSC-1817 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/9629104439 |
| `foothill-home` | 20130821-FS-LSC-1758 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/9629102217 |
| `smoke-plume` | Smoke plume Lateral West Fire | U. S. Fish and Wildlife Service - Northeast Region | Public domain mark | flickr | https://www.flickr.com/photos/43322816@N08/6044720607 |
| `tarp-roof` | Temporary roof repairs | USFWS/Southeast | Public domain mark | flickr | https://www.flickr.com/photos/41464593@N02/36807005454 |
| `roof-tile` | Ranger Roofing of Oklahoma - Emergency Roof Repair | jpoyter | Public domain mark | flickr | https://www.flickr.com/photos/150150080@N04/34824178772 |
| `roof-aerial` | Rubber roof shingle 03 | Wikideas1 | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=143615044 |
| `roof-crew` | Roof repair on refuge residence | USFWS/Southeast | Public domain mark | flickr | https://www.flickr.com/photos/41464593@N02/37177142902 |
| `palms-wind` | Palm Trees Background | Image Catalog | CC0 1.0 | flickr | https://www.flickr.com/photos/132795455@N08/22798015370 |
| `storm-clouds` | Storm clouds over the Peaks (HDR) | deborah.soltesz | CC0 1.0 | flickr | https://www.flickr.com/photos/10836653@N05/3575369599 |
| `fallen-tree` | Fallen Trees | U.S. Fish & Wildlife Service Southwest Region | Public domain mark | flickr | https://www.flickr.com/photos/51896441@N04/37330421606 |
| `water-ceiling` | 20220127-RD-LSC-0527 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/51868728476 |
| `quake-chimney` | House of Cards | U.S. Geological Survey | CC0 1.0 | flickr | https://www.flickr.com/photos/27784370@N05/16476128909 |
| `la-skyline` | Los Angeles Skyline; August 30, 2022 | ItzAPotato2009 | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=157019541 |
| `sd-skyline` | San Diego Skyline - Point Loma Harborview Road View 36-edited | ryanwschwark | Public domain mark | flickr | https://www.flickr.com/photos/193963407@N02/54864244186 |
| `sf-victorians` | 2015-10-01_15-53-24_USA_San_Francisco_K_JH | Juhele_CZ | CC0 1.0 | flickr | https://www.flickr.com/photos/96541566@N06/52997739639 |
| `sacramento-capitol` | File:California Capitol, Sacramento, California.jpg | Alex Wild | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=30429706 |
| `san-jose-house` | Thomas Fallon house, San Jose, California - DSC03797 | Daderot | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=18347185 |
| `oakland-view` | View of Oakland, California and tree on hill from Oakland Zoo | D Coetzee | CC0 1.0 | flickr | https://www.flickr.com/photos/29507259@N02/10526409583 |
| `fresno-building` | 2309 Tulare Avenue Fresno California 02 | Jengod | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=171842042 |
| `riverside-inn` | International Rotunda, Mission Inn (Riverside, California) | Davestolte | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=150862558 |
| `chico-building` | United States Post Office - Chico, California - DSC03042 | Daderot | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=37388999 |
| `burned-trees` | 2015 Butte Fire Effects | blmcalifornia | Public domain mark | flickr | https://www.flickr.com/photos/50976304@N07/28704575532 |
| `consult` | Business Man | Direct Media | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-man-XTVALHTBUK |
| `clipboard-site` | Business Man | Direct Media | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-man-SZCQC1QEW1 |
| `paper-writing` | Paperwork Desk | Matt Moloney | CC0 1.0 | stocksnap | https://stocksnap.io/photo/paperwork-desk-3YJOHX53SQ |
| `contractor` | BSEE Inspects New Appomattox Platform | bseegov | Public domain mark | flickr | https://www.flickr.com/photos/123443813@N05/41186909981 |
| `calculator` | Calculator Numbers | Martin Vorel | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-VVXW9WBTB8 |
| `calc-paper` | Calculator | motazabdelazeem صور من الوطن | Public domain mark | flickr | https://www.flickr.com/photos/91352576@N06/24217746621 |
| `clipboard` | Office Work | Ch%E2u%20Th%F4ng%20Phan | CC0 1.0 | stocksnap | https://stocksnap.io/photo/office-work-UP9J4EZYNJ |
| `kitchen` | Free modern kitchen interior image | — | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5912749/image-public-domain-kitchen-interior |
| `living-room` | Free minimalist living room interior | — | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5927318/photo-image-public-domain-minimalist-house |
| `office` | Office Building | Open Grid Scheduler / Grid Engine | CC0 1.0 | flickr | https://www.flickr.com/photos/29155878@N03/26118317213 |
| `condo` | HCM00580 | Community Archives of Belleville & Hastings County | CC0 1.0 | flickr | https://www.flickr.com/photos/134017397@N03/43509473371 |
| `demolition` | 20120106-OC-AMW-0047 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/6862190228 |
| `hillside-homes` | 65 Kenneth Hahn State Recreation Area (65) - Christine's Point (2) - Hillside Homes | The Fun Chronicles | CC0 1.0 | flickr | https://www.flickr.com/photos/196406308@N04/55194756645 |

## SEO rules enforced by `validate.py`

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique.
- Meta description **110–143 characters** (under 144), unique, ends with a full sentence, and identical `og:description` /
  `twitter:description`. Applies to every page including the 404. Current range: 117–143.
- Exactly one H1, first heading is the H1, no skipped heading levels (footer, sidebar boxes and tool widgets included).
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/CollectionPage) linked to its
  BreadcrumbList, primaryImageOfPage and mainEntity; graph always holds ProfessionalService (logo, contactPoint, CA region/country,
  state + 12 cities as areaServed, OfferCatalog) and WebSite. Plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo
  and DefinedTermSet where they apply.
- Canonical to `https://californiainsuranceappraiser.com/...`, Open Graph (image size + alt), Twitter card, `geo.region`.
- No broken internal links or anchors; `alt` on every image; sitemap URLs all resolve.
- Homepage main content must contain "California Insurance Appraiser" at least 14 times (currently 21).
- No sister-state names anywhere in the build (all 37 sister states, word-boundary match), no `photo-credits` references.
- Every `dir/index.php` starts with the guard line and has no other PHP; no `index.html` anywhere; only `404.html`, `home.html` and
  the Search Console file as root `.html`.

## Contact form

`/api/contact.php`: POST only, honeypot (`website`), 5 submissions per IP per 10 minutes, validation (name; a valid email or a
phone with ≥7 digits; consent). It sends through `info@californiainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (created with a `<?php http_response_code(404); exit; ?>` header). Both private files return 404 when
requested directly. They live inside `public_html` because Hostinger's file API can't write outside it.

**Never commit credentials** (`_private/` and `*-config.php` are git-ignored). When the mailbox password arrives, upload
`public_html/api/_private/config.php`:

```php
<?php
if (!defined('CIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@californiainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then: confirm the config URL returns 404 with 0 bytes, send one submission labeled as a test, and confirm the log line shows
`"via":"smtp"`. Delete any local copy of the config.

## Going live checklist

1. ~~Point the nameservers~~ — done.
2. ~~SSL on apex and `www.`~~ — the first certificate covered only the apex; reissued with `agency-hosting_ssl_reinstall-website`
   on Nov 17, 2026 and `ssl_cert.names` now lists both.
3. ~~Canonical-host checks on the live domain~~ — `http://`, `http://www.` → 301 to `https://californiainsuranceappraiser.com/<page>/`,
   `/<page>/index.php` → 301 to `/<page>/`, all 51 sitemap URLs 200 with no `X-Robots-Tag`, our robots.txt served, Search Console file
   200 with exact bytes. If a www URL ever returns a cached 200 (`x-hcdn-cache-status: HIT`), clear the cache again.
4. ~~Mailbox + SMTP and GTM~~ — done.
5. In Search Console, verify the URL-prefix property `https://californiainsuranceappraiser.com/`, then submit `/sitemap.xml`.
   Keep `googlecccfbf2f7e9e5ae4.html` on the server permanently.
