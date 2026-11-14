<?php
// New Mexico Insurance Appraiser - canonical host guard. Required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nmia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nmia_real  = 'newmexicoinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nmia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://newmexicoinsuranceappraiser.com - only on the real domain.
if ($nmia_host === 'www.' . $nmia_real || ($nmia_host === $nmia_real && $nmia_proto === 'http')) {
    header('Location: https://' . $nmia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// /dir/index.php (and /index.php) are duplicate URLs: 301 to the directory.
$nmia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nmia_uri, '?'), $nmia_m)) {
    $nmia_q = strpos($nmia_uri, '?') !== false ? substr($nmia_uri, strpos($nmia_uri, '?')) : '';
    header('Location: ' . $nmia_m[1] . $nmia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($nmia_host !== $nmia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
