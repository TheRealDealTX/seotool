# illinoisinsuranceappraiser.com — static site

Illinois Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a small
PHP front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `uJ2yGXv1l` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, created in the Boston datacenter) |
| Domain | `illinoisinsuranceappraiser.com` (attached at creation; waiting on nameservers) |
| Preview URL | https://linen-armadillo-842275.hostingersite.com (serves `X-Robots-Tag: noindex`; Hostinger's own robots.txt blocks Googlebot there) |
| Nameservers to set at the registrar | `aurora.dns-parking.com`, `nebula.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@illinoisinsuranceappraiser.com (mailbox not created yet) |
| Google Tag Manager | none yet: set `GTM_ID` in `build.py` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, schema, sitemap, `_guard.php`, `index.php`, Search Console file |
| `src/services.py` | 11 service pages |
| `src/locations.py` | 12 Illinois city pages |
| `src/tools.py` | 7 interactive tools (markup and copy). The math lives in `static/assets/js/app.js` |
| `src/learn.py` | Process guide, grouped FAQ, 39-term glossary, 6 articles |
| `src/photos.json` | Internal photo manifest: source URL, license, creator, size. **Not published** |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` as-is |
| `tools/make_icons.py` | Regenerates favicons, app icons, `site.webmanifest` and the OG image (uses `tools/fonts/`, OFL) |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks (must report zero errors) |
| `deploy.sh` | Uploads `public/` to the website's `public_html` over TUS |

## Build and deploy

```sh
python3 build.py && python3 validate.py
# fresh credentials: Hostinger API agency-hosting_files_generate-upload-url (website_uid uJ2yGXv1l)
export IIA_FB_URL=… IIA_FB_AUTH=… IIA_FB_REST=…
./deploy.sh        # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites. If a page is removed or renamed, delete the old file on the server:
`DELETE {url-without-/tus}/resources/public_html/<path>` with the same `X-Auth` and `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` was deleted on first deploy.

To preview locally the way the host serves files, run PHP's built-in server with a router script that serves real
files directly, executes a directory's `index.php`, and sends everything else to `/index.php`.

## Pages (50 in sitemap.xml, plus the 404)

| Section | URL |
| --- | --- |
| Home, About, Contact | `/`, `/about-the-firm/`, `/contact-an-appraiser/` |
| Services (index + 11) | `/appraiser-services/…` |
| Cities (index + 12) | `/cities-we-serve/<city>-il/`: Chicago, Aurora, Naperville, Joliet, Rockford, Springfield, Peoria, Champaign, Bloomington–Normal, Elgin, Belleville, Carbondale |
| Tools (index + 7) | `/calculators-and-planners/…`: disputed amount and net recovery estimator, recoverable depreciation planner, pitch-adjusted roof squares, deductible dollars converter, Illinois claim deadline calendar (.ics), appraisal file strength score, **sewer backup endorsement gap checker** (Illinois-specific) |
| Resources | `/illinois-appraisal-process/`, `/appraisal-questions/`, `/insurance-claim-terms/`, `/policyholder-articles/` + 6 articles |
| Legal / navigation | `/privacy-statement/`, `/terms-and-conditions/`, `/important-disclaimer/`, `/all-pages/`, `404.html` (real 404 status) |

There is no Photo Credits page and nothing links to one. Every URL slug was checked against all sister-site slugs
so none repeat.

## Design

- **Palette:** main `#FF5F0F`; deep burnt umber `#2B1105`; light peach tint `#FFF1E8`; complementary cerulean accent
  `#0A74A8`; warm neutrals (`#1F1A17` ink, `#645A53` muted, `#EBE0D7` lines, `#F8F4F0` stone). `#B83D00` is the
  text-safe orange for links on white. Buttons use dark text on orange for contrast.
- **Fonts:** Big Shoulders Display (uppercase display, designed for Chicago) + DM Sans body. No sister site uses either.
- **Layout:** full-bleed Chicago lakefront hero with a lead form, a stat strip overlapping the hero with counters,
  photo service cards, a horizontal five-step process line that fills as you scroll (vertical on mobile), a
  horizontally scrolling row of five Illinois region cards, an Illinois storm-record timeline, a city grid, role
  comparison cards, FAQ, articles, a parallax CTA and a contact section. Interior pages use photo heroes and a
  two-column layout with a sticky sidebar (call box plus related links).
- **Effects:** header turns solid on scroll, hero and banner parallax (clamped to the image's overscan), staggered
  reveal, counters, hover zoom on cards, scroll-filled process line, a back-to-top button with a scroll-progress
  ring, and the parallax CTA. No marquee, tilt, region tabs or top progress bar. All motion respects
  `prefers-reduced-motion`, and the page renders fully without JavaScript (reveals only hide when `html.js` is set).
- **Mobile:** off-canvas drawer outside the sticky header, with accordion submenus, scroll lock, closing with ×,
  overlay tap, link tap or Escape, `inert`/`aria-hidden` state, and shadow/visibility applied only while it's open.
  A fixed call bar sits at the bottom.
- **Logo:** an orange rounded square with a white roofline and two umber "estimate" bars. `favicon.svg`, a 16/32/48
  `favicon.ico` drawn from a bolder variant, a 96px PNG, a full-bleed 180px `apple-touch-icon.png`, and maskable
  192/512 PNGs in `site.webmanifest`. Every icon link carries `?v=1`. The OG image (1200×630 JPG) uses the
  lakefront photo.

## Hosting notes

- The host ignores `.htaccess`, has no Agency-plan "force HTTPS" setting, and **serves real files directly without
  running the root `index.php`**. A `dir/index.html` would skip any redirect, so `http://www.…/page/` would load
  with a 200.
- That's why every page except the homepage is written as `dir/index.php`, whose first line is
  `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>` followed by static HTML with no other PHP.
  `validate.py` enforces this and fails if any `dir/index.html` or root `index.html` exists.
- `_guard.php`: on the real domain only, 301s `www.` and plain http (from `X-Forwarded-Proto`, falling back to
  `HTTPS`) to `https://illinoisinsuranceappraiser.com`. On any host, it 301s `/dir/index.php` (and `/index.php`)
  to the directory, sends `X-Robots-Tag: noindex, nofollow` on any host that isn't the real domain, and returns 404
  if requested directly.
- `index.php` (front controller) requires the guard, serves `home.html` for `/`, 301s directory URLs to add the
  trailing slash, includes `dir/index.php` for directory URLs that reach it, and returns `404.html` with a real 404.
- The only static `.html` files at the root are `home.html`, `404.html` and the Search Console file.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html` at the site root.
- Exact contents (one line, no trailing newline, no HTML, guard, GTM or BOM):
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `build.py` writes it from the `GSC_FILE`/`GSC_BODY` constants on every build, so a rebuild never drops it.
  `validate.py` checks the bytes and keeps it out of page checks; it isn't in `sitemap.xml`, the HTML site map,
  internal links or `robots.txt`.
- It must stay at the root permanently: Google rechecks it, and removing it unverifies the property. It's a real
  file, so the host serves it directly and the guard doesn't run for it. That's expected.
- Verification works only for the **URL-prefix** property `https://illinoisinsuranceappraiser.com/`.

## Photos (internal record — not published)

All 35 photos are **CC0 1.0** (StockSnap, rawpixel, Wikimedia Commons CC0 uploads), found through the Openverse API
with `license=cc0,pdm`. No attribution is required, so the site has no credits page. Each photo is served as
1200px (StockSnap/rawpixel cap at about 1000px) and 640px WebP with `srcset`, `sizes` and width/height. Decorative
backgrounds use `alt=""`. Some photos were taken outside Illinois (for example the stone bridge, the brick depot and
the storm-damage photos). Their alt text stays generic and never claims an Illinois location.

| Key | Source | License | Creator | Landing page |
| --- | --- | --- | --- | --- |
| `chicago-lakefront-aerial` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5906687/photo-image-public-domain-free-city |
| `chicago-skyline-night` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5926982/photo-image-public-domain-free-city |
| `chicago-towers-park` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5925111/photo-image-public-domain-free-city |
| `chicago-night-aerial` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5926732/photo-image-public-domain-free-city |
| `chicago-loop-street` | stocksnap | CC0 1.0 | Sawyer Bengtson | https://stocksnap.io/photo/chicago-architecture-ZY7FE8SBKU |
| `springfield-capitol` | rawpixel | CC0 1.0 | Carol M Highsmith | https://www.rawpixel.com/image/3094243/free-photo-image-america-architecture-blue-sky |
| `peoria-brick-building` | rawpixel | CC0 1.0 | libraryofcongress | https://www.rawpixel.com/image/3800180/photo-image-vintage-retro-building |
| `illinois-cornfield` | stocksnap | CC0 1.0 | Skitter Photo | https://stocksnap.io/photo/cornfields-farming-420322FE63 |
| `fire-gutted-house` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/7433149/photo-image-public-domain-city |
| `shingle-rows` | stocksnap | CC0 1.0 | Bernard Spragg | https://stocksnap.io/photo/roof-shingle-RIUJONCXNY |
| `storm-cloud-mono` | stocksnap | CC0 1.0 | Daniel Páscoa | https://stocksnap.io/photo/dark-clouds-5AQVUNY6O4 |
| `snowy-suburban-home` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5913696/image-public-domain-house-interior |
| `craftsman-bungalow` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/6023013/photo-image-public-domain-house-free |
| `brick-two-story` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/6040724/photo-image-public-domain-house-home |
| `suburban-street` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/6026000/photo-image-public-domain-house-home |
| `team-meeting` | stocksnap | CC0 1.0 | Startup Stock Photos | https://stocksnap.io/photo/team-meeting-69TMH4ITIE |
| `signing-paperwork` | stocksnap | CC0 1.0 | Matt Moloney | https://stocksnap.io/photo/paperwork-desk-A5DG6YREVH |
| `calculator-charts` | stocksnap | CC0 1.0 | Negative Space | https://stocksnap.io/photo/calculator-numbers-Y2GUBQIPXD |
| `calculator-sticky-note` | stocksnap | CC0 1.0 | Martin Vorel | https://stocksnap.io/photo/calculator-numbers-JY874BSKKC |
| `contractors-plans` | stocksnap | CC0 1.0 | Burst | https://stocksnap.io/photo/construction-blueprint-BZ4FJO6KZE |
| `conference-room` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/5969848/meeting-table-office |
| `tornado-debris-field` | wikimedia | CC0 1.0 | NWS Tulsa, OK | https://commons.wikimedia.org/w/index.php?curid=148240293 |
| `flooded-basement` | wikimedia | CC0 1.0 | B137 | https://commons.wikimedia.org/w/index.php?curid=61270024 |
| `joliet-victorian` | wikimedia | CC0 1.0 | Smallbones | https://commons.wikimedia.org/w/index.php?curid=15224975 |
| `belleville-depot` | wikimedia | CC0 1.0 | TheCatalyst31 | https://commons.wikimedia.org/w/index.php?curid=63729907 |
| `frozen-pipes` | wikimedia | CC0 1.0 | Jidanni | https://commons.wikimedia.org/w/index.php?curid=157554068 |
| `prairie-supercell` | wikimedia | CC0 1.0 | Šime Barešić | https://commons.wikimedia.org/w/index.php?curid=157426479 |
| `roofers-at-work` | wikimedia | CC0 1.0 | Daniel Moskowitz from Denver, USA | https://commons.wikimedia.org/w/index.php?curid=105046310 |
| `illinois-river-bridge` | wikimedia | CC0 1.0 | Brandonrush | https://commons.wikimedia.org/w/index.php?curid=150096506 |
| `wind-torn-house` | wikimedia | CC0 1.0 | Johnson524 | https://commons.wikimedia.org/w/index.php?curid=151309862 |
| `brick-apartments` | wikimedia | CC0 1.0 | TheCatalyst31 | https://commons.wikimedia.org/w/index.php?curid=65129239 |
| `campus-brick-hall` | wikimedia | CC0 1.0 | Daderot | https://commons.wikimedia.org/w/index.php?curid=50399739 |
| `chicago-river-west` | wikimedia | CC0 1.0 | Ikmckenz | https://commons.wikimedia.org/w/index.php?curid=80039113 |
| `storm-wreckage` | wikimedia | CC0 1.0 | National Oceanic and Atmospheric Administration | https://commons.wikimedia.org/w/index.php?curid=149764160 |
| `snow-cabin` | rawpixel | CC0 1.0 | unknown | https://www.rawpixel.com/image/3296963/free-photo-image-blizzard-building-cabin |

## SEO rules enforced by validate.py

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); unique titles
- Hand-written meta description on every page, **110–143 characters** (under 144), ending in a full sentence, unique;
  `og:description` and `twitter:description` must match it exactly
- Exactly one H1, the first heading is the H1, and no skipped heading levels (footer, sidebar and tools included)
- Valid JSON-LD with ProfessionalService (logo, contact point, IL address region, state + cities served, offer
  catalog), WebSite and exactly one page node (WebPage, AboutPage, ContactPage or CollectionPage) with breadcrumb,
  primaryImageOfPage and mainEntity. Every `@id` reference must resolve. Service, FAQPage, ItemList,
  WebApplication, BlogPosting, HowTo and DefinedTermSet appear where they apply
- No broken internal links or anchors, `alt` on every image, canonical on the real domain
- Homepage main content mentions "Illinois Insurance Appraiser" at least 14 times (currently 18)
- No sister-state names (all 27 other `*insuranceappraiser*` states) anywhere in the build
- Guard line on every `dir/index.php`, no other PHP, no `dir/index.html`, Search Console file byte-exact

## Contact form

`/api/contact.php` has a honeypot, a per-IP limit (5 per 10 minutes) and validation (name, valid email or phone,
consent). It sends through `info@illinoisinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`)
when `api/_private/config.php` exists, falls back to PHP `mail()`, and always appends a JSON line to
`api/_private/leads.log.php`. Both private files return 404 when requested directly: the config through its
defined-constant guard, the log through its `<?php http_response_code(404); exit; ?>` header. They sit inside
`public_html` because Hostinger's file API can't write outside it. `_private/` is in `.gitignore`. **Never commit
credentials.** Keep any local copy of the config outside the repo, and delete it once it's uploaded.

```php
<?php
if (!defined('IIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@illinoisinsuranceappraiser.com', 'smtp_pass' => '…'];
```

Once the mailbox exists: upload the config, confirm `/api/_private/config.php` returns 404 with 0 bytes, send one
submission labelled as a test, and confirm the log shows `"via":"smtp"`.

## Go-live checklist

1. Point the domain's nameservers to `aurora.dns-parking.com` / `nebula.dns-parking.com`.
2. Confirm SSL covers both `illinoisinsuranceappraiser.com` and `www.` (`ssl_cert.names`); reissue with
   `agency-hosting_ssl_reinstall-website` if `www` is missing.
3. Check the redirects on the live domain (http, www and https-www → `https://illinoisinsuranceappraiser.com/page/`;
   `/page/index.php` → `/page/`), that every sitemap URL returns 200 with no `X-Robots-Tag`, and that the
   Search Console file returns 200 with exact bytes. If a www URL returns 200 with `x-hcdn-cache-status: HIT`,
   clear the cache again.
4. Add GTM (set `GTM_ID`) and wire SMTP, rebuild, run validate, redeploy, clear cache.
5. In Search Console, click **Verify** on the URL-prefix property, then submit `https://illinoisinsuranceappraiser.com/sitemap.xml`.
