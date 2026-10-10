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

There are no stock photos. Each post gets **seeded generative cover art**
(inline SVG, so each post's art is unique and stays the same between builds),
plus a matching 1200×630 Open Graph PNG made with Pillow.

## Hosting (Hostinger Agency, plain php-fpm website)

The platform serves existing files directly, ignores `.htaccess`, and sends
every other path to `index.php`. So:

- There is no root `index.html`. The homepage is `home.html`, served by
  `index.php` at `/`.
- Pages are stored at `<path>/index.html`, and `index.php` serves them at the
  slash-less legacy URL with a 200. Trailing-slash variants 301 to the
  canonical form, and case variants and common aliases 301 as well.
- On `yasminsblog.com` / `www.yasminsblog.com`, http and non-www 301 to
  `https://www.yasminsblog.com` (the host the old site ranked on).
- On **any other host** (for example the temporary `*.hostingersite.com`
  domain) every routed page gets `X-Robots-Tag: noindex, nofollow`, so the
  staging copy can't compete with the real domain. This switches off by itself
  once the real domain points at the site, with no rebuild needed.

Deploy with `./deploy.sh` (see the header comment for credentials).

## Before going live

- Point the domain at the website, then submit `sitemap.xml` in Search Console.
- Set up the `hello@yasminsblog.com` mailbox, or change `SITE["email"]` in `content.py`.
- Recheck the visit details in the posts (hours, which shops are still open).
