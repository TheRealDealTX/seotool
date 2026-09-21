# rooftarp.com — static rebuild

A static HTML rebuild of [rooftarp.com](https://rooftarp.com), replacing the
WordPress/Elementor/Rank Math site. No PHP, no database, no plugins — HTML, one
CSS file, one JS file. Upload this directory to any web host.

This is a separate site from `huttoroofs.com` in the repository root. The two
share an owner and a phone number but nothing else; this directory is
self-contained and has its own `build.py`, `siteconfig.py` and `content/`.

## Why this rebuild exists

On **21 August 2026** rooftarp.com lost roughly 80% of its Search Console
impressions in a single day. Average position went from ~50 to ~85 and clicks
went to zero. That date is not a coincidence: Google's **August 2026 spam
update** rolled out 18 August and completed 21 August, and it targeted scaled
content abuse and doorway pages — explicitly including location pages that
only change the city name.

The old site had **158** `/service-areas/roof-tarp-<city>/` pages. Measured
against each other they were near-identical:

| Template | Pages | Identical to cluster representative |
| --- | --- | --- |
| 2,949 words | 61 | 98.17% |
| 1,861 words | 42 | 98.55% |
| 3,001 words | 25 | 96.47% |
| 1,888 words | 12 | 97.43% |
| 2,932 words | 7 | 98.50% |
| 1,887 words | 4 | 96.96% |

151 of 158 sat in a ≥95% near-duplicate cluster. The only thing that varied
was the city name and its possessive.

Nothing was technically broken — `robots.txt` was permissive, pages carried
`index, follow` and correct canonicals, and the server returned 200. There was
no manual action. It was a purely algorithmic demotion of a content pattern
that had been in place since March 2025.

## What changed

**Kept 17 metros, removed 141.** Selection came from the 16-month Search
Console export (2025-05-20 → 2026-09-19), not from guesswork. Of the 158 city
pages, 67 ever earned an impression and 27 ever earned a click. The 141 removed
pages account for **14 clicks in 16 months** between them — under one click a
month, in exchange for the pattern that demoted the whole domain.

Every kept URL already exists on the live site, so those rankings carry over
rather than starting from zero.

**Added the service pages the old site never had.** `/services/` returned 404
on WordPress, which meant the highest-volume head terms had no page to rank:

| Query | Impressions (16mo) | Old position |
| --- | --- | --- |
| emergency roof tarp | 9,654 | 61.0 |
| emergency roof tarping | 5,704 | 57.1 |
| emergency roof tarp service | 3,087 | 47.8 |
| emergency tarping | 3,079 | 52.9 |

There are now eight service pages, each targeting one of these clusters.

**Kept all nine blog posts verbatim.** They carried 73 of 251 clicks (29%) from
16.5% of impressions, and two ranked on page one — the only pages on the domain
that did. Body copy and FAQs are ported from the originals so no ranking signal
is lost. Note that `emergency-roof-tarp-101` (16 clicks, 14,900 impressions) was
never linked from the old homepage; it is linked properly here.

**141 removed URLs return 410 Gone**, generated into `.htaccess` from
`prune-list.txt`. 410 tells Google the pages are intentionally gone, which
de-indexes them faster than a 404 and, unlike a redirect, does not preserve the
doorway pattern.

## Guard against a repeat

`validate.py` runs a **cross-page near-duplicate scan** and fails the build if
any two pages exceed 60% word-level similarity on their unique body copy
(shared chrome — header, footer, sidebar, CTA bands — is excluded so it cannot
mask real duplication).

Current worst pair is **19.2%**. The old city pages scored **98.2%**.

This is the check that matters. The next person who needs a Tyler page will be
tempted to copy the Waco one and swap the city name — that is precisely how the
site got demoted. Verified by doing exactly that:

```
FAIL  NEAR-DUPLICATE: /service-areas/roof-tarp-hutto/ and
      /service-areas/roof-tarp-tyler/ are 95.1% identical
```

`build.py` also **removes stale pages**: anything under `services/`,
`service-areas/` or `blog/` that the current build did not write is deleted, so
dropping a city from `content/areas.py` actually removes it rather than leaving
it deployed and indexed.

## Rebuilding

```sh
python3 build.py      # regenerate every HTML file
python3 validate.py   # verify the output — run this every time
```

No dependencies beyond the Python 3 standard library. `build.py` writes into
this directory, so generated HTML is committed alongside its source.

Preview with `python3 -m http.server 8000`.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` and the `*/index.html` files | The generated site — the deliverable |
| `build.py` | Generator: shared layout, page templates, schema builders |
| `validate.py` | Post-build checks, including the near-duplicate scan |
| `siteconfig.py` | Business details, navigation, brand constants |
| `content/services.py` | Eight service pages |
| `content/areas.py` | Seventeen metro pages |
| `content/blog.py` | Nine blog posts, ported from WordPress |
| `content/pages.py` | About, FAQs, Contact |
| `content/legal.py` | Privacy policy, terms of use |
| `prune-list.txt` | The 141 removed city slugs; `build.py` turns these into 410 rules |
| `assets/css/site.css` | The single stylesheet |
| `assets/js/site.js` | Mobile nav + form guard (the only script) |
| `assets/img/site-icon-*.png` | Brand icons, carried over from the WordPress media library |
| `google*.html` | Search Console verification files — keep them |

## Page inventory (45 pages)

**Homepage** — `roof tarping services`

**Services** (`/services/`) — one primary keyword each:

| Page | Keyword |
| --- | --- |
| `/services/emergency-roof-tarping/` | emergency roof tarp |
| `/services/roof-tarp-installation/` | roof tarp installation |
| `/services/long-term-roof-tarping/` | long-term roof tarp |
| `/services/residential-roof-tarping/` | residential roof tarping |
| `/services/commercial-roof-tarping/` | commercial roof tarping |
| `/services/storm-damage-roof-tarping/` | storm damage roof tarping |
| `/services/hail-damage-roof-tarping/` | hail damage roof tarping |
| `/services/24-7-roof-tarping/` | 24/7 roof tarping |

**Service areas** (`/service-areas/`) — Houston, Dallas, Fort Worth, Austin,
San Antonio, El Paso, Lubbock, Corpus Christi, Arlington, Waco, McKinney,
Sugar Land, Midland, Beaumont, The Woodlands, Huntsville, Hutto.

Each carries its own county, geography, storm profile, roof-covering mix and
response detail. The storm profile is the real differentiator and it is
genuinely regional: Gulf tropical systems on the coast, hail alley through DFW
and I-35, High Plains wind in Lubbock, desert monsoon and flat roofs in El Paso,
pine fall in the Piney Woods, expansive clay in Fort Bend County.

**Blog** (`/blog/`) — nine guides, ported from WordPress.

**Other** — `/about/`, `/faqs/`, `/contact/`, `/privacy-policy/`,
`/terms-of-use/`, `/sitemap/`, `/404.html`, `/sitemap.xml`, `/robots.txt`,
`/.htaccess`.

## Design

Palette carried over from the live site's Elementor globals so the rebuild keeps
the same brand identity:

- Primary `#18230F`, secondary `#27391C`, accent `#1F7D53`, alert `#D20000`,
  text `#252525`

Type is a system font stack rather than the original's Arial-only rule: it
renders closer to the intended weight on every platform and costs no webfont
request.

## SEO

Every page has a unique title and meta description, a single H1 carrying its
keyword, a canonical URL, Open Graph and Twitter tags, and JSON-LD: a shared
`RoofingContractor`/`LocalBusiness` graph plus per-page `Service`,
`BreadcrumbList`, `FAQPage`, `BlogPosting` or `ItemList` as appropriate.

`validate.py` enforces all of it: valid JSON-LD, exactly one H1, unique titles
and descriptions, no broken internal links or missing assets, keyword presence
in the title and body of every service page, city and county presence on every
area page, sitemap coverage, no WordPress/Elementor fingerprints, no unreplaced
template placeholders, and the near-duplicate scan.

## Deploying

**Not yet deployed.** The build is complete and validated but has not been
pushed to the live server — rooftarp.com is still serving WordPress.

Deploying means uploading this directory to the document root at
`/home/u401386392/domains/rooftarp.com/public_html` (Hostinger account
`u401386392`, order `64270646`). Before doing that:

1. **Back up the WordPress site** — files and database both. The current site is
   the only copy of nine blog posts' original markup.
2. **Check `.htaccess`** merges cleanly with anything the host adds. The
   generated file includes the 410 rules, HTTPS/www canonicalisation, legacy
   sitemap redirects and a 404 document.
3. **Keep `wp-content/uploads/`** in place if any old image URL should keep
   returning 200.
4. **Resubmit `sitemap.xml`** in Search Console and expect the 141 pruned URLs
   to leave the index over the following weeks.

## Known gaps

- **The callback form is not wired up.** It posts nowhere. `site.js` guards it
  so it tells the visitor to call rather than silently swallowing an emergency
  enquiry, but it needs pointing at a form handler or CRM endpoint before this
  matters commercially.
- **No photography.** The WordPress site's images were Elementor-managed and are
  not carried over beyond the brand icons. Real job photographs would
  substantially strengthen the service and area pages.
- **Recovery is not immediate.** Spam-update demotions are typically reassessed
  on the next rollout, so expect months rather than weeks even with a clean fix.
  There is no manual action to appeal.
