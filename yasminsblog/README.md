# yasminsblog.com: expired-domain rebuild

A static rebuild of yasminsblog.com, a New York food, culture and photography
blog that used to run on Squarespace. It's plain HTML, one CSS file, one JS
file and a short `index.php` router, with no CMS or database.

```sh
python3 build.py      # writes ./public
python3 validate.py   # SEO + link checks, and confirms every legacy URL is built
php -S 127.0.0.1:8099 -t public devrouter.php   # local preview (mimics Hostinger)
```

## What was rebuilt, and why

Every URL that had **organic rankings** (Semrush positions export) or
**backlinks** (Semrush backlinks export) is rebuilt at its **exact original
path**, with no trailing slash, as Squarespace served it:

| URL | Signal |
| --- | --- |
| `/` | ~650 backlinks (Medium, The Kitchn, Apartment Therapy author pages) |
| `/mamablog/2020/5/5/turkish-immigrant-restaurant-owners-in-new-york-amp-london` | 26 backlinks (Medium) |
| `/mamablog/category/Photography` | 2 backlinks |
| `/mamablog/2020/3/28/24-hours-in-new-orleans-a-mini-mardi-gras-bender` | 1 backlink |
| `/mamablog/tag/porto+rico+importing+co` | #18–19 for "porto rico importing (co)" (3,600 + 480/mo) |
| `/mamablog/2018/10/20/porto-rico-importing-co` | porto rico coffee nyc / wholesale |
| `/mamablog/2018/1/20/katz-deli-some-delicious-pastrami` | why is katz deli so expensive, can cats have pastrami |
| `/mamablog/2018/4/17/little-tong-noodle-shop` | little tong noodle shop (880/mo) |
| `/mamablog/2018/2/17/mountain-province` | mountain province coffee (#14) |
| `/mamablog/2018/9/11/journalistic-inquiry-notes-quotes-and-details` | ramen quotes, ramen festival nyc (#13–27) |
| `/mamablog/2018/10/30/its-more-than-just-a-slice-to-end-the-night` | dollar pizza lower east side |
| `/mamablog/2018/12/17/defining-your-own-rules-welcome-to-the-new-age-of-spirituality` | catland, eggshells in witchcraft |
| `/mamablog/2019/1/2/pies-thighs-and-all-things-nice` | pies n thighs brunch |
| `/mamablog/2019/5/9/more-than-skin-deep-with-byron-kim` | stick and poke tattoo tokyo |
| `/mamablog/2019/5/12/on-pole-dancing-with-shawanda-davis` | foxy pole / pole dancing |
| `/mamablog/2019/11/2/young-women-come-together-at-photoville-…` | jessica bennett / anya strzemien nytimes |
| `/mamablog/2020/6/13/4-photos-from-economy-candy` | economy candy store nyc |
| `/mamablog/2020/6/26/4-photos-from-salerno` | 4 photos |
| `/mamablog/2018/4/24/subway-photos-trial-no1` | walker evans subway photography |
| `/mamablog/tag/jaden+smith`, `/tag/human.nyc`, `/tag/new+york` | tag-page rankings |

New supporting pages: `/mamablog` (filterable journal), the four category
pages, `/about`, `/contact`, `/privacy-policy`, `/mamablog/feed.xml` (also
served at `/mamablog?format=rss`, the old Squarespace feed URL), `sitemap.xml`
and `robots.txt`.

The Wayback Machine could not be reached from the build environment, so the
structure comes from the two Semrush exports. The copy is newly written:
nothing from the old site was copied. The articles are fact-checked editorial
guides on the same topics, with no invented quotes, interviews or first-person
experiences, and nobody's real identity is used. `/about` says the site is
independently operated and not affiliated with any previous owner of the domain.

## Design

An editorial look: Fraunces (display serif) and Inter, with a cream, tomato,
mustard and teal palette and automatic or toggled dark mode. Effects include
floating gradient blobs with film grain, a cursor spotlight on the hero, a
gradient-shimmer headline, an animated card stack, a rotating text badge, a
tilted marquee, scroll-reveal animation, 3D tilt on cards, cover-art shapes
that move on hover, parallax post headers, a reading-progress bar and a
hide-on-scroll header. Everything respects `prefers-reduced-motion`.

**Photos** are real, royalty-free images (CC0, Public Domain, CC BY or
CC BY-SA, all free for commercial use), found through
[Openverse](https://openverse.org) and checked one by one. Place-specific
posts show the actual place (the Katz's, Porto Rico, Economy Candy and 2 Bros
storefronts, Salerno itself). Generic food shots are never captioned as a
particular restaurant.

- `images.py`: which photo goes where (hero, inline figures, the "4 Photos" plates), with alt text and captions.
- `photos.json`: title, author, licence and source for every photo. It feeds the per-image credit lines and `/photo-credits`.
- `static/assets/img/photos/<name>.webp` (1600px) and `-sm.webp` (800px), served with `srcset`. Open Graph images are 1200×630 JPEG crops of each post's hero.

CC BY and CC BY-SA require attribution, so keep the credit lines and the
`/photo-credits` page. To swap a photo, drop the new files into the photos
folder, add its entry to `photos.json` and point `images.py` at it.

## Hosting (Hostinger Agency, plain php-fpm website)

**Live (staging):** https://darkorange-lobster-110332.hostingersite.com
on Agency Growth order `1008744732`, website UID **`X7EvpZ4Zq`**, PHP 8.3,
created 2026-10-10.

How the platform behaves, and how the build works around it:

- It serves existing files directly, ignores `.htaccess`, and sends every
  other path to `index.php`.
- **Any URL that matches a real directory is 301'd to `<url>/` before PHP
  runs.** So pages are stored as `_pages/<path>.html` (for example
  `_pages/mamablog/2018/1/20/katz-deli-some-delicious-pastrami.html`), not
  `<path>/index.html`, and `index.php` serves them at the slash-less legacy
  URL with a 200. Never upload a directory whose path matches a page URL.
  `_pages/` is disallowed in robots.txt.
- There is no root `index.html`: `index.php` serves `home.html` at `/`.
- Trailing-slash, case and alias variants 301 to the canonical URL.
- On `yasminsblog.com` / `www.yasminsblog.com`, http and non-www 301 to
  `https://www.yasminsblog.com` (the host the old site ranked on).
- On **any other host** (the temporary domain) every routed page sends
  `X-Robots-Tag: noindex, nofollow`. This switches off by itself once the real
  domain is attached, with no rebuild needed.

Deploy with `./deploy.sh` (see its header for credentials), then clear the
cache (`agency-hosting_cache_clear-website`). The deploy script only uploads,
and old files stay on the server. To remove one, use the File Browser REST API
with the same credentials:
`curl -X DELETE -H "X-Auth: …" -H "X-Auth-Rest: …" "<url-without-/tus>/resources/public_html/<path>"`.

Local preview that behaves like the host: `php -S 127.0.0.1:8099 -t public devrouter.php`.

## Going live on yasminsblog.com

1. Once the domain is registered, attach it:
   `agency-hosting_domains_change-website` (website `X7EvpZ4Zq`, from
   `darkorange-lobster-110332.hostingersite.com` to `yasminsblog.com`), and
   link `www.yasminsblog.com` too. Point DNS at Hostinger and wait for SSL.
2. Check that `https://yasminsblog.com/…` 301s to `https://www.…` and that the
   `X-Robots-Tag` header is gone.
3. Submit `https://www.yasminsblog.com/sitemap.xml` in Google Search Console.

## Before going live

- Set up the `hello@yasminsblog.com` mailbox, or change `SITE["email"]` in `content.py`.
- Recheck the visit details in the posts (hours, which shops are still open).
