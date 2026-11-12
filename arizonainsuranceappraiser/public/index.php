<?php
// Arizona Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$apex = 'arizonainsuranceappraiser.com';

// Canonical host and scheme - only on the real domain (TLS terminates upstream, so check X-Forwarded-Proto).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ? 'https' : 'http'));
if ($host === 'www.' . $apex || ($host === $apex && $proto === 'http')) {
    header('Location: https://' . $apex . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== $apex) {
    header('X-Robots-Tag: noindex, nofollow');
}

if (strpos($path, '..') !== false) {
    $path = '/__invalid__';
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    $qs = $_SERVER['QUERY_STRING'] ?? '';
    header('Location: ' . $path . '/' . ($qs !== '' ? '?' . $qs : ''), true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
