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

## Photos

All photographs are free stock images from [Pexels](https://www.pexels.com/license/) (free for commercial use,
no attribution required; credited here for the record). Each is stored in `assets/img/photos/` as a
1600px WebP plus a 720px `-sm` version for `srcset`. Photo-to-page assignments and alt text live at the top of
`build.py` (`PHOTO_ALT`, `SVC_PHOTO`, `LOC_PHOTO`, `POST_PHOTO`). The Tallahassee page uses a generic North
Florida live-oak street photo (St. Augustine), and its alt text does not claim it is Tallahassee.

| File | Source |
| --- | --- |
| `florida-home-palm-trees` | https://www.pexels.com/photo/5177211/ |
| `hurricane-palm-trees-wind` | https://www.pexels.com/photo/16313103/ |
| `hurricane-damage-aerial` | https://www.pexels.com/photo/4170441/ |
| `roofer-shingle-roof-repair` | https://www.pexels.com/photo/9431615/ |
| `water-damage-collapsed-ceiling` | https://www.pexels.com/photo/30499666/ |
| `cracked-wall-foundation` | https://www.pexels.com/photo/7717787/ |
| `fire-damaged-house` | https://www.pexels.com/photo/12180092/ |
| `florida-condo-building` | https://www.pexels.com/photo/31642742/ |
| `florida-commercial-property` | https://www.pexels.com/photo/30648770/ |
| `insurance-documents-review` | https://www.pexels.com/photo/7731335/ |
| `estimate-review-clipboard-laptop` | https://www.pexels.com/photo/7731333/ |
| `florida-coastal-homes` | https://www.pexels.com/photo/19219055/ |
| `property-inspector-clipboard` | https://www.pexels.com/photo/8293667/ |
| `inspector-checklist` | https://www.pexels.com/photo/8293680/ |
| `claim-meeting-paperwork` | https://www.pexels.com/photo/7731328/ |
| `home-insurance-policy` | https://www.pexels.com/photo/7735634/ |
| `post-storm-flooding-florida` | https://www.pexels.com/photo/13865771/ |
| `flooded-house-street` | https://www.pexels.com/photo/28447774/ |
| `tile-roof-inspection` | https://www.pexels.com/photo/37623622/ |
| `miami-beach-skyline` | https://www.pexels.com/photo/20486030/ |
| `tampa-skyline` | https://www.pexels.com/photo/29330870/ |
| `orlando-lake-eola-skyline` | https://www.pexels.com/photo/11665601/ |
| `jacksonville-skyline-bridge` | https://www.pexels.com/photo/15058860/ |
| `fort-lauderdale-beachfront` | https://www.pexels.com/photo/32207987/ |
| `west-palm-beach-waterfront` | https://www.pexels.com/photo/9867776/ |
| `fort-myers-neighborhood-aerial` | https://www.pexels.com/photo/12569258/ |
| `naples-pier-sunset` | https://www.pexels.com/photo/3731068/ |
| `sarasota-skyline` | https://www.pexels.com/photo/31848418/ |
| `st-petersburg-pier` | https://www.pexels.com/photo/9422516/ |
| `north-florida-live-oaks` | https://www.pexels.com/photo/31361526/ |
| `pensacola-beach` | https://www.pexels.com/photo/12382682/ |
