# utahinsuranceappraiser.com — static site

Utah Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it,
and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.
The engineering came from `georgiainsuranceappraiser/` (generator, `validate.py`, `deploy.sh`,
`api/contact.php`, the calculator logic and the guard). The content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `EAf4DuRFX` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | `utahinsuranceappraiser.com` (attached when the site was created) |
| Live | https://utahinsuranceappraiser.com (SSL covers apex and www; www and http 301 to it) |
| Preview URL | https://bisque-salmon-709623.hostingersite.com (sends `X-Robots-Tag: noindex, nofollow`) |
| Nameservers to set at the registrar | `atlas.dns-parking.com`, `hyperion.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@utahinsuranceappraiser.com (form delivers over SMTP) |
| Google Tag Manager | `GTM-NPG24925`: the owner's head snippet, used verbatim, plus the noscript iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php`, `_guard.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 Utah community pages |
| `src/tools.py` | 7 calculators (markup and copy). Their logic is in `static/assets/js/app.js` |
| `src/learn.py` | Process guide (8 steps), FAQ in 4 topic groups, 41-term glossary, 6 articles |
| `src/photos.json` | Photo metadata (title, creator, license, source, size, alt text) |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`, copied into `public/` as-is |
| `public/` | **Build output.** This is what gets deployed |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the TUS file API |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# get fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid EAf4DuRFX)
export UIA_FB_URL=… UIA_FB_AUTH=… UIA_FB_REST=…
./deploy.sh        # then clear the cache: agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites files. If a page is removed or renamed, delete the old file on the
server with `DELETE {url-without-/tus}/resources/public_html/<path>` and the same two auth headers.

To preview locally with the host's behavior (real files served directly, a directory's `index.php`
executed, everything else sent to `index.php`), run `php -S 127.0.0.1:8099 -t public router.php`
with a router that does exactly that.

## Pages (51 in the sitemap, plus the 404 page)

- Home, `/our-company/`, `/contact-utah-appraiser/`
- `/utah-appraisal-services/` and 12 services: appraisal clause representation, homeowner,
  commercial and HOA, roof and hail, wind and tornado, snow load / ice dam / freeze, water, fire and smoke,
  wildfire, earthquake (endorsement claims), estimate review, umpire services
- `/utah-communities/` and 12 cities: Salt Lake City, West Valley City, Sandy, Provo, Orem, Lehi,
  Ogden, Layton, St. George, Logan, Park City, Cedar City
- `/utah-claim-calculators/` and 7 calculators: claim gap and fee estimator, RCV to ACV holdback,
  roof pitch and squares, percentage deductible (earthquake, wind, hail), claim timeline planner
  (.ics export, Utah 3-year suit default), appraisal readiness checkup, roof snow load estimator (new for Utah)
- `/how-utah-appraisal-works/` (HowTo), `/utah-appraisal-faq/`, `/claim-terms-glossary/` (searchable),
  `/utah-claim-articles/` and 6 articles
- `/your-privacy/`, `/use-terms/`, `/legal-disclaimers/`, `/utah-site-map/`, `404.html`
  (a `/photo-credits/` page was removed at the owner's request on Nov 13, 2026 and deleted from the server)

None of the URL bases are used by a sister site.

## Design

- Palette: navy `#071D49` (main), deep `#030E26`, mid navy `#123574`, light tint `#E9EEF8`,
  canyon-orange accent `#E0703A` (dark `#B9531F`), sand neutral `#F7F2EA`, ink `#121A2B`, muted `#566079`
- Fonts: Urbanist (headings) and Work Sans (body). No sister site uses either one
- Effects: header that turns solid on scroll, parallax hero and photo CTA, staggered reveal, animated
  counters, card hover zoom, expanding region panels ("five claim climates"), a process rail that fills
  as it comes into view, and a back-to-top button. No progress bar, marquee or 3D tilt, which Georgia uses.
  Everything respects `prefers-reduced-motion`, and pages render fully without JavaScript
  (`no-js` / `js` classes on `<html>`)
- Mobile: off-canvas drawer `#drawer` placed outside the fixed header, with accordion submenus,
  scroll lock and `inert`/`aria-hidden` handling. It closes with ×, an overlay tap, a link tap or Escape,
  and gets its shadow and visibility only while open. There is a fixed call bar at the bottom.
- Logo: a navy square with white peaks and an orange sun. `favicon.svg`, a multi-size `favicon.ico`
  (16/32/48, bolder mark), a 96px PNG, a full-bleed 180px apple-touch icon, maskable 192/512 PNGs in
  `site.webmanifest`, and `?v=` cache-busters on every icon link. The brand link doesn't change color
  on hover in the header, drawer or footer.

## Photos

35 photos, all CC0 or public domain, found through the Openverse API (`license=cc0,pdm`): StockSnap,
Wikimedia Commons (including Utah city photos), Flickr public-domain (U.S. Forest Service, including
the 2017 Brian Head Fire) and others. Every candidate was checked against the photo URLs of all sister
sites in this repo, and none are reused. They were downloaded one at a time with pauses (Wikimedia
1280px thumbnails), center-cropped where needed and saved as 1200px and 640px WebP. Pages use them with
`srcset`/`sizes`, width and height. Alt text is descriptive, and decorative backgrounds use `alt=""`.
Each photo's title, creator, license and source URL is kept in `src/photos.json` (there is no public credits page).

## Hosting notes (why every page is `dir/index.php`)

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting. It **serves real files
  directly** (a directory's `index.php` included) and sends only `/` and unknown paths to the root `index.php`.
  So a `dir/index.html` page would skip any redirect, and `http://www.…/page/` would load with a 200.
- Every page is written as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP.
  The homepage is `home.html`, served by the front controller.
- `_guard.php` does four things. It 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`)
  to `https://utahinsuranceappraiser.com`, only on the real domain. It 301s `/dir/index.php` and `/index.php`
  to the directory. It sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview URL.
  It returns 404 when requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing
  slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- Never add a root `index.html` or leave a `dir/index.html` on the server.
- The server also holds `googlecccfbf2f7e9e5ae4.html` (Google Search Console verification) and
  `api/_private/` (SMTP config and lead log). None of them are in git, and `deploy.sh` never deletes them. Leave them in place.
- On the preview URL, Hostinger serves its own Googlebot-blocking `robots.txt`. That's expected. Our
  `robots.txt` is served on the real domain.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px)
- Meta description 110–150 characters, with unique titles and descriptions
- Exactly one H1, the first heading is the H1, and no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD. The graph needs a ProfessionalService, a WebSite and exactly one page node, and every
  `@id` reference must resolve
- Canonical to `https://utahinsuranceappraiser.com/…`, OG image size and alt, Twitter card, `geo.region` US-UT
- No broken internal links or anchors, and an `alt` on every image
- "Utah Insurance Appraiser" at least 14 times in the homepage `<main>` (currently 19, or 24 counting the header and footer)
- No sister-state names anywhere in the build (24 states: Alabama … Wyoming, including ND, MN and RI)
- Every `dir/index.php` starts with the guard line and has no other PHP

Each page's JSON-LD graph holds the ProfessionalService (logo ImageObject, contactPoint, addressRegion UT,
areaServed state and cities, OfferCatalog of the 12 services), the WebSite, and one WebPage, AboutPage,
ContactPage or CollectionPage node. That node links to its BreadcrumbList, primary image and main entity.
Service pages and community pages add a Service node. Pages also add FAQPage, ItemList (index pages),
WebApplication (calculators), BlogPosting (articles), HowTo (process guide) and DefinedTermSet (glossary)
where they apply.

## Contact form delivery

`/api/contact.php` has a honeypot field, a per-IP limit (5 per 10 minutes) and validation (a name, an
email or phone, and consent). When `api/_private/config.php` exists, it sends through
`info@utahinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`). Otherwise it falls
back to PHP `mail()`. Either way it always appends a JSON line to `api/_private/leads.log.php`, which starts
with `<?php http_response_code(404); exit; ?>`. Hostinger's file API can't write outside `public_html`,
which is why the private folder sits there. `_private/` is in `.gitignore`, so **never commit credentials**.

Upload this as `public_html/api/_private/config.php` once the mailbox exists. Keep any local copy outside
the repo and delete it after uploading:

```php
<?php
if (!defined('UIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@utahinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm the config URL returns 404 with 0 bytes, send one submission labelled as a test, and check
that the log line shows `"via":"smtp"`.

## Google Tag Manager

`GTM_ID` and `GTM_HEAD` in `build.py` hold the container (`GTM-NPG24925`) and the owner's head snippet,
used exactly as supplied. The `<noscript>` iframe goes right after `<body>`. Set `GTM_ID = ""` to remove both.

## Going live checklist (all done Nov 13, 2026 except Search Console)

1. Point the domain's nameservers to `atlas.dns-parking.com` and `hyperion.dns-parking.com`.
2. Confirm SSL is active and covers both `utahinsuranceappraiser.com` and `www.` (`agency-hosting_websites_get`
   → `ssl_cert.names`). The first certificate covered only `www`; it was reissued with
   `agency-hosting_ssl_reinstall-website` and now lists both names.
3. On the homepage and at least three interior pages, check that http, http www and https www all 301
   to `https://utahinsuranceappraiser.com/page/`, and that `/page/index.php` 301s to `/page/`. Check that every
   sitemap URL returns 200, and that the real domain sends no `X-Robots-Tag` and serves our `robots.txt`.
   If a www URL still returns 200 with `x-hcdn-cache-status: HIT`, clear the cache and check again.
4. Create the mailbox, upload the SMTP config and run the test above.
5. Add GTM if wanted, then redeploy and clear the cache.
6. Submit `https://utahinsuranceappraiser.com/sitemap.xml` in Google Search Console.
