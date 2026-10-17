# kotric.com: static rebuild

A rebuild of the expired domain **kotric.com**, a fabric crafts, DIY projects and sewing blog.
It's a static HTML site behind a small PHP front controller, hosted on the Hostinger Agency Growth plan.

- **Hostinger website UID:** `OZUvakKhz` (php-fpm 8.3, Boston datacenter)
- **Domain:** kotric.com (attached; DNS not connected yet)
- **Preview:** https://wheat-emu-881126.hostingersite.com
- **Contact email:** info@kotric.com

## Build, check and deploy

```sh
python3 build.py      # writes ./public
python3 validate.py   # links, anchors, assets, titles, JSON-LD
./deploy.sh           # see the header comment for the three upload credentials
```

Page copy lives in `content/` (`posts.py`, `posts_more.py`, `projects.py`, `pages.py`, `tools.py`).
The layout, SEO tags and sitemap are in `build.py`. Styles and scripts are `assets/css/site.css` and `assets/js/site.js`.
Root files (index.php, contact.php, robots.txt, icons) are in `static/`.

## Recovered URLs (from the backlink export)

| URL | Backlinks | Status |
| --- | --- | --- |
| `/` | 1,409 (1,368 domains) | Rebuilt homepage |
| `/no-sew-fabric-craft-projects/` | 39 (incl. engineermommy.com) | Rebuilt: "41 Amazing No-Sew DIY Fabric Projects", filterable, with a made-it tracker |
| `/4no-sew-diy-fabric-projects/` | 38 | Rebuilt: 4 step-by-step no-sew tutorials |

Note: almost all of the homepage links come from spammy auto-generated directory sites
("Premium Backlinks…" anchors). Consider a disavow file for those domains.

## Hosting notes

The host serves existing files directly and sends `/` and unknown paths to `index.php`.
That's why the homepage is `home.html`, and why there must be no root `index.html`.
`index.php` returns real 404s, 301s old WordPress paths, and forces https and the non-www host once the domain is live.
`contact.php` emails info@kotric.com and keeps a copy in `../kotric-contact-messages.log`, outside the web root.

Images are CC0 photos from StockSnap and need no attribution.
