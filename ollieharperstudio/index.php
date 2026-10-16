<?php
// ollieharperstudio.com - front controller. See README, "Hosting".
// The host serves existing files directly and ignores .htaccess, so pages are kept
// in _pages/ (not directly servable) and every page request lands here first.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$canonicalHost = 'ollieharperstudio.com';

// Canonical scheme + host, only once the real domain is attached
// (the temporary *.hostingersite.com preview is left alone).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';   // TLS ends upstream
if ($host === 'www.' . $canonicalHost || ($host === $canonicalHost && $insecure)) {
    // Add a page's missing trailing slash in the same hop, so there is never a redirect chain.
    $slug0 = trim($path, '/');
    if (preg_match('#^[a-z0-9-]+(/[a-z0-9-]+)*$#', $slug0) && substr($path, -1) !== '/' && is_file(__DIR__ . '/_pages/' . $slug0 . '.php')) {
        $uri = $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '');
    }
    header('Location: https://' . $canonicalHost . $uri, true, 301);
    exit;
}

function go($to) { header('Location: ' . $to, true, 301); exit; }
function page($file, $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    if ($code >= 400) header('X-Robots-Tag: noindex');
    readfile(__DIR__ . '/' . $file);
    exit;
}

define('OH_PAGE', true);
if ($path === '/index.php') go('/');
// Rebuilt pages: /culinary/ -> _pages/culinary.php, / -> _pages/home.php.
$slug = trim($path, '/');
if ($slug === '' || ($slug !== 'home' && preg_match('#^[a-z0-9-]+(/[a-z0-9-]+)*$#', $slug))) {
    $file = __DIR__ . '/_pages/' . ($slug === '' ? 'home' : $slug) . '.php';
    if (is_file($file)) {
        if (substr($path, -1) !== '/') go($path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''));
        header('Content-Type: text/html; charset=utf-8');
        include $file;
        exit;
    }
}

// Legacy Squarespace URLs (2014-2017) -> their rebuilt equivalents.
$legacy = [
    '/commercial' => '/', '/design' => '/', '/fashion' => '/images/', '/fashion-illustration' => '/images/',
    '/prop-styling' => '/set-stylingdirection/', '/aboutamber' => '/about/', '/blog' => '/thoughts/',
    '/home' => '/', '/home.html' => '/', '/index.html' => '/',
];
$key = rtrim($path, '/');
if (isset($legacy[$key])) go($legacy[$key]);
if (preg_match('#^/\d{4}/\d{1,2}/\d{1,2}/#', $path)) go('/projects/');          // old Squarespace blog permalinks
if (preg_match('#^/(blog|thoughts)/?.*format=rss#i', $uri)) go('/thoughts/');

// 2018 spam pages left by a previous owner of the domain: tell crawlers they are gone for good.
if (preg_match('#^/[a-z0-9-]+/[^/]+\.php$#i', $path)
    || preg_match('#^/(images|img|fonts)/.+\.[a-z0-9]{2,5}$#i', $path)
    || preg_match('#\.php$#i', $path)) {
    page('410.html', 410);
}

page('404.html', 404);
