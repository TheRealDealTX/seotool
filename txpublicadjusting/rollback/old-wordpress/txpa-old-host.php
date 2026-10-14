<?php
/**
 * Plugin Name: TXPA old-site host (archive)
 * Description: Lets the archived WordPress site run at old.txpublicadjusting.com
 * after txpublicadjusting.com moved to the new site. On that host only: URLs are
 * rewritten to the old.* host, canonical redirects are disabled, and every
 * response is noindex so the archive never competes with the live site.
 * On any other host this file does nothing. Delete it to undo.
 */
if (!isset($_SERVER['HTTP_HOST']) || stripos($_SERVER['HTTP_HOST'], 'old.txpublicadjusting.com') !== 0) {
    return;
}
$txpa_https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https');
$txpa_base = ($txpa_https ? 'https' : 'http') . '://old.txpublicadjusting.com';

add_filter('option_home', function () use ($txpa_base) { return $txpa_base; });
add_filter('option_siteurl', function () use ($txpa_base) { return $txpa_base; });
add_filter('redirect_canonical', '__return_false');
add_filter('robots_txt', function () { return "User-agent: *\nDisallow: /\n"; }, 99);
add_action('send_headers', function () { header('X-Robots-Tag: noindex, nofollow', true); });
add_action('wp_head', function () { echo '<meta name="robots" content="noindex, nofollow">' . "\n"; }, 0);
header('X-Robots-Tag: noindex, nofollow', true);
ob_start(function ($html) use ($txpa_base) {
    return str_replace(
        ['https://txpublicadjusting.com', 'http://txpublicadjusting.com', 'https:\/\/txpublicadjusting.com'],
        [$txpa_base, $txpa_base, str_replace('/', '\/', $txpa_base)],
        $html
    );
});
