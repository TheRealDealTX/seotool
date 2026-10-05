# austinlandscapelighting.com — custom PHP rebuild

A hand-built PHP/HTML site for [Austin Landscape Lighting](https://austinlandscapelighting.com),
replacing the WordPress/Elementor install. No CMS, no database, no framework:
one front controller, a small template library, content as PHP arrays, one
stylesheet, two scripts and local images. Runs on any PHP 8.2+ host.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical host/scheme, legacy WordPress redirects, trailing-slash rule, route table, 404 |
| `config.php` | Business facts, service/area/tool order, nav, reviews, process steps |
| `lib/` | `render.php` (page shell, header, footer), `components.php` (hero, cards, FAQ, forms, compare slider…), `tools.php` (markup for the interactive tools and the SVG night scene), `schema.php` (JSON-LD), `content.php` (loaders), `icons.php`, `helpers.php` |
| `pages/` | One template per route: home, services, service, areas, area, blog, post, tools, tool, gallery, about, contact, contact-send (form handler), reviews, faq, privacy, terms, sitemap, sitemap-xml, thank-you, 404 |
| `content/services/*.php` | 12 service pages (title, description, intro, highlights, planning range, body HTML, FAQs) |
| `content/areas/*.php` | 12 city pages with neighborhoods, ZIPs, landmarks, coordinates, body, FAQs |
| `content/posts/*.php` | 12 blog posts (2 ported from WordPress, 10 new) |
| `assets/css/site.css` | The stylesheet (dark night palette, warm 2700K accents, Fraunces + Manrope) |
| `assets/js/site.js` | Header, nav, scroll progress, reveal-on-scroll, parallax, counters, cursor spotlight, card tilt, hero canvas (stars + fireflies), lights-off toggle, compare slider, lightbox, map, TOC |
| `assets/js/tools.js` | The eight calculators/tools |
| `assets/img/` | 142 photos from the old media library, resized to 1600px (`thumbs/` at 720px); `brand/` holds the logo, icon and OG image |
| `validate.py` | Crawls the site on PHP's built-in server and checks links, assets, H1s, titles, JSON-LD, alt text, keyword placement, sitemap coverage |
| `deploy.sh` | Uploads the tree to the Hostinger Agency website via the File Browser TUS API |
| `backup/` | Content-level backup of the WordPress site taken before the switch |

## Running locally

```sh
php -S 127.0.0.1:8080 index.php    # then open http://127.0.0.1:8080/
python3 validate.py                 # crawl + checks (starts its own server)
```

## Pages (57)

- **Home** `/` — primary keyword *Austin Landscape Lighting* (25 mentions in the page copy; `validate.py` enforces at least 14). Hero with an animated SVG night scene and a site-wide "flip the switch" toggle, stats counters, city marquee, 12 service cards, lights-off/lights-on compare slider, interactive technique explorer, why-us, process with scroll-filled line, parallax quote band, tools grid with an embedded fixture calculator, reviews, service-area chips, gallery strip with lightbox, latest posts, FAQ (FAQPage schema), contact form.
- **Services** `/services/` + 12 pages: architectural-uplighting, path-and-walkway-lighting, garden-and-tree-lighting, deck-and-patio-lighting, pool-and-water-feature-lighting, smart-lighting-systems, led-upgrade-and-retrofit, security-and-safety-lighting, commercial-landscape-lighting, maintenance-and-repair, custom-lighting-design, low-voltage-landscape-lighting.
- **Service areas** `/service-areas/` (interactive SVG map) + 12 pages: austin, round-rock, cedar-park, pflugerville, georgetown, bee-cave, lakeway, westlake-hills, rollingwood, kyle, buda, dripping-springs.
- **Tools** `/tools/` + 8 pages: fixture-calculator, cost-estimator, lighting-visualizer, led-savings-calculator, transformer-calculator, color-temperature-guide, sunset-timer (NOAA solar math for Austin), lighting-style-quiz. Tools can be embedded in posts with `<!-- TOOL:slug -->`.
- **Blog** `/blog/` + 12 posts at root-level URLs (the WordPress permalink structure, so the two existing posts keep their URLs): how-many-landscape-lights-do-i-need, best-front-yard-landscape-lighting-ideas, backyard-landscape-lighting-ideas, landscape-lighting-ideas-for-trees, landscape-lighting-ideas-for-pools, modern-landscape-lighting-ideas, solar-vs-low-voltage-landscape-lighting, landscape-lighting-design-guidelines, how-to-design-landscape-lighting, landscape-lighting-cost-in-austin, how-to-choose-a-landscape-lighting-company-in-austin, outdoor-landscape-lighting-ideas.
- **Other** — `/gallery/` (142 photos, filterable, lightbox), `/about-us/`, `/reviews/`, `/faq/`, `/contact/`, `/thank-you/`, `/privacy-policy/`, `/terms-of-service/`, `/sitemap/`, `/sitemap.xml`, `/robots.txt`, 404.

Legacy WordPress paths redirect: `/feed/`, `/category/*` → `/blog/`; `/wp-*`, `/xmlrpc.php` → `/`; the Yoast sitemaps → `/sitemap.xml`; `/blog/<post>/` → `/<post>/`.

## Contact form

`/contact/send` validates the fields, drops bot submissions (honeypot + 3-second
timing check), emails `info@austinlandscapelighting.com` via PHP `mail()` with
the visitor as Reply-To, appends the lead to `../leads/leads.log` (outside the
document root, best effort) and redirects to `/thank-you/`. If `mail()` reports
failure the thank-you page asks the visitor to also call. Hostinger's php-fpm
websites deliver `mail()` through the platform MTA; if deliverability is poor,
point the handler at an SMTP service or form endpoint.

## SEO

Every page has a unique title and description, a single H1, canonical, Open
Graph and Twitter tags, and a JSON-LD graph: a shared
`HomeAndConstructionBusiness`/`LocalBusiness` node (Austin, areaServed = the 12
cities, hours, offer catalog) plus per-page `WebPage`, `BreadcrumbList`,
`Service`, `FAQPage`, `BlogPosting`, `ItemList`, `WebApplication` (tools) or
`ImageGallery`. Service, area and post pages each carry their own keyword in
title, description, H1 and body. Legal pages are `noindex`.

## Deploying

Hostinger Agency website **UID `64Mujs88W`** (php-fpm 8.5, Phoenix, created
2026-10-05 to replace the WordPress website `1AbSzNVGl`). Deployed and the
domain moved on 2026-10-05; the existing SSL certificate carried over. Get upload
credentials with the Hostinger API operation
`agency-hosting_files_generate-upload-url` and run:

```sh
export ALL_FB_URL='…' ALL_FB_AUTH='…' ALL_FB_REST='…'
python3 validate.py && ./deploy.sh
```

then clear the cache (`agency-hosting_cache_clear-website`). The platform serves
existing files directly and routes everything else to `index.php`; it ignores
`.htaccess`, so all redirects live in `index.php`. There is deliberately no
`index.html`.

The old WordPress website (`1AbSzNVGl`) was left in place; releasing the domain
moved it to the temporary domain `ghostwhite-flamingo-551464.hostingersite.com`,
so it can be re-linked if anything needs to roll back. Delete it from hPanel once the new site has been live for a while.
