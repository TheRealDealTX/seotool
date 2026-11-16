<?php
// Oregon Insurance Appraiser - canonical host guard, required by index.php and by every page's index.php.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === __FILE__) { http_response_code(404); exit; }
$oia_host  = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$oia_real  = 'oregoninsuranceappraiser.com';
// TLS terminates upstream: trust X-Forwarded-Proto, fall back to HTTPS.
$oia_proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http'));
// 301 www. and plain http to https://oregoninsuranceappraiser.com - only on the real domain.
if ($oia_host === 'www.' . $oia_real || ($oia_host === $oia_real && $oia_proto === 'http')) {
    header('Location: https://' . $oia_real . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// A page requested as /dir/index.php (or /index.php) is a duplicate URL: 301 to the directory.
$oia_uri = $_SERVER['REQUEST_URI'] ?? '/';
if (preg_match('#^(.*/)index\.php$#', strtok($oia_uri, '?'), $oia_m)) {
    $oia_q = strpos($oia_uri, '?') !== false ? substr($oia_uri, strpos($oia_uri, '?')) : '';
    header('Location: ' . $oia_m[1] . $oia_q, true, 301);
    exit;
}
// Keep preview domains out of search results.
if ($oia_host !== $oia_real) {
    header('X-Robots-Tag: noindex, nofollow');
}
header('Content-Type: text/html; charset=utf-8');
