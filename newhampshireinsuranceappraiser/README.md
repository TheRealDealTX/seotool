# newhampshireinsuranceappraiser.com — static site

New Hampshire Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it,
and it runs on a Hostinger Agency Growth website through a small PHP front controller and a canonical-host guard.
The engineering comes from the Georgia template (`georgiainsuranceappraiser/`: generator, `validate.py`, `deploy.sh`,
`api/contact.php`, the tool logic in `app.js`, the photo and favicon pipelines, `_guard.php`). The content, URL
slugs and design are new and don't match any sister site.

| | |
| --- | --- |
| Hostinger website UID | `neutcGqkb` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter selected) |
| Domain | `newhampshireinsuranceappraiser.com` (attached at creation, primary) |
| Preview URL | https://lime-manatee-930708.hostingersite.com (use it for live checks until DNS points here) |
| Nameservers to set at the registrar | `helios.dns-parking.com`, `aster.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@newhampshireinsuranceappraiser.com (the mailbox is created separately) |
| Google Tag Manager | `GTM_ID` in `build.py`. It is empty, so no GTM code is output |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 calculators (markup and copy). Their logic is in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 steps), FAQ (5 groups, 25 Qs), glossary (47 terms), 6 guides |
| `src/photos.json` | Internal photo manifest: source URL, landing page, creator, license and size of each photo |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This is what gets deployed, and it is committed |
| `validate.py` | Post-build checks. Must exit with 0 errors |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over TUS |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # must print "0 errors"
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid neutcGqkb)
export NHIA_FB_URL='…' NHIA_FB_AUTH='…' NHIA_FB_REST='…'
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites files. If you remove or rename a page, delete its old file on the server
with `DELETE {NHIA_FB_URL without /tus}/resources/public_html/<path>`, sending the same `X-Auth` and
`X-Auth-Rest` headers. Hostinger's placeholder `public_html/default.php` has already been deleted.

For a local preview that behaves like the host, run `php -S` with a router that serves real files directly,
runs a directory's `index.php` for `/dir/`, and sends everything else to `index.php`.

## Pages (51 in sitemap.xml, plus a 404)

- Home `/`, About `/about-our-appraisers/`, Contact `/contact-nh-appraiser/`
- Services `/nh-appraisal-services/` plus 12 pages:
  - appraisal clause representation
  - homeowners
  - condo/HOA/commercial
  - roof & hail
  - wind/microburst/tornado
  - tropical storm & nor'easter
  - frozen pipe/water
  - fire/smoke
  - **ice dam & roof snow load** (the New Hampshire–specific peril)
  - tree fall
  - estimate audit
  - umpire
- Cities `/new-hampshire-cities/` plus 12 pages: Manchester, Nashua, Concord, Portsmouth, Dover, Rochester, Derry,
  Salem, Keene, Laconia, Lebanon & Hanover, North Conway (`/new-hampshire-cities/<city>-nh/`)
- Calculators `/nh-claim-calculators/` plus 7 tools:
  - dispute size & net recovery estimator (fees)
  - two-check RCV/ACV holdback planner
  - steep-roof squares checker
  - percent-to-dollars deductible tool
  - Granite State claim clock (.ics export)
  - claim file readiness gauge
  - **snow weight roof calculator** (new for this state)
- Resources:
  - `/how-nh-appraisal-works/` (HowTo)
  - `/nh-appraisal-faq/`
  - `/nh-claim-glossary/` (searchable)
  - `/nh-appraisal-guides/` plus 6 guides
- Legal and navigation: `/website-privacy/`, `/nh-site-terms/`, `/nh-appraiser-disclaimer/`, `/nh-site-map/`,
  and `404.html`, which is served with a real 404 status
- There is **no Photo Credits page**. Every photo is CC0 or public domain (see below)

Every slug was checked against the 1,262 URLs of the ~30 sister `*insuranceappraiser*` sites, and none collide.
`validate.py` rejects any sister-state name in the build. It allows only "Mount Washington", the New Hampshire
mountain.

## Design

- **Palette:** "Granite & Gold".
  - Navy `#002A86`, with a deep shade `#001A55` and ink `#0B1430`
  - Gold `#EFAE0E`, with deep gold `#B98200` and a soft tint `#FFF4D6`
  - Light tint `#E8EEFB`
  - Complementary ember accent `#C9542C`, used sparingly
  - Warm granite neutrals: `#F7F5EF`, `#E3E0D7`, slate `#56607A`
- **Fonts:** Playfair Display for display text and Be Vietnam Pro for body text. No sister site uses this pairing.
- **Layout:**
  - A floating white pill header that becomes a full-width bar with a gold rule on scroll. It uses no `backdrop-filter`.
  - A full-bleed photo hero with a slow Ken Burns zoom and a white lead card.
  - An animated counter ribbon and a gold marquee of town names.
  - An illustrative estimate "ledger".
  - Photo cards for services, featuring two cards.
  - A 12-month New Hampshire claim calendar.
  - A horizontal process line that fills as you scroll.
  - Region tabs with photos.
  - A storm record timeline, photo city cards, three "who to call" cards, the FAQ and guide cards.
  - Interior pages have a photo hero and a two-column layout with a sticky sidebar holding a call box and link lists.
- **Effects:** all of them honor `prefers-reduced-motion`, and the pages render fully without JavaScript.
- **Mobile navigation:** an off-canvas drawer that sits *outside* the fixed header. It has:
  - accordion submenus
  - scroll lock while open
  - closing with ×, an overlay tap, a link tap or Escape
  - `inert` and `aria-hidden` state handling
  - a shadow and visibility applied only while it is open

  A call bar is fixed to the bottom of the screen on mobile.
- **Brand link:** the brand link in the header, drawer and footer doesn't change color or underline on hover.
  Playwright checks this.
- **Logo:** a navy tile with white granite peaks, a gold ridge line and a gold sun. The icon set includes:
  - `favicon.svg`
  - a 16/32/48 `favicon.ico` drawn from a bolder small-size mark
  - a 96px PNG
  - a full-bleed 180px `apple-touch-icon`
  - maskable 192 and 512 PNGs listed in `site.webmanifest`

  Every icon link has a `?v=` cache-buster. The OG image is a 1200×630 JPG made from a site photo.

## Photos (internal record — not published on the site)

All 44 photos are CC0 1.0 or public domain (Public Domain Mark), found through the Openverse API with
`license=cc0,pdm`. Sources:

- Flickr: CC0 and PDM, including US government agencies such as FEMA, NOAA, USFWS and USFS
- Wikimedia Commons: CC0
- rawpixel: CC0
- StockSnap: CC0

None needs attribution, so the site has no credits page. Each photo is center-cropped to 3:2 and saved as WebP
at full width (up to 1200px) and at 640px. The pages use `srcset`/`sizes` with explicit `width`/`height`.
Decorative backgrounds have `alt=""`, and content images have descriptive alt text (`ALT` in `build.py`).
Flickr, StockSnap and rawpixel originals come through at about 1024px, so those files are 940–1024px wide rather
than 1200.

The full record is in `src/photos.json`. Each entry holds `title`, `creator`, `license`, `source`, `landing`,
`url` and `openverse_id`. Summary:

| File | License | Source | Landing page |
| --- | --- | --- | --- |
| `storm-sky-homes` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=116040737 |
| `icicles-eaves` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/6066279/free-public-domain-cc0-photo |
| `icicles-brick` | Public domain (PDM) | flickr | https://www.flickr.com/photos/56844220@N00/5214941839 |
| `snow-roof-chimney` | Public domain (PDM) | flickr | https://www.flickr.com/photos/158350039@N03/26706281238 |
| `ice-storm-limb` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=128350213 |
| `ice-storm-car` | CC0 1.0 | flickr | https://www.flickr.com/photos/43371449@N00/52665605113 |
| `fallen-trees-yard` | Public domain (PDM) | flickr | https://www.flickr.com/photos/51896441@N04/37330421606 |
| `fallen-trees-snow-road` | Public domain (PDM) | flickr | https://www.flickr.com/photos/80223459@N05/8577919489 |
| `storm-collapsed-house` | Public domain (PDM) | flickr | https://www.flickr.com/photos/41284017@N08/7008298739 |
| `flood-damaged-homes` | Public domain (PDM) | flickr | https://www.flickr.com/photos/43322816@N08/6106625390 |
| `roof-shingles-close` | CC0 1.0 | flickr | https://www.flickr.com/photos/37996646802@N01/2271254470 |
| `roof-edge-damage` | Public domain (PDM) | flickr | https://www.flickr.com/photos/41284017@N08/51867761912 |
| `roof-aerial-damage` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=143615045 |
| `roof-crew` | Public domain (PDM) | flickr | https://www.flickr.com/photos/43322816@N08/15871499500 |
| `hailstorm` | Public domain (PDM) | flickr | https://www.flickr.com/photos/39735679@N00/426155154 |
| `lightning-night` | Public domain (PDM) | flickr | https://www.flickr.com/photos/39735679@N00/452386521 |
| `gust-clouds` | Public domain (PDM) | flickr | https://www.flickr.com/photos/39735679@N00/426262117 |
| `noreaster-satellite` | Public domain (PDM) | flickr | https://www.flickr.com/photos/125201706@N06/26942113238 |
| `snow-shoveling` | Public domain (PDM) | flickr | https://www.flickr.com/photos/11906554@N05/25478082537 |
| `fire-damaged-house` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=181512006 |
| `woodstove-cabin` | Public domain (PDM) | flickr | https://www.flickr.com/photos/80223459@N05/54611881331 |
| `inspection-visit` | Public domain (PDM) | flickr | https://www.flickr.com/photos/41284017@N08/37132208273 |
| `consult-table` | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-meeting-SKBXLJOILI |
| `consult-laptop` | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-meeting-Z1ZIMB54UM |
| `calculator-notes` | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-JY874BSKKC |
| `calculator-papers` | Public domain (PDM) | flickr | https://www.flickr.com/photos/91352576@N06/24217746621 |
| `condo-building` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=85192310 |
| `brick-mill` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5967498/brick-mill-building |
| `victorian-home` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5962637/free-public-domain-cc0-photo |
| `colonial-home` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=69831526 |
| `porch-home` | CC0 1.0 | flickr | https://www.flickr.com/photos/59081381@N03/28060404887 |
| `snow-day-house` | CC0 1.0 | flickr | https://www.flickr.com/photos/71401718@N00/6729770599 |
| `kitchen-interior` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/6043001/photo-image-public-domain-house-kitchen |
| `concord-state-house` | CC0 1.0 | flickr | https://www.flickr.com/photos/59081381@N03/49211379746 |
| `manchester-mills` | Public domain (PDM) | flickr | https://www.flickr.com/photos/199507919@N07/55392161006 |
| `nashua-city-hall` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=69822567 |
| `portsmouth-aerial` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/3093163/free-photo-image-new-hampshire-aerial-view-america |
| `hampton-dunes` | Public domain (PDM) | flickr | https://www.flickr.com/photos/43322816@N08/5169633559 |
| `lebanon-library` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=43616273 |
| `hanover-webster-hall` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=27467377 |
| `laconia-mills` | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/2354866/photo-image-plant-tree-sky |
| `wolfeboro-street` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=167827319 |
| `conway-covered-bridge` | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=22614273 |
| `lonesome-lake` | CC0 1.0 | wordpress | https://wordpress.org/photos/photo/74066f3669/ |

## Hosting notes

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting. It **serves real files directly**,
  and for `/dir/` it runs that directory's `index.php`. It sends `/` and unknown paths to the root `index.php`.
- That is why every page except the homepage is written as **`dir/index.php`**. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML that contains no other PHP.
  A `dir/index.html` would skip PHP entirely, so `http://www.…/page/` would answer 200 instead of redirecting.
  Never create a root `index.html` or any `dir/index.html`. `validate.py` fails the build if one exists.
- `_guard.php`:
  - 301-redirects `www.` and plain http (read from `X-Forwarded-Proto`, falling back to `HTTPS`) to
    `https://newhampshireinsuranceappraiser.com`, but only on the real domain
  - 301-redirects `/dir/index.php` and `/index.php` to the directory URL
  - sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview domain
  - returns 404 when it is requested directly
- The root `index.php` requires the guard. It serves `home.html` for `/`, 301-redirects directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- The only static `.html` files at the root are `home.html`, `404.html` and the Search Console file.
- These redirects were verified locally with a router that mimics the host. Requesting an interior page with
  `Host: www.…`, or with the real host plus `X-Forwarded-Proto: http`, returns a 301 to
  `https://newhampshireinsuranceappraiser.com/that-page/`. `/that-page/index.php` returns a 301 to `/that-page/`.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html`, at the site root
- Exact contents: a single line with no HTML, no BOM and no trailing newline:
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it from the `GSC_FILE`/`GSC_BODY` constants on every build, so a rebuild never drops it.
  `validate.py` checks its bytes, leaves it out of the page checks, and confirms that neither `sitemap.xml` nor
  `robots.txt` lists it.
- It is a real file, so the host serves it directly and the guard does not run for it. That is expected.
- **Keep it on the server permanently.** Google rechecks it, and removing it unverifies the property. It works only
  for the **URL-prefix** property `https://newhampshireinsuranceappraiser.com/`. A Domain property needs a DNS TXT
  record instead.

## SEO rules enforced by validate.py

- Title: 60 characters or fewer and about 580px or less (Arial metrics at 20px). Titles are unique.
- Meta description: **110–143 characters**, exactly one per page, hand-written, unique, and ending in a full
  sentence. `og:description` and `twitter:description` must match it.
- Headings: exactly one H1, the first heading is the H1, and no level is skipped. This covers the footer, sidebar
  boxes and tool widgets too.
- Images and links: alt on every image, no broken internal links or anchors.
- Meta tags: a canonical on the real domain that also appears in `sitemap.xml`, plus OG, Twitter and
  `geo.region` tags.
- JSON-LD must parse, and every `@id` reference must resolve. Each graph holds:
  - a ProfessionalService with the logo ImageObject, contactPoint, region/country, areaServed (the state and
    cities) and an OfferCatalog of the services
  - a WebSite node
  - exactly **one** page node (WebPage, AboutPage, ContactPage or CollectionPage), with `breadcrumb`,
    `primaryImageOfPage` and `mainEntity`

  It adds Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply.
- Homepage keyword: "New Hampshire Insurance Appraiser" appears **≥ 14** times inside `<main>`. It is currently 16.
- No sister-state names, and no `photo-credits`.
- Page files: each `dir/index.php` starts with the guard line at the right depth and has no other PHP. There is
  no root `index.html` and no `dir/index.html`.

## Contact form

`/api/contact.php` uses a honeypot (`website`), a per-IP rate limit (5 per 10 minutes) and server-side
validation: a name, a valid email or a phone number, and consent. It sends through
info@newhampshireinsuranceappraiser.com over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, and falls back to `mail()`. It always appends a JSON line to
`api/_private/leads.log.php`. That file starts with `<?php http_response_code(404); exit; ?>`, so a direct request
returns 404 with 0 bytes. Hostinger's file API can't write outside `public_html`, which is why these files sit
there. `_private/` is in `.gitignore`. **Never commit credentials.**

When the mailbox password is available, upload `public_html/api/_private/config.php` and delete any local copy:

```php
<?php
if (!defined('NHIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@newhampshireinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then check it:

1. The config URL returns 404 with 0 bytes.
2. One submission labelled as a test goes through.
3. The log shows `"via":"smtp"`.

## Google Tag Manager

Set `GTM_ID = "GTM-XXXXXXX"` in `build.py`, rebuild, validate and deploy. The head snippet is output right after
`<meta charset>`, and the `<noscript>` iframe right after `<body>`. If a full snippet is provided, use it exactly
as given.

## When the nameservers point here

1. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`). Reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
2. Check the canonical-host behavior on the homepage and at least three interior pages:
   - http, www and https-www all 301 to the https apex
   - `/page/index.php` 301s to `/page/`
   - every sitemap URL returns 200
   - the real domain sends no `X-Robots-Tag` and serves this site's own `robots.txt`
   - the verification file returns 200 with exactly the line above
   - if a www URL returns 200 with `x-hcdn-cache-status: HIT`, clear the cache again
3. Verify the URL-prefix property in Search Console, then submit `https://newhampshireinsuranceappraiser.com/sitemap.xml`.
