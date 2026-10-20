# Live WordPress site before the rebuild went live (2026-10-20)

Hosting account u401386392, domain publicadjustersdallas.com, document root
/home/u401386392/domains/publicadjustersdallas.com/public_html.

The new site was uploaded OVER the WordPress install; WordPress core, wp-config.php and
wp-content/ were left on the server untouched. Only these two files were replaced:

* `index.php`  (WordPress front controller) — copy: `index.php.wordpress`
* `.htaccess`  (LiteSpeed Cache + WordPress rules) — copy: `htaccess.wordpress`

Rollback: put those two files back in public_html and purge the LiteSpeed cache.
The WordPress database is untouched.
