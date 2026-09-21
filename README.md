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
| `build.py` | Generator: shared layout, page templates, schema builders |
| `siteconfig.py` | Business details, locality facts, navigation |
| `content/` | Page copy — services, service areas, blog, legal |
| `validate.py` | Post-build checks (run it after every build) |

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

**Blog** (`/blog/`) — six Central Texas homeowner guides.

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

## SEO

Every page has a unique title and meta description, a single H1 carrying its
keyword, a canonical URL, Open Graph and Twitter tags, and JSON-LD: a shared
`RoofingContractor`/`LocalBusiness` graph plus per-page `Service`,
`BreadcrumbList`, `FAQPage`, `BlogPosting` or `ItemList` as appropriate. The
LocalBusiness data carries Hutto's address, 78634 postcode, coordinates and the
`areaServed` list.

`validate.py` enforces this: valid JSON-LD, one H1, unique titles and
descriptions, no broken internal links or missing assets, alt text on every
image, no WordPress or source-city leftovers, and keyword presence in the title,
H1, meta description and body of each money page.

## Known gaps

- **The blog brief was truncated.** The task description cut off mid-list at
  "how much does a", so the first post matches that opening and the other five
  cover the questions that most commonly accompany it. See the note at the top
  of `content/blog.py`; the list is a plain Python list and easy to extend.
- **The estimate form is not wired up.** It posts nowhere and shows a reminder
  on submit. Point it at a form handler or CRM endpoint before going live
  (`contact_section()` in `build.py`, and the submit handler in
  `assets/js/site.js`).
- **Cost figures are planning ranges**, not quotes, and are labelled as such on
  the pages. Review them before publishing.
