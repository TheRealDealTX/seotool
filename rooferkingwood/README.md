# rooferkingwood.com — Kingwood Roofers

A static HTML/PHP site for **Kingwood Roofers** (phone (512) 297-7580), built on the same page set as rooferkaty.com but with its own design: maroon + pine green, Fraunces serif headings, two-tier header, arched hero, editorial service index, "storm desk" weather band and a lead popup.

**Hosting:** Hostinger Agency Growth plan, website UID `jhGHXYw37` (php-fpm, PHP 8.5, Phoenix).
Preview URL until DNS is connected: https://mediumslateblue-gazelle-304055.hostingersite.com/

**Deliverable:** `rooferkingwood-hostinger-upload.zip` (files at the zip root → extract into `public_html`), or push with `./deploy.sh`.

## Forms & email
- Every form (hero quick bar, popup, inspection page, contact, service/area pages) posts to `/send.php`.
- Recipient: `info@rooferkingwood.com`, set only in `includes/config.php` (PHP, never sent to browsers). The notification is sent **from** the same address.
- Create the `info@rooferkingwood.com` mailbox in hPanel → Emails once the domain is connected. For reliable delivery fill in `smtp_user` / `smtp_pass` in `includes/config.php` with that mailbox's login (then mail goes through Hostinger SMTP instead of PHP `mail()`).
- Every submission is also appended to `includes/submissions-log.php` (starts with a PHP `exit`, so it isn't web-readable). Leads are never lost even before the mailbox exists.
- Spam protection: honeypot field + minimum fill time.

## Lead popup
Opens 4 seconds after page load, once per browser session (sessionStorage), on every page except `/thank-you/`. It waits if the visitor is typing in another form, closes with ×, backdrop or Esc, and doesn't reappear after a submission.

## Pages (39 indexable)
- `/` homepage — "Kingwood roofers" used 19× in the body (check.py enforces ≥14); phone in the SEO title.
- `/free-roof-inspection/` landing page with the full booking form.
- `/services/` + 8 services: replacement, repair, storm & hail, tree & limb damage, insurance claim help, metal, commercial, gutters.
- `/areas/` + 6 areas: Atascocita, Humble, Porter, New Caney, Huffman, Crosby (plus the Kingwood village list).
- `/weather/` Kingwood storm desk: NWS alerts, current conditions, 24-hour gust/rain chart, 7-day forecast with roof-risk rating (Open-Meteo + api.weather.gov, no key). The homepage and contact page carry live mini versions.
- `/tools/` + 4 tools: roof cost calculator, pitch & area calculator, storm damage self-check, roof age & lifespan estimator. The homepage has a tabbed quick estimator.
- `/blog/` + 10 articles, 3 days apart (2026-09-21 → 2026-10-18).
- `/about/`, `/contact/`, `/privacy-policy/`, `/terms/`, `/thank-you/` (noindex), `404.html`.

## Build
```sh
python3 build.py   # dist/ + rooferkingwood-hostinger-upload.zip
python3 check.py   # links, assets, JSON-LD, H1s, keyword count, popup, recipient, blog dates
```
Needs Python 3 and ImageMagick `identify`. Copy lives in `content/` (format: `content/FORMAT.md`); layout in `build.py`, `pages_home.py`, `pages_main.py`; static files in `src/`.

## Notes
- `index.php` serves `home.html` for `/`, adds trailing slashes, returns real 404s, and only forces https / non-www on rooferkingwood.com itself so the preview domain keeps working.
- Photos are CC0 / public-domain images (sources in `src/assets/img/CREDITS.md`). Swap in your own project photos with the same filenames.
- No Google Analytics tag yet (rooferkaty has one); send a GA4 ID to add it.
- No street address, license numbers, reviews or years in business were invented.
