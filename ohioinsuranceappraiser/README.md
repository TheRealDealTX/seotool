# ohioinsuranceappraiser.com — static site

Ohio Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a small
PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `usEtwjHWE` (Agency Growth, order 1008744732, php-fpm, PHP 8.3) |
| Domain | `ohioinsuranceappraiser.com` (attached at creation) |
| Preview URL | https://lightskyblue-ibis-120121.hostingersite.com |
| Nameservers to set at the registrar | `helios.dns-parking.com`, `aster.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@ohioinsuranceappraiser.com |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |

The setup asked for the Boston datacenter (closest to Ohio). Every site on this order shares the same server
(72.60.128.114); Hostinger reports it as `us-phx-h5g-node3`.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 11 service pages (`/appraisal-practice/…`) |
| `src/locations.py` | 12 Ohio city pages (`/service-cities/<city>-ohio/`) |
| `src/tools.py` | 7 tools: markup and copy (`/appraisal-workbench/…`). The logic is in `static/assets/js/app.js` |
| `src/learn.py` | Appraisal timeline, grouped Q&A, 43-term lexicon, 6 briefings |
| `src/photos.json` | Photo metadata (alt, size, title, creator, license, source). Written by `photo_pipeline.py` |
| `src/BRIEF.md` | Content brief: vetted Ohio facts, banned words, copy rules |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `public/` | **Build output.** This is what gets deployed (committed) |
| `validate.py` | Post-build SEO, link, schema and guard checks |
| `deploy.sh` | Uploads `public/` to the website's `public_html` (TUS file API) |
| `photo_pipeline.py` | Source JPGs → 1200px and 640px WebP + `src/photos.json` |
| `make_icons.js` | Brand mark → favicon.svg/ico, PNG and maskable icons, OG image (Playwright) |
| `dev_router.php` | Local router that mimics the host, for `php -S` testing |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # must end with zero ERROR lines
# fresh credentials: agency-hosting_files_generate-upload-url (website_uid usEtwjHWE)
export OIA_FB_URL=… OIA_FB_AUTH=… OIA_FB_REST=…
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites files. If you remove or rename a page, delete the old file on the server:
`DELETE {OIA_FB_URL without /tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.

Local preview that behaves like the host:

```sh
cd public && php -S 127.0.0.1:8000 ../dev_router.php
curl -sI -H 'Host: www.ohioinsuranceappraiser.com' http://127.0.0.1:8000/service-cities/columbus-ohio/   # 301
```

Icons and the OG image: `node make_icons.js static/assets/img/photos/<photo>.webp`, then bump `FAV` in `build.py`.

## Pages (51 in the sitemap, plus the 404)

- Home, About (`/meet-the-firm/`), Contact (`/contact-our-team/`)
- `/appraisal-practice/` + 11 services: appraisal demand representation, home, commercial & HOA, hail & roof,
  tornado & windstorm, derecho & hurricane remnant, water (incl. sewer backup), fire & smoke,
  ice dam & frozen pipe (the Ohio-specific peril), estimate audit, neutral umpire
- `/service-cities/` + 12 cities: Columbus, Cleveland, Cincinnati, Toledo, Akron, Dayton, Canton, Youngstown,
  Sandusky, Lima, Xenia, Zanesville
- `/appraisal-workbench/` + 7 tools: claim gap & fee estimator (three outcomes + break-even), RCV/ACV holdback
  calculator (labor-share option), roof area & pitch calculator (steep/high flags), percentage deductible
  calculator (flat vs 1/2/5%), Ohio claim calendar builder (.ics export, appraisal-demand dates),
  appraisal readiness checkup, basement backup sublimit calculator (new for Ohio)
- `/appraisal-timeline/` (HowTo), `/appraisal-q-and-a/` (FAQ by topic), `/appraisal-lexicon/` (searchable glossary),
  `/appraisal-briefings/` + 6 guides
- `/privacy-commitment/`, `/usage-terms/`, `/disclaimer-notice/`, `/photo-sources/`, `/site-guide/` (HTML site map),
  `404.html` (served with a real 404), `sitemap.xml`, `robots.txt`

The URLs, copy, section order and design differ on purpose from every sister `*insuranceappraiser*` site on
the Hostinger account. `validate.py` fails the build if any sister-state name appears anywhere in `public/`.

## Design

Crimson `#C12637` with a deep shade (`#4A0D16`, `#26070C`), a light tint (`#FCEDEE`), a teal complementary
accent (`#1D7A74`, light `#7FD8CF`) and warm neutrals. Fonts: Red Hat Display for headings and Albert Sans for
body text. No sister site uses either font.

The homepage runs in this order: full-bleed photo hero with a lead form, a four-promise strip, an intro split,
photo service cards, crimson animated counters, a region carousel (scroll-snap with prev/next), a dark five-step
stepper, the workbench (live gap check plus the tool list), a city photo mosaic, an Ohio storm-history timeline,
three "who does what" cards, an FAQ, briefings, a parallax photo CTA and the contact form.

Effects: a header that turns solid on scroll, hero/CTA/page-hero parallax, staggered reveal, counters, card hover
zoom and back-to-top. All motion respects `prefers-reduced-motion`. Without JavaScript nothing is hidden: the reveal
classes only apply once JS adds `body.anim`.

Mobile nav is an off-canvas `#drawer` rendered **outside** the sticky header (a header `backdrop-filter` would trap
`position: fixed` children). It has accordion sections and a scroll lock (body fixed at its scroll offset). It
closes on ×, an overlay tap, a link tap or Escape, and manages `inert`/`aria-hidden`. Its shadow and visibility
apply only while it's open. A fixed call bar sits at the bottom on phones. The brand link in the header, drawer
and footer never changes color on hover.

## Photos

36 royalty-free photos (CC0 or public domain), found through the Openverse API (`license=cc0,pdm`): StockSnap,
rawpixel, Flickr and Wikimedia Commons / US government. Each is a 1200px and a 640px WebP in
`static/assets/img/photos/`, used with `srcset`/`sizes` and width/height set. Each has descriptive alt text,
decorative backgrounds use `alt=""`, and all are listed with license and source on `/photo-sources/`.
To add one: put the JPG in a folder, add metadata to the shortlist JSON and alt text to `ALT` in
`photo_pipeline.py`, then run `python3 photo_pipeline.py <dir> <shortlist.json>`.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" switch. It **serves real files directly**
  (running a directory's `index.php`) and sends `/` and unknown paths to the root `index.php`. A `dir/index.html`
  page would skip any redirect logic, so `http://www.…/page/` would load with a 200.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by plain HTML with no other PHP.
  The homepage is `home.html`, served by the front controller. There is no root `index.html`, and the build
  refuses to write any `dir/index.html`.
- `_guard.php`:
  - 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://ohioinsuranceappraiser.com`, only on the real domain
  - 301s `/dir/index.php` and `/index.php` to the directory URL
  - sends `X-Robots-Tag: noindex, nofollow` on every other host (such as the preview URL)
  - returns 404 if requested directly
- `index.php` requires the guard. It serves `home.html` for `/`, 301s directory URLs that lack the trailing slash,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404 status.
- On the preview URL Hostinger serves its own Googlebot-blocking `robots.txt`; that is expected. The real domain
  serves ours.

## SEO rules (enforced by validate.py)

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px). Meta description 110–150 characters. Titles and descriptions unique
- Exactly one H1, the first heading is the H1, and no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD where every `@id` reference resolves. No broken internal links or anchors. Every image has `alt`
- The homepage's `<main>` mentions "Ohio Insurance Appraiser" at least 14 times
- No sister-state names. Every `dir/index.php` starts with the guard line and has no other PHP. No `dir/index.html`

Each page's JSON-LD `@graph` has:
- the ProfessionalService (logo ImageObject, contactPoint, OH/US address, Ohio + cities as areaServed, OfferCatalog)
- the WebSite
- one page node (WebPage / AboutPage / ContactPage / CollectionPage) linked to its BreadcrumbList, primary image and main entity
- Service, FAQPage, ItemList, WebApplication, BlogPosting, HowTo or DefinedTermSet where they apply

## Contact form

`/api/contact.php` has a honeypot, a per-IP limit (5 per 10 minutes) and validation. It sends each lead
through `info@ohioinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when
`api/_private/config.php` exists, and falls back to PHP `mail()`. Every submission is appended to
`api/_private/leads.log.php`. Both private files 404 when requested directly: the config through its defines-guard,
the log through its `<?php http_response_code(404); exit; ?>` header. They live inside `public_html` because the
Hostinger file API can't write above it. `_private/` is in `.gitignore`. **Never commit the password.**

Config to upload (keep any local copy outside the repo and delete it after uploading):

```php
<?php
if (!defined('OIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@ohioinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading:
1. Check that `/api/_private/config.php` returns 404 with 0 bytes.
2. Send one test submission labelled TEST.
3. Check that the log shows `"via":"smtp"`.

## Going live checklist

1. Point the domain's nameservers to `helios.dns-parking.com` and `aster.dns-parking.com`.
2. Check that SSL covers both `ohioinsuranceappraiser.com` and `www.` (`agency-hosting_websites_get` → `ssl_cert.names`).
   If `www` is missing, run `agency-hosting_ssl_reinstall-website`.
3. Check the www/http/`index.php` redirects on the homepage and on interior pages, check that every sitemap URL
   returns 200, and check the real domain sends no `X-Robots-Tag`.
4. Create the mailbox and upload `api/_private/config.php` (see above).
5. Add the GTM container ID to `GTM_ID`, rebuild, validate, redeploy and clear the cache.
6. Submit `https://ohioinsuranceappraiser.com/sitemap.xml` to Google Search Console.
