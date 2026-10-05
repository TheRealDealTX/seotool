# beltonbanners.com — Christina Dittman Creations ("Belton Banners")

A custom HTML/PHP rebuild of [beltonbanners.com](https://beltonbanners.com),
replacing the WordPress/Elementor site. No CMS, no database, no plugins: a
Python generator writes plain HTML, a ten-line `index.php` fronts it on the
host, and `contact.php` handles every form on the site.

## What's here

| Path | What it is |
| --- | --- |
| `home.html`, `*/index.html`, `404.html` | The generated site — the deliverable |
| `index.php` | Front controller for the Hostinger H5G host: serves `/`, 301s the old WordPress-only URLs, real 404s for everything else |
| `contact.php` | Quote/contact form handler (validation, honeypot, `mail()` to the studio, private log copy) |
| `assets/css/site.css` | The single stylesheet (tokens, layout, components, effects, responsive, reduced-motion) |
| `assets/js/site.js` | Site behavior: sticky header, mobile nav, scroll reveals, parallax, counters, tilt, paint-trail cursor, gallery strip, filters, lightbox, the banner designer, AJAX forms |
| `assets/img/brand/` | The original logo (kept), OG image, generated kraft/paper textures |
| `assets/img/gallery/` | The 17 gallery photos + hero and blog images at 1600/800/400 px |
| `wp-content/uploads/2026/03/` | The old WordPress media library at its original URLs (originals + the resized variants the old pages referenced), so every old image URL still returns 200 |
| `favicon.*`, `apple-touch-icon.png`, `web-app-manifest-*.png`, `site.webmanifest` | Icons generated from the logo |
| `build.py` | Generator: shared layout, page builders, JSON-LD, sitemap, robots, manifest |
| `siteconfig.py` | Business details, keyword strings, sizes, navigation |
| `content/` | Page data: `creations.py` (gallery), `occasions.py` (banner-type pages), `blog.py` (posts), `legal.py` |
| `validate.py` | Post-build checks (run after every build) |
| `deploy.sh` | Uploads the build to the Hostinger website through its File Browser API |
| `backup/wordpress-2026-10-05/` | The WordPress site as it was: rendered HTML of every URL, REST API exports, Yoast sitemaps |

## Rebuilding

```sh
python3 build.py      # regenerate every HTML file (+ sitemap.xml, robots.txt, manifest)
python3 validate.py   # verify the output
```

Python 3 standard library only (Pillow was used once to render the image
sizes and favicons; they are committed). Preview locally with PHP so the front
controller and the form handler run:

```sh
php -S 127.0.0.1:8085 /path/to/router.php   # see "Hosting note" — or open /home.html statically
```

## URLs

Every URL the WordPress site published is kept (checked by `validate.py`):

- `/`, `/about-christina-dittman-creations/`, `/contact-us/`, `/gallery/`, `/privacy-policy/`, `/blog/`
- `/hand-painted-banner/` — the original post, word for word
- `/creation/<slug>/` — all 17 gallery pieces, same slugs, same order, same starting prices
- `/category/general/` — kept as a listing (noindex)
- `/sitemap_index.xml` (now points at `/sitemap.xml`); `post-/page-/creation-/category-sitemap.xml` 301 to `/sitemap.xml`
- `/banner-type/hand-painted-banners/` → `/gallery/`; feeds → `/blog/`; attachment pages → their creation; `wp-admin` etc. → `/`

New pages:

- `/custom-banners/` + six banner-type pages: `birthday-banners`, `wedding-banners`, `baby-shower-banners`, `church-banners`, `graduation-banners`, `holiday-seasonal-banners`
- `/how-it-works/`, `/pricing-and-sizes/`, `/faq/`, `/design-your-banner/`, `/belton-banners/` (local landing page), `/terms-of-use/`, `/sitemap/`, `/thank-you/` (noindex)
- Two new posts: `/custom-birthday-banner-ideas/`, `/church-banner-ideas/`

## SEO

Primary keyword **belton banners**; brand keyword **Christina Dittman Creations**.
The homepage title is `Belton Banners | Christina Dittman Creations | Hand-Painted in Belton, TX`
and the body mentions "Belton Banners" 29 times (validate.py enforces ≥ 14) and the
brand 16 times. Every page has a unique title and description, one H1, canonical,
Open Graph/Twitter tags and JSON-LD: `LocalBusiness` (alternateName "Belton Banners")
+ `WebSite` on every page, plus `Product` for creations, `Service` + `FAQPage` for
banner types, `BlogPosting` + `FAQPage` for posts, `HowTo` on the process page,
`BreadcrumbList` on interior pages, `ItemList` on collections.

## Interactive and visual features

- **Banner designer** (home, `/design-your-banner/`, process and pricing pages): occasion
  presets, wording, lettering style, paper, ink color, motif, size and "wobble"; live
  preview; "Send this design for a quote" fills the contact form (or carries the design
  to `/contact-us/` through sessionStorage).
- Hero with parallax background, word-by-word title animation, animated brush-stroke
  underline, animated counters, and a paint-splatter cursor trail (pointer devices only).
- Scroll-reveal with stagger on every section, brush-reveal (clip-path) image frames,
  scroll progress bar, blurred sticky header, marquee strip, tilt cards.
- Gallery: category filters (deep-linkable with `#birthday` etc.), lightbox with
  keyboard and swipe, draggable scroll-snap strip on the homepage.
- FAQ accordions, copy-link buttons, AJAX forms with inline status.
- Everything respects `prefers-reduced-motion`; every page works without JavaScript.

## Forms

All forms post to `/contact.php`, which emails `dittmanbanners@gmail.com`
(From `noreply@beltonbanners.com`, Reply-To the sender) and appends a copy to
`../inquiries/inquiries-YYYY-MM.txt` outside the document root. With JavaScript
the response is JSON and shown inline; without it, the browser lands on
`/thank-you/`. **Confirm an email actually arrives in the Gmail inbox** (and the
spam folder) after the first real submission; the handler returns success when
either the mail was accepted or the log copy was written.

## Hosting note

The site runs on Hostinger Agency website **`duFSuwfQj`** (plain php-fpm, PHP 8.5,
Phoenix), created 2026-10-05. `beltonbanners.com` was moved to it from the
WordPress website `yC3Lm7xR9`, which still exists untouched on
`lavenderblush-fly-932440.hostingersite.com` as the rollback (link the domain
back to it to revert). Delete it once the new site has been live for a while.

The platform serves existing files directly, ignores `.htaccess`, and routes
`/` and unknown paths to `index.php` — unless an `index.html` exists at the
root. So the homepage is `home.html` served by `index.php` for `/` (and
`home.html` is `Disallow`ed in robots.txt). Missing files inside existing
directories are 404'd by the platform itself, which is why the resized media
variants are real files rather than `index.php` rewrites.

## Deploying

```sh
python3 build.py && python3 validate.py && ./deploy.sh
```

`deploy.sh` needs the three File Browser credentials from
`agency-hosting_files_generate-upload-url` (see its header). Clear the site
cache afterwards (`agency-hosting_cache_clear-website`).

Deployed 2026-10-05 (145 site files + 113 media files).
