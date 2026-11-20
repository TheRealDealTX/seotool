# westcarrolltonapartments.com — West Carrollton, OH apartment directory

Custom PHP 8 site (no framework). Deployed to Hostinger (Agency plan, nginx + PHP-FPM) at `public_html/`.

- `index.php` front controller / router (nginx falls back to it for unknown paths)
- `app/` controllers, views, helpers. Every file starts with `defined('WCA') || exit;` because nginx ignores `.htaccess`.
- `app/config.php` **server only, git-ignored** (copy `app/config.sample.php`): MySQL, SMTP mailbox, admin hash, Stripe.
- `app/data/seed_listings.php` initial listings, inserted on first run when the `listings` table is empty.
- `content/posts/*.php` blog posts (see `content/POST_SPEC.md`). `old_urls` in each post 301-redirect old WordPress URLs.
- `app/content.php` legacy redirect map + 410 list for removed WordPress posts.
- `assets/` CSS/JS/images (photos: Unsplash license, see `assets/img/photos/CREDITS.txt`).
- `uploads/` owner-uploaded photos (re-encoded to WebP by GD).

Payments: Stripe Checkout via REST (keys in Admin → Settings). Webhook: `/stripe/webhook` (`checkout.session.completed`).
Owner accounts are passwordless (email verification + magic sign-in links).
Admin: `/admin/`.
