# kentuckyinsuranceappraiser.com — static site

Kentucky Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a small
PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `qzi3K4TYW` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter) |
| Live domain | https://kentuckyinsuranceappraiser.com — live since Nov 12, 2026. Let’s Encrypt SSL covers the apex and `www` (expires Feb 10, 2027); www and http 301 to the apex |
| Preview URL | https://darkslategrey-woodcock-756719.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Nameservers | `lunar.dns-parking.com`, `solar.dns-parking.com` (from `agency-hosting_websites_get`) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@kentuckyinsuranceappraiser.com. The form delivers through it over authenticated SMTP |
| Google Tag Manager | `GTM-WFR968BR`. The owner’s head snippet is output exactly as given (`GTM_SNIPPET` in `build.py`), plus a `<noscript>` iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, templates, JSON-LD, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 city pages (county, neighborhoods, housing mix, storm history, FAQs) |
| `src/tools.py` + `src/tool_copy.py` | 7 calculator widgets (markup) and their page copy; logic is in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (7 steps), FAQ (5 groups), glossary (40 terms), 7 guide articles |
| `src/photos.json` | Photo metadata: alt text, size, title, creator, license, source, landing page |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as is |
| `public/` | **Build output**, the folder that gets deployed (committed) |
| `validate.py` | Post-build SEO and structure checks (must report zero errors) |
| `check_content.py` | Quick pre-build checks of the content modules |
| `photo_pipeline.py` | Source JPGs → 1200px + 640px WebP and `src/photos.json` |
| `make_icons.js` | Renders the mark to favicon.svg/.ico/PNGs and the 1200×630 OG image (Playwright Chromium) |
| `deploy.sh` | Uploads `public/` to `public_html` over the File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # validate must print no ERROR lines
# fresh credentials: agency-hosting_files_generate-upload-url (website_uid qzi3K4TYW); they expire after a few hours
export KIA_FB_URL='https://…/api/tus' KIA_FB_AUTH='…' KIA_FB_REST='…'
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete its old file on the server with
`DELETE {KIA_FB_URL without /tus}/resources/public_html/<path>` and the same two auth headers.

Local preview that behaves like the host (real files served directly, a directory's `index.php` executed, everything
else to the front controller): `cd public && php -S 127.0.0.1:8099 ../dev_router.php`. Requests with
`-H 'Host: www.kentuckyinsuranceappraiser.com'`, or `-H 'Host: kentuckyinsuranceappraiser.com' -H 'X-Forwarded-Proto: http'`,
must 301 to `https://kentuckyinsuranceappraiser.com/<same path>`.

## Pages (52 in sitemap.xml)

- Home, `/about-us/`, `/contact-us/`
- `/insurance-appraisal/` + 11 services: party-appraiser representation, homeowners, commercial & HOA, roof & hail,
  tornado & wind, water, fire & smoke, ice storm & freeze (the Kentucky-specific peril), farm/barn/equine, estimate review, umpire
- `/regions-served/` + 12 cities: Louisville, Lexington, Bowling Green, Owensboro, Covington, Richmond, Elizabethtown,
  Paducah, Frankfort, Hopkinsville, Pikeville, Ashland
- `/appraisal-calculators/` + 7 tools: appraisal payoff estimator (fees + break-even point), RCV & ACV holdback,
  roof measurement (with carrier-squares comparison), percentage deductible (break-even loss), claim timeline builder
  (.ics export, appraisal-demand milestones), appraisal readiness checkup, storm tree removal coverage (Kentucky twist)
- `/kentucky-appraisal-process/`, `/insurance-appraisal-questions/`, `/appraisal-terms/` (searchable), `/appraisal-articles/` + 7 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/photo-credits/`, `/site-index/`, `404.html` (served with a real 404)

URL slugs, section order, copy, palette and fonts were chosen to differ from the sister sites (AL, FL, GA, NC, NV, AZ, MO,
MT, MA, WY, WV, MD). `validate.py` fails the build if any of those state names appears.

## Design

- **Palette:** royal blue `#0033A0` (main), deep navy `#001A57` / `#000E33`, light tint `#E9EFFC` / `#F5F8FE`,
  coral accent `#FF6B4A`, and cool slate neutrals.
- **Fonts:** Sora (display) and Hanken Grotesk (body).
- **Logo:** an estimate's line items under a roofline, with a coral dot.
- **Layout:**
  - full-bleed photo hero with a solid lead-form card
  - triage cards overlapping the hero
  - "at a glance" counter panel
  - photo service rows
  - dark gap-check section
  - horizontal 7-step timeline that fills as you scroll
  - region photo cards
  - storm-history snap rail
  - calculator cards, myth/fact pairs, FAQ, guides
  - parallax CTA and city list
- **Effects:** header turns solid on scroll, hero/CTA parallax, staggered reveal, counters, hover zoom, back-to-top.
  No progress bar, tilt, marquee or tabs, which keeps the mix different from Georgia's. Everything respects
  `prefers-reduced-motion`, and content is fully visible without JavaScript.
- **Interior pages:** photo hero, two-column layout, sticky sidebar with a call box and related links.
- **Mobile:**
  - off-canvas drawer outside the sticky header (no `backdrop-filter` anywhere)
  - accordion submenus, scroll lock, `inert`/`aria-hidden`
  - closes on ×, overlay tap, link tap or Escape
  - shadow and visibility only while open
  - fixed call bar at the bottom
- **Logo hover:** the brand link never changes color or underlines on hover (header, drawer, footer).

## Photos

42 photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`):
- rawpixel (mostly Carol M. Highsmith's Library of Congress Kentucky collection)
- StockSnap
- Wikimedia Commons, including Daderot's capitol photos, the National Weather Service and the U.S. Forest Service
- WordPress Photo Directory

How they were handled:
- Downloaded one at a time with pauses and backoff.
- Wikimedia files fetched as standard-width thumbnails: 330px for contact sheets, 1280px for finals.
- Reviewed on contact sheets by file label. Artwork, engravings, text-heavy signage, tropical scenes and photos that
  don't look like Kentucky were rejected.
- rawpixel's `image_1300` size is watermarked, so the clean `editor_1024` size is used. StockSnap's CDN tops out at 960px.
- Each photo is served as ≤1200px and 640px WebP with `srcset`/`sizes` and width/height. Content images have
  descriptive alt text; decorative backgrounds and card images use `alt=""`.
- Every photo is credited, with its license and a link, on `/photo-credits/`.

## SEO rules (validate.py)

- Title ≤ 60 characters and ≤ ~580px (Arial at 20px); meta description 110–150 characters; titles and descriptions unique
- Exactly one H1, the first heading is the H1, and no skipped heading levels (footer, sidebar boxes and widgets included)
- Valid JSON-LD where every `@id` reference resolves. Each graph has:
  - a ProfessionalService (logo ImageObject, contactPoint, KY/US address, state + 12 cities in areaServed, OfferCatalog)
  - a WebSite
  - exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage) with breadcrumb, primaryImageOfPage and mainEntity
  - plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo and DefinedTermSet where they apply
- Canonical to `https://kentuckyinsuranceappraiser.com/...`, OG tags (with image size and alt), Twitter card and `geo.region` on every page
- No broken internal links or anchors; every `<img>` has `alt`
- Homepage main content uses "Kentucky Insurance Appraiser" at least 14 times (currently 19; 24 counting header/footer)
- No sister-state names; no `index.html` anywhere; every `dir/index.php` starts with the guard line and holds no other PHP

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and serves real files directly (running a
  directory's `index.php`) without running the root `index.php`. `/` and unknown paths go to the root `index.php`.
- That is why every page is `dir/index.php`, whose first line is `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`
  followed by static HTML. A `dir/index.html` would be served without PHP, so `http://www.…/page/` would load with a 200.
  **Never add a root `index.html` or a `dir/index.html`.** The homepage is `home.html`, served by the front controller.
- `_guard.php`:
  - sends one 301 to `https://kentuckyinsuranceappraiser.com` + the same path for `www.` and plain http (from
    `X-Forwarded-Proto`, falling back to `HTTPS`), on the real domain only
  - 301s `/dir/index.php` and `/index.php` to the directory URL
  - sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview domain
  - returns 404 when requested directly
- `index.php` requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash, includes
  `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.
- Hostinger serves its own Googlebot-blocking `robots.txt` on the preview domain. That's expected; the real domain serves ours.

## Contact form

`/api/contact.php`:
- has a honeypot (`website`) and a per-IP rate limit (5 per 10 minutes)
- validates name, a valid email, phone and consent (422 otherwise)
- sends each lead through `info@kentuckyinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
  `api/_private/config.php` exists, and falls back to PHP `mail()`
- always appends a JSON line to `api/_private/leads.log.php`, whose `<?php http_response_code(404); exit; ?>` header
  makes direct requests return an empty 404

The Hostinger file API can't write outside `public_html`, which is why `_private/` sits there. `_private/` is git-ignored.
**Never commit credentials.** Write the config in a scratch location outside the repo, upload it, then delete the local copy:

```php
<?php
if (!defined('KIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@kentuckyinsuranceappraiser.com', 'smtp_pass' => '…'];
```

SMTP has been live since Nov 12, 2026. These checks passed:
- the config URL returns 404 with 0 bytes
- one labelled test submission was sent
- `leads.log.php` (read through the file API) shows `"via":"smtp"` with no error

To change the password, re-upload `public_html/api/_private/config.php` and repeat those checks.

## Go-live (done Nov 12, 2026)

1. The domain resolves to the website. The Let’s Encrypt certificate covers `kentuckyinsuranceappraiser.com` and
   `www.kentuckyinsuranceappraiser.com`, and both hostnames present it.
2. On the homepage and four interior pages:
   - `http://`, `http://www.` and `https://www.` each send one 301 to `https://kentuckyinsuranceappraiser.com/<page>/`
   - `/page/index.php` 301s to `/page/`
   - all 52 sitemap URLs return 200
   - the real domain sends no `X-Robots-Tag` and serves our own `robots.txt`

   If a www URL ever returns 200 with `x-hcdn-cache-status: HIT`, clear the cache and recheck after a few minutes.
3. The GTM tag was added and SMTP wired. `validate.py` reports zero errors, and the site was redeployed and the cache cleared.
4. Still to do: submit `https://kentuckyinsuranceappraiser.com/sitemap.xml` in Google Search Console.
