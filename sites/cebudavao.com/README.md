# cebudavao.com — Cebu-Davao news, travel & lifestyle site

A static-HTML + small-PHP rebuild of [cebudavao.com](https://cebudavao.com),
replacing the WordPress/Elementor install. News, travel, food, culture, sports,
entertainment, money and tech, focused on Cebu and Davao, plus live weather, a
live news wire and free reader tools.

Hosted on the Hostinger Agency (Growth) plan as a plain php-fpm website,
UID `gLBQLhLT2`, same server (72.60.128.114, Phoenix) as the other sites.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator — layout, post/listing/hub/tool/weather pages, schema, sitemaps, RSS, redirect map |
| `pages.py` | About, contact, editorial policy, FAQs, privacy, terms, photo credits, HTML sitemap, 404 |
| `md.py` | Tiny Markdown renderer used for posts |
| `config.py` | Site constants, categories, nav, weather cities |
| `content/posts/*.md` | 131 articles (97 recreated legacy URLs + 34 new) — format in `content/CONTENT_GUIDE.md` |
| `content/briefs/` | The editorial briefs the articles were written from (keywords from the Semrush export) |
| `data/plan.py` | Which legacy URLs were recreated, and the new-post plan |
| `data/redirects.py` | 301 decisions for retired legacy URLs |
| `data/legacy-urls.txt`, `data/legacy-volume.json` | The 684 URLs (and their search volume) from the 2017 Semrush export |
| `data/photos.json` | Photo library: Wikimedia Commons file, author, licence (credited on pages and `/photo-credits/`) |
| `php/` | `index.php` front controller + `api/` (live news, contact form, newsletter) |
| `assets/` | CSS, JS (weather, tools, search…), tool data JSON, images |
| `wp-content/uploads/` | Media from the old WordPress site, kept at the same URLs |
| `backup/wordpress-2026-10-07/` | WordPress REST export + database dump (see its README) |
| `public/` | **Build output — this is what gets deployed** |

## Build, check, deploy

```sh
python3 build.py        # regenerate public/
python3 validate.py     # HTML, one H1, canonicals, JSON-LD, links, images, legacy coverage, php -l
./deploy.sh             # upload public/ (needs CD_FB_* credentials — see the script header)
./deploy.sh changed     # only files changed since the last deploy
```

Then clear the site cache in hPanel (or `agency-hosting_clear-website-cache`).
Python 3 + Pillow (for resizing images). Local preview with PHP:
`php -S 127.0.0.1:8099 -t public public/index.php` (or any router that falls
back to `public/index.php`).

## Adding a post

Create `content/posts/<slug>.md` following `content/CONTENT_GUIDE.md` (front
matter: title, path, category, places, keyword, description, image…; Markdown
body; FAQ section at the end becomes FAQPage schema; `type: recipe` adds Recipe
schema). Rebuild, validate, `./deploy.sh changed`. It appears on the homepage,
its category and city hubs, `/blog/`, search, RSS and the sitemap automatically.

## Legacy URLs (2017 Semrush export)

- **97 recreated in place** with new 2026 content (same URL, so rankings and
  backlinks carry over): Kung Hei Fat Choi, Cebu lechon, the OPM band list,
  Samal/Davao/Cebu travel guides, Bisaya word meanings, recipes, etc.
- **Retired URLs 301** — politics/2016 election items, celebrity gossip, adult
  "scandal" pages, tag/author/page archives, lotto results, dead promos — go to
  the homepage, as requested. Where a retired page had a near-identical
  recreated twin (e.g. three kinilaw recipes → one), it points to that page
  instead, which keeps more of its value. Old category archives point to the
  matching new hub. Any other URL under a 2017 section also 301s home.
- The **51 posts from the 2023–2025 WordPress site** (Texas apartments, public
  adjusters, travel) stay live at their original URLs with their original
  outbound links, grouped under *Living Abroad* (`/category/expat-living/`),
  and kept off the homepage.
- `/feed/`, `/sitemap_index.xml`, `/wp-sitemap*.xml`, `/?s=`, `/home/`,
  `/category/articles|popular/` and other WordPress paths are handled in
  `php/index.php`.

## Hosting notes

- The platform serves existing files directly, ignores `.htaccess`, and sends
  `/` and unknown paths to `index.php`. So there is no root `index.html`: the
  homepage is `home.html`, served by `index.php` (robots-disallowed, canonical
  `/`). Bare section folders (`/food/` …) contain a one-line `index.php` 301.
- PHP may not write outside `public_html`, so contact messages and newsletter
  sign-ups are stored in `public_html/api/_data/*.php`, each starting with an
  exit guard (requesting them returns an empty 404). Download them with the
  file manager. To also get an email for each contact message, create
  `api/_data/config.php` on the server containing
  `<?php return ['notify_email' => 'you@example.com'];` (PHP `mail()`).
- Live headlines come from Google News RSS searches via `api/news.php`
  (cached 20 min). Weather comes from Open-Meteo and exchange rates from
  ExchangeRate-API, both called from the browser — no API keys.

## Known gaps / to review

- Content was written from general knowledge, fact-checked, and hedged; prices,
  fares and schedules are labelled approximate. Time-sensitive items worth a
  periodic check: DFA passport fees, the Samal bridge status, CCLEX tolls, MLBB
  champions after M6, festival dates marked "approx.".
- A few posts use a category or near-match photo where no free photo of the
  exact subject was available (see `data/photos.json`).
- The newsletter collects addresses but does not send anything yet — connect a
  mailing service when ready.
