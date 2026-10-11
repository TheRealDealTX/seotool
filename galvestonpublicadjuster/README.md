# galvestonpublicadjuster.com

Lead-generation site for Galveston Public Adjuster (Joseph Dittman). Plain PHP, no database, no
framework. Every page is routed through `index.php`.

Live on Hostinger Agency website **`lCCnMqaFW`** (php-fpm), preview at
https://linen-sandpiper-973090.hostingersite.com. Server path: `/home/u914589053/websites/lCCnMqaFW/public_html`.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: routes, trailing-slash and canonical-host redirects, `X-Robots-Tag: noindex` on any other host (the preview domain), 404s, `sitemap.xml`, `feed.xml` |
| `inc/config.php` | Phone, lead email, author, nav, service area, the 70 mph weather threshold, `PAGE_UPDATED` dates |
| `inc/sitemap.php` | Sitemap. `<lastmod>` comes from `PAGE_UPDATED` (static pages), the newest post (home, blog) or the last weather check — never from file mtimes, which every deploy resets |
| `inc/layout.php` | `<head>`, JSON-LD, top banner, header, footer, 5-second popup, lead form, CTA banners |
| `inc/art.php` | Inline SVG illustrations and the wind gauge |
| `inc/content.php` | Blog and weather-event data access |
| `pages/*.php` | One file per page |
| `api/lead.php` | Form handler: emails every lead to `jditt@risepublicadjusting.com` and logs it to `data/private/leads.php` (starts with `<?php exit;` so it cannot be read over the web) |
| `cron/weekly.php` | Weekly job: 70+ mph wind check, then publishes the next blog post (CLI only) |
| `data/blog-queue/*.json` | Written blog posts. They publish one per week, in filename order |
| `data/keywords.json` | High-intent keywords from the Semrush export. Used once the queue runs out |
| `data/published.json`, `data/weather-*.json` | Runtime state written by the cron. `deploy.sh` does not overwrite these unless you pass `--init` |
| `tools/check.py` | QA: status, PHP errors, one H1, keyword counts (homepage 14× "galveston public adjuster" and 4× "twia expert"; TWIA page 14× "twia expert") |

## Weekly cron

The Hostinger cron runs `17 12 * * 1`:
`/usr/bin/php /home/u914589053/websites/lCCnMqaFW/public_html/cron/weekly.php`

- **Weather:** reads NWS KGLS observations (measured, last ~7 days) and Open-Meteo daily maximums for
  Galveston Island (modeled). Any day with gusts or sustained winds of 70 mph or more is added to
  `/weather-events/`. `php cron/weekly.php --weather-only --backfill=2024-01-01` backfills from the
  archive; the initial backfill found Beryl (2024-07-08).
- **Blog:** publishes the next queued post, at most once every 6 days. There are 16 posts: 3 went
  live at launch and 13 are queued, which covers about three months. After that, the cron writes a
  new post with the Claude API from `data/keywords.json`, but only if a key is present. To enable
  it, create `data/private/config.php` containing
  `<?php return ['anthropic_api_key' => 'sk-ant-…'];`. Upload it by hand; it is never committed or
  deployed. Without a key the cron does nothing once the queue is empty. You can also keep adding
  JSON posts to `data/blog-queue/` and redeploy.

## Search Console: "Discovered - currently not indexed"

Google first reported this on 10/3/26 for 13 of the 16 sitemap URLs, all with *Last crawled: N/A*. The pages
are fine (200, fast, self-canonical, no `noindex`, linked from the nav and footer of every page): Google found
them in the sitemap but has not scheduled a crawl yet, which is normal for a domain launched on 9/28/26 with
no backlinks. What is in the code is done; what remains is in Search Console and off-site:

1. **URL inspection → Request indexing** for each of the 13 URLs (one at a time, about 10 per day are
   accepted). This is the only direct way to pull a never-crawled URL forward.
2. **Sitemaps → add `https://galvestonpublicadjuster.com/feed.xml`** next to `sitemap.xml`. Google accepts
   RSS as a sitemap and polls it more often for new posts. Every page also now advertises the feed with
   `<link rel="alternate" type="application/rss+xml">`.
3. **Link to the site from txpublicadjusting.com** (footer or a "Galveston" service-area page) and from the
   Google Business Profile. The sister site is the one established domain that can pass crawl priority here;
   today it does not link to galvestonpublicadjuster.com at all.
4. **Keep lastmod honest.** When you materially edit a page, bump its date in `PAGE_UPDATED`
   (`inc/config.php`). Blog posts and the weather page move on their own. Dates that jump on every deploy
   teach Google to ignore the sitemap's lastmod entirely.
5. **www certificate.** `https://www.galvestonpublicadjuster.com` fails the TLS handshake: the platform
   certificate was issued on 9/27 before the `www` DNS record existed and does not cover it. Hostinger
   does not let `www` be linked separately (`agency-hosting_domains_link-to-website` rejects it), so
   re-issue the apex certificate (`agency-hosting_ssl_reinstall-website`, or hPanel → SSL → Reinstall) now
   that `www` resolves; expect a few minutes without a valid certificate while it re-issues.

Validation in Search Console takes one to three weeks after the request. If URLs move from "Discovered" to
"Crawled - currently not indexed", the cause is content/quality, not crawling, and the fix is more links
and more substantive pages, not anything technical.

## Deploying

```sh
# credentials from agency-hosting_generateUploadURLV1 (expire after a few hours)
export GPA_FB_URL=… GPA_FB_AUTH=… GPA_FB_REST=…
python3 tools/check.py            # against a local `php -S 127.0.0.1:8099 index.php` (pages, keywords, sitemap lastmod)
./deploy.sh                       # never --init after launch
```
Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`).

## Open items

- **DNS:** the domain is not in this Hostinger account's domain list and its Hostinger DNS zone is
  empty. Point `galvestonpublicadjuster.com` at the site (A record `72.60.128.114`, or the Hostinger
  nameservers shown in hPanel). The Let's Encrypt certificate finishes once DNS resolves.
- **Firm details** (legal name, TDI license #3356839, Belton address, office hours, headshot) come from
  txpublicadjusting.com and live in `inc/config.php`. They appear in the footer on every page, the popup,
  the About and Contact pages and the JSON-LD, which meets TDI Bulletin B-0006-26's address and license rule.
- **Content review:** manufacturer wind ratings, statute references and storm data were researched
  in September 2026 and cite their sources. Review them, especially the rows marked "verify".
