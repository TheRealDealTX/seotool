# heathergreenstudios.com — expired-domain rebuild

A static rebuild of heathergreenstudios.com as **HGS Studio Journal**, an
independent journal of printmaking, works on paper and the Bisbee, Arizona
art scene. Plain HTML/CSS/JS plus two small PHP files; no database.

**Live (temporary domain):** https://lightcoral-mole-192256.hostingersite.com
Hostinger Agency Growth order `1008744732`, website UID `BzzTLgzXV`, Phoenix
datacenter, php-fpm 8.3. Contact email: info@heathergreenstudios.com.

## Build and deploy

```sh
python3 build.py     # writes ./public (stdlib only)
./deploy.sh          # uploads ./public to public_html (see header for credentials)
```

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, pages, generative SVG artwork, schema, sitemap |
| `content/posts.py` | The 12 journal articles |
| `src/` | Static assets plus `index.php` (front controller) and `contact.php` (form → email) |
| `public/` | Build output, the deployable site (committed, like the repo's other site) |

Local preview with the PHP routing: `php -S 127.0.0.1:8765 -t public <router>`.
A router that serves existing files and falls back to `index.php` is enough.

## Research behind it

- **Backlinks (750 in the CSV):** every link targets the homepage (742 to
  `https://heathergreenstudios.com/`, 8 to `http://www.…/`). The few
  editorial ones are stylebyemilyhenderson.com ("How to Hang Art Correctly"),
  maps.roadtrippers.com (Bisbee listing), theimaginationtree.com and
  rockforrehab.blogspot.com. The rest are spam directories with
  "link building" anchors, which are worth disavowing once the domain is in
  Search Console.
- **The old site** was the Blogger blog heathergreenstudios.blogspot.com
  (2009–2015, 55 posts): a printmaker's studio and gallery on Subway Street
  in Bisbee, AZ. It covered printmaking, paper dresses, anniversary open
  calls, the Bisbee After 5 / second-Saturday art walk and mail art.
- **Traffic data:** Semrush returned no API units, so page-level traffic
  history could not be pulled. Because all link equity points at `/`, the
  homepage is the priority, and the blog's most substantial topics were rebuilt
  at their **original Blogger paths** (`/YYYY/MM/slug.html`).

## Page inventory (20 pages)

Home, `/printmaking/`, `/bisbee-art-guide/`, `/journal/`, `/about/`,
`/contact/`, `/privacy-policy/`, 404, and the journal articles:

- `/2011/07/how-to-print-linoleum-block.html`
- `/2009/03/dos-and-donts-of-collecting-artists.html`
- `/2009/02/original-art-for-little-scratch.html`
- `/2011/04/paper-quilts.html`
- `/2012/02/stitches-and-folds.html`
- `/2009/06/great-reference-for-artists-books.html`
- `/2012/03/wall-musings.html`
- `/2015/01/call-to-artists-mail-art-exchange.html`
- `/2009/03/date-night-bisbee-after-5.html`
- `/2011/11/my-paper-anniversary.html`
- `/2015/04/life-is-process-as-is-art.html`
- `/journal/how-to-hang-art/`: new; matches the Emily Henderson backlink's topic and includes a hanging-height calculator

`index.php` 301s the remaining old Blogger URL shapes (`/YYYY/MM/*.html`,
`/YYYY/`, `/search/…`, `/feeds/…`) to `/journal/` and `/p/*.html` to
`/about/`; anything else gets a real 404.

## Content and brand

All article text is newly written; nothing was copied from the old blog. No
images from the old blog are used either: every illustration is generated SVG
"print" artwork (Mule Mountain ridges, sun discs, halftone and hatching). The
site does not present itself as the original artist. The About page explains
the domain's history and states that the journal is independent and not
affiliated with her.

## Design

Copper `#b8602c` and turquoise `#1f8a83` (Bisbee's copper and Bisbee Blue),
ink and paper. Fraunces + Space Grotesk. Effects: a pointer-reactive ink-bloom
canvas hero, word-by-word headline reveals, scroll reveals, a rotating badge, a
marquee, tilt-on-hover plates, an ink cursor, count-up stats, a reading
progress bar, a filterable journal and an active table of contents.
`prefers-reduced-motion` turns the motion off.

## When the domain is ready

1. Link heathergreenstudios.com to website `BzzTLgzXV`
   (`agency-hosting_domains_change-website`, from the temporary domain) and
   point DNS at Hostinger. Canonicals, sitemap and schema already use
   `https://heathergreenstudios.com`. `index.php` redirects `www.` to the apex.
2. Create the `info@heathergreenstudios.com` mailbox so `contact.php` mail is
   delivered (it sends with PHP `mail()`, From and To that address).
3. Submit `sitemap.xml` in Search Console and disavow the spam backlinks.
