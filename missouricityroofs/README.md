# missouricityroofs.com — Missouri City Roofers

A static HTML/PHP site for **Missouri City Roofers** (phone (512) 297-7580, email info@missouricityroofs.com). It has the same feature set as rooferkaty.com, rebuilt with its own design: forest green and brass colors, Fraunces and Manrope type, a split hero with a horizontal quote bar, numbered service rows and an interactive roof calendar.

## Hosting
- Hostinger **Agency Growth** plan (order 1008744732), website UID **`72jZRj3qX`**, php-fpm, PHP 8.5, Phoenix datacenter.
- Preview URL until DNS is connected: https://maroon-cod-118551.hostingersite.com
- `missouricityroofs.com` is already attached to the website. To go live, point the domain's nameservers or A record at Hostinger (A `72.60.128.114`). SSL is issued automatically once DNS resolves.
- Deploy: `python3 build.py && python3 check.py && ./deploy.sh`. The header of `deploy.sh` explains the upload credentials. Clear the site cache afterwards.

## Forms
- Every form posts to `/send.php`: the hero quote bar, the 4-second popup, the inspection, contact, service and area forms.
- The recipient and sender are both `info@missouricityroofs.com`, set in `src/includes/config.php`.
- **Create that mailbox in hPanel → Emails**, otherwise PHP `mail()` has no valid sender.
- For the most reliable delivery, also put the mailbox password into `smtp_user` / `smtp_pass` in the deployed `includes/config.php`.
- Every submission is also logged to `includes/submissions-log.php`. That file is not readable from the web.
- The popup opens 4 seconds after page load, once per browser session. It doesn't open on the free-inspection, contact, thank-you or 404 pages, and it waits if the visitor is already typing in a form.

## Pages (37 indexable)
- `/` homepage: "Missouri City roofers" appears 15 times in the body, plus in the title and meta description. The title includes the phone number.
- `/free-roof-inspection/`
- `/services/` plus 7 service pages.
- `/areas/` plus 6 area pages: Sienna, Sugar Land, Stafford, Pearland, Fresno and Richmond.
- `/weather/` "Storm Watch": live Open-Meteo conditions, NWS alerts, a 7-day forecast and a daily roof-risk rating.
- The homepage also shows a live weather chip, a 3-day panel and a month-by-month roof calendar.
- `/tools/` plus the roof cost calculator, the roof pitch & area calculator and the storm damage self-check. The homepage also has a quick estimator.
- `/blog/` plus 10 posts dated 3 days apart (2026-09-20 → 2026-10-17).
- `/about/`, `/contact/`, `/privacy-policy/`, `/terms/`, `/thank-you/` (noindex) and `404.html`.

## Editing
- Copy lives in `content/` (format in `content/FORMAT.md`).
- Layout is in `build.py`, `pages_home.py` and `pages_main.py`.
- Static files are in `src/`.
- `check.py` validates links, JSON-LD, H1s, the keyword count, the title/phone, the form recipient, the popup and the blog dates. It also flags any leftover Katy text.

## Photos
- Images come from Unsplash and US public-domain sources: FEMA photos and CC0 files on Wikimedia Commons.
- None of them repeat rooferkaty.com's photos.
- Swap in real project photos when you have them, keeping the same filenames in `src/assets/img/`.

## SEO setup
- Google tag `G-K3YRCSMJKS` is the first thing in `<head>` on every page (`GTAG` in `build.py`).
- Search Console verification file: `src/googlecccfbf2f7e9e5ae4.html`, served at the site root.
- `sitemap.xml` lists all 37 indexable pages, with lastmod dates and each page's main image. `robots.txt` points to it.
- Each page has:
  - a unique title (62 characters or fewer) and meta description (120–160 characters)
  - a canonical URL
  - Open Graph and Twitter tags, including the image size
  - one H1
  - JSON-LD
- Favicon set: `favicon.svg`, `favicon.ico`, a 96px PNG, an Apple touch icon and the PWA manifest icons.
- Images are WebP at 1400px or smaller. The build also writes 800px copies for phones, served through `srcset`. The homepage hero image is preloaded.
- The `*.hostingersite.com` preview domain serves Hostinger's own robots.txt, which blocks Google there. The real domain serves this site's own robots.txt.

## Not included
- No street address, license numbers, reviews or years in business were invented.
