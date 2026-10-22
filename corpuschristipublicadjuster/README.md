# CorpusChristiPublicAdjuster.com — website source

Complete rebuild of https://corpuschristipublicadjuster.com/ (formerly WordPress + Elementor) as a fast,
dependency-free custom PHP site for Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`).
No database, no Node, no API keys. Built on the same engine as the McAllen Public Adjuster rebuild,
with a new coastal design, Corpus Christi content, and extra tools.

| Path | What it is |
|---|---|
| `dist/corpuschristipublicadjuster-public_html.zip` | **Upload-ready package** — extract directly into `public_html` |
| `INSTALL-HOSTINGER.md` | Step-by-step install, SMTP, cron, HTTPS, testing, launch |
| `VERIFICATION-REPORT.md` | URL inventory, preserved/new content, redirects, tools, test results |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Build/test scripts, content spec, verified fact sheets, original-site archive (not uploaded) |

## Highlights

* **Every original URL kept** (7 articles, 6 pages, `/blog/`); WordPress archives, sitemaps, shortlinks
  and the old author URL 301 to their new homes. All original `/wp-content/uploads/` image URLs still resolve.
* **Forms** (homepage, contact, Free Claim Review, and a popup that opens **5 seconds** after page load)
  email **info@corpuschristipublicadjuster.com** over authenticated SMTP. Joseph Dittman's direct email
  (jditt@risepublicadjusting.com) is shown for visitors who want to reach him directly.
* **Author:** every article is by Joseph Dittman, Licensed Public Adjuster (byline, bio box, Person schema).
* **Weather app** (`/weather/`): NWS current conditions (KCRP), hourly chart + strip, 7-day forecast,
  alerts, animated NEXRAD radar loop, NOAA tide chart (observed vs. predicted, 3 stations), NHC tropics
  watch, hurricane-season countdown.
* **Tools:** hurricane deductible calculator, claim deadline calculator (Tex. Ins. Code ch. 542 and TWIA
  ch. 2210 timelines), settlement calculator, documentation checklist, storm lookup, storm history,
  recent weather events (NOAA NCEI + NWS LSR data for Nueces, San Patricio, Aransas, Kleberg counties).
* **Design:** brand palette from the original site (black, steel blue #4A70A9, sky #8FABD4, cream) with
  a sunset accent; aurora gradients, animated waves, glass header/cards, spotlight + tilt cards, marquee,
  word-reveal headline, scroll progress, reveal-on-scroll — all disabled under `prefers-reduced-motion`.

## Site structure (`site/`)

```
index.php            front controller (routing, legacy redirects, sitemap.xml, /feed/)
.htaccess            HTTPS + apex redirect, private-folder blocking, caching, security headers
api/                 claim-review.php (form handler), form-token.php, storms.php (JSON)
assets/              css/site.css, js/{site,calculator,checklist,storms,weather-app,tools}.js, img/, fonts/, vendor/leaflet/
content/pages/       page content files      (pages/about-us.php -> /about-us/, service-areas__rockport-tx.php -> /service-areas/rockport-tx/)
content/services/    19 service pages        (-> /services/<slug>/)
content/posts/       21 articles             (-> /<slug>/, same as the original WordPress permalinks)
templates/           layouts + components (header, footer, hero, waves, forms, weather, storm cards…)
includes/            config.php, functions, SEO/schema, form security + PHPMailer, weather/tides/tropics + storm data
cron/                run-all.php, refresh-weather.php, update-weather-events.php, update-storm-history.php, maintenance.php
data/                storm-history.json (NOAA NCEI), weather-events.json (NWS LSR), places.json; cache/ logs/ ratelimit/
wp-content/uploads/  original WordPress images kept at their old URLs
```

## Local development

```sh
sh tools/test/serve.sh                         # PHP dev server on http://127.0.0.1:8081
python3 tools/test/crawl.py                    # SEO + link crawl of every page
NODE_PATH=$(npm root -g) node tools/test/functional.js   # browser tests (Playwright)
python3 tools/build_images.py                  # regenerate featured images + responsive variants
sh tools/package.sh                            # build dist/corpuschristipublicadjuster-public_html.zip
```

Content rules for writers are in `tools/CONTENT_SPEC.md`; verified facts in `tools/notes/local-facts.md`
and `tools/notes/storm-facts.md`.

## Deployment (live since 2026-10-22)

* **Live site:** Hostinger **Agency** plan, plain php-fpm website UID **`j0WNY4Y29`** (PHP 8.3), document root
  `/home/u914589053/websites/j0WNY4Y29/public_html`, domain `corpuschristipublicadjuster.com` (Let's Encrypt SSL).
  Deployed with `bash tools/deploy.sh` (File Browser TUS API; credentials from
  `agency-hosting_files_generate-upload-url`), then `agency-hosting_cache_clear-website`.
* **The H5G platform ignores `.htaccess`** and the File Browser can only write inside `public_html`, so:
  * `index.php` enforces `https://` + apex (301 from `http://` and `www.`) and all legacy redirects;
  * every private PHP file (`includes/`, `templates/`, `content/`) starts with `defined('CCPA_ROOT') || exit;`
    so a direct request returns an empty page; `cron/` scripts refuse non-CLI requests;
  * logs (`data/logs/*.log.php`) and the form-signing secret (`data/secret.php`) are PHP files whose first line
    returns 404 and exits, so they are never readable over HTTP.
* **Email:** forms go to info@corpuschristipublicadjuster.com. `public_html/includes/config.local.php` on the
  server (not in git) currently sets `allow_mail_fallback => true`, so mail is sent with the server's PHP
  `mail()`. To send through the Hostinger mailbox instead (better deliverability), add
  `'smtp_pass' => '<mailbox password>'` to that file. Verified with a live test submission on 2026-10-22.
* **Cron (website cron jobs):** `*/15 * * * *` refresh-weather.php · `7 * * * *` update-weather-events.php ·
  `23 8 * * *` maintenance.php · `41 9 * * 1` update-storm-history.php
  (each `/usr/bin/php /home/u914589053/websites/j0WNY4Y29/public_html/cron/<script>`).
* **Old WordPress site:** Agency website UID `cSSyXpzsS` was **not deleted** — the domain was only unlinked
  from it, so its files and database are intact. Rollback: unlink the domain from `j0WNY4Y29` and link it back
  to `cSSyXpzsS` (`agency-hosting_domains_unlink-from-website` / `agency-hosting_domains_link-to-website`).
  Delete it in hPanel once you no longer need it.
* **Testing a live host:** the CDN rate-limits fast crawls; use `CRAWL_DELAY=0.8 python3 tools/test/crawl.py https://corpuschristipublicadjuster.com`.
