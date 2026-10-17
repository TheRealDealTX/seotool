# live-style.co.uk — expired-domain rebuild

A static rebuild of live-style.co.uk, a London interiors & lifestyle journal (2013–2016),
with fresh writing at the original URLs. Python standard library only.

```sh
python3 build.py      # writes the site into public/
python3 validate.py   # links, assets, one H1, unique titles/descriptions, JSON-LD, required legacy URLs
./deploy.sh           # uploads public/ to Hostinger (see header comment for credentials)
```

## Hosting

- Hostinger Agency Growth plan, website UID `8ppHiZSjN` (UK datacentre, php-fpm 8.3).
- Temporary domain: https://papayawhip-beaver-497975.hostingersite.com
- When live-style.co.uk is ready, link it with `agency-hosting_domains_link-to-website` /
  `agency-hosting_domains_change-website`. Canonicals, OG tags and the sitemap already use
  `https://live-style.co.uk`; `index.php` forces https and strips `www.` on the real domain.
- Like the other Agency sites, the platform serves existing files directly and routes `/` plus
  unknown paths to `index.php` (it ignores `.htaccess`). So there is no root `index.html`: the
  homepage is `home.html`, served by `index.php`, which also handles robots.txt (noindex everywhere
  except the real domain), legacy WordPress redirects and real 404s.
- `contact.php` mails the contact form to info@live-style.co.uk with PHP `mail()`. Create
  that mailbox (or a forwarder) once the domain is live.

## Pages rebuilt from the SEO data

Every URL in the backlink and organic-positions exports exists, at the same path:

- Backlinked: `/`, `/2013/06/30/open-shelving-in-kitchens/`,
  `/2013/11/28/open-studio-and-christmas-fair-in-london/`, `/2013/08/25/swedish-charms/`
- Organic traffic/rankings: 28 article URLs, 3 tag pages (`/tag/west-elm-james-harrison-rocker/`,
  `/tag/wallsandfloors-co-uk/`, `/tag/custard-cream-photography/`), the
  `/2016/01/22/end-of-sale-edit/christine-lemieux/` attachment URL (rebuilt as a profile page),
  and `/?cat=134588537`, which 301s to `/category/january-cure/`.
- Legacy patterns: `/feed/`, `/page/N/`, `/author/*`, date archives, `wp-*` paths, and any
  unknown child of a real page (`/amp/`, `/feed/`, attachment pages) 301 to the nearest page.

The full list is enforced by `REQUIRED` in `validate.py`.

## Content

`content/posts_*.py` hold the 31 articles (see `CONTENT-BRIEF.md` for the format and voice).
`posts_d.py` also carries the tag and category intros. The Wayback Machine was blocked
from the build environment, so the copy is newly written from the URLs and ranking keywords and
fact-checked with web search, not copied from the old site. Writing is in an editorial "we" voice
and doesn't use the original author's name.

Tags with only one article (other than the three ranking tag pages) are `noindex` and left out of
the sitemap.

## Images

Royalty-free Unsplash photos in `assets/img/` (1600px) and `assets/img/thumbs/` (720px).
