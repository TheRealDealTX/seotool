# tennesseeinsuranceappraiser.com — static site

Tennessee Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and a small PHP guard + front controller serve it on a Hostinger Agency Growth website.
Engineering is adapted from `georgiainsuranceappraiser/`; content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `y1mAg5X8i` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter selected) |
| Domain | https://tennesseeinsuranceappraiser.com (attached at creation; SSL issues once DNS points here) |
| Preview URL | https://open-azure-meerkat-95.hostingersite.com |
| Nameservers to set at the registrar | `hermes.dns-parking.com`, `artemis.dns-parking.com` |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@tennesseeinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, templates, JSON-LD, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Tennessee location pages |
| `src/tools.py` | 7 interactive tools (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide, grouped FAQ, 43-term glossary, 6 guides |
| `src/photo_sources.json` | Photo picks: source URL, landing page, license, creator, alt text |
| `src/photos.json` | Photo manifest written by `photos.py` (adds final width/height) |
| `photos.py` | Photo pipeline: downloads picks one at a time with backoff, writes 1200px + 640px WebP |
| `assets.py` | Favicon/logo/OG pipeline (svg, ico 16/32/48 bold, 96 png, 180 apple-touch, maskable 192/512, og-image.jpg) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`; copied into `public/` |
| `public/` | **Build output**, deployed as-is (committed) |
| `validate.py` | Post-build checks (must report 0 errors) |
| `deploy.sh` | Uploads `public/` to `public_html` over the TUS file API |

## Build & deploy

```sh
python3 photos.py      # only when photo picks change
python3 assets.py      # only when the mark or OG image changes
python3 build.py && python3 validate.py
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid y1mAg5X8i)
export TIA_FB_URL='…/api/tus' TIA_FB_AUTH='…' TIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid y1mAg5X8i)
```

`deploy.sh` only adds and overwrites. When a page is removed or renamed, delete the old file on the
server: `DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` / `X-Auth-Rest`
headers. Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.
There is no `/photo-credits/` page and none was ever uploaded (it returns 404).

Local preview with host-like routing: run `cd public && php -S 127.0.0.1:8099 ../router.php`, where
`router.php` (in this folder) serves real files directly, executes a directory's `index.php`, and sends everything else
to the root `index.php`.

## Pages (50 in sitemap + 404)

| Section | URL |
| --- | --- |
| Home | `/` |
| About / Contact | `/who-we-are/`, `/get-a-claim-review/` |
| Services (index + 11) | `/tn-claim-appraisals/…` |
| Service areas (index + 12) | `/tennessee-service-areas/<city>/` — Nashville, Memphis, Knoxville, Chattanooga, Clarksville, Murfreesboro, Franklin, Jackson, Johnson City, Kingsport, Cookeville, Sevierville & Gatlinburg |
| Tools (index + 7) | `/tennessee-claim-tools/…` — claim gap & fee estimator, RCV/ACV holdback, roof area & pitch, percentage deductible (wind/hail + earthquake), claim deadline calendar (.ics), appraisal readiness check, **tree & debris allowance calculator** (new) |
| Resources | `/appraisal-process-tennessee/`, `/tennessee-appraisal-questions/`, `/claim-terms-glossary/`, `/claim-dispute-guides/` + 6 guides |
| Legal | `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/all-pages/` (HTML site map) |
| 404 | `404.html`, served with a real 404 status by `index.php` |

All slug bases were checked against the sister sites and are unused elsewhere.
The homepage's main content mentions "Tennessee Insurance Appraiser" 19 times (minimum 14, enforced).

## Design

- Palette: red `#CC0000` and navy `#002D65` (brief), deep navy `#001A3D`/`#00112A`, mist tint `#F1F4F9`,
  sky accent `#8FC1F0` (links/eyebrows on dark), warm paper `#FBFAF8` and slate neutrals.
- Fonts: **Arvo** (display slab) + **Cabin** (body). Neither is used by any sister site.
- Mark: navy tile, red roofline, three white stars (the flag's three Grand Divisions). Same mark in header,
  drawer and footer; brand links don't change color or underline on hover.
- Layout: full-bleed photo hero with a lead form, stats band overlapping the hero, numbered service photo
  cards, Grand Division tabs with photos, gap mini-calculator, sticky-column process timeline that fills on
  scroll, horizontal Tennessee storm timeline, tool/city/guide photo cards, “who to call” comparison,
  FAQ, parallax CTA, contact form. Interior pages: photo hero + two-column layout with a sticky sidebar.
- Effects: scroll progress bar, header that compacts on scroll, hero Ken Burns zoom, staggered reveals,
  animated counters, hover zoom, process fill, region tabs, parallax CTA, back-to-top. No marquee or tilt.
  `prefers-reduced-motion` respected; everything renders without JavaScript (reveals only hide under `.js`,
  region panels stack without JS).
- Mobile: off-canvas drawer outside the sticky header with accordions, scroll lock, close on ×/overlay/
  link/Escape, `inert` + `aria` state, shadow/visibility only while open; fixed bottom call bar.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan “force HTTPS” setting, and **serves real files directly
  without running the root `index.php`**. A `dir/index.html` page would therefore skip any redirect, and
  `http://www.…/any-page/` would load with a 200.
- So every page except the homepage is written as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP.
  The homepage is `home.html`, served for `/` by the front controller. Never add a root `index.html` or
  leave any `dir/index.html` on the server.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://tennesseeinsuranceappraiser.com` on the real domain only, 301s `/dir/index.php` and `/index.php`
  to the directory, sends `X-Robots-Tag: noindex, nofollow` on any other host (e.g. the preview URL),
  and returns 404 when requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, adds the trailing slash on directories,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a 404 status.
- Preview URLs get Hostinger's own Googlebot-blocking `robots.txt`; our `robots.txt` applies on the domain.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents (single line, no trailing newline, no wrapper):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it from the `GSC_FILE` / `GSC_CONTENT` constants on every build, so a rebuild can't
  drop it. `validate.py` checks it byte-for-byte and excludes it from page checks, `sitemap.xml`, the HTML
  site map and internal links; `robots.txt` doesn't block it.
- It must stay at the root permanently: Google rechecks it, and removing it unverifies the property.
  It's a real file, so the host serves it directly (no guard) — expected.
- HTML-file verification works only for the **URL-prefix** property `https://tennesseeinsuranceappraiser.com/`.

## Photos (CC0 / public domain only — no public credits page)

All 38 photos were found through the Openverse API with `license=cc0,pdm` (Flickr CC0/PD — much of it
U.S. government work such as USDA and Forest Service — and StockSnap CC0). None requires attribution,
so the site has no credits page. Wikimedia downloads were rate-limited (429), so no Wikimedia files are used.
Picks exclude identifiable political figures, text overlays and artwork. Each photo is served as 1200px
(or the source's max, ≥683px) and 640px WebP with `srcset`/`sizes` and width/height. Decorative
backgrounds use `alt=""`. Where no CC0/PD city photo existed, a city card uses a representative housing or
weather photo whose alt text describes the photo, not the city. This list is for our records only:

| Key | Source | License | Creator | Source page |
| --- | --- | --- | --- | --- |
| `hero-home` | flickr | Public domain mark | Dingus Nugget | https://www.flickr.com/photos/185078984@N02/51438616285 |
| `house-porch` | flickr | CC0 1.0 | w_lemay | https://www.flickr.com/photos/59081381@N03/28060404887 |
| `house-siding` | flickr | Public domain mark | YellowstoneNPS | https://www.flickr.com/photos/80223459@N05/50014554012 |
| `roof-shingles` | flickr | CC0 1.0 | booledozer | https://www.flickr.com/photos/55289779@N00/8451194514 |
| `roof-closeup` | flickr | Public domain mark | USDAgov | https://www.flickr.com/photos/41284017@N08/51867761912 |
| `tornado-damage` | flickr | Public domain mark | USDAgov | https://www.flickr.com/photos/41284017@N08/7008296545 |
| `tornado-debris` | flickr | Public domain mark | USDAgov | https://www.flickr.com/photos/41284017@N08/7008294773 |
| `water-ceiling` | flickr | Public domain mark | USDAgov | https://www.flickr.com/photos/41284017@N08/51869042369 |
| `house-fire` | flickr | Public domain mark | USDAgov | https://www.flickr.com/photos/41284017@N08/9629106733 |
| `ice-branches` | flickr | CC0 1.0 | David Kitto | https://www.flickr.com/photos/43371449@N00/52663504054 |
| `fallen-tree` | flickr | Public domain mark | Santa Monica Mountains National Recreation Area | https://www.flickr.com/photos/38729417@N06/8722153110 |
| `tree-on-house` | flickr | CC0 1.0 | David Kitto | https://www.flickr.com/photos/43371449@N00/52665605113 |
| `icicles` | flickr | CC0 1.0 | dankeck | https://www.flickr.com/photos/140641142@N05/39521724941 |
| `apartments` | flickr | CC0 1.0 | Gary Lee Todd, Ph.D. | https://www.flickr.com/photos/101561334@N08/25816147120 |
| `office` | flickr | CC0 1.0 | Amsterdam free photos & pictures of the Dutch city | https://www.flickr.com/photos/104736837@N03/11496236035 |
| `meeting` | stocksnap | CC0 1.0 | Direct Media | https://stocksnap.io/photo/business-meeting-Z1ZIMB54UM |
| `consult` | stocksnap | CC0 1.0 | Christina Morillo | https://stocksnap.io/photo/business-meeting-SKBXLJOILI |
| `laptop-calc` | stocksnap | CC0 1.0 | Matt Moloney | https://stocksnap.io/photo/laptop-work-BQLCXMHSHP |
| `calculator` | flickr | Public domain mark | motazabdelazeem صور من الوطن | https://www.flickr.com/photos/91352576@N06/24217746621 |
| `paperwork` | stocksnap | CC0 1.0 | Martin Vorel | https://stocksnap.io/photo/calculator-numbers-JY874BSKKC |
| `clipboard` | flickr | Public domain mark | U.S. Fish and Wildlife Service - Midwest Region | https://www.flickr.com/photos/49208525@N08/6343722631 |
| `inspection` | flickr | CC0 1.0 | Dennis S. Hurd | https://www.flickr.com/photos/43296902@N00/4363286049 |
| `roofer` | flickr | CC0 1.0 | Simon_Cotterill | https://www.flickr.com/photos/137828720@N06/51711148603 |
| `storm-sky` | flickr | Public domain mark | Bonnie Moreland (free images) | https://www.flickr.com/photos/66741228@N05/50298057333 |
| `kitchen` | stocksnap | CC0 1.0 | Matt Bango | https://stocksnap.io/photo/kitchen-interior-3ZX53UFU8B |
| `nashville` | flickr | CC0 1.0 | blcope | https://www.flickr.com/photos/26190392@N02/53038526864 |
| `memphis` | flickr | Public domain mark | Ben 'B' Evans | http://www.flickr.com/photos/153542224@N04/48110511598 |
| `chattanooga` | flickr | CC0 1.0 | Gary Lee Todd, Ph.D. | https://www.flickr.com/photos/101561334@N08/10483463625 |
| `smokies` | flickr | Public domain mark | mrksteele04 | https://www.flickr.com/photos/158934835@N04/48932847298 |
| `hillside-house` | flickr | CC0 1.0 | w_lemay | https://www.flickr.com/photos/59081381@N03/27227394257 |
| `suburb-house` | flickr | CC0 1.0 | w_lemay | https://www.flickr.com/photos/59081381@N03/28060401287 |
| `two-story-house` | flickr | CC0 1.0 | w_lemay | https://www.flickr.com/photos/59081381@N03/28224686298 |
| `colonial-house` | flickr | Public domain mark | GlacierNPS | https://www.flickr.com/photos/43288043@N04/9241094605 |
| `lightning` | flickr | Public domain mark | pingnews.com | https://www.flickr.com/photos/39735679@N00/426174574 |
| `ridge-sunset` | flickr | Public domain mark | jody.claborn | https://www.flickr.com/photos/130478877@N02/19848727336 |
| `snowy-ridge` | flickr | Public domain mark | Great Smoky Mountains National Park | https://www.flickr.com/photos/53081745@N05/49070151563 |
| `storm-tree` | flickr | Public domain mark | Bonnie Moreland (free images) | https://www.flickr.com/photos/66741228@N05/49394921528 |
| `log-cabin` | flickr | Public domain mark | LandBetweentheLakesKYTN | https://www.flickr.com/photos/82242140@N05/7537845912 |

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique titles.
- Meta description **110–143 characters** on every page (including 404), unique, ending in a full sentence,
  and identical to `og:description` and `twitter:description`.
- Exactly one H1, which is the first heading; no skipped heading levels anywhere (footer, sidebar, tools).
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/
  CollectionPage) with `breadcrumb`, `primaryImageOfPage` and `mainEntity`; ProfessionalService with logo,
  contactPoint, address, areaServed and OfferCatalog; WebSite; BreadcrumbList. Service (services and
  locations), FAQPage, ItemList (indexes), WebApplication (tools), BlogPosting (guides), HowTo (process),
  DefinedTermSet (glossary).
- Canonical `https://tennesseeinsuranceappraiser.com/…` on every page; OG image size/alt; Twitter card; `geo.region`.
- No broken internal links or anchors; `alt` on every image; homepage keyword count ≥ 14.
- No other state's name anywhere in the build (allowed: “Mississippi River”, “Washington County”).
- Every `dir/index.php` starts with the guard line (correct depth) and contains no other PHP;
  no `dir/index.html`, no root `index.html`.

## Contact form

`/api/contact.php`: honeypot (`website`), per-IP rate limit (5 per 10 minutes), validation (name +
valid email or phone + consent). Sends through `info@tennesseeinsuranceappraiser.com` over authenticated
SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to `mail()`, and always
appends a JSON line to `api/_private/leads.log.php` (whose `<?php http_response_code(404); exit; ?>`
header makes it 404 if requested). Hostinger's file API can't write outside `public_html`, so both
private files live there. **Never commit credentials** — `_private/` is in `.gitignore`.

Config file to upload once the mailbox exists (keep any local copy outside the repo and delete it after upload):

```php
<?php
if (!defined('TIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@tennesseeinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After upload: confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled
as a test, and confirm the log line shows `"via":"smtp"`.

## Google Tag Manager

`GTM_ID` in `build.py` is empty. Set it (e.g. `GTM-XXXXXXX`) to output the head snippet and the
`<noscript>` iframe right after `<body>` on every page, then rebuild and redeploy.

## Going live checklist

1. Point the domain's nameservers to `hermes.dns-parking.com` and `artemis.dns-parking.com`.
2. Confirm SSL covers both `tennesseeinsuranceappraiser.com` and `www.` (`agency-hosting_websites_get` →
   `ssl_cert.names`); reissue with `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check `http://`, `http://www.` and `https://www.` on home + interior pages all 301 to `https://…/page/`,
   `/page/index.php` 301s, sitemap URLs return 200, no `X-Robots-Tag` on the real domain, our `robots.txt`
   is served, and the GSC file returns 200 with exact bytes. If a www URL returns 200 with
   `x-hcdn-cache-status: HIT`, clear the cache again and recheck.
4. Click **Verify** in Search Console (URL-prefix property), then submit `/sitemap.xml`.
5. Create the mailbox and upload the SMTP config (above); add GTM when available.
