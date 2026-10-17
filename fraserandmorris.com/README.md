# fraserandmorris.com — expired-domain rebuild

Static rebuild of the expired garden-design domain fraserandmorris.com, styled as a
modern plant-led garden design studio. HTML, one CSS file, one JS file and local
WebP images, with a small PHP front controller and a contact form handler.

**Live:** https://fraserandmorris.com (Hostinger Agency Growth plan, website UID
`haI1jJ1FP`, UK datacenter, PHP 8.3). Google Analytics 4: `G-NV7KRXJDDG`.
Search Console HTML-file verification: `googlecccfbf2f7e9e5ae4.html` (keep it).

## Rebuilt URLs

Every URL from the old site that ranked (Semrush organic positions, July 2017) or
carries backlinks is rebuilt at its **exact old path**:

| URL | Topic / target keyword | Why |
| --- | --- | --- |
| `/` | garden design london, fraser morris | 974 backlinks, brand rankings |
| `/about.html` | studio / approach | Backlink (The Guardian) |
| `/contact.html` | contact | Ranked (camberwell grove london) |
| `/services.html` | garden design services | Archived page |
| `/gardens.html` | garden types overview | Ranked (fraser and fraser london) |
| `/gardens/courtyard.html` | courtyard garden design | Ranked |
| `/gardens/courtyard/courtyard2.jpg` | image | 2 backlinks, now a real courtyard photo |
| `/gardens/belsize.html` | town garden design | Ranked #22–26 |
| `/gardens/highgate.html` | family garden design | Ranked |
| `/gardens/family.html` | garden design oxfordshire | Ranked |
| `/gardens/country.html` | architectural planting | Ranked |
| `/gardens/fox.html` | internal / lush garden design, garden designers south london | Ranked |
| `/gardens/artists.html` | atmospheric (artist's garden) planting | Ranked |
| `/gardens/study.html` | study garden design | Ranked |
| `/gardens/print.html` | house garden design | Ranked |

## Blog

`/blog/` lists eight garden design articles at `/blog/<slug>.html`, published
three days apart (21 Sep to 12 Oct 2026). Copy lives in `content_blog.py`. To add
a post, append an entry with a `date` three days after the newest one, then rebuild
(`validate.py` enforces the three-day spacing). Each post gets `BlogPosting`
schema, a link to a related garden page, previous/next links and its own sitemap
`lastmod`. The index has category filters; posts have a reading-progress bar.

`index.php` 301s `/index.html`, `/gardens/` and similar old paths. Note: the host
serves static file extensions (`.pdf`, `.jpg`) itself and never passes them to
PHP, so `/pdfs/GardensIllustrated.pdf` (old ranking, no traffic, no backlinks)
returns 404.

Content is written fresh. It does not name or claim to be the original
partners, and does not present their past client projects as this site's work.
The garden pages describe how each type of garden is designed.

## Files

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, page templates, schema (`python3 build.py`) |
| `content.py` | Copy for the nine garden pages and the homepage FAQ |
| `content_blog.py` | Blog articles (dated three days apart) |
| `validate.py` | Post-build checks: one H1, unique titles and descriptions, JSON-LD, alt text, broken links, legacy URLs |
| `assets/css/site.css`, `assets/js/site.js` | Styles and behavior (mobile nav, reveals, parallax, petals, seasons tabs) |
| `assets/img/*.webp` | Royalty-free photos (Pexels license), resized and converted |
| `_pages/` | Built pages as guarded PHP (generated; served only via `index.php`) |
| `index.php` | Router: https + bare-domain 301s, serves `_pages/`, legacy 301s, real 404s, `noindex` header on non-production hosts |
| `contact.php` | Form handler; emails enquiries to info@fraserandmorris.com |
| `deploy.sh` | Uploads the build through the Hostinger File Browser TUS API |

## Hosting: why pages live in `_pages/`

The host serves any file that exists directly (ignoring `.htaccess`) and only
routes unknown paths to `index.php`. Static `.html` files therefore could not be
301-redirected from `http://` or `www.` (79 old backlinks use `http://www.`), and
were sent with a one-year cache header. So `build.py` writes every page to
`_pages/<url>.php` behind a guard (direct requests get a 404) and `index.php`
serves them. That gives one canonical origin (`https://fraserandmorris.com`, 301
from http and www), real 404s, legacy redirects, and sensible cache and security
headers. `validate.py` fails if a static `.html` file reappears; `deploy.sh`
prunes old `.html` files from the server. `gardens/index.php` exists only because
`/gardens/` is a real folder (it holds `courtyard/courtyard2.jpg`).

**`https://www.` certificate:** the platform certificate covers only
`fraserandmorris.com`; Hostinger will not attach `www` as a separate domain on the
agency plan. `http://www.` redirects correctly. To cover `https://www.` too,
reinstall the SSL certificate in hPanel (the www CNAME is in place now, so the new
certificate should include it).

## SEO

- One H1, unique title (25 to 65 characters) and description (110 to 165) per page,
  all enforced by `validate.py`.
- Canonical, Open Graph (1200×630 JPG in `assets/img/og/`) and Twitter tags.
- JSON-LD graph: `ProfessionalService`/`LocalBusiness`, `WebSite`, `WebPage`, plus
  `BreadcrumbList`, `Service`, `FAQPage`, `Blog`/`BlogPosting` and `ItemList` as relevant.
- `sitemap.xml` with `lastmod` and image entries; `robots.txt` points to it.
- Responsive images (`-800.webp` variants with `srcset`), hero image preload,
  lazy loading below the fold, width/height on every image.
- Favicon set: `favicon.ico`, `favicon.svg`, `favicon-96x96.png`,
  `apple-touch-icon.png`, `site.webmanifest` with 192/512 icons.
- Google tag first in `<head>` on every page (checked by `validate.py`).
- Garden pages link to related blog posts and vice versa.

## Notes

- The frosted header background is on `.site-header::before`, not the header
  itself. A `backdrop-filter` on the header would become the containing block for
  the fixed mobile menu and clip it to the header bar once the page is scrolled.
- CSS and JS links carry a content-hash `?v=` so the Hostinger CDN never serves a
  stale copy after a deploy.

## Build & deploy

```sh
python3 build.py && python3 validate.py
export FM_FB_URL=... FM_FB_AUTH=... FM_FB_REST=...   # from agency-hosting_files_generate-upload-url
./deploy.sh
```

## Going live on fraserandmorris.com

1. Attach the domain to website `haI1jJ1FP` (`agency-hosting_domains_change-website`
   or hPanel) and point DNS at Hostinger.
2. Canonicals, Open Graph URLs and the sitemap already use `https://fraserandmorris.com`.
   The `X-Robots-Tag: noindex` header stops automatically once the site is served
   on fraserandmorris.com, and `index.php` 301s `www.` to the bare domain.
3. Create the `info@fraserandmorris.com` mailbox so form enquiries are delivered,
   and send a test enquiry.
4. Submit `sitemap.xml` in Google Search Console.
