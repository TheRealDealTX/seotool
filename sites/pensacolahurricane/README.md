# pensacolahurricane.com — Pensacola Hurricane

Attorney lead-generation site for The Lawgical Firm, P.A. (Florida property
insurance claims): denied, underpaid and delayed hurricane claims in Pensacola,
Escambia and Santa Rosa counties, backed by a free hurricane information center
(live tracker, weather, evacuation zones, tools). Firm details live in `FIRM`
in `build.py`; the header phone/CTA, footer attorney-advertising disclosures,
CTA band and lead form all render from it.

**Hosting:** Hostinger Agency website UID `JWAYmkIOa` (php-fpm, Phoenix),
Created 2026-10-08 on the temporary address violet-squid-690755.hostingersite.com.
On 2026-10-10 the website's domain was changed (outside this repo) to
**destinhurricane.com**, with preview address
**https://darkorchid-turtle-604356.hostingersite.com**; the old temporary address
no longer serves. pensacolahurricane.com is not connected yet.

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
| `deploy.sh` | Uploads `public/` via the Hostinger File Browser TUS API (see header for credentials) |

NWS data (alerts, forecast, KPNS observations, gridded wind/rain, HLS/AFD
products) is fetched in the browser from api.weather.gov, which allows CORS.

## Build & deploy

```sh
python3 build.py && python3 validate.py && ./deploy.sh
```

## Going live on pensacolahurricane.com

1. Point the domain at the website (Hostinger `agency-hosting_domains_change-website`
   from `violet-squid-690755.hostingersite.com` to `pensacolahurricane.com`, or hPanel).
2. Set `STAGING = False` in `build.py` (removes the site-wide `noindex` and the
   `Disallow: /` in robots.txt), rebuild and redeploy.
3. Submit `https://pensacolahurricane.com/sitemap.xml` in Search Console.

Canonical URLs already point at `https://pensacolahurricane.com`.

## Time-sensitive content

`src/pages/12-news-isaias.html` and the "Present day" paragraph in
`06-history.html` describe Hurricane Isaias as of NHC Advisory 8 (Oct 8, 2026).
Update them with final impacts after the NHC post-storm report.

## Lead forms

`{{LEAD_FORM}}` (full) and `{{LEAD_FORM_COMPACT}}` in any page body render the
case review form (`lead_form()` in `build.py`). Pages can set `"cta": false` in
their header to drop the footer CTA band (used on /free-case-review/).

## Attorney advertising

The site is a Florida lawyer advertisement. Footer and /disclaimer/ carry the
firm name, office city, no-attorney-client-relationship, past-results and fee
disclosures. Avoid unverifiable quality claims ("best", "top-rated", "expert",
"specialist") and testimonials or results without the firm's sign-off.
