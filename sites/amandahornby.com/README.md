# amandahornby.com — expired-domain rebuild

A static interiors journal ("The Painted Room") built for the expired domain
amandahornby.com. Inspired by the 2017–2020 site (Home / About / Projects /
Press / Contact), redesigned with scroll and motion effects.

The previous owner is a working interior designer, so the site does not use her
name as a brand, her biography, contact details or project photographs. The
footer and About page say the domain changed hands.

## Photography

All photos are from StockSnap.io under CC0 (public domain, no attribution
required), found through the Openverse API. They live in `src/img/` as WebP at
960px and 560px wide; `IMAGES` in `build.py` holds alt text and dimensions.
StockSnap only serves 960px-wide files to non-browser clients, so hero images
use the full 960px file. The Projects page says they are inspiration images,
not client work.

## Backlinks

All 837 backlinks in the Semrush export point at the homepage (`/`,
`http://` and `www.` variants), so there are no deep URLs to restore. The
only editorial links are seven nofollow links from houseandgarden.co.uk
decorating galleries; the journal guides cover the same topics. The old URLs
`/about`, `/projects-1`, `/press`, `/contact` are kept as they were, and
`/home` 301s to `/`.

## Build and deploy

    python3 build.py      # writes ./public (stdlib only)
    php -S 127.0.0.1:8765 -t public public/index.php   # local preview
    ./deploy.sh           # see the header for the upload credentials

Hostinger Agency website UID `RozD314ms`, temporary domain
https://beige-koala-105302.hostingersite.com (sends `X-Robots-Tag: noindex`).
`index.php` serves `public/_pages/*.html` at extensionless URLs, forces https
and the bare host once the request host is amandahornby.com, and drops
the noindex header automatically on the real domain.

## Go-live

1. Link amandahornby.com to the website (`agency-hosting_domains_change-website`
   or hPanel) and point DNS at Hostinger.
2. Wait for SSL, then check `/`, `/about`, `http://www.amandahornby.com/` (should 301).
3. Make sure the info@amandahornby.com inbox exists (it is `EMAIL` in `build.py`).
4. Submit `https://amandahornby.com/sitemap.xml` in Search Console.
