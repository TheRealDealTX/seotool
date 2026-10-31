# WordPress rollback files

The rebuild leaves the WordPress install (wp-admin, wp-content, wp-includes, the
database) untouched in `public_html`. It only overwrites two WordPress files:

- `.htaccess` → original saved here as `htaccess.original`
- `index.php` → original saved here as `index.php.original`

To roll back to WordPress: upload these two files back to `public_html` under
their original names (`.htaccess`, `index.php`), delete the new `index.html`,
and purge the LiteSpeed cache in hPanel. Static folders left behind
(e.g. `/tools/`) are harmless but can be deleted.
