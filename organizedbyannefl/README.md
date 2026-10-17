# organizedbyannefl.com — rebuild

Static rebuild of the expired domain **organizedbyannefl.com**, a Fort Lauderdale
professional organizing site. The original was a small Wix site (Home, About,
Services, Contact) positioned as "Organizing with a touch of design". This rebuild
keeps that positioning and the original URLs, and adds service pages, a blog and
interactive tools.

**Live (temporary domain):** https://aliceblue-whale-708226.hostingersite.com
— Hostinger Agency Growth website UID `hj0ebIzH3` (php-fpm 8.3, Boston datacenter).

## Rebuilding

```sh
python3 build.py      # regenerate pages/, sitemap.xml, routes.json
python3 validate.py   # one H1, unique titles/descriptions, links, assets, JSON-LD, no phone numbers
```

Needs Python 3 and Pillow (used for image dimensions and the 640px `-sm.webp` variants).

Local preview with the same routing as the host (real files first, else `index.php`):

```sh
php -S 127.0.0.1:8000 router.php   # router: `if (is_file(__DIR__.$path)) return false; require 'index.php';`
```

## Layout

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: maps clean URLs to `pages/*.html`, 301s trailing slashes, uppercase and old Wix paths, real 404s |
| `lib/contact.php` | Contact + tips-signup handler (`POST /contact-submit`): emails `info@organizedbyannefl.com` and appends to `../../oba-submissions/submissions.log` (outside the web root) |
| `pages/` | Generated HTML (deliverable) |
| `assets/` | `css/site.css`, `js/site.js` (nav, effects), `js/tools.js` (tools), `img/` (royalty-free Unsplash photos, WebP) |
| `build.py` | Generator: layout, schema, page builders |
| `content/` | `services.py`, `blog_a.py`, `blog_b.py`, `pages_content.py` (home/about/contact/tools/legal copy), `SPEC.md` (voice + rules) |
| `icons/` | Lucide SVG sources, inlined at build time (not deployed) |
| `deploy.sh` | Uploads the build through the File Browser TUS API (see header comment) |

## URLs

Backlinked/legacy URLs preserved exactly: `/` (1,475 backlinks), `/about` (Apartment
Therapy link), `/services`, `/contact`. The domain's real editorial links come from
Apartment Therapy articles (junk drawers, under-bed storage, homeschool organization,
organizing mistakes, refreshing a space for under $10) and Reader's Digest (when to
replace household items) — the blog covers each of those topics.

- Services: `/services/{home-organizing, closet-organization, kitchen-pantry-organization,
  decluttering-downsizing, move-in-unpacking, home-office-organization,
  laundry-bathroom-organization, virtual-organizing}`
- Blog: `/blog` + 14 posts
- Tools: `/tools/{organizing-time-estimator, declutter-decision-helper,
  30-day-declutter-challenge, closet-rod-calculator}`
- `/service-area`, `/privacy-policy`, `/terms`, `/sitemap.xml`, `/robots.txt`

## Notes before the real domain goes live

- Canonicals, Open Graph URLs and the sitemap already point at `https://organizedbyannefl.com`.
  `index.php` 301s `www.` and `http://` to it once the domain is attached.
- Contact form mail is sent with PHP `mail()` from `info@organizedbyannefl.com`;
  set up that mailbox (and SPF/DKIM) when the domain is connected. Submissions are
  also logged to `oba-submissions/submissions.log` in the site's home directory.
- No phone number is published (the old site's number belonged to the previous owner).
- The About page uses brand voice ("we") with no biography or credentials; add the
  real owner's details if wanted.
