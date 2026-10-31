# rodeotexas.org: adding blog articles

`app/bin/add-article.php` is installed on the server at
`/home/u401386392/domains/rodeotexas.org/app/bin/add-article.php` (outside public_html, command line only).

1. Write `app/data/article-<slug>.json` (same fields as an entry in the site's `app/data/articles.json`:
   slug, title, seo_title, meta_description, excerpt, content_html, featured_image, featured_alt,
   featured_width, featured_height, categories, published_at, updated_at; times are UTC).
2. Upload images to `public_html/wp-content/uploads/YYYY/MM/` (File Browser upload URL works).
3. Commit and push; note the 12-character commit SHA.
4. Hostinger cron (account u401386392), `* * * * *`:
   - `wget -qO /home/u401386392/domains/rodeotexas.org/app/data/article-<slug>.json https://raw.githubusercontent.com/TheRealDealTX/seotool/<sha12>/rodeo-texas-merch/main-site-tools/app/data/article-<slug>.json`
   - `/usr/bin/php /home/u401386392/domains/rodeotexas.org/app/bin/add-article.php /home/u401386392/domains/rodeotexas.org/app/data/article-<slug>.json`
     (add `--update` to replace the text of an existing article)
5. Watch the live URL, read the cron output ("Added: …" / "Updated: …"), then delete the temporary crons.

Posted so far: /rodeo-clown/ (id 22, 2026-10-31).
