<?php
// Maine Insurance Appraiser - canonical-host guard. Required first by index.php and by every page's dir/index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$mia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$mia_real  = 'maineinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$mia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
$mia_uri   = $_SERVER['REQUEST_URI'] ?? '/';
// 301 www. and plain http to https://maineinsuranceappraiser.com - only on the real domain.
if ($mia_host === 'www.' . $mia_real || ($mia_host === $mia_real && $mia_proto === 'http')) {
    header('Location: https://' . $mia_real . $mia_uri, true, 301);
    exit;
}
// /dir/index.php (or /index.php) duplicates /dir/: 301 to the directory, keeping any query string.
if (preg_match('#^(.*/)index\.php$#', (string) strtok($mia_uri, '?'), $mia_m)) {
    $mia_q = strpos($mia_uri, '?') !== false ? substr($mia_uri, strpos($mia_uri, '?')) : '';
    header('Location: ' . $mia_m[1] . $mia_q, true, 301);
    exit;
}
// Keep preview / temporary hosts out of search results.
if ($mia_host !== $mia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
