# Prompt: build a new state insurance-appraiser site

Copy everything below the line, fill in the three values at the top, and send it as one message.

---

Build a new insurance appraiser website and put it on Hostinger.

- **DOMAIN:** `example.com`
- **SITE TITLE / MAIN KEYWORD:** `Texas Insurance Appraiser`
- **MAIN COLOR:** `#0f4c5c` (or a color name)

The state is the one named in the site title. Use these fixed details everywhere:
- **Phone:** +1 (844) 537-1427
- **Email:** `info@<DOMAIN>`. I'll create the mailbox later.

Follow everything below without stopping to ask questions. Make sensible choices and tell me what you chose at the end.

## 1. Starting point and sister sites

- Use `georgiainsuranceappraiser/` in this repo as the engineering template. Copy it into a new folder named after the domain without the TLD, for example `texasinsuranceappraiser/`. Reuse the generator, `validate.py`, `deploy.sh`, `api/contact.php`, the tool logic in `app.js`, and the favicon and photo pipelines.
- **The content, URL slugs and design must be new.** This site has to look and read differently from every sister site, not just Georgia. Before writing anything, list the Hostinger Agency websites to find the other `*insuranceappraiser*` sites, such as alabamainsuranceappraiser.com, the Florida site and georgiainsuranceappraiser.com. Skim them so you don't repeat their:
  - layouts
  - section order and headings
  - palettes and fonts
  - URL structure
  - copy
- Write all copy fresh and specific to this state. Cover:
  - its real perils, regions and major cities
  - its counties and county count
  - its insurance regulator, FAIR plan or wind pool
  - its well-known storms
  - its bad-faith statute, described only generally
  
  Stay factual and cautious about legal points. Use no fabricated reviews, testimonials, client results or credentials. Label any example figures as illustrative.
- Add the other states' names to `validate.py`'s banned-word check so no sister-state name leaks into the build.

## 2. Pages

Use URL slugs that differ from the sister sites, and give every page a single main keyword.

- **Home**
- **About** and **Contact**
- **About 10–12 services**, with an index page. Include:
  - appraisal clause representation
  - homeowner
  - commercial / HOA
  - roof & hail
  - wind or tornado
  - hurricane, where relevant to the state
  - water
  - fire & smoke
  - one peril specific to this state, such as sinkhole, wildfire, freeze or tree fall
  - estimate review
  - umpire services
- **About 12 city or location pages**, with an index page. Each needs real local detail: county, neighborhoods, storm history and the housing mix.
- **At least 6 free interactive tools**, with an index page. Use different names and twists from the sister sites, for example:
  - an appraisal value / claim gap estimator with fees
  - an RCV/ACV depreciation & holdback calculator
  - a roof squares & pitch calculator
  - a percentage deductible calculator
  - a claim deadline planner with .ics calendar export
  - an appraisal readiness score
  - one new tool that fits the state
  
  Everything runs in the browser and nothing is stored.
- **Resources:**
  - an appraisal process guide
  - an FAQ grouped by topic
  - a searchable glossary of 35+ terms
  - 5 or more guide articles
- **Other pages:**
  - Privacy, Terms and Disclaimer
  - Photo Credits
  - an HTML site map
  - a 404 page that returns a real 404 status
  - `sitemap.xml` and `robots.txt`
- **Homepage keyword:** the exact SITE TITLE must appear **at least 14 times in the homepage's main content**, not counting the header and footer. Keep it natural. `validate.py` enforces this count.

## 3. Design

The design should be modern, distinct from the sister sites, and built on **MAIN COLOR**.

- **Palette:** build it from MAIN COLOR with a deep shade, a light tint, one complementary accent and neutrals. Use gradients sparingly. Pick a Google Fonts display + body pairing that no sister site uses.
- **Real photos only, no illustrations.** Use royalty-free photos that are CC0 or public domain:
  - Search with the Openverse API (`license=cc0,pdm`). Good sources are StockSnap, rawpixel, Flickr CC0/PD and US government sources like FEMA and USDA.
  - Do not try to get around bot checks on Unsplash or Pexels.
  - Review contact sheets by file label, because index positions shift when a download fails.
  - Skip anything with identifiable political figures, text overlays or artwork.
  - Pick about 30 photos: damage, roofs, storms, homes, commercial buildings, consultations, calculators, and city photos where available.
  - Save each as 1200px and 640px WebP with `srcset`/`sizes` and width/height set.
  - Write descriptive alt text, and use `alt=""` for decorative backgrounds.
  - List every photo with its license and source on `/photo-credits/`.
- **Layout:**
  - a full-bleed photo hero with a lead form
  - photo cards for services, tools, guides and locations
  - photo heroes on interior pages
  - a two-column interior layout with a sticky sidebar holding a call box and related links
- **Effects:** use some of these, but choose a different mix and arrangement from the sister sites:
  - scroll progress bar
  - header that turns solid on scroll
  - hero zoom or parallax
  - staggered reveal on scroll
  - animated counters
  - hover zoom on cards
  - 3D tilt
  - marquee
  - a process timeline that fills as you scroll
  - region tabs with photos
  - parallax CTA
  - back-to-top button
  
  Respect `prefers-reduced-motion`, and make sure the page still renders correctly without JavaScript.
- **Mobile navigation:** use an off-canvas drawer placed **outside** the sticky header. A `backdrop-filter` on the header traps `position: fixed` children, which broke the first Georgia version. The drawer needs:
  - accordion submenus
  - scroll lock while open
  - closing with ×, an overlay tap, a link tap or Escape
  - `inert`/`aria` state handling
  - its shadow and visibility applied only while it's open, so no haze shows at the screen edge
  
  Add a fixed mobile call bar at the bottom.
- **Known pitfalls to avoid:**
  - SVG icons inside buttons need an explicit size.
  - Tools placed in colored sections must reset text color.
  - Links on dark backgrounds need a light color.
  - Grid children need `min-width: 0`.
  - There must be no horizontal scroll at 390px wide.
- **Logo and favicon:** design a simple mark in the brand colors. Generate:
  - `favicon.svg`
  - a multi-size `favicon.ico` (16/32/48) using a bolder version for small sizes
  - a 96px PNG
  - a full-bleed 180px `apple-touch-icon`
  - maskable 192/512 PNGs listed in `site.webmanifest`
  
  Add a `?v=` cache-buster to every icon link. Use the same mark in the header and footer. Make a 1200×630 JPG OG image using a site photo.

## 4. SEO and schema

`validate.py` must pass with **zero errors**. It checks:

- every title is **60 characters or fewer and about 580px or less**, estimated with Arial metrics at 20px
- every meta description is **110–150 characters**
- titles and descriptions are unique
- each page has **exactly one H1**, the first heading is the H1, and **no heading level is skipped**, including in the footer, sidebar boxes and tool widgets
- JSON-LD is valid
- there are no broken internal links or anchors
- every image has an `alt` attribute
- the homepage keyword count is met
- no sister-state names appear

Every page also needs:
- a canonical URL to `https://<DOMAIN>/...`
- Open Graph tags with image size and alt, plus Twitter card tags and `geo.region`

Every page's JSON-LD `@graph` should contain:
- a ProfessionalService node with:
  - logo ImageObject
  - contactPoint
  - addressRegion and country
  - the state and cities as areaServed
  - an OfferCatalog of the services
- a WebSite node
- **one page node** (WebPage, AboutPage, ContactPage or CollectionPage) linked to its BreadcrumbList `@id`, primaryImageOfPage and mainEntity

Add these where they apply:
- Service on service and location pages
- FAQPage
- ItemList on index pages
- WebApplication on tool pages
- BlogPosting on guides
- HowTo on the process page
- DefinedTermSet on the glossary

Check that every `@id` reference resolves.

## 5. Contact form

- `api/contact.php` must have a honeypot, a per-IP rate limit and validation.
- It sends through `info@<DOMAIN>` using authenticated SMTP (`smtp.hostinger.com:465`) when `api/_private/config.php` exists, and falls back to `mail()`. It always appends to `api/_private/leads.log.php`.
- Both private files must return 404 when requested directly. The config defines-guard and the log's `<?php exit;` header do this.
- Hostinger's file API can't write outside `public_html`, so that's where they go.
- **Never commit credentials.** Add `_private/` to `.gitignore`.
- When I later send the mailbox password:
  1. Upload the config.
  2. Confirm the config URL returns 404 with 0 bytes.
  3. Send one submission labelled as a test.
  4. Confirm the log shows `"via":"smtp"`.

## 6. Google Tag Manager

- Leave a `GTM_ID` constant that is empty by default. When it's set, output the head snippet and the `<noscript>` iframe after `<body>`.
- If I give you a GTM container ID or snippet, use it exactly as provided.

## 7. Hostinger deployment

1. Create a new **Agency Growth** website on order `1008744732`. Use `php-fpm`, PHP 8.3 and **no domain**, so you get a temporary `*.hostingersite.com` URL. Pick the datacenter nearest the state, for example Boston for the East and Phoenix for the West.
2. Poll the setup until it finishes.
3. The host ignores `.htaccess` and serves an `index.html` for unknown paths. So **don't create a root `index.html`**. Render the homepage as `home.html` and generate an `index.php` front controller that:
   - serves `home.html` for `/`
   - redirects to add a trailing slash on directories
   - returns `404.html` with a real 404 status
   - sends `X-Robots-Tag: noindex` on any host that isn't `<DOMAIN>`
   - 301-redirects `www.` and plain http to `https://<DOMAIN>`, only on the real domain
4. Deploy `public/` with `deploy.sh`, using the TUS upload API with fresh credentials from `agency-hosting_files_generate-upload-url`.
5. Delete Hostinger's placeholder `public_html/default.php`, then clear the cache.
6. Verify the live site:
   - status codes for pages, a missing page and a no-trailing-slash URL
   - assets load and there are no console errors
   - the form endpoint rejects invalid input

## 8. Quality checks before reporting back

- Run `build.py`, then `validate.py` with zero errors.
- Use Playwright with the preinstalled Chromium:
  - Take desktop (1440px) and mobile (iPhone 13) screenshots of the home, service, location and tool pages, and review them visually.
  - Check that `scrollWidth` matches the viewport.
  - Check that every image loads after scrolling.
  - Test every tool's math.
  - Test the mobile drawer end to end: open it, expand a section, tap a link and land on the right URL, then close it all three ways.
- Repeat a quick check on the live temporary URL after deploying.

## 9. Git and report

- Commit on the designated branch with a clear message, then push. Update the folder's README with:
  - website UID and temporary URL
  - build and deploy steps
  - hosting notes
  - photo sourcing
  - the SEO rules
  - form setup
- Report back:
  - the temporary URL and website UID
  - the page count and the homepage keyword count
  - palette and fonts
  - anything I need to do

## 10. When I connect the domain later

1. Confirm the domain is on the website and SSL is active.
2. Check that www and http redirect and that the real domain has no noindex header.
3. Add the GTM tag if I provide it, and wire SMTP once I give the mailbox password (section 5).
4. Re-run `validate.py`, redeploy and clear the cache.
5. Remind me to submit `https://<DOMAIN>/sitemap.xml` to Search Console.
