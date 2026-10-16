# ollieharperstudio.com — expired-domain rebuild

A static rebuild of **ollieharperstudio.com** as a modern illustration-studio
site. It keeps the topic and URL structure of the domain's 2014–2017 era, when it
was an LA commercial illustration studio on Squarespace. No CMS, no database:
generated HTML, one CSS file, one JS file and royalty-free (CC0) photography.

- **Live:** https://ollieharperstudio.com (since 2026-10-15). Hostinger Agency Growth,
  website UID `IBqTPWf6a`, Phoenix, PHP 8.3 php-fpm. The temporary domain
  `darkblue-quail-416052.hostingersite.com` was replaced by the real one.

## Build & deploy

```sh
python3 build.py             # production: indexable, sitemap in robots.txt
python3 validate.py          # SEO + integrity checks; must report 0 errors before deploying
./deploy.sh                  # needs OH_FB_URL / OH_FB_AUTH / OH_FB_REST, see header comment
STAGING=1 python3 build.py   # only for a preview copy: noindex everywhere, robots.txt Disallow: /
```

The build uses only the Python 3 standard library. Each build writes its files into this directory.
Local preview: `php -S 127.0.0.1:8099 -t . router.php`, where `router.php` serves
existing files directly and sends everything else to `index.php` (that's how the
host behaves). A plain `python3 -m http.server` can't preview pages, because
they're served by PHP.

| File | What it is |
| --- | --- |
| `build.py` | Layout, all page copy, JSON-LD, sitemap, robots |
| `art.py` | The coloring-page line art (interactive SVG), favicon, lipstick shades |
| `assets/photos/` | CC0 photos as 480/960px WebP, plus `credits.json` (source, creator, license, alt text) |
| `assets/css/site.css`, `assets/js/site.js` | Styles and effects |
| `index.php` | Front controller: https/non-www 301s, page routing, legacy 301s, 404/410 |
| `validate.py` | Post-build checks: titles, descriptions, H1s, canonicals, Google tag, JSON-LD, links, icons, robots, sitemap |
| `_pages/*.php`, `404.html`, `410.html`, `sitemap.xml`, `robots.txt`, `site.webmanifest` | Generated output (committed) |
| `favicon.*`, `apple-touch-icon.png`, `web-app-manifest-*.png` | Icons rendered from `favicon.svg` (the OH mark) |
| `googlecccfbf2f7e9e5ae4.html` | Google Search Console verification file. Keep it. |
| `assets/fonts/` | Self-hosted Fraunces + DM Sans variable fonts (SIL OFL) |

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
owner, and that the photography is stock imagery rather than client work. Keep it that way: presenting the site as
her studio would be impersonation, and is also a common reason expired-domain
sites get flagged.

## Design

Cream paper, ink outlines, and a tomato / blush / mustard / sage / cobalt
palette. Fraunces for display type, DM Sans for body. Effects:

- Hero photos unveil with a clip-path wipe, then drift in a slow Ken Burns zoom
  over an offset color block and a floating disc
- Spinning "commissions open" sticker on the homepage hero
- Full-bleed photo cards with 3D tilt and hover zoom
- Gallery tiles that rotate and zoom on hover
- Staggered scroll reveals, a split-line hero headline and a rotated marquee
- Cursor-following glow, mouse parallax on the hero and a paper grain overlay
- Interactive coloring page: palette, custom color, undo, "surprise me", SVG download

Everything respects `prefers-reduced-motion`.

## Photography

All photos are **CC0 (public domain)** from [StockSnap](https://stocksnap.io),
found through the [Openverse](https://openverse.org) API. They're free for
commercial use, need no attribution and need no permission. Each one is cropped
to 4:3 and saved as 480px and 960px WebP. To swap a photo, replace both
`assets/photos/<name>-480.webp` and `-960.webp` and update its entry in
`credits.json`; the `alt` text there is what the pages use.

| Key | Alt text | Source |
| --- | --- | --- |
| `hero` | Artist's palette, paint tubes and brushes on a wooden studio table | [paint-supplies-TCHBOFXNQ1](https://stocksnap.io/photo/paint-supplies-TCHBOFXNQ1) |
| `studio` | An illustrator painting a watercolor wash with a fine brush | [painting-painter-BEWOYG4VRW](https://stocksnap.io/photo/painting-painter-BEWOYG4VRW) |
| `projects` | Designer working on a laptop beside printed layout sketches | [office-work-42H3JH8QI5](https://stocksnap.io/photo/office-work-42H3JH8QI5) |
| `lipsticks` | A pile of black lipstick tubes on white fur | [lipstick-beauty-LIDZNETFVF](https://stocksnap.io/photo/lipstick-beauty-LIDZNETFVF) |
| `culinary` | Overhead view of a brunch table with waffles, eggs and coffee | [breakfast-food-OC8WX0E0X3](https://stocksnap.io/photo/breakfast-food-OC8WX0E0X3) |
| `fashion` | Fashion portrait of a woman in a camel coat with a faux-fur collar | [fashion-woman-2JSWQ7PQIU](https://stocksnap.io/photo/fashion-woman-2JSWQ7PQIU) |
| `styling` | Styled interior with a patterned orange armchair and side table | [house-interior-XCOZ3XTV7M](https://stocksnap.io/photo/house-interior-XCOZ3XTV7M) |
| `coloring` | Rainbow row of colored pencils on a pink background | [colorful-pencils-UFDTNK6BWQ](https://stocksnap.io/photo/colorful-pencils-UFDTNK6BWQ) |
| `thoughts` | Hands writing in a notebook next to coffee and a croissant | [journal-notepad-DPKNIIN5X3](https://stocksnap.io/photo/journal-notepad-DPKNIIN5X3) |
| `contact` | Minimal desk with a notebook, keyboard and a cup of coffee | [office-desk-0EFDQKW84D](https://stocksnap.io/photo/office-desk-0EFDQKW84D) |
| `about` | An artist's studio crowded with brushes, paint pots and canvases | [paint-brushes-AQ051P63XP](https://stocksnap.io/photo/paint-brushes-AQ051P63XP) |
| `map` | Red-brick corner building with a busy restaurant patio | [houses-apartments-C958DA23C4](https://stocksnap.io/photo/houses-apartments-C958DA23C4) |
| `tile-latte` | Latte with rosetta latte art in a red cup | [coffee-latte-ZJZWZJL0DB](https://stocksnap.io/photo/coffee-latte-ZJZWZJL0DB) |
| `tile-croissant` | Golden croissant on a white plate | [croissant-pastry-3020ACDE09](https://stocksnap.io/photo/croissant-pastry-3020ACDE09) |
| `tile-lemon` | Fresh lemons scattered on a white surface | [lemons-fruits-W28QPZPAK6](https://stocksnap.io/photo/lemons-fruits-W28QPZPAK6) |
| `tile-pizza` | Hands slicing a pepperoni and olive pizza | [pizza-food-R926LU1YEA](https://stocksnap.io/photo/pizza-food-R926LU1YEA) |
| `tile-sunglasses` | Yellow sunglasses on a split blue and pink background | [sunglasses-summer-EVAARS1W4M](https://stocksnap.io/photo/sunglasses-summer-EVAARS1W4M) |
| `tile-heel` | Black heels and white trousers stepping up stone stairs | [fashion-woman-UOQEL3GJBA](https://stocksnap.io/photo/fashion-woman-UOQEL3GJBA) |
| `tile-lipstick` | Colorful eyeshadow palette and makeup on a dark table | [beauty-makeup-34MSYVUYS0](https://stocksnap.io/photo/beauty-makeup-34MSYVUYS0) |
| `tile-pencil` | Fan of colored pencils on a turquoise background | [colored-pencil-KDFVIYEYB2](https://stocksnap.io/photo/colored-pencil-KDFVIYEYB2) |
| `tile-chair` | Cozy living room with bookshelves, a fireplace and armchairs | [house-home-6KJ12UWOKQ](https://stocksnap.io/photo/house-home-6KJ12UWOKQ) |
| `tile-plant` | Succulent in a tin can against a pale blue wall | [house-plant-SUSVDM9A0A](https://stocksnap.io/photo/house-plant-SUSVDM9A0A) |
| `tile-lamp` | Desk with a lamp in front of a bold patterned wallpaper | [office-work-3TJ6NCTIRT](https://stocksnap.io/photo/office-work-3TJ6NCTIRT) |

## Hosting

The host serves any file that exists on disk directly, ignores `.htaccess`,
and only runs `index.php` for paths that don't exist. Pages are therefore
built as `_pages/<slug>.php` rather than `<slug>/index.html`. Every page request
reaches `index.php`, which:

- 301s `http://` and `www.` to `https://ollieharperstudio.com` in one hop
  (adding a missing trailing slash in the same redirect),
- serves `/culinary/` from `_pages/culinary.php` (and `/` from `_pages/home.php`),
- 301s `/culinary` to `/culinary/`, and old Squarespace URLs to their new pages,
- returns 404/410 for everything else.

Each `_pages` file starts with a guard, so requesting it directly returns a 404.
Don't put `index.html` files back in folders: the host would serve them
without the redirects (`validate.py` flags any it finds).

## SEO setup

- Every page has a unique title (≤60 characters) and meta description (110–160),
  one H1, a self-referencing canonical, Open Graph and Twitter tags (1200×630
  `og.png`), and JSON-LD:
  - an `Organization` + `WebSite` graph on every page
  - `BreadcrumbList` on every page except the homepage
  - `FAQPage`, `Service`, `BlogPosting`, `CollectionPage` etc. per page
- Google tag `G-7Q3VFC1CX1` is the first thing in `<head>` on every page,
  including the 404/410 pages. It's defined once as `GTAG` in `build.py`.
  The privacy policy discloses Google Analytics.
- Icons: `favicon.ico` (16/32/48), `favicon.svg`, 96px PNG, 180px
  `apple-touch-icon.png`, plus 192/512px manifest icons and a maskable icon.
  `site.webmanifest` is written by the build.
- Fonts are self-hosted, preloaded and use `font-display: optional`, so there is no layout shift.
  Lighthouse on the homepage (2026-10-16): Performance 91, Accessibility 93,
  Best Practices 100, SEO 100, CLS 0.
- `robots.txt` allows everything and lists the sitemap. The 2018 spam `.php`
  URLs are deliberately *not* disallowed, so Google can recrawl them, get the 404
  and drop them.

## Next steps (manual)

1. In Google Search Console, verify `https://ollieharperstudio.com` with the HTML-file method (the file is live), then
   submit `https://ollieharperstudio.com/sitemap.xml`.
2. Use *Removals* or wait for recrawl so the 2018 spam URLs drop out of the index.
   Consider disavowing the spam anchors ("Buy Backlinks", "PBN Network Service"…).
3. Create the mailbox `info@ollieharperstudio.com`; the contact form sends to it.
