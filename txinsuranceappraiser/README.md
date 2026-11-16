# txinsuranceappraiser.com — custom PHP rebuild

A custom HTML/PHP site that replaces the WordPress/Elementor site at
https://txinsuranceappraiser.com. No database and no plugins. Content is stored as JSON
and plain PHP, and a single front controller renders every URL.

**Staging (temporary domain, same Hostinger Cloud Enterprise account `u401386392`):**
https://lightpink-woodpecker-185489.hostingersite.com — it sends `noindex` on every page and a
`Disallow: /` robots.txt, because both switch on automatically for any host other than
txinsuranceappraiser.com.

## Layout

| Path | Purpose |
| --- | --- |
| `index.php` | Front controller: canonical host/HTTPS (production only), legacy redirects, routing |
| `.htaccess` | Sends non-file requests to `index.php`, blocks `inc/ pages/ content/ data/`, caching headers |
| `inc/config.php` | Business facts (phone, email, Joseph Dittman, license), navigation, tool list |
| `inc/helpers.php` | Escaping, data loaders (cities, posts), icons |
| `inc/layout.php` | `<head>`, header and mega-menu, footer, CTA band, FAQ and lead form components |
| `inc/longform.php` | Long-form template for service and guide pages (TOC sidebar) |
| `inc/schema.php` | JSON-LD: ProfessionalService/LocalBusiness, Person, WebSite, Breadcrumb, FAQ, Service |
| `inc/regions.php` | Peril profiles for 12 Texas regions, used by the city pages |
| `inc/redirects.php` | 301s for WordPress-only URLs, feeds, Yoast sitemaps, typo URLs and old `/wp-content/uploads/` images |
| `inc/contact-handler.php` | Lead form handler: emails `info@txinsuranceappraiser.com` and keeps a backup copy in `data/leads.csv` |
| `pages/*.php` | One template per page type (home, about, service, city, post, tool, etc.) |
| `data/cities.json` | 288 cities with county, coordinates, region, nearest hub and nearby cities |
| `content/cities/batch-*.json` | Local facts per city: intro, neighborhoods, landmarks, weather, roofs, ZIPs, a local FAQ |
| `content/posts/*.json` | 76 rewritten blog posts (SEO title, meta, body HTML, FAQs, key takeaways) |
| `content/legal/*.html` | Privacy policy and terms, carried over from the old site including the SMS consent language |
| `assets/` | `css/site.css`, `js/site.js` (effects and UI), `js/tools.js` (calculators), optimized WebP images |
| `_dev/` | Local dev router, `validate.py` and the legacy URL list. **Do not deploy.** |

## URLs

Every URL the WordPress site exposed returns 200 at the same address: home, about, what-is-an-appraisal,
services (4) and areas index, 288 city pages, 76 posts, blog, contact, privacy and terms.
`/category/blog/`, feeds, the Yoast sitemaps and five typo URLs that Search Console picked up all
301 to their correct pages. Old image URLs under `/wp-content/uploads/...` 301 to the new WebP files.

New pages: `/services/umpire/` (Search Console shows a lot of "<city>, tx insurance umpire services" impressions),
`/tools/` plus 5 tools, `/sitemap.xml`, `/robots.txt` and `/thank-you/` (noindex).

## Local development

```bash
php -S 127.0.0.1:8090 _dev/router.php
```

```bash
python3 _dev/validate.py
```

The validator checks:
- every legacy URL resolves
- no PHP errors
- titles and descriptions are unique and the right length
- each page has exactly one H1
- JSON-LD parses
- canonical tags are correct
- every image has alt text
- there are no broken internal links or missing assets
- the homepage has at least 14 "TX Insurance Appraiser" mentions

Point it at another host with `BASE=https://… python3 _dev/validate.py`.

## Editing content

- **Phone, email, hours, license:** `inc/config.php`.
- **A blog post:** edit or add `content/posts/<slug>.json`. A new file appears automatically on `/blog/`,
  in the sitemap and at `/<slug>/`. Put the featured image in `assets/img/blog/` and set `"image"`.
- **A city:** add a row to `data/cities.json` and its local facts to a `content/cities/*.json` file.

## Going live (manual)

1. Back up the WordPress site in hPanel: files and database.
2. Build the archive from this folder, leaving out `_dev/` and `README.md`:
   `zip -qr site.zip . -x '_dev/*' README.md`
3. Upload it to `txinsuranceappraiser.com/public_html/` and extract it, either with hPanel's File Manager
   or the same API flow used for staging (`hosting_files_generate-upload-url`, then a TUS upload, then
   `hosting_websites_deploy-static-site-archive`). Remove the old WordPress files first; the new
   `.htaccess` replaces WordPress's own.
4. Make sure `data/` is writable, so the backup copy of form leads in `data/leads.csv` can be written.
5. Clear the LiteSpeed/CDN cache. Then submit `https://txinsuranceappraiser.com/sitemap.xml` in Search Console
   and remove the old Yoast sitemaps.
6. Send a real test lead through `/contact-us/` and confirm it arrives at info@txinsuranceappraiser.com.
   If mail() is filtered, set up SMTP or create the `no-reply@` mailbox the From header uses.

## Review before launch

- City facts (neighborhoods, ZIP codes, named storms) were researched for each city and checked automatically
  for format, not against outside sources. Spot-check the cities you care most about.
- Blog posts cite only well-established Texas law: Ins. Code ch. 541, 542 and 542A, and the Johnson,
  Barbara Technologies and Ortiz decisions. They contain no invented statistics. Dollar examples are labeled as illustrative.
- Two pairs of posts target near-identical queries:
  - `/insurance-loss-reported-meaning/` and `/what-does-insurance-loss-reported-mean/`
  - `/what-does-an-insurance-umpire-do/` and `/how-insurance-umpires-are-chosen-in-texas/`

  Both pages of each pair are kept so no URL is lost, and each pair cross-links. Consider consolidating one of each pair later.
- The old "Houston-TX.webp" image actually shows Austin, so the Houston page uses a storm-damage image instead.
- Joseph's photo is `assets/img/site/joseph-dittman-appraiser.webp` (path set in `SITE['photo']`).
- License shown site-wide: Rise Public Adjusting LLC, Texas public adjuster license #3341461 (`inc/config.php`).

## Lead capture

Every form (contact page, city pages, homepage hero and the popup) posts to `/contact-submit/` and is emailed to
`SITE['form_to']` = info@txinsuranceappraiser.com. The popup opens from the header's "Free Claim Review" button and
the mobile "Free Review" button, after 35 seconds, or on exit intent. It shows once per browser session and never on
the contact or thank-you pages.
