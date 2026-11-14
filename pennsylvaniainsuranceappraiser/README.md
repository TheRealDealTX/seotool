# pennsylvaniainsuranceappraiser.com — static site

**Pennsylvania Insurance Appraiser**: a static site with no database and no plugins. A Python generator builds it,
and each page is served as a tiny PHP file (one guard line + static HTML) on a Hostinger Agency Growth website.
Engineering (generator pattern, `validate.py`, `deploy.sh`, `api/contact.php`, calculator logic, favicon/photo
pipelines, canonical-host guard) comes from the `georgiainsuranceappraiser/` template. The copy, URL slugs, layout,
palette, fonts, photos and homepage structure are new and differ from every sister `*insuranceappraiser*` site.

| | |
| --- | --- |
| Hostinger website UID | `NFEbrRe2M` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter selected) |
| Domain | `pennsylvaniainsuranceappraiser.com` (attached at creation) |
| Preview URL | https://lightgreen-alligator-527245.hostingersite.com |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@pennsylvaniainsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |

Until the nameservers point to Hostinger the real domain won't resolve and SSL can't be issued, so live checks
run on the preview URL. Hostinger serves its own Googlebot-blocking `robots.txt` on preview URLs (expected), and
our guard adds `X-Robots-Tag: noindex, nofollow` on any host other than the real domain.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php`, Search Console file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Pennsylvania city pages |
| `src/tools.py` | 7 calculators (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide steps, grouped FAQ, 42-term glossary, 6 guide articles |
| `src/photos.json` | Photo manifest: alt text, size, source URL, landing page, creator, license (internal record only) |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php` — copied into `public/` as-is |
| `public/` | **Build output** (committed). This folder is what gets deployed |
| `validate.py` | Post-build checks (must report 0 errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS upload API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid NFEbrRe2M)
export PIA_FB_URL='…/tus' PIA_FB_AUTH='…' PIA_FB_REST='…'
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid NFEbrRe2M)
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`DELETE {PIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

Local preview that behaves like the host (real files served directly, a directory's `index.php` executed,
everything else to the root `index.php`): run `php -S 127.0.0.1:8090 router.php` from `public/` with a router like
the one described under *Hosting notes*. `curl -H 'Host: www.pennsylvaniainsuranceappraiser.com' …/where-we-work/erie/`
must 301 to `https://pennsylvaniainsuranceappraiser.com/where-we-work/erie/`.

## URL scheme (51 pages, 50 in sitemap.xml)

- `/` (home), `/about-us/`, `/contact-us/`
- `/property-appraisal-services/` + 11 services
- `/where-we-work/` + 12 cities: philadelphia, pittsburgh, allentown, erie, reading, scranton, lancaster,
  harrisburg, state-college, wilkes-barre, york, johnstown
- `/claim-calculators/` + 7 tools: claim gap & fee projector, RCV vs ACV holdback, roof pitch & squares,
  deductible impact, claim deadline calendar (.ics export), appraisal readiness checkup, roof snow load estimator
- `/appraisal-process-explained/`, `/insurance-appraisal-faq/`, `/claim-terms-glossary/`,
  `/policy-and-claim-guides/` + 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/all-pages/` (HTML site map), `404.html` (real 404 status)
- **No photo-credits page.** All photos are CC0 / public domain; `validate.py` fails if one appears.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting and **serves real files directly without
  running the root `index.php`**. A `dir/index.html` would therefore skip any redirect, and
  `http://www.pennsylvaniainsuranceappraiser.com/any-page/` would load with a 200.
- So every page is `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP).
  The homepage is `home.html`, served by the front controller. There is no root `index.html` and never a
  `dir/index.html`. The only other root `.html` files are `404.html` and the Search Console file.
- `_guard.php`: 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://pennsylvaniainsuranceappraiser.com` — only on the real domain; 301s `/dir/index.php` and `/index.php` to
  the directory; sends `X-Robots-Tag: noindex, nofollow` on any other host; returns 404 if requested directly.
- `index.php` front controller: requires the guard, serves `home.html` for `/`, adds the trailing slash to directory
  URLs (301), includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root. Contents, exactly (one line, no newline, no HTML):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- Written by `build.py` on every build from the `GSC_FILE` / `GSC_BODY` constants, so a rebuild never drops it.
  `validate.py` checks the bytes and makes sure it isn't in `sitemap.xml`, the HTML site map, internal links or
  blocked by `robots.txt`.
- It must stay at the root permanently: Google rechecks it, and removing it unverifies the property. Verify it as a
  **URL-prefix** property `https://pennsylvaniainsuranceappraiser.com/` (a Domain property needs DNS TXT instead).
- It's a real file, so the host serves it directly and the guard doesn't run for it. That's expected.

## Design

- **Palette:** Keystone navy `#002A86` (main), gold `#FFCE00` (main), deep navy `#001A55` / `#000F33`,
  navy tint `#EAF0FC`, gold tint `#FFF7D6`, complementary brick `#C4512A` (accents and warnings), neutrals
  `#F7F6F1` paper, `#E1E3EA` lines, `#182033` text, `#576074` muted.
- **Fonts:** Libre Caslon Text (display — Caslon is the face of colonial Philadelphia printing) + Schibsted
  Grotesk (body/UI). No sister site uses either.
- **Logo:** a keystone with a gold rim and a white house chevron (`static/favicon.svg`, inline in header,
  drawer and footer). Favicons: `favicon.svg`, multi-size `favicon.ico` (16/32/48, bolder art), 96px PNG,
  full-bleed 180px `apple-touch-icon.png`, maskable 192/512 PNGs in `site.webmanifest`; every icon link has `?v=`.
- **Layout & effects:** full-bleed photo hero with a chevron (keystone-point) bottom edge and a lead form; navy
  "ledger" with animated counters overlapping the hero; drop-cap intro with offset photo frame; numbered service photo
  cards (keystone-shaped number badges); a four-season Pennsylvania claim calendar; a horizontal process timeline that
  fills on scroll (vertical on mobile); region photo cards; tool and guide photo cards; three-card "who to call"
  comparison; parallax CTA band; staggered reveal; hover zoom on card photos; header that turns solid on scroll;
  back-to-top button. Interior pages: photo hero with parallax, two-column layout with a sticky sidebar (call box +
  related links). All motion respects `prefers-reduced-motion`, and pages render fully without JavaScript.
- **Mobile nav:** off-canvas drawer `#drawer` rendered *outside* the fixed header (no `backdrop-filter` anywhere),
  accordion submenus, scroll lock, closes on ×, overlay tap, link tap or Escape, `inert`/`aria-hidden` toggled, and
  its shadow/visibility only applied while open. Fixed mobile call bar at the bottom.

## Photos (CC0 / public domain only — internal record, not published)

All photos were found with the Openverse API (`license=cc0,pdm`), reviewed on labelled contact sheets and saved as
1200px and 640px WebP (`static/assets/img/photos/<key>.webp` and `<key>-640.webp`) with `srcset`/`sizes` and
width/height. Decorative backgrounds use `alt=""`. No CC BY or other attribution licenses are used, so the site has no
credits page. The full record (source URL, landing page, creator, license) lives in `src/photos.json`:

| Key | Source | License | Creator | Source file | Landing page |
| --- | --- | --- | --- | --- | --- |
| `apartments` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/2003_3rd_Harrisburg_PA.JPG/1280px-2003_3rd_Harrisburg_PA.JPG | https://commons.wikimedia.org/w/index.php?curid=27605847 |
| `brick-rowhomes` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Gauff_Roth_Allentown_PA.jpg/1280px-Gauff_Roth_Allentown_PA.jpg | https://commons.wikimedia.org/w/index.php?curid=17061235 |
| `brick-rowhomes-2` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/North_York%2C_York_Co_PA.jpg/1280px-North_York%2C_York_Co_PA.jpg | https://commons.wikimedia.org/w/index.php?curid=41464093 |
| `calc-desk` | wikimedia | CC0 1.0 | HP-15C_Calculator-horizontal.jpg: Pittigrilli derivative work: Hic et nunc | https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/HP-15C_Calculator-horizontal-2.jpg/1280px-HP-15C_Calculator-horizontal-2.jpg | https://commons.wikimedia.org/w/index.php?curid=24872899 |
| `calc-papers` | wikimedia | CC0 1.0 | Pittigrilli | https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Financial_Calculator_Hewlett-Packard_HP-12C_built_from_1981%2C_this_item_produced_1988_%28edited_to_remove_background%2C_warmer_colours%29.jpg/1280px-Financial_Calculator_Hewlett-Packard_HP-12C_built_from_1981%2C_this_item_produced_1988_%28edited_to_remove_background%2C_warmer_colours%29.jpg | https://commons.wikimedia.org/w/index.php?curid=146120775 |
| `clipboard` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvaXM3NTk2LWltYWdlLWt3dndyZnA2LmpwZw.jpg | https://www.rawpixel.com/image/5916638/image-public-domain-person-notebook |
| `college-town` | wikimedia | CC0 1.0 | JohnDziak | https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Schlow_Library_In_Downtown_State_College.jpg/1280px-Schlow_Library_In_Downtown_State_College.jpg | https://commons.wikimedia.org/w/index.php?curid=118707263 |
| `consult-table` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvbnMxODI3Ni1pbWFnZS1rd3Z5YzFvei5qcGc.jpg | https://www.rawpixel.com/image/5926299/photo-image-public-domain-hand-person |
| `contractor` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Hibshman_Farm_LanCo_PA.JPG/1280px-Hibshman_Farm_LanCo_PA.JPG | https://commons.wikimedia.org/w/index.php?curid=27188123 |
| `farm-barn` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Farm_Eden_TWP_LanCo_PA.JPG/1280px-Farm_Eden_TWP_LanCo_PA.JPG | https://commons.wikimedia.org/w/index.php?curid=41120667 |
| `flood-street` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTExL2ZsMzY3NjY3NTc1MjItaW1hZ2UuanBn.jpg | https://www.rawpixel.com/image/8723819/photo-image-border-public-domain |
| `harrisburg` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Midtown_Harrisburg_PA_SW_corner_Green_and_Verbeke.JPG/1280px-Midtown_Harrisburg_PA_SW_corner_Green_and_Verbeke.JPG | https://commons.wikimedia.org/w/index.php?curid=27610269 |
| `hero` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/34_Manheim_East_York_YorkCo_PA.JPG/1280px-34_Manheim_East_York_YorkCo_PA.JPG | https://commons.wikimedia.org/w/index.php?curid=29549723 |
| `hill-town` | wikimedia | CC0 1.0 | Bonnachoven | https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Johnstown_PA.jpg/1280px-Johnstown_PA.jpg | https://commons.wikimedia.org/w/index.php?curid=43598110 |
| `house-fire` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA3L2xyL2ZsNDgzNjI3MDI0MzctaW1hZ2UuanBn.jpg | https://www.rawpixel.com/image/7433329/photo-image-public-domain-firefighter |
| `house-porch` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Yorkana%2C_York_County%2C_PA_06.JPG/1280px-Yorkana%2C_York_County%2C_PA_06.JPG | https://commons.wikimedia.org/w/index.php?curid=40445397 |
| `icicles` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL2Zyc25vd19yb29mX3Blb3BsZV9tdXJjaWEtaW1hZ2Uta3liYWxwcDIuanBn.jpg | https://www.rawpixel.com/image/6018207/photo-image-public-domain-nature-ice |
| `inspector` | wikimedia | CC0 1.0 | User:Hassocks5489 | https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Fire-Damaged_House_at_Buxted_%28October_2010%29.jpg/1280px-Fire-Damaged_House_at_Buxted_%28October_2010%29.jpg | https://commons.wikimedia.org/w/index.php?curid=181512006 |
| `interior` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvaXMxNTc5OC1pbWFnZS1rd3Z5Z29ycy5qcGc.jpg | https://www.rawpixel.com/image/5927053/photo-image-frame-light-public-domain |
| `meeting` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL3B4OTA5MDM3LWltYWdlLWt3dnVzd3FqLmpwZw.jpg | https://www.rawpixel.com/image/5904074/photo-image-public-domain-people-office |
| `office` | wikimedia | CC0 1.0 | Thomson200 | https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cumberland%2C_Georgia_office_buildings%2C_2016.jpg/1280px-Cumberland%2C_Georgia_office_buildings%2C_2016.jpg | https://commons.wikimedia.org/w/index.php?curid=51157450 |
| `philadelphia` | wikimedia | CC0 1.0 | Mefman00 | https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Philadelphia_skyline_from_South_Street_Bridge.jpg/1280px-Philadelphia_skyline_from_South_Street_Bridge.jpg | https://commons.wikimedia.org/w/index.php?curid=44062964 |
| `pittsburgh` | wikimedia | CC0 1.0 | Cbaile19 | https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Pittsburgh_Skyline_from_North_Shore%2C_2015-06-17%2C_04.jpg/1280px-Pittsburgh_Skyline_from_North_Shore%2C_2015-06-17%2C_04.jpg | https://commons.wikimedia.org/w/index.php?curid=41066285 |
| `river-town` | wikimedia | CC0 1.0 | Bonnachoven | https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Thomas_J_Hatem_Bridge_Susquehanna_river_from_Amtrak_bridge.jpg/1280px-Thomas_J_Hatem_Bridge_Susquehanna_river_from_Amtrak_bridge.jpg | https://commons.wikimedia.org/w/index.php?curid=114780623 |
| `roof-shingles` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvZmw1MTE1OTM1NzYxMi1pbWFnZS1reWNpbGthbC5qcGc.jpg | https://www.rawpixel.com/image/6073937/hail-storm_auburn |
| `roof-slate` | wikimedia | CC0 1.0 | Øyvind Holmstad | https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Takskifer.jpg/1280px-Takskifer.jpg | https://commons.wikimedia.org/w/index.php?curid=17182012 |
| `rowhouse-street` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Juniata_Terrace_remarkably_similar_houses.jpg/1280px-Juniata_Terrace_remarkably_similar_houses.jpg | https://commons.wikimedia.org/w/index.php?curid=49167167 |
| `snow-roofs` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/cHJpdmF0ZS9zdGF0aWMvaW1hZ2Uvd2Vic2l0ZS8yMDIyLTA0L2xyL3B4MTE0ODg1Ny1pbWFnZS1rd3Z3YmF5di5qcGc.jpg | https://www.rawpixel.com/image/5913696/image-public-domain-house-interior |
| `snow-street` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvZnJkZWVwX3Nub3dfd2ludGVyX21pY2hpZ2FuXzAtaW1hZ2Uta3liZHd5cTkuanBn.jpg | https://www.rawpixel.com/image/6038822/photo-image-public-domain-house-snow |
| `storm-sky` | rawpixel | CC0 1.0 | unknown | https://images.rawpixel.com/editor_1024/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvd2s3MTMyMDUzMy1pbWFnZS1rcHFuYndveC5qcGc.jpg | https://www.rawpixel.com/image/3372029/free-photo-image-asphalt-cc0-cloud |
| `tornado-damage` | wikimedia | CC0 1.0 | Johnson524 | https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Tornado_damage_from_TS_Debby_in_Lucama_2.jpg/1280px-Tornado_damage_from_TS_Debby_in_Lucama_2.jpg | https://commons.wikimedia.org/w/index.php?curid=151309862 |
| `victorian-house` | wikimedia | CC0 1.0 | Smallbones | https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Joseph_Cassese_House_Scranton_PA.JPG/1280px-Joseph_Cassese_House_Scranton_PA.JPG | https://commons.wikimedia.org/w/index.php?curid=27748685 |
| `water-ceiling` | wikimedia | CC0 1.0 | Indy beetle | https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Eden_Mall_water_damage.jpg/1280px-Eden_Mall_water_damage.jpg | https://commons.wikimedia.org/w/index.php?curid=85607779 |

All 33 are CC0 1.0 (22 Wikimedia Commons, 11 rawpixel). Eleven rawpixel originals are only served at 1024px wide, so their
1200px WebP is a mild upscale (`upscaled: true` in the manifest); they sit behind overlays or in cards. Rejected during review:
one rawpixel tornado photo with a faint watermark and one bungalow photo with a photographer signature. Flickr and StockSnap
blocked automated downloads, so no images came from them (no bot checks were bypassed).

## SEO rules enforced by `validate.py`

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique.
- Meta description **110–143 characters** (under 144), present, unique, ends with a complete sentence, and identical
  to `og:description` and `twitter:description`.
- Exactly one H1, the first heading is the H1, no skipped heading levels anywhere (footer, sidebar and tools included).
- One valid JSON-LD `@graph` per page with ProfessionalService (logo, contactPoint, address region/country,
  areaServed, OfferCatalog), WebSite, exactly one page node (WebPage/AboutPage/ContactPage/CollectionPage) with
  breadcrumb, primaryImageOfPage and mainEntity; every `@id` reference resolves. Service, FAQPage, ItemList,
  WebApplication, BlogPosting, HowTo and DefinedTermSet appear where they apply.
- Canonical URL, Open Graph (with image size and alt), Twitter card and `geo.region` on every page.
- No broken internal links or anchors; `alt` on every image.
- Homepage main content mentions "Pennsylvania Insurance Appraiser" at least 14 times.
- No sister-state names anywhere in the build (list in `validate.py`; note it bans "Delaware", "Ohio" and
  "Washington", so the copy avoids those place names too).
- Every `dir/index.php` starts with the guard line (correct depth) and contains no other PHP; no `index.html` pages.

## Contact form

`/api/contact.php`: honeypot field, per-IP rate limit (5 per 10 minutes), validation (name, consent and a valid email
or phone). It sends through `info@pennsylvaniainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a
JSON line to `api/_private/leads.log.php` (which starts with `<?php http_response_code(404); exit; ?>`).

The config is **never committed** (`_private/` is in `.gitignore`). Hostinger's file API can't write outside
`public_html`, so it lives at `public_html/api/_private/config.php`:

```php
<?php
if (!defined('PIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@pennsylvaniainsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives: upload that file (keep any local copy outside the repo and delete it afterwards),
confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and confirm the
log line shows `"via":"smtp"`.

## Going live checklist

1. Point the domain's nameservers to `orbit.dns-parking.com` and `horizon.dns-parking.com`.
2. Confirm SSL covers both `pennsylvaniainsuranceappraiser.com` and `www.` (`agency-hosting_websites_get` →
   `ssl_cert.names`); reissue with `agency-hosting_ssl_reinstall-website` if www is missing.
3. Check `http://`, `http://www.` and `https://www.` interior pages all 301 to `https://pennsylvaniainsuranceappraiser.com/…`,
   `/page/index.php` 301s to `/page/`, every sitemap URL is 200, and the real domain sends no `X-Robots-Tag`.
4. Create the mailbox and wire SMTP (above). Add GTM if provided.
5. Click **Verify** in Search Console (URL-prefix property), then submit `https://pennsylvaniainsuranceappraiser.com/sitemap.xml`.
