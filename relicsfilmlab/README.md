# relicsfilmlab.com — rebuild

A static rebuild and rebrand of relicsfilmlab.com (formerly a Shopify store) as an
affiliate commerce site. Every product page keeps its old Shopify URL; orders go to
Amazon with the affiliate tag `relicsfilmlab-20`.

## Hosting

* Hostinger **Agency Growth** plan, website UID `85ugmexVF` (php-fpm 8.3), on the
  temporary `*.hostingersite.com` domain until the real domain is connected.
* The temporary domain sends `X-Robots-Tag: noindex` (see `src/index.php`), and every
  page's canonical already points at `https://relicsfilmlab.com`, so nothing needs to
  change when the domain is switched — `index.php` also 301s `www.` and `http://`
  to `https://relicsfilmlab.com` once it is live.
* The host serves existing files directly, ignores `.htaccess`, and routes every
  unknown path to `index.php`. So pages live in `public/_p/<url>.html` and
  `index.php` serves them at their exact old URL (no trailing slash, like Shopify),
  301s retired URLs (`public/_redirects.php`) and returns a real 404 otherwise.
  There is deliberately no `index.html` anywhere in the web root.

## Build & deploy

```sh
python3 fetch_images.py   # (optional) download any missing photos
python3 build.py          # writes ./public
python3 validate.py       # checks every old URL + every internal link via php -S
./deploy.sh               # see header of deploy.sh for credentials
```

Local preview: `php -S 127.0.0.1:8000 -t public src/dev_router.php`.

## Source layout

| Path | What |
| --- | --- |
| `catalog.py` | Every product (slug = old Shopify handle), category, spec line, intro; plus `PRODUCT_REDIRECTS` |
| `content.py` | Brand blurbs, buying checklists, film/battery data, collection copy, guide list |
| `pages.py` | Home, info pages, film-lab/service pages, old-URL redirects (`STATIC_REDIRECTS`) |
| `guides.py` | Long-form guides at `/blogs/guides/<slug>` |
| `build.py` | Layout, product/collection templates, sitemap, search index, router output |
| `src/` | CSS, JS, `index.php` router, static root files |
| `data/` | Semrush keyword + backlink exports, `keywords.json` (per-URL keywords), `image_credits.json` |

## URLs and redirects

* All 300+ ranking/backlinked URLs from the Semrush exports return 200 or a single
  301 — `validate.py` checks them all.
* Kept exactly: `/`, every `/products/<handle>`, `/collections/*`, `/pages/*`,
  `/blogs/guides/*`, `/camera-repairs`, `/film-services`, `/order-now`.
* 301'd (poor/duplicate URLs): hash-style handles (`b656e39…` → `vivitar-v3000s`,
  `av092fe…` → `canon-ftb`), suffixed duplicates (`canon-ae-1-program-2-5p8r3` →
  `canon-ae-1-program`), over-long handles, gift cards/merch (→ gift guide /
  accessories), nested `/collections/x/products/y` → `/products/y`, `/404` → `/`.
* `/cdn/shop/files/IMG_0006…jpg` and `IMG_0171…jpg` (image backlinks) still resolve.

## Affiliate links

All buy buttons are Amazon search links (`amazon.com/s?k=…&tag=relicsfilmlab-20`,
`rel="sponsored nofollow"`), because vintage cameras are sold by many independent
sellers and listings change daily. No prices are shown (Amazon policy). The
disclosure is in the footer, on every buy box and at `/pages/affiliate-disclosure`.

## Photos

Real photographs only, from Openverse/Flickr and Wikimedia Commons under licences
that allow commercial use (CC0, Public Domain, CC BY, CC BY-SA). Each product page
credits its photo; the full list is at `/pages/photo-credits`.

Contact address used on the site: info@relicsfilmlab.com.
