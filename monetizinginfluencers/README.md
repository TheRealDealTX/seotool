# monetizinginfluencers.com: custom PHP rebuild

A hand-built PHP/HTML site that replaced the 2023 WordPress + Elementor install on
**2026-10-25**. No WordPress, no database, no plugins. Pages are plain PHP files that
share one layout, one stylesheet and one script.

- **Hosting:** Hostinger web hosting (JWeb, Cloud Enterprise order 64270646), user `u401386392`,
  document root `/home/u401386392/domains/monetizinginfluencers.com/public_html`
- **Search Console:** verified by `google9d8d740410b54935.html` (kept in the web root)
- **Contact email used by forms:** info@monetizinginfluencers.com
- **Google Analytics:** not set up. Put the GA4 ID in `GA_ID` in `public/inc/layout.php`.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | The web root. Everything in here is uploaded to `public_html/`. |
| `public/inc/config.php` | Site name, contact details, navigation, blog post list (`site_posts()`) |
| `public/inc/layout.php` | `page_start()`, `page_end()`, `page_hero()`, `faq_block()`, `cta_band()`, `post_cards()`, SEO tags and JSON-LD |
| `public/inc/icons.php` | Inline SVG icon set: `icon('rocket')` |
| `public/assets/css/site.css` | Design system: dark creator theme, glass cards, gradients, animations |
| `public/assets/css/{platforms,pages,blog,tools}.css` | Page-group styles |
| `public/assets/js/site.js` | Nav, scroll progress, reveal-on-scroll, card tilt, cursor glow, hero network canvas, typewriter, counters, confetti, copy buttons, AJAX forms |
| `public/assets/js/tools/*.js` | One script per interactive tool |
| `public/api/form.php` | Handles every form; emails info@ and appends to `../mi-form-submissions.log` (outside the web root) |
| `public/.htaccess` | https/non-www redirects, old WordPress URL redirects, blocks WordPress entry points |
| `public/_wp-backup/` | Copies of the WordPress `.htaccess` and `index.php` (web access denied) |
| `backup/wordpress-2026-10-25/` | Same copies plus rollback steps |
| `validate.py` | Crawls a local preview, checks every page, writes `public/sitemap.xml` |
| `deploy.sh` | Uploads `public/` through Hostinger's File Browser API |
| `dev-router.php` | Router for local preview with `php -S` |

## Work on it

```sh
php -S 127.0.0.1:8080 -t public dev-router.php   # preview at http://127.0.0.1:8080
python3 validate.py                              # check everything + regenerate sitemap.xml
./deploy.sh                                      # see the header comment for credentials
```

To add a blog post: copy any post folder (e.g. `public/how-to-get-brand-deals/`), edit it,
add a row to `site_posts()` in `public/inc/config.php` (that feeds `/blogs/`, the homepage,
related posts and the RSS feed), then run `validate.py` so the sitemap picks it up.

## SEO plan (from the Search Console export, Jun 2025 - Oct 2026)

The old site had 676 impressions and 22 clicks in 16 months; 21 of the clicks went to
`/write-for-us/`. Every URL that had impressions was kept and rewritten around the queries
it was already showing for:

| URL | Target queries |
| --- | --- |
| `/` | monetizing influencers, influencer monetization |
| `/write-for-us/` | influencer marketing write for us, creator economy write for us, affiliate marketing write for us, influencer marketing article submission |
| `/social-platforms/pinterest/` | pinterest influencer marketing, influencer marketing on pinterest, pinterest influencers, pinterest influencer marketing platform |
| `/monetization/` | influencer monetization, monetization for influencers, monetize influencers |
| `/website-design/` | web design for influencers (was already position ~13) |
| `/social-platforms/facebook/` | facebook influencer marketing, facebook influencers, how to contact facebook influencers |
| `/social-platforms/{youtube,tiktok,instagram}/` | platform monetization |
| `/how-to-write-to-an-influencer/` (new) | how to write to an influencer, how to write to influencers |

New supporting content: six more blog guides, six interactive tools under `/tools/`,
About, Contact, Terms and an HTML sitemap. Every page has a unique title and description,
one H1, canonical, Open Graph/Twitter tags and JSON-LD (Organization, WebSite, WebPage,
BreadcrumbList, FAQPage, BlogPosting, WebApplication where relevant).

## Hosting notes

- LiteSpeed honours `.htaccess`. Directory URLs (`/monetization/`) are real folders with an `index.php`.
- The WordPress files and database are still on the server, unreachable. See
  `backup/wordpress-2026-10-25/README.md` to roll back, or delete them once the new site has settled.
- Old image URLs under `/wp-content/uploads/` still resolve.
- Money figures on the site (rates, RPMs, calculator outputs) are labelled estimates.
