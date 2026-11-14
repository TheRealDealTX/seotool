# virginiainsuranceappraiser.com: static site

Virginia Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it,
and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.
The engineering (generator, validator, deploy script, form handler, tool logic) is adapted from the Georgia
template; the copy, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `u35aHyasJ` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter requested) |
| Domain | `virginiainsuranceappraiser.com` (attached at creation) |
| Preview URL | https://springgreen-hippopotamus-295995.hostingersite.com |
| Nameservers to set at the registrar | `nova.dns-parking.com`, `cosmos.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@virginiainsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | not set yet (`GTM_ID = ""` in `build.py`) |

Until the nameservers point to Hostinger the real domain won’t resolve and SSL can’t be issued, so live checks
run on the preview URL. Hostinger serves its own Googlebot-blocking `robots.txt` on preview hosts. That’s expected.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php`, GSC file |
| `src/services.py` | 12 service pages (one keyword each, `kw`) |
| `src/locations.py` | 12 locality pages, each with its own title and description |
| `src/tools.py` | 7 interactive tools (markup and copy; logic is in `static/assets/js/app.js`) |
| `src/learn.py` | Process guide (7 steps), grouped FAQ, 42-term glossary, 6 guides |
| `src/photos.json` | Internal photo manifest: source URL, license, creator, size and alt text. Not published |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `public/` | **Build output** that gets deployed (committed) |
| `validate.py` | Post-build checks; must report zero errors |
| `deploy.sh` | Uploads `public/` to the website’s `public_html` over the TUS upload API |
| `dev-router.php` | Local stand-in for the host: `php -S 127.0.0.1:8080 -t public dev-router.php` |

## Build and deploy

```sh
python3 build.py && python3 validate.py
```

Then get fresh upload credentials with `agency-hosting_files_generate-upload-url` (website_uid `u35aHyasJ`)
and run:

```sh
export VIA_FB_URL='…' VIA_FB_AUTH='…' VIA_FB_REST='…'
./deploy.sh
```

Finish by clearing the cache with `agency-hosting_cache_clear-website`.

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server with
`DELETE {url-without-/tus}/resources/public_html/<path>` and the same two auth headers.

## Hosting notes: why every page is `dir/index.php`

- The host ignores `.htaccess`, has no “force HTTPS” switch on the Agency plan, and **serves real files directly**
  (running a directory’s `index.php`) without passing through the root `index.php`. A `dir/index.html` page would
  skip any redirect logic, so `http://www.…/any-page/` would load with a 200.
- So every page except the homepage is written as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by the static HTML. The page HTML contains no
  other `<?`. The homepage is `home.html`, served by the front controller. The only other root `.html` files are
  `404.html` and the Search Console file.
- `_guard.php`:
  - 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://virginiainsuranceappraiser.com`, only on the real domain
  - 301s `/dir/index.php` (and `/index.php`) to `/dir/`
  - sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview domain
  - returns 404 when requested directly
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Never create a root `index.html` and never leave a `dir/index.html` on the server. `validate.py` fails the build if
  any static `.html` page other than `home.html`, `404.html` and the GSC file exists, and checks the guard line
  (and its depth) on every `dir/index.php`.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents, a single line with no trailing newline, HTML wrapper, guard, GTM or BOM:
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it on every build from the `GSC_FILE`/`GSC_BODY` constants, so a rebuild never drops it.
  `validate.py` compares the bytes and keeps it out of the page checks, `sitemap.xml`, the HTML site map and internal links.
  `robots.txt` doesn’t block it.
- It must stay at the root permanently: Google rechecks it, and removing it unverifies the property. HTML-file
  verification works only for a **URL-prefix** property (`https://virginiainsuranceappraiser.com/`). A Domain property
  needs a DNS TXT record instead. It’s a real file, so the host serves it directly and the guard doesn’t run for it.

## Pages (51 in sitemap, plus 404)

Each page has one main keyword.

- Home: `Virginia Insurance Appraiser` (validate.py requires at least 14 uses in `<main>`)
- `/about-our-appraisers/`, `/schedule-a-claim-review/` (contact)
- `/appraisal-and-umpire-services/` plus 12 services: appraisal clause representation, homeowners, commercial & HOA,
  roof & hail, wind & tornado, hurricane & nor’easter, water, fire & smoke, fallen tree & ice storm (state peril),
  historic home, estimate review, umpire services
- `/virginia-localities/` plus 12 localities (`/virginia-localities/insurance-appraiser-<place>-va/`): Virginia Beach,
  Norfolk, Chesapeake, Newport News, Richmond, Arlington, Alexandria, Fairfax County, Fredericksburg,
  Charlottesville, Roanoke, Lynchburg
- `/calculators-for-policyholders/` plus 7 tools: claim gap & fee estimator, holdback recovery (RCV/ACV) calculator,
  roof pitch & squares checker, hurricane & wind deductible converter, claim clock & calendar builder (.ics export),
  appraisal readiness scorecard, and a Virginia-specific fallen tree claim splitter (debris-removal limits)
- `/virginia-appraisal-steps/` (HowTo), `/virginia-appraisal-questions/` (FAQ by topic),
  `/claim-and-policy-terms/` (42-term searchable glossary), `/policy-and-claim-guides/` plus 6 guides
- `/how-we-handle-data/` (privacy), `/website-terms-of-use/`, `/disclaimer-and-notices/`, `/site-contents/` (HTML site map), `404.html`
- There is no photo-credits page, by design.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique
- Meta description **110–143 characters** (under 144), unique, ending in a full sentence, and identical in
  `og:description` and `twitter:description`
- Exactly one H1, the first heading is the H1, and no skipped heading levels anywhere (footer, sidebar boxes and tool
  widgets included; tool titles are styled `<p>`s)
- Canonical to `https://virginiainsuranceappraiser.com/...` (404 is noindex and has none), Open Graph with image size
  and alt, Twitter card tags and `geo.region`
- One JSON-LD block per page whose `@graph` holds ProfessionalService (logo, contactPoint, address, areaServed,
  OfferCatalog), WebSite, exactly one page node (WebPage, AboutPage, ContactPage or CollectionPage) linked to its
  BreadcrumbList, primary image and main entity, plus Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo
  or DefinedTermSet where relevant. Every `@id` reference must resolve
- No broken internal links or anchors, alt on every image, every indexable page in `sitemap.xml`
- No sister-state names anywhere in the output (31 names, including “Washington” and “West Virginia”) and no photo-credit references

## Contact form

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation (name, plus a valid
email or a phone number, plus consent). It sends through `info@virginiainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a
JSON line to `api/_private/leads.log.php`, which starts with `<?php http_response_code(404); exit; ?>`.

The SMTP password is never committed (`_private/` is in `.gitignore`). The Hostinger file API can’t write outside
`public_html`, which is why the private files sit under `api/_private/`. Both return 404 when requested directly.
The config file looks like this:

```php
<?php
if (!defined('VIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@virginiainsuranceappraiser.com', 'smtp_pass' => '…'];
```

When the mailbox password arrives:

1. Upload the config, keeping any local copy outside the repo and deleting it afterwards.
2. Confirm `/api/_private/config.php` returns 404 with 0 bytes.
3. Send one submission labelled as a test.
4. Confirm the log shows `"via":"smtp"`.

## Google Tag Manager

Set `GTM_ID` in `build.py` (e.g. `"GTM-XXXXXXX"`) and rebuild. That outputs the standard head snippet and the
`<noscript>` iframe straight after `<body>`. If a full snippet is provided, use it exactly as given.

## Design

- Palette from `#00297B`: deep `#00163F`, ink navy `#0B1530`, light tint `#E9EEF9`, complementary brick-orange accent
  `#F08A4B`, warm paper `#FBFAF7` and slate neutrals
- Fonts: Libre Caslon Text (display) with Public Sans (body)
- Photo-led layout:
  - full-bleed parallax hero with a lead form card
  - overlapping “ledger” counter strip
  - photo cards for services, tools, guides and localities
  - a horizontal seven-step process track that fills on scroll
  - expanding region photo panels (CSS-only)
  - a Virginia ground-rules fact grid
  - parallax CTA
  - photo heroes and a sticky two-column sidebar on interior pages
- Effects: scroll progress bar, header that turns solid navy on scroll (no `backdrop-filter`), staggered reveal,
  animated counters, hover zoom, back-to-top. 3D tilt and the marquee were deliberately left out
- Mobile: off-canvas drawer rendered outside the header (accordion submenus, scroll lock, closes on ×, overlay tap,
  link tap or Escape, `inert`/`aria-hidden` handling, shadow only while open) and a fixed call bar
- Everything respects `prefers-reduced-motion` and renders without JavaScript
- Logo: navy tile with a white roof/house line over a brick-orange “ledger” bar. `favicon.svg`, multi-size
  `favicon.ico` (bold variant at 16/32/48), 96px PNG, full-bleed 180px apple-touch icon and maskable 192/512 icons,
  all with `?v=` cache-busters

## Photos

All 30 photos are CC0 or public domain, so no credit is legally required and the site has **no photo-credits page**. Every license was checked on the source page, not only in search results. This list is internal (it is not linked from the site). Each photo is served as `assets/img/photos/<key>.webp` (up to 1200px) plus `<key>-640.webp`, with `srcset`, and alt text from `desc` in `src/photos.json`. `assets/img/og-image.jpg` (1200×630) is cropped from `hero-brick-colonial`.

| Key | Title / creator | License | Source |
| --- | --- | --- | --- |
| `richmond-skyline` | Richmond, Virginia skyline from Shockoe Bottom (Packer1028) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=154257469) |
| `virginia-beach` | Old Coast Guard Station 24th Atlantic in Virginia Beach (BretFisher) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=23170926) |
| `norfolk-waterfront` | Coast Guard participates in Norfolk, Va. OpSail 2012's Parade of Sails (Petty Officer 3rd Class David Marin) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:Coast_Guard_participates_in_Norfolk,_Va._OpSail_2012%27s_Parade_of_Sails_120608-G-MD940-715.jpg) |
| `chesapeake-waterway` | Great Dismal Swamp National Wildlife Refuge- Peaks October 22 – Octobe (U. S. Fish and Wildlife Service - Northe) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:Great_Dismal_Swamp_National_Wildlife_Refuge-_Peaks_October_22_%E2%80%93_October_28_(50432511333).jpg) |
| `newport-news-james` | Newport News Shipyard, aerial view, Oct 1994 (Don S. Montgomery) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:Newport_News_Shipyard,_aerial_view,_Oct_1994.jpeg) |
| `alexandria-old-town` | King Street, Alexandria, Virginia (Hermann Luyken) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=64154474) |
| `arlington-rosslyn` | Rosslyn from Georgetown 2 (Theodore Christopher) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/wiki/File:Rosslyn_from_Georgetown_2.jpg) |
| `fairfax-suburb` | Tree Outside Suburban Homes (Image Catalog) | CC0 1.0 | [flickr](https://www.flickr.com/photos/132795455@N08/16681992243) |
| `fredericksburg-downtown` | View of Fredericksburg across Rappahannock from Chatham grounds at sun (Mary O'Neill) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:View_of_Fredericksburg_across_Rappahannock_from_Chatham_grounds_at_sunset_(02f56597-2c8c-4090-a152-70a325f8dcf8).jpg) |
| `charlottesville-rotunda` | University of Virginia Rotunda 2006 (Aaron Josephson; cropped by Ibn Battuta) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:University_of_Virginia_Rotunda_2006.jpg) |
| `roanoke-valley` | Star (apbell427) | Public Domain Mark | [flickr](https://www.flickr.com/photos/146431966@N02/45889362585) |
| `lynchburg-hills` | Downtown Lynchburg (Northern-Virginia-Photographer) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=166226973) |
| `blue-ridge-mountains` | Skyline Drive, Shenandoah National Park (stefanserena) | CC0 1.0 | [flickr](https://www.flickr.com/photos/146738176@N02/46992330511) |
| `hero-brick-colonial` | Locust Grove, Louisville, KY (w_lemay) | CC0 1.0 | [flickr](https://www.flickr.com/photos/59081381@N03/27225898877) |
| `hurricane-flooding` | Hurricane Irma Flooding in Vero Beach (WeatheredAviation) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/wiki/File:Hurricane_Irma_Flooding_in_Vero_Beach.jpg) |
| `storm-roof-damage` | FEMA - 29543 - Blue roof tarps in Texas (Earl Armstrong) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:FEMA_-_29543_-_Blue_roof_tarps_in_Texas.jpg) |
| `hail-shingles` | Kroupy (Karel Štípek) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/wiki/File:Kroupy.jpg) |
| `tree-on-house` | FEMA - 8462 - Photograph by Mark Wolfe taken on 09-21-2003 in North Ca (Mark Wolfe) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:FEMA_-_8462_-_Photograph_by_Mark_Wolfe_taken_on_09-21-2003_in_North_Carolina.jpg) |
| `ice-storm` | Ice Storm Tree Damage (David Kitto) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=128350213) |
| `tornado-damage` | Low-end EF3 damage to a home in Virginia Beach, Virginia (National Weather Service) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:Low-end_EF3_damage_to_a_home_in_Virginia_Beach,_Virginia.jpg) |
| `fire-damage` | Fire-Damaged House at Buxted (October 2010) (User:Hassocks5489) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/wiki/File:Fire-Damaged_House_at_Buxted_(October_2010).jpg) |
| `water-ceiling` | Ceiling sheetrock damaged by water so paint was peeling (Tomwsulcer) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/wiki/File:Ceiling_sheetrock_damaged_by_water_so_paint_was_peeling.jpg) |
| `roofer-shingles` | FEMA - 44634 - Roofer working on a home in Oklahoma (Patsy Lynch) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:FEMA_-_44634_-_Roofer_working_on_a_home_in_Oklahoma.jpg) |
| `storm-sky` | Sunset Thunderstorm (53721202248) (Bob Hyatt, U.S. National Weather Service) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:Sunset_Thunderstorm_(53721202248).jpg) |
| `condo-building` | Modern apartment building (DennisM2) | CC0 1.0 | [flickr](https://www.flickr.com/photos/14674348@N04/14996764996) |
| `historic-interior` | Ossian Sweet House interior - fireplace (City of Detroit) | CC0 1.0 | [wikimedia](https://commons.wikimedia.org/w/index.php?curid=174254044) |
| `consult-table` | Free close two people hands (rawpixel) | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5927609/photo-image-background-public-domain-hands) |
| `calculator-papers` | Accounting Finance (Wilfred Iven) | CC0 1.0 | [stocksnap](https://stocksnap.io/photo/accounting-finance-JONMP7TPGK) |
| `tape-measure` | FEMA - 44370 - FEMA PA officer documenting damages to a roof in OK (Win Henderson) | Public Domain Mark | [wikimedia](https://commons.wikimedia.org/wiki/File:FEMA_-_44370_-_FEMA_PA_officer_documenting_damages_to_a_roof_in_OK.jpg) |
| `laptop-estimate` | Laptop with spreadsheet (rawpixel) | CC0 1.0 | [rawpixel](https://www.rawpixel.com/image/5974308/photo-image-laptop-work-macbook) |
