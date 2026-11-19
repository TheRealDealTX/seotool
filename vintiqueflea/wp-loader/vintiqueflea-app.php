<?php
/**
 * Plugin Name: Vintique Flea site loader
 * Description: Hands every request to the custom PHP site in public_html/app.php before WordPress loads
 *              its theme or plugins. Delete this file to switch vintiqueflea.com back to WordPress.
 *
 * Why: this Hostinger Agency site runs a managed WordPress stack where the core files (including the
 * root index.php) are locked and nginx ignores .htaccess, so every request enters through WordPress.
 */
if ((defined('WP_CLI') && WP_CLI) || (defined('DOING_CRON') && DOING_CRON)) {
    return;
}
require ABSPATH . 'app.php';
exit;
