# Hostinger Installation Guide — McAllenPublicAdjuster.com

This site is plain **PHP 8.2+ / HTML / CSS / JavaScript** on Apache/LiteSpeed with `.htaccess`.
It needs **no database, no Node.js, no Python, and no API keys**. Everything below is done in
Hostinger's **hPanel**.

Upload file: `dist/mcallenpublicadjuster-public_html.zip`

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
3. Upload `mcallenpublicadjuster-public_html.zip` into `public_html`.
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

All Free Claim Review submissions are emailed to **jditt@risepublicadjusting.com** (set in
`includes/config.php` as `mail_to`; it is never displayed on the site). Mail is sent with
PHPMailer over authenticated SMTP from the **info@mcallenpublicadjuster.com** mailbox.

1. hPanel → **Emails** → make sure the mailbox `info@mcallenpublicadjuster.com` exists (create it if
   needed) and note its password. DNS for the domain should use Hostinger's MX/SPF/DKIM records
   (Emails → *DNS settings / Email deliverability* shows green checks).
2. Create the private config file. Recommended location is **one level above** `public_html`:
   * File Manager → go to the folder that *contains* `public_html` (e.g. `/domains/mcallenpublicadjuster.com/`).
   * Create a file named `mpa-config.php` with:

   ```php
   <?php
   return [
       'smtp_host'   => 'smtp.hostinger.com',
       'smtp_port'   => 465,
       'smtp_secure' => 'ssl',
       'smtp_user'   => 'info@mcallenpublicadjuster.com',
       'smtp_pass'   => 'THE-MAILBOX-PASSWORD',
       'mail_from'   => 'info@mcallenpublicadjuster.com',
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
| Current conditions, 7-day forecast, alerts | National Weather Service API (api.weather.gov), station KMFE | No (identifies itself with a User-Agent containing info@mcallenpublicadjuster.com, as NWS requests) |
| Recent storm reports | NWS Local Storm Reports (api.weather.gov) + Iowa Environmental Mesonet LSR archive | No |
| Historical storms | NOAA NCEI Storm Events Database (bulk CSV) | No |
| City/ZIP coordinates | U.S. Census Bureau Gazetteer (bundled in `data/places.json`) | No |
| Storm maps | OpenStreetMap tiles via Leaflet (bundled) | No |

## 6. Cron jobs (automatic weather + storm updates)

hPanel → **Advanced → Cron Jobs** → *Create a new cron job* → type **PHP**.
Replace `USERNAME` with your Hostinger username (shown in File Manager paths).

**Option A — one job (recommended):** every 15 minutes (`*/15 * * * *`)

```
/usr/bin/php /home/USERNAME/domains/mcallenpublicadjuster.com/public_html/cron/run-all.php
```

`run-all.php` refreshes weather every run, collects new storm reports hourly, runs maintenance
daily at 3 AM, and updates NOAA storm history Mondays at 4 AM (Central time).

**Option B — separate jobs** (use this if `run-all.php` reports that `passthru` is disabled):

| Schedule | Command (prefix `/usr/bin/php /home/USERNAME/domains/mcallenpublicadjuster.com/public_html/`) |
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

The ZIP already includes current data (NOAA history through the September 2026 NCEI release and
storm reports through October 3, 2026), so the site works before cron runs. If an external
service is down, pages keep showing the last good data with its timestamp, or a fallback message.

## 7. Database

None. All content lives in PHP files under `content/`; storm data and caches are JSON files in `data/`.

## 8. HTTPS

1. hPanel → **Security → SSL** → install/activate the free SSL certificate for
   `mcallenpublicadjuster.com` and `www.mcallenpublicadjuster.com`.
2. The `.htaccess` already forces `https://mcallenpublicadjuster.com` (no www) with 301 redirects.
3. After confirming HTTPS works everywhere, you may enable HSTS by un-commenting the
   `Strict-Transport-Security` line in `.htaccess`.
4. If Hostinger's CDN or LiteSpeed Cache is enabled, purge it after uploading.

## 9. Test the forms

1. Open https://mcallenpublicadjuster.com/free-claim-review/ and submit a test request (attach a photo).
2. You should see: *"Thank you! Your Free Claim Review request has been received. Our team will contact you."*
3. Confirm the email arrives at jditt@risepublicadjusting.com (check spam the first time; mark as "not spam").
   Reply-To is set to the visitor's email so you can reply directly.
4. If it fails, read `data/logs/mail.log` for the SMTP error (wrong password, port blocked, etc.).
5. Limits: 5 submissions per hour per visitor, 3 files × 8 MB (JPG, PNG, WEBP, HEIC, PDF).

## 10. Verify existing URLs (all must return 200)

```
/  /about-us/  /services/  /blog/  /contact/  /privacy-policy/  /terms-of-use/
/public-adjuster-vs-insurance-adjuster-for-hail-claims/
/hail-damage-claim-supplements/
/what-to-do-if-your-hail-claim-was-denied-in-mcallen/
/document-hail-damage-for-an-insurance-claim/
/roof-hail-damage-insurance-claim-mcallen/
/fire-insurance-adjuster/
/claim-changes-knowing-when-to-hire-a-public-adjuster/
/fire-insurance-public-adjuster/
```

And these redirect (301): `/category/general/` → `/blog/`, `/sitemap_index.xml` → `/sitemap.xml`,
`/?p=243` → `/fire-insurance-adjuster/`, `http://` and `www.` → `https://mcallenpublicadjuster.com`.
`/wp-admin/` and `/wp-login.php` return 410 Gone.

## 11. Verify weather integrations

* https://mcallenpublicadjuster.com/weather/ — current conditions show "Observed … at McAllen-Miller
  International Airport (KMFE)" with a recent time; 7 forecast cards; alerts box.
* https://mcallenpublicadjuster.com/weather-events/ — "Last updated" timestamp advances hourly once cron runs.
* https://mcallenpublicadjuster.com/storm-history/ and /storm-lookup/ — filters return results;
  e.g. ZIP 78504 with date 05/08/2025 shows hail reports.

## 12. Launch checklist

1. Google Search Console: submit `https://mcallenpublicadjuster.com/sitemap.xml` (the old Yoast
   sitemap URLs now redirect there). Use URL Inspection on the homepage and a few articles.
2. Verify the **TDI license #3356839** on the TDI license lookup before launch
   (https://www.tdi.texas.gov/agent/agent-lookup.html). The number appears in
   `includes/config.php` (`license`) — change it there if needed and it updates site-wide.
3. Optional analytics: put a GA4 ID in `analytics_id` in `includes/config.php`, and update the
   Privacy Policy (`content/pages/privacy-policy.php`) to mention it.
4. Delete the old WordPress backup folder from the server once you're satisfied.

## Editing content later

* Articles: `content/posts/<slug>.php` → URL `/<slug>/`. Start from `content/posts/_NEW-POST-TEMPLATE.txt`.
* Service pages: `content/services/<slug>.php` → `/services/<slug>/`.
* Pages: `content/pages/<name>.php` (`author__joseph-dittman.php` → `/author/joseph-dittman/`).
* Phone, email, license, SMTP recipient: `includes/config.php`.
* Navigation and footer links: `includes/functions.php` (`primary_nav()`, `footer_nav()`).
* The sitemap, RSS feed, blog list, related posts, and schema update automatically.
