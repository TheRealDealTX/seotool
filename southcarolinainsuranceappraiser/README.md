# southcarolinainsuranceappraiser.com — static site

South Carolina Insurance Appraiser: a static site with no database and no plugins, built by a
Python generator and served by a tiny PHP front controller on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `RKnVWfGN0` (Agency Growth, order 1008744732, php-fpm, PHP 8.3; created with datacenter `boston`, server reports `us-phx-h5g-node3`) |
| Domain | `southcarolinainsuranceappraiser.com` (attached at creation) |
| Preview URL | https://red-snail-854335.hostingersite.com (Hostinger serves its own Googlebot-blocking robots.txt here; our pages also send `X-Robots-Tag: noindex, nofollow` on any non-canonical host) |
| Nameservers to set at the registrar | `helios.dns-parking.com`, `aster.dns-parking.com` (from `agency-hosting_websites_get`) |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@southcarolinainsuranceappraiser.com |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 South Carolina location pages (county, region, neighborhoods, housing, storms) |
| `src/tools.py` | 7 interactive tools (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 steps), FAQ (5 topics), glossary (43 terms), 6 guides |
| `src/photos.json` | Photo metadata (title, creator, license, source, alt, size), written by `tools/photos.py` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** — what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` via the TUS file API |
| `tools/make_icons.py` | Favicon/logo pipeline |
| `tools/photos.py` | Photo pipeline (download → 1200/640 WebP → `photos.json`) |
| `tools/router.php` | `php -S` router that mimics the host, for local testing |
| `tools/shots.js`, `tools/qa.js` | Playwright screenshots/layout checks and functional QA (tool math, drawer, logo hover) |
| `CONTENT_BRIEF.md` | Copy rules and South Carolina facts used to write `src/` |

## Build, test, deploy

```sh
python3 build.py && python3 validate.py          # zero errors required
cd public && php -S 127.0.0.1:8099 ../tools/router.php   # local preview (restart after each build)
node tools/qa.js http://127.0.0.1:8099            # tool math, drawer, logo hover
node tools/shots.js http://127.0.0.1:8099 /tmp/shots   # screenshots + scrollWidth/image checks
```

Deploy (credentials from `agency-hosting_files_generate-upload-url`, website_uid `RKnVWfGN0`; they expire):

```sh
export SCIA_FB_URL='https://…/tus' SCIA_FB_AUTH='…' SCIA_FB_REST='…'
./deploy.sh        # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the
server: `DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.

## Pages (52 in sitemap)

- Home, `/about-the-firm/`, `/contact-an-appraiser/`
- `/claim-dispute-services/` + 12 services
- `/locations-served/` + 12 cities (`/locations-served/<city>/`)
- `/free-claim-tools/` + 7 tools: claim gap & fee estimator, RCV vs. ACV holdback calculator, roof area & pitch
  estimator, hurricane deductible calculator, claim timeline builder (.ics export), appraisal readiness checkup,
  wind vs. flood damage splitter
- `/appraisal-process-explained/`, `/insurance-appraisal-faq/`, `/appraisal-glossary/`, `/appraisal-guides/` + 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/photo-credits/`, `/site-index/`, `404.html` (real 404 status), `sitemap.xml`, `robots.txt`

URL slugs, section order, copy, palette and fonts were chosen to differ from all 16 sister `*insuranceappraiser*`
sites on the Agency account.

## Design

Dark blue base (`#153a70`, deep `#0a1f3f`, darkest `#06142b`), pale harbor tint (`#e9f0f9`), copper accent
(`#c2773a` / `#9a5823`), warm sand neutral (`#f8f5f0`). Newsreader (serif display) + Albert Sans (text).
Squared, editorial look: thin rules, copper kicker lines, 4–8px radii, no glass.

Effects: header turns solid on scroll, hero and CTA parallax, staggered reveal, animated counters (ledger band),
hover zoom on photo cards, a marquee of all 46 counties, and a back-to-top button. All motion respects
`prefers-reduced-motion`; reveals only hide content once JS has run, so the site renders fully without JS.

Mobile nav is an off-canvas drawer (`#drawer`) rendered **outside** the sticky header (the header has no
`backdrop-filter`), with accordion submenus, scroll lock, `inert`/`aria-hidden` handling, and close on ×,
overlay tap, link tap or Escape. Its shadow and visibility apply only while open. A fixed call bar sits at the
bottom on phones. The brand link never changes color or underlines on hover.

## Photos

All photos are royalty-free: CC0 or public domain (U.S. government agencies, Flickr CC0/PD, rawpixel,
Wikimedia Commons PD), found with the Openverse API (`license=cc0,pdm`). Candidates were reviewed on labelled
contact sheets (330px thumbnails, fetched one at a time with pauses); originals come from Wikimedia at the
standard 1280px thumbnail width (falling back to the pre-rendered 960px width when Wikimedia refuses an on-demand
render) or Flickr's 1024px size; StockSnap's CDN tops out at 960px. Sources under 1200px are upscaled with Lanczos
so every photo ships as one 3:2 size set. There are no usable CC0/PD photos of Columbia, Greenville, Spartanburg,
Rock Hill, Summerville, Florence or Aiken, so those pages use relevant generic photos (flooding, Upstate storm
clouds, homes, live oaks, ice storm) with honest alt text. Each is served as 1200px and 640px WebP with
`srcset`/`sizes` and width/height; decorative backgrounds use `alt=""`. Every photo is listed with its license and
source on `/photo-credits/`. Rerun with `python3 -I tools/photos.py candidates.json selection.json`.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly**
  (running a directory's `index.php`) — it only routes `/` and unknown paths to the root `index.php`.
- So every page is `dir/index.php` whose first line is `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`
  followed by static HTML with no other PHP. A `dir/index.html` would be served without PHP and skip the guard,
  so **never create a root `index.html` or any `dir/index.html`**. The homepage is `home.html`, served by `index.php`.
- `_guard.php` 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://southcarolinainsuranceappraiser.com` — only on the real domain — 301s `/dir/index.php` (and `/index.php`)
  to `/dir/`, sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview domain), and 404s if requested directly.
- `index.php` requires the same guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.
- `validate.py` checks every `dir/index.php` starts with the guard line and has no other PHP tag.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form

`/api/contact.php`: honeypot field, per-IP rate limit (5 per 10 minutes), validation (name, consent, and a valid
email or phone). It sends through `info@southcarolinainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a
JSON line to `api/_private/leads.log.php` (`"via":"smtp"` when SMTP worked).

Both private files 404 when requested directly: the log starts with `<?php http_response_code(404); exit; ?>`
and the config with a defines-guard. They live inside `public_html` because Hostinger's file API can't write
outside it. **Never commit credentials** — `_private/` is git-ignored; keep any local copy of the config outside
the repo and delete it once uploaded:

```php
<?php
if (!defined('SCIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@southcarolinainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Once uploaded: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a
test, and confirm the log shows `"via":"smtp"`.

## Google Tag Manager

`GTM_ID` in `build.py` is empty by default. Set it (exactly as provided) and rebuild: the head snippet is output
right after `<meta charset>` and the `<noscript>` iframe right after `<body>` on every page.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; both unique
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; ProfessionalService + WebSite + exactly one page node
  (WebPage/AboutPage/ContactPage/CollectionPage) with `breadcrumb`, `primaryImageOfPage` and `mainEntity`
- Canonical to `https://southcarolinainsuranceappraiser.com/…`, OG image size/alt, Twitter card, `geo.region` US-SC
- No broken internal links or anchors; `alt` on every image
- Homepage main content mentions "South Carolina Insurance Appraiser" at least 14 times
- No sister-state names (Alabama, Arizona, Florida, Georgia, Missouri, Montana, Nevada, North Carolina, Wyoming,
  West Virginia, Massachusetts, Maryland, Maine, Delaware, New York, Kentucky) anywhere in the build

Schema per page: ProfessionalService (logo ImageObject, contactPoint, SC address region, state + 12 cities as
`areaServed`, OfferCatalog of the 12 services), WebSite, one page node, BreadcrumbList, plus Service (service and
location pages), FAQPage, ItemList (index pages), WebApplication (tools), BlogPosting (guides), HowTo (process)
and DefinedTermSet (glossary).

## Going live checklist

1. Point the domain's nameservers to the two above.
2. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check http/www/`index.php` 301s on the live domain and that the real domain sends no `X-Robots-Tag`.
4. Create the mailbox, upload `api/_private/config.php`, run the SMTP test above.
5. Add GTM if wanted, rebuild, validate, redeploy, clear cache.
6. Submit `https://southcarolinainsuranceappraiser.com/sitemap.xml` to Google Search Console.
