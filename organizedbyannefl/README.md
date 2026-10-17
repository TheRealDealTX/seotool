# organizedbyannefl.com — rebuild

Static rebuild of the expired domain **organizedbyannefl.com**, a Fort Lauderdale
professional organizing site. The original was a small Wix site (Home, About,
Services, Contact) positioned as "Organizing with a touch of design". This rebuild
keeps that positioning and the original URLs, and adds service pages, a blog and
interactive tools.

**Live:** https://organizedbyannefl.com — Hostinger Agency Growth website UID `hj0ebIzH3`
(php-fpm 8.3, Boston datacenter). The hostingersite.com preview domain is sent an
`X-Robots-Tag: noindex` header by `index.php` so only the real domain gets indexed.

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

## SEO setup

- Google tag `G-8097R535LY` in the `<head>` of every page (`GTAG` in `build.py`).
- Google Search Console file verification: `googlecccfbf2f7e9e5ae4.html` at the root.
- `sitemap.xml` with image entries (also in `robots.txt`); unique titles (<= 60 chars,
  brand suffix only when it fits), descriptions, canonicals, Open Graph/Twitter cards with
  1200x630 JPEG share images (`assets/og/`, generated), JSON-LD (`ProfessionalService`,
  `WebSite`, `BreadcrumbList`, `Service`, `BlogPosting`, `FAQPage`, `WebApplication`).
- Favicons: `favicon.ico` (48/32/16), `favicon.svg`, `favicon-96x96.png`,
  `apple-touch-icon.png`, `site.webmanifest` + 192/512 and maskable icons.
- `index.php` 301s `www.`, `http://`, trailing slashes, uppercase and old Wix paths.
- `validate.py` enforces all of the above.

## Notes
- Contact form mail is sent with PHP `mail()` from `info@organizedbyannefl.com`;
  set up that mailbox (and SPF/DKIM) when the domain is connected. Submissions are
  also logged to `oba-submissions/submissions.log` in the site's home directory.
- No phone number is published (the old site's number belonged to the previous owner).
- The About page uses brand voice ("we") with no biography or credentials; add the
  real owner's details if wanted.
