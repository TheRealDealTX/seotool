<?php
// saffronsupplement.com front controller. Every page request lands here:
// the host serves real files (assets, robots.txt) directly and routes
// everything else to this file. See README.md, "Hosting".
// Local preview (php -S 127.0.0.1:8099 index.php): let the dev server serve real files.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) return false;

define('SS_APP', true);
require __DIR__ . '/app/config.php';
require __DIR__ . '/app/products.php';
require __DIR__ . '/app/routes.php';
require __DIR__ . '/app/layout.php';

$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$path = '/' . ltrim(preg_replace('#/+#', '/', rawurldecode($path)), '/');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$qs   = isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : '';

// Canonical scheme + host (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.saffronsupplement.com' || ($host === 'saffronsupplement.com' && $insecure)) {
    redirect(SITE_ORIGIN . $path . $qs);
}

if ($path === '/index.php') redirect('/');
if ($path === '/sitemap.xml' || $path === '/sitemap_index.xml') { render_sitemap(); exit; }
if ($path === '/feed.xml') { render_feed(); exit; }

if (isset(REDIRECTS[$path])) redirect(REDIRECTS[$path]);
if (isset(REDIRECTS[$path . '/'])) redirect(REDIRECTS[$path . '/']);
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php|author|category|tag)(/|$)#', $path)) redirect('/');

if (!isset(ROUTES[$path]) && isset(ROUTES[$path . '/'])) redirect($path . '/' . $qs);

if (!isset(ROUTES[$path])) {
    http_response_code(404);
    render_page('/404', ['file' => '404', 'type' => 'page', 'title' => 'Page Not Found | ' . SITE_NAME,
        'desc' => 'This page could not be found.', 'h1' => 'Page not found', 'noindex' => true]);
    exit;
}

render_page($path, ROUTES[$path]);

function redirect($to) {
    header('Location: ' . $to, true, 301);
    exit;
}
