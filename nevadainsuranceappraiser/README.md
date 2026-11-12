# nevadainsuranceappraiser.com — static site

Nevada Insurance Appraiser is a static site with no database and no plugins. A Python generator builds it,
and a small PHP front controller serves it on a Hostinger Agency Growth website.
The engineering came from `georgiainsuranceappraiser/` (generator pattern, `validate.py`, `deploy.sh`,
`api/contact.php`, tool logic, favicon and photo pipelines). The copy, URL slugs, palette, fonts, layout
and effects are new and differ from every sister site (Alabama, Florida, Georgia, North Carolina).

| | |
| --- | --- |
| Hostinger website UID | `pUs9TSRI1` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Live domain | https://nevadainsuranceappraiser.com (SSL active; `www.` and http redirect to it) |
| Preview domain | https://mintcream-cat-710250.hostingersite.com (sends `X-Robots-Tag: noindex`; the original temporary URL was aqua-alligator-772171.hostingersite.com) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@nevadainsuranceappraiser.com (form delivers over SMTP, verified) |
| Google Tag Manager | `GTM-PDTLXWJ8`: the owner's head snippet verbatim (`GTM_SNIPPET` in `build.py`) + `<noscript>` iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD graph, sitemap, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages (county, neighborhoods, housing mix, storm history, FAQs) |
| `src/tools.py` | 7 tools (markup + copy); the logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Appraisal roadmap (7 steps), FAQ (22 Qs in 5 groups), claim dictionary (43 terms), 6 field notes |
| `src/photo_sources.json` → `src/photos.json` | Photo sources and processed metadata (size, license, creator, landing page) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This folder is what gets deployed (it is committed) |
| `tools/make_icons.py` | Favicon + logo pipeline (SVG, ICO 16/32/48 from a bolder variant, 96px, 180px full-bleed touch icon, maskable 192/512) |
| `tools/photos.py` | Photo pipeline: download → ≤1200px and 640px WebP + `photos.json` |
| `tools/make_og.js` | Renders the 1200×630 `og-image.jpg` with Playwright, using a site photo and the site fonts |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
```

```sh
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid pUs9TSRI1); they expire after a few hours
export NVIA_FB_URL='…' NVIA_FB_AUTH='…' NVIA_FB_REST='…'
./deploy.sh
```

Then clear the cache with `agency-hosting_cache_clear-website` (website_uid `pUs9TSRI1`).
When CSS or JS changes, bump `VER` in `build.py`. When icons change, bump `FAV` and the `?v=` in
`static/site.webmanifest`. Rebuild icons with `python3 tools/make_icons.py` and the OG image with
`node tools/make_og.js`.

Local preview with real routing: `php -S 127.0.0.1:8765 -t public router.php`, where the router returns
`false` for existing files and otherwise requires `public/index.php`. Or run `python3 -m http.server` in
`public/` and open `/home.html`.

## Pages (52 in sitemap + 404)

One main keyword per page. URL scheme:

- `/` home (*Nevada Insurance Appraiser*), `/our-story/`, `/get-in-touch/`
- `/appraisal/` + 12 services: appraisal-clause-help, homeowner-claims, commercial-hoa-claims,
  roof-hail-claims (tile roofs), high-wind-claims (zephyrs, downslope winds, microbursts),
  monsoon-storm-claims (monsoon and tropical remnants, the hurricane slot for this state),
  water-leak-claims (slab leaks), fire-smoke-claims, wildfire-claims and snow-load-freeze-claims
  (the two state-specific perils), estimate-review, umpire-services
- `/cities/` + 12 cities: las-vegas, henderson, north-las-vegas, boulder-city, mesquite, pahrump, reno,
  sparks, carson-city, minden-gardnerville, incline-village, elko
- `/toolkit/` + 7 tools: claim-gap-estimator (net after fees + break-even share of the gap),
  depreciation-recovery-calculator, roof-squares-tile-calculator (tile counts + broken-tile share),
  percentage-deductible-calculator (wind/hail or earthquake), claim-calendar-builder (.ics export),
  appraisal-file-scorecard, smoke-ash-cleaning-estimator (new, wildfire smoke scope)
- `/appraisal-roadmap/` (HowTo), `/questions/` (FAQ by topic), `/claim-dictionary/` (searchable glossary),
  `/field-notes/` + 6 guides
- `/privacy-notice/`, `/website-terms/`, `/disclaimers/`, `/photo-credits/`, `/site-index/` (HTML site map),
  `/404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** desert gold `#c8961f` / bright `#e2b13c` (buttons, counters), deep bronze `#211a0b` (header,
  footer, dark sections), gold tint `#fbf3dc`, complementary dusk indigo `#2f3a8f` / `#1b2159` (loss-history
  section, CTA strips, chart accents) and sand/stone neutrals.
- **Type:** Bricolage Grotesque (display) + Figtree (body). No sister site uses either.
- **Layout:** full-bleed photo hero with a solid lead-form card, a peril ribbon, a split intro with a photo
  pair, a gold counter band, 12 service photo cards, four region tabs with photos ("one state, very
  different losses"), a quick gap check, five process cards, a Nevada loss-history list, tool cards, city
  photo tiles, fits/doesn't cards, FAQ, guides, a parallax CTA and a contact section. Interior pages use
  photo heroes with fact chips and a two-column layout with a sticky sidebar (call box + related links).
- **Effects:** header turns solid on scroll, slow hero zoom, staggered reveal, animated counters, hover zoom on
  cards, region tabs, parallax CTA and a back-to-top button. Left out on purpose (used by sister sites):
  scroll progress bar, marquee, 3D tilt and the scroll-filled timeline. Motion respects
  `prefers-reduced-motion`. Without JS, everything is visible, the header is solid and all region panels show.
- **Mobile nav:** off-canvas `#drawer` rendered outside the fixed header (no `backdrop-filter` anywhere).
  Accordion submenus, scroll lock, closes on ×, scrim tap, link tap or Escape, toggles
  `inert`/`aria-hidden`/`aria-expanded`; shadow and visibility only while open. Fixed call bar below 760px.

## Photos

43 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`): rawpixel (many are
Library of Congress, USFS and other public-domain originals), StockSnap and Wikimedia Commons. Candidates were
reviewed on contact sheets labelled by Openverse ID; photos already used on the Georgia or North Carolina sites
were excluded, as were images with political figures, text overlays, watermarks or artwork. Each is served as
≤1200px and 640px WebP with `srcset`/`sizes` and width/height. All are listed with license and source on
`/photo-credits/`. Rawpixel's free originals top out at 1024px, so heroes sit behind dark overlays.
Re-run `python3 tools/photos.py` after editing `src/photo_sources.json`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150 characters.
  Titles and descriptions are unique.
- Exactly one H1, the first heading is the H1, and no skipped levels (footer, sidebar and tool widgets included).
- Valid JSON-LD. Every `{"@id": …}` reference must resolve. The graph has ProfessionalService (logo,
  contactPoint, address, areaServed, OfferCatalog) + WebSite + exactly one page node with breadcrumb,
  primaryImageOfPage and mainEntity. Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo and
  DefinedTermSet are added where they apply.
- Canonical equals `https://nevadainsuranceappraiser.com/...`. OG (with image size/alt), Twitter and
  `geo.region` tags are present.
- No broken internal links or anchors. Every image has `alt` and width/height.
- The homepage's `<main>` contains "Nevada Insurance Appraiser" at least 14 times (currently 18).
- No sister-state name (Alabama, Florida, Georgia, North Carolina/Carolina, Texas) appears anywhere in the output.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown paths to `index.php`.
  Don't add a root `index.html`: the homepage is `home.html`.
- `index.php` serves `home.html` for `/`, 301-redirects directory URLs to the trailing-slash form, serves
  `404.html` with a real 404 status, sends `X-Robots-Tag: noindex` on any host other than the real domain,
  and 301-redirects `www.` and plain http to `https://nevadainsuranceappraiser.com` (only on the real domain).
- On the temporary `*.hostingersite.com` domain the CDN serves its own `robots.txt` (blocking Googlebot);
  ours is served once the real domain is connected.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.
- The host serves existing files directly, so `index.php` only redirects `/`, unknown paths and
  no-trailing-slash URLs. Plain-http and `www.` requests for interior pages are answered by the host with
  a 200, so every page carries a one-line script in `<head>` that moves those visitors to the https apex.
  Canonical tags already point there.

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation. It sends each
lead through `info@nevadainsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (it starts with a 404-and-exit PHP header, so it can't be read over the web).

The password is **never committed** (`_private/` is in `.gitignore`). Once the mailbox exists, upload this file to
`public_html/api/_private/config.php` with the File Browser API (it can't write outside `public_html`):

```php
<?php
if (!defined('NVIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@nevadainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled TEST, and check
that the log line shows `"via":"smtp"`. Done on 2026-11-10: config and log both return 404 with 0 bytes, and the
TEST lead was logged with `"via":"smtp"`. If the mailbox password changes, re-upload that file.

## Going live checklist

1. ~~Connect the domain and wait for SSL~~ (done 2026-11-10).
2. ~~Check `www.`/http redirects and that the real domain sends no noindex header~~ (done).
3. ~~Wire up SMTP and add GTM~~ (done).
4. ~~Rebuild, validate, redeploy, clear the cache~~ (done).
5. Submit `https://nevadainsuranceappraiser.com/sitemap.xml` in Google Search Console.

## Canonical host guard (added Nov 12, 2026)

The host ignores `.htaccess` and serves real files without running the root `index.php`, so
`http://` and `www.` requests for interior pages used to load with a 200 instead of redirecting.
`deploy.sh` now runs `guardify.py` on a staging copy of `./public` before uploading:

- every page `dir/index.html` goes up as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by the unchanged HTML
- `_guard.php` 301s `www.` and plain http to `https://nevadainsuranceappraiser.com`, 301s `/dir/index.php` to `/dir/`,
  sends `X-Robots-Tag: noindex, nofollow` on any other host (preview domains) and 404s if requested directly
- the root `index.php` front controller requires the guard and looks for `dir/index.php`
- after a clean upload, the stale `dir/index.html` pages are deleted from the server, because the
  host would serve them before `index.php`

`./public` and `validate.py` keep plain `index.html`, so the build and checks are unchanged.
**Always deploy with `deploy.sh`**: uploading `./public` any other way would put `index.html` pages
back on the server and reopen the gap.
