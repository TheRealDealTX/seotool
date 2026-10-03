# McAllenPublicAdjuster.com — website source

Complete rebuild of https://mcallenpublicadjuster.com/ as a fast, dependency-free PHP site for
Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`). No database, no Node, no API keys.

| Path | What it is |
|---|---|
| `dist/mcallenpublicadjuster-public_html.zip` | **Upload-ready package** — extract directly into `public_html` |
| `INSTALL-HOSTINGER.md` | Step-by-step install, SMTP, cron, HTTPS, testing, launch |
| `VERIFICATION-REPORT.md` | URL inventory, preserved/new content, redirects, tools, integrations, test results |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Build/test scripts, content spec, original-site archive (not uploaded) |

## Site structure (`site/`)

```
index.php            front controller (routing, legacy redirects, sitemap.xml, /feed/)
.htaccess            HTTPS + apex redirect, private-folder blocking, caching, security headers
api/                 claim-review.php (form handler), form-token.php, storms.php (JSON)
assets/              css/site.css, js/{site,calculator,checklist,storms}.js, img/, fonts/, vendor/leaflet/
content/pages/       page content files      (pages/about-us.php -> /about-us/)
content/services/    16 service pages        (-> /services/<slug>/)
content/posts/       20 articles             (-> /<slug>/, same as the original WordPress permalinks)
templates/           layouts + components (header, footer, hero, forms, weather, storm cards…)
includes/            config.php, functions, SEO/schema, form security + PHPMailer, weather + storm data
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
sh tools/package.sh                            # build dist/mcallenpublicadjuster-public_html.zip
```

Content rules for writers are in `tools/CONTENT_SPEC.md`; verified storm facts in `tools/notes/storm-facts.md`.
