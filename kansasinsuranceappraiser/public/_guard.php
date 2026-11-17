<?php
// Kansas Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$kia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$kia_real  = 'kansasinsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$kia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://kansasinsuranceappraiser.com - only on the real domain.
if ($kia_host === 'www.' . $kia_real || ($kia_host === $kia_real && $kia_proto === 'http')) {
    header('Location: https://' . $kia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
if (preg_match('#^(.*/)index\.php$#', strtok($_SERVER['REQUEST_URI'] ?? '/', '?'), $kia_m)) {
    $kia_q = strpos($_SERVER['REQUEST_URI'], '?') !== false ? substr($_SERVER['REQUEST_URI'], strpos($_SERVER['REQUEST_URI'], '?')) : '';
    header('Location: ' . $kia_m[1] . $kia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($kia_host !== $kia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
