# westvirginiainsuranceappraiser.com — static site

West Virginia Insurance Appraiser: a static site with no database and no plugins. A Python
generator builds it, and a small PHP front controller serves it on a Hostinger Agency Growth website.
The engineering (generator, validator, deploy script, form handler, tool logic, photo and icon
pipelines) comes from the Georgia template. The content, URL slugs and design are new.

| | |
| --- | --- |
| Hostinger website UID | `yMnjyMKVb` (Agency Growth, order 1008744732, php-fpm 8.3, Boston datacenter) |
| Temporary URL | https://darkorange-shark-370586.hostingersite.com (sends `X-Robots-Tag: noindex`) |
| Final domain | https://westvirginiainsuranceappraiser.com (not connected yet) |
| Google Tag Manager | not set (`GTM_ID = ""` in `build.py`) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@westvirginiainsuranceappraiser.com (mailbox still to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 city pages + 7 region summaries |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, FAQ (5 topics), glossary (40 terms), 6 guides |
| `src/photo_sources.json` | Chosen Openverse photos (source URL, license, creator, landing page) |
| `src/photos.json` | Generated photo metadata (adds final width/height) used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `tools/photos.py` | Photo pipeline: download → 3:2 crop where needed → 1200px + 640px WebP |
| `tools/make_icons.py` | Logo + favicon pipeline (SVG, ICO 16/32/48 with bolder strokes, 96px PNG, 180px apple-touch, maskable 192/512) |
| `tools/make_og.js` | 1200×630 OG image rendered from a site photo with Playwright |
| `public/` | **Build output** that gets deployed (committed) |
| `validate.py` | Post-build checks; must report zero errors |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py          # zero errors required
# Credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid yMnjyMKVb); they expire after a few hours
export WVIA_FB_URL='…/api/tus' WVIA_FB_AUTH='…' WVIA_FB_REST='…'
./deploy.sh
# then clear the cache: agency-hosting_cache_clear-website (website_uid yMnjyMKVb)
```

Regenerate assets only when they change: `python3 tools/photos.py` (needs Pillow), `python3 tools/make_icons.py`,
`NODE_PATH=$(npm root -g) node tools/make_og.js`. Bump `VER` (CSS/JS) or `FAV` (icons) in `build.py` to bust caches.

Local preview that behaves like the host (real files served directly, everything else through `index.php`):
`cd public && php -S 127.0.0.1:8088 -t . router.php`, with a router that returns `false` for existing files.

## Pages (52 in sitemap + 404)

URL scheme, chosen to differ from every sister site:

- Home, `/about-the-firm/`, `/request-a-review/` (contact)
- `/wv-appraisal-services/` + 12 services: invoking-appraisal-representation, homeowners-claim-appraiser,
  commercial-hoa-claim-appraiser, roof-hail-claim-appraiser, derecho-wind-tornado-appraiser, tropical-remnant-storm-appraiser,
  water-damage-claim-appraiser, fire-smoke-claim-appraiser, **mine-subsidence-claim-appraiser** (state-specific peril),
  ice-snow-freeze-claim-appraiser, claim-estimate-review, appraisal-umpire-services
- `/west-virginia-service-areas/` + 12 cities (`<city>-wv/`): Charleston, Huntington, Morgantown, Parkersburg, Wheeling,
  Martinsburg, Fairmont, Beckley, Clarksburg, Lewisburg, Bluefield, Elkins
- `/free-appraisal-tools/` + 7 tools: claim gap & fee estimator (3 outcomes, flat/percent/hourly fees, break-even),
  RCV/ACV & holdback calculator (repair-by date), roof square & pitch estimator (compare with the carrier's squares),
  percentage deductible checker (0.5–5% ladder), claim timeline planner (.ics export), appraisal readiness scorecard,
  **mine subsidence limit calculator** (new, WV-specific)
- `/appraisal-step-by-step/` (HowTo), `/faq-by-topic/`, `/appraisal-glossary/` (searchable), `/claim-library/` + 6 guides
- `/privacy-statement/`, `/terms-and-conditions/`, `/legal-notice/`, `/photo-credits/`, `/html-sitemap/`, `404.html`, `sitemap.xml`, `robots.txt`

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; both unique
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer, sidebar and tool widgets included)
- Valid JSON-LD; every `@id` reference resolves; one page node (WebPage/AboutPage/ContactPage/CollectionPage) with
  breadcrumb, primaryImageOfPage, mainEntity and isPartOf; ProfessionalService with logo, contactPoint, address, areaServed, OfferCatalog
- Canonical = `https://westvirginiainsuranceappraiser.com/…`; OG (with image size/alt), Twitter card and `geo.region` on every page
- No broken internal links or anchors; every image has `alt`, width and height
- The homepage `<main>` mentions "West Virginia Insurance Appraiser" at least 14 times (currently 19; 24 with header/footer)
- No sister-state names anywhere in the output: Alabama, Florida, Georgia, Carolina, Arizona, Missouri, Montana, Nevada, Texas
  ("Virginia" alone can't be banned because it is part of this state's name)

Schema per page type: Service (services, cities), FAQPage, ItemList (index pages), WebApplication (tools),
BlogPosting (guides), HowTo (process), DefinedTermSet (glossary).

## Design

- **Palette:** forest green `#15370D` (main), deep `#0B1F07`, lighter greens `#235C16`/`#3F7A2E`, moss tint `#EEF3EA`,
  limestone neutral `#F6F5F0`, and a complementary rhododendron accent `#B8336A` (light `#F4A9C9` on dark backgrounds).
  The rhododendron is the state flower.
- **Fonts:** Zilla Slab (display) + Public Sans (body). No sister site uses either.
- **Mark:** a cream ridgeline over a pink level line, with a pink sun, on a green tile. The same SVG is used in the header, drawer and footer.
- **Layout:** full-bleed New River Gorge hero with a slow Ken Burns zoom and a solid lead-form card; an overlapping
  counter band; photo cards (hover zoom) for services, tools, regions, cities and guides; a horizontally scrolling
  storm-history carousel; a horizontal process timeline that fills on scroll (it turns vertical on mobile); a
  "can / can't decide" panel; a parallax CTA; a ridgeline footer.
- **Interior pages:** photo heroes and a two-column layout with a sticky sidebar (call box + related links).
- **Behaviour:** the header goes from transparent to solid on scroll (no `backdrop-filter`); reveals are staggered;
  there is a back-to-top button; all motion respects `prefers-reduced-motion`; content is fully visible without JavaScript.
- **Mobile nav:** an off-canvas drawer outside the fixed header, with accordion submenus, scroll lock and
  `inert`/`aria-hidden` handling. It closes on ×, overlay tap, link tap or Escape, and its shadow and visibility apply only while open.
  A fixed call bar sits at the bottom.

## Photos

35 photos, all CC0 or public domain, found with the Openverse API (`license=cc0,pdm`): rawpixel, StockSnap, Flickr
(including U.S. government public-domain photos), WordPress Photo Directory and Wikimedia Commons. They were reviewed on
contact sheets by file label. Photos with political figures, text overlays or artwork were skipped. Each photo is
served as 1200px-max and 640px WebP with `srcset`/`sizes` and width/height set. Content images have descriptive alt
text; decorative backgrounds and card images use `alt=""`. Every photo is listed with its license and source on
`/photo-credits/`. Wikimedia rate-limits originals, so the pipeline fetches their 1280px thumbnails.

## Hosting notes

- The host ignores `.htaccess`, serves real files directly and sends `/` and unknown paths to `index.php`. **Don't add a root `index.html`.**
- `index.php` serves `home.html` for `/`, 301s directory URLs to add a trailing slash, returns `404.html` with a
  real 404, sends `X-Robots-Tag: noindex, nofollow` on any host other than the domain, and only on the real domain
  301s `www.` and plain http (checked through `X-Forwarded-Proto`) to `https://westvirginiainsuranceappraiser.com`.
- Hostinger's placeholder `public_html/default.php` was deleted after the first deploy.

## Contact form

`/api/contact.php` has a honeypot field, a per-IP limit (5 per 10 minutes) and validation (name, plus a valid email
or a phone number, plus consent). It sends through `info@westvirginiainsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a
JSON line to `api/_private/leads.log.php`, whose `<?php … exit;` header makes direct requests return an empty 404.

Credentials are **never committed** (`_private/` is in `.gitignore`). The Hostinger file API can't write outside
`public_html`, so once the mailbox exists, upload this file to `public_html/api/_private/config.php`:

```php
<?php
if (!defined('WVIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@westvirginiainsuranceappraiser.com', 'smtp_pass' => '…'];
```

Then confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and check
that the log line shows `"via":"smtp"`.

## Google Tag Manager

Set `GTM_ID` in `build.py`. If the owner supplies a full head snippet, paste it into `GTM_HEAD_SNIPPET` exactly as
given. The head snippet and the `<noscript>` iframe after `<body>` are then output on every page. Rebuild, validate and deploy.

## Going live checklist

1. Attach `westvirginiainsuranceappraiser.com` to website `yMnjyMKVb` and wait for SSL.
2. Check that www and http 301 to `https://westvirginiainsuranceappraiser.com` and that the real domain has no `X-Robots-Tag` header.
3. Add GTM if provided; create the mailbox and wire SMTP as described above.
4. `python3 build.py && python3 validate.py`, deploy, clear the cache.
5. Submit `https://westvirginiainsuranceappraiser.com/sitemap.xml` to Google Search Console.
