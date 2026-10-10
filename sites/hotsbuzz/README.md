# hotsbuzz.com — expired-domain rebuild

A static rebuild of **hotsbuzz.com**, a DIY projects and crafts site (its old
tagline: *"DIY projects | DIY ideas | crafts | And More"*). The generator,
content and deployable output all live in this folder. It is independent of
the huttoroofs.com site at the repo root, and the root `deploy.sh` skips
`sites/`.

```sh
python3 build.py && python3 validate.py         # regenerate ./public and check it
node render_og.mjs && python3 build.py          # only after adding/renaming posts: social images + icons
./deploy.sh                                     # upload ./public (see header for credentials)
```

Standard library Python only. `render_og.mjs` uses the preinstalled Playwright/Chromium.
Preview: `cd public && python3 -m http.server`, then open `/home.html`. Or use PHP's
built-in server with a router that serves real files and falls back to `index.php`.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | **The deliverable.** Upload its contents to `public_html/`. |
| `build.py` | Generator: layout, pages, JSON-LD, sitemap, feed, cover art |
| `siteconfig.py` | Site name, origin, categories and colors, the `STAGING` switch |
| `content/posts_*.py` | The 23 tutorials (schema in `content/SCHEMA.md`) |
| `motifs.py` | SVG motifs used for the generated cover art and decor |
| `assets/` | `site.css`, `site.js`, `og/` social images (rendered) |
| `static/` | Root files copied as-is: `index.php`, icons, manifest |
| `validate.py` | Post-build checks: one H1, unique titles and descriptions, valid JSON-LD, no broken links |

## Backlinks and link equity

The backlink export (506 links from 455 domains) points **only at the homepage**:
466 to `https://hotsbuzz.com/` and 40 to `http://hotsbuzz.com/`. No inner URLs
have links. So the main job is a strong homepage that returns **200 at `/`**, plus
`http://` and `www.` returning a 301 to `https://hotsbuzz.com/` (handled in `index.php`).

The Wayback Machine could not be reached from the build environment. The
structure was rebuilt from the brand's surviving Pinterest profile, whose boards
map one-to-one to the categories here: DIY Home Decor, Creative Crafts,
Christmas DIY & Crafts, Halloween, Thanksgiving, Valentine's Crafts and
St. Patrick's Day Crafts. The site uses WordPress-style URLs (`/post-slug/`,
`/category/slug/`). `index.php` 301s the usual WordPress leftovers (`/feed/`,
`/page/N/`, `/tag/…`, `/author/…`, date archives, `/?s=`, `/wp-admin`, likely old
category slugs) to their closest new page. If an archive check later turns up old
post URLs with links, add a matching post, or a 301, to `index.php`.

**Link quality warning:** most of the referring domains are PBN, link-seller and
"website stats" spam (anchors such as "High Quality Dofollow Backlinks DA 50 PA 40…").
The roughly 14 Pinterest links are the real, topical ones. Consider a disavow file
for the spam domains once the site is live in Search Console.

## Hosting

The site is built for the same kind of plain php-fpm Hostinger Agency website as
huttoroofs.com. The platform serves real files directly and routes `/` and unknown
paths to `index.php`. Because of that there is deliberately **no `index.html`**: the
homepage is `home.html`, served by `index.php`, and unknown paths get `404.html`
with a real 404.

### Where it lives

Hostinger Agency website UID **`Rgklz2dNn`** (order 1008744732, phoenix, php-fpm 8.5),
created 2026-10-10 on the temporary domain
**https://springgreen-goshawk-823337.hostingersite.com**. Deployed with `./deploy.sh`.
Hostinger's placeholder `default.php` was deleted after the first upload.

### Temporary domain → hotsbuzz.com

While the site lives on the temporary Hostinger domain, `STAGING = True` in
`siteconfig.py`. In that mode every page carries `noindex, nofollow` and
`robots.txt` blocks crawling, so the temporary hostname is never indexed.
Canonicals, sitemap and JSON-LD already point at `https://hotsbuzz.com`.

On the day hotsbuzz.com is connected:
1. Point hotsbuzz.com's nameservers/DNS at Hostinger, then attach it to website `Rgklz2dNn`
   (`agency-hosting_domains_change-website` from the temporary domain, or hPanel).
2. Set `STAGING = False`, then run `python3 build.py && python3 validate.py && ./deploy.sh`, and clear the cache.
3. Check that `http://hotsbuzz.com/` and `https://www.hotsbuzz.com/` 301 to `https://hotsbuzz.com/`.
4. Add the site to Google Search Console and submit `/sitemap.xml`.

## Known gaps

- `hello@hotsbuzz.com` (Contact page) needs a real mailbox or forwarder.
- Cover art is generated illustration, not photography. Swap in real project
  photos as they are made, for better image search and Pinterest performance.
