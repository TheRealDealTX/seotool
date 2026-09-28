# galvestonpublicadjuster.com

Lead-generation site for Galveston Public Adjuster (Joseph Dittman). Plain PHP, no database, no
framework. Every page is routed through `index.php`.

Live on Hostinger Agency website **`lCCnMqaFW`** (php-fpm), preview at
https://linen-sandpiper-973090.hostingersite.com. Server path: `/home/u914589053/websites/lCCnMqaFW/public_html`.

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: routes, trailing-slash and canonical-host redirects, 404s, `sitemap.xml`, `feed.xml` |
| `inc/config.php` | Phone, lead email, author, nav, service area, the 70 mph weather threshold |
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

## Deploying

```sh
# credentials from agency-hosting_generateUploadURLV1 (expire after a few hours)
export GPA_FB_URL=… GPA_FB_AUTH=… GPA_FB_REST=…
python3 tools/check.py            # against a local `php -S 127.0.0.1:8099 index.php`
./deploy.sh                       # never --init after launch
```
Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`).

## Open items

- **DNS:** the domain is not in this Hostinger account's domain list and its Hostinger DNS zone is
  empty. Point `galvestonpublicadjuster.com` at the site (A record `72.60.128.114`, or the Hostinger
  nameservers shown in hPanel). The Let's Encrypt certificate finishes once DNS resolves.
- **TDI advertising rule (Bulletin B-0006-26, July 2026):** public adjuster ads must show the
  business address and license number. Add both to `inc/config.php` and the footer.
- **Content review:** manufacturer wind ratings, statute references and storm data were researched
  in September 2026 and cite their sources. Review them, especially the rows marked "verify".
