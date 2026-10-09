# ollieharperstudio.com — expired-domain rebuild

A static rebuild of **ollieharperstudio.com** as a modern illustration-studio
site. It keeps the topic and URL structure of the domain's 2014–2017 era, when it
was an LA commercial illustration studio on Squarespace. No CMS, no database:
generated HTML, one CSS file, one JS file and original SVG artwork.

- **Staging (live now):** https://darkblue-quail-416052.hostingersite.com
  (Hostinger Agency Growth, website UID `IBqTPWf6a`, Phoenix, PHP 8.3 php-fpm)
- **Production:** https://ollieharperstudio.com, once the domain is registered
  and attached (see *Going live*).

## Build & deploy

```sh
STAGING=1 python3 build.py   # temporary domain: noindex on every page, robots.txt Disallow: /
python3 build.py             # production: indexable, sitemap in robots.txt
./deploy.sh                  # needs OH_FB_URL / OH_FB_AUTH / OH_FB_REST, see header comment
```

The build uses only the Python 3 standard library. Each build writes its files into this directory.
Local preview: `php -S 127.0.0.1:8099 -t .` plus a small router that serves
`dir/index.html`. A plain `python3 -m http.server` won't run `index.php`, so
open `/home.html` for the homepage there.

| File | What it is |
| --- | --- |
| `build.py` | Layout, all page copy, JSON-LD, sitemap, robots |
| `art.py` | Every illustration, drawn as SVG (no stock images) |
| `assets/css/site.css`, `assets/js/site.js` | Styles and effects |
| `index.php` | Front controller: homepage, legacy 301s, 404/410 |
| `home.html`, `*/index.html`, `404.html`, `410.html`, `sitemap.xml`, `robots.txt`, `assets/img/*.svg` | Generated output (committed) |

## SEO research behind the page list

**Backlinks (Semrush export, 253 links):** every link points to the homepage
(`/` 252, plus one to `/images/wynagov.gif`). The editorial links worth keeping
come from apartmenttherapy.com and createcultivate.com, crediting the studio's
illustrations. The rest are mostly PBN and "buy backlinks" spam with
exact-match anchors. **Link equity is recovered through the homepage**, which is
why `/` is the strongest, most complete page.

**Organic positions (Semrush, 240 rows / 143 URLs):** every ranking URL dates
from Aug–Oct 2018, after the domain had lapsed and been taken over for adult
spam doorway pages (`/outdoor/…-tumblr.php`, `/kinky/…php`, etc.). These were
deliberately **not rebuilt**. They would put adult content on the domain, risk
a manual action, and the backlinks never pointed to them anyway.

**Legitimate URLs (Wayback CDX, 2014–2017), rebuilt at the same paths:**

| URL | Then | Now |
| --- | --- | --- |
| `/` | "commercial" portfolio | Commercial illustration homepage |
| `/culinary/` | culinary portfolio | Culinary illustration |
| `/images/` | fashion illustration portfolio | Fashion & beauty illustration (URL kept) |
| `/coloring-book/` | coloring book | Coloring book with an interactive coloring page |
| `/set-stylingdirection/` | prop styling | Prop styling & set direction |
| `/projects/` | project posts | Project types and process |
| `/thoughts/` | blog | Journal index |
| `/thoughts/lipstick-theory/` | blog post | Rewritten "Lipstick Theory" |
| `/thoughts/artsdistrictingredients/` | blog post | Rewritten food-map process post |
| `/contact/` | contact | Contact form (opens mail app) |
| `/about/` | — | New; `/aboutamber/` 301s here |

The legacy redirects in `index.php` are: `/aboutamber/` → `/about/`,
`/blog/` → `/thoughts/`, `/design/` and `/commercial/` → `/`, and
`/YYYY/M/D/...` Squarespace permalinks → `/projects/`. Paths without a trailing
slash get a 301 to the slashed version.

**Spam URLs:** the platform answers missing `.php` and static-file paths
itself with a 404, before `index.php` runs. So the 2018 spam URLs return 404
rather than the 410 that `index.php` would send. Google drops both. If you want
true 410s, create stub files at those paths.

## Identity note

The 2017 studio belonged to a real, still-working illustrator, and the
Apartment Therapy links credit her by name. The rebuild does **not** use her
name, bio, client list or artwork, and `/about/` states that the studio
relaunched under new ownership and isn't affiliated with the domain's previous
owner. All artwork is drawn in `art.py`. Keep it that way: presenting the site as
her studio would be impersonation, and is also a common reason expired-domain
sites get flagged.

## Design

Cream paper, ink outlines, and a tomato / blush / mustard / sage / cobalt
palette. Fraunces for display type, DM Sans for body. Effects:

- Animated morphing color blobs and floating SVG objects
- Coffee steam and twinkling sparkles
- Staggered scroll reveals and a split-line hero headline
- Rotated marquee
- 3D tilt cards and a cursor-following glow
- Paper grain overlay
- Interactive coloring page: palette, custom color, undo, "surprise me", SVG download

Everything respects `prefers-reduced-motion`.

## Going live checklist

1. Register ollieharperstudio.com and point it at Hostinger. Then attach it to website
   `IBqTPWf6a` (`agency-hosting_domains_change-website`, from the temp domain).
2. `python3 build.py && ./deploy.sh` (production build: drops noindex), then clear the cache.
3. Check that `https://ollieharperstudio.com/robots.txt` is ours (the preview domain
   serves Hostinger's own robots.txt), and that `www` and `http` 301 to `https://ollieharperstudio.com`.
4. Create the mailbox `hello@ollieharperstudio.com`, or change `EMAIL` in `build.py`.
5. Add the domain to Google Search Console, submit `sitemap.xml`, and consider
   disavowing the spam anchors ("Buy Backlinks", "PBN Network Service"…).
