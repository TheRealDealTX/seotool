# rhodeislandinsuranceappraiser.com — static site

Rhode Island Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and it is
served from a Hostinger Agency Growth website through a small PHP guard and front controller.

| | |
| --- | --- |
| Hostinger website UID | `96IM2CwtT` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, created in the Boston datacenter; the API reports server `us-phx-h5g-node3`) |
| Domain | https://rhodeislandinsuranceappraiser.com (live; SSL covers the apex and www, both expire 2027-02-11; www and http 301 to the apex) |
| Preview URL | https://peachpuff-herring-145397.hostingersite.com (every page sends `X-Robots-Tag: noindex`; Hostinger serves its own blocking robots.txt here) |
| Nameservers to set at the registrar | `pixel.dns-parking.com`, `byte.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@rhodeislandinsuranceappraiser.com (form delivers over SMTP; config is on the server only) |
| Google Tag Manager | `GTM-TD55R2LF` (`GTM_ID` in `build.py`; head snippet exactly as supplied + `<noscript>` iframe after `<body>`) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 community pages + the 6 homepage regions |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, grouped FAQ, 40-term glossary, 6 guides |
| `src/photos.json`, `src/photo_alt.json` | Photo metadata (title, creator, license, source, size) and alt text |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`, copied into `public/` as-is |
| `make_assets.py` | Favicon/logo/OG pipeline (Pillow + Playwright Chromium to rasterize the SVG mark) |
| `public/` | **Build output** that gets deployed (committed) |
| `validate.py` | Post-build checks; must report 0 errors |
| `deploy.sh` | Uploads `public/` to `public_html` over the File Browser TUS API |
| `dev-router.php` | Local `php -S` router that mimics the host (not deployed) |

## Build & deploy

```sh
python3 make_assets.py          # only when the mark or OG photo changes
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 96IM2CwtT)
export RIA_FB_URL='https://…/tus' RIA_FB_AUTH='…' RIA_FB_REST='…'
./deploy.sh                     # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the server:
`DELETE {RIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.

Local preview with real routing: `cd public && php -S 127.0.0.1:8099 "$PWD/../dev-router.php"`.

## Pages (50 in the sitemap, plus a 404)

- Home, `/firm-profile/` (about), `/request-a-claim-review/` (contact)
- `/claim-valuation-services/` + 11 services (appraisal clause, homeowner, commercial/condo/HOA, roof & hail,
  wind/microburst/tornado, hurricane, water, **ice dam & frozen pipe** (the state-specific peril), fire & smoke,
  estimate review, umpire)
- `/rhode-island-communities/` + 12 communities: Providence, Warwick, Cranston, Pawtucket, East Providence,
  Woonsocket, Newport, Westerly, Narragansett, Bristol, North Kingstown, Coventry
- `/policyholder-tools/` + 7 tools: settlement gap estimator (flat, percent or hourly fees + umpire share),
  RCV/ACV holdback calculator, roof area & pitch converter, hurricane deductible calculator, claim timeline builder
  (.ics export), appraisal readiness checkup, and the Rhode Island-specific **wind vs. flood damage splitter**
- `/the-appraisal-sequence/` (process guide, HowTo), `/policyholder-questions/` (FAQ by topic),
  `/claim-wordbook/` (searchable glossary, 40 terms), `/claim-notebook/` + 6 guides
- `/data-privacy/`, `/use-terms/`, `/claim-disclaimer/`, `/browse-the-site/` (HTML site map)
- The photo credits page was removed at the owner's request (Nov 13, 2026) and deleted from the server; sources stay in `src/photos.json`
- `404.html`, served with a real 404 status by the front controller

Slugs, copy and design are deliberately different from every sister `*insuranceappraiser*` site.

## Design

- Palette from the main color: sun `#FEC500`, deep shade `#8A6A00` (text accents) and `#3A2C00`, tints `#FFF2BF` /
  `#FFFAE6`, complementary harbor indigo `#23317A` (deep `#141C4A`), charcoal ink `#16171B`, stone `#F5F3EE`.
- Fonts: **Epilogue** (display) + **Instrument Sans** (body), a pairing no sister site uses.
- Logo: a sun-yellow tile with a charcoal roof line over an indigo Ocean State wave (`favicon.svg`, `assets/img/mark.svg`).
  Small favicons use a bolder variant; the apple-touch icon is full bleed and the 192/512 icons are maskable.
- Homepage order: photo hero with a ticket-style lead form → yellow counter band → "Covered isn't the same as paid"
  ledger (illustrative figures, labelled) → horizontal scroll-snap services rail → Ocean State claim calendar (seasons) →
  region tabs with photos → five-step process → quick gap check → storm record timeline → tools → community photo grid →
  three-question test → FAQ → guides → contact.
- Effects: scroll progress bar, header that turns solid on scroll, slow hero zoom, staggered reveal, animated counters,
  hover zoom on photo cards, region tabs, scroll rails, back-to-top. All motion is off under `prefers-reduced-motion`,
  and pages render fully without JavaScript (reveal styles apply only once JS sets `html.js`; without JS the menu link
  goes to the site map and dropdowns open on hover/focus).
- Mobile nav is an off-canvas drawer **outside** the header (the header has no `backdrop-filter`), with accordion
  submenus, scroll lock, close on ×, overlay tap, link tap or Escape, `inert`/`aria-hidden` handling, and its shadow
  and visibility applied only while open. A fixed call bar sits at the bottom on phones.
- The brand link keeps its color and has no underline on hover in the header, drawer and footer.

## Photos

About 30 real photos, all **CC0 or public domain**, found through the Openverse API (`license=cc0,pdm`) and
Wikimedia/Flickr/StockSnap/US-government sources, downloaded one at a time with backoff and Wikimedia's standard thumbnail
widths. None reuse a photo from a sister site. Each one is served as 1200px and 640px WebP with `srcset`, `sizes`, width
and height. Decorative backgrounds use `alt=""`. Each photo's license, creator and source URL are recorded in `src/photos.json` (no public credits page, at the owner's request).

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" switch, and **serves real files directly without running
  the root `index.php`**. A `dir/index.html` page would skip any redirect, so `http://www.…/any-page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP). The homepage is
  `home.html`, served by the front controller for `/`. There is no root `index.html`, and there must never be a
  `dir/index.html` on the server. `validate.py` enforces this.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://rhodeislandinsuranceappraiser.com` on the real domain only, 301s `/dir/index.php` and `/index.php` to the
  directory URL, sends `X-Robots-Tag: noindex, nofollow` on every other host (such as the preview URL), and returns 404 if
  requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs that lack a trailing
  slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a 404 status.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; all unique
- Exactly one H1, the first heading is the H1, and no skipped heading levels anywhere (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/CollectionPage) with
  breadcrumb, `primaryImageOfPage` and `mainEntity`; a ProfessionalService node with logo, contact point, `addressRegion` RI,
  areaServed (state + cities) and an OfferCatalog; a WebSite node. Service, FAQPage, ItemList, WebApplication, BlogPosting,
  HowTo and DefinedTermSet are added where they apply
- Canonical `https://rhodeislandinsuranceappraiser.com/...`, Open Graph (with image size and alt), Twitter card and `geo.region`
- No broken internal links or anchors; every image has `alt`; every sitemap URL maps to a page
- The homepage's main content (header and footer excluded) mentions "Rhode Island Insurance Appraiser" at least 14 times
- No sister-state name (Alabama, Alaska, Arizona, Arkansas, Delaware, Florida, Georgia, Kentucky, Maine, Maryland,
  Massachusetts, Missouri, Montana, Nevada, New Jersey, New York, North Carolina, Ohio, South Carolina, West Virginia,
  Wyoming) anywhere in the build
- Every page file starts with the guard line and contains no other PHP; no `index.html` pages

## Contact form

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and server-side validation (name, a valid
email or a phone number, and consent). It sends through `info@rhodeislandinsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a
JSON-lines record (with `"via"`) to `api/_private/leads.log.php`.

Both private files sit inside `public_html` (the file API can't write outside it) and return an empty 404 if requested
directly. `_private/` is git-ignored. **Never commit the config.** Keep any local copy outside the repo and delete it after
upload. Format:

```php
<?php
if (!defined('RIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@rhodeislandinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Done Nov 13, 2026: config uploaded, `/api/_private/config.php` and the log both return 404 with 0 bytes, and a submission labelled
as a test was logged with `"via":"smtp"` and no error.

## Google Tag Manager

`GTM_ID = "GTM-TD55R2LF"` in `build.py`. `gtm_head()` outputs the owner's snippet verbatim (async `gtm.js` + `dataLayer`/`gtag('js')`),
and the `<noscript>` iframe follows `<body>`. Clear `GTM_ID` to remove both. The privacy policy mentions GTM.

## Go-live checklist

1. ~~Nameservers, SSL for apex + www~~: done. http, www and `/dir/index.php` URLs 301 to the https apex on the homepage and
   interior pages, all 50 sitemap URLs return 200, and the real domain sends no `X-Robots-Tag` and serves our robots.txt.
2. ~~Mailbox + SMTP~~: done. ~~GTM~~: done.
3. Submit `https://rhodeislandinsuranceappraiser.com/sitemap.xml` to Google Search Console.
