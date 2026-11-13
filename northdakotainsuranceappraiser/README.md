# northdakotainsuranceappraiser.com — static site

North Dakota Insurance Appraiser: a static site with no database and no plugins. It is built by a
Python generator and served through a small PHP guard + front controller on a Hostinger Agency
Growth website. It was started from the `georgiainsuranceappraiser/` engine (generator, `validate.py`,
`deploy.sh`, `api/contact.php`, tool logic, canonical-host guard), but the copy, URL slugs and
design are new and differ from every sister site.

| | |
| --- | --- |
| Hostinger website UID | `Hw07YkBDa` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Live domain | https://northdakotainsuranceappraiser.com — live since Nov 13, 2026; SSL covers apex + `www` (expires 2027-02-11, auto-renewed by Hostinger); www and http 301 to the apex |
| Preview URL | https://lightpink-ram-106624.hostingersite.com (sends `X-Robots-Tag: noindex`; Hostinger serves its own robots.txt here) |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` (as reported by `agency-hosting_websites_get`) |
| Server | `us-phx-h5g-node3.hstgr.io`, IPv4 72.60.128.114 |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@northdakotainsuranceappraiser.com — form delivers over SMTP (tested Nov 13, 2026, `"via":"smtp"`) |
| Google Tag Manager | `GTM-T28JCQDJ` — head snippet exactly as supplied (`GTM_HEAD` in `build.py`) + noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema graph, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide (8 stages), grouped FAQ, 44-term glossary, 6 handbook guides |
| `src/photos.json` | Photo metadata (title, creator, license, source URL, size) used by `img()`; the source record for every photo |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** — what gets deployed (committed) |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |
| `tools/make_icons.py` | Favicon/manifest icon + OG image pipeline |
| `tools/router.php` | Local router that mimics the host, for `php -S` testing |
| `tools/shots.js` | Playwright screenshots + overflow / broken-image checks |

## Build & deploy

```sh
python3 tools/make_icons.py        # only when the mark or OG photo changes
python3 build.py && python3 validate.py
# creds: agency-hosting_files_generate-upload-url (website_uid Hw07YkBDa)
export NDIA_FB_URL=… NDIA_FB_AUTH=… NDIA_FB_REST=…
./deploy.sh                        # then agency-hosting_cache_clear-website
```

Local preview that behaves like the host:

```sh
cd public && php -S 127.0.0.1:8080 ../tools/router.php
```

## Pages (50 in sitemap.xml)

- Home, `/firm-overview/` (about), `/request-an-appraisal/` (contact)
- `/appraisal-representation/` + 11 services (appraisal clause, homeowner, commercial/HOA/multifamily,
  hail & roof, wind/derecho/tornado, water, fire & smoke, freeze/ice dam/snow load, farm & ranch
  buildings, estimate review, umpire). There is no hurricane page — not a North Dakota peril.
- `/across-north-dakota/` + 12 cities (Fargo, West Fargo, Bismarck, Mandan, Grand Forks, Minot,
  Williston, Dickinson, Jamestown, Wahpeton, Devils Lake, Valley City)
- `/claim-planning-tools/` + 7 tools: claim gap & fee estimator (with break-even point), RCV/ACV
  holdback, roof pitch & squares (with eave ice-barrier courses), percentage deductible, claim
  timeline planner (.ics export, construction-season reminder), appraisal readiness check, roof snow
  load estimator (new for this state)
- `/how-an-appraisal-unfolds/` (HowTo), `/policyholder-faq/` (grouped), `/appraisal-terms-a-z/`
  (searchable glossary), `/claim-handbook/` + 6 guides
- `/your-privacy/`, `/conditions-of-use/`, `/not-legal-advice/`, `/every-page/`
  (HTML site map), `404.html` (served with a real 404), `sitemap.xml`, `robots.txt`

## Design

Navy `#002A86` (deep `#001A54`, darkest `#00113A`, tint `#EAF0FC`) with gold `#FFD12B`
(soft `#FFF4C7`), a prairie-rust accent `#C8553D` used only for warnings/"no" states, and stone
`#F6F4EF` neutrals. Fonts: **Epilogue** (display) + **Instrument Sans** (body) — not used by any
sister site. Style: crisp 6px-radius cards with an offset gold "hard shadow" on hover, numbered
section labels, gold CTA strips.

Effects: scroll progress bar, header that turns solid on scroll, slow hero zoom, staggered reveal,
animated counters, hover zoom on photo cards, a horizontal process route that fills as you scroll
(vertical on mobile), region tabs with photos, back-to-top. No marquee, 3D tilt or parallax.
Everything respects `prefers-reduced-motion`, and content is visible without JavaScript (reveal
styles only apply once JS removes `no-js`).

Mobile nav: an off-canvas drawer (`#drawer`) rendered **outside** the fixed header (no
`backdrop-filter` anywhere), accordion submenus, scroll lock, closes on ×, overlay tap, link tap or
Escape, `inert`/`aria-hidden` toggled, and its shadow/visibility applied only while open. A fixed call
bar sits at the bottom on phones. The brand link never changes color or underlines on hover.

## Photos

38 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`):
Carol M. Highsmith's Library of Congress photographs (via rawpixel, clean 1024px files), Wikimedia
Commons (standard 330px thumbs for contact sheets, 1280px thumbs for finals, one request at a time
with backoff), StockSnap and rawpixel CC0 stock. Each is saved as 1200px and 640px WebP with
`srcset`/`sizes`/width/height. rawpixel's `image_1300` files are watermarked — use `editor_1024`.
The public photo-credits page was removed at the owner's request on Nov 13, 2026 (and deleted from the server); `src/photos.json` keeps each photo's license and source.

## Hosting notes (canonical-host guard)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files
  directly** (running a directory's `index.php`) without going through the root `index.php`.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other `<?`).
  A `dir/index.html` would be served without PHP and skip the redirects — never create one, and never
  add a root `index.html`. The homepage is `home.html`, served by `index.php`.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://northdakotainsuranceappraiser.com` (only on the real domain), 301s `/dir/index.php` to
  `/dir/`, sends `X-Robots-Tag: noindex, nofollow` on any other host (the preview URL), and 404s if
  requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing
  slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a 404.
- `deploy.sh` only adds/overwrites. When a page is removed or renamed, delete it on the server:
  `DELETE {url-without-/tus}/resources/public_html/<path>` with the same two auth headers.
- Server-only files, never in git — leave them in place: `api/_private/config.php` (SMTP), `api/_private/leads.log.php`, and `googlecccfbf2f7e9e5ae4.html` (Google Search Console verification, uploaded Nov 13, 2026).

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters;
  titles and descriptions unique
- Exactly one H1, first heading is the H1, no skipped levels (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; exactly one page node with breadcrumb,
  primaryImageOfPage and mainEntity
- No broken internal links or anchors; every image has `alt`
- "North Dakota Insurance Appraiser" appears ≥ 14 times in the homepage `<main>`
- No sister-state names anywhere in the build ("Missouri River" is the one allowed phrase —
  it runs through Bismarck-Mandan)
- Every `dir/index.php` starts with the guard line and contains no other PHP

Schema per page: ProfessionalService (logo ImageObject, contactPoint, ND address region, state +
cities as areaServed, OfferCatalog), WebSite, one page node (WebPage/AboutPage/ContactPage/
CollectionPage) linked to its BreadcrumbList, plus Service, FAQPage, ItemList, WebApplication,
BlogPosting, HowTo or DefinedTermSet where they apply.

## Contact form delivery

`/api/contact.php` has a honeypot, a per-IP rate limit (5 per 10 minutes) and validation. It sends
through `info@northdakotainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (whose `<?php http_response_code(404); exit; ?>` header makes it 404).
The SMTP password is **never committed** (`_private/` is git-ignored). Upload this file to
`public_html/api/_private/config.php` once the mailbox exists, then delete any local copy:

```php
<?php
if (!defined('NDIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@northdakotainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test, and
check the log shows `"via":"smtp"`.

## Going live checklist

1. ~~Point the nameservers~~ — done; SSL issued for apex + `www`.
2. ~~Check http/www/`index.php` 301s on the live domain (home + 3 interior pages), sitemap URLs 200, no `X-Robots-Tag`, own robots.txt~~ — done Nov 13, 2026.
3. ~~Create the mailbox, upload the SMTP config, send a test lead~~ — done; config URL returns 404 / 0 bytes.
4. ~~Add GTM~~ — done (`GTM-T28JCQDJ`).
5. Submit `https://northdakotainsuranceappraiser.com/sitemap.xml` to Google Search Console.
