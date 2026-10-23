# saffronsupplement.com — custom PHP rebuild

A from-scratch rebuild of [saffronsupplement.com](https://saffronsupplement.com),
replacing the WordPress install. Plain PHP 8.3 with no framework, no database
and no plugins: one front controller, one stylesheet, one shared script.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical host/scheme, redirects, routing, 404, `/sitemap.xml` |
| `app/config.php` | Site constants (name, origin, **Amazon tag `saffronsupplement-20`**), link/FAQ/source helpers |
| `app/products.php` | The 12 reviewed products (ASIN, dose, extract, badge, score, pros/cons) and the card/table renderers |
| `app/routes.php` | Every URL with its title, meta description, H1, schema type and breadcrumb parent; legacy WordPress redirects |
| `app/layout.php` | `<head>`, header/nav, footer, JSON-LD graph, sitemap |
| `app/pages/*.php` | Page bodies (one per route) and the shared sidebar |
| `assets/` | `css/style.css`, `js/app.js`, `img/` (OG image, logo, touch icon) |
| `validate.py` | Crawls every sitemap URL and checks status, H1, titles/descriptions, JSON-LD, internal links, Amazon tags |
| `deploy.sh` | Uploads the site through the Hostinger File Browser API |

Files under `app/` exit immediately if requested directly, and `robots.txt` disallows `/app/`.

## Pages (27)

- **Home** `/`: "saffron supplement" (the brand name "Saffron Supplement" appears 19× in the main content, 27× counting header and footer)
- **Review** `/best-saffron-supplements/`: 12 products, comparison table, method
- **Benefits** `/saffron-benefits/` plus mood, sleep, eye health, weight/appetite, PMS
- **Guides** `/guides/`, `/saffron-dosage/`, `/saffron-side-effects/`, `/how-to-choose-a-saffron-supplement/`, `/affron-vs-satiereal/`
- **Tools** `/tools/` plus dosage calculator, supplement finder quiz, cost-per-dose calculator, safety checker, 12-week mood & sleep tracker (all client-side; the tracker uses localStorage)
- **Other** FAQ, About, Contact, Affiliate Disclosure, Privacy, Medical Disclaimer, Terms, HTML Sitemap

Old WordPress URLs (`/contact-us/`, `/about-us/`, `/blog/`, `/topic/*`, the two old posts, `/wp-*`) 301 to their new equivalents.

## Editing

- **Add or change a product:** edit `PRODUCTS` in `app/products.php`. Every Amazon link goes through `amz()` / `amz_url()`, so the tag is applied automatically.
- **Add a page:** add an entry to `ROUTES` in `app/routes.php` and create `app/pages/<file>.php`. It is added to the sitemap automatically.
- **Change the "last updated" date:** `UPDATED` / `UPDATED_HUMAN` in `app/config.php`.

## Local preview and checks

```sh
php -S 127.0.0.1:8099 index.php     # then open http://127.0.0.1:8099/
python3 validate.py                 # or: python3 validate.py https://saffronsupplement.com
```

## Hosting

Hostinger Agency Growth plan, website UID **`JfEovlw7l`** (plain `php-fpm`, PHP 8.3,
Boston datacenter), created 2026-10-23. The platform serves real files directly,
ignores `.htaccess`, and routes everything else to `index.php`.

The old WordPress site (UID `269tp1YJD`) has **not** been deleted. On
2026-10-23 its domain was unlinked and moved to the new site; it is still
reachable at `indigo-gnat-260277.hostingersite.com`. A content export of its
pages, posts and media metadata (REST API JSON) is in `../saffronsupplement-backup/`.
Delete the WordPress site in hPanel once you're happy with the new one.

Deploy: get credentials from the Hostinger API operation
`agency-hosting_files_generate-upload-url` (website `JfEovlw7l`), export them as
`SS_FB_URL`, `SS_FB_AUTH`, `SS_FB_REST`, then run `./deploy.sh`.

## Contact form

`/contact/` validates input, drops bots (honeypot + 3-second timer), emails each
message to **info@saffronsupplement.com** over Hostinger SMTP (`app/mailer.php`,
smtp.hostinger.com:465), and appends it as a JSON line to
`app/private/messages.php` (first line `<?php exit; ?>`, so a direct request
returns nothing). Each row records whether the email went out (`"emailed"`).

SMTP credentials live **only on the server** in `app/private/smtp.php`, which
is git-ignored and skipped by `deploy.sh` (Hostinger's file API can't write
above `public_html`). Format:

```php
<?php
defined('SS_APP') || exit;
return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@saffronsupplement.com', 'pass' => '…'];
```

If you change the mailbox password, update that file in hPanel's File Manager.

## SEO setup

- Google Analytics 4 tag (`G-J76LEX8DPZ`, set as `GA_ID` in `app/config.php`) in the `<head>` of every page, 404 included.
- Unique title (≤60 chars) and meta description (110–160 chars), canonical URL, Open Graph and Twitter tags on every page.
- JSON-LD: Organization, WebSite, WebPage, plus Article/MedicalWebPage, ItemList, WebApplication, BreadcrumbList and FAQPage where relevant.
- Favicons: `favicon.ico`, `favicon.svg`, `favicon-96x96.png`, `apple-touch-icon.png`, `site.webmanifest` with 192/512 icons.
- `/sitemap.xml` (dynamic, listed in `robots.txt`), an HTML `/sitemap/` page, and an RSS feed at `/feed.xml`.
- IndexNow key file `2ba8f5aa08740881cfccb230a30e6c0b.txt`. All URLs were submitted on 2026-10-23. Resubmit after big changes:
  `POST https://api.indexnow.org/indexnow` with that key and the URL list.
- `validate.py` checks all of the above on every page.

**Still to do in Google Search Console:** verify the domain (DNS TXT record, or the
GA tag method now that the tag is live) and submit `https://saffronsupplement.com/sitemap.xml`.

## Content notes

- Product facts (dose, standardization, count) come from the Amazon listing titles as of October 2026. Scores are editorial. Prices aren't shown because they change constantly.
- Health claims cite peer-reviewed trials; each article ends with its sources.
- No testimonials or "we tested" claims: the About page states that products were not lab-tested.
