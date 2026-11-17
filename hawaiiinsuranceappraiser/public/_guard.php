<?php
// Hawaii Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$hia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$hia_real  = 'hawaiiinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$hia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://hawaiiinsuranceappraiser.com - only on the real domain.
if ($hia_host === 'www.' . $hia_real || ($hia_host === $hia_real && $hia_proto === 'http')) {
    header('Location: https://' . $hia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $hia_m)) {
    $hia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $hia_m[1] . $hia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($hia_host !== $hia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
