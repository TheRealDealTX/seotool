# austinsroofing.com — custom PHP rebuild

This rebuilds the WordPress/Elementor site at https://austinsroofing.com as a plain PHP site. It has no database, no plugins and no build step. The contents of this folder are the whole of `public_html`.

**Hosting:** JWeb Hosting, Hostinger Cloud Enterprise plan. The account username is `u401386392` and the site root is `/home/u401386392/domains/austinsroofing.com/public_html`. The site runs on LiteSpeed, which honors `.htaccess`.

## What's here

| Path | What it is |
| --- | --- |
| `index.php` | Homepage. It says "Austin Roofing" 31 times in the main content; the brief asked for at least 14. |
| `about-us/`, `services/`, `faqs/`, `contact-us/`, `blog/`, `category/general/`, `sitemap/`, `privacy-policy/`, `terms-of-service/` | Every URL carried over from WordPress, with new content |
| `blog/<slug>/` | All 11 WordPress posts at their original URLs, rewritten. Every old heading anchor (`#h-…`) is kept. |
| `services/<slug>/` | **New:** 15 service pages, one keyword each |
| `service-areas/` + 13 area pages | **New:** East Austin, South Austin and 11 surrounding cities |
| `roofing-tools/` + 6 tools | **New:** interactive calculators (see below) |
| `includes/config.php` | Business details plus the registries of services, areas, tools and posts. Every list, nav menu and sitemap is built from these. |
| `includes/layout.php` | Header, footer, schema, and the hero, FAQ, CTA, card and form components. Also the `render_service/area/post/tool()` page templates. |
| `assets/css/site.css`, `assets/js/site.js`, `assets/js/tools.js` | One stylesheet and two scripts, with no dependencies |
| `wp-content/uploads/` | Original WordPress logo, icon, background and blog images at their original paths. Old image URLs keep working. |
| `submit.php` → `thank-you/` | Form handler. It emails `info@austinsroofing.com` and keeps a backup line in `includes/leads.log`. |
| `sitemap-xml.php` | Serves the Yoast URLs `/sitemap_index.xml`, `/page-sitemap.xml`, `/post-sitemap.xml` and `/category-sitemap.xml` |
| `.htaccess` | HTTPS and non-www, clean URLs, sitemap rewrites, 301s for old WordPress paths (`?p=ID`, feeds, date archives, `/wp-admin`, …), caching |
| `.dev/` | Local preview router and validator. Web access is denied and it does not need to be uploaded. |

Brand, logo, icon, images and colors are kept from the original: red `#E62727`, teal `#1E93AB`, green `#00AD48`, charcoal `#363636`, cream `#F3F2EC`. Fonts are Alfa Slab One and Helvetica. Contact details are unchanged: +1 (956) 465-6045 and info@austinsroofing.com. The GA4 property `G-G6C3B8SGY7` is kept.

## SEO approach (from the Search Console export, last 12 months)

- **Homepage** targets *austin roofing* (2,971 impressions), *austin roofing company* (3,119), *austin roof*, *austin roofing contractor*, *austin roofers* and *austin roofing services*.
- **About Us** (5,561 impressions) targets *Austin roofing company*. **Contact Us** (2,576 impressions) targets *austin roofing estimate*. **Services** (1,622 impressions) targets *austin roofing services*.
- **New service pages** cover queries that already had impressions but no dedicated page:
  - roof repair: *austin roofing repair services*, *austin roofing repairs* and *austin roof repair*, about 2,000 impressions combined
  - replacement
  - commercial
  - residential
  - composition shingle
  - multi-family
  - insurance claims
  - hail and wind
  - plus others
- **Blog winners got the most work:**
  - Underlayment types: *roofing felt types* (position 23), *roofing paper types* (position 10)
  - Shingle price per square
  - Storm insurance coverage
  - Architectural vs asphalt shingles
  - Permit requirements / *roof replacement guidelines*
- **Area pages** use real local detail rather than swapped city names. *east austin roofing* and *south austin roofing* both already had impressions.
- **Every page** has:
  - a unique title and meta description
  - one H1
  - a canonical URL
  - Open Graph and Twitter tags
  - JSON-LD: a sitewide `RoofingContractor`/`LocalBusiness` graph, plus `Service`, `BlogPosting`, `FAQPage`, `BreadcrumbList`, `WebApplication` or `ItemList` depending on the page

## Interactive tools and visual effects

- **Roof replacement cost calculator:** size, stories, pitch, shape, material and tear-off → squares and an installed-cost range
- **Roofing square and shingle bundle calculator:** squares, bundles, underlayment rolls, starter, ridge cap, drip edge and nails
- **Roof pitch calculator:** a live SVG roof that redraws as you change the pitch
- **Repair-or-replace quiz**
- **Hail size and damage checker:** an animated hailstone drop
- **Roof lifespan calculator:** an animated gauge

The tools are also embedded on relevant service pages and blog posts. They run entirely in the browser.

**Visual effects:**
- Canvas rain, hail or heat on the heroes, with a Rain/Hail/Heat toggle and lightning flashes on the homepage
- Roof-peak section dividers and a roofline footer
- An animated house illustration whose shingle rows lay themselves on scroll
- A ridge-shaped scroll-progress bar and reveal-on-scroll cards

All motion turns off when the visitor has `prefers-reduced-motion` set.

## Preview and validate locally

```sh
php -S 127.0.0.1:8080 -t austinsroofing.com austinsroofing.com/.dev/router.php
python3 austinsroofing.com/.dev/validate.py
```

The validator crawls every sitemap URL and every legacy WordPress URL. It checks:
- HTTP 200
- one H1
- unique titles and descriptions, at sane lengths
- canonicals
- JSON-LD that parses
- alt text on images
- every internal link and asset
- the old `/services/#…` and blog `#h-…` anchors
- the homepage "Austin Roofing" count

Current result: **57 pages and 89 link targets, 0 errors.**

## Deploying (replaces the live WordPress site)

1. **Back up WordPress first.** In hPanel, download the full backup or zip `public_html` and export the database.
2. Delete the WordPress core files from `public_html`: `wp-admin/`, `wp-includes/`, `wp-*.php`, `xmlrpc.php`, `index.php`, `license.txt`, `readme.html` and `.htaccess`. Delete `wp-content/` **except `wp-content/uploads/`**, so every old image URL keeps working.
3. Upload this folder's contents into `public_html`, skipping `.dev/` and `README.md`.
4. Optional: create `includes/.form-secret` containing a random string. A fallback is used if the file is missing.
5. Send a test through the contact form to confirm Hostinger's `mail()` delivers to `info@austinsroofing.com`. If it doesn't, create that mailbox or an SMTP sender in hPanel.
6. In Search Console:
   - resubmit `https://austinsroofing.com/sitemap_index.xml`
   - inspect the homepage and the top blog post
   - watch Pages → Not found for a couple of weeks

## Things to review before launch

- Cost figures in the tools and posts are labelled typical 2026 planning ranges, not quotes. Adjust them to your real pricing if needed.
- A few smaller subdivision names on area pages are worth a quick local check: Behrens Ranch, Anderson Mill West, Brooklands, Benbrook Ranch and Colovista.
- Several pages state Texas rules in plain language. These are:
  - contractors may not waive deductibles (Ins. Code ch. 707)
  - Texas has no state roofing license
  - HOA limits on impact-resistant shingles (Prop. Code §202.011)
  - a public adjuster can't also be the roofer on a claim (Ins. Code ch. 4102)
