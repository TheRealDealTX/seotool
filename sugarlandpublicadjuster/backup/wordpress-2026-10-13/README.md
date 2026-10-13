# WordPress backup — sugarlandpublicadjuster.com (2026-10-13)

The custom PHP site replaced WordPress by overwriting only two files in
`public_html`: `index.php` and `.htaccess`. Their WordPress originals are saved
here (`index.php.txt`, `htaccess.txt`). Every other WordPress file
(`wp-admin/`, `wp-includes/`, `wp-content/`, `wp-config.php`) and the MySQL
database were left untouched on the server, and Hostinger's automatic daily
backups cover the account.

New directories the PHP site added (`about-us/`, `blog/`, `services/`, …) would
shadow WordPress permalinks, so delete them too if you ever roll back.

**To roll back to WordPress:** upload `index.php.txt` as `public_html/index.php`
and `htaccess.txt` as `public_html/.htaccess`, delete the new site
directories, then clear the cache in hPanel.
