# connecticutinsuranceappraiser.com — static site

Connecticut Insurance Appraiser: a static site with no database and no plugins. A Python
generator builds it, and a small PHP front controller plus a canonical-host guard serve it on a
Hostinger Agency Growth website. The engineering came from `georgiainsuranceappraiser/`. The copy,
URL scheme and design are new, and they differ from all 36 sister `*insuranceappraiser*` sites.

| | |
| --- | --- |
| Hostinger website UID | `3S90GANgM` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter selected) |
| Domain | https://connecticutinsuranceappraiser.com (attached at creation) |
| Preview URL | https://dodgerblue-crow-274676.hostingersite.com (Hostinger sends its own noindex robots.txt here; our guard adds `X-Robots-Tag: noindex`) |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Server | us-phx-h5g-node3.hstgr.io, IPv4 72.60.128.114 |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@connecticutinsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | `GTM_ID` in `build.py` (empty: no GTM output yet) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 12 services |
| `src/locations.py` | 12 town pages |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide (8 steps), FAQ (5 topics), glossary (41 terms), 6 guides |
| `src/photos.json` | Internal photo manifest: source URL, license, creator, sizes. Not published |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `tools/make_icons.py` | Regenerates favicon.svg/ico, PNG icons, maskable icons, manifest and the OG image |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks, which must report zero errors |
| `deploy.sh` | Uploads `public/` to `public_html` through the TUS file API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# creds: Hostinger API agency-hosting_files_generate-upload-url (website_uid 3S90GANgM); they expire after a few hours
export CIA_FB_URL='…/api/tus' CIA_FB_AUTH='…' CIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid 3S90GANgM)
```

`deploy.sh` only adds and overwrites files. If a page is removed or renamed, delete the old file on
the server with `DELETE {url-without-/tus}/resources/public_html/<path>`, sending the same `X-Auth` and
`X-Auth-Rest` headers. Hostinger's placeholder `default.php` has already been deleted.

To preview locally, run `cd public && php -S localhost:8000 router.php`. The router needs to mimic
the host: serve real files directly, execute a directory's `index.php`, and send everything else to
`/index.php`.

## Pages (51 in sitemap + 404)

- Home, About (`/about-ct-insurance-appraiser/`), Contact (`/contact-ct-appraiser/`)
- `/ct-appraisal-services/` + 12 services: appraisal clause, homeowners, commercial/condo/HOA, roof & hail,
  wind & tornado, hurricane & tropical storm, water & frozen pipe, fire & smoke, **fallen tree** (Connecticut's
  signature peril), ice dam & winter storm, estimate review, umpire
- `/ct-towns/` + 12 towns: Hartford, New Haven, Stamford, Bridgeport, Waterbury, Norwalk, Danbury,
  New London, Greenwich, West Hartford, Milford, Torrington
- `/ct-claim-tools/` + 7 tools: claim gap & fee estimator (flat/percent/hourly fees and a break-even point),
  RCV vs ACV holdback calculator (with a repair-by date), roof square & pitch converter (compares against the
  carrier's squares), hurricane deductible calculator (with a trigger toggle), claim calendar builder
  (.ics export with 14-day reminders), appraisal readiness checkup, **fallen tree claim calculator** (new)
- `/ct-appraisal-process/`, `/ct-appraisal-faq/`, `/ct-claim-glossary/` (searchable), `/ct-claim-insights/` + 6 guides
- `/ct-privacy-policy/`, `/ct-terms-of-use/`, `/ct-disclaimer/`, `/ct-sitemap/`, `404.html` (real 404 status)
- No photo-credits page. Every photo is CC0 or public domain, so none needs attribution.

## Design

- **Palette:** primary `#1F64E5`, charcoal `#333333` (body text) and `#1E1F22` (deep). Supporting shades are a
  deep blue `#0D2C6B`, an ink blue `#08183D` and a light tint `#EAF1FD`. The accent is coral `#FF6B57` (split
  complement), and the neutrals are `#F6F8FB` and `#DEE4EE`.
- **Fonts:** Bitter (slab display) and Golos Text (body). No sister site uses this pairing.
- **Layout:** full-bleed photo hero with a docked horizontal lead form, a counter band, an "illustrative"
  estimate ledger, portrait photo cards for the 12 services, a horizontal storm almanac (1938 to 2021),
  expanding region panels, a sticky-left process timeline that fills on scroll, a gap check on deep blue,
  3D-tilt tool cards, town photo cards, a "who to call" card trio, a parallax CTA and a contact form.
  Interior pages use a photo hero and a two-column layout with a sticky sidebar.
- **Effects:** header turns solid on scroll, hero/CTA parallax (clamped), staggered reveal, counters, hover
  zoom, tilt, expanding panels, almanac scroller, timeline fill, back-to-top. All respect
  `prefers-reduced-motion`, and reveals only hide content after JS has run.
- **Mobile:** the off-canvas `#drawer` sits *outside* the sticky header. The header has no `backdrop-filter`.
  The drawer has accordions, scroll lock and `inert`/`aria-hidden` handling, and closes on ×, a scrim tap, a
  link tap or Escape. Its shadow and visibility apply only while open. A fixed call bar sits at the bottom.
- Brand links in the header, drawer and footer keep their color on hover.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting. It serves real files directly
  (including a directory's `index.php`) and only routes `/` and unknown paths to the root `index.php`. A
  `dir/index.html` would therefore skip any redirect logic.
- Every page is written as `dir/index.php`. Its first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP.
- `_guard.php`:
  - 301s `www.` and plain http (read from `X-Forwarded-Proto`, falling back to `HTTPS`) to
    `https://connecticutinsuranceappraiser.com`, on the real domain only
  - 301s `/dir/index.php` to `/dir/`
  - sends `X-Robots-Tag: noindex, nofollow` on any other host
  - returns 404 if requested directly
- `index.php` serves `home.html` for `/`, 301s to add the trailing slash on directories, and returns
  `404.html` with a real 404 status.
- Never add a root `index.html` or any `dir/index.html`. `validate.py` fails on them.

## Google Search Console verification file

`googlecccfbf2f7e9e5ae4.html` sits at the site root. Its exact contents, with no newline, wrapper or BOM, are:

```
google-site-verification: googlecccfbf2f7e9e5ae4.html
```

- `build.py` writes it on every build from the `GSC_FILE`/`GSC_BODY` constants.
- `validate.py` checks the bytes and keeps the file out of page checks, the sitemap and links.
- It must stay at the root permanently. Google rechecks it, and removing it unverifies the property.
- Verification works for the **URL-prefix** property `https://connecticutinsuranceappraiser.com/`.
- The host serves it directly, so the guard doesn't run for it. That is expected.

## Photos (internal record — not published)

There are 35 photos. All are CC0 1.0 or public domain (U.S. government), and none needs attribution:
- found through the Openverse API with `license=cc0,pdm`
- downloaded one at a time with backoff
- Wikimedia thumbnails at 1280px
- each served as WebP at 1200px (or the source width, if smaller) and 640px, with `srcset`/`sizes` and
  width/height set

Six damage photos reuse sources already vetted for the template. Location pages use a real photo of
the town where one existed (Hartford, New Haven, Stamford, Norwalk/Rowayton, Danbury/Candlewood Lake,
New London, Milford Point). Elsewhere they use generic photos whose alt text does not name a place.

| Key | License | Source | Creator | Landing page |
| --- | --- | --- | --- | --- |
| `hero-saltbox` | CC0 1.0 | wikimedia | CityLimitsJunction | https://commons.wikimedia.org/w/index.php?curid=155330615 |
| `hartford-river` | CC0 1.0 | wikimedia | K1wy K1WY | https://commons.wikimedia.org/w/index.php?curid=7106613 |
| `new-haven-pirelli` | CC0 1.0 | wikimedia | Pat Krupa | https://commons.wikimedia.org/w/index.php?curid=76738197 |
| `stamford-tower` | CC0 1.0 | wikimedia | WikileaksIntern | https://commons.wikimedia.org/w/index.php?curid=150439695 |
| `candlewood-lake` | CC0 1.0 | wikimedia | CityLimitsJunction | https://commons.wikimedia.org/w/index.php?curid=153840683 |
| `new-london-harbor` | CC0 1.0 | wikimedia | Nepoboy22 | https://commons.wikimedia.org/w/index.php?curid=167912622 |
| `rowayton-marina` | CC0 1.0 | wikimedia | Pedro Xing | https://commons.wikimedia.org/w/index.php?curid=19469143 |
| `milford-point` | CC0 1.0 | wikimedia | FrostyLemon | https://commons.wikimedia.org/w/index.php?curid=145398468 |
| `winter-farm` | CC0 1.0 | stocksnap | Olia Gozha | https://stocksnap.io/photo/winter-snow-OT65EM96JH |
| `foursquare-snow` | CC0 1.0 | wikimedia | CityLimitsJunction | https://commons.wikimedia.org/w/index.php?curid=150220973 |
| `victorian-home` | CC0 1.0 | wikimedia | CityLimitsJunction | https://commons.wikimedia.org/w/index.php?curid=155573802 |
| `hartford-office-tower` | CC0 1.0 | wikimedia | Daderot | https://commons.wikimedia.org/w/index.php?curid=54750499 |
| `winter-valley` | CC0 1.0 | wikimedia | Brianegge | https://commons.wikimedia.org/w/index.php?curid=37019972 |
| `snowy-lakehouses` | CC0 1.0 | stocksnap | Bob Richards | https://stocksnap.io/photo/house-snow-0FLURAV6J5 |
| `roof-shingles` | CC0 1.0 | stocksnap | Bernard Spragg | https://stocksnap.io/photo/roof-shingle-RIUJONCXNY |
| `storm-sky` | CC0 1.0 | stocksnap | Free Nature Stock | https://stocksnap.io/photo/storm-clouds-KRZSQKJRCT |
| `stormy-beach` | CC0 1.0 | stocksnap | Jay Mantri | https://stocksnap.io/photo/beach-storm-XKR99VRD9R |
| `lighthouse-coast` | CC0 1.0 | stocksnap | Holly's Coastal View | https://stocksnap.io/photo/lighthouse-ocean-HEWT71JYXM |
| `fallen-tree` | CC0 1.0 | stocksnap | Matt Moloney | https://stocksnap.io/photo/fallen-tree-XJAA6LFZC5 |
| `storm-damaged-house` | Public domain mark | flickr | USDAgov | https://www.flickr.com/photos/41284017@N08/6862190228 |
| `consultation` | CC0 1.0 | stocksnap | Christina Morillo | https://stocksnap.io/photo/business-meeting-SKBXLJOILI |
| `team-laptops` | CC0 1.0 | stocksnap | Burst | https://stocksnap.io/photo/colleagues-meeting-KPVOIKEPSG |
| `calculator-laptop` | CC0 1.0 | stocksnap | Negative Space | https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD |
| `calculator-hands` | CC0 1.0 | stocksnap | Tevarak | https://stocksnap.io/photo/calculator-calendar-RFVHCUGML3 |
| `laptop-calculator` | CC0 1.0 | stocksnap | Wilfred Iven | https://stocksnap.io/photo/accounting-finance-JONMP7TPGK |
| `kitchen` | CC0 1.0 | stocksnap | NeONBRAND | https://stocksnap.io/photo/house-interior-APBDJIC32G |
| `living-room` | CC0 1.0 | stocksnap | Nathan Fertig | https://stocksnap.io/photo/house-interior-WDVIQZEXML |
| `office-lobby` | CC0 1.0 | stocksnap | Verne Ho | https://stocksnap.io/photo/office-building-7HRFNYC7GU |
| `rowayton-boathouse` | CC0 1.0 | wikimedia | Jerry Dougherty | https://commons.wikimedia.org/w/index.php?curid=44059545 |
| `house-fire` | CC0 1.0 | rawpixel | Unknown | https://www.rawpixel.com/image/5918064/burning-house-free-public-domain-cc0-photo |
| `roof-torn-open` | CC0 1.0 | flickr | Daquella manera | https://www.flickr.com/photos/62518311@N00/65665301 |
| `hurricane-trees-down` | Public domain mark | flickr | U. S. Fish and Wildlife Service - Northeast Region | https://www.flickr.com/photos/43322816@N08/8145838525 |
| `tornado-home-damage` | Public domain mark | flickr | MassDOT | https://www.flickr.com/photos/42009447@N05/5793071807 |
| `rain-window` | CC0 1.0 | stocksnap | Pawel Kadysz | https://stocksnap.io/photo/raining-raindrops-3AKFOCTZEQ |
| `storm-debris` | Public domain mark | flickr | USDAgov | https://www.flickr.com/photos/41284017@N08/7008296545 |

## Contact form

`/api/contact.php` has a honeypot, a limit of 5 posts per 10 minutes per IP, and validation (a name, an
email or phone, and consent are required).
- **Delivery:** it sends through `info@connecticutinsuranceappraiser.com` over authenticated SMTP
  (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, and falls back to `mail()` otherwise.
- **Lead log:** it always appends JSON lines to `api/_private/leads.log.php`. That file starts with
  `<?php http_response_code(404); exit; ?>`, so it returns a 404 with an empty body.
- **Secrets:** `_private/` is in `.gitignore`. Never commit credentials. The Hostinger file API can't write
  outside `public_html`, which is why the private files live there.

Config to upload when the mailbox exists. Keep any local copy outside the repo, and delete it after uploading.

```php
<?php
if (!defined('CIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@connecticutinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Once it is uploaded:
1. Confirm `/api/_private/config.php` returns a 404 with 0 bytes.
2. Send one submission labelled TEST.
3. Confirm the log shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title: 60 characters or fewer, and about 580px or less (Arial at 20px)
- Meta description: 110–143 characters, one per page, unique, ending in a full sentence;
  `og:description` and `twitter:description` must match it
- Headings: exactly one H1, the first heading is the H1, and no level is skipped (footer, sidebar and
  tool widgets included)
- JSON-LD: valid, every `@id` reference resolves, every page has a page node, and every page is in sitemap.xml
- Links and images: no broken internal links or anchors, and `alt` on every image
- Homepage: at least 14 mentions of "Connecticut Insurance Appraiser" in `<main>` (currently 20)
- Banned content: no sister-state names anywhere in the published files
- Page files: every page starts with the guard and contains no other PHP; no `index.html` and no
  photo-credits page
- GSC file: byte-exact, not linked, not in the sitemap and not blocked by robots.txt

Each JSON-LD graph contains the ProfessionalService (logo, contact point, CT and city `areaServed`, offer
catalog), the WebSite and one page node linked to its BreadcrumbList, primary image and main entity. Pages
add Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply.

## Going live checklist

1. Point the domain's nameservers to `nova.dns-parking.com` / `cosmos.dns-parking.com`.
2. Confirm SSL covers both the bare and `www` hosts. If `www` is missing, reissue it with `agency-hosting_ssl_reinstall-website`.
3. Recheck the canonical redirects on the live domain, on the homepage and at least three interior pages.
4. Add the GTM container ID (`GTM_ID`) and wire up SMTP once the mailbox exists.
5. Verify the URL-prefix property in Search Console, then submit `https://connecticutinsuranceappraiser.com/sitemap.xml`.
