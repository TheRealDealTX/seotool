# vintiqueflea.com: custom PHP site

A hand-built PHP site that replaces the old WordPress/Elementor install on Hostinger
(Agency Growth plan, website UID `67Tls7oNq`). It has no database, no plugins and no framework:
one front controller, PHP templates, one stylesheet and vanilla JavaScript.

## Structure

| Path | Purpose |
| --- | --- |
| `index.php` | Front controller: legacy redirects, 410s, trailing slashes, routing |
| `.htaccess` | Sends everything that isn't a real file to `index.php`; blocks `inc/`, `data/` and leftover WordPress files |
| `inc/config.php` | **Edit me:** business details, contact email, Amazon tag, **upcoming market dates** |
| `inc/data.php` | Shop categories and Amazon picks, game metadata, seasonal editions |
| `inc/routes.php` | Static page routes, old→new URL map (301), removed URLs (410) |
| `inc/guides/*.php` | One file per guide article (drop in a new file and it's live and in the sitemap) |
| `inc/pages/*.php` | Page templates |
| `inc/layout.php` | Head/header/footer, SEO meta, JSON-LD schema, product cards |
| `inc/forms.php` | Contact, vendor application and newsletter handling (emailed + logged to `data/*.jsonl`) |
| `assets/` | CSS, JS (site + one file per game), images |
| `data/` | Private, writable: form submissions and the CSRF secret. Never web-accessible |
| `rollback/` | Stock WordPress `index.php` + `.htaccess` to revert instantly |

## URL map

- Kept and rewritten (301): `/about-us/`→`/about/`, `/our-events/`→`/events/`, `/contact-us/`→`/contact/`,
  `/write-for-us/`→`/vendors/`, the four event posts→`/events/{season}-vintage-market-houston/`, and the relevant
  Houston, decorating and shopping posts→`/guides/…`. Categories redirect to the closest hub.
- Removed (410 Gone): about 36 off-topic apartment, salary, real-estate and roofing posts, plus all `wp-*` paths.
- New: `/shop/` with 8 category pages (64 Amazon picks tagged `josephrayditt-20`), `/play/` with 5 games,
  `/food-trucks/`, `/vendors/`, `/affiliate-disclosure/`, `/privacy-policy/`, dynamic `/sitemap.xml`.

## Common edits

- **Announce market dates:** add an entry to `UPCOMING_EVENTS` in `inc/config.php`. It appears on the home,
  events and season pages and produces Event schema.
- **Link a specific Amazon product:** add `'asin' => 'B0…'` to a product in `inc/data.php`. Otherwise the
  links go to tagged Amazon searches, so they never break.
- **Social links:** fill in `SOCIAL` in `inc/config.php`.

## Local preview

```sh
php -S 127.0.0.1:8000 -t . index.php
```

## Deploy

See `deploy.sh`. It uploads via the Hostinger file-browser TUS API, sending `index.php` and `.htaccess` last.
`./deploy.sh rollback` restores WordPress's entry files (the WordPress files and database are left untouched).
