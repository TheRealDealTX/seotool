# purelywholesome.com: custom PHP rebuild

A rebuild of the Purely Wholesome Farm WordPress/Elementor site as a small custom
PHP site with no database and no plugins. Every URL the old site had in its
sitemap or in Search Console still works: it either renders or 301s to its new home.

**Live:** https://purelywholesome.com (Hostinger Agency website `ZST1Yj5FK`;
DNS at GoDaddy, `@` A record `72.60.128.114`). The website's temporary address,
https://mediumslateblue-woodpecker-252575.hostingersite.com, sends
`X-Robots-Tag: noindex` and omits the Google tag, so it never competes with
the real domain or skews analytics (`is_production_host()` in `app/bootstrap.php`).

The old WordPress site is being moved to
https://violet-finch-215265.hostingersite.com (shared hosting account
`u401386392`, copied with hPanel's Copy Website tool).

## Why traffic dropped (from the Search Console and GA4 exports)

| Period | Weekly clicks | Avg. position |
| --- | --- | --- |
| Nov 2025 – Mar 2026 (peak) | 400 – 2,450 | 3 – 6 |
| From **Apr 6, 2026** | 55 – 125 | 12 – 25 |
| From **Aug 21, 2026** | 2 – 7 | 35 – 60 |

Two step drops, each overnight, both lining up with Google updates:

1. **Apr 6, 2026: about -80%.** Between Feb and Apr 2026 the site published
   dozens of paid guest posts with no connection to a farm or kitchen site
   (floor leveling in Tampa, kitchen cabinet suppliers in Houston, banking, mold
   inspection, rat removal, Ugandan coffee…), plus "write for us" pages
   selling placements. That is the pattern Google targets as site reputation
   abuse and unhelpful content, and it pulls down the whole domain.
2. **Aug 21, 2026: near-total loss.** Rankings fell to page 4-6 site-wide while
   more placements kept going up (the last on Aug 11).

Other problems found in the data: about 15 lifestyle posts with 1-5 second
engagement (paid or bot traffic), keyword-stuffed headings ("Tomato Sauce /
Mint Sauce / Lamb Recipe / Lamb Chops"), near-duplicate posts competing for the
same query, removed posts 301ing to the homepage (soft 404s), anonymous
"info@" authorship, and low CTR on pages that ranked #2-4 (for example "how to
brine chicken": 16k impressions, 0.9% CTR).

## What changed

* **Off-topic placements:** 52 posts (listed in `OFF_TOPIC` in
  `_build/import_wp.py`) still return 200 at their URLs but are `noindex`,
  removed from listings, search, feeds and sitemaps, carry a disclosure, and
  their outbound links are `rel="sponsored nofollow"`. "Write for us" pages
  301 to contact. On-topic vendor posts (the cattle-handling series and others)
  stay indexed but their links are marked sponsored.
* **Retitled top pages:** the pages that carried the traffic got new titles,
  descriptions and, where they were keyword-stuffed, headings, aimed at the
  queries each one actually ranked for (`OVERRIDES` in the importer).
* **Clean content:** all 259 posts imported, stripped of Elementor/WordPress
  markup, with heading anchors, a table of contents, FAQ accordions with FAQPage
  schema, sized lazy-loaded images (large PNGs get optimized WebP copies),
  related posts, and an author and editorial box linking to a new
  `/editorial-policy/`.
* **Redirects:** old duplicate URLs now point at the matching post, not the homepage
  (`app/redirects.php`). All 1,898 WordPress image-size URLs (`-300x200.webp`) exist
  as real files. `/feed/`, `/?s=` and the Yoast sitemap URLs all still work.
* **9 interactive tools** at `/tools/`, each also embedded in the relevant
  articles: brine calculator, lamb cooking calculator, lamb dinner plate
  builder, goat gestation calculator (with calendar export), goat temperature
  checker, backyard egg planner, canning altitude adjuster, pumpkin pie
  troubleshooter and recipe scaler.
* **New hubs:** `/topics/<topic>/` hub pages (lamb, brining, baking, canning,
  goats, chickens & eggs, homestead, crafts, kitchen) build topical clusters.
  The original `/category/` URLs still work too.
* **Design:** same logo and palette (forest `#1C352D`, sage `#A6B28B`, peach
  `#F5C9B0`, cream `#F9F6F3`). Fraunces and Plus Jakarta Sans fonts. Effects:
  animated blobs and grain, falling leaves, morphing photo frames, mouse
  parallax, a drawn underline, a marquee, scroll reveals, tilt cards, count-up
  stats, a reading progress bar, a scroll-spy table of contents, instant search
  (press `/`) and view transitions. All motion respects `prefers-reduced-motion`.
* The homepage mentions "Purely Wholesome Farm" 22 times in visible content.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: redirects, sitemaps, feed, robots, routing |
| `app/bootstrap.php` | Config (site name, canonical origin), topics, helpers |
| `app/controllers/`, `app/views/` | Page logic and templates |
| `app/tools/` | Tool registry (copy, FAQ, sources) and markup; logic in `assets/js/tools.js` |
| `app/redirects.php` | Legacy URL map |
| `app/mailer.php`, `app/storage/` | Contact form and newsletter handling. Messages go to info@purelywholesome.com and to `app/storage/*.php`, which start with an exit guard so they can't be read over HTTP |
| `content/posts/<slug>.php`, `content/index.php` | Post bodies and the metadata index (the source of truth now) |
| `wp-content/uploads/` | The old media library at its original paths, plus `optimized/` WebP copies |
| `_build/import_wp.py` | One-time importer from the WordPress scrape (kept for reference) |
| `_build/make_variants.py` | Recreates WordPress resized image files (`-300x200.webp`). The host 404s missing images before PHP runs, so these must exist as real files |
| `_build/validate.py` | Checks old URLs and crawls for broken links, H1s, meta and JSON-LD |

## Running and deploying

```sh
php -S 127.0.0.1:8099 index.php                     # local preview
python3 _build/validate.py http://127.0.0.1:8099 old-urls.txt
./deploy.sh                                          # see header for credentials
```

The Hostinger platform ignores `.htaccess` and sends unknown paths to
`index.php`, so routing doesn't depend on rewrite rules. Don't add an
`index.html`. The platform answers missing paths that look like static files
(`.txt`, images) with its own 404 before PHP runs. That's why `robots.txt`,
the favicons and the Search Console verification file
(`googlecccfbf2f7e9e5ae4.html`) are real files at the root, not PHP routes.
Sitemaps (`.xml`), the feed and `search-index.json` do reach PHP.

## SEO checklist (what's in place)

* Google tag `G-JB48YFCMM7` in the `<head>` of every page on the real domain
  (`app/views/layout.php`); the privacy policy discloses Google Analytics.
* Favicons from the original site icon: `/favicon.ico` (16/32/48),
  `assets/img/favicon-96x96.png`, `/apple-touch-icon.png`, `/site.webmanifest`.
* `/sitemap_index.xml` with post, page and category sitemaps (the Yoast URLs),
  with lastmod and image entries; noindexed posts are left out. `robots.txt`
  points to it.
* Titles stay within about 65 characters: the brand suffix is dropped when it
  won't fit (`seo_title()`), and over-long post titles were rewritten
  (`_build/set_titles.py`). Descriptions are cut at 160 characters (`seo_desc()`).
* Every page: one H1, canonical, Open Graph and Twitter tags (with image size
  and alt text), JSON-LD (Organization, WebSite, BlogPosting, BreadcrumbList,
  FAQPage, CollectionPage). Posts also carry `article:published_time` and
  `article:modified_time`.

## Going live

1. ~~Point purelywholesome.com at website `ZST1Yj5FK`~~ (done 2026-10-20).
2. In Search Console, submit `/sitemap_index.xml` and request indexing for the
   top 10 pages listed in `POPULAR` in `app/bootstrap.php`.
3. Don't publish new paid placements. Recovery from a site-wide demotion
   usually shows at the next core update after the cleanup is crawled.
4. Add a real author name, photo and bio. Named, experienced authors are the
   biggest remaining E-E-A-T gap. Use them in `app/views/post.php` and in the
   `author` field of the schema in `app/controllers/post.php`.
5. Test the contact form once on the live domain (it relies on PHP `mail()`).
