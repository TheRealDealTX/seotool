<?php
// Nebraska Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$nia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$nia_real  = 'nebraskainsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$nia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://nebraskainsuranceappraiser.com - only on the real domain.
if ($nia_host === 'www.' . $nia_real || ($nia_host === $nia_real && $nia_proto === 'http')) {
    header('Location: https://' . $nia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$nia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($nia_uri, '?'), $nia_m)) {
    $nia_q = strpos($nia_uri, '?') !== false ? substr($nia_uri, strpos($nia_uri, '?')) : '';
    header('Location: ' . $nia_m[1] . $nia_q, true, 301);
    exit;
}
// Keep temporary preview domains out of search results.
if ($nia_host !== $nia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
