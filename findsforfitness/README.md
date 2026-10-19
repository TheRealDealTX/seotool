# findsforfitness.com — static rebuild

Rebuild of the expired findsforfitness.com fitness blog as a fast static site
(HTML + one CSS + two JS files, no database). Everything lives in this folder.

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, article/category/tool pages, schema, sitemap, `index.php`, `contact.php` |
| `siteconfig.py` | Site name, email (info@findsforfitness.com), categories, nav |
| `content/posts/*.html` | 27 articles (JSON front matter + body). Format: `content/POST_SPEC.md` |
| `content/tools.py` | 7 interactive tool pages (markup + copy) |
| `images.json` | Unsplash photo id → local file name |
| `public/` | The built site — this is what gets deployed. `public/assets/` holds the hand-written CSS/JS and images |
| `static/` | PNG icons copied into the build |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads `public/` to Hostinger |

```sh
python3 build.py && python3 validate.py   # rebuild + check
./deploy.sh                               # see header for the 3 env vars
```

## What was preserved from the old site
- **Backlinked pages, same URLs:** `/` (1,560 links), `/best-tennis-shoes-for-flat-feet/` (48),
  `/healthy-breakfast-foods-for-weight-loss/` (3) — rewritten and expanded.
- **All 17 posts found in the 2022–2024 archive**, same slugs, rewritten fresh.
- **Old category URLs**: `/category/skin_care/`, `/category/weight_loss/`, `/category/workout/`,
  `/category/health-tips/`, `/category/product-reviews/`.
- **Old pages**: `/privacy-policy/`, `/terms-of-service/`, `/affiliate-disclosure/`, `/disclaimers/`.
- **301s in `index.php`**: `/contact-us-2/` → `/contact/`, `/privacy-policy-4/` → `/privacy-policy/`,
  `/category/health_news/`, `/page/N/`, `/feed/` → `/blog/`, `wp-*` → `/`.

New: 10 articles, 7 tools (BMI, calorie/TDEE, protein, water intake + tracker, running pace,
shoe finder quiz, HIIT interval timer), blog with category filters, about/contact pages.

## Hosting
Hostinger Agency Growth, website UID `kAOBwY0ha` (php-fpm 8.3, Phoenix), domain
findsforfitness.com attached; preview at https://seagreen-stork-985978.hostingersite.com.
Same platform rules as the parent repo's huttoroofs build: no root `index.html`; `index.php`
serves `home.html` for `/`, handles redirects and returns real 404s.

`contact.php` emails info@findsforfitness.com with PHP `mail()` and appends every
submission to `form-submissions.csv` one level above `public_html`.

Photos are from Unsplash (free license), downloaded and served locally as WebP.

## SEO setup
- Google tag `G-3VM6161ZL8` is the first thing in `<head>` on every generated page (`GTAG` in `build.py`).
- Search Console HTML verification file `googlecccfbf2f7e9e5ae4.html` lives in `static/` and is copied to the site root.
- `sitemap.xml` (with image entries, stable lastmod dates), `robots.txt`, RSS at `/feed.xml` (`/feed/` 301s to it).
- Favicons: `favicon.ico` (16/32/48), SVG, 32/48/96 PNG, apple-touch-icon, 192/512 manifest icons.
- Per page: unique title + description, canonical, Open Graph + Twitter cards, `max-image-preview:large`,
  JSON-LD (Organization, WebSite, BlogPosting, BreadcrumbList, FAQPage, WebApplication, CollectionPage).
- Fonts are self-hosted and preloaded; images use `srcset` so phones load the 720px variants.
