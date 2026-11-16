# mississippiinsuranceappraiser.com — static site

Mississippi Insurance Appraiser: a static site with no database or plugins. A Python generator builds it, and tiny PHP guards
serve it on a Hostinger Agency Growth website. The engineering (generator layout, validator, deploy script, form handler,
canonical-host guard) follows the Georgia template. The content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `P50Jr3L6H` (Agency Growth, order 1008744732, php-fpm, PHP 8.3; created with the Boston datacenter code, served from `us-phx-h5g-node3.hstgr.io`) |
| Domain | `mississippiinsuranceappraiser.com` (attached at creation) |
| Preview URL | https://darkturquoise-lark-455119.hostingersite.com (Hostinger serves its own noindex `robots.txt` here; our guard also sends `X-Robots-Tag: noindex, nofollow` on any non-canonical host) |
| Nameservers to set at the registrar | `lunar.dns-parking.com`, `solar.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@mississippiinsuranceappraiser.com |
| Google Tag Manager | `GTM_ID` in `build.py`, empty until a container ID is provided |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, every page template, JSON-LD, sitemap, robots, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 service pages (copy, title, description, FAQs) |
| `src/locations.py` | 12 city pages (county, neighborhoods, housing, storm history, FAQs) |
| `src/tools.py` | 7 calculators: markup and explanatory copy (math lives in `static/assets/js/app.js`) |
| `src/learn.py` | Appraisal roadmap, grouped FAQ, 43-term glossary, 6 guides |
| `src/photos.json` | Internal photo manifest: source URL, landing page, creator, license (CC0/PDM only), sizes, alt text |
| `src/BRIEF.md` | Internal content brief and fact sheet (not published; excluded from the build) |
| `make_icons.py` | Draws the logo mark and writes the favicon set and `site.webmanifest` into `static/` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build checks (must pass with zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# Get fresh upload credentials: agency-hosting_files_generate-upload-url (website_uid P50Jr3L6H)
export MIA_FB_URL='…' MIA_FB_AUTH='…' MIA_FB_REST='…'
./deploy.sh
# Then clear the cache: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server with
`DELETE {url-without-/tus}/resources/public_html/<path>` and the same two auth headers (`X-Auth`, `X-Auth-Rest`).
Hostinger's placeholder `public_html/default.php` was deleted the same way.

Local preview that mimics the host (real files direct, a directory's `index.php` executed, everything else to the root `index.php`):
`php -S 127.0.0.1:8000 -t public router.php`. The router lives in the session scratchpad and is reproduced in the hosting notes below.

## Pages (51 in sitemap.xml, plus 404)

- Home, Who we are (`/who-we-are/`), Talk to an appraiser (`/talk-to-an-appraiser/`)
- `/our-appraisal-services/` + 12 services: appraisal demand representation, home, commercial/HOA, roof & hail, tornado & wind,
  hurricane & named storm, water & plumbing, fire & smoke, fallen tree, ice storm & freeze, carrier estimate review, neutral umpire
- `/counties-and-cities/` + 12 cities (`/counties-and-cities/<city>-<county>-county/`): Jackson, Gulfport, Biloxi, Hattiesburg,
  Southaven, Tupelo, Meridian, Oxford, Pascagoula, Vicksburg, Columbus, Greenville
- `/claim-calculator-suite/` + 7 tools: appraisal payoff estimator (fees + break-even), RCV/ACV holdback recovery, roof pitch &
  squares (with eave footage), named-storm deductible (1–10% ladder), claim calendar builder (.ics, appraisal windows),
  appraisal readiness checkup, and the Mississippi-specific **wind vs. water split estimator**
- `/appraisal-roadmap/` (HowTo), `/questions-answered/` (FAQ grouped by topic), `/insurance-claim-terms/` (searchable glossary,
  DefinedTermSet), `/claim-advice/` + 6 guides (BlogPosting)
- `/privacy-notice/`, `/website-terms/`, `/legal-disclaimer/`, `/page-directory/` (HTML site map), `404.html` (real 404 status)
- No photo-credits page. Every photo is CC0 or public domain, so no attribution is needed.

## Design

- **Palette:** crimson `#C21F32` and goldenrod `#EAAB22` (main colors), oxblood `#4A0B14` (deep shade), rose tint `#FBEDEE`,
  gold tint `#FCF1D6`, cream `#FFF9F0`, deep-teal accent `#0F5E5A`, and ink/neutral `#1D1718` / `#6B5F61` / `#EADFDA`.
- **Fonts:** Alegreya (display, 600–800) and Commissioner (body). No sister site uses either.
- **Layout:** full-bleed photo hero with a lead form card, a crimson stat strip with counters, a split intro with a captioned photo,
  service photo cards, six region photo cards on ink, a gap-check mini tool, a horizontal process timeline that fills as you scroll
  (vertical on mobile), tool cards, a parallax CTA, a comparison table, a city grid, an FAQ, guide cards and a contact section.
  Interior pages have photo heroes, breadcrumbs, fact chips and a two-column layout with a sticky sidebar (call box and related links).
- **Effects:** scroll progress bar, a header that goes from transparent to solid on scroll, hero/CTA parallax, staggered reveal,
  animated counters, card hover zoom, the scroll-filled timeline and a back-to-top button. There's no marquee, 3D tilt or region tabs
  (the Georgia mix). Reveal hiding only applies when JS runs and motion is allowed (`.js` class + `prefers-reduced-motion`).
- **Mobile nav:** off-canvas drawer from the left, rendered *outside* the header. The header has no `backdrop-filter`.
  It has accordion submenus, scroll lock, closes on ×, scrim tap, link tap or Escape, and toggles `inert`/`aria-hidden`.
  Its shadow and visibility apply only while it's open. There's a fixed call bar at the bottom on phones.
- **Logo:** a crimson tile with a gold roofline over two white "level" bars (fair value). `make_icons.py` writes `favicon.svg`,
  `favicon.ico` (16/32/48 using a bolder two-stroke variant), the 96px PNG, a full-bleed 180px `apple-touch-icon` and maskable 192/512
  PNGs listed in `site.webmanifest`. Icon links carry `?v=1` (`FAV` in `build.py`). The brand link never changes color on hover.

## Hosting notes (guard, front controller, why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly without running the root
  `index.php`**. A `dir/index.html` would therefore skip any redirect, and `http://www.<domain>/page/` would load with a 200.
- So every page except the homepage is written as `dir/index.php`. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` and the rest is static HTML with no other PHP (`validate.py` enforces both).
  The homepage is `home.html`, served by the front controller. There is **no root `index.html`, and no `dir/index.html` may ever exist**.
  The generator asserts this and the validator fails on it. The only other root `.html` files are `404.html` and the Search Console file.
- `_guard.php`:
  - 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to `https://mississippiinsuranceappraiser.com`, only on the real domain.
  - 301s `/dir/index.php` (and `/index.php`) to `/dir/`.
  - Sends `X-Robots-Tag: noindex, nofollow` on every other host (such as the preview URL).
  - Returns 404 with an empty body when requested directly.
- `index.php` front controller requires the guard. It serves `home.html` for `/`, 301s directory URLs that lack the trailing slash,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.

## Google Search Console verification file

- File: `public/googlecccfbf2f7e9e5ae4.html`, written by `build.py` (`GSC_FILE` / `GSC_BODY` constants) on every build.
- Contents, exactly (no newline, no HTML, no BOM): `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- It must stay at the site root permanently. Google re-checks it, and removing it unverifies the property. It is a real file, so the host
  serves it directly and the guard doesn't run for it (no redirect or `X-Robots-Tag`; that's expected).
- It is excluded from the validator's page checks, `sitemap.xml`, the HTML page directory and internal links. `robots.txt` doesn't block it.
  The validator checks the bytes match.
- This works for the **URL-prefix** property `https://mississippiinsuranceappraiser.com/` only. A Domain property needs a DNS TXT record.

## Contact form

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation (name, valid email or phone, consent).
It sends through `info@mississippiinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line (including `"via"`) to
`api/_private/leads.log.php`. Both private files return 404 when requested directly. The config has a defines guard, and the log starts
with a PHP `exit` header. They live under `public_html` because Hostinger's file API can't write outside it. `_private/` is in
`.gitignore`. **Never commit credentials.** Keep any local copy of the config outside the repo and delete it once uploaded.

```php
<?php
if (!defined('MIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@mississippiinsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives:
1. Upload the config.
2. Confirm `/api/_private/config.php` returns 404 with 0 bytes.
3. Send one form submission labelled TEST.
4. Confirm the log line shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Titles are unique.
- Meta description **110–143 characters** (under 144), unique, ending in a full sentence, and identical to `og:description` and
  `twitter:description`. Applies to every page, including the 404.
- Exactly one H1, which is the first heading, and no skipped heading levels anywhere (footer and sidebar use H2, calculators use no headings).
- Valid JSON-LD. Every page's `@graph` has ProfessionalService (logo ImageObject, contactPoint, MS region, state + 12 cities in
  areaServed, OfferCatalog), WebSite and exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage) with breadcrumb,
  primaryImageOfPage and mainEntity. Plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where
  they apply. Every `@id` reference must resolve.
- No broken internal links or anchors, `alt` on every image, canonical on the domain.
- Homepage main content must contain "Mississippi Insurance Appraiser" at least 14 times.
- No sister-state names anywhere in the build. "Washington County" (Greenville) is allowed. Louisiana and Tennessee are allowed
  because they border Mississippi and aren't sister sites.
- The guard line on every `dir/index.php`, no `dir/index.html`, a sitemap consistent with the pages, and a byte-exact Search Console file.

## Photos (internal record — not published)

All photos are CC0 or public domain (PDM). Most were found through the Openverse API (`license=cc0,pdm`), downloaded one at a time
with backoff, reviewed on labelled contact sheets and saved as 1200px and 640px WebP with `srcset`/`sizes` and width/height.
Decorative backgrounds use `alt=""`. The full record (direct URL, landing page, creator, license) is in `src/photos.json`:

PHOTO_TABLE
