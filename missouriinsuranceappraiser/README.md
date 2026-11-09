# missouriinsuranceappraiser.com — static site

Missouri Insurance Appraiser is a static site with no database and no plugins. A Python generator
builds it, and a small PHP front controller serves it on a Hostinger Agency Growth website.
The engineering comes from `georgiainsuranceappraiser/` (generator pattern, `validate.py`, `deploy.sh`,
`api/contact.php`, tool logic, favicon and photo pipelines). The copy, URL slugs, palette, fonts and
layout are new and differ from every sister site on the account (Alabama, Florida, Georgia, North Carolina).

| | |
| --- | --- |
| Hostinger website UID | `GIDhww0uy` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter) |
| Temporary URL | https://forestgreen-raven-354869.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Final domain | https://missouriinsuranceappraiser.com (not connected yet) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@missouriinsuranceappraiser.com (mailbox still to be created) |
| Google Tag Manager | Off. Set `GTM_ID` in `build.py` to turn it on |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD graph, sitemap, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 community pages (county, neighborhoods, housing, storm history, FAQs) |
| `src/tools.py` | 7 tools (markup + copy); the logic lives in `static/assets/js/app.js` |
| `src/learn.py` | Appraisal roadmap (8 stages), FAQ (26 Qs in 5 groups), glossary (47 terms), 6 field notes |
| `src/photo_sources.json` → `src/photos.json` | Photo sources and processed metadata (size, license, creator, landing page) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This folder is what gets deployed (it is committed) |
| `tools/make_icons.py` | Favicon + logo pipeline (SVG, ICO 16/32/48 with bolder strokes, 96px, 180px touch icon, maskable 192/512) |
| `tools/photos.py` | Photo pipeline: download → ≤1200px and 640px WebP + `photos.json` |
| `tools/make_og.js` | Renders the 1200×630 `og-image.jpg` with Playwright, using the site fonts |
| `tools/checkcopy.py` | Pre-build check of the content modules (title/description limits, headings, banned words) |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
```

```sh
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid GIDhww0uy); they expire after a few hours
export MOIA_FB_URL='…' MOIA_FB_AUTH='…' MOIA_FB_REST='…'
./deploy.sh
```

Then clear the cache with `agency-hosting_cache_clear-website` (website_uid `GIDhww0uy`).
When CSS or JS changes, bump `VER` in `build.py`. When icons change, bump `FAV`
(the manifest has its own `?v=`).

Local preview with real routing: `php -S 127.0.0.1:8765 -t public router.php`, where the router
returns `false` for existing files and otherwise requires `public/index.php`. Or run
`python3 -m http.server` in `public/` and open `/home.html`.

## Pages (51 in sitemap + 404)

URL scheme, with one main keyword per page:

- `/` home (*Missouri Insurance Appraiser*), `/our-firm/`, `/get-in-touch/`
- `/appraisal-help/` + 11 services: appraisal-demand-representation, homeowner-claim-appraisal,
  commercial-hoa-appraisal, hail-roof-damage-appraisal, tornado-straight-line-wind-appraisal,
  burst-pipe-water-damage-appraisal, fire-smoke-damage-appraisal, sinkhole-ground-collapse-appraisal
  (the state-specific peril: karst terrain), winter-storm-ice-damage-appraisal, insurer-estimate-review,
  appraisal-umpire-services. No hurricane page: it isn't a Missouri peril.
- `/communities/` + 12: kansas-city, st-louis, springfield, columbia, independence, lees-summit,
  st-charles, st-joseph, joplin, jefferson-city, cape-girardeau, chesterfield
- `/toolkit/` + 7 tools: award-net-payout-estimator (deductible, prior checks, fees, 3 outcomes),
  depreciation-recovery-calculator, roof-measurement-calculator (pitch, waste, tear-off layers),
  hail-deductible-calculator (percentage vs. flat, comparison table), claim-calendar-builder (.ics export),
  appraisal-readiness-score, roof-repair-or-replace-splitter (new: slope-by-slope repair vs. full roof)
- `/appraisal-roadmap/` (HowTo), `/questions-answered/` (FAQ grouped by topic), `/appraisal-dictionary/`
  (searchable glossary), `/field-notes/` + 6 articles
- `/privacy-notice/`, `/terms-of-service/`, `/site-disclaimer/`, `/photo-credits/`, `/site-index/` (HTML site map),
  `/404.html` (real 404 status), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** espresso `#2A1A0E` (main), deep `#170D06`, bark `#5A3A22`, parchment tint `#F6EFE5`,
  sand `#E6D9C6`, one complementary river-teal accent (`#1F7A80`, light `#8FD3D5` for links on dark),
  and cream/stone neutrals. Gradients only in the logo and hero/banner overlays.
- **Type:** Bricolage Grotesque (display) + Figtree (body). No sister site uses either.
- **Logo:** a cream catenary arch over a teal roof line and ground line on an espresso tile.
- **Layout:** full-bleed photo hero with a “ticket” lead form, counters on a card that overlaps the hero,
  a sticky-heading intro with fit/not-fit boxes, numbered service photo cards, a month-by-month
  Missouri claim calendar (perils × months), sticky stacking process cards, a six-region photo mosaic,
  a storm ledger, a gap check, tool cards, community tiles, FAQ and field-note cards.
  Interior pages use photo banners and a two-column layout with a sticky sidebar (call box + related links).
- **Effects:** masthead turns solid on scroll, hero zoom-out on load, staggered reveal, animated counters,
  season-bar fill, sticky stacking process cards, hover zoom on cards, parallax CTA and a back-to-top button.
  Left out on purpose because sister sites use them: progress bar, marquee, 3D tilt, region tabs, filling
  timeline, progress ring. All motion respects `prefers-reduced-motion`; without JS the content shows and
  the header is solid.
- **Mobile nav:** an off-canvas `#drawer` (slides from the left) rendered outside the fixed header, with no
  `backdrop-filter` anywhere. Accordion submenus, scroll lock, and close on ×, overlay tap, link tap or
  Escape. It toggles `inert`/`aria-hidden`/`aria-expanded`; shadow and visibility apply only while open.
  A fixed call bar sits at the bottom below 760px.

## Photos

57 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`): Flickr CC0/PDM
(including U.S. government uploads), StockSnap, rawpixel and WordPress Photo Directory. Each was reviewed
on contact sheets labelled by file ID; photos with political figures, text overlays or artwork were skipped,
and so were any already used on the Georgia or North Carolina sites. Each is served as ≤1200px and 640px
WebP with `srcset`/`sizes` and width/height, and listed with license and source on `/photo-credits/`.
Re-run `python3 tools/photos.py` after editing `src/photo_sources.json`. Some Flickr and StockSnap originals
are only available at 960–1024px, so they sit behind overlays in heroes.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150
  characters. Titles and descriptions are unique.
- Exactly one H1, the first heading is the H1, and no skipped levels (footer, sidebar and tool
  widgets included).
- Valid JSON-LD. Every `{"@id": …}` reference must resolve within the page graph. The graph has
  ProfessionalService (logo, contactPoint, address, areaServed, OfferCatalog) + WebSite + exactly
  one page node with breadcrumb, primaryImageOfPage and mainEntity. Service, FAQPage, ItemList,
  WebApplication, BlogPosting, HowTo and DefinedTermSet are added where they apply.
- Canonical equals `https://missouriinsuranceappraiser.com/...`. OG (with image size/alt), Twitter and
  `geo.region` tags are present.
- No broken internal links or anchors. Every image has `alt` and width/height.
- The homepage's `<main>` contains "Missouri Insurance Appraiser" at least 14 times (currently 18).
- No sister-state name (Alabama, Florida, Georgia, North Carolina, Texas) appears anywhere in the output.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown paths to
  `index.php`. Don't add a root `index.html`: the homepage is `home.html`.
- `index.php` serves `home.html` for `/`, 301-redirects directory URLs to the trailing-slash
  form, serves `404.html` with a real 404 status, sends `X-Robots-Tag: noindex` on any host other
  than the real domain, and 301-redirects `www.` and plain http to `https://missouriinsuranceappraiser.com`
  (only on the real domain).
- On the temporary `*.hostingersite.com` host the platform serves its own `robots.txt`; ours applies on the
  real domain.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation. It sends each
lead through `info@missouriinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php` (it starts with a 404-and-exit PHP header, so it can't be read over the web).

The password is **never committed** (`_private/` is in `.gitignore`, and `deploy.sh` skips it). Once the mailbox
exists, upload this file to `public_html/api/_private/config.php` with the File Browser API (it can't write outside
`public_html`):

```php
<?php
if (!defined('MOIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@missouriinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled TEST, and
check that the log line shows `"via":"smtp"`.

## Going live checklist

1. Connect the domain to website `GIDhww0uy` and wait for SSL to become active.
2. Check that `www.` and `http://` 301 to `https://missouriinsuranceappraiser.com` and that the real domain
   sends no `X-Robots-Tag: noindex`.
3. Create the mailbox, then wire up SMTP (above). If you have a GTM container, set `GTM_ID`.
4. `python3 build.py && python3 validate.py`, redeploy, then clear the cache.
5. Submit `https://missouriinsuranceappraiser.com/sitemap.xml` in Google Search Console.
