# nebraskainsuranceappraiser.com — static site

Nebraska Insurance Appraiser: a static site with no database and no plugins, built by a Python generator and
served on a Hostinger Agency Growth website through a tiny PHP front controller and canonical-host guard.

| | |
| --- | --- |
| Hostinger website UID | `MzvyUm9HJ` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | `nebraskainsuranceappraiser.com` (attached at creation; nameservers not yet pointed) |
| Preview URL | https://blueviolet-barracuda-496096.hostingersite.com (sends `X-Robots-Tag: noindex`; Hostinger serves its own Googlebot-blocking robots.txt here) |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` (from `agency-hosting_websites_get`) |
| Google Tag Manager | not set yet: `GTM_ID = ""` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@nebraskainsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Nebraska city pages |
| `src/tools.py` | 7 interactive tools (markup, copy, FAQs) |
| `src/learn.py` | Process guide (7 steps), grouped FAQ, 41-term word list, 6 guides |
| `src/photos.json` | Internal photo manifest: title, creator, license, source and landing URL, output size |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `tools/photos.py` | Photo pipeline: CC0/PD originals → 1200px + 640px WebP, updates `src/photos.json` (rejects other licenses) |
| `tools/icons.py` | Logo/favicon/OG pipeline: `favicon.svg`, 16/32/48 `favicon.ico` (bold variant), 96px PNG, 180px apple-touch-icon, maskable 192/512, `site.webmanifest`, `og-image.jpg` |
| `public/` | **Build output.** What gets deployed (committed, minus `api/_private/`) |
| `validate.py` | Post-build checks (must report 0 errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # must end with "0 errors"
# fresh creds: Hostinger API agency-hosting_files_generate-upload-url (website_uid MzvyUm9HJ)
export NIA_FB_URL='…/api/tus' NIA_FB_AUTH='…' NIA_FB_REST='…'
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server:
`curl -X DELETE "${NIA_FB_URL%/tus}/resources/public_html/<path>" -H "X-Auth: $NIA_FB_AUTH" -H "X-Auth-Rest: $NIA_FB_REST"`.
Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed, everything else to `index.php`):

```php
<?php // router.php — run: php -S 127.0.0.1:8080 -t public router.php
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH); $f = $_SERVER['DOCUMENT_ROOT'] . $p;
if ($p !== '/' && (is_file($f) || (substr($p, -1) === '/' && is_file($f . 'index.php')))) return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
```

## Pages (50 in sitemap + 404)

| Section | URL |
| --- | --- |
| Home | `/` (rendered as `home.html`) |
| About / Contact | `/about-our-appraisers/`, `/free-claim-review/` |
| Services index + 11 | `/appraisal-services-nebraska/<slug>/` — appraisal demand representation, homeowner, commercial & HOA, hail & roof, tornado & straight-line wind, farm & ranch outbuildings (state-specific), water, fire & smoke, ice dam & frozen pipe (state-specific), carrier estimate review, umpire selection |
| Cities index + 12 | `/nebraska-cities/<city>/` — Omaha, Lincoln, Bellevue, Papillion, Grand Island, Kearney, Fremont, Hastings, Norfolk, North Platte, Columbus, Scottsbluff |
| Tools index + 7 | `/claim-tools-nebraska/<slug>/` — award gap & fee estimator, ACV holdback calculator, roof square & pitch converter (multi-section), hail deductible calculator, claim calendar builder (.ics), appraisal readiness check, slope-by-slope repair gap calculator (new) |
| Resources | `/nebraska-appraisal-process/`, `/questions-about-appraisal/`, `/appraisal-word-list/`, `/nebraska-claim-guides/` + 6 guides |
| Legal & nav | `/our-privacy-policy/`, `/website-terms-of-use/`, `/appraisal-disclaimers/`, `/site-contents/`, `404.html` |

No Photo Credits page exists or is linked. URL slugs, section order, copy and design differ from every sister
`*insuranceappraiser*` site in the Hostinger account (checked against all 33 listed).

## Design

- **Palette:** navy `#002A86` (deep `#001B57`, darkest `#000E30`), light tint `#E8EEFA` / `#F4F6FB`, gold `#FFCC00`,
  silver `#C8C8C8` (light `#EEEEEC`), one complementary accent “prairie rust” `#B4532A` (kickers, “no” states), neutral inks.
- **Fonts:** Schibsted Grotesk (display, 600–900) + Public Sans (body). No sister site uses either.
- **Mark:** navy tile with a white roof line over a gold “ledger” bar and a short silver bar; bold two-element variant for 16–48px.
- **Layout:** full-bleed supercell hero with Ken Burns zoom and a gold-topped “ticket” lead form; gold tally band with counters
  overlapping the hero; numbered section tags (01–12) with a gold rule; horizontal process timeline that fills on scroll
  (vertical on mobile); featured-card service grid; storm record list; region tabs with photos; city photo cards; tool and guide cards;
  photo heroes and a two-column layout with a sticky call box + related links on interior pages.
- **Effects used:** solid-on-scroll header, hero zoom, staggered reveal, counters, card hover zoom, scroll-filled timeline, region tabs,
  back-to-top. Not used: progress bar, 3D tilt, marquee, parallax CTA. All respect `prefers-reduced-motion`; the page renders fully
  without JavaScript (`.no-js` header is solid, reveal content visible, all region panels shown).
- **Mobile:** off-canvas drawer from the left, rendered **outside** the fixed header (no `backdrop-filter` anywhere), accordion
  submenus, scroll lock, closes on ×/overlay/link/Escape, `inert` + `aria-hidden`, shadow and visibility only while open; fixed call bar.
- Brand link colour is pinned in header, drawer and footer so hover never recolours or underlines it.

## Hosting notes (canonical-host guard)

- The host ignores `.htaccess`, has no Agency-plan “force HTTPS” setting and **serves real files directly without running the root
  `index.php`**. A `dir/index.html` would therefore skip any redirect, so `http://www.…/any-page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP. There is no root
  `index.html` and no `dir/index.html` anywhere; the only root `.html` files are `home.html`, `404.html` and the Search Console file.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://nebraskainsuranceappraiser.com`
  on the real domain only, 301s `/dir/index.php` (and `/index.php`) to `/dir/`, sends `X-Robots-Tag: noindex, nofollow` on any other host,
  and returns 404 if requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash,
  includes `dir/index.php` when a directory URL reaches it, and returns `404.html` with a real 404.
- `validate.py` fails if a page lacks the guard line, contains other PHP, or if any `dir/*.html`/root `index.html` exists.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root. Contents, exactly (no newline, no HTML, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- Written by `build.py` on every build from the `GSC_FILE` / `GSC_BODY` constants, so a rebuild never drops it.
- It is a real file, so the host serves it directly and the guard doesn't run for it (expected). It is excluded from page checks,
  `sitemap.xml`, the HTML site map and internal links, and `robots.txt` doesn’t block it. `validate.py` checks its bytes.
- It must stay at the root permanently: Google rechecks it, and removing it unverifies the URL-prefix property.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique.
- Meta description **110–143 characters** (under 144), hand-written per page, unique, ending in a full sentence;
  `og:description` and `twitter:description` must match it. (Current range: 125–143.)
- Exactly one H1, first heading is H1, no skipped levels anywhere (footer, sidebar boxes and tool widgets included).
- Canonical on `https://nebraskainsuranceappraiser.com/…`, Open Graph (with image size/alt), Twitter card and `geo.region` on every page.
- JSON-LD valid; each `@graph` has ProfessionalService (logo, contactPoint, addressRegion/country, areaServed state + cities,
  OfferCatalog), WebSite and exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage) linked to its BreadcrumbList,
  primaryImageOfPage and mainEntity; plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where
  they apply. Every `@id` reference must resolve.
- No broken internal links or anchors; every image has `alt`.
- Homepage main content must contain “Nebraska Insurance Appraiser” at least 14 times (currently 20).
- No other state’s name may appear (all 49, word-bounded). “Missouri River” is allowed because it is the state’s eastern border river.
- `sitemap.xml` URLs must all exist; no photo-credits page.

## Contact form

`/api/contact.php`: honeypot (`website`), per-IP limit (5 per 10 minutes), validation (name, email or phone, consent).
It sends through `info@nebraskainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`public_html/api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (created with a `<?php http_response_code(404); exit; ?>` header). Both private files return 404
over the web. They sit inside `public_html` because the Hostinger file API can't write outside it. `_private/` is git-ignored.

Config to upload once the mailbox exists (keep any local copy outside the repo and delete it after upload):

```php
<?php
if (!defined('NIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@nebraskainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and confirm the
log line shows `"via":"smtp"`.

## Photos (internal record — not published)

44 photos, all **CC0 1.0 or public domain** (no attribution-required licenses), found via the Openverse API
(`license=cc0,pdm`): Wikimedia Commons, Flickr CC0/PD (incl. NOAA/NSSL and USDA), rawpixel (Library of Congress/Highsmith), StockSnap.
Downloaded one at a time with pauses and backoff (Wikimedia via standard 330px/960px/1280px thumbnail widths), reviewed on labelled
contact sheets, then converted by `tools/photos.py` to 1200px and 640px WebP (`srcset`/`sizes`, width/height set). Decorative
backgrounds use `alt=""`. `house-fire` is reused from the template's CC0 set. There is no public credits page.

| Key | Title | Creator | License | Source | Landing URL |
| --- | --- | --- | --- | --- | --- |
| `barn-storm` | Barn and storm clouds, Willamette Valley, Oregon | Bonnie Moreland (free images) | Public domain | flickr | https://www.flickr.com/photos/66741228@N05/50298057333 |
| `barn-sunset` | Old barn, winter sunset, Oregon | Bonnie Moreland (free images) | CC0 1.0 | flickr | https://www.flickr.com/photos/66741228@N05/32628641981 |
| `bellevue-church` | Bellevue, Nebraska First Presbyterian from SE 1 | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=22454408 |
| `calculator-laptop` | Calculator Numbers | Negative Space | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD |
| `calculator-pen` | Calculator Numbers | Martin Vorel | CC0 1.0 | stocksnap | https://stocksnap.io/photo/calculator-numbers-JY874BSKKC |
| `ceiling-water` | Eden Mall water damage | Indy beetle | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=85607779 |
| `chimney-rock` | iconic Chimney Rock, now U.S | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8041251/photo-image-cloud-grass-sky |
| `clipboard` | Clipboard Desk | Design by Matt | CC0 1.0 | stocksnap | https://stocksnap.io/photo/clipboard-desk-VXAISJRBH9 |
| `columbus-hall` | City Hall in Columbus, Nebraska | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8041297/city-hall-columbus-nebraska |
| `condo-building` | Modern apartment building | DennisM2 | CC0 1.0 | flickr | https://www.flickr.com/photos/14674348@N04/14996764996 |
| `consultation` | Business Meeting | Christina Morillo | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-meeting-SKBXLJOILI |
| `contractor-belt` | Construction Worker | Leeroy | CC0 1.0 | stocksnap | https://stocksnap.io/photo/construction-worker-6B70C91911 |
| `craftsman-home` | Suburban housing, real estate | Unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/6023013/photo-image-public-domain-house-free |
| `family-home` | Tree Outside Suburban Homes | Image Catalog | CC0 1.0 | flickr | https://www.flickr.com/photos/132795455@N08/16681992243 |
| `farm-silos` | Nebraska Farm & Silos | Gary Lee Todd, Ph.D. | CC0 1.0 | flickr | https://www.flickr.com/photos/101561334@N08/33136328323 |
| `flood-aerial` | 20110618-OSEC-RBN-4945 | USDAgov | Public domain | flickr | https://www.flickr.com/photos/41284017@N08/6302933528 |
| `flood-road` | Road to Boyers Chute NWR under water 6.19.2011 | MONGO | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=15579719 |
| `fremont-main` | Fremont, Nebraska 3rd and Main looking NW | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=18223168 |
| `glass-office` | Office Building | Open Grid Scheduler / Grid Engine | CC0 1.0 | flickr | https://www.flickr.com/photos/29155878@N03/26627905122 |
| `grain-bin-wreck` | A grain bin that was destroyed southwest of Lyons, Nebraska | National Oceanic and Atmospheric Administration | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=132695257 |
| `grain-bins` | Grain Bins and Farm Sheds | keystonecops555 | Public domain | flickr | https://www.flickr.com/photos/183085050@N02/49159824332 |
| `grand-island` | Scene downtown Grand Island, Nebraska | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8041481/photo-image-cloud-plant-person |
| `hailstones` | Some of the hailstones that were pummeling my van while I wa | Kim Siever | Public domain | flickr | https://www.flickr.com/photos/57873306@N00/9087743581 |
| `hastings-homes` | Hastings, Nebraska 800-odd N Lincoln Ave | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=22716840 |
| `hastings-park` | Hastings, Nebraska Heartwell Park from W 1 | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=22675720 |
| `hero-supercell` | Nebraska Supercell thunderstorm | NOAA NSSL | Public domain | flickr | https://www.flickr.com/photos/47838549@N08/48044614771 |
| `house-fire` | Burning house | Unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5918064/burning-house-free-public-domain-cc0-photo |
| `icicles` | Berkeley Heights library large icicles hanging from roof | Tomwsulcer | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=31298171 |
| `lincoln-capitol` | Nebraska Capitol, Lincoln | Gary Lee Todd, Ph.D. | CC0 1.0 | flickr | https://www.flickr.com/photos/101561334@N08/33136321833 |
| `lincoln-haymarket` | Lincoln, Nebraska Haymarket P St from 9th 1 | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=21353904 |
| `norfolk-theatre` | File:Grand Theatre (Norfolk, Nebraska) from NE 2.JPG | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=28379490 |
| `north-platte` | Golden Spike Tower, North Platte | Ammodramus | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=18588775 |
| `omaha-dusk` | City of Omaha, Nebraska Skyline on Gene Leahy Mall | JNOJ1423 | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=141090612 |
| `omaha-skyline` | Downtown view Omaha, Nebraska's largest | Carol M Highsmith | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/8027840/photo-image-cloud-sky-public-domain |
| `platte-woods` | Oak trees line the Platte River at Crane Meadows National Wi | U.S. Fish and Wildlife Service - Midwest Region | Public domain | flickr | https://www.flickr.com/photos/49208525@N08/49018812867 |
| `review-meeting` | Business Meeting | Direct Media | CC0 1.0 | stocksnap | https://stocksnap.io/photo/business-meeting-SSKSJIBMMP |
| `roof-tarp` | Roofers | Dennis S. Hurd | CC0 1.0 | flickr | https://www.flickr.com/photos/43296902@N00/4363286049 |
| `scotts-bluff` | View towards the north from the North Overlook, Scotts Bluff | DimiTalen | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=156012291 |
| `shingles` | Roof Shingle | Bernard Spragg | CC0 1.0 | stocksnap | https://stocksnap.io/photo/roof-shingle-RIUJONCXNY |
| `snowy-home` | Free suburban house winter photo | Unknown | CC0 1.0 | rawpixel | https://www.rawpixel.com/image/5913696/image-public-domain-house-interior |
| `storm-anvil` | Supercell 059 | Šime Barešić | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=157426479 |
| `tornado-home` | Extreme EF4 damage done to a home from the Pilger tornado | National Weather Service | CC0 1.0 | wikimedia | https://commons.wikimedia.org/w/index.php?curid=151251240 |
| `tornado-plains` | TORUS tornado | NOAA NSSL | Public domain | flickr | https://www.flickr.com/photos/47838549@N08/47953539496 |
| `tornado-street` | Monson tornado damage, June 3, 2011 | MassDOT | Public domain | flickr | https://www.flickr.com/photos/42009447@N05/5793523681 |

## Going live checklist

1. Point the domain's nameservers to `orbit.dns-parking.com` and `horizon.dns-parking.com`.
2. Confirm SSL covers both `nebraskainsuranceappraiser.com` and `www.` (`agency-hosting_websites_get` → `ssl_cert.names`);
   reissue with `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check `http://`, `http://www.` and `https://www.` interior URLs 301 to `https://nebraskainsuranceappraiser.com/…`,
   `/page/index.php` 301s to `/page/`, sitemap URLs return 200, no `X-Robots-Tag` on the real domain, our own `robots.txt`.
   If a www URL returns 200 with `x-hcdn-cache-status: HIT`, clear the cache again.
4. Add the GTM container ID (`GTM_ID`) and wire SMTP once provided; rebuild, validate, deploy, clear cache.
5. In Search Console: verify the **URL-prefix** property `https://nebraskainsuranceappraiser.com/` (HTML file), then submit
   `https://nebraskainsuranceappraiser.com/sitemap.xml`. Keep `googlecccfbf2f7e9e5ae4.html` on the server permanently.
