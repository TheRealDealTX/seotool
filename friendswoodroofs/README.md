# Friendswood Roofers — friendswoodroofs.com

Website for Friendswood Roofers, a roofing company serving Friendswood, TX.
It is plain PHP 8.1+, HTML, CSS and vanilla JavaScript. There is **no build step,
no Node.js and no database**. Upload the files and it runs on standard Hostinger
hosting (Apache/LiteSpeed with `mod_rewrite`).

## Status

| Area | Status |
| --- | --- |
| All pages, 7 service pages, 5 articles, planner, legal pages, 404, thank-you | Complete |
| Navigation, mobile menu, FAQ accordions, blog filters, planner, scroll effects | Complete and tested |
| Estimate form (validation, CSRF, honeypot, rate limit, SMTP via PHPMailer) | Complete and tested against a local SMTP server. **Real delivery is waiting on SMTP credentials** (see [Email setup](#email-setup-smtp)). |
| Weather map (RainViewer embed) | Integrated. Confirm it renders on the live site; see [Weather map](#weather-map). |
| SEO: titles, descriptions, canonicals, Open Graph, JSON-LD, sitemap, robots | Complete |
| Deployment to Hostinger | **Not done.** The Hostinger connector was not authorized in the build session. Follow [Deployment](#deployment-hostinger). |

## File structure

```
friendswoodroofs/
├── public_html/              → upload to the domain's public_html (web root)
│   ├── index.php             front controller: finds ../app and runs it
│   ├── .htaccess             HTTPS, www→apex, clean URLs, caching, blocks private paths
│   ├── robots.txt
│   ├── favicon.svg, favicon.ico, favicon-32.png, apple-touch-icon.png, icon-*.png, site.webmanifest
│   └── assets/
│       ├── css/site.css      all styles (design tokens at the top)
│       ├── js/site.js        all scripts (progressive enhancement only)
│       └── img/              WebP photos (480/960/1600px), og-default.jpg, logo-mark.png
├── app/                      → upload NEXT TO public_html (outside the web root)
│   ├── bootstrap.php
│   ├── config/
│   │   ├── site.php          phone, domain, launch date, service cities, weather settings
│   │   ├── mail.example.php  SMTP template → copy to mail.php (never committed)
│   │   └── mail.php          (you create this; holds the SMTP password)
│   ├── content/              all editable copy (see "Editing content")
│   ├── src/                  router, helpers, security, mailer, form handler, SEO/schema
│   ├── templates/            layout.php, partials/ (header, footer, form…), pages/
│   ├── storage/              rate-limit files, logs, auto-generated secret.key (must be writable)
│   ├── vendor/               PHPMailer 6.12 (installed with Composer, committed so no Composer is needed on the server)
│   └── .htaccess             "Require all denied" (protects app/ if it ever sits inside public_html)
└── tools/                    local-only helpers (not deployed)
    ├── dev-router.php        local preview router for `php -S`
    ├── validate.py           crawls a running copy and checks SEO/a11y basics
    ├── package.sh            builds dist/friendswoodroofs-deploy.zip
    └── deploy-hostinger.sh   uploads via the Hostinger Agency File Browser API
```

`public_html/index.php` looks for the app folder in this order: `$FR_APP_DIR`
(environment variable), `../app` (recommended), then `public_html/app`
(fallback, blocked from the web by `app/.htaccess` and the root `.htaccess`).

## Local preview

```sh
cd friendswoodroofs
php -S 127.0.0.1:8080 -t public_html tools/dev-router.php
# open http://127.0.0.1:8080
python3 tools/validate.py http://127.0.0.1:8080   # SEO/a11y crawl
```

To test the form locally without real email, point `FR_MAIL_CONFIG` at a
config file for a local SMTP catcher (for example MailHog or Mailpit on
port 1025, with `'encryption' => 'none'`).

## Deployment (Hostinger)

These steps fit hPanel on shared, Cloud or Agency hosting.

1. **Point the domain** `friendswoodroofs.com` at the Hostinger website and enable
   the free **SSL certificate** (hPanel → Security → SSL). The `.htaccess` forces HTTPS
   and redirects `www` to the bare domain.
2. **PHP version:** hPanel → Advanced → PHP Configuration → choose **PHP 8.1 or newer**
   (8.2/8.3 recommended). Default extensions (`openssl`, `mbstring`, `json`) are enough.
3. **Upload the files.** Pick one:
   - **File Manager (simplest):** run `tools/package.sh` locally (or zip the
     `public_html` and `app` folders yourself), upload the zip to the domain folder
     (the one that *contains* `public_html`, e.g. `domains/friendswoodroofs.com/`) and
     extract it. You should end up with `…/public_html/index.php` and `…/app/bootstrap.php`
     side by side. Delete any default `index.html` or `default.php` Hostinger placed in `public_html`.
   - **Agency plan API:** generate File Browser upload credentials with the Hostinger API
     call `agency-hosting_generateUploadURLV1`, export them as `FR_FB_URL`, `FR_FB_AUTH`,
     `FR_FB_REST`, and run `tools/deploy-hostinger.sh`. Then clear the cache with
     `agency-hosting_clearWebsiteCacheV1` (or hPanel → Cache).
   - If your plan only lets you write inside `public_html`, put the app at
     `public_html/app/`. It still works, and both `.htaccess` files block web access to it.
4. **Make storage writable:** `app/storage/`, `app/storage/logs/` and
   `app/storage/ratelimit/` need write permission for PHP (755 for folders is normally
   enough on Hostinger). If storage isn't writable, rate limiting falls back to the system
   temp folder.
5. **Create `app/config/mail.php`** (see next section).
6. **Check the site:** open `/`, `/sitemap.xml`, `/robots.txt`, a missing page (should show the
   custom 404 with status 404), then submit a test estimate request.
7. **Search Console:** add the domain property and submit `https://friendswoodroofs.com/sitemap.xml`.

If you see "Site configuration error: the 'app' folder was not found", the `app`
folder is not in either expected location.

## Email setup (SMTP)

The form sends through **authenticated SMTP using PHPMailer**. Nothing is sent
with PHP's `mail()`, and the recipient address and credentials exist only in
`app/config/mail.php`, never in browser code.

1. **Create a mailbox on the domain** in hPanel → Emails, for example
   `estimates@friendswoodroofs.com`. The sender must be on `friendswoodroofs.com`
   so SPF/DKIM/DMARC line up. The visitor's email, when given, is used only as `Reply-To`.
2. **Copy** `app/config/mail.example.php` to `app/config/mail.php` and fill in:

   | Setting | Hostinger value |
   | --- | --- |
   | `recipient` | `teamwriteforus.today@gmail.com` (already set) |
   | `host` | `smtp.hostinger.com` |
   | `port` / `encryption` | `465` / `'ssl'` (or `587` / `'tls'`) |
   | `username` | the full mailbox address |
   | `password` | the mailbox password |
   | `from_email` | the same mailbox address |

   Alternatively, put the file anywhere outside the web root and set the
   environment variable `FR_MAIL_CONFIG` to its absolute path.
3. **Domain email authentication** (hPanel → Emails → the domain → DNS / Authentication,
   or at your DNS provider if the domain's DNS is not on Hostinger):
   - **SPF:** one TXT record on `@`, e.g. `v=spf1 include:_spf.mail.hostinger.com ~all`.
     If an SPF record already exists, merge the include into it (only one SPF record is allowed).
   - **DKIM:** enable it in hPanel; it publishes the `hostingermail-*._domainkey` record(s).
   - **DMARC:** add TXT on `_dmarc`, starting with monitoring:
     `v=DMARC1; p=none; rua=mailto:<a mailbox you read>`. Tighten to `p=quarantine` once reports look clean.
   - Use the exact values hPanel shows; they can change.
4. **Test:** submit the form with your own phone number. Check that the message reaches
   `teamwriteforus.today@gmail.com` (and isn't in spam), that **Reply** goes to the
   visitor email when one is entered, and that `app/storage/logs/mail.log` has no errors.
   In Gmail, consider a filter so messages from the estimates mailbox are never sent to spam.

**Failure behaviour:** if SMTP is not configured or the server rejects the message,
the visitor sees "Sorry, your request could not be sent right now and was not
delivered. Please call us at …". They are never shown a success message for an
unsent request. The transport error (no form contents, no password) is logged to
`app/storage/logs/mail.log`.

### Form protections

- Server-side validation of every field. Required: name, phone, address/ZIP, service, consent. Email and message are optional, so phone-only inquiries work.
- CSRF token (session cookie `fr_sess`, set only on pages with the form).
- Hidden honeypot field (bots are silently discarded) and a signed timestamp that rejects submissions made under 3 seconds after page load.
- Rate limit: 5 submissions per hour per visitor (IP is hashed with a server secret, files expire after about a day). Change `RATE_LIMIT_*` in `app/src/estimate.php`.
- Header-injection protection: control characters, including CR/LF, are stripped from single-line fields, the email is validated, and PHPMailer encodes headers.
- All output is escaped with `htmlspecialchars`. Security headers (CSP, nosniff, frame options, referrer policy) are sent from `app/src/security.php`.
- Works without JavaScript (normal POST → redirect to `/thank-you/`, or back to the form with errors and the visitor's input kept). With JavaScript, it validates inline and submits with `fetch`.

## Editing content

| What | Where |
| --- | --- |
| Phone, domain, launch date, service cities, weather map | `app/config/site.php` |
| Service pages (intro, problems, scope, process, cost factors, FAQs, related links) | `app/content/services.php` |
| Blog article list (titles, SEO titles, descriptions, categories, images, dates) | `app/content/articles.php` |
| Article bodies and FAQs | `app/content/articles/<slug>.php` (HTML) |
| FAQ page (and the homepage FAQ subset, `'home' => true`) | `app/content/faqs.php` |
| Planner questions | `app/content/planner.php` |
| Page titles and meta descriptions for fixed pages | `page_meta()` in `app/src/content.php` |
| Page layouts and copy for Home, About, Contact, legal pages, etc. | `app/templates/pages/*.php` |
| Header, footer, form, CTA band, cards | `app/templates/partials/*.php` |
| Colors, spacing, fonts | top of `public_html/assets/css/site.css` |

**Adding a service:** add an entry to `services.php` with a new slug. It
appears automatically in the navigation, footer, services grid, form options, sitemap and structured data.

**Adding an article:** add an entry to `articles.php` (choose `days_before_launch`)
and create `app/content/articles/<slug>.php` returning `['body' => '…HTML…', 'faqs' => [...]]`.
Use an existing article as a template.

**Images:** register photos in `app/content/images.php` and provide
`<key>-480.webp`, `<key>-960.webp` and `<key>-1600.webp` (3:2) in `public_html/assets/img/`.
All current photos are openly licensed Wikimedia Commons images, credited on
`/image-credits/` and captioned as illustrative. Replace them with your own project
photos when you have them, and only caption a photo as your work if it is.

## Publication dates

Article dates are calculated from `launch_date` in `app/config/site.php`
(currently `2026-10-01`). The newest article uses that date, and the others are 3, 6, 9
and 12 days earlier:

| Article | Offset |
| --- | --- |
| Friendswood Roofers: How to Choose a Roofing Contractor | launch date |
| Roof Repair or Replacement? A Guide for Friendswood Homeowners | −3 days |
| Friendswood Roofing Maintenance: A Seasonal Checklist | −6 days |
| Asphalt Shingles vs. Metal Roofing for Homes in Friendswood, TX | −9 days |
| What to Expect During a Roof Inspection in Friendswood | −12 days |

The same dates are used on the blog index, article pages, `BlogPosting`
structured data and sitemap `lastmod`. They only change when you edit
`launch_date`; nothing changes on page load. Set it to the owner-approved launch
date before going live. The privacy policy and terms also use it as their effective date.

## Weather map

- **Provider:** [RainViewer](https://www.rainviewer.com/) live radar embed
  (`https://www.rainviewer.com/map.html?loc=29.5294,-95.2010,8&…&layer=radar`), centered on Friendswood with the radar/precipitation layer.
- **Why RainViewer:** its [Terms](https://www.rainviewer.com/terms.html) (section VII) let websites
  embed its live radar maps, provided the RainViewer watermark/source is not hidden or distorted.
  Windy's embed was ruled out because Windy says its widget is not for commercial websites.
- **Attribution:** the RainViewer logo inside the map is kept, and the caption credits RainViewer with a link.
- **Behaviour:** the iframe has a descriptive `title`, fixed 4:3 aspect ratio (no layout shift)
  and `loading="lazy"`, so it loads only near the viewport. A visible fallback link opens the radar on
  RainViewer. If the map hasn't loaded 20 seconds after it scrolls into view, the frame is replaced
  with that link. The rest of the page never depends on it, and the CSP only allows frames from `www.rainviewer.com`.
- **Official warnings:** the section links to NWS Houston/Galveston, the NWS point forecast for
  Friendswood and the National Hurricane Center.
- **Privacy:** RainViewer's embed loads its own scripts, including Google Tag Manager. The privacy policy says so.
- **Configuration:** `weather` in `app/config/site.php` (`enabled`, `zoom`). Embed parameters live in
  `app/templates/partials/weather-map.php`. Re-check RainViewer's terms periodically.
- **Testing note:** in the build sandbox, RainViewer's page shell, logo and controls loaded in Chromium
  and its public radar data feed returned current frames, but proxy limits stopped the map tiles from
  rendering. **Check the map visually on the live site.**

## SEO

- Unique `<title>` and meta description per page, one `<h1>`, logical heading order and descriptive URLs.
- Canonical URLs and Open Graph/Twitter tags point to `https://friendswoodroofs.com`.
- `/sitemap.xml` is generated from the route list (services and articles are added automatically).
  `/robots.txt` points to it. `/thank-you/` and the 404 page are `noindex`.
- JSON-LD: `RoofingContractor` (name, URL, phone, logo, area served = Friendswood, TX; **no address,
  ratings, reviews, hours or credentials**), `WebSite`, `BreadcrumbList`, `Service` on service pages and `BlogPosting` on articles.
- Keywords: "Friendswood Roofers" is in the homepage title, H1 and introduction. "friendswood roofing" and
  "roofers in Friendswood" appear naturally. "roofers friendswood" and "roofing company friendswood"
  are not forced into ungrammatical copy.
- No ranking or rich-result outcomes are promised.

## Owner review before launch

Please confirm or edit these items. They are business decisions or legal details the site can't verify:

1. **`launch_date`** in `app/config/site.php` (sets article dates and policy effective dates).
2. **Service area:** only Friendswood is listed. Add other cities to `service_cities` only if you serve them.
3. **Process promises:** the site says you provide written estimates before work, photos of findings,
   clean-up and a final walkthrough, and that you do not pressure customers, promise insurance outcomes or
   waive deductibles (Home hero, About, service pages). Remove anything that doesn't match how you work.
4. **Consent wording** on the form ("by phone, text or email"). If you won't text customers, remove "text".
   If you plan marketing texts, get legal advice on TCPA consent.
5. **Privacy policy:** email retention period, the email provider description, and whether you'll add
   analytics (if so, update the policy).
6. **Terms of use:** governing law (Texas) and the limitation-of-liability wording. Consider a lawyer's review.
7. **Windstorm/TWIA and permit notes** (service area, storm page, FAQs, articles): general guidance only.
   Confirm they match your experience.
8. **Photos:** all are illustrative stock with credits. Swap in real project photos when available.
9. **SMTP credentials and DNS records** (SPF/DKIM/DMARC), then a live test submission.
10. **Hostinger deployment** of this folder to the friendswoodroofs.com website (Agency plan).

## What was tested (build session)

- All 23 indexable URLs plus `/thank-you/` return 200, unknown URLs return a real 404, and a missing
  trailing slash returns a 301 (PHP built-in server with `tools/dev-router.php`).
- `tools/validate.py`: unique titles and descriptions, single H1, heading order, canonicals, OG tags,
  img alt/width/height, iframe title/lazy/size, labelled form controls, valid JSON-LD, no duplicate
  IDs, no visible email address or recipient leak, every page internally linked, article dates
  consistent across index, article, schema and sitemap.
- Form, server side (28 + 9 checks): no-JS POST → 303 → thank-you; JSON path; phone-only; validation errors
  with preserved input; CSRF (wrong or cross-session token); honeypot; minimum time; forged timestamp;
  CR/LF header injection; rate limit (5 then 429); SMTP down → 503 with no false success; SMTP not
  configured → same; SMTP AUTH, From = domain mailbox, Reply-To = visitor, recipient correct
  (against a local authenticated SMTP server).
- Browser (Playwright/Chromium, 48 checks): mobile menu (open, focus, submenu, Escape returns focus),
  skip link, keyboard submenu, focus outlines, FAQ accordion by keyboard, inline validation with
  aria-invalid and error summary, fetch submission, service prefill, blog filters (URL, aria-current,
  live status), planner (validation, summary, copy, insert into form, service preselect),
  scroll reveal, and with JavaScript disabled: navigation, server-side blog filter, server-side
  planner summary, and form submission.
- Responsive screenshots from 320px to 1920px. No horizontal overflow at 320px.
  `prefers-reduced-motion` disables reveal animations and transitions.
- Text contrast: all text/background pairs meet WCAG AA (4.5:1+). Form borders are 3.4:1.
- Not measured: real-world Core Web Vitals (measure with PageSpeed Insights after launch), live SMTP
  delivery, and the rendered RainViewer map on the live site.
