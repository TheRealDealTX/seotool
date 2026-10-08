# pensacolahurricane.com — Pensacola Hurricane

Static hurricane-information site for Pensacola, FL, with a few small PHP
endpoints for live data. Built for The Lawgical Firm; the firm is referenced
lightly (claims, recovery, tools and homepage "claims" boxes) via `FIRM` in `build.py`.

**Hosting:** Hostinger Agency website UID `JWAYmkIOa` (php-fpm, Phoenix),
temporary address **https://violet-squid-690755.hostingersite.com**.
Created 2026-10-08. The real domain is not connected yet.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies; first line is a JSON header (path, title, description, nav, group) |
| `src/static/` | Copied verbatim: CSS, JS, favicon, OG image, `index.php` front controller, `api/` |
| `src/static/api/storms.php` | NHC `CurrentStorms.json` proxy (5-min cache) |
| `src/static/api/nhc-feed.php` | NHC Atlantic RSS → JSON (10-min cache) |
| `src/static/api/zone.php` | Address → Census geocoder → Escambia / Santa Rosa evacuation-zone GIS + nearest Escambia shelter sites |
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
