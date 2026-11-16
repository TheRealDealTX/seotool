<?php
/**
 * conversepublicadjuster.com static-site front controller for Hostinger's Agency (H5G) WordPress platform.
 *
 * Installed as wp-content/db.php (a WordPress "drop-in" that WordPress loads on every request before
 * plugins, must-use plugins and the theme). It serves the static site files in the web root (home.html,
 * <dir>/index.html, 404.html) in place of WordPress. The platform provisions the domain as a locked
 * WordPress install: index.php cannot be replaced, wp-content/mu-plugins/ is read-only and .htaccess is
 * not processed, so this is the earliest writable hook and the only place 301 redirects can live.
 * wp-admin, wp-login and WP-Cron keep working. It does not define $wpdb, so WordPress falls back to its
 * normal database class.
 */
if (PHP_SAPI === 'cli' || (defined('WP_CLI') && WP_CLI)) {
    return;
}
// Only act when WordPress's front controller (index.php) is handling the request. Other scripts that load
// WordPress (wp-cron, wp-login, custom PHP that requires wp-load.php) are left alone.
if (basename($_SERVER['SCRIPT_NAME'] ?? '') !== 'index.php') {
    return;
}

$sa_uri  = $_SERVER['REQUEST_URI'] ?? '/';
$sa_path = parse_url($sa_uri, PHP_URL_PATH) ?: '/';

// Leave WordPress itself alone.
if (preg_match('#^/(wp-admin|wp-login\.php|wp-cron\.php|wp-json|xmlrpc\.php|wp-includes|wp-content)#', $sa_path)) {
    return;
}

$sa_origin = 'https://conversepublicadjuster.com';
$sa_root   = rtrim(ABSPATH, '/');
$sa_https  = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
          || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
$sa_host   = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Force HTTPS and non-www (what .htaccess would do on a normal Apache/LiteSpeed host).
if (!$sa_https || str_starts_with($sa_host, 'www.')) {
    header('Location: ' . $sa_origin . $sa_uri, true, 301);
    exit;
}

// 301 redirects from the old Converse / storm-dated site to the closest evergreen page.
// Keys are matched with and without a trailing slash and with or without a ".html" suffix.
$sa_redirects = [
    '/converse-hail-storm-september-2026' => '/services/hail-damage-claims/',
    '/about'   => '/about/',
    '/contact' => '/contact/',
    '/blog'    => '/blog/',
    '/home'    => '/',
    '/index'   => '/',
    '/blog/index' => '/blog/',
    '/blog/how-to-get-insurance-to-pay-for-roof-replacement-after-the-converse-hail-storm'
        => '/blog/how-to-get-insurance-to-pay-for-a-roof-replacement-in-san-antonio/',
    '/blog/hail-damage-roof-inspection-converse-before-the-heat-bakes-it-in'
        => '/blog/hail-damage-roof-inspection-san-antonio/',
    '/blog/seven-line-items-missing-from-your-hail-roof-estimate'
        => '/blog/line-items-missing-from-san-antonio-roof-estimates/',
    '/blog/door-knockers-in-converse-what-texas-law-lets-a-roofer-do'
        => '/blog/door-knocking-roofers-texas-law/',
    '/blog/appraisal-clause-explained-for-bexar-county-homeowners'
        => '/blog/appraisal-clause-explained-san-antonio/',
    '/blog/acv-vs-rcv-why-the-first-check-is-smaller-than-the-estimate'
        => '/blog/acv-vs-rcv-insurance-check-explained/',
    '/blog/hail-history-of-converse-and-northeast-bexar-county'
        => '/blog/san-antonio-hail-history/',
];
$sa_key = preg_replace('#\.html$#', '', rtrim($sa_path, '/'));
if ($sa_key === '') {
    $sa_key = '/';
}
if ($sa_key !== '/' && isset($sa_redirects[$sa_key]) && $sa_path !== $sa_redirects[$sa_key]) {
    header('Location: ' . $sa_origin . $sa_redirects[$sa_key], true, 301);
    exit;
}

// Resolve the static file: "/" -> home.html, "/about/" -> about/index.html.
// The homepage file is home.html on purpose: if index.html exists in the web root, the platform serves it
// for EVERY unknown path with a 200; with it absent, unknown paths fall through to index.php and this file.
$sa_rel = trim($sa_path, '/');
if ($sa_rel === '') {
    $sa_candidates = ['home.html'];
} else {
    // A directory page requested without its trailing slash gets a 301 to the canonical URL.
    if (substr($sa_path, -1) !== '/' && is_file($sa_root . '/' . $sa_rel . '/index.html')) {
        header('Location: ' . $sa_origin . $sa_path . '/', true, 301);
        exit;
    }
    $sa_candidates = [$sa_rel . '/index.html', $sa_rel, $sa_rel . '.html'];
}

foreach ($sa_candidates as $sa_candidate) {
    $sa_file = realpath($sa_root . '/' . $sa_candidate);
    if ($sa_file
        && str_starts_with($sa_file, $sa_root . DIRECTORY_SEPARATOR)
        && is_file($sa_file)
        && substr($sa_file, -5) === '.html') {
        header('Content-Type: text/html; charset=utf-8');
        header('X-LiteSpeed-Cache-Control: public, max-age=3600');
        readfile($sa_file);
        exit;
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile($sa_root . '/404.html');
exit;
