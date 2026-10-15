<?php
// Destin Hurricane (destinhurricane.com) - static site front controller. The host serves real
// files directly; anything else lands here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://destinhurricane.com';

// Canonical host/scheme on the live domain (the *.hostingersite.com preview
// address is left alone and marked noindex below).
if (substr($host, -strlen('destinhurricane.com')) === 'destinhurricane.com') {
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host === 'www.destinhurricane.com') {
        header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
        exit;
    }
}
if (strpos($host, 'hostingersite.com') !== false) {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
// Pages this domain served before the Destin rewrite (Oct 2026) -> their Destin replacements.
$moved = [
    '/denied-hurricane-claim/' => '/denied-hurricane-claim-destin/',
    '/underpaid-hurricane-claim/' => '/underpaid-hurricane-claim-destin/',
    '/delayed-hurricane-claim/' => '/delayed-hurricane-claim-destin/',
    '/insurance-claims/' => '/destin-hurricane-claim-lawyer/',
    '/hurricane-isaias-claims/' => '/hurricane-isaias-claims-destin/',
    '/the-lawgical-firm/' => '/our-firm/',
    '/hurricane-tracker/' => '/destin-hurricane-tracker/',
    '/weather/' => '/destin-weather/',
    '/evacuation-zones/' => '/okaloosa-walton-evacuation-zones/',
    '/shelters-roads-outages/' => '/walton-okaloosa-hurricane-shelters/',
    '/storm-surge-flood-risk/' => '/destin-storm-surge/',
    '/preparedness/' => '/hurricane-preparedness/',
    '/tools/' => '/hurricane-tools/',
    '/hurricane-history/' => '/destin-hurricane-history/',
    '/alerts/' => '/storm-alerts/',
    '/recovery/' => '/after-the-storm/',
];
$key = rtrim($path, '/') . '/';
$to = $moved[$key] ?? null;
if (!$to && preg_match('#^/(news|communities)/[^/]+/?$#', $path, $m) && !is_dir(__DIR__ . $path)) {
    $to = '/' . $m[1] . '/';
}
if ($to) {
    header('Location: ' . $home . $to, true, 301);
    exit;
}

if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
