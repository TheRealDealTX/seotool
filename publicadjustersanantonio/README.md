# PublicAdjusterSanAntonio.com — website source

Complete rebuild of https://publicadjustersanantonio.com/ (San Antonio Public Adjuster) as a fast,
dependency-free custom PHP site for Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`).
No database, no WordPress, no API keys. Same engine as the McAllen Public Adjuster rebuild,
re-themed (olive / tan / sage / cream, modern effects) and rewritten for San Antonio and Bexar County.

| Path | What it is |
|---|---|
| `dist/publicadjustersanantonio-public_html.zip` | Upload-ready package — extract into `public_html` (build with `sh tools/package.sh`) |
| `INSTALL-HOSTINGER.md` | Install, SMTP, cron, HTTPS, testing, launch |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Build/test scripts, content spec, storm and building-code notes, original-site archive (not uploaded) |

## Key settings (`site/includes/config.php`)

* Every form (5-second popup, homepage, contact, Free Claim Review) is emailed to **info@publicadjustersanantonio.com**.
* Joseph Dittman's direct email **jditt@risepublicadjusting.com** is shown on the homepage, contact, about,
  author, and footer (shortcode `[[joseph-email]]` in content).
* Phone +1 (832) 503-5866, TDI license #3356839 (Rise Public Adjusting LLC).
* Weather: NWS station KSAT (San Antonio International Airport), forecast office EWX; storm history from
  NOAA NCEI for Bexar County (1,525 events, refreshed weekly by cron); places/ZIPs from the 2024 Census Gazetteer.
* The SMTP password goes in a private `spa-config.php` above `public_html` (see INSTALL guide).

## URLs

All 16 original URLs are kept (homepage, 6 pages, 8 articles, plus `/category/general/` → `/blog/`),
original images stay at their `/wp-content/uploads/...` paths, and WordPress shortlinks/sitemaps 301 to the new pages.
New: 17 service pages, 7 new articles (15 total, all by Joseph Dittman), FAQ, 9 area pages, claim calculator,
documentation checklist, storm lookup, live weather, storm history, weather events, building codes, author page.

## Local development

```sh
sh tools/test/serve.sh                                 # PHP dev server on http://127.0.0.1:8081
python3 tools/test/crawl.py                            # SEO + link crawl of every page
NODE_PATH=$(npm root -g) node tools/test/functional.js # browser tests (Playwright)
python3 tools/build_images.py                          # featured images + responsive variants
sh tools/package.sh                                    # build the upload ZIP
```

Content rules for writers: `tools/CONTENT_SPEC.md`. Verified storm facts: `tools/notes/storm-facts.md`.
