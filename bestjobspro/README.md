# bestjobspro.com: custom PHP rebuild

A hand-built PHP site that replaces the WordPress/Elementor install at
[bestjobspro.com](https://bestjobspro.com). No database, no plugins, no build step.
Upload the contents of this folder to `public_html` on Hostinger.

## What's here

| Path | What it is |
| --- | --- |
| `index.php` | Front controller: canonical host, 301 redirects, routing, 404s |
| `.htaccess` | Sends every non-file request to `index.php`; blocks `inc/` and `content/`; caching |
| `inc/config.php` | Business details (NAP), navigation, **job openings**, tools list, redirects |
| `inc/layout.php` | `<head>`, header, footer, icons, schema (EmploymentAgency, Breadcrumb, FAQ) |
| `inc/pages/*.php` | One template per page (home, about, services, employers, jobs, apply, contact, blog, tools, legal, 404) |
| `inc/posts.php` + `content/posts/*.php` | Blog engine and the nine posts (one PHP array per post) |
| `inc/tools.php` + `assets/js/tools.js` | Six interactive career tools |
| `inc/forms.php` | Contact and application forms: validation, honeypot + signed timestamp, email with résumé attachment |
| `inc/sitemap.php` | Dynamic `/sitemap.xml` |
| `assets/` | `css/site.css`, `js/site.js` (nav, animations, talent-network canvas), images |

## URLs: nothing from the old site 404s

Every URL in the old Yoast sitemaps still answers:

- Pages kept at the same path: `/`, `/about/`, `/our-services/`, `/employers/`, `/job-postings/`,
  `/applications/`, `/contact-us/`, `/blog/`, `/privacy-policy/`, `/category/job-articles/` (now `noindex`, it duplicates `/blog/`).
- All nine blog posts keep their slugs, e.g. `/independent-contractor-tax-responsibilities/`.
- **301 redirects:** `/write-for-us/` → `/blog/` (page removed as requested), `/feed/` and other feeds,
  `/sitemap_index.xml`, `/post-sitemap.xml`, `/page-sitemap.xml`, `/category-sitemap.xml` → `/sitemap.xml`,
  `wp-admin`/`wp-login.php`/`wp-json`/`xmlrpc.php` → `/`, old `/wp-content/uploads/…` image URLs → the copy in `assets/img/`
  (when one exists), missing trailing slashes → slash version.

New pages: `/career-tools/` plus six tool pages, and `/terms-of-use/`.

## Editing content

- **Job openings:** edit the `JOBS` array in `inc/config.php`. The job board, homepage, quiz and application form all read it.
- **Phone, email, address:** constants at the top of `inc/config.php`.
- **New blog post:** copy any file in `content/posts/`, rename it to the new slug, edit the array. It appears on
  `/blog/`, in the sitemap and at `/<slug>/` automatically. `{{tool}}` and `{{cta}}` in the body insert a tool widget
  and the apply box; every `<h2>` needs an `id` (the table of contents is built from them).
- After changing CSS/JS, bump `ASSET_VER` in `inc/config.php`.

## Deploying to Hostinger

1. In hPanel → Websites → bestjobspro.com, back up the current WordPress site (Files + Database) first.
2. Remove the WordPress files from `public_html` (keep any `google*.html` Search Console verification file).
3. Upload everything in this folder (including the hidden `.htaccess`) to `public_html`.
4. hPanel → **Emails**: make sure the mailbox `careers@bestjobspro.com` exists, and create `no-reply@bestjobspro.com`
   (forms send from it; mail from a non-existent address is often rejected).
5. hPanel → Security → SSL: turn on **Force HTTPS**.
6. Optional: create `inc/secret.php` containing `<?php const FORM_SECRET = 'some-long-random-string';` (not committed).
7. Test: submit the contact form and an application with a résumé, then check the inbox.
8. Search Console: submit `https://bestjobspro.com/sitemap.xml` and request indexing for the homepage.

PHP 8.1+ is required (Hostinger default is fine). The `fileinfo` extension (on by default) is used to check résumé uploads.

## Local preview

```sh
php -S localhost:8000 index.php
```
