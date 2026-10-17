# dukoraidea.com — expired-domain rebuild

A static rebuild of dukoraidea.com, a 2020–2021 Shopify store for fairy lights and
smart LEDs. It is now a DIY lighting ideas site: the old product URLs are in-depth
**light guides**, the old blog posts are rewritten and expanded, there are 7 new
posts, and 4 interactive tools. Nothing is sold on the site.

## Rebuilding

```sh
python3 build.py      # writes _pages/*.html, sitemap.xml, robots.txt
python3 validate.py   # h1s, canonicals, titles/descriptions, JSON-LD, links, assets, legacy URLs
php -S localhost:8000 index.php   # local preview with the real routing
```

Standard library only, plus PHP for the router. Content lives in `content/`
(`posts_a.py`, `posts_b.py`, `posts_c.py`, `products.py`; format in `content/SPEC.md`).

## URLs kept from the old site

Taken from the Semrush organic positions export (Sep 2021) and the backlinks export.

| Old URL | Why | Now |
| --- | --- | --- |
| `/` | ~1,710 backlinks | Homepage |
| `/blogs/blog/create-your-mason-jar-fairy-lights-in-5-minutes` | Top traffic page (#2–#10 for "mason jar fairy lights", "fairy lights in a jar") + backlinks | Rewritten, expanded, battery calculator |
| `/products/outdoor-fairy-lights` | Ranked for "fairy lights" (110k), "battery operated fairy lights" | Light guide |
| `/collections/smart-lights/products/wifi-smart-led-strip-lights` | 154 backlinks ("LED strip lights") | 301 → `/products/wifi-smart-led-strip-lights` (Shopify canonical) |
| `/collections/smart-lights/products/smart-led-light-bulbs`, `…/led-controller` | Backlinks | 301 → `/products/…` |
| 8 more `/products/…` | Ranking keywords | Light guides |
| 9 more `/blogs/blog/…` | Ranking keywords | Rewritten posts (slugs unchanged, typos included) |

Most of the ~1,870 backlinks are spam/PBN anchors pointing at the homepage; the real
editorial links (PCBWay, onesmartlighting.net, Painting with a Twist, PEERtrainer…)
target the homepage, the smart-light product URLs and the mason jar post.

## Routing (index.php)

The Hostinger Agency php-fpm platform serves existing files directly and sends
everything else to `index.php`. Pages are rendered to `_pages/<path>.html`, and
`index.php` serves them at clean Shopify-style URLs with no trailing slash. It
also:

- 301s `www.` and plain `http://` to `https://dukoraidea.com`
- 301s trailing-slash and uppercase variants
- 301s legacy Shopify paths: `/collections/*/products/x` → `/products/x`, `/blogs/news`, `/blogs/blog/tagged/*`, `/cart`, `/account`, `/pages/contact-us`, `/policies/*`, Shopify sitemaps, unknown `/products/*` and `/collections/*` → `/collections/all`
- handles the contact form (`POST /contact` → `mail()` to info@dukoraidea.com, honeypot field)
- returns `_pages/404.html` with a real 404 status

`robots.txt` disallows `/_pages/`, and every page has a canonical tag.

## Interactive tools (assets/js/site.js)

Battery-life calculator, LED strip power-supply calculator, color temperature and
mood picker, and patio string-light planner. They are embedded in the relevant posts and
guides via `{{tool:…}}` tokens and collected at `/pages/light-tools`.

## Images

30 royalty-free photos from Pexels (free to use, no attribution required),
converted to WebP in `assets/img/` with `-800` variants for `srcset`.

## Hosting

Hostinger Agency Growth plan, website UID `5Iuo12rhh`, created 2026-10-17 as a plain
php-fpm (PHP 8.3) site with domain dukoraidea.com. Point the domain's DNS at the
website, then confirm SSL is issued.
Deploy with `./deploy.sh` (see its header for the upload credentials).

## Known gaps

- The contact form uses PHP `mail()`. It only delivers once info@dukoraidea.com is a
  real mailbox and the domain has SPF/DKIM set up on Hostinger.
- Battery and power figures in the tools are typical estimates and are labelled as such.
