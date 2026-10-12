<?php
// fraserandmorris.com - front controller. The host serves existing files directly
// and routes "/" plus every unknown path here (it ignores .htaccess).
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$scheme = 'https://';

// Once the real domain is attached: force https and the bare domain.
if ($host === 'www.fraserandmorris.com' || ($host === 'fraserandmorris.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: https://fraserandmorris.com' . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
$base = $scheme . ($host !== '' ? $host : 'fraserandmorris.com');

// Temporary preview domains must not be indexed.
if ($host !== 'fraserandmorris.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Legacy URLs from the old site.
$redirects = [
    '/index.html' => '/',
    '/index.htm' => '/',
    '/home.html' => '/',
    '/gardens/index.html' => '/gardens.html',
    '/gardens/' => '/gardens.html',
    '/gardens' => '/gardens.html',
    '/press.html' => '/about.html',
    '/news.html' => '/about.html',
    '/pdfs/GardensIllustrated.pdf' => '/gardens/artists.html',
];
if (isset($redirects[$path])) {
    header('Location: ' . $base . $redirects[$path], true, 301);
    exit;
}
if (preg_match('#^/pdfs/#i', $path)) {
    header('Location: ' . $base . '/about.html', true, 301);
    exit;
}
// Old per-garden image folders (e.g. /gardens/fox/fox1.jpg) -> that garden's page.
if (preg_match('#^/gardens/([a-z]+)/[^/]+\.(jpe?g|png|gif)$#i', $path, $m) && is_file(__DIR__ . '/gardens/' . strtolower($m[1]) . '.html')) {
    header('Location: ' . $base . '/gardens/' . strtolower($m[1]) . '.html', true, 301);
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
