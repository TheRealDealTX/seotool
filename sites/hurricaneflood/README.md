# hurricaneflood.com: HurricaneFlood.com

Attorney lead-generation and information site for The Lawgical Firm, P.A.
(Florida property insurance claims). Topic: hurricane flood damage in Florida.
It covers storm surge vs rain flooding vs wind-driven rain, which policy pays
(homeowners windstorm vs NFIP/private flood), the wind-vs-water dispute and
anti-concurrent causation, documenting water lines, hurricane deductibles
(s. 627.701), deadlines for both policy types, and legal help when an insurer
blames flood to deny wind damage.

The firm's site (checked 2026-10-15) lists hurricane/windstorm, water damage,
roof, mold, plumbing and commercial property claims. It does **not** list
NFIP or flood-policy claims, so the site claims representation only for the
homeowners/commercial (wind) side and says so wherever flood policies come up.
Fee wording follows the firm's site: free case review, no upfront fees, no
attorney fee unless there is a recovery. Phone: (407) 433-4131.

## Keyword targets (one primary per page)

| Path | Primary keyword |
| --- | --- |
| `/` | hurricane flood (plus "hurricane flood damage", "hurricane flood insurance claim") |
| `/storm-surge-damage-claim/` | storm surge damage insurance claim (storm surge damage claim Florida) |
| `/wind-vs-flood-damage/` | wind vs flood damage |
| `/wind-driven-rain-claim/` | wind-driven rain claim |
| `/hurricane-flood-insurance-claim-florida/` | hurricane flood insurance claim Florida |
| `/hurricane-deductible-florida/` | hurricane deductible Florida |
| `/documenting-hurricane-flood-damage/` | documenting hurricane flood damage |
| `/hurricane-claim-deadlines-florida/` | hurricane claim deadlines Florida |
| `/claim-denied-as-flood/` | hurricane claim denied as flood |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `/404.html` | support pages |

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies. Line 1 is a JSON comment: path, title, description, kind (`home`/`guide`/`page`/`error`), crumb, group, cta |
| `src/static/` | Copied as-is: `assets/css/storm.css`, `assets/js/storm.js`, firm logos, `favicon.svg`, `index.php`, `.htaccess`, `api/` |
| `src/static/index.php` | Front controller: serves `home.html` for `/`, sends www/http to `https://hurricaneflood.com`, adds a trailing slash to directory URLs, and returns a real 404 with `404.html` |
| `src/static/api/lead.php` | Free case review form endpoint. Appends to `public_html/data/leads.php` (first line exits, so it 404s on the web). If `public_html/data/lead-config.php` exists on the server it also emails each lead. That file is never committed and starts with `<?php if (!defined('HF_LEAD')) { http_response_code(404); exit; }`, then `return ['to' => ['intake@...'], 'from' => 'leads@hurricaneflood.com'];` |
| `build.py` | Stdlib builder. Wraps pages in the shared shell, expands `{{SHORTCODES}}` (`{{LEAD_FORM}}`, `{{RELATED}}`, `{{REVIEWED}}`, `{{SITEMAP}}`, firm fields), builds JSON-LD (WebSite, LegalService with both offices, WebPage, BreadcrumbList, plus Article on guides and FAQPage taken from each page's `<details class="qa">` blocks), and writes `public/`, `sitemap.xml` and `robots.txt`. `STAGING = False` |
| `validate.py` | Checks one H1 per page; unique title and meta description; canonical URLs; internal links and anchors; no `href="#"`; JSON-LD types; footer disclosures; Florida Bar-sensitive words; guide length (900 to 2000 words) and the "Last reviewed" line; homepage "hurricane flood" use (6 to 10 visible; also in title, H1, first paragraph, an H2 and the meta description); sitemap coverage |

Design: charcoal and navy bands (`#0b121a`, `#0d1b2e`) with electric cyan
(`#19d3f0`, `#066e82` on light) and storm-warning red (`#d42a25`). Barlow
Condensed headings, Source Sans 3 body. Full-width banded sections and a
hazard-red warning bar. The home page has a vanilla-JS "Wind or water?"
10-question checklist with an evidence meter (and a sticky mini meter on
mobile). The deductible guide has an s. 627.701(5) calculator. There is a
sticky call/review bar on mobile.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh hurricaneflood
```

`deploy-cloud.sh` needs `FB_URL`, `FB_AUTH` and `FB_REST` from Hostinger's
`hosting_files_generate-upload-url` (domain hurricaneflood.com). See the
script's header.
