# hawaiiinsuranceappraiser.com — static site

Hawaii Insurance Appraiser: a static site with no database and no plugins. A Python generator builds it, and a small PHP
front controller plus a canonical-host guard serve it on a Hostinger Agency Growth website.

| | |
| --- | --- |
| Hostinger website UID | `664HJBPMN` (Agency Growth, order 1008744732, php-fpm, PHP 8.3, Phoenix datacenter) |
| Domain | https://hawaiiinsuranceappraiser.com (attached at creation; waiting for nameservers) |
| Preview URL | https://carefree-brown-shrew-19.hostingersite.com |
| Nameservers to set at the registrar | `orbit.dns-parking.com`, `horizon.dns-parking.com` |
| Phone | +1 (844) 537-1427 |
| Email / form inbox | info@hawaiiinsuranceappraiser.com (mailbox still to be created) |
| Google Tag Manager | none yet — set `GTM_ID` in `build.py` |

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, homepage, page templates, JSON-LD, sitemap, `index.php`, `_guard.php`, Search Console file |
| `src/services.py` | 12 appraisal specialties |
| `src/locations.py` | 12 island community pages |
| `src/tools.py` | 7 interactive tools (markup + copy) |
| `src/learn.py` | Process map, FAQ by topic, glossary (47 terms), 5 claim guides |
| `src/photos.json` | Internal photo manifest: source URL, license, creator, size, alt text. **Not published** |
| `static/` | CSS, JS, icons, OG image, photos, `api/contact.php`. Copied into `public/` unchanged |
| `tools/make_icons.py` | Regenerates favicon.svg/.ico, PNG and maskable icons, `site.webmanifest` and the OG image |
| `public/` | **Build output** (committed). This is what gets deployed |
| `validate.py` | Post-build checks. Must report `OK` (zero errors) |
| `deploy.sh` | Uploads `public/` to `public_html` through the TUS file API |

## Build & deploy

```sh
python3 tools/make_icons.py   # only when the mark or hero photo changes
python3 build.py && python3 validate.py
# creds: Hostinger API agency-hosting_files_generate-upload-url (website_uid 664HJBPMN); they expire after a few hours
export HIA_FB_URL='…/api/tus' HIA_FB_AUTH='…' HIA_FB_REST='…'
./deploy.sh                   # then agency-hosting_cache_clear-website
```

`deploy.sh` only adds and overwrites files. If you remove or rename a page, delete the old file on the server with
`DELETE {url-without-/tus}/resources/public_html/<path>`, sending the same `X-Auth` and `X-Auth-Rest` headers.
Hostinger's placeholder `public_html/default.php` has already been deleted.

Local preview: `cd public && php -S 127.0.0.1:8123 ../tools/router.php`, using a router that mimics the host. Real files are served as-is,
a directory's `index.php` is executed, and everything else goes to the root `index.php`.

## Pages (50 in sitemap, plus the 404)

The URL scheme is deliberately unlike every sister site's:
- Home, `/about-hawaii-appraiser/`, `/contact-hawaii-appraiser/`
- `/appraisal-specialties/` plus 12 specialties: appraisal clause, homeowner, condo/AOAO/commercial, roof & hail,
  Kona storm & high wind, hurricane, water, fire & smoke, wildfire, volcanic/ash/lava, carrier estimate review, umpire
- `/island-communities/` plus 12 communities: Honolulu, Kailua & Kaneohe, Pearl City & Aiea, Kapolei & Ewa Beach, Mililani & Wahiawa,
  Hilo, Kailua-Kona, Puna & Pahoa, Kahului & Wailuku, Kihei & Wailea, Lahaina & West Maui, Lihue & Kapaa
- `/island-claim-tools/` plus 7 tools: claim gap & fee estimator, RCV/ACV holdback, roof pitch & squares (shingle or metal),
  hurricane deductible, claim timeline builder (.ics export), appraisal readiness check, and a condo deductible share calculator (AOAO + HO-6)
- `/appraisal-process-map/` (HowTo), `/appraisal-questions-by-topic/`, `/property-claim-glossary/` (searchable),
  `/hawaii-claim-guides/` plus 5 guides
- `/privacy-and-your-data/`, `/terms-of-site-use/`, `/appraisal-and-legal-disclaimer/`, `/island-site-map/`, `404.html` (real 404 status)
- There is **no photo-credits page**, and nothing links to one.

## Design

- **Palette:** brand purple `#6B3FA0`, with a deep shade `#2A1442` and ink `#1A0B2C`.
  - The light tints are `#F3EEFA` and `#E6DCF3`.
  - The accent is plumeria gold `#F2B544`, roughly complementary to the purple.
  - Neutrals are `#1E1A24` (ink), `#686174` (muted) and `#E4DFEA` (lines).
- **Fonts:** Instrument Serif for display and Kumbh Sans for body text. No sister site uses either font.
- **Homepage layout:**
  - full-bleed parallax photo hero with a white lead-form card
  - overlapping figure band with counters
  - offset-frame intro photo
  - 12 numbered specialty photo cards
  - vertical island tabs with photos
  - gap check on deep purple
  - horizontal stepper
  - a "record" of events from 1959 to 2023
  - tool photo cards
  - community photo tiles
  - fit / no-fit cards
  - FAQ, guide cards, parallax CTA and contact form
- **Interior pages:** photo hero with breadcrumbs and a two-column layout. The sticky sidebar sits on the left on desktop and drops below the content on mobile.
- **Effects:**
  - header that turns solid on scroll
  - hero and CTA parallax
  - staggered reveal
  - counters
  - card hover zoom
  - island tabs
  - back-to-top button

  All of them respect `prefers-reduced-motion`. Without JavaScript the page renders fully: reveals stay visible and all island panels show.
- **Mobile:** an off-canvas drawer outside the header, with no `backdrop-filter`.
  - It has accordion submenus and locks page scroll while open.
  - It closes on ×, an overlay tap, a link tap or Escape, and manages `inert` / `aria-hidden`.
  - Its shadow and visibility apply only while it is open.
  - A fixed call bar sits at the bottom of the screen.
- The brand link in the header, drawer and footer never changes colour or gains an underline on hover. Playwright verifies this.

## Hosting notes (why pages are `dir/index.php`)

- The host ignores `.htaccess` and has no Agency-plan "force HTTPS" setting.
  - It serves real files directly, so the root `index.php` does not run for them.
  - It sends `/` and unknown paths to the root `index.php`.
- Every page is written as `dir/index.php`. Its first line is `<?php require_once dirname(__DIR__, n) . '/_guard.php'; ?>`, followed by
  static HTML with no other PHP. `validate.py` enforces this.
- `_guard.php` does the following:
  - 301-redirects `www.` and plain http (read from `X-Forwarded-Proto`, falling back to `HTTPS`) to `https://hawaiiinsuranceappraiser.com`, but only on the real domain
  - 301-redirects `/dir/index.php` and `/index.php` to the directory
  - sends `X-Robots-Tag: noindex, nofollow` on any other host, such as the preview URL
  - returns 404 when requested directly
- The root `index.php` front controller requires the guard, then:
  - serves `home.html` for `/`
  - 301-redirects to add a trailing slash
  - includes `dir/index.php` for directory URLs that reach it
  - returns `404.html` with a real 404 status
- **Never** create a root `index.html` or leave any `dir/index.html` on the server. The host would serve it and skip the guard.
  The only static `.html` files at the root are `home.html`, `404.html` and the Search Console file.
- On the preview URL Hostinger serves its own Googlebot-blocking `robots.txt`. That's expected; the real domain serves ours.

## Google Search Console verification file

- File: `googlecccfbf2f7e9e5ae4.html`, written to the root of `public/` on every build from the `GSC_FILE` / `GSC_BODY` constants in `build.py`.
- Exact contents: one line with no trailing newline, BOM, HTML or guard:
  `google-site-verification: googlecccfbf2f7e9e5ae4.html`
- `validate.py` checks its bytes. It also checks that the file is not in `sitemap.xml`, the HTML site map or any internal link, and that `robots.txt` does not block it.
- It must stay at the root permanently. Google rechecks it, and removing it unverifies the property. It only works for a **URL-prefix**
  property (`https://hawaiiinsuranceappraiser.com/`).

## Photos (internal record — not published)

All 30 photos are **CC0 1.0 or public domain** (U.S. government: USGS, NOAA, NPS, FEMA, U.S. military), so none needs attribution and
the site has no credits page.
- They were found through the Openverse API (`license=cc0,pdm`) and Wikimedia Commons and downloaded one at a time with backoff.
- Wikimedia files were fetched at the standard 1280px thumbnail width.
- Each is served as WebP at 1200px (or the source width if smaller) and 640px, with `srcset` / `sizes` and width/height set.
- Decorative backgrounds and card images use `alt=""`; content images use the descriptive alt text stored in `photos.json`.
- Five generic damage photos are from outside Hawaii: `fire-damage`, `flood-street`, `fallen-tree`, `roof-damage` and `wind-palms`.
  Their alt text names no place.

| Key | License | Source | Creator | Landing page |
| --- | --- | --- | --- | --- |
| `hero-island-homes` | CC0 1.0 | wikimedia | Christian Joudrey | https://commons.wikimedia.org/wiki/File:Honolulu_cityscape.jpg |
| `honolulu-skyline` | CC0 1.0 | wikimedia | ArdentArbitration | https://commons.wikimedia.org/wiki/File:Downtown_Honolulu_from_P%C5%ABowaina_(Punchbowl_Crater).jpg |
| `windward-oahu` | CC0 1.0 | wikimedia | — | https://commons.wikimedia.org/wiki/File:Kailua_bay.JPG |
| `oahu-suburb` | CC0 1.0 | wikimedia | Syced | https://commons.wikimedia.org/wiki/File:Aimuu_Gulch.jpg |
| `north-shore` | CC0 1.0 | wikimedia | Christian Joudrey | https://commons.wikimedia.org/wiki/File:Haleiwa,_United_States.jpg |
| `hilo-bay` | CC0 1.0 | wikimedia | Kaleodu at English Wikipedia | https://commons.wikimedia.org/wiki/File:Mauna_loa_from_hilo_bay.JPG |
| `kona-coast` | CC0 1.0 | wikimedia | Thomas Ensley thethomasensley | https://commons.wikimedia.org/wiki/File:Kailua-Kona,_United_States_(Unsplash).jpg |
| `lava-flow` | Public domain | wikimedia | United States Geological Survey | https://commons.wikimedia.org/wiki/File:USGS_K%C4%ABlauea_multimediaFile-2481_(2018-07-22).jpg |
| `lava-zone-homes` | Public domain | wikimedia | USGS | https://commons.wikimedia.org/wiki/File:USGS_Lava_on_Makamae_Street.jpg |
| `maui-valley` | CC0 1.0 | wikimedia | Bernard Spragg. NZ from Christchurch, New Zealand | https://commons.wikimedia.org/wiki/File:Iao_Valley_State_Park_Maui._(11248131064).jpg |
| `kihei-coast` | CC0 1.0 | wikimedia | Christian Joudrey | https://commons.wikimedia.org/wiki/File:Wedding_Beach,_Makena.jpg |
| `lahaina-harbor` | CC0 1.0 | wikimedia | Anna Goncharova goanne | https://commons.wikimedia.org/wiki/File:Lahaina_Harbor,_Lahaina,_United_States_(Unsplash).jpg |
| `kauai-coast` | CC0 1.0 | wikimedia | Brian Heimann bjheimann | https://commons.wikimedia.org/wiki/File:Napali_Coast_1_(Unsplash).jpg |
| `hurricane-satellite` | Public domain | wikimedia | NOAA | https://commons.wikimedia.org/wiki/File:Major_Hurricane_Lane_Approaches_Hawaii_(NESDIS_2018-08-22).jpg |
| `storm-surf` | CC0 1.0 | wikimedia | Tim Marshall timmarshall | https://commons.wikimedia.org/wiki/File:Here_comes_the_storm_(Unsplash).jpg |
| `wildfire` | Public domain | wikimedia | Hawai‘i Volcanoes NPS | https://commons.wikimedia.org/wiki/File:Brushfire_from_the_road_(50174820377).jpg |
| `fire-damage` | Public domain | wikimedia | Michael Mancino | https://commons.wikimedia.org/wiki/File:FEMA_-_39650_-_Wildfires_in_Hidden_Hills_neighborhood..jpg |
| `flood-street` | Public domain | wikimedia | Patsy Lynch | https://commons.wikimedia.org/wiki/File:Gretna,_La_flooded_street_Hurricane_Isaac_30_Aug_2012.jpg |
| `wind-palms` | Public domain | wikimedia | LCpl Patricia D. Lockhart | https://commons.wikimedia.org/wiki/File:The_wind_whips_through_palm_trees_as_Typhoon_Chaba_blows_ashore_at_U.S._Marine_Corps_Base_Smedley_D._Butler,_Okinawa,_Japan,_Oct._28,_2010_101028-M-VG363-103.jpg |
| `fallen-tree` | Public domain | wikimedia | Liz Roll | https://commons.wikimedia.org/wiki/File:FEMA_-_40050_-_House_damaged_by_a_tree_in_Kentucky.jpg |
| `metal-roof` | CC0 1.0 | wikimedia | Hermann Luyken | https://commons.wikimedia.org/wiki/File:2013.11.01.112836_Haili_Street_Hilo_Hawaii.jpg |
| `roof-shingles` | CC0 1.0 | stocksnap | The Building Envelope | https://stocksnap.io/photo/house-roof-SQQD7NUGYO |
| `roof-damage` | Public domain | wikimedia | Barry Bahler | https://commons.wikimedia.org/wiki/File:FEMA_-_38126_-_Installing_a_blue_roof_in_Louisiana_after_Hurricane_Gustav.jpg |
| `condo-towers` | CC0 1.0 | wikimedia | Bernard Spragg. NZ from Christchurch, New Zealand | https://commons.wikimedia.org/wiki/File:Hilton_Waikiki_Hawaii._(16545672009).jpg |
| `commercial-building` | CC0 1.0 | wikimedia | Joel Bradshaw | https://commons.wikimedia.org/wiki/File:Honolulu-FortStreet-ProgressBlock-corner.JPG |
| `lanai-interior` | CC0 1.0 | wikimedia | Jarosław Ceborski jarson | https://commons.wikimedia.org/wiki/File:Living_room_(Unsplash).jpg |
| `consultation` | CC0 1.0 | stocksnap | Helloquence | https://stocksnap.io/photo/writing-papers-Y01VDYAX63 |
| `laptop-calculator` | CC0 1.0 | wikimedia | — | https://commons.wikimedia.org/wiki/File:Desktop_with_laptop_and_calculator_(Unsplash).jpg |
| `calculator-documents` | CC0 1.0 | stocksnap | Tevarak | https://stocksnap.io/photo/calculator-calendar-RFVHCUGML3 |
| `inspection-clipboard` | CC0 1.0 | wikimedia | Clem Onojeghuo clemono2 | https://commons.wikimedia.org/wiki/File:At_a_Building_site_(Unsplash).jpg |

## SEO rules enforced by validate.py (must report zero errors)

- Title ≤ 60 characters and ≤ ~580px (Arial metrics at 20px); titles unique.
- Every page has one hand-written meta description of **110–143 characters** that ends in a full sentence. Descriptions are unique, and `og:description` and `twitter:description` match them.
  The current range is 125–140 characters.
- Exactly one H1; the first heading is the H1; no skipped heading levels anywhere (footer, sidebar boxes and tools included).
- JSON-LD parses, and every `@id` reference resolves. Each page node (WebPage, AboutPage, ContactPage or CollectionPage) links to its BreadcrumbList,
  primary image and main entity. The graph also includes:
  - Service on specialty and community pages
  - FAQPage, ItemList, WebApplication, BlogPosting, HowTo and DefinedTermSet where they apply
  - ProfessionalService, with logo, contactPoint, HI/US, the state and cities as areaServed, and an OfferCatalog
- No broken internal links or anchors; every image has `alt`; every page is in `sitemap.xml`; Open Graph and Twitter tags and `geo.region` are present.
- The homepage's `<main>` mentions "Hawaii Insurance Appraiser" at least 14 times. It currently has 16.
- No sister-state name appears in any published text file. All 43 other states are on the banned list in `validate.py`.
- Every page file starts with the guard line and contains no other PHP; no `index.html` files and no `photo-credits/`.

## Contact form

`/api/contact.php` has a honeypot, a per-IP limit of 5 submissions per 10 minutes, and validation (name, a valid email or a phone number, and consent).
- When `api/_private/config.php` exists, it sends through `info@hawaiiinsuranceappraiser.com` over authenticated SMTP (`smtp.hostinger.com:465`).
- Otherwise it falls back to PHP `mail()`.
- It always appends a JSON line to `api/_private/leads.log.php`. That file starts with `<?php http_response_code(404); exit; ?>`, so direct requests get a 404.
- The Hostinger file API can't write outside `public_html`, which is why both private files sit inside it.
- `_private/` is in `.gitignore`. **Never commit credentials.** Keep any local copy of the config outside the repo, and delete it once uploaded.

Config file to upload once the mailbox exists:

```php
<?php
if (!defined('HIA_CONFIG_OK')) { http_response_code(404); exit; }
return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
        'smtp_user' => 'info@hawaiiinsuranceappraiser.com', 'smtp_pass' => '…'];
```

After uploading:
1. Confirm `/api/_private/config.php` returns 404 with 0 bytes.
2. Send one submission labelled as a test.
3. Check that the log line shows `"via":"smtp"`.

## Going-live checklist

1. Point the domain's nameservers to `orbit.dns-parking.com` / `horizon.dns-parking.com`.
2. Confirm that SSL covers both the apex and `www`. If `www` is missing, run `agency-hosting_ssl_reinstall-website`.
3. Re-check the www and http 301s, the `index.php` 301, the sitemap URLs (all 200), that no `X-Robots-Tag` is sent, and the Search Console file on the real domain.
4. Create the mailbox, upload the SMTP config, and run the test above.
5. In Search Console, verify the URL-prefix property `https://hawaiiinsuranceappraiser.com/`, then submit `/sitemap.xml`.
