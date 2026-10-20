# PublicAdjustersDallas.com — website source

Complete rebuild of https://publicadjustersdallas.com/ (Dallas Public Adjuster) as a fast,
dependency-free custom PHP site for Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`).
No database, no WordPress, no API keys. Same engine as the McAllen Public Adjuster rebuild (and the
later San Antonio one), re-themed in the original Dallas brand colors — navy `#0B2D72`, blue `#0992C2`,
cyan `#0AC4E0`, cream `#F6E7BC`, green `#00AC23` — with modern effects (animated hero with storm
streaks, lightning flash and Dallas skyline, glass cards, cursor spotlight, scroll reveals, counters),
and rewritten for Dallas and Dallas County.

| Path | What it is |
|---|---|
| `dist/publicadjustersdallas-public_html.zip` | Upload-ready package — extract into `public_html` (build with `sh tools/package.sh`) |
| `INSTALL-HOSTINGER.md` | Install, SMTP, cron, HTTPS, testing, launch |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Build/test scripts, content spec, storm and building-code notes, original-site archive (not uploaded) |

## Key settings (`site/includes/config.php`)

* Every form (popup that opens 5 seconds after page load, homepage hero + form, contact, Free Claim Review)
  is emailed to **info@publicadjustersdallas.com**.
* Joseph Dittman (licensed Texas public adjuster) is the author of every article; his direct email
  **jditt@risepublicadjusting.com** is shown on the homepage, contact, about, author and footer.
* Phone +1 (832) 503-5866, TDI license #3356839 (Rise Public Adjusting LLC). Google tag G-N643D280GQ (same as the old site).
* Weather: NWS station KDAL (Dallas Love Field), forecast office FWD (Fort Worth/Dallas); storm history from
  NOAA NCEI for Dallas County (2,142 events since 1952, refreshed weekly by cron); NWS Local Storm Reports
  for recent events; places/ZIPs from the 2024 Census Gazetteer.
* The SMTP password goes in a private `pad-config.php` above `public_html` (or `includes/config.local.php`) — see the INSTALL guide.

## URLs

All original URLs are kept: homepage, `/about-us/`, `/services/`, `/blog/`, `/contact/`, `/privacy-policy/`,
`/terms-of-use/`, the 8 original articles at their exact permalinks, and `/category/general/` → `/blog/`.
Original images stay at their `/wp-content/uploads/...` paths; WordPress shortlinks (`/?p=208`), the
author archive and the Yoast sitemaps 301 to the new pages.

New: 18 service pages, 8 new articles (16 total), FAQ, Free Claim Review, author page, 10 area pages
(Highland Park, University Park, Richardson, Garland, Irving, Mesquite, Carrollton, Grand Prairie, Plano,
Rowlett), tools (claim settlement calculator, documentation checklist, storm lookup), live weather,
storm history, weather events, Dallas building codes, HTML sitemap.

## Local development

```sh
sh tools/test/serve.sh                                 # PHP dev server on http://127.0.0.1:8081
python3 tools/test/crawl.py                            # SEO + link crawl of every page (also checks the homepage keyword count ≥ 14)
NODE_PATH=$(npm root -g) node tools/test/functional.js # browser tests (Playwright)
python3 tools/build_images.py                          # featured images + responsive variants
sh tools/package.sh                                    # build the upload ZIP
```

Content rules for writers: `tools/CONTENT_SPEC.md`. Verified storm facts: `tools/notes/storm-facts.md`.
Building-code research: `tools/notes/building-codes.md`.
