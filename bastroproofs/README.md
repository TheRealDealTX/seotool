# bastroproofs.com: custom PHP rebuild

This replaces the WordPress/Elementor site for **Bastrop Roofing**, which is
WordPress website UID `uXznqPatC` on the Hostinger Agency Growth plan. The new
site is plain PHP 8 with one stylesheet and one script. It needs no database,
no plugins and no build step. To deploy, upload the contents of this folder to
`public_html/`.

The logo, icons, images, navy and copper palette, and fonts (DM Serif Display
and Manrope) come from the original site. The phone number and email are
unchanged. All of the copy is new.

## Structure

| Path | What it is |
| --- | --- |
| `index.php` | Homepage. It also acts as the front controller for unknown paths: it enforces the canonical host, 301-redirects old WordPress URLs and serves the 404. |
| `includes/config.php` | Business details, navigation and neighborhoods. Every value is defined once here. |
| `includes/functions.php` | Escaping, icons and JSON-LD builders (RoofingContractor, Service, FAQPage, BreadcrumbList, BlogPosting). |
| `includes/components.php` | Layout (`page_start` / `page_end`), hero, FAQ, CTA, estimate form, cards and sidebar. |
| `includes/data/*.php` | Page content for services, areas, blog and tools. |
| `includes/templates/*.php` | Templates for service, area, blog post, tool and legal pages. |
| `includes/tools/*.php` | Markup for the interactive tool widgets. Their logic lives in `assets/js/main.js`. |
| `services/`, `service-areas/`, `blog/`, `roofing-tools/` | One folder per URL. Each holds a 3-line `index.php` that picks a template. |
| `contact/send.php` | Estimate form handler. It uses PHP `mail()` to send to `FORM_RECIPIENT` and has a honeypot. |
| `bin/build-sitemap.php` | Regenerates `sitemap.xml`. Run it after adding pages. |
| `bin/validate.py` | Crawls a running copy and checks titles, descriptions, H1s, canonicals, JSON-LD, links and the homepage keyword count. |

## Pages (38)

- **Home**: targets `bastrop roofing`, `roofing bastrop`, `roofing bastrop tx`, `bastrop roofer` and `bastrop metal roofing`. "Bastrop Roofing" appears 24 times in the body text.
- **10 services**: roof repair, roof replacement, metal roofing (`bastrop metal roofing` / `bastrop metal roofer`), shingle roof replacement, residential, commercial, inspection, storm damage, hail damage and emergency repair. Each one targets a query from the Search Console report.
- **6 service areas**: Elgin, Smithville, Cedar Creek, Paige, McDade and Red Rock.
- **5 interactive tools**: roof replacement cost calculator, metal vs. shingle lifetime cost calculator, roof pitch and area calculator, repair-or-replace quiz, and storm damage checklist.
- **6 blog posts**, plus About, Contact, FAQ, Privacy Policy, Terms of Use, an HTML sitemap and the 404 page.

The old URLs `/privacy-policy/`, `/terms-of-use/` and `/sitemap/` keep the
same paths. `/sitemap_index.xml` and `/page-sitemap.xml` 301-redirect to
`/sitemap.xml`.

## Visual effects

- A weather canvas in the hero. Visitors can switch it between sun, rain, hail and wind, and storms add lightning flashes.
- An animated standing-seam metal roof with rain running down the panels.
- A roof-anatomy builder whose layers drop into place on scroll.
- Shingle-edge hero borders, a roofline footer, scroll reveals, count-up stats, a pulsing service-area map and a "gutter" scroll-progress bar.

All motion is turned off when the visitor has `prefers-reduced-motion` set.

## Local preview and checks

```sh
cd bastroproofs
php -S 127.0.0.1:8099 &
python3 bin/validate.py          # all 38 pages should pass
```

## Deployment

The site is live on Hostinger Agency website UID **`wIZQiliPf`**, a plain
php-fpm website on PHP 8.5. It was created on 2026-10-26, and bastroproofs.com
was moved to it the same day.

The old WordPress site (UID `uXznqPatC`) was **not deleted**. The domain was
unlinked from it, but its files and database are untouched. To roll back,
change `wIZQiliPf`'s domain back to a temporary one and link bastroproofs.com
to `uXznqPatC` again.

To redeploy, run `./deploy.sh`. Its header explains the three upload
credentials it needs. Clear the site cache afterwards.

### Hosting notes

- This platform ignores `.htaccess`. It serves existing files directly and
  sends unknown paths to `index.php`. That is why `index.php` handles the www
  redirect, the old WordPress URLs and the 404s. The `.htaccess` file is still
  kept for portability.
- Because `.htaccess` is ignored, `http://` requests for directory pages are
  served as-is instead of being redirected. Every page carries an `https://`
  canonical tag.
- Template files return a 404 when requested directly. The config and data
  files output nothing.

## Still to do

- **Search Console:** submit `https://bastroproofs.com/sitemap.xml`. The
  verification file `googlecccfbf2f7e9e5ae4.html` was carried over.
- **Email delivery:** send a real test through the estimate form and check that
  it reaches info@bastroproofs.com. `mail()` sends from
  `no-reply@bastroproofs.com`. If messages land in spam, switch to SMTP.
- **Cost figures:** these are planning ranges, and the site labels them that
  way. Review them.
- **Service-area facts:** double-check the drive distances and a few local names
  (Saratoga Farms in Elgin, FM 2104 near Paige, Red Rock on FM 20 / FM 812).
