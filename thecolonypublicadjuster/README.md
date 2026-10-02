# thecolonypublicadjuster.com: rebuild

A static HTML + PHP rebuild of [thecolonypublicadjuster.com](https://thecolonypublicadjuster.com/) for Hostinger
web hosting. It has no database, CMS or build step on the server. The only PHP is the contact form handler.

**Deliverable:** `thecolonypublicadjuster-site.zip` (full site) and `thecolonypublicadjuster-update-google-tag.zip` (HTML-only update adding the Google Analytics tag G-EVQS4TKQT9).

## Upload to Hostinger

1. In hPanel, open **Websites → Manage → File Manager** and go to `public_html/`.
2. Back up or delete the old site files there.
3. Upload `thecolonypublicadjuster-site.zip`, right-click it, choose **Extract**, and extract into `public_html/`.
   The `index.html`, `.htaccess` and `send-mail.php` files must sit directly in `public_html/`, not in a subfolder.
4. In **Emails**, make sure `info@thecolonypublicadjuster.com` exists, and create `noreply@thecolonypublicadjuster.com`.
   The form sends from `noreply@`. You can change both addresses at the top of `send-mail.php`.
5. Turn on SSL for the domain. `.htaccess` redirects `http://` and `www.` to `https://thecolonypublicadjuster.com`.
6. In Google Search Console, submit `https://thecolonypublicadjuster.com/sitemap.xml`.

## Rebuilding after edits

```sh
python3 build.py      # regenerates dist/ and the zip
python3 validate.py   # keyword counts, broken links, titles, H1s, JSON-LD
```

The generator needs Python 3. Pillow is optional; it reads image sizes and makes `og-image.jpg`.

| Path | What it is |
| --- | --- |
| `build.py` | Layout, header and footer, SEO meta, schema, sitemap and zip |
| `content/pages.py` | Home, about, process, services hub, blog, FAQs, contact, legal, sitemap and 404 |
| `content/services.py` | Copy for the six service pages |
| `content/blog.py` | The five blog posts, using the same URLs as the old site |
| `content/tool_pages.py` | Tools hub and the seven tool pages |
| `static/assets/css/style.css` | All styles, including scroll and reveal effects and responsive rules |
| `static/assets/js/site.js` | Nav, scroll effects, interactive claim guide, blog filter and contact form |
| `static/assets/js/tools.js` | The seven claim tools |
| `static/send-mail.php` | Contact form: CSRF token, honeypot, time trap, per-IP rate limit, PHP `mail()` |
| `static/.htaccess` | HTTPS and non-www redirects, 404 page, caching, compression, security headers |
| `IMAGE-CREDITS.md` | Source and license for every photo (all Unsplash License) |

## SEO

* The primary keyword "The Colony Public Adjuster" appears 15 times in the homepage body and at least once on every other page.
* Each page has its own title and meta description, a canonical URL, Open Graph and Twitter tags, and one H1.
* JSON-LD covers ProfessionalService/LocalBusiness with license and area served, plus WebSite, WebPage,
  BreadcrumbList, Service, FAQPage, BlogPosting and WebApplication on the tool pages.
* The URLs match the old site, so existing rankings and links carry over. Common alternate URLs redirect with a 301.
