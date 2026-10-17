<?php
// evergrey-photography.com front controller. Serves the generated pages in
// _pages/ at clean, slash-less URLs (the original Wix paths such as /about and
// /post/<slug>), redirects legacy and trailing-slash variants, and returns a
// real 404 for everything else. The host ignores .htaccess, so this is the
// only place to enforce canonical URLs.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$qpos = strpos($uri, '?');
$qs   = $qpos === false ? '' : substr($uri, $qpos);
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$live = 'https://www.evergrey-photography.com';

function go($to) { header('Location: ' . $to, true, 301); exit; }

// Once the real domain is attached: force https and the www host.
if (preg_match('/(^|\.)evergrey-photography\.com$/', $host)) {
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($host !== 'www.evergrey-photography.com' || $insecure) go($live . $uri);
} else {
    // Temporary/preview hostname: keep it out of search results.
    header('X-Robots-Tag: noindex, nofollow');
}

// Legacy Wix paths and common guesses.
$aliases = [
    '/home' => '/', '/index.html' => '/', '/index.php' => '/',
    '/about-us' => '/about', '/about-me' => '/about',
    '/contact-us' => '/contact', '/book' => '/contact', '/inquire' => '/contact',
    '/gallery' => '/portfolio', '/galleries' => '/portfolio', '/work' => '/portfolio',
    '/investment' => '/pricing', '/packages' => '/pricing', '/prices' => '/pricing',
    '/services' => '/weddings', '/wedding' => '/weddings', '/elopement' => '/elopements',
    '/engagement' => '/engagements', '/couples' => '/engagements',
    '/post' => '/blog', '/posts' => '/blog', '/journal' => '/blog', '/blog-1' => '/blog',
    '/blog-feed.xml' => '/feed.xml', '/rss' => '/feed.xml',
];

if ($path !== '/' && substr($path, -1) === '/') go(rtrim($path, '/') . $qs);
if (strtolower($path) !== $path) go(strtolower($path) . $qs);
if (isset($aliases[$path])) go($aliases[$path] . $qs);
if (preg_match('#^/blog/(categories|tags|page|hashtags)(/|$)#', $path)) go('/blog');

$route = $path === '/' ? 'index' : substr($path, 1);
if (preg_match('#^[a-z0-9][a-z0-9\-/]*$#', $route) && strpos($route, '..') === false) {
    $file = __DIR__ . '/_pages/' . $route . '.html';
    if ($route !== '404' && is_file($file)) {
        header('Content-Type: text/html; charset=utf-8');
        header('Cache-Control: public, max-age=600');
        readfile($file);
        exit;
    }
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/_pages/404.html');
