# cowboytinyhomes.com — PHP source (working copy)

Copy of the editable source of https://cowboytinyhomes.com (Hostinger Cloud, user `u401386392`,
document root `domains/cowboytinyhomes.com/public_html`). Secrets (`inc/secrets.php`, `.private/`),
plan data/files, images and the old WordPress backup are **not** included — the server is the source of truth.

Not deployed by the huttoroofs `deploy.sh` (this folder is excluded there).

## Amazon affiliate links
- `inc/amazon.php` — `amz($key, $text)` inline link, `gear_box($keys, $heading, $intro)` product box,
  `amz_disclosure()`. Tag: `cowboytinyhomes-20`. Links are `https://www.amazon.com/dp/ASIN?tag=…`
  with `rel="sponsored nofollow noopener"`.
- `inc/amazon-products.php` — the one catalog of products (key => ASIN, name, blurb). Swap an ASIN here
  if a listing goes dead.
- `/tiny-home-gear/` (`pages/tiny-home-gear.php`) — the gear roundup page.
- Disclosure: site-wide footer line, next to every box/inline link, and in the privacy policy.
