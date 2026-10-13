# txpublicadjusting.com rebuild

A custom PHP site (no WordPress, no database) that replaces the WordPress/Elementor
site demoted by Google's June 2026 spam update. It's built around the audit's
findings: no doorway pages, consolidated content, a visible licensed expert, and
genuinely useful tools.

- **Preview:** https://lightcoral-ibex-664819.hostingersite.com (Hostinger Agency website `cR6CoQmvm`)
- The preview is automatically `noindex`. Any host that isn't `txpublicadjusting.com`
  gets an `X-Robots-Tag: noindex` header, a `noindex` meta tag and a disallow-all
  robots.txt. When the site is served on the real domain, it becomes indexable with no
  code changes.

## What's in it (72 URLs)

| Section | URLs | Notes |
| --- | --- | --- |
| Core | `/`, `/about-us/`, `/contact-us/`, `/privacy-policy/`, `/terms-of-use/` | Home has a quick-review form and a live "Texas storm watch" section (NWS forecast by city or location, active Texas alerts, last-24-hour storm reports); About is Joseph Dittman's author page (Person schema with TDI license credential) |
| Services | `/services/` + 5 | Roof & hail, water, fire & smoke, hurricane & wind, denied & underpaid |
| Commercial | `/commercial-claims/` + 10 | Down from 45 templated pages; the others 301 to the closest page or the hub |
| Service areas | `/areas/` + 16 metro pages | Down from 411 city pages; the other ~395 301 to the nearest kept metro (matched by distance) |
| Guides | `/blog/` + 25 posts under `/post/` | 62 posts consolidated; merged URLs 301 to their new home |
| Tools | `/tools/` + 6 | Settlement calculator, Chapter 542 deadline calculator (with .ics export), documentation checklist, contents inventory (CSV export), live NWS storm report lookup, "Do I need a public adjuster?" quiz |

Old URLs are handled in `site/app/redirects.php`: 500 301 redirects and 4 permanent 410s
(the off-topic cigarette and smoke-smell posts, plus an off-topic roofing post). Old
WordPress paths (`/wp-content/…`, `/wp-admin/`, feeds, category and author archives) are
also handled in `site/app/router.php`.

## Layout

```
site/                  → this folder is public_html
  index.php            front controller (every non-file request)
  app/                 config.php (the only file you normally edit), router, views, schema, redirects
  content/             page copy as PHP arrays: pages/, services/, commercial/, areas/, posts/, tools/
  assets/              css/site.css, js/site.js, js/tools/*.js, img/, data/tx-places.json
  storage/             form leads CSV + form secret (created on the server, never committed)
CONTENT_GUIDE.md       writing rules, verified Texas law facts, file format; read it before adding pages
validate.py            crawler: links, titles, descriptions, H1s, JSON-LD, sitemap coverage
deploy.sh              uploads site/ through Hostinger's File Browser (TUS)
```

To add a blog post, drop a new file in `site/content/posts/` (copy an existing one),
add a 1200×800 image as `assets/img/blog/{slug}.webp` and a 600×400 copy as
`{slug}-600.webp`. It appears in the blog, the sitemap and related links
automatically. The same pattern works for areas, services and commercial pages.

## Local preview and checks

```sh
php -S 127.0.0.1:8088 -t site site/index.php
python3 validate.py http://127.0.0.1:8088      # must print OK
```

## Deploy

```sh
# credentials from the Hostinger API: agency-hosting_files_generate-upload-url (website_uid cR6CoQmvm)
export TX_FB_URL=… TX_FB_AUTH=… TX_FB_REST=…
./deploy.sh                 # everything
./deploy.sh app/config.php  # or specific files
```

Hosting notes (Hostinger Agency, plain PHP): the platform ignores `.htaccess`,
serves real files directly and sends every other path to `index.php`. So
HTTPS, `www` and all redirects are enforced in PHP. Don't add an `index.html`. Files
under `app/` and `content/` are PHP that print nothing if requested directly. The
folder above `public_html` isn't writable, so leads are stored in
`storage/leads-<random>.csv`, a name derived from a server-side secret that can't be
guessed. Download them from the Hostinger File Manager.

## Go live on txpublicadjusting.com

1. **Lead email.** Form submissions are emailed to `info@txpublicadjusting.com`
   (`$LEAD_EMAIL` in `app/config.php`) and always logged to the leads CSV, which
   has an `emailed` column showing whether the server accepted each send. After the
   domain moves, make sure its SPF record allows Hostinger's mail servers, or the
   emails may go to spam.
2. **Search Console.** If the domain property is verified by DNS, nothing changes. If
   the old site was verified through Site Kit or an HTML tag, put the code in
   `GOOGLE_SITE_VERIFICATION` in `app/config.php`. Optionally set `GA4_ID`.
3. **Switch the domain.** Point txpublicadjusting.com at this website: change its
   domain from the temporary one with the Hostinger API call
   `agency-hosting_domains_change-website`, or in hPanel. Then update DNS at the
   registrar if the domain isn't already on Hostinger. SSL is issued automatically.
4. **After DNS switches:**
   - Check that `https://txpublicadjusting.com/robots.txt` shows the sitemap line.
   - Check that a few old URLs redirect, for example
     `/areas/public-insurance-adjuster-katy/` and `/post/public-adjuster-for-roof-claim/`.
   - Run `python3 validate.py https://txpublicadjusting.com`.
5. **In Search Console:**
   - Submit `https://txpublicadjusting.com/sitemap.xml` and remove the old sitemaps.
   - Use URL Inspection to request indexing of the home page, the services and the top guides.
   - Watch Pages → "Not found (404)" and "Redirect" for a few weeks.
6. **Don't** recreate the deleted city pages or publish in bursts. Add pages slowly, with
   real local proof: fill `case_notes` on the area pages, and add new guides one or two a
   week.
