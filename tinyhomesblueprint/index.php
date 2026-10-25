<?php
// Tiny Homes Blueprint - front controller. .htaccess sends every request that is not a
// real file here; we resolve it against $ROUTES (inc/config.php) and render pages/<file>.
declare(strict_types=1);
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$PATH = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';

header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('X-Frame-Options: SAMEORIGIN');

function redirect(string $to, int $code = 301): void {
    header('Location: ' . SITE_URL . $to, true, $code);
    exit;
}

// Collapse duplicate slashes, /index.php and uppercase paths.
$clean = preg_replace('#/{2,}#', '/', $PATH);
if ($clean === '/index.php') $clean = '/';
if (strtolower($clean) !== $clean && isset($ROUTES[strtolower($clean)])) $clean = strtolower($clean);
if ($clean !== $PATH) redirect($clean . $qs);

if ($PATH === '/sitemap.xml') {
    require __DIR__ . '/pages/sitemap-xml.php';
    exit;
}

// Old WordPress URLs.
$key = substr($PATH, -1) === '/' || strpos(basename($PATH), '.') !== false ? $PATH : $PATH . '/';
if (isset($REDIRECTS[$key])) redirect($REDIRECTS[$key]);
if (preg_match('#^/(product|plans)/(plan-12-241[78])/?$#', $PATH, $m) && $PATH !== "/plans/{$m[2]}/") redirect("/plans/{$m[2]}/");
if (preg_match('#^/plan-category/#', $PATH)) redirect('/tiny-house-plans/');
if (preg_match('#^/(wp-json|feed|author|tag|category)(/|$)#', $PATH)) redirect('/');

// Enforce trailing slash on known routes.
if (substr($PATH, -1) !== '/' && isset($ROUTES[$PATH . '/'])) redirect($PATH . '/' . $qs);

if (!isset($ROUTES[$PATH])) {
    http_response_code(404);
    $ROUTE = ['type' => '404', 'title' => 'Page Not Found | ' . SITE_NAME, 'description' => ''];
    require __DIR__ . '/pages/404.php';
    exit;
}

$ROUTE = $ROUTES[$PATH];
header('Content-Type: text/html; charset=utf-8');
require __DIR__ . '/pages/' . $ROUTE['file'];
