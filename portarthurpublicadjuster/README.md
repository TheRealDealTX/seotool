# PortArthurPublicAdjuster.com — website source

Complete rebuild of https://portarthurpublicadjuster.com/ (WordPress/Elementor) as a fast, custom
PHP/HTML site for Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`). Built on the same
engine as the McAllen Public Adjuster rebuild, re-themed and re-written for Port Arthur, Jefferson County,
and Southeast Texas. No database, no Node, no API keys.

| Path | What it is |
|---|---|
| `dist/portarthurpublicadjuster-public_html.zip` | **Upload-ready package** — extract directly into `public_html` |
| `INSTALL-HOSTINGER.md` | Step-by-step install, SMTP, cron, HTTPS, testing, launch |
| `VERIFICATION-REPORT.md` | URL inventory, preserved/new content, tools, integrations, test results |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Content spec, verified storm facts, image builder, tests, original-site archive (not uploaded) |

## Highlights

* **Every original URL kept** — `/`, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/privacy-policy/`,
  `/terms-of-use/`, `/are-insurance-adjusters-honest/`, `/category/general/`, and all 26 `/wp-content/uploads/` images.
* **57 indexable pages**: 19 service pages, 10 articles by Joseph Dittman (licensed public adjuster),
  6 service-area pages, FAQ, tools, legal pages.
* **Weather & tools**: live hurricane tracker (National Hurricane Center), live Port Arthur weather + KLCH radar,
  hurricane deductible calculator, settlement calculator, documentation checklist, storm event lookup,
  NOAA storm history (Jefferson County, 1955–2026), recent NWS storm reports.
* **Forms**: Free Claim Review form (page, homepage, contact) and a popup that opens **5 seconds** after load.
  Every submission is emailed to **info@portarthurpublicadjuster.com**.
* **Design**: original palette (deep teal `#334443`, sea teal `#34656D`, cream `#FAF8F1`, sand gold `#FAEAB1`)
  with a modern layer — aurora hero, glass cards, pointer spotlight, shine buttons, scroll progress,
  blur-in reveals, area ticker, animated counters — all disabled under `prefers-reduced-motion`.
* Homepage uses "Port Arthur Public Adjuster" 20 times in main content (26 including header/footer).

## Site structure (`site/`)

```
index.php            front controller (routing, legacy redirects, sitemap.xml, /feed/)
.htaccess            HTTPS + apex redirect, private-folder blocking, caching, security headers
api/                 claim-review.php (form handler), form-token.php, storms.php (JSON)
assets/              css/site.css, js/{site,calculator,checklist,storms,tropics,deductible}.js, img/, fonts/, vendor/leaflet/
content/pages/       page content files      (pages/about-us.php -> /about-us/, a__b.php -> /a/b/)
content/services/    19 service pages        (-> /services/<slug>/)
content/posts/       10 articles             (-> /<slug>/, same as the original WordPress permalinks)
templates/           layouts + components (header, footer, hero, forms, weather, tropics, storm cards…)
includes/            config.php, functions, SEO/schema, form security + PHPMailer, weather, tropics, storm data
cron/                run-all.php, refresh-weather.php, update-weather-events.php, update-storm-history.php, maintenance.php
data/                storm-history.json (NOAA NCEI), weather-events.json (NWS LSR), places.json; cache/ logs/ ratelimit/
wp-content/uploads/  original WordPress images kept at their old URLs
```

## Local development

```sh
sh tools/test/serve.sh                         # PHP dev server on http://127.0.0.1:8081
python3 tools/test/smtp_sink.py 2527 &         # local mail sink (with site/includes/config.local.php)
python3 tools/test/crawl.py                    # SEO + link crawl of every page
NODE_PATH=$(npm root -g) node tools/test/functional.js   # browser tests (Playwright)
python3 tools/build_images.py                  # regenerate featured images + responsive variants
sh tools/package.sh                            # build dist/portarthurpublicadjuster-public_html.zip
```

Content rules for writers are in `tools/CONTENT_SPEC.md`; verified storm facts in `tools/storm-facts.md`.
