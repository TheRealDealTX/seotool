# Notes for Claude

## What this repo is
Static rebuild of huttoroofs.com (see README.md). Other sites the owner runs live on
Hostinger as WordPress installs, not in this repo. Site-specific code for them lives
under `wordpress/<domain>/`.

## Hostinger: how to change files on a WordPress site
Account username `u401386392`. All sites are addon domains under
`/home/u401386392/domains/<domain>/public_html`.

- `hosting_files_list-website-and-directories` and `hosting_files_website-content`
  work for reading.
- `hosting_files_generate-upload-url` returns **404 for these addon domains** — do not
  rely on it.
- **Working write path:** commit the file to this (public) repo, push, then create a
  cron job that fetches it onto the server:
  `hosting_cron-jobs_create` with `time: "* * * * *"` and
  `wget -qO /home/u401386392/domains/<domain>/public_html/<path> https://raw.githubusercontent.com/TheRealDealTX/seotool/<short-sha>/<repo-path>`
  - Command must be ≤ 255 chars (use a 12-char commit SHA, not the full one).
  - Pin to a commit SHA, not a branch — raw.githubusercontent caches branch URLs ~5 min.
  - Avoid `&&`, `$VAR`, `curl … |` in the command: Cloudflare's WAF 403s the request.
  - Poll `hosting_files_list-website-and-directories` until the size matches, then
    **delete the cron** (`hosting_cron-jobs_delete`) and purge cache with
    `hosting_cache_clear-website`.
- `wordpress_installations_list` returns `[]` for this account, so the `wordpress_*`
  plugin/LiteSpeed tools (which need an installation id) are unusable. Use
  `wp-content/mu-plugins/` for drop-in code instead — no activation needed.
- Headless Chromium in the sandbox fails TLS against the agent proxy; verify live pages
  with `curl` (+ jsdom for JS behaviour) rather than Playwright.

## shineyourlightblog.com (AdSense placement, deployed 2026-10-03)
- WordPress + Elementor Pro (Hello Elementor theme), Yoast, Site Kit, LiteSpeed Cache.
  Front page is a static Elementor page (so `is_front_page()` is also `is_singular()`).
  Post body is rendered by Elementor's Post Content widget → `the_content` filter works.
  Archives use Elementor Loop Grid: `.elementor-loop-container > .e-loop-item`.
- AdSense publisher `ca-pub-3886800648957674` (script already loaded by Site Kit).
  Slots: display `8096221599`, in-article `1960371044`, multiplex `8746967795`,
  in-feed `5524169668` (layout key `-gd+y-52-bo+14o`).
- Live plugin: `wp-content/mu-plugins/syl-ad-placement.php`, source in
  `wordpress/shineyourlightblog/`. Rules: top ad after ~50-word intro, in-article every
  ~350 words (max 4), multiplex after body, in-feed after posts 3 and 9; never within
  two blocks of an affiliate/shopping link, disclosure or embed; never under a heading.
  Per-post opt-out: custom field `syl_no_ads = 1`.
- Affiliate links on the blog are mostly `amzn.to`, plus retailer links (Wayfair,
  Pottery Barn, RH, Home Depot, Crate & Barrel, Wisteria) and `teamwrite.gumroad.com`.
