# washingtoninsuranceappraiser.com — static site

Washington Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it,
and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.
The engineering (generator, validator, deploy script, form handler, tool logic, guard) started from
`georgiainsuranceappraiser/`. The content, URL slugs, design, palette and fonts are new and differ from every
sister `*insuranceappraiser*` site.

| | |
| --- | --- |
| Hostinger website UID | `BijEtYhpF` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | https://washingtoninsuranceappraiser.com: live, SSL covers the apex and `www` (www/http 301 to the apex) |
| Preview URL | https://mediumblue-grouse-262565.hostingersite.com |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@washingtoninsuranceappraiser.com |
| Google Tag Manager | `GTM-NSVPS7XM`: the owner's snippet in `<head>` exactly as provided, plus the noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, robots, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages (county, neighborhoods, storm history, housing mix, hand-written meta descriptions) |
| `src/tools.py` | 7 calculators (markup + copy). Logic is in `static/assets/js/app.js` |
| `src/learn.py` | Process guide, grouped FAQ, 41-term glossary, 6 guide articles |
| `src/photos.json` | Photo manifest: alt text, output size, source URL, landing page, creator, license (internal record only) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output** that gets deployed (committed) |
| `validate.py` | Post-build checks (must report 0 errors) |
| `deploy.sh` | Uploads `public/` to `public_html` over TUS. `--delete <path>` removes old server files |
| `tools/` | `photos.py` (photo pipeline), `make_icons.py`, `make_og.js`, `router.php` (local host mimic), `qa.js`, `shots.js` |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh creds: Hostinger API agency-hosting_files_generate-upload-url (website_uid BijEtYhpF)
export WIA_FB_URL='https://…/tus' WIA_FB_AUTH='…' WIA_FB_REST='…'
./deploy.sh                       # only adds/overwrites
./deploy.sh --delete old/index.php # remove a renamed or deleted page on the server
# then clear the cache: agency-hosting_cache_clear-website
```

Local preview that behaves like the host (real files served directly, a directory's `index.php` executed,
everything else through the root `index.php`):

```sh
php -S 127.0.0.1:8099 -t public tools/router.php
node tools/qa.js http://127.0.0.1:8099      # calculator math, drawer, logo hover, overflow
node tools/shots.js http://127.0.0.1:8099 /tmp/shots
```

## Pages (51 in sitemap + 404)

- Home, About (`/about-washington-insurance-appraiser/`), Contact (`/talk-to-an-appraiser/`)
- `/insurance-appraisal-services/` + 12 services: appraisal clause representation, homeowner, condo/HOA/commercial,
  roof & hail, windstorm & tornado, fallen tree, water & rain intrusion, fire & smoke, wildfire & ash,
  snow/ice dam/freeze, carrier estimate review, neutral umpire. No hurricane page, since Washington has no hurricane exposure.
- `/cities-we-serve/` + 12 cities: Seattle, Spokane, Tacoma, Vancouver, Bellevue, Everett, Olympia, Bellingham,
  Yakima, Tri-Cities, Wenatchee, Bremerton
- `/free-claim-calculators/` + 7 tools: appraisal payoff (gap + fees), replacement cost holdback (RCV/ACV),
  roof pitch & squares, percentage deductible (earthquake/wind/hail), claim timeline planner (.ics export),
  appraisal readiness quiz, **wildfire total-loss coverage check** (new, Washington-specific)
- `/claim-resources/` (index) + 6 guides, `/how-insurance-appraisal-works/` (HowTo), `/claim-appraisal-faq/`,
  `/claim-appraisal-glossary/` (searchable, 41 terms)
- `/your-privacy-rights/`, `/terms-for-using-this-site/`, `/disclaimers-and-limits/`, `/browse-every-page/` (HTML site map), `404.html`
- **No photo credits page.** Every photo is CC0 or public domain, so no attribution is needed.

Every URL path was checked against all sister-site sitemaps in this repo: there is no overlap except `/`.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` would skip any redirect, so
  `http://www.…/any-page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP.
  The homepage is `home.html`, served by the front controller. There is no root `index.html` and never a `dir/index.html`.
- `_guard.php` (generated):
  - on the real domain only, 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to `https://washingtoninsuranceappraiser.com`
  - 301s `/dir/index.php` and `/index.php` to the directory URL
  - sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL)
  - returns 404 when requested directly
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, adds the trailing slash on
  directories, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- `deploy.sh` only adds and overwrites. Delete removed or renamed files on the server with `./deploy.sh --delete <path>`.
- Hostinger serves its own Googlebot-blocking `robots.txt` on `*.hostingersite.com` preview URLs. That's expected:
  our own `robots.txt` is served on the real domain.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Contents, exactly, as one line with no newline, wrapper, guard, GTM or BOM:
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- The generator writes it on every build (`GSC_FILE`/`GSC_BODY` constants in `build.py`), so a rebuild never drops it.
  `validate.py` checks the bytes and keeps it out of the page checks, `sitemap.xml`, the HTML site map and internal links.
- It is a real file, so the host serves it directly and the guard does not run for it. That's expected.
- **It must stay at the root permanently.** Google re-checks it, and removing it unverifies the property.
  Verify the **URL-prefix** property `https://washingtoninsuranceappraiser.com/` (HTML-file verification doesn't work
  for Domain properties), then submit `https://washingtoninsuranceappraiser.com/sitemap.xml`.

## Design

- Emerald `#008457` (deep `#00432c`, ink `#002a1c`, tint `#e6f3ee`), yellow `#FFD520`, coral accent `#e8613c`, warm neutrals.
- Fonts: **Gabarito** (display) and **Libre Franklin** (body). Neither is used by any sister site.
- Full-bleed photo hero with a slow zoom-out and a lead form card, an overlapping yellow counter band, a horizontal peril rail
  (scroll-snap with prev/next buttons), photo cards with hover zoom, a Westside/Eastside split, a scroll-filled vertical
  process timeline, a parallax CTA photo, staggered reveals, a scroll progress bar, a header that turns solid on scroll,
  and a back-to-top button. All motion respects `prefers-reduced-motion`, and the page renders fully without JavaScript.
- Interior pages: photo hero with breadcrumbs, and a two-column layout with a sticky sidebar (call box + related links).
- Mobile: an off-canvas drawer **outside** the sticky header, with accordion submenus, scroll lock, close on ×, overlay,
  link or Escape, `inert`/`aria-hidden` handling, and shadow/visibility only while open. Fixed mobile call bar.
- The brand link's color comes from a CSS variable, so hover never changes it in the header, drawer or footer.
- Icons (`tools/make_icons.py`): white roof chevron over a yellow "W" on an emerald tile. Outputs `favicon.svg`, a 16/32/48
  `favicon.ico` with bolder strokes, a 96px PNG, a full-bleed 180px apple-touch icon, and maskable 192/512 PNGs in
  `site.webmanifest`. Every icon link carries `?v=`.
- OG image: 1200×630 JPG rendered from a site photo by `tools/make_og.js`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique.
- **Meta description 110–143 characters** (under 144), present on every page, unique, ending with a full sentence,
  and identical to `og:description` and `twitter:description`. Every page has its own hand-written description.
- Exactly one H1, which is the first heading; no skipped levels anywhere (footer, sidebar, tools included).
- One JSON-LD `@graph` per page: ProfessionalService (logo ImageObject, contactPoint, addressRegion WA / US,
  state + cities as areaServed, OfferCatalog), WebSite, one page node (WebPage/AboutPage/ContactPage/CollectionPage)
  with `breadcrumb`, `primaryImageOfPage` and `mainEntity`, and a BreadcrumbList. Plus Service, FAQPage, ItemList,
  WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply. Every `@id` reference must resolve.
- Canonical, Open Graph (with image size and alt), Twitter card and `geo.region` on every page.
- No broken internal links or anchors; `alt` on every image.
- Homepage main content must contain "Washington Insurance Appraiser" at least 14 times.
- No sister-state names anywhere in the build (30 states listed in `validate.py`).
- Every `dir/index.php` starts with the guard line at the right depth and contains no other PHP;
  no `index.html` pages; Search Console file bytes exact.

## Contact form

`/api/contact.php` has a honeypot, a per-IP rate limit (5 per 10 minutes) and validation. It sends each lead
from `info@washingtoninsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php`. Both private files live in `public_html` (Hostinger's file API can't write
outside it) and return an empty 404 if requested directly. **Credentials are never committed:**
`_private/` is in `.gitignore`. Keep any local copy of the config outside the repo and delete it after upload.

```php
<?php
if (!defined('WIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@washingtoninsuranceappraiser.com', 'smtp_pass' => '…'];
```

**Status: wired (Nov 14, 2026).** The config is uploaded, both private URLs return 404 with 0 bytes, and one test submission
logged `"via":"smtp"` with no error. To change the password, re-upload the config file (never commit it).

Never put a literal `?>` in a PHP `//` comment in `contact.php`: PHP ends code there, and the rest of the file is sent as text.

## Photos (CC0 / public domain only)

All 30 photos are **CC0 or public domain only**, so no attribution is required and the site has **no public
photo credits page** (don't create `/photo-credits/`). They were found with the Openverse API (`license=cc0,pdm`) from
StockSnap, rawpixel, Flickr CC0/PDM (much of it U.S. government agency work), the WordPress Photo Directory and
Wikimedia Commons. Downloads ran one file at a time with pauses and backoff, using Wikimedia's standard
thumbnail widths (330px for contact sheets, 1280px for finals, with a 960px fallback). Photos with identifiable
political figures, text overlays or artwork were skipped. `tools/photos.py` crops each to 3:2 and writes 1200px
and 640px WebP. Pages use `srcset`/`sizes` and width/height, alt text comes from the manifest, and decorative
backgrounds use `alt=""`. Sub-1200px sources (Flickr's 1024px size) are upscaled with Lanczos so there is one size set.

Internal record (also in `src/photos.json` with title, creator and file URL; not published on the site):

| Key | Source | License | Source page |
| --- | --- | --- | --- |
| `hero-home` | Flickr | CC0 1.0 | https://www.flickr.com/photos/184134070@N08/51872082918 |
| `home-evergreens` | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/5969571/house |
| `storm-sky` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/66741228@N05/50298057333 |
| `fallen-tree-house` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/51896441@N04/37330421606 |
| `tree-down-street` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/80223459@N05/53024932171 |
| `roof-damage` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/41284017@N08/7008298577 |
| `roof-shingles` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/roof-shingle-RIUJONCXNY |
| `roofer-work` | Flickr | CC0 1.0 | https://www.flickr.com/photos/43296902@N00/4363286049 |
| `wildfire-hillside` | Flickr | CC0 1.0 | https://www.flickr.com/photos/27784370@N05/2595333088 |
| `wildfire-smoke` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/80223459@N05/36114718993 |
| `burned-home` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/140082569@N07/43331319204 |
| `snow-house` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/house-winter-O7Y8ZBW5HN |
| `icicles-roof` | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/6018207/photo-image-public-domain-nature-ice |
| `water-damage` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/41284017@N08/51868728476 |
| `house-fire` | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/7433149/photo-image-public-domain-city |
| `commercial-building` | Flickr | CC0 1.0 | https://www.flickr.com/photos/44034762@N04/5321765179 |
| `condo-building` | Flickr | CC0 1.0 | https://www.flickr.com/photos/14674348@N04/14996764996 |
| `consultation-table` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/team-meeting-69TMH4ITIE |
| `paperwork-review` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/paperwork-desk-A5DG6YREVH |
| `calculator-paperwork` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/calculator-numbers-VVXW9WBTB8 |
| `calculator-desk` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD |
| `clipboard-inspection` | StockSnap | CC0 1.0 | https://stocksnap.io/photo/clipboard-desk-VXAISJRBH9 |
| `kitchen` | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/6042580/photo-image-public-domain-house-kitchen |
| `living-room` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/96511847@N04/9202793852 |
| `seattle-skyline` | wordpress | CC0 1.0 | https://wordpress.org/photos/photo/51568ae0ba/ |
| `tacoma` | Wikimedia Commons | CC0 1.0 | https://commons.wikimedia.org/w/index.php?curid=167367676 |
| `olympia-capitol` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/184829900@N06/48956418491 |
| `mount-rainier` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/130826934@N07/29991542286 |
| `columbia-river` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/184134070@N08/51872685165 |
| `wenatchee` | Flickr | Public domain (PDM) | https://www.flickr.com/photos/124469042@N05/42106833025 |

