# jazandtheo.com — rebuild

A static HTML/PHP rebuild of the expired domain **jazandtheo.com**, once the blog
of a husband-and-wife wedding and portrait photography team (El Paso, Tucson,
the Gila Valley, Phoenix, later Austin). It is now an independent journal on the
same subjects: weddings, portraits, the desert Southwest and DIY home projects.
No WordPress, no database — HTML, one stylesheet, two scripts and local images.

This folder is self-contained: everything in it (minus the sources listed
below) is what gets uploaded to `public_html`.

## What's here

| Path | What it is |
| --- | --- |
| `home.html`, `*/index.html`, `404.html` | The generated site (committed) |
| `index.php` | Front controller: serves `/`, 301s old WordPress URL shapes, real 404s |
| `contact.php` | Contact form handler — emails **info@jazandtheo.com** |
| `assets/css/site.css` | The stylesheet (tokens, layout, effects, mobile nav, tools) |
| `assets/js/site.js` | Header, mobile nav, scroll reveals, parallax, counters, tilt, lightbox, TOC, checklists, AJAX form |
| `assets/js/tools.js` | The eight interactive tools |
| `assets/img/` | Royalty-free photos (CC0 / public domain) at 800/1600 px WebP, heroes also 2400 px; `manifest.json` records each source |
| `wp-content/uploads/…` | The three old image URLs that still have backlinks, kept at their exact paths |
| `build.py` | Generator: layout, page builders, JSON-LD, sitemap.xml, rss.xml, robots.txt |
| `content/posts/*.html` | The 35 posts — JSON front matter + HTML body with `<!--img:-->` / `<!--tool:-->` markers |
| `content/pages.py`, `content/tools.py` | Hub, About, Privacy and tool-page copy |
| `content/legacy-urls.txt` | Every old URL with rankings or backlinks; `validate.py` checks each resolves |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads the build through the Hostinger File Browser API |

## Rebuilding

```sh
python3 build.py      # regenerate every page
python3 validate.py   # verify: one H1, unique titles/descriptions, JSON-LD, links, assets, legacy URLs
php -S localhost:8000 index.php   # local preview with the front controller
```

## URLs preserved

From the SEMrush positions export (June 2020) and the backlink export:

- **Home** `/` (ranked for El Paso wedding photography terms; ~2,000 backlinks)
- **Hubs** `/weddings`, `/portraits`, `/lifestyle`, `/shop` (now with trailing slash; index.php 301s the slashless form)
- **Archives** `/blog/page/2/`, `/category/wedding/`, `/tag/amy-and-jordan-business-course/`, `/tag/jaz-and-theo-weekly-adventures/`
- **27 posts** at their exact old URLs, including the two with backlinks only
  (`/2018/08/all-about-windows/`, `/2020/08/lake-powell-desitination-wedding-mikay-ryker/`)
- **3 image URLs** under `/wp-content/uploads/` that external pages hotlink

Old posts that were wedding/session write-ups for real couples were rewritten
as location and venue guides on the same topic. Couples' names are kept only
in the URL slugs (validate.py fails the build if one appears in page copy), and
nothing claims the editors photographed a real event.

## New content

- 8 new 2026 guides (cost of wedding photography, wedding-day timeline, golden
  hour, El Paso locations, Arizona elopements, engagement outfits, Austin photo
  spots, senior checklist)
- 8 free tools at `/tools/`: golden hour calculator, wedding timeline builder,
  photography cost calculator, chandelier size calculator, peg rail planner,
  cloth napkin savings calculator, wedding exit quiz, outfit palette picker.
  Each is embedded in the matching posts too.
- `/shop/` is a free-printables page (no store).

## Hosting

Hostinger Agency Growth plan, website UID **`tjhqL1FqG`** (plain php-fpm,
PHP 8.4, Phoenix datacenter), on the temporary domain
**https://darkseagreen-wildcat-209722.hostingersite.com** until jazandtheo.com
is ready. While it is on the temporary domain, `index.php` sends
`X-Robots-Tag: noindex` and every canonical tag already points at
`https://jazandtheo.com`.

The platform serves existing files directly, ignores `.htaccess`, and routes `/`
and unknown paths to `index.php` — unless an `index.html` exists at the root.
So the homepage is `home.html`, served by `index.php` for `/` (and disallowed in
robots.txt).

### Moving to jazandtheo.com

1. Point the domain at Hostinger and link it: `agency-hosting_domains_change-website`
   (website `tjhqL1FqG`, from the temporary domain to `jazandtheo.com`) or hPanel.
2. Wait for SSL, then check `https://jazandtheo.com/` and a few legacy URLs.
3. Set up the mailbox/forwarder for **info@jazandtheo.com** so contact-form mail
   is delivered (until then `mail()` may be rejected; messages are also logged
   to `../inquiries/` outside the web root).
4. Submit `https://jazandtheo.com/sitemap.xml` in Google Search Console.

## Deploying

```sh
python3 build.py && python3 validate.py && ./deploy.sh
```

`deploy.sh` needs the three File Browser credentials from
`agency-hosting_files_generate-upload-url` (see its header). Clear the site cache
afterwards (`agency-hosting_cache_clear-website`).
