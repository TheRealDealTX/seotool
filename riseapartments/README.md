# riseapartments.com — Amazon affiliate links for blog posts

Adds a "Helpful Finds" block (4 Amazon links tagged `riseapartments-20` plus an
Associates disclosure) to every published **post** on riseapartments.com that
recorded views in the GA4 "Pages and screens" export. Pages, property listings
and posts that already carried hand-placed `amzn.to` links are left untouched.

| File | What it is |
| --- | --- |
| `affiliate_links.py` | Classifier + block builder + WordPress REST writer |
| `analytics.csv` | GA4 export used to pick posts (2026-09-07 to 2026-10-04) |
| `report.csv` | One row per post touched: views, id, slug, URL, product set, status |
| `posts_cache.json` | Raw post content downloaded before the change (not committed, 28 MB) |

## How it works

1. Downloads all published posts (`context=edit`) and caches them.
2. Matches post titles to GA4 page titles (the ` | Rise Apartments` suffix is stripped) and keeps posts with at least one view.
3. Classifies each post by slug into one of ~45 product sets (walk-in showers, Airbnb hosting, second-chance approval kit, moving day, EV charging, etc.). `RULES` is first-match; `OVERRIDES` pins specific slugs.
4. Builds Gutenberg blocks: separator, H3, intro, 4-item list of tagged Amazon search links (`rel="nofollow sponsored noopener noreferrer"`), small-print disclosure.
5. Inserts the block before the first Conclusion / Final Thoughts / FAQ heading, otherwise before a trailing AdSense block, otherwise at the end.
6. Writes with `POST /wp/v2/posts/{id}`. The `<!-- rise-amazon-picks -->` marker makes reruns idempotent.

Amazon search links are used instead of ASINs so no link can go dead when a
product is discontinued. Swap any search URL for a `/dp/ASIN?tag=riseapartments-20`
link in `SETS` if you want a specific product.

## Running

```sh
export WP_USER=riseapartments WP_APP_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx'
python3 affiliate_links.py plan    # classify, write report.csv, no writes
python3 affiliate_links.py apply   # write to WordPress
```

Delete `posts_cache.json` to refetch the live content before another run.
