TEMPLE ROOFERS — templeroofs.com
Website package for Hostinger shared hosting (PHP 8 + Apache)
=====================================================================

This folder IS the website. Everything in it goes into public_html.
No Node.js, no database, no build step.

---------------------------------------------------------------------
1. UPLOAD AND EXTRACT
---------------------------------------------------------------------
 1. Log in to Hostinger hPanel > Websites > templeroofs.com > File Manager.
 2. Open public_html. Delete any placeholder files (e.g. default.php,
    index.html) that Hostinger created.
 3. Upload templeroofs-hostinger-ready.zip into public_html.
 4. Right-click the ZIP > Extract > extract into public_html itself
    (leave the folder field as "." / public_html). The files sit at the
    ZIP root, so you should end up with public_html/index.php,
    public_html/.htaccess, public_html/assets/ ... (no extra sub-folder).
 5. Delete the ZIP afterwards.
 6. Make sure hidden files are shown in File Manager and that
    public_html/.htaccess exists (it powers the clean URLs).

Server settings (hPanel > Advanced > PHP Configuration):
 - PHP version 8.1 or newer (8.2/8.3 recommended).
 - Extensions: curl, mbstring, openssl, json (all enabled by default).
 - SSL: hPanel > Security > SSL — make sure the free SSL is "Active".
   .htaccess redirects every request to https:// and www to non-www.
   If you are testing on a temporary Hostinger domain without SSL,
   temporarily comment out the two "Force HTTPS" lines in .htaccess.
 - The folder public_html/storage must be writable by PHP (it is by
   default on Hostinger). It holds the weather cache, form rate-limit
   records and logs. It is blocked from the web.

---------------------------------------------------------------------
2. CONFIGURE EMAIL DELIVERY (lead forms)  — IMPORTANT
---------------------------------------------------------------------
Every form on the site posts to /api/lead/ (server-side PHP). The
destination address is stored ONLY in a private PHP config file on the
server. It never appears in any page, script, stylesheet or network
response.

The package ships with includes/private/mail-config.php, already set
to deliver to the private recipient address you provided, using PHP
mail() until SMTP is configured. For reliable delivery (and to keep
leads out of spam), set up authenticated SMTP:

 a) hPanel > Emails > create a mailbox on your domain, e.g.
    no-reply@templeroofs.com (any name works). Note its password.

 b) RECOMMENDED — move the config outside public_html:
    In File Manager, go one level ABOVE public_html (the folder that
    contains public_html), create a folder named
        templeroofs-private
    and MOVE includes/private/mail-config.php into it, so the path is
        .../templeroofs-private/mail-config.php
    The site checks that location first automatically.
    (config-templates/mail-config.sample.php is a blank template.)

 c) Edit mail-config.php:
        'from_email' => 'no-reply@templeroofs.com',
        'smtp' => [
            'host'     => 'smtp.hostinger.com',
            'port'     => 465,
            'secure'   => 'ssl',
            'username' => 'no-reply@templeroofs.com',
            'password' => 'THE-MAILBOX-PASSWORD',
        ],
    Leave 'recipient' as it is unless you want leads sent elsewhere.
    If port 465 is blocked, use port 587 with 'secure' => 'tls'.

 d) Submit a test request at /free-roof-inspection/ and confirm the
    email "New Temple Roofers Lead — Free Roof Inspection Request"
    arrives (check spam the first time and mark it "Not spam").

If delivery ever fails, the visitor sees an honest error with the phone
number (never a fake success), and their request is saved as a JSON
file in templeroofs-private/undelivered-leads/ (or, if that folder does
not exist, storage/undelivered-leads/, which is blocked from the web).
Check there if you suspect missed leads; delete files once handled.
Delivery errors (no personal data) are logged to storage/logs/forms.log.

Form protections built in: server-side validation, signed CSRF/timing
token (submissions faster than 3 s or older than 6 h are refused),
hidden honeypot field, same-origin check, rate limit of 5 submissions
per 15 minutes per visitor (IP stored only as a salted hash), CR/LF
stripping to prevent email header injection, HTML-escaped email body.

---------------------------------------------------------------------
3. LIVE WEATHER (/weather/ and the homepage widget)
---------------------------------------------------------------------
 - No API key is needed.
 - The browser calls /api/weather/ on your own site. The server fetches:
     * Current conditions + 7-day forecast from Open-Meteo
       (api.open-meteo.com) for Temple, TX (31.0982, -97.3428),
       Fahrenheit, mph, inches, America/Chicago time zone.
     * Active alerts from the National Weather Service
       (api.weather.gov/alerts/active?point=31.0982,-97.3428).
 - Responses are cached in storage/cache: forecast 10 minutes, alerts
   5 minutes. If a service is down, the most recent copy (up to 6 hours
   old) is shown with a clear "cached data from <time> — not live" note;
   older than that, the page shows a friendly "unavailable" message.
   NWS alerts are never invented: if NWS cannot be reached, the page
   says alerts could not be retrieved.
 - The "roof-weather indicator" is informational only (rules are shown
   on the page) and is clearly separated from official alerts.
 - Change the coordinates/cache times in includes/config.php.

---------------------------------------------------------------------
4. BLOG POSTS AND SCHEDULED PUBLISHING
---------------------------------------------------------------------
 - All 10 articles are included in content/blog/ (01-...php to 10-...php).
 - Article N is published automatically at 00:00 Central Time on:
       blog_launch_date + (N - 1) x blog_interval_days
   With the default settings in includes/config.php
   ('blog_launch_date' => '2026-10-03', 'blog_interval_days' => 3):
       1 Oct 3 · 2 Oct 6 · 3 Oct 9 · 4 Oct 12 · 5 Oct 15
       6 Oct 18 · 7 Oct 21 · 8 Oct 24 · 9 Oct 27 · 10 Oct 30, 2026
 - If you launch on a different date, change ONLY blog_launch_date —
   every date recalculates automatically.
 - Before its date, an article returns 404 and is excluded from the blog
   index, categories, search, RSS feed (/blog/feed/), homepage, HTML
   sitemap and sitemap.xml. Links to it inside other pages are shown as
   plain text until it goes live. No cron job or manual upload needed.
 - To add a new article, copy an existing file in content/blog/, give it
   the next 'order' number and a new 'slug', and edit the text.

---------------------------------------------------------------------
5. EDITING TEXT, IMAGES AND CONTACT DETAILS
---------------------------------------------------------------------
 - Business name, phone, website URL, coordinates, blog dates:
       includes/config.php
 - Which services / service areas are listed and in what order:
       includes/catalog.php
   To stop advertising a community you do not serve, set its
   'published' => false. Its page then returns 404 and disappears from
   menus, structured data and both sitemaps (the content stays as an
   unpublished template).
 - Service page copy:   content/services/<slug>.php
 - Service area copy:   content/areas/<slug>.php
 - About page copy:     content/pages/about.php
 - Blog articles:       content/blog/NN-<slug>.php
 - Homepage, inspection page, legal pages, tools page text:
       includes/pages/<page>.php
 - Cost calculator assumptions (illustrative prices per square, tear-off,
   decking, labor multipliers): includes/calculator-costs.php
   Update these to match your real costs whenever they change.
 - Images: assets/images/<key>-480.webp, -800.webp, -1600.webp plus
   dimensions/alt text in assets/images/manifest.json. To replace an
   image, keep the same file names and aspect ratio (or update w/h in
   manifest.json). Image sources and licenses: assets/images/CREDITS.txt.
   All photos are licensed stock images and are labeled site-wide as
   illustrations, not Temple Roofers projects. Replacing them with your
   own job photos over time is recommended.
 - Colors and fonts: assets/css/site.css (variables at the top).
 - Text files are UTF-8. Edit with hPanel's File Manager editor.

---------------------------------------------------------------------
6. TESTING AFTER UPLOAD
---------------------------------------------------------------------
 [ ] https://templeroofs.com/ loads over HTTPS; http:// and www redirect.
 [ ] Click through the menu: Services, Service Areas, Roofing Tools,
     Weather, Blog, About, Contact, plus footer links.
 [ ] /some-made-up-page/ shows the branded 404 page.
 [ ] /weather/ shows current Temple conditions, 7 forecast days and an
     alerts box ("No active alerts" or real NWS alerts).
 [ ] /tools/roof-replacement-cost-calculator/, /tools/roof-pitch-calculator/
     and /tools/storm-damage-checklist/ update results as you type.
 [ ] Submit /free-roof-inspection/ and /contact/ forms; you land on
     /thank-you/ and the email arrives.
 [ ] https://templeroofs.com/includes/config.php and /storage/ return
     403 Forbidden (private folders are protected).
 [ ] /sitemap.xml and /robots.txt load. Submit
     https://templeroofs.com/sitemap.xml in Google Search Console.
 [ ] Phone buttons dial (512) 297-7580 on a mobile phone.

---------------------------------------------------------------------
7. FILE MAP
---------------------------------------------------------------------
 index.php             Front controller (clean URLs, all pages)
 404.php               Apache error-page fallback
 .htaccess             HTTPS, clean URLs, security & caching headers
 robots.txt            Crawler rules + sitemap location
 sitemap.xml           Generated dynamically by index.php
 favicon.*, apple-touch-icon.png, site.webmanifest
 assets/css, js, fonts, images     Static assets (self-hosted fonts)
 includes/             PHP templates, config, form + weather logic (private)
 includes/private/     mail-config.php (private; move outside public_html)
 content/              Page copy: services, areas, blog, about (private)
 vendor/phpmailer/     PHPMailer 7.1.1 (LGPL 2.1) for SMTP email (private)
 storage/              Cache, rate-limit records, logs (private, writable)
 config-templates/     Blank mail-config template (private)

Nothing in this package contains passwords or API secrets.
