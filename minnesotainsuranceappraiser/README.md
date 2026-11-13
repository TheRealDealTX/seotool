# minnesotainsuranceappraiser.com — static site

Minnesota Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and a small PHP guard and front controller serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `jSCKKO45I` (Agency Growth, order 1008744732, php-fpm, PHP 8.3) |
| Domain | `minnesotainsuranceappraiser.com` (attached at creation; nameservers not pointed yet) |
| Preview URL | https://paleturquoise-barracuda-248082.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Nameservers to set at the registrar | `hermes.dns-parking.com`, `artemis.dns-parking.com` (from `agency-hosting_websites_get`) |
| Server | `us-phx-h5g-node3.hstgr.io` (requested Boston, nearest to Minnesota; the order's server is in Phoenix) |
| Google Tag Manager | Not set yet. Put the container ID in `GTM_ID` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@minnesotainsuranceappraiser.com (mailbox not created yet) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 11 appraisal solution pages |
| `src/locations.py` | 12 Minnesota city pages (county, neighborhoods, housing, storm history) |
| `src/tools.py` | 7 interactive tools (markup + copy). Logic is in `static/assets/js/app.js` |
| `src/learn.py` | 8-step process guide, grouped FAQ, 50-term glossary, 6 guides |
| `src/photos.json` | Photo metadata (title, creator, license, source, size), used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, manifest, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build checks. Must pass with zero errors |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# Credentials from the Hostinger API: agency-hosting_files_generate-upload-url (website_uid jSCKKO45I). They expire after a few hours.
export MIA_FB_URL='…/api/tus' MIA_FB_AUTH='…' MIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid jSCKKO45I)
```

`deploy.sh` only adds and overwrites files. If you remove or rename a page, delete the old file on the
server: `DELETE {url-without-/tus}/resources/public_html/<path>`, sending the same `X-Auth` and
`X-Auth-Rest` headers.

To preview locally the way the host serves files, run `php -S` with a router script. The router
should serve real files directly, run a directory's `index.php`, and send everything else to
`/index.php`.

## Pages (51 in sitemap, plus 404)

- Home, `/who-we-are/`, `/contact-us/`
- `/appraisal-solutions/` plus 11 solutions: appraisal clause help, home, commercial/HOA, hail & roof,
  tornado/derecho wind, water, fire & smoke, ice dam & winter damage (the Minnesota-specific peril),
  estimate review, umpire, contents
- `/service-area/` plus 12 cities: Minneapolis, St. Paul, Rochester, Duluth, Bloomington, Plymouth,
  Woodbury, Eagan, Blaine, St. Cloud, Mankato, Moorhead
- `/free-tools/` plus 7 tools: claim gap & fee estimator (with break-even), RCV/ACV & holdback,
  roof area & pitch, percentage deductible, claim timeline planner (.ics export), appraisal readiness
  checkup, and roof snow load calculator (new for Minnesota)
- `/appraisal-process-guide/`, `/common-questions/`, `/insurance-terms/` (searchable),
  `/learning-center/` plus 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/photo-credits/`, `/html-sitemap/`, `404.html` (real 404)

The URL slugs, section order, copy, palette and fonts differ from every sister `*insuranceappraiser*`
site. Before building, the Georgia, Florida, Alabama, Arizona, the Carolinas, Missouri, Montana, Nevada,
Wyoming, Ohio, Alaska, Delaware, Maine, Maryland, Massachusetts, Kentucky, New York, New Jersey,
Arkansas and West Virginia builds were all surveyed.

## Design

- **Palette:** navy `#002D5D` (deep `#001833`, lighter `#0B4A8F`), sky `#52C9E8` (link ink `#0B7397`),
  ice tint `#EEF8FC`, amber accent `#F4A93B`, slate neutrals.
- **Fonts:** Schibsted Grotesk for display and Instrument Sans for body. No sister site uses either.
- **Layout:** a full-bleed photo hero with a white lead-form card and a stats band that overlaps it.
  Photo cards for services, tools, seasons and cities. Photo heroes on interior pages. A two-column
  interior layout with a sticky sidebar.
- **Effects:** the header turns solid on scroll, hero and CTA parallax, staggered reveal on scroll,
  animated counters, hover zoom on cards, a process timeline that fills as you scroll, region tabs
  with photos, and a back-to-top button. It deliberately leaves out the marquee, 3D tilt and scroll
  progress bar that Georgia uses. All motion respects `prefers-reduced-motion`, and every section
  renders without JavaScript.
- **Mobile:**
  - The off-canvas drawer `#drawer` sits outside the sticky header, and the header has no
    `backdrop-filter`.
  - It has accordion submenus and locks page scroll while open.
  - It closes on ×, an overlay tap, a link tap or Escape.
  - `inert` and `aria-hidden` are toggled with it.
  - Its shadow and `visibility` apply only while it is open.
  - A fixed call bar sits at the bottom of the screen.
- **Logo:** a navy tile with a sky roof line over a level bar and an amber dot, the "measured roof".
  - The same mark is used in the header, drawer and footer.
  - Brand links are excluded from hover colour changes.
  - Icon files: `favicon.svg`, `favicon.ico` (16/32/48, bolder strokes), a 96px PNG, a full-bleed
    180px apple-touch icon, and maskable 192/512 PNGs listed in `site.webmanifest`.
  - All icon links carry `?v=` cache-busters.
  - `og-image.jpg` is 1200×630 and built from a site photo.

## Photos

35 photos, all royalty-free, found through the Openverse API (`license=cc0,pdm`):

- CC0 from StockSnap, rawpixel, Flickr and Wikimedia Commons.
- Public domain, including USDA and U.S. Fish & Wildlife Service photos.

They were downloaded one at a time with pauses, using 1280px Wikimedia thumbnails. Each is saved as
WebP at up to 1200px and at 640px, served with `srcset`/`sizes`, width and height. Alt text is
descriptive, and decorative backgrounds use `alt=""`. Every photo's license and source is listed on
`/photo-credits/`. The Flickr originals come through Openverse at 1024px, so those are the widest
versions available. Photos showing political figures, text overlays or artwork were skipped.

## Hosting notes (why every page is `dir/index.php`)

- **How the host serves files:**
  - It ignores `.htaccess`.
  - The Agency plan has no "force HTTPS" setting.
  - It serves real files directly, and runs a directory's `index.php` without going through the
    root `index.php`.
  - Only `/` and unknown paths reach the root `index.php`.
- **Page files:** a `dir/index.html` page would skip any redirect logic. Every page is therefore
  written as `dir/index.php`, starting with `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`
  and followed by static HTML that contains no other `<?`. The homepage is `home.html`.
- **Never create a root `index.html` or any `dir/index.html`.** `validate.py` fails the build if one
  exists.
- **What `_guard.php` does:**
  - On the real domain, it 301s `www.` and plain http to `https://minnesotainsuranceappraiser.com`.
    It reads `X-Forwarded-Proto` and falls back to `HTTPS`.
  - It 301s `/dir/index.php` and `/index.php` to the directory URL.
  - On any other host, such as the preview domain, it sends `X-Robots-Tag: noindex, nofollow`.
  - It returns 404 when requested directly.
- **What the root `index.php` front controller does:**
  - Requires the guard.
  - Serves `home.html` for `/`.
  - 301s directory URLs that are missing the trailing slash.
  - Includes `dir/index.php` when a directory URL reaches it.
  - Otherwise returns `404.html` with a real 404 status.
- **Verified locally with a host-like router:**
  - `Host: www.minnesotainsuranceappraiser.com` → `/service-area/duluth/` 301s to the https apex.
  - `X-Forwarded-Proto: http` → `/service-area/duluth/` 301s to the https apex.
  - `/free-tools/index.php` 301s to `/free-tools/`.
- On the preview URL, Hostinger serves its own `robots.txt`, which blocks Googlebot. That is expected.
  The real domain will serve ours.

## SEO rules enforced by `validate.py`

- **Titles:** 60 characters or fewer, and no more than about 580px using Arial metrics at 20px.
  Each title is unique.
- **Meta descriptions:** 110–150 characters. Each description is unique.
- **Headings:** exactly one H1, the first heading is the H1, and no heading level is skipped,
  including in the footer, sidebar and tool widgets.
- **JSON-LD:**
  - It must parse.
  - Every `@id` reference must resolve.
  - Each page needs ProfessionalService and WebSite nodes.
  - Each page needs exactly one page node (WebPage, AboutPage, ContactPage or CollectionPage) that has
    `breadcrumb`, `primaryImageOfPage` and `mainEntity`.
- **Links and images:** no broken internal links or same-page anchors, and every image has an `alt`
  attribute.
- **Homepage keyword:** "Minnesota Insurance Appraiser" must appear at least 14 times in `<main>`.
  It currently appears 17 times.
- **Sister states:** none of the sister-state names may appear in any built text file.
- **Page files:** every `dir/index.php` must start with the guard line and contain no other PHP.
  There must be no `index.html` pages.

**Schema per page type:**

- **ProfessionalService:** logo ImageObject, contactPoint, MN/US address, Minnesota plus the 12
  cities as `areaServed`, and an OfferCatalog of the 11 services.
- **Service pages and location pages:** Service.
- **Pages with FAQs:** FAQPage.
- **Index pages:** ItemList.
- **Tool pages:** WebApplication.
- **Guides:** BlogPosting.
- **Process page:** HowTo.
- **Glossary:** DefinedTermSet.

## Contact form

`/api/contact.php` handles the lead form:

- **Spam and input checks:** a honeypot field (`website`), a per-IP limit of 5 submissions per 10
  minutes, and validation. Name and consent are required, plus a valid email or a phone number.
- **Sending:** it sends through `info@minnesotainsuranceappraiser.com` over authenticated SMTP
  (`smtp.hostinger.com:465`) when `public_html/api/_private/config.php` exists. Otherwise it falls back
  to PHP `mail()`.
- **Backup log:** it always appends a JSON line to `api/_private/leads.log.php`, whose
  `<?php http_response_code(404); exit; ?>` header makes it 404 when requested directly.

The SMTP password is **never committed**. `_private/` is listed in `.gitignore`. To wire it up once the
mailbox exists:

1. Create `config.php` outside the repo:
   ```php
   <?php
   if (!defined('MIA_CONFIG_OK')) { http_response_code(404); exit; }
   return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
           'smtp_user' => 'info@minnesotainsuranceappraiser.com', 'smtp_pass' => '…'];
   ```
2. Upload it to `public_html/api/_private/config.php` with the TUS API, then delete the local copy.
3. Confirm that `https://<host>/api/_private/config.php` returns 404 with 0 bytes.
4. Send one submission marked as a test.
5. Confirm the log line shows `"via":"smtp"`.

## Google Tag Manager

Set `GTM_ID = "GTM-XXXXXXX"` in `build.py`. The standard head snippet is then printed right after
`<head>`, and the `<noscript>` iframe right after `<body>`. Then rebuild, validate, deploy and clear
the cache.

## Going-live checklist

1. Point the domain's nameservers to `hermes.dns-parking.com` and `artemis.dns-parking.com`.
2. Confirm SSL covers both the apex and `www`.
   - Check with `agency-hosting_websites_get` → `ssl_cert.names`.
   - If `www` is missing, run `agency-hosting_ssl_reinstall-website`.
3. Re-check the redirects on the live domain, on the homepage and at least three interior pages:
   - `http://`, `http://www.` and `https://www.` all 301 to `https://minnesotainsuranceappraiser.com/…`.
   - `/page/index.php` 301s to `/page/`.
   - Every sitemap URL returns 200.
   - There is no `X-Robots-Tag`, and our own `robots.txt` is served.
   - If a `www` URL returns 200 with `x-hcdn-cache-status: HIT`, clear the cache and check again.
4. Add the GTM container, and wire SMTP once the mailbox exists.
5. Submit `https://minnesotainsuranceappraiser.com/sitemap.xml` to Google Search Console.
