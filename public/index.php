<?php
/**
 * solarcctvcamera.com front controller.
 *
 * The Hostinger platform serves real files directly and sends every other
 * request here, so this file owns canonical-host redirects, the legacy
 * WordPress redirects, page routing, sitemap.xml and real 404s.
 */
define('SCC', true);
require __DIR__ . '/inc/bootstrap.php';
require __DIR__ . '/inc/routes.php';
require __DIR__ . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical scheme + host (TLS terminates upstream; REQUEST_SCHEME is always http here).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? 'https') === 'http';
if ($host === 'www.solarcctvcamera.com' || ($insecure && $host === 'solarcctvcamera.com')) {
    header('Location: ' . SITE_ORIGIN . $uri, true, 301);
    exit;
}

// Never expose private folders, even though their files guard themselves.
if (preg_match('#^/(inc|content|pages)(/|$)#', $path)) {
    not_found();
}

if ($path === '/index.php') {
    header('Location: ' . SITE_ORIGIN . '/', true, 301);
    exit;
}

if ($path === '/sitemap.xml') {
    require __DIR__ . '/inc/sitemap.php';
    exit;
}

if ($path === '/contact/send' && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    require __DIR__ . '/inc/contact-handler.php';
    exit;
}

$routes = routes();

// Trailing-slash normalisation for known routes.
if (!isset($routes[$path]) && isset($routes[$path . '/'])) {
    header('Location: ' . SITE_ORIGIN . $path . '/' . (isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : ''), true, 301);
    exit;
}

$redirects = redirects();
$key = rtrim($path, '/') . (str_ends_with($path, '.xml') ? '' : '/');
if (isset($redirects[$key]) || isset($redirects[$path])) {
    header('Location: ' . SITE_ORIGIN . ($redirects[$path] ?? $redirects[$key]), true, 301);
    exit;
}
// Any other legacy WordPress endpoint.
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php|tag|category|author|page)(/|$)#', $path)) {
    header('Location: ' . SITE_ORIGIN . '/', true, 301);
    exit;
}

if (!isset($routes[$path])) {
    not_found();
}

[$kind, $source, $section] = $routes[$path];
header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');

if ($kind === 'article') {
    require __DIR__ . '/inc/article.php';
    render_article($path, $source, $section);
} elseif ($kind === 'tool') {
    require __DIR__ . '/inc/article.php';
    require __DIR__ . '/pages/tools/_render.php';
    render_tool($path, $source);
} else {
    require __DIR__ . "/pages/$source.php";
}

function not_found(): void
{
    http_response_code(404);
    header('Content-Type: text/html; charset=utf-8');
    require ROOT . '/pages/404.php';
    exit;
}
