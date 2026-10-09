<?php
// ollieharperstudio.com - static site front controller. See README, "Hosting".
// The host serves existing files directly and ignores .htaccess, so every
// request for a path that is not a file on disk lands here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$canonicalHost = 'ollieharperstudio.com';

// Canonical scheme + host, only once the real domain is attached
// (the temporary *.hostingersite.com preview is left alone).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';   // TLS ends upstream
if ($host === 'www.' . $canonicalHost || ($host === $canonicalHost && $insecure)) {
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

if ($path === '/' || $path === '/index.php') page('home.html');

// Legacy Squarespace URLs (2014-2017) -> their rebuilt equivalents.
$legacy = [
    '/commercial' => '/', '/design' => '/', '/fashion' => '/images/', '/fashion-illustration' => '/images/',
    '/prop-styling' => '/set-stylingdirection/', '/aboutamber' => '/about/', '/blog' => '/thoughts/',
    '/home' => '/', '/home.html' => '/',
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

// Directory without its trailing slash -> add it.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    go($path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''));
}

page('404.html', 404);
