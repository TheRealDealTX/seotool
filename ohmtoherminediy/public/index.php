<?php
// ohmtoherminediy.com - static site front controller.
// The host serves existing files directly, ignores .htaccess, and sends "/" and
// unknown paths here. So: serve home.html for "/", 301 old WordPress-style URLs
// to their new homes, and return 404.html with a real 404 for everything else.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$prod = 'ohmtoherminediy.com';

// Canonical host/scheme only once the real domain is attached (temp domain is left alone).
if ($host === 'www.' . $prod || ($host === $prod && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: https://' . $prod . $uri, true, 301);
    exit;
}
if ($host !== $prod) {
    header('X-Robots-Tag: noindex, nofollow'); // staging/temporary domain
}

function go($to) { header('Location: ' . $to, true, 301); exit; }

if ($path === '/' || $path === '/index.php') {
    if (isset($_GET['p']) || isset($_GET['page_id'])) go('/');
    if (isset($_GET['s'])) go('/blog/');
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$routes = json_decode(@file_get_contents(__DIR__ . '/routes.json'), true) ?: ['posts' => [], 'categories' => []];
$p = rtrim($path, '/');

// WordPress leftovers
if ($p === '/feed') {
    header('Content-Type: application/rss+xml; charset=utf-8');
    readfile(__DIR__ . '/feed.xml');
    exit;
}
if (preg_match('#^/(comments/feed|rss|blog/feed|feed\.xml|rss\.xml|atom)$#', $p)) go('/feed/');
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content)(/|$)#', $path)) go('/');
if (preg_match('#^/(tag|tags)/#', $path)) go('/blog/');
if (preg_match('#^/author/#', $path)) go('/about/');
if (preg_match('#^/(page/\d+|blog/page/\d+)$#', $p)) go('/blog/');
if (preg_match('#^/category/([^/]+)(/.*)?$#', $p, $m)) go(in_array($m[1], $routes['categories']) ? '/category/' . $m[1] . '/' : '/blog/');
if (preg_match('#^/(contact-us|contact-me)$#', $p)) go('/contact/');
if (preg_match('#^/(about-us|about-me)$#', $p)) go('/about/');
if (preg_match('#^/(privacy|privacy-policy-2)$#', $p)) go('/privacy-policy/');
if (preg_match('#^/(terms-of-use|terms-and-conditions|terms-of-service)$#', $p)) go('/terms/');
if (preg_match('#^/(shop|store|projects|diy-projects|diy)$#', $p)) go('/blog/');

// Old flat (/slug/) or dated (/2019/05/12/slug/) permalinks -> /blog/slug/
if (preg_match('#^/(?:\d{4}/\d{2}(?:/\d{2})?/)?([a-z0-9-]+)$#', $p, $m)) {
    if (in_array($m[1], $routes['posts'])) go('/blog/' . $m[1] . '/');
}
if (preg_match('#^/\d{4}(/\d{2})?(/\d{2})?$#', $p)) go('/blog/');

// Directory without trailing slash
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) go($path . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
