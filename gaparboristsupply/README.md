# gaparboristsupply.com — rebuild

A custom PHP store and buying guide for arborist gear. It rebuilds the expired
gaparboristsupply.com under new ownership. It has no database and no CMS:
content lives in JSON, a compile step turns it into one PHP array, and one
front controller renders every page.

**Live (temporary domain):** https://greenyellow-woodcock-344499.hostingersite.com
on Hostinger Agency website `wvWrkASNv` (Agency Growth plan, plain php-fpm 8.5, Phoenix).
While on the temporary domain, every page carries `noindex` (`'live' => false` in
`site/app/config.php`).

## What's in it

| | |
|---|---|
| 314 product pages | Each has fresh copy, highlights, specs, Q&A, a typical price, Add to cart, Save, Compare and Check price |
| 121 category pages | Brand and price filters, sorting, a buying guide and FAQ |
| 64 brand pages + `/brands/` A–Z | |
| 6 buying guides | `/guides/` |
| 6 interactive tools | `/tools/`: climbing kit builder, rigging load calculator, tree height and rope length, 2-stroke fuel mix, NGK spark plug decoder and reader, chain and file size finder |
| Cart | Stored in the browser. Includes a saved list, a shareable list link, a printable checklist and a "check prices" handoff to retailers |
| Shop all and search | `/shop-all/` has faceted filters; `/search/` has live suggestions in the header |

Visual effects: drifting leaves and sawdust on a canvas in the hero, parallax
treeline layers, animated growth rings, a rope-and-climber scroll progress bar,
3D card tilt with a spotlight, a saw-chain animated button border, fly-to-cart,
and reveal on scroll. All of it respects `prefers-reduced-motion`.

## URLs and SEO equity

`seo-data/` holds the Semrush exports: organic positions (737 ranking URLs)
and backlinks (10.7k links). `scripts/plan.py` and `scripts/select.py` turn
them into `seo-data/build-plan.json`, which decides what gets a page:

- Every category and brand URL, plus every product that had traffic, backlinks
  or search volume ≥ 390, keeps its **exact old URL** as a real page.
- Product URLs that were not rebuilt 301 to their category. Merged categories
  301 to the category that absorbed them.
- Backlinked URLs from the store's earlier platforms (`/Name/image/item/…`,
  `/shop/product/…`, `/search.php?search_query=`) 301 to the closest page. They
  use an explicit map (`LEGACY` in `index.php`) and fall back to fuzzy matching.
- `/static/images/logo.png` (backlinked) is served again.

`python3 scripts/check_urls.py <origin>` requests all 780 URLs from both exports
and fails if any of them doesn't end at a 200 within two hops. Current result on
the live site: 490 serve directly, 290 redirect once, 0 broken.

## Affiliate links (to do)

Every "Check price" button goes through `/go/?p=<product path>`, which 302s to
the retailer. To set links:
- **Per product:** create `site/data/affiliates.json` as `{"/product/path/": "https://…"}`.
- **Fallback:** `affiliate_fallback` in `config.php`, currently an Amazon search
  for the product name. Put your Associates tag in `amazon_tag` and it is appended
  automatically.

## Editing and deploying

```sh
# edit site/data/products/*.json, categories/*.json, brands.json, guides.json
php scripts/compile.php                       # -> site/data/catalog.php + site/assets/data/catalog-lite.json
php -S 127.0.0.1:8080 -t site scripts/dev-router.php   # local preview
python3 scripts/check_urls.py http://127.0.0.1:8080    # legacy URL check
./deploy.sh                                   # see header for the 3 upload credentials
```

The host serves real files directly and sends every other path to `index.php`.
There is deliberately no `index.html`. `.htaccess` is ignored, so redirects,
`robots.txt` and `sitemap.xml` are all produced by `index.php`.

## Going live on gaparboristsupply.com

1. Point the domain at website `wvWrkASNv` (hPanel, or connect it with the Hostinger API).
2. Set `'live' => true` in `site/app/config.php`. This removes `noindex`, serves a
   real `robots.txt` and sitemap, and 301s www, http and the temporary host to
   `https://gaparboristsupply.com`.
3. Run `php scripts/compile.php && ./deploy.sh`, then clear the cache.
4. Submit `/sitemap.xml` in Search Console.

## Content notes

- Copy was written fresh; nothing was copied from the old site. No address,
  phone number, reviews, ratings or dealer claims are made.
- **Prices are typical-price estimates. Specs only include figures the writers
  were confident of.** Before going live, spot-check prices and specs on the
  high-traffic pages (372XP, 3120XP, Silky Sugoi and Gunfighter, NGK plugs,
  450 Rancher), and confirm the brand on items marked "Gap Arborist Supply"
  (generic or house items).
- Product images are illustrations (`site/assets/img/kinds/*.svg`). Swap in
  retailer images when the affiliate feeds are connected.
- The contact address `hello@gaparboristsupply.com` in `config.php` needs a
  mailbox once the domain is live.
