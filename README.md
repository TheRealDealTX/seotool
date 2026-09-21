# huttoroofs.com — static rebuild

A static HTML rebuild of [huttoroofs.com](https://huttoroofs.com), replacing the
WordPress/Elementor site. No PHP, no database, no plugins — just HTML, one CSS
file, one JS file and local images. Upload the repo root to any web host.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` and the `*/index.html` files | The generated site — this is the deliverable |
| `assets/css/site.css` | The single shared stylesheet |
| `assets/js/site.js` | Sticky header + mobile nav (the only script) |
| `assets/img/` | All images, downloaded from the original site |
| `favicon.*`, `apple-touch-icon.png`, `site.webmanifest`, `web-app-manifest-*.png`, `googlecccfbf2f7e9e5ae4.html` | Root files carried over from the WordPress install (icons, PWA manifest, Google Search Console verification) — keep them |
| `build.py` | Generator: shared layout, page templates, schema builders |
| `siteconfig.py` | Business details, locality facts, navigation |
| `content/` | Page copy — services, service areas, blog, legal |
| `validate.py` | Post-build checks (run it after every build) |
| `templates/blog-post.html` | Generated blog post template for drop-in posts |

## Rebuilding

```sh
python3 build.py      # regenerate every HTML file
python3 validate.py   # verify the output
```

No dependencies beyond the Python 3 standard library. `build.py` writes into the
repo root, so the generated HTML is committed alongside its source.

Preview locally with `python3 -m http.server 8000`.

## Page inventory (29 pages)

**Homepage** — `roofing hutto tx`

**Services** (`/services/`) — one primary keyword each:

| Page | Keyword |
| --- | --- |
| `/services/roof-repair-hutto-tx/` | roof repair hutto tx (+ roof leak repair hutto tx) |
| `/services/roof-replacement-hutto-tx/` | roof replacement hutto tx |
| `/services/roof-installation-hutto-tx/` | roof installation hutto tx |
| `/services/hail-damage-roof-repair-hutto-tx/` | hail damage roof repair hutto tx |
| `/services/storm-damage-roof-repair-hutto-tx/` | storm damage roof repair hutto tx |
| `/services/shingle-roofing-hutto-tx/` | shingle roofing hutto tx |
| `/services/metal-roofing-hutto-tx/` | metal roofing hutto tx |
| `/services/roof-inspection-hutto-tx/` | roof inspection hutto tx |
| `/services/commercial-roofing-hutto-tx/` | commercial roofing hutto tx |
| `/services/emergency-roof-repair-hutto-tx/` | emergency roof repair hutto tx |

**Service areas** (`/service-areas/`) — Round Rock, Pflugerville, Taylor,
Georgetown, Manor. Each carries its own local detail (neighborhoods, drive time
from Hutto, storm pattern, county) and links back to the Hutto homepage.

**Blog** (`/blog/`) — six Central Texas homeowner guides, one keyword each:

| Page | Keyword |
| --- | --- |
| `/blog/how-much-does-a-roof-replacement-cost-in-hutto-tx/` | how much does a roof replacement cost in hutto tx |
| `/blog/best-roofing-materials-for-central-texas-heat/` | best roofing materials for central texas heat |
| `/blog/shingle-vs-metal-roofing-which-is-right-for-you/` | shingle vs metal roofing |
| `/blog/signs-you-need-a-new-roof/` | signs you need a new roof |
| `/blog/how-long-does-a-roof-last-in-texas/` | how long does a roof last in texas |
| `/blog/how-to-choose-a-roofing-contractor-in-hutto/` | how to choose a roofing contractor in hutto |

**Other** — `/privacy-policy/`, `/terms-of-use/`, `/sitemap/`, `/404.html`,
`/sitemap.xml`, `/robots.txt`.

## How the content was sourced

The original huttoroofs.com was a four-page site: homepage plus two legal pages
and a sitemap. The sister sites (templeroofs.com, kyleroofs.com,
copperascoveroofs.com) turned out to be the same single-page template with a
different city name, so there were no service or area pages to port. What they
supplied was the page architecture, section structure and writing voice; the
service, area and blog pages here are written fresh against that pattern.

Everything local is Hutto's own: **Williamson County**, **78634**, neighborhoods
(Legends of Hutto, Star Ranch, Emory Farms, Creek Bend, Cottonwood Creek,
Riverwalk), landmarks (Old Town Hutto, the Co-Op District, Brushy Creek, US-79,
SH-130, FM 1660, Chris Kelley Boulevard) and Blackland Prairie weather. Nearby
cities are Round Rock, Pflugerville, Taylor, Georgetown and Manor. The business
name and phone number are Hutto Roofers' own throughout — nothing from the
source sites was carried over.

The homepage hero paragraph and its "Local Roofing Focus" section were rewritten
so the page is not a near-duplicate of templeroofs.com.

## Design

Header, nav, footer, colors and fonts are reproduced from the original. The
palette and type were lifted from the live site's own CSS:

- Ink `#151513`, gold `#9a7324`, gold-2 `#c29a49`, cream `#f8f5ee`, paper `#fffdfa`
- DM Serif Display for headings, DM Sans for body (Google Fonts)

The original's header and footer were Elementor templates, so those are rebuilt
here using the `.announcement` / `.site-header` / `.site-footer` classes that
the site's own stylesheet already defined but did not use. Interior pages
(services, areas, blog) add a compact hero, a prose/sidebar layout and a few
components on top of the same tokens.

## Deploying

The site is live on the Hostinger Agency website UID `Y2Ln5wYMP`
(huttoroofs.com; created 2026-09-21 as a plain php-fpm website to replace the
WordPress website `Kq0nqTlGe`, which was deleted after the domain moved).
`./deploy.sh` pushes the build through the website's File Browser upload API;
its header comment explains the three credentials it needs. Clear the site
cache afterwards.

Deployed 2026-09-21. The WordPress site was backed up first — see
`backup/wordpress-2026-09-21/README.md` for the files zip, database dump and
restore steps.

## Hosting note

The site runs on a plain (php-fpm, no WordPress) Hostinger Agency website,
which serves the files directly and returns a real 404 for unknown paths.
`wp-content/uploads/2026/09/` holds the old WordPress media library exactly
as it was, so every image URL the old site ever exposed still returns 200;
the static pages themselves use `/assets/img/`.

## SEO

Every page has a unique title and meta description, a single H1 carrying its
keyword, a canonical URL, Open Graph and Twitter tags, and JSON-LD: a shared
`RoofingContractor`/`LocalBusiness` graph plus per-page `Service`,
`BreadcrumbList`, `FAQPage`, `BlogPosting` or `ItemList` as appropriate. The
LocalBusiness data carries Hutto's address, 78634 postcode, coordinates and the
`areaServed` list.

`validate.py` enforces this: valid JSON-LD, one H1, unique titles and
descriptions, no broken internal links or missing assets, alt text on every
image, keyword presence in the title, H1, meta description and body of every
service, area and blog page, and — per the brief's QA step — no leftover
source-city names, counties, zip codes, phone numbers or WordPress
fingerprints anywhere in the build (only Hutto's 78634 and (512) 297-7580 may
appear).

## Adding a blog post

Two ways, both end with `python3 build.py && python3 validate.py`.

**As an HTML file (no Python):** copy `templates/blog-post.html` to
`blog/<slug>/index.html` and replace the `{{PLACEHOLDERS}}` — the comment at
the top of the template lists them. `build.py` finds any `blog/*/index.html` it
did not generate itself, reads the title, description, H1 and
`article:published_time`, and adds it to `/blog/` and `sitemap.xml`. The
template is regenerated on every build from the live design, so it never
drifts.

**In Python:** add a dict to `POSTS` in `content/blog.py`. This is what the six
existing posts use, and it gives you the shared phone/business constants.

`templates/` is excluded from the sitemap, from validation and from the deploy
archive, and `robots.txt` disallows it.

## Known gaps


- **The estimate form is not wired up.** It posts nowhere and shows a reminder
  on submit. Point it at a form handler or CRM endpoint before going live
  (`contact_section()` in `build.py`, and the submit handler in
  `assets/js/site.js`).
- **Cost figures are planning ranges**, not quotes, and are labelled as such on
  the pages. Review them before publishing.
