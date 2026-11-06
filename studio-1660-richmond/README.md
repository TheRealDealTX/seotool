# Studio at 1660 Richmond: concept site

A static pitch site (plain HTML/CSS/JS, no framework) for Studio at 1660 Richmond, a 16-unit studio courtyard building at 1660 Richmond Ave, Houston, TX 77006 (Montrose). A small `index.php` beside each page only sets headers on Hostinger.

**Live demo (temporary Hostinger domain):** https://sandybrown-bear-867005.hostingersite.com

Built on the Los Arcos demo's build system (`los-arcos/` on branch `claude/modest-brahmagupta-ccoj6j`), with a new design: pool teal, ochre and gallery-paper palette, Bricolage Grotesque with Instrument Sans and Instrument Serif italics, and a mid-century breeze-block motif taken from the building's courtyard screen wall.

## Build and check

```bash
pip install pillow        # only dependency (reads image sizes)
python3 build.py          # writes the finished site to ./dist
python3 check.py          # links, assets, titles/descriptions, noindex, JSON-LD, name count
```

- `build.py` holds all page content, the property facts (`P`), the FAQs (also used for FAQPage schema), the schema and the shared header and footer.
- `src/css/style.css` is the design system. Tokens are at the top; the advanced-effects layer is at the bottom, and all of it is disabled under `prefers-reduced-motion`.
- `src/js/main.js` holds every interaction: menu, hero slideshow, word reveals, clip reveals, counters, spotlight and tilt cards, magnetic buttons, progress bar, smart header, lazy map, gallery filters and lightbox, contact tabs and forms.
- `images.json` and `IMAGES.md` list every image with its source and where it appears.
- Fonts are self-hosted and subset to Latin (`src/fonts`, 77 KB total). Bricolage is instanced at opsz 60, weights 500–800.

## Before going live

- Search the source for `[confirm]`. Each marker flags something to verify with the owner (rent, unit sizes, deposit, pet fees, parking, utilities, hours, schools, drive times).
- Replace the placeholder URLs at the top of `build.py`: `APPLY_URL`, `PAY_URL`, `MAINT_URL`, `PORTAL_URL`. Fat Property already runs applications and the resident portal on Buildium. Social links are in `footer()`.
- Connect the forms. See the `LEASING CRM / EMAIL HOOK` comment in `src/js/main.js`.
- Remove `<meta name="robots" content="noindex, nofollow">` from `page()`, the `X-Robots-Tag` line in the PHP templates and the disallow-all `src/robots.txt`. Remove the "Concept site" line from `footer()`.

## Deploy (Hostinger Agency plan)

1. Zip the contents of `dist/` (with `index.html` at the archive root).
2. Run `agency-hosting_files_generate-upload-url`, then TUS-upload the zip to `.h5g/<name>.zip`.
3. Run `agency-hosting_files_import-website-from-archive`.

### Platform notes

- **CDN caching.** Hostinger's CDN caches plain `.html` for a year, and `agency-hosting_cache_clear-website` doesn't reliably purge every edge. The build writes an `index.php` next to every `index.html`. Hostinger serves `index.php` first, and it returns the same HTML with `Cache-Control: no-cache` and `X-Robots-Tag: noindex, nofollow`. CSS and JS are cache-busted with `?v=<hash>`. Images keep long caching, so give a replaced photo a new file name.
- **Unknown URLs.** Hostinger answers unknown paths with the root `index.html` itself, bypassing PHP, with HTTP 200. The homepage carries a one-line guard that sends any other path to `/404.html`. Each `index.php` also returns a real 404 if PHP ever receives a path that isn't its own. A true 404 status needs a custom domain or host-level config.
- **`.htaccess`** is ignored on this platform.
- **robots.txt.** `*.hostingersite.com` serves Hostinger's own robots.txt, not ours. Ours (`Disallow: /`) takes effect on a custom domain. The `noindex` meta tag and `X-Robots-Tag` header keep the demo out of search in the meantime.
- **Mobile menu.** Never put `transform`, `filter`, `backdrop-filter` or `view-transition-name` on `.header`; it would trap the fixed mobile menu inside the header. The blur lives on `.header::before`, and the smart-hide animates `top`.
