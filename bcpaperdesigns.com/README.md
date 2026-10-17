# bcpaperdesigns.com — expired-domain rebuild

Static rebuild of BC Paper Designs, a former Shopify party-decor shop (2017–2020)
that sold themed baby shower and birthday paper sets. The new site is a party-theme
idea library with DIY paper decor and free planning tools. Plain HTML/CSS/JS plus
a small `index.php` front controller; no database.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, page templates, schema, root files. Writes `public/` |
| `siteconfig.py` | Site constants, nav, collections, quiz tags, old-URL aliases, featured themes |
| `content/themes_a.py`, `content/themes_b.py` | 31 theme guides (one per old product URL) |
| `content/blog.py` | 10 blog posts |
| `validate.py` | Post-build checks (one H1, unique titles/descriptions, links, assets, JSON-LD, old URLs covered) |
| `public/` | The deliverable: upload its contents to `public_html` |
| `public/assets/css/site.css`, `js/site.js`, `js/tools.js` | Design system, nav/effects, interactive tools |
| `deploy.sh` | Uploads `public/` through the Hostinger File Browser API |

```sh
python3 build.py && python3 validate.py
```

Needs Python 3.12+ and Pillow (image sizes, icons and the OG image).

## SEO decisions

- **Backlinks:** all 1,850 known backlinks point at the homepage, so `/` carries the brand
  name, a strong hub of internal links and the full theme library.
- **Traffic pages:** every old URL from the Semrush organic export is either rebuilt at its
  exact path or 301'd to the matching rebuilt page.
  - 31 `/products/<slug>/` theme guides keep their original slugs, even the long ones.
  - 7 near-duplicate product URLs 301 to their sibling (`PRODUCT_ALIASES` in `siteconfig.py`).
  - `/collections/<c>/products/<slug>` 301s to `/products/<slug>/`.
  - `/collections/baby-shower-decorations/` and `/collections/banners/` are rebuilt; `?page=N` lands on the same page.
  - Shopify paths (`/pages/about-us`, `/blogs/...`, `/cart`) redirect to their nearest equivalent.
- Each theme page targets the old URL's main keyword in the title, H1, description and intro,
  with its secondary keywords used naturally. Character themes (lion king, baby shark, my little
  pony) use generic designs and carry a not-affiliated note.

## Interactive features

Banner maker (prints one letter per page; theme pages pre-load their palette via
`?text=&colors=`), party food calculator, planning timeline (dated checklist, `.ics`
download), theme finder quiz, baby shower bingo generator, per-theme decor checklists
saved in localStorage, click-to-copy palettes, filterable theme and blog grids.

## Hosting

Hostinger Agency Growth plan, website UID `DVA2OMwns` (php-fpm 8.3), domain
`bcpaperdesigns.com`, preview `https://blueviolet-shark-372196.hostingersite.com`.
The platform serves existing files directly and sends `/` and unknown paths to
`index.php`. If an `index.html` existed, it would answer unknown paths with a 200,
so the homepage is `home.html` served by `index.php`, which also handles the 301s
and real 404s. `index.php`'s redirects are host-relative, so they work on the
preview domain too. The www-to-apex and http-to-https redirects only apply once
the real domain points here.

Contact email: info@bcpaperdesigns.com. The contact form opens the visitor's email app
with the message pre-filled (no server-side mail needed).

Images are royalty-free CC0/public-domain photos (StockSnap, WordPress Photo Directory,
Rawpixel via Openverse), resized to WebP in `public/assets/img/`.
