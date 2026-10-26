<?php
// Better Outdoors - front controller.
// The Hostinger Agency platform serves real files directly and sends every
// other request here (it ignores .htaccess), so all routing and redirects live
// in this file. .htaccess mirrors it for plain Apache hosts.

if (PHP_SAPI === 'cli-server') {
    // Local preview: `php -S localhost:8000 index.php`
    $f = __DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    if (is_file($f) && basename($f) !== 'index.php') return false;
}

define('BO', true);
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/helpers.php';
require __DIR__ . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$live = in_array($host, ['betteroutdoors.net', 'www.betteroutdoors.net'], true);

function redirect($to, $code = 301) {
    header('Location: ' . $to, true, $code);
    exit;
}

// Canonical scheme and host (only on the real domain, never on preview hosts).
if ($live) {
    // Agency platform: TLS ends upstream and X-Forwarded-Proto says so.
    // Classic hosting (LiteSpeed): no such header, so fall back to HTTPS.
    $xfp = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '');
    $insecure = $xfp !== '' ? $xfp === 'http' : (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off');
    if ($insecure || $host === 'www.betteroutdoors.net') redirect(SITE_URL . $uri);
} else {
    header('X-Robots-Tag: noindex, nofollow');
}

// Legacy WordPress query URLs.
if ($path === '/' && isset($_GET['s'])) redirect('/blog/?q=' . rawurlencode((string)$_GET['s']));
if ($path === '/' && isset($_GET['p'])) redirect('/blog/');

// Legacy WordPress / stray paths -> nearest live page.
$legacy = [
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-signup\.php)(/|$)#' => '/',
    '#^/(comments/)?feed/?$#'                    => '/blog/',
    '#^/(blog|category/tips)/page/\d+/?$#'       => null, // handled below
    '#^/category/(?!tips/?$)[^/]+/?#'            => '/category/tips/',
    '#^/(tag|author)/[^/]+/?#'                   => '/blog/',
    '#^/pages/contact(-us)?/?$#'                 => '/contact-us/',
    '#^/pages/about(-us)?/?$#'                   => '/about-us/',
    '#^/collections/#'                           => '/understanding-mathews-compound-bow-packages/',
    '#^/products/#'                              => '/blog/',
    '#^/(home|index\.html?|sample-page)/?$#'     => '/',
    '#^/contact/?$#'                             => '/contact-us/',
    '#^/about/?$#'                               => '/about-us/',
];
foreach ($legacy as $re => $to) {
    if (!preg_match($re, $path, $mm)) continue;
    if ($to !== null) redirect($to);
    if (str_contains($path, '/page/')) redirect('/' . $mm[1] . '/');
}
// /{post}/feed/, /{post}/amp/, /{post}/attachment/... -> the post itself.
if (preg_match('#^/([a-z0-9-]+)/(feed|amp|embed|attachment/.*|comment-page-\d+)/?$#', $path, $mm) && isset($POSTS[$mm[1]])) {
    redirect('/' . $mm[1] . '/');
}

// Sitemaps (the WordPress sitemap URLs keep working too).
if (preg_match('#^/(sitemap|sitemap_index|wp-sitemap|post-sitemap|page-sitemap|category-sitemap|tool-sitemap)\.xml$#', $path, $mm)) {
    require __DIR__ . '/pages/sitemap.php';
    render_sitemap($mm[1]);
    exit;
}

// Route table: path => page file.
$routes = [
    '/'                => 'home',
    '/blog/'           => 'blog',
    '/category/tips/'  => 'category-tips',
    '/about-us/'       => 'about-us',
    '/contact-us/'     => 'contact-us',
    '/privacy-policy/' => 'privacy-policy',
    '/terms-of-use/'   => 'terms-of-use',
    '/tools/'          => 'tools',
];
foreach ($POSTS as $slug => $_) $routes['/' . $slug . '/'] = 'post';
foreach ($TOOLS as $slug => $_) $routes['/tools/' . $slug . '/'] = 'tool';

if ($path === '/index.php') $path = '/';

// Missing trailing slash on a known route -> 301 to the slashed URL.
if (!isset($routes[$path]) && isset($routes[$path . '/'])) {
    $qs = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    redirect($path . '/' . $qs);
}

if (!isset($routes[$path])) {
    http_response_code(404);
    require __DIR__ . '/pages/404.php';
    exit;
}

header('Content-Type: text/html; charset=utf-8');
$page = $routes[$path];
if ($page === 'post') {
    $slug = trim($path, '/');
} elseif ($page === 'tool') {
    $slug = basename($path);
}
require __DIR__ . '/pages/' . $page . '.php';
