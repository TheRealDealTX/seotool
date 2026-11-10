# massachusettsinsuranceappraiser.com — static site

Massachusetts Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a
small PHP front controller serves it on a Hostinger Agency Growth website. The engineering (generator, `validate.py`,
`deploy.sh`, `api/contact.php`, tool logic, favicon and photo pipelines) came from `georgiainsuranceappraiser/`. Content,
URL slugs and design are new and differ from every sister site.

| | |
| --- | --- |
| Hostinger website UID | `GhANGdvRH` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Boston datacenter requested) |
| Temporary URL | https://mediumaquamarine-squirrel-144702.hostingersite.com |
| Final domain | https://massachusettsinsuranceappraiser.com (not connected yet) |
| Google Tag Manager | none yet. Set `GTM_ID` (and optionally `GTM_HEAD_SNIPPET`) in `build.py` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@massachusettsinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, GTM toggle |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 city pages |
| `src/tools.py` | 7 interactive estimators (markup and copy). The logic is in `static/assets/js/app.js` |
| `src/learn.py` | Roadmap steps and body, FAQ groups, 44-term glossary, 6 claim-library guides |
| `src/photo_sources.json` | The chosen CC0/PD photos (source URL, title, creator, license, landing page) |
| `src/photos.json` | Generated photo metadata with final sizes. Used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`. Copied into `public/` unchanged |
| `tools/photos.py` | Photo pipeline: downloads each source and writes 1200px and 640px WebP |
| `tools/make_icons.py` | Favicon pipeline: SVG, ICO (16/32/48, bold variant), 96px, 180px apple-touch and maskable 192/512 |
| `tools/make_og.js` | Renders the 1200×630 `og-image.jpg` with Playwright |
| `public/` | **Build output.** This folder is what gets deployed (committed) |
| `validate.py` | Post-build checks (see below) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` with the TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # must print no ERROR lines
# fresh upload credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid GhANGdvRH)
export MIA_FB_URL=… MIA_FB_AUTH=… MIA_FB_REST=…
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid GhANGdvRH)
```

Local preview needs a router that serves real files directly, the way the host does:
`cd public && php -S 127.0.0.1:8765 ../tools/router.php`. The router returns `false` for existing non-PHP files and
otherwise requires `index.php`. You can also use `python3 -m http.server` and open `/home.html`.

Regenerate assets only when they change: `python3 tools/photos.py`, `python3 tools/make_icons.py`, `node tools/make_og.js`.
After an icon change, bump `FAV` in `build.py`. After a CSS or JS change, bump `VER`.

## Pages (51 in sitemap + 404)

- Home, `/about-us/`, `/contact-us/`
- `/what-we-appraise/` + 11 services: appraisal representation, home, condo/HOA/commercial, roof & hail,
  wind & tornado, hurricane & nor'easter, water & burst pipes, fire & smoke, **ice dam & snow load** (the
  Massachusetts-specific peril), estimate review, umpire services
- `/cities-and-towns/` + 12 cities: Boston, Worcester, Springfield, Cambridge, Lowell, Quincy, New Bedford,
  Brockton, Plymouth, Barnstable, Pittsfield, Salem
- `/estimators/` + 7 tools: award gap & fee estimator, RCV/ACV holdback calculator, roof area & pitch converter,
  hurricane deductible calculator, claim calendar builder (.ics export), appraisal file checkup and
  **roof snow load estimator** (new, Massachusetts-specific)
- `/appraisal-roadmap/` (HowTo), `/questions/` (FAQ grouped by topic), `/insurance-terms/` (searchable, 44 terms),
  `/claim-library/` + 6 guides
- `/privacy/`, `/terms/`, `/legal-disclaimer/`, `/photo-credits/`, `/site-index/` (HTML site map), `404.html`
  (real 404 status through `index.php`), `sitemap.xml`, `robots.txt`

## Design

- **Palette:** main slate `#202734`, deep shade `#12161f`, light tint `#e9edf4`, warm paper neutral `#f7f6f3`, and one
  complementary coral accent `#e07a4f` (`#b4532c` for accent text on light backgrounds).
- **Fonts:** DM Serif Display (headings) with Plus Jakarta Sans (body). No sister site uses either.
- **Homepage section order:** photo hero with a white lead-form card → counters band → intro with a photo stack →
  numbered service photo cards → "storm almanac" horizontal scroller on dark → sticky-heading roadmap that fills as you
  scroll → swipeable region photo cards → estimator cards → coral gap-check band → cities list → parallax CTA →
  comparison cards → FAQ → guides → contact.
- **Effects used:** header that turns solid on scroll (no `backdrop-filter`), hero and CTA parallax (clamped to the
  image overscan), staggered reveal, animated counters, card hover zoom, a roadmap line that fills on scroll, and a
  back-to-top button. Not used here: progress bar, 3D tilt, marquee, region tabs.
- `prefers-reduced-motion` turns motion off. Without JS, the `no-js` class stays on: reveals show, the header is solid
  and the roadmap shows fully filled.
- **Mobile:** off-canvas `#drawer` outside the header, with accordion submenus, scroll lock, and close on ×, overlay
  tap, link tap or Escape. It manages `inert` and `aria-hidden`. The shadow and visibility apply only while it is open.
  A fixed call bar sits at the bottom.
- **Logo:** a coral gable roofline with a white window over a white tide line, on a slate tile. The same inline SVG is
  used in the header, drawer and footer.

## Photos

There are 36 royalty-free photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`). Sources
are StockSnap, rawpixel, Flickr CC0/PD and WordPress Photos. Government photos come from MassDOT (the Monson tornado
damage from June 2011), USDA and USFWS. The Lanesborough/Route 7 Berkshires shot is from Flickr PD. Each photo has a
1200px (or native size, if smaller) and a 640px WebP with `srcset`/`sizes` and width/height set. Every photo is listed
on `/photo-credits/`. Decorative hero backgrounds and card images use `alt=""`, and content images have descriptive
alt text. Many Flickr originals are only available at 1024px, so heroes sit behind overlays.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown paths to `index.php`, so
  there is **no root `index.html`**. The homepage is `home.html`. `index.php` serves it for `/`, 301s directory URLs
  that lack a trailing slash, returns `404.html` with a real 404, and blocks `/api/_private/*`.
- On any host other than the final domain, `index.php` sends `X-Robots-Tag: noindex, nofollow`. Canonicals already
  point to `https://massachusettsinsuranceappraiser.com`.
- On the real domain only, `www.` and plain http get a 301 to `https://massachusettsinsuranceappraiser.com`. Every page
  also has a tiny inline script that does the same in the browser, because the host serves existing files without
  going through `index.php`.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form delivery

`/api/contact.php` has a honeypot (`website`), a per-IP rate limit (5 per 10 minutes) and server-side validation
(name, a valid email or phone, consent). It sends through `info@massachusettsinsuranceappraiser.com` with
authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, and falls back to PHP `mail()`.
It always appends a JSON line (with `"via"`) to `api/_private/leads.log.php`, which starts with
`<?php http_response_code(404); exit; ?>`.

The SMTP password is **never committed** (`_private/` is in `.gitignore`). Once the mailbox exists, upload this file
to `public_html/api/_private/config.php`:

```php
<?php
if (!defined('MIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@massachusettsinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then check that the config URL returns 404 with 0 bytes, send one submission labelled as a test, and confirm the log
shows `"via":"smtp"`.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; titles and
  descriptions unique
- Exactly one H1, the first heading is H1, and no skipped levels anywhere (footer, sidebar boxes and tools included)
- JSON-LD parses, every `@id` reference resolves, and each graph has a ProfessionalService, a WebSite and exactly one
  page node (WebPage/AboutPage/ContactPage/CollectionPage) with `primaryImageOfPage` and `mainEntity`, plus a
  `breadcrumb` on interior pages
- Canonical on the final domain; OG title/description/image/size/alt, Twitter card and `geo.region` on every page
- No broken internal links or anchors; `alt` on every image
- Homepage main content mentions "Massachusetts Insurance Appraiser" at least 14 times (currently 18; 23 in all
  visible text)
- No sister-state names anywhere in the build: Alabama, Florida, Georgia, Arizona, Missouri, Montana, Nevada,
  (North) Carolina

The JSON-LD also includes Service (services and cities), FAQPage, ItemList (index pages), WebApplication (tools),
BlogPosting (guides), HowTo (roadmap) and DefinedTermSet (glossary).

## When the domain is connected

1. Attach `massachusettsinsuranceappraiser.com` to website `GhANGdvRH` and wait for SSL to become active.
2. Check that `http://` and `www.` 301 to `https://massachusettsinsuranceappraiser.com/`, and that the real domain
   sends no `X-Robots-Tag` header.
3. Add GTM (`GTM_ID` / `GTM_HEAD_SNIPPET`) if a container is provided, and wire up SMTP once the mailbox password
   exists (see above).
4. `python3 build.py && python3 validate.py`, redeploy, and clear the cache.
5. Submit `https://massachusettsinsuranceappraiser.com/sitemap.xml` to Google Search Console.
