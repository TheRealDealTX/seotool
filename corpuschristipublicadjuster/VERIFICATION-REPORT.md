# Verification Report — McAllenPublicAdjuster.com Rebuild

Prepared October 3, 2026. Everything below was checked on a local copy of the site running under
**Apache 2.4 + PHP 8.3 with the shipped `.htaccess`**, plus the PHP built-in server. A few items
can only be confirmed on the live Hostinger account; they're listed under **Remaining
configuration steps**.

## 1. Audit of the existing site

The live site was a WordPress install (Elementor + Yoast SEO). Its REST API and Yoast sitemaps
(post, page, and category) list everything that was published:

* **7 pages**, **8 blog posts**, **1 category** (`/category/general/`), and 1 author archive.
* **53 media items** (240 image files counting WordPress's resized copies). All 225 that still return 200 on the live site were downloaded and kept at the **same `/wp-content/uploads/…` URLs**. The other 15 already return 404 on the live site: logo/icon variants that were deleted.
* There were no custom redirects. Every page and post was indexable (index, follow), with canonicals on the same URLs.
* The original text, HTML, titles, meta descriptions, and dates are archived in `tools/original-content/` (`posts_full.json`, `pages_full.json`, `media.json`, plus one Markdown file per page).

## 2. Original pages and articles preserved (15 of 15)

Every original URL is kept exactly as it was. No URL changed, so no content redirects were needed. Publish dates are the original dates; "Updated October 3, 2026" is shown on the rewritten posts.

| Original URL | Original title | Orig. date | Status | New body words (orig.) | FAQs |
|---|---|---|---|---|---|
| `/about-us/` | About Us | 2026-02-06 | Preserved, same URL (200) | 1,110 (875) | 5 |
| `/contact/` | Contact | 2026-02-06 | Preserved, same URL (200) | 219 (90) | 4 |
| `/` | McAllen Public Adjuster | 2026-02-06 | Preserved, same URL (200) | template-built | 7 |
| `/privacy-policy/` | Privacy Policy | 2026-02-06 | Preserved, same URL (200) | 986 (712) | 3 |
| `/blog/` | Blog | 2026-02-06 | Preserved, same URL (200) | template-built | 0 |
| `/services/` | Services | 2026-02-06 | Preserved, same URL (200) | 925 (841) | 5 |
| `/terms-of-use/` | Terms of Use | 2026-02-06 | Preserved, same URL (200) | 767 (653) | 3 |
| `/document-hail-damage-for-an-insurance-claim/` | How to Document Hail Damage for an Insurance Claim | 2026-04-26 | Preserved, same URL (200) | 1,617 (1,835) | 6 |
| `/hail-damage-claim-supplements/` | Hail Damage Claim Supplements: What Carriers Miss in Their Scope | 2026-04-26 | Preserved, same URL (200) | 1,711 (1,283) | 6 |
| `/public-adjuster-vs-insurance-adjuster-for-hail-claims/` | Public Adjuster vs. Insurance Adjuster for Hail Claims in Texas | 2026-04-26 | Preserved, same URL (200) | 1,753 (1,637) | 6 |
| `/what-to-do-if-your-hail-claim-was-denied-in-mcallen/` | What to Do If Your Hail Claim Was Denied in McAllen | 2026-04-26 | Preserved, same URL (200) | 1,663 (2,200) | 6 |
| `/roof-hail-damage-insurance-claim-mcallen/` | Roof Hail Damage Insurance Claim McAllen | 2026-04-25 | Preserved, same URL (200) | 1,912 (1,863) | 6 |
| `/fire-insurance-adjuster/` | Fire Insurance Adjuster: How They Protect Your Claim | 2026-03-28 | Preserved, same URL (200) | 1,728 (1,130) | 6 |
| `/claim-changes-knowing-when-to-hire-a-public-adjuster/` | The Moment a Claim Changes: Knowing When to Hire a Public Adjuster | 2026-03-15 | Preserved, same URL (200) | 1,706 (2,124) | 6 |
| `/fire-insurance-public-adjuster/` | Fire Insurance Public Adjuster: Maximize Your Fire Damage Claim in McAllen, TX | 2026-02-12 | Preserved, same URL (200) | 1,734 (1,877) | 6 |

Changes made to the original content: the writing was improved and expanded, and these were added:
* local NOAA/NWS storm data
* Texas regulatory facts (Insurance Code Ch. 4102 and 542)
* tables, key-takeaways boxes, FAQs (with FAQ schema), sources, and internal links

The following were removed:
* unsupported claims: "you pay nothing unless…", "team of licensed public adjusters", "maximize your payout", made-up dollar examples, and a 5–15% fee range
* off-topic dictionary and Wikipedia links (e.g. Epistemology, Fourier transform)
* the phone-number suffix in every title tag

## 3. New pages added (28)

| URL | Title | Type | Body words | FAQs |
|---|---|---|---|---|
| `/service-areas/` | Areas We Serve in the Rio Grande Valley | Page / tool | 1,048 | 4 |
| `/claim-tools/` | Free Insurance Claim Tools | Page / tool | 345 | 3 |
| `/claim-calculator/` | Insurance Claim Settlement Calculator | Page / tool | 634 | 5 |
| `/author/joseph-dittman/` | Joseph Dittman, Public Adjuster | Page / tool | 418 | 3 |
| `/weather/` | Live McAllen Weather & 7-Day Forecast | Page / tool | 652 | 5 |
| `/storm-history/` | McAllen & Hidalgo County Storm History | Page / tool | 859 | 5 |
| `/local-building-codes/` | McAllen Building Codes and Insurance Claims | Page / tool | 1,497 | 6 |
| `/claim-documentation-checklist/` | Property Insurance Claim Documentation Checklist | Page / tool | 562 | 4 |
| `/weather-events/` | Recent Weather Events in McAllen & Hidalgo County | Page / tool | 589 | 4 |
| `/free-claim-review/` | Request a Free Claim Review | Page / tool | 293 | 4 |
| `/sitemap/` | Sitemap | Page / tool | 0 | 0 |
| `/storm-lookup/` | Storm Event Lookup for McAllen Properties | Page / tool | 571 | 4 |
| `/services/hail-damage-claims/` | Hail Damage Insurance Claims in McAllen, TX | Service page | 993 | 6 |
| `/services/roof-damage-insurance-claims/` | Roof Damage Insurance Claims in McAllen, TX | Service page | 937 | 6 |
| `/services/wind-damage-claims/` | Wind Damage Insurance Claims in McAllen, TX | Service page | 913 | 6 |
| `/services/storm-damage-claims/` | Storm Damage Insurance Claims in McAllen, TX | Service page | 920 | 6 |
| `/services/hurricane-damage-claims/` | Hurricane Damage Insurance Claims in McAllen, TX | Service page | 941 | 6 |
| `/services/fire-damage-claims/` | Fire Damage Insurance Claims in McAllen, TX | Service page | 912 | 6 |
| `/services/smoke-damage-claims/` | Smoke Damage Insurance Claims in McAllen, TX | Service page | 925 | 6 |
| `/services/water-damage-claims/` | Water Damage Insurance Claims in McAllen, TX | Service page | 921 | 6 |
| `/services/commercial-property-claims/` | Commercial Property Insurance Claims in McAllen | Service page | 1,059 | 6 |
| `/services/residential-property-claims/` | Residential Property Insurance Claims in McAllen | Service page | 941 | 6 |
| `/services/denied-insurance-claims/` | Denied Insurance Claim Help in McAllen, TX | Service page | 1,001 | 6 |
| `/services/underpaid-insurance-claims/` | Underpaid Insurance Claim Help in McAllen, TX | Service page | 925 | 6 |
| `/services/delayed-insurance-claims/` | Delayed Insurance Claims in McAllen, TX | Service page | 949 | 6 |
| `/services/insurance-claim-supplements/` | Insurance Claim Supplements in McAllen, TX | Service page | 926 | 6 |
| `/services/insurance-appraisal/` | Insurance Appraisal in McAllen | Service page | 932 | 6 |
| `/services/insurance-estimate-review/` | Insurance Estimate Review in McAllen, TX | Service page | 953 | 6 |

## 4. New articles added (12)

All new articles are dated October 3, 2026, the day they were written. None are backdated. Each one has:
* the Joseph Dittman byline and author box
* a key-takeaways box, tables, and FAQs
* authoritative sources and a Free Claim Review CTA

Their topics don't duplicate the 8 existing posts.

| URL | Title | Published | Body words | FAQs |
|---|---|---|---|---|
| `/building-codes-insurance-repairs-mcallen/` | How Local Building Codes Can Affect Insurance Repairs in McAllen | 2026-10-03 | 1,725 | 5 |
| `/document-commercial-property-damage-after-storm/` | How to Document Commercial Property Damage After a Storm | 2026-10-03 | 1,852 | 7 |
| `/freeze-damage-burst-pipe-claims-rio-grande-valley/` | Freeze Damage and Burst Pipe Claims in the Rio Grande Valley | 2026-10-03 | 1,551 | 5 |
| `/how-to-review-underpaid-roof-insurance-estimate/` | How to Review an Underpaid Roof Insurance Estimate | 2026-10-03 | 1,804 | 6 |
| `/hurricane-damage-mcallen-homeowners-guide/` | What McAllen Homeowners Should Know About Hurricane-Related Damage | 2026-10-03 | 1,934 | 6 |
| `/insurance-company-disputes-storm-damage/` | What to Do When an Insurance Company Disputes Storm Damage | 2026-10-03 | 2,213 | 6 |
| `/mcallen-hail-season-storm-data/` | When Is Hail Season in McAllen? What 70 Years of NOAA Data Shows | 2026-10-03 | 1,632 | 6 |
| `/noaa-weather-records-document-property-damage-mcallen/` | Using NOAA Weather Records to Document Property Damage in McAllen | 2026-10-03 | 1,613 | 6 |
| `/replacement-cost-vs-actual-cash-value-texas/` | Replacement Cost vs. Actual Cash Value in Texas Property Insurance | 2026-10-03 | 1,598 | 6 |
| `/water-damage-vs-flood-damage-mcallen/` | Water Damage vs. Flood Damage: What McAllen Property Owners Should Know | 2026-10-03 | 1,880 | 6 |
| `/why-property-insurance-claims-are-delayed-texas/` | Common Reasons Property Insurance Claims Are Delayed in Texas | 2026-10-03 | 2,123 | 6 |
| `/wind-damage-insurance-claims-mcallen-tx/` | How to Handle Wind Damage Insurance Claims in McAllen, TX | 2026-10-03 | 2,099 | 6 |

## 5. Redirects and legacy URL handling (verified under Apache)

| Request | Result |
|---|---|
| `http://…` (any page) | 301 → `https://mcallenpublicadjuster.com/…` |
| `https://www.mcallenpublicadjuster.com/…` | 301 → `https://mcallenpublicadjuster.com/…` |
| `/about-us` (no trailing slash) | 301 → `/about-us/` |
| `/category/general/`, `/category/uncategorized/` | 301 → `/blog/` |
| `/author/infohoustonpublicadjusting-com/` (old WP author) | 301 → `/author/joseph-dittman/` |
| `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml`, `/wp-sitemap.xml` | 301 → `/sitemap.xml` |
| `/?p=<id>` and `/?page_id=<id>` (all 15 original WordPress IDs) | 301 → the matching page |
| `/blog/page/2/` | 301 → `/blog/?pg=2` |
| `/<post>/feed/`, `/<post>/amp/`, `/<post>/embed/` | 301 → the post |
| `/comments/feed/` | 301 → `/feed/` (RSS feed preserved at `/feed/`) |
| `/home/`, `/contact-us/`, `/about/`, `/building-codes/`, `/tools/` | 301 → the matching new page |
| `/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`, `/wp-json/` | 410 Gone |
| Unknown URLs | Custom 404 page (HTTP 404) |
| `/includes/`, `/content/`, `/templates/`, `/data/`, `/cron/`, dotfiles, `config.local.php` | Blocked (404 page), confirmed under Apache |

## 6. Tools created

| Tool | URL | What it does | Test result |
|---|---|---|---|
| Insurance Claim Settlement Calculator | `/claim-calculator/` | RCV, depreciation ($ or %), ACV, deductible, prior payments, non-covered costs, policy limit, RC vs ACV policy. Real-time results, explanations, reset, print, download (.txt) | 5 hand-checked scenarios pass, including % depreciation + prior payments, ACV policy, limit cap, and deductible larger than the loss |
| Property Damage Documentation Checklist | `/claim-documentation-checklist/` | 6 damage categories (hail, wind, fire, water, roof, commercial), 20–21 items each, progress bar, per-item and general notes, print, download, reset. Saving to localStorage is opt-in. Nothing is transmitted | Pass |
| Storm Event Lookup (optional tool #3) | `/storm-lookup/` | Search by city or ZIP (36 places, 29 ZIP codes), radius, approximate date ± window or date range, and event type. NOAA + NWS records, distances, map, documentation guidance, disclaimer | Pass. ZIP 78504 around May 8, 2025 returns the hail reports |
| Storm History | `/storm-history/` | 698 NOAA NCEI events for Hidalgo County (1955–2026). Filters: date range, location, type, minimum wind mph, minimum hail size, keyword. Timeline chart, Leaflet map, paginated table with an NCEI link on every row | Pass. Baseball-size (≥2.75") filter returns 12 events; adding "McAllen" returns 1 (the 4.5" hail of April 20, 2012) |
| Live Weather | `/weather/` | Current KMFE observation (temperature, conditions, wind speed/direction, gusts, humidity, heat index/dew point, pressure, visibility), 7-day forecast with chance of rain and forecast rainfall, active NWS alerts, detailed forecast, timestamps | Real NWS data loaded. Stale-cache and fallback paths are coded |
| Weather Events | `/weather-events/` | Automatically updated NWS Local Storm Reports for Hidalgo County. Event cards show type, date/time, place, severity, description, reporter, source link, and last-verified time. Includes type filter and a "Did a Recent Storm Damage Your Property?" CTA | 72 real reports (2024–2026) loaded. Hourly cron tested |

## 7. Integrations completed

* **NWS API (api.weather.gov):** grid point BRO 49,19, station KMFE, forecast + raw grid QPF, and active alerts. Results are cached server-side (10 min current, 30 min forecast, 5 min alerts) with lock files. If NWS fails, the last good data is shown with its age; if there is no cache, a fallback message links to weather.gov. Expired alerts are filtered out on read and purged daily.
* **Weather events cron (`cron/update-weather-events.php`):** reads new LSR text products from the NWS API (fixed-width parser) and backfills from the Iowa Environmental Mesonet archive of the same NWS reports. It filters to Hidalgo County, TX with a bounding-box check, dedupes on time/type/location, applies NWS "Corrects previous" corrections, and keeps 3 years. It records source status and last success, and logs to `data/logs/events.log`.
* **Storm history cron (`cron/update-storm-history.php`):** downloads NCEI bulk CSVs (current + previous year weekly; `--full` rebuilds 1950–present), streams and filters them, and drops events NCEI removed. Wind speeds are converted from knots to mph. A full rebuild was run locally: 75 yearly files, 698 tracked events.
* **Forms:**
  * PHPMailer 6.10 over authenticated SMTP. Submissions go to jditt@risepublicadjusting.com with Reply-To set to the visitor. That address appears on **no** public page (checked by the crawler).
  * Security: signed one-time CSRF tokens (JS refreshes them, so cached pages work), honeypot, minimum fill time, same-origin check, and rate limiting (5 per hour per IP, stored as hashed IPs). Validation and sanitization happen on both server and client, all output is escaped, header injection is stripped, and attachments are MIME-checked with finfo (JPG/PNG/WEBP/HEIC/PDF, 3 × 8 MB, emailed and never stored).
  * The success message appears only after the SMTP server accepts the message. The form also works without JavaScript.
* **SEO:**
  * Unique titles and descriptions (≤150 characters on every page), one H1 per page, canonicals, Open Graph/Twitter tags, and breadcrumbs with BreadcrumbList schema.
  * Schema: ProfessionalService/LocalBusiness (no address, area served, TDI credential), WebSite, WebPage, BlogPosting + Person (Joseph Dittman) on articles, Service on service pages, FAQPage, and Person on the author page.
  * XML sitemap and RSS feed are generated from the content files. `robots.txt` points to the sitemap. There is also an HTML sitemap at `/sitemap/`. Search, category, and paginated blog views are noindex.

## 8. Testing results

| Test | Result |
|---|---|
| PHP lint of every `.php` file | Pass |
| Crawl of all 55 sitemap pages + 143 internal link targets (`tools/test/crawl.py`), under both Apache and the PHP server | **0 problems.** All 200, one H1 each, unique titles/descriptions, valid canonicals, JSON-LD parses, every `<img>` has alt text and resolves, no PHP warnings, no internal email exposed |
| Homepage keyword "McAllen Public Adjuster" (visible text) | 18 occurrences, used naturally across the H1, intro, sections, FAQs, forms, and footer |
| Functional browser tests (`tools/test/functional.js`, Playwright/Chromium) | **22/22 pass** under Apache: calculator math and UI, checklist (progress, save, download, reset), storm history filters, storm lookup, form client validation, form submission via JS, mobile nav, sticky call bar, no JS errors |
| Form server tests | Valid submission with attachment delivered to the recipient (local SMTP sink: correct To, Reply-To, subject, attachment). Token reuse, invalid fields, `.php` upload, cross-origin post, honeypot, GET, and rate limit (6th request → 429) all handled. SMTP down → 502 error and no success message. No-JS post renders a confirmation page |
| Accessibility (axe-core 4.10, WCAG 2 A/AA) on 12 key pages | 0 violations after fixes (footer button contrast, link underlines) |
| Mobile (390 px) and desktop (1366 px) screenshots of 15 templates | No horizontal overflow. Layout checked visually |
| Reduced motion | All animations, parallax, and smooth scroll are disabled under `prefers-reduced-motion` |
| External links (66) | All return 200, except ecode360.com (blocks automated checks with 403 but works in a browser) |

## 9. Performance notes

* No frameworks. Total JS is about 12 KB (site) plus page-specific tools. Leaflet is loaded only on the two storm-map pages. Fonts (Montserrat + Inter, latin subset) are self-hosted and preloaded.
* Images are WebP with generated 480/960/1440 px variants, `srcset`/`sizes`, explicit width/height, and lazy loading. Only the hero image is eager, with `fetchpriority=high`.
* `.htaccess` turns on gzip/deflate, long-lived caching for static assets (versioned query strings bust the cache), and security headers.

## 10. Remaining configuration steps (cannot be completed from here)

1. **SMTP password:** create `mpa-config.php` with the info@mcallenpublicadjuster.com mailbox password (see INSTALL-HOSTINGER.md §4), then send a live test and confirm it arrives at jditt@risepublicadjusting.com. Live delivery was tested only against a local mail server.
2. **Cron jobs:** add them in hPanel (§6). Until cron runs, pages refresh weather on demand, and the bundled storm data (current to October 3, 2026) is shown.
3. **TDI license #3356839:** it matches the number on the current site and on txpublicadjusting.com, but it was **not** confirmed in TDI's own lookup (the lookup is an interactive form). Verify it at https://www.tdi.texas.gov/agent/agent-lookup.html before launch. It is set in one place: `includes/config.php`.
4. **SSL/HTTPS and CDN purge** on Hostinger (§8). HSTS is left commented out until HTTPS is confirmed.
5. **Search Console:** submit `/sitemap.xml` after launch.
6. **Map tiles:** OpenStreetMap tiles couldn't load in the test sandbox (network policy) but load normally in browsers. The map code, markers, and fallbacks were tested.
7. **Joseph Dittman's photo** is the one published on txpublicadjusting.com. Replace `assets/img/joseph-dittman.webp` if a different photo is preferred.
8. **Images:** all photos come from the business's existing media library (cropped into new featured images). No stock or third-party photos were added. Swap any featured image in `assets/img/featured/` and re-run `python3 tools/build_images.py` for responsive versions.

## 11. Facts verified for content (sources)

* McAllen code adoption: City of McAllen Residential Permit Checklist REV 01/2026 lists "International Residential Code 2024 / International Energy Code 2024". Texas Border Business (Nov 2025) reports adoption of the 2024 ICC codes + 2023 NEC effective January 1, 2026, and the City permits/inspections pages and fee schedule are cited. Verified October 3, 2026.
* Texas law: Insurance Code Ch. 4102 (10% fee cap, 72-hour rescission, "We represent the insured only"), Ch. 542 Subchapter B deadlines (15 days / 15 business days / +45 days / 5 business days, +15 days after a declared catastrophe), and Ch. 542A pre-suit notice. TWIA catastrophe area counties (Hidalgo not included).
* Weather history: NOAA NCEI Storm Events Database, every cited event linked to its NCEI record (`tools/notes/storm-facts.md`).
* Author bio: txpublicadjusting.com author box for Joseph Dittman. No certifications, counts, or awards beyond what is published there were added.
