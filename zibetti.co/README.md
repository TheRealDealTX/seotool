# zibetti.co — Zibetti Photo + Film (static rebuild)

Rebuild of the expired domain zibetti.co, a destination wedding & elopement photo + film
studio based in Provo, Utah. Plain HTML/CSS/JS, plus two small PHP files for routing and
the inquiry form. No database, no CMS.

| Path | What it is |
| --- | --- |
| `site/` | The deliverable — upload its contents to `public_html` |
| `site/assets/css/site.css` | Single stylesheet (design tokens, effects, responsive, print) |
| `site/assets/js/site.js` | Header, mobile nav, scroll reveals, parallax, hero slider, gallery, lightbox |
| `site/assets/js/tools.js` | Golden hour calculator, timeline builder, location finder, pricing estimator |
| `site/assets/img/` | Royalty-free Unsplash photos as WebP (`name.webp` 1800px, `name-sm.webp` 900px) |
| `site/index.php` | Front controller: serves `home.html` for `/`, 301s old URLs, real 404s |
| `site/contact.php` | Inquiry form → `mail()` to info@zibetti.co (honeypot spam trap) |
| `build.py` / `posts.py` | Generator: layout, pages, schema; journal posts |
| `validate.py` | Links, assets, one H1, alt text, meta, JSON-LD, sitemap, no old-owner names |
| `deploy.sh` | Uploads `site/` through the Hostinger File Browser TUS API |

```sh
python3 build.py && python3 validate.py      # build + check
cd site && php -S 127.0.0.1:8099 index.php   # local preview (router handles /)
```

## Hosting

Hostinger **Agency Growth** plan, website UID `SnbVxef3f`, domain `zibetti.co`
(preview: https://lightblue-turtle-102447.hostingersite.com). Like the other Agency sites,
the platform serves real files directly, ignores `.htaccess` and routes `/` and unknown paths
to `index.php`, so there is no root `index.html` — the homepage is `home.html`.
Credentials for `deploy.sh` come from `agency-hosting_files_generate-upload-url`.

## Pages & SEO

The old site (2020–2022, per the Wayback Machine) had: home, about-us, video, pricing, blog,
contact-us, faq, plus three client blog posts. Only the homepage had ranking keywords
("zibetti", navigational) and every backlink points at the homepage (Brides.com anchors
"Zibetti & Co" / "ZIBETTI PHOTO AND FILM"), so the brand name "Zibetti Photo + Film" is kept.

Rebuilt at the same URLs: `/`, `/about-us/`, `/video/`, `/pricing/`, `/blog/`, `/contact-us/`, `/faq/`.
Redirects (301): `/home` → `/`, `/YYYY/MM/DD/<post>/` → `/blog/`, plus common aliases.
New: `/portfolio/`, `/tools/` (3 tools + estimator on `/pricing/`), 9 journal posts,
`/privacy-policy/`. Every page has unique title/description, canonical, OG tags and JSON-LD
(ProfessionalService/LocalBusiness, BreadcrumbList, FAQPage, BlogPosting, WebApplication).

## Content notes

- The original owners' names, personal bio and client names are **not** reused. The old
  client posts redirect to `/blog/` instead of being recreated.
- No testimonials/reviews are included — add real ones once you have them.
- Prices, policies (50% retainer, 8–10 week delivery, 300/500 image guarantee, $200/hr
  overtime, $600 second shooter, $2,000 film add-on) are placeholders — review before launch.
- Utah permit/licence info is general guidance and is labelled as such.
- `contact.php` uses PHP `mail()`. Create the info@zibetti.co mailbox and send a test inquiry
  once the domain is connected.
