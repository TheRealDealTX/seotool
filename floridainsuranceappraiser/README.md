# floridainsuranceappraiser.com — static site

Brand: **Florida Insurance Appraiser** · +1 (844) 537-1427 · info@floridainsuranceappraiser.com
Hosting: Hostinger Agency Growth, website UID `BHoKZ0Ik1` (plain php-fpm, Boston datacenter).
Temporary domain: https://pink-tiger-234102.hostingersite.com

```sh
python3 build.py      # renders everything into dist/
python3 validate.py   # links, assets, one H1, unique titles/descriptions, JSON-LD, homepage keyword count (>=14)
./deploy.sh           # uploads dist/ (see header comment for credentials)
```

## Layout
| Path | What |
| --- | --- |
| `build.py` | Layout, homepage, all page templates, schema, sitemap, `index.php`, `api/contact.php` |
| `siteconfig.py` | Name, phone, email, origin |
| `content/` | Copy: `services.py` (10), `locations.py` (12 cities), `tools.py` (7 tools), `blog.py` (5), `resources.py` (about, process, FAQ, glossary, legal) |
| `assets/` | `site.css`, `site.js` (nav, home gap estimator, form), `tools.js` (all calculators), images |

49 HTML pages: home, about, contact, appraisal process, FAQ, glossary, 10 services + index,
12 Florida locations + index, 7 tools + index, 5 guides + index, privacy/terms/disclaimer, HTML sitemap, 404.

Hosting note (same platform behaviour as huttoroofs.com): the homepage is `home.html`, served by
`index.php`, which also returns real 404s. Don't add an `index.html` at the root.

## Going live on the real domain
1. Link `floridainsuranceappraiser.com` to website `BHoKZ0Ik1` (hPanel or `agency-hosting_domains_change-website`) and point DNS.
2. Canonicals, sitemap and schema already use `https://floridainsuranceappraiser.com`; `index.php` 301s `www.` and plain http to it.
3. Create the mailbox `info@floridainsuranceappraiser.com`. The form (`/api/contact.php`) emails it with PHP `mail()` and
   also appends each lead to `leads.log` one level above `public_html`, so nothing is lost before the mailbox exists.
4. Submit `sitemap.xml` in Search Console.
