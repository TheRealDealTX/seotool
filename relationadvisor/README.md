# relationadvisor.com — rebuild

A static rebuild of the expired relationship-advice blog **relationadvisor.com**
(a WordPress/HitMag site, 2018–2021), redesigned from scratch. Plain HTML, one
CSS file, one JS file, local WebP photos and two small PHP files.

**Live:** https://relationadvisor.com (launched 2026-10-16) — Hostinger Agency
Growth website UID `28XI7AXR5` (php-fpm 8.3, Phoenix datacenter; preview domain
pink-mouse-436843.hostingersite.com). Google Analytics 4 `G-T8DR7RLN6E` is on every
page; Search Console is verified with `googlecccfbf2f7e9e5ae4.html` (in `static/`).

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator — layout, page templates, schema, redirects. Writes `public/` |
| `validate.py` | Post-build checks; pass a base URL to also test every archived URL |
| `deploy.sh` | Uploads `public/` to the Hostinger website via the File Browser TUS API |
| `content/posts/*.json` | The 127 articles (format in `content/CONTENT_SPEC.md`) |
| `content/plan.json` | Slug → category assignment (and the old titles/outlines) |
| `content/old-urls.txt`, `content/old-tags.txt` | URLs found for the old site in Common Crawl (2019–2021) |
| `assets/` | `css/site.css`, `js/site.js`, `img/*.webp` (+ `images.json`: alt text and Unsplash source of each photo) |
| `static/` | Favicons / app icons copied to the site root |
| `public/` | Build output (git-ignored) — this is what gets deployed |

```sh
python3 build.py                 # production build (default)
python3 validate.py              # content + output + SEO checks
STAGING=1 python3 build.py       # noindex preview build
```

Local preview with routing: `php -S 127.0.0.1:8765 -t public <router>` where the
router serves existing files and hands everything else to `public/index.php`.

## What was rebuilt

The Wayback Machine is not reachable from the build environment and Semrush
had no API units, so the page inventory came from **Common Crawl**: 241 unique
URLs captured between 2019 and 2021 — 118 articles, 6 category archives,
92 tag archives, author pages and pagination.

- **All 118 archived article URLs** are rebuilt at the same slug with fresh,
  original copy (the old text was not reused). Manipulative angles in some old
  posts were reframed toward honest, consent-based advice; abuse-related posts
  carry the National DV Hotline.
- **All 6 old category URLs** (`relationships`, `pickup-lines`, `quotes`,
  `captions`, `wedding`, `zodiac`) are live hubs, plus three new ones
  (`dating`, `breakups`, `questions`) to split the oversized Relationships archive.
- **9 new posts** fill the formerly empty Wedding/Zodiac/Captions/Quotes hubs.
- **Every other archived URL 301s** (handled in the generated `index.php`):
  tags → closest article (hand-tuned in `TAG_OVERRIDES`), authors → `/about/`,
  `/category/x/page/N/` → `/category/x/`, feeds → home, old malformed URLs →
  the right article, slugs without a trailing slash → with one.
  `validate.py <base-url>` confirms all 241 resolve to a 200.

Pages also new: `/blog/` (filterable library + search), `/about/`, `/contact/`,
`/privacy-policy/`, `/terms-of-use/`, `/disclaimer/`, `/sitemap/`, `404`.

## Design

Plum ink, rose→coral gradient and cream; Fraunces + Plus Jakarta Sans. Effects:
animated gradient blobs and floating hearts in the hero, rotating headline word,
tilted marquee, scroll reveals, 3D card tilt, image zoom on hover, reading
progress bar, sticky table of contents with scroll-spy, one-tap copy on every
line/question/note, "line of the day" shuffler, animated counters, stage tabs,
live search. All motion respects `prefers-reduced-motion`.

Mobile nav: slide-in drawer with overlay, body scroll lock, focus trap,
Escape/overlay/link closes it, accordion Topics submenu. (The header's
`backdrop-filter` is disabled under 980px because it would otherwise become the
containing block of the fixed drawer and clip it.)

## Hosting notes

Same platform behavior as huttoroofs.com: existing files are served directly,
`.htaccess` is ignored, and unknown paths go to `index.php`. So there is **no
root `index.html`** — the homepage is `home.html`, served by `index.php` for `/`.
The placeholder `default.php` Hostinger creates on a new site was deleted.

`contact.php` emails form submissions to **info@relationadvisor.com** with
PHP `mail()` (honeypot + minimum-time spam checks). It will only deliver once
that mailbox exists.

## SEO setup

- Unique title/description per page (descriptions clipped to 160 chars at a word
  boundary), one H1, canonical to `https://relationadvisor.com/…`, `index, follow,
  max-image-preview:large`.
- Open Graph + Twitter cards with 1200×630 JPEG share images generated from the
  page photo (`public/assets/og/`), `og:locale`, `article:*` times and section.
- JSON-LD: Organization, WebSite + SearchAction, BlogPosting (ImageObject, stable
  `datePublished` = relaunch date), BreadcrumbList, FAQPage, CollectionPage/ItemList.
- `sitemap.xml` with image entries, `feed.xml` (RSS; old `/feed/` 301s to it),
  `robots.txt` with the sitemap. LCP photo preloaded on every page.
- Favicons: `favicon.ico`, `favicon.svg`, `favicon-96x96.png`, `apple-touch-icon.png`,
  web-app manifest icons.
- Backlinks (DataForSEO, Oct 2026): 12 pages on the domain have links; all
  resolve. `/flirty-questions-to-ask-a-boy/` was not in Common Crawl and was added.
  The homepage's ~1,560 referring domains are mostly spammy cheap-TLD links
  (spam score 53) built while the domain redirected elsewhere.

Lighthouse (desktop, live): SEO 100, Best Practices 100, Performance 88, Accessibility 96–97.

## Open items

- `https://www.relationadvisor.com` has no SSL certificate (the platform rejects
  linking `www` via the API). `http://www` already 301s to the apex. Fix in hPanel
  (SSL → include www) so https://www links don't show a certificate error.
