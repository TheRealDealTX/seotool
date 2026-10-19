<?php
// txlandscapelights.com - front controller. The host ignores .htaccess and routes
// "/" plus every unknown path here, so this serves the homepage, canonical
// redirects and real 404s. Existing files (pages, assets) are served directly.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://txlandscapelights.com';

// Canonical host and scheme, only once the real domain points here (preview domains pass through).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.txlandscapelights.com' || ($insecure && $host === 'txlandscapelights.com')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html') && strpos($path, '..') === false) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
