# Hostinger Installation Guide — PortArthurPublicAdjuster.com

This site is plain **PHP 8.2+ / HTML / CSS / JavaScript** on Apache/LiteSpeed with `.htaccess`.
It needs **no database, no Node.js, no Python, and no API keys**. Everything below is done in
Hostinger's **hPanel**.

Upload file: `dist/portarthurpublicadjuster-public_html.zip`

---

## 1. Back up the current WordPress site

The current site is WordPress. Before replacing it:

1. hPanel → **Websites → Manage → Files → Backups** → create/download a full backup (files + database).
2. Optional: keep a copy of `public_html/wp-content/uploads/` locally. (The new ZIP already contains
   every image file the old site served, at the same URLs.)

## 2. Clear `public_html` and upload the ZIP

1. hPanel → **File Manager** → open `public_html`.
2. Move the old WordPress files into a folder **outside** `public_html` (e.g. `/old-wordpress/`),
   or delete them after your backup is confirmed. WordPress files left in `public_html` would
   conflict with the new `.htaccess` and `index.php`.
3. Upload `portarthurpublicadjuster-public_html.zip` into `public_html`.
4. Right-click the ZIP → **Extract** → extract into `public_html` itself (the ZIP has no wrapper
   folder, so `index.php` lands directly in `public_html`). Delete the ZIP afterwards.
5. Make sure hidden files were extracted: `public_html/.htaccess` and `public_html/.user.ini` must exist
   (File Manager → Settings → show hidden files).

Resulting structure:

```
public_html/
  index.php  .htaccess  .user.ini  robots.txt  favicon.ico  site.webmanifest  apple-touch-icon.png
  api/        claim-review.php, form-token.php, storms.php
  assets/     css/ js/ img/ fonts/ vendor/leaflet/
  content/    pages/ posts/ services/   (all page text — blocked from the web)
  cron/       scheduled PHP scripts       (blocked from the web)
  data/       storm data, caches, logs    (blocked from the web)
  includes/   PHP code + config           (blocked from the web)
  templates/  page layouts                (blocked from the web)
  wp-content/uploads/  original WordPress images (kept so old image URLs still work)
```

## 3. PHP settings

hPanel → **Advanced → PHP Configuration**:

* **PHP version: 8.2 or 8.3** (8.1 also works).
* Extensions (normally on by default): `curl`, `fileinfo`, `json`, `mbstring`, `openssl`, `zlib`.
* `.user.ini` already sets `upload_max_filesize = 10M`, `post_max_size = 32M`, `display_errors = Off`.

Make sure the `data/` folder is writable by PHP (Hostinger's default 755 folders owned by your
user are fine).

## 4. Configure email delivery (SMTP) — required for the forms

All form submissions — the Free Claim Review page, the contact page, the homepage forms, and the
5-second popup — are emailed to **info@portarthurpublicadjuster.com** (set in `includes/config.php`
as `mail_to`). Mail is sent with
PHPMailer over authenticated SMTP from the **info@portarthurpublicadjuster.com** mailbox.

1. hPanel → **Emails** → make sure the mailbox `info@portarthurpublicadjuster.com` exists (create it if
   needed) and note its password. DNS for the domain should use Hostinger's MX/SPF/DKIM records
   (Emails → *DNS settings / Email deliverability* shows green checks).
2. Create the private config file. Recommended location is **one level above** `public_html`:
   * File Manager → go to the folder that *contains* `public_html` (e.g. `/domains/portarthurpublicadjuster.com/`).
   * Create a file named `papa-config.php` with:

   ```php
   <?php
   return [
       'smtp_host'   => 'smtp.hostinger.com',
       'smtp_port'   => 465,
       'smtp_secure' => 'ssl',
       'smtp_user'   => 'info@portarthurpublicadjuster.com',
       'smtp_pass'   => 'THE-MAILBOX-PASSWORD',
       'mail_from'   => 'info@portarthurpublicadjuster.com',
   ];
   ```

   (If you cannot create files above `public_html`, copy `includes/config.local.sample.php` to
   `includes/config.local.php` instead — the `.htaccess` blocks web access to it.)
3. Port 587 with `'smtp_secure' => 'tls'` also works if 465 is blocked.
4. The form will **not** show a success message unless the SMTP server accepts the email. If SMTP is
   not configured, visitors see an error with the phone number and public email instead.

## 5. API credentials

None needed. The site uses free public data sources:

| Data | Source | Key? |
|---|---|---|
| Current conditions, 7-day forecast, alerts | National Weather Service API (api.weather.gov), station KBPT (Jack Brooks Regional Airport) | No (identifies itself with a User-Agent containing info@portarthurpublicadjuster.com, as NWS requests) |
| Active hurricanes / tropical storms | National Hurricane Center CurrentStorms.json (nhc.noaa.gov) | No |
| Radar loop + 7-day tropical outlook images | radar.weather.gov (KLCH) and nhc.noaa.gov, loaded live in the browser | No |
| Recent storm reports | NWS Local Storm Reports (api.weather.gov) + Iowa Environmental Mesonet LSR archive | No |
| Historical storms | NOAA NCEI Storm Events Database (bulk CSV) | No |
| City/ZIP coordinates | U.S. Census Bureau Gazetteer (bundled in `data/places.json`) | No |
| Storm maps | OpenStreetMap tiles via Leaflet (bundled) | No |

## 6. Cron jobs (automatic weather + storm updates)

hPanel → **Advanced → Cron Jobs** → *Create a new cron job* → type **PHP**.
Replace `USERNAME` with your Hostinger username (shown in File Manager paths).

**Option A — one job (recommended):** every 15 minutes (`*/15 * * * *`)

```
/usr/bin/php /home/USERNAME/domains/portarthurpublicadjuster.com/public_html/cron/run-all.php
```

`run-all.php` refreshes weather and the National Hurricane Center feed every run, collects new storm reports hourly, runs maintenance
daily at 3 AM, and updates NOAA storm history Mondays at 4 AM (Central time).

**Option B — separate jobs** (use this if `run-all.php` reports that `passthru` is disabled):

| Schedule | Command (prefix `/usr/bin/php /home/USERNAME/domains/portarthurpublicadjuster.com/public_html/`) |
|---|---|
| `*/15 * * * *` | `cron/refresh-weather.php` |
| `5 * * * *` | `cron/update-weather-events.php` |
| `20 3 * * *` | `cron/maintenance.php` |
| `40 4 * * 1` | `cron/update-storm-history.php` |

Hostinger's panel may show the command field as just the script path after selecting "PHP" —
use the full path in that case. Logs are written to `data/logs/` (cron.log, events.log,
history.log, mail.log, http.log, php-errors.log) and can be viewed in File Manager.

Optional one-time commands (hPanel → Advanced → **SSH Access**, or a temporary cron entry):

```
php cron/update-weather-events.php --days=1100   # backfill ~3 years of storm reports (already included)
php cron/update-storm-history.php --full          # rebuild all NOAA years 1950–present (already included; slow)
```

The ZIP already includes current data (Jefferson County NOAA history 1955–2026 through the September 2026
NCEI release, and NWS storm reports through October 19, 2026), so the site works before cron runs. If an external
service is down, pages keep showing the last good data with its timestamp, or a fallback message.

## 7. Database

None. All content lives in PHP files under `content/`; storm data and caches are JSON files in `data/`.

## 8. HTTPS

1. hPanel → **Security → SSL** → install/activate the free SSL certificate for
   `portarthurpublicadjuster.com` and `www.portarthurpublicadjuster.com`.
2. The `.htaccess` already forces `https://portarthurpublicadjuster.com` (no www) with 301 redirects.
3. After confirming HTTPS works everywhere, you may enable HSTS by un-commenting the
   `Strict-Transport-Security` line in `.htaccess`.
4. If Hostinger's CDN or LiteSpeed Cache is enabled, purge it after uploading.

## 9. Test the forms

1. Open https://portarthurpublicadjuster.com/free-claim-review/ and submit a test request (attach a photo).
2. You should see: *"Thank you! Your Free Claim Review request has been received. Our team will contact you."*
3. Confirm the email arrives at info@portarthurpublicadjuster.com (check spam the first time; mark as "not spam").
   Reply-To is set to the visitor's email so you can reply directly.
4. If it fails, read `data/logs/mail.log` for the SMTP error (wrong password, port blocked, etc.).
5. Limits: 5 submissions per hour per visitor, 3 files × 8 MB (JPG, PNG, WEBP, HEIC, PDF).

## 10. Verify existing URLs (all must return 200)

Every URL from the old WordPress site is kept:

```
/  /about-us/  /services/  /blog/  /contact/  /privacy-policy/  /terms-of-use/
/are-insurance-adjusters-honest/  /category/general/
/wp-content/uploads/2026/02/...   (all 26 original image files)
```

And these redirect (301): `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml` → `/sitemap.xml`,
`/comments/feed/` → `/feed/`, `/?p=251` → `/are-insurance-adjusters-honest/`, `http://` and `www.` → `https://portarthurpublicadjuster.com`.
`/wp-admin/` and `/wp-login.php` return 410 Gone.

## 11. Verify weather integrations

* https://portarthurpublicadjuster.com/weather/ — current conditions show "Observed … at Jack Brooks Regional
  Airport (KBPT)" with a recent time; 7 forecast cards; alerts box; KLCH radar loop.
* https://portarthurpublicadjuster.com/hurricane-tracker/ — season status, active storms from the National
  Hurricane Center with distance from Port Arthur, the storm map, and tropical alerts.
* https://portarthurpublicadjuster.com/weather-events/ — "Last updated" timestamp advances hourly once cron runs.
* https://portarthurpublicadjuster.com/storm-history/ and /storm-lookup/ — filters return results;
  e.g. ZIP 77640 with date 12/28/2024 shows a hail report.

## 12. Launch checklist

1. Google Search Console: submit `https://portarthurpublicadjuster.com/sitemap.xml` (the old Yoast
   sitemap URLs now redirect there). Use URL Inspection on the homepage and a few articles.
2. Verify the **TDI license #3356839** on the TDI license lookup before launch
   (https://www.tdi.texas.gov/agent/agent-lookup.html). The number appears in
   `includes/config.php` (`license`) — change it there if needed and it updates site-wide.
3. Google Analytics (G-L7RSXW5PY8) is hard-coded in `templates/head.php`; leave `analytics_id` in `includes/config.php`, and update the
   Privacy Policy (`content/pages/privacy-policy.php`) to mention it.
4. Delete the old WordPress backup folder from the server once you're satisfied.

## Editing content later

* Articles: `content/posts/<slug>.php` → URL `/<slug>/`. Start from `content/posts/_NEW-POST-TEMPLATE.txt`.
* Service pages: `content/services/<slug>.php` → `/services/<slug>/`.
* Pages: `content/pages/<name>.php` (`author__joseph-dittman.php` → `/author/joseph-dittman/`).
* Phone, email, license, SMTP recipient: `includes/config.php`.
* Navigation and footer links: `includes/functions.php` (`primary_nav()`, `footer_nav()`).
* The sitemap, RSS feed, blog list, related posts, and schema update automatically.

## Deployment record (October 20, 2026)

The site is live on a separate Agency Plan **php-fpm** website (UID `UwXzNYPkl`, PHP 8.3), and
`portarthurpublicadjuster.com` was moved to it. The old WordPress website (UID `fF4aIqfKr`) was **not deleted**;
it only lost the domain, so it can be restored by linking the domain back.

Platform notes (they differ from classic shared hosting):

* **`.htaccess` is ignored.** The platform serves existing files directly and sends everything else to
  `index.php`. HTTPS and `www` → apex redirects are therefore done in `index.php`. PHP files in private
  folders execute and print nothing, so no code is exposed.
* **Private runtime files** (logs, caches, rate-limit files, the form secret) go to a randomly named folder
  inside `data/` (its name is stored in `data/private-dir.php`), because PHP cannot write above `public_html`.
* **`passthru()` is disabled**, so the four cron scripts run as separate jobs (times are UTC):
  `*/15 * * * *` refresh-weather.php · `5 * * * *` update-weather-events.php ·
  `20 8 * * *` maintenance.php · `40 9 * * 1` update-storm-history.php
  (each as `/usr/bin/php /home/u914589053/websites/UwXzNYPkl/public_html/cron/<script>`).
* **Email:** forms currently send with PHP `mail()` (`allow_mail_fallback`). The live test reached
  info@portarthurpublicadjuster.com but landed in **Junk**. For reliable inbox delivery, create the SMTP
  override (section 4) with the mailbox password. On this platform, use `includes/config.local.php`
  (PHP cannot read files above `public_html`).
