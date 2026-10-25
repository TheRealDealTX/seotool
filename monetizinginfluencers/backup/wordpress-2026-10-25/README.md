# WordPress backup (2026-10-25)

monetizinginfluencers.com ran WordPress + Elementor + Yoast + LiteSpeed Cache until the
custom PHP rebuild went live on 2026-10-25.

The WordPress install was **not deleted**. Its files (`wp-admin/`, `wp-includes/`,
`wp-content/`, `wp-config.php`, ...) and its database are untouched on the server.
The new `.htaccess` blocks every WordPress entry point except `wp-content/uploads/`
(old image URLs keep working).

Only two WordPress files were overwritten by the rebuild:

| Live path | Copy here | Also on server at |
| --- | --- | --- |
| `public_html/.htaccess` | `htaccess.txt` | `public_html/_wp-backup/htaccess.txt` |
| `public_html/index.php` | `index.php.txt` | `public_html/_wp-backup/index.php.txt` |

`htaccess.bk.txt` is the older `.htaccess.bk` that was already on the server (left in place).

## Roll back to WordPress

1. Upload `htaccess.txt` as `public_html/.htaccess` and `index.php.txt` as `public_html/index.php`.
2. Optionally delete the new site's folders (`assets/`, `inc/`, `api/`, `monetization/`, ...).
3. Purge the LiteSpeed cache in hPanel.
