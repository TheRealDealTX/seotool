# ohmtoherminediy.com — Oh, Mother Mine DIY (rebuild)

A static rebuild of the expired DIY blog **Oh, Mother Mine DIY** (the brand behind
pinterest.com/ohmothermine). DIY home decor, furniture makeovers, kids' crafts,
holiday decor, handmade gifts and organizing, plus five interactive DIY tools.
No WordPress or database — HTML, one CSS file, two small JS files, local WebP
images, and two tiny PHP files (front controller + form mailer).

**Live (temporary domain):** https://mediumseagreen-wallaby-208321.hostingersite.com
— Hostinger Agency Growth plan, website UID `WSPEsjCDT`, Phoenix datacenter, PHP 8.3.
The temp domain sends `X-Robots-Tag: noindex` on PHP-routed pages; canonicals and
the sitemap already point at `https://ohmtoherminediy.com`.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, page templates, schema, sitemap → writes `public/` |
| `content/posts_a.py`, `content/posts_b.py` | The 16 blog posts |
| `content/pages.py` | Categories, tools copy, pillar page, about, legal |
| `src/assets/` | `css/site.css`, `js/site.js` (nav, effects), `js/tools.js` (tools), `img/` |
| `src/root/` | `index.php`, `send.php`, favicons, manifest |
| `public/` | The generated site — this is what gets deployed |
| `validate.py` | Post-build checks (one H1, unique titles/descriptions, links, assets, JSON-LD) |
| `deploy.sh` | Uploads `public/` to the Hostinger website (see header for credentials) |
| `dev-router.php` | Local preview that mimics the host's routing |

```sh
python3 build.py && python3 validate.py
php -S 127.0.0.1:8097 -t public dev-router.php   # preview at http://127.0.0.1:8097
./deploy.sh                                      # needs OMM_FB_* env vars
```

## Pages (37 + 404)

- **Homepage** — every backlink in the audit CSV (1,380 links / 1,341 domains) points
  to `/`, so the homepage is the page carrying the link equity. Its brand anchors
  ("Oh, Mother Mine DIY") match the real Pinterest profile links.
- **`/diys-for-moms/`** — pillar guide. Before expiring, the domain 301'd to a
  third-party "diys-for-moms" page, so this captures that same intent on-site.
- **`/blog/`** (filter + search) and **16 posts** at `/blog/<slug>/`.
- **6 categories** at `/category/<slug>/` (WordPress-style paths).
- **`/diy-tools/`** + 5 tools: paint calculator, chalk paint mixer, project finder
  quiz, makeover budget planner, color palette generator.
- About, Contact (form → `info@ohmtoherminediy.com`), Privacy, Terms, Disclosure,
  HTML sitemap, `sitemap.xml`, `robots.txt`.

## Old URLs

No archived copy of the old site was reachable (Wayback Machine refused
connections) and the domain has no recorded organic traffic, so old post URLs
are unknown. `index.php` covers the usual WordPress patterns: flat `/slug/` and
dated `/2019/05/slug/` permalinks 301 to `/blog/slug/` when the slug matches,
`/category/*`, `/tag/*`, `/author/*`, `/feed/`, `/page/N`, `?p=`, `wp-admin` etc.
redirect to the nearest section, and everything else returns a real 404.

## Hosting notes

The Agency platform serves existing files directly, ignores `.htaccess`, and
routes `/` and unknown paths to `index.php` — so there is **no `index.html`**:
the homepage is `home.html` (disallowed in robots, canonical `/`).

When the real domain is ready: link it to website `WSPEsjCDT`
(`agency-hosting_domains_change-website`), enable SSL, and create the
`info@ohmtoherminediy.com` mailbox. `index.php` then 301s `www.` and `http://`
to `https://ohmtoherminediy.com` and drops the noindex header automatically.
The contact/newsletter form uses PHP `mail()`; test it once the domain's mail
is set up.

## Images

Royalty-free CC0 / public-domain photos (via Openverse), resized to WebP at
1024px and 720px.
