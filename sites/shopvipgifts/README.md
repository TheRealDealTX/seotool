# shopvipgifts.com — expired-domain rebuild

Static rebuild of shopvipgifts.com as a curated VIP / luxury gift-ideas site.
Plain HTML + one CSS + two JS files, served by a tiny PHP front controller.

## Hosting
- Hostinger Agency Growth plan, website UID `TN4sIVjvm` (php-fpm, Phoenix).
- Domain attached: `shopvipgifts.com` (DNS not connected yet — point nameservers / A record at Hostinger when ready, then enable SSL).
- Preview: https://aqua-clam-488710.hostingersite.com
- Contact email used site-wide: info@shopvipgifts.com (contact + newsletter forms post to `contact.php`, which uses PHP `mail()`; create the mailbox in Hostinger so delivery works).

## SEO data used
- Organic positions export: only the homepage ranked ("vip gift" #10, "vip gifts" #10, "vipgift" #29).
- Backlinks export: all 1,602 links target the homepage (mostly low-quality directory/spam anchors).
- So the homepage targets "VIP gifts" / "VIP gift" directly, and `index.php` 301s common old shop paths
  (`/shop`, `/products/*`, `/collections/*`, `/cart`, `/blogs/*`, `/pages/about` …) to the closest new page.

## Pages (29 + 404)
Home · Gift guides hub + 6 guides (him, her, corporate, gift boxes, experiences, personalized) ·
4 interactive tools (Gift Finder quiz, Budget Planner, Message Generator, Anniversary Gifts by Year) + tools hub ·
Blog hub + 10 posts · About · Contact · Privacy · Terms · HTML sitemap.

## Build & deploy
```sh
python3 build.py && python3 validate.py
# get FB_URL / FB_AUTH / FB_REST from agency-hosting_files_generate-upload-url (website TN4sIVjvm)
./deploy.sh
# then agency-hosting_cache_clear-website
```
Source: `build.py`, `content/` (copy), `server/` (PHP), `public/assets/` (CSS/JS/images). Output: `public/`.
Images are royalty-free Unsplash photos, resized to WebP.
