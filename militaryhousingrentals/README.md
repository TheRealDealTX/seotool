# militaryhousingrentals.com: listing add-on

Claim-a-listing, free/paid property submissions with Stripe, owner accounts and an
admin panel, added to the existing custom-PHP site **without rebuilding it**.

## What the site is

- Custom PHP 8.2 on Hostinger Cloud Enterprise (CloudLinux, LiteSpeed, `.htaccess` honored).
  Account `u401386392`, docroot `/home/u401386392/domains/militaryhousingrentals.com/public_html`.
- Front controller `site.php` (routed by `.htaccess`), templates in `app/views/`, helpers in `app/lib.php`.
- The 139 original listings live in `app/data/listings.json` (no database before this add-on).
  `wp-content/uploads/` is only image storage left over from the old WordPress install.

## What this folder holds

| Path | |
| --- | --- |
| `public_html/app/mhr/` | The add-on (new). Not web-reachable: `.htaccess` refuses `/app/`. |
| `public_html/assets/css/mhr.css` | Styles for the new components (new). |
| `public_html/wp-content/uploads/owners/.htaccess` | Owner photo folder: images only, PHP never runs (new). |
| `public_html/site.php`, `app/lib.php`, `app/forms.php`, `app/views/property.php`, `app/views/submit.php` | Existing files with small hooks. The first commit in this folder is the untouched live copy, so `git diff` shows exactly what changed. |
| `private/config.sample.php` | Template for the real config, which lives **outside** `public_html` at `/home/u401386392/domains/militaryhousingrentals.com/private/config.php`. Never commit the real one. |
| `dev/` | Local test harness: `router.php` (emulates `.htaccess` for `php -S`), `stripe-mock.php`, `e2e.js` (Playwright), `live-smoke.js`. |

Not committed: `listings.json`, posts and the rest of the existing site (unchanged on the server), and `app/storage/submissions.log` (personal data).

## How it works

- **Data:** MySQL `u401386392_mhr` (tables `mhr_*`, created automatically on first connection from `app/mhr/schema.sql`).
  Existing listings stay in `listings.json`; a row in `mhr_listings` adds owner edits (stored as overrides), status,
  owner and contact visibility. New submissions are stored in full in that table. `listings()` in `lib.php` merges both,
  so the listing grid, maps, base pages, sitemaps and RSS pick up new listings automatically.
- **Hidden contact details:** every listing whose row isn't `contact_visible` has phone, email, website, phone note and
  the Sources list removed from the data before any template runs (so they're absent from HTML *and* schema), and phone
  numbers/emails in the description are redacted. The property page shows "🔒 Contact details hidden until the owner
  verifies this listing" with a **Claim this listing** button.
- **Claim ($10, set in admin):** `/claim/{slug}/` → name, email, authorization checkbox → Stripe Checkout
  (`allow_promotion_codes=true`) → on `paid` or `no_payment_required` the listing gets the owner, contact details and the
  "✓ Verified owner" badge. Fulfilment is idempotent (row lock + status) and runs from both `/checkout/success/` (retrieves
  the session) and the webhook `/stripe/webhook` (`checkout.session.completed`, signature verified).
- **Submit:** `/submit-property/` (same URL/title/meta). Free → pending → admin approves → published with contact hidden
  and the approval email (`app/mhr/emails.php`, HTML + plain text from the site mailbox: live URL and the paid upgrade). Paid → Stripe → published instantly with contact shown. A cancelled checkout keeps the submission
  as a free pending listing.
- **Featured:** every paid listing (claim or paid submission) is Featured: badge, home-page Featured section,
  `/bases/featured/`, and first in `/properties/` and base pages (server order and the "Newest" sort in `site.js`).
  Admins can toggle Featured on any listing.
- **Owners:** passwordless. One-time email links (30 min sign-in / 7 day verification, only a SHA-256 hash stored).
  Dashboard at `/account/` to edit listing details and photos. Photos are checked by content (JPEG/PNG/WebP/GIF), decoded
  with GD, resized to 1600px and re-encoded as WebP under random names.
- **Admin:** `/admin/`: submissions, listings (edit/unpublish/delete/restore, owner assign/revoke, contact + badge toggles),
  owners, payments, messages (incl. the old contact-form log), settings (Stripe keys stored AES-256-GCM encrypted, price,
  test-Stripe and test-email buttons, password change). Lockout after 5 failed logins per IP (10 per username) for 15 min.
- **Security:** CSRF token + honeypot on every form, prepared statements everywhere, output escaped with `e()`,
  session cookie `Secure; HttpOnly; SameSite=Lax` with strict mode, `no-store` + `noindex` on claim/checkout/account/admin.
- **Email:** SMTP over implicit TLS to `smtp.hostinger.com:465` as `info@militaryhousingrentals.com`
  (password only in the private config).

## Deploy

Files are uploaded to the matching paths under `public_html/` (Hostinger File Manager or its upload API).
Upload `app/mhr/*` before `app/lib.php`, and `app/lib.php` before `app/views/submit.php`. Clear the Hostinger cache afterwards.

## Local testing

```bash
mysqld_safe & # MariaDB with database mhr_local
php -S 127.0.0.1:8099 dev/stripe-mock.php            # env MOCK_WEBHOOK_URL, MOCK_WHSEC, MOCK_STATE
php -S 127.0.0.1:8080 -t <copy-of-public_html> dev/router.php
node dev/e2e.js http://127.0.0.1:8080 <mail-dir> <shots-dir> <fixtures-dir>
```

Use a private config with `'dev' => true`, `'stripe_api_base' => 'http://127.0.0.1:8099'` and
`'smtp' => ['capture_dir' => …]`, and point `origin` in the local copy of `app/config.php` at `http://127.0.0.1:8080`.
