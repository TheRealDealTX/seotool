<?php
// Front controller: every page on the site is routed through here.
// Local preview (php -S 127.0.0.1:8099 index.php): let the built-in server serve real files.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) return false;
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/content.php';
require __DIR__ . '/inc/art.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical scheme/host for the real domain (TLS terminates upstream).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if (($host === 'www.galvestonpublicadjuster.com') || ($insecure && str_ends_with($host, 'galvestonpublicadjuster.com'))) {
    header('Location: ' . SITE_URL . $uri, true, 301);
    exit;
}

const ROUTES = [
    '/'                         => 'home',
    '/about/'                   => 'about',
    '/twia-claims-expert/'      => 'twia',
    '/galveston-fire-claims/'   => 'fire',
    '/calculators/'             => 'calculators',
    '/texas-windstorm-rules/'   => 'windstorm-rules',
    '/galveston-local-code/'    => 'local-code',
    '/galveston-storm-history/' => 'storm-history',
    '/weather-events/'          => 'weather-events',
    '/blog/'                    => 'blog',
    '/contact/'                 => 'contact',
    '/thank-you/'               => 'thank-you',
    '/privacy-policy/'          => 'privacy',
];

if ($path === '/index.php') $path = '/';
if ($path === '/sitemap.xml') { require __DIR__ . '/inc/sitemap.php'; exit; }
if ($path === '/feed.xml' || $path === '/blog/feed/') { require __DIR__ . '/inc/feed.php'; exit; }

// Add the trailing slash to page URLs.
if ($path !== '/' && substr($path, -1) !== '/' && !str_contains(basename($path), '.')) {
    $q = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    header('Location: ' . $path . '/' . $q, true, 301);
    exit;
}

$page = ROUTES[$path] ?? null;
$vars = [];
if (!$page && preg_match('#^/blog/([a-z0-9-]+)/$#', $path, $mm) && blog_post($mm[1])) {
    $page = 'blog-post';
    $vars['post'] = blog_post($mm[1]);
}
if (!$page) {
    http_response_code(404);
    $page = '404';
}

$meta = ['path' => $path, 'schema' => []];
ob_start();
extract($vars);
include __DIR__ . '/pages/' . $page . '.php';
$body = ob_get_clean();
render_page($meta, $body);
