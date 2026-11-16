# conversepublicadjuster.com — San Antonio Public Adjuster static site

Evergreen San Antonio rebuild of the former Converse / storm-dated site. Pure HTML (CSS inline), one
server-side form handler (`contact.php`), and a PHP front controller (`wp-content/db.php`) that the
Hostinger platform needs.

| Path | What it is |
| --- | --- |
| `home.html` | The homepage. Named `home.html`, not `index.html`, on purpose (see Hosting) |
| `about/`, `contact/`, `contact/thanks/`, `services/*/`, `service-areas/*/`, `blog/*/` | Pages, one `index.html` each |
| `404.html` | Not-found page (noindex) |
| `assets/mark.svg` | Logo / favicon carried over from the old site |
| `contact.php` | The old site's working form handler (PHP `mail()` with a FormSubmit relay fallback). Unchanged apart from the email subject line |
| `wp-content/db.php` | Front controller: serves `/` → `home.html`, `/x/` → `x/index.html`, 301s every old URL, real 404s |
| `googlecccfbf2f7e9e5ae4.html` | Google Search Console verification file, carried over |
| `sitemap.xml`, `robots.txt` | 65 indexable URLs; `home.html`, `contact.php`, `contact/thanks/` disallowed |
| `.htaccess`, `_redirects` | Same 301 map for Apache/LiteSpeed and Netlify/Cloudflare hosts. Not read by the current host |
| `_old-site/` | Raw backup of the live site as fetched before this rebuild (`server/` holds files read off the host) |
| `tools/transform.py`, `tools/fix_meta.py` | The one-off transformations applied to the generated build (idempotent) |
| `tools/seo_check.py` | Static SEO checks; run `python3 -I tools/seo_check.py` after any edit |
| `tools/router.php` | Local stand-in for the host: `php -S 127.0.0.1:8089 tools/router.php` then open http://127.0.0.1:8089/ |
| `deploy.sh` | Uploads to the Hostinger Agency website via its file-browser TUS endpoint |

## Hosting

The domain is a Hostinger Agency Plan (H5G) website, UID `h1GbQ1rks`, IP 72.60.128.114, LiteSpeed behind
Hostinger's `hws` front end. It is provisioned as a locked WordPress install: `index.php` cannot be
replaced, `.htaccess` is not processed, and if a root `index.html` exists the platform serves it for every
unknown path with a 200. So the homepage is `home.html`, and `wp-content/db.php` (a WordPress drop-in
that loads before anything else) serves the static files, issues the 301s and returns `404.html` with a
real 404. `contact.php` runs as ordinary PHP.
