<?php
// Utah Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$uia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$uia_real  = 'utahinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$uia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://utahinsuranceappraiser.com - only on the real domain.
if ($uia_host === 'www.' . $uia_real || ($uia_host === $uia_real && $uia_proto === 'http')) {
    header('Location: https://' . $uia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$uia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($uia_uri, '?'), $uia_m)) {
    $uia_q = strpos($uia_uri, '?') !== false ? substr($uia_uri, strpos($uia_uri, '?')) : '';
    header('Location: ' . $uia_m[1] . $uia_q, true, 301);
    exit;
}
// Keep the temporary preview domain (and any other host) out of search results.
if ($uia_host !== $uia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
