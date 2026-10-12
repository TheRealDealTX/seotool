# rjbledlcdtvservicecentre.com — expired-domain rebuild

Static rebuild of RJB LED LCD TV Service Centre (Kolkata TV repair). Python
standard library only; HTML, one CSS file, one JS file, local WebP images.

```sh
STAGING=1 python3 build.py   # temporary domain: noindex + robots Disallow
python3 build.py             # production, once the real domain is pointed
python3 validate.py          # one H1, unique titles, JSON-LD, links, alt text
./deploy.sh                  # needs FB_URL / FB_AUTH / FB_REST (see header)
```

Then clear the cache (`agency-hosting_cache_clear-website`).

## Hosting

Hostinger Agency Growth plan, website UID `DZbtKzYiX` (plain php-fpm, Mumbai
datacenter), temporary domain **https://coral-ostrich-175008.hostingersite.com**.
The host ignores `.htaccess` and routes `/` and unknown paths to `index.php`, so
there is no root `index.html`: `index.php` serves `home.html`, 301s legacy URLs,
adds trailing slashes and returns `404.html` with a real 404.

**Going live:** link `rjbledlcdtvservicecentre.com` to the website, rebuild
*without* `STAGING=1`, redeploy. `index.php` then also 301s `www.` and `http://`
to `https://rjbledlcdtvservicecentre.com`. Canonicals already point there.

## URL inventory (from the Semrush positions + backlinks exports)

Kept at their original slugs:

| URL | Why |
| --- | --- |
| `/` | 6,344 of 6,406 backlinks; ranking |
| `/samsung-led-lcd-tv-service-centre-kolkata/` | top traffic page; 12 backlinks |
| `/videocon-led-lcd-tv-service-centre-kolkata/` | traffic (incl. "led or lcd" queries); 6 backlinks |
| `/sony-led-lcd-tv-service-centre-kolkata/` | traffic; 12 backlinks |
| `/led-lcd-tv-repairing-in-kolkata/` | traffic; 16 backlinks |
| `/lg-led-lcd-tv-service-centre-kolkata/` | 39 keywords; 15 backlinks |
| `/led-tv-service-center-in-ruby/` | backlink |
| 10 area posts (Bally, Howrah, Chandannagar, Uttarpara, Baidyabati, Phoolbagan, Ghoshpara, Akra, Bamangachi, Santoshpur) | ranking keywords |

Ranking WordPress tag archives became real area pages at the post-style slug
(Bhadreshwar, Naihati, Barrackpore, Kankurgachi, Palta, Budge Budge, Gangpur)
and `/tag/<slug>` 301s to them; the four `/tag/…-in-kolkata` tags 301 to the
brand pages, other `/tag/*` to `/service-areas/`, `/author/admin/` to `/about/`.
New pages: `/service-areas/`, `/led-vs-lcd-tv/` (targets "which is better led
or lcd tv"), `/about/`, `/contact/`, `/privacy-policy/`.

## Notes

- web.archive.org is blocked from the build environment, so structure and copy
  were rebuilt from the URL/keyword/anchor data, not the archived HTML.
- Only an email address is published (no phone/street address was supplied).
- The contact form posts to `send.php` (PHP `mail()` to info@…). It will only
  deliver once the domain has a working mailbox/MX.
- Photos are Unsplash-licensed (free, no attribution required), self-hosted
  in `public/assets/img/`.
- Pages carry an "independent, not an authorised brand service centre" notice.
