# kansasinsuranceappraiser.com — static site

Kansas Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served through a tiny PHP guard/front controller on a Hostinger Agency Growth website.
The engineering (generator, validator, deploy script, form handler, tool logic, guard) comes from
`georgiainsuranceappraiser/`; the content, URL slugs, design, palette, fonts and photos are new.

| | |
| --- | --- |
| Hostinger website UID | `mYtxbSNax` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter, server `us-phx-h5g-node3`) |
| Live domain | https://kansasinsuranceappraiser.com (live Nov 18, 2026; SSL covers the domain and `www`, expires Feb 15, 2027 and auto-renews; www and http 301 to it) |
| Preview URL | https://growing-olive-turkey-24.hostingersite.com (sends `X-Robots-Tag: noindex, nofollow`) |
| Nameservers to set at the registrar | `helios.dns-parking.com`, `aster.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@kansasinsuranceappraiser.com (form delivers over SMTP; verified Nov 18, 2026) |
| Google Tag Manager | `GTM-MF386JDG` (owner-supplied head tag + noscript iframe on every page) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 Kansas city pages |
| `src/tools.py` | 7 interactive calculators (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide, FAQ by topic, 42-term glossary, 6 guide articles |
| `src/photos.json` | Photo manifest: alt text, size, title, creator, license, source page (internal record only) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** — this folder is deployed (committed) |
| `validate.py` | Post-build checks (must exit 0) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` via the TUS upload API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid mYtxbSNax)
export KIA_FB_URL='…' KIA_FB_AUTH='…' KIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the
server: `DELETE {upload-url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and
`X-Auth-Rest` headers. Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed,
everything else to the root `index.php`): `php -S 127.0.0.1:8765 -t public router.php` with a router like
the one described under Hosting notes.

## Pages (51 in sitemap)

- Home (`home.html`, served at `/`), About (`/about-our-kansas-firm/`), Contact (`/request-kansas-claim-review/`)
- `/what-we-handle/` + 12 services: appraisal clause representation, homeowner, commercial & HOA,
  roof & hail, tornado & straight-line wind, ice storm & freeze, water, fire & smoke,
  **wildfire & grass fire** (the Kansas-specific peril), farm & ranch buildings, estimate review, umpire
- `/kansas-cities-served/` + 12 cities (`/kansas-cities-served/<city>-insurance-appraiser/`): Wichita,
  Overland Park, Kansas City, Olathe, Topeka, Lawrence, Manhattan, Salina, Hutchinson, Dodge City, Garden City, Hays
- `/claim-calculators-kansas/` + 7 tools: appraisal payoff projector, holdback recovery calculator,
  roof square footage & pitch calculator, percentage deductible converter, claim timeline builder (.ics export),
  appraisal prep scorecard, and the new **roof age payment schedule calculator**
- `/kansas-appraisal-process/` (HowTo), `/kansas-claim-faq/` (grouped by topic), `/kansas-claim-glossary/`
  (42 searchable terms), `/kansas-appraisal-guides/` + 6 guides
- `/privacy-information-ks/`, `/website-terms-ks/`, `/appraisal-disclaimer-ks/`, `/kansas-page-index/` (HTML site map),
  `404.html` (real 404 status), `sitemap.xml`, `robots.txt`
- **No photo credits page.** All photos are CC0 or public domain; none is linked or generated.

Homepage keyword: “Kansas Insurance Appraiser” appears 17 times in `<main>` (22 counting header/footer);
`validate.py` requires at least 14.

## Design

- Palette: navy `#002569` (deep `#00143d`, mid `#13408f`), sunflower gold `#F1AD02` (deep `#b98300`,
  soft `#fff3d1`), sky tint `#eef3fb`, ember accent `#c2410c` (used sparingly for warnings), warm paper
  `#fbfaf6` and slate neutrals.
- Fonts: **Sofia Sans Condensed** (display, uppercase hero) + **Atkinson Hyperlegible** (body) — not used by any sister site.
- Layout: full-bleed photo hero with a white “free claim check” card; numbered section kickers (01–11);
  photo service cards; horizontal process track; region photo cards; list-style calculator rows with
  thumbnails; city tiles; photo heroes on interior pages; two-column interior layout with a sticky sidebar.
- Effects: gold scroll-progress bar, header that turns solid navy on scroll, hero parallax, staggered
  reveal, animated counters, hover zoom on cards, process line that fills as you scroll (vertical on
  mobile), back-to-top. No marquee, tilt or region tabs (those are on sister sites). All motion respects
  `prefers-reduced-motion`; without JS the header is solid, reveals are visible and the process line is full.
- Mobile nav: off-canvas drawer **outside** the fixed header (the header has no `backdrop-filter`),
  accordion submenus, scroll lock, close on ×, overlay tap, link tap or Escape, `inert`/`aria-hidden`
  toggled, shadow and visibility only while open. Fixed mobile call bar at the bottom.
- Logo: navy tile with a gold roof chevron and three white “estimate” lines (`static/assets/img/mark.svg`,
  inline in header, drawer and footer). Icons: `favicon.svg`, `favicon.ico` (16/32/48, bolder small mark),
  96px PNG, full-bleed 180px `apple-touch-icon.png`, 192/512 any + maskable PNGs in `site.webmanifest`,
  all linked with `?v=1`. OG image: 1200×630 JPG from a site photo.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan “force HTTPS” setting, and **serves real files directly**
  (running a directory’s `index.php`) without passing through the root `index.php`. Only `/` and unknown
  paths reach the front controller.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP).
  A `dir/index.html` page would be served without the guard, so `http://www.…/page/` would load with a 200.
  **Never create a root `index.html` or any `dir/index.html`.** The only static `.html` files at the root are
  `home.html`, `404.html` and the Search Console file.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://kansasinsuranceappraiser.com` — only on the real domain — 301s `/dir/index.php` and `/index.php`
  to the directory URL, sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview domain), and
  returns 404 if requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs that
  lack a trailing slash, includes `dir/index.php` for directory URLs that reach it, and otherwise returns
  `404.html` with a real 404 status.
- `validate.py` checks every page starts with the guard line, contains no other PHP, and that no
  `index.html` or `photo-credits` exists.

## Google Search Console verification file

`public/googlecccfbf2f7e9e5ae4.html` is written by `build.py` (constants `GSC_FILE` / `GSC_BODY`) on every
build, byte for byte, with no newline, wrapper, guard, GTM or BOM:

```
google-site-verification: googlecccfbf2f7e9e5ae4.html
```

It must stay at the site root permanently: Google re-checks it, and removing it unverifies the property.
It is a real file, so the host serves it directly and the guard does not run (expected). It is excluded
from page checks, `sitemap.xml`, the HTML site map and internal links; `robots.txt` doesn’t block it;
`validate.py` fails if its bytes ever change. HTML-file verification works only for a **URL-prefix**
property (`https://kansasinsuranceappraiser.com/`).

## Photos (CC0 / public domain only, no public credits page)

All photos were found through the Openverse API with `license=cc0,pdm` and downloaded one at a time with
pauses. Each is saved as a large WebP (native width up to 1200px; rawpixel and Flickr sources cap at 1024px)
and a 640px WebP, used with `srcset`/`sizes`/width/height. Alt text is descriptive; decorative heroes and
card images use `alt=""`. The source list below is an **internal record only** and is not published on the site.

| Key | Title (as listed) | Creator | License | Via | Source page |
| --- | --- | --- | --- | --- | --- |
| `calculator` | Calculator | motazabdelazeem صور من الوطن | Public domain mark | flickr | https://www.flickr.com/photos/91352576@N06/24217746621 |
| `clipboard` | Calculator Numbers | Martin Vorel | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-JY874BSKKC |
| `commercial-roof` | Bakewell Street, Covington, KY | w_lemay | CC0 1.0 | flickr | https://www.flickr.com/photos/59081381@N03/49674203276 |
| `consultation` | untitled | unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5945923/free-public-domain-cc0-photo |
| `documents` | Paperwork Desk | Matt Moloney | CC0 1.0 | stocksnap | https://stocksnap.io/photo/paperwork-desk-A5DG6YREVH |
| `dodge-city` | File:Lora Locke Hotel from SE 2.JPG | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=39275962 |
| `estimate-review` | Calculator Numbers | Negative Space | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD |
| `flint-hills` | 20180529-RD-PJK-1336_TONED | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/27570349637 |
| `garden-city` | Scene railroad depot Garden City | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8041555/photo-image-sky-road-public-domain |
| `grain-elevator` | block-long grain elevator Overland Park | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8043143/photo-image-public-domain-city-united-states |
| `grass-fire` | Yes, this field outside Greensburg | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8070330/photo-image-fire-public-domain-united-states |
| `hail-roof` | 20220127-RD-LSC-0692 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/51867761912 |
| `hero` | Kansas | NOAA NSSL | Public domain mark | flickr | https://www.flickr.com/photos/47838549@N08/48039373122 |
| `house-fire` | President Donald J. Trump Travels to California | The White House | Public domain mark | flickr | https://www.flickr.com/photos/148748355@N05/45931137101 |
| `hutchinson` | This Hutchinson, Kansas, 'labor temple,' | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8042719/photo-image-public-domain-united-states-library |
| `ice-storm` | Ice Storm Tree Damage | David Kitto | CC0 1.0 | flickr | https://www.flickr.com/photos/43371449@N00/52665605113 |
| `kansas-city` | enormous grain elevator Kansas City | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8043261/photo-image-public-domain-city-united-states |
| `kansas-prairie` | Classic Kansas field waving wheat | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/433965/free-photo-image-wheat-carol-highsmith-kansas |
| `kitchen` | Housing improvement project goal 1: two-bedroom unit, kitchen and livi | YellowstoneNPS | Public domain mark | flickr | https://www.flickr.com/photos/80223459@N05/52067000921 |
| `lawrence` | Suburban housing, real estate | unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/6023013/photo-image-public-domain-house-free |
| `main-street` | colorful tidy RHV Hardware Store | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8070867/photo-image-public-domain-united-states |
| `metal-barn` | Barn & Milkhouse | Ted LaBar | Public domain mark | flickr | https://www.flickr.com/photos/46154524@N04/4321340838 |
| `new-homes` | Lockport New York - United States - Col. William M. and Nancy Ralston  | Onasill - Bill Badzo - 149 Million Views - Thank Y | Public domain mark | flickr | https://www.flickr.com/photos/7156765@N05/51583472754 |
| `office-building` | 20110420-RD-LSC-0350 | USDAgov | Public domain mark | flickr | https://www.flickr.com/photos/41284017@N08/6252247115 |
| `prairie-road` | array hay rolls seems neatly | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8071218/photo-image-plant-grass-sky |
| `ranch-home` | modest, color-coordinated house Arapahoe, small | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8068213/photo-image-border-plant-grass |
| `roofer` | Roofers | Dennis S. Hurd | CC0 1.0 | flickr | https://www.flickr.com/photos/43296902@N00/4363286049 |
| `shingle-roof` | Free suburban house winter photo | unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5913696/image-public-domain-house-interior |
| `siding` | Paddock Road, Bond Hill, Cincinnati, OH | w_lemay | CC0 1.0 | flickr | https://www.flickr.com/photos/59081381@N03/27226382697 |
| `storm-front` | Hail Core | NOAA NSSL | Public domain mark | flickr | https://www.flickr.com/photos/47838549@N08/47953539536 |
| `suburb-street` | Ryland Avenue, Bond Hill, Cincinnati, OH | w_lemay | CC0 1.0 | flickr | https://www.flickr.com/photos/59081381@N03/27226392837 |
| `topeka-capitol` | Capitol building, locally often called | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8069847/photo-image-public-domain-united-states-building |
| `tornado` | Project Vortex-99: Occluded mesocyclone tornado (NOAA/unidentified fot | pingnews.com | Public domain mark | flickr | https://www.flickr.com/photos/39735679@N00/452392668 |
| `tornado-damage` | Brimfield Tornado Home Damage, June 3, 2011 | MassDOT | Public domain mark | flickr | https://www.flickr.com/photos/42009447@N05/5793071807 |
| `water-ceiling` | ceiling of the former Pan Am Worldport, Delta's T3 at JFK | brianj.lowe | Public domain mark | flickr | https://www.flickr.com/photos/68433569@N02/8174894771 |
| `wheat-storm` | untitled | unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5952949/free-public-domain-cc0-photo |
| `wichita` | One two cable-stayed pedestrian bicycle | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8041527/photo-image-public-domain-city-united-states |

## Contact form

`/api/contact.php`: honeypot field, per-IP rate limit (5 per 10 minutes), validation (name, a valid email
or a phone, consent). It sends through `info@kansasinsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `public_html/api/_private/config.php` exists, falls back to `mail()`, and
always appends a JSON line to `public_html/api/_private/leads.log.php` (which starts with a PHP 404/exit
header, so it returns 404 when requested). Hostinger’s file API can’t write outside `public_html`, which
is why `_private/` lives there. `_private/` is in `.gitignore` — **never commit credentials**.

The config is **on the server** (uploaded Nov 18, 2026; no copy kept anywhere else). It returns 404 with 0 bytes, and a
labelled test submission logged `"via":"smtp"`. To change the password, re-upload a file in this shape (keep any local
copy outside the repo and delete it after upload):

```php
<?php
if (!defined('KIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@kansasinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test,
and confirm the log line shows `"via":"smtp"`.

## Google Tag Manager

`GTM_ID = "GTM-MF386JDG"` in `build.py`. `GTM_HEAD` holds the head tag exactly as the owner supplied it (an async
`gtm.js` loader plus a `dataLayer`/`gtag('js')` init); it is output right after `<meta charset>` on every page, and the
standard `<noscript>` iframe for the same container is output right after `<body>`. Empty `GTM_HEAD` falls back to the
standard GTM snippet; empty `GTM_ID` outputs no tag at all.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique
- Meta description **110–143 characters** (under 144), unique, ending in a full sentence; `og:description`
  and `twitter:description` must match it
- Exactly one H1, the first heading is the H1, no skipped levels (footer, sidebar and tools included)
- Valid JSON-LD and every `@id` reference resolves within the page graph
- No broken internal links or anchors; every image has `alt`
- Homepage main content mentions “Kansas Insurance Appraiser” ≥ 14 times
- No sister-state names (every other `*insuranceappraiser` state) anywhere in the build
- Pages start with the guard line; GSC file bytes exact; no `index.html`, no photo credits

Each page’s JSON-LD `@graph` holds the ProfessionalService (logo ImageObject, contactPoint, KS region/US,
Kansas + 12 cities as areaServed, OfferCatalog of services), the WebSite and one page node (WebPage,
AboutPage, ContactPage or CollectionPage) linked to its BreadcrumbList, primary image and main entity,
plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply.

## Go-live checks (done Nov 18, 2026)

1. Confirm SSL covers `kansasinsuranceappraiser.com` **and** `www.` (`agency-hosting_websites_get` → `ssl_cert.names`);
   if `www` is missing, `agency-hosting_ssl_reinstall-website` and wait for `active`.
2. Check `http://`, `http://www.` and `https://www.` versions of the homepage and three interior pages 301 to
   `https://kansasinsuranceappraiser.com/page/`, `/page/index.php` 301s to `/page/`, every sitemap URL is 200,
   no `X-Robots-Tag` on the real domain, our own `robots.txt` is served, and the GSC file matches byte for byte.
   A www URL returning 200 with `x-hcdn-cache-status: HIT` is a stale CDN copy: clear the cache and recheck.
3. Verify the URL-prefix property in Search Console, then submit `https://kansasinsuranceappraiser.com/sitemap.xml`
   (owner action). Keep `googlecccfbf2f7e9e5ae4.html` on the server permanently.

Steps 1–2 passed on Nov 18, 2026: SSL names include `www`, all redirects 301 correctly on the homepage and three
interior pages, all 51 sitemap URLs return 200, the real domain sends no `X-Robots-Tag`, our `robots.txt` is served
and the GSC file is byte-identical.
