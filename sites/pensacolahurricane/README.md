# pensacolahurricane.com — Pensacola Hurricane

Attorney lead-generation site for The Lawgical Firm, P.A. (Florida property
insurance claims): denied, underpaid and delayed hurricane claims in Pensacola,
Escambia and Santa Rosa counties, backed by a free hurricane information center
(live tracker, weather, evacuation zones, tools). Firm details live in `FIRM`
in `build.py`; the header phone/CTA, footer attorney-advertising disclosures,
CTA band and lead form all render from it.

**Hosting:** live on **https://pensacolahurricane.com** (2026-10-15), an addon
website on the Hostinger Cloud Enterprise plan (order 64270646, account
u401386392, server 193.203.178.215). DNS stays at GoDaddy: `A @ → 193.203.178.215`,
`CNAME www → @`. Hostinger lifetime SSL covers the apex and www; `.htaccess`
sends www and http:// to https://pensacolahurricane.com and routes unknown URLs
to `index.php`. Deploy with `../deploy-cloud.sh pensacolahurricane` (credentials
from `hosting_files_generate-upload-url`, domain pensacolahurricane.com).

This site used to be served on destinhurricane.com (Agency website UID
`JWAYmkIOa`); that domain now gets its own Destin site in `../destinhurricane/`.

Brand: The Lawgical Firm's navy (#00007C/#01017C) and gold (#C58911/#E09900),
Outfit for headings (closest free match to the firm's Euclid Circular), and the
firm's logos in `src/static/assets/img/` (copied from thelawgicalfirm.com).

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies; first line is a JSON header (path, title, description, nav, group) |
| `src/static/` | Copied verbatim: CSS, JS, favicon, OG image, `index.php` front controller, `api/` |
| `src/static/api/storms.php` | NHC `CurrentStorms.json` proxy (5-min cache) |
| `src/static/api/nhc-feed.php` | NHC Atlantic RSS → JSON (10-min cache) |
| `src/static/api/zone.php` | Address → Census geocoder → Escambia / Santa Rosa evacuation-zone GIS + nearest Escambia shelter sites |
| `src/static/api/lead.php` | Free case review form. Appends every lead to `public_html/data/leads.php` (404s on the web; download from hPanel File Manager) and, if `public_html/data/lead-config.php` exists on the server, emails it: `<?php return ['to' => ['intake@…'], 'from' => 'leads@pensacolahurricane.com'];` (never commit that file) |
| `src/static/api/subscribe.php` | Alert sign-ups. Stored in `public_html/data/subscribers.php` (first line exits, so it 404s on the web) because the home dir above `public_html` is not writable on this plan |
| `build.py` | Wraps pages in the shared layout → `public/` (+ sitemap.xml, robots.txt) |
| `validate.py` | Checks homepage uses "Pensacola Hurricane" ≥ 14 times, internal links/anchors, one H1, meta tags |
| `../deploy-cloud.sh` | Uploads `public/` via the Hostinger File Browser TUS API (see its header for credentials) |

NWS data (alerts, forecast, KPNS observations, gridded wind/rain, HLS/AFD
products) is fetched in the browser from api.weather.gov, which allows CORS.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ./deploy.sh
```
