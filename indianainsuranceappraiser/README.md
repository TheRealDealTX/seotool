# indianainsuranceappraiser.com — static site

Indiana Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served on a Hostinger Agency Growth website. Engineering is based on the
`georgiainsuranceappraiser/` template (generator, `validate.py`, `deploy.sh`, `api/contact.php`,
tool logic, favicon/photo pipelines, canonical-host guard). Content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `6mhwd230h` (Agency Growth, order 1008744732, php-fpm, PHP 8.3; requested datacenter: Boston) |
| Domain | `indianainsuranceappraiser.com` (attached at creation) |
| Preview URL | https://inventive-powderblue-lyrebird-53.hostingersite.com |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@indianainsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | none yet (`GTM_ID = ""` in `build.py`) |

Until the nameservers point to Hostinger, the real domain won't resolve and SSL can't issue, so live
checks run against the preview URL. Hostinger serves its own Googlebot-blocking `robots.txt` on
preview URLs; that's expected.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, templates, schema, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Indiana city pages |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, grouped FAQ, 40-term glossary, 6 guide articles |
| `src/photos.json` | Internal photo manifest: source URL, landing page, creator, license (CC0/PD), size |
| `src/alts.py` | Alt text for each photo |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output** — this folder is what gets deployed (committed) |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS upload API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh upload credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 6mhwd230h)
export IIA_FB_URL=… IIA_FB_AUTH=… IIA_FB_REST=…
./deploy.sh
# then clear the cache: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the
server: `DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and
`X-Auth-Rest` headers. Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed,
everything else to the root `index.php`): `cd public && php -S 127.0.0.1:8000 router.php` with a
router like the one described under "Hosting notes", or simply `php -S 127.0.0.1:8000` for a rough look.

## Pages (50 in sitemap.xml, plus 404)

- Home, `/about-us/`, `/contact-us/`
- `/indiana-claim-appraisal/` + 11 services (appraisal clause, homeowner, commercial/HOA, roof & hail,
  tornado & wind, water, fire & smoke, ice dam/freeze/snow load, farm & outbuilding, estimate review, umpire)
- `/hoosier-cities/` + 12 cities (`/hoosier-cities/<city>-insurance-appraisal/`): Indianapolis, Fort Wayne,
  Evansville, South Bend, Carmel, Fishers, Bloomington, Hammond, Lafayette, Kokomo, Terre Haute, Jeffersonville
- `/claim-gap-tools/` + 7 tools: claim gap & net recovery estimator (three scenarios), RCV/ACV holdback
  calculator, roof pitch & squares calculator (with carrier comparison), percentage deductible calculator,
  claim timeline builder (.ics export), appraisal readiness checkup, roof snow load estimator (Indiana-specific)
- `/appraisal-process-indiana/`, `/indiana-appraisal-questions/` (FAQ by topic), `/insurance-appraisal-terms/`
  (searchable glossary), `/claim-dispute-guides/` + 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/html-sitemap/`, `404.html` (real 404 status)
- No photo-credits page (all photos are CC0/public domain).

Hurricane isn't a separate service (Indiana is inland); hurricane remnants such as Ike (2008) are
covered on the wind page. The state-specific services are ice dam/freeze/snow load and farm buildings.

## Design

- Palette: navy `#002D62` (deep `#001B3D`, darkest `#00112A`, light tint `#E6EDF6`), gold `#FDBB30`
  (tint `#FFF5DC`), steel `#BEC0C2` (light `#EEF0F2`), complementary brick accent `#B4412B` used sparingly,
  neutral ink `#15202D` / muted `#55606D`.
- Fonts: **Oswald** (display) + **Merriweather Sans** (body) — a pairing no sister site uses.
- Motif: a checkered gold/navy stripe (a nod to Indiana racing) on the hero edge, footer and CTA bands.
- Effects: gold scroll progress bar under the header, header transparent → solid navy on scroll, slow
  hero zoom, staggered reveal, animated counters on a gold stat band, hover zoom on photo cards,
  a process timeline that fills as you scroll (horizontal on desktop, vertical on mobile), claim-zone tabs
  with photos, animated "claim gap" bar chart, back-to-top button. No marquee, tilt or parallax CTA.
  All motion respects `prefers-reduced-motion`; reveals only hide content when JS has run (`html.js`).
- Mobile: off-canvas drawer rendered outside the sticky header (no `backdrop-filter` anywhere), accordion
  submenus, scroll lock, closes on ×, scrim tap, link tap or Escape, `inert`/`aria-hidden` toggled, shadow
  and visibility applied only while open; fixed bottom call bar.
- Logo: navy tile with a gold roof chevron over a white balance beam (property + fair valuation).
  `favicon.svg`, a 16/32/48 `favicon.ico` drawn from a bolder variant, 96px PNG, full-bleed 180px
  `apple-touch-icon`, maskable 192/512 PNGs in `site.webmanifest`; every icon link has `?v=`.
  OG image: 1200×630 JPG cropped from a site photo.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files
  directly** (running a directory's `index.php`) without passing through the root `index.php`.
  A `dir/index.html` page would skip any redirect logic, so `http://www.…/page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by the static HTML (no other PHP).
  The homepage is `home.html`, served by the root `index.php`. No root `index.html` and no `dir/index.html`
  may exist; `validate.py` fails the build if one does.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://indianainsuranceappraiser.com` (real domain only), 301s `/dir/index.php` and `/index.php` to
  the directory URL, sends `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview
  domain), and returns 404 when requested directly.
- `index.php` requires the same guard, serves `home.html` for `/`, adds the trailing slash to
  directory URLs, includes `dir/index.php` for directory URLs that reach it and returns `404.html` with a
  real 404 status.
- The only static `.html` files at the root are `home.html`, `404.html` and the Search Console file.

## Google Search Console verification file

- File: `public/googlecccfbf2f7e9e5ae4.html`, written by `build.py` (constants `GSC_FILE`/`GSC_BODY`) on every build.
- Exact contents (single line, no newline, no HTML, no guard, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- It must stay at the site root permanently: Google rechecks it, and removing it unverifies the property.
  It is a real file, so the host serves it directly and the guard doesn't run for it (expected).
- It is excluded from `validate.py`'s page checks, `sitemap.xml`, the HTML site map and internal links,
  and `robots.txt` doesn't block it. `validate.py` checks its bytes on every run.
- Verify in Search Console as a **URL-prefix** property `https://indianainsuranceappraiser.com/`
  (HTML-file verification doesn't work for Domain properties, which need a DNS TXT record).

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique titles
- Meta description present on every page, **110–143 characters** (under 144), unique, ends with a full
  sentence, and identical `og:description` / `twitter:description`
- Exactly one H1, first heading is the H1, no skipped heading levels (footer and sidebar use non-heading labels)
- Valid JSON-LD; every `@id` reference resolves; exactly one page node (WebPage, AboutPage, ContactPage
  or CollectionPage) per page, linked to its BreadcrumbList, primary image and main entity
- Canonical to `https://indianainsuranceappraiser.com/…`, OG image size/alt, Twitter card, `geo.region`
- No broken internal links or anchors; every image has `alt`
- Homepage main content mentions "Indiana Insurance Appraiser" at least 14 times
- No sister-state names anywhere in the build (only "Ohio River" and "Lake Michigan" are allowed as
  geographic names); no photo-credits page or link; GSC file byte-exact and not in the sitemap
- Every `dir/index.php` starts with the guard line and contains no other PHP

Schema per page: ProfessionalService (logo ImageObject, contactPoint, addressRegion IN / US, Indiana and
the 12 cities as areaServed, OfferCatalog of services), WebSite, one page node, BreadcrumbList, plus
Service (services and cities), FAQPage, ItemList (index pages), WebApplication (tools), BlogPosting
(guides), HowTo (process) and DefinedTermSet (glossary) where they apply.

## Contact form

`/api/contact.php` validates input, has a honeypot (`website`) and a per-IP rate limit (5 per 10 minutes).
It sends each lead through `info@indianainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `public_html/api/_private/config.php` exists, falls back to PHP `mail()`,
and always appends a JSON line to `public_html/api/_private/leads.log.php`.

Credentials are **never committed** (`_private/` is in `.gitignore`). The Hostinger file API can't write
outside `public_html`, so the private files live there and return 404 when requested directly: the config
has a defines-guard and the log starts with `<?php http_response_code(404); exit; ?>`. Config format:

```php
<?php
if (!defined('IIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@indianainsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives: upload the config (keep any local copy outside the repo and delete it
after), confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a
test, and confirm the log shows `"via":"smtp"`.

## Google Tag Manager

`GTM_ID` in `build.py` is empty by default. When set (e.g. `"GTM-XXXXXXX"`), every page gets the standard
head snippet and the `<noscript>` iframe right after `<body>`. If a full snippet is supplied, paste it
into `gtm_head()` / `gtm_body()` exactly as provided.

## Photos

All photos are **CC0 or public domain only** (no attribution required), found through the Openverse API
(`license=cc0,pdm`) and fetched one at a time with pauses. Each is served as 1200px and 640px WebP with
`srcset`/`sizes` and width/height. Decorative backgrounds use `alt=""`. There is deliberately no public
credits page; this list is for our internal records (the full manifest is `src/photos.json`).

| Key | Title | Creator | License | Source |
| --- | --- | --- | --- | --- |
| `hero-storm-home` | Supercell | NOAA NSSL | Public Domain Mark | [flickr](https://www.flickr.com/photos/47838549@N08/48039373157) |
| `supercell` | Supercell thunderstorm | NOAA NSSL | Public Domain Mark | [flickr](https://www.flickr.com/photos/47838549@N08/48044614641) |
| `lightning` | Lightning Storm | Brandon Morgan | CC0 | [stocksnap](https://stocksnap.io/photo/lightning-storm-3EPA01FY99) |
| `tornado-damage` | Tornado aftermath can be seen | U.S. Department of Defense | CC0 | [rawpixel](https://www.rawpixel.com/image/3315443/free-photo-image-aftermath-cc0-countryside) |
| `tornado-debris` | aerial view tornado damage Moore | U.S. Forest Service (source) | CC0 | [rawpixel](https://www.rawpixel.com/image/8728258/photo-image-public-domain-nature-landscape) |
| `hailstones` | Hailstorm (NOAA/NSSL Collection) | pingnews.com | Public Domain Mark | [flickr](https://www.flickr.com/photos/39735679@N00/426155154) |
| `flood-street` | stop sign stands flooded street | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/8723819/photo-image-border-public-domain) |
| `icicles-house` | A random view snow thickness on roof and icicles formation | Tinjure20 | CC0 | [wordpress](https://wordpress.org/photos/photo/45063bddda/) |
| `snow-roof` | snow covered house staircase hills | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/3291573/free-photo-image-blizzard-cc0-creative-commons) |
| `ice-storm-trees` | Ice Storm Tree Damage | David Kitto | CC0 | [flickr](https://www.flickr.com/photos/43371449@N00/52665605113) |
| `fallen-tree` | Fallen Trees | U.S. Fish & Wildlife Service Southwest R | Public Domain Mark | [flickr](https://www.flickr.com/photos/51896441@N04/37330421606) |
| `roofer` | Cyrus Brame cleaning gutters | U. S. Fish and Wildlife Service - Northe | Public Domain Mark | [flickr](https://www.flickr.com/photos/43322816@N08/6086748364) |
| `victorian-home` | Dr. D. D. Hooper House, Sylva, NC | w_lemay | CC0 | [flickr](https://www.flickr.com/photos/59081381@N03/31741901727) |
| `farm-barn` | The Red Barn on the Farm | *MMM2* | CC0 | [flickr](https://www.flickr.com/photos/14493178@N07/5615076236) |
| `commercial-building` | Strip Mall, Watertown, New York 02 | Lallint | CC0 | [flickr](https://www.flickr.com/photos/194250376@N05/52111756820) |
| `apartment-condo` | Modern apartment building | DennisM2 | CC0 | [flickr](https://www.flickr.com/photos/14674348@N04/14996764996) |
| `consultation` | Team Meeting | Startup Stock Photos | CC0 | [stocksnap](https://stocksnap.io/photo/team-meeting-69TMH4ITIE) |
| `documents-review` | Writing Papers | Helloquence | CC0 | [stocksnap](https://stocksnap.io/photo/writing-papers-Y01VDYAX63) |
| `calculator` | Calculator Numbers | Negative Space | CC0 | [stocksnap](https://stocksnap.io/photo/calculator-numbers-GIDMT5TDUF) |
| `laptop-spreadsheet` |  | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/5974308/photo-image-laptop-work-macbook) |
| `indiana-cornfield` | Cornfields Farming | Skitter Photo | CC0 | [stocksnap](https://stocksnap.io/photo/cornfields-farming-420322FE63) |
| `fire-damage` | Tilstone House Fire | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/7433149/photo-image-public-domain-city) |
| `smoke-interior` | DSC08838 | callum.darragh | Public Domain Mark | [flickr](https://www.flickr.com/photos/191009661@N02/50657208663) |
| `brick-home` | new roof 2 | City of Detroit Gov | Public Domain Mark | [flickr](https://www.flickr.com/photos/126249508@N04/49503228767) |
| `shingle-roof` | Moss growing on a shingled roof, with a brick wall in the background. | Topher | CC0 | [wordpress](https://wordpress.org/photos/photo/6456862d81/) |
| `suburban-home` | Simple home exterior design photo | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/5912682/image-public-domain-house-home) |
| `hail-roof` | Tarp | USFWS/Southeast | Public Domain Mark | [flickr](https://www.flickr.com/photos/41464593@N02/36443859574) |
| `water-ceiling` | Water damage to Timberline Lodge, Mt. Hood National Forest | Forest Service Pacific Northwest Region | Public Domain Mark | [flickr](https://www.flickr.com/photos/135886671@N08/53666631661) |
| `carmel` | House | unknown | CC0 | [rawpixel](https://www.rawpixel.com/image/9658269/house) |
| `fort-wayne` | Fort wayne skyline as viewed from promenade park | Monster Wedge | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=153476425) |
| `jeffersonville` | Big Four Bridge | Huskydaddy | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=145202976) |
| `lafayette` | Limestone pillars purdue | Guilherme Garbino | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=169344128) |
| `bloomington` | Monroe County Courthouse, Bloomington, IN, December 2018 | TheCatalyst31 | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=143664441) |
| `south-bend` | File:South Bend Tribune street view 2015.JPG | Ian Havens | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=41333485) |
| `hammond` | shoreline Indiana Dunes State Park | Carol M Highsmith | CC0 | [rawpixel](https://www.rawpixel.com/image/2346707/photo-image-cloud-plant-tree) |
| `kokomo` | Kokomo, Indiana skyline | JJIndiana | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=146435264) |
| `evansville` | Northwest side of Old Vanderburgh County Courthouse, Evansville, IN | TheCatalyst31 | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=146364824) |
| `terre-haute` | Dobbs Park, Terre Haute Indiana | Samdamanfr | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=185759345) |
| `indianapolis-skyline` | Indianapolis Skyline and Canal 2025-10-14 | TheWxResearcher | CC0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=176831931) |

Stand-ins: `carmel` (generic new neighborhood), `lafayette` (Purdue campus, West Lafayette), `hammond` (Indiana Dunes shoreline), `terre-haute` (Dobbs Park), `hail-roof` (storm-damaged roof being tarped). Most Flickr/rawpixel/StockSnap originals are only 960–1024px wide, so those WebPs are served at their native width (never upscaled).
