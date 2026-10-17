# customsouthernco.com — static rebuild

A static rebuild of the expired vintage/DIY blog **Custom Southern Co.**
(customsouthernco.com). It runs on the same plain-PHP Hostinger pattern as the
huttoroofs.com site in the repo root: static HTML, one CSS file, two small JS
files, local WebP images and a tiny `index.php` front controller.

| Path | What it is |
| --- | --- |
| `site/` | **The deliverable.** Upload its contents to `public_html/`. Generated, committed |
| `build.py` | Generator: layout, post/category/tool/static pages, schema, sitemap, icons |
| `siteconfig.py` | Brand, categories, season tags, tools, nav |
| `content/posts_*.py` | Article copy (`POSTS` lists). `content/SPEC.md` is the writer brief |
| `assets/css/site.css` | Stylesheet (Fraunces + DM Sans, cream/forest/rust palette) |
| `assets/js/site.js` | Sticky header, mobile nav, scroll reveal, parallax, TOC, tabs, blog filter, contact form |
| `assets/js/tools.js` | The four interactive tools |
| `assets/img/` | CC0 / public-domain photos as WebP (`KEY.webp` + `KEY-sm.webp`); `SOURCES.json` records origins, not published |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads `site/` through the Hostinger File Browser API |

```sh
python3 build.py && python3 validate.py     # needs Pillow (image sizes, favicons)
cd site && php -S localhost:8000 index.php  # preview with the front controller
```

## What was rebuilt

Every URL that had organic traffic (Semrush, Sept 2023) or backlinks keeps its
exact old slug at the site root, e.g. `/history-of-prince-albert-tins/` (≈95 %
of the old traffic), `/how-to-make-laundry-detergent-with-3-ingredients/`,
`/how-to-repurpose-antique-light-globes/` and `/easy-vintage-cutting-board-decor/`
(the most-linked inner pages). 31 legacy posts plus 8 new articles: Ball jar
dating, tobacco tin values, rust removal, estate sales, spotting reproductions,
fabric softener, chalk-paint distressing and porch decor. `validate.py` fails
the build if a legacy URL goes missing.

`index.php` 301s the old short links (`/d05b`, `/u2ur`), WordPress paths
(`/wp-content/…`, `/feed/`, `/tag/…`, date archives) and `http`/`www` to the
canonical `https://customsouthernco.com`.

Interactive tools (each a page under `/tools/` and embedded in related posts):
Prince Albert tin dater, Ball jar age finder, DIY laundry detergent calculator
and DIY project finder.

The old site's author is not named anywhere; the byline is "The Custom Southern
Co. Team". The contact address is info@customsouthernco.com. The contact form
posts to `contact.php`, which uses PHP `mail()`, so it starts delivering once
that mailbox exists.

## Hosting

Hostinger Agency Growth plan, website UID `Zyl2IapmX` (php-fpm 8.3), created
2026-10-17 with the domain customsouthernco.com, which is not connected yet.
Point the domain's DNS at Hostinger to go live. As with huttoroofs.com there is
deliberately **no `index.html`**. The homepage is `home.html`, served by
`index.php`.
