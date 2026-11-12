<?php
// New Jersey Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nja_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nja_real  = 'newjerseyinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nja_proto = strtolower(trim(explode(',', $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'))[0]));
// 301 www. and plain http to https://newjerseyinsuranceappraiser.com - only on the real domain.
if ($nja_host === 'www.' . $nja_real || ($nja_host === $nja_real && $nja_proto === 'http')) {
    header('Location: https://' . $nja_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$nja_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nja_uri, '?'), $nja_m)) {
    $nja_q = strpos($nja_uri, '?') !== false ? substr($nja_uri, strpos($nja_uri, '?')) : '';
    header('Location: ' . $nja_m[1] . $nja_q, true, 301);
    exit;
}
// Keep preview and temporary domains out of search results.
if ($nja_host !== $nja_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
