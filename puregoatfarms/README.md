# puregoatfarms.com — Milking & Dairy content cluster

Source files for three new articles and a set of contextual internal links on
[puregoatfarms.com](https://puregoatfarms.com) (WordPress 7 + Elementor Pro +
Yoast, Hostinger Agency website `VSUHIRjmA`). This folder is unrelated to the
huttoroofs.com build in the rest of the repo and is excluded from it.

## Why

The Search Console export for 16 Jul – 16 Oct 2026 shows one post,
`/how-much-milk-can-a-goat-really-give-at-once/`, earning 187 impressions and
0 clicks at an average position of 21. Nearly every query behind those
impressions asks something the post only answers in passing:

| Query cluster (Search Console) | Impr. | Avg. pos. | US volume (DataForSEO) |
| --- | ---: | ---: | ---: |
| how much milk does a goat produce / a day / per day, goat milk production (per day), saanen / alpine / nubian goat milk production per day | ~60 | 16–42 | 260 + 210 + 1,000 + breed terms |
| do goats produce milk all the time, …without being pregnant, do all goats produce milk, do goats make milk | ~20 | 30–63 | 50 + 210 + 70 + 140 (how long…) |
| how often do you milk a goat, how often can you / do you need to milk a goat | ~7 | 6–37 | 140 + 140 + 30 |

Google is ranking a "per milking" article for "per day", "all the time" and
"how often" questions because the site has nothing closer. Each cluster now
gets a dedicated article with the query phrasing in the title, H1, opening
paragraph, an H2 and the FAQ schema, and all five Milking & Dairy pages link
to each other with descriptive anchors.

## What gets published

New posts (category Milking & Dairy, Yoast meta description, focus keyword,
primary category, FAQ block for FAQPage schema, featured image):

| URL | Focus keyword | Words |
| --- | --- | ---: |
| `/how-much-milk-does-a-goat-produce-per-day/` | how much milk does a goat produce | ~2,400 |
| `/do-goats-produce-milk-all-the-time/` | do goats produce milk all the time | ~2,050 |
| `/how-often-do-you-milk-a-goat/` | how often do you milk a goat | ~2,100 |

Edits to existing posts (eight one-sentence additions, each carrying one
contextual link; the existing text is not changed):

- `/how-much-milk-can-a-goat-really-give-at-once/` → links to all three new
  posts and to the cheese post.
- `/how-many-goats-do-you-need-to-make-cheese/` → links to all three new posts
  and to the at-once post.

The homepage "Fresh from the field" grid, `/blog/`, the category pages and the
Related Articles widget are Elementor posts widgets, so they pick the new posts
up automatically, as does the Yoast sitemap.

## Files

| File | Purpose |
| --- | --- |
| `build_posts.py` | The three articles and the eight link edits, written as Gutenberg block HTML; writes `payload.json` |
| `payload.json` | Generated payload (committed so the content can be reviewed as data) |
| `make_images.py` | 1000×563 WebP featured-image cards in the site palette (placeholders; swap for photos in wp-admin) |
| `publish.php` | One-off importer: creates/updates the posts, sets Yoast meta and thumbnails, splices the links, verifies, deletes itself |
| `publish.sh` | Uploads payload + images + importer through the Hostinger File Browser API, runs a dry run, then `--live` |

## Publishing

```sh
# credentials from agency-hosting_files_generate-upload-url (website VSUHIRjmA)
export PGF_FB_URL=… PGF_FB_AUTH=… PGF_FB_REST=…
./publish.sh          # upload + dry run (reports what would change)
./publish.sh --live   # publish; the importer removes itself and the payload
```

Then clear the site cache (`agency-hosting_cache_clear-website` for
`VSUHIRjmA`) and request indexing for the three new URLs in Search Console.

Safety notes built into `publish.php`:

- Runs as the admin user so WordPress does not pass content through kses.
  Re-saving the two existing posts through kses would strip the `<style>` and
  `<script>` of their calculators.
- An edit is applied only if its anchor sentence occurs exactly once and the
  link is not already present, and the saved content is compared byte for
  byte with the expected result; on a mismatch the original content is
  restored. Re-running is safe.
- Posts are matched by slug, so re-running updates rather than duplicates.

## Reverting

Trash the three posts in wp-admin, and restore the two existing posts from
their revision history (the edits are ordinary `wp_update_post` saves, so each
has a revision from just before the change).
