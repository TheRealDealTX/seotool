# arkansasinsuranceappraiser.com — static site

Arkansas Insurance Appraiser: a static site with no database and no plugins. A Python generator
builds it, and a small PHP guard + front controller serves it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `ZZxCZVdjC` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Live domain | https://arkansasinsuranceappraiser.com (SSL covers apex + www; www and http 301 to it) |
| Preview URL | https://dodgerblue-kingfisher-478637.hostingersite.com |
| Nameservers to set at the registrar | `aurora.dns-parking.com`, `nebula.dns-parking.com` (from `agency-hosting_websites_get`) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@arkansasinsuranceappraiser.com (form delivers over SMTP, verified Nov 13, 2026) |
| Google Tag Manager | `GTM-MQTN2KFK` (head snippet exactly as provided + noscript iframe after `<body>`) |
| Search Console | `googlecccfbf2f7e9e5ae4.html` verification file in `static/` (skipped by validate.py) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 11 service pages (one main keyword each, `kw`) |
| `src/locations.py` | 12 Arkansas city pages |
| `src/tools.py` | 7 interactive tools (markup + copy); logic in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 steps), grouped FAQ, 42-term glossary, 6 guides |
| `src/photos.json` | Photo metadata (title, creator, license, source, sizes), used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`, copied into `public/` as is |
| `tools/make_icons.py` | Regenerates favicon set, manifest and OG image (Pillow) |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks (must exit 0) |
| `deploy.sh` | Uploads `public/` to `public_html` over the TUS file API |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# fresh creds: agency-hosting_files_generate-upload-url (website_uid ZZxCZVdjC); they expire after a few hours
export AIA_FB_URL=… AIA_FB_AUTH=… AIA_FB_REST=…
./deploy.sh            # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` / `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` has already been deleted. `api/_private/` (SMTP config, lead log) lives only on the server; leave it in place.

Local preview that mimics the host: `cd public && php -S 127.0.0.1:8765 ../tools/router.php`. The router serves
real files directly, executes `.php` files and a directory's `index.php`, and sends everything else to `index.php`.

## URL structure (different from every sister site)

- Home `/` · `/company/` · `/contact-an-appraiser/`
- `/claim-appraisal-services/` + 11 services
- `/arkansas-locations/` + 12 cities at `/arkansas-locations/<city>-appraiser/`
- `/property-claim-tools/` + 7 tools: claim gap & fee estimator, RCV vs. ACV holdback (with labor-share toggle),
  roof pitch & squares, percentage deductible, claim timeline builder (.ics), appraisal readiness checkup,
  ice load limb calculator (Arkansas-specific)
- `/appraisal-process-explained/`, `/faq/`, `/insurance-claim-glossary/`, `/appraisal-guides/` + 6 guides
- `/privacy-information/`, `/website-use-terms/`, `/appraisal-disclaimer/`, `/photo-credits/`, `/site-navigation/`, 404

52 HTML files, 51 URLs in `sitemap.xml`.

## Hosting notes (why every page is `dir/index.php`)

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly without
  running the root `index.php`**. A `dir/index.html` page would skip any redirect, so `http://www.…/page/` would load with 200.
- So the homepage is `home.html` (served by the front controller) and every other page is `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP; `validate.py` enforces this).
- `_guard.php` 301s `www.` and plain http (`X-Forwarded-Proto`, falling back to `HTTPS`) to `https://arkansasinsuranceappraiser.com`
  only on the real domain, 301s `/dir/index.php` and `/index.php` to the directory, sends `X-Robots-Tag: noindex, nofollow` on any
  other host (the preview URL), and 404s if requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, 301s directories to add the trailing slash, includes `dir/index.php`
  for directory URLs that reach it, and returns `404.html` with a real 404.
- Never create a root `index.html` or any `dir/index.html` (validate.py fails if one exists).
- On the preview URL Hostinger serves its own Googlebot-blocking `robots.txt`; that's expected. The real domain serves ours.

## Contact form

`/api/contact.php`: honeypot (`website`), per-IP rate limit (5 per 10 minutes), validation (name + valid email or phone + consent).
It sends through `info@arkansasinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, falls back to `mail()`, and always appends a JSON line to `api/_private/leads.log.php`
(created with a `<?php http_response_code(404); exit; ?>` header so it 404s). `_private/` is git-ignored; the Hostinger file API
can't write outside `public_html`, which is why it sits there. Config file (upload it, never commit it):

```php
<?php
if (!defined('AIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@arkansasinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading: confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test, and check the log shows `"via":"smtp"`.

## Design

- Palette: dark red `#8f1d24` (deep `#4a0d12`, deepest `#2b070a`, tint `#fbf0f0`), complementary teal `#157570` / `#4fc1b9`,
  warm stone neutrals (`#f6f2ee`, `#fcfbf9`, ink `#1f1a1b`). Gradients only on hero overlays and red CTA bands.
- Fonts: Red Hat Display (headings) + Red Hat Text (body). No sister site uses this pair.
- Mark: dark red badge with a white roofline over a teal diamond (a nod to Arkansas's diamond field), used in header, drawer and footer.
- Effects: header turns solid white on scroll (no `backdrop-filter`), parallax hero and CTA, staggered reveals, animated counters,
  hover zoom on photo cards, CSS-sticky stacking process cards, horizontal region rail with prev/next buttons, seasonal claim
  calendar, back-to-top button with a scroll-progress ring. All respect `prefers-reduced-motion`; content renders without JS.
- Mobile: off-canvas drawer from the left, outside the fixed header, with accordion submenus, scroll lock, close on ×/overlay/link/Escape,
  `inert` + `aria-hidden`, shadow and visibility only while open. Fixed call bar at the bottom.

## Photos

38 royalty-free photos (CC0 or public domain) found through the Openverse API (`license=cc0,pdm`): Flickr CC0/PD (including
USDA, U.S. Forest Service, USFWS and FEMA-era Arkansas tornado photos from Atkins), Wikimedia Commons CC0 (Little Rock, Springdale,
Fayetteville, Pine Bluff, aerial roofs), rawpixel CC0, StockSnap and WordPress Photos. Downloaded one at a time with pauses and
backoff, Wikimedia at the 1280px thumbnail width. Each is a ≤1200px and a 640px WebP with `srcset`/`sizes`, width and height.
None reuse the sister Georgia set. All are listed with license and source on `/photo-credits/`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; unique titles and descriptions
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/CollectionPage) with breadcrumb,
  primaryImageOfPage and mainEntity; complete ProfessionalService node (logo, contactPoint, address, areaServed, OfferCatalog)
- Canonical, OG image size/alt, Twitter card and `geo.region` on every page
- No broken internal links or anchors; `alt` on every image
- "Arkansas Insurance Appraiser" ≥ 14 times in the homepage `<main>` (currently 20; 25 in all visible text)
- No sister-state names (Alabama, Arizona, Delaware, Florida, Georgia, Kentucky, Maine, Maryland, Massachusetts, Missouri,
  Montana, Nevada, New York, North Carolina, West Virginia, Wyoming) anywhere in the build
- Every `dir/index.php` starts with the guard line and contains no other PHP; no `index.html` anywhere

## Going live checklist

1. ~~Point the nameservers~~ — done; SSL covers `arkansasinsuranceappraiser.com` and `www.` (Hostinger `ssl_cert.names`).
2. ~~Check the canonical host on the live domain~~ — done Nov 13, 2026: http, www and `/index.php` 301 to the https apex on the
   homepage and four interior pages; all 51 sitemap URLs return 200 with no `X-Robots-Tag`; our `robots.txt` is served.
3. ~~Mailbox + SMTP~~ — done; config URL returns 404 with 0 bytes, test submission logged with `"via":"smtp"`.
4. ~~GTM~~ — done (`GTM-MQTN2KFK`). ~~GSC verification file~~ — done.
5. Submit `https://arkansasinsuranceappraiser.com/sitemap.xml` to Google Search Console.

## Mobile tables

Wide tables (homepage comparison, tool scenario tables, holdback line items, photo credits) carry the `stack-sm` class and become
labelled cards at ≤700px (`td[data-label]`), so nothing is cut off or needs sideways scrolling at 390px.
