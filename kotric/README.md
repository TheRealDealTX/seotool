# kotric.com: static rebuild

A rebuild of the expired domain **kotric.com**, a fabric crafts, DIY projects and sewing blog.
It's a static HTML site behind a small PHP front controller, hosted on the Hostinger Agency Growth plan.

- **Hostinger website UID:** `OZUvakKhz` (php-fpm 8.3, Boston datacenter)
- **Domain:** https://kotric.com (live)
- **Google Analytics:** G-Q1D6K5T4D2 (in every page's `<head>`)
- **Search Console:** verified by `googlecccfbf2f7e9e5ae4.html` in the web root
- **Contact email:** info@kotric.com

## Build, check and deploy

```sh
python3 build.py        # writes ./public (pages in ./public/_pages)
python3 validate.py     # links, anchors, assets, Google tag, canonicals, title/description lengths, sitemap, JSON-LD
./deploy.sh [--prune]   # see the header comment for the three upload credentials
```

Page copy lives in `content/` (`posts.py`, `posts_more.py`, `projects.py`, `pages.py`, `tools.py`).
The layout, SEO tags and sitemap are in `build.py`. Styles and scripts are `assets/css/site.css` and `assets/js/site.js`.
Root files (index.php, contact.php, robots.txt, icons) are in `static/`.

## Recovered URLs (from the backlink export)

| URL | Backlinks | Status |
| --- | --- | --- |
| `/` | 1,409 (1,368 domains) | Rebuilt homepage |
| `/no-sew-fabric-craft-projects/` | 39 (incl. engineermommy.com) | Rebuilt: "41 Amazing No-Sew DIY Fabric Projects", filterable, with a made-it tracker |
| `/4no-sew-diy-fabric-projects/` | 38 | Rebuilt: 4 step-by-step no-sew tutorials |

Note: almost all of the homepage links come from spammy auto-generated directory sites
("Premium Backlinks…" anchors). Consider a disavow file for those domains.

## SEO setup

- Titles 25–60 characters and meta descriptions 70–160 characters, both unique per page and enforced by `validate.py`.
- Canonical, Open Graph (with image size), Twitter card and article time tags, plus JSON-LD: Organization, WebSite,
  BlogPosting, Article, HowTo, ItemList, FAQPage, BreadcrumbList and WebApplication.
- `sitemap.xml` with image entries (referenced from robots.txt), and an RSS feed at `/feed/`.
- Favicons: `favicon.ico` (16/32/48), `favicon.svg`, `favicon-96x96.png`, `apple-touch-icon.png`, and web-app manifest icons at 192 and 512.

## Hosting notes

The host serves existing files directly, ignores `.htaccess`, and sends `/` and unknown paths to `index.php`.
The File Browser API can only write inside `public_html`. So the pages live in `public_html/_pages/`,
which nothing links to and robots.txt blocks, and every page URL is answered by `index.php`. That script:

- 301s `http://` and `www.` to `https://kotric.com`
- adds trailing slashes
- redirects old WordPress paths
- serves the page with ETag and Last-Modified headers
- returns real 404s

Never put an `index.html` or page directories at the root of `public_html`: the host would serve them directly
and skip those redirects. `validate.py` checks for this, and `deploy.sh --prune` removes leftovers.
`contact.php` emails info@kotric.com and keeps a copy in `../kotric-contact-messages.log`, outside the web root.

Images are CC0 photos from StockSnap and need no attribution.
