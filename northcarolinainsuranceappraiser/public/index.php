<?php
// North Carolina Insurance Appraiser - front controller for the static build.
// The host ignores .htaccess, serves real files directly and routes "/" and unknown paths here.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$home = 'https://northcarolinainsuranceappraiser.com';

// Canonical host and scheme, only on the real domain (TLS terminates upstream).
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off' ? 'http' : 'https'));
if ($host === 'www.northcarolinainsuranceappraiser.com' || ($host === 'northcarolinainsuranceappraiser.com' && $proto === 'http')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== 'northcarolinainsuranceappraiser.com') {
    header('X-Robots-Tag: noindex, nofollow');
}
if (strpos($path, '..') !== false || strpos($path, "\0") !== false) {
    $path = '/__invalid__';
}
$serve = function (string $file, int $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile($file);
    exit;
};
if ($path === '/' || $path === '/index.php') {
    $serve(__DIR__ . '/home.html');
}
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}
if (substr($path, -1) === '/' && is_file(__DIR__ . $path . 'index.html')) {
    $serve(__DIR__ . $path . 'index.html');
}
$serve(__DIR__ . '/404.html', 404);
