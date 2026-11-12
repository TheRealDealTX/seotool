# newjerseyinsuranceappraiser.com — static site

New Jersey Insurance Appraiser is a static site with no database and no plugins. A Python generator builds it, and a small PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `JMeZ7Hu3s` (Agency Growth, order 1008744732, php-fpm, PHP 8.3) |
| Domain | `newjerseyinsuranceappraiser.com`, attached when the site was created |
| Preview URL | https://ivory-viper-458822.hostingersite.com |
| Nameservers to set at the registrar | `atlas.dns-parking.com`, `hyperion.dns-parking.com` |
| Server | `us-phx-h5g-node3.hstgr.io`. Boston was requested; the order's server lives in Phoenix, the same as the sister sites |
| Google Tag Manager | `GTM_ID` in `build.py`, empty, so no snippet is output yet |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@newjerseyinsuranceappraiser.com (mailbox to be created) |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `_guard.php`, `index.php`, `GTM_ID` |
| `src/services.py` | 12 service pages |
| `src/locations.py` | 12 New Jersey location pages |
| `src/tools.py` | 7 interactive tools (markup and copy) |
| `src/learn.py` | Process guide, grouped FAQ, 40-term glossary, 6 articles |
| `src/photos.json` | Photo metadata: title, creator, license, source, size and alt text. Used by `img()` and `/photo-credits/` |
| `static/` | CSS, JS, icons, OG image, photos and `api/contact.php`, copied into `public/` as-is |
| `tools/make_icons.py` | Favicons, touch icon, maskable icons, manifest and the OG image (Pillow) |
| `tools/router.php` | Local router that mimics the host, for `php -S` |
| `public/` | **Build output**, which is what gets deployed (committed) |
| `validate.py` | Post-build checks; must report zero errors |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over the TUS file API |

## Build and deploy

```sh
python3 build.py && python3 validate.py          # must end with zero errors
# credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid JMeZ7Hu3s)
export NJA_FB_URL=… NJA_FB_AUTH=… NJA_FB_REST=…
./deploy.sh                                       # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites files. If you remove or rename a page, delete the old file on the server with `DELETE {url-without-/tus}/resources/public_html/<path>`, sending the same two auth headers.

To preview locally the way the host serves files:

```sh
php -S 127.0.0.1:8090 -t public tools/router.php
curl -sI -H 'Host: www.newjerseyinsuranceappraiser.com' http://127.0.0.1:8090/appraisal-practice/   # 301 to https://newjerseyinsuranceappraiser.com/appraisal-practice/
```

## Pages (53 in the sitemap, plus 404.html)

- Home, `/about-us/`, `/contact-us/`
- `/appraisal-practice/` plus 12 services: appraisal demand representation, homeowners, condo/HOA and commercial, roof and hail, wind and tornado, hurricane and nor’easter, water and ice dam, fire and smoke, Pinelands wildfire (the state-specific peril), fallen trees and ice storms, estimate review, and umpire services
- `/garden-state-coverage/` plus 12 cities (`/garden-state-coverage/<city>-nj/`): Newark, Jersey City, Paterson, Hackensack, Edison, Morristown, Trenton, Toms River, Long Branch, Cherry Hill, Atlantic City and Ocean City
- `/claim-toolbox/` plus 7 tools: claim gap and net recovery estimator (fees, three outcomes), ACV and holdback calculator (labor option), roof pitch and squares (tear-off layers), hurricane deductible (trigger toggle and minimum), claim calendar builder (.ics export, appraisal deadlines), appraisal readiness checkup, and the fallen tree coverage calculator (the new New Jersey tool)
- `/resource-center/` with the appraisal process guide, a grouped FAQ, a searchable glossary, and `/resource-center/articles/` with 6 articles
- `/privacy/`, `/terms/`, `/disclaimer/`, `/photo-credits/`, `/site-index/` (HTML site map), and `404.html` served with a real 404 status
- `sitemap.xml` and `robots.txt`

## Design

- Palette: amber `#FFCA66` (main), deep bronze-ink `#1F1606` / `#2A1E08` (deep shade), cream tint `#FFF6E3` (light tint), harbor blue `#1F5FA8` (complementary accent, used for links), warm neutrals `#FBF9F4`, `#EAE2D2`, `#665B47`.
- Fonts: Space Grotesk (display) and Karla (body). No sister site uses either.
- Logo: an appraisal dial (amber arc, cream needle) on deep ink. It's used in the header, drawer and footer, and in every favicon. The 16/32/48 sizes use a bolder variant.
- Layout and effects: full-bleed photo hero with parallax and a docked lead form; an amber counter strip overlapping the hero; an intro photo stack; a 12-card service grid with numbered badges and hover zoom; a horizontally scrolling storm-record track; a sticky process intro beside a vertical timeline that fills as you scroll; five region photo cards; an amber quick-check tool band; tool cards; a parallax location banner; a parallax CTA; a scroll progress bar; a header that turns solid on scroll; staggered reveals; and a back-to-top button. Interior pages use photo heroes and a two-column layout with a sticky sidebar holding a call box and related links.
- Motion respects `prefers-reduced-motion`. Without JavaScript, every section is visible: reveals only hide content once JS has set `html.js`.
- The mobile drawer (`#drawer`) sits outside the fixed header, which has no `backdrop-filter`. It has accordion submenus, scroll lock, closes on ×, scrim tap, link tap or Escape, toggles `inert`/`aria-hidden`, and gets its shadow and visibility only while open. A fixed call bar sits at the bottom on phones.

## Photos

All photos are CC0 or public domain, found through the Openverse API (`license=cc0,pdm`) from Flickr public-domain uploads (largely U.S. government agencies), rawpixel, Wikimedia Commons and StockSnap. They were downloaded one at a time with pauses and backoff, chosen from contact sheets reviewed by file label, and saved as 1200px and 640px WebP with `srcset`/`sizes` and width/height set. Images with political figures, text overlays or artwork were skipped. Each photo is listed with its license and source on `/photo-credits/`. Decorative hero backgrounds use `alt=""`.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan “force HTTPS” setting, and **serves real files directly** without running the root `index.php`. That's why there's no root `index.html` and no `dir/index.html` anywhere: a static page would skip any redirect.
- Every page is `dir/index.php`. Its first line is `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by static HTML with no other PHP. The homepage is `home.html`, served by `index.php`.
- `_guard.php` 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://newjerseyinsuranceappraiser.com`, but only on the real domain. It 301s `/dir/index.php` (and `/index.php`) to `/dir/`, sends `X-Robots-Tag: noindex, nofollow` on any other host (such as the preview URL), and returns 404 when requested directly.
- `index.php` requires the guard, serves `home.html` for `/`, 301s directory URLs that lack a trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a 404 status.
- On the preview URL, Hostinger serves its own Googlebot-blocking `robots.txt`. That's expected; ours takes over on the real domain.
- `validate.py` checks that every page starts with the guard line, that no other `<?` appears, and that no `index.html` exists.

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); meta description 110–150 characters; titles and descriptions unique
- Exactly one H1, the first heading is the H1, no skipped heading levels (footer, sidebar boxes and tools included)
- Valid JSON-LD; every `@id` reference resolves; exactly one page node (WebPage, AboutPage, ContactPage or CollectionPage) with `breadcrumb`, `primaryImageOfPage` and `mainEntity`; ProfessionalService and WebSite nodes on every page
- No broken internal links or anchors (cross-page anchors included); `alt` on every image
- Canonical, Open Graph image size and alt, Twitter card and `geo.region` on every page
- “New Jersey Insurance Appraiser” appears at least 14 times in the homepage `<main>`
- No sister-site state name anywhere in the build (AL, AZ, AR, DE, FL, GA, KY, ME, MD, MA, MO, MT, NV, NY, NC, SC, WV, WY)

Schema per page: ProfessionalService (logo ImageObject, contactPoint, `addressRegion` NJ, country, state and cities in `areaServed`, OfferCatalog of the 12 services), WebSite, one page node, BreadcrumbList, plus Service (services and locations), FAQPage, ItemList (index pages), WebApplication (tools), BlogPosting (articles), HowTo (process guide) and DefinedTermSet (glossary).

## Contact form

`/api/contact.php` has a honeypot field, a per-IP rate limit (5 per 10 minutes) and validation (name, plus a valid email or a phone number, plus consent). It sends through `info@newjerseyinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists on the server, falls back to PHP `mail()`, and always appends a JSON line to `api/_private/leads.log.php`.

Both private files return an empty 404 when requested directly: the config through its `defined()` guard, and the log through its `<?php … exit; ?>` header. They live inside `public_html` because Hostinger's file API can't write outside it. `_private/` is in `.gitignore`. **Never commit credentials.**

```php
<?php
if (!defined('NJA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@newjerseyinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Once the mailbox exists: upload that file to `public_html/api/_private/config.php` from a copy kept outside the repo (delete the local copy afterwards). Confirm `/api/_private/config.php` returns 404 with 0 bytes, send one submission labelled as a test, and confirm the newest log line shows `"via":"smtp"`.

## Going live checklist

1. Point the domain's nameservers to `atlas.dns-parking.com` and `hyperion.dns-parking.com`.
2. Confirm SSL covers both the apex and `www` (`agency-hosting_websites_get` → `ssl_cert.names`); reissue with `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check the canonical-host redirects on the home page and on interior pages, check that every sitemap URL returns 200, and check there's no `X-Robots-Tag` on the real domain.
4. Create the mailbox and wire SMTP as described above. Add the GTM ID to `GTM_ID` when available, then rebuild, validate, deploy and clear the cache.
5. Submit `https://newjerseyinsuranceappraiser.com/sitemap.xml` to Google Search Console.
