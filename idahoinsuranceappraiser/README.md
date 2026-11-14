# idahoinsuranceappraiser.com — static site

Idaho Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and a tiny PHP guard plus front controller serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `5v55YjD3F` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | `idahoinsuranceappraiser.com` (attached at creation) |
| Preview URL | https://darkturquoise-cod-820153.hostingersite.com |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@idahoinsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | Not set. `GTM_ID` in `build.py` is empty, so no GTM code is output |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `_guard.php`, `index.php`, GSC file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Idaho location pages |
| `src/tools.py` | 7 interactive tools (markup + copy). Logic is in `static/assets/js/app.js` |
| `src/learn.py` | Process guide, FAQ (grouped), glossary (43 terms), 6 guide articles |
| `src/photos.json` | Photo manifest: alt text, size, title, creator, license, source URL, landing page (internal record) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output** (committed). This folder is what gets deployed |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS upload API |
| `tools/make_icons.js` | Renders the logo mark into favicon.svg/.ico/PNGs (run once; needs Playwright) |
| `tools/process_photos.py` | Originals → 1200px + 640px WebP, writes `src/photos.json` |
| `tools/dev_router.php` | Local router that mimics the host, for redirect tests |

## Build & deploy

```sh
python3 build.py && python3 validate.py
```

Local preview that behaves like the host (real files served directly, a directory's `index.php`
executed, everything else to the front controller):

```sh
php -S 127.0.0.1:8080 -t public tools/dev_router.php
curl -sI -H 'Host: www.idahoinsuranceappraiser.com' http://127.0.0.1:8080/property-claim-appraisal/   # 301 to https://idahoinsuranceappraiser.com/...
```

Deploy (credentials from the Hostinger API call `agency-hosting_files_generate-upload-url` with
`website_uid` `5v55YjD3F`; they expire after a few hours):

```sh
export IIA_FB_URL='https://…/tus'  IIA_FB_AUTH='…'  IIA_FB_REST='…'
./deploy.sh
```

Then clear the cache (`agency-hosting_cache_clear-website`). `deploy.sh` only adds and overwrites.
If a page is removed or renamed, delete the old file on the server with
`DELETE {url-without-/tus}/resources/public_html/<path>` and the same two auth headers.

## Pages (50 in sitemap.xml, plus 404)

- Home, About (`/our-appraisal-approach/`), Contact (`/schedule-a-consult/`)
- `/property-claim-appraisal/` + 11 services: appraisal clause representation, homeowner, commercial/HOA/farm,
  roof & hail, wind & microburst, water & frozen pipe, fire & smoke, wildfire, snow load & ice dam (Idaho peril),
  estimate review, umpire services
- `/idaho-appraisal-areas/` + 12 cities (`/idaho-appraisal-areas/<city>-insurance-appraiser/`): Boise, Meridian,
  Nampa, Caldwell, Eagle, Idaho Falls, Pocatello, Rexburg, Twin Falls, Coeur d’Alene, Lewiston, Ketchum & Sun Valley
- `/policy-math-tools/` + 7 tools: claim gap & net recovery estimator (fees, three landing points, break-even),
  RCV vs. ACV holdback calculator, roof pitch & squares calculator (with carrier comparison), percentage deductible
  calculator (with a 0.5–5% ladder), Idaho claim timeline builder (.ics export), appraisal readiness checkup,
  roof snow load estimator (new, Idaho-specific)
- `/how-the-appraisal-clause-works/` (HowTo), `/idaho-appraisal-questions/` (FAQ by topic), `/claim-terms-defined/`
  (searchable glossary), `/appraisal-know-how/` + 6 guides
- Privacy, Terms, Disclaimer, HTML site directory (`/idaho-site-directory/`), 404 (real 404 status)
- No photo credits page. All photos are CC0 or public domain, so none is needed.

The URL scheme, copy and design are new and differ from every sister site (checked against the
31 `*insuranceappraiser*` sites on the Hostinger account and their generators in this repo).

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` page would skip any redirect in the front
  controller, so `http://www.…/any-page/` would load with a 200.
- So the homepage is `home.html` and **every other page is `dir/index.php`**. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP.
- `_guard.php`:
  - 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://idahoinsuranceappraiser.com`,
    only on the real domain
  - 301s `/dir/index.php` (and `/index.php`) to `/dir/`
  - sends `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview domain)
  - returns 404 when requested directly
- The root `index.php` front controller requires the same guard, serves `home.html` for `/`, 301s directory
  URLs without a trailing slash, includes `dir/index.php` for directory URLs that reach it and returns
  `404.html` with a real 404 status.
- Never add a root `index.html` or any `dir/index.html`. `validate.py` fails the build if one appears, and
  checks that every `dir/index.php` starts with the guard line and has no other PHP.
- Preview URLs serve Hostinger's own Googlebot-blocking `robots.txt`; that's expected. The real domain serves ours.

## Google Search Console verification file

- File: `/googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents (one line, no newline, no HTML wrapper, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it on every build from the `GSC_FILE` / `GSC_BODY` constants, so a rebuild never drops it.
  `validate.py` checks the bytes, keeps it out of the page checks, and fails if it's linked, listed in
  `sitemap.xml` or mentioned in `robots.txt`.
- It must stay at the root permanently. Google re-checks it, and removing it unverifies the property.
  HTML-file verification works only for the **URL-prefix** property `https://idahoinsuranceappraiser.com/`.
  It's a real file, so the host serves it directly and the guard doesn't run for it.

## Design

- **Palette:** navy `#003776` (main), deep navy `#001a3a`, light tint `#eaf1fa`, yellow `#FFE835` (main),
  complementary burnt orange `#d9622b` (sparingly: badges, warnings), warm paper `#fbfaf6`, slate text `#2a3647`.
- **Fonts:** Chivo (display, 600–900) and Be Vietnam Pro (body). No sister site uses either.
- **Layout:** full-bleed photo hero with a white lead-form card and a yellow/navy hazard-stripe edge, counter strip,
  photo peril cards with yellow icon tabs, a horizontal process timeline that fills as you scroll (vertical on
  mobile), a swipeable region carousel on navy, a yellow gap-check band, tool photo cards, city list beside a photo,
  fit/no-fit cards plus a comparison table, guides, FAQ and a navy contact section. Interior pages have photo
  heroes and a two-column layout with a sticky sidebar (call box + related links).
- **Effects:** scroll progress bar, header that turns solid on scroll, hero parallax, staggered reveal,
  animated counters, hover zoom on cards, scroll-filled timeline, region carousel, back-to-top button.
  All motion respects `prefers-reduced-motion`; without JavaScript, content shows and the header stays in place.
- **Mobile nav:** off-canvas drawer outside the header (no `backdrop-filter` anywhere), accordion submenus,
  scroll lock, closes on ×, scrim tap, link tap or Escape, `inert`/`aria-hidden` toggled, shadow and visibility
  only while open. Fixed call bar at the bottom.
- **Logo:** navy tile, yellow twin-peak roofline (mountains and a roof), small sun, white level line. A bolder
  variant is used for the 16/32/48 favicon.ico. `?v=` cache-buster on every icon link.

## Photos (internal record; not published)

All photos are **CC0 1.0 or public domain** (U.S. government works such as USDA Forest Service, or CC0
uploads on StockSnap, rawpixel and Flickr), found through the Openverse API with `license=cc0,pdm`.
None requires attribution, so the site has no credits page. Each is served as 1200px (or the source width
if smaller) and 640px WebP with `srcset`, `sizes`, width and height. Full source details are in
`src/photos.json`; summary:

| Key | Title (as published at source) | Creator | License | Source |
| --- | --- | --- | --- | --- |
| `hero` | Long shot time lapse urban | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/3302880/free-photo-image-architecture-asphalt-boise) |
| `wildfire-ridge` | Retardant drop on the Boise Foothills in 2015 | National Interagency Fire Center | Public domain (flickr) | [link](https://www.flickr.com/photos/165415395@N07/30608405718) |
| `wildfire-smoke` | 20160827-FS-Boise-KG-077 | Forest Service Photography | Public domain (flickr) | [link](https://www.flickr.com/photos/140082569@N07/28431976667) |
| `farm-barn` | Barn Farm | Bonnie Moreland | CC0 1.0 (stocksnap) | [link](https://stocksnap.io/photo/barn-farm-EYKUN3I4DR) |
| `farmland` | Farmer Brown Moderne: Milk and butter fat receiving depot and creamery | polkbritton | Public domain (flickr) | [link](https://www.flickr.com/photos/157979053@N04/41126054801) |
| `commercial-building` | Cast-iron front commercial buildings (Superblock), 100 block of N. How | Baltimore Heritage | CC0 1.0 (flickr) | [link](https://www.flickr.com/photos/44034762@N04/5321765179) |
| `icicles` | Closeup icicles roof | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/6018207/photo-image-public-domain-nature-ice) |
| `kitchen` | Modern white kitchen interior | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/6042749/photo-image-public-domain-minimal-house) |
| `living-room` | Housing improvement project goal 1: two-bedroom unit, living room | YellowstoneNPS | Public domain (flickr) | [link](https://www.flickr.com/photos/80223459@N05/52067485855) |
| `clipboard` | CWD datasheet | U.S. Fish and Wildlife Service - Midwest Region | Public domain (flickr) | [link](https://www.flickr.com/photos/49208525@N08/6343722631) |
| `roof-shingles` | Roof Shingle | Bernard Spragg | CC0 1.0 (stocksnap) | [link](https://stocksnap.io/photo/roof-shingle-RIUJONCXNY) |
| `roof-inspection` | (untitled) | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/5942657/free-public-domain-cc0-photo) |
| `house-fire` | Tilstone House Fire | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/7433149/photo-image-public-domain-city) |
| `lewiston` | Bridge Lewiston, Idaho (2005) Carol | Carol M Highsmith | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/591512/carol-highsmiths-idaho-photograph) |
| `sun-valley` | 20181020-FS-SCNF-JJS-Sun | Intermountain Region US Forest Service | Public domain (flickr) | [link](https://www.flickr.com/photos/107640324@N05/48942459636) |
| `sawtooth` | Wolf and Sawtooth mountains rise above the ridge Custer Gallatin Natio | Forest Service - Northern Region | Public domain (flickr) | [link](https://www.flickr.com/photos/40882383@N03/53515622298) |
| `snow-house` | snow covered house staircase hills | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/3291573/free-photo-image-blizzard-cc0-creative-commons) |
| `snow-roof` | Cabins laden heavy snow outside | Carol M Highsmith | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/582523/carol-highsmiths-colorado-photograph) |
| `neighborhood` | Suburban home quiet neighborhood | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/6038388/photo-image-public-domain-tree-plant) |
| `home-exterior` | Charming suburban home with driveway | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/9658092/house) |
| `home-exterior-2` | Charming suburban home with garden | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/5969571/house) |
| `storm-front` | Storm clouds over the Peaks (HDR) | deborah.soltesz | CC0 1.0 (flickr) | [link](https://www.flickr.com/photos/10836653@N05/3576177210) |
| `thunderstorm` | Thunderstorm at sunset, Swan Lake Flat | YellowstoneNPS | Public domain (flickr) | [link](https://www.flickr.com/photos/80223459@N05/18837881242) |
| `snake-river` | Fall Snake River Canyon at Cottonwood | Intermountain Region US Forest Service | Public domain (flickr) | [link](https://www.flickr.com/photos/107640324@N05/11712452083) |
| `hail-ground` | Hail | Open Grid Scheduler / Grid Engine | CC0 1.0 (flickr) | [link](https://www.flickr.com/photos/29155878@N03/22919917430) |
| `idaho-falls` | 20170819-FS-CT NF-LS-Upper Mesa Falls-01 | Intermountain Region US Forest Service | Public domain (flickr) | [link](https://www.flickr.com/photos/107640324@N05/36933196144) |
| `pocatello` | Emergency Stabilization and Rehabilitation | National Interagency Fire Center | Public domain (flickr) | [link](https://www.flickr.com/photos/165415395@N07/49871414876) |
| `twin-falls` | Snake river in canyon Fall BLIP | hagermanpathways | Public domain (flickr) | [link](https://www.flickr.com/photos/149777496@N06/33467748564) |
| `coeur-d-alene` | Looking at Coeur d'Alene Lake from Canfield Mountain | Forest Service - Northern Region | Public domain (flickr) | [link](https://www.flickr.com/photos/40882383@N03/48014691637) |
| `calculator` | Free calculator working desk image | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/5912338/image-background-public-domain-note) |
| `consult-table` | Woman writing on a notepad | unknown | CC0 1.0 (rawpixel) | [link](https://www.rawpixel.com/image/5916855/woman-writing-notepad) |
| `meeting-room` | Taking emergency management to the classroom | US Embassy Canada | Public domain (flickr) | [link](https://www.flickr.com/photos/38144472@N04/7160697417) |
| `laptop-docs` | Accounting Finance | Wilfred Iven | CC0 1.0 (stocksnap) | [link](https://stocksnap.io/photo/accounting-finance-JONMP7TPGK) |
| `paperwork` | Finance Flatlay | Artsy Crafty | CC0 1.0 (stocksnap) | [link](https://stocksnap.io/photo/finance-flatlay-M9MYHLGNDA) |
| `frozen-pipe` | 20220125-RD-LSC-0345 | USDAgov | Public domain (flickr) | [link](https://www.flickr.com/photos/41284017@N08/51843649876) |

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique
- Meta description **110–143 characters**, present on every page, unique, ends with a complete sentence,
  and identical to `og:description` and `twitter:description`
- Exactly one H1, the first heading is the H1 and no heading level is skipped (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage)
  with `primaryImageOfPage`, `mainEntity` and (except home) `breadcrumb`; ProfessionalService and WebSite present
- Canonical URL is `https://idahoinsuranceappraiser.com/...` for the page
- No broken internal links or anchors; every image has `alt`
- Homepage main content mentions "Idaho Insurance Appraiser" at least 14 times
- No sister-state names anywhere in the build
- Every `sitemap.xml` URL maps to a page; no `index.html` pages; GSC file bytes are exact

Each page's JSON-LD `@graph` holds the ProfessionalService (logo ImageObject, contactPoint, addressRegion ID,
areaServed state + cities, OfferCatalog of services), the WebSite and one page node, plus Service (services and
locations), FAQPage, ItemList (index pages), WebApplication (tools), BlogPosting (guides), HowTo (process) and
DefinedTermSet (glossary) where they apply.

## Contact form

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation (name, a valid
email or phone, consent). It sends each lead through `info@idahoinsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always
appends a JSON line to `api/_private/leads.log.php` (its `<?php http_response_code(404); exit; ?>` header makes
direct requests return 404 with no body).

The SMTP password is **never committed** (`_private/` is in `.gitignore`). Hostinger's file API can't write
outside `public_html`, so the private files sit in `public_html/api/_private/`. When the mailbox exists, upload:

```php
<?php
if (!defined('IIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@idahoinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test,
and check that the log line shows `"via":"smtp"`. Keep any local copy outside the repo and delete it after upload.

## Google Tag Manager

`GTM_ID` in `build.py` is empty, so nothing is output. Set it (e.g. `GTM-XXXXXXX`) to output the standard head
snippet and the `<noscript>` iframe right after `<body>`; if a full snippet is provided, use it exactly.

## Going live checklist

1. Point the domain's nameservers to `nova.dns-parking.com` and `cosmos.dns-parking.com`.
2. Confirm SSL covers both `idahoinsuranceappraiser.com` and `www.idahoinsuranceappraiser.com`
   (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with `agency-hosting_ssl_reinstall-website` if not.
3. Check http/www/`index.php` 301s on the homepage and interior pages, every sitemap URL returns 200, no
   `X-Robots-Tag` on the real domain and our own `robots.txt` is served. If a www URL returns 200 with
   `x-hcdn-cache-status: HIT`, clear the cache and recheck.
4. Create the mailbox and upload the SMTP config (above). Add GTM if provided.
5. In Google Search Console, verify the URL-prefix property `https://idahoinsuranceappraiser.com/`, then submit
   `https://idahoinsuranceappraiser.com/sitemap.xml`. Keep the verification file on the server permanently.
