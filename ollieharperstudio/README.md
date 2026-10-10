# ollieharperstudio.com — expired-domain rebuild

A static rebuild of **ollieharperstudio.com** as a modern illustration-studio
site. It keeps the topic and URL structure of the domain's 2014–2017 era, when it
was an LA commercial illustration studio on Squarespace. No CMS, no database:
generated HTML, one CSS file, one JS file and royalty-free (CC0) photography.

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
| `art.py` | The coloring-page line art (interactive SVG), favicon, lipstick shades |
| `assets/photos/` | CC0 photos as 480/960px WebP, plus `credits.json` (source, creator, license, alt text) |
| `assets/css/site.css`, `assets/js/site.js` | Styles and effects |
| `index.php` | Front controller: homepage, legacy 301s, 404/410 |
| `home.html`, `*/index.html`, `404.html`, `410.html`, `sitemap.xml`, `robots.txt` | Generated output (committed) |

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

## Going live checklist

1. Register ollieharperstudio.com and point it at Hostinger. Then attach it to website
   `IBqTPWf6a` (`agency-hosting_domains_change-website`, from the temp domain).
2. `python3 build.py && ./deploy.sh` (production build: drops noindex), then clear the cache.
3. Check that `https://ollieharperstudio.com/robots.txt` is ours (the preview domain
   serves Hostinger's own robots.txt), and that `www` and `http` 301 to `https://ollieharperstudio.com`.
4. Create the mailbox `hello@ollieharperstudio.com`, or change `EMAIL` in `build.py`.
5. Add the domain to Google Search Console, submit `sitemap.xml`, and consider
   disavowing the spam anchors ("Buy Backlinks", "PBN Network Service"…).
