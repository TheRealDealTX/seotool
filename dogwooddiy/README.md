# dogwooddiy.com — rebuild

A static rebuild of the expired home-renovation and garden blog **Dogwood DIY**
(Jared & Stephanie Tilton, the "Dogwood House", a 1960s brick ranch in North
Carolina). No WordPress, no database. Python 3 standard library only.

```sh
python3 build.py      # writes the site into ./public
python3 validate.py   # links, assets, H1s, titles, JSON-LD, legacy URLs
./deploy.sh           # pushes ./public to Hostinger (see header for credentials)
```

Local preview: `python3 -m http.server -d public 8000` and open `/home.html`
(the homepage is served by `index.php` on the host — see Hosting below).

## Hosting

Hostinger **Agency Growth** plan, order `1008744732`, website UID `cMBtJbc7B`
(plain php-fpm, Boston/US). Domain `dogwooddiy.com` is attached but DNS isn't
pointed yet; preview: https://linen-lion-855038.hostingersite.com

As with the other Agency sites, there is deliberately **no `index.html`**:
`home.html` is the homepage, and `index.php` serves it for `/`, enforces
https + non-www, 301s old WordPress paths (`/feed/`, `/wp-admin`, old category
slugs, missing trailing slashes) and returns `404.html` with a real 404.

`contact.php` emails form submissions to **info@dogwooddiy.com** via PHP
`mail()` (honeypot spam check, redirects back to `/contact/?sent=1|0`). It
will only deliver once the domain's DNS/mailbox is set up.

## What was rebuilt (and why)

Source data: the Semrush organic positions export (Jan 2020) and the backlinks
export. Every URL that had traffic or backlinks is rebuilt at the **same path**:

| URL | Why |
| --- | --- |
| `/` | 1,495 of 1,497 backlinks (realtor.com, laopinion.com, …) |
| `/about/` | backlink ("Dogwood DIY") |
| `/german-schmear-fireplace/` | ~776 visits/mo, "german schmear" 14.8k vol |
| `/remove-overgrown-shrubs-easy/` | ~580 visits/mo, "how to remove bushes" #2 |
| `/replace-old-caulk-bathtub/` | 136 ranking keywords |
| `/simple-wallpaper-removal/`, `/painted-grout-bathroom/`, `/decorating-outdoor-spaces/`, `/beginner-gardening-tips/`, `/simple-diy-boxwood-wreath-you-can-make-in-20-minutes/` | ranking keywords |
| `/category/decor-design/` | ranking keyword |
| `/disclaimer/` | linked from the original posts |

Copy keeps the original authors' story and voice (from the Wayback Machine
snapshots) but is rewritten and expanded around each page's ranking keywords,
with FAQs (FAQPage schema). Old affiliate links were dropped.

**11 new posts** support those pages with internal links: German schmear vs
limewash vs whitewash, best shrubs for the front of a house, how to plant a
dogwood tree, painting kitchen cabinets, peel-and-stick backsplash, modern
farmhouse living room, essential DIY tools, 1960s ranch renovation plan,
budget bathroom makeover, spring yard cleanup checklist, easy houseplants.

**Interactive tools** (`/tools/`, also embedded in related posts;
`assets/js/tools.js`): German schmear mortar calculator with a live canvas
preview, room paint calculator, wallpaper-remover mix calculator, caulk &
grout paint calculator, mulch & soil calculator, and a DIY budget planner
that saves to localStorage.

## Layout

| Path | What |
| --- | --- |
| `build.py` | Layout, page templates, calculators, schema, sitemap |
| `content/site.py` | Site settings, categories, nav |
| `content/posts_legacy.py` | Posts at their original URLs |
| `content/posts_new.py` | New posts (+ extra sections appended at the bottom) |
| `content/pages.py` | About and legal pages |
| `assets/` | CSS, JS, images (WebP, 1600px + 720px) |
| `static/` | `index.php`, `contact.php`, favicons — copied to the web root |

Post bodies support tokens: `[[img:name|alt|caption]]`, `[[tool:key]]`,
`[[tool_link:key]]`, `[[post:slug|anchor]]`. H2s get ids and feed the
sidebar table of contents automatically.

## Design

Palette: forest `#2f4a3a`, sage `#8fa98f`, dogwood blossom `#e8a1b0`, brick
`#b5573b`, cream/paper backgrounds. Fraunces (headings) + Plus Jakarta Sans.
Effects: falling dogwood-petal canvas and Ken Burns parallax on the hero,
scroll reveals, count-up stats, category marquee, card hover zooms, reading
progress bar, active table of contents, project-finder filters. All motion is
disabled under `prefers-reduced-motion`.

Mobile nav: slide-in panel with backdrop; closes on link tap, backdrop tap and
Esc. (The header drops `backdrop-filter` under 960px — with it, the header
becomes the containing block for the fixed panel and the menu breaks.)

Photos are royalty-free (Unsplash and the WordPress.org CC0 photo directory),
downloaded and converted to WebP locally.
