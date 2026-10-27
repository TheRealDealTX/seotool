# houstonapartments.com — map-search rebuild

A PHP + MySQL apartment search site for Houston (Apartments.com-style map
search with freehand draw-to-search and filters), fed from the
riseapartments.com WordPress site and hosted on the Hostinger Agency plan.

Preview: https://hotpink-guanaco-475335.hostingersite.com (Hostinger website
UID `SwlS15suw`, `noindex` until launch).

## How it fits together

| Piece | Where |
| --- | --- |
| Front controller / router (all old WordPress URLs kept) | `public/index.php` |
| Config defaults (copy to `config.local.php` on the server, never committed) | `public/app/config.sample.php` |
| Business details, nav, area pages ↔ Rise location IDs | `public/app/site.php` |
| Search, cards, property SEO/schema | `public/app/lib/Listings.php` |
| Rise import: REST list + property-page parser + geocoder + image copy | `public/app/lib/Rise.php` |
| CLI (migrate, import, sync, parse) — also the cron entry point | `public/app/cli.php` |
| Templates | `public/app/views/` |
| Styles / scripts | `public/assets/css/site.css`, `public/assets/js/site.js`, `public/assets/js/map.js` |
| Migrated WordPress posts and pages | `public/app/content/{posts,pages}.json` |
| One-off WordPress migration | `tools/migrate_wp.py` |
| Deploy over Hostinger's File Browser TUS API | `deploy.sh` |

The Hostinger platform sends every request for a missing file to
`index.php` and ignores `.htaccess`, so routing and redirects live in PHP.
Only `public_html/` is writable through the file API, so the app sits inside
it; library files exit when requested directly and `config.local.php` only
returns an array.

## Admin panel

`/admin/` (`public/app/admin.php`, views in `public/app/views/admin/`). Sign-in with
email + password (bcrypt, CSRF tokens, 8 failed attempts per IP per 15 min).
Roles: *admin* (also manages users) and *editor* (listings + leads).

- Listings: search/filter, add, edit (photos with drag-to-reorder, floor
  plans, starting prices per bedroom, amenities, description, schools, FAQs,
  map pin), hide or delete. Manual listings get IDs from 900000001.
- Saving a Rise listing locks it (`locked = 1`) so the sync no longer
  overwrites it, unless "keep updating from Rise" is ticked.
- Leads: status + notes (autosave), CSV export; new leads are emailed to
  `lead_email` (info@houstonapartments.com).
- Import from Rise: by URL/slug, or "sync new & updated" in small batches.
- First account: `POST /admin/setup/` with `key=ADMIN_KEY`, only while no users exist.

## Prices and filter URLs

Prices are hidden from visitors (`price_display` = `hidden`: every listing
says "Check for availability", map pins are plain dots). `starts_at` would show
"Starts at $X" instead. The real numbers stay in the database for the price filter.

Filters live in the path (`public/app/lib/Filters.php`):
`/apartments/3-beds/`, `/apartments/3-beds-1200-to-1600/`,
`/apartments/houston-heights/pet-friendly-with-pool-gym-closets/` (one `with-` prefix, short amenity words). Token order is fixed
(beds, baths, price, flags, amenities, year) and any other URL for the same
filters 301s to the canonical one, including old `?beds=3` links. Keyword,
drawn-area, sort and multi-bedroom searches stay in the query string and are
`noindex`; path pages with 1–3 filters and results are indexable, server-rendered,
and listed in `/search-sitemap.xml`.

## Listings data

Rise's REST API (application password for user `riseapartments`) lists the
apartments and their `location` terms. The detailed fields (floor plans,
per-bedroom "Price Starts At", amenities, schools, FAQs) are ACF fields that
aren't exposed over REST, so `RiseParser` reads them from each property's
public page. Notes:

- Rise hides the per-bedroom starting prices on its own pages (the elements
  carry `ae-visibility-hidden`), but they are in the HTML and are what the
  price filters use. When a property has none, the range quoted in its
  description is used (`data.price_source = description`).
- Addresses are geocoded with the US Census geocoder (Nominatim fallback) and
  cached in the `geocache` table.
- Photos and floor plans are copied to `public_html/media/p/{id}/`, so the
  site never hotlinks Rise.
- Rise's firewall resets bursts; page requests are spaced ~1.2 s apart.

Import or refresh:

```sh
php public/app/cli.php import camden-heights 1810-main   # specific slugs
php public/app/cli.php sync 200                           # next 200 new/changed Houston listings
```

On the server the same runs through `/admin/sync/?key=ADMIN_KEY&slugs=a,b`
or `/admin/sync/?key=ADMIN_KEY&limit=25` (stops after ~4 minutes), or as a
Hostinger cron job running `php …/public_html/app/cli.php sync`.
Leads are stored in the `leads` table (`/admin/leads/?key=ADMIN_KEY`) and
emailed to `lead_email` when set.

## Local development

```sh
cp public/app/config.sample.php public/app/config.local.php   # set db_dsn to sqlite, rise_pass
php public/app/cli.php import 1810-main camden-heights
php -S localhost:8080 -t public tools/devserver.php
```

## Maps

Leaflet + Leaflet.markercluster with OpenFreeMap vector tiles rendered by
MapLibre (`map_style` in config; free, no API key). The draw tool is a
freehand lasso: the polygon is simplified (Douglas-Peucker) and sent as
`poly=lat,lng;…`; the server filters with a bounding box in SQL, then a
point-in-polygon test.

## Launch checklist

1. Add houstonapartments.com (and www) to website `SwlS15suw` in Hostinger and point DNS at it; wait for SSL.
   Requests on that host automatically use `https://houstonapartments.com` as the canonical URL and allow
   indexing (`live_host`); www redirects to the bare domain. The preview domain stays noindex.
2. Check https://houstonapartments.com/robots.txt shows the sitemap line, then resubmit
   `/sitemap_index.xml` in Search Console.
3. Keep the domain's existing MX/email DNS records when moving DNS.
