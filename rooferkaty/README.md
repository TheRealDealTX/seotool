# rooferkaty.com — Katy Roofer

A static HTML/PHP site for **Katy Roofer** (phone (512) 297-7580). It is modeled on converseroofer.com's page set and runs on any Hostinger PHP plan.

**Deliverable:** `rooferkaty-hostinger-upload.zip`. Every file sits at the zip root, so it extracts straight into `public_html`.

## Upload to Hostinger
1. Open hPanel, then **Websites → rooferkaty.com → File Manager → public_html**.
2. Delete the placeholder `default.php` or `index.html` if one is there.
3. Upload `rooferkaty-hostinger-upload.zip`, right-click it and choose **Extract** into `public_html`, then delete the zip.
4. Create a mailbox called `no-reply@rooferkaty.com` (hPanel → Emails). The form sends mail as this address.
5. Recommended for reliable delivery: open `includes/config.php` and fill in `smtp_user` / `smtp_pass` with that mailbox's login. Forms then send through Hostinger SMTP instead of PHP `mail()`.
6. Submit a test request on `/contact/` and check the inbox.

The address that receives the forms is set only in `includes/config.php`. It never appears in any HTML or JavaScript. Each submission is also appended to `includes/submissions-log.php` as a backup. That file starts with a PHP `exit`, so it can't be read over the web.

## Pages (37 indexable)
- `/` homepage. Uses "Katy roofer" 14 times in the body, plus "Katy roofing", "roofer in Katy" and "roofers in Katy".
- `/free-roof-inspection/` landing page with the full booking form.
- `/services/` plus 7 service pages: replacement, repair, storm & hail, insurance claim help, metal, commercial, gutters.
- `/areas/` plus 6 area pages: Cinco Ranch, Fulshear, Brookshire, Cypress, Richmond, West Houston.
- `/weather/` live Katy weather: current conditions, NWS alerts, a 7-day forecast and a daily roof-risk rating. Data comes from Open-Meteo and api.weather.gov in the browser, so no API key is needed.
- `/tools/` with 3 tools: roof cost calculator, roof pitch & area calculator, storm damage self-check.
- `/blog/` plus 10 articles dated 3 days apart (2026-09-05 → 2026-10-02).
- `/about/`, `/contact/`, `/privacy-policy/`, `/terms/`, `/thank-you/` (noindex) and `404.html`.

## How it works
- `index.php` serves `home.html` for `/`, adds trailing slashes and returns real 404s. There is deliberately no root `index.html`. This keeps the site working on Hostinger setups that ignore `.htaccess`.
- `.htaccess` (honored on standard shared hosting) forces https, drops `www`, and adds caching and compression.
- Scroll effects live in `assets/js/site.js`: reveal-on-scroll, hero parallax, a reading-progress bar, a shrinking sticky header, animated counters and a scroll-filled process timeline. All of them respect `prefers-reduced-motion`.
- SEO: every page has a unique title and description, a canonical URL, Open Graph tags and JSON-LD (`RoofingContractor` plus Service, FAQPage, BlogPosting, BreadcrumbList and WebApplication), along with `sitemap.xml` and `robots.txt`.

## Editing & rebuilding
Page copy lives in `content/` (blog, services, areas). The format is in `content/FORMAT.md`. Layout and the other pages are in `build.py`, `pages_home.py` and `pages_main.py`. Static files are in `src/`.

```sh
python3 build.py   # writes dist/ and rooferkaty-hostinger-upload.zip
python3 check.py   # links, JSON-LD, H1s, keyword counts, hidden email, blog dates
```
Requires Python 3 and ImageMagick's `identify`, which is used to read image sizes.

## Notes
- Photos are free-license Unsplash stock images. Swap in your own project photos when you have them (`src/assets/img/`, same filenames).
- Cost figures are labeled planning ranges. No street address, license numbers, reviews or years in business were invented. Add real ones to the schema and footer once you have them.
