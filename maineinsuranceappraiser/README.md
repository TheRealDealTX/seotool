# maineinsuranceappraiser.com — static site

Maine Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it,
and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `4QdxBSl4j` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, created in the Boston datacenter; the order's server is `us-phx-h5g-node3.hstgr.io`) |
| Domain | https://maineinsuranceappraiser.com (attached at creation) |
| Preview URL | https://linen-weasel-655539.hostingersite.com (Hostinger serves its own Googlebot-blocking `robots.txt` here; our guard also sends `X-Robots-Tag: noindex, nofollow` on every non-canonical host) |
| Nameservers to set at the registrar | `orbit.dns-parking.com` and `horizon.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@maineinsuranceappraiser.com (mailbox to be created) |
| Google Tag Manager | none yet. Set `GTM_ID` in `build.py` to output the head snippet and the `<noscript>` iframe after `<body>` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `_guard.php`, `index.php` |
| `src/services.py` | 12 service pages (`/appraisal-work/…`) |
| `src/locations.py` | 12 town pages (`/towns-we-cover/<town>-maine/`) |
| `src/tools.py` | 7 interactive tools: markup and copy (`/claim-math/…`) |
| `src/learn.py` | Process guide, grouped FAQ, glossary, 6 owner guides |
| `src/photos.json` | Photo metadata (title, creator, license, source, alt, size), used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`. Copied into `public/` as is |
| `public/` | **Build output.** This folder is what gets deployed (committed) |
| `validate.py` | Post-build checks; must exit 0 |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# Fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid 4QdxBSl4j)
export MIA_FB_URL=… MIA_FB_AUTH=… MIA_FB_REST=…
./deploy.sh
# then: agency-hosting_cache_clear-website (website_uid 4QdxBSl4j)
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.

Local preview that mimics the host (real files served directly, a directory's `index.php` executed, everything
else to the front controller): see the router in "Hosting notes", or simply `cd public && php -S localhost:8000`.

## Pages (52 in the sitemap, plus the 404)

- Home, `/our-approach/` (about), `/reach-us/` (contact)
- `/appraisal-work/` + 12 services: appraisal clause representation, homeowner, commercial/condo/HOA,
  roof & hail, windstorm & microburst, nor’easter & hurricane, water damage, fire/smoke/puffback,
  **ice dam & snow load** (the Maine-specific peril), fallen tree, estimate review, umpire services
- `/towns-we-cover/` + 12 towns: Portland, Lewiston, Bangor, Augusta, Biddeford, Brunswick, Scarborough,
  Waterville, Rockland, Bar Harbor, Presque Isle, Sanford. Each has county, neighborhoods, housing mix,
  storm record, local copy and FAQs
- `/claim-math/` + 7 tools (all in the browser, nothing stored): settlement gap projector (fees and three
  award scenarios), RCV/ACV holdback calculator, roof pitch & squares converter (with ice-barrier courses),
  percentage deductible checker, claim date tracker (.ics export), appraisal file strength test, and the
  Maine-specific **seasonal camp vacancy check**
- `/the-appraisal-path/` (HowTo), `/answers/` (25 FAQs in 5 groups), `/plain-english-glossary/` (41 terms,
  searchable), `/owner-guides/` + 6 guides
- `/privacy-practices/`, `/site-terms/`, `/fine-print/` (disclaimer), `/photo-credits/`, `/page-directory/`
  (HTML site map), `404.html` (served with a real 404 status), `sitemap.xml`, `robots.txt`

URL slugs, section order, headings, palette, fonts and copy were chosen to differ from all eleven sister
sites (AL, FL, GA, AZ, MO, MT, NV, NC, WY, WV, MA). `validate.py` fails the build if any of those state
names appears in any built file.

## Design

Navy `#133458` base, deep `#0a1d33`, light tint `#e6eef7`, one complementary coral accent `#e2683c`
(dark `#b9481f`), fog `#f6f4ef` and slate neutrals. Fonts: **Archivo** (expanded width, 600–800) for display,
**Onest** for body. The mark is a white gable roof over two coral swells on a navy tile.

Layout and effects: full-bleed photo hero with a docked lead form; a "ledger" intro with animated counters;
photo service cards with hover zoom; expanding season panels (the Maine claim year); a sticky, stacking
five-step process; a scroll-snap region rail; tool, town and guide cards; a storm-record list; a parallax
CTA; staggered reveals; a header that turns solid navy on scroll; back-to-top. All motion respects
`prefers-reduced-motion`, and content is visible without JavaScript (reveals only hide when JS adds the `js` class).
Interior pages use a photo hero and a two-column layout with a sticky sidebar (call box + related links).

The header has **no** `backdrop-filter`. The mobile drawer sits outside the header, slides in from the left,
has accordion submenus, scroll lock, `inert`/`aria-hidden` handling, and closes on ×, overlay tap, link tap
or Escape. Its shadow and visibility apply only while open. Without JS, the burger is a `#drawer` link and the
drawer opens with `:target`. A fixed call bar shows on phones. The brand link never changes color on hover.

## Photos

All photos are CC0 or public domain, found through the Openverse API (`license=cc0,pdm`) and downloaded one
at a time with pauses and backoff (Wikimedia files via standard thumbnail widths: 330px for contact sheets,
1280px for finals). Contact sheets were reviewed by file label. Each photo is saved as WebP at up to 1200px and
at 640px in `static/assets/img/photos/`, used with `srcset`/`sizes`, width/height and descriptive alt text
(decorative backgrounds use `alt=""`). Every photo's title, creator, license and source link is on `/photo-credits/`.
Some Flickr sources top out at 1024px wide; those are served at their native width rather than upscaled.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly**
  (running a directory's `index.php`) without passing through the root `index.php`. `/` and unknown paths go
  to the root `index.php`.
- So every page is written as `dir/index.php` whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML (no other PHP). The
  homepage is `home.html`, read by the front controller. There is **no root `index.html` and never a
  `dir/index.html`**: the host would serve it directly and skip the guard (`validate.py` fails if one exists).
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to
  `https://maineinsuranceappraiser.com` on the real domain only; 301s `/dir/index.php` and `/index.php` to the
  directory; sends `X-Robots-Tag: noindex, nofollow` on any other host; and 404s if requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, 301s directory URLs to add the trailing slash,
  includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- The server also holds `api/_private/` (SMTP config and lead log). It is not in git. Leave it in place.

## Contact form

`/api/contact.php`: honeypot field, per-IP rate limit (5 per 10 minutes), validation (name, consent, and a
valid email or phone). It sends through `info@maineinsuranceappraiser.com` over authenticated SMTP
(`smtp.hostinger.com:465`) when `api/_private/config.php` exists, falls back to PHP `mail()`, and always
appends a JSON line to `api/_private/leads.log.php` (`"via":"smtp"` when SMTP delivered it).

The password is **never committed** (`_private/` is in `.gitignore`). Upload this file to
`public_html/api/_private/config.php`; it returns 404 with an empty body when requested directly, and so
does the log (its first line is `<?php http_response_code(404); exit; ?>`):

```php
<?php
if (!defined('MIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@maineinsuranceappraiser.com', 'smtp_pass' => '…'];
```

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters;
  titles and descriptions unique
- Exactly one H1, the first heading is the H1, no skipped heading levels anywhere (footer, sidebar, tools included)
- Valid JSON-LD; every `@id` reference resolves; each page has ProfessionalService, WebSite, BreadcrumbList and
  one page node (WebPage, AboutPage, ContactPage or CollectionPage)
- Canonical = `https://maineinsuranceappraiser.com/<path>`; Open Graph (with image size and alt), Twitter card
  and `geo.region` present
- No broken internal links or anchors; every image has `alt`
- Homepage main content mentions "Maine Insurance Appraiser" at least 14 times
- No sister-state names; every `dir/index.php` starts with the guard line and has no other PHP

Each page's JSON-LD `@graph` holds the ProfessionalService (logo ImageObject, contactPoint, `addressRegion` ME,
country, Maine + towns as `areaServed`, OfferCatalog of the services), the WebSite, and one page node linked to its
BreadcrumbList, `primaryImageOfPage` and `mainEntity`. Service (services and towns), FAQPage, ItemList (index pages),
WebApplication (tools), BlogPosting (guides), HowTo (process) and DefinedTermSet (glossary) are added where they apply.

## Going live checklist

1. Point the domain's nameservers to `orbit.dns-parking.com` / `horizon.dns-parking.com`.
2. Confirm SSL covers both `maineinsuranceappraiser.com` and `www.` and that www/http 301 to the canonical host.
3. Create the mailbox, then upload `api/_private/config.php` and send one labelled test lead.
4. Add GTM when the container ID is ready (`GTM_ID` in `build.py`), rebuild, deploy, clear cache.
5. Submit `https://maineinsuranceappraiser.com/sitemap.xml` in Google Search Console.
