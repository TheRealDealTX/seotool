# delawareinsuranceappraiser.com — static site

Delaware Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served by a small PHP front controller on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `mnkyxd7Sn` (Agency Growth, order 1008744732, php-fpm, PHP 8.3) |
| Domain | `delawareinsuranceappraiser.com` (attached at creation; www and http 301 to https apex) |
| Preview URL | https://seashell-ostrich-882608.hostingersite.com (Hostinger serves its own noindex `robots.txt` here) |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Server | `us-phx-h5g-node3.hstgr.io` (Boston was requested; the order's sites all live on this node) |
| Google Tag Manager | not set — `GTM_ID = ""` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@delawareinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Delaware community pages |
| `src/tools.py` | 7 interactive worksheets (markup + copy) |
| `src/learn.py` | Appraisal roadmap, grouped FAQ, 42-term glossary, 6 journal articles |
| `src/photos.json` | Photo metadata (title, creator, license, source, size) used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `scripts/make_icons.py` | Draws the brand mark → `favicon.svg`, `favicon.ico` (16/32/48, bold variant), PNGs, manifest |
| `scripts/make_og.py` | Builds the 1200×630 `og-image.jpg` from a site photo |
| `public/` | **Build output** — this is what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid mnkyxd7Sn)
export DIA_FB_URL=… DIA_FB_AUTH=… DIA_FB_REST=…
./deploy.sh        # then clear the cache: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`DELETE {DIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` / `X-Auth-Rest` headers.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed,
everything else to `index.php`): run `php -S 127.0.0.1:8090 router.php` from `public/` with a router like
the one described under *Hosting notes*.

## Pages (51 in sitemap + 404)

URL slugs were chosen so none match the sister sites:

- Home `/`, `/our-practice/` (about), `/start-your-review/` (contact)
- `/appraisal-expertise/` + 11 services (appraisal clause, homeowners, commercial/condo/HOA, roof & hail,
  wind & tornado, hurricane & coastal storm, pipe & water loss, fire & smoke, nor’easter & winter storm,
  carrier estimate review, umpire)
- `/serving-delaware/` + 12 communities: Wilmington, Dover, Newark, Middletown, Bear, Smyrna, Milford,
  Georgetown, Seaford, Lewes, Rehoboth Beach, Bethany Beach (county, neighborhoods, housing mix, storm history)
- `/claim-worksheets/` + 7 worksheets: claim gap & fee estimator, depreciation holdback worksheet, roof pitch &
  squares, named-storm deductible worksheet, policy deadline calendar (.ics export), appraisal readiness check,
  and the Delaware-specific wind vs. flood split estimator
- `/how-the-appraisal-panel-works/` (HowTo), `/delaware-appraisal-faq/` (grouped), `/claim-terms-explained/`
  (searchable glossary), `/appraisal-journal/` + 6 guides
- `/privacy-practices/`, `/terms-of-service-de/`, `/important-disclaimer/`, `/photo-credits/`,
  `/browse-all-pages/` (HTML site map), `404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- Palette: slate `#233D4D` (brand), deep `#142530`, ink `#0D1A22`, tint `#E6EEF2`, mist `#F3F7F9`,
  sand `#F8F3ED`; complementary coral accent `#F0795B` (buttons use the darker `#C24A2C` for contrast).
- Fonts: **Sora** (display) + **Nunito Sans** (body) — not used by any sister site.
- Logo: slate tile with a white roofline/house and a coral “balance” bar; same SVG in header, drawer and footer.
- Layout: full-bleed photo hero (slow zoom) with a quick lead form; an overlapping counter “ledger”; three-county
  tabs with photos; photo service/worksheet/journal cards (hover zoom); a dark gap-check band; a sticky-heading
  roadmap whose line fills as you scroll; a horizontal storm-record strip; community photo tiles; interior photo
  heroes with a two-column layout and sticky sidebar (call box + related links).
- Effects: scroll progress bar, header that compacts on scroll, staggered reveals, counters, back-to-top.
  No marquee, tilt or parallax. Everything respects `prefers-reduced-motion`; without JS all content
  (including all three county panels) still renders.
- Mobile: off-canvas drawer rendered **outside** the sticky header (no `backdrop-filter` anywhere), accordion
  submenus, scroll lock, close on × / overlay / link / Escape, `inert` + `aria-hidden`, shadow and visibility only
  while open. Fixed call bar at the bottom.

## Photos

Every photo is CC0 or public domain, found through the Openverse API (`license=cc0,pdm`) and other
public-domain sources, downloaded one at a time with pauses. Each is served as 1200px and 640px WebP with
`srcset`/`sizes` and width/height. Sources and licenses are listed on `/photo-credits/`.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan “force HTTPS” setting, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` would skip any redirect logic.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP).
  The homepage is `home.html`, served by the front controller. There is no root `index.html` and there must
  never be a `dir/index.html` on the server (`validate.py` fails the build if one exists).
- `_guard.php`: 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://delawareinsuranceappraiser.com` on the real domain only; 301s `/dir/index.php` (and `/index.php`) to
  `/dir/`; sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL); 404s if requested directly.
- `index.php` front controller: requires the guard, serves `home.html` for `/`, adds the trailing slash to
  directory URLs (301), includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a
  real 404 status.

## Contact form

`/api/contact.php` has a honeypot (`website`), a per-IP limit (5 per 10 minutes) and validation (name,
email or phone, consent). It sends through `info@delawareinsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends
a JSON line to `api/_private/leads.log.php`. Both private files 404 when requested (config define-guard; the log
starts with `<?php http_response_code(404); exit; ?>`). They live inside `public_html` because the file API can’t
write outside it. `_private/` is git-ignored — **never commit credentials**. Config format:

```php
<?php
if (!defined('DIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@delawareinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading it: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled
as a test, and confirm the log line shows `"via":"smtp"`. Delete any local copy of the config.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; both unique
- Exactly one H1, first heading is the H1, no skipped heading levels anywhere (footer, sidebar, tools included)
- Valid JSON-LD; every `@id` reference resolves; graph holds ProfessionalService + WebSite + exactly one page node
  (WebPage/AboutPage/ContactPage/CollectionPage) with `breadcrumb`, `primaryImageOfPage` and `mainEntity`
- Canonical to `https://delawareinsuranceappraiser.com/…`, OG image size + alt, Twitter card, `geo.region`
- No broken internal links or anchors; `alt` on every image
- Homepage main content mentions “Delaware Insurance Appraiser” at least 14 times
- No sister-state names anywhere in the build (Alabama, Florida, Georgia, Arizona, Missouri, Montana, Nevada,
  North Carolina, West Virginia, Wyoming, Massachusetts)
- Every `dir/index.php` starts with the guard line and contains no other PHP; no `index.html` files

JSON-LD per page: ProfessionalService (logo ImageObject, contactPoint, DE address region, state + cities as
`areaServed`, OfferCatalog of services), WebSite, the page node and BreadcrumbList, plus Service (service and
community pages), FAQPage, ItemList (index pages), WebApplication (worksheets), BlogPosting (journal), HowTo
(roadmap) and DefinedTermSet (glossary).

## Go-live checklist

1. Point the domain’s nameservers to `nova.dns-parking.com` and `cosmos.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check `http://`, `http://www.` and `https://www.` interior URLs 301 to the https apex, `/page/index.php` 301s to
   `/page/`, every sitemap URL returns 200, and the real domain sends no `X-Robots-Tag`.
4. Add GTM and the SMTP config when available, re-run `validate.py`, redeploy, clear the cache.
5. Submit `https://delawareinsuranceappraiser.com/sitemap.xml` to Google Search Console.
