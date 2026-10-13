# Addendum: filling in old URLs from Google Search Console

These are old gaparboristsupply.com product URLs that Google had crawled but the
new site doesn't have yet. There is no keyword data for them: the URL slug is
the product. Follow `/home/user/seotool/gaparboristsupply/work/BRIEF.md` (voice,
hard rules, Product JSON schema, KIND list, brand slugs) with these changes:

- Every item is tier `standard`: `body` 2 sections, ~200–300 words total;
  `faq` 2 entries; 3–6 specs (only figures you are confident of).
- `keyword`: pick a natural search phrase for the product (usually the
  product name, lower case, without filler such as sizes in parentheses).
- `category`: if the input gives a category, use it exactly. If it is `null`,
  choose the single best match from
  `/home/user/seotool/gaparboristsupply/work/fill/category-list.json` (copy the
  path exactly).
- Work out what the product is from the slug. Many are well-known arborist
  items (Teufelberger, Yale, Samson, Sterling, Petzl, DMM, ISC, Notch, CMI,
  Husqvarna, Silky, Buckingham, Weaver, Stihl-compatible parts, etc.). If you
  genuinely can't tell what a slug is, write a careful, generic page for the
  closest product type and keep specs to what the name states.
- `body` links: at most 2, and only to the product's own `category` path.
- Extra brand slugs you may use (plus the list in BRIEF.md and any sensible new
  lowercase-hyphenated slug): 4srt, arb-climber, aspen-fuel, at-height,
  beaver-state-plastics, bigfoot, boss, land, paulhaul, preformed-line-products,
  razorback, rigguy, the-splice-shop, tylaska, xtc, reecoil, sirius, ocean,
  stihl, maasdam, crosby, spencer, haix, gecko.

## Batches 35–41 (from Search Console performance)
These inputs also carry `gsc_clicks` and `gsc_impressions` from the old site's
last 16 months, and some are tier `full` (follow BRIEF.md's full-tier length).
Pages with more clicks deserve the most careful, specific copy.
