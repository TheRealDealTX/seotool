# newmexicoinsuranceappraiser.com — static site

New Mexico Insurance Appraiser: a static site with no database and no plugins, built by a Python
generator and served on a Hostinger Agency Growth website (php-fpm, PHP 8.3).

| | |
| --- | --- |
| Hostinger website UID | `3dr5vg4G5` (Agency Growth, order 1008744732, php-fpm 8.3, Phoenix datacenter) |
| Domain | `newmexicoinsuranceappraiser.com` (attached at creation) |
| Preview URL | https://brown-gaur-609134.hostingersite.com |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@newmexicoinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php`, GSC file |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 estimators (markup + copy) |
| `src/learn.py` | Process guide, grouped FAQ, 45-term glossary, 6 reading-room guides |
| `src/photos.json` | Photo manifest: alt text, sizes, **source URL and license** for every photo (internal record) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS upload API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 3dr5vg4G5)
export NMIA_FB_URL=… NMIA_FB_AUTH=… NMIA_FB_REST=…
./deploy.sh
# then: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the
server: `DELETE {upload-url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and
`X-Auth-Rest` headers.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed,
everything else to the root `index.php`): run `php -S 127.0.0.1:8090 router.php` from `public/` with a
small router script like the one described under Hosting notes.

## Pages (52 in sitemap.xml)

- Home, About (`/about-the-company/`), Contact (`/contact-new-mexico-appraiser/`)
- `/appraiser-services/` + 12 services: appraisal demand representation, home, commercial & HOA, hail & roof,
  high wind, water, fire & smoke, **wildfire** (state-specific), **flat roof & stucco** (state-specific),
  winter freeze, estimate review, umpire
- `/cities-we-serve/` + 12 cities: Albuquerque, Las Cruces, Rio Rancho, Santa Fe, Roswell, Farmington, Hobbs,
  Clovis, Carlsbad, Alamogordo, Los Alamos, Ruidoso
- `/claim-estimators/` + 7 tools: claim gap net-recovery estimator, depreciation holdback splitter, roof area &
  pitch converter, percentage deductible converter, claim calendar builder (.ics), appraisal file checkup,
  **wildfire contents inventory estimator** (new). All run in the browser; nothing is stored.
- `/inside-the-appraisal-process/`, `/frequently-asked/`, `/claim-terms-a-to-z/` (searchable), `/reading-room/` + 6 guides
- `/privacy-and-cookies/`, `/terms-of-website-use/`, `/important-notices/`, `/all-site-pages/` (HTML site map), 404
- **No photo-credits page.** All photos are CC0 / public domain; `validate.py` fails if one appears or is linked.

URL slugs, copy, layout, palette and fonts were chosen to differ from every sister `*insuranceappraiser*` site
(checked against all 27 on the Agency account and in this repo). `validate.py` bans every sister-state name
(plus Texas and Colorado) across pages, sitemap, robots, CSS, JS, manifest and `contact.php`.

## Design

- Palette: flag red `#BF0A30` (primary), sun gold `#FFD700` (accent/buttons), deep red `#5E0718`/`#33040D`,
  light tint `#FFF6CC`/`#FFFBEA`, complementary turquoise `#127C80`, sand `#F6F0E4` and charcoal `#1F1A17` neutrals.
- Fonts: **Unbounded** (display) + **DM Sans** (text) — not used by any sister site.
- Squared corners, stepped "terrace" dividers, full-bleed photo hero with a solid lead-form card, gold peril band,
  photo cards with hover zoom, horizontally scrolling region cards, a horizontal process stepper that fills on
  scroll (vertical on mobile), animated counters, staggered reveals, hero/page-hero parallax, header that turns
  solid on scroll, back-to-top button. No progress bar, marquee, 3D tilt or tabs. All motion respects
  `prefers-reduced-motion`; reveals only hide content when JS runs (`html.no-js` is removed by `app.js`).
- Mobile nav: off-canvas drawer (`#drawer`) rendered **outside** the sticky header (the header has no
  `backdrop-filter`), accordion submenus, scroll lock, close on ×/overlay/link/Escape, `inert` + `aria-hidden`,
  shadow/visibility only while open. Fixed mobile call bar.
- Logo mark: red tile, gold stepped roofline and sun disc (deliberately not the Zia symbol). `favicon.svg`,
  `favicon.ico` (16/32/48, bolder art), 96px PNG, full-bleed 180px apple-touch icon, maskable 192/512 PNGs in
  `site.webmanifest`; every icon link has `?v=`. OG image: 1200×630 JPG from a site photo.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` would skip any redirect, so
  `http://www.…/page/` would load with a 200.
- Therefore the homepage is `home.html` and **every other page is `dir/index.php`** whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP.
  There is no root `index.html` and no `dir/index.html` anywhere (`build.py` asserts this, `validate.py` checks it).
- `_guard.php` 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://newmexicoinsuranceappraiser.com` on the real domain only; 301s `/dir/index.php` and `/index.php` to the
  directory; sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL); 404s if requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs without a
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Root static `.html` files allowed: `home.html`, `404.html` and the Search Console file only.
- Hostinger serves its own Googlebot-blocking `robots.txt` on `*.hostingersite.com` preview URLs; that's expected.

## Google Search Console verification file

- File: `public/googlecccfbf2f7e9e5ae4.html`, written by `build.py` (`GSC_FILE` / `GSC_BODY`) on every build.
- Exact contents (one line, no newline, no HTML, no BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- It must stay at the site root permanently: Google rechecks it, and removing it unverifies the URL-prefix
  property `https://newmexicoinsuranceappraiser.com/`. It's excluded from page checks, `sitemap.xml`, the HTML site
  map and internal links, `robots.txt` doesn't block it, and `validate.py` checks it is byte-exact. The host serves
  it directly, so the guard doesn't run for it (expected).

## Photos (internal record — not published on the site)

All photos are **CC0 or public domain only** (no CC BY), found via the Openverse API (`license=cc0,pdm`) and
Wikimedia Commons (license filtered to public domain / CC0). Each is saved as 1200px and 640px WebP
(`static/assets/img/photos/<key>.webp` and `<key>-640.webp`) with `srcset`, `sizes`, width and height. Decorative
backgrounds use `alt=""`. The source URL, creator and license of every photo are in `src/photos.json`; the table
below mirrors it.

PHOTO_TABLE

## Contact form

`/api/contact.php`: honeypot (`website`), per-IP rate limit (5 per 10 minutes), validation (name, email or phone,
consent). Sends through `info@newmexicoinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (starts with `<?php http_response_code(404); exit; ?>`, so it 404s if requested).

The config is **never committed** (`_private/` is in `.gitignore`). Hostinger's file API can't write outside
`public_html`, so it lives at `public_html/api/_private/config.php`:

```php
<?php
if (!defined('NMIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@newmexicoinsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives: upload the config (keep any local copy outside the repo and delete it after),
confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and confirm
the log line shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique
- Meta description present, **110–143 characters**, ends with a full sentence, unique; `og:description` and
  `twitter:description` identical to it
- Exactly one H1, first heading is the H1, no skipped heading levels (footer, sidebar boxes and tools included)
- Valid JSON-LD; one page node (WebPage/AboutPage/ContactPage/CollectionPage) per graph with `breadcrumb`,
  `primaryImageOfPage` and `mainEntity`; ProfessionalService and WebSite present; every `@id` reference resolves
- No broken internal links or anchors, `alt` on every image
- Homepage main content contains "New Mexico Insurance Appraiser" at least 14 times
- No sister-state names, no photo-credits page or link
- Every `dir/index.php` starts with the guard line and has no other PHP; no `index.html` pages
- Search Console file present and byte-exact, and not in the sitemap

## Going live

1. Point the domain's nameservers to `orbit.dns-parking.com` and `horizon.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Verify the www/http/index.php redirects on the live domain, that the real domain sends no `X-Robots-Tag`,
   and that every sitemap URL returns 200. If a www URL returns 200 with `x-hcdn-cache-status: HIT`, clear the cache.
4. In Search Console, verify the **URL-prefix** property `https://newmexicoinsuranceappraiser.com/` (HTML-file
   verification doesn't work for Domain properties), then submit `/sitemap.xml`.
