# southdakotainsuranceappraiser.com — static site

South Dakota Insurance Appraiser: a static site (no database, no CMS) built by a Python generator
and served by a tiny PHP front controller plus a canonical-host guard on a Hostinger Agency Growth website.
The engineering (generator, validator, deploy script, form handler, tool logic, guard) started from
`georgiainsuranceappraiser/`; the copy, URL scheme, design, palette, fonts, photos and homepage structure are new.

| | |
| --- | --- |
| Hostinger website UID | `2FJj5lTsf` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | https://southdakotainsuranceappraiser.com (live; SSL covers the domain and www; www and http 301 to it) |
| Preview URL | https://dimgrey-echidna-626694.hostingersite.com (noindex; Hostinger serves its own robots.txt here) |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@southdakotainsuranceappraiser.com (form delivers over SMTP; verified Nov 14, 2026) |
| Google Tag Manager | `GTM-PG57CVJ6`: the supplied head snippet verbatim (`GTM_HEAD_SNIPPET`) plus the noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 calculators (markup + copy); logic in `static/assets/js/app.js` (`window.SDIA`) |
| `src/learn.py` | Process guide, grouped FAQ, 43-term glossary, 6 articles |
| `src/photo_sources.json` | Internal photo manifest: source URL, landing page, creator, license, alt text |
| `src/photos.json` | Same, plus rendered sizes. Written by `tools/photos.py`, read by `build.py` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output** — this is what gets deployed (committed) |
| `validate.py` | Post-build checks (must exit 0) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |
| `tools/make_icons.py` | Favicon pipeline (SVG, ICO 16/32/48 bold variant, 96px, 180px apple-touch, maskable 192/512) |
| `tools/photos.py` | Photo pipeline (download once, 1200px + 640px WebP, writes `src/photos.json`) |
| `tools/dev_router.php` | Local router that mimics the host for `php -S` |
| `tools/qa.js` | Playwright QA (screenshots, overflow, lazy images, tool math, drawer, logo hover, console) |

## Build, check, deploy

```sh
python3 build.py && python3 validate.py
php -S 127.0.0.1:8080 -t public tools/dev_router.php     # local preview that behaves like the host
node tools/qa.js http://127.0.0.1:8080 /tmp/qa            # browser QA
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 2FJj5lTsf)
export SDIA_FB_URL='https://…/tus' SDIA_FB_AUTH='…' SDIA_FB_REST='…'
./deploy.sh                                               # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server:
`curl -X DELETE -H "X-Auth: $SDIA_FB_AUTH" -H "X-Auth-Rest: $SDIA_FB_REST" "${SDIA_FB_URL%/tus}/resources/public_html/<path>"`.

## Pages (51 in sitemap.xml, plus the 404 page)

- Home, Company profile (`/company-profile/`), Contact (`/get-a-claim-review/`)
- `/appraiser-services/` + 12 services (appraisal clause, homeowner, commercial & HOA, roof & hail, wind/tornado/derecho,
  water, fire & smoke, Black Hills wildfire, blizzard/ice/snow load, farm & ranch buildings, estimate review, umpire).
  No hurricane page: tropical systems don't reach South Dakota, and the services index says so.
- `/cities-we-serve/` + 12 cities (`/cities-we-serve/<city>-appraiser/`): Sioux Falls, Rapid City, Aberdeen, Brookings,
  Watertown, Mitchell, Yankton, Pierre, Huron, Spearfish, Vermillion, Sturgis
- `/policyholder-calculators/` + 7 tools: appraisal payoff estimator (fees + break-even point), depreciation recovery
  calculator, roof squares & slope factor calculator, hail percentage deductible calculator (with a % ladder),
  appraisal calendar builder (.ics export, optional "name your appraiser" date), claim file readiness grader (letter grade),
  coinsurance penalty calculator (the South Dakota-specific tool, for farm/commercial/HOA policies)
- `/inside-the-appraisal-process/`, `/appraisal-questions-answered/`, `/insurance-appraisal-glossary/`,
  `/storm-claim-articles/` + 6 articles
- `/site-privacy/`, `/site-conditions/`, `/appraiser-disclaimer/`, `/page-map/`, `404.html`
- No photo credits page (all photos are CC0 / public domain).

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly** without
  running the root `index.php`. A `dir/index.html` page would therefore skip any redirect, and
  `http://www.southdakotainsuranceappraiser.com/any-page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP.
  The homepage is `home.html`, served by the root `index.php`. There is no root `index.html` and there must never be
  a `dir/index.html` on the server. The only root `.html` files are `home.html`, `404.html` and the Search Console file.
- `_guard.php` (generated): 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://southdakotainsuranceappraiser.com` — only on the real domain; 301s `/dir/index.php` and `/index.php` to the
  directory URL; sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview domain); 404s if requested directly.
- `index.php` (generated) requires the guard, serves `home.html` for `/`, 301s directory URLs without a trailing
  slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.
- `validate.py` checks that every page starts with the guard line at the right depth and contains no other PHP,
  and fails on any `index.html` or stray `.html` file.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents (one line, no newline, no HTML, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it byte-for-byte on every build from the `GSC_FILE`/`GSC_BODY` constants, so a rebuild never drops it.
  It is excluded from page checks, `sitemap.xml`, the HTML page map and internal links; `robots.txt` doesn't block it.
  `validate.py` fails if it is missing or its bytes change.
- It must stay at the root permanently: HTML-file verification works only for the **URL-prefix** property
  `https://southdakotainsuranceappraiser.com/`, and Google rechecks the file — removing it unverifies the property.
  The host serves it directly (the guard doesn't run for real files), which is expected.

## Contact form

`/api/contact.php` has a honeypot, a per-IP limit (5 per 10 minutes) and validation. It sends through
`info@southdakotainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php`. Both private files 404 when requested directly (the config's defines-guard, the log's
`<?php … exit;` header). They live under `public_html` because the file API can't write outside it.
`_private/` is in `.gitignore`. **Never commit credentials**; keep any local copy of the config outside the repo and
delete it after upload. Config format:

```php
<?php
if (!defined('SDIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@southdakotainsuranceappraiser.com', 'smtp_pass' => '…'];
```

The config was uploaded on Nov 14, 2026: `/api/_private/config.php` returns 404 with 0 bytes, and a submission labelled
as a test was logged with `"via":"smtp"`. To change the password, re-upload that file (never commit it).

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique titles
- Meta description 110–143 characters, present, unique, ends with a full sentence, identical to og:description and
  twitter:description
- Exactly one H1, first heading is the H1, no skipped levels anywhere (footer, sidebar boxes and tools included)
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/CollectionPage) linked to
  its BreadcrumbList, primary image and main entity; ProfessionalService has logo, contactPoint, address, areaServed and
  an OfferCatalog
- Canonical on the real domain, Open Graph (with image size and alt), Twitter card and `geo.region` on every page
- No broken internal links or anchors; every image has `alt`; no links to photo credits
- Homepage main content mentions "South Dakota Insurance Appraiser" at least 14 times (currently 20)
- No sister-state names in the output (all 26 sister states; "Missouri River" is whitelisted as real geography)

## Design

- Palette: sky blue `#0074A8` (main), sun gold `#FFC400` (main), deep `#06324A` / `#03202F`, light tint `#E6F3FA`,
  complementary rust `#C9502A` (used sparingly for warnings/"past due"), neutrals ink `#0E1E27`, stone `#F5F3EE`.
- Fonts: Gabarito (display) + Rethink Sans (body) — not used by any sister site.
- Logo: a prairie horizon with a rising sun in a rounded blue square; same mark in header, drawer and footer.
- Homepage order (different from every sister site): full-bleed photo hero with a white lead-form card and a counter
  rail → "three questions" cards → intro with offset-frame photo → 12 poster photo cards → gold quick-gap band →
  horizontal process rail that fills on scroll → East River / West River region tabs with photos → storm history
  ledger (horizontal scroll) → calculator list cards → city lists split by side of the river under a parallax banner →
  "who should be in your corner" cards → two-column FAQ → articles → parallax CTA → contact form.
- Effects: header turns solid on scroll, slow hero zoom, staggered reveal, animated counters, hover zoom on cards,
  scroll-filled process rail, region tabs, parallax banner and CTA, back-to-top button. No progress bar, marquee or
  3D tilt. Everything respects `prefers-reduced-motion`; without JavaScript all content is visible.
- Mobile: off-canvas drawer rendered outside the header (no `backdrop-filter` anywhere), accordion submenus, scroll lock,
  closes on ×, overlay tap, link tap or Escape, `inert`/`aria-hidden` handling, shadow and visibility only while open;
  fixed bottom call bar.

## Photos (internal record — not published on the site)

All photos are **CC0 or public domain** (no attribution required, so there is no credits page), found through the
Openverse API with `license=cc0,pdm`. Flickr originals were fetched at 1600px from the photo page; rawpixel at its
public 1300px rendition. Each is served as 1200px and 640px WebP with `srcset`/`sizes` and width/height.
Wikimedia files were skipped (its robot policy requires contact details in the user agent).

| Key | Subject (alt text) | Source | License | Creator | Size used | Landing page |
| --- | --- | --- | --- | --- | --- | --- |
| `hero-home` | Lone prairie house under dark storm clouds | flickr | Public domain (PDM) | Walter B. Myers | 1200px | https://www.flickr.com/photos/196993038@N02/52952818810 |
| `sioux-falls` | The falls of the Big Sioux River over pink quartzite at Falls Park in Sioux Falls | flickr | CC0 1.0 | U.S. Geological Survey | 1200px | https://www.flickr.com/photos/27784370@N05/20913627122 |
| `rapid-city` | Highway winding through pine forest and granite peaks in the Black Hills near Rapid City | rawpixel | CC0 1.0 | Carol M Highsmith | 1024px | https://www.rawpixel.com/image/8043866/photo-image-public-domain-black-hills |
| `black-hills` | Granite outcrop lit by evening sun above pine forest in the Black Hills | flickr | CC0 1.0 | sbmeaper1 | 1200px | https://www.flickr.com/photos/142289055@N04/50231009132 |
| `badlands` | Banded buttes and grassland in Badlands National Park in western South Dakota | flickr | Public domain (PDM) | National Park Service | 1200px | https://www.flickr.com/photos/42600860@N02/32852214947 |
| `spearfish-canyon` | Aerial view of Spearfish Canyon's cliffs and pine forest in the northern Black Hills | flickr | Public domain (PDM) | Black Hills National Forest | 1200px | https://www.flickr.com/photos/140925193@N05/52212787665 |
| `river-bluffs` | Rolling prairie and river valley in Stanley County, South Dakota | rawpixel | CC0 1.0 | Carol M Highsmith | 1024px | https://www.rawpixel.com/image/8063102/photo-image-public-domain-city-united-states |
| `river-storm` | Low storm clouds over a wide river and flat shoreline | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/8702962859 |
| `lake-sunrise` | Red and orange sunrise over a South Dakota prairie lake | flickr | Public domain (PDM) | USFWS Mountain Prairie | 1200px | https://www.flickr.com/photos/51986662@N05/52474236541 |
| `sturgis-main` | The historic brick Hotel Sturgis building on Main Street in Sturgis | rawpixel | CC0 1.0 | Carol M Highsmith | 1024px | https://www.rawpixel.com/image/8064776/photo-image-public-domain-black-city |
| `storm-sky` | Storm clouds gathering over the banded hills of the Badlands | flickr | CC0 1.0 | exit78 | 1200px | https://www.flickr.com/photos/28826830@N00/5790058047 |
| `prairie-storm` | Supercell thunderstorm with a lowering cloud base over flat farm country | flickr | Public domain (PDM) | NOAA NSSL | 1200px | https://www.flickr.com/photos/47838549@N08/48039373122 |
| `river-flood` | Floodwater covering a riverside park and trees after spring flooding | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/8705322279 |
| `prairie-farm` | Barbed-wire fence along open prairie grassland under a big sky | rawpixel | CC0 1.0 | Carol M Highsmith | 1024px | https://www.rawpixel.com/image/8040305/photo-image-public-domain-united-states |
| `hailstones` | Hailstones scattered across a patio table and chairs after a hailstorm | flickr | CC0 1.0 | catseye1812 | 1200px | https://www.flickr.com/photos/55255025@N06/52564224838 |
| `metal-barn` | Red wooden barn with a steel roof standing in winter snow | flickr | CC0 1.0 | cogdogblog | 1200px | https://www.flickr.com/photos/37996646802@N01/54297820566 |
| `grain-bins` | Steel grain bins and farm sheds on the open plains | flickr | Public domain (PDM) | keystonecops555 | 1200px | https://www.flickr.com/photos/183085050@N02/49159824332 |
| `farm-buildings` | Storm-damaged pole barn with exposed roof framing behind a farm fence | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/51955838181 |
| `roofer` | Roofing crew working on a long garage roof stripped to the decking | flickr | Public domain (PDM) | U. S. Fish and Wildlife Service - Northeast Region | 1200px | https://www.flickr.com/photos/43322816@N08/15871499500 |
| `hail-roof` | Close-up of a damaged roof with a broken section among intact tiles | flickr | Public domain (PDM) | jpoyter | 800px | https://www.flickr.com/photos/150150080@N04/34824178772 |
| `snow-house` | Red house with a roof buried under deep snow among pine trees | rawpixel | CC0 1.0 | unknown | 683px | https://www.rawpixel.com/image/3300517/free-photo-image-snow-abies-building |
| `wildfire` | Wildfire burning across a forested ridge at night above a lake | flickr | Public domain (PDM) | Forest Service Pacific Northwest Region | 1200px | https://www.flickr.com/photos/135886671@N08/53902149761 |
| `shelf-cloud` | Shelf cloud rolling in ahead of a thunderstorm over open water | flickr | CC0 1.0 | otrow_photography | 1200px | https://www.flickr.com/photos/183939796@N07/50772162733 |
| `calculator` | Calculator and pen resting on a page of checked figures | rawpixel | CC0 1.0 | unknown | 1024px | https://www.rawpixel.com/image/5945923/free-public-domain-cc0-photo |
| `office-building` | Single-story retail strip center beside a parking lot | flickr | CC0 1.0 | Lallint | 1200px | https://www.flickr.com/photos/194250376@N05/52111756820 |
| `meeting` | Conference room with a long table and leather chairs | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/6252780514 |
| `estimate-desk` | Hands typing on a laptop spreadsheet beside a notebook and coffee | rawpixel | CC0 1.0 | unknown | 1024px | https://www.rawpixel.com/image/5974308/photo-image-laptop-work-macbook |
| `living-room` | Bright living room with a sofa, armchair and large windows | rawpixel | CC0 1.0 | unknown | 1024px | https://www.rawpixel.com/image/5927318/photo-image-public-domain-minimalist-house |
| `water-ceiling` | Worker repairing damaged drywall in a room under a window | flickr | Public domain (PDM) | USFWS Mountain Prairie | 1200px | https://www.flickr.com/photos/51986662@N05/49525529776 |
| `home-porch` | Farmhouse and trees under gathering storm clouds | flickr | Public domain (PDM) | jessdenman | 1200px | https://www.flickr.com/photos/12811967@N08/5534210176 |
| `house-fire` | Fire-gutted brick building with charred, empty window openings | flickr | Public domain (PDM) | Newcastle Libraries | 800px | https://www.flickr.com/photos/39821974@N06/4083357275 |
| `roof-inspection` | Disaster inspector talking with a homeowner inside a storm-damaged house | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/37132208273 |
| `inspector` | Inspector photographing damaged belongings inside a home | flickr | Public domain (PDM) | USDAgov | 1200px | https://www.flickr.com/photos/41284017@N08/23949763208 |
| `tornado-damage` | Building with its roof covering torn away by strong wind | flickr | CC0 1.0 | Simon_Cotterill | 1200px | https://www.flickr.com/photos/137828720@N06/51711148603 |
| `calendar-desk` | Open calendar planner with handwritten notes | rawpixel | CC0 1.0 | unknown | 1024px | https://www.rawpixel.com/image/3299160/free-photo-image-calendar-time-plan |
| `paperwork` | Pen resting on a printed business document | stocksnap | CC0 1.0 | Daria Nepriakhina | 960px | https://stocksnap.io/photo/business-document-AB4F938C85 |
| `policy-review` | Open planner and pen on a desk, ready for notes | rawpixel | CC0 1.0 | unknown | 1024px | https://www.rawpixel.com/image/5912649/image-paper-book-public-domain |
| `consult-table` | Papers, notebooks and a phone spread across a work desk | flickr | CC0 1.0 | cogdogblog | 1200px | https://www.flickr.com/photos/37996646802@N01/265279980 |
| `lake-home` | Wood cabin with a green roof among trees near a lake | flickr | Public domain (PDM) | LandBetweentheLakesKYTN | 1200px | https://www.flickr.com/photos/82242140@N05/26036012684 |
| `apartments` | Mid-rise apartment building against a blue sky | flickr | CC0 1.0 | DennisM2 | 1200px | https://www.flickr.com/photos/14674348@N04/26401105160 |

Four sources top out below 1200px (hail-roof 800, house-fire 800, snow-house 683/867, paperwork 960); rawpixel files are its clean 1024px version because its larger public renditions are watermarked. These are used where they display smaller or behind overlays.
