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

**141 removed URLs return 410 Gone**, generated from `prune-list.txt` into
`index.php` (the Agency platform ignores `.htaccess`) and into `.htaccess` for
Apache hosts. 410 tells Google the pages are intentionally gone, which
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
| `home.html`, `index.php` and the `*/index.html` files | The generated site — the deliverable (`index.php` serves `home.html` at `/` and returns the 410s; see Deploying) |
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

**Cut over at the platform level on 2026-09-21; DNS delegation pending.**

| | |
| --- | --- |
| Agency website UID | `xilM91tbv` (order `1008744732`, `phoenix`, php-fpm 8.5) |
| Primary domain | `rooftarp.com` (attached 2026-09-21 19:20 UTC via `changeWebsiteDomain`) |
| Platform nameservers for this domain | `pixel.dns-parking.com`, `byte.dns-parking.com` |
| Registrar | GoDaddy — delegation still `ns1`/`ns2.dns-parking.com` (the old cloud pair) |
| Deployed from | `deploy.sh` (56 files via the File Browser TUS endpoint) |

Verified on the preview host before cutover: kept pages 200, the 141 pruned
city URLs **410**, unknown paths 404, legacy sitemap and feed URLs 301,
`sitemap.xml` 42 URLs. The preview host's platform-injected `Googlebot /
Disallow: /` is preview-only (huttoroofs.com on the same platform serves its
real `robots.txt`).

### What happened to the WordPress site

The cloud-plan website `rooftarp.com` (account `u401386392`) and its database
`u401386392_BlNOR` **no longer exist**. Four API delete calls returned 400,
but the website disappeared from the account shortly afterwards — either one of
those requests was accepted asynchronously after all, or it was removed in
hPanel. Its DNS zone on `ns1`/`ns2.dns-parking.com` went with it. The 176-page
content archive in `backup/wordpress-2026-09-21/` is the only copy of that
site; there is no database export.

### Finishing the cutover

The Agency platform provisions this domain's zone on `pixel`/`byte`, and the
control case proves the pair matters: huttoroofs.com's registrar delegation is
exactly the `lunar`/`solar` pair its platform reports. Until GoDaddy delegates
rooftarp.com to `pixel`/`byte`, public DNS is SERVFAIL and the site is dark.

1. **GoDaddy → rooftarp.com → DNS → Nameservers → Change → "I'll use my own"**
   → `pixel.dns-parking.com`, `byte.dns-parking.com`. Propagation is usually
   minutes to an hour.
2. Once `rooftarp.com` resolves: `agency-hosting_reinstallWebsiteSSLV1(xilM91tbv,
   rooftarp.com)` (the setup the platform auto-started at link time will have
   failed on the missing DNS), then poll `getWebsiteSSLStatusV1` until `active`.
3. `agency-hosting_clearWebsiteCacheV1(xilM91tbv)`.
4. Verify `https://rooftarp.com/` (title, a pruned slug → 410, real
   `robots.txt`), then resubmit `sitemap.xml` in Search Console.

**Email:** rooftarp.com has no Hostinger mail order, so whatever served
`info@rooftarp.com` (MX records) lived in the deleted zone and is not known
here. Re-create MX/SPF/DKIM in the new zone from the email provider's records.

Redeploying later: `python3 build.py && python3 validate.py && ./deploy.sh`
with fresh credentials from `agency-hosting_generateUploadURLV1(xilM91tbv)`.

### `deploy/rooftarp` branch

`make-deploy-branch.sh` maintains an orphan branch whose root is the document
root (56 servable files, no source, no backup archive). It is a public,
zip-downloadable copy of exactly what is deployed; the Agency site itself is
deployed with `deploy.sh`.

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
