# agadecor.com — expired-domain rebuild

A static rebuild of agadecor.com, an expired Chicago wedding and event décor domain
(Wix site, about 2013–2024). It is hand-built HTML/CSS/JS with a small PHP front
controller. Nothing to install: the generator only needs the Python 3 standard library.

**Live preview:** https://snow-mole-583626.hostingersite.com (Hostinger Agency Growth, website UID `DlnCdXsX9`, Boston datacenter)

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Generator: layout, every page's content, schema, route table |
| `blog.py` | Journal posts (3 legacy URLs + 3 new guides) |
| `siteconfig.py` | Brand, email, service area, navigation |
| `validate.py` | Post-build checks (H1s, JSON-LD, titles, links, images, legacy routes) |
| `image-credits.json` | Source and licence of every photo (all CC0) |
| `deploy.sh` | Uploads `public/` through the File Browser TUS API |
| `public/` | **The deploy root**, uploaded to `public_html/` as-is |
| `public/index.php` | Front controller: routing, 301s, 410s, robots, sitemap, inquiry form |
| `public/pages/*.html` | Generated pages (served through `index.php`) |
| `public/routes.php` | Generated route table |

```sh
python3 build.py && python3 validate.py
./deploy.sh        # needs AG_FB_URL / AG_FB_AUTH / AG_FB_REST, see header comment
```

## How the backlinks are handled

Semrush backlink export: 855 links pointing at 6 target URLs.

| Target | Links | Handling |
| --- | --- | --- |
| `/` | 567 | Rebuilt as the homepage |
| `/profile/marilynnwilbur12874145/profile` | 130 | **410 Gone** |
| `/profile/lisawaldschmidt4308271/profile` | 96 | **410 Gone** |
| `/profile/manvradenburg16872462/profile` | 58 | **410 Gone** |
| `/profile/lowelldanielsen19143309/profile` | 3 | **410 Gone** |
| `/profile/christinesha82/profile` | 1 | **410 Gone** |

The `/profile/…` URLs were Wix member profiles. Every link to them is **nofollow**
with page authority 0, all from comment spam on Joomla K2 pages. They pass no link
equity, and redirecting them would tie the homepage to spam. To 301 them to the
homepage anyway, set `PROFILE_MODE = 'home'` in `public/index.php`.

Pages that ranked in Semrush's organic data, and every other page in the old Wix
sitemap, keep their **exact original URL** (no trailing slash, original casing):

`/decor-rental` (flower wall rental chicago), `/single-post/2014/03/01/Modern-Luxury-Bride-Northshore-Magazine`
(northshore magazine), `/single-post/2015/09/27/Give-me-everything-that-sparkles`,
`/single-post/2015/11/15/Trends-of-2016`, `/about-us`, `/services`, `/wedding-planing`
(the original spelling), `/destination-weddings`, `/linens`, `/furniture`, `/vases`,
`/extras`, `/vendors`, `/contact-us`, `/blog`.

Retired old URLs get a 301 to their closest equivalent: `/home`, `/2home`,
`/index.html` → `/`; `/aga-galus` → `/about-us`; `/copy-of-gallery`,
`/photo-gallery.html` → `/gallery`; `/book-online` → `/contact-us`; `/shop-1`,
`/product-page/*`, `/cart-page`, `/backdrops.html` → `/decor-rental`; the 2012
`ceremony/hall/mandaps.html` pages → `/services`; Wix blog archive, tag and feed
URLs → `/blog`; `/account/*` → `/`. Paths with a trailing slash or the wrong case
301 to the canonical path. Wix `?lightbox=` query URLs serve the page, and the
page's canonical tag points to the clean URL.

## Content and brand decisions

- **No impersonation.** The old site belonged to a real business and a named
  person. This rebuild does not use her name, bio, phone number, photos,
  awards, prices or testimonials. The brand is "AGA Décor — Art · Glamour ·
  Ambiance". The footer and privacy page say the domain is independently owned
  and not affiliated with its previous user.
- **Photos** are CC0 stock from Openverse (StockSnap, rawpixel, Wikimedia), stored
  as local WebP files and credited on `/privacy-policy#credits`. The site labels
  them as inspiration imagery, not portfolio work.
- **No invented facts.** The site claims no review counts, years in business,
  awards, street address or phone number. Fill these in `siteconfig.py` and
  `build.py` once they are real.
- The copy is rewritten from scratch. It keeps the old site's structure and
  themes: the Plan · Design · Décor process, rental categories, the gallery
  theme names and the venue list. New guides target the domain's old keywords:
  *wedding flower decoration*, *wedding reception at home decorations* and
  *flower wall rental*.

## Design and effects

Noir, blush and champagne palette. Cormorant Garamond for headings, Manrope for
body text. Effects:

- Falling-petal canvas, Ken Burns hero and pointer-following glow
- Word-by-word headline reveal with a gold shimmer
- Scroll reveals, parallax image bands and 3D tilt on cards
- A scroll-driven Plan → Design → Décor timeline
- An interactive **palette studio**: the reception-table illustration recolours by theme
- A filterable gallery with a lightbox
- A sticky rental-category nav and a back-to-top progress ring

All effects respect `prefers-reduced-motion`.

## Hosting

The platform serves real files directly and sends every other path to
`index.php`, and it ignores `.htaccess`. So the build deliberately has **no
`index.html`**, and pages live in `public/pages/`. `index.php`:

- serves routes from `routes.php`, and handles the 301s and 410s above
- **on any host other than agadecor.com**, sends `X-Robots-Tag: noindex, nofollow`
  and a `Disallow: /` robots.txt, so the temporary domain is not indexed. On
  agadecor.com it forces https and the bare host, and serves the real robots.txt
  and sitemap.xml.
- handles the inquiry form at `POST /contact-us`. Each inquiry is appended to
  `public_html/_leads/leads.php`, which has an exit guard, so it returns 404 over
  HTTP; read it in the File Manager. Set `LEAD_EMAIL` in `index.php` to also get
  each inquiry by email.

## Go-live checklist (when agadecor.com is ready)

1. Point the domain at Hostinger and run `agency-hosting_domains_change-website`
   (website `DlnCdXsX9`, from `snow-mole-583626.hostingersite.com` to `agadecor.com`).
2. Wait for SSL. Check that `https://agadecor.com/robots.txt` shows the sitemap line.
3. Create the `hello@agadecor.com` mailbox, or change `SITE["email"]`, then set `LEAD_EMAIL`.
4. Submit `https://agadecor.com/sitemap.xml` in Google Search Console.
5. Spot-check the legacy URLs above with `curl -I`.
