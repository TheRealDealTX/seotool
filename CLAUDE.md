# CLAUDE.md

This repo is the static rebuild of huttoroofs.com (see README.md). It also holds
notes and source for related sites the owner runs on Hostinger, under `affiliate/`.
`deploy.sh` skips `affiliate/` and this file, so none of it ships to huttoroofs.com.

## Amazon affiliate links

- Associates tag: `josephrayditt-20`. Product links: `https://www.amazon.com/dp/<ASIN>/?tag=josephrayditt-20`;
  fall back to a tagged search (`/s?k=<query>&tag=…`) only when no ASIN can be verified.
- amazon.com returns 503 to fetches from the cloud sandbox. Find ASINs with WebSearch
  restricted to `amazon.com` / `camelcamelcamel.com` and only use an ASIN a source ties to the product title.
- Every site with links needs: a disclosure line in posts with boxes, the footer line
  "As an Amazon Associate, <Site> earns from qualifying purchases.", and an Amazon Associates
  section in the privacy policy. Links use `rel="sponsored nofollow noopener"`. No prices or star ratings.

## Hostinger: how to edit files

Two hosting accounts, two different situations:

**Agency plan sites (username u914589053), e.g. puregoatfarms.com, huttoroofs.com: writes WORK.**
1. Get credentials: `agency-hosting_files_generate-upload-url` with the site's `website_uid`
   (find it via `agency-hosting_websites_list-plan` + `domain` filter). Keys expire after a few hours.
2. The returned `url` ends in `/api/tus`; the File Browser REST API is the same base with `/api`:
   - list: `GET {base}/api/resources/public_html/<dir>/`
   - download: `GET {base}/api/raw/public_html/<file>`
   - delete: `DELETE {base}/api/resources/public_html/<file>`
   - upload: TUS `POST` then `PATCH` to `{base}/api/tus/public_html/<file>?override=true`
     (see `deploy.sh`). Headers on every call: `X-Auth: <auth_key>`, `X-Auth-Rest: <rest_auth_key>`.
3. **`wp-content/mu-plugins/` is locked (403)** — Hostinger keeps its own plugins there. Every
   other folder is writable. Hostinger's `wordpress_plugins_activate` does not cover Agency sites,
   so a normal plugin can't be activated from here either.
4. **Working pattern for WordPress:** upload the code as a plugin file in
   `wp-content/plugins/<name>/<name>.php`, then append a guarded loader line to the active theme's
   `functions.php` (download a backup first, upload, check pages, restore the backup on any error).
   A theme update overwrites `functions.php` and drops the loader — re-add it if boxes disappear.
   Activating the plugin in wp-admin makes it survive theme updates (the loader guard avoids a double load).

**Web hosting account (username u401386392, Cloud Enterprise order 64270646), e.g. rodeotexas.org: writes BLOCKED.**
- `hosting_files_website-content` and `hosting_files_list-website-and-directories` read files fine.
- `hosting_files_generate-upload-url` returns `404 [Hosting:9999] Not found` for every site on the
  account, including the main domain jmautida.com (checked 2026-10-03; reconnecting the connector
  did not help). No Git deployment is connected. Needs a fix from Hostinger support before Claude can write.

## puregoatfarms.com (Agency, website_uid VSUHIRjmA, WordPress + Elementor, theme hello-elementor) — LIVE

- Plugin source: `affiliate/puregoatfarms/pgf-amazon-affiliate.php`, deployed to
  `public_html/wp-content/plugins/pgf-amazon-affiliate/pgf-amazon-affiliate.php`.
- Loaded by the line in `affiliate/puregoatfarms/functions-php-loader.txt`, appended to the end of
  `public_html/wp-content/themes/hello-elementor/functions.php` (Hello Elementor 3.4.9).
- It adds boxes via the `the_content` filter (post content in the DB is untouched): 7 on
  "how-many-goats-do-you-need-to-make-cheese", 6 on "how-much-milk-can-a-goat-really-give-at-once",
  a "Dairy goat essentials" box at the end of any other post, a disclosure paragraph, a footer
  line, and an Amazon section appended to the privacy-policy page.
- Edit products in `pgf_aff_products()` and placements in `pgf_aff_placements()`
  (slug => [heading text, box title, product keys]); boxes go at the end of the matching section.
- Verified live 2026-10-03: all pages 200, no PHP errors, 13 boxes, footer and privacy text present.

## shineyourlightblog.com (web hosting account u401386392, WordPress + Elementor + Yoast + LiteSpeed Cache)

- Amazon tag for THIS site: `shineyourlightblog-20` (josephrayditt-20 and arriveoutdoors-20 links already in
  older posts are also the owner's; leave them).
- Hostinger can't write to this account, so edits go through the WordPress REST API with an Application
  Password for user `claude` (administrator). The password is not stored here: ask the owner, or have
  them create a new one in wp-admin → Users → Profile → Application Passwords.
- 2026-10-03: affiliate links added to ~1,150 of 1,892 posts. Everything added is wrapped in
  `<!-- shine-aff -->…<!-- /shine-aff -->` (disclosure paragraph + "Products we recommend" html block);
  inline links carry `rel="sponsored nofollow noopener"` and the tag. Posts that already had Amazon links
  were skipped. The 30 highest-traffic posts (GA, Sept 2026) got hand-picked products; the rest used
  keyword/topic rules. WordPress revisions hold the pre-edit version of every post.
- Gotcha: the disclosure is the first paragraph, so posts without an excerpt would get it as their
  Yoast og:description. Each edited post was given an explicit excerpt equal to WordPress's own
  auto-excerpt of the ORIGINAL content (first 55 words). Do the same for any future edits.

## 360carseat.com (web hosting account u401386392, WordPress + Elementor + Yoast + LiteSpeed Cache)

- Amazon tag for THIS site: `360carseat-20`. Edits go through the WordPress REST API with an Application
  Password ("Claude affiliate") for login `info@360carseat.com` (administrator; the username is the email).
  The password is not stored here.
- 2026-10-05: affiliate links added to 302 of 331 posts (56 hand-picked top-traffic posts from GA
  Jul–Oct 2026, 246 by rules), wrapped in `<!-- 360aff -->` markers, box class `carseat-aff-box`.
  Excerpts set to the original auto-excerpt (same Yoast gotcha as shineyourlightblog.com).
  Amazon Associates section appended to the privacy policy page (id 3).
- Safety rule for this niche: never link products that attach to a car seat or its harness (strap
  covers, inserts, under-seat protectors, mirrors on the seat) — manufacturers warn they aren't crash-tested.
- Joie Spin 360 / i-Spin 360 are not sold on Amazon US; posts about them link the Joie Chili Spin (US
  version) in the box only, never as an inline link on "Joie Spin 360" text. Nuna REVV uses a tagged
  search link (no ASIN could be verified as the REVV).

## underdeskelliptical.com (Agency plan, WordPress + Elementor + Yoast + LiteSpeed Cache)

- Amazon tag for THIS site: `underdeskellipticaljditt-20`. REST login `admin` (administrator) with an
  Application Password named "Claude Affiliate" (not stored here).
- 2026-10-05: every post hand-planned (53 of 55 edited) — brand reviews link the reviewed model; topic posts
  link matching picks (motorized/manual/compact, walking pad, under-desk treadmill or bike, Fitbit for the
  steps post). Wrapped in `<!-- udeaff -->`, box class `ude-aff-box`, original auto-excerpts set.
  Privacy policy and /affiliate-disclosure/ already covered Amazon, so pages were not edited.
- Posts 95 (DeskCycle Ellipse review) and 86 (Cubii Pro HD review) were left alone: they already link
  Amazon with josephrayditt-20. Note the Cubii Pro HD post's link actually goes to the Cubii JR1 (B074F1S194).
- Viamotion, Fousae, Geoneo, Fntkech and Flex Fitness have no Amazon listing naming the brand: tagged
  search links are used for those.
- All verified live: 53/53 posts 200 with one box, tagged links, disclosure, unchanged og:description.

## carstereooutlethouston.com (WordPress + Elementor + Yoast; Amazon-affiliate storefront)

- Amazon tag for THIS site: `carstereohouston-20`. REST login `nancy` (administrator), Application Password
  "Claude Affiliate" (not stored here). Post URLs are `/post/<slug>/`; products are a `product` post type
  at `/post/product/<slug>/` (27 listings, each already has a tagged amzn.to buy button — left alone).
- 2026-10-05: 7 of 8 blog posts got hand-placed boxes + inline links (`<!-- csoaff -->`, box class
  `cso-aff-box`), reusing the store's own products where they fit plus verified gap products (CarPlay /
  Android Auto adapters, FM transmitter, aux receiver, Pioneer DMH-W2770NEX, Pioneer/Rockford speakers,
  amp, PS-8 sub, LC2i). Post 371 (store launch) left alone. Amazon Associates section added to the
  privacy policy. Original auto-excerpts set.

## rodeotexas.org (web hosting account u401386392, custom PHP app) — BUILT, NOT DEPLOYED

- Changes are ready in `affiliate/rodeotexas/update/` (paths relative to `public_html`);
  `affiliate/rodeotexas/original/` holds exact copies of the live files they replace.
  New `includes/affiliate.php` injects boxes at render time into `pages/article.php` (36 boxes on 14
  articles), adds a sidebar card to articles and upcoming event pages (`pages/event.php`), a footer
  line (`includes/footer.php`) and an Amazon section (`pages/privacy.php`).
- Blocked by the upload 404 above. Once writes work: upload the 5 update files, check pages.
- **Security to-do:** `public_html/_install_87ded30003069ca5.php` (one-time installer with a working
  token) and `public_html/rodeotexas-package.zip` (the Sept 30 build) are still on the server.
  Its steps can overwrite the live site with the old package or reset the admin password.
  Delete both as soon as there is write access.
