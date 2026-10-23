<?php
// dogearcleaner.com - static site front controller. See README, "Hosting".
// The host serves existing files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$home = 'https://dogearcleaner.com';

function go($url) { header('Location: ' . $url, true, 301); exit; }

// Canonical scheme and host (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || ($_SERVER['HTTP_HOST'] ?? '') === 'www.dogearcleaner.com') {
    go($home . $uri);
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: public, max-age=600');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress / Yoast URLs.
if (preg_match('#^/(sitemap_index|post-sitemap|page-sitemap|category-sitemap|author-sitemap|wp-sitemap[a-z0-9-]*)\.xml$#', $path)) go($home . '/sitemap.xml');
if (preg_match('#^/(feed|comments/feed)/?$#', $path)) go($home . '/resources/');
if (preg_match('#^/([a-z0-9-]+)/feed/?$#', $path, $m) && is_dir(__DIR__ . '/' . $m[1])) go($home . '/' . $m[1] . '/');
if (preg_match('#^/topic/([a-z-]+)/(page/\d+/?|feed/?)$#', $path, $m) && is_dir(__DIR__ . '/topic/' . $m[1])) go($home . '/topic/' . $m[1] . '/');
if (preg_match('#^/resources/page/\d+/?$#', $path)) go($home . '/resources/');
if (preg_match('#^/author/#', $path)) go($home . '/about-us/');
if (preg_match('#^/category/(how-to|reviews|guides)/?$#', $path, $m)) go($home . '/topic/' . $m[1] . '/');
if ($path === '/home-2/' || $path === '/dog-ear-cleaner/' || $path === '/home/') go($home . '/');
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) go($home . '/');

// Directory without trailing slash.
if (substr($path, -1) !== '/' && strpos($path, '..') === false && is_dir(__DIR__ . $path)) go($home . $path . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
