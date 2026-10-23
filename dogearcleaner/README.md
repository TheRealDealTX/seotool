# dogearcleaner.com — static HTML/PHP rebuild

Replaces the WordPress/Elementor site with a generated static site and a small
PHP front controller, hosted on the Hostinger Agency Growth plan. No database,
no plugins. All copy was rewritten for the queries in the site's Search Console
report (2026-07 to 2026-10), and every old URL still works.

## What's here

| Path | What it is |
| --- | --- |
| `site/` | **The deployable build** (upload its contents to `public_html/`) |
| `build.py` | Generator: layout, shortcodes, JSON-LD, listings, sitemap |
| `pages.py` | Homepage |
| `tools.py` | The four interactive tools (form markup and tool-page copy) |
| `products.py` | Amazon catalog: ASINs and the affiliate tag `dogearcleanerjditt-20` |
| `siteconfig.py` | Site name, nav, categories |
| `content/posts/*.html` | The 10 articles (format: `CONTENT_SPEC.md`) |
| `content/pages/*.html` | About, contact and legal pages |
| `src/` | CSS, JS, images, and root files (`index.php`, `contact-submit.php`, manifest) |
| `validate.py` | Post-build checks; run after every build |
| `deploy.sh` | Uploads `site/` through Hostinger's File Browser API |
| `backup/wordpress-2026-10-23/` | Content backup of the WordPress site (REST export, rendered pages, media) |

## Rebuild

```sh
python3 build.py && python3 validate.py
```

Python 3.12+ and Pillow (for image resizing). For a local preview with the real
PHP routing, run `php -S` with a router that falls through to `site/index.php`.

## The brief, and where it's enforced

- **Keep every URL.** All 20 URLs from the old Yoast sitemaps are rebuilt at
  the same paths, including the typo slug `/how-to-clean-dog-earss-matters/`.
  Old media URLs under `/wp-content/uploads/2026/05/` still return the original
  images. `index.php` 301s the WordPress leftovers: Yoast sitemaps go to
  `/sitemap.xml`, `/feed/` to `/resources/`, `/author/*` to `/about-us/`,
  `/category/*` to `/topic/*`, and `wp-admin` and friends to `/`. Everything
  else gets a real 404. `validate.py` fails the build if any old URL is missing.
- **Amazon links tagged `dogearcleanerjditt-20`.** Every link is built from
  `products.py`. The build has about 160 Amazon links, all `rel="nofollow
  sponsored"`. `validate.py` fails on any Amazon link without the tag. Prices
  and star ratings are never shown (Amazon Associates rules); buttons say
  "Check price on Amazon".
- **"Dog Ear Cleaner" at least 14 times on the homepage.** It's 19 in the main
  content and 23 counting the header and footer. `validate.py` counts it.
- **SEO rewrite from GSC data.** 280 of the ~350 impressions went to the
  Epi-Otic review (queries like "epi-otic reviews", "virbac epiotic ohrreiniger
  reviews", "epi clean review"). That page now targets "Epi-Otic review(s)",
  covers the international names (Epiotic, Ohrreiniger, nettoyant auriculaire,
  oorreiniger) and compares against EpiKlean. The homepage targets "dog ear
  cleaner", "ear cleanser for dogs", "dog ear care" and "dog ear rinse".

## New pages

- `/best-dog-ear-cleaner/` — 10-pick roundup ("best dog ear cleaner", 2,400/mo US)
- `/tools/` plus four tools:
  - `/tools/ear-symptom-checker/` — home care, vet this week, or vet today
  - `/tools/ear-cleaning-schedule/` — cleaning frequency, with dates you can save as a calendar file (.ics)
  - `/tools/ear-cleaner-finder/` — quiz that matches a dog to two products
  - `/tools/ear-cleaner-dose-calculator/` — mL per ear and how long a bottle lasts

The tools are also embedded in the articles (`[[tool:…]]`) and the homepage.
They run entirely in the browser.

## Hosting

- **Live website:** Hostinger Agency website UID `2PvpG8RKu` (php-fpm, PHP 8.5),
  created 2026-10-23. dogearcleaner.com was moved onto it the same day.
- **Old WordPress website:** UID `PZJDtrILR` was left in place, with its domain
  unlinked but its files and database intact. To roll back, link
  dogearcleaner.com back to it. Delete it only once you're happy with the new site.
- The platform serves existing files directly, ignores `.htaccess`, and routes
  `/` and unknown paths to `index.php`. So there is deliberately **no root
  `index.html`**: the homepage is `home.html`, served by `index.php`.
- **Contact form** (`contact-submit.php`) appends messages to
  `<website root>/.h5g/dogearcleaner-private/messages.csv`. That folder is
  outside `public_html`, isn't web-served, and can be read in hPanel's File
  Manager. To also get email, create
  `.h5g/dogearcleaner-private/config.php` containing
  `<?php return ['to' => 'you@example.com'];`.
- **Deploy:** get credentials with `agency-hosting_files_generate-upload-url`
  for `2PvpG8RKu`, export them as shown in `deploy.sh`, run it, then clear the
  cache (`agency-hosting_cache_clear-website`).

## Adding an article

Create `content/posts/<slug>.html` following `CONTENT_SPEC.md`, add the slug to
`order` in `build.py` if you want it ranked, then build, validate and deploy.
New product: add it to `products.py` and reference it with `[[product:key]]`.
