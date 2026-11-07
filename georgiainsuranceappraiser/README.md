# georgiainsuranceappraiser.com — static site

Georgia Insurance Appraiser: a static site with no database and no plugins. It is built
by a Python generator and served by a tiny PHP front controller on a Hostinger Agency
Growth website.

| | |
| --- | --- |
| Hostinger website UID | `NtH7QOTDM` (Agency Growth, order 1008744732, php-fpm 8.3) |
| Temporary URL | https://snow-chinchilla-788360.hostingersite.com |
| Final domain | georgiainsuranceappraiser.com (not connected yet) |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@georgiainsuranceappraiser.com |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `index.php` |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Georgia location pages |
| `src/tools.py` | 6 interactive tools (markup + copy) |
| `src/learn.py` | Process guide, FAQ, glossary, 5 insight posts |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `src/photos.json` | Photo metadata (title, creator, license, source URL, size) used for `img()` and `/photo-credits/` |
| `public/` | **Build output.** This folder is what gets deployed (committed) |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads `public/` to the website's `public_html` |

## Build & deploy

```sh
python3 build.py && python3 validate.py
# get creds from the Hostinger API: agency-hosting_files_generate-upload-url (website_uid NtH7QOTDM)
export GIA_FB_URL=… GIA_FB_AUTH=… GIA_FB_REST=…
./deploy.sh        # then clear cache: agency-hosting_cache_clear-website
```

Local preview: `cd public && php -S localhost:8000` (or `python3 -m http.server` and open `/home.html`).

## Pages (48 in sitemap)

- Home, About, Contact
- `/appraisal-services/` + 11 services
- `/locations/` + 12 cities (`/locations/<city>-ga/`)
- `/claim-tools/` + 6 tools: appraisal value estimator, depreciation & holdback,
  roof squares & pitch, wind/hail deductible, claim deadline planner (.ics export),
  appraisal readiness score
- `/how-appraisal-works/`, `/appraisal-faq/`, `/claim-glossary/`, `/insights/` + 5 posts
- Privacy, Terms, Disclaimer, HTML site map, 404

The URL scheme, copy and design differ from the sister Alabama site on purpose.
`validate.py` fails the build if the word "Alabama" appears anywhere. It also checks
that the homepage's main content mentions "Georgia Insurance Appraiser" at least 14 times
(currently 18, or 22 counting the header and footer). It checks for broken links, one H1
per page, valid JSON-LD, and unique titles and descriptions.

## Design

Maroon base (`#7a1d33`, deep `#2b0b14`) with warm gold (`#e3a94f`) and blush accents;
Outfit headings, Inter body. Photo-led: full-bleed hero with slow zoom and a glass lead form,
animated stat counters, a bento grid of service photo cards, a scroll-filled process
timeline, region tabs with photos, 3D-tilt tool cards, parallax banners, scroll progress bar,
staggered reveal animations and a header that goes from transparent to frosted on scroll.
All motion respects `prefers-reduced-motion`.

Mobile nav is an off-canvas drawer (`#drawer`) rendered *outside* the sticky header, with
accordion submenus, scroll lock, and close on ×, overlay tap, link tap or Escape.

## Photos

All 30 photos are royalty-free: CC0 (StockSnap, rawpixel, Flickr CC0) or public domain
(U.S. government agency photos), found through the Openverse API. Each is served as
1200px and 640px WebP in `static/assets/img/photos/`. Sources and creators are listed on
`/photo-credits/` (attribution isn't required, but it's included). The StockSnap originals
are limited to 960px wide via their CDN, so hero images sit behind overlays.

## Hosting notes

- The host ignores `.htaccess`. It serves real files directly and sends `/` and unknown
  paths to `index.php`. That file serves `home.html` for `/`, returns a real 404 otherwise,
  and adds a trailing slash to directory URLs. Don't add a root `index.html`.
- While the site runs on the temporary `*.hostingersite.com` domain, `index.php` sends
  `X-Robots-Tag: noindex`. Canonical tags already point to the final domain.
- Once the domain is connected, `index.php` 301-redirects `www.` and plain http to
  `https://georgiainsuranceappraiser.com`.

## Going live checklist

1. Attach georgiainsuranceappraiser.com to website `NtH7QOTDM` in hPanel and wait for SSL.
2. Create the mailbox info@georgiainsuranceappraiser.com. The form at `/api/contact.php`
   sends to it with PHP `mail()`. It also keeps a JSON-lines backup at `../gia-leads.log`,
   outside `public_html`.
3. Submit `https://georgiainsuranceappraiser.com/sitemap.xml` to Google Search Console.
