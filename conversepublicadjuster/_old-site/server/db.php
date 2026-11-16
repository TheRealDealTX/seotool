<?php
/**
 * conversepublicadjuster.com static-site front controller for Hostinger's Agency (H5G) WordPress platform.
 *
 * Installed as wp-content/db.php (a WordPress "drop-in" that WordPress loads on every request before
 * plugins, must-use plugins and the theme). It serves the static site files in the web root (index.html,
 * *.html, 404.html) in place of WordPress. The platform provisions the domain as a locked WordPress
 * install: index.php cannot be replaced, wp-content/mu-plugins/ is read-only and .htaccess is not
 * processed, so this is the earliest writable hook. wp-admin, wp-login and WP-Cron keep working.
 * It does not define $wpdb, so WordPress falls back to its normal database class.
 */
if (PHP_SAPI === 'cli' || (defined('WP_CLI') && WP_CLI)) {
    return;
}
// Only act when WordPress's front controller (index.php) is handling the request. Other scripts that load
// WordPress (wp-cron, wp-login, custom PHP that requires wp-load.php) are left alone.
if (basename($_SERVER['SCRIPT_NAME'] ?? '') !== 'index.php') {
    return;
}

$converse_uri  = $_SERVER['REQUEST_URI'] ?? '/';
$converse_path = parse_url($converse_uri, PHP_URL_PATH) ?: '/';

// Leave WordPress itself alone.
if (preg_match('#^/(wp-admin|wp-login\.php|wp-cron\.php|wp-json|xmlrpc\.php|wp-includes|wp-content)#', $converse_path)) {
    return;
}

$converse_root  = rtrim(ABSPATH, '/');
$converse_https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
               || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
$converse_host  = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Force HTTPS and non-www (what .htaccess would do on a normal Apache/LiteSpeed host).
if (!$converse_https || str_starts_with($converse_host, 'www.')) {
    header('Location: https://conversepublicadjuster.com' . $converse_uri, true, 301);
    exit;
}

// Resolve the static file: "/" -> index.html, "/about" -> about.html, "/blog/" -> blog/index.html
$converse_rel = trim($converse_path, '/');
// On Hostinger the homepage file is uploaded as home.html: if index.html exists in the web root, the
// platform serves it for EVERY unknown path (so /about and /blog/<slug> showed the homepage); with it
// absent, unknown paths fall through to index.php and this file resolves them to the right .html.
$converse_candidates = $converse_rel === ''
    ? ['home.html', 'index.html']
    : [$converse_rel, $converse_rel . '.html', $converse_rel . '/index.html'];

foreach ($converse_candidates as $converse_candidate) {
    $converse_file = realpath($converse_root . '/' . $converse_candidate);
    if ($converse_file
        && str_starts_with($converse_file, $converse_root . DIRECTORY_SEPARATOR)
        && is_file($converse_file)
        && substr($converse_file, -5) === '.html') {
        header('Content-Type: text/html; charset=utf-8');
        header('X-LiteSpeed-Cache-Control: public, max-age=3600');
        readfile($converse_file);
        exit;
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile($converse_root . '/404.html');
exit;
