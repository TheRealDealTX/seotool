# fraserandmorris.com — expired-domain rebuild

Static rebuild of the expired garden-design domain fraserandmorris.com, styled as a
modern plant-led garden design studio. HTML, one CSS file, one JS file and local
WebP images, with a small PHP front controller and a contact form handler.

**Temporary URL:** https://darkgoldenrod-lyrebird-960547.hostingersite.com
(Hostinger Agency Growth plan, website UID `haI1jJ1FP`, UK datacenter, PHP 8.3).

## Rebuilt URLs

Every URL from the old site that ranked (Semrush organic positions, July 2017) or
carries backlinks is rebuilt at its **exact old path**:

| URL | Topic / target keyword | Why |
| --- | --- | --- |
| `/` | garden design london, fraser morris | 974 backlinks, brand rankings |
| `/about.html` | studio / approach | Backlink (The Guardian) |
| `/contact.html` | contact | Ranked (camberwell grove london) |
| `/services.html` | garden design services | Archived page |
| `/gardens.html` | garden types overview | Ranked (fraser and fraser london) |
| `/gardens/courtyard.html` | courtyard garden design | Ranked |
| `/gardens/courtyard/courtyard2.jpg` | image | 2 backlinks, now a real courtyard photo |
| `/gardens/belsize.html` | town garden design | Ranked #22–26 |
| `/gardens/highgate.html` | family garden design | Ranked |
| `/gardens/family.html` | garden design oxfordshire | Ranked |
| `/gardens/country.html` | architectural planting | Ranked |
| `/gardens/fox.html` | internal / lush garden design, garden designers south london | Ranked |
| `/gardens/artists.html` | atmospheric (artist's garden) planting | Ranked |
| `/gardens/study.html` | study garden design | Ranked |
| `/gardens/print.html` | house garden design | Ranked |

`index.php` 301s `/index.html`, `/gardens/` and similar old paths. Note: the host
serves static file extensions (`.pdf`, `.jpg`) itself and never passes them to
PHP, so `/pdfs/GardensIllustrated.pdf` (old ranking, no traffic, no backlinks)
returns 404.

Content is written fresh. It does not name or claim to be the original
partners, and does not present their past client projects as this site's work.
The garden pages describe how each type of garden is designed.

## Files

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, page templates, schema (`python3 build.py`) |
| `content.py` | Copy for the nine garden pages and the homepage FAQ |
| `validate.py` | Post-build checks: one H1, unique titles and descriptions, JSON-LD, alt text, broken links, legacy URLs |
| `assets/css/site.css`, `assets/js/site.js` | Styles and behavior (mobile nav, reveals, parallax, petals, seasons tabs) |
| `assets/img/*.webp` | Royalty-free photos (Pexels license), resized and converted |
| `index.php` | Serves `home.html` at `/`, legacy 301s, real 404s, `noindex` header on non-production hosts |
| `contact.php` | Form handler; emails enquiries to info@fraserandmorris.com |
| `deploy.sh` | Uploads the build through the Hostinger File Browser TUS API |

## Build & deploy

```sh
python3 build.py && python3 validate.py
export FM_FB_URL=... FM_FB_AUTH=... FM_FB_REST=...   # from agency-hosting_files_generate-upload-url
./deploy.sh
```

## Going live on fraserandmorris.com

1. Attach the domain to website `haI1jJ1FP` (`agency-hosting_domains_change-website`
   or hPanel) and point DNS at Hostinger.
2. Canonicals, Open Graph URLs and the sitemap already use `https://fraserandmorris.com`.
   The `X-Robots-Tag: noindex` header stops automatically once the site is served
   on fraserandmorris.com, and `index.php` 301s `www.` to the bare domain.
3. Create the `info@fraserandmorris.com` mailbox so form enquiries are delivered,
   and send a test enquiry.
4. Submit `sitemap.xml` in Google Search Console.
