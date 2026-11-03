# solarcctvcamera.com — custom PHP rebuild

**Solar CCTV Camera** (https://solarcctvcamera.com) rebuilt from WordPress/Elementor
into a hand-written PHP site: no CMS, no database, no plugins. One front controller,
one stylesheet, one site script and seven vanilla-JS calculators.

Live on the Hostinger Agency Growth plan, website UID `IhhWxQZAx` (php-fpm, PHP 8.3).
The old WordPress website (`f5Tzp57oS`) was backed up and deleted on 2026-11-03;
see `backup/wordpress-2026-11-03/README.md`.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | Everything deployed to `public_html` |
| `public/index.php` | Front controller: canonical host, legacy WordPress 301s, routing, sitemap.xml, 404s |
| `public/inc/routes.php` | **The URL registry** (every page once) + the redirect map + article helpers |
| `public/inc/layout.php` | `<head>`, header/nav, footer, JSON-LD Organization/WebSite, cards |
| `public/inc/article.php` | Article renderer: hero, TOC, quick answer, tool embeds, FAQ + FAQPage schema, related |
| `public/inc/contact-handler.php`, `mailer.php` | Contact form (honeypot, signed time token, JS check, link/keyword filter, rate limit) sending over SMTP |
| `public/content/*.php` | Article content: each file returns an array (title, description, h1, lede, takeaways, body HTML, faq, related) |
| `public/content/tool-*.php` | Explainer text under each tool |
| `public/pages/*.php` | Home, hubs, about, contact, legal, 404 |
| `public/pages/tools/*.widget.php` + `public/assets/js/tools/*.js` | The seven calculators |
| `public/assets/css/site.css`, `assets/js/site.js` | Design system + scroll effects |
| `tools/dev-router.php` | Local preview router |
| `tools/validate.py` | Crawls the preview and checks every page |
| `deploy.sh` | Uploads `public/` through the Hostinger File Browser API |
| `backup/` | Content-level WordPress export + the GSC report the rebuild was based on |

Every file under `inc/`, `content/` and `pages/` starts with `defined('SCC') || exit;`
and the router 404s those paths, so nothing private renders if requested directly.

## Working on it

```sh
php -S 127.0.0.1:8080 -t public tools/dev-router.php   # preview
python3 tools/validate.py                              # must print ALL OK
```

The validator checks: HTTP 200 for every sitemap URL, exactly one `<h1>`, title 25–65 and
description 110–165 characters, no duplicate titles/descriptions, self-canonical, valid JSON-LD,
alt text, every internal link/asset resolves, legacy redirects land on 200 pages, private paths 404.

**Add an article:** create `public/content/<slug>.php` (copy any existing one), add one line to
`routes()` in `public/inc/routes.php`, run the validator. Hubs, related links, sitemap.xml and
the HTML sitemap pick it up automatically. Put `<!--tool:ID-->` in a body to embed a calculator
(IDs: `panel-angle battery planner site-check data coverage cost`).

**Deploy:** get credentials from the Hostinger API op `agency-hosting_files_generate-upload-url`
(website `IhhWxQZAx`), export `FB_URL`/`FB_AUTH`/`FB_REST`, run `./deploy.sh` (or
`./deploy.sh public/path/file …` for single files), then clear the cache with
`agency-hosting_cache_clear-website`.

## Private config (not in git)

`public_html/inc/config.local.php` on the server holds the SMTP password and the form-signing
secret (`smtp_host`, `smtp_port`, `smtp_user`, `smtp_pass`, `form_secret`). It is git-ignored,
guarded like every other include, and `deploy.sh` never overwrites it. The platform does not allow
writing outside `public_html` (other than `.h5g/`), so it lives in `inc/`. If the mailbox password
changes, edit that file in hPanel’s File Manager.

## SEO decisions

Based on the Search Console export in `backup/gsc-performance-2026-11-03.xlsx` (last 6 months:
920 impressions, 5 clicks):

- **Doubled down** on what earned impressions: `/best-solar-security-cameras/` (385),
  `/guides/solar-camera-panel-angle/` (250, avg position 8.5; now the definitive guide plus the
  Panel Angle Calculator), `/solar-camera-installation/` (94; was almost empty, now a full guide),
  `/use-cases/solar-cameras-for-rvs/`, `/how-solar-cameras-work/`, night/Wi‑Fi guides.
- **Restored** seven pages that were deleted in June 2026 but still had impressions (driveway alert,
  gate camera, camping, street light price, rental property, remote cabin) and added a construction-site page.
- **Consolidated / removed** (all 301-redirected): duplicate “how does a solar camera work” post,
  two overlapping “are solar cameras any good” reviews (merged into “worth it”), the barn and camper
  posts (merged into farms / RVs), every thin category and tag archive, Yoast sitemaps, feeds and
  WordPress endpoints. Also removed: fabricated “14 models tested / 30-day test protocol” claims,
  fake ratings, and an auto-login PHP file left in the old web root.
- Every page: unique title/description, one H1 with its keyword, quick-answer box, self-canonical,
  Open Graph/Twitter, JSON-LD (Organization, WebSite, BreadcrumbList, Article/WebPage, FAQPage,
  WebApplication for tools, ItemList on hubs). The homepage mentions “Solar CCTV Camera” 20+ times.
- Kept: Google Search Console verification file, Google tag `GT-K54JDCWX`, Amazon affiliate links
  (tag `josephrayditt-20`, now `rel="sponsored nofollow"`).

## Known gaps

- Product specs on the buying guides are research-based and should be re-checked when models change.
- Article energy figures are labelled as illustrative; the battery calculator uses its own stated
  assumptions (~3 W active on Wi‑Fi, ~4 W on LTE).
