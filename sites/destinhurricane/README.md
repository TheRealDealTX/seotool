# destinhurricane.com — Destin Hurricane

Attorney lead-generation site for The Lawgical Firm, P.A. (Florida property
insurance claims) built around a free hurricane information desk for Destin,
Okaloosa County and Walton County: live NHC tracker, NWS weather and alerts,
evacuation-zone lookup, shelters, surge, preparedness, history, news, tools,
alert sign-ups, recovery, community guides and claim pages (denied, underpaid,
delayed, Hurricane Isaias). Firm details live in `FIRM` in `build.py`; the
header, footer attorney-advertising disclosure, claim card and lead forms all
render from it.

pensacolahurricane.com is a **separate site** in `../pensacolahurricane`
(Escambia/Santa Rosa). This site was cloned from it and then rebuilt with its
own design, copy, slugs and keyword targets; do not copy changes between them.

## Keyword targets

| Page | Primary keyword |
| --- | --- |
| `/` | Destin hurricane (title front, H1, first paragraph, H2, meta; checked by `validate.py`, ≥14 visible uses, case-insensitive) |
| `/destin-hurricane-claim-lawyer/` | Destin hurricane claim lawyer |
| `/denied-hurricane-claim-destin/` | denied hurricane claim Destin |
| `/underpaid-hurricane-claim-destin/` | underpaid hurricane claim Destin FL |
| `/delayed-hurricane-claim-destin/` | delayed hurricane claim Destin |
| `/hurricane-isaias-claims-destin/` | Hurricane Isaias claims Destin |
| `/destin-hurricane-tracker/` | Destin hurricane tracker |
| `/destin-weather/` | Destin weather / radar |
| `/okaloosa-walton-evacuation-zones/` | Okaloosa County evacuation zones |
| `/walton-okaloosa-hurricane-shelters/` | Walton County hurricane shelters |
| `/destin-storm-surge/` | Destin storm surge |
| `/hurricane-preparedness/` | Destin hurricane preparedness checklist |
| `/hurricane-tools/` | hurricane deductible calculator Florida |
| `/destin-hurricane-history/` | Destin hurricane history |
| `/storm-alerts/`, `/after-the-storm/`, `/news/…`, `/communities/…` | supporting pages |

## Design

Emerald-coast palette (emerald `#0d6e63`, sand `#fbf7ef`, foam `#e4f4f0`, coral
CTA `#c2410c`, sun accent `#f4b942`); the firm block keeps the Lawgical navy
`#01017c` and gold `#c58911`. Fonts: Fraunces (headings) + Figtree (text).
White sticky header with inline nav and a dark-emerald live NWS strip under it;
slide-down mobile panel; floating call/review dock on phones; sand page heads
with a striped edge; numbered-row and timeline components; wave footer.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | One file per page. First line is a JSON comment: `path`, `title`, `description`, `nav`, `group`, and optionally `h1`/`kicker`/`lede`/`crumb`/`crumbs` (rendered page head + breadcrumb + BreadcrumbList), `head_form` (claim form beside the head), `reviewed` ("Last reviewed: October 2026"), `article` + `published` (Article schema), `faq` (list of `[q, a]`, rendered at `{{FAQ}}` with FAQPage schema), `cta: false`, `sitemap: false` |
| `src/static/` | Copied verbatim: CSS, JS, icons, OG image, `index.php` front controller, `api/` |
| `src/static/api/storms.php` | NHC `CurrentStorms.json` proxy (5-min cache) |
| `src/static/api/nhc-feed.php` | NHC Atlantic RSS → JSON (10-min cache) |
| `src/static/api/zone.php` | Address → Census geocoder → Okaloosa County zone layer (`services7.arcgis.com/lOFQguHNarTIBTRU/.../Emergency_Layers/FeatureServer/0`, the layer behind the county's official zone search) or Walton County's published `EvacuationZones` layer (`services1.arcgis.com/TaXHPwWfIMuzJ7Ov`, 2010 regional study; response tells users to confirm). Also nearest Okaloosa shelters with their GIS status (`FeatureServer/109`), and `?shelters=1` for the live list. Some Okaloosa polygons carry conflicting letters in `EVAC_ZONE` vs `EvacDesc`; the API returns the more cautious letter and a `conflict` flag |
| `src/static/api/lead.php` | Claim review form. Appends to `public_html/data/leads.php` (404s on the web) and, if `public_html/data/lead-config.php` exists on the server, emails it: `<?php if (!defined('DH_LEAD')) { http_response_code(404); exit; } return ['to' => ['intake@…'], 'from' => 'leads@destinhurricane.com'];` (never commit that file) |
| `src/static/api/subscribe.php` | Alert sign-ups → `../dh-private/subscribers.csv` above the web root if writable, else `public_html/data/subscribers.php` |
| `build.py` | Wraps pages in the layout → `public/` (+ `sitemap.xml`, `robots.txt`) |
| `validate.py` | Keyword placement/count on the homepage, one H1, unique titles/descriptions, canonicals, internal links/anchors, no `href="#"` |
| `deploy.sh` | Uploads `public/` via the Hostinger Agency File Browser TUS API (see its header) |

Browser-side NWS data (api.weather.gov, CORS): alerts for Destin (NWS Mobile)
and Miramar Beach (NWS Tallahassee), KDTS observations, the Destin grid
forecast/gusts/rain, and HLS products from MOB and TAE.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ./deploy.sh
```

**Hosting:** Hostinger Agency website UID `JWAYmkIOa` (php-fpm). No `.htaccess`
is needed: the host serves real files, and `index.php` handles `/`, adds
trailing slashes, returns real 404s and 301-redirects `http://` (via
`X-Forwarded-Proto`) and `www.` to `https://destinhurricane.com`. DNS is at
GoDaddy (`A @ → 72.60.128.114`, `CNAME www → destinhurricane.com`); Hostinger
issues the Let's Encrypt certificates.

## Time-sensitive content

Isaias pages (`14-isaias-claims.html`, `31-news-isaias.html`, home band,
history) reflect NHC products through Advisory 15 and local reports to
Oct. 15, 2026. Update with the NHC Tropical Cyclone Report and any FEMA
major-disaster declaration for Okaloosa/Walton.

## Attorney advertising

Footer, `/disclaimer/` and forms carry the Florida Bar disclosures (firm name,
Orlando principal office, Destin office, no attorney-client relationship,
fees, past results). Avoid "best", "expert", "specialist", guarantees,
testimonials and case results.
