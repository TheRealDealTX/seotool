# asmith.photography — rebuild

A static rebuild of the expired domain **asmith.photography** as an independent
Los Angeles photography journal (skate, footwear, editorial, sport, brand
campaigns, personal work). Every URL the old site ranked for or had backlinks
to is rebuilt at the same path.

**Live (temporary domain):** https://purple-baboon-917875.hostingersite.com
— Hostinger Agency Growth website UID `xpKP4rrWT` (php-fpm, Phoenix DC).

## Why a journal and not a portfolio

The old domain was the portfolio of a working photographer. Rebuilding it as
*his* portfolio would mean impersonating a real person and claiming client
work (Nike SB, Vans, Stacy Adams …) we did not shoot. Instead each old URL is
now an article about **how that kind of shoot is made**: same topic, same
keyword, honest framing. The `/about` page says the site is independent
and not affiliated with any photographer, brand or publication it names.
The article copy never claims to have shot the named brands or people and
never mentions the previous owner.

## URL inventory

Sources: `asmith.photography-organic.Positions-us-20170315` (Semrush, 49 URLs)
and `asmith.photography-backlinks.csv` (577 links, 11 target URLs) — 55
distinct paths after merging.

| Old URL | Now |
| --- | --- |
| `/` (417 traffic; "aaron smith", "asmith photography") | Homepage |
| `/nike-sb` (42 traffic, #1 "nike sb photography") | Article |
| `/johnny-layton-for-vans` (13 traffic, #2 "vans photographer") | Article |
| `/stacy-adams-shoes` (2 traffic) | Article |
| 44 more ranked / linked pages (`/skateboarding`, `/ucla-water-polo`, `/people`, `/contact`, `/stacy-adams-spring-2018`, `/womens-march-los-angeles` …) | Article (or the contact page) at the same path |
| `/fila-spring-2017-new` | 301 → `/fila-spring-2017` |
| `/etnia-barcelona-vintage-campaign-2016` | 301 → `/etnia-barcelona-vintage-collection-campaign` |
| `/leica-sofort-campaign-3` | 301 → `/leica-sofort-campaign-2` |
| `/m/disney-mix` | 301 → `/disney-interactive` |
| `/m//day-in-the-life-kelly-vittengl/…html` | 301 → `/people` |

Also handled: trailing slashes and upper-case variants 301 to the canonical
slug, `/m/<slug>` 301s to `/<slug>`, query strings (`?ref=…`) are ignored.
New pages: `/journal` (filterable index), `/about`, `/credits`.
The full list is `content/plan.json`; `validate.py` checks every entry routes.

## Layout

| Path | What |
| --- | --- |
| `build.py` | Generator: layout, home, articles, journal, about, contact, credits, `index.php`, sitemap |
| `content/plan.json` | Slug → category, focus keyword, angle; legacy redirects |
| `content/pages/*.json` | Article copy (title, description, h1, dek, sections, notes, pull quote, related) |
| `content/BRIEF.md` | The writing rules the copy follows |
| `content/credits.json` | Licence + attribution for every image |
| `fetch_images.py` | Pulls CC0 / CC BY / public-domain photos from Openverse (StockSnap first) |
| `content/image-picks.json`, `image-blocklist.txt` | Hand-picked overrides / rejected images |
| `contact_sheet.py` | Labelled contact sheets for reviewing the picked images |
| `src/` | `site.css`, `site.js`, favicon |
| `public/` | Build output — this is what gets deployed |
| `validate.py` | Post-build checks |
| `deploy.sh` | Uploads `public/` to Hostinger |

```sh
python3 build.py && python3 validate.py
php -S 127.0.0.1:8080 -t public dev_router.php   # local preview with the real routing
```

## Design

Dark, cinematic film aesthetic: Instrument Serif / Inter Tight / JetBrains
Mono, safelight orange and film-gold accents. Effects: aperture-iris intro
(once per session), Ken Burns hero with animated light leak and a camera
viewfinder HUD (roaming focus box, frame counter), animated film grain,
film-strip marquee, letter-by-letter headline reveal, scroll-lit statement,
"darkroom develop" image reveals, black-and-white → colour cards with 3D tilt,
custom cursor, reading-progress bar and live table of contents on articles,
journal filter + search, and an interactive **exposure lab** (aperture /
shutter / ISO sliders that change the frame and a light meter). Everything
respects `prefers-reduced-motion`.

## Hosting notes

The platform serves real files directly, ignores `.htaccess`, and sends
unknown paths to `index.php`. There is deliberately **no `index.html`** at the
root. `index.php` serves `home.html` for `/`, maps each slug to
`pages/<slug>.html`, does the legacy 301s, returns a real 404, and stores
contact-form posts in `../asmith-messages/messages.jsonl` (outside the web
root) and emails them to info@asmith.photography via PHP `mail()`. On `asmith.photography` it forces https + non-www; on any other host
it sends `X-Robots-Tag: noindex` (Hostinger's temp domain also serves its own
robots.txt blocking Googlebot).

## Going live on asmith.photography

1. Point the domain at Hostinger and swap it onto website `xpKP4rrWT`
   (`agency-hosting_domains_change-website`, from
   `purple-baboon-917875.hostingersite.com` to `asmith.photography`), then
   wait for SSL.
2. Clear the cache. Canonicals, sitemap and JSON-LD already use
   `https://asmith.photography`.
3. Submit `https://asmith.photography/sitemap.xml` in Search Console.

## Deploying

`./deploy.sh` (see its header for the three upload credentials from
`agency-hosting_files_generate-upload-url`), then clear the website cache.
