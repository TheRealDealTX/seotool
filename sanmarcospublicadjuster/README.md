# SanMarcosPublicAdjuster.com — website source

Complete rebuild of https://sanmarcospublicadjuster.com/ (San Marcos Public Adjuster) as a fast,
dependency-free custom PHP site for Hostinger shared hosting (PHP 8.2+, Apache/LiteSpeed, `.htaccess`).
No database, no WordPress, no API keys. Same engine as the McAllen and San Antonio Public Adjuster
rebuilds, re-themed in the original San Marcos colors (navy #2A3044, green #00AC23, cream) with modern
effects (animated gradient orbs, river-wave hero edge, glass cards, cursor spotlight, scroll progress,
counters, storm-milestone timeline), and rewritten for San Marcos and Hays County.

| Path | What it is |
|---|---|
| `dist/sanmarcospublicadjuster-public_html.zip` | Upload-ready package — extract into `public_html` (build with `sh tools/package.sh`) |
| `INSTALL-HOSTINGER.md` | Install, SMTP, cron, HTTPS, testing, launch |
| `site/` | The website (what the ZIP contains) |
| `tools/` | Build/test scripts, content spec, verified local/storm facts, original-site archive (not uploaded) |

## Key settings (`site/includes/config.php`)

* Every form (5-second popup, homepage hero + form, contact, Free Claim Review) is emailed to
  **info@sanmarcospublicadjuster.com**, which is also the only email shown on the site.
* Phone +1 (832) 503-5866, TDI license #3356839 (Rise Public Adjusting LLC). Google tag G-7X0T39TV8P (from the old site).
* Weather: NWS station KHYI (San Marcos Regional Airport), forecast office EWX; storm history from
  NOAA NCEI for Hays County (502 events 1953–2026, refreshed weekly by cron); NWS Local Storm Reports
  hourly; places/ZIPs from the 2024 Census Gazetteer.
* The SMTP password goes in a private `smpa-config.php` above `public_html` (see INSTALL guide).

## URLs

Every original URL is kept: homepage, `/about-us/`, `/services/`, `/contact/`, `/blog/`, `/privacy-policy/`,
`/terms-of-use/`, and the three posts (`/roof-damage-public-adjuster/`, `/do-i-need-a-public-adjuster/`,
`/after-the-flames-insurance-adjuster/`), all rewritten by Joseph Dittman. The five old image-attachment
URLs that Google could see (`/what-is-a-public-adjuster-and-how-to-hire-one/`, `/what-is-a-public-claims-adjuster/`,
`/how-to-find-a-public-adjuster/`, `/when-is-it-too-late-to-hire-a-public-adjuster/`, `/are-public-adjusters-worth-it/`)
are now full articles. Other attachment pages, `/category/general/`, the author archive, WordPress shortlinks
(`?p=`, `?page_id=`, `?attachment_id=`) and Yoast sitemaps 301 to the right new page. Original images stay at
their `/wp-content/uploads/...` paths.

New: 17 service pages, 12 more articles (20 total), FAQ, 8 area pages (Kyle, Buda, Wimberley, Dripping Springs,
New Braunfels, Lockhart, Seguin, Martindale), claim calculator, documentation checklist, storm lookup map,
live weather, storm history, weather events, San Marcos building codes, author page, HTML sitemap.

## Local development

```sh
sh tools/test/serve.sh                                 # PHP dev server on http://127.0.0.1:8081
python3 tools/test/crawl.py                            # SEO + link crawl of every page
NODE_PATH=$(npm root -g) node tools/test/functional.js # browser tests (Playwright)
python3 tools/build_images.py                          # featured images + responsive variants
sh tools/package.sh                                    # build the upload ZIP
```

Content rules for writers: `tools/CONTENT_SPEC.md`. Verified facts: `tools/notes/local-facts.md`,
`tools/notes/storm-facts.md`; photo list: `tools/notes/photos.md`.
