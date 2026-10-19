# insuranceadjustersalary.com - custom PHP rebuild

Replaces the WordPress/Elementor site. Plain PHP 8.3, no database, no plugins.

**Live (temporary domain):** https://honeydew-goat-878624.hostingersite.com/ - Hostinger Agency website UID `SU5z7VSkt`.

## Structure

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: homepage, legacy WordPress redirects, `sitemap.xml`, `robots.txt`, 404 |
| `inc/config.php` | Site constants, helpers, nav, tool list, blog loader |
| `inc/header.php`, `inc/footer.php` | Shared layout, meta tags, JSON-LD |
| `inc/home.php` | Homepage (targets "insurance adjuster salary") |
| `inc/data.php` | BLS anchor figures, state wage index, chart data |
| `inc/post-template.php` | Blog post renderer (TOC, FAQ schema, related posts) |
| `content/posts/*.php` | One file per blog post - see `content/POST_SPEC.md` |
| `insurance-adjuster-advice/` | Blog index + one folder per post (keeps the original blog URL) |
| `salary-calculator/`, `cat-deployment-calculator/`, `public-adjuster-fee-calculator/`, `salary-by-state/`, `tools/` | Interactive tools |
| `assets/` | CSS, JS, images (Unsplash License photos, WebP) |

## Adding a blog post

1. Create `content/posts/<slug>.php` following `content/POST_SPEC.md`.
2. Create `insurance-adjuster-advice/<slug>/index.php` containing
   `<?php $slug = '<slug>'; require dirname(__DIR__, 2) . '/inc/post-template.php';`
3. Deploy. The blog index, homepage cards and sitemap pick it up automatically.

## Moving the domain

Everything builds URLs from the request host, so no code changes are needed. When the
real domain is attached in Hostinger, the temporary-domain `noindex` switches to
`index, follow` automatically, `robots.txt` starts listing the sitemap, and http/www
requests redirect to `https://insuranceadjustersalary.com`.

## Local preview / deploy

```sh
php -S 127.0.0.1:8000 -t .   # inner pages need a router that serves dir/index.php
./deploy.sh                   # see header for the IAS_FB_* credentials
```

## Texas focus and the affiliate code

- The site leans on Texas: Texas metro estimates and a claim-season calendar live in `inc/data.php`
  (`texas_metros()`, `texas_seasons()`), calculators default to Texas, and every post has a Texas section.
- Every "Get Certified" link must carry "Use joe20 for 20% off". Use `cert_btn()` / `promo_line()` from
  `inc/config.php` in templates, and follow any AdjustingOnline link in post bodies with
  `Use <strong>joe20</strong> for 20% off.`
