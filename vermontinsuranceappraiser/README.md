# vermontinsuranceappraiser.com — static site

Vermont Insurance Appraiser: a static site built by a Python generator and served on a Hostinger
Agency Growth website by a tiny PHP front controller plus a canonical-host guard. No database, no plugins.
Engineering (generator pattern, guard, front controller, contact handler, tool logic, deploy script)
was adapted from the Georgia site; the copy, URL structure, palette, fonts and layout are new.

| | |
| --- | --- |
| Hostinger website UID | `BU6JAuqzl` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter) |
| Domain | `vermontinsuranceappraiser.com` (attached at creation; not resolving until nameservers are set) |
| Preview URL | https://aliceblue-spider-233953.hostingersite.com (Hostinger serves its own noindex `robots.txt` here) |
| Nameservers to set at the registrar | `hermes.dns-parking.com`, `artemis.dns-parking.com` (from `agency-hosting_websites_get`) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@vermontinsuranceappraiser.com (mailbox not created yet) |
| Google Tag Manager | `GTM_ID` in `build.py`, empty for now (no GTM output until set) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 town pages (county, neighborhoods, storm history, housing mix, hand-written meta descriptions) |
| `src/tools.py` | 7 tools (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 steps), grouped FAQ, 40-term glossary, 6 field guides |
| `src/photos.json` | Internal photo manifest: source URL, creator, license, original size. Not published |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` |
| `tools/make_icons.py` | Regenerates favicon set, maskable icons, `site.webmanifest` and `og-image.jpg` |
| `tools/router.php` | Local router that mimics the host (for `php -S` testing) |
| `public/` | **Build output** — what gets deployed (committed) |
| `validate.py` | Post-build checks (must report `OK`) |
| `deploy.sh` | Uploads `public/` to `public_html` over the File Browser TUS API |

## Build & deploy

```sh
python3 tools/make_icons.py      # only when the mark or OG image changes
python3 build.py && python3 validate.py
# fresh creds: agency-hosting_files_generate-upload-url (website_uid BU6JAuqzl)
export VIA_FB_URL='…/api/tus' VIA_FB_AUTH='…' VIA_FB_REST='…'
./deploy.sh                      # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server:
`DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` / `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

Local preview that behaves like the host:

```sh
php -S 127.0.0.1:8080 -t public tools/router.php
curl -sI -H 'Host: www.vermontinsuranceappraiser.com' http://127.0.0.1:8080/vermont-towns/barre/   # 301 to https://vermontinsuranceappraiser.com/vermont-towns/barre/
```

## Pages (51 in sitemap + 404)

- Home, `/our-vermont-practice/` (About), `/claim-review-request/` (Contact)
- `/vt-claim-appraisal/` + 12 services: appraisal clause representation, homeowner, commercial & HOA, roof & hail,
  wind & microburst, tropical storm, water, fire & smoke, ice dam & frozen pipe (state peril), snow load & collapse
  (state peril), estimate review, umpire
- `/vermont-towns/` + 12 towns: Burlington, South Burlington, Rutland, Montpelier, Barre, St. Albans, Brattleboro,
  Bennington, Middlebury, St. Johnsbury, Stowe, Hartford (White River Junction / Quechee)
- `/vermont-claim-tools/` + 7 tools: claim gap & fee estimator (3 scenarios, flat/hourly/percent fees), RCV/ACV holdback
  (optional non-depreciated labor), roof pitch & squares (with ice barrier), percentage deductible, claim deadline calendar
  (.ics export), appraisal readiness check, roof snow load estimator
- `/vermont-appraisal-process/`, `/vermont-claim-questions/`, `/searchable-claim-glossary/`, `/appraisal-field-guides/` + 6 guides
- `/how-we-use-information/` (privacy), `/site-use-terms/`, `/scope-disclaimer/`, `/all-vermont-pages/` (HTML site map), `404.html`

There is **no photo credits page** and nothing links to one; `validate.py` fails if one appears.

## Design

- Palette: forest green `#154734` (deep `#0b2a1f`, ink `#071c14`, tint `#e7f0eb`), gold `#ffcc33` (deep `#d9a400`, soft `#fff4cf`),
  barn-red accent `#a8323e`, warm paper `#fbfaf5` and green-gray neutrals.
- Fonts: **Spectral** (display, incl. italic accents) + **Lato** (body). Neither is used by a sister site.
- Layout: full-bleed photo hero with a white lead card, gold marquee of claim types, an illustrative "ledger" estimate
  comparison, season tabs with photos (winter / mud season / summer / fall), numbered service rows with thumbnails,
  a sticky-heading process timeline that fills as you scroll, four region cards, photo cards for tools, towns and guides,
  parallax CTA. Interior pages: photo hero with breadcrumbs and fact strip, two-column layout with sticky sidebar.
- Effects: scroll progress bar, header that goes from transparent to solid, hero/hero-banner parallax, staggered reveal,
  hover zoom, marquee, season tabs, timeline fill, parallax CTA, back-to-top. No 3D tilt or counters. All motion respects
  `prefers-reduced-motion`; reveal styles only apply under `html.js`, so the page renders fully without JavaScript.
- Mobile nav: off-canvas `#drawer` outside the header (header uses no `backdrop-filter`), accordions, scroll lock, closes on
  ×, overlay, link tap or Escape; `inert`/`aria-hidden` toggled; shadow and visibility only while open. Fixed mobile call bar.
- Mark: green rounded seal, gold ring, gold mountain ridge and a white level line. `favicon.svg`, multi-size `favicon.ico`
  (bolder 16/32/48 variant), 96px PNG, full-bleed 180px apple-touch icon, maskable 192/512 in `site.webmanifest`; links use `?v=1`.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS", serves real files directly and only sends `/` and unknown
  paths to the root `index.php`. A `dir/index.html` would bypass any redirect, so `http://www.…/page/` would load with 200.
- So every page is `dir/index.php` whose first line is `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by
  static HTML with no other PHP. The homepage is `home.html`, served by `index.php`. Never add a root `index.html` or any
  `dir/index.html` (the build asserts this and `validate.py` fails on it).
- `_guard.php`: 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://vermontinsuranceappraiser.com`
  on the real domain only; 301s `/dir/index.php` and `/index.php` to the directory; sends `X-Robots-Tag: noindex, nofollow` on any
  other host (the preview URL); 404s if requested directly.
- `index.php`: requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash, includes
  `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.

## Google Search Console verification file

`googlecccfbf2f7e9e5ae4.html` is written to the site root on every build (`GSC_FILE` / `GSC_BODY` in `build.py`). Its contents are
exactly this single line, with no trailing newline, HTML, guard or GTM:

```
google-site-verification: googlecccfbf2f7e9e5ae4.html
```

It must stay at the root permanently: Google rechecks it, and removing it unverifies the URL-prefix property
`https://vermontinsuranceappraiser.com/`. It is excluded from page checks, `sitemap.xml`, the HTML site map and internal links;
`validate.py` checks its bytes. The host serves it directly, so the guard does not run for it (expected).

## Contact form

`/api/contact.php`: honeypot (`website`), 5 posts per IP per 10 minutes, validation (name, valid email or phone, consent).
It sends through `info@vermontinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to `mail()`, and always appends a JSON line to `api/_private/leads.log.php`
(created with a `<?php http_response_code(404); exit; ?>` header). `_private/` is in `.gitignore`; credentials are never committed.
The Hostinger file API cannot write outside `public_html`, which is why the private files live there. Config file to upload
(keep any local copy outside the repo and delete it after uploading):

```php
<?php
if (!defined('VIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@vermontinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled TEST, and confirm the
log line shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique
- Every page (including 404, legal pages and the site map) has exactly one hand-written meta description, **110–143 characters**,
  unique, ending in a full sentence, identical in `og:description` and `twitter:description` (current range 121–142)
- Exactly one H1, first heading is H1, no skipped levels (footer, sidebar and widgets included)
- Valid JSON-LD with ProfessionalService + WebSite + exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage) linked
  to its BreadcrumbList, primaryImageOfPage and mainEntity; every `@id` reference resolves. Service, FAQPage, ItemList,
  WebApplication, BlogPosting, HowTo and DefinedTermSet appear where they apply
- No broken internal links or anchors; `alt` on every image
- Homepage main content contains "Vermont Insurance Appraiser" ≥ 14 times (currently 16)
- No sister-state names anywhere in the build (all other 49 states; Vermont's own "Washington County" is allowed)
- Every `dir/index.php` starts with the guard at the right depth and has no other PHP; no `index.html` pages; GSC file bytes exact

## Photos (internal record — not published)

All 37 photos are **CC0 1.0 or public domain** (no attribution required), found with the Openverse API (`license=cc0,pdm`),
mostly Flickr public-domain uploads (including USDA Forest Service), StockSnap and rawpixel. Each is saved as 1200px and 640px
WebP in `static/assets/img/photos/` and used with `srcset`/`sizes` and width/height. Several Flickr originals are 1024px wide and
were upscaled slightly to 1200px. Photos are illustrative and do not show client properties.

| Key | Title | Creator | Source | License | Landing page |
| --- | --- | --- | --- | --- | --- |
| `farmhouse-snow` | Old Farmhouse in The Driftless, Mt. Carroll, IL | AJ in Chicagoland | flickr | CC0 1.0 | https://www.flickr.com/photos/190865407@N05/54344896183 |
| `foliage-ridge` | 20241002-FS-GM-BAG-FallFoliage-009 | Forest Service Photography | flickr | Public domain mark | https://www.flickr.com/photos/140082569@N07/54401004325 |
| `foliage-valley` | 20241002-FS-GM-BAG-FallFoliage-011 | Forest Service Photography | flickr | Public domain mark | https://www.flickr.com/photos/140082569@N07/54400813194 |
| `icicles-gutter` | Roof gutter snow icicles against the sun | Tinjure20 | wordpress | CC0 1.0 | https://wordpress.org/photos/photo/928622e651/ |
| `snow-roof-eaves` | A random view snow thickness on roof and icicles formation | Tinjure20 | wordpress | CC0 1.0 | https://wordpress.org/photos/photo/45063bddda/ |
| `snowy-street` | A street view of houses with snow covered roofs and backyard | Tinjure20 | wordpress | CC0 1.0 | https://wordpress.org/photos/photo/78561fadfd/ |
| `victorian-snow` | 2021-024-3-13-1 | Community Archives of Belleville & Hastings County | flickr | CC0 1.0 | https://www.flickr.com/photos/134017397@N03/52179601758 |
| `red-barn-snow` | Barn Roof Day 14/14 | cogdogblog | flickr | CC0 1.0 | https://www.flickr.com/photos/37996646802@N01/54296945642 |
| `white-barn-snow` | White barn in the snow, Coastal Range, Oregon | Bonnie Moreland (free images) | flickr | Public domain mark | https://www.flickr.com/photos/66741228@N05/51808445941 |
| `barn-roof-crew` | Barn Roof Day 6/14 | cogdogblog | flickr | CC0 1.0 | https://www.flickr.com/photos/37996646802@N01/54298055974 |
| `roof-aerial` | New Roof for Arctic Point_Payette NF_Kelly Martin | Intermountain Region US Forest Service | flickr | Public domain mark | https://www.flickr.com/photos/107640324@N05/51798023645 |
| `roof-damage` | Witley Bay - Bingo Hall roof damage | Simon_Cotterill | flickr | CC0 1.0 | https://www.flickr.com/photos/137828720@N06/51711148603 |
| `roofer-ladder` | 20210811-160009LC | Luc Coekaerts from Tessenderlo | flickr | CC0 1.0 | https://www.flickr.com/photos/92947007@N03/51580226349 |
| `shingles` | Roof Shingle | Bernard Spragg | stocksnap | CC0 1.0 | https://stocksnap.io/photo/roof-shingle-RIUJONCXNY |
| `river-flood` | Looking across flooded Arkansas River from Dardanelle | exit78 | flickr | Public domain mark | https://www.flickr.com/photos/28826830@N00/51990325641 |
| `winter-river` | Winter River | Tricia Gray | stocksnap | CC0 1.0 | https://stocksnap.io/photo/winter-river-X3K0FOUD76 |
| `timber-frame` | 20230919-FS-KM-028 | Forest Service Photography | flickr | Public domain mark | https://www.flickr.com/photos/140082569@N07/53215372408 |
| `framing-pipes` | 20230919-FS-KM-024 | Forest Service Photography | flickr | Public domain mark | https://www.flickr.com/photos/140082569@N07/53215065391 |
| `bennington-aerial` | Aerial View of Bennington, VT from Bennington Monument | voyager.annelid | flickr | Public domain mark | https://www.flickr.com/photos/199507919@N07/55274213931 |
| `north-bennington-house` | North Bennington, VT | voyager.annelid | flickr | Public domain mark | https://www.flickr.com/photos/199507919@N07/55274428044 |
| `fairbanks-museum` | 20230919-FS-KM-032 | Forest Service Photography | flickr | Public domain mark | https://www.flickr.com/photos/140082569@N07/53215575365 |
| `covered-bridge` | Foster Bridge, Vermont | ForwardDefensive | flickr | Public domain mark | https://www.flickr.com/photos/78091088@N02/52658095926 |
| `windstorm-trees` | Windstorm and rain at Lake Village on July 4, 2023: fallen t | YellowstoneNPS | flickr | Public domain mark | https://www.flickr.com/photos/80223459@N05/53024932171 |
| `fallen-trees-building` | Windstorm and rain at Lake Village on July 4, 2023: fallen t | YellowstoneNPS | flickr | Public domain mark | https://www.flickr.com/photos/80223459@N05/53025323015 |
| `fire-ladder` | Winsford House Fire | Unknown | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/7433329/photo-image-public-domain-firefighter |
| `burned-house` | Tilstone House Fire | Unknown | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/7433074/photo-image-public-domain-nature |
| `calculator-pencil` | Calculator Numbers | Martin Vorel | stocksnap | CC0 1.0 | https://stocksnap.io/photo/calculator-numbers-VVXW9WBTB8 |
| `calculator-hands` | Calculator Calendar | Tevarak | stocksnap | CC0 1.0 | https://stocksnap.io/photo/calculator-calendar-RFVHCUGML3 |
| `calculator-notebook` | Using Calculator | Alabama Extension | flickr | CC0 1.0 | https://www.flickr.com/photos/184594136@N08/51327975511 |
| `team-meeting` | Team Meeting | Startup Stock Photos | stocksnap | CC0 1.0 | https://stocksnap.io/photo/team-meeting-JBW2PXDOL6 |
| `writing-papers` | Writing Papers | Helloquence | stocksnap | CC0 1.0 | https://stocksnap.io/photo/writing-papers-Y01VDYAX63 |
| `business-document` | Business Document | Daria Nepriakhina | stocksnap | CC0 1.0 | https://stocksnap.io/photo/business-document-AB4F938C85 |
| `condo-building` | Carrollton Condominium/The Carrollton Apartments (1956), 360 | Baltimore Heritage | flickr | CC0 1.0 | https://www.flickr.com/photos/44034762@N04/54132876878 |
| `office-night` | Office Building | Verne Ho | stocksnap | CC0 1.0 | https://stocksnap.io/photo/office-building-7HRFNYC7GU |
| `thunderstorm` | Thunderstorm | Daniel_Koehn | flickr | Public domain mark | https://www.flickr.com/photos/55825136@N02/51367127852 |
| `lightning-houses` | Lightning tonight | Dingus Nugget | flickr | Public domain mark | https://www.flickr.com/photos/185078984@N02/51437890743 |
| `treasury-house` | Treasury Inn, neoclassical home built | Carol M Highsmith | rawpixel | CC0 1.0 | https://www.rawpixel.com/image/8071718/photo-image-public-domain-city-united-states |

## Going live (to do)

1. Point the domain's nameservers to `hermes.dns-parking.com` and `artemis.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`ssl_cert.names`); reissue with `agency-hosting_ssl_reinstall-website` if needed.
3. Check http/www/https-www and `/page/index.php` 301s on the homepage and interior pages; every sitemap URL 200; no
   `X-Robots-Tag` on the real domain; our own `robots.txt`; the GSC file returns 200 with exact bytes.
4. Create the mailbox, upload `api/_private/config.php`, send a test lead, confirm `"via":"smtp"`.
5. Add the GTM container ID to `GTM_ID`, rebuild, validate, redeploy, clear cache.
6. Click Verify in Search Console for the URL-prefix property `https://vermontinsuranceappraiser.com/`, then submit `/sitemap.xml`.
