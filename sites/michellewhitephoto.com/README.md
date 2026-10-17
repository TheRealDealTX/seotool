# michellewhitephoto.com — expired-domain rebuild

Static rebuild of michellewhitephoto.com, a Salt Lake City wedding and interiors photography site.
It is a modern redesign, not a copy of the 2018 site.

- **Live:** https://michellewhitephoto.com (temporary URL: https://lavenderblush-mole-750761.hostingersite.com)
- **Hostinger:** Agency Growth plan, order 1008744732, website UID `TgdLuLxCB` (php-fpm 8.3, Phoenix datacenter)
- **Email used on the site:** info@michellewhitephoto.com

## Build and deploy

```sh
python3 build.py      # writes ./public (stdlib only)
./deploy.sh           # uploads ./public to public_html; see the script header for credentials
```

| Path | What it is |
| --- | --- |
| `build.py` | Layout, components and page builders |
| `content.py` | All page copy, FAQs, galleries and journal posts |
| `src/` | CSS, JS, images (WebP, 800w + 1600w), `index.php` router, `contact.php` form handler |
| `public/` | Generated, deployable site |

## Preserved URLs (from the Semrush organic + backlink exports)

| Old URL | Why | Now |
| --- | --- | --- |
| `/` | ~all traffic ("michelle white", "kychelle photography", "michelle white photography") + 1,181 backlinks | Homepage |
| `/about/` | Backlinks + ranking | About page |
| `/blog/mandi-and-riley-nelson` | Ranked (mandi white/nelson photography) | 301 to `/blog/mandi-and-riley-nelson/` |
| `/blog/sarah-winward` | Ranked (sarah winward) | 301 to `/blog/sarah-winward/` |
| `/blog/maris-spencer-2` | Ranked | 301 to `/blog/maris-spencer-2/` |
| `/blog/rebecca-mike` | Ranked | 301 to `/blog/rebecca-mike/` |
| `/blog/madison-bryan-wedding` | Ranked | 301 to `/blog/madison-bryan-wedding/` |

The host's web server adds the trailing slash to directory paths before PHP runs, so the slash form is canonical.
`index.php` also 301s `/blog`, `/about`, `/journal`, `/portfolio`, `/info`, `/investment`, `?format=` feeds
and `/blog/tag|category/*` to their nearest pages. Unknown paths return `404.html` with a real 404.

New pages: `/weddings/`, `/interiors/`, `/blog/` (journal), `/contact/`, `/privacy-policy/`, plus two new guides.

## SEO and tracking

- Google tag `G-FTGZF9WD7R` sits at the top of `<head>` on every page (`GTAG` in `build.py`).
- Search Console HTML verification file: `src/googlecccfbf2f7e9e5ae4.html`, served at the site root.
- Favicons, the touch icon and the web manifest are generated from `src/icon-master.png` by `build_icons()`.
- 1200x630 JPEG share images go in `assets/og/` (`build_og()`). Every `<img>` has width/height, and the first hero image is preloaded.
- Titles are 60 characters or fewer and descriptions 160 or fewer. `sitemap.xml` includes image entries. `robots.txt` is static,
  because the host never routes `.txt` requests to PHP.

## Hosting note

Same pattern as the huttoroofs.com build: no root `index.html`. `home.html` is served by `index.php` for `/`.
The platform serves its own `robots.txt` on `*.hostingersite.com` domains (Googlebot disallowed), so the
temporary URL isn't indexed. All canonicals already point to `https://michellewhitephoto.com`.

## Going live

1. Link `michellewhitephoto.com` to website `TgdLuLxCB` (`agency-hosting_domains_link-to-website` or hPanel)
   and point DNS at Hostinger.
2. `index.php` then 301s `www.` and `http://` to `https://michellewhitephoto.com`, and serves a production robots.txt.
3. Create the `info@michellewhitephoto.com` mailbox. The contact form uses PHP `mail()` to that address.
4. Submit `https://michellewhitephoto.com/sitemap.xml` in Search Console.

## Images

Royalty-free photos from Unsplash (Unsplash License: free commercial use, no attribution required), stored locally.
