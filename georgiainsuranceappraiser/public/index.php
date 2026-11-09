<?php
// Georgia Insurance Appraiser - front controller for the static build.
// The host serves real files directly and routes "/" and unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://georgiainsuranceappraiser.com';

// Canonical host/scheme - only once the real domain is connected.
if ($host === 'www.georgiainsuranceappraiser.com' ||
    ($host === 'georgiainsuranceappraiser.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($host !== 'georgiainsuranceappraiser.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
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
