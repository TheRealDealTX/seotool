# freegradecalculator.com

Custom PHP site (no framework, no database): 29 calculators, 12 guides, Amazon picks.
Hosted on Hostinger Cloud Enterprise (order 64270646, account u401386392).

| Path | What |
| --- | --- |
| `index.php` | Router: pages, tools, blog, legacy `.html` → slug 301s, www → apex |
| `inc/` | config, helpers, tool registry (`tools.php`), Amazon products, SMTP mailer, icons |
| `templates/` | header/footer layout and page templates |
| `widgets/` | calculator markup, one file per tool |
| `content/tools/*.php` | SEO copy + FAQs per tool |
| `content/articles/*.php` | blog posts (future `date` = scheduled, hidden until then) |
| `assets/js/tools.js` | all calculator logic (runs in the browser) |
| `assets/js/app.js` | UI: theme, search palette (Ctrl/⌘K), reveal effects, confetti |
| `CONTENT_SPEC.md` | format + keyword map for writing new content |

## Adding things
* **Article:** drop `content/articles/{slug}.php` (see CONTENT_SPEC.md). It appears on /blog, sitemap and search automatically.
* **Tool:** add to `inc/tools.php`, create `widgets/{slug}.php`, `content/tools/{slug}.php`, and a `T.<name>` function in `tools.js`.
* **Product:** add a key in `inc/products.php`, use `[[product:key]]` in content. Links carry tag `freegradecalculator-20`.

## Mail (contact form)
Sends from `info@freegradecalculator.com` via `smtp.hostinger.com:465`. Put the password in a file
**outside** public_html (e.g. `/home/u401386392/domains/<domain>/fgc-secrets.php`):
```php
<?php return ['smtp_pass' => 'MAILBOX-PASSWORD'];
```
Until then the form falls back to PHP `mail()`.

## Local preview
`php -S 127.0.0.1:8099 index.php`

## Deploy
Get upload credentials with the Hostinger API `hosting_files_generate-upload-url`, export
`FGC_URL`, `FGC_AUTH`, `FGC_REST`, then `./deploy.sh` (or `./deploy.sh path/to/file …`).
