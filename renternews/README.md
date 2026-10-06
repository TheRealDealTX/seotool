# renternews.net — static rebuild

A modern, static rebuild of [renternews.net](https://renternews.net), replacing
the WordPress/Elementor site on Hostinger (Cloud Enterprise, `u401386392`,
`/home/u401386392/domains/renternews.net/public_html`).

```sh
python3 build.py      # writes the whole site into ./public
python3 validate.py   # legacy URLs, links, schema, titles, XML
```

Standard library only, plus Pillow for `tools/covers.py`. **`public/` is the
deliverable**: upload its contents to `public_html`.

## What's in it

| | |
| --- | --- |
| **51 articles** | The 28 original WordPress posts (same `/news/<slug>/` URLs, same images under `/wp-content/uploads/`), plus 23 new, sourced articles from Aug–Oct 2026: 8 apartment fire/safety reports, 8 rent-market and policy stories, 7 renter guides |
| **Sections** | `/news/` plus `/news/category/{fire,safety,rent-prices,housing-policy,tenant-rights,guides}/`, paginated WordPress-style (`/page/2/`) |
| **Live weather** | `/weather/`: city search, geolocation, °F/°C, current conditions with animated sky, 24-hour chart, 7-day forecast, AQI, NWS alerts and renter tips (Open-Meteo + api.weather.gov, no keys). A mini widget sits in the top bar, sidebar and homepage |
| **Renter tools** | `/tools/`: rent affordability, roommate rent split, rent increase, move-in cost, rent vs. buy, renters insurance coverage, lease notice date (.ics export), fire safety checklist |
| **Fire map** | `/fire-map/`: Leaflet + OpenStreetMap map of every incident covered, filterable by type and year |
| **Search** | `/search/?q=` over a JSON index; old `/?s=` links redirect there |
| **Pages** | About, Contact (working form → `contact.php` → info@renternews.net), FAQs, Privacy, Terms (originals kept), plus new Editorial Policy, Corrections Policy and an author page |

Design: brand blue/gold from the logo, Fraunces + Inter, light/dark mode, a
breaking-news ticker, animated gradient heroes, scroll reveals, card hover
effects, reading progress bar and cross-page view transitions. Original
partner offers (renters insurance, credit score) are kept and labeled
*Sponsored*.

## Google News readiness

- `NewsArticle` JSON-LD on every article (headline, image, dates, author,
  publisher, section, location, citations); `NewsMediaOrganization` with
  `publishingPrinciples` and `correctionsPolicy`
- `news-sitemap.xml` (articles from the last 48 hours, per Google's spec — so
  **rebuild and redeploy whenever you publish**), plus the original Yoast
  sitemap names: `sitemap_index.xml`, `post-sitemap.xml`, `page-sitemap.xml`,
  `category-sitemap.xml`
- RSS at `/feed/`, visible bylines and dates, editorial and corrections
  policies, contact page, `max-image-preview:large`
- Remaining steps that only the owner can do: submit the site in
  [Google Publisher Center](https://publishercenter.google.com/), and
  resubmit `sitemap_index.xml` and `news-sitemap.xml` in Search Console.
  Google weighs real, named authors with bios; consider replacing the
  "Renter News Staff" byline with named reporters.

## Publishing a new article

Drop a JSON file (one object or a list) into `content/articles/`:

```json
{"slug": "my-story", "title": "Headline", "description": "140–160 chars",
 "category": "fire", "date": "2026-10-07", "city": "Austin, TX",
 "tags": ["..."], "key_points": ["..."], "body_html": "<p>…</p><h2>…</h2>",
 "sources": [{"name": "Austin Fire Department", "url": "https://…"}]}
```

Then `python3 tools/geocode.py` (if the city is new), `python3 build.py`,
`python3 validate.py`, and upload. `build.py` draws an original cover image
for any article without one (`static/assets/img/covers/<slug>.webp`); set
`"image"` to use your own photo instead.

## URL preservation

`content/legacy_urls.txt` lists every URL from the WordPress sitemaps and the
whole media library; `validate.py` fails if any is missing. The generated
`.htaccess` (from `templates/htaccess`) also maps `/?p=<id>` and
`/?page_id=<id>` shortlinks to their articles, `/feed/` to the RSS file,
the old author archive to the new author page, `/page/N/` to `/news/page/N/`,
and forces `https://renternews.net`.

## Deploying (not done yet)

1. **Back up WordPress first** (hPanel → Files → Backups, or download
   `public_html` and export the database).
2. Move the WordPress files out of `public_html` (keep them in a folder
   outside the web root until the new site is verified).
3. Upload the contents of `public/` into `public_html` (File Manager, FTP or
   Git deploy). Keep the Google verification files and anything else at the root
   not created by WordPress.
4. Clear the Hostinger/LiteSpeed cache and spot-check a few old URLs.
