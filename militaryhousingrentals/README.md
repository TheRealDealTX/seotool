# militaryhousingrentals.com

Custom PHP site that replaces the WordPress/Elementor front end. No database:
content lives in `app/data/`.

| Path | What it is |
| --- | --- |
| `index.php` | Router. Keeps every WordPress URL (`/properties/{slug}/`, `/bases/{slug}/`, `/{post}/`, sitemaps, `?p=ID`). RSS is at `/feed.xml`; `/feed/` is an HTML page and the old per-base `/feed/` URLs redirect to the base page |
| `app/data/listings.json` | Listings: address, beds/baths, floor-plan ranges, phone, hours, eligibility, pets, utilities, schools, photos, sources |
| `app/data/bases.json` | Installations. Optional per-base keys: `guide` (name of a file in `app/data/guides/` rendered at the bottom of the base page with Article + FAQ schema), `seo` (`full_title`, `h1`, `intro`, `description` overrides), `guide_url`/`guide_label` (link to a guide that lives elsewhere) |
| `app/data/guides/*.html` | Long-form housing guides. `fort-hood-housing.html` renders on `/feed/`; `joint-base-san-antonio.html` renders on `/bases/joint-base-san-antonio/`. Same markup as posts (h2 sections, optional `.schema-faq` block) |
| `app/data/posts.json` + `app/data/posts/*.html` | Blog posts (metadata + body) |
| `app/views/` | Page templates; `partials.php` has the BAH calculator and PCS countdown; `latest.php` is the `/feed/` page, `feed.php` the RSS at `/feed.xml` |
| `assets/` | CSS, JS, logo variants, public-domain photos |
| `backup/` | Original WordPress `index.php`/`.htaccess` and a full content export, for rollback |

Run locally: `php -S 127.0.0.1:8099 index.php` (or any router that sends non-files to `index.php`).

Images in `/wp-content/uploads/` stay on the server from the WordPress install.

To add a listing, append an object to `listings.json` (copy an existing one) and upload that file.
To add a post, add an entry to `posts.json` and the body to `posts/{slug}.html`.
Form submissions are emailed to info@militaryhousingrentals.com and logged to `app/storage/submissions.log`.
