# marylandinsuranceappraiser.com — static site

Maryland Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and
a small PHP guard and front controller serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `vYLlD8zwQ` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, created Nov 12, 2026) |
| Domain | `marylandinsuranceappraiser.com` (attached at creation; SSL issues once DNS points here) |
| Preview URL | https://darkred-pigeon-443632.hostingersite.com (do live checks here until DNS moves) |
| Nameservers to set at the registrar | `atlas.dns-parking.com`, `hyperion.dns-parking.com` |
| Server | `us-phx-h5g-node3.hstgr.io`, IP 72.60.128.114 (Boston was requested; the order's server hosts the site) |
| Google Tag Manager | Not set. Fill in `GTM_ID` in `build.py` to output the head snippet and the `<noscript>` iframe |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@marylandinsuranceappraiser.com (mailbox still to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 Maryland location pages |
| `src/tools.py` | 7 calculators (markup and copy). The math is in `static/assets/js/app.js` |
| `src/learn.py` | Process steps and guide, grouped FAQ, 40-term glossary, 6 knowledge-base guides |
| `src/media.py` | Alt text and which photo goes on which page; homepage regions |
| `src/photos.json` | Photo metadata (title, creator, license, source, size), used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |
| `tools/make_icons.py` | Rebuilds `favicon.svg/.ico`, 96px PNG, apple-touch-icon, maskable 192/512 PNGs, manifest and the OG image |
| `tools/router.php` | Local router that copies how the host serves files, for testing the guard |
| `CONTENT_BRIEF.md` | Writing rules and the Maryland fact sheet the copy was written from |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # validate must end with no ERROR lines
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid vYLlD8zwQ)
export MIA_FB_URL='…/api/tus' MIA_FB_AUTH='…' MIA_FB_REST='…'
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If you remove or rename a page, delete the old file on the server with
`DELETE {MIA_FB_URL without /tus}/resources/public_html/<path>` and the same two auth headers.

Local preview that behaves like the host (guard included):

```sh
php -S 127.0.0.1:8090 -t public tools/router.php
curl -sI -H 'Host: www.marylandinsuranceappraiser.com' http://127.0.0.1:8090/service-locations/annapolis/   # 301 to https apex
```

## Pages (52 in the sitemap, plus 404)

- Home, About (`/about-the-firm/`), Contact (`/start-a-claim-review/`)
- `/property-claim-services/` + 12 services: appraisal demand representation, home, commercial & HOA, roof & hail,
  windstorm & tornado, hurricane & nor’easter, water, fire & smoke, snow/ice dam/freeze (the Maryland peril),
  tree impact, carrier estimate review, neutral umpire
- `/service-locations/` + 12 cities: Baltimore, Towson, Ellicott City, Annapolis, Frederick, Rockville, Bowie,
  Waldorf, Hagerstown, Cumberland, Salisbury, Ocean City
- `/appraisal-calculators/` + 7 tools: claim gap & fee estimator, RCV/ACV & holdback worksheet, roof square & pitch,
  hurricane deductible, claim timeline planner (.ics export), appraisal readiness checklist, snow & ice roof load
  estimator (the new tool)
- `/the-appraisal-process/` (HowTo), `/common-questions/` (22 Q&As in 5 topics), `/appraisal-glossary/` (40 terms,
  searchable), `/knowledge-base/` + 6 guides
- `/privacy-practices/`, `/site-terms/`, `/important-disclaimer/`, `/photo-credits/`, `/all-pages/` (HTML site map),
  `404.html` (served with a real 404), `sitemap.xml`, `robots.txt`

The URL scheme, copy, section order and design differ on purpose from the eleven sister sites (AL, AZ, FL, GA, MA,
MO, MT, NV, NC, WV, WY). `validate.py` fails the build if any of those state names appears in any shipped file.

## Design

- **Palette:** olive `#2E2910` (main), deep `#1a1708`, mid `#4a4421`, brass `#b39a45` / `#d9c27a`,
  parchment tint `#f5f2e6`, and a complementary Chesapeake blue accent `#2f6b8f` (deep `#1f4b66`).
- **Fonts:** Young Serif (display) and Hanken Grotesk (body). No sister site uses either.
- **Logo:** a roof chevron over a house outline and a Bay wave line, in olive, brass and blue. It is the same SVG
  in the header, drawer and footer. The brand link never changes color or underlines on hover.
- **Layout:** a full-bleed photo hero with a lead-form card, and a counter ribbon that overlaps the hero. Then an
  editorial intro with a numbered list, a scroll-snap service rail with arrow buttons, and appraisal fit / not-fit
  panels. Then a horizontal process stepper that fills as you scroll, expanding region panels, calculator rows next
  to an inline gap check, and photo location cards. Then a comparison table, FAQ, guides, a parallax CTA and the
  contact form. Interior pages have a photo hero and two columns with a sticky sidebar (call box and related links).
- **Effects:** the header turns solid on scroll, hero and CTA parallax, staggered reveal, animated counters, hover
  zoom on cards, the process fill and a back-to-top button. Everything respects `prefers-reduced-motion`, and pages
  render fully without JavaScript (reveal styles only apply under `html.js`).
- **Mobile:** an off-canvas drawer outside the sticky header with:
  - accordion submenus
  - scroll lock while open
  - closing with ×, an overlay tap, a link tap or Escape
  - `inert` and `aria-hidden` handling
  - shadow and visibility applied only while open

  A fixed call bar sits at the bottom of the screen.

## Photos

40 photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`). Sources are Flickr
(Baltimore Heritage, USDA, U.S. Fish & Wildlife, MassDOT and others), StockSnap, rawpixel (including Library of
Congress / Carol M. Highsmith) and the WordPress Photo Directory. They were downloaded one at a time with pauses.
Wikimedia was rate-limiting during sourcing, so nothing was taken from it. Every photo is reviewed on contact sheets
labelled by key, and all are listed with license and source on `/photo-credits/`.

Each photo is served as `<key>.webp` at its native width (the Openverse originals are 960–1024px, so none were
upscaled to 1200) and as `<key>-640.webp`, with `srcset`, `sizes`, `width` and `height`. Decorative backgrounds use
`alt=""`. The OG image is 1200×630, built from the Bay Bridge hero photo.

## Hosting notes (canonical-host guard)

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting. It **serves real files directly**,
  running a directory's `index.php`, and sends `/` and unknown paths to the root `index.php`. A `dir/index.html`
  page would therefore skip any redirect logic, and `http://www.…/any-page/` would load with a 200.
- So every page is written as `dir/index.php`. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML that contains no other
  PHP. The homepage is `home.html`. There is no root `index.html`, and `deploy.sh` refuses to upload any
  `index.html`.
- `_guard.php`:
  - 301-redirects `www.` and plain http (read from `X-Forwarded-Proto`, falling back to `HTTPS`) to
    `https://marylandinsuranceappraiser.com`, on the real domain only
  - 301-redirects `/dir/index.php` and `/index.php` to the directory
  - sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview URL
  - returns 404 when requested directly
- The root `index.php` front controller requires the same guard. It serves `home.html` for `/`, adds the trailing
  slash on directory URLs with a 301, includes `dir/index.php` for directory URLs that reach it, and returns
  `404.html` with a real 404.
- On the preview URL Hostinger serves its own robots.txt that blocks Googlebot. That's expected; ours is served on
  the real domain.
- Hostinger's placeholder `public_html/default.php` was deleted.

## SEO rules enforced by validate.py

- Every page file (`dir/index.php`) starts with the guard line and contains no other PHP; no `index.html` exists
- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; all unique
- Exactly one H1, the first heading is the H1, and no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD; each graph has ProfessionalService, WebSite and exactly one page node; every `@id` reference resolves
- No broken internal links or anchors; every image has `alt`
- "Maryland Insurance Appraiser" appears at least 14 times in the homepage `<main>` (currently 18, or 23 with the
  header and footer)
- No sister-state names anywhere in the build

Each page's JSON-LD graph holds:
- the ProfessionalService: logo ImageObject, contactPoint, MD/US address, the state and cities as areaServed, and
  an OfferCatalog of the 12 services
- the WebSite
- one page node (WebPage, AboutPage, ContactPage or CollectionPage) linked to its BreadcrumbList, primary image
  and main entity

Where they apply, graphs also include Service (services and locations), FAQPage, ItemList (index pages),
WebApplication (tools), BlogPosting (guides), HowTo (process) and DefinedTermSet (glossary).

## Contact form

`/api/contact.php` has a honeypot field, a per-IP limit of 5 submissions per 10 minutes, and validation (it needs a
name, a valid email or a phone number, and consent). It sends through `info@marylandinsuranceappraiser.com` over
authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, and falls back to PHP
`mail()` otherwise. It always appends a JSON line, including `"via"`, to `api/_private/leads.log.php`. That log
starts with a `<?php … exit;` header, so requesting it returns a 404 with 0 bytes.

**Credentials are never committed** (`_private/` is in `.gitignore`). When the mailbox exists, upload this file to
`public_html/api/_private/config.php`, keeping any local copy outside the repo and deleting it after upload:

```php
<?php
if (!defined('MIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@marylandinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then:
1. Confirm the config URL returns 404 with 0 bytes.
2. Send one submission labelled as a test.
3. Confirm the log line shows `"via":"smtp"`.

## Go-live checklist

1. Point the domain's nameservers to `atlas.dns-parking.com` and `hyperion.dns-parking.com`.
2. Once it resolves, confirm SSL is active and covers both the apex and `www` (`agency-hosting_websites_get` →
   `ssl_cert.names`). If `www` is missing, reissue with `agency-hosting_ssl_reinstall-website`.
3. On the homepage and at least three interior pages, check:
   - `http://`, `http://www.` and `https://www.` all 301 to `https://marylandinsuranceappraiser.com/…`
   - `/page/index.php` 301s to `/page/`
   - every sitemap URL returns 200
   - there's no `X-Robots-Tag` on the real domain, and our own robots.txt is served

   If a www URL still returns 200 with `x-hcdn-cache-status: HIT`, clear the cache again.
4. Add the GTM ID, set up SMTP (above), rebuild, validate, redeploy and clear the cache.
5. Submit `https://marylandinsuranceappraiser.com/sitemap.xml` to Google Search Console.
